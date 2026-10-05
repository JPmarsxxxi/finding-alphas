# SESSION NOTES — cloud session 2026-09-30 → 2026-10-02 (crypto-cost10 hunt → EDA#2)

Handover for continuing on the local machine. All three repos are on branch **`claude/crypto-data-availability-cltiy2`**
(pushed). Pull that branch locally in each repo before continuing.

| repo | what this session added |
|---|---|
| finding-alphas | `hunts/2026-09-30_crypto-cost10/` (all data, pull scripts, docs, Step 1b, Step 2); `alpha_log.md` EDA#2 entry |
| eda-routine | `data/crypto_panel_2026-09-30/` (force-added, clean-room bundle); run `runs/2026-09-30_crypto-panel-1h/`; `TARGET.md`, `MODES.md` |
| backtest_engine | `backtest_engine2/notebooks/eda02_crypto_reversal/` (Cells 1–3) |

---

## 1. What was done, in order

1. **Step 0 — hunting ground.** FTMO crypto cost menu (x098) ranked: BTC/BNB cheapest, then ETH/SOL; swap −30%/yr both
   sides on all ten → intraday-only economics.
2. **Data pull (231 series, everything reachable from the cloud).** Scripts `pull/p1..p8`. Families: spot (Binance 10 coins
   1h, Bitstamp BTC 2011→, Coinbase, Upbit KRW), perps (Binance klines/premium/funding/5m metrics, BVOL), derivs (Deribit
   DVOL/funding, Hyperliquid funding), on-chain (CoinMetrics community, mempool.space, blockchain.com), DeFi (DefiLlama),
   attention (F&G, GDELT, HN, SEC full-text, geomagnetic Kp), macro (47 Yahoo tickers, UST curve, NY Fed, TGA, auctions,
   CFTC TFF, FOMC dates, BIS/ECB). Catalog: `CATALOG.md`, `coverage.png`; mechanisms: `MECHANISMS.md` (29 claims).
   Failed/blocked: Wikipedia pageviews (403 bot policy), BIS JP, one GDELT query; blocked hosts listed in MECHANISMS.md.
3. **Seal handling.** Every series split at 2023-11-30: explore rows in `data/<family>/`, later rows in `data/_sealed/`
   (TEST + SEALED). The sealed side was pulled but **never opened**. ⚠️ The registry (`data/registry.jsonl`) records row counts
   and last dates of the sealed side — bookkeeping only, but tell me if you count that as a touch. **Seal decision still yours.**
4. **EDA hand-off (clean room).** A separate agent installed an explore-only, idea-free bundle into eda-routine (224 files,
   cut at 2023-11-30, verified per file). No mechanisms, scripts or finding-alphas results went across.
5. **EDA routine v3 run** (separate agent, mode E): `eda-routine/runs/2026-09-30_crypto-panel-1h/REPORT.md`. gate.py PASS,
   eda-v3-judge PASS. Stop S2. ⚠️ It opened VAL once for H5 under the runbook's instruction — see HOLDOUT_RULES rule 3 question.
6. **Step 1b close-out** (`step1b/`, rules written first): cost gate + decay-first on H2/H7/H6, years 2018→2023-03-19.
   | idea | gross bp/event | edge/cost | decay-first | result |
   |---|---|---|---|---|
   | H7 crash-day rebound (long) | +105.5 (t 2.33) | 4.06 | STRONGEST-RECENT | → Step 2 |
   | H2 volume-shock next-day reversal | +35.7 (t 2.28) | 1.35 (net t 0.85) | FLAT | → Step 2 |
   | H6 6h reversal in high vol | +6.3 | 0.31 | ALTERNATING | rejected |
   H5, H3, H1, H4 logged as light sub-entries (died at the EDA's cost line). Arc renamed **EDA#2** (user rule: EDA-pipeline
   signals get `EDA#n`; #049 left unused).
7. **Step 2** (`step2/EXPRESSIONS.md`): both ideas as 3-parameter formulas, units checked, fill timing, neutral variants
   (N-a..N-d) parked for Step 4.
8. **Step 3, engine notebook (PROTOCOL cell by cell)** — `backtest_engine2/notebooks/eda02_crypto_reversal/`:
   - **Cell 1** data panel: bars re-stamped to CLOSE time (no look-ahead), gaps never filled, TRAIN only. ✔
   - **Cell 2** strategies `CrashRebound`/`VolShockReversal`; truncation look-ahead test 0/568 mismatches. ✔
   - **Cell 3** costs — **REVISED, not final** (see §3). Current: spread = max(FTMO x098 half, MEASURED Binance half by
     hour-of-day from Tardis first-of-month quotes), LOW = median / HIGH = p90; commission 3.25 bp/side; swap charged once a
     night at 17:00 New York, Friday ×3, weekend 0. Truncation test 0/120. OHLC estimators (EDGE, Abdi-Ranaldo) were tried
     and REJECTED (BTC read 3–57 bp vs 0.09 bp measured).
   - **Cell 4** (raw backtest) — announced, NOT written.

## 2. Mistakes made and corrected this session (so they are not repeated)
- I read `data-hygiene.md` before the big fetch but did not follow rule 1 (pull both sides) or flag rule 3 (clock-anchored
  signals need two-sided data, spread at the trade minute). Corrected partly with Tardis quotes; the full fix is §3.
- Step 1b first run included 2017 against the rule → fixed to 2018+ (it changed H2 from ALTERNATING to FLAT; both shown).
- Cell 3 first used a constant spread without asking (skills/04-costs §4b mandatory decision) → corrected.
- I presented "FTMO BTC spread = fixed $1" (from alpha_log line 630) and extrapolated it to 2019 as if verified. It is NOT
  verified here (source data is local only), and a third-party page claims $10–12. FTMO changed its crypto pricing on
  **2025-07-28** (commission 0.0325%/side + "tighter, market-aligned spreads"). Treat the $1 as unverified.

## 3. Open decisions / next steps (pick up here)
1. **Bid/ask source for mid prices (data-hygiene rules 1–3, user: "follow it to the t").** Options found:
   - **Dukascopy** 1-min BID+ASK (your `x030_pull_1min_ohlc.py` pattern): BTC 2017→, ETH 2018→, LTC/XRP/BCH 2019→,
     ADA 2022→; **no SOL, DOGE, DOT, BNB** under any name tried. Weekends must be included for crypto; rate-limit backoff.
   - **FTMO via MT5** (local only): check depth first — script not yet written: earliest H1/M1/tick per coin, then pull H1
     bars WITH the `spread` column to 2026-04-30 (FTMO sealed from 2026-05-01; server clock = NY+7h).
   - Tardis paid (all coins, all days) — not done.
   - Pending choice for SOL/DOGE/DOT/BNB: (a) drop from the main backtest [recommended], (b) keep on trade prints flagged,
     (c) paid data.
2. **Cell 3 edit**: spread at the exact trade minute (k:00), not the hourly median (hygiene rule 3). Then Cell 3b: trade
   print vs real mid at those minutes (feeds the tripwire), then **Cell 4** on mids with the GROSS mid-to-mid tripwire row.
3. **Cell 4 agreed settings**: entry lag k ∈ {0,1,2,4} h, LOW/HIGH/zero cost, G = 1.0, `ann_factor=8760`, 2018-01-01 →
   2023-03-19 (VAL not opened), count positions closed by a missing price, yearly tables.
4. **H7 open risks to carry**: entry lag (#048 lost half its edge to one bar), bull-year dependence (2020–21), survivorship
   (today's FTMO list), crash-day FTMO spread widening unmeasured (MT5 real-tick tester could measure it later).
5. **Seal**: pulled data after 2023-11-30 sits in `data/_sealed/` unopened. HOLDOUT_RULES rule 3 wording: decide whether
   "held-out window" includes VAL (the EDA run treated VAL as runbook-authorised).
6. **Later**: MT5 Strategy Tester ("every tick based on real ticks") as the final FTMO execution check if H7 survives
   Steps 3–5; must stop at 2026-04-30.

## 4. Where the data is (all committed)
- finding-alphas `hunts/2026-09-30_crypto-cost10/data/` — 916 parquet files, ~527 MB, **all tracked in git** (explore side,
  `_sealed/`, and `quotes_minute/` raw Tardis day files + combined `quotes/`). Registry: `data/registry.jsonl`.
- eda-routine `data/crypto_panel_2026-09-30/` — 224 files force-added (the repo normally ships data as a Release asset).
- backtest_engine `backtest_engine2/data/eda02_crypto/` — **gitignored** copies (10 spot files + 10 quote files). Re-create
  locally by copying from the finding-alphas hunt folder (`data/spot/binance_*.parquet`, `data/quotes/*`).
- Cloud-only, not committed: eda-routine `.venv/` (recreate from TARGET.md's pre-approved installs).

---

# LOCAL SESSION 2026-10-02 → 2026-10-04 — data sourcing for EDA#2 (FINDINGS, not verdicts)

Worktrees (main folders untouched): `finding-alphas_wt_eda02`, `backtest_engine_wt_eda02`, `eda-routine_wt_eda02`,
all on `claude/crypto-data-availability-cltiy2`. Engine Cells 1–2 re-run locally: truncation test 0/568 ✔.

## 5. What was measured (scripts in `pull/`, outputs in this folder)
| script | what | key result |
|---|---|---|
| p9 `mt5_depth.csv` | FTMO MT5 history depth | server clock UTC+3 now (= NY+7h, verified); terminal maxbars 100k |
| p10 `data/ftmo/` | FTMO H1 bars, all 10 coins, full span, split at 2023-11-30 | clock verified vs Binance (best shift 0, every year); BTC H1 from 2011 but 2011–16 = 1 bar/day; weekends missing until 2021; spread recorded as 0 on many 2017–21 hours (BTC 2019: 72%); SOL has NO explore-side FTMO data |
| p11 `ftmo_h1_verification*.csv` | FTMO H1 vs FTMO ticks, 2022-02..2023-11 | bars are BID; bar spread = hour's MINIMUM spread; built mid error median 0 bp (BTC/ETH), p90 0.6–5.5 bp; **DOT spread stored 10× too small** |
| p12 `coverage_two_sided.csv` | free two-sided coverage | FTMO ticks from 2022-02 (BNB/BCH/SOL 2025-05); Binance futures bookTicker only 2023-05..2024-03; Dukascopy rate-limited us once (block lifted next day) |
| p13 `bitmex_vs_spot.csv` | BitMEX quotes (free, 2014-11→) vs spot, 104 sample days | perpetuals match spot from ~2018–22 (corr 0.99+, gap 2–15 bp); quarterly futures 2014–17 sit 1–4% off spot → not usable as spot mids |
| p14 `price_vs_mid.csv` | Step P1: last-trade closes vs real mids | A (Binance vs own mid, 2019–23): mostly ✅, 1–2 bp; B (vs FTMO 2022–23): ✅ except BCH; C (vs BitMEX perp) and D (vs BTC-e 2015–16, Harvard Dataverse CC0) fail — venue differences, cannot isolate trade-vs-mid error |
| p15 `data/validated/` | Step P2: validated stitched set | see §6 |

Research (no data bought): vendors with bid/ask history — CoinAPI (claims quotes from 2014-02, $1/GB, $25 credit,
card required), Amberdata (claims Bitstamp 2014 / Coinbase 2014-12 order books, free trial key on request), Kaiko
(2015+, ~$9.5k+/yr), Tardis (2019+, $450+/mo), CCData (2020+), Coin Metrics (2019+). yfinance/TradingView: no bid/ask.
Nobody has bid/ask before 2014-02 → BTC cannot reach 80% of its life on two-sided data from any source.

## 6. Data decisions taken by the user (2026-10-04)
1. **Validated data only** ("I don't want garbage data"). The 80%-of-life target is NOT met for most coins; the user
   chose validated-only over coverage.
2. Pass rule for "trade price ≈ mid" = **tight (b)**: same venue |gap| ≤ 2.5 bp; cross venue ≤ 10 bp after removing the
   yearly offset; daily-return difference ≤ 5 bp.
3. Stitch: **Binance last-trade (validated years) up to 2021-12-31, FTMO hourly mid from 2022-01-01** for BTC ETH XRP
   LTC ADA DOGE DOT. **BNB, BCH stay on Binance** (FTMO's BNB/BCH unverified — ticks only from 2025 — and track Binance
   at only 0.60–0.78). SOL = Binance only.
4. **Failed years are cut**, never patched: ADA 2019, DOGE 2019–20, SOL 2020, BCH 2022–23 (BCH ends 2021). LTC/DOT
   2022 failed check A but are covered by FTMO.
5. **DOT FTMO spread × 10** (checked vs ticks: ratio exactly 10.0 every month; mid error −16 → 0.0 bp). Raw file NOT
   modified; sealed-side DOT file needs the same fix when the seal is opened.
6. Bars after a source switch or a gap carry `new_source=True` — never take a return across them. Binance↔FTMO
   offset at the 2022 switch: 0.4–3 bp median.

## 7. Open — pick up here
1. **Cell 1** → point at `data/validated/` (copy into the engine worktree; data dir is gitignored).
2. **Cell 3 costs, 2019–21:** those hours have no FTMO spread you can trust. Decision needed: which FTMO spread to
   charge (e.g. FTMO 2022–23 measured spread by coin × hour-of-day, applied backwards — note FTMO repriced crypto on
   2025-07-28).
3. Spread at the TRADE MINUTE (hygiene rule 3) is still owed from the cloud session's list.
4. Not yet done: 4 BitMEX sample days (2023-08..11) and 5 BTC-e months failed to download (network) — not needed for the
   validated set.

---

## 8. Engine notebook on the validated set (2026-10-04) — FINDINGS, not verdicts
Engine worktree `backtest_engine_wt_eda02/backtest_engine2/notebooks/eda02_crypto_reversal/`, TRAIN only (2019-01-01 →
2023-03-19; VAL 2023-03-25..11-30 and SEALED 2023-12 → not loaded). Nothing committed.

**Cell 1** — validated prices; last bar before each Binance→FTMO switch dropped (no cross-source return). **Rule (b)
(user):** a day still counts if its only missing hours are FTMO's fixed Saturday windows (bars closing 06–11 and 18:00
New York; measured over 100 Saturdays) — Sat/Sun complete days for FTMO coins 0% → 83–84%; Binance coins unchanged.
Volume (H2 input) = raw Binance for every hour. Cell 2 truncation test 0 mismatches (re-run after each change).
**Cell 3** — spread = FTMO quote IN FORCE at the trade minute (p16: 7 coins × 1,648 trade minutes, 2022-02 → TRAIN end;
quote age 0.3–4 s). 2022+: measured at t. 2019–21: coin × hour median (LOW) / p90 (HIGH) applied backwards [assumption].
BNB, SOL = stand-in (median of the 7 tick coins; BNB bar spread read 0.17 bp = likely scale error; SOL only had a 2026
new-pricing snapshot). BCH = FTMO bars, unverified. Commission 3.25 bp/side kept on top of old-regime spreads
(conservative). RT 24h LOW: BTC 18.9, ETH 25.4, LTC 36.5, ADA/DOGE/DOT/BNB/SOL ~45–47, XRP 68.6, BCH 65.5 bp.
**Cell 4** — 48 runs (H7/H2 × k∈{0,1,2,4} × ZERO/LOW/HIGH × all10/measured7); full metrics in cell_04_metrics_full.csv.
- Tripwire (gross per trade at our prices, k=0): **H7 +116.8 bp (t 5.0, n 963); H2 +30.8 bp (t 2.5)** — not quote mechanics.
- H7 k=0 LOW: Sharpe 0.55 (all10) / 0.67 (measured7), 95% CI includes 0, PSR 0.87/0.92, maxDD −65%, underwater ~85% of
  the time, beta to BTC 0.34. Sharpe falls with entry delay: k=0 0.55 → k=1 0.45 → k=2 0.34 → k=4 0.04.
- H2: gross real but costs take it all — net Sharpe −0.03 to −0.35 in every cell; BCH (unverified cost) carries its gross.
**Cell 5** — H7 IR (Finding Alphas, daily) 0.029 / 0.036; in a position 18% of days; +57 bp per active day, 60% hit; 55%
positive months; rolling 6-month IR > 0 in 58% of windows (range −2.9 … +3.9). **Cross-sectional IC ≈ 0** (+0.010, t 0.8)
→ H7's edge is TIMING (being long after crash days), not coin selection.
**Cell 6** — regimes at the START of each day (past-only): **wild (BTC 30d vol > its past median) vs calm decides it, not
bull/bear.** IR: BEAR-wild +2.11, BULL-wild +2.15, BULL-calm −0.95, BEAR-calm −1.84. Per trade gross: wild +192/+152 bp
(t 4.5/3.8), calm −148/−1 bp. k-means cross-check agrees. Deep drawdowns (−59% 2019-07→2020-11; −60% 2021-07→ still
under at TRAIN end, trough FTX Nov 2022) are long grinds through mixed regimes.
**Cell 7** (rules written before running) — decay-first **FLAT, survives** (2022 gross +41 / +69 bp measured7; net 2022
−3 / +27). Concentration **FLAG**: best 10% of trades = 154% of gross (without the 10 best still +61 bp/trade); deepest
fifth of crashes (≈ −2.8 sd) = 54% of gross. All coin-days: next-day +95 bp (t 4.0) in the bottom-10% zone, fading to
negative above the 20th percentile. Wild > calm in **10/10 coins**.
These are found on TRAIN after many looks — a volatility filter derived from Cell 6 is a refinement that must be
pre-registered and tested once on VAL.

## 9. Step 4 (one lever) — volatility filter, pre-registered (2026-10-04) — FINDING
`step4/PREREG_vol_filter.md` written BEFORE any filtered result (rule: enter H7 only if BTC 30d vol > its expanding past
median; pass = VAL ≥ 30 positions with gross > 0 and net LOW > 0). VAL (2023-03-25 → 11-30) opened ONCE (user).
- Filter ON 50% of TRAIN days, **6% of VAL days** → primary cell **3 positions → INCONCLUSIVE** (as pre-warned: 2023 calm).
- Unfiltered H7 on VAL (not a gate): all10 k=0: 147 positions, gross +52.5 bp (t 1.9), net LOW +10.0 bp/position, yet
  day-weighted Sharpe −1.03, −24% (equal-weight across triggered coins: single-coin days get 100% and lost in 2023).
- TRAIN filtered (in-sample, not evidence): Sharpe 1.22, maxDD −36%, gross +197 bp (t 6.6).
- Observation (no rule change): the expanding-median cut-off is anchored on very volatile 2019–21, so "wild" is rarely
  reached in calmer later years. Redefining it = a NEW idea needing its own pre-registration. **VAL is spent for this lever.**
- Open for the user: what (if anything) the SEALED period (2023-12 → 2026-04-30) should test; commit of the worktrees.

## 10. Holding-period profile (Cell 9, 2026-10-04) — FINDING, descriptive (nothing chosen)
The 24h hold was INHERITED (EDA daily framing → Step 2 `hold 24h`), never measured. Cell 9 = average path of all 963 H7
positions (k=0, all 10, TRAIN, full 72h inside TRAIN), hour by hour, LOW cost with swap charged at the real rollover hour.
| h | gross | baseline* | H7 excess | net LOW | net day-weighted |
|---|---|---|---|---|---|
| 4 | +33 | −5 | +38 | −2 | −23 |
| 12 | +77 | +5 | +72 | +43 | +12 |
| 20 | +76 | – | – | +42 | +16 |
| **24** | +117 | +31 | **+86** | **+74** | +42 |
| 48 | +150 | +60 | +90 | +98 | +57 |
| 72 | +240 | +88 | +152 | +181 | +95 |
*baseline = any coin, any 00:00 UTC entry, Jul-2019 → TRAIN end (crypto's own drift).
- Break-even ≈ 6–8 h. H7's excess bounce builds over the first 24 h, ~flat 24→48 h; 72 h point least reliable.
- Per DAY of capital (H7 refires daily): 24h +74 bp/day > 72h +60 > 48h +49. Net minus drift: 24h +43, 48h +38, 72h +93.
  → 48h worse than 24h; 72h unclear (bull-run drift, 3 swap nights, overlap); 24h stands as a reasonable choice.
- Closing before the rollover (~20h) saves 8.2 bp swap but gives up ~40 bp of bounce — not worth it.
- Wild regime net rises with hold (+154 @24h, +191 @48h, +307 @72h); calm regime negative at every hour (−78 @24h).
- t-stats in Cell 9 are OVERSTATED (same-day positions correlated; multi-day holds overlap).

## 11. RESUME HERE (state at power-off, 2026-10-04)
**Next step (user asked for it, not yet run): ENGINE hold-period SENSITIVITY check** — purpose: "does H7 fall apart if the
hold changes?" (Step 5), NOT to pick a winner. Spec to announce on resume:
- H7 unfiltered, k=0, LOW and HIGH cost, all10 + measured7, TRAIN only (VAL spent, SEALED closed).
- Holds 24h / 48h / 72h as TRANCHES: capital split into H equal daily slices (⅓ of equity per day for 72h), each slice
  runs H7's 24h weights for its own entry day and holds H hours → no double-use of capital. Report Sharpe, maxDD, net per
  position, yearly Sharpe; same truncation test on the new strategy class.
**Where everything is** (all UNCOMMITTED, in worktrees on branch `claude/crypto-data-availability-cltiy2`):
- finding-alphas: `C:\Users\User\finding-alphas_wt_eda02\hunts\2026-09-30_crypto-cost10\` — pull scripts p9–p17, data
  (ftmo/, _sealed/ftmo/, validated/, ftmo_trade_minute(_val)/, bitmex_sample/, btce_sample/), CSV outputs, step4/PREREG.
  Main repo `C:\Users\User\finding-alphas` (branch main) untouched; its uncommitted README/alpha_log/data-hygiene edits kept.
- engine: `C:\Users\User\backtest_engine_wt_eda02\backtest_engine2\notebooks\eda02_crypto_reversal\` — cell_01..cell_09,
  eda02_strategies.py (Saturday-window rule, empty-slice fix, btc_wild, CrashReboundVolFilter), eda02_costs.py
  (ftmo_trade_minute_half_frames); data copies in backtest_engine2/data/eda02_crypto/ (gitignored: validated/, ftmo/).
- eda-routine: `C:\Users\User\eda-routine_wt_eda02` (fetched, untouched).
**Open decisions for the user:** (1) what the SEALED period (2023-12 → 2026-04-30) should test, pre-registered;
(2) commit the worktrees; (3) nothing written to alpha_log.md for §5–§10 yet (findings live here until discussed).
**Session rules in force:** one step per turn (part-0); validated data only; user decides kills; explain simply.
