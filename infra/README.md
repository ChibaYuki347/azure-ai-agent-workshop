# Infrastructure for Azure AI Agent Workshop

This folder hosts infrastructure-as-code assets and deployment guidance for the workshop scenarios described in `docs/ja/workshop-structure.md`.

## Target Azure Resources

| Layer | Resource | Purpose |
| --- | --- | --- |
| Governance | Resource Group (per environment) | Logical boundary for workshop assets. |
| Identity & Secrets | Azure Key Vault | Stores connection strings (Logic Apps, SMTP bridging, API auth). |
| Networking | Virtual Network (optional) | Provides private connectivity when Managed Network / Private Link is required. |
| Core AI | Azure AI Foundry hub + project | Hosts Azure AI Agent Service, Prompt flow, evaluation artifacts. *Created via portal/CLI today.* |
| Model Serving | Azure OpenAI resource | Deploy GPT-series models used by the agents. |
| Retrieval | Azure AI Search service + index | Backs the RAG scenarios. |
| Tooling | Logic App Standard | Implements the email/notification workflow consumed via Logic App tool. |
| Monitoring | Log Analytics workspace + Application Insights | Central monitoring for agent runs, Logic Apps, and evaluation flows. |
| Evaluation | Azure AI Project (Prompt flow) features | Lives inside the AI Foundry project; uses Storage + App Insights. |
| API Management (optional) | Azure API Management (Developer tier) | Demonstrates rate limiting and token throttling policies. |
| Storage | General-purpose Storage account | Stores RAG source docs, evaluation datasets, Logic App state. |

## Deployment Options

1. **Baseline Bicep template** (`main.bicep`): provisions repeatable resources (all except the AI Foundry hub/project, which currently require Azure CLI/portal).
2. **Post-deploy scripts**: configure AI Search index, Logic App workflow definition, and API Management policies.
3. **Manual steps**: create the Azure AI Foundry hub/project and enable Agent Service & Prompt flow (until full ARM/Bicep coverage is available).

## Environments

Use consistent naming such as:

- `rg-aiagent-workshop-<env>` (resource group)
- `vnet-aiagent-<env>` (optional VNet)
- `aifoundry-hub-<env>` / `aifoundry-project-<env>` (hub/project)
- `aoai-<region>-<env>` (Azure OpenAI)
- `aisearch-<env>` (AI Search)
- `logicapp-agent-<env>` (Logic App)
- `appi-aiagent-<env>` (Application Insights)
- `kv-aiagent-<env>` (Key Vault)

## Prerequisites

- Azure CLI `2.62.0` or later (for `az ai` commands)
- Bicep CLI `0.26.170` or later
- Required Azure subscriptions with `Owner` or equivalent permissions for deployment
- Quota for Azure OpenAI models (GPT-4o, GPT-4o-mini)

## Deployment Flow

1. Deploy the baseline template (Bicep) to create shared resources.
2. Create the Azure AI Foundry hub and project (`az ai project create ...`).
3. Connect the project to existing Azure OpenAI, AI Search, Logic App by assigning connections.
4. Import Logic App workflow definition and connections (scripts to be added).
5. Configure Prompt flow evaluation workspace and Application Insights linkage.
6. (Optional) Apply API Management token limiting policy.

### 1. Deploy baseline resources

```bash
# login and select subscription
az login
az account set --subscription <subscription-id>

# deploy bicep (requires Bicep CLI / az CLI 2.62+)
az deployment group create \
  --resource-group rg-aiagent-workshop-dev \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json \
  --parameters adminObjectId=<your-AAD-object-id>
```

> **Note**: local environment currently lacks the Bicep CLI (`bicep build` failed). Install it via `az bicep install` before running the deployment.

### 2. Create Azure AI Foundry hub & project

```bash
az extension add --name ai-experimental
az ai hub create --name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev --location japaneast
az ai project create --name aifoundry-project-dev --hub-name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev
```

Associate connections inside the project:

```bash
az ai project connection create aoai --name aoai-connection --project-name aifoundry-project-dev --resource-group rg-aiagent-workshop-dev --resource-id $(az cognitiveservices account show --name workshop-aoai --resource-group rg-aiagent-workshop-dev --query id -o tsv)
az ai project connection create aisearch --name aisearch-connection --project-name aifoundry-project-dev --resource-group rg-aiagent-workshop-dev --service-endpoint https://workshop-aisearch.search.windows.net --api-key <key-from-keyvault>
```

### 3. Import Logic App workflow definition

Update `logic-app-definition.json` with the actual email connector, then redeploy or use:

```bash
az logic workflow update --name workshop-agent-logicapp --resource-group rg-aiagent-workshop-dev --definition @infra/logic-app-definition.json --parameters "{\"$connections\":{...}}"
```

### 4. Configure evaluation and observability

- Enable Prompt flow evaluation inside the AI Foundry project, pointing to the existing Application Insights instance (`appi-aiagent-<env>`).
- Create evaluation datasets in the storage account container `evaluation` and register them in Prompt flow.
- Enable diagnostic settings (already configured for Logic App/API Management) and review data in Log Analytics.

Detailed command snippets follow in the root `README` once the automation scripts are completed.
