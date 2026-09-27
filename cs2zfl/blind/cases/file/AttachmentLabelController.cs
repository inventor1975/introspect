using System;
using System.IO;
using System.Linq;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Projects.Web.Controllers
{
    [Authorize]
    [Route("attachments")]
    public class AttachmentLabelController : Controller
    {
        private const string AttachmentsDir = "/srv/projects/attachments";
        private static readonly string[] Permitted = { ".pdf", ".docx", ".xlsx", ".png", ".txt" };

        [HttpPost("rename")]
        [ValidateAntiForgeryToken]
        public IActionResult Rename(string currentName, string newName)
        {
            var from = Path.GetFileName(currentName);
            var to = Path.GetFileName(newName);

            if (string.IsNullOrEmpty(from) || string.IsNullOrEmpty(to))
            {
                return BadRequest();
            }

            var ext = Path.GetExtension(to);
            if (!Permitted.Contains(ext, StringComparer.OrdinalIgnoreCase))
            {
                return BadRequest("Extension not permitted.");
            }

            var source = Path.Combine(AttachmentsDir, from);
            var destination = Path.Combine(AttachmentsDir, to);
            if (!System.IO.File.Exists(source) || System.IO.File.Exists(destination))
            {
                return Conflict();
            }

            System.IO.File.Move(source, destination);
            return RedirectToAction("Index");
        }
    }
}
