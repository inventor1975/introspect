using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace Storefront.Web.Controllers
{
    public class QuickSearchController : Controller
    {
        private readonly ILogger<QuickSearchController> _logger;

        public QuickSearchController(ILogger<QuickSearchController> logger)
        {
            _logger = logger;
        }

        [HttpPost("/search/quick")]
        public IActionResult Quick([FromForm] string term)
        {
            _logger.LogInformation("Quick search for {Term}", term);
            var html = "<p>We are preparing results for your search.</p>";
            return Content(html, "text/html");
        }
    }
}
