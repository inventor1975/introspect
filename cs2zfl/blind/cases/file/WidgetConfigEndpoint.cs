using System.IO;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Routing;

namespace Dashboard.Api
{
    public static class WidgetConfigEndpoint
    {
        private static readonly Regex WidgetId = new Regex("^[a-zA-Z0-9_-]{1,64}$");
        private const string WidgetDir = "/app/widgets";

        public static void MapWidgetConfig(this IEndpointRouteBuilder app)
        {
            app.MapGet("/widgets/config", ([FromQuery] string widget) =>
            {
                if (!WidgetId.IsMatch(widget))
                {
                    return Results.BadRequest();
                }

                var configPath = Path.Combine(WidgetDir, widget + ".json");
                return File.Exists(configPath)
                    ? Results.Text(File.ReadAllText(configPath), "application/json")
                    : Results.NotFound();
            });
        }
    }
}
