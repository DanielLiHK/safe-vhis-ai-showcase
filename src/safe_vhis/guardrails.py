from __future__ import annotations

import re

from .schemas import Action, ModelAnswer


INJECTION_PATTERNS = [
    r"ignore (?:all|every|previous)",
    r"忽略(?:所有|以上|之前)",
    r"invent (?:a )?(?:source|citation)",
    r"作(?:一個)?來源",
    r"pretend (?:the )?government",
    r"扮政府",
]

PERSONALISED_PATTERNS = [
    r"\bmy\b", r"\bi have\b", r"\bshould i\b", r"\bwill my\b",
    r"exactly how much", r"definitely pay", r"my income",
    r"我(?:應唔應該|聽日|今年|呢張|嘅)", r"一定賠", r"扣幾多稅",
    r"買[\w\u4e00-\u9fff]+公司",
]

AMBIGUOUS_PATTERNS = [
    r"已有病包唔包", r"pre-existing conditions covered",
    r"全部都包", r"cover everything",
]


def route_question(question: str) -> Action | None:
    text = question.lower()
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in INJECTION_PATTERNS):
        return Action.REFER_TO_HUMAN
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in PERSONALISED_PATTERNS):
        return Action.REFER_TO_HUMAN
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in AMBIGUOUS_PATTERNS):
        return Action.ASK_CLARIFICATION
    return None


def deterministic_response(action: Action) -> ModelAnswer:
    if action == Action.ASK_CLARIFICATION:
        return ModelAnswer(
            action=action,
            answer_zh_hk="資料不足。請先說明你問的是一般標準計劃規則，還是某份具體保單、保障或情況。",
            answer_en=(
                "There is not enough information. Please clarify whether you mean the general "
                "Standard Plan rules or a specific policy, benefit, or situation."
            ),
            citations=[],
            rationale_code="AMBIGUOUS_SCOPE",
        )
    return ModelAnswer(
        action=Action.REFER_TO_HUMAN,
        answer_zh_hk=(
            "呢個問題涉及個人保障、索償、產品、稅務或試圖繞過安全限制，系統不會作決定。"
            "請查閱正式文件並向相關保險公司或合資格專業人士核實。"
        ),
        answer_en=(
            "This request involves a personal coverage, claim, product, tax decision, or an attempt "
            "to bypass safety controls. The system will not decide it. Check the formal documents "
            "and consult the relevant insurer or a qualified professional."
        ),
        citations=[],
        rationale_code="HUMAN_DECISION_REQUIRED",
    )


def citations_are_valid(citations: list[str], allowed_ids: set[str]) -> bool:
    return bool(citations) and set(citations).issubset(allowed_ids)

