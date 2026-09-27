using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("admin/reviews")]
    public class ReviewModerationController : Controller
    {
        private readonly DbConnections _db;

        public ReviewModerationController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost("filter")]
        [ValidateAntiForgeryToken]
        public IActionResult Filter()
        {
            var author = Request.Form["author"].ToString();
            var table = new DataTable("Reviews");
            using (var conn = _db.OpenMain())
            using (var adapter = new SqlDataAdapter("SELECT Id, ProductId, Author, Body, Rating FROM Reviews WHERE Author = '" + author + "' AND Approved = 0", conn))
            {
                adapter.Fill(table);
            }
            return View("Pending", table);
        }
    }
}
