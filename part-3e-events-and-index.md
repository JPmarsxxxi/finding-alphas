# Part III-E — Event-Driven & Index Strategies (Ch. 25, 28)

*Alphas keyed to discrete corporate events and index mechanics. Returns are largely uncorrelated with the broad market → diversification value. Some need a balance sheet (institutional), but the spread/impact ideas are usable.*

---

## Ch. 25 — Event-Driven Investing

Strategies exploiting price inefficiencies around corporate events. **All-season**: every business-cycle phase produces some event type (M&A in expansions, distressed in contractions). Returns are market-uncorrelated → portfolio diversifier.

### Merger arbitrage (the classic)
A bet on whether an announced deal **closes**. Post-announcement the target jumps but stays below the offer price (deal risk). The arbitrageur captures the gap:
```
Deal spread = (offer price − target stock price) / target stock price
```
This is the return if the deal completes. **All-stock deal:** long the target, short the acquirer (hedge). Diversify across many deals so no single break hurts. Watch the **MAC clause** (lets a party walk). Friendly > hostile completion odds; deals fail on antitrust, financing (credit crunch), or market declines. Mostly market-neutral, but correlation to market **rises in severe downturns**.

### Spin-offs / split-offs / carve-outs
Divestiture to unlock value. Spin-off = pro-rata shares to parent holders; split-off = exchange parent shares for sub shares; carve-out = parent sells a fractional stake. Both parent & spun-off unit tend to **outperform** afterward (focus + accurate per-unit valuation), but short-term weakness when the small-cap spin-off doesn't fit parent holders' mandates (forced selling).

### Distressed-asset investing
Securities of distressed/bankrupt firms, often forced-sold below intrinsic value (mandate constraints) → "cigar-butt" bargains (Buffett). Spans high-yield bonds, bank loans, CDS, preferred/common, warrants. Best in bull markets (turnaround payoff); company/sector-specific more than cycle-driven. Active (turnaround, info-restricted) vs passive (trading) managers.

### Index-rebalancing arbitrage → see Ch. 28
### Capital-structure arbitrage
Trade one security of a firm vs another: long bonds / short stock, equity vs CDS, senior vs junior debt, convertible-bond arb, dual-listing mispricings. Bad news hits stock harder than bonds (priority claim, dividend cut, equity liquidity) → long equity / short bond (or buy CDS protection) on detected mispricing.

---

## Ch. 28 — Finding an Index Alpha

### Index arbitrage (needs a balance sheet)
Profit from gaps between actual & theoretical index-futures prices:
```
Fair value of future = cash value of index + interest − dividends
```
Holding a future frees capital (low margin) but forgoes dividends → interest & dividends are the two drivers. Bank desks layered overlays (ETF creation/redemption, stock lending, options reversals/conversions, event plays) to push <1% → 5%+. Mostly only feasible for the largest firms with funding/balance-sheet advantages.

### Market impact from index changes (buy-side-accessible)
The tradable part for active managers. Index reconstitution forces buying of adds / selling of deletes → predictable impact:
- **Russell 2000** reconstitutes annually (June) → estimated **28 bps/yr drag** (2007–2015). Trade: **short the adds, buy the deletes on the effective date** (reversion as relative-value traders push dislocations back). True cost of owning IWM ≫ its 20 bps expense ratio.
- **S&P 500 / total-market** (CRSP) products see far less drag (higher liquidity, harder-to-predict additions, no trading on cap migrations).

### Other index anomalies
- **Captive capital-raising**: newly-added S&P 500 names (esp. REITs) raise equity at tiny discounts (~17–26 bps vs ~2.8% normal) because index funds are forced buyers → distorts event-driven alphas expecting post-offering selling.
- **Index vs nonindex valuation distortion**: Russell 2000 members trade at a **premium** to nonindex peers (every sector, e.g. comms P/E 30 vs 19) despite >30% having negative earnings; in large caps it **reverses** (S&P 500 trades at a discount, partly long-momentum-factor exposure).

---

## Checklist

- [ ] Merger arb: compute deal spread, weight by completion probability, hedge (long target/short acquirer), diversify across deals, read the MAC clause.
- [ ] Spin-offs: consider holding both parent & unit; expect short-term forced selling of the small-cap unit.
- [ ] Index changes: trade Russell 2000 reconstitution (short adds / buy deletes); know S&P 500 behaves differently.
- [ ] Adjust event alphas for captive-buyer effects around index additions.
- [ ] Most pure index-arb needs institutional funding — focus your effort on the impact/anomaly side.
