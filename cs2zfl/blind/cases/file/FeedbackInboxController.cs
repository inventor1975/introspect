using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Kiosk.Web.Controllers
{
    public class FeedbackInboxController : Controller
    {
        private const string InboxFile = "/var/kiosk/feedback/inbox.log";

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Submit(string name, string message)
        {
            if (string.IsNullOrWhiteSpace(message))
            {
                ModelState.AddModelError(nameof(message), "Please write something.");
                return View("Index");
            }

            var line = string.Format("{0:u}\t{1}\t{2}{3}",
                DateTime.UtcNow,
                (name ?? "anonymous").Replace('\t', ' ').Replace('\n', ' '),
                message.Replace('\t', ' ').Replace('\n', ' '),
                Environment.NewLine);

            System.IO.File.AppendAllText(InboxFile, line);
            return RedirectToAction("Thanks");
        }
    }
}
