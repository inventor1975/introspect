using System.Collections.Generic;
using System.Globalization;
using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Notes.Api.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/recycle-bin")]
    public class RecycleBinController : ControllerBase
    {
        private const string BinDir = "/var/notes/recycle";

        [HttpPost("empty")]
        public IActionResult Empty([FromBody] List<int> noteIds)
        {
            var deleted = 0;
            foreach (var noteId in noteIds)
            {
                var path = Path.Combine(BinDir, noteId.ToString(CultureInfo.InvariantCulture) + ".note");
                if (System.IO.File.Exists(path))
                {
                    System.IO.File.Delete(path);
                    deleted++;
                }
            }

            return Ok(new { deleted });
        }
    }
}
