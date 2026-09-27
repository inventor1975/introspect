using Microsoft.Extensions.DependencyInjection;
using Storefront.Web.Markup;

namespace Storefront.Web.Startup
{
    public static class ServiceRegistration
    {
        public static IServiceCollection AddStorefrontMarkup(this IServiceCollection services)
        {
            services.AddSingleton<IMarkupRenderer, PlainMarkupRenderer>();
            return services;
        }
    }
}
