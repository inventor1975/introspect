using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.AspNetCore.Mvc;

namespace Kb.Web.Controllers
{
    public class KnowledgeBaseSearchController : Controller
    {
        private const string ArticlesDir = "/app/kb/articles";

        public IActionResult Search(string q)
        {
            var hits = new List<(string Title, string Snippet)>();
            if (string.IsNullOrWhiteSpace(q))
            {
                return View(hits);
            }

            foreach (var file in Directory.EnumerateFiles(ArticlesDir, "*.txt"))
            {
                var text = System.IO.File.ReadAllText(file);
                var idx = text.IndexOf(q, StringComparison.OrdinalIgnoreCase);
                if (idx >= 0)
                {
                    var start = Math.Max(0, idx - 40);
                    var len = Math.Min(text.Length - start, 120);
                    hits.Add((Path.GetFileNameWithoutExtension(file), text.Substring(start, len)));
                }
            }

            ViewBag.Query = q;
            return View(hits);
        }
    }
}
