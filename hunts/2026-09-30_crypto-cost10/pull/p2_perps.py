"""Family `perp`: Binance USD-M perpetual archives from data.binance.vision (bulk zips; fapi is geo-blocked).

perp_klines_<SYM>   1h trade-print OHLCV of the perp.                         knowable open+1h
perp_premium_<SYM>  1h premium index klines = (perp - index)/index -> the BASIS. Mechanism: leverage demand;
                    a rich perp means longs are paying up, arbitrageurs short it and it mean-reverts.
funding_<SYM>       8h (later 4h/1h on some coins) realised funding. Mechanism: crowded side pays to stay in;
                    extremes precede forced deleveraging (#045 on BTC; cross-section never tested).
metrics_<SYM>       5m open interest, top-trader and all-account long/short ratios, taker buy/sell volume ratio.
                    Mechanism: positioning fragility - OI built into a move is fuel for a liquidation cascade.
bvol_<X>            Binance BVOL implied-vol index (options-implied, BTC/ETH).
Archive timestamps switch ms -> microseconds partway through (alpha_log #044 note): detected from magnitude.
"""
import io
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from lib import COINS, client, get, log_fail, save

S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
DL = "https://data.binance.vision/"


def list_keys(cli, prefix):
    keys, marker = [], ""
    while True:
        r = get(cli, S3, {"prefix": prefix, "marker": marker}, as_json=False)
        txt = r.text
        ks = re.findall(r"<Key>([^<]+\.zip)</Key>", txt)
        keys += ks
        if "<IsTruncated>true</IsTruncated>" not in txt:
            break
        marker = re.findall(r"<Key>([^<]+)</Key>", txt)[-1]
    return keys


def fetch_csv(cli, key, names=None):
    r = get(cli, DL + key, as_json=False)
    if r is None:
        return None
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        raw = z.read(z.namelist()[0]).decode()
    df = pd.read_csv(io.StringIO(raw), header=None)
    first = str(df.iloc[0, 0])
    if not re.match(r"^-?\d", first):  # header row present
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    elif names:
        df.columns = names[: df.shape[1]]
    return df


def to_ts(s):
    s = pd.to_numeric(s)
    unit = "us" if s.max() > 1e14 else "ms"
    return pd.to_datetime(s, unit=unit, utc=True)


def to_ts_mixed(s):
    s = pd.to_numeric(s)
    out = pd.to_datetime(s.where(s < 1e14, s // 1000), unit="ms", utc=True)
    return out


KL = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count",
      "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def pull_series(cli, pool, prefixes, names):
    keys = []
    for p in prefixes:
        keys += list_keys(cli, p)
    if not keys:
        return None
    dfs = list(pool.map(lambda k: fetch_csv(cli, k, names), keys))
    dfs = [d for d in dfs if d is not None and len(d)]
    return pd.concat(dfs, ignore_index=True) if dfs else None


def job(kind, base, pool):
    sym = base + "USDT"
    ftmo = base + "USD"
    try:
        with client() as cli:
            if kind in ("klines", "premiumIndexKlines"):
                df = pull_series(cli, pool, [f"data/futures/um/monthly/{kind}/{sym}/1h/",
                                             f"data/futures/um/daily/{kind}/{sym}/1h/{sym}-1h-2026-09"], KL)
                if df is None:
                    return log_fail("perp", f"{kind}_{sym}", "no files")
                df = df.drop(columns=[c for c in ["ignore", "close_time"] if c in df.columns])
                df["t"] = to_ts_mixed(df.pop("open_time"))
                for c in df.columns:
                    if c != "t":
                        df[c] = pd.to_numeric(df[c])
                df = df.drop_duplicates("t")
                name = "perp_klines" if kind == "klines" else "perp_premium"
                prov = dict(source=f"Binance USD-M perp {sym} ({kind})", freq="1h", stamp="UTC bar open",
                            knowable="open + 1h",
                            type="trade print" if kind == "klines" else "index: (perp mark - spot index)/index, OHLC",
                            notes="Monthly archive + daily files for the current month.")
                save(df, "perp", f"{name}_{ftmo}", "t", prov)
            elif kind == "fundingRate":
                df = pull_series(cli, pool, [f"data/futures/um/monthly/fundingRate/{sym}/"],
                                 ["calc_time", "funding_interval_hours", "last_funding_rate"])
                if df is None:
                    return log_fail("perp", f"funding_{sym}", "no files")
                df["t"] = to_ts_mixed(df.pop("calc_time"))
                for c in df.columns:
                    if c != "t":
                        df[c] = pd.to_numeric(df[c])
                save(df, "perp", f"funding_{ftmo}", "t", dict(
                    source=f"Binance USD-M {sym} fundingRate archive", freq="8h (4h/1h on some coins later)",
                    type="realised funding rate (fraction per interval)", stamp="UTC settlement time",
                    knowable="at settlement; the predicted rate is visible live before it",
                    notes="Monthly archive only: the current month is not in it yet."))
            elif kind == "metrics":
                df = pull_series(cli, pool, [f"data/futures/um/daily/metrics/{sym}/"], None)
                if df is None:
                    return log_fail("perp", f"metrics_{sym}", "no files")
                df["t"] = pd.to_datetime(df.pop("create_time"), utc=True)
                df = df.drop(columns=["symbol"], errors="ignore")
                for c in df.columns:
                    if c != "t":
                        df[c] = pd.to_numeric(df[c], errors="coerce")
                save(df, "perp", f"metrics_{ftmo}", "t", dict(
                    source=f"Binance USD-M {sym} daily metrics archive", freq="5m",
                    type="exchange-computed positioning stats", stamp="UTC create_time (snapshot time)",
                    knowable="create_time (a few seconds after)",
                    notes="OI in base and USD; long/short = accounts ratio; taker ratio = buy/sell taker volume."))
    except Exception as e:
        log_fail("perp", f"{kind}_{sym}", e)


def bvol(pool):
    with client() as cli:
        for s in ["BTCBVOLUSDT", "ETHBVOLUSDT"]:
            try:
                df = pull_series(cli, pool, [f"data/option/daily/BVOLIndex/{s}/"], None)
                df["t"] = to_ts_mixed(df.pop("calc_time"))
                df["index_value"] = pd.to_numeric(df["index_value"])
                df = df[["t", "index_value"]]
                save(df, "perp", f"bvol_{s[:3]}", "t", dict(
                    source=f"Binance options BVOLIndex {s}", freq="as archived (sub-hourly)",
                    type="implied-vol index", stamp="UTC calc_time", knowable="calc_time", notes=""))
            except Exception as e:
                log_fail("perp", f"bvol_{s}", e)


if __name__ == "__main__":
    pool = ThreadPoolExecutor(24)
    outer = ThreadPoolExecutor(4)
    jobs = [(k, COINS[c][0]) for k in ["klines", "premiumIndexKlines", "fundingRate", "metrics"] for c in COINS]
    list(outer.map(lambda j: job(j[0], j[1], pool), jobs))
    bvol(pool)
    print("DONE p2_perps", file=sys.stderr)
