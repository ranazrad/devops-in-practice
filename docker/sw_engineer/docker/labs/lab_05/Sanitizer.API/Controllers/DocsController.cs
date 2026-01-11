using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RabbitMQ.Client;
using Sanitizer.Shared;
using System.Text;
using System.Text.Json;

namespace Sanitizer.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocsController : ControllerBase
{
    private readonly AppDbContext _db;
    private readonly IConfiguration _config;
    private readonly ILogger<DocsController> _logger;

    public DocsController(AppDbContext db, IConfiguration config, ILogger<DocsController> logger)
    {
        _db = db;
        _config = config;
        _logger = logger;
    }

    [HttpGet]
    public async Task<IActionResult> GetDocs()
    {
        return Ok(await _db.Docs.OrderByDescending(d => d.CreatedAt).Take(20).ToListAsync());
    }

    [HttpPost]
    public async Task<IActionResult> Upload([FromBody] DocRequest request)
    {
        // 1. Save to MySQL
        request.Status = DocStatus.Pending;
        request.CreatedAt = DateTime.UtcNow;
        _db.Docs.Add(request);
        await _db.SaveChangesAsync();

        _logger.LogInformation("New file received: {FileName} (ID: {Id})", request.FileName, request.Id);

        // 2. Publish to RabbitMQ
        var factory = new ConnectionFactory() { HostName = _config["MessageBroker"] ?? "broker-rabbit" };
        using var connection = factory.CreateConnection();
        using var channel = connection.CreateModel();

        channel.QueueDeclare(queue: "sanitization_queue", durable: false, exclusive: false, autoDelete: false, arguments: null);

        var body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(request));

        channel.BasicPublish(exchange: "", routingKey: "sanitization_queue", basicProperties: null, body: body);

        return Ok(request);
    }
}