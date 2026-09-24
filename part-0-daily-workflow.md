# Part 0 — The Daily Alpha-Hunting Workflow

*The orchestration doc. The other files explain concepts; this one is the step-by-step loop that uses them. Start here each session.*

---

## How this loop is RUN — ONE STEP PER TURN (hard rule)

*Adopted 2026-08-22. The workflow-level twin of `backtest_engine2/PROTOCOL.md` §1/§2/§4, which
governs notebook cells. Same reason, same shape: less structured runs produced steps that were
merged, skipped, or reported as done without anything to look at.*

Every step below — Step 0 through Step 7 — follows this loop. No exceptions.

```
┌──────────────────────────────────────────────────────────────────┐
│  1. ANNOUNCE  what this step will do, what it needs, what it     │
│               will produce                                       │
│  2. ASK       for any decision the step depends on               │
│  3. WAIT      for explicit go-ahead. Do nothing yet.             │
│  4. DO        exactly ONE step                                   │
│  5. SHOW      what it produced — numbers, a plot, a written      │
│               hypothesis. Something the user can check.          │
│  6. STATE     what passed or failed your expectation, plainly    │
│  7. ASK       for go-ahead to the next step                      │
│  8. WAIT      for explicit go-ahead                              │
└──────────────────────────────────────────────────────────────────┘
```

### The announcement — before doing anything

```
### Step <N> — <step name>

**What this step will do:**
- <one line per concrete action>

**Inputs it needs:** <files, data, outputs of prior steps>

**What it will produce:** <the thing shown at the end>

**Decisions I need from you:**
1. <question, recommended default first>

Ready to run this step once you confirm.
```

Then stop. Do not run it.

### One step per turn — and it CANNOT be turned off

This applies even when:

- **The user says "just do all of it."** Refuse, restate this rule, ask which step to start with.
  There is no standing-continue and no override phrase. The failure mode this rule exists to stop is
  running ahead while things are going well, so an off switch would be taken at exactly the moment it
  does the most damage.
- **Two steps "obviously" belong together.** They don't. Steps are gates.
- **The previous step went cleanly and the next is "trivial."** Same rule. Announce, ask, wait, do.

**Every step must end with something to look at** — a number, a table, a plot, a written sentence.
A step that produced nothing checkable was not a step.

A step's *substeps* are its own business: whatever happens inside a step happens inside that turn.
The gate is between steps.

---

## Mindset (read before starting)

- **You are testing an idea, not manufacturing a winner.** Walking in needing a profitable strat *today* is the #1 cause of overfitting — it pushes you into storytelling and knob-twisting ([[part-2c-overfitting-defense]]).
- **A single alpha is too weak to be "the strategy."** Profit emerges at the *batch* level — dozens of weak, low-correlated alphas where the crossing effect ([[part-2b-cost-and-uniqueness]]) lets the combination survive costs. Your daily job is to **feed the batch**, not birth a winner.
- **Realistic morning deliverable:** 1–2 candidate alphas — tested, logged, and either added to the batch or killed.

---

## The loop

### Step 0 — Pick the hunting ground (5 min, no code)
Use the **Triple-Axis Plan** ([[part-2d-robustness-risk-and-tooling]]). Don't free-associate — choose deliberately:
- **Idea/dataset** × **Region/universe** × **Performance parameter**.
- Freeze one axis, vary the other two.
- Check the **alpha log**: where are the *empty corners* of the batch? Aim there. This stops you re-digging the same gold mine (variants of one idea share failure modes).

### Step 1 — Pick a SOURCE, get one claim, state it in one sentence (15–30 min)
**Your search is directed by Step 0**, not random. The frozen TAP axis *is* your search query.
- e.g. gap = "no options-based alphas" → search `"option implied volatility" "stock returns" predictability`, not "browse SSRN."

**The four sources — pick ONE, and say which:**

| source | what it is | what it hands you |
|---|---|---|
| **Cookbook catalog** | [[part-3a-price-volume-momentum]] … [[part-3g-etfs-futures]] | named published effects — skew, accruals, COT, reconstitution |
| **SSRN / papers** | working papers | a single narrow claim, usually one table |
| **Seeking Alpha / Wilmott** | practitioner writing | informal claims, occasionally a real desk observation |
| **Lens corpus** | [[lenses]] | book-length material with an outline you grep — pull only the part that informs something interesting |

> **The cookbook's *recipe* half is NOT a source.** Roughly half of `part-3*` is instruments and
> method, not claims: Glosten-Milgrom, DPIN, put-call parity, Amihud's breakeven horizon, "use
> rate-of-change not levels", "point-in-time data", "normalize by total assets". That half is a
> **toolbox that serves every step**. Only the catalog of named effects is a source of claims.

**MANDATORY — announce the pick before searching or reading.** Name (a) which source, (b) why that
one, (c) the TAP corner from Step 0 it is aimed at. Then wait: the user approves or redirects. A
source picked silently is a source picked badly — it is the one decision in the whole loop with no
downstream test that can catch it.

- **Wildcard budget (~20%):** occasionally chase a serendipitous/contrarian idea (the book explicitly allocates effort to "wild theories"). But it still must pass the test below.
- **The test (mandatory):** write it as **"a change in [data] predicts [price response] because [economic reason]."** No economic reason → drop it (the 3964 World Cup parable, [[part-2c-overfitting-defense]]).

> Tell-tale bug: if you open SSRN with no answer to "what gap am I filling?", you skipped Step 0. Go back and pick the corner.

### Step 1b — EDA: does the claim survive contact with OUR data? (added 2026-08-22)

The claim arrived from somewhere else — a paper, a textbook, a catalog entry, a lens corpus —
measured on someone else's universe, someone else's period, someone else's costs. **Before expressing
it, measure the claimed effect directly on the data we would actually trade.**

> **The method for this step is `backtest_engine2/skills/14c-eda.md`. Read it; do not improvise one.**
> It is written for exactly this case — *"whenever a hunt starts with an idea (paper, hunch, inherited
> spec) and you need to verify the idea's claims hold in this specific data."* In brief: decompose the
> hypothesis into falsifiable atomic sub-claims C1…Cn, one cell each; pick tools by claim type from
> its menu; **pre-commit the decision rule before running** ("supported if X, refuted if Y,
> inconclusive if Z"); stop the hunt the moment an atomic claim the hypothesis cannot survive without
> is refuted; close with the hypothesis-update cell. Exhaustive *within* the hypothesis, lean outside
> it — 20 generic diagnostics hoping a pattern jumps out is how spurious findings get believed.

**Every step gets a plot — no exceptions.** This is already enforced one level down by
`backtest_engine2/PROTOCOL.md §5.1`: every code cell ends with a representative plot, built through
`cellplot.py`, rendered inline **and** saved to `notebooks/<name>/plots/cell_NN_slug.png`, so the
plots folder reads as a visual table of contents. Skill 14c inherits the cell loop, so it inherits
this. Stated here because at workflow level it kept being treated as optional: **a number in a table
is checked by one person; a shape in a chart is checked at a glance.** The notebook and its `plots/`
folder ARE the EDA record — do not re-narrate them in markdown.

Two things this step adds on top of skill 14c, because they are workflow-level rather than notebook-level:

- **Cheap cost sanity.** Is the claimed edge the same order of magnitude as the round trip? If not,
  stop here — expressing it cannot fix that. (Cost-gate-first, [[spread-cost-playbook]].)
- **The decay-first gate**, below. Skill 14c does not have it.

#### The decay-first gate — the reason ANY source is allowed

Sources are not ranked by respectability. A cookbook entry, an SSRN paper, a Seeking Alpha post and a
lens corpus are all welcome, because the thing that makes a literature-sourced idea dangerous is that
it may already be **crowded** — and a crowded idea shows up as a **decayed** one. So test that directly
instead of rationing sources.

**Split the sample into eras and read the effect era by era. Never pool first.** Then classify:

| shape | reading |
|---|---|
| **Monotone decay**, strongest early, dead late | Real once, arbitraged away. Kill — this is the crowding signature. |
| **Strongest recently**, or flat across eras | Survives. Cf. #037: *"strongest post-2015 (+16.3 bp, n=90) — survives the Kurov et al. death of pre-FOMC drift."* |
| **Alternating** — on, off, on, off | **Noise, not decay.** Cf. A02: pre-2000 5.46x / 2000-09 0.13x / 2010-14 7.44x / 2015-19 0.02x / 2020-24 4.14x. Kill. This is the #039 C4 signature and it is the one most often mistaken for a regime effect. |

A pooled number that hides any of these describes no period at all. Run the gate in its established
order (`alpha_log:1190`): **cost/turnover → swap → venue tier → decay-first.**

> ⚠️ **Not to be confused with `skills/19-decay.md`**, which is Stage-7 signal *smoothing* — blending a
> signal with its own history to cut turnover. Same word, unrelated. This gate is a kill test; that one
> is a construction lever.

**Fail → REJECT and go back to Step 1** for another claim, or another source. Log it as a **light
sub-entry** under the arc that spawned it — not a new arc number, and **as a finding, not a verdict**
(Step 6). A claim that died at 1b is exactly the kind of thing tomorrow's Step 0 needs to know.

**What lands in [[alpha_log]] from this step** — the working stays in the notebook, only this comes out:

```
1b finding — <claim, one line>   [source: <cookbook/SSRN/SA/lens>]   [ledger: ALPHA|METHOD]
  C1 <sub-claim> — supported   (<number, t, null>)
  C2 <sub-claim> — REFUTED     (<number that refuted it>)   ← the one that killed it
  decay-first: <decaying | flat | strongest-recent | ALTERNATING>  <era numbers>
  cost:  edge/cost = <x>   (priced at trade minute, n events, range)
  K so far: <n>            notebook: notebooks/<name>/
  still untested: <what a later pass would have to do to overturn this>
```

That last line is not optional. It is what makes the entry re-openable instead of final.

> **1b is not Step 3.** 1b measures the *claimed effect*, with no strategy built and no engine run —
> it is the cheap screen that stops you spending Steps 2–4 expressing something that was never in our
> data. Step 3 builds the expression and runs the engine. Passing 1b means "the effect is here";
> passing Step 3 means "it survives being turned into positions."

### Step 2 — Express it simply (15 min)
Simplest formula that encodes the sentence (expression vocabulary in [[part-2a-build-loop]]). Fewest parameters. **Units must add up.**

### Step 3 — Backtest the raw version
Run in your engine (or WorldQuant BRAIN, [[part-4-websim]]). Read the five numbers: **IR · return · max drawdown · turnover · margin** ([[part-2a-build-loop]]). Don't refine yet — just check there's *any* signal.

### Step 4 — Refine ONE motivated lever at a time (the Ch. 5 loop)
Each change needs a reason; re-read the **full** metric table after each. A change that lifts IR but wrecks turnover/margin is **not** an improvement.
1. **Neutralize** (industry/market) → kills biggest risk, usually large drawdown drop.
2. **Rank** → relative beats absolute magnitude.
3. **Decay/smooth** → cuts turnover, stabilizes. (Don't decay past the horizon, [[part-2b-cost-and-uniqueness]].)

### Step 5 — Try to KILL it (overfitting gauntlet, [[part-2c-overfitting-defense]])
> **Screens import `DataPanel` and the cost model from the engine — never re-implement loading or costs.**
> Everything else (masks, conditional means, t-stats) stays hand-written and vectorized; only the two
> numbers that have silently broken before come from tested code. Cf. #016 (commission never modelled)
> and A02 (graded against a banked cost *estimate*, 2.78x → 0.94x once measured).
>
> **The cost gate obeys [[data-hygiene]] rule 3: price the spread AT THE TRADE MINUTE, per event —
> never a daily, and never a pooled, median.** A pooled median hides regime shifts and hands you a
> ratio no trader ever faced. Report mean cost across events (what you actually pay), the range, and
> **how many events clear the bar** — not one summary number. Cf. #039: FTMO WTI round trip moved
> 1.71 → 12.40 bp (7.2x) across one year of releases, with a 2.7x step-up in 2026-03; a 14-day
> median read 0.82x where the per-event mean reads 1.21x.

- **Cost gate:** edge/cost ≥ 5x, priced per event at the trade minute (above).
- **Decay-first** (Step 1b) — re-run it here on the refined version, not just the raw claim. Refining
  can manufacture an era-specific fit that the raw claim did not have.
- Works in **another universe / region**? (good alphas travel)
- **Insensitive** to small parameter changes?
- Few enough parameters / does it have a story?
- **Quintile & sector distribution** healthy ([[part-2d-robustness-risk-and-tooling]]), not all PnL in the tails or 2 sectors?
- If it survives → hold out **true OOS** data and check there.

### Step 6 — Check uniqueness, then log it (always) ([[part-2b-cost-and-uniqueness]])
- Correlate vs the existing batch: `<0.3` good, `0.3–0.5` ok, `>0.7` likely redundant.
  ⚠️ Since #042 this screen measures novelty against a **graveyard**: scoring *above* 0.30 is
  informative (you share a failure mode with something already dead), scoring below it means little.
- **Log it whether kept or killed**: idea, formula, TAP corner, metrics, max-correlation, decision. The log powers tomorrow's Step 0 and protects against multiple-testing self-deception.

#### FINDINGS during, VERDICTS only at close-out (added 2026-08-22)

**Do not write a verdict into [[alpha_log]] before the notebook's final stage.** Until close-out,
everything logged is a **finding**.

| | **finding** | **verdict** |
|---|---|---|
| when | any time — EDA, Step 1b, mid-notebook | close-out only, after the full gauntlet |
| says | what was measured, against what null, over what eras, and what it *currently suggests* | `KILLED` / `PARKED-NON-FTMO` / `PARKED-POOL` / `CANDIDATE` (tiers at the top of [[alpha_log]]) |
| must include | **what is still untested** | the tier and the evidence for it |
| tone | "IC +0.0205 (t 30) at lag 1, decaying 75%/bar; economics not yet priced" | "real signal, sub-economic standalone — PARKED as a pool ingredient" |

**Why this rule exists.** Six premature verdicts in this log were later reversed, and **every one was
a premature negative**: #027 *"my Step-2 'microstructure artifact' call was wrong"* (the signal was
real at ~30σ); #029e *"the earlier 'definitively closed / −85' call was WRONG: it omitted the spread
gate"* (flipped negative to positive); #036c *"my too-quick 'poor vehicle' dismissal"*; #016 *"my
regime-fragility concern was WRONG"*; #042 *"so 'you already own this' was wrong"*; and a data-coverage
claim generalised from a handful of probe days. The bias is one-directional — toward killing early —
and once a kill is written it reads as settled to the next run, which then does not re-open it. **A
premature verdict does not just record an error; it forecloses the work that would have found it.**

**Reversals get logged AS reversals.** When a finding or verdict is overturned, say so explicitly and
keep both — what was believed, what changed it, and why the first read was reachable. Those entries
are the most informative in the file.

**A claim rejected at Step 1b gets a light sub-entry**, not its own arc number — nested under the arc
that spawned it, one or two lines: the sub-claim that failed, the number that failed it, the decay
shape. Numbering is for alphas that got built; inflating it with claims that died at 1b makes `K`
accounting unreadable.

### Step 7 — Pre-commit the exit ([[part-1-introduction]], cutting losses)
Before anything nears live money, write the **max acceptable loss `Y`** and the cut conditions — now, while calm, not mid-drawdown.

---

## Flow at a glance

```
Step 0 (TAP gap) ──directs──► Step 1 (pick a SOURCE → claim + 1-sentence hypothesis)
                                    ▲  │  (~20% wildcard, still must pass the test)
                             REJECT ┆  ▼
                                    ┆ Step 1b — EDA: is the claim in OUR data? (vs a null)
                                    └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘  │ PASS
                                                       ▼
       Step 2 express → Step 3 raw backtest → Step 4 refine one lever
       → Step 5 try to kill it → Step 6 correlate + LOG → Step 7 pre-commit exit
```

## What "done for the morning" means
1–2 alphas through the full loop and **logged** (kept or killed). The strategy is the growing batch, not any single morning's output.

## Dependency
This loop needs an **alpha log / batch tracker** to exist — otherwise Step 0 (find the gap) and Step 6 (uniqueness) don't function and "directed search" collapses into aimless browsing.
