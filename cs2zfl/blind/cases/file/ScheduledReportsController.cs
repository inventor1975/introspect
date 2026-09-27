using System;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Fleet.Reports.Controllers
{
    public enum ReportKind
    {
        Mileage,
        FuelUsage,
        Maintenance,
        DriverHours
    }

    [ApiController]
    [Route("api/reports/scheduled")]
    public class ScheduledReportsController : ControllerBase
    {
        private const string OutputDir = "/var/fleet/reports";

        [HttpGet("{kind}")]
        public IActionResult Latest(string kind)
        {
            if (!Enum.TryParse<ReportKind>(kind, ignoreCase: true, out var parsed) || !Enum.IsDefined(typeof(ReportKind), parsed))
            {
                return NotFound();
            }

            var path = Path.Combine(OutputDir, parsed.ToString().ToLowerInvariant() + ".csv");
            var stream = new FileStream(path, FileMode.Open, FileAccess.Read);
            return File(stream, "text/csv");
        }
    }
}
