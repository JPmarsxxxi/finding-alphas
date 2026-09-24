# Market Maker lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Sinclair, *Volatility Trading*** (Wiley) — indexed, 17 sections | LIFFE floor clerk -> DAX/EuroStoxx options market maker -> prop trader, Bluefin -> Talton Capital; PhD physics, Bristol | 227pp. Option pricing, volatility measurement and forecasting, hedging, position sizing | `sinclair_volatility_trading/INDEX.md` |
| **Sinclair, *Positional Option Trading: An Advanced Guide*** | as above | 392k chars | `sinclair_positional_option_trading.txt` |

## Gaps

- **Bouchaud, Bonart, Donier & Gould, *Trades, Quotes and Prices*** (CUP) — backs F3-F5 (concave impact, long-memory order flow, hidden liquidity). Not obtained; **most of the underlying papers are free on arXiv** and would make a usable backbone.

## Backbone — *Trades, Quotes and Prices* (not obtained)

The book is commercial. Its content is largely the authors' own papers, which are free on arXiv, so
the backbone is held instead:

| paper | pp | what it backs |
|---|---:|---|
| **Bouchaud, Farmer & Lillo, *How Markets Slowly Digest Changes in Supply and Demand*** (2008) | 111 | F3, F4, F6 — the long-form handbook chapter; impact, order-flow memory, and why liquidity is revealed slowly |
| **Bouchaud et al., *Fluctuations and Response in Financial Markets*** (2003) | 30 | F3 — the response function and the subtle nature of price changes |
| **Tóth, Bouchaud et al., *Anomalous Price Impact and the Critical Nature of Liquidity*** (2011) | 16 | F3 — square-root impact, and liquidity as a critical phenomenon |
| **Lillo & Farmer, *The Long Memory of the Efficient Market*** (2004) | 19 | F4 — order-flow sign autocorrelation over hours, from order splitting |

Together these are the argument of the book; what is missing is its textbook framing and the
order-book mechanics chapters.
