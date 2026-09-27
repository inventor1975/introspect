using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/contacts")]
    public class CustomerContactController : ControllerBase
    {
        private readonly DbConnections _db;

        public CustomerContactController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("by-email")]
        public ActionResult<Customer> ByEmail([FromQuery] string email, [FromQuery] string? city)
        {
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            var where = SqlFragments.BindEquals(cmd, "Email", email);
            if (!string.IsNullOrEmpty(city))
            {
                where += " AND " + SqlFragments.BindEquals(cmd, "City", city);
            }
            cmd.CommandText = "SELECT TOP 1 Id, Name, Email, City FROM Customers WHERE " + where;
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return NotFound();
            }
            return new Customer
            {
                Id = reader.GetInt32(0),
                Name = reader.GetString(1),
                Email = reader.GetString(2),
                City = reader.GetString(3)
            };
        }
    }
}
