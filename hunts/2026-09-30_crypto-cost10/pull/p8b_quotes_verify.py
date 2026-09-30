"""Combine the Tardis first-of-month quote days per coin, verify them against Binance's own 1h trade bars, and draw the
spread-by-hour profile (data-hygiene.md checklist). Explore side only (all days <= 2023-03-01)."""
import glob
import os

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from lib import DATA, ROOT, save  # noqa: E402

Q = os.path.join(DATA, "quotes_minute")
COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
rows, prof = [], {}
for c in COINS:
    q = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(Q, f"{c}_*.parquet")))], ignore_index=True)
    q["t"] = pd.to_datetime(q["t"], utc=True)
    save(q, "quotes", f"binance_quotes_minute_{c}", "t", dict(
        source=f"Tardis.dev binance quotes (bookTicker), {c[:-3]}USDT, first day of each month", freq="1 min (from ticks)",
        type="MEASURED best bid/ask; half_bp_tw = time-weighted half-spread bp", stamp="UTC minute START (Tardis receipt time)",
        knowable="minute end", notes="Free tier samples only the 1st of each month, 2019-04 .. 2023-03."))
    k = pd.read_parquet(os.path.join(DATA, "spot", f"binance_{c}.parquet"))[["t", "close"]]
    k["t_end"] = k["t"] + pd.Timedelta("1h")                  # bar close time
    ql = q.set_index("t")
    # the last quote of the bar's final minute (minute starting at t_end - 1 min)
    last = ql.reindex(k["t_end"] - pd.Timedelta("1min"))[["bid_last", "ask_last"]].set_axis(k.index)
    m = k.join(last).dropna(subset=["bid_last"])
    tick = (m["ask_last"] - m["bid_last"]).clip(lower=1e-12)
    inside = (m["close"] >= m["bid_last"] - tick) & (m["close"] <= m["ask_last"] + tick)
    mid = (m["bid_last"] + m["ask_last"]) / 2
    dev = (m["close"] / mid - 1).abs() * 1e4
    rows.append({"coin": c, "days": q["t"].dt.floor("D").nunique(), "hours_matched": len(m),
                 "close_within_bid_ask_pm1spread": round(float(inside.mean()), 3),
                 "median_|close-mid|_bp": round(float(dev.median()), 3),
                 "median_half_bp": round(float(q["half_bp_tw"].median()), 3),
                 "p90_half_bp": round(float(q["half_bp_tw"].quantile(0.9)), 3)})
    prof[c] = q.groupby(q["t"].dt.hour)["half_bp_tw"].median()
res = pd.DataFrame(rows)
res.to_csv(os.path.join(ROOT, "quotes_verification.csv"), index=False)
print(res.to_string(index=False))
P = pd.DataFrame(prof)
P.to_csv(os.path.join(ROOT, "quotes_hour_profile.csv"))
print("\nmedian half-spread (bp) by UTC hour, 00/01/12/21/22/23:\n", P.loc[[0, 1, 12, 21, 22, 23]].round(3).to_string())

PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
fig, ax = plt.subplots(figsize=(10, 4.2), facecolor="#fcfcfb")
ax.set_facecolor("#fcfcfb")
Pn = P / P.median()
for i, c in enumerate(COINS[:8]):
    ax.plot(Pn.index, Pn[c], color=PAL[i], lw=1.6, label=c)
for c in COINS[8:]:
    ax.plot(Pn.index, Pn[c], color="#9b9a94", lw=1.0, ls="--", label=c + " (grey)")
for h in (0, 21, 22):
    ax.axvline(h, color="#52514e", lw=0.7, ls=":")
ax.set_xlabel("UTC hour (dotted: 00 = strategy entry/exit; 21/22 = FTMO rollover)", color="#52514e")
ax.set_ylabel("median half-spread / coin's own median", color="#52514e")
ax.set_title("Measured Binance spot half-spread by hour (Tardis, 1st of month 2019-04..2023-03)", loc="left", fontsize=11)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(ncol=5, fontsize=7.5, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(ROOT, "quotes_hour_profile.png"), dpi=130)
