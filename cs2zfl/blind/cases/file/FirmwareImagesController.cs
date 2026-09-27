using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Devices.Fleet.Controllers
{
    [ApiController]
    [Route("api/firmware")]
    public class FirmwareImagesController : ControllerBase
    {
        private const string FirmwareDir = "/srv/fleet/firmware";

        [HttpGet("image")]
        public IActionResult Image([FromQuery(Name = "path")] string relativePath)
        {
            if (string.IsNullOrEmpty(relativePath) || relativePath.Contains(".."))
            {
                return BadRequest(new { error = "invalid path" });
            }

            var full = Path.Combine(FirmwareDir, relativePath);
            if (!System.IO.File.Exists(full))
            {
                return NotFound();
            }

            return PhysicalFile(full, "application/octet-stream", enableRangeProcessing: true);
        }
    }
}
