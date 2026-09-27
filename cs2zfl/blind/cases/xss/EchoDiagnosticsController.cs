using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    [Route("diag")]
    public class EchoDiagnosticsController : Controller
    {
        [HttpGet("echo")]
        public IActionResult Echo([FromQuery] string payload)
        {
            Response.Headers["X-Content-Type-Options"] = "nosniff";
            return Content("received: " + payload, "text/plain");
        }
    }
}
