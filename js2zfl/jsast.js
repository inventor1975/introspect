// jsast — thin JS/TS AST -> JSON dumper for js2zfl (the introspect's JavaScript/TypeScript module).
// Uses @babel/parser (handles JS/JSX/TS/TSX). Emits a compact typed tree of the nodes the taint
// analyzer needs. Every function-like node (declaration, expression, arrow, method) is collected
// FLAT into `funcs` (with a name hint where knowable) so Express inline handlers are analyzed too;
// a synthetic "<top>" func holds module-level statements. Usage: node jsast.js <file>  (JSON to stdout).
"use strict";
const parser = require("@babel/parser");
const fs = require("fs");

const funcs = [];
function line(n) { return n && n.loc ? n.loc.start.line : 0; }

function paramName(p) {
  if (!p) return "";
  if (p.type === "Identifier") return p.name;
  if (p.type === "AssignmentPattern") return paramName(p.left);
  if (p.type === "RestElement") return paramName(p.argument);
  if (p.type === "TSParameterProperty") return paramName(p.parameter);
  return "";
}

// per parameter: [topKey, boundName] pairs of a destructuring pattern ({ query: { name } } -> [["query","name"]])
function patPairs(p) {
  if (!p) return [];
  if (p.type === "AssignmentPattern") return patPairs(p.left);
  if (p.type !== "ObjectPattern") return [];
  const out = [];
  for (const q of p.properties || []) {
    if (q.type === "RestElement") continue;
    const key = q.key && (q.key.name !== undefined ? q.key.name : q.key.value);
    for (const nm of patNames(q.value)) out.push([key, nm]);
  }
  return out;
}

// "Name" or "Name:Arg1,Arg2" for a decorator: @Param('id', ParseUUIDPipe) -> "Param:ParseUUIDPipe"
function decoStr(d) {
  const e = d.expression || {};
  const name = e.callee ? (e.callee.name || (e.callee.property && e.callee.property.name)) : e.name;
  const args = (e.arguments || []).map(a => a.type === "Identifier" ? a.name :
    (a.type === "StringLiteral" ? JSON.stringify(a.value) : (a.type === "NewExpression" && a.callee ? a.callee.name : ""))).filter(Boolean);
  return args.length ? name + ":" + args.join(",") : name;
}
let FILE_DIRECTIVES = [];

function addFunc(node, name, owner) {
  const params = (node.params || []).map(paramName);
  const pdeco = (node.params || []).map(p => ((p.decorators || (p.parameter && p.parameter.decorators) || [])
    .map(decoStr).filter(Boolean)));
  const mdeco = ((owner && owner.decorators) || node.decorators || []).map(decoStr).filter(Boolean);
  const directives = ((node.body && node.body.directives) || []).map(d => d.value && d.value.value).filter(Boolean);
  const ppat = (node.params || []).map(patPairs);
  let body;
  if (node.body && node.body.type === "BlockStatement") body = node.body.body.map(encStmt);
  else if (node.body) body = [{ k: "return", argument: enc(node.body), line: line(node.body) }]; // arrow expr
  else body = [];
  funcs.push({ k: "func", fid: funcs.length, name: name || "", params, pdeco, ppat, mdeco, directives,
               filedirectives: FILE_DIRECTIVES, body, line: line(node) });
  return funcs.length - 1;
}

// every identifier a binding pattern binds: {a, b: {c}}, [x, ...y], d = 1
function patNames(p) {
  if (!p) return [];
  switch (p.type) {
    case "Identifier": return [p.name];
    case "AssignmentPattern": return patNames(p.left);
    case "RestElement": return patNames(p.argument);
    case "ArrayPattern": return (p.elements || []).flatMap(patNames);
    case "ObjectPattern": return (p.properties || []).flatMap(q => patNames(q.type === "RestElement" ? q : q.value));
    case "VariableDeclaration": return (p.declarations || []).flatMap(d => patNames(d.id));
    default: return [];
  }
}

function propName(n) {
  if (n.computed) return enc(n.property);
  const p = n.property;
  return { k: "ident", name: p.name !== undefined ? p.name : p.value };
}

function enc(n) {
  if (!n) return { k: "nil" };
  switch (n.type) {
    case "Identifier": return { k: "ident", name: n.name };
    case "ThisExpression": return { k: "ident", name: "this" };
    case "StringLiteral": return { k: "lit", kind: "STRING", value: n.value };
    case "NumericLiteral": case "BooleanLiteral": case "BigIntLiteral":
      return { k: "lit", kind: "NUM", value: String(n.value) };
    case "NullLiteral": return { k: "lit", kind: "NULL" };
    case "RegExpLiteral": return { k: "lit", kind: "REGEX", value: n.pattern };
    case "TemplateLiteral": return { k: "template", exprs: (n.expressions || []).map(enc),
                                     quasis: (n.quasis || []).map(q => (q.value && q.value.cooked) || "") };
    case "TaggedTemplateExpression": return { k: "template", exprs: (n.quasi.expressions || []).map(enc) };
    case "BinaryExpression": case "LogicalExpression":
      return { k: "bin", op: n.operator, x: enc(n.left), y: enc(n.right) };
    case "CallExpression": case "OptionalCallExpression":
      return { k: "call", callee: enc(n.callee), args: (n.arguments || []).map(enc), line: line(n) };
    case "NewExpression":
      return { k: "new", callee: enc(n.callee), args: (n.arguments || []).map(enc), line: line(n) };
    case "MemberExpression": case "OptionalMemberExpression":
      return { k: "member", object: enc(n.object), property: propName(n), computed: !!n.computed };
    case "AwaitExpression": case "YieldExpression":
      return { k: "await", x: enc(n.argument) };
    case "ConditionalExpression":
      return { k: "cond", x: enc(n.consequent), y: enc(n.alternate) };
    case "ArrayExpression":
      return { k: "array", elts: (n.elements || []).map(enc) };
    case "ObjectExpression":
      return { k: "object", props: (n.properties || []).map(p => (p.value ? enc(p.value) : { k: "nil" })),
               keys: (n.properties || []).map(p => (p.key ? (p.key.name !== undefined ? p.key.name : p.key.value) : null)) };
    case "SequenceExpression":
      return { k: "seq", exprs: (n.expressions || []).map(enc) };
    case "TSAsExpression": case "TSNonNullExpression": case "TSTypeAssertion":
    case "ParenthesizedExpression":
      return enc(n.expression);
    case "SpreadElement": return enc(n.argument);
    case "UnaryExpression":
      return { k: "unary", op: n.operator, x: enc(n.argument) };
    case "AssignmentExpression":
      return { k: "assignexpr", op: n.operator, left: enc(n.left), names: patNames(n.left), right: enc(n.right) };
    case "FunctionExpression": case "ArrowFunctionExpression":
      return { k: "funcref", fid: addFunc(n, n.id ? n.id.name : "") };
    default: return { k: "other", t: n.type };
  }
}

function blockOf(node) {
  if (!node) return [];
  if (node.type === "BlockStatement") return node.body.map(encStmt);
  return [encStmt(node)];
}

function encStmt(s) {
  if (!s) return { k: "other" };
  switch (s.type) {
    case "VariableDeclaration": {
      const decls = (s.declarations || []).map(d => {
        const before = funcs.length;
        const init = enc(d.init);   // enc() adds any function to `funcs`; patch its name from the var
        if (init.k === "funcref" && funcs.length > before && !funcs[funcs.length - 1].name && d.id && d.id.name)
          funcs[funcs.length - 1].name = d.id.name;
        return { name: d.id && d.id.type === "Identifier" ? d.id.name : null, names: patNames(d.id), init };
      });
      return { k: "vardecl", kind: s.kind, decls, line: line(s) };
    }
    case "ExpressionStatement": {
      const e = s.expression;
      if (e.type === "AssignmentExpression") {
        const before = funcs.length;
        const right = enc(e.right);
        if (right.k === "funcref" && funcs.length > before && !funcs[funcs.length - 1].name
            && e.left.type === "Identifier")
          funcs[funcs.length - 1].name = e.left.name;
        return { k: "assign", op: e.operator, left: enc(e.left), names: patNames(e.left), right, line: line(s) };
      }
      return { k: "exprstmt", x: enc(e), line: line(s) };
    }
    case "IfStatement":
      return { k: "if", test: enc(s.test), body: blockOf(s.consequent),
               els: s.alternate ? encStmt(s.alternate) : null, line: line(s) };
    case "BlockStatement": return { k: "block", body: s.body.map(encStmt) };
    case "ForStatement":
      return { k: "for", pre: s.init ? [s.init.type === "VariableDeclaration" ? encStmt(s.init)
                                                   : { k: "exprstmt", x: enc(s.init), line: line(s) }] : [],
               test: enc(s.test), update: enc(s.update), body: blockOf(s.body), line: line(s) };
    case "ForInStatement": case "ForOfStatement":
      return { k: "for", left: patNames(s.left), iter: enc(s.right), body: blockOf(s.body), line: line(s) };
    case "WhileStatement": case "DoWhileStatement":
      return { k: "for", test: enc(s.test), body: blockOf(s.body), line: line(s) };
    case "BreakStatement": return { k: "break" };
    case "ContinueStatement": return { k: "continue" };
    case "ReturnStatement": return { k: "return", argument: enc(s.argument), line: line(s) };
    case "ThrowStatement": return { k: "throw", argument: enc(s.argument), line: line(s) };
    case "TryStatement":
      return { k: "try", body: blockOf(s.block), handler: s.handler ? blockOf(s.handler.body) : [],
               param: s.handler ? patNames(s.handler.param) : [],
               finalizer: s.finalizer ? blockOf(s.finalizer) : [] };
    case "SwitchStatement":
      return { k: "switch", disc: enc(s.discriminant),
               cases: (s.cases || []).map(c => ({ k: "case", isdefault: !c.test, body: (c.consequent || []).map(encStmt) })) };
    case "FunctionDeclaration":
      addFunc(s, s.id && s.id.name); return { k: "funcref" };
    case "ClassDeclaration": case "ClassExpression":
      (s.body.body || []).forEach(m => {
        if ((m.type === "ClassMethod" || m.type === "ClassPrivateMethod") && m.body)
          addFunc(m, m.key && (m.key.name || m.key.value), m);
        // show = (req, res) => { .. }: a class property holding a function is a method too
        if ((m.type === "ClassProperty" || m.type === "ClassPrivateProperty") && m.value &&
            (m.value.type === "ArrowFunctionExpression" || m.value.type === "FunctionExpression"))
          addFunc(m.value, m.key && (m.key.name || m.key.value || (m.key.id && m.key.id.name)));
      });
      return { k: "other" };
    case "ImportDeclaration":
      return { k: "import", source: s.source.value, specs: (s.specifiers || []).map(sp => ({
        local: sp.local.name,
        imported: sp.type === "ImportSpecifier" ? (sp.imported.name || sp.imported.value) :
                  (sp.type === "ImportDefaultSpecifier" ? "default" : "*") })) };
    case "ExportNamedDeclaration": case "ExportDefaultDeclaration":
      return s.declaration ? encStmt(s.declaration) : { k: "other" };
    default: return { k: "other", t: s.type };
  }
}

function main() {
  const src = fs.readFileSync(process.argv[2], "utf8");
  let ast;
  try {
    ast = parser.parse(src, {
      sourceType: "unambiguous",
      errorRecovery: true,
      plugins: ["jsx", "typescript", "classProperties", "classPrivateMethods",
                "optionalChaining", "nullishCoalescingOperator", "objectRestSpread",
                "decorators-legacy", "dynamicImport"],
    });
  } catch (e) {
    process.stdout.write(JSON.stringify({ k: "file", error: String(e), funcs: [] }));
    return;
  }
  FILE_DIRECTIVES = (ast.program.directives || []).map(d => d.value && d.value.value).filter(Boolean);
  const topBody = (ast.program.body || []).map(encStmt);
  funcs.push({ k: "func", name: "<top>", params: [], body: topBody, line: 0 });
  process.stdout.write(JSON.stringify({ k: "file", funcs }));
}
main();
