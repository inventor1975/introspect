using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class ItemDetailsEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/items/details", (HttpRequest request) =>
            {
                string raw = request.Query["id"];
                if (!int.TryParse(raw, out var itemId))
                {
                    return Results.Content("<p>Invalid item.</p>", "text/html", null, 400);
                }
                return Results.Content($"<h1>Item #{itemId}</h1><p>Loading details...</p>", "text/html");
            });
        }
    }
}
