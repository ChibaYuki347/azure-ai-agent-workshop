# Document Samples

E-1. Internal Memo — “Why start with Agent Service?”

Length: ~140 words / Good for: #2 Bullet Summarizer, #8 Short Q&A, #5 Fact-vs-Guess
Text:
Our platform team plans to standardize on Azure AI Foundry Agent Service for production agents. The runtime bundles thread management, tool orchestration, identity, networking, and observability in one place. This consolidation reduces glue code and shortens the path from prototype to operations. The immediate wins we expect are: (1) safer defaults via content safety guardrails, (2) consistent tool calls to Logic Apps and custom functions, and (3) centralized monitoring through Application Insights. Risks include quota allocation and model choice drift across regions. To mitigate, we’ll document per-region model deployments and apply token rate limits at the API gateway. Success will be measured by task success rate, tool-call success rate, and mean latency. Teams keep the option to use Semantic Kernel for planning but must expose tools through the Agent’s catalog to keep telemetry consistent.

E-2. Meeting Notes — “RAG scope for Knowledge Agent”

Length: ~150 words / Good for: #2 Bullet Summarizer, #3 Procedure Writer, #4 RAG Answer
Text:
Participants aligned on a minimal RAG scope for the knowledge agent. Index sources: product FAQs, implementation runbooks, and policy pages with stable URLs. We’ll favor hybrid retrieval (keyword + vector) and add semantic ranking after we collect feedback. Citations in answers are mandatory; the agent must decline when no grounded sources are found. Batch evaluation will compare precision-like groundedness and coverage across prompt variants. For ingestion, we’ll automate indexing via a scheduled pipeline and small doc chunks (~800–1200 tokens). Known risks: duplicated pages between wiki and handbook; we’ll add canonical tags and filter by site path. Success criteria: 80%+ task adherence on a test set, <2 tool retries per conversation on average, and <2.5s median retrieval latency. Action items: finalize index schema, connect the AI Search tool, and ship a pilot to the helpdesk team.

E-3. Operations Report — “Logic Apps integration pilot”

Length: ~130 words / Good for: #2 Bullet Summarizer, #6 Tool-First Orchestrator
Text:
During week one, we connected the agent to Logic Apps to post Teams alerts and create tickets. The orchestration reduced manual steps, but two issues surfaced. First, malformed inputs from free-text prompts caused validation failures; we added a guarded function that normalizes parameters. Second, retries hid real connector outages; we now log one retry and then surface a human-readable error. A lightweight “run log” appended to each response improved transparency. Metrics: 92% tool-call success, 1.3 average retries before the change, 0.4 after. Next, we’ll add role-based restrictions so only ops-labeled threads can trigger ticket creation. If the pilot holds for two weeks, we’ll template the flow and publish it as a reusable tool for other agents.

E-4. Policy Brief — “Safety posture for chat workflows”

Length: ~150 words / Good for: #8 Short Q&A, #10 Safety Micro-Guard, #5 Fact-vs-Guess
Text:
We will enforce a layered safety posture for chat workflows. Inputs and outputs pass through content safety checks aligned with core categories (hate, violence, sexual, self-harm). For borderline cases, the agent responds with high-level guidance and avoids actionable details. We’ll log safety blocks and monitor block-rate spikes alongside quality metrics to detect prompt drift. Because grounding reduces but doesn’t eliminate hallucinations, answers must include transparent citations when the RAG tool is used; otherwise the agent should state when it cannot answer. Review cadence: weekly dashboards in Application Insights, plus a red-team test before each release. Limitations remain: safety filters can over-block creative content and under-catch oblique harms; we’ll keep thresholds adjustable and document escalation paths for human review.