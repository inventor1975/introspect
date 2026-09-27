using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/registry")]
    public class GiftRegistryController : ControllerBase
    {
        private readonly DbConnections _db;

        public GiftRegistryController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{owner}")]
        public IActionResult ForOwner(string owner, [FromQuery] string? list)
        {
            SqlCommand Build(SqlConnection c, string who, string? name)
            {
                var command = new SqlCommand("SELECT ProductId FROM RegistryItems WHERE Owner = @owner"
                                             + (string.IsNullOrEmpty(name) ? "" : " AND ListName = @list"), c);
                command.Parameters.AddWithValue("@owner", who);
                if (!string.IsNullOrEmpty(name))
                {
                    command.Parameters.AddWithValue("@list", name);
                }
                return command;
            }

            var ids = new List<int>();
            using var conn = _db.OpenMain();
            using var cmd = Build(conn, owner, list);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                ids.Add(reader.GetInt32(0));
            }
            return Ok(ids);
        }
    }
}
