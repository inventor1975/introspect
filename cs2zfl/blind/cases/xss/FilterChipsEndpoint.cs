using System.Text;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class FilterChipsEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/filters/chips", (HttpRequest request) =>
            {
                var enc = HtmlEncoder.Default;
                var sb = new StringBuilder("<ul class=\"chips\">");
                foreach (var f in request.Query["f"])
                {
                    var label = enc.Encode(f ?? string.Empty);
                    sb.Append("<li>").Append(label).Append("</li>");
                }
                sb.Append("</ul>");
                return Results.Content(sb.ToString(), "text/html");
            });
        }
    }
}
