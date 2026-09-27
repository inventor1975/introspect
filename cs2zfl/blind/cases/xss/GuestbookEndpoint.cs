using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class GuestbookEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapPost("/guestbook/echo", HandleAsync);
        }

        private static async Task HandleAsync(HttpContext context)
        {
            var form = await context.Request.ReadFormAsync();
            var author = form["author"].ToString();
            var entry = form["entry"].ToString();
            context.Response.ContentType = "text/html";
            await context.Response.WriteAsync($"<div class=\"entry\"><b>{author}</b> wrote:<br/>{entry}</div>");
        }
    }
}
