from __future__ import annotations

import json
import re
from dataclasses import dataclass

from openai import OpenAI

from .config import Settings
from .schemas import ModelAnswer


@dataclass(frozen=True)
class CompletionResult:
    answer: ModelAnswer
    prompt_tokens: int | None
    completion_tokens: int | None


def parse_model_json(text: str) -> ModelAnswer:
    stripped = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, re.DOTALL | re.IGNORECASE)
    if fenced:
        stripped = fenced.group(1)
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        start, end = stripped.find("{"), stripped.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Model did not return a JSON object")
        payload = json.loads(stripped[start : end + 1])
    return ModelAnswer.model_validate(payload)


class QwenClient:
    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)

    def complete(self, model: str, messages: list[dict[str, str]]) -> CompletionResult:
        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=600,
        )
        content = response.choices[0].message.content or ""
        usage = response.usage
        return CompletionResult(
            answer=parse_model_json(content),
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
        )

