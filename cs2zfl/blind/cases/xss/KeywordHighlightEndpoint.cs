using System.Linq;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class KeywordHighlightEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/highlight", (string keywords) =>
            {
                string Chip(string k) => "<mark>" + k.Trim() + "</mark>";

                var chips = keywords
                    .Split(',')
                    .Where(k => k.Length > 0)
                    .Select(Chip);
                return Results.Content("<p>Matching: " + string.Join(" ", chips) + "</p>", "text/html");
            });
        }
    }
}
