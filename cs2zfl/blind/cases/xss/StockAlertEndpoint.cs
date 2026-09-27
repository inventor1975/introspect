using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class StockAlertEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapPost("/stock/alert", Handle);
        }

        private static string Row(string label, string value)
        {
            return "<tr><th>" + label + "</th><td>" + WebUtility.HtmlEncode(value) + "</td></tr>";
        }

        private static async Task Handle(HttpContext context)
        {
            var form = await context.Request.ReadFormAsync();
            var html = "<table>" + Row("Product", form["product"]) + Row("Email", form["email"]) + "</table>";
            context.Response.ContentType = "text/html";
            await context.Response.WriteAsync(html);
        }
    }
}
