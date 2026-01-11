using Microsoft.EntityFrameworkCore;
using RabbitMQ.Client;
using Sanitizer.Shared;
using Serilog;
using System.Text;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);

// 1. Serilog Setup
builder.Host.UseSerilog((ctx, lc) => lc
    .ReadFrom.Configuration(ctx.Configuration)
    .WriteTo.Console()
    .WriteTo.Seq(ctx.Configuration["Serilog:SeqUrl"] ?? "http://logs-seq:80"));

// 2. Database Setup
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));

// 3. RabbitMQ & Services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// 4. Ensure DB Created (Auto Migration for Demo)
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    // Retry logic for DB connection
    for (int i = 0; i < 10; i++)
    {
        try {
            if (db.Database.CanConnect()) {
                db.Database.EnsureCreated();
                break;
            }
        } catch { Thread.Sleep(2000); }
    }
}

app.UseSwagger();
app.UseSwaggerUI();
app.UseAuthorization();
app.MapControllers();

app.Run();

// --- Classes in same file for simplicity ---

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<DocRequest> Docs { get; set; }
}