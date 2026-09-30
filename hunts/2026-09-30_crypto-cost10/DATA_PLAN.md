# DATA PLAN — crypto-cost10 hunt (2026-09-30)

Planning step before any fetch. Reachability was tested from the cloud container on 2026-09-30
(HTTP 200 = reachable).

**Constraint that decides fit:** on FTMO every crypto symbol pays −30%/yr swap on both sides
(~8.2 bp/night, triple on Friday), so the trades are **intraday**. Data that updates hourly or faster can be
a signal. Daily or weekly data mostly works as a **regime filter or conditioner** on intraday trades.

## Prices (decided: 1b)
| set | source | history | status |
|---|---|---|---|
| 10 FTMO coins, spot | Binance `data-api.binance.vision` | listing → today | 200 |
| BTC/USD long history (kept separate, not spliced) | Bitstamp | 2011-09 → today | 200 |
| FTMO spread column | x098 live MT5 sample, constant per symbol | 2026-09-02 | from log |

## A. Crypto alt data — ranked by fit
| # | data | source | history / freq | why it could move price | batch overlap | fit |
|---|---|---|---|---|---|---|
| A1 | Perp funding rate, all 10 | `data.binance.vision` um fundingRate; OKX | 2019-09 → / 8h | crowded leverage pays to stay in; extremes force deleveraging | #045 used BTC only | **high**: sub-daily, cross-section untested |
| A2 | Open interest + top-trader/retail long-short + taker ratios | `data.binance.vision` um metrics | ~2020-09 → / 5m | positioning fragility; liquidation cascades | #045 BTC/ETH | **high** (cross-section new) |
| A3 | Perp–spot basis | um klines vs spot klines | 2019-09 → / 1h | leverage demand; arbitrage pressure closes it | none | **high**, new |
| A4 | Deribit DVOL (implied vol index), BTC/ETH | Deribit API | 2021-03 → / 1h | implied−realised gap prices fear; vol regime | banked, never tested as signal | medium-high |
| A5 | Exchange supply / inflows | Coin Metrics community (`SplyExNtv`, `FlowInExNtv`) | ~2011 → / 1d | coins moved onto exchanges = supply about to be sold | none | medium (daily) |
| A6 | Active addresses, hashrate, MVRV | Coin Metrics community | ~2010 → / 1d | network use; miner stress; holders' profit vs cost basis | none | low-medium (slow) |
| A7 | Mempool fees / congestion | mempool.space | ~2016 → / block | on-chain urgency spikes around panic and exchange flows | none | medium |
| A8 | Stablecoin supply (USDT+USDC) | DefiLlama | 2017 → / 1d | new dollars minted = buying power arriving | none | medium |
| A9 | Chain TVL (ETH, SOL, BNB) | DefiLlama | 2018 → / 1d | capital committed to each chain; alt-specific demand | none | low-medium |
| A10 | Fear & Greed index | alternative.me | 2018-02 → / 1d | crowd sentiment extremes → reversal | none | low (composite of price) |
| A11 | Wikipedia pageviews (per coin) | Wikimedia | 2015-07 → / 1d | retail attention inflow | none | low-medium |
| A12 | CME Bitcoin futures COT | CFTC | 2017-12 → / weekly | institutional positioning | #024 COT (commodities) | low (weekly) |

**Blocked from this container:** Google Trends, Reddit, GitHub API, Glassnode (key required),
Farside ETF flows, Bybit, Binance main REST and futures REST (451 geo-block), FRED, Stooq.

## B. Fundamental / macro data that correlates with crypto
| # | data | source | history / freq | why | fit |
|---|---|---|---|---|---|
| B1 | **US net liquidity** = Fed balance sheet − TGA − reverse repo | Fed H.4.1 (federalreserve.gov), Treasury fiscaldata (TGA), NY Fed (RRP) | 2002 → / weekly+daily | Howell *Capital Wars* (lens corpus): crypto is the purest liquidity asset | medium-high regime filter |
| B2 | Treasury yield curve (2y, 10y, real yields) | treasury.gov CSV | 1990 → / 1d | cost of holding zero-yield assets | medium |
| B3 | Policy rates: SOFR, EFFR | NY Fed | 2018 → / 1d | same | low-medium |
| B4 | Dollar index DXY, EURUSD, USDJPY | Yahoo, ECB | 1971 → / 1d (Yahoo also intraday, recent only) | dollar liquidity; yen carry unwinds (2024-08) | medium |
| B5 | Risk assets: S&P 500, Nasdaq-100, VIX, MOVE-proxy (TLT) | Yahoo | decades / 1d | risk-on beta; correlation regimes | medium |
| B6 | Gold, oil | Yahoo | decades / 1d | "digital gold" / inflation hedge claims | low-medium |
| B7 | Crypto equities/ETFs: IBIT, GBTC, MSTR, COIN, miners | Yahoo | 2015–2024 → / 1d | US-hours institutional flow proxy (ETF volume = flow proxy) | medium |
| B8 | Macro event calendar: FOMC, CPI, NFP dates | Fed / BLS schedules | 2011 → | scheduled volatility; drift into and out of the release (#037/#038 did this for FOMC on equities) | **high**: intraday by construction |
| B9 | Policy rates (other central banks) | BIS, ECB | decades | global liquidity | low |

## Recommendation
1. **Best fit for intraday FTMO trading:** A1–A3 across all 10 coins, then B8 (event-time intraday), then A4.
2. **Pull as conditioners (cheap, daily):** B1, B2, B4, B5, B7, A5, A8.
3. **Pull only if wanted:** A6, A7, A9–A12, B3, B6, B9.
