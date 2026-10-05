"""p11 - Is the FTMO hourly mid (bid + spread/2, p10) accurate? Check against FTMO's own ticks (EDA#2).

Part 1  zero-spread bars by year, per coin (from data/ftmo/, explore side only, no MT5).
Part 2  tick check. Sample = the 15th of each month, 2022-02 .. 2023-11 (explore side, ticks exist).
        One server-day at a time (memory). Bars and ticks both in raw SERVER seconds, so no tz conversion here.
        Per hour:
          bid_ok      bar close == last tick bid in the hour        (are bars really BID?)
          mid_err_bp  (bar bid_close + spread/2) - last tick mid    (how wrong is the built mid?)
          spread      bar spread vs tick spread in the hour: min / last / time-weighted mean
BNB, BCH, SOL: FTMO ticks start 2025-05 (sealed side) -> not checked.
"""
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import MetaTrader5 as mt5

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ALL = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
TICKED = ["BTCUSD", "ETHUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "DOTUSD"]
DAYS = pd.date_range("2022-02-15", "2023-11-15", freq="MS") + pd.Timedelta(days=14)
PAUSE = 0.3


def part1():
    out = {}
    for s in ALL:
        p = os.path.join(ROOT, "data", "ftmo", f"ftmo_h1_{s}.parquet")
        d = pd.read_parquet(p, columns=["t", "zero_spread"])
        if len(d):
            g = d.groupby(d.t.dt.year)["zero_spread"]
            out[s] = (100 * g.mean()).round(1).astype(str) + "% of " + g.size().astype(str)
    return pd.DataFrame(out)


def check_day(s, day, point):
    a = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    b = a + pd.Timedelta(days=1)
    lo, hi = int(a.timestamp()), int(b.timestamp())
    r = mt5.copy_rates_range(s, mt5.TIMEFRAME_H1, a, b); time.sleep(PAUSE)
    t = mt5.copy_ticks_range(s, a, b, mt5.COPY_TICKS_ALL); time.sleep(PAUSE)
    if r is None or t is None or not len(r) or not len(t):
        return []
    r = r[(r["time"] >= lo) & (r["time"] < hi)]
    tk = pd.DataFrame({"ts": t["time_msc"] / 1000.0, "bid": t["bid"], "ask": t["ask"]})
    tk = tk[(tk.bid > 0) & (tk.ask >= tk.bid)]
    rows = []
    for bar in r:
        T = int(bar["time"])
        h = tk[(tk.ts >= T) & (tk.ts < T + 3600)]
        if len(h) < 2:
            continue
        sp = (h.ask - h.bid).values
        dur = np.diff(np.append(h.ts.values, T + 3600))            # time each quote was live
        last = h.iloc[-1]
        tmid = (last.bid + last.ask) / 2
        bsp = bar["spread"] * point
        rows.append(dict(
            symbol=s, day=day.date(), hour=T,
            bid_ok=abs(bar["close"] - last.bid) <= point / 2,
            mid_err_bp=((bar["close"] + bsp / 2) - tmid) / tmid * 1e4,
            bar_sp_bp=bsp / tmid * 1e4,
            tick_min_bp=sp.min() / tmid * 1e4,
            tick_last_bp=(last.ask - last.bid) / tmid * 1e4,
            tick_tw_bp=np.average(sp, weights=np.maximum(dur, 1e-3)) / tmid * 1e4,
            bar_eq_min=abs(bsp - sp.min()) <= point / 2,
            bar_eq_last=abs(bsp - (last.ask - last.bid)) <= point / 2,
            bar_zero=bar["spread"] == 0, n_ticks=len(h)))
    return rows


def main():
    pd.set_option("display.width", 220)
    print("PART 1 - zero-spread bars, share per year (explore side)")
    print(part1().to_string())

    if not mt5.initialize():
        print("MT5 initialize FAILED:", mt5.last_error()); return 1
    rows = []
    for s in TICKED:
        mt5.symbol_select(s, True); time.sleep(0.5)
        point = mt5.symbol_info(s).point
        for day in DAYS:
            rows += check_day(s, day, point)
        print(f"  {s} done", flush=True)
    mt5.shutdown()

    d = pd.DataFrame(rows)
    d.to_csv(os.path.join(ROOT, "ftmo_h1_verification_hours.csv"), index=False)
    g = d.groupby("symbol")
    summ = pd.DataFrame({
        "days": g["day"].nunique(), "hours": g.size(),
        "bars_are_bid_%": (100 * g["bid_ok"].mean()).round(1),
        "mid_err_median_bp": g["mid_err_bp"].median().round(2),
        "|mid_err|_p90_bp": g["mid_err_bp"].apply(lambda x: x.abs().quantile(0.9)).round(2),
        "bar_spread_bp": g["bar_sp_bp"].median().round(2),
        "tick_min_bp": g["tick_min_bp"].median().round(2),
        "tick_last_bp": g["tick_last_bp"].median().round(2),
        "tick_timewtd_bp": g["tick_tw_bp"].median().round(2),
        "bar==min_%": (100 * g["bar_eq_min"].mean()).round(1),
        "bar==last_%": (100 * g["bar_eq_last"].mean()).round(1),
        "zero_bars": g["bar_zero"].sum(),
    }).reindex(TICKED)
    summ.to_csv(os.path.join(ROOT, "ftmo_h1_verification.csv"))
    print("\nPART 2 - FTMO hourly bars vs FTMO ticks (15th of each month, 2022-02 .. 2023-11)")
    print(summ.to_string())
    z = d[d.bar_zero]
    if len(z):
        print("\nzero-spread bars in the sample: what the ticks said the spread was (median bp):",
              z.groupby("symbol")["tick_tw_bp"].median().round(2).to_dict())
    return 0


if __name__ == "__main__":
    sys.exit(main())
