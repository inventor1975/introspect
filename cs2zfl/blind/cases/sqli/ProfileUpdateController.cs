using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class ProfileUpdateRequest
    {
        public int CustomerId { get; set; }
        public string Email { get; set; } = "";
        public string City { get; set; } = "";
    }

    [ApiController]
    [Authorize]
    [Route("api/profile")]
    public class ProfileUpdateController : ControllerBase
    {
        private readonly DbConnections _db;

        public ProfileUpdateController(DbConnections db)
        {
            _db = db;
        }

        [HttpPut]
        public IActionResult Update([FromBody] ProfileUpdateRequest request)
        {
            if (request.CustomerId <= 0)
            {
                return BadRequest();
            }

            var text = "UPDATE Customers SET Email = '" + request.Email + "', City = '" + request.City
                       + "' WHERE Id = " + request.CustomerId;
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(text, conn);
            var n = cmd.ExecuteNonQuery();
            return n == 1 ? NoContent() : NotFound();
        }
    }
}
