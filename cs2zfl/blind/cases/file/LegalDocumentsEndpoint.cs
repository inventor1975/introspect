using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;

namespace Shop.Api.Endpoints
{
    public static class LegalDocumentsEndpoint
    {
        private const string LegalDir = "/app/legal";

        private static readonly HashSet<string> Published = new HashSet<string>(StringComparer.Ordinal)
        {
            "terms.pdf",
            "privacy.pdf",
            "cookies.pdf",
            "imprint.pdf",
        };

        public static void MapLegalDocuments(this IEndpointRouteBuilder app)
        {
            app.MapGet("/legal/{doc}", (string doc) =>
            {
                if (!Published.Contains(doc))
                {
                    return Results.NotFound();
                }

                var bytes = File.ReadAllBytes(Path.Combine(LegalDir, doc));
                return Results.File(bytes, "application/pdf", doc);
            });
        }
    }
}
