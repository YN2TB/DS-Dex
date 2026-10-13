# Mathematical Statistics: subject context

**Status: ✅ complete** (2026-07-27), rewritten concisely 2026-10-09. `contents/00-Index.md` plus chapters 01–09.

## Sources

9 `.pptx` decks in `documents/slides/` by Bui Duong Hai (Actuary Bachelor Degree). Reference textbooks in `documents/`: Devore 2e, Miller & Freund 8e, Hogg 7e, Larsen 6e.

## Chapters

01 Introduction to Statistics · 02 Tables and Charts · 03 Descriptive Statistics · 04 Sampling Distributions · 05 Point Estimation · 06 Confidence Interval · 07 Hypothesis Testing - One Sample · 08 Inferences on Two Samples · 09 Non-parametric Testing

## Extraction

Every equation is an embedded image, so none survive `python-pptx`. Lecture 04 has 22 of 31 slides title-only, Lecture 05 24 of 29. Formulas in ch. 03–09 are standard textbook forms reconstructed from slide titles; the lecturer's notation may differ. If the user supplies clearer slides or photos, correct the note.

Reliable: data tables, Excel output, R code and output, example statements in Lectures 6–9, exercise-set references.

Missing: Lecture 1's probability revision, the CLT statement, Fisher information and Cramér–Rao, Examples 5.1–5.9, 7.1, 7.2, 7.7, 7.8, 8.2, and the Wilcoxon test (promised on Lecture 9's contents slide).

## Corrections in the 2026-10-09 rewrite

- ch03: grouped mean 7.65 → 8.4.
- ch04 Ex. 5: power at $n=100$ with fixed limits is 0.50, not 99.99%.
- ch07: `CHISQ.DIST.RT(30.4, 19)` = 0.0469, not 0.0476.
- ch09 Example 9.3(b): Poisson(2.6) gives χ² = 4.69, df 5, p = 0.46 (not rejected); the old note claimed neither Poisson fits.

Cross-subject: probability foundations are in `Probability Theory/contents/` ch. 04–08.
