"""BVOL implied-vol index, resampled to 1h per daily file as it downloads (raw archive is per-second -> OOM)."""
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from lib import client, log_fail, save
from p2_perps import fetch_csv, list_keys, to_ts_mixed


def one(cli, key):
    df = fetch_csv(cli, key)
    if df is None or not len(df):
        return None
    t = to_ts_mixed(df["calc_time"])
    v = pd.to_numeric(df["index_value"])
    s = pd.Series(v.values, index=t).sort_index()
    o = s.resample("1h").agg(["first", "max", "min", "last", "count"])
    return o.rename(columns={"first": "open", "max": "high", "min": "low", "last": "close", "count": "n_obs"})


if __name__ == "__main__":
    with client() as cli, ThreadPoolExecutor(12) as pool:
        for s in ["BTCBVOLUSDT", "ETHBVOLUSDT"]:
            try:
                keys = list_keys(cli, f"data/option/daily/BVOLIndex/{s}/")
                parts = [p for p in pool.map(lambda k: one(cli, k), keys) if p is not None]
                df = pd.concat(parts).groupby(level=0).agg(
                    {"open": "first", "high": "max", "low": "min", "close": "last", "n_obs": "sum"})
                df = df[df["n_obs"] > 0].reset_index(names="t")
                save(df, "perp", f"bvol_{s[:3]}", "t", dict(
                    source=f"Binance options BVOLIndex {s}", freq="1h (resampled from raw ticks)",
                    type="implied-vol index OHLC", stamp="UTC hour open", knowable="hour end",
                    notes="n_obs = raw index prints inside the hour."))
            except Exception as e:
                log_fail("perp", f"bvol_{s}", e)
    print("DONE p2b_bvol", file=sys.stderr)
