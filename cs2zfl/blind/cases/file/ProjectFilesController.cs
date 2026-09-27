using System.IO;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Studio.Web.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/projects/{projectId:int}/files")]
    public class ProjectFilesController : ControllerBase
    {
        private const string ProjectsRoot = "/srv/studio/projects";

        [HttpGet]
        public IActionResult Get(int projectId, [FromQuery] string subfolder, [FromQuery] string name)
        {
            var safeName = Path.GetFileName(name);
            var path = Path.Combine(ProjectsRoot, projectId.ToString(), subfolder ?? string.Empty, safeName);

            if (!System.IO.File.Exists(path))
            {
                return NotFound();
            }

            return PhysicalFile(path, "application/octet-stream", safeName);
        }
    }
}
