using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("invoices")]
    public class InvoiceDetailController : Controller
    {
        private readonly DbConnections _db;

        public InvoiceDetailController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("detail")]
        public IActionResult Detail()
        {
            var raw = Request.Query["invoiceId"].ToString();
            var cleaned = raw.Replace("'", "''").Trim();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Id, CustomerId, PlacedAt, Status, Total FROM Orders WHERE Id = " + cleaned, conn);
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
