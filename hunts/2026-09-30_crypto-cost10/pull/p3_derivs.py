"""Family `deriv`: non-Binance derivatives venues.

deribit_dvol_<X>        Deribit DVOL (30d implied vol index), BTC/ETH, 1h. Mechanism: implied minus realised =
                        the price of fear; DVOL spikes without a price move = options desks hedging something.
deribit_funding_<X>     Deribit perpetual hourly funding (interest_1h) + index price.
hyperliquid_funding_<X> Hyperliquid (on-chain perp DEX) hourly funding. Mechanism: DEX-vs-CEX funding gap =
                        where leverage is migrating; a gap that arbitrage cannot close signals capital friction.
"""
import sys
import time

import pandas as pd

from lib import COINS, client, get, log_fail, save

NOW = int(time.time() * 1000)


def dvol(cur):
    rows, end = [], NOW
    start0 = int(pd.Timestamp("2021-03-01", tz="UTC").timestamp() * 1000)
    with client() as cli:
        while end > start0:
            j = get(cli, "https://www.deribit.com/api/v2/public/get_volatility_index_data",
                    {"currency": cur, "start_timestamp": start0, "end_timestamp": end, "resolution": 3600})
            d = j["result"]["data"]
            if not d:
                break
            rows += d
            cont = j["result"].get("continuation")
            if not cont or cont >= end:
                break
            end = cont
    df = pd.DataFrame(rows, columns=["t", "open", "high", "low", "close"]).drop_duplicates("t")
    df["t"] = pd.to_datetime(df["t"], unit="ms", utc=True)
    save(df, "deriv", f"deribit_dvol_{cur}", "t", dict(
        source=f"Deribit DVOL {cur}", type="implied-vol index (annualised %, 30d)", freq="1h",
        stamp="UTC bar open", knowable="open + 1h", notes=""))


def deribit_funding(cur):
    rows = []
    start = int(pd.Timestamp("2019-05-01", tz="UTC").timestamp() * 1000)
    step = 30 * 24 * 3600 * 1000
    with client() as cli:
        while start < NOW:
            j = get(cli, "https://www.deribit.com/api/v2/public/get_funding_rate_history",
                    {"instrument_name": f"{cur}-PERPETUAL", "start_timestamp": start,
                     "end_timestamp": min(start + step, NOW)})
            rows += j["result"]
            start += step
    df = pd.DataFrame(rows).drop_duplicates("timestamp")
    df["t"] = pd.to_datetime(df.pop("timestamp"), unit="ms", utc=True)
    save(df, "deriv", f"deribit_funding_{cur}", "t", dict(
        source=f"Deribit {cur}-PERPETUAL funding history", type="realised hourly funding + index price",
        freq="1h", stamp="UTC hour end", knowable="at stamp", notes="interest_1h / interest_8h are fractions."))


def hyperliquid(coin):
    rows = []
    start = int(pd.Timestamp("2023-05-01", tz="UTC").timestamp() * 1000)
    with client() as cli:
        while start < NOW:
            b = get(cli, "https://api.hyperliquid.xyz/info", method="POST",
                    body={"type": "fundingHistory", "coin": coin, "startTime": start})
            if not b:
                break
            rows += b
            nxt = b[-1]["time"] + 1
            if nxt <= start or len(b) < 10:
                break
            start = nxt
            time.sleep(0.3)
    if not rows:
        return log_fail("deriv", f"hyperliquid_funding_{coin}", "no rows")
    df = pd.DataFrame(rows)
    df["t"] = pd.to_datetime(df.pop("time"), unit="ms", utc=True)
    df["fundingRate"] = pd.to_numeric(df["fundingRate"])
    df["premium"] = pd.to_numeric(df["premium"])
    save(df.drop(columns=["coin"]), "deriv", f"hyperliquid_funding_{coin}USD", "t", dict(
        source=f"Hyperliquid {coin} perp", type="realised hourly funding + premium", freq="1h",
        stamp="UTC settlement", knowable="at stamp", notes="Hyperliquid launched 2023; short history."))


if __name__ == "__main__":
    for fn, args in ([(dvol, c) for c in ["BTC", "ETH"]] + [(deribit_funding, c) for c in ["BTC", "ETH"]] +
                     [(hyperliquid, COINS[c][0]) for c in COINS]):
        try:
            fn(args)
        except Exception as e:
            log_fail("deriv", f"{fn.__name__}_{args}", e)
    print("DONE p3_derivs", file=sys.stderr)
