using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class NewsletterFormController : Controller
    {
        [HttpGet("/newsletter/form")]
        public IActionResult Form(string email)
        {
            var prefill = WebUtility.HtmlEncode(email ?? string.Empty);
            var html = "<form method=\"post\" action=\"/newsletter\">" +
                       "<input type=\"email\" name=\"email\" value=\"" + prefill + "\"/>" +
                       "<button>Subscribe</button></form>";
            return Content(html, "text/html");
        }
    }
}
