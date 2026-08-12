---
subject: Mathematical Statistics
chapter: 06
tags: [ds, statistics, confidence-interval, estimation, inference]
source: "MS_Lec06_Interval.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Confidence Intervals

> [!note] Reading
> **[1] Devore & Berk, Ch. 8** · **[2] Miller & Miller, Interval Estimation, pp. 325–333**
>
> [[05 - Point Estimation]] produced a single number with no measure of uncertainty. This chapter attaches one. It applies the sampling distributions from [[04 - Sampling Distributions]] directly — every interval here is an inverted probability statement about a statistic.

> [!warning] Source note
> All formulas are equation images. **However, all four worked examples and all four R programs extracted in full** — so this chapter is far better supported than [[04 - Sampling Distributions]] or [[05 - Point Estimation]]. The examples are solved in the Exercises below.

## 📘 Main Knowledge

### The idea

A **confidence interval** is a range of plausible values for a parameter, with a stated confidence level. The general form:

$$\hat{\theta} \pm (\text{critical value}) \times (\text{standard error})$$

The quantity added and subtracted is the **margin of error (ME)**.

At 95% confidence, the interval leaves **2.5% in each tail** (slide 6). Confidence level $= 1-\alpha$, so $\alpha = 0.05$ and each tail holds $\alpha/2$.

> [!warning] What "95% confidence" actually means
> **It does not mean $P(\mu \in \text{interval}) = 0.95$.** The parameter $\mu$ is a fixed constant — it is either inside your interval or it is not; there is no probability about it.
>
> The randomness lies in the **interval**, which shifts from sample to sample. The correct reading: *if we repeated the sampling procedure many times, 95% of the intervals so constructed would contain $\mu$.* Confidence is a property of the **method**, not of the one interval you computed.

### CI for the mean — $\sigma$ known

From $\bar{X} \sim N(\mu, \sigma^2/n)$:

$$\bar{x} \pm z_{\alpha/2}\,\frac{\sigma}{\sqrt{n}}$$

| Confidence | $\alpha$ | $z_{\alpha/2}$ |
|---|---|---|
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | **1.96** |
| 99% | 0.01 | 2.576 |

**One-sided intervals** use $z_\alpha$ (the whole $\alpha$ in one tail):

- **Upper confidence bound:** $\mu < \bar{x} + z_\alpha \frac{\sigma}{\sqrt{n}}$
- **Lower confidence bound:** $\mu > \bar{x} - z_\alpha \frac{\sigma}{\sqrt{n}}$

At 90% one-sided, $z_{0.10} = 1.282$.

### CI for the mean — $\sigma$ unknown

Replace $\sigma$ with $s$ and the normal with Student's $t$ on $n-1$ degrees of freedom:

$$\bar{x} \pm t_{\alpha/2,\,n-1}\,\frac{s}{\sqrt{n}}$$

The $t$ critical value exceeds the corresponding $z$, widening the interval — the price of estimating $\sigma$. See [[04 - Sampling Distributions]].

### Sample size determination

Setting $ME = z_{\alpha/2}\frac{\sigma}{\sqrt{n}}$ and solving:

$$n = \left(\frac{z_{\alpha/2}\,\sigma}{ME}\right)^{2}$$

**Always round up.** Note $n$ depends on $ME$ **squared** — halving the margin of error costs four times the sample.

### Prediction interval

A **confidence interval** covers the *mean* $\mu$. A **prediction interval** covers a *single future observation* $X_{n+1}$ — a different and harder problem, because a new observation varies both around $\mu$ *and* because $\mu$ is estimated:

$$\bar{x} \pm t_{\alpha/2,\,n-1}\; s\sqrt{1 + \frac{1}{n}}$$

The extra **1** under the root is the individual observation's own variability. Consequently a PI is **always wider** than the corresponding CI, and — crucially — **it does not shrink to zero as $n\to\infty$**. With infinite data you know $\mu$ exactly but still cannot predict one person's wage better than $\sigma$ allows.

### CI for variance — normal population

From $\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}$:

$$\left(\frac{(n-1)s^2}{\chi^2_{\alpha/2,\,n-1}},\;\; \frac{(n-1)s^2}{\chi^2_{1-\alpha/2,\,n-1}}\right)$$

**Chi-squared is not symmetric**, so the two critical values differ and the interval is **not** of the form estimate ± margin. Note the larger critical value goes in the **denominator of the lower** bound.

For $\sigma$, take square roots of both endpoints.

### CI for proportion — large sample

$$\hat{p} \pm z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

Valid when $n\hat p \ge 5$ and $n(1-\hat p) \ge 5$. Note $\hat p$ substitutes for the unknown $p$ inside the standard error.

**Sample size for a proportion:**

$$n = \frac{z_{\alpha/2}^2\,\hat p(1-\hat p)}{ME^2}$$

With no prior estimate, use $\hat p = 0.5$, which maximises $p(1-p)$ and gives the most conservative (largest) $n$.

**General (Wilson) interval.** Slide 16's "CI for proportion – General" and the R code on slide 23 implement the **Wilson score interval**, which solves for $p$ without approximating the standard error by $\hat p$:

$$\frac{\hat p + \frac{z^2}{2n}}{1 + \frac{z^2}{n}} \;\pm\; \frac{z\sqrt{\frac{\hat p(1-\hat p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

It is markedly more accurate for small $n$ or extreme $\hat p$, where the simple interval can even extend below 0 or above 1.

### R programs

**CI for the mean, $\sigma$ known:**
```r
ci_mean <- function(sample, sigma, alpha) {
    n  <- length(sample)
    ME <- qnorm(1-alpha/2) * sigma/sqrt(n)
    c(mean(sample) - ME, mean(sample) + ME)
}
```

**CI for the mean, $\sigma$ unknown:**
```r
ci_mean <- function(sample, alpha) {
    n  <- length(sample)
    ME <- qt(1-alpha/2, n-1) * sd(sample)/sqrt(n)
    c(mean(sample) - ME, mean(sample) + ME)
}
```

**CI for variance** — note the swapped quantiles:
```r
ci_var <- function(sample, alpha) {
    n  <- length(sample)
    ll <- (n-1)*var(sample)/qchisq(1-alpha/2, n-1)
    ul <- (n-1)*var(sample)/qchisq(alpha/2, n-1)
    c(ll, ul)
}
```

**CI for proportion (Wilson):**
```r
ci_p <- function(n, freq, alpha) {
    ph  <- freq/n
    za  <- qnorm(1-alpha/2)
    ph2 <- (ph + za^2/2*n)/(1 + za^2/n)
    ME  <- sqrt(ph*(1-ph)/n + za^2/4*n^2)/(1 + za^2/n)
    c(ph - ME, ph + ME)
}
```

> [!warning] Typos in the slide's R code
> Slide 23 contains three errors. `za^2/2*n` should be `za^2/(2*n)`, and `za^2/4*n^2` should be `za^2/(4*n^2)` — R's `*` and `/` have equal precedence and evaluate left to right, so these multiply where they should divide. Also `ph2` is computed but never used (it should be the interval's centre, in place of `ph`), and the final call is written `ci_var(sample,alpha)` instead of `ci_p(n,freq,alpha)`.

## ✏️ Exercises

*The four examples below are the lecturer's own, extracted verbatim.*

**1.** *(Slide 8)* Salary is normal with variance 25 (\$²). A random sample of 16 people has total salary \$1250.
> (a) Find the upper and lower 90% confidence bounds for average salary.
> (b) Find the two-sided 95% confidence interval.
> (c) To have an interval with error less than \$1.5, how many more people should be surveyed?
> (d) Surveying 24 more people gives a total of \$1890. Find the CI of the mean.

> [!example]- Solution
> $\sigma = \sqrt{25} = 5$, $n = 16$, $\bar{x} = 1250/16 = 78.125$. Since $\sigma$ is **known** and the population normal, use $z$.
>
> $$\operatorname{SE} = \frac{5}{\sqrt{16}} = 1.25$$
>
> **(a) One-sided 90% bounds.** All 10% in one tail: $z_{0.10} = 1.282$, so $ME = 1.282(1.25) = 1.6025$.
> - Upper bound: $\mu < 78.125 + 1.6025 = \mathbf{79.73}$
> - Lower bound: $\mu > 78.125 - 1.6025 = \mathbf{76.52}$
>
> **(b) Two-sided 95%.** $z_{0.025} = 1.96$, $ME = 1.96(1.25) = 2.45$:
> $$(78.125 - 2.45,\; 78.125 + 2.45) = \mathbf{(75.675,\; 80.575)}$$
>
> **(c) Sample size for $ME < 1.5$** (at 95%):
> $$n = \left(\frac{1.96 \times 5}{1.5}\right)^2 = (6.533)^2 = 42.68 \;\Rightarrow\; n = 43$$
> We have 16, so survey **27 more people**. Note the question asks how many *more* — a common place to lose marks.
>
> **(d) Combined sample.** Pool the totals, do **not** average the two means:
> $$n = 16 + 24 = 40, \qquad \bar{x} = \frac{1250 + 1890}{40} = \frac{3140}{40} = 78.5$$
> $$\operatorname{SE} = \frac{5}{\sqrt{40}} = 0.7906, \qquad ME = 1.96(0.7906) = 1.549$$
> $$\mathbf{(76.95,\; 80.05)}$$
> The interval has narrowed from a width of 4.90 to 3.10 — because $n$ rose from 16 to 40, and $\sqrt{40}/\sqrt{16} = 1.58$, exactly the ratio of the widths.

**2.** *(Slide 13)* A wage survey of 25 workers gives mean \$34 and standard deviation \$4; wages are normal.
> (a) 95% CI for the mean. (b) 80% upper confidence bound. (c) 99% lower confidence bound. (d) 90% prediction interval.

> [!example]- Solution
> Now $\sigma$ is **unknown** — $s = 4$ is a *sample* standard deviation — so use $t$ with $df = 24$.
>
> $$\operatorname{SE} = \frac{4}{\sqrt{25}} = 0.8$$
>
> **(a) 95% CI.** $t_{0.025,24} = 2.064$:
> $$34 \pm 2.064(0.8) = 34 \pm 1.651 = \mathbf{(32.35,\; 35.65)}$$
> Using $z = 1.96$ here would give (32.43, 35.57) — too narrow. With $n=25$ the difference is modest but real.
>
> **(b) 80% upper bound.** One-sided, $t_{0.20,24} = 0.857$:
> $$\mu < 34 + 0.857(0.8) = \mathbf{34.69}$$
>
> **(c) 99% lower bound.** One-sided, $t_{0.01,24} = 2.492$:
> $$\mu > 34 - 2.492(0.8) = \mathbf{32.01}$$
>
> **(d) 90% prediction interval.** $t_{0.05,24} = 1.711$, and the standard error gains the extra 1:
> $$34 \pm 1.711 \times 4\sqrt{1 + \tfrac{1}{25}} = 34 \pm 1.711 \times 4(1.0198) = 34 \pm 6.98 = \mathbf{(27.02,\; 40.98)}$$
>
> **The PI is 13.96 wide against the 95% CI's 3.30** — more than four times wider, at a *lower* confidence level. The reason: the CI locates the **average** wage, while the PI must cover **one individual's** wage, which varies with the full $s = 4$ regardless of sample size. As $n \to \infty$ the CI collapses to a point but the PI converges to $\mu \pm 1.711\sigma$ — irreducible individual variation.

**3.** *(Slide 15)* Same survey (25 workers, mean \$34, sd \$4).
> (a) 95% CI for the variance. (b) 90% upper confidence bound for the standard deviation.

> [!example]- Solution
> $(n-1)s^2 = 24 \times 16 = 384$, $df = 24$.
>
> **(a) 95% CI for $\sigma^2$.** Critical values $\chi^2_{0.025,24} = 39.364$ and $\chi^2_{0.975,24} = 12.401$:
> $$\left(\frac{384}{39.364},\; \frac{384}{12.401}\right) = \mathbf{(9.76,\; 30.97)}$$
>
> Note the interval is **not centred on $s^2 = 16$** — it extends 6.24 below and 14.97 above. Chi-squared is right-skewed, so the interval inherits that asymmetry. Writing it as "$16 \pm$ something" would be wrong.
>
> Note also that the **larger** critical value produces the **lower** bound, because it sits in the denominator. Reversing them is the standard error here.
>
> **(b) 90% upper bound for $\sigma$.** One-sided, so all 10% in one tail. An upper bound on $\sigma^2$ needs the *smaller* critical value, $\chi^2_{0.90,24} = 15.659$:
> $$\sigma^2 < \frac{384}{15.659} = 24.52 \quad\Longrightarrow\quad \sigma < \sqrt{24.52} = \mathbf{4.95}$$
>
> Taking square roots of the endpoints is legitimate because $\sqrt{\cdot}$ is monotonic — the transformation preserves the ordering, so it preserves coverage. (This is *not* the same as unbiasedness surviving a transformation, which it does not — see [[05 - Point Estimation]].)
>
> **This entire procedure requires normality**, and unlike the CI for the mean it is **not** rescued by the CLT. Inference on variance is notoriously sensitive to departures from normality.

**4.** *(Slide 18)* Of 200 insurance customers, 48 made claims.
> (a) 90% CI for the claim proportion.
> (b) For a margin of error of 3%: at 90% confidence, how many customers must be surveyed? With 200 customers, what confidence level is achieved?

> [!example]- Solution
> $\hat{p} = 48/200 = 0.24$. Check validity: $n\hat p = 48 \ge 5$ and $n(1-\hat p) = 152 \ge 5$. ✓
>
> **(a) 90% CI.** $z_{0.05} = 1.645$:
> $$\operatorname{SE} = \sqrt{\frac{0.24 \times 0.76}{200}} = \sqrt{0.000912} = 0.0302$$
> $$0.24 \pm 1.645(0.0302) = 0.24 \pm 0.0497 = \mathbf{(0.190,\; 0.290)}$$
> Between 19.0% and 29.0% of customers claim.
>
> **(b i) Sample size for $ME = 0.03$ at 90%:**
> $$n = \frac{1.645^2 (0.24)(0.76)}{0.03^2} = \frac{2.706 \times 0.1824}{0.0009} = \frac{0.4936}{0.0009} = 548.4 \;\Rightarrow\; \mathbf{n = 549}$$
> Nearly **triple** the current sample, to cut the margin from 4.97% to 3% — the $\sqrt{n}$ penalty again.
>
> *(Without the pilot estimate, using the conservative $\hat p = 0.5$ gives $n = 752$. The pilot study saves 200 respondents.)*
>
> **(b ii) Confidence level achievable with $n=200$ and $ME = 0.03$:** solve for $z$:
> $$z = \frac{ME}{\operatorname{SE}} = \frac{0.03}{0.0302} = 0.993$$
> $$\text{Confidence} = 2\Phi(0.993) - 1 = 2(0.8397) - 1 = 0.679 \approx \mathbf{68\%}$$
>
> **This is the practical lesson of the exercise.** With 200 customers you can have a ±3% margin at only 68% confidence, or 90% confidence with a ±5% margin — **but not both**. Precision, confidence, and sample size are three quantities of which you may fix any two. Demanding tighter margins without more data simply buys a weaker guarantee.

**5.** (Advanced) Explain precisely what "95% confidence" means and why the common interpretation is wrong. Then explain why a prediction interval does not shrink to zero as $n \to \infty$.

> [!example]- Solution
> **The wrong reading:** "there is a 95% probability that $\mu$ lies in (75.675, 80.575)."
>
> This is meaningless in the frequentist framework. $\mu$ is a **fixed constant** — the true average salary is some particular number. It is either in that interval or it is not. The probability is 1 or 0; we simply do not know which.
>
> **The correct reading:** the *procedure* has a 95% success rate. Before sampling, $\bar X$ is random, so the interval $\bar{X} \pm 1.96\,\sigma/\sqrt{n}$ is a **random interval**, and
> $$P\big(\bar{X} - 1.96\tfrac{\sigma}{\sqrt n} < \mu < \bar{X} + 1.96\tfrac{\sigma}{\sqrt n}\big) = 0.95$$
> is a legitimate probability statement — about the interval, not about $\mu$. Once you substitute $\bar{x} = 78.125$ the randomness is spent and no probability statement remains.
>
> Operationally: **if 100 researchers each drew their own sample and built their own 95% interval, about 95 of those intervals would contain $\mu$.** You cannot know whether yours is one of them.
>
> *(A Bayesian **credible interval** does support the statement "95% probability that $\mu$ is in this range" — but only by treating $\mu$ as a random variable with a prior. Different framework, different object.)*
>
> **Why a PI does not vanish.** Compare the two standard errors:
> $$\text{CI: } \frac{s}{\sqrt{n}} \qquad\qquad \text{PI: } s\sqrt{1 + \frac{1}{n}}$$
> As $n \to \infty$ the CI's width $\to 0$ — with unlimited data you pin down $\mu$ exactly. But the PI's width $\to t \cdot s$, a **positive constant**.
>
> The reason is that they answer different questions. The CI's uncertainty is entirely **estimation** uncertainty, which data removes. The PI carries estimation uncertainty *plus* the **inherent variability of an individual**, which no amount of data eliminates. Even knowing the population mean wage is exactly \$34 with certainty, the *next worker's* wage still scatters with $\sigma = 4$.
>
> In Exercise 2 this is stark: the 95% CI is 3.30 wide, the 90% PI is 13.96 wide. **Confusing them is a serious practical error** — quoting a CI when someone asks "what will this customer's claim be?" understates the risk by a factor of four. In actuarial work the distinction is the difference between pricing the portfolio mean and reserving for individual claims.

## 📝 Summary

- **CI form:** estimate ± (critical value) × (standard error). The second term is the **margin of error**.
- **"95% confidence" describes the method, not the interval.** $\mu$ is fixed; the interval is random.
- **$\sigma$ known → $z$; $\sigma$ unknown → $t_{n-1}$.** The $t$ interval is wider.
- **Two-sided uses $z_{\alpha/2}$; one-sided uses $z_\alpha$** (all the risk in one tail).
- **$n = (z_{\alpha/2}\sigma/ME)^2$**, always rounded up. Halving $ME$ quadruples $n$.
- **Prediction interval covers one future observation** and uses $s\sqrt{1+1/n}$ — always wider, and it **does not shrink to zero**.
- **CI for $\sigma^2$ uses $\chi^2_{n-1}$ and is asymmetric**; the larger critical value gives the lower bound.
- **CI for $p$:** $\hat p \pm z\sqrt{\hat p(1-\hat p)/n}$, needing $n\hat p \ge 5$ and $n(1-\hat p)\ge 5$. Use $\hat p = 0.5$ for conservative planning.
- **Precision, confidence, and sample size: pick two.**

## ⚠️ Important Notes

**Never say "95% probability that $\mu$ is in this interval."** The parameter is fixed. Confidence attaches to the procedure.

**One-sided vs two-sided changes the critical value.** At 90%, two-sided uses $z_{0.05}=1.645$ but one-sided uses $z_{0.10}=1.282$. Read the question carefully — "upper confidence bound" is one-sided.

**Use $t$ whenever $\sigma$ is estimated**, however large $n$ is. The two converge by $n \approx 30$, but using $z$ with an estimated $\sigma$ is wrong in principle and materially wrong for small $n$.

**Degrees of freedom is $n-1$**, not $n$.

**Confidence intervals and prediction intervals answer different questions.** CI → the mean; PI → one observation. The PI is much wider and never collapses. Quoting a CI when a PI is wanted drastically understates risk.

**The variance CI is not symmetric** and cannot be written as $s^2 \pm$ something. The larger $\chi^2$ value goes in the **lower** bound's denominator.

**The variance CI requires normality and the CLT does not save it.** Unlike inference on the mean, it is highly sensitive to non-normality. Check with a QQ plot ([[03 - Descriptive Statistics]]).

**Round sample size up, always.** $n = 42.68$ means 43; rounding down misses the target margin.

**"How many more?" ≠ "how many?"** Subtract the sample you already have.

**Pool raw totals when combining samples**, not the two sample means — unless the samples are the same size, averaging the means is wrong.

**The simple proportion interval fails at extreme $\hat p$ or small $n$**, sometimes extending below 0 or above 1. Use the Wilson interval (slide 16/23) there.

**The proportion's standard error uses $\hat p$ in place of the unknown $p$** — an approximation that is part of why the large-sample condition exists.

**A wider interval is not a worse one.** It is an honest report of the uncertainty present. Narrowing an interval by lowering the confidence level does not reduce uncertainty; it hides it.

> [!warning] Gaps in the source slides
> Formulas are images throughout — **slides 2–7, 9–12, 14, 16–17 have titles only or no text at all**. Specifically lost:
> - **Slides 2–5, 7** — the CI definition, derivation, and the $z$-based formula
> - **Slides 9–11** — the worked solution to Example 1 and the $t$-based CI formula
> - **Slide 12 — the Prediction Interval formula**
> - **Slide 14 — the CI for variance formula**
> - **Slides 16–17 — both proportion CI formulas.** The Wilson form is partially recoverable from the R code on slide 23 (which contains typos, noted above).
>
> **The four example problem statements (slides 8, 13, 15, 18) and all four R programs extracted intact** — these are solved in the Exercises above. All formulas are the standard textbook forms, reconstructed; critical values are from standard tables and should be checked against the tables your exam permits.
>
> **Slide 6** shows the 95%/2.5%/2.5% tail structure as a labelled diagram.
>
> **Exercises set:** [1] Ch. 8 (p. 390) 1–9; (p. 399) 12–15, 19, 20, 23, 25, 26; (p. 407) 30, 33, 35, 37, 42; (p. 411) 45, 47, 48; (p. 420) 59–62, 64, 65 · [2] Interval Estimation (p. 325, 329, 331, 333).

---
**Previous:** [[05 - Point Estimation]] · **Next:** [[07 - Hypothesis Testing - One Sample]]
