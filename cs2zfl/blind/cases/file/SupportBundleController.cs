using System;
using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Shared.Storage;

namespace Appliance.Admin.Controllers
{
    [Authorize(Roles = "Support")]
    [Route("support/bundles")]
    public class SupportBundleController : Controller
    {
        private const string BundleRoot = "/var/appliance/support-bundles";

        [HttpGet("{**relative}")]
        public IActionResult Fetch(string relative)
        {
            string path;
            try
            {
                path = RootedPaths.ResolveUnder(BundleRoot, relative);
            }
            catch (UnauthorizedAccessException)
            {
                return Forbid();
            }

            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "application/gzip", Path.GetFileName(path));
        }
    }
}
