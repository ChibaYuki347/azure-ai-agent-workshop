from __future__ import annotations

import logging
import sys
from typing import Optional

from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ..common import configure_logging, load_config

_logger = logging.getLogger("connected_agents")


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:
        _logger.error("Failed to load configuration (設定取得に失敗しました): %s", exc)
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
        main_agent_id: Optional[str] = None
        child_agent_id: Optional[str] = None
        try:
            _logger.info(
                "Creating sub-agent for stock prices (株価を回答するサブエージェントを作成します)"
            )
            stock_agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="stock_price_bot",
                instructions="When asked about stock prices, respond with the last known closing price and include the retrieval date.",
            )
            child_agent_id = stock_agent.id

            connected_tool = ConnectedAgentTool(
                id=stock_agent.id,
                name=stock_agent.name,
                description="Fetches the latest available stock price information for a given company ticker.",
            )

            main_agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="workshop-coordinator-agent",
                instructions="You orchestrate specialist agents. When a user asks about stock prices, delegate to the stock_price_bot.",
                tools=connected_tool.definitions,
            )
            main_agent_id = main_agent.id

            thread = project_client.agents.threads.create()
            project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content="MSFT の直近の株価を教えてください。出典も含めてください。",
            )

            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=main_agent.id)
            if run.status == "failed":
                _logger.error("Run failed (実行が失敗しました): %s", run.last_error)
                return 1

            response = project_client.agents.messages.list(thread_id=thread.id).get_last_message_by_role(MessageRole.AGENT)
            if response:
                for text_message in response.text_messages:
                    _logger.info("Response: %s (応答)", text_message.text.value)
            else:
                _logger.warning("No agent response retrieved (エージェントからの応答が取得できませんでした)")
            return 0
        except HttpResponseError as exc:
            _logger.exception(
                "Failed to run Connected Agents sample (Connected Agents サンプルの実行に失敗しました): %s",
                exc,
            )
            return 1
        finally:
            if main_agent_id:
                _logger.info("Deleting main agent (メイン エージェントを削除します)")
                project_client.agents.delete_agent(main_agent_id)
            if child_agent_id:
                _logger.info("Deleting sub agent (サブ エージェントを削除します)")
                project_client.agents.delete_agent(child_agent_id)


if __name__ == "__main__":
    sys.exit(main())
