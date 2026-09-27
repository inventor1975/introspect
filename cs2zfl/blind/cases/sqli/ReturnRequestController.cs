using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/returns")]
    public class ReturnRequestController : ControllerBase
    {
        private readonly DbConnections _db;

        public ReturnRequestController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{rma}")]
        public IActionResult Get(string rma)
        {
            Guid parsed;
            try
            {
                parsed = Guid.Parse(rma);
            }
            catch (FormatException)
            {
                return BadRequest("malformed RMA number");
            }

            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "SELECT Status, Reason, CreatedAt FROM Returns WHERE Rma = '" + parsed.ToString("D") + "'";
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return NotFound();
            }
            return Ok(new { status = reader.GetString(0), reason = reader.GetString(1), created = reader.GetDateTime(2) });
        }
    }
}
