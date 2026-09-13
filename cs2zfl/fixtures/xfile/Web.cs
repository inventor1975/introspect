public class WebController : Controller {
  public IActionResult Show() {
    var id = Request.Query["id"];
    new Dao().Q(id);                             // EXPECT: REFUTED cross-file (Q param -> sql)
    return View();
  }
}
