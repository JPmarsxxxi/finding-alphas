"""p10 - Family `ftmo`: FTMO MT5 hourly bars for the 10 crypto CFDs, with FTMO's own spread (EDA#2).

Provenance (data-hygiene "one sentence"): these prices are BID-side OHLC from FTMO's MT5 server (FTMO-Demo),
timestamped at bar OPEN on the server clock (America/New_York + 7h), knowable at bar open + 1h; `spread` is
MT5's per-bar spread in points (one figure for the whole hour - its exact definition is the broker's, so the
built mid is APPROXIMATE until checked against FTMO ticks).

  mid_* = bid_* + spread_price / 2          (approximate mid, rule 1)
  spread_bp = spread_price / mid_close * 1e4 (full spread, bp of mid)

Pulled the way the Strategy Tester asks for history (copy_rates_from_pos, under the terminal's maxbars), FULL span,
then cut at the EDA#2 seal (2023-11-30 23:59 UTC): explore rows -> data/ftmo/, later rows -> data/_sealed/ftmo/.
The sealed side is written and counted, never summarised.

Hygiene gates, counts logged per coin (rules 8-11, 14):
  time    server -> UTC via NY+7h; DST-ambiguous / non-existent hours set NaT and DROPPED (counted)
  dups    exact duplicate rows; same timestamp with different values (kept: first; counted)
  bad     bid <= 0, high < low, spread < 0  -> deleted (counted); spread == 0 -> flagged (counted), kept
  gaps    left missing, never filled
Clock check (rule 8 - measured, not assumed): per explore year, correlation of FTMO hourly mid returns with Binance
hourly close returns at shifts -3..+3 h; the best shift should be 0 in every year.
"""
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import MetaTrader5 as mt5

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXP = os.path.join(ROOT, "data", "ftmo")
SEAL = os.path.join(ROOT, "data", "_sealed", "ftmo")
REG = os.path.join(ROOT, "data", "registry.jsonl")
SEAL_AT = pd.Timestamp("2023-12-01", tz="UTC")          # rows >= this are sealed
SYMS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD",
        "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]


def to_utc(server_sec):
    """MT5 returns server wall-clock seconds as if UTC. Server = NY + 7h -> NY wall clock -> UTC."""
    ny_wall = pd.to_datetime(server_sec, unit="s") - pd.Timedelta(hours=7)
    return pd.DatetimeIndex(ny_wall).tz_localize("America/New_York", ambiguous="NaT",
                                                 nonexistent="NaT").tz_convert("UTC")


def pull(s, maxbars):
    r = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_H1, 0, maxbars - 1)
    if r is None or not len(r):
        return None, {"error": str(mt5.last_error())}
    d = pd.DataFrame(r)
    log = {"rows_raw": len(d), "capped_by_maxbars": len(d) >= maxbars - 1}
    point = mt5.symbol_info(s).point

    d["t"] = to_utc(d["time"].values)
    log["dst_nat_dropped"] = int(d["t"].isna().sum())
    d = d[d["t"].notna()]

    n0 = len(d); d = d.drop_duplicates(); log["exact_dups"] = n0 - len(d)
    n0 = len(d); d = d.drop_duplicates("t", keep="first"); log["same_t_diff_values"] = n0 - len(d)

    bad = (d[["open", "high", "low", "close"]] <= 0).any(axis=1) | (d.high < d.low) | (d.spread < 0)
    log["impossible_deleted"] = int(bad.sum()); d = d[~bad]
    log["zero_spread_flagged"] = int((d.spread == 0).sum())

    sp = d["spread"] * point
    out = pd.DataFrame({"t": d["t"].values,
                        "bid_open": d.open.values, "bid_high": d.high.values,
                        "bid_low": d.low.values, "bid_close": d.close.values,
                        "spread_pts": d.spread.values, "tick_volume": d.tick_volume.values})
    out["t"] = pd.to_datetime(out["t"], utc=True)        # .values drops the tz label; the instants are already UTC
    out["mid_open"] = out.bid_open + sp.values / 2
    out["mid_close"] = out.bid_close + sp.values / 2
    out["spread_bp"] = sp.values / out.mid_close * 1e4
    out["zero_spread"] = out.spread_pts == 0
    out = out.sort_values("t").reset_index(drop=True)
    log["rows_clean"] = len(out)
    return out, log


def clock_check(s, f):
    """best UTC shift of FTMO vs Binance hourly returns, per explore year"""
    b = pd.read_parquet(os.path.join(ROOT, "data", "spot", f"binance_{s}.parquet"), columns=["t", "close"])
    rb = np.log(b.set_index("t")["close"]).diff()
    rf = np.log(f.set_index("t")["mid_close"]).diff()
    res = {}
    for y in sorted(set(rf.index.year)):
        a = rf[rf.index.year == y]
        best = max(range(-3, 4), key=lambda k: a.corr(rb.shift(k).reindex(a.index)) if a.notna().sum() > 100 else -9)
        c0 = a.corr(rb.reindex(a.index))
        res[y] = (best, round(c0, 3) if pd.notna(c0) else None)
    return res


def main():
    os.makedirs(EXP, exist_ok=True); os.makedirs(SEAL, exist_ok=True)
    if not mt5.initialize():
        print("MT5 initialize FAILED:", mt5.last_error()); return 1
    a, ti = mt5.account_info(), mt5.terminal_info()
    print(f"account {a.login}  server {a.server}  maxbars {ti.maxbars:,}")

    logs, per_year, spread_year, clocks = {}, {}, {}, {}
    for s in SYMS:
        mt5.symbol_select(s, True); time.sleep(0.5)
        d, log = pull(s, ti.maxbars)
        logs[s] = log
        if d is None:
            print(f"  {s}: NO DATA {log}"); continue
        exp, sea = d[d.t < SEAL_AT], d[d.t >= SEAL_AT]
        exp.to_parquet(os.path.join(EXP, f"ftmo_h1_{s}.parquet"), index=False)
        sea.to_parquet(os.path.join(SEAL, f"ftmo_h1_{s}.parquet"), index=False)
        log.update(rows_explore=len(exp), rows_sealed=len(sea))
        per_year[s] = exp.t.dt.year.value_counts().sort_index()                    # explore side only
        spread_year[s] = exp[~exp.zero_spread].groupby(exp.t.dt.year)["spread_bp"].median().round(2)
        clocks[s] = clock_check(s, exp)
        with open(REG, "a") as fh:
            fh.write(json.dumps({
                "family": "ftmo", "name": f"ftmo_h1_{s}", "rows_explore": len(exp), "rows_sealed": len(sea),
                "first": str(exp.t.min().date()) if len(exp) else None,
                "explore_last": str(exp.t.max().date()) if len(exp) else None,
                "sealed_last": str(sea.t.max().date()) if len(sea) else None,
                "columns": [c for c in d.columns if c != "t"],
                "source": f"FTMO MT5 ({a.server}) {s} H1, copy_rates_from_pos",
                "freq": "1h", "type": "BID OHLC + per-bar spread; mid = bid + spread/2 (APPROXIMATE)",
                "stamp": "UTC bar open (server NY+7h converted)", "knowable": "open + 1h",
                "notes": f"pulled {pd.Timestamp.now(tz='UTC'):%Y-%m-%d}; gate counts: " + json.dumps(log)}) + "\n")
        print(f"  {s} done", flush=True)
    mt5.shutdown()

    pd.set_option("display.width", 220)
    print("\nGATE COUNTS (per coin)")
    print(pd.DataFrame(logs).T.to_string())
    print("\nEXPLORE SIDE (<= 2023-11-30 UTC): hourly bars per year (full year = 8760)")
    print(pd.DataFrame(per_year).fillna(0).astype(int).to_string())
    print("\nFTMO median FULL spread, bp of mid, per year (explore side; zero-spread bars excluded)")
    print(pd.DataFrame(spread_year).to_string())
    print("\nCLOCK CHECK vs Binance: best shift in hours (should be 0) / corr at shift 0")
    print(pd.DataFrame({s: {y: f"{v[0]:+d} / {v[1]}" for y, v in c.items()} for s, c in clocks.items()}).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
