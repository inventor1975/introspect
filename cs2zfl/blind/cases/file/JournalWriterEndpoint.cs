using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace FieldNotes.Api
{
    public static class JournalWriterEndpoint
    {
        private const string JournalDir = "/var/fieldnotes/journals";

        public static void MapJournalWriter(this IEndpointRouteBuilder endpoints)
        {
            endpoints.MapPost("/journal", async (HttpRequest request) =>
            {
                var form = await request.ReadFormAsync();
                var journal = form["journal"].ToString();
                var entry = form["entry"].ToString();

                if (journal.Length == 0 || entry.Length == 0)
                {
                    return Results.BadRequest();
                }

                var path = Path.Combine(JournalDir, journal);
                using (var writer = new StreamWriter(path, append: true))
                {
                    await writer.WriteLineAsync($"{DateTime.UtcNow:O}\t{entry}");
                }

                return Results.NoContent();
            });
        }
    }
}
