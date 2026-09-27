using System;
using Microsoft.AspNetCore.Mvc;
using Shared.Storage;

namespace Gallery.Api.Controllers
{
    [ApiController]
    [Route("api/thumbnails")]
    public class ThumbnailController : ControllerBase
    {
        private readonly ThumbnailCache _cache = new ThumbnailCache("/var/cache/gallery/thumbs");

        [HttpGet("{imageId:guid}")]
        public IActionResult Get(Guid imageId, [FromQuery] int w = 256, [FromQuery] int h = 256)
        {
            if (w <= 0 || h <= 0 || w > 2048 || h > 2048)
            {
                return BadRequest();
            }

            var path = _cache.PathFor(imageId, w, h);
            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "image/webp");
        }
    }
}
