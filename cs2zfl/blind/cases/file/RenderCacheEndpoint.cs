using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace Renderer.Service
{
    public static class RenderCacheEndpoint
    {
        private const string CacheDir = "/var/cache/renderer";

        private static string CacheKey(string url)
        {
            using var sha = SHA256.Create();
            var hash = sha.ComputeHash(Encoding.UTF8.GetBytes(url));
            return Convert.ToHexString(hash).ToLowerInvariant();
        }

        public static void MapRenderCache(this IEndpointRouteBuilder app)
        {
            app.MapGet("/render/cached", async (HttpContext ctx) =>
            {
                var url = ctx.Request.Query["url"].ToString();
                if (url.Length == 0)
                {
                    return Results.BadRequest();
                }

                var cachePath = Path.Combine(CacheDir, CacheKey(url) + ".png");
                if (!File.Exists(cachePath))
                {
                    return Results.NotFound(new { url });
                }

                var png = await File.ReadAllBytesAsync(cachePath);
                return Results.File(png, "image/png");
            });
        }
    }
}
