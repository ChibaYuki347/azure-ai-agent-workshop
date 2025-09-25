using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Azure.AI.Agents.Persistent;
using Microsoft.Extensions.Logging;

namespace AgentWorkshop.Common;

/// <summary>
/// Configuration used for forwarding function tool invocations to a Logic App workflow.
/// </summary>
public sealed record LogicAppToolConfig
{
    public LogicAppToolConfig(string callbackUrl)
    {
        if (string.IsNullOrWhiteSpace(callbackUrl))
        {
            throw new ArgumentException("Logic App のコールバック URL は必須です。", nameof(callbackUrl));
        }

        if (!Uri.TryCreate(callbackUrl, UriKind.Absolute, out Uri? uri))
        {
            throw new ArgumentException("有効な絶対 URL を指定してください。", nameof(callbackUrl));
        }

        CallbackUri = uri;
    }

    /// <summary>
    /// Logic App の HTTP トリガー URL。
    /// </summary>
    public Uri CallbackUri { get; }

    /// <summary>
    /// HTTP 呼び出しのタイムアウト。省略時は 30 秒。
    /// </summary>
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}

/// <summary>
/// Logic App 連携用の Function Tool を生成し、ツール呼び出しが要求された際に HTTP 経由で Logic App を起動するヘルパー。
/// </summary>
public sealed class LogicAppFunctionTool
{
    public const string ToolName = "send_email_via_logic_app";

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull,
        WriteIndented = false,
    };

    public LogicAppFunctionTool(LogicAppToolConfig config, string? description = null)
    {
        Config = config ?? throw new ArgumentNullException(nameof(config));
        string toolDescription = description ?? "Send an email notification via Logic App.";

        Definition = new FunctionToolDefinition(
            name: ToolName,
            description: toolDescription,
            parameters: BinaryData.FromObjectAsJson(
                new
                {
                    Type = "object",
                    Properties = new
                    {
                        To = new { Type = "string", Description = "Recipient email address." },
                        Subject = new { Type = "string", Description = "Mail subject." },
                        Body = new { Type = "string", Description = "Mail body text." },
                    },
                    Required = new[] { "to", "subject", "body" },
                },
                JsonOptions));

        Definitions = new[] { (ToolDefinition)Definition };
    }

    public LogicAppToolConfig Config { get; }

    public FunctionToolDefinition Definition { get; }

    public IReadOnlyList<ToolDefinition> Definitions { get; }

    /// <summary>
    /// SubmitToolOutputsAction に含まれるツール呼び出しを処理し、Logic App 実行結果を ToolOutput として返します。
    /// </summary>
    public async Task<IReadOnlyList<ToolOutput>> ExecutePendingToolCallsAsync(
        SubmitToolOutputsAction action,
        HttpClient? httpClient = null,
        ILogger? logger = null,
        CancellationToken cancellationToken = default)
    {
        if (action is null)
        {
            throw new ArgumentNullException(nameof(action));
        }

        var outputs = new List<ToolOutput>(action.ToolCalls.Count);

        foreach (RequiredToolCall toolCall in action.ToolCalls)
        {
            ToolOutput? output = await TryHandleToolCallAsync(toolCall, httpClient, logger, cancellationToken).ConfigureAwait(false);
            if (output is not null)
            {
                outputs.Add(output);
            }
        }

        return outputs;
    }

    /// <summary>
    /// 単一のツール呼び出しを Logic App に転送します。対象外のツール名の場合は <c>null</c> を返します。
    /// </summary>
    public async Task<ToolOutput?> TryHandleToolCallAsync(
        RequiredToolCall toolCall,
        HttpClient? httpClient = null,
        ILogger? logger = null,
        CancellationToken cancellationToken = default)
    {
        if (toolCall is not RequiredFunctionToolCall functionCall)
        {
            return null;
        }

        if (!string.Equals(functionCall.Name, ToolName, StringComparison.OrdinalIgnoreCase))
        {
            return null;
        }

        (string To, string Subject, string Body) arguments = ParseArguments(functionCall);

        HttpClient client = httpClient ?? CreateHttpClient();
        bool disposeClient = httpClient is null;

        try
        {
            using HttpRequestMessage request = BuildRequest(arguments);
            logger?.LogInformation("Logic App を呼び出します: {Uri}", request.RequestUri);

            using HttpResponseMessage response = await client.SendAsync(request, cancellationToken).ConfigureAwait(false);
            string responseBody = await response.Content.ReadAsStringAsync(cancellationToken).ConfigureAwait(false);

            logger?.LogInformation("Logic App 応答: {StatusCode}", response.StatusCode);

            response.EnsureSuccessStatusCode();

            string? location = response.Headers.TryGetValues("Location", out IEnumerable<string>? values)
                ? values.FirstOrDefault()
                : null;

            var resultPayload = new
            {
                status = (int)response.StatusCode,
                reason = response.ReasonPhrase,
                location,
                body = string.IsNullOrWhiteSpace(responseBody) ? null : responseBody,
            };

            string serialized = JsonSerializer.Serialize(resultPayload, JsonOptions);

            return new ToolOutput(functionCall, serialized);
        }
        catch (HttpRequestException ex)
        {
            logger?.LogError(ex, "Logic App 呼び出しに失敗しました。");
            throw;
        }
        finally
        {
            if (disposeClient)
            {
                client.Dispose();
            }
        }
    }

    private HttpClient CreateHttpClient()
    {
        return new HttpClient
        {
            Timeout = Config.Timeout,
        };
    }

    private HttpRequestMessage BuildRequest((string To, string Subject, string Body) arguments)
    {
        var payload = new
        {
            to = arguments.To,
            subject = arguments.Subject,
            body = arguments.Body,
        };

        string json = JsonSerializer.Serialize(payload, JsonOptions);
        var request = new HttpRequestMessage(HttpMethod.Post, Config.CallbackUri)
        {
            Content = new StringContent(json, Encoding.UTF8, "application/json"),
        };

        return request;
    }

    private static (string To, string Subject, string Body) ParseArguments(RequiredFunctionToolCall functionCall)
    {
        try
        {
            using JsonDocument json = JsonDocument.Parse(functionCall.Arguments);
            JsonElement root = json.RootElement;

            string to = GetRequiredString(root, "to");
            string subject = GetRequiredString(root, "subject");
            string body = GetRequiredString(root, "body");

            return (to, subject, body);
        }
        catch (JsonException ex)
        {
            throw new InvalidOperationException("Logic App ツールの引数を解析できません。", ex);
        }
    }

    private static string GetRequiredString(JsonElement root, string propertyName)
    {
        if (!root.TryGetProperty(propertyName, out JsonElement valueElement))
        {
            throw new InvalidOperationException($"Logic App ツールの引数 '{propertyName}' が見つかりません。");
        }

        string? value = valueElement.GetString();
        if (string.IsNullOrWhiteSpace(value))
        {
            throw new InvalidOperationException($"Logic App ツールの引数 '{propertyName}' が空です。");
        }

        return value;
    }
}
