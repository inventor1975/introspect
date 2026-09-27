using System;
using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ExternalLinkController : Controller
    {
        [HttpGet("/out")]
        public IActionResult Interstitial([FromQuery] string target)
        {
            if (!Uri.TryCreate(target, UriKind.Absolute, out var uri) ||
                (uri.Scheme != Uri.UriSchemeHttps && uri.Scheme != Uri.UriSchemeHttp))
            {
                return BadRequest();
            }
            var href = WebUtility.HtmlEncode(uri.AbsoluteUri);
            return Content($"<p>You are leaving the store.</p><a href=\"{href}\" rel=\"noopener\">Continue</a>", "text/html");
        }
    }
}
