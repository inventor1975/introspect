using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Banking.Web.Controllers
{
    [Authorize]
    [Route("statements")]
    public class StatementPdfController : Controller
    {
        private const string StatementsDir = "/secure/banking/statements";

        [HttpGet("{accountId}/{period}")]
        public IActionResult Get([FromRoute] int accountId, [FromRoute] int period)
        {
            var fileName = $"{accountId}-{period}.pdf";
            var path = Path.Combine(StatementsDir, fileName);

            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "application/pdf", fileName);
        }
    }
}
