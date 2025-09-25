using Microsoft.Extensions.Logging;

namespace AgentWorkshop.Common;

public static class LoggingConfiguration
{
    public static ILoggerFactory CreateLoggerFactory(LogLevel level = LogLevel.Information)
    {
        return LoggerFactory.Create(builder =>
        {
            builder.ClearProviders();
            builder.SetMinimumLevel(level);
            builder.AddSimpleConsole(options =>
            {
                options.TimestampFormat = "yyyy-MM-dd HH:mm:ss ";
                options.SingleLine = true;
                options.IncludeScopes = false;
            });
        });
    }

    public static ILogger<T> CreateLogger<T>(LogLevel level = LogLevel.Information)
        => CreateLoggerFactory(level).CreateLogger<T>();
}
