var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// The path inside the container where logs will be stored
const string LogFilePath = "/app/logs/transactions.log";

app.MapGet("/", () => "API is running. Use /write to add logs.");

app.MapGet("/write", () =>
{
    try 
    {
        Directory.CreateDirectory(Path.GetDirectoryName(LogFilePath)!);
        File.AppendAllText(LogFilePath, $"Log Entry: {DateTime.Now:yyyy-MM-dd HH:mm:ss}{Environment.NewLine}");
        return Results.Ok($"Success! Log written to {LogFilePath}");
    }
    catch (Exception ex)
    {
        return Results.Problem($"Failed to write log: {ex.Message}");
    }
});

app.Run("http://0.0.0.0:8080");