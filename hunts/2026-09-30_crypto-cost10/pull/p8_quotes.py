"""Family `quotes`: MEASURED Binance spot best bid/ask (Tardis.dev free tier = first day of each month), per data-hygiene.md
rule 1 ("pull BOTH sides"). Source: https://datasets.tardis.dev/v1/binance/quotes/YYYY/MM/01/<SYM>.csv.gz (the exchange's
bookTicker stream as recorded by Tardis; Binance spot bookTicker carries no exchange timestamp, so `timestamp` = Tardis
receipt time, microseconds UTC). Coverage starts 2019-03-30. Range pulled: 2019-04 .. 2023-03 (TRAIN only).

Each day is reduced on arrival to per-minute rows and the raw file deleted:
  t (minute START, UTC) · half_bp_tw (time-weighted mean half-spread, bp) · half_bp_max · bid_last · ask_last · n_updates
The free tier has a data-transfer limit: on HTTP 429 the script sleeps the server's retryAfterSeconds and resumes.
Files already reduced are skipped, so the script can be re-run at any time.
"""
import io
import json
import os
import sys
import time

import httpx
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "quotes_minute")
LOG = os.path.join(os.path.dirname(HERE), "logs", "p8_quotes_progress.jsonl")
COINS = {"BTCUSD": "BTCUSDT", "ETHUSD": "ETHUSDT", "BNBUSD": "BNBUSDT", "SOLUSD": "SOLUSDT", "XRPUSD": "XRPUSDT",
         "DOGEUSD": "DOGEUSDT", "ADAUSD": "ADAUSDT", "LTCUSD": "LTCUSDT", "BCHUSD": "BCHUSDT", "DOTUSD": "DOTUSDT"}
LISTED = {"SOLUSD": "2020-09-01", "DOTUSD": "2020-09-01", "DOGEUSD": "2019-08-01", "BCHUSD": "2019-12-01"}


def months():
    ms = pd.date_range("2019-04-01", "2023-03-01", freq="MS")
    # quarterly months first so a partial pull is already spread over the whole period
    first = [m for m in ms if m.month in (1, 4, 7, 10)]
    return first + [m for m in ms if m not in first]


def reduce_day(raw):
    d = pd.read_csv(io.BytesIO(raw), usecols=["timestamp", "bid_price", "ask_price"], compression="gzip")
    d = d[(d.bid_price > 0) & (d.ask_price >= d.bid_price)]
    ts = pd.to_datetime(d["timestamp"], unit="us", utc=True)
    mid = (d.ask_price + d.bid_price) / 2
    half = ((d.ask_price - d.bid_price) / mid * 1e4 / 2).to_numpy()
    tnum = ts.astype("int64").to_numpy()
    dur = np.diff(tnum, append=tnum[-1] + 1)          # each quote lives until the next one (last: 1 us)
    minute = ts.dt.floor("min")
    g = pd.DataFrame({"t": minute.to_numpy(), "hw": half * dur, "w": dur, "half": half,
                      "bid": d.bid_price.to_numpy(), "ask": d.ask_price.to_numpy()}).groupby("t")
    out = pd.DataFrame({"half_bp_tw": g["hw"].sum() / g["w"].sum(), "half_bp_max": g["half"].max(),
                        "bid_last": g["bid"].last(), "ask_last": g["ask"].last(), "n_updates": g["half"].size()})
    return out.reset_index()


def log(rec):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    cli = httpx.Client(timeout=300, follow_redirects=True, headers={"User-Agent": "finding-alphas-research"})
    for m in months():
        for coin, sym in COINS.items():
            if m < pd.Timestamp(LISTED.get(coin, "2019-01-01")):
                continue
            path = os.path.join(OUT, f"{coin}_{m:%Y-%m-%d}.parquet")
            if os.path.exists(path):
                continue
            url = f"https://datasets.tardis.dev/v1/binance/quotes/{m:%Y/%m/%d}/{sym}.csv.gz"
            for attempt in range(50):
                try:
                    r = cli.get(url)
                except httpx.HTTPError as e:
                    time.sleep(30)
                    continue
                if r.status_code == 429:
                    try:
                        wait = int(r.json().get("retryAfterSeconds", 600))
                    except ValueError:
                        wait = 600
                    log({"coin": coin, "day": f"{m:%Y-%m-%d}", "status": 429, "sleep_s": min(wait, 3600)})
                    time.sleep(min(wait, 3600))
                    continue
                break
            if r.status_code != 200:
                log({"coin": coin, "day": f"{m:%Y-%m-%d}", "status": r.status_code})
                continue
            agg = reduce_day(r.content)
            agg.to_parquet(path, index=False)
            log({"coin": coin, "day": f"{m:%Y-%m-%d}", "status": 200, "mb": round(len(r.content) / 1e6, 1),
                 "minutes": len(agg), "median_half_bp": round(float(agg.half_bp_tw.median()), 4)})
    print("DONE p8_quotes", file=sys.stderr)


if __name__ == "__main__":
    main()
