using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { int n = int.Parse(Request.Query["n"]); Process.Start("sleep", n.ToString()); } }  // nothing
