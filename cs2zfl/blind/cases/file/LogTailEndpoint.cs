using System;
using System.IO;
using System.Linq;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Ops.Console
{
    public static class LogTailEndpoint
    {
        public static void MapLogTail(this WebApplication app)
        {
            app.MapGet("/ops/logs/tail", (HttpContext ctx) =>
            {
                string log = ctx.Request.Query["log"];
                if (string.IsNullOrWhiteSpace(log))
                {
                    log = "app.log";
                }

                var text = File.ReadAllText($"/var/log/ops/{log}");
                var lines = text.Split('\n');
                var tail = string.Join('\n', lines.Skip(Math.Max(0, lines.Length - 200)));
                return Results.Text(tail, "text/plain");
            });
        }
    }
}
