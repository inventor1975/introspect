using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Storefront.Api
{
    public enum ShippingSpeed
    {
        Standard,
        Express,
        Overnight
    }

    public static class ShippingSpeedEndpoint
    {
        public static void Map(WebApplication app)
        {
            app.MapGet("/shipping/option", (string speed) =>
            {
                if (!Enum.TryParse<ShippingSpeed>(speed, true, out var parsed) || !Enum.IsDefined(typeof(ShippingSpeed), parsed))
                {
                    parsed = ShippingSpeed.Standard;
                }
                return Results.Content($"<p>Selected shipping: <b>{parsed}</b></p>", "text/html");
            });
        }
    }
}
