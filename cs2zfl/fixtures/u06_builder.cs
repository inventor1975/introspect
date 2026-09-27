using System.Diagnostics; using Microsoft.AspNetCore.Mvc;
public class C : Controller { public void Run() { var sb = new System.Text.StringBuilder("ls "); sb.Append(Request.Query["c"]); Process.Start("sh", sb.ToString()); } }  // REFUTED
