# Time-series Analysis: subject context

**Status: ✅ complete** (2026-07-27), rewritten concisely 2026-10-09. `contents/00-Index.md` plus chapters 01–10.

## Sources

11 Colab notebooks in `documents/slides/*.ipynb` (not PDFs). Slides are HTML strings in `%%html` / `HTML(...)` cells: read the JSON and strip tags. Lecturer: Dr. Tran Thi Ha, Faculty of Mathematical Economics. Reference books in `documents/`: Hamilton, Peixeiro, Auffarth.

## Extraction bug

Stripping HTML tags eats `<` inside inline LaTeX, so `\(|\phi| < 1\)` becomes `\(|\phi| \)`. Every such inequality in the notes is a reconstruction. When re-extracting, protect `\(...\)` spans before stripping tags.

## Numbering

Filenames, not the syllabus, define chapters from Lecture 6: 06 Kalman Filter, 07 SARIMA + VAR, 08 VECM, 09 ARCH/GARCH, 10 SVAR. The ARCH deck calls itself "Lecture 10". Two VECM notebooks (`lecture08_VECM_DSEB.ipynb`, 57 cells; `VECM_lecture_slides.ipynb`, 16 cells) are complementary; ch. 08 uses both.

## Chapters

01 What is a Time Series · 02 Trend, Seasonality and Decomposition · 03 Stationarity and Difference Equations · 04 AR, MA and ARMA Processes · 05 ACF, PACF and the Box-Jenkins Methodology · 06 The Kalman Filter and State-Space Models · 07 SARIMA and Vector Autoregression · 08 VECM and Cointegration · 09 ARCH, GARCH and Extensions · 10 Structural Vector Autoregression

## Slide errors (corrected in the notes)

- ch. 02: ETS(A,A,M) level/trend updates should use $e_t/s_{t-m}$ (found 2026-10-09).
- ch. 03: the stability-triangle figure contradicts its caption.
- ch. 04: MA(2) example $\gamma_0=31/19$ → 31/18; roots −2, −3 → +2, +3.
- ch. 05: Bartlett's variance formula omits the leading 1 and the factor 2.

**Verified correct, don't "fix"**: the AR(3) Yule–Walker values, the CPI PACF arithmetic, Example 7.1's IRF/FEVD, both VECM Π = αβ′ decompositions, and ch. 08's Johansen critical values (17.8, 11.2, 4.13 are the standard 5% max-eigenvalue values for three variables without deterministic terms, statsmodels `det_order=-1`; an earlier note wrongly flagged them).

If the user questions a formula, check whether it is a reconstructed inequality or a flagged slide error before assuming the note is wrong.

## Data and figures

All data files are missing except `lutkepohl2.dta` and `m1gdp.dta` (fetched from stata-press.com). No notebook saved outputs, so no figures survive. Only Lectures 3 and 4 have exercises (no solutions); the other exercises are constructed and checked.

## Named but never taught

IGARCH/FIGARCH, structural FEVD, sign restrictions, the Kalman smoother, weak-exogeneity testing, seasonal unit-root tests, IRF confidence bands.

Cross-subject: `Econometrics/contents/` ch. 10–12 covers stationarity, unit roots and serial correlation from the regression side.
