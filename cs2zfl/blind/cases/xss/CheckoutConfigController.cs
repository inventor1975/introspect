using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace Storefront.Web.Controllers
{
    public class CheckoutConfigController : Controller
    {
        [HttpGet("/checkout/boot")]
        public IActionResult Boot(string coupon, string currency)
        {
            var config = new { coupon, currency, step = 1 };
            var json = JsonConvert.SerializeObject(config);
            var html = "<div id=\"checkout\"></div><script>window.__CHECKOUT__ = " + json + ";</script>";
            return Content(html, "text/html");
        }
    }
}
