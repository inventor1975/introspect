# go2zfl — Go module of the introspect

Fourth language after php2zfl / py2zfl / java2zfl, on the shared contract (../INTROSPECT-SEMANTICS.md).
Motivating user: Arkady's Go projects.

## How it parses
Go's OWN parser: `goast.go` (a thin go/ast -> JSON dumper) + `go2zfl.py` (the taint analyzer, same
F/T/Z zero-trust engine as the other modules). `go2zfl.py` builds `goast` on first use (needs the Go
toolchain). Run: `python3 go2zfl.py <file.go>`  ·  gate: `python3 test_go2zfl.py`.

## Slice 1
Sources (net/http): FormValue, PostFormValue, FormFile, `r.URL.Query().Get(..)`, `r.Header.Get(..)`.
Sinks: `exec.Command`/`CommandContext` -> shell; `database/sql` Query/Exec/QueryRow/Prepare(+Context) -> sql
(the has-args gate avoids colliding with `url.Query()`). String concat, transparent conversions
(string()/[]byte()/fmt.Sprintf), cross-function + cross-file summaries, branch-join.
Verdicts: REFUTED (tainted reaches sink) / OPEN (не знаю) / clean.
