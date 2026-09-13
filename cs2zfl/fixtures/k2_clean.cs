using System.Diagnostics;
public class BController : Controller {
  public IActionResult Info() {
    var q = Request.Query["q"];                 // read but not sunk
    Process.Start("uptime");                     // constant: EXPECT nothing
    return View();
  }
}
