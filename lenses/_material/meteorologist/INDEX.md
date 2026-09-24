# Meteorologist lens — corpus index

**Entry point.** Grep this file for the right source, then its own `INDEX.md` where it has one, then open ONLY the section you need. Every source has a `.txt` twin — **grep the text, never open a PDF to browse.**

| source | who | what | index |
|---|---|---|---|
| **Kalnay, *Atmospheric Modeling, Data Assimilation and Predictability*** (CUP 2003) | Directed NCEP's Environmental Modeling Center 1987-97; delivered the first operational ensemble forecasting | 369pp, **44 sections** — the PDF's own bookmarks were per-page scan artifacts, so sections were detected by typography instead. Governing equations, NWP, **data assimilation**, predictability and ensemble forecasting | `kalnay_atmospheric_modeling/INDEX.md` |
| **Palmer, *The Primacy of Doubt*** | Met Office -> ECMWF; drove the Ensemble Prediction System operational in 1992 | 367pp, **31 sections** — chaos, the geometry of chaos, Monte Carlo, **climate change, pandemics, financial crashes**, decisions under uncertainty. ⚠️ Detected by typography and it **over-splits**: some entries are drop-cap paragraph openers (`LET US RETURN TO the...`) rather than chapters. Boundaries are sound, titles are mixed | `palmer_primacy_of_doubt/INDEX.md` |

## Gaps

- **Jolliffe & Stephenson, *Forecast Verification: A Practitioner's Guide*** — backs F3, F4 and F7: calibration vs skill, scoring against a reference forecast, scoring every forecast on a fixed protocol. **This is the lens's scoring half, and it is the one thing missing.** Not obtained.

## Backbone — forecast verification (Jolliffe & Stephenson not obtained)

The book is the lens's **scoring half**, and its absence is the biggest single gap in the roster. Held
in its place, from the working group Jolliffe chaired:

| source | what it backs |
|---|---|
| **WWRP/WGNE Joint Working Group, *Forecast Verification — Issues, Methods and FAQ*** (~99k chars, captured as text) | F3, F4, F7. Documents **reliability diagrams (7), Brier score and Brier skill score (12), ROC (25), ranked probability score (6), rank histograms (3), skill scores against a reference (25)** — the exact instruments the lens's Forbidden list demands |
| **WGNE, *Recommendations for the Verification and Intercomparison of QPFs*** (24pp) | F4 — scoring against a reference forecast rather than against zero |

⚠️ **CRPS does not appear in the captured reference** — if a pass needs it, look it up separately
([[lenses]] rule 7 permits researching the instrument).
