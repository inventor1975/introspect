# rb2zfl — Ruby module of the introspect

Sixth language after php/py/java/go/js, on the shared contract (../INTROSPECT-SEMANTICS.md).

## How it parses
`rbast.rb` (Ruby's OWN stdlib Ripper -> compact JSON, zero install) + `rb2zfl.py` (taint analyzer, same
F/T/Z engine). Every def/defs collected flat (+ a synthetic `<top>`). Run: `python3 rb2zfl.py <file.rb>`
· gate: `python3 test_rb2zfl.py`. Needs `ruby` on PATH.

## Slice 1
Sources: params, params[:x], request.params/GET/POST, cookies. Sinks: system/exec/`backticks`/IO.popen
(shell), eval/instance_eval (code), find_by_sql/execute + interpolated where/order/... (sql; where(hash)
is safe), raw/html_safe (xss), File.* (file), open/Net::HTTP (ssrf). String-interpolation + concat,
guards (== / .include? / negated), cross-method + cross-file summaries, branch-join.
