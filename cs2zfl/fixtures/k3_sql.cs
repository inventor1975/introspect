using System.Data.SqlClient;
public class CController : Controller {
  public IActionResult Find(string name) {      // bare action param = model-bound source
    var cmd = new SqlCommand("SELECT * FROM u WHERE n='" + name + "'", conn);  // EXPECT: REFUTED [sql]
    cmd.ExecuteReader();
    return View();
  }
}
