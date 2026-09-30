"""Family `attention`: sentiment, attention and wildcard series.

fear_greed          alternative.me Crypto Fear & Greed (0-100, daily). Composite, partly built from price -> weak.
wiki_<article>      English Wikipedia daily user pageviews. Mechanism: retail attention precedes retail flow
                    (Da, Engelberg & Gao 2011 "In Search of Attention" used search volume; pageviews are the
                    reachable proxy - Google Trends is blocked here). Fear pages (Recession, Bank run) = macro angst.
hn_<term>           Hacker News stories/week mentioning the term. Mechanism: tech-crowd attention; a lead on
                    developer/early-adopter interest, historically noisy.
gdelt_<q>           GDELT global news volume (raw article count) / tone for a query. Mechanism: news intensity and
                    negativity; regulation headlines as event shocks.
sec_<term>          Weekly count of SEC filings mentioning the term (EDGAR full-text search). Mechanism: corporate/
                    institutional adoption paperwork (S-1s, 10-Ks with BTC treasuries, ETF filings) leads flows.
kp_geomagnetic      Daily planetary Kp/Ap geomagnetic index (GFZ Potsdam, since 1932). WILDCARD: Krivelyova &
                    Robotti (2003) report lower stock returns after geomagnetic storms (mood channel). Low prior.
"""
import io
import sys
import time

import pandas as pd

from lib import client, get, log_fail, save


def fg(cli):
    j = get(cli, "https://api.alternative.me/fng/", {"limit": 0, "format": "json"})
    df = pd.DataFrame(j["data"])
    df["t"] = pd.to_datetime(df.pop("timestamp").astype(int), unit="s", utc=True)
    df["value"] = df["value"].astype(int)
    save(df[["t", "value", "value_classification"]], "attention", "fear_greed", "t", dict(
        source="alternative.me Fear & Greed", type="composite sentiment index", freq="1d",
        stamp="UTC day 00:00", knowable="published ~00:00 UTC for that day", notes="Built partly from price/vol."))


WIKI = ["Bitcoin", "Ethereum", "Solana_(blockchain_platform)", "Dogecoin", "XRP_Ledger", "Ripple_Labs",
        "Cardano_(blockchain_platform)", "Litecoin", "Binance", "Bitcoin_Cash", "Polkadot_(blockchain_platform)",
        "Cryptocurrency", "Tether_(cryptocurrency)", "Cryptocurrency_bubble", "Non-fungible_token",
        "Blockchain", "Satoshi_Nakamoto", "FTX", "Recession", "Inflation", "Bank_run", "Stock_market_crash"]


def wiki(cli, art):
    r = cli.get(f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"
                f"{art}/daily/20150701/20260929",
                headers={"User-Agent": "finding-alphas-research/0.1 (low-volume research; python-httpx)"})
    if r.status_code != 200:
        return log_fail("attention", f"wiki_{art}", f"HTTP {r.status_code}: {r.text[:120]}")
    j = r.json()
    if not j or not j.get("items"):
        return log_fail("attention", f"wiki_{art}", "no items (title?)")
    df = pd.DataFrame(j["items"])[["timestamp", "views"]]
    df["t"] = pd.to_datetime(df.pop("timestamp"), format="%Y%m%d%H", utc=True)
    save(df, "attention", f"wiki_{art}", "t", dict(
        source=f"Wikimedia pageviews en.wikipedia/{art}", type="daily user pageviews", freq="1d",
        stamp="UTC day", knowable="day end (+ ~1 day publication lag)", notes="agent=user excludes known bots."))


def hn(cli, term, start):
    weeks = pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp.now(tz="UTC").normalize(), freq="7D")
    rows = []
    for a, b in zip(weeks[:-1], weeks[1:]):
        j = get(cli, "https://hn.algolia.com/api/v1/search",
                {"query": term, "tags": "story", "hitsPerPage": 0,
                 "numericFilters": f"created_at_i>={int(a.timestamp())},created_at_i<{int(b.timestamp())}"})
        rows.append((a, j["nbHits"]))
        time.sleep(0.25)
    df = pd.DataFrame(rows, columns=["t", "stories"])
    save(df, "attention", f"hn_{term}", "t", dict(
        source=f"HN Algolia search '{term}' (stories)", type="weekly story count", freq="7d",
        stamp="UTC week start", knowable="week end", notes="Full-text match, includes false positives."))


def gdelt(cli, q, mode):
    time.sleep(7)
    r = get(cli, "https://api.gdeltproject.org/api/v2/doc/doc",
            {"query": q, "mode": mode, "format": "csv", "startdatetime": "20170101000000",
             "enddatetime": pd.Timestamp.now(tz="UTC").strftime("%Y%m%d000000")}, as_json=False, sleep_on_429=15)
    df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")))
    df.columns = [c.strip() for c in df.columns]
    df["t"] = pd.to_datetime(df.pop("Date"), utc=True)
    safe = q.replace('"', "").replace(" ", "_")
    save(df, "attention", f"gdelt_{mode}_{safe}", "t", dict(
        source=f"GDELT DOC 2.0 {mode} '{q}'", type="global online news aggregate", freq="1d (auto for long spans)",
        stamp="UTC day", knowable="~15 min after publication; daily value at day end",
        notes="volraw = matching article count (+ total monitored); tone = avg sentiment."))


def sec(cli, term, start):
    weeks = pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp.now(tz="UTC").normalize(), freq="7D")
    rows = []
    for a, b in zip(weeks[:-1], weeks[1:]):
        j = get(cli, "https://efts.sec.gov/LATEST/search-index",
                {"q": f'"{term}"', "dateRange": "custom", "startdt": a.strftime("%Y-%m-%d"),
                 "enddt": (b - pd.Timedelta("1D")).strftime("%Y-%m-%d")})
        rows.append((a, j["hits"]["total"]["value"]))
        time.sleep(0.2)
    df = pd.DataFrame(rows, columns=["t", "filings"])
    save(df, "attention", f"sec_{term.replace(' ', '_')}", "t", dict(
        source=f"SEC EDGAR full-text search '{term}'", type="weekly filing count", freq="7d",
        stamp="UTC week start (filing date)", knowable="week end", notes="Counts cap at 10,000 per query."))


def kp(cli):
    r = get(cli, "https://kp.gfz-potsdam.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt", as_json=False)
    out = []
    for line in r.text.splitlines():
        if not line or line.startswith("#"):
            continue
        # columns: YYYY MM DD days days_m Bsr dB Kp1..Kp8 ap1..ap8 Ap SN F10.7obs F10.7adj D
        p = line.split()
        kps = list(map(float, p[7:15]))
        out.append({"t": f"{p[0]}-{p[1]}-{p[2]}", "kp_max": max(kps), "kp_mean": sum(kps) / 8, "Ap": float(p[23]),
                    "sunspots": float(p[24]), "f107_obs": float(p[25])})
    df = pd.DataFrame(out)
    save(df, "attention", "kp_geomagnetic", "t", dict(
        source="GFZ Potsdam Kp_ap_Ap_SN_F107_since_1932.txt", type="geophysical index", freq="1d",
        stamp="UTC day", knowable="nowcast within hours; definitive values revised ~monthly",
        notes="WILDCARD. -1 = missing."))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    with client() as cli:
        if mode in ("gdelt", "all"):
            for q in ["bitcoin", "cryptocurrency", "crypto regulation", "stablecoin", "ethereum"]:
                for m in ["timelinevolraw", "timelinetone"]:
                    if q == "bitcoin" and m == "timelinevolraw" and mode == "gdelt":
                        continue  # already pulled
                    try:
                        gdelt(cli, q, m)
                    except Exception as e:
                        log_fail("attention", f"gdelt_{m}_{q}", e)
        if mode in ("hn", "all"):
            for fn, a in [(hn, ("bitcoin", "2010-07-05")), (hn, ("ethereum", "2014-01-06")),
                          (hn, ("crypto", "2013-01-07"))]:
                try:
                    fn(cli, *a)
                except Exception as e:
                    log_fail("attention", f"{fn.__name__}{a}", e)
        if mode in ("sec", "all"):
            for fn, a in [(sec, ("bitcoin", "2013-01-07")), (sec, ("digital asset", "2015-01-05"))]:
                try:
                    fn(cli, *a)
                except Exception as e:
                    log_fail("attention", f"{fn.__name__}{a}", e)
        if mode in ("wiki", "all"):
            for x in WIKI:
                try:
                    wiki(cli, x)
                except Exception as e:
                    log_fail("attention", f"wiki_{x}", e)
                time.sleep(3)
    print("DONE p6_attention", mode, file=sys.stderr)
