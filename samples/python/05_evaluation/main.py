from __future__ import annotations

import json
import logging
import os
import sys
from typing import Optional

from azure.ai.evaluation import (
    AIAgentConverter,
    ContentSafetyEvaluator,
    IntentResolutionEvaluator,
)
from azure.ai.evaluation._model_configurations import AzureOpenAIModelConfiguration
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from ..common import configure_logging, load_config

_logger = logging.getLogger("evaluation_sample")


def _load_judge_model_config() -> AzureOpenAIModelConfiguration:
    try:
        return AzureOpenAIModelConfiguration(
            azure_endpoint=os.environ["EVAL_AOAI_ENDPOINT"],
            api_key=os.environ["EVAL_AOAI_API_KEY"],
            api_version=os.environ.get("EVAL_AOAI_API_VERSION", "2024-05-01-preview"),
            azure_deployment=os.environ["EVAL_AOAI_DEPLOYMENT"],
        )
    except KeyError as exc:  # pragma: no cover - input validation
        raise EnvironmentError(
            "Azure OpenAI evaluation settings are missing (評価用の Azure OpenAI 設定が不足しています). Check the EVAL_AOAI_* environment variables (EVAL_AOAI_* の環境変数を確認してください)."
        ) from exc


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:
        _logger.error("Failed to load configuration (設定の読み込みに失敗しました): %s", exc)
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
        agent_id: Optional[str] = None
        try:
            _logger.info("Creating agent for evaluation (評価対象のエージェントを作成します)")
            agent = project_client.agents.create_agent(
                model=config.model_deployment_name,
                name="workshop-eval-agent",
                instructions=(
                    "Answer travel questions for Contoso employees. If information is missing, clearly state the limitation."
                ),
            )
            agent_id = agent.id

            thread = project_client.agents.threads.create()
            project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content="ロンドン出張に必要な社内承認フローを教えて。",
            )

            run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
            if run.status == "failed":
                _logger.error("Agent run failed (エージェント実行が失敗しました): %s", run.last_error)
                return 1

            converter = AIAgentConverter(project_client)
            converted = converter.convert(thread.id, run.id)

            judge_config = _load_judge_model_config()
            quality_eval = IntentResolutionEvaluator(model_config=judge_config)
            content_safety_eval = ContentSafetyEvaluator(
                azure_ai_project=config.evaluation_project_endpoint or config.project_endpoint,
                credential=credential,
            )

            _logger.info("Running Intent Resolution (Intent Resolution を実行します)")
            intent_result = quality_eval(**converted)
            _logger.info("結果: %s", json.dumps(intent_result, ensure_ascii=False, indent=2))

            _logger.info("Running Content Safety evaluation (Content Safety を実行します)")
            safety_result = content_safety_eval(**converted)
            _logger.info("結果: %s", json.dumps(safety_result, ensure_ascii=False, indent=2))

            return 0
        except (HttpResponseError, EnvironmentError) as exc:
            _logger.exception("Failed to run evaluation sample (評価サンプルの実行に失敗しました): %s", exc)
            return 1
        finally:
            if agent_id:
                _logger.info("Deleting evaluation agent (評価用エージェントを削除します)")
                project_client.agents.delete_agent(agent_id)


if __name__ == "__main__":
    sys.exit(main())
