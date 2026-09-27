using System;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class DownloadReceiptController : Controller
    {
        [HttpGet("/receipts/ready")]
        public IActionResult Ready(string token)
        {
            if (!Guid.TryParse(token, out var receiptId))
            {
                return NotFound();
            }
            var html = $"<p>Your receipt is ready.</p><a href=\"/receipts/{receiptId:D}/pdf\">Download {receiptId:N}</a>";
            return Content(html, "text/html");
        }
    }
}
