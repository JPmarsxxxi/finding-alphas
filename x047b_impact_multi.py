"""#047b - impact decay across instruments. How big is the TRANSITORY component on each?

#047 on BTCUSD: 1sd of flow moves price +2.543bp, R(240) = 2.293, so the non-permanent part is
0.250bp - the entire pool a mean-reversion strategy could fish in. Against BTCUSD's 0.1325bp round
trip that is a 1.9x ceiling, assuming perfect capture.

This asks whether another instrument has a bigger pool. Prices are BINANCE for every symbol so the
curves are comparable like for like (BTC's FTMO-priced 0.250 is re-derived here on Binance as a
consistency check). Costs are the FTMO round trips measured live 2026-08-19:
    BTCUSD 0.1325 | ETHUSD 3.17 | SOLUSD 3.95 | XRPUSD 14.94
"""
import numpy as np, pandas as pd, glob, os, sys

D = r"C:\Users\User\backtest_engine\backtest_engine2\data"
RT = {"BTCUSDT": 0.1325, "ETHUSDT": 3.17, "SOLUSDT": 3.95, "XRPUSDT": 14.94}
KS = [0, 1, 2, 5, 10, 30, 60, 240]
rng = np.random.default_rng(9)

def load(sym):
    parts = []
    for sub in (f"binance_{sym.lower()}_monthly", f"binance_{sym.lower()}_1m"):
        for x in sorted(glob.glob(os.path.join(D, sub, "*.parquet"))):
            if os.path.getsize(x) > 2000:
                parts.append(pd.read_parquet(x))
    if not parts:
        return None
    d = pd.concat(parts).sort_index()
    d = d[~d.index.duplicated(keep="first")]
    return d[(d.buy_vol + d.sell_vol) > 0]

print(f"{'symbol':<9}{'minutes':>11}{'R(0)':>8}{'R(240)':>9}{'transitory':>12}"
      f"{'FTMO rt':>9}{'ceiling':>9}{'null max':>10}")
print("-"*78)
for sym in ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"):
    d = load(sym)
    if d is None or len(d) < 100_000:
        print(f"{sym:<9}{'(not pulled yet)':>11}")
        continue
    n = len(d); lp = np.log(d.close.values)
    imb = ((d.buy_vol - d.sell_vol) / (d.buy_vol + d.sell_vol).replace(0, np.nan)).fillna(0.0)
    z = ((imb - imb.rolling(1440, min_periods=200).mean())
         / imb.rolling(1440, min_periods=200).std().replace(0, np.nan)).values

    def curve(flow):
        out = []
        for k in KS:
            hi = n - k - 2
            m = np.isfinite(flow[1:hi]) & np.isfinite(lp[1:hi]) & np.isfinite(lp[1+k:hi+k])
            out.append(np.polyfit(flow[1:hi][m],
                                  (lp[1+k:hi+k][m] - lp[0:hi-1][m]) * 1e4, 1)[0])
        return np.array(out)

    o, nl = curve(z), curve(rng.permutation(z))
    trans = o[0] - o[-1]
    print(f"{sym:<9}{n:>11,}{o[0]:>8.3f}{o[-1]:>9.3f}{trans:>12.3f}"
          f"{RT[sym]:>9.3f}{trans/RT[sym]:>8.1f}x{np.abs(nl).max():>10.3f}")
print("\nceiling = transitory / round trip, assuming PERFECT capture of the whole come-back.")
print("bar in this log is 5x.")
