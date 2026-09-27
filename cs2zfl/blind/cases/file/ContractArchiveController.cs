using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Shared.Storage;

namespace Legal.Portal.Controllers
{
    [Authorize]
    [Route("contracts")]
    public class ContractArchiveController : Controller
    {
        private readonly DocumentStore _store = new DocumentStore("/srv/legal/contracts");

        [HttpGet("{id}")]
        public IActionResult Download(string id)
        {
            if (!_store.Exists(id))
            {
                return NotFound();
            }

            var content = _store.Load(id);
            return File(content, "application/pdf", "contract.pdf");
        }
    }
}
