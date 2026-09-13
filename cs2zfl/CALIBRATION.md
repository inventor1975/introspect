# cs2zfl — calibration (2026-09-13, MEASURED)

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
