# Lenses — idea generation by discipline

*Companion to [[part-0-daily-workflow]]. **One of the four sources at Step 1** — alongside the cookbook
catalog, SSRN/papers, and Seeking Alpha/Wilmott. Not a replacement for them.*

Built 2026-08-15 after four consecutive paper-sourced arcs (#037-#040) died or parked. Diagnosis at the
time: the pipeline is **generation-starved, not validation-starved** — the kill machinery is fast and
reusable, while the idea supply was artisanal and literature-bound.

**Revised 2026-08-22 (user's call).** The original conclusion — that literature-bound ideas are
pre-crowded *by construction* and must therefore be replaced — was too strong. Crowding is not a
property of where an idea came from; it is a property that can be **measured**, and a crowded idea
shows up as a decayed one. Step 1b's **decay-first gate** tests it directly. So every source is
welcome and none is ranked by respectability; what changed is that a lens now reads **book-length
curated material** rather than whatever a search surfaced that morning.

## The rules

1. **A lens is a CORPUS, and a pass derives its claims from it.** *(Rewritten 2026-08-22; previously
   "a lens outputs a PLACE TO LOOK, never a claim.")* The corpus is deep enough to argue with, so a
   pass may take a hypothesis from it — but every claim carries the **file and section** it came from.
   A claim with no citation is a prior wearing a corpus as a costume, and the two are indistinguishable
   on the page without one.
2. **EDA does the talking.** Nothing may be asserted without a number from the EDA behind it.
3. **Whatever the pass carries forward faces Step 1b.** *(Rewritten 2026-08-22; previously "only what
   the EDA surfaces crosses".)* A claim may now originate in the corpus rather than in the data, so the
   EDA's job is **validation** rather than nomination — `skills/14c-eda.md` decomposes it into atomic
   sub-claims with pre-committed decision rules, and the decay-first gate asks whether it is already
   crowded. A corpus claim that fails 1b is rejected exactly like a paper's would be.
4. **Looking is free, crossing is counted.** Explore the discovery sample without limit — no claim
   rests on it. Whatever crosses to the sealed holdout is `K` for the deflated Sharpe
   (`backtest.selection.dsr(returns, K=K)`).
5. **The holdout stays sealed** until the carry list is frozen. Split is a PARAMETER (time,
   instrument, or synthetic) — never hardcoded, because sometimes the right control is synthetic
   data with a known answer.
6. **The economic reason is an EXIT requirement, not an entry one.** You do not need a story to
   look. You need one to deploy — and it only counts if it predicts something not yet examined.
   (Failure mode to avoid: the BoJ-QQE story invented for #038c *after* seeing the result, which
   explained everything and forbade nothing.)
   **Reconciled with Step 1's mandatory test 2026-08-22.** Part 0 says *"no economic reason → drop
   it"*, which reads as an entry gate and appears to contradict this. It does not: that test fires
   when the **one-sentence hypothesis is written at the end of Step 1** — after the corpus work, after
   the looking. Both stand. You may look with no story; you may not leave Step 1 without one; and it
   only counts at deployment if it forbids something.

## Testing vs trials — two ledgers, declared BEFORE the crossing

*Added 2026-08-18 after the user identified that #041 conflated these.*

A **trial** is any hypothesis checked against the sealed sample. Trials are always counted — but they
come in two kinds, and booking them together is what made #041 unreadable:

- **ALPHA trial** — hunting a deployable edge. These are the `K` in
  `backtest.selection.dsr(returns, K=K)` for the candidate being judged.
- **METHOD trial** — spent to answer a question about our own process, not about a market.
  **Permitted** to use the sealed sample (user's call, 2026-08-18: a process that is only ever
  checked against old data can fool itself in ways old data cannot catch). But it is booked to the
  METHOD ledger and does **not** enter any alpha's `K`.

**The rule: declare the ledger before you cross. Undeclared defaults to ALPHA.**

What went wrong in #041: Arm B was correctly pre-declared non-tradable so it would not inflate `K`.
**Arm A never got the equivalent declaration** — its seven crossings were method spend, booked as if
they were an alpha hunt, and then graded with a deployment bar. Retro-classification: those seven are
METHOD trials. The holdout exposure they cost is real and stays on the method ledger.

## How a lens is scored — two scores, kept apart

Also 2026-08-18. A lens is a *generator*; grading it on whether the whole downstream pipeline made
money is a category error, but dropping the money question entirely lets a lens win by being
interesting and useless. So both, never merged:

1. **GENERATION score — per pass, decides roster membership.**
   - *Novelty*: did it point somewhere no other lens pointed? (Convergence = one lens added nothing.)
   - *Non-rediscovery*: is it absent from the kill list?
   - *Yield*: did the EDA there find something **measurable**? Not tradable — measurable.
2. **CONVERSION tally — long-run, per lens, judged over several passes and never over one.**
   Did anything this lens produced reach deployment?

**A lens is not failed on conversion after a single pass.** Re-scored under this: #041's
market-maker and statistician passes score high on generation ([[direction-is-unpredictable]],
[[fx-microstructure-facts]], the capture-fraction gate) and 0/1 on conversion — which is not yet a
verdict on either lens.

## How to run it — ONE LENS AT A TIME

**This is the operating instruction. Do not run lenses in parallel and do not batch them.**

1. **Pick one lens file** from `lenses/`. Read it in full — including its `Log`, and for a CORPUS lens
   its `GREP LOG`, which says what has already been read and what has not.
2. **Work the corpus, then the EDA, and exhaust both.** For a CORPUS lens the reading comes first:
   index → grep → cite → log. For a PERSONA lens there is nothing to read, so it starts at the EDA.
   Follow the thread down to the insight behind the insight. Do not move to the next lens because the
   first one got interesting; move on when it has nothing left to say.
3. **Reason OUT LOUD, conversationally, in small steps** — one question, one measurement, one
   interpretation, then the next question chosen in light of what you just saw. The user is in the
   loop to nudge, and cannot nudge a finished script.
4. **ALWAYS include plots.** Every step. A number in a table is checked by one person; a shape in a
   chart is checked at a glance.
5. **Do not pre-plan the EDA in a big script.** The point is that the next question depends on the
   last answer. Write small, run, look, decide.
6. **Update the lens file as you go.** These are living documents — its `Log`, its unfinished
   business, and any new `Forbidden` rule the pass earned. The MD improves; that is the compounding
   asset, more than any single result.
7. **RESEARCH THE HOW, AND — SINCE 2026-08-22 — THE WHAT AS WELL.** If a pass needs a tool, an
   estimator, a protocol or a methodology it does not already have — a reliability diagram, a CRPS, a
   breakpoint test, a frequency-severity fit, whatever the lens calls for — **web search and read for
   it. Encouraged, no permission needed.** Half of what a discipline is worth is its instruments, and
   guessing at them badly is how a lens gets reduced to a costume.

   **The old guard rail is GONE.** It read *"research supplies the INSTRUMENT, never the HYPOTHESIS"*,
   on the grounds that literature-sourced ideas are pre-crowded by construction. That was replaced by
   a measurement: **the decay-first gate in Step 1b tests crowding directly**, so hypotheses may now
   come from the corpus, from a paper, or from anywhere else. What remains is the citation rule
   (rule 1) and the requirement that everything faces 1b (rule 3).

   **What survives of the original worry:** a *curated corpus* is not the same thing as *whatever a
   search surfaced this morning*. Depth is the point — a chapter that argues its case can be
   disagreed with; an abstract cannot. Prefer the corpus, but do not refuse a source because of where
   it came from.

**Standing constraint — THE LENS PICKS THE PLACE, THE INSTRUMENT FOLLOWS** (2026-08-18).
A lens may point at any market, including ones we have never held and have no data for. Whether the
instrument is obtainable, affordable or FTMO-tradable is a **downstream** check, never an entry
filter. Pulling data is cheap; ideas are the scarce input — that is the founding diagnosis of this
whole file. Designing the roster around what is already in the data folder makes it a function of
past decisions, which is the opposite of an idea generator.

**Standing constraint — NON-PRICE INPUT IS THE SCARCE AXIS** (2026-08-18).
Sort the roster by what each lens *natively consumes*, not by its discipline name. As of this date
all seven generators consumed price (market-maker, physicist, mathematician, statistician,
underwriter) or price plus a calendar (economist, historian). **That, more than the shared-pack lure,
is why #041's lenses converged** — seven personas measuring functions of the same series will find
the same things whatever vocabulary they use. A lens whose native data is not price cannot converge
with them by construction. New lenses are therefore prioritised by input, not by prestige.

**Standing constraint — STATE VARIABLES, not clocks** (salvaged from the removed philosopher lens).
No lens may propose a conditioner that is a clock or a calendar. "17:00", "January", "Wednesday" are
proxies; name the measured state variable underneath. Precedent: #029e flipped a pooled result from
−85 to positive by conditioning on point-in-time spread instead of the hour, and #041 unwrapped
"21:00 UTC" → "17:00 New York" → "the value date rolls and nobody is at their desk", which is what
finally explained why it could not be traded.

**Standing constraint — TABLE SELECTION IS PART OF THE IDEA** (salvaged from the removed poker lens).
A proposal names the instrument it is best in, not the first one tried. #041 measured instrument
choice as worth **8.6x to 29.6x** — larger than most signals ever found here. The capture fraction a
signal must deliver to clear 5x: **EURUSD 14%, USDJPY 18%, GBPUSD 34%, USDCHF 48%, USDCAD 58%,
AUDUSD 68%, NZDUSD 77%.** Five of seven pairs are not worth playing whatever the signal.

**Standing constraint — THE EDA LIST POINTS AT A MARKET, NEVER AT THE LOG** (2026-08-18, learned the
expensive way). A lens's `The EDA this lens wants` section may contain **only forward-looking
measurements on data** — places nobody has looked yet. It may **not** contain:
- "re-examine / rescore / retro-audit / re-express" any past arc or banked result,
- "finish" or "resolve" an unfinished item from a previous run,
- any item whose subject is *our own history* rather than *a market*.

Those things are **maintenance**, and maintenance is real work but it is not generation. A lens whose
EDA list is backward-looking will produce an audit every single time it is run — which is a critic in
a generator's costume, and the roster has no critics because **the kill tests are the critic**.

*How this was learned:* the first autonomous lens run (2026-08-19) spent its entire night auditing old
work, because the EDA list it was handed asked for exactly that. The system obeyed; the file was wrong.
Unfinished business still belongs in a lens's `Log`, where it is a record — never in the EDA list,
where it is an instruction.

**Anti-lure rule** (learned the hard way, 2026-08-15): do not flag one anomaly loudly in a shared
EDA pack. Four of seven lenses converged on the stale-open flag purely because it was the loudest
number in the pack — destroying the diversity the whole method exists to create. Salience is not
relevance.

## What a CORPUS lens is (2026-08-22)

A corpus lens is a folder of book-length material plus a file that tells you how to work it. Nothing
in the file is a summary of the material.

```
lenses/<name>.md                     the lens: question, boundaries, Forbidden, EDA list, GREP LOG
lenses/_material/SOURCES.md          the acquisition list — what is held, what to buy, what failed
lenses/_material/<name>/INDEX.md     entry point — which source, and this lens's gaps
lenses/_material/<name>/<source>/    per-source INDEX.md + one .txt per chapter/section
lenses/_material/index_corpus.py     PDFs WITH an embedded outline -> per-section .txt + INDEX
lenses/_material/split_corpus.py     no outline: parse the printed contents, locate each entry
lenses/_material/split_by_font.py    no usable contents: detect openers by TYPOGRAPHY
```

**Three splitters, tried in that order.** Each prints a verification report — section count,
monotonicity, coverage, largest section — and a **quality gate rejects** any split with fewer than 5
sections, a section over 25% of the book, or coverage under 60%. A body-heading scanner was built and
deleted: it matched numbered prose (`4. Using the optimized code, what is the...`) and produced splits
that *looked* structured but were not, which is worse than none. Where all three fail the source is
marked **NO-SECTION-INDEX** with the reason, and is grepped rather than assumed to have structure.

**Sourcing rule — academically solid × institutionally applied.** The same cross the roster was built
on, now applied to authors: prefer the bulky work written by people who both published and ran money.
Where a book cannot be obtained, **reconstruct from the primary papers behind it and record the
coverage gap in the file** — behavioural holds 5 of the 7 chapters of Shleifer's *Inefficient Markets*
and says which two are missing; market-maker holds Bouchaud's arXiv papers in place of *Trades, Quotes
and Prices*; economist holds Bookstaber's OFR working papers in place of his book.

**Verify every fetched file against its expected title.** Three arXiv IDs recalled from memory during
this build returned unrelated papers — a category-theory paper under Bouchaud's name, a hep-ph paper
under Derman's, a computational-geometry paper under Gatheral's. All three were caught only because
the first page was checked. **A plausible filename is not evidence of content.**

**Never build on a pirated copy.** Two supplied files carried an `oceanofpdf` watermark in their bytes;
both were left out and the material sourced legitimately instead. Scan for it — the filename will not
tell you.

**Working rule.** Index for structure, **grep the `.txt` twins for content** — material is often filed
under a title that does not name it. Cite file and section for every claim (rule 1). Then **write what
you grepped into the lens file's GREP LOG**, which is a coverage record and not a prohibition: re-read
freely for a different question, and say why.

**Why no fundamentals.** The first corpus lens was written with eight, derived from ~19,000 characters
of a ~2,000,000-character corpus — under 1%. Freezing that in the file means every later pass reads one
shallow reading instead of the sources, which is the narrowness the corpus build exists to remove.
A persona's F-list is exactly this problem, which is why the 13 remaining persona lenses are marked for
conversion rather than treated as finished.

## The roster

Generators only — there are no critics, because **the kill tests are the critic**. Each lens must
produce a **different measurement**, not a different description. Sorted by **native input**, which
is the axis that actually creates diversity (see the standing constraint above).

**Every lens now has a corpus** (2026-08-22): 61 sources, 29 indexed section sets, ~355 MB under
`_material/`. What differs is whether the **lens file** has been rewritten to use it.

- **CORPUS build** — question, boundaries, `Forbidden` (only what the corpus cannot supply), EDA list,
  and a **GREP LOG**. No pre-written fundamentals: claims are derived at pass time and cited by file
  and section. **15 of 15, completed 2026-08-24.**
- **PERSONA build** — retired. No lens file carries fundamentals any more.

**What the conversions found.** Rewriting each file against its own corpus surfaced things reading the
corpus index alone did not:

- **Physicist** had nothing behind F1 (scale) or F2 (the variance ratio) — its first two fundamentals.
  Cont and Lo-MacKinlay were fetched to close it.
- **Signal-processing** has no source for two of its five core questions (detection vs estimation, the
  matched filter). **Kay is the roster's highest-value purchase** for that reason.
- **Mathematician** is the worst-matched corpus in the roster — three of four books are memoirs — and
  now points at the identity evidence held under `behavioural/` and `rates/` instead of pretending.
- **Poker** lost a "source" that was a practice rather than a document.

Each file also gained `Forbidden` rules the corpus could never supply, because they are measurements
from this log: #030's gross zero-cost ceiling, #027's 75%/bar decay that meant nothing, #044's
+52.94 bp before the trigger fires, A02's alternating era profile, the capture-fraction exclusions.

**Corpus quality is uneven and is recorded per lens.** Each `_material/<lens>/INDEX.md` states what is
held, what is missing, and — where a source resisted indexing — why. Three honest weak spots:

| lens | state |
|---|---|
| **Mathematician** | Weakest in the roster. Three of its four books are **memoirs**; only *Beat the Market* (1967) is on-topic. The identity *evidence* it needs is cross-referenced from other lenses' folders (twin shares, carve-outs, CIP) rather than held directly. |
| **Signal-processing** | **No book at all** — its two texts are commercial and unobtained. Held as primary papers (Shannon, Rabiner, Kalman). Kay's *Fundamentals of Statistical Signal Processing* is the one purchase that would fix it. |
| **Poker** | One book. Its second listed source was "Susquehanna's game-theory training", which is a practice, not a document. |

### Written

| lens | build | native input | first question | **forbidden** |
|---|---|---|---|---|
| **Supply chain** | corpus | **cargoes, inventories, freight, storage** | Where is the physical stuff, where does it need to be, and what does moving it cost? | anything that is not a space/time/form trade; reading contango as sentiment; crude without a stated round-trip cost |
| **Flow** | corpus | **positioning and flow data** | Who is holding what, how did they come to hold it, and what will force them out? | positioning as a direction signal (it is a fragility signal); a flow dataset without its lag stated |
| **Rates** | corpus | **curves, balance sheets, policy paths** | Whose balance sheet is constrained, what does that force, and what does the curve already price? | a policy-event trade without asking what the curve prices; treating a calendar date as the cause |
| **Meteorologist** | corpus | **physical forecasts** | What is actually forecastable here, how far out, and how do I know my probabilities are honest? | forecasting past a measured skill horizon; a single deterministic forecast; skill without a reference forecast |
| **Market-maker** *(v2)* | corpus | quotes, order flow, fills | Who quotes here, what are they afraid of, and when are they forced to widen? | anything without naming who provides the liquidity; treating the spread as constant; assuming a passive fill gets the posted advantage |
| **Physicist** *(v2)* | corpus | price across **scales** | What is the characteristic time-scale, and how does the system relax after an impulse? | no stated time-scale; generalising a measurement taken at one frequency; sample higher moments that do not converge |
| **Mathematician** *(v2)* | corpus | relationships true by **construction** | What relationship is FORCED to be true, and what is the residual when it is not? | fitted/estimated relationships — identities only; an identity with no nameable friction; padding to fill a quota |
| **Statistician** *(v2)* | corpus | price distributions + the trial count | Which part of the distribution is actually different, and how many things have I looked at? | **testing a conditional MEAN**; a t-stat without its trial count; a row count presented as a sample size |
| **Underwriter** *(probation)* | corpus | price | What premium am I collecting, for accepting what loss distribution, and where is ruin? | direction forecasts — the product is premium collection, not prediction |
| **Poker** | corpus | **who else is playing** | Which game here is soft, and what repeatable mistake is someone else making? | assuming a mistake instead of measuring one; naming an instrument without saying why it is the softest available |
| **Signal-processing** | corpus | price (capability, not diversity) | What is the noise floor here, and is there anything above it? | a signal claim with no measured noise floor; smoothing presented as filtering; a periodicity unchecked against the sampling rate |
| **Economist** *(v2)* | corpus | price + calendar + **rule-books** | Who is on the other side, and why are they willing to lose money to me? | behavioural hand-waving; treating a cost anomaly as evidence of an obligation; forced flow with no volume footprint |
| **Historian** *(v2)* | corpus | rule-books, venue changes, sample inhomogeneity | What was structurally different about the period this worked in, and is that structure still here? | pooled statistics unchecked across their range; conditioning on a regime LABEL rather than observables; reporting an effect without its era |
| **Behavioural** | corpus | **investor-level records** — account and trade data with an identity behind it | What specific, repeatable mistake does a named population make, and why has nobody arbitraged it away? | assuming a mistake instead of measuring one; pooling buy-side and sell-side flow; importing a lab result without a market footprint; retro-fitting a bias name to an effect already found |
| **Machine learning** | corpus | whatever it is fed (capability, not diversity) | Where does model complexity buy something a linear model cannot get, and how would I know it was not noise? | any model before the LINEAR BENCHMARK is measured on our data; a proposal that does not state the breadth gap (N); cross-validation without purging where labels overlap |


**Underwriter is on probation**: its imports generate (the underwriting cycle produced a place to look
no other lens had; the winner's curse named an effect already measured in #041 and never labelled),
but its literal product — selling premium — has a short inventory. The generation score decides it,
not an argument.

## Removed, and why

- **"Quant"** — not a discipline, it is the job title of whoever runs the exercise. Guaranteed to
  restate the default approach, which is the generic output the roster exists to prevent.
- **Philosopher** (removed 2026-08-18, user's call). It was a critic, and
  **the kill tests are already the critic** — a persona that only judges is redundant with a gauntlet
  that judges better and cheaper. The roster exists to GENERATE. Anything that does not generate is
  removed, not demoted. Its non-redundant rule was a generation constraint rather than a judgement and
  survives below as a standing rule on every lens.
- **Poker was removed the same day and REINSTATED as a generator.** Removed while written as a critic
  ("is your edge big enough?" — the gauntlet answers that better). Reinstated because its real first
  question is a place to look, not a judgement: **where are the bad players?** Nothing else in the
  roster asks it. Lesson recorded: *a lens can be miscast rather than wrong — check the framing before
  removing the discipline.*

## The #041 method test — a result about a ROSTER THAT NO LONGER EXISTS

*Kept as history, not as a scorecard. Re-read this whole section as past tense.* Full detail: #041 in
[[alpha_log]].

| | Arm A (lenses) | Arm B (random control) |
|---|---:|---:|
| tradable hypotheses | 7 | 8 |
| **passing edge/cost >= 5x** | **0** | **0** |
| best | 2.78x | 1.73x |

**Why it does not grade the current roster.** Of the seven lenses tested, five have since been rebuilt
from the ground up and six more have been added. More importantly the test was **mis-specified in
three ways that were only understood later**:

1. **It graded a GENERATOR with a DEPLOYMENT bar.** `edge/cost >= 5x` is what a candidate must clear to
   be traded; a lens's job is only to point somewhere new and real. Whether that converts depends on
   cost, execution and everything downstream. See the two-score rule above.
2. **Its crossings were METHOD trials booked as ALPHA trials.** Arm B was correctly pre-declared
   non-tradable so it would not inflate `K`; Arm A never got the equivalent declaration. Seven
   crossings of the sealed sample were spent answering a question about our own process. See the
   two-ledger rule above.
3. **It could not have shown diversity, because all seven lenses read PRICE.** Four of seven converging
   on the stale-open flag was read as a lens failure and a pack-design fault. It was neither — seven
   personas measuring functions of the same series will converge whatever vocabulary they use. The fix
   was structural, not editorial, and arrived on 2026-08-18: four of the thirteen lenses then in the
   roster took non-price input. (The roster is 15 as of 2026-08-22.)

Other honest flaws recorded at the time: the EDA pack was ~15 measurements, half the lens output was
DIAGNOSTIC rather than tradable, three Arm B cells were not computable, the 6.40 bp equity cost was a
banked estimate rather than a measurement, and **the one-lens-at-a-time form was never run** — only
the parallel-agent form, which the user judged "kind of extra".

**What it did establish, and this still stands:** the plumbing works end to end — pack → lenses →
frozen carry list → sealed holdout → identical gauntlet for both arms → every result reported. And the
market-maker and statistician deep passes produced the two most generalisable results in the entire
log ([[direction-is-unpredictable]], [[fx-microstructure-facts]]) plus the capture-fraction gate.

**Standing conclusion:** #041 is evidence about *that* roster, run in *that* form, graded on the
*wrong* bar. It is not evidence that lens-directed generation does not work, and it must not be cited
as such. The current roster has never been tested.

## What a fair test would look like, whenever one is run

Two arms, identical treatment, **declared as METHOD trials before any crossing**:
- **Arm A** — what the lens-directed EDA surfaces, one lens at a time, conversational form.
- **Arm B (control)** — same structural form, randomly chosen instrument / conditioner / window /
  horizon. Pre-declared non-tradable so it cannot inflate `K`.

Graded on the **generation** bar, not the deployment bar: did Arm A produce places to look that were
(a) novel against each other, (b) absent from the kill list, and (c) yielded something measurable?
Deployment conversion is tracked separately and judged over several passes, never one.

Diversity is now checkable *before* the test rather than after: **if two lenses share a native input,
expect convergence and treat it as predicted rather than as news.** The shared-measurement notes now
carried in the lens files ("run once, credit one") exist so the roster cannot inflate its own trial
count by having three lenses commission the same experiment.
