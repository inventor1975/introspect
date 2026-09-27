using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Office.Print.Controllers
{
    [ApiController]
    [Route("api/print")]
    public class PrintQueueController : ControllerBase
    {
        private const string SpoolDir = "/var/spool/office";

        [HttpPost("{queue}")]
        public IActionResult Enqueue(string queue, [FromBody] string document)
        {
            string spoolFile;
            if (queue == "color")
            {
                spoolFile = "color.queue";
            }
            else
            {
                spoolFile = "mono.queue";
            }

            System.IO.File.AppendAllText(Path.Combine(SpoolDir, spoolFile), document + "\n");
            return Accepted(new { queue = spoolFile });
        }
    }
}
