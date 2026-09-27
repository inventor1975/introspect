using System.IO;
using System.Web;
using Microsoft.AspNetCore.Mvc;

namespace Training.Web.Controllers
{
    public class GlossaryController : Controller
    {
        private const string TermsDir = "/app/data/glossary";

        public IActionResult Term(string slug)
        {
            var encoded = HttpUtility.HtmlEncode(slug);
            var path = Path.Combine(TermsDir, encoded + ".txt");

            if (!System.IO.File.Exists(path))
            {
                return View("Missing", encoded);
            }

            var definition = System.IO.File.ReadAllText(path);
            ViewData["Title"] = encoded;
            return View("Term", definition);
        }
    }
}
