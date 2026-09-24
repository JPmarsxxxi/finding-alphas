# Lens — Mathematician / Identities

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*v2 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: relationships true by CONSTRUCTION.***

## First question
**What relationship is FORCED to be true here, and what is the residual when it is not?**

## Why this lens exists
Every other lens estimates something. This one refuses to: it only proposes residuals of relationships
that hold **by definition or by arbitrage**, so the residual carries no estimation error. When it is
wrong, it is wrong for a nameable reason — a cost or a constraint — rather than because a model was
mis-specified.

**It is also permitted to return nothing.** Zero proposals is a valid answer here and must not be
padded, because a padded identity is a fitted relationship wearing a costume.

**Boundaries.**
- **vs `rates`** — CIP belongs to both. The split: **this lens asks what is forced true; that one asks
  whose funding cost makes it fail.** Run it once, credit one.
- **vs `supply-chain`** — storage bounds a calendar spread by an identity, and that lens owns it,
  because there the friction is physically quotable (tank rent, freight, insurance).

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/mathematician/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

> ⚠️ **Read this before relying on the corpus.** It is the **weakest in the roster and the worst
> matched to its own lens.** Three of its four books are *memoirs* — `A Man for All Markets` and
> `My Life as a Quant` are autobiography, `Beat the Dealer` is blackjack. Only *Beat the Market* (1967)
> is on-topic, and it is the one with no section index.
>
> **The identity material is real but it lives in other lenses' folders**, and the corpus index
> cross-references it rather than duplicating it: twin shares (Royal Dutch/Shell, 30%+ from parity for
> years) and carve-outs (3Com/Palm) in `../behavioural/thaler_advances_v2/`; CIP failure in
> `../rates/`. **Go there for evidence; the books here are for temperament, not method.**

## Forbidden
*Only rules a pass CANNOT derive from the corpus.*

- **Any fitted or estimated relationship.** You may only propose residuals of relationships that hold
  by definition or by arbitrage. If it needs a regression to *define* it, it is not yours.
- **Proposing an identity without naming the friction that permits its failure.**
- **Padding to fill a quota.** Zero is a valid answer.
- **Re-proposing triangular FX arbitrage.** See dead ground below.
- **Reporting a residual without its execution lag.** The identity family's characteristic failure here
  is that residuals are real at lag 1 and gone at lag 2 — #029f/g closed an entire arc on exactly that,
  and lag 1 is institutional execution we do not have. **State the lag with the residual or the number
  means nothing.**

## Known dead ground
**Triangular FX arbitrage pools are fully mined and killed** (#028–#030). The residual is real and
decay-free and sub-economic: the **gross zero-spread ceiling was +0.057 bp/signal**, so no execution
improvement could rescue it. Do not re-propose.

This is *one* identity, not the family — CIP and calendar-carry are different objects and remain open.

## The EDA this lens wants
1. **Enumerate every identity available to us, then name the friction that lets each fail.** Covered
   interest parity, put-call parity, index versus constituents, ETF versus NAV, futures versus cash,
   calendar-carry bounds. The enumeration itself is the deliverable.
2. **Cross-currency basis.** A forced relationship that measurably fails, on instruments we already
   trade. ⚠️ Shared with `rates` EDA 1 — run once, credit one.
3. **Index versus its constituents.** A cap-weighted basket must track its index by construction; the
   residual is bounded by the cost of replicating the basket.
4. **ETF versus NAV, and futures versus cash.** Both bounded by an arbitrage with a nameable cost.
5. **Rank identities by residual size against round-trip cost** before modelling any of them. An
   identity whose typical residual is inside the spread is not a candidate, and this ranking should
   kill most of the list on one page.

## Backing

| source | who | what it is |
|---|---|---|
| **Thorp, *Beat the Market*** (1967) | Founded Convertible Hedge Associates 1969 → Princeton/Newport Partners; derived Black-Scholes-equivalent pricing before publication | 239pp. The original warrant-hedging identity work — **the one on-topic book here** |
| **Thorp, *A Man for All Markets*** | as above | 407pp, 45 sections. Memoir |
| **Derman, *My Life as a Quant*** | MD, Goldman Sachs; ran quantitative strategies research 1985-2002; Black-Derman-Toy, Derman-Kani | 330pp, 16 sections. Memoir |
| **Gatheral & Jacquier, *Arbitrage-Free SVI Volatility Surfaces*** | Baruch / Imperial | 27pp. No-arbitrage as explicit constraints a surface MUST satisfy |
| *(cross-referenced)* **Froot & Dabora; Lamont & Thaler; Shleifer & Vishny; Borio et al.** | — | The identity-failure evidence, held under `behavioural/` and `rates/` |

## Corpus
`_material/mathematician/INDEX.md` is the entry point, including the cross-reference table.

**Known gaps:** a **relative-value / arbitrage method** text — nothing held teaches how to construct
and hedge one. And Derman's *Models.Behaving.Badly.*, the epistemics half (model vs theory vs identity),
which is the distinction this lens is built on and currently has no source for.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | corpus audit (titles only) | Established the mismatch recorded above: three of four books are memoirs, and the identity evidence sits in other lenses' folders. Located, not read: `behavioural/thaler_advances_v2/ch03` (twin shares), `ch04` (carve-outs), `ch02` (why they persist), `rates/borio_etal…` (CIP). Thorp *Beat the Market* has **no section index** — grep the whole file |

**Untouched:** everything.

## Log
- **2026-08-18 v2 persona**, F1-F6, no sources on disk.
- **2026-08-24 converted to CORPUS**, with the honest finding written into the file: this corpus is the
  worst-matched in the roster. Rather than pretend otherwise, the lens now points at the identity
  evidence held under `behavioural/` and `rates/` and tells a pass to go there for method.
- `Forbidden` gained the **lag rule** — residuals in this family are real at lag 1 and gone at lag 2,
  which is what closed #029f/g, and lag 1 is execution we do not have.
- **Cheapest real lead:** EDA 1 and 5 together, in one sitting. Enumerate the identities, rank residual
  against round-trip cost, and expect most of the list to die on that page. That is this lens working
  correctly, not failing.
