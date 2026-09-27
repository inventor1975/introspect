using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Configuration;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("dashboard")]
    public class DashboardViewController : Controller
    {
        private readonly DbConnections _db;
        private readonly IConfiguration _config;

        public DashboardViewController(DbConnections db, IConfiguration config)
        {
            _db = db;
            _config = config;
        }

        [HttpGet("{storeId:int}")]
        public IActionResult Store(int storeId, [FromQuery] string period)
        {
            var viewName = _config["Reporting:DashboardView"] ?? "vw_StoreDashboard";
            var sql = "SELECT Metric, Value FROM " + viewName + " WHERE StoreId = @store AND Period = @period";
            var table = new DataTable();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@store", storeId);
            cmd.Parameters.AddWithValue("@period", period ?? "month");
            using var adapter = new SqlDataAdapter(cmd);
            adapter.Fill(table);
            return View(table);
        }
    }
}
