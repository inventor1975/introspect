using System.Linq;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class UsernamePreviewController : Controller
    {
        [HttpGet("/account/username/preview")]
        public IActionResult Preview(string desired)
        {
            var handle = new string((desired ?? string.Empty).Where(char.IsLetterOrDigit).Take(24).ToArray());
            return Content($"<p>Your profile will be at <b>/u/{handle}</b></p>", "text/html");
        }
    }
}
