from __future__ import annotations

import logging
import sys
from typing import Optional

from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ..common import configure_logging, load_config, pretty_print_messages

_logger = logging.getLogger("minimal_agent")


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:  # pragma: no cover - defensive branch
        _logger.error("Failed to load configuration (設定を読み込めませんでした): %s", exc)
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
        agent = None
        try:
            _logger.info(
                "Creating agent (エージェントを作成します) [model=%s]", config.model_deployment_name
            )
            agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="workshop-minimal-agent",
                instructions="You are a polite assistant for quick math checks.",
                tools=CodeInterpreterTool().definitions,
            )
            thread = project_client.agents.threads.create()
            project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content="Please plot y = 4x + 9 and summarise the intercepts.",
            )

            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent.id,
                additional_instructions="Address the user as Workshop Participant.",
            )
            if run.status == "failed":
                _logger.error("Agent run failed (エージェントの実行が失敗しました): %s", run.last_error)
                return 1

            _logger.info("Fetching thread responses (スレッドの応答を取得します)")
            messages = project_client.agents.messages.list(thread_id=thread.id)
            pretty_print_messages(messages)
            return 0
        except HttpResponseError as exc:
            _logger.exception("Azure AI Agent Service call failed (Azure AI Agent Service 呼び出しに失敗しました): %s", exc)
            return 1
        finally:
            if agent is not None:
                _logger.info("Deleting created agent (作成したエージェントを削除します)")
                project_client.agents.delete_agent(agent.id)


if __name__ == "__main__":
    sys.exit(main())
