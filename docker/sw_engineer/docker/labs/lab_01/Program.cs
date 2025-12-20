var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Simple endpoint for demonstration
app.MapGet("/", () => "Welcome to Acme Corp! Running inside a Docker Container!");

app.Run();