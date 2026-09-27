using System.Collections.Generic;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("deals")]
    public class RegionPreferenceController : Controller
    {
        private const string RegionKey = "deals.region";
        private readonly DbConnections _db;

        public RegionPreferenceController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost("region")]
        public IActionResult ChooseRegion([FromForm] string region)
        {
            HttpContext.Session.SetString(RegionKey, region ?? "");
            return RedirectToAction(nameof(Current));
        }

        [HttpGet("")]
        public IActionResult Current()
        {
            var region = HttpContext.Session.GetString(RegionKey) ?? "";
            var deals = new List<string>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Title FROM Deals WHERE Region = N'" + region + "' AND EndsAt > SYSUTCDATETIME()", conn);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                deals.Add(reader.GetString(0));
            }
            return View(deals);
        }
    }
}
