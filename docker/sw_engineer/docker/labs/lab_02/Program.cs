var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Endpoint to check Environment Variables and Version
app.MapGet("/", () => new 
{ 
    Message = "Hello from Docker!",
    Environment = Environment.GetEnvironmentVariable("APP_MODE") ?? "Not Set",
    Version = "1.0.0" // This could be passed via ARG/ENV
});

app.Run();