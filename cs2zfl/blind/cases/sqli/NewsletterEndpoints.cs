using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Npgsql;

namespace Storefront.Api
{
    public static class NewsletterEndpoints
    {
        public static RouteGroupBuilder MapNewsletter(this IEndpointRouteBuilder app)
        {
            var group = app.MapGroup("/newsletter");

            group.MapPost("/unsubscribe", async (HttpRequest req, NpgsqlDataSource ds) =>
            {
                var form = await req.ReadFormAsync();
                var address = form["address"].ToString().Trim().ToLowerInvariant();
                if (address.Length == 0 || !address.Contains('@'))
                {
                    return Results.BadRequest();
                }

                await using var conn = await ds.OpenConnectionAsync();
                await using var cmd = conn.CreateCommand();
                cmd.CommandText = "UPDATE subscribers SET active = false, left_at = now() WHERE lower(address) = '" + address + "'";
                var rows = await cmd.ExecuteNonQueryAsync();
                return rows > 0 ? Results.NoContent() : Results.NotFound();
            });

            return group;
        }
    }
}
