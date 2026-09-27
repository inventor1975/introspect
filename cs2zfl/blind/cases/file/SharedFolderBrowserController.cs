using System.IO;
using System.Linq;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Intranet.Web.Controllers
{
    [Authorize(Roles = "Staff")]
    public class SharedFolderBrowserController : Controller
    {
        private const string ShareRoot = @"D:\Shares\Public";

        public IActionResult Index(string folder = "")
        {
            var current = Path.Combine(ShareRoot, folder ?? string.Empty);

            if (!Directory.Exists(current))
            {
                return NotFound();
            }

            var entries = Directory.GetFiles(current)
                .Select(p => new FileInfo(p))
                .OrderBy(f => f.Name)
                .Select(f => new { f.Name, f.Length, f.LastWriteTimeUtc })
                .ToList();

            ViewBag.Folder = folder;
            return View(entries);
        }
    }
}
