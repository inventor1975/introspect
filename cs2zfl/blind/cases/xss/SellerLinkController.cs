using System.IO;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace Storefront.Web.Controllers
{
    public class SellerLinkController : Controller
    {
        [HttpGet("/sellers/link")]
        public IActionResult Link([FromQuery] string shop, [FromQuery] string tagline)
        {
            var anchor = new TagBuilder("a");
            anchor.MergeAttribute("href", "/sellers/" + System.Uri.EscapeDataString(shop ?? ""));
            anchor.MergeAttribute("title", tagline);
            anchor.InnerHtml.Append(shop);

            using var sw = new StringWriter();
            anchor.WriteTo(sw, HtmlEncoder.Default);
            return Content("<p>Sold by " + sw + "</p>", "text/html");
        }
    }
}
