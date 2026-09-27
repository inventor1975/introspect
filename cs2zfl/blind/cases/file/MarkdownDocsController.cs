using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace DevPortal.Controllers
{
    [Route("docs")]
    public class MarkdownDocsController : Controller
    {
        private const string DocsRoot = "/app/devportal/docs";

        [HttpGet("{*page}")]
        public IActionResult Render(string page)
        {
            var slug = Path.GetFileNameWithoutExtension(page ?? "index");
            if (string.IsNullOrEmpty(slug))
            {
                slug = "index";
            }

            var mdPath = Path.Combine(DocsRoot, slug + ".md");
            if (!System.IO.File.Exists(mdPath))
            {
                return NotFound();
            }

            var markdown = System.IO.File.ReadAllText(mdPath);
            ViewData["Slug"] = slug;
            return View("Page", markdown);
        }
    }
}
