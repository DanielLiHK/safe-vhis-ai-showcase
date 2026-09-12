import pytest

from safe_vhis.provider import parse_model_json
from safe_vhis.schemas import Action


def test_parse_fenced_json() -> None:
    answer = parse_model_json(
        """```json
        {"action":"ANSWER","answer_zh_hk":"是","answer_en":"Yes",
         "citations":["VHIS-P01-RENEWAL"],"rationale_code":"SUPPORTED"}
        ```"""
    )
    assert answer.action == Action.ANSWER


def test_duplicate_citations_rejected() -> None:
    with pytest.raises(ValueError):
        parse_model_json(
            '{"action":"ANSWER","answer_zh_hk":"是","answer_en":"Yes",'
            '"citations":["A","A"],"rationale_code":"BAD"}'
        )

