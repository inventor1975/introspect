using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class AccountHeaderController : Controller
    {
        [HttpGet("/account/header")]
        public IActionResult Header()
        {
            string display = Request.Query["display"];
            string who;
            if (string.IsNullOrWhiteSpace(display))
            {
                who = "Guest";
            }
            else
            {
                who = display.Trim();
            }
            return Content($"<nav><span class=\"user\">Signed in as {who}</span></nav>", "text/html");
        }
    }
}
