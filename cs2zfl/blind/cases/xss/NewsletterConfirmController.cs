using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class NewsletterConfirmController : Controller
    {
        [HttpGet("/newsletter/confirm")]
        public IActionResult Confirm(string email, bool strict = false)
        {
            string shown = email;
            if (strict)
            {
                shown = WebUtility.HtmlEncode(email);
            }
            return Content($"<p>A confirmation link was sent to <b>{shown}</b>.</p>", "text/html");
        }
    }
}
