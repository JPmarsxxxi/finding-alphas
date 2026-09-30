"""Family `macro`: fundamental / cross-asset data that co-moves with crypto.

yahoo_<ticker>   Daily OHLCV (+adjclose). Indices, FX, rates, commodities, crypto equities, spot ETFs, CME futures.
                 HYGIENE: Yahoo index OPENS are often synthetic (= prior close) - never use index opens;
                 Yahoo FX is an indicative composite. Close-to-close only. Stamps are the exchange's local date.
                 Mechanisms: SPX/NDX = risk-on beta; VIX/MOVE = cross-asset fear; DXY = dollar liquidity;
                 JPY = carry-unwind channel (2024-08); KRW = kimchi-premium denominator; gold = "digital gold";
                 IBIT/GBTC/FBTC/ETHA volume = US spot-ETF flow proxy; MSTR = leveraged BTC treasury demand;
                 miners (MARA/RIOT/CLSK) = hashprice stress; BTC=F/ETH=F = CME basis and weekend gap.
ust_yields       US Treasury par yield curve (1990-), ust_real_yields (2003-). Mechanism: the cost of holding a
                 zero-yield asset; real yields vs BTC is a much-cited inverse link.
nyfed_effr, nyfed_sofr, nyfed_rrp, nyfed_soma   policy/funding rates, reverse repo usage, Fed securities held.
tga              Treasury General Account daily balances. With SOMA and RRP -> the "net liquidity" proxy
                 (Howell, Capital Wars, lens corpus): SOMA - TGA - RRP.
ecb_dfr, bis_policy_<CC>   ECB deposit facility rate; central-bank policy rates for US, EZ, JP, GB, CN, KR.
cftc_tff_<mkt>   CFTC Traders in Financial Futures for CME Bitcoin/Ether contracts (weekly, as-of Tuesday,
                 published Friday 15:30 ET -> knowable 3 days AFTER the stamp).
fomc_dates       FOMC statement dates (14:00 ET) scraped from federalreserve.gov. Mechanism: scheduled vol
                 event; pre-FOMC drift (#037/#038 tested on equities, never on crypto).
"""
import io
import re
import sys
import time

import pandas as pd

from lib import client, get, log_fail, save

YAHOO = ["^GSPC", "^NDX", "^RUT", "^VIX", "^VVIX", "^MOVE", "DX-Y.NYB", "^TNX", "^IRX", "^FVX", "^TYX",
         "GC=F", "SI=F", "CL=F", "HG=F", "NG=F", "JPY=X", "EURUSD=X", "KRW=X", "CNY=X", "GBPUSD=X", "TRY=X",
         "ARS=X", "NGN=X", "TLT", "HYG", "LQD", "SPY", "QQQ", "SMH", "ARKK", "GLD", "IBIT", "FBTC", "GBTC",
         "ETHA", "BITO", "MSTR", "COIN", "HOOD", "MARA", "RIOT", "CLSK", "NVDA", "BTC=F", "ETH=F", "MBT=F"]


def yahoo(cli, tk):
    j = get(cli, f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}",
            {"period1": 0, "period2": int(time.time()), "interval": "1d", "events": "div,splits"})
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({"t": pd.to_datetime(res["timestamp"], unit="s", utc=True), **q})
    if "adjclose" in res["indicators"]:
        df["adjclose"] = res["indicators"]["adjclose"][0]["adjclose"]
    df = df.dropna(subset=["close"])
    tz = res["meta"].get("exchangeTimezoneName", "UTC")
    df["local_date"] = df["t"].dt.tz_convert(tz).dt.date.astype(str)
    safe = tk.replace("^", "").replace("=", "_").replace(".", "_")
    save(df, "macro", f"yahoo_{safe}", "t", dict(
        source=f"Yahoo Finance chart {tk}", type="daily OHLCV (index opens may be synthetic; FX indicative)",
        freq="1d", stamp=f"session open instant in UTC (local date in local_date, tz {tz})",
        knowable="at that session's close", notes="Use close-to-close; lag by one session before joining to crypto."))


def ust(cli, kind, first):
    frames = []
    for y in range(first, pd.Timestamp.now().year + 1):
        r = get(cli, f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
                     f"daily-treasury-rates.csv/{y}/all",
                {"type": kind, "field_tdr_date_value": y, "page": "", "_format": "csv"}, as_json=False)
        if r is not None and r.text.strip():
            frames.append(pd.read_csv(io.StringIO(r.text)))
        time.sleep(0.3)
    df = pd.concat(frames, ignore_index=True)
    df["t"] = pd.to_datetime(df.pop("Date"), utc=True)
    name = "ust_yields" if kind == "daily_treasury_yield_curve" else "ust_real_yields"
    save(df, "macro", name, "t", dict(
        source=f"US Treasury {kind}", type="official par yields (%)", freq="1d (business days)",
        stamp="US date", knowable="that date ~18:00 ET", notes=""))


def nyfed_rate(cli, path, name):
    frames = []
    for y in range(2015, pd.Timestamp.now().year + 1):
        j = get(cli, f"https://markets.newyorkfed.org/api/rates/{path}/search.json",
                {"startDate": f"{y}-01-01", "endDate": f"{y}-12-31"})
        if j and j.get("refRates"):
            frames.append(pd.DataFrame(j["refRates"]))
    df = pd.concat(frames, ignore_index=True)
    df["t"] = pd.to_datetime(df.pop("effectiveDate"), utc=True)
    for c in df.columns:
        if c.startswith(("percent", "volume", "target")):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    save(df, "macro", name, "t", dict(source=f"NY Fed {path}", type="official reference rate (%)", freq="1d",
                                      stamp="US effective date", knowable="next business day ~08:00 ET", notes=""))


def nyfed_rrp(cli):
    frames = []
    for y in range(2013, pd.Timestamp.now().year + 1):
        j = get(cli, "https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json",
                {"startDate": f"{y}-01-01", "endDate": f"{y}-12-31"})
        ops = (j or {}).get("repo", {}).get("operations", [])
        frames.append(pd.DataFrame([{"t": o["operationDate"], "total_accepted": o.get("totalAmtAccepted"),
                                     "counterparties": o.get("participatingCpty")} for o in ops]))
    df = pd.concat(frames, ignore_index=True)
    df = df.groupby("t", as_index=False).agg({"total_accepted": "sum", "counterparties": "max"})
    save(df, "macro", "nyfed_rrp", "t", dict(source="NY Fed reverse repo operations", type="ON RRP take-up (USD)",
                                             freq="1d", stamp="US operation date", knowable="~13:15 ET same day",
                                             notes="Summed across operations per day."))


def nyfed_soma(cli):
    j = get(cli, "https://markets.newyorkfed.org/api/soma/summary.json")
    df = pd.DataFrame(j["soma"]["summary"])
    df["t"] = pd.to_datetime(df.pop("asOfDate"), utc=True)
    for c in df.columns:
        if c != "t":
            df[c] = pd.to_numeric(df[c], errors="coerce")
    save(df, "macro", "nyfed_soma", "t", dict(
        source="NY Fed SOMA summary", type="Fed securities held outright (USD)", freq="weekly (Wednesday)",
        stamp="as-of Wednesday", knowable="Thursday ~16:30 ET (H.4.1 timing)",
        notes="Proxy for the Fed balance sheet (securities are ~90% of total assets); WALCL itself is on FRED, blocked."))


def tga(cli):
    rows, page = [], 1
    while True:
        j = get(cli, "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/"
                     "operating_cash_balance",
                {"page[size]": 10000, "page[number]": page,
                 "fields": "record_date,account_type,close_today_bal,open_today_bal"})
        rows += j["data"]
        if page >= j["meta"]["total-pages"]:
            break
        page += 1
    df = pd.DataFrame(rows)
    df["t"] = pd.to_datetime(df.pop("record_date"), utc=True)
    for c in ["close_today_bal", "open_today_bal"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    save(df, "macro", "tga", "t", dict(
        source="US Treasury Daily Treasury Statement, operating cash balance", type="official balances ($mn)",
        freq="1d", stamp="US record date", knowable="next business day ~16:00 ET",
        notes="Long format: account_type naming changed in 2021-10 (Federal Reserve Account -> TGA). "
              "Post-2021 close_today_bal is null; use next day's opening balance."))


def ecb(cli):
    r = get(cli, "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.DFR.LEV",
            {"format": "csvdata"}, as_json=False)
    df = pd.read_csv(io.StringIO(r.text))[["TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "dfr"})
    df["t"] = pd.to_datetime(df.pop("TIME_PERIOD"), utc=True)
    save(df, "macro", "ecb_dfr", "t", dict(source="ECB SDW FM DFR", type="policy rate (%)", freq="business day",
                                           stamp="date", knowable="announcement date", notes=""))


def bis(cli, cc):
    r = get(cli, f"https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBPOL/1.0/D.{cc}",
            {"format": "csv"}, as_json=False)
    df = pd.read_csv(io.StringIO(r.text))
    df = df[["TIME_PERIOD", "OBS_VALUE"]].rename(columns={"OBS_VALUE": "policy_rate"})
    df["t"] = pd.to_datetime(df.pop("TIME_PERIOD"), utc=True)
    save(df, "macro", f"bis_policy_{cc}", "t", dict(source=f"BIS WS_CBPOL D.{cc}", type="policy rate (%)",
                                                   freq="1d", stamp="date", knowable="announcement", notes=""))


def cftc(cli):
    j = get(cli, "https://publicreporting.cftc.gov/resource/gpe5-46if.json",
            {"$where": "commodity_name in ('BITCOIN','ETHER')", "$limit": 50000})
    df = pd.DataFrame(j)
    df["t"] = pd.to_datetime(df.pop("report_date_as_yyyy_mm_dd"), utc=True)
    for mkt, g in df.groupby("contract_market_name"):
        g = g.copy()
        for c in g.columns:
            if c not in ("t",) and g[c].astype(str).str.match(r"^-?[\d.]+$").all():
                g[c] = pd.to_numeric(g[c])
        save(g, "macro", f"cftc_tff_{re.sub(r'[^A-Za-z0-9]+', '_', mkt).strip('_')}", "t", dict(
            source="CFTC TFF futures-only (Socrata gpe5-46if)", type="weekly positions by trader class",
            freq="weekly", stamp="as-of Tuesday", knowable="Friday 15:30 ET (3 days after stamp)",
            notes="Lag by >= 3 days before use."))


MON = {m[:3]: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                           "August", "September", "October", "November", "December"])}


def _date(y, month_txt, days_txt):
    """Statement day = last day of the meeting; a cross-month meeting ('April/May', '30-1') ends in the 2nd month."""
    m = MON[month_txt.split("/")[-1].strip()[:3]]
    d = int(re.findall(r"\d+", days_txt)[-1])
    return pd.Timestamp(year=int(y), month=m, day=d, hour=14, tz="America/New_York").tz_convert("UTC")


def fomc(cli):
    dates = set()
    txt = get(cli, "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm", as_json=False).text
    for block in txt.split('<div class="panel panel-default">'):
        y = re.search(r"(\d{4}) FOMC Meetings", block)
        if not y:
            continue
        for m, d in re.findall(r'fomc-meeting__month[^>]*><strong>([^<]+)</strong>.*?fomc-meeting__date[^>]*>([^<]+)<',
                               block, flags=re.S):
            if re.search(r"\d", d) and "notation" not in d.lower() and "unscheduled" not in d.lower():
                dates.add(_date(y.group(1), m, d))
    for y in range(2011, 2022):
        r = get(cli, f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm", as_json=False)
        if r is None:
            continue
        for m, d, m2, d2 in re.findall(
                r"<h5[^>]*>\s*([A-Za-z/]+)\s+(\d+(?:-\d+)?)(?:-([A-Za-z]+)\s+(\d+))?\s+Meeting", r.text):
            dates.add(_date(y, m2, d2) if m2 else _date(y, m, d))  # 'July 31-August 1' form
        time.sleep(0.5)
    df = pd.DataFrame({"t": sorted(dates)})
    df["event"] = "FOMC statement (scheduled meeting)"
    save(df, "macro", "fomc_dates", "t", dict(
        source="federalreserve.gov fomccalendars + fomchistorical pages", type="event calendar",
        freq="~8/yr", stamp="statement time 14:00 ET in UTC", knowable="dates published a year ahead",
        notes="Scheduled meetings only (unscheduled/notation votes excluded). 2020-03 had no scheduled statement."))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "fomc":
    with client() as cli:
        fomc(cli)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "sofr":
    with client() as cli:
        nyfed_rate(cli, "secured/sofr", "nyfed_sofr")
elif __name__ == "__main__" and len(sys.argv) == 1:
    with client() as cli:
        jobs = [(yahoo, (t,)) for t in YAHOO] + [
            (ust, ("daily_treasury_yield_curve", 1990)), (ust, ("daily_treasury_real_yield_curve", 2003)),
            (nyfed_rate, ("unsecured/effr", "nyfed_effr")), (nyfed_rate, ("secured/sofr", "nyfed_sofr")),
            (nyfed_rrp, ()), (nyfed_soma, ()), (tga, ()), (ecb, ()), (cftc, ()), (fomc, ())] + [
            (bis, (cc,)) for cc in ["US", "XM", "JP", "GB", "CN", "KR"]]
        for fn, a in jobs:
            try:
                fn(cli, *a)
            except Exception as e:
                log_fail("macro", f"{fn.__name__}{a}", e)
            time.sleep(0.5)
    print("DONE p7_macro", file=sys.stderr)


def auctions(cli):
    """Treasury auction results. Mechanism: a weak auction (high bid-to-cover tail, low indirect take-up) is a
    duration-supply shock -> yields jump -> risk-off, and crypto is the highest-beta risk asset."""
    rows, page = [], 1
    while True:
        j = get(cli, "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query",
                {"page[size]": 10000, "page[number]": page})
        rows += j["data"]
        if page >= j["meta"]["total-pages"]:
            break
        page += 1
    df = pd.DataFrame(rows).replace("null", None)
    df["t"] = pd.to_datetime(df.pop("auction_date"), utc=True)
    keep = ["t", "security_type", "security_term", "cusip", "offering_amt", "total_accepted", "total_tendered",
            "bid_to_cover_ratio", "high_yield", "high_discnt_rate", "high_investment_rate", "avg_med_yield",
            "indirect_bidder_accepted", "direct_bidder_accepted", "primary_dealer_accepted", "issue_date"]
    df = df[[c for c in keep if c in df.columns]]
    for c in df.columns[4:-1]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    save(df, "macro", "ust_auctions", "t", dict(
        source="Treasury fiscaldata auctions_query", type="auction results", freq="event",
        stamp="auction date (results ~13:00 ET)", knowable="auction day 13:00 ET",
        notes="Future-dated rows are announced auctions without results."))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "auctions":
    with client() as cli:
        auctions(cli)
