# Lens corpora — the full acquisition list

One shopping trip for all 15 lenses. Sources are taken from each lens's own `Backing` table, which
already applied the roster rule: **academically solid × institutionally applied**. Added where a lens
was missing one half of that cross.

**Legend**
`FREE` — publisher/author/official-source hosted, I can fetch it.
`CHECK` — probably free but I have not verified the host; I'll confirm before fetching.
`BUY` — commercial. Uni library first.
`HELD` — already in `_material/`.

**Priority** — `1` do first (non-price input, the scarce axis, or a live lead), `2` normal, `3` last.

---

## FINAL STATE — 2026-08-22

**61 sources, 29 indexed section sets, ~355 MB.** Every lens has material. Per-lens detail, including
what is missing and why, is in each `_material/<lens>/INDEX.md`.

| lens | sources | indexed sets | headline |
|---|---:|---:|---|
| **Physicist** | 10 | 3 | Bouchaud & Potters 401pp; Farmer; Gatheral; **+ the scaling canon** (Cont stylized facts, Lo-MacKinlay variance ratio) |
| **Flow** | 6 | 3 | Donnelly ×2, Howell *Capital Wars*, Kang-Rouwenhorst-Tang, CFTC methodology |
| **Market-maker** | 6 | 2 | Sinclair ×2 + Bouchaud's four arXiv papers |
| **Machine learning** | 5 | 5 | **AFML hand-mapped, 22 chapters**; de Prado MLAM; Kelly & Xiu ×2; ESL |
| **Mathematician** | 5 | 2 | Thorp ×3, Derman — *weakest, mostly memoirs*; identity evidence cross-referenced |
| **Economist** | 4 | 1 | Ilmanen ×2 (2.4M chars) + Bookstaber's OFR papers |
| **Meteorologist** | 4 | 2 | Kalnay 369pp, Palmer, **WWRP verification reference** |
| **Signal-processing** | 4 | 0 | **No book** — Shannon, Rabiner (OCR'd), Kalman ×2 |
| **Supply chain** | 4 | 1 | Stopford 593pp, Trafigura, Gorton-Rouwenhorst ×2 |
| **Behavioural** | 3 | 5 | Thaler Vol II 720pp, Barber & Odean, Montier 121pp |
| **Historian** | 3 | 1 | Marks (repaired), Harris **excerpt only** |
| **Underwriter** | 3 | 1 | Complete without buying anything — CAS ×2 + Berkshire |
| **Rates** | 2 | 1 | **Pozsar 40 notes / 655pp**, BIS CIP |
| **Poker** | 1 | 1 | One book |
| **Statistician** | 1 | 1 | RiskMetrics 296pp; shares de Prado with ML |

### THE BUY LIST — books, in order

*Set after the 15 conversions, each of which checked a lens's questions against what is actually on
disk. Ranked by whether the gap leaves a question **unsourced** (1-2) or merely **thin** (3+).*

**Closes an unsourced question:**

| # | book | lens | what it closes |
|---:|---|---|---|
| 1 | **Kay, *Fundamentals of Statistical Signal Processing*, Vols I-II** | signal-processing | **Two of five core questions have no source**: detection vs estimation as different problems, and the matched filter. Highest-value purchase in the roster |
| 2 | **Huggins & Schaller, *Fixed Income Relative Value Analysis*** (Wiley) — Huggins: Bankers Trust, Deutsche | mathematician | Nothing held teaches how to **construct and hedge** a relative-value trade. That corpus is three memoirs and a 1967 book |

**Closes a thin corpus:**

| # | book | lens | what it closes |
|---:|---|---|---|
| 3 | **Montier, *Behavioural Investing: A Practitioner's Guide*** (Wiley 2007, ~700pp) | behavioural | The practitioner spine. 121pp of DrKW notes stand in for it |
| 4 | **Harris, *Trading and Exchanges*** (OUP) — Chief Economist of the SEC 2002-04 | historian | **113pp of ~640 held.** Doubles as reference for market-maker |
| 5 | **McNeil, Frey & Embrechts, *Quantitative Risk Management*** (Princeton) — Embrechts is the EVT authority | statistician | The lens is about distributions and tails and owns no distribution book. *(Free 96pp exercise companion now held — see below)* |
| 6 | **Bouchouev, *Virtual Barrels*** (Springer 2023) — ex-President, Koch Global Partners | supply chain | The quantitative-desk half; what is held is physical trade and shipping |
| 7 | **Aaron Brown, *The Poker Face of Wall Street*** (Wiley) — risk manager at AQR and Morgan Stanley, **and** a professional poker player | poker | A second text, and arguably a better fit than Chen: the academic x institutional x poker cross in one person |
| 8 | **Tuckman & Serrat, *Fixed Income Securities*** (Wiley) | rates | Instrument mechanics. Everything held is desk research and official-sector commentary |
| 9 | **Meucci, *Risk and Asset Allocation*** (Springer) — Lehman, Bloomberg, Kepos Capital | statistician | Alternative to #5. *(Free 182pp technical appendices now held — see below)* |
| 10 | **Derman, *Models.Behaving.Badly.*** | mathematician | The model-vs-theory-vs-identity distinction the lens is built on |

### What could be had free, and what could not

Checked all seven priority books for legitimate free versions — **none of the books themselves are
free.** Two have substantial publisher- or author-hosted companions, and both are now held:

- **`statistician/meucci_risk_and_asset_allocation_technical_appendices`** — 182pp, from Meucci's own
  ARPM site. **All the proofs from *Risk and Asset Allocation*.** Not the book, but the mathematical
  core of it.
- **`statistician/mcneil_qrm_exercise_book`** — 96pp, 13 sections, from **Princeton's own asset
  server**. Chapters mirror the textbook: risk in perspective, empirical properties of financial data,
  financial time series, **extreme value theory**, multivariate models, **copulas and dependence**,
  aggregate risk, market and credit risk. Worked problems rather than exposition — but it is the
  statistician lens's first real distribution material.

Full copies of several of these circulate on unauthorised mirrors. **Those are not used** — see the
watermark rule in [[lenses]].

### Sources that resisted indexing

Marked NO-SECTION-INDEX in their lens index, with the reason and `grep -n` instructions: Ilmanen
*Investing Amid Low Expected Returns* (no font variation across 674 pages), Thorp *Beat the Market*
and *Beat the Dealer*, Harris (excerpt), Trafigura (84pp, small enough not to matter).

### Repairs

- **Marks** — the supplied `.odg` had **zero word spaces** (average token 21 chars). Re-rendered
  through LibreOffice so the extractor could infer word boundaries; 0% → 15.8% spaces. Residual
  damage measured: 0.11% of tokens run together, a few spans dropped. Then hand-mapped to 18 chapters.
- **AFML** — contents could not be matched to the body; hand-mapped on the `N.1 Motivation` line that
  opens almost every chapter, cross-checked against the published chapter list.
- **Rabiner** — a pure scan (29 chars of text layer). OCR'd with Tesseract at 200dpi; two-column
  interleaving, so grep-friendly but not quote-friendly.

## Summary

| | count |
|---|---|
| **BUY** | ~26 books |
| `FREE` — I can fetch now | ~11 |
| `CHECK` — verify host first | ~8 |
| **HELD** | 2 lenses complete bar one book each |

**If you buy only five**, buy these — one per lens where the practitioner half is otherwise missing
entirely and no free substitute exists:

1. **Montier, *Behavioural Investing*** — behavioural has no practitioner spine without it
2. **de Prado, *Advances in Financial Machine Learning*** — already on order
3. **Donnelly, *The Art of Currency Trading*** — flow, and it is the FX desk view we keep reasoning about without a source
4. **Bouchouev, *Virtual Barrels*** — supply chain has no other quantitative-desk text
5. **Harris, *Trading and Exchanges*** — historian, and it doubles as reference for market-maker and microstructure work

**Cheapest real progress without buying anything:** the `FREE` column alone gives flow its academic
half (Kang-Rouwenhorst-Tang + CFTC methodology + BIS), rates most of its CIP material (BIS), physicist
most of Farmer, economist the AQR library, historian the Oaktree memos, and underwriter its entire
corpus. That is six lenses moved off zero.
