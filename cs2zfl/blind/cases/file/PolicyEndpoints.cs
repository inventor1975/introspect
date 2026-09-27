using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace Insurance.Api
{
    public static class PolicyEndpoints
    {
        private const string PolicyDocs = "/app/policy-docs";

        public static void MapPolicyEndpoints(this IEndpointRouteBuilder app)
        {
            app.MapGet("/policy/{product}/wording", (string product) =>
            {
                string? file = product switch
                {
                    "home" => "home-wording-2026.pdf",
                    "motor" => "motor-wording-2026.pdf",
                    "travel" => "travel-wording-2025.pdf",
                    _ => null
                };

                if (file is null)
                {
                    return Results.NotFound();
                }

                return Results.File(Path.Combine(PolicyDocs, file), "application/pdf", file);
            });
        }
    }
}
