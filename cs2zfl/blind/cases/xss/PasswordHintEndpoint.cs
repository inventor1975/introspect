using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class PasswordHintEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapPost("/account/password/strength", async (HttpContext ctx) =>
            {
                var form = await ctx.Request.ReadFormAsync();
                string candidate = form["password"];
                int length = candidate?.Length ?? 0;
                bool hasDigit = candidate != null && candidate.Any(char.IsDigit);
                var verdict = length >= 12 && hasDigit ? "strong" : "weak";
                ctx.Response.ContentType = "text/html";
                await ctx.Response.WriteAsync($"<p>Length: {length}. Strength: <b>{verdict}</b></p>");
            });
        }
    }
}
