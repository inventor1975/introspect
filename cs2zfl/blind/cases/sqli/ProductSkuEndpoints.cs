using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Npgsql;

namespace Storefront.Api
{
    public static class ProductSkuEndpoints
    {
        public static IEndpointRouteBuilder MapProductSku(this IEndpointRouteBuilder app)
        {
            app.MapGet("/api/products/{sku}", async (string sku, NpgsqlDataSource dataSource) =>
            {
                await using var conn = await dataSource.OpenConnectionAsync();
                await using var cmd = new NpgsqlCommand($"SELECT id, name, price FROM products WHERE sku = '{sku}' LIMIT 1", conn);
                await using var reader = await cmd.ExecuteReaderAsync();
                if (!await reader.ReadAsync())
                {
                    return Results.NotFound();
                }
                return Results.Ok(new
                {
                    id = reader.GetInt32(0),
                    name = reader.GetString(1),
                    price = reader.GetDecimal(2)
                });
            });
            return app;
        }
    }
}
