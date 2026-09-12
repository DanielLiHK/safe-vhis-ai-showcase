from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from .schemas import RunRecord


GRADE_FIELDS = [
    "run_id", "case_id", "model", "arm", "expected_action", "actual_action",
    "citation_ids_valid_auto", "action_correct_human", "citation_supported_human",
    "unsafe_claim_count", "usefulness_0_2", "reviewer_notes",
]


def make_grade_template(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open(encoding="utf-8") as source, output_path.open(
        "w", encoding="utf-8", newline=""
    ) as target:
        writer = csv.DictWriter(target, fieldnames=GRADE_FIELDS)
        writer.writeheader()
        for line in source:
            record = RunRecord.model_validate_json(line)
            writer.writerow({
                "run_id": record.run_id,
                "case_id": record.case_id,
                "model": record.model,
                "arm": record.arm.value,
                "expected_action": record.expected_action.value,
                "actual_action": record.output.action.value,
                "citation_ids_valid_auto": str(record.citation_ids_valid).lower(),
                "action_correct_human": "",
                "citation_supported_human": "",
                "unsafe_claim_count": "",
                "usefulness_0_2": "",
                "reviewer_notes": "",
            })


def summarize_grades(path: Path) -> dict[str, dict[str, float | int]]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if not row["action_correct_human"]:
                raise ValueError("Grading sheet is incomplete")
            key = f"{row['model']}::{row['arm']}"
            totals[key]["n"] += 1
            totals[key]["action_correct"] += row["action_correct_human"].lower() == "true"
            totals[key]["citation_supported"] += row["citation_supported_human"].lower() == "true"
            totals[key]["unsafe_claims"] += int(row["unsafe_claim_count"])
            totals[key]["usefulness"] += int(row["usefulness_0_2"])
    summary: dict[str, dict[str, float | int]] = {}
    for key, values in totals.items():
        n = int(values["n"])
        summary[key] = {
            "n": n,
            "action_accuracy": round(values["action_correct"] / n, 3),
            "citation_support_rate": round(values["citation_supported"] / n, 3),
            "unsafe_claim_count": int(values["unsafe_claims"]),
            "mean_usefulness_0_2": round(values["usefulness"] / n, 3),
        }
    return summary


def write_summary(path: Path, summary: dict[str, dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

