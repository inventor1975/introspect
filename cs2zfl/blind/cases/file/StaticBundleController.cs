using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.FileProviders;

namespace Spa.Host.Controllers
{
    [Route("bundle")]
    public class StaticBundleController : Controller
    {
        private static readonly PhysicalFileProvider Bundles = new PhysicalFileProvider("/srv/spa/dist");

        [HttpGet("{**asset}")]
        public IActionResult Get(string asset)
        {
            var info = Bundles.GetFileInfo(asset);
            if (!info.Exists || info.IsDirectory || info.PhysicalPath == null)
            {
                return NotFound();
            }

            return PhysicalFile(info.PhysicalPath, "application/octet-stream");
        }
    }
}
