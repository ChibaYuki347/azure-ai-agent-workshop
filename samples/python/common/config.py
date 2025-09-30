from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

_ENV_KEYS = {
    "project_endpoint": "PROJECT_ENDPOINT",
    "model_deployment_name": "MODEL_DEPLOYMENT_NAME",
    "openai_connection_id": "AZURE_OPENAI_CONNECTION_ID",
    "ai_search_connection_id": "AI_SEARCH_CONNECTION_ID",
    "ai_search_index_name": "AI_SEARCH_INDEX_NAME",
    "logic_app_callback_url": "LOGIC_APP_CALLBACK_URL",
    "subscription_id": "AZURE_SUBSCRIPTION_ID",
    "resource_group_name": "AZURE_RESOURCE_GROUP_NAME",
    "evaluation_project_endpoint": "AZURE_AI_PROJECT",
}


@dataclass(slots=True)
class WorkshopConfig:
    """Typed view over environment variables required by the samples."""

    project_endpoint: str
    model_deployment_name: str
    openai_connection_id: Optional[str] = None
    ai_search_connection_id: Optional[str] = None
    ai_search_index_name: Optional[str] = None
    logic_app_callback_url: Optional[str] = None
    subscription_id: Optional[str] = None
    resource_group_name: Optional[str] = None
    evaluation_project_endpoint: Optional[str] = None

    @property
    def has_search(self) -> bool:
        return bool(self.ai_search_connection_id and self.ai_search_index_name)

    @property
    def has_logic_app(self) -> bool:
        return bool(self.logic_app_callback_url)


def _get_env_or_fail(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(
            f"Environment variable '{name}' is not set. (環境変数 '{name}' が設定されていません。) Check the prerequisites in README.md."
        )
    return value


def load_config(optional: bool = True) -> WorkshopConfig:
    """Load configuration from environment variables.

    Parameters
    ----------
    optional:
        When True, optional settings are allowed to be missing. When False,
        all known environment variables must exist.
    """

    required = {
        "project_endpoint": _get_env_or_fail(_ENV_KEYS["project_endpoint"]),
        "model_deployment_name": _get_env_or_fail(_ENV_KEYS["model_deployment_name"]),
    }

    data: dict[str, Optional[str]] = {
        key: required.get(key)
        if key in required
        else os.getenv(env_key) if optional else _get_env_or_fail(env_key)
        for key, env_key in _ENV_KEYS.items()
    }

    return WorkshopConfig(**data)  # type: ignore[arg-type]
