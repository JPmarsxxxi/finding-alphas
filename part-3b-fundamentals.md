# Part III-B — Fundamentals & Financial Statements (Ch. 19, 20)

*Building alphas from accounting data. Low turnover, low coverage, longer payoff. Ch. 19 (factor catalog) and Ch. 20 (analysis) overlap heavily — merged here.*

---

## The four statements

| Statement | What it shows | Key identity |
|---|---|---|
| **Balance sheet** | snapshot at a point in time | `Assets = Liabilities + Equity` |
| **Income statement** | performance over a period (accrual-based) | net sales → gross margin → income from ops → net income |
| **Cash flow** | cash in/out over a period | `cash flow = ops + borrowings + stock sale − purchases − taxes` |
| **Shareholders' equity** | change in net worth | paid-in capital, retained earnings |

Audited annual statements are most authoritative; preliminary quarterly numbers can be revised.

---

## Factor catalog (Piotroski-style, +correlated with future returns)

**Balance sheet:** ↑liquidity (current assets/current liabilities), ↑sales/total assets, no equity issuance, less long-term debt.
**Income statement:** net income > 0, ↑net income/total assets, ↑gross margin.
**Cash flow:** cash from ops > 0, cash from ops > net income.
**Growth stocks** (low book-to-market; Chan et al., Bartov-Mohanram) — vs industry median: net income/assets, cash flow/assets, R&D/assets, capex/assets, advertising/assets all above median; income variances below median.
**Governance** (Abarbanell-Bushee): ↓inventory/sales, ↑receivables/sales, ↓admin expense/sales, improved tax rate, FIFO↔LIFO changes, sales/employee.

**Negative / short factors** (Beneish-Nichols, Nissim-Penman): net sales > free cash flow, low book-to-price, high sales growth, low CFO/price, acquisition in past 5yr, equity issuance > industry avg, **high financial leverage** (net financing debt / common equity → liquidity/insolvency risk; cf. LTCM, Enron).

**Normalization:** total assets is the standard normalizer to compare across companies/time (consider discounting goodwill).

---

## Analysis techniques (Ch. 20)

- **Valuation ratios**: P/E, P/B, P/S, dividend yield → label stocks **value** (low P/E, P/B, P/S; high yield) vs **growth** (opposite).
- **Accruals anomaly (Sloan):** earnings = cash flow + accruals. Scale by total assets, rank into deciles. **Cash-flow component predicts future earnings far better than the accruals component** → rely on cash-flow earnings, distrust accrual-heavy earnings.
- **Footnotes:** unstructured text holding red flags (accounting changes, litigation, options). Many new footnotes / obscure ones = warning. Needs text-mining → uncorrelated signals.
- **Conference calls:** management/analyst tone predicts earnings surprises over next ~60 days; analyst interest predicts fundamentals over next 3mo; extreme words → abnormal volume/returns.
- **Sell-side reports:** the **"surprise" (consensus vs actual) often matters more than the fundamentals themselves** because consensus is already priced in. Analyst views can be self-fulfilling short-term.
- **Macro overlays:** oil↔transportation, rates↔financials.

---

## Converting factors → alphas (the practical rules)

- **Use rate-of-change** (subtract prior year), not raw levels — kills seasonality in quarter-over-quarter comparisons.
- **Point-in-time data** — removes the forward bias from statement refilings (gives *worse* but *realistic* backtests).
- **Factors-as-screens**: assign +1 per passed test, sum, go long the highest-scored (reasonable absent deeper stats; Kahneman 2011).
- Beyond screens: multifactor regression, factor-correlation analysis, ML/genetic search for good factor combinations.
- **Industry matters**: commodity-based sales ≠ improved performance; banks report differently; business-cycle phase changes debt↔price correlation.

**Profile:** fundamental alphas → low turnover, low stock coverage, returns concentrate around the next earnings announcement and level off ~1yr after disclosure.

**Checklist:** pull point-in-time data → compute rate-of-change ratios → normalize by total assets / industry median → screen or regress → expect low turnover & long horizon → watch leverage & accruals as red flags.
