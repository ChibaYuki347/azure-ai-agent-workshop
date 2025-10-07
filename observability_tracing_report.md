# Observability Tracing Sample Run Report (2025-10-07)

## Execution summary

- **Command** (`zsh`):

  ```bash
  APPLICATIONINSIGHTS_CONNECTION_STRING='***redacted***' \
  ENABLE_AGENT_TRACE_CONTENT=true \
  python -m samples.python.06_observability_tracing.main
  ```

- **Environment**: local macOS, Python 3.10 virtual environment (`.venv`)
- **Objective**: Validate OpenTelemetry instrumentation and Azure Monitor exporter flow from `samples/python/06_observability_tracing/main.py` with content tracing enabled.

## Outcome

- Exit code **1** because the agent run returned `RunStatus.FAILED` with `server_error: "Sorry, something went wrong."`
- Agent resources were cleaned up automatically after the failure.

## Console highlights

- Tracing pipeline initialised and authenticated:
  - `Application Insights exporter configured for tracing output`
  - `DefaultAzureCredential acquired a token from AzureCliCredential`
- Telemetry successfully sent to Application Insights multiple times (e.g. `Items received: 14 / Items accepted: 14`).
- Run failure logged at `12:20:20` with the exact status/error payload.

### Key identifiers

- **Thread ID**: `thread_avklT9py2T0fwePYn0GI7zGW`
- **Run ID**: `run_Py3LqbJQBQReVqf0zHHjOFto`
- **Traceparent example**: `00-f1a9fccca894f1236a42c175af9c295e-66b030459449673a-01`

## Application Insights follow-up

To inspect collected telemetry, run the following Kusto query in the Application Insights workspace associated with the provided connection string:

```kusto
traces
| where customDimensions["gen_ai.thread.run.id"] == "run_Py3LqbJQBQReVqf0zHHjOFto"
| project timestamp, message, customDimensions
| order by timestamp asc
```

If content tracing remains enabled, the events contain message payloads (`gen_ai.event.content`) and tool call metadata.

## Next steps

1. Re-run the sample after resolving the upstream `server_error` (service-side incident or quota issue) to capture a successful trace baseline.
2. Create a Workbook or Alert in Application Insights filtered by `gen_ai.system == "az.ai.agents"` to monitor future agent runs.
3. Optionally reduce log verbosity (`logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)`) once instrumentation is validated.

## Additional telemetry runs

| Iteration | Local start (JST) | Thread ID | Run ID | Outcome | Telemetry accepted (batch sizes) |
| --- | --- | --- | --- | --- | --- |
| 1 | 12:20 | `thread_avklT9py2T0fwePYn0GI7zGW` | `run_Py3LqbJQBQReVqf0zHHjOFto` | `FAILED` (`server_error`) | 14 |
| 2 | 12:25 | `thread_9VDUdO3JBvp74h4IO8UGRTk9` | `run_FQ8Wk8JyppdBDO3vzNieeenx` | `FAILED` (`server_error`) | 13, 7, 9, 12 |

- Both iterations transmitted telemetry successfully despite the upstream failure state, confirming that the OpenTelemetry pipeline remains healthy.
- The latest run used `ENABLE_AGENT_TRACE_CONTENT=true`, producing richer spans (message bodies, tool payloads) that appear under `customDimensions.gen_ai.event.content` in Application Insights.
- Each run automatically deleted the temporary agent, so no manual cleanup is required in the portal.
