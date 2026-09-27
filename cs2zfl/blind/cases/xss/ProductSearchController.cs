using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ProductSearchController : Controller
    {
        private readonly HtmlEncoder _encoder;

        public ProductSearchController(HtmlEncoder encoder)
        {
            _encoder = encoder;
        }

        [HttpGet("/products/search")]
        public IActionResult Search([FromQuery] string q)
        {
            var html = "<div class=\"results\"><p>No products matched <strong>" + _encoder.Encode(q) + "</strong>.</p></div>";
            return Content(html, "text/html");
        }
    }
}
