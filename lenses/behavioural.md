# Lens — Behavioural / Investor Psychology

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-22 — the first lens built on a **corpus** rather than on a persona.*
***Native input: investor-level records** — account and trade data with an identity behind it.*

## First question
**What specific, repeatable mistake does a named population make — and why has nobody arbitraged it away?**

## Why this lens exists
Every other lens reads what the market *did*. This one reads what identifiable people *did*, at the
account level, and asks what they were feeling when they did it. It is the only lens whose primary
evidence is a record of individual decisions rather than an aggregate.

**Boundaries — this lens is not two others.** The economist lens forbids exactly this material
("behavioural hand-waving", F1: *name the OBLIGATION, not the mistake*) — it studies people who are
*compelled*, this one studies people who are *wrong*. The poker lens asks **which table is soft and
where do I sit**; this one asks **what is the mechanism of the mistake and when does it fire**.
Same subject, different question, different data. If a pass finds itself ranking instruments by
softness, it has drifted into poker — stop and hand it over.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** A summary would freeze one reading of a
~2M-character corpus into a paragraph, and every later pass would read the paragraph instead of the
books — which is the narrowness this rebuild exists to remove. **Derive at pass time.**

1. **Start at `_material/behavioural/INDEX.md`** for structure — which source, which chapter.
2. **Grep the `.txt` twins for content.** Every PDF has one. Full-text grep beats any topic map,
   because the material you want is often filed under an unrelated title: the attention-asymmetry
   result lives inside a section called *"6. Failure to Diversify"*.
3. **Cite what you derive.** Every claim carries the file and section it came from. A claim with no
   citation is a prior wearing a corpus as a costume — and the difference is invisible without the
   citation, which is exactly why it is mandatory.
4. **Log what you grepped** in the grep log below, before moving on.

## Forbidden
*Only rules a pass CANNOT derive from the corpus. The books do not know what we have measured;
anything they would tell you has been left out on purpose.*

- **Assuming a mistake instead of measuring one.** Inherited from the poker lens, and the reason
  #041's 17:00 FX result failed: nobody was forced and nobody was wrong — they were absent.
- **Retro-fitting a bias name to an effect already found.** There are enough named biases to explain
  any result after the fact; that is the #038c BoJ-QQE failure with psychological vocabulary.
  ([[lenses]] rule 6: a story only counts if it forbids something not yet examined.)
- **Testing a conditional MEAN.** [[direction-is-unpredictable]] measured negative OOS R² for
  direction and mean across 445 series, 4 asset classes, 4 frequencies. This lens's raw material is
  largely direction claims, so it is the lens most likely to violate that. Prefer **flow asymmetry,
  dispersion, and supply overhang**.
- **Conditioning on a clock.** The corpus will hand you calendar effects; name the state variable
  underneath before proposing one ([[lenses]] standing constraint).
- **Importing a laboratory result as a market claim** without locating its footprint in market data.
  The corpus is full of experiments on students, judges and photocopier queues. They are evidence
  about people, not about prices.

## The EDA this lens wants
1. **Coverage sweep: where does PUBLIC account-level data exist?** Exchange long/short **account**
   ratios versus **position** ratios — the gap between the two is a direct read on how the small
   accounts sit relative to the size — plus top-trader breakdowns, and retail-heavy versus
   institution-heavy instruments. Map that coverage against what is tradable; that map decides where
   this lens can operate at all.
2. **Disposition footprint.** Build an unrealized-gain state variable from a volume-weighted
   cost-basis proxy, and measure whether forward **volume and dispersion** differ above versus below
   it. A supply overhang is a size claim, which is the only kind permitted.
3. **Split the flow that #043 pooled.** #043 measured Binance aggressor-flagged flow as a single
   imbalance series and found it flat then negative on price. Test whether aggressive BUY and
   aggressive SELL trades carry different past-return profiles, at what horizon, and whether
   separating them recovers anything the pooled series destroyed.
4. **Attention asymmetry.** Where attention proxies are free, measure whether a shock produces a
   **buy-side** imbalance specifically rather than a symmetric volume rise. Price comes last.
5. **Confidence versus accuracy at market scale.** After a run of gains for a population, does its
   trading *volume* rise while price discovery does not improve? Self-attribution predicts more
   activity, not better activity — and the volume half is measurable without forecasting anything.

## Backing

| source | who | what it is |
|---|---|---|
| **Thaler (ed.), *Advances in Behavioral Finance* Vol II** (Russell Sage, 2005) | Thaler — Chicago; co-founded Fuller & Thaler Asset Management | 19 chapters, 720pp. The academic canon |
| **Barber & Odean, *The Behavior of Individual Investors*** (Handbook of the Economics of Finance ch. 22, 2013) | UC Davis / Berkeley Haas | 38pp. Brokerage records — the empirical spine |
| **Shleifer, *Inefficient Markets*** (Oxford 2000) — held as primary papers, 5 of 7 chapters | Harvard; co-founded LSV Asset Management | Noise-trader risk, closed-end funds, positive feedback |
| **Montier, *Seven Sins of Fund Management*** (DrKW 2005, 105pp) + ***Behaving Badly*** (2006) | Dresdner Kleinwort → Société Générale co-head of global strategy → GMO | The practitioner half, tested on professionals rather than students |

**Known gap:** Montier's *Behavioural Investing: A Practitioner's Guide* (Wiley 2007, ~700pp) was not
obtained — the practitioner half rests on 121pp instead. *Inefficient Markets* chs. 1 and 7 (framing
and synthesis) are also missing. Say so if a pass leans on either.

---

## GREP LOG
*What has already been read, and what was taken from it. Check here before grepping — but this is a
**coverage record, not a prohibition**: re-read a section freely if the question is different, and
say why. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-22 | `thaler_advances_v2/ch01…` §2.2 Theory + section headings | The two building blocks (limits to arbitrage + psychology). The three limits named: **fundamental risk** (substitutes imperfect), **noise-trader risk**, **implementation costs** (commissions, bid-ask, price impact, and short-sale constraints — D'Avolio's 10–15bp borrow fee). Shleifer-Vishny's *"separation of brains and capital"*: arbitrageurs run others' money, get judged on returns, and are forced to liquidate as the mispricing worsens |
| 2026-08-22 | `barber_odean_2013/15_8_conclusion.txt` | *"Buying is forward-looking and selling backward-looking."* Bought stocks outperform by ~40pps over the **two years prior**; investors are net sellers of recent strong performers, net buyers of long-horizon ones. Disposition effect is emotional — *"emotionally unpalatable to sell for a loss"* — and flips late in the tax year |
| 2026-08-22 | `barber_odean_2013/13_6_failure_to_diversify.txt` | Attention drives **buying** but not selling, because *"investors own only a small number of stocks and only sell stocks that they own, [so] selling poses less of a search problem."* Proxies used: abnormal volume, prior-day return, news coverage. Corroborated by Seasholes & Wu on 6,459,723 Shanghai accounts |
| 2026-08-22 | `montier_drkw_ssrn/seven_sins/01_sin_city.txt` | The seven sins in summary: forecasting/anchoring (**~75% of fund managers rate themselves above average**), illusion of knowledge (more information raises confidence not accuracy), meeting companies, out-smarting everyone (**3 of 1,000** won the beauty contest), short horizons (**11-month** average NYSE holding period), believing stories, and group decisions (groups **amplify** biases — compress variance of opinion, raise confidence without accuracy, bad at surfacing information only one member holds) |

**Untouched:** all 19 Thaler chapters in full (only ch. 1 §2.2 was read); Barber & Odean sections
1–12 and 14; *Seven Sins* sections 2–10 — i.e. **every sin in detail**, only the summary has been
read; both *Inefficient Markets* papers; *Behaving Badly*; all 7 GMO white papers.

## Log
- **2026-08-22 written.** First corpus-backed lens. Nothing run yet. Cheapest real lead in the file:
  **EDA 3**, because the data is already banked from #043.
- **2026-08-22 restructured** (user's call). Pre-written fundamentals removed — they froze one <1%
  reading of the corpus and would have been read in place of the books. Replaced by derive-at-pass-time
  plus the grep log above.
