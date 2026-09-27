using System.Data;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Authorize(Roles = "Admin")]
    [Route("admin/export")]
    public class ExportTableController : Controller
    {
        private static readonly Regex Identifier = new Regex(@"^[A-Za-z_][A-Za-z0-9_]{0,63}\z", RegexOptions.CultureInvariant);
        private readonly DbConnections _db;

        public ExportTableController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{table}")]
        public IActionResult Export(string table)
        {
            if (!Identifier.IsMatch(table))
            {
                return BadRequest("invalid table name");
            }

            var data = new DataTable(table);
            using var conn = _db.OpenMain();
            using var adapter = new SqlDataAdapter("SELECT TOP 5000 * FROM [dbo].[" + table + "]", conn);
            adapter.Fill(data);
            return View(data);
        }
    }
}
