using System.Collections.Generic;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/audit/search")]
    public class AuditedSearchController : ControllerBase
    {
        private readonly DbConnections _db;
        private readonly ILogger<AuditedSearchController> _log;

        public AuditedSearchController(DbConnections db, ILogger<AuditedSearchController> log)
        {
            _db = db;
            _log = log;
        }

        [HttpGet]
        public IActionResult Search([FromQuery] string actor, [FromQuery] string action)
        {
            var trace = new StringBuilder();
            trace.Append("audit search actor='").Append(actor).Append("' action='").Append(action).Append('\'');
            _log.LogInformation(trace.ToString());

            const string sql = "SELECT TOP 200 Id, Actor, Action, At FROM AuditLog WHERE Actor = @actor AND Action = @action ORDER BY At DESC";
            var rows = new List<object>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@actor", actor);
            cmd.Parameters.AddWithValue("@action", action);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                rows.Add(new { id = reader.GetInt64(0), actor = reader.GetString(1), action = reader.GetString(2), at = reader.GetDateTime(3) });
            }
            return Ok(rows);
        }
    }
}
