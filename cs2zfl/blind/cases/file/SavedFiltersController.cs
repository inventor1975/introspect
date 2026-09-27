using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Inventory.Api.Controllers
{
    public class SavedFilterDto
    {
        public string Name { get; set; } = "";
        public string Query { get; set; } = "";
    }

    [ApiController]
    [Route("api/filters")]
    public class SavedFiltersController : ControllerBase
    {
        private const string FiltersDir = "/var/inventory/filters";

        [HttpPut]
        public IActionResult Save([FromBody] SavedFilterDto dto)
        {
            var name = dto.Name?.Trim() ?? string.Empty;
            if (name.Length == 0
                || name.Length > 80
                || name.IndexOfAny(Path.GetInvalidFileNameChars()) >= 0
                || name.Contains('/')
                || name.Contains('\\')
                || name.StartsWith("."))
            {
                return BadRequest("Filter name is not allowed.");
            }

            var target = Path.Combine(FiltersDir, name + ".filter");
            System.IO.File.WriteAllText(target, dto.Query);
            return NoContent();
        }
    }
}
