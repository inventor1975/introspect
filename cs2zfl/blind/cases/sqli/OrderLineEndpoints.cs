using System.Collections.Generic;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Npgsql;

namespace Storefront.Api
{
    public static class OrderLineEndpoints
    {
        public static void MapOrderLines(this IEndpointRouteBuilder app)
        {
            app.MapGet("/api/orders/{id:long}/lines", async (long id, NpgsqlDataSource ds) =>
            {
                await using var conn = await ds.OpenConnectionAsync();
                await using var cmd = new NpgsqlCommand($"SELECT sku, quantity, unit_price FROM order_lines WHERE order_id = {id} ORDER BY line_no", conn);
                var lines = new List<object>();
                await using var reader = await cmd.ExecuteReaderAsync();
                while (await reader.ReadAsync())
                {
                    lines.Add(new { sku = reader.GetString(0), qty = reader.GetInt32(1), price = reader.GetDecimal(2) });
                }
                return Results.Ok(lines);
            });
        }
    }
}
