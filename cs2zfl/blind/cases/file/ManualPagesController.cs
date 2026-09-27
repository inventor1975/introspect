using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Docs.Portal.Controllers
{
    public class ManualPagesController : Controller
    {
        private const string ManualRoot = "/opt/docs-portal/manual";

        private static string StripTraversal(string input)
        {
            return input.Replace("../", string.Empty).Replace("..\\", string.Empty);
        }

        [HttpGet("manual/page")]
        public IActionResult Page(string topic)
        {
            if (string.IsNullOrEmpty(topic))
            {
                return RedirectToAction(nameof(Page), new { topic = "index.html" });
            }

            var cleaned = StripTraversal(topic);
            var html = System.IO.File.ReadAllText(Path.Combine(ManualRoot, cleaned));
            return Content(html, "text/html");
        }
    }
}
