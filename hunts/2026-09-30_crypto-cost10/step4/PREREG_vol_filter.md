# PRE-REGISTRATION — H7 volatility filter (Step 4, one lever) — written 2026-10-04, BEFORE any filtered result

User decisions 2026-10-04: open VAL ONCE for this test (1a); pass condition (2a) below.

## Origin (why this lever)
Cell 6 (TRAIN, many looks): H7 earns in WILD regimes (BTC 30d vol above its past median) and loses in CALM ones —
IR +2.1 / +2.2 vs −1.0 / −1.8; per-trade gross wild +192 / +152 bp vs calm −148 / −1 bp; wild > calm in 10/10 coins
(Cell 7). Mechanism offered: in high-volatility markets forced selling overshoots and liquidity providers are paid to
absorb it; a crash in a calm market is more often information. This is a TRAIN finding, so TRAIN results of the filtered
rule are in-sample by construction and are NOT evidence.

## The rule (no free parameters chosen after this point)
At each H7 entry (00:00 UTC, k = 0): compute BTC's 30-day volatility = std of the last 30 daily log returns of BTC
(00:00 UTC closes, validated panel) × sqrt(365). The cut-off = the median of that volatility over all PRIOR days
(expanding, minimum 90 days, today excluded). **H7 enters only if today's BTC 30-day volatility > the cut-off.**
Otherwise it holds nothing that day. Everything else is H7 unchanged: trigger = coin's day return below its trailing
365-day 10th percentile (min 180 days), equal weight across triggered coins, G = 1.0, 24 h hold.
Identical to the Cell 6 "wild" bucket definition. Not tuned: 30 days, median and 90-day minimum are Cell 6's original choices.

## Data and costs
- Prices: the validated stitched set (p15). VAL = 2023-03-25 00:00 → 2023-11-30 23:00 UTC (the cloud session's split).
  Signal history before VAL (TRAIN) is used for thresholds - it was knowable at the time.
- Costs: commission 3.25 bp/side; FTMO swap nightly (Fri ×3); spread = FTMO quote in force at the trade minute for the
  7 tick coins (pulled for VAL in this step); BNB, SOL = the TRAIN stand-in (median of 7 coins by hour). BCH has no
  validated prices after 2021 (no VAL trades).
- Known caveat written in advance: BNB/SOL Binance prices in VAL (Apr–Nov 2023) are inside a year that passed check A
  on Jan–Mar samples only.

## PASS CONDITION (fixed now)
Primary cell: **filtered H7, k = 0, LOW cost, all 10 coins, on VAL.** Unit = one position (coin, entry day).
- **INCONCLUSIVE** if fewer than 30 positions on VAL.
- otherwise **PASS** if mean GROSS per position > 0 AND mean NET (LOW) per position > 0; else **FAIL**.
Reported alongside, NOT gates: unfiltered H7 on VAL; HIGH cost; measured-7 universe; k = 1; TRAIN in-sample numbers.

## Known risks recorded before the test
- Concentration FLAG (Cell 7): best 10% of trades = 154% of gross; deepest fifth of crashes = 54% of gross. A short VAL
  window may contain no large crash at all.
- 2023 was mostly a calm year for BTC: the filter may fire rarely → INCONCLUSIVE is a likely outcome.
- K: this is one more look; VAL has been opened once before by the EDA routine for a different idea (H5).

---
## OUTCOME (appended after the run, 2026-10-04 — the text above is unchanged)
Primary cell (filtered H7, k=0, LOW, all 10, VAL 2023-03-25 → 2023-11-30): **3 positions → INCONCLUSIVE** (gross −42.9,
net −95.6 bp/position). The filter was ON on only **6% of VAL days** (50% of TRAIN days) — 2023 was calm, as feared.
Reported alongside (not gates): unfiltered H7 on VAL, all 10, k=0: 147 positions, gross +52.5 bp (t 1.9), net LOW +10.0 bp
per position, but day-weighted Sharpe −1.03 and −24% total. TRAIN filtered (in-sample, not evidence): Sharpe 1.22,
maxDD −36%, 630 positions, gross +197 bp (t 6.6). Truncation test of the filtered strategy: 0/193. VAL is now SPENT for
this lever. Engine: cell_08_volfilter_val.py, cell_08_volfilter_val.csv, cell_08_prereg_result.csv.
