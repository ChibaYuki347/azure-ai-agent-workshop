# Workshop Structure: Azure AI Foundry Agent Service Introduction (2-Day Program)

---

## Day 1 (September 23) — "Build and Run Agents" 13:00–17:00

### Module A: Introduction (Concepts & Overview)

**S1. Opening & Goals**

* **Key Elements**: Three main goals (①Agentic AI fundamentals ②Minimal agent construction ③RAG+tool execution experience) / Overall agenda diagram
* **Notes**: Emphasize that "Azure AI Foundry Agent Service" (hereafter "Agent Service") covered in this workshop is an execution platform that integrates models, tools, observability, identity, and networking. ([Microsoft Learn][1])

**S2. What is Agentic AI (Differences from Copilot/Assistants)**

* **Key Elements**: Comparison table (Assistant ≈ conversation-centric vs Agent ≈ goal achievement + tool execution + state management)
* **Notes**: Agent Service provides **thread management**, **tool invocation**, **content safety**, and **identity/network/observability integration**. ([Microsoft Learn][1])

**S3. Azure Options and Positioning**

* **Key Elements**: Three-column diagram (Agent Service GA / Assistants API (Preview) / Framework: Semantic Kernel)
* **Notes**: Contrast how Assistants is in preview while Agent Service comes standard with operational requirements (observability, networking, etc.). ([Microsoft Learn][2])

---

### Module B: Agent Service Fundamentals

**S4. Agent Service Architecture Overview**

* **Key Elements**: Relationship diagram of Portal/REST/SDK, Models, Tools (Logic Apps etc.), RAG (AI Search), Observability, Entra ID, Private Link
* **Notes**: Single runtime integrating all these components. Clarify terminology (Agent/Thread/Message/Run/Tool). ([Microsoft Learn][1])

**S5. Managed "State"**

* **Key Elements**: Data persistence diagram (Threads / Messages / Runs / Files)
* **Notes**: Agent Service is a **stateful API**. Explicitly show that it persists entities like threads and files. ([Microsoft Learn][3])

**S6. Tool Types and Addition Methods**

* **Key Elements**: Built-in tools list (Bing Grounding, Azure AI Search, Logic Apps, third-party etc.) & tool addition UI screenshots (placeholder for replacement)
* **Notes**: Tool roles and addition procedure overview. ([Microsoft Learn][4])

**S7. Quick Start (Create→Conversation→Execution)**

* **Key Elements**: Portal procedures or REST/SDK minimal steps (diagrams + simple pseudo-code)
* **Notes**: Flow from minimal agent creation ~ thread creation ~ message addition ~ run execution. ([Microsoft Learn][5])

---

### Module C: Hands-on ① "Hello, Agent"

**S8. Demo Plan (Success Criteria & Rollback)**

* **Key Elements**: Success conditions (user question → agent response) / Fallback for failures (model/deployment name)
* **Notes**: OK with either Portal/SDK, recommend `DefaultAzureCredential` for authentication.

**S9. Minimal SDK Code (Python)**

* **Key Elements**: 10–15 line sample of **Agent creation→Thread→Message→Run**
* **Notes**: Code is for "concept understanding". Production requires exception handling, retry, and logging. ([Microsoft Learn][5])

**S10. Common Pitfalls (Model Names, Permissions, Regions)**

* **Key Elements**: Checklist (deployment name match / RBAC / quota verification)
* **Notes**: Mention that RBAC/Quota will be covered in depth later. ([Microsoft Learn][6])

**S11. Thread and Message Design Tips**

* **Key Elements**: Short-term/long-term threads, conversation scope and persistence diagrams
* **Notes**: Threads are "minimal units of conversation and state". Explain in relation to FAQ "storage targets". ([Microsoft Learn][3])

**S12. Practice Exercises**

* **Key Elements**: Prompt instruction techniques (style / evidence requirements / step-by-step)
* **Notes**: Set up for the Day 2 evaluation module where Azure AI Evaluation agent evaluators (Task Adherence / Tool Call Accuracy, etc.) will be used to score results. ([Microsoft Learn][16])

---

### Module D: RAG (Azure AI Search Tool) for Evidence-based Responses

**S13. Why RAG (Hallucination Prevention and Recency)**

* **Key Elements**: Comparison diagram of generation-only vs search + generation
* **Notes**: Agent Service can connect **Azure AI Search tool** to enhance responses. ([Microsoft Learn][7])

**S14. Connection Procedure (Connections→Add→AI Search)**

* **Key Elements**: Portal procedures (Connections tab → Azure AI Search) / CLI/SDK example fragments
* **Notes**: Connections are per-project. Index design will be covered in later tuning section. ([Microsoft Learn][7])

**S15. Search Mode Selection (Keyword/Semantic/Vector/Hybrid)**

* **Key Elements**: Application conditions table (e.g., FAQ = Semantic, technical docs = Hybrid)
* **Notes**: Also present **Agentic Retrieval** reference. ([Microsoft Learn][8])

**S16. Demo: Internal Document RAG**

* **Key Elements**: Query → hits → citation extraction (source URL/title) flow diagram
* **Notes**: Introduce prompt examples that include **citations** (source presentation) in output.

**S17. Tuning (Embeddings, Field Design, Caching)**

* **Key Elements**: Index design checklist
* **Notes**: Reference "Agent to Agent + Search" pattern setup guide and plan to validate improvements with Azure AI Evaluation RAG evaluators (Groundedness / Response Completeness / Retrieval). ([Microsoft Learn][8], [Microsoft Learn][15])

---

### Module E: Tool Execution (Actionization)

**S18. Logic Apps Integration (1,400+ Connectors)**

* **Key Elements**: **Business action** examples like ticket creation and approval flows
* **Notes**: Agents can call tools like **Logic Apps** (catalog selling point). ([Microsoft Azure][9])

**S19. OpenAPI/Functions Tool Design Points**

* **Key Elements**: I/O design based on function calling / input validation
* **Notes**: Tools should be "minimal and safe". Establish fallback procedures for failures. ([Microsoft Learn][4])

**S20. Demo: Operating External SaaS via Logic Apps**

* **Key Elements**: Flow diagram (Agent→Tool→SaaS) / audit log verification points
* **Notes**: "Who executed what" will be visualized in later observability module.

---

### Module F: Connected Agents (Multi-agent Introduction)

**S21. Pattern Introduction**

* **Key Elements**: Orchestrator + sub-agents (research / summarization / validation / generation) relationship diagram
* **Notes**: **Connected Agents** allows delegation from agent to agent. ([Microsoft Learn][10])

**S22. Role Separation and Prompt Design**

* **Key Elements**: Responsibility separation template (e.g., Critic/Planner/Executor)
* **Notes**: Clarify "which agent has which tools".

**S23. Mini Demo or Workshop**

* **Key Elements**: 3-minute demo of research → summarization → validation → report generation
* **Notes**: Connect to Day 2 evaluation, monitoring, and operations.

**S24. Day 1 Summary & Q&A**

* **Key Elements**: Today's deliverables / tomorrow's preview (evaluation, monitoring, security, rate control)
* **Notes**: Present homework until next time (RAG data preparation, etc.).

---

## Day 2 (September 30) — "Evaluate, Secure, and Operate Agents" 13:00–17:00

### Module G: Multi-agent Deep Dive

**S25. Representative Patterns (Sequential/Parallel/Critic-Loop)**

* **Key Elements**: Three pattern diagrams and failure examples (infinite loops / redundant tool calls)
* **Notes**: Planning can also use frameworks like Semantic Kernel in combination. ([Microsoft Learn][11])

**S26. Responsibility & SLO Design**

* **Key Elements**: Agent-specific KPIs (success rate, tool call success rate, latency)
* **Notes**: SLOs are measured and visualized with later Observability, and Azure AI Evaluation agent evaluators (Intent Resolution / Tool Call Accuracy / Task Adherence) provide supporting quality metrics. ([Microsoft Learn][12], [Microsoft Learn][16])

**S27. Hands-on: Connected Agents Configuration**

* **Key Elements**: Portal operation key points screen (Add Connected Agent)
* **Notes**: Write specific delegation target descriptions (boundary conditions, input/output contracts). ([Microsoft Learn][10])

---

### Module H: Evaluation (Azure AI Evaluation)

#### S28. Why Evaluation is Necessary (Updated)

* **Key Elements**: Metric categories for Quality (Relevance / Coherence / Fluency / Similarity), RAG-specific (Groundedness / Response Completeness / Retrieval), Safety (Violence / Sexual / Self-harm / Hate, etc.), and Agent-specific (Intent Resolution / Tool Call Accuracy / Task Adherence).
* **Notes**: Emphasize that Azure AI Evaluation offers these metrics out of the box and records results in the project for ongoing improvement. ([Microsoft Learn][13], [Microsoft Learn][15], [Microsoft Learn][16])

#### S29. How to Run Evaluations (UI / SDK / Cloud)

* **Key Elements**: UI wizard steps to choose dataset / target / metrics and compare runs, SDK (local) flow calling `azure-ai-evaluation` `evaluate()`, and cloud evaluations (preview) to share evaluation records with the team.
* **Notes**: Clarify when to use UI, SDK, or cloud evaluations (scale, automation, collaboration) and that Azure AI projects keep evaluation outputs centralized. ([Microsoft Learn][13], [Microsoft Learn][14], [Microsoft Learn][15])

#### S30. Demo: Evaluating a RAG Response (Updated)

* **Key Elements**: Dataset containing question, expected answer, and context; select Groundedness / Response Completeness / Retrieval; review pass/fail status and rationales.
* **Notes**: Show how evaluation insights inform improvement actions (prompt updates / tool settings / index tuning). ([Microsoft Learn][15])

#### S31. Manual Review and A/B Comparison Tips (Updated)

* **Key Elements**: Portal Evaluation page features like threshold settings, sample-level review, and run comparison UI for A/B testing.
* **Notes**: Combine automated scoring with manual inspection, using the comparison dashboard to support decisions. ([Microsoft Learn][13])

---

### Module I: Observability (Operational Visibility)

**S32. What to Observe (Ops/Quality/Safety)**

* **Key Elements**: KPI map (latency, request count, tokens, safety block rate)
* **Notes**: **Azure AI Foundry Observability** integrates with **Application Insights**. ([Microsoft Learn][12])

**S33. Setup Flow**

* **Key Elements**: Project → Enable Observability → App Insights connection flow diagram
* **Notes**: Monitoring is "prerequisite for continuous operations" and Azure AI Evaluation run data is captured in the project for comparison and drilldown. ([Microsoft Learn][12], [Microsoft Learn][13])

**S34. Dashboard Examples (Alerts/Diagnostics)**

* **Key Elements**: Anomaly detection (spikes/drops) and SLO deviation examples
* **Notes**: Recommend simultaneous quality & safety monitoring. ([TECHCOMMUNITY.MICROSOFT.COM][17])

**S35. Extensions (Third-party/OTel Integration Considerations)**

* **Key Elements**: OpenTelemetry references (optional)
* **Notes**: Reference that there are options beyond official ones. ([Dynatrace][18])

---

### Module J: Responsible AI (Content Safety)

**S36. Content Safety Basics**

* **Key Elements**: Four categories (Hate/Violence/Sexual/Self-harm) + threshold adjustment diagram
* **Notes**: Policies and thresholds require **verification according to use cases**. ([Microsoft Learn][19], [Microsoft Azure][20])

**S37. Application Points for Agents**

* **Key Elements**: Guardrail placement diagram for input, intermediate output, and final output
* **Notes**: Flow of detection → block/regeneration/red team evaluation.

**S38. Lab: Inappropriate Input Detection Testing**

* **Key Elements**: "Try it" test procedures (screenshot replacement)
* **Notes**: Explain safety log observation and deviation response. ([Microsoft Learn][19])

---

### Module K: Identity & Permissions (Admin)

**S39. RBAC and Role Design**

* **Key Elements**: Azure RBAC table for projects/hubs (built-in + custom roles)
* **Notes**: Separate with minimal privileges (Dev/Reviewer/Operator, etc.). ([Microsoft Learn][6])

**S40. Agent ID Concepts (Non-human ID Management)**

* **Key Elements**: Agent ID and Defender/Purview integration diagram (audit and governance perspective)
* **Notes**: Share "digital labor" governance strengthening trends. ([TECHCOMMUNITY.MICROSOFT.COM][21])

**S41. Authentication (Keyless/Entra ID)**

* **Key Elements**: Comparison table and recommendations for Managed Identity/tokens/keys
* **Notes**: Organize authentication options for Azure AI/Agent/On Your Data. ([Microsoft Learn][22])

---

### Module L: Network Isolation (Admin)

**S42. Overall Options**

* **Key Elements**: Diagram comparing Hub/Project **Managed Network** and **Private Link**, Agent Service **VNet usage (Note: SKU/method differences)**
* **Notes**: Hub side is basically **Managed VNet**. For latest trends in Agent Service VNet support (Network Injection/BYO VNet), read official/TechCommunity together. ([Microsoft Learn][23], [TECHCOMMUNITY.MICROSOFT.COM][24])

**S43. Agent VNet-ization (How-to Key Points)**

* **Key Elements**: High-level steps for VNet usage in Agent Service (subnet delegation, outbound control)
* **Notes**: Control agent ingress/egress with dedicated VNet. ([Microsoft Learn][25])

**S44. Azure OpenAI Network Protection**

* **Key Elements**: Reference architecture diagram for OpenAI resource Private Endpoint configuration
* **Notes**: Also make Agent → OpenAI path private. ([Microsoft Learn][26])

**S45. On Your Data Network/Access**

* **Key Elements**: Organization of data source authentication (MI/token etc.) and network reachability
* **Notes**: Design with both data access and authentication. ([Microsoft Learn][27])

---

### Module M: Quota, Rate Control, and Cost

**S46. Quota/Rate Basics (TPM/RPM/Capacity)**

* **Key Elements**: TPM/RPM relationship, model-specific trends, **unit capacity** concept
* **Notes**: Emphasize that RPM:TPM ratio differs by model. Always refer to latest **Azure OpenAI Quotas/Limits**. ([Microsoft Learn][28])

**S47. Deployment Allocation (TPM Assignment)**

* **Key Elements**: Portal TPM allocation screen (replacement)
* **Notes**: Design allocation per subscription × region × model. ([Microsoft Learn][29])

**S48. **Token Rate Limit** Application with APIM**

* **Key Elements**: `azure-openai-token-limit-policy` application example (key points excerpt)
* **Notes**: Can suppress "overuse" with **1 customer = 1 key** etc. ([Microsoft Learn][30])

**S49. APIM Other Throttling/Plan Controls**

* **Key Elements**: Combination patterns with `rate-limit-by-key` and **quota** (monthly etc.)
* **Notes**: Effective as organizational guardrails. ([Microsoft Learn][31])

**S50. Cost Optimization Checklist**

* **Key Elements**: Cache (past responses/summaries), RAG document granularity, response control (output length), model selection (mini series utilization)
* **Notes**: Based on continuous operations of evaluation → monitoring → adjustment.

---

### Module N: Closing

**S51. Production Deployment Checklist**

* **Key Elements**: Safety (Content Safety/red team) / Operations (Observability/SLO) / ID & Network / Rate / BCP
* **Notes**: Distribute in a form that can be transferred to company requirements. Re-present related official hubs. ([Microsoft Learn][32])

**S52. Next Steps & Reference Resources**

* **Key Elements**: Link collection for tutorials, samples, learning paths
* **Notes**: Operations to follow latest information through Learn/Docs/TechCommunity. ([Microsoft Learn][5], [TECHCOMMUNITY.MICROSOFT.COM][21])

---

## Day2 Demo Sample Code (Python / .NET)

The following end-to-end snippets map directly to Day2 modules (evaluation, observability, safety, operations). Apply the steps in order to recreate demos for S25–S50.

### 0) Prerequisites (Shared)

```bash
# Azure AI Foundry Project
export PROJECT_ENDPOINT="https://<xxx>.services.ai.azure.com/api/projects/<project-name>"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"

# Application Insights / Log Analytics
export APPLICATIONINSIGHTS_CONNECTION_STRING="<App Insights connection string>"
export LOGS_WORKSPACE_ID="<Log Analytics Workspace ID>"

# Azure AI Content Safety
export CONTENT_SAFETY_ENDPOINT="https://<your-contentsafety>.cognitiveservices.azure.com"
export CONTENT_SAFETY_KEY="<content-safety-key>"

# (Optional) APIM-backed rate control demo
export APIM_OPENAI_BASE="https://<your-apim>.azure-api.net"
export APIM_SUBSCRIPTION_KEY="<your-apim-subscription-key>"
export OPENAI_DEPLOYMENT="<your-aoai-deployment>"
export OPENAI_API_VERSION="2024-06-01"
```

> Review Agent/Thread/Run vocabulary and minimal creation flow in the overview and quickstart. ([Microsoft Learn][1], [Microsoft Learn][5])

### 1) [G] Connected Agents (Multi-agent orchestration)

#### Python

```python
# pip install azure-ai-projects azure-ai-agents azure-identity
import os
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

stock_agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="stock_price_bot",
    instructions=(
        "You get the stock price of a company. If real-time is not available, "
        "return the last known price."
    ),
)

connected = ConnectedAgentTool(
    id=stock_agent.id,
    name=stock_agent.name,
    description="Gets the stock price of a company",
)

main_agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="research_agent",
    instructions="Use available tools to answer questions.",
    tools=connected.definitions,
)

thread = project.agents.threads.create()
project.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="What is the stock price of Microsoft?",
)
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=main_agent.id,
)

for message in project.agents.messages.list(thread_id=thread.id).text_messages:
    print(message)
```

#### .NET (C#)

```csharp
// dotnet add package Azure.AI.Agents.Persistent --prerelease
// dotnet add package Azure.Identity
using Azure.AI.Agents.Persistent;
using Azure.Identity;

var endpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var model = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");

var client = new PersistentAgentsClient(endpoint, new DefaultAzureCredential());

var stockAgent = client.Administration.CreateAgent(
    model: model,
    name: "stock_price_bot",
    instructions: "Get stock prices. If real-time isn't available, return the last known price."
);

var connected = new ConnectedAgentToolDefinition(
    new ConnectedAgentDetails(
        stockAgent.Id,
        stockAgent.Name,
        "Gets the stock price of a company"
    )
);

var mainAgent = client.Administration.CreateAgent(
    model: model,
    name: "research_agent",
    instructions: "Use available tools to answer questions.",
    tools: [connected]
);

var thread = client.Threads.CreateThread();
client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the stock price of Microsoft?"
);
var run = client.Runs.CreateRun(thread, mainAgent);

while (run.Status is RunStatus.InProgress or RunStatus.Queued)
{
    Thread.Sleep(500);
    run = client.Runs.GetRun(thread.Id, run.Id);
}

foreach (var message in client.Messages.GetMessages(thread.Id, order: ListSortOrder.Ascending))
{
    foreach (var content in message.ContentItems)
    {
        if (content is MessageTextContent text)
        {
            Console.WriteLine($"{message.Role}: {text.Text}");
        }
    }
}
```

> Configure connected agents and delegation prompts per the official how-to. ([Microsoft Learn][10])

### 2) [H] Evaluation (quality, safety, agent metrics)

#### 2-A. Python: Continuous Evaluation (cloud)

```python
# pip install azure-ai-projects azure-identity azure-monitor-query
import os
from datetime import timedelta
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentEvaluationRequest, EvaluatorIds
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

evaluators = {
    "Relevance": {"Id": EvaluatorIds.Relevance.value},
    "Fluency": {"Id": EvaluatorIds.Fluency.value},
    "Coherence": {"Id": EvaluatorIds.Coherence.value},
    "ToolCallAccuracy": {"Id": EvaluatorIds.ToolCallAccuracy.value},
}

app_insights_cs = project.telemetry.get_application_insights_connection_string()

eval_run = project.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(
        thread=thread.id,
        run=run.id,
        evaluators=evaluators,
        app_insights_connection_string=app_insights_cs,
    )
)
print("Evaluation requested:", eval_run.name)

logs = LogsQueryClient(DefaultAzureCredential())
kql = f"""
traces
| where message == "gen_ai.evaluation.result"
| where customDimensions["gen_ai.thread.run.id"] == "{run.id}"
"""
response = logs.query_workspace(
    os.environ["LOGS_WORKSPACE_ID"],
    kql,
    timespan=timedelta(days=1),
)

if response.status == LogsQueryStatus.SUCCESS:
    for table in response.tables:
        for row in table.rows:
            print(dict(zip(table.columns, row)))
```

> Follow the continuous evaluation guide to wire Application Insights telemetry. ([Microsoft Learn][34])

#### 2-B. Python: Local Evaluation SDK (RAG metrics)

```python
# pip install azure-ai-evaluation
from azure.ai.evaluation import evaluate

result = evaluate(
    data="dataset.jsonl",
    evaluators={
        "Groundedness": "groundedness",
        "ResponseCompleteness": "response_completeness",
        "Retrieval": "retrieval",
    },
    evaluation_name="rag-eval-run",
)

print(result["metrics"])
```

> Built-in evaluators and usage details are documented in the Evaluation SDK guide. ([Microsoft Learn][36])

#### 2-C. .NET: Agent evaluation API

```csharp
// dotnet add package Azure.AI.Projects --prerelease
// dotnet add package Azure.Identity
using Azure.AI.Projects;
using Azure.Identity;

var projects = new AIProjectsClient(endpoint, new DefaultAzureCredential());

var evaluators = new Dictionary<string, EvaluatorConfiguration>
{
    { "Relevance", new EvaluatorConfiguration(EvaluatorIds.Relevance) },
    { "Fluency", new EvaluatorConfiguration(EvaluatorIds.Fluency) },
    { "ToolCallAccuracy", new EvaluatorConfiguration(EvaluatorIds.ToolCallAccuracy) },
};

var request = AzureAIProjectsModelFactory.AgentEvaluationRequest(
    runId: run.Id,
    threadId: thread.Id,
    evaluators: evaluators
);

var evaluation = projects.Evaluations.CreateAgentEvaluation(request);
Console.WriteLine($"Agent evaluation started: {evaluation.Value.Name}");
```

> Use the `Evaluations.CreateAgentEvaluation` method from the .NET SDK. ([Microsoft Learn][37])

### 3) [I] Observability (monitoring & tracing)

#### 3-A. Python: Send OpenTelemetry to App Insights

```python
# pip install azure-monitor-opentelemetry opentelemetry-sdk
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

# Subsequent AIProjectClient executions emit traces into App Insights
```

> Minimal OpenTelemetry setup is covered in the Azure Monitor configuration article. ([Microsoft Learn][38])

#### 3-B. .NET: Query App Insights via KQL

```csharp
// dotnet add package Azure.Monitor.Query
// dotnet add package Azure.Identity
using Azure.Identity;
using Azure.Monitor.Query;

var logsClient = new LogsQueryClient(new DefaultAzureCredential());

var query = $@"
traces
| where message == "gen_ai.evaluation.result"
| where tostring(customDimensions["gen_ai.thread.run.id"]) == "{run.Id}"
";

var result = logsClient.QueryWorkspace(
    Environment.GetEnvironmentVariable("LOGS_WORKSPACE_ID"),
    query,
    TimeSpan.FromDays(1)
);

foreach (var table in result.Value.Tables)
{
    foreach (var row in table.Rows)
    {
        Console.WriteLine(string.Join(" | ", row));
    }
}
```

> See the Azure Monitor Query samples for more KQL examples. ([Microsoft Learn][39])

### 4) [J] Responsible AI (Content Safety guards)

#### Python: Input/output safety check

```python
# pip install azure-ai-contentsafety
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    AnalyzeTextOutputType,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint=os.environ["CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["CONTENT_SAFETY_KEY"]),
)

def is_safe_text(text: str) -> bool:
    options = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type=AnalyzeTextOutputType.FOUR_SEVERITY_LEVELS,
    )
    result = client.analyze_text(options)
    severities = [category.severity for category in result.categories_analysis]
    return max(severities, default=0) < 4

user_input = "..."
if not is_safe_text(user_input):
    raise ValueError("Input rejected by safety policy")

agent_output = "..."
if not is_safe_text(agent_output):
    agent_output = "The response was withheld due to safety policy."
```

> SDK usage and severity interpretation are detailed in the Content Safety README. ([Microsoft Learn][40])

#### .NET: Input/output safety check

```csharp
// dotnet add package Azure.AI.ContentSafety
// dotnet add package Azure.Identity
using Azure;
using Azure.AI.ContentSafety;

var csClient = new ContentSafetyClient(
    new Uri(Environment.GetEnvironmentVariable("CONTENT_SAFETY_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("CONTENT_SAFETY_KEY"))
);

bool IsSafe(string text)
{
    var options = new AnalyzeTextOptions(text)
    {
        OutputType = AnalyzeTextOutputType.FourSeverityLevels,
    };

    var response = csClient.AnalyzeText(options);
    var maxSeverity = response.Value.CategoriesAnalysis.Max(category => (int)category.Severity);
    return maxSeverity < 4;
}
```

> The .NET Content Safety SDK mirrors the same options; see the official reference. ([Microsoft Learn][41])

### 5) [M] Rate control & cost optimization (APIM + 429 retry)

Apply APIM's `azure-openai-token-limit-policy` and configure `tokens-per-minute` / `counter-key` thresholds to enforce tenant-level quotas. ([Microsoft Learn][30])

#### Python: Honor 429 `Retry-After`

```python
# pip install requests
import os
import time
import requests

def call_openai_via_apim(messages):
    url = (
        f"{os.environ['APIM_OPENAI_BASE']}/openai/deployments/"
        f"{os.environ['OPENAI_DEPLOYMENT']}/chat/completions"
        f"?api-version={os.environ['OPENAI_API_VERSION']}"
    )
    headers = {
        "Ocp-Apim-Subscription-Key": os.environ["APIM_SUBSCRIPTION_KEY"],
        "Content-Type": "application/json",
    }
    payload = {"messages": messages, "max_tokens": 256}

    for _ in range(5):
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 429:
            retry_after = (
                response.headers.get("Retry-After")
                or response.headers.get("Retry-After-Ms")
            )
            delay = (
                float(retry_after) / 1000.0
                if retry_after and retry_after.isdigit() and int(retry_after) > 1000
                else float(retry_after or 1)
            )
            time.sleep(min(delay, 10))
            continue
        response.raise_for_status()
        return response.json()

    raise RuntimeError("Retries exhausted")
```

#### .NET: Retry with Polly

```csharp
// dotnet add package Polly
// dotnet add package Azure.Identity
using Polly;
using System.Text;
using System.Text.Json;

double GetDelay(HttpResponseMessage response)
{
    if (response.Headers.TryGetValues("Retry-After", out var seconds) &&
        double.TryParse(seconds.FirstOrDefault(), out var sec))
    {
        return sec;
    }

    if (response.Headers.TryGetValues("Retry-After-Ms", out var milliseconds) &&
        double.TryParse(milliseconds.FirstOrDefault(), out var ms))
    {
        return ms / 1000.0;
    }

    return 1.0;
}

var policy = Policy
    .HandleResult<HttpResponseMessage>(resp => (int)resp.StatusCode == 429)
    .WaitAndRetryAsync(5, (retry, context) =>
    {
        var lastResponse = (HttpResponseMessage)context["lastResponse"];
        return TimeSpan.FromSeconds(Math.Min(GetDelay(lastResponse), 10));
    }, (outcome, delay, retry, context) => Task.CompletedTask);

var httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Add(
    "Ocp-Apim-Subscription-Key",
    Environment.GetEnvironmentVariable("APIM_SUBSCRIPTION_KEY")
);

var requestUri = (
    $"{Environment.GetEnvironmentVariable("APIM_OPENAI_BASE")}/openai/deployments/"
    + $"{Environment.GetEnvironmentVariable("OPENAI_DEPLOYMENT")}/chat/completions"
    + $"?api-version={Environment.GetEnvironmentVariable("OPENAI_API_VERSION")}" 
);

var payload = JsonSerializer.Serialize(new
{
    messages = new[] { new { role = "user", content = "hello" } },
    max_tokens = 256,
});

var response = await policy.ExecuteAsync(async context =>
{
    var httpResponse = await httpClient.PostAsync(
        requestUri,
        new StringContent(payload, Encoding.UTF8, "application/json")
    );
    context["lastResponse"] = httpResponse;
    return httpResponse;
}, new Context());

response.EnsureSuccessStatusCode();
```

> Cross-check latest quota guidance when designing rate allocation. ([Microsoft Learn][28])

### 6) [K/L] Identity & network highlights

* Use `DefaultAzureCredential` as the base, layering Managed Identity / Entra ID best practices.
* Once Observability is enabled, wire the Foundry dashboard to App Insights. ([Microsoft Learn][12])
* Select Hub/Project Managed Network, Private Link, or Agent Service VNet options per requirement, and prefer Private Endpoints for OpenAI/data sources. ([Microsoft Learn][23])

### Bonus: Installation cheat sheet for Day2 samples

```bash
pip install azure-ai-projects azure-ai-agents azure-identity \
            azure-ai-evaluation azure-monitor-query \
            azure-ai-contentsafety azure-monitor-opentelemetry opentelemetry-sdk requests
```

```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Agents.Persistent --prerelease
dotnet add package Azure.Monitor.Query
dotnet add package Azure.AI.ContentSafety
dotnet add package Azure.Identity
dotnet add package Polly
```

---

## Appendix: "Diagrams, Tables, Code Fragments" Templates for Slide Materials

* **Architecture Diagrams (Day1 S4/S13/S18, Day2 S42–S45)**

  * *Layers*: User → Agent Service (Thread/Run/Tools) → (AI Search / Logic Apps / Functions) → Azure OpenAI → Observability (App Insights) → Entra ID/Network (Private Link/VNet).
  * Reference: Agent Service overview / Tool overview / Agentic Retrieval / Observability. ([Microsoft Learn][1])

* **Evaluation Flow Diagram (Day2 S28–S31)**

  * *Elements*: Test set → Prompt flow (app flow) → Evaluation flow (metrics) → Comparison dashboard.
  * Reference: Complete Prompt flow Evaluation flow set. ([Microsoft Learn][13])

* **Network Configuration Diagram (Day2 S42–S45)**

  * *Elements*: Hub Managed Network / Private Link, Agent VNet (Network Injection/BYO VNet as needed) and OpenAI/data source Private Endpoints.
  * Reference: Each document for Managed Network/Private Link/Agent VNet/On Your Data. ([Microsoft Learn][23])

* **Sample Code Fragments (Day1 S9 / Day1 S16)**

  * Minimal example of Agent creation ~ Run (Python) and prompt instruction example including **citations** in RAG responses.
  * Reference: Agent quickstart / AI Search tool how-to. ([Microsoft Learn][5])

* **Rate Control Snippets (Day2 S48–S49)**

  * Key attributes excerpt of APIM's `azure-openai-token-limit-policy` (`tokens-per-minute`/`counter-key`/`estimate-prompt-tokens`) display only.
  * Reference: Official APIM policy / GitHub samples. ([Microsoft Learn][30], [GitHub][33])

---

## Progress and Materials (Instructor Notes)

* **Pre-preparation**: Azure subscription (Agent Service/AI Search/App Insights), model deployment, small-scale index for RAG, APIM (optional).
* **Live Demo**:

  * *Day1*: Minimal Agent → RAG → Logic Apps tool invocation.
  * *Day2*: Connected Agents → Prompt flow evaluation → Observability → APIM token rate limiting.
* **Troubleshooting Alternative**: Demonstrate with Portal-centric procedures → switch to code presentation later.
* **Note**: Rates and features are updated regularly, so always refer to **latest Quotas/Limits** and **official How-to/FAQ** (add shortened URLs at slide end). ([Microsoft Learn][28])

---

### Reference Links (Used in Sections)

* Agent Service overview/FAQ/quickstart: ([Microsoft Learn][1])
* Tools (Azure AI Search/overall): ([Microsoft Learn][7])
* Connected Agents: ([Microsoft Learn][10])
* Agentic Retrieval (AI Search): ([Microsoft Learn][8])
* Prompt flow (evaluation/batch): ([Microsoft Learn][13])
* Observability (App Insights integration): ([Microsoft Learn][12])
* Content Safety (product/portal): ([Microsoft Azure][20], [Microsoft Learn][19])
* RBAC/ID: ([Microsoft Learn][6])
* Network (Managed Network/Private Link/Agent VNet/On Your Data): ([Microsoft Learn][23])
* Quotas/Limits & allocation: ([Microsoft Learn][28])
* APIM Token Limit & rate control: ([Microsoft Learn][30])

---

### Next Actions (If Desired)

* We can immediately generate **PPT templates (chapter structure, divider frames, diagram placeholders, footnotes)** based on this design.
* Code fragments can be inserted for either **Python/.NET** according to participants' technology stack (same structure presentation).

Should we proceed with creating materials? If you tell us about distribution format (Japanese/English combined, PPT/Google Slides) and availability of internal data for RAG demo materials, we can incorporate specific names and screenshot insertion positions into slides.

[1]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview "What is Azure AI Foundry Agent Service?"
[2]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/assistants "Azure OpenAI Assistants API (Preview)"
[3]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/faq "Azure AI Foundry Agent Service frequently asked questions"
[4]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview "What are tools in Azure AI Foundry Agent Service"
[5]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart "Quickstart - Create a new Azure AI Foundry Agent Service ..."
[6]: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry "Role-based access control for Azure AI Foundry"
[7]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search "How to use an existing AI Search index with the Azure AI ..."
[8]: https://learn.microsoft.com/en-us/azure/search/search-agentic-retrieval-how-to-pipeline "Build an agentic retrieval solution - Azure AI Search"
[9]: https://azure.microsoft.com/en-us/products/ai-foundry/agent-service/ "Azure AI Foundry Agent Service"
[10]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents "How to use connected agents - Azure AI Foundry"
[11]: https://learn.microsoft.com/en-us/semantic-kernel/concepts/planning "What are Planners in Semantic Kernel"
[12]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications "Monitor your Generative AI Applications - Azure AI Foundry"
[13]: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/prompt-flow "Prompt flow in Azure AI Foundry portal"
[14]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/flow-bulk-test-evaluation "Submit batch run and evaluate a flow - Azure AI Foundry"
[15]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/flow-develop-evaluation "Develop an evaluation flow in Azure AI Foundry portal"
[16]: https://azure.github.io/slm-innovator-lab/3_3_1_evaluation/ "Lab 3.3.1 Evaluate your models using Prompt Flow (UI)"
[17]: https://techcommunity.microsoft.com/blog/aiplatformblog/continuously-monitor-your-genai-application-with-azure-ai-foundry-and-azure-moni/4303450 "Continuously monitor your GenAI application with Azure AI ..."
[18]: https://www.dynatrace.com/hub/detail/azure-ai-foundry/ "Azure AI Foundry monitoring & observability | Dynatrace Hub"
[19]: https://learn.microsoft.com/en-us/azure/ai-foundry/ai-services/content-safety-overview "Content Safety in Azure AI Foundry portal overview"
[20]: https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety "Azure AI Content Safety"
[21]: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/securely-build-and-manage-agents-in-azure-ai-foundry/4415186 "Securely Build and Manage Agents in Azure AI Foundry"
[22]: https://learn.microsoft.com/en-us/azure/ai-services/authentication "Authenticate requests to Azure AI services"
[23]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/configure-managed-network "How to set up a managed network for Azure AI Foundry hubs"
[24]: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/built-in-enterprise-readiness-with-azure-ai-agent-service/4386541 "Built-in Enterprise Readiness with Azure AI Agent Service"
[25]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/virtual-networks "How to use a virtual network with the Azure AI Foundry ..."
[26]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/network "Securing Azure OpenAI inside a virtual network with private ..."
[27]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/on-your-data-configuration "Network and access configuration for Azure OpenAI On ..."
[28]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits "Azure OpenAI in Azure AI Foundry Models Quotas and Limits"
[29]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/quota "Manage Azure OpenAI in Azure AI Foundry Models quota"
[30]: https://learn.microsoft.com/en-us/azure/api-management/azure-openai-token-limit-policy "Limit Azure OpenAI API token usage"
[31]: https://learn.microsoft.com/en-us/azure/api-management/api-management-sample-flexible-throttling "Advanced Request Throttling with Azure API Management"
[32]: https://learn.microsoft.com/en-us/azure/ai-foundry/ "Azure AI Foundry documentation"
[33]: https://github.com/microsoft/AzureOpenAI-with-APIM "microsoft/AzureOpenAI-with-APIM"
[34]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents "Continuously Evaluate your AI agents"
[36]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk "Local evaluation with the Azure AI Evaluation SDK"
[37]: https://learn.microsoft.com/en-us/dotnet/api/azure.ai.projects.evaluations.createagentevaluation "Evaluations.CreateAgentEvaluation Method"
[38]: https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-configuration "Configure Azure Monitor OpenTelemetry"
[39]: https://learn.microsoft.com/en-us/samples/azure/azure-sdk-for-python/query-azuremonitor-samples/ "Azure Monitor Query client library Python samples"
[40]: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-contentsafety-readme "Azure AI Content Safety client library for Python"
[41]: https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.contentsafety-readme "Azure AI Content Safety client library for .NET"
