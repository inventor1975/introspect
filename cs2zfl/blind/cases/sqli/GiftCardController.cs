using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/giftcards")]
    public class GiftCardController : ControllerBase
    {
        private readonly DbConnections _db;

        public GiftCardController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("balance")]
        public IActionResult Balance([FromQuery] string cardNumber)
        {
            using var conn = _db.OpenMain();
            using var cmd = conn.CreateCommand();
            cmd.CommandText = "SELECT Balance FROM GiftCards WHERE CardNumber = " + SqlFragments.Literal(cardNumber);
            var balance = cmd.ExecuteScalar();
            return balance is null ? NotFound() : Ok(new { balance });
        }
    }
}
