---
subject: Econometrics
chapter: 03
tags: [ds, econometrics, ols, multiple-regression, omitted-variable-bias, gauss-markov, multicollinearity]
source: "documents/Wooldridge — *Introductory Econometrics: A Modern Approach*, 7th ed., Ch. 3 (pp. 66–116)"
---

# Multiple Regression Analysis: Estimation

> [!abstract] Where this sits in the course
> [[02 - The Simple Regression Model]] ended with a warning: simple regression is *"in effect an analysis of correlation"*, and $\mathbb{E}(u\mid x)=0$ is implausible whenever an omitted factor is correlated with $x$. **Multiple regression is the direct response** — hold the confounders fixed by putting them in the equation.
>
> This chapter contains the two results that matter most in the whole book: **the omitted variable bias formula**, which tells you the direction of the damage when a confounder is left out, and the **Gauss–Markov theorem**, which says OLS is the best you can do when the assumptions hold.

---

## 📘 Main Knowledge

### 1. The model and why it beats simple regression

The multiple linear regression model with $k$ independent variables:

$$
\boxed{\;y = \beta_0+\beta_1x_1+\beta_2x_2+\cdots+\beta_kx_k+u\;} \tag{3.31}
$$

Each $\beta_j$ is a **partial effect**: the change in $y$ from a one-unit change in $x_j$, **holding all other included regressors fixed**.

$$
\Delta\hat y = \hat\beta_1\Delta x_1 + \hat\beta_2\Delta x_2+\cdots+\hat\beta_k\Delta x_k
$$

> [!important] The central advantage over simple regression
> In simple regression, "holding other factors fixed" was a *hope* about $u$. **In multiple regression, the factors you include are held fixed by construction.**
>
> Consider the test-score example the text uses repeatedly:
> $$avgscore = \beta_0+\beta_1expend+\beta_2avginc+u$$
> *"We fully expect $expend$ and $avginc$ to be correlated: school districts with high average family incomes tend to spend more per student on education. **In fact, the primary motivation for including $avginc$ in the equation is that we suspect it is correlated with $expend$, and so we would like to hold it fixed in the analysis.**"*
>
> **Correlation between regressors is the reason to include them, not a problem to be avoided.** This is exactly the opposite of the instinct many students bring to the subject.

**The model is flexible.** Because MLR.1 requires only linearity **in the parameters**, $y$ and the $x_j$ can be arbitrary functions of underlying variables:

$$
\log(salary) = \beta_0+\beta_1\log(sales)+\beta_2\,ceoten+\beta_3\,ceoten^2+u \tag{3.33}
$$

Here $\beta_1$ is an elasticity, and the quadratic in tenure allows the effect of experience to change with its level.

---

### 2. Mechanics and interpretation

#### OLS estimation

The OLS estimates $\hat\beta_0,\hat\beta_1,\dots,\hat\beta_k$ minimise

$$
\sum_{i=1}^n\big(y_i-\hat\beta_0-\hat\beta_1x_{i1}-\cdots-\hat\beta_kx_{ik}\big)^2
$$

giving $k+1$ first order conditions. **The algebraic properties of [[02 - The Simple Regression Model]] carry over exactly:**

1. $\sum_i\hat u_i = 0$
2. $\sum_i x_{ij}\hat u_i = 0$ for **every** $j=1,\dots,k$
3. The point $(\bar x_1,\dots,\bar x_k,\bar y)$ lies on the OLS hyperplane

And so do $\text{SST}=\text{SSE}+\text{SSR}$ and $R^2 = \text{SSE}/\text{SST} = 1-\text{SSR}/\text{SST}$.

#### The "partialling out" interpretation

This is the single most illuminating result about what multiple regression *does*. With $k=2$:

$$
\hat\beta_1 = \frac{\sum_{i=1}^n \hat r_{i1}y_i}{\sum_{i=1}^n \hat r_{i1}^2} \tag{3.22}
$$

**where the $\hat r_{i1}$ are the OLS residuals from a simple regression of $x_1$ on $x_2$.**

> [!important] What (3.22) says, in words
> **Step 1.** Regress $x_1$ on $x_2$ and keep the residuals $\hat r_1$. These are the part of $x_1$ that is **uncorrelated with $x_2$** — $x_1$ with $x_2$'s influence stripped out.
>
> **Step 2.** Regress $y$ on those residuals. The slope is **exactly** the multiple regression coefficient $\hat\beta_1$.
>
> So *"$\hat\beta_1$ measures the sample relationship between $y$ and $x_1$ **after $x_2$ has been partialled out.**"* In the general case, $\hat\beta_1$ *"measures the effect of $x_1$ on $y$ after $x_2,\dots,x_k$ have been partialled or netted out."*
>
> **Note that $y$ plays no role in Step 1.** The partialling happens entirely among the regressors.
>
> **In simple regression there is no partialling out, because no other variables are included** — which is precisely why simple regression conflates the effect of $x_1$ with the effects of everything correlated with it.
>
> *(This is the Frisch–Waugh–Lovell theorem; you will meet the same idea in [[Time-series Analysis/contents/08 - VECM and Cointegration|Johansen's auxiliary regressions]], which partial out short-run dynamics before estimating long-run relations.)*

#### The relationship between simple and multiple regression estimates

Write $\tilde\beta_1$ for the **simple** regression slope of $y$ on $x_1$, and $\hat\beta_1,\hat\beta_2$ for the **multiple** regression slopes of $y$ on $x_1,x_2$. Then

$$
\boxed{\;\tilde\beta_1 = \hat\beta_1 + \hat\beta_2\tilde\delta_1\;} \tag{3.23}
$$

where $\tilde\delta_1$ is the slope from the simple regression of $x_2$ on $x_1$.

> [!important] The two cases where they coincide
> $\tilde\beta_1 = \hat\beta_1$ **if and only if** either
> 1. **$\hat\beta_2 = 0$** — $x_2$ has no partial effect on $y$ in the sample; or
> 2. **$\tilde\delta_1 = 0$** — $x_1$ and $x_2$ are **uncorrelated in the sample**.
>
> **This equation is the algebraic skeleton of omitted variable bias** (§4), and it is worth memorising in this form: *the simple regression slope equals the multiple regression slope plus (the effect of the omitted variable) × (its relationship with the included one).*

#### Goodness of fit

$$
R^2 = \frac{\text{SSE}}{\text{SST}} = 1-\frac{\text{SSR}}{\text{SST}}
$$

> [!warning] **$R^2$ never falls when a variable is added**
> Adding **any** regressor — however irrelevant — **cannot increase SSR**, so **$R^2$ can only rise or stay the same.** It therefore **cannot be used to decide whether a variable belongs in the model.**
>
> *"A low $R^2$ does not mean that the equation is useless."* An equation with a small $R^2$ can still deliver a precisely estimated, policy-relevant partial effect — and a high $R^2$ guarantees nothing about causality.
>
> **This defect is what motivates adjusted $R^2$** in [[06 - Multiple Regression Analysis - Further Issues]] and the **$F$ test** in [[04 - Multiple Regression Analysis - Inference]].

---

### 3. The Gauss–Markov assumptions

| | Assumption | Statement |
|---|---|---|
| **MLR.1** | **Linear in parameters** | $y = \beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$ in the population |
| **MLR.2** | **Random sampling** | A random sample $\{(x_{i1},\dots,x_{ik},y_i):i=1,\dots,n\}$ following MLR.1 |
| **MLR.3** | **No perfect collinearity** | No $x_j$ is constant, and there are **no exact linear relationships** among the $x_j$ |
| **MLR.4** | **Zero conditional mean** | $\mathbb{E}(u\mid x_1,\dots,x_k)=0$ |
| **MLR.5** | **Homoskedasticity** | $\mathrm{Var}(u\mid x_1,\dots,x_k)=\sigma^2$ |

**MLR.1–MLR.5 are collectively the Gauss–Markov assumptions** (for cross-sectional regression). Equivalently, MLR.1 and MLR.4 together say

$$
\mathbb{E}(y\mid \mathbf{x}) = \beta_0+\beta_1x_1+\cdots+\beta_kx_k
$$

and MLR.5 says $\mathrm{Var}(y\mid\mathbf{x})=\sigma^2$.

> [!important] MLR.4 and MLR.5 are of completely different weight
> *"Assumption MLR.4 says that the expected value of $y$, given $\mathbf{x}$, is linear in the parameters"* — this is a substantive claim about the world, and **its failure biases OLS.**
>
> MLR.5 concerns only the **spread** of $y$ around that mean. **Its failure leaves OLS unbiased and damages only the standard errors** — see [[08 - Heteroskedasticity]].

#### MLR.3 in detail — what perfect collinearity is and is not

**MLR.3 rules out *exact* linear relationships, not correlation.** *"Assumption MLR.3 only rules out perfect correlation between $expend$ and $avginc$ in our sample... **some correlation, perhaps a substantial amount, is expected and certainly allowed.**"*

**Ways MLR.3 can fail:**

| Cause | Example |
|---|---|
| **Same variable in different units** | Including income in dollars **and** in thousands of dollars. *"What sense would it make to hold income measured in dollars fixed while changing income measured in thousands of dollars?"* |
| **An exact linear combination** | Including $expendA$, $expendB$ and $totexpend = expendA+expendB$ |
| **Too few observations** | *"MLR.3 fails if $n < k+1$. Intuitively: to estimate $k+1$ parameters, we need at least $k+1$ observations."* |
| **Bad luck** | A sample in which every individual happens to have exactly twice as much education as experience — *"very unlikely unless we have an extremely small sample size"* |

> [!note] Nonlinear functions of the same variable are fine
> $cons = \beta_0+\beta_1inc+\beta_2inc^2+u$ **does not violate MLR.3**: *"even though $x_2=inc^2$ is an exact function of $x_1=inc$, $inc^2$ is not an exact **linear** function of $inc$."*
>
> **Including $inc^2$ is a useful way to generalise functional form, unlike including income in dollars and in thousands.**

#### MLR.4 and the language of endogeneity

**MLR.4 can fail for several distinct reasons:**

1. **Functional form misspecification** — omitting $inc^2$ when it belongs; using $wage$ when the true model has $\log(wage)$.
2. **Omitting a relevant variable correlated with an included one** — §4, the main case.
3. **Measurement error** in an explanatory variable — [[09 - More on Specification and Data Issues]].
4. **Simultaneity** — $y$ also determines $x_j$.

**Terminology:** when $x_j$ is correlated with $u$ it is called an **endogenous explanatory variable**; when uncorrelated, **exogenous**. *"The terms 'exogenous' and 'endogenous' originated in simultaneous equations analysis."*

#### Theorem 3.1 — Unbiasedness of OLS

$$
\boxed{\;\text{Under MLR.1–MLR.4: } \mathbb{E}(\hat\beta_j)=\beta_j \text{ for } j=0,1,\dots,k\;}
$$

> [!note] Including *irrelevant* variables does not cause bias
> Suppose the true model is $y=\beta_0+\beta_1x_1+\beta_2x_2+u$ but we estimate with $x_3$ also included. Since unbiasedness holds **for any value of $\beta_j$, including $\beta_j=0$**, we get $\mathbb{E}(\hat\beta_3)=0$ and all other coefficients remain unbiased.
>
> *"Including one or more irrelevant variables in a multiple regression model, or **overspecifying the model**, does not affect the unbiasedness of the OLS estimators."*
>
> **But it is not harmless:** *"including irrelevant variables can have undesirable effects on the variances of the OLS estimators"* — see §5. **Overspecification costs precision; underspecification costs unbiasedness.** That trade-off is the whole of applied model selection.

---

### 4. Omitted variable bias

**The central result of the chapter.**

#### The simple case

Let the true model be

$$
y = \beta_0+\beta_1x_1+\beta_2x_2+u \tag{3.40}
$$

satisfying MLR.1–MLR.4, but suppose we **omit $x_2$** and estimate $\tilde y = \tilde\beta_0+\tilde\beta_1x_1$.

From the algebraic relationship (3.23), $\tilde\beta_1 = \hat\beta_1+\hat\beta_2\tilde\delta_1$. Since $\tilde\delta_1$ depends only on the regressors (treat it as fixed) and $\hat\beta_1,\hat\beta_2$ are unbiased:

$$
\mathbb{E}(\tilde\beta_1) = \beta_1+\beta_2\tilde\delta_1 \tag{3.45}
$$

$$
\boxed{\;\mathrm{Bias}(\tilde\beta_1) = \mathbb{E}(\tilde\beta_1)-\beta_1 = \beta_2\,\tilde\delta_1\;} \tag{3.46}
$$

where $\tilde\delta_1$ is the slope from regressing $x_2$ on $x_1$ — **the sample covariance of $x_1$ and $x_2$ over the sample variance of $x_1$.**

> [!important] **Bias = (effect of the omitted variable on $y$) × (its relationship with the included variable)**
> **Two cases give no bias:**
> 1. **$\beta_2=0$** — $x_2$ does not belong in the true model. (Known already from [[02 - The Simple Regression Model|chapter 2]].)
> 2. **$\tilde\delta_1=0$** — **$x_1$ and $x_2$ are uncorrelated in the sample.** *"If $x_1$ and $x_2$ are uncorrelated in the sample, then $\tilde\beta_1$ is unbiased."*
>
> **Both conditions must fail for bias to arise.** An omitted variable that is unrelated to your regressor of interest is harmless — which is why the question is never "did I omit something?" (you always did) but **"did I omit something correlated with $x_1$?"**

#### The sign table

| | $\mathrm{Corr}(x_1,x_2) > 0$ | $\mathrm{Corr}(x_1,x_2) < 0$ |
|---|---|---|
| **$\beta_2>0$** | **Positive bias** (upward) | **Negative bias** (downward) |
| **$\beta_2<0$** | **Negative bias** | **Positive bias** |

*(Wooldridge's Table 3.2. "Upward bias" means $\mathbb{E}(\tilde\beta_1) > \beta_1$; "downward" the reverse. Note that with a negative $\beta_1$, an upward bias makes the estimate **smaller in magnitude** — the language refers to the signed value, not the absolute value.)*

> [!example] Example 3.6 — Ability bias in the return to education
> Suppose the true model is
> $$\log(wage) = \beta_0+\beta_1educ+\beta_2abil+u$$
> **`WAGE1` contains no data on ability**, so we estimate the simple regression:
> $$\widehat{\log(wage)} = 0.584+0.083\,educ \qquad n=526,\;R^2=0.186 \tag{3.47}$$
>
> **Signing the bias:**
> - *"By definition, more ability leads to higher productivity and therefore higher wages: $\beta_2>0$."*
> - *"There are reasons to believe that $educ$ and $abil$ are positively correlated: on average, individuals with more innate ability choose higher levels of education."* So $\tilde\delta_1>0$.
> - **Bias $=\beta_2\tilde\delta_1 > 0$ — upward.**
>
> **Conclusion: the OLS estimates from the simple regression are on average too large.**
>
> > [!warning] Read the conclusion precisely
> > *"This does **not** mean that the estimate obtained from our sample is too big. We can only say that **if we collect many random samples and obtain the simple regression estimates each time, then the average of these estimates will be greater than $\beta_1$.**"*
> >
> > And: *"This is the result from only a single sample, so we cannot say that 0.083 is greater than $\beta_1$; the true return to education could be lower or higher than 8.3% (**and we will never know for sure**)."*
> >
> > **Bias is a property of the sampling distribution, not of your number.** Exam answers that say "the estimate of 8.3% is too high" are wrong; "the estimator is biased upward, so on average such estimates overstate the return" is right.

#### More general cases

> *"Deriving the sign of omitted variable bias when there are multiple regressors is more difficult. We must remember that **correlation between a single explanatory variable and the error generally results in ALL OLS estimators being biased.**"*

If the true model has $x_1,x_2,x_3$ and we omit $x_3$, then even if $x_2$ is uncorrelated with $x_3$, *"both $\tilde\beta_1$ and $\tilde\beta_2$ will normally be biased. The only exception is when $x_1$ and $x_2$ are also uncorrelated."*

**The practical approximation:** if $x_1$ and $x_2$ are (roughly) uncorrelated, analyse the bias in $\tilde\beta_1$ **as if $x_2$ were absent from both models**, replacing $\beta_2$ with $\beta_3$ and $x_2$ with $x_3$ in the sign table.

> [!important] One endogenous regressor contaminates the whole equation
> This is a point students consistently underestimate. **If ability is omitted from $wage = \beta_0+\beta_1educ+\beta_2exper+\beta_3abil+u$, both $\tilde\beta_1$ and $\tilde\beta_2$ are biased** — even though experience may be unrelated to ability.
>
> **You cannot rescue "the coefficients I care about" by conceding that one other coefficient is biased.** Endogeneity is a property of the equation, not of a single term in it.

---

### 5. The variance of the OLS estimators

#### Theorem 3.2 — Sampling variances

**Under MLR.1–MLR.5, conditional on the sample values of the regressors:**

$$
\boxed{\;\mathrm{Var}(\hat\beta_j) = \frac{\sigma^2}{\text{SST}_j\,(1-R_j^2)}\;}, \qquad j=1,\dots,k \tag{3.51}
$$

where $\text{SST}_j=\sum_i(x_{ij}-\bar x_j)^2$ is the total sample variation in $x_j$, and **$R_j^2$ is the $R$-squared from regressing $x_j$ on ALL the other independent variables** (including an intercept).

> [!warning] All five assumptions are used
> *"Whereas we did not need the homoskedasticity assumption to conclude that OLS is unbiased, **we do need it to justify equation (3.51)**."* Under heteroskedasticity this formula is simply wrong — and **every regression package reports it as the default standard error.**

#### The three components

| Component | Effect on $\mathrm{Var}(\hat\beta_j)$ | Interpretation |
|---|---|---|
| **$\sigma^2$** — error variance | Larger $\sigma^2$ ⇒ **larger** variance | *"More 'noise' in the equation makes it more difficult to estimate the partial effect."* **A feature of the population — nothing to do with sample size**, and the only unknown component |
| **$\text{SST}_j$** — variation in $x_j$ | Larger $\text{SST}_j$ ⇒ **smaller** variance | More spread in $x_j$ ⇒ easier to trace its effect. Grows with $n$ |
| **$R_j^2$** — collinearity with other regressors | Larger $R_j^2$ ⇒ **larger** variance; $\mathrm{Var}(\hat\beta_j)\to\infty$ as $R_j^2\to1$ | *"The proportion of the total variation in $x_j$ that can be explained by the other independent variables"* |

> [!important] Reading $R_j^2$ correctly
> **$R_j^2$ is not the regression's $R^2$.** It is the $R^2$ from an **auxiliary regression of $x_j$ on all the other $x$'s**. It measures how much of $x_j$ is redundant given the rest.
>
> - **$R_j^2 = 0$** (the best case, *"rarely encountered"*) — $x_j$ has zero sample correlation with every other regressor.
> - **$R_j^2 = 1$** is **ruled out by MLR.3** — that is perfect collinearity.
> - **$R_j^2$ close to 1** is **multicollinearity**.
>
> **The intuition connects directly to partialling out (§2):** $\hat\beta_j$ is estimated from the part of $x_j$ that is *left over* after removing the other regressors. If $R_j^2 = 0.9$, only 10% of $x_j$'s variation is left to identify $\beta_j$ — **so the estimate is imprecise.**

#### Multicollinearity — Wooldridge's deflationary treatment

> [!important] *"A case where $R_j^2$ is close to one is NOT a violation of Assumption MLR.3."*
> > *"Because multicollinearity violates none of our assumptions, **the 'problem' of multicollinearity is not really well defined.** When we say that multicollinearity arises when $R_j^2$ is 'close' to one, we put 'close' in quotation marks because **there is no absolute number that we can cite** to conclude that multicollinearity is a problem."*
>
> **OLS remains unbiased, BLUE, and correctly standard-errored under multicollinearity.** Nothing is broken. The estimates are simply **imprecise** — which the standard errors already tell you.

**Goldberger's joke, which is also a serious point:**

> *"Just as a large value of $R_j^2$ can cause a large $\mathrm{Var}(\hat\beta_j)$, so can a small value of $\text{SST}_j$. Therefore, **a small sample size can lead to large sampling variances too. Worrying about high degrees of correlation among the independent variables is really no different from worrying about a small sample size: both work to increase $\mathrm{Var}(\hat\beta_j)$.**"*
>
> *"The famous University of Wisconsin econometrician **Arthur Goldberger**, reacting to econometricians' obsession with multicollinearity, has (tongue in cheek) coined the term **micronumerosity**, which he defines as the 'problem of small sample size.'"*

> [!warning] Do not "fix" multicollinearity by dropping variables
> *"In the social sciences, where we are usually passive collectors of data, **there is no good way to reduce variances of unbiased estimators other than to collect more data.** For a given data set, we can try dropping other independent variables in an effort to reduce multicollinearity. **Unfortunately, dropping a variable that belongs in the population model can lead to bias**, as we saw in Section 3-3."*
>
> **This is the trade-off in its sharpest form:** keeping a collinear control costs **variance**; dropping it costs **bias**. **Bias does not shrink with sample size; variance does.** That asymmetry is a strong argument for keeping the control.

> [!important] Multicollinearity among *controls* is irrelevant
> A crucial and frequently missed point. Suppose you are estimating a discrimination effect while controlling for several highly correlated ability measures. *"**High correlations among these controls do not make it more difficult to determine the effects of discrimination.**"*
>
> **What matters is $R_j^2$ for the coefficient you care about**, not overall collinearity in the design matrix. This is exactly why *"omnibus"* diagnostics such as the **condition number** are *"of questionable value, because they might reveal a 'problem' simply because two control variables, whose coefficients we do not care about, are highly correlated."*

#### Estimating $\sigma^2$ and standard errors

$$
\boxed{\;\hat\sigma^2 = \frac{\text{SSR}}{n-k-1}\;}
$$

**$n-k-1$ degrees of freedom** — one lost for each of the $k+1$ estimated parameters, generalising the $n-2$ of [[02 - The Simple Regression Model]].

$$
\mathrm{se}(\hat\beta_j) = \frac{\hat\sigma}{\sqrt{\text{SST}_j(1-R_j^2)}}
$$

An equivalent form that makes the role of $n$ explicit:

$$
\mathrm{se}(\hat\beta_j) = \frac{\hat\sigma}{\sqrt{n}\;\mathrm{sd}(x_j)\sqrt{1-R_j^2}} \tag{3.59}
$$

> [!important] Standard errors shrink at rate $1/\sqrt n$
> *"The other three terms — $\hat\sigma$, $\mathrm{sd}(x_j)$, and $R_j^2$ — will change with different samples, but as $n$ gets large they settle down to constants. Therefore **the standard errors shrink to zero at the rate $1/\sqrt n$.** This formula demonstrates the value of getting more data."*
>
> **Contrast with unbiasedness**, which *"holds for any sample size subject to being able to compute the estimators."* **More data buys precision, never unbiasedness.** If your estimator is biased, a million observations will give you a very precise wrong answer.

---

### 6. Efficiency: the Gauss–Markov theorem

> [!important] **Theorem 3.4 — Gauss–Markov**
> $$\text{Under MLR.1–MLR.5, } \hat\beta_0,\hat\beta_1,\dots,\hat\beta_k \text{ are the } \textbf{Best Linear Unbiased Estimators (BLUE)}$$
>
> Unpacking the acronym:
> - **B**est — smallest variance
> - **L**inear — a linear function of the $y_i$
> - **U**nbiased — $\mathbb{E}(\tilde\beta_j)=\beta_j$
> - **E**stimators
>
> Formally: *"for any estimator $\tilde\beta_j$ that is linear and unbiased, $\mathrm{Var}(\hat\beta_j)\le\mathrm{Var}(\tilde\beta_j)$, and the inequality is usually strict."* The theorem says more: **any linear combination of the $\beta_j$ is best estimated by the corresponding combination of the OLS estimators.**
>
> *"When the standard set of assumptions holds, **we need not look for alternative unbiased estimators: none will be better than OLS.**"*

> [!warning] What breaks the theorem, and what each break costs
> | Assumption fails | Unbiased? | BLUE? | Standard errors valid? | Remedy |
> |---|---|---|---|---|
> | **MLR.4** (zero conditional mean) | ❌ **No** | ❌ No | ❌ No | Better model, panel data, IV |
> | **MLR.5** (homoskedasticity) | ✅ **Yes** | ❌ **No** | ❌ **No** | Robust SEs or WLS — [[08 - Heteroskedasticity]] |
> | **MLR.3** (no perfect collinearity) | — | — | — | OLS **cannot be computed at all** |
>
> **The middle row is the one to internalise.** *"Heteroskedasticity does not cause OLS to be biased. However, OLS no longer has the smallest variance among linear unbiased estimators."* **Failure of MLR.5 is an efficiency and inference problem, not a bias problem.**

---

## ✏️ Exercises

> [!note] The textbook's computer exercises require data files not present in the vault. These are my own construction, using regressions reported in the text.

### Exercise 1 — Sign the omitted variable bias

For each, identify the omitted variable, state whether $\beta_2>0$ or $<0$, state the sign of $\mathrm{Corr}(x_1,x_2)$, and give the direction of bias.

(a) $\widehat{\log(wage)} = 0.584+0.083\,educ$, omitting ability.
(b) $\widehat{math10} = 32.14-0.319\,lnchprg$, omitting the poverty rate.
(c) $\widehat{crime} = \beta_0+\beta_1 police$, omitting the underlying crime rate that prompted police hiring.
(d) $\widehat{salary} = \beta_0+\beta_1 educ$ for CEOs, omitting firm size.

> [!example]- Solution
> **(a) Ability — upward bias.**
> $\beta_2>0$ (ability raises wages); $\mathrm{Corr}(educ,abil)>0$ (more able people get more education). **Bias $=\beta_2\tilde\delta_1>0$.** The 8.3% estimate **overstates the return on average.**
>
> **(b) Poverty rate — downward bias, plausibly reversing the sign.**
> $\beta_2<0$ (poverty lowers test scores); $\mathrm{Corr}(lnchprg,povrate)>0$ (lunch eligibility *is* a poverty measure). **Bias $<0$.**
>
> The true effect of the lunch programme is plausibly **zero or positive**, yet the estimate is $-0.319$. **The bias is large enough to flip the sign** — the strongest possible illustration of the formula's importance.
>
> **(c) Prior crime — upward bias.**
> Cities hire police *because* crime is high, so $\mathrm{Corr}(police, \text{prior crime})>0$, and prior crime raises current crime ($\beta_2>0$). **Bias $>0$.**
>
> A naive regression can find that **more police cause more crime.** Here the mechanism is **reverse causality** operating through an omitted variable — the same structure as (b), and a standard motivation for instrumental variables.
>
> **(d) Firm size — upward bias.**
> Larger firms pay more ($\beta_2>0$), and better-educated CEOs tend to run larger firms ($\mathrm{Corr}>0$). **Bias $>0$.**
>
> ---
> **The pattern:** in **(a)**, **(c)** and **(d)** the omitted variable raises both $y$ and $x_1$, giving upward bias. In **(b)** it lowers $y$ while raising $x_1$, giving downward bias. **Sign the two pieces separately, then multiply** — that is the whole method, and it works even though the omitted variable is unobserved.

---

### Exercise 2 — Simple vs multiple regression

A researcher estimates, on $n=935$ workers:

$$
\text{Simple: } \widehat{\log(wage)} = 5.97 + 0.060\,educ
$$
$$
\text{Multiple: } \widehat{\log(wage)} = 5.66 + 0.039\,educ + 0.0059\,IQ
$$

(a) Interpret both coefficients on $educ$. (b) Using (3.23), what must be the sign of the relationship between $educ$ and $IQ$? Verify by computing $\tilde\delta_1$. (c) Which estimate is closer to the causal return, and why is neither certainly correct?

> [!example]- Solution
> **(a)** **Simple:** comparing workers who differ by one year of education, log wage is higher by 0.060, i.e. **about 6.0%** — **not** holding IQ fixed.
>
> **Multiple:** among workers **with the same IQ**, one more year of education is associated with **about 3.9%** higher wage. The IQ coefficient says one more IQ point is associated with **0.59%** higher wage, holding education fixed.
>
> **(b)** From (3.23), $\tilde\beta_1 = \hat\beta_1+\hat\beta_2\tilde\delta_1$:
> $$0.060 = 0.039 + 0.0059\,\tilde\delta_1
> \;\Longrightarrow\;
> \tilde\delta_1 = \frac{0.060-0.039}{0.0059} = \frac{0.021}{0.0059} = \mathbf{3.56}$$
>
> **$\tilde\delta_1 = 3.56 > 0$**: in the sample, one more year of education is associated with **about 3.6 more IQ points**. Positive, as expected.
>
> **Check the bias formula directly:** $\mathrm{Bias} = \beta_2\tilde\delta_1 \approx 0.0059\times3.56 = 0.021$ — **exactly the gap between the two estimates** ✓
>
> **(c) The multiple regression estimate (3.9%) is closer, but is not certainly right.**
>
> **It is better because** it removes the part of the ability–wage relationship that IQ captures. Controlling for IQ **cuts the estimated return by a third** — a large and revealing correction, and direct evidence that the simple regression was contaminated.
>
> **It is still not certainly causal, for three reasons:**
> 1. **IQ is an imperfect proxy for ability.** Motivation, perseverance, social skills and family connections all raise wages and correlate with education, and none is captured by IQ. **Residual ability bias remains, still upward.**
> 2. **IQ is measured with error**, which is itself a source of bias — [[09 - More on Specification and Data Issues]].
> 3. **Reverse causality:** education may *raise* IQ scores, in which case IQ is a "bad control" partly absorbing the effect we want to measure — **biasing the estimate downward.**
>
> **The two biases run in opposite directions**, which is why the literature on the return to schooling has not converged after fifty years. **Adding controls narrows the problem; it does not eliminate it.**

---

### Exercise 3 — Variance and multicollinearity

A regression on $n=200$ gives $\hat\sigma^2 = 4.0$, and for $x_1$: $\text{SST}_1 = 500$, $R_1^2 = 0.85$.

(a) Compute $\mathrm{Var}(\hat\beta_1)$ and $\mathrm{se}(\hat\beta_1)$. (b) What would they be if $R_1^2 = 0$? (c) What would they be if $n$ quadrupled (with $\text{SST}_1$ scaling proportionally)? (d) A colleague suggests dropping the collinear variable. Advise.

> [!example]- Solution
> **(a)** From (3.51):
> $$\mathrm{Var}(\hat\beta_1) = \frac{\hat\sigma^2}{\text{SST}_1(1-R_1^2)} = \frac{4.0}{500(0.15)} = \frac{4.0}{75} = \mathbf{0.05333}$$
> $$\mathrm{se}(\hat\beta_1) = \sqrt{0.05333} = \mathbf{0.2309}$$
>
> **(b) With $R_1^2 = 0$:**
> $$\mathrm{Var} = \frac{4.0}{500(1)} = 0.008 \qquad \mathrm{se} = \mathbf{0.0894}$$
>
> **The standard error is 2.58× larger because of the collinearity** — equivalently, the **variance inflation factor** is $1/(1-R_1^2) = 1/0.15 = 6.67$, and $\sqrt{6.67}=2.58$.
>
> **(c) Quadrupling $n$ to 800**, so $\text{SST}_1 \approx 2{,}000$ (and $\hat\sigma^2$, $R_1^2$ settle to constants):
> $$\mathrm{Var} = \frac{4.0}{2{,}000(0.15)} = 0.01333 \qquad \mathrm{se} = \mathbf{0.1155}$$
>
> **The standard error halves** — exactly the $1/\sqrt n$ rate of (3.59): $\sqrt4 = 2$.
>
> **Note that quadrupling $n$ does not fully undo the collinearity here** (0.1155 vs 0.0894), but it goes most of the way. **More data is the genuine remedy.**
>
> **(d) Advise against dropping it — with one exception.**
>
> **The case against dropping:**
> - **If the variable belongs in the population model, dropping it causes omitted variable bias** (§4). You would trade a $\mathrm{se}$ of 0.231 for a **biased** estimate.
> - **Bias does not shrink with $n$; variance does.** Part (c) shows the variance problem is solvable by collecting data; the bias problem is not solvable at all.
> - **Multicollinearity violates no assumption.** The estimator is still unbiased and BLUE, and **the standard error already reports the imprecision honestly.** Nothing is hidden.
>
> **The exception:** if the collinear variable is a **control you do not care about** and is **not** correlated with the error, and if theory says it does not belong, dropping it is defensible. But note Wooldridge's point: **collinearity among controls does not harm the coefficient of interest anyway**, so dropping them buys nothing.
>
> **The right answers, in order:** (i) collect more data; (ii) accept the wide confidence interval and report it honestly; (iii) consider whether the two variables are measuring the same construct and should be combined into an index.

---

### Exercise 4 — Partialling out, verified

With $n=5$: $x_1 = (2,4,6,8,10)$, $x_2 = (1,3,4,6,7)$, $y = (5,9,12,17,20)$.

(a) Regress $x_1$ on $x_2$ and obtain residuals $\hat r_1$. (b) Regress $y$ on $\hat r_1$ (through the origin) and confirm the slope equals the multiple regression $\hat\beta_1$. (c) Explain why this must work.

> [!example]- Solution
> **(a) Regress $x_1$ on $x_2$.** Means: $\bar x_1 = 6$, $\bar x_2 = 4.2$.
>
> | $x_1$ | $x_2$ | $x_1-\bar x_1$ | $x_2-\bar x_2$ | product | $(x_2-\bar x_2)^2$ |
> |---|---|---|---|---|---|
> | 2 | 1 | $-4$ | $-3.2$ | 12.8 | 10.24 |
> | 4 | 3 | $-2$ | $-1.2$ | 2.4 | 1.44 |
> | 6 | 4 | 0 | $-0.2$ | 0 | 0.04 |
> | 8 | 6 | 2 | 1.8 | 3.6 | 3.24 |
> | 10 | 7 | 4 | 2.8 | 11.2 | 7.84 |
> | | | | **sum** | **30.0** | **22.80** |
>
> $$\hat\delta_1 = 30.0/22.80 = 1.31579, \qquad \hat\delta_0 = 6 - 1.31579(4.2) = 0.47368$$
>
> Fitted values and residuals $\hat r_1 = x_1 - \hat x_1$:
>
> | $x_2$ | $\hat x_1$ | $\hat r_1$ |
> |---|---|---|
> | 1 | 1.78947 | **$+0.21053$** |
> | 3 | 4.42105 | **$-0.42105$** |
> | 4 | 5.73684 | **$+0.26316$** |
> | 6 | 8.36842 | **$-0.36842$** |
> | 7 | 9.68421 | **$+0.31579$** |
>
> (Check: $\sum\hat r_1 = 0$ ✓, and $\sum x_2\hat r_1 = 0$ ✓ — the algebraic properties of §2.)
>
> **(b) Regress $y$ on $\hat r_1$ through the origin:**
> $$\hat\beta_1 = \frac{\sum \hat r_{i1}y_i}{\sum \hat r_{i1}^2}$$
>
> $$\sum \hat r_{i1}y_i = 0.21053(5) + (-0.42105)(9) + 0.26316(12) + (-0.36842)(17) + 0.31579(20)$$
> $$= 1.05263 - 3.78947 + 3.15789 - 6.26316 + 6.31579 = \mathbf{0.47368}$$
>
> $$\sum \hat r_{i1}^2 = 0.04432+0.17729+0.06925+0.13573+0.09972 = \mathbf{0.52632}$$
>
> $$\hat\beta_1 = \frac{0.47368}{0.52632} = \mathbf{0.9000}$$
>
> **Verification by direct multiple regression** of $y$ on $x_1,x_2$ gives
> $$\hat\beta_0 = 1.600,\qquad \hat\beta_1 = \mathbf{0.900},\qquad \hat\beta_2 = 1.333$$
> **The partialling-out slope matches $\hat\beta_1$ exactly.** ✓
>
> *(Sanity check: at $(x_1,x_2)=(2,1)$, $\hat y = 1.6+0.9(2)+1.333(1) = 4.73$ against an actual $y$ of 5 — a close fit, as expected for data constructed to be nearly linear.)*
>
> **A second, more revealing check.** The denominator of (3.22) should equal $\text{SST}_1(1-R_1^2)$ from the variance formula (3.51). Here $\text{SST}_1 = 40$ and $\mathrm{Corr}(x_1,x_2)^2 = 0.98684$, so
> $$\text{SST}_1(1-R_1^2) = 40(0.01316) = \mathbf{0.52632} = \sum\hat r_{i1}^2 \;\;✓$$
> **The two formulas are literally the same quantity** — which is the content of part (c).
>
> **(c) Why it must work.**
>
> $\hat r_1$ is **the part of $x_1$ orthogonal to $x_2$** — by construction, $\sum x_{i2}\hat r_{i1}=0$ and $\sum\hat r_{i1}=0$.
>
> When you regress $y$ on $\hat r_1$, **$x_2$ can contribute nothing**, because $\hat r_1$ is orthogonal to it. So the resulting slope isolates precisely the relationship between $y$ and the component of $x_1$ that $x_2$ cannot explain — **which is exactly the definition of a partial effect.**
>
> **The practical payoff:** this is why $\hat\beta_1$ has a *ceteris paribus* interpretation **within the sample**, and why $\mathrm{Var}(\hat\beta_1)$ depends on $1-R_1^2$ — the denominator $\sum\hat r_{i1}^2$ **is** $\text{SST}_1(1-R_1^2)$. **The variance formula and the partialling-out formula are the same fact seen twice.**

---

### Exercise 5 — Assumption audit

For each scenario, state which Gauss–Markov assumption is threatened and the consequence.

(a) Regressing quantity on price, where price is set by market equilibrium.
(b) A wage regression including both $exper$ and $age$, where every worker started at 18 so $exper = age - 18$ exactly.
(c) A regression of firm profit on advertising, where profit variability rises with firm size.
(d) A consumption function $cons = \beta_0+\beta_1inc+u$ when the true relationship is concave.
(e) A survey of household wealth in which rich households refuse to respond.

> [!example]- Solution
> **(a) MLR.4 fails — simultaneity.**
> Price and quantity are **jointly determined**: demand shocks (in $u$) move price. So $\mathrm{Corr}(price,u)\neq0$ and price is **endogenous**. **OLS is biased and inconsistent**, and the estimated "demand curve" is a mixture of demand and supply. **Remedy: instrumental variables** — a variable shifting supply but not demand, such as an input cost.
>
> **(b) MLR.3 fails — perfect collinearity.**
> $exper = age-18$ is an **exact linear function** of $age$. **OLS cannot be computed at all** — software will drop one variable or report an error.
>
> *Note this is a knife-edge case:* if even **one** worker started at a different age, MLR.3 holds and estimation proceeds — though with $R_j^2$ near 1, so §5's multicollinearity applies and the estimates will be hopelessly imprecise. **Perfect collinearity is a computational failure; near-perfect collinearity is a precision problem.**
>
> **(c) MLR.5 fails — heteroskedasticity.**
> $\mathrm{Var}(u\mid \mathbf{x})$ depends on firm size. **OLS remains unbiased**, but it is **no longer BLUE**, and **the reported standard errors are wrong**, so all $t$ and $F$ tests are invalid. **Remedy: robust standard errors or WLS** — [[08 - Heteroskedasticity]].
>
> **This is the row of the table in §6 worth knowing cold:** heteroskedasticity is an inference problem, **not** a bias problem.
>
> **(d) MLR.4 fails — functional form misspecification.**
> If the true model is $cons = \beta_0+\beta_1inc+\beta_2inc^2+u$ and we omit $inc^2$, then the omitted term is in the error and **is certainly correlated with $inc$**. This is **omitted variable bias with the omitted variable being a function of an included one.**
>
> **The remedy is free:** add $inc^2$. It requires no new data and **does not violate MLR.3**, because $inc^2$ is not an exact *linear* function of $inc$. Tested formally by **RESET** in [[09 - More on Specification and Data Issues]].
>
> **(e) MLR.2 fails — non-random sampling (sample selection).**
> This is the wealth example from [[01 - The Nature of Econometrics and Economic Data]] §3.1: *"if wealthier families are less likely to disclose, then the resulting sample on wealth is not a random sample."*
>
> **The consequence depends on whether selection is related to the error.** If refusal depends only on the *regressors*, OLS can survive; if it depends on the **outcome** (wealth itself), OLS is **biased**. Since here refusal depends directly on wealth, **it is biased.** Treated in [[09 - More on Specification and Data Issues]].
>
> ---
> **The general triage:**
> - **MLR.3 fails** → nothing computes. Diagnose immediately.
> - **MLR.5 fails** → coefficients fine, standard errors broken. Cheap to fix.
> - **MLR.2 or MLR.4 fails** → **coefficients biased.** Expensive to fix, and often not fixable with the data at hand.
>
> **Always check in that order**, and spend your worry budget on MLR.4.

---

## 📝 Summary

- **Multiple regression** $y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$ gives each $\beta_j$ a **partial effect** interpretation — the effect of $x_j$ **holding the other included regressors fixed.** Correlated regressors are the *reason* to include controls, not an obstacle.
- **Partialling out:** $\hat\beta_1 = \sum\hat r_{i1}y_i/\sum\hat r_{i1}^2$, where $\hat r_1$ are residuals from regressing $x_1$ on the other regressors. **$\hat\beta_1$ uses only the part of $x_1$ that the other regressors cannot explain.**
- **Simple vs multiple:** $\tilde\beta_1 = \hat\beta_1+\hat\beta_2\tilde\delta_1$. They agree **iff** $\hat\beta_2=0$ or $x_1,x_2$ are uncorrelated in the sample.
- **$R^2$ never decreases when a regressor is added**, so it cannot be used for variable selection.
- **Gauss–Markov assumptions:** MLR.1 linear in parameters, MLR.2 random sampling, MLR.3 no perfect collinearity, MLR.4 zero conditional mean, MLR.5 homoskedasticity.
- **Theorem 3.1: under MLR.1–MLR.4, OLS is unbiased.** Including **irrelevant** variables does not cause bias (but costs variance); **omitting relevant** ones does.
- **Omitted variable bias:**
  $$\mathrm{Bias}(\tilde\beta_1) = \beta_2\,\tilde\delta_1$$
  — the omitted variable's effect on $y$ times its relationship with the included regressor. **No bias if $\beta_2=0$ or if $x_1,x_2$ are uncorrelated.** With more regressors, **one endogenous variable generally biases all the coefficients.**
- **Theorem 3.2: under MLR.1–MLR.5,**
  $$\mathrm{Var}(\hat\beta_j) = \frac{\sigma^2}{\text{SST}_j(1-R_j^2)}$$
  Precision falls with error variance and with $R_j^2$ (**the $R^2$ from regressing $x_j$ on the other regressors**), and rises with the spread of $x_j$ and with $n$. Standard errors shrink at rate $1/\sqrt n$.
- **Multicollinearity** ($R_j^2$ near 1) **violates no assumption**; OLS stays unbiased and BLUE and the standard errors are honest. It is *"really no different from worrying about a small sample size"* — **micronumerosity**. **Do not fix it by dropping variables that belong**, and note that collinearity among *controls* does not harm the coefficient of interest.
- **Theorem 3.4 — Gauss–Markov: under MLR.1–MLR.5, OLS is BLUE.** Failure of MLR.4 destroys unbiasedness; failure of MLR.5 leaves unbiasedness intact but destroys efficiency and the standard errors.

---

## ⚠️ Important Notes

> [!warning] Bias is a property of the estimator, not of your estimate
> "The estimator is biased upward" means **the average across hypothetical repeated samples exceeds $\beta_1$.** It does **not** mean your particular number is too big — *"the true return to education could be lower or higher than 8.3%, and we will never know for sure."* Get this phrasing right; it is worth marks.

> [!important] Sign an omitted variable bias in two steps
> $$\mathrm{Bias} = \underbrace{\beta_2}_{\text{effect of omitted var on }y} \times \underbrace{\tilde\delta_1}_{\text{its correlation with }x_1}$$
> **Sign each factor from economics, then multiply.** This works even though the omitted variable is unobserved, and it is the most useful single tool in applied work: it tells you **which direction your estimate errs** before you have any better data.

> [!warning] Multicollinearity is not an assumption violation
> $R_j^2\to1$ inflates $\mathrm{Var}(\hat\beta_j)$ but breaks nothing. OLS is still unbiased, still BLUE, and the standard errors correctly report the imprecision. **The only real remedy is more data.** Dropping a variable that belongs trades a variance problem for a **bias** problem — and bias does not vanish as $n$ grows.

> [!important] Overspecify rather than underspecify, when in doubt
> | | Cost |
> |---|---|
> | **Include an irrelevant variable** | Higher variance. **Still unbiased.** |
> | **Omit a relevant variable** | **Bias.** Does not shrink with $n$. |
>
> The asymmetry favours inclusion — with the caveat that a "bad control" (one affected by the treatment) can *create* bias. Judgement is required; the default should be inclusion.

> [!tip] Distinguish $R^2$ from $R_j^2$
> - **$R^2$** — the regression's own goodness of fit, $\text{SSE}/\text{SST}$.
> - **$R_j^2$** — from an **auxiliary regression of $x_j$ on all the other regressors**, appearing in the variance formula.
>
> They are different quantities and answer different questions. **The variance inflation factor is $1/(1-R_j^2)$**, and its square root is the multiplier on the standard error.

> [!note] $n-k-1$ degrees of freedom
> $\hat\sigma^2 = \text{SSR}/(n-k-1)$ — one degree of freedom lost per estimated parameter, generalising $n-2$ from simple regression. **MLR.3 requires $n \ge k+1$**, and estimating $k+1$ parameters from barely more than $k+1$ observations leaves nothing to estimate $\sigma^2$ with.

> [!warning] Source-material note
> Written from the **Wooldridge 7th edition PDF** (pp. 66–116). Text extracts cleanly; **all figures are images** (notably Figure 3.1, the $\mathrm{Var}(\hat\beta_1)$-against-$R_1^2$ curve, described in §5). **Equations extract with mangled symbols** (`b^ j`, `R2 j`, `SSTj`) and have been **transcribed and checked by hand** against their numbered references.
>
> **Table 3.2** (the omitted-variable-bias sign table) is an image; the version in §4 is reconstructed from the surrounding text, which states the four cases explicitly.
>
> **The data files are absent** — only the textbook PDF is in the vault — so no reported regression can be re-estimated. **All exercises are my own construction**, and the arithmetic in Exercises 3 and 4 has been verified by hand.
>
> **There are no lecture slides for this subject**; the chapter scope of these notes is my own editorial decision. See [[00-Index]].

---

**Previous:** [[02 - The Simple Regression Model]] · **Next:** [[04 - Multiple Regression Analysis - Inference]] · **Index:** [[00-Index]]

#econometrics #ols #multiple-regression #omitted-variable-bias #gauss-markov #multicollinearity #blue
