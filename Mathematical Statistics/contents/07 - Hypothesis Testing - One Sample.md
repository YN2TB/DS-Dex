---
subject: Mathematical Statistics
chapter: 07
tags: [ds, statistics, hypothesis-testing, p-value, power, neyman-pearson]
source: "MS_Lec07_Test.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Hypothesis Testing — One Sample

> [!note] Reading
> **[1] Devore & Berk, Ch. 9, pp. 425–483** · **[2] Miller & Miller, Hypothesis Testing, pp. 337–390**
>
> The counterpart to [[06 - Confidence Interval]]: instead of estimating a parameter, we **decide** between two claims about it. Both rest on the same sampling distributions from [[04 - Sampling Distributions]], and a two-sided test at level $\alpha$ is exactly equivalent to checking whether the $(1-\alpha)$ CI contains the hypothesised value.

> [!warning] Source note
> Formulas are equation images, but **Examples 7.3, 7.5, 7.6 extracted in full**, along with the error-type table, the binomial table for Example 7.8, and the summary. Those examples are solved in the Exercises.

## 📘 Main Knowledge

### Hypotheses

- **$H_0$ (null hypothesis)** — the default claim, always containing an equality.
- **$H_1$ (alternative hypothesis)** — what we are trying to establish.

The three standard pairs:

| Type | $H_0$ | $H_1$ | Rejection region |
|---|---|---|---|
| Two-sided | $\mu = \mu_0$ | $\mu \ne \mu_0$ | both tails |
| Right-tailed | $\mu \le \mu_0$ | $\mu > \mu_0$ | right tail |
| Left-tailed | $\mu \ge \mu_0$ | $\mu < \mu_0$ | left tail |

**The claim you want to prove goes in $H_1$.** The logic is asymmetric by design: we assume $H_0$ and ask whether the data are too implausible under it. Failing to reject is *not* proof of $H_0$ — merely insufficient evidence against it.

### Types of error

| Decision | $H_0$ is True | $H_0$ is False |
|---|---|---|
| **Accept $H_0$** | Correct decision | **Type 2 error** ($\beta$) |
| **Reject $H_0$** | **Type 1 error** ($\alpha$) | Correct decision |

- **Type 1 error** — rejecting a true $H_0$ (a false positive). Its probability is the **significance level $\alpha$**, which *we choose*.
- **Type 2 error** — failing to reject a false $H_0$ (a false negative). Probability $\beta$.
- **Power** $= 1 - \beta$ — the probability of correctly rejecting a false $H_0$.

**At fixed $n$, reducing $\alpha$ increases $\beta$.** The only way to reduce both is to increase $n$.

### Testing procedure

1. State $H_0$ and $H_1$.
2. Choose the significance level $\alpha$.
3. Compute the **test statistic**.
4. Find the **critical value** / **rejection region**, or compute the **p-value**.
5. Decide: reject $H_0$ or do not reject.
6. Conclude in the language of the problem.

### The p-value

**The probability, assuming $H_0$ is true, of observing a test statistic at least as extreme as the one obtained.**

**Rule: reject $H_0$ if p-value $< \alpha$.**

| Test | p-value |
|---|---|
| Right-tailed | $P(Z > z_{obs})$ |
| Left-tailed | $P(Z < z_{obs})$ |
| Two-sided | $2P(Z > \lvert z_{obs}\rvert)$ |

The p-value is the **smallest $\alpha$ at which $H_0$ would be rejected**, which is why it is more informative than a bare reject/don't-reject verdict.

### Test for the mean

**$\sigma$ known (normal population, or large $n$):**
$$Z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}} \sim N(0,1) \text{ under } H_0$$

**$\sigma$ unknown (normal population):**
$$T = \frac{\bar{x} - \mu_0}{s/\sqrt{n}} \sim t_{n-1} \text{ under } H_0$$

Critical values: two-sided $\pm z_{\alpha/2}$; right-tailed $+z_\alpha$; left-tailed $-z_\alpha$.

### Test for variance — normal population

$$\chi^2 = \frac{(n-1)s^2}{\sigma_0^2} \sim \chi^2_{n-1} \text{ under } H_0$$

### Test for proportion — large sample

$$Z = \frac{\hat{p} - p_0}{\sqrt{p_0(1-p_0)/n}} \sim N(0,1) \text{ under } H_0$$

**Note the standard error uses $p_0$, not $\hat p$** — because under $H_0$ the proportion *is* $p_0$, so it is known. This differs from the confidence interval of [[06 - Confidence Interval]], which has no hypothesised value and must use $\hat p$. A frequently examined distinction.

### Test for proportion — small sample

With $n$ too small for the normal approximation, compute the p-value **exactly from the binomial distribution**. Slide 23 supplies the table for $B(n=20,\, p=0.3)$:

| $x$ | $P(X=x)$ | | $x$ | $P(X=x)$ |
|---|---|---|---|---|
| 0 | .0008 | | 8 | .1144 |
| 1 | .0068 | | 9 | .0654 |
| 2 | .0278 | | 10 | .0308 |
| 3 | .0716 | | 11 | .0120 |
| 4 | .1304 | | 12 | .0039 |
| 5 | .1789 | | 13 | .0010 |
| 6 | **.1916** | | 14 | .0002 |
| 7 | .1643 | | 15 | .0000 |

The p-value is a **sum of binomial probabilities** in the relevant tail.

### Most powerful test and the Neyman–Pearson Lemma

Among all tests with significance level $\le \alpha$, the **most powerful** test is the one maximising $1-\beta$ against a given alternative.

**Neyman–Pearson Lemma:** for testing a *simple* $H_0: \theta = \theta_0$ against a *simple* $H_1: \theta = \theta_1$, the most powerful test rejects $H_0$ when the **likelihood ratio** is small:

$$\Lambda = \frac{L(\theta_0)}{L(\theta_1)} \le k$$

with $k$ chosen so that $P(\Lambda \le k \mid H_0) = \alpha$.

This is a strong optimality result: it says the likelihood ratio is *the* right thing to look at, and no other test at the same $\alpha$ achieves higher power. It connects directly to the likelihood machinery of [[05 - Point Estimation]].

### Likelihood ratio test

The generalisation to composite hypotheses:

$$\Lambda = \frac{\max_{\theta \in \Theta_0} L(\theta)}{\max_{\theta \in \Theta} L(\theta)}$$

Reject $H_0$ for small $\Lambda$. **Wilks' theorem** gives the large-sample distribution $-2\ln\Lambda \xrightarrow{d} \chi^2_r$, where $r$ is the number of constrained parameters — which is why so many modern tests are chi-squared tests.

**The summary slide's checklist:** null and alternative hypotheses · Error Types 1 and 2 · reject vs not reject · significance level and power · rejection region and critical value · statistic value and p-value · tests for mean, proportion, and variance.

## ✏️ Exercises

*Examples 7.3, 7.5 and 7.6 below are the lecturer's own, extracted verbatim.*

**1.** *(Example 7.3)* Price is normal with variance 25 (\$²). A survey of 100 observations gives sample mean 24.
> (a) Test that average price is higher than 23, at 5% and 1%. Find the p-value. If the true mean is 24.8, find the power.
> (b) Test that average price is 24.5 at 5%, and find the p-value.
> (c) Find the p-value for the test that the mean is less than 25.5.

> [!example]- Solution
> $\sigma = 5$, $n = 100$, $\bar x = 24$, so $\operatorname{SE} = 5/10 = 0.5$. $\sigma$ known → $z$-test.
>
> **(a) Right-tailed.** $H_0: \mu \le 23$ vs $H_1: \mu > 23$.
> $$z = \frac{24 - 23}{0.5} = 2.0$$
> Critical values: $z_{0.05}=1.645$, $z_{0.01}=2.326$.
> - At 5%: $2.0 > 1.645$ → **reject $H_0$**.
> - At 1%: $2.0 < 2.326$ → **do not reject $H_0$**.
>
> $$p\text{-value} = P(Z > 2.0) = 1 - 0.9772 = \mathbf{0.0228}$$
> Consistent with both: $0.0228 < 0.05$ but $> 0.01$. **The same data give opposite verdicts at different $\alpha$** — which is exactly why the p-value is reported rather than a bare decision.
>
> **Power when $\mu = 24.8$.** The test rejects when $\bar{X} > 23 + 1.645(0.5) = 23.8225$. If truly $\bar{X} \sim N(24.8, 0.5^2)$:
> $$z = \frac{23.8225 - 24.8}{0.5} = -1.955$$
> $$\text{Power} = P(Z > -1.955) = \mathbf{0.9747}$$
> A 97.5% chance of detecting this alternative; $\beta = 2.5\%$.
>
> **(b) Two-sided.** $H_0: \mu = 24.5$ vs $H_1: \mu \ne 24.5$.
> $$z = \frac{24 - 24.5}{0.5} = -1.0$$
> $\lvert -1.0\rvert < 1.96$ → **do not reject**.
> $$p = 2P(Z > 1) = 2(0.1587) = \mathbf{0.3174}$$
>
> **(c) Left-tailed.** $H_0: \mu \ge 25.5$ vs $H_1: \mu < 25.5$.
> $$z = \frac{24 - 25.5}{0.5} = -3.0 \qquad p = P(Z < -3) = \mathbf{0.00135}$$
> Overwhelming evidence that the mean is below 25.5.

**2.** *(Example 7.5)* Income of 20 workers: sample mean 32, sample sd 4, income normal.
> (a) Test $\mu > 30$ at 5%. (b) Estimate the p-value from the $t$ table. (c) Find it in Excel. (d) At 10%, test $\mu = 33$. (e) At 1%, test $\mu < 34$.

> [!example]- Solution
> $s = 4$ is a **sample** sd → $t$-test with $df = 19$. $\operatorname{SE} = 4/\sqrt{20} = 0.8944$.
>
> **(a)** $H_0: \mu \le 30$ vs $H_1: \mu > 30$.
> $$t = \frac{32-30}{0.8944} = 2.236$$
> $t_{0.05,19} = 1.729$. Since $2.236 > 1.729$ → **reject $H_0$**; mean income exceeds 30.
>
> **(b) p-value from the table.** Bracket 2.236 in row $df=19$: $t_{0.025,19} = 2.093$ and $t_{0.01,19} = 2.539$. Since $2.093 < 2.236 < 2.539$:
> $$\mathbf{0.01 < p < 0.025}$$
> $t$ tables give only bracketing bounds — unlike the $z$ table, which gives exact values. That is the point of parts (b) and (c).
>
> **(c) Excel.** `=T.DIST.RT(2.236, 19)` → **0.0187**. (Legacy: `=TDIST(2.236,19,1)`.) Inside the bracket from (b). ✓
>
> **(d) Two-sided at 10%.** $H_0: \mu = 33$.
> $$t = \frac{32-33}{0.8944} = -1.118$$
> $t_{0.05,19} = 1.729$. $\lvert-1.118\rvert < 1.729$ → **do not reject**.
> $p = 2P(T_{19} > 1.118) \approx 2(0.1387) = \mathbf{0.277}$.
>
> **(e) Left-tailed at 1%.** $H_0: \mu \ge 34$ vs $H_1: \mu < 34$.
> $$t = \frac{32-34}{0.8944} = -2.236$$
> $-t_{0.01,19} = -2.539$. Since $-2.236 > -2.539$ → **do not reject at 1%** ($p \approx 0.0187$).
>
> Note (a) and (e) produce the same $\lvert t\rvert = 2.236$ and the same p-value, yet opposite conclusions — because $\alpha$ differs (5% vs 1%). **The evidence is identical; only the standard of proof changed.**

**3.** *(Example 7.6)* Same data (20 workers, mean 32, sd 4).
> (a) Test that the variance exceeds 10, at 5%. (b) Estimate the p-value from the χ² table. (c) Find it in Excel.

> [!example]- Solution
> **(a)** $H_0: \sigma^2 \le 10$ vs $H_1: \sigma^2 > 10$.
> $$\chi^2 = \frac{(n-1)s^2}{\sigma_0^2} = \frac{19 \times 16}{10} = \frac{304}{10} = 30.4$$
> Critical value $\chi^2_{0.05,19} = 30.144$. Since $30.4 > 30.144$ → **reject $H_0$** (only just).
>
> **(b) p-value from the table.** Row $df=19$: $\chi^2_{0.05,19} = 30.144$ and $\chi^2_{0.025,19} = 32.852$. Our 30.4 lies between them, so
> $$\mathbf{0.025 < p < 0.05}$$
>
> **(c) Excel.** `=CHISQ.DIST.RT(30.4, 19)` → **0.0476**. Just under 0.05 — consistent with the marginal rejection.
>
> **Two cautions.** This result is *borderline*: at $\alpha = 0.04$ we would not reject. Reporting "significant at 5%" without the p-value would badly overstate the strength of evidence.
>
> And this test **requires normality and is not protected by the CLT**. Unlike tests for the mean, χ² variance tests are highly sensitive to non-normal data — mild kurtosis can badly distort the true error rate. With $p = 0.0476$ against a threshold of 0.05, that fragility matters.

**4.** Explain the relationship between Type 1 and Type 2 errors, and why "accept $H_0$" is poor terminology.

> [!example]- Solution
> **The trade-off.** At fixed $n$, lowering $\alpha$ pushes the critical value further into the tail, so rejection requires stronger evidence — which necessarily means more false $H_0$s survive, i.e. $\beta$ rises. Exercise 1 shows it concretely: at $\alpha = 0.05$ we reject; at $\alpha = 0.01$ the same data do not. The second choice halves the false-positive risk and raises the false-negative risk.
>
> **Only increasing $n$ reduces both**, by shrinking the standard error so that true and hypothesised values separate more sharply.
>
> **Which error matters more is a domain question, not a statistical one.** In drug approval, Type 1 (approving an ineffective drug) is worse → small $\alpha$. In screening for a treatable cancer, Type 2 (missing a real case) is worse → larger $\alpha$ accepted for higher power.
>
> **Why "accept $H_0$" is poor terminology.** The test never provides evidence *for* $H_0$; it only fails to find evidence against it. Two very different situations produce the same non-rejection:
> - The null really is true.
> - The null is false but the test lacked **power** — $n$ too small, or the effect too subtle.
>
> In Exercise 2(d) we did not reject $\mu = 33$ with $\bar x = 32$ and $n = 20$. But we also would not reject $\mu = 32.5$, or $\mu = 33.5$. **A whole range of nulls survives** — precisely the confidence interval. Saying we "accept $\mu = 33$" would absurdly imply we had also accepted several incompatible values.
>
> Correct phrasing: **"do not reject $H_0$"** or "insufficient evidence to conclude $\mu \ne 33$." Absence of evidence is not evidence of absence.

**5.** (Advanced) State the Neyman–Pearson Lemma and explain why the likelihood ratio is the right criterion. Then explain the relationship between two-sided tests and confidence intervals.

> [!example]- Solution
> **Neyman–Pearson.** For simple $H_0: \theta = \theta_0$ against simple $H_1: \theta = \theta_1$, among all tests with size $\le \alpha$, the test rejecting when
> $$\Lambda = \frac{L(\theta_0)}{L(\theta_1)} \le k$$
> (with $k$ set so that $P(\Lambda \le k \mid H_0) = \alpha$) is **most powerful**.
>
> **Why the likelihood ratio is the right criterion.** $L(\theta_0)$ measures how well $\theta_0$ explains the data; $L(\theta_1)$ likewise for $\theta_1$. Their ratio is the *complete* comparison of the two hypotheses' ability to account for what was observed — every other feature of the data is irrelevant once you know it.
>
> There is a budget interpretation that makes the optimality intuitive. We may allocate probability $\alpha$ worth of sample space to the rejection region. To maximise power we should spend it on the outcomes that are **most likely under $H_1$ relative to $H_0$** — i.e. those with the smallest $\Lambda$. Ordering outcomes by $\Lambda$ and taking them greedily until the budget is exhausted is exactly what the lemma prescribes, and greedy allocation is optimal here for the same reason it is in a fractional knapsack.
>
> The **likelihood ratio test** generalises this to composite hypotheses by maximising $L$ over each hypothesis set, and **Wilks' theorem** ($-2\ln\Lambda \to \chi^2_r$) supplies its large-sample null distribution.
>
> **Two-sided tests and confidence intervals are equivalent.** The test does not reject $H_0: \mu = \mu_0$ at level $\alpha$ **if and only if** $\mu_0$ lies inside the $(1-\alpha)$ confidence interval.
>
> Both come from the same inequality:
> $$\left|\frac{\bar x - \mu_0}{s/\sqrt n}\right| < t_{\alpha/2} \quad\Longleftrightarrow\quad \bar x - t_{\alpha/2}\tfrac{s}{\sqrt n} < \mu_0 < \bar x + t_{\alpha/2}\tfrac{s}{\sqrt n}$$
> The left side is the test's non-rejection condition; the right side is the CI containing $\mu_0$. **They are the same statement rearranged.**
>
> Check with Exercise 2: the 95% CI is $32 \pm 2.093(0.8944) = (30.13,\, 33.87)$. In (d) we did not reject $\mu = 33$ — and indeed $33 \in (30.13, 33.87)$. ✓ We would also fail to reject 31, 32, or 33.8, all of which lie inside.
>
> **This is why the CI is the more informative report.** A test answers one question with one bit; the interval answers it for *every* candidate value at once, and displays the effect's magnitude and precision rather than just its statistical significance. The correspondence holds for two-sided tests; one-sided tests correspond to one-sided confidence bounds.

## 📝 Summary

- **$H_0$ contains the equality; the claim to be established goes in $H_1$.**
- **Type 1 = reject a true $H_0$ (probability $\alpha$, chosen); Type 2 = fail to reject a false $H_0$ (probability $\beta$). Power $= 1-\beta$.**
- **At fixed $n$, $\alpha$ and $\beta$ trade off.** Only larger $n$ improves both.
- **p-value** = probability under $H_0$ of a result at least as extreme. **Reject if $p < \alpha$.** It is the smallest $\alpha$ at which $H_0$ falls.
- **Mean:** $z = \frac{\bar x - \mu_0}{\sigma/\sqrt n}$ ($\sigma$ known) or $t = \frac{\bar x - \mu_0}{s/\sqrt n}$ on $n-1$ df.
- **Variance:** $\chi^2 = \frac{(n-1)s^2}{\sigma_0^2}$ on $n-1$ df, normality required.
- **Proportion:** $z = \frac{\hat p - p_0}{\sqrt{p_0(1-p_0)/n}}$ — **uses $p_0$, not $\hat p$**. Small samples use exact binomial probabilities.
- **Neyman–Pearson:** the likelihood ratio test is most powerful for simple vs simple hypotheses.
- **A two-sided test at $\alpha$ ⟺ whether the $(1-\alpha)$ CI contains $\mu_0$.**

## ⚠️ Important Notes

**Never "accept $H_0$" — say "do not reject".** Non-rejection may mean the null is true, or merely that the test lacked power. Many mutually incompatible nulls survive the same data.

**The proportion test uses $p_0$ in the standard error; the confidence interval uses $\hat p$.** Under $H_0$ the proportion is specified, so it is known. Mixing these up is a classic exam error.

**The p-value is not the probability that $H_0$ is true.** It is $P(\text{data this extreme} \mid H_0)$, not $P(H_0 \mid \text{data})$ — the same conditional inversion as the base rate fallacy in [[02 - Tables and Charts]].

**A significant result is not necessarily an important one.** With large $n$, a trivially small effect becomes statistically significant. Report the effect size and CI, not just $p$.

**Report the p-value, not just the verdict.** Exercise 1 rejects at 5% and not at 1% on identical data; $p = 0.0228$ conveys both at once.

**Borderline p-values deserve caution.** Example 7.6's $p = 0.0476$ is "significant at 5%" by 0.0024. Treating that as established fact overstates the evidence.

**Choose $\alpha$ before seeing the data.** Selecting the threshold afterwards to obtain significance is p-hacking, and it invalidates the error rate the test claims.

**The variance test requires normality and the CLT does not rescue it.** χ² tests on variance are far more fragile to non-normality than tests on the mean.

**$t$ tables give only bracketing bounds for p-values**, unlike the $z$ table. Use software (`T.DIST.RT`, `CHISQ.DIST.RT`) for exact values.

**Check whether the test is one- or two-sided before choosing the critical value.** "Higher than", "less than" → one-sided; "equals", "differs from" → two-sided. The two-sided p-value is double the one-sided.

**Multiple testing inflates the Type 1 rate.** Twenty independent tests at $\alpha=0.05$ yield roughly a 64% chance of at least one false positive. Adjust (Bonferroni or similar) when testing many hypotheses.

> [!warning] Gaps in the source slides
> Formulas are images throughout. **Titles only** on slides 2–4, 6–13, 15–16, 18, 20–22, 24–26 — specifically:
> - **Slides 2–3** — the definition of hypotheses and the parameter hypothesis pairs
> - **Slide 4 — Example 7.1: lost**
> - **Slides 6–7 — the testing procedure**
> - **Slides 8–11 — Example 7.2 and its solution: lost**
> - **Slides 12–13, 15–16** — the mean test statistics, rejection regions, and the p-value definition
> - **Slide 18 — the variance test statistic**
> - **Slides 20–22** — the proportion tests; **Example 7.7 lost**
> - **Slide 23 — Example 7.8**: the binomial table for $B(20, 0.3)$ extracted, but **the question itself is an image**, so the table cannot be used as intended
> - **Slides 24–26 — Most Powerful test, Neyman–Pearson Lemma, and the Likelihood Ratio test.** These are the actuarially examinable theory and are entirely images; my statements are reconstructed from standard sources.
>
> **Note the example numbering skips 7.4** — no slide bears that label, so an example appears to be missing from the deck.
>
> **Examples 7.3, 7.5, 7.6 extracted in full** and are solved above. Critical values are from standard tables — check against the tables permitted in your exam.
>
> **Exercises set:** [1] Ch. 9 (p. 434) 1, 2, 3, 9, 10, 11, 13; (p. 447) 15, 16, 19, 20, 21, 26, 27, 30, 33; (p. 454) 36–39, 42, 44; (p. 465) 45–49, 54, 55, 57; (p. 481) 72, 74, 75, 79, 88, 89 · [2] Ch. 12 + 13 (p. 345, 354, 369).

---
**Previous:** [[06 - Confidence Interval]] · **Next:** [[08 - Inferences on Two Samples]]
