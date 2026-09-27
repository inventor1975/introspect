using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace Helpdesk.Web.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/tickets/{ticketId:int}/attachments")]
    public class AttachmentRemovalController : ControllerBase
    {
        private const string UploadsRoot = "/data/helpdesk/uploads";
        private readonly ILogger<AttachmentRemovalController> _log;

        public AttachmentRemovalController(ILogger<AttachmentRemovalController> log)
        {
            _log = log;
        }

        [HttpDelete("{fileName}")]
        public IActionResult Remove([FromRoute] int ticketId, [FromRoute] string fileName)
        {
            var ticketDir = Path.Combine(UploadsRoot, ticketId.ToString());
            var target = Path.Combine(ticketDir, fileName);

            System.IO.File.Delete(target);
            _log.LogInformation("Removed attachment {File} from ticket {Ticket}", fileName, ticketId);
            return NoContent();
        }
    }
}
