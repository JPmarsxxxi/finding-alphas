# MECHANISMS — why each dataset might predict crypto returns (crypto-cost10, 2026-09-30)

Each line uses the Step 1 test form: **a change in [data] predicts [price response] because [economic reason]**.
These are candidate claims for Step 1, not findings. Nothing has been measured. Prior: H/M/L, my judgement, stated
before any look at the data. "Intraday-fit" = the signal refreshes fast enough to trade within FTMO's no-overnight
constraint (swap ≈ 8.2 bp/night on every coin).

## Crypto-native positioning and derivatives (hourly or faster: intraday-fit)
| # | claim | data | prior |
|---|---|---|---|
| M1 | Coins with the most extreme funding **relative to the other nine** underperform the next hours, because the crowded side pays to stay in and is the first to be liquidated | `perp/funding_*` | M |
| M2 | A rising perp-over-spot premium with falling spot volume predicts reversal, because the move is leverage, not spot demand, and arbitrage closes it | `perp/perp_premium_*`, `spot/binance_*` | M |
| M3 | OI rising fast into a price move predicts a larger, faster reversal (a liquidation cascade) than the same move on flat OI | `perp/metrics_*` | M |
| M4 | Top-trader vs all-account long/short divergence: when "smart" accounts lean against the crowd, price follows the smart side | `perp/metrics_*` | L-M |
| M5 | Binance-vs-Hyperliquid and Binance-vs-Deribit funding gaps that persist mean capital cannot cross venues; the gap closes via price on the richer venue | `deriv/hyperliquid_funding_*`, `deriv/deribit_funding_*` | L-M |
| M6 | DVOL rising while price is flat predicts a large move (direction from the skew/funding sign), because options desks price information before spot | `deriv/deribit_dvol_*`, `perp/bvol_*` | M |

## Cross-venue premia (exotic, hourly: intraday-fit)
| # | claim | data | prior |
|---|---|---|---|
| M7 | **Coinbase premium**: Coinbase USD above Binance USDT predicts positive returns over the following hours, because it is US spot buyers (institutions, ETF desks) moving first on the venue they are allowed to use | `spot/coinbase_*` vs `spot/binance_*` | M-H |
| M8 | **Kimchi premium** extremes (Upbit KRW / (Binance × USDKRW) − 1) predict negative returns, because Korean retail euphoria behind capital controls marks local tops | `spot/upbit_*`, `macro/yahoo_KRW_X` | M |
| M9 | **USDT above its peg** predicts positive returns, because it measures demand for offshore dollars to buy crypto | `spot/coinbase_USDTUSD` | M |
| M10 | The CME gap from the weekend (BTC=F Friday close vs Monday open) tends to fill, because CME basis traders and hedgers anchor to it | `macro/yahoo_BTC_F`, `spot/binance_BTCUSD` | L (folklore; test it to kill it) |

## Liquidity and flow (daily: conditioner)
| # | claim | data | prior |
|---|---|---|---|
| M11 | Stablecoin net mints predict positive returns over the next days, because new dollars arrive to be spent on crypto | `defi/stable_*` | M |
| M12 | Stablecoins accumulating on a specific chain (SOL, BSC, TRON) predict that chain's token outperforming, because dry powder is parked where it will be spent | `defi/stable_chain_*`, `defi/tvl_*` | L-M |
| M13 | Exchange net inflows (coins onto exchanges) predict negative returns, because coins go to exchanges to be sold | `onchain/cm_*` FlowIn/FlowOut | M (flows are relabelled backwards: not PIT) |
| M14 | Rising US net liquidity (Fed securities − TGA − RRP) predicts positive BTC returns over weeks (Howell, *Capital Wars*) | `macro/nyfed_soma`, `macro/tga`, `macro/nyfed_rrp` | M (weekly: too slow to trade, usable as a regime) |
| M15 | Spot-ETF volume spikes (IBIT/FBTC/GBTC) during US hours predict the next Asian session, because creations are bought after the close | `macro/yahoo_IBIT` etc. | L-M (2024+ only: all sealed today) |

## Miner and network (daily: conditioner)
| # | claim | data | prior |
|---|---|---|---|
| M16 | Falling hashprice (miner revenue per hash) predicts negative returns, because stressed miners sell inventory | `onchain/bcom_miners_revenue`, `onchain/mempool_hashrate` | L-M |
| M17 | Large positive difficulty adjustments are followed by miner selling in the next days | `onchain/mempool_difficulty_adj` | L |
| M18 | Fee and mempool spikes mark panic transfers to exchanges and precede volatility | `onchain/mempool_feerates`, `onchain/bcom_mempool_*` | L-M |
| M19 | MVRV extremes (market cap far above the holders' cost basis) predict weak forward returns, because holders sitting on big profits take them | `onchain/cm_*` CapMVRVCur | M (long horizon: conditioner only) |

## Events (event-time: intraday-fit around the event)
| # | claim | data | prior |
|---|---|---|---|
| M20 | Crypto drifts up into FOMC statements and reverts after (the pre-FOMC drift, never tested on crypto here; #037/#038 tested equities) | `macro/fomc_dates` | M |
| M21 | Weak Treasury auctions (low bid-to-cover, a yield tail) cause risk-off within hours; crypto is the highest-beta risk asset | `macro/ust_auctions` | L-M |
| M22 | A large DeFi hack sells off the affected chain's token within hours to days | `defi/hacks` | M |
| M23 | CFTC TFF: leveraged funds' extreme net short on CME BTC is basis trade, not direction; the *change* in asset-manager longs leads | `macro/cftc_tff_*` | L |

## Attention (daily/weekly: conditioner)
| # | claim | data | prior |
|---|---|---|---|
| M24 | Wikipedia pageview spikes predict short-term positive then negative returns (the attention-driven buying pressure of Da, Engelberg & Gao, 2011) | `attention/wiki_*` | M |
| M25 | News volume up plus tone down (GDELT) predicts continuation of a selloff | `attention/gdelt_*` | L-M |
| M26 | SEC filings mentioning bitcoin (adoption paperwork) lead institutional flows by weeks | `attention/sec_*` | L |
| M27 | Fear & Greed extremes are contrarian | `attention/fear_greed` | L (partly built from price) |

## Wildcard (~20% budget, low prior on purpose)
| # | claim | data | prior |
|---|---|---|---|
| M28 | Geomagnetic storms lower next-day returns through a mood channel (Krivelyova & Robotti, 2003, on equities) | `attention/kp_geomagnetic` | L |
| M29 | Carry-unwind shocks: sharp yen strength (JPY=X) or stress in emerging-market currencies (TRY, ARS, NGN, which are also stablecoin-adoption markets) spills into crypto | `macro/yahoo_JPY_X`, `_TRY_X`, `_ARS_X`, `_NGN_X` | L-M |

## Tried and unreachable from this container
Google Trends, Reddit, GitHub API, Glassnode, Farside ETF flows, Bybit, Binance main and futures REST (451 geo-block),
FRED, Stooq, BLS release calendar (CPI dates), CME FedWatch, Upbit listing notices (Cloudflare), DefiLlama bridges and
derivatives (paid plan), beaconcha.in (key), Dune (key), EIA (key), ERCOT. Binance option EOH summaries exist only for
about 150 days in 2023 and were skipped.
