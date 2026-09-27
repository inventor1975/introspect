using System.Collections.Generic;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class StoreLocation
    {
        public int Id { get; set; }
        public string City { get; set; } = "";
        public string Address { get; set; } = "";
    }

    [Route("stores")]
    public class StoreLocatorController : Controller
    {
        private readonly DbConnections _db;

        public StoreLocatorController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet]
        public IActionResult Index([FromQuery] string? city)
        {
            var condition = string.IsNullOrWhiteSpace(city)
                ? "1 = 1"
                : "City = N'" + city + "'";
            using var conn = _db.OpenMain();
            IEnumerable<StoreLocation> stores = conn.Query<StoreLocation>("SELECT Id, City, Address FROM Stores WHERE " + condition + " ORDER BY City");
            return View(stores);
        }
    }
}
