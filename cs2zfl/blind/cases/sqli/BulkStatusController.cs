using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/orders/status")]
    public class BulkStatusController : ControllerBase
    {
        private readonly DbConnections _db;

        public BulkStatusController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost("ship")]
        public IActionResult MarkShipped()
        {
            var ids = Request.Query["id"];
            if (ids.Count == 0)
            {
                return BadRequest("no ids");
            }

            var list = new StringBuilder();
            foreach (var id in ids)
            {
                if (list.Length > 0)
                {
                    list.Append(',');
                }
                list.Append('\'').Append(id).Append('\'');
            }

            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "UPDATE Orders SET Status = 'Shipped' WHERE Id IN (" + list + ")";
            var changed = cmd.ExecuteNonQuery();
            return Ok(new { changed });
        }
    }
}
