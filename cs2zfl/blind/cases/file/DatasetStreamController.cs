using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Research.Data.Controllers
{
    [ApiController]
    [Route("api/datasets")]
    public class DatasetStreamController : ControllerBase
    {
        private const string DatasetDir = "/mnt/research/datasets";

        [HttpGet("{project}/raw")]
        public IActionResult Raw(string project, [FromQuery] string file)
        {
            var path = string.Format("{0}/{1}/{2}", DatasetDir, project, file);
            var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read, 81920, useAsync: true);
            return File(stream, "application/octet-stream");
        }
    }
}
