# Step 2 — express it simply (EDA#2, 2026-09-30)

Both ideas, as the simplest formulas that encode the Step 1 sentences (RULES.md in step1b). Raw versions only. Neutralisation
variants are listed for Step 4 (lever 1), not used in Step 3.

Notation: `r[i,d]` = log return of coin i over UTC day d (close of the 23:00 bar of day d-1 → close of the 23:00 bar of day d),
from Binance spot 1h trade prints, defined only for complete consecutive days. `q(x, p, L)` = the p-quantile of x over the L
days strictly before d (point-in-time). `live(d)` = coins with a complete day d.

## H7 — crash-day rebound (long only)
```
signal[i,d] = 1  if  r[i,d] < q(r[i,·], 0.10, 365)        (needs ≥ 180 prior days)
w[i,d]      = G · signal[i,d] / max(1, Σ_j signal[j,d])    (equal weight across today's triggers, total gross G)
hold        : enter at 00:00 UTC of day d+1 (= close of day d), exit 24h later (00:00 UTC of day d+2)
```
Parameters: **3** (lookback 365, quantile 0.10, hold 24h) + the sizing constant G (not a signal parameter). The minimum history
of 180 is a data-availability guard, not tuned.

## H2 — volume-shock next-day reversal
```
shock[d]  = mean_{i ∈ live(d)} log( V[i,d] / median(V[i,d-30..d-1]) )      V = daily quote volume (USDT)
high[d]   = shock[d] > q(shock, 0.67, all days before d)                   (needs ≥ 90 prior days)
w[i,d]    = G · high[d] · (−sign(r[i,d])) / |live(d)|
hold      : enter at 00:00 UTC of day d+1, exit 24h later
```
Parameters: **3** (volume window 30, shock quantile 0.67, hold 24h) + G. Net exposure = G·(#down − #up)/N, so it is only roughly
market-neutral; the demeaned form (Step 4) makes it exactly dollar-neutral.

## Units check
| quantity | unit | check |
|---|---|---|
| r[i,d], thresholds q(r) | log return (dimensionless) | a return is compared with a quantile of the same coin's returns ✔ |
| V, median(V) | USDT per day | ratio → dimensionless; log of a ratio ✔ |
| shock, q(shock) | dimensionless | compared like with like ✔ |
| w[i,d] | fraction of equity (notional / equity) | Σ\|w\| = G by construction (H7); ≤ G (H2) ✔ |
| P&L[d+1] | fraction of equity | Σ_i w[i,d] · (exp(r[i,d+1]) − 1) ✔ |
| cost per position | bp of notional | (coin round trip + 8.2 swap) × \|w\| ✔ (one rollover per 24h hold) |

## Order and fill timing
- The signal is known at 00:00:00 UTC (the 23:00 bar closes). **Zero-lag fill = that bar's close**: the Step 1b ceiling.
- Step 3 fills at the close of the bar k hours later, k ∈ {0, 1, 2, 4}, and exits exactly 24h after entry. The FTMO rollover
  (21:00/22:00 UTC by DST) falls inside every 24h hold → one swap charge per position.
- No overlap: a coin that re-triggers while held is not doubled; the position is extended from the new entry.

## Neutralisation variants (Step 4, lever 1)
| id | applies to | hedge | extra cost per event |
|---|---|---|---|
| N-a | H7 | short equal notional of BTCUSD | BTC 6.6 + 8.2 swap ≈ 14.8 bp |
| N-b | H7 | short β̂·notional BTCUSD, β̂ = trailing-90d beta of coin i on BTC (point-in-time) | ≈ β̂ × 14.8 bp |
| N-c | H7 | short equal-weight basket of the other live coins | basket mean (≈ 20 + 8.2 bp) |
| N-d | H2 | cross-sectional demean: w[i,d] ∝ −(r[i,d] − mean_j r[j,d]) sign, dollar-neutral | none extra (both legs already priced) |
