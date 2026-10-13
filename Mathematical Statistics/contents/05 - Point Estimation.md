---
subject: Mathematical Statistics
chapter: 05
tags: [ds, statistics, estimation, mle, unbiasedness, actuarial]
source: "MS_Lec05_Estimator.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Point Estimation

Reading: Devore & Berk ch. 7; Miller & Miller, Point Estimation, pp. 283–316. The most mathematical and most actuarial lecture (MLE, Fisher information, Cramér–Rao).

> [!warning] Source note
> 24 of 29 slides have only a title; Examples 5.1–5.9 are lost. Formulas below are standard results named in the titles; the two classification tables and the likelihood table extracted.

## 📘 Main Knowledge

### Point and interval estimates

- **Point estimate**: one number for a parameter ($\hat\mu=8.1$).
- **Interval estimate**: a range with a confidence level ($\mu\in(7.4,8.8)$ at 95%), [[06 - Confidence Interval]].

### Estimator vs estimate

Slide: "Estimator is a formula on a random sample. Estimate is the observed value from an observed sample."
- Estimator $\hat\theta(X_1,\dots,X_n)$: a random variable with a distribution, mean and variance.
- Estimate $\hat\theta(x_1,\dots,x_n)$: a number.

Unbiasedness, efficiency and consistency are properties of estimators, not of single estimates.

### Mean squared error

$$\text{MSE}(\hat{\theta}) = E\big[(\hat{\theta} - \theta)^2\big] = \operatorname{Var}(\hat{\theta}) + \big[\text{Bias}(\hat{\theta})\big]^2,\qquad \text{Bias}=E[\hat\theta]-\theta$$

Error comes from systematic offset (bias) and instability (variance), as in the bias–variance trade-off of [[Machine Learning/contents/00-Index|Machine Learning]].

### Unbiasedness and efficiency

- **Unbiased**: $E[\hat\theta]=\theta$; otherwise over- or under-estimating.
- **Efficient**: smallest variance among unbiased estimators.

| Estimator | | |
|---|---|---|
| unbiased | efficient | best case |
| | not efficient | |
| biased (over/under) | | |

$\bar X$ is unbiased for $\mu$; $s^2$ with divisor $n-1$ is unbiased for $\sigma^2$, with divisor $n$ it is biased downward ([[03 - Descriptive Statistics]]).

### Method of moments

Set population moments equal to sample moments and solve:
$$E[X^k] = \frac{1}{n}\sum_{i=1}^{n} X_i^k,\qquad k=1,2,\dots$$
(one equation per parameter). Example: $X\sim\text{Exp}(\lambda)$, $E[X]=1/\lambda$, so $\hat\lambda_{MM}=1/\bar X$. Simple, but can be inefficient or give values outside the parameter space.

### Percentile matching

Match theoretical and sample quantiles: $F^{-1}(p\mid\theta)=\hat x_p$. Used in actuarial loss fitting (tail quantiles matter) and when moments do not exist (Cauchy, heavy-tailed Pareto).

### Likelihood

$$L(\theta) = \prod_{i=1}^{n} f(x_i \mid \theta),\qquad \ell(\theta) = \ln L(\theta) = \sum_{i=1}^{n} \ln f(x_i \mid \theta)$$

With the data fixed, $L$ measures how plausible each $\theta$ is. It is not a probability distribution over $\theta$ ($\theta$ is fixed, and $L$ need not integrate to 1); only comparisons like $L(\theta_1)>L(\theta_2)$ matter.

Slide 18 evaluates $L(p)$ on a grid:

| $p$ | $L(p)$ |
|---|---|
| 0.01 | 0.000099 |
| 0.02 | 0.000392 |
| 0.03 | 0.000873 |
| … | … |
| 0.66 | 0.148104 |
| 0.67 | 0.148137 (maximum) |
| 0.68 | 0.147968 |
| … | … |
| 0.98 | 0.019208 |
| 0.99 | 0.009801 |

These values equal $p^2(1-p)$, i.e. 2 successes in 3 trials. Analytically, solve $d\ell/d\theta=0$.

### Maximum likelihood estimator

$$\hat{\theta}_{MLE} = \arg\max_{\theta} L(\theta) = \arg\max_{\theta} \ell(\theta)$$

Maximize $\ell$: same argmax, sums instead of products, no numerical underflow. Under regularity conditions the MLE is consistent, asymptotically unbiased, asymptotically efficient, asymptotically normal, and invariant ($g(\hat\theta)$ is the MLE of $g(\theta)$).

### Fisher information and Cramér–Rao

$$I(\theta) = E\left[\left(\frac{\partial \ell}{\partial \theta}\right)^2\right] = -E\left[\frac{\partial^2 \ell}{\partial \theta^2}\right]$$

The expected curvature of the log-likelihood: a sharp peak pins $\theta$ down, a flat one does not. For i.i.d. data $I_n=nI_1$.

**Cramér–Rao lower bound** (unbiased $\hat\theta$):
$$\operatorname{Var}(\hat{\theta}) \ge \frac{1}{I(\theta)} = \frac{1}{n\,I_1(\theta)}$$
An unbiased estimator attaining it is efficient (minimum variance unbiased). The bound depends only on the distribution.

### Asymptotic properties

- asymptotically unbiased: $E[\hat\theta]\to\theta$;
- asymptotically efficient: $\operatorname{Var}(\hat\theta)\to$ CRLB;
- consistent: $\hat\theta\xrightarrow{P}\theta$.

Slide 25's classification:

| | | |
|---|---|---|
| unbiased | efficient (best) | |
| | not efficient | asymptotically efficient |
| | | not asymptotically efficient |
| biased | | asymptotically unbiased |
| | | not asymptotically unbiased |

A biased but asymptotically unbiased, low-variance estimator can beat an unbiased high-variance one on MSE; only "not even asymptotically unbiased" is unusable.

## ✏️ Exercises

**1.** Estimator vs estimate: why does "unbiased" apply to only one?

> [!example]- Solution
> The estimator $\bar X$ is a rule and a random variable; the estimate $\bar x=8.1$ is a number. Unbiasedness, $E[\hat\theta]=\theta$, averages over all possible samples; a single number has no expectation. An unbiased estimator can still give a poor estimate on one sample, which is why variance (and MSE) matters.

**2.** Show $\bar X$ is unbiased for $\mu$ and $\frac1n\sum(X_i-\bar X)^2$ is biased for $\sigma^2$.

> [!example]- Solution
> $E[\bar X]=\frac1n\sum E[X_i]=\mu$ (linearity; no independence needed).
>
> Using $\sum(X_i-\mu)^2=\sum(X_i-\bar X)^2+n(\bar X-\mu)^2$ and taking expectations (independence gives $E[(\bar X-\mu)^2]=\sigma^2/n$):
> $$n\sigma^2=E\Big[\sum(X_i-\bar X)^2\Big]+\sigma^2\ \Rightarrow\ E\Big[\sum(X_i-\bar X)^2\Big]=(n-1)\sigma^2$$
> So $E[\tilde S^2]=\frac{n-1}{n}\sigma^2$ (bias $-\sigma^2/n$), while $S^2$ with divisor $n-1$ is unbiased. $S$ is still biased for $\sigma$ (Jensen: $E[\sqrt Y]\neq\sqrt{E[Y]}$).

**3.** Derive the Bernoulli MLE and check it against slide 18.

> [!example]- Solution
> With $k$ successes in $n$ trials: $L(p)=p^k(1-p)^{n-k}$, $\ell(p)=k\ln p+(n-k)\ln(1-p)$,
> $$\frac{d\ell}{dp}=\frac kp-\frac{n-k}{1-p}=0\ \Rightarrow\ \hat p=\frac kn=\bar x$$
> $\ell''=-k/p^2-(n-k)/(1-p)^2<0$, a maximum. Slide 18's values are $p^2(1-p)$ ($k=2$, $n=3$): $L(2/3)=0.1481$, and the grid peak 0.148137 at 0.67. The likelihood is very flat near the top (0.148104 at 0.66), so with $n=3$ the information is low. The method of moments gives the same $\hat p$ here.

**4.** State Cramér–Rao and explain efficiency. Why is the bound about the distribution, not the analyst?

> [!example]- Solution
> $\operatorname{Var}(\hat\theta)\ge1/(nI_1(\theta))$ for unbiased $\hat\theta$; equality means efficient. $I(\theta)$ is computed from $f(x\mid\theta)$ alone: if nearby $\theta$ values give nearly identical densities, no procedure can separate them. Uses: know when to stop searching, benchmark estimators (80% efficiency needs 25% more data), plan sample sizes. Limits: only unbiased estimators (biased ones can have lower variance and MSE, e.g. ridge), and regularity conditions (fails for Uniform(0, θ), whose support depends on θ).

**5.** (Advanced) Explain the MSE decomposition and give a case where a biased estimator is better.

> [!example]- Solution
> Add and subtract $E[\hat\theta]$ inside the square; the cross term vanishes because $E[\hat\theta-E\hat\theta]=0$.
>
> Normal $\sigma^2$, dividing the sum of squares by $c$:
>
> | Divisor | Bias | MSE |
> |---|---|---|
> | $n-1$ | 0 | $2\sigma^4/(n-1)$ |
> | $n+1$ | negative | $2\sigma^4/(n+1)$ (smaller) |
>
> The $n+1$ divisor is biased but has lower MSE for every $n$. $n-1$ is still taught because unbiasedness underlies the $t$ and $\chi^2$ procedures.
>
> Shrinkage: ridge regression $\hat\beta=(X'X+\lambda I)^{-1}X'y$ adds bias to cut variance under collinearity ([[Econometrics/contents/00-Index|Econometrics]]). In actuarial credibility theory, a premium blends a risk's own (unbiased, noisy) experience with the portfolio mean (biased, stable). Prefer unbiasedness when estimates are aggregated, when the parameter has legal meaning, or when $n$ is large.

## 📝 Summary

- Estimator = random variable; estimate = number; properties belong to estimators.
- MSE = variance + bias².
- Unbiased: $E[\hat\theta]=\theta$; efficient: minimum variance among unbiased estimators.
- $\bar X$ unbiased; sum of squares/$n$ biased, /$(n-1)$ unbiased.
- Method of moments and percentile matching.
- Likelihood is not a probability over θ; maximize $\ell=\ln L$.
- MLE: consistent, asymptotically unbiased, efficient, normal, invariant.
- Fisher information = expected curvature; $I_n=nI_1$; Cramér–Rao: $\operatorname{Var}\ge1/I$.

## ⚠️ Important Notes

1. Unbiasedness is lost under non-linear transformations; MLE invariance is not.
2. Likelihood is not probability (only with a Bayesian prior does θ get a distribution).
3. Work with the log-likelihood.
4. Check the second derivative (or boundaries).
5. The normal MLE of $\sigma^2$ divides by $n$: MLEs can be biased in finite samples.
6. Uniform(0, θ): the MLE is $\max x_i$, at a boundary; calculus finds no stationary point.
7. Cramér–Rao needs unbiasedness and regularity.
8. Asymptotic efficiency says nothing about small $n$.
9. A flat likelihood means little information.
10. Method of moments can give impossible values; MLE respects the parameter space.
11. Shrinkage and credibility deliberately add bias; judge by MSE and purpose.

> [!warning] Gaps in the source slides
> - Slides 2, 4 (MSE), 5–6 (bias/efficiency illustrations), 7–10 (Examples 5.1–5.3 and one more), 11 (method of moments), 12–13 (Example 5.4, whose parameter list is an image), 14–15 (percentile matching, Example 5.5), 16–17 (likelihood, Example 5.6), 19–20 (MLE, Example 5.7), 21–23 (Fisher information, Cramér–Rao, Example 5.8: the costliest gap), 24, 26 (asymptotics, Example 5.9) and 29 (R) are images.
> - All formulas are standard reconstructions; check Devore ch. 7 and Miller & Miller pp. 283–316.
> - Exercise set: [1] ch. 7 (p. 346) 1, 2, 7–13; (p. 359) 21–23, 27, 30; (p. 378) 42–46; [2] pp. 290, 299, 305.

**Previous:** [[04 - Sampling Distributions]] · **Next:** [[06 - Confidence Interval]]
