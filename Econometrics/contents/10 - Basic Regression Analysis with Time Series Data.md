---
subject: Econometrics
chapter: 10
tags: [ds, econometrics, time-series, distributed-lag, trends, seasonality]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 10 (pp. 333–365)"
---

# Basic Regression Analysis with Time Series Data

> [!abstract] What this chapter is for
> **Part 2 begins.** Everything in chapters 1–9 assumed a **random sample from a population**. Time series data are not that: **the observations are ordered, and the past affects the future.**
>
> **The good news is how little changes.** Under a new set of assumptions — **TS.1 through TS.6** — every finite-sample result of [[03 - Multiple Regression Analysis - Estimation|ch. 03]]–[[04 - Multiple Regression Analysis - Inference|ch. 04]] carries over **verbatim**: same variance formula, same Gauss–Markov theorem, same $t$ and $F$ distributions.
>
> **The bad news is what those assumptions cost.** Random sampling is replaced by **strict exogeneity**, which forbids any feedback from $y$ to future $x$ — and **most policy variables in the social sciences violate it.** A brand-new assumption, **no serial correlation**, is also needed.
>
> | § | Topic |
> |---|---|
> | **1** | Time series data as a **stochastic process** |
> | **2** | **Static** and **finite distributed lag** models; impact propensity and the **LRP** |
> | **3** | **TS.1–TS.6**, and how each differs from its cross-sectional twin |
> | **4** | Logs, dummies, **event studies**, index numbers, nominal vs real |
> | **5** | **Trends** (and spurious regression), **detrending**, and **seasonality** |

---

## 📘 Main Knowledge

### 1. The nature of time series data

**Two differences from cross-sectional data.**

**The obvious one: temporal ordering.** 1970 precedes 1971, and that matters. *"For analyzing time series data in the social sciences, we must recognize that the past can affect the future, but not vice versa."*

**The subtle one: where does the randomness come from?**

> [!important] A time series is one realization of a stochastic process
> **A sequence of random variables indexed by time is a stochastic process (or time series process).** Collecting a data set gives **one possible outcome, or realization**, of it.
>
> **We see only a single realization — we cannot go back in time and start the process over.** (Exactly as in cross-sectional work we collect only one random sample.) **Had history differed, we would have observed a different realization.** That is why time series data are random variables.
>
> $$\text{The set of all possible realizations plays the role of the *population*.}$$
> $$\text{The number of time periods observed plays the role of the *sample size*.}$$
>
> The variables clearly qualify: **we do not know today what the Dow will close at tomorrow**, or what Canadian output growth will be next year.

---

### 2. Two model types

#### 2a. Static models

$$y_t=\beta_0+\beta_1z_t+u_t,\qquad t=1,2,\dots,n$$

**"Static" because it models a contemporaneous relationship.** Postulated when a change in $z$ at time $t$ has an **immediate** effect: $\Delta y_t=\beta_1\Delta z_t$ when $\Delta u_t=0$. Also used simply to describe a **trade-off**.

**The static Phillips curve:**
$$inf_t=\beta_0+\beta_1 unem_t+u_t$$
**This form assumes a constant natural rate of unemployment and constant inflationary expectations** — assumptions worth remembering, because [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] relaxes them.

**A multiple static model** for city murder rates:
$$mrdrte_t=\beta_0+\beta_1 convrte_t+\beta_2 unem_t+\beta_3 yngmle_t+u_t$$

#### 2b. Finite distributed lag models

**An FDL model lets $z$ affect $y$ with a lag.**

$$gfr_t=\alpha_0+\delta_0 pe_t+\delta_1 pe_{t-1}+\delta_2 pe_{t-2}+u_t$$

where $gfr$ is the general fertility rate and $pe$ the real value of the personal tax exemption. **The point is that for both biological and behavioural reasons, decisions to have children do not respond instantly to a tax change.**

##### Interpreting the coefficients: the temporary shock

Set $z=c$ in every period before $t$; at $t$ it rises to $c+1$ and reverts at $t+1$. **Set every error to zero** to isolate the ceteris paribus effect:

| Period | $y$ |
|---|---|
| $t-1$ | $\alpha_0+\delta_0c+\delta_1c+\delta_2c$ |
| $t$ | $\alpha_0+\delta_0(c+1)+\delta_1c+\delta_2c$ |
| $t+1$ | $\alpha_0+\delta_0c+\delta_1(c+1)+\delta_2c$ |
| $t+2$ | $\alpha_0+\delta_0c+\delta_1c+\delta_2(c+1)$ |
| $t+3$ | $\alpha_0+\delta_0c+\delta_1c+\delta_2c$ — **back to $y_{t-1}$** |

$$\boxed{\;\delta_0=y_t-y_{t-1},\qquad \delta_1=y_{t+1}-y_{t-1},\qquad \delta_2=y_{t+2}-y_{t-1}\;}$$

- **$\delta_0$ is the impact propensity (impact multiplier)** — the immediate change.
- **Plotting $\delta_j$ against $j$ gives the lag distribution**, which summarizes the **dynamic** effect of a temporary one-unit increase.
- **If you standardize $y_{t-1}=0$, the lag distribution *is* the path of $y$.**

##### Interpreting the coefficients: the permanent shock

Now $z_s=c$ for $s<t$ and $z_s=c+1$ for $s\ge t$:

| Period | Cumulative change in $y$ |
|---|---|
| $t$ | $\delta_0$ |
| $t+1$ | $\delta_0+\delta_1$ |
| $t+2$ | $\delta_0+\delta_1+\delta_2$ — **and no further change** |

$$\boxed{\;\text{LRP}=\delta_0+\delta_1+\cdots+\delta_q\;}$$

**The long-run propensity (long-run multiplier) is the total change in $y$ from a permanent one-unit increase in $z$.** More generally, for any horizon $h$, the **cumulative effect** is $\delta_0+\delta_1+\cdots+\delta_h$ — *the change in the expected outcome $h$ periods after a permanent one-unit increase.*

> [!important] The central estimation difficulty of FDL models — and its silver lining
> **$z_t$, $z_{t-1}$, $z_{t-2}$, … are usually highly correlated with one another.** That is **multicollinearity**, and it makes the individual $\hat\delta_j$ **imprecise** ([[03 - Multiple Regression Analysis - Estimation|ch. 03]] §3-4).
>
> **But — and this is the practically important point — even when the individual $\delta_j$ cannot be pinned down, the LRP can often be estimated well.** Example 10.4 below is exactly that case: **not one $\hat\delta_j$ is individually significant, and the LRP has $t=3.37$.**
>
> **The intuition:** collinearity makes it hard to apportion a shared effect among the lags, but the **total** is what the data actually identify.

**An FDL of order $q$:**
$$y_t=\alpha_0+\delta_0z_t+\delta_1z_{t-1}+\cdots+\delta_qz_{t-q}+u_t$$
**The static model is the special case $\delta_1=\cdots=\delta_q=0$**, so a primary use of an FDL is to **test whether $z$ has a lagged effect at all**. The impact propensity is always the coefficient on the contemporaneous $z_t$; **if $z_t$ is omitted, the impact propensity is zero by construction.**

> [!note] Convention about the time index
> If the equation holds from $t=1$, the regressors in the first period are $z_1,z_0,z_{-1}$. **Our convention: those are the initial values in the sample, so the time index always starts at $t=1$.** In practice regression packages track this automatically — but for chapters 10–12 we need a fixed convention.

---

### 3. Finite sample properties under the classical assumptions

**The six time series assumptions, and how each differs from its cross-sectional twin.**

| | Time series | Cross-sectional analogue | Difference |
|---|---|---|---|
| **TS.1** | Linear in parameters | MLR.1 | **None in substance** |
| **TS.2** | No perfect collinearity | MLR.3 | **None** |
| **TS.3** | **$\mathbb{E}(u_t\mid\mathbf{X})=0$ for all $t$** | MLR.4 + MLR.2 | **Much stronger — see below** |
| **TS.4** | $\mathrm{Var}(u_t\mid\mathbf{X})=\sigma^2$ | MLR.5 | Same idea |
| **TS.5** | **$\mathrm{Corr}(u_t,u_s\mid\mathbf{X})=0$, $t\ne s$** | — | **Brand new** |
| **TS.6** | $u_t$ independent of $\mathbf{X}$, i.i.d. $\mathrm{Normal}(0,\sigma^2)$ | MLR.6 | Stronger |

**Notation:** $\mathbf{x}_t=(x_{t1},\dots,x_{tk})$ is the regressor vector at time $t$; **$\mathbf{X}$ is the whole $n\times k$ array** — every regressor in every period. Row $t$ of $\mathbf{X}$ is $\mathbf{x}_t$. *This mirrors exactly how software stores time series data.*

#### TS.3 — the assumption that does all the work

$$\boxed{\;\mathbb{E}(u_t\mid \mathbf{X})=0,\qquad t=1,2,\dots,n\;}$$

**Read it as uncorrelatedness: the error at time $t$ is uncorrelated with every explanatory variable in *every* time period.** And because it is stated as a conditional expectation, it also requires that **the functional form be correctly specified.**

> [!important] Contemporaneous versus strict exogeneity — the distinction to memorize
> **Contemporaneous exogeneity:**
> $$\mathbb{E}(u_t\mid x_{t1},\dots,x_{tk})=\mathbb{E}(u_t\mid\mathbf{x}_t)=0$$
> $u_t$ uncorrelated with the regressors **dated at time $t$**. This is the direct analogue of MLR.4.
>
> **Strict exogeneity (TS.3):** $u_t$ uncorrelated with $x_{sj}$ **for every $s$, including $s\ne t$** — past **and future**.
>
> | Needed for | Assumption |
> |---|---|
> | **Consistency** of OLS ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]) | **Contemporaneous** exogeneity suffices |
> | **Unbiasedness** of OLS (this chapter) | **Strict** exogeneity required |
>
> **Why is strict exogeneity needed here and not in cross-sections?** Because **random sampling did the job silently.** Under MLR.2, $u_i$ is automatically independent of the regressors for every *other* observation $i$. **With time series, random sampling is almost never appropriate, so the condition must be stated explicitly.**
>
> **TS.3 restricts nothing about correlation *among* the regressors over time, or among the $u_t$ over time.** It says only that the **average value of $u_t$ is unrelated to the regressors in all periods.**

##### The two ways strict exogeneity fails — one obvious, one not

**The obvious ways: omitted variables and measurement error** in the regressors — as always ([[09 - More on Specification and Data Issues|ch. 09]]).

**The subtle way, and the one that matters most in practice: feedback.**

In $y_t=\beta_0+\beta_1z_t+u_t$, TS.3 requires $u_t$ uncorrelated with **past and future** $z$. Two implications:

1. **$z$ can have no lagged effect on $y$.** If it does, **estimate a distributed lag model** — otherwise the lagged effect sits in $u_t$ and correlates with $z_{t-1}$.
2. **Changes in today's error cannot cause future changes in $z$.** **This rules out feedback from $y$ to future $z$.**

> [!warning] The police-and-murder example — read this one carefully
> $$mrdrte_t=\beta_0+\beta_1 polpc_t+u_t$$
>
> Grant that $u_t$ is uncorrelated with $polpc_t$ and with **past** values of $polpc$. **But suppose the city adjusts its police force in response to past murder rates.** Then a high $u_t$ raises $mrdrte_t$, which raises $polpc_{t+1}$ — **so $polpc_{t+1}$ is correlated with $u_t$, and TS.3 fails.**
>
> **Nothing is wrong with the contemporaneous relationship. The violation runs *forward in time*.**

> [!important] Which variables are plausibly strictly exogenous?
> | Variable | Strictly exogenous? |
> |---|---|
> | **Rainfall** in an agricultural production function | ✅ **Yes** — future rainfall is not influenced by past output |
> | **Labour input** chosen by the farmer | ❌ **No** — the farmer adjusts based on last year's yield |
> | **Money supply growth, welfare spending, speed limits** | ❌ **Generally no** — policy responds to outcomes |
>
> **"Explanatory variables that are strictly exogenous cannot react to what has happened to $y$ in the past."**
>
> **In the social sciences, many explanatory variables very well may violate strict exogeneity.** We assume it anyway, to get unbiasedness — and [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] shows what survives when we drop it.

> [!note] Why not just assume the regressors are non-random?
> **Most treatments of static and FDL models assume TS.3 by assuming the $x_{tj}$ are "fixed in repeated samples."** That is **obviously false** for time series — you cannot re-run 1974 with a different inflation rate.
>
> **TS.3 is more honest:** it is realistic about the randomness of the $x_{tj}$ while **isolating exactly the condition needed** for unbiasedness.

#### The four theorems — every one identical to its cross-sectional twin

> [!important] Theorem 10.1 — **Unbiasedness**
> Under **TS.1, TS.2, TS.3**, the OLS estimators are unbiased conditional on $\mathbf{X}$, and hence unconditionally: $\mathbb{E}(\hat\beta_j)=\beta_j$.
>
> **The proof is essentially Theorem 3.1.** The only change: random sampling has been **replaced** by TS.3. **If TS.3 fails, OLS cannot be shown to be unbiased.**
>
> **And the omitted-variables-bias analysis of [[03 - Multiple Regression Analysis - Estimation|ch. 03]] §3-3 carries over unchanged** — Table 3.2 and the sign reasoning apply exactly as before.

> [!important] Theorem 10.2 — **Sampling variances**
> Under **TS.1–TS.5**,
> $$\mathrm{Var}(\hat\beta_j\mid\mathbf{X})=\frac{\sigma^2}{\text{SST}_j\left(1-R_j^2\right)}$$
> **Identical to [[03 - Multiple Regression Analysis - Estimation|ch. 03]].** Everything said there about what inflates variances — small $\text{SST}_j$, multicollinearity — **applies immediately.**

> [!important] Theorems 10.3 and 10.4
> - **Theorem 10.3:** $\hat\sigma^2=\text{SSR}/(n-k-1)$ is **unbiased** for $\sigma^2$ under TS.1–TS.5.
> - **Theorem 10.4 (Gauss–Markov):** under TS.1–TS.5, OLS is **BLUE conditional on $\mathbf{X}$**.

> [!important] Theorem 10.5 — **Normal sampling distributions**
> Under **TS.1–TS.6**, the OLS estimators are normally distributed conditional on $\mathbf{X}$; under $H_0$, each $t$ statistic has a $t$ distribution and each $F$ statistic an $F$ distribution. **Confidence intervals are constructed exactly as before.**
>
> **The implication is of the utmost importance: when TS.1–TS.6 hold, *everything* learned about estimation and inference for cross-sections applies directly to time series.**

> [!warning] But the assumptions are much more restrictive
> **The CLM assumptions for time series are far more demanding than for cross-sections — in particular strict exogeneity (TS.3) and no serial correlation (TS.5) can be unrealistic.** They remain a good starting point, and [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] and [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]] relax them.

#### TS.4 and TS.5 in a bit more detail

**Homoskedasticity (TS.4)** requires $\mathrm{Var}(u_t\mid\mathbf{X})=\sigma^2$ — **the variance cannot depend on $\mathbf{X}$, and must be constant over time.** For
$$i3_t=\beta_0+\beta_1 inf_t+\beta_2 def_t+u_t$$
this requires the unobservables driving interest rates to have **constant variance across the whole sample.** **Policy regime changes are known to affect interest-rate variability**, and the variability may depend on the level of inflation or the size of the deficit. **TS.4 might very well be false.**

**No serial correlation (TS.5).** Ignoring the conditioning,
$$\mathrm{Corr}(u_t,u_s)=0\quad\text{for all }t\ne s$$

**When this fails, the errors suffer from serial correlation (autocorrelation).** If $u_{t-1}>0$ tends to be followed by $u_t>0$, then $\mathrm{Corr}(u_t,u_{t-1})>0$ — for the interest-rate equation, *if rates are unexpectedly high this period, they are likely to be above average next period too.* **This is a reasonable description of many applications** ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]).

> [!warning] TS.5 says nothing about correlation in the *regressors*
> **$inf_t$ is almost certainly correlated across time. That is irrelevant to whether TS.5 holds.** TS.5 is about the **errors**.

> [!note] Why no such assumption in cross-sections — and where TS.1–TS.5 also apply
> **Random sampling makes $u_i$ and $u_h$ independent automatically**, for any two observations, and also conditional on the regressors. **So serial correlation is a time-series problem** (and, later, a panel-data one).
>
> **But TS.1–TS.5 sometimes fit cross-sections too** — e.g. city-level data where property tax rates are correlated **across cities within a state.** **Correlation among the *regressors* across observations causes no problem**, provided the **errors** are uncorrelated across cities.

#### Two examples

**Example 10.1 — the static Phillips curve** (`PHILLIPS`, through 2006):
$$\widehat{inf_t}=1.01+0.505\,unem_t,\qquad n=59,\;R^2=0.065,\;\bar R^2=0.049$$
$$\qquad\quad(1.49)\;\;(0.257)$$

Testing $H_0:\beta_1=0$ against $H_1:\beta_1<0$ (the trade-off hypothesis): $t=0.505/0.257=\mathbf{1.96}$, two-sided $p\approx\mathbf{0.055}$.

> [!warning] **The sign is wrong.** $\hat\beta_1>0$: if anything, a **positive** relationship
> **Two reasons not to take this at face value.**
> 1. **[[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|Chapter 12]] shows the CLM assumptions do not hold here**, so the $t$ statistic is not what it appears.
> 2. **The static Phillips curve is probably the wrong model.** Macroeconomists prefer the **expectations-augmented** Phillips curve — the static form's assumption of *constant inflationary expectations* is exactly what fails. See [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]].

**Example 10.2 — inflation, deficits and interest rates** (`INTDEF`, 1948–2003):
$$\widehat{i3_t}=1.73+0.606\,inf_t+0.513\,def_t,\qquad n=56,\;R^2=0.602$$
$$\qquad\;\;(0.43)\;(0.082)\qquad(0.118)$$

**A one percentage point rise in inflation raises the T-bill rate by 0.606 points.** $t_{inf}=7.39$, $t_{def}=4.35$ — **both very significant**, *assuming the CLM assumptions hold.* Both signs are what basic economics predicts.

---

### 4. Functional form, dummy variables, and index numbers

**Every functional form from [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] transfers.** Logs matter most: **time series regressions with constant percentage effects are everywhere in applied work.**

**Example 10.3 — Puerto Rican employment and the minimum wage** (`PRMINWGE`, 1950–1987):
$$\widehat{\log(prepop_t)}=-1.05-0.154\log(mincov_t)-0.012\log(usgnp_t)$$
$$\qquad\qquad\qquad(0.77)\;\;(0.065)\qquad\qquad(0.089)$$
$$n=38,\quad R^2=0.661$$

where $mincov=(avgmin/avgwage)\cdot avgcov$ measures the **importance of the minimum wage relative to average wages, times the coverage rate.**

**The elasticity is $-0.154$ with $t=-2.37$: a higher minimum wage lowers the employment rate**, as classical economics predicts. **GNP is insignificant — which changes completely once a time trend is added** (§5c, Example 10.9). *Hold that thought.*

**Logs in distributed lag models** give elasticities at each horizon:
$$\log(M_t)=\alpha_0+\delta_0\log(GDP_t)+\delta_1\log(GDP_{t-1})+\cdots+\delta_4\log(GDP_{t-4})+u_t$$
- **$\delta_0$ is the short-run elasticity** — the immediate % change in money demand from a 1% rise in GDP.
- **The LRP $\delta_0+\cdots+\delta_4$ is the long-run elasticity** — the % increase after four quarters from a **permanent** 1% rise.

#### Dummy variables in time series

**The unit of observation is time, so a dummy indicates whether an event occurred in that period.** `democ` for a Democratic president; a dummy for years Texas had capital punishment. **Often used to isolate periods that are systematically different.**

**Example 10.4 — the personal exemption and fertility** (`FERTIL3`, 1913–1984):
$$\widehat{gfr_t}=98.68+0.083\,pe_t-24.24\,ww2_t-31.59\,pill_t$$
$$\qquad\quad(3.21)\;(0.030)\qquad(7.46)\qquad\;(4.08)$$
$$n=72,\quad R^2=0.473$$

- **Every variable is significant at 1%.**
- **During WWII (1941–45), about 24 fewer births per 1,000 women of childbearing age** — enormous, given that $gfr$ ranged from about **65 to 127** over the period.
- **Since the pill became available (1963 onward), substantially lower fertility.**
- **$pe$:** the average is \$100.40 (range 0 to \$243.83). **A \$12 increase in $pe$ raises $gfr$ by about one birth per 1,000 women** ($12\times0.083=0.996$). *"Hardly trivial."*

**Now the distributed lag version:**
$$\widehat{gfr_t}=95.87+0.073\,pe_t-0.0058\,pe_{t-1}+0.034\,pe_{t-2}-22.12\,ww2_t-31.30\,pill_t$$
$$\qquad\quad(3.28)\;(0.126)\qquad(0.1557)\qquad\;(0.126)\qquad\;(10.73)\qquad\;(3.98)$$
$$n=70,\quad R^2=0.499$$

**Only 70 observations — two are lost to lagging $pe$ twice.**

> [!important] The textbook demonstration of the collinearity problem — and its solution
> **Not one of the three $pe$ coefficients is individually significant.** ($t$ statistics of $0.58$, $-0.04$, $0.27$.) **There is substantial correlation between $pe_t$, $pe_{t-1}$ and $pe_{t-2}$.**
>
> **Yet they are jointly significant: $F$ has $p=0.012$.** *(And $pe_{t-1}$, $pe_{t-2}$ are jointly insignificant, $p=0.95$ — so the static model of (10.18) is defensible.)*
>
> **So $pe$ affects $gfr$, but we cannot say whether the effect is contemporaneous or lagged by one or two years, or some of each.**
>
> **The LRP is $0.073-0.0058+0.034=\mathbf{0.101}$** — but **equation (10.19) contains no way to get its standard error**, because $\mathrm{Var}(\hat\delta_0+\hat\delta_1+\hat\delta_2)$ needs all three **covariances**.
>
> **The [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4 trick.** Let $\theta_0=\delta_0+\delta_1+\delta_2$, so $\delta_0=\theta_0-\delta_1-\delta_2$. Substituting:
> $$gfr_t=\alpha_0+(\theta_0-\delta_1-\delta_2)pe_t+\delta_1 pe_{t-1}+\delta_2 pe_{t-2}+\cdots$$
> $$\boxed{\;=\alpha_0+\theta_0\,pe_t+\delta_1(pe_{t-1}-pe_t)+\delta_2(pe_{t-2}-pe_t)+\cdots\;}$$
>
> **Regress $gfr_t$ on $pe_t$, $(pe_{t-1}-pe_t)$, $(pe_{t-2}-pe_t)$, $ww2_t$, $pill_t$.** The coefficient on $pe_t$ **is** $\hat\theta_0$ and the package prints its standard error.
>
> **Result:** $\hat\theta_0=0.101$ (as we knew) with $\mathrm{se}(\hat\theta_0)=\mathbf{0.030}$, so
> $$t=\frac{0.101}{0.030}=\mathbf{3.37},\qquad \text{95\% CI}=[0.041,\;0.160]$$
>
> **Even though not one $\hat\delta_j$ is individually significant, the LRP is very significant.** **This is the practical payoff of the whole section: collinearity destroys the individual coefficients and leaves the total intact.**
>
> Whittington, Alm & Peters (1990) allow further lags but **restrict the coefficients** to ease the collinearity. **For estimating the LRP, such restrictions are unnecessary.**

#### Event studies

$$R_t^f=\beta_0+\beta_1R_t^m+\beta_2d_t+u_t$$

$R_t^f$ is the firm's stock return, $R_t^m$ the market return, $d_t$ a dummy for the event. **Including $R_t^m$ controls for broad market movements that might coincide with the event.**

**Multiple dummies are common** — e.g. one for a few weeks **before** a regulation was announced and one for the weeks **after.** *"The first dummy variable might detect the presence of inside information."*

#### Index numbers, nominal and real

> [!important] An index number is meaningless in isolation
> **To interpret it you need the base period and the base value.** The Index of Industrial Production had base year 1987 = 100 in the 1997 *ERP*. Since IIP = 107.7 in 1992, **industrial production was 7.7% higher in 1992 than 1987.**
>
> **Any two years give a percentage difference:** IIP was 61.4 in 1970 and 85.7 in 1979, so industrial production grew about $\mathbf{39.6\%}$ during the 1970s.
>
> **Changing the base year:**
> $$\boxed{\;newindex_t=100\left(\frac{oldindex_t}{oldindex_{\text{new base}}}\right)\;}$$
> Rebasing 1992's IIP from 1987 to 1982 (when IIP was 81.9): $100(107.7/81.9)=\mathbf{131.5}$.
>
> **Price indexes work the same way.** CPI was 38.8 in 1970 and 130.7 in 1990: **the price level grew by almost 237%** over 20 years. (In the 1997 *ERP*, the CPI base period is **1982–1984**, averaging 100.)

**Nominal to real.** Set $p=\text{CPI}/100$ so that the base-year value is 1; then the **real wage is $w/p$**, measured in base-period dollars.

> [!warning] Why this matters — a striking illustration
> | Year | Nominal hourly wage | **Real wage (1982 \$)** |
> |---|---|---|
> | 1960 | \$2.09 | \$6.79 |
> | 1973 | \$3.94 | **\$8.55** (the peak) |
> | 1995 | \$11.44 | **\$7.40** |
>
> **Nominal wages nearly tripled between 1973 and 1995. Real wages *fell*.** *"The increase in the nominal wage was due entirely to inflation."*
>
> **Standard measures of output are already real.** Reported GDP growth is always **real** GDP growth.

**Logs of real variables impose a testable restriction.** From
$$\log(hours)=\beta_0+\beta_1\log(w/p)+u$$
and $\log(w/p)=\log(w)-\log(p)$:
$$\log(hours)=\beta_0+\beta_1\log(w)+\beta_2\log(p)+u,\qquad\textbf{with }\beta_2=-\beta_1$$

> [!tip] This is a hypothesis you can test, not a definition
> **"Only the real wage matters" is the restriction $\beta_2=-\beta_1$.** If $\beta_2\ne-\beta_1$, **the price level affects labour supply on its own** — which can happen **if workers do not fully understand the distinction between real and nominal wages** (money illusion).
>
> **Because index magnitudes are uninformative, indexes usually appear in logs, so coefficients read as percentage changes.**

**Example 10.5 — antidumping filings and chemical imports** (`BARIUM`, monthly, Feb 1978 – Dec 1988):

U.S. barium chloride producers filed a complaint with the ITC in **October 1983**; the ITC ruled in their favour in **October 1984**. Three dummies: `befile6` (six months before filing), `affile6` (six months after filing), `afdec6` (six months after the decision).

$$\widehat{\log(chnimp)}=-17.80+3.12\log(chempi)+0.196\log(gas)+0.983\log(rtwex)$$
$$\qquad\qquad\qquad(21.05)\;(0.48)\qquad\quad(0.907)\qquad\quad(0.400)$$
$$\qquad\qquad\qquad+0.060\,befile6-0.032\,affile6-0.565\,afdec6$$
$$\qquad\qquad\qquad\;\;(0.261)\qquad\quad(0.264)\qquad\quad(0.286)$$
$$n=131,\quad R^2=0.305$$

| Question | Answer |
|---|---|
| **Were imports unusually high just before filing?** | **No** — `befile6` is insignificant |
| **Did imports change after filing?** | **Barely** — $-3.2\%$, very insignificant |
| **After the favourable decision?** | **A large fall.** $100[e^{-0.565}-1]=\mathbf{-43.2\%}$, significant at 5% ($t=-1.98$) |

**Control variables behave as expected:** more chemical production raises demand for the cleaning agent; gasoline production is insignificant; **a stronger dollar raises Chinese imports**, as theory predicts. *(And the exchange-rate elasticity is not statistically different from 1: $t=(0.983-1)/0.400=-0.04$.)*

**Example 10.6 — election outcomes and economic performance** (`FAIR`, 1916–1992, $n=20$):

$$demvote=\beta_0+\beta_1 partyWH+\beta_2 incum+\beta_3\,partyWH\!\cdot\! gnews+\beta_4\,partyWH\!\cdot\! inf+u$$

> [!note] Why $partyWH$ is $\pm1$ rather than a 0/1 dummy
> $partyWH=+1$ for a Democrat in the White House, $-1$ for a Republican. **Fair uses this to impose the restriction that the effects have the same magnitude and opposite sign** — natural, since the two party shares must sum to one **by definition**. **It also saves two degrees of freedom, which matters enormously with $n=20$.** Same for $incum$ ($+1$, $-1$, or $0$).
>
> $gnews$ = number of the administration's first 15 quarters with per capita output growth above 2.9% annualized; $inf$ = average inflation over those 15 quarters.
>
> **The interactions are the objects of interest:** since $partyWH=1$ under a Democrat, **$\beta_3$ is the effect of good economic news on the party in power** (expect $\beta_3>0$), and **$\beta_4$ the effect of inflation** (expect $\beta_4<0$).

$$\widehat{demvote}=0.481-0.0435\,partyWH+0.0544\,incum+0.0108\,partyWH\!\cdot\! gnews-0.0077\,partyWH\!\cdot\! inf$$
$$\qquad\qquad(0.012)\;(0.0405)\qquad\qquad(0.0234)\qquad\;(0.0041)\qquad\qquad\quad(0.0033)$$
$$n=20,\quad R^2=0.663,\quad\bar R^2=0.573$$

- **All coefficients except $partyWH$ significant at 5%.**
- **Incumbency is worth about 5.4 percentage points of the vote.**
- **One more quarter of good news is worth about 1.1 points.**
- **Two percentage points more average inflation costs the incumbent party about 1.5 points.**

**Out-of-sample prediction for 1996** (Clinton, a Democratic incumbent): $partyWH=1$, $incum=1$, $gnews=3$, $inf=3.019$.
$$\widehat{demvote}=0.481-0.0435+0.0544+0.0108(3)-0.0077(3.019)=\mathbf{0.5011}$$

**Predicted: a razor-thin 50.1% of the two-party vote. Actual: 54.65%.** *A genuine forecast from information available before the election — and a reminder that a good in-sample fit does not guarantee a sharp forecast.*

---

### 5. Trends and seasonality

#### 5a. Characterizing trending series

**Many economic series grow over time — and ignoring this can produce entirely false conclusions.**

> [!warning] The core danger
> **Two series may appear correlated only because both are trending, for reasons related to other unobserved factors.** Concluding that one causes the other is the **spurious regression** problem.

**The linear trend model:**
$$y_t=\alpha_0+\alpha_1t+e_t$$
with $\{e_t\}$ i.i.d., $\mathbb{E}(e_t)=0$, $\mathrm{Var}(e_t)=\sigma_e^2$.

- **$\alpha_1$ is the change in $y_t$ per period due purely to the passage of time.** If $\Delta e_t=0$ then $\Delta y_t=\alpha_1$.
- **Equivalently, $\mathbb{E}(y_t)=\alpha_0+\alpha_1t$** — the mean is a linear function of time. $\alpha_1>0$: upward trend. $\alpha_1<0$: downward.
- **The variance is constant:** $\mathrm{Var}(y_t)=\sigma_e^2$. *Only the mean trends.*

**A more realistic version lets $\{e_t\}$ be correlated over time — this does not change the flavour.** *What matters for the CLM results is that $\mathbb{E}(y_t)$ is linear in $t$.*

**The exponential trend** — for series with a roughly **constant average growth rate**:
$$\log(y_t)=\beta_0+\beta_1t+e_t\quad\Longleftrightarrow\quad y_t=\exp(\beta_0+\beta_1t+e_t)$$

Since $\Delta\log(y_t)\approx(y_t-y_{t-1})/y_{t-1}$ is the **growth rate**, setting $\Delta e_t=0$ gives
$$\boxed{\;\Delta\log(y_t)=\beta_1\;}$$
**$\beta_1$ is approximately the average per-period growth rate.** If $t$ is a year and $\beta_1=0.027$, **$y$ grows about 2.7% per year on average.**

**The quadratic trend:**
$$y_t=\alpha_0+\alpha_1t+\alpha_2t^2+e_t,\qquad \frac{\Delta y_t}{\Delta t}\approx\alpha_1+2\alpha_2t$$

**Both positive: an increasing slope. $\alpha_1>0$, $\alpha_2<0$: a hump shape** — which may be a poor description, since it forces an increasing trend to be followed eventually by a decreasing one. **Over a given span, though, it is a flexible way to model complicated trends.**

#### 5b. Trending variables in regression

> [!important] Nothing about trends violates TS.1–TS.6 — but you must account for them
> **Unobserved, trending factors affecting $y_t$ may be correlated with the regressors.** The fix is direct:
> $$y_t=\beta_0+\beta_1x_{t1}+\beta_2x_{t2}+\beta_3t+u_t$$
> **This is just multiple regression with $x_{t3}=t$.** It explicitly recognizes that $y_t$ may be growing ($\beta_3>0$) or shrinking ($\beta_3<0$) for reasons unrelated to $x_{t1},x_{t2}$.
>
> **Omitting $t$ is omitting an important variable** — and the bias is severe **precisely when $x_{t1}$ and $x_{t2}$ are themselves trending**, since they will then be highly correlated with $t$.

**Example 10.7 — housing investment and prices** (`HSEINV`, 1947–1988):

**Without a trend:**
$$\widehat{\log(invpc)}=-0.550+1.241\log(price),\qquad n=42,\;R^2=0.208$$
$$\qquad\qquad\;\;(0.043)\;\;(0.382)$$

**A very large, significant price elasticity ($t=3.25$), not statistically different from 1.** *Be careful.*

**Both series trend upward:** regressing $\log(invpc)$ on $t$ gives a trend coefficient of $0.0081$ (se $0.0018$); for $\log(price)$, $0.0044$ (se $0.0004$). *(The standard errors are not reliable — these regressions contain substantial serial correlation — but the point estimates reveal the trends.)*

**With a trend:**
$$\widehat{\log(invpc)}=-0.913-0.381\log(price)+0.0098\,t,\qquad n=42,\;R^2=0.341$$
$$\qquad\qquad\;\;(1.36)\;\;(0.679)\qquad\qquad(0.0035)$$

> [!warning] **The story is completely different.** The elasticity flips to $-0.381$ and is insignificant ($t=-0.56$)
> **The trend is significant, implying about 1% growth in $invpc$ per year on average.** *"We cannot conclude that real per capita housing investment is influenced at all by price."*
>
> **The original result was spurious** — driven entirely by the fact that **both** series trend upward.

**Example 10.8 — the fertility equation, with trends.** Adding a linear trend to (10.18):
$$\widehat{gfr_t}=111.77+0.279\,pe_t-35.59\,ww2_t+0.997\,pill_t-1.15\,t,\qquad R^2=0.662$$
$$\qquad\quad(3.36)\;(0.040)\qquad(6.30)\qquad\;(6.626)\qquad(0.19)$$

**The $pe$ coefficient is more than triple the (10.18) estimate** ($0.279$ vs $0.083$, a factor of 3.36) **and far more significant** ($t=6.98$). **Interestingly, $pill$ is now insignificant once a trend is allowed for.**

**With a quadratic trend:**
$$\widehat{gfr_t}=124.09+0.348\,pe_t-35.88\,ww2_t-10.12\,pill_t-2.53\,t+0.0196\,t^2,\qquad R^2=0.727$$
$$\qquad\quad(4.36)\;(0.040)\qquad(5.71)\qquad\;(6.34)\qquad(0.39)\qquad(0.0050)$$

**$pe$ is larger still and more significant ($t=8.7$); $pill$ now has the expected negative sign and is marginally significant ($t=-1.60$); both trend terms are significant.** *"The quadratic trend is a flexible way to account for the unusual trending behavior of $gfr$"* — which had **both** upward and downward phases over 1913–1984.

> [!warning] Why not a cubic? A quartic? Know when to stop
> **Nothing prevents adding $t^3$, and it may be warranted.** But:
>
> **"We want relatively simple trends that capture broad movements in the dependent variable that are not explained by the independent variables. If we include enough polynomial terms in $t$, then we can track any series pretty well. But this offers little help in finding which explanatory variables affect $y_t$."**
>
> **A trend is a stand-in for what you have not modelled — not a model.**

#### 5c. The detrending interpretation

> [!important] Including a time trend *is* detrending the data first
> By the **Frisch–Waugh** partialling-out result of [[03 - Multiple Regression Analysis - Estimation|ch. 03]] §3-2, $\hat\beta_1$ and $\hat\beta_2$ from
> $$\hat y_t=\hat\beta_0+\hat\beta_1x_{t1}+\hat\beta_2x_{t2}+\hat\beta_3t$$
> can be obtained in two steps:
>
> **(i) Regress each of $y_t$, $x_{t1}$, $x_{t2}$ on a constant and $t$, and save the residuals $\ddot y_t,\ddot x_{t1},\ddot x_{t2}$.** For example $\ddot y_t=y_t-\hat\alpha_0-\hat\alpha_1t$ — **the linearly detrended series.**
>
> **(ii) Regress $\ddot y_t$ on $\ddot x_{t1},\ddot x_{t2}$** (no intercept needed; including one changes nothing, as it is estimated to be zero).
>
> **This gives exactly $\hat\beta_1$ and $\hat\beta_2$.** It holds for any number of regressors and for quadratic or higher-order trends.
>
> **So the estimates of interest come from a regression with no trend, on detrended data.** Omit $t$ and no detrending occurs — **and $y_t$ may seem related to the $x_{tj}$ simply because each contains a trend.** That is Example 10.7 exactly.
>
> **The diagnostic rule:** *"If the trend term is statistically significant, and the results change in important ways when a time trend is added, then the initial results without a trend should be treated with suspicion."*

> [!tip] Include a trend if **any** regressor trends — even when $y$ does not
> If $y_t$ has no noticeable trend but $x_{t1}$ is growing, **omitting a trend may make it look as if $x_{t1}$ has no effect** — **even though movements of $x_{t1}$ *about its trend* do affect $y_t$.** Including $t$ captures this.

**Example 10.9 — Puerto Rican employment revisited.** Adding a linear trend to (10.17):
$$\widehat{\log(prepop_t)}=-8.70-0.169\log(mincov_t)+1.06\log(usgnp_t)-0.032\,t$$
$$\qquad\qquad\qquad(1.30)\;\;(0.044)\qquad\qquad(0.18)\qquad\qquad(0.005)$$
$$n=38,\quad R^2=0.847$$

| | Without trend (10.17) | **With trend (10.38)** |
|---|---|---|
| $\log(usgnp)$ | $-0.012$ (se $0.089$), **insignificant** | $\mathbf{+1.06}$ (se $0.18$), $t=5.89$ |
| $\log(mincov)$ | $-0.154$ (se $0.065$), $t=-2.37$ | $-0.169$ (se $0.044$), $t=-3.84$ |
| $R^2$ | $0.661$ | $\mathbf{0.847}$ |

> [!important] This is the "adding a trend makes a variable *more* significant" case
> **$prepop$ shows no clear trend, but $\log(usgnp)$ has a strong upward one** — a regression of $\log(usgnp)$ on $t$ gives about $0.03$, i.e. **3% growth per year.**
>
> **Read the 1.06 correctly:** *when $usgnp$ increases by 1% **above its long-run trend**, $prepop$ increases by about 1.06%.* **The coefficient is about deviations from trend, not about levels.**
>
> **And the minimum wage coefficient barely moved but became more precise** — its standard error fell from $0.065$ to $0.044$, exactly the "reduce the error variance" benefit of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3e.

#### 5d. $R^2$ when the dependent variable is trending

**Time series $R^2$s are often very high compared with cross-sectional ones. Does that mean we learn more? Not necessarily.**

**Part of it is genuine:** time series data are often **aggregates** (average hourly wages in the whole economy), and aggregates are easier to explain than individual outcomes. **But part of it is an artefact.**

> [!warning] Why a trending $y$ inflates $R^2$
> $$\bar R^2=1-\frac{\hat\sigma_u^2}{\hat\sigma_y^2},\qquad \hat\sigma_y^2=\frac{\text{SST}}{n-1},\quad\text{SST}=\sum_{t=1}^n(y_t-\bar y)^2$$
>
> **Estimating $\sigma_u^2$ is fine, provided a trend is in the regression. The problem is the denominator.**
>
> **When $\mathbb{E}(y_t)$ follows a linear trend, $\text{SST}/(n-1)$ is neither unbiased nor consistent for $\mathrm{Var}(y_t)$** — it does not account for the trend, and can **substantially overstate** the variance. **A big denominator makes $R^2$ look big.**

> [!important] The fix: compute $R^2$ on the detrended dependent variable
> 1. **Regress $y_t$ on $t$** (and $t^2$, … if needed) and save the residuals $\ddot y_t$.
> 2. **Regress $\ddot y_t$ on $x_{t1},x_{t2}$ and $t$.** Then
> $$\boxed{\;R^2_{\text{detrended}}=1-\frac{\text{SSR}}{\sum_{t}\ddot y_t^{\,2}}\;}$$
> **The SSR is identical to that from the original regression** — only the denominator changes.
>
> **Since $\sum\ddot y_t^2\le\sum(y_t-\bar y)^2$ (usually strictly), this $R^2$ is no greater than the usual one, and typically much less.** With a strong trend in $y_t$, **far less.**
>
> **For an adjusted version:** divide SSR by the df in the *usual* regression and $\sum\ddot y_t^2$ by $n-p$, where **$p$ is the number of trend parameters estimated in detrending** ($p=2$ for a linear trend, 3 for a quadratic). **A computationally simple approximation that works fine: report the adjusted $R^2$ from regressing $\ddot y_t$ on $t,\dots,t^p,x_{t1},\dots,x_{tk}$.**

**Example 10.10 — housing investment again.** Equation (10.33) reports $R^2=0.341$ — *"taken literally, we are explaining 34.1% of the variation in $\log(invpc)$."* **Misleading.**

**Detrend $\log(invpc)$ first, then regress on $\log(price)$ and $t$:**
$$R^2=\mathbf{0.008},\qquad \bar R^2\;\text{is actually \textbf{negative}}$$

> [!important] **Movements in $\log(price)$ about its trend have virtually no explanatory power for movements in $\log(invpc)$ about its trend**
> **And this is exactly consistent with the tiny $t$ statistic on $\log(price)$ in (10.33).** *The honest $R^2$ and the honest $t$ statistic tell the same story; the naive $R^2$ was the outlier.*
>
> **"We can always explain a trending variable with some sort of trend, but this does not mean we have uncovered any factors that cause movements in $y_t$."**

> [!warning] One exception — do **not** detrend for $F$ statistics
> **In computing the $R^2$ form of an $F$ statistic for multiple hypotheses, use the usual $R^2$s with no detrending.** The $R^2$ form is **just a computational device**, and the usual formula is always the right one.

#### 5e. Seasonality

**Monthly, quarterly (or weekly, daily) data may exhibit seasonality.** Midwest housing starts are higher in June than January because of weather; retail sales are higher in the fourth quarter because of Christmas. **Model it by letting $\mathbb{E}(y_t)$ differ across months.**

> [!note] Not every series is seasonal, and most published ones are already adjusted
> **Monthly interest and inflation rates show no noticeable seasonal pattern.** And series that do are usually **seasonally adjusted** before publication — quarterly U.S. GDP is the leading example. **Seasonal adjustment is so common that unadjusted data are often unobtainable**, which limits the scope for doing your own.

**When you do have unadjusted data:**

$$y_t=\beta_0+\delta_1 feb_t+\delta_2 mar_t+\cdots+\delta_{11}dec_t+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t$$

> [!important] Eleven dummies for twelve months
> **January is the base month and $\beta_0$ is its intercept** — the $g-1$ rule of [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §3. **With quarterly data, three dummies.**
>
> **If there is no seasonality in $y_t$ once the $x_{tj}$ are controlled for, $\delta_1$ through $\delta_{11}$ are all zero — easily tested with an $F$ test.**
>
> **And exactly as with trends, including seasonal dummies *is* deseasonalizing the data**: by Frisch–Waugh, the slopes equal those from regressing deseasonalized $\ddot y_t$ on deseasonalized $\ddot x_{t1},\ddot x_{t2}$.
>
> **Seasonal dummies can also be interacted with the $x_{tj}$**, to let the effect of $x_{tj}$ differ across the year.

**Example 10.11 — antidumping filings, seasonally checked.** The `BARIUM` data of Example 10.5 are **monthly and not seasonally adjusted**, so the dummies could matter — *it could be that the months just before the suit was filed are systematically high- or low-import months.*

**Adding all 11 monthly dummies and testing joint significance: $p=\mathbf{0.59}$.** **The seasonal dummies are jointly insignificant, and nothing important changes.** (Krupp & Pollard used three seasonal dummies — fall, spring, summer, with winter as base — with essentially the same outcome.)

> [!tip] The right way to report a robustness check
> **The check was necessary because the data were unadjusted; it came out clean; and that is worth one sentence.** Had it not come out clean, the seasonal dummies would have stayed in the model.

---

## ✏️ Exercises

### Exercise 1 — Impact propensity, lag distribution, and the LRP

An FDL model of order 3 is estimated on annual data:
$$\hat y_t=\hat\alpha_0+0.20\,z_t+0.45\,z_{t-1}+0.30\,z_{t-2}+0.10\,z_{t-3}$$

**(a)** State the impact propensity and the LRP.
**(b)** Trace the path of $y$ following a **temporary** one-unit increase in $z$ at time $t$ (normalize $y_{t-1}=0$). At what period does $y$ return to its original level?
**(c)** Trace the **cumulative effects** following a **permanent** one-unit increase at time $t$.
**(d)** With $n=50$ annual observations, how many are actually usable, and why?
**(e)** A researcher reports that none of the four coefficients is individually significant and concludes that $z$ does not affect $y$. Give two reasons this conclusion may be wrong, and say what she should do instead.

> [!example]- Solution
> **(a)**
> $$\textbf{Impact propensity}=\hat\delta_0=\mathbf{0.20}$$
> $$\textbf{LRP}=0.20+0.45+0.30+0.10=\mathbf{1.05}$$
>
> **The impact propensity is always the coefficient on the contemporaneous $z_t$.** A one-unit rise in $z$ raises $y$ immediately by $0.20$ and, if sustained forever, by $1.05$ in total. **The long-run effect is more than five times the immediate one** — the bulk of the response arrives with a lag.
>
> **(b)** With $y_{t-1}$ normalized to 0 and all errors set to zero, **the lag distribution *is* the path of $y$**:
>
> | Period | $y$ | Comment |
> |---|---|---|
> | $t-1$ | $0$ | baseline |
> | $t$ | $\mathbf{0.20}$ | impact |
> | $t+1$ | $\mathbf{0.45}$ | **peak** |
> | $t+2$ | $0.30$ | |
> | $t+3$ | $0.10$ | |
> | $t+4$ | $\mathbf{0}$ | **back to baseline** |
>
> **$y$ returns to its original level at $t+4$** — one period after the last lag in the model, because only $z_t,\dots,z_{t-3}$ appear.
>
> **The peak effect is at the first lag**, not on impact. The normalized weights ($\delta_j/\text{LRP}$) are $0.190,\,0.429,\,0.286,\,0.095$ — **43% of the total response arrives one period after the shock.**
>
> **(c)** For a permanent increase, the cumulative effect at horizon $h$ is $\delta_0+\cdots+\delta_h$:
>
> | Horizon $h$ | Cumulative effect |
> |---|---|
> | $0$ | $0.20$ |
> | $1$ | $0.65$ |
> | $2$ | $0.95$ |
> | $3$ | $\mathbf{1.05}=\text{LRP}$ |
> | $4+$ | $1.05$ — **no further change** |
>
> **After three periods the adjustment is complete.** **The cumulative-effect path is the *integral* of the lag distribution**, and its limit is the LRP.
>
> **Note the contrast with (b): the same four numbers describe a hump-shaped temporary response and a monotonically rising permanent response.** Which one you plot depends on the question.
>
> **(d) 47 observations.** Three are lost to lagging $z$ three times: for $t=1,2,3$ you would need $z_0,z_{-1},z_{-2}$, which precede the sample.
>
> **This is the practical cost of long lag structures**, and it compounds: an FDL of order $q$ costs $q$ observations, **and** $q+1$ parameters. **With 50 annual observations, an FDL of order 8 would leave 42 observations to estimate 10 parameters.** *(The [[00-Index|convention]] adopted in the text is that $z_0,z_{-1},z_{-2}$ are treated as initial values in the sample so the index can start at $t=1$; either way, the estimation sample loses three periods.)*
>
> **(e) Two reasons, and they are the whole point of the section.**
>
> **Reason 1 — multicollinearity.** $z_t$, $z_{t-1}$, $z_{t-2}$, $z_{t-3}$ are usually **highly correlated with one another** (an economic series is persistent). By the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] variance formula
> $$\mathrm{Var}(\hat\delta_j)=\frac{\sigma^2}{\text{SST}_j(1-R_j^2)}$$
> **each $R_j^2$ is near 1, so every standard error is inflated.** The data cannot apportion a shared effect among the lags — **but that is a statement about identification of the individual $\delta_j$, not about whether $z$ matters.**
>
> **Reason 2 — individual $t$ statistics cannot test a joint hypothesis.** The [[04 - Multiple Regression Analysis - Inference|ch. 04]] lesson, and it recurs here in its purest form. **"$z$ has no effect" is $H_0:\delta_0=\delta_1=\delta_2=\delta_3=0$ — four restrictions, requiring an $F$ test.**
>
> **What she should do:**
> 1. **Run the joint $F$ test** of all four $\delta_j=0$. In Example 10.4, exactly this situation gave individual $t$'s of $0.58$, $-0.04$ and $0.27$ — and a joint **$p=0.012$**.
> 2. **Estimate the LRP and its standard error** via the reparameterization of Exercise 3. **The LRP is often precisely estimated even when no individual coefficient is.** In Example 10.4 the LRP had $t=\mathbf{3.37}$.
> 3. **Consider whether a static model suffices.** If the lags are jointly insignificant *given* $z_t$ (in Example 10.4, $p=0.95$ for $pe_{t-1},pe_{t-2}$), **drop them** — you regain observations and precision.

---

### Exercise 2 — TS.3: strict versus contemporaneous exogeneity

**(a)** State TS.3 formally and explain what $\mathbf{X}$ denotes.
**(b)** Distinguish strict from contemporaneous exogeneity. Which is needed for unbiasedness and which for consistency?
**(c)** Why is there no analogue of TS.3 in the cross-sectional assumptions?
**(d)** For $mrdrte_t=\beta_0+\beta_1 polpc_t+u_t$, explain precisely how TS.3 can fail even if $u_t$ is uncorrelated with $polpc_t$ and all *past* values of $polpc$.
**(e)** Classify as plausibly strictly exogenous or not: rainfall in a crop yield equation; farm labour input; the federal funds rate in a GDP equation; a state's speed limit in a traffic-fatality equation. Then say why we assume TS.3 anyway.

> [!example]- Solution
> **(a)** $$\boxed{\;\mathbb{E}(u_t\mid\mathbf{X})=0,\qquad t=1,2,\dots,n\;}$$
>
> **$\mathbf{X}$ is the entire $n\times k$ array of regressors — every explanatory variable in every time period.** Row $t$ is $\mathbf{x}_t=(x_{t1},\dots,x_{tk})$; the first row is $t=1$, the last is $t=n$. *(This is exactly how software stores the data.)*
>
> **Read it as uncorrelatedness: $u_t$ is uncorrelated with each explanatory variable in every time period.** And since it is a conditional expectation, **it also requires the functional form to be correctly specified.**
>
> **(b)**
>
> | | Condition | Restricts |
> |---|---|---|
> | **Contemporaneous exogeneity** | $\mathbb{E}(u_t\mid\mathbf{x}_t)=0$ | Only period-$t$ regressors |
> | **Strict exogeneity (TS.3)** | $\mathbb{E}(u_t\mid\mathbf{X})=0$ | **All periods — past, present and future** |
>
> $$\textbf{Unbiasedness (Theorem 10.1) requires \textbf{strict} exogeneity.}$$
> $$\textbf{Consistency ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]) requires only \textbf{contemporaneous} exogeneity.}$$
>
> **This asymmetry is the reason [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] exists.** Strict exogeneity is often indefensible; giving up **finite-sample unbiasedness** in exchange for **large-sample consistency** buys a far more realistic assumption. **The same trade appears in [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]]** — asymptotics purchases weaker assumptions.
>
> **(c) Because random sampling (MLR.2) delivered it silently.**
>
> Under random sampling, **$u_i$ is automatically independent of the explanatory variables for every *other* observation $i$** — and it can be shown this holds conditional on all the regressors in the sample. **There was nothing to assume.**
>
> **With time series, random sampling is almost never appropriate**, so the relationship between $u_t$ and the regressors in **other** periods must be stated explicitly. **TS.3 replaces MLR.2 and MLR.4 together.**
>
> **Note also that TS.3 restricts nothing about correlation among the regressors over time, or among the $u_t$ over time.** Serial correlation of the errors is a **separate** assumption (TS.5), and persistence in $inf_t$ or $polpc_t$ is simply irrelevant to TS.3.
>
> **(d) Through feedback — a violation that runs forward in time.**
>
> Grant the premise: $\mathrm{Corr}(u_t,polpc_t)=0$ and $\mathrm{Corr}(u_t,polpc_s)=0$ for all $s<t$. **TS.3 still requires $\mathrm{Corr}(u_t,polpc_s)=0$ for $s>t$.**
>
> **Suppose the city sets its police force in response to past murder rates.** Then:
> $$u_t\uparrow\;\Longrightarrow\;mrdrte_t\uparrow\;\Longrightarrow\;polpc_{t+1}\uparrow$$
>
> **So $polpc_{t+1}$ is correlated with $u_t$, and TS.3 fails.**
>
> **The contemporaneous relationship is entirely innocent.** What breaks the assumption is that the regressor **reacts to what happened to $y$.** *"Explanatory variables that are strictly exogenous cannot react to what has happened to $y$ in the past."*
>
> **The same issue arises in distributed lag models.** We usually do not worry about $u_t$ being correlated with **past** $z$ — we are controlling for past $z$ in the model. **But feedback from $u$ to future $z$ is always an issue.**
>
> **(e)**
>
> | Variable | Strictly exogenous? | Why |
> |---|---|---|
> | **Rainfall** in a crop-yield equation | ✅ **Yes** | Future rainfall is not influenced by current or past output |
> | **Farm labour input** | ❌ **No** | The farmer **chooses** it, and may adjust based on last year's yield |
> | **Federal funds rate** in a GDP equation | ❌ **No** | **The Fed sets it in response to output and inflation** — textbook feedback |
> | **State speed limit** in a fatality equation | ❌ **No** | A policy variable; legislatures respond to fatality rates |
>
> **The pattern: natural phenomena qualify; anything chosen by an agent who observes $y$ does not.** *"Policy variables, such as growth in the money supply, expenditures on welfare, and highway speed limits, are often influenced by what has happened to the outcome variable in the past. In the social sciences, many explanatory variables may very well violate the strict exogeneity assumption."*
>
> **Why assume it anyway — two reasons.**
>
> 1. **It is the price of finite-sample unbiasedness.** Without TS.3, OLS **cannot be shown to be unbiased**, and the whole apparatus of Theorems 10.1–10.5 collapses. **The CLM framework is a good starting point** even where it is not the finishing point.
>
> 2. **The alternative in the literature is worse.** Most treatments obtain TS.3 by the **stronger** assumption that the regressors are **non-random, or "fixed in repeated samples."** That is **obviously false** for time series — you cannot re-run 1974 with different inflation. **TS.3 is more honest: it keeps the $x_{tj}$ random and isolates exactly the condition required.**
>
> **And the escape route is signposted:** [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] shows OLS is still **consistent** under contemporaneous exogeneity alone, which is what makes lagged dependent variables and most policy regressors usable.

---

### Exercise 3 — The long-run propensity and its standard error

From equation (10.19), fitted on $n=70$ annual observations:

| Coefficient | Estimate | se | $t$ |
|---|---|---|---|
| $pe_t$ | $0.073$ | $0.126$ | $0.58$ |
| $pe_{t-1}$ | $-0.0058$ | $0.1557$ | $-0.04$ |
| $pe_{t-2}$ | $0.034$ | $0.126$ | $0.27$ |

**(a)** Compute the estimated LRP.
**(b)** Explain why $\mathrm{se}(\widehat{\text{LRP}})$ cannot be computed from this table.
**(c)** Derive the reparameterization that delivers the LRP as a single coefficient, stating exactly which regression to run.
**(d)** The reparameterized regression gives $\mathrm{se}(\hat\theta_0)=0.030$. Compute $t$ and a 95% CI. Then compute what $\mathrm{se}(\widehat{\text{LRP}})$ would be **if the three estimators were uncorrelated**, and interpret the discrepancy.
**(e)** Not one coefficient is individually significant, yet the LRP is highly significant. Is this a contradiction? What does it tell you about what the data can and cannot identify?

> [!example]- Solution
> **(a)** $$\widehat{\text{LRP}}=0.073+(-0.0058)+0.034=\mathbf{0.1012}\approx0.101$$
>
> **A permanent \$1 increase in the personal exemption raises the general fertility rate by about 0.10 births per 1,000 women of childbearing age**, once all adjustment is complete.
>
> **(b) Because the variance of a sum requires the covariances, and the table does not report them.**
>
> $$\mathrm{Var}(\hat\delta_0+\hat\delta_1+\hat\delta_2)=\sum_{j}\mathrm{Var}(\hat\delta_j)+2\sum_{j<k}\mathrm{Cov}(\hat\delta_j,\hat\delta_k)$$
>
> **The standard errors give the three variances. The three covariances are nowhere in the output** — they live in the estimated covariance matrix, which regression tables do not print.
>
> **And these covariances are not a technicality here.** Because $pe_t$, $pe_{t-1}$ and $pe_{t-2}$ are strongly correlated, the estimators are **strongly correlated too** — see (d).
>
> *(This is exactly the [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4 problem, and the same problem as testing the difference between two non-base dummy groups in [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §3.)*
>
> **(c)** Define $\theta_0=\delta_0+\delta_1+\delta_2$, so $\delta_0=\theta_0-\delta_1-\delta_2$. Substitute into
> $$gfr_t=\alpha_0+\delta_0 pe_t+\delta_1 pe_{t-1}+\delta_2 pe_{t-2}+\cdots$$
> $$=\alpha_0+(\theta_0-\delta_1-\delta_2)pe_t+\delta_1 pe_{t-1}+\delta_2 pe_{t-2}+\cdots$$
> $$\boxed{\;=\alpha_0+\theta_0\,pe_t+\delta_1\left(pe_{t-1}-pe_t\right)+\delta_2\left(pe_{t-2}-pe_t\right)+\cdots\;}$$
>
> **Run the regression**
> $$gfr_t \;\text{ on }\; pe_t,\;(pe_{t-1}-pe_t),\;(pe_{t-2}-pe_t),\;ww2_t,\;pill_t$$
>
> **The coefficient on $pe_t$ is $\hat\theta_0=\widehat{\text{LRP}}$, and the package prints its standard error.**
>
> > **Two checks that you did it right:** the coefficient on $pe_t$ must come out at $0.101$ (which we already knew), and **$R^2$, SSR, $\hat\sigma$ and the $ww2$/$pill$ coefficients must be identical to (10.19)** — this is a **pure reparameterization**, not a different model. If anything else moved, a variable was built wrong.
>
> **(d)** $$t=\frac{0.101}{0.030}=\mathbf{3.37}$$
> With $df=70-5-1=64$, $t_{.025}\approx1.998$:
> $$\text{95\% CI}=0.101\pm1.998(0.030)=[\mathbf{0.041},\;\mathbf{0.160}]$$
> **The LRP is statistically different from zero at very small significance levels.**
>
> **Now the counterfactual.** If $\hat\delta_0,\hat\delta_1,\hat\delta_2$ were **uncorrelated**, the variance of their sum would be just the sum of variances:
> $$\mathrm{Var}=0.126^2+0.1557^2+0.126^2=0.01588+0.02424+0.01588=0.05599$$
> $$\mathrm{se}=\sqrt{0.05599}=\mathbf{0.237}$$
>
> **That is 7.9 times the actual standard error of 0.030.** Working backwards:
> $$2\sum_{j<k}\mathrm{Cov}(\hat\delta_j,\hat\delta_k)=0.030^2-0.05599=\mathbf{-0.0551}$$
>
> > **The covariances are large and strongly negative — and that is exactly what collinearity among the lags produces.** When $pe_t$, $pe_{t-1}$ and $pe_{t-2}$ move together, OLS can trade off the coefficients against one another: **push $\hat\delta_0$ up and $\hat\delta_1$ comes down, leaving the fit almost unchanged.** Each individual estimate is therefore very imprecise, **but their sum is nearly pinned down**, because the trade-offs cancel in the sum.
> >
> > **The negative covariances are not a nuisance — they are the reason the LRP is precisely estimated.**
>
> **(e) No contradiction whatsoever. The two statements are about different parameters.**
>
> - **"$\hat\delta_1$ is insignificant"** means the data cannot determine how much of the effect arrives **one year later**.
> - **"$\hat\theta_0$ is significant"** means the data can determine the **total** effect very well.
>
> **What the data identify:** **the sum $\delta_0+\delta_1+\delta_2$**, sharply.
> **What the data do not identify:** **the allocation of that sum across the three lags.**
>
> **The economic reading is clean.** *"$pe$ does have an effect on $gfr$, but we do not have good enough estimates to determine whether it is contemporaneous or with a one- or two-year lag (or some of each)."* **The joint $F$ test confirms it: $p=0.012$ for the three $pe$ terms together.**
>
> **And it is corroborated by the static model.** In (10.18), $pe_t$ alone has $t=2.77$ — with a single regressor there is no collinearity to destroy the precision. **Indeed $pe_{t-1}$ and $pe_{t-2}$ are jointly insignificant ($p=0.95$), so the static model is defensible here** — the LRP exercise was for illustration.
>
> > **The general lesson, which recurs throughout time series work: report the LRP, not the individual lag coefficients.** Whittington, Alm & Peters allowed further lags but had to **restrict the coefficients** to fight the collinearity. **For the LRP — usually the object of economic interest — no such restrictions are needed.**

---

### Exercise 4 — Trends and spurious regression

A researcher regresses $\log(invpc)$ on $\log(price)$ using 42 annual observations and obtains a price elasticity of $1.241$ (se $0.382$). Regressing $\log(invpc)$ on $t$ gives a trend coefficient of $0.0081$; regressing $\log(price)$ on $t$ gives $0.0044$.

**(a)** Compute the $t$ statistic on the elasticity and test whether it differs from 1.
**(b)** Adding $t$ to the regression gives $-0.381$ (se $0.679$) on $\log(price)$ and $0.0098$ (se $0.0035$) on $t$. What happened, and what is the correct conclusion?
**(c)** Explain the **detrending interpretation**: state the two-step procedure that reproduces the trend-inclusive slopes exactly, and name the result it rests on.
**(d)** In a different application, $y_t$ has no visible trend but $x_{t1}$ grows at 3% a year. Should a trend be included? Explain what omitting it would do.
**(e)** Why not add $t^3$, $t^4$, … until the fit is excellent?

> [!example]- Solution
> **(a)** $$t_{H_0:\beta_1=0}=\frac{1.241}{0.382}=\mathbf{3.25}$$ — **highly significant.**
> $$t_{H_0:\beta_1=1}=\frac{1.241-1}{0.382}=\frac{0.241}{0.382}=\mathbf{0.63}$$ — **not different from 1.**
>
> **Taken at face value: a very large, unit-elastic supply response of housing investment to price.** *"We must be careful here."*
>
> **The warning sign is already visible in the auxiliary regressions.** Both series trend upward — $\log(invpc)$ at about 0.81% a year, $\log(price)$ at about 0.44% a year. **Two upward-trending series will appear correlated whether or not either causes the other.**
>
> *(The standard errors on those trend coefficients are **not reliable** — such regressions typically contain substantial serial correlation, violating TS.5 — but the point estimates do establish that trends are present.)*
>
> **(b) The result reverses completely, and the original one was spurious.**
>
> | | Without trend | **With trend** |
> |---|---|---|
> | $\log(price)$ | $+1.241$, $t=3.25$ | $\mathbf{-0.381}$, $t=\mathbf{-0.56}$ |
> | $t$ | — | $0.0098$, $t=\mathbf{2.80}$ |
> | $R^2$ | $0.208$ | $0.341$ |
>
> **The elasticity changes sign, loses two-thirds of its magnitude, and becomes thoroughly insignificant. The trend is significant, implying about 1% growth in $invpc$ per year on average.**
>
> **The correct conclusion:** *"We cannot conclude that real per capita housing investment is influenced at all by price."* **There are other factors, captured by the trend, that drive $invpc$ — and we have not modelled them.**
>
> **Why the original was biased:** omitting $t$ when $y_t$ genuinely depends on it is **omitting a relevant variable** ([[03 - Multiple Regression Analysis - Estimation|ch. 03]]). **The bias is severe precisely because $\log(price)$ is itself trending, hence highly correlated with the omitted $t$.**
>
> **(c) By the Frisch–Waugh partialling-out result** ([[03 - Multiple Regression Analysis - Estimation|ch. 03]] §3-2):
>
> **Step (i).** Regress **each** of $y_t$ and every $x_{tj}$ on a constant and $t$; save the residuals:
> $$\ddot y_t=y_t-\hat\alpha_0-\hat\alpha_1t,\qquad \ddot x_{tj}=x_{tj}-\hat\gamma_{0j}-\hat\gamma_{1j}t$$
> **These are the linearly detrended series.**
>
> **Step (ii).** Regress $\ddot y_t$ on $\ddot x_{t1},\ddot x_{t2},\dots$ **No intercept is needed** (including one changes nothing — it is estimated as zero).
>
> **This reproduces $\hat\beta_1,\hat\beta_2,\dots$ from the trend-inclusive regression exactly.** It holds for any number of regressors and for quadratic or higher-order trends.
>
> > **The interpretation this licenses:** *the estimates of interest come from a regression with no trend, but on data from which the trends have first been removed.* **They are about co-movement around the trends, not about levels.**
> >
> > **And it explains part (b) mechanically:** omit $t$ and **no detrending occurs**, so $y_t$ can seem related to $x_{tj}$ merely because each contains a trend.
> >
> > **The diagnostic rule:** *"If the trend term is statistically significant, and the results change in important ways when a time trend is added, then the initial results without a trend should be treated with suspicion."* **Both conditions hold in (b).**
>
> **(d) Yes — include the trend.** This is the case that catches people out, because the usual worry ("$y$ is trending") does not apply.
>
> **What omitting it would do: make $x_{t1}$ look irrelevant when it is not.**
>
> **The mechanism, via (c).** With $t$ in the regression, $\hat\beta_1$ is the slope from regressing **detrended $y$** on **detrended $x_1$** — i.e. it measures whether **movements of $x_{t1}$ about its trend** move $y_t$ about its trend. **Omit $t$ and $x_{t1}$ enters undetrended**, so most of its variation is the 3%-a-year growth — variation that $y_t$, having no trend, cannot match. **That trend variation is pure noise for explaining $y_t$, and it dilutes the signal in the deviations.**
>
> **Example 10.9 is precisely this case.** $prepop$ shows no clear trend; $\log(usgnp)$ grows about 3% a year:
>
> | | Without trend | **With trend** |
> |---|---|---|
> | $\log(usgnp)$ | $-0.012$ (se $0.089$), **insignificant** | $\mathbf{+1.06}$ (se $0.18$), $t=5.89$ |
> | $\log(mincov)$ | $-0.154$ (se $0.065$) | $-0.169$ (se $\mathbf{0.044}$) |
> | $R^2$ | $0.661$ | $0.847$ |
>
> **And the coefficient must be read accordingly:** *when $usgnp$ rises 1% **above its long-run trend**, $prepop$ rises about 1.06%.*
>
> **A bonus:** the minimum-wage standard error fell from $0.065$ to $0.044$ — **the trend absorbed error variance without inducing collinearity with $\log(mincov)$**, exactly the free-precision case of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3e.
>
> **The rule: include a trend if *any* variable in the model trends, whether or not $y$ does.**
>
> **(e) Because a high-order polynomial in $t$ will fit anything, and teach you nothing.**
>
> **Nothing forbids $t^3$** — Wooldridge notes it may even be warranted for the fertility data. **But:**
>
> > *"We want relatively simple trends that capture broad movements in the dependent variable that are not explained by the independent variables in the model. If we include enough polynomial terms in $t$, then we can track any series pretty well. But this offers little help in finding which explanatory variables affect $y_t$."*
>
> **A trend is not a model — it is a placeholder for what you have not modelled.** Every polynomial term you add:
> - **spends a degree of freedom** (and time series samples are small — 42 observations here);
> - **absorbs variation the economic regressors might have explained**, biasing you toward finding nothing;
> - **has no interpretation** — you cannot say what $\hat\alpha_4$ means.
>
> **The discipline is [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3d's over-controlling warning applied to trends: chasing fit is not the objective.** In Example 10.8, the quadratic was justified because **$gfr$ genuinely had both upward and downward phases over 1913–1984** — a *substantive* reason, not a fit-based one.

---

### Exercise 5 — $R^2$ with a trending dependent variable, and seasonality

A time series regression of $y_t$ on $x_{t1}$ and $t$ ($n=42$) yields $\text{SSR}=0.90$ and $\sum_t(y_t-\bar y)^2=15.0$. Detrending $y_t$ first gives $\sum_t\ddot y_t^{\,2}=1.20$.

**(a)** Compute the usual $R^2$ and the detrended $R^2$. Which should be reported, and why?
**(b)** Compute the adjusted detrended $R^2$, being explicit about the degrees of freedom in each term.
**(c)** The researcher now wants an $F$ test of two exclusion restrictions. Should she use the detrended $R^2$s? Explain.
**(d)** She has monthly, seasonally unadjusted data. Write the model with seasonal dummies, state how many are needed, and say how to test for seasonality.
**(e)** Her seasonal dummies are jointly insignificant ($p=0.59$) and nothing else changes. Was the exercise a waste of time?

> [!example]- Solution
> **(a)**
> $$R^2_{\text{usual}}=1-\frac{\text{SSR}}{\sum(y_t-\bar y)^2}=1-\frac{0.90}{15.0}=\mathbf{0.94}$$
> $$R^2_{\text{detrended}}=1-\frac{\text{SSR}}{\sum\ddot y_t^{\,2}}=1-\frac{0.90}{1.20}=\mathbf{0.25}$$
>
> **Note that the SSR is identical in both — only the denominator changes.**
>
> **Report the detrended one, $0.25$.** The usual figure is inflated by the trend.
>
> **Why.** $\bar R^2=1-\hat\sigma_u^2/\hat\sigma_y^2$ with $\hat\sigma_y^2=\text{SST}/(n-1)$. **Estimating $\sigma_u^2$ is fine provided a trend is in the regression. The denominator is the problem:** when $\mathbb{E}(y_t)$ follows a linear trend, **$\text{SST}/(n-1)$ is neither unbiased nor consistent for $\mathrm{Var}(y_t)$** — it does not account for the trend and **substantially overstates** the variance. A big denominator makes $R^2$ look big.
>
> **Here $\sum(y_t-\bar y)^2=15.0$ but $\sum\ddot y_t^{\,2}=1.20$ — 92% of the apparent variation in $y_t$ is just its trend.** *"We can always explain a trending variable with some sort of trend, but this does not mean we have uncovered any factors that cause movements in $y_t$."*
>
> **Example 10.10 is the extreme version:** the housing-investment equation reports $R^2=0.341$, but on detrended $\log(invpc)$ it collapses to **$0.008$, with a negative adjusted $R^2$** — **entirely consistent with the tiny $t$ statistic on $\log(price)$.** *The honest $R^2$ and the honest $t$ agree; the naive $R^2$ was the outlier.*
>
> **(b)** Two different degrees-of-freedom corrections:
> - **SSR** is divided by the df in the **usual regression**: $n-k-1$ where $k=2$ ($x_{t1}$ and $t$), so $42-3=\mathbf{39}$.
> - **$\sum\ddot y_t^{\,2}$** is divided by $n-p$, where **$p$ is the number of trend parameters estimated in detrending** — for a linear trend $p=2$ (intercept and slope), so $42-2=\mathbf{40}$.
>
> $$\bar R^2_{\text{detrended}}=1-\frac{0.90/39}{1.20/40}=1-\frac{0.023077}{0.030}=\mathbf{0.231}$$
>
> **The two denominators are different numbers and it matters.** *(For a quadratic trend, $p=3$.)*
>
> > **The practical shortcut:** rather than assembling this by hand, **regress $\ddot y_t$ on $t,\dots,t^p,x_{t1},\dots,x_{tk}$ and read off the package's adjusted $R^2$.** Wooldridge (1991a) gives detailed df corrections, but this approximation is fine.
>
> **(c) No — use the usual $R^2$s, with no detrending.**
>
> $$F=\frac{(R^2_{ur}-R^2_r)/q}{(1-R^2_{ur})/(n-k-1)}$$
>
> **The $R^2$ form of the $F$ statistic is *just a computational device*, and the usual formula is always appropriate.** It is derived from $\text{SSR}_r-\text{SSR}_{ur}$ by dividing through by a **common SST**; any consistent choice of SST cancels, so substituting detrended $R^2$s would be gratuitous — and if applied inconsistently, wrong.
>
> **This is the mirror image of the [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3b rule that $\bar R^2$ must never enter the $F$ formula.** *Two different corrections, one common principle: the $F$ statistic uses the raw $R^2$.*
>
> **(d)** With January as the base month:
> $$y_t=\beta_0+\delta_1 feb_t+\delta_2 mar_t+\cdots+\delta_{11}dec_t+\beta_1x_{t1}+\cdots+\beta_kx_{tk}+u_t$$
>
> **Eleven dummies for twelve months** — the $g-1$ rule of [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §3. **Including all twelve with an intercept is the dummy variable trap.** $\beta_0$ is January's intercept; each $\delta_j$ is the difference from January. **(With quarterly data: three dummies.)**
>
> **Testing for seasonality:** if there is none in $y_t$ once the $x_{tj}$ are controlled for, then $\delta_1=\cdots=\delta_{11}=0$ — **an ordinary $F$ test with $q=11$.**
>
> **And note the parallel with trends: including seasonal dummies *is* deseasonalizing the data.** By Frisch–Waugh, the slopes equal those from regressing deseasonalized $\ddot y_t$ on deseasonalized $\ddot x_{tj}$ — where "deseasonalized" means residuals from a regression on the monthly dummies. **The interpretation is that the $\hat\beta_j$ measure co-movement *net of* the normal seasonal pattern.**
>
> **Seasonal dummies can also be interacted with the $x_{tj}$**, letting the effect of $x_{tj}$ differ across the year.
>
> **(e) No — it was necessary, and reporting it in one sentence is exactly right.**
>
> **Three reasons the check had to be done.**
>
> 1. **The data are unadjusted, so seasonality was a live possibility.** Most published macro series are seasonally adjusted, so the issue rarely arises — **but when it does, an unmodelled seasonal pattern in $y_t$ sits in the error term** and, if correlated with a regressor, biases the estimates.
>
> 2. **In an event study, the risk is specific and serious.** The `BARIUM` dummies mark six-month windows around a filing date. **If the months just before the suit happen to be systematically high- or low-import months, the `befile6` coefficient would pick that up and be read as evidence about the filing.** *The dummy would be measuring the calendar, not the event.*
>
> 3. **You cannot know the answer without running it.** "Jointly insignificant" is a **result**, not an assumption.
>
> **What a clean result licenses.** With $p=0.59$ and no meaningful change in the other estimates, **the seasonal dummies can be dropped**, regaining 11 degrees of freedom — worth having with $n=131$. **The published conclusions stand as reported.** (Krupp & Pollard used three seasonal dummies rather than eleven and reached essentially the same outcome — **a reminder that the specific parameterization rarely matters when the effect is absent.**)
>
> **Had the dummies been significant, they would stay in the model** — and any conclusion about `befile6` drawn without them would have to be revisited.
>
> > **The general principle: a robustness check that comes out clean is not wasted work. It is the reason you are entitled to report the simpler model.**

---

## 📝 Summary

- **A time series is one realization of a stochastic process.** The set of all possible realizations plays the role of the population; the number of periods plays the role of the sample size. **We can never observe a second realization.**
- **A static model** relates $y_t$ to contemporaneous $z_t$; a **finite distributed lag model** lets $z$ act with a lag. **The impact propensity $\delta_0$ is the immediate effect; the lag distribution $\{\delta_j\}$ traces a temporary shock; the cumulative effects trace a permanent one; and the LRP $=\sum_j\delta_j$ is the total long-run response.**
- **Lags of an economic series are highly collinear, so the individual $\hat\delta_j$ are usually imprecise — but the LRP often is not.** Obtain it, and its standard error, by rewriting the model as $$y_t=\alpha_0+\theta_0 z_t+\delta_1(z_{t-1}-z_t)+\delta_2(z_{t-2}-z_t)+\cdots$$ and reading off the coefficient on $z_t$. In Example 10.4 no $\hat\delta_j$ had $|t|>0.6$ while the LRP had $t=3.37$.
- **TS.1–TS.6 replace MLR.1–MLR.6, and every theorem carries over unchanged:** OLS is unbiased (TS.1–3), $\mathrm{Var}(\hat\beta_j)=\sigma^2/[\text{SST}_j(1-R_j^2)]$ and BLUE (TS.1–5), and $t$ and $F$ statistics have exact distributions (TS.1–6).
- **The cost is TS.3, strict exogeneity: $u_t$ uncorrelated with the regressors in *every* period, past and future.** It replaces random sampling, and it **rules out any feedback from $y$ to future $x$** — so policy variables, choice variables and anything set in response to past outcomes generally violate it. **Contemporaneous exogeneity alone suffices for *consistency* ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]).**
- **TS.5, no serial correlation, is entirely new** — random sampling had made it automatic in cross-sections. **It concerns the errors only; persistence in the regressors is irrelevant to it.**
- **Dummy variables in time series mark periods**, and are the basis of **event studies**, where a market return is included to control for broad movements coinciding with the event. **Index numbers are meaningless without a base period; rebase with $100(\text{old}_t/\text{old}_{\text{new base}})$; and deflate nominal series by CPI/100** — U.S. nominal wages nearly tripled from 1973 to 1995 while real wages **fell**.
- **A model in real terms imposes a testable restriction:** $\log(hours)=\beta_0+\beta_1\log(w)+\beta_2\log(p)+u$ with $\beta_2=-\beta_1$. **Rejecting it is evidence of money illusion.**
- **Two trending series will appear related whether or not either causes the other — the spurious regression problem.** Adding a time trend fixes it: housing investment's price elasticity fell from $+1.24$ ($t=3.25$) to $-0.38$ ($t=-0.56$) once a trend was included.
- **Including a trend *is* detrending the data first** (Frisch–Waugh), so the slopes describe co-movement **around** the trends. **Include a trend whenever *any* variable trends — even if $y$ does not**: Puerto Rican employment's GNP elasticity went from $-0.01$ (insignificant) to $+1.06$ ($t=5.89$) once a trend was added.
- **When $y_t$ trends, the usual $R^2$ is inflated**, because $\text{SST}/(n-1)$ overstates $\mathrm{Var}(y_t)$. **Report $1-\text{SSR}/\sum\ddot y_t^{\,2}$ instead** — for the housing equation this cuts $0.341$ to $\mathbf{0.008}$. **But use the ordinary $R^2$s inside an $F$ statistic.**
- **Seasonality is handled with $g-1$ seasonal dummies**, tested jointly by $F$, and including them **deseasonalizes** the data in exactly the same Frisch–Waugh sense.

---

## ⚠️ Important Notes

> [!warning] The eleven mistakes this chapter is designed to prevent
>
> 1. **Concluding "$z$ has no effect" because no individual lag coefficient is significant.** Collinearity among lags destroys the individual estimates. **Run the joint $F$ test and estimate the LRP.**
> 2. **Trying to compute $\mathrm{se}(\widehat{\text{LRP}})$ from the printed standard errors.** You need the covariances, which are large and **negative**. Reparameterize.
> 3. **Treating strict exogeneity as though it were just MLR.4.** It also forbids **feedback from $y$ to future $x$** — which most policy and choice variables exhibit.
> 4. **Thinking TS.5 is about the regressors.** $inf_t$ is persistent; that has nothing to do with whether the **errors** are serially correlated.
> 5. **Interpreting a regression of two trending series causally.** The classic spurious regression. **Add a trend and see whether the result survives.**
> 6. **Omitting a trend because $y_t$ does not trend.** If a **regressor** trends, its trend variation swamps the deviations that actually carry the signal — Example 10.9 exactly.
> 7. **Reading a trend-inclusive coefficient as a level effect.** It is about **deviations from trend**: *"when $usgnp$ increases by 1% above its long-run trend…"*
> 8. **Reporting a high $R^2$ from a trending dependent variable.** $0.341$ becomes $0.008$ once $\log(invpc)$ is detrended.
> 9. **Detrending inside an $F$ statistic.** The $R^2$ form is a computational device; **always use the usual $R^2$s.**
> 10. **Adding polynomial trends until the fit is good.** Enough powers of $t$ will track anything — **and teach you nothing about which regressors matter.**
> 11. **Skipping the seasonality check on unadjusted data.** In an event study, a seasonal pattern can masquerade as the event.

> [!important] The four ideas most likely to be examined
>
> **1. Impact propensity, lag distribution, cumulative effect, LRP.** Know that the lag distribution traces a **temporary** shock and the cumulative effects trace a **permanent** one, and be able to derive both by writing out $y_{t-1},y_t,y_{t+1},\dots$ with the errors set to zero.
>
> **2. The LRP reparameterization.** $\delta_0=\theta_0-\delta_1-\delta_2$ gives $$y_t=\alpha_0+\theta_0z_t+\delta_1(z_{t-1}-z_t)+\delta_2(z_{t-2}-z_t)+\cdots$$ **Be able to derive it in one line and state which regression to run.** It is the same device as [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4, [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4a and [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §3.
>
> **3. Strict vs contemporaneous exogeneity — the distinction, and which theorem needs which.** **Strict ⇒ unbiasedness (Theorem 10.1); contemporaneous ⇒ consistency ([[11 - Further Issues in Using OLS with Time Series Data|ch. 11]]).** Be able to give the police/murder feedback example and explain that the violation runs **forward** in time.
>
> **4. The detrending interpretation and the corrected $R^2$.** Frisch–Waugh: including $t$ is detrending everything first. And $$R^2_{\text{detrended}}=1-\frac{\text{SSR}}{\sum_t\ddot y_t^{\,2}}$$ with **SSR from the usual regression** and $\sum\ddot y_t^{\,2}$ replacing SST. Know the two different df corrections.

> [!note] Cross-subject connections
> - **This chapter is the regression-side view of what [[Time-series Analysis/contents/00-Index|Time-series Analysis]] covers from the stochastic-process side.** Trends and deterministic detrending appear in [[Time-series Analysis/contents/02 - Trend, Seasonality and Decomposition|TS ch. 02]]; **spurious regression is treated properly in [[11 - Further Issues in Using OLS with Time Series Data|ch. 11]] here and in [[Time-series Analysis/contents/08 - VECM and Cointegration|TS ch. 08]] there.** The two treatments complement each other: **Wooldridge asks whether OLS coefficients mean anything; the TS course asks what the data-generating process is.**
> - **Distributed lag models are the regression form of an impulse response function.** The lag distribution $\{\delta_j\}$ **is** the IRF of $y$ to a unit shock in $z$, and the cumulative effect is the **step response**. In [[Time-series Analysis/contents/07 - SARIMA and Vector Autoregression|TS ch. 07]] and [[Time-series Analysis/contents/10 - Structural Vector Autoregression|TS ch. 10]] the same object is computed from a VAR, where $z$ is endogenous — **which is exactly the strict-exogeneity failure this chapter warns about.**
> - **Seasonal dummies are the deterministic-seasonality approach**; [[Time-series Analysis/contents/07 - SARIMA and Vector Autoregression|SARIMA]] models handle **stochastic** seasonality instead. **Dummies assume the pattern is fixed across years; seasonal differencing does not.**
> - **The detrending/deseasonalizing interpretation is Frisch–Waugh**, the same partialling-out result behind [[03 - Multiple Regression Analysis - Estimation|ch. 03]]'s omitted variable bias formula and behind **residualization** in ML feature engineering.
> - **The index-number and real-vs-nominal material is core [[Principle of Accounting/contents/00-Index|accounting]] and macro literacy** — deflating a series before analysis is the single most common failure in applied work on financial data, and it is a **data preparation** step in [[Data Preparation and Visualization/contents/00-Index|DPV]] terms.
> - **Event studies** are the econometric ancestor of **A/B test analysis with a control series** and of **difference-in-differences**: the market return $R_t^m$ plays the role of the control group.
> - **"Include enough polynomial terms and you can track any series"** is **overfitting**, stated in 1930s vocabulary — the same warning that motivates cross-validation and regularization in [[Machine Learning/contents/00-Index|ML]].

> [!warning] Gaps in the source material
> - **No lecture slides exist for Econometrics.** Chapter scope (Wooldridge 1–12) is my own editorial decision — see [[00-Index]].
> - **No data files are in the vault.** `PHILLIPS`, `INTDEF`, `PRMINWGE`, `FERTIL3`, `BARIUM`, `FAIR`, `HSEINV` and `EARNS` are referenced here and **none can be re-estimated.** All coefficients, standard errors and $R^2$ values are **quoted as printed.**
> - **Internal consistency verified wherever checkable, and it holds throughout:** the Phillips curve $t$ statistic ($1.965$, matching "about 1.96") and its $p$-value ($0.054$ vs the printed $0.055$); both `INTDEF` $t$ statistics; the `PRMINWGE` elasticity $t$ ($-2.37$); the $\$12\times0.083=0.996$ fertility calculation; the LRP ($0.1012$), its $t$ ($3.37$) and its CI ($[0.041,0.161]$ against the printed $[0.041,0.160]$); the exact percentage for `afdec6` ($-43.16\%$ vs the printed $-43.2\%$); the exchange-rate unit-elasticity test ($t=-0.04$); **the full 1996 election prediction ($0.50105$, matching the printed $0.5011$)**; all `HSEINV` and `FERTIL3` trend-model $t$ statistics; the "more than triple" claim ($0.279/0.083=3.36$); both `PRMINWGE` trend-model $t$ statistics; and all three index-number computations ($131.5$, $39.6\%$, $237\%$). ✓
> - **Figures 10.1, 10.2 and 10.3 are images** and do not extract. Figure 10.1 plots a two-lag distribution peaking at the first lag; Figure 10.2 plots U.S. output per hour 1947–1987 (1977 = 100) rising from about 50 to about 110; Figure 10.3 plots nominal U.S. imports 1948–1995 in billions, showing the accelerating shape of an exponential trend. **All three are reconstructed from the surrounding prose, which states their content explicitly.**
> - **Tables 10.1 and 10.2 extracted intact** (inflation/unemployment listing; the $\mathbf{X}$ array illustration).
> - **The extraction of §10-5e is truncated mid-sentence** at the deseasonalizing procedure ("save the residuals, say, $\ddot y_t$, $\ddot x_{t1}$, and $\ddot x_{t2}$, for all $t=1,2,\dots,n$"). **Step (ii) — regress $\ddot y_t$ on $\ddot x_{t1},\ddot x_{t2}$ — is stated above by exact analogy with the trend case in §10-5c, which the text spells out in full.** No content appears to be lost, but it is an inference rather than a quotation.
> - **The `HSEINV` trend-regression standard errors are explicitly flagged as unreliable by the author** ("these regressions tend to contain substantial serial correlation"), so **the trend coefficients are used above only to establish that trends exist**, never for inference.
> - **Notation mangling in the PDF:** `b^ j` for $\hat\beta_j$, `y$ t` for $\ddot y_t$ (the detrended series), `s2 e` for $\sigma_e^2$, `E1ut0X2` for $\mathbb{E}(u_t\mid\mathbf{X})$, `R2 j` for $R_j^2$, `Rf t` and `Rm t` for $R_t^f$ and $R_t^m$, `1inft2` for $(inf_t)$, `u^0` for $\hat\theta_0$. **Every equation has been transcribed by hand against its numbered reference.**
> - **One source oddity:** equation (10.14) reports the Phillips curve with $\bar R^2=0.049$ against $R^2=0.065$, which is consistent ($n=59$, $k=1$), but the text calls $t=1.96$ *"about 1.96"* while the printed coefficients give $1.9650$ — **fine, but note the $p$-value of "about .055" is $0.0543$ on 57 df.** Immaterial.

#econometrics #time-series #distributed-lag #trends #seasonality #spurious-regression
