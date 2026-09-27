using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class InventoryReportController : Controller
    {
        private readonly DbConnections _db;

        public InventoryReportController(DbConnections db)
        {
            _db = db;
        }

        private static string Escape(string input)
        {
            return input.Replace("'", "''");
        }

        public IActionResult Stock(string category, string orderBy)
        {
            var sql = "SELECT Sku, Name, Price FROM Products WHERE Category = N'" + Escape(category) + "'";
            if (!string.IsNullOrWhiteSpace(orderBy))
            {
                sql += " ORDER BY " + Escape(orderBy);
            }

            var rows = new List<Product>();
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = sql;
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                rows.Add(new Product { Sku = reader.GetString(0), Name = reader.GetString(1), Price = reader.GetDecimal(2) });
            }
            return View(rows);
        }
    }
}
