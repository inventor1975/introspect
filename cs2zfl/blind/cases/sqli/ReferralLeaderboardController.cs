using System.Collections.Generic;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("referrals")]
    public class ReferralLeaderboardController : Controller
    {
        private readonly DbConnections _db;

        public ReferralLeaderboardController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost("join")]
        public IActionResult Join([FromForm] string nickname, [FromForm] int customerId)
        {
            using var conn = _db.OpenMain();
            conn.Execute("INSERT INTO Referrers (CustomerId, Nickname) VALUES (@customerId, @nickname)", new { customerId, nickname });
            return RedirectToAction(nameof(Top));
        }

        [HttpGet("top")]
        public IActionResult Top()
        {
            using var conn = _db.OpenMain();
            var leaders = conn.Query<string>("SELECT TOP 10 Nickname FROM Referrers ORDER BY Referrals DESC");
            var counts = new Dictionary<string, int>();
            foreach (var nick in leaders)
            {
                var n = conn.ExecuteScalar<int>("SELECT COUNT(*) FROM ReferralSignups WHERE ReferrerNickname = '" + nick + "'");
                counts[nick] = n;
            }
            return View(counts);
        }
    }
}
