---
subject: Mathematical Statistics
chapter: 09
tags: [ds, statistics, non-parametric, chi-squared, goodness-of-fit, independence]
source: "MS_Lec09_NonPara.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Non-parametric Testing

Reading: Devore & Berk ch. 13, pp. 723–757. Earlier tests assumed a distributional form (usually normal) and tested a parameter. Non-parametric tests drop that assumption.

> [!warning] Source note
> Formulas are images, but all example data tables and R outputs extracted.

## 📘 Main Knowledge

### χ² goodness-of-fit

Does the data follow a specified distribution? The lecturer's examples: quality levels A–D in proportions 10/20/30/40%; customers uniform across weekdays; forgotten luggage on trains Poisson.

$$\chi^2=\sum_{i=1}^{k}\frac{(O_i-E_i)^2}{E_i}\sim\chi^2_{k-1-m},\qquad E_i=np_i$$

$O_i$ observed, $E_i$ expected, $k$ categories, $m$ parameters estimated from the data.

- Always right-tailed: large χ² means poor fit.
- Fully specified distribution: df $=k-1$. Each estimated parameter costs one df (Poisson with λ estimated: $k-2$; normal with μ, σ estimated: $k-3$), because fitting makes the model match the data better by construction.
- Validity: $E_i\ge5$ in every cell; merge sparse categories otherwise.

### χ² test of independence

Are two categorical variables related? $A$ has $h$ categories, $B$ has $k$; observed counts $O_{ij}$ form a contingency table ([[02 - Tables and Charts]]).

Under independence $P(A_i\cap B_j)=P(A_i)P(B_j)$, so
$$E_{ij}=\frac{R_i\,C_j}{n}\quad(\text{row total}\times\text{column total}/n),\qquad \chi^2=\sum_{i,j}\frac{(O_{ij}-E_{ij})^2}{E_{ij}}\sim\chi^2_{(h-1)(k-1)}$$
$H_0$: independent; $H_1$: dependent. This is the statistic behind `sklearn`'s `chi2` scorer in [[Data Preparation and Visualization/contents/08 - Feature Selection|Feature Selection]].

### Normality tests

**Jarque–Bera**, from skewness $S$ and kurtosis $K$:
$$JB=\frac n6\left(S^2+\frac{(K-3)^2}{4}\right)\sim\chi^2_2$$
A normal distribution has $S=0$, $K=3$. Excel's `KURT` (and the slide-21 output) gives excess kurtosis $K-3$, so use it directly in place of $(K-3)$. In R: `jarque.bera.test(x)`.

χ² goodness-of-fit can also test normality by binning the data; with μ and σ estimated, df $=k-3$.

### Correlation test

$$H_0:\rho=0,\qquad t=\frac{r\sqrt{n-2}}{\sqrt{1-r^2}}\sim t_{n-2}$$
Tests the linear correlation of [[03 - Descriptive Statistics]]. Spearman's rank correlation applies the same idea to ranks and detects any monotonic relationship.

## ✏️ Exercises

Exercises 1–4 are the lecturer's examples.

**1.** (Example 9.1) A report claims quality levels A, B, C, D occur in proportions 10%, 20%, 30%, 40%. A sample of 400 gives 50, 60, 125, 165. Is the report inappropriate (a) at 5%, (b) at 2.5%? (c) p-value.

> [!example]- Solution
> | Level | $O$ | $E$ | $(O-E)^2/E$ |
> |---|---|---|---|
> | A | 50 | 40 | 2.500 |
> | B | 60 | 80 | 5.000 |
> | C | 125 | 120 | 0.208 |
> | D | 165 | 160 | 0.156 |
> | Sum | 400 | 400 | 7.865 |
>
> df 3 (nothing estimated).
> (a) $7.865>\chi^2_{0.05,3}=7.815$: reject, just.
> (b) $7.865<\chi^2_{0.025,3}=9.348$: don't reject.
> (c) R: `X-squared = 7.8646, df = 3, p-value = 0.04889` from `chisq.test(c(50,60,125,165), p = c(0.1,0.2,0.3,0.4))`.
> Borderline. Level B supplies 5.0 of the 7.86 (60 observed vs 80 expected); C and D fit well.

**2.** (Example 9.2) Test at 5% that customers are uniform across the week: Mon 290, Tue 250, Wed 238, Thu 257, Fri 265, Sat 230, Sun 192.

> [!example]- Solution
> $n=1722$, $E_i=246$.
>
> | Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
> |---|---|---|---|---|---|---|---|
> | $O-E$ | +44 | +4 | −8 | +11 | +19 | −16 | −54 |
> | $(O-E)^2/E$ | 7.870 | 0.065 | 0.260 | 0.492 | 1.467 | 1.041 | 11.854 |
>
> $\chi^2=23.05$, df 6, $23.05>12.592$: reject ($p=0.0008$). `chisq.test(customers)` uses equal probabilities by default.
> Sunday and Monday supply 19.7 of the 23.05: Sunday is quiet, Monday busy, the rest close to uniform.

**3.** (Example 9.3) Forgotten luggage $X$ on 300 trains. Test at 5% that $X$ is (a) Poisson(3), (b) Poisson with the mean estimated.

| $X$ | 0 | 1 | 2 | 3 | 4 | 5 | ≥6 |
|---|---|---|---|---|---|---|---|
| Freq | 30 | 50 | 70 | 65 | 45 | 25 | 15 |
| Prob | .050 | .149 | .224 | .224 | .168 | .101 | — |

> [!example]- Solution
> The printed probabilities are Poisson(3); the tail is $1-0.916=0.084$.
>
> (a) Fully specified, df 6.
>
> | $X$ | 0 | 1 | 2 | 3 | 4 | 5 | ≥6 |
> |---|---|---|---|---|---|---|---|
> | $E$ | 15.0 | 44.7 | 67.2 | 67.2 | 50.4 | 30.3 | 25.2 |
> | $(O-E)^2/E$ | 15.000 | 0.628 | 0.117 | 0.072 | 0.579 | 0.927 | 4.129 |
>
> $\chi^2=21.45>12.592$: reject ($p=0.0015$). The $X=0$ cell alone contributes 15: twice as many zeros as Poisson(3) predicts, and too few large counts.
>
> (b) $\hat\lambda=\bar x=780/300=2.6$ (treating ≥6 as 6). Expected counts from Poisson(2.6): 22.28, 57.93, 75.31, 65.27, 42.43, 22.06, 14.71. $\chi^2=4.69$, df $7-1-1=5$, critical value 11.070: don't reject ($p=0.46$).
>
> The data are consistent with a Poisson distribution, just not with mean 3; the true mean is lower. Estimating λ lowers χ², and the lost df lowers the critical value to compensate.

**4.** (Example 9.4) Test at 5% that a government office's "saying" (columns) and "doing" (rows) are independent. Categories: within 1 day, 2–3 days, more than 3 days.

> [!example]- Solution
> | | S1 | S2 | S3 | Row |
> |---|---|---|---|---|
> | D1 | 65 | 35 | 55 | 155 |
> | D2 | 70 | 30 | 70 | 170 |
> | D3 | 25 | 10 | 40 | 75 |
> | Col | 160 | 75 | 165 | 400 |
>
> Expected $R_iC_j/n$:
>
> | | S1 | S2 | S3 |
> |---|---|---|---|
> | D1 | 62.00 | 29.06 | 63.94 |
> | D2 | 68.00 | 31.88 | 70.13 |
> | D3 | 30.00 | 14.06 | 30.94 |
>
> $\chi^2=7.4385$, df 4, $7.4385<9.488$: don't reject. R: `X-squared = 7.4385, df = 4, p-value = 0.1145`.
>
> Not rejecting is not proof of independence. χ² also says nothing about direction or strength; look at standardized residuals $(O-E)/\sqrt E$ or Cramér's V.
>
> Slide 17's `matrix(c(65,35,55,70,30,70,25,10,40), 3, 3)` fills by column and builds the transpose (its printed row 1 is 65, 70, 25). χ² is unchanged by transposing, but use slide 18's `rbind` version or `byrow = TRUE`.

**5.** (Advanced) When should non-parametric tests be preferred, and what do they cost? Test slide 21's customer ages for normality: $n=100$, skewness 0.525, Excel kurtosis 0.0664.

> [!example]- Solution
> Prefer them when normality fails and $n$ is too small for the CLT, the data are ordinal ([[01 - Introduction to Statistics]]), there are outliers (ranks are robust), or the hypothesis is about a distribution's shape.
>
> Costs: less power when the parametric assumptions hold (Wilcoxon signed-rank has about 95% of the $t$-test's efficiency under normality); weaker conclusions (χ² shows dependence, not its form); magnitudes are discarded by rank tests; and the hypothesis changes (medians or distributions rather than means).
>
> Excel's kurtosis is excess kurtosis:
> $$JB=\frac{100}{6}\left(0.525^2+\frac{0.0664^2}{4}\right)=16.667(0.2756+0.0011)=4.612$$
> $4.612<\chi^2_{0.05,2}=5.991$: don't reject normality ($p=0.0997$). The departure comes almost entirely from skewness. Normality tests have little power at small $n$ and reject trivial departures at large $n$; a QQ plot shows where the distribution departs.

## 📝 Summary

- Non-parametric tests drop distributional assumptions: use them for non-normal small samples, ordinal data, outliers.
- Goodness-of-fit: $\sum(O-E)^2/E$, $E=np$, right-tailed, df $k-1-m$.
- Independence: $E_{ij}=R_iC_j/n$, df $(h-1)(k-1)$.
- Need $E\ge5$ in every cell.
- Cell contributions show where the misfit is.
- Jarque–Bera: $JB\sim\chi^2_2$ from skewness and kurtosis; Excel reports excess kurtosis.
- Correlation test: $t=r\sqrt{n-2}/\sqrt{1-r^2}$, df $n-2$.

## ⚠️ Important Notes

1. Every estimated parameter costs one df; forgetting this inflates significance.
2. χ² tests are right-tailed; a small statistic means good fit.
3. $E\ge5$ in every cell, or merge categories / use an exact test.
4. Don't round expected frequencies (29.06 is fine).
5. χ² shows that variables are dependent, not how; use residuals or Cramér's V.
6. Dependence is not causation, and non-rejection is not independence.
7. Don't subtract 3 twice: Excel's `KURT` is already excess kurtosis.
8. Normality tests: weak at small $n$, oversensitive at large $n$; prefer a QQ plot.
9. R's `matrix()` fills by column; use `rbind` or `byrow = TRUE`.
10. Use counts, not percentages, in a contingency table.
11. Report borderline p-values (Example 9.1: 0.0489).
12. Rejecting Poisson(3) does not reject Poisson: Example 9.3(b) fits with λ = 2.6.

> [!warning] Gaps in the source slides
> - Slides 2, 4, 10 (partly), 12–14, 20, 23 and 25 are title-only or images: the goodness-of-fit definition, the χ² statistic, the expected-frequency derivation, the independence statistic, the Jarque–Bera formula, the correlation test and the summary. All are standard reconstructions.
> - Slide 22 asks for Jarque–Bera and χ² normality tests on a sample whose data is an image.
> - Slide 9 (Example 9.3) gives no probability for ≥6; 0.084 is the Poisson(3) complement. Part (b)'s Poisson(2.6) calculation is mine.
> - Examples 9.5 (age × satisfaction, slide 19) and 9.6 (correlation of Q, P, Z, slide 24) have data but no solutions: extra practice.
> - The Wilcoxon test is listed on the contents slide but no slide covers it, so Wilcoxon signed-rank and rank-sum are missing from the material.
> - Corrected (2026-10-09): Example 9.3(b) gives χ² = 4.69 (p = 0.46), so Poisson with estimated mean is not rejected. The previous version left (b) uncomputed and claimed neither Poisson fits.
> - Exercise set: [1] ch. 13 (p. 730) 2–5, 9.

**Previous:** [[08 - Inferences on Two Samples]] · **Back to** [[00-Index]]
