using Microsoft.AspNetCore.Mvc;

public class DocsController : Controller
{
    public IActionResult Read(string page)
    {
        var text = System.IO.File.ReadAllText("/srv/docs/" + page);   // the qualified form, as in controllers
        System.IO.Directory.Delete("/srv/tmp/" + page, true);
        return Ok(text);
    }
}
