# Part III-G — Other Asset Classes: ETFs & Futures/Forwards (Ch. 29, 30)

*Taking alpha research beyond single-stock equities. Both share a theme: small, heterogeneous tradable universes → breadth is scarce and overfitting is easier.*

---

## Ch. 29 — ETFs and Alpha Research

ETFs trade on exchanges, mostly tracking an index (first: SPY, 1993). Universe is huge (≈5,785 ETFs, $4.78T AUM as of 2018) spanning equities, bonds, commodities, currencies.

**Merits (why they're tradable for alphas):**
- **Intraday exchange trading** (vs mutual funds at end-of-day NAV) → intraday strategies, arbitrage, shorting, limit/stop orders, margin.
- **Low cost** (expense ratio <1%, SPY 0.09%, some 0.03%).
- **Tax efficiency** via the creation/redemption mechanism (only APs create/redeem, in-kind → no capital-gains event).
- **Transparency** (daily holdings) and **easy market exposure/diversification** (sectors, countries, bonds, commodities, FX).

**Risks (and where they create or destroy alpha):**
- **Tracking error** (≠ premium/discount to NAV) — worse for futures-based (negative roll yield) & commodity ETFs; can be an arb opportunity.
- **Leveraged/inverse ETFs** (2x, 3x, −1, −2x, −3x) — rebalancing decay in volatile markets; handle carefully in long–short books.
- **Factor-risk heterogeneity** — equity ETFs carry market beta; sector/country ETFs carry their exposures; VIX ETFs are special; bond ETFs carry duration; commodity/FX carry macro factors.
- **Capacity constraints** — niche ETFs can grow too big for their index (GDXJ 2017 suspended creations near 20% ownership).
- **Separation from underlying** — US-listed foreign-market ETFs keep trading when the local market is closed/halted (becomes a price-discovery tool).

**Worked alpha ideas:**
- **US sector momentum** (Samuel Lee): 10 sector ETFs; hold up to 3 with best 12-mo return that are also above their 12-mo SMA, else cash. Long-short the market by shorting SPY → market-neutral. (But low Sharpe ~0.38 once market beta removed — use only within a broader portfolio.)
- **Seasonality**: "sell in May" (Nov–Apr equities, May–Oct bonds via TLT/HYG) nearly doubled Sharpe (0.40 → 0.77) and halved drawdown; also gold (Sep–Oct), agricultural ETFs. More market-timing than hedged alpha, but inspires macro indicators.

**Challenges unique to ETF research:**
- **Liquidity is highly skewed** — SPY ≈ 25% of all-ETF volume, top-10 ≈ 50% → real tradable universe is tiny.
- **Near-duplicate funds** (SPY/IVV/VOO all track S&P 500) — don't assign opposite values to near-identical instruments; arb won't cover costs.
- **The inverse/leveraged trap**: long SPY + short SH (inverse S&P) looks dollar-neutral but is **double-long market beta**. Handle inverse/leveraged carefully or your "dollar-neutral" alpha isn't hedged.
- **Small universe → easy overfitting**; persistent factor exposure can fake a high Sharpe (e.g. short-VXX ≈ Sharpe 1.1 is just a vol risk premium). New ETFs only exist late in the backtest → unreliable in-sample.

---

## Ch. 30 — Futures and Forwards

Futures give exposure to an underlying without holding it (equity indices, commodities, currencies, bonds); short-dated FX forwards give relative-currency exposure. Convenient for hedgers & speculators.

**Underlying factor exposure & instrument grouping (the central idea):**
- A future's price depends on the **same factors as its underlying**. Distinct trader groups specialize in distinct sectors (farmers in ags, airlines in energy) with their own risk limits/behavior → **correlations are much weaker than in equities**, and you must group instruments by underlying.
- **Breadth problem**: `Sharpe ∝ √breadth`, but futures sub-universes are tiny (1 to a few dozen). So futures alphas need **greater depth of info per instrument** — and stronger per-instrument alphas decay faster (more visible). Reward: far greater liquidity → trade large size with low impact.
- Tighter groups make the **delete-one-instrument cross-validation** test more meaningful. Finding the right-size group is a core step. (Note: seemingly different asset classes correlate more during crises.)

**Basic alpha-testing checklist (futures):**
1. Identify the sectors & timescales where the idea should appear (e.g. weather → oil/gas, storm duration).
2. Fit a simple model; test robustness while varying parameters; include a **diluted-effect comparison asset** (e.g. Brent vs US crude).
3. Test the **converse** — where you expect NO relationship (other sectors). Great at catching mis-coded tests.
4. Then test out-of-sample (crucial given tiny universes).

**Worked idea families:**
- **Follow the (smart) money — COT report** (weekly, CFTC): breakdown of open interest by commercial (hedgers), noncommercial (large specs), nonreportable (small specs). Go **long instruments with rising speculator open interest, short falling**. Works where speculators are a big share; compare cross-sectionally within tight groups; hedge/exit before surprises (Fed meetings, crop reports).
- **Seasonality**: agriculture/energy (harvest, heating/cooling); AUD (commodity-linked); horizon ~1–3 months; fails on supply/demand shocks.
- **Risk-on / risk-off**: classify the regime (daily→quarterly) and assets, position accordingly. Indicators: **VIX** (high/rising = risk-off), yield curve (steep = risk-on), sector flows (consumer-disc vs utilities), carry pairs (AUD/JPY), top covariance eigenvector (= risk-off). Trade on VIX & broad cross-section; works on weeks-to-months horizon.
- **Carry & contango/backwardation**: contango = upward curve (storage cost; commodities); backwardation = downward (financials, coupons). **Carry trade**: sell contango, buy backwardation; profit = contract roll-down + roll yield. Works where ≥1 side has nonzero interest; fails when curves are flat (G-10 carry died post-2008 at zero rates); slow steady profits but vulnerable to risk-off crashes.

---

## Checklist

- [ ] ETFs: filter to genuinely liquid names; never oppose near-duplicates; treat inverse/leveraged explicitly so "dollar-neutral" is truly hedged; beware tiny-universe overfitting & late-listing bias.
- [ ] Futures: group by underlying; accept low breadth → need deep per-instrument signals; run the converse/no-relationship test; lean on OOS.
- [ ] Futures idea menu: COT speculator flow, seasonality (1–3mo), risk-on/off (VIX/yield-curve/carry), carry (contango/backwardation).
