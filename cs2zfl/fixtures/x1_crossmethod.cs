using System.Diagnostics;
public class FController : Controller {
  void RunCmd(string c) { Process.Start("cmd", "/c " + c); }  // param -> shell (summary)
  public IActionResult Do() {
    var cmd = Request.Query["cmd"];
    RunCmd(cmd);                                 // EXPECT: REFUTED (cross-method summary)
    return View();
  }
}
