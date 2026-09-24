# Do alphas even fucking exist?

I want to start this thing with the strategy that broke me.

Call it #016. FX time-of-day seasonality, three pairs, short at 21:00, long at 23:00 London. Backtest net Sharpe 5.28. Plus 12.5% a year. Every one of five out-of-sample years positive. It held up on a currency I never fit it on, which is the test I trust most. The costs weren't guessed either; I pulled tick data off MT5 and measured the actual spread by hour, and the whole design dodges the overnight swap by construction. On paper this was the first thing I'd built in months that cleared a prop firm's bar organically, without leverage games.

I deployed it. It never worked. Not "underperformed" — the edge simply was not there. Gross negative, spread gate or no spread gate. I killed it on the 24th of July.

Then, three weeks later, doing a routine review, I found it had still been trading. I'd made the kill decision and never unregistered the scheduled task. Two books ran for another twenty days on a strategy I had already declared dead, and the reason I noticed is that I sat down to reconcile the fills against the broker's own deal history instead of my own log. Which is when I found the second thing: FTMO bills a commission on FX. 25 cents a deal, 50 cents a leg round trip. In basis points of the size I was trading, that's 2.00 bp a night across three legs, against an expected edge of 1.24 bp. The book was negative before it opened. No script I had ever written contained a commission term. I grepped. Zero hits.

So the honest sequence is: the backtest was partly an artifact, the live test refuted it, I killed it, the kill didn't take, and the whole thing had been arithmetically doomed by a cost class I didn't know existed.

That's when the question in the title stopped being rhetorical.

## The body count

The log is at 41 numbered ideas. Cross-sectional reversal, crypto skew, index overnight drift, GEX regimes, multi-asset momentum, COT positioning, month-end rebalancing flow, statistical arbitrage on daily and then intraday FX, customer-supplier links, FX carry, pre-FOMC drift, EIA inventories. Two books are alive today and one of them has produced literally zero information in nine sessions, because the model it's supposed to be testing has never once declined to trade.

Everything else is killed or parked.

For a while I thought the problem was me. Bad ideas, artisanal and few. So I went to the literature and worked published anomalies instead. Those died faster. Three in a row failed at the decay check, meaning the effect is there in the paper's sample window and gone afterwards. Obvious in hindsight. If I can read it, it's crowded.

Then I thought the problem was that I was too harsh on costs. So I measured everything: swap per side per instrument, spread by hour of day off real ticks, the commission I'd missed. That made it worse. It turns out I hadn't been harsh enough.

Then I thought the problem was the machine.

## The part where you go slightly insane

This is the phase I actually want to write about, because nobody warns you.

When your backtester kills everything you feed it, there are exactly two explanations, and from the inside they feel identical. Either markets are efficient enough that your ideas genuinely have no edge, or your engine has a bug that eats edges. Every result you produce is consistent with both. You start reading your own cost model at 1am wondering whether you've spent months building a machine that can only say no.

I broke it two ways.

First, a synthetic test. I generated data with an edge deliberately rigged into it, ran it through the same pipeline, and got Sharpe 9.2. Then I ran pure noise through the same pipeline and got flat. So the engine can see an edge when one is there, and doesn't invent one when it isn't.

Second, I took one of my dead ideas to WorldQuant's platform and ran it on somebody else's simulator, with their data and their cost assumptions. Gross Sharpe 1.78, which looks great until you notice it fails their own fitness gate, and the reason it fails is turnover. Their metric discounts Sharpe by how much you trade. That is, in different notation, the exact thing my engine had been telling me for months.

The engine was fine. Which is the worse answer, because it means the verdicts were real.

## The finding that reframed everything

Months later I ran something dumb and simple: point the same forecaster at different moments of the return distribution and compare out-of-sample R².

Direction, out-of-sample R², by asset class. FX hourly: −0.052. US equities daily: −0.050. World indices: −0.049. Mid-cap US: −0.052. FX five-minute: −0.051. That's 445 series across four asset classes and four frequencies, and every cell sits within 0.003 of every other cell. Negative R² means the forecast is worse than just using the average.

Size of the move, same forecaster, same data: +0.108 on US equities, +0.155 on world indices, +0.141 on FX five-minute.

I sat with that table for a long time. Direction isn't hard. Direction is flat everywhere I can measure, to three decimal places, in every market I have access to. And then the part that actually hurt: I went back through the log and checked the shape of each dead idea. Every single one was a conditional mean test. I had spent a year and change mining the one moment of the distribution that carries no information anywhere, and the cause of death looked different every time (decay, spread, swap, beta, sample size) but the thing underneath was always the same.

## So: do they exist?

Yes. That's the annoying answer.

I have a residual FX signal with an information coefficient of 0.0205 measured on 2.16 million observations. Roughly thirty standard errors from zero. It is not a fluke, not a bug, not a microstructure artifact; I called it fake at first and I was wrong. It is also worth approximately nothing, because it decays 75% in one bar and the spread eats what's left.

I have an equity linkage effect, real reversal, Sharpe 1.40, that only exists on a venue I can't trade from where I sit.

I have an overnight trade around FOMC that is real, doesn't decay, and clears its measured cost by 7.5x. It makes 0.96% a year, because it fires eight times.

And I have the one that taught me the most: a strategy that passed every kill test I own, then lost by a factor of three to the stupidest possible control, which was doing the trade every single night instead of only on the special one. The edge was real. The form was wrong.

That's the shape of it. Alphas exist roughly the way gold in seawater exists. The concentration is real, it's measurable, it's reliably non-zero, and it costs more to get out than it's worth. Nobody is lying to you when they say the anomaly is there. The anomaly is there. The question was never whether the signal is real. The question is whether it survives the toll, at your size, on your venue, in a form you can actually hold.

I don't think most people fail because they can't find signal. I think they find signal, confirm it's real, and never do the second calculation.

## What I'd tell myself fourteen months ago

Price the trade before you build it. If the edge per trade isn't five to ten times the round-trip cost, you don't have a research project, you have an expensive way to find out.

Measure instead of reasoning. In one session I had three separate confident mechanical arguments contradicted by data within an hour of testing them. Thin order books should mean bigger moves; they meant smaller ones, by a factor of three. Rebalancing a diversified book should have earned +386 bp a year by the standard formula; it lost 1,178.

Run the boring control. Always test "do this every period" against "do this on the special period." Selectivity has to earn its keep and usually doesn't.

And a kill isn't done until the scheduled task is gone.

The log is at #041. I'm still going, not because I'm especially optimistic, but because at this point what I want is to know.
