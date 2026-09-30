"""Pull Binance SPOT 1h klines for the 10 FTMO crypto symbols, attach FTMO measured spread.

Source : https://data-api.binance.vision/api/v3/klines (public, no key; api.binance.com is geo-blocked here)
Spread : FTMO live MT5 measurement x098 (2026-09-02), round trip, bp of notional (alpha_log.md).
         Constant per symbol: a single live sample, NOT a historical series.
Holdout: HOLDOUT_RULES.md. Rows <= 2023-11-30 -> data/<sym>_1h.parquet (explore = TRAIN+VAL).
         Rows >= 2023-12-06 (TEST + SEALED) -> data/_sealed/<sym>_1h.parquet. Never read, never summarised.
         Embargo 2023-12-01..05 dropped.
Timestamps: UTC, bar OPEN time (knowable at open + 1h).
"""
import os
import time

import httpx
import pandas as pd

BASE = "https://data-api.binance.vision/api/v3/klines"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data")
SEALED = os.path.join(OUT, "_sealed")
EXPLORE_END = pd.Timestamp("2023-11-30 23:59", tz="UTC")
TEST_START = pd.Timestamp("2023-12-06", tz="UTC")

# FTMO symbol -> (Binance symbol, x098 spread round trip bp)
FTMO = {
    "BTCUSD": ("BTCUSDT", 0.129),
    "BNBUSD": ("BNBUSDT", 0.145),
    "ETHUSD": ("ETHUSDT", 2.503),
    "SOLUSD": ("SOLUSDT", 3.004),
    "DOGEUSD": ("DOGEUSDT", 11.022),
    "XRPUSD": ("XRPUSDT", 11.121),
    "ADAUSD": ("ADAUSDT", 15.110),
    "BCHUSD": ("BCHUSDT", 24.506),
    "DOTUSD": ("DOTUSDT", 25.4),
    "LTCUSD": ("LTCUSDT", 30.0),
}
COMMISSION_RT_BP = 6.5  # FTMO crypto, 3.25 bp/side

COLS = ["open_time", "open", "high", "low", "close", "vol", "close_time", "quote_vol",
        "n", "buy_vol", "buy_quote_vol", "_ignore"]


def pull(symbol: str) -> pd.DataFrame:
    rows, start = [], 0
    with httpx.Client(timeout=30) as cli:
        while True:
            for attempt in range(5):
                try:
                    r = cli.get(BASE, params={"symbol": symbol, "interval": "1h",
                                              "startTime": start, "limit": 1000})
                    r.raise_for_status()
                    break
                except httpx.HTTPError:
                    time.sleep(2 ** attempt)
            else:
                raise RuntimeError(f"{symbol}: failed at startTime={start}")
            batch = r.json()
            if not batch:
                break
            rows.extend(batch)
            start = batch[-1][0] + 1
            if len(batch) < 1000:
                break
    df = pd.DataFrame(rows, columns=COLS).drop(columns=["_ignore", "close_time"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    num = [c for c in df.columns if c != "open_time"]
    df[num] = df[num].astype(float)
    df["n"] = df["n"].astype("int64")
    df["sell_vol"] = df["vol"] - df["buy_vol"]
    return df.drop_duplicates("open_time").sort_values("open_time").reset_index(drop=True)


def main():
    os.makedirs(SEALED, exist_ok=True)
    summary = []
    for ftmo_sym, (bin_sym, spread) in FTMO.items():
        df = pull(bin_sym)
        df.insert(0, "symbol", ftmo_sym)
        df.insert(1, "binance_symbol", bin_sym)
        df["ftmo_spread_rt_bp"] = spread
        df["ftmo_commission_rt_bp"] = COMMISSION_RT_BP
        explore = df[df["open_time"] <= EXPLORE_END]
        sealed = df[df["open_time"] >= TEST_START]
        explore.to_parquet(os.path.join(OUT, f"{ftmo_sym}_1h.parquet"), index=False)
        sealed.to_parquet(os.path.join(SEALED, f"{ftmo_sym}_1h.parquet"), index=False)
        # Explore-side stats only. Sealed side: row count only (bookkeeping, not a measurement).
        span_h = (explore["open_time"].iloc[-1] - explore["open_time"].iloc[0]) / pd.Timedelta("1h") + 1
        summary.append({
            "symbol": ftmo_sym, "binance": bin_sym,
            "ftmo_spread_rt_bp": spread,
            "explore_first": explore["open_time"].iloc[0].strftime("%Y-%m-%d"),
            "explore_last": explore["open_time"].iloc[-1].strftime("%Y-%m-%d"),
            "explore_rows": len(explore),
            "missing_hours": int(span_h - len(explore)),
            "median_daily_quote_vol_musd": round(
                explore.set_index("open_time")["quote_vol"].resample("1D").sum().median() / 1e6, 1),
            "sealed_rows": len(sealed),
        })
        print(f"{ftmo_sym:8s} {len(explore):>7,} explore rows  {len(sealed):>6,} sealed rows", flush=True)
    s = pd.DataFrame(summary)
    s.to_csv(os.path.join(HERE, "pull_summary.csv"), index=False)
    print()
    print(s.to_string(index=False))


if __name__ == "__main__":
    main()
