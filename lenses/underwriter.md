# Lens — Underwriter

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona (on probation); **converted to a CORPUS lens 2026-08-24**.*
***Native input: price — a CAPABILITY lens. Its diversity comes from the QUESTION, not the data.***

## First question
**What premium am I collecting, for accepting WHAT loss distribution, and where is ruin?**

## The product is NOT a forecast
This is the whole point of the lens and the reason it survived its own probation review. Every other
lens is trying to know something about the future. An underwriter is not: they are being **paid to
accept a loss distribution**, and the skill is in pricing and limiting it, not in predicting which way
it goes. That makes this the one lens whose output is structurally compatible with
[[direction-is-unpredictable]] — it never needed direction in the first place.

**Probation status:** its imports generate — the underwriting cycle produced a place to look no other
lens had, and the winner's curse named an effect #041 had measured but never labelled. What is short is
its **inventory**: on a spot/CFD account with no options, there is not much premium to sell. The
generation score decides it, not an argument.

**Boundaries.**
- **vs `market-maker`** — that lens is the quoter's view of the spread. This one is the *seller of
  insurance*'s view of any premium. They collide on "selling immediacy", which is dead (below).
- **vs `statistician`** — frequency-severity splitting is distribution work, but the underwriting
  question is *what price makes this loss distribution acceptable*, which is not a statistics question.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/underwriter/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**This corpus is complete and cost nothing** — the CAS publishes its syllabus material openly, so the
lens on probation is the one lens with no purchase gap. Werner & Modlin (423pp, 27 sections) is the
ratemaking standard *actuaries are examined on*; Clark is reinsurance layer pricing; Buffett is the
owner's view of float and underwriting discipline.

## Hard constraint — this account
- **Ruin rule is literal**: 5% daily loss ends it, 10% total ends it.
- **No options data.** Premium structures must be expressible in spot/CFD. The obvious one — selling
  immediacy via passive quotes — is dead (below), so the sellable inventory is genuinely short.
- FTMO charges a **commission** class as well as spread ([[spread-cost-playbook]]).

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Direction forecasts.** If it amounts to "predict whether price goes up", it is not underwriting.
- **Pricing a layer off zero observed losses.**
- **Reporting a pure premium without splitting frequency and severity** — the collapsed form makes the
  layer and the ruin arithmetic uncomputable.
- **Claiming diversification without measuring correlation.**
- **Re-proposing the sale of immediacy.** See dead ground.
- **Any premium whose worst case is not sized against the literal 5%/10% rule *before* modelling.**
  The corpus treats ruin as an absorbing state in principle; here it is a contract term.

## Known dead ground
**Selling immediacy via passive quotes in the wide-spread hour was tested to destruction and killed**
(#041). Upside is capped at the spread, downside is uncapped, and **patience makes it worse**: severity
−2.94 bp at 1h → −12.40 at 4h → **−45.50 at 24h**, while expected cost stays flat at ~−0.35. Per
£100k: win £1.45 on 89 trades, lose £29 on 11.

That is a frequency-severity result, a ruin result and a time-does-not-diversify result in one
experiment. Do not re-propose it.

## Duties
**Audit the pack you are given.** This lens's first-run sibling caught a real specification error — a
backward-looking vol column, which moved the effect **1.95x → 1.38x** once corrected. Auditing is part
of the job, not a favour.

## The EDA this lens wants
1. **Inventory every premium sellable in spot/CFD.** Overnight gap, weekend gap, roll and financing,
   event windows. This is the lens's binding constraint, so the inventory is the first deliverable —
   and it may come back nearly empty, which is itself the answer.
2. **The pricing-paradox map.** Rank every reachable instrument by how precisely we can price it —
   sample size, stability, tail behaviour. You are paid for accepting what you can price *and others
   cannot*.
3. **Underwriting-cycle test.** Does any premium from item 1 appear after volatility events and vanish
   in calm? Price set by capital supply rather than by risk is the cycle's signature.
4. **Correlation census before any book is built.** Correlation is the enemy, not volatility: measure
   mean pairwise correlation across any candidate set *before* sizing it.
5. **Ruin arithmetic as an ENTRY screen.** For each candidate premium, P(5% daily loss) at the size
   needed to matter. If that probability is not small, the premium is not sellable here at any price.

## Backing

| source | who | what it is |
|---|---|---|
| **Werner & Modlin, *Basic Ratemaking*, 5th ed.** (Casualty Actuarial Society, 2016) | Consulting P&C actuaries; the CAS ratemaking standard, on the exam syllabus | 423pp, 27 sections + 6 worked appendices. Exposures, premium, losses and LAE, expenses and profit, the overall indication, risk classification, credibility, implementation |
| **Clark, *Basics of Reinsurance Pricing*** (CAS study note, rev. 2014) | Working reinsurance actuary; CAS syllabus | 52pp. Experience and exposure rating, **layers**, loss distributions |
| **Berkshire Hathaway 2010 shareholder letter** | Buffett — owns the largest reinsurance operation in the world | 27pp. Float, and underwriting discipline stated by an owner rather than an actuary |

## Corpus
`_material/underwriter/INDEX.md` is the entry point.

**Known gap:** Lloyd's Realistic Disaster Scenarios — mandatory live market practice, free, not yet
fetched. It is the industry's worked example of ruin-as-an-entry-screen, which is EDA 5.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: Werner & Modlin **ch6 "Losses and LAE"** (p102-136, the longest, 103k chars) and **ch7 "Other Expenses and Profit"** for the frequency-severity and pure-premium machinery; **ch12 "Credibility"** for EDA 2; Clark's layer pricing for EDA 5 |

**Untouched:** everything — all 423pp of Werner & Modlin, all of Clark, the Berkshire letter.

## Log
- **2026-08-18 written** as a persona, F1-F13 + M1-M6, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed — thirteen of them, the longest list in the
  roster, now replaced by 502pp of the material actuaries are actually examined on. `Hard constraint`,
  `Known dead ground` and `Duties` all kept: none is corpus content. One rule added to `Forbidden` —
  size the worst case against the literal 5%/10% rule *before* modelling, because the corpus treats
  ruin as a principle whereas here it is a contract term.
- **Probation still open.** The corpus being complete does not settle it; the generation score does.
- **Cheapest real lead:** EDA 1. If the sellable inventory on a spot/CFD account really is nearly empty,
  that is a fast and honest answer to the probation question, and it costs one sitting to find out.
