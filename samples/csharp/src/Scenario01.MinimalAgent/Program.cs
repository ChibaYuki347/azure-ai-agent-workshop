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
	ILogger logger = loggerFactory.CreateLogger("Scenario01.MinimalAgent");

	var credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
	{
		ExcludeInteractiveBrowserCredential = false,
	});

	PersistentAgentsClient agentClient = new(config.ProjectEndpoint, credential);

	PersistentAgent? agent = null;

	try
	{
		logger.LogInformation("Creating minimal agent with model {Model}", config.ModelDeploymentName);
		agent = await agentClient.Administration.CreateAgentAsync(
			model: config.ModelDeploymentName,
			name: "workshop-minimal-agent",
			instructions: "You are a polite assistant for quick math checks.",
			tools: new ToolDefinition[] { new CodeInterpreterToolDefinition() });

		PersistentAgentThread thread = await agentClient.Threads.CreateThreadAsync();

		logger.LogInformation("Posting user message to thread {ThreadId}", thread.Id);
		await agentClient.Messages.CreateMessageAsync(
			threadId: thread.Id,
			role: MessageRole.User,
			content: "Please plot y = 4x + 9 and summarise the intercepts.");

		ThreadRun run = await agentClient.Runs.CreateRunAsync(
			threadId: thread.Id,
			assistantId: agent.Id,
			additionalInstructions: "Address the user as Workshop Participant.");

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

		logger.LogInformation("Agent run completed. Fetching messages...");

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
