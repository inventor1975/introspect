# cs2zfl on a blind corpus (2026-09-27)

Until now cs2zfl had no outside measure. Everything rested on fixtures written by the analyzer's own author.
This is its **first** held-out measure: cases written by authors who had seen neither the analyzer nor its
fixtures, **committed before cs2zfl was first run on them**.

## Pre-registration

| | |
|---|---|
| corpus commit (pre-registration) | **`dede0dfa820624b13966f40687e9ed63034145ac`**: `cases/`, `labels.csv`, `score.py` (the verdict rule) and `parsecheck/` |
| analyzer measured | introspect **`b49bb74`** (`main`; `cs2zfl.py` and `csast/` unchanged by this branch) |
| environment | .NET 8 SDK from Ubuntu's archive (apt `dotnet-sdk-8.0` 8.0.131), because `builds.dotnet.microsoft.com` is denied by the environment's egress policy; `csast` built in `cs2zfl/csast/bin/pub` |
| after the run | `cases/`, `labels.csv` and `score.py` unchanged; `analysis.csv` and this report added |

```bash
git checkout bench/csharp-blind-2026-09
export DOTNET_ROOT=/usr/lib/dotnet
(cd cs2zfl/csast && dotnet build -c Release -o bin/pub)
python3 cs2zfl/blind/score.py                                  # every number below
git diff dede0df -- cs2zfl/blind/cases cs2zfl/blind/labels.csv cs2zfl/blind/score.py   # empty
(cd cs2zfl/blind/parsecheck && dotnet build -c Release -o bin/pub)
cs2zfl/blind/parsecheck/bin/pub/parsecheck $(find cs2zfl/blind/cases -name '*.cs')   # 218 parsed, 0 failed
```

**Who wrote what.**
- **Authors:** fresh sub-agents, one per category, with no context from the measuring session.
- **What they could read:** only `INTROSPECT-SEMANTICS.md` and `cs2zfl/README.md`. **There is no
  `cs2zfl/README.md` on `main`**, so in practice they could read only `INTROSPECT-SEMANTICS.md`.
- **Forbidden:** the module source (`cs2zfl.py`), its parser front end (`csast/`), the fixtures, the tests,
  `CALIBRATION.md`, every `blind*` folder, and git history.
- **The measuring session** wrote only `score.py`, adapted from the earlier rounds, and the parse-check
  tooling in `parsecheck/`.
- **The analysis** (this report and `analysis.csv`) was done after the run by a separate sub-agent, not
  blind, which read the analyzer and confirmed every cause. The measuring session re-checked a sample of the
  causes by reproduction before committing.

**Limits.** The authors are the same model family that wrote the analyzer. They report reading nothing
else, which cannot be verified from outside.

**No deserialisation or command-injection cases.** The authors of **`deser`** and **`cmdi`** were each stopped
by a safety filter while generating, and wrote nothing. As the task says, these categories were skipped and
the task was **not** rephrased to get around the filter. Nothing below speaks about cs2zfl's `deser` or
`shell` contexts.

**The corpus:**
- 202 labelled cases: sqli 69, xss 68 and file 65, about half vulnerable.
- 16 helper files under `*/lib/`.
- ASP.NET Core MVC and API controllers, Razor Pages, minimal APIs, one Blazor component and WebForms
  code-behind; ADO.NET, Dapper and EF Core.

**Parsing.** `csast` reports `error` only when it throws an exception, never on a Roslyn syntax diagnostic,
so `cs2zfl.UNPARSED` can hardly ever be non-empty. The authors' check, `parsecheck` (Roslyn 4.11
`GetDiagnostics`, errors only), confirmed that all 218 files parse without syntax errors. It was re-run
for this report with the same result.

## How it is scored

This is the task's rule, fixed in `score.py` before the run. `cs2zfl.analyze_app` runs over all 218 files at
once, as `introspect.py` runs it. A case's verdict is the worst record of its category's context (`sql`,
`xss`, `file`) **in that case file**, in the order REFUTED > OPEN > SILENT. Files in `cs2zfl.UNPARSED` are
listed separately. **There are none.**

## Results

| category | label | expect_open | n | REFUTED | OPEN | SILENT |
|---|---|---|--:|--:|--:|--:|
| sqli | vulnerable | no | 31 | 12 | 3 | **16** |
| sqli | vulnerable | yes | 2 | 0 | 1 | 1 |
| sqli | safe | no | 34 | **2** | 9 | 23 |
| sqli | safe | yes | 2 | 0 | 1 | 1 |
| xss | vulnerable | no | 32 | 3 | 1 | **28** |
| xss | vulnerable | yes | 3 | 0 | 0 | 3 |
| xss | safe | no | 30 | 0 | 0 | 30 |
| xss | safe | yes | 3 | 0 | 0 | 3 |
| file | vulnerable | no | 30 | 2 | 1 | **27** |
| file | vulnerable | yes | 3 | 0 | 0 | 3 |
| file | safe | no | 28 | 0 | 2 | 26 |
| file | safe | yes | 4 | 0 | 0 | 4 |

Decided cases only (expect_open = no):

| category | vulnerable: REFUTED / OPEN / SILENT | safe: REFUTED / OPEN / SILENT | TPR | FPR |
|---|---|---|--:|--:|
| sqli | 12 / 3 / **16** of 31 | **2** / 9 / 23 of 34 | 38.7% | 5.9% |
| xss | 3 / 1 / **28** of 32 | 0 / 0 / 30 of 30 | 9.4% | 0.0% |
| file | 2 / 1 / **27** of 30 | 0 / 2 / 26 of 28 | 6.7% | 0.0% |
| all | 17 / 5 / **71** of 93 | **2** / 11 / 79 of 92 | 18.3% | 2.2% |

**The low FPR is not evidence of precision.** Of the 79 decided safe cases that are SILENT, 69 are silent
because no sink of their context was judged at all. Only 10 were judged and cleared (EARNED). The gaps that
silence the vulnerable cases below also hide the safe ones.

**Records outside the scored cells:**
- **One OPEN in a helper file,** `file/lib/DocumentStore.cs:22` (`File.ReadAllBytes`).
  - It comes from the judge walk of the helper itself. `Load(name)` is not an action, so `name` is F. The
    `_root` field is unknown (Z), so `Path.Combine(_root, name)` is Z.
  - It is an honest "don't know" on library code, not a false alarm.
  - The same function makes `file/ContractArchiveController` a hit (`Load()->sink`, REFUTED).
- **No REFUTED in any case file outside its own category.**
- **One record in another context:** an OPEN `[deser] Deserialize` at `sqli/ExportPresetController.cs:33`.
  - It is a `System.Text.Json` `JsonSerializer.Deserialize<T>` of a file on disk, matched by the bare
    method name.
  - It is not scored and not an alarm.

## 1. Every silence on a vulnerable case: 78 (71 decided + 7 expect_open)

A silence is a contract breach: it reads as "clean".
- **77 of the 78 have no sink of their context judged at all.** The other one (`BulkStatus`) is judged and
  cleared (EARNED).
- **By the stage where the flow is lost:** 58 at the sink, 17 at the source, 3 in propagation.
- **Cases with more than one gap** are listed at the earliest point on the path where the flow becomes F or
  stops being analysed. The other gaps are named in `analysis.csv`.
- **None of the 78 has a record in a helper file or in another context.**

**How each cause was confirmed:**
- A subclass of `Engine` recorded every sink the judge walk evaluated, with its taint letter, including the
  EARNED ones the module drops.
- Every case was read against the analyzer code.
- Each cause was reproduced on a minimal file run through the unmodified analyzer.
- A throwaway what-if run checked that closing the named gap(s) makes each case non-silent. It used an
  extended sink list, a `csast` copy that also emits lambda bodies, `using` blocks and object initialisers,
  extra request bases, and folding of chained `Append` calls.

### Sink: 58

| n | cause | cases |
|--:|---|---|
| **15** | **XSS: `Content(html, "text/html")` is not a sink.** The xss sinks are only `Response.Write/WriteAsync` (receiver literally `Response`), `Html.Raw` and `new HtmlString`. With it as a sink, 10 would be REFUTED and 5 OPEN; the OPEN values come from session state, DI, anonymous-object serialisation, a catch variable and the fields of a fluent builder. | `AccountHeader`, `BackLink`, `CategoryLabel`, `CouponBanner`, `Feedback`, `InvoiceHeader`, `NewsletterConfirm`, `Notice`, `ReviewPreview`, `Search`, `CheckoutConfig`, `LandingPage`, `ReportSort`, `Alerts` (eo), `Nickname` (eo) |
| **10** | **File: `System.IO.File.X(..)` is not recognised.** The file sink test reads the callee's base identifier, which is `System`, not `File`. Inside a controller the qualified form is the norm, because `ControllerBase.File(..)` shadows the type: 24 corpus files use the qualified form, 5 the plain one. | `Changelog`, `EvidenceViewer`, `ExportArchive`, `Glossary`, `LocaleBundle`, `ManualPages`, `SnapshotExport`, `TemplatePreview`, `AssetProxy` (eo), `ExportSession` (eo) |
| **10** | **SQL: Dapper and EF Core raw-SQL calls are not sinks.** The sql sinks are only `new *Command/*DataAdapter(arg0)` and `.CommandText = ..`. Dapper: `Query`, `QueryFirstOrDefaultAsync`, `ExecuteAsync`, `ExecuteScalar` (6 cases, one through the cross-file `CatalogRepository`). EF Core: `FromSqlRaw`, `ExecuteSqlRaw(Async)` (4 cases). | Dapper: `CustomerDirectory`, `LoyaltyPoints`, `ProfileBio`, `StoreLocator`, `CatalogSearch`, `ReferralLeaderboard` (eo). EF: `ArchiveCleanup`, `CartMaintenance`, `CategoryBrowse`, `SupplierSearch` |
| **7** | **File: methods missing from the catalogue.** `FILE_METHODS` has no `Delete`, `Move` or `Copy`, and no `Directory.*` method is a sink. | `AttachmentRemoval`, `BulkPurge`, `DraftRename`, `MediaDuplicate`, `StoredUploads` (eo), `SharedFolderBrowser` (`GetFiles`), `WorkspaceCleanup` (`Directory.Delete`) |
| **6** | **File: framework file responses are not sinks:** `PhysicalFile(..)` (5 cases) and WebForms `Response.WriteFile(..)` (1). | `FirmwareImages`, `InvoiceDownload`, `ProjectFiles`, `SpecSheet`, `TenantAssets`, `DocumentViewerPage` |
| **4** | **A `using (..) { }` statement is dropped.** `csast` emits it as `other` with no children, so a sink in its header or body is never evaluated. `using var x = ..;` declarations are kept. | `OrderHistory.aspx`, `OrderSearch`, `ReviewModeration`, `PluginInstall` (also `System.IO.File.Create`) |
| 3 | **Wrong-context escaping is credited.** `HtmlEncode` clears the single `xss` context, but the value lands in an unquoted JavaScript expression, a `javascript:` URL in `href`, and an unquoted `class` attribute. Each would be EARNED even if the output call were a sink. The output calls are `Content(..)` and `new ContentResult { Content = .. }`; `csast` drops that initialiser. | `ChartEmbed`, `ProfileLink`, `ThemeWidget` |
| 3 | **Other HTML outputs are not sinks:** WebForms `Literal.Text = ..` (an assignment); `context.Response.WriteAsync(..)` (the receiver's base is `context`, not `Response`); Blazor `builder.AddContent(.., (MarkupString)..)`, where `csast` also erases the cast. | `ContactThanks.aspx`, `Guestbook`, `AnnouncementBar` |

### Source: 17

| n | cause | cases |
|--:|---|---|
| **16** | **Minimal-API lambda handlers are never analysed.** `csast` turns every lambda into a bodyless `funcref` and collects only methods, constructors and local functions, so neither the lambda's parameters nor its body are seen. Only `ProductSku` would be REFUTED with the lambda walked. The other gaps behind this group: `Results.Content`, `Results.File`, `SendFileAsync` and `CreateCommand` are not sinks. `ctx`, `request` and `req` are not request bases, and `HttpContext`/`HttpRequest` parameters are not sources, so `LogTail`, `CampaignLanding`, `TagCloud` and `AdvancedSearch` would read F (EARNED). `ReadFormAsync()` reads Z. | file: `JournalWriter`, `LogTail`, `ReportEndpoints`, `SignedDownload`, `ThemeStylesheet`; sqli: `AdvancedSearch`, `Newsletter`, `ProductSku`; xss: `CampaignLanding`, `ColorSwatch`, `DocsPage`, `Greeting`, `KeywordHighlight`, `StatusBoard`, `TagCloud`, `WishlistShare` |
| 1 | **An `IFormFile` parameter is not a source.** It is neither a simple type nor marked with a `From*` attribute, so `avatar.FileName` is F. The `new FileStream` sink is also inside a dropped `using` statement. | `AvatarUpload` |

### Propagation: 3

| n | cause | cases |
|--:|---|---|
| 2 | **Chained `Append` drops values.** In `sb.Append(a).Append(b)` only the innermost call's receiver is a local, so only its argument is folded into `sb`. `BulkStatus` is judged at `CommandText` and cleared (EARNED). | `BulkStatus`, `ProductQuestions` (eo) |
| 1 | **`HtmlDecode` is transparent,** so the xss-clean state set by `HtmlEncode` survives the decode. `Content(..)` is not a sink either. | `MessageRelay` |

**What-if run with all the named gaps closed** (an illustration of the causes, not a measure):
- 56 of the 71 decided silences become REFUTED, 11 OPEN, and 4 stay EARNED (the three wrong-context
  escapers and `MessageRelay`).
- All 7 expect_open silences become OPEN.
- The same run also turns 12 more decided safe cases and 2 expect_open safe cases into REFUTED.

## 2. Every false alarm: 2 (both decided)

| n | stage | cause | cases |
|--:|---|---|---|
| 1 | guard | **A regex validation is not recognised.** In `if (!Identifier.IsMatch(table)) return ..;` the anchored identifier regex is ignored, because `_guard` knows only `x == literal`, `x != literal` and `Contains/ContainsKey/Any(x)`. The table name stays T at `new SqlDataAdapter`. | `ExportTable` |
| 1 | source | **Types are not tracked.** In `query.Region.ToString()` every member of a `[FromBody]` parameter inherits its T, so an enum-typed property is not seen as a name or digits. | `RegionalSales` |

`analysis.csv` holds the cause per case; `score.py` prints it next to each label's reason.

## 3. Counted

- **Hits:** 17 of 93 decided vulnerable cases (sqli 12/31, xss 3/32, file 2/30). None of the 8
  expect_open vulnerable cases was refuted.
- **OPEN, decided cases:** 5 of 93 vulnerable and 11 of 92 safe.
- **OPEN, expect_open cases:** 1 of 8 vulnerable and 1 of 9 safe.

## 4. Labels

Labels were not changed after the run. Rereading the 80 disagreements found none that is wrong.

Two groups depend on framework behaviour. I agree with their labels:
- **Route values:** the single-segment route values in `Changelog`, `AttachmentRemoval`, `LocaleBundle`,
  `ReportEndpoints` and `TenantAssets` carry `../` only as `%2F`-encoded slashes, which ASP.NET Core routing
  decodes.
- **`ContactThanks.aspx`** relies on `Literal`'s default mode passing HTML through unchanged.

The authors raised no label judgement calls in their hand-back reports. The `file` author noted that a
vulnerable case uses a method named `StripTraversal`, which is ordinary code naming, not a label hint.

## AI disclosure

The cases were written by Claude (Anthropic) sub-agents under the reading rules above. The scoring, the
analysis and this report are also by Claude, with **Vitaly Reznik** as curator. This branch changes nothing
outside `cs2zfl/blind/`.
