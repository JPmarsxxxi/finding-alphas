# Lens — Rates / Monetary Plumbing

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: curves, balance sheets, policy paths.***

## First question
**Whose balance sheet is constrained here, what does that force them to do, and what does the curve already price?**

## Why this lens exists
Every other lens looks at an asset. This one looks at the **funding** behind the asset — who borrowed
to hold it, at what rate, against what collateral, and what happens at the date their balance sheet is
measured. It is the only lens whose subject is the machinery rather than the price.

**Boundaries.**
- **vs `economist`** — that lens asks who is *obliged* by a rule. This one asks whose *balance sheet*
  cannot carry the position. An obligation is contractual; a constraint is arithmetic, and the
  arithmetic is observable.
- **vs `mathematician`** — CIP is an identity, so the cross-currency basis belongs to both. The split:
  that lens asks *what is forced true*; this one asks *whose funding cost makes it fail*.
- **vs `flow`** — positioning is who holds it. This is who **financed** it.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** A summary would freeze one reading of a
655-page corpus into a paragraph, and every later pass would read the paragraph instead of the sources.
**Derive at pass time.**

1. **Start at `_material/rates/INDEX.md`**, then `pozsar_global_money_notes/INDEX.md` — 40 notes, each
   short and self-contained, titled.
2. **Grep the `.txt` twins for content.** The note titles in that index are heuristic (first
   non-boilerplate line), so they are a hint, not a contents page — **grep, do not trust the title.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below, before moving on.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Treating a calendar date as the cause.** Name the rule that binds and whose balance sheet it binds.
  This lens is the most likely in the roster to produce a clock dressed as a mechanism, because its
  material is full of dates — quarter-ends, reserve maintenance periods, settlement. #041 unwrapped
  "21:00 UTC" → "17:00 New York" → *"the value date rolls and nobody is at their desk"*, and only the
  last of those was tradable-or-not. ([[lenses]] standing constraint: state variables, not clocks.)
- **Proposing a policy-event trade without asking what the curve already prices.** If it is in the
  forward, it is not an edge. Cf. #037: the FOMC-eve effect was real, decay-free and FTMO-legal, and
  still sub-economic at +0.96%/yr on 8 trades a year — **wrong FORM, not wrong idea**.
- **Quoting an "expected path" as observed.** It is a decomposition with a term premium in it.
- **Assuming a rate we can earn is the rate the plumbing pays.** Measured: FTMO's swap markup runs
  ~1.3-3.4%/yr per leg against fair carry, which turned #036's real +3.69%/yr carry premium into
  **−0.98%/yr net**. Everything this lens finds must be priced against the venue's actual financing,
  not the policy rate.

## The EDA this lens wants
1. **Cross-currency basis across every pair reachable.** CIP is forced by construction and fails
   measurably; the basis is the price of someone's balance sheet. Where is it widest, when, and against
   what funding stress?
2. **Carry census.** Rank every instrument we can hold by what we are PAID to hold it, net of
   financing, using the venue's real swap rather than the policy differential.
3. **Find the constrained balance sheets and their dates.** Reporting dates, reserve maintenance
   periods, quarter-ends — then reduce each to the state variable underneath before proposing anything.
4. **The data, not the decision.** For policy-sensitive instruments, does the DATA RELEASE that moves
   the expected path matter more than the meeting that ratifies it?
5. **Where is the curve steepest relative to its own volatility?** A forward-implied path is a forecast
   with a risk premium in it; steepness against realised variability says where that premium is largest.

## Backing

| source | who | what it is |
|---|---|---|
| **Pozsar, *Global Money Notes*** (Credit Suisse) | NY Fed → US Treasury → Global Head of Short-Term Rate Strategy, Credit Suisse; drew the shadow-banking map that prompted G20 regulation | **40 notes, 655pp.** Repo, collateral, o/n rates, the cross-currency basis, swap lines, excess reserves, and the Bretton Woods III sequence |
| **Borio, McCauley, McGuire & Sushko, *Covered Interest Parity Lost*** (BIS Quarterly, Sep 2016) | BIS — official sector, not a trading desk | 20pp. The identity that demonstrably fails, and why |
| **Pozsar, *The Safe Asset Glut*** | as above | 16pp |

## Corpus
`_material/rates/INDEX.md` is the entry point. **Grep the index, open one note, read that slice.**
Every source has a `.txt` twin.

**Known gap:** Tuckman & Serrat, *Fixed Income Securities* — the textbook half. Everything held is desk
research and official-sector commentary, which is strong on plumbing and weak on instrument mechanics.
Say so if a pass needs the mechanics.

---

## GREP LOG
*What has already been read, and what was taken from it. A **coverage record, not a prohibition**.
Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | `pozsar_global_money_notes/INDEX.md` (titles only) | Located, not read. Directly on the EDA list: **#20 "BEAT, FRA-OIS and the Cross-Currency Basis"**, **#26 "Fed Funds and the Market for Intraday Liquidity"**, **#29 "Collateral Supply and o/n Rates"** (49pp, the longest), **#32 "Design Options for an o/n Repo Facility"**, **#38 "U.S. Dollar Libor and Swap Line Rollovers"**, **#30 "The Revenge of the Plumbing"**. The 2022+ run (#39-49, Bretton Woods III → commodity encumbrance → currency statecraft) is a distinct arc |

**Untouched:** all 40 notes, the BIS paper, the Safe Asset Glut.

## Log
- **2026-08-18 written** as a persona, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed — Pozsar *is* F1, F5 and F7, at 655pp
  instead of three sentences. Two persona rules survived into `Forbidden` because they are ours, not
  the corpus's; two were added: the #037 wrong-FORM lesson, and the swap-markup measurement that killed
  #036.
- **Cheapest real lead:** EDA 1. The cross-currency basis is the one object in this lens that is
  simultaneously an identity (so the mathematician lens can cross-check it), measurable on data we can
  get, and documented in both the corpus's academic half (BIS) and its desk half (Pozsar #20). It is
  also **not a direction claim**, so it clears [[direction-is-unpredictable]] by construction.
