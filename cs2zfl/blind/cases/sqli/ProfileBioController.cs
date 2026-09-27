using System.Threading.Tasks;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/users/{id:int}/bio")]
    public class ProfileBioController : ControllerBase
    {
        private readonly DbConnections _db;

        public ProfileBioController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost]
        public async Task<IActionResult> Save(int id, [FromForm] string bio)
        {
            if (bio.Length > 2000)
            {
                return BadRequest("bio too long");
            }
            await using var conn = _db.OpenMain();
            await conn.ExecuteAsync($"UPDATE Users SET Bio = N'{bio}', UpdatedAt = SYSUTCDATETIME() WHERE Id = @id", new { id });
            return NoContent();
        }
    }
}
