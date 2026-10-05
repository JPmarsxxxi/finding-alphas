"""p17 - VAL copy of p16 (opened once, user 2026-10-04, PREREG_vol_filter.md). FTMO bid/ask AT THE TRADE MINUTE (data-hygiene rule 3), for Cell 3 costs (EDA#2, user 2026-10-04: 1a 2a).

For each coin with FTMO ticks in the TRAIN window (BTC ETH XRP LTC ADA DOGE DOT; BNB/BCH/SOL ticks start 2025-05 = sealed),
each UTC day 2022-02-01 .. 2023-03-19, each entry hour k in {0,1,2,4} UTC: the quote IN FORCE at k:00:00 UTC =
the last FTMO tick at or before that instant (looked back up to 30 minutes). Output per row:
  t (UTC, = the bar-close stamp the engine trades at) | bid | ask | half_bp | quote_age_s
Server clock = America/New_York + 7h (verified p9/p10); requests are made in server wall time.
Resume-safe: one parquet per coin in data/ftmo_trade_minute/.
"""
import os
import sys
import time
from datetime import timezone

import numpy as np
import pandas as pd
import MetaTrader5 as mt5

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "ftmo_trade_minute_val")
COINS = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD", "DOGEUSD", "DOTUSD"]
KS = [0, 1, 2, 4]
DAYS = pd.date_range("2023-03-25", "2023-11-30", freq="D", tz="UTC")   # VAL only
LOOKBACK = pd.Timedelta(minutes=30)


def server_wall(t_utc):
    return (t_utc.tz_convert("America/New_York").tz_localize(None) + pd.Timedelta(hours=7)).to_pydatetime().replace(tzinfo=timezone.utc)


def main():
    os.makedirs(OUT, exist_ok=True)
    if not mt5.initialize():
        print("MT5 initialize FAILED:", mt5.last_error()); return 1
    for c in COINS:
        out = os.path.join(OUT, f"{c}.parquet")
        if os.path.exists(out):
            print(f"  {c} skip (on disk)"); continue
        mt5.symbol_select(c, True); time.sleep(0.5)
        rows = []
        for d in DAYS:
            for k in KS:
                t = d + pd.Timedelta(hours=k)
                s = server_wall(t)
                tk = mt5.copy_ticks_range(c, s - LOOKBACK.to_pytimedelta(), s, mt5.COPY_TICKS_ALL)
                if tk is None or not len(tk):
                    rows.append((t, np.nan, np.nan, np.nan, np.nan)); continue
                lim = int(s.timestamp() * 1000)
                tk = tk[(tk["time_msc"] <= lim) & (tk["bid"] > 0) & (tk["ask"] >= tk["bid"])]
                if not len(tk):
                    rows.append((t, np.nan, np.nan, np.nan, np.nan)); continue
                last = tk[-1]
                mid = (last["bid"] + last["ask"]) / 2
                rows.append((t, last["bid"], last["ask"], (last["ask"] - last["bid"]) / 2 / mid * 1e4,
                             (lim - int(last["time_msc"])) / 1000))
            time.sleep(0.02)
        d = pd.DataFrame(rows, columns=["t", "bid", "ask", "half_bp", "quote_age_s"])
        d.to_parquet(out, index=False)
        print(f"  {c}: {d.half_bp.notna().sum()}/{len(d)} trade minutes with a quote; median half {d.half_bp.median():.3f} bp, "
              f"p90 {d.half_bp.quantile(.9):.3f}; median quote age {d.quote_age_s.median():.1f}s", flush=True)
    mt5.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
