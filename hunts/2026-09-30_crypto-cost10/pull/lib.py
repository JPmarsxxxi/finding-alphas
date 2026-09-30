"""Shared helpers for the crypto-cost10 pulls.

Every series goes through `save()`:
  * rows <= EXPLORE_END -> data/<family>/<name>.parquet
  * rows  > EXPLORE_END -> data/_sealed/<family>/<name>.parquet  (TEST 2023-12-06.. + SEALED 2024-08-01..,
    HOLDOUT_RULES.md). The user said "fetch now, talk about the seal later", so nothing is thrown away;
    it is only kept apart. Nothing in this folder reads, plots or summarises the _sealed side.
  * one provenance record per series appended to data/registry.jsonl (data-hygiene.md: type / venue /
    timestamp / knowable-at, written BEFORE any return is computed).
"""
import json
import os
import threading
import time

import httpx
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
SEALED = os.path.join(DATA, "_sealed")
REGISTRY = os.path.join(DATA, "registry.jsonl")
EXPLORE_END = pd.Timestamp("2023-11-30 23:59:59", tz="UTC")
UA = {"User-Agent": "Mozilla/5.0 (finding-alphas research pull)"}
_lock = threading.Lock()

# FTMO symbol -> Binance base asset, x098 measured round-trip spread (bp), 2026-09-02 single live sample
COINS = {
    "BTCUSD": ("BTC", 0.129), "BNBUSD": ("BNB", 0.145), "ETHUSD": ("ETH", 2.503),
    "SOLUSD": ("SOL", 3.004), "DOGEUSD": ("DOGE", 11.022), "XRPUSD": ("XRP", 11.121),
    "ADAUSD": ("ADA", 15.110), "BCHUSD": ("BCH", 24.506), "DOTUSD": ("DOT", 25.4),
    "LTCUSD": ("LTC", 30.0),
}
FTMO_COMMISSION_RT_BP = 6.5


def client(**kw):
    return httpx.Client(timeout=60, headers=UA, follow_redirects=True, **kw)


def get(cli, url, params=None, tries=6, sleep_on_429=10, as_json=True, method="GET", body=None):
    last = None
    for i in range(tries):
        try:
            r = cli.post(url, json=body) if method == "POST" else cli.get(url, params=params)
            if r.status_code == 429:
                time.sleep(sleep_on_429 * (i + 1))
                continue
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json() if as_json else r
        except (httpx.HTTPError, ValueError) as e:
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"GET failed {url} {params}: {last}")


def save(df, family, name, tcol, prov):
    """Split at EXPLORE_END, write both parts, log provenance. `prov` keys:
    source, type, freq, stamp, knowable, notes."""
    if df is None or len(df) == 0:
        log_fail(family, name, "empty")
        return
    df = df.copy()
    t = pd.to_datetime(df[tcol], utc=True)
    df[tcol] = t
    df = df.sort_values(tcol).drop_duplicates()
    exp, sea = df[df[tcol] <= EXPLORE_END], df[df[tcol] > EXPLORE_END]
    for part, base in ((exp, DATA), (sea, SEALED)):
        d = os.path.join(base, family)
        os.makedirs(d, exist_ok=True)
        part.to_parquet(os.path.join(d, f"{name}.parquet"), index=False)
    rec = {
        "family": family, "name": name, "rows_explore": int(len(exp)), "rows_sealed": int(len(sea)),
        "first": str(t.min().date()), "explore_last": str(exp[tcol].max().date()) if len(exp) else None,
        "sealed_last": str(sea[tcol].max().date()) if len(sea) else None,
        "columns": [c for c in df.columns if c != tcol], **prov,
    }
    with _lock, open(REGISTRY, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"[ok] {family}/{name}: {len(exp):,} explore + {len(sea):,} sealed rows from {rec['first']}", flush=True)


def log_fail(family, name, why):
    with _lock, open(os.path.join(DATA, "failures.jsonl"), "a") as fh:
        fh.write(json.dumps({"family": family, "name": name, "why": str(why)[:300]}) + "\n")
    print(f"[FAIL] {family}/{name}: {why}", flush=True)
