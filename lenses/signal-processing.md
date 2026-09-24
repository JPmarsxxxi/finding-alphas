# Lens — Signal-Processing Engineer

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: price — a CAPABILITY lens, not a diversity one. Ranked last in the roster on purpose.***

## First question
**What is the noise floor here, and is there anything above it?**

## Honest position in the roster
Its input is price, like six of the other lenses, so it cannot deliver the structural diversity the
non-price lenses do. Several of its questions are the same object another lens already owns, reached
through different machinery — cross-reference and **credit once, not twice**. **Its value is that it
asks price questions with better instruments**, not that it asks new ones.

A sourcing caveat that applies to nothing else in the roster: **the practitioners who made the money
here published nothing about it.** Renaissance is closed by design. What is documented is the
*technique* and the *biography* — Jelinek instigated HMMs at IBM's Speech Recognition Group and
co-authored the 1983 maximum-likelihood speech paper with **Robert Mercer**; **Peter Brown** and Mercer
published HMM parameter estimation in 1988; both then went to Renaissance, which hired physicists,
astronomers, code breakers and speech-recognition researchers and **no finance people**. The chain is
real and verifiable. **The trading application is inference, and must be labelled as such in any
proposal this lens makes.**

**Boundaries.**
- **vs `physicist`** — that lens owns the **shape** of what is there: exponent, relaxation, scale. This
  one owns whether there is anything above the floor at all, and how to detect it.
- **vs `statistician`** — that lens owns multiplicity and whether an estimate is honest given how many
  things were tried. This one owns the detection problem itself.
- **vs `machine_learning`** — that lens owns whether complexity pays. A matched filter is not a model
  in that sense; it is an instrument.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/signal_processing/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

> ⚠️ **This lens has NO BOOK.** Both intended texts — Jelinek's *Statistical Methods for Speech
> Recognition* and Kay's *Fundamentals of Statistical Signal Processing* — are commercial and were not
> obtained. What is held is the **primary-paper backbone**, and it is uneven:
>
> | question | covered by | status |
> |---|---|---|
> | noise floor, sampling, aliasing | Shannon 1948 | held |
> | hidden state behind an observable | Rabiner 1989 (OCR'd) | held |
> | running state estimate with uncertainty | Welch & Bishop; SIGGRAPH course | held |
> | **detection vs estimation as different problems** | Kay | **MISSING** |
> | **the matched filter** | Kay | **MISSING** |
>
> **Two of this lens's five core questions have no source.** Kay is the single most valuable purchase
> in the roster's buy list for that reason. Say so if a pass leans on either.

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Claiming a signal without a measured noise floor.**
- **Using data after `t` in anything that must run live** — smoothing presented as filtering.
- **Reporting a periodicity without checking the sampling rate against it.**
- **Presenting a technique as Renaissance's method.** The biographical chain is real; the trading
  application is inference. Label it.
- **Proposing a detector without stating its lag.** A filter that needs `k` bars to declare a state has
  a `k`-bar delay, and #044 measured what that costs: with a 30-minute backward trigger, **+52.94 bp
  (t 33.0) of the move happens BEFORE the trigger fires** and only +1.15 bp (t 0.7) remains. *Any
  detector built on accumulated evidence fires after the move it detects.* That is this lens's
  characteristic failure and it must be priced up front.

## The EDA this lens wants
1. **Sweep for repeating structure.** Across every instrument reachable, compute the autocorrelation of
   returns, |returns| and signed flow, and check any periodicity against the sampling rate.
2. **Rank instruments by DETECTION HEADROOM, not by result.** For each instrument estimate the noise
   floor and ask how large a signal would have to be to clear it. This is the lens's most distinctive
   output — a ranking of where detection is even *possible* before anyone looks for a signal.
3. **Build a response-template library from endogenous shocks.** Take the largest |moves| in each
   instrument and average the surrounding path to get an empirical impulse response. A template is what
   a matched filter needs, and none exists.
4. **Cross-instrument lead-lag detection.** Cross-correlate at sub-daily lags across every pair we can
   hold. ⚠️ Shared object with `physicist` EDA 3 — run once, credit one.
5. **Hidden-state sweep.** Fit a small HMM to each instrument's return and volatility series and ask
   whether the inferred states are stable, interpretable and *usable at the time they are inferred*
   rather than in hindsight.

## Backing

| source | who | what it is |
|---|---|---|
| **Shannon (1948), *A Mathematical Theory of Communication*** | Bell Labs | 55pp. The information-theoretic floor, sampling, channel capacity |
| **Rabiner (1989), *A Tutorial on Hidden Markov Models*** (Proc. IEEE) | Bell Labs; the canonical HMM reference | 30pp. ⚠️ **OCR'd from a scan** — two-column interleaving, so grep-friendly, not quote-friendly |
| **Welch & Bishop, *An Introduction to the Kalman Filter*** (UNC TR 95-041) | UNC Chapel Hill | 16pp, plus the 80pp SIGGRAPH course version with the extended filter and worked numbers |

## Corpus
`_material/signal_processing/INDEX.md` is the entry point.

**Known gaps:** Kay (detection/estimation, the matched filter) and Jelinek. See the warning above —
these are not decorative gaps; they are two of the lens's five questions.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | corpus audit | Established the coverage table above: three of five core questions have a source, two do not. Rabiner's PDF was a pure scan (29 chars of text layer) and was OCR'd with Tesseract at 200dpi → 147k chars |

**Untouched:** everything.

## Log
- **2026-08-18 written** as a persona, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. `Honest position` kept in full — it is the
  most useful paragraph in the file and none of it is corpus content. Two rules added to `Forbidden`:
  label the Renaissance inference as inference, and **state a detector's lag**, with #044's measurement
  as the worked case (+52.94 bp before the trigger, +1.15 bp after).
- **The conversion produced a purchase recommendation:** Kay is the roster's highest-value buy, because
  it is the only gap that leaves core questions of a lens completely unsourced.
- **Cheapest real lead:** EDA 2. A detection-headroom ranking needs only price data we already hold,
  produces a *shortlist* rather than a diagnostic, and no other lens produces it.
