"""p14 - Step P1: do last-trade hourly closes agree with REAL mids? (EDA#2, middle-ground data plan, user 2026-10-04)

Trade prices under test (data/spot, last-trade OHLC, t = UTC bar OPEN, close = last trade before t+1h):
  binance_<coin>, coinbase_<coin>, bitstamp_BTCUSD
Mids (two-sided), each taken at the END of bar t (the moment the trade close is printed):
  A  Binance bid/ask, Tardis minute file: minute t+59 -> (bid_last+ask_last)/2      same venue, 1st of each month 2019-04..2023-03
  B  FTMO H1 mid_close (bid + bar spread/2; verified 2022+ vs FTMO ticks)           2022-01..2023-11, DOT excluded (spread scale bug)
  C  BitMEX PERPETUALS only (XBTUSD, ETHUSD, <coin>USD/USDT), last quote in hour      sample days (15th) 2016..2023-07; NO dated futures
  D  BTC-e spot order book (Harvard Dataverse CC0), last 10s snapshot in hour         2015-01..2016-08, BTC only (streamed, raw deleted)
Everything stops at the seal: rows >= 2023-12-01 are never read into a comparison.

Metrics per check x venue x coin x year:
  gap_bp        median of (close/mid - 1) in bp                       (the offset)
  |gap|_med     median |gap| (same venue)  or  median |gap - offset| (cross venue: venue offset removed)
  |gap|_p90     90th percentile of the same quantity
  hr_corr       correlation of hourly returns, trade vs mid (consecutive hours only)
  day_diff_bp   median |r_trade - r_mid| over each UTC day, return from the 00:00 bar close to the 23:00 bar close
PASS (user rule (b), 2026-10-04):
  same venue    |gap|_med <= 2.5 bp   and day_diff_bp <= 5 bp
  cross venue   |gap|_med <= 10 bp    and day_diff_bp <= 5 bp
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPOT = os.path.join(ROOT, "data", "spot")
SEAL = pd.Timestamp("2023-12-01", tz="UTC")
COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
GITBASH = r"C:\Program Files\Git\usr\bin\bash.exe"
BTCE_DIR = os.path.join(ROOT, "data", "btce_sample")
BTCE_DS = "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/8HCUFH"
MES = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
       "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
SNAP = re.compile(rb'\{"time":"([^"]+)","asks":\[\[([0-9.]+),[^\]]*\].*?"bids":\[\[([0-9.]+),')


# ---------------------------------------------------------------- D: BTC-e fetch (streamed, resume-safe)
def btce_fetch():
    import httpx
    os.makedirs(BTCE_DIR, exist_ok=True)
    files = httpx.get(BTCE_DS, timeout=60).json()["data"]["latestVersion"]["files"]
    for f in files:
        name = f["dataFile"]["filename"]
        m = re.match(r"OrderBook_BTCE_([A-Za-z]+)-(\d{4})\.txt", name)
        if not m:
            continue
        ym = f"{m.group(2)}-{MES[m.group(1)]:02d}"
        out = os.path.join(BTCE_DIR, f"{ym}.parquet")
        if os.path.exists(out):
            continue
        url = f"https://dataverse.harvard.edu/api/access/datafile/{f['dataFile']['id']}"
        p = subprocess.Popen([GITBASH, "-c", f"curl -sfL --max-time 1800 '{url}'"], stdout=subprocess.PIPE)
        rows, buf, crossed = [], b"", 0
        while True:
            chunk = p.stdout.read(8 << 20)
            if not chunk:
                break
            buf += chunk
            last = 0
            for mm in SNAP.finditer(buf):
                ask, bid = float(mm.group(2)), float(mm.group(3))
                if bid <= 0 or ask < bid:
                    crossed += 1
                else:
                    rows.append((mm.group(1).decode(), bid, ask))
                last = mm.end()
            buf = buf[last:]
        rc = p.wait()
        if rc != 0 or not rows:
            print(f"  BTC-e {ym}: DOWNLOAD FAILED rc {rc} - nothing written", flush=True)
            continue
        d = pd.DataFrame(rows, columns=["time", "bid", "ask"])
        d["time"] = pd.to_datetime(d["time"], utc=True)
        d = d.drop_duplicates("time").sort_values("time")
        d["t"] = d["time"].dt.floor("h")
        h = d.groupby("t").agg(bid=("bid", "last"), ask=("ask", "last"), n=("bid", "size")).reset_index()
        h.to_parquet(out, index=False)
        print(f"  BTC-e {ym}: {len(d):,} snapshots -> {len(h)} hours, crossed/empty dropped {crossed}", flush=True)


# ---------------------------------------------------------------- loaders: mids at end of bar t
def trade(venue, coin):
    p = os.path.join(SPOT, f"{venue}_{coin}.parquet")
    if not os.path.exists(p):
        return None
    s = pd.read_parquet(p, columns=["t", "close"]).set_index("t")["close"]
    return s[s.index < SEAL]


def mids_A(coin):
    q = pd.read_parquet(os.path.join(ROOT, "data", "quotes", f"binance_quotes_minute_{coin}.parquet"),
                        columns=["t", "bid_last", "ask_last"])
    q = q[q.t.dt.minute == 59]
    return pd.Series(((q.bid_last + q.ask_last) / 2).values, index=q.t - pd.Timedelta(minutes=59))


def mids_B(coin):
    f = pd.read_parquet(os.path.join(ROOT, "data", "ftmo", f"ftmo_h1_{coin}.parquet"), columns=["t", "mid_close", "zero_spread"])
    f = f[(f.t >= pd.Timestamp("2022-01-01", tz="UTC")) & ~f.zero_spread]
    return f.set_index("t")["mid_close"]


def mids_C(coin):
    b = pd.read_parquet(os.path.join(ROOT, "bitmex_hourly_sample.parquet"))
    root = "XBT" if coin == "BTCUSD" else coin[:-3]
    b = b[(b.coin == coin) & b.sym.isin([root + "USD", root + "USDT"])]          # perpetuals only
    return b.drop_duplicates("hour").set_index("hour")["mid_usd"]


def mids_D():
    fs = sorted(os.listdir(BTCE_DIR)) if os.path.isdir(BTCE_DIR) else []
    if not fs:
        return None
    d = pd.concat(pd.read_parquet(os.path.join(BTCE_DIR, f)) for f in fs)
    return pd.Series(((d.bid + d.ask) / 2).values, index=d.t)


# ---------------------------------------------------------------- compare
def compare(check, venue, coin, close, mid, same_venue):
    j = pd.concat([close.rename("c"), mid.rename("m")], axis=1, join="inner").dropna()
    j = j[j.index < SEAL]
    out = []
    for y, g in j.groupby(j.index.year):
        if len(g) < 20:
            continue
        gap = (g.c / g.m - 1) * 1e4
        off = gap.median()
        dev = gap.abs() if same_venue else (gap - off).abs()
        cons = g.index.to_series().diff() == pd.Timedelta(hours=1)
        rc, rm = np.log(g.c).diff()[cons], np.log(g.m).diff()[cons]
        days = []
        for _, gd in g.groupby(g.index.normalize()):
            a, b = gd[gd.index.hour == 0], gd[gd.index.hour == 23]
            if len(a) and len(b):
                days.append(abs((b.c.iloc[0] / a.c.iloc[0]) - (b.m.iloc[0] / a.m.iloc[0])) * 1e4)
        dd = float(np.median(days)) if days else np.nan
        lim = 2.5 if same_venue else 10.0
        ok = (dev.median() <= lim) and (dd <= 5.0) if days else (dev.median() <= lim)
        out.append(dict(check=check, venue=venue, coin=coin, year=y, hours=len(g), days=len(days),
                        gap_bp=round(off, 2), gap_med=round(dev.median(), 2), gap_p90=round(dev.quantile(0.9), 2),
                        hr_corr=round(rc.corr(rm), 4) if cons.sum() > 10 else np.nan,
                        day_diff_bp=round(dd, 2) if days else np.nan,
                        PASS="yes" if ok else "NO" + ("" if days else " (no full days)")))
    return out


def main():
    if "--analyse-only" not in sys.argv:
        print("fetching BTC-e (streamed, one month at a time)", flush=True)
        btce_fetch()
    rows = []
    for coin in COINS:
        for venue in ("binance", "coinbase", "bitstamp"):
            c = trade(venue, coin)
            if c is None:
                continue
            if venue == "binance":
                rows += compare("A same-venue", venue, coin, c, mids_A(coin), True)
            if coin != "DOTUSD":
                rows += compare("B vs FTMO", venue, coin, c, mids_B(coin), False)
            rows += compare("C vs BitMEX perp", venue, coin, c, mids_C(coin), False)
            if coin == "BTCUSD" and venue in ("bitstamp", "coinbase"):
                md = mids_D()
                if md is not None:
                    rows += compare("D vs BTC-e", venue, coin, c, md, False)
    r = pd.DataFrame(rows)
    r.to_csv(os.path.join(ROOT, "price_vs_mid.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    print(r.to_string(index=False))
    print("\nPASS COUNT by venue x coin (years passing / years tested):")
    s = r.assign(p=r.PASS.eq("yes")).groupby(["venue", "coin"]).p.agg(lambda x: f"{x.sum()}/{len(x)}")
    print(s.unstack(0).to_string())


if __name__ == "__main__":
    main()
