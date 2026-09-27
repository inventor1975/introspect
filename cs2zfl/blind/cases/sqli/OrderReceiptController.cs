using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("receipts")]
    public class OrderReceiptController : Controller
    {
        private readonly DbConnections _db;

        public OrderReceiptController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("view")]
        public IActionResult Receipt()
        {
            var raw = Request.Query["orderId"].ToString();
            if (!int.TryParse(raw, out var orderId))
            {
                return BadRequest("orderId must be numeric");
            }
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Id, CustomerId, PlacedAt, Status, Total FROM Orders WHERE Id = " + orderId, conn);
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return NotFound();
            }
            var order = new Order
            {
                Id = reader.GetInt32(0),
                CustomerId = reader.GetInt32(1),
                PlacedAt = reader.GetDateTime(2),
                Status = reader.GetString(3),
                Total = reader.GetDecimal(4)
            };
            return View(order);
        }
    }
}
