using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { string H(string s) { return SomeLib.F(s); }
  public void Run() { Process.Start("sh", H(Request.Query["c"])); } }  // OPEN
