# Lens — Physicist

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: price across SCALES.***

## First question
**What is the characteristic time-scale here, and how does the system relax after an impulse?**

## Why this lens exists
Every other price-reading lens picks a frequency and works there. This one treats **frequency itself
as the variable**, and asks what changes as you aggregate. That is the difference between "the signal
decays 75% per bar" as an annoyance and as a measurement of the system.

**Boundaries.**
- **vs `market-maker`** — impact and order-flow memory sit in both corpora, because Bouchaud wrote for
  both. The split: **this lens asks about laws and scales; that one asks who sets the quote.** Run the
  shared measurement once and credit one lens, or the roster inflates its own trial count.
- **vs `signal-processing`** — that lens owns the **noise floor and detection**: is there anything
  above it. This one owns the **shape of what is there**: exponent, relaxation, scale.
- **vs `statistician`** — tails belong to both; that lens owns the trial count and the estimator's
  honesty, this one owns whether the moment exists at all.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/physicist/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**This is the roster's largest corpus — 10 sources — and it is in three layers.** Bouchaud & Potters
(401pp) is the *theory*; Farmer (340pp + 2 papers) is the *ecology* argument; and the **scaling canon**
(Cont, Lo-MacKinlay) is what the first two do not cover — the stylized-facts list and the variance-ratio
test itself. Gatheral is the vol-surface application. Start from the layer your question is in.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Proposing anything without stating its characteristic time-scale explicitly.** A proposal with no
  scale is not a physics proposal.
- **Generalising a measurement taken at one frequency** — and **seasonally adjust before declaring a
  scale dead**, which #041 failed to do.
- **Using a sample estimate of a higher moment without checking it converges.**
- **Confusing a decay measurement with an edge.** #027 measured a real signal that decayed **75% per
  bar** — IC +0.0205 at lag 1, ~30σ, entirely genuine — and it was still uneconomic. The scale
  measurement was right and told you nothing about tradability on its own.
- **Reporting a scale finding without its cost counterpart.** This lens's natural output is
  "the characteristic time is X"; the immediately following question is always whether the move over X
  clears the round trip at X. #029f/g is the precedent: a real decay-free micro-edge, dead because lag1
  execution is institutional and we trade at lag2.

## The EDA this lens wants
1. **Signature plot / variance ratio across scales, everywhere reachable.** Where does each market
   depart from a random walk, and at what scale? ⚠️ Lo & MacKinlay is now in the corpus — **use their
   test and their null**, do not hand-roll one.
2. **Relaxation form after large moves.** Exponential or power law, per instrument? A power law means
   no characteristic scale, which changes what a horizon even means.
3. **Scaling-exponent census.** Estimate the same exponent — Hurst, tail index, impact where measurable
   — across every instrument reachable, and compare rather than interpret one in isolation.
4. **Where is the natural SCALE mismatched to the COST?** Cross each market's departure-from-random-walk
   scale against its round-trip cost at that scale. This is the one item on the list that produces a
   *tradable* shortlist rather than a diagnostic.
5. **Decay rate versus deployed capital.** If a market is an ecology, an edge should decay faster where
   more capital chases it — testable against the log's own dead arcs.

## Backing

| source | who | what it is |
|---|---|---|
| **Bouchaud & Potters, *Theory of Financial Risk and Derivative Pricing*** (CUP) | Bouchaud — co-founder and chairman, Capital Fund Management | 401pp, 24 sections. Statistical physics applied to risk: distributions, correlations, tails |
| **Farmer, *Making Sense of Chaos*** (2024) + 2 papers | Co-founded Prediction Company (1991, sold to UBS 2006); Complex Systems Group, Los Alamos; Oxford/INET, Santa Fe | 340pp, 25 sections + *Market Force, Ecology and Evolution* (66pp) and *Zero Intelligence* (18pp) |
| **Cont (2001), *Stylized Facts*** | CNRS / Oxford | 14pp. The canonical list: heavy tails, no linear autocorrelation, volatility clustering, aggregational Gaussianity |
| **Lo & MacKinlay (1988), *Stock Market Prices Do Not Follow Random Walks*** | MIT / Wharton | 47pp. **The variance-ratio test and its distribution under the null** — EDA 1 itself |
| **Gatheral, *The Volatility Surface*** (Wiley 2006) | PhD physics, Cambridge; headed Equity Quantitative Analytics at Merrill Lynch as MD | 210pp, 19 sections |

## Corpus
`_material/physicist/INDEX.md` is the entry point.

**Known gap:** no Mandelbrot and no Mantegna-Stanley. The scaling canon here is Cont and Lo-MacKinlay,
which covers the *measurements* but not the multifractal literature. Also `gatheral_lecture_notes` is a
38pp fragment, **not the book** — the 210pp file is the real one.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | corpus audit (titles and abstracts only) | Established that the books cover tails, universality and ecology but **not F1 and F2** — scale and the variance ratio — which is why Cont and Lo-MacKinlay were added. Located, not read: Lo-MacKinlay for EDA 1, Cont's stylized-facts list for EDA 3, Farmer's *Market Force, Ecology and Evolution* for EDA 5 |

**Untouched:** everything. All 401pp of Bouchaud & Potters, all of Farmer, both new papers, Gatheral.

## Log
- **2026-08-18 v2 persona**, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS**, and the conversion **found a real hole**: the corpus covered F5
  (tails), F6 (universality) and F7 (ecology) but had nothing behind F1 (scale) or F2 (the variance
  ratio / signature plot) — its first two fundamentals. Cont and Lo-MacKinlay were fetched to close it.
  That is an argument for doing these conversions rather than assuming a corpus fits its lens.
- `Forbidden` grew from three rules to five: added the **#027 decay-is-not-edge** lesson (a 75%/bar
  decay was measured correctly and meant nothing about tradability) and the requirement to report a
  scale finding with its cost counterpart (#029f/g).
- **Cheapest real lead:** EDA 4. It is the only item that yields a tradable shortlist rather than a
  diagnostic, and this lens's failure mode is producing beautiful measurements nobody can trade.
