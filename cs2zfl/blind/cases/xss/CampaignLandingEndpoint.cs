using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class CampaignLanding
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/c/landing", async (HttpContext ctx) =>
            {
                string campaign = ctx.Request.Query["utm_campaign"];
                ctx.Response.ContentType = "text/html; charset=utf-8";
                await ctx.Response.WriteAsync("<html><body>");
                await ctx.Response.WriteAsync("<h2>Offer: " + campaign + "</h2>");
                await ctx.Response.WriteAsync("</body></html>");
            });
        }
    }
}
