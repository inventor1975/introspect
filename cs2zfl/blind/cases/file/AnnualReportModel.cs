using System.IO;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace InvestorRelations.Pages
{
    public class AnnualReportModel : PageModel
    {
        private const string ReportsDir = "/app/ir/annual-reports";

        [BindProperty(SupportsGet = true)]
        public int Year { get; set; }

        public IActionResult OnGetDownload()
        {
            if (Year < 2000 || Year > 2100)
            {
                return NotFound();
            }

            var path = Path.Combine(ReportsDir, $"annual-report-{Year}.pdf");
            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "application/pdf", $"annual-report-{Year}.pdf");
        }
    }
}
