# Lens — Supply Chain / Physical Commodities

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: physical flows** — cargoes, inventories, freight, storage.*

## First question
**Where is the physical stuff, where does it need to be, and what does moving it cost?**

## Why this lens exists
It is the only lens whose primary evidence is **matter in a place**, not a price series. A barrel in
Cushing and a barrel in Rotterdam are different objects with a measurable cost between them, and that
cost is an observable, not an estimate.

**Boundaries.**
- **vs `mathematician`** — storage bounds a calendar spread by an identity, which is that lens's
  object. The difference is that here the friction is **physical and quotable** (tank rent, freight,
  insurance), not a market friction to be inferred.
- **vs `flow`** — positioning data says who holds the *paper*. This lens is about who holds the
  *barrel*, and they are not the same people (see the corpus on paper-vs-physical size).
- **vs `economist`** — a delivery obligation is a contract, so it can belong to either; the split is
  that this lens must be able to point at the cargo.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** A summary would freeze one reading of the
corpus into a paragraph, and every later pass would read the paragraph instead of the sources.
**Derive at pass time.**

1. **Start at `_material/supply_chain/INDEX.md`** for structure — which source, which chapter.
2. **Grep the `.txt` twins for content.** Every source has one.
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below, before moving on.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Proposing anything in crude without stating the round-trip cost up front.** Measured, not assumed:
  FTMO's WTI round trip ran **1.71 to 12.40 bp across one year of releases (7.2x)**, with a **2.7x
  step-up in 2026-03** that stayed. #039 died here — edge/cost 1.21x, and **0 of 43 release days
  cleared 5x**. WTI's round trip is ~28x EURUSD's.
- **Pricing a commodity spread on a pooled or median cost.** Per [[data-hygiene]] rule 3, price it at
  the trade minute, per event — a 14-day median read 0.82x on #039 where the per-event mean read 1.21x.
- **Carrying an effect on one instrument into a family.** #024's positioning effect was
  crude-oil-carried and the pooled number described nothing; #026 found WTI-Brent was the *only* robust
  daily pair, and swap killed it.
- **Assuming a physical relationship survives a CFD wrapper.** Everything this lens finds must still
  pass the venue check — real carry is earned on futures and spot, not on marked-up CFD swap (#036).

## The EDA this lens wants
1. **Map the three families across everything reachable** — location spreads (space), calendar spreads
   (time), grade and quality spreads (form). Which exist in tradable form, and at what cost? Physical
   trading is only ever these three, so this map is the lens's entire opportunity set.
2. **Storage bound as an identity.** Is the calendar spread bounded by measured carry cost, and what
   happens AT the bound? The break at a physical limit is the object — a bounded relationship, not a
   fitted one.
3. **Freight and vessel movement as a leading input.** Does any freight or shipping series lead a
   tradable commodity, and by how long? Genuinely non-price data with a physical lead time; needs data
   we do not hold.
4. **Inventory state as a conditioner.** Measure whether price response to supply news differs when
   storage is near a binding limit versus mid-range. Hard limits produce asymmetry — a size claim with
   a monitorable trigger.
5. **Cost gate first, always.** For each candidate spread, round-trip cost against typical spread move,
   before any modelling. Most of this lens's output should die here, and should die cheaply.

## Backing

| source | who | what it is |
|---|---|---|
| **Stopford, *Maritime Economics*, 3e** | 45 years in shipping; MD of Clarkson Research to 2012, executive director Clarksons PLC | 593pp, 19 chapters. The shipping market's organisation, the shipping cycle, freight rate mechanics, costs, ship markets |
| **Trafigura, *Commodities Demystified*, 2e** | A top-3 physical trading house documenting its own business — **primary source** | 84pp. Space / time / form arbitrage described by people doing it |
| **Gorton & Rouwenhorst, *Facts and Fantasies about Commodity Futures*** (NBER w10595) | Yale SOM | 41pp. What commodity futures actually return, and how much is the curve rather than the spot |
| **Gorton, Hayashi & Rouwenhorst, *The Fundamentals of Commodity Futures Returns*** (NBER w13249) | Yale SOM | 63pp. **Inventory as the state variable** — the link from stocks to the basis and to risk premia. The paper for EDA 4 |

## Corpus
`_material/supply_chain/INDEX.md` is the entry point. **Grep the index, open one chapter, read that
slice.** Every source has a `.txt` twin; never open a PDF to browse.

**Known gap:** Bouchouev's *Virtual Barrels: Quantitative Trading in the Oil Market* (Springer 2023)
was not obtained — the quantitative-desk half. What is held is physical trade, shipping and the
academic treatment. Say so if a pass leans on desk practice. EIA storage reports are free and not yet
pulled.

---

## GREP LOG
*What has already been read, and what was taken from it. A **coverage record, not a prohibition** —
re-read freely for a different question, and say why. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: Stopford **ch1 "The economic organization of the shipping market"** (p32-67) and **ch2 "The shipping market cycle"** (p68-107) for EDA 3; Gorton-Hayashi-Rouwenhorst in full for EDA 4 (inventory → basis); Trafigura whole (84pp, no section index — grep it) |

**Untouched:** everything. All 593pp of Stopford, all of Trafigura, both Gorton papers.

## Log
- **2026-08-18 written** as a persona, F1-F6, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. `Forbidden` rewritten: the persona's three
  rules were all derivable from the corpus (space/time/form, contango-as-inventory), so they went; what
  replaced them is the **measured cost history** the books cannot know — #039's 7.2x intra-year range
  and 0-of-43 pass rate, the per-event pricing rule, and the CFD-venue check from #036.
- **Cheapest real lead:** EDA 2 and 4 together. The storage bound is an identity with a *quotable*
  friction, and Gorton-Hayashi-Rouwenhorst gives the inventory-to-basis link to test it against. Both
  are size claims, so neither collides with [[direction-is-unpredictable]].
