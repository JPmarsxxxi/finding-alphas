"""p9 - FTMO MT5 history depth per coin (EDA#2). Read-only, no prices.

Requests history the way the Strategy Tester does, so the terminal downloads it from the
server on demand. Span = last 20 years; light touch: H1 full range,
M1 and ticks one 1-hour window per month with a pause between requests; seals are cut AFTER the full pull, not here.
Output = timestamps and counts only.

Probes:
  clock   server-time offset vs UTC, from the latest live tick (crypto quotes 24/7)
  H1      copy_rates_range over the 20-year span -> first bar, count
  M1/ticks 1-hour windows (12:00 server, day 15): yearly, then monthly near the first hit,
          and whether those ticks carry BOTH bid and ask
"""
import sys, time
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import MetaTrader5 as mt5

SYMS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD",
        "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
START = datetime(datetime.now().year - 20, 1, 1, tzinfo=timezone.utc)   # 20 years is enough
PAUSE = 0.3   # seconds between server requests - don't hammer the FTMO history server
CUTOFF = datetime.now(timezone.utc) + pd.Timedelta(hours=12)   # server clock runs ahead of UTC
OUT = __file__.replace("pull\\p9_mt5_depth.py", "mt5_depth.csv").replace("pull/p9_mt5_depth.py", "mt5_depth.csv")


def ts(x):
    return pd.Timestamp(int(x), unit="s").strftime("%Y-%m-%d %H:%M")


def h1_depth(s, maxbars):
    r = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_H1, 0, maxbars - 1)
    if r is None or not len(r):
        return None, None, 0, {}, len(r) if r is not None else 0
    t = pd.to_datetime(r["time"], unit="s")
    per_year = t.year.value_counts().sort_index().to_dict()
    return ts(r["time"][0]), ts(r["time"][-1]), len(r), per_year, len(r) >= maxbars - 1   # True = capped by maxbars


def rates_depth(s, tf):
    r = None
    for _ in range(3):                      # first call may only trigger the download
        r = mt5.copy_rates_range(s, tf, START, CUTOFF)
        if r is not None and len(r):
            break
        time.sleep(2)
    if r is None or len(r) == 0:
        return None, None, 0
    return ts(r["time"][0]), ts(r["time"][-1]), len(r)


def _probe(s, kind, m):
    """one 1-hour window at 12:00 on the 15th of month m; returns the array or None"""
    a = (m + pd.Timedelta(days=14, hours=12)).to_pydatetime().replace(tzinfo=timezone.utc)
    if kind == "M1":
        r = mt5.copy_rates_range(s, mt5.TIMEFRAME_M1, a, a + pd.Timedelta(hours=1))
    else:
        r = mt5.copy_ticks_range(s, a, a + pd.Timedelta(hours=1), mt5.COPY_TICKS_ALL)
    time.sleep(PAUSE)
    if r is None or not len(r):
        return None
    lo = int(a.timestamp())
    r = r[(r["time"] >= lo) & (r["time"] < lo + 3600)]   # MT5 returns the NEAREST bar when the window is empty
    return r if len(r) else None


def first_month(s, kind):
    """coarse-to-fine: one probe per year (January), then month by month across the year before
    the first January hit and that year itself. Also reports how many yearly probes hit (gaps)."""
    years = pd.date_range(START.strftime("%Y-01-01"), pd.Timestamp.now(), freq="YS")
    hits = [y for y in years if _probe(s, kind, y) is not None]
    if not hits:
        return None, None, f"0/{len(years)}"
    y0 = hits[0]
    for m in pd.date_range(y0 - pd.DateOffset(years=1), y0, freq="MS"):
        r = _probe(s, kind, m)
        if r is not None:
            extra = float(((r["bid"] > 0) & (r["ask"] > 0)).mean()) if kind == "ticks" else None
            return m.strftime("%Y-%m"), extra, f"{len(hits)}/{len(years)}"
    return y0.strftime("%Y-%m"), None, f"{len(hits)}/{len(years)}"


def main():
    if not mt5.initialize():
        print("MT5 initialize FAILED:", mt5.last_error()); return 1
    a = mt5.account_info()
    ti = mt5.terminal_info()
    if a is None:
        print("terminal up but NO ACCOUNT:", mt5.last_error()); mt5.shutdown(); return 1
    print(f"account {a.login}  server {a.server}  terminal maxbars {ti.maxbars:,}")

    for s in SYMS:
        mt5.symbol_select(s, True)
    time.sleep(1.5)

    # clock: latest live tick time (server clock, stored as if UTC) minus true UTC now
    offs = []
    for s in ["BTCUSD", "ETHUSD"]:
        tk = mt5.symbol_info_tick(s)
        if tk:
            offs.append((tk.time - time.time()) / 3600)
    print("server clock offset vs UTC (h): " + ", ".join(f"{o:+.2f}" for o in offs))

    rows, h1_years = [], {}
    for s in SYMS:
        i = mt5.symbol_info(s)
        h1 = h1_depth(s, ti.maxbars)
        h1_years[s] = h1[3]
        m1 = first_month(s, "M1")
        tk = first_month(s, "ticks")
        rows.append(dict(symbol=s, digits=i.digits if i else None, point=i.point if i else None,
                         H1_first=h1[0], H1_last=h1[1], H1_n=h1[2], H1_capped=h1[4],
                         M1_first_month=m1[0], M1_years_hit=m1[2],
                         tick_first_month=tk[0], tick_two_sided_frac=tk[1], tick_years_hit=tk[2]))
        print(f"  {s} done", flush=True)
    mt5.shutdown()

    d = pd.DataFrame(rows)
    pd.set_option("display.width", 220)
    print("\nFTMO MT5 DEPTH (last 20 years; counts and timestamps only, server clock)")
    print(d.to_string(index=False))
    d.to_csv(OUT, index=False)
    y = pd.DataFrame(h1_years).fillna(0).astype(int).sort_index()
    print("\nH1 bars per year (24/7 full year = 8760; server clock)")
    print(y.to_string())
    y.to_csv(OUT.replace(".csv", "_h1_by_year.csv"))
    print(f"\n[saved] {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
