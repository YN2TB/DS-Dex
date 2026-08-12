---
subject: Econometrics
chapter: 11
tags: [ds, econometrics, time-series, stationarity, weak-dependence, unit-root, asymptotics]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 11 (pp. 366–393)"
---

# Further Issues in Using OLS with Time Series Data

> [!abstract] What this chapter is for
> [[10 - Basic Regression Analysis with Time Series Data|Chapter 10]] gave the **finite-sample** theory for time series: under TS.1–TS.6, OLS is unbiased, BLUE, and the $t$ and $F$ statistics are exact. **But TS.3 (strict exogeneity) is brutal** — and this chapter opens by proving that *any* model with a lagged dependent variable **must** violate it.
>
> So we redo the whole thing asymptotically, exactly as [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] did for cross-sections. **But there is a new obstacle.** In ch. 05, random sampling handed us the LLN and the CLT for free. Here the observations are **correlated across time**, and the limit theorems only apply if that correlation **dies out fast enough as observations get further apart.**
>
> **That condition has a name — weak dependence — and it is the whole chapter.**
>
> | § | Topic | The one thing to take away |
> |---|---|---|
> | **1** | **Stationarity** and **weak dependence** | Two *different* ideas that get confused constantly |
> | **2** | **TS.1′–TS.5′** and the asymptotic theorems | Buy: lagged $y$ allowed. Pay: unbiasedness → consistency only |
> | **3** | **Highly persistent series**, unit roots, **I(0) vs I(1)** | If $\hat\rho_1 > .9$, **difference it** |
> | **4** | **Dynamic completeness** | Complete dynamics $\Rightarrow$ no serial correlation |
> | **5** | Homoskedasticity for time series | Whatever is on the right-hand side, $\mathrm{Var}(y_t\mid\cdot)$ must not depend on it |

---

## 📘 Main Knowledge

### 1. Stationary and weakly dependent time series

These are the two properties a time series needs before the standard asymptotic machinery applies. **They are logically independent of each other** — that is the single most-missed point in the chapter.

#### 1a. Stationarity

> [!important] Strict stationarity
> The process $\{x_t : t=1,2,\dots\}$ is **stationary** if for every collection of indices $1 \le t_1 < t_2 < \cdots < t_m$, the joint distribution of
> $$(x_{t_1}, x_{t_2}, \dots, x_{t_m})$$
> is **the same** as the joint distribution of
> $$(x_{t_1+h}, x_{t_2+h}, \dots, x_{t_m+h}) \qquad \text{for all integers } h \ge 1.$$
>
> **In words: shifting the whole sequence forward in time changes nothing about its probability structure.**

Two consequences worth spelling out:

- Take $m=1$: **every $x_t$ has the same distribution.** The sequence is identically distributed.
- Take $m=2$: the joint distribution of $(x_1,x_2)$ equals that of $(x_t,x_{t+1})$ for any $t$.

> [!warning] Stationarity does *not* mean independence
> It places **no restriction whatsoever** on how strongly $x_t$ and $x_{t+1}$ are related — they may be correlated $0.999$. It requires only that **the nature of that correlation is the same in every time period.**
>
> This is precisely why stationarity alone is not enough, and why §1b exists.

A process that is not stationary is **nonstationary**. Detecting stationarity is genuinely hard, because it is a property of the **underlying process**, not of the single realization we observe (see [[10 - Basic Regression Analysis with Time Series Data#1. The nature of time series data|ch. 10 §1]] on realizations). But some cases are obvious: **anything with a time trend is nonstationary** — at a minimum its mean changes over time.

#### 1b. Covariance stationarity

A weaker, purely second-moment version. Requires a finite second moment $\mathbb{E}(x_t^2) < \infty$.

> [!important] Covariance stationary
> $\{x_t\}$ is **covariance stationary** if
>
> 1. $\mathbb{E}(x_t)$ is constant;
> 2. $\mathrm{Var}(x_t)$ is constant;
> 3. for any $t, h \ge 1$, $\mathrm{Cov}(x_t, x_{t+h})$ **depends only on $h$, not on $t$.**
>
> Condition (iii) immediately implies $\mathrm{Corr}(x_t, x_{t+h})$ also depends only on $h$.

**The relationship between the two:**

$$\text{strict stationarity} + \text{finite 2nd moment} \;\Longrightarrow\; \text{covariance stationarity}$$

**but the converse is false.** Covariance stationarity constrains only the first two moments; strict stationarity constrains the entire joint distribution.

> [!note] Terminology in these notes
> Following Wooldridge, **"stationary" always means the strict form.** When only the second-moment version is meant, it is said explicitly.

**Why do we care at all?** Two reasons, one technical and one practical:

- **Technical:** stationarity simplifies statements of the LLN and CLT.
- **Practical — and this is the real reason:** regression analysis needs *some* stability over time. **If the relationship between $y_t$ and $x_t$ were allowed to change arbitrarily each period, a single realization could tell us nothing.** Writing down a model with fixed $\beta_j$ is *already* assuming a form of stationarity.

#### 1c. Weak dependence

> [!important] Weak dependence
> A stationary process $\{x_t\}$ is **weakly dependent** if $x_t$ and $x_{t+h}$ are "almost independent" as $h \to \infty$.
>
> For a **covariance stationary** process this can be made concrete: it is weakly dependent if
> $$\mathrm{Corr}(x_t, x_{t+h}) \to 0 \quad \text{sufficiently quickly as } h \to \infty.$$
> Such sequences are called **asymptotically uncorrelated**.

> [!warning] There is no single formal definition
> Wooldridge is explicit: *"We cannot formally define weak dependence because there is no definition that covers all cases of interest."* Many specific formalisations exist (mixing conditions), all beyond an introductory course. **An intuitive grasp is what is being examined.**

**Why it matters — the one-sentence answer:**

> [!important] Weak dependence replaces random sampling
> In [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]], random sampling delivered the LLN and CLT. **Here, weak dependence does that job.** The best-known time series CLT requires **stationarity plus weak dependence** — so *stationary, weakly dependent series are the ideal input to a time series regression.*
>
> Series that are **not** weakly dependent (§3) generally **do not satisfy a CLT**, which is exactly why using them in regressions is treacherous.

##### Example 1: MA(1) — moving average of order one

$$\boxed{x_t = e_t + \alpha_1 e_{t-1}, \qquad t = 1, 2, \dots}$$

where $\{e_t\}$ is i.i.d. with mean zero and variance $\sigma_e^2$. **$x_t$ is a weighted average of this period's and last period's shock.** (Setting the coefficient on $e_t$ to 1 costs nothing — it is a normalisation.)

Work out the correlations:

$$\mathrm{Var}(x_t) = (1+\alpha_1^2)\sigma_e^2$$
$$\mathrm{Cov}(x_t, x_{t+1}) = \mathrm{Cov}(e_t + \alpha_1 e_{t-1},\; e_{t+1}+\alpha_1 e_t) = \alpha_1\mathrm{Var}(e_t) = \alpha_1\sigma_e^2$$

$$\boxed{\mathrm{Corr}(x_t, x_{t+1}) = \frac{\alpha_1}{1+\alpha_1^2}}$$

$$\boxed{\mathrm{Corr}(x_t, x_{t+h}) = 0 \quad \text{for all } h \ge 2}$$

The second line is the striking one: $x_{t+2} = e_{t+2}+\alpha_1 e_{t+1}$ shares **no shock at all** with $x_t = e_t + \alpha_1e_{t-1}$, so they are *independent*, not merely uncorrelated.

> [!note] Numerical feel
> | $\alpha_1$ | $\mathrm{Corr}(x_t,x_{t+1})$ |
> |---|---|
> | $0.5$ | $0.5/1.25 = \mathbf{0.400}$ |
> | $0.8$ | $0.8/1.64 = \mathbf{0.488}$ |
> | $1.0$ | $1/2 = \mathbf{0.500}$ ← **the maximum possible** |
>
> **An MA(1) can never have adjacent correlation above $0.5$.** (Maximise $\alpha/(1+\alpha^2)$: the derivative vanishes at $\alpha=1$.)

An MA(1) is **stationary** (from the identical distribution of the $e_t$) **and weakly dependent** — trivially so, since the correlation is not merely small for large $h$, it is exactly zero. LLN and CLT apply.

##### Example 2: AR(1) — autoregression of order one

$$\boxed{y_t = \rho_1 y_{t-1} + e_t, \qquad t=1,2,\dots}$$

with starting value $y_0$, $\{e_t\}$ i.i.d. mean zero variance $\sigma_e^2$, the $e_t$ independent of $y_0$, and $\mathbb{E}(y_0)=0$.

> [!important] The stability condition
> $$\boxed{|\rho_1| < 1}$$
> A process satisfying it is a **stable AR(1)**. **This single inequality is the dividing line of the entire chapter** — everything in §3 is about what happens when it fails.

**Deriving the variance.** Assume covariance stationarity. Then $\mathbb{E}(y_t)=\mathbb{E}(y_{t-1})$, and from the model this forces $\mathbb{E}(y_t) = 0$ (given $\rho_1 \ne 1$). Taking variances, using independence of $e_t$ and $y_{t-1}$:

$$\sigma_y^2 = \rho_1^2\sigma_y^2 + \sigma_e^2 \quad\Longrightarrow\quad \boxed{\sigma_y^2 = \frac{\sigma_e^2}{1-\rho_1^2}}$$

**This is only finite because $\rho_1^2 < 1$.** Note how it blows up as $|\rho_1| \to 1$ — a preview of §3.

**Deriving the correlation.** Repeated substitution gives

$$y_{t+h} = \rho_1^h y_t + \rho_1^{h-1}e_{t+1} + \cdots + \rho_1 e_{t+h-1} + e_{t+h}$$

Multiply by $y_t$, take expectations, and use that $e_{t+j}$ is uncorrelated with $y_t$ for $j\ge1$:

$$\mathrm{Cov}(y_t,y_{t+h}) = \rho_1^h\,\mathbb{E}(y_t^2) = \rho_1^h\sigma_y^2$$

$$\boxed{\mathrm{Corr}(y_t, y_{t+h}) = \rho_1^{\,h}}$$

In particular $\mathrm{Corr}(y_t,y_{t+1}) = \rho_1$: **$\rho_1$ *is* the correlation between adjacent terms.**

> [!important] Geometric decay is the mechanism
> Because $|\rho_1|<1$, $\rho_1^h \to 0$ as $h\to\infty$ — **and geometrically fast.** That is the weak dependence.
>
> | $h$ | $\rho_1 = 0.9$ | $\rho_1 = 0.5$ |
> |---|---|---|
> | 1 | $0.900$ | $0.500$ |
> | 5 | $0.591$ | $0.031$ |
> | 10 | $0.349$ | $0.001$ |
> | 20 | $0.122$ | $\approx 0$ |
>
> **Even at $\rho_1=0.9$ — very high adjacent correlation — observations 20 years apart correlate only $0.12$.** At $\rho_1=0.5$ the memory is gone within a handful of periods.

The AR(1) is the workhorse of the rest of the course: it returns in [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]] as a model of the *errors*, and in forecasting.

#### 1d. Trending series can still be weakly dependent

> [!warning] The confusion this chapter most wants to prevent
> **Trending $\ne$ persistent.** A trending series is certainly **nonstationary** (its mean moves), but it can be perfectly **weakly dependent**.
>
> The linear-trend model of [[10 - Basic Regression Analysis with Time Series Data#5. Trends and seasonality|ch. 10 §5]], $y_t = \alpha_0+\alpha_1 t+e_t$, has $\{y_t\}$ **actually independent across $t$** — the only thing linking observations is a deterministic function of $t$.

A series that is stationary about its time trend **and** weakly dependent is called a **trend-stationary process**. *(The name is imperfect: weak dependence is being assumed alongside stationarity.)*

> [!tip] The practical rule
> **Trend-stationary processes can be used in regression exactly as in ch. 10 — provided the time trend is included in the model.** Include the trend and all the asymptotics of §2 go through.

---

### 2. Asymptotic properties of OLS

Same architecture as [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]]: weaken the assumptions, lose exactness, keep large-sample validity. The primed assumptions **replace** TS.1–TS.6 wholesale.

#### 2a. The five assumptions

> [!important] TS.1′ — Linearity and Weak Dependence
> The model is
> $$y_t = \beta_0+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t$$
> and $\{(\mathbf{x}_t, y_t)\}$ is **stationary and weakly dependent**, so the LLN and CLT apply to sample averages.
>
> **The critical addition over TS.1 is weak dependence.** **And crucially: the $x_{tj}$ may now include lags of the dependent variable.**

*Wooldridge's own footnote is worth internalising: stationarity is included "for convenience" and is not critical; **weak dependence is the assumption doing the work.***

> [!important] TS.2′ — No Perfect Collinearity
> Identical to TS.2.

> [!important] TS.3′ — Zero Conditional Mean (**contemporaneous** exogeneity)
> $$\boxed{\mathbb{E}(u_t \mid \mathbf{x}_t) = 0}$$
> where $\mathbf{x}_t = (x_{t1},\dots,x_{tk})$ is **only the current period's regressors**.

> [!important] TS.4′ — Contemporaneous Homoskedasticity
> $$\mathrm{Var}(u_t\mid\mathbf{x}_t)=\sigma^2$$

> [!important] TS.5′ — No Serial Correlation
> $$\mathbb{E}(u_tu_s\mid\mathbf{x}_t,\mathbf{x}_s)=0 \qquad \text{for all } t\ne s$$

> [!tip] How to read the primes
> **Every prime means "condition on less."** TS.3 conditioned on $\mathbf{X}$ — the regressors in *all* periods. TS.3′ conditions on **period $t$ alone**. Likewise TS.4′ drops to $\mathbf{x}_t$, and TS.5′ conditions only on the two periods involved.
>
> **When thinking about TS.5′, it is fine to ignore the conditioning entirely and just ask: are $u_t$ and $u_s$ uncorrelated?**

For consistency alone, even TS.3′ is more than needed — zero *unconditional* mean plus zero covariances suffices:

$$\mathbb{E}(u_t)=0, \qquad \mathrm{Cov}(x_{tj},u_t)=0, \quad j=1,\dots,k \tag{11.6}$$

#### 2b. The two theorems

> [!important] Theorem 11.1 — Consistency of OLS
> Under **TS.1′, TS.2′, TS.3′**:
> $$\operatorname{plim}\hat\beta_j = \beta_j, \qquad j=0,1,\dots,k$$

> [!important] Theorem 11.2 — Asymptotic Normality of OLS
> Under **TS.1′ through TS.5′**, the OLS estimators are asymptotically normal, and **the usual OLS standard errors, $t$ statistics, $F$ statistics and LM statistics are asymptotically valid.**

> [!warning] The trade, stated plainly
> | | Ch. 10 (TS.1–TS.6) | Ch. 11 (TS.1′–TS.5′) |
> |---|---|---|
> | Exogeneity needed | **Strict** — $u_t \perp$ *all* periods' $x$ | **Contemporaneous** — period $t$ only |
> | Lagged $y$ as a regressor | **Impossible** | **Allowed** |
> | Dependence in the series | Unrestricted | **Must be weakly dependent** |
> | What you get | **Unbiased**, BLUE, **exact** $t$/$F$ | **Consistent**, asymptotically normal, **approximate** $t$/$F$ |
> | Normality needed | Yes (TS.6) for exactness | **No** |
>
> **Read the second row and the fourth row together — that is the entire bargain of this chapter.**

Also worth knowing: under TS.1′–TS.5′ OLS is **asymptotically efficient** in the class of Theorem 5.3 (with $i$ replaced by $t$), and **trending regressors are fine provided the series are trend stationary and the trends are in the equation.**

#### 2c. Four examples of what TS.3′ does and does not allow

##### Example 11.1 — Static model

$$y_t = \beta_0+\beta_1z_{t1}+\beta_2z_{t2}+u_t, \qquad \mathbb{E}(u_t\mid z_{t1},z_{t2})=0$$

The condition rules out exactly what it always ruled out: **omitted variables correlated with the regressors, misspecified functional form** (no function of $z_{t1}$ or $z_{t2}$ may correlate with $u_t$), and **measurement error** — the same list as [[09 - More on Specification and Data Issues|ch. 09]].

> [!important] What TS.3′ newly permits — feedback
> TS.3′ says **nothing** about $\mathrm{Corr}(u_{t-1}, z_{t1})$. So a policy rule like
> $$z_{t1} = \delta_0+\delta_1 y_{t-1}+v_t$$
> — say, money-supply growth responding to last month's inflation — is **completely allowed**, even though it makes $z_{t1}$ and $u_{t-1}$ correlated.
>
> **This is precisely the feedback that killed strict exogeneity in [[10 - Basic Regression Analysis with Time Series Data#3. Assumptions TS.1–TS.6|ch. 10 §3]].** It is the main practical dividend of going asymptotic.

##### Example 11.2 — Finite distributed lag model

$$y_t = \alpha_0+\delta_0z_t+\delta_1z_{t-1}+\delta_2z_{t-2}+u_t$$

The natural assumption is

$$\mathbb{E}(u_t\mid z_t,z_{t-1},z_{t-2},z_{t-3},\dots)=0$$

i.e. **once two lags are in, no further lag of $z$ affects $\mathbb{E}(y_t\mid\cdot)$** — if one did, you would include it. Setting $\mathbf{x}_t=(z_t,z_{t-1},z_{t-2})$, TS.3′ holds and OLS is consistent. **Again, feedback from $y$ to future $z$ is not ruled out.**

##### Example 11.3 — AR(1) model: why lagged $y$ *must* break strict exogeneity

$$y_t=\beta_0+\beta_1y_{t-1}+u_t, \qquad \mathbb{E}(u_t\mid y_{t-1},y_{t-2},\dots)=0 \tag{11.12–11.13}$$

Together these give

$$\mathbb{E}(y_t\mid y_{t-1},y_{t-2},\dots) = \mathbb{E}(y_t\mid y_{t-1}) = \beta_0+\beta_1y_{t-1} \tag{11.14}$$

**"First order" means exactly this: once one lag is controlled for, no further lag helps.**

> [!important] The proof that TS.3 is impossible here
> Since $\mathbf{x}_t$ contains only $y_{t-1}$, condition (11.13) gives TS.3′ immediately. But **strict exogeneity TS.3** would require $u_t$ to be uncorrelated with the regressors in *every* period — i.e. with all of $y_0,y_1,\dots,y_{n-1}$.
>
> That **cannot** hold. Under (11.13), $u_t$ is uncorrelated with $y_{t-1}$, and therefore
> $$\boxed{\mathrm{Cov}(y_t,u_t)=\mathrm{Var}(u_t)>0}$$
> since $y_t = \beta_0+\beta_1y_{t-1}+u_t$ and the first two terms are uncorrelated with $u_t$.
>
> **$y_t$ is itself a regressor (in period $t+1$), and it is mechanically correlated with $u_t$. A model with a lagged dependent variable can never satisfy TS.3.**

For weak dependence we additionally need $|\beta_1|<1$. Then Theorem 11.1 gives consistency — **but**:

> [!warning] Consistent is not unbiased
> $\hat\beta_1$ **is biased**, and the bias can be severe when $n$ is small **or when $\beta_1$ is near 1** (in which case it is sharply **downward**). In moderate to large samples it is fine.
>
> This is the ch. 11 bargain made concrete: **you get to put $y_{t-1}$ on the right-hand side, and the price is that finite-sample unbiasedness is gone forever.**

##### TS.5′ holds automatically in the AR(1)

Take $s<t$. Since $u_s = y_s-\beta_0-\beta_1y_{s-1}$, $u_s$ is a function of $y$ dated before $t$. By (11.13), $\mathbb{E}(u_t\mid u_s,y_{t-1},y_{s-1})=0$, so

$$\mathbb{E}(u_tu_s\mid u_s,y_{t-1},y_{s-1}) = u_s\,\mathbb{E}(u_t\mid u_s, y_{t-1},y_{s-1}) = 0$$

and the law of iterated expectations gives $\mathbb{E}(u_tu_s\mid y_{t-1},y_{s-1})=0$.

> [!important] The link that §4 generalises
> **If genuinely only one lag belongs in the equation, the errors are automatically serially uncorrelated.** Serial correlation and omitted dynamics are **the same problem wearing two hats.**

#### 2d. Two applied examples

##### Example 11.4 — Efficient markets hypothesis

A strict form of the EMH: information available before week $t$ cannot predict week $t$'s return —

$$\mathbb{E}(y_t\mid y_{t-1},y_{t-2},\dots) = \mathbb{E}(y_t) \tag{11.15}$$

Test it by nesting inside an AR(1) and testing $H_0:\beta_1=0$. **Note how neatly the null does the theoretical work:** under $H_0$ returns are serially uncorrelated, hence certainly weakly dependent, and TS.3′ holds by (11.15).

Weekly NYSE returns, Jan 1976–Mar 1989 (mean $0.196\%$, max $8.45\%$, min $-15.32\%$ during the October 1987 crash):

$$\widehat{return}_t = \underset{(0.081)}{0.180} + \underset{(0.038)}{0.059}\,return_{t-1}$$
$$n=689,\quad R^2=.0035,\quad \bar R^2=.0020$$

$t = 0.059/0.038 \approx \mathbf{1.55}$ — **not rejected even at 10%.** A hint of positive weekly persistence, but nothing that would overturn the EMH.

An AR(1) alternative could miss correlation more than one week out, so extend to AR(2):

$$\widehat{return}_t = \underset{(0.081)}{0.186} + \underset{(0.038)}{0.060}\,return_{t-1} - \underset{(0.038)}{0.038}\,return_{t-2}$$
$$n=688,\quad R^2=.0048,\quad \bar R^2=.0019$$

Individually insignificant; jointly, using the $R^2$ form of the $F$ statistic from [[04 - Multiple Regression Analysis - Inference|ch. 04]] (the restricted $R^2$ is $0$ under $H_0:\beta_1=\beta_2=0$):

$$F = \frac{.0048/2}{(1-.0048)/685} = \mathbf{1.65}, \qquad p = .193$$

**Not rejected even at 15%.**

> [!note] Why an $F$ test is legitimate here
> Theorem 11.2 requires TS.4′ too, so we add $\mathrm{Var}(u_t\mid y_{t-1},y_{t-2})=\sigma^2$. **Financial returns are the textbook case of *volatility clustering*, which violates exactly this** — see ARCH in [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]. The test above assumes the problem away.

##### Example 11.5 — Expectations-augmented Phillips curve

$$inf_t - inf_t^{\,e} = \beta_1(unem_t-\mu_0)+e_t$$

with $\mu_0$ the **natural rate of unemployment**, $inf^e_t$ expected inflation formed in year $t-1$, $inf_t - inf^e_t$ **unanticipated inflation**, $unem_t-\mu_0$ **cyclical unemployment**, and $e_t$ a **supply shock**. A tradeoff means $\beta_1<0$.

Close the model with **adaptive expectations** in their simplest form, $inf^e_t = inf_{t-1}$:

$$\boxed{\Delta inf_t = \beta_0+\beta_1 unem_t + e_t, \qquad \beta_0 = -\beta_1\mu_0}$$

**The change in inflation, not its level, is what unemployment explains.** Since $\beta_1<0$ and $\mu_0>0$, $\beta_0>0$.

`PHILLIPS` data through 2006:

$$\widehat{\Delta inf}_t = \underset{(1.18)}{2.82} - \underset{(0.202)}{0.515}\,unem_t$$
$$n=58,\quad R^2=0.104,\quad \bar R^2=0.089$$

$t = -0.515/0.202 = \mathbf{-2.55}$, two-sided $p \approx \mathbf{.014}$ — **a pronounced and significant tradeoff.**

> [!important] Contrast with the static Phillips curve
> [[10 - Basic Regression Analysis with Time Series Data|Ch. 10]]'s **static** Phillips curve found a *slightly positive* relation between inflation and unemployment. **Adding expectations flips the sign and makes it significant.** The specification, not the data, was the problem.

**Backing out the natural rate.** Since $\mu_0 = \beta_0/(-\beta_1)$:

$$\hat\mu_0 = \frac{2.82}{0.515} \approx \mathbf{5.48}$$

comfortably inside the 5–6% range macroeconomists usually cite. Wooldridge reports $\mathrm{se}(\hat\mu_0) = .577$, giving an asymptotic 95% CI of about $\mathbf{[4.35,\,6.61]}$.

> [!warning] Why that standard error is hard
> $\hat\mu_0$ is a **nonlinear function of two OLS estimates** — a ratio. **It cannot be read off the regression output.** Obtaining it requires the delta method (Wooldridge 2010, ch. 3).
>
> **Compare the reparameterisation trick** used for the LRP in [[10 - Basic Regression Analysis with Time Series Data|ch. 10]], for the prediction CI in [[06 - Multiple Regression Analysis - Further Issues|ch. 06 §4]], and for rebasing dummies in [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07 §3]]: when the quantity of interest is a **linear** combination, you can rewrite the model so the package prints its standard error. **A ratio is not linear, so the trick fails here.** That distinction is exam-worthy.

---

### 3. Highly persistent time series

**This is where things break.** Many economic series are simply not weakly dependent, and using them raw invites nonsense.

#### 3a. The random walk

Set $\rho_1=1$ in the AR(1):

$$\boxed{y_t = y_{t-1}+e_t}, \qquad t=1,2,\dots \tag{11.20}$$

with $\{e_t\}$ i.i.d. mean zero variance $\sigma_e^2$, and $y_0$ independent of every $e_t$. **Today's value is yesterday's value plus an independent shock.**

By repeated substitution, $y_t = e_t+e_{t-1}+\cdots+e_1+y_0$ — **a random walk is just an accumulated sum of shocks.** Everything follows from that.

> [!important] The four properties
> $$\mathbb{E}(y_t) = \mathbb{E}(y_0) \quad\text{(constant; }=0\text{ if } y_0=0)$$
> $$\boxed{\mathrm{Var}(y_t) = \sigma_e^2\,t} \quad \text{— grows linearly in } t$$
> $$\boxed{\mathbb{E}(y_{t+h}\mid y_t) = y_t \quad \text{for all } h\ge1}$$
> $$\boxed{\mathrm{Corr}(y_t,y_{t+h}) = \sqrt{\tfrac{t}{t+h}}}$$
> (the last two assuming $\mathrm{Var}(y_0)=0$).

Take each in turn.

**The mean is constant** — so a random walk has no trend. **Do not equate persistence with trending.**

**The variance grows without bound.** $\mathrm{Var}(y_t)=\sigma_e^2 t$ **immediately rules out stationarity** (condition (ii) of covariance stationarity fails). The shocks never fade, so their variances keep piling up.

**The best forecast at any horizon is today's value.** Contrast the stable AR(1), where $\mathbb{E}(y_{t+h}\mid y_t)=\rho_1^h y_t \to 0 = \mathbb{E}(y_t)$: **memory of $y_t$ dies, and the forecast reverts to the unconditional mean.** In a random walk it never does.

> [!tip] A random walk *justifies* adaptive expectations
> At $h=1$, $\mathbb{E}(y_{t+1}\mid y_t)=y_t$ is **exactly** the assumption $inf^e_t = inf_{t-1}$ of Example 11.5. **If inflation follows a random walk, adaptive expectations are not a crude approximation — they are the optimal forecast.**

**The correlation dies far too slowly.** $\sqrt{t/(t+h)}$ depends on $t$ — so $\{y_t\}$ is **not even covariance stationary**. And for fixed $t$ it tends to zero as $h\to\infty$, but *glacially*, and **the larger $t$ is, the slower it goes.**

> [!important] The killer property
> **For any horizon $h$, you can find a $t$ making the correlation as close to 1 as you like.**
>
> | $t$ | $h$ | $\mathrm{Corr}(y_t,y_{t+h})$ |
> |---|---|---|
> | 50 | 10 | $0.913$ |
> | 500 | 10 | $0.990$ |
> | 50 | 50 | $0.707$ |
> | 1000 | 100 | $\mathbf{0.953}$ |
>
> Wooldridge's own illustration: **with $h=100$, taking $t>1{,}000$ gives correlation above $.95$.** (Check: $\sqrt{1000/1100}=.9535$; the threshold is crossed at $t=926$, where $\sqrt{926/1026}=.9500$.)
>
> **A random walk is therefore *not* asymptotically uncorrelated — it fails weak dependence outright, and with it the CLT.**

#### 3b. Unit root processes and drift

> [!important] Unit root process
> A **random walk is the special case** $\rho_1=1$ **of an AR(1) with i.i.d. innovations.** The general **unit root process** is (11.20) with $\{e_t\}$ allowed to be *any* weakly dependent series — it could itself be an MA(1) or a stable AR(1).
>
> The exact formulas above then fail, **but the essential feature survives: today's $y$ stays highly correlated with $y$ in the distant future.**

**Random walk with drift** adds a constant:

$$\boxed{y_t = \alpha_0+y_{t-1}+e_t} \tag{11.23}$$

Repeated substitution gives $y_t = \alpha_0 t+e_t+\cdots+e_1+y_0$, so with $y_0=0$:

$$\mathbb{E}(y_t)=\alpha_0 t, \qquad \mathbb{E}(y_{t+h}\mid y_t)=\alpha_0 h+y_t, \qquad \mathrm{Var}(y_t)=\sigma_e^2 t$$

**The mean now follows a linear time trend, so the series both trends and is highly persistent.** The best $h$-step forecast is today's value plus $h$ drifts. Wooldridge's Figure 11.3 shows the signature: **the series grows, but never regularly returns to the trend line** — unlike a trend-stationary series, which does.

> [!warning] Why "return to trend" is the diagnostic
> **Trend-stationary:** deviations from the trend are weakly dependent, so the series is pulled back. **Random walk with drift:** deviations are permanent — a shock shifts the whole future path.
>
> **This is not a cosmetic distinction; it is the difference between a policy having a temporary and a permanent effect.**

> [!note] Why policymakers care
> If GDP is asymptotically uncorrelated, GDP 30 years hence is at best weakly related to today's — **so a policy that moved GDP long ago has little lasting impact.** If GDP is strongly dependent, **a policy causing a discrete change in GDP has long-lasting effects.** Same data, opposite conclusions.

Wooldridge cites the **three-month T-bill rate (1948–1996)** as a series generally thought to be well characterised by a random walk. **He also warns that eyeballing a plot rarely settles it** — formal tests wait until ch. 18.

#### 3c. Transformations: I(0) versus I(1)

> [!important] The integration vocabulary
> - **Integrated of order zero, I(0)** — **weakly dependent.** *Nothing needs to be done*: sample averages already obey the standard limit theorems.
> - **Integrated of order one, I(1)** — the **first difference** is weakly dependent. Unit root processes (with or without drift) are I(1). Also called **difference-stationary**.

For the pure random walk this is transparent:

$$\Delta y_t = y_t - y_{t-1} = e_t, \qquad t=2,3,\dots \tag{11.24}$$

— **the differenced series is literally i.i.d.** More generally, if $\{e_t\}$ is any weakly dependent process, $\{\Delta y_t\}$ is weakly dependent.

**For strictly positive series, $\log(y_t)$ is often I(1)**, so use

$$\Delta\log(y_t)=\log(y_t)-\log(y_{t-1}) \approx \frac{y_t-y_{t-1}}{y_{t-1}} \tag{11.25}$$

i.e. the **growth rate**. That is exactly what Example 11.4 did: rather than modelling the stock price $p_t$, it modelled $return_t = 100\cdot(p_t-p_{t-1})/p_{t-1}$.

> [!warning] Proportionate vs percentage
> $\Delta\log(y_t)$ is a **proportionate** change; multiply by 100 for a **percentage** change. **Always check which convention a data set uses before interpreting a coefficient** — it is a factor-of-100 error waiting to happen. (Naming conventions: `cy`/`dy` for changes, `gy` for growth rates.)

> [!tip] Differencing also removes a linear trend — for free
> If $y_t=\gamma_0+\gamma_1t+v_t$ with $\mathbb{E}(v_t)=0$, then
> $$\Delta y_t = \gamma_1+\Delta v_t \quad\Longrightarrow\quad \mathbb{E}(\Delta y_t)=\gamma_1 \text{ (constant)}$$
> **So instead of including a time trend, you can difference the trending variables.** Same for $\Delta\log(y_t)$ when $\log(y_t)$ trends linearly.
>
> **But these are not equivalent strategies** — detrending assumes trend stationarity, differencing assumes a unit root. **Choosing wrongly either leaves a unit root in place or over-differences.**

#### 3d. Deciding whether a series is I(1)

Formal tests (Dickey–Fuller) are ch. 18. The informal tool:

> [!important] First order autocorrelation
> $\hat\rho_1$ = the **sample correlation between $y_t$ and $y_{t-1}$**. Since $\rho_1=\mathrm{Corr}(y_t,y_{t-1})$ in a stable AR(1), $\hat\rho_1$ estimates it — **consistently, provided $|\rho_1|<1$, though never unbiasedly.**

> [!tip] The rule of thumb
> $$\boxed{\text{Difference if } \hat\rho_1 > 0.9; \text{ some economists difference at } \hat\rho_1 > 0.8}$$
> **No hard-and-fast rule exists.** This is a judgement call.

> [!warning] Why a confidence interval for $\rho_1$ won't save you
> The obvious move — build a CI for $\rho_1$ and see whether it excludes 1 — **does not work.** The sampling distribution of $\hat\rho_1$ is **radically different** when $\rho_1$ is near 1 than when it is well below 1, and **when $\rho_1$ is close to one, $\hat\rho_1$ has a severe downward bias.**
>
> **So the very case you most need to detect is the case where the estimator is most misleading — and biased in the direction of missing it.** This non-standard distribution is exactly why unit root testing needs its own machinery.

> [!warning] Detrend *before* computing $\hat\rho_1$
> When the series has an obvious trend, compute $\hat\rho_1$ **on the detrended series**. Otherwise the autocorrelation is **overestimated**, biasing you toward **finding a unit root in a merely trending process.**

##### Example 11.6 — Fertility equation, revisited

[[10 - Basic Regression Analysis with Time Series Data|Ch. 10]]'s Example 10.4 regressed the general fertility rate $gfr$ on the personal exemption $pe$ **in levels**. But

$$\hat\rho_1 = .977 \;(gfr), \qquad \hat\rho_1=.964\;(pe)$$

**Both are far above the .9 threshold** — strongly suggestive of unit roots, which *"raise serious questions about our use of the usual OLS $t$ statistics for this example back in Chapter 10."*

In first differences (dropping the dummy for simplicity):

$$\widehat{\Delta gfr} = \underset{(0.502)}{-0.785} - \underset{(0.028)}{0.043}\,\Delta pe$$
$$n=71,\quad R^2=.032,\quad \bar R^2=.018$$

$t=-1.54$ — **an increase in $pe$ now *lowers* $gfr$ contemporaneously, and insignificantly.** *"This gives very different results than when we estimated the model in levels, and it casts doubt on our earlier analysis."*

Adding two lags of $\Delta pe$:

$$\widehat{\Delta gfr} = \underset{(0.468)}{-0.964} - \underset{(0.027)}{0.036}\,\Delta pe - \underset{(0.028)}{0.014}\,\Delta pe_{-1} + \underset{(0.027)}{0.110}\,\Delta pe_{-2}$$
$$n=69,\quad R^2=.233,\quad \bar R^2=.197$$

$\Delta pe$ and $\Delta pe_{-1}$ are small and **jointly insignificant** ($p=.28$), but the **second lag is very significant** ($t = .110/.027 = \mathbf{4.07}$).

> [!important] The economics improved along with the statistics
> A **two-year-delayed** response of fertility to a tax incentive **makes far more sense than a contemporaneous one** — conception, gestation and the decision lag all take time. **The differenced specification is both statistically defensible and economically more sensible.** $\bar R^2$ also jumped from $.018$ to $.197$.

##### Example 11.7 — Wages and productivity

$hrwage$ = average hourly wage, $outphr$ = output per hour. Both display clear upward linear trends, so include a trend (`EARNS`, 1947–1987):

$$\widehat{\log(hrwage_t)} = \underset{(0.37)}{-5.33} + \underset{(0.09)}{1.64}\log(outphr_t) - \underset{(0.002)}{0.018}\,t$$
$$n=41,\quad R^2=.971,\quad \bar R^2=.970$$

**The elasticity of 1.64 is not credible.** A 1% productivity gain raising real wages 1.64%? *"U.S. workers would probably have trouble believing that their wages increase by more than 1.5% for every 1% increase in productivity."* And because $\mathrm{se}=.09$ is tiny, $H_0:\beta_1=1$ is crushed: $t=(1.64-1)/.09=\mathbf{7.11}$, with a 95% CI of roughly $[1.46,\,1.82]$ — **unit elasticity easily excluded.**

But **detrended** first order autocorrelations are $.967$ for $\log(hrwage)$ and $.945$ for $\log(outphr)$ — **unit roots even after removing the trends.** Re-estimate in first differences (no trend needed now):

$$\widehat{\Delta\log(hrwage_t)} = \underset{(0.0042)}{-0.0036} + \underset{(0.173)}{0.809}\,\Delta\log(outphr_t)$$
$$n=40,\quad R^2=.364,\quad \bar R^2=.348$$

Now the elasticity is $\mathbf{0.81}$, and $t$ for $H_0:\beta_1=1$ is $(0.809-1)/0.173 = \mathbf{-1.10}$ — **not distinguishable from one**, which is what economic theory would predict. $\bar R^2=.348$: growth in output explains about **35% of the growth in real wages**.

> [!important] The lesson these two examples exist to teach
> **The levels regression had $R^2=.971$ and a $t$ statistic of 7 against unit elasticity. It was wrong.**
>
> Spectacular fit plus enormous $t$ statistics is the *signature* of regressing one I(1) series on another — **not** evidence of a strong relationship. See **spurious regression** in [[10 - Basic Regression Analysis with Time Series Data#5. Trends and seasonality|ch. 10 §5]].
>
> **When data are highly persistent, we usually have more faith in first-difference results.**

> [!note] Mixed cases
> In both examples *both* variables had unit roots. In practice you can face a **mixture** — one I(1) regressor, one weakly dependent (though possibly trending) regressor. Wooldridge leaves this to Computer Exercise C1; the general treatment (cointegration) is ch. 18.

---

### 4. Dynamically complete models and the absence of serial correlation

§2c showed that a *correctly specified* AR(1) automatically satisfies TS.5′. **How far does that generalise?**

#### 4a. The static model

$$y_t=\beta_0+\beta_1z_t+u_t \tag{11.30}$$

Consistency needs only $\mathbb{E}(u_t\mid z_t)=0$, and **generally the $\{u_t\}$ will be serially correlated.** But if we strengthen it to

$$\mathbb{E}(u_t\mid z_t,y_{t-1},z_{t-1},\dots)=0 \tag{11.31}$$

then TS.5′ holds. Equivalently:

$$\mathbb{E}(y_t\mid z_t,y_{t-1},z_{t-1},\dots) = \mathbb{E}(y_t\mid z_t) = \beta_0+\beta_1z_t \tag{11.32}$$

**Read that first equality carefully: once $z_t$ is controlled for, *no lag of either $y$ or $z$* helps explain $y_t$.**

> [!warning] This is a very strong requirement
> It is *"implausible when the lagged dependent variable has predictive power, which is often the case."* **If the first equality in (11.32) fails, expect serially correlated errors.**

#### 4b. Generalising

For a two-lag FDL model $y_t=\beta_0+\beta_1z_t+\beta_2z_{t-1}+\beta_3z_{t-2}+u_t$, the natural distributed-lag assumption is that at most two lags of $z$ matter. **Condition (11.31) says more:** once $z$ and its two lags are in, **no lag of $y$ and no further lag of $z$** affects $y_t$. More likely than the static case — **but it still rules out lagged $y$ having predictive power.**

> [!important] Dynamically complete model
> For the general model $y_t=\beta_0+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t$ (where $\mathbf{x}_t$ may or may not contain lags of $y$ or $z$), the condition is
> $$\boxed{\mathbb{E}(u_t\mid\mathbf{x}_t,y_{t-1},\mathbf{x}_{t-1},\dots)=0} \tag{11.37}$$
> equivalently
> $$\boxed{\mathbb{E}(y_t\mid\mathbf{x}_t,y_{t-1},\mathbf{x}_{t-1},\dots)=\mathbb{E}(y_t\mid\mathbf{x}_t)} \tag{11.38}$$
>
> **In words: whatever is in $\mathbf{x}_t$, enough lags have been included that no further lag of anything helps explain $y_t$.**

#### 4c. Dynamic completeness $\Rightarrow$ TS.5′

Since (11.37) is equivalent to $\mathbb{E}(u_t\mid\mathbf{x}_t,u_{t-1},\mathbf{x}_{t-1},u_{t-2},\dots)=0$ (11.39), take $s<t$ and apply the law of iterated expectations:

$$\mathbb{E}(u_tu_s\mid\mathbf{x}_t,\mathbf{x}_s) = \mathbb{E}\big[\mathbb{E}(u_tu_s\mid\mathbf{x}_t,\mathbf{x}_s,u_s)\,\big|\,\mathbf{x}_t,\mathbf{x}_s\big] = \mathbb{E}\big[u_s\,\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_s,u_s)\,\big|\,\mathbf{x}_t,\mathbf{x}_s\big]$$

Because $s<t$, the triple $(\mathbf{x}_t,\mathbf{x}_s,u_s)$ is a **subset** of the conditioning set in (11.39), so $\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_s,u_s)=0$ and the whole thing is $\mathbb{E}(u_s\cdot 0\mid\cdot)=0$. **TS.5′ holds.**

> [!important] The equivalence to remember
> $$\boxed{\text{dynamically complete} \;\Longrightarrow\; \text{no serial correlation}}$$
> **Contrapositive — and this is how it is used in practice: serial correlation in the errors means your dynamics are incomplete.**

#### 4d. Should every model be dynamically complete?

> [!warning] No — and the rigid view is wrong
> Some argue every model should be dynamically complete and that serial correlation always signals misspecification. Wooldridge: ***"This stance is too rigid."***
>
> - **For forecasting** (ch. 18): **yes.** You want every scrap of predictive information in the model.
> - **Otherwise: not necessarily.** Sometimes a **static model is the object of interest** (a Phillips curve), or a **finite distributed lag** is (the long-run wage response to a 1% productivity gain). **The parameter you want is well defined whether or not lagged $y$ predicts current $y$.**
>
> In those cases you **keep the specification and fix the inference** — [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]].

##### Example 11.8 — Fertility again

Is equation (11.27) — $\Delta gfr$ on $\Delta pe$ and two lags — dynamically complete? **Add $\Delta gfr_{-1}$ and look:** the coefficient is $\mathbf{.300}$ with $t=\mathbf{2.84}$.

**Highly significant, so no: the model is not dynamically complete**, and we should expect serially correlated errors — to be tested and corrected in ch. 12.

#### 4e. Sequential exogeneity — the weaker cousin

> [!important] Sequentially exogenous
> $$\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_{t-1},\dots)=\mathbb{E}(u_t)=0 \tag{11.40}$$
> **Condition on all past and present $\mathbf{x}$ — but *not* on past $y$.**

> [!important] The hierarchy
> $$\text{strict} \;\Rightarrow\; \text{sequential} \;\Rightarrow\; \text{contemporaneous}$$
> and separately
> $$\text{dynamic completeness} \;\Rightarrow\; \text{sequential exogeneity}$$
> (because $(\mathbf{x}_t,\mathbf{x}_{t-1},\dots)$ is a subset of $(\mathbf{x}_t,y_{t-1},\mathbf{x}_{t-1},\dots)$).
>
> **Special case: if $\mathbf{x}_t$ contains $y_{t-1}$, dynamic completeness and sequential exogeneity are the same condition.**

**Why the distinction earns its keep.** When $\mathbf{x}_t$ does *not* contain $y_{t-1}$, sequential exogeneity **allows the dynamics to be incomplete**. In an FDL model that is often exactly what you want:

$$\mathbb{E}(y_t\mid z_t,z_{t-1},z_{t-2},z_{t-3},\dots)=\mathbb{E}(y_t\mid z_t,z_{t-1},z_{t-2})=\alpha_0+\delta_0z_t+\delta_1z_{t-1}+\delta_2z_{t-2}$$

makes $\mathbf{x}_t=(z_t,z_{t-1},z_{t-2})$ **sequentially exogenous** — two lags suffice for the *distributed lag dynamics*. But typically the model is **not dynamically complete**, since past $y$ may still predict current $y$.

> [!tip] The question each assumption answers
> - **Sequential exogeneity:** *have I included enough lags of the explanatory variables to capture the distributed lag dynamics?* — **usually what an FDL model cares about**
> - **Dynamic completeness:** *have I included enough lags of everything, including $y$, that nothing further predicts $y_t$?* — **what forecasting cares about**
>
> **And note: the regressors in an FDL model may or may not be strictly exogenous** — sequential exogeneity says nothing about feedback from $y$ to *future* $z$.

---

### 5. The homoskedasticity assumption for time series models

TS.4′ looks just like its cross-sectional twin, **but because $\mathbf{x}_t$ can contain lagged $y$, it needs unpacking.**

> [!important] The rule
> **Whatever appears on the right-hand side, the variance of $y_t$ given those variables must be constant.**

| Model | TS.4′ requires |
|---|---|
| Static: $y_t=\beta_0+\beta_1z_t+u_t$ | $\mathrm{Var}(u_t\mid z_t)=\sigma^2$ |
| AR(1): $y_t=\beta_0+\beta_1y_{t-1}+u_t$ | $\mathrm{Var}(u_t\mid y_{t-1})=\mathrm{Var}(y_t\mid y_{t-1})=\sigma^2$ |
| $y_t=\beta_0+\beta_1z_t+\beta_2y_{t-1}+\beta_3z_{t-1}+u_t$ | $\mathrm{Var}(u_t\mid z_t,y_{t-1},z_{t-1})=\sigma^2$ |

Note the pattern in the middle row: **$\mathbb{E}(y_t\mid y_{t-1})$ is allowed to depend on $y_{t-1}$; $\mathrm{Var}(y_t\mid y_{t-1})$ is not.** The *location* of the distribution may move with the past; **its spread may not.**

> [!warning] What this rules out
> If the model contains lagged $y$ or lagged regressors, TS.4′ **explicitly rules out dynamic heteroskedasticity** — variance that depends on the recent past. **That is exactly ARCH**, and exactly what financial returns do ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]).
>
> **But in a static model, only $\mathrm{Var}(y_t\mid z_t)$ is restricted** — no direct restriction is placed on $\mathrm{Var}(y_t\mid y_{t-1})$.

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> The vault contains **no data files**, so nothing here can be re-estimated. Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — MA(1) and AR(1): the anatomy of weak dependence**

Let $\{e_t\}$ be i.i.d. with mean zero and $\mathrm{Var}(e_t)=\sigma_e^2=1$.

**(i)** For the MA(1) process $x_t = e_t + 0.8\,e_{t-1}$, find $\mathrm{Var}(x_t)$, $\mathrm{Corr}(x_t,x_{t+1})$ and $\mathrm{Corr}(x_t,x_{t+2})$. Is it covariance stationary? Weakly dependent?

**(ii)** Show that for an MA(1), $\mathrm{Corr}(x_t,x_{t+1})$ can never exceed $0.5$, and find the $\alpha_1$ that attains it.

**(iii)** For a stable AR(1) $y_t=\rho_1y_{t-1}+e_t$, tabulate $\mathrm{Corr}(y_t,y_{t+h})$ at $h=1,5,10,20,50$ for $\rho_1=0.7$ and $\rho_1=0.95$. Which would you be comfortable putting into a regression untransformed?

**(iv)** Find $\mathrm{Var}(y_t)$ for each of the two $\rho_1$ values. What happens as $\rho_1\to1$?

> [!example]- Solution
> **(i)** With $\alpha_1=0.8$:
> $$\mathrm{Var}(x_t)=(1+\alpha_1^2)\sigma_e^2 = 1+0.64=\mathbf{1.64}$$
> $$\mathrm{Corr}(x_t,x_{t+1})=\frac{\alpha_1}{1+\alpha_1^2}=\frac{0.8}{1.64}=\mathbf{0.488}$$
> $$\mathrm{Corr}(x_t,x_{t+2})=\mathbf{0}$$
> because $x_{t+2}=e_{t+2}+0.8e_{t+1}$ shares no shock with $x_t=e_t+0.8e_{t-1}$; they are in fact **independent**.
>
> **Covariance stationary:** yes — the mean is $0$, the variance is $1.64$, and the covariance depends only on $h$ (all constants, no $t$).
> **Weakly dependent:** yes, emphatically — the correlation is not merely small for large $h$, it is **exactly zero for $h\ge2$**.
>
> ---
> **(ii)** Maximise $f(\alpha)=\alpha/(1+\alpha^2)$:
> $$f'(\alpha)=\frac{(1+\alpha^2)-\alpha(2\alpha)}{(1+\alpha^2)^2}=\frac{1-\alpha^2}{(1+\alpha^2)^2}$$
> which vanishes at $\alpha=1$, giving $f(1)=1/2$. Since $f'>0$ for $\alpha<1$ and $f'<0$ for $\alpha>1$, this is the **maximum**: $\boxed{\alpha_1=1,\ \mathrm{Corr}=0.5}$.
>
> **The point:** an MA(1) is structurally incapable of strong adjacent correlation. **To generate high persistence you need an autoregression, not a moving average.**
>
> ---
> **(iii)** $\mathrm{Corr}(y_t,y_{t+h})=\rho_1^h$:
>
> | $h$ | $\rho_1=0.7$ | $\rho_1=0.95$ |
> |---|---|---|
> | 1 | $0.700$ | $0.950$ |
> | 5 | $0.168$ | $0.774$ |
> | 10 | $0.028$ | $0.599$ |
> | 20 | $0.001$ | $0.359$ |
> | 50 | $\approx 0$ | $0.077$ |
>
> **$\rho_1=0.7$:** memory is gone within about 10 periods. **Comfortably weakly dependent — use it as is.**
>
> **$\rho_1=0.95$:** still correlated $0.36$ at $h=20$. **Technically weakly dependent** (it is a stable AR(1), and $0.95^h\to0$), **but it is above the $\hat\rho_1>0.9$ rule of thumb.** In a finite sample the asymptotics will be a poor approximation and $\hat\rho_1$ will be biased downward — **you would not be able to tell it from a unit root, and you should difference.**
>
> **This is the exercise's real lesson: "weakly dependent" is an asymptotic property, and a series can satisfy it while behaving, in 40 annual observations, exactly like a random walk.**
>
> ---
> **(iv)** $\sigma_y^2=\sigma_e^2/(1-\rho_1^2)$:
> $$\rho_1=0.7:\quad \frac{1}{1-0.49}=\mathbf{1.96} \qquad\qquad \rho_1=0.95:\quad \frac{1}{1-0.9025}=\mathbf{10.26}$$
> As $\rho_1\to1$ the denominator $\to0$ and $\boxed{\sigma_y^2\to\infty}$ — **there is no finite stationary variance at a unit root**, consistent with $\mathrm{Var}(y_t)=\sigma_e^2t$ growing without bound.

---

**Exercise 2 — What TS.1′–TS.5′ buy and what they cost**

**(i)** State the four substantive differences between {TS.1–TS.6} and {TS.1′–TS.5′}, and say what OLS delivers under each set.

**(ii)** Prove that the AR(1) model $y_t=\beta_0+\beta_1y_{t-1}+u_t$ with $\mathbb{E}(u_t\mid y_{t-1},y_{t-2},\dots)=0$ **cannot** satisfy strict exogeneity TS.3.

**(iii)** A researcher regresses monthly inflation on money-supply growth, where the central bank sets money growth partly in response to *last* month's inflation. Which of TS.3 and TS.3′ can hold? What are the consequences for OLS?

**(iv)** Explain why TS.6 (normality) does not appear in the primed list at all.

> [!example]- Solution
> **(i)**
>
> | | TS.1–TS.6 | TS.1′–TS.5′ |
> |---|---|---|
> | **Dependence** | Unrestricted | **Weak dependence required** |
> | **Exogeneity** | **Strict**: $\mathbb{E}(u_t\mid\mathbf{X})=0$ (all periods) | **Contemporaneous**: $\mathbb{E}(u_t\mid\mathbf{x}_t)=0$ |
> | **Lagged $y$** | Forbidden (it breaks TS.3) | **Allowed** |
> | **Normality** | TS.6 assumed | **Dropped** |
>
> **Delivers:** ch. 10 — unbiased, BLUE (TS.1–5), **exact** $t$ and $F$ (with TS.6). Ch. 11 — **consistent** (TS.1′–3′), asymptotically normal with **asymptotically valid** usual standard errors, $t$, $F$ and LM (TS.1′–5′).
>
> **The one-line summary: you trade finite-sample exactness for the ability to model dynamics.**
>
> ---
> **(ii)** Strict exogeneity requires $u_t$ to be uncorrelated with the regressor in **every** period. The regressors across all periods are $y_0,y_1,\dots,y_{n-1}$ — which include $y_t$ itself (it is the regressor in period $t+1$).
>
> From the model, $y_t=\beta_0+\beta_1y_{t-1}+u_t$. Given $\mathbb{E}(u_t\mid y_{t-1},\dots)=0$, $u_t$ is uncorrelated with $y_{t-1}$, so
> $$\mathrm{Cov}(y_t,u_t)=\mathrm{Cov}(\beta_0+\beta_1y_{t-1}+u_t,\;u_t)=\beta_1\underbrace{\mathrm{Cov}(y_{t-1},u_t)}_{=0}+\mathrm{Var}(u_t)=\mathrm{Var}(u_t)>0 \;\blacksquare$$
>
> **This is structural, not a defect of any particular data set. No model with a lagged dependent variable is ever strictly exogenous** — which is precisely why ch. 11 must exist.
>
> ---
> **(iii)** Write $y_t$ = inflation, $z_t$ = money growth, with $z_t=\delta_0+\delta_1y_{t-1}+v_t$.
>
> **TS.3 fails.** Substituting for $y_{t-1}$ shows $z_t$ depends on $u_{t-1}$, so $\mathrm{Cov}(z_t,u_{t-1})\ne0$ — and TS.3 requires $u_{t-1}$ to be uncorrelated with the regressor in **every** period, including $t$.
>
> **TS.3′ can hold** — it constrains only $\mathbb{E}(u_t\mid z_t)$, saying nothing about $u_{t-1}$ and $z_t$.
>
> **Consequences:** OLS is **biased** (TS.3 fails, so Theorem 10.1 is unavailable) but **consistent**, and the usual inference is **asymptotically valid**, provided the series are weakly dependent (Theorems 11.1–11.2).
>
> **This is the single most useful thing ch. 11 does for applied work: policy variables respond to past outcomes, and ch. 10's theory simply cannot accommodate that.**
>
> ---
> **(iv)** TS.6 exists only to make the $t$ and $F$ statistics have **exact** $t$ and $F$ distributions in finite samples. Once we are content with **asymptotic** validity, the CLT supplies approximate normality of $\hat\beta_j$ regardless of the distribution of $u_t$ — **so the assumption has no work left to do.**
>
> Exactly as in [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05 §2]] for cross-sections: *"as usual for large-sample analysis, we dispense with the normality assumption entirely."*

---

**Exercise 3 — Random walk versus stable AR(1)**

Let $y_t=y_{t-1}+e_t$ with $y_0=0$ and $\mathrm{Var}(e_t)=\sigma_e^2=1$.

**(i)** Find $\mathrm{Var}(y_t)$ at $t=10$ and $t=100$. Why does this alone rule out covariance stationarity?

**(ii)** Compute $\mathrm{Corr}(y_t,y_{t+h})$ at $(t,h)=(50,10)$, $(500,10)$, $(50,50)$ and $(1000,100)$. What do the first two, taken together, show that a stable AR(1) can never do?

**(iii)** Compare $\mathbb{E}(y_{t+h}\mid y_t)$ for the random walk with the same quantity for a stable AR(1) with $\rho_1=0.7$, at $h=1$ and $h=20$, taking $y_t=8$.

**(iv)** GDP is claimed to be I(1). What does that imply about the long-run effect of a one-off policy shock, compared with GDP being I(0)?

> [!example]- Solution
> **(i)** $\mathrm{Var}(y_t)=\sigma_e^2 t = t$:
> $$t=10:\ \mathbf{10}\ (\mathrm{sd}\ 3.16) \qquad t=100:\ \mathbf{100}\ (\mathrm{sd}\ 10)$$
> Covariance stationarity requires **constant** variance (condition (ii)). Here it **grows linearly in $t$ without bound**, so the process is nonstationary — **and this is true even though the mean, $\mathbb{E}(y_t)=\mathbb{E}(y_0)=0$, is perfectly constant.**
>
> **Note the diagnostic value:** a random walk has **no trend** but is wildly nonstationary. **Nonstationarity is not the same thing as trending.**
>
> ---
> **(ii)** $\mathrm{Corr}(y_t,y_{t+h})=\sqrt{t/(t+h)}$:
>
> | $t$ | $h$ | Correlation |
> |---|---|---|
> | 50 | 10 | $\sqrt{50/60}=\mathbf{0.913}$ |
> | 500 | 10 | $\sqrt{500/510}=\mathbf{0.990}$ |
> | 50 | 50 | $\sqrt{50/100}=\mathbf{0.707}$ |
> | 1000 | 100 | $\sqrt{1000/1100}=\mathbf{0.953}$ |
>
> **Rows 1 and 2 are the key pair.** The horizon is **identical** ($h=10$) yet the correlation **rises** from $.913$ to $.990$ purely because $t$ is larger. **The correlation depends on $t$, not just $h$** — so the process is **not covariance stationary**, and there is no such thing as "the" correlation at lag 10.
>
> **A stable AR(1) can never do this:** $\mathrm{Corr}=\rho_1^h$ depends on $h$ **alone**. And row 4 makes the fatal point: **at any horizon, however long, a large enough $t$ pushes the correlation arbitrarily close to 1.** The random walk is **not asymptotically uncorrelated**, so no CLT applies.
>
> ---
> **(iii)** With $y_t=8$:
>
> | | $h=1$ | $h=20$ |
> |---|---|---|
> | **Random walk** $\mathbb{E}(y_{t+h}\mid y_t)=y_t$ | $\mathbf{8}$ | $\mathbf{8}$ |
> | **AR(1), $\rho_1=0.7$**, $=\rho_1^hy_t$ | $0.7\times8=\mathbf{5.6}$ | $0.7^{20}\times8=\mathbf{0.006}$ |
>
> **The stable AR(1) forgets.** By $h=20$ the forecast has collapsed to the unconditional mean of zero — today's value is irrelevant. **The random walk never forgets: the best forecast 20 periods out is still exactly 8.**
>
> **Shocks are transitory under stability and permanent under a unit root.** That is the whole distinction, in two rows.
>
> ---
> **(iv)** **If GDP is I(1)**, a one-off shock is **permanently** absorbed into the level — $\mathbb{E}(y_{t+h}\mid y_t)=y_t$ means the entire future path shifts. **A policy causing a discrete change in GDP has long-lasting effects.**
>
> **If GDP is I(0)**, deviations decay geometrically and GDP reverts to its trend/mean. **GDP 30 years hence is at best weakly related to today's, so a policy that moved GDP long ago has very little lasting impact.**
>
> **Same data, opposite policy conclusions — which is why the I(0)/I(1) question is not a technicality.**

---

**Exercise 4 — Diagnosing and fixing a unit root**

A researcher has four annual series, with first order autocorrelations computed as shown:

| Series | $\hat\rho_1$ | Notes |
|---|---|---|
| $gfr$ (general fertility rate) | $.977$ | no obvious trend |
| $pe$ (personal exemption) | $.964$ | no obvious trend |
| $\log(hrwage)$ | $.967$ | **computed after linear detrending** |
| $\log(outphr)$ | $.945$ | **computed after linear detrending** |

**(i)** What does the rule of thumb say to do with each?

**(ii)** Why must $\hat\rho_1$ for the last two be computed **after** detrending? What goes wrong otherwise?

**(iii)** A colleague proposes building a 95% confidence interval for $\rho_1$ and differencing only if it excludes 1. Why is that a bad idea?

**(iv)** The levels regression of $\log(hrwage)$ on $\log(outphr)$ and a trend gave an elasticity of $1.64$ with $\mathrm{se}=.09$ and $R^2=.971$; the first-difference version gave $0.809$ with $\mathrm{se}=.173$ and $\bar R^2=.348$. Test $H_0:\beta_1=1$ in each and say which you believe.

> [!example]- Solution
> **(i)** **All four exceed $0.9$, so difference all four.** Under the stricter $>.8$ convention, the conclusion is the same. These are *"highly suggestive of unit root behavior."*
>
> Note what this does to the ch. 10 analyses: it *"raises serious questions about our use of the usual OLS $t$ statistics."* Exact $t$ distributions need the **full** CLM assumptions; relaxing them in any way and appealing to asymptotics **requires I(0) series** — which these are not.
>
> ---
> **(ii)** If a trending series is **not** detrended first, the trend itself creates correlation between $y_t$ and $y_{t-1}$ — both are near the trend line at nearby dates, regardless of the stochastic dynamics. **$\hat\rho_1$ is then overestimated, biasing you toward finding a unit root in a merely trending process.**
>
> This matters because the two diagnoses call for **different fixes**: a trend-stationary series should be **detrended** (or have a trend included, per §1d); a unit root series must be **differenced**. **Getting it wrong means either leaving a unit root in place or over-differencing a perfectly usable series.**
>
> *(Note how severe the finding is here: $\log(hrwage)$ has $\hat\rho_1=.967$ **after** the trend has been stripped out. The persistence is not the trend.)*
>
> ---
> **(iii)** Two reasons, and the second is worse than the first.
>
> 1. **The sampling distribution of $\hat\rho_1$ is completely different near $\rho_1=1$** than for $\rho_1$ well below 1 — it is non-normal and non-standard, so an ordinary CI has the wrong coverage exactly where it is applied.
> 2. **When $\rho_1$ is close to one, $\hat\rho_1$ has a severe downward bias.** So the estimator systematically understates persistence **precisely in the case you are trying to detect**, tilting the test toward wrongly concluding stationarity.
>
> **The case you most need to catch is the case where the tool is most broken, and broken in the direction of missing it.** Proper unit root testing (Dickey–Fuller, ch. 18) exists because of this.
>
> ---
> **(iv)** **Levels:**
> $$t=\frac{1.64-1}{0.09}=\mathbf{7.11}$$
> — unit elasticity **decisively rejected**; the 95% CI is roughly $[1.46,1.82]$ (using $t_{38,.025}\approx2.02$).
>
> **First differences:**
> $$t=\frac{0.809-1}{0.173}=\mathbf{-1.10}$$
> — **not remotely rejected.** (And $\beta_1=0$ *is* rejected: $t=0.809/0.173=4.68$.)
>
> **Believe the first differences.** Three reasons:
>
> 1. **Both series have unit roots even after detrending**, so the levels regression violates the weak dependence needed for the asymptotics — its $t$ statistics are not trustworthy.
> 2. **$R^2=.971$ and $t=7.11$ are exactly the signature of spurious regression** between two I(1) series, not evidence of a strong relationship. **High $R^2$ is the symptom, not the reassurance.**
> 3. **1.64 is not economically credible** — real wages rising $1.64\%$ per $1\%$ productivity gain would be extraordinary. **$0.81$, statistically indistinguishable from 1, is what theory predicts.**
>
> **The general principle: when data are highly persistent, we usually have more faith in first-difference results.**

---

**Exercise 5 — Dynamic completeness and serial correlation**

Consider the first-differenced fertility model

$$\Delta gfr_t = \beta_0+\beta_1\Delta pe_t+\beta_2\Delta pe_{t-1}+\beta_3\Delta pe_{t-2}+u_t$$

**(i)** State precisely what dynamic completeness requires here, and give the test that Wooldridge performs.

**(ii)** Adding $\Delta gfr_{t-1}$ gives a coefficient of $.300$ with $t=2.84$. What do you conclude, and what does it predict about the errors? Recover the standard error.

**(iii)** Prove the implication *dynamic completeness $\Rightarrow$ TS.5′* for this model, taking $s<t$.

**(iv)** Is the model **sequentially exogenous**? Does the failure in (ii) mean the researcher must respecify?

**(v)** Why is a correctly specified AR(1) *automatically* free of serial correlation, while a static model generally is not?

> [!example]- Solution
> **(i)** With $\mathbf{x}_t=(\Delta pe_t,\Delta pe_{t-1},\Delta pe_{t-2})$, dynamic completeness is
> $$\mathbb{E}(\Delta gfr_t\mid\mathbf{x}_t,\Delta gfr_{t-1},\mathbf{x}_{t-1},\dots)=\mathbb{E}(\Delta gfr_t\mid\mathbf{x}_t)$$
> — **once $\Delta pe$ and its two lags are controlled for, neither lags of $\Delta gfr$ nor further lags of $\Delta pe$ should matter.**
>
> **The test is direct: add the candidate omitted dynamics and test their significance.** Wooldridge adds $\Delta gfr_{t-1}$.
>
> ---
> **(ii)** $t=2.84$ is significant at the 1% level (two-sided $p\approx.005$). **The model is not dynamically complete.**
>
> Recovering the standard error: $\mathrm{se}=.300/2.84=\mathbf{.106}$.
>
> **Prediction about the errors:** since dynamic completeness $\Rightarrow$ TS.5′, the **contrapositive** warns that TS.5′ may fail — **expect serially correlated errors**, which would invalidate the usual standard errors even asymptotically. Testing and correcting for it is [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]].
>
> ---
> **(iii)** Dynamic completeness (11.37) is equivalent to
> $$\mathbb{E}(u_t\mid\mathbf{x}_t,u_{t-1},\mathbf{x}_{t-1},u_{t-2},\dots)=0$$
> Take $s<t$. By the law of iterated expectations, conditioning first on the larger set $(\mathbf{x}_t,\mathbf{x}_s,u_s)$:
> $$\mathbb{E}(u_tu_s\mid\mathbf{x}_t,\mathbf{x}_s)=\mathbb{E}\big[\mathbb{E}(u_tu_s\mid\mathbf{x}_t,\mathbf{x}_s,u_s)\mid\mathbf{x}_t,\mathbf{x}_s\big]$$
> Inside, $u_s$ is a **function of the conditioning variables**, so it pulls out:
> $$=\mathbb{E}\big[u_s\,\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_s,u_s)\mid\mathbf{x}_t,\mathbf{x}_s\big]$$
> Since $s<t$, the set $(\mathbf{x}_t,\mathbf{x}_s,u_s)$ is a **subset** of the conditioning set in (11.39), so the inner expectation is **zero**:
> $$=\mathbb{E}(u_s\cdot0\mid\mathbf{x}_t,\mathbf{x}_s)=0 \;\blacksquare$$
> **The step that does all the work is "$s<t$ makes it a subset" — the asymmetry of time is what makes the proof go through.**
>
> ---
> **(iv)** **Sequential exogeneity** requires only $\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_{t-1},\dots)=0$ — **conditioning on past $\Delta pe$ but *not* on past $\Delta gfr$.** That is plausible here: it says **two lags suffice to capture the distributed lag dynamics of $pe$**, which is exactly the modelling assumption.
>
> **No, the researcher need not respecify.** *"This stance is too rigid."* The object of interest is the **distributed lag response of fertility to the tax exemption** — a well-defined parameter whether or not lagged $\Delta gfr$ predicts current $\Delta gfr$. **Keep the specification, fix the inference** (ch. 12).
>
> **The exception is forecasting**, where you *do* want dynamic completeness, because any predictive information left out is forecast accuracy given away.
>
> ---
> **(v)** **AR(1):** the assumption $\mathbb{E}(u_t\mid y_{t-1},y_{t-2},\dots)=0$ **is itself the statement that one lag exhausts the dynamics** — it says no further lag of $y$ affects $\mathbb{E}(y_t\mid\cdot)$. Dynamic completeness is therefore built into the model's defining assumption, and §2c's derivation shows TS.5′ follows. *"As long as only one lag belongs in (11.12), the errors must be serially uncorrelated."*
>
> **Static model:** $\mathbb{E}(u_t\mid z_t)=0$ constrains **only the contemporaneous relationship**. Nothing prevents $u_t$ — which absorbs every omitted influence on $y_t$ — from being persistent, and **omitted influences on economic outcomes usually are persistent.** So the errors will generally be serially correlated.
>
> > **The unifying statement: serial correlation is omitted dynamics.** Put the dynamics in the equation and it vanishes; leave them out (deliberately, because you want a static parameter) and you must deal with it in the standard errors.

---

## 📝 Summary

- **Stationarity and weak dependence are different properties.** Stationarity = the joint distribution is invariant to time shifts (it permits arbitrarily strong correlation); weak dependence = $\mathrm{Corr}(x_t,x_{t+h})\to0$ fast enough (asymptotically uncorrelated). **Covariance stationarity** is the weaker, second-moment-only version: constant mean, constant variance, $\mathrm{Cov}(x_t,x_{t+h})$ depending only on $h$.
- **Weak dependence is what replaces random sampling**, delivering the LLN and CLT. **Series that are not weakly dependent generally satisfy no CLT** — which is why using them raw in a regression is dangerous.
- **MA(1):** $x_t=e_t+\alpha_1e_{t-1}$ has $\mathrm{Corr}(x_t,x_{t+1})=\alpha_1/(1+\alpha_1^2)\le0.5$ and **exactly zero beyond $h=1$**. **Stable AR(1):** $|\rho_1|<1$ gives $\sigma_y^2=\sigma_e^2/(1-\rho_1^2)$ and $\mathrm{Corr}(y_t,y_{t+h})=\rho_1^h$ — **geometric decay is the mechanism of weak dependence.**
- **TS.1′–TS.5′** weaken TS.1–TS.6 to **contemporaneous** exogeneity $\mathbb{E}(u_t\mid\mathbf{x}_t)=0$, contemporaneous homoskedasticity, and no serial correlation, adding **weak dependence** and dropping **normality**. **Theorem 11.1:** consistency (needs TS.1′–3′). **Theorem 11.2:** asymptotic normality, and the usual $t$/$F$/LM statistics are asymptotically valid.
- **The bargain: lagged $y$ becomes a legal regressor, and feedback from $y$ to future $x$ becomes legal — at the price of unbiasedness.** Any model with a lagged dependent variable **must** violate strict exogeneity, because $\mathrm{Cov}(y_t,u_t)=\mathrm{Var}(u_t)>0$.
- **A random walk** ($\rho_1=1$) has constant mean but $\mathrm{Var}(y_t)=\sigma_e^2t$, $\mathbb{E}(y_{t+h}\mid y_t)=y_t$ at every horizon, and $\mathrm{Corr}(y_t,y_{t+h})=\sqrt{t/(t+h)}$ — **which depends on $t$, so it is not even covariance stationary, and never becomes asymptotically uncorrelated.** Adding a drift $\alpha_0$ makes the mean trend linearly while persistence is unchanged.
- **I(0) = weakly dependent, use as is. I(1) = unit root, first-difference it** ($\Delta y_t$ or $\Delta\log y_t$, the growth rate). **Differencing also removes a linear trend for free** — but detrending and differencing are **not** interchangeable: one assumes trend stationarity, the other a unit root.
- **The diagnostic is $\hat\rho_1$, the first order autocorrelation: difference if $\hat\rho_1>0.9$ (some say $0.8$), computed *after detrending* for trending series.** A confidence interval for $\rho_1$ **will not do** — its distribution is non-standard near 1 and $\hat\rho_1$ is severely biased downward exactly there.
- **Dynamic completeness** — $\mathbb{E}(y_t\mid\mathbf{x}_t,y_{t-1},\mathbf{x}_{t-1},\dots)=\mathbb{E}(y_t\mid\mathbf{x}_t)$ — **implies TS.5′.** Contrapositive: **serial correlation means the dynamics are incomplete.** A correctly specified AR(1) is automatically dynamically complete; static and FDL models generally are not.
- **Not every model should be dynamically complete.** For **forecasting**, yes. For a static Phillips curve or an FDL long-run propensity, the parameter of interest is well defined regardless — **keep the specification and fix the standard errors** ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]). **Sequential exogeneity** ($\mathbb{E}(u_t\mid\mathbf{x}_t,\mathbf{x}_{t-1},\dots)=0$) is the weaker condition that FDL models actually need.

---

## ⚠️ Important Notes

> [!warning] Stationarity ≠ weak dependence ≠ absence of a trend
> **Three properties, all independent.** The table that resolves every exam question on this:
>
> | Process | Stationary? | Weakly dependent? | Trending? |
> |---|---|---|---|
> | i.i.d. sequence | ✅ | ✅ | ❌ |
> | MA(1) | ✅ | ✅ | ❌ |
> | Stable AR(1) | ✅ | ✅ | ❌ |
> | $y_t=\alpha_0+\alpha_1t+e_t$ (trend stationary) | ❌ (mean moves) | ✅ (**independent!**) | ✅ |
> | Random walk | ❌ (variance grows) | ❌ | ❌ (**constant mean**) |
> | Random walk with drift | ❌ | ❌ | ✅ |
>
> **Read the last two rows.** A random walk **has no trend** and is nonstationary. A trend-stationary process **trends** and is perfectly weakly dependent. **"It trends, therefore it's persistent" and "no trend, therefore it's fine" are both wrong.**

> [!warning] Consistency is not unbiasedness
> Theorem 11.1 delivers $\operatorname{plim}\hat\beta_j=\beta_j$ — **nothing more**. In the AR(1), $\hat\beta_1$ **is biased**, and *"this bias can be large if the sample size is small or if $\beta_1$ is near 1"*, in which case it is **severely downward**.
>
> **The trap:** this is the same downward bias that afflicts $\hat\rho_1$ near a unit root (§3d). **A near-unit-root AR coefficient is systematically underestimated — so the finite-sample evidence tilts toward stationarity precisely when the series is most persistent.** Time series samples are often 40–60 observations. **"Asymptotically valid" is a promise about a sample size you do not have.**

> [!warning] High $R^2$ plus huge $t$ statistics is a *symptom*, not a reassurance
> Example 11.7's levels regression: $R^2=.971$, and unit elasticity rejected with $t=7.11$. **It was spurious.** Regressing one I(1) series on another manufactures exactly this pattern.
>
> **Before celebrating a time series regression's fit, check $\hat\rho_1$ on each series (after detrending).** See [[10 - Basic Regression Analysis with Time Series Data#5. Trends and seasonality|ch. 10 §5]] on spurious regression, and ch. 18 for cointegration — the case where a levels regression of I(1) variables *is* legitimate.

> [!warning] "Weakly dependent" is asymptotic — it does not certify a finite sample
> A stable AR(1) with $\rho_1=0.95$ **satisfies weak dependence by definition** ($0.95^h\to0$). It is also **correlated $0.36$ at $h=20$**, above the differencing rule of thumb, and in 40 annual observations **indistinguishable from a random walk**.
>
> **The theory being satisfied in the limit tells you nothing about whether the approximation is any good at your $n$.** This is the same gap as in [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] — asymptotic results are approximations whose quality is an empirical matter.

> [!warning] Detrending and differencing are not the same fix
> Both make a trending series usable, and **choosing between them is a substantive decision:**
>
> | If the series is… | Correct fix | Wrong fix does |
> |---|---|---|
> | **Trend stationary** (I(0) around a trend) | Include a time trend / detrend | **Over-differencing** — induces a moving average in the errors |
> | **Unit root with drift** (I(1)) | **First difference** | Leaves a unit root in place — **spurious regression** |
>
> **And $\hat\rho_1$ computed without detrending is biased toward the unit-root verdict**, so the diagnostic itself must be applied carefully.

> [!warning] The primes weaken, they do not strengthen
> TS.3′ is **weaker** than TS.3 (conditions on less), TS.4′ weaker than TS.4, TS.5′ weaker than TS.5. **But TS.1′ is *stronger* than TS.1** — it adds stationarity and weak dependence.
>
> **The primed set is not uniformly weaker.** It buys exogeneity slack and pays in dependence restrictions. **Stating "TS.1′–TS.5′ are just weaker versions of TS.1–TS.6" will lose marks.**
>
> *(Also note: TS.6 has no primed counterpart — normality is dropped, not weakened.)*

> [!warning] Serial correlation is not automatically a specification error
> The rigid view — *serial correlation always means misspecification, always add lags* — is **explicitly rejected** by Wooldridge. Sometimes the static or FDL parameter is genuinely the object of interest.
>
> **Match the assumption to the question:**
> - Forecasting → you want **dynamic completeness**
> - Estimating a distributed lag / LRP → **sequential exogeneity** suffices; live with serial correlation and fix inference in ch. 12
>
> **Adding $y_{t-1}$ to "cure" serial correlation changes the parameter you are estimating.** $\beta_1$ in $y_t=\beta_0+\beta_1z_t+u_t$ and in $y_t=\beta_0+\beta_1z_t+\beta_2y_{t-1}+u_t$ are **different quantities.**

> [!warning] The natural rate's standard error is not on the regression printout
> $\hat\mu_0=\hat\beta_0/(-\hat\beta_1)$ is a **ratio** — a nonlinear function of two estimates. **The reparameterisation trick that works everywhere else in this course fails here.**
>
> **Where the trick *does* work** (make the quantity a coefficient, read off its standard error): centring for interactions ([[06 - Multiple Regression Analysis - Further Issues|ch. 06 §2]]), prediction intervals ([[06 - Multiple Regression Analysis - Further Issues|ch. 06 §4]]), rebasing dummies ([[07 - Multiple Regression Analysis with Qualitative Information|ch. 07 §3]]), the LRP ([[10 - Basic Regression Analysis with Time Series Data|ch. 10]]).
>
> **The distinguishing test: is the quantity a *linear* combination of the $\beta_j$?** Linear → reparameterise. **Nonlinear (ratios, turning points $-\beta_1/2\beta_2$, elasticities at a point) → delta method.** Wooldridge reports $\mathrm{se}(\hat\mu_0)=.577$ without deriving it.

> [!warning] TS.4′ forbids *dynamic* heteroskedasticity
> When lagged $y$ is a regressor, TS.4′ requires $\mathrm{Var}(y_t\mid y_{t-1})$ to be **constant** even though $\mathbb{E}(y_t\mid y_{t-1})$ moves. **Financial returns violate this flagrantly** — volatility clusters, so $\mathrm{Var}(u_t)$ depends on recent shocks. **That is ARCH** ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]).
>
> So Example 11.4's $F$ test on the NYSE AR(2) **assumes away the best-documented feature of financial data.** The conclusion (EMH not rejected) is probably fine; **the stated justification is not.**

> [!note] Cross-subject connections
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — **the same material from the other side.** Stationarity, ACF/PACF, ARMA, unit roots and Dickey–Fuller are developed there in far more depth; **this chapter is the regression-user's minimum.** The AR(1) and MA(1) here are the $p=1$ and $q=1$ cases of ARMA($p,q$).
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — the LLN, the CLT, consistency and $\operatorname{plim}$ are all developed there. **The whole chapter is an argument about when those theorems apply.**
> - [[05 - Multiple Regression Analysis - OLS Asymptotics|Ch. 05]] — the cross-sectional template this chapter mirrors: weaken assumptions, lose exactness, keep large-sample validity.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **the i.i.d. assumption underlying almost all supervised learning is exactly what fails here.** Random train/test splits on time series leak the future into the past; the analogue of weak dependence is why time-based splits are mandatory.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Figures are images and cannot be extracted:**
> - **Figure 11.1** — two computer-generated random walk realizations ($y_0=0$, $e_t\sim N(0,1)$, $n=50$). Only the axis labels survive extraction (range roughly $-10$ to $5$). **The visual point — that the two paths wander apart and neither returns to zero — is described in the text and reconstructed in §3a.**
> - **Figure 11.2** — the U.S. three-month T-bill rate, 1948–1996. Axis values $1$, $8$, $14$ and the year $1972$ extract; **the series itself does not.** The text's claim — that it is *"generally thought to be well characterized by a random walk"* — is quoted, not verified.
> - **Figure 11.3** — a random walk with drift ($\alpha_0=2$, $e_t\sim N(0,9)$, $n=50$) with the dashed line $\mathbb{E}(y_t)=2t$. **The key visual — that the series grows but "does not regularly return to the trend line" — is stated in the caption text and preserved in §3b.**
>
> **Numbers I could not verify from the source:**
> - **$\mathrm{se}(\hat\mu_0)=.577$** for the natural rate in Example 11.5 is **quoted without derivation** — it requires the delta method (Wooldridge 2010, ch. 3), which is outside this book. The resulting CI $[4.35,6.61]$ is my own arithmetic from $5.476\pm1.96(.577)$ and matches the text's "about 4.35 to 6.61".
> - **Example 11.8** reports only the coefficient $.300$ and $t=2.84$ for $\Delta gfr_{-1}$. **No standard error, $R^2$ or sample size is given**; the $\mathrm{se}=.106$ in Exercise 5 is recovered arithmetically.
> - The **$p$-value of $.28$** for the joint insignificance of $\Delta pe$ and $\Delta pe_{-1}$ in Example 11.6 is quoted; **the $F$ statistic itself is not reported**, so it cannot be checked.
>
> **Notation mangled by the two-column PDF layout** (all transcribed by hand against the numbered equations): `r1` for $\rho_1$, `a1` for $\alpha_1$, `s2 e` for $\sigma_e^2$, `s2 y` for $\sigma_y^2$, `r^ 1` for $\hat\rho_1$, `Ts.19` for TS.1′, `"t/1t 1 h2` for $\sqrt{t/(t+h)}$, `E1ut0xt2` for $\mathbb{E}(u_t\mid\mathbf{x}_t)$, `Dgfr` for $\Delta gfr$, `0r10 , 1` for $|\rho_1|<1$.
>
> **A typo in the source:** the boxed summary of Assumption TS.3′ (p. 387) reads *"TS.3′ is notably weaker than the strict exogeneity Assumption **TS.3′**"* — it should read **TS.3**. The body text (p. 371) states it correctly.
>
> **All regressions are quoted as printed** — the vault has no data files, so `NYSE`, `PHILLIPS`, `FERTIL3`, `EARNS` and `INTQRT` cannot be re-estimated. **Every derived statistic in these notes ($t$ ratios, the $F$ statistic, the natural rate, the CIs) has been recomputed from the printed coefficients and standard errors and agrees with the text.**

#econometrics #time-series #stationarity #weak-dependence #unit-root #asymptotics
