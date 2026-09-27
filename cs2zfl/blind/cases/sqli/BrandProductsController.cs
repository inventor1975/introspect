using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/brands")]
    public class BrandProductsController : ControllerBase
    {
        private readonly StoreContext _context;

        public BrandProductsController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet("{brand}/products")]
        public async Task<IActionResult> Products(string brand, [FromQuery] decimal? maxPrice)
        {
            var ceiling = maxPrice ?? decimal.MaxValue;
            var items = await _context.Products
                .FromSql($"SELECT p.* FROM Products p JOIN Brands b ON b.Id = p.BrandId WHERE b.Slug = {brand} AND p.Price <= {ceiling}")
                .AsNoTracking()
                .ToListAsync();
            return Ok(items);
        }
    }
}
