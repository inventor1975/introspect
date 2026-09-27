using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [Route("warehouse/bins")]
    public class WarehouseBinController : Controller
    {
        private static readonly Regex BinCode = new Regex("[A-Z]{2}-[0-9]{3}", RegexOptions.Compiled);
        private readonly DbConnections _db;

        public WarehouseBinController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{code}")]
        public IActionResult Contents(string code)
        {
            if (!BinCode.IsMatch(code))
            {
                return BadRequest("Bin codes look like AB-123");
            }

            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT Sku, Quantity FROM BinStock WHERE BinCode = '" + code + "'", conn);
            using var reader = cmd.ExecuteReader();
            var model = new System.Collections.Generic.Dictionary<string, int>();
            while (reader.Read())
            {
                model[reader.GetString(0)] = reader.GetInt32(1);
            }
            return View(model);
        }
    }
}
