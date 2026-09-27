using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class RelatedSearchEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/search/related", (string q) =>
            {
                var urlPart = UrlEncoder.Default.Encode(q);
                var text = HtmlEncoder.Default.Encode(q);
                var html = $"<p>Also try: <a href=\"/search?q={urlPart}&amp;sort=new\">{text} (newest)</a></p>";
                return Results.Content(html, "text/html");
            });
        }
    }
}
