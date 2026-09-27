using System;
using System.IO;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Compliance.Api.Controllers
{
    [Authorize(Roles = "Auditor")]
    [ApiController]
    [Route("api/audit")]
    public class AuditLogRangeController : ControllerBase
    {
        private const string AuditLog = "/var/compliance/audit.log";

        [HttpGet("chunk")]
        public IActionResult Chunk([FromQuery] long offset, [FromQuery] int length = 4096)
        {
            length = Math.Clamp(length, 1, 65536);

            using var fs = new FileStream(AuditLog, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
            if (offset < 0 || offset >= fs.Length)
            {
                return BadRequest();
            }

            fs.Seek(offset, SeekOrigin.Begin);
            var buffer = new byte[length];
            var read = fs.Read(buffer, 0, length);
            return Content(Encoding.UTF8.GetString(buffer, 0, read), "text/plain");
        }
    }
}
