using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class BackLinkController : Controller
    {
        [HttpGet("/help/contact")]
        public IActionResult Contact()
        {
            string returnUrl = Request.Query["returnUrl"];
            if (string.IsNullOrEmpty(returnUrl))
            {
                returnUrl = "/";
            }
            var html = "<p>Our support team answers within 24 hours.</p>" +
                       "<p><a href='" + returnUrl + "'>Go back</a></p>";
            return Content(html, "text/html");
        }
    }
}
