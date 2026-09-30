# Step 1b close-out — pre-committed rules (written 2026-09-30, BEFORE any code for this step)

Ideas: H2, H7 and H6 from eda-routine run `2026-09-30_crypto-panel-1h`. The user chose: years 2018 → 2023-03-19 (TRAIN only;
VAL not reopened); H7 measured despite survivorship, with a flag; all three ideas go through.

## Step 1 test form (claim + economic reason)
- **H2** — a panel-wide volume shock on day d predicts next-day (d+1) reversal of each coin's day-d move, because liquidity
  providers who absorb forced flow on shock days are paid back as the flow subsides (Lehmann 1990; Nagel 2012).
- **H7** — an extreme down day for a coin predicts a positive next-day return, because liquidation cascades overshoot fair
  value and the forced sellers are gone the next day.
- **H6** — when trailing 7-day panel volatility is high, a coin's 6h block return predicts reversal in the next 6h block,
  because the liquidity-provision premium widens when volatility is high ("evaporating liquidity", Nagel 2012).

## Tradeable measurement (bp of notional, gross, per coin-event)
Returns are Binance spot 1h closes aggregated to UTC days / 6h blocks (00/06/12/18). Only consecutive, complete periods are
used (no return across a gap). Everything that selects an event is point-in-time:
- **H2** — shock_d = mean over live coins of log(vol_d / median(vol over d-30..d-1)). A day is HIGH if shock_d > the
  expanding 67th percentile of shock over days < d (min 90 days of history). Event on HIGH days: `-sign(r_d) * r_{d+1}`, every
  live coin.
- **H7** — event when r_d < the coin's own trailing 365-day 10th percentile of daily returns (days < d, min 180). Event
  return: r_{d+1} (long next day).
- **H6** — a day is HIGH-VOL if the equal-weight panel's trailing 168h realised variance at 00:00 UTC > the expanding 67th
  percentile over days < d (min 90). Event, for each coin block b on a HIGH-VOL day (b's successor may be the next day's
  first block): `-sign(r_b) * r_{b+1}`.

## Cost per event (FTMO, the x098 menu)
coin round trip (ftmo_spread_rt_bp + 6.5 commission) + swap: 8.2 bp for a daily hold (crosses one rollover); for a 6h hold,
8.2 × 1/4 = 2.05 bp on average (one block in four crosses the rollover). net = gross − cost, per event, per coin.

## Gate 1: cost (pooled over TRAIN, all coins)
edge/cost = mean gross / mean cost over the idea's events.
- **PASS** if edge/cost ≥ 1.0 AND mean net t-stat > 0 (day-clustered SE).
- **MARGINAL** (carry to Step 2 with a flag) if 0.5 ≤ edge/cost < 1.0.
- **REJECT** if edge/cost < 0.5.

## Gate 2: decay-first (by calendar year, GROSS mean, only years with ≥ 20 events; 2023 = Jan 1 → Mar 19)
Computed on the yearly gross means, in this order:
- **ALTERNATING** if the sign changes ≥ 3 times across the years in order → REJECT.
- **DECAY** if Spearman(year, effect) ≤ −0.7 AND the last full year (2022) effect ≤ 0 → REJECT.
- **STRONGEST-RECENT** if the largest yearly effect is in 2021, 2022 or 2023 AND 2022 > 0 → survives.
- **FLAT** otherwise → survives.

## Outcome
An idea goes to Step 2 only if Gate 1 is PASS or MARGINAL AND Gate 2 survives. Anything else is a light sub-entry in
alpha_log #049, as a finding, not a verdict.

K: this step adds 3 looks (one per idea) on TRAIN, which the EDA already looked at (EDA K = 18). A 1b pass here is
**not** fresh evidence — it is a cost/decay screen on already-seen data.
