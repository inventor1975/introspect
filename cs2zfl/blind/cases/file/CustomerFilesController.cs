using System;
using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Crm.Api.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/customers/files")]
    public class CustomerFilesController : ControllerBase
    {
        private static readonly string FilesRoot =
            Path.GetFullPath("/srv/crm/customer-files") + Path.DirectorySeparatorChar;

        [HttpGet]
        public IActionResult Get([FromQuery] string path)
        {
            if (string.IsNullOrWhiteSpace(path))
            {
                return BadRequest();
            }

            var requested = Path.GetFullPath(Path.Combine(FilesRoot, path));
            if (!requested.StartsWith(FilesRoot, StringComparison.Ordinal))
            {
                return Forbid();
            }

            if (!System.IO.File.Exists(requested))
            {
                return NotFound();
            }

            return PhysicalFile(requested, "application/octet-stream", Path.GetFileName(requested));
        }
    }
}
