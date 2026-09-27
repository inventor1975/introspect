# -*- coding: utf-8 -*-
"""go2zfl — Go module of the introspect (slices 1-4 + calibration, 2026-09-12).
Parser: Go's OWN go/ast via the `goast` helper (goast.go -> compact JSON tree). Shared contract
INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: source->sink taint, string-concat propagation, transparent conversions/Sprintf,
cross-function + cross-file SUMMARIES, branch-join. Slice2: receiver-aware sources/sinks (gin
c.Query via *gin.Context type; w.Write via http.ResponseWriter), file/ssrf/xss sinks, mux.Vars,
prepared-statement awareness (stmt from .Prepare passes BOUND params, not SQL). Slice3: package-level
constant resolution. Slice4: guards (equality / map-membership / negated-early-return). Fourth language.
Slice5 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base, returns captured where they happen, OPEN sink effects kept, same-name functions that disagree
-> Z, summaries to a fixpoint; switch cases and loops joined (zero iterations, fallthrough over-
approximated); range binds key/value; `+=` joins; m[k] = v / append / buf.WriteString fold into the
container; escapers tag one context; comparisons and arithmetic are F."""
import json, subprocess, os, sys, re as _re, ast as _pyast
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> the shared taint->ZFL->judge adapter
import taintjudge
GOAST = os.path.join(HERE, "goast")

# sources (net/http): method-name calls + selector chains (X.{Query|Header|Form|PostForm}.Get / mux.Vars)
SOURCE_METHODS = {"FormValue", "PostFormValue", "FormFile", "PathValue", "Referer", "UserAgent"}
GET_CHAIN_RECV = {"Header", "Form", "PostForm", "Trailer"}   # X.Header.Get(..) etc.
# gin: RECEIVER-aware (only when the receiver is typed *gin.Context) -> avoids the c.Query / db.Query collision
GIN_CTX_TYPES = {"gin.Context"}
GIN_SRC = {"Query", "Param", "PostForm", "DefaultQuery", "DefaultPostForm",
           "QueryArray", "PostFormArray", "GetHeader", "GetQuery", "GetPostForm", "QueryMap", "PostFormMap",
           "Cookie", "GetRawData"}
# sinks
#   exec.Command / exec.CommandContext -> shell (any tainted arg)
#   database/sql receiver methods -> sql; value maps method -> QUERY arg index (Context variants: ctx first)
SQL_METHODS = {"Query": 0, "Exec": 0, "QueryRow": 0, "Prepare": 0,
               "QueryContext": 1, "ExecContext": 1, "QueryRowContext": 1, "PrepareContext": 1}
# package-function sinks keyed by (pkg-ident, func) -> ctx; the dangerous arg is arg0
PKG_SINKS = {("os", "Open"): "file", ("os", "OpenFile"): "file", ("os", "ReadFile"): "file",
             ("os", "Create"): "file", ("os", "Remove"): "file", ("os", "RemoveAll"): "file",
             ("ioutil", "ReadFile"): "file", ("ioutil", "WriteFile"): "file",
             ("http", "Get"): "ssrf", ("http", "Post"): "ssrf", ("http", "Head"): "ssrf",
             ("http", "PostForm"): "ssrf", ("template", "HTML"): "xss", ("template", "JS"): "xss",
             ("template", "URL"): "xss"}
XSS_WRITER_TYPES = {"http.ResponseWriter", "gin.ResponseWriter"}   # receiver-typed w.Write(..) -> xss
# round 1 of the blind corpus (2026-09-27): the sinks it showed missing
SQL_METHODS.update({"Where": 0, "Order": 0, "Raw": 0, "Having": 0, "Joins": 0, "Select": 0,
                    "Queryx": 0, "QueryRowx": 0, "MustExec": 0, "NamedExec": 0, "NamedQuery": 0})
SQLX_DEST = {"Get": 1, "Select": 1}               # sqlx db.Get(&dest, query, args..): the query is arg1
NOT_SQL_TYPES = GIN_CTX_TYPES | {"url.URL", "url.Values", "sql.Stmt", "sqlx.Stmt", "http.Request", "http.Header"}
PKG_SINKS.update({("os", "WriteFile"): "file", ("os", "ReadDir"): "file", ("os", "Mkdir"): "file",
                  ("os", "MkdirAll"): "file", ("ioutil", "ReadDir"): "file", ("template", "ParseFiles"): "file",
                  ("template", "ParseGlob"): "file", ("httputil", "NewSingleHostReverseProxy"): "ssrf"})
PKG_SINK_ARGS = {("http", "NewRequest"): ("ssrf", 1), ("http", "NewRequestWithContext"): ("ssrf", 2),
                 ("net", "Dial"): ("ssrf", 1), ("net", "DialTimeout"): ("ssrf", 1),
                 ("http", "ServeFile"): ("file", 2), ("os", "Rename"): ("file", None),
                 ("os", "Symlink"): ("file", None), ("os", "Link"): ("file", None)}
CLIENT_TYPES = {"http.Client"}
CLIENT_METHODS = {"Get", "Post", "Head", "PostForm"}
GIN_FILE = {"File": 0, "FileAttachment": 0, "SaveUploadedFile": 1}
FPRINT = {"Fprintf": 1, "Fprint": 0, "Fprintln": 0}      # value = index of the format arg after w (1) or none (0)
PKG_CLEAN = {("os", "Getenv"), ("os", "LookupEnv")}      # deployment configuration, not request data
NUM_TYPES = {"int", "int8", "int16", "int32", "int64", "uint", "uint8", "uint16", "uint32", "uint64",
             "float32", "float64", "bool", "time.Duration", "time.Time"}
# boolean predicates: `if !P(x) { return }` validates x after the if; `if P(x) {..}` inside
PRED_FUNCS = {"MatchString", "Match", "IsLocal", "HasPrefix", "HasSuffix", "Contains", "ContainsFunc"}
_FLAGS = _re.compile(r'^\(\?[a-zA-Z]+\)')

def _anchored(p):
    """^...$ (or \\A..\\z) with no top-level alternation: the regexp constrains the WHOLE value."""
    p = _FLAGS.sub("", p or "")
    if not (p.startswith("^") or p.startswith("\\A")): return False
    if not ((p.endswith("$") and not p.endswith("\\$")) or p.endswith("\\z")): return False
    depth, cls, esc = 0, False, False
    for ch in p:
        if esc: esc = False; continue
        if ch == "\\": esc = True
        elif cls: cls = ch != "]"
        elif ch == "[": cls = True
        elif ch == "(": depth += 1
        elif ch == ")": depth -= 1
        elif ch == "|" and depth == 0: return False
    return True
# parsers that fail on anything but their format: `v, err := strconv.Atoi(x); if err != nil { return }` validates x
VALIDATING_PARSERS = {("strconv", n) for n in ("Atoi", "ParseInt", "ParseUint", "ParseFloat", "ParseBool")} | \
    {("uuid", "Parse"), ("uuid", "MustParse"), ("netip", "ParseAddr"), ("time", "Parse"), ("time", "ParseDuration")}
REQ_FIELDS = {"URL": "url.URL", "Form": "url.Values", "PostForm": "url.Values", "Header": "http.Header",
              "Body": "io.ReadCloser"}
REQ_TAINTED = {"Host", "RequestURI"}                     # r.Host etc.: request data
URL_TAINTED = {"Path", "RawQuery", "RawPath", "Fragment", "Host"}
# context-aware escapers: neutralise ONE context, transparent for others (like php2zfl)
CTX_SANITIZERS = {"EscapeString": "xss", "HTMLEscapeString": "xss", "JSEscapeString": "js",
                  "QueryEscape": "urlq", "PathEscape": "urlp", "Base": "file"}
# what each escaper family clears where it stands, and the marker that lets a later concatenation
# re-decide by position (html escaping in an href start / unquoted attribute / script does not protect;
# a url-escaped value protects ssrf only after a fixed scheme://host/)
# QueryEscape leaves no quote, angle, colon or slash: safe in any HTML position; PathEscape keeps ':' so an
# href START can still be javascript:%2E..; JSEscapeString is for a JS string (and harmless in text)
FAM_TAGS = {"xss": {"xss": F, "~html": F}, "js": {"xss": F, "~js": F},
            "urlq": {"file": F, "~url": F, "xss": F}, "urlp": {"file": F, "~url": F, "xss": F, "~html": F},
            "file": {"file": F}}
UNESCAPERS = {"QueryUnescape", "PathUnescape", "UnescapeString", "Unescape"}   # undo an earlier check
BIND_SAFE_TAGS = ("alphanum", "alpha", "numeric", "number", "uuid", "oneof=", "boolean", "hexadecimal", "ulid")
CONV_IDENTS = {"string", "byte", "rune"}          # string(x) etc: transparent conversions

_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# package functions whose result carries their arguments' taint (strings.Join, url.QueryUnescape, ...)
PKG_TRANSPARENT = {"Join", "Replace", "ReplaceAll", "TrimSpace", "Trim", "TrimLeft", "TrimRight", "TrimPrefix",
                   "TrimSuffix", "ToLower", "ToUpper", "Title", "Split", "SplitN", "Fields", "Repeat",
                   "QueryUnescape", "PathUnescape", "DecodeString", "EncodeToString", "Quote", "Unquote",
                   "NewBufferString", "NewReader", "Errorf", "New", "Clean", "Dir", "Ext", "Abs",
                   "ReadAll", "Sprint", "Sprintf", "Sprintln", "JoinPath", "NewDecoder"}
PKG_TRANSPARENT_PAIRS = {("url", "Parse"), ("url", "ParseRequestURI")}
HTML_SANITIZER_TYPES = {"bluemonday.Policy"}     # p.Sanitize(x): an HTML sanitiser (tags the xss family)
# results that are numbers / booleans
NUMERIC_RESULT = {"len", "cap", "Atoi", "ParseInt", "ParseUint", "ParseFloat", "ParseBool", "Itoa", "FormatInt",
                  "FormatUint", "FormatBool", "Contains", "HasPrefix", "HasSuffix", "Index", "Count",
                  "EqualFold", "Compare", "MatchString"}
# methods that store their argument in the receiver
MUTATORS = {"WriteString", "Write", "WriteByte", "WriteRune", "Add", "Set", "Store", "Push"}

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
    for k in keys:
        if "." in k and not all(k in e for e in envs): continue   # a field known on one path only: from its root
        out[k] = join(*[e[k] for e in envs if k in e])
    return out
def _set_env(env, new): env.clear(); env.update(new)
def _root(n):
    while isinstance(n, dict) and n.get("k") in ("index", "sel", "star", "slice"): n = n.get("x", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None


_VERB = _re.compile(r'%[-+# 0-9.*\[\]]*[a-zA-Z%]')
_URL_ATTRS = {"href", "src", "action", "formaction", "xlink:href", "data", "poster", "background", "srcset"}

def _litstr(n):
    if not (isinstance(n, dict) and n.get("k") == "lit" and n.get("kind") == "STRING"): return None
    v = n.get("value", "")
    if v.startswith("`"): return v[1:-1]
    try: return _pyast.literal_eval(v)
    except Exception: return v[1:-1]

def _html_ok(prefix):
    """Does HTML-escaping protect a value placed right after this literal text? Text content and a quoted
    ordinary attribute: yes. Script/style, an unquoted attribute, an event/style attribute, the START of a
    URL attribute (javascript: survives), a bare tag position: no."""
    p = prefix.lower()
    if p.rfind("<script") > p.rfind("</script") or p.rfind("<style") > p.rfind("</style"): return False
    if p.rfind("<") <= p.rfind(">"): return True
    m = _re.search(r'([\w:.-]+)\s*=\s*("[^"]*|\'[^\']*|[^\s"\'>]*)$', p)
    if not m or not m.group(2) or m.group(2)[0] not in "\"'": return False
    attr, val = m.group(1), m.group(2)[1:]
    if attr.startswith("on") or attr == "style": return False
    if attr in _URL_ATTRS and not val.strip(): return False
    return True

_CLS = {"w": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"), "d": set("0123456789"),
        "s": set(" \t\r\n\f\v")}
# a context is cleared by an anchored regexp that can match none of its dangerous characters
DANGER = {"sql": set("'\";\\"), "xss": set("<>\"'"), "file": set("/\\"), "shell": set(";|&$`<>()'\"\n \\"),
          "ssrf": set("/:@\\?#%.")}

def _charset(spec):
    out, i = set(), 0
    while i < len(spec):
        if i + 2 < len(spec) and spec[i + 1] == "-":
            out |= {chr(c) for c in range(ord(spec[i]), ord(spec[i + 2]) + 1)}; i += 3
        else:
            if spec[i] == "\\" and i + 1 < len(spec): i += 1
            out.add(spec[i]); i += 1
    return out

def _regex_chars(src):
    r"""Every character a regexp can match; None for `.`, a negated class, \W \S \D."""
    out, i, n = set(), 0, len(src)
    while i < n:
        ch = src[i]
        if ch == "\\" and i + 1 < n:
            c = src[i + 1]; i += 2
            if c in "Azb": continue
            if c in _CLS: out |= _CLS[c]
            elif c in "WDS": return None
            else: out.add(c)
            continue
        if ch == "[":
            j = i + 1
            if j < n and src[j] == "^": return None
            spec = ""
            while j < n and src[j] != "]":
                if src[j] == "\\" and j + 1 < n:
                    c = src[j + 1]
                    if c in _CLS: out |= _CLS[c]
                    elif c in "WDS": return None
                    else: spec += "\\" + c
                    j += 2; continue
                spec += src[j]; j += 1
            out |= _charset(spec); i = j + 1; continue
        if ch == ".": return None
        if ch in "^$()?*+{}|,0123456789":
            i += 1; continue
        out.add(ch); i += 1
    return out

def _regex_spec(src):
    r"""What an anchored regexp validates: None (every context) or the contexts it can say nothing
    dangerous in (^[\w./-]+$ is anchored and still lets ../ through: not a file guard)."""
    chars = _regex_chars(_FLAGS.sub("", src))
    if chars is None: return ()
    ok = tuple(sorted(cx for cx, bad in DANGER.items() if not (chars & bad)))
    return None if len(ok) == len(DANGER) else ok

_ACTION = _re.compile(r'\{\{-?\s*(.*?)\s*-?\}\}', _re.S)
_TMPL_CTRL = ("if ", "else", "end", "range ", "with ", "define ", "template ", "block ", "break", "continue", "/*")

def _tmpl_all_escaped(src):
    """text/template: does every printing action pass through the html / js / urlquery builtin?"""
    for m in _ACTION.finditer(src):
        a = m.group(1)
        if a.startswith(_TMPL_CTRL) or a in ("else", "end", "break", "continue"): continue
        if not _re.search(r'(^|[|\s(])(html|js|urlquery)(\s|$|\))', a): return False
    return True

def _fixed_host(prefix):
    i = prefix.find("://")
    return i >= 0 and any(c in prefix[i + 3:] for c in "/?#")

def _callee_name(fun):
    if not isinstance(fun, dict): return None
    if fun.get("k") == "ident": return fun.get("name")
    if fun.get("k") == "sel": return fun.get("sel")
    return None

# a validation spec: None = every context clean; a tuple of contexts cleaned; "Z" = no longer proven tainted
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
    for c in cx: v = _clean_for(v, c)
    return v

class Engine:
    def __init__(self):
        self.summaries = {}
        self.sinks = []
        self.vt = {}          # per-function: var/param name -> type name (receiver-aware sources & sinks)
        self.prepared = set() # per-function: vars assigned from .Prepare(..) -> their Query/Exec pass BOUND params
        self.pg = {}          # package name -> its package-level facts (Go scope: globals are per package)
        self.cur_pkg = None
        self.funcs = {}       # name -> [func node] (bare names: methods of different types collide)
        self._rets = None
        self._dirty = False
        self.stypes = {}      # struct name -> {field: type}
        self.sfields = {}     # struct name -> [field node with tag]
        self.user_pkgs = set()        # package names of the analysed files (their calls may use summaries)
        self.prep_fields = set()      # struct fields assigned a prepared statement anywhere
        self.cur_imports = {}         # current file: import name -> path
        self.cur_params = set()       # current function's params/receiver: their fields are unknown (Z)
        self.ctype = None             # current handler's declared Content-Type: None | "html" | "other"
        self.errsrc = {}              # err var -> {var: spec} a validating parser / helper checked
        self.cur_body = None
        self.hostalias = {}           # host := strings.ToLower(u.Hostname()): a check on host checks u's host

    def _pgd(self):
        return self.pg.setdefault(self.cur_pkg, {"env": {}, "types": {}, "const": {}, "vals": {}})
    genv = property(lambda self: self._pgd()["env"])      # package-level const/var taint
    gtypes = property(lambda self: self._pgd()["types"])  # package var -> type
    gconst = property(lambda self: self._pgd()["const"])  # package const -> its value node
    gvals = property(lambda self: self._pgd()["vals"])    # package var -> its initializer node

    def _cands(self, fun):
        """(name, indexes into self.funcs[name]) a call can reach: an unqualified call stays in this package,
        pkg.F in that package, a method by its receiver type when known."""
        nm = _callee_name(fun); fns = self.funcs.get(nm) or []
        if not fns or not isinstance(fun, dict): return nm, []
        if fun.get("k") == "ident":
            return nm, [i for i, f in enumerate(fns) if not f.get("recv") and f.get("_pkg") == self.cur_pkg]
        if fun.get("k") == "sel":
            if self._pkg(fun.get("x")) is not None:
                pk = fun["x"]["name"]
                return nm, [i for i, f in enumerate(fns) if not f.get("recv") and f.get("_pkgname") == pk]
            rt = (self._typ(fun.get("x")) or "").split(".")[-1]
            ms = [i for i, f in enumerate(fns) if f.get("recv")]
            typed = [i for i in ms if (fns[i]["recv"][0].get("typ") or "").split(".")[-1] == rt] if rt else []
            return nm, typed or ms
        return nm, []

    def _cand_fns(self, fun):
        nm, idx = self._cands(fun)
        return [self.funcs[nm][i] for i in idx]

    def _sums_of(self, fun):
        nm, idx = self._cands(fun)
        if not idx: return None
        ss = self._sums(nm) or []
        return [ss[i] for i in idx if i < len(ss)]

    # ---------- whole-program facts ----------
    def _nodes(self, n):
        if isinstance(n, dict):
            yield n
            for v in n.values(): yield from self._nodes(v)
        elif isinstance(n, list):
            for x in n: yield from self._nodes(x)

    def _all_decls(self, body):
        out = set()
        for d in self._nodes(body):
            k = d.get("k")
            if k == "assign" and d.get("tok") == ":=":
                out |= {l.get("name") for l in d.get("lhs", []) if isinstance(l, dict) and l.get("k") == "ident"}
            elif k == "var":
                for vd in d.get("vars", []): out |= set(vd.get("names", []))
            elif k == "range" and d.get("tok") == ":=":
                out |= {_root(d.get(p)) for p in ("key", "value") if d.get(p)}
            elif k == "funclit":
                out |= {p.get("name") for p in d.get("params", [])}
        return out

    def _all_writes(self, body):
        for d in self._nodes(body):
            if d.get("k") == "assign" and d.get("tok") != ":=":
                for l in d.get("lhs", []):
                    r = _root(l)
                    if r: yield r

    def prepare(self, trees):
        for t in trees:
            self.cur_imports = {i["name"]: i["path"] for i in t.get("imports", [])}
            self.cur_pkg = t.get("_pkey", t.get("pkg"))
            if t.get("pkg"): self.user_pkgs.add(t["pkg"])
            for ty in t.get("types", []):
                self.stypes.setdefault(ty["name"], {}).update(
                    {f["name"]: f["typ"] for f in ty.get("fields", []) if f.get("name") and f.get("typ")})
                self.sfields.setdefault(ty["name"], []).extend(f for f in ty.get("fields", []) if f.get("name"))
            for gl in t.get("globals", []):
                nm, val = gl.get("name"), gl.get("value") or {}
                if not nm or nm == "_": continue
                ty = gl.get("typ") or self._typ(val)
                if ty: self.gtypes[nm] = ty
                self.gvals[nm] = val
                if gl.get("const"): self.gconst[nm] = val
        self.cur_imports = {}
        for pk in {t.get("_pkey", t.get("pkg")) for t in trees}:
            self.cur_pkg = pk
            self._pgd()["env"] = self.globals_env([t for t in trees if t.get("_pkey", t.get("pkg")) == pk])
        for t in trees: self.index(t)
        for fns in list(self.funcs.values()):
            for fn in fns:
                for d in self._nodes(fn.get("body")):
                    if d.get("k") == "assign" and any(isinstance(r, dict) and r.get("k") == "call" and
                            r.get("fun", {}).get("sel") in ("Prepare", "PrepareContext", "Preparex") for r in d.get("rhs", [])):
                        self.prep_fields |= {l.get("sel") for l in d.get("lhs", []) if isinstance(l, dict) and l.get("k") == "sel"}
                    if d.get("k") == "kv" and isinstance(d.get("value"), dict) and d["value"].get("k") == "call" \
                            and d["value"].get("fun", {}).get("sel") in ("Prepare", "PrepareContext", "Preparex") \
                            and d.get("key", {}).get("k") == "ident":
                        self.prep_fields.add(d["key"]["name"])
                self.cur_pkg = fn.get("_pkg")
                if fn.get("name") in ("init", "main") and not fn.get("recv"): continue   # startup configuration
                local = {p.get("name") for p in fn.get("params", []) + fn.get("recv", [])} | self._all_decls(fn.get("body"))
                for nm in set(self._all_writes(fn.get("body"))):
                    # a package var WRITTEN by a handler is state: what it holds when read is not its initializer
                    if nm in self.genv and nm not in local and nm not in self.gconst:
                        self.genv[nm] = join(self.genv[nm], Z)

    def globals_env(self, trees):
        """Taint of package-level const/var declarations (2 passes for const-of-const chains)."""
        g = {}
        pairs = [(gl.get("name"), gl.get("value")) for t in trees for gl in t.get("globals", [])]
        for _ in range(2):
            for name, val in pairs:
                if name and name != "_": g[name] = self.taint(val, g)
        return g

    def _join(self, a, b): return join(a, b)

    # ---------- types ----------
    def _pkg(self, n):
        """The import path when n is a package identifier (not shadowed by a local), else None."""
        if isinstance(n, dict) and n.get("k") == "ident" and n.get("name") in self.cur_imports \
                and n.get("name") not in self.vt:
            return self.cur_imports[n["name"]]
        return None

    def _call_types(self, c):
        fun = c.get("fun", {}); nm = _callee_name(fun)
        if fun.get("k") == "sel":
            path = self._pkg(fun.get("x"))
            if path is not None:
                if path == "net/http" and nm in ("NewRequest", "NewRequestWithContext"): return ["http.Request", "error"]
                if path == "net/http" and nm in ("Get", "Post", "Head", "PostForm"): return ["http.Response", "error"]
                if path in ("html/template", "text/template") and nm in ("New", "Must", "ParseFiles", "ParseGlob", "ParseFS"):
                    return ["template.Template", "error"]
                if path == "net/url" and nm in ("Parse", "ParseRequestURI"): return ["url.URL", "error"]
                if "bluemonday" in path: return ["bluemonday.Policy"]
                return []
            if self._is_template(fun.get("x")) and nm in ("Parse", "Funcs", "Delims", "Option", "New", "Lookup", "Clone"):
                return ["template.Template", "error"]
            if nm == "Query" and self._typ(fun.get("x")) == "url.URL": return ["url.Values"]
            if self._typ(fun.get("x")) in HTML_SANITIZER_TYPES and nm in ("AllowElements", "AllowAttrs", "RequireNoFollowOnLinks"):
                return ["bluemonday.Policy"]
        fns = self._cand_fns(fun)
        if fns:
            rs = fns[0].get("results") or []
            return [r.get("typ") for r in rs]
        return []

    def _typ(self, n):
        if not isinstance(n, dict): return None
        k = n.get("k")
        if k == "ident":
            nm = n.get("name")
            return self.vt.get(nm) if nm in self.vt else self.gtypes.get(nm)
        if k in ("star", "unary"): return self._typ(n.get("x"))
        if k == "composite": return n.get("typ") or None
        if k == "call": return (self._call_types(n) or [None])[0]
        if k == "sel":
            x, s = n.get("x", {}), n.get("sel")
            path = self._pkg(x)
            if path is not None:
                return "http.Client" if (path, s) == ("net/http", "DefaultClient") else None
            tx = self._typ(x)
            if tx in GIN_CTX_TYPES: return {"Writer": "gin.ResponseWriter", "Request": "http.Request"}.get(s)
            if tx == "http.Request": return REQ_FIELDS.get(s)
            if tx:
                return (self.stypes.get(tx.split(".")[-1]) or {}).get(s)
        return None

    def _add_types(self, body, vt):
        for st in self._iter_stmts(body):
            if st.get("k") == "var":
                for vd in st.get("vars", []):
                    vals = vd.get("values", [])
                    for i, nm in enumerate(vd.get("names", [])):
                        t = vd.get("typ") or (self._typ(vals[i]) if i < len(vals) else None)
                        if t: vt[nm] = t
            elif st.get("k") == "assign" and st.get("tok") in (":=", "="):
                lhs, rhs = st.get("lhs", []), st.get("rhs", [])
                if len(lhs) == len(rhs): ts = [self._typ(r) for r in rhs]
                elif len(rhs) == 1 and isinstance(rhs[0], dict) and rhs[0].get("k") == "call": ts = self._call_types(rhs[0])
                else: ts = []
                for l, t in zip(lhs, ts):
                    if t and isinstance(l, dict) and l.get("k") == "ident" and l.get("name") not in vt: vt[l["name"]] = t

    def _types_of(self, fn):
        """var/param name -> type name for one function (params, `var x T`, x := <typed expr>)."""
        vt = {}
        self.vt = vt
        for p in fn.get("params", []) + fn.get("recv", []):
            if p.get("name") and p.get("typ"): vt[p["name"]] = p["typ"]
        self._add_types(fn.get("body"), vt)
        return vt

    def _prepared_of(self, fn): return self._prepared_in(fn.get("body"))

    def _prepared_in(self, body):
        """Vars bound from a .Prepare(..)/.PrepareContext(..) call: calls ON them pass BOUND params (safe)."""
        prep = set()
        for st in self._iter_stmts(body):
            if st.get("k") == "assign":
                for r in st.get("rhs", []):
                    if isinstance(r, dict) and r.get("k") == "call" \
                       and r.get("fun", {}).get("sel") in ("Prepare", "PrepareContext", "Preparex"):
                        for l in st.get("lhs", []):
                            if l.get("k") == "ident" and l.get("name") != "_": prep.add(l["name"])
        return prep

    def _is_writer(self, n): return self._typ(n) in XSS_WRITER_TYPES

    def _struct_fields(self, t):
        return self.sfields.get((t or "").split(".")[-1], [])

    def _is_template(self, n):
        while isinstance(n, dict) and n.get("k") in ("call", "sel"):
            n = n.get("fun") if n.get("k") == "call" else n.get("x")
        if not (isinstance(n, dict) and n.get("k") == "ident"): return False
        if self._pkg(n) in ("html/template", "text/template"): return True
        return self._typ(n) == "template.Template"

    def _text_template(self):
        ps = set(self.cur_imports.values())
        return "text/template" in ps and "html/template" not in ps

    def _ctype_of(self, body):
        """The Content-Type a handler declares: "html", "other" (every declared type is not HTML), or None."""
        out = None
        for c in self._iter_calls(body):
            fun = c.get("fun", {}); a = c.get("args", [])
            if fun.get("k") != "sel" or len(a) < 2: continue
            key = _litstr(a[0])
            if not key or key.lower() != "content-type": continue
            rx = fun.get("x", {})
            hdr = (fun.get("sel") in ("Set", "Add") and isinstance(rx, dict) and rx.get("k") == "call"
                   and rx.get("fun", {}).get("sel") == "Header") \
                or (fun.get("sel") == "Header" and self._typ(rx) in GIN_CTX_TYPES)
            if not hdr: continue
            v = _litstr(a[1])
            if v is None and isinstance(a[1], dict) and a[1].get("k") == "ident":
                v = _litstr(self.gconst.get(a[1].get("name")))
            if v is None or "html" in v.lower(): return "html"
            out = "other"
        return out

    # ---------- taint of an expression node ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k == "lit": return F
        if k == "ident":
            nm = n.get("name")
            if nm in env: return F if self.vt.get(nm) in NUM_TYPES else env[nm]
            return F if nm in ("nil", "true", "false", "iota") else Z
        if k == "bin":
            if n.get("op") != "+": return F                  # comparison, logic, arithmetic: bool / number
            return self._concat(self._flat(n), env)
        if k == "unary" and n.get("op") in ("!", "-", "^", "+"): return F
        if k in ("star", "unary", "slice", "typeassert", "index"): return self.taint(n.get("x"), env)
        if k == "kv": return join(self.taint(n.get("value"), env), self.taint(n.get("key"), env))
        if k == "composite":
            v = join(*[self.taint(e, env) for e in n.get("elts", [])])
            if n.get("typ") == "url.URL":                # url.URL{Scheme, Host: const, Path: x}: the host decides ssrf
                hs = [self.taint(e.get("value"), env) for e in n.get("elts", []) if e.get("k") == "kv"
                      and e.get("key", {}).get("name") in ("Scheme", "Host", "User", "Opaque")]
                d, over = _parts(v); over["ssrf"] = _lj(*[_at(h, "ssrf") for h in hs]) if hs else F
                return _mk(d, over)
            return v
        if k == "call": return self._call_taint(n, env)
        if k == "sel": return self._sel_taint(n, env)
        if k == "funclit": return F
        return Z if k == "other" else F

    def _sel_taint(self, n, env):
        x, s = n.get("x", {}), n.get("sel")
        if isinstance(x, dict) and x.get("k") == "ident" and x.get("name", "") + "." + s in env:
            return env[x["name"] + "." + s]              # a field assigned / bound / checked on this path
        tx = self._typ(x)
        if tx == "http.Request" and (s in REQ_TAINTED or s in ("Form", "PostForm", "Body")): return T
        if tx == "url.URL" and s in URL_TAINTED and isinstance(x, dict) and x.get("k") == "sel" \
                and self._typ(x.get("x")) == "http.Request":
            # r.URL.Path: net/http's ServeMux (and ServeFile) reject/clean `..`; other routers may not -> file Z
            return _mk(T, {"file": Z}) if s == "Path" else T
        if self._typ(n) in NUM_TYPES: return F
        if isinstance(x, dict) and x.get("k") == "ident" and x.get("name") in env:
            d = _parts(env[x["name"]])[0]
            if d == T: return T                          # a field of request data (bound struct, parsed url)
            if d == F and x["name"] not in self.cur_params: return F   # a field of a value built here
        return Z                                         # unknown field access (h.cfg.X etc.): honest unknown

    def _flat(self, n):
        """A string expression as left-to-right ("s", literal text) / ("e", node) parts."""
        if isinstance(n, dict):
            if n.get("k") == "bin" and n.get("op") == "+": return self._flat(n.get("x")) + self._flat(n.get("y"))
            ls = _litstr(n)
            if ls is not None: return [("s", ls)]
            if n.get("k") == "call":
                fun = n.get("fun", {}); a = n.get("args", [])
                if fun.get("k") == "sel" and self._pkg(fun.get("x")) == "fmt" and fun.get("sel") == "Sprintf" and a:
                    return self._fmt_parts(a[0], a[1:])
                if (fun.get("k") == "other" or (fun.get("k") == "ident" and fun.get("name") in CONV_IDENTS)) and len(a) == 1:
                    return self._flat(a[0])
        return [("e", n)]

    def _fmt_parts(self, fmtn, args):
        f = _litstr(fmtn)
        if f is None: return [("e", fmtn)] + [("e", a) for a in args]
        out, i, pos = [], 0, 0
        for m in _VERB.finditer(f):
            out.append(("s", f[pos:m.start()])); pos = m.end()
            if m.group() == "%%": out.append(("s", "%")); continue
            if i < len(args): out.append(("e", args[i])); i += 1
        out.append(("s", f[pos:]))
        return out + [("e", a) for a in args[i:]]

    def _pos_level(self, v, ctx, prefix):
        """One part's level for ctx, given the literal text before it (escaper markers re-decided here)."""
        if ctx == "xss" and _at(v, "~html") == F: return F if _html_ok(prefix) else _parts(v)[0]
        if ctx == "ssrf" and _at(v, "~url") == F and _fixed_host(prefix): return F
        return _at(v, ctx)

    def _ctx_join(self, parts, env, ctx, vals=None):
        acc, out, i = "", [], 0
        for kd, x in parts:
            if kd == "s": acc += x; continue
            v = vals[i] if vals is not None else self.taint(x, env); i += 1
            out.append(self._pos_level(v, ctx, acc))
            acc += "https://\x01" if (not acc and v == F) else "\x00"   # a trusted leading base URL fixes the host
        return _lj(*out) if out else F

    def _concat(self, parts, env):
        vals = [self.taint(x, env) for kd, x in parts if kd == "e"]
        base = join(*vals) if vals else F
        if all(isinstance(v, str) for v in vals): return base
        d, over = _parts(base)
        over.pop("~html", None); over.pop("~url", None)   # a built string is judged by position, not re-escaped
        for ctx in ("xss", "ssrf", "file"): over[ctx] = self._ctx_join(parts, env, ctx, vals)
        return _mk(d, over)

    def _ctx_taint(self, n, env, ctx): return self._ctx_join(self._flat(n), env, ctx)

    def _is_source(self, call):
        fun = call.get("fun", {})
        if not isinstance(fun, dict) or fun.get("k") != "sel": return False
        sel = fun.get("sel"); x = fun.get("x", {})
        if sel in SOURCE_METHODS: return True
        if sel == "Vars" and x.get("name") == "mux": return True    # gorilla/mux path vars (tainted map)
        tx = self._typ(x)
        if sel in GIN_SRC and tx in GIN_CTX_TYPES: return True       # receiver-aware gin
        if sel == "Get":                                    # X.Query().Get(..) / X.{Header|Form|PostForm}.Get(..)
            if x.get("k") == "call" and x.get("fun", {}).get("sel") == "Query": return True
            if x.get("k") == "sel" and x.get("sel") in GET_CHAIN_RECV: return True
            if tx == "url.Values": return True              # q := r.URL.Query(); q.Get(..)
        if sel == "Query" and tx == "url.URL" and not call.get("args"): return True
        if sel == "Cookie" and tx == "http.Request": return True
        return False

    def _call_taint(self, n, env):
        fun = n.get("fun", {}); args = n.get("args", [])
        if self._is_source(n): return T
        if fun.get("k") == "ident" and fun.get("name") in CONV_IDENTS:
            return self.taint(args[0], env) if args else F
        path = self._pkg(fun.get("x")) if fun.get("k") == "sel" else None
        pk = fun.get("x", {}).get("name") if path is not None else None
        name0 = _callee_name(fun)
        if (pk, name0) in PKG_CLEAN: return F
        own = fun.get("k") == "ident" and self._sums_of(fun)
        if name0 in CTX_SANITIZERS and not own and (path is not None or CTX_SANITIZERS[name0] != "file"):
            d, over = _parts(join(*[self.taint(a, env) for a in args]))
            over.update(FAM_TAGS[CTX_SANITIZERS[name0]]); return _mk(d, over)
        if name0 in ("Sanitize", "SanitizeBytes") and self._typ(fun.get("x")) in HTML_SANITIZER_TYPES:
            d, over = _parts(join(*[self.taint(a, env) for a in args]))
            over.update(FAM_TAGS["xss"]); return _mk(d, over)
        if fun.get("k") == "ident" and name0 == "append": return join(*[self.taint(a, env) for a in args])
        if fun.get("k") == "other" and len(args) == 1:      # T(x) / []byte(x): conversion, transparent
            return self.taint(args[0], env)
        if pk == "fmt" and name0 == "Sprintf" and args:
            return self._concat(self._fmt_parts(args[0], args[1:]), env)
        if pk == "fmt" and name0 in ("Sprint", "Sprintln"):
            return join(*[self.taint(a, env) for a in args])
        if pk == "strings" and name0 in ("Replace", "ReplaceAll") and len(args) >= 3:
            v = join(*[self.taint(a, env) for a in args])
            old = _litstr(args[1]) or ""                    # a hand-rolled quote/angle escaper: unknown, not clean
            d, over = _parts(v)
            for ch, cx in (("'", "sql"), ("<", "xss")):
                if ch in old and _at(v, cx) == T: over[cx] = Z
            return _mk(d, over)
        if (pk, name0) in PKG_TRANSPARENT_PAIRS: return join(*[self.taint(a, env) for a in args])
        if path is not None and name0 in UNESCAPERS:      # decoding after a check revives what it rejected
            return _parts(join(*[self.taint(a, env) for a in args]))[0]
        if pk in ("filepath", "path") and name0 == "Clean" and args:
            fl = self._flat(args[0])
            if fl and fl[0][0] == "s" and fl[0][1].startswith("/"):   # Clean("/"+x): rooted, cannot climb
                d, over = _parts(join(*[self.taint(a, env) for a in args])); over["file"] = F; return _mk(d, over)
        name = name0
        external = path is not None and pk not in self.user_pkgs     # a library call: never a user summary
        sums = None if external else self._sums_of(fun)
        pkg = path is not None or (fun.get("k") == "sel" and fun.get("x", {}).get("k") == "ident"
                                   and fun.get("x", {}).get("name") not in env and fun.get("x", {}).get("name") not in self.vt)
        if sums is not None and not (pkg and (name in PKG_TRANSPARENT or name in NUMERIC_RESULT)):
            return self._apply(sums, args, env)
        if name in NUMERIC_RESULT: return F
        if pkg and name in PKG_TRANSPARENT: return join(*[self.taint(a, env) for a in args])
        if fun.get("k") == "sel" and name == "String" and not args: return self.taint(fun.get("x"), env)
        return Z

    def _sums(self, name):
        if self._dirty: self._summarize_all()
        return self.summaries.get(name)

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

    # ---------- sink reporting ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") == "funclit": return               # a closure is walked on its own (_closures)
            if n.get("k") == "call": yield n
            for v in n.values(): yield from self._iter_calls(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_calls(x)

    def _join_args(self, args, env):
        return join(*[self.taint(a, env) for a in args])

    def _apply_summary(self, call, name, args, env, sums):
        sums = [s for s in (sums or []) if s is not None]
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

    def _leaf_sinks(self, node, env):
        for c in self._iter_calls(node):
            fun = c.get("fun", {}); args = c.get("args", [])
            sel = fun.get("sel") if fun.get("k") == "sel" else None
            rx = fun.get("x", {}) if sel else {}
            path = self._pkg(rx) if sel else None
            xnm = rx.get("name") if path is not None else None
            rt = self._typ(rx) if sel and path is None else None
            xss_on = self.ctype != "other"
            if sel in ("Command", "CommandContext") and xnm == "exec":
                self._judge(c, "exec." + sel, "shell", self._join_args(args, env))
            elif (xnm, sel) in PKG_SINKS and args:          # os./ioutil./http./template. package sinks (arg0)
                cx = PKG_SINKS[(xnm, sel)]
                self._judge(c, xnm + "." + sel, cx, self._ctx_taint(args[0], env, cx))
            elif (xnm, sel) in PKG_SINK_ARGS:
                cx, i = PKG_SINK_ARGS[(xnm, sel)]
                vs = args if i is None else args[i:i + 1]
                if vs: self._judge(c, xnm + "." + sel, cx, join(*[self._ctx_taint(a, env, cx) for a in vs]))
            elif xnm == "fmt" and sel in FPRINT and len(args) > 1 and self._is_writer(args[0]):
                if xss_on:
                    parts = self._fmt_parts(args[1], args[2:]) if FPRINT[sel] else [("e", a) for a in args[1:]]
                    self._judge(c, "fmt." + sel, "xss", self._ctx_join(parts, env, "xss"))
            elif xnm == "io" and sel == "WriteString" and len(args) > 1 and self._is_writer(args[0]):
                if xss_on: self._judge(c, "io.WriteString", "xss", self._ctx_taint(args[1], env, "xss"))
            elif sel in ("Write", "WriteString") and rt in XSS_WRITER_TYPES and args:   # receiver-typed w.Write
                if xss_on: self._judge(c, sel, "xss", self._ctx_taint(args[0], env, "xss"))
            elif sel == "WriteTo" and args and self._is_writer(args[0]):
                if xss_on: self._judge(c, "WriteTo", "xss", _at(self.taint(rx, env), "xss"))
            elif rt in GIN_CTX_TYPES and sel == "String" and len(args) > 1:   # gin sets text/plain unless preset
                if self.ctype == "html":
                    self._judge(c, "c.String", "xss", self._ctx_join(self._fmt_parts(args[1], args[2:]), env, "xss"))
            elif rt in GIN_CTX_TYPES and sel == "Data" and len(args) > 2:
                ct = _litstr(args[1])
                if ct is None or "html" in ct.lower(): self._judge(c, "c.Data", "xss", self._ctx_taint(args[2], env, "xss"))
            elif rt in GIN_CTX_TYPES and sel in GIN_FILE and len(args) > GIN_FILE[sel]:
                self._judge(c, "c." + sel, "file", self._ctx_taint(args[GIN_FILE[sel]], env, "file"))
            elif sel == "Parse" and args and self._is_template(rx):          # the template SOURCE itself
                self._judge(c, "template.Parse", "xss", self.taint(args[0], env))
            elif sel in ("Execute", "ExecuteTemplate") and len(args) >= 2 and self._is_writer(args[0]) \
                    and self._is_template(rx) and self._text_template():        # text/template does not escape
                src = self._tmpl_src(rx)
                if xss_on and not (src is not None and _tmpl_all_escaped(src)):   # unless every action pipes | html
                    self._judge(c, "text/template." + sel, "xss", _at(self.taint(args[-1], env), "xss"))
            elif sel in CLIENT_METHODS and args and rt in CLIENT_TYPES:
                self._judge(c, "http.Client." + sel, "ssrf", self._ctx_taint(args[0], env, "ssrf"))
            elif sel in SQLX_DEST and len(args) >= 2 and isinstance(args[0], dict) and args[0].get("k") == "unary" \
                    and args[0].get("op") == "&" and path is None and rt not in NOT_SQL_TYPES:
                self._judge(c, sel, "sql", self.taint(args[SQLX_DEST[sel]], env))
            elif sel in SQL_METHODS and args and path is None and rx.get("name") not in self.prepared \
                    and rt not in NOT_SQL_TYPES and not (rx.get("k") == "sel" and rx.get("sel") in self.prep_fields):
                qi = SQL_METHODS[sel]                        # prepared-stmt receiver passes BOUND params (safe)
                q = args[qi] if qi < len(args) else None
                qt = self._typ(q)
                if q is not None and not (q.get("k") == "composite" or qt == "map" or (qt or "").split(".")[-1] in self.stypes):
                    self._judge(c, sel, "sql", self.taint(q, env))   # a map/struct condition is bound, not SQL text
            else:
                nm = _callee_name(fun)
                ss = None if (path is not None and rx.get("name") not in self.user_pkgs) else self._sums_of(fun)
                if ss: self._apply_summary(c, nm, args, env, ss)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge, not a local rule
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- statement walk ----------
    def _iter_stmts(self, body):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": yield from self._iter_stmts(st.get("body"))
            elif k == "if":
                if st.get("init"): yield st["init"]
                yield from self._iter_stmts(st.get("body"))
                if st.get("els"): yield from self._iter_stmts([st["els"]])
            elif k in ("for", "range", "switch", "case"): yield from self._iter_stmts(st.get("body"))
            else: yield st

    def _effects(self, n, env):
        """Calls that store into a local: buf.WriteString(x), v.Add(k, x), and writes through &x."""
        for c in self._iter_calls(n):
            fun = c.get("fun", {}); args = c.get("args", [])
            ptrs = [_root(a.get("x")) for a in args if isinstance(a, dict) and a.get("k") == "unary" and a.get("op") == "&"]
            ptrs = [p for p in ptrs if p and p != "_"]
            if ptrs:
                sel = fun.get("sel") if fun.get("k") == "sel" else None
                rx = fun.get("x", {}) if sel else {}
                others = [a for a in args if not (isinstance(a, dict) and a.get("k") == "unary" and a.get("op") == "&")]
                if sel and self._typ(rx) in GIN_CTX_TYPES and sel.startswith(("Bind", "ShouldBind", "MustBind")):
                    v = T                                              # gin binds request data into the struct
                elif sel == "Decode": v = join(Z, self.taint(rx, env))     # json.NewDecoder(r.Body).Decode(&x)
                elif sel == "Unmarshal": v = join(*[self.taint(a, env) for a in others]) if others else Z
                else: v = join(Z, *[self.taint(a, env) for a in others])   # Scan(&x): second order, unknown
                for p in ptrs:
                    env[p] = F if self.vt.get(p) in NUM_TYPES else join(env.get(p, F), v)
                    for k2 in [k2 for k2 in env if k2.startswith(p + ".")]: del env[k2]
                    if v == T:                                 # validator tags (alphanum, oneof=..) bound the field
                        for fd in self._struct_fields(self.vt.get(p)):
                            b = _re.search(r'binding:"([^"]*)"', fd.get("tag") or "")
                            if fd.get("typ") in NUM_TYPES or (b and any(t.startswith(BIND_SAFE_TAGS) for t in b.group(1).split(","))):
                                env[p + "." + fd["name"]] = F
            if fun.get("k") != "sel": continue
            r = fun.get("x", {})
            if not (isinstance(r, dict) and r.get("k") == "ident" and r.get("name") in env): continue
            vs = [self.taint(a, env) for a in args]
            if fun.get("sel") in MUTATORS: env[r["name"]] = join(env[r["name"]], *vs)
            elif fun.get("sel") not in NUMERIC_RESULT and any(x != F for x in vs) \
                    and fun.get("sel") not in SQL_METHODS:
                env[r["name"]] = join(env[r["name"]], Z)              # an unknown call MAY store it

    def _terminates(self, body):
        """Does this block leave the enclosing flow (return / continue / break / panic / log.Fatal)?"""
        if not (isinstance(body, list) and body): return False
        last = body[-1]
        if not isinstance(last, dict): return False
        if last.get("k") == "return": return True
        if last.get("k") == "branch": return last.get("tok") in ("continue", "break", "goto")
        if last.get("k") == "exprstmt" and isinstance(last.get("x"), dict) and last["x"].get("k") == "call":
            f = last["x"].get("fun", {})
            if f.get("k") == "ident" and f.get("name") == "panic": return True
            if f.get("k") == "sel" and self._pkg(f.get("x")) in ("os", "log") \
                    and f.get("sel") in ("Exit", "Fatal", "Fatalf", "Fatalln", "Panic", "Panicf"): return True
        return False

    def _is_const(self, b):
        if not isinstance(b, dict): return False
        if b.get("k") == "lit": return True
        if b.get("k") == "ident": return b.get("name") in self.gconst or b.get("name") in ("true", "false")
        if b.get("k") == "sel": return self._pkg(b.get("x")) is not None and (b.get("sel") or "a")[:1].isupper()
        return False

    def _const_bool(self, c):
        if isinstance(c, dict) and c.get("k") == "unary" and c.get("op") == "!":
            v = self._const_bool(c.get("x")); return None if v is None else not v
        if isinstance(c, dict) and c.get("k") == "ident":
            v = self.gconst.get(c.get("name"))
            if isinstance(v, dict) and v.get("k") == "ident" and v.get("name") in ("true", "false"):
                return v["name"] == "true"
        return None

    def _target(self, a):
        """What a check is about: x, x.f, or u.Host for u.Hostname(); through one-arg wrappers (ToLower(x))."""
        if not isinstance(a, dict): return None
        k = a.get("k")
        if k == "ident": return self.hostalias.get(a.get("name"), a.get("name"))
        if k == "sel" and a.get("x", {}).get("k") == "ident": return a["x"]["name"] + "." + a.get("sel", "")
        if k == "call":
            fun, args = a.get("fun", {}), a.get("args", [])
            if fun.get("k") == "sel" and fun.get("sel") == "Hostname" and not args and fun.get("x", {}).get("k") == "ident":
                return fun["x"]["name"] + ".Host"
            if len(args) == 1: return self._target(args[0])
        return None

    def _arg_vars(self, args): return [t for t in (self._target(a) for a in args) if t]

    def _str_of(self, n):
        v = _litstr(n)
        if v is None and isinstance(n, dict) and n.get("k") == "ident": v = _litstr(self.gconst.get(n.get("name")))
        return v

    def _ends_sep(self, n):
        """Does this prefix end in a path separator (so HasPrefix is a directory containment, not 42 vs 421)?"""
        parts = self._flat(n)
        if not parts: return False
        kd, x = parts[-1]
        if kd == "s": return x.endswith("/") or x.endswith("\\")
        if isinstance(x, dict) and x.get("k") == "sel" and x.get("sel") in ("PathSeparator", "Separator"): return True
        v = self._str_of(x)
        return bool(v) and (v.endswith("/") or v.endswith("\\"))

    def _regex_of(self, rx):
        """The pattern text behind a compiled regexp variable, when it is a literal."""
        if not (isinstance(rx, dict) and rx.get("k") == "ident"): return None
        nm = rx["name"]; cands = []
        for d in self._nodes(self.cur_body):
            if d.get("k") == "assign":
                for l, r in zip(d.get("lhs", []), d.get("rhs", [])):
                    if isinstance(l, dict) and l.get("name") == nm: cands.append(r)
        if not cands and nm in self.gvals: cands.append(self.gvals[nm])
        for r in cands:
            for c in self._iter_calls(r):
                if c.get("fun", {}).get("sel") in ("MustCompile", "Compile", "MustCompilePOSIX", "CompilePOSIX") and c.get("args"):
                    return _litstr(c["args"][0])
        return None

    def _tmpl_src(self, rx):
        """The literal text a template variable was parsed from, if any."""
        if not (isinstance(rx, dict) and rx.get("k") == "ident"): return None
        nm = rx["name"]; cands = []
        for d in self._nodes(self.cur_body):
            if d.get("k") == "assign":
                for l, r in zip(d.get("lhs", []), d.get("rhs", [])):
                    if isinstance(l, dict) and l.get("name") == nm: cands.append(r)
        if not cands and nm in self.gvals: cands.append(self.gvals[nm])
        for r in cands:
            for c in self._iter_calls(r):
                if c.get("fun", {}).get("sel") == "Parse" and c.get("args"):
                    return self._str_of(c["args"][0])
        return None

    def _validates_param(self, fn, i):
        """Does this helper return a non-nil error on a condition that depends on param i?"""
        ps = fn.get("params", [])
        if i >= len(ps) or not ps[i].get("name"): return False
        dep, changed = {ps[i]["name"]}, True
        idents = lambda n: {d.get("name") for d in self._nodes(n) if d.get("k") == "ident"}
        while changed:
            changed = False
            for d in self._nodes(fn.get("body")):
                if d.get("k") == "assign" and idents(d.get("rhs")) & dep:
                    new = {l.get("name") for l in d.get("lhs", []) if isinstance(l, dict) and l.get("k") == "ident"} - dep - {"_"}
                    if new: dep |= new; changed = True
        for d in self._nodes(fn.get("body")):
            if d.get("k") == "if" and idents(d.get("cond")) & dep:
                for st in d.get("body") or []:
                    if isinstance(st, dict) and st.get("k") == "return" and st.get("results") \
                            and not (st["results"][-1].get("k") == "ident" and st["results"][-1].get("name") == "nil"):
                        return True
        return False

    def _is_bool_func(self, fun):
        nm = _callee_name(fun)
        if fun.get("k") == "sel" and self._pkg(fun.get("x")) is not None and fun["x"]["name"] not in self.user_pkgs:
            return False
        fns = self._cand_fns(fun)
        return bool(fns) and all([r.get("typ") for r in f.get("results") or []] == ["bool"] for f in fns)

    def _conds(self, c, init=None):
        """(vars validated when c is true, vars validated when c is false): name -> ctx (None = every ctx)."""
        if not isinstance(c, dict): return {}, {}
        k, op = c.get("k"), c.get("op")
        if k == "unary" and op == "!":
            t, e = self._conds(c.get("x"), init); return e, t
        if k == "bin" and op in ("&&", "||"):
            t1, e1 = self._conds(c.get("x"), init); t2, e2 = self._conds(c.get("y"), init)
            return (_vunion(t1, t2), _vinter(e1, e2)) if op == "&&" else (_vinter(t1, t2), _vunion(e1, e2))
        if k == "bin" and op in ("==", "!="):
            eq = op == "=="
            x, y = c.get("x", {}), c.get("y", {})
            for a, b in ((x, y), (y, x)):
                if a.get("k") == "ident" and b.get("k") == "ident" and b.get("name") == "nil" and a.get("name") in self.errsrc:
                    v = dict(self.errsrc[a["name"]])                  # err from a validating parser / helper
                    return (v, {}) if eq else ({}, v)
            for a, b in ((x, y), (y, x)):
                tg = self._target(a) if a.get("k") in ("ident", "sel") or (a.get("k") == "call" and not a.get("args")) else None
                if tg and a.get("name") != "nil" and self._is_const(b):
                    v = {tg: None}                                     # x == "c" / x != pkg.Const / u.Hostname() == "h"
                    return (v, {}) if eq else ({}, v)
            return {}, {}
        if k == "index":                                               # allow[x]
            tg = self._target(c.get("index"))
            if tg: return {tg: None}, {}
        if k == "ident" and isinstance(init, dict) and init.get("k") == "assign":   # _, ok := allow[x]; ok
            if c.get("name") in [l.get("name") for l in init.get("lhs", []) if isinstance(l, dict)]:
                for r in init.get("rhs", []):
                    if isinstance(r, dict) and r.get("k") == "index":
                        tg = self._target(r.get("index"))
                        if tg: return {tg: None}, {}
        if k == "call":
            fun = c.get("fun", {}); nm = _callee_name(fun); a = c.get("args", [])
            path = self._pkg(fun.get("x")) if fun.get("k") == "sel" else None
            if nm in ("Contains", "ContainsAny", "ContainsRune") and path == "strings":
                lit = _litstr(a[1]) if len(a) >= 2 else None
                if lit is not None and (".." in lit or "/" in lit or "\\" in lit):   # a traversal rejection
                    return {}, {n: ("file",) for n in self._arg_vars(a[:1])}
                return {}, {}                     # a substring test is not validation (evil.com/?acme-cdn.net)
            if nm in ("MatchString", "Match"):
                pat = _litstr(a[0]) if path == "regexp" and a else (None if path else self._regex_of(fun.get("x")))
                tg = self._arg_vars(a[1:] if path == "regexp" else a)
                if pat is None: return {n: "Z" for n in tg}, {}          # a pattern we cannot read: not proven either way
                if not _anchored(pat): return {}, {}
                sp = _regex_spec(pat)
                return ({n: sp for n in tg}, {}) if sp != () else ({}, {})
            if nm == "IsLocal": return {n: ("file",) for n in self._arg_vars(a[:1])}, {}
            if nm == "HasPrefix" and len(a) >= 2 and path == "strings":
                cx = (["file"] if self._ends_sep(a[1]) else []) + \
                     (["ssrf"] if _fixed_host(self._str_of(a[1]) or "") else [])
                return ({n: tuple(cx) for n in self._arg_vars(a[:1])}, {}) if cx else ({}, {})
            if nm == "HasSuffix" and len(a) >= 2 and path == "strings":   # a hostname inside an owned zone
                lit = self._str_of(a[1]) or ""
                tg = [n for n in self._arg_vars(a[:1]) if n.endswith(".Host")]
                return ({n: ("ssrf",) for n in tg}, {}) if lit.startswith(".") and tg else ({}, {})
            if nm in ("Contains", "ContainsFunc") and path in ("slices", "maps") and len(a) >= 2:
                return {n: None for n in self._arg_vars(a[1:])}, {}
            if self._is_bool_func(fun):
                return {n: None for n in self._arg_vars(a)}, {}
        return {}, {}

    def _validate(self, env, v):
        for n, cx in v.items():
            if "." in n:
                root, f = n.split(".", 1)
                if f == "Host" and root in env and self._typ({"k": "ident", "name": root}) == "url.URL":
                    if cx == "Z": env[root] = _mk(_parts(env[root])[0], dict(_parts(env[root])[1], ssrf=Z if _at(env[root], "ssrf") == T else _at(env[root], "ssrf")))
                    elif cx is None or "ssrf" in cx: env[root] = _clean_for(env[root], "ssrf")   # the host is checked
            if n in env: env[n] = _apply_spec(env[n], cx)
            if cx is None:
                for k2 in [k2 for k2 in env if k2.startswith(n + ".")]: env[k2] = F

    def _decls(self, body):
        out = set()
        for st in body or []:
            if not isinstance(st, dict): continue
            if st.get("k") == "assign" and st.get("tok") == ":=":
                out |= {l.get("name") for l in st.get("lhs", []) if isinstance(l, dict) and l.get("k") == "ident"}
            elif st.get("k") == "var":
                for vd in st.get("vars", []): out |= set(vd.get("names", []))
        return out

    def _restore(self, env, snap, names):
        for nm in names:
            if nm in snap: env[nm] = snap[nm]
            else: env.pop(nm, None)

    def _scoped(self, body, env):
        """Walk a nested block: names it declares (:=, var) shadow the outer ones and end with it."""
        snap = dict(env); self._walk(body, env); self._restore(env, snap, self._decls(body))

    def _funclits(self, n):
        if isinstance(n, dict):
            if n.get("k") == "call" and isinstance(n.get("fun"), dict) and n["fun"].get("k") == "funclit":
                yield n["fun"], n.get("args", [])                    # go func(u string) {..}(x)
                for a in n.get("args", []): yield from self._funclits(a)
                return
            if n.get("k") == "funclit": yield n, None; return
            for v in n.values(): yield from self._funclits(v)
        elif isinstance(n, list):
            for x in n: yield from self._funclits(x)

    def _closures(self, n, env):
        for fl, args in list(self._funclits(n)): self._walk_funclit(fl, env, args)

    def _walk_funclit(self, fl, env, args):
        """A closure: its body runs later (or now, when called in place), over the variables it captures."""
        saved = (self.vt, self._rets, self.ctype, self.errsrc, self.prepared, self.cur_params, dict(self.hostalias))
        params = [p.get("name") for p in fl.get("params", [])]
        self.vt = dict(self.vt); self.errsrc = {}; self._rets = None
        e = dict(env)
        for i, p in enumerate(fl.get("params", [])):
            nm = p.get("name")
            if not nm or nm == "_": continue
            if p.get("typ"): self.vt[nm] = p["typ"]
            e[nm] = self.taint(args[i], env) if args is not None and i < len(args) else F
        try:
            self.cur_params = set(self.cur_params) | set(params)
            self._add_types(fl.get("body"), self.vt)
            self.prepared = self.prepared | self._prepared_in(fl.get("body"))
            self.ctype = self._ctype_of(fl.get("body")) or self.ctype
            self._scoped(fl.get("body"), e)
        finally:
            self.vt, self._rets, self.ctype, self.errsrc, self.prepared, self.cur_params, self.hostalias = saved
        for nm in list(env):                                 # what the closure wrote into captured variables
            if nm in e and nm not in params and e[nm] != env[nm]: env[nm] = join(env[nm], e[nm])

    def _els_body(self, els):
        return els.get("body") if isinstance(els, dict) and els.get("k") == "block" else None

    def _multi(self, r, n, vals, env):
        """a, b := f(..): per-position taint where known, else the single rhs taint spread."""
        if isinstance(r, dict) and r.get("k") == "call" and n == 2:
            fun = r.get("fun", {}); nm = _callee_name(fun)
            pk = fun.get("x", {}).get("name") if fun.get("k") == "sel" and self._pkg(fun.get("x")) else None
            if nm in NUMERIC_RESULT or (pk, nm) in VALIDATING_PARSERS:
                return [F, join(*[self.taint(a, env) for a in r.get("args", [])])]   # the error quotes its input
        return [vals[0] if vals else Z] * n

    def _walk(self, body, env):
        for st in (body or []):
            if not isinstance(st, dict): continue
            k = st.get("k")
            if k == "block": self._scoped(st.get("body"), env); continue
            if k == "if":
                snap = dict(env)
                if st.get("init"): self._walk([st["init"]], env)
                cond = st.get("cond")
                self._leaf_sinks(cond, env); self._effects(cond, env); self._closures(cond, env)
                tv, ev = self._conds(cond, st.get("init"))
                cb = self._const_bool(cond)
                e1 = dict(env); e2 = dict(env)
                self._validate(e1, tv); self._validate(e2, ev)
                if cb is not False: self._scoped(st.get("body"), e1)
                if st.get("els") and cb is not True: self._scoped([st["els"]], e2)
                if cb is False: out = e2                              # if constFalse {..}: never runs
                elif cb is True: out = e1
                elif self._terminates(st.get("body")): out = e2       # continuation follows else/fallthrough
                elif st.get("els") and self._terminates(self._els_body(st["els"])): out = e1
                else: out = _ejoin(e1, e2)
                _set_env(env, out)
                self._restore(env, snap, self._decls([st["init"]] if st.get("init") else []))
                continue
            if k in ("for", "range"):
                if st.get("x"): self._leaf_sinks(st.get("x"), env); self._closures(st.get("x"), env)
                snap = dict(env)
                loopvars = [nm for nm in (_root(st.get("key")), _root(st.get("value"))) if nm and nm != "_"]
                def head(e):
                    if k == "range":
                        v = self.taint(st.get("x"), e)
                        for nm in loopvars: e[nm] = v
                e0 = dict(env)
                e1 = dict(env); head(e1); self._scoped(st.get("body"), e1)
                e2 = _ejoin(e0, e1)
                e3 = dict(e2); head(e3); self._scoped(st.get("body"), e3)
                _set_env(env, _ejoin(e2, e3))                 # zero or more iterations
                if st.get("tok") == ":=": self._restore(env, snap, loopvars)
                continue
            if k == "switch":
                snap = dict(env)
                if st.get("init"): self._walk([st["init"]], env)
                tag = st.get("tag")
                if tag: self._leaf_sinks(tag, env); self._effects(tag, env)
                tagvar = tag.get("name") if isinstance(tag, dict) and tag.get("k") == "ident" else None
                outs, prev, has_default = [], None, False
                for c in st.get("body") or []:
                    e = dict(env)
                    if prev is not None and prev[1]: e = _ejoin(env, prev[0])   # explicit fallthrough
                    if isinstance(c, dict) and c.get("k") == "case":
                        lst = c.get("list") or []
                        if not lst: has_default = True
                        elif tagvar and tagvar in e and all(self._is_const(x) for x in lst): e[tagvar] = F
                        elif not tag and len(lst) == 1: self._validate(e, self._conds(lst[0])[0])
                        b = c.get("body") or []
                        self._scoped(b, e)
                        ft = bool(b) and isinstance(b[-1], dict) and b[-1].get("k") == "branch" and b[-1].get("tok") == "fallthrough"
                    else:
                        self._walk([c], e); ft = False
                    outs.append(e); prev = (e, ft)
                if not has_default: outs.append(dict(env))   # no case may run
                _set_env(env, _ejoin(*outs))
                self._restore(env, snap, self._decls([st["init"]] if st.get("init") else []))
                continue
            if k == "case":
                self._walk(st.get("body"), env); continue
            # leaf statements
            if k == "assign":
                self._effects(st, env)
                rhs, lhs = st.get("rhs", []), st.get("lhs", [])
                vals = [self.taint(r, env) for r in rhs]
                compound = st.get("tok") not in ("=", ":=", None)
                if len(vals) != len(lhs): vals = self._multi(rhs[0] if rhs else None, len(lhs), vals, env)
                if len(rhs) == 1 and isinstance(rhs[0], dict) and rhs[0].get("k") == "call":
                    fun = rhs[0].get("fun", {})
                    pk = fun.get("x", {}).get("name") if fun.get("k") == "sel" and self._pkg(fun.get("x")) else None
                    cn = _callee_name(fun); cargs = rhs[0].get("args", [])
                    last = lhs[-1] if lhs else None
                    has_err = len(lhs) >= 1 and isinstance(last, dict) and last.get("k") == "ident" and last.get("name") != "_"
                    if (pk, cn) in VALIDATING_PARSERS:
                        if len(lhs) >= 2 and has_err:
                            self.errsrc[last["name"]] = {n: None for n in self._arg_vars(cargs)}
                        elif len(lhs) == 1 or cn.startswith("Must"):
                            self._validate(env, {n: None for n in self._arg_vars(cargs)})
                    elif has_err and (pk is None or pk in self.user_pkgs) and self._cand_fns(fun):
                        fns = self._cand_fns(fun)
                        if all(([r.get("typ") for r in f.get("results") or []] or [None])[-1] == "error" for f in fns):
                            chk = [i for i in range(len(cargs)) if any(self._validates_param(f, i) for f in fns)]
                            if chk:   # a helper that rejects on its argument: checked, but not proven by us -> Z
                                v = {n: "Z" for i in chk for n in self._arg_vars([cargs[i]])}
                                v.update({l["name"]: "Z" for l in lhs[:-1] if isinstance(l, dict) and l.get("k") == "ident" and l.get("name") != "_"})
                                self.errsrc[last["name"]] = v
                            else: self.errsrc.pop(last["name"], None)
                    elif has_err: self.errsrc.pop(last["name"], None)
                for l, v in zip(lhs, vals):
                    if not isinstance(l, dict): continue
                    if l.get("k") == "ident" and len(lhs) == len(rhs) == 1:
                        tg = self._target(rhs[0]) if rhs[0].get("k") in ("call", "sel") else None
                        if tg and tg.endswith(".Host") and not tg.startswith(l["name"] + "."): self.hostalias[l["name"]] = tg
                        else: self.hostalias.pop(l["name"], None)
                    if l.get("k") == "ident":
                        if l["name"] == "_": continue
                        env[l["name"]] = join(env.get(l["name"], Z), v) if compound else v
                        if not compound:
                            for k2 in [k2 for k2 in env if k2.startswith(l["name"] + ".")]: del env[k2]
                    else:                                    # m[k] = v / s.f = v / *p = v
                        if l.get("k") == "sel" and ((l.get("sel") in ("Host", "Scheme") and self._typ(l.get("x")) == "url.URL")
                                                    or (l.get("sel") in ("URL", "Host") and self._typ(l.get("x")) == "http.Request")):
                            self._judge(st, "proxy target ." + l["sel"], "ssrf", self._ctx_taint(rhs[min(lhs.index(l), len(rhs) - 1)], env, "ssrf") if rhs else v)
                        r = _root(l)
                        if r is not None:
                            env[r] = join(env.get(r, F), v if l.get("k") in ("index", "star") or st.get("tok") == "<-" else
                                          (F if v == F else Z))
                        if l.get("k") == "sel" and l.get("x", {}).get("k") == "ident":
                            fk = l["x"]["name"] + "." + l.get("sel", "")
                            env[fk] = join(env.get(fk, Z), v) if compound else v    # this field now holds v
            elif k == "var":
                for vd in st.get("vars", []):
                    names, values = vd.get("names", []), vd.get("values", [])
                    for i, nm in enumerate(names):
                        env[nm] = self.taint(values[i], env) if i < len(values) else F   # Go zero value
            elif k == "return":
                self._effects(st, env)
                if self._rets is not None:
                    self._rets.append(join(*[self.taint(r, env) for r in st.get("results", [])]))
            elif k == "exprstmt":
                self._effects(st, env)
            self._leaf_sinks(st, env)
            self._closures(st, env)

    # ---------- passes ----------
    def _enter(self, fn):
        self.cur_imports = fn.get("_imports", {}); self.cur_pkg = fn.get("_pkg")
        self.vt = self._types_of(fn); self.prepared = self._prepared_of(fn)
        self.cur_params = {p.get("name") for p in fn.get("params", []) + fn.get("recv", [])}
        self.ctype = self._ctype_of(fn.get("body")); self.errsrc = {}; self.cur_body = fn.get("body")
        self.hostalias = {}

    def _summ_of(self, fn):
        saved = (self.sinks, self._rets, self.cur_imports, self.cur_pkg, self.cur_body)
        self._enter(fn)
        params = [p.get("name") for p in fn.get("params", [])]
        def run(env):
            self.sinks, self._rets = [], []
            self.errsrc = {}
            self._walk(fn.get("body"), env)
            got = {}
            for (l, m, ctx, d) in self.sinks:
                key = (l, m, ctx)
                if _DRANK[d] > _DRANK.get(got.get(key), -1): got[key] = d
            return (join(*self._rets) if self._rets else F), got
        try:
            base_env = dict(self.genv)
            base_env.update({p: F for p in params if p and p != "_"})
            base, bs = run(dict(base_env))
            summ = {"sinks": {}, "passes": set(), "params": params, "base": base, "ret": []}
            for i, p in enumerate(params):
                env = dict(base_env)
                if p and p != "_": env[p] = T
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
            self.sinks, self._rets, self.cur_imports, self.cur_pkg, self.cur_body = saved

    def index(self, tree):
        imps = {i["name"]: i["path"] for i in tree.get("imports", [])}
        for fn in tree.get("funcs", []):
            fn["_imports"] = imps; fn["_pkg"] = tree.get("_pkey", tree.get("pkg")); fn["_pkgname"] = tree.get("pkg")
            if fn.get("name"): self.funcs.setdefault(fn["name"], []).append(fn)
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
        for fn in tree.get("funcs", []):
            self._enter(fn)
            env = dict(self.genv)
            env.update({p["name"]: F for p in fn.get("params", []) if p.get("name") and p.get("name") != "_"})
            self._rets = None
            self._walk(fn.get("body"), env)
        best, order = {}, []
        for rec in self.sinks:
            key = rec[:3]
            if key not in best: order.append(key); best[key] = rec
            elif _DRANK[rec[3]] > _DRANK[best[key][3]]: best[key] = rec
        self.sinks = [best[key] for key in order if best[key][3] != "EARNED"]
        return self.sinks

    def run(self, tree):
        self.prepare([tree]); return self.judge(tree)

def _ensure_goast():
    """Build the goast helper on first use so the module is self-contained; raise if Go is absent."""
    if os.path.exists(GOAST): return
    src = os.path.join(HERE, "goast.go")
    env = dict(os.environ, GO111MODULE="off", GOCACHE=os.environ.get("GOCACHE", "/tmp/gocache"))
    r = subprocess.run(["go", "build", "-o", GOAST, src], capture_output=True, text=True, cwd=HERE, env=env)
    if r.returncode != 0 or not os.path.exists(GOAST):
        raise RuntimeError("go2zfl: could not build goast helper (need Go toolchain): " + r.stderr.strip())

def parse(path):
    _ensure_goast()
    out = subprocess.run([GOAST, path], capture_output=True, text=True, timeout=30)
    return json.loads(out.stdout) if out.stdout.strip() else {"funcs": []}

def analyze(path): return Engine().run(parse(path))

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean

def analyze_app(paths):
    e = Engine(); trees = []
    del UNPARSED[:]
    for p in paths:
        t = parse(p)
        if t.get("error"): UNPARSED.append((p, str(t["error"])[:60])); continue
        t["_pkey"] = os.path.dirname(os.path.abspath(p)) + ":" + str(t.get("pkg"))   # a Go package is a directory
        if t.get("funcs") or t.get("globals") or t.get("types"): trees.append((p, t))
    e.prepare([t for _, t in trees])
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
