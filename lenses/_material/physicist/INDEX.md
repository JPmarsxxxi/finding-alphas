# Physicist lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Bouchaud & Potters, *Theory of Financial Risk and Derivative Pricing*** (CUP) — indexed, 24 sections | Bouchaud — co-founder and chairman, Capital Fund Management | 401pp. Statistical physics applied to risk: distributions, correlations, tails | `bouchaud_potters_theory_of_financial_risk/INDEX.md` |
| **Farmer, *Making Sense of Chaos*** (2024) | Co-founded Prediction Company (1991, sold to UBS 2006); founded the Complex Systems Group at Los Alamos; Oxford/INET and Santa Fe Institute | 340pp, **25 sections** — complex systems, the economy as one, inefficient markets, the self-referential market, **ecology and evolution in finance**, how credit causes financial instability | `farmer_making_sense_of_chaos/INDEX.md` |
| **Gatheral, *The Volatility Surface*** (Wiley 2006) — indexed, 19 sections | PhD theoretical physics, Cambridge 1983; headed Equity Quantitative Analytics at Merrill Lynch 1997-2005 as MD | 210pp | `gatheral_volatility_surface/INDEX.md` |
| **Gatheral — lecture notes** | as above | WARNING: 38pp, **not the book** — a separate short set, kept for reference | `gatheral_lecture_notes_PARTIAL.txt` |

## Gaps

- Farmer's **arXiv / Santa Fe papers** — the methodological half; the book is narrative. Free, not yet fetched.

## Backbone — Farmer's methodological papers

*Making Sense of Chaos* is narrative. The measurements behind it are in the papers:

| paper | pp | what it backs |
|---|---:|---|
| **Farmer, *Market Force, Ecology and Evolution*** | 66 | F7 — a market as an ecology of strategies rather than an equilibrium |
| **Farmer et al., *The Predictive Power of Zero Intelligence in Financial Markets*** | 18 | F6 — universality: how much of price behaviour follows from market structure alone, with no clever agents |

## Backbone — the SCALING canon (added after an audit found F1/F2 unsupported)

The books cover tails, universality and ecology. They do **not** cover the lens's first two
fundamentals — *a quantity without a scale is not a measurement*, and *aggregation reveals the law*.
These do:

| paper | pp | what it backs |
|---|---:|---|
| **Cont (2001), *Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues*** | 14 | F1, F4, F5 — the canonical stylized-facts list: heavy tails, absence of linear autocorrelation, volatility clustering, aggregational Gaussianity, slow decay of |return| autocorrelation |
| **Lo & MacKinlay (1988), *Stock Market Prices Do Not Follow Random Walks*** (NBER w2168) | 47 | **F2 directly** — this is the variance-ratio test, the signature plot the lens asks for, and its distribution under the null |
| **Bouchaud et al. (2002), *More Statistical Properties of Order Books and Price Impact*** | 9 | F3 — relaxation and impact measured rather than assumed |
