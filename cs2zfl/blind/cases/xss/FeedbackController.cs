using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class FeedbackController : Controller
    {
        [HttpPost("/feedback")]
        public IActionResult Submit([FromForm] string comment)
        {
            if (comment == null || comment.Length > 500)
            {
                return BadRequest("Comment must be 1-500 characters.");
            }
            return Content("<h3>Thanks!</h3><blockquote>" + comment + "</blockquote>", "text/html");
        }
    }
}
