using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class CategoryBrowseController : Controller
    {
        private readonly StoreContext _context;

        public CategoryBrowseController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("/browse/{category}")]
        public async Task<IActionResult> Index(string category)
        {
            var products = await _context.Products
                .FromSqlRaw($"SELECT * FROM Products WHERE Category = '{category}' AND IsActive = 1")
                .OrderBy(p => p.Name)
                .ToListAsync();
            ViewData["Category"] = category;
            return View(products);
        }
    }
}
