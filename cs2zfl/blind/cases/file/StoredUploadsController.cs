using System;
using System.IO;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Shared.Storage;

namespace Dropbox.Lite.Controllers
{
    [Authorize]
    [Route("uploads")]
    public class StoredUploadsController : Controller
    {
        private const string UploadRoot = "/srv/dropbox-lite/files";
        private readonly FilesDbContext _db;

        public StoredUploadsController(FilesDbContext db)
        {
            _db = db;
        }

        [HttpPost("")]
        public async Task<IActionResult> Upload(IFormFile file)
        {
            var owner = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
            var ownerDir = Path.Combine(UploadRoot, owner);
            Directory.CreateDirectory(ownerDir);

            var record = new FileRecord
            {
                OwnerId = owner,
                OriginalName = file.FileName,
                Size = file.Length,
                UploadedUtc = DateTime.UtcNow
            };

            using (var target = System.IO.File.Create(Path.Combine(ownerDir, Guid.NewGuid().ToString("N"))))
            {
                await file.CopyToAsync(target);
                record.StoragePath = target.Name;
            }

            _db.Files.Add(record);
            await _db.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        [HttpPost("{id:int}/publish")]
        public async Task<IActionResult> Publish(int id)
        {
            var owner = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
            var record = await _db.Files.SingleOrDefaultAsync(f => f.Id == id && f.OwnerId == owner);
            if (record == null)
            {
                return NotFound();
            }

            var publicCopy = Path.Combine(UploadRoot, "public", record.OriginalName);
            System.IO.File.Copy(record.StoragePath, publicCopy, overwrite: true);
            return RedirectToAction(nameof(Index));
        }

        [HttpGet("")]
        public async Task<IActionResult> Index()
        {
            var owner = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
            var files = await _db.Files.Where(f => f.OwnerId == owner).ToListAsync();
            return View(files);
        }
    }
}
