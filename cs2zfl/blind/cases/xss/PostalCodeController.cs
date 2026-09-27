using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class DeliveryCheckInput
    {
        [Required]
        [RegularExpression("^[0-9]{5}$")]
        public string PostalCode { get; set; } = "";
    }

    public class PostalCodeController : Controller
    {
        [HttpGet("/delivery/check")]
        public IActionResult Check([FromQuery] DeliveryCheckInput input)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest("Enter a 5-digit postal code.");
            }
            return Content($"<p>Next-day delivery is available for {input.PostalCode}.</p>", "text/html");
        }
    }
}
