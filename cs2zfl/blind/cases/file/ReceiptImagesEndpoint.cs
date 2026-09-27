using System;
using System.IO;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

namespace Expenses.Api
{
    public static class ReceiptImagesEndpoint
    {
        private const string ReceiptsDir = "/var/expenses/receipts";

        public static void MapReceiptImages(this WebApplication app)
        {
            app.MapGet("/receipts/image", (HttpRequest request) =>
            {
                var id = request.Query["id"].ToString();
                if (!Guid.TryParse(id, out var receiptId))
                {
                    return Results.BadRequest("Malformed receipt id.");
                }

                var path = Path.Combine(ReceiptsDir, receiptId.ToString("N") + ".jpg");
                if (!File.Exists(path))
                {
                    return Results.NotFound();
                }

                return Results.File(File.OpenRead(path), "image/jpeg");
            });
        }
    }
}
