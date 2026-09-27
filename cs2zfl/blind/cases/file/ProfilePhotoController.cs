using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace Social.Web.Controllers
{
    public class ProfilePhotoController : Controller
    {
        private static readonly string[] AllowedExtensions = { ".jpg", ".jpeg", ".png", ".webp" };
        private readonly IWebHostEnvironment _env;
        private readonly ILogger<ProfilePhotoController> _logger;

        public ProfilePhotoController(IWebHostEnvironment env, ILogger<ProfilePhotoController> logger)
        {
            _env = env;
            _logger = logger;
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Upload(IFormFile photo)
        {
            if (photo == null || photo.Length == 0)
            {
                return BadRequest();
            }

            var ext = Path.GetExtension(photo.FileName).ToLowerInvariant();
            if (Array.IndexOf(AllowedExtensions, ext) < 0)
            {
                return BadRequest("Unsupported image type.");
            }

            var storedName = Guid.NewGuid().ToString("N") + ext;
            var target = Path.Combine(_env.WebRootPath, "uploads", "photos", storedName);

            using (var stream = System.IO.File.Create(target))
            {
                await photo.CopyToAsync(stream);
            }

            _logger.LogInformation("Stored {Original} as {Stored}", photo.FileName, storedName);
            TempData["PhotoName"] = photo.FileName;
            return RedirectToAction("Edit", "Profile", new { photo = storedName });
        }
    }
}
