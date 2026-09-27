using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class DocsPageEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/docs/{section}/{page}", (string section, string page) =>
            {
                var known = section == "api" && page == "overview";
                if (known)
                {
                    return Results.Content("<h1>API overview</h1><p>Start here.</p>", "text/html");
                }
                var notFound = string.Format("<h1>Not found</h1><p>No page <code>{0}/{1}</code> exists.</p>", section, page);
                return Results.Content(notFound, "text/html", null, StatusCodes.Status404NotFound);
            });
        }
    }
}
