using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Build.Agent.Controllers
{
    [Authorize]
    [Route("workspaces")]
    public class WorkspaceCleanupController : Controller
    {
        private const string WorkspacesRoot = "/var/build/workspaces";

        [HttpPost("cleanup")]
        [ValidateAntiForgeryToken]
        public IActionResult Cleanup()
        {
            var workspace = Request.Form["workspace"].ToString();
            if (string.IsNullOrWhiteSpace(workspace))
            {
                TempData["Error"] = "No workspace selected.";
                return RedirectToAction("Index", "Dashboard");
            }

            var dir = Path.Combine(WorkspacesRoot, workspace.Trim());
            if (Directory.Exists(dir))
            {
                Directory.Delete(dir, recursive: true);
            }

            TempData["Info"] = $"Workspace {workspace} removed.";
            return RedirectToAction("Index", "Dashboard");
        }
    }
}
