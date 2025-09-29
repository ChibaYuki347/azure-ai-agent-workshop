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
* **Notes**: Setup for later evaluation module to measure "task adherence".

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
* **Notes**: Reference "Agent to Agent + Search" pattern setup guide. ([Microsoft Learn][8])

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
* **Notes**: SLOs are measured and visualized with later Observability. ([Microsoft Learn][12])

**S27. Hands-on: Connected Agents Configuration**

* **Key Elements**: Portal operation key points screen (Add Connected Agent)
* **Notes**: Write specific delegation target descriptions (boundary conditions, input/output contracts). ([Microsoft Learn][10])

---

### Module H: Evaluation (Prompt flow)

**S28. Why Evaluation is Necessary**

* **Key Elements**: Metric list like **Task Adherence / Groundedness / Tool Accuracy**
* **Notes**: Overall picture of Prompt flow **Evaluation flow** types and metrics. ([Microsoft Learn][13])

**S29. How to Create Evaluation Flows**

* **Key Elements**: Test set → batch evaluation → metrics comparison diagram
* **Notes**: Batch evaluation and history comparison UI explanation. ([Microsoft Learn][14])

**S30. Demo: RAG Response Evaluation**

* **Key Elements**: Evaluation results dashboard (metrics equivalent to Precision/Recall)
* **Notes**: Improvement loop (prompt updates / tool setting reviews / index tuning). ([Microsoft Learn][15])

**S31. Manual Evaluation and A/B Comparison Tips**

* **Key Elements**: Manual evaluation UI screenshots / A/B design checks
* **Notes**: Practical use combines automatic + manual evaluation. ([Azure][16])

---

### Module I: Observability (Operational Visibility)

**S32. What to Observe (Ops/Quality/Safety)**

* **Key Elements**: KPI map (latency, request count, tokens, safety block rate)
* **Notes**: **Azure AI Foundry Observability** integrates with **Application Insights**. ([Microsoft Learn][12])

**S33. Setup Flow**

* **Key Elements**: Project → Enable Observability → App Insights connection flow diagram
* **Notes**: Monitoring is "prerequisite for continuous operations". ([Microsoft Learn][12])

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