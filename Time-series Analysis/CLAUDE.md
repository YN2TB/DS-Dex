# Time-series Analysis — subject context

**Status: ✅ complete** (2026-07-27). `contents/00-Index.md` plus chapters 01–10.

## Sources

**11 Colab notebooks** in `documents/slides/*.ipynb` — **not PDFs**. Slides are HTML strings inside `%%html` / `HTML(...)` cells; extract by reading the JSON and stripping tags. Instructor: **Dr. Tran Thi Ha**, Faculty of Mathematical Economics.

`documents/` also holds Hamilton, Peixeiro (*Time Series Forecasting in Python*) and Auffarth as reference books.

## ⚠️ A systematic extraction bug affects every chapter

**Stripping HTML tags eats `<` inside inline LaTeX**, silently truncating conditions like `\(|\phi| < 1\)` to `\(|\phi| \)`. **Every inequality of that form in the notes is a reconstruction** — mathematically certain, but not the lecturer's original wording. Each chapter's gaps callout lists its own cases.

If you re-extract, handle `<` before tag-stripping (e.g. protect `\(...\)` spans first).

## Numbering: filenames beat the syllabus

**Syllabus titles diverge from filenames from Lecture 6 on.** The notes follow the **filenames**: 06 Kalman Filter, 07 SARIMA+VAR, 08 VECM, 09 ARCH/GARCH, 10 SVAR. The ARCH deck titles itself "Lecture 10", clashing with the SVAR deck.

**Two VECM notebooks exist and are complementary, not duplicates** — `lecture08_VECM_DSEB.ipynb` (57 cells, full derivation) and `VECM_lecture_slides.ipynb` (16 cells, overview with VECM IRFs). Ch. 08 uses both.

## Chapters

01 What is a Time Series · 02 Trend, Seasonality and Decomposition · 03 Stationarity and Difference Equations · 04 AR, MA and ARMA Processes · 05 ACF, PACF and the Box-Jenkins Methodology · 06 The Kalman Filter and State-Space Models · 07 SARIMA and Vector Autoregression · 08 VECM and Cointegration · 09 ARCH, GARCH and Extensions · 10 Structural Vector Autoregression

## Errors found in the slides and corrected in the notes

- **ch. 04** — the MA(2) example prints $\gamma_0=31/19$ (correct **31/18**) and roots $-2,-3$ (correct **$+2,+3$**)
- **ch. 03** — the stability-triangle figure contradicts its own caption
- **ch. 05** — the Bartlett variance formula omits the leading 1 and the factor 2
- **ch. 08** — the Johansen critical values match no standard table

**Verified correct** (so don't "fix" these): the AR(3) Yule–Walker values, the CPI PACF arithmetic, Example 7.1's IRF/FEVD, both VECM $\Pi=\alpha\beta'$ decompositions.

*If the user questions a formula, check whether it is one of the reconstructed inequalities or a flagged slide error before assuming the note is wrong.*

## Data and figures

**All data files are missing except two** — `lutkepohl2.dta` and `m1gdp.dta`, fetched from stata-press.com at runtime. **No notebook saved any cell outputs**, so **no figure survives**. Slides provide exercises only in Lectures 3 and 4, and without solutions — every other exercise in the notes is my own construction with verified arithmetic.

## Topics named on title slides but never taught — flag to the lecturer

IGARCH/FIGARCH, structural FEVD, sign restrictions, the Kalman smoother, weak-exogeneity testing, seasonal unit-root tests, IRF confidence bands.

Cross-subject: `Econometrics/contents/` ch. 10–12 covers the same stationarity / unit-root / serial-correlation material from the regression side and cross-links heavily.
