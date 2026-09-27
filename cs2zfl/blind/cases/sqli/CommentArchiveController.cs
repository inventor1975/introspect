using System.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("admin/comments")]
    public class CommentArchiveController : Controller
    {
        private readonly DbConnections _db;

        public CommentArchiveController(DbConnections db)
        {
            _db = db;
        }

        private static string QuoteUnicode(string value)
        {
            return "N'" + value.Replace("'", "''") + "'";
        }

        [HttpGet("archive")]
        public IActionResult Archive(string author)
        {
            if (string.IsNullOrEmpty(author) || author.Length > 100)
            {
                return BadRequest();
            }
            var sql = "SELECT Id, Author, Body, PostedAt FROM CommentArchive WHERE Author = " + QuoteUnicode(author)
                      + " ORDER BY PostedAt DESC";
            var table = new DataTable();
            using (var conn = _db.OpenMain())
            using (var adapter = new SqlDataAdapter(sql, conn))
            {
                adapter.Fill(table);
            }
            return View(table);
        }
    }
}
