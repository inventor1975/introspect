using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class CategoryLabelController : Controller
    {
        private static readonly Dictionary<string, string> Labels = new Dictionary<string, string>
        {
            ["kitchen"] = "Kitchen &amp; Dining",
            ["garden"] = "Garden",
            ["toys"] = "Toys &amp; Games",
        };

        [HttpGet("/category/{key}/title")]
        public IActionResult Title([FromRoute] string key)
        {
            var label = Labels.TryGetValue(key, out var known) ? known : key;
            return Content($"<h1 class=\"category\">{label}</h1>", "text/html");
        }
    }
}
