from __future__ import annotations

import json
import re
from pathlib import Path

from .schemas import SourceChunk, TestCase


ROOT = Path(__file__).resolve().parents[2]


def load_sources(path: Path | None = None) -> list[SourceChunk]:
    source_path = path or ROOT / "data" / "sources.json"
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    return [SourceChunk.model_validate(item) for item in payload["chunks"]]


def load_cases(path: Path | None = None) -> list[TestCase]:
    case_path = path or ROOT / "data" / "test_cases.json"
    payload = json.loads(case_path.read_text(encoding="utf-8"))
    return [TestCase.model_validate(item) for item in payload["cases"]]


def _terms(text: str) -> set[str]:
    lowered = text.lower()
    latin = set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", lowered))
    compact = re.sub(r"\s+", "", lowered)
    chinese_bigrams = {
        compact[index : index + 2]
        for index in range(max(0, len(compact) - 1))
        if any("\u4e00" <= char <= "\u9fff" for char in compact[index : index + 2])
    }
    return latin | chinese_bigrams


def retrieve(question: str, sources: list[SourceChunk], limit: int = 3) -> list[SourceChunk]:
    question_terms = _terms(question)
    ranked: list[tuple[int, SourceChunk]] = []
    for source in sources:
        keyword_text = " ".join(source.keywords)
        body = f"{source.text_zh_hk} {source.text_en} {keyword_text}"
        score = len(question_terms & _terms(body))
        if score:
            ranked.append((score, source))
    ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
    return [source for _, source in ranked[:limit]]

