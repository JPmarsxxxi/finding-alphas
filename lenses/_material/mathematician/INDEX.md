# Mathematician lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Thorp, *A Man for All Markets*** — indexed, 45 sections | Founded Convertible Hedge Associates 1969 -> Princeton/Newport Partners; derived Black-Scholes-equivalent pricing before publication | 407pp | `thorp_a_man_for_all_markets/INDEX.md` |
| **Thorp, *Beat the Market*** (1967) | as above | 287k chars. The original warrant-hedging identity work | `thorp_beat_the_market.txt` |
| **Derman, *My Life as a Quant*** | MD, Goldman Sachs; ran quantitative strategies research in fixed income, equities and risk 1985-2002; Black-Derman-Toy and Derman-Kani | 643k chars | `derman_my_life_as_a_quant.txt` |
| **Thorp, *Beat the Dealer*** | as above | 215pp. Blackjack, not markets — *tangential; kept because the edge-and-bet-sizing reasoning is the same object the poker lens uses* | `thorp_beat_the_dealer.txt` |

## Gaps

- **Derman, *Models.Behaving.Badly.*** — the epistemics half. Not obtained.

## NO-SECTION-INDEX — grep these, do not assume structure

Contents-page matching and typography detection both failed. Left as whole-book `.txt`:
`grep -n` for the term, then read around the hit with `sed -n 'START,ENDp'`.

- `thorp_beat_the_market.txt` — 239pp, 294k chars. No contents page in the export; font detection finds 7 candidates but leaves one section at 35% of the book.
- `thorp_beat_the_dealer.txt` — 215pp, 356k chars. Blackjack rather than markets; not worth hand-mapping unless a pass needs it.

## Backbone — the IDENTITY material (added after an audit)

**Honest reading of this corpus:** three of its four books are *memoirs*. `A Man for All Markets` and
`My Life as a Quant` are autobiography; only *Beat the Market* (1967) is on-topic, and it is the one
with no section index. The lens's fundamentals are about relationships **forced true by construction**
and the residual when they fail — which memoirs do not teach.

| source | pp | what it backs |
|---|---:|---|
| **Gatheral & Jacquier, *Arbitrage-Free SVI Volatility Surfaces*** (arXiv 1204.0646) | 27 | F1, F4 — no-arbitrage stated as explicit constraints a surface MUST satisfy, and what breaks when it does not |

### Identity failures already held — in another lens's folder

The best evidence for F4 (*identities fail for reasons, and the reason is always a cost or a
constraint*) is in `../behavioural/thaler_advances_v2/`. **Do not re-fetch it; cite across.**

| what | where |
|---|---|
| **Twin shares** — Royal Dutch / Shell, an identity that traded 30%+ away from parity for years | `thaler_advances_v2/ch03_how_are_stock_prices_affected_by_the_location_of_tra.txt` (Froot & Dabora) |
| **Carve-outs** — 3Com/Palm, where the market could not add and subtract | `thaler_advances_v2/ch04_can_the_market_add_and_subtract_mispricing_in_tech_s.txt` (Lamont & Thaler) |
| **Why they persist** — fundamental risk, noise-trader risk, implementation costs | `thaler_advances_v2/ch02_the_limits_of_arbitrage.txt` (Shleifer & Vishny) |
| **CIP, an identity that measurably fails** | `../rates/borio_etal_covered_interest_parity_lost_bis2016.txt` |

## Gaps

- A **relative-value / arbitrage method** text. The identity *evidence* is now covered by the
  cross-references above, but nothing here teaches how to construct and hedge one.
- **Derman, *Models.Behaving.Badly.*** — the epistemics half (model vs theory vs identity).
