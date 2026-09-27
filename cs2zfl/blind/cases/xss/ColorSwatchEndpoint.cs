using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Storefront.Web.Validation;

namespace Storefront.Api
{
    public static class ColorSwatchEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/swatch", (string color) =>
            {
                if (!InputRules.HasLetters(color))
                {
                    return Results.BadRequest();
                }
                var html = $"<div style=\"width:40px;height:40px\" title=\"{color}\">{color}</div>";
                return Results.Content(html, "text/html");
            });
        }
    }
}
