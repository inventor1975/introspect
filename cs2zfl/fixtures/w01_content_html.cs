using Microsoft.AspNetCore.Mvc;

public class BannerController : Controller
{
    public IActionResult Show(string name)
    {
        return Content("<h1>Hello " + name + "</h1>", "text/html");   // an HTML body
    }

    public IActionResult Plain(string name)
    {
        return Content("Hello " + name);                              // text/plain by default
    }
}
