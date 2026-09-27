using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("account/orders")]
    public class PagedOrdersController : Controller
    {
        private readonly DbConnections _db;

        public PagedOrdersController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index(int customerId)
        {
            int.TryParse(Request.Query["page"], out var page);
            int.TryParse(Request.Query["size"], out var size);
            page = Math.Max(page, 1);
            size = Math.Clamp(size, 10, 100);
            var offset = (page - 1) * size;

            var orders = new List<Order>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(
                $"SELECT Id, PlacedAt, Status, Total FROM Orders WHERE CustomerId = @cid ORDER BY PlacedAt DESC OFFSET {offset} ROWS FETCH NEXT {size} ROWS ONLY", conn);
            cmd.Parameters.AddWithValue("@cid", customerId);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                orders.Add(new Order { Id = reader.GetInt32(0), PlacedAt = reader.GetDateTime(1), Status = reader.GetString(2), Total = reader.GetDecimal(3) });
            }
            return View(orders);
        }
    }
}
