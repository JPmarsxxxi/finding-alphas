# Lens — Market Maker

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: quotes, order flow, fills.***

## First question
**Who is quoting here, what are they afraid of, and when are they forced to widen?**

## Why this lens exists
Everyone else treats the spread as a cost. This lens treats it as **someone's price**, set by a named
participant with an inventory and a fear, and therefore as something with structure to read.

**Track record — the strongest in the roster.** Its #041 deep pass produced
[[fx-microstructure-facts]]: the spread is a **NY-anchored clock** that shifts with DST (UTC-pooling
understates it 40%), caused by **absence, not financing**; a wide spread is **not a discount** because
the mid stays put; patience cannot escape adverse selection; and the 17:00 rule is FX-only — WTI is
*tightest* then. That pass also caught a specification error in the pack it was handed. Read those
before running it again.

**Boundaries.**
- **vs `physicist`** — impact and order-flow memory sit in both corpora (Bouchaud wrote for both). The
  split: that lens asks about **scales and laws**, this one asks **who is on the other side of the
  quote and what changes their mind**.
- **vs `signal-processing`** — noise floor and detection are theirs.
- **vs `poker`** — softness of the table is theirs; who *makes* the price is this lens's.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/market_maker/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**Note the shape of this corpus.** Sinclair is an **options** market maker: pricing, implied-vol
dynamics, hedging, position sizing. The **order-flow and impact** half — which is what most of the EDA
list actually needs — is the Bouchaud backbone (four arXiv papers, 176pp) standing in for *Trades,
Quotes and Prices*. Use Sinclair for how a quoter thinks about risk and inventory; use Bouchaud for
what flow does to price.

## Duties
*Kept from the v2 persona. These are not corpus content — they are what the first run of this lens
learned about running it.*

1. **Audit the pack you are given.** On its first run this lens caught a real specification error: a
   "vol by spread quintile" column measured **backward** (the return *ending* at t), and therefore
   near-tautological. Forward versus backward moved the effect **1.95x → 1.38x**.
2. **Do not chase the loudest anomaly.** Four of seven lenses converged on the stale-open flag in #041
   purely because it was flagged loudly. Salience is not relevance.
3. **Distinguish TRADABLE from DIAGNOSTIC explicitly.** Half of this lens's first-run output was
   measurement, not trade — which is fine, and only became a problem when it was graded as if it were.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Proposing anything without naming who provides the liquidity and what makes them change the quote.**
- **Treating the spread as a constant.** Measured here: it is a NY-anchored clock, it shifts with DST,
  and pooling in UTC understates it by 40%.
- **Reading a wide spread as a discount.** The mid stays put — measured, [[fx-microstructure-facts]].
- **Assuming a passive order is filled at the posted advantage.** #030 tested this directly: limit
  orders **do** recover nearly the full spread (−0.93 → +0.018 bp/signal, the biggest single lever
  found), and it still did not matter, because the **gross zero-spread ceiling was only +0.057 bp/sig**.
  The execution win was real and the edge underneath was not.
- **Optimising execution before measuring the gross zero-cost ceiling.** That is the #027-030 lesson in
  one line, and this is the lens most likely to repeat it.

## The EDA this lens wants
1. **Forecast FLOW, not price.** Order flow has long memory because parent orders are split, so the
   sign sequence is the forecastable object. ⚠️ #043 confirmed the premise literally on genuine
   aggressor-flagged data — flow predicts **future flow** at +0.17 to +0.20 — and found that is exactly
   why it does not pay: it predicts price at +0.008, then negative. Any new work here starts from that.
2. **Decompose widening into adverse selection versus inventory**, per instrument. After the spread
   widens, does the mid move (adverse selection) or revert (inventory)?
3. **Bid/ask asymmetry as an inventory tell.** Does the ask widen more than the bid, or the reverse,
   and does the skew predict anything?
4. **Is the spread FORECASTABLE one step ahead?** If tight periods can be predicted, entries can be
   timed — and #029e already showed a point-in-time spread gate flipping a pooled result from −85 to
   positive.
5. **Opportunity-to-cost surface for every NEW instrument** before anything is built on it.

## Backing

| source | who | what it is |
|---|---|---|
| **Sinclair, *Volatility Trading*** (Wiley) | LIFFE floor clerk → DAX/EuroStoxx options market maker → prop trader, Bluefin → Talton Capital; PhD physics, Bristol | 227pp, 17 sections. Option pricing, volatility measurement and forecasting, implied-vol dynamics, hedging, money management, trade evaluation |
| **Sinclair, *Positional Option Trading*** | as above | 287pp. The variance premium, and position-level construction |
| **Bouchaud, Farmer & Lillo, *How Markets Slowly Digest Changes in Supply and Demand*** + 3 more arXiv papers | Bouchaud — co-founder and chairman, Capital Fund Management | 176pp. Impact, response functions, square-root impact, and the long memory of order flow. **Stands in for *Trades, Quotes and Prices*, which was not obtained** |

## Corpus
`_material/market_maker/INDEX.md` is the entry point.

**Known gap:** Bouchaud, Bonart, Donier & Gould, *Trades, Quotes and Prices* — the textbook framing and
the order-book mechanics chapters. The papers carry the argument, not the mechanics.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: Sinclair **ch2 "Volatility Measurement and Forecasting"** (p28-57, the longest chapter) and **ch3 "Implied Volatility Dynamics"** (p58-75); Bouchaud-Farmer-Lillo (111pp) for EDA 1-2; Tóth et al. on square-root impact for EDA 5 |

**Untouched:** everything. Both Sinclair books, all four Bouchaud papers.

## Log
- **2026-08-18 v2 persona**, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. `Duties` kept in full — they are process
  lessons from this lens's own first run, not corpus content. `Forbidden` grew from three rules to
  five: the two additions are the **#030 execution finding** (limit orders recovered nearly the full
  spread and it still did not matter, because the gross ceiling was 0.057 bp/sig) and its generalisation
  — **measure the gross zero-cost ceiling before optimising execution**.
- **Cheapest real lead:** EDA 2. Adverse-selection-versus-inventory decomposition is a *size* question,
  it uses data already held, and it is the one item on the list that #041 and #043 did not already
  answer or kill.
