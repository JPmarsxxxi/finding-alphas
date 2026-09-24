# Lens — Poker / Game Selection

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Reinstated 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: who else is playing.***

## First question
**Which game here is soft — and what specific, repeatable mistake is someone else making?**

## Why it is a generator, not a critic
It was removed once for being written as a critic ("is your edge big enough?" — the gauntlet answers
that better and cheaper) and **reinstated the same day**, because its real first question is a place to
look, not a judgement: **where are the bad players?** Nothing else in the roster asks it.

Lesson recorded at the time and worth keeping: *a lens can be miscast rather than wrong — check the
framing before removing the discipline.*

**Its standing result is the largest single effect in the log.** #041 measured instrument choice as
worth **8.6x to 29.6x** — bigger than most signals ever found here. The capture fraction a signal must
deliver to clear 5x: **EURUSD 14%, USDJPY 18%, GBPUSD 34%, USDCHF 48%, USDCAD 58%, AUDUSD 68%,
NZDUSD 77%.** Five of seven pairs are not worth playing whatever the signal.

**Boundaries.**
- **vs `behavioural`** — that lens asks *what the mechanism of the mistake is and when it fires*. This
  one asks *which table is soft and where do I sit*. Same subject, different question, different data.
  If a pass here starts explaining the psychology of the mistake, hand it over.
- **vs `market-maker`** — who *makes* the price is theirs; who is *bad at* the game is this lens's.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/poker/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

> ⚠️ **One-book corpus, and it is the roster's thinnest.** Chen & Ankenman (367pp, 30 sections) is
> genuinely on-topic and genuinely authoritative — Bill Chen runs Statistical Arbitrage at Susquehanna
> and has two WSOP bracelets, which is the academic × institutional cross in one person. But there is
> no second source, and the lens's other listed backing was *"Susquehanna's game-theory training"*,
> which is a practice rather than a document and has been removed. **A pass should say when it is
> reasoning past the one book it has.**

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Assuming a mistake rather than measuring one.** Inherited from [[economist]] and it still binds —
  #041's 17:00 result failed exactly here: nobody was making a mistake, **they were absent**.
- **Proposing an instrument without saying why it is the softest available.** "It was the first one
  with data" is not table selection.
- **Reading a short run as evidence about the edge**, in either direction.
- **Proposing a table without its SEAT.** Instrument and hour are one choice, not two: the same pair
  swings **8x–36x** in what it demands depending on when you sit. A proposal that names EURUSD without
  naming the hour has not done table selection.
- **Proposing any of the five pairs the capture-fraction gate already excludes** without saying why
  this signal is the exception. GBPUSD needs 34%, USDCHF 48%, USDCAD 58%, AUDUSD 68%, NZDUSD 77%.

## The EDA this lens wants
1. **Scout the tables — this lens's core job.** Rank every reachable instrument by softness: retail
   share, order-size distribution, time-of-day composition, anything that separates who is playing.
2. **Cheapest seat wins.** Cross the softness ranking against round-trip cost. A soft table with a big
   rake is unbeatable at any skill level, and that is a fact about the venue, not the signal.
3. **Map repeatable behavioural mistakes.** Round-number clustering, breakout chasing, session-open
   behaviour. ⚠️ #043 already killed the round-number version: clustering measured **1.009% against a
   1.000% null**, spread 0.169 vs 0.170 bp, forward move 1.02x. Start from that.
4. **Price the seat.** Quantify what acting later is worth: the gap between idealised and realistic
   execution. #029f/g measured this as the whole verdict — lag1 marginally positive, lag2 negative.
5. **Where is the game getting softer?** New instruments, new retail venues, newly listed markets —
   softness is a moving target and the roster has never looked for where it is moving *to*.

## Backing

| source | who | what it is |
|---|---|---|
| **Chen & Ankenman, *The Mathematics of Poker*** | **Bill Chen — head of Statistical Arbitrage, Susquehanna**; PhD maths, Berkeley; two WSOP bracelets (2006). Ankenman also at Susquehanna, also a bracelet winner | 367pp, 30 sections. Game selection, bet sizing, variance and bankroll, and reading results from short runs |
| *(adjacent, held elsewhere)* **Thorp, *Beat the Dealer*** | — | Blackjack rather than markets, filed under `mathematician/`, but the edge-and-bet-sizing reasoning is the same object |

## Corpus
`_material/poker/INDEX.md` is the entry point.

**Known gaps:** a **second text**. Also *The Mathematics of Poker* has **no embedded bookmarks** — its
30 sections were detected from its printed contents, so verify a section boundary before quoting
across one.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | `chen_ankenman_mathematics_of_poker/INDEX.md` (titles only) | Located, not read. The sections this lens needs first are the **bankroll and variance** material for EDA 4 and the **game-selection** material for EDA 1 — note the book's own framing is that game selection dominates play quality, which is the claim #041 independently measured at 8.6x–29.6x |

**Untouched:** everything.

## Log
- **2026-08-18 reinstated** as a persona, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. The non-document "source" (Susquehanna's
  training) removed from the backing table — a practice is not a corpus. `Forbidden` gained one rule:
  do not re-propose the five pairs the capture-fraction gate already excludes without saying why this
  signal is the exception.
- **EDA 3 now carries its own partial kill** — #043 measured round-number clustering at 1.009% against
  a 1.000% null, so that particular mistake is not there.
- **Cheapest real lead:** EDA 5. Softness is a moving target, the roster has only ever measured it on
  instruments it already trades, and the standing constraint says the lens may point at any market —
  including ones we have never held.
