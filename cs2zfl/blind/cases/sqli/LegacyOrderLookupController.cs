using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("orders/lookup")]
    public class LegacyOrderLookupController : Controller
    {
        private readonly DbConnections _db;
        private readonly ILogger<LegacyOrderLookupController> _log;

        public LegacyOrderLookupController(DbConnections db, ILogger<LegacyOrderLookupController> log)
        {
            _db = db;
            _log = log;
        }

        [HttpGet]
        public IActionResult Find(string reference)
        {
            using var conn = _db.OpenMain();
            SqlCommand cmd;
            try
            {
                var id = int.Parse(reference);
                cmd = new SqlCommand("SELECT Id, Status, Total FROM Orders WHERE Id = @id", conn);
                cmd.Parameters.AddWithValue("@id", id);
            }
            catch (FormatException)
            {
                _log.LogInformation("Non-numeric reference, falling back to legacy code lookup");
                cmd = new SqlCommand("SELECT Id, Status, Total FROM Orders WHERE LegacyCode = '" + reference + "'", conn);
            }

            using (cmd)
            using (var reader = cmd.ExecuteReader())
            {
                if (!reader.Read())
                {
                    return NotFound();
                }
                return Json(new { id = reader.GetInt32(0), status = reader.GetString(1), total = reader.GetDecimal(2) });
            }
        }
    }
}
