using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { Process.Start("sh", Outer(Request.Query["c"])); }
  string Outer(string v) { return Inner(v); } string Inner(string v) { return v; } }  // REFUTED
