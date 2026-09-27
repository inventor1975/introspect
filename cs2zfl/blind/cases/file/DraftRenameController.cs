using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Blogging.Web.Controllers
{
    [Authorize]
    [Route("drafts")]
    public class DraftRenameController : Controller
    {
        private const string DraftsDir = "/srv/blog/drafts";

        [HttpPost("{draftId:guid}/rename")]
        [ValidateAntiForgeryToken]
        public IActionResult Rename(System.Guid draftId, [FromForm] string newName)
        {
            var current = Path.Combine(DraftsDir, draftId.ToString("N") + ".md");
            if (!System.IO.File.Exists(current))
            {
                return NotFound();
            }

            var renamed = Path.Combine(DraftsDir, newName.Trim() + ".md");
            System.IO.File.Move(current, renamed);

            return RedirectToAction("Index", "Drafts");
        }
    }
}
