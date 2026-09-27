using System.Net;
using Microsoft.AspNetCore.Mvc;

namespace Storefront.Web.Controllers
{
    public class ThemeWidgetController : Controller
    {
        [HttpGet("/widgets/banner")]
        public ContentResult Banner(string cssClass, string text)
        {
            var cls = WebUtility.HtmlEncode(cssClass);
            var txt = WebUtility.HtmlEncode(text);
            return new ContentResult
            {
                ContentType = "text/html",
                Content = "<div class=" + cls + ">" + txt + "</div>"
            };
        }
    }
}
