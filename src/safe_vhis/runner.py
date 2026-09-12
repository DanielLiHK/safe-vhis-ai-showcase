from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import Settings, validate_models
from .guardrails import citations_are_valid, deterministic_response, route_question
from .knowledge import load_cases, load_sources, retrieve
from .prompts import build_messages
from .provider import QwenClient
from .schemas import Action, ExperimentArm, RunRecord


def _write_record(path: Path, record: RunRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(record.model_dump_json() + "\n")


def run_experiment(models: list[str], limit: int | None = None, output: Path | None = None) -> Path:
    validate_models(models)
    settings = Settings.from_env()
    client = QwenClient(settings)
    sources = load_sources()
    cases = load_cases()[:limit]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output_path = output or Path("results/raw") / f"{run_id}.jsonl"
    all_source_ids = {item.id for item in sources}

    for model in models:
        for case in cases:
            for arm in ExperimentArm:
                retrieved = [] if arm == ExperimentArm.BASELINE else retrieve(
                    f"{case.question_zh_hk} {case.question_en}", sources
                )
                started = time.perf_counter()
                error = None
                prompt_tokens = None
                completion_tokens = None
                try:
                    route = route_question(f"{case.question_zh_hk} {case.question_en}")
                    if arm == ExperimentArm.GUARDED and route is not None:
                        answer = deterministic_response(route)
                    elif arm == ExperimentArm.GUARDED and not retrieved:
                        # Fail closed without consulting the gold label. Using the expected
                        # action here would leak test answers into the system under test.
                        answer = deterministic_response(Action.ASK_CLARIFICATION)
                    else:
                        result = client.complete(
                            model,
                            build_messages(case.question_zh_hk, case.question_en, arm, retrieved),
                        )
                        answer = result.answer
                        prompt_tokens = result.prompt_tokens
                        completion_tokens = result.completion_tokens
                except Exception as exc:  # Preserve failures as data; do not silently drop them.
                    error = f"{type(exc).__name__}: {exc}"
                    # A provider or parsing failure must never use the gold label.
                    answer = deterministic_response(Action.REFER_TO_HUMAN)
                elapsed_ms = int((time.perf_counter() - started) * 1000)
                allowed = all_source_ids if arm == ExperimentArm.BASELINE else {item.id for item in retrieved}
                if arm == ExperimentArm.BASELINE:
                    citation_valid = not answer.citations
                elif answer.action.value != "ANSWER":
                    citation_valid = not answer.citations
                else:
                    citation_valid = citations_are_valid(answer.citations, allowed)
                record = RunRecord(
                    run_id=run_id,
                    timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    model=model,
                    arm=arm,
                    case_id=case.id,
                    expected_action=case.expected_action,
                    retrieved_source_ids=[item.id for item in retrieved],
                    output=answer,
                    citation_ids_valid=citation_valid,
                    latency_ms=elapsed_ms,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    error=error,
                )
                _write_record(output_path, record)
    return output_path
