"""p15 - Step P2: build the VALIDATED, stitched hourly price set (EDA#2). Explore side only (< 2023-12-01).

Decisions (user, 2026-10-04):
  - validated years only ("I don't want garbage data"): a Binance coin-year is used only if it PASSED check A
    (p14: Binance last-trade close vs Binance's own mid, |gap| median <= 2.5 bp and daily diff <= 5 bp)
  - FTMO hourly mids from 2022-01-01 for coins whose FTMO bars were verified against FTMO ticks (p11):
    BTC ETH XRP LTC ADA DOGE DOT.   BNB, BCH stay on Binance (FTMO unverified + tracks poorly); SOL has no FTMO pre-seal
  - failed years are CUT (left as a hole), never patched
  - DOT: FTMO stores DOT spread 10x too small (p11) -> corrected here (raw file untouched), after checking the fix
    against FTMO DOT ticks from p11's saved hours
Columns per coin:  t (UTC bar open) | price (value at bar END) | source | ftmo_spread_bp | binance_quote_vol | new_source
  source: binance_trade (last-trade close; validated 1-2 bp from mid) or ftmo_mid (bid + bar spread/2; verified)
  new_source = True on the first bar after a source switch -> the backtest must not take a return ACROSS a switch.
Gaps are left as gaps (rule 9). Raw files in data/spot and data/ftmo are not modified.
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "validated")
SEAL = pd.Timestamp("2023-12-01", tz="UTC")
FTMO_FROM = pd.Timestamp("2022-01-01", tz="UTC")
FTMO_COINS = {"BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD", "DOGEUSD", "DOTUSD"}
DOT_SPREAD_FIX = 10.0


def dot_fix_check():
    h = pd.read_csv(os.path.join(ROOT, "ftmo_h1_verification_hours.csv"), parse_dates=["day"])
    d = h[h.symbol == "DOTUSD"].copy()
    d["fixed_sp_bp"] = d.bar_sp_bp * DOT_SPREAD_FIX
    d["fixed_mid_err_bp"] = d.mid_err_bp + (DOT_SPREAD_FIX - 1) * d.bar_sp_bp / 2      # mid = bid + spread/2
    d["ratio"] = d.tick_min_bp / d.bar_sp_bp
    by_m = d.groupby(d.day.dt.to_period("M")).ratio.median().round(2)
    print("DOT spread fix check vs FTMO ticks (p11 sample, 15th of each month 2022-02..2023-11):")
    print(f"  tick min spread / bar spread, monthly medians: min {by_m.min()}  max {by_m.max()}  (fix assumes 10)")
    print(f"  built mid error vs tick mid: BEFORE median {d.mid_err_bp.median():+.2f} bp, |p90| {d.mid_err_bp.abs().quantile(.9):.2f}"
          f"   AFTER median {d.fixed_mid_err_bp.median():+.2f} bp, |p90| {d.fixed_mid_err_bp.abs().quantile(.9):.2f}")
    print(f"  fixed bar spread {d.fixed_sp_bp.median():.2f} bp vs tick min {d.tick_min_bp.median():.2f} bp\n")
    return by_m.between(9.5, 10.5).all()


def validated_years():
    a = pd.read_csv(os.path.join(ROOT, "price_vs_mid.csv"))
    a = a[(a.check == "A same-venue") & (a.venue == "binance")]
    return {c: sorted(g[g.PASS == "yes"].year.tolist()) for c, g in a.groupby("coin")}


def build(coin, years_ok, dot_ok):
    b = pd.read_parquet(os.path.join(ROOT, "data", "spot", f"binance_{coin}.parquet"), columns=["t", "close", "quote_vol"])
    b = b[b.t < SEAL].set_index("t")
    use_ftmo = coin in FTMO_COINS and (coin != "DOTUSD" or dot_ok)
    keep_b = b.index.year.isin(years_ok)
    if use_ftmo:
        keep_b &= b.index < FTMO_FROM
    parts = [pd.DataFrame({"price": b.close[keep_b], "source": "binance_trade", "ftmo_spread_bp": np.nan})]
    if use_ftmo:
        f = pd.read_parquet(os.path.join(ROOT, "data", "ftmo", f"ftmo_h1_{coin}.parquet"))
        f = f[(f.t >= FTMO_FROM) & (f.t < SEAL) & ~f.zero_spread].set_index("t")
        sp = f.spread_pts * (DOT_SPREAD_FIX if coin == "DOTUSD" else 1.0)
        point_px = f.spread_pts.replace(0, np.nan)
        sp_price = (f.mid_close - f.bid_close) * 2 / point_px * sp            # spread in price units, rescaled
        mid = f.bid_close + sp_price / 2
        parts.append(pd.DataFrame({"price": mid, "source": "ftmo_mid", "ftmo_spread_bp": sp_price / mid * 1e4}))
    d = pd.concat(parts).sort_index()
    d["binance_quote_vol"] = b.quote_vol.reindex(d.index)                     # H2 volume input (signal, not price)
    d["new_source"] = d.source.ne(d.source.shift())
    gap_hours = d.index.to_series().diff() > pd.Timedelta(hours=1)
    d.loc[gap_hours, "new_source"] = True                                     # also never take a return across a hole
    d.index.name = "t"
    return d.reset_index(), use_ftmo


def junction(coin, d):
    """offset at the switch: Binance close vs FTMO mid over Jan 2022 (both present there in the raw files)"""
    b = pd.read_parquet(os.path.join(ROOT, "data", "spot", f"binance_{coin}.parquet"), columns=["t", "close"]).set_index("t").close
    f = d[d.source == "ftmo_mid"].set_index("t").price
    f = f[f.index < FTMO_FROM + pd.Timedelta(days=31)]
    g = ((b.reindex(f.index) / f - 1) * 1e4).dropna()
    return round(g.median(), 2), round(g.abs().quantile(0.9), 2), len(g)


def main():
    os.makedirs(OUT, exist_ok=True)
    dot_ok = dot_fix_check()
    print(f"DOT fix accepted: {dot_ok}\n")
    yrs = validated_years()
    rows = []
    for coin in ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD", "DOGEUSD", "DOTUSD", "BNBUSD", "BCHUSD", "SOLUSD"]:
        d, use_ftmo = build(coin, yrs.get(coin, []), dot_ok)
        d.to_parquet(os.path.join(OUT, f"validated_{coin}.parquet"), index=False)
        jn = junction(coin, d) if use_ftmo else (None, None, 0)
        by = d.groupby([d.t.dt.year, "source"]).size().unstack(fill_value=0)
        for y, r in by.iterrows():
            rows.append(dict(coin=coin, year=y, binance_trade=int(r.get("binance_trade", 0)), ftmo_mid=int(r.get("ftmo_mid", 0))))
        print(f"{coin}: {len(d):,} hours  {d.t.min():%Y-%m-%d} -> {d.t.max():%Y-%m-%d}   switches/holes flagged {int(d.new_source.sum())}"
              + (f"   junction Jan-2022 Binance vs FTMO: median {jn[0]:+} bp, |p90| {jn[1]} bp ({jn[2]} h)" if use_ftmo else ""))
    t = pd.DataFrame(rows).pivot(index="year", columns="coin", values=["binance_trade", "ftmo_mid"]).fillna(0).astype(int)
    pd.set_option("display.width", 250)
    print("\nHOURS PER YEAR BY SOURCE (blank year = cut / not available; full year = 8760)")
    print(t.to_string())


if __name__ == "__main__":
    main()
