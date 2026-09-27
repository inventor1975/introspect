using System.Linq;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/products/batch")]
    public class OrderBatchController : ControllerBase
    {
        private readonly DbConnections _db;

        public OrderBatchController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Get([FromQuery(Name = "sku")] string[] skus)
        {
            if (skus == null || skus.Length == 0 || skus.Length > 200)
            {
                return BadRequest();
            }
            using var conn = _db.OpenMain();
            var products = conn.Query<Product>(
                "SELECT Id, Sku, Name, Category, Price, IsActive FROM Products WHERE Sku IN @skus",
                new { skus }).ToList();
            return Ok(products);
        }
    }
}
