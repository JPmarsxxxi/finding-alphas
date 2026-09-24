# Part III-A — Price/Volume & Momentum (Ch. 18, 21)

*Signals built from market data alone (no fundamentals, no text). The bread-and-butter of alpha hunting.*

---

## Ch. 18 — Equity Price & Volume

**Why price-volume alphas exist:** strong-form EMH says they can't, but markets are never fully efficient. Price-volume alphas "refute the EMH every day."

**Trading frequency ↔ significance ↔ cost:**
- More frequent trading → more statistically significant results. The mean of `N` iid draws has the same mean but `1/√N` the std → trade **4× more often → ~2× the IR** (same IC).
- But cost scales with frequency: strategies turning over **>5×/year can lose >1%/month** to costs (Novy-Marx & Velikov 2015). Always a high-IR vs low-cost trade-off.

**Momentum-Reversion (horizon-dependent):**
- Single instruments: **mean-revert** over short horizons (intraday/daily), **trend** over longer ones (weeks/months).
- Within a correlated group (industry): stronger stocks tend to **revert** to weaker.
- Sample strategies (S&P 500, trend-following, ~10.5–11.6% ann, Sharpe 0.54–0.62):
  - **MA rule**: buy when price > 250- or 500-day average.
  - **MA crossover**: buy when short MA > long MA.
  - **Breakout**: buy at an x-day high.
- Intraday mean-reversion: when prior day is down and `(high − low) > threshold`, buy prior-day low, sell at close (volatility → stronger reversion).

**Technical indicators:**
- **MACD** = `short-term MA(price) − long-term MA(price)` (momentum).
- **ATR** = moving-average-based volatility, typically 14-day.

**Other price-volume signals:**
- **Integer / round-number effect**: humans cluster orders at round prices (100, not 155.29); also loss aversion / holding losers too long.
- **Price-volume + events**: volume shocks predict returns. Frazzini-Lamont (2007): buy stocks expected to announce earnings next month, short those not → 7–18% excess (strong for large caps).

**Checklist:** pick frequency for the signal's horizon; respect the >5×/yr cost cliff; decide momentum *or* reversion by horizon & grouping; combine price-volume with events for extra power.

---

## Ch. 21 — Momentum Alphas

**Core fact:** Jegadeesh-Titman (1993) — past 3–12 month winners/losers keep winning/losing. Works across asset classes & markets globally; shrank recently, big drawdown around 2008.

**Why it works (behavioral):** investors **underreact** to new info (conservatism bias); it takes time to price in. Momentum even **builds before** announcements (expectations via analyst forecasts). Delayed-overreaction theory → eventual reversal (short-term momentum, long-term reversal).

**Risk vs return source — the key practical distinction:**
- In many signals, momentum is an **unintended risk loading** → neutralize it (see [[part-2d-robustness-risk-and-tooling]], Ch. 13).
- In others (e.g. seasonality), momentum is the **intended return driver** → do NOT neutralize.

**Where momentum is stronger:** high bid-ask spread (illiquidity premium), low analyst coverage (slow info diffusion), growth stocks (harder to value), high-volume stocks (Lee-Swaminathan).

**Momentum variants:**
- **Factor momentum**: factor returns are more stable & trend more than single stocks; trade factors the market currently favors (reverse-engineer mutual-fund holdings).
- **Group / industry momentum** (Moskowitz-Grinblatt): high-industry-return stocks outperform over the next 6 months.
- **Lead-lag**: leaders in a group move first; lagged stocks inherit the momentum (and across supply-chain-linked groups).
- **Seasonality**: quarter-ending months show higher momentum returns (window-dressing + tax-loss selling).

**Checklist:** decide if momentum is signal or risk for your idea; pick the 3–12mo formation horizon; consider group/industry/lead-lag forms; mind transaction costs (momentum often lives in illiquid names).
