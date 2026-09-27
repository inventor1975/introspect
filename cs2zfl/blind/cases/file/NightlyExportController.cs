using System;
using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace Erp.Integration.Controllers
{
    [Authorize(Roles = "Integration")]
    [ApiController]
    [Route("api/nightly")]
    public class NightlyExportController : ControllerBase
    {
        private readonly IConfiguration _config;

        public NightlyExportController(IConfiguration config)
        {
            _config = config;
        }

        [HttpGet("export")]
        public IActionResult Export([FromQuery] string format)
        {
            var exportDir = _config["NightlyExport:Directory"];
            var fileName = format == "xml" ? "nightly.xml" : "nightly.csv";
            var path = Path.Combine(exportDir!, fileName);

            if (!System.IO.File.Exists(path))
            {
                return NotFound(new { message = "Export not generated yet." });
            }

            var contentType = format == "xml" ? "application/xml" : "text/csv";
            return PhysicalFile(path, contentType, $"nightly-{DateTime.UtcNow:yyyyMMdd}.{(format == "xml" ? "xml" : "csv")}");
        }
    }
}
