using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public static class GreetingEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/welcome", (string name) =>
                Results.Content($"<h1>Welcome back, {name}!</h1><p>Your cart is waiting.</p>", "text/html"));
        }
    }
}
