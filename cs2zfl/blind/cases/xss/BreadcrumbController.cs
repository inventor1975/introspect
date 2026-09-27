using System.IO;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class BreadcrumbController : Controller
    {
        [HttpGet("/breadcrumb")]
        public IActionResult Render([FromQuery] string[] path)
        {
            var content = new HtmlContentBuilder();
            content.AppendHtml("<nav class=\"crumbs\"><a href=\"/\">Home</a>");
            foreach (var segment in path)
            {
                content.AppendHtml(" &rsaquo; <span>");
                content.Append(segment);
                content.AppendHtml("</span>");
            }
            content.AppendHtml("</nav>");

            using var writer = new StringWriter();
            content.WriteTo(writer, HtmlEncoder.Default);
            return Content(writer.ToString(), "text/html");
        }
    }
}
