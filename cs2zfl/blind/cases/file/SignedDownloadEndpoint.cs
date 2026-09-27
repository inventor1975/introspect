using System;
using System.IO;
using System.Text;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Delivery.Service
{
    public static class SignedDownloadEndpoint
    {
        private const string DeliveryRoot = "/srv/delivery/outbox";

        public static void MapSignedDownloads(this WebApplication app)
        {
            app.MapGet("/d/{token}", ([FromRoute] string token) =>
            {
                string relative;
                try
                {
                    var raw = Convert.FromBase64String(token.Replace('-', '+').Replace('_', '/'));
                    relative = Encoding.UTF8.GetString(raw);
                }
                catch (FormatException)
                {
                    return Results.BadRequest();
                }

                var parts = relative.Split('|');
                if (parts.Length != 2)
                {
                    return Results.BadRequest();
                }

                var expires = DateTimeOffset.FromUnixTimeSeconds(long.Parse(parts[1]));
                if (expires < DateTimeOffset.UtcNow)
                {
                    return Results.StatusCode(StatusCodes.Status410Gone);
                }

                var path = Path.Combine(DeliveryRoot, parts[0]);
                return Results.File(path, "application/octet-stream", Path.GetFileName(path));
            });
        }
    }
}
