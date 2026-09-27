using System.IO;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;

namespace Catalog.Web.Controllers
{
    public class SpecSheetController : Controller
    {
        private static readonly Regex AllowedName = new Regex(@"^[\w\-./]+$", RegexOptions.Compiled);
        private const string SheetsDir = "/srv/catalog/specsheets";

        [HttpGet("products/specsheet")]
        public IActionResult Download([FromQuery] string sheet)
        {
            if (sheet == null || !AllowedName.IsMatch(sheet))
            {
                return BadRequest();
            }

            var file = Path.Combine(SheetsDir, sheet);
            return PhysicalFile(file, "application/pdf");
        }
    }
}
