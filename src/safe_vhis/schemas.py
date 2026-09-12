from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Action(str, Enum):
    ANSWER = "ANSWER"
    ASK_CLARIFICATION = "ASK_CLARIFICATION"
    REFER_TO_HUMAN = "REFER_TO_HUMAN"


class ExperimentArm(str, Enum):
    BASELINE = "baseline"
    GROUNDED = "grounded"
    GUARDED = "guarded"


class SourceChunk(BaseModel):
    id: str
    pdf_page: int = Field(ge=1)
    section: str
    text_zh_hk: str
    text_en: str
    keywords: list[str]


class TestCase(BaseModel):
    id: str
    category: str
    question_zh_hk: str
    question_en: str
    expected_action: Action
    gold_source_ids: list[str]
    gold_points: list[str]


class ModelAnswer(BaseModel):
    action: Action
    answer_zh_hk: str = ""
    answer_en: str = ""
    citations: list[str] = Field(default_factory=list)
    rationale_code: str = ""

    @field_validator("citations")
    @classmethod
    def citations_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("citations must be unique")
        return value


class RunRecord(BaseModel):
    run_id: str
    timestamp_utc: str
    model: str
    arm: ExperimentArm
    case_id: str
    expected_action: Action
    retrieved_source_ids: list[str]
    output: ModelAnswer
    citation_ids_valid: bool
    latency_ms: int
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    error: str | None = None

