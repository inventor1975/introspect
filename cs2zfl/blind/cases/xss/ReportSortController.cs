using System;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ReportSortController : Controller
    {
        private static readonly string[] Columns = { "date", "total", "customer" };

        [HttpGet("/reports/orders")]
        public IActionResult Orders(string sort)
        {
            try
            {
                var column = ResolveColumn(sort);
                return Content($"<p>Sorted by {column}</p>", "text/html");
            }
            catch (ArgumentException ex)
            {
                return Content("<div class=\"error\">" + ex.Message + "</div>", "text/html");
            }
        }

        private static string ResolveColumn(string sort)
        {
            foreach (var c in Columns)
            {
                if (string.Equals(c, sort, StringComparison.OrdinalIgnoreCase)) return c;
            }
            throw new ArgumentException($"Unknown sort column '{sort}'");
        }
    }
}
