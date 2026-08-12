---
subject: Time-series Analysis
chapter: 04
tags: [ds, time-series, arma, yule-walker, forecasting, random-walk]
source: "documents/slides/Lecture_4_Timeseries_DSEB.ipynb (Lecture 4 — Time Series Models: AR, MA and ARMA Processes, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 3–4"
---

# AR, MA and ARMA Processes

> [!abstract] Where this sits in the course
> [[03 - Stationarity and Difference Equations]] established *when* a linear dynamic system is stable and *how* shocks propagate. This chapter turns that machinery into the three model families that dominate applied time-series work — **AR**, **MA** and **ARMA** — derives their moments, and shows how to forecast with them. [[05 - ACF, PACF and the Box-Jenkins Methodology]] then answers the practical question this chapter deliberately leaves open: *given data, which model and which orders?*

---

## 📘 Main Knowledge

### 1. The Random Walk — the canonical non-stationary process

Before the stationary models, the boundary case. The **random walk** is the AR(1) with $\phi = 1$, and it is the single most important non-stationary process in economics and finance.

#### Definition and explicit form

$$
y_t = y_{t-1} + \varepsilon_t,
\qquad
\varepsilon_t \sim WN(0,\sigma^2),
\quad y_0 \text{ given}
$$

Unrolling it:

$$
\begin{aligned}
y_1 &= y_0 + \varepsilon_1 \\
y_2 &= y_1 + \varepsilon_2 = y_0 + \varepsilon_1 + \varepsilon_2 \\
y_3 &= y_0 + \varepsilon_1 + \varepsilon_2 + \varepsilon_3 \\
&\;\;\vdots \\
y_t &= y_0 + \sum_{j=1}^{t}\varepsilon_j
\end{aligned}
$$

**A random walk is a running sum of all shocks that have ever hit it.** Everything below follows from that one observation.

#### Moments

**Mean** — constant, because shocks have zero mean:

$$
\mathbb{E}[y_t] = \mathbb{E}\!\left[y_0 + \sum_{j=1}^t \varepsilon_j\right] = y_0 + \sum_{j=1}^t 0 = y_0
$$

**Variance** — grows without bound, because uncorrelated variances add:

$$
\mathrm{Var}(y_t) = \mathrm{Var}\!\left(\sum_{j=1}^t\varepsilon_j\right) = \sum_{j=1}^t\mathrm{Var}(\varepsilon_j) = t\sigma^2
$$

$\mathrm{Var}(y_t) = t\sigma^2$ **increases with $t$**, so the random walk is **non-stationary** — the second condition of covariance stationarity fails outright.

**Autocovariance** — for $k \ge 0$, $y_{t-k} = y_0 + \sum_{j=1}^{t-k}\varepsilon_j$, and only the $t-k$ shocks the two sums share contribute:

$$
\begin{aligned}
\mathrm{Cov}(y_t, y_{t-k})
&= \mathrm{Cov}\!\left(\sum_{i=1}^{t}\varepsilon_i,\; \sum_{j=1}^{t-k}\varepsilon_j\right)
&& \text{(constants drop out)} \\
&= \sum_{j=1}^{t-k}\mathrm{Var}(\varepsilon_j)
&& \text{(only common terms survive)} \\
&= (t-k)\sigma^2
\end{aligned}
$$

$$
\boxed{\;\mathrm{Cov}(y_t,y_{t-k}) = (t-k)\sigma^2\;}
$$

This depends on $t$ **and** $k$, not on $k$ alone — a second, independent violation of stationarity.

**Autocorrelation:**

$$
\rho_k(t) = \frac{(t-k)\sigma^2}{\sqrt{t\sigma^2}\sqrt{(t-k)\sigma^2}} = \sqrt{\frac{t-k}{t}} \;\longrightarrow\; 1 \quad \text{as } t \to\infty
$$

> [!important] Why this matters for diagnostics
> For large $t$, **every** autocorrelation of a random walk is close to 1 — the sample ACF decays *linearly and very slowly* rather than geometrically. This is the visual signature you look for in [[05 - ACF, PACF and the Box-Jenkins Methodology]]: **an ACF that refuses to die is a unit root, not a highly persistent AR(1)**.

#### Permanent shocks

Split the sum at time $t$:

$$
y_{t+k} = y_0 + \sum_{j=1}^{t-1}\varepsilon_j + \varepsilon_t + \varepsilon_{t+1}+\cdots+\varepsilon_{t+k}
$$

The shock $\varepsilon_t$ enters with coefficient **1** and stays with coefficient 1 in $y_t, y_{t+1}, y_{t+2}, \ldots$ forever. In the language of [[03 - Stationarity and Difference Equations]], $\psi_j = 1$ for all $j$ — the impulse response never decays. **Shocks to a random walk are permanent.**

This is the economic content of the unit-root debate: is a recession a temporary deviation from trend (stationary, shocks decay) or a permanent downward shift in the level of output (unit root, shocks persist)?

#### Random walk with drift

$$
y_t = c + y_{t-1} + \varepsilon_t
$$

Unrolling gives a **deterministic trend plus a stochastic trend**:

$$
\begin{aligned}
y_1 &= y_0 + c + \varepsilon_1 \\
y_2 &= y_0 + 2c + \varepsilon_1 + \varepsilon_2 \\
&\;\;\vdots \\
y_t &= y_0 + tc + \sum_{j=1}^t \varepsilon_j
\end{aligned}
$$

| Drift | Behaviour |
|---|---|
| $c > 0$ | Upward deterministic trend superimposed on the random walk |
| $c < 0$ | Downward deterministic trend |
| $c = 0$ | Pure random walk |

$\mathbb{E}[y_t] = y_0 + tc$ now grows linearly, so the **mean** condition fails too. This is the standard model for log stock prices, log GDP, log exchange rates — the drift is the average growth rate.

> [!tip] Random walk vs. deterministic trend — a critical distinction
> Both produce a series that trends upward, but they demand completely different treatment:
> - **Trend-stationary**: $y_t = a + bt + u_t$ with $u_t$ stationary. Remove the trend by **regressing on $t$**; deviations are temporary.
> - **Difference-stationary** (unit root): $y_t = c + y_{t-1} + \varepsilon_t$. Remove the trend by **differencing**: $\Delta y_t = c + \varepsilon_t$, which is stationary. Deviations are permanent.
>
> Detrending a unit-root series by regression leaves highly autocorrelated residuals; differencing a trend-stationary series **over-differences**, injecting a non-invertible MA(1) unit root into the errors. Getting this wrong is one of the most consequential errors in applied work. The formal test (ADF) belongs to [[05 - ACF, PACF and the Box-Jenkins Methodology]] — it is **not** covered in this lecture, see the gaps note.

---

### 2. Autoregressive processes

#### 2.1 AR(1) without a constant

$$
y_t = \phi\,y_{t-1} + \varepsilon_t,
\qquad
\varepsilon_t\sim WN(0,\sigma^2),
\qquad
|\phi| < 1
$$

Notation: $\gamma_k = \mathrm{Cov}(y_t,y_{t-k})$, $\gamma_0 = \mathrm{Var}(y_t)$.

**Mean.** Take expectations: $\mathbb{E}[y_t] = \phi\,\mathbb{E}[y_{t-1}]$. Under stationarity $\mathbb{E}[y_t]=\mathbb{E}[y_{t-1}]=\mu$, so $(1-\phi)\mu = 0$, and since $\phi \neq 1$:

$$
\boxed{\;\mathbb{E}[y_t] = 0\;}
$$

**Variance.** Apply $\mathrm{Var}(aX+bY) = a^2\mathrm{Var}X + b^2\mathrm{Var}Y + 2ab\,\mathrm{Cov}(X,Y)$:

$$
\mathrm{Var}(y_t) = \phi^2\mathrm{Var}(y_{t-1}) + \mathrm{Var}(\varepsilon_t) + 2\phi\,\mathrm{Cov}(y_{t-1},\varepsilon_t)
$$

The cross term vanishes: $\varepsilon_t$ is white noise, uncorrelated with everything dated $t-1$ or earlier. Under stationarity $\mathrm{Var}(y_t)=\mathrm{Var}(y_{t-1})=\gamma_0$:

$$
\gamma_0 = \phi^2\gamma_0 + \sigma^2
\qquad\Longrightarrow\qquad
\boxed{\;\gamma_0 = \frac{\sigma^2}{1-\phi^2}\;},\qquad |\phi|<1
$$

Note $\gamma_0 > \sigma^2$ always: **autocorrelation amplifies variance**. As $|\phi|\to1$ the variance explodes — the smooth transition into the random-walk case.

**Autocovariances.** Multiply the model by $y_{t-k}$ and take expectations. Since $\mathrm{Cov}(\varepsilon_t, y_{t-k}) = 0$ for $k \ge 1$:

$$
\gamma_k = \phi\,\mathrm{Cov}(y_{t-1},y_{t-k}) + \underbrace{\mathrm{Cov}(\varepsilon_t,y_{t-k})}_{=\,0}
\qquad\Longrightarrow\qquad
\boxed{\;\gamma_k = \phi\,\gamma_{k-1}\;},\quad k\ge1
$$

This is the **Yule–Walker recursion**. Iterating from $\gamma_0$:

$$
\gamma_1 = \phi\gamma_0,\quad
\gamma_2 = \phi^2\gamma_0,\quad\ldots\quad
\gamma_k = \phi^k\gamma_0 = \phi^k\frac{\sigma^2}{1-\phi^2}
$$

$$
\boxed{\;\rho_k = \frac{\gamma_k}{\gamma_0} = \phi^k\;}
$$

**The ACF of an AR(1) decays geometrically** — monotonically if $\phi>0$, alternating in sign if $\phi<0$. It never cuts off. This exponential tail is *the* diagnostic signature of an AR process.

#### 2.2 AR(1) with a constant

$$
Y_t = \alpha + \phi Y_{t-1} + u_t,
\qquad u_t\sim WN(0,\sigma^2)
$$

| $|\phi|$ | Verdict |
|---|---|
| $|\phi| > 1$ | **Explosive**, non-stationary |
| $|\phi| = 1$ | **Random walk with drift**, non-stationary |
| $|\phi| < 1$ | **Mean-reverting**, stationary |

**Recursive expansion.** Substituting repeatedly from $Y_0$:

$$
\begin{aligned}
Y_1 &= \alpha + \phi Y_0 + \varepsilon_1 \\
Y_2 &= \alpha + \alpha\phi + \phi^2 Y_0 + \phi\varepsilon_1 + \varepsilon_2 \\
Y_3 &= \alpha + \alpha\phi + \alpha\phi^2 + \phi^3 Y_0 + \phi^2\varepsilon_1 + \phi\varepsilon_2 + \varepsilon_3
\end{aligned}
$$

giving the **closed form**

$$
Y_t = \phi^t Y_0 + \alpha\big(1+\phi+\phi^2+\cdots+\phi^{t-1}\big) + \phi^{t-1}\varepsilon_1 + \phi^{t-2}\varepsilon_2 + \cdots + \varepsilon_t
$$

with

$$
\mathbb{E}(Y_t) = \phi^t Y_0 + \alpha\frac{1-\phi^t}{1-\phi},
\qquad
\mathrm{Var}(Y_t) = \sigma^2\big(1 + \phi^2 + \phi^4 + \cdots + \phi^{2(t-1)}\big)
$$

As $t\to\infty$ with $|\phi|<1$ these converge to $\mu = \tfrac{\alpha}{1-\phi}$ and $\gamma_0 = \tfrac{\sigma^2}{1-\phi^2}$ — the process **forgets its initial condition** and settles into its stationary distribution.

**The mean-deviation trick.** Define $\mu = \dfrac{\alpha}{1-\phi}$; then

$$
\boxed{\;Y_t - \mu = \phi(Y_{t-1}-\mu) + \varepsilon_t\;}
$$

The constant disappears. **All autocovariance results carry over unchanged** — a constant shifts the level, never the dynamics:

$$
\gamma_k = \phi^k\gamma_0,
\qquad
\rho_k = \phi^k
$$

> [!tip] Always centre before computing autocovariances
> Working with $Y_t - \mu$ instead of $Y_t$ removes the intercept from every derivation. This trick is used relentlessly in this course and is the reason the AR(1)-without-constant results are stated first.

#### 2.3 AR(2)

$$
Y_t = \mu + \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + u_t,
\qquad u_t \sim WN(0,\sigma^2)
$$

> [!warning] Notation clash in the slides
> The lecture writes the **intercept** as $\mu$ while also using $\mu$ for the unconditional mean, and on one slide switches to $\phi_0$ for the same intercept. Here $\mu$ (or $\phi_0$) denotes the **intercept**, and $\mathbb{E}(Y)$ the mean — they are different numbers unless $\phi_1+\phi_2=0$.

**Characteristic equations.** Two equivalent routes, exactly as in [[03 - Stationarity and Difference Equations]]:

- Assume a homogeneous solution $Y_t = \lambda^t$ → the **difference equation** $\lambda^2 - \phi_1\lambda - \phi_2 = 0$ (inverse roots).
- Write $(1-\phi_1L-\phi_2L^2)Y_t = u_t$ → the **characteristic equation** $1 - \phi_1 z - \phi_2 z^2 = 0$ (characteristic roots).

**Stationarity condition.** The AR(2) is stationary **iff** all roots of $1-\phi_1z-\phi_2z^2 = 0$ lie **outside** the unit circle:

$$
|z_1| > 1, \qquad |z_2| > 1
\qquad\Longleftrightarrow\qquad
|\lambda_1| < 1,\;\;|\lambda_2| < 1 \;\;(\lambda = 1/z)
$$

This guarantees a finite unconditional mean, finite variance, and well-defined autocovariances, and it is equivalent to the **stability triangle** of the previous chapter.

**Mean.** Take expectations and use stationarity ($\mathbb{E}Y_t = \mathbb{E}Y_{t-1} = \mathbb{E}Y_{t-2} = \mathbb{E}Y$):

$$
\mathbb{E}(Y)(1-\phi_1-\phi_2) = \mu
\qquad\Longrightarrow\qquad
\boxed{\;\mathbb{E}(Y) = \frac{\mu}{1-\phi_1-\phi_2}\;}
$$

**Autocovariances (Yule–Walker).** Centre the process, multiply by $(Y_{t-k}-\mathbb{E}Y)$ and take expectations:

$$
\boxed{\;\gamma_k = \phi_1\gamma_{k-1} + \phi_2\gamma_{k-2}\;},
\qquad
\rho_k = \phi_1\rho_{k-1} + \phi_2\rho_{k-2},
\qquad k\ge1
$$

**The ACF obeys the same difference equation as the process itself.** That is why an AR(2) with complex roots produces a *damped oscillating ACF* — the ACF inherits the cyclical dynamics derived in [[03 - Stationarity and Difference Equations]].

The first two equations, using $\rho_0 = 1$ and $\rho_{-1} = \rho_1$:

$$
k=1:\quad \gamma_1 = \phi_1\gamma_0 + \phi_2\gamma_1
\;\Longrightarrow\;
\boxed{\;\rho_1 = \frac{\phi_1}{1-\phi_2}\;}
$$
$$
k=2:\quad \gamma_2 = \phi_1\gamma_1 + \phi_2\gamma_0
\;\Longrightarrow\;
\boxed{\;\rho_2 = \phi_1\rho_1 + \phi_2\;}
$$

**Variance.** The $k=0$ equation picks up the innovation variance (because $\mathbb{E}[\varepsilon_t(Y_t-\mu)] = \sigma^2$, not 0 — $\varepsilon_t$ *is* part of $Y_t$):

$$
\gamma_0 = \phi_1\gamma_1 + \phi_2\gamma_2 + \sigma^2
$$

Substituting $\gamma_1 = \rho_1\gamma_0$, $\gamma_2 = \rho_2\gamma_0$ and solving:

$$
\boxed{\;\gamma_0 = \mathrm{Var}(Y_t) = \frac{(1-\phi_2)\,\sigma^2}{(1+\phi_2)\big[(1-\phi_2)^2 - \phi_1^2\big]}\;}
$$

> [!note] Summary card — stationary AR(2)
> $$\mathbb{E}(Y_t) = \frac{\mu}{1-\phi_1-\phi_2},\qquad \rho_1 = \frac{\phi_1}{1-\phi_2},\qquad \rho_2 = \phi_1\rho_1+\phi_2$$
> $$\mathrm{Var}(Y_t) = \frac{(1-\phi_2)\sigma^2}{(1+\phi_2)[(1-\phi_2)^2-\phi_1^2]}$$
> The ACF **decays gradually**, possibly with damped oscillation. It never cuts off.

#### 2.4 AR($p$) and the Yule–Walker system

$$
Y_t = \mu + \phi_1Y_{t-1}+\cdots+\phi_pY_{t-p} + \varepsilon_t
\qquad\Longleftrightarrow\qquad
(1-\phi_1L-\cdots-\phi_pL^p)Y_t = \mu + \varepsilon_t
$$

with characteristic equation $1-\phi_1z-\cdots-\phi_pz^p = 0$ (roots outside the unit circle for stationarity).

**Mean:**

$$
\boxed{\;\mathbb{E}(Y_t) = \frac{\mu}{1-\sum_{i=1}^p\phi_i}\;}
$$

**Yule–Walker equations.** Multiply the centred model by $Y_{t-j}$ and take expectations:

$$
\gamma_j = \phi_1\gamma_{j-1} + \phi_2\gamma_{j-2}+\cdots+\phi_p\gamma_{j-p},
\qquad j=1,\ldots,p
$$

**Variance equation** ($j=0$):

$$
\gamma_0 = \phi_1\gamma_1 + \phi_2\gamma_2 + \cdots + \phi_p\gamma_p + \sigma^2
$$

Together: $p+1$ linear equations in the $p+1$ unknowns $\gamma_0,\ldots,\gamma_p$ (given $\phi$ and $\sigma^2$) — or, read backwards, $p$ equations that recover $\phi$ from the ACF, which is exactly how the Yule–Walker *estimator* works.

**Consequences:**

1. $\gamma_0$ is determined by the system but has **no simple closed form** for $p\ge3$ — unlike AR(1) and AR(2), you solve the linear system numerically.
2. For $k\ge p$, autocovariances satisfy the pure recursion $\gamma_k = \phi_1\gamma_{k-1}+\cdots+\phi_p\gamma_{k-p}$.
3. The ACF $\rho_k = \gamma_k/\gamma_0$ is a **mixture of exponential and oscillatory components**, one per root of $1-\phi_1z-\cdots-\phi_pz^p = 0$ — precisely the $\sum_i c_i\lambda_i^k$ structure of the dynamic multipliers.

**Matrix form.** With $\vec\gamma = (\gamma_1,\ldots,\gamma_p)'$, $\vec\phi = (\phi_1,\ldots,\phi_p)'$ and the **Toeplitz** covariance matrix

$$
\Gamma = \begin{pmatrix}
\gamma_0 & \gamma_1 & \cdots & \gamma_{p-1}\\
\gamma_1 & \gamma_0 & \cdots & \gamma_{p-2}\\
\vdots & \vdots & \ddots & \vdots\\
\gamma_{p-1} & \gamma_{p-2} & \cdots & \gamma_0
\end{pmatrix}
$$

the system is

$$
\boxed{\;\vec\gamma = \Gamma\vec\phi\;},
\qquad
\boxed{\;\gamma_0 = \vec\phi^{\,\top}\vec\gamma + \sigma^2\;}
$$

$\Gamma$ is symmetric Toeplitz — constant along diagonals — because stationarity makes the covariance depend only on the gap. Solving $\vec\phi = \Gamma^{-1}\vec\gamma$ recovers the coefficients from the autocovariances; this is the Yule–Walker estimator, and it is also the basis of the **PACF** in [[05 - ACF, PACF and the Box-Jenkins Methodology]]. The Toeplitz structure is what makes the Levinson–Durbin algorithm $O(p^2)$ rather than $O(p^3)$ — see [[Linear Algebra/contents/00-Index|structured matrices]].

> [!example] Worked AR(3) — the lecture's example, verified
> $$y_t = \tfrac12 y_{t-1} + \tfrac15 y_{t-2} + \tfrac1{10}y_{t-3} + u_t, \qquad \sigma^2 = 1$$
> The Yule–Walker equations, using $\gamma_{-k}=\gamma_k$:
> $$\gamma_1 = \phi_1\gamma_0 + \phi_2\gamma_1 + \phi_3\gamma_2$$
> $$\gamma_2 = \phi_1\gamma_1 + \phi_2\gamma_0 + \phi_3\gamma_1$$
> $$\gamma_3 = \phi_1\gamma_2 + \phi_2\gamma_1 + \phi_3\gamma_0$$
> $$\gamma_0 = \phi_1\gamma_1 + \phi_2\gamma_2 + \phi_3\gamma_3 + \sigma^2$$
> Four linear equations, four unknowns. Solving exactly:
> $$\gamma_0 = \tfrac{925}{434} \approx 2.1313,\quad \gamma_1 = \tfrac{325}{217}\approx1.4977,\quad \gamma_2 = \tfrac{575}{434}\approx1.3249,\quad \gamma_3 = \tfrac{255}{217}\approx1.1751$$
> $$\rho_1 = \tfrac{26}{37}\approx0.7027,\qquad \rho_2 = \tfrac{23}{37}\approx0.6216,\qquad \rho_3 = \tfrac{102}{185}\approx0.5514$$
> (I re-solved this system independently with exact rational arithmetic — **the slide's values are correct**.) Note $\sum\phi_i = 0.8 < 1$ and the ACF decays slowly but monotonically: three real roots, no oscillation.

---

### 3. Moving average processes

An MA process is a weighted sum of the **last $q$ shocks** — finite memory by construction.

#### 3.1 MA(1)

$$
Y_t = \mu + \varepsilon_t + \theta\varepsilon_{t-1}
$$

**Moments:**

$$
\mathbb{E}(Y_t) = \mu,
\qquad
\mathrm{Var}(Y_t) = \sigma^2(1+\theta^2)
$$

**Autocovariances.** Expand the products and keep only terms where the shock indices match:

$$
\mathrm{Cov}(Y_t,Y_{t-1}) = \mathbb{E}\big[(\varepsilon_t+\theta\varepsilon_{t-1})(\varepsilon_{t-1}+\theta\varepsilon_{t-2})\big] = \theta\sigma^2
$$
$$
\mathrm{Cov}(Y_t,Y_{t-k}) = \mathbb{E}\big[(\varepsilon_t+\theta\varepsilon_{t-1})(\varepsilon_{t-k}+\theta\varepsilon_{t-k-1})\big] = 0, \qquad k > 1
$$

Only $\varepsilon_{t-1}$ is shared between $Y_t$ and $Y_{t-1}$, giving $\theta\sigma^2$. At lag 2 there is **no shared shock at all**, so the covariance is exactly zero.

**ACF:**

$$
\rho_k = \begin{cases}
\dfrac{\theta}{1+\theta^2}, & k = 1\\[8pt]
0, & k > 1
\end{cases}
$$

> [!important] The MA signature: the ACF *cuts off*
> An MA($q$) has $\rho_k = 0$ **exactly** for $k > q$ — a hard cut-off, not a decay. Contrast the AR, whose ACF tails off geometrically forever. This is the core of ACF-based identification in [[05 - ACF, PACF and the Box-Jenkins Methodology]].

Because $\mu$, $\mathrm{Var}$ and every $\gamma_k$ are time-invariant for **any** $\theta$, the MA(1) is **covariance-stationary for all parameter values**. No condition needed.

> [!note] $|\rho_1| \le 1/2$ always
> Maximising $\theta/(1+\theta^2)$ gives $\rho_1 = 0.5$ at $\theta=1$ and $\rho_1 = -0.5$ at $\theta=-1$. **A first-order autocorrelation above 0.5 in absolute value rules out an MA(1) immediately.** Note also that $\theta$ and $1/\theta$ give the *same* $\rho_1$ — the identification problem that invertibility resolves.

#### 3.2 MA($q$)

$$
Y_t = \mu + \varepsilon_t + \theta_1\varepsilon_{t-1} + \cdots + \theta_q\varepsilon_{t-q}
\qquad\Longleftrightarrow\qquad
Y_t = \mu + \theta(L)\varepsilon_t
$$

with $\theta(L) = 1 + \theta_1L + \cdots + \theta_qL^q$ and the convention $\theta_0 = 1$.

**Moments:**

$$
\mathbb{E}(Y_t) = \mu,
\qquad
\mathrm{Var}(Y_t) = (1+\theta_1^2+\cdots+\theta_q^2)\sigma^2
$$

**Autocovariance function:**

$$
\boxed{\;
\gamma_k = \begin{cases}
\big(\theta_k + \theta_{k+1}\theta_1 + \theta_{k+2}\theta_2 + \cdots + \theta_q\theta_{q-k}\big)\sigma^2, & k \le q\\[4pt]
0, & k > q
\end{cases}
\;}
$$

Read it as $\gamma_k = \sigma^2\sum_{j=0}^{q-k}\theta_j\theta_{j+k}$: **slide the coefficient vector against itself by $k$ positions and sum the overlapping products.** Once the shift exceeds $q$ there is no overlap and the covariance is zero.

**An MA($q$) is covariance-stationary for any parameter vector $\theta$.** Full stop.

#### 3.3 MA($\infty$)

$$
Y_t = \mu + \varepsilon_t + \psi_1\varepsilon_{t-1} + \psi_2\varepsilon_{t-2}+\cdots = \mu + \psi(L)\varepsilon_t
$$

$$
\mathbb{E}(Y_t) = \mu,
\qquad
\mathrm{Var}(Y_t) = \big(1+\psi_1^2+\psi_2^2+\cdots\big)\sigma^2,
\qquad
\gamma_k = \sigma^2\sum_{j=0}^{\infty}\psi_j\psi_{j+k}
$$

Now stationarity **does** require a condition — the variance must be finite:

$$
\sum_{k=0}^\infty \psi_k^2 < \infty
\qquad\text{(square-summability)}
$$

This is the Wold representation of [[03 - Stationarity and Difference Equations]] with the convergence condition made explicit. It is also why a stationary AR *has* an MA($\infty$) form: $\psi_j = \sum_i c_i\lambda_i^j$ is square-summable precisely when all $|\lambda_i|<1$.

#### 3.4 Invertibility

**Definition.** An MA($q$) is **invertible** if the innovations can be recovered as a convergent linear function of observed past values:

$$
\varepsilon_t = (1 + \eta_1L + \eta_2L^2 + \cdots)(Y_t-\mu),
\qquad
(1+\eta_1L+\cdots) = \theta(L)^{-1}
$$

Invertibility lets an MA($q$) be rewritten as an **AR($\infty$)** — the mirror image of a stationary AR being rewritten as an MA($\infty$).

**Condition.** All roots of

$$
1 + \theta_1z + \theta_2z^2 + \cdots + \theta_qz^q = 0
$$

must lie **outside the unit circle**, $|z| > 1$.

> [!important] The perfect symmetry
> | | Polynomial | Property | Condition | Gives you |
> |---|---|---|---|---|
> | **AR** | $\phi(z)$ | Stationarity | $\lvert z\rvert>1$ | MA($\infty$) form |
> | **MA** | $\theta(z)$ | Invertibility | $\lvert z\rvert>1$ | AR($\infty$) form |
>
> Same condition, different polynomial. **Stationarity constrains the AR side; invertibility constrains the MA side.** An MA is always stationary; an AR is always invertible.

**Why invertibility matters.** Without it the model is not identified: $\theta$ and $1/\theta$ generate identical ACFs (with rescaled $\sigma^2$), so the data cannot distinguish them. Convention picks the invertible representation — the one where today's shock is recoverable from observed history, which is also the only one you can actually forecast with (see §5).

> [!example] The lecture's MA(2) example — with two slide errors corrected
> $$Y_t = \Big(1 - \tfrac56 L + \tfrac16 L^2\Big)\varepsilon_t, \qquad \sigma^2 = 1$$
> So $\theta_1 = -\tfrac56$, $\theta_2 = \tfrac16$.
>
> **(a) Stationary?** Yes — a finite MA is stationary for any coefficients, since $\varepsilon_t$ is white noise with constant variance and no autocorrelation.
>
> **(b) Mean and variance.** $\mathbb{E}(Y_t) = 0$ and
> $$\gamma_0 = (1+\theta_1^2+\theta_2^2)\sigma^2 = 1 + \tfrac{25}{36} + \tfrac1{36} = \tfrac{62}{36} = \boxed{\tfrac{31}{18}} \approx 1.7222$$
> > [!warning] The slide prints $\tfrac{31}{19}$. That is a **typo** — the arithmetic gives $\tfrac{31}{18}$.
>
> **(c) Autocovariances.**
> $$\gamma_1 = (\theta_1 + \theta_1\theta_2)\sigma^2 = -\tfrac56 + \big(-\tfrac56\big)\big(\tfrac16\big) = -\tfrac56-\tfrac5{36} = -\tfrac{35}{36} \approx -0.9722$$
> $$\gamma_2 = \theta_2\sigma^2 = \tfrac16 \approx 0.1667,\qquad \gamma_3 = 0 \;\;(\text{since } q=2)$$
>
> **(d) Invertibility.** The MA polynomial is $\theta(z) = 1 - \tfrac56 z + \tfrac16 z^2$. Setting it to zero and multiplying by 6: $z^2 - 5z + 6 = 0$, so
> $$z_1 = 2, \qquad z_2 = 3$$
> Both real and outside the unit circle → **invertible**.
> > [!warning] The slide writes the characteristic equation as $1 + \tfrac56 z + \tfrac16 z^2 = 0$ and reports $z = -2, -3$. The **signs are wrong** — $\theta_1$ is $-\tfrac56$, not $+\tfrac56$. The moduli (and hence the invertibility conclusion) are unaffected, but the roots are $+2$ and $+3$.

---

### 4. ARMA($p,q$)

Combine both memories: persistence through past *values* (AR) and through past *shocks* (MA).

$$
Y_t = \phi_0 + \phi_1Y_{t-1}+\cdots+\phi_pY_{t-p} + \varepsilon_t + \theta_1\varepsilon_{t-1}+\cdots+\theta_q\varepsilon_{t-q}
\tag{5.11}
$$

In operator form:

$$
\phi(L)Y_t = \phi_0 + \theta(L)\varepsilon_t
\tag{5.12}
$$
$$
\phi(L) = 1-\phi_1L-\cdots-\phi_pL^p,
\qquad
\theta(L) = 1+\theta_1L+\cdots+\theta_qL^q
$$

**Stationarity** depends only on $\phi(L)$: all roots of $1-\phi_1z-\cdots-\phi_pz^p = 0$ outside the unit circle. **Invertibility** depends only on $\theta(L)$.

**MA($\infty$) form.** Multiply (5.12) through by $\phi(L)^{-1}$:

$$
Y_t = \phi(L)^{-1}\phi_0 + \phi(L)^{-1}\theta(L)\varepsilon_t = \mu + \Psi(L)\varepsilon_t,
\qquad
\Psi(L) = \frac{\theta(L)}{\phi(L)}
$$

To compute $\Psi(L)$ in practice: **factor** $\phi(L) = (1-\alpha_1L)\cdots(1-\alpha_pL)$, apply partial fractions, and expand each $\tfrac1{1-\alpha_iL}$ as a geometric series — exactly the §4.7 procedure of [[03 - Stationarity and Difference Equations]].

> [!tip] Why bother with ARMA at all?
> **Parsimony.** A slowly decaying ACF might need an AR(8); a mixed pattern might need an MA(12). An ARMA(1,1) can often reproduce both with **two** parameters. Fewer parameters → lower estimation variance → better out-of-sample forecasts. This is the whole rationale for the Box–Jenkins approach.

> [!example] Worked ARMA(2,1) — the lecture's example
> $$Y_t = 1 + 0.3Y_{t-1} - 0.02Y_{t-2} + \varepsilon_t + 0.2\varepsilon_{t-1}, \qquad \varepsilon_t\sim N(0,1)$$
>
> **(a) Operator form.** Move the AR terms left:
> $$(1 - 0.3L + 0.02L^2)Y_t = 1 + (1+0.2L)\varepsilon_t$$
>
> **(b)–(c) Roots and stationarity.** $\;1 - 0.3z + 0.02z^2 = 0$. Multiplying by 50: $z^2 - 15z + 50 = 0$, so
> $$z_1 = 5, \qquad z_2 = 10$$
> Both satisfy $|z|>1$ → **stationary**. (Inverse roots $0.2$ and $0.1$, both inside the unit circle.)
>
> **(d) Factorisation.** Since $\lambda_i = 1/z_i$:
> $$\phi(L) = (1-0.2L)(1-0.1L)$$
> Check: $1 - 0.3L + 0.02L^2$ ✓.
>
> **(e) Inverse operator.** Partial fractions:
> $$\phi(L)^{-1} = \frac{1}{(1-0.2L)(1-0.1L)} = \frac{2}{1-0.2L} - \frac{1}{1-0.1L}$$
> Each term expands as $\frac{1}{1-aL} = \sum_{j\ge0}a^jL^j$ for $|a|<1$, giving
> $$\phi(L)^{-1} = \sum_{j=0}^\infty \big(2(0.2)^j - (0.1)^j\big)L^j = 1 + 0.3L + 0.07L^2 + 0.015L^3 + \cdots$$
> confirming that the AR part admits an MA($\infty$) representation. Multiplying by $\theta(L) = 1+0.2L$ gives the full $\Psi(L)$:
> $$\psi_0 = 1,\quad \psi_1 = 0.3+0.2 = 0.5,\quad \psi_2 = 0.07 + 0.2(0.3) = 0.13,\quad \psi_3 = 0.015+0.2(0.07) = 0.029$$
> The **mean** is $\mathbb{E}(Y) = \dfrac{1}{1-0.3+0.02} = \dfrac{1}{0.72} \approx 1.3889$.

---

### 5. Forecasting

#### 5.1 The optimal forecast is the conditional expectation

Forecast $Y_{t+1}$ from information $X_t$ available at time $t$, using a rule $Y^*_{t+1|t} = g(X_t)$, judged by **quadratic loss**:

$$
\mathrm{MSE}(Y^*_{t+1|t}) = \mathbb{E}\big(Y_{t+1}-Y^*_{t+1|t}\big)^2
$$

The MSE decomposes as

$$
\mathbb{E}[Y_{t+1}-g(X_t)]^2
= \underbrace{\mathbb{E}\big[Y_{t+1}-\mathbb{E}(Y_{t+1}|X_t)\big]^2}_{\text{irreducible uncertainty}}
+ \underbrace{\mathbb{E}\big[\mathbb{E}(Y_{t+1}|X_t)-g(X_t)\big]^2}_{\ge\,0}
$$

The first term does not involve $g$ at all; the second is a square, minimised at zero by choosing $g(X_t) = \mathbb{E}(Y_{t+1}|X_t)$:

$$
\boxed{\;Y^*_{t+1|t} = \mathbb{E}(Y_{t+1}\mid X_t)\;}
$$

> [!note] This is the same decomposition as everywhere else in statistics
> It is the bias–variance identity, the ANOVA decomposition, and the projection theorem, in time-series clothing. The conditional mean minimises squared error; no model can beat the irreducible term. Compare [[Machine Learning/contents/00-Index|the bias–variance decomposition]] and [[Mathematical Statistics/contents/05 - Point Estimation]].

#### 5.2 The Wiener–Kolmogorov prediction formula

Start from the MA($\infty$) form of a covariance-stationary process:

$$
Y_t - \mu = \psi(L)\varepsilon_t,
\qquad
\psi(L) = \sum_{j=0}^\infty\psi_jL^j,
\quad \psi_0 = 1,
\quad \sum_{j=0}^\infty|\psi_j| < \infty
$$

The $s$-step-ahead value splits into future (unknown) and past (known) shocks:

$$
Y_{t+s} = \mu + \underbrace{\varepsilon_{t+s}+\psi_1\varepsilon_{t+s-1}+\cdots+\psi_{s-1}\varepsilon_{t+1}}_{\text{future — unobserved at } t}
+ \underbrace{\psi_s\varepsilon_t + \psi_{s+1}\varepsilon_{t-1}+\cdots}_{\text{past — known at } t}
$$

**Replace every unknown future shock by its expectation, zero:**

$$
\hat{\mathbb{E}}[Y_{t+s}\mid\varepsilon_t,\varepsilon_{t-1},\ldots] = \mu + \psi_s\varepsilon_t + \psi_{s+1}\varepsilon_{t-1}+\psi_{s+2}\varepsilon_{t-2}+\cdots
$$

**Forecast error and MSE.** The error is exactly the discarded future block:

$$
Y_{t+s} - \hat{\mathbb{E}}[Y_{t+s}] = \varepsilon_{t+s}+\psi_1\varepsilon_{t+s-1}+\cdots+\psi_{s-1}\varepsilon_{t+1}
$$
$$
\boxed{\;\mathrm{MSE}(s) = \big(1+\psi_1^2+\psi_2^2+\cdots+\psi_{s-1}^2\big)\sigma^2\;}
$$

$\mathrm{MSE}(s)$ is **increasing in $s$** — every extra step forward adds one more unforecastable shock. This is why forecast intervals fan out. As $s\to\infty$ it converges to $\mathrm{Var}(Y_t)$: at infinite horizon the best you can do is the unconditional mean, and your uncertainty is the unconditional variance.

**Compact form via the annihilation operator.** Write

$$
\frac{\psi(L)}{L^s} = L^{-s} + \psi_1L^{1-s}+\cdots+\psi_s + \psi_{s+1}L+\cdots
$$

and define $[\,\cdot\,]_+$ as the operator that **sets all negative powers of $L$ to zero**:

$$
\left[\frac{\psi(L)}{L^s}\right]_+ = \psi_s + \psi_{s+1}L + \psi_{s+2}L^2 + \cdots
$$

Then the **Wiener–Kolmogorov prediction formula** is

$$
\boxed{\;\hat{\mathbb{E}}[Y_{t+s}\mid\mathcal{F}_t] = \mu + \left[\frac{\psi(L)}{L^s}\right]_+\varepsilon_t\;}
$$

The annihilation operator is just "delete the terms you cannot observe" written algebraically. If the process is also invertible, $\eta(L)(Y_t-\mu) = \varepsilon_t$ with $\eta(L) = \psi(L)^{-1}$, so forecasts can be written entirely in terms of **observed** lagged $Y$'s — which is what makes any of this usable.

#### 5.3 Forecasting an AR(1)

$$
(1-\phi L)(Y_t-\mu) = \varepsilon_t,
\qquad |\phi|<1
$$

MA($\infty$) form: $\psi(L) = \frac{1}{1-\phi L}$, so $\psi_j = \phi^j$. Apply the filter:

$$
\left[\frac{\psi(L)}{L^s}\right]_+ = \phi^s + \phi^{s+1}L + \phi^{s+2}L^2 + \cdots = \frac{\phi^s}{1-\phi L}
$$

Substituting $\varepsilon_t = (1-\phi L)(Y_t-\mu)$, the operator cancels:

$$
\hat{\mathbb{E}}[Y_{t+s}\mid\mathcal{F}_t] = \mu + \frac{\phi^s}{1-\phi L}(1-\phi L)(Y_t-\mu)
$$

$$
\boxed{\;\hat Y_{t+s|t} = \mu + \phi^s(Y_t-\mu)\;}
$$

Beautifully simple: **the forecast decays geometrically back to the mean at rate $\phi$**, and only the *most recent* observation matters. Forecast error variance:

$$
\mathrm{MSE}(s) = \big(1+\phi^2+\phi^4+\cdots+\phi^{2(s-1)}\big)\sigma^2
\;\xrightarrow[s\to\infty]{}\;
\frac{\sigma^2}{1-\phi^2} = \mathrm{Var}(Y_t)
$$

At long horizons the forecast is the unconditional mean and the uncertainty is the unconditional variance — the process has told you everything it knows.

#### 5.4 Forecasting an AR($p$)

Using the companion matrix $F$ from [[03 - Stationarity and Difference Equations]]:

$$
\boxed{\;\hat Y_{t+s|t} = \mu + f_{11}^{(s)}(Y_t-\mu) + f_{12}^{(s)}(Y_{t-1}-\mu) + \cdots + f_{1p}^{(s)}(Y_{t-p+1}-\mu)\;}
$$

where $f_{ij}^{(s)} = (F^s)_{ij}$. **The same matrix powers that gave the impulse response give the forecast weights.** For any horizon, the forecast is a constant plus a linear function of the last $p$ observations.

**Iterated projection** — the practical recipe. One step:

$$
\hat Y_{t+1|t}-\mu = \phi_1(Y_t-\mu)+\phi_2(Y_{t-1}-\mu)+\cdots+\phi_p(Y_{t-p+1}-\mu)
$$

Two steps — feed the forecast back in as if it were data:

$$
\hat Y_{t+2|t}-\mu = \phi_1(\hat Y_{t+1|t}-\mu)+\phi_2(Y_t-\mu)+\cdots
= (\phi_1^2+\phi_2)(Y_t-\mu) + (\phi_1\phi_2+\phi_3)(Y_{t-1}-\mu)+\cdots
$$

**General recursion:**

$$
\boxed{\;(\hat Y_{t+j|t}-\mu) = \phi_1(\hat Y_{t+j-1|t}-\mu)+\cdots+\phi_p(\hat Y_{t+j-p|t}-\mu)\;}
\qquad
\hat Y_{\tau|t} = Y_\tau \;\text{ for } \tau\le t
$$

Read the initialisation carefully: **use the actual value when it is known, the forecast when it is not.** That single rule is all of multi-step ARMA forecasting.

#### 5.5 Forecasting an MA(1) and MA($q$)

For an invertible MA(1), $Y_t-\mu = (1+\theta L)\varepsilon_t$ with $|\theta|<1$. At $s=1$, $\big[\tfrac{1+\theta L}{L}\big]_+ = \theta$, so

$$
\hat Y_{t+1|t} = \mu + \frac{\theta}{1+\theta L}(Y_t-\mu)
= \mu + \theta(Y_t-\mu) - \theta^2(Y_{t-1}-\mu) + \theta^3(Y_{t-2}-\mu) - \cdots
$$

an infinite, sign-alternating, geometrically damped weighting of the entire past. **Invertibility is what makes this converge** — with $|\theta|>1$ the weights would explode and the forecast would be meaningless.

**Innovations representation.** Rather than the infinite sum, recover the shocks recursively:

$$
\hat\varepsilon_t = (Y_t-\mu) - \theta\hat\varepsilon_{t-1}
\qquad\Longrightarrow\qquad
\boxed{\;\hat Y_{t+1|t} = \mu + \theta\hat\varepsilon_t\;}
$$

For $s\ge2$, $\big[\tfrac{1+\theta L}{L^s}\big]_+ = 0$ and therefore

$$
\boxed{\;\hat Y_{t+s|t} = \mu,\qquad s\ge2\;}
$$

**An MA(1) is useless beyond one step ahead.** Its memory is exactly one period long; past that, the best forecast is the mean. Generalising, for an invertible MA($q$):

$$
\hat Y_{t+s|t} = \mu + \big(\theta_s + \theta_{s+1}L+\cdots+\theta_qL^{q-s}\big)\hat\varepsilon_t,
\qquad
\hat\varepsilon_t = (Y_t-\mu)-\theta_1\hat\varepsilon_{t-1}-\cdots-\theta_q\hat\varepsilon_{t-q}
$$

$$
\boxed{\;\hat Y_{t+s|t} = \mu \quad\text{for } s > q\;}
$$

**The forecast horizon of an MA($q$) is exactly $q$ periods.** This mirrors the ACF cut-off — same finite memory, seen from the forecasting side.

#### 5.6 Forecasting ARMA

For a stationary, invertible ARMA(1,1), $(1-\phi L)(Y_t-\mu) = (1+\theta L)\varepsilon_t$, the filter evaluates to

$$
\left[\frac{1+\theta L}{(1-\phi L)L^s}\right]_+ = \frac{\phi^s+\theta\phi^{s-1}}{1-\phi L}
$$

giving

$$
\boxed{\;\hat Y_{t+s|t} = \mu + \frac{\phi^s+\theta\phi^{s-1}}{1+\theta L}(Y_t-\mu)\;}
$$

At $s=1$ this simplifies to the form you would actually implement:

$$
(\hat Y_{t+1|t}-\mu) = \phi(Y_t-\mu) + \theta\hat\varepsilon_t,
\qquad
\hat\varepsilon_t = Y_t - \hat Y_{t|t-1}
$$

**The innovation is the previous period's forecast error.** That recursive structure is exactly what the [[06 - The Kalman Filter and State-Space Models|Kalman filter]] generalises.

**General ARMA($p,q$).** One step ahead:

$$
(\hat Y_{t+1|t}-\mu) = \sum_{i=1}^p\phi_i(Y_{t-i+1}-\mu) + \sum_{j=1}^q\theta_j\hat\varepsilon_{t-j+1},
\qquad \hat\varepsilon_t = Y_t-\hat Y_{t|t-1}
$$

$s$ steps ahead:

$$
(\hat Y_{t+s|t}-\mu) =
\begin{cases}
\displaystyle\sum_{i=1}^p\phi_i(\hat Y_{t+s-i|t}-\mu) + \sum_{j=s}^q\theta_j\hat\varepsilon_{t+s-j}, & s\le q\\[14pt]
\displaystyle\sum_{i=1}^p\phi_i(\hat Y_{t+s-i|t}-\mu), & s > q
\end{cases}
$$

with $\hat Y_{\tau|t} = Y_\tau$ for $\tau\le t$.

> [!important] **Beyond horizon $q$, an ARMA forecast is a pure AR($p$) recursion.**
> The MA terms have run out of observed shocks and drop away entirely. So the *long-run* shape of any ARMA forecast — the rate at which it reverts to $\mu$ — is governed **only by the AR roots**. The MA part shapes the first $q$ steps and nothing more.

---

## ✏️ Exercises

### Exercise 1 — MA(2) stationarity, autocovariances and invertibility

*(Lecture Exercise 3.1.)* Let $\mathbb{E}(\varepsilon_t\varepsilon_\tau) = 1$ if $t=\tau$ and $0$ otherwise. Consider

$$
Y_t = (1 + 2.4L + 0.8L^2)\varepsilon_t
$$

(a) Is the process covariance-stationary? Why? (b) Compute $\gamma_0,\gamma_1,\gamma_2$. (c) Is it invertible?

> [!example]- Solution
> **(a) Yes.** A finite-order MA is a finite weighted sum of white-noise terms. Its mean ($=0$), variance and autocovariances are all constants independent of $t$, so covariance stationarity holds **for any** $\theta_1,\theta_2$ — no condition to check.
>
> **(b)** With $\theta_0=1,\ \theta_1=2.4,\ \theta_2=0.8,\ \sigma^2=1$, use $\gamma_k = \sigma^2\sum_{j=0}^{q-k}\theta_j\theta_{j+k}$:
> $$\gamma_0 = 1 + 2.4^2 + 0.8^2 = 1 + 5.76 + 0.64 = \mathbf{7.40}$$
> $$\gamma_1 = \theta_0\theta_1 + \theta_1\theta_2 = 2.4 + (2.4)(0.8) = 2.4 + 1.92 = \mathbf{4.32}$$
> $$\gamma_2 = \theta_0\theta_2 = \mathbf{0.8}$$
> $$\gamma_k = 0 \quad \text{for } k \ge 3$$
> Autocorrelations: $\rho_1 = 4.32/7.40 \approx 0.584$, $\rho_2 = 0.8/7.40 \approx 0.108$, $\rho_k = 0$ for $k\ge3$.
>
> **(c) No.** Solve $1 + 2.4z + 0.8z^2 = 0$:
> $$z = \frac{-2.4 \pm\sqrt{5.76 - 3.2}}{1.6} = \frac{-2.4\pm1.6}{1.6} = \{-0.5,\; -2.5\}$$
> The root $z_1 = -0.5$ has $|z_1| = 0.5 < 1$ — **inside** the unit circle → **not invertible**.
>
> Equivalently, $\theta(L) = (1+2L)(1+0.4L)$, and the factor $(1+2L)$ has $|2| > 1$. There exists an **invertible twin** with identical autocorrelations: replace $2$ by $1/2$, giving $\theta^*(L) = (1+0.5L)(1+0.4L) = 1+0.9L+0.2L^2$ with $\sigma^{*2} = 4$. Check: $\gamma_0^* = 4(1+0.81+0.04) = 7.40$ ✓, $\gamma_1^* = 4(0.9+0.18) = 4.32$ ✓, $\gamma_2^* = 4(0.2) = 0.8$ ✓. **Identical second moments, different parameters** — exactly the identification problem invertibility resolves. Software would report the starred version.

---

### Exercise 2 — AR(2) stationarity and autocovariances

*(Lecture Exercise 3.2.)* With $\sigma^2 = 1$, consider

$$
(1 - 1.1L + 0.18L^2)Y_t = \varepsilon_t
$$

(a) Is it covariance-stationary? (b) Compute $\gamma_0,\gamma_1,\gamma_2$. (c) Give the general recursion for $\gamma_k$, $k\ge1$.

> [!example]- Solution
> First read off the coefficients. The model is $Y_t = 1.1Y_{t-1} - 0.18Y_{t-2}+\varepsilon_t$, so
> $$\phi_1 = 1.1, \qquad \phi_2 = -0.18$$
> **Watch the sign** — $\phi(L) = 1-\phi_1L-\phi_2L^2$, so the $+0.18L^2$ in the polynomial means $\phi_2 = -0.18$.
>
> **(a)** Characteristic equation $1 - 1.1z + 0.18z^2 = 0$:
> $$z = \frac{1.1\pm\sqrt{1.21 - 0.72}}{0.36} = \frac{1.1\pm0.7}{0.36} = \{5,\; 1.1\overline{1}\}$$
> Both $|z| > 1$ → **covariance-stationary**. Inverse roots: $\lambda = \{0.2,\,0.9\}$, both inside the unit circle. Factorisation: $(1-0.2L)(1-0.9L)$. The dominant root $0.9$ means slow, monotone decay with no oscillation ($\Delta = \phi_1^2+4\phi_2 = 1.21-0.72 = 0.49 > 0$, real roots).
>
> Triangle check: $\phi_2 = -0.18 < 1-\phi_1 = -0.1$ ✓; $-0.18 < 1+1.1 = 2.1$ ✓; $-1 < -0.18 < 1$ ✓.
>
> **(b)** Yule–Walker:
> $$\rho_1 = \frac{\phi_1}{1-\phi_2} = \frac{1.1}{1.18} = \frac{55}{59} \approx 0.9322$$
> $$\rho_2 = \phi_1\rho_1 + \phi_2 = 1.1(0.9322) - 0.18 \approx 0.8454$$
> Variance:
> $$\gamma_0 = \frac{(1-\phi_2)\sigma^2}{(1+\phi_2)\big[(1-\phi_2)^2-\phi_1^2\big]} = \frac{1.18}{0.82\big[1.3924 - 1.21\big]} = \frac{1.18}{0.82(0.1824)} = \frac{36875}{4674} \approx \mathbf{7.8894}$$
> Hence
> $$\gamma_1 = \rho_1\gamma_0 \approx \mathbf{7.3545}, \qquad \gamma_2 = \rho_2\gamma_0 \approx \mathbf{6.6699}$$
> **Verification** via the variance equation: $\phi_1\gamma_1 + \phi_2\gamma_2 + \sigma^2 = 1.1(7.3545) - 0.18(6.6699) + 1 = 8.0900 - 1.2006 + 1 = 7.8894$ ✓.
>
> Note how large $\gamma_0$ is relative to $\sigma^2 = 1$: a dominant root of $0.9$ produces nearly eightfold variance amplification.
>
> **(c)**
> $$\gamma_k = 1.1\gamma_{k-1} - 0.18\gamma_{k-2}, \qquad k \ge 1$$
> with $\gamma_{-1} = \gamma_1$. Continuing: $\gamma_3 = 1.1(6.6699)-0.18(7.3545) \approx 6.0131$, i.e. $\rho_3 \approx 0.7622$. In closed form $\rho_k = c_1(0.9)^k + c_2(0.2)^k$; the $0.9$ term dominates almost immediately, so the ACF looks nearly like that of an AR(1) with $\phi = 0.9$.

---

### Exercise 3 — Random walk vs stationary AR(1)

Two series are simulated with the same shocks $\varepsilon_t\sim N(0,1)$, $T = 200$, $y_0 = 0$:
$$\text{(A) } y_t = y_{t-1}+\varepsilon_t \qquad\qquad \text{(B) } y_t = 0.95\,y_{t-1}+\varepsilon_t$$
$\phi = 0.95$ is very close to 1. (a) How do their theoretical variances behave? (b) At what $t$ does the random walk's variance exceed the AR(1)'s stationary variance? (c) How would you tell them apart from a single realisation?

> [!example]- Solution
> **(a)** For **(A)**, $\mathrm{Var}(y_t) = t\sigma^2 = t$ — unbounded and linear in $t$. For **(B)**, $\mathrm{Var}(y_t) \to \tfrac{\sigma^2}{1-\phi^2} = \tfrac{1}{1-0.9025} = \tfrac{1}{0.0975} \approx 10.26$ — bounded.
>
> **(b)** $t\sigma^2 > 10.26$ at $t = 11$. So after only 11 periods, the random walk is already more variable than the AR(1) ever gets. Over $T=200$ its variance reaches 200 — roughly **20× larger**.
>
> **(c)** This is genuinely hard, and that difficulty is the entire reason unit-root testing exists.
> - **Time plot.** (A) wanders freely and never returns to any particular level; (B) reverts, but slowly — over a short sample the two look near-identical.
> - **Sample ACF.** (A) decays **linearly**: $\rho_k(t) = \sqrt{(t-k)/t}$, still $\approx 0.97$ at lag 10 for $t=200$. (B) decays **geometrically**: $\rho_k = 0.95^k$, giving $0.60$ at lag 10 and $0.36$ at lag 20. Diagnostic in principle, but noisy in a finite sample.
> - **Differencing.** $\Delta y_t$ is white noise for (A) but an over-differenced, non-invertible MA for (B). Check the ACF of the differenced series: near-zero everywhere → (A); a significant negative spike at lag 1 → over-differenced, so (B).
> - **The proper answer** is a formal **ADF or KPSS test**. Note their power is low precisely in this region: distinguishing $\phi = 1$ from $\phi = 0.95$ with $T = 200$ is close to hopeless, and everyone in applied macro knows it.
>
> > [!warning] These tests are **not covered in this lecture** — see the gaps note at the end. They appear in [[05 - ACF, PACF and the Box-Jenkins Methodology]] as part of the Box–Jenkins identification step.

---

### Exercise 4 — Forecasting an ARMA(1,1) by hand

Let $Y_t = 2 + 0.6Y_{t-1} + \varepsilon_t + 0.4\varepsilon_{t-1}$ with $\sigma^2 = 1$. You observe $Y_t = 7$ and have computed $\hat\varepsilon_t = 0.5$. Produce forecasts for $s = 1,2,3$ and their 95% intervals.

> [!example]- Solution
> **Mean.** $\mu = \dfrac{2}{1-0.6} = \mathbf{5}$. So $Y_t - \mu = 7-5 = 2$.
>
> **One step ahead** ($s=1$), using $(\hat Y_{t+1|t}-\mu) = \phi(Y_t-\mu)+\theta\hat\varepsilon_t$:
> $$\hat Y_{t+1|t} = 5 + 0.6(2) + 0.4(0.5) = 5 + 1.2 + 0.2 = \mathbf{6.4}$$
>
> **Two steps** ($s = 2 > q = 1$), so the MA term drops out and the recursion is pure AR:
> $$\hat Y_{t+2|t} = 5 + 0.6(6.4-5) = 5 + 0.84 = \mathbf{5.84}$$
>
> **Three steps:**
> $$\hat Y_{t+3|t} = 5 + 0.6(5.84-5) = 5 + 0.504 = \mathbf{5.504}$$
>
> The forecast decays toward $\mu = 5$ at rate $\phi = 0.6$ — geometric mean reversion, exactly as §5.6 predicts.
>
> **Forecast intervals.** First the $\psi$ weights of $\Psi(L) = \frac{1+0.4L}{1-0.6L}$:
> $$\psi_0 = 1, \qquad \psi_1 = \phi+\theta = 1.0, \qquad \psi_2 = \phi\psi_1 = 0.6, \qquad \psi_j = 0.6\,\psi_{j-1} \;(j\ge2)$$
> Then $\mathrm{MSE}(s) = (1+\psi_1^2+\cdots+\psi_{s-1}^2)\sigma^2$:
>
> | $s$ | Forecast | MSE | SE | 95% interval |
> |---|---|---|---|---|
> | 1 | 6.400 | $1$ | 1.000 | $[4.44,\;8.36]$ |
> | 2 | 5.840 | $1+1^2 = 2$ | 1.414 | $[3.07,\;8.61]$ |
> | 3 | 5.504 | $1+1+0.36 = 2.36$ | 1.536 | $[2.49,\;8.52]$ |
>
> Two things to notice: the **point forecast converges** to 5 while the **interval widens**, and the limiting MSE is the unconditional variance $\gamma_0 = \sigma^2\sum\psi_j^2 = 1 + \frac{1}{1-0.36} \cdot 1 = 1 + 1.5625 = 2.5625$, reached quickly. Beyond about $s=6$ the forecast is effectively "5, plus or minus 3.1" — the model has nothing left to say.

---

### Exercise 5 — Deriving the MA($\infty$) form of an ARMA(2,1)

Take the lecture's ARMA(2,1): $\phi(L) = (1-0.2L)(1-0.1L)$, $\theta(L) = 1+0.2L$. Derive $\psi_j$ in closed form and verify the first four terms against the recursion.

> [!example]- Solution
> **Closed form.** From the partial fractions worked in §4,
> $$\phi(L)^{-1} = \frac{2}{1-0.2L} - \frac{1}{1-0.1L} = \sum_{j=0}^\infty\big(2(0.2)^j - (0.1)^j\big)L^j$$
> Multiply by $\theta(L) = 1+0.2L$. Writing $a_j = 2(0.2)^j-(0.1)^j$, the coefficient of $L^j$ in $\Psi(L)$ is $\psi_j = a_j + 0.2\,a_{j-1}$ (with $a_{-1}=0$):
> $$\boxed{\;\psi_j = \big(2(0.2)^j - (0.1)^j\big) + 0.2\big(2(0.2)^{j-1} - (0.1)^{j-1}\big),\qquad j\ge1\;}$$
> which simplifies to $\psi_j = 4(0.2)^j - 3(0.1)^j$ for $j \ge 1$ (since $0.2 \cdot 2(0.2)^{j-1} = 2(0.2)^j$ and $0.2(0.1)^{j-1} = 2(0.1)^j$).
>
> **Check the first four:**
>
> | $j$ | $a_j$ | Closed form $\psi_j$ | Recursion $\psi_j = 0.3\psi_{j-1} - 0.02\psi_{j-2} + \theta_j$ |
> |---|---|---|---|
> | 0 | $1$ | $1$ | $\psi_0 = 1$ |
> | 1 | $0.3$ | $4(0.2)-3(0.1) = 0.5$ | $0.3(1) + 0.2 = 0.5$ ✓ |
> | 2 | $0.07$ | $4(0.04)-3(0.01) = 0.13$ | $0.3(0.5)-0.02(1) = 0.13$ ✓ |
> | 3 | $0.015$ | $4(0.008)-3(0.001) = 0.029$ | $0.3(0.13)-0.02(0.5) = 0.029$ ✓ |
>
> Both routes agree. **The recursion** $\psi_j = \sum_i\phi_i\psi_{j-i} + \theta_j$ (with $\theta_j = 0$ for $j>q$) is the general rule for extracting $\Psi(L) = \theta(L)/\phi(L)$ — just polynomial long division, and it is what you would actually code. The closed form is only worth deriving when you need the asymptotic decay rate, here governed by the dominant root $0.2$.
>
> Note $\psi_j \to 0$ geometrically at rate $0.2$: this ARMA has very short memory despite being second-order, because both roots are small. Its unconditional variance is $\sigma^2\sum\psi_j^2 \approx 1.27$.

---

## 📝 Summary

- **Random walk** $y_t = y_{t-1}+\varepsilon_t$: $\mathbb{E}[y_t] = y_0$, $\mathrm{Var}(y_t) = t\sigma^2$, $\mathrm{Cov}(y_t,y_{t-k}) = (t-k)\sigma^2$, $\rho_k(t) = \sqrt{(t-k)/t}\to1$. Non-stationary; **shocks are permanent** ($\psi_j\equiv1$). With drift $c$, the mean also trends: $\mathbb{E}[y_t] = y_0+tc$.
- **AR(1):** $\mathbb{E}=\tfrac{\alpha}{1-\phi}$, $\gamma_0 = \tfrac{\sigma^2}{1-\phi^2}$, $\gamma_k = \phi\gamma_{k-1}$, $\rho_k = \phi^k$. The ACF **decays geometrically and never cuts off**. Centring by $\mu$ removes the intercept from every derivation.
- **AR(2):** stationary iff the roots of $1-\phi_1z-\phi_2z^2$ lie outside the unit circle. $\rho_1 = \tfrac{\phi_1}{1-\phi_2}$, $\rho_2 = \phi_1\rho_1+\phi_2$, $\gamma_0 = \tfrac{(1-\phi_2)\sigma^2}{(1+\phi_2)[(1-\phi_2)^2-\phi_1^2]}$. **The ACF obeys the same difference equation as the process**, so complex roots give an oscillating ACF.
- **AR($p$) Yule–Walker:** $\gamma_j = \sum_i\phi_i\gamma_{j-i}$ for $j\ge1$ plus $\gamma_0 = \sum_i\phi_i\gamma_i+\sigma^2$; in matrix form $\vec\gamma = \Gamma\vec\phi$ with $\Gamma$ Toeplitz. No closed form for $\gamma_0$ when $p\ge3$.
- **MA($q$):** $\mathrm{Var} = (1+\sum\theta_i^2)\sigma^2$ and $\gamma_k = \sigma^2\sum_j\theta_j\theta_{j+k}$ for $k\le q$, **zero beyond**. Stationary for **any** parameters; the ACF **cuts off at lag $q$** — the mirror image of the AR's geometric tail.
- **Invertibility** (roots of $\theta(z)$ outside the unit circle) gives an AR($\infty$) representation and resolves the identification problem that $\theta$ and $1/\theta$ produce identical ACFs. Stationarity constrains $\phi(L)$; invertibility constrains $\theta(L)$.
- **ARMA($p,q$):** $\phi(L)Y_t = \phi_0+\theta(L)\varepsilon_t$, with $\Psi(L) = \theta(L)/\phi(L)$ obtained by factoring, partial fractions and geometric expansion. Its appeal is **parsimony**.
- **Forecasting:** the optimal forecast under quadratic loss is $\mathbb{E}(Y_{t+1}|X_t)$; the Wiener–Kolmogorov formula $\hat Y_{t+s|t} = \mu + [\psi(L)/L^s]_+\varepsilon_t$ implements it by deleting unobservable future shocks. For AR(1), $\hat Y_{t+s|t} = \mu+\phi^s(Y_t-\mu)$. For MA($q$), forecasts equal $\mu$ once $s>q$. $\mathrm{MSE}(s) = (1+\psi_1^2+\cdots+\psi_{s-1}^2)\sigma^2$ rises with $s$ toward $\mathrm{Var}(Y_t)$.

---

## ⚠️ Important Notes

> [!warning] Sign conventions will bite you
> The AR polynomial carries **minus** signs, the MA polynomial **plus** signs:
> $$\phi(L) = 1 - \phi_1L - \cdots - \phi_pL^p, \qquad \theta(L) = 1 + \theta_1L+\cdots+\theta_qL^q$$
> So $(1 - 1.1L + 0.18L^2)$ means $\phi_1 = 1.1$ and $\phi_2 = \mathbf{-0.18}$. Getting this backwards flips your stationarity verdict. Note also that some textbooks (and R's `arima`) use $\theta(L) = 1-\theta_1L-\cdots$; `statsmodels` uses the $+$ convention above. **Check the sign convention of any software before interpreting an estimated $\theta$.**

> [!warning] Two slide typos in the MA(2) example
> The worked example $Y_t = (1-\tfrac56L+\tfrac16L^2)\varepsilon_t$ contains two errors:
> 1. $\gamma_0$ is printed as $\tfrac{31}{19}$; the correct value is $\tfrac{31}{18} = 1 + \tfrac{25}{36}+\tfrac1{36}$.
> 2. The characteristic equation is printed as $1+\tfrac56z+\tfrac16z^2 = 0$ with roots $z = -2,-3$; the signs are wrong. Since $\theta_1 = -\tfrac56$, it is $1-\tfrac56z+\tfrac16z^2=0$, with roots $z = \mathbf{2},\ \mathbf{3}$.
>
> The invertibility conclusion (both roots outside the unit circle) is unaffected. The AR(3) Yule–Walker example, by contrast, I re-solved exactly and it is **correct**.

> [!warning] The intercept is not the mean
> In $Y_t = \mu + \phi_1Y_{t-1}+\phi_2Y_{t-2}+u_t$, $\mu$ is the **intercept**; the mean is $\mathbb{E}(Y) = \mu/(1-\phi_1-\phi_2)$. The slides use $\mu$ for both (and $\phi_0$ for the intercept on one slide). `statsmodels`' `ARIMA` reports `const` as the **mean** when `trend='c'`, not the intercept — another place to check conventions before comparing numbers.

> [!tip] The identification cheat sheet (previewing chapter 05)
> | Process | ACF | PACF |
> |---|---|---|
> | **AR($p$)** | Tails off (geometric / damped oscillation) | **Cuts off after lag $p$** |
> | **MA($q$)** | **Cuts off after lag $q$** | Tails off |
> | **ARMA($p,q$)** | Tails off after lag $q$ | Tails off after lag $p$ |
> | **Random walk** | Decays **linearly**, stays near 1 | Single spike $\approx 1$ at lag 1 |
>
> Everything derived in this chapter feeds directly into this table.

> [!note] Why $\mathbb{E}[\varepsilon_t(Y_t-\mu)] = \sigma^2$, not $0$
> A recurring stumble. $\mathrm{Cov}(\varepsilon_t, Y_{t-k}) = 0$ for $k \ge 1$ — the shock is unrelated to the *past*. But $\varepsilon_t$ **is a component of** $Y_t$, so $\mathbb{E}[\varepsilon_t(Y_t-\mu)] = \mathbb{E}[\varepsilon_t^2] = \sigma^2$. This is exactly why the $k=0$ Yule–Walker equation carries the extra $+\sigma^2$ that the $k\ge1$ equations do not.

> [!note] Over-differencing is a real cost
> If a series is already stationary, differencing it introduces a **non-invertible MA(1) unit root** into the errors ($\theta = -1$), which inflates variance and breaks the invertibility that forecasting depends on. Difference only when the data demand it. The symptom: a large negative spike at lag 1 in the ACF of the differenced series.

> [!tip] Long-horizon forecasts are always boring — and that's correct
> Every stationary ARMA forecast converges to $\mu$, and every forecast interval converges to $\mu \pm 1.96\sqrt{\gamma_0}$. This is not a defect. A stationary process genuinely contains no information about the distant future beyond its unconditional distribution. If someone shows you a 10-year ARMA forecast that is not essentially flat, either the model has a unit root, or it has a deterministic trend, or something is wrong.

> [!warning] Gaps in the source slides
> - **Unit-root tests are never introduced.** The lecture spends seven slides establishing that random walks are non-stationary but never presents the **ADF, Phillips–Perron or KPSS** tests that detect them. Given the emphasis, this material is presumably assumed or deferred to Lecture 5 — worth confirming with the lecturer, since it is highly examinable.
> - **The `ρ_k(t) = √((t−k)/t)` result on the random-walk summary slide is stated without derivation.** I have supplied it above; it follows from $\gamma_k/\sqrt{\gamma_0(t)\gamma_0(t-k)}$.
> - **Duplicate slides**: the AR(1) Yule–Walker derivation appears twice (s14–s16 and s17–s18), and the MA($q$)/MA($\infty$) definitions appear twice (s45/s47 and s50/s51). Not additional content.
> - **HTML extraction truncated every inline `<`**, so conditions written as `\(|\phi| < 1\)` lost their right-hand side. All such inequalities above are reconstructed from context. Affected slides include the AR(1) stationarity conditions, the MA($\infty$) square-summability condition, and the ARMA(1,1) forecasting preamble.
> - **Slide 25 and 26 ("Long-Run Mean, Variance, Covariance, and ACF"; "MA($\infty$) Representation") extracted as titles only** — their entire bodies were lost to the `<` truncation. The content is recoverable from the surrounding slides, and I have reconstructed it, but the original wording is gone.
> - **Simulation figures are not stored** in the notebook (no saved outputs), so the random-walk-vs-AR(1) comparison plot and the AR(1) simulation plots were reconstructed from the plotting code and theory rather than seen.
> - **Exercise 3.1 and 3.2 have no provided solutions.** My answers above are independently derived and arithmetically verified.
> - **Two code cells contain Vietnamese comments** (`số bước thời gian`, `nhiễu trắng`, `HÀM MÔ PHỎNG AR(1)`) — noted in case a future reader wonders about the mixed language.

---

**Previous:** [[03 - Stationarity and Difference Equations]] · **Next:** [[05 - ACF, PACF and the Box-Jenkins Methodology]] · **Index:** [[00-Index]]

#time-series #arma #yule-walker #random-walk #unit-root #forecasting
