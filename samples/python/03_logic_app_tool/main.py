from __future__ import annotations

import logging
import sys
from typing import Optional

import requests
from azure.ai.agents.models import MessageRole
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ..common import (
    LogicAppToolConfig,
    configure_logging,
    create_logic_app_function_tool,
    load_config,
)

_logger = logging.getLogger("logic_app_tool")


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:
        _logger.error("Failed to load configuration (設定を読み込めませんでした): %s", exc)
        return 1

    if not config.has_logic_app:
        _logger.error(
            "LOGIC_APP_CALLBACK_URL is required; set the Logic Apps trigger URL (LOGIC_APP_CALLBACK_URL が必要です。Logic Apps トリガーの URL を設定してください)"
        )
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
        agent_id: Optional[str] = None
        try:
            tool = create_logic_app_function_tool(
                LogicAppToolConfig(callback_url=config.logic_app_callback_url)
            )

            agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="workshop-logic-app-agent",
                instructions="You can send operational notifications by calling the send_email_via_logic_app tool.",
                tools=tool.definitions,
            )
            agent_id = agent.id

            thread = project_client.agents.threads.create()
            project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content="メールで本日の講義の開始時間をリマインドしてください。",
            )

            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            if run.status == "failed":
                _logger.error("Logic App integration failed (Logic App 連携実行が失敗しました): %s", run.last_error)
                return 1

            messages = project_client.agents.messages.list(thread_id=thread.id)
            for message in messages:
                if message.role == MessageRole.AGENT:
                    for text_message in message.text_messages:
                        _logger.info("Response: %s (応答)", text_message.text.value)
            return 0
        except (HttpResponseError, requests.RequestException) as exc:
            _logger.exception("Logic App tool execution failed (Logic App ツールの実行でエラーが発生しました): %s", exc)
            return 1
        finally:
            if agent_id:
                _logger.info("Deleting agent (エージェントを削除します)")
                project_client.agents.delete_agent(agent_id)


if __name__ == "__main__":
    sys.exit(main())
