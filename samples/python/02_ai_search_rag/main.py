from __future__ import annotations

import logging
import sys
from typing import Optional

from azure.ai.agents.models import (
    AzureAISearchQueryType,
    AzureAISearchTool,
    MessageRole,
)
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ..common import configure_logging, load_config

_logger = logging.getLogger("ai_search_rag")


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:
        _logger.error("Failed to load configuration (設定の読み込みに失敗しました): %s", exc)
        return 1

    if not config.has_search:
        _logger.error(
            "AI_SEARCH_CONNECTION_ID and AI_SEARCH_INDEX_NAME must be set (AI_SEARCH_CONNECTION_ID と AI_SEARCH_INDEX_NAME を設定してください)."
        )
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
        agent_id: Optional[str] = None
        try:
            search_tool = AzureAISearchTool(
                index_connection_id=config.ai_search_connection_id,
                index_name=config.ai_search_index_name,
                query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID,
                top_k=5,
            )

            _logger.info("Creating agent for RAG scenario (RAG 用エージェントを作成します)")
            agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="workshop-rag-agent",
                instructions=(
                    "You answer questions using the Azure AI Search tool. Always cite the document title and URL in markdown."
                ),
                tools=search_tool.definitions,
                tool_resources=search_tool.resources,
            )
            agent_id = agent.id

            thread = project_client.agents.threads.create()
            project_client.agents.messages.create(
                thread_id=thread.id,
                role=MessageRole.USER,
                content=(
                    "Contoso 製品ラインの保守契約に関する最新の更新点を要約し、引用を明示してください。"
                ),
            )

            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            if run.status == "failed":
                _logger.error("Run failed (実行に失敗しました): %s", run.last_error)
                return 1

            response = project_client.agents.messages.list(thread_id=thread.id).get_last_message_by_role(
                MessageRole.AGENT
            )
            if response is None:
                _logger.warning("No response messages found (応答メッセージが見つかりませんでした)")
                return 0

            for text_message in response.text_messages:
                _logger.info("回答: %s", text_message.text.value)
            for citation in response.url_citation_annotations:
                _logger.info("引用: %s (%s)", citation.url_citation.title, citation.url_citation.url)

            return 0
        except HttpResponseError as exc:
            _logger.exception("Failed to run RAG scenario (RAG シナリオの実行に失敗しました): %s", exc)
            return 1
        finally:
            if agent_id:
                _logger.info("Cleaning up agent (エージェントをクリーンアップします)")
                project_client.agents.delete_agent(agent_id)


if __name__ == "__main__":
    sys.exit(main())
