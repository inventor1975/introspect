using System.Collections.Generic;
using System.Text;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Npgsql;

namespace Storefront.Api
{
    public static class FilteredSearchEndpoints
    {
        private static readonly Dictionary<string, string> Columns = new Dictionary<string, string>
        {
            ["brand"] = "brand_slug",
            ["color"] = "color",
            ["size"] = "size_code",
            ["category"] = "category"
        };

        public static void MapFilteredSearch(this IEndpointRouteBuilder app)
        {
            app.MapGet("/api/search/filtered", async (HttpRequest request, NpgsqlDataSource dataSource) =>
            {
                var where = new StringBuilder("TRUE");
                await using var cmd = dataSource.CreateCommand();
                var n = 0;
                foreach (var pair in request.Query)
                {
                    if (!Columns.TryGetValue(pair.Key, out var column))
                    {
                        continue;
                    }
                    var p = "f" + n++;
                    where.Append(" AND ").Append(column).Append(" = @").Append(p);
                    cmd.Parameters.AddWithValue(p, pair.Value.ToString());
                }

                cmd.CommandText = "SELECT name FROM products WHERE " + where + " LIMIT 100";
                var names = new List<string>();
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
