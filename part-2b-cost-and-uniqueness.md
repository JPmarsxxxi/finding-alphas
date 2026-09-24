# Part II-B — Cost & Uniqueness (Ch. 7–8)

*Two things that decide whether a "good" alpha is actually usable: trading cost (turnover) and how different it is from what you already have (correlation).*

---

## Turnover (Ch. 7)

**Definition:** `turnover = value traded / value held`. Driven by how fast the underlying data changes.

**Horizon ↔ turnover ↔ cost trade-off:**
- Shorter horizon → more info, higher raw IR/IC → but higher turnover, higher cost, tighter execution window (may have to cross the spread).
- Longer horizon → lower turnover, lower cost, better execution, higher capacity — sometimes *better after costs even if worse before*.
- Price-based alphas turn over faster than fundamental alphas (price moves every tick; EPS moves quarterly).

**The cost of a trade:** commission + **spread** (bid < ask; you cross it). Cost scales with illiquidity:
- Top-500 US ≈ 5 bps spread; Southeast Asia ≈ 25–30 bps.
- Same alpha, wider/less-liquid universe → much larger after-cost deterioration even at similar turnover (Ch. 7 example: top-1000 lost ~4 bps margin, top-3000 lost ~10 bps).

### The crossing effect — *the key idea of this chapter*
Individual alphas are usually too weak to survive costs alone. In a combined strategy, opposing trades **cross**: alpha A buys 200 IBM, alpha B sells 300 IBM → only 100 net shares hit the market; the other 200 are **cost-free**.

> Therefore: **don't reject a high-turnover alpha purely on its standalone after-cost performance.** Its real value shows up after crossing inside the pool. Wider universes and more uniform (non-spiky) turnover profiles → more crossing opportunities.

### Controlling turnover (techniques)
- **Clamp / winsorize** outliers (bounds = percentile or N-sigma).
- **Hump / threshold**: ignore changes below a threshold (keeps previous value). Reduces turnover but creates a concentrated, bursty trade profile.
- **Decay / smoothing**: EMA or simple/weighted MA → smoother profile, similar turnover reduction.
- **Tuning rule:** a good turnover level *maximizes IR (or profit) / turnover*. Don't decay past the alpha's horizon — you'll slow the signal beyond where the return lives. Short-horizon signals tolerate less decay than long-horizon ones.
- Test across **multiple universes/liquidity sets** — a turnover fine in top-500 may be untradable in top-3000 or a developing market.

### Cost-aware construction (net-of-cost weighting)
The crossing effect handles *trade* cost at the batch level; **holding cost** (swap/borrow on overnight positions) is handled at the *weighting* step. When holding cost is **dispersed / asymmetric across instruments** (FX, indices, metals, oil — not crypto, whose swap is symmetric), don't weight by naive rank — solve for weights **net of cost**: `max αᵀw − (γ/2)wᵀΣw − cost_longᵀw⁺ − cost_shortᵀw⁻`. The optimizer tilts toward cheap-to-hold names and drops legs where the swap exceeds the signal.

> **Load-bearing caution (validated live, alpha log #036c):** optimizing *without* the cost term can be **worse than equal-weight** — it concentrates into the highest-signal names, which on a swap book are the highest-*cost* names. On the killed FX-carry book, net of real FTMO swap: equal-weight −0.11, **cost-blind −0.50**, **cost-aware +0.26** Sharpe. If you optimize, optimize net of cost.

- **It reallocates, it does not manufacture a mean.** Needs a real gross signal *and* cost dispersion. On weak carry it only reached breakeven — the rescue can't exceed what the signal carries.
- **Dynamic variant** (Gârleanu-Pedersen "aim portfolio"): trade *partially* toward the target and weight **slow-decay signals more** (fast signals cost too much to chase). Handles turnover-over-time; pair with the static holding-cost weighting.
- Code: `backtest/alpha_pipeline/cost_aware` (static) + `garleanu_pedersen` (dynamic), fed by the `backtest/costs/Swap` model (one source: the same swap the engine charges). Skill `17b-cost-aware-construction.md`. Papers: Gârleanu & Pedersen (2013 JF); Boyd et al. (cvxportfolio).

---

## Alpha correlation (Ch. 8)

Uniqueness is a first-class quality metric. Lower correlation to the existing pool → more diversification value. Matters more as the pool grows.

**Setup:** two PnL vectors over `n` days, `Pᵢ = [Pᵢ₁,…,Pᵢₙ]`, `Pⱼ = [Pⱼ₁,…,Pⱼₙ]`.

**What you can correlate:**
- **PnL correlation** — over a long window (2–4 yrs). Variants:
  - *Pearson* (standard; invariant to linear transforms; demeaned):
    ```
    r = cov(Pᵢ,Pⱼ) / (σ_Pᵢ · σ_Pⱼ)
      = Σ(Pᵢₖ − P̄ᵢ)(Pⱼₖ − P̄ⱼ) / [ √Σ(Pᵢₖ−P̄ᵢ)² · √Σ(Pⱼₖ−P̄ⱼ)² ]
    ```
  - *Dot-product / angle* (raw, un-demeaned): `cos(θ) = (Pᵢ·Pⱼ)/(|Pᵢ||Pⱼ|)`. θ=0 → identical line; θ=90° → orthogonal. (Note: uncorrelated ≠ orthogonal, because Pearson demeans first.)
  - *Temporal-weighted* — weights recent days more:
    ```
    r = Σ wₖ Pᵢₖ Pⱼₖ / [ √Σ wₖ Pᵢₖ² · √Σ wₖ Pⱼₖ² ],   e.g. wₖ = 1 − k/n
    ```
  - *Generalized* — transform both PnL vectors by a matrix `M`, then correlate: `Qᵢ = M·Pᵢ`, `Qⱼ = M·Pⱼ`.
    - `M = identity` → plain Pearson.
    - *Weekly*: `M` averages blocks of 5 days (`mᵢ,(i−1)·5+t = 1/5`), so `k = ⌈n/5⌉` rows. (Weekly corr usually > daily.)
    - *Temporal*: `M` = square diagonal with `mᵢᵢ = √wᵢ`.
  - *Sign correlation* — correlate the signs: `Qᵢ = [sgn(Pᵢ₁),…,sgn(Pᵢₙ)]`, `sgn ∈ {+1, 0, −1}`.
- **Position & trading correlation** — over a short recent window (`d ≈ 20` days × #instruments `m`). Position vector on day `t`: `αᵗ = [α₁ᵗ,…,α_mᵗ] ∈ ℝᵐ` (αₖᵗ ∝ $ in instrument k; Σ|αₖᵗ| ∝ total $).
  ```
  Position corr:  correlate  αᵢ = [αᵢ¹, αᵢ², …, αᵢᵈ]                (∈ ℝ^{m·d})
  Trading  corr:  correlate  the differences [αᵢ¹−αᵢ², αᵢ²−αᵢ³, …]   (∈ ℝ^{m·(d−1)})
  ```
  Use the universe intersection if two alphas trade different sets.

**Pool-level measures (use the distribution, not one number):**
- *Max correlation* — value added vs the single closest alpha.
- *Average correlation* / *T-corr* (sum of correlations with all others) — more meaningful as pool grows.
- *Correlation density histogram* — richest view; the whole shape matters more than max or mean.

**Practical nuance:** highly-correlated alphas from one idea aren't necessarily redundant — split capital across them rather than picking one, since you don't know which will work *forward*. Each represents the idea differently; together they're more robust. The most value comes from an alpha on a **genuinely novel idea**.

---

## Quick checklist

- [ ] Compute turnover; relate it to the intended horizon.
- [ ] Charge realistic spread cost; check margin (PnL/$traded) per universe.
- [ ] Before rejecting on after-cost numbers, ask: will it **cross** inside the pool?
- [ ] Reduce turnover via clamp / hump / decay — but never past the horizon; target max IR/turnover.
- [ ] Measure correlation to the pool (PnL long-window; position/trading short-window).
- [ ] Judge uniqueness by the **distribution** (max + average + histogram), not one max.
- [ ] Prize genuinely novel ideas — they add the most.
