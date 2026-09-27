using System.Text;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class TagCloudEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/tags/cloud", (HttpRequest request) =>
            {
                var sb = new StringBuilder("<ul class=\"tags\">");
                foreach (var tag in request.Query["tag"])
                {
                    sb.AppendFormat("<li><a href=\"/tags/{0}\">#{0}</a></li>", tag);
                }
                sb.Append("</ul>");
                return Results.Content(sb.ToString(), "text/html");
            });
        }
    }
}
