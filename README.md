# Finding Alphas — Distilled Notes

Two layers. Underneath: operational notes distilled from *Finding Alphas: A Quantitative Approach to Building Trading Strategies*, 2nd ed. (Tulchinsky et al., WorldQuant / Wiley, 2020) — definitions, the expression vocabulary, checklists, transcribed formulas. On top: **the operating layer this programme actually runs on** — the daily loop, the lens method and its corpora, the alpha log, and the ops runbook. The book is the reference; the operating layer is what changed as a result of running it.

**How to use:** work in this directory (`CLAUDE.md` loads the rules), or upload the doc(s) for the part you're working in. The "reach for it when" column says which. Docs cross-link with `[[name]]`.

> **Read `CLAUDE.md` first.** One rule governs every session here: **one step per turn** — announce
> what the step will do, ask, **wait**, do exactly one step, show what it produced, ask again. It
> cannot be turned off. Full text in `part-0-daily-workflow` §"How this loop is RUN".

---

## Index

### The operating layer *(not from the book)*

| Doc | What's in it | Reach for it when… |
|---|---|---|
| `CLAUDE.md` | The one-step-per-turn rule, always in force. Loads automatically in this directory | every session, before anything |
| `part-0-daily-workflow` | **START HERE.** The spine — Step 0 pick the corner → **Step 1 pick a SOURCE** (cookbook / SSRN / Seeking Alpha / lens corpus) → **Step 1b EDA + the decay-first gate** → express → backtest → refine → kill-test → correlate + log → pre-commit exit. Also: the step-gate rule, and FINDINGS-vs-VERDICTS | every session — it's the spine |
| `lenses.md` | The lens method: 15 lenses, the two builds (CORPUS vs PERSONA), the two ledgers (ALPHA vs METHOD), the two scores (generation vs conversion), the standing constraints, and the #041 method test kept as history | picking where to look; adding or scoring a lens |
| `lenses/*.md` | One file per lens. A CORPUS lens carries its question, boundaries, `Forbidden`, EDA list and **GREP LOG** — no pre-written fundamentals; claims are derived from the sources at pass time and cited | running a lens pass, one at a time |
| `lenses/_material/` | The corpora themselves — indexed, with a `.txt` twin per chapter for grep. `index_corpus.py` turns any bookmarked PDF into that shape | reading source material; adding a new book |
| `alpha_log.md` | **The batch tracker.** One entry per tested alpha, kept or killed. Verdict tiers (`KILLED` vs `PARKED-*`), the FINDINGS-vs-VERDICTS rule and its six reversals, the methodology roadmap | Step 0 (empty corners) and Step 6 (uniqueness) — both depend on it |
| `overnight_results.md` | A METHOD-ledger measurement batch — discovery sample only, `K` unaffected. The template for method work that must not inflate an alpha's trial count | running measurements about our own process |
| `ops-live-scheduling` | **Runbook.** Live strategies on the Windows box: one-shot per-minute "tick" tasks (not daemons), `pythonw` for no console flash, exact Task Scheduler settings, health checks. *A kill is not done until `Get-ScheduledTask` is clean* | deploying / babysitting a strat on the live FTMO demo |
| `data-hygiene` | **What a "price" is allowed to be.** `p = m + c·b` and its two fake-alpha modes (Roll bounce, scheduled-spread drift); both-sides/mid/spread-as-cost rules; the mandatory gross mid-to-mid tripwire; PIT; limit-order adverse selection. Code twin: `backtest_engine2/data_hygiene.py` | onboarding ANY new data source; any intraday or clock-anchored signal; any time a backtest looks too good |
| *(engine convention)* | **Notebook plots + layout** (2026-07-17): every notebook cell ends with a representative plot — glanceable without reading code — via `backtest_engine2/cellplot.py`, saved to `notebooks/<name>/plots/` so the folder reads as a visual table of contents. Rule in `backtest_engine2/PROTOCOL.md §5.1`; notebooks always in `notebooks/<name>/`, never repo root | writing or reviewing ANY notebook — EDA included |

### The book *(Tulchinsky et al., distilled)*

| Doc | Chapters | What's in it | Reach for it when… |
|---|---|---|---|
| `part-1-introduction` | 1–3 | What an alpha *is* (idea → expression → positions), alphas live on data *changes*, EMH/why alphas exist, the UnRule & cutting losses | you want the philosophy / framing |
| `part-2a-build-loop` | 4–6 | The 4 design decisions, the Ch. 5 refine-loop template (neutralize→rank→decay), metric formulas, data validation | starting a new alpha from scratch |
| `part-2b-cost-and-uniqueness` | 7–8 | Turnover, the crossing effect, correlation math (Pearson/temporal/generalized/position/trading) | judging tradability & uniqueness |
| `part-2c-overfitting-defense` | 9–10 | Luck-Sharpe table, true-OOS rules, IR=IC·√breadth, systematic + behavioral biases | validating a signal is real, not fitted |
| `part-2d-robustness-risk-and-tooling` | 11–17 | TAP search framework, robustness transforms (rank/Fisher/Z/winsorize), risk factors (CAPM/APT/neutralization), drawdowns/bootstrapping, automated search, ML, algo toolkit | hardening, risk-managing, or scaling alphas |
| `part-3a-price-volume-momentum` | 18, 21 | Price/volume signals, momentum-reversion by horizon, MACD/ATR, momentum variants | building market-data signals |
| `part-3b-fundamentals` | 19, 20 | Four statements, Piotroski factor catalog, accruals anomaly, factors→alphas rules | building fundamental alphas |
| `part-3c-text-news-analyst` | 22, 24 | News dimensions (sentiment/novelty/relevance/category), 7 analyst alpha formulas | using news / social / analyst data |
| `part-3d-options` | 23 | Put-call parity + the 4 options alphas (skew, spread, O/S, OI) | mining the options market for stock signals |
| `part-3e-events-and-index` | 25, 28 | Merger/deal spread, spin-offs, distressed, index-arb fair value, reconstitution impact | event-driven & index strategies |
| `part-3f-microstructure-intraday` | 26, 27 | Illiquidity premium, Glosten-Milgrom/PIN/DPIN, intraday mean-reversion variants | high-frequency / intraday / microstructure |
| `part-3g-etfs-futures` | 29, 30 | ETF merits/risks/traps, futures grouping & √breadth, COT/seasonality/risk-on-off/carry | other asset classes (ETFs, futures, FX) |
| `part-4-websim` | 31 | WebSim/BRAIN platform: alpha structure, settings table, reading results, worked expressions | testing ideas on WorldQuant BRAIN |
| `part-5-habits` | 32 | Seven habits + the risk–reward task-prioritization matrix | non-technical; prioritizing research effort |

---

## Also here, not indexed above
- `substack-01-do-alphas-exist.md` + `substack_plots/` — a write-up of the programme for a general
  reader, built from the log's own corpses. Not part of the pipeline.
- Loose `x0NN_*.py` at repo root — one-off analysis scripts from recent arcs (e.g.
  `x047b_impact_multi.py`, impact decay across instruments). Working files, not methodology.

## Notes on fidelity
- Formulas were transcribed from **rendered page images** (the PDF text layer dropped math). Written in plain notation (Σ, √, superscripts) for clean upload.
- Style: summary notes leaning operating-manual; each Part II–III doc ends with an actionable checklist.
- Ch. 16 (ML) is flagged in-doc as the weakest/most dated; Ch. 19+20 were merged (heavy overlap).
- "WebSim" in the book = today's **WorldQuant BRAIN** (`platform.worldquantbrain.com`).
- **The `part-3*` files are two things at once**, and Step 1 treats them differently: a *catalog* of
  named published effects (skew, accruals, COT, reconstitution) which is one of the four sources of
  claims, and a *recipe book* of instruments and method (Glosten-Milgrom, DPIN, put-call parity,
  "use rate-of-change not levels", PIT data, normalize by total assets) which is a toolbox serving
  every step. Only the catalog half is a source.
