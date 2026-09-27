using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Validation;

namespace Storefront.Web.Controllers
{
    public class ReviewPreviewController : Controller
    {
        [HttpPost("/reviews/preview")]
        public IActionResult Preview()
        {
            string text = Request.Form["review"];
            var cleaned = InputRules.StripScriptTags(text);
            return Content($"<div class=\"review-preview\">{cleaned}</div>", "text/html");
        }
    }
}
