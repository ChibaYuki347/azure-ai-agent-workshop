using AgentWorkshop.Common;
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Logging;

try
{
	await RunAsync();
}
catch (Exception ex)
{
	Console.Error.WriteLine($"Unexpected failure: {ex.Message}");
	Environment.ExitCode = 1;
}

static async Task RunAsync()
{
	WorkshopConfig config = WorkshopConfig.Load();

	using ILoggerFactory loggerFactory = LoggingConfiguration.CreateLoggerFactory();
	ILogger logger = loggerFactory.CreateLogger("Scenario02.AiSearchRag");

	if (!config.HasSearch)
	{
		logger.LogError("AI_SEARCH_CONNECTION_ID と AI_SEARCH_INDEX_NAME を設定してください。");
		return;
	}

	var credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
	{
		ExcludeInteractiveBrowserCredential = false,
	});

	PersistentAgentsClient agentClient = new(config.ProjectEndpoint, credential);

	PersistentAgent? agent = null;

	try
	{
		AzureAISearchToolResource searchResource = new(
			config.AiSearchConnectionId!,
			config.AiSearchIndexName!,
			topK: 5,
			filter: string.Empty,
			queryType: AzureAISearchQueryType.VectorSemanticHybrid);

		ToolResources toolResources = new()
		{
			AzureAISearch = searchResource,
		};

		logger.LogInformation(
			"Creating Azure AI Search RAG agent with index {Index}",
			config.AiSearchIndexName);

		agent = await agentClient.Administration.CreateAgentAsync(
			model: config.ModelDeploymentName,
			name: "workshop-rag-agent",
			instructions: "You answer questions using the Azure AI Search tool. Always cite the document title and URL in markdown.",
			tools: new ToolDefinition[] { new AzureAISearchToolDefinition() },
			toolResources: toolResources);

		PersistentAgentThread thread = await agentClient.Threads.CreateThreadAsync();

		const string question = "Contoso 製品ラインの保守契約に関する最新の更新点を要約し、引用を明示してください。";
		logger.LogInformation("Posting user request to thread {ThreadId}", thread.Id);
		await agentClient.Messages.CreateMessageAsync(
			threadId: thread.Id,
			role: MessageRole.User,
			content: question);

		ThreadRun run = await agentClient.Runs.CreateRunAsync(
			threadId: thread.Id,
			assistantId: agent.Id,
			additionalInstructions: "Respond in Japanese when appropriate and include citations for all statements.");

		while (run.Status == RunStatus.InProgress || run.Status == RunStatus.Queued)
		{
			await Task.Delay(TimeSpan.FromMilliseconds(500));
			run = await agentClient.Runs.GetRunAsync(thread.Id, run.Id);
		}

		if (run.Status != RunStatus.Completed)
		{
			RequestFailedException? error = run.LastError is null
				? null
				: new RequestFailedException(
					status: 0,
					message: run.LastError.Message ?? "Run failed",
					errorCode: run.LastError.Code,
					innerException: null);

			if (error is not null)
			{
				throw error;
			}

			logger.LogWarning("Run finished with status {Status}", run.Status);
			return;
		}

		logger.LogInformation("Run completed. Fetching messages...");

		var messages = new List<PersistentThreadMessage>();
		await foreach (PersistentThreadMessage message in agentClient.Messages.GetMessagesAsync(
			threadId: thread.Id,
			order: ListSortOrder.Ascending))
		{
			messages.Add(message);
		}

		ThreadMessagePrinter.LogMessages(messages, logger);
	}
	catch (RequestFailedException ex)
	{
		logger.LogError(ex, "Azure AI Agent Service call failed.");
		throw;
	}
	finally
	{
		if (agent is not null)
		{
			logger.LogInformation("Deleting agent {AgentId}", agent.Id);
			await agentClient.Administration.DeleteAgentAsync(agent.Id);
		}
	}
}
