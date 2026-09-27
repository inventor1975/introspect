using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Authorize(Roles = "Admin")]
    [Route("api/admin/stats")]
    public class TableStatsController : ControllerBase
    {
        private readonly DbConnections _db;

        public TableStatsController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{table}/count")]
        public IActionResult RowCount(string table)
        {
            using var builder = new SqlCommandBuilder();
            var quoted = builder.QuoteIdentifier(table);
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT COUNT_BIG(*) FROM dbo." + quoted, conn);
            var count = (long)cmd.ExecuteScalar();
            return Ok(new { table, count });
        }
    }
}
