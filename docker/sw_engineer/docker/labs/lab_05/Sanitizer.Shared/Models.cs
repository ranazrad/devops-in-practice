namespace Sanitizer.Shared;

public enum DocStatus
{
    Pending,
    Processing,
    Clean,
    Failed  
}

public class DocRequest
{
    public int Id { get; set; }
    public string FileName { get; set; } = string.Empty;
    public string Owner { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DocStatus Status { get; set; } = DocStatus.Pending;
    public string Log { get; set; } = "File uploaded to secure vault.";
}