# Lens — Machine Learning

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-22, corpus-backed. **CAPABILITY lens, not a diversity one** — see below.*

## First question
**Where does model complexity buy something a linear model cannot get — and how would I know it was not noise?**

## Honest position in the roster
This lens **consumes whatever it is fed**, so it cannot add a new input axis by construction. It is
the same standing as `signal-processing` — kept for what it can *do*, not for where it can *look*, and
it should never be scored on novelty it is structurally unable to produce. If a pass here produces
"apply a random forest to the thing another lens found", that is this lens working correctly.

**It is also the lens most able to manufacture a false positive.** The log is a graveyard of
overfitting; this lens's `Forbidden` list is doing more work than any other's, and it is not
negotiable.

**Boundaries.**
- **vs `statistician`** — that lens owns *how many things have I looked at*: multiplicity, trial
  counts, deflated Sharpe, grading a selected maximum against the noise maximum. This lens owns
  *does complexity buy anything, and does it survive purged cross-validation*. Do not re-derive the
  statistician's rules here; they apply, and they are stated there.
- **vs `signal-processing`** — that lens owns the noise floor and detection. This one owns
  high-dimensional function approximation. If a pass is asking "is there anything above the noise",
  that is signal-processing; if it is asking "is the relationship non-linear", it is this one.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** A summary would freeze one reading of
the corpus into a paragraph and every later pass would read the paragraph instead of the sources.
**Derive at pass time.**

1. **Start at `_material/machine_learning/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.** Every PDF has one.
3. **Cite what you derive** — file and section, every claim. A claim with no citation is a prior
   wearing a corpus as a costume, and the two are indistinguishable on the page without it.
4. **Log what you grepped** in the grep log below.

## Forbidden
*Only rules a pass CANNOT derive from the corpus. The books do not know our universe, our breadth,
or our history; anything they would tell you has been left out on purpose.*

- **No model before the LINEAR BENCHMARK is measured on OUR data.** Gu-Kelly-Xiu's whole result is
  stated against a 3-characteristic panel regression, and we have never computed the equivalent
  number for any universe we trade. Without it, any ML result is uninterpretable — you cannot claim
  complexity paid if you never priced simplicity.
- **Name N before proposing anything.** The published settings are ~30,000 stocks × 60 years × 900+
  predictors. Our universes are 167 FTMO symbols, 59 of them equities; some arcs run on 5–28 FX pairs.
  That is one to three orders of magnitude below the setting these methods were demonstrated in, and
  `IR = IC·√breadth` does not care how good the model is. **State the breadth gap explicitly in any
  proposal, or the proposal is not made.**
- **The cost gate comes first, as always.** Cost-gate-first is a house rule that predates this lens
  ([[spread-cost-playbook]]); a model that improves an uneconomic signal has improved nothing. Price
  the spread at the trade minute, per event, before any fitting.
- **No cross-validation without purging and embargo** where labels overlap in time. Standard K-fold
  leaks across the boundary when the label horizon exceeds the fold gap. *(Note: the primary treatment
  of this is AFML ch. 7, which is **not currently in the corpus** — see `_AFML_PENDING.md`. Until it
  arrives this rule is asserted from our own leakage history, not derived.)*
- **[[direction-is-unpredictable]] still binds, and a model does not repeal it.** Negative OOS R² for
  direction and mean was measured across 445 series, 4 asset classes, 4 frequencies. An ML model
  predicting returns is a conditional-mean test with more parameters. If a pass ends up forecasting
  direction, it has walked into the one result the log is most sure of.
- **Trial counts are the statistician's rule and apply in full here** — including every architecture,
  hyper-parameter grid and feature set tried. A hyper-parameter sweep is a trial count, not a
  free parameter.

## The EDA this lens wants
1. **Measure the linear benchmark, everywhere reachable.** What *is* the out-of-sample R² of a two- or
   three-predictor linear model on each universe and frequency we can trade? Gu-Kelly-Xiu report
   0.16%/month for theirs; we have no equivalent number for anything. Until that table exists this
   lens cannot tell a gain from a baseline.
2. **Breadth audit against the published settings.** Assemble what we could actually build —
   instruments × history × predictors — per universe, and put it beside the settings in which these
   methods were demonstrated. That map decides where this lens can operate at all, and it may
   conclude nowhere.
3. **Complexity ramp on our own panels.** Does out-of-sample performance rise monotonically with
   model capacity, peak and fall, or fall from the start? The corpus makes a strong claim about
   over-parameterisation; it is directly testable on data we hold, and the answer is a fact about our
   data rather than about the literature.
4. **Meta-labelling on already-banked signals.** Predict *whether to act* on an existing signal rather
   than predicting direction. #027 (real IC +0.0205, ~30σ, decays 75%/bar) and #044 (passed a
   pre-registered sealed test at 9.8x cost) both have banked data and a known weak edge — the exact
   shape this technique addresses, and the only route in the corpus that does not run head-first into
   [[direction-is-unpredictable]].
5. **Where does non-linearity actually exist?** Take relationships we have already measured linearly
   and test for interaction and non-monotonicity. Cheap, and it answers whether this lens has anything
   to do here before any model is built.

## Backing

| source | who | what it is |
|---|---|---|
| **Kelly & Xiu (2023), *Financial Machine Learning*** (Foundations & Trends in Finance) | Kelly — Yale SOM + AQR head of machine learning; Xiu — Chicago Booth | 160pp survey: the case for financial ML, complex models, return prediction, risk-return tradeoffs, optimal portfolios |
| **Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning*** (RFS) | as above | 80pp. The method horse race on 30,000 US stocks, 1957–2016 |
| **López de Prado (2020), *Machine Learning for Asset Managers*** (Cambridge Elements) | AQR head of ML → Guggenheim head of global quant research → Cornell | 152pp, 8 chapters. Denoising, clustering, labels, feature importance, testing-set overfitting |
| **Hastie, Tibshirani & Friedman, *ESL*** (2nd ed.) | Stanford | 764pp. Instrument reference only — how to compute, never what to expect |
| **López de Prado (2018), *Advances in Financial Machine Learning*** | as above | **HELD since 2026-08-22** — 481pp, 22 chapters, hand-mapped to `.txt`. The intended spine, and now the primary source for labeling/meta-labeling (ch3), sample weights (ch4), purged CV (ch7), feature importance (ch8), bet sizing (ch10), backtest statistics (ch14) |

## Corpus
`_material/machine_learning/INDEX.md` is the entry point. **Grep the index, open one section, read
that slice.** Every PDF has a `.txt` twin; never open a PDF to browse.

---

## GREP LOG
*What has already been read, and what was taken from it. Check here before grepping — a **coverage
record, not a prohibition**: re-read freely if the question is different, and say why. Anything not
listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-22 | `kelly_xiu_financial_machine_learning/02_the_virtues_of_complex_models.txt` (first ~3.4k chars) | The parsimony principle is contested: models that exactly fit training data are often best out-of-sample in vision and NLP. Belkin (2021): *"the largest technologically feasible networks are consistently preferable."* Breiman's question — why don't heavily parameterised networks overfit? Terms to follow: **over-parameterisation, benign overfit, double descent**. Kelly's framing is economic (the risk-return tradeoff of ML portfolios), not just statistical |
| 2026-08-22 | `gu_kelly_xiu_empirical_asset_pricing_ml/03_…_main.txt` | Setting: ~30,000 stocks, 1957–2016, 94 characteristics × 8 macro series × 74 industry dummies = **900+ baseline signals**. Benchmark = 3-characteristic panel (size, book-to-market, momentum), OOS **R² = 0.16%/month**. Expanding OLS to 900+ predictors sends R² **deeply negative** — the failure is estimation efficiency, not absence of signal |
| 2026-08-22 | `gu_kelly_xiu_empirical_asset_pricing_ml/04_what_machine_learning_cannot_do_literature.txt` | ML predictions are **measurements, not mechanisms** — they do not identify economic associations. To get a mechanism the economist must build the hypothesised structure into the estimation problem |
| 2026-08-22 | `deprado_ml_for_asset_managers/08_8_testing_set_overfitting.txt` (first ~2.8k chars) | A backtest is not a controlled experiment — you cannot re-run history with changed variables, so backtests cannot establish cause. **Selection bias under multiple testing (SBuMT)**: present the best of many simulations as a single trial and performance is inflated. **Backtest hyperfitting** — the two-level version where researchers select from their own runs and the firm then selects among researchers. Monte Carlo on synthetic data is offered as the controlled alternative |
| 2026-09-01 | `gu_kelly_xiu_empirical_asset_pricing_ml/05_sample_splitting_and_tuning_via_validation.txt` | **The three-way split, and why two is not enough.** *"we divide our sample into three disjoint time periods that maintain the temporal ordering of the data"* — train estimates parameters, validation tunes hyperparameters, test is untouched. The load-bearing sentence: *"The validation sample fits are of course **not truly out-of-sample** because they are used for tuning."* Anything used to CHOOSE (depth, trees, a threshold) stops being out-of-sample |
| 2026-09-01 | `gu_kelly_xiu_empirical_asset_pricing_ml/14_an_empirical_study_of_us_equities.txt` | **The horse race verdict, and it is not trees.** OOS R²: OLS-3 benchmark 0.16%, random forest 0.33%, boosted trees 0.34%, NN1 0.33%, **NN3 0.40%** — *"Neural networks are the best performing nonlinear method, and the best predictor overall."* Linear models are *"handily outperformed by tree-based models and neural networks"*; the gain is *"the value of incorporating complex predictor interactions."* Also: *"Random forests generally estimate shallow trees, with one to five layers on average"* |
| 2026-09-01 | `deprado_advances_financial_ml/ch06_ensemble_methods.txt` §6.6 | **Bagging over boosting, for finance specifically.** *"Boosting's main advantage is that it reduces both variance and bias... However, correcting bias comes at the cost of greater risk of overfitting. It could be argued that in financial applications bagging is generally preferable to boosting. Bagging addresses overfitting, while boosting addresses underfitting. Overfitting is often a greater concern than underfitting, as it is not difficult to overfit an ML algorithm to financial data, because of the **low signal-to-noise ratio**."* Directly contradicts a default choice of GBM on our data |

**Untouched:** Kelly & Xiu sections 1, 3–7 (return prediction, risk-return tradeoffs, optimal
portfolios — the bulk); Gu-Kelly-Xiu sections 1–2, 6–13, 15 (the individual method treatments);
de Prado MLAM chapters 1–7; **AFML chapters 1–5 and 8–22 except ch6** — including ch3 (labeling /
triple barrier), ch4 (sample weights, uniqueness), ch7 (purged CV) and ch8 (feature importance),
all four of which the #046 build depends on and none of which has been read yet; all 23 ESL sections.

## Log
- **2026-08-22 written.** Second corpus-backed lens, first built on the no-fundamentals template from
  the start. Nothing run yet. Cheapest real lead: **EDA 1** — the linear benchmark number does not
  exist for any universe we trade, it is cheap to compute, and without it nothing else in this file
  can be interpreted.
