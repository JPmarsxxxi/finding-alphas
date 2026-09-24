# Lens — Historian

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24** — the last of the thirteen.*
***Native input: rule-books, venue changes, sample inhomogeneity.***

## First question
**What was structurally DIFFERENT about the period in which this held, and is that structure still here?**

## Allergy
Treating a long sample as one homogeneous population. Averaging across a structural break.

## Why this lens exists
Every other lens produces a number. This one asks **over what population**, and the log says that
question has teeth: A02 looked alive at 2.86x on the cheapest names and died on the era split —
pre-2000 **5.46x** / 2000-09 **0.13x** / 2010-14 **7.44x** / 2015-19 **0.02x** / 2020-24 **4.14x**.
That is **alternating, not decaying**, which is the #039 C4 noise signature and the single most useful
diagnostic shape in the log.

**This lens now owns the decay-first gate** written into Part 0 Step 1b on 2026-08-22. Monotone decay
means arbitraged away; strongest-recent or flat means it survives; **alternating means noise**. That
gate is why every source is now allowed at Step 1 — crowding is measured rather than assumed — and it
is this lens's instrument.

**Boundaries.**
- **vs `statistician`** — that lens owns multiplicity and the trial count. This one owns
  **inhomogeneity**: whether the sample was ever one population.
- **vs `economist`** — a rule that creates a forced participant belongs to that lens once it exists.
  This one owns the *change* itself: what was different before, and when it flipped.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/historian/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

> ⚠️ **Two corpus defects, both material to how you read it.**
>
> **Harris, *Trading and Exchanges*, is an EXCERPT** — 113pp of a ~640pp book. It is the lens's
> reference for venue structure and rule change, and most of it is missing. Say so if a pass leans on it.
>
> **Marks was repaired, not clean.** The supplied file had **zero word spaces**; it was re-rendered
> through LibreOffice to recover them (0% → 15.8%). Measured residual damage: **0.11% of tokens run
> together** (`StudyCycles`, `calledThe`), 0.44% suspiciously long, and a few short spans dropped
> outright. Good to grep and read; **check the PDF page before quoting a phrase.**

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Treating any pooled statistic as applying uniformly across its date range without checking.**
- **Conditioning on a regime LABEL rather than on observables available at the time.** A label is
  hindsight; the live version only has the state variable.
- **Reporting an effect without stating the era in which it holds.**
- **Reading an alternating era profile as a regime effect.** It is the noise signature — A02 above, and
  #039 C4. This is the mistake this lens exists to catch and it is the easiest one to make, because an
  alternating profile always has a plausible regime story available.
- **Ignoring the instrument's own history.** Measured 2026-08-15: `^FTSE`/`^GSPC`/`^AXJO`/`^IBEX`
  publish a **stale open** on 68/54/36/15% of days, which silently voids any gap test; and Stooq died
  to a JS proof-of-work the same month. The data source has an era too.

## The EDA this lens wants
1. **What is changing RIGHT NOW?** Enumerate structural changes in force or arriving — settlement
   cycle, venue rules, listing changes, index methodology. A change that has not finished propagating
   is the one place this lens can be early rather than retrospective.
2. **Find the youngest liquid markets available to us.** Short history means short crowding history.
   Rank reachable instruments by age and check whether the young ones behave differently.
3. **Regime-conditional predictability sweep.** Build a credit/liquidity state variable from
   observables and re-run any banked effect conditional on it — never on a label.
4. **Where did a rule create a forced participant that did not exist before?** Rule changes manufacture
   obligation. ⚠️ Hand the resulting obligation to [[economist]]; this lens owns the dating of it.
5. **Age-of-effect discipline.** For any candidate this lens is handed, date the start of its regime
   and check the effect within it. This is the decay-first gate applied as a service to other lenses.

## Backing

| source | who | what it is |
|---|---|---|
| **Marks, *Mastering the Market Cycle*** (2018) | Citicorp senior PM (convertibles, high yield); led distressed, high-yield and convertibles at TCW 1985-95; **co-founded Oaktree 1995** | 245pp, **18 chapters**. The economic cycle, the pendulum of investor psychology, attitudes to risk, the credit cycle, distressed debt, real estate, and **cycle positioning** — where you are as an actionable state, without forecasting |
| **Harris, *Trading and Exchanges*** — **EXCERPT** | **Chief Economist of the SEC 2002-04**, directing the Office of Economic Analysis; contributed to the specification of Reg NMS | 113pp of ~640pp. Market microstructure for practitioners: venue rules, order types, who trades and why |

## Corpus
`_material/historian/INDEX.md` is the entry point.

**Known gaps:** the **full Harris** — the single most useful purchase for this lens, and it doubles as
reference for `market-maker`. And the **Oaktree memos** — decades of them, free at oaktreecapital.com,
never fetched because they are a scrape rather than a file. Marks's book is the distilled version; the
memos are the contemporaneous record, which for a lens about *what people believed at the time* is the
more valuable object.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: Marks **ch IX "The Credit Cycle"** (p107-124) and **ch VIII "The Cycle in Attitudes Toward Risk"** (p81-106, the longest) for EDA 3's state variable; **ch XIV "Cycle Positioning"** (p184-196) for EDA 5. Harris excerpt has 280 bookmarks over 113 pages — the contents survived, most of the body did not |

**Untouched:** everything.

## Log
- **2026-08-18 v2 persona**, F1-F6, no sources on disk.
- **2026-08-24 converted to CORPUS — last of the thirteen.** Fundamentals removed; `Allergy` kept as
  the one line that is the lens. Two rules added: **an alternating era profile is noise, not a regime**
  (A02 and #039 C4), and **the data source has an era too** (the stale-open measurement, Stooq's death).
- **This lens acquired ownership of the decay-first gate** when it was written into Part 0 Step 1b on
  2026-08-22 — EDA 5 is now a service the lens performs for the rest of the roster.
- **Cheapest real lead:** EDA 1. Structural change in flight is the only way this lens is early rather
  than retrospective, and it needs rule-books rather than data.
