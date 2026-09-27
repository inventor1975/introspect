using System.IO;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace ProductSite.Controllers
{
    public class ChangelogController : Controller
    {
        private readonly ILogger<ChangelogController> _logger;
        private const string ReleaseNotesDir = "/app/content/release-notes";

        public ChangelogController(ILogger<ChangelogController> logger)
        {
            _logger = logger;
        }

        [HttpGet("changelog/{version}")]
        public IActionResult Show(string version)
        {
            string markdown;
            try
            {
                markdown = System.IO.File.ReadAllText(Path.Combine(ReleaseNotesDir, version + ".md"));
            }
            catch (FileNotFoundException)
            {
                _logger.LogWarning("Release notes for {Version} not found", version);
                return NotFound();
            }
            catch (DirectoryNotFoundException)
            {
                return NotFound();
            }

            ViewData["Version"] = version;
            return View("Show", markdown);
        }
    }
}
