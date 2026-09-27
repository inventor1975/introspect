using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class ProductSortController : Controller
    {
        private readonly DbConnections _db;

        public ProductSortController(DbConnections db)
        {
            _db = db;
        }

        public IActionResult List(string category, string sort)
        {
            string orderBy;
            switch (sort)
            {
                case "price":
                    orderBy = "Price";
                    break;
                case "price_desc":
                    orderBy = "Price DESC";
                    break;
                case "newest":
                    orderBy = "Id DESC";
                    break;
                default:
                    orderBy = "Name";
                    break;
            }

            var sql = "SELECT Sku, Name, Price FROM Products WHERE Category = @category ORDER BY " + orderBy;
            var rows = new List<Product>();
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = sql;
            cmd.Parameters.AddWithValue("@category", category ?? "");
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                rows.Add(new Product { Sku = reader.GetString(0), Name = reader.GetString(1), Price = reader.GetDecimal(2) });
            }
            return View(rows);
        }
    }
}
