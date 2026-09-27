using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/accounts")]
    public class AccountLookupController : ControllerBase
    {
        private readonly DbConnections _db;

        public AccountLookupController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("by-email")]
        public ActionResult<Customer> ByEmail([FromQuery] string email)
        {
            var sql = "SELECT TOP 1 Id, Name, Email, City FROM Customers" + SqlFragments.WhereEquals("Email", email);
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(sql, conn);
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
