using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class StoreSlugEndpoint
    {
        private static readonly Regex Handle = new Regex(@"^[A-Za-z0-9_-]{1,32}$");

        public static void Map(WebApplication app)
        {
            app.MapGet("/stores/{handle}", (string handle) =>
            {
                if (!Handle.IsMatch(handle))
                {
                    return Results.Content("<p>Unknown store.</p>", "text/html", null, 404);
                }
                return Results.Content($"<h1>@{handle}</h1><div id=\"store\" data-handle=\"{handle}\"></div>", "text/html");
            });
        }
    }
}
