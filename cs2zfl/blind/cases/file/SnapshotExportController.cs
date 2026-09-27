using System;
using System.IO;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;

namespace Monitoring.Api.Controllers
{
    public class SnapshotExportRequest
    {
        public string OutputName { get; set; } = "";
        public string Format { get; set; } = "json";
        public DateTime From { get; set; }
        public DateTime To { get; set; }
    }

    [ApiController]
    [Route("api/snapshots")]
    public class SnapshotExportController : ControllerBase
    {
        private const string ExportDir = "/var/monitoring/exports";

        [HttpPost("export")]
        public IActionResult Export([FromBody] SnapshotExportRequest request)
        {
            if (request.To < request.From)
            {
                return BadRequest("Invalid range.");
            }

            var payload = JsonSerializer.SerializeToUtf8Bytes(new
            {
                request.From,
                request.To,
                generated = DateTime.UtcNow
            });

            var target = Path.Combine(ExportDir, request.OutputName);
            System.IO.File.WriteAllBytes(target, payload);

            return Accepted(new { path = request.OutputName });
        }
    }
}
