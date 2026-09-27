using System.Linq;
using Microsoft.AspNetCore.Mvc;

public class HandleController : Controller
{
    public IActionResult Preview(string desired, string raw)
    {
        var handle = new string(desired.Where(char.IsLetterOrDigit).ToArray());
        var quoted = raw.Replace("'", "''");
        return Content("<p>" + handle + "</p><p>" + quoted + "</p>", "text/html");
    }
}
