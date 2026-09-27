using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class NicknameController : Controller
    {
        [HttpPost("/me/nickname")]
        public IActionResult Save([FromForm] string nickname)
        {
            HttpContext.Session.SetString("nick", nickname ?? string.Empty);
            return RedirectToAction(nameof(Card));
        }

        [HttpGet("/me/card")]
        public IActionResult Card()
        {
            var nick = HttpContext.Session.GetString("nick") ?? "friend";
            return Content($"<div class=\"member-card\">Hi {nick}!</div>", "text/html");
        }
    }
}
