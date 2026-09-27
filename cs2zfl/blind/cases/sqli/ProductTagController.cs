using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    [ApiController]
    [Route("api/tags")]
    public class ProductTagController : ControllerBase
    {
        private const int MaxTagLength = 40;
        private readonly DbConnections _db;

        public ProductTagController(DbConnections db)
        {
            _db = db;
        }

        [HttpGet("{tag}/products")]
        public IActionResult ProductsForTag(string tag)
        {
            if (string.IsNullOrWhiteSpace(tag) || tag.Length > MaxTagLength)
            {
                return BadRequest("invalid tag");
            }

            var skus = new List<string>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand(
                "SELECT p.Sku FROM Products p JOIN ProductTags t ON t.ProductId = p.Id WHERE t.Tag = '" + tag + "'", conn);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                skus.Add(reader.GetString(0));
            }
            return Ok(skus);
        }
    }
}
