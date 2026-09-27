using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("admin/orders")]
    public class ArchivedOrdersController : Controller
    {
        private readonly DbConnections _db;

        public ArchivedOrdersController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index()
        {
            string flag = Request.Query["archived"];
            bool.TryParse(flag, out var archived);
            var sql = "SELECT Id, CustomerId, Status, Total FROM Orders WHERE IsArchived = " + (archived ? 1 : 0)
                      + " ORDER BY Id DESC";
            var table = new DataTable();
            using var conn = _db.OpenMain();
            using var adapter = new SqlDataAdapter(new SqlCommand(sql, conn));
            adapter.Fill(table);
            ViewBag.Archived = archived;
            return View(table);
        }
    }
}
