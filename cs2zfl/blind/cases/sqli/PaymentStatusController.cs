using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Logging;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("payments")]
    public class PaymentStatusController : Controller
    {
        private readonly DbConnections _db;
        private readonly ILogger<PaymentStatusController> _log;

        public PaymentStatusController(DbConnections db, ILogger<PaymentStatusController> log)
        {
            _db = db;
            _log = log;
        }

        [HttpGet("status")]
        public IActionResult Status(string reference)
        {
            long paymentId;
            try
            {
                paymentId = long.Parse(reference);
            }
            catch (FormatException)
            {
                _log.LogWarning("Rejected payment reference {Reference}", reference);
                return BadRequest("reference must be numeric");
            }
            catch (OverflowException)
            {
                return BadRequest("reference out of range");
            }

            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT State, Amount FROM Payments WHERE Id = " + paymentId, conn);
            using var reader = cmd.ExecuteReader();
            if (!reader.Read())
            {
                return NotFound();
            }
            return Json(new { state = reader.GetString(0), amount = reader.GetDecimal(1) });
        }
    }
}
