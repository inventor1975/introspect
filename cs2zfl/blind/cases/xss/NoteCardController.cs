using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Markup;

namespace Storefront.Web.Controllers
{
    [Route("notes")]
    public class NoteCardController : Controller
    {
        [HttpGet("card")]
        public IActionResult Card(string message)
        {
            var body = HtmlFragments.EncodedParagraph(message);
            return Content(HtmlFragments.Document("Note", body), "text/html");
        }
    }
}
