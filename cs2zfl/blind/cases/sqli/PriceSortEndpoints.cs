using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Routing;
using Npgsql;
using Storefront.Data;

namespace Storefront.Api
{
    public static class PriceSortEndpoints
    {
        public static void MapPriceSort(this IEndpointRouteBuilder app)
        {
            app.MapGet("/api/products/by-price", async ([FromQuery] string? dir, [FromQuery] string category, NpgsqlDataSource ds) =>
            {
                if (!Enum.TryParse<SortDirection>(dir, ignoreCase: true, out var direction))
                {
                    direction = SortDirection.Asc;
                }
                var order = direction == SortDirection.Desc ? "DESC" : "ASC";

                await using var cmd = ds.CreateCommand("SELECT sku, price FROM products WHERE category = $1 ORDER BY price " + order);
                cmd.Parameters.Add(new NpgsqlParameter { Value = category });
                var rows = new List<object>();
                await using var reader = await cmd.ExecuteReaderAsync();
                while (await reader.ReadAsync())
                {
                    rows.Add(new { sku = reader.GetString(0), price = reader.GetDecimal(1) });
                }
                return Results.Ok(rows);
            });
        }
    }
}
