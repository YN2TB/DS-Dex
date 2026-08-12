# Econometrics — subject context

**Status: ✅ complete** (2026-07-28). `contents/00-Index.md` plus chapters 01–12.

## Source

**Wooldridge, *Introductory Econometrics: A Modern Approach*, 7e** — `documents/Wooldridge-Introductory-Econometrics_-A-Modern-Approach.pdf`. **No lecture slides.**

This subject's `00-Index.md` is **the template for every textbook-only subject** — scope stated up front, followed by a "what is not covered, and why" section.

## Scope — my editorial decision, needs syllabus confirmation

**Chapters 1–12 (Wooldridge Parts 1 and 2)**: cross-sectional regression plus basic time series — the standard undergraduate one-semester sequence.

**Excluded: ch. 13–19** — panel data, IV/2SLS, simultaneous equations, limited dependent variables, advanced time series. Each is listed in the index with a one-line reason. **Ch. 15 (instrumental variables) is the omission most likely to matter** if the course emphasises endogeneity.

If new Econometrics material arrives, check it against this scope first — material from ch. 13–19 needs a **new chapter file and an index update**, not an edit to an existing note.

## Chapters

01 The Nature of Econometrics and Economic Data · 02 The Simple Regression Model · 03 Multiple Regression Analysis — Estimation · 04 — Inference · 05 — OLS Asymptotics · 06 — Further Issues · 07 Multiple Regression Analysis with Qualitative Information · 08 Heteroskedasticity · 09 More on Specification and Data Issues · 10 Basic Regression Analysis with Time Series Data · 11 Further Issues in Using OLS with Time Series Data · 12 Serial Correlation and Heteroskedasticity in Time Series Regressions

## No data files exist in the vault

`WAGE1`, `PHILLIPS`, `BARIUM`, `NYSE`, `EARNS` and the rest are **all absent**, so **no regression can be re-estimated.** Every regression in these notes is quoted as printed in the text.

**Every derived statistic stated in the notes was recomputed with scipy before writing and agrees with the text** — t ratios, F and LM statistics, p-values, turning points, confidence intervals, the Newey–West standard error. All exercises are my own construction with independently verified arithmetic.

## Extraction quirks

Two-column layout mangles maths: `b^ j` for $\hat\beta_j$, `E1u0x2` for $E(u\mid x)$, `g` for $\Sigma$, `R2 j` for $R^2_j$. **Every equation must be transcribed and checked by hand.**

**The minus sign renders as the digit `2` throughout** — every negative coefficient in these notes was sign-checked by hand against the surrounding prose.

All figures and all statistical tables are images and do not extract.

## Source problem worth remembering

**Table 9.1's turning point does not reconcile.** The printed coefficients give **0.379**; the text says **0.365**; no rounding bridges them. Recorded in the notes as an unresolved discrepancy, not silently corrected.

Cross-subject: `Time-series Analysis/contents/` covers the same stationarity / unit-root / serial-correlation material from the ARMA side — ch. 10–12 cross-link to it heavily. Ch. 03–05 lean on `Linear Algebra/contents/08 - Orthogonality.md` and `Optimization/contents/08 - Least Squares and Linear Equations.md`.
