using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.Sqlite;
using Microsoft.Extensions.Configuration;

namespace Storefront.Web.Controllers
{
    [Route("blog")]
    public class BlogPostController : Controller
    {
        private readonly string _connectionString;

        public BlogPostController(IConfiguration config)
        {
            _connectionString = config.GetConnectionString("Blog") ?? "Data Source=blog.db";
        }

        [HttpGet("{slug}")]
        public IActionResult Post(string slug)
        {
            using var conn = new SqliteConnection(_connectionString);
            conn.Open();
            var slugLower = slug.ToLowerInvariant();
            using var cmd = new SqliteCommand("SELECT title, body, published_at FROM posts WHERE slug = '" + slugLower + "'", conn);
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return NotFound();
            }
            ViewBag.Title = reader.GetString(0);
            ViewBag.Body = reader.GetString(1);
            ViewBag.Published = reader.GetDateTime(2);
            return View();
        }
    }
}
