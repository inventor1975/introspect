using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace Storefront.Endpoints
{
    public static class ThemeStylesheetEndpoint
    {
        public static RouteHandlerBuilder MapThemeStylesheet(this IEndpointRouteBuilder routes, string themesDir)
        {
            return routes.MapGet("/theme.css", async (HttpContext context) =>
            {
                var theme = context.Request.Cookies["storefront_theme"] ?? "default/site.css";
                var cssPath = Path.Combine(themesDir, theme);

                if (!File.Exists(cssPath))
                {
                    cssPath = Path.Combine(themesDir, "default/site.css");
                }

                context.Response.ContentType = "text/css";
                await context.Response.SendFileAsync(cssPath);
            });
        }
    }
}
