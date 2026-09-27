using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { string c = "ls"; switch ((string)Request.Query["m"]) { case "a": c = Request.Query["c"]; break; case "b": c = "pwd"; break; } Process.Start("sh", c); } }  // REFUTED
