# Part III-D — Stock Signals from the Options Market (Ch. 23)

*Options traders are informed & leveraged, so option prices/volumes can lead the stock. Four signal families, each a worked long–short equity alpha.*

---

## Why options carry stock-return information

Options give leveraged, direction-precise exposure → informed traders have incentive to trade options first → option data can be a **leading** signal for the underlying. Key building block is **implied volatility** (the σ that makes a pricing model like Black-Scholes match the option's market price).

**Put-call parity** (European, non-dividend stock):
```
C − P = S − D·K
```
`C`,`P` = call/put price, `S` = spot, `K` = strike, `D` = discount factor. For American options (early exercise) it becomes an inequality `S ≥ D·K + C − P`, creating a **volatility spread** between call & put IVs.

---

## The four signal families

### 1. Volatility skew
Plot IV vs strike → skewed curve. Skew = IV difference across OTM/ATM/ITM. Money managers prefer writing calls → characteristic skew. **Higher skew → underperformance** (Xing et al.: ~10.9%/yr risk-adjusted underperformance for high-skew names; predicts negative jumps around earnings).
```
Alpha = −(change in slope of the implied-volatility curve)
```
→ buy stocks whose skew is *decreasing*, short whose skew is *increasing*. (Russell 1000 in the book.)

### 2. Volatility spread
Excess demand for calls vs puts (informed bullishness) lifts call IV relative to put IV. Cremers-Weinbaum: high-spread stocks outperform low-spread by ~50 bps/week.
```
Alpha = implied volatility of ATM (call options − put options)
```
→ buy high call-minus-put IV, short low. (Russell 3000.)

### 3. Options trading volume (O/S)
`O/S` = total option volume / total equity volume. Reflects informed private info. Johnson-So: **low-O/S companies outperform high-O/S** (short-sale costs push informed bears into options) → ~1.47% monthly hedged return; O/S also predicts earnings surprises.
```
Alpha = stock trading volume / (call + put option trading volume)
```
→ buy *high* stock-to-option-volume (= low O/S), short low. (Russell 1000.)

### 4. Option open interest (OI)
OI = outstanding contracts. Informed traders express bullish views via long calls, bearish via long puts. Fodor et al.: rising put OI → underperformance; the **call-OI / put-OI ratio** is the most effective predictor (positive).
```
Alpha = open interest of call options / open interest of put options
```
→ buy high call/put OI, short low. (Russell 3000.)

---

## Checklist

- [ ] Compute IV from a pricing model; derive skew, ATM call-vs-put spread.
- [ ] Build the four signals: `−Δskew slope`, `ATM(callIV − putIV)`, `stockVol/(callVol+putVol)`, `callOI/putOI`.
- [ ] Go long the "bullish-options" side, short the "bearish-options" side; neutralize as usual.
- [ ] Note the asymmetry: options info advantage is **stronger for negative news** (short-sale-cost story).
- [ ] These need an options data feed (PHLX, OCC) — heavier data dependency than price-volume.
