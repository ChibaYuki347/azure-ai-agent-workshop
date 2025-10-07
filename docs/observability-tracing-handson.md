# Observability Tracing Hands-on Guide

This worksheet walks participants through running `samples/python/06_observability_tracing/main.py` locally, emitting OpenTelemetry traces to Azure Monitor, and validating the collected telemetry. Follow these steps during the workshop to reproduce the end-to-end flow on your own machine.

## 1. Prerequisites

Make sure you have the following before you begin:

- An **Azure subscription** with an Azure AI Foundry project.
- A deployed **model** (for example, `gpt-4o-mini`) that appears under **Models + Endpoints** in the project.
- **Application Insights** resource (or a workspace connection string) where you can push traces.
- **Azure CLI** installed and authenticated (`az login`).
- **Python 3.10 or later** available on your machine.
- Access to this repository (clone or download).

> 💡 **Authentication**: The sample relies on `DefaultAzureCredential`. On a developer machine the most common path is Azure CLI (`az login`). If you are using a different identity, make sure it is authorized for the Azure AI Foundry project.

## 2. Repository setup

1. Open a terminal and change into the Python samples directory:

    ```bash
    cd samples/python
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # PowerShell: .venv\Scripts\Activate.ps1
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## 3. Configure environment variables

The sample loads required settings from the environment. Prepare a `.env` file or export the variables in your shell.

| Variable | Required | Description |
| --- | --- | --- |
| `PROJECT_ENDPOINT` | ✅ | Project endpoint, e.g. `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| `MODEL_DEPLOYMENT_NAME` | ✅ | Model deployment name to run the agent (for example, `gpt-4o-mini`) |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Optional but recommended | Application Insights connection string used by the exporter |
| `ENABLE_AGENT_TRACE_CONTENT` | Optional | Set to `true` to capture message payloads inside trace spans |

> 🔐 **Tip**: Keep connection strings outside the repo. Export them in the shell or load them via `direnv`, `dotenv`, or your preferred secrets manager.

## 4. Run the tracing sample

From the root of the repository (or while the virtual environment is active), execute:

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING="<your-connection-string>" \
ENABLE_AGENT_TRACE_CONTENT=true \
python -m samples.python.06_observability_tracing.main
```

Expected console highlights:

- `Application Insights exporter configured for tracing output`
- `DefaultAzureCredential acquired a token ...`
- `Agent run did not complete successfully (status=RunStatus.FAILED, error={'code': 'server_error', ...})`
- `Cleaning up created agent`

The run may exit with code `1` if the upstream service returns a `server_error`. This is acceptable for observability exercises because the trace pipeline continues to emit telemetry.

## 5. Example run identifiers and telemetry counts

Two recent workshop runs produced the following metadata (Japan Standard Time):

| Iteration | Local start | Thread ID | Run ID | Outcome | Items accepted |
| --- | --- | --- | --- | --- | --- |
| 1 | 12:20 | `thread_avklT9py2T0fwePYn0GI7zGW` | `run_Py3LqbJQBQReVqf0zHHjOFto` | `FAILED` (`server_error`) | 14 |
| 2 | 12:25 | `thread_9VDUdO3JBvp74h4IO8UGRTk9` | `run_FQ8Wk8JyppdBDO3vzNieeenx` | `FAILED` (`server_error`) | 13, 7, 9, 12 |

Use your own run identifiers from the console when reviewing telemetry—values will differ on each execution.

## 6. Validate traces in Application Insights

1. Navigate to the Application Insights resource that matches your connection string.
2. Open **Logs (Analytics)** and run a Kusto query filtering by your run ID:

    ```kusto
    traces
    | where customDimensions["gen_ai.thread.run.id"] == "run_FQ8Wk8JyppdBDO3vzNieeenx"
    | order by timestamp asc
    | project timestamp, message, severityLevel, customDimensions
    ```

3. To see all Azure AI Agent spans emitted by the sample, query by service metadata:

    ```kusto
    traces
    | where customDimensions["gen_ai.system"] == "az.ai.agents"
    | where customDimensions["service.name"] == "workshop-agent-tracing"
    | summarize count() by bin(timestamp, 5m), customDimensions["gen_ai.event"]
    ```

4. When `ENABLE_AGENT_TRACE_CONTENT=true`, additional payloads show up under `customDimensions.gen_ai.event.content`.

## 7. Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `ModuleNotFoundError: No module named 'azure.monitor'` | Ensure `pip install -r requirements.txt` succeeded. The exporter package is included in the requirements file. |
| `Failed to load configuration: ... PROJECT_ENDPOINT` | Double-check environment variables and that `samples/python/common/config.py` can read them. |
| `Agent run did not complete successfully (server_error)` | Retry later or confirm the Azure AI Foundry project quota/state. Telemetry still flows and can be inspected. |
| Telemetry not visible in Application Insights | Confirm the connection string matches the target resource, and that your query filters on the correct run/thread identifiers. |

## 8. Cleanup

- Each execution deletes the temporary agent automatically; no manual cleanup is needed in the Azure portal.
- Deactivate the virtual environment when you finish: `deactivate`.
- Remove any temporary `.env` files that contain secrets.

## 9. References

- [Azure AI Foundry Agents Quickstart (Python)](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure)
- [Azure Monitor OpenTelemetry Exporter for Python](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-configuration)
- [OpenTelemetry Python documentation](https://opentelemetry.io/docs/languages/python/)
- Internal report: [`observability_tracing_report.md`](../observability_tracing_report.md)
