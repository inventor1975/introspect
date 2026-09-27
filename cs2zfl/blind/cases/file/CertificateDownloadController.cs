using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Academy.Web.Controllers
{
    [Route("certificates")]
    public class CertificateDownloadController : Controller
    {
        private const string CertificateTemplate = "/app/assets/certificate-blank.pdf";

        [HttpGet("download")]
        public IActionResult Download([FromQuery] string saveAs)
        {
            var downloadName = string.IsNullOrWhiteSpace(saveAs) ? "certificate.pdf" : saveAs + ".pdf";
            return PhysicalFile(CertificateTemplate, "application/pdf", downloadName);
        }
    }
}
