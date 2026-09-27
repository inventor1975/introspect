using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace DealRoom.Web.Controllers
{
    [Authorize]
    [Route("dataroom")]
    public class DataRoomController : Controller
    {
        private static readonly string RoomRoot = Path.GetFullPath("/srv/dealroom/room");

        [HttpGet("file")]
        public IActionResult Open(string path)
        {
            var full = Path.GetFullPath(Path.Combine(RoomRoot, path ?? string.Empty));
            var relative = Path.GetRelativePath(RoomRoot, full);

            if (relative == "." || relative.StartsWith("..") || Path.IsPathRooted(relative))
            {
                return BadRequest();
            }

            var stream = System.IO.File.OpenRead(full);
            return File(stream, "application/octet-stream", Path.GetFileName(full));
        }
    }
}
