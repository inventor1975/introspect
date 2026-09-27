using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { string c = Request.Query["c"]; Process.Start("sh", c.Replace("a", "b")); } }  // REFUTED (receiver)
