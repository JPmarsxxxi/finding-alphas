"""p12 - Coverage map of FREE two-sided (bid AND ask) sources per coin, vs the 80%-of-life target (EDA#2).

Price-only sources are excluded (data-hygiene rule 1). Paid sources excluded (user, 2026-10-03).
Sources:
  Dukascopy   1-min BID and ASK candles - PROBED here: a hit = both BID and ASK files decode to >0 bars with volume,
              on any of days 15/16/17 of the month. Yearly probe (June), then monthly around the first and last hit.
  FTMO ticks  from p9 (2026-10-02): first month with ticks, monthly probe -> continuous to now assumed (rule-of-thumb,
              confirm when pulled)
  Binance fut bookTicker (USD-M perps, data.binance.vision listing 2026-10-03): 2023-05-16 .. 2024-03-30, all 10
  Tardis free 1 day per month only - a SAMPLE, never counted as coverage; listed for validation use
Life start = first exchange trading, approximate public dates (labelled approximate).
"""
import lzma
import os
import struct
import time

import httpx
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NOW = pd.Timestamp("2026-10-03")
LIFE = {"BTCUSD": "2010-07-17", "LTCUSD": "2011-10-13", "XRPUSD": "2013-08-01", "DOGEUSD": "2013-12-15",
        "ETHUSD": "2015-08-07", "BNBUSD": "2017-07-25", "BCHUSD": "2017-08-01", "ADAUSD": "2017-10-01",
        "SOLUSD": "2020-04-10", "DOTUSD": "2020-08-19"}
FTMO_TICKS = {s: "2022-02" for s in LIFE} | {"BNBUSD": "2025-05", "SOLUSD": "2025-05", "BCHUSD": "2025-05"}
BFUT = ("2023-05-16", "2024-03-30")
PAUSE = 0.15


def get(client, url):
    for a in range(4):
        try:
            r = client.get(url, timeout=15)
            if r.status_code == 404:
                return None
            if r.status_code == 200:
                return r.content
        except Exception:
            pass
        time.sleep(1.5 * (a + 1))
    return None


def has_side(client, sym, day, side):
    c = get(client, f"https://datafeed.dukascopy.com/datafeed/{sym}/{day.year}/{day.month - 1:02d}/{day.day:02d}/"
                    f"{side}_candles_min_1.bi5")
    time.sleep(PAUSE)
    if not c:
        return False
    try:
        raw = lzma.decompress(c)
    except lzma.LZMAError:
        return False
    vols = [struct.unpack(">5if", raw[i * 24:(i + 1) * 24])[5] for i in range(len(raw) // 24)]
    return sum(v > 0 for v in vols) > 0


def hit(client, sym, month_start):
    for dd in (15, 16, 17):
        day = month_start + pd.Timedelta(days=dd - 1)
        if day > NOW:
            return False
        if has_side(client, sym, day, "BID") and has_side(client, sym, day, "ASK"):
            return True
    return False


def duka_span(client, sym):
    years = [pd.Timestamp(f"{y}-06-01") for y in range(2010, NOW.year + 1)]
    yh = [y for y in years if hit(client, sym, y)]
    if not yh:
        return None, None, f"0/{len(years)}"
    first = last = None
    for m in pd.date_range(yh[0] - pd.DateOffset(years=1), yh[0] + pd.DateOffset(months=1), freq="MS"):
        if hit(client, sym, m):
            first = m; break
    for m in reversed(pd.date_range(yh[-1], min(NOW, yh[-1] + pd.DateOffset(years=1)), freq="MS")):
        if hit(client, sym, m):
            last = m; break
    return first, last, f"{len(yh)}/{len(years)}"


def covered_from(intervals):
    """earliest date from which the union of intervals runs unbroken to NOW (None if it never reaches NOW)"""
    iv = sorted((a, b) for a, b in intervals if a is not None)
    start = None
    reach = None
    for a, b in iv:
        if reach is None or a > reach + pd.Timedelta(days=45):     # a gap > 45 days restarts the chain
            start, reach = a, b
        else:
            reach = max(reach, b)
    return start if reach is not None and reach >= NOW - pd.Timedelta(days=45) else None


def main():
    rows = []
    with httpx.Client(headers={"User-Agent": "Mozilla/5.0"}) as client:
        for s, life in LIFE.items():
            f, l, yhits = duka_span(client, s)
            life = pd.Timestamp(life)
            target = life + 0.2 * (NOW - life)                     # 80% of life -> data needed from here
            ft = pd.Timestamp(FTMO_TICKS[s] + "-01")
            ivs = [(f, (l + pd.offsets.MonthEnd(0)) if l is not None else None), (ft, NOW),
                   (pd.Timestamp(BFUT[0]), pd.Timestamp(BFUT[1]))]
            start = covered_from(ivs)
            pct = 100 * ((NOW - start) / (NOW - life)) if start is not None else 0.0
            ov = []
            if f is not None and l is not None and l >= ft:
                ov.append(f"Duka x FTMO {ft:%Y-%m}..{l:%Y-%m}")
            if f is not None and l is not None and l >= pd.Timestamp(BFUT[0]):
                ov.append("Duka x BinFut")
            ov.append("FTMO x BinFut" if ft <= pd.Timestamp(BFUT[1]) else "-")
            rows.append(dict(coin=s, life_start=f"{life:%Y-%m}", need_from_80pct=f"{target:%Y-%m}",
                             duka_first=f"{f:%Y-%m}" if f is not None else "none",
                             duka_last=f"{l:%Y-%m}" if l is not None else "none", duka_years_hit=yhits,
                             ftmo_ticks_from=FTMO_TICKS[s], binfut=f"{BFUT[0][:7]}..{BFUT[1][:7]}",
                             stitched_from=f"{start:%Y-%m}" if start is not None else "-",
                             pct_of_life=round(pct), meets_80=pct >= 80, overlaps=" | ".join(ov)))
            print(f"  {s} done", flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(os.path.join(ROOT, "coverage_two_sided.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
    print("\nFREE TWO-SIDED COVERAGE (life start approximate; Tardis free = 1 day/month sample, not counted)")
    print(d.to_string(index=False))


if __name__ == "__main__":
    main()
