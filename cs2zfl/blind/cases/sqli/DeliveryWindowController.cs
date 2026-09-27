using System;
using System.Collections.Generic;
using System.Globalization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/delivery/windows")]
    public class DeliveryWindowController : ControllerBase
    {
        private readonly DbConnections _db;

        public DeliveryWindowController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Available([FromQuery] string date)
        {
            if (!DateTime.TryParse(date, CultureInfo.InvariantCulture, DateTimeStyles.None, out var day))
            {
                return BadRequest("date expected");
            }
            var isoDay = day.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);

            var slots = new List<string>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT SlotLabel FROM DeliverySlots WHERE SlotDate = '" + isoDay + "' AND Remaining > 0", conn);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                slots.Add(reader.GetString(0));
            }
            return Ok(slots);
        }
    }
}
