using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("orders/status")]
    public class OrderStatusController : Controller
    {
        private readonly DbConnections _db;

        public OrderStatusController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index()
        {
            string status = Request.Query["status"];
            var results = new List<Order>();
            using (var conn = _db.OpenMain())
            {
                var cmd = new SqlCommand("SELECT Id, CustomerId, PlacedAt, Status, Total FROM Orders WHERE Status = @status ORDER BY PlacedAt DESC", conn);
                cmd.Parameters.AddWithValue("@status", status ?? "");
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        results.Add(new Order
                        {
                            Id = reader.GetInt32(0),
                            CustomerId = reader.GetInt32(1),
                            PlacedAt = reader.GetDateTime(2),
                            Status = reader.GetString(3),
                            Total = reader.GetDecimal(4)
                        });
                    }
                }
            }
            return View(results);
        }
    }
}
