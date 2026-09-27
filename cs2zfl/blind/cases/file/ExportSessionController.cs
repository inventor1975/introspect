using System.IO;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Ledger.Web.Controllers
{
    [Route("ledger/export")]
    public class ExportSessionController : Controller
    {
        private const string ExportFolder = "/var/ledger/exports";
        private const string SessionKey = "Ledger.PendingExport";

        [HttpPost("prepare")]
        [ValidateAntiForgeryToken]
        public IActionResult Prepare(string exportFile)
        {
            HttpContext.Session.SetString(SessionKey, exportFile ?? "ledger.csv");
            return RedirectToAction(nameof(Ready));
        }

        [HttpGet("ready")]
        public IActionResult Ready()
        {
            return View();
        }

        [HttpGet("fetch")]
        public IActionResult Fetch()
        {
            var pending = HttpContext.Session.GetString(SessionKey);
            if (pending == null)
            {
                return RedirectToAction(nameof(Ready));
            }

            var bytes = System.IO.File.ReadAllBytes(Path.Combine(ExportFolder, pending));
            return File(bytes, "text/csv", "ledger-export.csv");
        }
    }
}
