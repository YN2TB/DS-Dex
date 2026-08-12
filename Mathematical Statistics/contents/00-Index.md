---
subject: Mathematical Statistics
chapter: 00
tags: [ds, moc, index, statistics, inference, actuarial]
source: "MS_Lec01_Intro.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Mathematical Statistics — Index

**Lecturer:** Bui Duong Hai, Faculty of Mathematical Economics, NEU
`haitkt@gmail.com` · `www.mfe.edu.vn/buiduonghai`

**Programme:** Actuary Bachelor Degree

## 🗺️ Map of Content

### Part 1 — Descriptive Statistics

| # | Chapter | One-line description |
|---|---|---|
| 01 | [[01 - Introduction to Statistics]] | Branches, data sources, population vs sample, and the variable-type taxonomy that governs everything after |
| 02 | [[02 - Tables and Charts]] | Frequency and cross tables, the three percentage directions, histograms, ogives, distribution shape |
| 03 | [[03 - Descriptive Statistics]] | Mean/median/mode, variance and $n-1$, CV, IQR, boxplots, skewness, correlation, z-scores |

### Part 2 — The Bridge: Probability into Inference

| # | Chapter | One-line description |
|---|---|---|
| 04 | [[04 - Sampling Distributions]] | **The pivot of the course** — $\bar X$'s distribution, the CLT, standard error, $\chi^2$ and $t$ |
| 05 | [[05 - Point Estimation]] | Estimator vs estimate, MSE = variance + bias², MLE, Fisher information, Cramér–Rao |

### Part 3 — Statistical Inference

| # | Chapter | One-line description |
|---|---|---|
| 06 | [[06 - Confidence Interval]] | CIs for mean, variance, and proportion; prediction intervals; sample size determination |
| 07 | [[07 - Hypothesis Testing - One Sample]] | $H_0$/$H_1$, Type 1 and 2 errors, power, p-values, Neyman–Pearson |
| 08 | [[08 - Inferences on Two Samples]] | Paired vs independent, pooled and Welch $t$-tests, the F-test, two proportions |
| 09 | [[09 - Non-parametric Testing]] | χ² goodness-of-fit and independence, normality tests, correlation testing |

---

## 🎯 Course framing

### The organising question

**How do you learn something about a population you cannot observe, from a sample you can?**

Chapters 01–03 describe what you have. Chapter 04 explains how a sample statistic *behaves*, which is the licence for everything else. Chapters 05–09 use that licence — to estimate, to bound, and to decide.

### Two branches

- **Descriptive Statistics** — organise, summarise, present.
- **Inferential Statistics** — predict, forecast, verify.

The lecturer's hierarchy places **Probability** beneath Inferential Statistics; "Normal Statistics" covers description plus basic inference, while **Mathematical Statistics** is the probability-grounded treatment. Hence [[Probability Theory/contents/00-Index|Probability Theory]] is the prerequisite.

### The caution stated in Lecture 1

> **Statistics is the fact? Yes, but No!**
>
> Statistics may be biased. Without testing for correctness, decisions would be wrong. Two questions always: **Is the data accurate? Is the method appropriate?**

### Software

Microsoft Excel with the **Data Analysis Toolpak** · IBM SPSS · **R** · calculator. Data and extra material at `www.mfe.edu.vn/buiduonghai` → *Program* → *Class*.

Excel and R commands are collected in [[03 - Descriptive Statistics]] (statistics functions), [[06 - Confidence Interval]] (four CI programs), and [[08 - Inferences on Two Samples]] (`t.test`, `var.test`).

### Textbooks

1. **Devore & Berk (2012)**, *Modern Mathematical Statistics with Applications*, 2nd ed., Springer — **the primary text**, source of nearly all exercise sets ✅ *in `documents/`*
2. **Miller & Miller (2014)**, *John E. Freund's Mathematical Statistics with Applications*, 8th ed., Pearson ✅ *in `documents/`*
3. **Hogg, McKean & Craig (2013)**, *Introduction to Mathematical Statistics*, 7th ed., Pearson ✅ *in `documents/`*
4. **Anderson, Sweeney, Williams, Camm, Cochran (2017)**, *Statistics for Business and Economics*, 12th ed., South-Western — ⚠️ **not in `documents/`**, though cited in the Lecture 1–3 exercise sets

*(`documents/` also holds Larsen (2018), *An Introduction to Mathematical Statistics and Its Application*, 6th ed., which the slides do not cite.)*

---

## 🔗 Cross-subject connections

| Topic | Links to |
|---|---|
| Random variables, distributions, expectation | [[Probability Theory/contents/00-Index\|Probability Theory]] |
| Hypothesis testing, $t$-tests, dummy variables | [[Econometrics/contents/00-Index\|Econometrics]] |
| χ² and ANOVA F as feature filters; `StandardScaler` as the z-score | [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] |
| Bias–variance trade-off, MLE as a loss function, regularisation as shrinkage | [[Machine Learning/contents/00-Index\|Machine Learning]] |
| Sampling, stationarity, autocorrelation | [[Time-series Analysis/contents/00-Index\|Time-series Analysis]] |
| Credibility theory, loss distributions, percentile matching | *Actuarial applications throughout* |

---

## ⚠️ Gaps in the source material

> [!warning] The formulas are almost all images
> **This is the defining limitation of this subject's notes.** The slides were authored with equations as embedded images, which do not survive text extraction. Roughly:
>
> | Lecture | Slides with title only |
> |---|---|
> | 03 Descriptive | ~20 of 49 |
> | **04 Sampling** | **22 of 31** |
> | **05 Estimation** | **24 of 29** |
> | 06 Interval | ~12 of 23 |
> | 07 Testing | ~18 of 28 |
> | 08 Two samples | ~14 of 38 |
> | 09 Non-parametric | ~8 of 26 |
>
> **Every formula in chapters 03–09 is the standard textbook form, reconstructed from slide titles and section headings.** They are correct as mathematics, but **notation may differ from the lecturer's** — and notation matters in exams. Verify against the original `.pptx` files or Devore.
>
> **What survived and is reliable:** all data tables, all Excel outputs, all R code and output, all example *problem statements* in Lectures 6–9, the standard normal table (truncated at $z=0.7$), the binomial table for $B(20, 0.3)$, and every exercise set reference.

> [!warning] Specific content gaps
> **1. The probability revision (Lecture 1, slides 24–27) is entirely images.** Expectation, variance, and the standard discrete/continuous distributions are not captured anywhere. Use [[Probability Theory/contents/00-Index|Probability Theory]] or Devore Ch. 2–4.
>
> **2. The Central Limit Theorem statement (Lecture 4, slides 14–16) is an image** — the single most important result in the course.
>
> **3. Fisher information and Cramér–Rao (Lecture 5, slides 21–23) are images**, as is the MLE definition. These are core actuarial exam material.
>
> **4. All nine worked examples in Lecture 5 (5.1–5.9) are lost**, including two that ask "find the estimators of the following parameters" where the parameter list is itself an image.
>
> **5. Examples 7.1, 7.2, 7.7, 7.8 and 8.2 are lost.** Lecture 7's numbering skips 7.4 entirely, suggesting a missing slide.
>
> **6. The Wilcoxon test is promised on Lecture 9's contents slide but never appears.** The deck ends at the correlation test — signed-rank and rank-sum are missing from the provided material entirely.
>
> **7. Slide 45 of Lecture 3 ("Combined sample") is title-only** — presumably pooled mean/variance formulas for merging samples.
>
> **8. A data discrepancy in Lecture 8:** slide 3 lists Firm B's values differently from Examples 8.3–8.5 (75/87 vs 72/88). The Excel and R outputs match the *examples*, so I used those.
>
> **9. Two R code errors in the slides:** Lecture 6 slide 23's Wilson interval has operator-precedence bugs (`za^2/2*n` should be `za^2/(2*n)`), and Lecture 9 slide 17's `matrix()` builds the transpose of the intended table. Both are noted in place.

---

## 📌 The one-page revision path

The load-bearing ideas, in dependency order:

1. **Variable type determines permitted operations** — and therefore which statistic, chart, and test is valid — [[01 - Introduction to Statistics]]
2. **Row-% ≠ column-%** (the base rate fallacy) — [[02 - Tables and Charts]]
3. **Sample variance divides by $n-1$** for unbiasedness; **only the mean is outlier-sensitive** — [[03 - Descriptive Statistics]]
4. **$\operatorname{Var}(\bar X) = \sigma^2/n$, so precision improves with $\sqrt n$**; the **CLT** makes $\bar X$ normal regardless of the population — [[04 - Sampling Distributions]]
5. **$\text{MSE} = \text{Var} + \text{Bias}^2$**; MLE maximises $\ell = \ln L$ — [[05 - Point Estimation]]
6. **"95% confidence" describes the procedure, not the interval**; a **PI is much wider than a CI and never shrinks to zero** — [[06 - Confidence Interval]]
7. **Never "accept $H_0$"**; the p-value is $P(\text{data}\mid H_0)$, not $P(H_0\mid\text{data})$ — [[07 - Hypothesis Testing - One Sample]]
8. **Paired vs independent is decided by the design**, and pairing removes between-unit variation — [[08 - Inferences on Two Samples]]
9. **Every estimated parameter costs a degree of freedom** in χ² — [[09 - Non-parametric Testing]]
10. **A two-sided test at $\alpha$ ⟺ whether the $(1-\alpha)$ CI contains the null value** — the unifying identity of chapters 06–08

### Which test do I use?

| Situation | Test |
|---|---|
| One mean, $\sigma$ known | $z$-test |
| One mean, $\sigma$ unknown | $t$-test, $df = n-1$ |
| One variance | $\chi^2$, $df = n-1$ |
| One proportion, large $n$ | $z$-test (SE uses $p_0$) |
| One proportion, small $n$ | Exact binomial |
| Two means, paired | $t$-test on differences, $df = n-1$ |
| Two means, independent, equal var. | Pooled $t$, $df = n_1+n_2-2$ |
| Two means, independent, unequal var. | **Welch $t$** (preferred default) |
| Two variances | $F$-test, $df = (n_1-1, n_2-1)$ |
| Two proportions | $z$-test (SE **pools**) |
| Distribution shape | χ² goodness-of-fit, $df = k-1-m$ |
| Two categorical variables | χ² independence, $df = (h-1)(k-1)$ |
| Normality | Jarque–Bera, $\chi^2_2$ |
| Correlation ≠ 0 | $t = \frac{r\sqrt{n-2}}{\sqrt{1-r^2}}$, $df = n-2$ |
