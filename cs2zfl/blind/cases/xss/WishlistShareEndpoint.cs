using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Api
{
    public record WishlistShareRequest(string OwnerName, string Note, int ItemCount);

    public static class WishlistShareEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapPost("/wishlist/share/preview", ([FromBody] WishlistShareRequest req) =>
            {
                var card = BuildCard(req);
                return Results.Content(card, "text/html");
            });
        }

        private static string BuildCard(WishlistShareRequest req)
        {
            var owner = req.OwnerName;
            var note = req.Note;
            return $"<article><h3>{owner}'s wishlist ({req.ItemCount} items)</h3><p>{note}</p></article>";
        }
    }
}
