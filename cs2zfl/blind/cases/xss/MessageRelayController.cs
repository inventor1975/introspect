using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class MessageRelayController : Controller
    {
        [HttpGet("/relay/message")]
        public IActionResult Show(string text)
        {
            var stored = WebUtility.HtmlEncode(text);
            var display = WebUtility.HtmlDecode(stored);
            return Content("<div class=\"relay\">" + display + "</div>", "text/html");
        }
    }
}
