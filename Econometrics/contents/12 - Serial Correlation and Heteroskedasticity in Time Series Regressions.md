---
subject: Econometrics
chapter: 12
tags: [ds, econometrics, time-series, serial-correlation, newey-west, arch, gls]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 12 (pp. 394–424)"
---

# Serial Correlation and Heteroskedasticity in Time Series Regressions

> [!abstract] What this chapter is for
> **The last chapter of the course, and it closes the loop.** [[11 - Further Issues in Using OLS with Time Series Data|Chapter 11]] showed that a **dynamically complete** model has serially uncorrelated errors, and that **static and finite distributed lag models are usually not dynamically complete.** So serial correlation is the *normal* state of affairs for exactly the models we most want to estimate.
>
> **The structure deliberately mirrors [[08 - Heteroskedasticity|ch. 08]]:** consequences → robust inference → tests → GLS correction. **And the punchline is the same:** the coefficients survive, **the standard errors do not.**
>
> **But there is one thing serial correlation does that heteroskedasticity never did** — the usual OLS standard errors are typically **too small**, so $t$ statistics are **too big**. *"We will tend to think the OLS slope estimator is more precise than it actually is."* **Heteroskedasticity could bias the standard errors either way; serial correlation reliably flatters you.**
>
> | § | Topic | Requires strict exogeneity? |
> |---|---|---|
> | **1** | What serial correlation does (and does not) break | — |
> | **2** | **Newey–West / HAC** standard errors | **No** ← why this is now the default |
> | **3** | **Testing**: the $t$ test, Durbin–Watson, Durbin's alternative, **Breusch–Godfrey** | §3a–b yes; §3c–d no |
> | **4** | **Correcting**: quasi-differencing, **Cochrane–Orcutt**, **Prais–Winsten**, FGLS | **Yes** ← the catch |
> | **5** | Differencing as a serial correlation fix | — |
> | **6** | Heteroskedasticity in time series; **ARCH** | — |

---

## 📘 Main Knowledge

### 1. Properties of OLS with serially correlated errors

#### 1a. What survives: unbiasedness and consistency

> [!important] Serial correlation does **not** bias the coefficients
> - **Theorem 10.1** (unbiasedness) assumed only **TS.1–TS.3** — **nothing about serial correlation.** So under **strict exogeneity**, $\hat\beta_j$ is unbiased **regardless of how serially correlated the errors are.**
> - **Theorem 11.1** (consistency) needed only **contemporaneous exogeneity** and weak dependence — again **no assumption about serial correlation.**
>
> **Exactly parallel to heteroskedasticity in [[08 - Heteroskedasticity|ch. 08]]: it is a property of $\mathrm{Var}(u\mid x)$ or $\mathrm{Cov}(u_t,u_s)$, and unbiasedness is a property of $\mathbb{E}(u\mid x)$. Different moments, different consequences.**

#### 1b. What breaks: efficiency and inference

**Gauss–Markov (Theorem 10.4) requires both homoskedasticity *and* no serial correlation, so OLS is no longer BLUE.** Worse — and this is the practical damage — **the usual standard errors and test statistics are invalid, even asymptotically.**

To see exactly how, take the simple regression $y_t=\beta_0+\beta_1x_t+u_t$ with $\bar x=0$ (a harmless normalisation), so

$$\hat\beta_1 = \beta_1 + \mathrm{SST}_x^{-1}\sum_{t=1}^n x_tu_t \tag{12.3}$$

and let the errors follow a **stable AR(1)**:

$$u_t=\rho u_{t-1}+e_t, \qquad |\rho|<1 \tag{12.1–12.2}$$

Because $\mathbb{E}(u_tu_{t+j})=\mathrm{Cov}(u_t,u_{t+j})=\rho^{\,j}\sigma^2$ (from $\mathrm{Corr}(u_t,u_{t+h})=\rho^h$ in [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]), the variance of the sum picks up **every cross-product term**:

$$\boxed{\mathrm{Var}(\hat\beta_1)=\underbrace{\frac{\sigma^2}{\mathrm{SST}_x}}_{\text{the usual formula}} + \underbrace{2\left(\frac{\sigma^2}{\mathrm{SST}_x^2}\right)\sum_{t=1}^{n-1}\sum_{j=1}^{n-t}\rho^{\,j}x_tx_{t+j}}_{\textbf{the term OLS ignores}}} \tag{12.4}$$

> [!important] Why OLS standard errors are usually **too small**
> The second term is what the usual variance estimator throws away. **In most economic applications it is positive**, for two reasons that hold together:
>
> 1. **$\rho>0$ is by far the most common case**, so $\rho^{\,j}>0$ for every $j$.
> 2. **Regressors in economics are themselves positively serially correlated**, so $x_tx_{t+j}>0$ for most pairs.
>
> **Positive × positive = the true variance exceeds $\sigma^2/\mathrm{SST}_x$.** So:
> $$\text{usual se } \downarrow \;\Longrightarrow\; t \text{ statistics } \uparrow \;\Longrightarrow\; \textbf{over-rejection}$$
> *"If $\rho$ is large or $x_t$ has a high degree of positive serial correlation—a common case—the bias in the usual OLS variance estimator can be substantial."*

> [!warning] But the sign is not guaranteed
> **If $\rho<0$**, then $\rho^{\,j}$ alternates sign (negative for odd $j$, positive for even $j$), and the sum's sign is **indeterminate** — the usual formula may actually **overstate** the true variance.
>
> **Either way the usual variance estimator is biased.** The reliable statement is *"biased"*; the *usual* statement is *"biased downward."*

$F$ and LM statistics for multiple hypotheses are invalid for the same reason.

#### 1c. Goodness of fit survives

> [!tip] $R^2$ and $\bar R^2$ are fine — a claim you will hear otherwise
> A common assertion is that serial correlation invalidates $R^2$. **It does not, provided the data are stationary and weakly dependent.**
>
> The population $R^2$ is $1-\sigma_u^2/\sigma_y^2$ ([[06 - Multiple Regression Analysis - Further Issues|ch. 06 §3]]). Under stationarity **both variances are constant over time**, and by the LLN, $R^2$ and $\bar R^2$ **consistently estimate it.** Same argument as heteroskedasticity in [[08 - Heteroskedasticity|ch. 08 §1]].
>
> **There is never an unbiased estimator of the population $R^2$, so "bias in $R^2$ caused by serial correlation" is not even a well-posed idea.**

> [!warning] The exception
> **This fails if $\{y_t\}$ is I(1)**, because $\mathrm{Var}(y_t)$ grows with $t$ — **there is no population $R^2$ to estimate, and goodness of fit does not make much sense.** Trends and seasonality should be accounted for first (see [[10 - Basic Regression Analysis with Time Series Data|ch. 10 §5]] on the detrended $R^2$).

#### 1d. Lagged dependent variables: a myth, corrected

> [!warning] *"OLS is inconsistent in the presence of lagged dependent variables and serially correlated errors"*
> **Almost every textbook contains this sentence. As a general assertion it is false.** There is a correct version, but it requires precision.

**Where the claim fails.** Suppose the conditional expectation really is first-order:

$$\mathbb{E}(y_t\mid y_{t-1})=\beta_0+\beta_1y_{t-1}, \qquad |\beta_1|<1 \tag{12.5}$$

Write it in error form: $y_t=\beta_0+\beta_1y_{t-1}+u_t$ with $\mathbb{E}(u_t\mid y_{t-1})=0$ (12.6–12.7). **This satisfies TS.3′ by construction, so OLS is consistent.**

**But the errors can still be serially correlated!** Condition (12.7) makes $u_t$ uncorrelated with $y_{t-1}$ — **it says nothing about $u_t$ and $y_{t-2}$.** Since $u_{t-1}=y_{t-1}-\beta_0-\beta_1y_{t-2}$,

$$\mathrm{Cov}(u_t,u_{t-1}) = -\beta_1\mathrm{Cov}(u_t,y_{t-2}) \quad \text{which need not be zero.}$$

> [!important] So: lagged dependent variable **+** serially correlated errors **+** consistent OLS, all at once
> **Inference is invalid, consistency is not affected.** $\beta_0$ and $\beta_1$ are the parameters of the conditional expectation (12.5), and OLS estimates them consistently.

**Where the claim holds.** Inconsistency arises when you write (12.6) **and additionally assume $\{u_t\}$ follows a stable AR(1)** with

$$\mathbb{E}(e_t\mid u_{t-1},u_{t-2},\dots)=\mathbb{E}(e_t\mid y_{t-1},y_{t-2},\dots)=0 \tag{12.8}$$

Then $\mathrm{Cov}(y_{t-1},u_t)=\rho\,\mathrm{Cov}(y_{t-1},u_{t-1})\ne0$ unless $\rho=0$, and **OLS is inconsistent.**

> [!warning] But the correct version is *wrongheaded*
> *"The correctness of this statement makes it no less wrongheaded."* **What would be the point of estimating (12.6) when the errors follow an AR(1)?** Substitute $u_{t-1}=y_{t-1}-\beta_0-\beta_1y_{t-2}$ into $u_t=\rho u_{t-1}+e_t$:
> $$y_t = \underbrace{\beta_0(1-\rho)}_{\alpha_0}+\underbrace{(\beta_1+\rho)}_{\alpha_1}y_{t-1}\underbrace{-\rho\beta_1}_{\alpha_2}y_{t-2}+e_t$$
> **The model *is* an AR(2)** — and
> $$\mathbb{E}(y_t\mid y_{t-1},y_{t-2},\dots)=\alpha_0+\alpha_1y_{t-1}+\alpha_2y_{t-2} \tag{12.9}$$
> **is what you actually want**, for forecasting or anything else. **OLS on (12.9) is consistent and asymptotically normal.**
>
> **The lesson:** *"you need a good reason for having both a lagged dependent variable in a model and a particular model of serial correlation in the errors."* **Serial correlation in a dynamic model usually just means you left out $y_{t-2}$.** Add the lag.

---

### 2. Serial correlation–robust (HAC) inference after OLS

> [!important] Why this section is the modern default
> **OLS needs only contemporaneous exogeneity for consistency.** So the attractive strategy is: **run OLS, then fix the standard errors** — exactly as heteroskedasticity-robust standard errors became routine in cross-sections ([[08 - Heteroskedasticity|ch. 08 §2]]).
>
> **The GLS methods of §4 require *strict* exogeneity. This does not.** That asymmetry is why HAC has won.

#### 2a. The Newey–West / Wooldridge procedure

Consider the multiple regression $y_t=\beta_0+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t$, and suppose we want a robust standard error for $\hat\beta_1$. Write $x_{t1}$ as a linear function of the other regressors plus an error:

$$x_{t1}=\delta_0+\delta_2x_{t2}+\cdots+\delta_kx_{tk}+r_t$$

Then

$$\mathrm{AVar}(\hat\beta_1)=\left(\sum_{t=1}^n\mathbb{E}(r_t^2)\right)^{-2}\mathrm{Var}\left(\sum_{t=1}^n r_tu_t\right)$$

**Under TS.5′, $a_t\equiv r_tu_t$ is serially uncorrelated** and the usual (or heteroskedasticity-robust) standard errors work. **If TS.5′ fails, we must account for $\mathrm{Corr}(a_t,a_s)$** — and in practice we assume that beyond a few periods the correlation is essentially zero. *(Weak dependence guarantees it is approaching zero, so this is reasonable.)*

> [!important] Serial correlation–robust standard error for $\hat\beta_1$
> **(i)** Estimate the model by OLS. Keep `"se($\hat\beta_1$)"` (the usual, incorrect one), $\hat\sigma$ (the SER / root MSE), and the residuals $\hat u_t$.
>
> **(ii)** Run the **auxiliary regression** $x_{t1}$ on $x_{t2},\dots,x_{tk}$ (with an intercept); keep the residuals $\hat r_t$. Form
> $$\hat a_t = \hat r_t\hat u_t$$
>
> **(iii)** For a chosen integer $g>0$ (the **truncation lag** or **bandwidth**),
> $$\boxed{\hat\nu = \sum_{t=1}^n\hat a_t^2 + 2\sum_{h=1}^{g}\left[1-\frac{h}{g+1}\right]\left(\sum_{t=h+1}^{n}\hat a_t\hat a_{t-h}\right)} \tag{12.12}$$
>
> **(iv)** The robust standard error is
> $$\boxed{\mathrm{se}(\hat\beta_1)=\left[\frac{\text{“se}(\hat\beta_1)\text{''}}{\hat\sigma}\right]^2\sqrt{\hat\nu}} \tag{12.13}$$
>
> *In words: take the usual standard error, divide by $\hat\sigma$, square it, multiply by $\sqrt{\hat\nu}$.*

Two special cases worth memorising:

$$g=1:\qquad \hat\nu=\sum_{t=1}^n\hat a_t^2+\sum_{t=2}^n\hat a_t\hat a_{t-1} \tag{12.14}$$

$$g=2:\qquad \hat\nu=\sum_{t=1}^n\hat a_t^2+\tfrac{4}{3}\sum_{t=2}^n\hat a_t\hat a_{t-1}+\tfrac{2}{3}\sum_{t=3}^n\hat a_t\hat a_{t-2} \tag{12.15}$$

> [!tip] Two structural facts about the formula
> **The weights $[1-h/(g+1)]$ are not decoration.** They decline linearly with $h$ (the **Bartlett kernel**) and exist to **guarantee $\hat\nu\ge0$** — essential, since $\hat\nu$ estimates a variance and its square root appears in (12.13).
>
> **Drop the second term entirely ($g=0$) and (12.13) becomes the ordinary heteroskedasticity-robust standard error of [[08 - Heteroskedasticity|ch. 08]]** (without the df adjustment). **HAC is White's estimator plus autocovariance terms.** Hence the name: **heteroskedasticity and autocorrelation consistent (HAC)**.

#### 2b. Choosing the truncation lag $g$

This is the awkward part. **Theory says (12.13) works for fairly arbitrary serial correlation provided $g$ grows with $n$** — larger samples permit more flexibility — but that leaves the finite-sample choice open.

| Rule | Formula | $n=70$ | $n=280$ |
|---|---|---|---|
| EViews default (Newey–West 1994, preliminary stage) | $4(n/100)^{2/9}$ | $3.70\to\mathbf{3}$ | $5.03\to\mathbf{5}$ |
| Stock & Watson (2014), from Andrews (1991) assuming AR(1) with $\rho=.5$ | $\tfrac34 n^{1/3}$ | $3.09\to\mathbf{3}$ | $4.91\to\mathbf{4}$ |
| Another common suggestion | $n^{1/4}$ | $2.89\to\mathbf{2}$ | $4.09\to\mathbf{4}$ |

> [!tip] Practical guidance by data frequency
> - **Annual data:** $g=1$ or $2$ is likely to capture most of the serial correlation
> - **Quarterly:** $g=4$ or $8$
> - **Monthly:** $g=12$ or $24$
>
> — assuming you have enough data for it.

> [!warning] Two honest caveats about HAC
> 1. **Newey–West standard errors can be poorly behaved with substantial serial correlation and small $n$** — *"where small can even be as large as, say, 100."* Time series samples are usually small; large cross-sections are where robust methods shine.
> 2. **The standard errors can be sensitive to $g$**, and you must either choose it or accept a package's rule of thumb. **Different researchers, same data, different standard errors.** (See Kiefer and Vogelsang 2005.)
>
> **This is precisely why §3 still bothers to test for serial correlation** — if you cannot detect it, it may be prudent not to adjust at all.

##### Example 12.1 — The Puerto Rican minimum wage

Extending Example 10.9, regress the employment rate on $\log(mincov)$, $\log(usgnp)$, $\log(prgnp)$ and a linear trend. OLS gives

$$\hat\beta_1=-0.2123, \qquad \text{“se''}=0.0402, \qquad \hat\sigma=0.0328$$

With $g=2$, the procedure yields $\hat\nu=.000805$, so

$$\mathrm{se}(\hat\beta_1)=\left(\frac{.0402}{.0328}\right)^2\sqrt{.000805} = (1.2256)^2(0.02837) \approx \mathbf{0.0426}$$

> [!note] Reading the result
> The HAC standard error is **larger than the OLS one — but only by about 6%.** The HAC $t$ statistic is $-0.2123/0.0426 \approx \mathbf{-4.98}$ (versus $-5.28$), **so the elasticity remains overwhelmingly significant.**
>
> **The value of the exercise is not that the conclusion changed — it is that we can now defend it.** *"We can now have more confidence in our inference because we have accounted for serial correlation."*

#### 2c. The Kiefer–Vogelsang alternative

An elegant sidestep to the bandwidth problem. Instead of requiring $g/n\to0$, **let $b=(g+1)/n$ settle at a nonzero fraction** — at $b=1$, $g=n-1$ and **every** covariance term in (12.12) is included. The resulting $t$ statistic is **not** asymptotically standard normal, but it does have a tabulated asymptotic distribution:

| Two-sided test | Kiefer–Vogelsang critical value | Standard normal |
|---|---|---|
| 5% | $\mathbf{4.771}$ | $1.96$ |
| 10% | $\mathbf{3.764}$ | $1.645$ |

> [!important] The trade
> **You need a much larger $t$ statistic — but you never have to choose $g$.** The critical values price in the cost of using all the covariance terms.

*HAC-robust $F$-type statistics for multiple hypotheses exist and are computed routinely by packages, but their derivation is beyond this course.*

---

### 3. Testing for serial correlation

> [!note] Why test at all, given §2?
> Three reasons:
> 1. **HAC requires a bandwidth, and different choices give different standard errors even when there is no serial correlation.** If simple forms cannot be detected, **it may be prudent not to adjust.**
> 2. **§4's GLS may be more efficient** — but only if serial correlation is genuinely present. **Same logic as demanding evidence of heteroskedasticity before switching to WLS in [[08 - Heteroskedasticity|ch. 08 §4]].**
> 3. **Some models *should* have no serial correlation** — especially forecasting models with lagged $y$. **Then a test is a diagnostic for missing lags** ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11 §4]]).

**In every test below the null is "no serial correlation."** As with heteroskedasticity, **we assume the best and require the data to prove otherwise.**

#### 3a. The $t$ test for AR(1) with strictly exogenous regressors

The AR(1) alternative $u_t=\rho u_{t-1}+e_t$ with $\mathbb{E}(e_t\mid u_{t-1},\dots)=0$ and $\mathrm{Var}(e_t\mid u_{t-1})=\sigma_e^2$, testing

$$H_0:\ \rho=0 \tag{12.18}$$

If the $u_t$ were observed we could just regress $u_t$ on $u_{t-1}$ and use Theorem 11.2. **They are not — so we substitute the OLS residuals.**

> [!important] Testing for AR(1) with strictly exogenous regressors
> **(i)** Regress $y_t$ on $x_{t1},\dots,x_{tk}$; obtain $\hat u_t$.
> **(ii)** Regress $\hat u_t$ on $\hat u_{t-1}$ for $t=2,\dots,n$; obtain $\hat\rho$ and $t_{\hat\rho}$. *(An intercept may or may not be included — asymptotically valid either way.)*
> **(iii)** Test $H_0:\rho=0$ using $t_{\hat\rho}$ as usual. **Report the $p$-value.**

> [!tip] Why replacing $u_t$ with $\hat u_t$ is harmless here
> $\hat u_t$ depends on $\hat\beta_0,\dots,\hat\beta_k$, so it is not obvious the $t$ statistic is unaffected. **It is unaffected — but only because of strict exogeneity.** (Proof: Wooldridge 1991b, well beyond this text.) **Drop strict exogeneity and this test breaks — hence §3c.**

**A one-sided alternative $H_1:\rho>0$ is often appropriate**, since positive serial correlation is expected a priori.

> [!warning] What this test can and cannot detect
> $\hat\rho$ consistently estimates $\mathrm{Corr}(u_t,u_{t-1})$, so **it picks up *any* serial correlation that makes adjacent errors correlated — not just AR(1).**
>
> **But it is blind to serial correlation where adjacent errors are uncorrelated** — e.g. $u_t$ correlated with $u_{t-2}$ but not $u_{t-1}$. **For that, use the AR($q$) test of §3d.**

**Heteroskedasticity-robust version:** just use the heteroskedasticity-robust $t$ statistic from [[08 - Heteroskedasticity|ch. 08]] in step (ii).

##### Example 12.2 — Testing the Phillips curves

| Model | $\hat\rho$ | $t$ | $p$-value | $n$ | Verdict |
|---|---|---|---|---|---|
| **Static** Phillips curve (Example 10.1) | $\mathbf{.571}$ | $\mathbf{5.48}$ | $.000$ | 58 | **Very strong positive serial correlation** |
| **Expectations-augmented** (Example 11.5) | $-.033$ | $-.29$ | $.773$ | 57 | **No evidence at all** |

> [!important] Two chapters converging on the same verdict
> **The static Phillips curve is badly misspecified; the expectations-augmented version is not.** [[11 - Further Issues in Using OLS with Time Series Data|Ch. 11]] reached this conclusion from *economics* — the static version gave a **positive** inflation–unemployment relation, contradicting theory. **Ch. 12 reaches it from the residuals.**
>
> Consequence: **the ch. 10 standard errors and $t$ statistics for the static curve are not valid**, and a HAC standard error should be computed.
>
> *(Heteroskedasticity-robust check: the static curve's $t$ falls from $5.48$ to $\mathbf{3.98}$ — smaller, still overwhelming.)*

#### 3b. The Durbin–Watson test

$$\boxed{DW=\frac{\sum_{t=2}^n(\hat u_t-\hat u_{t-1})^2}{\sum_{t=1}^n\hat u_t^2}} \tag{12.21}$$

$$\boxed{DW \approx 2(1-\hat\rho)} \tag{12.22}$$

> [!note] Why the approximation is not exact
> $\hat\rho$ has $\sum_{t=2}^n\hat u_{t-1}^2$ in its denominator; $DW$ has the sum of squares of **all** residuals. **Even at moderate $n$ the approximation is often close, and the two tests are conceptually the same.**

Reading the statistic:

$$\hat\rho\approx 0 \;\Rightarrow\; DW\approx2 \qquad\qquad \hat\rho>0 \;\Rightarrow\; DW<2$$

so testing against $H_1:\rho>0$ means **looking for $DW$ significantly below 2.**

> [!warning] The inconclusive region
> Durbin and Watson (1950) derived the exact distribution of $DW$ — **but it requires the full CLM assumptions including normality, and it depends on the values of the regressors**, plus $n$, $k$, and whether an intercept is included. So tables report **two** bounds:
>
> $$DW<d_L \Rightarrow \textbf{reject } H_0 \qquad DW>d_U \Rightarrow \textbf{fail to reject} \qquad d_L\le DW\le d_U \Rightarrow \textbf{inconclusive}$$
>
> **Example:** at 5% with $n=45$, $k=4$: $d_L=1.336$, $d_U=1.720$. **Anything between them and the test simply gives no answer.**

**Applied to Example 12.2:**

| Model | $DW$ | Critical value | Verdict |
|---|---|---|---|
| Static Phillips curve | $\mathbf{.80}$ | $d_L=1.32$ (1% level, $k=1$, $n=50$) | **Reject** — positive serial correlation at 1% |
| Expectations-augmented | $\mathbf{1.77}$ | $d_U=1.59$ (5%) | **Fail to reject**, comfortably |

> [!warning] Prefer the $t$ test — the DW statistic is largely a historical artefact
> **Its only advantage is that an exact sampling distribution can be tabulated.** Against that:
>
> | | $t$ test from (12.20) | Durbin–Watson |
> |---|---|---|
> | Needs normality | **No** | **Yes** (for the tabulated values) |
> | Inconclusive region | **None** | **Often wide** |
> | Valid under heteroskedasticity in $x_{tj}$ | **Yes** | No |
> | Easily made fully heteroskedasticity-robust | **Yes** | No |
> | Valid without strict exogeneity | No (→ §3c) | No |
>
> *"The practical disadvantages of the DW statistic are substantial."*

#### 3c. Durbin's alternative — testing without strict exogeneity

> [!warning] When the regressors are not strictly exogenous, **neither the §3a $t$ test nor DW is valid, even in large samples**
> **The leading case is a lagged dependent variable**, where $y_{t-1}$ and $u_{t-1}$ are obviously correlated.

*(Durbin (1970) also proposed **Durbin's $h$ statistic**, but it cannot always be computed, so it is not covered.)*

> [!important] Testing for serial correlation with general regressors
> **(i)** Regress $y_t$ on $x_{t1},\dots,x_{tk}$; obtain $\hat u_t$.
> **(ii)** Regress
> $$\hat u_t \text{ on } \hat u_{t-1},\,x_{t1},\,x_{t2},\dots,x_{tk}, \qquad t=2,\dots,n \tag{12.24}$$
> obtaining $\hat\rho$ and $t_{\hat\rho}$.
> **(iii)** Test $H_0:\rho=0$ as usual.

> [!tip] The whole trick is one added set of regressors
> **Including $x_{t1},\dots,x_{tk}$ explicitly allows each $x_{tj}$ to be correlated with $u_{t-1}$** — which is exactly what strict exogeneity forbade and what (12.20) silently assumed away. **That is what restores the approximate $t$ distribution.**
>
> **Any number of lagged dependent variables may appear among the $x_{tj}$.** The test also works fine when the regressors *are* strictly exogenous — **so when in doubt, use this one.**
>
> *(Incidentally: because $\hat u_t=y_t-\hat\beta_0-\hat\beta_1x_{t1}-\cdots$, the $t$ statistic on $\hat u_{t-1}$ is **identical** if you use $y_t$ as the dependent variable in (12.24).)*

**Heteroskedasticity-robust version:** use the heteroskedasticity-robust $t$ statistic on $\hat u_{t-1}$.

##### Example 12.3 — The minimum wage equation

Regressing $\hat u_t$ on $\hat u_{t-1},\log(mincov),\log(usgnp),\log(prgnp),t$ over 37 observations:

$$\hat\rho=.481, \qquad t=2.89, \qquad p=.007$$

**Strong evidence of AR(1) serial correlation**, so the earlier $t$ statistics are invalid. *(Using the simpler regression (12.20) instead gives $\hat\rho=.417$, $t=2.63$ — a similar outcome here.)* **The $\hat\beta_j$ remain consistent**, since $u_t$ is contemporaneously uncorrelated with each regressor.

> [!important] The pairing with Example 12.1 is the point
> **Strong, highly significant serial correlation — and the HAC standard error was only 6% larger than the usual one.**
>
> **Statistical significance of $\hat\rho$ does not translate into a large correction.** Look back at (12.4): what inflates the variance is the **product** $\rho^{\,j}x_tx_{t+j}$ summed over all pairs. Formally, *"it is the sample autocorrelations of $\hat a_t=\hat r_t\hat u_t$ that determine the robust standard error"* — **not the autocorrelation of $\hat u_t$ alone.**

#### 3d. Higher-order serial correlation: the Breusch–Godfrey test

For the AR($q$) alternative $u_t=\rho_1u_{t-1}+\cdots+\rho_qu_{t-q}+e_t$, testing

$$H_0:\ \rho_1=\rho_2=\cdots=\rho_q=0 \tag{12.27}$$

> [!important] Testing for AR($q$) serial correlation
> **(i)** Regress $y_t$ on $x_{t1},\dots,x_{tk}$; obtain $\hat u_t$.
> **(ii)** Regress
> $$\hat u_t \text{ on } \hat u_{t-1},\hat u_{t-2},\dots,\hat u_{t-q},\,x_{t1},\dots,x_{tk}, \qquad t=(q+1),\dots,n \tag{12.28}$$
> **(iii)** Compute the **$F$ test for joint significance of $\hat u_{t-1},\dots,\hat u_{t-q}$**.
>
> **Or use the LM form — the Breusch–Godfrey test:**
> $$\boxed{LM=(n-q)R^2_{\hat u} \;\overset{a}{\sim}\; \chi^2_q} \tag{12.30}$$
> where $R^2_{\hat u}$ is the $R^2$ from (12.28).

> [!tip] Notes on the mechanics
> - **If the $x_{tj}$ are strictly exogenous they can be omitted** from (12.28). **Including them makes the test valid either way** — so include them.
> - Requires the homoskedasticity assumption $\mathrm{Var}(u_t\mid\mathbf{x}_t,u_{t-1},\dots,u_{t-q})=\sigma^2$ (12.29); **a heteroskedasticity-robust version exists.**
> - Using $y_t$ as the dependent variable in (12.28) gives an **identical** answer.

##### Example 12.4 — AR(3) in the barium chloride event study

Monthly data (Example 10.5, equation 10.22), so higher orders are plausible. From regression (12.28):

$$F=5.12 \quad \text{with } df=(3,\,118), \qquad p=\mathbf{.0023}$$

*(Arithmetic check: $n=131$, lose 3 to lagging $\to128$; 10 parameters estimated $\to128-10=118$.)*

**Strong evidence of AR(3) serial correlation.** *"If we were trying to publish the findings... we should use Newey-West standard errors, probably with a truncated lag of three or four given the sample size of 131."*

##### Seasonal serial correlation

With quarterly or monthly data that are **not seasonally adjusted**, test the seasonal alternative $u_t=\rho_4u_{t-4}+e_t$ (12.31) — **just replace $\hat u_{t-1}$ with $\hat u_{t-s}$** in (12.20) or (12.24).

For the monthly barium data, regressing $\hat u_t$ on $\hat u_{t-12}$:

$$\hat\rho_{12}=-.187, \quad p=.028 \qquad\qquad \text{(with regressors included: } -.170,\ p=.052)$$

**Evidence of *negative* seasonal autocorrelation** — which Wooldridge notes is *"somewhat unusual and does not have an obvious explanation."*

---

### 4. Correcting for serial correlation with strictly exogenous regressors

> [!warning] Read the section title — the condition is the whole story
> §2's HAC approach needs only **contemporaneous** exogeneity. **Everything in this section needs *strict* exogeneity.** *"We certainly should not use GLS methods to estimate models with lagged dependent variables."*
>
> **So why bother?** Because if strict exogeneity does hold, **GLS is asymptotically more efficient than OLS**, and inference is simplified. **You may be forced to try it if the Newey–West standard errors are so large that confidence intervals are useless.**

#### 4a. The BLUE estimator under AR(1) errors — quasi-differencing

Assume TS.1–TS.4 hold but TS.5 fails, with $u_t=\rho u_{t-1}+e_t$ and hence $\mathrm{Var}(u_t)=\sigma_e^2/(1-\rho^2)$. For $y_t=\beta_0+\beta_1x_t+u_t$, write the equation at $t$ and $t-1$, **multiply the lagged one by $\rho$ and subtract:**

$$y_t-\rho y_{t-1}=(1-\rho)\beta_0+\beta_1(x_t-\rho x_{t-1})+e_t, \qquad t\ge2$$

> [!important] Quasi-differenced data
> $$\boxed{\tilde y_t=y_t-\rho y_{t-1}, \qquad \tilde x_t = x_t-\rho x_{t-1}} \tag{12.35}$$
> **The errors in the transformed equation are $e_t$ — serially uncorrelated.** The transformed equation satisfies **all** the Gauss–Markov assumptions.
>
> **If $\rho=1$ these are ordinary first differences** — but we are assuming $|\rho|<1$, so they are only *quasi*-differences.

**Remember to divide the estimated intercept by $(1-\rho)$** to recover $\beta_0$.

##### The first observation

The estimator from $t\ge2$ alone is **not quite BLUE — it throws away period 1.** But period 1 cannot simply be appended: $\mathrm{Var}(u_1)=\sigma_e^2/(1-\rho^2)>\sigma_e^2=\mathrm{Var}(e_t)$, so adding it raw would introduce **heteroskedasticity**. Multiply through by $(1-\rho^2)^{1/2}$:

$$\boxed{\tilde y_1=(1-\rho^2)^{1/2}y_1,\quad \tilde x_1=(1-\rho^2)^{1/2}x_1,\quad \text{intercept} = (1-\rho^2)^{1/2}\beta_0} \tag{12.37}$$

Then $\mathrm{Var}(\tilde u_1)=(1-\rho^2)\mathrm{Var}(u_1)=\sigma_e^2$ — **matched.** OLS on (12.37) together with (12.34) is the **GLS estimator**, and it is **BLUE** under TS.1–TS.4 plus the AR(1) model.

With $k$ regressors nothing changes: $\tilde x_{tj}=x_{tj}-\rho x_{t-1,j}$ for $t\ge2$, and $\tilde x_{1j}=(1-\rho^2)^{1/2}x_{1j}$.

#### 4b. Feasible GLS — Cochrane–Orcutt and Prais–Winsten

**$\rho$ is never known. But we already know how to estimate it — regression (12.20).**

> [!important] Feasible GLS estimation of the AR(1) model
> **(i)** OLS regression of $y_t$ on $x_{t1},\dots,x_{tk}$; obtain $\hat u_t$.
> **(ii)** Regress $\hat u_t$ on $\hat u_{t-1}$ (equation 12.20); obtain $\hat\rho$.
> **(iii)** Apply OLS to the quasi-differenced equation
> $$\tilde y_t=\beta_0\tilde x_{t0}+\beta_1\tilde x_{t1}+\cdots+\beta_k\tilde x_{tk}+error_t \tag{12.39}$$
> where $\tilde x_{t0}=(1-\hat\rho)$ for $t\ge2$ and $\tilde x_{10}=(1-\hat\rho^2)^{1/2}$.
>
> **The usual standard errors, $t$ and $F$ statistics are asymptotically valid.**

> [!important] The two named variants — the difference is one observation
> | | First observation | $\hat\rho$ from |
> |---|---|---|
> | **Cochrane–Orcutt (CO)** | **Dropped** | (12.20) |
> | **Prais–Winsten (PW)** | **Kept**, weighted by $(1-\hat\rho^2)^{1/2}$ | (12.20) |
>
> **Asymptotically identical. But time series samples are small, so the difference can be notable in applications** — with $n=49$, one observation is 2% of the sample.

**Both are normally run *iteratively*:** get FGLS estimates → new residuals → new $\hat\rho$ → re-transform → re-estimate, until $\hat\rho$ stabilises. **Packages do this automatically.** *"It is difficult to say whether more than one iteration helps"* — the large-sample properties are the same either way.

> [!warning] What FGLS costs
> **$\hat\rho$ is estimated, so the FGLS estimator has no tractable finite-sample properties.**
> - **It is not unbiased** — therefore **not BLUE**, despite GLS-with-known-$\rho$ being BLUE.
> - It **is** consistent (under weak dependence) and **asymptotically more efficient than OLS** when the AR(1) model holds and the regressors are strictly exogenous.
> - **$t$ and $F$ are only approximately distributed as $t$ and $F$** — even with normal $e_t$ — *"we must be careful with small sample sizes."*
>
> **Exactly parallel to feasible GLS for heteroskedasticity in [[08 - Heteroskedasticity|ch. 08 §4]]: estimating the nuisance parameter costs you the finite-sample theory.**

##### Example 12.5 — Prais–Winsten in the event study

`BARIUM` data, dependent variable $\log(chnimp)$, iterated PW versus OLS:

| Coefficient | OLS | Prais–Winsten |
|---|---|---|
| $\log(chempi)$ | $3.12\ (0.48)$ | $2.94\ (0.63)$ |
| $\log(gas)$ | $0.196\ (0.907)$ | $1.05\ (0.98)$ |
| $\log(rtwex)$ | $0.983\ (0.400)$ | $1.13\ (0.51)$ |
| $befile6$ | $0.060\ (0.261)$ | $-0.016\ (0.322)$ |
| $affile6$ | $-0.032\ (0.264)$ | $-0.033\ (0.322)$ |
| $afdec6$ | $-0.565\ (0.286)$ | $-0.577\ (0.342)$ |
| intercept | $-17.80\ (21.05)$ | $-37.08\ (22.78)$ |
| $\hat\rho$ | — | $\mathbf{.293}$ |
| $n$ / $R^2$ | $131$ / $.305$ | $131$ / $.202$ |

> [!important] Three things to read off this table
> **1. The significant coefficients barely move.** $\log(chempi)$, $\log(rtwex)$ and $afdec6$ are all close across methods. *"It is not surprising for statistically insignificant coefficients to change, perhaps markedly, across different estimation methods."* — note $\log(gas)$ going from $0.196$ to $1.05$, and being insignificant in both.
>
> **2. Every PW standard error is larger. This is common** — the OLS standard errors *"usually understate the actual sampling variation... and should not be relied upon when significant serial correlation is present."* The practical consequence: **the ITC decision effect $afdec6$ falls from $t=-1.98$ to $t=-1.69$** — from marginally significant at 5% to not. **The event study's headline result is weaker than ch. 10 suggested.**
>
> **3. Do not compare the two $R^2$ values.** $.305$ versus $.202$ is **not** a deterioration. The OLS $R^2$ uses **untransformed** variables; the PW $R^2$ comes from the final regression of **transformed** variables on transformed variables. *"It is not clear what this $R^2$ is actually measuring; nevertheless, it is traditionally reported."*

#### 4c. Comparing OLS and FGLS — the trap

**A big divergence between OLS and FGLS is often read as proof of FGLS's superiority. That reading is wrong.**

Consistency of **OLS** for $\beta_1$ needs only

$$\mathrm{Cov}(x_t,u_t)=0 \tag{12.40}$$

**Consistency of FGLS needs more.** The weakest additional condition is

$$\boxed{\mathrm{Cov}\big[(x_{t-1}+x_{t+1}),\,u_t\big]=0} \tag{12.41}$$

**Practically: $u_t$ must be uncorrelated with $x_{t-1}$, $x_t$ *and* $x_{t+1}$.**

> [!tip] Where (12.41) comes from — a short, worth-knowing derivation
> Take $\rho$ known and drop the first observation (CO). GLS regresses on $x_t-\rho x_{t-1}$ with error $u_t-\rho u_{t-1}$. By Theorem 11.1, consistency needs those uncorrelated:
> $$\mathbb{E}[(x_t-\rho x_{t-1})(u_t-\rho u_{t-1})] = \underbrace{\mathbb{E}(x_tu_t)}_{=0} -\rho\mathbb{E}(x_{t-1}u_t)-\rho\mathbb{E}(x_tu_{t-1})+\rho^2\underbrace{\mathbb{E}(x_{t-1}u_{t-1})}_{=0}$$
> $$= -\rho\big[\mathbb{E}(x_{t-1}u_t)+\mathbb{E}(x_tu_{t-1})\big]$$
> Under **stationarity**, $\mathbb{E}(x_tu_{t-1})=\mathbb{E}(x_{t+1}u_t)$ (shift the index forward one period), so the bracket is $\mathbb{E}[(x_{t-1}+x_{t+1})u_t]$ — **which is (12.41).** $\blacksquare$
>
> *(If $\rho=0$ the whole thing vanishes — we are back to OLS, which is why OLS never needs it.)*

> [!warning] The correct reading of a big OLS/FGLS divergence
> **A large gap may mean (12.41) fails — in which case OLS is consistent and FGLS is *inconsistent*.**
>
> **The two structural cases that break (12.41):**
> - **$x$ has a lagged effect on $y$** (so $u_t$ correlates with $x_{t-1}$)
> - **$x_{t+1}$ reacts to $u_t$** — feedback, the thing [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] worked so hard to permit
>
> **"FGLS can produce misleading results."** The decision rule:
>
> | | Interpretation |
> |---|---|
> | **OLS ≈ FGLS**, serial correlation present | **Prefer FGLS** — more efficient, valid test statistics |
> | **OLS ≠ FGLS substantially** | **Warning sign.** Possibly (12.41) fails → **prefer OLS with HAC** |
>
> *(Testing formally whether the difference is significant needs Hausman (1978), beyond this text.)*

##### Example 12.6 — Static Phillips curve, OLS versus PW

| Coefficient | OLS | Prais–Winsten |
|---|---|---|
| $unem$ | $\mathbf{0.468}\ (0.289)$ | $\mathbf{-0.716}\ (0.313)$ |
| intercept | $1.424\ (1.719)$ | $8.296\ (2.231)$ |
| $\hat\rho$ | — | $\mathbf{.781}$ |
| $n$ / $R^2$ | $49$ / $.053$ | $49$ / $.136$ |

**The sign flips.** OLS: $t=1.62$, a wrong-signed and insignificant *positive* relation. PW: $t=-2.29$, a **significant tradeoff consistent with theory.**

> [!important] Why PW and first differencing agree here
> With $\hat\rho=.781$, **quasi-differencing is close to first differencing** ($\rho=1$). And indeed the PW estimates *"are fairly close to what is obtained by first differencing both $inf$ and $unem$."*
>
> **The economic reading: $inf$ and $unem$ may simply not be related in levels, but have a negative relationship in first differences.**
>
> **The dilemma this poses is genuine.** If we truly want a static relationship and both series are I(0), **OLS is consistent with no further assumptions.** But if either has a unit root, OLS loses its usual properties (ch. 18). **Here FGLS gives more sensible estimates precisely because, being near-differencing, it approximately eliminates the unit roots.**

#### 4d. Higher-order corrections

For AR(2) errors $u_t=\rho_1u_{t-1}+\rho_2u_{t-2}+e_t$, the stability conditions are:

$$\boxed{\rho_2>-1, \qquad \rho_2-\rho_1<1, \qquad \rho_1+\rho_2<1}$$

> [!note] Worked check
> $(\rho_1,\rho_2)=(.8,-.3)$: $-.3>-1$ ✅, $-.3-.8=-1.1<1$ ✅, $.8-.3=.5<1$ ✅ → **stable**
> $(\rho_1,\rho_2)=(.7,.4)$: first two hold, but $.7+.4=1.1\not<1$ ❌ → **unstable**

The transformation for $t>2$ is

$$\tilde y_t = y_t-\rho_1y_{t-1}-\rho_2y_{t-2}, \qquad \tilde x_t = x_t-\rho_1x_{t-1}-\rho_2x_{t-2} \tag{12.42}$$

with intercept coefficient $\beta_0(1-\rho_1-\rho_2)$. **Obtain $\hat\rho_1,\hat\rho_2$ from regressing $\hat u_t$ on $\hat u_{t-1},\hat u_{t-2}$ — the same regression used to *test* for AR(2).**

The **first two** observations need their own transformation:

$$\tilde z_1=\left\{\frac{(1+\rho_2)\left[(1-\rho_2)^2-\rho_1^2\right]}{1-\rho_2}\right\}^{1/2}z_1, \qquad \tilde z_2=(1-\rho_2^2)^{1/2}z_2-\left[\frac{\rho_1(1-\rho_2^2)^{1/2}}{1-\rho_2}\right]z_1$$

**These are not derived, and you will not compute them by hand** — packages handle general AR($q$) errors. **Their purpose is the same as $(1-\rho^2)^{1/2}$ in the AR(1) case: kill the serial correlation among the initial observations and equalise their error variances at $\sigma_e^2$.**

#### 4e. What if the serial correlation model is wrong?

> [!important] The most reassuring — and most reusable — idea in the chapter
> **Getting the serial correlation model wrong does *not* cause inconsistency**, provided the regressors satisfy (12.40) and (12.41).
>
> > **Exogeneity of the explanatory variables is what matters for consistency, not the serial correlation or variance properties of the errors.**
>
> **This one sentence unifies [[08 - Heteroskedasticity|ch. 08]] and ch. 12.** Second-moment misspecification costs **efficiency and valid inference**, never consistency. First-moment misspecification costs **consistency**.

**What *does* break is the inference from (12.38)/(12.39):** if $\{u_t\}$ is actually AR(2) but you fit AR(1), the transformed errors have a complicated correlation pattern of their own.

> [!tip] The fix is delightfully circular — and correct
> **Quasi-difference the data, estimate (12.39) by OLS, then apply Newey–West standard errors to *that* regression.**
>
> **Using HAC after FGLS looks absurd** — the point of CO/PW was to eliminate serial correlation. **But it is exactly right:**
> - The **PW correction may still be more efficient than OLS** even if AR(1) is the wrong model — *"accounting for some of the serial correlation... might be considerably better than ignoring"* it
> - **The HAC standard errors keep inference valid** even though the model is wrong
> - **Bonus: they are also robust to arbitrary heteroskedasticity in $\{u_t\}$**
>
> *"The careful researcher readily admits that the AR(1) structure could be incorrect... and, therefore, conducts inference that is fully robust."*
>
> **The same principle appeared in [[08 - Heteroskedasticity|ch. 08 §4c]]:** WLS with an imperfect variance function may beat OLS on efficiency — **just compute robust standard errors so the comparison is honest.** *(Neither strategy is built into standard software; both are easy "by hand.")*

---

### 5. Differencing and serial correlation

**A second argument for differencing, independent of the unit-root argument of [[11 - Further Issues in Using OLS with Time Series Data|ch. 11 §3]].**

Start from $y_t=\beta_0+\beta_1x_t+u_t$ with $u_t$ following an AR(1). **In the extreme case where $\{u_t\}$ is a random walk, the equation makes no sense** — $\mathrm{Var}(u_t)$ grows with $t$. Difference it:

$$\Delta y_t = \beta_1\Delta x_t+\Delta u_t \tag{12.44}$$

**If $u_t$ is a random walk, $e_t\equiv\Delta u_t$ has zero mean, constant variance, and is serially uncorrelated** — the problem is gone entirely. And **even when $u_t$ is not a random walk, if $\rho$ is positive and large, differencing eliminates most of the serial correlation.**

> [!warning] But (12.44) is a different model from (12.43)
> **You are now estimating the relationship between *changes*, not *levels*.** Keep that firmly in mind when comparing coefficients. And **do not assume the differenced equation has no serial correlation either** — apply Newey–West to it too.

##### Example 12.7 — Differencing the interest rate equation

The levels equation (10.15) relating the three-month T-bill rate to inflation and the federal deficit: regressing its residuals on one lag gives

$$\hat\rho=.623\ (.110) \qquad t=5.66$$

**Serial correlation is at minimum a problem.** In differences:

$$\widehat{\Delta i3_t}=\underset{(0.171)}{0.042}+\underset{(0.092)}{0.149}\,\Delta inf_t-\underset{(0.148)}{0.181}\,\Delta def_t$$
$$n=55,\quad R^2=.176,\quad \bar R^2=.145$$

**The coefficients differ sharply from the levels equation** — suggesting either that the regressors are not strictly exogenous, or that something has a unit root. And indeed $\mathrm{Corr}(i3_t,i3_{t-1})\approx\mathbf{.885}$, *"which may indicate a problem with interpreting (10.15) as a meaningful regression."*

**Crucially, the differenced equation has essentially no serial correlation left:** regressing its residuals on one lag gives $\hat\rho=.072\ (.134)$, $t=0.54$.

> [!important] Differencing did two jobs at once
> **It removed the (possible) unit root *and* the serial correlation.** *"We probably have more faith in the estimates and standard errors from (12.45) than (10.15)."*
>
> **The substantive finding:** annual **changes** in interest rates are only weakly, positively related to changes in inflation ($t=1.62$), and the $\Delta def$ coefficient is **negative** and not significant even at 20% ($t=-1.22$, two-sided $p\approx.23$). **The levels regression told a much more confident story about a relationship that may not be there.**

---

### 6. Heteroskedasticity in time series regressions

**The mechanics carry over from [[08 - Heteroskedasticity|ch. 08]] essentially unchanged. What is new is the *dynamic* form.**

#### 6a. Heteroskedasticity-robust statistics

> [!important] Same conclusions as the cross-sectional case
> Heteroskedasticity has **no bearing on unbiasedness (Theorem 10.1) or consistency (Theorem 11.1)** — it invalidates the usual standard errors, $t$ and $F$ statistics, nothing more.
>
> **The [[08 - Heteroskedasticity|ch. 08 §2]] adjustments work directly for time series under TS.1′, TS.2′, TS.3′ and TS.5′.**
>
> **Read that list carefully: TS.5′ is *required*.** *"Serially correlated errors cause problems that adjustments for heteroskedasticity are not able to address."* **Heteroskedasticity-robust ≠ HAC.**

#### 6b. Testing, with two caveats

The Breusch–Pagan and White tests of [[08 - Heteroskedasticity|ch. 08 §3]] apply directly, **but:**

> [!warning] Caveat 1 — order of operations
> **The $u_t$ must not be serially correlated; any serial correlation generally invalidates a heteroskedasticity test.**
>
> **So: test for serial correlation first** (using a heteroskedasticity-robust version if heteroskedasticity is suspected), **correct it, and only then test for heteroskedasticity.**

> [!warning] Caveat 2 — the auxiliary equation's own errors
> For the BP regression
> $$u_t^2=\delta_0+\delta_1x_{t1}+\cdots+\delta_kx_{tk}+v_t \tag{12.46}$$
> the $F$ test (with $\hat u_t^2$ replacing $u_t^2$) requires the $\{v_t\}$ to be **homoskedastic *and* serially uncorrelated.**
>
> **Assuming $\{v_t\}$ is serially uncorrelated rules out exactly the dynamic heteroskedasticity of §6c.**

If heteroskedasticity is found (and the $u_t$ are not serially correlated), use robust statistics or **WLS — mechanically identical to the cross-sectional case.**

##### Example 12.8 — Heteroskedasticity and the EMH

Return to $return_t=\beta_0+\beta_1return_{t-1}+u_t$ from Example 11.4, where $t_{\hat\beta_1}=1.55$ gave no evidence against the EMH. **The EMH constrains the conditional *mean*; it says nothing about the conditional *variance*.** So run BP — regress $\hat u_t^2$ on $return_{t-1}$:

$$\hat u_t^2=\underset{(0.43)}{4.66}-\underset{(0.201)}{1.104}\,return_{t-1}$$
$$n=689,\quad R^2=.042$$

$t\approx\mathbf{-5.5}$ — **strong evidence of heteroskedasticity.** *(Equivalently $LM=689\times.042=28.9$ against $\chi^2_1$, $p<10^{-7}$.)*

> [!important] An economically interesting sign
> The coefficient is **negative**: **volatility is lower when the previous return was high, and higher after a bad week.** *"We have found what is common in many financial studies: the expected value of stock returns does not depend on past returns, but the variance of returns does."*

#### 6c. ARCH — autoregressive conditional heteroskedasticity

> [!important] Dynamic heteroskedasticity with no dynamics in the mean
> Take a purely **static** model $y_t=\beta_0+\beta_1z_t+u_t$ satisfying Gauss–Markov, so OLS is BLUE and $\mathrm{Var}(u_t\mid\mathbf{Z})$ is constant. **Engle (1982) asked a different question: what is the variance of $u_t$ conditional on *past errors*?**
>
> The **first-order ARCH model**:
> $$\boxed{\mathbb{E}(u_t^2\mid u_{t-1},u_{t-2},\dots)=\mathbb{E}(u_t^2\mid u_{t-1})=\alpha_0+\alpha_1u_{t-1}^2} \tag{12.49}$$
> **This is a conditional variance only if $\mathbb{E}(u_t\mid u_{t-1},\dots)=0$ — i.e. only if the errors are serially uncorrelated.** Since variances must be positive, $\alpha_0>0$ and $\alpha_1\ge0$.

Written as a regression,

$$u_t^2=\alpha_0+\alpha_1u_{t-1}^2+v_t \tag{12.50}$$

— **an autoregression in $u_t^2$, hence the name.** The stability condition is $\alpha_1<1$, just as for an AR(1).

> [!important] The defining feature
> **When $\alpha_1>0$, the *squared* errors are serially correlated even though the errors themselves are not.**
>
> **Volatility clusters: a big shock last period predicts a big shock this period, in magnitude but not in sign.**

**Why care, if OLS is still fine?**

> [!tip] Two reasons — one statistical, one substantive
> **1. Efficiency.** A weighted least squares procedure based on estimating (12.50) gives **consistent (though not unbiased) estimators that are asymptotically more efficient than OLS.** Maximum likelihood also works under conditional normality.
>
> **2. The conditional variance is itself the object of interest.** Engle's original application was UK inflation — *a larger $u_{t-1}^2$ was associated with a larger error variance today.* **Because volatility is a key element of asset pricing theories, ARCH models have become central to empirical finance.**

**ARCH also applies when there *are* dynamics in the mean.** With $\mathbb{E}(y_t\mid z_t,y_{t-1},z_{t-1},\dots)=\beta_0+\beta_1z_t+\beta_2y_{t-1}+\beta_3z_{t-1}$, the conditional variance may follow $\alpha_0+\alpha_1u_{t-1}^2$. **Consistency of OLS is unaffected, and the usual heteroskedasticity-robust standard errors remain valid — ARCH is just one particular form of heteroskedasticity.**

##### Example 12.9 — ARCH in stock returns

Square the OLS residuals from the return equation and regress on their own lag:

$$\hat u_t^2=\underset{(0.44)}{2.95}+\underset{(0.036)}{0.337}\,\hat u_{t-1}^2$$
$$n=688,\quad R^2=.114$$

$t=0.337/0.036=\mathbf{9.36}$ — **overwhelming evidence of ARCH.**

> [!important] The pair of facts that make this example famous
> $$\hat u_t \text{ on } \hat u_{t-1}: \quad \hat\rho=.0014, \quad t_{\hat\rho}=\mathbf{0.038}$$
>
> **The residuals themselves are completely serially uncorrelated — entirely consistent with the EMH. Their squares are massively autocorrelated.**
>
> **Returns are unpredictable; their volatility is highly predictable.** That is the empirical foundation of an entire field.
>
> *(Reading the fitted equation: after a quiet week, $\hat u_{t-1}^2\approx0$ and predicted variance is $2.95$; after a $\pm5\%$ surprise, $\hat u_{t-1}^2=25$ and predicted variance is $2.95+.337(25)=11.4$ — nearly four times as large.)*

#### 6d. Both problems at once

**Nothing rules out heteroskedasticity and serial correlation together.** If unsure, **use OLS with fully robust (HAC) standard errors.**

> [!note] Which problem to prioritise
> **Serial correlation is usually viewed as the more important problem** — *"it usually has a larger impact on standard errors and the efficiency of estimators than does heteroskedasticity."*

**A combined WLS + AR(1) procedure.** Model

$$y_t=\beta_0+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t, \qquad u_t=\sqrt{h_t}\,v_t, \qquad v_t=\rho v_{t-1}+e_t \tag{12.52}$$

with $h_t$ a function of the $x_{tj}$. Then $\mathrm{Var}(u_t\mid\mathbf{x}_t)=\sigma_v^2h_t$ where $\sigma_v^2=\sigma_e^2/(1-\rho^2)$, **but $v_t=u_t/\sqrt{h_t}$ is homoskedastic and follows a stable AR(1)** — so dividing through by $\sqrt{h_t}$ leaves an equation with AR(1) errors, which CO/PW can handle.

> [!important] Feasible GLS with heteroskedasticity **and** AR(1) serial correlation
> **(i)** Estimate by OLS; save $\hat u_t$.
> **(ii)** Regress $\log(\hat u_t^2)$ on $x_{t1},\dots,x_{tk}$ (or on $\hat y_t,\hat y_t^2$); get fitted values $\hat g_t$.
> **(iii)** $\hat h_t=\exp(\hat g_t)$.
> **(iv)** Estimate
> $$\hat h_t^{-1/2}y_t=\hat h_t^{-1/2}\beta_0+\beta_1\hat h_t^{-1/2}x_{t1}+\cdots+\beta_k\hat h_t^{-1/2}x_{tk}+error_t \tag{12.54}$$
> **by standard Cochrane–Orcutt or Prais–Winsten.**
>
> **This is literally [[08 - Heteroskedasticity|ch. 08 §4]]'s log-variance FGLS bolted onto §4b's quasi-differencing.** Steps (ii)–(iii) are the ch. 08 procedure verbatim.

**Asymptotically efficient if (12.52) holds, with all standard errors valid.** And if you doubt either the variance function or the AR(1) structure: **quasi-difference (12.54), estimate by OLS, and apply Newey–West** — *"asymptotically efficient while ensuring that our inference is valid."*

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> The vault contains **no data files**, so nothing here can be re-estimated. Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — What serial correlation actually does to $\mathrm{Var}(\hat\beta_1)$**

Consider $y_t=\beta_0+\beta_1x_t+u_t$ with $\bar x=0$, $\sigma^2=\mathrm{Var}(u_t)=1$, AR(1) errors, and the six observations

$$x=(-5,-3,-1,1,3,5)$$

**(i)** Compute $\mathrm{SST}_x$ and the usual variance formula $\sigma^2/\mathrm{SST}_x$.

**(ii)** Using (12.4), compute the true $\mathrm{Var}(\hat\beta_1)$ for $\rho=0.6$ and for $\rho=-0.6$. By what factor does the usual standard error mis-state the truth in each case?

**(iii)** Now keep $\rho=0.6$ but reorder the regressor as $x=(-5,3,-1,1,-3,5)$, so it alternates rather than trends. Recompute. What does the comparison with (ii) establish?

**(iv)** A researcher reports $t=2.4$ for $\hat\beta_1$ in an annual macro regression where both $y$ and $x$ trend upward and the residuals show $\hat\rho=.6$. What should you conclude?

> [!example]- Solution
> **(i)** $\mathrm{SST}_x=25+9+1+1+9+25=\mathbf{70}$, so the usual formula gives
> $$\frac{\sigma^2}{\mathrm{SST}_x}=\frac{1}{70}=\mathbf{0.014286}$$
>
> ---
> **(ii)** The correction term in (12.4) is $2(\sigma^2/\mathrm{SST}_x^2)\sum_{t=1}^{5}\sum_{j=1}^{6-t}\rho^{\,j}x_tx_{t+j}$.
>
> | $\rho$ | $\sum\sum\rho^{\,j}x_tx_{t+j}$ | True $\mathrm{Var}(\hat\beta_1)$ | Ratio to usual | **se ratio** |
> |---|---|---|---|---|
> | $+0.6$ | $+12.504$ | $0.019389$ | $1.357$ | $\mathbf{1.165}$ |
> | $-0.6$ | $-17.400$ | $0.007184$ | $0.503$ | $\mathbf{0.709}$ |
>
> **$\rho=+0.6$:** the true standard error is **16.5% larger** than the one OLS reports. **Reported $t$ statistics are inflated by about 16%** — a reported $t$ of $2.3$ is really $2.0$.
>
> **$\rho=-0.6$:** the usual formula **overstates** the variance — the true standard error is only 71% of the reported one. **The usual test is conservative here.**
>
> **The general statement is "biased," not "biased downward." The *usual* case is downward because $\rho>0$ is usual.**
>
> ---
> **(iii)** With the alternating $x$, $\mathrm{SST}_x$ is unchanged at $70$, but the double sum becomes $\mathbf{-18.60}$, giving a variance ratio of $\mathbf{0.469}$ — **the usual formula now *overstates* the variance, even though $\rho=+0.6$ is positive.**
>
> > **This is the point of the exercise. Positive $\rho$ is not sufficient.** Look again at the sign of the correction term:
> > $$\text{sign} \propto \text{sign}(\rho^{\,j}) \times \text{sign}(x_tx_{t+j})$$
> > **You need $\rho>0$ *and* $x_tx_{t+j}>0$ for most pairs — i.e. the *regressor* must also be positively serially correlated.** Wooldridge says exactly this: *"the independent variables in regression models are often positively correlated over time, so that $x_tx_{t+j}$ is positive for most pairs."*
> >
> > **It happens to be true in economics, which is why the downward-bias warning is a good default. It is not a theorem.**
>
> ---
> **(iv)** **Be sceptical of the $t$ statistic.** Both conditions for the bad case hold: **$\hat\rho=.6>0$, and trending regressors are strongly positively serially correlated.** The reported standard error is very likely **too small** and $t=2.4$ **too large** — significance at 5% is not established.
>
> **What to do:** (a) compute a **Newey–West standard error** with $g=1$ or $2$ (annual data); (b) since both series trend, **check $\hat\rho_1$ for a unit root** ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11 §3d]]) — trending series plus serially correlated errors is also the profile of a **spurious regression**.

---

**Exercise 2 — Choosing the right test**

For each situation, name the appropriate test for serial correlation, state what regression you would run, and say why the simpler alternatives fail.

**(i)** A static model, annual data, strictly exogenous regressors, testing for AR(1).

**(ii)** $y_t=\beta_0+\beta_1z_t+\beta_2y_{t-1}+u_t$, testing for AR(1).

**(iii)** Monthly, seasonally unadjusted data, testing for AR(3).

**(iv)** The same monthly data, testing for a purely seasonal pattern in which $u_t$ correlates with $u_{t-12}$ but adjacent errors are uncorrelated.

**(v)** In Example 12.2, the static Phillips curve gave $\hat\rho=.571$ with $n=58$. Recover $\mathrm{se}(\hat\rho)$, and check the reported $DW=.80$ against the approximation (12.22). Comment on any discrepancy.

> [!example]- Solution
> **(i)** **The $t$ test of §3a.** Regress $\hat u_t$ on $\hat u_{t-1}$, $t=2,\dots,n$; use $t_{\hat\rho}$ (one-sided $H_1:\rho>0$ is defensible a priori). **Durbin–Watson would also be valid but is inferior** — it needs normality and has an inconclusive region.
>
> ---
> **(ii)** **Durbin's alternative (§3c).** Regress
> $$\hat u_t \text{ on } \hat u_{t-1},\,z_t,\,y_{t-1}$$
> **Both the §3a $t$ test and DW are invalid — not just inefficient, but asymptotically wrong.** The lagged dependent variable is the leading violation of strict exogeneity: **$y_{t-1}$ and $u_{t-1}$ are obviously correlated**, and (12.20) ignores that correlation entirely. **Including the regressors in the auxiliary equation is what allows each $x_{tj}$ to correlate with $u_{t-1}$**, restoring the approximate $t$ distribution.
>
> ---
> **(iii)** **Breusch–Godfrey (§3d)**, $q=3$. Regress
> $$\hat u_t \text{ on } \hat u_{t-1},\hat u_{t-2},\hat u_{t-3},\,x_{t1},\dots,x_{tk}, \qquad t=4,\dots,n$$
> and take either the $F$ test for joint significance of the three lags, or $LM=(n-3)R^2_{\hat u}\overset{a}{\sim}\chi^2_3$.
>
> **Why not the AR(1) test?** It only detects correlation between **adjacent** errors. **Monthly data can easily have $u_t$ correlated with $u_{t-3}$ while $\mathrm{Corr}(u_t,u_{t-1})\approx0$**, and the AR(1) test would miss it completely.
>
> ---
> **(iv)** Regress $\hat u_t$ on $\hat u_{t-12}$ (adding the $x_{tj}$ if strict exogeneity is doubtful) — **equation (12.20) or (12.24) with $\hat u_{t-12}$ in place of $\hat u_{t-1}$.**
>
> **The AR(1) test is exactly the wrong tool by construction:** the alternative specifies $\mathrm{Corr}(u_t,u_{t-1})=0$, which is the null the AR(1) test would happily fail to reject. **And Breusch–Godfrey with $q=12$ would work but spends 12 degrees of freedom to detect a one-parameter alternative** — much less powerful than testing the single lag you actually suspect.
>
> ---
> **(v)** $\mathrm{se}(\hat\rho)=\hat\rho/t = .571/5.48=\mathbf{.104}$.
>
> **DW check:** $2(1-\hat\rho)=2(1-.571)=\mathbf{.858}$ versus the reported $DW=\mathbf{.80}$ — **close, and both far below 2, so the same conclusion follows either way.**
>
> **On the discrepancy:** (12.22) is an approximation because **$\hat\rho$'s denominator is $\sum_{t=2}^n\hat u_{t-1}^2$ while $DW$'s is $\sum_{t=1}^n\hat u_t^2$** — different sums over different ranges. **Do not expect exact agreement, especially at modest $n$.**
>
> *(The expectations-augmented model shows a larger gap: $\hat\rho=-.033$ implies $DW\approx2.066$, but $1.77$ is reported. **Both are firmly in the fail-to-reject region, so the substantive conclusion is unchanged** — which is precisely why (12.22) is described as "conceptually the same," not numerically identical.)*

---

**Exercise 3 — Computing a Newey–West standard error by hand**

An OLS regression produces `"se($\hat\beta_1$)" = 0.50` and $\hat\sigma = 2.0$. The products $\hat a_t=\hat r_t\hat u_t$ over $n=6$ periods are

$$\hat a = (1,\ 2,\ -1,\ 3,\ 1,\ -2)$$

**(i)** Compute $\sum\hat a_t^2$, $\sum_{t\ge2}\hat a_t\hat a_{t-1}$ and $\sum_{t\ge3}\hat a_t\hat a_{t-2}$.

**(ii)** Compute $\hat\nu$ for $g=0$, $g=1$ and $g=2$, and the corresponding standard errors from (12.13).

**(iii)** Verify that the $g=1$ and $g=2$ formulas (12.14) and (12.15) follow from the general formula (12.12), and explain the role of the weights $[1-h/(g+1)]$.

**(iv)** In Example 12.1, `"se" = .0402`, $\hat\sigma=.0328$, and $g=2$ gave $\hat\nu=.000805$. Reproduce the HAC standard error and $t$ statistic, and comment on the size of the correction.

**(v)** For $n=280$ (70 years of quarterly data), compute the three bandwidth rules and give the integer parts.

> [!example]- Solution
> **(i)**
> $$\textstyle\sum\hat a_t^2 = 1+4+1+9+1+4=\mathbf{20}$$
> $$\textstyle\sum_{t\ge2}\hat a_t\hat a_{t-1}=(2)(1)+(-1)(2)+(3)(-1)+(1)(3)+(-2)(1)=2-2-3+3-2=\mathbf{-2}$$
> $$\textstyle\sum_{t\ge3}\hat a_t\hat a_{t-2}=(-1)(1)+(3)(2)+(1)(-1)+(-2)(3)=-1+6-1-6=\mathbf{-2}$$
>
> ---
> **(ii)** From (12.13), $\mathrm{se}=(0.50/2.0)^2\sqrt{\hat\nu}=0.0625\sqrt{\hat\nu}$:
>
> | $g$ | $\hat\nu$ | $\mathrm{se}(\hat\beta_1)$ |
> |---|---|---|
> | $0$ (heteroskedasticity-robust only) | $20$ | $\mathbf{0.2795}$ |
> | $1$ | $20+(-2)=\mathbf{18}$ | $\mathbf{0.2652}$ |
> | $2$ | $20+\tfrac43(-2)+\tfrac23(-2)=\mathbf{16}$ | $\mathbf{0.2500}$ |
>
> **The standard errors *fall* as $g$ rises**, because both autocovariances are **negative** here. **This is the $\rho<0$ case of Exercise 1 in miniature** — HAC does not mechanically inflate standard errors; it corrects them in whichever direction the data indicate.
>
> ---
> **(iii)** At $g=1$ the only term is $h=1$ with weight $1-\tfrac12=\tfrac12$, so $2\cdot\tfrac12=1$:
> $$\hat\nu=\textstyle\sum\hat a_t^2+\sum\hat a_t\hat a_{t-1} \;\checkmark \text{ (12.14)}$$
> At $g=2$: $h=1$ has weight $1-\tfrac13=\tfrac23$ giving $2\cdot\tfrac23=\tfrac43$; $h=2$ has weight $1-\tfrac23=\tfrac13$ giving $2\cdot\tfrac13=\tfrac23$:
> $$\hat\nu=\textstyle\sum\hat a_t^2+\tfrac43\sum\hat a_t\hat a_{t-1}+\tfrac23\sum\hat a_t\hat a_{t-2} \;\checkmark \text{ (12.15)}$$
>
> **The weights (the Bartlett kernel) decline linearly in $h$ and exist to guarantee $\hat\nu\ge0$** (Newey–West 1987). **This is not optional: $\hat\nu$ estimates a variance and $\sqrt{\hat\nu}$ appears in (12.13) — a negative $\hat\nu$ would make the standard error undefined.** Equally weighting the autocovariances can produce exactly that.
>
> ---
> **(iv)**
> $$\mathrm{se}(\hat\beta_1)=\left(\frac{.0402}{.0328}\right)^2\sqrt{.000805}=(1.2256)^2(.02837)=\mathbf{.0426}$$
> $$t_{\text{HAC}}=\frac{-.2123}{.0426}=\mathbf{-4.98} \qquad\text{versus}\qquad t_{\text{usual}}=\frac{-.2123}{.0402}=-5.28$$
>
> **The correction is about 6%** ($.0426/.0402=1.060$). **The elasticity remains overwhelmingly significant.**
>
> **The lesson, read together with Example 12.3:** that equation had **strongly significant** AR(1) serial correlation ($\hat\rho=.481$, $t=2.89$), yet the standard error moved only 6%. **Significance of $\hat\rho$ tells you serial correlation exists; it does not tell you the correction will be large** — that depends on the autocorrelations of $\hat a_t=\hat r_t\hat u_t$, not of $\hat u_t$.
>
> ---
> **(v)** For $n=280$:
>
> | Rule | Value | Integer part |
> |---|---|---|
> | $4(280/100)^{2/9}$ | $5.028$ | $\mathbf{5}$ |
> | $\tfrac34(280)^{1/3}$ | $4.907$ | $\mathbf{4}$ |
> | $(280)^{1/4}$ | $4.091$ | $\mathbf{4}$ |
>
> **Compare $n=70$, where the answers were $3,3,2$.** Quadrupling the sample moves the bandwidth up by only 1–2 lags — **$g$ grows with $n$, but very slowly** (as $n^{1/3}$ or $n^{2/9}$, not $n$). **And the rules still disagree with each other, which is exactly the sensitivity Kiefer and Vogelsang's approach was designed to sidestep.**

---

**Exercise 4 — Quasi-differencing, and when FGLS is worse than OLS**

**(i)** Derive the quasi-differencing transformation for $y_t=\beta_0+\beta_1x_t+u_t$ with $u_t=\rho u_{t-1}+e_t$, and explain why the transformed intercept is $(1-\rho)\beta_0$.

**(ii)** Why must the first observation be multiplied by $(1-\rho^2)^{1/2}$ rather than simply included? Compute the weight for $\hat\rho=.293$ (Example 12.5) and $\hat\rho=.781$ (Example 12.6), and say which sample loses more from Cochrane–Orcutt.

**(iii)** State condition (12.41) and give two economic situations that violate it.

**(iv)** In Example 12.6 the $unem$ coefficient is $+0.468$ (OLS) and $-0.716$ (PW). By the decision rule of §4c this large divergence is a *warning sign*. Yet Wooldridge prefers PW. Reconcile these.

**(v)** A model has $y_t=\beta_0+\beta_1y_{t-1}+u_t$ with $\beta_0=2$, $\beta_1=.5$, and $u_t=.4u_{t-1}+e_t$. Rewrite it as an AR(2), check stability, and say what you should have estimated in the first place.

> [!example]- Solution
> **(i)** Write the equation at $t$ and at $t-1$, multiply the second by $\rho$, and subtract:
> $$\begin{aligned} y_t &= \beta_0+\beta_1x_t+u_t\\ \rho y_{t-1} &= \rho\beta_0+\rho\beta_1x_{t-1}+\rho u_{t-1}\\[2pt] \hline y_t-\rho y_{t-1} &= (1-\rho)\beta_0+\beta_1(x_t-\rho x_{t-1})+\underbrace{(u_t-\rho u_{t-1})}_{=\,e_t}\end{aligned}$$
> **The error is now $e_t$, which is serially uncorrelated** — the transformed equation satisfies all the Gauss–Markov assumptions.
>
> **The intercept becomes $(1-\rho)\beta_0$ because the constant is quasi-differenced too:** the "regressor" attached to $\beta_0$ is the constant 1 in both periods, and $1-\rho\cdot1=1-\rho$. **So divide the estimated intercept by $(1-\rho)$ to recover $\beta_0$.**
>
> ---
> **(ii)** Period 1 has no predecessor to difference against, so it enters as $y_1=\beta_0+\beta_1x_1+u_1$ — but
> $$\mathrm{Var}(u_1)=\frac{\sigma_e^2}{1-\rho^2} > \sigma_e^2 = \mathrm{Var}(e_t)$$
> **Appending it raw would make the pooled equation heteroskedastic**, destroying the Gauss–Markov property we just bought. Multiplying by $(1-\rho^2)^{1/2}$ gives $\mathrm{Var}(\tilde u_1)=(1-\rho^2)\cdot\sigma_e^2/(1-\rho^2)=\sigma_e^2$ — **exactly matched.**
>
> | Example | $\hat\rho$ | $(1-\hat\rho^2)^{1/2}$ |
> |---|---|---|
> | 12.5 (barium) | $.293$ | $\mathbf{0.956}$ |
> | 12.6 (Phillips) | $.781$ | $\mathbf{0.625}$ |
>
> **Neither loses "more" in the sense of a bigger sample-size cost** — CO drops exactly one observation either way (about 2% of Example 12.6's $n=49$).
>
> **But the *informational* loss is larger when $\rho$ is small.** At $\hat\rho=.293$ the first observation carries almost full weight ($0.956$) in PW, so **dropping it discards nearly a whole observation's worth of information.** At $\hat\rho=.781$ it enters with weight $0.625$ — **already heavily downweighted, so CO discards less.** *(This is intuitive: the more persistent the errors, the less independent information the first observation contains.)*
>
> ---
> **(iii)** $$\mathrm{Cov}\big[(x_{t-1}+x_{t+1}),\,u_t\big]=0 \tag{12.41}$$
> Practically, **$u_t$ must be uncorrelated with $x_{t-1}$, $x_t$ and $x_{t+1}$** — a strict-exogeneity-flavoured condition that OLS never requires.
>
> **Two violations:**
> 1. **$x$ has a lagged effect on $y$.** If $x_{t-1}$ genuinely belongs in the equation but was omitted, it sits in $u_t$ — so $\mathrm{Cov}(x_{t-1},u_t)\ne0$.
> 2. **Feedback: $x_{t+1}$ reacts to $u_t$.** A policy variable responding to this period's shock — money growth responding to an inflation surprise, a central bank reacting to output. **[[11 - Further Issues in Using OLS with Time Series Data|Ch. 11]] went to considerable trouble to make OLS valid under exactly this feedback; FGLS throws that away.**
>
> ---
> **(iv)** **Both readings are live, and Wooldridge is explicit that the case is difficult.**
>
> **The §4c warning applies in general:** a large divergence *can* mean (12.41) fails, leaving OLS consistent and FGLS inconsistent. **You cannot tell from the estimates alone** — formally testing the difference needs Hausman (1978).
>
> **But three specific facts tip the balance toward PW here:**
> 1. **The OLS estimate has the wrong sign.** A *positive* inflation–unemployment relation contradicts the theory the regression exists to test.
> 2. **$\hat\rho=.781$ makes quasi-differencing close to first differencing**, and the PW estimates are *"fairly close to what is obtained by first differencing both $inf$ and $unem$."* **Two different corrections agreeing is real evidence.**
> 3. **A unit root is the more likely explanation than a failure of (12.41).** If $inf$ or $unem$ is I(1), OLS in levels loses its usual properties anyway (ch. 18) — and **FGLS, being near-differencing, approximately eliminates the unit root.**
>
> > **The reconciliation: the §4c warning is about *strict exogeneity failure* as the cause of divergence. Here the likelier cause is *non-stationarity*, and the fix for that happens to be what PW is doing.** The honest summary is Wooldridge's own: *"it may just be that $inf$ and $unem$ are not related in levels, but they have a negative relationship in first differences."*
>
> ---
> **(v)** Substitute $u_{t-1}=y_{t-1}-\beta_0-\beta_1y_{t-2}$ into $u_t=\rho u_{t-1}+e_t$:
> $$y_t=\underbrace{\beta_0(1-\rho)}_{\alpha_0}+\underbrace{(\beta_1+\rho)}_{\alpha_1}y_{t-1}\underbrace{-\rho\beta_1}_{\alpha_2}y_{t-2}+e_t$$
> With $\beta_0=2$, $\beta_1=.5$, $\rho=.4$:
> $$\alpha_0=2(0.6)=\mathbf{1.2},\qquad \alpha_1=.5+.4=\mathbf{0.9},\qquad \alpha_2=-(.4)(.5)=\mathbf{-0.2}$$
>
> **Stability check** ($\rho_2>-1$; $\rho_2-\rho_1<1$; $\rho_1+\rho_2<1$):
> $$-0.2>-1\ ✅ \qquad -0.2-0.9=-1.1<1\ ✅ \qquad 0.9-0.2=0.7<1\ ✅ \quad\Rightarrow\ \textbf{stable}$$
>
> **What you should have estimated: $y_t$ on $y_{t-1}$ and $y_{t-2}$, by OLS.** That regression is consistent and asymptotically normal, and $\mathbb{E}(y_t\mid y_{t-1},y_{t-2},\dots)=\alpha_0+\alpha_1y_{t-1}+\alpha_2y_{t-2}$ is **the conditional expectation you actually want** — for forecasting or anything else.
>
> **The general moral:** *"you need a good reason for having both a lagged dependent variable in a model and a particular model of serial correlation in the errors."* **Serial correlation in a dynamic model usually just means a lag is missing. Add it rather than modelling the error.**

---

**Exercise 5 — ARCH, the EMH, and what "robust" covers**

**(i)** In Example 12.8, the BP regression of $\hat u_t^2$ on $return_{t-1}$ gave a coefficient of $-1.104$ with $\mathrm{se}=.201$, $n=689$, $R^2=.042$. Compute the $t$ statistic and the LM statistic, and interpret the **sign**.

**(ii)** In Example 12.9, regressing $\hat u_t^2$ on $\hat u_{t-1}^2$ gave $2.95+0.337\hat u_{t-1}^2$ with $\mathrm{se}(\hat\alpha_1)=.036$, while regressing $\hat u_t$ on $\hat u_{t-1}$ gave $\hat\rho=.0014$ with $t=.038$. **State plainly what these two results say together**, and compute the predicted conditional variance after a quiet week ($\hat u_{t-1}^2\approx0$) versus a $\pm5\%$ surprise.

**(iii)** Does ARCH invalidate the EMH test of Example 11.4? Does it invalidate OLS?

**(iv)** A researcher has time series residuals showing **both** heteroskedasticity and serial correlation, and reports heteroskedasticity-robust standard errors. What is wrong, and what should they do?

**(v)** Why must you test for serial correlation *before* testing for heteroskedasticity, and not the other way round?

> [!example]- Solution
> **(i)** $$t=\frac{-1.104}{.201}=\mathbf{-5.49}, \qquad LM=nR^2=689(.042)=\mathbf{28.94}\ \overset{a}{\sim}\ \chi^2_1$$
> against a 5% critical value of $3.84$ — $p<10^{-7}$. **Overwhelming evidence of heteroskedasticity.**
>
> **The sign is the interesting part.** The coefficient on $return_{t-1}$ is **negative**: **a high return last week predicts *lower* volatility this week; a bad week predicts higher volatility.** *"The expected value of stock returns does not depend on past returns, but the variance of returns does."*
>
> ---
> **(ii)** $$t_{\hat\alpha_1}=\frac{.337}{.036}=\mathbf{9.36} \qquad\text{versus}\qquad t_{\hat\rho}=\mathbf{0.038}$$
>
> > **The residuals are serially uncorrelated. Their squares are massively autocorrelated.**
> >
> > **Returns are unpredictable in level — exactly as the EMH claims — but highly predictable in volatility.**
>
> That is not a contradiction: **the EMH is a statement about the conditional *mean*, and says nothing about the conditional *variance*.** This pair of findings is the empirical foundation of ARCH/GARCH modelling in finance.
>
> **Predicted conditional variance** from $\hat u_t^2=2.95+0.337\hat u_{t-1}^2$:
>
> | Last week | $\hat u_{t-1}^2$ | Predicted $\mathrm{Var}(u_t)$ |
> |---|---|---|
> | Quiet | $\approx0$ | $\mathbf{2.95}$ |
> | $\pm5\%$ surprise | $25$ | $2.95+.337(25)=\mathbf{11.38}$ |
>
> **Nearly a fourfold increase — and the sign of the surprise is irrelevant, only its magnitude.** *(For reference, the implied unconditional variance is $\hat\alpha_0/(1-\hat\alpha_1)=2.95/.663=4.45$, and $\hat\alpha_1=.337<1$ satisfies the stability condition.)*
>
> ---
> **(iii)** **No to both, but for different reasons.**
>
> **OLS is fine.** ARCH is *"just one particular form of heteroskedasticity,"* and heteroskedasticity never affects unbiasedness (Theorem 10.1) or consistency (Theorem 11.1). Moreover **static and distributed lag models with ARCH errors satisfy TS.1′–TS.5′**, so the usual OLS statistics are asymptotically valid.
>
> **The EMH conclusion stands**, though the *justification* needs amending. [[11 - Further Issues in Using OLS with Time Series Data|Ch. 11]]'s Example 11.4 explicitly assumed $\mathrm{Var}(return_t\mid return_{t-1})=\sigma^2$ — **which Examples 12.8 and 12.9 demolish.** **The repair is trivial: use heteroskedasticity-robust standard errors, which are valid for any form of heteroskedasticity including ARCH.**
>
> **What you *could* gain:** WLS based on estimating (12.50), or maximum likelihood under conditional normality, would be **asymptotically more efficient** than OLS. And if the conditional variance is itself of interest — as it is for anyone pricing options — **ARCH is the model, not a nuisance.**
>
> ---
> **(iv)** **Heteroskedasticity-robust standard errors do not fix serial correlation.**
>
> The [[08 - Heteroskedasticity|ch. 08]] adjustments are valid in time series **only under TS.1′, TS.2′, TS.3′ *and TS.5′*** — and TS.5′ is precisely the assumption that has failed. *"Serially correlated errors cause problems that adjustments for heteroskedasticity are not able to address."*
>
> Concretely, in the HAC formula this amounts to using $g=0$: **keeping only $\sum\hat a_t^2$ and dropping every autocovariance term** — the terms that exist to handle serial correlation. **Since serial correlation is usually the larger of the two problems for standard errors, the correction is aimed at the wrong target.**
>
> **What to do — either:**
> - **OLS with fully robust HAC (Newey–West) standard errors** — handles both at once, needs only contemporaneous exogeneity. **The default.**
> - **Or**, if strict exogeneity is credible and efficiency matters: CO/PW quasi-differencing, then **heteroskedasticity-robust standard errors on the transformed equation** — or the combined WLS + AR(1) procedure (12.52)–(12.54), then Newey–West on top for safety.
>
> ---
> **(v)** **Because serial correlation invalidates the heteroskedasticity tests, but not vice versa.**
>
> Look at the BP auxiliary equation
> $$u_t^2=\delta_0+\delta_1x_{t1}+\cdots+\delta_kx_{tk}+v_t$$
> **The $F$ (or LM) test requires $\{v_t\}$ to be homoskedastic *and serially uncorrelated*.** If the $u_t$ are serially correlated, so are the $u_t^2$ — **so $\{v_t\}$ is serially correlated, and the test statistic has the wrong distribution.** The same applies to the White test.
>
> **The correct order:**
> 1. **Test for serial correlation** (use a **heteroskedasticity-robust** version of the test if heteroskedasticity is suspected — that direction of robustness *is* available)
> 2. **Correct it** (HAC, or quasi-differencing)
> 3. **Then test for heteroskedasticity** in the corrected equation
>
> **Note the asymmetry that makes this work: a serial correlation test can be made heteroskedasticity-robust, but a heteroskedasticity test cannot be made serial-correlation-robust.** That is what fixes the order.
>
> *(A further wrinkle: assuming $\{v_t\}$ is serially uncorrelated **rules out ARCH by assumption** — so a standard BP test is not the right tool for detecting dynamic heteroskedasticity. **Regress $\hat u_t^2$ on its own lags instead**, as Example 12.9 does.)*

---

## 📝 Summary

- **Serial correlation does not bias or make OLS inconsistent.** Theorem 10.1 (unbiasedness under strict exogeneity) and Theorem 11.1 (consistency under contemporaneous exogeneity + weak dependence) **assume nothing about $\mathrm{Cov}(u_t,u_s)$.** What breaks is **efficiency (OLS is no longer BLUE) and inference (standard errors, $t$, $F$, LM are invalid, even asymptotically).**
- **The usual OLS standard errors are typically *too small*.** From (12.4), the ignored term $\sum\sum\rho^{\,j}x_tx_{t+j}$ is positive when **both** $\rho>0$ **and** the regressor is positively serially correlated — the normal state of economic data. **Result: inflated $t$ statistics and over-rejection.** With $\rho<0$ the sign is indeterminate; **"biased" is guaranteed, "biased downward" is merely usual.**
- **$R^2$ and $\bar R^2$ remain consistent** for the population $R^2=1-\sigma_u^2/\sigma_y^2$ under stationarity and weak dependence. **They fail only if $y_t$ is I(1)**, where $\mathrm{Var}(y_t)$ grows and goodness of fit is meaningless.
- **"OLS is inconsistent with a lagged dependent variable and serially correlated errors" is false as stated.** If the model is the conditional expectation $\mathbb{E}(y_t\mid y_{t-1})$, OLS is consistent even with serially correlated errors. **Inconsistency requires additionally assuming the errors follow an AR(1) — and then the model is really an AR(2), which is what you should estimate.**
- **HAC / Newey–West standard errors** are the modern default because **they need only contemporaneous exogeneity.** Compute $\hat a_t=\hat r_t\hat u_t$ from the auxiliary regression, form $\hat\nu=\sum\hat a_t^2+2\sum_{h=1}^g[1-h/(g+1)]\sum\hat a_t\hat a_{t-h}$, then $\mathrm{se}=[\text{“se''}/\hat\sigma]^2\sqrt{\hat\nu}$. **The Bartlett weights guarantee $\hat\nu\ge0$; setting $g=0$ recovers the ordinary heteroskedasticity-robust standard error.** Bandwidth: $g=1{-}2$ annual, $4{-}8$ quarterly, $12{-}24$ monthly.
- **Testing, in order of generality:** the **$t$ test** on $\hat u_t$ vs $\hat u_{t-1}$ (**strictly exogenous regressors only**); **Durbin–Watson**, $DW\approx2(1-\hat\rho)$ (**needs normality, has an inconclusive region — largely superseded**); **Durbin's alternative**, adding the $x_{tj}$ to the auxiliary regression (**valid with lagged $y$**); **Breusch–Godfrey**, $LM=(n-q)R^2_{\hat u}\overset{a}{\sim}\chi^2_q$ (**AR($q$), and seasonal versions by using $\hat u_{t-s}$**).
- **Correcting by GLS requires *strict* exogeneity.** Quasi-difference: $\tilde y_t=y_t-\rho y_{t-1}$, $\tilde x_t=x_t-\rho x_{t-1}$, intercept $(1-\rho)\beta_0$; weight the first observation by $(1-\rho^2)^{1/2}$ to equalise variances. **Cochrane–Orcutt drops observation 1; Prais–Winsten keeps it.** Feasible GLS plugs in $\hat\rho$ from (12.20): **consistent and asymptotically more efficient than OLS, but no longer unbiased or BLUE.**
- **A large OLS/FGLS divergence is a warning, not a vindication of FGLS.** FGLS additionally needs $\mathrm{Cov}[(x_{t-1}+x_{t+1}),u_t]=0$ — **so a lagged effect of $x$ on $y$, or feedback from $u_t$ to $x_{t+1}$, makes FGLS *inconsistent* while OLS remains consistent.**
- **Getting the serial correlation model wrong does not cause inconsistency.** > *Exogeneity of the explanatory variables is what matters for consistency, not the serial correlation or variance properties of the errors.* **The fix for wrong-model risk: quasi-difference, estimate by OLS, and apply Newey–West to the transformed equation** — efficient if the model is right, valid if it is wrong.
- **Differencing kills serial correlation as well as unit roots.** If $u_t$ is a random walk, $\Delta u_t$ is i.i.d.; even for large positive $\rho$, differencing removes most of the correlation. **But $\Delta y$ on $\Delta x$ is a different model from $y$ on $x$.**
- **Heteroskedasticity in time series:** the ch. 08 tools apply, **but only if the errors are not serially correlated — so test for serial correlation first.** **ARCH** ($\mathbb{E}(u_t^2\mid u_{t-1})=\alpha_0+\alpha_1u_{t-1}^2$) makes the **squared** errors autocorrelated while the errors themselves are not — **volatility clustering.** OLS stays consistent and heteroskedasticity-robust statistics stay valid; **the gains from modelling ARCH are efficiency, and the conditional variance itself.**

---

## ⚠️ Important Notes

> [!warning] The whole course reduces to one sentence, and it is in this chapter
> > **Exogeneity of the explanatory variables is what matters for consistency, not the serial correlation or variance properties of the errors.**
>
> | Assumption that fails | What is lost | What survives |
> |---|---|---|
> | **Zero conditional mean** (MLR.4 / TS.3 / TS.3′) | **Consistency — the coefficients are wrong** | Nothing worth having |
> | **Homoskedasticity** (MLR.5 / TS.4 / TS.4′) | Efficiency; **valid standard errors** | **Unbiasedness, consistency** |
> | **No serial correlation** (TS.5 / TS.5′) | Efficiency; **valid standard errors** | **Unbiasedness, consistency** |
>
> **First-moment failures are fatal. Second-moment failures are inconvenient.** Every remedy in [[08 - Heteroskedasticity|ch. 08]] and ch. 12 is about the bottom two rows.

> [!warning] Serial correlation flatters you; heteroskedasticity is merely unreliable
> **Heteroskedasticity** could push the usual standard errors either way. **Serial correlation, in the typical economic case ($\rho>0$, regressors positively autocorrelated), reliably makes them too small.**
>
> **So the usual $t$ statistics are systematically too big, and you over-reject.** *"We will tend to think the OLS slope estimator is more precise than it actually is."*
>
> **Practical consequence: an impressive $t$ statistic in an uncorrected time series regression is weak evidence.** See Example 12.5, where the event-study effect fell from $t=-1.98$ to $t=-1.69$ once serial correlation was accounted for — **crossing the 5% line in the wrong direction.**

> [!warning] "Robust" is not one thing — check *what* it is robust to
> | Standard error | Robust to heteroskedasticity | Robust to serial correlation |
> |---|---|---|
> | Usual OLS | ❌ | ❌ |
> | Heteroskedasticity-robust (White) | ✅ | **❌** |
> | **HAC / Newey–West** | ✅ | ✅ |
>
> **Reporting heteroskedasticity-robust standard errors in a time series regression with serially correlated errors fixes nothing** — and since serial correlation usually has the larger effect, it fixes the *smaller* problem. **In HAC terms this is $g=0$: exactly the terms that handle serial correlation, discarded.**

> [!warning] Significance of $\hat\rho$ does not predict the size of the correction
> **Example 12.3:** $\hat\rho=.481$, $t=2.89$ — strong, highly significant AR(1) serial correlation.
> **Example 12.1, same equation:** the HAC standard error was **6% larger** than the usual one.
>
> **These are not in tension.** What inflates $\mathrm{Var}(\hat\beta_1)$ is $\sum\sum\rho^{\,j}x_tx_{t+j}$ — **it depends on the autocorrelations of $\hat a_t=\hat r_t\hat u_t$, not of $\hat u_t$ alone.** *"It is possible to have substantial serial correlation in $\{u_t\}$ but to also have similarities in the usual and SC-robust standard errors of some coefficients."*
>
> **So: test to learn whether serial correlation exists; compute HAC to learn whether it matters. They are different questions.**

> [!warning] A big OLS/FGLS gap is a red flag, not a victory for FGLS
> The instinct — *"the estimates moved a lot, so the correction was important"* — is **backwards**. FGLS needs $\mathrm{Cov}[(x_{t-1}+x_{t+1}),u_t]=0$ **on top of** what OLS needs. **A large gap may mean that condition fails, in which case OLS is consistent and FGLS is not.**
>
> | Situation | Prefer |
> |---|---|
> | Estimates similar, serial correlation present | **FGLS** (more efficient, valid statistics) |
> | Estimates substantially different | **OLS + HAC** — investigate why |
>
> **The two structural culprits: $x$ having a lagged effect on $y$, and $x_{t+1}$ reacting to $u_t$.** *"If $x$ has a lagged effect on $y$, or $x_{t+1}$ reacts to changes in $u_t$, FGLS can produce misleading results."*
>
> *(Example 12.6 is the instructive exception — there the divergence traces to **non-stationarity**, not to (12.41), and PW's near-differencing is the appropriate response. Diagnose the cause before choosing.)*

> [!warning] Never compare the OLS $R^2$ with the Prais–Winsten $R^2$
> In Table 12.1: OLS $R^2=.305$, PW $R^2=.202$. **This is not a deterioration in fit.**
>
> **The OLS $R^2$ is computed from untransformed variables; the PW $R^2$ comes from the final regression of *quasi-differenced* variables on *quasi-differenced* variables.** They measure different things — *"it is not clear what this $R^2$ is actually measuring; nevertheless, it is traditionally reported."*
>
> **Same trap as comparing $R^2$ across different dependent variables** ($y$ vs $\log y$, levels vs differences) — see [[06 - Multiple Regression Analysis - Further Issues|ch. 06 §3]].

> [!warning] Test for serial correlation *before* heteroskedasticity — the order is not arbitrary
> **Serial correlation invalidates BP and White; heteroskedasticity does not invalidate the serial correlation tests** (they can be made heteroskedasticity-robust). **That asymmetry fixes the order:**
>
> $$\text{serial correlation test (het-robust)} \to \text{correct} \to \text{heteroskedasticity test}$$
>
> **And note what the standard BP setup assumes away:** requiring $\{v_t\}$ in $u_t^2=\delta_0+\delta_1x_{t1}+\cdots+v_t$ to be serially uncorrelated **rules out ARCH by construction.** **To detect ARCH, regress $\hat u_t^2$ on its own lags** (Example 12.9), not on the $x_{tj}$.

> [!warning] The Durbin–Watson statistic is mostly of historical interest
> **Its one advantage — an exact tabulated distribution — costs the full CLM assumptions including normality, and buys an inconclusive region** (at 5%, $n=45$, $k=4$: anything in $[1.336,\,1.720]$ gives no answer).
>
> **The $t$ test from (12.20) is simpler, asymptotically valid without normality, valid under heteroskedasticity in the $x_{tj}$, and trivially made fully heteroskedasticity-robust.** *"The practical disadvantages of the DW statistic are substantial."*
>
> **And neither is valid without strict exogeneity — with a lagged dependent variable, use Durbin's alternative (12.24).** **Reporting a DW statistic for a model containing $y_{t-1}$ is a straightforward error.**

> [!warning] Applying HAC *after* FGLS is correct, not redundant
> It looks contradictory — CO/PW exist to remove serial correlation, so why compute serial-correlation-robust standard errors on the result? **Because the AR(1) model is almost certainly not exactly right.**
>
> **If $\{u_t\}$ is really AR(2) and you fit AR(1), the transformed errors have their own complicated correlation structure.** The quasi-differenced equation is still estimated by OLS, so **Newey–West applies directly to it.**
>
> **You get both: the efficiency gain from partially modelling the serial correlation, and valid inference despite the model being wrong.** *"The careful researcher readily admits that the AR(1) structure could be incorrect... and, therefore, conducts inference that is fully robust."* **Same principle as WLS-with-imperfect-variance-function plus robust standard errors in [[08 - Heteroskedasticity|ch. 08 §4c]].**

> [!warning] ARCH is about the variance, so it cannot refute the EMH
> The EMH constrains $\mathbb{E}(return_t\mid \text{past})$. **ARCH describes $\mathrm{Var}(return_t\mid\text{past})$. They are compatible, and empirically both hold.**
>
> Example 12.9 is the cleanest possible demonstration: **$t_{\hat\rho}=0.038$ on the residuals, $t_{\hat\alpha_1}=9.36$ on the squared residuals.**
>
> **But Example 11.4's stated justification does need repair.** It assumed $\mathrm{Var}(return_t\mid return_{t-1})=\sigma^2$ (TS.4′) to license the $F$ test — **and that assumption is comprehensively false.** **The conclusion survives; the argument needs heteroskedasticity-robust statistics.** *(A caveat worth carrying: a robust conclusion reached by a broken argument is still a broken argument.)*

> [!note] Cross-subject connections
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — **the natural sequel.** ARMA modelling, the ACF/PACF diagnostics that generalise $\hat\rho_1$, and GARCH are all developed properly there. **The AR(1) error model of §4 is the $p=1$ case; Breusch–Godfrey is the regression counterpart of the Ljung–Box test.**
> - [[08 - Heteroskedasticity|Ch. 08]] — **the structural twin.** Consequences → robust inference → tests → FGLS, in the same order, with the same conclusion: **second-moment problems cost inference, never consistency.** §6d literally bolts the two chapters together.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — the LM/score test behind Breusch–Godfrey, and the GLS/efficiency arguments.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **HAC standard errors are the econometric answer to a problem ML usually ignores: correlated observations make naive uncertainty estimates too confident.** The same issue drives blocked cross-validation for time series and cluster-robust inference for grouped data.
> - [[MLOps/contents/00-Index|MLOps]] — **ARCH is a formal model of what monitoring calls *volatility regimes*:** prediction error variance that is itself predictable from recent error magnitudes. Drift alarms calibrated on constant variance will fire in clusters.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Numbers in the source that do not fully reconcile:**
> - **The $DW\approx2(1-\hat\rho)$ approximation is looser than the text's "often pretty close" suggests.** For the expectations-augmented Phillips curve, $\hat\rho=-.033$ implies $DW\approx\mathbf{2.066}$, but $\mathbf{1.77}$ is reported — a gap of $0.30$. (The static curve is closer: $2(1-.571)=.858$ against a reported $.80$.) **Wooldridge explains the source of the discrepancy — the two statistics have different denominators — but does not quantify it.** Both conclusions are unaffected, since both statistics fall on the same side of every critical value. **The reconciliation in Exercise 2(v) is my own arithmetic.**
> - **Example 12.4's $p$-value of $.028$ for the seasonal test** is reported without the corresponding $t$ statistic or standard error, so it cannot be checked. Same for the *"with regressors"* variant ($\hat\rho_{12}=-.170$, $p=.052$).
> - **Table 12.1 and Table 12.2 report no $t$ statistics** — every $t$ quoted in these notes is my own arithmetic from the printed coefficients and standard errors. **The one $t$ the text does state, $t_{afdec6}=-1.69$ for Prais–Winsten, matches my computation of $-0.577/0.342=-1.687$.**
> - **Example 12.1's $\hat\nu=.000805$ is quoted, not derived** — reproducing it would require the `PRMINWGE` data. **The standard error and $t$ statistic computed from it ($.0426$, $-4.98$) both match the text.**
>
> **A typographical error in the source:** on p. 415 the text reads *"just as we can apply Newey-West to (12.37), we can do the same after estimating (12.38) by OLS."* **Equations (12.37) and (12.38) are the first-observation transformation and the multiple-regressor quasi-differenced equation** — neither is the differenced equation (12.44) under discussion. **The intended references are almost certainly (12.43) and (12.44).** The surrounding argument is clear regardless.
>
> **A minor inconsistency:** §6d refers the reader to *"fully robust standard errors, as described in Section 12-5."* **HAC standard errors are described in §12-2**; §12-5 is on differencing.
>
> **Notation mangled by the two-column PDF layout** (all transcribed by hand against the numbered equations): `b^ 1` for $\hat\beta_1$, `r^` for $\hat\rho$, `n^` for $\hat\nu$, `a^t` for $\hat a_t$, `u^t` for $\hat u_t$, `y|t` and `x|t` for the quasi-differenced $\tilde y_t,\tilde x_t$, `s2 e` for $\sigma_e^2$, `Ts.5r` for TS.5′, `2.716` for $-0.716$ (the minus sign renders as `2` throughout — **every negative coefficient in these notes has been sign-checked against the surrounding text**), `x2 q` for $\chi^2_q$, `"ht` for $\sqrt{h_t}$, `nt` for $v_t$.
>
> **The two-column layout also fragments Tables 12.1 and 12.2**, interleaving coefficients and standard errors in a single column. **Both tables have been reassembled by hand**; the pairing is unambiguous because each standard error follows its coefficient in parentheses.
>
> **All regressions are quoted as printed** — the vault has no data files, so `PRMINWGE`, `PHILLIPS`, `BARIUM`, `INTDEF` and `NYSE` cannot be re-estimated. **Every derived statistic in these notes ($t$ ratios, LM statistics, $p$-values, the HAC standard error, the AR(2) reparameterisation, the stability checks) has been recomputed and agrees with the text wherever the text states a value.**

#econometrics #time-series #serial-correlation #newey-west #arch #gls
