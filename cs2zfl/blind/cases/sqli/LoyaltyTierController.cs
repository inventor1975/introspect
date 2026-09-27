using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/loyalty/tier")]
    public class LoyaltyTierController : ControllerBase
    {
        private readonly DbConnections _db;

        public LoyaltyTierController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Tier()
        {
            string member = Request.Headers["X-Member-Code"];
            if (string.IsNullOrEmpty(member))
            {
                return Unauthorized();
            }

            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandType = CommandType.StoredProcedure;
            cmd.CommandText = "loyalty.usp_GetMemberTier";
            cmd.Parameters.Add(new SqlParameter("@MemberCode", SqlDbType.NVarChar, 32) { Value = member });
            var tier = cmd.ExecuteScalar() as string;
            return tier == null ? NotFound() : Ok(new { tier });
        }
    }
}
