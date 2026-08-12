---
subject: Econometrics
chapter: 04
tags: [ds, econometrics, hypothesis-testing, t-test, f-test, confidence-intervals, p-value]
source: "documents/Wooldridge — *Introductory Econometrics: A Modern Approach*, 7th ed., Ch. 4 (pp. 117–162)"
---

# Multiple Regression Analysis: Inference

> [!abstract] Where this sits in the course
> [[03 - Multiple Regression Analysis - Estimation]] gave us $\hat\beta_j$, showed it is unbiased, and derived its variance. **But a point estimate alone answers no question** — is 0.083 different from zero? From 0.10? Are these five variables jointly irrelevant?
>
> Answering requires the **full sampling distribution** of $\hat\beta_j$, not just its first two moments. This chapter adds one assumption to get it, then builds the entire testing apparatus: **$t$ tests** for single parameters, **confidence intervals**, and **$F$ tests** for multiple restrictions.

---

## 📘 Main Knowledge

### 1. The normality assumption and the CLM

> *"Knowing the expected value and variance of the OLS estimators is useful for describing the precision... However, in order to perform statistical inference, we need to know more than just the first two moments of $\hat\beta_j$; we need to know the **full sampling distribution**. **Even under the Gauss-Markov assumptions, the distribution of $\hat\beta_j$ can have virtually any shape.**"*

> [!important] **Assumption MLR.6 — Normality**
> **The population error $u$ is independent of the explanatory variables $x_1,\dots,x_k$ and is normally distributed with zero mean and variance $\sigma^2$:**
> $$u \sim \mathrm{Normal}(0,\sigma^2)$$

> [!warning] MLR.6 is much stronger than everything before it
> *"Because $u$ is **independent** of the $x_j$ under MLR.6, $\mathbb{E}(u\mid x_1,\dots,x_k)=\mathbb{E}(u)=0$ and $\mathrm{Var}(u\mid x_1,\dots,x_k)=\mathrm{Var}(u)=\sigma^2$. Thus, **if we make Assumption MLR.6, then we are necessarily assuming MLR.4 and MLR.5.**"*
>
> MLR.6 therefore **implies** both the zero conditional mean assumption and homoskedasticity, and adds a distributional shape on top.

**MLR.1–MLR.6 are the classical linear model (CLM) assumptions.** Compactly:

$$
y\mid\mathbf{x} \sim \mathrm{Normal}(\beta_0+\beta_1x_1+\cdots+\beta_kx_k,\;\sigma^2)
$$

> [!note] A stronger efficiency result comes free
> Under the CLM assumptions, *"the OLS estimators are the **minimum variance unbiased estimators**, which means that OLS has the smallest variance among unbiased estimators; **we no longer have to restrict our comparison to estimators that are linear in the $y_i$.**"*
>
> Compare the Gauss–Markov theorem of [[03 - Multiple Regression Analysis - Estimation]], which was restricted to *linear* unbiased estimators. **Normality upgrades BLUE to MVUE.**

#### Is normality plausible?

The usual defence: *"because $u$ is the sum of many different unobserved factors affecting $y$, we can invoke the **central limit theorem** to conclude that $u$ has an approximate normal distribution."*

> [!warning] Two weaknesses in that argument
> **1.** *"The factors in $u$ can have very different distributions in the population (for example, ability and quality of schooling in the error in a wage equation). Although the CLT can still hold in such cases, **the normal approximation can be poor** depending on how many factors appear in $u$ and how different their distributions are."*
>
> **2. The more serious problem:** *"it assumes that **all unobserved factors affect $y$ in a separate, additive fashion.** Nothing guarantees that this is so. If $u$ is a complicated function of the unobserved factors, then the CLT argument does not really apply."*
>
> **And a concrete failure:** *"there is no theorem that says wage conditional on $educ$, $exper$, and $tenure$ is normally distributed. If anything, simple reasoning suggests the opposite is true: **because wage can never be less than zero, it cannot, strictly speaking, have a normal distribution.**"*
>
> **The standard fix** is to take logs — $\log(wage)$ is unbounded below and empirically much closer to normal, which is one more reason logs are ubiquitous in applied work ([[02 - The Simple Regression Model]] §5).

> [!important] Normality is not needed in large samples
> This is the reassuring part, developed fully in [[05 - Multiple Regression Analysis - OLS Asymptotics]]: **the normality of the OLS estimators is still approximately true in large samples even without normality of the errors.** MLR.6 buys **exact** finite-sample distributions; asymptotics gives you **approximate** ones without it.

---

### 2. The $t$ test

> [!important] **Theorem 4.2 — $t$ distribution for the standardised estimators**
> **Under the CLM assumptions MLR.1–MLR.6:**
> $$\boxed{\;\frac{\hat\beta_j-\beta_j}{\mathrm{se}(\hat\beta_j)} \sim t_{n-k-1} = t_{df}\;} \tag{4.3}$$
> **where $k+1$ is the number of unknown parameters ($k$ slopes plus the intercept) and $n-k-1$ is the degrees of freedom.**

> [!note] Why $t$ rather than normal
> Theorem 4.1 gives $(\hat\beta_j-\beta_j)/\mathrm{sd}(\hat\beta_j)\sim\mathrm{Normal}(0,1)$ — using the **true** standard deviation. Theorem 4.2 replaces it with the **estimated** standard error, and **estimating $\sigma$ costs the extra variability that turns the normal into a $t$.** Same logic as the one-sample $t$ test in [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|introductory statistics]].
>
> As $n-k-1$ grows the $t$ converges to the standard normal — which is why the distinction stops mattering above roughly 120 degrees of freedom.

#### The most common null

$$
H_0: \beta_j = 0 \tag{4.4}
$$

**meaning: once $x_1,\dots,x_{j-1},x_{j+1},\dots,x_k$ have been controlled for, $x_j$ has no partial effect on $y$.** The test statistic is the ***t* statistic**:

$$
\boxed{\;t_{\hat\beta_j} = \frac{\hat\beta_j}{\mathrm{se}(\hat\beta_j)}\;} \tag{4.5}
$$

> [!warning] Keep the sign
> *"Some treatments define the $t$ statistic as the **absolute value** of (4.5)... **This practice has the drawback of making testing against one-sided alternatives clumsy.** Throughout this text, the $t$ statistic always has the same sign as the corresponding OLS coefficient estimate."*

#### One-sided alternatives

$$
H_1: \beta_j > 0 \tag{4.6}
$$

*"When we state the alternative as in (4.6), we are really saying that the null hypothesis is $H_0:\beta_j\le0$... **the null value that is hardest to reject is $\beta_j=0$.** In other words, if we reject the null $\beta_j=0$ then we automatically reject $\beta_j<0$."*

**Rejection rule:** choose a **significance level** — *"the probability of rejecting $H_0$ when it is in fact true"* — find the critical value $c$ from $t_{n-k-1}$, and **reject if $t_{\hat\beta_j} > c$.**

#### Two-sided alternatives

$$
H_1: \beta_j \neq 0 \tag{4.10}
$$

**Reject if $|t_{\hat\beta_j}| > c$**, where $c$ is now the $(1-\alpha/2)$ percentile. *"With 25 df, the 5% two-sided critical value is 2.06."*

> [!warning] Never choose the alternative after seeing the estimate
> *"Even when we know whether $\beta_j$ is positive or negative under the alternative, **a two-sided test is often prudent.** At a minimum, using a two-sided alternative prevents us from looking at the estimated equation and then basing the alternative on whether $\hat\beta_j$ is positive or negative."*
>
> *"Using the regression estimates to help us formulate the null or alternative hypotheses **is not allowed**, because classical statistical inference presumes that we state the null and alternative about the population **before looking at the data.**"*
>
> **This is a real and common form of $p$-hacking.** Switching to a one-sided test after seeing the sign halves your $p$-value for free — and invalidates it.

**Language:** when $H_0:\beta_j=0$ is rejected, we say *"$x_j$ is **statistically significant** at the $\alpha$ level"*; when not rejected, *"$x_j$ is statistically insignificant."*

#### Testing other hypotheses

The general $t$ statistic:

$$
t = \frac{\text{estimate}-\text{hypothesised value}}{\text{standard error}} = \frac{\hat\beta_j-a_j}{\mathrm{se}(\hat\beta_j)} \tag{4.13}
$$

**The usual $t$ statistic is the case $a_j=0$.**

> [!example] Example 4.4 — Campus crime and enrolment
> $$\log(crime) = \beta_0+\beta_1\log(enroll)+u$$
> *"It is not much use to test $H_0:\beta_1=0$, as we expect the total number of crimes to increase as the size of the campus increases. **A more interesting hypothesis is that the elasticity is one: $H_0:\beta_1=1$.** This means that a 1% increase in enrolment leads to, on average, a 1% increase in crime."*
>
> *"A noteworthy alternative is $H_1:\beta_1>1$, which implies that a 1% increase in enrolment increases campus crime by **more than 1%.** If $\beta_1>1$, then, in a relative sense — not just an absolute sense — crime is more of a problem on larger campuses."*
>
> **This is the example to remember for why $H_0:\beta_j=0$ is often the wrong null.** Testing against zero here is testing something nobody doubts; the economically interesting question is whether the elasticity exceeds one.

#### $p$-values

> *"Even after deciding on the appropriate alternative..."* the classical approach requires picking a significance level in advance. **The $p$-value avoids that.**

$$
p\text{-value} = P(|T| > |t|) \tag{4.15}
$$

where $T\sim t_{n-k-1}$ and $t$ is the computed statistic.

**Reject $H_0$ at level $\alpha$ if and only if $p < \alpha$.**

> [!note] What the printed $p$-value tests
> *"If a regression package reports a $p$-value along with the standard OLS output, **it is almost certainly the $p$-value for testing $H_0:\beta_j=0$ against the TWO-SIDED alternative.**"* For a one-sided test, halve it (provided the estimate has the sign of the alternative).
>
> **A $p$-value is the smallest significance level at which you would reject.** It is *not* the probability that $H_0$ is true — a distinction worth stating precisely in exam answers.

---

### 3. Confidence intervals

From Theorem 4.2, a **95% confidence interval** for $\beta_j$:

$$
\boxed{\;\hat\beta_j \pm c\cdot\mathrm{se}(\hat\beta_j)\;} \tag{4.16}
$$

**where $c$ is the 97.5th percentile of $t_{n-k-1}$.** For $df=25$, $c=2.06$, giving $[\hat\beta_j-2.06\,\mathrm{se},\;\hat\beta_j+2.06\,\mathrm{se}]$.

> [!warning] What a confidence interval means — and does not
> *"**If random samples were obtained over and over again**, with $\underline\beta_j$ and $\overline\beta_j$ computed each time, then the (unknown) population value $\beta_j$ would lie in the interval for 95% of the samples. **Unfortunately, for the single sample that we use to construct the CI, we do not know whether $\beta_j$ is actually contained in the interval.** We hope we have obtained a sample that is one of the 95%, **but we have no guarantee.**"*
>
> **It is wrong to say "there is a 95% probability that $\beta_j$ lies in this interval."** $\beta_j$ is a fixed constant; the *interval* is random. **The 95% is a property of the procedure, exactly as unbiasedness was in [[02 - The Simple Regression Model]].**

> [!important] CIs and two-sided tests are the same thing
> **$H_0:\beta_j=a_j$ is rejected at the 5% level against a two-sided alternative if and only if $a_j$ lies outside the 95% confidence interval.**
>
> So a CI performs **infinitely many two-sided tests at once** — one for every candidate value of $a_j$ — which is why reporting a CI is usually more informative than reporting a single $p$-value.

---

### 4. Testing a single hypothesis involving several parameters

Sometimes the hypothesis links two coefficients, e.g.

$$
H_0: \beta_1 = \beta_2 \quad\Longleftrightarrow\quad H_0: \beta_1-\beta_2 = 0
$$

The $t$ statistic is

$$
t = \frac{\hat\beta_1-\hat\beta_2}{\mathrm{se}(\hat\beta_1-\hat\beta_2)}
$$

but the standard error is **not** obtainable from the printed output, because

$$
\mathrm{se}(\hat\beta_1-\hat\beta_2) = \sqrt{\mathrm{Var}(\hat\beta_1)+\mathrm{Var}(\hat\beta_2)-2\,\mathrm{Cov}(\hat\beta_1,\hat\beta_2)}
$$

**and the covariance is not usually reported.**

> [!tip] The reparameterisation trick — always works, needs no extra output
> Define $\theta_1 = \beta_1-\beta_2$, so $\beta_1 = \theta_1+\beta_2$. Substituting into
> $$y = \beta_0+\beta_1x_1+\beta_2x_2+\cdots+u$$
> gives
> $$y = \beta_0+\theta_1x_1+\beta_2\underbrace{(x_1+x_2)}_{\text{new regressor}}+\cdots+u$$
>
> **Run this regression and read $\theta_1$ and its standard error straight off the output.** Testing $H_0:\theta_1=0$ is exactly testing $H_0:\beta_1=\beta_2$.
>
> **This trick generalises to any single linear restriction** and is far less error-prone than hunting for covariances.

---

### 5. Testing multiple restrictions: the $F$ test

The central problem: **can a *group* of variables be dropped?**

$$
H_0: \beta_{k-q+1}=0,\;\dots,\;\beta_k=0
$$

— **$q$ exclusion restrictions.** The full model is the **unrestricted** model; dropping the $q$ variables gives the **restricted** model.

$$
\boxed{\;F \equiv \frac{(\text{SSR}_r-\text{SSR}_{ur})/q}{\text{SSR}_{ur}/(n-k-1)}\;} \tag{4.37}
$$

> [!important] Reading the $F$ statistic
> **Numerator:** the *increase* in SSR from imposing the restrictions, per restriction. **Denominator:** $\hat\sigma^2$ from the unrestricted model.
>
> So $F$ asks: **how much worse does the model fit when the restrictions are imposed, relative to the noise level?**
>
> - $q$ = **numerator degrees of freedom** = number of restrictions = $df_r - df_{ur}$
> - $n-k-1$ = **denominator degrees of freedom** = $df_{ur}$
>
> **Under $H_0$, $F\sim F_{q,\,n-k-1}$.** Reject if $F>c$; the test is **always one-sided** (large $F$ means the restrictions hurt).

> [!warning] $F$ is always non-negative
> *"Because $\text{SSR}_r$ can be no smaller than $\text{SSR}_{ur}$, **the $F$ statistic is always nonnegative** (and almost always strictly positive). Thus, **if you compute a negative $F$ statistic, then something is wrong**; the order of the SSRs in the numerator has been reversed."*
>
> (SSR cannot fall when restrictions are imposed, for the same reason $R^2$ cannot fall when variables are added — [[03 - Multiple Regression Analysis - Estimation]] §2.)

#### The $R$-squared form

Since $\text{SSR}_r = \text{SST}(1-R_r^2)$ and $\text{SSR}_{ur}=\text{SST}(1-R_{ur}^2)$, the SST terms cancel:

$$
\boxed{\;F = \frac{(R_{ur}^2-R_r^2)/q}{(1-R_{ur}^2)/(n-k-1)}\;} \tag{4.41}
$$

*"Because the $R$-squared is reported with almost all regressions (whereas the SSR is not), it is easy to use the $R$-squareds... **Particular attention should be paid to the order: the unrestricted $R$-squared comes first.**"*

> [!warning] The $R^2$ form only works for **exclusion** restrictions
> *"Although (4.41) is very convenient for testing exclusion restrictions, **it cannot be applied for testing all linear restrictions.** As we will see when we discuss testing general linear restrictions, **the sum of squared residuals form of the $F$ statistic is sometimes needed.**"*
>
> The reason: restrictions such as $\beta_1+\beta_2=1$ change the dependent variable in the restricted regression, so SST differs and the cancellation fails. **When in doubt, use the SSR form.**

#### Why $F$ is not the same as several $t$ tests

> [!important] The single most important conceptual point in the chapter
> Individual $t$ tests and the joint $F$ test **can disagree in both directions**, and neither is "wrong":
>
> | Situation | Explanation |
> |---|---|
> | **All $t$'s insignificant, $F$ significant** | **Multicollinearity.** Each variable is imprecisely estimated *individually* because the others explain it ($R_j^2$ near 1 — [[03 - Multiple Regression Analysis - Estimation]] §5), **but jointly they clearly matter.** |
> | **Some $t$ significant, $F$ insignificant** | The one strong variable is diluted by several useless ones; $q$ is large and the average improvement per restriction is small. |
>
> *"If one variable is significant and it is tested jointly with another set of variables, the set will be jointly significant. In such cases, **there is no logical inconsistency in rejecting both null hypotheses.**"*
>
> **They answer different questions.** A $t$ test asks "does *this* variable matter, given the others?"; the $F$ test asks "does *this group* matter, given the rest?" **When variables are collinear, the group can matter even though no member is individually identifiable.**

#### The overall significance of the regression

The special case $q=k$ — all slopes zero:

$$
H_0: \beta_1=\beta_2=\cdots=\beta_k=0
\qquad\Longrightarrow\qquad
F = \frac{R^2/k}{(1-R^2)/(n-k-1)}
$$

**This is the "$F$ statistic" printed by every regression package.** Note it uses the model's own $R^2$, since the restricted model has $R_r^2=0$.

---

### 6. Statistical vs practical significance

> [!important] The distinction that separates good applied work from bad
> **A coefficient can be statistically significant and economically trivial**, or **economically large and statistically insignificant.**
>
> $$t = \frac{\hat\beta_j}{\mathrm{se}(\hat\beta_j)} = \frac{\hat\beta_j\sqrt{n}\,\mathrm{sd}(x_j)\sqrt{1-R_j^2}}{\hat\sigma}$$
>
> From [[03 - Multiple Regression Analysis - Estimation]] equation (3.59), **$\mathrm{se}(\hat\beta_j)\to0$ at rate $1/\sqrt n$.** So with a large enough sample, **any non-zero $\beta_j$ becomes statistically significant**, however small.
>
> **The right procedure:**
> 1. Look at the **magnitude** of $\hat\beta_j$ first — is the effect economically meaningful at a plausible change in $x_j$?
> 2. Then look at the $t$ statistic to judge how precisely it is estimated.
> 3. **Report a confidence interval**, which conveys both at once.
>
> **A large $t$ with a tiny coefficient means you have precisely estimated something that does not matter.** A small $t$ with a large coefficient means the data cannot resolve something that would matter a great deal — an argument for **more data**, not for concluding "no effect."

> [!warning] "Insignificant" ≠ "zero"
> Failing to reject $H_0:\beta_j=0$ means **the data cannot distinguish $\beta_j$ from zero** — not that it is zero. A confidence interval of $[-0.02,\,0.60]$ is "insignificant" and **also compatible with a very large effect.** Say so.

---

## ✏️ Exercises

> [!note] The textbook's computer exercises require data files not in the vault. These are my own construction.

### Exercise 1 — $t$ tests, one- and two-sided

A wage regression on $n=526$ workers with $k=3$ regressors gives
$$\widehat{\log(wage)} = 0.284 + 0.092\,educ + 0.0041\,exper + 0.022\,tenure$$
$$\phantom{\widehat{\log(wage)} = 0.284} (0.104)\;\;(0.0073)\;\;\;\;\;\;(0.0017)\;\;\;\;\;\;(0.0031)$$
(standard errors in parentheses).

(a) Test $H_0:\beta_{educ}=0$ against a two-sided alternative at 5%. (b) Test $H_0:\beta_{exper}=0$ against $H_1:\beta_{exper}>0$ at 5%. (c) Test $H_0:\beta_{educ}=0.10$ against a two-sided alternative. (d) Construct a 95% CI for $\beta_{tenure}$ and interpret.

> [!example]- Solution
> **Degrees of freedom:** $n-k-1 = 526-3-1 = \mathbf{522}$. With $df$ this large the $t$ is essentially standard normal: two-sided 5% critical value $\approx 1.96$; one-sided 5% $\approx 1.645$.
>
> **(a)** $$t = \frac{0.092}{0.0073} = \mathbf{12.60}$$
> $12.60 \gg 1.96$, so **reject $H_0$ decisively** ($p < 0.0001$). **Education is statistically significant at any conventional level.**
>
> **(b)** $$t = \frac{0.0041}{0.0017} = \mathbf{2.41}$$
> $2.41 > 1.645$, so **reject $H_0$** in favour of $\beta_{exper}>0$. The one-sided $p$-value is about $0.008$.
>
> *(Note the two-sided $p$-value would be $0.016$ — still significant at 5%, so here the choice does not change the verdict. **But you must fix the alternative before looking.**)*
>
> **(c)** Using the general form (4.13):
> $$t = \frac{0.092-0.10}{0.0073} = \frac{-0.008}{0.0073} = \mathbf{-1.10}$$
> $|-1.10| < 1.96$, so **fail to reject.** The data are **entirely consistent with a 10% return to education.**
>
> **This contrast with (a) is the point.** The same coefficient is *"significantly different from zero"* and *"not significantly different from 0.10."* **Significance is always relative to a stated null**, and the naked phrase "the coefficient is significant" means nothing without one.
>
> **(d)** $$0.022 \pm 1.96(0.0031) = 0.022 \pm 0.00608 = \mathbf{[0.0159,\;0.0281]}$$
>
> **Interpretation:** one more year with the current employer is associated with between **1.6% and 2.8%** higher wage, holding education and experience fixed. **The interval excludes zero**, so $\beta_{tenure}$ is significant at 5% — consistent with $t = 0.022/0.0031 = 7.10$.
>
> **What the interval adds over the $p$-value:** it tells you the effect is not merely non-zero but **economically substantial and fairly precisely pinned down.** A $p$-value alone would not.

---

### Exercise 2 — The $F$ test and its disagreement with $t$

A model of house prices with $n=88$ estimates
$$\log(price) = \beta_0+\beta_1\log(lotsize)+\beta_2\log(sqrft)+\beta_3\,bdrms+\beta_4\,bthrms+u$$
Unrestricted: $R_{ur}^2 = 0.643$. Dropping $bdrms$ and $bthrms$: $R_r^2 = 0.598$. The individual $t$ statistics on $bdrms$ and $bthrms$ are $1.34$ and $1.51$.

(a) Are $bdrms$ and $bthrms$ individually significant at 5%? (b) Test their joint significance. (c) Reconcile the results. (d) What would you conclude?

> [!example]- Solution
> **(a)** $df = 88-4-1 = 83$; two-sided 5% critical value $\approx 1.99$.
>
> $t_{bdrms} = 1.34 < 1.99$ → **not significant.**
> $t_{bthrms} = 1.51 < 1.99$ → **not significant.**
>
> **Neither is individually significant at 5%.**
>
> **(b)** $q = 2$ restrictions, $df_{ur} = 83$. Using the $R^2$ form (4.41):
> $$F = \frac{(R_{ur}^2-R_r^2)/q}{(1-R_{ur}^2)/(n-k-1)} = \frac{(0.643-0.598)/2}{(1-0.643)/83} = \frac{0.045/2}{0.357/83} = \frac{0.0225}{0.0043012} = \mathbf{5.23}$$
>
> The 5% critical value for $F_{2,83}$ is about **3.11** (and the 1% value about 4.88).
>
> $5.23 > 3.11$, so **reject $H_0:\beta_3=\beta_4=0$ — the two variables are JOINTLY significant**, even at the 1% level.
>
> **(c) Reconciling — this is the classic multicollinearity pattern.**
>
> **Bedrooms and bathrooms are strongly correlated with each other** (and with square footage): bigger houses have more of both. So in the auxiliary regression of $bdrms$ on the other regressors, $R_{bdrms}^2$ is high, inflating $\mathrm{Var}(\hat\beta_3)$ via
> $$\mathrm{Var}(\hat\beta_j) = \frac{\sigma^2}{\text{SST}_j(1-R_j^2)}$$
> from [[03 - Multiple Regression Analysis - Estimation]]. **The data cannot say whether an extra bedroom or an extra bathroom raises price, because the two almost always come together.**
>
> **But it can say clearly that "rooms" matter as a group** — and that is exactly what the $F$ test detects.
>
> *"There is no logical inconsistency in rejecting both null hypotheses"* — the $t$ tests and the $F$ test **answer different questions.**
>
> **(d) Conclusion and what to do.**
>
> **Keep both variables.** Dropping them would:
> - discard genuinely relevant information (the $F$ test says so);
> - risk **omitted variable bias** in $\hat\beta_1$ and $\hat\beta_2$, since lot size and square footage are correlated with room counts.
>
> **What to report:** the joint $F$ test, plus an honest statement that the individual contributions cannot be separated. If the *individual* effects are the research question, you need either more data or a design with independent variation in bedrooms and bathrooms.
>
> **What NOT to do:** report only the insignificant $t$ statistics and conclude "room counts don't affect price." That is the most common misreading of this pattern.

---

### Exercise 3 — Testing a hypothesis about two parameters

For the model $\log(wage) = \beta_0+\beta_1jc+\beta_2univ+\beta_3exper+u$ (where $jc$ = years of junior college, $univ$ = years at university), a researcher wants to test whether **a year of junior college is worth the same as a year of university**.

(a) State $H_0$ and $H_1$. (b) Why can't you use the printed output directly? (c) Show the reparameterisation. (d) Given $\hat\theta_1 = -0.0102$ with $\mathrm{se} = 0.0069$ and $n = 6{,}763$, carry out the test.

> [!example]- Solution
> **(a)** $$H_0:\beta_1=\beta_2 \quad\Longleftrightarrow\quad H_0:\beta_1-\beta_2=0$$
> A sensible one-sided alternative is $H_1:\beta_1<\beta_2$ — **a year of junior college is worth *less* than a year of university** — which is what one would expect *a priori*.
>
> **(b)** The statistic is $t = (\hat\beta_1-\hat\beta_2)/\mathrm{se}(\hat\beta_1-\hat\beta_2)$, and
> $$\mathrm{se}(\hat\beta_1-\hat\beta_2) = \sqrt{\mathrm{Var}(\hat\beta_1)+\mathrm{Var}(\hat\beta_2)-2\,\mathrm{Cov}(\hat\beta_1,\hat\beta_2)}$$
> **The covariance term is not in standard regression output.** You cannot simply combine the two printed standard errors — and note the covariance here is likely **negative** (the two education measures compete), which would make the naive calculation badly wrong in a predictable direction.
>
> **(c) Reparameterise.** Let $\theta_1 = \beta_1-\beta_2$, so $\beta_1 = \theta_1+\beta_2$. Substituting:
> $$\log(wage) = \beta_0+(\theta_1+\beta_2)jc+\beta_2univ+\beta_3exper+u$$
> $$= \beta_0+\theta_1\,jc+\beta_2\underbrace{(jc+univ)}_{\text{define } totcoll}+\beta_3exper+u$$
>
> **So: regress $\log(wage)$ on $jc$, $totcoll$ and $exper$.** The coefficient on $jc$ **is** $\theta_1=\beta_1-\beta_2$, and its printed standard error is exactly what you need.
>
> **(d)** $df = 6{,}763-3-1 = 6{,}759$ — effectively normal.
> $$t = \frac{-0.0102}{0.0069} = \mathbf{-1.48}$$
>
> **One-sided test at 5%:** critical value $-1.645$. Since $-1.48 > -1.645$, **fail to reject at 5%.**
>
> **At 10%:** critical value $-1.28$. Since $-1.48 < -1.28$, **reject at 10%** ($p \approx 0.069$).
>
> **Interpretation.** There is **suggestive but not conclusive** evidence that a year of junior college is worth about 1 percentage point less than a year of university. The point estimate is economically meaningful — **roughly a 1% wage penalty per year** — but with $\mathrm{se}=0.0069$ the 95% CI is $[-0.0237,\,0.0033]$, which includes zero.
>
> **The honest summary:** *"the estimated difference is about one percentage point in favour of university, but we cannot reject equality at conventional levels."* **Note how much more informative that is than "not significant."**

---

### Exercise 4 — Statistical vs practical significance

Two studies estimate the effect of a training programme on annual earnings.

**Study A:** $n = 200$. $\hat\beta = \$1{,}450$, $\mathrm{se} = \$890$.
**Study B:** $n = 500{,}000$. $\hat\beta = \$32$, $\mathrm{se} = \$11$.

(a) Compute $t$ statistics and test at 5%. (b) Which finding is more important? (c) Construct 95% CIs and use them to argue. (d) What does this reveal about $p$-values in large samples?

> [!example]- Solution
> **(a)**
>
> | | $\hat\beta$ | se | $t$ | Verdict at 5% |
> |---|---|---|---|---|
> | **Study A** | 1,450 | 890 | $1{,}450/890 = \mathbf{1.63}$ | **Not significant** ($<1.96$) |
> | **Study B** | 32 | 11 | $32/11 = \mathbf{2.91}$ | **Significant** ($>1.96$), $p\approx0.004$ |
>
> **(b) Study A is far more important economically, despite being "insignificant".**
>
> - **Study A** estimates the programme raises earnings by **$1,450 a year** — a substantial effect that would easily justify a modest training cost.
> - **Study B** estimates **$32 a year** — about 60 cents a week. **Even if perfectly measured, this effect is worthless.** No training programme costs less than $32 per participant.
>
> **Study B has precisely established that the programme does essentially nothing.** Study A has failed to establish anything, because the sample is too small.
>
> **(c) The confidence intervals make this unmistakable.**
>
> **Study A:** $1{,}450 \pm 1.96(890) = 1{,}450\pm1{,}744 = \mathbf{[-\$294,\;\$3{,}194]}$
>
> **Study B:** $32 \pm 1.96(11) = 32\pm21.6 = \mathbf{[\$10.4,\;\$53.6]}$
>
> Now read them:
> - Study A's interval is **compatible with a $3,194 benefit** — a hugely successful programme — **and** with a small loss. **It is uninformative, not evidence of no effect.**
> - Study B's interval **rules out anything above $54.** It is a **precise finding of a negligible effect.**
>
> **The CIs reverse the impression given by the $p$-values entirely.** This is the strongest argument for reporting intervals rather than significance stars.
>
> **(d) What large $n$ does to $p$-values.**
>
> From [[03 - Multiple Regression Analysis - Estimation]] (3.59), $\mathrm{se}(\hat\beta_j)\propto 1/\sqrt n$. So
> $$t = \frac{\hat\beta_j}{\mathrm{se}(\hat\beta_j)} \propto \hat\beta_j\sqrt{n}$$
>
> **With enough data, ANY non-zero effect becomes statistically significant.** In Study B, $n=500{,}000$ makes a \$32 effect detectable. Had $n$ been 5,000, the same estimate would have $\mathrm{se}\approx\$110$ and $t\approx0.29$ — "insignificant."
>
> **Consequences for practice:**
> - **In big data settings, statistical significance is nearly worthless as a filter.** Everything is significant. **Judge by magnitude and confidence intervals.**
> - **In small samples, insignificance is nearly worthless as evidence of absence.** Report the interval and say what it fails to rule out.
> - **Always ask "significant compared with what, and does it matter?"** before "is it significant?"

---

### Exercise 5 — Building an $F$ test from scratch

A researcher estimates a model of student test scores with $n=408$ schools:
$$score = \beta_0+\beta_1\,expend+\beta_2\,ratio+\beta_3\,lunch+\beta_4\,income+\beta_5\,ell+u$$
with $\text{SSR}_{ur} = 8{,}412$. Dropping $expend$, $ratio$ and $ell$ gives $\text{SSR}_r = 9{,}087$.

(a) Test the joint significance of the three dropped variables at 5%. (b) Convert to the $R^2$ form given $\text{SST}=44{,}500$ and verify. (c) The overall $F$ for the regression is 128.4 — what does it test, and is it informative? (d) If instead the restriction were $\beta_1+\beta_2=0$, could you use the $R^2$ form?

> [!example]- Solution
> **(a)** $q=3$ restrictions; $df_{ur} = 408-5-1 = \mathbf{402}$.
> $$F = \frac{(\text{SSR}_r-\text{SSR}_{ur})/q}{\text{SSR}_{ur}/(n-k-1)} = \frac{(9{,}087-8{,}412)/3}{8{,}412/402} = \frac{675/3}{20.925} = \frac{225}{20.925} = \mathbf{10.75}$$
>
> The 5% critical value for $F_{3,402}$ is about **2.63** (1% about 3.83).
>
> $10.75 > 2.63$: **reject $H_0:\beta_1=\beta_2=\beta_5=0$ decisively.** The three variables are **jointly significant** well beyond the 1% level.
>
> **(b)** $$R_{ur}^2 = 1-\frac{8{,}412}{44{,}500} = 1-0.18903 = \mathbf{0.81097}$$
> $$R_r^2 = 1-\frac{9{,}087}{44{,}500} = 1-0.20420 = \mathbf{0.79580}$$
> $$F = \frac{(0.81097-0.79580)/3}{(1-0.81097)/402} = \frac{0.015169/3}{0.18903/402} = \frac{0.0050562}{0.00047022} = \mathbf{10.75} \;\;✓$$
>
> **Identical, as it must be** — the SST terms cancel. Note the $R^2$ rises by only **1.5 percentage points**, yet the $F$ is 10.75. **A small $R^2$ gain can be highly significant when $n$ is large and $q$ is small** — another reason $R^2$ is a poor guide to variable selection ([[03 - Multiple Regression Analysis - Estimation]] §2).
>
> **(c) The overall $F$ tests $H_0:\beta_1=\cdots=\beta_5=0$** — that **none** of the five variables has any explanatory power.
>
> $F = 128.4$ against a critical value near 2.24 for $F_{5,402}$: **rejected overwhelmingly.**
>
> **Is it informative? Barely.** *"None of expenditure, class size, poverty, income or English-learner share affects test scores"* is a hypothesis nobody holds. **The overall $F$ is almost always rejected in applied work, and rejecting it tells you only that your regression is not pure noise.**
>
> **It is worth glancing at for one reason:** a **failure** to reject would be alarming — it would mean your entire specification explains nothing beyond chance.
>
> **(d) No — you must use the SSR form.**
>
> $H_0:\beta_1+\beta_2=0$ is a **linear restriction but not an exclusion restriction.** Imposing it requires substituting $\beta_2 = -\beta_1$, giving
> $$score = \beta_0+\beta_1(expend-ratio)+\beta_3lunch+\beta_4income+\beta_5ell+u$$
> — the same dependent variable, so here SST is in fact unchanged and (4.41) would work.
>
> **But the general warning stands**, and it bites whenever a restriction moves a term to the left-hand side. For example $H_0:\beta_1=1$ requires regressing $(score - expend)$ on the rest — **a different dependent variable, hence a different SST, and the $R^2$ form is invalid.**
>
> *"The sum of squared residuals form of the $F$ statistic is sometimes needed."* **Rule of thumb: exclusion restrictions → either form; anything else → SSR form.**

---

## 📝 Summary

- **Assumption MLR.6 (normality):** $u\sim\mathrm{Normal}(0,\sigma^2)$ and **independent of the regressors** — so MLR.6 **implies** MLR.4 and MLR.5. **MLR.1–MLR.6 are the classical linear model assumptions**, under which OLS is the **minimum variance unbiased estimator** (not merely BLUE).
- **The CLT defence of normality is weak** — unobserved factors may have very different distributions, and may not enter additively. **$wage$ cannot be normal (it is bounded below by zero); $\log(wage)$ is far more plausible.** In large samples normality is unnecessary ([[05 - Multiple Regression Analysis - OLS Asymptotics]]).
- **Theorem 4.2:** $(\hat\beta_j-\beta_j)/\mathrm{se}(\hat\beta_j)\sim t_{n-k-1}$. The **$t$ statistic** for $H_0:\beta_j=0$ is $\hat\beta_j/\mathrm{se}(\hat\beta_j)$; the general form is $(\hat\beta_j-a_j)/\mathrm{se}(\hat\beta_j)$. **Keep the sign.**
- **State the alternative before seeing the data.** One-sided tests use a smaller critical value; two-sided tests are usually prudent and protect against selecting the alternative from the estimate.
- **The $p$-value is the smallest level at which $H_0$ would be rejected.** Software reports the **two-sided** $p$-value for $H_0:\beta_j=0$.
- **A 95% CI is $\hat\beta_j\pm c\cdot\mathrm{se}(\hat\beta_j)$** with $c$ the 97.5th percentile of $t_{n-k-1}$. **The 95% is a property of the procedure, not a probability statement about $\beta_j$.** A CI is equivalent to running all possible two-sided tests at once.
- **For a hypothesis linking two parameters** ($H_0:\beta_1=\beta_2$), **reparameterise** — define $\theta_1=\beta_1-\beta_2$ and regress on $x_1$ and $(x_1+x_2)$ — because the required covariance is not in the standard output.
- **The $F$ test** for $q$ restrictions:
  $$F = \frac{(\text{SSR}_r-\text{SSR}_{ur})/q}{\text{SSR}_{ur}/(n-k-1)} = \frac{(R_{ur}^2-R_r^2)/q}{(1-R_{ur}^2)/(n-k-1)}$$
  distributed $F_{q,n-k-1}$ under $H_0$. **Always non-negative**; a negative value means the SSRs are the wrong way round. **The $R^2$ form works only for exclusion restrictions.**
- **$t$ and $F$ tests can disagree in both directions and both be right.** All $t$'s insignificant with a significant $F$ is the **classic multicollinearity signature**.
- **Statistical significance ≠ practical significance.** Since $\mathrm{se}\propto1/\sqrt n$, **any non-zero effect is significant in a large enough sample.** Judge the **magnitude** first, then the precision, and **report confidence intervals.**

---

## ⚠️ Important Notes

> [!warning] Fix the hypothesis before you look at the data
> Choosing a one-sided alternative after seeing the sign of $\hat\beta_j$ halves the $p$-value illegitimately. *"Classical statistical inference presumes that we state the null and alternative about the population **before looking at the data**."*

> [!warning] "Significant" is meaningless without a null
> Exercise 1 shows the same estimate significantly different from **0** and not significantly different from **0.10**. Always name the null being tested, and prefer economically interesting nulls — *"it is not much use to test $H_0:\beta_1=0$"* when nobody doubts the sign.

> [!important] A confidence interval is not a probability statement about $\beta_j$
> $\beta_j$ is fixed; the interval is random. **95% of such intervals cover $\beta_j$**, and you cannot tell whether yours is one of them. Wrong: "there is a 95% chance $\beta_j$ is in this interval."

> [!warning] Failing to reject is not evidence of no effect
> An "insignificant" coefficient with a wide CI is **uninformative**, not null. Exercise 4's Study A is compatible with a \$3,194 benefit. **Report the interval and say what it fails to rule out.**

> [!tip] A negative $F$ means you swapped the SSRs
> $\text{SSR}_r \ge \text{SSR}_{ur}$ always, because restrictions cannot improve fit. **Restricted first in the numerator; unrestricted first in the $R^2$ form.** The two orderings are opposite, which is exactly why the mistake is common.

> [!important] $t$ tests answer "given the others"; $F$ tests answer "as a group"
> Under multicollinearity a set of variables can be **jointly** significant while **none** is individually significant, because each is imprecisely estimated once the others are controlled for. **This is not a contradiction** — and reporting only the $t$ statistics in such a case is a serious misrepresentation.

> [!tip] The reparameterisation trick is worth memorising
> To test $H_0:\beta_1=\beta_2$: regress $y$ on $x_1$, $(x_1+x_2)$, and the rest. **The coefficient on $x_1$ is $\beta_1-\beta_2$**, with a correct standard error, straight from the output. Generalises to any single linear restriction.

> [!warning] Source-material note
> Written from the **Wooldridge 7th edition PDF** (pp. 117–162). Text extracts cleanly; **all figures are images** — notably Figure 4.1 (the homoskedastic normal distribution) and Figures 4.2–4.4 (the rejection regions), which are described in the surrounding text and reconstructed above.
>
> **Equations extract with mangled symbols** (`b^ j`, `se1b^ j2`, `tn2k21`) and have been **transcribed and checked by hand** against their numbered references. **The $t$ and $F$ distribution tables are images**, so all critical values quoted in the exercises are standard values I have supplied, not extracted.
>
> **The data files are absent**; all exercises are my own construction with arithmetic verified by hand.
>
> **There are no lecture slides for this subject**; the chapter scope is my own editorial decision. See [[00-Index]].

---

**Previous:** [[03 - Multiple Regression Analysis - Estimation]] · **Next:** [[05 - Multiple Regression Analysis - OLS Asymptotics]] · **Index:** [[00-Index]]

#econometrics #hypothesis-testing #t-test #f-test #confidence-intervals #p-value #clm
