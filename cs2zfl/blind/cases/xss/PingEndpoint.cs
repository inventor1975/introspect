using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class PingEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/ping", (string? note) =>
                Results.Text("<pong>" + (note ?? "") + "</pong>"));
        }
    }
}
