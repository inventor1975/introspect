using System;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ExportFormatController : Controller
    {
        [HttpGet("/export/start")]
        public IActionResult Start(string format)
        {
            try
            {
                var ext = Normalize(format);
                return Content($"<p>Export queued as .{ext}</p>", "text/html");
            }
            catch (NotSupportedException ex)
            {
                return Content("<div class=\"error\">" + ex.Message + "</div>", "text/html");
            }
        }

        private static string Normalize(string format)
        {
            switch ((format ?? "").ToLowerInvariant())
            {
                case "csv": return "csv";
                case "xlsx": return "xlsx";
                case "pdf": return "pdf";
                default: throw new NotSupportedException("That export format is not supported.");
            }
        }
    }
}
