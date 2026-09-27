using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CaseManager.Pages.Evidence
{
    [Authorize(Policy = "Investigators")]
    public class EvidenceViewerModel : PageModel
    {
        private const string EvidenceStore = "/secure/casemanager/evidence";

        [BindProperty(SupportsGet = true)]
        public string CaseNumber { get; set; } = "";

        [BindProperty(SupportsGet = true)]
        public string Item { get; set; } = "";

        public string Notes { get; private set; } = "";

        public IActionResult OnGet()
        {
            var caseDir = Path.Combine(EvidenceStore, CaseNumber);
            var notesFile = Path.Combine(caseDir, Item);

            if (!System.IO.File.Exists(notesFile))
            {
                return NotFound();
            }

            Notes = System.IO.File.ReadAllText(notesFile);
            return Page();
        }
    }
}
