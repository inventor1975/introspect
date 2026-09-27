using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("reports/sales")]
    public class SalesReportController : Controller
    {
        private readonly DbConnections _db;

        public SalesReportController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index(string status, string customer, int? minTotal)
        {
            var filter = new ReportFilter
            {
                Status = status ?? "",
                CustomerName = customer ?? "",
                MinTotal = minTotal
            };

            var sql = "SELECT o.Id, c.Name, o.Status, o.Total FROM Orders o JOIN Customers c ON c.Id = o.CustomerId"
                      + filter.ToWhereClause();

            var table = new DataTable();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(sql, conn);
            using var adapter = new SqlDataAdapter(cmd);
            adapter.Fill(table);
            return View(table);
        }
    }
}
