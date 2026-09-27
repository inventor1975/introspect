using System.Net;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("tracking")]
    public class ShipmentTrackingController : Controller
    {
        private readonly DbConnections _db;

        public ShipmentTrackingController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{shipment}")]
        public IActionResult Show([FromRoute] string shipment)
        {
            var encodedShipment = WebUtility.HtmlEncode(shipment);
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Carrier, TrackingCode, Status FROM Shipments WHERE ShipmentId = " + encodedShipment, conn);
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                ViewBag.Message = "Shipment " + encodedShipment + " was not found.";
                return View("Missing");
            }
            ViewBag.Carrier = reader.GetString(0);
            ViewBag.Code = reader.GetString(1);
            ViewBag.Status = reader.GetString(2);
            return View();
        }
    }
}
