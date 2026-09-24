# Part II-D — Robustness, Risk & Tooling (Ch. 11–17)

*Seven chapters: how to organize the search (11), make a signal robust (12), handle known risk factors (13), manage risk & drawdowns (14), scale via automated search (15), the ML toolbox (16), and the algorithm toolkit (17).*

---

## Ch. 11 — Triple-Axis Plan (TAP): organize the search

The alpha space is huge; new quants "dig one gold mine" — rebuilding the same alpha type, which *looks* low-correlated but shares **failure modes**. TAP structures the search on three axes:

| Axis | Examples |
|---|---|
| **Ideas & Datasets** | reversion, momentum, seasonality, lead-lag, ML / fundamentals, analyst, sentiment, social, options |
| **Regions & Universes** | US, Europe, Asia, global / TOP50…TOP1500, sector, instrument groups |
| **Performance Parameters** | high return, high Sharpe, low cost, low drawdown |

**How to use:** freeze one axis (e.g. "momentum"), then systematically vary the other two. Reveals the *missing* corners of your portfolio. Three levels: pick a focus → fill in the other axes → implement & iterate.

---

## Ch. 12 — Robustness techniques

A **robust alpha** is invariant to universe changes and doesn't collapse in extreme conditions. Three families:

- **Ordering methods** (nonparametric → invariance):
  - **Ranking** → rescale to [0,1]; invariant to any monotone transform. Use **Spearman** over Pearson (Pearson unstable for nonstationary/nonlinear inputs).
  - **Quantile approximation** / least-quantile-of-squares (e.g. median-squares) instead of unstable OLS.
- **Approximation to normal** (when data is ~normal but contaminated):
  - **Fisher transform**: `F(x) = ½·ln((1+x)/(1−x)) = arctanh(x)` (for `|x|<1`). `F(x)` is ≈ normal with standard error `1/√(N−3)`.
  - **Z-scoring**: `Z = (x − μ)/σ` → zero mean, unit std (distance from mean in std units).
  - (Normal pdf, for reference: `f(x|μ,σ²) = 1/√(2πσ²) · exp(−(x−μ)²/(2σ²))`.)
- **Limiting methods** (tame outliers):
  - **Trimming** (drop a fraction beyond threshold), **Winsorizing** (replace extremes with the cutoff value). Both → estimators much closer to the robust median. (All four — mean, median, k-trimmed mean, k-winsorized mean — are special cases of L-statistics, i.e. linear combinations of order statistics.)

⚠️ These assume *roughly-normal-but-contaminated* data. They **mislead** on inherently skewed data or when many values are identical.

---

## Ch. 13 — Alpha and risk factors

Lineage: CAPM → APT → **Fama-French 3-factor** (market, size, value) → **5-factor** (+profitability, +investment); plus momentum, liquidity, accruals (not absorbed).

```
CAPM:  Expected return = Risk-free rate + (market β) × (Market risk premium)
APT:   Expected return = Risk-free rate + Σ (factor βₖ) × (factor k risk premium)
```
In practice APT factors are built as **dollar-neutral & market-β-neutral portfolios**, each of which can itself be evaluated as a tradable alpha. Over time, published "alphas" decay into **hedge-fund betas / risk factors** (value Sharpe: 0.56 in 1950–89 → 0.11 in 1990–2017 after wide publication). **Adaptive Market Hypothesis** (Lo): opportunities are food in an ecology — found fast, wax and wane, sometimes reappear.

**Operational takeaways:**
- Your alpha may **unintentionally load** known factors (e.g. news-sentiment loads momentum) even without using price.
- **Neutralize known factors** via multivariate regression of the alpha against factor portfolios.
- Sharpe usually **rises after neutralization** even if per-dollar return falls (Ch. 13 Table 13.1: 1.55 → 1.84 after neutralizing momentum+size+value).
- Avoid high factor loadings: they have crowded, correlated unwinds (Aug-2007 quant crisis), require imbalanced long/short liquidity (size, liquidity factors), and suffer long macro drawdowns.

---

## Ch. 14 — Risk and drawdowns

Risk spectrum: unknowable (black swans/Knightian — don't overfit to the last one) → asset/operational → **extrinsic** & **intrinsic** (the focus).

- **Extrinsic risk** (external: industry, market, FF/Barra factors, event risk) → **neutralize or hedge**.
  - *Hard neutralization*: force risk to 0 (subtract group mean / orthogonalize / subtract β·factor) → dollar-neutral, industry-neutral.
  - *Soft neutralization*: cap exposure (partial subtraction or constrained optimization).
  - *Hedging*: offset with a correlated liquid instrument (S&P futures for market β; FX for currency) — imperfect but useful when shorting is hard.
- **Intrinsic risk** (the alpha's own return source) → can't eliminate, must **size dynamically**. When risk ↑, scale book size ↓. Use volatility / VaR / expected-tail-loss / position concentration; combine measures and use the most conservative. Stop-loss/take-profit = short-term sizing constraints.

**Measurement — two lenses:**
- *Position-based*: concentration, orthogonal projection onto a factor, regression β. Brittle, extreme-only.
- *PnL-based*: smoother. Check **sector PnL concentration** (Fig 14.1: alpha driven only by energy+IT is fragile) and **quintile distribution**:
  - *Ideal*: top quintile → positive returns, bottom → negative (monotone).
  - *Tails-only*: middle quintiles are noise → consider dropping sub-threshold instruments (but raises volatility).
  - *Dead-tails*: strongest signals don't work → probably not robust; refine or discard.

**Drawdown bootstrapping (clever, hard-to-overfit):**
1. Measure PnL autocorrelations (use only if finite/significant).
2. Build 1,000 synthetic 10-yr PnLs by resampling PnL snippets of autocorrelation length (with replacement).
3. Take the **90th-percentile max-drawdown** of the synthetics.
> If realized drawdown drops but bootstrapped doesn't, you've *masked* risk, not controlled it.

**"Just get out":** when underlying assumptions break (depeg, counterparty risk, unanticipated regime), no in-alpha logic will save you — exit.

---

## Ch. 15 — Alphas from automated search

Scales to thousands/day, but amplifies overfitting. Three problems: compute load, can't inspect each formula, lower per-alpha confidence. Treat input data / search algorithm / signal testing as the three components.

**Operating rules:**
- [ ] **Few data categories** — each has its own frequency (fundamentals quarterly, price-volume uniform, insider random); mixing many → complex & noise-prone.
- [ ] **Unitless, cross-comparable ratios** — raw price/earnings aren't comparable across stocks; use E/P (not P/E — P/E diverges near zero earnings), earnings/revenue, price/avg-price.
- [ ] **Prune the search space** — drop nonsensical function/data pairs (no `log` of returns); drop slow-varying data for short-horizon search; use **iterative coarse→fine grid** search.
- [ ] **Reuse intermediate variables** (e.g. P/E composite) — basis of genetic algorithms.
- [ ] **Seas of alphas, not one** — seek many local optima over a wide area, not the global optimum.
- [ ] **Simple > complex** — limit search *depth*, expand *breadth*; fewer but higher-quality alphas.
- [ ] **Longer backtests** raise significance only if dynamics are stable; use incremental-period iterative search (adds a quasi-OOS test each round).
- [ ] **Judge the batch, not single alphas** — batch performance is the unit (like an orchestra).
  - ⚠️ **Selection bias**: picking the OOS winners makes it no-longer-OOS. Accept/reject the *whole batch* on average significance (the example: 100 alphas, 60 positive OOS, but average OOS IR too low → reject **all 100**).
- [ ] **Yield test**: feed *noise* inputs; a good search space must yield meaningfully better than noise, else the process is broken.
- [ ] **Sensitivity/significance tests**: signal should be insensitive to data perturbations; each input should materially contribute (drop it / replace with noise and check).
- [ ] **Start manual** before automating the same inputs.

---

## Ch. 16 — Machine learning (toolbox survey)

Problem types: regression, classification, clustering. Core dilemma = overfit (complex) vs underfit (simplistic). Methods, by usefulness here:
- **Statistical models** (naive Bayes, LDA, logistic, **HMM** for regime/trend detection) — simple, robust to missing data, assume a data model.
- **SVM/SVR** — strong theory, prevents overfit, but slow & poor for parallelism; SVR margins can model volatility/asymmetric downside.
- **Neural nets** — flexible, powerful with compute, but opaque and atheoretical.
- **Ensembles (random forest, AdaBoost)** — *most relevant*: combine many **weak** predictors/alphas into a strong one (directly mirrors the WorldQuant breadth model). Variants AsymBoost/FloatBoost tune false-positive costs.
- **Deep learning** (RBM/CNN/RNN — vanishing gradient) and **fuzzy logic** — surveyed, lighter relevance.

*This chapter is the weakest/most dated — taxonomy more than how-to.*

---

## Ch. 17 — Thinking in algorithms (the toolkit)

- **Digital filters**: FIR (no feedback) vs IIR (feedback); low/high/band-pass/band-stop. MAs are low-pass filters. Use a **Butterworth** low-pass for smoothing with less lag; subtract low-pass from raw to get high-pass. Decompose series into trend+cycle for better signals.
- **Loss-function design**: **L2** penalizes big errors (good average fit, fragile to outliers); **L1** robust & sparse but unstable; **Huber** = L2 near zero, L1 in the tails (best of both). Regularization: **ridge** (L2 on coefficients), **lasso** (L1 → feature selection), **elastic net** (both).
- **Bias–variance**: curse of dimensionality (need exponentially more data per feature) + information decay (old data less relevant). High variance → overfit; high bias → underfit. Counter with dimensionality reduction or prior knowledge.
- **Dimensionality reduction**: **PCA** (risk models, principal portfolios, clustering); **sparse PCA** (few variables per component → better noise removal & feature selection).
- **Shrinkage**: pull a noisy raw estimator toward a structural one (trade a little bias for much less variance). **Ledoit-Wolf** covariance shrinkage → better portfolios than the sample covariance.
- **Parameter optimization**: prefer **dynamic** params (vary with time & cross-section, e.g. holding period ∝ market cap) over static; close the feedback loop with realized OOS performance → **self-adaptive** algorithms.

---

## Master checklist (Part II-D)

- [ ] Use **TAP** to find the empty corners of your portfolio, not just dig deeper.
- [ ] Make signals robust: **rank** for invariance, **winsorize/trim** outliers, Z-score/Fisher where ~normal.
- [ ] **Neutralize** known risk factors; expect Sharpe to rise.
- [ ] Separate **extrinsic** (neutralize/hedge) from **intrinsic** (size dynamically) risk.
- [ ] Diagnose with **sector PnL** + **quintile** distributions; estimate drawdown by **bootstrapping**.
- [ ] In automated search: unitless inputs, prune space, breadth>depth, **judge the batch**, run the **yield test**, beware **selection bias**.
- [ ] Toolkit reflexes: Butterworth smoothing, Huber/elastic-net losses, PCA/sPCA, Ledoit-Wolf shrinkage, dynamic parameters.
