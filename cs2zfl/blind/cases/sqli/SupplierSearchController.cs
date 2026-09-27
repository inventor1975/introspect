using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/suppliers/products")]
    public class SupplierSearchController : ControllerBase
    {
        private readonly StoreContext _context;

        public SupplierSearchController(StoreContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<IActionResult> Get([FromQuery] string supplier, [FromQuery] decimal maxPrice)
        {
            var sql = FormattableString.Invariant(
                $"SELECT p.* FROM Products p JOIN Suppliers s ON s.Id = p.SupplierId WHERE s.Code = '{supplier}' AND p.Price <= {maxPrice}");
            var items = await _context.Products.FromSqlRaw(sql).AsNoTracking().ToListAsync();
            return Ok(items);
        }
    }
}
