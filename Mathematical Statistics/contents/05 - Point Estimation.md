---
subject: Mathematical Statistics
chapter: 05
tags: [ds, statistics, estimation, mle, unbiasedness, actuarial]
source: "MS_Lec05_Estimator.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Point Estimation

> [!note] Reading
> **[1] Devore & Berk, Ch. 7** · **[2] Miller & Miller, Point Estimation, pp. 283–316**
>
> This is the most **mathematically demanding** lecture of the course and the most distinctly **actuarial** — MLE, Fisher information, and the Cramér–Rao bound are core actuarial exam material, and go well beyond a general business statistics syllabus.

> [!warning] Source note
> Like [[04 - Sampling Distributions]], this deck is **almost entirely equation images** — 24 of 29 slides carry only a title. Examples 5.1–5.9 are lost. The formulas below are the standard results the slide titles name, **reconstructed**; the two classification tables and the numeric likelihood table survived.

## 📘 Main Knowledge

### Point estimate vs interval estimate

- **Point estimate** — a single number offered as the value of a parameter. "$\hat\mu = 8.1$".
- **Interval estimate** — a range with an attached confidence level. "$\mu \in (7.4, 8.8)$ with 95% confidence." → [[06 - Confidence Interval]]

A point estimate alone conveys no uncertainty, which is why interval estimation exists. This chapter builds the machinery both depend on.

### Estimator vs estimate

> **Estimator is a formula on a random sample. Estimate is the observed value from an observed sample.**

- **Estimator** $\hat{\theta} = \hat\theta(X_1,\dots,X_n)$ — a **random variable**, because it is a function of random variables. It has a distribution, a mean, and a variance.
- **Estimate** $\hat{\theta}(x_1,\dots,x_n)$ — one realised **number**.

The distinction from [[04 - Sampling Distributions]] again: $\bar{X}$ is an estimator, $\bar{x} = 8.1$ is an estimate. **Every property in this chapter — unbiasedness, efficiency, consistency — is a property of the estimator, never of a single estimate.** It makes no sense to call the number 8.1 "unbiased".

### Mean squared error

The overall measure of an estimator's quality:

$$\text{MSE}(\hat{\theta}) = \mathbb{E}\big[(\hat{\theta} - \theta)^2\big] = \operatorname{Var}(\hat{\theta}) + \big[\text{Bias}(\hat{\theta})\big]^2$$

where $\text{Bias}(\hat{\theta}) = \mathbb{E}[\hat{\theta}] - \theta$.

**This decomposition is the central organising idea of the chapter.** Error comes from two sources: being *systematically off* (bias) and being *unstable* (variance). It is the same bias–variance trade-off that governs model selection in [[Machine Learning/contents/00-Index|Machine Learning]].

### Unbiasedness and efficiency

**Unbiased:** $\mathbb{E}[\hat{\theta}] = \theta$ — correct *on average* over repeated samples. Otherwise the estimator **over-** or **under-estimates**.

**Efficient:** among unbiased estimators, the one with **smallest variance**. An unbiased estimator can still be useless if it is wildly variable.

Slide 5 illustrates the four combinations, and slide 6 tabulates them:

| Estimator | | |
|---|---|---|
| **Unbiased** | **Efficient** | ← the best case |
| | Not efficient | |
| **Biased** (over or under) | | |

The classic examples:
- $\bar{X}$ is unbiased for $\mu$: $\mathbb{E}[\bar{X}] = \mu$.
- $s^2$ with divisor $n-1$ is unbiased for $\sigma^2$; with divisor $n$ it is **biased downward** — the reason for $n-1$ in [[03 - Descriptive Statistics]].

### Moment estimators (Method of Moments)

The oldest and simplest method: **equate population moments to sample moments and solve.**

$$\mathbb{E}[X^k] = \frac{1}{n}\sum_{i=1}^{n} X_i^k \qquad k = 1, 2, \dots$$

Use as many equations as there are unknown parameters. For a one-parameter family, setting $\mathbb{E}[X] = \bar{X}$ and solving usually suffices.

*Example:* for $X \sim \text{Exp}(\lambda)$, $\mathbb{E}[X] = 1/\lambda$, so setting $1/\lambda = \bar{X}$ gives $\hat{\lambda}_{MM} = 1/\bar{X}$.

**Pro:** simple, always computable. **Con:** can be inefficient, and may produce estimates outside the parameter space.

### Percentile matching estimator

The same idea applied to **quantiles** rather than moments: set the theoretical percentile equal to the sample percentile and solve.

$$F^{-1}(p \mid \theta) = \hat{x}_p$$

Common in actuarial work, where fitted loss distributions must match observed quantiles (a 95th-percentile claim size matters more than a mean), and usable when moments do not exist — as for heavy-tailed distributions like the Cauchy or a Pareto with small shape parameter.

### Likelihood function

$$L(\theta) = \prod_{i=1}^{n} f(x_i \mid \theta) \qquad\qquad \ell(\theta) = \ln L(\theta) = \sum_{i=1}^{n} \ln f(x_i \mid \theta)$$

The likelihood reads the density **backwards**: with the data fixed and $\theta$ varying, it measures how *plausible* each candidate $\theta$ is for the data actually seen.

> [!warning] Likelihood is not probability
> $L(\theta)$ is **not** the probability that $\theta$ takes a value — $\theta$ is a fixed constant, not random. $L$ does not integrate to 1 over $\theta$ and is not a distribution. It is a *relative* measure: $L(\theta_1) > L(\theta_2)$ means the data are more consistent with $\theta_1$.

### Maximising the likelihood

Slide 18 shows the search done numerically — evaluating $L(p)$ on a grid:

| $p$ | $L(p)$ |
|---|---|
| 0.01 | 0.000099 |
| 0.02 | 0.000392 |
| 0.03 | 0.000873 |
| … | … |
| 0.66 | 0.148104 |
| **0.67** | **0.148137** ← maximum |
| 0.68 | 0.147968 |
| … | … |
| 0.98 | 0.019208 |
| 0.99 | 0.009801 |

The likelihood rises to a peak near $p = 0.67$ and falls away — that peak is the MLE. Analytically one solves $\frac{d\ell}{d\theta} = 0$ rather than searching a grid.

### Maximum Likelihood Estimator (MLE)

$$\hat{\theta}_{MLE} = \arg\max_{\theta} L(\theta) = \arg\max_{\theta} \ell(\theta)$$

**Always maximise the log-likelihood**, for three reasons: $\ln$ is monotonic so the argmax is unchanged; products become sums, which differentiate easily; and it avoids numerical underflow when multiplying many small densities.

**Why MLE dominates:** under regularity conditions it is **consistent**, **asymptotically unbiased**, **asymptotically efficient** (attaining the Cramér–Rao bound), **asymptotically normal**, and **invariant** — if $\hat\theta$ is the MLE of $\theta$, then $g(\hat\theta)$ is the MLE of $g(\theta)$, a property the method of moments lacks.

### Fisher information

$$I(\theta) = \mathbb{E}\left[\left(\frac{\partial \ell}{\partial \theta}\right)^2\right] = -\,\mathbb{E}\left[\frac{\partial^2 \ell}{\partial \theta^2}\right]$$

Fisher information measures **how much the sample tells you about $\theta$**. The second form is the more intuitive: it is the expected *curvature* of the log-likelihood. A sharply peaked likelihood pins $\theta$ down precisely (high information); a flat one leaves many values nearly as plausible (low information).

For an i.i.d. sample, $I_n(\theta) = n \cdot I_1(\theta)$ — **information accumulates linearly with sample size**, which is precisely why variance falls as $1/n$.

### Cramér–Rao inequality

$$\operatorname{Var}(\hat{\theta}) \;\ge\; \frac{1}{I(\theta)} = \frac{1}{n\,I_1(\theta)} \qquad\text{(for unbiased } \hat\theta)$$

**A hard floor on precision.** No unbiased estimator can have variance below the Cramér–Rao Lower Bound (CRLB). An unbiased estimator attaining it is **efficient** — the Minimum Variance Unbiased Estimator (MVUE), the best that can exist.

This is a genuinely strong statement: it says the difficulty of estimating $\theta$ is a property of the *distribution*, not of the analyst's cleverness. No amount of ingenuity beats the bound.

### Asymptotic properties

Finite-sample optimality is often unattainable, so we ask what happens as $n \to \infty$:

- **Asymptotically unbiased** — $\mathbb{E}[\hat{\theta}] \to \theta$
- **Asymptotically efficient** — $\operatorname{Var}(\hat{\theta}) \to$ CRLB
- **Consistent** — $\hat{\theta} \xrightarrow{P} \theta$

**The full classification (slide 25):**

| | | |
|---|---|---|
| **Unbiased** | **Efficient (Best estimator)** | |
| | Not efficient | **Asymptotically efficient** |
| | | Not asymptotically efficient |
| **Biased** (over or under) | | **Asymptotically unbiased** |
| | | Not asymptotically unbiased |

The bottom-right cell — biased and not even asymptotically unbiased — is the only genuinely unusable category. A biased but asymptotically unbiased estimator with low variance is often **preferable** to an unbiased one with high variance, since MSE weighs both.

## ✏️ Exercises

**1.** Explain the difference between an estimator and an estimate, and why "unbiased" describes only one of them.

> [!example]- Solution
> An **estimator** is a *rule*: $\bar{X} = \frac{1}{n}\sum X_i$. Because it is a function of random variables, it is itself a **random variable** with a distribution, a mean, and a variance. An **estimate** is the *number* the rule produces from one dataset: $\bar{x} = 8.1$.
>
> **Only the estimator can be unbiased**, because unbiasedness is a statement about a long-run average:
> $$\mathbb{E}[\hat\theta] = \theta$$
> The expectation is taken over **all possible samples**. A single number has no expectation — asking whether 8.1 is unbiased is a category error, like asking whether one coin flip is fair.
>
> The practical consequence: an unbiased estimator can still give a badly wrong estimate on your particular sample. Unbiasedness guarantees no *systematic* error, not accuracy in any one instance. That is why variance matters too, and why MSE combines them.
>
> Notation convention: capital letters for estimators ($\bar{X}$, $S^2$), lowercase for estimates ($\bar{x}$, $s^2$) — the same distinction as random vs observed sample in [[04 - Sampling Distributions]].

**2.** Prove that $\bar{X}$ is unbiased for $\mu$, and show why $\frac{1}{n}\sum(X_i-\bar{X})^2$ is biased for $\sigma^2$.

> [!example]- Solution
> **$\bar{X}$ is unbiased.** By linearity of expectation:
> $$\mathbb{E}[\bar{X}] = \mathbb{E}\left[\frac{1}{n}\sum_{i=1}^{n} X_i\right] = \frac{1}{n}\sum_{i=1}^{n}\mathbb{E}[X_i] = \frac{1}{n} \cdot n\mu = \mu \;\checkmark$$
> Note this needs only identical distribution, **not independence** — linearity always holds.
>
> **The naive variance is biased.** Write $\tilde{S}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2$. The key algebraic identity:
> $$\sum(X_i - \mu)^2 = \sum(X_i - \bar{X})^2 + n(\bar{X}-\mu)^2$$
> Taking expectations, and using $\mathbb{E}[(X_i-\mu)^2] = \sigma^2$ and $\mathbb{E}[(\bar X - \mu)^2] = \operatorname{Var}(\bar X) = \sigma^2/n$:
> $$n\sigma^2 = \mathbb{E}\Big[\sum(X_i-\bar X)^2\Big] + n\cdot\frac{\sigma^2}{n}$$
> $$\mathbb{E}\Big[\sum(X_i-\bar X)^2\Big] = (n-1)\sigma^2$$
>
> Therefore
> $$\mathbb{E}[\tilde{S}^2] = \frac{n-1}{n}\sigma^2 < \sigma^2$$
> — **biased downward**, with bias $-\sigma^2/n$. Dividing by $n-1$ instead removes it exactly:
> $$\mathbb{E}[S^2] = \mathbb{E}\left[\frac{1}{n-1}\sum(X_i-\bar X)^2\right] = \sigma^2 \;\checkmark$$
>
> **Why it happens:** deviations are taken about $\bar{X}$, which is itself pulled toward the data, so $\sum(X_i-\bar X)^2$ is systematically *smaller* than $\sum(X_i-\mu)^2$ — by exactly $n(\bar X - \mu)^2$ on average.
>
> A caution worth knowing: **$S$ is still biased for $\sigma$** even though $S^2$ is unbiased for $\sigma^2$, because $\sqrt{\cdot}$ is non-linear and $\mathbb{E}[\sqrt{Y}] \ne \sqrt{\mathbb{E}[Y]}$ (Jensen's inequality). Unbiasedness does not survive non-linear transformation — unlike the MLE's invariance property.

**3.** Derive the MLE of $p$ for a Bernoulli sample, and verify it against the numeric table on slide 18.

> [!example]- Solution
> For $X_i \sim \text{Bernoulli}(p)$, $f(x\mid p) = p^x(1-p)^{1-x}$. With $\sum x_i = k$ successes in $n$ trials:
> $$L(p) = \prod_{i=1}^n p^{x_i}(1-p)^{1-x_i} = p^{k}(1-p)^{n-k}$$
> $$\ell(p) = k\ln p + (n-k)\ln(1-p)$$
> $$\frac{d\ell}{dp} = \frac{k}{p} - \frac{n-k}{1-p} = 0$$
> $$k(1-p) = (n-k)p \;\Longrightarrow\; k - kp = np - kp \;\Longrightarrow\; \boxed{\hat{p}_{MLE} = \frac{k}{n} = \bar{x}}$$
>
> The sample proportion — reassuringly, the obvious estimator is also the optimal one. The second derivative $-k/p^2 - (n-k)/(1-p)^2 < 0$ confirms a maximum.
>
> **Checking against slide 18:** the tabulated $L(p)$ peaks at $p = 0.67$, so the data must have $k/n \approx 0.67$ — consistent with, say, $k = 2$ of $n = 3$. Indeed $L(2/3) = (2/3)^2(1/3) = 0.1481$, matching the tabulated maximum of 0.148137. ✓
>
> Two observations. The likelihood is **very flat near its peak** — 0.148104 at $p=0.66$ versus 0.148137 at $p=0.67$, differing in the fifth decimal. Flat likelihood means **low Fisher information**, hence high variance: with $n=3$ we genuinely cannot distinguish $p = 0.66$ from $p = 0.67$. Curvature at the peak *is* the information.
>
> And the method of moments gives the same answer here ($\mathbb{E}[X] = p = \bar{X}$). The two methods often coincide for simple families and diverge for complex ones.

**4.** State the Cramér–Rao inequality and explain what it means for an estimator to be "efficient". Why is the bound a statement about the distribution rather than the analyst?

> [!example]- Solution
> For any unbiased $\hat\theta$:
> $$\operatorname{Var}(\hat{\theta}) \ge \frac{1}{I(\theta)} = \frac{1}{n I_1(\theta)}$$
>
> An unbiased estimator achieving equality is **efficient** — the MVUE, the best unbiased estimator that can exist.
>
> **Why it is a property of the distribution:** Fisher information $I(\theta) = -\mathbb{E}[\partial^2\ell/\partial\theta^2]$ is computed **entirely from the density $f(x\mid\theta)$**. No data, no estimator, no analyst appears in it. It quantifies how sharply the distribution's shape responds to changes in $\theta$.
>
> If two nearby values of $\theta$ produce nearly identical densities, samples from them look alike and *no procedure* can reliably tell them apart. The difficulty is intrinsic. This is why the CRLB is such a strong result: it is not "no one has yet found a better estimator", it is **no better unbiased estimator can exist**.
>
> The practical uses are threefold: it tells you when to **stop looking** for improvements; it gives a **benchmark** — an estimator at 80% efficiency needs 25% more data to match the MVUE; and since $I_n = n I_1$, it converts directly into **sample size planning**.
>
> **Caveats.** The bound applies to **unbiased** estimators only — a *biased* estimator can have variance below the CRLB and lower MSE overall (ridge regression is exactly this trade). It also requires **regularity conditions**: the support of $f$ must not depend on $\theta$, which fails for e.g. $\text{Uniform}(0,\theta)$, where the MLE $\max(X_i)$ beats the bound.

**5.** (Advanced) Explain the MSE decomposition and give a case where a **biased** estimator is preferable to an unbiased one.

> [!example]- Solution
> $$\text{MSE}(\hat\theta) = \mathbb{E}[(\hat\theta-\theta)^2] = \operatorname{Var}(\hat\theta) + \text{Bias}(\hat\theta)^2$$
>
> *Derivation:* add and subtract $\mathbb{E}[\hat\theta]$ inside the square and expand; the cross term $2\,\mathbb{E}\big[(\hat\theta - \mathbb{E}\hat\theta)\big]\cdot\text{Bias}$ vanishes because $\mathbb{E}[\hat\theta - \mathbb{E}\hat\theta] = 0$.
>
> **Two independent sources of error.** Bias is systematic — aiming at the wrong spot. Variance is instability — scattered shots. Total error weighs both, so **unbiasedness alone is not optimality**: an unbiased estimator with enormous variance can have far worse MSE than a slightly biased, stable one.
>
> **Concrete case — estimating $\sigma^2$ for a normal sample.** Compare divisors:
>
> | Divisor | Bias | MSE |
> |---|---|---|
> | $n-1$ | 0 (unbiased) | $\dfrac{2\sigma^4}{n-1}$ |
> | $n+1$ | slightly negative | $\dfrac{2\sigma^4}{n+1}$ ← **smaller** |
>
> Dividing by $n+1$ is **biased but has strictly lower MSE** for every $n$. The small downward bias buys a larger reduction in variance. We nonetheless teach $n-1$, because unbiasedness composes well across procedures and is the convention the $t$ and $\chi^2$ distributions are built on.
>
> **The case that matters in practice — shrinkage.** Ridge regression deliberately biases coefficients toward zero:
> $$\hat\beta_{ridge} = (X'X + \lambda I)^{-1}X'y$$
> OLS is unbiased (Gauss–Markov), but when predictors are collinear its variance explodes. Ridge accepts bias for a large variance reduction and achieves lower MSE and better prediction. The same logic underlies LASSO, James–Stein estimation, and regularisation generally — see [[Machine Learning/contents/00-Index|Machine Learning]] and [[Econometrics/contents/00-Index|Econometrics]].
>
> **In actuarial work this is credibility theory:** a premium estimate blends the individual risk's own experience (unbiased but volatile on thin data) with the portfolio mean (biased for that risk but stable). The credibility factor $Z$ is precisely a bias–variance trade-off, and it is why a new driver's premium is not based solely on their own two years of claims.
>
> **When to prefer unbiasedness:** when estimates will be aggregated (errors cancel only if centred), when the parameter has a contractual or legal meaning, and when $n$ is large enough that variance is already small.

## 📝 Summary

- **Estimator = formula on a random sample (a random variable); estimate = the observed number.** All properties belong to the estimator.
- **$\text{MSE} = \operatorname{Var} + \text{Bias}^2$** — the organising decomposition of the chapter.
- **Unbiased:** $\mathbb{E}[\hat\theta]=\theta$. **Efficient:** smallest variance among unbiased estimators.
- **$\bar X$ is unbiased for $\mu$**; dividing the sum of squares by $n$ is biased downward, by $n-1$ is unbiased.
- **Method of moments:** equate population and sample moments and solve. Simple, sometimes inefficient.
- **Percentile matching:** the same idea with quantiles; useful in actuarial fitting and when moments do not exist.
- **Likelihood $L(\theta)=\prod f(x_i\mid\theta)$ is not a probability over $\theta$.** Always maximise $\ell = \ln L$.
- **MLE is consistent, asymptotically unbiased, asymptotically efficient, asymptotically normal, and invariant.**
- **Fisher information = expected curvature of $\ell$**; $I_n = n I_1$, so information accumulates linearly in $n$.
- **Cramér–Rao:** $\operatorname{Var}(\hat\theta) \ge 1/I(\theta)$ for unbiased estimators — a hard floor set by the distribution itself.
- **Asymptotic properties** rescue estimators that are not finite-sample optimal; only "not even asymptotically unbiased" is truly unusable.

## ⚠️ Important Notes

**Unbiasedness is not preserved under non-linear transformation.** $S^2$ unbiased for $\sigma^2$ does **not** make $S$ unbiased for $\sigma$ (Jensen's inequality). The MLE, by contrast, **is** invariant — $g(\hat\theta_{MLE})$ is the MLE of $g(\theta)$.

**Likelihood is not probability.** $L(\theta)$ does not integrate to 1 over $\theta$ and says nothing about the probability that $\theta$ takes a value — $\theta$ is fixed, not random. (Only under a Bayesian prior does a probability statement about $\theta$ become meaningful.)

**Always work with the log-likelihood** — monotonic, turns products into sums, and prevents numerical underflow.

**Check the second derivative.** $\frac{d\ell}{d\theta}=0$ locates a stationary point, which could be a minimum or a boundary point. Verify $\frac{d^2\ell}{d\theta^2} < 0$.

**MLE can be biased in finite samples.** For $N(\mu,\sigma^2)$ the MLE of $\sigma^2$ divides by $n$, not $n-1$ — biased downward. MLE's optimality is *asymptotic*.

**MLE is not always at an interior stationary point.** For $\text{Uniform}(0,\theta)$ the likelihood increases up to $\theta = \max(x_i)$ and drops to zero after — the maximum is at a boundary and calculus finds nothing. Watch for parameter-dependent support.

**Cramér–Rao applies only to unbiased estimators, and only under regularity conditions.** Biased estimators can have lower variance *and* lower MSE. The bound fails when the support depends on $\theta$.

**Asymptotic efficiency says nothing about small samples.** An estimator can be asymptotically efficient and perform poorly at $n=20$. The relevant question is whether *your* $n$ is large enough.

**A flat likelihood means low information means high variance.** Slide 18's table barely distinguishes $p=0.66$ from $p=0.67$ — the data genuinely cannot separate them. Curvature at the peak *is* the information.

**Method of moments can produce impossible estimates** — a negative variance, or a probability outside $[0,1]$. MLE respects the parameter space by construction.

**Unbiasedness is not automatically the goal.** Regularisation, shrinkage, and actuarial credibility all deliberately introduce bias to reduce variance. Judge by MSE and by purpose.

> [!warning] Gaps in the source slides
> **24 of 29 slides carry only a title.** Everything mathematical is an embedded image:
> - **Slides 2, 4** — Estimation setup; **the MSE formula and its decomposition**
> - **Slides 5–6** — bias/efficiency illustrations (only the table skeleton extracted)
> - **Slides 7–10 — Examples 5.1, 5.2, 5.3 and one further example: lost entirely**
> - **Slide 11** — the Method of Moments definition
> - **Slides 12–13 — Example 5.4** ("Find Moment estimators of the following parameters") — **the parameters themselves are an image**, so the exercise is unusable
> - **Slides 14–15** — Percentile Matching and Example 5.5
> - **Slides 16–17** — the likelihood function definition and Example 5.6
> - **Slides 19–20** — **the MLE definition**, and Example 5.7 ("Find MLE of the following parameters") — again the parameter list is an image
> - **Slides 21–23** — **Fisher's information and the Cramér–Rao inequality**, plus Example 5.8. Given these are the actuarially examinable core, this is the most costly gap in the lecture.
> - **Slides 24, 26** — asymptotic properties; Example 5.9
> - **Slide 29** — the R likelihood-function extension
>
> **All nine worked examples (5.1–5.9) are unrecoverable.** Every formula above is the standard textbook form reconstructed from slide titles — verify against Devore Ch. 7 and Miller & Miller pp. 283–316.
>
> **Exercises set:** [1] Ch. 7 (p. 346) 1, 2, 7–13; (p. 359) 21, 22, 23, 27, 30; (p. 378) 42–46 · [2] Point Estimation (p. 290, p. 299, p. 305).

---
**Previous:** [[04 - Sampling Distributions]] · **Next:** [[06 - Confidence Interval]]
