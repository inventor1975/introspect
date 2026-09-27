using System.Web;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ChartEmbedController : Controller
    {
        [HttpGet("/embed/chart")]
        public IActionResult Chart([FromQuery(Name = "series")] string seriesId)
        {
            var id = HttpUtility.HtmlEncode(seriesId);
            var page = "<div id=\"chart\"></div>\n" +
                       "<script>\n" +
                       "  var seriesId = " + id + ";\n" +
                       "  renderChart(document.getElementById('chart'), seriesId);\n" +
                       "</script>";
            return Content(page, "text/html");
        }
    }
}
