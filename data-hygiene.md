# Data Hygiene — feeding price to a backtest

The layer *beneath* alpha research: rules for what a "price" column may be before any signal is
computed on it. Written after the #016 postmortem (alpha log 2026-07-15: a bid-only price file
manufactured a Sharpe-5 phantom that passed every statistical gate and died live). Sources:
Roll (1984), Keim (1989), Easley–O'Hara PIN, López de Prado *AFML* ch. 2 & 19 ([[part-3f-microstructure-intraday]]
has the book-side PIN notes). Enforced in code by `backtest_engine2/data_hygiene.py` and PROTOCOL §6.

---

## The identity everything follows from

Every recorded price is the truth plus a contamination term:

```
observed price  =  true mid  +  (half-spread × side)         p = m + c·b,  b ∈ {−1,+1}
```

A backtest computes returns on `p` but you trade against `m ± c`. Whenever `c` (the spread) or `b`
(which side got recorded) moves **systematically**, the difference stops being noise and becomes a
fake signal. Two canonical failure modes:

- **Random `b` (trades ping-pong bid/ask)** → fake mean-reversion. Roll 1984: strong enough that the
  spread can be *estimated* from it: `c = √(−cov(Δp_t, Δp_{t−1}))`. Any short-horizon reversion edge
  found on raw prices is guilty until proven innocent.
- **Scheduled `c` (spread widens on a clock — rollover, open, close, fix)** → fake time-of-day drift.
  Keim 1989 (January effect partly bid→ask hops at year-end) and our #016 (hour-21 "fall" = spread
  ballooning into the 22:00 rollover, recorded on bids). Passes OOS, Bonferroni, cross-instrument and
  per-year checks, because it IS a stable property of the data — of the wrong variable.

Why `c` moves on a clock is theory, not accident (PIN): the spread is the market maker's premium for
adverse selection; when noise-trader flow dies (rollover, dead hours), the premium balloons. Every
night, on schedule.

---

## The four things a "price" can be

Before the first backtest on ANY new data file, write one sentence in the log:
*"these prices are [type] from [venue], timestamped [when], knowable at [when]."* Can't fill it in →
not ready to compute a return.

| type | what it is | bias | fit for |
|---|---|---|---|
| **trade print** | actual transaction (equity closes = auction prints) | bounces between bid/ask at fine scales (Roll) | daily equity work; intraday with bounce awareness |
| **one-sided quote** | bid OR ask | truth ∓ half-spread; deadly when spread moves on your clock | costs/execution only — never signal returns |
| **mid** | (bid+ask)/2 | hides what you'd actually pay | signal research (with spread charged separately) |
| **indicative/composite** | vendor blend, construction opaque (e.g. Yahoo FX) | unauditable | nothing spread-sensitive |

---

## Trap catalogue additions (dated)

- **Vendor-synthetic OPENS (2026-07-17, caught by overnight_rf Cell-1 base-rate tripwire):** index-level
  daily "opens" are often stale copies of the prior close (Yahoo ^GSPC: 78-98% of days pre-2006, ~25%
  into 2013) → any prevClose→open quantity (overnight returns, gaps) reads as EXACTLY 0 on those days —
  fiction that dilutes means, hides drawdowns, and survives every statistical test. **Detection = the
  ZERO-GAP RATE by year (mandatory for any new OHLC source): real trading produces open == prevClose
  almost never (<~2%; SPY's eighth-tick 90s ≈ 1.9%).** Prefer traded-instrument prints (ETF) over index
  levels for open-dependent work.
- **Conditioning look-ahead (2026-07-17, VIX-gate postmortem):** a regime variable stamped the same day
  as the outcome CONTAINS the outcome (exit-day VIX includes the night's own panic). Every conditioning
  /gating variable must be lagged to its entry-knowable value before any table is drawn — descriptive
  anatomy on contemporaneous stamps is not evidence.

## Standing rules

1. **Pull BOTH sides, always** (Dukascopy serves BID and ASK candle feeds — request both; the #016
   pullers hardcoded BID). Signals on **mid**; spread charged **separately** as a time-varying cost.
2. **The tripwire is mandatory:** every backtest/execution table carries a *GROSS mid-to-mid,
   zero-cost* row. Strategy prints money while that row reads ~0 → the "edge" is quote mechanics.
   (This row is what caught #016.)
3. **Clock-anchored signals are maximum-risk** (time-of-day, fixes, opens/closes, month-end): quote
   dynamics live on the same clock as the signal, so nothing averages out. Two-sided data is
   non-negotiable and spread must be modeled **at the trade minute**, never as a daily median.
4. **Point-in-time or it didn't happen** (AFML ch. 2): fundamentals are stamped before they were
   public (Bloomberg ~1.5mo), vendors backfill corrections. For every column: when was it knowable?
5. **Unknown/one-sided series → run the Roll check** (`data_hygiene.roll_effective_spread`) to size
   the embedded spread before trusting fine-scale patterns; Corwin–Schultz (AFML 19.3.4) estimates
   spread from high/low when no quotes exist.
6. **No free lunch posting limit orders:** the spread is the adverse-selection premium (PIN). Resting
   orders at illiquid/flare moments get filled by informed flow and missed by the drift you wanted
   (#016i: 32-58% fills, worse than paying up). Earning the spread requires the fill NOT being
   conditioned against you — verify with an intrabar fill sim before believing it.
7. **Time bars have a cost** (AFML ch. 2): they oversample dead hours, undersample busy ones, and sync
   your sampling with the dealer's quote schedule. Right tool for clock-flow signals; for statistical/
   ML features prefer activity-based sampling where volume data exists.

---

## Checklist (run at data-onboarding, before the first signal)

- [ ] One-sentence provenance line written in the log (type / venue / timestamp / knowability)
- [ ] Both quote sides on disk (or trade prints), mid constructed, spread series kept
- [ ] Spread-by-time-of-day profile plotted once — know where YOUR data's `c` moves on a clock
- [ ] Roll estimate on any series whose construction is uncertain
- [ ] PIT audit for anything fundamental/vendor-processed
- [ ] Backtest template includes the gross mid-to-mid tripwire row
