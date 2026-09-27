using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Records.Web.Controllers
{
    public class ArchiveBrowserController : Controller
    {
        private const string LiveDir = "/srv/records/live";
        private const string ArchiveDir = "/srv/records/archive";

        [HttpGet]
        public IActionResult Open(string name, string scope)
        {
            var baseDir = scope == "archive" ? ArchiveDir : LiveDir;
            var fullPath = Path.Combine(baseDir, name);

            using var reader = new StreamReader(System.IO.File.OpenRead(fullPath));
            var body = reader.ReadToEnd();

            ViewBag.Name = name;
            return View("Record", body);
        }
    }
}
