using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class RegionNameController : Controller
    {
        private static readonly IReadOnlyDictionary<string, string> Regions = new Dictionary<string, string>
        {
            ["eu"] = "Europe",
            ["na"] = "North America",
            ["apac"] = "Asia &amp; Pacific",
        };

        [HttpGet("/region/{code}/title")]
        public IActionResult Title([FromRoute] string code)
        {
            if (!Regions.TryGetValue(code, out var label))
            {
                label = "Other regions";
            }
            return Content($"<h1 class=\"region\">{label}</h1>", "text/html");
        }
    }
}
