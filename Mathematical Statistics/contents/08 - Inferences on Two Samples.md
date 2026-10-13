---
subject: Mathematical Statistics
chapter: 08
tags: [ds, statistics, hypothesis-testing, t-test, f-test, paired-samples]
source: "MS_Lec08_2samples.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Inferences on Two Samples

Reading: Devore & Berk ch. 10. [[07 - Hypothesis Testing - One Sample]] compared one population with a fixed number; this chapter compares two populations with each other.

> [!warning] Source note
> Formulas are images, but every example's data, Excel output and R output extracted, so the numbers below are the lecturer's own results.

## 📘 Main Knowledge

### Paired or independent?

Decide this first; the wrong choice invalidates the analysis.

**Paired** samples: the same unit measured twice (slide 3, "Effective advertising policy?"):

| Store | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Before | 72 | 75 | 70 | 82 | 70 | 83 |
| After | 76 | 79 | 77 | 80 | 75 | 89 |

**Independent** samples: two separate groups, possibly of different sizes ("On average, are Sales of A and B different?"). Firm A: 77, 79, 76, 80, 82, 83. Firm B: 97, 86, 85, 93, 81, 72, 88, 90, 82.

Test: can each observation in sample 1 be matched with exactly one in sample 2 by a meaningful correspondence (same subject, before/after, matched twins)? Unequal sizes rule out pairing.

### Decision map (slides 5 and 33)

```
Paired?
├── yes → differences dᵢ → one-sample t-test on d
└── no  → σ known / large n → z-test
          σ unknown → equal variances? (F-test)
                      ├── yes → pooled t-test
                      └── no  → Welch t-test
```

### Paired samples

Compute $d_i=x_{2i}-x_{1i}$ and run the one-sample $t$-test on the differences:
$$t=\frac{\bar d-\mu_{d0}}{s_d/\sqrt n}\sim t_{n-1},\qquad \text{CI: }\bar d\pm t_{\alpha/2,\,n-1}\frac{s_d}{\sqrt n}$$

Pairing removes between-unit variation. Since
$$\operatorname{Var}(\bar X_2-\bar X_1)=\frac{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}{n},$$
positive correlation shrinks the variance. In Example 8.1 the columns have variances 34.3 and 25.9 but the differences only 10, because the correlation is 0.842.

### Independent samples, equal variances (pooled)

$$s_p^2=\frac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2},\qquad t=\frac{(\bar x_1-\bar x_2)-\delta_0}{s_p\sqrt{\frac1{n_1}+\frac1{n_2}}}\sim t_{n_1+n_2-2}$$
$s_p^2$ is the df-weighted average of the two sample variances.

### Independent samples, unequal variances (Welch)

$$t=\frac{(\bar x_1-\bar x_2)-\delta_0}{\sqrt{\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}}},\qquad df=\frac{\left(\frac{s_1^2}{n_1}+\frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1-1}+\frac{(s_2^2/n_2)^2}{n_2-1}}$$
The Welch–Satterthwaite df is usually not an integer and is at most $n_1+n_2-2$.

### F-test for equal variances

Slide 25: "How to know which assumption is correct?"
$$F=\frac{s_1^2}{s_2^2}\sim F_{n_1-1,\,n_2-1}\quad\text{under }H_0:\sigma_1^2=\sigma_2^2$$
The Fisher–Snedecor $F$ is a ratio of independent scaled χ² variables: on $[0,\infty)$, right-skewed, with numerator and denominator df. CI for the ratio:
$$\left(\frac{s_1^2}{s_2^2}\cdot\frac1{F_{\alpha/2,\,n_1-1,\,n_2-1}},\ \frac{s_1^2}{s_2^2}\cdot F_{\alpha/2,\,n_2-1,\,n_1-1}\right)$$

### Two proportions

$$Z=\frac{\hat p_1-\hat p_2}{\sqrt{\bar p(1-\bar p)\left(\frac1{n_1}+\frac1{n_2}\right)}},\qquad \bar p=\frac{x_1+x_2}{n_1+n_2}$$
Under $H_0:p_1=p_2$ there is one common proportion, so the test pools. The CI has no such null and does not pool:
$$(\hat p_1-\hat p_2)\pm z_{\alpha/2}\sqrt{\frac{\hat p_1(1-\hat p_1)}{n_1}+\frac{\hat p_2(1-\hat p_2)}{n_2}}$$

## ✏️ Exercises

Exercises 1–4 are the lecturer's examples.

**1.** (Example 8.1) The six stores above, normal sales. (a) Test for an increase in mean sales. (b) 95% CI for the increase. (c) Test that the increase equals 3.

> [!example]- Solution
> $d = 4, 4, 7, -2, 5, 6$; $\bar d=4$, $s_d^2=50/5=10$, $s_d=3.162$, $SE=1.291$, df 5.
> (a) $H_1:\mu_d>0$. $t=4/1.291=3.098>t_{0.05,5}=2.015$: reject. R: `t = 3.0984, df = 5, p-value = 0.01345`. Excel shows `t Stat = -3.098` because it subtracted After from Before.
> (b) $4\pm2.571(1.291)=(0.68,\ 7.32)$. R's one-sided interval `(1.398584, Inf)` matches (a)'s alternative.
> (c) $t=1/1.291=0.775<2.571$: don't reject ($p=0.47$). Consistent with (b): 3 is inside the CI.

**2.** (Examples 8.3, 8.4) Firms A and B above. Test whether mean sales differ under each variance assumption.

> [!example]- Solution
> $\bar x_A=79.5$, $s_A^2=7.5$, $n_A=6$; $\bar x_B=86$, $s_B^2=53.5$, $n_B=9$.
>
> Pooled: $s_p^2=(37.5+428)/13=35.808$, $SE=\sqrt{35.808(1/6+1/9)}=3.154$, $t=-6.5/3.154=-2.061$. df 13, $t_{0.025,13}=2.160$: don't reject, $p=0.060$. CI $(-13.31,\ 0.31)$ contains 0.
>
> Welch: $SE=\sqrt{1.25+5.944}=2.682$, $t=-2.423$, df 10.94 (Excel rounds to 11), $t_{0.025}=2.202$: reject, $p=0.034$. CI $(-12.41,\ -0.59)$ excludes 0.
>
> Same data, different verdicts at 5%. The variances differ by a factor of 7 and the smaller sample has the smaller variance, which is where the pooled test is least reliable.

**3.** (Example 8.5) Use an F-test to choose between the tests in Exercise 2. What problem does this create?

> [!example]- Solution
> $F=7.5/53.5=0.1402$, df (5, 8). R: `F = 0.14019, num df = 5, denom df = 8, p-value = 0.04457`. Reject equal variances, so use Welch: the means differ ($p=0.034$). The 95% CI for the variance ratio, $(0.029,\ 0.947)$, excludes 1.
>
> Slide 32 lines up the three p-values: F-test 0.044, pooled 0.060, Welch 0.034. The conclusion hinges on a borderline preliminary test; with $p_F=0.055$ we would have concluded no difference. Choosing a test based on an earlier test also distorts the overall Type 1 rate. Common practice is to use Welch by default (R's `t.test()` has `var.equal = FALSE`): it loses little power when variances are equal and is safer when they are not. The F-test is also more sensitive to non-normality than the t-tests it gates.

**4.** (Example 8.6) 140 of 200 men and 152 of 300 women are satisfied. (a) Test at 5% that men are more satisfied; p-value. (b) 90% CI for the difference.

> [!example]- Solution
> $\hat p_M=0.70$, $\hat p_F=0.5067$, difference 0.1933. All counts (140, 60, 152, 148) exceed 5.
> (a) Pool: $\bar p=292/500=0.584$, $SE=\sqrt{0.584(0.416)(1/200+1/300)}=0.04499$, $z=4.297>1.645$: reject; $p=8.7\times10^{-6}$.
> (b) Unpooled $SE=\sqrt{0.00105+0.000833}=0.04340$: $0.1933\pm1.645(0.0434)=(0.122,\ 0.265)$. Excludes 0.
> The SEs differ because the test assumes one common $p$ and the CI does not.

**5.** (Advanced) Analyse Example 8.1's data as if the samples were independent. What goes wrong, and what about the reverse mistake?

> [!example]- Solution
> Before: mean 75.333, $s^2=34.267$; after: mean 79.333, $s^2=25.867$. $s_p^2=30.067$, $SE=\sqrt{30.067/3}=3.166$, $t=1.263$ on df 10. One-sided $p=0.118$ ($t_{0.05,10}=1.812$): not significant, against the paired $p=0.013$.
>
> The unpaired test treats store-to-store differences (70 to 83 before) as noise, inflating the SE from 1.29 to 3.17. The paired test removes them, using the $-2\rho\sigma_1\sigma_2$ term with $\rho=0.842$. Pairing costs df (5 instead of 10), so it pays only when $\rho>0$.
>
> The reverse mistake, pairing independent samples, produces meaningless differences and an invalid Type 1 rate. Ignoring pairing costs power; false pairing costs validity. The study design decides the test, not the p-value.

## 📝 Summary

- First ask: paired or independent? Unequal $n$ means independent.
- Paired: one-sample $t$ on the differences, df $n-1$; removes between-unit variation.
- Independent, equal variances: pooled $s_p^2$, df $n_1+n_2-2$.
- Independent, unequal variances: Welch with Satterthwaite df.
- F-test $s_1^2/s_2^2$ on $(n_1-1,n_2-1)$ df; Welch by default avoids it.
- Two proportions: the test pools, the CI does not.
- Each test has a matching CI that agrees with it.

## ⚠️ Important Notes

1. Paired data analysed as independent loses power (Example 8.1: $p=0.013$ vs $0.118$).
2. Independent data analysed as paired is invalid.
3. Choose the design and test before seeing the data.
4. Pooled and Welch can disagree ($p=0.060$ vs $0.034$).
5. Excel's Data Analysis tool makes you choose; pick "Unequal Variances" unless there is a strong reason not to.
6. An F-test followed by a t-test is a two-stage procedure; the nominal 5% no longer holds.
7. The F-test is sensitive to non-normality.
8. Welch df is non-integer; by hand, round down.
9. Excel's sign depends on column order; the p-value doesn't.
10. F critical values are not symmetric: $F_{1-\alpha,d_1,d_2}=1/F_{\alpha,d_2,d_1}$.
11. Non-significance is not equality: the pooled CI $(-13.31,\ 0.31)$ allows B to be up to 13 higher.

> [!warning] Gaps in the source slides
> - Slides 4, 6–8, 12–13, 15–16, 20–21, 26–28 and 34–35 have titles only: the paired formulas, both independent $t$ formulas, pooled variance, Welch df, F statistic and density, variance-ratio CI and the two-proportion formulas. All are standard reconstructions.
> - Example 8.2 (slide 14) is lost.
> - Slide 33's flowchart extracted only as fragments (`Pair sample? / z-Test / Yes / No`); the map above is rebuilt from those and slide 5.
> - Data discrepancy: slide 3 lists Firm B's sixth and seventh values as 75 and 87; Examples 8.3–8.5 (slides 17, 22, 29) use 72 and 88, and the Excel/R outputs (variance 53.5) match the later version, which is used here.
> - Exercise set: [1] ch. 10 (p. 495) 1, 2, 4–7, 11, 17; (p. 505) 21, 25, 26, 36, 37; (p. 517) 39, 42, 44; (p. 525) 48, 50, 55, 57, 59; (p. 531) 61, 62, 64, 65, 68; (p. 545) 85, 86, 90–92.

**Previous:** [[07 - Hypothesis Testing - One Sample]] · **Next:** [[09 - Non-parametric Testing]]
