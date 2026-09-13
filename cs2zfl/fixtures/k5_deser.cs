using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
public class EController : Controller {
  public IActionResult Load() {
    var data = Request.Form["blob"];
    var bf = new BinaryFormatter();
    var obj = bf.Deserialize(new MemoryStream(Convert.FromBase64String(data)));  // EXPECT: REFUTED [deser]
    return View();
  }
}
