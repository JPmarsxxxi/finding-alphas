# Lens — Flow / Positioning

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: positioning and flow data** — who holds what, and how you know.*

## First question
**Who is holding what, how did they come to hold it, and what will force them out?**

## Why this lens exists
Price is the *output* of flow, and every other lens reads the output. This one reads the input. It is
also the only lens that can answer "who is on the other side" with a **measurement** rather than a
story — which is what the economist lens has always lacked.

**Boundaries.**
- **vs `economist`** — that lens studies who is *compelled* by a rule or contract. This one studies
  who is *positioned*, whether or not anything compels them. An obligation is a rule-book question; an
  inventory is a data question.
- **vs `behavioural`** — that lens asks what mistake a population makes and why it survives. This one
  does not care whether the holder was wrong, only that the position must eventually be unwound.
- **vs `rates`** — balance-sheet constraint is theirs; observable positioning is this lens's.

**Standing lead:** #024 sampled COT positioning once, found a **real gross extreme-reversal effect**
that died on swap and was carried by crude, and stopped. Sampled, not exhausted. The puller is banked
(`6dca-aqww`). See the grep log below for what the corpus now says about how that was measured.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** A summary would freeze one reading of the
corpus into a paragraph, and every later pass would read the paragraph instead of the sources.
**Derive at pass time.**

1. **Start at `_material/flow/INDEX.md`** for structure — which source, which chapter.
2. **Grep the `.txt` twins for content.** Every source has one.
3. **Cite what you derive** — file and section, every claim. A claim with no citation is a prior
   wearing a corpus as a costume, and the two are indistinguishable on the page without one.
4. **Log what you grepped** in the grep log below, before moving on.

## Forbidden
*Only rules a pass CANNOT derive from the corpus. The books do not know what we have measured;
anything they would tell you has been left out on purpose.*

- **Treating positioning as a DIRECTION signal.** It is an inventory that must unwind, so the claim is
  about **size and fragility**, never sign. This also keeps the lens inside
  [[direction-is-unpredictable]], which measured negative OOS R² for direction and mean across 445
  series — and #024 was tested as a conditional mean.
- **Calling anything "forced" without naming the rule or contract that forces it.** #041's 17:00 FX
  result is why: nobody was forced and nobody was wrong — **they were absent**. Absence and obligation
  look identical in price and are completely different trades.
- **Using a flow dataset without stating its LAG and its COVERAGE**, and without re-testing the effect
  at the real publication time rather than the observation date. A COT effect that only exists on the
  Tuesday it was measured is not tradable.
- **Pooling a positioning effect across instruments before checking which one carries it.** #024's
  effect was crude-oil-carried; the pooled number described no instrument. Cf. the capture-fraction
  gate in [[lenses]].
- **Ignoring the cost gate because the signal is slow.** #024 died on swap, not on edge.

## The EDA this lens wants
1. **Coverage sweep: where does positioning data exist for what we can actually trade?** COT
   categories, ETF share creation and redemption, fund flows, short interest, exchange open interest,
   exchange long/short **account** ratios versus **position** ratios. Map coverage against tradability
   — that map decides where this lens can operate at all.
2. **Fragility, not direction.** Wherever positioning data exists, measure whether extremes predict the
   **SIZE** of the forward move and forward dispersion. Positioning is an inventory that must unwind,
   so the claim is magnitude and never sign.
3. **Stop-cluster geography.** Round numbers, prior highs and lows, session extremes: is there
   measurable excess movement THROUGH them? Needs only price and volume, works on any instrument, and
   is the half of mechanical flow that options-hedging studies never reach.
4. **Price the reporting lag.** For each positioning dataset, how much of any effect survives entry at
   the real publication time rather than the observation date? That kills or saves whole families
   before a single signal is built.
5. **Where is flow price-INSENSITIVE?** Identify participants who transact regardless of price —
   benchmark trackers, hedgers, redemption-driven sellers — and measure their footprint. Only
   price-insensitive flow pays.

## Backing

| source | who | what it is |
|---|---|---|
| **Donnelly, *The Art of Currency Trading*** (Wiley 2019) + ***Alpha Trader*** (2021) | Head of G10 Spot Trading, Citi NY; MD and global head of G10 FX Trading, Nomura NY; senior FX trader, HSBC NY; trading FX since 1995 | 411pp + 563pp. The desk view of who moves majors, including a chapter each on microstructure and on **technicals, sentiment and positioning** |
| **Howell, *Capital Wars: The Rise of Global Liquidity*** (Palgrave 2020) | Research Director, Salomon Brothers; Head of Research and board director, Barings; founded CrossBorder Capital 1996 | 316pp, 22 sections. Global liquidity as the tide under everything: funding liquidity, cross-border flows, the liquidity transmission mechanism |
| **Kang, Rouwenhorst & Tang (2020), *A Tale of Two Premiums*** (J. Finance 75:377-417) | Yale SOM / HKU | 61pp. The academic treatment of COT positioning that #024 never had |
| **CFTC explanatory notes** — Disaggregated COT + Traders in Financial Futures | Primary data artifact | 8pp. What the trader categories do and do not mean |

## Corpus
`_material/flow/INDEX.md` is the entry point. **Grep the index, open one chapter, read that slice.**
Every source has a `.txt` twin; never open a PDF to browse.

**No known gaps.** The BIS Triennial Survey (turnover by counterparty type) is free and not yet
fetched, but nothing on the backing list is missing.

---

## GREP LOG
*What has already been read, and what was taken from it. Check here before grepping — a **coverage
record, not a prohibition**: re-read freely if the question is different, and say why. Anything not
listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | `kang_rouwenhorst_tang_tale_of_two_premiums` (abstract only) | Position changes decompose into two pieces with **opposite signs on expected returns**: short-horizon variation driven by the *liquidity demands of noncommercial* traders, long-horizon variation by the *hedging demands of commercials*. The gains commercials make providing liquidity largely offset the premium they pay for price insurance. **Direct bearing on #024**, which measured COT positioning as one pooled effect — the same error shape as #043's pooled flow. Not yet read past the abstract |
| 2026-08-24 | `INDEX.md` of all four sources (titles only) | Located, not read: Donnelly *Alpha Trader* **ch10 "Understand technicals, sentiment and positioning"** (p335-364) and **ch8 "Understand microstructure"** (p278-306); Howell **ch6 "Private Sector (Funding) Liquidity"** (p93-117), **ch8 "Cross-Border Capital Flows"** (p158-193), **ch10 "The Liquidity Transmission Mechanism"** (p214-249), **ch13 "Measuring Liquidity: the Global Liquidity Indexes"** (p275-281) |

**Untouched:** everything. Both Donnelly books in full (974pp combined), all of Howell, the body of
Kang-Rouwenhorst-Tang, both CFTC notes.

## Log
- **2026-08-18 written** as a persona, with fundamentals F1-F6 and no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed — they were one author's summary standing in
  for four books that now exist locally. `Forbidden` trimmed to the five rules the corpus cannot supply,
  all of them from our own history (#024, #041, the capture-fraction gate). EDA list unchanged: it was
  already forward-looking and market-pointing.
- **Cheapest real lead:** EDA 1-2 on COT, because #024's effect was measured as a conditional mean and
  this lens forbids that — the same data re-asked as a size question, with the lag applied honestly,
  and now with Kang-Rouwenhorst-Tang to say how the decomposition should be done.
