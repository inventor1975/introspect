using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Storefront.Pages.Gifts
{
    public class GiftNoteModel : PageModel
    {
        [BindProperty(SupportsGet = true)]
        public string Note { get; set; } = string.Empty;

        [BindProperty(SupportsGet = true)]
        public string Recipient { get; set; } = string.Empty;

        public IHtmlContent NoteHtml { get; private set; } = HtmlString.Empty;

        public void OnGet()
        {
            var formatted = Note.Replace("\n", "<br/>");
            NoteHtml = new HtmlString($"<p class=\"gift-note\">Dear {Recipient},<br/>{formatted}</p>");
        }
    }
}
