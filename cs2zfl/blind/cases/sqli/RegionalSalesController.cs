using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Storefront.Data;

namespace Storefront.Web.Controllers
{
    public class RegionalSalesQuery
    {
        public SalesRegion Region { get; set; }
        public DateTime From { get; set; }
        public DateTime To { get; set; }
    }

    [ApiController]
    [Route("api/sales/regional")]
    public class RegionalSalesController : ControllerBase
    {
        private readonly DbConnections _db;

        public RegionalSalesController(DbConnections db)
        {
            _db = db;
        }

        [HttpPost]
        public IActionResult Totals([FromBody] RegionalSalesQuery query)
        {
            var table = "Sales_" + query.Region.ToString();
            var totals = new Dictionary<DateTime, decimal>();
            using var conn = _db.OpenMain();
            using var cmd = new SqlCommand("SELECT CAST(SoldAt AS date), SUM(Amount) FROM " + table
                                           + " WHERE SoldAt >= @from AND SoldAt < @to GROUP BY CAST(SoldAt AS date)", conn);
            cmd.Parameters.AddWithValue("@from", query.From);
            cmd.Parameters.AddWithValue("@to", query.To);
            using var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                totals[reader.GetDateTime(0)] = reader.GetDecimal(1);
            }
            return Ok(totals);
        }
    }
}
