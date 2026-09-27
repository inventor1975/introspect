# -*- coding: utf-8 -*-
"""rb2zfl — Ruby module of the introspect (slice 1, 2026-09-13).
Parser: Ruby's OWN Ripper (stdlib, zero install) via the `rbast` helper (rbast.rb -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: Rails/Sinatra sources (params, params[:x], request.params/GET/POST, cookies) -> sinks
(system/exec/`backticks`=shell, eval/instance_eval=code, AR where/find_by_sql/execute=sql,
raw/html_safe=xss, File.*=file, open/Net::HTTP=ssrf); string-interpolation + concat propagation,
cross-method + cross-file SUMMARIES, branch-join. Sixth language after php/py/java/go/js.
Slice 2 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base; a method's LAST expression is its return (implicit return was never read, so a helper like
`def clean(x) x.strip end` returned F); block bodies are walked, their params bound to the receiver (they
were not parsed at all); rescue/ensure are parsed and joined; `x += y` joins; `a, b = v` assigns;
`h[k] = v`, `arr << v`, `push` fold into the container; case/when and loops joined; escapers tag one
context; comparisons give F; unmodelled expressions are Z."""
import json, subprocess, os, sys, re as _re
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> shared taint->ZFL->judge adapter
import taintjudge
RBAST = os.path.join(HERE, "rbast.rb")

SOURCE_IDENTS = {"params", "cookies"}                 # Rails bare sources (params[:x], cookies[:x])
REQ_SOURCE_MEMBERS = {"params", "GET", "POST", "query_parameters", "request_parameters",
                      "body", "cookies", "query_string", "referer", "user_agent", "path_parameters",
                      "headers", "raw_post", "fullpath", "original_fullpath", "path", "url", "original_url", "host"}
REQUEST_BASES = {"request", "req"}
# sinks
SHELL_IDENTS = {"system", "exec", "spawn", "syscall"}         # Kernel command execution
CODE_IDENTS = {"eval"}
XSS_IDENTS = {"raw"}                                          # ActionView raw() bypasses escaping
SSRF_IDENTS = {"open"}                                        # Kernel#open(url/"|cmd"): classic Ruby vuln
# raw SQL methods take a SQL string -> always a sink (T=REFUTED, Z=OPEN honest).
SQL_RAW = {"find_by_sql", "execute", "exec_query", "select_all", "select_one", "select_value", "select_values",
           "select_rows", "exec_update", "exec_delete", "exec_insert", "count_by_sql"}
# conditional methods are SAFE with a hash/array (where(active: true)); only a TAINTED STRING is the
# injection -> report ONLY T (suppress Z/OPEN so safe hash-conditions are not noise).
SQL_COND = {"where", "order", "group", "having", "select", "from", "joins", "pluck",
            "find_by", "exists?", "calculate", "reorder", "having", "update_all", "delete_all", "destroy_all",
            "lock", "find_or_create_by", "rewhere"}
CODE_METHODS = {"instance_eval", "class_eval", "module_eval", "eval", "instance_exec", "class_exec"}
DISPATCH = {"send", "public_send", "__send__", "method", "public_method", "try"}   # arg0 names the method to call
CONST_LOOKUP = {"constantize", "safe_constantize"}                               # receiver names a class
TEMPLATE_IDENTS = {"erb", "haml", "slim", "liquid", "markdown", "builder", "nokogiri"}  # Sinatra: a String arg IS the template
ROUTE_VERBS = {"get", "post", "put", "patch", "delete", "options", "head", "link", "unlink"}
FILE_UTILS = {"FileUtils"}
DIR_METHODS = {"glob", "entries", "children", "each_child", "mkdir", "rmdir", "delete", "unlink", "foreach",
               "exist?", "empty?", "[]", "chdir", "rm_rf"}
PATH_OBJ_METHODS = {"read", "write", "open", "readlines", "binread", "binwrite", "delete", "unlink", "rmtree",
                    "children", "each_line", "each_child", "rename", "truncate"}
HTML_UNSAFE_TAGS = {"script", "iframe", "object", "embed", "svg", "math", "style", "link", "meta", "base", "form"}
XSS_MEMBER = {"html_safe"}                                    # x.html_safe -> xss on x's taint
# context-aware escapers: neutralise ONE context, transparent for others
CTX_SANITIZERS = {"html_escape": "xss", "html_escape_once": "xss", "escapeHTML": "xss", "h": "xss",
                  "escape_html": "xss", "escape_javascript": "js", "j": "js", "json_escape": "json",
                  "url_encode": "urlq", "escape": "urlq", "encode_www_form_component": "urlq", "escape_uri": "urlq",
                  "basename": "file", "quote": "sql", "sanitize_sql": "sql", "sanitize_sql_like": "sql",
                  "shellescape": "shell", "escape_shell": "shell"}
# what each escaper family clears, and the marker a template re-decides by position (see _html_ok)
# escape_javascript escapes quotes, newlines and `</` only: a JS string, never HTML (<img onerror> survives)
# json_escape escapes < > & (and U+2028): a JSON value inside <script>, or text; not a quoted attribute
FAM_TAGS = {"xss": {"xss": F, "~html": F}, "js": {"~js": F}, "json": {"~json": F}, "urlq": {"xss": F, "~url": F},
            "file": {"file": F}, "sql": {"sql": F}, "shell": {"shell": F}}
_URL_ATTRS = {"href", "src", "action", "formaction", "xlink:href", "data", "poster", "background", "srcset"}

def _html_pos(prefix):
    """Where a value lands after this literal text: "text", "attr" (quoted, ordinary), "url" (the START of a
    quoted URL attribute), "script", or "bad" (unquoted attribute, event/style attribute, bare tag)."""
    p = prefix.lower()
    if p.rfind("<script") > p.rfind("</script"): return "script"
    if p.rfind("<style") > p.rfind("</style"): return "bad"
    if p.rfind("<") <= p.rfind(">"): return "text"
    m = _re.search(r"""([\w:.-]+)\s*=\s*("[^"]*|'[^']*|[^\s"'>]*)$""", p)
    if not m or not m.group(2) or m.group(2)[0] not in "\"'": return "bad"
    attr, val = m.group(1), m.group(2)[1:]
    if attr.startswith("on") or attr == "style": return "bad"
    if attr in _URL_ATTRS and not val.strip(): return "url"
    return "attr"

def _html_ok(prefix): return _html_pos(prefix) in ("text", "attr")

def _anchored(src):
    """A Ruby regexp constrains the WHOLE string only with \\A .. \\z (^ and $ are LINE anchors in Ruby)."""
    if src is None or not src.startswith("\\A"): return False
    if not (src.endswith("\\z") or src.endswith("\\Z")): return False
    depth, cls, esc = 0, False, False
    for ch in src:
        if esc: esc = False; continue
        if ch == "\\": esc = True
        elif cls: cls = ch != "]"
        elif ch == "[": cls = True
        elif ch == "(": depth += 1
        elif ch == ")": depth -= 1
        elif ch == "|" and depth == 0: return False
    return True

_CLS = {"w": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"), "d": set("0123456789"),
        "h": set("0123456789abcdefABCDEF"), "s": set(" \t\r\n\f\v")}
ALL = None   # "any character"

def _regex_chars(src):
    """Every character a regexp can match (ALL for `.`, a negated class, \\W / \\S / \\D)."""
    out, i, n = set(), 0, len(src)
    while i < n:
        ch = src[i]
        if ch == "\\" and i + 1 < n:
            c = src[i + 1]; i += 2
            if c in "AzZbBGh" and c != "h": continue
            if c in _CLS: out |= _CLS[c]
            elif c in "WDSH": return ALL
            else: out.add(c)
            continue
        if ch == "[":
            j = i + 1; neg = j < n and src[j] == "^"
            if neg: return ALL
            spec = ""
            while j < n and src[j] != "]":
                if src[j] == "\\" and j + 1 < n:
                    c = src[j + 1]
                    if c in _CLS: out |= _CLS[c]
                    elif c in "WDSH": return ALL
                    else: spec += "\\" + c
                    j += 2; continue
                spec += src[j]; j += 1
            out |= _charset(spec); i = j + 1; continue
        if ch == ".": return ALL
        if ch in "^$()?*+{}|,0123456789" and not ch.isalpha():
            i += 1; continue
        out.add(ch); i += 1
    return out

def _regex_spec(src):
    """What an anchored regexp validates: None (every context) or the contexts none of whose dangerous
    characters it can match (\\A[\\w./-]+\\z still lets ../ through: not a file guard)."""
    chars = _regex_chars(src)
    if chars is ALL: return ()
    ok = [cx for cx, bad in DANGER.items() if not (chars & bad)]
    if "code" not in ok and not (chars & CODE_STRUCT):
        ok.append("code?")        # an identifier and nothing else: cannot break out, can still NAME a method -> Z
    return None if len(ok) == len(DANGER) else tuple(sorted(ok))

CODE_STRUCT = set("'\"`#{}()[];$@:,.=+-*/%&|!<>?~^ \t\n\\")

def _charset(spec):
    """The characters a tr/delete-style set names ("a-z0-9_-")."""
    out, i = set(), 0
    while i < len(spec):
        if i + 2 < len(spec) and spec[i + 1] == "-":
            for c in range(ord(spec[i]), ord(spec[i + 2]) + 1): out.add(chr(c))
            i += 3
        else:
            if spec[i] == "\\" and i + 1 < len(spec): i += 1
            out.add(spec[i]); i += 1
    return out
# a context is cleared when the kept characters include none of its dangerous ones
DANGER = {"sql": set("'\";\\"), "xss": set("<>\"'"), "file": set("/\\"), "shell": set(";|&$`<>()'\"\n \\"),
          "code": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'\"`#{}$@:;")}   # no name, no quote: no call
FILE_BASES = {"File", "IO"}
FILE_METHODS = {"open", "read", "write", "new", "readlines", "binread"}
HTTP_BASES = {"Net", "HTTParty", "RestClient", "Faraday"}
HTTP_METHODS = {"get", "post", "get_response", "start", "get_print"}
CONV_IDENTS = {"String", "to_s"}                             # transparent-ish


def _base_ident(n):
    while isinstance(n, dict) and n.get("k") in ("member", "aref"):
        n = n.get("object", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None


_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# calls on a local that store their argument in it
MUTATORS = {"push", "<<", "concat", "append", "store", "merge!", "update", "insert", "unshift", "[]=",
            "add", "prepend"}
# methods whose result carries the receiver's taint
RECV_TRANSPARENT = {"read", "gets", "string", "classify", "camelize", "underscore", "singularize", "pluralize",
                    "titleize", "humanize", "demodulize", "tableize", "dasherize", "to_s", "strip", "lstrip", "rstrip", "chomp", "chop", "downcase", "upcase", "capitalize",
                    "squeeze", "freeze", "dup", "clone", "to_str", "first", "last", "reverse", "flatten",
                    "compact", "uniq", "sort", "values", "keys", "to_a", "to_h", "fetch", "dig", "slice", "[]",
                    "lines", "chars", "split", "encode", "force_encoding", "unpack1", "b", "permit", "require",
                    "to_unsafe_h", "with_indifferent_access", "presence", "try", "map", "select", "reject",
                    "detect", "find", "each_line", "tr", "delete", "succ", "center", "ljust", "rjust"}
# ... and whose ARGUMENTS are content too
ARG_CONTENT = {"gsub", "sub", "gsub!", "sub!", "join", "concat", "+", "%", "format", "sprintf", "insert",
               "prepend", "merge", "tr", "center"}
# results that are numbers / booleans
NUMERIC_RESULT = {"length", "size", "count", "to_i", "to_f", "include?", "nil?", "empty?", "blank?",
                  "present?", "any?", "none?", "all?", "start_with?", "end_with?", "match?", "zero?", "positive?",
                  "eql?", "is_a?", "kind_of?", "respond_to?", "index", "rindex", "between?", "exist?", "exists?"}


def _parts(v): return (v, {}) if isinstance(v, str) else (v[0], dict(v[1]))
def _mk(d, over):
    over = {c: l for c, l in over.items() if l != d}
    return d if not over else (d, tuple(sorted(over.items())))
def _at(v, ctx): return v if isinstance(v, str) else dict(v[1]).get(ctx, v[0])
def _pc(fn, *vs):
    if all(isinstance(v, str) for v in vs): return fn(*vs)
    ctxs = set()
    for v in vs: ctxs |= set(_parts(v)[1])
    return _mk(fn(*[_parts(v)[0] for v in vs]), {c: fn(*[_at(v, c) for v in vs]) for c in ctxs})
def _lj(*ls): return max(ls, key=_RANK.get) if ls else F
def join(*vs):
    vs = [v for v in vs if v is not None]
    if not vs: return F
    return _lj(*vs) if all(isinstance(v, str) for v in vs) else _pc(lambda *ls: _lj(*ls), *vs)
def _compose(a, r): return _pc(lambda x, y: F if x == F else (y if x == T else (Z if y != F else F)), a, r)
def _clean_for(v, ctx):
    d, over = _parts(v); over[ctx] = F; return _mk(d, over)
def _ejoin(*envs):
    out, keys = {}, set()
    for e in envs: keys |= set(e)
    for k in keys: out[k] = join(*[e[k] for e in envs if k in e])
    return out
def _set_env(env, new): env.clear(); env.update(new)

def _tail(body):
    """Ruby returns its last expression: make that an explicit return (copy; the tree is not changed)."""
    if not isinstance(body, list) or not body: return body
    last = body[-1]
    if not isinstance(last, dict): return body
    k = last.get("k"); new = dict(last)
    if k == "exprstmt": return body[:-1] + [{"k": "return", "argument": last.get("x"), "line": last.get("line", 0)}]
    if k == "assign": return body + [{"k": "return", "argument": last.get("right"), "line": last.get("line", 0)}]
    if k == "if":
        new["body"] = _tail(last.get("body"))
        if last.get("els"): new["els"] = _tail([last["els"]])[0] if last["els"].get("k") != "block" else \
            dict(last["els"], body=_tail(last["els"].get("body")))
        return body[:-1] + [new]
    if k == "switch":
        new["cases"] = [dict(c, body=_tail(c.get("body"))) for c in last.get("cases", [])]
        return body[:-1] + [new]
    if k == "block": new["body"] = _tail(last.get("body")); return body[:-1] + [new]
    if k == "try":
        new["body"] = _tail(last.get("body")); new["handler"] = _tail(last.get("handler"))
        return body[:-1] + [new]
    return body


def _sunion(x, y):
    if x is None or y is None: return None
    if x == "Z": return y
    if y == "Z": return x
    return tuple(sorted(set(x) | set(y)))
def _sinter(x, y):
    if x is None: return y
    if y is None: return x
    if x == "Z" or y == "Z": return "Z"
    s = set(x) & set(y)
    return tuple(sorted(s)) if s else False
def _vunion(a, b):
    r = dict(a)
    for k, c in b.items(): r[k] = _sunion(r[k], c) if k in r else c
    return r
def _vinter(a, b):
    r = {}
    for k in set(a) & set(b):
        v = _sinter(a[k], b[k])
        if v is not False: r[k] = v
    return r
def _apply_spec(v, cx):
    if cx is None: return F
    if cx == "Z": return _pc(lambda l: Z if l == T else l, v)
    for c in cx:
        if c.endswith("?"):                                 # "code?": capped at Z for that context
            d, over = _parts(v); over[c[:-1]] = Z if _at(v, c[:-1]) == T else _at(v, c[:-1]); v = _mk(d, over)
        else: v = _clean_for(v, c)
    return v

def _is_hash(n): return isinstance(n, dict) and n.get("k") == "array" and n.get("hash")
def _opt(n, key):
    """The value of `key:` in a trailing options hash argument list, or None."""
    for a in n if isinstance(n, list) else []:
        if _is_hash(a):
            for k2, v in zip(a.get("keys", []), a.get("elts", [])):
                if k2 == key: return v
    return None


class Engine:
    def __init__(self):
        self.summaries = {}   # name -> [summary] (bare names: methods of different classes collide)
        self.funcs = {}
        self.sinks = []
        self._rets = None
        self._dirty = False
        self.consts = {}      # CONSTANT -> its value node (a class/top-level `NAME = ..`)
        self.sequel = False   # the file requires 'sequel': DB[..] / db.fetch(..) are SQL
        self.sinatra = False  # the file requires 'sinatra': route blocks return the response body
        self.nonhtml = False  # the current route declared a non-HTML content type
        self._in_const = False
        self._in_pred = False
        self.urlof = {}       # uri -> the variable it was URI.parse'd from
        self.cur_owner = None # the class/module of the method being walked
        self._cur_env = None

    def _join(self, a, b): return join(a, b)

    # ---------- guards ----------
    def _terminates(self, body):
        if not (isinstance(body, list) and body): return False
        last = body[-1]
        if not isinstance(last, dict): return False
        if last.get("k") in ("return", "branch"): return True
        if last.get("k") == "exprstmt":
            x = last.get("x") or {}
            if x.get("k") == "bin" and x.get("op") in ("and", "&&"): x = x.get("y") or {}   # render .. and return
            if x.get("k") == "other" and x.get("t") in ("return", "return0", "next", "break"): return True
            if x.get("k") == "call" and x.get("callee", {}).get("k") == "ident" \
                    and x["callee"].get("name") in ("raise", "fail", "halt", "redirect", "abort", "exit", "throw", "error!", "not_found"):
                return True
            if x.get("k") == "ident" and x.get("name") in ("halt", "raise", "fail"): return True
        return False

    def _target(self, a):
        """What a check is about: x, params[:k] (a re-read source), through x.to_s / x.downcase / x.strip."""
        if not isinstance(a, dict): return None
        k = a.get("k")
        if k == "ident": return a.get("name")
        if k == "aref":
            key = self._aref_key(a)
            if key: return key
        if k == "member" and a.get("prop") in ("to_s", "downcase", "upcase", "strip", "to_sym", "presence", "squish"):
            return self._target(a.get("object"))
        if k == "call" and a.get("callee", {}).get("k") == "member" and not a.get("args") \
                and a["callee"].get("prop") in ("to_s", "downcase", "upcase", "strip", "to_sym"):
            return self._target(a["callee"].get("object"))
        return None

    def _aref_key(self, a):
        """params[:sort] -> "params[:sort]" (a literal index into an identifier)."""
        o = a.get("object", {}); idx = a.get("index") or []
        if isinstance(o, dict) and o.get("k") == "ident" and len(idx) == 1 and isinstance(idx[0], dict) \
                and idx[0].get("k") == "lit" and idx[0].get("value") is not None:
            return "%s[%s]" % (o.get("name"), idx[0]["value"])
        return None

    def _regex_src(self, n):
        if isinstance(n, dict) and n.get("k") == "regex" and not n.get("interp"): return n.get("src")
        if isinstance(n, dict) and n.get("k") == "ident" and n.get("name") in self.consts:
            return self._regex_src(self.consts[n["name"]])
        return None

    def _is_regexy(self, n):
        return isinstance(n, dict) and (n.get("k") == "regex" or (n.get("k") == "ident" and
                                        isinstance(self.consts.get(n.get("name")), dict) and self.consts[n["name"]].get("k") == "regex"))

    def _is_const(self, n):
        if not isinstance(n, dict): return False
        if n.get("k") == "lit": return True
        return n.get("k") == "ident" and (n.get("name") or "a")[:1].isupper()

    def _regex_check(self, rx, x):
        tg = self._target(x)
        if not tg: return {}, {}
        src = self._regex_src(rx)
        if src is None: return {tg: "Z"}, {}                     # a pattern we cannot read: not proven
        if not _anchored(src): return {}, {}                     # ^..$ are LINE anchors in Ruby: not a guard
        spec = _regex_spec(src)
        return ({tg: spec}, {}) if spec != () else ({}, {})

    def _conds(self, c):
        """(validated when c is true, validated when c is false): target -> None | (ctxs) | "Z"."""
        if not isinstance(c, dict): return {}, {}
        k, op = c.get("k"), c.get("op")
        if k == "unary" and op in ("!", "not"):
            t, e = self._conds(c.get("x")); return e, t
        if k == "bin" and op in ("&&", "and", "||", "or"):
            t1, e1 = self._conds(c.get("x")); t2, e2 = self._conds(c.get("y"))
            return (_vunion(t1, t2), _vinter(e1, e2)) if op in ("&&", "and") else (_vinter(t1, t2), _vunion(e1, e2))
        if k == "bin" and op in ("==", "!=", "eql?", "==="):
            x, y = c.get("x"), c.get("y")
            for a, b in ((x, y), (y, x)):
                tg = self._target(a)
                if tg and self._is_const(b) and not self._is_const(a):
                    v = {tg: None}
                    return (v, {}) if op != "!=" else ({}, v)
            return {}, {}
        if k == "bin" and op in ("=~", "!~"):
            x, y = c.get("x"), c.get("y")
            rx, val = (x, y) if self._is_regexy(x) else (y, x)
            t, e = self._regex_check(rx, val)
            return (t, e) if op == "=~" else (e, t)
        if k == "call" and c.get("callee", {}).get("k") == "member":
            prop = c["callee"].get("prop"); obj = c["callee"].get("object"); args = c.get("args", [])
            if prop in ("include?", "member?", "cover?", "key?", "has_key?", "include_key?", "value?", "any?") and args:
                tg = self._target(args[0])
                if tg and not self._tainted_coll(obj): return {tg: None}, {}
            if prop in ("match?", "match") and args:
                return self._regex_check(obj, args[0]) if self._is_regexy(obj) else \
                    (self._regex_check(args[0], obj) if self._is_regexy(args[0]) else ({}, {}))
            if prop in ("include?", "member?") and args and isinstance(args[0], dict) and args[0].get("k") == "member"                     and args[0].get("prop") == "scheme" and _base_ident(args[0].get("object")) in self.urlof                     and isinstance(obj, dict) and obj.get("k") == "array" and obj.get("elts")                     and all(isinstance(e, dict) and (e.get("value") or "").lower() in ("http", "https", "mailto", "ftp")
                            for e in obj["elts"]):
                src = self.urlof[_base_ident(args[0].get("object"))]      # %w[http https].include?(uri.scheme)
                return {src: ("~scheme",)}, {}
            if prop == "start_with?" and args and self._ends_sep(args[0]):
                tg = self._target(obj)                         # path.start_with?(ROOT + File::SEPARATOR)
                if tg: return {tg: ("file",)}, {}
            if prop in ("include?",) and args and isinstance(args[0], dict) and args[0].get("k") == "lit":
                v = args[0].get("value") or ""
                if ".." in v or "/" in v:                      # x.include?("..") rejects traversal, but NOT an
                    tg = self._target(obj)                     # absolute path, which expand_path / Pathname#join
                    if tg: return {}, {tg: ("file?",)}         # let replace the base: file Z, not clean
        if k == "call":                                    # an own predicate: allowed_material?(name)
            nm = c.get("callee", {}).get("name") if c.get("callee", {}).get("k") == "ident" else c.get("callee", {}).get("prop")
            fns = self.funcs.get(nm) or []
            if fns and not self._in_pred:
                args = c.get("args", []); out = {}
                self._in_pred = True
                try:
                    for i, a in enumerate(args):
                        specs = [self._pred_spec(f, i) for f in fns]
                        tg = self._target(a)
                        if tg and specs and all(sp is not False for sp in specs):
                            sp = specs[0]
                            for x in specs[1:]: sp = _sinter(sp, x)
                            if sp is not False: out[tg] = sp
                finally:
                    self._in_pred = False
                if out: return out, {}
        return {}, {}

    def _ends_sep(self, n):
        if not isinstance(n, dict): return False
        if n.get("k") == "bin" and n.get("op") == "+": return self._ends_sep(n.get("y"))
        if n.get("k") == "ident": return (n.get("full") or "").endswith(("::SEPARATOR", "::ALT_SEPARATOR"))
        if n.get("k") == "lit": return (n.get("value") or "").endswith(("/", "\\"))
        if n.get("k") == "template":
            ps = n.get("parts") or []
            return bool(ps) and "s" in ps[-1] and ps[-1]["s"].endswith(("/", "\\"))
        return False

    def _pred_spec(self, fn, i):
        """What `fn(arg_i)` being true proves about arg i (its last expression is a check on that param)."""
        ps = fn.get("params", [])
        body = fn.get("body") or []
        if i >= len(ps) or not body or not isinstance(body[-1], dict) or body[-1].get("k") != "exprstmt": return False
        tv, _ = self._conds(body[-1].get("x"))
        return tv.get(ps[i], False)

    def _tainted_coll(self, obj):
        """Is the allow-list itself request data? (params[:ids].include?(x) validates nothing)"""
        return self.taint(obj, self._cur_env) == T if self._cur_env is not None else False

    def _validate(self, env, v):
        for n, cx in v.items():
            if n in env or "[" in n: env[n] = _apply_spec(env.get(n, T), cx)

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k in ("lit", "nil", "regex"): return F
        if k == "ident":
            nm = n.get("name")
            if nm in env: return env[nm]
            if nm in SOURCE_IDENTS: return T
            if (nm or "a")[:1].isupper():                  # a constant: the program's own value
                c = self.consts.get(nm)
                if c is not None and not self._in_const:
                    self._in_const = True
                    try: return self.taint(c, {})
                    finally: self._in_const = False
                return F
            if nm in ("true", "false", "nil", "self"): return F
            return Z
        if k == "aref":
            key = self._aref_key(n)
            if key and key in env: return env[key]         # a checked params[:k]
            return self.taint(n.get("object"), env)        # params[:x] -> taint of params
        if k == "bin":
            if n.get("op") in ("==", "!=", "<", ">", "<=", ">=", "=~", "!~", "<=>", "==="):
                return F                                       # a || b / a && b: the value is a or b (joined below)
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))
        if k == "template": return self._template(n, env)
        if k == "array" and not n.get("hash") and len(n.get("elts", [])) >= 2:
            vs = [self.taint(e, env) for e in n["elts"]]      # ["status = ?", x]: the SQL text is the first element
            d, over = _parts(join(*vs)); over["~first"] = _at(vs[0], "sql"); return _mk(d, over)
        if k in ("xstring", "array"):
            return join(*[self.taint(e, env) for e in n.get("exprs", n.get("elts", []))])
        if k == "unary": return F
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "condexpr":
            br = n.get("branches", [])
            if len(br) == 2:                               # c ? a : b / if c then a else b: each branch refined
                saved = self._cur_env; self._cur_env = env
                tv, ev = self._conds(n.get("test")); self._cur_env = saved
                e1, e2 = dict(env), dict(env); self._validate(e1, tv); self._validate(e2, ev)
                return join(self._tail_taint(br[0], e1), self._tail_taint(br[1], e2))
            return join(*[self._tail_taint(b, env) for b in br])
        if k == "member":
            if n.get("prop") in REQ_SOURCE_MEMBERS and _base_ident(n.get("object")) in REQUEST_BASES:
                return T
            prop = n.get("prop")
            if prop in NUMERIC_RESULT: return F
            if prop in RECV_TRANSPARENT: return self.taint(n.get("object"), env)
            if prop in ("to_i", "to_f", "hash", "object_id", "id"): return F
            if prop in ("to_json", "to_sym"): return self.taint(n.get("object"), env)
            if prop == "root" and _base_ident(n.get("object")) == "Rails": return F
            sums = self._sums(prop)
            if sums: return self._apply(sums, [], env)
            return Z
        if k == "call": return self._call_taint(n, env)
        return Z                                          # funcref, other, anything not modelled: unknown

    def _tail_taint(self, stmts, env):
        if not stmts: return F
        st = stmts[-1]
        if not isinstance(st, dict): return Z
        if st.get("k") == "exprstmt": return self.taint(st.get("x"), env)
        if st.get("k") == "assign": return self.taint(st.get("right"), env)
        if st.get("k") == "return": return self.taint(st.get("argument"), env)
        if st.get("k") in ("other", "branch"): return F
        return Z

    def _template(self, n, env):
        parts = n.get("parts")
        vals = [self.taint(e, env) for e in n.get("exprs", [])]
        base = join(*vals) if vals else F
        if not parts: return base
        if all(isinstance(v, str) for v in vals):
            return _mk(base, {"~pfx": F}) if parts[0].get("s") else base   # a fixed leading literal
        d, over = _parts(base)
        for m in ("~html", "~js", "~url"): over.pop(m, None)
        acc, out, i = "", [], 0
        for p in parts:
            if "s" in p: acc += p["s"]; continue
            v = vals[i] if i < len(vals) else Z; i += 1
            pos = _html_pos(acc)
            if _at(v, "~url") == F: out.append(F)                       # CGI.escape: nothing HTML survives
            elif _at(v, "~html") == F and pos == "url" and _at(v, "~scheme") == F:
                out.append(F)                                           # escaped, and its scheme is http(s)
            elif _at(v, "~json") == F and pos in ("script", "text"): out.append(F)
            elif _at(v, "~js") == F and acc.lower().rfind("<script") > acc.lower().rfind("</script") \
                    and acc.rstrip("\x00")[-1:] in ("'", '"'):
                out.append(F)                                           # j(x) inside a quoted JS string
            elif _at(v, "~html") == F: out.append(F if _html_ok(acc) else _parts(v)[0])
            else: out.append(_at(v, "xss"))
            acc += "\x00"
        over["xss"] = _lj(*out) if out else F
        if parts and parts[0].get("s"): over["~pfx"] = F          # a fixed leading literal ("sort_by_#{x}")
        return _mk(d, over)

    def _sums(self, name):
        if self._dirty: self._summarize_all()
        return self.summaries.get(name)

    def _sums_for(self, callee):
        """Summaries a call can reach: RuleEngine.evaluate -> RuleEngine's; a bare call -> this class's
        first; otherwise every method of that name (bare names of different classes collide)."""
        nm = callee.get("name") if callee.get("k") == "ident" else callee.get("prop")
        ss = self._sums(nm)
        if not ss: return ss
        fns = self.funcs.get(nm) or []
        if callee.get("k") == "ident": want = self.cur_owner
        else:
            o = callee.get("object")
            want = o.get("name") if isinstance(o, dict) and o.get("k") == "ident" and (o.get("name") or "a")[:1].isupper() else None
        if want:
            idx = [i for i, f in enumerate(fns) if f.get("owner") == want]
            if idx: return [ss[i] for i in idx if i < len(ss)]
        return ss

    def _apply(self, sums, args, env):
        res = []
        for s in sums:
            if s is None: res.append(Z); continue
            v = s["base"]; n = len(s["ret"])
            for i, a in enumerate(args):
                v = join(v, _compose(self.taint(a, env), s["ret"][min(i, n - 1)] if n else Z))
            res.append(v)
        if not res: return Z
        return res[0] if all(r == res[0] for r in res) else Z

    def _keep_clean(self, v, kept):
        d, over = _parts(v)
        for cx, bad in DANGER.items():
            if not (kept & bad): over[cx] = F
        return _mk(d, over)

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        nm = callee.get("name") if callee.get("k") == "ident" else callee.get("prop")
        if callee.get("k") == "ident" and self._sums(nm):      # the program's own `h` / `escape` wins
            return self._apply(self._sums_for(callee), args, env)   # over the catalogue's escaper of that name
        if nm == "sanitize":                                   # Rails sanitize: safe with its default allow-list
            v = join(*[self.taint(a, env) for a in args[:1]])
            d, over = _parts(v)
            opts = args[1:]
            if not opts: over.update({"xss": F, "~hs": T})
            else:
                bad = self._unsafe_allowlist(opts)
                over.update({"xss": (_at(v, "xss") if bad else (F if bad is False else _pc(lambda l: Z if l == T else l, _at(v, "xss")))), "~hs": T})
            return _mk(d, over)
        if nm == "simple_format":
            v = join(*[self.taint(a, env) for a in args[:1]])
            s_opt = _opt(args, "sanitize")
            d, over = _parts(v)
            over["~hs"] = T
            if not (isinstance(s_opt, dict) and s_opt.get("k") == "ident" and s_opt.get("name") == "false"): over["xss"] = F
            return _mk(d, over)
        if nm in CTX_SANITIZERS:
            d, over = _parts(join(*[self.taint(a, env) for a in args]))
            over.update(FAM_TAGS[CTX_SANITIZERS[nm]]); return _mk(d, over)
        if callee.get("k") == "ident":
            if nm in CONV_IDENTS: return self.taint(args[0], env) if args else F
            if nm in ("Integer", "Float", "Rational", "BigDecimal"): return F
            if nm in TEMPLATE_IDENTS and args and isinstance(args[0], dict) and args[0].get("kind") == "SYM":
                return F                                     # erb :view renders the app's own template file
            if nm in ("Array", "Hash") and args: return self.taint(args[0], env)
            return Z
        if callee.get("k") == "member":
            obj = callee.get("object")
            base = _base_ident(obj)
            if nm in NUMERIC_RESULT: return F
            if nm == "sql" and base == "Arel": return join(*[self.taint(a, env) for a in args])
            if nm in ("parse", "load", "parse!", "safe_load", "decode") and base in ("JSON", "YAML", "Psych", "MultiJson", "Base64", "CGI"):
                return join(*[self.taint(a, env) for a in args[:1]])     # decoded request data is request data
            if nm in ("delete", "tr") and args and isinstance(args[0], dict) and (args[0].get("value") or "").startswith("^") \
                    and (nm == "delete" or (len(args) > 1 and (args[1].get("value") == ""))):
                return self._keep_clean(self.taint(obj, env), _charset(args[0]["value"][1:]))   # keep only this set
            if nm in ("gsub", "gsub!") and len(args) >= 2 and isinstance(args[0], dict) and args[0].get("k") == "regex" \
                    and isinstance(args[1], dict) and args[1].get("k") == "lit" and args[1].get("value") == "":
                m = _re.fullmatch(r"\[\^(.*)\]\+?", args[0].get("src") or "")
                if m: return self._keep_clean(self.taint(obj, env), _charset(m.group(1)))
            if nm in ("expand_path", "absolute_path", "realpath", "cleanpath", "join") and base in ("File", "Pathname", "Rails"):
                return join(*[self.taint(a, env) for a in args], F)
            if nm == "new" and base == "Pathname": return join(*[self.taint(a, env) for a in args])
            if nm in ARG_CONTENT: return join(self.taint(obj, env), *[self.taint(a, env) for a in args])
            if nm == "fetch" and len(args) > 1:            # h.fetch(k, default): the default is returned too
                return join(self.taint(obj, env), *[self.taint(a, env) for a in args[1:]])
            if nm in RECV_TRANSPARENT or nm in CONV_IDENTS: return self.taint(obj, env)
            if nm in ("to_i", "to_f", "id", "to_date"): return F
            if nm in ("to_json", "to_sym"): return self.taint(obj, env)
            sums = self._sums_for(callee)
            if sums: return self._apply(sums, args, env)
        return Z

    def _unsafe_allowlist(self, opts):
        """sanitize(x, tags: .., attributes: ..): True if it lets an event/style attribute or a scripting tag
        through, False if both lists are known and safe, None if we cannot read them."""
        known = True
        for key, bad in (("tags", HTML_UNSAFE_TAGS), ("attributes", None)):
            v = _opt(opts, key)
            if v is None: continue
            if isinstance(v, dict) and v.get("k") == "ident": v = self.consts.get(v.get("name"))
            while isinstance(v, dict) and v.get("k") == "member" and v.get("prop") == "freeze": v = v.get("object")
            if not (isinstance(v, dict) and v.get("k") == "array"): known = False; continue
            names = [(e.get("value") or "").lower() for e in v.get("elts", []) if isinstance(e, dict)]
            if key == "tags" and any(x in bad for x in names): return True
            if key == "attributes" and any(x.startswith("on") or x in ("style", "formaction") for x in names): return True
        return False if known else None

    def _ctx_taint(self, n, env, ctx):
        return _at(self.taint(n, env), ctx)

    # ---------- sinks ----------
    def _iter_nodes(self, n):
        if isinstance(n, dict):
            yield n
            for key, v in n.items():
                if key != "block": yield from self._iter_nodes(v)   # a block is walked on its own
        elif isinstance(n, list):
            for x in n: yield from self._iter_nodes(x)

    def _join_args(self, args, env):
        return join(*[self.taint(a, env) for a in args])

    def _apply_summary(self, call, name, args, env, sums=None):
        sums = [s for s in ((sums if sums is not None else self._sums(name)) or []) if s is not None]
        per = {}
        for s in sums:
            n = len(s["ret"])
            for i, eff in s["sinks"].items():
                for j, a in enumerate(args):
                    if not (j == i or (j > i and i == n - 1)): continue
                    for cx, d in eff.items():
                        x = _at(self.taint(a, env), cx)
                        l = F if x == F else (Z if (x == Z or d != "REFUTED") else T)
                        per.setdefault(cx, {})[id(s)] = _lj(per.get(cx, {}).get(id(s), F), l)
        for cx, by in per.items():
            ls = [by.get(id(s), F) for s in sums]
            l = T if all(x == T for x in ls) else (Z if any(x != F for x in ls) else F)
            self._judge(call, name + "()->sink", cx, l)

    def _sql_arg(self, args):
        """The SQL TEXT of a call: arg0, or the first element of an array form; a hash condition is bound."""
        if not args: return None
        a = args[0]
        if _is_hash(a): return None
        if isinstance(a, dict) and a.get("k") == "array": return (a.get("elts") or [None])[0]
        return a

    def _judge_sql(self, c, prop, args, env, raw):
        q = self._sql_arg(args)
        if q is None: return
        tv = self.taint(q, env)
        v = _at(tv, "~first") if "~first" in _parts(tv)[1] else _at(tv, "sql")   # a bind array built elsewhere
        if raw or (isinstance(q, dict) and q.get("k") in ("template", "bin")) or v == T:
            self._judge(c, prop, "sql", v)          # a var / call condition: only a proven string (T) is judged

    def _leaf_sinks(self, node, env):
        for c in self._iter_nodes(node):
            k = c.get("k")
            if k == "xstring":
                self._judge(c, "`backticks`", "shell", join(*[self.taint(e, env) for e in c.get("exprs", [])]))
            elif k == "member" and c.get("prop") in XSS_MEMBER:
                self._judge(c, c.get("prop"), "xss", self._ctx_taint(c.get("object"), env, "xss"))
            elif k == "member" and c.get("prop") in PATH_OBJ_METHODS and self._is_path_obj(c.get("object")):
                self._judge(c, "Pathname#" + c.get("prop"), "file", self._ctx_taint(c.get("object"), env, "file"))
            elif k == "member" and c.get("prop") in CONST_LOOKUP:
                self._judge(c, c.get("prop"), "code", self.taint(c.get("object"), env))
            elif k == "aref" and self.sequel and _base_ident(c.get("object")) in ("DB", "db") and c.get("index"):
                self._judge_sql(c, "DB[]", c.get("index"), env, True)
            elif k == "call":
                callee = c.get("callee", {}); args = c.get("args", [])
                if callee.get("k") == "ident":
                    nm = callee.get("name")
                    if nm in SHELL_IDENTS and args: self._judge(c, nm, "shell", self._join_args(args, env))
                    elif nm in CODE_IDENTS and args: self._judge(c, nm, "code", self.taint(args[0], env))
                    elif nm in XSS_IDENTS and args: self._judge(c, nm, "xss", self._ctx_taint(args[0], env, "xss"))
                    elif nm in SSRF_IDENTS and args: self._judge(c, nm, "ssrf", self.taint(args[0], env))
                    elif nm in DISPATCH and args and nm != "try":
                        self._judge(c, nm, "code", self._dispatch_level(args[0], env))
                        self._dispatch_targets(c, args[0], args[1:], env)
                    elif nm in ("send_file",) and args: self._judge(c, nm, "file", self._ctx_taint(args[0], env, "file"))
                    elif nm == "render" and args: self._render(c, args, env)
                    elif nm in TEMPLATE_IDENTS and args and not (isinstance(args[0], dict) and args[0].get("kind") == "SYM"):
                        self._judge(c, nm + "(string)", "code", self.taint(args[0], env))
                    elif nm in ("halt", "body") and args and self.sinatra and not self.nonhtml:
                        last = args[-1]
                        if not (isinstance(last, dict) and last.get("k") == "lit" and last.get("kind") == "NUM"):
                            self._judge(c, nm, "xss", self._ctx_taint(last, env, "xss"))
                    elif nm in SQL_RAW and args: self._judge_sql(c, nm, args, env, True)    # implicit self (a model)
                    elif nm in SQL_COND and args: self._judge_sql(c, nm, args, env, False)
                    elif self._sums(nm): self._apply_summary(c, nm, args, env, self._sums_for(callee))
                elif callee.get("k") == "member":
                    prop = callee.get("prop"); obj = callee.get("object"); base = _base_ident(obj)
                    if prop in SQL_RAW and args:
                        self._judge_sql(c, prop, args, env, True)
                    elif self.sequel and base in ("DB", "db") and prop in ("fetch", "run", "execute", "<<") and args:
                        self._judge_sql(c, "Sequel." + prop, args, env, True)
                    elif prop in SQL_COND and args:
                        self._judge_sql(c, prop, args, env, False)
                    elif prop in CODE_METHODS and args:
                        self._judge(c, prop, "code", self.taint(args[0], env))
                    elif prop in DISPATCH and args and prop != "try":
                        self._judge(c, prop, "code", self._dispatch_level(args[0], env))
                        self._dispatch_targets(c, args[0], args[1:], env)
                    elif prop == "const_get" and args:
                        self._judge(c, prop, "code", self.taint(args[0], env))
                    elif prop == "new" and base == "ERB" and args:
                        self._judge(c, "ERB.new", "code", self.taint(args[0], env))
                    elif prop in FILE_METHODS | {"delete", "unlink", "rename", "symlink", "link", "binwrite", "foreach",
                                                 "readlink", "truncate", "chmod", "size", "mtime"} and base in FILE_BASES and args:
                        self._judge(c, base + "." + prop, "file", join(*[self._ctx_taint(a, env, "file") for a in
                                                                         (args if prop in ("rename", "symlink", "link") else args[:1])]))
                    elif base in FILE_UTILS and args:
                        self._judge(c, "FileUtils." + prop, "file", join(*[self._ctx_taint(a, env, "file") for a in args
                                                                           if not _is_hash(a)]))
                    elif base == "Dir" and prop in DIR_METHODS and args:
                        self._judge(c, "Dir." + prop, "file", self._ctx_taint(args[0], env, "file"))
                    elif prop in PATH_OBJ_METHODS and self._is_path_obj(obj):
                        self._judge(c, "Pathname#" + prop, "file", self._ctx_taint(obj, env, "file"))
                    elif prop in HTTP_METHODS and base in HTTP_BASES and args:
                        self._judge(c, base + "." + prop, "ssrf", self.taint(args[0], env))
                    elif prop == "popen" and base == "IO" and args:
                        self._judge(c, "IO.popen", "shell", self.taint(args[0], env))
                    elif prop == "render" and args: self._render(c, args, env)
                    elif self._sums(prop) and prop not in RECV_TRANSPARENT | ARG_CONTENT | NUMERIC_RESULT | MUTATORS:
                        self._apply_summary(c, prop, args, env, self._sums_for(callee))

    def _parsed_from(self, r):
        """uri = URI.parse(target) / URI(target) (possibly inside begin/rescue): -> "target"."""
        for c in self._iter_nodes(r):
            if c.get("k") == "call" and c.get("args") and isinstance(c["args"][0], dict) and c["args"][0].get("k") == "ident":
                cal = c.get("callee", {})
                if (cal.get("k") == "member" and cal.get("prop") == "parse" and _base_ident(cal.get("object")) == "URI")                         or (cal.get("k") == "ident" and cal.get("name") == "URI"):
                    return c["args"][0]["name"]
        return None

    def _dispatch_level(self, a, env):
        """send("sort_by_#{x}"): a fixed name prefix limits the call to the program's own family of methods
        (not system / eval): not proven either way -> at most Z."""
        tv = self.taint(a, env); v = _at(tv, "code")
        if _at(tv, "~pfx") == F or (isinstance(a, dict) and a.get("k") == "template" and (a.get("parts") or [{}])[0].get("s")):
            return Z if v == T else v
        return v

    def _dispatch_targets(self, c, a, rest, env):
        """send("#{kind}_widget", x): every own method the name pattern can reach gets the arguments."""
        if not (isinstance(a, dict) and a.get("k") in ("template", "lit")): return
        parts = a.get("parts") or [{"s": a.get("value") or ""}]
        rx = "".join(_re.escape(p["s"]) if "s" in p else r"\w*" for p in parts)
        for nm in [n for n in self.funcs if _re.fullmatch(rx, n)]:
            if self._sums(nm): self._apply_summary(c, nm, rest, env)

    def _is_path_obj(self, n, depth=0):
        """Pathname.new(x) / Rails.root(.join(..)) / a constant holding one."""
        if depth > 6 or not isinstance(n, dict): return False
        if n.get("k") == "member" and n.get("prop") == "root" and _base_ident(n.get("object")) == "Rails": return True
        if n.get("k") == "ident" and n.get("name") in self.consts: return self._is_path_obj(self.consts[n["name"]], depth + 1)
        if n.get("k") == "call" and n.get("callee", {}).get("k") == "member":
            p = n["callee"].get("prop"); o = n["callee"].get("object")
            if p == "new" and _base_ident(o) == "Pathname": return True
            if p in ("join", "+", "expand_path", "cleanpath", "realpath", "parent", "sub_ext", "freeze"):
                return self._is_path_obj(o, depth + 1)
        if n.get("k") == "member" and n.get("prop") in ("freeze", "cleanpath", "parent"):
            return self._is_path_obj(n.get("object"), depth + 1)
        return False

    def _render(self, c, args, env):
        """Rails render: inline: compiles request text as ERB (code); html: sends an html_safe value raw."""
        v = _opt(args, "inline")
        if v is not None:
            self._judge(c, "render inline:", "code", self.taint(v, env))
            if isinstance(v, dict) and v.get("k") in ("lit", "template"):
                self._erb_raw(c, v.get("value") or "".join(p.get("s", "") for p in v.get("parts", [])))
        h = _opt(args, "html")
        if h is not None:
            t = self.taint(h, env)
            if _at(t, "~hs") == T: self._judge(c, "render html:", "xss", _at(t, "xss"))   # a plain String is escaped

    def _erb_raw(self, c, text):
        """An ERB template's UNESCAPED outputs (<%== x %>, <%= raw x %>, <%= x.html_safe %>) of request data."""
        for m in _re.finditer(r"<%(==|=)\s*(.*?)\s*-?%>", text, _re.S):
            expr = m.group(2)
            raw = m.group(1) == "==" or _re.match(r"raw\b", expr) or expr.endswith(".html_safe")
            if raw and _re.search(r"\b(params|cookies|request\.)", expr):
                self._judge(c, "ERB raw output", "xss", T)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- effects ----------
    def _route_block(self, c, blk, env):
        """A Sinatra route: its block's value IS the response body (text/html unless declared otherwise)."""
        e = dict(env)
        for p in blk.get("params", []): e[p] = T                     # get '/x/:id' do |id|: path captures
        body = _tail(blk.get("body"))
        saved = (self._rets, self.nonhtml)
        self._rets = []
        self.nonhtml = any(self._nonhtml_call(x) for x in self._iter_nodes(blk.get("body")))
        try:
            self._walk(body, e)
            if self._rets and not self.nonhtml:
                self._judge(c, "route body", "xss", _at(join(*self._rets), "xss"))
        finally:
            self._rets, self.nonhtml = saved

    def _nonhtml_call(self, x):
        if not (isinstance(x, dict) and x.get("k") == "call" and x.get("callee", {}).get("k") == "ident"
                and x["callee"].get("name") == "content_type" and x.get("args")): return False
        a = x["args"][0]
        v = (a.get("value") or "") if isinstance(a, dict) else ""
        return bool(v) and "html" not in v

    def _effects(self, node, env):
        """Blocks (walked zero or more times, their params bound to the receiver), and calls that store
        their argument in a local (arr << x, h.store(k, x), arr.push(x))."""
        for c in self._iter_nodes(node):
            if c.get("k") == "bin" and c.get("op") == "<<":
                root, vals = c, []
                while isinstance(root, dict) and root.get("k") == "bin" and root.get("op") == "<<":
                    vals.append(root.get("y")); root = root.get("x")      # out << a << b: both fold into out
                if isinstance(root, dict) and root.get("k") == "ident" and root.get("name") in env:
                    env[root["name"]] = join(env[root["name"]], *[self.taint(v, env) for v in vals])
            if c.get("k") != "call": continue
            callee = c.get("callee", {})
            if callee.get("k") == "member":
                obj = callee.get("object", {}); m = callee.get("prop")
                if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in env:
                    vs = [self.taint(a, env) for a in c.get("args", [])]
                    if m in MUTATORS: env[obj["name"]] = join(env[obj["name"]], *vs)
                    elif m not in RECV_TRANSPARENT and m not in ARG_CONTENT and m not in NUMERIC_RESULT \
                            and any(x != F for x in vs):
                        env[obj["name"]] = join(env[obj["name"]], Z)     # an unknown call MAY store it
            blk = c.get("block")
            if isinstance(blk, dict):
                if callee.get("k") == "ident" and callee.get("name") in ROUTE_VERBS and self.sinatra and c.get("args"):
                    self._route_block(c, blk, env); continue
                if callee.get("k") == "member" and callee.get("prop") == "new" \
                        and isinstance(callee.get("object"), dict) and _base_ident(callee["object"]) == "Tilt":
                    self._judge(c, "Tilt.new { source }", "code", self._tail_taint(blk.get("body"), env))
                bv = self.taint(callee.get("object"), env) if callee.get("k") == "member" else Z
                e1 = dict(env)
                for p in blk.get("params", []): e1[p] = bv
                self._walk(blk.get("body"), e1)
                e2 = _ejoin(env, e1)
                for p in blk.get("params", []): e2[p] = bv
                self._walk(blk.get("body"), e2)
                new = _ejoin(env, e1, e2)
                for p in blk.get("params", []):
                    if p not in env: new.pop(p, None)
                _set_env(env, new)

    # ---------- walk ----------
    def _iter_stmts(self, body):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": yield from self._iter_stmts(st.get("body"))
            elif k == "if":
                yield from self._iter_stmts(st.get("body"))
                if st.get("els"): yield from self._iter_stmts([st["els"]])
            elif k == "for": yield from self._iter_stmts(st.get("body"))
            elif k == "switch":
                for c in st.get("cases", []): yield from self._iter_stmts(c.get("body"))
            else: yield st

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "funcref": continue
            if k == "block": self._walk(st.get("body"), env); continue
            if k == "if":
                self._leaf_sinks(st.get("test"), env); self._effects(st.get("test"), env)
                self._cur_env = env
                tv, ev = self._conds(st.get("test"))
                self._cur_env = None
                e1 = dict(env); e2 = dict(env)
                self._validate(e1, tv); self._validate(e2, ev)
                self._walk(st.get("body"), e1)
                if st.get("els"): self._walk([st["els"]], e2)
                if self._terminates(st.get("body")): _set_env(env, e2)
                elif st.get("els") and st["els"].get("k") == "block" and self._terminates(st["els"].get("body")):
                    _set_env(env, e1)
                else: _set_env(env, _ejoin(e1, e2))
                continue
            if k == "for":
                def head(e):
                    if st.get("test"): self._leaf_sinks(st["test"], e); self._effects(st["test"], e)
                    if st.get("left"):
                        v = self.taint(st.get("iter"), e)
                        for nm in st["left"]: e[nm] = v
                e0 = dict(env)
                e1 = dict(env); head(e1); self._walk(st.get("body"), e1)
                e2 = _ejoin(e0, e1)
                e3 = dict(e2); head(e3); self._walk(st.get("body"), e3)
                _set_env(env, _ejoin(e2, e3))                 # zero or more iterations
                continue
            if k == "switch":                                  # Ruby case: no fallthrough
                outs, has_else = [], False
                for c in st.get("cases", []):
                    if c.get("isdefault"): has_else = True
                    e = dict(env); self._walk(c.get("body"), e); outs.append(e)
                if not has_else: outs.append(dict(env))
                _set_env(env, _ejoin(*outs) if outs else env)
                continue
            if k == "try":
                e_try = dict(env); self._walk(st.get("body"), e_try)
                eh = _ejoin(env, e_try)
                for nm in st.get("param") or []: eh[nm] = Z
                self._walk(st.get("handler"), eh)
                new = _ejoin(e_try, eh) if st.get("handler") else e_try
                self._walk(st.get("finalizer"), new)
                _set_env(env, new); continue
            if k == "assign":
                self._effects(st.get("right"), env)
                left = st.get("left", {}); v = self.taint(st.get("right"), env)
                compound = st.get("op") not in (None, "=")
                if st.get("names"):
                    for nm in st["names"]: env[nm] = v
                elif left.get("k") == "ident":
                    env[left["name"]] = join(env.get(left["name"], Z), v) if compound else v
                    src = self._parsed_from(st.get("right"))
                    if src: self.urlof[left["name"]] = src
                    else: self.urlof.pop(left["name"], None)
                elif left.get("k") in ("member", "aref"):          # h[:k] = v / o.attr = v
                    key = self._aref_key(left) if left.get("k") == "aref" else None
                    if key: env[key] = v                          # params[:sort] = "name": this key now holds v
                    r = _base_ident(left)
                    if r is not None and r not in SOURCE_IDENTS:
                        env[r] = join(env.get(r, F), v if left.get("k") == "aref" else (F if v == F else Z))
            elif k in ("return", "exprstmt"):
                self._effects(st.get("argument") if k == "return" else st.get("x"), env)
                if k == "return" and self._rets is not None:
                    a = st.get("argument")
                    self._rets.append(self.taint(a, env) if isinstance(a, dict) and a.get("k") != "nil" else F)
            self._leaf_sinks(st, env)

    # ---------- passes ----------
    def _summ_of(self, fn):
        params = [p for p in fn.get("params", [])]
        body = _tail(fn.get("body"))
        saved = (self.sinks, self._rets, self.sequel, self.sinatra, self.cur_owner)
        self.sequel, self.sinatra = fn.get("_sequel", False), fn.get("_sinatra", False)
        self.cur_owner = fn.get("owner")
        def run(env):
            self.sinks, self._rets = [], []
            self._walk(body, env)
            got = {}
            for (l, m, ctx, d) in self.sinks:
                key = (l, m, ctx)
                if _DRANK[d] > _DRANK.get(got.get(key), -1): got[key] = d
            return (join(*self._rets) if self._rets else F), got
        try:
            base, bs = run({p: F for p in params if p})
            summ = {"sinks": {}, "passes": set(), "params": params, "base": base, "ret": []}
            for i, p in enumerate(params):
                env = {q: F for q in params if q}
                if p: env[p] = T
                r, ps = run(env)
                summ["ret"].append(r)
                if _at(r, None) == T: summ["passes"].add(i)
                eff = {}
                for key, d in ps.items():
                    if _DRANK[d] > _DRANK.get(bs.get(key), 0) and _DRANK[d] > _DRANK.get(eff.get(key[2]), -1):
                        eff[key[2]] = d
                if eff: summ["sinks"][i] = eff
            return summ
        finally:
            self.sinks, self._rets, self.sequel, self.sinatra, self.cur_owner = saved

    def _requires(self, tree):
        out = set()
        for fn in tree.get("funcs", []):
            if fn.get("name") != "<top>": continue
            for st in fn.get("body") or []:
                x = st.get("x") if isinstance(st, dict) else None
                if isinstance(x, dict) and x.get("k") == "call" and x.get("callee", {}).get("name") in ("require", "require_relative"):
                    for a in x.get("args", []):
                        if isinstance(a, dict) and a.get("value"): out.add(a["value"])
        return out

    def index(self, tree):
        req = self._requires(tree)
        sequel = any(r.startswith("sequel") for r in req) or '"name": "Sequel"' in json.dumps(tree)
        sinatra = any(r.startswith("sinatra") for r in req)
        tree["_sequel"], tree["_sinatra"] = sequel, sinatra
        for fn in tree.get("funcs", []):
            fn["_sequel"], fn["_sinatra"] = sequel, sinatra
            if fn.get("name") in ("<top>",) or (fn.get("name") or "").startswith("<class"):
                for st in fn.get("body") or []:            # NAME = value at the top or in a class body
                    if isinstance(st, dict) and st.get("k") == "assign" and st.get("left", {}).get("k") == "ident" \
                            and (st["left"].get("name") or "a")[:1].isupper():
                        self.consts[st["left"]["name"]] = st.get("right")
            if fn.get("name") and fn["name"] != "<top>" and not fn["name"].startswith("<class"):
                self.funcs.setdefault(fn["name"], []).append(fn)
        self._dirty = True

    def _summarize_all(self):
        self._dirty = False
        fs = {}
        for _ in range(4):
            before = dict(fs)
            for name, fns in self.funcs.items():
                for fn in fns: fs[id(fn)] = self._summ_of(fn)
                self.summaries[name] = [fs.get(id(fn)) for fn in fns]
            if fs == before: break

    def judge(self, tree):
        if self._dirty: self._summarize_all()
        self.sinks = []
        self.sequel, self.sinatra = tree.get("_sequel", False), tree.get("_sinatra", False)
        for fn in tree.get("funcs", []):
            # an entry method's parameter literally named `params` is, by Rails convention, the request params
            env = {p: (T if p in SOURCE_IDENTS else F) for p in fn.get("params", []) if p}
            self._rets = None; self.cur_owner = fn.get("owner")
            self._walk(fn.get("body"), env)
        best, order = {}, []
        for rec in self.sinks:
            key = rec[:3]
            if key not in best: order.append(key); best[key] = rec
            elif _DRANK[rec[3]] > _DRANK[best[key][3]]: best[key] = rec
        self.sinks = [best[key] for key in order if best[key][3] != "EARNED"]
        return self.sinks

    def run(self, tree): self.index(tree); return self.judge(tree)


def parse(path):
    try:
        out = subprocess.run(["ruby", RBAST, path], capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        raise RuntimeError("rb2zfl: `ruby` not found -- Ruby (with stdlib Ripper) is required")
    if out.stdout.strip():
        return json.loads(out.stdout)
    raise RuntimeError("rb2zfl: parser produced no output for %s: %s" % (path, out.stderr.strip()[:200]))

def analyze(path): return Engine().run(parse(path))

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean

def analyze_app(paths):
    e = Engine(); trees = []
    del UNPARSED[:]
    for p in paths:
        t = parse(p)
        if t.get("error"): UNPARSED.append((p, str(t["error"])[:60])); continue
        if t.get("funcs"): trees.append((p, t)); e.index(t)
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
