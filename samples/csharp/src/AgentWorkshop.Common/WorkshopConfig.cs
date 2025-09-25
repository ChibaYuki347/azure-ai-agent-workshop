using System;
using System.Collections.Generic;

namespace AgentWorkshop.Common;

/// <summary>
/// Strongly-typed view of the environment variables required by the workshop samples.
/// Mirrors the Python configuration so that both stacks share the same setup guidance.
/// </summary>
public sealed class WorkshopConfig
{
    private static readonly IReadOnlyDictionary<string, string> EnvKeys = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
    {
        [nameof(ProjectEndpoint)] = "PROJECT_ENDPOINT",
        [nameof(ModelDeploymentName)] = "MODEL_DEPLOYMENT_NAME",
        [nameof(OpenAiConnectionId)] = "AZURE_OPENAI_CONNECTION_ID",
        [nameof(AiSearchConnectionId)] = "AI_SEARCH_CONNECTION_ID",
        [nameof(AiSearchIndexName)] = "AI_SEARCH_INDEX_NAME",
        [nameof(LogicAppCallbackUrl)] = "LOGIC_APP_CALLBACK_URL",
        [nameof(SubscriptionId)] = "AZURE_SUBSCRIPTION_ID",
        [nameof(ResourceGroupName)] = "AZURE_RESOURCE_GROUP_NAME",
        [nameof(EvaluationProjectEndpoint)] = "AZURE_AI_PROJECT",
        [nameof(EvaluationOpenAiEndpoint)] = "EVAL_AOAI_ENDPOINT",
        [nameof(EvaluationOpenAiApiKey)] = "EVAL_AOAI_API_KEY",
        [nameof(EvaluationOpenAiDeployment)] = "EVAL_AOAI_DEPLOYMENT",
        [nameof(EvaluationOpenAiApiVersion)] = "EVAL_AOAI_API_VERSION",
        [nameof(AppInsightsConnectionString)] = "APP_INSIGHTS_CONNECTION_STRING",
    };

    public string ProjectEndpoint { get; init; } = string.Empty;
    public string ModelDeploymentName { get; init; } = string.Empty;
    public string? OpenAiConnectionId { get; init; }
    public string? AiSearchConnectionId { get; init; }
    public string? AiSearchIndexName { get; init; }
    public string? LogicAppCallbackUrl { get; init; }
    public string? SubscriptionId { get; init; }
    public string? ResourceGroupName { get; init; }
    public string? EvaluationProjectEndpoint { get; init; }
    public string? EvaluationOpenAiEndpoint { get; init; }
    public string? EvaluationOpenAiApiKey { get; init; }
    public string? EvaluationOpenAiDeployment { get; init; }
    public string? EvaluationOpenAiApiVersion { get; init; }
    public string? AppInsightsConnectionString { get; init; }

    public bool HasSearch => !string.IsNullOrWhiteSpace(AiSearchConnectionId) && !string.IsNullOrWhiteSpace(AiSearchIndexName);
    public bool HasLogicApp => !string.IsNullOrWhiteSpace(LogicAppCallbackUrl);
    public bool HasEvaluationJudge => !string.IsNullOrWhiteSpace(EvaluationOpenAiEndpoint)
        && !string.IsNullOrWhiteSpace(EvaluationOpenAiApiKey)
        && !string.IsNullOrWhiteSpace(EvaluationOpenAiDeployment);

    public static WorkshopConfig Load(bool allowOptional = true)
    {
        static string GetRequired(string variable)
        {
            string? value = Environment.GetEnvironmentVariable(variable);
            if (string.IsNullOrWhiteSpace(value))
            {
                throw new InvalidOperationException($"環境変数 '{variable}' が設定されていません。README の手順を確認してください。");
            }

            return value;
        }

        string projectEndpoint = GetRequired(EnvKeys[nameof(ProjectEndpoint)]);
        string modelDeployment = GetRequired(EnvKeys[nameof(ModelDeploymentName)]);

        var values = new Dictionary<string, string?>(StringComparer.OrdinalIgnoreCase)
        {
            [nameof(ProjectEndpoint)] = projectEndpoint,
            [nameof(ModelDeploymentName)] = modelDeployment,
        };

        foreach (KeyValuePair<string, string> entry in EnvKeys)
        {
            if (values.ContainsKey(entry.Key))
            {
                continue;
            }

            string? value = Environment.GetEnvironmentVariable(entry.Value);
            if (!allowOptional && string.IsNullOrWhiteSpace(value))
            {
                value = GetRequired(entry.Value);
            }

            values[entry.Key] = value;
        }

        return new WorkshopConfig
        {
            ProjectEndpoint = values[nameof(ProjectEndpoint)] ?? string.Empty,
            ModelDeploymentName = values[nameof(ModelDeploymentName)] ?? string.Empty,
            OpenAiConnectionId = values[nameof(OpenAiConnectionId)],
            AiSearchConnectionId = values[nameof(AiSearchConnectionId)],
            AiSearchIndexName = values[nameof(AiSearchIndexName)],
            LogicAppCallbackUrl = values[nameof(LogicAppCallbackUrl)],
            SubscriptionId = values[nameof(SubscriptionId)],
            ResourceGroupName = values[nameof(ResourceGroupName)],
            EvaluationProjectEndpoint = values[nameof(EvaluationProjectEndpoint)],
            EvaluationOpenAiEndpoint = values[nameof(EvaluationOpenAiEndpoint)],
            EvaluationOpenAiApiKey = values[nameof(EvaluationOpenAiApiKey)],
            EvaluationOpenAiDeployment = values[nameof(EvaluationOpenAiDeployment)],
            EvaluationOpenAiApiVersion = values[nameof(EvaluationOpenAiApiVersion)] ?? "2024-05-01-preview",
            AppInsightsConnectionString = values[nameof(AppInsightsConnectionString)],
        };
    }
}
