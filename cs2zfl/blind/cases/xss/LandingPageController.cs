using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Markup;

namespace Storefront.Web.Controllers
{
    public class LandingPageController : Controller
    {
        [HttpGet("/promo")]
        public IActionResult Promo(string headline, string blurb)
        {
            var page = new PageBuilder()
                .Title("Seasonal promo")
                .Section(headline, blurb)
                .Build();
            return Content(page, "text/html");
        }
    }
}
