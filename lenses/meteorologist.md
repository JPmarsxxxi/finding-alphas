# Lens — Meteorologist / Forecast Verification

*One of the lenses in [[lenses]]. Read this, work the corpus it points at, exhaust it, then move on.*
*Written 2026-08-18 as a persona; **converted to a CORPUS lens 2026-08-24**.*
***Native input: physical forecasts** — the only lens whose driver is measured before the market sees it.*

## First question
**What is actually forecastable here, how far out, and how do I know my probabilities are honest?**

## Why this lens exists
Meteorology is the one field that has spent fifty years being **publicly, quantitatively wrong** and
built the machinery to measure exactly how wrong. It is the only discipline in the roster whose
professional output is a *calibrated probability* that gets scored every single day, on a fixed
protocol, including the forecasts it would rather forget.

That machinery is worth more to this programme than any weather trade. **Two of the log's most
expensive failures were verification failures, not idea failures:** #016 passed every backtest and
died live, and #041 graded a generator on a deployment bar. This lens owns the question *how would I
know*.

**Boundaries.**
- **vs `statistician`** — that lens owns multiplicity and the trial count: *how many things have I
  looked at*. This one owns **calibration and skill against a reference**: *when I said 70%, did it
  happen 70% of the time, and did I beat persistence*. Different questions, both about honesty.
- **vs `supply-chain`** — weather drives gas, power and ags, which are physical-flow instruments. The
  split: that lens asks where the stuff is, this one asks what is knowable about it in advance.

---

# HOW TO WORK THIS LENS

**There are no pre-written fundamentals here, deliberately.** Derive at pass time.

1. **Start at `_material/meteorologist/INDEX.md`** for structure.
2. **Grep the `.txt` twins for content.**
3. **Cite what you derive** — file and section, every claim.
4. **Log what you grepped** in the grep log below.

**Note the shape of this corpus:** Kalnay (369pp, 44 sections) and Palmer (367pp, 31 sections) are the
*forecasting* half. The **scoring** half is a backbone, not a book — Jolliffe & Stephenson was not
obtained, and the WWRP/WGNE verification reference stands in its place. That reference is a captured
web document, so it is one flat `.txt`: grep it, do not expect chapters.

## Forbidden
*Only rules a pass CANNOT derive from the corpus. Every rule below is one the corpus would happily
teach — they are kept anyway, because they are the reason this lens is in the roster at all, and
because the log shows we break them.*

- **Forecasting past a stated, measured skill horizon.**
- **Reporting skill without a reference forecast** — persistence AND climatology. Not against zero.
- **Reporting profit without calibration.** They are different questions and the log conflates them:
  #016 had profit in backtest and no honest probability behind it.
- **A single deterministic forecast.** Ensemble or nothing.
- **Applying this lens's machinery only to weather.** Its instruments — reliability diagrams,
  reference-relative skill, ensemble spread — are the right tools for grading **any** signal in this
  programme, and are currently used on none of them. That is a bigger opportunity than any gas trade.

## The EDA this lens wants
1. **Which tradable instruments have a physically forecastable driver?** Natural gas, power,
   agricultural. Map driver → instrument → whether we can trade it at all, before anything else.
2. **Measure a skill horizon, then trade only inside it.** For any driver-to-price relationship, find
   the horizon at which skill against persistence goes to zero, and treat it as a hard boundary.
3. **Ensemble spread as a tradability gate.** Perturb inputs, measure dispersion, act only in
   tight-spread states. The spread is the tradability signal, not the mean.
4. **Calibration, not profit.** Build a reliability diagram for any probabilistic signal: when it says
   70%, does it happen 70% of the time? **Run this on a banked signal first** — #044 passed a
   pre-registered sealed test and has never been checked for calibration.
5. **Reference forecasts as the bar.** Score every candidate against persistence AND climatology
   rather than against zero. This is a one-line change to how the log reports results and it has never
   been done.

## Backing

| source | who | what it is |
|---|---|---|
| **Kalnay, *Atmospheric Modeling, Data Assimilation and Predictability*** (CUP 2003) | Directed NCEP's Environmental Modeling Center 1987-97; delivered the first operational ensemble forecasting | 369pp, 44 sections. Governing equations, NWP, **data assimilation**, predictability and ensembles |
| **Palmer, *The Primacy of Doubt*** | Met Office → ECMWF; drove the Ensemble Prediction System operational in 1992 | 367pp, 31 sections. Chaos, ensembles, and the honest reading of a spread — with chapters applying it to **financial crashes** and pandemics |
| **WWRP/WGNE, *Forecast Verification — Issues, Methods and FAQ*** | The joint working group Jolliffe chaired | ~99k chars. Reliability diagrams, Brier and Brier skill scores, ROC, ranked probability score, rank histograms, skill against a reference |
| **WGNE, *Recommendations for the Verification and Intercomparison of QPFs*** | as above | 24pp |

## Corpus
`_material/meteorologist/INDEX.md` is the entry point.

**Known gaps:**
- **Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide*** — the scoring half, not
  obtained. The WWRP reference covers the instruments but not the practitioner judgement around them.
- **CRPS does not appear anywhere in the held material.** If a pass needs it, look it up
  ([[lenses]] rule 7 permits researching the instrument).
- Palmer's index **over-splits** — some entries are drop-cap paragraph openers rather than chapters.
  Boundaries are sound, titles are mixed.

---

## GREP LOG
*A **coverage record, not a prohibition**. Anything not listed is untouched.*

| date | file / section | what was taken |
|---|---|---|
| 2026-08-24 | `wwrp_forecast_verification_methods_reference.txt` (term counts only, not read) | Confirmed present: reliability diagrams (7 mentions), Brier score and Brier skill score (12), ROC (25), ranked probability score (6), rank histograms (3), skill scores against a reference (25). Confirmed **absent: CRPS (0)** |
| 2026-08-24 | source `INDEX.md`s (titles only) | Located, not read: Palmer's **"Financial Crashes"** (p207-227) — the corpus's own attempt at this transfer, worth reading before repeating it — and **"Decisions! Decisions!"** (p245-257) on the cost-loss model. Kalnay's data-assimilation sections for EDA 3 |

**Untouched:** all of Kalnay, all of Palmer, the body of both verification documents.

## Log
- **2026-08-18 written** as a persona, F1-F7, no sources on disk.
- **2026-08-24 converted to CORPUS.** Fundamentals removed. **`Forbidden` deliberately kept four rules
  the corpus would itself teach** — an exception to the usual trimming rule, stated in the file. The
  reason: these are not facts about weather, they are the reason the lens exists, and the log shows we
  break them (#016 reported profit with no calibration; nothing in the log is scored against
  persistence or climatology). A fifth rule was added — do not confine this machinery to weather.
- **Cheapest real lead:** EDA 4 and 5, and neither needs weather data. Run a reliability diagram and a
  persistence-relative skill score on a signal we already hold (#044). If our own banked results turn
  out to be uncalibrated or no better than persistence, that is a more valuable finding than a gas
  trade — and it is a **METHOD-ledger** measurement, so it costs no `K`.
