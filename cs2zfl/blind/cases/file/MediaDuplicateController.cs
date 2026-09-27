using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Newsroom.Api.Controllers
{
    public class DuplicateMediaRequest
    {
        public string Source { get; set; } = "";
        public string Target { get; set; } = "";
    }

    [ApiController]
    [Route("api/media")]
    public class MediaDuplicateController : ControllerBase
    {
        private const string MediaRoot = "/srv/newsroom/media";

        [HttpPost("duplicate")]
        public IActionResult Duplicate([FromBody] DuplicateMediaRequest body)
        {
            var from = Path.Combine(MediaRoot, body.Source);
            var to = Path.Combine(MediaRoot, "copies", body.Target);

            System.IO.File.Copy(from, to, overwrite: false);
            return Ok(new { copied = body.Target });
        }
    }
}
