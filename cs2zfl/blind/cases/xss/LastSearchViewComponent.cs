using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ViewComponents;
using Microsoft.AspNetCore.Html;

namespace Storefront.Web.ViewComponents
{
    public class LastSearchViewComponent : ViewComponent
    {
        public IViewComponentResult Invoke()
        {
            string last = HttpContext.Request.Query["q"];
            var builder = new HtmlContentBuilder();
            builder.AppendHtml("<aside class=\"recent\">You searched for: <em>");
            builder.Append(last);
            builder.AppendHtml("</em></aside>");
            return new HtmlContentViewComponentResult(builder);
        }
    }
}
