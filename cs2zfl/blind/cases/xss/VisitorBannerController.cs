using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class VisitorBannerController : Controller
    {
        [HttpGet("/banner/visitor")]
        public IActionResult Show(string name, bool remember)
        {
            string who = name;
            if (remember)
            {
                who = "returning shopper";
            }
            else
            {
                who = "new visitor";
            }
            return Content($"<div class=\"banner\">Hello, {who}!</div>", "text/html");
        }
    }
}
