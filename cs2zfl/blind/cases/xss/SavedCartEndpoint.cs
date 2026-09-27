using System.Text.Json;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class SavedCartEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/cart/restore", (string label, string promo) =>
            {
                var state = JsonSerializer.Serialize(new { label, promo, restored = true });
                var html = "<div id=\"cart\"></div><script>const saved = " + state + "; restoreCart(saved);</script>";
                return Results.Content(html, "text/html");
            });
        }
    }
}
