using System;
using System.IO;
using System.IO.Compression;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Forum.Admin.Controllers
{
    [Authorize(Roles = "Admin")]
    [Route("admin/themes")]
    public class ThemePackageController : Controller
    {
        private const string ThemesRoot = "/srv/forum/themes";

        [HttpPost("upload")]
        public IActionResult Upload(IFormFile package)
        {
            var themeId = Guid.NewGuid().ToString("N");
            var destination = Path.GetFullPath(Path.Combine(ThemesRoot, themeId)) + Path.DirectorySeparatorChar;
            Directory.CreateDirectory(destination);

            using var archive = new ZipArchive(package.OpenReadStream(), ZipArchiveMode.Read);
            foreach (var entry in archive.Entries)
            {
                var outPath = Path.GetFullPath(Path.Combine(destination, entry.FullName));
                if (!outPath.StartsWith(destination, StringComparison.Ordinal))
                {
                    return BadRequest($"Entry '{entry.FullName}' escapes the theme folder.");
                }

                if (entry.FullName.EndsWith("/"))
                {
                    Directory.CreateDirectory(outPath);
                    continue;
                }

                Directory.CreateDirectory(Path.GetDirectoryName(outPath)!);
                entry.ExtractToFile(outPath, overwrite: true);
            }

            return RedirectToAction("Index", new { installed = themeId });
        }
    }
}
