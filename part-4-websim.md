# Part IV — WebSim: the Simulation Platform (Ch. 31)

*WorldQuant's free, web-based backtesting platform — the tool behind every "simulation result" figure in the book. This is the operational counterpart to Parts I–III.*

> **Naming note:** the book (2020) calls it **WebSim** at `worldquantvrc.com`. It has since been rebranded **WorldQuant BRAIN** (`platform.worldquantbrain.com`) with expanded data/operators. Same concepts; search "WorldQuant BRAIN" today.

---

## What it is & why it exists

A market-simulation platform with a built-in knowledge base + educational component. Purpose: let anyone create, test, and get quantitative feedback on alphas (vs market and vs peers). Doubles as WorldQuant's **recruiting funnel** — qualifies remote Research Consultants and powers competitions (WorldQuant Challenge, International Quant Championship). Users are global and diverse (students, professors, gamers, even farmers); common trait = strong math + curiosity about markets.

---

## How an alpha is structured

In WebSim an alpha = **Data + Mathematical operators + Constants**, written as a simple math expression. The output value per instrument is a **relative portfolio weight**: positive → long, negative → short.

```
delta(close, 5)
# assigns each stock a position = (today's close − close 5 days ago)
```

Alphas can be trivial or complex; operator libraries assist. (See the expression vocabulary in [[part-2a-build-loop]] — `rank`, `delay`/`delta`, `decay`, `correlation`, etc.)

---

## Simulation settings (the knobs that change results)

| Setting | What it does | Practical guidance |
|---|---|---|
| **Region** | US / Europe / Asia | only that region's stocks are simulated |
| **Universe** | TOP200 … TOP3000 | top-N most liquid (by avg daily $ volume) |
| **Delay** | 0 = today's price, 1 = yesterday's | delay-1 is the safe default (no look-ahead) |
| **Decay** | linear-weighted blend of today's + prior days' alpha values | smooths signal, **lowers turnover** |
| **Max stock weight** | caps any single stock's weight | **0.05–0.1** typical; higher = more return + idiosyncratic risk; can be larger for small universes |
| **Neutralization** | demean by industry / market / subindustry | makes the book market-neutral (no directional exposure) |
| **Lookback days** | prior days of data loaded per simulation day | doesn't change alpha values; lower = faster, higher = needed for quarterly/annual fundamentals |

---

## Reading the results

WebSim runs a daily backtest on a fictitious **$20M book**, redistributing capital long/short across the universe per the alpha values (after neutralization + decay). Output = PnL graph + metric table.

**What to check, in order:**
1. **Profitable?** Are PnL and returns adequate?
2. **Sharpe ratio** (returns/volatility) — proxy for predictive ability; higher = more reliable.
3. **Turnover** — trading volume needed to reach desired positions. **>40% is a warning** — transaction costs (fees + spread) may eat the PnL. (Reduce via decay; cf. [[part-2b-cost-and-uniqueness]].)
4. **Distribution charts** — confirm positions/returns are spread across cap/industry/sector, not concentrated (cf. quintile/sector diagnostics in [[part-2d-robustness-risk-and-tooling]]).
5. If thresholds are met → **out-of-sample** test on more-current data.

---

## Worked example (fundamental ratio → alpha)

Hypothesis: high & rising debt-to-equity = risk (short); low D/E = value (long).
```
Ts_rank(-debt/equity, 240)
# time-series rank of −(debt/equity) over 240 days → picks longs/shorts from recent balance sheets
```
The book's sample-alpha footnote also gives:
```
Alpha = rank(sales / assets)
```

These tie straight back to the Part III idea cookbook — e.g. the fundamentals factors in [[part-3b-fundamentals]] and the price-volume/momentum expressions in [[part-3a-price-volume-momentum]].

---

## Checklist for a WebSim run

- [ ] Find an idea (papers/SSRN/Seeking Alpha/Wilmott, technical indicators: RSI, MFI, MACD, Bollinger).
- [ ] Express it as `operators(data, constants)`.
- [ ] Set region → universe → delay-1 → neutralization → decay → max stock weight (0.05–0.1) → lookback.
- [ ] Run; read PnL → Sharpe → turnover (<40%) → distribution charts.
- [ ] Iterate one motivated lever at a time (the Ch. 5 refine loop), then validate out-of-sample.
