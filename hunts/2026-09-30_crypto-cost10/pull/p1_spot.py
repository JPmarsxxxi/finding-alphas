"""Family `spot`: 1h trade-print OHLCV from four venues.

binance_<SYM>   Binance spot <BASE>USDT, data-api.binance.vision (api.binance.com geo-blocked here). + FTMO spread col.
bitstamp_BTCUSD Bitstamp BTC/USD from 2011 - the long-history BTC (kept separate, never spliced).
coinbase_<SYM>  Coinbase <BASE>-USD. Mechanism: Coinbase-minus-Binance premium = US (institutional/ETF-desk)
                demand vs offshore; practitioners read a persistent premium as US spot buying.
coinbase_USDT   USDT-USD: the peg. Mechanism: USDT trading above $1 = demand for offshore dollars to buy crypto.
upbit_<SYM>     Upbit <BASE>-KRW. Mechanism: "kimchi premium" (vs Binance x USDKRW) = Korean retail heat behind
                capital controls; extremes mark retail euphoria.
All stamps UTC, bar OPEN time, knowable at open + 1h.
"""
import datetime as dt
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from lib import COINS, FTMO_COMMISSION_RT_BP, client, get, log_fail, save

NOW_MS = int(pd.Timestamp.now(tz="UTC").timestamp() * 1000)
PROV = dict(type="trade print (last-trade OHLC)", freq="1h", stamp="UTC bar open",
            knowable="open + 1h", notes="")


def binance(ftmo):
    base, spread = COINS[ftmo]
    rows, start = [], 0
    with client() as cli:
        while True:
            b = get(cli, "https://data-api.binance.vision/api/v3/klines",
                    {"symbol": base + "USDT", "interval": "1h", "startTime": start, "limit": 1000})
            if not b:
                break
            rows += b
            start = b[-1][0] + 1
            if len(b) < 1000:
                break
    df = pd.DataFrame(rows, columns=["t", "open", "high", "low", "close", "vol", "_ct", "quote_vol", "n",
                                     "buy_vol", "buy_quote_vol", "_x"]).drop(columns=["_ct", "_x"])
    df["t"] = pd.to_datetime(df["t"], unit="ms", utc=True)
    for c in df.columns[1:]:
        df[c] = df[c].astype(float)
    df["sell_vol"] = df["vol"] - df["buy_vol"]
    df["ftmo_spread_rt_bp"] = spread
    df["ftmo_commission_rt_bp"] = FTMO_COMMISSION_RT_BP
    save(df, "spot", f"binance_{ftmo}", "t", {**PROV, "source": f"Binance spot {base}USDT",
         "notes": "buy_vol = taker-buy base volume. ftmo_spread_rt_bp is a constant single live sample (x098)."})


def bitstamp():
    rows, start = [], 1312156800  # 2011-08-01
    with client() as cli:
        while True:
            j = get(cli, "https://www.bitstamp.net/api/v2/ohlc/btcusd/", {"step": 3600, "limit": 1000, "start": start})
            b = j["data"]["ohlc"]
            if not b:
                break
            rows += b
            nxt = int(b[-1]["timestamp"]) + 3600
            if nxt <= start or nxt * 1000 > NOW_MS:
                break
            start = nxt
    df = pd.DataFrame(rows)
    df["t"] = pd.to_datetime(df.pop("timestamp").astype(int), unit="s", utc=True)
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    save(df, "spot", "bitstamp_BTCUSD", "t", {**PROV, "source": "Bitstamp BTC/USD",
         "notes": "Early years (2011-2013) have hours with zero volume and flat bars; check zero-gap rate."})


def coinbase(product, name, max_empty=6):
    rows = []
    end = pd.Timestamp.now(tz="UTC").floor("h")
    step = pd.Timedelta(hours=300)
    empty_run = 0
    with client() as cli:
        while empty_run < max_empty:
            start = end - step
            b = get(cli, f"https://api.exchange.coinbase.com/products/{product}/candles",
                    {"granularity": 3600, "start": start.isoformat(), "end": end.isoformat()})
            if b:
                rows += b
                empty_run = 0
            else:
                empty_run += 1
            end = start
    if not rows:
        log_fail("spot", name, "no rows")
        return
    df = pd.DataFrame(rows, columns=["t", "low", "high", "open", "close", "volume"])
    df["t"] = pd.to_datetime(df["t"], unit="s", utc=True)
    df = df.drop_duplicates("t")
    save(df, "spot", name, "t", {**PROV, "source": f"Coinbase {product}",
         "notes": "Walked backwards in 300h windows until 6 consecutive empty windows (= listing reached)."})


def upbit(base):
    rows, to = [], None
    with client() as cli:
        while True:
            p = {"market": f"KRW-{base}", "count": 200}
            if to:
                p["to"] = to
            b = get(cli, "https://api.upbit.com/v1/candles/minutes/60", p)
            if not b:
                break
            rows += b
            to = b[-1]["candle_date_time_utc"] + "Z"
            if len(b) < 200:
                break
    df = pd.DataFrame(rows)
    df["t"] = pd.to_datetime(df["candle_date_time_utc"], utc=True)
    df = df.rename(columns={"opening_price": "open", "high_price": "high", "low_price": "low",
                            "trade_price": "close", "candle_acc_trade_volume": "vol",
                            "candle_acc_trade_price": "quote_vol_krw"})[
        ["t", "open", "high", "low", "close", "vol", "quote_vol_krw"]]
    save(df, "spot", f"upbit_{base}KRW", "t", {**PROV, "source": f"Upbit KRW-{base}",
         "notes": "KRW-quoted. Kimchi premium needs USDKRW (macro/yahoo_KRW=X, daily) - hourly FX not available."})


def run(fn, *a):
    try:
        fn(*a)
    except Exception as e:  # keep the other pulls going
        log_fail("spot", f"{fn.__name__}{a}", e)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "xrp":
    coinbase("XRP-USD", "coinbase_XRPUSD", max_empty=100)  # ~1250 days of empty windows bridges the 2021-23 delisting
elif __name__ == "__main__":
    jobs = [(binance, c) for c in COINS] + [(bitstamp,)]
    jobs += [(coinbase, f"{COINS[c][0]}-USD", f"coinbase_{c}") for c in COINS if c != "BNBUSD"]
    jobs += [(coinbase, "USDT-USD", "coinbase_USDTUSD")]
    jobs += [(upbit, b) for b in ["BTC", "ETH", "XRP", "SOL", "DOGE", "ADA"]]
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda j: run(*j), jobs))
    print("DONE p1_spot", file=sys.stderr)
