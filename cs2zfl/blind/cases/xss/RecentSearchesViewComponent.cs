using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ViewComponents;

namespace Storefront.Web.ViewComponents
{
    public class RecentSearchesViewComponent : ViewComponent
    {
        public IViewComponentResult Invoke()
        {
            string last = HttpContext.Request.Query["q"];
            var markup = "<aside class=\"recent\">You searched for: <em>" + last + "</em></aside>";
            return new HtmlContentViewComponentResult(new HtmlString(markup));
        }
    }
}
