# Hands-on Lab: Building Your Own Search Agent

This guide walks you through creating a custom search agent using Azure AI Agent Service. The example involves building an agent that can perform web searches and return structured information based on user queries.

## Prerequisites

- An Azure subscription with access to Azure AI Agent Service.
- Uploaded your own documents to Blob Storage

Create required resources such as Azure AI Foundry, AI Agent Service, and AI Search.

use Bicep template in this repo for easy setup.

## Instructions - Indexing Documents

**Create AI Search Index**: In the Azure portal, navigate to your Azure AI Search resource and create a new index. 
Push "**Import data(new)**" button and follow the wizard to create an index from your Blob Storage container where you uploaded your documents.

## Instructions - Creating Agents

1. Navigate to Azure AI Foundry portal
2. Go to your project. 
3. Create a new agent with the following Instructions:

```txt
You are a "Search Agent."
Your role is to perform retrieve relevant information from an AI Search index.
Given a user's query, you should gather relevant, credible sourcesand return a structured search output.
```

 4. Push "Try in Playground" button to test the agent.

Prompt example:
```txt
Tell me about Azure AI Agent Workshop Structure
```

