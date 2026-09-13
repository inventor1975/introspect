# js2zfl — JavaScript/TypeScript module of the introspect

Fifth language after php2zfl / py2zfl / java2zfl / go2zfl, on the shared contract (../INTROSPECT-SEMANTICS.md).
Most significant remaining web surface (Node/Express, npm).

## How it parses
`jsast.js` (@babel/parser -> compact JSON; handles JS/JSX/TS/TSX) + `js2zfl.py` (taint analyzer, same
F/T/Z zero-trust engine). Every function-like node (incl. Express inline arrow handlers) is collected flat,
so handlers are analyzed as entry points. Needs `npm install` (@babel/parser) in this dir.
Run: `python3 js2zfl.py <file.js>`  ·  gate: `python3 test_js2zfl.py`.

## Slice 1
Sources (Express/Koa): req.query/params/body/headers/cookies (receiver-gated on req/request/ctx),
req.param()/get()/header()/cookie(). Sinks: child_process exec/spawn -> shell; eval / new Function -> code;
.query/.execute -> sql; res.send/write/end/render -> xss (gated on res/response/reply); fs.* -> file.
String-concat + template-literal propagation, cross-function + cross-file summaries, branch-join.
