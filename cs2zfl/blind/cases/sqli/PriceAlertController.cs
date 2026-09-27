using System.Data;
using System.Threading.Tasks;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class PriceAlertForm
    {
        public string Sku { get; set; } = "";
        public string Email { get; set; } = "";
        public decimal TargetPrice { get; set; }
    }

    [ApiController]
    [Route("api/price-alerts")]
    public class PriceAlertController : ControllerBase
    {
        private readonly DbConnections _db;

        public PriceAlertController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost]
        public async Task<IActionResult> Create([FromBody] PriceAlertForm form)
        {
            var args = new DynamicParameters();
            args.Add("sku", form.Sku, DbType.String, size: 32);
            args.Add("email", form.Email, DbType.String, size: 256);
            args.Add("target", form.TargetPrice, DbType.Decimal);

            var sql = "INSERT INTO PriceAlerts (Sku, Email, TargetPrice) VALUES (@sku, @email, @target)";
            await using var conn = _db.OpenMain();
            await conn.ExecuteAsync(sql, args);
            return Accepted();
        }
    }
}
