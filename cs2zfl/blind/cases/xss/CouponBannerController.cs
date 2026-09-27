using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Validation;

namespace Storefront.Web.Controllers
{
    public class CouponBannerController : Controller
    {
        [HttpGet("/coupons/banner")]
        public IActionResult Banner([FromQuery] string code)
        {
            InputRules.IsSlug(code);
            var label = InputRules.Truncate(code, 64);
            return Content("<div class=\"coupon\">Use code <kbd>" + label + "</kbd> at checkout</div>", "text/html");
        }
    }
}
