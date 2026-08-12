---
subject: Econometrics
chapter: 02
tags: [ds, econometrics, ols, simple-regression, zero-conditional-mean, r-squared, functional-form]
source: "documents/Wooldridge — *Introductory Econometrics: A Modern Approach*, 7th ed., Ch. 2 (pp. 20–65)"
---

# The Simple Regression Model

> [!abstract] Where this sits in the course
> [[01 - The Nature of Econometrics and Economic Data]] posed the problem: estimate a *ceteris paribus* effect from data where nothing was randomised. **This chapter gives the first answer** — ordinary least squares with one explanatory variable.
>
> Simple regression *"has limitations as a general tool for empirical analysis. Nevertheless, it is sometimes appropriate as an empirical tool. Learning how to interpret the simple regression model is good practice for studying multiple regression."* Almost every idea here — the zero conditional mean assumption, unbiasedness, $R^2$, log functional forms — reappears in [[03 - Multiple Regression Analysis - Estimation|chapter 3]] essentially unchanged.

---

## 📘 Main Knowledge

### 1. Definition of the model

**Much of applied econometrics begins with the premise:** $y$ and $x$ are two variables representing some population, and we want to *"explain $y$ in terms of $x$"* or *"study how $y$ varies with changes in $x$."*

**Writing down such a model confronts three issues:**

1. **Because there is never an exact relationship between two variables, how do we allow for other factors to affect $y$?**
2. **What is the functional relationship between $y$ and $x$?**
3. **How can we be sure we are capturing a *ceteris paribus* relationship?**

All three are resolved by one equation:

$$
\boxed{\;y = \beta_0 + \beta_1 x + u\;} \tag{2.1}
$$

**assumed to hold in the population of interest.** This defines the **simple linear regression model** (also the **two-variable** or **bivariate** linear regression model).

#### Terminology

| $y$ | $x$ |
|---|---|
| **Dependent variable** | **Independent variable** |
| **Explained variable** | **Explanatory variable** |
| Response variable | **Control variable** |
| Predicted variable | Predictor variable |
| **Regressand** | **Regressor** (also **covariate**) |

> [!warning] "Independent" here does **not** mean statistically independent
> *"Be aware that the label 'independent' here does not refer to the statistical notion of independence between random variables."* **"Explained" and "explanatory" are probably the most descriptive**; "response" and "control" belong to the experimental sciences where $x$ is under the experimenter's control.

**$u$ — the error term or disturbance — represents factors other than $x$ that affect $y$.** *"A simple regression analysis effectively treats all factors affecting $y$ other than $x$ as being unobserved. You can usefully think of $u$ as standing for 'unobserved.'"*

#### What the slope means

If the other factors in $u$ are held fixed, so $\Delta u = 0$:

$$
\Delta y = \beta_1 \Delta x \quad\text{if}\quad \Delta u = 0 \tag{2.2}
$$

**$\beta_1$ is the slope parameter, holding the other factors in $u$ fixed; it is of primary interest in applied economics.**

> **Example 2.2 — A simple wage equation.**
> $$wage = \beta_0 + \beta_1 educ + u \tag{2.4}$$
> With $wage$ in dollars per hour and $educ$ in years, **$\beta_1$ measures the change in hourly wage given another year of education, holding all other factors fixed** — labour force experience, innate ability, tenure, work ethic, and much else.

> [!note] Linearity is restrictive — but only in $x$, not in the underlying variables
> *"The linearity of (2.1) implies that a one-unit change in $x$ has the same effect on $y$, regardless of the initial value of $x$. This is unrealistic for many economic applications."* We might want **increasing returns** — the next year of education worth more than the last. §4 shows how to allow this **without leaving the linear framework.**

---

### 2. The key assumption

**The most difficult issue is whether (2.1) really allows *ceteris paribus* conclusions.** $\beta_1$ does measure the effect of $x$ on $y$ holding $u$ fixed — but *"how can we hope to learn about the ceteris paribus effect of $x$ on $y$, holding other factors fixed, when we are ignoring all those other factors?"*

**The answer: we must restrict how $u$ relates to $x$.**

#### Step 1 — a free normalisation

**As long as the intercept $\beta_0$ is included, nothing is lost by assuming the average value of $u$ in the population is zero:**

$$
\mathbb{E}(u) = 0 \tag{2.5}
$$

**This says nothing about the relationship between $u$ and $x$** — it is a statement about the distribution of the unobservables, and it essentially *defines* $\beta_0$.

#### Step 2 — the assumption that matters

**The crucial assumption is that the average value of $u$ does not depend on the value of $x$:**

$$
\mathbb{E}(u\mid x) = \mathbb{E}(u) \tag{2.6}
$$

**When (2.6) holds, $u$ is *mean independent* of $x$.** *"The average value of the unobservables is the same across all slices of the population determined by the value of $x$."* (Mean independence is implied by full independence, an assumption often used in basic probability.)

Combining (2.5) and (2.6) gives the **zero conditional mean assumption**:

$$
\boxed{\;\mathbb{E}(u\mid x) = 0\;}
$$

> [!important] *"It is critical to remember that (2.6) is the assumption with impact; (2.5) essentially defines the intercept."*
> **Everything in this course turns on whether $\mathbb{E}(u\mid x)=0$.** It is not testable — $u$ is unobserved — so it must be argued for on economic grounds every single time.

> [!example] What it demands in the wage equation
> Simplify by assuming $u$ *is* innate ability. Then (2.6) requires that **the average level of ability is the same regardless of years of education:**
> $$\mathbb{E}(abil\mid 8) = \mathbb{E}(abil\mid 16) = \cdots$$
> *"If we think that average ability increases with years of education, then (2.6) is FALSE."* And it plainly does — **people with more ability, on average, choose to become more educated.**
>
> *"As we cannot observe innate ability, we have no way of knowing whether average ability is the same for all education levels. But this is an issue that we must address before relying on simple regression analysis."*
>
> **Contrast with the fertilizer example:** if fertilizer amounts are chosen **independently** of other features of the plots, (2.6) holds — average land quality does not depend on fertilizer. **If more fertilizer is put on higher-quality plots, it fails.** Randomisation is exactly what makes (2.6) true by construction.

#### The population regression function

Given $\mathbb{E}(u\mid x)=0$, taking conditional expectations of (2.1):

$$
\mathbb{E}(y\mid x) = \beta_0 + \beta_1 x \tag{2.8}
$$

This is the **population regression function (PRF)** — a fixed but unknown feature of the population.

**It breaks $y$ into two pieces:**

| Piece | Name |
|---|---|
| $\beta_0+\beta_1x = \mathbb{E}(y\mid x)$ | **Systematic part** — the part of $y$ **explained** by $x$ |
| $u$ | **Unsystematic part** — the part **not** explained by $x$ |

---

### 3. Deriving the OLS estimates

Let $\{(x_i,y_i): i=1,\dots,n\}$ be a random sample, so

$$
y_i = \beta_0 + \beta_1 x_i + u_i \tag{2.9}
$$

#### The method-of-moments derivation

From (2.5) and an implication of (2.6) — **in the population, $u$ is uncorrelated with $x$**:

$$
\mathbb{E}(u) = 0 \tag{2.10}
\qquad\qquad
\mathrm{Cov}(x,u) = \mathbb{E}(xu) = 0 \tag{2.11}
$$

In terms of observables and the unknown parameters:

$$
\mathbb{E}(y-\beta_0-\beta_1x) = 0 \tag{2.12}
\qquad\qquad
\mathbb{E}\big[x(y-\beta_0-\beta_1x)\big] = 0 \tag{2.13}
$$

**Two restrictions, two unknowns.** Choose $\hat\beta_0,\hat\beta_1$ to solve the **sample counterparts**:

$$
n^{-1}\sum_{i=1}^n (y_i-\hat\beta_0-\hat\beta_1x_i) = 0 \tag{2.14}
$$
$$
n^{-1}\sum_{i=1}^n x_i(y_i-\hat\beta_0-\hat\beta_1x_i) = 0 \tag{2.15}
$$

**This is an example of the method of moments approach to estimation.**

#### Solving

Equation (2.14) rearranges to $\bar y = \hat\beta_0 + \hat\beta_1\bar x$, hence

$$
\boxed{\;\hat\beta_0 = \bar y - \hat\beta_1\bar x\;} \tag{2.17}
$$

Substituting into (2.15) and using the summation identities $\sum(x_i-\bar x) = 0$ and $\sum x_i(x_i-\bar x)=\sum(x_i-\bar x)^2$:

$$
\boxed{\;\hat\beta_1 = \frac{\sum_{i=1}^n(x_i-\bar x)(y_i-\bar y)}{\sum_{i=1}^n(x_i-\bar x)^2}\;} \tag{2.19}
$$

**provided** $\sum_{i=1}^n(x_i-\bar x)^2 > 0$ (2.18).

> [!important] Read (2.19) three ways
> **1. As a ratio of moments:** *"simply the sample covariance between $x_i$ and $y_i$ divided by the sample variance of $x_i$."*
>
> **2. As a scaled correlation:**
> $$\hat\beta_1 = \hat\rho_{xy}\cdot\frac{\hat\sigma_y}{\hat\sigma_x}$$
> so **positively correlated $x$ and $y$ ⇒ $\hat\beta_1>0$**, and vice versa. The population analogue is $\beta_1 = \rho_{xy}\cdot\sigma_y/\sigma_x$.
>
> **3. As a warning.** Wooldridge draws the conclusion himself:
> > *"Recognition that $\beta_1$ is just a scaled version of $\rho_{xy}$ highlights an important limitation of simple regression when we do not have experimental data: in effect, **simple regression is an analysis of correlation between two variables**, and so one must be careful in inferring causality."*
>
> **This is the chapter's central caution, stated in its most compact form.**

> [!note] When does (2.18) fail?
> Only if **every $x_i$ takes the same value.** *"If $y=wage$ and $x=educ$, then (2.18) fails only if everyone in the sample has the same amount of education. If just one person has a different amount, the estimates can be computed."* Either you were unlucky, or **$x$ does not vary in the population and the question is uninteresting.**

#### Why "least squares"

Define the **fitted value** and **residual**:

$$
\hat y_i = \hat\beta_0 + \hat\beta_1 x_i \tag{2.20}
\qquad\qquad
\hat u_i = y_i - \hat y_i \tag{2.21}
$$

**Choosing $\hat\beta_0,\hat\beta_1$ to minimise the sum of squared residuals**

$$
\sum_{i=1}^n \hat u_i^2 = \sum_{i=1}^n(y_i-\hat\beta_0-\hat\beta_1x_i)^2 \tag{2.22}
$$

**gives first order conditions that are exactly (2.14) and (2.15)** (without $n^{-1}$). **Hence the same solutions**, and hence the name **ordinary least squares**.

> [!note] Why squares rather than absolute values?
> *"Minimizing the sum of the absolute values of the residuals is sometimes very useful. But it does have some drawbacks."*
> - **No closed-form formulas** — estimates require numerical optimisation.
> - **The statistical theory is very complicated.**
> - With OLS, *"we will be able to derive unbiasedness, consistency, and other important statistical properties relatively easily."*
> - And **OLS is suited to estimating the parameters of the conditional mean function** (2.8) — which is what we want.
>
> (We would never minimise the sum of the residuals *themselves*: *"residuals large in magnitude but with opposite signs would tend to cancel out."*)

The **OLS regression line** or **sample regression function (SRF)**:

$$
\hat y = \hat\beta_0 + \hat\beta_1 x \tag{2.23}
$$

> [!important] PRF vs SRF
> **The PRF $\mathbb{E}(y\mid x)=\beta_0+\beta_1x$ is fixed but unknown in the population.** **The SRF $\hat y = \hat\beta_0+\hat\beta_1x$ is computed from a particular sample and changes with every new sample.** Confusing them is the commonest conceptual error in this chapter.

#### Worked examples

> **Example 2.3 — CEO salary and return on equity.** `CEOSAL1`, 209 CEOs, 1990.
> $$\widehat{salary} = 963.191 + 18.501\,roe \qquad n=209,\;\; R^2 = 0.0132 \tag{2.39}$$
> $salary$ is in **thousands of dollars**, $roe$ in **percent**. **A one-percentage-point rise in return on equity is associated with $18,501 more salary.**

> **Example 2.4 — Wage and education.** `WAGE1`, $n=526$, 1976.
> $$\widehat{wage} = -0.90 + 0.54\,educ \tag{2.27}$$
> *"We must interpret this equation with caution. The intercept of −0.90 literally means that a person with no education has a predicted hourly wage of −90¢ an hour. This, of course, is silly."* **Only 18 of the 526 people have fewer than eight years of education**, so *"it is not surprising that the regression line does poorly at very low levels of education."*
>
> At $educ=8$: $\widehat{wage} = -0.90+0.54(8) = \$3.42$ per hour (1976 dollars). **One more year of education raises predicted wage by 54¢; four more years by \$2.16.**
>
> **But** *"because of the linear nature of (2.27), another year of education increases the wage by the same amount, regardless of the initial level of education."*

> **Example 2.5 — Voting outcomes and campaign expenditures.** `VOTE1`, 173 two-party US House races, 1988.
> $$\widehat{voteA} = 26.81 + 0.464\,shareA \qquad n=173,\;\; R^2 = 0.856 \tag{2.28}$$
> **A one-percentage-point rise in A's share of spending is associated with almost half a percentage point more of the vote.** *"Whether or not this is a causal effect is unclear, but it is not unbelievable. If $shareA=50$, $voteA$ is predicted to be about 50."*

---

### 4. Algebraic properties (true for any sample)

> [!important] These hold **by construction** — no assumptions required
> They are consequences of the first order conditions alone, and they hold in every sample no matter how badly specified the model is. **A "good" residual pattern therefore proves nothing about causality.**

**(1) The sample average of the OLS residuals is zero:**
$$
\sum_{i=1}^n \hat u_i = 0 \tag{2.30}
$$
*"This says nothing about the residual for any particular observation $i$."*

**(2) The sample covariance between the regressor and the residuals is zero:**
$$
\sum_{i=1}^n x_i\hat u_i = 0 \tag{2.31}
$$

**(3) The point $(\bar x,\bar y)$ is always on the OLS regression line.**

> **Example 2.7.** In `WAGE1`, $\bar{wage}=5.90$ and $\overline{educ}=12.56$. Plugging into (2.27): $-0.90+0.54(12.56) = 5.8824 \approx 5.9$ ✓ (the small gap is rounding).

**Consequences:** the sample average of the fitted values equals $\bar y$, and **the fitted values and residuals are uncorrelated in the sample.**

#### The sums of squares

$$
\text{SST} \equiv \sum(y_i-\bar y)^2
\qquad
\text{SSE} \equiv \sum(\hat y_i-\bar y)^2
\qquad
\text{SSR} \equiv \sum \hat u_i^2
$$

**SST measures total sample variation in $y$** (divide by $n-1$ for the sample variance); **SSE the variation in the fitted values; SSR the variation in the residuals.**

$$
\boxed{\;\text{SST} = \text{SSE} + \text{SSR}\;} \tag{2.36}
$$

The proof expands $\sum[(y_i-\hat y_i)+(\hat y_i-\bar y)]^2$ and uses the fact that the cross term $\sum\hat u_i(\hat y_i-\bar y)=0$ — which is just the zero sample covariance of residuals and fitted values.

> [!warning] The abbreviations are not standardised
> *"There is no uniform agreement on the names or abbreviations."* SST is sometimes TSS. **Worse, the *explained* sum of squares is sometimes called the "regression sum of squares"** — which, abbreviated naturally, would be SSR, **exactly the abbreviation used here for the *residual* sum of squares.** Always check what a given source means.

#### $R$-squared

Dividing (2.36) by SST:

$$
\boxed{\;R^2 \equiv \frac{\text{SSE}}{\text{SST}} = 1 - \frac{\text{SSR}}{\text{SST}}\;} \tag{2.38}
$$

**$R^2$ is the fraction of the sample variation in $y$ that is explained by $x$**, always between 0 and 1. Multiply by 100 for a percentage. **It equals the square of the sample correlation between $y_i$ and $\hat y_i$** — hence the name.

> [!important] A low $R^2$ is not a problem, and a high $R^2$ is not a defence
> **Example 2.8:** the CEO salary regression has $R^2 = 0.0132$ — **return on equity explains barely 1.3% of the variation in CEO salaries.** *"Thus, other factors must be more important."*
>
> **Example 2.9:** the voting regression has $R^2 = 0.856$ — **spending share explains over 85% of the variation in election outcomes.**
>
> **Neither figure tells you whether the coefficient is a causal effect.** A regression can have $R^2 = 0.99$ and a hopelessly biased slope (spurious regressions do exactly this — [[11 - Further Issues in Using OLS with Time Series Data]]); it can have $R^2=0.01$ and an unbiased, policy-relevant slope. **$R^2$ measures fit, not validity.**

---

### 5. Units of measurement and functional form

#### Rescaling

| Change | Effect on $\hat\beta_1$ | Effect on $\hat\beta_0$ | Effect on $R^2$ |
|---|---|---|---|
| Multiply **$y$** by $c$ | multiplied by $c$ | multiplied by $c$ | **none** |
| Multiply **$x$** by $c$ | **divided** by $c$ | **none** | **none** |

> **From (2.39):** measuring salary in dollars rather than thousands gives $\widehat{salardol} = 963{,}191 + 18{,}501\,roe$ — both coefficients ×1,000, **same interpretation.** Measuring $roe$ as a decimal instead of a percentage gives $\widehat{salary} = 963.191 + 1{,}850.1\,roedec$ — **slope ×100, intercept unchanged**, because $roedec=0$ still means zero return.

**$R^2$ is invariant to changes in the units of $y$ or $x$** — *"the goodness-of-fit of the model should not depend on the units of measurement of our variables."*

#### The four functional forms

By redefining $y$ and $x$ as logs, simple regression accommodates important nonlinearities.

| Model | Dep. var. | Indep. var. | Interpretation of $\beta_1$ |
|---|---|---|---|
| **Level-level** | $y$ | $x$ | $\Delta y = \beta_1\Delta x$ |
| **Level-log** | $y$ | $\log(x)$ | $\Delta y = (\beta_1/100)\,\%\Delta x$ |
| **Log-level** | $\log(y)$ | $x$ | $\%\Delta y = (100\beta_1)\Delta x$ — **semi-elasticity** |
| **Log-log** | $\log(y)$ | $\log(x)$ | $\%\Delta y = \beta_1\,\%\Delta x$ — **elasticity** |

> **Example 2.10 — A log wage equation.** Same data as Example 2.4:
> $$\widehat{\log(wage)} = 0.584 + 0.083\,educ \qquad n=526,\;\; R^2=0.186 \tag{2.44}$$
> **"$wage$ increases by 8.3% for every additional year of education. This is what economists mean when they refer to the 'return to another year of education.'"**
>
> *"The main reason for using the log of wage is to impose a **constant percentage effect** of education on wage."*

> [!warning] Two precise errors to avoid with (2.44)
> **1.** *"It is NOT correct to say that another year of education increases $\log(wage)$ by 8.3%."* It increases $\log(wage)$ **by 0.083**, which means $wage$ rises by about 8.3%.
>
> **2.** The $R^2$ of 0.186 means $educ$ explains 18.6% of the variation in **$\log(wage)$, not in $wage$.** $R^2$ values from models with different dependent variables **are not comparable** — see [[06 - Multiple Regression Analysis - Further Issues]].
>
> *"The intercept in (2.44) is not very meaningful, because it gives the predicted $\log(wage)$ when $educ=0$."*
>
> And: *"equation (2.44) might not capture all of the nonlinearity. If there are 'diploma effects', then the twelfth year of education — graduation from high school — could be worth much more than the eleventh."* Handled in [[07 - Multiple Regression Analysis with Qualitative Information]].

> **Example 2.11 — Constant elasticity.** `CEOSAL1`, salary against firm sales (millions of dollars):
> $$\widehat{\log(salary)} = 4.822 + 0.257\,\log(sales) \qquad n=209,\;\; R^2=0.211 \tag{2.46}$$
> **"A 1% increase in firm sales increases CEO salary by about 0.257% — the usual interpretation of an elasticity."**

> [!tip] Rescaling a logged variable changes only the intercept
> If $\log(y_i)=\beta_0+\beta_1x_i+u_i$ and we rescale $y$ by $c_1$, then adding $\log(c_1)$ to both sides gives $\log(c_1y_i) = [\log(c_1)+\beta_0]+\beta_1x_i+u_i$. **The slope is unchanged; the intercept becomes $\log(c_1)+\beta_0$.** This is why **elasticities and semi-elasticities are unit-free** — a major practical advantage of logs.

#### What "linear" means

> *"The key is that this equation is **linear in the parameters** $\beta_0$ and $\beta_1$. There are no restrictions on how $y$ and $x$ relate to the original explained and explanatory variables of interest."*

So $cons = \beta_0+\beta_1\sqrt{inc}+u$ **is** a linear regression model. But $cons = 1/(\beta_0+\beta_1 inc)+u$ **is not** — it is **not linear in the parameters**, and estimating it *"takes us into the realm of the nonlinear regression model, which is beyond the scope of this text."*

> [!important] *"For successful empirical work, it is much more important to become proficient at interpreting coefficients than to become efficient at computing formulas such as (2.19)."*

---

### 6. Statistical properties: unbiasedness

Four assumptions.

| | Assumption | Statement |
|---|---|---|
| **SLR.1** | **Linear in parameters** | The population model is $y = \beta_0+\beta_1x+u$ |
| **SLR.2** | **Random sampling** | We have a random sample $\{(x_i,y_i):i=1,\dots,n\}$ following the population model |
| **SLR.3** | **Sample variation in $x$** | The $x_i$ are **not all the same value** |
| **SLR.4** | **Zero conditional mean** | $\mathbb{E}(u\mid x)=0$ |

> [!note] On SLR.3
> *"This is a very weak assumption — certainly not worth emphasizing, but needed nevertheless."* Simple inspection reveals whether it fails: **if the sample standard deviation of $x_i$ is zero, SLR.3 fails.**

#### The key algebraic step

Substituting (2.48) into the formula for $\hat\beta_1$ and simplifying:

$$
\boxed{\;\hat\beta_1 = \beta_1 + \frac{\sum_{i=1}^n(x_i-\bar x)u_i}{\text{SST}_x} = \beta_1 + \frac{1}{\text{SST}_x}\sum_{i=1}^n d_iu_i\;} \tag{2.52}
$$

with $d_i = x_i-\bar x$ and $\text{SST}_x = \sum(x_i-\bar x)^2$.

> [!important] Equation (2.52) is the most useful line in the chapter
> **The estimator equals the truth plus a weighted average of the errors.** *"Conditional on the values of $x_i$, the randomness in $\hat\beta_1$ is due entirely to the errors in the sample. The fact that these errors are generally different from zero is what causes $\hat\beta_1$ to differ from $\beta_1$."*
>
> Everything follows from it: **unbiasedness** (the second term has mean zero if $\mathbb{E}(u_i\mid x)=0$), **the variance formula** (the variance of the second term), and **bias when SLR.4 fails** (the second term does *not* have mean zero).

#### Theorem 2.1 — Unbiasedness of OLS

**Under SLR.1–SLR.4:**
$$
\mathbb{E}(\hat\beta_0)=\beta_0
\qquad\text{and}\qquad
\mathbb{E}(\hat\beta_1)=\beta_1 \tag{2.53}
$$

*Proof.* Conditioning on the $x_i$ (so $\text{SST}_x$ and $d_i$ are non-random),
$$
\mathbb{E}(\hat\beta_1) = \beta_1 + \frac{1}{\text{SST}_x}\sum_i d_i\,\mathbb{E}(u_i) = \beta_1 + \frac{1}{\text{SST}_x}\sum_i d_i\cdot 0 = \beta_1 \;\;\blacksquare
$$

> [!warning] What unbiasedness does and does not promise
> > *"Unbiasedness is a feature of the sampling distributions of $\hat\beta_1$ and $\hat\beta_0$, which says **nothing about the estimate that we obtain for a given sample**. We hope that, if the sample we obtain is somehow 'typical', then our estimate should be 'near' the population value. Unfortunately, it is always possible that we could obtain an unlucky sample that would give us a point estimate far from $\beta_1$, and **we can never know for sure whether this is the case**."*
>
> Unbiasedness is a property of the *procedure*, averaged over hypothetical repeated samples — **not a guarantee about your one estimate.**

#### Which assumption to worry about

*"Unbiasedness generally fails if any of our four assumptions fail... **The assumption we should concentrate on for now is SLR.4.** If SLR.4 holds, the OLS estimators are unbiased. Likewise, if SLR.4 fails, the OLS estimators generally will be biased."*

> **Example 2.12 — Math performance and the school lunch program.**
> $$\widehat{math10} = 32.14 - 0.319\,lnchprg$$
> **A 10-percentage-point rise in lunch-program eligibility predicts a 3.2-point fall in the maths pass rate.**
>
> *"**Do we really believe that higher participation in the lunch program actually causes worse performance? Almost certainly not.** A better explanation is that the error term $u$ is correlated with $lnchprg$. In fact, $u$ contains factors such as the **poverty rate** of children attending school, which affects student performance and is highly correlated with eligibility in the lunch program. Variables such as **school quality and resources** are also contained in $u$."*
>
> **This is the cleanest illustration in the chapter of a coefficient that is real, statistically strong, and causally meaningless.**

---

### 7. Variances of the OLS estimators

#### Assumption SLR.5 — Homoskedasticity

$$
\mathrm{Var}(u\mid x) = \sigma^2
$$

**The error has the same variance given any value of the explanatory variable.** Equivalently, in terms of $y$:

$$
\mathbb{E}(y\mid x) = \beta_0+\beta_1x \tag{2.55}
\qquad\qquad
\mathrm{Var}(y\mid x) = \sigma^2 \tag{2.56}
$$

**When $\mathrm{Var}(u\mid x)$ depends on $x$, the error exhibits *heteroskedasticity*.** Since $\mathrm{Var}(u\mid x)=\mathrm{Var}(y\mid x)$, **heteroskedasticity is present whenever $\mathrm{Var}(y\mid x)$ is a function of $x$.**

> [!example] Example 2.13 — Why homoskedasticity is doubtful in the wage equation
> Homoskedasticity requires $\mathrm{Var}(wage\mid educ)=\sigma^2$: *"while average wage is allowed to increase with education level, **the variability in wage about its mean is assumed to be constant across all education levels.**"*
>
> *"This may not be realistic. It is likely that people with more education have a wider variety of interests and job opportunities, which could lead to more wage variability at higher levels of education. People with very low levels of education have fewer opportunities and often must work at the minimum wage; this serves to reduce wage variability at low education levels."*
>
> **Whether SLR.5 holds is an empirical issue** — tested in [[08 - Heteroskedasticity]].

> [!important] SLR.5 is **not** needed for unbiasedness
> Unbiasedness needs only SLR.1–SLR.4. **Homoskedasticity is added purely to get simple variance formulas** — and later, in [[03 - Multiple Regression Analysis - Estimation|chapter 3]], for the Gauss–Markov theorem. **If it fails, $\hat\beta_1$ is still unbiased; only the standard errors are wrong.** That distinction is worth a great deal of exam credit.

#### Theorem 2.2 — Sampling variances

**Under SLR.1–SLR.5, conditional on the sample values of $x$:**

$$
\boxed{\;\mathrm{Var}(\hat\beta_1) = \frac{\sigma^2}{\sum_{i=1}^n(x_i-\bar x)^2} = \frac{\sigma^2}{\text{SST}_x}\;} \tag{2.57}
$$
$$
\mathrm{Var}(\hat\beta_0) = \frac{\sigma^2\,n^{-1}\sum_{i=1}^n x_i^2}{\sum_{i=1}^n(x_i-\bar x)^2} \tag{2.58}
$$

> [!important] Read (2.57) — it tells you how to design a study
> $$\mathrm{Var}(\hat\beta_1) = \frac{\sigma^2}{\text{SST}_x}$$
>
> | Driver | Effect on precision | Why |
> |---|---|---|
> | **Larger error variance $\sigma^2$** | **Worse** | *"More variation in the unobservables affecting $y$ makes it more difficult to precisely estimate $\beta_1$."* |
> | **More variability in $x$** (larger $\text{SST}_x$) | **Better** | *"The more spread out is the sample of independent variables, the easier it is to trace out the relationship between $\mathbb{E}(y\mid x)$ and $x$."* |
> | **Larger $n$** | **Better** | Increasing $n$ increases $\text{SST}_x$ |
>
> *"If we are interested in $\beta_1$ and we have a choice, then we should choose the $x_i$ to be as spread out as possible. **This is sometimes possible with experimental data, but rarely do we have this luxury in the social sciences.**"*

**These are the "standard" formulas, and they are invalid under heteroskedasticity** — the reason [[08 - Heteroskedasticity]] exists.

#### Estimating $\sigma^2$

**Errors are not residuals.** From (2.32) and (2.48):

$$
\hat u_i = u_i - (\hat\beta_0-\beta_0) - (\hat\beta_1-\beta_1)x_i \tag{2.59}
$$

*"The errors show up in the equation containing the population parameters. The residuals show up in the estimated equation. **The errors are never observed, while the residuals are computed from the data.**"*

Since $\sigma^2 = \mathbb{E}(u^2)$, a natural estimator would be $n^{-1}\sum \hat u_i^2 = \text{SSR}/n$ — but this is **biased**, because **the OLS residuals satisfy two restrictions**:

$$
\sum_{i=1}^n\hat u_i = 0, \qquad \sum_{i=1}^n x_i\hat u_i = 0 \tag{2.60}
$$

*"If we know $n-2$ of the residuals, we can always get the other two."* Hence **there are only $n-2$ degrees of freedom in the OLS residuals**, and the unbiased estimator makes a degrees-of-freedom adjustment:

$$
\boxed{\;\hat\sigma^2 = \frac{1}{n-2}\sum_{i=1}^n\hat u_i^2 = \frac{\text{SSR}}{n-2}\;} \tag{2.61}
$$

The **standard error of the regression (SER)** is

$$
\hat\sigma = \sqrt{\hat\sigma^2} \tag{2.62}
$$

*"$\hat\sigma$ is an estimate of the standard deviation in the unobservables affecting $y$; equivalently, it estimates the standard deviation in $y$ after the effect of $x$ has been taken out."* (It is **consistent** but not unbiased for $\sigma$.)

Finally, the **standard error of $\hat\beta_1$**:

$$
\boxed{\;\mathrm{se}(\hat\beta_1) = \frac{\hat\sigma}{\sqrt{\text{SST}_x}}\;}
$$

> [!note] $\mathrm{se}(\hat\beta_1)$ is a random variable *across* samples and a number *within* one
> *"$\mathrm{se}(\hat\beta_1)$ is viewed as a random variable when we think of running OLS over different samples, because $\hat\sigma$ varies with different samples. For a given sample, $\mathrm{se}(\hat\beta_1)$ is a number."* **Standard errors are used to build every test statistic and confidence interval from [[04 - Multiple Regression Analysis - Inference|chapter 4]] onward.**

---

### 8. Two special cases

#### Regression through the origin

Occasionally we impose $\hat y = 0$ when $x=0$ — for example, **zero income must mean zero income tax revenue.** The estimator becomes $\tilde\beta_1 = \sum x_iy_i / \sum x_i^2$.

> [!warning] Do this rarely, and know the cost
> *"Obtaining an estimate of $\beta_1$ using regression through the origin is not done very often in applied work, and for good reason: **if the intercept $\beta_0\neq0$, then $\tilde\beta_1$ is a biased estimator of $\beta_1$**."*
>
> **The reported $R^2$ is also misleading.** Software usually computes $1-\text{SSR}/\sum y_i^2$, whose denominator *"acts as if we know the average value of $y$ in the population is zero."* Using the usual SST instead **can make $R^2$ negative** — which is actually informative: it means **using $\bar y$ predicts better than the through-the-origin regression.**

**Regressing on a constant only** (no $x$) gives $\hat\beta_0=\bar y$ — *"the constant that produces the smallest sum of squared deviations is always the sample average."*

#### Regression on a binary explanatory variable

Suppose $x\in\{0,1\}$. With SLR.4, $\mathbb{E}(y\mid x)=\beta_0+\beta_1x$, so

$$
\mathbb{E}(y\mid x=0)=\beta_0
\qquad
\mathbb{E}(y\mid x=1)=\beta_0+\beta_1
$$

$$
\boxed{\;\beta_1 = \mathbb{E}(y\mid x=1) - \mathbb{E}(y\mid x=0)\;} \tag{2.72}
$$

> [!important] **OLS with a binary regressor *is* a difference in means**
> This is the bridge between regression and the two-sample comparison from [[Mathematical Statistics/contents/08 - Inferences on Two Samples|introductory statistics]] — they are the same calculation. **This is why Wooldridge introduces binary variables this early:** it lets him link OLS directly to the **potential-outcomes** framework of [[01 - The Nature of Econometrics and Economic Data]].
>
> Writing $y(0)$ and $y(1)$ for the two potential outcomes and $x$ for treatment status, $\beta_1$ is the **average treatment effect** — *provided* SLR.4 holds, which under **random assignment it does by construction.**
>
> **As with all simple regressions, $\beta_1$ can be merely descriptive, or it can be a causal effect of an intervention — and only the assignment mechanism decides which.**

---

## ✏️ Exercises

> [!note] The textbook's end-of-chapter computer exercises require data files (`WAGE1`, `CEOSAL1`, `VOTE1`, `MEAP93`, …) that are **not in the vault** — only the PDF is present. The exercises below are my own construction, using figures reported in the text.

### Exercise 1 — Interpret four regressions

Using the estimated equations in §3 and §5, answer:

(a) In (2.39), what is the predicted salary of a CEO whose firm has $roe = 25$?
(b) In (2.27), by how much does predicted wage rise going from 12 to 16 years of education?
(c) In (2.44), by how much does predicted wage rise over the same change?
(d) Why do (b) and (c) differ, and which is more plausible?

> [!example]- Solution
> **(a)** $\widehat{salary} = 963.191 + 18.501(25) = 963.191 + 462.525 = \mathbf{1{,}425.72}$, i.e. **about \$1,425,700** (salary is in thousands).
>
> **(b) Level-level.** $\Delta\widehat{wage} = 0.54 \times 4 = \mathbf{\$2.16}$ per hour — **the same $2.16 regardless of the starting level**, by construction.
>
> **(c) Log-level.** $\Delta\widehat{\log(wage)} = 0.083\times4 = 0.332$, so wage rises by approximately $\mathbf{33.2\%}$.
>
> The exact figure is $e^{0.332}-1 = 0.394$, i.e. **39.4%** — the approximation $100\beta_1$ is good for small changes but understates larger ones. **Report the exact form when the change exceeds about 10–15%.**
>
> Starting from the sample mean $\bar{wage}=5.90$, a 39.4% rise is about **\$2.32 per hour** — comparable to (b), but the *mechanism* differs.
>
> **(d) Why they differ, and which to prefer.**
>
> | | Level-level (2.27) | Log-level (2.44) |
> |---|---|---|
> | Constant thing | **Dollar** increase per year | **Percentage** increase per year |
> | Effect at $educ$ = 4 → 5 | +\$0.54 | +8.3% of a small wage ≈ +\$0.25 |
> | Effect at $educ$ = 18 → 19 | +\$0.54 | +8.3% of a large wage ≈ +\$1.00 |
>
> **The log model is far more plausible.** A year of education adding a *fixed 54 cents* to everyone from a school-leaver to a PhD is economically implausible; a *fixed percentage* is exactly how returns to human capital are usually theorised, and it is why $\log(wage)$ is the near-universal choice in labour economics.
>
> **Note also the $R^2$ figures: 0.186 for the log model.** These are **not comparable** with the level model's $R^2$, because **the dependent variables are different.**

---

### Exercise 2 — Is $\mathbb{E}(u\mid x)=0$ plausible?

For each regression, state what is in $u$, and argue whether SLR.4 is plausible. If not, give the likely **direction** of bias on $\hat\beta_1$.

(a) $\widehat{math10} = 32.14 - 0.319\,lnchprg$ (Example 2.12)
(b) $\widehat{voteA} = 26.81 + 0.464\,shareA$ (Example 2.5)
(c) A randomised experiment: $\widehat{yield} = \beta_0 + \beta_1\,fertilizer$, with fertilizer amounts assigned by coin flip.
(d) $\widehat{salary} = 963.191 + 18.501\,roe$ (Example 2.3)

> [!example]- Solution
> **(a) Almost certainly violated — this is Wooldridge's own example.**
>
> $u$ contains the **poverty rate** of the school's catchment, **parental education**, **school resources and quality**, **neighbourhood characteristics**. Every one is **strongly correlated with lunch-programme eligibility** and independently affects test scores.
>
> **Direction:** poverty ↓ scores and poverty ↑ $lnchprg$, so the correlation between $u$ and $x$ is **negative**, making $\hat\beta_1$ **too negative**. The true causal effect of the lunch programme is plausibly **zero or positive** — feeding hungry children does not lower test scores.
>
> **This is the ideal cautionary example** precisely because the sign is not merely biased but almost certainly *reversed*.
>
> **(b) Doubtful, and the direction is ambiguous.**
>
> $u$ contains **candidate quality**, **incumbency**, **party strength in the district**, **national political conditions**, **the absolute dollar amounts spent**.
>
> The central problem is **reverse causality**: **strong candidates attract donations.** So a high spending share may *reflect* an expectation of winning rather than cause it. That pushes $\hat\beta_1$ **upward**.
>
> Wooldridge is appropriately hedged: *"Whether or not this is a causal effect is unclear, but it is not unbelievable."*
>
> **(c) SLR.4 holds by construction.**
>
> Because fertilizer is assigned by **coin flip**, it is **independent of everything** — soil quality, drainage, sunlight, prior land use. So $\mathbb{E}(u\mid fertilizer) = \mathbb{E}(u) = 0$ automatically, **and you never even need to know what is in $u$.**
>
> **This is the entire value of randomisation**, and the reason [[01 - The Nature of Econometrics and Economic Data]] treats the impossibility of experiments as the defining problem of the field.
>
> **(d) Violated, but the story is subtler.**
>
> $u$ contains **firm size**, **industry**, **CEO tenure and ability**, **board composition**, **market conditions**. Larger firms pay more *and* may have systematically different returns on equity.
>
> The more interesting problem is **simultaneity**: a talented CEO **both** raises $roe$ **and** commands a high salary, so ability sits in $u$ and is positively correlated with $roe$. **Direction: upward bias.**
>
> **The $R^2$ of 0.0132 is a hint of the wider problem** — with 98.7% of salary variation unexplained, there is an enormous amount in $u$ for $roe$ to be correlated with.

---

### Exercise 3 — Algebra of OLS

A researcher runs a simple regression and reports: $n = 40$, $\sum(x_i-\bar x)^2 = 250$, $\text{SSR} = 180$, $\bar x = 10$, $\bar y = 25$, $\hat\beta_1 = 1.4$.

(a) Find $\hat\beta_0$. (b) Find $\hat\sigma^2$ and the SER. (c) Find $\mathrm{se}(\hat\beta_1)$. (d) If SST $= 320$, find $R^2$ and verify consistency with SSR. (e) The researcher now measures $y$ in cents rather than dollars. What happens to $\hat\beta_1$, $\mathrm{se}(\hat\beta_1)$, and $R^2$?

> [!example]- Solution
> **(a)** From (2.17): $\hat\beta_0 = \bar y - \hat\beta_1\bar x = 25 - 1.4(10) = \mathbf{11}$.
>
> **(b)** From (2.61), with $n-2 = 38$ degrees of freedom:
> $$\hat\sigma^2 = \frac{\text{SSR}}{n-2} = \frac{180}{38} = \mathbf{4.7368}
> \qquad
> \text{SER} = \hat\sigma = \sqrt{4.7368} = \mathbf{2.176}$$
>
> **(c)** $$\mathrm{se}(\hat\beta_1) = \frac{\hat\sigma}{\sqrt{\text{SST}_x}} = \frac{2.176}{\sqrt{250}} = \frac{2.176}{15.811} = \mathbf{0.1376}$$
>
> **(d)** $$R^2 = 1 - \frac{\text{SSR}}{\text{SST}} = 1 - \frac{180}{320} = \mathbf{0.4375}$$
> Check via SSE: $\text{SSE} = \text{SST}-\text{SSR} = 320-180 = 140$, and $140/320 = 0.4375$ ✓
>
> **(e) Rescaling $y$ by $c=100$:**
>
> | Quantity | New value | Why |
> |---|---|---|
> | $\hat\beta_1$ | $\mathbf{140}$ | Multiplied by 100 |
> | $\hat\beta_0$ | 1,100 | Multiplied by 100 |
> | SSR | $180\times100^2 = 1{,}800{,}000$ | Residuals ×100, then squared |
> | $\hat\sigma$, SER | $217.6$ | Multiplied by 100 |
> | $\mathrm{se}(\hat\beta_1)$ | $\mathbf{13.76}$ | Multiplied by 100 |
> | $R^2$ | $\mathbf{0.4375}$ — **unchanged** | SSR and SST both ×$100^2$; the ratio is invariant |
>
> **The point of (e):** $\hat\beta_1$ and $\mathrm{se}(\hat\beta_1)$ scale **together**, so their **ratio** — the $t$ statistic of [[04 - Multiple Regression Analysis - Inference|chapter 4]] — is $1.4/0.1376 = 140/13.76 = \mathbf{10.17}$ either way.
>
> **Statistical significance cannot be manufactured by changing units.** That invariance is a useful sanity check on any regression output.

---

### Exercise 4 — Binary regressor and potential outcomes

A firm runs a training programme. Of 200 workers, 80 were assigned to training **by lottery**. Post-training productivity averages 47.2 for the trained and 41.6 for the untrained.

(a) Write the regression and give $\hat\beta_0$ and $\hat\beta_1$. (b) Interpret $\hat\beta_1$ in potential-outcomes language. (c) What changes if workers had *volunteered* instead? (d) What if the firm had assigned its **best** workers to training?

> [!example]- Solution
> **(a)** With $train_i \in\{0,1\}$:
> $$prod_i = \beta_0 + \beta_1 train_i + u_i$$
> From (2.70)–(2.72):
> $$\hat\beta_0 = \overline{prod}\mid_{train=0} = \mathbf{41.6}
> \qquad
> \hat\beta_1 = 47.2 - 41.6 = \mathbf{5.6}$$
> **OLS on a binary regressor is exactly the difference in group means.**
>
> **(b) Under lottery assignment, $\hat\beta_1$ estimates the average treatment effect.**
>
> In potential-outcomes notation, each worker has $prod(0)$ and $prod(1)$; we want $\mathbb{E}[prod(1)-prod(0)]$. **We observe each worker in only one state** — the fundamental problem of [[01 - The Nature of Econometrics and Economic Data]].
>
> **But the lottery makes $train$ independent of $(prod(0),prod(1))$ and of everything in $u$.** So
> $$\mathbb{E}(u\mid train)=0$$
> **holds by construction — SLR.4 is satisfied**, and $\hat\beta_1 = 5.6$ is an unbiased estimate of the average causal effect: **training raises productivity by about 5.6 units.**
>
> **(c) Voluntary participation destroys this.**
>
> Volunteers are plausibly **more motivated, more ambitious, or more worried about their jobs** — all of which raise productivity independently. Motivation sits in $u$ and is **positively correlated** with $train$, so
> $$\mathbb{E}(u\mid train=1) > \mathbb{E}(u\mid train=0) \;\Longrightarrow\; \text{SLR.4 fails}$$
> **$\hat\beta_1$ is biased upward**: the 5.6 mixes the training effect with the selection effect, and the true causal effect is **smaller** — possibly zero.
>
> **This is precisely the job-training example that opens [[01 - The Nature of Econometrics and Economic Data|chapter 1]]**, where enrolment is described as voluntary.
>
> **(d) Assigning the best workers makes it worse and the direction is still up.**
>
> Now $train$ is deliberately correlated with prior ability, giving a **large upward bias.** A firm could report a "5.6-point training effect" that is **entirely** the pre-existing gap between its best and worst workers.
>
> **Worth noting the opposite case:** had the firm assigned training to its **struggling** workers — remedial training, the usual practice — the bias would be **downward**, and the programme could look harmful even if it helps. **This is exactly the class-size selection problem** from [[01 - The Nature of Econometrics and Economic Data]] Exercise 2.
>
> **General lesson: with a binary regressor, the entire causal question reduces to "how were units assigned?"** The arithmetic is trivial; the assignment mechanism is everything.

---

### Exercise 5 — Derive and interpret

(a) Starting from (2.52), show that if $\mathbb{E}(u_i\mid x)=\delta \neq 0$ (a constant), $\hat\beta_1$ is still unbiased but $\hat\beta_0$ is not. (b) Show $R^2$ is invariant to rescaling $x$. (c) Explain why $\sum \hat u_i = 0$ does **not** imply $\mathbb{E}(u\mid x)=0$.

> [!example]- Solution
> **(a)** From (2.52), $\hat\beta_1 = \beta_1 + \frac{1}{\text{SST}_x}\sum_i d_iu_i$ with $d_i = x_i-\bar x$. Taking expectations conditional on the $x$'s:
> $$\mathbb{E}(\hat\beta_1) = \beta_1 + \frac{1}{\text{SST}_x}\sum_i d_i\,\mathbb{E}(u_i) = \beta_1 + \frac{\delta}{\text{SST}_x}\sum_i d_i$$
> But $\sum_i d_i = \sum_i(x_i-\bar x) = \mathbf{0}$, so $\mathbb{E}(\hat\beta_1)=\beta_1$ — **still unbiased.**
>
> For the intercept, $\hat\beta_0 = \bar y - \hat\beta_1\bar x$ and $\bar y = \beta_0+\beta_1\bar x+\bar u$, so
> $$\mathbb{E}(\hat\beta_0) = \beta_0 + \mathbb{E}(\bar u) - \bar x\,[\mathbb{E}(\hat\beta_1)-\beta_1] = \beta_0 + \delta$$
> **$\hat\beta_0$ is biased by exactly $\delta$.**
>
> **Why this matters conceptually:** a **constant** non-zero mean in $u$ is harmless for the slope — it is simply absorbed into the intercept. **This is exactly why (2.5) is described as "essentially defining the intercept" and (2.6) as "the assumption with impact."** Only *dependence of $\mathbb{E}(u\mid x)$ on $x$* biases the slope.
>
> **(b)** Replace $x_i$ by $cx_i$. From §5, the new slope is $\hat\beta_1/c$ and the new intercept is unchanged. So each fitted value is
> $$\hat y_i^{new} = \hat\beta_0 + (\hat\beta_1/c)(cx_i) = \hat\beta_0+\hat\beta_1x_i = \hat y_i$$
> **The fitted values are numerically identical**, hence so are the residuals, hence SSE, SSR and SST are all unchanged, hence $R^2$ is unchanged. ∎
>
> (The same argument shows rescaling $y$ multiplies SSE, SSR and SST all by $c^2$, again leaving the ratio fixed.)
>
> **(c) This is the most important conceptual point in the chapter.**
>
> $\sum\hat u_i = 0$ and $\sum x_i\hat u_i = 0$ are the **first order conditions** — they hold **by construction, in every sample, for any data whatsoever.** OLS *chooses* $\hat\beta_0,\hat\beta_1$ to force them.
>
> $\mathbb{E}(u\mid x)=0$ is a statement about the **unobservable population errors**, and it is either true or false about the world **before you collect any data.**
>
> $$\underbrace{\hat u_i}_{\text{computed, observed}} \;\neq\; \underbrace{u_i}_{\text{never observed}}$$
>
> Recall (2.59): $\hat u_i = u_i - (\hat\beta_0-\beta_0)-(\hat\beta_1-\beta_1)x_i$.
>
> **The practical consequence:** running the lunch-programme regression of Example 2.12 produces residuals that sum to zero and are uncorrelated with $lnchprg$ — **and the estimate is still badly biased.** No residual diagnostic can detect a violation of SLR.4, because **OLS has already imposed the sample analogue of the condition it is violating.**
>
> **This is why econometrics is an argument about assumptions rather than a set of diagnostic tests**, and it is the single idea most worth carrying into the rest of the course.

---

## 📝 Summary

- **The simple linear regression model is $y = \beta_0+\beta_1x+u$**, assumed to hold in the population. $\beta_1$ is the **slope**, giving $\Delta y = \beta_1\Delta x$ when $\Delta u=0$; $u$ collects **all unobserved factors**.
- **$\mathbb{E}(u)=0$ is a free normalisation that defines the intercept.** **$\mathbb{E}(u\mid x)=\mathbb{E}(u)$ — mean independence — is the assumption with impact.** Together they give the **zero conditional mean assumption $\mathbb{E}(u\mid x)=0$** and the **population regression function $\mathbb{E}(y\mid x)=\beta_0+\beta_1x$**.
- **OLS solves the sample analogues of $\mathbb{E}(u)=0$ and $\mathrm{Cov}(x,u)=0$**, giving
  $$\hat\beta_1 = \frac{\sum(x_i-\bar x)(y_i-\bar y)}{\sum(x_i-\bar x)^2} = \hat\rho_{xy}\frac{\hat\sigma_y}{\hat\sigma_x}, \qquad \hat\beta_0 = \bar y - \hat\beta_1\bar x$$
  These are **identical** to the estimates that minimise $\sum\hat u_i^2$. **Because $\hat\beta_1$ is a scaled correlation, simple regression is in effect an analysis of correlation** — hence the care needed in inferring causality.
- **Algebraic properties, true in every sample:** $\sum\hat u_i = 0$, $\sum x_i\hat u_i = 0$, and $(\bar x,\bar y)$ lies on the line. **SST = SSE + SSR**, and $R^2 = \text{SSE}/\text{SST} = 1-\text{SSR}/\text{SST}$ is the **fraction of sample variation in $y$ explained by $x$** — a measure of **fit, not of validity**.
- **Rescaling:** multiplying $y$ by $c$ multiplies both coefficients by $c$; multiplying $x$ by $c$ divides the slope by $c$ and leaves the intercept alone. **$R^2$ is invariant to both.**
- **Four functional forms:** level-level, level-log, **log-level (semi-elasticity, $100\beta_1$ = percentage change)** and **log-log (elasticity)**. "Linear" means **linear in the parameters**, not in the variables.
- **Under SLR.1–SLR.4 (linearity, random sampling, sample variation in $x$, zero conditional mean), OLS is unbiased.** The key identity is
  $$\hat\beta_1 = \beta_1 + \frac{1}{\text{SST}_x}\sum_i(x_i-\bar x)u_i$$
  **SLR.4 is the one to worry about**; when it fails, OLS is biased.
- **Adding SLR.5 (homoskedasticity, $\mathrm{Var}(u\mid x)=\sigma^2$)** gives $\mathrm{Var}(\hat\beta_1) = \sigma^2/\text{SST}_x$: precision **falls** with error variance and **rises** with the spread of $x$ and with $n$. **Homoskedasticity is not needed for unbiasedness.**
- **$\hat\sigma^2 = \text{SSR}/(n-2)$** is unbiased for $\sigma^2$ (two restrictions cost two degrees of freedom); $\hat\sigma$ is the **SER**, and $\mathrm{se}(\hat\beta_1) = \hat\sigma/\sqrt{\text{SST}_x}$.
- **With a binary $x$, $\beta_1 = \mathbb{E}(y\mid x=1)-\mathbb{E}(y\mid x=0)$** — **OLS is a difference in means**, and under random assignment it estimates the **average treatment effect**.

---

## ⚠️ Important Notes

> [!warning] The algebraic properties prove nothing
> $\sum\hat u_i=0$ and $\sum x_i\hat u_i=0$ hold **by construction in every sample**, however wrong the model. **They are not evidence that $\mathbb{E}(u\mid x)=0$** — OLS forces the sample analogue of exactly the condition that may be failing. **No residual plot can detect endogeneity.**

> [!warning] Errors ≠ residuals
> $u_i$ is a population quantity, **never observed**. $\hat u_i$ is computed from the data, and $\hat u_i = u_i-(\hat\beta_0-\beta_0)-(\hat\beta_1-\beta_1)x_i$. Nearly every conceptual confusion in the chapter traces to conflating them.

> [!warning] $R^2$ is not a measure of model quality
> The CEO regression has $R^2=0.0132$ and the voting regression $R^2=0.856$ — **and neither figure bears on whether the coefficient is causal.** Low $R^2$ simply means $u$ matters a lot. **Never compare $R^2$ across models with different dependent variables** ($wage$ vs $\log(wage)$).

> [!important] Homoskedasticity is *not* needed for unbiasedness
> SLR.1–SLR.4 give unbiasedness. **SLR.5 buys only the simple variance formulas.** If heteroskedasticity is present, $\hat\beta_1$ remains unbiased and **only the standard errors are wrong** — fixable with robust standard errors in [[08 - Heteroskedasticity]].

> [!tip] Interpreting logs — the four cases, and when the approximation breaks
> | Model | $\beta_1$ means |
> |---|---|
> | $y$ on $x$ | $\Delta y = \beta_1\Delta x$ |
> | $y$ on $\log x$ | $\Delta y \approx (\beta_1/100)\%\Delta x$ |
> | $\log y$ on $x$ | $\%\Delta y \approx 100\beta_1\,\Delta x$ |
> | $\log y$ on $\log x$ | $\%\Delta y = \beta_1\%\Delta x$ (elasticity) |
>
> **The $100\beta_1$ approximation degrades above ~10–15%.** For a change of $\Delta$ in $\log(y)$, the exact percentage change is $100(e^{\Delta}-1)$.

> [!note] Why $n-2$ and not $n$
> The residuals satisfy **two** linear restrictions, so only $n-2$ are free. In [[03 - Multiple Regression Analysis - Estimation|multiple regression]] with $k$ regressors this becomes $n-k-1$ — same logic, one restriction per estimated parameter.

> [!warning] Source-material note
> Written from the **Wooldridge 7th edition PDF** (pp. 20–65). The text extracts cleanly, but:
> - **All figures (2.1–2.9) are images** — the scatterplots, the PRF diagram, the homoskedasticity/heteroskedasticity pictures. Their content is described in the surrounding text and reconstructed above.
> - **Equations extract with mangled symbols** (`b^ 1` for $\hat\beta_1$, `E1u0x2` for $\mathbb{E}(u\mid x)$, `g` for $\sum$). All equations above have been **transcribed and checked by hand** against the numbered references in the text.
> - **Table 2.2** (fitted values and residuals for 15 CEOs) extracts intact and was used to verify Example 2.6.
> - **The data files are not in the vault**, so no reported regression can be re-estimated. **The reported coefficients and $R^2$ values are quoted as printed.**
> - **There are no lecture slides for this subject** — the chapter scope for these notes is my own editorial decision. See [[00-Index]].

---

**Previous:** [[01 - The Nature of Econometrics and Economic Data]] · **Next:** [[03 - Multiple Regression Analysis - Estimation]] · **Index:** [[00-Index]]

#econometrics #ols #simple-regression #zero-conditional-mean #r-squared #functional-form #unbiasedness
