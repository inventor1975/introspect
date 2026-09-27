# -*- coding: utf-8 -*-
"""cs2zfl — C# module of the introspect (slice 1, 2026-09-13).
Parser: C#'s OWN Roslyn via the `csast` helper (dotnet, Microsoft.CodeAnalysis.CSharp -> compact JSON).
Shared contract INTROSPECT-SEMANTICS.md: zero-trust F/T/Z -> REFUTED/OPEN/EARNED, honest OPEN.
Slice1: ASP.NET sources (Request.Query/Form/..., [FromQuery]/[FromRoute]/[FromBody] + bare action params)
-> sinks: Process.Start=shell, new SqlCommand(concat)/.CommandText=sql, Response.Write/Html.Raw/new
HtmlString=xss, File.*=file, *.Deserialize=deser; string concat + interpolation, context-aware html
escapers (HttpUtility.HtmlEncode), cross-method + cross-file SUMMARIES, guards, branch-join.
Seventh language after php/py/java/go/js/ruby.
Slice 2 (2026-09-27), the java2zfl soundness lesson ported: tri-valued summaries with a parameter-free
base, returns captured where they happen, OPEN sink effects kept, same-name methods that disagree -> Z,
summaries to a fixpoint; try/catch, switch and loops joined (break/continue reach the exit); foreach binds
its variable; `+=` joins; o.P = v / d[k] = v / sb.Append(v) fold; a transparent call keeps its RECEIVER's
taint (s.Replace("a","b") read only its first argument, so a tainted s became F); escapers tag one context
and the program's own Encode(..) wins over the catalogue's; comparisons and arithmetic give F."""
import json, subprocess, os, sys, re as _re
F, T, Z = "F", "T", "Z"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # tool/ -> shared taint->ZFL->judge adapter
import taintjudge
CSAST = os.path.join(HERE, "csast", "bin", "pub", "csast")

REQUEST_BASES = {"Request", "httpContext", "HttpContext", "context"}
REQ_SOURCE_MEMBERS = {"Query", "Form", "QueryString", "Params", "Headers", "Cookies",
                      "RouteValues", "ServerVariables", "InputStream", "Body", "Path", "PathBase", "Host",
                      "RawUrl", "Url", "UrlReferrer", "UserAgent", "Files"}
REQ_TYPES = {"HttpContext", "HttpRequest", "HttpRequestBase", "HttpContextBase"}   # a parameter of these types is a request base
TAINT_TYPES = {"IFormFile", "IFormCollection", "IFormFileCollection", "IQueryCollection", "IHeaderDictionary"}
NUM_TYPES = {"int", "long", "short", "byte", "uint", "ulong", "ushort", "sbyte", "bool", "double", "float", "decimal",
             "Guid", "DateTime", "DateTimeOffset", "DateOnly", "TimeSpan", "Int32", "Int64", "Boolean", "Decimal", "Double"}
MAP_VERBS = {"MapGet", "MapPost", "MapPut", "MapDelete", "MapPatch", "Map", "MapMethods", "MapFallback"}
FROM_ATTRS = {"FromQuery", "FromRoute", "FromBody", "FromForm", "FromHeader"}
SIMPLE_TYPES = {"string", "String", "int", "Int32", "long", "Int64", "short", "byte", "bool",
                "Boolean", "double", "float", "decimal", "Guid", "string[]", "int?"}
# sinks
SHELL = {("Process", "Start")}                        # Process.Start(file, args)
XSS_MEMBER = {("Response", "Write"), ("Response", "WriteAsync"), ("Html", "Raw"), ("HtmlHelper", "Raw")}
FILE_BASES = {"File"}
FILE_METHODS = {"ReadAllText", "ReadAllBytes", "ReadAllLines", "WriteAllText", "WriteAllBytes",
                "AppendAllText", "OpenRead", "OpenWrite", "Open", "Create", "Delete", "Move", "Copy", "ReadLines",
                "AppendAllLines", "WriteAllLines", "OpenText", "CreateText", "AppendText", "Replace",
                "ReadAllTextAsync", "ReadAllBytesAsync", "ReadAllLinesAsync", "WriteAllTextAsync",
                "WriteAllBytesAsync", "AppendAllTextAsync", "WriteAllLinesAsync"}
DIR_METHODS = {"Delete", "GetFiles", "GetDirectories", "EnumerateFiles", "EnumerateDirectories", "Move",
               "EnumerateFileSystemEntries", "GetFileSystemEntries", "CreateDirectory"}
FILE_RESULTS = {"PhysicalFile", "SendFileAsync", "WriteFile", "TransmitFile"}    # a path sent as the response
DAPPER = {"Query", "QueryAsync", "QueryFirst", "QueryFirstAsync", "QueryFirstOrDefault", "QueryFirstOrDefaultAsync",
          "QuerySingle", "QuerySingleAsync", "QuerySingleOrDefault", "QuerySingleOrDefaultAsync", "QueryMultiple",
          "QueryMultipleAsync", "Execute", "ExecuteAsync", "ExecuteScalar", "ExecuteScalarAsync", "ExecuteReader",
          "ExecuteReaderAsync"}
EF_RAW = {"FromSqlRaw", "ExecuteSqlRaw", "ExecuteSqlRawAsync", "SqlQueryRaw", "ExecuteSqlCommand",
          "ExecuteSqlCommandAsync", "FromSql", "SqlQuery"}   # FromSql($"..")/FromSqlInterpolated are parameterised
CONTENT_RESULTS = {"Content", "Text"}                  # Content(html, "text/html"), Results.Text(..)
UNESCAPERS = {"HtmlDecode", "UrlDecode", "UnescapeDataString", "HtmlAttributeDecode"}
DESER_METHODS = {"Deserialize"}                       # BinaryFormatter/LosFormatter/JavaScriptSerializer.Deserialize
SQL_CMD_TYPES = {"SqlCommand", "MySqlCommand", "NpgsqlCommand", "OleDbCommand", "SqlDataAdapter",
                 "OdbcCommand", "SQLiteCommand"}
XSS_NEW_TYPES = {"HtmlString", "MvcHtmlString"}
FILE_NEW_TYPES = {"StreamReader", "StreamWriter", "FileStream"}
# context-aware escapers: neutralise ONE context, transparent for others
CTX_SANITIZERS = {"HtmlEncode": "xss", "HtmlAttributeEncode": "xss", "JavaScriptStringEncode": "js",
                  "Encode": "xss", "UrlEncode": "urlq", "EscapeDataString": "urlq", "UrlPathEncode": "urlp",
                  "GetFileName": "file"}
# what each family clears; ~markers let a string built around the value re-decide by position
FAM_TAGS = {"xss": {"xss": F, "~html": F}, "js": {"~js": F}, "urlq": {"xss": F, "~url": F},
            "urlp": {"~html": F}, "file": {"file": F}}
_URL_ATTRS = {"href", "src", "action", "formaction", "xlink:href", "data", "poster", "background", "srcset"}

def _html_pos(prefix):
    """Where a value lands after this literal text: text / attr / url (START of a URL attribute) / script / bad."""
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

_CLS = {"w": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"), "d": set("0123456789"),
        "s": set(" \t\r\n\f\v")}
DANGER = {"sql": set("'\";\\"), "xss": set("<>\"'"), "file": set("/\\"), "shell": set(";|&$`<>()'\"\n \\")}

def _charset(spec):
    out, i = set(), 0
    while i < len(spec):
        if i + 2 < len(spec) and spec[i + 1] == "-":
            out |= {chr(c) for c in range(ord(spec[i]), ord(spec[i + 2]) + 1)}; i += 3
        else:
            if spec[i] == "\\" and i + 1 < len(spec): i += 1
            out.add(spec[i]); i += 1
    return out

def _anchored(p):
    p = _re.sub(r"^\(\?[a-zA-Z]+\)", "", p or "")
    if not (p.startswith("^") or p.startswith("\\A")): return False
    if not ((p.endswith("$") and not p.endswith("\\$")) or p.endswith("\\z") or p.endswith("\\Z")): return False
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

def _regex_spec(src):
    """An anchored regexp clears the contexts none of whose dangerous characters it can match."""
    out, i, n = set(), 0, len(src)
    while i < n:
        ch = src[i]
        if ch == "\\" and i + 1 < n:
            c = src[i + 1]; i += 2
            if c in "AzZb": continue
            if c in _CLS: out |= _CLS[c]
            elif c in "WDS": return ()
            else: out.add(c)
            continue
        if ch == "[":
            j = i + 1
            if j < n and src[j] == "^": return ()
            spec = ""
            while j < n and src[j] != "]":
                if src[j] == "\\" and j + 1 < n:
                    c = src[j + 1]
                    if c in _CLS: out |= _CLS[c]
                    elif c in "WDS": return ()
                    else: spec += "\\" + c
                    j += 2; continue
                spec += src[j]; j += 1
            out |= _charset(spec); i = j + 1; continue
        if ch == ".": return ()
        if ch in "^$()?*+{}|,0123456789": i += 1; continue
        out.add(ch); i += 1
    ok = tuple(sorted(cx for cx, bad in DANGER.items() if not (out & bad)))
    return None if len(ok) == len(DANGER) else ok
CONV_IDENTS = {"Convert", "ToString"}
# transparent transforms: PRESERVE taint (decode/encode/case/trim), NOT sanitizers
TRANSPARENT_METHODS = {"FromBase64String", "ToBase64String", "GetString", "GetBytes", "Trim", "TrimStart",
                       "TrimEnd", "ToLower", "ToUpper", "ToLowerInvariant", "ToUpperInvariant",
                       "Substring", "Replace", "ToString", "Decode", "Normalize", "PadLeft", "PadRight"}


def _prop(member): return member.get("prop") if isinstance(member, dict) else None

def _base_ident(n):
    while isinstance(n, dict) and n.get("k") in ("member", "index"):
        n = n.get("object", {})
    return n.get("name") if isinstance(n, dict) and n.get("k") == "ident" else None

def _callee_name(callee):
    if not isinstance(callee, dict): return None
    if callee.get("k") == "ident": return callee.get("name")
    if callee.get("k") == "member": return callee.get("prop")
    return None


_RANK = {F: 0, Z: 1, T: 2}
_DRANK = {"EARNED": 0, "OPEN": 1, "REFUTED": 2}
# of the transparent methods, those whose ARGUMENTS are content too (Substring(i, j)'s are numbers)
ARG_CONTENT = {"Replace", "Insert", "Format", "Concat", "Join", "FromBase64String", "ToBase64String", "GetString",
               "GetBytes", "Decode", "UrlDecode", "HtmlDecode", "Combine", "ToString"}
NUMERIC_RESULT = {"ToInt32", "ToInt64", "ToInt16", "ToDouble", "ToDecimal", "ToBoolean", "Parse", "TryParse",
                  "Length", "Count", "Contains", "StartsWith", "EndsWith", "Equals", "IndexOf", "LastIndexOf",
                  "IsNullOrEmpty", "IsNullOrWhiteSpace", "Any", "All", "CompareTo", "GetHashCode", "Exists"}
# calls on a local that store their argument in it
MUTATORS = {"Append", "AppendLine", "AppendFormat", "Insert", "Add", "AddRange", "Push", "Enqueue", "Set",
            "Write", "WriteLine", "TryAdd"}


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

def _path(n):
    parts = []
    while isinstance(n, dict) and n.get("k") == "member":
        parts.append(n.get("prop")); n = n.get("object", {})
    if isinstance(n, dict) and n.get("k") == "ident" and parts and all(parts):
        return ".".join([n["name"]] + parts[::-1])
    return None


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
        if c.endswith("?"):                                  # "file?": that context capped at Z
            d, over = _parts(v); over[c[:-1]] = Z if _at(v, c[:-1]) == T else _at(v, c[:-1]); v = _mk(d, over)
        else: v = _clean_for(v, c)
    return v
def _lit(n): return n.get("value") if isinstance(n, dict) and n.get("k") == "lit" else None
def _qual(n):
    """The dotted name of a receiver chain: System.IO.File -> "System.IO.File"."""
    parts = []
    while isinstance(n, dict) and n.get("k") == "member":
        parts.append(n.get("prop") or ""); n = n.get("object")
    if isinstance(n, dict) and n.get("k") == "ident": parts.append(n.get("name") or "")
    return ".".join(reversed(parts))


class Engine:
    def __init__(self):
        self.summaries = {}   # name -> [summary]
        self.funcs = {}
        self.sinks = []
        self._rets = None
        self._esc = []
        self._dirty = False
        self.reqbases = set(REQUEST_BASES)   # + parameters typed HttpContext / HttpRequest
        self.vt = {}          # parameter -> declared type
        self.webforms = False # the method is in a Page / UserControl: `.Text =` renders HTML
        self._cur_env = None
        self._in_pred = False
        self._in_field = False
        self.fregexes = {}    # a static Regex field -> its pattern (from the class's field initialisers)
        self.ffields = {}     # a field -> its initialiser (FilesRoot = GetFullPath(..) + DirectorySeparatorChar)
        self.relof = {}       # rel = Path.GetRelativePath(root, full): a check on rel checks full
        self.bound = set()    # the current action's request-bound parameters
        self.encoded = set()  # WebForms controls set to LiteralMode.Encode
        self.sepvars = set()
        self.ptypes = {}      # class -> {property: type}
        self.ftypes = {}      # field -> its declared type (a WebForms control: Label, Literal, TextBox ..)
        self.enums = set()    # enum type names
        self.regexes = {}

    def _join(self, a, b): return join(a, b)

    def _terminates(self, body):
        if isinstance(body, list) and body:
            return isinstance(body[-1], dict) and body[-1].get("k") in ("return", "throw", "break", "continue")
        return False

    # ---------- guards ----------
    def _target(self, a):
        if not isinstance(a, dict): return None
        k = a.get("k")
        if k == "ident": return a.get("name")
        if k == "member":
            p = _path(a)
            if p and _base_ident(a) not in self.reqbases: return p
        if k == "call" and a.get("callee", {}).get("k") == "member" and not a.get("args") \
                and a["callee"].get("prop") in ("ToLower", "ToLowerInvariant", "ToUpper", "ToUpperInvariant", "Trim", "ToString"):
            return self._target(a["callee"].get("object"))
        if k in ("cast", "await"): return self._target(a.get("x"))
        return None

    def _is_const(self, n):
        if not isinstance(n, dict): return False
        if n.get("k") == "lit": return n.get("kind") != "NullLiteralExpression"
        if n.get("k") == "member": return (_base_ident(n) or "a")[:1].isupper() and _base_ident(n) not in self.reqbases
        return n.get("k") == "ident" and (n.get("name") or "a")[:1].isupper()

    def _regex_check(self, pat, x):
        tg = self._target(x)
        if not tg: return {}, {}
        if pat is None: return {tg: "Z"}, {}
        if not _anchored(pat): return {}, {}
        sp = _regex_spec(pat)
        return ({tg: sp}, {}) if sp != () else ({}, {})

    def _regex_of(self, n):
        if isinstance(n, dict) and n.get("k") == "new" and n.get("args"): return _lit(n["args"][0])
        if isinstance(n, dict) and n.get("k") in ("ident", "member"):
            nm = n.get("name") or n.get("prop")
            return self.regexes.get(nm)
        return None

    def _conds(self, c):
        if not isinstance(c, dict): return {}, {}
        k, op = c.get("k"), c.get("op")
        if k == "unary" and op == "!":
            t, e = self._conds(c.get("x")); return e, t
        if k == "bin" and op in ("&&", "||"):
            t1, e1 = self._conds(c.get("x")); t2, e2 = self._conds(c.get("y"))
            return (_vunion(t1, t2), _vinter(e1, e2)) if op == "&&" else (_vinter(t1, t2), _vunion(e1, e2))
        if k == "bin" and op in ("==", "!="):
            x, y = c.get("x"), c.get("y")
            for a, b in ((x, y), (y, x)):
                tg = self._target(a)
                if tg and self._is_const(b) and not self._is_const(a):
                    v = {tg: None}
                    return (v, {}) if op == "==" else ({}, v)
            return {}, {}
        if k == "member" and c.get("prop") == "IsValid" and _base_ident(c) == "ModelState":
            return {p: "Z" for p in self.bound}, {}         # [RegularExpression] etc. enforced: checked, not proven here
        if k == "call":
            callee = c.get("callee", {}); args = c.get("args", []); nm = _callee_name(callee)
            obj = callee.get("object") if callee.get("k") == "member" else None
            if nm in ("Contains", "ContainsKey", "Any", "TryGetValue") and args \
                    and _qual(obj).split(".")[-1] not in ("File", "Directory", "Path", "string", "String"):
                if nm == "Contains" and obj is not None and isinstance(args[0], dict) and _lit(args[0]) is not None:
                    v = _lit(args[0]) or ""                          # x.Contains("..") rejects traversal (file only)
                    tg = self._target(obj)
                    # rejecting ".." does not stop an ABSOLUTE path, which Path.Combine lets replace the base
                    if tg and (".." in v or "/" in v or "\\" in v): return {}, {tg: ("file?",)}
                    return {}, {}
                tg = self._target(args[0])
                if tg and obj is not None and self.taint(obj, self._cur_env or {}) != T: return {tg: None}, {}
            if nm == "IsMatch" and args:
                if _qual(obj) in ("Regex", "System.Text.RegularExpressions.Regex") and len(args) >= 2:
                    return self._regex_check(_lit(args[1]), args[0])
                return self._regex_check(self._regex_of(obj), args[0])
            if nm == "TryParse" and args:                        # int.TryParse(x, out n): x is a number
                tg = self._target(args[0])
                if tg: return {tg: None}, {}
            if nm == "StartsWith" and args and self._target(obj) in self.relof and (_lit(args[0]) or "").startswith(".."):
                return {}, {self.relof[self._target(obj)]: ("file",)}   # GetRelativePath(root, full).StartsWith("..")
            if nm == "StartsWith" and args and obj is not None and self._ends_sep(args[0]):
                tg = self._target(obj)
                if tg: return {tg: ("file",)}, {}
            if nm in self.funcs and not self._in_pred:           # an own bool check: IsAllowed(x)
                out = {}
                self._in_pred = True
                try:
                    for i, a in enumerate(args):
                        specs = [self._pred_spec(f, i) for f in self.funcs[nm]]
                        tg = self._target(a)
                        if tg and specs and all(sp is not False for sp in specs):
                            sp = specs[0]
                            for x in specs[1:]: sp = _sinter(sp, x)
                            if sp is not False: out[tg] = sp
                finally:
                    self._in_pred = False
                if out: return out, {}
        return {}, {}

    def _ends_sep(self, n, depth=0):
        if not isinstance(n, dict) or depth > 4: return False
        if n.get("k") == "ident" and n.get("name") in self.sepvars: return True
        if n.get("k") == "ident" and n.get("name") in self.ffields: return self._ends_sep(self.ffields[n["name"]], depth + 1)
        if n.get("k") == "bin" and n.get("op") == "+": return self._ends_sep(n.get("y"))
        if n.get("k") == "member" and n.get("prop") in ("DirectorySeparatorChar", "AltDirectorySeparatorChar"): return True
        if n.get("k") == "lit": return (n.get("value") or "").endswith(("/", "\\"))
        if n.get("k") == "template":
            ps = n.get("parts") or []
            if ps and "e" in ps[-1] and isinstance(ps[-1]["e"], dict) and ps[-1]["e"].get("prop") in ("DirectorySeparatorChar", "AltDirectorySeparatorChar"):
                return True
            return bool(ps) and "s" in ps[-1] and ps[-1]["s"].endswith(("/", "\\"))
        return False

    def _pred_spec(self, fn, i):
        ps = fn.get("params", []); body = fn.get("body") or []
        if i >= len(ps) or not body or not isinstance(body[-1], dict) or body[-1].get("k") != "return": return False
        tv, _ = self._conds(body[-1].get("argument"))
        return tv.get(ps[i].get("name"), False)

    def _validate(self, env, v):
        for n, cx in v.items():
            if n in env or "." in n: env[n] = _apply_spec(env.get(n, self._path_taint(n, env)), cx)
            if cx is None:
                for k2 in [k2 for k2 in env if k2.startswith(n + ".")]: env[k2] = F

    def _path_taint(self, p, env):
        root = p.split(".")[0]
        return env.get(root, Z)

    def _is_class(self, n, env):
        """A static receiver (Encoding.UTF8, Convert, HttpUtility): a type, not data."""
        b = _base_ident(n)
        return b is not None and b not in env and b[:1].isupper() and b not in self.reqbases

    # ---------- taint ----------
    def taint(self, n, env):
        if not isinstance(n, dict): return F
        k = n.get("k")
        if k in ("lit", "nil"): return F
        if k == "ident":
            nm = n.get("name")
            if nm in env: return env[nm]
            if nm in ("null", "true", "false"): return F
            init = self.ffields.get(nm)
            if isinstance(init, dict) and init.get("k") not in ("new", "array", "call") and not self._in_field:
                # a const / readonly VALUE initialised here (an object held in a field is state: unknown)
                self._in_field = True
                try: return self.taint(init, {})
                finally: self._in_field = False
            return Z
        if k == "index":                                              # Request.Query["x"] / Request["x"]
            obj = n.get("object", {})
            if isinstance(obj, dict) and obj.get("k") == "ident" and obj.get("name") in self.reqbases:
                return T                                                  # Request["x"] indexer (WebForms)
            return self.taint(obj, env)
        if k == "bin":
            if n.get("op") in ("==", "!=", "<", ">", "<=", ">=", "is", "as", "-", "*", "/", "%", "&", "|", "^",
                               "<<", ">>", "&&", "||"):
                return F
            if n.get("op") == "+": return self._concat(self._flat(n), env)
            return join(self.taint(n.get("x"), env), self.taint(n.get("y"), env))    # ??
        if k == "template": return self._concat(self._flat(n), env)
        if k == "await": return self.taint(n.get("x"), env)
        if k == "cast":
            t = (n.get("type") or "").rstrip("?")
            if t in ("int", "long", "short", "byte", "bool", "double", "float", "decimal", "Guid", "DateTime", "uint", "ulong"):
                return F
            return self.taint(n.get("x"), env)
        if k == "cond":
            saved = self._cur_env; self._cur_env = env
            tv, ev = self._conds(n.get("test")) if n.get("test") else ({}, {})
            self._cur_env = saved
            e1, e2 = dict(env), dict(env); self._validate(e1, tv); self._validate(e2, ev)
            return join(self.taint(n.get("x"), e1), self.taint(n.get("y"), e2))
        if k == "condaccess":
            return self.taint(self._bind(n.get("then"), n.get("x")), env)
        if k == "assignexpr": return self.taint(n.get("right"), env)
        if k == "unary": return F
        if k == "array": return join(*[self.taint(e, env) for e in n.get("elts", [])])
        if k == "lambda": return F
        if k == "member":
            p = _path(n)
            if p is not None and p in env: return env[p]
            o = n.get("object")
            if n.get("prop") in ("Text", "Value", "SelectedValue") and self.ftypes.get(_base_ident(n) or "") in \
                    ("TextBox", "HiddenField", "DropDownList", "ListBox", "RadioButtonList", "HtmlInputText",
                     "HtmlTextArea", "HtmlInputHidden"):
                return T                                      # a WebForms input control: the posted value
            # dto.Region where Region is an enum / a number
            if isinstance(o, dict) and o.get("k") == "ident":
                pt = self.ptypes.get(self.vt.get(o.get("name"), ""), {}).get(n.get("prop"))
                if pt and (pt in NUM_TYPES or pt in self.enums): return F
            if _prop(n) in REQ_SOURCE_MEMBERS and _base_ident(n) in self.reqbases: return T
            if _prop(n) in NUMERIC_RESULT: return F
            if self._is_class(n, env): return Z                        # a static member: unknown
            return self.taint(n.get("object"), env)                   # propagate (Request.Form.Get chains)
        if k in ("call", "new"): return self._call_taint(n, env)
        return Z                                                      # funcref, other: unknown

    def _bind(self, then, x):
        """o?.P(..): put o back where the member binding stands."""
        if not isinstance(then, dict): return then
        if then.get("k") == "member" and isinstance(then.get("object"), dict) and then["object"].get("k") == "nil":
            return dict(then, object=x)
        if then.get("k") in ("member", "call", "index"):
            key = "callee" if then.get("k") == "call" else "object"
            return dict(then, **{key: self._bind(then.get(key), x)})
        return then

    def _flat(self, n):
        if isinstance(n, dict):
            if n.get("k") == "bin" and n.get("op") == "+": return self._flat(n.get("x")) + self._flat(n.get("y"))
            if n.get("k") == "lit" and n.get("kind") == "StringLiteralExpression": return [("s", n.get("value") or "")]
            if n.get("k") == "template":
                return [("s", p["s"]) if "s" in p else ("e", p["e"]) for p in n.get("parts") or []] \
                    or [("e", e) for e in n.get("exprs", [])]
        return [("e", n)]

    def _concat(self, parts, env):
        vals = [self.taint(x, env) for kd, x in parts if kd == "e"]
        base = join(*vals) if vals else F
        if all(isinstance(v, str) for v in vals): return base
        d, over = _parts(base)
        for m in ("~html", "~js", "~url"): over.pop(m, None)
        acc, out, i = "", [], 0
        for kd, x in parts:
            if kd == "s": acc += x; continue
            v = vals[i]; i += 1
            pos = _html_pos(acc)
            if _at(v, "~url") == F: out.append(F)
            elif _at(v, "~html") == F and pos in ("text", "attr"): out.append(F)
            elif _at(v, "~js") == F and pos == "script" and acc.rstrip("\x00")[-1:] in ("'", '"'): out.append(F)
            elif _at(v, "~html") == F or _at(v, "~js") == F: out.append(_parts(v)[0])
            else: out.append(_at(v, "xss"))
            acc += "\x00"
        over["xss"] = _lj(*out) if out else F
        acc, sq, i = "", [], 0                                     # sql: a quote-doubled value protects only
        for kd, x in parts:                                        # inside a quoted literal
            if kd == "s": acc += x; continue
            v = vals[i]; i += 1
            if _at(v, "~qd") == F: sq.append(Z if acc.rstrip("\x00").endswith("'") else _parts(v)[0])
            else: sq.append(_at(v, "sql"))
            acc += "\x00"
        over["sql"] = _lj(*sq) if sq else F
        over.pop("~qd", None)
        return _mk(d, over)

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

    def _call_taint(self, n, env):
        callee = n.get("callee", {}); args = n.get("args", [])
        if n.get("k") == "new":                                       # StringBuilder(x) etc: transparent-ish
            vs = [self.taint(a, env) for a in args] + [self.taint(i.get("value"), env) for i in n.get("init") or []]
            return join(*vs) if vs else F
        cn = _callee_name(callee)
        own = callee.get("k") == "ident" and self._sums(cn)
        if cn in CTX_SANITIZERS and not own:                         # the program's own Encode(..) wins
            fam = CTX_SANITIZERS[cn]
            q = _qual(callee.get("object")) if callee.get("k") == "member" else ""
            if cn == "Encode" and "JavaScriptEncoder" in q: fam = "js"
            elif cn == "Encode" and "UrlEncoder" in q: fam = "urlq"
            d, over = _parts(join(*[self.taint(a, env) for a in args[:1]]))
            over.update(FAM_TAGS[fam]); return _mk(d, over)
        if cn in UNESCAPERS: return _parts(join(*[self.taint(a, env) for a in args[:1]]))[0]   # decoding undoes a check
        if own: return self._apply(self._sums(cn), args, env)
        if cn in NUMERIC_RESULT: return F
        recv = F
        if callee.get("k") == "member":
            obj = callee.get("object")
            recv = F if self._is_class(obj, env) else self.taint(obj, env)
            if cn in ("ReadFormAsync", "ReadFromJsonAsync") and _base_ident(obj) in self.reqbases: return T
            if cn in ("ReadFormAsync", "ReadFromJsonAsync", "ReadToEndAsync", "ReadToEnd", "ReadAsStringAsync",
                      "GetValueOrDefault", "FirstOrDefault", "First", "Single", "SingleOrDefault", "ElementAt",
                      "Select", "Take", "Skip", "OrderBy", "ToList", "ToArray", "Distinct"):
                return recv
            if cn in ("Combine", "Join", "GetFullPath", "Format", "Concat") and self._is_class(obj, env):
                return join(*[self.taint(a, env) for a in args])
        if cn == "ToBase64String" and args:                  # [A-Za-z0-9+/=]: no quote, no angle, no separator-free path
            return self._keep_clean(join(*[self.taint(a, env) for a in args[:1]]),
                                    set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="))
        if cn == "Where" and args and callee.get("k") == "member":
            keep = self._keep_set(args[0])
            if keep is not None: return self._keep_clean(recv, keep)     # s.Where(c => 'A' <= c && c <= 'Z' ..)
            return recv
        if cn == "Replace" and callee.get("k") == "member" and len(args) >= 2 and _lit(args[0]) in ("'", "\"") \
                and _lit(args[1]) in ("''", '""'):
            d, over = _parts(recv); over["~qd"] = F                # quote doubling: decided by where the value lands
            return _mk(d, over)
        if cn in ("SerializeObject", "ToJson") or (cn == "Serialize" and "JsonConvert" in _qual(callee.get("object"))):
            return join(*[self.taint(a, env) for a in args[:1]])   # Newtonsoft: < > survive into a <script>
        if cn == "Serialize" and "JsonSerializer" in _qual(callee.get("object")):
            v = join(*[self.taint(a, env) for a in args[:1]])
            if len(args) > 1:                                        # options may swap the encoder
                o = args[1]; oi = self.ffields.get(o.get("name")) if isinstance(o, dict) and o.get("k") == "ident" else o
                txt = json.dumps(oi) if oi is not None else ""
                if "UnsafeRelaxedJsonEscaping" in txt or "Create" in txt: return v
                if oi is None or "Encoder" in txt: return _pc(lambda l: Z if l == T else l, v)
            d, over = _parts(v)
            over["xss"] = F; return _mk(d, over)                     # System.Text.Json escapes < > & ' by default
        if cn in ("Invariant", "CurrentCulture") and "FormattableString" in _qual(callee.get("object")):
            return join(*[self.taint(a, env) for a in args])
        if cn == "Replace" and _qual(callee.get("object")).split(".")[-1] == "Regex" and len(args) >= 3 \
                and _lit(args[2]) == "" and _re.fullmatch(r"\[\^(.*)\][+*]?", _lit(args[1]) or ""):
            keep = _charset(_re.fullmatch(r"\[\^(.*)\][+*]?", _lit(args[1]))[1])  # Regex.Replace(x, "[^a-z0-9]", "")
            return self._keep_clean(self.taint(args[0], env), keep)
        if cn in TRANSPARENT_METHODS or cn in ARG_CONTENT:
            if cn in ARG_CONTENT: return join(recv, *[self.taint(a, env) for a in args])
            return recv
        sums = self._sums(cn)
        if sums is not None: return self._apply(sums, args, env)
        return Z

    def _ctx_taint(self, node, env, ctx):
        return _at(self.taint(node, env), ctx)

    def _keep_clean(self, v, kept):
        d, over = _parts(v)
        for cx, bad in DANGER.items():
            if not (kept & bad): over[cx] = F
        return _mk(d, over)

    def _keep_set(self, f):
        """The characters a Where(..) filter keeps: char.IsLetterOrDigit, or a lambda of ranges / equalities."""
        LET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"); DIG = set("0123456789")
        named = {"IsLetterOrDigit": LET | DIG, "IsLetter": LET, "IsDigit": DIG, "IsAsciiLetterOrDigit": LET | DIG,
                 "IsAsciiLetter": LET, "IsAsciiDigit": DIG, "IsUpper": LET, "IsLower": LET}
        if isinstance(f, dict) and f.get("k") == "member" and f.get("prop") in named: return named[f["prop"]]
        if not (isinstance(f, dict) and f.get("k") == "lambda" and f.get("params") and f.get("body")): return None
        c = f["params"][0].get("name"); body = f["body"][-1]
        if not (isinstance(body, dict) and body.get("k") == "return"): return None
        def chars(e):
            if not isinstance(e, dict): return None
            if e.get("k") == "bin" and e.get("op") == "||":
                a, b = chars(e.get("x")), chars(e.get("y"))
                return None if a is None or b is None else a | b
            if e.get("k") == "bin" and e.get("op") == "&&":           # c >= 'A' && c <= 'Z'
                lo = hi = None
                for side in (e.get("x"), e.get("y")):
                    if isinstance(side, dict) and side.get("k") == "bin" and (side.get("x") or {}).get("name") == c:
                        v = _lit(side.get("y"))
                        if v is None: return None
                        if side.get("op") in (">=", ">"): lo = chr(ord(v) + (side["op"] == ">"))
                        elif side.get("op") in ("<=", "<"): hi = chr(ord(v) - (side["op"] == "<"))
                if lo is None or hi is None: return None
                return {chr(x) for x in range(ord(lo), ord(hi) + 1)}
            if e.get("k") == "bin" and e.get("op") == "==" and (e.get("x") or {}).get("name") == c and _lit(e.get("y")):
                return {_lit(e.get("y"))}
            if e.get("k") == "call" and _callee_name(e.get("callee")) in named: return named[_callee_name(e["callee"])]
            return None
        return chars(body.get("argument"))

    # ---------- sinks ----------
    def _iter_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") == "lambda": return                          # walked on its own (_lambdas)
            if n.get("k") in ("call", "new", "cast"): yield n
            for v in n.values(): yield from self._iter_calls(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_calls(x)

    def _join_args(self, args, env):
        return join(*[self.taint(a, env) for a in args])

    def _apply_summary(self, call, name, args, env):
        sums = [s for s in (self._sums(name) or []) if s is not None]
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

    def _html_ct(self, n):
        """A content type argument: True if HTML (or not a literal we can read)."""
        v = _lit(n)
        return v is None or "html" in v.lower()

    def _dbish(self, obj):
        b = (_base_ident(obj) or _callee_name(obj.get("callee")) if isinstance(obj, dict) and obj.get("k") == "call" else _base_ident(obj)) or ""
        q = (_qual(obj) or b).lower()
        return any(w in q for w in ("conn", "db", "sql", "database", "cnn", "datasource")) or "createconnection" in json.dumps(obj).lower()

    def _leaf_sinks(self, node, env):
        for c in self._iter_calls(node):
            args = c.get("args", [])
            if c.get("k") == "cast":
                if (c.get("type") or "").split(".")[-1] in ("MarkupString", "HtmlString", "MvcHtmlString"):
                    self._judge(c, "(" + c["type"] + ")", "xss", self._ctx_taint(c.get("x"), env, "xss"))
                continue
            if c.get("k") == "new":
                typ = c.get("type", "").split("<")[0].split(".")[-1]
                init = {i.get("name"): i.get("value") for i in c.get("init") or []}
                if (typ.endswith("Command") or typ.endswith("DataAdapter")) and args:
                    self._judge(c, "new " + typ, "sql", self._ctx_taint(args[0], env, "sql"))
                elif typ.endswith("Command") and "CommandText" in init:
                    self._judge(c, "new " + typ, "sql", self._ctx_taint(init["CommandText"], env, "sql"))
                elif typ in XSS_NEW_TYPES and args:
                    self._judge(c, "new " + typ, "xss", self._ctx_taint(args[0], env, "xss"))
                elif typ in FILE_NEW_TYPES | {"FileInfo", "DirectoryInfo", "PhysicalFileResult"} and args:
                    self._judge(c, "new " + typ, "file", self._ctx_taint(args[0], env, "file"))
                elif typ == "ContentResult" and "Content" in init and self._html_ct(init.get("ContentType")):
                    self._judge(c, "new ContentResult", "xss", self._ctx_taint(init["Content"], env, "xss"))
                continue
            callee = c.get("callee", {})
            nm = _callee_name(callee)
            if callee.get("k") == "member":
                prop = callee.get("prop"); obj = callee.get("object"); base = _base_ident(obj)
                last = _qual(obj).split(".")[-1]
                if (base, prop) in SHELL:
                    self._judge(c, base + "." + prop, "shell", self._join_args(args, env))
                elif prop in ("Write", "WriteAsync") and args and (last == "Response" or self.vt.get(base) == "HttpResponse"):
                    self._judge(c, "Response." + prop, "xss", self._ctx_taint(args[0], env, "xss"))
                elif (base, prop) in XSS_MEMBER and args:
                    self._judge(c, prop, "xss", self._ctx_taint(args[0], env, "xss"))
                elif prop == "AddMarkupContent" and len(args) > 1:
                    self._judge(c, prop, "xss", self._ctx_taint(args[1], env, "xss"))
                elif last == "File" and prop in FILE_METHODS and args:
                    vs = args[:2] if prop in ("Move", "Copy", "Replace") else args[:1]
                    self._judge(c, "File." + prop, "file", join(*[self._ctx_taint(a, env, "file") for a in vs]))
                elif last == "Directory" and prop in DIR_METHODS and args:
                    vs = args[:2] if prop == "Move" else args[:1]
                    self._judge(c, "Directory." + prop, "file", join(*[self._ctx_taint(a, env, "file") for a in vs]))
                elif prop in FILE_RESULTS and args:
                    self._judge(c, prop, "file", self._ctx_taint(args[0], env, "file"))
                elif prop in ("File", "PhysicalFile") and last in ("Results", "TypedResults") and args:
                    self._judge(c, last + "." + prop, "file", self._ctx_taint(args[0], env, "file"))
                elif prop in CONTENT_RESULTS and last in ("Results", "TypedResults", "this") and args \
                        and (len(args) > 1 and self._html_ct(args[1])):
                    self._judge(c, last + "." + prop, "xss", self._ctx_taint(args[0], env, "xss"))
                elif prop == "CreateCommand" and args and self._dbish(obj):
                    self._judge(c, prop, "sql", self._ctx_taint(args[0], env, "sql"))
                elif prop in EF_RAW and args and not (prop in ("FromSql", "SqlQuery") and isinstance(args[0], dict) and args[0].get("k") == "template"):
                    self._judge(c, prop, "sql", self._ctx_taint(args[0], env, "sql"))
                elif prop in DAPPER and args and self._dbish(obj):
                    self._judge(c, prop, "sql", self._ctx_taint(args[0], env, "sql"))
                elif prop in DESER_METHODS and args:
                    self._judge(c, prop, "deser", self.taint(args[0], env))
                elif self._sums(prop) and prop not in TRANSPARENT_METHODS | ARG_CONTENT | NUMERIC_RESULT | MUTATORS:
                    self._apply_summary(c, prop, args, env)
            elif callee.get("k") == "ident":
                if nm in CONTENT_RESULTS and args and len(args) > 1 and self._html_ct(args[1]) and nm == "Content":
                    self._judge(c, "Content", "xss", self._ctx_taint(args[0], env, "xss"))
                elif nm in ("PhysicalFile",) and args:
                    self._judge(c, nm, "file", self._ctx_taint(args[0], env, "file"))
                elif self._sums(nm): self._apply_summary(c, nm, args, env)

    def _judge(self, call, name, ctx, st):
        st = _at(st, ctx)
        d = taintjudge.judge_taint(st, ctx, source="input", sink=name)   # the ONE ZTL judge
        if d in ("REFUTED", "OPEN", "EARNED"):
            self.sinks.append((call.get("line", 0), name, ctx, d))

    # ---------- effects ----------
    def _assign_to(self, left, v, env, op):
        compound = op not in (None, "=")
        if not isinstance(left, dict): return
        if left.get("k") == "ident":
            nm = left["name"]; env[nm] = join(env.get(nm, Z), v) if compound else v
            for k2 in [k2 for k2 in env if k2.startswith(nm + ".")]:
                if not compound: del env[k2]
        elif left.get("k") == "member":
            p = _path(left)
            if p is not None: env[p] = join(env.get(p, Z), v) if compound else v
            r = _base_ident(left)
            if r is not None and r in env: env[r] = join(env[r], F if v == F else Z)
        elif left.get("k") == "index":                              # d["k"] = v: the collection holds v
            r = _base_ident(left)
            if r is not None: env[r] = join(env.get(r, F), v)

    def _lambdas(self, node, env):
        """Lambdas in a statement: a minimal-API handler (MapGet(.., (string q) => ..)) is an entry point;
        any other lambda runs over the variables it captures, its parameter bound to the receiver."""
        for c in self._iter_all_calls(node):
            callee = c.get("callee", {}); nm = _callee_name(callee)
            recv = self.taint(callee.get("object"), env) if callee.get("k") == "member" else Z
            for a in c.get("args", []):
                if not (isinstance(a, dict) and a.get("k") == "lambda"): continue
                e = dict(env)
                saved = (self.vt, self._rets, self.reqbases)
                self.vt = dict(self.vt); self._rets = None; self.reqbases = set(self.reqbases)
                try:
                    for p in a.get("params", []):
                        pn = p.get("name")
                        if not pn: continue
                        typ = (p.get("typ") or "").split(".")[-1].rstrip("?")
                        self.vt[pn] = typ
                        if typ in REQ_TYPES: self.reqbases.add(pn); e[pn] = F
                        elif nm in MAP_VERBS: e[pn] = T if (self._param_source(p, True) or typ in TAINT_TYPES) else F
                        else: e[pn] = recv
                    self._walk(a.get("body"), e)
                finally:
                    self.vt, self._rets, self.reqbases = saved
                for k2 in list(env):
                    if k2 in e and e[k2] != env[k2] and k2 not in [p.get("name") for p in a.get("params", [])]:
                        env[k2] = join(env[k2], e[k2])

    def _iter_all_calls(self, n):
        if isinstance(n, dict):
            if n.get("k") == "lambda": return
            if n.get("k") == "call": yield n
            for v in n.values(): yield from self._iter_all_calls(v)
        elif isinstance(n, list):
            for x in n: yield from self._iter_all_calls(x)

    def _effects(self, node, env):
        if isinstance(node, dict):
            if node.get("k") == "lambda": return
            if node.get("k") == "assignexpr":
                self._effects(node.get("right"), env)
                self._assign_to(node.get("left"), self.taint(node.get("right"), env), env, node.get("op"))
                return
            if node.get("k") in ("call", "new"):
                for a in node.get("args", []): self._effects(a, env)
                callee = node.get("callee", {})
                if isinstance(callee, dict) and callee.get("k") == "member":
                    self._effects(callee.get("object"), env)
                    obj = callee.get("object", {}); m = callee.get("prop")
                    root = obj                                    # sb.Append(a).Append(b): both fold into sb
                    while isinstance(root, dict) and root.get("k") == "call" and _callee_name(root.get("callee")) in MUTATORS \
                            and root.get("callee", {}).get("k") == "member":
                        root = root["callee"].get("object")
                    if isinstance(root, dict) and root.get("k") == "ident" and root.get("name") in env:
                        vs = [self.taint(a, env) for a in node.get("args", [])]
                        if m in MUTATORS: env[root["name"]] = join(env[root["name"]], *vs)
                        elif root is obj and m not in TRANSPARENT_METHODS and m not in ARG_CONTENT and m not in NUMERIC_RESULT \
                                and any(x != F for x in vs):
                            env[root["name"]] = join(env[root["name"]], Z)
                if node.get("k") == "call" and _callee_name(callee) == "TryParse":
                    for a in node.get("args", []):         # int.TryParse(x, out var n): n is a number
                        pass
                return
            for v in node.values(): self._effects(v, env)
        elif isinstance(node, list):
            for x in node: self._effects(x, env)

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
            elif k == "try":
                yield from self._iter_stmts(st.get("body")); yield from self._iter_stmts(st.get("handler"))
                yield from self._iter_stmts(st.get("finalizer"))
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
                elif st.get("els") and isinstance(st["els"], dict) and st["els"].get("k") == "block" \
                        and self._terminates(st["els"].get("body")): _set_env(env, e1)
                else: _set_env(env, _ejoin(e1, e2))
                continue
            if k == "for":
                def head(e):
                    if st.get("test"): self._leaf_sinks(st["test"], e); self._effects(st["test"], e)
                    if st.get("left"):
                        v = self.taint(st.get("iter"), e)
                        for nm in st["left"]: e[nm] = v
                esc = []; self._esc.append(esc)
                try:
                    e0 = dict(env)
                    e1 = dict(env); head(e1); self._walk(st.get("body"), e1)
                    e2 = _ejoin(e0, e1, *esc)
                    e3 = dict(e2); head(e3); self._walk(st.get("body"), e3)
                    _set_env(env, _ejoin(e2, e3, *esc))
                finally:
                    self._esc.pop()
                continue
            if k in ("break", "continue"):
                if self._esc:
                    for lv in (self._esc if k == "continue" else self._esc[-1:]): lv.append(dict(env))
                continue
            if k == "try":
                e_try = dict(env); self._walk(st.get("body"), e_try)
                eh = _ejoin(env, e_try)
                for nm in st.get("param") or []: eh[nm] = Z
                self._walk(st.get("handler"), eh)
                new = _ejoin(e_try, eh) if st.get("handler") else e_try
                self._walk(st.get("finalizer"), new)
                _set_env(env, new); continue
            if k == "switch":
                self._leaf_sinks(st.get("disc"), env); self._effects(st.get("disc"), env)
                esc = []; self._esc.append(esc)
                try:
                    outs, has_default = [], False
                    for c in st.get("cases", []):                 # C#: no implicit fallthrough
                        if c.get("isdefault"): has_default = True
                        e = dict(env); self._walk(c.get("body"), e)
                        last = (c.get("body") or [{}])[-1] if c.get("body") else {}
                        if not (isinstance(last, dict) and last.get("k") in ("break", "return", "throw", "continue")):
                            outs.append(e)
                    if not has_default: outs.append(dict(env))
                    outs += esc
                    _set_env(env, _ejoin(*outs) if outs else env)
                finally:
                    self._esc.pop()
                continue
            if k == "vardecl":
                for d in st.get("decls", []):
                    self._effects(d.get("init"), env)
                    if d.get("name"):
                        init = d.get("init")
                        env[d["name"]] = self.taint(init, env) if isinstance(init, dict) and init.get("k") != "nil" else Z
                        if isinstance(init, dict) and init.get("k") == "call" and _callee_name(init.get("callee")) == "GetRelativePath" \
                                and len(init.get("args", [])) > 1 and self._target(init["args"][1]):
                            self.relof[d["name"]] = self._target(init["args"][1])
                        rx = self._regex_of(init) if isinstance(init, dict) and init.get("k") == "new" \
                            and "Regex" in (init.get("type") or "") else None
                        if rx is not None: self.regexes[d["name"]] = rx
            elif k == "assign":
                self._effects(st.get("right"), env)
                left = st.get("left", {})
                v = self.taint(st.get("right"), env)
                self._assign_to(left, v, env, st.get("op"))
                if left.get("k") == "ident" and self._ends_sep(st.get("right")): self.sepvars.add(left["name"])
                if left.get("k") == "member" and left.get("prop") == "CommandText":   # cmd.CommandText = concat
                    self._judge(st, "CommandText", "sql", self._ctx_taint(st.get("right"), env, "sql"))
                if left.get("k") == "member" and left.get("prop") == "Mode" and _qual(st.get("right")).endswith("LiteralMode.Encode"):
                    self.encoded.add(_path(left.get("object")))
                ctl = self.ftypes.get(_base_ident(left.get("object")) or "", "")
                if left.get("k") == "member" and left.get("prop") in ("InnerHtml", "Text") \
                        and _path(left.get("object")) not in self.encoded \
                        and ctl not in ("TextBox", "HiddenField", "DropDownList", "ListItem", "Button", "LinkButton",
                                        "CheckBox", "RadioButton", "TableCell") \
                        and (left.get("prop") == "InnerHtml" or self.webforms):     # WebForms Literal/Label.Text
                    self._judge(st, "." + left["prop"], "xss", self._ctx_taint(st.get("right"), env, "xss"))
            elif k in ("return", "throw", "exprstmt"):
                self._effects(st.get("argument") if k != "exprstmt" else st.get("x"), env)
                if k == "return" and self._rets is not None:
                    a = st.get("argument")
                    self._rets.append(self.taint(a, env) if isinstance(a, dict) and a.get("k") != "nil" else F)
            self._leaf_sinks(st, env)
            self._lambdas(st, env)

    # ---------- passes ----------
    def _param_source(self, p, action):
        attrs = p.get("attrs", []) or []
        typ = (p.get("typ") or "").split("<")[0].split(".")[-1].rstrip("?")
        if typ in NUM_TYPES or any(f"<{t}>" in (p.get("typ") or "") or (p.get("typ") or "") == t + "[]" for t in NUM_TYPES):
            return False                                        # a bound number / Guid carries no text
        if any(a in FROM_ATTRS for a in attrs): return True
        if action and typ in TAINT_TYPES: return True
        if action and p.get("typ", "").split("<")[0] in SIMPLE_TYPES and not attrs: return True
        return False

    def _enter(self, fn):
        self.vt = {p.get("name"): (p.get("typ") or "").split(".")[-1].rstrip("?") for p in fn.get("params", [])}
        self.reqbases = set(REQUEST_BASES) | {p for p, t in self.vt.items() if t in REQ_TYPES}
        bases = fn.get("bases") or ""
        self.webforms = any(b.strip().split(".")[-1] in ("Page", "UserControl", "MasterPage") for b in bases.split(","))
        self.regexes = dict(self.fregexes); self.relof = {}; self.encoded = set(); self.bound = set()
        self.sepvars = set()  # `if (!root.EndsWith(sep)) root += sep;`: root ends with a separator

    def _summ_of(self, fn):
        params = [p.get("name") for p in fn.get("params", [])]
        saved = (self.sinks, self._rets)
        self._enter(fn)
        def run(env):
            self.sinks, self._rets = [], []
            self._walk(fn.get("body"), env)
            got = {}
            for (l, m, ctx, d) in self.sinks:
                key = (l, m, ctx)
                if _DRANK[d] > _DRANK.get(got.get(key), -1): got[key] = d
            return (join(*self._rets) if self._rets else F), got
        try:
            base, bs = run({p: F for p in params if p})
            summ = {"sinks": {}, "passes": set(), "params": params, "base": base, "ret": []}
            numeric = {q.get("name") for q in fn.get("params", []) if (q.get("typ") or "").rstrip("?") in NUM_TYPES}
            for i, p in enumerate(params):
                env = {q: F for q in params if q}
                if p and p not in numeric: env[p] = T
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
            self.sinks, self._rets = saved

    def index(self, tree):
        for fn in tree.get("funcs", []):
            if fn.get("name") and fn["name"] != "<top>": self.funcs.setdefault(fn["name"], []).append(fn)
        for ty in tree.get("types", []):
            self.ptypes.setdefault(ty.get("name"), {}).update({p.get("name"): (p.get("typ") or "").rstrip("?") for p in ty.get("props", [])})
        self.enums |= set(tree.get("enums", []))
        for fd in tree.get("fields", []):                   # static readonly Regex X = new Regex("..")
            init = fd.get("init")
            self.ftypes[fd.get("name")] = (fd.get("typ") or "").split(".")[-1]
            if init is None: continue
            self.ffields[fd.get("name")] = init
            if isinstance(init, dict) and init.get("k") == "new" and ("Regex" in (init.get("type") or "") or "Regex" in (fd.get("typ") or "")) \
                    and init.get("args") and _lit(init["args"][0]) is not None:
                self.fregexes[fd.get("name")] = _lit(init["args"][0])
        self._dirty = True

    def _all_nodes(self, n):
        if isinstance(n, dict):
            yield n
            for v in n.values(): yield from self._all_nodes(v)
        elif isinstance(n, list):
            for x in n: yield from self._all_nodes(x)

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
            action = fn.get("action", False)
            env = {p["name"]: (T if self._param_source(p, action) else F)
                   for p in fn.get("params", []) if p.get("name")}
            self.bound = {p for p, v in env.items() if v == T}
            self._rets = None
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
    if not os.path.exists(CSAST):
        raise RuntimeError("cs2zfl: csast helper not built -- run `dotnet build -c Release -o bin/pub` in csast/")
    out = subprocess.run([CSAST, path], capture_output=True, text=True, timeout=60)
    if out.stdout.strip(): return json.loads(out.stdout)
    raise RuntimeError("cs2zfl: parser produced no output for %s: %s" % (path, out.stderr.strip()[:200]))

def analyze(path): return Engine().run(parse(path))

UNPARSED = []     # files the last analyze_app could not parse: NOT analysed, NOT clean

def analyze_app(paths):
    e = Engine(); trees = []
    del UNPARSED[:]
    for p in paths:
        t = parse(p)
        if t.get("error"): UNPARSED.append((p, str(t["error"])[:60])); continue
        if t.get("funcs") or t.get("fields") or t.get("types"): trees.append((p, t)); e.index(t)   # a designer file: control types
    out = []
    for p, t in trees:
        for rec in e.judge(t): out.append((p,) + rec)
    return out

if __name__ == "__main__":
    for ln, m, ctx, d in analyze(sys.argv[1]):
        print(f"  L{ln}: {d:8} [{ctx}] {m}")
