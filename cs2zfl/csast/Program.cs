// csast — thin C# AST -> JSON dumper for cs2zfl (the introspect's C# module).
// Uses Roslyn (Microsoft.CodeAnalysis.CSharp), C#'s OWN parser. Emits a compact typed tree in the same
// schema the other modules use (call/member/ident/lit/bin/template/assign/if/return/new/index...),
// collecting every method/constructor/local-function into a flat `funcs` list. Usage: csast <file.cs>.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

class CsAst
{
    static List<object> Funcs = new List<object>();

    static int Line(SyntaxNode n) =>
        n == null ? 0 : n.GetLocation().GetLineSpan().StartLinePosition.Line + 1;

    static Dictionary<string, object> D(params object[] kv)
    {
        var d = new Dictionary<string, object>();
        for (int i = 0; i + 1 < kv.Length; i += 2) d[(string)kv[i]] = kv[i + 1];
        return d;
    }

    static void AddFunc(string name, ParameterListSyntax pl, BlockSyntax body, ArrowExpressionClauseSyntax arrow, int line, bool isAction=false)
    {
        var ps = new List<object>();
        if (pl != null)
            foreach (var p in pl.Parameters)
            {
                var attrs = p.AttributeLists.SelectMany(al => al.Attributes)
                             .Select(a => a.Name.ToString().Split('.').Last()).ToList();
                ps.Add(D("name", p.Identifier.Text, "typ", p.Type?.ToString() ?? "", "attrs", attrs.Cast<object>().ToList()));
            }
        var stmts = new List<object>();
        if (body != null) foreach (var s in body.Statements) stmts.Add(Stmt(s));
        else if (arrow != null) stmts.Add(D("k", "return", "argument", Expr(arrow.Expression), "line", Line(arrow)));
        Funcs.Add(D("k", "func", "name", name ?? "", "params", ps, "body", stmts, "line", line, "action", isAction));
    }

    static object Expr(ExpressionSyntax e)
    {
        switch (e)
        {
            case null: return D("k", "nil");
            case IdentifierNameSyntax id: return D("k", "ident", "name", id.Identifier.Text);
            case LiteralExpressionSyntax lit: return D("k", "lit", "kind", lit.Kind().ToString());
            case MemberAccessExpressionSyntax ma:
                return D("k", "member", "object", Expr(ma.Expression), "prop", ma.Name.Identifier.Text);
            case InvocationExpressionSyntax inv:
                return D("k", "call", "callee", Expr(inv.Expression),
                         "args", inv.ArgumentList.Arguments.Select(a => Expr(a.Expression)).ToList(),
                         "line", Line(inv));
            case ObjectCreationExpressionSyntax oc:
                return D("k", "new", "type", oc.Type.ToString(),
                         "args", (oc.ArgumentList?.Arguments.Select(a => Expr(a.Expression)) ?? Enumerable.Empty<object>()).ToList(),
                         "line", Line(oc));
            case BinaryExpressionSyntax b:
                return D("k", "bin", "op", b.OperatorToken.Text, "x", Expr(b.Left), "y", Expr(b.Right));
            case AssignmentExpressionSyntax asg:
                return D("k", "assignexpr", "left", Expr(asg.Left), "right", Expr(asg.Right));
            case InterpolatedStringExpressionSyntax istr:
                return D("k", "template", "exprs",
                    istr.Contents.OfType<InterpolationSyntax>().Select(i => Expr(i.Expression)).ToList());
            case ElementAccessExpressionSyntax ea:
                return D("k", "index", "object", Expr(ea.Expression));
            case CastExpressionSyntax cast: return Expr(cast.Expression);
            case ParenthesizedExpressionSyntax par: return Expr(par.Expression);
            case AwaitExpressionSyntax aw: return D("k", "await", "x", Expr(aw.Expression));
            case ConditionalExpressionSyntax c:
                return D("k", "cond", "x", Expr(c.WhenTrue), "y", Expr(c.WhenFalse));
            case PostfixUnaryExpressionSyntax pu: return Expr(pu.Operand);
            case PrefixUnaryExpressionSyntax pr:
                return pr.OperatorToken.Text == "!" ? D("k", "unary", "op", "!", "x", Expr(pr.Operand)) : Expr(pr.Operand);
            case ArrayCreationExpressionSyntax ac:
                return D("k", "array", "elts",
                    (ac.Initializer?.Expressions.Select(x => Expr(x)) ?? Enumerable.Empty<object>()).ToList());
            case ImplicitArrayCreationExpressionSyntax iac:
                return D("k", "array", "elts", (iac.Initializer?.Expressions.Select(x => Expr(x)) ?? Enumerable.Empty<object>()).ToList());
            case ParenthesizedLambdaExpressionSyntax or SimpleLambdaExpressionSyntax:
                return D("k", "funcref");
            default: return D("k", "other", "t", e.Kind().ToString());
        }
    }

    static List<object> Block(StatementSyntax s)
    {
        if (s == null) return new List<object>();
        if (s is BlockSyntax b) return b.Statements.Select(Stmt).ToList();
        return new List<object> { Stmt(s) };
    }

    static object Stmt(StatementSyntax s)
    {
        switch (s)
        {
            case LocalDeclarationStatementSyntax ld:
                var decls = ld.Declaration.Variables.Select(v =>
                    (object)D("name", v.Identifier.Text, "init", v.Initializer != null ? Expr(v.Initializer.Value) : D("k", "nil"))).ToList();
                return D("k", "vardecl", "decls", decls, "line", Line(s));
            case ExpressionStatementSyntax es:
                if (es.Expression is AssignmentExpressionSyntax a)
                    return D("k", "assign", "left", Expr(a.Left), "right", Expr(a.Right), "line", Line(s));
                return D("k", "exprstmt", "x", Expr(es.Expression), "line", Line(s));
            case IfStatementSyntax iff:
                var m = D("k", "if", "test", Expr(iff.Condition), "body", Block(iff.Statement), "line", Line(iff));
                if (iff.Else != null) m["els"] = Stmt(iff.Else.Statement);
                return m;
            case BlockSyntax bl: return D("k", "block", "body", bl.Statements.Select(Stmt).ToList());
            case ForStatementSyntax f: return D("k", "for", "body", Block(f.Statement), "line", Line(f));
            case ForEachStatementSyntax fe: return D("k", "for", "body", Block(fe.Statement), "line", Line(fe));
            case WhileStatementSyntax w: return D("k", "for", "body", Block(w.Statement), "line", Line(w));
            case DoStatementSyntax dz: return D("k", "for", "body", Block(dz.Statement), "line", Line(dz));
            case ReturnStatementSyntax r: return D("k", "return", "argument", Expr(r.Expression), "line", Line(r));
            case ThrowStatementSyntax th: return D("k", "throw", "argument", Expr(th.Expression), "line", Line(th));
            case TryStatementSyntax t:
                var handlers = new List<object>();
                foreach (var c in t.Catches) handlers.AddRange(c.Block.Statements.Select(Stmt));
                return D("k", "try", "body", t.Block.Statements.Select(Stmt).ToList(),
                         "handler", handlers, "finalizer", t.Finally != null ? t.Finally.Block.Statements.Select(Stmt).ToList() : new List<object>());
            case SwitchStatementSyntax sw:
                var cases = sw.Sections.Select(sec => (object)D("k", "case", "body", sec.Statements.Select(Stmt).ToList())).ToList();
                return D("k", "switch", "cases", cases, "line", Line(sw));
            case LocalFunctionStatementSyntax lf:
                AddFunc(lf.Identifier.Text, lf.ParameterList, lf.Body, lf.ExpressionBody, Line(lf));
                return D("k", "funcref");
            default: return D("k", "other", "t", s.Kind().ToString());
        }
    }

    static void Main(string[] args)
    {
        try
        {
            var src = File.ReadAllText(args[0]);
            var tree = CSharpSyntaxTree.ParseText(src);
            var root = tree.GetRoot();
            foreach (var m in root.DescendantNodes().OfType<MethodDeclarationSyntax>())
            {
                var rt = m.ReturnType.ToString();
                bool hasHttp = m.AttributeLists.SelectMany(al => al.Attributes)
                                .Any(a => { var an = a.Name.ToString().Split('.').Last();
                                            return an.StartsWith("Http") || an == "Route"; });
                bool isPublic = m.Modifiers.Any(md => md.Text == "public");
                // an ASP.NET action: returns an ActionResult/…Result (or has an [Http*]/[Route] attr), and is
                // public. A private void helper in a Controller is NOT an action -> its params are not sources.
                bool isAction = hasHttp || (isPublic && (rt.Contains("ActionResult") || rt.EndsWith("Result")
                                || rt.Contains("Result>")));
                AddFunc(m.Identifier.Text, m.ParameterList, m.Body, m.ExpressionBody, Line(m), isAction);
            }
            foreach (var c in root.DescendantNodes().OfType<ConstructorDeclarationSyntax>())
                AddFunc(c.Identifier.Text, c.ParameterList, c.Body, c.ExpressionBody, Line(c));
            Console.Write(JsonSerializer.Serialize(D("k", "file", "funcs", Funcs)));
        }
        catch (Exception ex)
        {
            Console.Write(JsonSerializer.Serialize(D("k", "file", "error", ex.Message, "funcs", new List<object>())));
        }
    }
}
