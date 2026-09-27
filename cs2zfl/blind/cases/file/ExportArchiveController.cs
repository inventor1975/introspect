using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Warehouse.Api.Controllers
{
    [ApiController]
    [Route("api/exports")]
    public class ExportArchiveController : ControllerBase
    {
        private static readonly string ExportRoot = "/var/warehouse/exports";

        [HttpGet("archive")]
        public IActionResult GetArchive([FromQuery] string month, [FromQuery] string file)
        {
            var candidate = Path.Combine(ExportRoot, month, file);

            if (!candidate.StartsWith(ExportRoot, StringComparison.Ordinal))
            {
                return BadRequest("Invalid path.");
            }

            var stream = System.IO.File.OpenRead(candidate);
            return File(stream, "application/zip", file);
        }
    }
}
