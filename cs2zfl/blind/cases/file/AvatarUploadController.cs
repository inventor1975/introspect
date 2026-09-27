using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Community.Web.Controllers
{
    public class AvatarUploadController : Controller
    {
        private readonly IWebHostEnvironment _env;

        public AvatarUploadController(IWebHostEnvironment env)
        {
            _env = env;
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Upload(IFormFile avatar)
        {
            if (avatar == null || avatar.Length == 0)
            {
                ModelState.AddModelError("avatar", "Please choose an image.");
                return View();
            }

            if (avatar.Length > 2 * 1024 * 1024)
            {
                ModelState.AddModelError("avatar", "Image too large.");
                return View();
            }

            var avatarsDir = Path.Combine(_env.WebRootPath, "img", "avatars");
            var target = Path.Combine(avatarsDir, avatar.FileName);

            using (var stream = new FileStream(target, FileMode.Create))
            {
                await avatar.CopyToAsync(stream);
            }

            TempData["Message"] = "Avatar updated.";
            return RedirectToAction("Index", "Profile");
        }
    }
}
