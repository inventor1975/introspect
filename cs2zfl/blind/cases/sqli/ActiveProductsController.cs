using System.Collections.Generic;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("products")]
    public class ActiveProductsController : Controller
    {
        private readonly DbConnections _db;

        public ActiveProductsController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index([FromQuery] bool includeRetired, [FromQuery] string? category)
        {
            var condition = includeRetired ? "1 = 1" : "IsActive = 1";
            var sql = "SELECT Id, Sku, Name, Category, Price, IsActive FROM Products WHERE " + condition;
            if (!string.IsNullOrEmpty(category))
            {
                sql += " AND Category = @category";
            }
            using var conn = _db.OpenMain();
            IEnumerable<Product> products = conn.Query<Product>(sql + " ORDER BY Name", new { category });
            return View(products);
        }
    }
}
