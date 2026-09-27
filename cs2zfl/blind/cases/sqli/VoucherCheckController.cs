using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/vouchers")]
    public class VoucherCheckController : ControllerBase
    {
        private readonly DbConnections _db;

        public VoucherCheckController(DbConnections db)
        {
            _db = db;
        }

        private static string KeepCodeChars(string value)
        {
            return new string(value.ToUpperInvariant()
                .Where(c => (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '-')
                .Take(24)
                .ToArray());
        }

        [HttpGet("{code}")]
        public IActionResult Check(string code)
        {
            var normalized = KeepCodeChars(code ?? "");
            if (normalized.Length == 0)
            {
                return BadRequest();
            }
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Discount FROM Vouchers WHERE Code = '" + normalized + "' AND RedeemedAt IS NULL", conn);
            var discount = cmd.ExecuteScalar();
            return discount == null ? NotFound() : Ok(new { discount });
        }
    }
}
