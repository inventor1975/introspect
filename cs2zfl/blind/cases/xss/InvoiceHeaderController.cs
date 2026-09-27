using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class InvoiceHeaderController : Controller
    {
        [HttpGet("/invoices/header")]
        public IActionResult Header(string company, string reference)
        {
            var encodedCompany = WebUtility.HtmlEncode(company);
            var encodedReference = WebUtility.HtmlEncode(reference);
            var html = "<header><h1>" + encodedCompany + "</h1><small>Ref: " + reference + "</small></header>";
            return Content(html, "text/html");
        }
    }
}
