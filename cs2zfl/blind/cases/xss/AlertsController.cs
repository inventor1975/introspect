using Microsoft.AspNetCore.Mvc;
using Storefront.Web.Markup;

namespace Storefront.Web.Controllers
{
    public class AlertsController : Controller
    {
        private readonly IMarkupRenderer _renderer;

        public AlertsController(IMarkupRenderer renderer)
        {
            _renderer = renderer;
        }

        [HttpGet("/alerts/flash")]
        public IActionResult Flash(string msg)
        {
            var fragment = _renderer.RenderMessage(msg);
            return Content(fragment, "text/html");
        }
    }
}
