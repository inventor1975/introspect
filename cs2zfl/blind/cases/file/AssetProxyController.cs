using Microsoft.AspNetCore.Mvc;
using Shared.Storage;

namespace Marketing.Site.Controllers
{
    [Route("assets")]
    public class AssetProxyController : Controller
    {
        private readonly IAssetLocator _locator;

        public AssetProxyController(IAssetLocator locator)
        {
            _locator = locator;
        }

        [HttpGet("{*key}")]
        public IActionResult Get(string key)
        {
            var physical = _locator.Locate(key);
            if (!System.IO.File.Exists(physical))
            {
                return NotFound();
            }

            var data = System.IO.File.ReadAllBytes(physical);
            return File(data, "application/octet-stream");
        }
    }
}
