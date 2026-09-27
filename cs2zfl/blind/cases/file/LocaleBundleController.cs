using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Globalize.Api.Controllers
{
    [ApiController]
    [Route("api/i18n")]
    public class LocaleBundleController : ControllerBase
    {
        private const string BundleDir = "/app/i18n";

        private static readonly Dictionary<string, string> KnownBundles = new Dictionary<string, string>
        {
            ["en"] = "en-US.json",
            ["de"] = "de-DE.json",
            ["fr"] = "fr-FR.json",
            ["es"] = "es-ES.json",
        };

        [HttpGet("{locale}")]
        public IActionResult Bundle(string locale)
        {
            if (!KnownBundles.TryGetValue(locale, out var bundleFile))
            {
                bundleFile = locale.EndsWith(".json") ? locale : locale + ".json";
            }

            var json = System.IO.File.ReadAllText(Path.Combine(BundleDir, bundleFile));
            return Content(json, "application/json");
        }
    }
}
