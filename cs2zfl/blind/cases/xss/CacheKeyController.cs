using System;
using System.Security.Cryptography;
using System.Text;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class CacheKeyController : Controller
    {
        [HttpGet("/tools/cache-key")]
        public IActionResult Compute(string input)
        {
            var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(input ?? string.Empty));
            var hex = Convert.ToHexString(bytes);
            return Content("<p>Cache key for your input:</p><code>" + hex + "</code>", "text/html");
        }
    }
}
