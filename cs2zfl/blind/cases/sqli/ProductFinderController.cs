using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("catalog/find")]
    public class ProductFinderController : Controller
    {
        private readonly DbConnections _db;

        public ProductFinderController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Find([FromQuery] string term, [FromQuery] string mode)
        {
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            if (mode == "exact")
            {
                cmd.CommandText = "SELECT Id, Sku, Name FROM Products WHERE Name = @term";
                cmd.Parameters.AddWithValue("@term", term);
            }
            else
            {
                cmd.CommandText = "SELECT Id, Sku, Name FROM Products WHERE Name LIKE N'%" + term + "%'";
            }

            var found = new List<Product>();
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                found.Add(new Product { Id = reader.GetInt32(0), Sku = reader.GetString(1), Name = reader.GetString(2) });
            }
            return View(found);
        }
    }
}
