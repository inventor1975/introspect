using System.ComponentModel.DataAnnotations;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Logistics.Web.Controllers
{
    public class LabelRequest
    {
        [Required]
        [RegularExpression("^[A-Z]{2}[0-9]{9}[A-Z]{2}$", ErrorMessage = "Invalid tracking number.")]
        public string TrackingNumber { get; set; } = "";

        [Range(1, 4)]
        public int Copies { get; set; } = 1;
    }

    public class ShipmentLabelController : Controller
    {
        private const string LabelDir = "/var/logistics/labels";

        [HttpGet]
        public IActionResult Label([FromQuery] LabelRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var path = Path.Combine(LabelDir, request.TrackingNumber + ".zpl");
            var zpl = System.IO.File.ReadAllText(path);
            return Content(zpl, "application/zpl");
        }
    }
}
