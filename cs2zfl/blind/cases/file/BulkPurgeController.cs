using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace PhotoShare.Web.Controllers
{
    [Authorize]
    public class BulkPurgeController : Controller
    {
        private const string GalleryRoot = "/srv/photoshare/gallery";

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Purge()
        {
            var selected = Request.Form["photos"];
            var removed = new List<string>();

            foreach (var photo in selected)
            {
                if (string.IsNullOrEmpty(photo))
                {
                    continue;
                }

                var path = GalleryRoot + "/" + User.Identity!.Name + "/" + photo;
                if (System.IO.File.Exists(path))
                {
                    System.IO.File.Delete(path);
                    removed.Add(photo);
                }
            }

            TempData["Removed"] = removed.Count;
            return RedirectToAction("Index", "Gallery");
        }
    }
}
