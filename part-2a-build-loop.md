# Part II-A — The Build Loop (Ch. 4–6)

*How to go from raw data to a tested alpha. Covers Alpha Design (4), the Case Study (5), and Data (6).*

---

## Core mental model

An alpha = `f(data) → vector of positions`, where the vector is proportional to dollars held per instrument. Building one is a loop, not a line:

> **idea → expression → simulate → read metrics → refine → repeat → submit**

(Ch. 5, Figure 5.5 = "five steps to creating alphas": analyze data → form price-response idea → write expression → test → submit if favorable.)

---

## The four design decisions (Ch. 4)

| Decision | Options | Notes |
|---|---|---|
| **Data input** | price/volume, fundamentals, macro, text, multimedia; plus *risk models* & *relationship models* (used to reduce noise, not generate direction) | edge = better data OR better processing of it |
| **Universe** | asset class / region / country / sector / individual instruments | usually driven by data coverage or idea; can tune per-universe |
| **Prediction frequency** | tick → intraday → daily (delay-1, delay-0 snapshot, MOO/MOC) → weekly/monthly | usually driven by input-data frequency |
| **Horizon** | how far ahead you predict | drives turnover (see Part II-B) |

**Delay-1** = only data available *before* today's trading may be used. This is the safe default; delay-0 needs careful timestamping.

---

## The refine loop in action (Ch. 5 case study — the template to imitate)

Starting alpha: 5-day mean reversion on TOP3000 US. Each step is a single, *motivated* change measured against the prior version:

| Version | Change made | Why | Result (IR / drawdown) |
|---|---|---|---|
| Alpha1 | raw 5-day reversion (formula below) | reversion hypothesis | IR ~1.0, **drawdown 39%** |
| Alpha2 | **industry + market neutralize** | remove biggest equity risks | IR 1.37, **drawdown <9%** |
| Alpha3 | **cross-sectional rank** | relative size more accurate than raw magnitude | IR 1.76 |
| New_alpha | **decay (3-day smoothing)** | cut turnover, stabilize | IR 1.82, lower turnover |

**The actual expressions (each step is a transform of the previous):**

```
Alpha1     = -( close(today) - close(5_days_ago) ) / close(5_days_ago)
             # = -(1-week return). Negative sign → short the risers, long the fallers.

Alpha2     : neutralize so that  Σ(Alpha1 values within same industry) = 0
             # long–short balanced inside each industry

Alpha3     = rank(Alpha1)        # cross-sectional rank, rescaled to [0,1]
             # then re-impose  Σ(Alpha3 within same industry) = 0

New_alpha  = new_alpha + weighted_old_alpha     # decay / smoothing
             # = moving average of the signal over a window (here 3 days)
```

A standalone alpha maps to positions by: **prediction strength = dollar position** (vector ∝ money held per instrument). In the worked example, Alpha values {2, −1} → long $1M GOOG, short $0.5M AAPL on $1M capital.

**Lesson:** improve one lever at a time, each with a reason, and re-read the full metrics table after each — a change that lifts IR but wrecks turnover or margin is not an improvement.

---

## Evaluating a standalone alpha (Ch. 4)

You usually don't know the final strategy, so map predictions → positions (prediction strength = dollar position), simulate with *reduced* transaction costs, and read:

**Metric definitions (from the Ch. 5 case study):**

```
Ann_return       = ann_pnl / (booksize / 2)          # booksize/2 = one side of the long–short book
Information_ratio = mean(daily return) / std(daily return) × √256   # 256 ≈ trading days/yr → annualized
Daily_turnover    = (avg value traded each day) / booksize
Margin (Profit per $ traded) = pnl / total_traded_dollar
Max drawdown      = largest peak-to-trough PnL drop, as % of (booksize / 2)
```

- **Information Ratio (IR)** = mean(returns) / std(returns), annualized by ×√256. Consistency of prediction. *~1.0 for a unique, lightly-fitted alpha over 5 years* is reasonable; real ones run a bit higher due to fitting/correlation.
- **Margin** = PnL / $ traded. Cost-sensitivity. *~5 bps acceptable* for an average daily alpha. Low margin only OK if the alpha is very different from the pool.
- **Correlation** to most-correlated existing alpha:
  - `>0.7` too high (unless much better than the existing one)
  - `0.5–0.7` borderline (must excel elsewhere)
  - `0.3–0.5` acceptable
  - `<0.3` good
- Optional: check IR separately on **liquid vs illiquid** stocks. If only predictive on illiquid names, limited use at scale.

---

## Data: find it, validate it, understand it (Ch. 6)

**Where data comes from:** academic literature (search "stock returns" / "abnormal returns"), vendors (raw → parsed → NLP-processed → full alpha models). *The less well-known the data, the more valuable.* Avoid vendor-sold alpha *models* — likely overfit and overcrowded; if used, test OOS hard and use in nontrivial ways.

**Validation checklist (do BEFORE testing signals):**
- [ ] Every datum has a **timestamp** — no timestamp = unusable.
- [ ] Know the **delivery timeline** (occurrence vs arrival). Using data before it was available = **forward-looking bias** (looks amazing in sim, impossible live).
- [ ] Data will keep being produced on a **reliable schedule** (no dead feeds).
- [ ] Check **survivorship bias** — vendor may have tried 1,000 models and shown you the 1 survivor.
- [ ] **Sanity-check / clamp outliers** in the alpha code — one bad point can kill a signal or cause real losses live.
- [ ] For complex data (e.g. fundamentals), **understand it** (corporate finance) before crunching.

---

## Quick build checklist

- [ ] State the hypothesis in one sentence (what change in data → what price response).
- [ ] Pick universe + frequency from data coverage.
- [ ] Write the simplest expression that encodes it.
- [ ] Simulate; record IR, return, drawdown, turnover, margin.
- [ ] Refine one motivated lever at a time (neutralize → rank → decay …).
- [ ] Watch in-sample vs out-of-sample gap — at *your* level, not just per-alpha (it measures your tendency to overfit).
- [ ] Check correlation to the existing pool before declaring it valuable.
