using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class AuthorBioController : Controller
    {
        [HttpGet("/authors/preview")]
        public IActionResult Preview([FromQuery] string bio, [FromQuery] string name)
        {
            ViewData["AuthorName"] = name;
            ViewData["AuthorBio"] = new HtmlString(bio);
            return View("AuthorPreview");
        }
    }
}
