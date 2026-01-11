using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using Sanitizer.Shared;
using System.Text;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

namespace Sanitizer.Engine;

// נגדיר את ה-DbContext גם כאן
public class EngineDbContext : DbContext
{
    public DbSet<DocRequest> Docs { get; set; }
    
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // קורא Environment Variable שהזרקנו בדוקר
        var conn = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        optionsBuilder.UseMySql(conn, ServerVersion.AutoDetect(conn));
    }
}

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly string _hostname;

    public Worker(ILogger<Worker> logger, IConfiguration config)
    {
        _logger = logger;
        _hostname = config["MessageBroker"] ?? "broker-rabbit";
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // המתנה שה-RabbitMQ יעלה
        await Task.Delay(10000, stoppingToken);

        var factory = new ConnectionFactory() { HostName = _hostname };
        using var connection = factory.CreateConnection();
        using var channel = connection.CreateModel();

        channel.QueueDeclare(queue: "sanitization_queue", durable: false, exclusive: false, autoDelete: false, arguments: null);

        var consumer = new EventingBasicConsumer(channel);
        consumer.Received += async (model, ea) =>
        {
            try
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                var doc = JsonSerializer.Deserialize<DocRequest>(message);

                if (doc != null)
                {
                    await ProcessFile(doc);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing message");
            }
        };

        channel.BasicConsume(queue: "sanitization_queue", autoAck: true, consumer: consumer);
        
        // Loop forever
        await Task.Delay(Timeout.Infinite, stoppingToken);
    }

    private async Task ProcessFile(DocRequest doc)
    {
        _logger.LogInformation("Starting Sanitization for: {FileName}", doc.FileName);

        using var db = new EngineDbContext();

        // 1. Update Status to Processing
        var record = await db.Docs.FindAsync(doc.Id);
        if (record != null)
        {
            record.Status = DocStatus.Processing;
            record.Log = "Threat analysis in progress...";
            await db.SaveChangesAsync();
        }

        // 2. SIMULATE WORK (The Whitening Process)
        await Task.Delay(5000); // 5 seconds work

        // 3. Update Status to Clean
        if (record != null)
        {
            record.Status = DocStatus.Clean;
            record.Log = "File Disarmed and Reconstructed successfully.";
            await db.SaveChangesAsync();
            _logger.LogInformation("File {FileName} is CLEAN.", doc.FileName);
        }
    }
}