using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class OrderListController : Controller
    {
        private static readonly HashSet<string> SortableColumns = new HashSet<string> { "date", "total", "status" };

        [HttpGet("/orders")]
        public IActionResult Index(string sort)
        {
            var column = "date";
            if (SortableColumns.Contains(sort))
            {
                column = sort;
            }
            return Content("<table data-sort=\"" + column + "\"><caption>Orders sorted by " + column + "</caption></table>", "text/html");
        }
    }
}
