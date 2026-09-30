"""Family `defi`: DefiLlama free API. ALL series are vendor-aggregated and BACKFILLED (new protocols are added
with history, bugs are corrected in place) -> NOT point-in-time. Use for regime/conditioning, check robustness.

stable_total, stable_<SYM>     stablecoin circulating USD. Mechanism: mints = new dollars arriving to buy crypto;
                               USDT mints historically cluster before rallies; burns = capital leaving.
stable_chain_<CHAIN>           stablecoins parked on a chain = dry powder for that ecosystem (ETH, SOL, BNB, TRON).
tvl_<CHAIN>                    value locked. Mechanism: capital rotating into an ecosystem ahead of its token.
dex_<CHAIN>, dex_total         DEX volume. Mechanism: on-chain speculation share; DEX/CEX volume ratio.
fees_total                     fees paid across protocols = real usage/speculative heat.
perpdex_oi_total               open interest on perp DEXes = leverage built off-exchange.
hacks                          event list: date, amount, chain, technique. Mechanism: large hacks force selling
                               of the stolen coin and contagion across its chain.
"""
import sys
import time

import pandas as pd

from lib import client, get, log_fail, save

PROV = dict(source="DefiLlama", freq="1d", stamp="UTC day", knowable="day end (but BACKFILLED: not PIT)",
            type="vendor aggregate")


def daily(pairs, col):
    df = pd.DataFrame(pairs, columns=["t", col])
    df["t"] = pd.to_datetime(pd.to_numeric(df["t"]), unit="s", utc=True)
    return df


def run(name, fn):
    try:
        df, notes = fn()
        save(df, "defi", name, "t", {**PROV, "notes": notes})
    except Exception as e:
        log_fail("defi", name, e)
    time.sleep(1)


def stable(cli, path, col="usd"):
    j = get(cli, f"https://stablecoins.llama.fi/{path}")
    rows = [(int(x["date"]), (x.get("totalCirculatingUSD") or {}).get("peggedUSD")) for x in j]
    return daily(rows, col), path


def tvl(cli, chain):
    j = get(cli, f"https://api.llama.fi/v2/historicalChainTvl{('/' + chain) if chain else ''}")
    return daily([(x["date"], x["tvl"]) for x in j], "tvl_usd"), f"historicalChainTvl/{chain or 'all'}"


def overview(cli, kind, chain=None):
    url = f"https://api.llama.fi/overview/{kind}{('/' + chain) if chain else ''}"
    j = get(cli, url, {"excludeTotalDataChartBreakdown": "true", "excludeTotalDataChart": "false"})
    return daily(j["totalDataChart"], f"{kind}_usd"), url


def hacks(cli):
    df = pd.DataFrame(get(cli, "https://api.llama.fi/hacks"))
    df["t"] = pd.to_datetime(df.pop("date"), unit="s", utc=True)
    for c in df.columns:
        if df[c].map(lambda v: isinstance(v, (list, dict))).any():
            df[c] = df[c].map(lambda v: ",".join(map(str, v)) if isinstance(v, list) else str(v) if v is not None else None)
    return df, "api.llama.fi/hacks; amount in USD"


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "hacks":
    with client() as cli:
        run("hacks", lambda: hacks(cli))
elif __name__ == "__main__":
    with client() as cli:
        run("stable_total", lambda: stable(cli, "stablecoincharts/all"))
        for sid, sym in [(1, "USDT"), (2, "USDC"), (5, "DAI"), (146, "USDe")]:
            run(f"stable_{sym}", lambda sid=sid: stable(cli, f"stablecoincharts/all?stablecoin={sid}"))
        for ch in ["Ethereum", "Tron", "Solana", "BSC", "Arbitrum", "Base"]:
            run(f"stable_chain_{ch}", lambda ch=ch: stable(cli, f"stablecoincharts/{ch}"))
        run("tvl_all", lambda: tvl(cli, None))
        for ch in ["Ethereum", "Solana", "BSC", "Tron", "Arbitrum", "Base", "Polkadot", "Cardano", "Litecoin",
                   "Dogechain", "Bitcoin"]:
            run(f"tvl_{ch}", lambda ch=ch: tvl(cli, ch))
        run("dex_total", lambda: overview(cli, "dexs"))
        for ch in ["ethereum", "solana", "bsc", "arbitrum", "base"]:
            run(f"dex_{ch}", lambda ch=ch: overview(cli, "dexs", ch))
        run("fees_total", lambda: overview(cli, "fees"))
        run("perpdex_oi_total", lambda: overview(cli, "open-interest"))
        run("hacks", lambda: hacks(cli))
    print("DONE p5_defi", file=sys.stderr)
