using System.Text.Encodings.Web;
using System.Text.Json;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class StatusBoardEndpoint
    {
        private static readonly JsonSerializerOptions Relaxed = new JsonSerializerOptions
        {
            Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };

        public static void Map(WebApplication app)
        {
            app.MapGet("/status/board", (string filter) =>
            {
                var state = JsonSerializer.Serialize(new { filter, refresh = 30 }, Relaxed);
                var html = "<div id=\"board\"></div><script>const initial = " + state + "; mountBoard(initial);</script>";
                return Results.Content(html, "text/html");
            });
        }
    }
}
