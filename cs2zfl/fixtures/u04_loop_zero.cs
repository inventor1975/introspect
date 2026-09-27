using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { string c = Request.Query["c"]; foreach (var x in new string[0]) { c = x; } Process.Start("sh", c); } }  // REFUTED
