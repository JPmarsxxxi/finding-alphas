"""p13 - Does BitMEX (free two-sided quotes, 2014-11 ->) give the same figures as spot? (EDA#2, data-hygiene rule 12)

Source: public.bitmex.com/data/quote/YYYYMMDD.csv.gz - every best bid/ask change, all instruments, UTC timestamps.
Sample: the 15th of each month, 2014-12 .. 2023-11 (explore side only - nothing past the 2023-11-30 seal).
Each day is streamed (curl | gzip | grep for our 10 roots), reduced to hourly rows, and the raw text deleted.

Contract chosen per coin per day: the USD/USDT perpetual if quoted that day, else the most-quoted contract on that
root. Contracts priced in XBT (ETHXBT, ETHZ17, LTCZ17, XRPH18, BCHF18, ADAH19 ...) are converted to USD with the XBT
contract's mid in the same hour (both two-sided).
Hourly row = LAST quote in the hour (a mid knowable at hour end), labelled by hour OPEN (matches spot files).

Validation vs spot (reference priority: Coinbase USD > Bitstamp USD (BTC) > Binance USDT), per coin x year:
  ret_corr     correlation of hourly mid-to-mid returns vs spot hourly close returns      (same moves?)
  best_shift   shift in hours (-2..+2) that maximises that correlation                  (same clock? should be 0)
  basis_bp     median of (BitMEX mid / spot close - 1), bp                              (futures premium / USDT gap)
  |basis| p90  bp
  spread_bp    BitMEX median full spread, bp
Spot closes are last trades (0.1-3 bp off mid, measured in quotes_verification.csv) - small next to any basis.
"""
import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "bitmex_sample")
TMP = os.path.join(OUT, "_tmp.csv")
GITBASH = r"C:\Program Files\Git\usr\bin\bash.exe"     # NOT plain "bash" - on this machine that resolves to WSL
URL = "https://s3-eu-west-1.amazonaws.com/public.bitmex.com/data/quote/{}.csv.gz"
ROOTS = {"XBT": "BTCUSD", "ETH": "ETHUSD", "LTC": "LTCUSD", "XRP": "XRPUSD", "BCH": "BCHUSD",
         "ADA": "ADAUSD", "DOGE": "DOGEUSD", "SOL": "SOLUSD", "DOT": "DOTUSD", "BNB": "BNBUSD"}
DAYS = pd.date_range("2014-12-01", "2023-11-01", freq="MS") + pd.Timedelta(days=14)


def root_of(sym):
    for r in sorted(ROOTS, key=len, reverse=True):
        if sym.startswith(r):
            return r
    return None


def usd_quoted(sym, root):
    rest = sym[len(root):]
    return root == "XBT" or rest.startswith("USD")       # XBT* are USD-priced; ETHXBT / ETHZ17 / ADAH19 are XBT-priced


def fetch_day(day):
    out = os.path.join(OUT, f"{day:%Y%m%d}.parquet")
    if os.path.exists(out):
        return "skip"
    pat = "^[^,]*,(" + "|".join(ROOTS) + ")[A-Z0-9]*,"
    tmp = TMP.replace("\\", "/")
    cmd = (f"curl -sf --max-time 900 '{URL.format(f'{day:%Y%m%d}')}' | gzip -dc | grep -E '{pat}' > '{tmp}'; "
           f"exit ${{PIPESTATUS[0]}}")
    rc = subprocess.run([GITBASH, "-c", cmd], check=False).returncode
    if rc != 0:                                   # download failed: write NOTHING, so a re-run retries this day
        if os.path.exists(TMP):
            os.remove(TMP)
        return f"DOWNLOAD FAILED (curl rc {rc})"
    if os.path.getsize(TMP) == 0:
        pd.DataFrame().to_parquet(out); return "no coin quotes that day"
    rows = []
    for ch in pd.read_csv(TMP, header=None, usecols=[0, 1, 3, 4], names=["ts", "sym", "bid", "ask"],
                          chunksize=500_000):
        ch = ch[(ch.bid > 0) & (ch.ask >= ch.bid) & ~ch.sym.str.contains("_")]
        ch["t"] = pd.to_datetime(ch.ts.str.replace("D", "T", regex=False).str[:26], utc=True)
        ch["hour"] = ch.t.dt.floor("h")
        g = ch.groupby(["sym", "hour"])
        rows.append(pd.DataFrame({"bid": g.bid.last(), "ask": g.ask.last(), "n": g.size(), "t_last": g.t.max()}))
    os.remove(TMP)
    d = pd.concat(rows).reset_index()
    d = d.sort_values("t_last").groupby(["sym", "hour"]).agg(bid=("bid", "last"), ask=("ask", "last"),
                                                             n=("n", "sum")).reset_index()
    d.to_parquet(out, index=False)
    return f"{len(d)} rows"


def pick(day_df):
    """one contract per root per day, converted to USD; returns hourly rows"""
    if day_df.empty:
        return []
    day_df = day_df.assign(root=day_df.sym.map(root_of), mid=(day_df.bid + day_df.ask) / 2)
    day_df["sp_bp"] = (day_df.ask - day_df.bid) / day_df.mid * 1e4
    act = day_df.groupby("sym").n.sum()
    chosen = {}
    for r in ROOTS:
        cands = [s for s in act.index if root_of(s) == r]
        if not cands:
            continue
        perp = [s for s in cands if s in (r + "USD", r + "USDT")]
        chosen[r] = perp[0] if perp else act[cands].idxmax()
    xbt = day_df[day_df.sym == chosen.get("XBT", "")].set_index("hour").mid
    out = []
    for r, s in chosen.items():
        x = day_df[day_df.sym == s].set_index("hour")
        mid = x.mid if usd_quoted(s, r) else x.mid * xbt.reindex(x.index)
        out.append(pd.DataFrame({"coin": ROOTS[r], "sym": s, "usd_quoted": usd_quoted(s, r),
                                 "hour": x.index, "mid_usd": mid.values, "spread_bp": x.sp_bp.values}))
    return out


def spot(coin):
    refs = []
    for venue, f in (("coinbase", f"coinbase_{coin}"), ("bitstamp", f"bitstamp_{coin}"), ("binance", f"binance_{coin}")):
        p = os.path.join(ROOT, "data", "spot", f + ".parquet")
        if os.path.exists(p):
            s = pd.read_parquet(p, columns=["t", "close"]).set_index("t")["close"]
            refs.append(s.rename(venue))
    return pd.concat(refs, axis=1) if refs else None


def analyse():
    frames = []
    for day in DAYS:
        p = os.path.join(OUT, f"{day:%Y%m%d}.parquet")
        if os.path.exists(p):
            frames += pick(pd.read_parquet(p))
    h = pd.concat(frames)
    h.to_parquet(os.path.join(ROOT, "bitmex_hourly_sample.parquet"), index=False)
    res = []
    for coin, g in h.groupby("coin"):
        sp = spot(coin)
        g = g.set_index("hour").sort_index()
        for y, gy in g.groupby(g.index.year):
            ref_name, ref = None, None
            for v in ("coinbase", "bitstamp", "binance"):
                if sp is not None and v in sp and sp[v].reindex(gy.index).notna().mean() > 0.8:
                    ref_name, ref = v, sp[v]; break
            row = dict(coin=coin, year=y, days=gy.index.normalize().nunique(), hours=len(gy),
                       contracts=",".join(sorted(set(gy.sym)))[:40], xbt_priced=f"{100 * (~gy.usd_quoted).mean():.0f}%",
                       spread_bp=round(gy.spread_bp.median(), 2), ref=ref_name or "none")
            if ref is not None:
                # BitMEX row stamped hour OPEN holds the LAST quote of that hour -> compare with spot close of the same bar
                b = gy.mid_usd
                s = ref.reindex(gy.index)
                same_day = gy.index.to_series().diff() == pd.Timedelta(hours=1)
                rb = np.log(b).diff()[same_day]
                corr = {k: rb.corr(np.log(ref).diff().shift(k).reindex(rb.index)) for k in range(-2, 3)}
                basis = (b / s - 1) * 1e4
                row.update(ret_corr=round(corr[0], 3), best_shift=max(corr, key=lambda k: -9 if pd.isna(corr[k]) else corr[k]),
                           basis_bp=round(basis.median(), 1), abs_basis_p90=round(basis.abs().quantile(0.9), 1))
            res.append(row)
    r = pd.DataFrame(res)
    r.to_csv(os.path.join(ROOT, "bitmex_vs_spot.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    print(r.to_string(index=False))


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--analyse-only" not in sys.argv:
        for day in DAYS:
            t0 = time.time()
            st = fetch_day(day)
            print(f"  {day:%Y-%m-%d} {st} ({time.time() - t0:.0f}s)", flush=True)
    analyse()


if __name__ == "__main__":
    main()
