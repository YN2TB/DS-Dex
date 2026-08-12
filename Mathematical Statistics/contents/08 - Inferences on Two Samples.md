---
subject: Mathematical Statistics
chapter: 08
tags: [ds, statistics, hypothesis-testing, t-test, f-test, paired-samples]
source: "MS_Lec08_2samples.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Inferences on Two Samples

> [!note] Reading
> **[1] Devore & Berk, Ch. 10**
>
> [[07 - Hypothesis Testing - One Sample]] compared one population to a fixed number. This chapter compares **two populations to each other** — the commonest question in applied work ("did the treatment help?", "is A better than B?").

> [!warning] Source note
> Formulas are equation images, but **every worked example's data, Excel output, and R output extracted in full**. That makes this the best-supported lecture in the subject: the numbers below are the lecturer's actual results, not reconstructions.

## 📘 Main Knowledge

### The first question: paired or independent?

**Everything depends on this.** Choosing wrong invalidates the analysis.

**Paired (dependent) samples** — the *same* unit measured twice, so observations come in matched couples:

| Store | Before | After |
|---|---|---|
| 1 | 72 | 76 |
| 2 | 75 | 79 |
| 3 | 70 | 77 |
| 4 | 82 | 80 |
| 5 | 70 | 75 |
| 6 | 83 | 89 |

*Question: "Effective advertising policy?"* — each store is its own control.

**Independent samples** — two *separate* groups, possibly of different sizes:

| Firm A | Firm B |
|---|---|
| 77 | 95 |
| 79 | 86 |
| 76 | 85 |
| 80 | 93 |
| 82 | 81 |
| 83 | 75 |
| | 87, 88, 84 |

*Question: "On average, are Sales of A and B different?"*

The test: **can you pair each observation in sample 1 with exactly one in sample 2 by a meaningful correspondence?** If yes — same subject, matched twins, before/after — it is paired. Unequal sample sizes make pairing impossible, so those are always independent.

### The decision structure

Slide 5 and the slide-33 flowchart give the full map:

```
Pair sample?
├── YES → work with differences dᵢ → one-sample t-test on d
└── NO  → σ known / large n?  → z-test
          └── σ unknown → equal variances?  (test with F-test)
                          ├── YES → pooled t-test
                          └── NO  → Welch t-test
```

### Paired samples

Reduce two samples to **one**: compute $d_i = x_{2i} - x_{1i}$ and apply the one-sample $t$-test from [[07 - Hypothesis Testing - One Sample]] to the differences.

$$t = \frac{\bar{d} - \mu_{d0}}{s_d/\sqrt{n}} \sim t_{n-1}$$

**Confidence interval for the mean difference:**
$$\bar{d} \pm t_{\alpha/2,\,n-1}\frac{s_d}{\sqrt{n}}$$

> [!tip] Why pairing is more powerful
> Pairing **eliminates between-unit variation**. Store 6 sells more than store 5 in both periods; that difference is irrelevant to whether advertising worked, and subtracting removes it entirely. What remains is the effect of interest plus noise.
>
> The gain is visible in Example 8.1: the two samples have variances of 34.3 and 25.9, but the *differences* have a much smaller variance — because the two columns correlate at **0.842**. The stronger the pairing, the greater the advantage.

### Independent samples — equal variances (pooled $t$-test)

Assuming $\sigma_1^2 = \sigma_2^2$, pool the two variances:

$$s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}$$

$$t = \frac{(\bar{x}_1 - \bar{x}_2) - \delta_0}{s_p\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}} \sim t_{n_1+n_2-2}$$

The pooled variance is a **weighted average** of the two sample variances, weighted by degrees of freedom.

### Independent samples — unequal variances (Welch's $t$-test)

$$t = \frac{(\bar{x}_1 - \bar{x}_2) - \delta_0}{\sqrt{\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}}}$$

with the **Welch–Satterthwaite** degrees of freedom:

$$df = \frac{\left(\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1-1}+\frac{(s_2^2/n_2)^2}{n_2-1}}$$

— generally **not an integer**, and always smaller than $n_1+n_2-2$.

### The F-test for equal variances

Slide 25 asks the natural question: *"How to know which assumption is correct?"*

$$F = \frac{s_1^2}{s_2^2} \sim F_{n_1-1,\,n_2-1} \quad\text{under } H_0: \sigma_1^2 = \sigma_2^2$$

The **Fisher–Snedecor** $F$ distribution is the ratio of two independent scaled chi-squareds. It is defined on $[0,\infty)$, **right-skewed**, and has **two** degrees-of-freedom parameters (numerator and denominator, in that order).

**CI for the ratio of variances:**
$$\left(\frac{s_1^2}{s_2^2}\cdot\frac{1}{F_{\alpha/2,\,n_1-1,n_2-1}},\;\; \frac{s_1^2}{s_2^2}\cdot F_{\alpha/2,\,n_2-1,n_1-1}\right)$$

### Two proportions

$$Z = \frac{(\hat{p}_1 - \hat{p}_2)}{\sqrt{\bar{p}(1-\bar{p})\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}}, \qquad \bar{p} = \frac{x_1+x_2}{n_1+n_2}$$

Under $H_0: p_1 = p_2$ there is one common proportion, best estimated by **pooling** both samples. **The confidence interval, having no such null, does not pool:**

$$(\hat{p}_1 - \hat{p}_2) \pm z_{\alpha/2}\sqrt{\frac{\hat p_1(1-\hat p_1)}{n_1}+\frac{\hat p_2(1-\hat p_2)}{n_2}}$$

The same test-vs-interval asymmetry as the one-sample proportion in [[07 - Hypothesis Testing - One Sample]].

## ✏️ Exercises

**1.** *(Example 8.1)* Six stores' sales before and after an advertising campaign. Assume normality.
> (a) Test for an increase in mean sales. (b) Estimate the increase. (c) Test that the increase equals 3 units.

> [!example]- Solution
> **Compute the differences $d_i = \text{After} - \text{Before}$:**
>
> | Store | Before | After | $d_i$ |
> |---|---|---|---|
> | 1 | 72 | 76 | +4 |
> | 2 | 75 | 79 | +4 |
> | 3 | 70 | 77 | +7 |
> | 4 | 82 | 80 | **−2** |
> | 5 | 70 | 75 | +5 |
> | 6 | 83 | 89 | +6 |
>
> $\bar{d} = 24/6 = 4$. Deviations: 0, 0, 3, −6, 1, 2 → $\sum d^2 = 50$, so $s_d^2 = 50/5 = 10$, $s_d = 3.162$.
> $$\operatorname{SE} = \frac{3.162}{\sqrt{6}} = 1.291$$
>
> **(a)** $H_0: \mu_d \le 0$ vs $H_1: \mu_d > 0$, $df = 5$:
> $$t = \frac{4 - 0}{1.291} = 3.098$$
> $t_{0.05,5} = 2.015$. Since $3.098 > 2.015$ → **reject $H_0$**; sales increased significantly.
>
> This matches the R output exactly: `t = 3.0984, df = 5, p-value = 0.01345`. Excel reports `t Stat = -3.098` — negative because Excel computed Before − After; the magnitude and p-value are identical.
>
> **(b) 95% CI for the increase.** $t_{0.025,5} = 2.571$:
> $$4 \pm 2.571(1.291) = 4 \pm 3.319 = \mathbf{(0.68,\; 7.32)}$$
> R's one-sided interval `(1.398584, Inf)` corresponds to part (a)'s alternative.
>
> **(c)** $H_0: \mu_d = 3$ vs $H_1: \mu_d \ne 3$:
> $$t = \frac{4-3}{1.291} = 0.775$$
> $\lvert 0.775 \rvert < 2.571$ → **do not reject**. The data are consistent with an increase of exactly 3.
>
> Note this agrees with (b): 3 lies inside (0.68, 7.32) — the test/CI equivalence from [[07 - Hypothesis Testing - One Sample]].
>
> **The value of pairing:** the raw variances are 34.3 and 25.9, but the differences have variance only 10. The Pearson correlation of 0.842 between columns is what pairing exploits — store-level differences are removed rather than treated as noise. An unpaired test on this data would likely fail to detect the effect. Note too that store 4 *declined*; paired testing handles that naturally.

**2.** *(Examples 8.3 and 8.4)* Firm A: 77, 79, 76, 80, 82, 83. Firm B: 97, 86, 85, 93, 81, 72, 88, 90, 82. Test whether the mean sales differ, under both variance assumptions.

> [!example]- Solution
> $n_A = 6$, $\bar{x}_A = 79.5$, $s_A^2 = 7.5$. $n_B = 9$, $\bar{x}_B = 86$, $s_B^2 = 53.5$. **Independent** samples — different sizes, no pairing possible.
>
> **Equal-variance (pooled) $t$-test:**
> $$s_p^2 = \frac{5(7.5) + 8(53.5)}{6+9-2} = \frac{37.5 + 428}{13} = \frac{465.5}{13} = 35.808$$
> $$t = \frac{79.5 - 86}{\sqrt{35.808\left(\frac16+\frac19\right)}} = \frac{-6.5}{\sqrt{35.808 \times 0.2778}} = \frac{-6.5}{3.154} = -2.061$$
> $df = 13$, $t_{0.025,13} = 2.160$. Since $\lvert-2.061\rvert < 2.160$ → **do not reject**. Two-tailed $p = 0.060$.
>
> **Welch (unequal variance) $t$-test:**
> $$t = \frac{-6.5}{\sqrt{\frac{7.5}{6}+\frac{53.5}{9}}} = \frac{-6.5}{\sqrt{1.25 + 5.944}} = \frac{-6.5}{2.682} = -2.423$$
> $df = 10.944$ (Welch–Satterthwaite; Excel rounds to 11), $t_{0.025} = 2.201$. Since $\lvert-2.423\rvert > 2.201$ → **reject $H_0$**. Two-tailed $p = 0.034$.
>
> **The two tests disagree at $\alpha = 0.05$ on identical data** — $p = 0.060$ vs $p = 0.034$. That is the entire point of the pair of examples, and it is why slide 25 asks "how to know which assumption is correct?"
>
> The 95% CIs tell the same story: pooled gives $(-13.31,\, 0.31)$, which **contains 0**; Welch gives $(-12.41,\, -0.59)$, which **excludes 0**. Consistent with each test's verdict.
>
> The variances differ by a factor of 7 ($7.5$ vs $53.5$), so the equal-variance assumption is doubtful — and the smaller sample has the smaller variance, the configuration in which the pooled test is least reliable. Exercise 3 settles it.

**3.** *(Example 8.5)* Use an F-test to decide which of the two tests in Exercise 2 is appropriate. Then discuss the problem this sequence creates.

> [!example]- Solution
> $H_0: \sigma_A^2 = \sigma_B^2$ vs $H_1: \sigma_A^2 \ne \sigma_B^2$.
> $$F = \frac{s_A^2}{s_B^2} = \frac{7.5}{53.5} = 0.1402$$
> with $df_1 = 5$, $df_2 = 8$. R reports `F = 0.14019, num df = 5, denom df = 8, p-value = 0.04457`.
>
> Since $p = 0.045 < 0.05$ → **reject equal variances**. Therefore **Welch's test (Example 8.4) is the appropriate one**, and the conclusion is that mean sales **do differ significantly** ($p = 0.034$).
>
> The 95% CI for the variance ratio, $(0.029,\, 0.947)$, **excludes 1**, agreeing with the test.
>
> **The problem this creates — and slide 32 lays it out deliberately:**
>
> | Test | p-value |
> |---|---|
> | F-test for equal variances | 0.044 |
> | t-test, equal variances | 0.060 |
> | t-test, unequal variances | 0.034 |
>
> **The final conclusion hinges on a preliminary test that is itself borderline.** Had the F-test given $p = 0.055$ we would have kept equal variances and concluded no difference in means. The whole analysis pivots on 0.011 of p-value in a preliminary step.
>
> This is a **two-stage testing** problem: conditioning the choice of test on a prior test distorts the overall Type 1 error rate, which is no longer the nominal 5%.
>
> **The modern recommendation is to skip the F-test and use Welch's t-test by default.** It is nearly as powerful as the pooled test when variances *are* equal, and much more reliable when they are not — so there is little to gain and real risk in testing first. R's `t.test()` reflects this: its default is `var.equal = FALSE`.
>
> A further caution: **the F-test is very sensitive to non-normality**, more so than the t-tests it is meant to protect. Using a fragile test to decide whether to use a robust one inverts the logic.

**4.** *(Example 8.6)* Of 200 male customers, 140 say "satisfied"; of 300 females, 152 do.
> (a) Test at 5% that males are more satisfied, and find the p-value. (b) Find the 90% CI for the difference in proportions.

> [!example]- Solution
> $\hat{p}_M = 140/200 = 0.70$, $\hat{p}_F = 152/300 = 0.5067$.
>
> **(a)** $H_0: p_M \le p_F$ vs $H_1: p_M > p_F$ (right-tailed). **Pool under $H_0$:**
> $$\bar{p} = \frac{140+152}{200+300} = \frac{292}{500} = 0.584$$
> $$\operatorname{SE} = \sqrt{0.584(0.416)\left(\frac{1}{200}+\frac{1}{300}\right)} = \sqrt{0.24294 \times 0.008333} = \sqrt{0.0020245} = 0.04499$$
> $$z = \frac{0.70 - 0.5067}{0.04499} = \frac{0.1933}{0.04499} = 4.297$$
>
> $z_{0.05} = 1.645$. Since $4.297 \gg 1.645$ → **reject $H_0$** decisively.
> $$p\text{-value} = P(Z > 4.297) \approx \mathbf{0.0000087}$$
> Overwhelming evidence that male customers are more satisfied.
>
> **(b) 90% CI — do NOT pool.** $z_{0.05} = 1.645$:
> $$\operatorname{SE} = \sqrt{\frac{0.70(0.30)}{200}+\frac{0.5067(0.4933)}{300}} = \sqrt{0.00105 + 0.000833} = \sqrt{0.001883} = 0.04340$$
> $$0.1933 \pm 1.645(0.04340) = 0.1933 \pm 0.0714 = \mathbf{(0.122,\; 0.265)}$$
> Males are between 12.2 and 26.5 percentage points more likely to be satisfied. **The interval excludes 0**, consistent with (a).
>
> **Why the standard errors differ (0.04499 vs 0.04340):** under $H_0$ the two proportions are *equal*, so all 500 observations estimate one common $p$ — pooling is both valid and more efficient. The confidence interval assumes no such equality, so each proportion is estimated from its own sample. Using the pooled SE in the interval, or the unpooled SE in the test, is a standard exam error.
>
> Validity holds throughout: all four counts (140, 60, 152, 148) exceed 5.

**5.** (Advanced) Explain why paired and independent tests are not interchangeable, and what goes wrong if you analyse paired data as independent.

> [!example]- Solution
> **Analysing paired data as independent throws away the pairing information and usually destroys the test's power.**
>
> Take Example 8.1's data. Treating the two columns as independent samples:
> - $\bar{x}_{before} = 75.333$, $s^2 = 34.267$; $\bar{x}_{after} = 79.333$, $s^2 = 25.867$; $n_1 = n_2 = 6$
> - Pooled: $s_p^2 = \frac{5(34.267)+5(25.867)}{10} = 30.067$
> - $t = \frac{-4}{\sqrt{30.067(1/6+1/6)}} = \frac{-4}{3.166} = -1.263$ on $df = 10$
>
> Against $t_{0.05,10} = 1.812$: **not significant** ($p \approx 0.118$).
>
> **The paired test gave $t = 3.098$, $p = 0.013$ — significant. Same data, opposite conclusions.**
>
> **Why.** The independent test attributes *all* variation to noise, including the large genuine differences between stores (70 to 83 in the Before column alone). That store-to-store spread inflates the denominator, drowning the consistent +4 effect.
>
> The paired test removes it by construction: $d_i$ contains only the change, so store 6 being a high performer cancels out entirely. Formally,
> $$\operatorname{Var}(\bar{X}_2 - \bar{X}_1) = \frac{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2}{n}$$
> and the $-2\rho\sigma_1\sigma_2$ term is what pairing exploits. Here $\rho = 0.842$, so the reduction is large. The independent test implicitly assumes $\rho = 0$ and forfeits it.
>
> **The reverse error is worse.** Falsely pairing genuinely independent samples produces meaningless differences and an **invalid** test — a Type 1 error rate that is no longer $\alpha$. The first error costs power (conservative); the second costs validity (anti-conservative).
>
> **Note the degrees of freedom trade-off:** paired gives $df = n-1 = 5$, independent gives $df = 2n-2 = 10$. Pairing *costs* degrees of freedom, so it is only worth it when $\rho > 0$ — which is nearly always true for repeated measures on the same unit, but is why pairing on an irrelevant variable is counterproductive.
>
> **Decide the design before collecting data.** The question "same units measured twice, or two separate groups?" is answered by the study design, never by whichever test gives a better p-value.

## 📝 Summary

- **First question always: paired or independent?** Same units measured twice → paired; separate groups → independent. Unequal $n$ ⇒ independent.
- **Paired:** compute $d_i$, then run a **one-sample** $t$-test on the differences, $df = n-1$.
- **Pairing removes between-unit variation** and is far more powerful when the two measurements correlate.
- **Independent, equal variances:** pooled $s_p^2$, $df = n_1+n_2-2$.
- **Independent, unequal variances:** Welch's $t$ with Satterthwaite $df$ (non-integer, smaller).
- **F-test** $F = s_1^2/s_2^2$ on $(n_1-1, n_2-1)$ df compares variances — but **prefer Welch by default** rather than testing first.
- **Two proportions:** the test **pools** ($\bar p$) because $H_0$ says they are equal; the **CI does not**.
- **Every test has a matching CI**, and they always agree.

## ⚠️ Important Notes

**Analysing paired data as independent usually destroys power** (Example 8.1: $p = 0.013$ paired vs $p = 0.118$ unpaired). Analysing independent data as paired is **invalid**, not merely inefficient.

**The design determines the test, not the p-value.** Decide before collecting data.

**Pooled and Welch tests can disagree** — Example 8.3/8.4 gives $p=0.060$ vs $p=0.034$ on identical numbers.

**Prefer Welch's t-test by default.** It is barely less powerful under equal variances and much safer otherwise. R's `t.test()` defaults to `var.equal = FALSE`; **Excel's Data Analysis Toolpak makes you choose**, so choose "Unequal Variances" unless you have strong reason not to.

**Two-stage testing distorts error rates.** Running an F-test and then selecting a t-test conditions the second test on the first, so the overall Type 1 rate is not the nominal 5%.

**The F-test is highly sensitive to non-normality** — more fragile than the t-tests it is supposed to protect. Using it as a gatekeeper inverts the robustness ordering.

**Welch degrees of freedom are usually non-integer** (10.944 here). Software handles it; by hand, round *down* to be conservative.

**Two-proportion test pools, two-proportion CI does not.** Under $H_0$ there is one common $p$; without a null there are two.

**Excel's sign depends on column order.** Example 8.1 shows `t Stat = -3.098` where R shows `+3.0984` — Excel subtracted the other way. Interpret the sign against your own $H_1$; the p-value is unaffected.

**F-test critical values are not symmetric.** $F_{\alpha,d_1,d_2} \ne F_{\alpha,d_2,d_1}$, and $F_{1-\alpha,d_1,d_2} = 1/F_{\alpha,d_2,d_1}$. Order the degrees of freedom carefully — many tables only list the upper tail.

**A non-significant result is not proof of equality.** Example 8.3's $p = 0.060$ does not show the firms' means are equal; the CI $(-13.31, 0.31)$ shows the data are consistent with anything from B being 13 higher to A being 0.3 higher — hardly evidence of no difference.

> [!warning] Gaps in the source slides
> Formulas are images; **slides 4, 6–8, 12–13, 15–16, 20–21, 26–28, 34–35 have titles only** — specifically the paired-sample test and interval formulas, both independent-sample $t$ formulas, the pooled variance and Welch df formulas, the F-test statistic, the Fisher–Snedecor density, the variance-ratio CI, and both two-proportion formulas.
> - **Example 8.2 (slide 14) is lost entirely** — title only, no data.
> - **Slide 33's decision flowchart** extracted only as fragments (`Pair sample? / z-Test / Yes / No`); I have reconstructed it above from the fragments plus slide 5.
> - **Slide 25's question** *"How to know which assumption is correct?"* extracted, which is what motivates the F-test.
>
> **All data tables, Excel outputs, and R outputs for Examples 8.1, 8.3, 8.4, 8.5, 8.6 extracted intact** — the numbers in this note are the lecturer's own.
>
> **A data discrepancy:** slide 3 lists Firm B's sixth value as **75** and its seventh as 87, while slides 17/22/29 (Examples 8.3–8.5) use **72** and 88. The Excel/R outputs match the *later* version (variance 53.5), so I have used 97, 86, 85, 93, 81, 72, 88, 90, 82. Slide 3's Firm A also ends 83 where the examples use the same values — only B differs. Check which your lecturer intends.
>
> **Exercises set:** [1] Ch. 10 (p. 495) 1, 2, 4–7, 11, 17; (p. 505) 21, 25, 26, 36, 37; (p. 517) 39, 42, 44; (p. 525) 48, 50, 55, 57, 59; (p. 531) 61, 62, 64, 65, 68; (p. 545) 85, 86, 90, 91, 92.

---
**Previous:** [[07 - Hypothesis Testing - One Sample]] · **Next:** [[09 - Non-parametric Testing]]
