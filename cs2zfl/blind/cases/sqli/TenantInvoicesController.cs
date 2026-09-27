using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/tenant/invoices")]
    public class TenantInvoicesController : ControllerBase
    {
        private readonly DbConnections _db;

        public TenantInvoicesController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Recent()
        {
            if (!Request.Cookies.TryGetValue("tenant", out var tenant) || string.IsNullOrEmpty(tenant))
            {
                return Unauthorized();
            }

            var totals = new List<decimal>();
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = $"SELECT TOP 20 Total FROM [{tenant}].Invoices ORDER BY IssuedAt DESC";
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                totals.Add(reader.GetDecimal(0));
            }
            return Ok(totals);
        }
    }
}
