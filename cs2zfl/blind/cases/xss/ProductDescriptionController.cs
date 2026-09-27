using Ganss.Xss;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ProductDescriptionController : Controller
    {
        private static readonly HtmlSanitizer Sanitizer = new HtmlSanitizer();

        [HttpPost("/seller/description/preview")]
        public IActionResult Preview([FromForm] string descriptionHtml)
        {
            var clean = Sanitizer.Sanitize(descriptionHtml ?? string.Empty);
            return Content("<section class=\"description\">" + clean + "</section>", "text/html");
        }
    }
}
