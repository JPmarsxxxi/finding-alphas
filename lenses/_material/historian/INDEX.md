# Historian lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Marks, *Mastering the Market Cycle*** (2018) | Citicorp senior PM (convertibles, high yield); led distressed / high-yield / convertibles at TCW 1985-95; co-founded Oaktree 1995 | 245pp, **18 chapters — repaired and hand-mapped** (see note below). Where you are in a cycle as an actionable state, without forecasting: the economic cycle, the pendulum of investor psychology, attitudes to risk, credit, distressed debt, real estate, and cycle positioning | `marks_mastering_the_market_cycle/INDEX.md` |
| **Harris, *Trading and Exchanges*** — **PARTIAL** | Chief Economist of the SEC 2002-04; contributed to Reg NMS | WARNING: **113pp of a ~640pp book.** 280 bookmarks but only a fraction of the content — treat as an excerpt and say so if a pass leans on it | `harris_trading_and_exchanges_PARTIAL.txt` |

## Gaps

- **Harris, *Trading and Exchanges*** — the full book. What is held is an excerpt.
- **The Oaktree memos** — free at oaktreecapital.com, decades of them. Not yet fetched.

## Repair note — Marks

The supplied `.odg` had a text layer with **no word spaces at all**: 0% spaces, average token 21
characters (`Thisbookpresentstheideasofitsauthor`). It was unusable for grep.

Fix: re-rendered to PDF through LibreOffice, so the PDF extractor could infer word boundaries from
glyph positions, then line breaks were normalised back into prose. Result: 15.8% spaces, average word
4.9 — normal.

**Measured residual damage:** 0.11% of tokens are run together (`calledThe`, `StudyCycles` — which is
why chapter I reads "Why Studycycles?"), 0.44% are suspiciously long, and a few short spans were
dropped outright. **Good enough to grep and read; check the PDF page before quoting a phrase.**
Both the repaired `.pdf` and the original `.odg` are kept.
