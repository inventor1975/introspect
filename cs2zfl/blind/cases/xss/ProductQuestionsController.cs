using System.Linq;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Storefront.Web.Controllers
{
    public class ProductQuestion
    {
        public int Id { get; set; }
        public int ProductId { get; set; }
        public string Asker { get; set; } = "";
        public string Body { get; set; } = "";
    }

    public class CatalogDbContext : DbContext
    {
        public CatalogDbContext(DbContextOptions<CatalogDbContext> options) : base(options) { }
        public DbSet<ProductQuestion> Questions => Set<ProductQuestion>();
    }

    public class ProductQuestionsController : Controller
    {
        private readonly CatalogDbContext _db;

        public ProductQuestionsController(CatalogDbContext db)
        {
            _db = db;
        }

        [HttpPost("/products/{productId:int}/questions")]
        public IActionResult Ask(int productId, [FromForm] string asker, [FromForm] string body)
        {
            _db.Questions.Add(new ProductQuestion { ProductId = productId, Asker = asker, Body = body });
            _db.SaveChanges();
            return Redirect($"/products/{productId}/questions");
        }

        [HttpGet("/products/{productId:int}/questions")]
        public IActionResult List(int productId)
        {
            var items = _db.Questions.Where(q => q.ProductId == productId).ToList();
            var sb = new StringBuilder("<ol class=\"questions\">");
            foreach (var q in items)
            {
                sb.Append("<li><b>").Append(q.Asker).Append("</b>: ").Append(q.Body).Append("</li>");
            }
            sb.Append("</ol>");
            return Content(sb.ToString(), "text/html");
        }
    }
}
