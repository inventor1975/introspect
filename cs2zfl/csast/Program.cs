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

    static List<object> Params(ParameterListSyntax pl)
    {
        var ps = new List<object>();
        if (pl != null)
            foreach (var p in pl.Parameters)
            {
                var attrs = p.AttributeLists.SelectMany(al => al.Attributes)
                             .Select(a => a.Name.ToString().Split('.').Last()).ToList();
                ps.Add(D("name", p.Identifier.Text, "typ", p.Type?.ToString() ?? "", "attrs", attrs.Cast<object>().ToList()));
            }
        return ps;
    }

    // a lambda: its parameters and its body (a block, or one expression returned)
    static object Lambda(LambdaExpressionSyntax l)
    {
        var ps = new List<object>();
        if (l is ParenthesizedLambdaExpressionSyntax pl) ps = Params(pl.ParameterList);
        else if (l is SimpleLambdaExpressionSyntax sl) ps.Add(D("name", sl.Parameter.Identifier.Text, "typ", sl.Parameter.Type?.ToString() ?? "", "attrs", new List<object>()));
        var body = new List<object>();
        if (l.Block != null) body = l.Block.Statements.Select(Stmt).ToList();
        else if (l.ExpressionBody != null) body.Add(D("k", "return", "argument", Expr(l.ExpressionBody), "line", Line(l.ExpressionBody)));
        return D("k", "lambda", "params", ps, "body", body, "line", Line(l));
    }

    // "text {x} more" as ordered parts: {"s": literal text} / {"e": expression}
    static List<object> Parts(InterpolatedStringExpressionSyntax istr)
    {
        var parts = new List<object>();
        foreach (var c in istr.Contents)
        {
            if (c is InterpolatedStringTextSyntax t) parts.Add(D("s", t.TextToken.ValueText));
            else if (c is InterpolationSyntax i) parts.Add(D("e", Expr(i.Expression)));
        }
        return parts;
    }

    static string ClassBases(SyntaxNode n)
    {
        var cls = n.Ancestors().OfType<ClassDeclarationSyntax>().FirstOrDefault();
        return cls?.BaseList?.Types.Select(t => t.Type.ToString()).Aggregate("", (a, b) => a + "," + b) ?? "";
    }

    static int Line(SyntaxNode n) =>
        n == null ? 0 : n.GetLocation().GetLineSpan().StartLinePosition.Line + 1;

    static Dictionary<string, object> D(params object[] kv)
    {
        var d = new Dictionary<string, object>();
        for (int i = 0; i + 1 < kv.Length; i += 2) d[(string)kv[i]] = kv[i + 1];
        return d;
    }

    static void AddFunc(string name, ParameterListSyntax pl, BlockSyntax body, ArrowExpressionClauseSyntax arrow, int line, bool isAction=false, string owner="", string bases="")
    {
        var ps = Params(pl);
        var stmts = new List<object>();
        if (body != null) foreach (var s in body.Statements) stmts.Add(Stmt(s));
        else if (arrow != null) stmts.Add(D("k", "return", "argument", Expr(arrow.Expression), "line", Line(arrow)));
        Funcs.Add(D("k", "func", "name", name ?? "", "params", ps, "body", stmts, "line", line, "action", isAction,
                    "owner", owner, "bases", bases));
    }

    static object Expr(ExpressionSyntax e)
    {
        switch (e)
        {
            case null: return D("k", "nil");
            case IdentifierNameSyntax id: return D("k", "ident", "name", id.Identifier.Text);
            case LiteralExpressionSyntax lit: return D("k", "lit", "kind", lit.Kind().ToString(), "value", lit.Token.ValueText);
            case MemberAccessExpressionSyntax ma:
                return D("k", "member", "object", Expr(ma.Expression), "prop", ma.Name.Identifier.Text);
            case InvocationExpressionSyntax inv:
                return D("k", "call", "callee", Expr(inv.Expression),
                         "args", inv.ArgumentList.Arguments.Select(a => Expr(a.Expression)).ToList(),
                         "line", Line(inv));
            case ObjectCreationExpressionSyntax oc:
                return D("k", "new", "type", oc.Type.ToString(),
                         "args", (oc.ArgumentList?.Arguments.Select(a => Expr(a.Expression)) ?? Enumerable.Empty<object>()).ToList(),
                         "init", Init(oc.Initializer), "line", Line(oc));
            case ImplicitObjectCreationExpressionSyntax ioc:
                return D("k", "new", "type", "",
                         "args", ioc.ArgumentList.Arguments.Select(a => Expr(a.Expression)).ToList(),
                         "init", Init(ioc.Initializer), "line", Line(ioc));
            case AnonymousObjectCreationExpressionSyntax aoc:
                return D("k", "array", "elts", aoc.Initializers.Select(i => Expr(i.Expression)).ToList());
            case SwitchExpressionSyntax swe:                  // x switch { "a" => .., _ => .. }: one of the arms
                return D("k", "array", "elts", swe.Arms.Select(a => Expr(a.Expression)).ToList(), "switch", true);
            case ConditionalAccessExpressionSyntax ca:        // o?.P / o?.M(..): the value flows from o
                return D("k", "condaccess", "x", Expr(ca.Expression), "then", Expr(ca.WhenNotNull));
            case MemberBindingExpressionSyntax mb:
                return D("k", "member", "object", D("k", "nil"), "prop", mb.Name.Identifier.Text);
            case GenericNameSyntax gn: return D("k", "ident", "name", gn.Identifier.Text);
            case BinaryExpressionSyntax b:
                return D("k", "bin", "op", b.OperatorToken.Text, "x", Expr(b.Left), "y", Expr(b.Right));
            case AssignmentExpressionSyntax asg:
                return D("k", "assignexpr", "op", asg.OperatorToken.Text, "left", Expr(asg.Left), "right", Expr(asg.Right));
            case InterpolatedStringExpressionSyntax istr:
                return D("k", "template", "exprs",
                    istr.Contents.OfType<InterpolationSyntax>().Select(i => Expr(i.Expression)).ToList(), "parts", Parts(istr));
            case ElementAccessExpressionSyntax ea:
                return D("k", "index", "object", Expr(ea.Expression));
            case CastExpressionSyntax cast: return D("k", "cast", "type", cast.Type.ToString(), "x", Expr(cast.Expression));
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
            case LambdaExpressionSyntax lam: return Lambda(lam);
            default: return D("k", "other", "t", e.Kind().ToString());
        }
    }

    // new ContentResult { Content = x, ContentType = "text/html" }: the initialiser's name -> value pairs
    static List<object> Init(InitializerExpressionSyntax init)
    {
        var o = new List<object>();
        if (init == null) return o;
        foreach (var e in init.Expressions)
        {
            if (e is AssignmentExpressionSyntax a) o.Add(D("name", a.Left.ToString(), "value", Expr(a.Right)));
            else o.Add(D("name", "", "value", Expr(e)));
        }
        return o;
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
                    return D("k", "assign", "op", a.OperatorToken.Text, "left", Expr(a.Left), "right", Expr(a.Right), "line", Line(s));
                return D("k", "exprstmt", "x", Expr(es.Expression), "line", Line(s));
            case IfStatementSyntax iff:
                var m = D("k", "if", "test", Expr(iff.Condition), "body", Block(iff.Statement), "line", Line(iff));
                if (iff.Else != null) m["els"] = Stmt(iff.Else.Statement);
                return m;
            case BlockSyntax bl: return D("k", "block", "body", bl.Statements.Select(Stmt).ToList());
            case ForStatementSyntax f: return D("k", "for", "body", Block(f.Statement), "line", Line(f));
            case ForEachStatementSyntax fe:
                return D("k", "for", "left", new List<object> { fe.Identifier.Text }, "iter", Expr(fe.Expression),
                         "body", Block(fe.Statement), "line", Line(fe));
            case WhileStatementSyntax w: return D("k", "for", "test", Expr(w.Condition), "body", Block(w.Statement), "line", Line(w));
            case DoStatementSyntax dz: return D("k", "for", "test", Expr(dz.Condition), "body", Block(dz.Statement), "line", Line(dz));
            case BreakStatementSyntax: return D("k", "break");
            case ContinueStatementSyntax: return D("k", "continue");
            case ReturnStatementSyntax r: return D("k", "return", "argument", Expr(r.Expression), "line", Line(r));
            case ThrowStatementSyntax th: return D("k", "throw", "argument", Expr(th.Expression), "line", Line(th));
            case TryStatementSyntax t:
                var handlers = new List<object>();
                var cparams = new List<object>();
                foreach (var c in t.Catches) {
                    handlers.AddRange(c.Block.Statements.Select(Stmt));
                    if (c.Declaration != null && c.Declaration.Identifier.Text != "") cparams.Add(c.Declaration.Identifier.Text);
                }
                return D("k", "try", "body", t.Block.Statements.Select(Stmt).ToList(), "param", cparams,
                         "handler", handlers, "finalizer", t.Finally != null ? t.Finally.Block.Statements.Select(Stmt).ToList() : new List<object>());
            case SwitchStatementSyntax sw:
                var cases = sw.Sections.Select(sec => (object)D("k", "case",
                    "isdefault", sec.Labels.Any(l => l is DefaultSwitchLabelSyntax),
                    "body", sec.Statements.Select(Stmt).ToList())).ToList();
                return D("k", "switch", "disc", Expr(sw.Expression), "cases", cases, "line", Line(sw));
            case UsingStatementSyntax us:                     // using (var x = ..) { .. }: its header, then its body
                var ub = new List<object>();
                if (us.Declaration != null)
                    ub.Add(D("k", "vardecl", "decls", us.Declaration.Variables.Select(v =>
                        (object)D("name", v.Identifier.Text, "init", v.Initializer != null ? Expr(v.Initializer.Value) : D("k", "nil"))).ToList(), "line", Line(us)));
                else if (us.Expression != null) ub.Add(D("k", "exprstmt", "x", Expr(us.Expression), "line", Line(us)));
                ub.AddRange(Block(us.Statement));
                return D("k", "block", "body", ub);
            case LockStatementSyntax lk: return D("k", "block", "body", Block(lk.Statement));
            case CheckedStatementSyntax ck: return D("k", "block", "body", ck.Block.Statements.Select(Stmt).ToList());
            case LabeledStatementSyntax lb: return Stmt(lb.Statement);
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
                var owner = m.Ancestors().OfType<TypeDeclarationSyntax>().FirstOrDefault()?.Identifier.Text ?? "";
                AddFunc(m.Identifier.Text, m.ParameterList, m.Body, m.ExpressionBody, Line(m), isAction, owner, ClassBases(m));
            }
            // top-level statements (a minimal-API Program.cs): one synthetic function
            var globals = root.ChildNodes().OfType<GlobalStatementSyntax>().Select(g => Stmt(g.Statement)).ToList();
            if (globals.Count > 0)
                Funcs.Add(D("k", "func", "name", "<top>", "params", new List<object>(), "body", globals, "line", 1,
                            "action", false, "owner", "", "bases", ""));
            foreach (var c in root.DescendantNodes().OfType<ConstructorDeclarationSyntax>())
                AddFunc(c.Identifier.Text, c.ParameterList, c.Body, c.ExpressionBody, Line(c));
            var fields = new List<object>();                 // field initialisers: static readonly Regex X = new(..)
            foreach (var fd in root.DescendantNodes().OfType<FieldDeclarationSyntax>())
                foreach (var v in fd.Declaration.Variables)
                    fields.Add(D("name", v.Identifier.Text, "typ", fd.Declaration.Type.ToString(),
                                 "init", v.Initializer != null ? Expr(v.Initializer.Value) : null));
            var types = new List<object>();                  // property types of each class/record (a DTO's enum / int)
            foreach (var td in root.DescendantNodes().OfType<TypeDeclarationSyntax>())
            {
                var props = td.Members.OfType<PropertyDeclarationSyntax>()
                    .Select(pd => (object)D("name", pd.Identifier.Text, "typ", pd.Type.ToString())).ToList();
                if (td is RecordDeclarationSyntax rd && rd.ParameterList != null)
                    props.AddRange(rd.ParameterList.Parameters.Select(pp => (object)D("name", pp.Identifier.Text, "typ", pp.Type?.ToString() ?? "")));
                types.Add(D("name", td.Identifier.Text, "props", props));
            }
            var enums = root.DescendantNodes().OfType<EnumDeclarationSyntax>().Select(e => (object)e.Identifier.Text).ToList();
            Console.Write(JsonSerializer.Serialize(D("k", "file", "funcs", Funcs, "fields", fields, "types", types, "enums", enums)));
        }
        catch (Exception ex)
        {
            Console.Write(JsonSerializer.Serialize(D("k", "file", "error", ex.Message, "funcs", new List<object>())));
        }
    }
}
