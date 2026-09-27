using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/coupons")]
    public class CouponRedeemController : ControllerBase
    {
        private readonly DbConnections _db;

        public CouponRedeemController(DbConnections db)
        {
            _db = db;
        }

        private static string StripSqlMeta(string value)
        {
            return value.Replace("--", "").Replace(";", "").Replace("/*", "").Replace("*/", "");
        }

        [HttpPost("{code}/redeem")]
        public IActionResult Redeem(string code)
        {
            var cleaned = StripSqlMeta(code).ToUpperInvariant();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Discount FROM Coupons WHERE Code = '" + cleaned + "' AND RedeemedAt IS NULL", conn);
            var discount = cmd.ExecuteScalar();
            if (discount == null)
            {
                return NotFound();
            }
            return Ok(new { discount });
        }
    }
}
