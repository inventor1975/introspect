using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace Analytics.Api.Endpoints
{
    public static class ReportEndpoints
    {
        private const string ReportRoot = "/srv/analytics/reports";

        public static IEndpointRouteBuilder MapReportEndpoints(this IEndpointRouteBuilder app)
        {
            app.MapGet("/reports/{name}", (string name) =>
            {
                var path = Path.Combine(ReportRoot, name);
                return File.Exists(path)
                    ? Results.File(path, "text/csv", Path.GetFileName(path))
                    : Results.NotFound();
            });

            return app;
        }
    }
}
