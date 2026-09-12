import pytest

from safe_vhis.config import Settings, validate_models


def test_singapore_base_url() -> None:
    settings = Settings(api_key="placeholder", workspace_id="ws-123")
    assert settings.base_url == (
        "https://ws-123.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
    )


def test_model_allow_list() -> None:
    validate_models(["qwen3.8-flash", "qwen3.7-plus"])
    with pytest.raises(ValueError):
        validate_models(["unreviewed-model"])


def test_env_requires_workspace_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "placeholder")
    monkeypatch.delenv("DASHSCOPE_WORKSPACE_ID", raising=False)
    with pytest.raises(ValueError, match="Workspace Details"):
        Settings.from_env()

