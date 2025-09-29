# Azure AI Agent Build and Manage Workshop

[![English](https://img.shields.io/badge/🌐-English-blue.svg)](./README.md)
[![日本語](https://img.shields.io/badge/🌐-日本語-red.svg)](./README.ja.md)

A comprehensive 2-day workshop for building, evaluating, and managing production-ready AI agents using **Azure AI Foundry Agent Service**.

## 🎯 Workshop Goals

This workshop equips participants with hands-on experience in:

1. **Understanding Agentic AI fundamentals** - Core concepts, tools, and Azure AI Agent Service architecture
2. **Building minimal agents** - From basic conversations to RAG-enabled and tool-calling agents
3. **Production readiness** - Evaluation, observability, security, and operational best practices

## 📚 Workshop Structure

### Day 1: "Build and Run Agents" (4 hours)
- **Module A-C**: Agentic AI concepts, Azure AI Agent Service foundations, hands-on "Hello Agent"
- **Module D-F**: RAG with Azure AI Search, Logic Apps tool integration, Connected Agents (multi-agent patterns)

### Day 2: "Evaluate, Secure, and Operate" (4 hours)

- **Module G-I**: Advanced multi-agent patterns, Prompt flow evaluation, observability with Application Insights
- **Module J-M**: Content Safety, RBAC & identity, network isolation, quota & rate limiting, cost optimization

> 📖 **Detailed curriculum**: 
> - English: [docs/en/workshop-structure.md](./docs/en/workshop-structure.md)
> - Japanese: [docs/ja/workshop-structure.md](./docs/ja/workshop-structure.md)

## 🚀 Quick Start

### Prerequisites

- Azure subscription with sufficient quota for:
  - Azure OpenAI (GPT-4o, GPT-4o-mini)
  - Azure AI Search (Standard tier)
  - Azure AI Agent Service
- Azure CLI 2.72.0+ with Bicep support
- Visual Studio Code or preferred editor
- Python 3.8+ or .NET 6+ (depending on sample choice)

### 1. Infrastructure Setup

Deploy the workshop infrastructure using Bicep:

```bash
# Clone the repository
git clone https://github.com/ChibaYuki347/azure-ai-agent-workshop.git
cd azure-ai-agent-workshop

# Login and set subscription
az login
az account set --subscription <your-subscription-id>

# Create resource group
az group create --name rg-aiagent-workshop-dev --location japaneast

# Deploy infrastructure
az deployment group create \
  --resource-group rg-aiagent-workshop-dev \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json \
  --parameters adminObjectId=<your-azure-ad-object-id>
```

> 📋 **Infrastructure details**: See [infra/README.md](./infra/README.md) for complete deployment guide and post-deployment steps

### 2. Manual Configuration

After Bicep deployment, complete these manual steps:

1. **Azure AI Foundry Hub & Project** (until ARM support is available):
   ```bash
   az ai hub create --name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev
   az ai project create --name aifoundry-project-dev --hub-name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev
   ```

2. **AI Agent Service Connection**: In Azure portal, open the AI Agent Service account and manually create an Azure OpenAI connection using Entra ID authentication.

3. **AI Search Index**: Upload sample documents and create search indexes for RAG scenarios.

### 3. Run Workshop Samples

Choose your preferred language and follow the samples:

#### Python Samples
```bash
cd samples/python
pip install -r requirements.txt

# Basic agent conversation
python basic_agent.py

# RAG-enabled agent
python rag_agent.py

# Tool-calling agent with Logic Apps
python tool_agent.py
```

#### C# Samples
```bash
cd samples/csharp
dotnet restore

# Basic agent conversation
dotnet run --project BasicAgent

# RAG-enabled agent
dotnet run --project RagAgent

# Tool-calling agent
dotnet run --project ToolAgent
```

## 📁 Repository Structure

```
├── README.md                          # This file
├── README.ja.md                       # Japanese version
├── docs/                              # Workshop documentation
│   ├── en/                           # English documentation
│   └── ja/                           # Japanese documentation
│       └── workshop-structure.md     # Detailed curriculum
├── infra/                            # Infrastructure as Code
│   ├── main.bicep                    # Main Bicep template
│   ├── main.parameters.json          # Deployment parameters
│   ├── logic-app-definition.json     # Logic App workflow
│   └── README.md                     # Infrastructure guide
└── samples/                          # Workshop code samples
    ├── python/                       # Python samples
    │   ├── basic_agent.py           # Basic agent example
    │   ├── rag_agent.py             # RAG-enabled agent
    │   ├── tool_agent.py            # Tool-calling agent
    │   └── requirements.txt         # Python dependencies
    └── csharp/                       # C# samples
        ├── BasicAgent/              # Basic agent project
        ├── RagAgent/                # RAG agent project
        └── ToolAgent/               # Tool agent project
```

## 🔧 What Gets Deployed

The Bicep template provisions:

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Azure AI Agent Service** | Managed agent runtime with GPT-4o/4o-mini deployments | Custom RAI policies, project management |
| **Azure OpenAI** | Model serving for agents | GPT-4 deployment with content safety |
| **Azure AI Search** | RAG knowledge retrieval | Standard tier with semantic search |
| **Logic App Standard** | External tool integration | HTTP trigger for agent tool calls |
| **Key Vault** | Secrets and connection strings | RBAC-secured access |
| **Application Insights** | Observability and monitoring | Agent conversation tracking |
| **API Management** | Rate limiting and access control | Optional token-based throttling |

## 🎓 Learning Paths

### For Developers
- Start with `samples/python/basic_agent.py` or `samples/csharp/BasicAgent`
- Progress through RAG and tool integration samples
- Explore evaluation flows in Day 2 modules

### For Architects
- Review infrastructure design in `infra/main.bicep`
- Focus on network isolation and security modules (Day 2)
- Study multi-agent patterns and Connected Agents

### For Operators
- Examine observability setup and dashboards
- Learn quota management and cost optimization
- Practice with Content Safety and RBAC configurations

## 🛟 Troubleshooting

### Common Issues
- **RequestConflict during deployment**: Azure AI Agent Service operations conflict. Wait 5-10 minutes and retry.
- **Model deployment quota**: Ensure sufficient TPM quota in your region for GPT-4o models.
- **Logic App tool errors**: Verify `triggerBody()` expressions match your JSON schema.

### Getting Help
- Check [infra/README.md](./infra/README.md) for deployment troubleshooting
- Review Azure AI Agent Service [official documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/)
- Open issues in this repository for workshop-specific problems

## 🌐 Languages

- **English**: Primary documentation language
- **日本語**: Full Japanese translation available in [README.ja.md](./README.ja.md) and `docs/ja/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements to the workshop content, infrastructure templates, or sample code.

---

**Ready to build intelligent agents?** Start with the infrastructure setup above, then dive into the samples! 🚀