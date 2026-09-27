using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class SearchController : Controller
    {
        [HttpGet("/search")]
        public IActionResult Index([FromQuery] string q)
        {
            var html = "<div class=\"results\"><p>No products matched <strong>" + q + "</strong>.</p></div>";
            return Content(html, "text/html");
        }
    }
}
