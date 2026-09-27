using System.IO;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;

namespace Travel.Web.Controllers
{
    [Route("brochures")]
    public class BrochureDownloadController : Controller
    {
        private readonly IWebHostEnvironment _env;

        public BrochureDownloadController(IWebHostEnvironment env)
        {
            _env = env;
        }

        [HttpGet("{file}")]
        public IActionResult Download(string file)
        {
            var fileName = Path.GetFileName(file);
            var brochureDir = Path.Combine(_env.ContentRootPath, "brochures");
            var path = Path.Combine(brochureDir, fileName);

            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "application/pdf", fileName);
        }
    }
}
