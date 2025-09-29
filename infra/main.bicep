@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Environment name suffix (e.g. dev, staging, prod). Used for resource naming.')
param environment string

@description('Azure AD object ID for the primary administrator (granted access to Key Vault).')
param adminObjectId string

@description('SKU for the Azure AI Search service.')
@allowed([
  'basic'
  'standard'
  'standard2'
  'standard3'
])
param aiSearchSku string = 'standard'

@description('SKU tier for Azure OpenAI.')
@allowed([
  'S0'
])
param openAiSku string = 'S0'

@description('Replica count for Azure AI Search service.')
@minValue(1)
param aiSearchReplicaCount int = 1

@description('Partition count for Azure AI Search service.')
@minValue(1)
param aiSearchPartitionCount int = 1

@description('Logic App workflow definition. Override with a file path via `bicep --parameters`.')
param logicAppDefinition object = loadJsonContent('logic-app-definition.json')

@description('Enable deployment of an Azure API Management instance for rate limiting demos.')
param deployApim bool = false

@description('Tags applied to all resources.')
param resourceTags object = {
  workload: 'azure-ai-agent-workshop'
  environment: environment
}

var envSanitized = toLower(replace(environment, '-', ''))
var envSegment = substring(envSanitized, 0, min(length(envSanitized), 8))
var uniqueSegment = substring(uniqueString(resourceGroup().id), 0, 6)
var namePrefix = toLower(replace('${environment}-aiagent', '--', '-'))
var workspaceName = '${namePrefix}-log'
var appInsightsName = '${namePrefix}-appi'
var storageName = '${envSegment}ai${uniqueSegment}'
var keyVaultName = toLower(replace('${environment}-aiagent-kv', '-', ''))
var openAiName = toLower('${environment}-aoai')
var aiSearchName = toLower('${environment}-aisearch')
var logicAppName = '${environment}-agent-logicapp'
var apimName = toLower('${environment}-aiagent-apim')

// Log Analytics workspace
resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: workspaceName
  location: location
  tags: resourceTags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Application Insights linked to Log Analytics
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  tags: resourceTags
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Azure'
    WorkspaceResourceId: logWorkspace.id
  }
}

// Storage account for workshop assets
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  tags: resourceTags
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    supportsHttpsTrafficOnly: true
  }
}

// Key Vault for secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: resourceTags
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enablePurgeProtection: true
    enableSoftDelete: true
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: adminObjectId
        permissions: {
          secrets: [
            'get'
            'list'
            'set'
            'delete'
            'recover'
          ]
        }
      }
    ]
    publicNetworkAccess: 'Enabled'
  }
}

// Azure OpenAI resource
resource openAi 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiName
  location: location
  kind: 'OpenAI'
  sku: {
    name: openAiSku
  }
  tags: resourceTags
  properties: {
    apiProperties: {
      statisticsEnabled: true
    }
    publicNetworkAccess: 'Enabled'
  }
}

// Azure AI Search service
resource search 'Microsoft.Search/searchServices@2023-11-01' = {
  name: aiSearchName
  location: location
  sku: {
    name: aiSearchSku
  }
  tags: resourceTags
  properties: {
    hostingMode: 'default'
    partitionCount: aiSearchPartitionCount
    replicaCount: aiSearchReplicaCount
    publicNetworkAccess: 'enabled'
  }
}

// Logic App (consumption) with placeholder definition
resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: logicAppName
  location: location
  tags: resourceTags
  properties: {
    state: 'Enabled'
    definition: logicAppDefinition
  }
}

// Optional API Management for rate limiting demos
resource apim 'Microsoft.ApiManagement/service@2022-08-01' = if (deployApim) {
  name: apimName
  location: location
  tags: resourceTags
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherEmail: 'admin@example.com'
    publisherName: 'Agent Workshop'
    virtualNetworkType: 'None'
  }
}

// Diagnostic settings linking Logic App and API Management to Log Analytics
resource logicAppDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: '${logicApp.name}-diag'
  scope: logicApp
  properties: {
    workspaceId: logWorkspace.id
    logs: [
      {
        category: 'WorkflowRuntime'
        enabled: true
      }
    ]
  }
}

resource apimDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (deployApim) {
  name: '${apim.name}-diag'
  scope: apim
  properties: {
    workspaceId: logWorkspace.id
    logs: [
      {
        category: 'GatewayLogs'
        enabled: true
        retentionPolicy: {
          enabled: false
          days: 0
        }
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          enabled: false
          days: 0
        }
      }
    ]
  }
}

output storageAccountName string = storage.name
output keyVaultName string = keyVault.name
output openAiAccountName string = openAi.name
output aiSearchServiceName string = search.name
output logicAppCallbackUrl string = logicApp.properties.accessEndpoint
output logAnalyticsWorkspaceId string = logWorkspace.id
output appInsightsName string = appInsights.name
output apiManagementName string = deployApim ? apim.name : 'not-deployed'
