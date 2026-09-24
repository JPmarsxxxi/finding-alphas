# Lens — Economist

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: price + calendar + institutional RULE-BOOKS.***

## First question
**Who is on the other side of this trade, and why are they willing to lose money to me?**

## Allergy
A free lunch with no identified loser.

## Why this lens exists
It is the only lens that insists the counterparty be **named and compelled**. Nobody loses on purpose,
so an edge that survives must be somebody's obligation — a mandate, a contract, a rule they cannot opt
out of. That turns "why does this work" from a story into a question with a documentary answer.

**#041 paid for the version of this that goes wrong.** The 17:00 FX widening looked like forced flow
and was not: **nobody was forced and nobody was wrong — they were absent.** Absence and obligation look
identical in price and are completely different trades. That result is why F3's volume-footprint screen
is a `Forbidden` rule here rather than a suggestion.

**Boundaries.**
- **vs `flow`** — that lens reads *positioning data*: who holds it, measured. This one reads
  *rule-books*: who must trade, documented. An inventory is a data question; an obligation is a
  contract question.
- **vs `behavioural`** — that lens studies people who are **wrong**; this one studies people who are
  **compelled**. This lens explicitly forbids the other's material, and that separation is deliberate.
- **vs `rates`** — a balance-sheet constraint is arithmetic; an obligation is contractual.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/economist/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**Note the corpus shape.** Ilmanen is **2.4M characters across two books** — the largest single body of
material in the roster — and it answers *what is the premium and who pays it* across every asset class.
Bookstaber's OFR papers are the **forced-flow mechanism** half, written as the regulator's Head of Risk
Modelling. ⚠️ *Expected Returns* is indexed into 30 chapters; ***Investing Amid Low Expected Returns*
is NOT** — no contents match and no font variation across 674 pages. Grep that one.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **"Investors overreact / are irrational" / any behavioural hand-waving.** Name the constraint and the
  constrained agent, or say nothing. If the answer really is a psychological mechanism, it belongs to
  [[behavioural]] — hand it over rather than smuggling it in.
- **Treating a cost or price anomaly as evidence of an obligation.** #041 paid for this: a wide spread
  is evidence of *absence*, not of a forced seller.
- **Claiming forced flow with no volume footprint.** A compelled agent must leave one. Screen for it
  *before* any price work.
- **Proposing a mechanical-flow trade without checking the family's record.** This family has been
  mined hard and has **one** confirmed member: #025 (month-end FX rebalancing) died on OOS — the 2019+
  EUR magnitude-lean **reversed sign** over 2003-2019 — and #016, the one that worked, was killed live
  in 2026-07. A new obligation trade must say what makes it unlike those two.

## The EDA this lens wants
1. **Build the obligation calendar from RULE-BOOKS.** Index rebalance effective dates, ETF creation and
   redemption mechanics, futures roll windows, fixing windows, margin and settlement cycles. The
   calendar is the deliverable — it is a document nobody has assembled.
2. **Rank each obligation by whether the counterparty CAN STOP.** Mandates beat preferences. A tracker
   that must own the add has no discretion; a fund that prefers to is not the same trade.
3. **Volume-footprint screen across the whole calendar, before any price work.** A forced agent must
   leave a volume signature. No footprint, no obligation — drop it before pricing anything.
4. **Find the obligations nobody trades.** Cross the calendar against instrument liquidity: the same
   rule binds in illiquid corners where nobody is waiting for it.
5. **New obligations.** Which rules came into force recently enough that their forced flow has not been
   arbitraged? Regulatory changes create fresh forced participants, and they are datable.

## Backing

| source | who | what it is |
|---|---|---|
| **Ilmanen, *Expected Returns*** (Wiley 2011) | Central bank PM, Finland; a decade at Salomon/Citi as bond researcher, strategist, MD and trader; senior PM at Brevan Howard; principal at AQR | 1.55M chars, **30 chapters indexed**. Risk premia across every asset class, and what is actually paid for |
| **Ilmanen, *Investing Amid Low Expected Returns*** (2022) | as above | 860k chars. The same framework once the premia have compressed. ⚠️ **No section index — grep it** |
| **Bookstaber, OFR working papers ×2** | MD firm-wide risk, Salomon; Morgan Stanley's first market risk manager; Moore, Ziff, FrontPoint; then Head of Risk Modelling at the OFR | 61pp. Forced selling as a **reflexive** mechanism, with funding and collateral channels made explicit. Stands in for *A Demon of Our Own Design*, not obtained |

## Corpus
`_material/economist/INDEX.md` is the entry point.

**Known gap:** Bookstaber's *A Demon of Our Own Design* itself — the narrative half. The OFR papers
carry the mechanism but not the case histories.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: *Expected Returns* is indexed to 30 chapters, one per premium — the natural entry for EDA 1 is whichever chapter covers the premium a candidate obligation would pay. Bookstaber's *An Agent-based Model for Financial Vulnerability* (37pp) for EDA 3, since its subject is exactly the funding-channel footprint |

**Untouched:** everything — 2.4M characters of Ilmanen, both OFR papers.

## Log
- **2026-08-18 v2 persona**, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed — Ilmanen is F2 ("a premium is payment for
  bearing something specific") at 1.55M characters instead of one sentence. `Allergy` kept: one line,
  and it is the lens. One rule added to `Forbidden` — check the mechanical-flow family's record before
  proposing another one, since it has exactly one confirmed member and that member was **killed live**.
- **Cheapest real lead:** EDA 1. The obligation calendar does not exist, it is assembled from public
  rule-books rather than from data we must buy, and every other item on the list depends on it.
