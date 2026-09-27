using System.Linq;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/customers/search")]
    public class CustomerSearchController : ControllerBase
    {
        private readonly DbConnections _db;

        public CustomerSearchController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Search([FromQuery] string name, [FromQuery] int page = 1)
        {
            if (page < 1)
            {
                page = 1;
            }
            using var conn = _db.OpenMain();
            var sql = "SELECT Id, Name, Email, City FROM Customers WHERE Name LIKE @pattern ORDER BY Name OFFSET "
                      + ((page - 1) * 25) + " ROWS FETCH NEXT 25 ROWS ONLY";
            var rows = conn.Query<Customer>(sql, new { pattern = "%" + name + "%" }).ToList();
            return Ok(rows);
        }
    }
}
