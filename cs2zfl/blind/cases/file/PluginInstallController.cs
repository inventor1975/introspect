using System.IO;
using System.IO.Compression;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Cms.Admin.Controllers
{
    [Authorize(Roles = "Admin")]
    [Route("admin/plugins")]
    public class PluginInstallController : Controller
    {
        private const string PluginsDir = "/srv/cms/plugins";

        [HttpPost("install")]
        [RequestSizeLimit(50_000_000)]
        public IActionResult Install(IFormFile package, string pluginName)
        {
            if (package == null || !package.FileName.EndsWith(".zip"))
            {
                return BadRequest("A .zip package is required.");
            }

            var destination = Path.Combine(PluginsDir, Path.GetFileName(pluginName));
            Directory.CreateDirectory(destination);

            using (var archive = new ZipArchive(package.OpenReadStream(), ZipArchiveMode.Read))
            {
                foreach (var entry in archive.Entries)
                {
                    if (string.IsNullOrEmpty(entry.Name))
                    {
                        continue;
                    }

                    var outPath = Path.Combine(destination, entry.FullName);
                    Directory.CreateDirectory(Path.GetDirectoryName(outPath)!);

                    using (var input = entry.Open())
                    using (var output = System.IO.File.Create(outPath))
                    {
                        input.CopyTo(output);
                    }
                }
            }

            return RedirectToAction("Index");
        }
    }
}
