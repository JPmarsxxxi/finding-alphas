# Part III-F — Market Microstructure & Intraday Trading (Ch. 26, 27)

*The high-frequency end: order books, spreads, informed-trading models, and how to actually build an intraday alpha.*

---

## Ch. 26 — Intraday Data & Market Microstructure

**Market types:** quote-driven (dealers/market-makers quote bid/ask) vs order-driven (a public **order book** crosses limit orders). Equity alpha research is mostly order-driven.
- **Limit orders** provide liquidity (build the book); **market orders** consume it. Book *depth* = price impact of trading a given size → lets you estimate after-impact alpha performance.

**Illiquidity premium:** investors demand excess return for higher trading cost → positive spread↔return relationship.
- Amihud-Mendelson (1986): **+1% spread → +0.211% monthly risk-adjusted return**.
- Breakeven horizon: `1 / 0.211 ≈ 5 months` — a 1% extra fixed cost is repaid over ~5 months. So buy-and-hold (≥5mo) or daily alphas with **turnover < ~1%** (`0.211/21`) profit from high-spread assets.
- **Amihud illiquidity (2002)** = avg daily `|return| / dollar volume`; +1pp → +0.163% monthly.
- Liquidity isn't constant — spreads spike in crises (Pástor-Stambaugh: high liquidity-beta stocks earn ~7.5%/yr over low).

**Glosten-Milgrom (1985) spread formation** — informed traders (fraction π, know value `v^H` or `v^L`) vs uninformed (random, 50/50); risk-neutral specialist breaks even on bid & ask:
```
(1)  θπ(a − v^H) + 0.5(1−π)(a − v) = 0
(2)  θπ(v^L − b) + 0.5(1−π)(v − b) = 0
(3)  S = [θπ(1−θ)(v^H − v^L)] / [(θπ + 0.5(1−π))·((1−θ)π + 0.5(1−π))]
(4)  with random walk (θ = 0.5):   S = π(v^H − v^L)
```
→ **spread is linear in the probability of informed trading π**. Easley et al. (2002): **PIN** (probability of informed trading); +10pp PIN → +2.5%/yr premium. Ormos-Timotity: heuristic-driven traders (PH), +10pp → +4.5%/yr.

**DPIN** (dynamic, faster than max-likelihood PIN), size-filtered:
```
DPIN_size = [ (NB/NT)·𝟙(ε<0) + (NS/NT)·𝟙(ε>0) ] · LT
```
`NB`/`NS`/`NT` = buy/sell/total trades, `ε` = autocorrelation-filtered return, `LT` = large-trade indicator (informed trades are large; they buy when price falls / sell when it rises).
```
FSRV = log((1 − R²) / R²)     # firm-specific return variation; R² = market-model fit
```
Higher DPIN → higher FSRV (more idiosyncratic variance).

**Microstructure as a drawdown predictor:** informed-trading ramps precede crashes — VPIN peaked before the 2010 flash crash; PIN spiked at the 2000 dot-com peak. Practical use:
- **Low PIN** → technical/group-momentum alphas work better (patterns persist longer).
- **High PIN** → fundamental/insider-based alphas have higher Sharpe (firm-specific info dominates).

**Intraday patterns:** U-shaped volume & volatility, reversed-J spreads → trade when volume is high & spreads low for better after-cost performance.

---

## Ch. 27 — Intraday Trading

Buying & selling within one day. Fewer usable data sources (most daily signals have too-long horizons) but order-book/microstructure data shines. **Cost matters at the single-alpha level** (less crossing than daily — see [[part-2b-cost-and-uniqueness]]).

**Advantages over daily:** much higher returns/significance even on short backtests → OOS ≈ in-sample; overnight risk factors (dollar/sector exposure) are **tolerable below a threshold** because you can exit fast → use them to boost returns.
**Constraint:** liquidity restricts you to the top **200–500** instruments → smaller capital. Liquidity is U-shaped intraday (trade away from high-slippage open).

**Alpha types:**
- **Overnight-0** = no overnight positions (classic intraday).
- **Overnight-1** = holds overnight / intraday overlay on overnight positions.
- Continuous allocation vs discrete **entry/exit (event) signals** with stop-loss / profit-target exits.

**Worked example — intraday mean reversion** (overnight-0, top 500, dollar-neutral via subtracting cross-sectional mean):
```
Base:         alpha = (second_last_interval_close − last_interval_close)
×volatility:  alpha = (second_last_interval_close − last_interval_close) · std(close)   # over past 30–40 intervals
              → higher margin (better after-cost) but LOWER Sharpe (vol is in the denominator of Sharpe)
÷volatility:  alpha = (second_last_interval_close − last_interval_close) / std(close)
              → higher Sharpe but lower returns/margin
```
The margin-vs-Sharpe choice depends on whether transaction costs dominate. Variant: use the cross-sectional **rank** of `std(close)` instead of absolute values.

---

## Checklist

- [ ] Use order-book depth to estimate after-impact performance before trusting an intraday backtest.
- [ ] Match alpha style to PIN: technical when PIN low, fundamental when PIN high.
- [ ] Watch microstructure ramps (VPIN) as an early drawdown warning.
- [ ] Intraday: stick to top 200–500 liquid names, trade away from the high-slippage open, decide overnight-0 vs -1.
- [ ] Tune the volatility multiplier/divisor by whether margin (cost) or Sharpe is your binding constraint.
