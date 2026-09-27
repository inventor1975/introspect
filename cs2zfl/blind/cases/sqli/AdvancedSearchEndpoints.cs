using System.Collections.Generic;
using System.Text;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Npgsql;

namespace Storefront.Api
{
    public static class AdvancedSearchEndpoints
    {
        public static void MapAdvancedSearch(this IEndpointRouteBuilder app)
        {
            app.MapGet("/api/search/advanced", async (HttpRequest request, NpgsqlDataSource dataSource) =>
            {
                var where = new StringBuilder("TRUE");
                foreach (var pair in request.Query)
                {
                    if (pair.Key == "limit")
                    {
                        continue;
                    }
                    where.Append(" AND ").Append(pair.Key).Append(" = '").Append(pair.Value.ToString()).Append('\'');
                }

                var names = new List<string>();
                await using var cmd = dataSource.CreateCommand("SELECT name FROM products WHERE " + where + " LIMIT 100");
                await using var reader = await cmd.ExecuteReaderAsync();
                while (await reader.ReadAsync())
                {
                    names.Add(reader.GetString(0));
                }
                return Results.Ok(names);
            });
        }
    }
}
