---
subject: Econometrics
chapter: 09
tags: [ds, econometrics, regression, specification, measurement-error, outliers]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 9 (pp. 294–332)"
---

# More on Specification and Data Issues

> [!abstract] What this chapter is for
> [[08 - Heteroskedasticity|Chapter 08]] dealt with a **minor** failure — heteroskedasticity biases nothing and is cheaply fixed. **This chapter returns to the serious one: correlation between $u$ and a regressor.** When $\mathrm{Corr}(u,x_j)\ne0$, $x_j$ is an **endogenous explanatory variable** and OLS is biased and inconsistent.
>
> **Four distinct ways endogeneity arises, and what can be done about each:**
>
> | § | Problem | Remedy available with OLS? |
> |---|---|---|
> | **1** | **Functional form misspecification** — the omitted variable is a *function* of an included one | ✅ **Yes** — you have all the data you need |
> | **2** | **A genuinely unobserved variable** (ability, quality, motivation) | ⚠️ **Partly** — a **proxy variable** or a **lagged dependent variable** |
> | **4** | **Measurement error** in a regressor | ❌ **No** — needs IV (Wooldridge ch. 15) |
> | **5** | **Nonrandom sampling** on the dependent variable | ❌ **No** — needs selection models (ch. 17) |
>
> Plus **§3** on random slopes, **§5c** on outliers, and **§6** on **LAD** — an estimator less sensitive to extreme observations.
>
> **Everything here is still OLS.** Where OLS cannot be rescued, the chapter says so and points forward.

---

## 📘 Main Knowledge

### 1. Functional form misspecification

> [!important] The definition
> A model suffers **functional form misspecification** when it does not properly account for the relationship between $y$ and the **observed** regressors.
>
> **It is a special case of omitted variables bias** — the omitted variable happens to be a **function** of a variable you already have.

**Three ways to commit it:**

| Error | Consequence |
|---|---|
| **Omit $exper^2$** from $\log(wage)=\beta_0+\beta_1 educ+\beta_2 exper+\beta_3 exper^2+u$ | $\hat\beta_0,\hat\beta_1,\hat\beta_2$ all **biased**; and even an unbiased $\hat\beta_2$ would not give the return to experience, which is $\beta_2+2\beta_3exper$ |
| **Omit $female\cdot educ$** when the return to education differs by gender | No parameter is unbiased, **and it is not even clear which return you are estimating** |
| **Use $wage$ where $\log(wage)$ belongs** | Estimators of the partial effects are neither unbiased nor consistent |

> [!tip] Why this is the *least* bad of the endogeneity problems
> **By definition you have data on every variable you need.** The relationship is there in the data; you have simply written it down wrongly. Contrast §2, where the key variable **cannot be collected at all.**
>
> **Fix it by adding quadratics of the significant variables and running a joint $F$ test.** If they are significant, keep them — at the cost of a harder interpretation.
>
> **But a significant quadratic can be symptomatic of something else** — levels where logs belong, or vice versa. **It is often hard to pinpoint *why* the form is wrong.** In practice, logs plus quadratics catch most of the nonlinearity that matters in economics.

#### Example 9.1 — economic model of crime (`CRIME1`, $n=2{,}725$)

| Regressor | (1) linear | (2) with quadratics |
|---|---|---|
| $pcnv$ | $-0.133$ $(0.040)$ | $\mathbf{+0.553}$ $(0.154)$ |
| $pcnv^2$ | — | $-0.730$ $(0.156)$ |
| $avgsen$ | $-0.011$ $(0.012)$ | $-0.017$ $(0.012)$ |
| $tottime$ | $0.012$ $(0.009)$ | $0.012$ $(0.009)$ |
| $ptime86$ | $-0.041$ $(0.009)$ | $\mathbf{+0.287}$ |
| $ptime86^2$ | — | $-0.0296$ $(0.0039)$ |
| $qemp86$ | $-0.051$ $(0.014)$ | $-0.014$ $(0.017)$ |
| $inc86$ | $-0.0015$ $(0.0003)$ | $-0.0034$ $(0.0008)$ |
| $inc86^2$ | — | $+0.000007$ $(0.000003)$ |
| $black$ | $0.327$ $(0.045)$ | $0.292$ $(0.045)$ |
| $hispan$ | $0.194$ $(0.040)$ | $0.164$ $(0.039)$ |
| intercept | $0.569$ $(0.036)$ | $0.505$ $(0.037)$ |
| $R^2$ | $0.0723$ | $\mathbf{0.1035}$ |

**Only the three regressors significant in column (1) were squared.** $qemp86$ takes just five values, so its square is not included.

**Joint significance of the three quadratics:** $F=31.37$ on $(3,\,2713)$ df, $p\approx0$. ✓ (Reproducing from the $R^2$s: $\frac{(0.1035-0.0723)/3}{(1-0.1035)/2713}=31.47$ — rounding.) **The linear model overlooked important nonlinearities.**

**Turning points, and what they mean:**

| Variable | Turning point | Reading |
|---|---|---|
| $pcnv$ | $\approx0.365$ | **No deterrent effect at low conviction rates** — it only "kicks in" at higher prior conviction rates |
| $ptime86$ | $4.85$ months | Positive then negative |
| $inc86$ | $242.85$ ($=\$24{,}285$) | Negative effect on arrests, **with a diminishing magnitude** |

> [!warning] Every one of these needs a caveat, and Wooldridge supplies them
> - **$pcnv$ may not be exogenous.** Men never convicted ($pcnv=0$) are perhaps **casual criminals**, less likely to be arrested anyway. That would bias the estimates directly.
> - **The vast majority of men spent no time in prison in 1986**, so the $ptime86$ curve is fitted on very little variation.
> - **Only 46 of 2,725 men have income above \$24,285**, so the region beyond the $inc86$ turning point is nearly empty.
> - **And the dependent variable is a small count** ($narr86$), which a linear model handles poorly. Poisson models (Wooldridge ch. 17) are better suited.
>
> **This is the [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2b discipline applied four times over: compute the turning point, then ask how much of the sample lies past it.**

#### 1a. RESET — a general functional form test

**The logic in one sentence:** if $y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$ satisfies MLR.4, then **no nonlinear function of the regressors should be significant when added.**

**Adding quadratics has two drawbacks:** it burns degrees of freedom when $k$ is large (exactly like the full White test of [[08 - Heteroskedasticity|ch. 08]]), and **some neglected nonlinearities are simply not quadratic.**

> [!important] Ramsey's (1969) RESET
> 1. Estimate $y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$ by OLS; save the fitted values $\hat y$.
> 2. Estimate the expanded equation
> $$y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+\delta_1\hat y^2+\delta_2\hat y^3+\text{error}$$
> 3. **RESET is the $F$ statistic for $H_0:\delta_1=0,\;\delta_2=0$**, approximately $F_{2,\,n-k-3}$ in large samples.
>
> **You are not interested in the estimated $\delta_j$** — the expanded equation exists only to test. **$\hat y^2$ and $\hat y^3$ are just nonlinear functions of the $x_j$**, exactly as in White's special case ([[08 - Heteroskedasticity|ch. 08]] §3c).
>
> **How many powers?** There is no right answer; **squares and cubes work well in most applications.** An LM version exists ($\chi^2_2$), and both can be made **heteroskedasticity-robust** by the methods of [[08 - Heteroskedasticity|ch. 08]] §2.

**Example 9.2 — housing prices** (`HPRICE1`, $n=88$, $k=3$):

| Model | RESET | $p$ | Verdict |
|---|---|---|---|
| $price=\beta_0+\beta_1 lotsize+\beta_2 sqrft+\beta_3 bdrms+u$ | $4.67$ | $\mathbf{0.012}$ | **Reject** — misspecified |
| $\log(price)=\beta_0+\beta_1 llotsize+\beta_2 lsqrft+\beta_3 bdrms+u$ | $2.56$ | $0.084$ | Do not reject at 5% (would at 10%) |

**On the basis of RESET, the log-log model is preferred.**

> [!warning] Two limitations, one of them widely misunderstood
> **1. RESET gives no direction.** Rejecting the levels model does **not** suggest the log model is the fix. Equation (9.5) was tried because constant-elasticity models are interpretable and well-behaved; it **happened** to pass.
>
> **2. RESET is a functional form test, and nothing more.**
> Some claim it is a general misspecification test covering omitted variables and heteroskedasticity. **This is largely misguided:**
> - **RESET has no power against omitted variables** whenever their expectations are **linear in the included regressors**.
> - **If the functional form is correct, RESET has no power against heteroskedasticity.**
>
> **Compare [[08 - Heteroskedasticity|ch. 08]] §3c, where the arrow points the other way:** a heteroskedasticity test *can* reject because of a functional form error. **So: test functional form with RESET first, then test heteroskedasticity.** Neither test substitutes for the other.

#### 1b. Nonnested alternatives

Is $x_1$ in levels or in logs? Compare
$$y=\beta_0+\beta_1x_1+\beta_2x_2+u \tag{9.6}$$
$$y=\beta_0+\beta_1\log(x_1)+\beta_2\log(x_2)+u \tag{9.7}$$

**Neither is a special case of the other, so no ordinary $F$ test applies** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3c).

**Two approaches:**

> [!important] Mizon–Richard (1986): the comprehensive model
> $$y=\gamma_0+\gamma_1x_1+\gamma_2x_2+\gamma_3\log(x_1)+\gamma_4\log(x_2)+u$$
> - Test **$H_0:\gamma_3=0,\gamma_4=0$** — this is a test of **(9.6)**.
> - Test **$H_0:\gamma_1=0,\gamma_2=0$** — this is a test of **(9.7)**.
>
> Both are ordinary $F$ tests inside a nesting model.

> [!important] Davidson–MacKinnon (1981)
> **If (9.6) is the correct conditional mean, the fitted values from (9.7) should be insignificant when added to it.**
>
> - Estimate (9.7), get fitted values $\check y$. **Test (9.6)** via the $t$ statistic on $\check y$ in
> $$y=\beta_0+\beta_1x_1+\beta_2x_2+\theta_1\check y+\text{error}$$
> - Estimate (9.6), get $\hat y$. **Test (9.7)** via the $t$ on $\hat y$ in the log equation.
>
> **A significant $t$ (two-sided) rejects that model.** Works for **any** two nonnested models with the same dependent variable.
>
> **Note the family resemblance to RESET:** $\check y$ is a nonlinear function of $x_1,x_2$, so it should be irrelevant if the conditional mean is right.

> [!warning] Three problems with nonnested testing
> 1. **No clear winner is guaranteed.** Both models can be rejected, or neither. **If neither, use $\bar R^2$** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3c). **If both, more work is needed.** And ask the practical question: *if the effects of the key variables are similar either way, it does not matter which you use.*
> 2. **Rejecting (9.6) does not endorse (9.7).** (9.6) can be rejected for **any** functional form error.
> 3. **Different dependent variables — $y$ versus $\log(y)$ — is much harder.** Even getting comparable goodness-of-fit measures took [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4d. Tests exist (Wooldridge 1994a) but are beyond this text.

---

### 2. Proxy variables for unobserved regressors

**The hard case: a key variable cannot be collected at all.**

$$\log(wage)=\beta_0+\beta_1 educ+\beta_2 exper+\beta_3 abil+u$$

If $educ$ is correlated with $abil$ and $abil$ sits in the error, **$\hat\beta_1$ and $\hat\beta_2$ are biased** — the recurring theme of [[03 - Multiple Regression Analysis - Estimation|ch. 03]].

> [!note] What we do and do not care about
> - **We care about $\beta_1$ and $\beta_2$** (the slopes).
> - **We do not care about $\beta_0$** — and shall not get it.
> - **We can never estimate $\beta_3$**, and would not know how to interpret it anyway: *"ability is at best a vague concept."*

**A proxy variable is something related to the unobserved variable.** IQ for ability. **IQ need not *be* ability** — it needs to be correlated with it.

#### The framework

$$y=\beta_0+\beta_1x_1+\beta_2x_2+\beta_3x_3^*+u \tag{9.10}$$

with $x_3^*$ unobserved and $x_3$ the proxy, related by

$$x_3^*=\delta_0+\delta_3x_3+v_3 \tag{9.11}$$

**$\delta_3$ measures the relationship; if $\delta_3=0$, $x_3$ is not a suitable proxy.** The intercept $\delta_0$ just allows the two to be on **different scales** (unobserved ability need not average the same as IQ).

**The plug-in solution:** run $y$ on $x_1,x_2,x_3$ — **pretend $x_3$ is $x_3^*$.**

> [!important] The two assumptions the plug-in solution needs
> **(1) $u$ is uncorrelated with $x_1$, $x_2$, $x_3^*$ — and also with $x_3$.**
> The first part is just MLR.4 in model (9.10). **The extra part says $x_3$ is irrelevant once $x_1,x_2,x_3^*$ are included — which is essentially true by definition of a proxy: it is $x_3^*$ that affects $y$, not $x_3$.** Not controversial.
>
> **(2) $v_3$ is uncorrelated with $x_1$, $x_2$ and $x_3$.** ← **This is the demanding one.** Equivalently:
> $$\boxed{\;\mathbb{E}(x_3^*\mid x_1,x_2,x_3)=\mathbb{E}(x_3^*\mid x_3)=\delta_0+\delta_3x_3\;}$$
> **Once $x_3$ is controlled for, the expected value of $x_3^*$ does not depend on $x_1$ or $x_2$.** In the wage example:
> $$\mathbb{E}(abil\mid educ,exper,IQ)=\mathbb{E}(abil\mid IQ)$$
> **Average ability varies with IQ, not with education or experience** — once IQ is held fixed. *Maybe not exactly true, but it may be close, and it is certainly worth including IQ to see what happens.*

#### Why it works — the algebra

Substituting (9.11) into (9.10):
$$y=\underbrace{(\beta_0+\beta_3\delta_0)}_{\alpha_0}+\beta_1x_1+\beta_2x_2+\underbrace{\beta_3\delta_3}_{\alpha_3}x_3+\underbrace{u+\beta_3v_3}_{e}$$

**Under the two assumptions, $e$ has zero mean and is uncorrelated with $x_1,x_2,x_3$.** So the regression consistently estimates $\alpha_0$, **$\beta_1$, $\beta_2$**, and $\alpha_3$.

> [!important] What you get and what you lose
> - **You do NOT get $\beta_0$ or $\beta_3$** — you get $\alpha_0=\beta_0+\beta_3\delta_0$ and $\alpha_3=\beta_3\delta_3$.
> - **You DO get $\beta_1$ and $\beta_2$ — which is what you wanted.**
> - **And $\alpha_3$ is usually the more interesting quantity anyway:** in the wage equation it is **the return to one more IQ point**, which is measurable, whereas $\beta_3$ (the return to one more unit of "ability") is not.

#### Example 9.3 — IQ as a proxy for ability (`WAGE2`, $n=935$ men, 1980)

| | (1) no IQ | (2) with IQ | (3) with $educ\cdot IQ$ |
|---|---|---|---|
| $educ$ | $\mathbf{0.065}$ $(0.006)$ | $\mathbf{0.054}$ $(0.007)$ | $0.018$ $(0.041)$ |
| $exper$ | $0.014$ $(0.003)$ | $0.014$ $(0.003)$ | $0.014$ $(0.003)$ |
| $tenure$ | $0.012$ $(0.002)$ | $0.011$ $(0.002)$ | $0.011$ $(0.002)$ |
| $married$ | $0.199$ $(0.039)$ | $0.200$ $(0.039)$ | $0.201$ $(0.039)$ |
| $south$ | $-0.091$ $(0.026)$ | $-0.080$ $(0.026)$ | $-0.080$ $(0.026)$ |
| $urban$ | $0.184$ $(0.027)$ | $0.182$ $(0.027)$ | $0.184$ $(0.027)$ |
| $black$ | $-0.188$ $(0.038)$ | $\mathbf{-0.143}$ $(0.039)$ | $-0.147$ $(0.040)$ |
| $IQ$ | — | $0.0036$ $(0.0010)$ | $-0.0009$ $(0.0052)$ |
| $educ\cdot IQ$ | — | — | $0.00034$ $(0.00038)$ |
| $R^2$ | $0.253$ | $0.263$ | $0.263$ |

> [!important] Everything in this table tells a story
> - **The return to education falls from 6.5% to 5.4%** — exactly the direction predicted if omitted ability is **positively** correlated with education. **The proxy is doing its job.**
> - **$IQ$ is significant**: 10 more IQ points $\Rightarrow$ **3.6% higher earnings.** The sd of IQ in the US population is 15, so **one sd of IQ is worth $15(0.0036)=5.4\%$ — identical to one more year of education.** (The effect documented, controversially, in Herrnstein & Murray's *The Bell Curve*.)
> - **Education still matters a great deal**, just less than the naive estimate said.
> - **$R^2$ rises only from 0.253 to 0.263.** **Most of the variation in $\log(wage)$ is still unexplained** — a reminder that a proxy variable is about **bias**, not fit.
> - **Adding IQ does not eliminate the black–white gap**: a black man with the **same IQ**, education and experience is predicted to earn **14.3% less**, and the difference is very significant.
> - **Column (3) is worse, not better.** The interaction is insignificant, and adding it makes $educ$ and $IQ$ **individually insignificant** while complicating the model. (**And note: with $educ\cdot IQ$ present, the $educ$ coefficient is the return to education at $IQ=0$** — the [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §4b trap.) **Column (2) is preferred.**
>
> `WAGE2` also contains a **Knowledge of the World of Work (KWW)** score — a second proxy, usable instead of or alongside IQ. **There is no reason to stop at one proxy.**

#### When the proxy fails

Suppose the truth is
$$x_3^*=\delta_0+\delta_1x_1+\delta_2x_2+\delta_3x_3+v_3 \tag{9.14}$$
i.e. $\delta_1,\delta_2\ne0$ — **$x_3^*$ still depends on $x_1,x_2$ even after controlling for $x_3$.** Then

$$y=(\beta_0+\beta_3\delta_0)+(\beta_1+\beta_3\delta_1)x_1+(\beta_2+\beta_3\delta_2)x_2+\beta_3\delta_3x_3+u+\beta_3v_3$$

$$\boxed{\;\operatorname{plim}(\hat\beta_1)=\beta_1+\beta_3\delta_1,\qquad \operatorname{plim}(\hat\beta_2)=\beta_2+\beta_3\delta_2\;}$$

**With $x_1=educ$ and $x_3^*=abil$: $\beta_3>0$, so if ability retains a positive partial correlation with education ($\delta_1>0$), the return to education is still biased upward.**

> [!tip] But it is still worth doing
> *"We can reasonably hope that this bias is smaller than if we ignored the problem of omitted ability entirely."* **An imperfect proxy usually reduces the bias even when it does not remove it.**

> [!warning] "But IQ and educ are collinear — you're inflating my standard errors!"
> **This complaint misses two points.**
>
> 1. **Adding IQ *reduces* the error variance**, because the part of ability explained by IQ is taken out of $u$. This usually shows up as a **smaller SER** — partially offsetting the collinearity ([[08 - Heteroskedasticity|ch. 08]] and [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3e).
> 2. **More importantly: the added multicollinearity is a necessary evil.** *The reason $educ$ and $IQ$ are correlated is that $educ$ and $abil$ are correlated — that is the entire problem.* **If we could observe $abil$ we would include it, and the same collinearity would appear.** You cannot remove omitted variable bias without confronting the correlation that caused it.
>
> **This is the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] bias–variance trade-off**, and here the trade is worth making.

> [!note] Proxies can be binary
> Krueger (1993) — Example 7.9 — included a dummy for **computer use at home** alongside computer use at work. **Its purpose was to proxy for unobserved "technical ability"** that could affect wages directly and be related to computer use at work.

#### 2a. Lagged dependent variables as proxies

**Sometimes you suspect endogeneity but have no idea what to proxy for.** Then include **an earlier value of $y$**.

$$crime=\beta_0+\beta_1 unem+\beta_2 expend+\beta_3 crime_{-1}+u \tag{9.16}$$

> [!important] Why the lag belongs there
> We expect $\beta_3>0$ (crime has **inertia**) — but that is not the reason for including it.
>
> **The reason is that cities with high historical crime rates spend more on law enforcement.** Unobserved factors driving crime are therefore correlated with $expend$. **A pure cross-section cannot recover the causal effect of spending.**
>
> **With $crime_{-1}$ in the equation, $\beta_2$ answers a well-posed question:** *if two cities have the same previous crime rate and the same current unemployment rate, what does another dollar of law enforcement do?*
>
> **The lag captures historical factors that are otherwise impossible to account for**, and it captures inertia. Cost: **you now need two years of data.**

**Example 9.4 — city crime rates** (`CRIME2`, 46 cities, 1987):

| | (1) | (2) |
|---|---|---|
| $unem87$ | $-0.029$ $(0.032)$ | $0.009$ $(0.020)$ |
| $\log(lawexpc87)$ | $\mathbf{+0.203}$ $(0.173)$ | $\mathbf{-0.140}$ $(0.109)$ |
| $\log(crmrte82)$ | — | $1.194$ $(0.132)$ |
| intercept | $3.34$ $(1.25)$ | $0.076$ $(0.821)$ |
| $R^2$ | $0.057$ | $\mathbf{0.680}$ |

- **Without the lag, the expenditure elasticity is *positive*** ($t=1.17$) — spending more on police is associated with **more** crime. Possible readings: more enforcement improves **reporting**, so more crimes are recorded; **or** cities with high recent crime spend more.
- **With the lag, the elasticity flips to $-0.14$** ($t=-1.28$). **Not significant, but suggestive** — a bigger sample of cities could produce significance.
- **The lag is strongly related to current crime:** a 1% higher 1982 crime rate predicts a **1.19% higher** 1987 rate. **Cannot reject unit elasticity:** $t=(1.194-1)/0.132=\mathbf{1.47}$.
- **$R^2$ jumps from 0.057 to 0.680** — unsurprising, and **not the point.** *"The primary reason for including the lagged crime rate is to obtain a better estimate of the ceteris paribus effect of $\log(lawexpc87)$."*

> [!note] It is a crude device, and Wooldridge says so
> *"The practice of putting in a lagged $y$ as a general way of controlling for unobserved variables is hardly perfect. But it can aid in getting a better estimate of the effects of policy variables."* **Additional lags can be included when available. Panel data methods (Wooldridge chs. 13–14) do this properly.**

#### 2b. A different slant on multiple regression

> [!important] Set the goal more modestly, and the philosophical problem disappears
> Instead of positing a model with an unobservable and asking whether IQ is a "suitable proxy for ability," **just state from the outset what you are estimating:**
> $$\mathbb{E}(lwage\mid educ,exper,tenure,south,urban,black,IQ)$$
> **which is exactly what Table 9.2 reports.**
>
> The question answered becomes: *"If two people have the same IQ (and experience, tenure, …) but differ in education by one year, what is the expected difference in their log wages?"* **A question of genuine interest, with no nebulous concept of "ability" required.**
>
> **Same logic elsewhere.** A school poverty rate only crudely captures differences in children and parents. **But it is often all we have, and controlling for it almost certainly gets us closer to the ceteris paribus effect of spending than leaving it out.**

> [!tip] And if you only want to **predict**, the whole worry evaporates
> An admissions officer predicting college GPA should use whatever is **observable at application time** — high school GPA, test scores, activities, family background.
>
> - **Do not include college attendance** — it is not observed at application time.
> - **Do not wring your hands about "bias" from omitting attendance.** You have no interest in the effect of high school GPA *holding college attendance fixed*.
> - **Do not worry about unobserved motivation.** It would help if you had it; in its absence, fit the best model you can.
>
> **"Omitted variable bias" is a concept about causal parameters. It does not apply to a pure prediction problem.**

---

### 3. Models with random slopes

**What if the partial effect differs across units for *unobserved* reasons?**

$$y_i=a_i+b_ix_i \tag{9.17}$$

with a **unit-specific intercept and slope**. The simple regression model is the case $b_i=b$ with $a_i$ relabelled as $u_i$. **If $y_i=\log(wage_i)$ and $x_i=educ_i$, this lets the return to education vary by person** — for instance with unmeasured ability.

We cannot estimate $n$ slopes. **But we can estimate the average.** Define $\alpha=\mathbb{E}(a_i)$ and $\beta=\mathbb{E}(b_i)$; $\beta$ is the **average partial effect (APE)** — the average return to a year of schooling in the population. Write $a_i=\alpha+c_i$, $b_i=\beta+d_i$ (so $\mathbb{E}(c_i)=\mathbb{E}(d_i)=0$):

$$y_i=\alpha+\beta x_i+\underbrace{c_i+d_ix_i}_{u_i}$$

> [!important] When does plain OLS recover the APE?
> $$\boxed{\;\mathbb{E}(a_i\mid x_i)=\mathbb{E}(a_i)\quad\text{and}\quad\mathbb{E}(b_i\mid x_i)=\mathbb{E}(b_i)\;}$$
> — **both the intercept and the slope are mean independent of $x_i$.**
>
> **If so, OLS consistently estimates the population average of the individual slopes.** A genuinely useful finding: you do not need constant coefficients, only **uncorrelated** ones.

> [!warning] But heteroskedasticity is then automatic
> If $\mathrm{Var}(c_i\mid x_i)=\sigma_c^2$, $\mathrm{Var}(d_i\mid x_i)=\sigma_d^2$, $\mathrm{Cov}(c_i,d_i\mid x_i)=0$, then
> $$\mathrm{Var}(u_i\mid x_i)=\sigma_c^2+\sigma_d^2x_i^2$$
> **which is non-constant unless $\sigma_d^2=0$, i.e. unless every slope is the same.**
>
> **Handle it with robust standard errors, or estimate this variance function and use WLS** ([[08 - Heteroskedasticity|ch. 08]]) — but WLS here imposes homoskedasticity on $c_i$ and $d_i$, so **make the WLS analysis fully robust.**
>
> **Some authors therefore view heteroskedasticity generally as arising from random slopes. Resist this.** The form $\sigma_c^2+\sigma_d^2x_i^2$ is **special**, and it does not allow heteroskedasticity in $a_i$ or $b_i$ themselves. **A random-slope model and a constant-slope model with heteroskedastic $a_i$ cannot be convincingly distinguished.**

**Multiple regression works the same way.** And slopes may depend on **observables** too: with $b_{i2}=\beta_2+\delta_1(x_{i1}-\mu_1)+d_{i2}$,
$$\mathbb{E}(y_i\mid x_{i1},x_{i2})=\alpha+\beta_1x_{i1}+\beta_2x_{i2}+\delta_1(x_{i1}-\mu_1)x_{i2}$$
**— an interaction, with the mean subtracted so that $\beta_2$ is the APE.** Exactly the centring device of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2c.

> [!note] The point of this section
> **[[06 - Multiple Regression Analysis - Further Issues|Chapter 06]] justified squares and interactions as flexible functional forms. Random slopes give them a second, independent justification.** Allowing for random slopes is straightforward **provided they are mean independent of the regressors**. If the random intercept or slopes are **correlated** with the regressors, estimation becomes much harder — that is endogeneity, and it needs Wooldridge ch. 15.

---

### 4. Measurement error

> [!important] Measurement error is **not** the same problem as a proxy variable
> | | Proxy variable | Measurement error |
> |---|---|---|
> | The unobserved variable | **Vague concept** — "ability" | **Well-defined quantity** — actual income, marginal tax rate |
> | What you have | Something **associated** with it (IQ) | An **imprecise measure** of it (reported income) |
> | Variable of interest | Usually the **other** regressors | Often the **mismeasured variable itself** |
>
> **IQ is a proxy for ability. Reported income is a mismeasure of actual income.** The statistical structures are similar; the concepts are different.
>
> **And measurement error only matters when the variable the econometrician can collect differs from the variable that drives behaviour.**

#### 4a. Measurement error in the **dependent** variable

$$y^*=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u,\qquad e_0=y-y^*$$

Substituting $y^*=y-e_0$:
$$y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+\underbrace{u+e_0}_{\text{new error}}$$

> [!important] Verdict: usually harmless
> **If $e_0$ is independent of every $x_j$ (the usual assumption), the OLS estimators are unbiased and consistent, and $t$, $F$ and LM are all valid.** A non-zero mean for $e_0$ only biases the **intercept**, which is rarely a concern.
>
> **The only cost is precision.** If $e_0$ and $u$ are uncorrelated,
> $$\mathrm{Var}(u+e_0)=\sigma_u^2+\sigma_0^2>\sigma_u^2$$
> **so the standard errors are larger.** *"This is to be expected and there is nothing we can do about it (except collect better data)."*

**Example 9.5 — savings.** $sav^*=\beta_0+\beta_1 inc+\beta_2 size+\beta_3 educ+\beta_4 age+u$, with $sav$ the reported figure. **Is the reporting error related to income or education?** Plausibly families with higher incomes or more education report more accurately. **We can never know without data on $sav^*$** — in which case we would not have the problem.

**With a logged dependent variable**, the natural form is
$$\log(y)=\log(y^*)+e_0$$
which follows from **multiplicative** measurement error $y=y^*a_0$ with $e_0=\log(a_0)$.

> [!warning] Example 9.6 — when the error *is* correlated, and in the worst possible way
> $$\log(scrap^*)=\beta_0+\beta_1 grant+u,\qquad \log(scrap)=\log(scrap^*)+e_0$$
>
> **A cynical reading: a firm that received a grant is more likely to under-report its scrap rate, to make the grant look effective.** Then in the estimable equation
> $$\log(scrap)=\beta_0+\beta_1 grant+u+e_0$$
> **the composite error is negatively correlated with $grant$, producing a downward bias in $\hat\beta_1$** — which makes the training programme look **more** effective than it was (a lower scrap rate means higher productivity, so a more negative $\hat\beta_1$ is a "better" result).
>
> **Measurement error in $y$ is benign only when it is unrelated to the regressors. Incentives to misreport destroy exactly that.**

#### 4b. Measurement error in an **explanatory** variable

**This is the case traditionally regarded as serious.**

$$y=\beta_0+\beta_1x_1^*+u,\qquad e_1=x_1-x_1^*$$

We assume $\mathbb{E}(e_1)=0$ and, throughout, that **$u$ is uncorrelated with both $x_1^*$ and $x_1$** — equivalently $\mathbb{E}(y\mid x_1^*,x_1)=\mathbb{E}(y\mid x_1^*)$, which says $x_1$ does not affect $y$ once $x_1^*$ is controlled for. **Uncontroversial; it holds almost by definition.**

**Everything then depends on which of two polar assumptions you make.**

##### Case 1: $\mathrm{Cov}(x_1,e_1)=0$ — the error is uncorrelated with the *observed* measure

Write $x_1^*=x_1-e_1$:
$$y=\beta_0+\beta_1x_1+(u-\beta_1e_1)$$

**Since $u$ and $e_1$ both have zero mean and are uncorrelated with $x_1$, so is the composite error. OLS is consistent.** The error variance rises to $\sigma_u^2+\beta_1^2\sigma_{e_1}^2$ (unless $\beta_1=0$), so **standard errors are larger — and nothing else changes.**

> [!note] This is the proxy-variable assumption in disguise
> **It is the analogue of the §2 condition, and it makes OLS work perfectly.** Which is precisely why *this* is not what econometricians mean when they say "measurement error in a regressor."

##### Case 2: the **classical errors-in-variables (CEV)** assumption

$$\boxed{\;\mathrm{Cov}(x_1^*,e_1)=0\;}$$

i.e. write $x_1=x_1^*+e_1$ and assume the **two components are uncorrelated.** Then

$$\mathrm{Cov}(x_1,e_1)=\mathbb{E}(x_1^*e_1)+\mathbb{E}(e_1^2)=0+\sigma_{e_1}^2=\sigma_{e_1}^2\;\ne\;0$$

**The covariance between the observed measure and the error equals the variance of the measurement error.** So in $y=\beta_0+\beta_1x_1+(u-\beta_1e_1)$,

$$\mathrm{Cov}(x_1,\,u-\beta_1e_1)=-\beta_1\sigma_{e_1}^2\;\ne\;0$$

**OLS is biased and inconsistent.**

> [!important] Attenuation bias — the central formula
> $$\operatorname{plim}(\hat\beta_1)=\beta_1+\frac{\mathrm{Cov}(x_1,u-\beta_1e_1)}{\mathrm{Var}(x_1)}=\beta_1-\frac{\beta_1\sigma_{e_1}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}$$
> $$\boxed{\;\operatorname{plim}(\hat\beta_1)=\beta_1\left(\frac{\sigma_{x_1^*}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}\right)\;}$$
> using $\mathrm{Var}(x_1)=\mathrm{Var}(x_1^*)+\mathrm{Var}(e_1)$.
>
> **The multiplier — the *reliability ratio* — is always strictly between 0 and 1.**
>
> **Therefore $\operatorname{plim}(\hat\beta_1)$ is always closer to zero than $\beta_1$.** This is **attenuation bias**. If $\beta_1>0$, OLS **understates** it.
>
> **How bad it is depends entirely on the signal-to-noise ratio $\sigma_{x_1^*}^2/\sigma_{e_1}^2$.** If the true variable varies a lot relative to the measurement error, the reliability ratio is near 1 and **the inconsistency is small.** *"Measurement error need not cause large biases."*

##### With more regressors

$$y=\beta_0+\beta_1x_1^*+\beta_2x_2+\beta_3x_3+u$$

Assume $e_1$ is uncorrelated with $x_2$ and $x_3$ (almost always assumed) and with $u$.

- **If $e_1$ is uncorrelated with $x_1$ (Case 1): OLS on $y$ against $x_1,x_2,x_3$ is consistent.** ✅
- **Under CEV: everything is inconsistent — not just $\hat\beta_1$.**

$$\boxed{\;\operatorname{plim}(\hat\beta_1)=\beta_1\left(\frac{\sigma_{r_1^*}^2}{\sigma_{r_1^*}^2+\sigma_{e_1}^2}\right)\;}$$

where $r_1^*$ is the **population error from $x_1^*=\alpha_0+\alpha_1x_2+\alpha_2x_3+r_1^*$** — that is, $x_1^*$ **after partialling out the other regressors.**

> [!warning] Two consequences that are easy to miss
> **1. Attenuation gets *worse* with more regressors.** $\sigma_{r_1^*}^2\le\sigma_{x_1^*}^2$ — partialling out can only reduce variation. **So the reliability ratio falls, and the bias toward zero grows.** The more collinear $x_1^*$ is with the other regressors, the more severe the attenuation. **(Compare the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] variance formula: the same partialled-out variation appears in the denominator there.)**
>
> **2. The coefficients on the *correctly measured* variables are also inconsistent** — and *"the sizes, and even the directions of the biases, are not easily derived."* They are consistent only in the rare case that $x_1^*$ is uncorrelated with $x_2$ and $x_3$.

**Example 9.7 — GPA and family income:**
$$colGPA=\beta_0+\beta_1 faminc^*+\beta_2 hsGPA+\beta_3 SAT+u$$
$colGPA$, $hsGPA$ and $SAT$ are measured precisely; **family income as reported by students is not.** Under CEV, $\hat\beta_1$ is **biased toward zero**, so a test of $H_0:\beta_1=0$ has **less chance of detecting a genuine positive effect.** *The attenuation makes you more likely to conclude family income does not matter when it does.*

> [!warning] When CEV is clearly false
> $$colGPA=\beta_0+\beta_1 smoked^*+\beta_2 hsGPA+\beta_3 SAT+u$$
> where $smoked^*$ is the actual number of occasions a student smoked marijuana in the last 30 days.
>
> **Students who never smoke ($smoked^*=0$) will report 0 — the measurement error is exactly zero for them.** Students with $smoked^*>0$ are much more likely to miscount. **So $e_1$ and $smoked^*$ are correlated, violating CEV directly.**
>
> **Deriving the implications is beyond the text.** The general lesson: **CEV, while more believable than Case 1, is still a strong assumption. The truth is usually somewhere in between — and if $e_1$ is correlated with *both* $x_1^*$ and $x_1$, OLS is inconsistent with no clean formula.**
>
> **Must we accept inconsistency? No.** Wooldridge ch. 15 shows how **instrumental variables** consistently estimate the parameters under general measurement error — but that requires leaving OLS behind. **Multiple measures of the same variable can also reduce the attenuation.**

---

### 5. Missing data, nonrandom samples, and outliers

**These are violations of MLR.2 (random sampling), not MLR.4.** Some are harmless; some are fatal.

> [!note] Multicollinearity is *not* one of them
> Correlation among the regressors **violates no assumption.** It makes partial effects hard to estimate precisely — **and the usual OLS statistics report that honestly** through $\mathrm{se}(\hat\beta_j)$. Nothing is hidden.

#### 5a. Missing data

**Missing values are common:** 196 of 1,388 observations in `BWGHT` have no father's education (14%); 6 of 156 law schools in `LAWSCH85` lack median LSAT; 949 men in `CARD` have no IQ score.

**Any observation missing $y$ or any $x_j$ cannot be used.** Packages drop them automatically — the **complete cases estimator**.

> [!important] MCAR — when missingness is harmless
> Data are **missing completely at random (MCAR)** if the reason for missingness is **statistically independent of both the observed and unobserved factors affecting $y$.**
>
> **Under MCAR, missing data cause no statistical problem** — you can still treat the remaining data as a random sample, so MLR.2 holds. **The only cost is a smaller $n$.**

##### The missing indicator method, and why it is worse than it looks

**A tempting "fix":** when $x_k$ is sometimes missing, define
- $Z_{ik}=x_{ik}$ if observed, $0$ otherwise;
- $m_{ik}=1$ if $x_{ik}$ is missing, $0$ otherwise;

and regress $y_i$ on $x_{i1},\dots,x_{i,k-1},Z_{ik},m_{ik}$ using **all** observations.

**The appeal is obvious:** with $n=1{,}000$ and 30% missing, complete cases uses 700 while MIM uses 1,000.

> [!warning] The gain is largely illusory
> **MIM is consistent only under strong assumptions — MCAR *plus*, essentially, that $x_k$ is uncorrelated with $x_1,\dots,x_{k-1}$** (Jones 1996; Abrevaya & Donald 2018). **That is a severe restriction, and it is rarely plausible.**
>
> **Compare the complete cases estimator, which is *more* robust:** it stays consistent even when missingness depends on $(x_1,\dots,x_k)$ — something MCAR explicitly rules out — and it **puts no restrictions whatever on the correlations among the regressors.**
>
> **And one thing is certain: omitting $m_{ik}$ from the regression is a very poor idea** — that is identical to setting $x_{ik}=0$ whenever it is missing.
>
> **The counterintuitive bottom line: the naive default (drop incomplete cases) is the *more* robust procedure. More sophisticated fill-in schemes exist but are beyond this text.**

#### 5b. Nonrandom samples

> [!important] The distinction that decides everything: what is the selection based on?
>
> | Selection based on… | Name | Effect on OLS |
> |---|---|---|
> | **The independent variables** (or otherwise independent of $u$) | **Exogenous** sample selection / **MAR** | ✅ **Unbiased and consistent** |
> | **The dependent variable** | **Endogenous** sample selection | ❌ **Biased and inconsistent — always** |

**Exogenous selection.** For $saving=\beta_0+\beta_1 income+\beta_2 age+\beta_3 size+u$, a survey of **people over 35** gives a nonrandom sample of adults. **OLS is still unbiased**, because $\mathbb{E}(saving\mid income,age,size)$ **is the same for any subpopulation defined by $income$, $age$ or $size$.** *Provided there is enough variation in the regressors within the subpopulation*, the only cost is a smaller sample.

> [!note] "Missing at random" is a badly chosen name
> **MAR** allows missingness to depend on $(x_1,\dots,x_k)$; it only requires it be unrelated to $u$. **MCAR** requires missingness be unrelated to the $x_j$ **and** $u$.
>
> **So "random" here connotes *less* randomness than "completely at random"** — the reverse of what the words suggest. Blame Little & Rubin's terminology, not the statistics.

**Endogenous selection — always fatal.** For $wealth=\beta_0+\beta_1 educ+\beta_2 exper+\beta_3 age+u$, sampling **only people with wealth below \$250,000** biases everything, because
$$\mathbb{E}(wealth\mid educ,exper,age)\;\ne\;\mathbb{E}(wealth\mid educ,exper,age,\;wealth<250{,}000)$$

**Stratified sampling** divides the population into non-overlapping strata and over- or under-samples some. **The same test applies:**

| Stratification | OLS |
|---|---|
| **Oversample women** in a military pay survey (provided men are also sampled) | ✅ Fine — stratified on an **explanatory** variable |
| **Oversample lower-paid personnel** | ❌ Inconsistent — stratified on the **dependent** variable |

> [!warning] The subtle case — and why `WAGE1` is not what it appears
> Labour economists want the **wage offer** equation
> $$\log(wage^o)=\beta_0+\beta_1 educ+\beta_2 exper+u$$
> for the population of **all working-age people.** Every such person faces a wage offer and chooses whether to work. **For workers, the offer is the observed wage. For non-workers, the offer is unobserved** — though $educ$ and $exper$ can still be collected.
>
> **`WAGE1` is a random sample of *working* individuals — not of the population the equation describes.**
>
> **Is this endogenous selection?** *Not clear-cut.* Selection is on the **decision to work**, not directly on the size of the wage offer. **But the decision to work may be related to unobserved factors that affect the offer** — in which case selection is endogenous and OLS suffers **sample selection bias.**
>
> **Testing and correcting for it requires Wooldridge ch. 17.** *(And note the connection: [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]]'s `MROZ` labour-force-participation equation is exactly the model of that selection decision.)*

#### 5c. Outliers and influential observations

> [!important] Definitions, both admittedly vague
> - **Influential observation:** dropping it changes the key OLS estimates by a practically large amount.
> - **Outlier:** requires comparing one observation against the rest — inherently a judgement.
>
> **OLS is susceptible because it minimizes the sum of *squared* residuals — large residuals get enormous weight.**

**Two origins:**
1. **Data entry error** — an extra zero, a misplaced decimal. **Always compute summary statistics, especially minimums and maximums.** (But incorrect entries are not always obvious.)
2. **Genuinely unusual members of a small population.** Harder: the decision to keep or drop is difficult and the statistical properties of the result are complicated. **Outliers can be informative — they increase variation in the regressors, which *reduces* standard errors.**

> [!tip] The professional response
> **Report results with and without the suspect observations** whenever one or several data points substantially change the conclusions.

**Example 9.8 — R&D intensity and firm size** (`RDCHEM`, 32 chemical companies):

$$\widehat{rdintens}=2.625+0.000053\,sales+0.0446\,profmarg,\qquad R^2=0.0761,\;\bar R^2=0.0124$$
$$\qquad\qquad\;\;(0.586)\;(0.000044)\qquad\;(0.0462)$$

**Neither regressor is significant at even 10%** ($t_{sales}=1.20$).

**31 of 32 firms have sales under \$20 billion; one has almost \$40 billion — over twice the size of every other firm.** Dropping it:

$$\widehat{rdintens}=2.297+0.000186\,sales+0.0478\,profmarg,\qquad R^2=0.1728,\;\bar R^2=0.1137$$
$$\qquad\qquad\;\;(0.592)\;(0.000084)\qquad\;(0.0445)$$

**The $sales$ coefficient more than triples** ($0.000186/0.000053=3.5$) **and $t=2.21$ — now significant.** $profmarg$ barely moves.

##### Studentized residuals — and why they are not enough

> [!warning] Defining outliers by the size of the OLS residual is a bad idea
> **OLS adjusts to make the residuals small.** Including the largest firm **flattened the regression line**, so that firm's own residual is only $-1.62$ — against $\hat\sigma=1.82$, **less than one standard deviation from zero.** *The observation that distorted the whole regression does not look unusual by its residual.*

**Studentized residuals** divide the OLS residuals by an estimate of their standard deviation. **The computational trick:**

> [!important] The dummy-variable trick
> **Define a dummy equal to 1 for observation $h$ and 0 otherwise, and include it in the regression using all observations.**
>
> - **The dummy's coefficient is the residual for observation $h$ computed from the regression line fitted using only the *other* observations.**
> - **The $t$ statistic on the dummy *is* the studentized residual**, distributed $t_{n-k-2}$ under the CLM assumptions.
>
> Same device as the recentring trick of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4a: **make the quantity you want into a coefficient, and the package hands you its standard error.**

**Applied to `RDCHEM`:**

| Observation | Dummy coefficient | Studentized residual ($t$) |
|---|---|---|
| **#10** — largest firm | $-6.57$ | $-1.82$ ($p=0.08$) |
| **#1** — highest $rdintens$ ($\approx9.42$) | $+6.72$ | $\mathbf{+4.56}$ |

> [!warning] The conundrum, laid out plainly
> **By the studentized-residual criterion, observation 1 is *more* of an outlier than observation 10.** Yet:
> - **Dropping #10 more than triples the $sales$ coefficient.**
> - **Dropping #1 changes it barely at all** ($0.000053\to0.000051$), though $profmarg$ becomes larger and significant.
>
> **So which is the outlier?** *"These calculations show the conundrum one can enter when trying to determine observations that should be excluded, even when the data set is small."*
>
> **The general defect: the size of a studentized residual need not correspond to how influential an observation is** — and certainly not for all coefficients at once. **And there is circularity:** when computing #1's studentized residual, **#10 is still being used to fit the line** — and with the line flattened by #10, it is unsurprising that #1 looks far off.
>
> **Dropping both** (equivalently, adding two dummies): $n=30$, $R^2=0.2711$,
> $$\widehat{rdintens}=1.939+0.000160\,sales+0.0701\,profmarg$$
> $$\qquad\qquad\;\;(0.459)\;(0.000065)\qquad\;(0.0343)$$
> **Now both are significant** ($t=2.46$ and $t=2.04$, $p=0.051$). Dummy coefficients: $+6.47$ ($t=4.58$) for #1, $-5.41$ ($t=-1.95$) for #10. **And two observations still have studentized residuals above 2.** *There is no natural stopping point.*
>
> **Belsley, Kuh & Welsch (1980) formalize this with the *leverage* of an observation** — but it requires matrix algebra.

##### Logs again

**Example 9.9 — the same question, in logs.** Start from
$$rd=sales^{\beta_1}\exp(\beta_0+\beta_2 profmarg+u)\quad\Longrightarrow\quad \log(rd)=\beta_0+\beta_1\log(sales)+\beta_2 profmarg+u$$

**R&D intensity increases with size if and only if $\beta_1>1$.**

| Sample | $\hat\beta_1$ | se | $R^2$ | $t$ for $H_0:\beta_1=1$ |
|---|---|---|---|---|
| All 32 | $1.084$ | $0.060$ | $0.9180$ | $\mathbf{1.40}$ |
| Drop largest | $1.088$ | $0.067$ | $0.9037$ | $\mathbf{1.31}$ |

> [!tip] **Practically identical.** In neither case do we reject $H_0:\beta_1=1$ against $\beta_1>1$
> **The log transformation made the outlier problem disappear.** As [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a said: logs **narrow the range** of economic variables and yield functional forms — constant-elasticity models — that fit a **broader range of data.**
>
> **Notice also that $R^2$ jumped from 0.076 to 0.918** — but that comparison is **illegitimate**, because the dependent variables differ ($rdintens$ vs $\log(rd)$). [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3c.

**Example 9.10 — state infant mortality** (`INFMRT`, 50 states + D.C., 1990):

$$\widehat{infmort}=33.86-4.68\log(pcinc)+4.15\log(physic)-0.088\log(popul),\quad R^2=0.139$$
$$\qquad\qquad\;(20.43)\;\;(2.60)\qquad\qquad(1.51)\qquad\qquad(0.287)$$

**More physicians per capita is associated with *higher* infant mortality** ($t=2.75$) — counterintuitive. Population appears irrelevant.

**D.C. is unusual:** pockets of extreme poverty and great wealth in a tiny area. Infant mortality **20.7** vs **12.4** for the worst state; **615 physicians** per 100,000 vs **337** for the highest state. Dropping it:

$$\widehat{infmort}=23.95-0.57\log(pcinc)-2.74\log(physic)+0.629\log(popul),\quad R^2=0.273$$
$$\qquad\qquad\;(12.42)\;\;(1.64)\qquad\qquad(1.19)\qquad\qquad(0.191)$$

| | With D.C. | Without D.C. |
|---|---|---|
| $\log(physic)$ | $+4.15$, $t=2.75$ | $\mathbf{-2.74}$, $t=-2.30$ ✅ |
| $\log(pcinc)$ | $-4.68$, $t=-1.80$ | $-0.57$, $t=-0.35$ ❌ |
| $\log(popul)$ | $-0.088$, $t=-0.31$ | $+0.629$, $t=\mathbf{3.29}$ ✅ |
| $R^2$ | $0.139$ | $0.273$ |

> [!important] **Every conclusion in the equation reverses.** One observation out of 51
> More physicians now **lowers** infant mortality, significantly. The income effect collapses. Population becomes strongly significant. **And far more variation is explained.**
>
> *"Clearly, D.C. had substantial influence on the initial estimates, and we would probably leave it out of any further analysis."*
>
> **Note that D.C. was suspect *before* looking at the regression** — it is a city being treated as a state. **When you know in advance that a unit is fundamentally different, say so up front rather than discovering it through diagnostics.** This is common with aggregated data at city, county or state level.

---

### 6. Least absolute deviations

**Instead of hunting for influential observations, use an estimator that is less sensitive to them.**

$$\boxed{\;\min_{b_0,\dots,b_k}\;\sum_{i=1}^n\left|y_i-b_0-b_1x_{i1}-\cdots-b_kx_{ik}\right|\;}$$

> [!important] Why LAD is resistant
> **The LAD objective is linear on either side of zero:** a residual one unit larger raises the objective by one unit. **The OLS objective is quadratic, giving ever-increasing weight to large residuals.**
>
> **LAD estimates the parameters of the conditional *median* of $y$ given $\mathbf{x}$, not the conditional mean.** And **the median is unaffected by large changes in extreme observations** — which is exactly the resistance we want.

> [!warning] Three drawbacks, one of them subtle and important
> **1. Computational.** No closed form — the estimates cannot be written down. Historically hard; **now easy even on large data sets.**
>
> **2. All LAD inference is asymptotic.** Under the CLM assumptions, OLS $t$'s are **exact**; LAD statistics are justified only in large samples. **A minor concern in practice** (most LAD applications have hundreds or thousands of observations) — **but a real one at $n=32$, as in Example 9.8.** *In fairness, OLS also needs large-sample approximations whenever any CLM assumption fails.*
>
> **3. LAD does not always consistently estimate the conditional *mean* parameters.** ← **The one that matters.**
> The mean and median coincide only when the distribution of $y$ given $\mathbf{x}$ is **symmetric** about $\beta_0+\beta_1x_1+\cdots+\beta_kx_k$ (equivalently, $u$ is symmetric about zero). **Symmetry is not a Gauss–Markov assumption** — OLS is unbiased and consistent for the conditional mean **whether or not** the errors are symmetric.
>
> **So when LAD and OLS disagree under an asymmetric distribution, the difference may reflect nothing more than the gap between the median and the mean — and have nothing to do with outliers.**
>
> **If $u$ is *independent* of $(x_1,\dots,x_k)$, the slope estimates differ only by sampling error** whether or not $u$ is symmetric (the intercepts differ, since a zero-mean asymmetric $u$ has non-zero median). **But independence is unrealistically strong when LAD is used — it rules out heteroskedasticity, which is exactly what tends to accompany asymmetric distributions.**

> [!tip] The one clear advantage of LAD: monotonic transformations pass through
> **The conditional median passes through increasing functions.** So if
> $$\log(y)=\beta_0+\mathbf{x}\boldsymbol\beta+u,\qquad \mathrm{Med}(u\mid\mathbf{x})=0$$
> then $\mathrm{Med}[\log(y)\mid\mathbf{x}]=\beta_0+\mathbf{x}\boldsymbol\beta$ and therefore
> $$\boxed{\;\mathrm{Med}(y\mid\mathbf{x})=\exp\left(\beta_0+\mathbf{x}\boldsymbol\beta\right)\;}$$
> **$\beta_j$ is the semi-elasticity of the conditional median — recovered from the linear model with no extra assumptions.** No smearing factor, no normality, no independence of $u$ and $\mathbf{x}$.
>
> **Contrast the conditional mean.** A linear model for $\mathbb{E}[\log(y)\mid\mathbf{x}]$ gives **no general way to recover $\mathbb{E}(y\mid\mathbf{x})$.** [[06 - Multiple Regression Analysis - Further Issues|Chapter 06]] §4d needed a full distributional assumption (normality, giving $\exp(\sigma^2/2)$) or Duan's smearing estimate — **and [[08 - Heteroskedasticity|ch. 08]] §4d showed heteroskedasticity makes even that observation-specific.** **The median transforms cleanly; the mean does not.**

> [!warning] "Robust" means two different things — do not confuse them
> | Field | "Robust regression" means |
> |---|---|
> | **Statistics** | Insensitive to **extreme observations** — large residuals get less weight. LAD qualifies. |
> | **Econometrics** | Requires **fewer assumptions**. **By this standard LAD is *not* robust** for the conditional mean — it needs symmetry or independence, **neither of which OLS requires.** |
>
> **LAD is a special case of quantile regression**, which estimates effects at different points of the distribution — e.g. whether pension access affects high-wealth people differently from low-wealth people, and both differently from the median.

---

## ✏️ Exercises

### Exercise 1 — RESET and functional form

A researcher estimates a model with $k=5$ regressors on $n=200$ observations, obtaining $R^2=0.412$. Adding $\hat y^2$ and $\hat y^3$ raises it to $R^2=0.438$.

**(a)** Compute the RESET statistic, its degrees of freedom, and the 5% critical value. What do you conclude?
**(b)** Her colleague says the significant RESET means an important variable was omitted. Evaluate.
**(c)** A second colleague says RESET has detected heteroskedasticity. Evaluate.
**(d)** RESET rejects her level–level model. She proposes a log–log model. Is that the natural next step? What would justify it?
**(e)** She also wants to know whether $x_1$ belongs in levels or logs. Describe **two** ways to test this, and state what each concludes.

> [!example]- Solution
> **(a)** With $k=5$ and two added terms, the expanded equation has $n-k-3=200-8=\mathbf{192}$ degrees of freedom.
> $$F=\frac{(0.438-0.412)/2}{(1-0.438)/192}=\frac{0.013}{0.0029271}=\mathbf{4.44}$$
> $F_{2,192}$ 5% critical value $=\mathbf{3.04}$; $p=\mathbf{0.013}$.
>
> **Reject $H_0:\delta_1=\delta_2=0$ at the 5% level (and at 1.5%). There is evidence of functional form misspecification.**
>
> **(b) He is wrong, and the reason is precise.** **RESET has no power against omitted variables whenever their expectations are linear in the included regressors.** Since that is the standard case, RESET is essentially blind to omitted-variable problems.
>
> **The intuition:** RESET adds $\hat y^2,\hat y^3$ — **nonlinear functions of the *included* regressors.** If an omitted variable's conditional expectation is *linear* in those regressors, it contributes nothing that $\hat y^2$ or $\hat y^3$ can pick up; its effect is already absorbed linearly.
>
> **(c) Also wrong.** **If the functional form is correctly specified, RESET has no power against heteroskedasticity.** RESET is a test about $\mathbb{E}(y\mid\mathbf{x})$; heteroskedasticity is about $\mathrm{Var}(y\mid\mathbf{x})$. Different objects.
>
> **Note the arrow runs only one way, and this is worth getting straight:**
>
> | Test | Can it reject for the *other* reason? |
> |---|---|
> | **RESET** rejecting | **No** — not for omitted variables, not for heteroskedasticity |
> | **Breusch–Pagan / White** rejecting | **Yes** — a misspecified $\mathbb{E}(y\mid\mathbf{x})$ can trigger it ([[08 - Heteroskedasticity|ch. 08]] §3c) |
>
> **Which dictates the order of operations: test functional form first, then heteroskedasticity.** *"RESET is a functional form test, and nothing more."*
>
> **(d) It is *a* reasonable next step, but RESET did not suggest it.**
>
> **RESET's central drawback is that it gives no direction.** Rejecting the level–level model tells you *something* about the conditional mean is wrong — not what. It could be a missing quadratic, a missing interaction, the wrong transformation of $y$, the wrong transformation of an $x$, or several at once.
>
> **What justifies trying logs** is independent of RESET: constant-elasticity models are **easy to interpret**, have **nice statistical properties**, and — per [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a — are indicated whenever the variables are **strictly positive dollar amounts or large counts.**
>
> **Then run RESET on the new model.** In Example 9.2 the levels model gave $p=0.012$ and the log–log gave $p=0.084$ — **it happened to pass.** *There was no guarantee.*
>
> **(e) Two approaches, both for nonnested models with the same dependent variable.**
>
> **1. Mizon–Richard: the comprehensive model.** Nest both inside
> $$y=\gamma_0+\gamma_1x_1+\gamma_2x_2+\gamma_3\log(x_1)+\gamma_4\log(x_2)+u$$
> - $F$ test of $H_0:\gamma_3=\gamma_4=0$ → **a test of the levels model.**
> - $F$ test of $H_0:\gamma_1=\gamma_2=0$ → **a test of the log model.**
>
> Ordinary $F$ tests, since each is a set of exclusion restrictions inside one nesting model.
>
> **2. Davidson–MacKinnon: fitted values from the rival.** To test the **levels** model, estimate the **log** model, save $\check y$, and run
> $$y=\beta_0+\beta_1x_1+\beta_2x_2+\theta_1\check y+\text{error}$$
> **A significant $t$ on $\check y$ (two-sided) rejects the levels model.** Reverse the roles to test the log model.
>
> **The logic is RESET's:** $\check y$ is a nonlinear function of $x_1,x_2$, so it should be irrelevant if the levels model has the right conditional mean.
>
> **What each concludes — and the three ways it can go wrong:**
> - **One rejected, one not** → prefer the survivor.
> - **Neither rejected** → **use $\bar R^2$** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3c), valid here since the dependent variable is the same.
> - **Both rejected** → more work needed; the right form is neither.
>
> **And two cautions.** Rejecting the levels model **does not endorse** the log model — it can be rejected for any functional form error. **And ask the practical question first:** if the key effects are similar under both forms, **it does not matter which you use.**

---

### Exercise 2 — Proxy variables

**(a)** State the two conditions a proxy variable must satisfy, and say which is the demanding one and why.
**(b)** In the `WAGE2` regression, adding IQ moves the return to education from 6.5% to 5.4%. Explain why the direction is exactly what theory predicts.
**(c)** Which parameters does the plug-in regression consistently estimate, and which does it not? Why is this acceptable?
**(d)** Suppose $abil=\delta_0+\delta_1 educ+\delta_2 exper+\delta_3 IQ+v_3$ with $\delta_1>0$ — IQ is an imperfect proxy. Derive $\operatorname{plim}(\hat\beta_{educ})$ and sign the remaining bias. Is including IQ still worthwhile?
**(e)** A colleague objects that adding IQ worsens multicollinearity with $educ$ and inflates $\mathrm{se}(\hat\beta_{educ})$. Give the two-part reply.

> [!example]- Solution
> **(a)** With $y=\beta_0+\beta_1x_1+\beta_2x_2+\beta_3x_3^*+u$ and proxy $x_3$ for $x_3^*$:
>
> **Condition 1.** $u$ is uncorrelated with $x_1$, $x_2$, $x_3^*$ **and with $x_3$**. The first part is MLR.4; the extra part says **$x_3$ is irrelevant once $x_1,x_2,x_3^*$ are included.**
>
> **Condition 2.** $v_3$ is uncorrelated with $x_1,x_2,x_3$ — equivalently
> $$\mathbb{E}(x_3^*\mid x_1,x_2,x_3)=\mathbb{E}(x_3^*\mid x_3)=\delta_0+\delta_3x_3$$
>
> **Condition 2 is the demanding one.** Condition 1 is *"essentially true by definition"* — it is $x_3^*$ that affects $y$, not $x_3$; that is what "proxy" means. **Condition 2 asserts something about the world:** that once you know IQ, education and experience carry **no further information about ability.** In symbols, $\mathbb{E}(abil\mid educ,exper,IQ)=\mathbb{E}(abil\mid IQ)$.
>
> **That is almost certainly not exactly true.** More-educated people may be abler in ways IQ misses. **It may be close enough to be useful — which is (d).**
>
> **(b) Because the naive estimate suffers upward omitted variable bias, and the proxy removes part of it.**
>
> By the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] formula, omitting $abil$ gives
> $$\text{Bias}(\tilde\beta_{educ})=\beta_{abil}\cdot\tilde\delta_{educ}$$
> where $\tilde\delta_{educ}$ is the coefficient from regressing $abil$ on $educ$.
>
> - $\beta_{abil}>0$ — abler people earn more.
> - $\tilde\delta_{educ}>0$ — abler people get more schooling.
>
> **So the bias is positive: $6.5\%$ overstates the causal return.** Adding a proxy for the omitted variable should **pull it down** — and $6.5\%\to5.4\%$ is exactly that.
>
> **Had the estimate gone *up*, something would be wrong** — either the sign reasoning or the proxy.
>
> **(c)** Substituting $x_3^*=\delta_0+\delta_3x_3+v_3$:
> $$y=\underbrace{(\beta_0+\beta_3\delta_0)}_{\alpha_0}+\beta_1x_1+\beta_2x_2+\underbrace{\beta_3\delta_3}_{\alpha_3}x_3+\underbrace{u+\beta_3v_3}_{e}$$
>
> | Parameter | Recovered? |
> |---|---|
> | $\beta_1$, $\beta_2$ | ✅ **Yes** |
> | $\beta_0$ | ❌ — you get $\alpha_0=\beta_0+\beta_3\delta_0$ |
> | $\beta_3$ | ❌ — you get $\alpha_3=\beta_3\delta_3$ |
>
> **Acceptable for three reasons:**
> 1. **$\beta_1$ and $\beta_2$ are what we wanted** — the return to education and experience.
> 2. **We could not interpret $\beta_3$ anyway.** *"Ability is at best a vague concept"* — what is "one more unit" of it?
> 3. **$\alpha_3$ is the more useful quantity.** It is **the return to one more IQ point** — measurable, and directly interpretable. From Table 9.2, $\hat\alpha_3=0.0036$: ten IQ points are worth 3.6%, and one standard deviation (15 points) is worth $15(0.0036)=\mathbf{5.4\%}$ — **exactly the value of one more year of schooling.**
>
> **(d)** Substituting the richer equation into the model:
> $$y=(\beta_0+\beta_3\delta_0)+(\beta_1+\beta_3\delta_1)educ+(\beta_2+\beta_3\delta_2)exper+\beta_3\delta_3 IQ+(u+\beta_3v_3)$$
>
> Since $u+\beta_3v_3$ has zero mean and is uncorrelated with $educ$, $exper$ and $IQ$,
> $$\boxed{\operatorname{plim}(\hat\beta_{educ})=\beta_{educ}+\beta_3\delta_1}$$
>
> **Signing it:** $\beta_3>0$ (ability raises wages) and $\delta_1>0$ (ability retains a positive partial correlation with education even given IQ). **So the bias is positive — the return to education is still overstated.**
>
> **Yes, it is still worthwhile.** The bias fell from $\beta_3\tilde\delta_{educ}$ (the raw ability–education relationship) to $\beta_3\delta_1$ (the relationship **after partialling out IQ**), and $\delta_1<\tilde\delta_{educ}$ whenever IQ captures any of the ability–education link.
>
> **The empirical signature is visible in the table:** $6.5\%\to5.4\%$ is the part of the bias IQ removed. Whatever remains, **we have reasonable grounds to hope it is smaller than if we had ignored ability entirely.**
>
> > **Note what this is *not*.** It is not a proof that $5.4\%$ is unbiased. **A proxy reduces bias; it does not certify the result.** For a consistent estimate under general failure you need instrumental variables (Wooldridge ch. 15).
>
> **(e) The objection is factually right about the collinearity and wrong about what follows.**
>
> **Reply part 1: adding IQ also *reduces* the error variance.** The part of ability explained by IQ is taken **out of $u$**, so $\sigma^2$ falls — typically visible as a smaller SER. In the variance formula
> $$\mathrm{Var}(\hat\beta_{educ})=\frac{\sigma^2}{\text{SST}_{educ}(1-R^2_{educ})}$$
> **the numerator falls while the denominator falls. The net effect is ambiguous, not automatically adverse.** (This is [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3e in reverse: there, the added variable was uncorrelated and gave a free precision gain; here it is correlated, so the two effects fight.)
>
> **In Table 9.2 the standard error rises only from $0.006$ to $0.007$ — a trivially small price.**
>
> **Reply part 2, and this is the decisive one: the multicollinearity is a *necessary evil*.**
>
> **Why are $educ$ and $IQ$ correlated? Because $educ$ and $abil$ are correlated — which is the entire reason we have a problem.** If ability were observable we would include it directly, **and exactly the same collinearity would appear.**
>
> **You cannot remove omitted variable bias without confronting the correlation that produced it.** Demanding an unbiased estimate *and* the precision of the biased one is demanding something that does not exist. **This is the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] bias–variance trade-off, and here the trade is plainly worth making:** roughly a 17% increase in the standard error buys the removal of a bias worth 1.1 percentage points on a 6.5% coefficient.

---

### Exercise 3 — Measurement error and attenuation

**(a)** State the effect of measurement error in the **dependent** variable when the error is independent of the regressors. When does it become harmful?
**(b)** Distinguish the two polar assumptions about measurement error in a regressor, and say which one causes trouble.
**(c)** Derive the attenuation formula for simple regression. Suppose $\beta_1=0.10$, $\mathrm{Var}(x_1^*)=36$ and $\mathrm{Var}(e_1)=9$. Compute $\operatorname{plim}(\hat\beta_1)$. Repeat with $\mathrm{Var}(e_1)=36$ and $\mathrm{Var}(e_1)=4$.
**(d)** Now add two correctly measured regressors, and suppose the $R^2$ from regressing $x_1^*$ on them is $0.60$. Recompute the attenuation factor with $\mathrm{Var}(e_1)=9$. What general lesson follows?
**(e)** Give one example where CEV clearly fails, and explain what a researcher should do about measurement error that satisfies neither polar assumption.

> [!example]- Solution
> **(a)** With $y^*=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$ and $e_0=y-y^*$:
> $$y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+(u+e_0)$$
>
> **If $e_0$ is independent of every $x_j$, OLS is unbiased and consistent, and $t$, $F$ and LM are all valid.** A non-zero mean for $e_0$ biases only the **intercept** — rarely a concern.
>
> **The only cost is precision:** if $e_0$ and $u$ are uncorrelated, $\mathrm{Var}(u+e_0)=\sigma_u^2+\sigma_0^2>\sigma_u^2$, so all standard errors are larger. **Nothing can be done except collect better data.**
>
> **It becomes harmful when $e_0$ is systematically related to a regressor.** Example 9.6 is the sharp case: if firms receiving a training grant **under-report their scrap rate to make the grant look effective**, then $u+e_0$ is **negatively correlated with $grant$**, biasing $\hat\beta_1$ downward — i.e. **making the programme look more effective than it was.** *Wherever there is an incentive to misreport, expect exactly this.*
>
> **(b)** With $x_1=x_1^*+e_1$:
>
> | | Assumption | Consequence |
> |---|---|---|
> | **Case 1** | $\mathrm{Cov}(x_1,e_1)=0$ — error uncorrelated with the **observed** measure | ✅ **OLS consistent.** Error variance rises to $\sigma_u^2+\beta_1^2\sigma_{e_1}^2$; nothing else changes |
> | **Case 2 (CEV)** | $\mathrm{Cov}(x_1^*,e_1)=0$ — error uncorrelated with the **true** value | ❌ **OLS biased and inconsistent** |
>
> **CEV is the troublesome one — and the one econometricians mean.** Case 1 is the proxy-variable assumption in disguise, which is precisely why it causes no problems.
>
> **The two cannot both hold** (unless $\sigma_{e_1}^2=0$): from $x_1=x_1^*+e_1$, assuming one forces a correlation in the other. **Under CEV:**
> $$\mathrm{Cov}(x_1,e_1)=\mathbb{E}(x_1^*e_1)+\mathbb{E}(e_1^2)=0+\sigma_{e_1}^2=\sigma_{e_1}^2\ne0$$
>
> **(c) Derivation.** Write $x_1^*=x_1-e_1$ and substitute:
> $$y=\beta_0+\beta_1x_1+(u-\beta_1e_1)$$
> Since $u$ is uncorrelated with $x_1$,
> $$\mathrm{Cov}(x_1,\,u-\beta_1e_1)=-\beta_1\mathrm{Cov}(x_1,e_1)=-\beta_1\sigma_{e_1}^2$$
> and $\mathrm{Var}(x_1)=\sigma_{x_1^*}^2+\sigma_{e_1}^2$ (the two components being uncorrelated). Hence
> $$\operatorname{plim}(\hat\beta_1)=\beta_1+\frac{-\beta_1\sigma_{e_1}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}=\beta_1\left(1-\frac{\sigma_{e_1}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}\right)=\boxed{\beta_1\left(\frac{\sigma_{x_1^*}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}\right)}$$
>
> **The multiplier — the reliability ratio — is strictly between 0 and 1, so $\operatorname{plim}(\hat\beta_1)$ is always closer to zero than $\beta_1$.**
>
> | $\mathrm{Var}(e_1)$ | Reliability ratio | $\operatorname{plim}(\hat\beta_1)$ | Understatement |
> |---|---|---|---|
> | $4$ | $36/40=\mathbf{0.90}$ | $\mathbf{0.090}$ | 10% |
> | $9$ | $36/45=\mathbf{0.80}$ | $\mathbf{0.080}$ | 20% |
> | $36$ | $36/72=\mathbf{0.50}$ | $\mathbf{0.050}$ | **50%** |
>
> **The damage is governed entirely by the signal-to-noise ratio $\sigma_{x_1^*}^2/\sigma_{e_1}^2$.** When the true variable varies a great deal relative to the noise, **measurement error need not cause large biases** — the third row is the alarming one, where the noise variance equals the signal variance and half the effect vanishes.
>
> **(d)** The formula becomes
> $$\operatorname{plim}(\hat\beta_1)=\beta_1\left(\frac{\sigma_{r_1^*}^2}{\sigma_{r_1^*}^2+\sigma_{e_1}^2}\right)$$
> where $r_1^*$ is $x_1^*$ **after partialling out the other regressors**. With $R^2_1=0.60$:
> $$\sigma_{r_1^*}^2=36(1-0.60)=\mathbf{14.4}$$
> $$\text{factor}=\frac{14.4}{14.4+9}=\mathbf{0.615}\qquad\Longrightarrow\qquad\operatorname{plim}(\hat\beta_1)=\mathbf{0.0615}$$
>
> **The attenuation worsened from 20% to 38.5%, with no change in the measurement error at all.**
>
> > **The general lesson: attenuation bias gets worse the more collinear the mismeasured variable is with the other regressors.**
> >
> > **Why:** partialling out can only *reduce* the variation in $x_1^*$ ($\sigma_{r_1^*}^2\le\sigma_{x_1^*}^2$), while the measurement error variance $\sigma_{e_1}^2$ is **untouched**. The signal shrinks; the noise does not. **In the limit, as $x_1^*$ becomes nearly collinear with the controls, the reliability ratio $\to0$ and the estimated effect vanishes entirely.**
> >
> > **This is the same partialled-out variation that sits in the denominator of the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] variance formula** — collinearity hurts twice over: it inflates the standard error **and** deepens the attenuation.
>
> **And a further consequence:** under CEV, **all** the coefficients are inconsistent, not only $\hat\beta_1$. The biases on the correctly measured variables *"are not easily derived"* in size or even direction. They are consistent only in the rare case that $x_1^*$ is uncorrelated with the other regressors — **which is exactly the case where $R^2_1=0$ and the attenuation on $\hat\beta_1$ is at its mildest.**
>
> **(e) A clear failure of CEV:** $smoked^*$ = actual number of occasions a student smoked marijuana in the last 30 days, with $smoked$ the self-reported answer.
>
> **Students who never smoke ($smoked^*=0$) report 0 — their measurement error is exactly zero.** Students with $smoked^*>0$ are far more likely to miscount. **So $e_1$ is systematically related to $smoked^*$, and $\mathrm{Cov}(x_1^*,e_1)\ne0$.** CEV fails by construction.
>
> **The same structure appears whenever the variable has a natural floor at zero** — hours of training, charitable donations, doctor visits.
>
> **What to do about error satisfying neither assumption:**
> 1. **Acknowledge it.** *"The truth is probably somewhere in between, and if $e_1$ is correlated with both $x_1^*$ and $x_1$, OLS is inconsistent"* — with **no clean formula** for the direction or size.
> 2. **You do not have to accept it. Use instrumental variables** (Wooldridge ch. 15), which consistently estimate the parameters under general measurement error — **but that means leaving OLS.**
> 3. **Multiple measures help.** A second, independently-collected measure of the same variable can be used to reduce the attenuation. (In `WAGE2`, this is the logic behind having both IQ and KWW — though there the setting is proxy variables, not measurement error.)
> 4. **At minimum, know the direction if CEV is approximately right:** attenuation means a test of $H_0:\beta_1=0$ has **reduced power.** *A failure to reject is weak evidence of no effect when the regressor is badly measured.*

---

### Exercise 4 — Missing data and nonrandom samples

**(a)** Define MCAR and MAR, and explain why the names are misleading.
**(b)** A researcher with $n=1{,}000$ finds $x_k$ missing for 30% of cases. He proposes the missing indicator method to keep all 1,000. Evaluate against the complete cases estimator.
**(c)** Classify each of the following as exogenous or endogenous selection, and state the effect on OLS: (i) a saving survey of people over 35; (ii) a wealth survey restricted to people with wealth below \$250,000; (iii) a military pay survey that oversamples women; (iv) a military pay survey that oversamples low-paid personnel.
**(d)** `WAGE1` is a random sample of **working** individuals, used to estimate a **wage offer** equation. Is this exogenous or endogenous selection? Justify carefully.
**(e)** Why is multicollinearity not in this section?

> [!example]- Solution
> **(a)**
>
> | | Requires missingness be unrelated to… |
> |---|---|
> | **MCAR** (missing completely at random) | **$(x_1,\dots,x_k)$ *and* $u$** |
> | **MAR** (missing at random) | **$u$ only** — it **may** depend on $(x_1,\dots,x_k)$ |
>
> **MAR is the weaker condition.** In regression terms, MAR is exactly **exogenous sample selection**.
>
> **Why the names mislead:** *"random"* sounds like it should mean *"unrelated to anything,"* which would make MAR the stronger condition. **It is the reverse — "completely at random" is the strong one, and plain "at random" permits systematic dependence on the regressors.** Wooldridge calls MAR *"not a particularly good label."* **Read the definitions, not the names.**
>
> **(b) The gain is largely illusory, and MIM is the *less* robust choice.**
>
> **The method:** define $Z_{ik}=x_{ik}$ when observed and $0$ otherwise, and $m_{ik}=1$ when missing; regress $y_i$ on $x_{i1},\dots,x_{i,k-1},Z_{ik},m_{ik}$ using all 1,000.
>
> **The appeal is obvious: 1,000 observations instead of 700.**
>
> **The problem is the assumptions.** MIM requires **MCAR *plus*, essentially, that $x_k$ be uncorrelated with $x_1,\dots,x_{k-1}$** (Jones 1996; Abrevaya & Donald 2018). **That second condition is severe and rarely plausible** — regressors in economics are routinely correlated.
>
> **The comparison, which runs the opposite way to intuition:**
>
> | | Complete cases | MIM |
> |---|---|---|
> | Observations used | 700 | 1,000 |
> | Needs MCAR? | **No** — consistent even when missingness depends on $(x_1,\dots,x_k)$ | **Yes** |
> | Restricts correlations among regressors? | **No** | **Yes** — needs $x_k$ uncorrelated with the others |
>
> **The default that packages compute automatically is the more robust estimator.** And there is no way to know in general whether MIM's bias is practically important.
>
> **One thing is certain:** omitting $m_{ik}$ from the regression is a **very poor idea** — it is identical to setting $x_{ik}=0$ whenever it is missing, which asserts something false about 300 observations.
>
> **Recommendation: use complete cases, and report how many observations were lost.** More sophisticated fill-in methods exist (Little & Rubin 2002; Abrevaya & Donald 2018) but are beyond this text.
>
> **(c)**
>
> | Case | Selection based on | Type | Effect on OLS |
> |---|---|---|---|
> | (i) Saving survey, **age > 35** | $age$ — a **regressor** | **Exogenous** | ✅ **Unbiased and consistent** |
> | (ii) Wealth survey, **wealth < \$250k** | **The dependent variable** | **Endogenous** | ❌ **Biased and inconsistent** |
> | (iii) Military pay, **oversample women** | $female$ — a **regressor** | **Exogenous** | ✅ **Unbiased and consistent** |
> | (iv) Military pay, **oversample low-paid** | **The dependent variable** | **Endogenous** | ❌ **Biased and inconsistent** |
>
> **Why (i) works:** $\mathbb{E}(saving\mid income,age,size)$ is **the same function for any subpopulation defined by $income$, $age$ or $size$.** Restricting to $age>35$ selects a slice of the population but does not change the conditional mean being estimated. **The only cost is a smaller $n$ — provided there is still enough variation in the regressors within the subpopulation.**
>
> **Why (ii) fails:**
> $$\mathbb{E}(wealth\mid educ,exper,age)\;\ne\;\mathbb{E}(wealth\mid educ,exper,age,\;wealth<250{,}000)$$
> **Conditioning on the outcome changes the conditional mean.** Given education and experience, you have systematically excluded the people with large positive errors — so $\mathbb{E}(u\mid\mathbf{x},\text{selected})\ne0$, and MLR.4 fails in the selected sample.
>
> **(iii) vs (iv)** is the same distinction applied to stratified sampling. Oversampling a small group is common and perfectly fine **provided the stratification variable is a regressor.** In (iii) we can still estimate the gender differential and the returns to education and experience for all personnel — assuming those returns are not gender-specific, or that we include the interactions of [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §4b.
>
> **(d) Not clear-cut — and that is the honest answer.**
>
> **The equation describes all working-age people:**
> $$\log(wage^o)=\beta_0+\beta_1 educ+\beta_2 exper+u$$
> **Every working-age person faces an hourly wage offer** and chooses whether to work at it. For workers, the offer **is** the observed wage; **for non-workers it is unobserved** — although $educ$ and $exper$ can still be collected.
>
> **The argument for exogenous:** selection is on **the decision to work**, not directly on the size of the wage offer. This is unlike case (ii), where a fixed threshold on the dependent variable was applied.
>
> **The argument for endogenous — and it is the stronger one:** **the decision to work is very likely related to unobserved factors that also affect the wage offer.** Someone with high unobserved productivity faces a high offer *and* is more likely to accept it. If so, the selected sample over-represents people with large positive $u$, conditional on $educ$ and $exper$ — **which is endogenous selection, and OLS suffers sample selection bias.**
>
> **The verdict:** *"selection might be endogenous, and this can result in a sample selection bias."* **Testing and correcting for it requires Wooldridge ch. 17.**
>
> > **A neat closing of the loop:** the participation decision that creates this problem is exactly the `MROZ` labour-force-participation equation of [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §5. **Modelling selection *is* modelling that binary outcome** — which is why Heckman's correction begins with a probit for participation.
>
> **(e) Because correlation among the regressors violates no assumption at all.**
>
> **MLR.3 rules out only *perfect* collinearity.** Anything short of that is legal, and OLS remains unbiased, consistent and BLUE.
>
> **High correlation makes individual partial effects hard to estimate precisely — and the usual OLS statistics say so, honestly**, through the $1/(1-R_j^2)$ term in $\mathrm{Var}(\hat\beta_j)$ and hence through inflated standard errors and wide confidence intervals. **Nothing is hidden and nothing is biased.**
>
> **Contrast every genuine problem in this section:** missing data, nonrandom sampling and measurement error can all **break MLR.2 or MLR.4** and produce estimates that are systematically wrong **while the reported standard errors look fine.** *That* is what makes them data problems. **Multicollinearity is a precision issue that the output reports for you.**

---

### Exercise 5 — Outliers, studentized residuals, and LAD

From `RDCHEM` ($n=32$ chemical firms), regressing $rdintens$ on $sales$ and $profmarg$:

| Sample | $\hat\beta_{sales}$ | se | $R^2$ |
|---|---|---|---|
| All 32 | $0.000053$ | $0.000044$ | $0.0761$ |
| Drop the largest firm (#10) | $0.000186$ | $0.000084$ | $0.1728$ |

Also: $\hat\sigma=1.82$ with all 32; the residual for firm #10 is $-1.62$; a dummy for #10 has coefficient $-6.57$ and $t=-1.82$; a dummy for #1 has coefficient $+6.72$ and $t=+4.56$.

**(a)** Compute both $t$ statistics for $\hat\beta_{sales}$ and describe what dropping one observation did.
**(b)** Explain why firm #10's own OLS residual ($-1.62$) fails to flag it, and describe the dummy-variable trick for computing a studentized residual.
**(c)** By studentized residual, #1 looks like a worse outlier than #10 ($4.56$ vs $-1.82$) — yet dropping #1 barely changes $\hat\beta_{sales}$. Reconcile, and say what this shows about outlier diagnostics.
**(d)** Re-specifying in logs gives $\hat\beta_{\log(sales)}=1.084$ (se $0.060$) with all 32, and $1.088$ (se $0.067$) without #10. Test $H_0:\beta_1=1$ against $\beta_1>1$ in both. Why is the log model preferable here, and why can you **not** cite the rise in $R^2$ from $0.076$ to $0.918$ as evidence?
**(e)** Would LAD be a good alternative for this data set? Give the case for and against.

> [!example]- Solution
> **(a)**
> $$t_{\text{all 32}}=\frac{0.000053}{0.000044}=\mathbf{1.20}\qquad t_{\text{drop \#10}}=\frac{0.000186}{0.000084}=\mathbf{2.21}$$
>
> **Dropping one observation out of 32 changed the substantive conclusion completely.** The coefficient **more than tripled** ($0.000186/0.000053=3.5$), $R^2$ more than doubled ($0.076\to0.173$), and the effect went from **insignificant at 10%** to **significant at 5%**.
>
> **From the full sample you would conclude R&D intensity is unrelated to firm size. From the 31 smaller firms you would conclude there is a significant positive relationship.**
>
> **The mechanism:** 31 firms have sales under \$20 billion; one has almost \$40 billion — **over twice the size of every other firm.** With enormous leverage on the far right, that single point pulls the fitted line flat.
>
> **(b) Because OLS *adjusted itself* to accommodate the observation.**
>
> $$\frac{-1.62}{1.82}=-0.89$$
>
> **Less than one estimated standard deviation from the mean residual (which is zero by construction).** Nothing about it looks unusual.
>
> **The reason is circular and important: OLS minimizes the sum of squared residuals, so it *tilts the line toward* any high-leverage point.** By flattening the line to reach firm #10, OLS made #10's residual small. **The observation that distorted the entire regression is invisible by its own residual.**
>
> > **General rule: never define outliers by the size of the OLS residual from the full-sample regression.** The estimator has already conspired to hide them.
>
> **The dummy-variable trick.** To studentize observation $h$:
> 1. **Define a dummy equal to 1 for observation $h$ and 0 for all others.**
> 2. **Include it in the regression using all $n$ observations.**
>
> Then:
> - **The dummy's coefficient is the residual for observation $h$ from the regression line fitted using only the *other* observations** — i.e. a genuine out-of-sample residual.
> - **The $t$ statistic on the dummy *is* the studentized residual**, distributed $t_{n-k-2}$ under the CLM assumptions.
>
> **For firm #10 the dummy coefficient is $-6.57$** — against an ordinary residual of $-1.62$. **The observation is four times further from the line that the other 31 firms determine than its own residual suggested.**
>
> **Same device as [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4a's recentring:** make the quantity you want into a coefficient, and the package computes its standard error correctly for free.
>
> **(c) Both facts are true, and together they show that "outlier" and "influential" are different things.**
>
> | | Studentized residual | Effect of dropping it on $\hat\beta_{sales}$ |
> |---|---|---|
> | **#1** (highest $rdintens\approx9.42$) | $\mathbf{+4.56}$ — far larger | $0.000053\to0.000051$ — **negligible** |
> | **#10** (largest firm) | $-1.82$ ($p=0.08$) — marginal | $0.000053\to0.000186$ — **triples** |
>
> **Two reasons for the mismatch.**
>
> **1. Leverage, not residual size, drives influence.** #10 is extreme in **$sales$** — the regressor — so it sits at the far end of the $x$-axis where a single point exerts enormous pull on the slope. #1 is extreme in **$rdintens$** — the outcome — near the middle of the $sales$ range, where it mostly shifts the intercept. **A point can be far from the line without moving the slope.**
>
> **2. There is circularity in the diagnostic itself.** When computing #1's studentized residual, **#10 is still in the sample fitting the line.** *"Given how flat the regression line is with the largest firm included, it is not too surprising that the first observation, with its high value of $rdintens$, is far off."* **#10's influence is what made #1 look like an outlier.**
>
> **Dropping both** (two dummies, effectively $n=30$) gives $\hat\beta_{sales}=0.000160$ ($t=2.46$) and $\hat\beta_{profmarg}=0.0701$ ($t=2.04$, $p=0.051$) — **both significant.** Dummy coefficients $+6.47$ ($t=4.58$) and $-5.41$ ($t=-1.95$).
>
> **And even then, two observations still have studentized residuals above 2.** *There is no natural stopping point.*
>
> > **What this shows:** *"the size of the studentized residual need not correspond to how influential an observation is for the OLS slope estimates, and certainly not for all of them at once."* **Formal leverage measures (Belsley, Kuh & Welsch 1980) address this, but need matrix algebra.**
> >
> > **The practical discipline stands regardless: report the results with and without the suspect observations, and let the reader see the sensitivity.**
>
> **(d)** Testing $H_0:\beta_1=1$ against $H_1:\beta_1>1$ — R&D intensity rises with size **iff $\beta_1>1$**, from $rd=sales^{\beta_1}\exp(\beta_0+\beta_2 profmarg+u)$.
>
> $$t_{\text{all 32}}=\frac{1.084-1}{0.060}=\mathbf{1.40}\qquad t_{\text{drop \#10}}=\frac{1.088-1}{0.067}=\mathbf{1.31}$$
>
> **One-sided 5% critical value $\approx1.70$ ($t_{29}$). Do not reject in either case.** **R&D expenditure is approximately proportional to sales — R&D *intensity* does not rise with firm size.**
>
> **Note the trap in the test itself: $H_0$ is $\beta_1=1$, not $\beta_1=0$.** The printed $t$ statistic (over 18) tests the wrong hypothesis entirely.
>
> **Why the log model is preferable:** **the outlier problem simply vanishes.** The two estimates ($1.084$ and $1.088$) are practically identical, and so are the standard errors. As [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a promised, logs **narrow the range** of economic variables — a firm twice as large as the rest in levels is only $\log 2\approx0.69$ further along in logs — and yield **constant-elasticity forms that fit a broader range of data.**
>
> **A change of functional form did what deleting observations was trying to do, without deleting anything.**
>
> > **Why the $R^2$ comparison is illegitimate:** $0.076$ explains variation in **$rdintens$**; $0.918$ explains variation in **$\log(rd)$**. **Different dependent variables, different total variation.** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3c — the same error as comparing a levels and a log model by $R^2$.) **To compare them you would need the retransformation measure of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4d.**
>
> **(e) On balance, no — not for this data set, though the idea is right.**
>
> **The case for LAD.** It minimizes $\sum_i|y_i-b_0-b_1x_{i1}-\cdots|$, which is **linear on either side of zero** rather than quadratic. **A residual one unit larger raises the objective by one unit, not by an ever-increasing amount.** Since LAD estimates the conditional **median**, and the median is unaffected by large changes in extreme observations, **LAD estimates are far more resilient to points like firm #10 or D.C. in Example 9.10.** It is precisely the tool this section motivates.
>
> **The case against, here.**
>
> 1. **$n=32$ is far too small.** **All LAD inference is asymptotic** — there are no exact distributions. *"We might be pushing it if we apply large-sample approximations in an example such as Example 9.8, with $n=32$."* Most LAD applications have hundreds or thousands of observations.
> 2. **LAD estimates the median, not the mean** — and firm sizes and R&D spending are **strongly right-skewed**, so the two differ substantially. **Any gap between the LAD and OLS estimates would be uninterpretable:** is it the outlier being downweighted, or just the median–mean difference? **You could not tell.** (LAD and OLS slopes agree up to sampling error only if $u$ is **independent** of the regressors — which rules out heteroskedasticity, exactly what accompanies skewed data.)
> 3. **A better fix is already available and works.** The log specification of (d) **eliminates the outlier's influence entirely** while keeping OLS's exact inference, its unbiasedness for the conditional mean with no symmetry assumption, and an interpretable constant-elasticity parameter.
>
> > **And note the terminological trap.** In **statistics**, "robust regression" means insensitive to extreme observations — **LAD qualifies.** In **econometrics**, "robust" means requiring **fewer** assumptions — **and by that standard LAD is *not* robust for the conditional mean**, since it needs symmetry or independence, **neither of which OLS requires.**
> >
> > **Where LAD genuinely wins:** monotonic transformations pass through the median, so $\mathrm{Med}[\log(y)\mid\mathbf{x}]=\beta_0+\mathbf{x}\boldsymbol\beta$ gives $\mathrm{Med}(y\mid\mathbf{x})=\exp(\beta_0+\mathbf{x}\boldsymbol\beta)$ **directly, for any error distribution.** The conditional mean offers nothing comparable — [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4d needed normality or Duan's smearing estimate, and [[08 - Heteroskedasticity|ch. 08]] §4d showed heteroskedasticity makes even that observation-specific.
> >
> > **LAD is a special case of quantile regression** — worth knowing for when the effect differs across the distribution, not just at its centre.

---

## 📝 Summary

- **Functional form misspecification is omitted variable bias where the omitted variable is a *function* of an included one.** It causes bias in every coefficient — but it is the least bad endogeneity problem, because **you already have all the data you need.** Fix it by adding quadratics and interactions and running a joint $F$ test.
- **RESET** adds $\hat y^2$ and $\hat y^3$ to the equation and tests $H_0:\delta_1=\delta_2=0$ with $F_{2,\,n-k-3}$. **It gives no direction if it rejects, and it is a functional form test and nothing more**: it has **no power** against omitted variables whose expectations are linear in the included regressors, and **none** against heteroskedasticity when the form is right.
- **Nonnested models** are compared by nesting them in a **comprehensive model** (Mizon–Richard) or by adding the rival's **fitted values** and testing their $t$ statistic (Davidson–MacKinnon). Neither, both, or one model may be rejected; if neither, use $\bar R^2$. **Rejecting one does not endorse the other.**
- **A proxy variable** replaces an unobservable via $x_3^*=\delta_0+\delta_3x_3+v_3$. It works if $u$ is uncorrelated with everything **and** $\mathbb{E}(x_3^*\mid x_1,x_2,x_3)=\mathbb{E}(x_3^*\mid x_3)$ — **the demanding condition.** You recover $\beta_1,\beta_2$ but not $\beta_0$ or $\beta_3$; you get $\alpha_3=\beta_3\delta_3$ instead, **which is usually more interesting** (the return to an IQ point rather than to a unit of "ability").
- **If the proxy is imperfect**, $\operatorname{plim}(\hat\beta_1)=\beta_1+\beta_3\delta_1$ — bias remains, **but is generally smaller than ignoring the problem.** The collinearity it introduces is a **necessary evil**: $educ$ and $IQ$ are correlated *because* $educ$ and $abil$ are, which is the entire problem.
- **A lagged dependent variable** proxies for unobserved historical factors when you cannot name what to proxy for. Adding $\log(crmrte82)$ flipped the law-enforcement elasticity from $+0.203$ to $-0.140$.
- **Random slope models** $y_i=a_i+b_ix_i$ are consistently estimated by OLS for the **average partial effect** provided $a_i$ and $b_i$ are **mean independent** of $x_i$ — but the error is then automatically heteroskedastic, $\mathrm{Var}(u_i\mid x_i)=\sigma_c^2+\sigma_d^2x_i^2$.
- **Measurement error in $y$ is harmless** if independent of the regressors — only the error variance (hence the standard errors) grows. **It becomes harmful when there is an incentive to misreport** that correlates with a regressor.
- **Measurement error in a regressor** depends entirely on which polar assumption holds. **Case 1** ($\mathrm{Cov}(x_1,e_1)=0$): OLS consistent. **CEV** ($\mathrm{Cov}(x_1^*,e_1)=0$): $$\operatorname{plim}(\hat\beta_1)=\beta_1\left(\frac{\sigma_{x_1^*}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}\right)$$ — **attenuation bias**, always toward zero. **With other regressors, $\sigma_{x_1^*}^2$ is replaced by the *partialled-out* variance, so attenuation gets worse the more collinear the mismeasured variable is.** All coefficients become inconsistent, with signs that cannot generally be determined.
- **MCAR** (missingness unrelated to the $x_j$ *and* $u$) makes missing data harmless. The **missing indicator method** needs MCAR **plus** $x_k$ uncorrelated with the other regressors — **so the naive complete cases estimator is the more robust one.**
- **Selection on the explanatory variables (exogenous / MAR) leaves OLS unbiased; selection on the dependent variable (endogenous) always biases it.** Stratified sampling follows the same rule. **`WAGE1` is a sample of workers used for a wage-offer equation — the intermediate, unresolved case.**
- **Outliers are dangerous because OLS minimizes *squared* residuals**, so extreme points get enormous weight — and **OLS then tilts toward them, hiding them from their own residuals.** Studentized residuals (obtained as the $t$ on an observation-specific dummy) help but **do not measure influence**: in `RDCHEM`, #1 has the larger studentized residual while #10 has all the influence. **Report results with and without.** Logs often dissolve the problem entirely.
- **LAD** minimizes $\sum|\hat u_i|$ and estimates the **conditional median**, making it resistant to outliers, and **monotonic transformations pass through the median** so $\mathrm{Med}(y\mid\mathbf{x})=\exp(\beta_0+\mathbf{x}\boldsymbol\beta)$ follows directly. **But it estimates the mean only under symmetry or independence — assumptions OLS does not need — and all its inference is asymptotic.**

---

## ⚠️ Important Notes

> [!warning] The twelve mistakes this chapter is designed to prevent
>
> 1. **Treating a significant RESET as evidence of omitted variables or heteroskedasticity.** It has **no power** against either. RESET is a functional form test, full stop.
> 2. **Expecting RESET to tell you what to do next.** It never does. The log model in Example 9.2 was tried for independent reasons and **happened** to pass.
> 3. **Using an $F$ test to choose between nonnested models.** Nest them first (Mizon–Richard) or use Davidson–MacKinnon.
> 4. **Believing rejecting model A endorses model B.** A can be rejected for any functional form error.
> 5. **Expecting a proxy variable to deliver $\beta_3$.** You get $\alpha_3=\beta_3\delta_3$ and $\alpha_0=\beta_0+\beta_3\delta_0$ — **and $\beta_1,\beta_2$, which is the point.**
> 6. **Objecting to a proxy on multicollinearity grounds.** The collinearity **is** the problem you are solving; it would be there if you could observe the true variable. Adding the proxy also **cuts the error variance.**
> 7. **Assuming measurement error in $y$ is always benign.** It is benign only if uncorrelated with the regressors. **Incentive to misreport (the scrap-rate grant case) destroys that** and biases the treatment effect in the flattering direction.
> 8. **Forgetting that attenuation worsens with more regressors.** The reliability ratio uses the **partialled-out** variance $\sigma_{r_1^*}^2$, not $\sigma_{x_1^*}^2$ — collinearity hurts twice.
> 9. **Assuming only the mismeasured coefficient is affected.** Under CEV **every** coefficient is inconsistent, with directions that cannot generally be signed.
> 10. **Preferring the missing indicator method because it "uses more data."** It needs MCAR **plus** an implausible no-correlation condition. **Complete cases is more robust.** And never include $Z_{ik}$ without $m_{ik}$.
> 11. **Identifying outliers by the size of the OLS residual.** Firm #10 had residual $-1.62$ against $\hat\sigma=1.82$ — **and tripled the key coefficient when dropped.** OLS tilts toward high-leverage points and thereby conceals them.
> 12. **Equating a large studentized residual with influence.** #1 had $t=4.56$ and changed nothing; #10 had $t=-1.82$ and changed everything.

> [!important] The four ideas most likely to be examined
>
> **1. RESET: construction, distribution, and its two blind spots.** Add $\hat y^2,\hat y^3$; $F_{2,\,n-k-3}$; **no power against omitted variables linear in the included regressors, none against heteroskedasticity.** And know the asymmetry with [[08 - Heteroskedasticity|ch. 08]] §3c: a heteroskedasticity test **can** reject for functional form reasons, **so test functional form first.**
>
> **2. The proxy variable conditions and the plug-in algebra.** Substitute (9.11) into (9.10) in one line and read off $\alpha_0$, $\alpha_3$, and the composite error $e=u+\beta_3v_3$. Then state which parameters survive. **And be able to derive $\operatorname{plim}(\hat\beta_1)=\beta_1+\beta_3\delta_1$ when the proxy is imperfect, and sign it.**
>
> **3. Attenuation bias, derived.** From $y=\beta_0+\beta_1x_1+(u-\beta_1e_1)$ and $\mathrm{Cov}(x_1,e_1)=\sigma_{e_1}^2$ under CEV, get $$\operatorname{plim}(\hat\beta_1)=\beta_1\frac{\sigma_{x_1^*}^2}{\sigma_{x_1^*}^2+\sigma_{e_1}^2}$$ **Know that the multiplier is the reliability ratio, that it is always in $(0,1)$, and that with more regressors the numerator becomes the partialled-out variance.**
>
> **4. Exogenous versus endogenous sample selection.** **Selection on the $x_j$ is fine; selection on $y$ is fatal.** Be able to apply it to age restrictions, wealth thresholds, and both directions of stratified sampling — and to explain why `WAGE1` is the genuinely ambiguous case.

> [!note] Cross-subject connections
> - **Measurement error is a data-quality problem**, which is where [[Data Preparation and Visualization/contents/00-Index|Data Preparation & Visualization]] lives. The econometric contribution is that **it tells you the *direction* of the damage**: CEV always attenuates. **In [[Machine Learning/contents/00-Index|ML]] this appears as label noise (harmless if random, like error in $y$) versus feature noise (attenuating, like error in $x$)** — and it explains why noisy features get systematically underweighted by a fitted model.
> - **Missing data: MCAR / MAR / MNAR is the standard imputation taxonomy** used across [[Data Preparation and Visualization/contents/00-Index|DPV]] and [[MLOps/contents/00-Index|MLOps]]. **The econometric result here is a corrective to common practice:** the missing indicator method is *less* robust than dropping rows, which is the opposite of the usual intuition.
> - **Sample selection bias is the same problem as *training–serving skew* and *survivorship bias*** in [[MLOps/contents/00-Index|MLOps]]. **Selection on the label is the fatal case in both fields** — a credit model trained only on approved applicants is exactly the wealth-threshold example.
> - **Outliers and leverage** connect to [[Data Preparation and Visualization/contents/00-Index|DPV]]'s outlier detection and to **regularization** in [[Machine Learning/contents/00-Index|ML]]. **LAD is $L^1$ loss; OLS is $L^2$ loss** — the same choice as MAE versus MSE, and it has the same consequence: $L^1$ targets the conditional median, $L^2$ the conditional mean. **Huber loss is the compromise.**
> - **Quantile regression** generalizes LAD and is the direct analogue of quantile forecasting in [[Time-series Analysis/contents/00-Index|Time-series Analysis]] and prediction-interval methods in ML.
> - **Proxy variables and the "different slant" of §2b** are the econometric version of the **prediction versus inference** distinction that runs through [[Machine Learning/contents/00-Index|ML]]. **For pure prediction, "omitted variable bias" is not a coherent concern** — a point Wooldridge makes explicitly, and one that resolves a great deal of confusion when econometricians and ML practitioners talk past each other.
> - **Random slope models** are **mixed / hierarchical models** in statistics and ML — the same $y_i=a_i+b_ix_i$ with $a_i,b_i$ drawn from a population distribution.

> [!warning] Gaps in the source material
> - **No lecture slides exist for Econometrics.** Chapter scope (Wooldridge 1–12) is my own editorial decision — see [[00-Index]].
> - **No data files are in the vault.** `CRIME1`, `CRIME2`, `HPRICE1`, `WAGE2`, `WAGE1`, `RDCHEM`, `INFMRT`, `BWGHT`, `LAWSCH85`, `CARD` and `MROZ` are referenced here and **none can be re-estimated.** All coefficients, standard errors and $R^2$ values are **quoted as printed.**
> - **⚠️ One genuine internal inconsistency in the source.** Table 9.1 prints $\hat\beta_{pcnv}=0.553$ and $\hat\beta_{pcnv^2}=-0.730$, which give a turning point of $$\frac{0.553}{2(0.730)}=\mathbf{0.379}$$ **but the text states $pcnv^*=0.365$.** No rounding of the printed coefficients reconciles the two (matching $0.365$ would require $\hat\beta_{pcnv}=0.533$ or $\hat\beta_{pcnv^2}=-0.758$). **I have quoted the text's $0.365$ above and flag the discrepancy here.** The economic reading — no deterrent effect at low conviction rates — is unaffected.
> - **⚠️ Two further Table 9.1 problems.** (i) The standard error printed for $ptime86$ in column (2) extracts as $(0.004)$, which against a coefficient of $0.287$ implies $t\approx72$ — **implausible, and almost certainly a print or extraction error**; I have omitted it above rather than quote a figure I do not believe. (ii) The $inc86^2$ coefficient extracts with the PDF's minus-sign glyph, i.e. $-0.000007$ — **but the text's stated turning point of $242.85$ requires $+0.000007$**, since $0.0034/[2(0.000007)]=242.86$ **exactly**. The text's description ("negatively related with a diminishing effect") also requires a positive squared term. **I have used $+0.000007$.**
> - **Internal consistency verified everywhere else, and it holds:** the $ptime86$ turning point ($4.85$), the $inc86$ turning point ($242.86$), the quadratics' joint $F$ ($31.47$ from the $R^2$s against the printed $31.37$ — rounding), both RESET $p$-values ($0.012$ and $0.084$ from the printed $F$ statistics), the IQ standard-deviation effect ($15\times0.0036=0.054$), all `CRIME2` $t$ statistics including the unit-elasticity test ($1.47$), every `RDCHEM` $t$ statistic and the "more than triples" claim ($3.51$), the residual-to-$\hat\sigma$ ratio ($-0.89$), the studentized-residual $p$-value ($0.079$ vs the printed $0.08$), the $profmarg$ $p$-value in the $n=30$ regression ($0.0508$ vs the printed $0.051$), both $H_0:\beta_1=1$ tests in Example 9.9, and every `INFMRT` $t$ statistic. ✓
> - **Figure 9.1** (scatterplot of R&D intensity against firm sales, with the outlier labelled) and **Figure 9.2** (the OLS and LAD objective functions) **are images** and do not extract. Both are described in the surrounding prose and reconstructed above; **Figure 9.2's content — quadratic versus linear-in-$|u|$ — is stated explicitly in the text.**
> - **Tables 9.1, 9.2 and 9.3 extracted intact** apart from the sign and standard-error problems flagged above.
> - **§9-5a's discussion of more sophisticated missing-data methods is deliberately truncated by the author** ("beyond the scope of this text"), so **no imputation method is described** — only the complete-cases and missing-indicator estimators.
> - **Notation mangling in the PDF:** `xp 3` for $x_3^*$, `x*1` and `xp 1` both for $x_1^*$, `yˇ` for $\check y$, `s2 e1` for $\sigma_{e_1}^2$, `s2* x1` for $\sigma_{x_1^*}^2$, `E1u0x2` for $\mathbb{E}(u\mid x)$, `Med1u0x2` for $\mathrm{Med}(u\mid\mathbf{x})$, `tate` for $\tau_{ate}$, `2.133` for $-0.133$ (the minus sign renders as a `2` throughout). **Every equation has been transcribed by hand against its numbered reference.**
> - **One source typo:** §9-5b refers to *"the parameters in (9.32)"* where **(9.38)** is meant — (9.32) is the CEV covariance derivation, several pages earlier. Corrected silently above.

#econometrics #specification #proxy-variables #measurement-error #outliers #reset #lad
