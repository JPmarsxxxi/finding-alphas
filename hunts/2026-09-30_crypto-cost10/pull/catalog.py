"""Build CATALOG.md, the OHLC hygiene table and the coverage plot from data/registry.jsonl.

Reads ONLY the explore side (data/<family>/). The _sealed side contributes row counts from the registry
(bookkeeping) and nothing else.

Hygiene checks (data-hygiene.md "mandatory for any new OHLC source"), per hourly OHLC series, per year:
  zero_gap_rate  share of consecutive bars with open == previous close (vendor-synthetic open detector;
                 for 24/7 crypto trade prints a high rate is normal in a deep book - read with median gap)
  roll_bp        Roll implied spread 2*sqrt(-cov(r_t, r_t-1)) in bp, NaN when the autocovariance is positive
  zero_vol_share share of bars with zero volume (dead / stale feed)
  missing_hours  hours absent inside the series' own span
"""
import json
import os
import re

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from lib import DATA, REGISTRY, ROOT  # noqa: E402

BLUE, GRAY, INK, INK2, SURF = "#2a78d6", "#c3c2b7", "#0b0b0b", "#52514e", "#fcfcfb"


def registry():
    recs = [json.loads(l) for l in open(REGISTRY)]
    df = pd.DataFrame(recs).drop_duplicates(["family", "name"], keep="last")
    return df.sort_values(["family", "name"]).reset_index(drop=True)


def hygiene(reg):
    out = []
    for _, r in reg.iterrows():
        is_ohlc = r["family"] == "spot" or r["name"].startswith("perp_klines")
        if not is_ohlc or r["rows_explore"] == 0:
            continue
        df = pd.read_parquet(os.path.join(DATA, r["family"], r["name"] + ".parquet"))
        df = df.sort_values("t").set_index("t")
        vol = df["vol"] if "vol" in df else df["volume"]
        step = df.index.to_series().diff()
        consec = step == pd.Timedelta("1h")
        r_ = np.log(df["close"]).diff().where(consec)
        full = pd.date_range(df.index[0], df.index[-1], freq="1h")
        missing = pd.Series(1, index=full.difference(df.index))
        for y, g in df.groupby(df.index.year):
            c = consec.loc[g.index]
            prev_close = df["close"].shift(1).loc[g.index]
            zg = ((g["open"] == prev_close) & c).sum() / max(c.sum(), 1)
            rr = r_.loc[g.index]
            cov = rr.cov(rr.shift(1))
            out.append({"series": r["name"], "year": y, "bars": len(g),
                        "missing_hours": int((missing.index.year == y).sum()),
                        "zero_gap_rate": round(zg, 3),
                        "median_gap_bp": round(float(((g["open"] / prev_close - 1).abs() * 1e4)[c].median()), 3),
                        "roll_bp": round(2 * np.sqrt(-cov) * 1e4, 2) if cov < 0 else np.nan,
                        "zero_vol_share": round(float((vol.loc[g.index] == 0).mean()), 4)})
    h = pd.DataFrame(out)
    h.to_csv(os.path.join(ROOT, "hygiene_ohlc_by_year.csv"), index=False)
    return h


def coverage_plot(reg):
    reg = reg.copy()
    reg["first"] = pd.to_datetime(reg["first"])
    reg = reg[reg["first"] >= "2009-01-01"].copy() if False else reg
    lo = pd.Timestamp("2009-01-01")
    reg["start"] = reg["first"].clip(lower=lo)
    reg["exp_end"] = pd.to_datetime(reg["explore_last"])
    reg["sea_end"] = pd.to_datetime(reg["sealed_last"])
    n = len(reg)
    fig, ax = plt.subplots(figsize=(12, 0.16 * n + 1.6), facecolor=SURF)
    ax.set_facecolor(SURF)
    for i, r in reg.iloc[::-1].reset_index(drop=True).iterrows():
        if pd.notna(r["exp_end"]):
            ax.barh(i, (r["exp_end"] - r["start"]).days, left=r["start"], height=0.62, color=BLUE, linewidth=0)
        s0 = r["exp_end"] if pd.notna(r["exp_end"]) else r["start"]
        if pd.notna(r["sea_end"]):
            ax.barh(i, (r["sea_end"] - s0).days, left=s0, height=0.62, color=GRAY, linewidth=0)
    labels = (reg["family"] + " / " + reg["name"]).iloc[::-1].tolist()
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels, fontsize=6.5, color=INK2)
    ax.set_ylim(-0.8, n - 0.2)
    ax.axvline(pd.Timestamp("2023-11-30"), color=INK2, lw=0.8, ls="--")
    ax.text(pd.Timestamp("2023-12-15"), n - 0.5, "explore end 2023-11-30", fontsize=8, color=INK2, va="bottom")
    ax.set_xlim(lo, pd.Timestamp("2026-12-31"))
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRAY)
    ax.tick_params(axis="x", colors=INK2, labelsize=8)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e6e5e0", lw=0.6)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BLUE, label="explore (usable now, <= 2023-11-30)"),
                       Patch(color=GRAY, label="held apart in data/_sealed (TEST + SEALED, not opened)")],
              loc="upper left", bbox_to_anchor=(0, 1.0 + 0.9 / (0.16 * n + 1.6)), ncol=2, frameon=False,
              fontsize=9, labelcolor=INK)
    ax.set_title(f"Coverage of the {n} series pulled 2026-09-30 (bars before 2009 clipped)", loc="left",
                 fontsize=11, color=INK, pad=28)
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "coverage.png"), dpi=130, facecolor=SURF)


def catalog(reg, h):
    L = ["# DATA CATALOG: crypto-cost10 (pulled 2026-09-30)", "",
         "Generated by `pull/catalog.py` from `data/registry.jsonl`. One provenance line per series "
         "(data-hygiene.md: type / venue / timestamp / knowable-at).", "",
         "**Split:** rows <= 2023-11-30 are in `data/<family>/` (explore). Rows after that (TEST 2023-12-06.. and "
         "SEALED 2024-08-01..) are in `data/_sealed/<family>/`, pulled but not opened: no statistic, plot or "
         "hygiene check here touches them. The seal decision is still yours.", "",
         f"**{len(reg)} series** in {reg['family'].nunique()} families. See `coverage.png`.", ""]
    fams = {"spot": "Spot prices (1h trade prints)", "perp": "Binance perpetual futures", "deriv":
            "Other derivatives venues", "onchain": "On-chain", "defi": "DeFi / stablecoins (DefiLlama, BACKFILLED)",
            "attention": "Attention, sentiment, wildcards", "macro": "Macro / cross-asset / fundamental"}
    for fam, title in fams.items():
        g = reg[reg["family"] == fam]
        if not len(g):
            continue
        L += [f"## {title} ({len(g)})", "",
              "| series | source | type | freq | from | explore rows | sealed rows | knowable |",
              "|---|---|---|---|---|---|---|---|"]
        for _, r in g.iterrows():
            L.append(f"| `{r['name']}` | {r['source']} | {r['type']} | {r['freq']} | {r['first']} | "
                     f"{r['rows_explore']:,} | {r['rows_sealed']:,} | {r['knowable']} |")
        notes = g[g["notes"].astype(str).str.len() > 0][["name", "notes"]].drop_duplicates("notes")
        if len(notes):
            L += ["", "Notes: " + " ".join(f"`{n}`: {t}" for n, t in notes.values)]
        L.append("")
    if len(h):
        s = h.groupby("series").agg(years=("year", "count"), missing_hours=("missing_hours", "sum"),
                                    zero_gap_max=("zero_gap_rate", "max"),
                                    roll_bp_median=("roll_bp", "median"),
                                    zero_vol_max=("zero_vol_share", "max")).reset_index()
        L += ["## Hygiene: hourly OHLC series (explore side only)", "",
              "Full per-year table: `hygiene_ohlc_by_year.csv`.", "",
              "**How to read it.** *Zero-gap rate* of 0.3-0.6 is expected here: in a 24/7 market the next hour's "
              "first trade often prints at the previous hour's last price. This is not the vendor-synthetic-open "
              "trap (that shows as a rate near 1.0 with zero volume, as in `bitstamp_BTCUSD` 2011-2013). "
              "*Roll spread* at 1h bars is NOT a bid-ask estimate (BTC's measured FTMO spread is 0.13 bp): at this "
              "sampling it reads negative hourly autocorrelation, i.e. hourly reversal, and is blank in years "
              "where the autocorrelation is positive. *Missing hours*: Binance outages and maintenance; "
              "`coinbase_XRPUSD` carries the 2021-01 to 2023-07 delisting gap.", "",
              "| series | years | missing hours | max zero-gap rate | median Roll spread (bp) | max zero-volume share |",
              "|---|---|---|---|---|---|"]
        for _, r in s.iterrows():
            L.append(f"| `{r['series']}` | {r['years']} | {r['missing_hours']:,} | {r['zero_gap_max']:.3f} | "
                     f"{'' if pd.isna(r['roll_bp_median']) else round(r['roll_bp_median'], 2)} | "
                     f"{r['zero_vol_max']:.4f} |")
        L.append("")
    fails = os.path.join(DATA, "failures.jsonl")
    if os.path.exists(fails):
        f = pd.DataFrame([json.loads(l) for l in open(fails)])
        done = list(reg["name"])

        def resolved(n):
            m = re.match(r"(\w+)\('([^']+)'", n)  # e.g. hn('bitcoin', ...) -> hn_bitcoin
            cands = {n, n.replace("wiki('", "wiki_").split("'")[0]}
            if m:
                cands.add(f"{m.group(1)}_{m.group(2)}".replace(" ", "_").replace("/", "_"))
                cands.add(m.group(2).split("/")[-1])
            return any(d == c or d.startswith(c + "_") or ("nyfed_" + c) == d for c in cands for d in done)
        f = f[~f["name"].map(resolved)].drop_duplicates("name")
        if len(f):
            L += ["## Not pulled (final failures)", "", "| family | series | why |", "|---|---|---|"]
            L += [f"| {r.family} | {r.name} | {str(r.why)[:140]} |" for r in f.itertuples()]
    open(os.path.join(ROOT, "CATALOG.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    reg = registry()
    h = hygiene(reg)
    coverage_plot(reg)
    catalog(reg, h)
    print(len(reg), "series;", len(h), "hygiene rows")
