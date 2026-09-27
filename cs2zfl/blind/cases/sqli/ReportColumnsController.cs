using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("reports/customers")]
    public class ReportColumnsController : Controller
    {
        private static readonly HashSet<string> SortableColumns =
            new HashSet<string>(StringComparer.Ordinal) { "Name", "Email", "City", "Id" };

        private readonly DbConnections _db;

        public ReportColumnsController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index([FromQuery] string sortBy = "Name")
        {
            if (!SortableColumns.Contains(sortBy))
            {
                return BadRequest("unsupported sort column");
            }

            var table = new DataTable();
            using var conn = _db.OpenMain();
            using var adapter = new SqlDataAdapter("SELECT Id, Name, Email, City FROM Customers ORDER BY " + sortBy, conn);
            adapter.Fill(table);
            return View(table);
        }
    }
}
