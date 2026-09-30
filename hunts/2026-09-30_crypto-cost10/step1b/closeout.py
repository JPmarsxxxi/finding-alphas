"""Step 1b close-out: cost gate + decay-first on H2, H7, H6. Rules: RULES.md (written first). TRAIN only (<= 2023-03-19)."""
import os

import matplotlib
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data", "spot")
TRAIN_END = pd.Timestamp("2023-03-19 23:59:59", tz="UTC")
COINS = ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD", "XRPUSD", "DOGEUSD", "ADAUSD", "LTCUSD", "BCHUSD", "DOTUSD"]
SWAP = 8.2
BLUE, GRAY, INK, INK2, SURF = "#2a78d6", "#8a8984", "#0b0b0b", "#52514e", "#fcfcfb"


def load():
    closes, vols, cost = {}, {}, {}
    for c in COINS:
        df = pd.read_parquet(os.path.join(DATA, f"binance_{c}.parquet"))
        df = df[df["t"] <= TRAIN_END].set_index("t").sort_index()
        assert df.index.max() <= TRAIN_END
        closes[c], vols[c] = df["close"], df["quote_vol"]
        cost[c] = float(df["ftmo_spread_rt_bp"].iloc[0] + df["ftmo_commission_rt_bp"].iloc[0])
    return pd.DataFrame(closes), pd.DataFrame(vols), pd.Series(cost)


def period_returns(close, freq, need):
    """Log return per period from the last close of the previous period to the last close of this one; NaN unless the
    period has all `need` hourly bars and the previous period is complete too."""
    cnt = close.resample(freq).count()
    last = close.resample(freq).last()
    full = cnt >= need
    r = np.log(last).diff()
    return r.where(full & full.shift(1, fill_value=False))


def expanding_q(s, q, minp):
    return s.expanding(minp).quantile(q).shift(1)


def summarize(ev, name, cost_col):
    """ev: DataFrame with columns t, coin, gross (bp), cost (bp)."""
    ev = ev.dropna(subset=["gross"])
    ev = ev[ev["t"] >= pd.Timestamp("2018-01-01", tz="UTC")].copy()  # RULES.md: years 2018 -> 2023-03-19
    ev["net"] = ev["gross"] - ev["cost"]
    day = ev.groupby(ev["t"].dt.floor("D"))[["gross", "net", "cost"]].mean()
    t_net = day["net"].mean() / (day["net"].std(ddof=1) / np.sqrt(len(day)))
    t_gross = day["gross"].mean() / (day["gross"].std(ddof=1) / np.sqrt(len(day)))
    pooled = dict(idea=name, events=len(ev), days=len(day), gross_bp=ev["gross"].mean(), cost_bp=ev["cost"].mean(),
                  net_bp=ev["net"].mean(), t_gross=t_gross, t_net=t_net, edge_cost=ev["gross"].mean() / ev["cost"].mean())
    ev["year"] = ev["t"].dt.year
    yr = ev.groupby("year").agg(events=("gross", "size"), gross_bp=("gross", "mean"), net_bp=("net", "mean"))
    yr["t_gross"] = ev.groupby("year").apply(
        lambda g: (lambda d: d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))(g.groupby(g["t"].dt.floor("D"))["gross"].mean()))
    return pooled, yr, ev


def gate(p, yr):
    ec = p["edge_cost"]
    g1 = "PASS" if (ec >= 1.0 and p["t_net"] > 0) else ("MARGINAL" if ec >= 0.5 else "REJECT")
    y = yr[yr["events"] >= 20]["gross_bp"]
    signs = np.sign(y.values)
    flips = int((signs[1:] != signs[:-1]).sum())
    rho = stats.spearmanr(y.index, y.values).statistic if len(y) > 2 else np.nan
    e22 = y.get(2022, np.nan)
    if flips >= 3:
        g2 = "ALTERNATING"
    elif rho <= -0.7 and e22 <= 0:
        g2 = "DECAY"
    elif y.idxmax() in (2021, 2022, 2023) and e22 > 0:
        g2 = "STRONGEST-RECENT"
    else:
        g2 = "FLAT"
    ok = g1 in ("PASS", "MARGINAL") and g2 in ("STRONGEST-RECENT", "FLAT")
    return dict(gate1=g1, flips=flips, spearman=round(rho, 2), gate2=g2, to_step2="YES" if ok else "no")


def plot(yr, p, g, name, title, fn):
    fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor=SURF)
    ax.set_facecolor(SURF)
    x = np.arange(len(yr))
    ax.bar(x, yr["gross_bp"], width=0.6, color=BLUE, linewidth=0)
    ax.axhline(p["cost_bp"], color=GRAY, ls="--", lw=1.2)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.text(-0.45, p["cost_bp"], f"mean cost {p['cost_bp']:.1f} bp", color=INK2, va="bottom", ha="left", fontsize=8)
    for i, (v, n) in enumerate(zip(yr["gross_bp"], yr["events"])):
        ax.text(i, v, f"{v:+.0f}\nn={n}", ha="center", va="bottom" if v >= 0 else "top", fontsize=7.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels([str(i) if i != 2023 else "2023 (to 03-19)" for i in yr.index], fontsize=8, color=INK2)
    ax.set_ylabel("gross bp per event", fontsize=8.5, color=INK2)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.set_title(f"{name}: {title}\ncost gate {g['gate1']} (edge/cost {p['edge_cost']:.2f}) · decay-first {g['gate2']}"
                 f" · to Step 2: {g['to_step2']}", loc="left", fontsize=9.5, color=INK)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo - 0.12 * (hi - lo), hi + 0.12 * (hi - lo))
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, fn), dpi=130, facecolor=SURF)
    plt.close(fig)


def main():
    close, vol, cost = load()
    rd = pd.DataFrame({c: period_returns(close[c], "1D", 24) for c in COINS})
    vd = vol.resample("1D").sum(min_count=24)
    rows, out = [], {}

    # H2 — panel volume shock -> next-day reversal
    shock = np.log(vd / vd.rolling(30, min_periods=20).median().shift(1)).mean(axis=1)
    high = shock > expanding_q(shock, 0.67, 90)
    ev = []
    for c in COINS:
        g = (-np.sign(rd[c]) * rd[c].shift(-1) * 1e4)[high]
        ev.append(pd.DataFrame({"t": g.index, "coin": c, "gross": g.values, "cost": cost[c] + SWAP}))
    out["H2"] = summarize(pd.concat(ev), "H2", None)

    # H7 — coin extreme down day -> next-day long
    ev = []
    for c in COINS:
        thr = rd[c].rolling(365, min_periods=180).quantile(0.10).shift(1)
        sel = rd[c] < thr
        g = (rd[c].shift(-1) * 1e4)[sel]
        ev.append(pd.DataFrame({"t": g.index, "coin": c, "gross": g.values, "cost": cost[c] + SWAP}))
    out["H7"] = summarize(pd.concat(ev), "H7", None)

    # H6 — high trailing panel vol -> 6h block reversal
    r1 = np.log(close).diff().where(close.index.to_series().diff().eq(pd.Timedelta("1h")), axis=0)
    ew = r1.mean(axis=1)
    rv = (ew ** 2).rolling(168, min_periods=150).sum()
    rv_day = rv.shift(1).resample("1D").first()  # variance over the 168 h before 00:00 UTC
    hv = rv_day > expanding_q(rv_day, 0.67, 90)
    rb = pd.DataFrame({c: period_returns(close[c], "6h", 6) for c in COINS})
    hv_b = hv.reindex(rb.index, method="ffill")
    ev = []
    for c in COINS:
        g = (-np.sign(rb[c]) * rb[c].shift(-1) * 1e4)[hv_b.fillna(False)]
        ev.append(pd.DataFrame({"t": g.index, "coin": c, "gross": g.values, "cost": cost[c] + SWAP / 4}))
    out["H6"] = summarize(pd.concat(ev), "H6", None)

    titles = {"H2": "next-day reversal after panel volume-shock days", "H7": "next-day return after a coin's extreme down day",
              "H6": "6h reversal on high trailing-vol days"}
    yearly = []
    for k, (p, yr, ev) in out.items():
        g = gate(p, yr)
        rows.append({**p, **g})
        plot(yr, p, g, k, titles[k], f"{k}_decay_first.png")
        yearly.append(yr.assign(idea=k).reset_index())
        # per-coin view (descriptive)
        ev.groupby("coin").agg(events=("gross", "size"), gross_bp=("gross", "mean"), cost_bp=("cost", "mean"),
                               net_bp=("net", "mean")).round(1).to_csv(os.path.join(HERE, f"{k}_by_coin.csv"))
    res = pd.DataFrame(rows).round(2)
    res.to_csv(os.path.join(HERE, "gates.csv"), index=False)
    yl = pd.concat(yearly).round(2)
    yl.to_csv(os.path.join(HERE, "by_year.csv"), index=False)
    pd.set_option("display.width", 200)
    print(res.to_string(index=False))
    print()
    print(yl.to_string(index=False))
    for k in out:
        print(f"\n{k} by coin:\n", pd.read_csv(os.path.join(HERE, f"{k}_by_coin.csv")).to_string(index=False))


if __name__ == "__main__":
    main()
