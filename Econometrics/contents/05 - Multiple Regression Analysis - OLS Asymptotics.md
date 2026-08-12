---
subject: Econometrics
chapter: 05
tags: [ds, econometrics, consistency, asymptotic-normality, lagrange-multiplier, large-sample]
source: "documents/Wooldridge — *Introductory Econometrics: A Modern Approach*, 7th ed., Ch. 5 (pp. 163–180)"
---

# Multiple Regression Analysis: OLS Asymptotics

> [!abstract] Where this sits in the course
> [[04 - Multiple Regression Analysis - Inference]] bought exact $t$ and $F$ distributions at the price of **MLR.6 — normally distributed errors** — and immediately conceded that the assumption is often indefensible. **This chapter shows you do not need it.**
>
> Two results do the work: **consistency** ($\hat\beta_j\to\beta_j$ as $n\to\infty$) and **asymptotic normality** (the standardised $\hat\beta_j$ is approximately normal in large samples regardless of the distribution of $u$). Together they mean **everything in chapter 4 survives without MLR.6**, provided $n$ is large.

> [!note] Wooldridge's own note on this chapter
> *"Because the material in this chapter is more difficult to understand, and because one can conduct empirical work without a deep understanding of its contents, **this chapter may be skipped.**"*
>
> **But he immediately qualifies it:** the large-sample properties of OLS are referred to when studying **discrete response variables** ([[07 - Multiple Regression Analysis with Qualitative Information|ch. 7]]), when **relaxing homoskedasticity** ([[08 - Heteroskedasticity|ch. 8]]), and throughout **time series** (Part 2). *"Furthermore, **virtually all advanced econometric methods derive their justification using large-sample analysis.**"*

---

## 📘 Main Knowledge

### 1. Finite sample vs asymptotic properties

| **Finite sample** (small sample, exact) | **Asymptotic** (large sample) |
|---|---|
| Holds for **any** $n$ (subject to $n\ge k+1$) | Defined as **$n$ grows without bound** |
| **Unbiasedness** under MLR.1–4 | **Consistency** |
| **BLUE** under MLR.1–5 | **Asymptotic normality** |
| **Exact $t$ and $F$ distributions** under MLR.1–6 | **Approximate $t$ and $F$ distributions**, no MLR.6 needed |

> [!important] The practically important finding
> *"**Even without the normality assumption (MLR.6), $t$ and $F$ statistics have approximately $t$ and $F$ distributions, at least in large sample sizes.**"*
>
> This is what licenses everything applied econometricians actually do. **Without it, chapter 4's entire apparatus would rest on an assumption almost nobody believes.**

---

### 2. Consistency

> [!note] Why consistency, and not just unbiasedness
> *"Unbiasedness of estimators, although important, **cannot always be obtained.**"* Three examples the text gives:
> - **$\hat\sigma$ is not unbiased for $\sigma$** ([[02 - The Simple Regression Model|ch. 2]]) — only consistent.
> - **Time series regressions where OLS is not unbiased** ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]).
> - Several **biased yet useful** estimators in Part 3.
>
> *"Although not all useful estimators are unbiased, **virtually all economists agree that consistency is a minimal requirement.**"*
>
> **Nobel laureate Clive Granger:** *"If you can't get it right as $n$ goes to infinity, you shouldn't be in this business."* — *"The implication is that, if your estimator of a particular population parameter is not consistent, then **you are wasting your time.**"*

**The intuition.** For each $n$, $\hat\beta_j$ has a sampling distribution. **As $n$ grows, that distribution collapses onto $\beta_j$** — it becomes ever more tightly concentrated around the true value.

> [!important] **Theorem 5.1 — Consistency of OLS**
> **Under Assumptions MLR.1 through MLR.4, the OLS estimator $\hat\beta_j$ is consistent for $\beta_j$, for all $j=0,1,\dots,k$:**
> $$\operatorname{plim}\hat\beta_j = \beta_j$$

#### Proof in the simple regression case

Start exactly as for unbiasedness, then divide numerator and denominator by $n$:

$$
\hat\beta_1 = \beta_1 + \frac{n^{-1}\sum_{i}(x_{i1}-\bar x_1)u_i}{n^{-1}\sum_i(x_{i1}-\bar x_1)^2} \tag{5.2}
$$

*"Dividing both the numerator and denominator by $n$ does not change the expression but **allows us to directly apply the law of large numbers.**"* The two sample averages converge in probability to their population counterparts:

$$
\operatorname{plim}\hat\beta_1 = \beta_1 + \frac{\mathrm{Cov}(x_1,u)}{\mathrm{Var}(x_1)} = \beta_1 \quad\text{because } \mathrm{Cov}(x_1,u)=0 \tag{5.3}
$$

using the fact that **$\mathbb{E}(u\mid x_1)=0$ implies $x_1$ and $u$ are uncorrelated**, and $\mathrm{Var}(x_1)\neq0$ from MLR.3. $\blacksquare$

> [!tip] The trick worth remembering
> **Divide top and bottom by $n$ so that both become sample averages, then apply the law of large numbers.** This is the standard device in every asymptotic proof in econometrics, and it is why (5.2) looks almost identical to the unbiasedness derivation of [[02 - The Simple Regression Model|chapter 2]] equation (2.52).

#### A weaker assumption suffices

> [!important] **Assumption MLR.4′ — Zero mean and zero correlation**
> $$\mathbb{E}(u)=0 \quad\text{and}\quad \mathrm{Cov}(x_j,u)=0 \;\text{ for } j=1,\dots,k$$

*"MLR.4′ is **weaker** than MLR.4 in the sense that the latter implies the former. One way to characterise the zero conditional mean assumption is that **any function of the explanatory variables is uncorrelated with $u$.** MLR.4′ requires only that **each $x_j$** is uncorrelated with $u$."*

> [!note] Why the book uses MLR.4 anyway
> *"MLR.4′ is more natural an assumption because **it leads directly to the OLS estimates**"* — the first order conditions in [[03 - Multiple Regression Analysis - Estimation|(3.13)]] *"are simply the sample analogs of the population zero correlation assumptions."* And *"when we think about violations of MLR.4, we usually think in terms of $\mathrm{Cov}(x_j,u)\neq0$."*
>
> **The reason to keep MLR.4:** OLS is **biased (but consistent) under MLR.4′**. Unbiasedness needs the stronger conditional-mean version.
>
> **Practical upshot:** MLR.4′ is enough for consistency, so **consistency is a genuinely weaker demand than unbiasedness** — one more reason it is the "minimal requirement."

---

### 3. Inconsistency — when consistency fails

> [!important] The sentence to memorise
> > *"**If the error is correlated with any of the independent variables, then OLS is biased AND inconsistent.** This is very unfortunate because it means that **any bias persists as the sample size grows.**"*

From (5.3), whether or not $u$ and $x_1$ are uncorrelated:

$$
\boxed{\;\operatorname{plim}\hat\beta_1 - \beta_1 = \frac{\mathrm{Cov}(x_1,u)}{\mathrm{Var}(x_1)}\;} \tag{5.4}
$$

**This is the *inconsistency*, sometimes loosely called the asymptotic bias.**

- **Positive** if $x_1$ and $u$ are positively correlated; **negative** if negatively correlated.
- *"If the covariance between $x_1$ and $u$ is small relative to the variance in $x_1$, the inconsistency can be negligible; **unfortunately, we cannot even estimate how big the covariance is because $u$ is unobserved.**"*

#### The asymptotic omitted variable formula

If the true model is $y=\beta_0+\beta_1x_1+\beta_2x_2+v$ satisfying MLR.1–4, and we omit $x_2$ (so $u=\beta_2x_2+v$):

$$
\operatorname{plim}\tilde\beta_1 = \beta_1+\beta_2\delta_1 \tag{5.5}
\qquad\text{where}\qquad
\delta_1 = \frac{\mathrm{Cov}(x_1,x_2)}{\mathrm{Var}(x_1)} \tag{5.6}
$$

> [!important] Compare with the finite-sample bias formula
> | | [[03 - Multiple Regression Analysis - Estimation\|Chapter 3]] | Here |
> |---|---|---|
> | Quantity | $\mathrm{Bias}(\tilde\beta_1) = \beta_2\tilde\delta_1$ | $\operatorname{plim}\tilde\beta_1-\beta_1 = \beta_2\delta_1$ |
> | $\delta$ is | the **sample** regression slope of $x_2$ on $x_1$ | the **population** ratio $\mathrm{Cov}(x_1,x_2)/\mathrm{Var}(x_1)$ |
>
> *"For practical purposes, **we can view the inconsistency as being the same as the bias.** The difference is that the inconsistency is expressed in terms of the population variance and covariance, while the bias is based on their sample counterparts."*
>
> **So Table 3.2 — the sign table — applies unchanged.** Sign $\beta_2$, sign the correlation, multiply.

> [!warning] More data makes it worse, not better
> > *"An important point about inconsistency is that, **by definition, the problem does not go away by adding more observations.** If anything, **the problem gets worse with more data**: the OLS estimator gets closer and closer to $\beta_1+\beta_2\delta_1$ as the sample size grows."*
>
> **This is the most important practical implication of the chapter.** With a *variance* problem, more data helps ([[03 - Multiple Regression Analysis - Estimation|ch. 3]] §5: $\mathrm{se}\propto1/\sqrt n$). With an *endogeneity* problem, more data gives you **an ever more precise estimate of the wrong number** — and a shrinking confidence interval that excludes the truth with increasing confidence.
>
> **Big data does not solve endogeneity. It disguises it.**

#### One bad regressor contaminates all of them

*"If $x_1$ is correlated with $u$ but the other independent variables are uncorrelated with $u$, **all of the OLS estimators are generally inconsistent**"* — including the intercept.

**The one exception:** *"If $x_1$ and $x_2$ are uncorrelated, then any correlation between $x_1$ and $u$ does not result in the inconsistency of $\hat\beta_2$: $\operatorname{plim}\hat\beta_2=\beta_2$."*

**Generally:** if $x_1$ is correlated with $u$ **but $x_1$ and $u$ are uncorrelated with the other regressors**, then only $\hat\beta_1$ is inconsistent, with the inconsistency given by (5.4).

> [!note] This mirrors [[03 - Multiple Regression Analysis - Estimation|chapter 3]] §4 exactly
> **You cannot rescue "the coefficients I care about" by conceding one is endogenous.** Endogeneity is a property of the equation. The escape route — orthogonality among the regressors — is rarely available in practice, since regressors are usually correlated (that is why they are in the model).

---

### 4. Asymptotic normality

> *"Consistency of an estimator is an important property, but **it alone does not allow us to perform statistical inference.** Simply knowing that the estimator is getting closer to the population value does not allow us to test hypotheses."*

#### Why normality of $u$ often fails, concretely

Two of Wooldridge's own examples:

**Example — `narr86`, arrests of young men in 1986.** *"In the population, most men are not arrested during the year, and the vast majority are arrested one time at the most. (In the sample of 2,725 men in `CRIME1`, **fewer than 8% were arrested more than once**.) Because `narr86` takes on only two values for **92% of the sample**, it cannot be close to being normally distributed."*

**Example — `prate`, 401(k) participation rates.** *"The distribution is **heavily skewed to the right.** In fact, **over 40% of the observations are at the value 100**, indicating 100% participation. This violates the normality assumption **even conditional on the explanatory variables.**"*

> [!important] **Theorem 5.2 — Asymptotic normality of OLS**
> **Under the Gauss–Markov assumptions MLR.1–MLR.5** (note: **not** MLR.6):
> $$\sqrt{n}\,(\hat\beta_j-\beta_j) \;\xrightarrow{\;a\;}\; \mathrm{Normal}\!\left(0,\;\frac{\sigma^2}{a_j^2}\right)$$
> where $a_j^2 = \operatorname{plim}\big(n^{-1}\sum_i\hat r_{ij}^2\big)$, and $\hat r_{ij}$ are the residuals from regressing $x_j$ on the other regressors. Equivalently, **$\hat\beta_j$ is asymptotically normally distributed**, and
> $$\frac{\hat\beta_j-\beta_j}{\mathrm{se}(\hat\beta_j)} \;\xrightarrow{\;a\;}\; \mathrm{Normal}(0,1)$$
>
> **Also: $\hat\sigma^2$ is a consistent estimator of $\sigma^2$.**

*"Theorem 5.2 is useful because **the normality Assumption MLR.6 has been dropped**; the only restriction on the distribution of the error is that it has **finite variance**, something we will always assume."*

> [!warning] The most common misunderstanding of Theorem 5.2
> > *"It is important to keep separate the notions of **the population distribution of the error term $u$** and **the sampling distributions of the $\hat\beta_j$** as the sample size grows. **A common mistake is to think that something is happening to the distribution of $u$ — namely, that it is getting 'closer' to normal — as the sample size grows.** But remember that **the population distribution is immutable and has nothing to do with the sample size.**"*
>
> `narr86` takes small non-negative integer values **in the population**. *"Whether we sample 10 men or 1,000 men from this population obviously has no effect on the population distribution."*
>
> **What Theorem 5.2 actually says:** *"regardless of the population distribution of $u$, **the OLS estimators, when properly standardized, have approximate standard normal distributions.** This approximation comes about by the central limit theorem because **the OLS estimators involve — in a complicated way — the use of sample averages.**"*
>
> **The CLT acts on the estimator, not on the error.** That is the whole idea.

#### Consequences for $t$ and $F$

$$
\frac{\hat\beta_j-\beta_j}{\mathrm{se}(\hat\beta_j)} \;\overset{a}{\sim}\; t_{n-k-1} \tag{5.8}
$$

*"Because $t_{df}$ approaches the Normal(0,1) distribution as $df$ gets large, and because under the CLM assumptions the $t_{n-k-1}$ distribution holds exactly, **it makes sense to treat $(\hat\beta_j-\beta_j)/\mathrm{se}(\hat\beta_j)$ as a $t_{n-k-1}$ random variable generally, even when MLR.6 does not hold.**"*

> **"$t$ testing and the construction of confidence intervals are carried out exactly as under the classical linear model assumptions."** And *"the asymptotic normality of the OLS estimators also implies that **the $F$ statistics have approximate $F$ distributions** in large sample sizes."*

**So the `prate` and `narr86` analyses need not change at all** — *"in both cases, we have at least 1,500 observations, which is certainly enough to justify the approximation."*

> [!warning] Two crucial caveats
> **1. How large is "large"? Nobody can say.**
> > *"If the sample size is not very large, then the $t$ distribution can be a poor approximation... **there are no general prescriptions on how big the sample size must be.** Some econometricians think that $n=30$ is satisfactory, but **this cannot be sufficient for all possible distributions of $u$.**... **the quality of the approximation depends not just on $n$, but on the $df$, $n-k-1$: with more independent variables, a larger sample size is usually needed.**"*
>
> **2. The CLT does NOT rescue you from heteroskedasticity.**
> > *"It is very important to see that **Theorem 5.2 does require the homoskedasticity assumption** (along with the zero conditional mean assumption). **If $\mathrm{Var}(y\mid x)$ is not constant, the usual $t$ statistics and confidence intervals are invalid NO MATTER HOW LARGE THE SAMPLE SIZE IS; the central limit theorem does not bail us out when it comes to heteroskedasticity.**"*
>
> **This second point is worth its own line in your notes.** Asymptotics rescues you from **non-normality**, never from **heteroskedasticity** — which is precisely why [[08 - Heteroskedasticity|chapter 8]] exists as a separate chapter.

#### The $1/\sqrt n$ rule of thumb

$$
\mathrm{se}(\hat\beta_j) \approx \frac{c_j}{\sqrt n} \tag{5.10}
\qquad\text{where}\qquad
c_j = \frac{\sigma}{\sigma_j\sqrt{1-\rho_j^2}}
$$

with $\sigma=\mathrm{sd}(u)$, $\sigma_j=\mathrm{sd}(x_j)$, and $\rho_j^2$ the **population** $R$-squared from regressing $x_j$ on the other regressors.

**This is the population version of [[03 - Multiple Regression Analysis - Estimation|(3.59)]]** — same three drivers of precision (error variance, spread of $x_j$, collinearity), now as constants that do not depend on $n$.

> [!example] Example 5.2 — Standard errors in a birth weight equation
> Using `BWGHT` ($n=1{,}388$), regressing $\log(bwght)$ on `cigs` and $\log(faminc)$:
>
> | Sample | $\mathrm{se}(\hat\beta_{cigs})$ |
> |---|---|
> | First half ($n=694$) | $0.0013$ |
> | Full sample ($n=1{,}388$) | $0.00086$ |
>
> **Actual ratio:** $0.00086/0.0013 \approx \mathbf{0.662}$
> **Predicted by (5.10):** $\sqrt{694/1{,}388} = \sqrt{0.5} \approx \mathbf{0.707}$
>
> *"This percentage is pretty close to the 66.2% we actually compute."*
>
> **The rule of thumb: doubling the sample cuts standard errors by about 30%.** To halve them you need **four times** the data.

---

### 5. The Lagrange multiplier statistic

Once in the asymptotic realm, an alternative to the $F$ test becomes available for testing $q$ **exclusion restrictions**.

**The LM statistic (also the score statistic) procedure:**

1. **Regress $y$ on the restricted set of regressors** and save the residuals $\tilde u$.
2. **Regress $\tilde u$ on ALL the regressors** (restricted set *and* the excluded ones); obtain $R_u^2$.
3. Compute
$$
\boxed{\;LM = n\,R_u^2 \;\overset{a}{\sim}\; \chi^2_q\;}
$$
4. **Reject $H_0$ if $LM$ exceeds the $\chi^2_q$ critical value.**

> [!important] Why the auxiliary regression works
> Under $H_0$, the excluded variables have no partial effect, so **they should not help explain the residuals from the restricted model.** If they do — if $R_u^2$ is appreciably above zero — the restrictions are false.
>
> **This "regress the residuals on everything and use $nR^2$" construction is the single most reused device in the rest of the book.** You will meet it again as:
> - the **Breusch–Pagan test** for heteroskedasticity ([[08 - Heteroskedasticity|ch. 8]]),
> - the **White test** ([[08 - Heteroskedasticity|ch. 8]]),
> - the **Breusch–Godfrey test** for serial correlation ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]),
> - the **ARCH test** ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]], and [[Time-series Analysis/contents/09 - ARCH, GARCH and Extensions|Engle's LM test]]).
>
> **Learn the pattern once and you get four tests free.**

> [!note] LM vs $F$
> **Both are valid** for exclusion restrictions in large samples, and **they usually agree.** $F$ requires estimating both models; **LM requires only the restricted model plus one auxiliary regression** — an advantage when the unrestricted model is awkward to estimate.
>
> **In finite samples the $F$ statistic is generally preferred**, because it has an exact distribution under MLR.6 while LM is only ever asymptotic.

---

## ✏️ Exercises

> [!note] Constructed exercises — the textbook's require data files not in the vault.

### Exercise 1 — Consistency vs unbiasedness

Classify each statement as true or false, and explain.

(a) An unbiased estimator is always consistent.
(b) A consistent estimator is always unbiased.
(c) If $\mathrm{Cov}(x_1,u)\neq0$, collecting more data will eventually fix the problem.
(d) $\hat\sigma$ is an unbiased estimator of $\sigma$.
(e) OLS is consistent under MLR.1–MLR.4′ but may be biased.

> [!example]- Solution
> **(a) False.** Unbiasedness says $\mathbb{E}(\hat\theta)=\theta$ for every $n$; consistency says the distribution **collapses** onto $\theta$. An estimator can be unbiased with a variance that **does not shrink** — for example, using only the *first* observation, $\hat\mu = y_1$, is unbiased for $\mathbb{E}(y)$ but has variance $\sigma^2$ forever. **It never converges.**
>
> **(b) False.** *"In Part 3 of the text, we encounter several other estimators that are biased yet useful."* Instrumental variables (ch. 15) is the standard case: **biased in finite samples, consistent as $n\to\infty$** — and used precisely because OLS is *neither*.
>
> **(c) False, and this is the key point of §3.** *"**By definition, the problem does not go away by adding more observations.** If anything, the problem gets worse."* As $n\to\infty$, $\hat\beta_1\to\beta_1+\mathrm{Cov}(x_1,u)/\mathrm{Var}(x_1)$ — **a precise estimate of the wrong quantity**, with a confidence interval that shrinks around it.
>
> **More data cures variance, never bias.**
>
> **(d) False.** *"The standard error of the regression, $\hat\sigma$, is **not** an unbiased estimator for $\sigma$."* $\hat\sigma^2 = \text{SSR}/(n-k-1)$ **is** unbiased for $\sigma^2$, but the square root of an unbiased estimator is not unbiased for the square root (Jensen's inequality). **$\hat\sigma$ is consistent, which is why we use it anyway** — a good illustration of why consistency is the working standard.
>
> **(e) True.** MLR.4′ ($\mathbb{E}(u)=0$ and $\mathrm{Cov}(x_j,u)=0$) is **weaker** than MLR.4 ($\mathbb{E}(u\mid\mathbf{x})=0$). It delivers consistency but **not** unbiasedness: *"OLS turns out to be biased (but consistent) under MLR.4′."*
>
> **The general lesson:** consistency demands less than unbiasedness, which is exactly why Granger called it the **minimal** requirement.

---

### Exercise 2 — Compute an inconsistency

The true model is $\log(wage) = \beta_0+\beta_1educ+\beta_2abil+v$ with $\beta_2 = 0.012$. In the population, $\mathrm{Cov}(educ,abil) = 3.2$ and $\mathrm{Var}(educ) = 7.5$.

(a) Compute $\delta_1$ and the inconsistency in the simple regression estimator. (b) If the true $\beta_1 = 0.065$, what does $\hat\beta_1$ converge to? (c) A researcher with $n=50{,}000$ reports $\hat\beta_1 = 0.0762$ with $\mathrm{se}=0.0009$. Comment. (d) What if the researcher had $n=5$ million?

> [!example]- Solution
> **(a)** From (5.6):
> $$\delta_1 = \frac{\mathrm{Cov}(educ,abil)}{\mathrm{Var}(educ)} = \frac{3.2}{7.5} = \mathbf{0.4267}$$
> $$\text{Inconsistency} = \beta_2\delta_1 = 0.012\times0.4267 = \mathbf{0.005120}$$
>
> **(b)** $$\operatorname{plim}\tilde\beta_1 = \beta_1+\beta_2\delta_1 = 0.065+0.00512 = \mathbf{0.07012}$$
>
> So the simple regression converges to **about 7.0%** when the true causal return is **6.5%** — **an overstatement of about 7.9%** of the true value.
>
> **The sign is as expected:** $\beta_2>0$ (ability raises wages) and $\mathrm{Cov}>0$ (abler people get more education), so **upward inconsistency** — exactly the sign table of [[03 - Multiple Regression Analysis - Estimation|chapter 3]].
>
> **(c) This is the trap the exercise is built around.**
>
> The 95% CI is $0.0762\pm1.96(0.0009) = \mathbf{[0.0744,\;0.0780]}$ — **extremely tight**, and $t = 0.0762/0.0009 = 84.7$.
>
> **The estimate looks superb and is wrong.** The interval **excludes the true $\beta_1 = 0.065$ entirely**. It does contain the plim of $0.0701$… almost — and the small remaining gap is ordinary sampling noise.
>
> **The researcher would report, with enormous confidence, a return to education about 17% higher than the truth.**
>
> **(d) Five million observations makes it strictly worse.**
>
> By (5.10), $\mathrm{se}\propto1/\sqrt n$, so multiplying $n$ by 100 divides the standard error by 10: $\mathrm{se}\approx0.00009$, giving a CI of roughly $[0.0699,\;0.0703]$.
>
> **The interval now converges tightly on $0.0701$ — the plim — and excludes the true value $0.065$ by a margin of 60 standard errors.**
>
> > *"If anything, the problem gets worse with more data: the OLS estimator gets closer and closer to $\beta_1+\beta_2\delta_1$."*
>
> **The moral, stated as bluntly as possible:** a tiny standard error is evidence about **precision**, not about **truth**. In an endogenous regression, **massive $n$ produces a confidently reported wrong answer** — and every diagnostic on the printed output will look excellent.

---

### Exercise 3 — Asymptotic normality in practice

A researcher regresses `narr86` (number of arrests, 92% of which are 0 or 1) on several regressors with $n = 2{,}725$, and worries that the dependent variable is far from normal.

(a) Is MLR.6 satisfied? (b) Are the OLS estimates still unbiased? Still BLUE? (c) Can $t$ tests be used? (d) What if $n$ were 40 instead? (e) What if the errors were heteroskedastic with $n = 2{,}725$?

> [!example]- Solution
> **(a) No, clearly not.** *"Because `narr86` takes on only two values for 92% of the sample, **it cannot be close to being normally distributed in the population.**"* And since $y = \beta_0+\mathbf{x}\boldsymbol\beta+u$, a non-normal $y$ conditional on $\mathbf{x}$ means a non-normal $u$.
>
> **(b) Yes to both — normality was never needed for either.**
> - **Unbiasedness** requires MLR.1–4 only ([[03 - Multiple Regression Analysis - Estimation|Theorem 3.1]]).
> - **BLUE** requires MLR.1–5 only (Gauss–Markov).
>
> *"We know that normality plays no role in the unbiasedness of OLS, nor does it affect the conclusion that OLS is the best linear unbiased estimator."*
>
> **(c) Yes.** With $n=2{,}725$, Theorem 5.2 applies comfortably. *"Our analysis of dependent variables like `prate` and `narr86` does not have to change at all... in both cases we have at least 1,500 observations, which is certainly enough to justify the approximation."*
>
> **Use $t$ tests, CIs and $F$ tests exactly as in [[04 - Multiple Regression Analysis - Inference|chapter 4]].**
>
> **(d) With $n=40$, be cautious.**
>
> *"There are no general prescriptions on how big the sample size must be. Some econometricians think $n=30$ is satisfactory, but **this cannot be sufficient for all possible distributions of $u$.**"* And with a dependent variable this discrete and skewed, the CLT will converge **slowly**.
>
> Note also the $df$ point: *"the quality of the approximation depends not just on $n$, but on $n-k-1$."* With $n=40$ and 6 regressors, $df=33$ — **the approximation is doubly strained.**
>
> **Practical response:** report results with an explicit caveat, and consider a bootstrap or a model designed for count data (Poisson regression) rather than forcing OLS.
>
> **(e) Heteroskedasticity is a different problem entirely, and $n$ does not help.**
>
> > *"If $\mathrm{Var}(y\mid x)$ is not constant, the usual $t$ statistics and confidence intervals are invalid **no matter how large the sample size is**; the central limit theorem does not bail us out."*
>
> **And heteroskedasticity is essentially guaranteed here.** For a count variable bounded below by zero, the variance mechanically rises with the mean — the classic case where $\mathrm{Var}(y\mid\mathbf{x})$ depends on $\mathbf{x}$.
>
> **The fix is robust standard errors** ([[08 - Heteroskedasticity|chapter 8]]), not a bigger sample.
>
> ---
> **The summary this exercise is designed to produce:**
>
> | Problem | Does large $n$ fix it? |
> |---|---|
> | **Non-normal errors** | ✅ **Yes** — Theorem 5.2 |
> | **Heteroskedasticity** | ❌ **No** — needs robust SEs |
> | **Endogeneity** | ❌ **No — gets worse** |

---

### Exercise 4 — The $1/\sqrt n$ rule

A study reports $\mathrm{se}(\hat\beta_1) = 0.048$ with $n = 400$.

(a) Approximately what standard error would $n=1{,}600$ give? (b) What $n$ is needed to reach $\mathrm{se}=0.012$? (c) The point estimate is $\hat\beta_1 = 0.071$. Is it significant at 5% with $n=400$? At what $n$ would it become significant if the estimate stayed the same? (d) Comment on (c).

> [!example]- Solution
> **(a)** From (5.10), $\mathrm{se}\approx c/\sqrt n$, so
> $$\frac{\mathrm{se}_{1600}}{\mathrm{se}_{400}} = \sqrt{\frac{400}{1600}} = \sqrt{0.25} = 0.5
> \;\Longrightarrow\;
> \mathrm{se}_{1600} \approx 0.048\times0.5 = \mathbf{0.024}$$
> **Quadrupling $n$ halves the standard error.**
>
> **(b)** We need to divide 0.048 by 4:
> $$\frac{0.012}{0.048} = 0.25 = \sqrt{\frac{400}{n}}
> \;\Longrightarrow\;
> \frac{400}{n} = 0.0625
> \;\Longrightarrow\;
> n = \mathbf{6{,}400}$$
> **A sixteen-fold increase in data for a four-fold gain in precision.**
>
> **(c)** With $n=400$ and (say) $k=4$, $df=395$, so the 5% two-sided critical value is $\approx1.966$.
> $$t = \frac{0.071}{0.048} = \mathbf{1.48} \quad<1.966 \;\Longrightarrow\; \textbf{not significant}$$
>
> To reach $t=1.96$ with the estimate unchanged we need $\mathrm{se} = 0.071/1.96 = 0.03622$:
> $$\frac{0.03622}{0.048} = 0.7546 = \sqrt{\frac{400}{n}}
> \;\Longrightarrow\;
> n = \frac{400}{0.5695} \approx \mathbf{702}$$
>
> **About 700 observations — a 76% increase.**
>
> **(d) Two things are worth saying, and they pull in opposite directions.**
>
> **In favour of collecting more data.** The current CI is $0.071\pm1.966(0.048) = [-0.023,\;0.165]$ — **compatible with a large positive effect and with a modest negative one.** This is the situation described in [[04 - Multiple Regression Analysis - Inference|chapter 4]]: **"insignificant" here means *uninformative*, not "no effect."** Roughly 300 more observations would settle it.
>
> **The warning.** *Planning* to collect exactly enough data to cross $t=1.96$ is a form of $p$-hacking. **The honest procedure is to decide the sample size in advance** (a power calculation) and report whatever comes out.
>
> **And the deeper point:** this whole calculation assumes $\hat\beta_1$ is **consistent**. If $x_1$ is endogenous, going from 400 to 700 observations buys you a *significant* estimate of the **wrong** number — **which is worse than the insignificant one you started with**, because it will now be believed.

---

### Exercise 5 — The LM test

Test whether three variables can be excluded from a model with $n=500$ and $k=8$ in the unrestricted model.

(a) Describe the LM procedure step by step. (b) If the auxiliary regression gives $R_u^2 = 0.0182$, compute $LM$ and test at 5%. (c) Compare with the $F$ approach. (d) Why does this construction recur so often later in the book?

> [!example]- Solution
> **(a) The procedure.**
> 1. **Estimate the restricted model** — $y$ on the 5 retained regressors — and save residuals $\tilde u$.
> 2. **Regress $\tilde u$ on all 8 regressors** (the 5 retained plus the 3 excluded). Obtain $R_u^2$.
> 3. $LM = n\,R_u^2$.
> 4. Compare with $\chi^2_q$ where $q=3$.
>
> **(b)** $$LM = 500\times0.0182 = \mathbf{9.10}$$
>
> Critical values for $\chi^2_3$: **7.81** at 5%, **11.34** at 1%.
>
> $9.10 > 7.81$, so **reject $H_0$ at the 5% level** — the three variables are **jointly significant**. (Not at 1%; the $p$-value is about 0.028.)
>
> **(c) The $F$ approach** would require estimating **both** models and computing
> $$F = \frac{(R_{ur}^2-R_r^2)/3}{(1-R_{ur}^2)/491}$$
>
> **The two tests are asymptotically equivalent** and here would give the same verdict. The relationship is roughly $LM \approx qF$ for large $df$: $9.10/3 = 3.03$, against an $F_{3,491}$ 5% critical value of about 2.62 — **consistent.** ✓
>
> **When to prefer each:**
>
> | | Advantage |
> |---|---|
> | **LM** | Needs only the **restricted** model plus one auxiliary regression — valuable when the unrestricted model is hard to estimate |
> | **$F$** | Has an **exact** distribution under MLR.6; generally **preferred in finite samples** |
>
> **(d) Because the $nR^2$ construction generalises to any "does this extra structure matter?" question.**
>
> The logic is always the same: **estimate under the null, then check whether the thing you left out can explain the residuals.** If it can, the null is false.
>
> | Test | Regress residuals on… | Detects |
> |---|---|---|
> | **LM exclusion** (here) | the excluded regressors | omitted variables |
> | **Breusch–Pagan** ([[08 - Heteroskedasticity\|ch. 8]]) | $\hat u^2$ on the regressors | heteroskedasticity |
> | **White** ([[08 - Heteroskedasticity\|ch. 8]]) | $\hat u^2$ on regressors, squares, cross-products | general heteroskedasticity |
> | **Breusch–Godfrey** ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions\|ch. 12]]) | $\hat u_t$ on regressors and lagged residuals | serial correlation |
> | **Engle's ARCH** ([[Time-series Analysis/contents/09 - ARCH, GARCH and Extensions\|ch. 9]]) | $\hat u_t^2$ on lagged $\hat u^2$ | conditional heteroskedasticity |
>
> **Every one is $nR^2\sim\chi^2_q$ from an auxiliary regression on residuals.** Recognising the pattern turns five separate tests into one idea — and it is why this chapter, nominally "skippable," pays for itself.

---

## 📝 Summary

- **Finite sample properties** (unbiasedness, BLUE, exact $t$/$F$) hold for any $n$; **asymptotic properties** (consistency, asymptotic normality) are defined as $n\to\infty$. **The practically important finding is that $t$ and $F$ statistics work approximately even without MLR.6.**
- **Consistency is the minimal requirement** — *"if you can't get it right as $n$ goes to infinity, you shouldn't be in this business."* Not all useful estimators are unbiased ($\hat\sigma$ is not; IV is not), but virtually all must be consistent.
- **Theorem 5.1:** under MLR.1–MLR.4, $\operatorname{plim}\hat\beta_j=\beta_j$. The proof divides numerator and denominator by $n$ so the **law of large numbers** applies, giving $\operatorname{plim}\hat\beta_1 = \beta_1+\mathrm{Cov}(x_1,u)/\mathrm{Var}(x_1)$.
- **MLR.4′** ($\mathbb{E}(u)=0$ and $\mathrm{Cov}(x_j,u)=0$) is **weaker** than MLR.4 and suffices for consistency — though OLS is then **biased but consistent**.
- **Inconsistency** $= \mathrm{Cov}(x_1,u)/\mathrm{Var}(x_1)$. For an omitted variable, $\operatorname{plim}\tilde\beta_1 = \beta_1+\beta_2\delta_1$ with $\delta_1=\mathrm{Cov}(x_1,x_2)/\mathrm{Var}(x_1)$ — **the population version of the chapter 3 bias formula**, so the sign table is unchanged.
- **Inconsistency does not shrink with $n$ — it gets worse.** More data yields an ever more precise estimate of the wrong number. **One endogenous regressor generally makes all coefficients inconsistent.**
- **Theorem 5.2 — asymptotic normality:** under MLR.1–MLR.5 (**no MLR.6**), the standardised $\hat\beta_j$ is approximately standard normal, and $\hat\sigma^2$ is consistent. **The CLT acts on the estimator (which involves sample averages), not on the error distribution — which is fixed in the population.**
- **Consequently $t$ tests, CIs and $F$ tests proceed exactly as before.** But: **there is no universal rule for how large $n$ must be** (it depends on the distribution of $u$ and on $n-k-1$), and **asymptotics does not rescue you from heteroskedasticity — no sample size does.**
- $\mathrm{se}(\hat\beta_j)\approx c_j/\sqrt n$ with $c_j = \sigma/(\sigma_j\sqrt{1-\rho_j^2})$: **standard errors shrink at rate $1/\sqrt n$.** Verified in the birth weight example (0.662 actual vs 0.707 predicted).
- **The Lagrange multiplier test:** regress $y$ on the restricted set, save $\tilde u$, regress $\tilde u$ on **all** regressors, and use $LM = nR_u^2 \sim \chi^2_q$. **The $nR^2$-on-residuals construction recurs throughout the rest of the book.**

---

## ⚠️ Important Notes

> [!warning] More data cures variance, never bias
> $$\mathrm{se}\propto\frac1{\sqrt n} \quad\text{but}\quad \operatorname{plim}\tilde\beta_1-\beta_1 = \beta_2\delta_1 \;\text{ regardless of } n$$
> **With an endogenous regressor, a huge sample gives a very precise wrong answer** — and a confidence interval that confidently excludes the truth. **Never treat a small standard error as evidence of correctness.**

> [!warning] The CLT applies to the estimator, not to the errors
> *"A common mistake is to think that something is happening to the distribution of $u$ — namely, that it is getting 'closer' to normal — as the sample size grows."* **The population distribution of $u$ is immutable.** What becomes normal is the **sampling distribution of $\hat\beta_j$**, because OLS is built from sample averages.

> [!warning] Asymptotics does not fix heteroskedasticity
> *"If $\mathrm{Var}(y\mid x)$ is not constant, the usual $t$ statistics and confidence intervals are invalid **no matter how large the sample size is**."* Theorem 5.2 **requires MLR.5.** Large $n$ buys you freedom from MLR.6 and nothing else.

> [!note] Consistency is weaker than unbiasedness
> Unbiased ⇏ consistent (the variance may not shrink); consistent ⇏ unbiased (IV, and OLS under MLR.4′). **They are logically independent**, and consistency is the one econometrics insists on.

> [!tip] Learn the $nR^2$ auxiliary-regression pattern once
> **Estimate under the null → save residuals → regress them on what you left out → $nR^2\sim\chi^2_q$.** This single template gives you the LM exclusion test, Breusch–Pagan, White, Breusch–Godfrey and Engle's ARCH test.

> [!warning] Source-material note
> Written from the **Wooldridge 7th edition PDF** (pp. 163–180). Text extracts cleanly; **Figures 5.1 (collapsing sampling distributions) and 5.2 (the histogram of `prate`) are images**, described in the surrounding prose and reconstructed above.
>
> **Equations extract with mangled symbols** and have been transcribed by hand. **Theorem 5.2's formal statement is partly reconstructed** — the PDF's rendering of the asymptotic variance expression is badly garbled, so the version in §4 uses standard notation consistent with the text's verbal description and with equation (5.10), which does extract cleanly.
>
> **The LM test section (5-2a) is cut off mid-sentence in the extraction**; §5 above reconstructs the four-step procedure from standard sources. **Verify the steps against the textbook before relying on them.**
>
> **No data files are in the vault**; all exercises are my own construction with arithmetic verified. **No lecture slides exist for this subject** — see [[00-Index]] for the scope decision.

---

**Previous:** [[04 - Multiple Regression Analysis - Inference]] · **Next:** [[06 - Multiple Regression Analysis - Further Issues]] · **Index:** [[00-Index]]

#econometrics #consistency #asymptotic-normality #lagrange-multiplier #plim #large-sample
