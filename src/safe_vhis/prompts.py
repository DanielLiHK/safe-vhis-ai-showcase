from __future__ import annotations

import json

from .schemas import ExperimentArm, SourceChunk


OUTPUT_SCHEMA = {
    "action": "ANSWER | ASK_CLARIFICATION | REFER_TO_HUMAN",
    "answer_zh_hk": "Traditional Chinese answer",
    "answer_en": "English answer",
    "citations": ["source ID"],
    "rationale_code": "short machine-readable code",
}


CORE_BOUNDARY = """You are part of a controlled insurance research experiment.
You may explain only general information. Never decide personal coverage, claim payment,
product suitability, tax outcome, pricing, or underwriting. Never invent a source ID.
Return JSON only, matching this shape:
{schema}
Both language fields are required. Keep each answer concise.
"""


def build_messages(
    question_zh_hk: str,
    question_en: str,
    arm: ExperimentArm,
    sources: list[SourceChunk],
) -> list[dict[str, str]]:
    system = CORE_BOUNDARY.format(schema=json.dumps(OUTPUT_SCHEMA, ensure_ascii=False))
    if arm == ExperimentArm.BASELINE:
        system += "\nThis is the baseline arm. Do not cite sources; return an empty citations list."
    else:
        evidence = [
            {
                "id": item.id,
                "pdf_page": item.pdf_page,
                "text_zh_hk": item.text_zh_hk,
                "text_en": item.text_en,
            }
            for item in sources
        ]
        system += (
            "\nUse only the EVIDENCE below for factual VHIS claims. "
            "If it is insufficient, do not guess. Cite only supplied IDs.\nEVIDENCE:\n"
            + json.dumps(evidence, ensure_ascii=False, indent=2)
        )
    user = f"問題 / Question:\nZH-HK: {question_zh_hk}\nEN: {question_en}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

