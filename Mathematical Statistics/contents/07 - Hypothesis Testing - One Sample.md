---
subject: Mathematical Statistics
chapter: 07
tags: [ds, statistics, hypothesis-testing, p-value, power, neyman-pearson]
source: "MS_Lec07_Test.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Hypothesis Testing: One Sample

Reading: Devore & Berk ch. 9 (pp. 425–483); Miller & Miller, Hypothesis Testing, pp. 337–390. Instead of estimating a parameter ([[06 - Confidence Interval]]), we decide between two claims about it. A two-sided test at level α is equivalent to checking whether the $(1-\alpha)$ CI contains the hypothesized value.

> [!warning] Source note
> Formulas are images, but Examples 7.3, 7.5, 7.6, the error table, the binomial table for Example 7.8 and the summary extracted.

## 📘 Main Knowledge

### Hypotheses

- $H_0$ (null): the default claim, containing the equality.
- $H_1$ (alternative): what we want to establish.

| Type | $H_0$ | $H_1$ | Rejection region |
|---|---|---|---|
| two-sided | $\mu=\mu_0$ | $\mu\neq\mu_0$ | both tails |
| right-tailed | $\mu\le\mu_0$ | $\mu>\mu_0$ | right tail |
| left-tailed | $\mu\ge\mu_0$ | $\mu<\mu_0$ | left tail |

We assume $H_0$ and ask whether the data are too unlikely under it. Not rejecting is not proof of $H_0$.

### Errors

| Decision | $H_0$ true | $H_0$ false |
|---|---|---|
| accept $H_0$ | correct | Type 2 error (β) |
| reject $H_0$ | Type 1 error (α) | correct |

- Type 1: rejecting a true $H_0$; probability = significance level α (chosen).
- Type 2: not rejecting a false $H_0$; probability β. Power = $1-\beta$.
- At fixed $n$, lowering α raises β; only a larger $n$ reduces both.

### Procedure

1. State $H_0$, $H_1$. 2. Choose α. 3. Compute the test statistic. 4. Find the critical value/rejection region or the p-value. 5. Decide. 6. Conclude in the problem's terms.

### p-value

The probability, under $H_0$, of a statistic at least as extreme as observed. Reject $H_0$ if $p<\alpha$; $p$ is the smallest α at which $H_0$ would be rejected.

| Test | p-value |
|---|---|
| right-tailed | $P(Z>z_{obs})$ |
| left-tailed | $P(Z<z_{obs})$ |
| two-sided | $2P(Z>\lvert z_{obs}\rvert)$ |

### Test statistics

- Mean, σ known: $Z=(\bar x-\mu_0)/(\sigma/\sqrt n)\sim N(0,1)$ under $H_0$.
- Mean, σ unknown (normal population): $T=(\bar x-\mu_0)/(s/\sqrt n)\sim t_{n-1}$.
- Variance (normal population): $\chi^2=(n-1)s^2/\sigma_0^2\sim\chi^2_{n-1}$.
- Proportion (large $n$): $Z=(\hat p-p_0)/\sqrt{p_0(1-p_0)/n}$. The SE uses $p_0$ (known under $H_0$), unlike the CI, which uses $\hat p$.
- Proportion (small $n$): exact binomial p-values. Slide 23's table for $B(20, 0.3)$:

| $x$ | $P(X=x)$ | | $x$ | $P(X=x)$ |
|---|---|---|---|---|
| 0 | .0008 | | 8 | .1144 |
| 1 | .0068 | | 9 | .0654 |
| 2 | .0278 | | 10 | .0308 |
| 3 | .0716 | | 11 | .0120 |
| 4 | .1304 | | 12 | .0039 |
| 5 | .1789 | | 13 | .0010 |
| 6 | .1916 | | 14 | .0002 |
| 7 | .1643 | | 15 | .0000 |

The p-value is the sum of binomial probabilities in the relevant tail.

### Most powerful tests

**Neyman–Pearson lemma**: for simple $H_0:\theta=\theta_0$ vs simple $H_1:\theta=\theta_1$, the most powerful level-α test rejects when
$$\Lambda = \frac{L(\theta_0)}{L(\theta_1)} \le k,\qquad P(\Lambda\le k\mid H_0)=\alpha$$

**Likelihood ratio test** (composite hypotheses):
$$\Lambda = \frac{\max_{\theta \in \Theta_0} L(\theta)}{\max_{\theta \in \Theta} L(\theta)}$$
Reject for small Λ. Wilks: $-2\ln\Lambda\xrightarrow{d}\chi^2_r$ ($r$ = number of constrained parameters).

Summary slide: null and alternative; Type 1 and 2 errors; reject/not reject; significance level and power; rejection region and critical value; statistic and p-value; tests for mean, proportion, variance.

## ✏️ Exercises

Examples 7.3, 7.5 and 7.6 are the lecturer's.

**1.** (Example 7.3) Price is normal with variance 25; $n=100$, $\bar x=24$. (a) Test $\mu>23$ at 5% and 1%; p-value; power if $\mu=24.8$. (b) Test $\mu=24.5$ at 5%; p-value. (c) p-value for $\mu<25.5$.

> [!example]- Solution
> σ = 5 known, $SE=0.5$.
> (a) $z=(24-23)/0.5=2.0$. 5%: $2.0>1.645$, reject. 1%: $2.0<2.326$, don't reject. $p=P(Z>2)=0.0228$. Power: reject when $\bar X>23+1.645(0.5)=23.8225$; if $\mu=24.8$, $P(Z>(23.8225-24.8)/0.5)=P(Z>-1.955)=0.9747$.
> (b) $z=-1.0$, $|z|<1.96$, don't reject; $p=2(0.1587)=0.3174$.
> (c) $z=-3.0$, $p=0.00135$.

**2.** (Example 7.5) 20 workers: mean 32, sd 4, normal income. (a) Test $\mu>30$ at 5%. (b) p-value from the t table. (c) In Excel. (d) At 10%, test $\mu=33$. (e) At 1%, test $\mu<34$.

> [!example]- Solution
> $t$-test, df 19, $SE=4/\sqrt{20}=0.8944$.
> (a) $t=2.236>t_{0.05,19}=1.729$: reject.
> (b) $t_{0.025,19}=2.093<2.236<t_{0.01,19}=2.539$, so $0.01<p<0.025$.
> (c) `=T.DIST.RT(2.236, 19)` = 0.0188.
> (d) $t=-1.118$, $|t|<1.729$: don't reject; $p=0.277$.
> (e) $t=-2.236>-2.539$: don't reject at 1% ($p=0.0188$).
> (a) and (e) have the same evidence but different α, hence different verdicts.

**3.** (Example 7.6) Same data. (a) Test $\sigma^2>10$ at 5%. (b) p-value from the χ² table. (c) In Excel.

> [!example]- Solution
> (a) $\chi^2=19\cdot16/10=30.4>\chi^2_{0.05,19}=30.144$: reject, just.
> (b) Between 30.144 (0.05) and 32.852 (0.025): $0.025<p<0.05$.
> (c) `=CHISQ.DIST.RT(30.4, 19)` = 0.0469.
> A borderline result, and variance tests depend heavily on normality.

**4.** How are Type 1 and Type 2 errors related? Why is "accept $H_0$" poor wording?

> [!example]- Solution
> Lowering α moves the critical value outward, so more false nulls survive (β rises). Only a larger $n$ reduces both. Which error is worse depends on the context (drug approval: avoid Type 1; cancer screening: avoid Type 2).
>
> Non-rejection can mean $H_0$ is true or that the test lacked power. In 2(d) we don't reject μ = 33, but also not 32.5 or 33.5: a whole range survives (the CI). Say "do not reject $H_0$".

**5.** (Advanced) State Neyman–Pearson and explain why the likelihood ratio is the right criterion. How do two-sided tests relate to CIs?

> [!example]- Solution
> For simple vs simple hypotheses, rejecting when $L(\theta_0)/L(\theta_1)\le k$ is most powerful at level α. The ratio compares how well each hypothesis explains the data. With an α "budget" of sample space for the rejection region, power is maximized by spending it on outcomes most likely under $H_1$ relative to $H_0$, i.e. smallest Λ. The LRT extends this to composite hypotheses, with Wilks' χ² approximation.
>
> $\left|\frac{\bar x-\mu_0}{s/\sqrt n}\right|<t_{\alpha/2}\iff\bar x-t_{\alpha/2}\frac{s}{\sqrt n}<\mu_0<\bar x+t_{\alpha/2}\frac{s}{\sqrt n}$. In Exercise 2 the 95% CI is $32\pm2.093(0.8944)=(30.13,\ 33.87)$, which contains 33, so $\mu=33$ is not rejected. The CI reports the result for all candidate values at once, plus magnitude and precision.

## 📝 Summary

- $H_0$ contains the equality; the claim goes in $H_1$.
- Type 1 (α, chosen) and Type 2 (β); power $1-\beta$; at fixed $n$ they trade off.
- p-value: probability under $H_0$ of a result at least as extreme; reject if $p<\alpha$.
- Mean: $z$ (σ known) or $t_{n-1}$; variance: $\chi^2_{n-1}$ (normality); proportion: $z$ with $p_0$ in the SE; small samples: exact binomial.
- Neyman–Pearson: likelihood ratio tests are most powerful.
- Two-sided test at α ⟺ $(1-\alpha)$ CI contains $\mu_0$.

## ⚠️ Important Notes

1. Say "do not reject", not "accept".
2. Proportion tests use $p_0$ in the SE; CIs use $\hat p$.
3. The p-value is $P(\text{data this extreme}\mid H_0)$, not $P(H_0\mid\text{data})$.
4. Statistically significant ≠ important; report effect sizes and CIs.
5. Report the p-value, not just the verdict.
6. Treat borderline p-values (0.0469) with caution.
7. Choose α before seeing data.
8. Variance tests are fragile to non-normality.
9. t and χ² tables only bracket p-values; use software for exact values.
10. Check one- vs two-sided before choosing critical values.
11. Multiple testing: 20 tests at 5% give a 64% chance of at least one false positive; adjust (e.g. Bonferroni).

> [!warning] Gaps in the source slides
> - Slides 2–3 (hypotheses), 4 (Example 7.1), 6–7 (procedure), 8–11 (Example 7.2), 12–13, 15–16 (mean statistics, p-value), 18 (variance statistic), 20–22 (proportion tests, Example 7.7) and 24–26 (most powerful test, Neyman–Pearson, LRT) are images.
> - Slide 23 (Example 7.8): the binomial table extracted but the question is an image.
> - Numbering skips Example 7.4.
> - Corrected (2026-10-09): `CHISQ.DIST.RT(30.4, 19)` is 0.0469 (previously 0.0476).
> - Exercise set: [1] ch. 9 (p. 434) 1–3, 9–11, 13; (p. 447) 15, 16, 19–21, 26, 27, 30, 33; (p. 454) 36–39, 42, 44; (p. 465) 45–49, 54, 55, 57; (p. 481) 72, 74, 75, 79, 88, 89; [2] ch. 12–13 (pp. 345, 354, 369).

**Previous:** [[06 - Confidence Interval]] · **Next:** [[08 - Inferences on Two Samples]]
