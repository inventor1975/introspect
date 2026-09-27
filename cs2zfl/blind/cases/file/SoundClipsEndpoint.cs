using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Routing;

namespace Podcast.Api
{
    public static class SoundClipsEndpoint
    {
        private const string ClipsDir = "/srv/podcast/clips";

        public static void MapSoundClips(this IEndpointRouteBuilder app)
        {
            app.MapGet("/clips", ([FromQuery] string clip, HttpResponse response) =>
            {
                if (string.IsNullOrEmpty(clip)
                    || Path.GetFileName(clip) != clip
                    || clip.StartsWith('.')
                    || clip.Contains('\\'))
                {
                    return Results.BadRequest();
                }

                var path = Path.Combine(ClipsDir, clip);
                if (!File.Exists(path))
                {
                    return Results.NotFound();
                }

                response.Headers.CacheControl = "public, max-age=86400";
                return Results.File(path, "audio/mpeg", enableRangeProcessing: true);
            });
        }
    }
}
