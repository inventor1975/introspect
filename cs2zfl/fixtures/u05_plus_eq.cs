using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { string c = Request.Query["c"]; c += " -la"; Process.Start("sh", c); } }  // REFUTED
