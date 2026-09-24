# Machine-learning lens — corpus index

**Entry point.** Grep this file to find the right source, open that source's own `INDEX.md`, then
open ONLY the section you need. Grep the `.txt` files for content — the material you want is often
filed under a title that does not name it.

Selection rule: **academically solid × institutionally applied.** Both halves present.

## Finance

| source | who | what | index |
|---|---|---|---|
| **López de Prado (2020), *Machine Learning for Asset Managers*** (Cambridge Elements) | AQR head of ML → Guggenheim head of global quantitative research → Cornell | 152pp, 8 chapters: denoising/detoning, distance metrics, optimal clustering, financial labels, feature importance, portfolio construction, testing-set overfitting | `deprado_ml_for_asset_managers/INDEX.md` |
| **Kelly & Xiu (2023), *Financial Machine Learning*** (Foundations & Trends in Finance) | Kelly — Yale SOM + AQR head of machine learning; Xiu — Chicago Booth | 160pp, 7 sections: the case for financial ML, the virtues of complex models, return prediction, risk-return tradeoffs, optimal portfolios | `kelly_xiu_financial_machine_learning/INDEX.md` |
| **Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning*** (RFS) | as above | 80pp, 15 sections. The horse race: penalised linear, PCR/PLS, generalised linear, boosted trees, random forests, neural nets — on US equities | `gu_kelly_xiu_empirical_asset_pricing_ml/INDEX.md` |
| **López de Prado (2018), *Advances in Financial Machine Learning*** (Wiley) | as above | **481pp, 22 chapters — hand-mapped.** Labeling and meta-labeling (ch3), fractional differentiation (ch5), **purged/embargoed cross-validation (ch7)**, feature importance (ch8), bet sizing (ch10), **the backtesting dangers and backtest statistics that the deflated Sharpe comes from (ch11-14)**, HRP asset allocation (ch16), structural breaks, entropy and microstructural features (ch17-19) | `deprado_advances_financial_ml/INDEX.md` |

## Instrument layer

| source | who | what | index |
|---|---|---|---|
| **Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*** (2nd ed.) | Stanford | 764pp, 23 sections. Not finance — the estimator reference. Model assessment and selection (§9), boosting (§12), random forests (§17), high-dimensional problems (§20) | `hastie_tibshirani_friedman_esl/INDEX.md` |

Per [[lenses]] rule 7, research supplies the **instrument**, never the hypothesis. ESL is here as an
instrument reference only: look up how to compute something, never what to expect from it.

## Gaps

- No **practitioner-failure** account yet. de Prado's *"The 7 Reasons Most Machine Learning Funds
  Fail"* is the obvious candidate and is a standalone paper; not fetched.

## Re-indexing

`../index_corpus.py <pdf> [--level N] [--title "..."]` splits any PDF with embedded bookmarks into
per-section `.txt` plus an `INDEX.md`. Start at the default level; go one deeper if a section spans a
whole part. It refuses PDFs with no bookmarks rather than guessing.

