# Economist lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Ilmanen, *Expected Returns: An Investor's Guide to Harvesting Market Rewards*** (Wiley 2011) | Central bank PM, Finland; a decade at Salomon/Citi as bond researcher, strategist, MD and trader; senior PM at Brevan Howard; principal at AQR | 1.55M chars — the largest single source in any corpus here. Risk premia across asset classes, and what is actually paid for | `ilmanen_expected_returns.txt` |
| **Ilmanen, *Investing Amid Low Expected Returns*** (2022) | as above | 860k chars. The same framework re-run once the premia have compressed | `ilmanen_investing_amid_low_expected_returns.txt` |

## Gaps

- **Bookstaber, *A Demon of Our Own Design*** (Wiley 2007) — backs F5 (reflexive forced selling) and F3. Not obtained.

## NO-SECTION-INDEX — grep these, do not assume structure

Contents-page matching and typography detection both failed. Left as whole-book `.txt`:
`grep -n` for the term, then read around the hit with `sed -n 'START,ENDp'`.

- `ilmanen_investing_amid_low_expected_returns.txt` — 674pp, 884k chars. Contents match failed (10 entries, 2 located) and the render carries **no font-size variation at all** (1 candidate opener across 674 pages), so typography cannot help either. *Expected Returns* — the larger and more useful book — split cleanly into 30 sections; start there.

## Backbone — Bookstaber (book not obtained)

*A Demon of Our Own Design* is commercial. Bookstaber's Office of Financial Research working papers
are free and carry the same argument in measurable form:

| paper | pp | what it backs |
|---|---:|---|
| **Bookstaber, *Using Agent-Based Models for Analyzing Threats to Financial Stability*** (OFR WP 0003, 2012) | 24 | F5 — forced selling is reflexive; why top-down equilibrium models cannot see it |
| **Bookstaber, Paddrik & Tivnan, *An Agent-based Model for Financial Vulnerability*** (OFR WP 2014-05) | 37 | F5, F3 — the mechanism made explicit, with funding and collateral channels |

He wrote these as the OFR's Head of Risk Modelling — the same person, the regulator-side view.
