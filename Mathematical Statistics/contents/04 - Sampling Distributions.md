---
subject: Mathematical Statistics
chapter: 04
tags: [ds, statistics, sampling-distribution, central-limit-theorem, inference]
source: "MS_Lec04_Sampling.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Sampling Distributions

> [!note] Reading
> **[1] Devore & Berk, Ch. 6, pp. 284–381**
>
> **This is the pivot of the course.** Everything before it describes data ([[03 - Descriptive Statistics]]); everything after it — estimation, confidence intervals, hypothesis tests — depends on knowing how a statistic behaves across repeated samples. That is what a sampling distribution is.

> [!warning] Source note
> This deck is **overwhelmingly equation images**: 22 of 31 slides have a title only. The formulas below are the standard results the slide titles name, **reconstructed**. The dice example's tables, the standard normal table, and the summary/exercise lists extracted intact.

## 📘 Main Knowledge

### Population, random sample, observed sample

Three distinct objects that are easy to conflate:

- **Population** — all units of interest, described by fixed unknown **parameters** ($\mu$, $\sigma^2$, $p$).
- **Random sample** — $X_1, X_2, \dots, X_n$, a set of **random variables** before the data is collected. Usually assumed **i.i.d.**: independent and identically distributed as the population.
- **Observed sample** — $x_1, x_2, \dots, x_n$, the actual numbers after collection.

The capital/lowercase distinction carries the whole idea. $\bar{X}$ is a **random variable** with a distribution; $\bar{x}$ is one realised number. **A sampling distribution is the distribution of $\bar{X}$** — what would happen across all possible samples, not what happened in yours.

### Random statistics

A **statistic** is any function of the random sample containing no unknown parameters. Being a function of random variables, a statistic is **itself a random variable** and therefore has a distribution — the *sampling distribution*.

### Example 4.1 — rolling two dice

The lecture's concrete demonstration. Population = $\{1,2,3,4,5,6\}$, uniform, with $\mu = 3.5$ and $\sigma^2 = 35/12 \approx 2.917$. Take a sample of $n = 2$; all 36 outcomes are equally likely:

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | (1,1) | (1,2) | (1,3) | (1,4) | (1,5) | (1,6) |
| **2** | (2,1) | (2,2) | (2,3) | (2,4) | (2,5) | (2,6) |
| **3** | (3,1) | (3,2) | (3,3) | (3,4) | (3,5) | (3,6) |
| **4** | (4,1) | (4,2) | (4,3) | (4,4) | (4,5) | (4,6) |
| **5** | (5,1) | (5,2) | (5,3) | (5,4) | (5,5) | (5,6) |
| **6** | (6,1) | (6,2) | (6,3) | (6,4) | (6,5) | (6,6) |

The corresponding sample means $\bar{x}$:

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 |
| **2** | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 |
| **3** | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 |
| **4** | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 |
| **5** | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 |
| **6** | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |

**This is the entire concept in one table.** The population is *flat* — every face equally likely. But the sample means are **not** flat: $\bar{x} = 3.5$ occurs 6 times while $\bar{x} = 1$ occurs once. Averaging concentrates probability toward the centre, producing a triangular distribution already visibly moving toward a bell shape at $n = 2$.

Two properties visible here hold generally:
$$\mathbb{E}[\bar{X}] = \mu = 3.5 \qquad \operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n} = \frac{2.917}{2} \approx 1.458$$

### The key results for the sample mean

For an i.i.d. sample from any population with mean $\mu$ and variance $\sigma^2$:

$$\mathbb{E}[\bar{X}] = \mu \qquad\qquad \operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n} \qquad\qquad \operatorname{SD}(\bar{X}) = \frac{\sigma}{\sqrt{n}}$$

$\sigma/\sqrt{n}$ is the **standard error of the mean**. Note the $\sqrt{n}$: to halve the standard error you must **quadruple** the sample size — the reason large surveys hit diminishing returns.

### Normal population

If $X \sim N(\mu, \sigma^2)$ then **exactly**, for any $n$:

$$\bar{X} \sim N\!\left(\mu, \frac{\sigma^2}{n}\right) \qquad\Longrightarrow\qquad Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim N(0,1)$$

The **standard normal table** (slide 9) gives $\Phi(z) = P(Z \le z)$, indexed by the first decimal down the rows and the second across the columns:

| $z$ | .00 | .01 | .02 | .03 | .04 | .05 | .06 | .07 | .08 | .09 |
|---|---|---|---|---|---|---|---|---|---|---|
| **0.0** | .5000 | .5040 | .5080 | .5120 | .5160 | .5199 | .5239 | .5279 | .5319 | .5359 |
| **0.1** | .5398 | .5438 | .5478 | .5517 | .5557 | .5596 | .5636 | .5675 | .5714 | .5753 |
| **0.2** | .5793 | .5832 | .5871 | .5910 | .5948 | .5987 | .6026 | .6064 | .6103 | .6141 |
| **0.3** | .6179 | .6217 | .6255 | .6293 | .6331 | .6368 | .6406 | .6443 | .6480 | .6517 |
| **0.4** | .6554 | .6591 | .6628 | .6664 | .6700 | .6736 | .6772 | .6808 | .6844 | .6879 |
| **0.5** | .6915 | .6950 | .6985 | .7019 | .7054 | .7088 | .7123 | .7157 | .7190 | .7224 |
| **0.6** | .7257 | .7291 | .7324 | .7357 | .7389 | .7422 | .7454 | .7486 | .7517 | .7549 |
| **0.7** | .7580 | .7611 | .7642 | .7673 | .7704 | .7734 | .7764 | .7794 | .7823 | .7852 |

*(The deck's table is truncated at $z = 0.7$; the full table extends to ~3.9.)*

In Excel: `=NORMDIST(b, µ, σ, 1)` for $P(X<b)$, `=NORMSDIST(z)` for the standard normal, `=NORMSINV(p)` to invert.

### Non-normal population, large sample — the Central Limit Theorem

If the population is **not** normal, the exact result fails — but asymptotically:

$$\bar{X} \;\xrightarrow{\;d\;}\; N\!\left(\mu, \frac{\sigma^2}{n}\right) \quad\text{as } n \to \infty$$

**The CLT is why normal-based inference works almost everywhere.** The conventional threshold is $n \ge 30$, though heavily skewed populations need more.

The dice table is the CLT in miniature: a uniform population produces a triangular mean distribution at $n=2$, and it grows more bell-shaped with every increment of $n$.

### Interval of the sample mean — "3 popular intervals"

Slide 16 refers to the standard coverage intervals, following from $\bar X$'s normality:

$$P\left(\mu - z_{\alpha/2}\frac{\sigma}{\sqrt{n}} < \bar{X} < \mu + z_{\alpha/2}\frac{\sigma}{\sqrt{n}}\right) = 1 - \alpha$$

| Confidence | $z_{\alpha/2}$ |
|---|---|
| 90% | 1.645 |
| 95% | **1.96** |
| 99% | 2.576 |

These are **acceptance intervals** — the range in which $\bar{X}$ is likely to fall *given* $\mu$. Inverting them produces the confidence intervals of [[06 - Confidence Interval]], and comparing an observed $\bar{x}$ against them is the basis of [[07 - Hypothesis Testing - One Sample]].

### Distribution of the sample proportion

For a binary variable with population proportion $p$, the sample proportion $\hat{p} = X/n$ satisfies:

$$\mathbb{E}[\hat{p}] = p \qquad \operatorname{Var}(\hat{p}) = \frac{p(1-p)}{n}$$

and by the CLT, for large $n$:

$$\hat{p} \;\dot\sim\; N\!\left(p, \frac{p(1-p)}{n}\right) \qquad Z = \frac{\hat{p} - p}{\sqrt{p(1-p)/n}}$$

The usual adequacy condition is $np \ge 5$ **and** $n(1-p) \ge 5$.

### The chi-squared distribution

If $Z_1,\dots,Z_k$ are independent standard normals, then $\sum Z_i^2 \sim \chi^2_k$ with $k$ **degrees of freedom**.

Properties: defined on $[0,\infty)$ only, **right-skewed**, with $\mathbb{E}[\chi^2_k] = k$ and $\operatorname{Var} = 2k$. It becomes more symmetric as $k$ grows.

### The Student $t$ distribution

If $Z \sim N(0,1)$ and $V \sim \chi^2_k$ independently, then

$$T = \frac{Z}{\sqrt{V/k}} \sim t_k$$

**Why it exists:** when $\sigma$ is unknown we substitute the sample $s$, which adds extra variability. The $t$ distribution accounts for it — symmetric and bell-shaped like the normal, but with **heavier tails**. It converges to $N(0,1)$ as $k \to \infty$ (practically, by $k \approx 30$).

$$T = \frac{\bar{X} - \mu}{s/\sqrt{n}} \sim t_{n-1}$$

Note the degrees of freedom: **$n-1$**, the same $n-1$ that appears in $s^2$ ([[03 - Descriptive Statistics]]) — and for the same reason.

### Distribution of the sample variance

For a normal population:

$$\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}$$

This is the result that lets us build confidence intervals and tests for $\sigma^2$.

**The summary slide's structure** (slide 28) — the three sampling distributions to memorise:

| Statistic | Distribution |
|---|---|
| Sample **Mean** | **Normal** (or **Student $t$** when $\sigma$ unknown) |
| Sample **Proportion** | **Normal** (large sample) |
| Statistic of Sample **Variance** | **Chi-squared** |

## ✏️ Exercises

**1.** Using the dice table, find the probability distribution of $\bar{X}$ for $n=2$, and verify $\mathbb{E}[\bar X] = \mu$ and $\operatorname{Var}(\bar X) = \sigma^2/2$.

> [!example]- Solution
> Counting each $\bar x$ in the 36-cell table:
>
> | $\bar{x}$ | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 4.5 | 5 | 5.5 | 6 |
> |---|---|---|---|---|---|---|---|---|---|---|---|
> | Count | 1 | 2 | 3 | 4 | 5 | **6** | 5 | 4 | 3 | 2 | 1 |
> | $P$ | 1/36 | 2/36 | 3/36 | 4/36 | 5/36 | 6/36 | 5/36 | 4/36 | 3/36 | 2/36 | 1/36 |
>
> **A triangular distribution** — symmetric about 3.5, peaked at the centre.
>
> By symmetry $\mathbb{E}[\bar{X}] = 3.5 = \mu$. ✓
>
> For the variance, the population has $\sigma^2 = \frac{1}{6}\sum(x-3.5)^2 = \frac{17.5}{6} \approx 2.9167$. Computing $\operatorname{Var}(\bar X)$ directly from the table gives $\approx 1.4583$, and indeed
> $$\frac{\sigma^2}{n} = \frac{2.9167}{2} = 1.4583 \;\checkmark$$
>
> **What to take from this:** the population is perfectly **uniform**, yet the sample mean is **triangular**. Averaging concentrates probability — extreme means require *every* observation to be extreme (only (1,1) gives $\bar x = 1$), while central means arise many ways. That concentration, repeated as $n$ grows, *is* the Central Limit Theorem.

**2.** A population has $\mu = 50$, $\sigma = 12$. For $n = 36$, find $P(\bar{X} > 53)$. State the assumptions.

> [!example]- Solution
> $$\operatorname{SE} = \frac{\sigma}{\sqrt{n}} = \frac{12}{6} = 2$$
> $$Z = \frac{53 - 50}{2} = 1.5$$
> $$P(\bar{X} > 53) = P(Z > 1.5) = 1 - \Phi(1.5) = 1 - 0.9332 = \mathbf{0.0668}$$
>
> **Assumptions.** If the population is normal, this is **exact** for any $n$. If not, we rely on the **CLT** — and $n = 36 \ge 30$ makes the approximation reasonable unless the population is severely skewed.
>
> Two things worth noticing. First, the **individual** probability $P(X > 53)$ would use $\sigma = 12$, giving $Z = 0.25$ and $P = 0.40$ — six times larger. The sample mean is far less variable than a single observation, which is the entire reason we sample.
>
> Second, this requires **known $\sigma$**. In practice $\sigma$ is unknown, we use $s$, and the statistic becomes $t_{n-1}$ rather than $Z$ — the situation of [[06 - Confidence Interval]].

**3.** Explain why $\operatorname{SD}(\bar{X}) = \sigma/\sqrt{n}$ and not $\sigma/n$. What does this imply about the cost of precision?

> [!example]- Solution
> Start from the variance. For independent $X_i$:
> $$\operatorname{Var}(\bar{X}) = \operatorname{Var}\!\left(\frac{1}{n}\sum X_i\right) = \frac{1}{n^2}\operatorname{Var}\!\left(\sum X_i\right) = \frac{1}{n^2}\cdot n\sigma^2 = \frac{\sigma^2}{n}$$
>
> Two rules combine here: a constant leaves the variance **squared** ($\operatorname{Var}(cX) = c^2\operatorname{Var}(X)$), while independent variances merely **add**. Taking the square root gives $\sigma/\sqrt{n}$.
>
> This is the same algebra as the diversification result in [[01 - Introduction to Statistics]] — and it depends on the same assumption. **Independence is essential:** with positively correlated observations (cluster sampling, time series) the covariance terms survive and the true standard error is larger. Treating a correlated sample as independent produces confidence intervals that are too narrow.
>
> **The cost of precision:** to halve the standard error you must **quadruple** $n$. Going from $n=100$ to $n=400$ halves it; halving it again needs $n=1600$. Precision improves with $\sqrt{n}$ while cost grows with $n$, so **the marginal value of each extra observation falls**. This is why national polls settle around $n \approx 1000$ — a margin of error near ±3%, and reducing it to ±1.5% would cost four times as much.
>
> Note $n$ appears, not the population size $N$: a sample of 1,000 is equally precise for a city or a country (provided $n/N$ is small).

**4.** Distinguish the chi-squared and Student $t$ distributions: what each is used for, and why $t$ has heavier tails than the normal.

> [!example]- Solution
> **Chi-squared** — the distribution of a **sum of squared standard normals**, $\sum_{i=1}^{k} Z_i^2 \sim \chi^2_k$. Since squares are non-negative it lives on $[0,\infty)$ and is **right-skewed**, with mean $k$ and variance $2k$. Used for **variance** inference, via $\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}$, and for the χ² independence test in [[09 - Non-parametric Testing]].
>
> **Student $t$** — the ratio $T = Z/\sqrt{V/k}$ with $V \sim \chi^2_k$ independent of $Z$. Symmetric about 0, bell-shaped, but with **heavier tails**. Used for **mean** inference when $\sigma$ is unknown.
>
> **Why the heavier tails.** With $\sigma$ known, $Z = \frac{\bar X - \mu}{\sigma/\sqrt n}$ has **one** source of randomness — the numerator. Replacing $\sigma$ with $s$ gives $T = \frac{\bar X - \mu}{s/\sqrt n}$, which has **two**: the numerator *and* the denominator both vary from sample to sample.
>
> The asymmetry in how the denominator misbehaves is what fattens the tails. When $s$ happens to come out small, it *divides* the numerator and inflates $T$ — and small values of $s$ are not rare. So extreme values of $T$ occur more often than for $Z$, and the critical values are correspondingly larger: at 95% with $n=10$, $t_9 = 2.262$ versus $z = 1.96$.
>
> **As $k \to \infty$, $t_k \to N(0,1)$**, because $s \to \sigma$ and the extra uncertainty vanishes. By $k \approx 30$ the difference is negligible — which is where the "$n \ge 30$" rule of thumb comes from. The two are linked: $t$ is built *from* a chi-squared in its denominator.

**5.** (Advanced) A machine fills bottles with $\mu = 500$ ml, $\sigma = 8$ ml. Quality control samples $n = 25$ and rejects the batch if $\bar{x}$ falls outside $500 \pm 3$ ml. Find the rejection probability when the machine is working correctly, and when $\mu$ drifts to 503 ml.

> [!example]- Solution
> $$\operatorname{SE} = \frac{8}{\sqrt{25}} = 1.6$$
>
> **When correct ($\mu = 500$)** — this is the **Type I error**, rejecting a good batch:
> $$Z = \frac{\pm 3}{1.6} = \pm 1.875$$
> $$P(\text{reject}) = 2\big(1 - \Phi(1.875)\big) = 2(1 - 0.9696) = \mathbf{0.0608}$$
> About **6% of good batches are rejected** — the producer's risk, and a direct cost of the rule.
>
> **When drifted ($\mu = 503$)** — now $\bar{X} \sim N(503, 1.6^2)$ and the fixed limits are 497 and 503:
> $$Z_{\text{upper}} = \frac{503 - 503}{1.6} = 0 \qquad Z_{\text{lower}} = \frac{497 - 503}{1.6} = -3.75$$
> $$P(\text{reject}) = P(Z > 0) + P(Z < -3.75) = 0.5 + 0.0001 = \mathbf{0.5001}$$
>
> **Only 50% of drifted batches are caught** — the **power** of the test. The other 50% pass, a **Type II error**. The reason is stark: the drifted mean sits *exactly on* the upper limit, so it is a coin flip.
>
> **How to improve it.** Increasing $n$ shrinks the SE and sharpens both errors: at $n = 100$, SE = 0.8, the false-alarm rate drops to 0.02% and power rises to ~99.99%. Widening the limits reduces false alarms but *lowers* power. **You cannot reduce both error types at fixed $n$** — that trade-off is the whole subject of [[07 - Hypothesis Testing - One Sample]].
>
> This is exactly the "acceptance interval" idea from slide 19, and it makes the sampling distribution's practical role concrete: it converts a claim about $\mu$ into a probability about observable $\bar{x}$.

## 📝 Summary

- **Population (parameters) → random sample $X_i$ (random variables) → observed sample $x_i$ (numbers).** Capital vs lowercase is the whole distinction.
- **A statistic is a random variable**, so it has a distribution — the *sampling distribution*.
- **$\mathbb{E}[\bar{X}] = \mu$ and $\operatorname{Var}(\bar{X}) = \sigma^2/n$** for any i.i.d. sample; $\sigma/\sqrt{n}$ is the **standard error**.
- **Normal population ⇒ $\bar{X}$ exactly normal, any $n$.**
- **Central Limit Theorem:** for large $n$ ($\ge 30$ conventionally), $\bar{X}$ is approximately normal **regardless of the population's shape**.
- **Precision improves with $\sqrt{n}$** — quadruple the sample to halve the error.
- **Sample proportion:** $\hat{p} \dot\sim N(p, p(1-p)/n)$, valid when $np \ge 5$ and $n(1-p) \ge 5$.
- **$\chi^2_k$** = sum of $k$ squared standard normals; non-negative, right-skewed; used for **variance**.
- **$t_k$** = normal ÷ √(χ²/k); symmetric with **heavier tails**; used for **means with unknown $\sigma$**; → normal as $k\to\infty$.
- **$\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}$** and **$\frac{\bar X - \mu}{s/\sqrt n} \sim t_{n-1}$.**

## ⚠️ Important Notes

**Do not confuse the population distribution with the sampling distribution.** The dice population is uniform; the distribution of $\bar{X}$ is triangular. They are different objects with different shapes and different variances.

**Standard deviation vs standard error.** $\sigma$ describes the spread of individual observations; $\sigma/\sqrt{n}$ describes the spread of the *sample mean*. The standard error shrinks with $n$; the standard deviation does not.

**The CLT applies to the sample mean, not the data.** A skewed population stays skewed no matter how large $n$ is. Only $\bar{X}$ becomes normal.

**$n \ge 30$ is a rule of thumb, not a theorem.** Severely skewed or heavy-tailed populations need considerably more; near-symmetric ones need far less.

**Independence is required for $\operatorname{Var}(\bar X) = \sigma^2/n$.** Clustered or autocorrelated samples have a larger true standard error, so intervals computed this way are too narrow and tests reject too often.

**Use $z$ when $\sigma$ is known, $t$ when it is estimated by $s$.** Using $z$ with an estimated $\sigma$ understates uncertainty — the error is largest at small $n$, exactly when it matters most.

**Degrees of freedom for the one-sample mean and variance are $n-1$**, not $n$ — the same correction as in $s^2$.

**Chi-squared is not symmetric**, so a two-sided interval for $\sigma^2$ needs **two different critical values** ($\chi^2_{\alpha/2}$ and $\chi^2_{1-\alpha/2}$), unlike the symmetric $\pm z$ or $\pm t$.

**The proportion's variance depends on $p$ itself**, which is unknown. This creates a circularity in interval construction that [[06 - Confidence Interval]] resolves by substituting $\hat p$. Note $p(1-p)$ is maximised at $p = 0.5$ — the worst case, used for conservative sample-size planning.

**Increasing $n$ improves precision but never fixes bias.** A biased sampling method converges confidently on the wrong answer — the *Literary Digest* lesson from [[01 - Introduction to Statistics]].

> [!warning] Gaps in the source slides
> **22 of 31 slides have only a title.** Everything mathematical is an embedded image. Specifically unrecoverable:
> - **Slides 2–5** — Population, Random/Observed Sample, Statistics, Sample Mean: **all definitions and notation**
> - **Slides 6, 12–13, 18** — Examples 4.1 (setup), 4.2, and 4.3. Only Example 4.1's two dice tables survived; **Examples 4.2 and 4.3 are lost entirely**
> - **Slides 8, 11** — the normal distribution and normality-of-population results
> - **Slides 14–16** — **the Central Limit Theorem statement and the "3 popular intervals"**. Given the CLT is the central result of the lecture, this is the most serious gap.
> - **Slides 17, 19** — sample proportion distribution; acceptance interval
> - **Slides 20–23** — chi-squared and Student distributions: densities, properties, tables
> - **Slides 25–26** — distribution of the sample variance
> - **Slides 10, 24** — the Excel function tables
> - **Slides 30–31** — the R random-sampling extension
>
> **Every formula in this note is the standard textbook result**, reconstructed from the slide titles and the summary slide. Verify notation against Devore Ch. 6. The **standard normal table (slide 9) is truncated at $z = 0.7$** in the deck.
>
> **Exercises set:** [1] Ch. 6 (p. 295) 1, 2, 5, 6; (p. 304) 11–13, 15, 16, 18, 19, 21, 22; (p. 312) 27–29, 33, 36, 38, 42; (p. 325) 47, 48, 56, 64, 68, 69, 71, 73, 74, 77 · [2] Sampling Distribution (p. 241, p. 258).

---
**Previous:** [[03 - Descriptive Statistics]] · **Next:** [[05 - Point Estimation]]
