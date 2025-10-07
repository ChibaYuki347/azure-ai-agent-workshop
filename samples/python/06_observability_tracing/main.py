from __future__ import annotations

import logging
import os
import sys
from typing import Callable, Optional

from azure.ai.agents.models import CodeInterpreterTool, MessageRole
from azure.ai.agents.telemetry import AIAgentsInstrumentor
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError
from azure.core.settings import settings
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan
from azure.identity import DefaultAzureCredential

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

try:  # pragma: no cover - optional dependency
    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
except ImportError:  # pragma: no cover - optional dependency
    AzureMonitorTraceExporter = None  # type: ignore[assignment]

from ..common import configure_logging, load_config, pretty_print_messages

_logger = logging.getLogger("observability_tracing")


def _configure_tracing(
    app_insights_connection_string: Optional[str],
    enable_content_recording: bool,
) -> Callable[[], None]:
    """Configure OpenTelemetry exporters and instrument the Azure AI Agents SDK.

    Returns a callable that should be invoked to gracefully shut down tracing.
    """

    resource = Resource.create(
        {
            "service.name": "workshop-agent-tracing",
            "service.namespace": "azure-ai-agents",
            "service.instance.id": os.getenv("HOSTNAME", "local"),
        }
    )

    tracer_provider = TracerProvider(resource=resource)

    span_processor = None
    if app_insights_connection_string and AzureMonitorTraceExporter is not None:
        try:
            exporter = AzureMonitorTraceExporter.from_connection_string(
                app_insights_connection_string
            )
            span_processor = BatchSpanProcessor(exporter)
            _logger.info("Application Insights exporter configured for tracing output")
        except Exception as exc:  # pragma: no cover - defensive
            _logger.warning(
                "Failed to configure Azure Monitor exporter (%s). Falling back to console exporter.",
                exc,
            )
            span_processor = None
    elif app_insights_connection_string and AzureMonitorTraceExporter is None:
        _logger.warning(
            "Azure Monitor exporter package is missing; traces will be emitted to the console instead."
        )

    if span_processor is None:
        console_exporter = ConsoleSpanExporter()
        span_processor = SimpleSpanProcessor(console_exporter)
        _logger.info("Console span exporter enabled (stdout)")

    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Wire Azure Core to use OpenTelemetry spans and enable agent instrumentation.
    settings.tracing_implementation = OpenTelemetrySpan
    instrumentor = AIAgentsInstrumentor()
    instrumentor.instrument(enable_content_recording=enable_content_recording)

    def shutdown() -> None:
        instrumentor.uninstrument()
        tracer_provider.shutdown()

    return shutdown


def _should_record_content() -> bool:
    flag = os.getenv("ENABLE_AGENT_TRACE_CONTENT", "false").lower()
    return flag in {"1", "true", "yes", "on"}


def main() -> int:
    configure_logging()

    try:
        config = load_config()
    except EnvironmentError as exc:  # pragma: no cover - defensive branch
        _logger.error("Failed to load configuration: %s", exc)
        return 1

    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    try:
        shutdown_tracing = _configure_tracing(
            app_insights_connection_string=connection_string,
            enable_content_recording=_should_record_content(),
        )
    except ModuleNotFoundError as exc:
        _logger.error(
            "Tracing dependencies are missing. Install the tracing extras via 'pip install -r requirements.txt'. (%s)",
            exc,
        )
        return 1

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    tracer = trace.get_tracer("samples.python.observability_tracing")

    exit_code = 0
    try:
        with tracer.start_as_current_span("observability-sample") as sample_span:
            sample_span.set_attribute("workshop.module", "Day2-Observability")
            try:
                with AIProjectClient(endpoint=config.project_endpoint, credential=credential) as project_client:
                    agent = None
                    try:
                        _logger.info("Creating an agent instrumented for tracing")
                        agent = project_client.agents.create_agent(
                            model=config.model_deployment_name,
                            name="workshop-observability-agent",
                            instructions=(
                                "You are a helpful operations assistant. Explain the steps you take "
                                "to answer each request."
                            ),
                            tools=CodeInterpreterTool().definitions,
                        )

                        with tracer.start_as_current_span("thread-setup"):
                            thread = project_client.agents.threads.create()
                            project_client.agents.messages.create(
                                thread_id=thread.id,
                                role=MessageRole.USER,
                                content="Graph the function y = 2x^2 - 5x + 3 and summarise the vertex.",
                            )

                        with tracer.start_as_current_span("agent-run"):
                            run = project_client.agents.runs.create_and_process(
                                thread_id=thread.id,
                                agent_id=agent.id,
                                additional_instructions="Address the audience as Observability Team.",
                            )
                            if run.status != "succeeded":
                                _logger.error(
                                    "Agent run did not complete successfully (status=%s, error=%s)",
                                    run.status,
                                    run.last_error,
                                )
                                exit_code = 1

                        if exit_code == 0:
                            with tracer.start_as_current_span("read-messages"):
                                messages = project_client.agents.messages.list(thread_id=thread.id)
                                pretty_print_messages(messages)
                    finally:
                        if agent is not None:
                            _logger.info("Cleaning up created agent")
                            try:
                                project_client.agents.delete_agent(agent.id)
                            except Exception as exc:  # pragma: no cover - defensive cleanup
                                _logger.warning("Failed to delete agent cleanly: %s", exc)
            except HttpResponseError as exc:
                sample_span.record_exception(exc)
                _logger.exception("Azure AI Agent Service operation failed: %s", exc)
                exit_code = 1
    finally:
        shutdown_tracing()

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
