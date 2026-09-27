using System.IO;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;

namespace Billing.Web.Controllers
{
    [ApiController]
    [Route("api/invoices")]
    public class InvoiceDownloadController : ControllerBase
    {
        private readonly IWebHostEnvironment _env;

        public InvoiceDownloadController(IWebHostEnvironment env)
        {
            _env = env;
        }

        [HttpGet("download")]
        public IActionResult Download([FromQuery] string file)
        {
            var invoiceDir = Path.Combine(_env.ContentRootPath, "storage", "invoices");
            var fullPath = Path.Combine(invoiceDir, file);

            if (!System.IO.File.Exists(fullPath))
            {
                return NotFound();
            }

            return PhysicalFile(fullPath, "application/pdf");
        }
    }
}
