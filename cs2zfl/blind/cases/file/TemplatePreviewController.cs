using System.IO;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Shared.Storage;

namespace Mailer.Admin.Controllers
{
    [Route("admin/templates")]
    public class TemplatePreviewController : Controller
    {
        private readonly IWebHostEnvironment _env;

        public TemplatePreviewController(IWebHostEnvironment env)
        {
            _env = env;
        }

        [HttpGet("preview")]
        public IActionResult Preview(string template)
        {
            var templatesRoot = Path.Combine(_env.ContentRootPath, "EmailTemplates");
            var path = PathJoin.UnderContent(templatesRoot, template);
            var bytes = System.IO.File.ReadAllBytes(path);
            return File(bytes, "text/html");
        }
    }
}
