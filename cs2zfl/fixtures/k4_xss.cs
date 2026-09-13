using System.Web;
public class DController : Controller {
  public IActionResult Show() {
    var msg = Request.Form["msg"];
    Response.Write("<h1>" + HttpUtility.HtmlEncode(msg) + "</h1>");  // EXPECT: clean (encoded)
    Response.Write("<h1>" + msg + "</h1>");                          // EXPECT: REFUTED [xss]
    return View();
  }
}
