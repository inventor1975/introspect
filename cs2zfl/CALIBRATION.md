# cs2zfl — calibration

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
