using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Storefront.Pages.Gifts
{
    public class DedicationModel : PageModel
    {
        private readonly HtmlEncoder _html;

        public DedicationModel(HtmlEncoder html)
        {
            _html = html;
        }

        [BindProperty(SupportsGet = true)]
        public string Note { get; set; } = string.Empty;

        public IHtmlContent NoteHtml { get; private set; } = HtmlString.Empty;

        public void OnGet()
        {
            var encoded = _html.Encode(Note);
            var formatted = encoded.Replace("\n", "<br/>");
            NoteHtml = new HtmlString($"<p class=\"gift-note\">{formatted}</p>");
        }
    }
}
