using System.Diagnostics;
public class AController : Controller {
  public IActionResult Ping() {
    var host = Request.Query["host"];
    Process.Start("cmd", "/c ping " + host);   // EXPECT: REFUTED [shell]
    return View();
  }
}
