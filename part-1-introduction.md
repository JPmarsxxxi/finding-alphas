# Finding Alphas — Part I: Introduction (Summary Notes)

*Source: Tulchinsky et al., Finding Alphas, 2nd ed. (WorldQuant / Wiley, 2020). Covers Ch. 1–3, pp. 1–44.*

---

## Ch. 1 — Introduction to Alpha Design (Igor Tulchinsky)

**What an alpha is.** Fundamentally, an alpha is *an idea about how the market works*. Concretely, it's an automated predictive model that decodes some market relation, built as an algorithm = mathematical expression + computer source code + configuration parameters. It contains rules that convert **input data → positions/trades** in the securities markets.

- Historical root: "Jensen's alpha" (Michael Jensen, 1968) — risk-adjusted return vs. the expected market. Evolved into "alpha" = returns exceeding a market/benchmark.
- WorldQuant usage differs: an alpha is an *individual trading signal* that seeks to add value to a portfolio, not the whole strategy.
- Why they should exist: even in efficient markets, *something* has to push prices toward equilibrium → opportunity always exists. An alpha is "a signal in an always-noisy market."

**Alphas live on CHANGES in data.** Prices change in response to events; events show up in data. *If the data never changes, there is no alpha.* Changes convey information; a change in information should produce a change in the alpha.

Common ways to express a change (Table 1.1):
| Form | Example |
|---|---|
| Difference `A − B` | `today_price − yesterday_price` |
| Ratio `A / B` | `today_price / yesterday_price` |
| Expression | `1 / today_price` (buy more when price is low) |

Expression → hypothesis pairs (Table 1.2):
| Expression | Hypothesis |
|---|---|
| `1/price` | Invest more if price is low |
| `delay(price,3)` based move | Price continues its 3-day direction |
| `price` | High-priced stocks go higher |
| `correlation(price, delay(price,1))` | Stocks that trend, outperform |
| `(price/delay(price,3)) * rank(volume)` | Trending stocks with rising volume outperform |

**Defining quality.** Information ratio = daily return / daily volatility; measures strength + steadiness of the signal (true signal vs. noise). Traits of a quality alpha:
- The idea and expression are **simple**.
- The expression/code is **elegant**.
- Good **in-sample Sharpe** ratio.
- **Not sensitive** to small changes in data or parameters.
- Works in **multiple universes**.
- Works in **different regions**.

> Caveat: until an alpha is tested, put into production, and observed **out of sample**, you don't really know how good it is.

**Alpha construction — 5 steps:**
1. Analyze the variables in the data.
2. Get an idea of the price response to the change you want to model.
3. Write a math expression that translates that change into stock positions.
4. Test the expression.
5. If the result is favorable, submit the alpha.

---

## Ch. 2 — Perspectives on Alpha Research (Geoffrey Lauprete)

**Formal definition.** An alpha is a *function*: it takes data expected to be relevant to future prices and outputs forecasted prices/returns for each instrument in its universe, **relative to a benchmark**. Implemented in C++, Python, etc.

**Brief history.** Forecasting predates computers (de la Vega, *Confusion of Confusions*, 1688; Charles Dow → technical analysis). Affordable computing hit Wall Street in the 1980s → PhDs/quants arrive. Simons founds Renaissance Technologies (1982); David Shaw founds D.E. Shaw (1988). By Jan 2018, ~1/3 of hedge-fund assets ran on systematic methods. "Black box" stigma faded as track records held up. Bumps along the way: **2007 quant meltdown** (crowded de-leveraging stampede), 2008 GFC.

**Statistical arbitrage (stat arb).** Unlike *pure* arbitrage (risk-free, locked-in profit), stat arb exploits relationships among asset prices *estimated from historical data*. Because estimation is imperfect and relationships are unknown/complex, profit is **uncertain** — subject to estimation error, overfitting, incomplete information, and shifting market dynamics. Goal: separate valid relationships from bogus ones via data analysis + hypothesis testing.

- Academia is a source of ideas (CAPM → Sharpe 1964 → Fama–French → factor models) but its models are often incomplete or built on unrealistic assumptions, so they can be hard to use directly. E.g. regressions minimize mean-squared error for convenience, but traders care more about steady cash flow + downside management. Real objectives live in firms' proprietary trade secrets.

**Do alphas even exist? (EMH debate).** Efficient Market Hypothesis: prices reflect all available information → patterns aren't exploitable, prices ~ random walk.
- Counter (behavioral economics): imperfections from overconfidence, overreaction, cognitive biases.
- Key self-defeating argument: *if no one bothered to gather/analyze info, prices wouldn't reflect it, so the market wouldn't be efficient — which would attract profit-seekers to do the analysis.* **Therefore some investors must profit from analyzing information.** (This is the Grossman–Stiglitz idea.)

**Reducing complexity via relative prices.** Predicting an absolute price requires understanding (1) the stock, (2) its industry, (3) the whole world economy. Instead, predict a stock **relative to peers in its industry** → (2) and (3) drop out. Monetize via **market-neutral** strategies.

**Evaluation pointers.**
- Good in-sample ≠ good out-of-sample.
- **Outliers** can ruin a model.
- **Multiple-hypothesis testing**: the more ideas/alternatives you sift, the *lower* the chance your chosen "winner" is real and not a statistical artifact.
- An out-of-sample period is necessary. Longer OOS → more confidence but less in-sample data to calibrate. Optimal in/out ratio depends on model complexity.

**Backtesting cautions (Looking Back).**
- History doesn't repeat exactly — a great backtest is only a *level of confidence*, not a guarantee.
- Track *every* idea you tried; otherwise multiple-testing makes you "mistake lumps of coal for gold."
- Hindsight bias: the past *looks* easier to trade than it was (20/20 hindsight, over-scrubbed data inflating performance, tools that didn't exist back then).

**The opportunity.** Exploitable patterns exist because participants differ in objectives, risk tolerance, info-processing ability, horizon, and resources. Markets keep evolving → opportunity persists indefinitely, **but** models built for vanished conditions decay inexorably. *An alpha researcher's job is never finished.*

---

## Ch. 3 — Cutting Losses (Igor Tulchinsky)

**The UnRule.** Infinitely many rules describe reality, but only one rule governs them all: **no rule ever works perfectly.** Grounded in Popper (1934): a universal truth can't be verified, only disproved by a single counterinstance. Every rule is flawed; every rule works *sometimes*. (Newton → Einstein as the canonical example.)

**Consequence for trading:**
- Represent trading rules as **alphas**. Managing millions of them surfaces regularities.
- The most universal way to handle the fact that all rules eventually break down is **knowing when to cut your losses**.
- Cutting losses originated in **trend following** (enter on new high, exit when accumulated profit breaches a limit). Modern version: apply trend-following logic to the **whole strategy's P&L**, not a single security.
- Plainly: **cutting losses = abandoning rules that no longer work.**

**Why people fail to cut losses:** ego/pride tied to "my rule," lack of alternative rules, and high cost of switching strategies. Cutting losses requires discipline and subjugating the ego.

**Combine many rules.** Don't believe exclusively in any one theory — believe them all a little, embrace none completely. The best indicator of whether a rule is good is *how well it's working right now*. Collect all ideas; let time + performance arbitrate. The more (imperfect) alphas you hold, the better you approximate reality — "one eye in the land of the blind."

Street-crossing metaphor (rules applied in tandem, overriding as conditions change):
1. Look left/right/left → safe to cross.
2. Hear a loud noise → turn toward it.
3. See a car coming → run!
A honk triggers Rule 2, which voids Rule 1's conclusion; then Rule 3 takes over. Implications:
- Come up with as many good rules as possible.
- No single rule can be relied on completely.
- Develop a strategy for using rules **simultaneously**.

**When is a strategy not working?** It performs outside expected returns, signaled by:
- A drawdown exceeding typical prior drawdowns.
- Sharpe ratio falling significantly.
- Rules seen in historical simulation no longer valid in live trading.

**The cut-loss procedure (do this BEFORE starting activity X):**
- Identify the **maximum acceptable loss `Y`** in advance.
- Track the **observed loss `Z`**.
- If `Z > Y` **and** exit cost is not too high → **cut the loss.**

**Summary checklist (per action):**
- What's the objective?
- What are the normal, expected difficulties?
- Plan in advance how to exit the strategy cheaply.
- Pursue multiple strategies simultaneously.
- Cut all strategies that fall outside expectations.

---

## Part I in one breath

An alpha is a small, testable idea about market behavior, expressed as code that turns data *changes* into positions. Alphas can exist because perfectly efficient markets are self-contradictory — someone must be paid to process information. But every signal is weak, estimated, and decaying: in-sample success means little, multiple testing manufactures false winners, and no rule lasts. The discipline that makes the whole thing work is **breadth + humility**: hold many imperfect alphas, never marry one, judge by current performance, and pre-commit to cutting losses when a strategy drifts outside expectations.
