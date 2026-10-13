---
subject: Mathematical Statistics
chapter: 04
tags: [ds, statistics, sampling-distribution, central-limit-theorem, inference]
source: "MS_Lec04_Sampling.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Sampling Distributions

Reading: Devore & Berk ch. 6 (pp. 284–381). The turning point of the course: estimation, confidence intervals and tests all depend on how a statistic behaves across repeated samples.

> [!warning] Source note
> 22 of 31 slides have only a title (equations are images). Formulas below are the standard results named in the titles. The dice tables, the normal table and the summary/exercise lists extracted intact.

## 📘 Main Knowledge

### Population, random sample, observed sample

- **Population**: all units; fixed unknown parameters ($\mu$, $\sigma^2$, $p$).
- **Random sample** $X_1,\dots,X_n$: random variables before data collection, usually i.i.d. (independent, identically distributed as the population).
- **Observed sample** $x_1,\dots,x_n$: the numbers obtained.

$\bar X$ is a random variable; $\bar x$ is one realized value. A **statistic** is a function of the sample with no unknown parameters; it is a random variable, and its distribution is the **sampling distribution**.

### Example 4.1: two dice

Population {1, …, 6}, uniform, $\mu=3.5$, $\sigma^2=35/12\approx2.917$. With $n=2$ the 36 outcomes are equally likely; sample means:

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 |
| **2** | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 |
| **3** | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 |
| **4** | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 |
| **5** | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 |
| **6** | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |

The population is flat, but $\bar x=3.5$ occurs 6 times and $\bar x=1$ once: the means are triangular and already moving toward a bell shape. $E[\bar X]=3.5$, $\operatorname{Var}(\bar X)=2.917/2\approx1.458$.

### Results for the sample mean

For an i.i.d. sample from any population with mean $\mu$, variance $\sigma^2$:
$$E[\bar{X}] = \mu,\qquad \operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n},\qquad \operatorname{SD}(\bar{X}) = \frac{\sigma}{\sqrt{n}}\ \text{(standard error)}$$

Halving the standard error requires four times the sample.

**Normal population**: exactly, for any $n$,
$$\bar{X} \sim N\!\left(\mu, \frac{\sigma^2}{n}\right),\qquad Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0,1)$$

Standard normal table (slide 9, $\Phi(z)=P(Z\le z)$; rows = first decimal, columns = second):

| $z$ | .00 | .01 | .02 | .03 | .04 | .05 | .06 | .07 | .08 | .09 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | .5000 | .5040 | .5080 | .5120 | .5160 | .5199 | .5239 | .5279 | .5319 | .5359 |
| 0.1 | .5398 | .5438 | .5478 | .5517 | .5557 | .5596 | .5636 | .5675 | .5714 | .5753 |
| 0.2 | .5793 | .5832 | .5871 | .5910 | .5948 | .5987 | .6026 | .6064 | .6103 | .6141 |
| 0.3 | .6179 | .6217 | .6255 | .6293 | .6331 | .6368 | .6406 | .6443 | .6480 | .6517 |
| 0.4 | .6554 | .6591 | .6628 | .6664 | .6700 | .6736 | .6772 | .6808 | .6844 | .6879 |
| 0.5 | .6915 | .6950 | .6985 | .7019 | .7054 | .7088 | .7123 | .7157 | .7190 | .7224 |
| 0.6 | .7257 | .7291 | .7324 | .7357 | .7389 | .7422 | .7454 | .7486 | .7517 | .7549 |
| 0.7 | .7580 | .7611 | .7642 | .7673 | .7704 | .7734 | .7764 | .7794 | .7823 | .7852 |

(The deck's table stops at 0.7.) Excel: `NORMDIST(b, µ, σ, 1)`, `NORMSDIST(z)`, `NORMSINV(p)`.

**Central Limit Theorem**: for a non-normal population,
$$\bar{X} \xrightarrow{d} N\!\left(\mu, \frac{\sigma^2}{n}\right)\quad\text{as } n\to\infty$$
Rule of thumb $n\ge30$; skewed populations need more. The dice table is the CLT in miniature.

**Intervals for the sample mean** (slide 16, "3 popular intervals"):
$$P\left(\mu - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} < \bar{X} < \mu + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right) = 1 - \alpha$$

| Level | $z_{\alpha/2}$ |
|---|---|
| 90% | 1.645 |
| 95% | 1.96 |
| 99% | 2.576 |

These are acceptance intervals for $\bar X$ given $\mu$. Inverting them gives confidence intervals ([[06 - Confidence Interval]]); comparing $\bar x$ with them is a test ([[07 - Hypothesis Testing - One Sample]]).

### Sample proportion

$\hat p=X/n$ for a binary variable with proportion $p$:
$$E[\hat{p}] = p,\qquad \operatorname{Var}(\hat{p}) = \frac{p(1-p)}{n},\qquad \hat p \;\dot\sim\; N\!\left(p, \frac{p(1-p)}{n}\right)\text{ for large }n$$
Condition: $np\ge5$ and $n(1-p)\ge5$.

### Chi-squared, t and the sample variance

- $\chi^2_k$: $\sum_{i=1}^k Z_i^2$ for independent standard normals; on $[0,\infty)$, right-skewed, mean $k$, variance $2k$.
- $t_k$: $Z/\sqrt{V/k}$ with $V\sim\chi^2_k$ independent of $Z$; symmetric, heavier tails than normal, tends to $N(0,1)$ as $k\to\infty$.
- With $\sigma$ unknown: $T = (\bar{X} - \mu)/(s/\sqrt{n}) \sim t_{n-1}$ (normal population).
- Sample variance (normal population): $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$.

Summary slide (28):

| Statistic | Distribution |
|---|---|
| sample mean | normal (Student $t$ if σ unknown) |
| sample proportion | normal (large sample) |
| statistic of sample variance | chi-squared |

## ✏️ Exercises

**1.** From the dice table, find the distribution of $\bar X$ ($n=2$) and check $E[\bar X]=\mu$ and $\operatorname{Var}(\bar X)=\sigma^2/2$.

> [!example]- Solution
> | $\bar x$ | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |
> |---|---|---|---|---|---|---|---|---|---|---|---|
> | count | 1 | 2 | 3 | 4 | 5 | 6 | 5 | 4 | 3 | 2 | 1 |
>
> Probabilities are count/36: triangular, symmetric about 3.5, so $E[\bar X]=3.5$. $\sigma^2=17.5/6=2.9167$ and the variance from the table is 1.4583 $=\sigma^2/2$. Extreme means need every die extreme (only (1,1) gives 1); central means arise in many ways. That concentration is what the CLT describes.

**2.** $\mu=50$, $\sigma=12$, $n=36$. Find $P(\bar X>53)$ and state the assumptions.

> [!example]- Solution
> $SE=12/6=2$, $Z=(53-50)/2=1.5$, $P=1-\Phi(1.5)=1-0.9332=0.0668$. Exact if the population is normal; otherwise the CLT with $n=36$ is reasonable unless the population is very skewed. A single observation has $P(X>53)=P(Z>0.25)=0.401$, six times larger. With $\sigma$ unknown, use $s$ and $t_{35}$.

**3.** Why is $\operatorname{SD}(\bar X)=\sigma/\sqrt n$ and not $\sigma/n$? What does this mean for the cost of precision?

> [!example]- Solution
> $\operatorname{Var}(\bar X)=\frac1{n^2}\operatorname{Var}(\sum X_i)=\frac1{n^2}n\sigma^2=\sigma^2/n$: constants come out squared, independent variances add. Independence is essential; positively correlated observations (clusters, time series) give a larger true SE and intervals that are too narrow.
>
> Halving the SE needs 4× the data (100 → 400 → 1600), so each extra observation is worth less. Polls stop around $n\approx1000$ (margin about ±3%). The SE depends on $n$, not on the population size $N$ (when $n/N$ is small).

**4.** Chi-squared vs Student $t$: uses, and why $t$ has heavier tails.

> [!example]- Solution
> $\chi^2_k$ (sum of squared normals): non-negative, right-skewed, mean $k$, variance $2k$; used for variance inference and the χ² test ([[09 - Non-parametric Testing]]). $t_k$: used for means with unknown σ.
>
> $Z=(\bar X-\mu)/(\sigma/\sqrt n)$ has one random part; $T=(\bar X-\mu)/(s/\sqrt n)$ also has a random denominator, and when $s$ happens to be small $T$ becomes large. Hence heavier tails and larger critical values: 95%, $n=10$: $t_9=2.262$ vs $z=1.96$. As $k\to\infty$, $s\to\sigma$ and $t_k\to N(0,1)$ (close by $k\approx30$).

**5.** (Advanced) Bottles: $\mu=500$ ml, $\sigma=8$ ml. QC samples $n=25$ and rejects a batch if $\bar x$ is outside $500\pm3$. Find the rejection probability when the machine is correct and when $\mu$ drifts to 503.

> [!example]- Solution
> $SE=8/5=1.6$.
>
> Correct machine (Type I error): $Z=\pm3/1.6=\pm1.875$; $P=2(1-\Phi(1.875))=0.0608$, so about 6% of good batches are rejected.
>
> Drift to 503: limits 497 and 503; $Z_{upper}=0$, $Z_{lower}=(497-503)/1.6=-3.75$; $P=0.5+0.0001=0.5001$. Only half the drifted batches are caught (power ≈ 0.50; Type II error ≈ 0.50), because the drifted mean sits exactly on the upper limit.
>
> Increasing $n$ with the same ±3 limits cuts false alarms (at $n=100$, $SE=0.8$: 0.0002) but power stays 0.50, since the true mean is still on the limit. To detect a drift of 3 ml reliably, the limits must lie inside the drift, e.g. $500\pm1.96\,SE$: at $n=100$ that is $500\pm1.57$, giving power $P(\bar X>501.57\mid\mu=503)=P(Z>-1.79)\approx0.96$. At fixed $n$, tighter limits raise power but also false alarms ([[07 - Hypothesis Testing - One Sample]]).

## 📝 Summary

- Population (parameters) → random sample $X_i$ → observed sample $x_i$.
- A statistic is a random variable with a sampling distribution.
- $E[\bar X]=\mu$, $\operatorname{Var}(\bar X)=\sigma^2/n$; standard error $\sigma/\sqrt n$.
- Normal population → $\bar X$ exactly normal; otherwise the CLT for large $n$.
- Precision grows with $\sqrt n$.
- $\hat p\;\dot\sim\;N(p,p(1-p)/n)$ when $np\ge5$, $n(1-p)\ge5$.
- $\chi^2_k$ for variances; $t_k$ for means with unknown σ.
- $(n-1)s^2/\sigma^2\sim\chi^2_{n-1}$; $(\bar X-\mu)/(s/\sqrt n)\sim t_{n-1}$.

## ⚠️ Important Notes

1. The population distribution and the sampling distribution are different objects (uniform dice vs triangular means).
2. Standard deviation describes individuals; standard error describes the mean and shrinks with $n$.
3. The CLT applies to the mean, not the data.
4. $n\ge30$ is a rule of thumb.
5. $\operatorname{Var}(\bar X)=\sigma^2/n$ needs independence.
6. Use $z$ when σ is known, $t$ when it is estimated.
7. Degrees of freedom for one-sample mean and variance are $n-1$.
8. Chi-squared is asymmetric: intervals for $\sigma^2$ need two different critical values.
9. $\operatorname{Var}(\hat p)$ depends on the unknown $p$; $p(1-p)$ is largest at 0.5 (used for conservative planning).
10. A larger $n$ does not fix bias.

> [!warning] Gaps in the source slides
> - Slides 2–5 (definitions), 6, 12–13, 18 (Examples 4.1 setup, 4.2, 4.3; only 4.1's tables survive), 8, 11 (normal results), 14–16 (CLT statement and the three intervals, the most serious gap), 17, 19 (proportion, acceptance interval), 20–23 (χ² and t), 25–26 (sample variance), 10, 24 (Excel tables), 30–31 (R) are images.
> - All formulas are standard reconstructions; check against Devore ch. 6.
> - Corrected (2026-10-09): exercise 5 previously claimed power rises to ~99.99% at $n=100$; with limits fixed at 503 and the drifted mean at 503, power stays 0.50.
> - Exercise set: [1] ch. 6 (p. 295) 1, 2, 5, 6; (p. 304) 11–13, 15, 16, 18, 19, 21, 22; (p. 312) 27–29, 33, 36, 38, 42; (p. 325) 47, 48, 56, 64, 68, 69, 71, 73, 74, 77; [2] pp. 241, 258.

**Previous:** [[03 - Descriptive Statistics]] · **Next:** [[05 - Point Estimation]]
