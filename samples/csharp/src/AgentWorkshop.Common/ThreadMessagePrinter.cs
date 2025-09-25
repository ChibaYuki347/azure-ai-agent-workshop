using System.Collections.Generic;
using Azure.AI.Agents.Persistent;
using Microsoft.Extensions.Logging;

namespace AgentWorkshop.Common;

public static class ThreadMessagePrinter
{
    public static void LogMessages(IEnumerable<PersistentThreadMessage> messages, ILogger logger)
    {
        foreach (PersistentThreadMessage message in messages)
        {
            string role = message.Role.ToString();

            foreach (MessageContent content in message.ContentItems)
            {
                switch (content)
                {
                    case MessageTextContent text:
                        logger.LogInformation("{Role}: {Text}", role, text.Text);
                        break;
                    case MessageImageFileContent image:
                        logger.LogInformation("{Role}: 画像ファイル (ID: {Id})", role, image.FileId);
                        break;
                }
            }
        }
    }
}
