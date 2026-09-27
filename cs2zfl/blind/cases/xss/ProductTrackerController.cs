using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ProductTrackerController : Controller
    {
        [HttpGet("/analytics/view")]
        public IActionResult TrackView(string sku)
        {
            var js = JavaScriptEncoder.Default.Encode(sku ?? string.Empty);
            var html = "<script>\n" +
                       "  window.dataLayer = window.dataLayer || [];\n" +
                       "  window.dataLayer.push({ event: 'view_item', sku: \"" + js + "\" });\n" +
                       "</script>";
            return Content(html, "text/html");
        }
    }
}
