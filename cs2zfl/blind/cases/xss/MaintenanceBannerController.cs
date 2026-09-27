using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace Storefront.Web.Controllers
{
    public class MaintenanceBannerController : Controller
    {
        private readonly IConfiguration _config;

        public MaintenanceBannerController(IConfiguration config)
        {
            _config = config;
        }

        [HttpGet("/banner/maintenance")]
        public IActionResult Banner()
        {
            var text = _config["Storefront:MaintenanceBannerHtml"] ?? "";
            return Content("<div class=\"maintenance\">" + text + "</div>", "text/html");
        }
    }
}
