from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluation import make_grade_template, summarize_grades, write_summary
from .guardrails import deterministic_response, route_question
from .knowledge import load_cases, load_sources, retrieve
from .prompts import build_messages
from .runner import run_experiment
from .schemas import ExperimentArm


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="safe-vhis",
        description="Bilingual responsible-AI evaluation for general VHIS questions / 一般自願醫保問題的中英雙語負責任 AI 評估",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    dry = commands.add_parser(
        "dry-run", help="Inspect routing/prompt without calling an API / 不呼叫 API，檢查路由及提示"
    )
    dry.add_argument("--case", required=True)
    dry.add_argument("--arm", choices=[item.value for item in ExperimentArm], required=True)

    run = commands.add_parser("run", help="Run the fixed experiment / 執行固定實驗")
    run.add_argument("--models", nargs="+", required=True)
    run.add_argument("--limit", type=int)
    run.add_argument("--output", type=Path)

    grade = commands.add_parser(
        "grade-template", help="Create the human grading CSV / 建立人手評分 CSV"
    )
    grade.add_argument("--input", type=Path, required=True)
    grade.add_argument("--output", type=Path, default=Path("results/grading.csv"))

    summary = commands.add_parser(
        "summarize", help="Summarize a completed grading CSV / 匯總已完成的評分 CSV"
    )
    summary.add_argument("--grades", type=Path, required=True)
    summary.add_argument("--output", type=Path, default=Path("results/summary.json"))
    return parser


def _dry_run(case_id: str, arm_value: str) -> None:
    case = next((item for item in load_cases() if item.id == case_id), None)
    if case is None:
        raise SystemExit(f"Unknown case / 未知個案: {case_id}")
    arm = ExperimentArm(arm_value)
    sources = [] if arm == ExperimentArm.BASELINE else retrieve(
        f"{case.question_zh_hk} {case.question_en}", load_sources()
    )
    routed = route_question(f"{case.question_zh_hk} {case.question_en}")
    payload: dict[str, object] = {
        "case_id": case.id,
        "arm": arm.value,
        "expected_action": case.expected_action.value,
        "retrieved_source_ids": [item.id for item in sources],
    }
    if arm == ExperimentArm.GUARDED and routed is not None:
        payload["deterministic_output"] = deterministic_response(routed).model_dump()
    else:
        payload["messages"] = build_messages(
            case.question_zh_hk, case.question_en, arm, sources
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    args = _parser().parse_args()
    if args.command == "dry-run":
        _dry_run(args.case, args.arm)
    elif args.command == "run":
        path = run_experiment(args.models, args.limit, args.output)
        print(path)
    elif args.command == "grade-template":
        make_grade_template(args.input, args.output)
        print(args.output)
    elif args.command == "summarize":
        summary = summarize_grades(args.grades)
        write_summary(args.output, summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
