---
subject: Mathematical Statistics
chapter: 00
tags: [ds, moc, index, statistics, inference, actuarial]
source: "MS_Lec01_Intro.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Mathematical Statistics: Index

Lecturer: Bui Duong Hai, Faculty of Mathematical Economics, NEU (`www.mfe.edu.vn/buiduonghai`). Programme: Actuary Bachelor Degree.

## Map of content

| # | Chapter | Topics | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to Statistics]] | branches, data sources, population vs sample, variable types | ✅ |
| 02 | [[02 - Tables and Charts]] | frequency and cross tables, percentage directions, histograms, ogives | ✅ |
| 03 | [[03 - Descriptive Statistics]] | centre, spread, $n-1$, CV, IQR, boxplots, skewness, correlation | ✅ |
| 04 | [[04 - Sampling Distributions]] | distribution of $\bar X$, CLT, standard error, χ² and $t$ | ✅ |
| 05 | [[05 - Point Estimation]] | MSE, method of moments, MLE, Fisher information, Cramér–Rao | ✅ |
| 06 | [[06 - Confidence Interval]] | CIs for mean, variance, proportion; prediction intervals; sample size | ✅ |
| 07 | [[07 - Hypothesis Testing - One Sample]] | errors, power, p-values, Neyman–Pearson | ✅ |
| 08 | [[08 - Inferences on Two Samples]] | paired vs independent, pooled and Welch $t$, F-test, two proportions | ✅ |
| 09 | [[09 - Non-parametric Testing]] | χ² goodness-of-fit and independence, Jarque–Bera, correlation test | ✅ |

Chapters 01–03 describe the sample, 04 explains how statistics behave across samples, 05–09 estimate and test. Lecture 1's caution: "Statistics is the fact? Yes, but No!": always ask whether the data are accurate and the method appropriate.

**Software:** Excel with the Data Analysis Toolpak, SPSS, R. Commands are in ch. 03 (Excel functions), 06 (CI programs) and 08 (`t.test`, `var.test`).

**Textbooks:** Devore & Berk (2012) 2nd ed. (primary, most exercise sets); Miller & Miller (2014) 8th ed.; Hogg, McKean & Craig (2013) 7th ed. All three are in `documents/`, plus Larsen (2018), which the slides don't cite. Anderson et al., *Statistics for Business and Economics* 12th ed., cited for Lectures 1–3, is not in `documents/`.

## Which test?

| Situation | Test |
|---|---|
| one mean, σ known | $z$ |
| one mean, σ unknown | $t$, df $n-1$ |
| one variance | χ², df $n-1$ |
| one proportion, large $n$ | $z$ (SE uses $p_0$) |
| one proportion, small $n$ | exact binomial |
| two means, paired | $t$ on differences, df $n-1$ |
| two means, independent, equal variances | pooled $t$, df $n_1+n_2-2$ |
| two means, independent, unequal variances | Welch $t$ (default) |
| two variances | $F$, df $(n_1-1,n_2-1)$ |
| two proportions | $z$ (SE pools) |
| distribution shape | χ² goodness-of-fit, df $k-1-m$ |
| two categorical variables | χ² independence, df $(h-1)(k-1)$ |
| normality | Jarque–Bera, $\chi^2_2$ |
| correlation ≠ 0 | $t=r\sqrt{n-2}/\sqrt{1-r^2}$, df $n-2$ |

A two-sided test at α rejects exactly when the $(1-\alpha)$ CI excludes the null value.

## Cross-subject links

| Topic | Subject |
|---|---|
| random variables, distributions | [[Probability Theory/contents/00-Index\|Probability Theory]] |
| $t$-tests in regression | [[Econometrics/contents/00-Index\|Econometrics]] |
| χ² and F as feature filters; z-scores as `StandardScaler` | [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] |
| bias–variance, MLE as a loss, shrinkage | [[Machine Learning/contents/00-Index\|Machine Learning]] |
| autocorrelation, stationarity | [[Time-series Analysis/contents/00-Index\|Time-series Analysis]] |

## Gaps in the source material

> [!warning] Formulas are images
> The decks embed equations as images, which don't extract. Title-only slides: Lec 03 ~20/49, Lec 04 22/31, Lec 05 24/29, Lec 06 ~12/23, Lec 07 ~18/28, Lec 08 ~14/38, Lec 09 ~8/26. Formulas in ch. 03–09 are standard textbook forms; the lecturer's notation may differ. Data tables, Excel and R output, the example statements in Lectures 6–9 and the exercise references all extracted.

Missing content:
- Lecture 1's probability revision (slides 24–27); see [[Probability Theory/contents/00-Index|Probability Theory]].
- The CLT statement (Lec 4, slides 14–16) and Fisher information / Cramér–Rao (Lec 5, slides 21–23).
- All of Lecture 5's Examples 5.1–5.9; Examples 7.1, 7.2, 7.7, 7.8 (question) and 8.2. Lecture 7 skips 7.4.
- The Wilcoxon test, promised on Lecture 9's contents slide.
- Lecture 3 slide 45 ("Combined sample").
- Lecture 8 slide 3 lists Firm B's values as 75/87; the examples and their outputs use 72/88.
- Slide code errors: Lec 6 slide 23 (Wilson interval precedence), Lec 9 slide 17 (`matrix()` transposes).

Corrections made in the 2026-10-09 rewrite: ch03 grouped mean (8.4), ch04 Exercise 5 power, ch07 χ² p-value (0.0469), ch09 Example 9.3(b) (Poisson with estimated mean fits, $p=0.46$).
