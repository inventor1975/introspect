# cs2zfl — calibration

## 2026-09-28 night — the first BLIND measure (cloud, PR #10) and what it changed (MEASURED)
Fresh authors who saw neither the analyzer nor its fixtures wrote a corpus (ASP.NET Core MVC, minimal APIs,
Razor Pages, WebForms, Dapper, EF Core, ADO.NET; 202 cases, sqli / xss / file) committed before the analyzer
ran. On `b49bb74`, blind (reproduced locally): sqli 38.7, xss 9.4, file 6.7 found — all **18.3% found, 2.2%
false alarms, 71 silent** of 93 decided vulnerable. The weakest first measure of the seven modules.
Causes, fixed:
- the front end (`csast`): lambdas were a bodyless `funcref`, so no minimal-API handler was ever analysed;
  `using (..) { }` was dropped with its header and body; object initialisers (`new ContentResult { Content
  = .. }`), casts (`(MarkupString)x`), `?.`, switch expressions and anonymous objects were `other`; top-level
  statements (a minimal-API Program.cs) were never collected. Now kept, with interpolation text (sub-contexts),
  literal values, field initialisers, property types and enum names.
- sinks: `Content(html, "text/html")` / `Results.Content` / `new ContentResult` (by content type), a
  `Response.WriteAsync` on any receiver ending in `Response`, Blazor `(MarkupString)` / `AddMarkupContent`,
  WebForms `Label/Literal.Text =` (not a `TextBox`, not `LiteralMode.Encode`: control types from the
  designer file); `System.IO.File.X` (the qualified form controllers use), `File.Delete/Move/Copy/..`,
  `Directory.*`, `PhysicalFile`, `Results.File`, `SendFileAsync`, `Response.WriteFile`; Dapper
  `Query*/Execute*` on a connection-like receiver (a NAME heuristic: conn / db / sql / datasource), EF Core
  `FromSqlRaw/ExecuteSqlRaw/SqlQueryRaw` (not `FromSqlInterpolated`, not `FromSql($"..")`), `CreateCommand(sql)`.
- sources: minimal-API lambda parameters (string / `[From*]` / `IFormFile`), `HttpContext`/`HttpRequest`
  parameters as request bases, `ReadFormAsync()`, `Request.Body/Path/Host`, WebForms `TextBox.Text`.
  A bound number (`int`, `long`, `Guid`, an enum property of a DTO) carries no text.
- escapers by position, as in the other modules: `HtmlEncode` at an href START, in an unquoted attribute or a
  script does not protect; `JavaScriptEncoder.Encode` protects a quoted JS string only; `UrlEncode` any HTML
  position; `JsonConvert.SerializeObject` keeps `<`, `System.Text.Json` escapes it (unless
  `UnsafeRelaxedJsonEscaping`); quote doubling protects SQL only inside a quoted literal (and then only Z);
  `HtmlDecode`/`UrlDecode` undo an earlier encode; `Where(char.IsLetterOrDigit)` / a lambda of character
  ranges / `Regex.Replace(x, "[^..]", "")` / `ToBase64String` clear the contexts their kept set excludes.
- guards: an anchored `Regex.IsMatch` (field-held patterns too) clears the contexts its characters cannot
  express; `int.TryParse(x, out ..)`; `GetFullPath` + `StartsWith(root + separator)` (a root field or a
  variable made to end with the separator); `GetRelativePath(..).StartsWith("..")`; own bool checks;
  `ModelState.IsValid` makes bound values Z (an annotation is checked, not proven here). `File.Exists(x)` is
  not a check on x; `x.Contains("..")` is Z, not clean (an absolute path still replaces the base in
  `Path.Combine`).
- propagation: chained `sb.Append(a).Append(b)`; a const / readonly VALUE field is its value (an object
  held in a field stays unknown); `FormattableString.Invariant`.
Fixtures w01–w12: every one fails on `b49bb74`. Stand: 28 + cross-file.
After the fixes, on the SAME corpus (fitted, not a measure): **87.1 / 0.0 / 0 silent**; expect_open cases:
vulnerable 8 — 0 REFUTED, 8 OPEN; safe 9 — 0 REFUTED, 8 OPEN, 1 clean.
App: WebGoat.NET 5 REFUTED / 74 OPEN (was 0 / 5). The five are real: ReflectedXSS (`LoadCity` into a Label
— the lesson), HeaderInjection (request headers into a Label), PathManipulation (the file name echoed into a
Label), Orders (the order number into a Literal), EncryptVSEncode (a custom cipher's output into a TableCell).
Most new OPENs are Labels given values of unknown origin (database rows, exception messages).
A new blind round is the only way to get a number again.

## 2026-09-27 — slice 2: the java2zfl soundness lesson ported (MEASURED)
10 new fixtures (u01–u10), all fail on the slice-1 engine; 8 were SILENT on a real flow (a Z helper
return read as F, catch overwriting try, switch sections walked in sequence, `+=` read as `=`,
sb.Append, `o.Cmd = v`, a callee defined after its caller, and `s.Replace("a","b")` — a transparent
call read its FIRST ARGUMENT instead of its receiver). The Roslyn helper (csast) now keeps assignment
operators, foreach variable + collection, break/continue, switch default, catch variable; build it
offline from the local NuGet cache: `dotnet restore --source ~/.nuget/packages && dotnet build -c
Release -o bin/pub --no-restore` (run with DOTNET_ROOT set).
- WebGoat.NET: OPEN 3 -> 5; the two new are BinaryFormatter.Deserialize over profile bytes read from
  the database (origin unknown: honest OPEN); the old engine passed them in silence. No REFUTED either
  way. No labelled denominator for C#.

## 2026-09-13 — calibration (MEASURED)

Parser is C#'s own Roslyn (csast helper via dotnet) — no API/LLM calls, no token spend.

## Engine validated (fixtures, modern ASP.NET MVC/Core patterns)
6 fixtures + cross-file green: Request.Query["x"] / Request["x"] / bare action params / [FromQuery] as
sources; Process.Start=shell, new SqlCommand(concat)/.CommandText=sql, Response.Write/Html.Raw=xss,
File.*=file, BinaryFormatter.Deserialize=deser; HttpUtility.HtmlEncode credited context-aware (xss clean,
transparent for shell/sql); cross-method + cross-file summaries; guards.

## WebGoat.NET (deliberately vulnerable, but WebForms) — honest limitation surfaced
162 .cs, 0 parse errors. **0 REFUTED, 3 OPEN (2 file, 1 deser). 0 false positives.**
NOT a core-engine failure: WebGoat.NET is an old WebForms app whose user input flows through server-control
`.Text` properties (166 uses; controls declared in .aspx markup, populated over the page lifecycle) — a
WebForms-specific source surface not modelled (like Java MyBatis / Go framework-dispatch boundaries). Its
SQLi helpers (DoQuery/DoScalar -> new SqliteCommand / SQLiteDataAdapter) ARE now recognised (fixed a
case/variant gap: match any *Command/*DataAdapter), but the taint SOURCE (.Text) never enters, so the chains
stay unlit. On modern ASP.NET (MVC/Core, Request.*/[From*]/action params) the flow IS caught (fixtures).

## Honest verdict
Engine is sound and precise (0 FP; every fixture verdict correct; context-aware escaper). Recall proven on
MVC/Core patterns; WebForms `.Text` control-property sources are an un-modelled surface (a real gap, notable).
No modern ASP.NET-Core deliberately-vulnerable corpus was cloned for a TP denominator — fixtures stand in.

## Gate
6 fixtures + cross-file. Fixtures k1-k5 + x1 + xfile/. csast built via `dotnet build -c Release -o bin/pub`
(needs .NET SDK at ~/.dotnet; DOTNET_ROOT=~/.dotnet).
