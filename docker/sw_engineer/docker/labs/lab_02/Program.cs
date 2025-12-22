var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Endpoint to check Environment Variables and Version
string version = Environment.GetEnvironmentVariable("APP_VERSION") ?? "No Version Provided";
string mode = Environment.GetEnvironmentVariable("APP_MODE") ?? "Development";

app.MapGet("/", () => new 
{ 
    Message = "Hello from Docker!",
    CurrentMode = mode,
    BuildVersion = version
});

app.Run();