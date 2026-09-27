using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/wishlist")]
    public class WishlistController : ControllerBase
    {
        private readonly DbConnections _db;

        public WishlistController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{owner}")]
        public IActionResult ForOwner(string owner, [FromQuery] string? list)
        {
            Func<string, string, string> build = (who, name) =>
                "SELECT ProductId FROM WishlistItems WHERE Owner = '" + who + "'" +
                (string.IsNullOrEmpty(name) ? "" : " AND ListName = '" + name + "'");

            var ids = new List<int>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(build(owner, list ?? ""), conn);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                ids.Add(reader.GetInt32(0));
            }
            return Ok(ids);
        }
    }
}
