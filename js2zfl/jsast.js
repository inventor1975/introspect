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

function addFunc(node, name) {
  const params = (node.params || []).map(paramName);
  let body;
  if (node.body && node.body.type === "BlockStatement") body = node.body.body.map(encStmt);
  else if (node.body) body = [{ k: "return", argument: enc(node.body), line: line(node.body) }]; // arrow expr
  else body = [];
  funcs.push({ k: "func", name: name || "", params, body, line: line(node) });
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
    case "TemplateLiteral": return { k: "template", exprs: (n.expressions || []).map(enc) };
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
      return { k: "object", props: (n.properties || []).map(p => (p.value ? enc(p.value) : { k: "nil" })) };
    case "SequenceExpression":
      return { k: "seq", exprs: (n.expressions || []).map(enc) };
    case "TSAsExpression": case "TSNonNullExpression": case "TSTypeAssertion":
    case "ParenthesizedExpression":
      return enc(n.expression);
    case "SpreadElement": return enc(n.argument);
    case "UnaryExpression":
      return { k: "unary", op: n.operator, x: enc(n.argument) };
    case "AssignmentExpression":
      return { k: "assignexpr", left: enc(n.left), right: enc(n.right) };
    case "FunctionExpression": case "ArrowFunctionExpression":
      addFunc(n, n.id ? n.id.name : ""); return { k: "funcref" };
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
        return { name: d.id && d.id.type === "Identifier" ? d.id.name : null, init };
      });
      return { k: "vardecl", decls, line: line(s) };
    }
    case "ExpressionStatement": {
      const e = s.expression;
      if (e.type === "AssignmentExpression") {
        const before = funcs.length;
        const right = enc(e.right);
        if (right.k === "funcref" && funcs.length > before && !funcs[funcs.length - 1].name
            && e.left.type === "Identifier")
          funcs[funcs.length - 1].name = e.left.name;
        return { k: "assign", left: enc(e.left), right, line: line(s) };
      }
      return { k: "exprstmt", x: enc(e), line: line(s) };
    }
    case "IfStatement":
      return { k: "if", test: enc(s.test), body: blockOf(s.consequent),
               els: s.alternate ? encStmt(s.alternate) : null, line: line(s) };
    case "BlockStatement": return { k: "block", body: s.body.map(encStmt) };
    case "ForStatement": case "ForInStatement": case "ForOfStatement":
    case "WhileStatement": case "DoWhileStatement":
      return { k: "for", body: blockOf(s.body), line: line(s) };
    case "ReturnStatement": return { k: "return", argument: enc(s.argument), line: line(s) };
    case "ThrowStatement": return { k: "throw", argument: enc(s.argument), line: line(s) };
    case "TryStatement":
      return { k: "try", body: blockOf(s.block), handler: s.handler ? blockOf(s.handler.body) : [],
               finalizer: s.finalizer ? blockOf(s.finalizer) : [] };
    case "SwitchStatement":
      return { k: "switch", cases: (s.cases || []).map(c => ({ k: "case", body: (c.consequent || []).map(encStmt) })) };
    case "FunctionDeclaration":
      addFunc(s, s.id && s.id.name); return { k: "funcref" };
    case "ClassDeclaration": case "ClassExpression":
      (s.body.body || []).forEach(m => {
        if ((m.type === "ClassMethod" || m.type === "ClassPrivateMethod") && m.body)
          addFunc(m, m.key && (m.key.name || m.key.value));
      });
      return { k: "other" };
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
  const topBody = (ast.program.body || []).map(encStmt);
  funcs.push({ k: "func", name: "<top>", params: [], body: topBody, line: 0 });
  process.stdout.write(JSON.stringify({ k: "file", funcs }));
}
main();
