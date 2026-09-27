using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Markup;

namespace Storefront.Web.Controllers
{
    [Route("notices")]
    public class NoticeController : Controller
    {
        [HttpGet("preview")]
        public IActionResult Preview(string message)
        {
            var body = HtmlFragments.Paragraph(message);
            return Content(HtmlFragments.Document("Notice", body), "text/html");
        }
    }
}
