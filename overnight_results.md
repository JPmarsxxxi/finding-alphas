# Lens measurement batch — 2026-08-18/19

**LEDGER: METHOD trials.** Discovery sample only (<= 2024-12-31). The sealed holdout is not
touched by anything here and `K` is unaffected. These are measurements, not crossings.

Equity panel: 14276 rows x 41 names, 1970-01-02 .. 2026-08-14

---

## 1. A02 — overnight return conditioned on same-day intraday vol (economist)

#041: **+17.77 bp, t +3.11, n=3232**, died at 2.78x on a *banked estimate* of 6.40 bp cost.
Re-measured here with (a) stale opens removed, (b) a real per-symbol spread.

pooled rows before filtering: 379,447
after removing stale opens:   304,356  (19.8% dropped)

**WITH stale opens (as #041 measured it)** — overnight return (bp) by same-day intraday-vol quintile

| ivol quintile | n | mean bp | t |
|---|---:|---:|---:|
| q0 | 75,922 | +2.66 | +9.77 |
| q1 | 75,911 | +3.12 | +9.42 |
| q2 | 75,849 | +4.05 | +10.84 |
| q3 | 75,868 | +4.06 | +8.99 |
| q4 | 75,897 | +9.38 | +12.02 |

**STALE OPENS REMOVED** — overnight return (bp) by same-day intraday-vol quintile

| ivol quintile | n | mean bp | t |
|---|---:|---:|---:|
| q0 | 60,892 | +3.30 | +9.80 |
| q1 | 60,872 | +3.84 | +9.33 |
| q2 | 60,850 | +4.94 | +10.71 |
| q3 | 60,863 | +5.39 | +9.55 |
| q4 | 60,879 | +11.55 | +11.83 |

Top-quintile effect: **+9.38 bp (t +12.02)** with stale opens, **+11.55 bp (t +11.83)** without.

---

## 1b. The cost measurement A02 never got

spread profile: 315 rows, 45 symbols, ny_hour 9..15

Round trip = half-spread at entry (NY 15-16, close) + at exit (NY 9-10, open).

| | bp |
|---|---:|
| median round trip across 45 symbols | **12.23** |
| 25th pct (cheapest quartile) | 9.12 |
| 75th pct | 18.37 |
| #041's banked ESTIMATE | 6.40 |

- edge/cost on **median** cost (12.23 bp): **0.94x**  (bar is 5x)
- edge/cost on **cheapest quartile** cost (9.12 bp): **1.27x**  (bar is 5x)
- edge/cost on **banked estimate** cost (6.40 bp): **1.80x**  (bar is 5x)

---

## 2. Frequency x severity — the split neither lens could compute before

Underwriter F2 / statistician F7: a mean bp figure is frequency x severity already collapsed.

| ivol quintile | n | win rate | mean WIN bp | mean LOSS bp | mean bp |
|---|---:|---:|---:|---:|---:|
| q0 | 60,892 | 53.4% | +48.6 | -48.6 | +3.30 |
| q1 | 60,872 | 53.8% | +57.9 | -59.2 | +3.84 |
| q2 | 60,850 | 53.5% | +68.7 | -68.5 | +4.94 |
| q3 | 60,863 | 53.5% | +82.8 | -83.8 | +5.39 |
| q4 | 60,879 | 53.9% | +131.6 | -128.9 | +11.55 |

---

## 3. Effective sample size (statistician F3)

Row counts flatter you. Overlapping/correlated observations mean effective n << row count.

| | |
|---|---:|
| rows in top quintile | 60,879 |
| distinct DAYS | 11,130 |
| names | 41 |
| mean pairwise corr of same-day overnight returns | **0.499** |
| **effective n** (cross-sectional clustering) | **2,905** |

Deflation factor on the t-stat: **0.218x** — a t of +3.11 becomes ~**+0.68**.

---

## 4. Noise floor for the searched grid (signal-processing F1)

Expected maximum |t| from pure noise at this trial count, vs what we observed.

-   5 cells -> expected max |t| under noise ~ **1.79**
-  25 cells -> expected max |t| under noise ~ **2.54**
- 224 cells -> expected max |t| under noise ~ **3.29**

(#041 measured this once: best t across 224 cells was +1.98 vs ~2.2 expected. It should be routine.)

---

## 5. Stale-open rate by decade (historian EDA2 — wanted by 3 lenses)

Permanent name-level quirk, or an artifact that stopped when quoting went electronic?
**Decides whether the panel's early history is usable at all.**

| decade | names | median stale-open rate | min | max |
|---|---:|---:|---:|---:|
| 1970s | 15 | **73.6%** | 57.6% | 89.7% |
| 1980s | 22 | **38.8%** | 26.8% | 83.7% |
| 1990s | 30 | **19.9%** | 3.8% | 78.0% |
| 2000s | 35 | **8.0%** | 0.5% | 18.5% |
| 2010s | 39 | **2.2%** | 0.6% | 8.3% |
| 2020s | 41 | **1.7%** | 0.1% | 4.8% |

---

## 6. Mean pairwise correlation by sub-period (historian EDA3)

Pooled figure is **0.305** across 1970-2024. A 55-year average is not a number.

| decade | names w/ data | mean pairwise corr |
|---|---:|---:|
| 1970s | 11 | **0.343** |
| 1980s | 20 | **0.348** |
| 1990s | 24 | **0.230** |
| 2000s | 30 | **0.331** |
| 2010s | 37 | **0.367** |
| 2020s | 41 | **0.361** |

---

## 7. #024 re-asked as a SIZE claim, not a mean (flow F1)

Flow F1: positioning is not a direction signal, it is a **fragility** signal — it predicts
the SIZE of the move if something forces the exit. #024 tested it as a conditional mean.

COT: 24,496 rows, 15 symbols, 1986-01-15 .. 2024-12-31

price panel: 313,160 rows, 45 symbols

pooled: 11,218 symbol-weeks across 9 symbols

**SIZE, not direction** — forward 4-week |move| and realised vol by positioning extreme

| positioning z | n | mean fwd \|move\| % | median | fwd realised vol % |
|---|---:|---:|---:|---:|
| <-2 (crowded short) | 385 | **3.52** | 2.24 | 2.07 |
| -2..-1 | 1,922 | **2.82** | 1.93 | 1.63 |
| -1..1 (normal) | 6,520 | **2.64** | 1.86 | 1.50 |
| 1..2 | 2,031 | **2.68** | 1.91 | 1.52 |
| >2 (crowded long) | 360 | **2.36** | 1.83 | 1.48 |

Extreme vs normal positioning: **2.96%** vs **2.64%** = **1.12x** the forward move size.

For contrast, the MEAN test #024 actually ran (signed forward return):

| positioning z | n | mean fwd return % | t |
|---|---:|---:|---:|
| <-2 (crowded short) | 385 | -0.16 | -0.60 |
| -2..-1 | 1,922 | +0.18 | +1.85 |
| -1..1 (normal) | 6,520 | +0.21 | +4.30 |
| 1..2 | 2,031 | +0.32 | +3.81 |
| >2 (crowded long) | 360 | -0.35 | -2.05 |

---

*End of batch. All measurements on the discovery sample; the sealed holdout was not opened.*
