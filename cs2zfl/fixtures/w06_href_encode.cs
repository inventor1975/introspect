using System.Web;
using Microsoft.AspNetCore.Mvc;

public class LinkController : Controller
{
    public IActionResult Go(string url, string label)
    {
        var html = "<a href=\"" + HttpUtility.HtmlEncode(url) + "\">" + HttpUtility.HtmlEncode(label) + "</a>";
        return Content(html, "text/html");   // javascript: survives HTML-encoding at an href START
    }
}
