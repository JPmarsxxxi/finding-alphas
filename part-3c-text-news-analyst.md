# Part III-C — Text: News, Social Media & Analyst Reports (Ch. 22, 24)

*Unstructured/text data → signals via NLP. High volume, weak per-item accuracy, but uncorrelated with price-volume alphas.*

---

## Ch. 22 — News & Social Media

Raw news isn't machine-readable → use NLP/ML (naive Bayes, SVM, word2vec, deep learning) to score it. Algorithm advantage = speed + coverage; disadvantage = weaker accuracy than a human. Big news → instant move, often with overshoot + reversal.

**The dimensions that turn news into a signal:**
- **Sentiment** — polarity, normalized to a cross-sectionally comparable score (e.g. 0–100; >50 good, ~50 neutral, <30 bad).
- **Novelty** — brand-new vs follow-up. Less novel → less impact (already priced). `novelty ∝ 1 / time-between-events`.
- **Relevance** — how focused the news is on a specific stock (company-specific earnings = high; supply-chain/industry news = lower, spread across names). Maps sentiment → individual stocks.
- **Category** — earnings / legal / M&A etc. Different categories have different response times; markets favor different "flavors" at different times (category-rotation); some are sector-specific.
- **Expected vs unexpected** — *surprise drives price, not polarity.* "+150% earnings" is bad news if consensus was +200%. Combine news with consensus/calendar.
- **Headlines vs full text** — headlines are clean & high-info; in full text, first & last sentences/paragraphs carry most info.
- **No news is good news** — news = uncertainty (higher vol/volume, analyst revisions); funds reduce news-heavy names → lower returns.
- **News momentum** — if not fully priced, price drifts. Stronger for **small caps & unexpected news**; for large caps & expected news, expect **reversal after overshoot**.

**Worked alpha sketches (from the chapter):**
```
Simple:    if sentiment > 70 → long;  if sentiment < 30 → short;  neutralize vs no-news peers in industry
+Novelty:  weight the above by novelty score (0–1)
+Relevance:weight by relevance (0–1); ignore news hitting too many stocks (ns large)
+Category: category_score = avg relative stock return after that category's news over past 2yr
No-news:   when abnormal news VOLUME for a company → short it
NewsMom:   for 3 days after release, hold same direction as the 2-day pre-release return;
           then reverse for the next 5 days to capture the reversal
```

**Social media** = news but higher volume, more noise, casual formatting, lots of derivative/fake signals. Twitter is most-used (maps to @ticker / CEOs). The 2013 fake-AP-tweet flash crash ($136B in 2 min) shows the stakes. Example: short companies with rising tweet/retweet frequency (tweets skew negative).

---

## Ch. 24 — Analyst Reports (Institutional Research)

Sell-side reports contain: company/industry description, financial estimates, **price target**, **buy/hold/sell rec**, and a thesis. Accessible free via Yahoo/Google Finance, Seeking Alpha, Motley Fool, company IR.

**Seven worked alphas (each formula straight from the chapter footnotes):**
```
1. Recommendations:  Alpha = avg buy recommendation − avg sell recommendation
2. Price target:     Alpha = analyst price target − stock price
3. Earnings est.:    Alpha = change in analyst earnings estimate for next fiscal period
4. Earnings surprise:Alpha = actual earnings reported − analyst earnings estimate
5. Buybacks:         Alpha = if board executes share buyback → long; else short
6. Earnings-call:    Alpha = avg positive sentiment − avg negative sentiment (call text)
7. Coverage drop:    Alpha = short-term analyst coverage / long-term analyst coverage
```
(all run on Russell 3000 in the book.)

**The deeper lesson — generalize the analyst's *reasoning*, not the call:** "she likes AAPL because the CEO is buying stock" → test "does insider buying predict returns *across all stocks*?" Analyst Q&A on earnings calls also flags which accounting items actually matter.

**Watch-outs (biases baked into analyst data):**
- **Positive bias** — far more buys than sells (banking-relationship conflict) → distribution is skewed.
- **Herding** — analysts cluster near consensus (career risk); the *deviators* (confident/reputable) are the interesting signal.
- **Coverage drop** — analysts drop coverage rather than issue a sell (esp. large caps) → a coverage drop is a **red flag** (basis for alpha #7).

**Checklist:** score sentiment/novelty/relevance/category; weight by surprise-vs-consensus; for analyst data exploit recs/targets/estimates/surprise/coverage but correct for positive bias & herding; always ask "does this analyst's *logic* generalize to other names?"
