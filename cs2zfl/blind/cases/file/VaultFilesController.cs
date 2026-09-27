using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Shared.Storage;

namespace Vault.Web.Controllers
{
    [Authorize]
    [Route("vault")]
    public class VaultFilesController : Controller
    {
        private readonly FilesDbContext _db;

        public VaultFilesController(FilesDbContext db)
        {
            _db = db;
        }

        [HttpGet("{id:int}")]
        public async Task<IActionResult> Download(int id, [FromQuery] string? inline)
        {
            var owner = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var record = await _db.Files
                .Where(f => f.Id == id && f.OwnerId == owner)
                .SingleOrDefaultAsync();

            if (record == null)
            {
                return NotFound();
            }

            var bytes = await System.IO.File.ReadAllBytesAsync(record.StoragePath);
            if (inline == "1")
            {
                return File(bytes, "application/octet-stream");
            }

            return File(bytes, "application/octet-stream", "download.bin");
        }
    }
}
