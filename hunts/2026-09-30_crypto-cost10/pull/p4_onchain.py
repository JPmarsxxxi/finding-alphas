"""Family `onchain`: blockchain-derived data.

cm_<asset>           Coin Metrics community (free) daily metrics, every free metric per asset.
                     Mechanisms: FlowInEx/SplyEx = coins moving onto exchanges -> supply about to be sold;
                     CapMVRVCur = market cap / realised cap -> holders' average unrealised profit (profit-taking
                     pressure at extremes); HashRate/IssTot = miner economics (forced selling when margins squeeze);
                     AdrActCnt/TxCnt = network use.
                     PIT WARNING: exchange-flow metrics rest on address labels that are revised backwards as
                     labelling improves; values for old dates are today's view, not what was knowable then.
mempool_*            mempool.space: per-block-group fee percentiles, hashrate + difficulty, difficulty adjustments.
                     Mechanisms: fee spikes = urgency (panic moves to exchanges); difficulty adjustments are a
                     scheduled supply-side event every 2016 blocks.
bcom_<chart>         blockchain.com charts (mempool size/count, miner revenue, fees, unique addresses, volume).
                     Mechanism: hashprice = miner revenue / hashrate; miner capitulation.
"""
import sys
import time

import pandas as pd

from lib import client, get, log_fail, save

CM = "https://community-api.coinmetrics.io/v4"
ASSETS = {"btc": "BTC", "eth": "ETH", "bnb": "BNB", "sol": "SOL", "doge": "DOGE", "xrp": "XRP",
          "ada": "ADA", "bch": "BCH", "dot": "DOT", "ltc": "LTC"}


def coinmetrics(cli, a):
    cat = get(cli, f"{CM}/catalog-v2/asset-metrics", {"assets": a, "page_size": 1000})
    if not cat or not cat.get("data"):
        return log_fail("onchain", f"cm_{a}", "not in catalog")
    ms = [m["metric"] for m in cat["data"][0]["metrics"]
          if any(f.get("community") and f["frequency"] == "1d" for f in m["frequencies"])]
    ms = [m for m in ms if m not in ("AssetCompletionTime", "AssetEODCompletionTime")]
    frames = []
    for i in range(0, len(ms), 10):
        chunk = ms[i:i + 10]
        rows, token = [], None
        while True:
            p = {"assets": a, "metrics": ",".join(chunk), "frequency": "1d", "page_size": 10000,
                 "start_time": "2009-01-01", "ignore_forbidden_errors": "true", "ignore_unsupported_errors": "true"}
            if token:
                p["next_page_token"] = token
            j = get(cli, f"{CM}/timeseries/asset-metrics", p)
            rows += j.get("data", [])
            token = j.get("next_page_token")
            if not token:
                break
            time.sleep(0.7)
        if rows:
            frames.append(pd.DataFrame(rows).drop(columns=["asset"]).set_index("time"))
        time.sleep(0.7)
    df = pd.concat(frames, axis=1).reset_index()
    df = df.loc[:, ~df.columns.duplicated()]
    for c in df.columns:
        if c != "time" and not c.endswith("-status"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[[c for c in df.columns if not c.endswith("-status")]]
    save(df, "onchain", f"cm_{ASSETS[a]}", "time", dict(
        source=f"Coin Metrics community API, {a}", type="on-chain daily aggregates", freq="1d",
        stamp="UTC day (00:00 = the day's aggregate)", knowable="after day end (~00:00-02:00 UTC next day)",
        notes="Exchange-flow metrics are label-based and revised backwards (NOT point-in-time)."))


def mempool(cli):
    j = get(cli, "https://mempool.space/api/v1/mining/blocks/fee-rates/all")
    df = pd.DataFrame(j)
    df["t"] = pd.to_datetime(df.pop("timestamp"), unit="s", utc=True)
    save(df, "onchain", "mempool_feerates", "t", dict(
        source="mempool.space mining/blocks/fee-rates/all", type="fee-rate percentiles per block group (sat/vB)",
        freq="~daily groups of blocks", stamp="UTC block-group timestamp", knowable="at stamp", notes=""))
    j = get(cli, "https://mempool.space/api/v1/mining/hashrate/all")
    h = pd.DataFrame(j["hashrates"])
    h["t"] = pd.to_datetime(h.pop("timestamp"), unit="s", utc=True)
    h["avgHashrate"] = h["avgHashrate"].astype(float)
    save(h, "onchain", "mempool_hashrate", "t", dict(
        source="mempool.space mining/hashrate/all", type="estimated network hashrate", freq="1d",
        stamp="UTC day", knowable="day end", notes=""))
    d = pd.DataFrame(get(cli, "https://mempool.space/api/v1/mining/difficulty-adjustments/all"),
                     columns=["timestamp", "height", "difficulty", "change"])
    d["t"] = pd.to_datetime(d.pop("timestamp"), unit="s", utc=True)
    save(d, "onchain", "mempool_difficulty_adj", "t", dict(
        source="mempool.space difficulty-adjustments/all", type="event list: difficulty retargets",
        freq="every 2016 blocks (~2 weeks)", stamp="UTC block time", knowable="at stamp; date predictable ahead",
        notes="change = ratio new/old."))


BCOM = ["mempool-size", "mempool-count", "mempool-growth", "miners-revenue", "transaction-fees-usd",
        "n-unique-addresses", "n-transactions", "estimated-transaction-volume-usd", "hash-rate", "difficulty",
        "avg-block-size", "median-confirmation-time", "output-volume", "trade-volume", "cost-per-transaction"]


def bcom(cli, chart):
    j = get(cli, f"https://api.blockchain.info/charts/{chart}",
            {"timespan": "all", "format": "json", "sampled": "false"})
    df = pd.DataFrame(j["values"]).rename(columns={"x": "t", "y": chart.replace("-", "_")})
    df["t"] = pd.to_datetime(df["t"], unit="s", utc=True)
    save(df, "onchain", f"bcom_{chart.replace('-', '_')}", "t", dict(
        source=f"blockchain.com charts/{chart}", type="BTC network aggregate", freq=j.get("period", "day"),
        stamp="UTC period start", knowable="period end", notes=j.get("description", "")[:200]))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "mempool":
    with client() as cli:
        mempool(cli)
elif __name__ == "__main__":
    with client() as cli:
        for a in ASSETS:
            try:
                coinmetrics(cli, a)
            except Exception as e:
                log_fail("onchain", f"cm_{a}", e)
        try:
            mempool(cli)
        except Exception as e:
            log_fail("onchain", "mempool", e)
        for c in BCOM:
            try:
                bcom(cli, c)
            except Exception as e:
                log_fail("onchain", f"bcom_{c}", e)
            time.sleep(1)
    print("DONE p4_onchain", file=sys.stderr)
