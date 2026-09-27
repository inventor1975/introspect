using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class CategoryListingController : Controller
    {
        private readonly StoreContext _context;

        public CategoryListingController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("/categories/{category}")]
        public async Task<IActionResult> Index(string category)
        {
            var products = await _context.Products
                .FromSqlInterpolated($"SELECT * FROM Products WHERE Category = {category} AND IsActive = 1")
                .OrderBy(p => p.Name)
                .ToListAsync();
            ViewData["Category"] = category;
            return View(products);
        }
    }
}
