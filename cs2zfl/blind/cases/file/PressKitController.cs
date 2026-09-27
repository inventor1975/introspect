using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Corporate.Site.Controllers
{
    [Route("press")]
    public class PressKitController : Controller
    {
        private const string KitDir = "/app/presskit";

        private static readonly Dictionary<string, string> ContentTypes = new Dictionary<string, string>
        {
            [".png"] = "image/png",
            [".jpg"] = "image/jpeg",
            [".pdf"] = "application/pdf",
        };

        [HttpGet("asset/{assetNo:int}")]
        public IActionResult Asset(int assetNo, [FromQuery] string requestedAs)
        {
            var ext = Path.GetExtension(requestedAs ?? string.Empty).ToLowerInvariant();
            if (!ContentTypes.TryGetValue(ext, out var contentType))
            {
                ext = ".pdf";
                contentType = "application/pdf";
            }

            var path = Path.Combine(KitDir, "asset-" + assetNo.ToString("D4") + ext);
            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, contentType);
        }
    }
}
