using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/orders/cancel")]
    public class BulkCancelController : ControllerBase
    {
        private readonly DbConnections _db;

        public BulkCancelController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost]
        public IActionResult Cancel()
        {
            var ids = Request.Query["id"];
            if (ids.Count == 0)
            {
                return BadRequest("no ids");
            }

            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            var placeholders = new List<string>();
            var i = 0;
            foreach (var id in ids)
            {
                var name = "@id" + i;
                placeholders.Add(name);
                cmd.Parameters.AddWithValue(name, id ?? "");
                i++;
            }
            cmd.CommandText = "UPDATE Orders SET Status = 'Cancelled' WHERE Id IN (" + string.Join(",", placeholders) + ")";
            var changed = cmd.ExecuteNonQuery();
            return Ok(new { changed });
        }
    }
}
