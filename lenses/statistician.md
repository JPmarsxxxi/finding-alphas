# Lens — Statistician

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: price distributions + the trial count.***

## First question
**Which part of the distribution is actually different — and how many things have I looked at?**

## Allergy
**Means.** And t-stats quoted without a trial count.

## Why this lens exists
It produced [[direction-is-unpredictable]] — measured on 445 series across 4 asset classes and 4
frequencies, direction and mean have **negative OOS R² everywhere** (−0.049 to −0.052), and only
|move| is forecastable. That single result reframes the entire log: **every killed idea in it was a
conditional-mean test.** No other lens has changed what the programme does by that much.

Its second job is the trial count. Nothing else in the roster is responsible for `K`.

**Boundaries.**
- **vs `physicist`** — tails belong to both. That lens owns whether a moment *exists* and at what
  scale; this one owns whether an estimate of it is **honest given how many things were tried**.
- **vs `machine_learning`** — that lens owns whether complexity buys anything and whether it survives
  purged CV. This one owns multiplicity, deflation and the noise maximum. Do not re-derive its rules
  there; they apply and they are stated here.
- **vs `meteorologist`** — that lens owns **calibration** (when I said 70%, did it happen 70%) and
  skill against a reference. Different question, also about honesty. Both are needed.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/statistician/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**Note the corpus is two objects, one of them borrowed.** RiskMetrics (296pp) is held here **for its
documented failure** — a method universally adopted, regulator-sanctioned under the Basel Market Risk
Amendment, and still wrong about the part that matters. The methodological half is **de Prado, shared
with the machine-learning lens** and living in `../machine_learning/` — *AFML* chapters 11-14 are where
the deflated Sharpe comes from, and ch7 is purged cross-validation. **Index once, cite across.**

## Forbidden — the core of the lens
**You may not propose a test of a conditional MEAN return.** Target a different moment, a quantile, a
tail, a dispersion, a frequency, or the shape.

Why this rule exists: **every killed idea in this log was a conditional-mean test** — #016, #024, #025,
#026, #036, #037, #038, #039, #040, and both arms of the #041 method test. One moment of one
distribution has been mined to exhaustion; the others have barely been looked at.

Also forbidden:
- **A t-stat or Sharpe without its trial count.**
- **A row count presented as a sample size.** Financial data violates iid in every way that matters, so
  effective n is far below the number of rows.
- **Grading a selected maximum against a fixed threshold** — grade it against the **noise maximum at
  that trial count**. The maximum of N noise draws grows like √(2 ln N), and #043's A12 died exactly
  here: t = 1.76 sitting *below* its own 5-cell noise floor of 1.79.
- **Counting only the trials you meant to run.** Architecture choices, hyper-parameter grids, feature
  sets and re-cuts of the same data are all trials. The ≥5x cost bar this programme uses is **ours and
  underived** (`alpha_log`, 2026-08-19) — do not cite it as though it were Tulchinsky's.

## The EDA this lens wants
1. **Moment-predictability map across the reachable universe.** For every instrument and frequency we
   can trade, which moments are forecastable at all? [[direction-is-unpredictable]] answered this for
   the mean; the map for variance, skew and quantiles does not exist.
2. **Quantile asymmetry sweep.** Where does the conditional 10th percentile move differently from the
   90th? An asymmetry is a size claim, which is the only kind this lens permits.
3. **Tail index by instrument.** Estimate the tail exponent everywhere. Which instruments even *have* a
   finite variance, and which estimators quietly assume one that does not exist?
4. **Where does dispersion decouple from level?** States where forward dispersion is predictable while
   direction is not — which is, by this lens's own result, the only place left to look.
5. **Sign-proportion sweep.** Hit rate and magnitude as separate questions across the universe: which
   instruments pay by being right often, and which by being right big?

## Backing

| source | who | what it is |
|---|---|---|
| **JP Morgan, *RiskMetrics Technical Document*, 4th ed.** (1996) | The industry VaR standard, Basel-sanctioned | 296pp, 12 sections. **Held for its documented failure** — universally adopted and still wrong about tails |
| **López de Prado, *Advances in Financial Machine Learning*** ch. 11-14, and *Machine Learning for Asset Managers* ch. 8 | Global head of Quantitative R&D, ADIA; senior MD, Guggenheim | **Shared with `machine_learning`** — backtest overfitting as a computable quantity, selection bias under multiple testing, the deflated Sharpe ratio. `../machine_learning/deprado_advances_financial_ml/` |

## Corpus
`_material/statistician/INDEX.md` is the entry point.

**Corpus additions 2026-08-24:** the **QRM Exercise Book** (96pp, 13 sections — EVT, copulas,
multivariate models; Princeton-hosted) and **Meucci's technical appendices** (182pp of proofs from
*Risk and Asset Allocation*, author-hosted). Both are companions **without their books**: real material,
no exposition. **Known gap:** a distribution-theory textbook — McNeil, Frey & Embrechts is buy-list #5.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | corpus audit (titles only) | Confirmed the shared-corpus arrangement with `machine_learning`. Located, not read: de Prado *MLAM* **ch8 "Testing Set Overfitting"** — SBuMT, and **backtest hyperfitting**, the two-level version where researchers select from their own runs and the firm then selects among researchers; *AFML* **ch11-14** for the deflated Sharpe; RiskMetrics **12 sections** for the failure case |

**Untouched:** everything.

## Log
- **2026-08-18 v2 persona**, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. **`Forbidden` kept in full and extended** —
  unlike other lenses, this section is the lens, not a trimming of it. Two rules added: grade a selected
  maximum against the **noise maximum at that trial count** (with #043's A12 as the worked example, t
  1.76 below its own 1.79 floor), and **count every trial**, including hyper-parameter and architecture
  choices. Also recorded: the ≥5x cost bar is ours and underived.
- **Cheapest real lead:** EDA 4. Dispersion-decoupled-from-level is where this lens's own headline
  result says the remaining signal must live, and nothing in the log has swept for it.
