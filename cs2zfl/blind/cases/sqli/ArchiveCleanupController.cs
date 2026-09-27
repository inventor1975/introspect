using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Authorize(Roles = "Staff")]
    [Route("api/archive")]
    public class ArchiveCleanupController : ControllerBase
    {
        private readonly StoreContext _context;

        public ArchiveCleanupController(StoreContext context)
        {
            _context = context;
        }

        [HttpDelete("{kind}/{id:int}")]
        public async Task<IActionResult> Purge(string kind, int id)
        {
            var table = kind + "Archive";
            var count = await _context.Database.ExecuteSqlRawAsync("DELETE FROM " + table + " WHERE Id = {0}", id);
            return Ok(new { count });
        }
    }
}
