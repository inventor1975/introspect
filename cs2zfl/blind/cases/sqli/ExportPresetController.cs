using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Npgsql;

namespace Storefront.Web.Controllers
{
    public class ExportPreset
    {
        public string Source { get; set; } = "";
        public string Columns { get; set; } = "*";
    }

    [ApiController]
    [Route("api/exports")]
    public class ExportPresetController : ControllerBase
    {
        private readonly NpgsqlDataSource _ds;
        private readonly IWebHostEnvironment _env;

        public ExportPresetController(NpgsqlDataSource ds, IWebHostEnvironment env)
        {
            _ds = ds;
            _env = env;
        }

        [HttpGet("nightly")]
        public IActionResult Nightly([FromQuery] string since)
        {
            var path = Path.Combine(_env.ContentRootPath, "App_Data", "export-preset.json");
            var preset = JsonSerializer.Deserialize<ExportPreset>(System.IO.File.ReadAllText(path)) ?? new ExportPreset();

            using var cmd = _ds.CreateCommand("SELECT " + preset.Columns + " FROM " + preset.Source + " WHERE updated_at >= @since::timestamptz");
            cmd.Parameters.AddWithValue("since", since ?? "1970-01-01");
            var rows = new List<object[]>();
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                var values = new object[reader.FieldCount];
                reader.GetValues(values);
                rows.Add(values);
            }
            return Ok(rows);
        }
    }
}
