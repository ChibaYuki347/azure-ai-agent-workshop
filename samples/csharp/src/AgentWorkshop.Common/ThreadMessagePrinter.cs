using System;
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

                        if (text.Annotations is { Count: > 0 })
                        {
                            foreach (MessageTextAnnotation annotation in text.Annotations)
                            {
                                switch (annotation)
                                {
                                    case MessageTextUriCitationAnnotation uriCitation when uriCitation.UriCitation is not null:
                                        string title = string.IsNullOrWhiteSpace(uriCitation.UriCitation.Title)
                                            ? uriCitation.UriCitation.Uri
                                            : uriCitation.UriCitation.Title;
                                        logger.LogInformation("    ↳ Citation: {Title} ({Url})", title, uriCitation.UriCitation.Uri);
                                        break;
                                    case MessageTextFileCitationAnnotation fileCitation:
                                        logger.LogInformation(
                                            "    ↳ File citation: {Quote} (File ID: {FileId})",
                                            fileCitation.Quote,
                                            fileCitation.FileId);
                                        break;
                                    case MessageTextFilePathAnnotation filePath:
                                        logger.LogInformation(
                                            "    ↳ File path: {FileId} ({Text})",
                                            filePath.FileId,
                                            filePath.Text);
                                        break;
                                }
                            }
                        }

                        break;
                    case MessageImageFileContent image:
                        logger.LogInformation("{Role}: 画像ファイル (ID: {Id})", role, image.FileId);
                        break;
                }
            }
        }
    }
}
