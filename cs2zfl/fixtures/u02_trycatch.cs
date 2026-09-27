using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { string c; try { c = Request.Query["c"]; } catch (System.Exception e) { c = "ls"; } Process.Start("sh", c); } }  // REFUTED
