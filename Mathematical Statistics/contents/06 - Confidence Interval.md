---
subject: Mathematical Statistics
chapter: 06
tags: [ds, statistics, confidence-interval, estimation, inference]
source: "MS_Lec06_Interval.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Confidence Intervals

Reading: Devore & Berk ch. 8; Miller & Miller, Interval Estimation, pp. 325–333. Adds uncertainty to the point estimates of [[05 - Point Estimation]] using the sampling distributions of [[04 - Sampling Distributions]].

> [!warning] Source note
> Formulas are images, but all four worked examples and all four R programs extracted; the examples are solved below.

## 📘 Main Knowledge

### The idea

$$\hat\theta \pm (\text{critical value})\times(\text{standard error})$$
The second term is the **margin of error (ME)**. At 95% each tail holds 2.5% (slide 6): level $1-\alpha$, $\alpha/2$ per tail.

**Meaning of 95% confidence**: not "$P(\mu\in\text{interval})=0.95$". $\mu$ is fixed; the interval is random. If the procedure were repeated many times, 95% of the intervals would contain $\mu$.

### Mean, σ known

$$\bar{x} \pm z_{\alpha/2}\frac{\sigma}{\sqrt{n}}$$

| Level | α | $z_{\alpha/2}$ |
|---|---|---|
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.96 |
| 99% | 0.01 | 2.576 |

One-sided bounds use $z_\alpha$: upper $\mu<\bar x+z_\alpha\sigma/\sqrt n$, lower $\mu>\bar x-z_\alpha\sigma/\sqrt n$ ($z_{0.10}=1.282$).

### Mean, σ unknown

$$\bar{x} \pm t_{\alpha/2,\,n-1}\frac{s}{\sqrt{n}}$$
Wider than the $z$ interval: the cost of estimating σ.

### Sample size

From $ME=z_{\alpha/2}\sigma/\sqrt n$:
$$n = \left(\frac{z_{\alpha/2}\,\sigma}{ME}\right)^{2}\quad\text{(round up)}$$
Halving ME needs four times the sample.

### Prediction interval

Covers one future observation $X_{n+1}$, not the mean:
$$\bar{x} \pm t_{\alpha/2,\,n-1}\, s\sqrt{1 + \frac{1}{n}}$$
The extra 1 is the individual's own variability, so a PI is always wider than the CI and does not shrink to zero as $n\to\infty$.

### Variance (normal population)

From $(n-1)s^2/\sigma^2\sim\chi^2_{n-1}$:
$$\left(\frac{(n-1)s^2}{\chi^2_{\alpha/2,\,n-1}},\; \frac{(n-1)s^2}{\chi^2_{1-\alpha/2,\,n-1}}\right)$$
($\chi^2_{\alpha/2}$ denotes the upper-tail critical value.) Asymmetric, not "estimate ± margin"; the larger critical value gives the lower bound. Take square roots for σ.

### Proportion (large sample)

$$\hat{p} \pm z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}},\qquad n\hat p\ge5,\ n(1-\hat p)\ge5$$
Sample size: $n = z_{\alpha/2}^2\hat p(1-\hat p)/ME^2$; with no prior estimate use $\hat p=0.5$ (largest $n$).

**Wilson interval** (slide 16 "general" and the R code on slide 23):
$$\frac{\hat p + \frac{z^2}{2n}}{1 + \frac{z^2}{n}} \pm \frac{z\sqrt{\frac{\hat p(1-\hat p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
More accurate for small $n$ or extreme $\hat p$, where the simple interval can go below 0 or above 1.

### R programs

```r
ci_mean <- function(sample, sigma, alpha) {           # sigma known
    n <- length(sample); ME <- qnorm(1-alpha/2) * sigma/sqrt(n)
    c(mean(sample) - ME, mean(sample) + ME) }
ci_mean <- function(sample, alpha) {                  # sigma unknown
    n <- length(sample); ME <- qt(1-alpha/2, n-1) * sd(sample)/sqrt(n)
    c(mean(sample) - ME, mean(sample) + ME) }
ci_var <- function(sample, alpha) {
    n <- length(sample)
    ll <- (n-1)*var(sample)/qchisq(1-alpha/2, n-1)
    ul <- (n-1)*var(sample)/qchisq(alpha/2, n-1)
    c(ll, ul) }
ci_p <- function(n, freq, alpha) {                    # Wilson, as printed (with typos)
    ph <- freq/n; za <- qnorm(1-alpha/2)
    ph2 <- (ph + za^2/2*n)/(1 + za^2/n)
    ME  <- sqrt(ph*(1-ph)/n + za^2/4*n^2)/(1 + za^2/n)
    c(ph - ME, ph + ME) }
```

Slide 23's code has errors: `za^2/2*n` should be `za^2/(2*n)` and `za^2/4*n^2` should be `za^2/(4*n^2)` (R evaluates `*` and `/` left to right); `ph2` should be the centre instead of `ph`; and the call is written `ci_var(sample,alpha)` instead of `ci_p(n,freq,alpha)`.

## ✏️ Exercises

The four problems are the lecturer's examples.

**1.** (Slide 8) Salary is normal with variance 25. A sample of 16 has total \$1250. (a) 90% upper and lower bounds; (b) 95% two-sided CI; (c) how many more people for an error below \$1.5? (d) 24 more people give a total of \$1890; find the CI.

> [!example]- Solution
> σ = 5 (known), $\bar x=78.125$, $SE=5/4=1.25$; use $z$.
>
> (a) $z_{0.10}=1.282$, ME = 1.6025: $\mu<79.73$; $\mu>76.52$.
> (b) $78.125\pm1.96(1.25)=(75.675,\ 80.575)$.
> (c) $n=(1.96\cdot5/1.5)^2=42.68\Rightarrow43$; survey 27 more.
> (d) Pool totals: $n=40$, $\bar x=3140/40=78.5$, $SE=5/\sqrt{40}=0.7906$, ME = 1.549: $(76.95,\ 80.05)$. The width falls from 4.90 to 3.10, ratio $\sqrt{40/16}=1.58$.

**2.** (Slide 13) 25 workers: mean \$34, sd \$4, wages normal. (a) 95% CI; (b) 80% upper bound; (c) 99% lower bound; (d) 90% prediction interval.

> [!example]- Solution
> σ unknown → $t_{24}$; $SE=4/5=0.8$.
> (a) $t_{0.025,24}=2.064$: $34\pm1.651=(32.35,\ 35.65)$ (with $z$ it would be too narrow: (32.43, 35.57)).
> (b) $t_{0.20,24}=0.857$: $\mu<34.69$.
> (c) $t_{0.01,24}=2.492$: $\mu>32.01$.
> (d) $t_{0.05,24}=1.711$: $34\pm1.711\cdot4\sqrt{1.04}=34\pm6.98=(27.02,\ 40.98)$.
>
> The PI (width 13.96) is over four times the 95% CI (3.30) despite a lower level: it must cover one worker, whose wage varies with $s=4$ whatever the sample size.

**3.** (Slide 15) Same survey. (a) 95% CI for the variance; (b) 90% upper bound for σ.

> [!example]- Solution
> $(n-1)s^2=24\cdot16=384$.
> (a) $\chi^2_{0.025,24}=39.364$, $\chi^2_{0.975,24}=12.401$: $(384/39.364,\ 384/12.401)=(9.76,\ 30.97)$. Not centred on 16 (chi-squared is skewed).
> (b) Upper bound needs the lower-tail value $\chi^2_{0.90,24}=15.659$: $\sigma^2<24.52$, $\sigma<4.95$. Square roots preserve coverage because √ is monotonic.
>
> Variance intervals require normality; the CLT does not rescue them.

**4.** (Slide 18) 48 of 200 insurance customers claimed. (a) 90% CI for the claim proportion. (b) For ME = 3%: sample size at 90%; and the confidence achieved with 200 customers.

> [!example]- Solution
> $\hat p=0.24$; $n\hat p=48$, $n(1-\hat p)=152$ ✓. $SE=\sqrt{0.24\cdot0.76/200}=0.0302$.
> (a) $0.24\pm1.645(0.0302)=0.24\pm0.0497=(0.190,\ 0.290)$.
> (b) $n=1.645^2(0.24)(0.76)/0.03^2=548.3\Rightarrow549$ (with $\hat p=0.5$: 752). With $n=200$: $z=0.03/0.0302=0.993$, confidence $2\Phi(0.993)-1\approx0.68$. Sample size, precision and confidence: you can fix any two.

**5.** (Advanced) What does "95% confidence" mean? Why doesn't a prediction interval shrink to zero?

> [!example]- Solution
> "95% probability that μ is in (75.675, 80.575)" is wrong in the frequentist view: μ is fixed, so it is in or not. Before sampling, $\bar X\pm1.96\sigma/\sqrt n$ is a random interval with 95% coverage; after substituting $\bar x$, no probability remains. Of 100 researchers' intervals, about 95 contain μ. (A Bayesian credible interval does allow the probability statement, by treating μ as random.)
>
> CI uses $s/\sqrt n\to0$; PI uses $s\sqrt{1+1/n}\to s$. The CI has only estimation uncertainty; the PI also includes individual variability, which data cannot remove. Quoting a CI for "what will this customer's claim be?" understates risk badly.

## 📝 Summary

- CI = estimate ± critical value × SE.
- Confidence describes the method, not the computed interval.
- σ known → $z$; σ unknown → $t_{n-1}$ (wider).
- Two-sided $z_{\alpha/2}$, one-sided $z_\alpha$.
- $n=(z_{\alpha/2}\sigma/ME)^2$, rounded up.
- Prediction interval: $s\sqrt{1+1/n}$, wider, does not vanish.
- Variance CI: $\chi^2_{n-1}$, asymmetric.
- Proportion CI with conditions $n\hat p\ge5$, $n(1-\hat p)\ge5$; Wilson for small $n$.
- Precision, confidence, sample size: pick two.

## ⚠️ Important Notes

1. Never say "95% probability that μ is in this interval".
2. One-sided vs two-sided changes the critical value (90%: 1.282 vs 1.645).
3. Use $t$ whenever σ is estimated.
4. Degrees of freedom $n-1$.
5. CI is for the mean, PI for one observation.
6. The variance CI is asymmetric; the larger χ² value goes in the lower bound.
7. Variance intervals need normality.
8. Round sample sizes up; "how many more" means subtract what you have.
9. Combine samples by pooling totals, not averaging means.
10. The simple proportion interval fails for small $n$ or extreme $\hat p$; use Wilson.
11. Lowering the confidence level narrows the interval without reducing uncertainty.

> [!warning] Gaps in the source slides
> - Slides 2–5, 7 (definition, z formula), 9–11 (Example 1 solution, t formula), 12 (prediction interval), 14 (variance CI), 16–17 (proportion CIs) are images; Wilson is partly recoverable from slide 23's R code.
> - The four example statements (slides 8, 13, 15, 18) and the R programs extracted; critical values are from standard tables (all verified with scipy).
> - Exercise set: [1] ch. 8 (p. 390) 1–9; (p. 399) 12–15, 19, 20, 23, 25, 26; (p. 407) 30, 33, 35, 37, 42; (p. 411) 45, 47, 48; (p. 420) 59–62, 64, 65; [2] pp. 325, 329, 331, 333.

**Previous:** [[05 - Point Estimation]] · **Next:** [[07 - Hypothesis Testing - One Sample]]
