using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { class O { public string Cmd; } public void Run() { var o = new O(); o.Cmd = Request.Query["c"]; Process.Start("sh", o.Cmd); } }  // REFUTED
