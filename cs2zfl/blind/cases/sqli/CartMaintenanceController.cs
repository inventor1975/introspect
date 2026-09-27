using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/cart")]
    public class CartMaintenanceController : ControllerBase
    {
        private const string DeleteTemplate = "DELETE FROM CartItems WHERE CartToken = '{0}'";
        private readonly StoreContext _context;

        public CartMaintenanceController(StoreContext context)
        {
            _context = context;
        }

        [HttpDelete("{token}")]
        public IActionResult Clear([FromRoute] string token)
        {
            var sql = string.Format(DeleteTemplate, token);
            var removed = _context.Database.ExecuteSqlRaw(sql);
            return Ok(new { removed });
        }
    }
}
