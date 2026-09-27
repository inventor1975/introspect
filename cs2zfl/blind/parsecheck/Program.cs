// parsecheck — every corpus file must parse with Roslyn (the parser cs2zfl/csast uses) with NO syntax errors.
// csast itself only reports an exception, never a syntax diagnostic, so this checks what csast would silently accept.
//   dotnet run --project cs2zfl/blind/parsecheck -- <file.cs>...   -> one line per error; exit 1 if any
using System;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

class ParseCheck
{
    static int Main(string[] args)
    {
        int bad = 0;
        foreach (var f in args)
        {
            var tree = CSharpSyntaxTree.ParseText(File.ReadAllText(f), path: f);
            var errs = tree.GetDiagnostics().Where(d => d.Severity == DiagnosticSeverity.Error).ToList();
            if (errs.Count > 0) { bad++; foreach (var d in errs.Take(3)) Console.WriteLine($"PARSE ERROR {d}"); }
        }
        Console.WriteLine($"{args.Length - bad} parsed, {bad} failed");
        return bad > 0 ? 1 : 0;
    }
}
