# Part II-C — The Overfitting Defense (Ch. 9–10)

*The heart of the book. Backtesting tells you what worked historically; the entire skill is telling a real signal apart from a lucky fit. Ch. 9 = the statistics of overfitting; Ch. 10 = the human/process biases that cause it.*

---

## Why prediction is only "statistical" (Ch. 9)

You cannot predict one stock on one day with confidence. Prediction works only **in aggregate** — over many bets, random errors average out. A real price-driving rule should be predictive **across all instruments over all days**, not on a hand-picked slice.

Same rule → many uncorrelated alphas via different *implementations* (different ways to compute the mean, define reversion, etc.). Distinguish the **idea's essential constraints** from **implementation choices** (the "wheel needn't be round — just convex, constant-width" analogy). An *ensemble of implementations* beats any single one.

---

## The overfitting trap, quantified (Ch. 9, Table 9.1)

If you try enough random configs, you will find a great Sharpe by pure luck (true OOS Sharpe = 0):

| Days | Configs to expect a Sharpe-2 by chance |
|---|---|
| 250 | ~21 |
| 500 | ~197 |
| 1,000 | ~13,700 |

Modern compute makes this *easy* to do accidentally. The "**3964 World Cup formula**" is the parable: a beautiful numeric pattern that predicted nothing. Lesson — playing with numbers finds significant-looking results; only an underlying **price-driving principle** separates signal from noise.

---

## How to avoid overfitting (Ch. 9 checklist)

- [ ] **True out-of-sample test.** OOS means *forward* — build, then test daily going forward. NOT true OOS: (1) backtest recent N yrs then use *earlier* data as "OOS" (history influenced the recent period); (2) fit on some instruments, "OOS" on others (instruments are correlated).
  - ⚠️ As the *number* of alphas tested OOS grows, single-alpha OOS performance becomes biased — one wins by luck. Judge in aggregate.
- [ ] **Raise the in-sample Sharpe bar.** Higher Sharpe → less overfit risk. Wider universe → higher Sharpe via breadth: **IR = IC × √breadth** (fundamental law, Grinold & Kahn).
- [ ] **Test over longer history** (Table 9.1) — but not so long the market regime no longer applies.
- [ ] **Cross-validate across instruments/regions** — good alphas travel (US → Europe → Asia).
- [ ] **Make it elegant**: simple, has a theory/story, and **units must add up** (can't add dollar-returns to share-counts).
- [ ] **Minimize parameters & operations** — fewer degrees of freedom = less sensitivity; extra fitting eventually has *negative* value.

> Caveat from the authors: papers & sell-side reports publish only winners. They don't report how many things they tried or their failures, and many results don't reproduce. Treat them as idea sources, not validated alphas.

---

## Controlling biases (Ch. 10)

### Systematic biases (coded in accidentally)
- **Look-ahead bias** — using data not yet available. Causes:
  - *Timestamping*: dual-timestamp every datum with **occurrence** time and **arrival** time. Key off *arrival*. This is **point-in-time data**. Watch revised series (GDP), vendor corrections, and **time zones** for multi-region strategies.
  - *In ML*: tune hyper-parameters on **backward-looking data only**; beware sentiment dictionaries trained on future data.
- **Data mining** — tinkering until in-sample looks good. Control with **holdouts**:
  - *Time-series holdout*: omit a continuous stretch (usually the end) OR interleaved stretches (watch seasonality/autocorrelation).
  - *Asset holdout*: hold out a representative, relatively-independent set (no country/industry/size/liquidity skew).
- **Formulation bias** — which formulation (3/6/12-month momentum? mean vs RMS volume?). Mitigate by **diversifying across formulations** with an unbiased weighting (equal weight, risk parity) rather than picking one.

### Behavioral biases (ad hoc human decisions)
- **Storytelling / theory-fitting** — inventing an unverifiable story to justify performance ("reversion just doesn't work for French stocks").
- **Confirmation bias** — believing what fits your priors; "latest research = greatest" fallacy.
- **Familiarity bias** — only S&P 500, only one signal style, only nearby/known names.
- **Narrow framing** — deciding without considering the whole portfolio (e.g. changing models mid-drawdown).
- **Availability bias** — overweighting recent memorable events (Brexit-won't-happen-because-Grexit-didn't).
- **Herding** — crowding into the same positions; quants are notoriously correlated → use **differentiating research**.

**Best practical defense:** write a **drawdown playbook in advance**. The urge to act on bias peaks during drawdowns; pre-commitment removes the in-the-moment decision. Containing systematic bias takes sustained engineering (point-in-time data, holdouts); containing behavioral bias takes awareness + reduced ad hoc intervention.

---

## One-line summary

Every other chapter in the book is an overfitting defense wearing a different hat. The unifying cure: **robust general principles, true forward OOS, fewer parameters, aggregate (not single-alpha) judgment, and pre-committed discipline.**
