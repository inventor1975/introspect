using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/cart/expire")]
    public class CartExpiryController : ControllerBase
    {
        private const string DeleteTemplate = "DELETE FROM CartItems WHERE CartToken = {0}";
        private readonly StoreContext _context;

        public CartExpiryController(StoreContext context)
        {
            _context = context;
        }

        [HttpDelete("{token}")]
        public IActionResult Expire([FromRoute] string token)
        {
            var removed = _context.Database.ExecuteSqlRaw(DeleteTemplate, token);
            return Ok(new { removed });
        }
    }
}
