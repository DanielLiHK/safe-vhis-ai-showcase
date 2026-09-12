from __future__ import annotations

import os
import re
from dataclasses import dataclass


SUPPORTED_REGION = "ap-southeast-1"
ALLOWED_MODELS = {"qwen3.7-plus", "qwen3.8-flash"}


@dataclass(frozen=True)
class Settings:
    api_key: str
    workspace_id: str
    region: str = SUPPORTED_REGION

    @property
    def base_url(self) -> str:
        return (
            f"https://{self.workspace_id}.{self.region}.maas.aliyuncs.com/"
            "compatible-mode/v1"
        )

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
        workspace_id = os.getenv("DASHSCOPE_WORKSPACE_ID", "").strip()
        region = os.getenv("DASHSCOPE_REGION", SUPPORTED_REGION).strip()
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY is not set")
        if not workspace_id:
            raise ValueError(
                "DASHSCOPE_WORKSPACE_ID is not set; use the ID from Workspace Details, "
                "not only the workspace display name"
            )
        if region != SUPPORTED_REGION:
            raise ValueError(f"This study is locked to Singapore ({SUPPORTED_REGION})")
        if not re.fullmatch(r"[A-Za-z0-9-]+", workspace_id):
            raise ValueError("DASHSCOPE_WORKSPACE_ID contains unexpected characters")
        return cls(api_key=api_key, workspace_id=workspace_id, region=region)


def validate_models(models: list[str]) -> None:
    invalid = sorted(set(models) - ALLOWED_MODELS)
    if invalid:
        raise ValueError(f"Models outside the pre-registered allow-list: {invalid}")

