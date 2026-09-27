using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Support.Web.Controllers
{
    public class HelpTopicsController : Controller
    {
        private const string TopicsDir = "/app/help";

        private static readonly IReadOnlyDictionary<string, string> TopicFiles = new Dictionary<string, string>
        {
            ["getting-started"] = "01-getting-started.html",
            ["billing"] = "02-billing.html",
            ["security"] = "03-security.html",
            ["api"] = "04-api.html",
        };

        public IActionResult Topic(string id)
        {
            if (id == null || !TopicFiles.TryGetValue(id, out var fileName))
            {
                return NotFound();
            }

            var html = System.IO.File.ReadAllText(Path.Combine(TopicsDir, fileName));
            return Content(html, "text/html");
        }
    }
}
