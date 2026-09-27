using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace SaaS.Portal.Controllers
{
    [Route("t/{tenant}/assets")]
    public class TenantAssetsController : Controller
    {
        private const string AssetsBase = "/srv/portal/tenants";

        [HttpGet("{**assetPath}")]
        public IActionResult Get(string tenant, string assetPath)
        {
            var tenantRoot = Path.Combine(AssetsBase, tenant);
            var resolved = Path.GetFullPath(Path.Combine(tenantRoot, assetPath));

            if (!resolved.StartsWith(Path.GetFullPath(tenantRoot), StringComparison.OrdinalIgnoreCase))
            {
                return Forbid();
            }

            if (!System.IO.File.Exists(resolved))
            {
                return NotFound();
            }

            return PhysicalFile(resolved, "application/octet-stream");
        }
    }
}
