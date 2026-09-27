using System.Threading.Tasks;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/loyalty")]
    public class LoyaltyPointsController : ControllerBase
    {
        private readonly DbConnections _db;

        public LoyaltyPointsController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("points")]
        public async Task<IActionResult> Points()
        {
            string member = Request.Headers["X-Member-Code"];
            if (string.IsNullOrEmpty(member))
            {
                return Unauthorized();
            }
            using var conn = _db.OpenMain();
            var points = await conn.QueryFirstOrDefaultAsync<int?>(
                string.Concat("SELECT Points FROM LoyaltyMembers WHERE MemberCode = '", member, "'"));
            return points.HasValue ? Ok(new { points }) : NotFound();
        }
    }
}
