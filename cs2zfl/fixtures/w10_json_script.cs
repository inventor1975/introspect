using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

public class BootController : Controller
{
    public IActionResult Boot(string coupon)
    {
        var a = JsonConvert.SerializeObject(new { coupon });            // < > survive
        var b = System.Text.Json.JsonSerializer.Serialize(new { coupon });   // escapes < > & by default
        return Content("<script>var a = " + a + "; var b = " + b + ";</script>", "text/html");
    }
}
