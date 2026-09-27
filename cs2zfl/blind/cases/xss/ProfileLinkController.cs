using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ProfileLinkController : Controller
    {
        [HttpGet("/profile/website")]
        public IActionResult Website([FromQuery] string url, [FromQuery] string label)
        {
            var safeLabel = WebUtility.HtmlEncode(label);
            var safeUrl = WebUtility.HtmlEncode(url);
            var html = $"<p>Visit my site: <a href=\"{safeUrl}\" rel=\"nofollow\">{safeLabel}</a></p>";
            return Content(html, "text/html");
        }
    }
}
