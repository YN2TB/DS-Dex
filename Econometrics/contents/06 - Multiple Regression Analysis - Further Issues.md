---
subject: Econometrics
chapter: 06
tags: [ds, econometrics, regression, functional-form, prediction]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 6 (pp. 181–219)"
---

# Multiple Regression Analysis: Further Issues

> [!abstract] What this chapter is for
> Chapters [[03 - Multiple Regression Analysis - Estimation|03]]–[[05 - Multiple Regression Analysis - OLS Asymptotics|05]] built the machinery: estimate, test, and know when it works. **This chapter is about what you actually write down.** The model $y=\beta_0+\beta_1x_1+\cdots+u$ is a *choice*, and the choice has consequences that no amount of correct inference can repair.
>
> Four questions:
> 1. **Do units matter?** (§1) No — but you must be able to prove it.
> 2. **Is the relationship a straight line?** (§2) Usually not. Logs, quadratics, interactions.
> 3. **How do I choose between models?** (§3) $\bar R^2$ — and a warning about when goodness-of-fit is exactly the wrong criterion.
> 4. **How do I predict, and how wrong will I be?** (§4)
>
> Wooldridge: *"These topics are not as fundamental as the material in Chapters 3 and 4, but they are important for applying multiple regression to a broad range of empirical problems."*

---

## 📘 Main Knowledge

### 1. Data scaling — everything essential is invariant

Suppose you rescale a variable. **Nothing that matters changes.** That is the whole result, but the bookkeeping is worth knowing cold because it appears on exams.

#### The three cases

| You multiply… | Coefficients | Standard errors | $t$, $F$, $R^2$ | SSR | SER $\hat\sigma$ |
|---|---|---|---|---|---|
| **$y$ by $c$** | **all** $\times c$ (incl. intercept) | all $\times c$ | **unchanged** | $\times c^2$ | $\times c$ |
| **$x_j$ by $c$** | $\hat\beta_j \div c$; others unchanged | $\mathrm{se}(\hat\beta_j)\div c$ | **unchanged** | unchanged | unchanged |
| **either, in logs** | slopes **unchanged**; only the **intercept** moves | unchanged | unchanged | unchanged | unchanged |

> [!important] Why the log case is special
> $$\log(c_1 y_i)=\log(c_1)+\log(y_i)$$
> The rescaling is absorbed **entirely into the intercept**: $\hat\beta_0^{\text{new}} = \log(c_1)+\hat\beta_0$. Every slope is untouched.
>
> **This is the same fact as "elasticities and semi-elasticities are unit-free."** If $\log(x_j)$ appears, rescaling $x_j$ likewise moves only the intercept.

#### Worked example — birth weight (Table 6.1)

$$\widehat{bwght} = 116.974 - 0.4634\,cigs + 0.0927\,faminc$$
$$\qquad (1.049)\quad\;\;(0.0916)\qquad\;\;(0.0292)$$
$$n=1{,}388,\quad R^2=0.0298,\quad \text{SSR}=557{,}485.51,\quad \text{SER}=20.063$$

**Change $y$ to pounds** ($bwghtlbs = bwght/16$, so $c=1/16$):

$$\widehat{bwghtlbs} = 7.3109 - 0.0289\,cigs + 0.0058\,faminc$$
$$\qquad (0.0656)\quad\;\;(0.0057)\qquad\;\;(0.0018)$$

- Every coefficient and standard error is $\tfrac1{16}$ of before. $t$ on $cigs$ is $-5.06$ **in both**.
- SSR: $557{,}485.51/256 = 2{,}177.68$ — divided by $\mathbf{16^2=256}$, because residuals are divided by 16 and then **squared**.
- SER: $20.063/16=1.2539$. ✓ (Check: $\sqrt{2177.68/1385}=1.2539$.)

> [!warning] The SER trap
> The SER **fell from 20.06 to 1.25.** *That is not a better-fitting model.* Nothing about the fit changed — $R^2$ is $0.0298$ in both. **The SER is in the units of $y$**, so comparing SERs across differently-scaled dependent variables is meaningless. $R^2$ is the unit-free one.

**Change $x$ to packs** ($packs = cigs/20$, so $c=1/20$ and the coefficient is *multiplied* by 20):

$$\widehat{bwght} = 116.974 - 9.268\,packs + 0.0927\,faminc$$
$$\qquad (1.049)\quad\;\;(1.832)\qquad\;\;(0.0292)$$

The intercept, $faminc$, $R^2$, SSR and SER are **all identical to column (1)**. Only $cigs \to packs$ changed, and its $t$ is unchanged: $-9.268/1.832 = -5.06$.

> [!note] Never include both $cigs$ and $packs$
> $packs = cigs/20$ exactly. That is **perfect collinearity** — a violation of MLR.3, and OLS cannot be computed. See [[03 - Multiple Regression Analysis - Estimation|ch. 03]].

**The practical use of all this:** cosmetics. Rescale to kill leading zeros. `−0.000214` reads badly; `−0.214` reads well; the economics is identical.

---

### 1a. Beta coefficients (standardized coefficients)

**The problem.** You cannot look at two coefficients and say "this one is bigger, so this variable matters more" — **the magnitudes are whatever the units make them.** Multiply a regressor by 1,000 and its coefficient shrinks by 1,000 with no change in substance.

**The fix.** Standardize everything to $z$-scores and rerun. Starting from
$$y_i = \hat\beta_0+\hat\beta_1x_{i1}+\cdots+\hat\beta_kx_{ik}+\hat u_i$$
average, subtract, and divide through by $\hat\sigma_y$:

$$\frac{y_i-\bar y}{\hat\sigma_y}=\left(\frac{\hat\sigma_1}{\hat\sigma_y}\hat\beta_1\right)\frac{x_{i1}-\bar x_1}{\hat\sigma_1}+\cdots+\frac{\hat u_i}{\hat\sigma_y}$$

which is
$$\boxed{\;\hat z_y = \hat b_1 z_1 + \hat b_2 z_2 + \cdots + \hat b_k z_k, \qquad \hat b_j = \left(\frac{\hat\sigma_j}{\hat\sigma_y}\right)\hat\beta_j\;}$$

**The intercept vanishes** (every $z$ has mean zero).

> [!important] Interpretation
> **A one-standard-deviation increase in $x_j$ changes $\hat y$ by $\hat b_j$ standard deviations.**
>
> - Now the regressors are on **equal footing** — comparing $|\hat b_j|$ is a defensible statement about relative importance.
> - With **one** regressor, $\hat b_1$ is exactly the **sample correlation** $\hat\rho_{yx}$, so $|\hat b_1|\le 1$. With several regressors there is **no such bound**.
> - **$t$ statistics are identical** before and after standardizing. Standardization is about *interpretation*, never about *significance*.

**Example 6.1 — pollution and housing prices** (`HPRICE2`, $n=506$):

$$\hat z_{price} = -0.340\,z_{nox} - 0.143\,z_{crime} + 0.514\,z_{rooms} - 0.235\,z_{dist} - 0.270\,z_{stratio}$$

- One sd more pollution $\Rightarrow$ price falls $0.34$ sd. One sd more crime $\Rightarrow$ $0.14$ sd.
- **Pollution moves house prices about 2.4× as much as crime**, per standard deviation.
- **$rooms$ has the largest standardized effect** ($0.514$) — house size dominates everything environmental.

> [!tip] Betas are useful even when coefficients are already interpretable
> Elasticities are unit-free, so why standardize? Because **"a 10% change" is not equally realistic for every variable.** In a state with huge income variation but tiny spending variation, a 10% income change is routine and a 10% spending change is unheard of. Beta coefficients scale by *what the data actually vary by*.

---

### 2. Functional form

#### 2a. Logs — the exact percentage change

The familiar approximation $\%\Delta y \approx 100\cdot\Delta\log(y)$ **degrades as the change gets bigger.** The exact version:

$$\boxed{\;\%\Delta\hat y = 100\left[\exp(\hat\beta_2\Delta x_2)-1\right]\;}\qquad\text{and for }\Delta x_2=1:\quad 100\left[\exp(\hat\beta_2)-1\right]$$

**Housing prices** (`HPRICE2`):
$$\widehat{\log(price)} = 9.23 - 0.718\log(nox) + 0.306\,rooms$$
$$\qquad\;\; (0.19)\quad\;\;(0.066)\qquad\;\;\;(0.019)\qquad n=506,\; R^2=0.514$$

| Change | Approximate | Exact |
|---|---|---|
| $rooms$: $+1$ | $+30.6\%$ | $100[e^{0.306}-1]=\mathbf{+35.8\%}$ |
| $rooms$: $-1$ | $-30.6\%$ | $100[e^{-0.306}-1]=\mathbf{-26.4\%}$ |
| $stratio$: $+1$ ($\hat\beta=-0.052$) | $-5.2\%$ | $-5.1\%$ |
| $stratio$: $+5$ | $-26\%$ | $100[e^{-0.26}-1]=\mathbf{-22.9\%}$ |

> [!important] Why the approximation is still worth reporting
> $$-26.4\% \;<\; 30.6\% \;<\; 35.8\%$$
> **The log coefficient always lands between the absolute values of the increase and the decrease.** It is a *symmetric summary* of an asymmetric effect — the same idea as an **arc elasticity** in intro micro, where you use average price and quantity so the answer doesn't depend on which end you start from.
>
> Use the exact formula when the question is specifically "what if it goes up by 1?"; report the coefficient when you want one number.

> [!warning] $100[\exp(\hat\beta_2)-1]$ is **consistent but biased**
> $\exp(\cdot)$ is nonlinear, and $\mathbb{E}$ does not pass through nonlinear functions — but $\operatorname{plim}$ **does**. So this is a [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] result: unbiasedness is lost, consistency survives.

#### When to take logs — the working rules

| Variable type | Log it? |
|---|---|
| **Positive dollar amounts** (wages, salaries, sales, market value) | **Yes, almost always** |
| **Large counts** (population, employees, enrollment) | **Usually yes** |
| **Measured in years** (education, experience, tenure, age) | **No** — keep in levels |
| **Already a percent or proportion** (unemployment rate, pass rate) | **Usually no** |
| **Can equal zero** | **Cannot** — see below |

**Four reasons logs are used so heavily:**
1. **Coefficients become elasticities/semi-elasticities** — unit-free and directly interpretable.
2. **The CLM assumptions hold better.** Strictly positive variables are typically **skewed and heteroskedastic**; the log mitigates both. Normality of $u$ becomes more plausible.
3. **The range narrows**, so OLS is **less sensitive to outliers** (see [[09 - More on Specification and Data Issues|ch. 09]]).
4. **Rescaling becomes irrelevant** — no need to know the units.

> [!warning] Three ways logs bite back
> 1. **Logs can *create* extreme values.** If $y$ is a proportion with values near zero, $\log(y)$ is a large negative number — **more** variable than $y$, not less.
> 2. **$\log(y)$ is undefined at $y=0$.** The common patch is $\log(1+y)$, tolerable when zeros are *rare*, but the percentage interpretation breaks at $y=0$ (where "% change" is undefined anyway), and $\log(1+y)$ **cannot be normally distributed**. The proper tools are Tobit and Poisson (Wooldridge ch. 17 — outside this scope).
> 3. **You cannot compare $R^2$ across $y$ and $\log(y)$ models.** They are explaining *different dependent variables*. §4c gives the fix.

> [!important] Percentage change vs percentage **point** change — the classic exam trap
> $unem$ goes from **8 to 9**.
> - **One percentage point** increase.
> - **$12.5\%$** increase ($1/8$).
> - $\log(9)-\log(8)=0.118$, so the **log approximation says $11.8\%$** — approximating the $12.5\%$, *not* the one point.
>
> **If $unem$ enters in levels, coefficients are per percentage point. If it enters in logs, they are per percent.** These differ by a factor of $unem$ itself.

#### 2b. Quadratics

$$y=\beta_0+\beta_1x+\beta_2x^2+u$$

> [!warning] $\beta_1$ is **not** the effect of $x$ on $y$
> "Hold $x^2$ fixed while changing $x$" is meaningless. The partial effect is
> $$\boxed{\;\frac{\Delta\hat y}{\Delta x}\approx \hat\beta_1+2\hat\beta_2 x\;}$$
> **It depends on where you are.** $\hat\beta_1$ alone is only the slope in going from $x=0$ to $x=1$.

**The turning point:**
$$\boxed{\;x^* = \left|\frac{\hat\beta_1}{2\hat\beta_2}\right|\;}\qquad\text{(signed version: } x^*=-\hat\beta_1/(2\hat\beta_2))$$

| $\hat\beta_1$ | $\hat\beta_2$ | Shape | Turning point |
|---|---|---|---|
| $+$ | $-$ | **Parabola** (rises then falls) | at $x^*>0$ — a **maximum** |
| $-$ | $+$ | **U-shape** (falls then rises) | at $x^*>0$ — a **minimum** |
| $+$ | $+$ | Increasing, **accelerating** | $x^*<0$ — **irrelevant** if $x\ge0$ |
| $-$ | $-$ | Decreasing, accelerating | $x^*<0$ — **irrelevant** if $x\ge0$ |

**Same signs $\Rightarrow$ no turning point in the relevant range.** Opposite signs $\Rightarrow$ there is one, and **you must compute it and ask whether it makes sense.**

**Example — wage and experience** (`WAGE1`, $n=526$):
$$\widehat{wage} = 3.73 + 0.298\,exper - 0.0061\,exper^2,\qquad R^2=0.093$$
$$\quad\;(0.35)\quad\;(0.041)\qquad\;\;(0.0009)$$

- 1st year of experience: $\approx\$0.298$/hour.
- 2nd year ($x=1$): $0.298-2(0.0061)(1)=\$0.286$.
- 10th→11th ($x=10$): $0.298-2(0.0061)(10)=\$0.176$.
- **Turning point:** $0.298/[2(0.0061)]=\mathbf{24.4}$ years — after which more experience *lowers* wage.

> [!warning] The turning point is a diagnostic, not a finding
> Wage falling after 24 years is not believable. **The right question is what fraction of the sample lies beyond it.** Here **about 28% do** — far too many to wave away. Wooldridge's diagnosis: the equation controls for **nothing else** (no education), and $\log(wage)$ would be the better dependent variable. **A silly turning point usually means a misspecified model, not a real reversal.**
>
> *The cost of using a quadratic to capture diminishing returns is that the quadratic must eventually turn around.* Whether that matters depends on **where** it turns relative to your data.

**Example 6.2 — a U-shape** (`HPRICE2`):
$$\widehat{\log(price)} = 13.39 - 0.902\log(nox) - 0.087\log(dist) - 0.545\,rooms + 0.062\,rooms^2 - 0.048\,stratio$$
$$\qquad (0.57)\qquad (0.115)\qquad\quad (0.043)\qquad\quad (0.165)\qquad\;\;(0.013)\qquad\;\;(0.006)$$
$$n=506,\quad R^2=0.603$$

$t$ on $rooms^2$ is $0.062/0.013\approx 4.77$ — **very significant**. Turning point: $0.545/[2(0.062)]=\mathbf{4.4}$ rooms. Below that, an extra room *lowers* price — absurd, but **only 5 of 506 communities (about 1%) are there**, so it is safely ignorable.

Above 4.4, the semi-elasticity is
$$\%\Delta price \approx (-54.5 + 12.4\,rooms)\,\Delta rooms$$

| $rooms$: from → to | $\%\Delta price$ |
|---|---|
| 5 → 6 | $-54.5+12.4(5) = \mathbf{+7.5\%}$ |
| 6 → 7 | $-54.5+12.4(6) = \mathbf{+19.9\%}$ |
| 7 → 8 | $-54.5+12.4(7) = \mathbf{+32.3\%}$ |

> [!important] Never dismiss a quadratic coefficient because it looks small
> $0.062$ looks like nothing. It is not — it is **how fast the slope is changing**, so it gets multiplied by $x$ and by $2$. Dropping $rooms^2$ gives a flat $+25.5\%$ per room at every $rooms$; the quadratic model **crosses $25.5\%$ at $rooms=6.45$** and diverges sharply on either side.
>
> **Rule: always compute the partial effect at real values of $x$ and compare it with the linear model's constant slope.** Magnitude of the squared coefficient tells you nothing on its own.

**Quadratics in logs.** $\log(price)$ on $\log(nox)$ and $[\log(nox)]^2$ gives a **non-constant elasticity**:
$$\%\Delta price \approx \left[\beta_1+2\beta_2\log(nox)\right]\%\Delta nox$$
so the elasticity itself depends on the pollution level. If $\beta_2=0$ we are back to constant elasticity.

Cubics and quartics are legal (a cost function $\beta_0+\beta_1q+\beta_2q^2+\beta_3q^3$ is standard) — estimation is unchanged, interpretation just gets messier.

#### 2c. Interaction terms

$$price=\beta_0+\beta_1 sqrft+\beta_2 bdrms+\beta_3\,(sqrft\cdot bdrms)+\beta_4 bthrms+u$$

$$\boxed{\;\frac{\Delta price}{\Delta bdrms}=\beta_2+\beta_3\,sqrft\;}$$

If $\beta_3>0$, **an extra bedroom is worth more in a bigger house** — the two variables *interact*.

> [!warning] $\beta_2$ is the effect of $bdrms$ in a house with **zero square feet**
> That is the single most misread coefficient in applied econometrics. **In a model with an interaction, the coefficient on a level term is the partial effect when the interacting variable equals zero** — and zero is often nonsense.

**The fix — centre the interaction.** Rewrite
$$y=\alpha_0+\delta_1x_1+\delta_2x_2+\beta_3(x_1-\mu_1)(x_2-\mu_2)+u$$

Multiplying out shows $\delta_2=\beta_2+\beta_3\mu_1$ — so **$\delta_2$ is the partial effect of $x_2$ at the mean of $x_1$**, and the regression hands you **its standard error for free**. Any other interesting value can replace $\mu_1$. (This is the same reparameterization device as in [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4 for testing linear combinations.)

**Example 6.3 — attendance and exam performance** (`ATTEND`, $n=680$):

$$stndfnl=\beta_0+\beta_1 atndrte+\beta_2 priGPA+\beta_3 ACT+\beta_4 priGPA^2+\beta_5 ACT^2+\beta_6\,priGPA\cdot atndrte+u$$

$$\widehat{stndfnl} = 2.05 - 0.0067\,atndrte - 1.63\,priGPA - 0.128\,ACT$$
$$\qquad\quad (1.36)\quad\;\;(0.0102)\qquad\;\;(0.48)\qquad\;(0.098)$$
$$\qquad\qquad + 0.296\,priGPA^2 + 0.0045\,ACT^2 + 0.0056\,priGPA\cdot atndrte$$
$$\qquad\qquad\;\;\, (0.101)\qquad\;\;(0.0022)\qquad\;\;(0.0043)$$
$$n=680,\quad R^2=0.229,\quad \bar R^2=0.222$$

**Two traps, both sprung at once:**

1. **The coefficient on $atndrte$ is $-0.0067$.** Reading that as "attending class hurts" is wrong — it is the effect **when $priGPA=0$**, and the *lowest* prior GPA in the sample is about $0.86$.
2. **Neither $\hat\beta_1$ nor $\hat\beta_6$ is individually significant**, yet the **$F$ test of $H_0:\beta_1=0,\beta_6=0$ has $p=0.014$** — reject at 5%. Exactly the collinearity pattern of [[04 - Multiple Regression Analysis - Inference|ch. 04]]: **separate $t$'s cannot test a joint hypothesis.**

**The correct partial effect** at the sample mean $\overline{priGPA}=2.59$:
$$\frac{\Delta stndfnl}{\Delta atndrte}=\hat\beta_1+\hat\beta_6\,priGPA = -0.0067+0.0056(2.59)\approx \mathbf{0.0078}$$

A **10 percentage point** rise in attendance raises the standardized exam score by **0.078 standard deviations**.

**Is that significant?** Rerun with $(priGPA-2.59)\cdot atndrte$ in place of $priGPA\cdot atndrte$. Then the coefficient on $atndrte$ **is** the effect at the mean, with its own standard error: $0.0078$ with $\mathrm{se}=0.0026$, so $t=3.0$. **Significant.** Nothing else in the regression changes.

#### 2d. Average partial effects (APE)

With quadratics and interactions, **the partial effect is a different number for every observation.** The APE collapses it to one:

$$\widehat{\text{APE}}_{atndrte}=\hat\beta_1+\hat\beta_6\,\overline{priGPA}$$
$$\widehat{\text{APE}}_{priGPA}=\hat\beta_2+2\hat\beta_4\,\overline{priGPA}+\hat\beta_6\,\overline{atndrte}$$

**Centring every variable about its sample mean before forming quadratics and interactions forces the level coefficients to *be* the APEs**, with correct standard errors, since an APE is just a **linear combination of the OLS coefficients**. Most packages report APEs on request. They return in Wooldridge ch. 17 for genuinely nonlinear models.

---

### 3. Goodness-of-fit and choosing regressors

#### 3a. A small $R^2$ is not a problem

> [!important] $R^2$ and unbiasedness are unrelated
> **Nothing in MLR.1–6 requires $R^2$ to be anything.** $R^2$ estimates the population $\rho^2=1-\sigma_u^2/\sigma_y^2$ — *how much of $y$ the regressors explain*. **MLR.4 is what determines unbiasedness**, and it says nothing about $R^2$.

Two clean demonstrations:

- **Randomized computer grants.** Grant amounts assigned at random $\Rightarrow$ uncorrelated with *everything* $\Rightarrow$ simple regression of GPA on the grant is **unbiased**. The $R^2$ will be tiny (grants explain little of GPA), and it doesn't matter.
- **`APPLE`.** Prices of regular and "ecolabeled" apples were **assigned experimentally**, so they are unrelated to income, environmental attitudes, everything. The regression is **unbiased by construction**, and $R^2=\mathbf{0.0364}$.

What a small $R^2$ *does* mean: **$\sigma^2$ is large relative to $\mathrm{Var}(y)$, so $\hat\beta_j$ is imprecise** — from the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] variance formula. But a large $n$ offsets a large $\sigma^2$. And it means **prediction will be poor** (§4) — most of $y$ is driven by things you don't observe.

**The *change* in $R^2$ is still central**, though — the $F$ statistic of [[04 - Multiple Regression Analysis - Inference|ch. 04]] is built entirely out of $R^2_{ur}-R^2_r$.

#### 3b. Adjusted $R^2$

$R^2=1-(\text{SSR}/n)/(\text{SST}/n)$ uses **biased** estimators of $\sigma_u^2$ and $\sigma_y^2$. Replace both with unbiased ones:

$$\boxed{\;\bar R^2 = 1-\frac{\text{SSR}/(n-k-1)}{\text{SST}/(n-1)} = 1-\frac{\hat\sigma^2}{\text{SST}/(n-1)} = 1-\frac{(1-R^2)(n-1)}{n-k-1}\;}$$

> [!warning] $\bar R^2$ does **not** correct the bias in $R^2$
> "Corrected $R$-squared" is a bad name. **The ratio of two unbiased estimators is not unbiased**, and $\bar R^2$ is not known to be a better estimator of $\rho^2$ than $R^2$. Its value is the **penalty for extra parameters**, nothing more.

**Three facts to memorize:**

1. **$\bar R^2$ rises when a variable is added $\iff$ its $|t| > 1$.** For a group, $\iff$ its joint $F>1$. **A $t$ of 1 is nowhere near significant**, so *selecting variables by $\bar R^2$ is much more permissive than testing them.*
2. **$\bar R^2$ can be negative.** With $R^2=0.10$, $n=51$, $k=10$: $\bar R^2 = 1-0.90(50)/40 = \mathbf{-0.125}$. A negative $\bar R^2$ signals a **terrible fit relative to the degrees of freedom spent**.
3. **The $F$ statistic uses $R^2$, never $\bar R^2$.** Substituting $\bar R^2_r$ and $\bar R^2_{ur}$ into the $F$ formula is simply **invalid**.

Sample calculation: $R^2=0.30$, $n=51$, $k=10 \Rightarrow \bar R^2 = 1-0.70(50)/40 = 0.125$. **For small $n$ and large $k$ the gap is enormous.**

#### 3c. Choosing between **nonnested** models

$F$ tests only compare **nested** models (one is a restricted version of the other). These are **not** nested:
$$\log(salary)=\beta_0+\beta_1 years+\beta_2 gamesyr+\beta_3 bavg+\beta_4 hrunsyr+u$$
$$\log(salary)=\beta_0+\beta_1 years+\beta_2 gamesyr+\beta_3 bavg+\beta_4 rbisyr+u$$

**$\bar R^2$ can arbitrate.** `MLB1`: $\bar R^2=0.6211$ with $hrunsyr$ vs $\mathbf{0.6226}$ with $rbisyr$ — a whisker in favour of $rbisyr$. (Both have 5 parameters, so plain $R^2$ gives the same ranking.)

**Where $\bar R^2$ genuinely earns its keep: comparing functional forms with different parameter counts.**

$$rdintens = \beta_0+\beta_1\log(sales)+u \tag{6.23}$$
$$rdintens = \beta_0+\beta_1 sales+\beta_2 sales^2+u \tag{6.24}$$

`RDCHEM`, $n=32$ chemical firms:

| Model | $k$ | $R^2$ | $\bar R^2$ |
|---|---|---|---|
| (6.23) log | 1 | 0.061 | **0.030** |
| (6.24) quadratic | 2 | 0.148 | **0.089** |

Plain $R^2$ is **unfair** to (6.23) — it has one fewer parameter, i.e. it is more **parsimonious**. After the penalty, **the quadratic still wins.**

> [!warning] The hard limit — you can never use $R^2$ or $\bar R^2$ to choose the form of $y$
> **Different transformations of $y$ have different amounts of variation to explain.** They are literally different dependent variables.
>
> **Example 6.4 — CEO pay** (`CEOSAL1`, $n=209$):
>
> | Model | $R^2$ | $\bar R^2$ | SST of the dependent variable |
> |---|---|---|---|
> | $salary$ on $sales$, $roe$ | 0.029 | 0.020 | **391,732,982** |
> | $\log(salary)$ on $\log(sales)$, $roe$ | 0.282 | 0.275 | **66.72** |
>
> $0.282 \gg 0.029$ **proves nothing.** There is vastly less variation in $\log(salary)$ to explain in the first place. §4c gives a comparison that *is* valid.

#### 3d. Controlling for **too many** factors

> [!important] Over-controlling: the mirror image of omitted variable bias
> [[03 - Multiple Regression Analysis - Estimation|Chapter 03]] taught the fear of leaving variables out. **The opposite error is just as real.** Ask always: *does it make sense to hold this fixed?*

**Beer taxes and traffic fatalities.**
$$fatalities=\beta_0+\beta_1 tax+\beta_2 miles+\beta_3 percmale+\beta_4 perc16\_21+\cdots$$
**Should $beercons$ be included? No.** The whole mechanism is *tax → less drinking → fewer deaths*. Controlling for consumption asks "what does a tax do to fatalities **holding drinking constant**?" — which **shuts off the only channel of interest**. Age and gender composition *should* be controlled for; they aren't affected by the tax.

**Pesticides and health expenditure.** Should you control for **doctor visits**? **No** — doctor visits *are part of* health expenditure. You would be measuring the effect of pesticides on health spending **other than doctor visits**. Doctor visits belong on the **left-hand side of a separate regression**.

**Housing assessments.** Regressing $\log(price)$ on $\log(lotsize)$, $\log(sqrft)$, $bdrms$: $\bar R^2 = 0.630$. Add $\log(assess)$: $\bar R^2 = \mathbf{0.762}$. **Goodness-of-fit says include it. Goodness-of-fit is wrong here.** For a **hedonic price model** you want the marginal value of an attribute; including the assessed value means *holding one measure of value fixed and asking what a bedroom does to another measure of value.* Meaningless.

**Not always clear-cut.** Betts (1995) studies school quality and earnings: if better schools cause **more education**, controlling for education **understates** the return to quality. Betts reports results **both ways** to bracket the answer. *That is the professional response to an ambiguous control.*

> [!tip] The rule
> **Do not control for a variable that is a *channel* through which your variable of interest operates, or that is a *component* of your outcome.** Chasing $\bar R^2$ will lead you into both mistakes.

#### 3e. Adding regressors to **reduce** the error variance

There is one case with **no downside**:

> [!important] Always include variables that affect $y$ and are **uncorrelated with the regressors of interest**
> - They **do not induce multicollinearity** (so $R_j^2$ barely moves), and
> - they **shrink $\sigma^2$** by pulling explanatory power out of the error.
>
> From $\mathrm{Var}(\hat\beta_j)=\sigma^2/[\text{SST}_j(1-R_j^2)]$: numerator down, denominator unchanged $\Rightarrow$ **smaller standard errors, in large samples.** No bias is involved either way — this is purely about **precision**.

**Beer demand:** county-level prices are plausibly uncorrelated with individual age and education, so adding those controls sharpens the price elasticity for free.

**Randomized grants:** grant amounts are random, so adding high-school GPA, SAT/ACT, family background **cannot** bias the grant effect and **will** reduce $\sigma^2$.

> [!note] Under random assignment, endogeneity of the *controls* doesn't matter
> Estimating the effect of job-training **hours** on earnings, you may include **pre-programme schooling** even though schooling is correlated with unobserved ability — **because you are not trying to estimate the return to schooling.** Any control **not itself affected by the treatment** is safe.
>
> **What you must never include is a post-treatment variable** — e.g. education obtained *after* the training, since training may have caused it. That is over-controlling in its most dangerous form.
>
> **Unfortunately, variables uncorrelated with the regressors of interest are rare in the social sciences.** This is a licence you rarely get to use.

---

### 4. Prediction and residual analysis

#### 4a. A confidence interval for a prediction

You want to estimate
$$\theta_0=\beta_0+\beta_1c_1+\cdots+\beta_kc_k=\mathbb{E}(y\mid x_1=c_1,\dots,x_k=c_k)$$

The point estimate $\hat\theta_0$ is trivial to compute. **Its standard error is not** — every $\hat\beta_j$ appears in it, so you need the whole covariance matrix.

> [!important] The trick — recentre the regressors
> Write $\beta_0=\theta_0-\beta_1c_1-\cdots-\beta_kc_k$ and substitute:
> $$y=\theta_0+\beta_1(x_1-c_1)+\cdots+\beta_k(x_k-c_k)+u$$
> **Regress $y_i$ on $(x_{i1}-c_1),\dots,(x_{ik}-c_k)$.** The **intercept** of that regression is $\hat\theta_0$, and its **reported standard error** is $\mathrm{se}(\hat\theta_0)$. Then $\hat\theta_0\pm t_{.025}\cdot\mathrm{se}(\hat\theta_0)$.
>
> Same device as §2c centring and as [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4. **Slopes, $R^2$, $\hat\sigma$ are all unchanged — which is your check that you did the transformation right.**

**Example 6.5** (`GPA2`, $n=4{,}137$):
$$\widehat{colgpa}=1.493+0.00149\,sat-0.01386\,hsperc-0.06088\,hsize+0.00546\,hsize^2$$
$$\qquad\; (0.075)\;\;\;(0.00007)\qquad (0.00056)\qquad\;\;(0.01650)\qquad\;\;(0.00227)$$
$$R^2=0.278,\quad \bar R^2=0.277,\quad \hat\sigma=0.560$$

At $sat=1200$, $hsperc=30$, $hsize=5$: $\widehat{colgpa}=2.70$.

Recentring ($sat0=sat-1200$, $hsperc0=hsperc-30$, $hsize0=hsize-5$, $hsizesq0=hsize^2-25$) gives an **intercept of 2.700 with standard error 0.020**, and every slope identical. ✓

$$\text{95\% CI for } \mathbb{E}(colgpa\mid x) = 2.70\pm1.96(0.020)=[2.66,\;2.74]$$

> [!note] Prediction is most precise at the mean
> $\mathrm{Var}(\hat y)$ is **smallest when every $c_j=\bar x_j$** and grows as you move away. *We trust the regression line most in the middle of the data* — and **extrapolation beyond the data is where it is least trustworthy.**

#### 4b. Prediction interval for an individual outcome

A CI for the **average** person with those characteristics is **not** an interval for **a** person. For a new unit,
$$y^0=\beta_0+\beta_1x_1^0+\cdots+\beta_kx_k^0+u^0$$
the prediction error is $\hat e^0=y^0-\hat y^0$, with $\mathbb{E}(\hat e^0)=0$ and, since $u^0$ is uncorrelated with the in-sample $\hat\beta_j$,

$$\boxed{\;\mathrm{Var}(\hat e^0)=\underbrace{\mathrm{Var}(\hat y^0)}_{\propto\,1/n\;\to\;0}+\underbrace{\sigma^2}_{\text{never shrinks}}\;}$$
$$\mathrm{se}(\hat e^0)=\left\{\left[\mathrm{se}(\hat y^0)\right]^2+\hat\sigma^2\right\}^{1/2},\qquad \textbf{95\% PI: } \hat y^0\pm t_{.025}\cdot\mathrm{se}(\hat e^0)$$

**Example 6.6.** $\mathrm{se}(\hat y^0)=0.020$, $\hat\sigma=0.560$:
$$\mathrm{se}(\hat e^0)=\sqrt{0.020^2+0.560^2}=0.5604$$
$$\text{95\% PI}=2.70\pm1.96(0.5604)=[\mathbf{1.60},\;\mathbf{3.80}]$$

> [!important] $[2.66,\,2.74]$ versus $[1.60,\,3.80]$ — **28 times wider**
> $$\frac{0.5604}{0.020}=28.0$$
> With $n=4{,}137$, **essentially all** of the prediction error is $\sigma$ — our ignorance of the individual. **More data cannot fix this.** $\mathrm{Var}(\hat y^0)\to0$; $\sigma^2$ does not budge. Even with infinite data the interval stays $\pm1.96(0.560)=\pm1.10$.
>
> **This is the deepest practical message of the chapter, and it is why a low $R^2$ makes prediction hopeless.** Substantively, it is also *good news*: SAT and high-school rank do **not** preordain your college GPA.

#### 4c. Residual analysis

Look at $\hat u_i=y_i-\hat y_i$ for individual observations.

- **House hunting.** `HPRICE1`, $n=88$: regress $price$ on $lotsize$, $sqrft$, $bdrms$. The most negative residual is $-120.206$ for house 81 — asking **\$120,206 below** its predicted price. **Underpriced given observables… or it has a defect the model doesn't see** (which is precisely what "the error term" means). Pair the residual with a **prediction interval** from (6.37) before making an offer.
- **Ranking law schools.** Regress median starting salary on entering-class LSAT and GPA. **The largest positive residual is the highest *value added*** — outcomes beyond what the intake predicts.
- **Litigation.** *"Judge Says Pupil's Poverty, Not Segregation, Hurts Scores"* (**NYT, 28 June 1995**). Hartford's test scores were regressed on district socioeconomic characteristics. The judge ruled that scores were **"about at the levels that one would expect"** — i.e. **Hartford's residual was not sufficiently negative** to blame the schools. **A residual decided a civil-rights case.**

#### 4d. Predicting $y$ when $\log(y)$ is the dependent variable

$$\log y = \beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$$

> [!warning] $\hat y = \exp(\widehat{\log y})$ is **systematically too low**
> Because $\exp(\cdot)$ is convex, exponentiating the prediction of the log gives (roughly) the **median**, not the mean.

**Under normality (MLR.6):** $\mathbb{E}[\exp(u)]=\exp(\sigma^2/2)$, so

$$\boxed{\;\hat y = \exp(\hat\sigma^2/2)\cdot\exp(\widehat{\log y})\;}$$

Since $\hat\sigma^2>0$, the factor **always exceeds 1**, and for large $\hat\sigma^2$ it is substantial.

**Without normality**, assume only that $u$ is **independent** of the $x_j$. Then $\mathbb{E}(y\mid x)=\alpha_0\exp(\beta_0+\beta_1x_1+\cdots)$ with $\alpha_0=\mathbb{E}[\exp(u)]>1$, and $\hat y=\hat\alpha_0\exp(\widehat{\log y})$. Two estimators:

| | Formula | Property |
|---|---|---|
| **Duan (1983) smearing** | $\hat\alpha_0=n^{-1}\sum_{i=1}^n\exp(\hat u_i)$ | Consistent, biased; **always $>1$** (since $\sum\hat u_i=0$ and $\exp$ is convex — Jensen) |
| **Regression estimate** | $\check\alpha_0=\left(\sum\hat m_i^2\right)^{-1}\left(\sum \hat m_i y_i\right)$, $\hat m_i=\exp(\widehat{\log y_i})$ | Consistent, biased; **not guaranteed $>1$** |

$\check\alpha_0$ comes from regressing $y_i$ on $\hat m_i$ **through the origin**.

> [!warning] $\check\alpha_0<1$ is a red flag
> $\alpha_0>1$ must hold in the population. If $\check\alpha_0<1$ — especially well below 1 — **the independence of $u$ and the $x_j$ is probably violated**. Falling back on $\hat\alpha_0$ may just be masking a broken model.

**The procedure:**
1. Regress $\log y$ on $x_1,\dots,x_k$; keep fitted values $\widehat{\log y_i}$ and residuals $\hat u_i$.
2. Compute $\hat\alpha_0$ (smearing) or $\check\alpha_0$ (regression).
3. Compute $\widehat{\log y}$ at the desired $x$ values.
4. $\hat y=\hat\alpha_0\exp(\widehat{\log y})$.

**Example 6.7 — CEO salaries** (`CEOSAL2`, $n=177$):
$$\widehat{lsalary}=4.504+0.163\,lsales+0.109\,lmktval+0.0117\,ceoten,\qquad R^2=0.318$$
$$\qquad\;\;\;(0.257)\;\;(0.039)\qquad\;(0.050)\qquad\;\;(0.0053)$$

At $sales=5{,}000$ (\$5 bn), $mktval=10{,}000$ (\$10 bn), $ceoten=10$: $\widehat{lsalary}\approx 7.013$, so $\exp(7.013)\approx 1{,}110.98$.

| Estimator | Predicted salary |
|---|---|
| **Naive** $\exp(\widehat{lsalary})$ | \$1,110,983 |
| **Duan smearing** $\hat\alpha_0=1.136$ | **\$1,262,077** |
| **Regression** $\check\alpha_0=1.117$ | **\$1,240,968** |
| **Normal** $\exp(\hat\sigma^2/2)$, $\hat\sigma=0.505$ | \$1,262,075 |

> [!tip] A detail worth noticing
> $\exp(\hat\sigma^2/2)=\exp(0.505^2/2)=\mathbf{1.1360}$ — **numerically identical to Duan's $\hat\alpha_0=1.136$.** The normality-based factor and the distribution-free one agree, which is itself **evidence that the errors here are close to normal.** When they disagree sharply, trust the smearing estimate.
>
> **The two adjusted predictions differ from each other by far less than either differs from the naive one.** The choice of $\alpha_0$ estimator is a detail; **making the adjustment at all is not.**

**A goodness-of-fit measure comparable across $y$ and $\log(y)$ models.** Two options:

1. **Squared correlation between $y_i$ and $\hat m_i$.** In a linear model, $R^2$ *is* $\mathrm{corr}(y_i,\hat y_i)^2$. Since correlation is invariant to multiplication by a constant, **this measure doesn't depend on which $\alpha_0$ estimate you use.**
2. **An SSR-based version** using $\hat r_i = y_i-\hat\alpha_0\exp(\widehat{\log y_i})$:
$$1-\frac{\sum_i\hat r_i^2}{\sum_i(y_i-\bar y)^2}$$
This one **does** depend on $\hat\alpha_0$ (it is minimized by $\check\alpha_0$ — which is not a reason to prefer $\check\alpha_0$).

**Example 6.8 — the comparison that is finally legitimate.** $\mathrm{corr}(salary_i,\hat m_i)=0.493$, so the measure is $0.493^2=\mathbf{0.243}$.

| Model | Measure of variation explained **in $salary$** |
|---|---|
| $\log(salary)$ model, retransformed | **0.243** |
| $salary$ on $sales$, $mktval$, $ceoten$ (levels) | **0.201** |

**The log model wins — on the same dependent variable.** (Its $R^2$ of $0.318$ refers to $\log(salary)$ and was never comparable.) It is also preferred on interpretability and realism.

**Prediction intervals for $y$ from a log model.** Build the interval in logs and exponentiate — valid because $\exp$ is strictly increasing:
$$c_l=\widehat{\log y^0}-t_{.025}\,\mathrm{se}(\hat e^0),\qquad c_u=\widehat{\log y^0}+t_{.025}\,\mathrm{se}(\hat e^0)$$
$$P\left[\exp(c_l)\le y^0\le \exp(c_u)\right]=0.95$$

For the CEO prediction: $\hat\sigma=0.505$, $\mathrm{se}(\widehat{\log y^0})=0.075$, so $\mathrm{se}(\hat e^0)=\sqrt{0.075^2+0.505^2}\approx0.511$.
$$\exp(7.013\pm1.96\times0.511) \Rightarrow \mathbf{[\$408{,}071,\;\$3{,}024{,}678]}$$

> [!warning] The interval is **not symmetric** around the point prediction
> The point prediction \$1,262,075 sits **much closer to the lower bound than the upper**. Exponentiating a symmetric interval gives an asymmetric one — and **the point prediction is not its midpoint.** A 7.4-fold range from bottom to top, with $n=177$: **an enormous amount about CEO pay is simply not in the model.**

---

## ✏️ Exercises

### Exercise 1 — Data scaling, end to end

A city analyst estimates, across $n=300$ US cities,
$$\widehat{crime} = 42.60 - 1.85\,police - 0.214\,income$$
$$\qquad\;\;\; (4.15)\qquad (0.62)\qquad\quad (0.058)$$
$$R^2=0.283,\quad \text{SSR}=18{,}400,\quad \text{SER}=7.871$$

where $crime$ = crimes per **1,000** residents, $police$ = officers per 1,000 residents, $income$ = median household income in **thousands** of dollars.

**(a)** Write out the equation when $crime$ is measured per **100,000** residents instead. Report every coefficient, standard error, $t$, $R^2$, SSR and SER.
**(b)** Return to the original units, but measure income in **dollars** ($incdol = 1{,}000\cdot income$). What changes?
**(c)** Which of (a) or (b) is the better way to present these results, and why?
**(d)** Now suppose the dependent variable were $\log(crime)$. If you rescale $crime$ from per-1,000 to per-100,000, what changes?

> [!example]- Solution
> **(a)** $crime$ is multiplied by $c=100$, so **every coefficient and every standard error is multiplied by 100**:
> $$\widehat{crime_{100k}} = 4{,}260 - 185\,police - 21.4\,income$$
> $$\qquad\qquad\;\; (415)\qquad (62)\qquad\quad (5.8)$$
>
> | Statistic | Value | Why |
> |---|---|---|
> | $t$ on $police$ | $-185/62=\mathbf{-2.98}$ | identical to $-1.85/0.62$ |
> | $t$ on $income$ | $-21.4/5.8=\mathbf{-3.69}$ | identical |
> | $R^2$ | $\mathbf{0.283}$ | **unit-free** |
> | SSR | $18{,}400\times100^2=\mathbf{184{,}000{,}000}$ | residuals $\times100$, then **squared** |
> | SER | $7.871\times100=\mathbf{787.1}$ | $\sqrt{184{,}000{,}000/297}=787.1$ ✓ |
>
> **(b)** Only $income$ is rescaled, by $c=1{,}000$, so **only its coefficient and standard error are divided by 1,000**:
> $$\hat\beta_{incdol}=-0.000214,\qquad \mathrm{se}=0.000058$$
>
> **Everything else is untouched** — intercept, $police$ coefficient and se, $R^2$, SSR, SER. Note SSR and SER **do not move**, unlike in (a): rescaling a *regressor* does not change any fitted value or residual, it only relabels the axis.
>
> $t = -0.000214/0.000058 = \mathbf{-3.69}$. ✓ Identical.
>
> **(c) The original presentation (income in thousands) is best.** $-0.214$ is readable; $-0.000214$ is four leading zeros of noise. And "one more officer per 1,000 residents cuts crime by 1.85 per 1,000" is a sentence you can say out loud, whereas per-100,000 units force you to carry 4,260 and 185 around for no gain.
>
> **This is purely cosmetic — and that is exactly the point.** Scaling can improve the *appearance* of an equation "while changing nothing that is essential."
>
> **(d)** $\log(100\cdot crime)=\log(100)+\log(crime)$, so **only the intercept changes**, rising by $\log(100)=\mathbf{4.605}$. Every slope, standard error, $t$, $R^2$, SSR and SER is **exactly as before** — the residuals themselves are unchanged, because the shift is a constant absorbed by $\hat\beta_0$.
>
> **The lesson:** when the dependent variable is in logs, you can be completely ignorant of its units.

---

### Exercise 2 — Beta coefficients and "which variable matters most"

From the `GPA2` regression, $\widehat{colgpa}=1.493+0.00149\,sat-0.01386\,hsperc-0.0609\,hsize+\cdots$, with sample standard deviations

| Variable | sd |
|---|---|
| $colgpa$ | 0.47 |
| $sat$ | 139 |
| $hsperc$ | 24.3 |
| $hsize$ | 3.7 |

**(a)** Compute the beta coefficient for each regressor.
**(b)** Rank the three variables by standardized importance. Does the ranking match the ranking of the raw coefficients?
**(c)** A classmate says "$sat$ has a coefficient of $0.00149$ and $hsize$ has $-0.0609$, so school size matters 40 times more than SAT score." Diagnose the error.
**(d)** Do the $t$ statistics change when you standardize? Does the intercept survive?
**(e)** In a simple regression of $colgpa$ on $sat$ alone, what would the beta coefficient equal, and what range must it lie in? Does that bound apply in (a)?

> [!example]- Solution
> **(a)** $\hat b_j=(\hat\sigma_j/\hat\sigma_y)\hat\beta_j$:
>
> | Variable | $\hat\beta_j$ | $\hat\sigma_j/\hat\sigma_y$ | $\hat b_j$ |
> |---|---|---|---|
> | $sat$ | $0.00149$ | $139/0.47=295.7$ | $\mathbf{+0.441}$ |
> | $hsperc$ | $-0.01386$ | $24.3/0.47=51.70$ | $\mathbf{-0.717}$ |
> | $hsize$ | $-0.0609$ | $3.7/0.47=7.87$ | $\mathbf{-0.479}$ |
>
> **(b)** By $|\hat b_j|$: $\;hsperc\;(0.717)\;>\;hsize\;(0.479)\;>\;sat\;(0.441)$.
>
> By raw $|\hat\beta_j|$: $\;hsize\;(0.0609)\;>\;hsperc\;(0.01386)\;>\;sat\;(0.00149)$.
>
> **The rankings disagree, and the raw ranking is meaningless.** Standardized: **high-school percentile rank is the strongest predictor of college GPA** — a one-sd better rank is worth $0.72$ sd of GPA, well ahead of a one-sd higher SAT.
>
> **(c) Two errors at once.**
> 1. **The comparison is a units artefact.** $sat$ ranges over hundreds of points; $hsize$ over a handful of hundreds-of-students. Measure $sat$ in *hundreds* of points and its coefficient becomes $0.149$ — now it "matters 2.4× more" than $hsize$. **Nothing about the world changed.**
> 2. **"Matters more" needs a common yardstick.** With betas, $0.479$ vs $0.441$: **$hsize$ and $sat$ are close, with $hsize$ slightly ahead** — nowhere near a factor of 40.
>
> **(d) The $t$ statistics are identical.** $\hat b_j$ and $\mathrm{se}(\hat b_j)$ are both scaled by the same factor $\hat\sigma_j/\hat\sigma_y$, so the ratio is invariant. **Standardization is an interpretation device with zero inferential content.**
>
> **The intercept is exactly zero and is dropped** — every $z$-score has sample mean zero, so the fitted plane passes through the origin.
>
> **(e)** With one regressor, $\hat b_1=\hat\rho_{y,sat}$, the **sample correlation** — necessarily in $[-1,1]$.
>
> **That bound does not carry over to (a).** With multiple correlated regressors, beta coefficients are partial effects and **can exceed 1 in absolute value** (as ordinary coefficients can). The $[-1,1]$ intuition is a simple-regression fact only.

---

### Exercise 3 — Quadratics, turning points, exact percentage changes

Using `WAGE1` ($n=526$):
$$\widehat{\log(wage)} = 0.128 + 0.0904\,educ + 0.0410\,exper - 0.000714\,exper^2$$

**(a)** Find the turning point in $exper$.
**(b)** Compute the partial effect of one more year of experience at $exper=1$, $5$, $10$, and $20$. Express each as a percentage.
**(c)** Give the approximate **and exact** percentage effect on wage of **four** more years of education. How big is the approximation error?
**(d)** A student concludes from (a) that wages fall after 28.7 years of experience. Evaluate.
**(e)** Compare this equation with the levels equation $\widehat{wage}=3.73+0.298\,exper-0.0061\,exper^2$ ($R^2=0.093$), whose turning point is 24.4 years. Which specification is more credible, and can you use $R^2$ to decide?

> [!example]- Solution
> **(a)** $$exper^* = \frac{0.0410}{2(0.000714)} = \mathbf{28.7\text{ years}}$$
>
> **(b)** $\dfrac{\Delta\log(wage)}{\Delta exper}\approx 0.0410-2(0.000714)\,exper$; multiply by 100 for a percentage.
>
> | $exper$ | Partial effect | Interpretation |
> |---|---|---|
> | 1 | $0.0410-0.00143=0.03957$ | $\approx\mathbf{4.0\%}$ per year |
> | 5 | $0.0410-0.00714=0.03386$ | $\approx\mathbf{3.4\%}$ |
> | 10 | $0.0410-0.01428=0.02672$ | $\approx\mathbf{2.7\%}$ |
> | 20 | $0.0410-0.02856=0.01244$ | $\approx\mathbf{1.2\%}$ |
>
> **Clearly diminishing returns**, which is the whole reason for the quadratic. Note this is a **semi-elasticity**: the returns are proportional, not in dollars, which is far more plausible than the levels model's fixed cents-per-hour.
>
> **(c)** $\Delta educ=4$, so $\Delta\log(wage)=4(0.0904)=0.3616$.
>
> $$\text{Approximate: } 100(0.3616)=\mathbf{36.2\%}$$
> $$\text{Exact: } 100\left[e^{0.3616}-1\right]=\mathbf{43.6\%}$$
>
> **An error of 7.4 percentage points — over a fifth of the approximate figure.** For **one** year the gap is trivial ($9.04\%$ vs $9.46\%$); the approximation degrades as $\Delta\log(y)$ grows. **Any time you are quoting a change above about 20%, use the exact formula.**
>
> **(d) The conclusion does not follow, for two reasons.**
>
> 1. **It confuses the model with the world.** A quadratic *must* turn around — that is the price of using two parameters to capture curvature. The turning point is an **artefact you must check**, not an estimate you report.
> 2. **The right test is what share of the sample lies past it.** If almost nobody has 29+ years of experience, the right-hand branch is fitted on nothing and can be ignored. If a substantial share does, **the functional form is inadequate** and the whole curve is suspect.
>
> **I cannot check this share — `WAGE1` is not in the vault.** In the *levels* version Wooldridge reports that **about 28% of the sample exceeds the 24.4-year turning point**, which he calls "too high a percentage to ignore." At 28.7 years the fraction is smaller but the same question must be asked.
>
> **(e) The log specification is more credible**, for three reasons:
> - It **controls for education**; the levels equation controls for nothing, so its $exper$ coefficient absorbs omitted variable bias from schooling ([[03 - Multiple Regression Analysis - Estimation|ch. 03]]).
> - **Proportional returns to experience are more plausible than fixed dollar returns.**
> - It pushes the turning point out to a **more defensible 28.7 years**.
>
> > [!warning] **You absolutely cannot use $R^2$ to make this comparison.**
> > One model explains $wage$, the other explains $\log(wage)$ — **two different dependent variables with different total variation.** Any comparison of $0.093$ against the log model's $R^2$ is invalid. **To compare them you would need §4d's retransformation measure: exponentiate the log model's fitted values, apply $\hat\alpha_0$, and take the squared correlation with $wage_i$.**

---

### Exercise 4 — Adjusted $R^2$ and the parsimony penalty

**(a)** For the R&D models on $n=32$ chemical firms, compute $\bar R^2$:
- (i) $rdintens$ on $\log(sales)$: $R^2=0.061$, $k=1$
- (ii) $rdintens$ on $sales$ and $sales^2$: $R^2=0.148$, $k=2$

Which model is preferred, and why was the raw $R^2$ comparison unfair?

**(b)** A researcher has $R^2=0.30$ with $n=51$ and $k=10$. Compute $\bar R^2$. Now suppose the fit had been $R^2=0.10$ instead. Compute $\bar R^2$ and interpret.

**(c)** She adds one more regressor whose $t$ statistic is $1.4$. Does $R^2$ rise? Does $\bar R^2$? Would you keep the variable?

**(d)** She then reports an $F$ statistic computed as $\dfrac{(\bar R^2_{ur}-\bar R^2_r)/q}{(1-\bar R^2_{ur})/(n-k-1)}$. What is wrong?

**(e)** Why is "maximize $\bar R^2$" the same rule as "minimize $\hat\sigma$"?

> [!example]- Solution
> **(a)** $\bar R^2 = 1-\dfrac{(1-R^2)(n-1)}{n-k-1}$:
>
> | Model | $k$ | $R^2$ | $\bar R^2$ |
> |---|---|---|---|
> | (i) log | 1 | 0.061 | $1-\frac{0.939(31)}{30}=\mathbf{0.030}$ |
> | (ii) quadratic | 2 | 0.148 | $1-\frac{0.852(31)}{29}=\mathbf{0.089}$ |
>
> **The quadratic still wins after the penalty.**
>
> **The raw comparison was unfair** because model (ii) **spends one more parameter** to buy its higher $R^2$, and $R^2$ *never falls* when you add a regressor. **Everything else equal, simpler models are better** — (i) is the more parsimonious model, and only $\bar R^2$ charges (ii) for the extra parameter. Here the extra parameter more than pays for itself.
>
> **(b)**
> $$R^2=0.30:\quad \bar R^2 = 1-\frac{0.70(50)}{40}=1-0.875=\mathbf{0.125}$$
> $$R^2=0.10:\quad \bar R^2 = 1-\frac{0.90(50)}{40}=1-1.125=\mathbf{-0.125}$$
>
> **With $n=51$ and $k=10$ the penalty is brutal** — $R^2$ of $0.30$ collapses to $0.125$. And $\bar R^2$ **can go negative**: it is not a squared anything and has no lower bound at zero. **A negative $\bar R^2$ means the model fits worse than the sample mean of $y$, once you charge for the degrees of freedom spent.**
>
> **(c)**
> - **$R^2$ rises — always.** Adding any regressor cannot increase SSR.
> - **$\bar R^2$ rises too**, because the rule is *$\bar R^2$ increases $\iff |t|>1$*, and $1.4>1$.
> - **But I would not keep it on this evidence.** $|t|=1.4$ is **not significant at any conventional level** ($p\approx0.17$). **The $\bar R^2$ criterion is far more permissive than a $t$ test** — it accepts everything with $|t|>1$, i.e. roughly everything with $p<0.32$.
>
> **This is the practical warning: $\bar R^2$ is a weak filter, not a hypothesis test.** Keep the variable if theory says it belongs, or if it is uncorrelated with your variable of interest and shrinks $\sigma^2$ (§3e) — not because $\bar R^2$ ticked up.
>
> **(d) The formula is invalid.** The $F$ statistic of [[04 - Multiple Regression Analysis - Inference|ch. 04]] is built from **$R^2$, never $\bar R^2$**:
> $$F=\frac{(R^2_{ur}-R^2_r)/q}{(1-R^2_{ur})/(n-k-1)}$$
> The derivation runs through $\text{SSR}_r-\text{SSR}_{ur}$, and $R^2$ is what maps onto SSR with a common SST. **$\bar R^2$ has degrees-of-freedom adjustments already baked in**, so substituting it double-counts the correction and produces a statistic with **no known distribution**. Her "$F$" cannot be compared to any table.
>
> **(e)** Because
> $$\bar R^2 = 1-\frac{\hat\sigma^2}{\text{SST}/(n-1)}$$
> and for a **fixed dependent variable and fixed sample**, $\text{SST}/(n-1)$ is a **constant**. So $\bar R^2$ is a strictly decreasing function of $\hat\sigma^2$: **maximizing $\bar R^2$ is minimizing $\hat\sigma$, exactly.**
>
> > [!warning] The "fixed dependent variable" caveat is the whole reason $\bar R^2$ can't compare $y$ with $\log(y)$
> > Change the dependent variable and $\text{SST}$ changes, breaking the equivalence — which is why comparing $\hat\sigma$ across a levels model and a log model is just as meaningless as comparing their $\bar R^2$s. (Recall §1: $\hat\sigma$ is in the units of $y$.)

---

### Exercise 5 — Prediction: the average person vs a person

From the `GPA2` regression: at $sat=1200$, $hsperc=30$, $hsize=5$, the recentred regression gives an intercept of $2.700$ with $\mathrm{se}=0.020$, and $\hat\sigma=0.560$, $n=4{,}137$.

**(a)** Construct a 95% CI for $\mathbb{E}(colgpa\mid x)$ at these values, and a 95% prediction interval for an individual student. How many times wider is the second?
**(b)** The admissions office wants the individual interval narrowed. They propose collecting 40,000 more observations. Evaluate quantitatively.
**(c)** Explain why the recentring trick works, and how you can verify you did it correctly.
**(d)** Now the CEO model: $\widehat{lsalary}=7.013$, $\hat\sigma=0.505$, and the Duan smearing estimate is $\hat\alpha_0=1.136$. Give the naive prediction, the smearing prediction, and the normality-based prediction. Comment on what you notice.
**(e)** With $\mathrm{se}(\widehat{lsalary^0})=0.075$, construct a 95% prediction interval for salary. Is the point prediction at its centre?

> [!example]- Solution
> **(a)**
> $$\textbf{CI for the mean: } 2.70\pm1.96(0.020) = [\mathbf{2.66},\;\mathbf{2.74}]\qquad\text{width }0.078$$
> $$\mathrm{se}(\hat e^0)=\sqrt{(0.020)^2+(0.560)^2}=\sqrt{0.0004+0.3136}=\mathbf{0.5604}$$
> $$\textbf{PI for an individual: } 2.70\pm1.96(0.5604)=[\mathbf{1.60},\;\mathbf{3.80}]\qquad\text{width }2.197$$
>
> $$\text{Ratio} = \frac{0.5604}{0.020}=\mathbf{28.0}\text{ times wider}$$
>
> **They answer different questions.** The first is about the **average GPA of the subpopulation** with these characteristics — pinned down tightly because $n$ is large. The second is about **one named student**, and must additionally carry $u^0$: everything about that person the regression cannot see.
>
> **(b) Collecting more data is nearly worthless here, and I can show exactly how worthless.**
>
> $\mathrm{Var}(\hat y^0)\propto 1/n$, so $\mathrm{se}(\hat y^0)\propto 1/\sqrt n$. Going from $n=4{,}137$ to $n=44{,}137$ multiplies it by $\sqrt{4137/44137}=0.306$:
> $$\mathrm{se}(\hat y^0):\;0.020\;\to\;0.0061$$
> $$\mathrm{se}(\hat e^0)=\sqrt{0.0061^2+0.560^2}=0.56003$$
>
> **The prediction interval goes from $\pm1.0984$ to $\pm1.0977$ — a width reduction of about 0.06%.**
>
> **The limit as $n\to\infty$ is $\pm1.96(0.560)=\pm1.10$**, i.e. $[1.60,\,3.80]$ to three digits. **No sample size fixes this.** $\mathrm{Var}(\hat y^0)\to0$ but $\sigma^2$ is a property of the *population*, not the sample.
>
> **The only way to narrow an individual prediction interval is to reduce $\sigma$ — that is, to find variables that actually explain the individual variation.** Which is the same as saying: **raise the $R^2$.** This is the concrete link between §3a ("a low $R^2$ isn't a bias problem") and §4b ("but it *is* a prediction problem").
>
> **(c)** Substituting $\beta_0=\theta_0-\sum\beta_jc_j$ into the population model gives
> $$y=\theta_0+\beta_1(x_1-c_1)+\cdots+\beta_k(x_k-c_k)+u$$
> so **$\theta_0$ has literally become the intercept** of a regression on recentred regressors. The package's reported intercept and its standard error are then $\hat\theta_0$ and $\mathrm{se}(\hat\theta_0)$ — computed correctly, including **every covariance among the $\hat\beta_j$**, which is the part you cannot do by hand.
>
> **The verification:** recentring is a **pure reparameterization** — it shifts the regressors by constants and changes nothing else. So **all slope coefficients, all their standard errors, $R^2$, $\bar R^2$, SSR and $\hat\sigma$ must be identical to the original regression.** If any of them moved, you built a variable wrong. (In Example 6.5 all four slopes, all four standard errors, $R^2=0.278$ and $\hat\sigma=0.560$ match exactly. ✓)
>
> **Note the trap in that example:** $hsize^2$ appears in the model, and the recentred version needs $hsizesq0 = hsize^2-25$, **not** $(hsize-5)^2$. You subtract the value of the *regressor as it enters the model*, evaluated at $c$.
>
> **(d)**
>
> | Method | Factor | Prediction |
> |---|---|---|
> | **Naive** $\exp(7.013)$ | — | $1{,}110.98$ = **\$1,110,983** |
> | **Duan smearing** | $\hat\alpha_0=1.136$ | $1{,}110.98\times1.136=$ **\$1,262,077** |
> | **Normality** $\exp(\hat\sigma^2/2)$ | $\exp(0.505^2/2)=1.1360$ | **\$1,262,075** |
>
> **What I notice:** the two adjustment factors are **numerically identical to four significant figures** — $1.136$ both ways. They rest on completely different assumptions: the normality factor requires MLR.6, while Duan's requires only that $u$ be independent of the $x_j$. **Their agreement is empirical evidence that the errors in this log-wage-style equation really are close to normal** — i.e. that $salary$ is close to lognormal, which is the standard stylized fact about pay.
>
> **The naive prediction is \$151,000 too low — about 12%.** Exponentiating without adjustment is not a rounding issue; it is a **systematic downward bias**, and it grows with $\hat\sigma^2$.
>
> **(e)**
> $$\mathrm{se}(\hat e^0)=\sqrt{(0.075)^2+(0.505)^2}=\sqrt{0.005625+0.255025}=\mathbf{0.5105}\approx 0.511$$
>
> Build the interval **in logs**, then exponentiate:
> $$c_l = 7.013-1.96(0.511)=6.0114,\qquad c_u=7.013+1.96(0.511)=8.0146$$
> $$\left[e^{6.0114},\;e^{8.0146}\right]=[408.1,\;3025.4]\;\Longrightarrow\;\boxed{[\$408{,}071,\;\$3{,}024{,}678]}$$
>
> **This is valid because $\exp$ is strictly increasing**, so $P(c_l\le \log y^0\le c_u)=0.95$ implies $P(e^{c_l}\le y^0\le e^{c_u})=0.95$ exactly. No approximation.
>
> **No — the point prediction is nowhere near the centre.**
> $$1262 - 408 = 854 \qquad\text{vs}\qquad 3025 - 1262 = 1763$$
>
> **The upper gap is more than twice the lower one.** A symmetric interval in logs becomes a **right-skewed** interval in levels, and the point prediction sits **well below the midpoint** $(408+3025)/2 = 1717$.
>
> > [!warning] Do not "recentre" a log-model prediction interval
> > Reporting $\$1{,}262{,}077 \pm \$1{,}308{,}000$ would be wrong in both directions. **Report the two bounds.** Asymmetry is a real feature of the lognormal, not a defect of the method.
>
> **Substantively:** a **7.4-fold** range for a CEO with fixed sales, market value and tenure. Note also $\mathrm{se}(\hat e^0)=0.511$ against $\hat\sigma=0.505$ — **once again the error variance swamps the estimation error**, even at $n=177$.

---

## 📝 Summary

- **Rescaling changes nothing essential.** Multiply $y$ by $c$: all coefficients and standard errors $\times c$, SSR $\times c^2$, SER $\times c$. Multiply $x_j$ by $c$: $\hat\beta_j\div c$ only. **$t$, $F$ and $R^2$ never move.** If a variable is in **logs**, rescaling it moves **only the intercept**.
- **Beta coefficients** $\hat b_j=(\hat\sigma_j/\hat\sigma_y)\hat\beta_j$ put regressors in sd units so their magnitudes can legitimately be compared. **They change no $t$ statistic**, and the intercept vanishes.
- **The exact percentage change is $100[\exp(\hat\beta\Delta x)-1]$**, not $100\hat\beta\Delta x$. The coefficient always lies **between** the magnitudes of the increase and the decrease effects — a symmetric summary of an asymmetric effect.
- **In a quadratic, $\hat\beta_1$ is not the effect of $x$.** The partial effect is $\hat\beta_1+2\hat\beta_2x$ and the turning point is $|\hat\beta_1/(2\hat\beta_2)|$. **Always compute the turning point and ask what fraction of the sample lies beyond it** — a silly turning point signals misspecification. **Never judge a squared term by the size of its coefficient.**
- **In an interaction model, the level coefficient is the effect when the interacting variable equals zero** — usually meaningless. **Centre the interaction** to make the level coefficients into effects at the mean, with free standard errors. And **never test a joint hypothesis with separate $t$ statistics** (Example 6.3: both $t$'s insignificant, joint $F$ has $p=0.014$).
- **$\bar R^2 = 1-(1-R^2)(n-1)/(n-k-1)$** penalizes parameters; it **rises iff the added variable has $|t|>1$** — far weaker than a significance test. **It can be negative.** The $F$ statistic uses $R^2$, **never** $\bar R^2$. Neither can compare models with **different transformations of $y$**.
- **A low $R^2$ is not a bias problem** — MLR.4 governs unbiasedness, and randomized experiments routinely give $R^2\approx0.03$ with perfectly unbiased estimates. **But a low $R^2$ is fatal for prediction.**
- **Over-controlling is as real an error as omitting a variable.** Never control for a **channel** of your effect (beer consumption when studying beer taxes) or a **component** of your outcome (doctor visits inside health expenditure). Conversely, **always include variables that affect $y$ and are uncorrelated with your regressors of interest** — free precision, no multicollinearity cost.
- **$\mathrm{Var}(\hat e^0)=\mathrm{Var}(\hat y^0)+\sigma^2$.** The first term $\to0$ with sample size; **the second never does.** A prediction interval for an individual is typically an order of magnitude wider than a CI for the subpopulation mean (28× in Example 6.6), and **no amount of data closes the gap**.
- **Predicting $y$ from a $\log(y)$ model requires an upward adjustment**: $\hat y=\exp(\hat\sigma^2/2)\exp(\widehat{\log y})$ under normality, or $\hat y = \hat\alpha_0\exp(\widehat{\log y})$ with **Duan's smearing estimate** $\hat\alpha_0=n^{-1}\sum\exp(\hat u_i)>1$ without it. The **squared correlation of $y_i$ with $\hat m_i$** is the goodness-of-fit measure that can finally be compared against a levels model's $R^2$ (CEO: **0.243 log vs 0.201 levels**).

---

## ⚠️ Important Notes

> [!warning] The eleven mistakes this chapter is designed to prevent
>
> 1. **Reading the SER as a measure of fit.** It is in the units of $y$. Rescale $y$ and the SER moves; $R^2$ does not. **Never compare SERs across differently-scaled dependent variables.**
> 2. **Ranking variables by raw coefficient size.** Meaningless — magnitudes are a choice of units. Use **beta coefficients**, or at least standard-deviation changes.
> 3. **Thinking beta coefficients must lie in $[-1,1]$.** True only in **simple** regression, where $\hat b_1=\hat\rho_{yx}$.
> 4. **Interpreting $\hat\beta_1$ in $y=\beta_0+\beta_1x+\beta_2x^2$ as "the effect of $x$."** It is the effect only at $x=0$. **The effect is $\hat\beta_1+2\hat\beta_2 x$.**
> 5. **Dismissing a small squared-term coefficient.** $0.062$ on $rooms^2$ turns a flat $+25.5\%$-per-room into anything from $+7.5\%$ to $+32.3\%$ across the sample. **Compute the partial effect at real $x$ values before judging.**
> 6. **Interpreting the level coefficient in an interaction model.** In Example 6.3, $-0.0067$ on $atndrte$ is the effect **at $priGPA=0$** — a value that does not exist in the sample. **The honest number is $\hat\beta_1+\hat\beta_6\overline{priGPA}=+0.0078$, and it is significant ($t=3.0$).**
> 7. **Using separate $t$ statistics to test a joint hypothesis.** Both $t$'s insignificant, joint $p=0.014$. **This is the collinearity pattern of [[04 - Multiple Regression Analysis - Inference|ch. 04]], and it recurs constantly with interactions and quadratics** — the level term and its square (or interaction) are nearly always highly correlated.
> 8. **Comparing $R^2$ or $\bar R^2$ across models with $y$ and $\log(y)$.** They explain **different dependent variables**. CEO: $\text{SST}(salary)=391{,}732{,}982$ vs $\text{SST}(\log salary)=66.72$. **Use the §4d retransformation measure.**
> 9. **Putting $\bar R^2$ into the $F$ formula.** The statistic has no known distribution. **$F$ uses $R^2$.**
> 10. **Chasing goodness-of-fit into an over-controlled model.** Adding $\log(assess)$ lifts $\bar R^2$ from $0.630$ to $0.762$ **and destroys the hedonic interpretation.** Different models serve different purposes.
> 11. **Exponentiating a log prediction without adjustment.** $\exp(\widehat{\log y})$ is **systematically too low** — by 12% in the CEO example.

> [!important] The three ideas most likely to be examined
>
> **1. The turning-point diagnostic.** Compute $x^*$; then ask *what share of the sample is beyond it*. Marks are given for the diagnosis, not just the number. Signs matter: **opposite signs ⇒ turning point at $x^*>0$; same signs ⇒ $x^*<0$, i.e. no turning point if $x\ge0$.**
>
> **2. The interaction reparameterization.** $y=\alpha_0+\delta_1x_1+\delta_2x_2+\beta_3(x_1-\mu_1)(x_2-\mu_2)+u$ makes $\delta_2$ the partial effect at $\bar x_1$ **and hands you its standard error**. Be able to show $\delta_2=\beta_2+\beta_3\mu_1$ by multiplying out. **It is the same device as the prediction-CI trick of §4a and the linear-combination test of [[04 - Multiple Regression Analysis - Inference|ch. 04]].**
>
> **3. $\mathrm{Var}(\hat e^0)=\mathrm{Var}(\hat y^0)+\sigma^2$ and why the second term is immovable.** The best exam answer names both sources, says which vanishes with $n$, and states that **only reducing $\sigma$ — finding better explanatory variables — narrows an individual prediction interval.**

> [!note] Cross-subject connections
> - **Standardization** (§1a) is the same $z$-score transform used for feature scaling in [[Machine Learning/contents/00-Index|Machine Learning]] and in [[Data Preparation and Visualization/contents/00-Index|Data Preparation & Visualization]]. In ML the motive is **optimization** (gradient descent conditioning) or **regularization** (making the $L^1/L^2$ penalty scale-free); here it is purely **interpretation**. In econometrics standardizing changes no inference at all; in penalized regression it changes the estimates themselves.
> - **Model selection by $\bar R^2$** is the primitive ancestor of **AIC, BIC and HQ**, used for lag-order choice in [[Time-series Analysis/contents/07 - SARIMA and Vector Autoregression|Time-series Analysis]]. All four trade fit against parameter count; they differ only in how steeply they charge for parameters — and **$\bar R^2$ is by far the most permissive** ($|t|>1$ is enough).
> - **Over-controlling** (§3d) is the econometric statement of what causal-inference literature calls **conditioning on a mediator** (a channel) or on a **collider**. The beer-tax example is textbook mediator conditioning.
> - **The prediction-vs-confidence-interval distinction** (§4b) is the same as the split between a **confidence band** and a **prediction band** in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]], and it is exactly what separates in-sample fit from **generalization error** in [[Machine Learning/contents/00-Index|Machine Learning]].
> - **Duan's smearing estimate** (§4d) is a **retransformation bias** correction — the same problem appears whenever a model is fitted on a transformed target and predictions are needed on the original scale, e.g. log-target regression in an ML pipeline.
> - **Beta coefficients as a variable-importance measure** are the linear-model analogue of permutation importance or SHAP values in [[MLOps/contents/00-Index|MLOps]] model-explanation workflows — and share their central weakness: **correlated regressors make "importance" ambiguous no matter how you scale.**

> [!warning] Gaps in the source material
> - **There are no lecture slides for Econometrics.** The chapter scope (Wooldridge 1–12) is my own editorial decision — see [[00-Index]].
> - **No data files are in the vault.** `BWGHT`, `HPRICE1`, `HPRICE2`, `WAGE1`, `ATTEND`, `GPA2`, `CEOSAL1`, `CEOSAL2`, `MLB1`, `RDCHEM` and `APPLE` are all referenced in this chapter and **none can be re-estimated.** Every reported coefficient, standard error and $R^2$ above is **quoted as printed in the text**. Where the text reports enough to check itself, I have verified internal consistency — SSR$/256$, SER$/16$, both turning points, all exact-percentage conversions, both $\bar R^2$ calculations, $\mathrm{se}(\hat e^0)$ in both examples, the CEO point prediction and its prediction interval **all reproduce the printed figures.** ✓
> - **Exercise 3(d) cannot be fully answered.** Determining what share of `WAGE1` has more than 28.7 years of experience requires the data. Wooldridge reports the analogous figure (**28%** beyond 24.4 years) for the levels model only; I have flagged this in the solution rather than guessing.
> - **Figures 6.1 and 6.2 are images** and do not extract. Figure 6.1 plots $wage$ against $exper$ as a parabola peaking at $24.4$ with intercept $3.73$ and maximum $7.37$; Figure 6.2 plots $\log(price)$ against $rooms$ as a U-shape with minimum at $4.4$. **Both are reconstructed from the surrounding prose, which states their content explicitly.**
> - **Table 6.1 extracted intact** (all three columns), and **all its internal relationships check out numerically.**
> - **The `APPLE` $R^2$ of $0.0364$ and the `MLB1` $\bar R^2$ figures ($0.6211$ vs $0.6226$) are quoted, not verified** — the difference in the latter is $0.0015$, well inside what rounding in the text could hide. **Do not lean on that comparison.**
> - **Notation mangling in the PDF:** `b^ j` for $\hat\beta_j$, `b^j` for the beta coefficient $\hat b_j$, `s^ y` for $\hat\sigma_y$, `aˇ 0` for $\check\alpha_0$, `1u^i/1622` for $(\hat u_i/16)^2$, `g` for $\sum$, `E1y0x2` for $\mathbb{E}(y\mid x)$. **Every equation above has been transcribed by hand against its numbered reference.** In particular, the text's own notation collides: **$\hat b_j$ (beta coefficient) versus $\hat\beta_j$ (OLS estimate)** — Wooldridge himself calls this "unfortunate." I have used $\hat b_j$ for the standardized coefficient throughout.
> - **Equation (6.48) extracts with a typo in the source**: the denominator prints as $\sum(y_i-\bar y)$ where it must be $\sum(y_i-\bar y)^2$ for the expression to be an $R^2$. **Corrected above.**

#econometrics #regression #functional-form #prediction #model-selection
