---
subject: Mathematical Statistics
chapter: 09
tags: [ds, statistics, non-parametric, chi-squared, goodness-of-fit, independence]
source: "MS_Lec09_NonPara.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Non-parametric Testing

> [!note] Reading
> **[1] Devore & Berk, Ch. 13, pp. 723–757**
>
> The final lecture. Every test so far assumed a **distributional form** — normality, usually — and tested a **parameter** ($\mu$, $\sigma^2$, $p$). Non-parametric tests drop that assumption, which is what makes them the fallback when normality fails.

> [!warning] Source note
> Formulas are equation images, but **all example data tables and R outputs extracted in full**, so the worked results below are the lecturer's own.

## 📘 Main Knowledge

### The χ² goodness-of-fit test

**Question:** does the data follow a specified distribution?

The lecturer's three examples of the question:
- Product quality levels A, B, C, D are in proportions 10%, 20%, 30%, 40%.
- Customers across weekdays are **uniform** (same proportion each day).
- Forgotten luggage on trains follows a **Poisson** distribution.

**The test statistic:**

$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i} \;\sim\; \chi^2_{k-1-m}$$

where $O_i$ is the observed frequency, $E_i = n \times p_i$ the expected frequency, $k$ the number of categories, and $m$ the number of parameters **estimated from the data**.

**Always right-tailed** — large $\chi^2$ means observed and expected diverge, so we reject. A small $\chi^2$ means good fit.

> [!warning] Degrees of freedom depend on what you estimated
> - Distribution **fully specified** (proportions given, or Poisson with a stated mean): $df = k - 1$.
> - **One parameter estimated** from the data (Poisson with $\lambda$ estimated by $\bar x$): $df = k - 2$.
>
> Every estimated parameter costs one degree of freedom, because fitting it makes the model match the data better *by construction*. Example 9.3(a) vs 9.3(b) is precisely this contrast.

The standard validity requirement is $E_i \ge 5$ for every cell; merge sparse categories if not.

### The χ² test of independence

**Question:** are two categorical variables related?

Characteristic $A$ has $h$ categories $A_1,\dots,A_h$; characteristic $B$ has $k$ categories $B_1,\dots,B_k$. The observed frequency of $(A_i, B_j)$ is $F_{ij}$, laid out in a **contingency table** — the cross tables of [[02 - Tables and Charts]].

**Expected frequencies under independence.** If $A$ and $B$ are independent then $P(A_i \cap B_j) = P(A_i)P(B_j)$, so

$$E_{ij} = n \times \frac{R_i}{n} \times \frac{C_j}{n} = \frac{R_i \times C_j}{n}$$

**row total × column total ÷ grand total.**

$$\chi^2 = \sum_{i=1}^{h}\sum_{j=1}^{k}\frac{(O_{ij}-E_{ij})^2}{E_{ij}} \;\sim\; \chi^2_{(h-1)(k-1)}$$

- $H_0$: the two variables are **independent**
- $H_1$: they are **dependent**

This is the same χ² used for feature selection in [[Data Preparation and Visualization/contents/08 - Feature Selection|Feature Selection]] — `sklearn`'s `chi2` scorer is exactly this statistic.

### Normality tests

**Jarque–Bera** tests normality through **skewness** $S$ and **kurtosis** $K$:

$$JB = \frac{n}{6}\left(S^2 + \frac{(K-3)^2}{4}\right) \;\sim\; \chi^2_2$$

A normal distribution has $S=0$ and $K=3$ (excess kurtosis 0), so $JB$ measures departure from both. In R: `jarque.bera.test(x)`.

> [!note] Excel reports *excess* kurtosis
> Excel's `KURT` and the slide-21 output give **excess** kurtosis ($K - 3$), so a normal distribution reads 0, not 3. Use $\frac{n}{6}(S^2 + \frac{K_{excess}^2}{4})$ when working from Excel output.

χ² goodness-of-fit can also test normality, by binning the data and comparing observed counts with normal expected counts. Two parameters ($\mu$, $\sigma$) are estimated, so $df = k - 3$.

### Correlation test

Tests whether a population correlation differs from zero:

$$H_0: \rho = 0 \qquad t = \frac{r\sqrt{n-2}}{\sqrt{1-r^2}} \sim t_{n-2}$$

This tests the **linear** correlation of [[03 - Descriptive Statistics]]. Its non-parametric counterpart, Spearman's rank correlation, applies the same formula to ranks and detects any monotonic relationship.

## ✏️ Exercises

**1.** *(Example 9.1)* A report claims quality levels A, B, C, D occur in proportions 10%, 20%, 30%, 40%. A sample of 400 products gives 50, 60, 125, 165.
> (a) At 5%, is there enough evidence to say the report is inappropriate? (b) At 2.5%? (c) Find the p-value.

> [!example]- Solution
> $H_0$: proportions are 0.1, 0.2, 0.3, 0.4. $H_1$: at least one differs.
>
> | Level | $O_i$ | $p_i$ | $E_i = 400p_i$ | $(O_i-E_i)^2/E_i$ |
> |---|---|---|---|---|
> | A | 50 | 0.1 | 40 | $100/40 = 2.500$ |
> | B | 60 | 0.2 | 80 | $400/80 = 5.000$ |
> | C | 125 | 0.3 | 120 | $25/120 = 0.208$ |
> | D | 165 | 0.4 | 160 | $25/160 = 0.156$ |
> | **Sum** | **400** | **1** | **400** | **7.865** |
>
> $$\chi^2 = 7.865, \qquad df = k - 1 = 3$$
> (Nothing was estimated — the proportions were given by the report.)
>
> **(a) At 5%:** $\chi^2_{0.05,3} = 7.815$. Since $7.865 > 7.815$ → **reject $H_0$**. There is (just) enough evidence that the report is inappropriate.
>
> **(b) At 2.5%:** $\chi^2_{0.025,3} = 9.348$. Since $7.865 < 9.348$ → **do not reject**. Not enough evidence.
>
> **(c) p-value.** R gives `X-squared = 7.8646, df = 3, p-value = 0.04889`. Excel: `=CHITEST(observed, expected)`.
>
> ```r
> quality <- c(50, 60, 125, 165)
> chisq.test(quality, p = c(0.1, 0.2, 0.3, 0.4))
> ```
>
> **The result is borderline** — $p = 0.0489$ clears 0.05 by 0.0011. The rejection at 5% is real but fragile, and reporting "significant" without the p-value would badly overstate it. The same lesson as Example 7.6 in [[07 - Hypothesis Testing - One Sample]].
>
> Inspecting the contributions shows *where* the misfit is: **B contributes 5.00 of the 7.86**, with 60 observed against 80 expected. C and D fit almost perfectly. So the report's error is concentrated in the B proportion — a diagnostic the single statistic hides.

**2.** *(Example 9.2)* Test at 5% that customer numbers are uniform across the week.
> Mon 290, Tue 250, Wed 238, Thu 257, Fri 265, Sat 230, Sun 192.

> [!example]- Solution
> $H_0$: customers are uniformly distributed (equal proportion each day), i.e. $p_i = 1/7$ for all $i$.
>
> $n = 290+250+238+257+265+230+192 = 1722$, so $E_i = 1722/7 = 246$ for every day.
>
> | Day | $O_i$ | $E_i$ | $O_i - E_i$ | $(O_i-E_i)^2/E_i$ |
> |---|---|---|---|---|
> | Mon | 290 | 246 | +44 | 7.870 |
> | Tue | 250 | 246 | +4 | 0.065 |
> | Wed | 238 | 246 | −8 | 0.260 |
> | Thu | 257 | 246 | +11 | 0.492 |
> | Fri | 265 | 246 | +19 | 1.468 |
> | Sat | 230 | 246 | −16 | 1.041 |
> | Sun | 192 | 246 | −54 | 11.854 |
> | | | | | **23.05** |
>
> $$\chi^2 = 23.05, \qquad df = 7 - 1 = 6$$
>
> $\chi^2_{0.05,6} = 12.592$. Since $23.05 \gg 12.592$ → **reject $H_0$** decisively ($p \approx 0.0008$).
>
> Customer numbers are **not** uniform across the week.
>
> ```r
> customers <- c(290, 250, 238, 257, 265, 230, 192)
> chisq.test(customers)     # equal probabilities is the default
> ```
>
> As in Exercise 1, the contributions localise the effect: **Sunday (11.85) and Monday (7.87) supply 19.7 of the 23.05**. Sunday is far quieter and Monday far busier than uniform; Tuesday through Saturday fit well. A manager should read this as "staff Mondays more heavily and Sundays less", which is far more actionable than "reject uniformity."
>
> Note $E_i = 246 \ge 5$ comfortably, so the χ² approximation is sound.

**3.** *(Example 9.3)* Forgotten luggage $X$ on trains. Test at 5% that $X$ is Poisson (a) with mean 3, and (b) Poisson with the mean estimated.

| $X$ | 0 | 1 | 2 | 3 | 4 | 5 | ≥6 |
|---|---|---|---|---|---|---|---|
| Freq | 30 | 50 | 70 | 65 | 45 | 25 | 15 |
| Prob | .050 | .149 | .224 | .224 | .168 | .101 | — |


> [!example]- Solution
> $n = 30+50+70+65+45+25+15 = 300$. The tabulated probabilities are Poisson(3), and the tail $P(X\ge 6) = 1 - 0.916 = 0.084$.
>
> **(a) Poisson with mean 3 — fully specified.**
>
> | $X$ | $O_i$ | $p_i$ | $E_i = 300p_i$ | $(O_i-E_i)^2/E_i$ |
> |---|---|---|---|---|
> | 0 | 30 | .050 | 15.0 | 15.000 |
> | 1 | 50 | .149 | 44.7 | 0.628 |
> | 2 | 70 | .224 | 67.2 | 0.117 |
> | 3 | 65 | .224 | 67.2 | 0.072 |
> | 4 | 45 | .168 | 50.4 | 0.579 |
> | 5 | 25 | .101 | 30.3 | 0.927 |
> | ≥6 | 15 | .084 | 25.2 | 4.129 |
> | | **300** | | **300** | **21.45** |
>
> $$\chi^2 = 21.45, \qquad df = k - 1 = 6$$
> $\chi^2_{0.05,6} = 12.592$. Since $21.45 > 12.592$ → **reject**. $X$ is not Poisson(3). ($p \approx 0.0015$)
>
> The $X=0$ cell alone contributes 15.0 — twice as many zero-luggage trains as Poisson(3) predicts.
>
> **(b) Poisson with $\lambda$ estimated.** Estimate from the data:
> $$\hat\lambda = \bar{x} = \frac{0(30)+1(50)+2(70)+3(65)+4(45)+5(25)+6(15)}{300} = \frac{780}{300} = 2.6$$
> *(treating the ≥6 class as 6, which slightly understates $\hat\lambda$).*
>
> Recompute $E_i$ from Poisson(2.6) and, critically, **lose one more degree of freedom**:
> $$df = k - 1 - m = 7 - 1 - 1 = 5$$
> with critical value $\chi^2_{0.05,5} = 11.070$.
>
> **The point of comparing (a) and (b):** fitting $\lambda$ to the data guarantees a better match, so $\chi^2$ falls — but the critical value falls too, precisely to offset the advantage. **You cannot buy significance by fitting more parameters**; the degrees-of-freedom penalty is the accounting that prevents it.
>
> Even so, the excess of zeros suggests neither Poisson fits: with far more zeros than a Poisson allows, this looks like **zero-inflation** — many trains simply have no luggage left behind, a separate mechanism from the count process.

**4.** *(Example 9.4)* Test at 5% that a government office's "saying" and "doing" are independent.

|Within 1 day | 2–3 days | > 3 days |
|---|---|---|---|
| **Within 1 day** | 65 | 35 | 55 |
| **2–3 days** | 70 | 30 | 70 |
| **> 3 days** | 25 | 10 | 40 |

> [!example]- Solution
> $H_0$: saying and doing are independent. $H_1$: they are dependent.
>
> **Observed with margins:**
>
> | $O_{ij}$ | S1 | S2 | S3 | **Row** |
> |---|---|---|---|---|
> | D1 | 65 | 35 | 55 | **155** |
> | D2 | 70 | 30 | 70 | **170** |
> | D3 | 25 | 10 | 40 | **75** |
> | **Col** | **160** | **75** | **165** | **400** |
>
> **Expected** via $E_{ij} = R_i C_j / n$:
>
> | $E_{ij}$ | S1 | S2 | S3 |
> |---|---|---|---|
> | D1 | $\frac{155(160)}{400}=62.00$ | $\frac{155(75)}{400}=29.06$ | $\frac{155(165)}{400}=63.94$ |
> | D2 | $\frac{170(160)}{400}=68.00$ | $\frac{170(75)}{400}=31.88$ | $\frac{170(165)}{400}=70.13$ |
> | D3 | $\frac{75(160)}{400}=30.00$ | $\frac{75(75)}{400}=14.06$ | $\frac{75(165)}{400}=30.94$ |
>
> Check: rows and columns of $E$ reproduce the same margins as $O$. ✓
>
> $$\chi^2 = \frac{(65-62)^2}{62} + \frac{(35-29.06)^2}{29.06} + \cdots = 7.4385$$
>
> $$df = (3-1)(3-1) = 4$$
>
> $\chi^2_{0.05,4} = 9.488$. Since $7.4385 < 9.488$ → **do not reject $H_0$**. At 5% there is insufficient evidence that saying and doing are dependent.
>
> R confirms: `X-squared = 7.4385, df = 4, p-value = 0.1145`.
>
> ```r
> D1 <- c(65,35,55); D2 <- c(70,30,70); D3 <- c(25,10,40)
> table2 <- rbind(D1, D2, D3)
> colnames(table2) <- c("S1","S2","S3")
> chisq.test(table2)
> ```
>
> **Two cautions on interpretation.** First, "do not reject" is **not** proof of independence — see [[07 - Hypothesis Testing - One Sample]]. With $p = 0.11$ there is a hint of association that this sample size cannot resolve.
>
> Second, χ² detects **any** departure from independence but says nothing about **direction or strength**. For that, inspect the standardised residuals $(O-E)/\sqrt{E}$, or compute Cramér's V.
>
> **Note the R code on slide 17 is subtly wrong.** `matrix(c(65,35,55,70,30,70,25,10,40), 3, 3)` fills **column-wise**, producing the *transpose* of the intended table — as the printed output shows (row 1 reads 65, 70, 25). It happens to give the same $\chi^2$ here, since transposing leaves the statistic unchanged, but the table displayed is not the one intended. Slide 18's `rbind` version is correct and is the one to use.

**5.** (Advanced) Explain when non-parametric tests should be preferred, what they cost, and — using the slide-21 output — test the customer ages for normality.

> [!example]- Solution
> **When to prefer non-parametric tests:**
> - The **normality assumption fails** and $n$ is too small for the CLT to rescue you.
> - The data are **ordinal**, where means are undefined ([[01 - Introduction to Statistics]]).
> - There are **outliers** — rank-based tests are far more robust, since one extreme value changes a rank by at most a position but can move a mean arbitrarily.
> - The hypothesis is about a **distribution's shape** rather than a parameter — exactly the goodness-of-fit case.
>
> **What they cost:**
> - **Less power when parametric assumptions do hold.** The Wilcoxon signed-rank test has ~95% of the $t$-test's efficiency under normality — so on genuinely normal data you need ~5% more observations for the same power. A modest price.
> - **Weaker conclusions.** χ² tells you variables are dependent, not how or how strongly.
> - **Discarded information.** Rank-based tests use ordering only; the *magnitudes* of differences are thrown away.
> - **Different hypotheses.** The Wilcoxon test is about medians/distributions, not means — so it does not answer the same question the $t$-test does.
>
> **Testing the customer ages for normality (slide 21):** $n = 100$, skewness $S = 0.525$, and Excel's kurtosis $= 0.0664$, which is **excess** kurtosis.
>
> $$JB = \frac{n}{6}\left(S^2 + \frac{K_{excess}^2}{4}\right) = \frac{100}{6}\left(0.525^2 + \frac{0.0664^2}{4}\right)$$
> $$= 16.667\,(0.2756 + 0.0011) = 16.667 \times 0.2767 = \mathbf{4.612}$$
>
> Compare with $\chi^2_{0.05,2} = 5.991$. Since $4.612 < 5.991$ → **do not reject normality at 5%** ($p \approx 0.0997$).
>
> The evidence is marginal, though: the departure comes almost entirely from **skewness** (0.525, a moderate right skew), while kurtosis is essentially normal. The descriptive statistics agree — mean 43.08 > median 42 > mode 46 is not a clean ordering, but mean above median is the right-skew signature from [[03 - Descriptive Statistics]], and the maximum of 78 sits 2.8 standard deviations above the mean against a minimum only 1.9 below.
>
> **A caution about normality tests generally:** they are **underpowered at small $n$** (they fail to reject almost anything) and **oversensitive at large $n$** (they reject trivial, harmless departures). At $n = 100$ we are in a reasonable middle range, but a QQ plot ([[03 - Descriptive Statistics]]) is usually more informative than the test — it shows *where* and *how* the distribution departs, not merely whether some test crossed a threshold.

## 📝 Summary

- **Non-parametric tests make no distributional assumption**, so they apply when normality fails, data are ordinal, or outliers are present.
- **χ² goodness-of-fit:** $\chi^2 = \sum\frac{(O_i-E_i)^2}{E_i}$ with $E_i = np_i$, always **right-tailed**.
- **$df = k - 1 - m$**, where $m$ is the number of parameters estimated from the data.
- **χ² test of independence:** $E_{ij} = \frac{R_i C_j}{n}$, $df = (h-1)(k-1)$.
- **Require $E_i \ge 5$ in every cell**; merge sparse categories otherwise.
- **Inspect individual cell contributions** — they show *where* the misfit is, which the total hides.
- **Jarque–Bera** tests normality via skewness and kurtosis, $JB \sim \chi^2_2$. Excel reports **excess** kurtosis.
- **Correlation test:** $t = \frac{r\sqrt{n-2}}{\sqrt{1-r^2}}$ on $n-2$ df.
- **The cost of non-parametric methods** is lower power under normality (~95% efficiency) and weaker conclusions.

## ⚠️ Important Notes

**Every estimated parameter costs a degree of freedom.** Poisson with a given mean → $df = k-1$; with $\lambda$ estimated → $df = k-2$; normality with $\mu,\sigma$ estimated → $df = k-3$. Forgetting this inflates significance.

**χ² tests are always right-tailed.** A small statistic means good fit, never "significantly good fit".

**$E_i \ge 5$ is required in every cell.** Small expected counts make the χ² approximation unreliable — merge categories or use an exact test.

**Expected frequencies need not be integers.** $E = 29.06$ is correct; do not round.

**χ² tells you *that* variables are dependent, not *how*.** Inspect standardised residuals $(O-E)/\sqrt{E}$, or compute Cramér's V for strength.

**Independence tests do not establish causation** — and non-rejection does not establish independence.

**Excel's `KURT` returns excess kurtosis** ($K-3$), so a normal distribution reads 0. Jarque–Bera formulas written with $(K-3)$ expect the raw kurtosis; do not subtract 3 twice.

**Normality tests are underpowered at small $n$ and oversensitive at large $n$.** At $n = 10{,}000$ they reject harmless departures; at $n = 15$ they accept almost anything. Prefer a QQ plot.

**R's `matrix()` fills column-wise by default.** Slide 17's code builds the transpose of the intended table. Use `rbind` (slide 18) or pass `byrow = TRUE`.

**χ² for independence needs a table of *counts*, not percentages.** Feeding row-percentages in produces a meaningless statistic — the test's power depends on $n$, which percentages have discarded.

**Borderline results deserve their p-value.** Example 9.1's $p = 0.0489$ clears 5% by 0.0011; "significant" alone is a misleading summary.

> [!warning] Gaps in the source slides
> Formulas are images. **Titles only** on slides 2, 4, 10 (partial), 12–14, 20, 23, 25 — specifically the goodness-of-fit definition, **the χ² statistic itself**, the expected-frequency derivation, the independence test statistic, **the normality test (Jarque–Bera formula)**, and the **correlation test statistic**. All are reconstructed above from standard sources.
> - **Slide 25 ("Summary") is an image** — the lecturer's own summary is not captured.
> - **Slide 22** — "Test for Normality, using following sample ... using Jarque-Bera and Chi-squared test" — **the sample data is an image**, so the exercise cannot be completed.
> - **Slide 9 (Example 9.3)** gives no probability for the `≥6` class; I computed $0.084$ as the Poisson(3) tail complement.
> - **Example 9.5** (customer age × satisfaction, slide 19) and **Example 9.6** (correlation of Q, P, Z, slide 24) have **full data tables but no worked solutions**. Both are straightforward applications of the methods above — good extra practice.
> - **Slide 21's Wilcoxon test** is listed in the lecture's contents (slide 1) but **no slide covers it**. The deck ends at the correlation test. **Wilcoxon signed-rank and rank-sum are therefore missing entirely from the provided material** — worth raising with the lecturer, since slide 1 promises them.
>
> **All example data tables and R outputs extracted intact.**
>
> **Exercises set:** [1] Ch. 13 (p. 730) 2, 3, 4, 5, 9.

---
**Previous:** [[08 - Inferences on Two Samples]] · **Back to** [[00-Index]]
