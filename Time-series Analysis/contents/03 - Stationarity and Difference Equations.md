---
subject: Time-series Analysis
chapter: 03
tags: [ds, time-series, stationarity, difference-equations, impulse-response]
source: "documents/slides/lecture 3_timeseries_DSEB.ipynb (Lecture 3 — Basic Concepts and Difference Equations, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 1–3"
---

# Stationarity and Difference Equations

> [!abstract] Where this sits in the course
> Chapter [[02 - Trend, Seasonality and Decomposition]] removed trend and seasonality from a series. **What is left over is what this chapter models.** Everything from [[04 - AR, MA and ARMA Processes|AR/MA/ARMA]] onward is a special case of the difference equations derived here, so this is the most load-bearing chapter of the subject — if the algebra of the lag operator and the characteristic roots is solid, every later model is bookkeeping on top of it.

---

## 📘 Main Knowledge

### 1. Stationarity

A time series model is only estimable if the *same* statistical structure is being observed repeatedly. That is what stationarity buys you: one realisation of a process becomes usable as if it were many draws from a fixed distribution.

#### Strict stationarity

A stochastic process $\{X_t\}$ is **strictly stationary** if its entire joint distribution is invariant to a shift in time. For any set of dates $t_1,\dots,t_k$ and any shift $\tau$:

$$
F_{X_{t_1},\dots,X_{t_k}}(x_1,\dots,x_k)
=
F_{X_{t_1+\tau},\dots,X_{t_k+\tau}}(x_1,\dots,x_k)
$$

Nothing about the process depends on *where* you are in time — only on the spacing between observations. This is extremely strong: it constrains all moments, all higher-order dependence, the shape of every marginal, everything.

#### Weak (covariance) stationarity

In practice we only need the **first two moments** to be time-invariant:

$$
\mathbb{E}[X_t] = \mu,
\qquad
\mathrm{Var}(X_t) = \sigma^2,
\qquad
\mathrm{Cov}(X_t, X_{t+h}) = \gamma(h)
$$

The three requirements, in words:

1. **Constant mean** — the series does not drift.
2. **Constant variance** — the spread of fluctuations does not grow or shrink.
3. **Autocovariance depends only on the gap $h$, never on $t$** — the relationship between January and February is the same as between July and August.

> [!important] Which one do the models actually need?
> **AR, MA and ARMA models require only weak stationarity.** This is the whole reason weak stationarity is the working definition in this course — strict stationarity is a theoretical ideal you almost never verify, whereas the three moment conditions above can be checked from data.

> [!note] The two coincide under Gaussianity
> A Gaussian distribution is fully described by its mean and covariance. So for a **Gaussian process**, weak stationarity $\Rightarrow$ strict stationarity. Outside the Gaussian world the implication runs one way only: strict $\Rightarrow$ weak (provided the second moments exist at all — a strictly stationary i.i.d. Cauchy process is not weakly stationary, because its variance is infinite).

#### White noise

**White noise** is the elementary building block — the "atom" of every model in this course. $\varepsilon_t \sim WN(0,\sigma^2)$ means:

$$
\mathbb{E}[\varepsilon_t] = 0,
\qquad
\mathrm{Var}(\varepsilon_t) = \sigma^2,
\qquad
\mathrm{Cov}(\varepsilon_t,\varepsilon_s) = 0 \;\; \text{for } t \neq s
$$

It is stationary by construction and completely unpredictable from its own past. Every model below is a **filter** that takes white noise as input and produces a correlated series as output — see [[Mathematical Statistics/contents/04 - Sampling Distributions|sampling distributions]] for why the i.i.d. assumption matters when you later do inference on the parameters.

> [!warning] White noise is *not* the same as i.i.d.
> White noise requires only **zero correlation**, not independence. A GARCH process (see [[09 - ARCH, GARCH and Extensions]]) has white-noise residuals — uncorrelated — while its *squared* residuals are strongly autocorrelated. Zero linear dependence, plenty of nonlinear dependence. This distinction is exactly what makes volatility modelling possible.

---

### 2. The Wold Decomposition

The **Wold decomposition** is the theoretical justification for the entire ARMA framework. It says that *every* covariance-stationary process can be written as:

$$
y_t = \underbrace{\sum_{j=0}^{\infty} \psi_j \, \varepsilon_{t-j}}_{\text{stochastic part}} \;+\; \underbrace{\eta_t}_{\text{deterministic part}}
$$

| Component | Meaning |
|---|---|
| $\varepsilon_t$ | White noise: $\mathbb{E}[\varepsilon_t]=0$, $\mathrm{Var}(\varepsilon_t)=\sigma^2$ |
| $\psi_j$ | **Dynamic multipliers** — how strongly a shock $j$ periods ago still affects today |
| $\eta_t$ | Deterministic component (trend, fixed seasonal pattern) — perfectly predictable from the infinite past |

**Why this matters so much:** it means an $MA(\infty)$ representation always exists. Every stationary process is a weighted sum of its own past shocks. AR, MA and ARMA models are therefore not arbitrary functional forms — they are **parsimonious approximations to the Wold representation**, using a handful of parameters to capture an infinite sequence of $\psi_j$'s.

The whole of §4 below is really about one question: *given a model, what are the $\psi_j$?*

> [!note] Normalisation
> Conventionally $\psi_0 = 1$ (a shock enters contemporaneously one-for-one) and $\sum_{j=0}^\infty \psi_j^2 < \infty$ (square-summability), which is what guarantees the infinite sum converges in mean square.

---

### 3. The Lag Operator

The lag operator turns *time-indexed recursions* into *ordinary algebra*. Almost every trick in this course is really a polynomial manipulation in disguise.

#### Definition

$$
L y_t = y_{t-1},
\qquad
L^2 y_t = y_{t-2},
\qquad \ldots \qquad
L^k y_t = y_{t-k}
$$

$L$ shifts the series **backward** by one period. Treating $L$ as if it were a number is legitimate: it behaves algebraically like a scalar.

#### Properties

| Property | Statement |
|---|---|
| Linearity | $L(a y_t + b x_t) = a\,L y_t + b\,L x_t$ |
| Powers compose | $L^k L^m y_t = L^{k+m} y_t$ |
| First difference | $(1 - L)y_t = y_t - y_{t-1} \equiv \Delta y_t$ |
| Inverse (if convergent) | $(1-L)^{-1} y_t = y_t + y_{t-1} + y_{t-2} + \cdots$ |
| Acts on noise too | $L\varepsilon_t = \varepsilon_{t-1}$ |
| Polynomials multiply | $(1-aL)(1-bL)y_t = \big(1 - (a+b)L + abL^2\big)y_t$ |
| Higher differences | $\Delta^k y_t = (1-L)^k y_t$ |

#### Intuition on a concrete series

$$
\begin{aligned}
y_t &= [10,\;12,\;15,\;18,\;20] \\
L y_t &= [\,\text{–},\;10,\;12,\;15,\;18] \\
(1-L)y_t &= [\,\text{–},\;2,\;3,\;3,\;2]
\end{aligned}
$$

The first entry is lost each time you lag — **differencing costs you one observation per difference taken**. This connects directly to the `.shift()` and `.diff()` operations from [[01 - What is a Time Series]].

#### Why it is useful

An AR(2), written the long way:

$$
y_t = a_1 y_{t-1} + a_2 y_{t-2} + \varepsilon_t
$$

becomes, after moving the lags to the left:

$$
(1 - a_1 L - a_2 L^2)\,y_t = \varepsilon_t
$$

The parenthesis is a **polynomial in $L$**. Everything you know about polynomials — factoring, roots, partial fractions, geometric series — now applies to a dynamic system. The payoff is immediate:

$$
y_t = \frac{1}{1 - aL}\,\varepsilon_t
 = \varepsilon_t + a\varepsilon_{t-1} + a^2\varepsilon_{t-2} + \cdots
$$

An AR(1) has been *inverted* into its Wold ($MA(\infty)$) form by a one-line geometric-series expansion. The same manoeuvre drives:

- compact notation for AR, MA, ARIMA, SARIMA and VAR models,
- analysis of stability, persistence and oscillation,
- **impulse response functions (IRFs)**,
- the derivation of the Wold representation itself.

---

### 4. Difference Equations

#### General forms

$$
\begin{aligned}
\text{First order:} \quad & Y_t = \alpha + \beta Y_{t-1} + \varepsilon_t \\
\text{Second order:} \quad & Y_t = \alpha + \beta_1 Y_{t-1} + \beta_2 Y_{t-2} + \varepsilon_t \\
\text{Order } p: \quad & Y_t = \alpha + \sum_{i=1}^{p}\beta_i Y_{t-i} + \varepsilon_t
\end{aligned}
$$

In lag-operator form:

$$
(1 - \beta_1 L - \beta_2 L^2 - \cdots - \beta_p L^p)\,Y_t = \alpha + \varepsilon_t
$$

---

#### 4.1 First-order difference equation

$$
y_t = \phi\, y_{t-1} + w_t
$$

- $y_t$ — value of the variable at time $t$
- $\phi$ — how strongly the past carries into the present
- $w_t$ — the shock (deterministic or stochastic; usually white noise)

**Solve by repeated substitution.** Replace $y_{t-1}$ with $\phi y_{t-2} + w_{t-1}$, then $y_{t-2}$, and so on down to $y_0$:

$$
y_t = \phi^t y_0 + \sum_{i=0}^{t-1}\phi^{i} w_{t-i}
= w_t + \phi w_{t-1} + \phi^2 w_{t-2} + \cdots + \phi^{t-1}w_1 + \phi^t y_0
$$

Two readings of this identity:

1. **The initial condition $y_0$ is scaled by $\phi^t$.** If $|\phi|<1$ this dies out — the process forgets where it started. If $|\phi|\ge 1$ it does not.
2. **Every past shock survives, weighted by $\phi^{\text{age}}$.** This is the Wold representation with $\psi_j = \phi^j$.

#### 4.2 Dynamic multipliers

The **dynamic multiplier** answers: *if a one-unit shock hits at time $t$, how much of it is still visible $j$ periods later?* It is a partial derivative of the solution:

$$
\frac{\partial y_t}{\partial w_{t-j}} =
\begin{cases}
\phi^{j}, & j = 0,1,\ldots,t-1 \\
0, & j \ge t
\end{cases}
\qquad\Longleftrightarrow\qquad
\boxed{\;\frac{\partial y_{t+j}}{\partial w_t} = \phi^{j}\;}
$$

(The two forms say the same thing read forwards or backwards in time. The zero for $j \ge t$ is just because the process started at $t=0$ — shocks before the beginning do not exist.)

Short-run effects:

$$
\frac{\partial y_{t+1}}{\partial w_t} = \phi,
\qquad
\frac{\partial y_{t+2}}{\partial w_t} = \phi^2
$$

**Cumulative effect** after $h$ periods (a finite geometric sum):

$$
\sum_{j=0}^{h}\frac{\partial y_{t+j}}{\partial w_t} = \sum_{j=0}^{h}\phi^j = \frac{1-\phi^{h+1}}{1-\phi}
$$

**Long-run cumulative effect** — the total lifetime impact of a one-off shock:

$$
\sum_{j=0}^{\infty}\frac{\partial y_{t+j}}{\partial w_t} = \frac{1}{1-\phi},
\qquad \text{provided } |\phi| < 1
$$

> [!tip] Reading $\phi$ off a chart
> | $\phi$ | Behaviour of $\psi_j = \phi^j$ |
> |---|---|
> | $0 < \phi < 1$ | Smooth geometric decay to zero — persistent but stable |
> | $-1 < \phi < 0$ | Alternating sign, shrinking magnitude — decaying oscillation, period 2 |
> | $\phi = 1$ | $\psi_j = 1$ forever — **random walk**, shocks are permanent |
> | $\phi > 1$ | Explodes monotonically |
> | $\phi < -1$ | Explodes while alternating sign |
>
> The lecture's simulation plots exactly the four cases $\phi \in \{0.8,\,-0.8,\,1.1,\,-1.1\}$ as stem plots of $\psi_j$ over $j=0,\dots,20$. The $\phi=1$ boundary case is the subject of the unit-root discussion in [[04 - AR, MA and ARMA Processes]].

**Economic reading.** The dynamic multiplier is the *transmission mechanism*: how a policy shock, a demand shock or a noise term propagates through the system over time. $|\phi|<1$ means a finite long-run effect $\tfrac{1}{1-\phi}$; $|\phi|\ge 1$ means the system is unstable or explosive and shocks never wash out.

---

#### 4.3 Second-order difference equation

$$
y_t = \phi_1 y_{t-1} + \phi_2 y_{t-2} + w_t
$$

Repeated substitution still works but gets ugly fast:

$$
\begin{aligned}
y_t &= \phi_1(\phi_1 y_{t-2} + \phi_2 y_{t-3} + w_{t-1}) + \phi_2 y_{t-2} + w_t \\
&= (\phi_1^2+\phi_2)y_{t-2} + \phi_1\phi_2 y_{t-3} + [\,w_t + \phi_1 w_{t-1}\,] \\
&= \cdots \\
&= \cdots + \big[\,w_t + \phi_1 w_{t-1} + (\phi_1^2+\phi_2)w_{t-2} + \big((\phi_1^2+\phi_2)\phi_1 + \phi_1\phi_2\big)w_{t-3}\,\big]
\end{aligned}
$$

Reading off the coefficients gives the dynamic multipliers:

$$
\psi_1 = \frac{\partial y_{t+1}}{\partial w_t} = \phi_1,
\qquad
\psi_2 = \frac{\partial y_{t+2}}{\partial w_t} = \phi_1^2 + \phi_2,
\qquad
\psi_3 = \frac{\partial y_{t+3}}{\partial w_t} = \phi_1^3 + 2\phi_1\phi_2
$$

This is clearly not scalable. Two better routes exist, and both are used below: the **matrix / companion-form** route (§4.4) and the **lag-polynomial factorisation** route (§4.7).

#### 4.4 Matrix (state-space) form

Stack the current and previous value into a vector and the second-order scalar equation becomes a **first-order vector** equation:

$$
\begin{bmatrix} y_t \\ y_{t-1}\end{bmatrix}
=
\begin{bmatrix} \phi_1 & \phi_2 \\ 1 & 0 \end{bmatrix}
\begin{bmatrix} y_{t-1} \\ y_{t-2}\end{bmatrix}
+
\begin{bmatrix} w_t \\ 0 \end{bmatrix}
\qquad\Longleftrightarrow\qquad
\mathbf{y}_t = F\mathbf{y}_{t-1} + \mathbf{w}_t
$$

The second row is the trivial identity $y_{t-1} = y_{t-1}$ — it exists only to carry the lag forward. Recursing exactly as in the scalar case:

$$
\mathbf{y}_t = F^t \mathbf{y}_0 + \begin{bmatrix}w_t\\0\end{bmatrix} + F\begin{bmatrix}w_{t-1}\\0\end{bmatrix} + F^2\begin{bmatrix}w_{t-2}\\0\end{bmatrix} + \cdots + F^{t-1}\begin{bmatrix}w_1\\0\end{bmatrix}
$$

and the dynamic multiplier is simply the **top-left element of a matrix power**:

$$
\frac{\partial y_{t+j}}{\partial w_t} = \big(F^{j}\big)_{(1,1)}
$$

$F$ encodes the dependence structure; $F^j$ propagates a shock $j$ periods forward; its $(1,1)$ entry is the IRF. The system is stable when all eigenvalues of $F$ lie inside the unit circle. **This trick — rewriting order-$p$ dynamics as first-order vector dynamics — is the same idea that underpins the [[06 - The Kalman Filter and State-Space Models|state-space form]] and [[07 - SARIMA and Vector Autoregression|VAR models]].**

#### 4.5 AR($p$): companion matrix and eigenvalues

$$
Y_t = \phi_1 Y_{t-1} + \phi_2 Y_{t-2} + \cdots + \phi_p Y_{t-p} + W_t
$$

Define the **state vector** and stack:

$$
\xi_t = \begin{bmatrix} Y_t \\ Y_{t-1} \\ \vdots \\ Y_{t-p+1}\end{bmatrix},
\qquad
\xi_t = F\xi_{t-1} + V_t
$$

with the **companion matrix** and innovation vector:

$$
F = \begin{bmatrix}
\phi_1 & \phi_2 & \cdots & \phi_{p-1} & \phi_p \\
1 & 0 & \cdots & 0 & 0 \\
0 & 1 & \cdots & 0 & 0 \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \cdots & 1 & 0
\end{bmatrix},
\qquad
V_t = \begin{bmatrix} W_t \\ 0 \\ \vdots \\ 0 \end{bmatrix}
$$

Only the first row carries information; the subdiagonal of ones is pure bookkeeping.

**Recursive solution.** Given $\xi_{-1}$:

$$
\xi_0 = F\xi_{-1} + V_0,
\qquad
\xi_1 = F\xi_0 + V_1 = F^2\xi_{-1} + FV_0 + V_1
$$

and by induction, for $t \ge 0$:

$$
\xi_t = F^{t+1}\xi_{-1} + F^t V_0 + F^{t-1}V_1 + \cdots + FV_{t-1} + V_t
$$

The first equation of this system gives

$$
Y_{t+j} = f_{11}^{(j+1)}Y_{t-1} + \cdots + f_{1p}^{(j+1)}Y_{t-p} + f_{11}^{(j)}W_t + \cdots + W_{t+j}
\qquad\Longrightarrow\qquad
\frac{\partial Y_{t+j}}{\partial W_t} = f_{11}^{(j)}
$$

**Eigenvalues.** Solving $\lvert F - \lambda I_p\rvert = 0$ yields the **characteristic polynomial**:

$$
\lambda^p - \phi_1\lambda^{p-1} - \phi_2\lambda^{p-2} - \cdots - \phi_{p-1}\lambda - \phi_p = 0
$$

> [!note] Proposition 1.1
> The $p$ eigenvalues $\lambda_1,\dots,\lambda_p$ of the companion matrix $F$ are exactly the roots of the characteristic equation above.

If the eigenvalues are **distinct**, $F$ diagonalises as $F = T\Lambda T^{-1}$ with $\Lambda = \mathrm{diag}(\lambda_1,\dots,\lambda_p)$ and the columns of $T$ the eigenvectors. Then matrix powers are trivial:

$$
F^j = T\Lambda^j T^{-1},
\qquad
\Lambda^j = \mathrm{diag}(\lambda_1^j,\dots,\lambda_p^j)
$$

Extracting the $(1,1)$ element gives the closed-form IRF:

$$
\boxed{\;\psi_j = f_{11}^{(j)} = c_1\lambda_1^j + c_2\lambda_2^j + \cdots + c_p\lambda_p^j\;}
\qquad\text{with}\qquad
c_1 + c_2 + \cdots + c_p = 1
$$

The constraint $\sum c_i = 1$ is just $\psi_0 = 1$ — a shock enters one-for-one on impact.

> [!note] Proposition 1.2
> For **distinct** eigenvalues,
> $$c_i = \frac{\lambda_i^{\,p-1}}{\displaystyle\prod_{k=1,\,k\neq i}^{p}(\lambda_i - \lambda_k)}$$
>
> **Sanity check — AR(1):** with $p=1$ the characteristic equation is $\lambda - \phi_1 = 0$, so $\lambda_1 = \phi_1$, $c_1 = 1$, and $\partial Y_{t+j}/\partial W_t = \phi_1^j$ — exactly the §4.2 result. The general machinery reduces to the simple case.

**The impulse response is a weighted average of eigenvalues raised to the power $j$.** Each root is one independent "dynamic mode" of the system; the $c_i$ say how much weight each mode carries. If all $|\lambda_i| < 1$ every mode decays and the process is stable.

---

#### 4.6 AR(2): real vs complex roots

For the AR(2), $y_t = \phi_1 y_{t-1} + \phi_2 y_{t-2} + w_t$, the **inverted characteristic equation** is

$$
\lambda^2 - \phi_1\lambda - \phi_2 = 0
\qquad\Longrightarrow\qquad
\lambda_{1,2} = \frac{\phi_1 \pm \sqrt{\phi_1^2 + 4\phi_2}}{2}
$$

Everything hinges on the discriminant $\Delta = \phi_1^2 + 4\phi_2$.

> [!important] Two notations, one condition — learn both
> The slides use **both** conventions, and mixing them up is the single most common exam error.
>
> | Object | Equation | Stability condition |
> |---|---|---|
> | **Characteristic roots** $z$ (from the lag polynomial $1-\phi_1 L - \phi_2 L^2 = 0$) | $z^2 - \phi_1 z - \phi_2 = 0$ *in the slides' convention*, or $1-\phi_1 z-\phi_2 z^2=0$ | roots **outside** the unit circle, $\lvert z\rvert > 1$ |
> | **Inverse roots** $\lambda = 1/z$ (eigenvalues of $F$) | $\lambda^2 - \phi_1\lambda - \phi_2 = 0$ | roots **inside** the unit circle, $\lvert\lambda\rvert < 1$ |
>
> They are the same statement. Whenever you read "roots outside the unit circle" check whether the author means $z$ or $\lambda$. Python's `statsmodels` reports **inverse roots** (`arroots` are the $z$; the `.plot_diagnostics` / root plots show $1/z$ against the unit circle).

**Case 1 — real roots** ($\Delta = \phi_1^2 + 4\phi_2 > 0$):

$$
z_{1,2} = \frac{\phi_1 \pm\sqrt{\phi_1^2+4\phi_2}}{2},
\qquad
\lambda_{1,2} = \frac{1}{z_{1,2}}
$$

If all $|\lambda_i| < 1$ the process is stationary, adjustment toward equilibrium is **monotonic**, and there is no oscillation.

**Case 2 — complex conjugate roots** ($\Delta < 0$):

$$
\lambda_{1,2} = \frac{\phi_1 \pm i\sqrt{\lvert\phi_1^2 + 4\phi_2\rvert}}{2} = a \pm bi,
\qquad
R = \sqrt{a^2+b^2}
$$

with weights that are themselves complex conjugates:

$$
c_1 = \frac{\lambda_1}{\lambda_1-\lambda_2},
\quad
c_2 = \frac{\lambda_2}{\lambda_2-\lambda_1},
\qquad
c_1 = \alpha + \beta i,\;\; c_2 = \alpha - \beta i
$$

The multiplier $\psi_j = c_1\lambda_1^j + c_2\lambda_2^j$ is **always real** — the imaginary parts cancel. Here is the derivation, which is worth being able to reproduce.

##### Why complex roots give real, oscillating multipliers

Write $c = u + iv$ and put the root in polar form $\lambda = R(\cos\theta + i\sin\theta)$, with conjugates $\bar c = u-iv$, $\bar\lambda = R(\cos\theta - i\sin\theta)$. Then $\psi_j = c\lambda^j + \bar c\,\bar\lambda^j$.

**Step 1 — De Moivre.**

$$
\lambda^j = R^j(\cos j\theta + i\sin j\theta),
\qquad
\bar\lambda^j = R^j(\cos j\theta - i\sin j\theta)
$$

**Step 2 — multiply out.**

$$
(u+iv)(\cos + i\sin) = u\cos - v\sin + i(u\sin + v\cos)
$$
$$
(u-iv)(\cos - i\sin) = u\cos - v\sin - i(u\sin + v\cos)
$$

**Step 3 — add.** The imaginary parts are exact negatives and cancel:

$$
\psi_j = 2R^j\big[u\cos(j\theta) - v\sin(j\theta)\big]
$$

**Step 4 — rename** $A = 2u$, $B = -2v$:

$$
\boxed{\;\psi_j = R^j\big[A\cos(j\theta) + B\sin(j\theta)\big]\;}
$$

A **damped (or explosive) sine wave**. Two parameters govern it:

- $R$ — the **modulus**, controlling how fast the cycle dies out ($R^j$ envelope);
- $\theta$ — the **angle**, controlling how fast the system rotates, hence the cycle length.

##### Cycle length

$\cos(j\theta)$ repeats when $j\theta$ increases by $2\pi$, so the period is

$$
\boxed{\;T = \frac{2\pi}{\theta}\;}
$$

measured in periods (quarters, months, …) per oscillation.

| Modulus | Behaviour |
|---|---|
| $R < 1$ | **Convergent** — damped oscillation decaying to zero at rate $R^j$ |
| $R = 1$ | **Persistent** oscillation — constant amplitude, never dies |
| $R > 1$ | **Divergent** oscillation — amplitude grows at rate $R^j$ |

**Economic reading.** Complex roots are how a linear model produces *cycles*. With $R<1$ the system returns to equilibrium but overshoots on the way — the classic picture for output gaps, exchange rates and asset prices fluctuating around a long-run level. Real roots can only give monotone adjustment; if your data cycles, you need complex roots, which means you need at least AR(2).

> [!tip] Constructing an AR(2) with a target cycle
> Inverting $\lambda_{1,2} = Re^{\pm i\theta}$ gives
> $$\phi_1 = 2R\cos\theta, \qquad \phi_2 = -R^2$$
> The lecture uses this to generate IRFs with $\theta = 30° = \pi/6$ (so $T = 12$ periods) at $R \in \{0.9,\,1.0,\,1.1\}$ — damped, persistent and explosive cycles of the same length. Note $\phi_2 = -R^2 < 0$: **a negative $\phi_2$ is the signature of cyclical behaviour.**

##### The stability triangle

For an AR(2), stability ($\lvert\lambda_{1,2}\rvert<1$) holds exactly when all three of the following are satisfied:

$$
\begin{cases}
\phi_2 < 1 + \phi_1 \\
\phi_2 < 1 - \phi_1 \\
-1 < \phi_2 < 1
\end{cases}
$$

These three lines cut a **triangle** in $(\phi_1,\phi_2)$-space with vertices at $(-2,-1)$, $(2,-1)$ and $(0,1)$. Inside it the process is stationary; outside it is explosive.

Within the triangle, the parabola $\phi_2 = -\phi_1^2/4$ (i.e. $\Delta = 0$) splits the two regimes:

- **above** the parabola: $\Delta > 0$, real roots, monotone adjustment (the slides colour this **yellow**);
- **below** the parabola: $\Delta < 0$, complex roots, damped oscillation (coloured **green**).

Outside the triangle the process is unstable — explosive and non-oscillatory to the left and right, explosive and oscillatory below $\phi_2 = -1$.

> [!warning] The lecture's stability-triangle figure is mislabelled
> The plotting code shades **yellow** the region *between the slanted boundaries and $\phi_2 = 1$* — which lies **outside** the stability triangle, i.e. explosive — and shades **green** the entire interior of the triangle, without splitting it by the discriminant parabola. The accompanying caption ("yellow = stable with real roots, green = stable with complex roots") does not match what the code draws: the real/complex split is the **parabola** $\phi_2 = -\phi_1^2/4$, not the triangle's straight edges.
>
> **Trust the algebraic conditions above, not the colours in the slide.** Worth raising with the lecturer.

---

#### 4.7 Solving via the lag polynomial (the elegant route)

The whole AR(2) can be handled without matrices at all. Write it as

$$
(1 - \phi_1 L - \phi_2 L^2)\,Y_t = W_t
$$

and **factor the polynomial** using the roots $\lambda_1,\lambda_2$ of $\lambda^2 - \phi_1\lambda - \phi_2 = 0$:

$$
1 - \phi_1 L - \phi_2 L^2 = (1-\lambda_1 L)(1-\lambda_2 L),
\qquad
\phi_1 = \lambda_1+\lambda_2,
\quad
\phi_2 = -\lambda_1\lambda_2
$$

(Expand the product and match coefficients to verify — this is Vieta's formulas, cf. [[Linear Algebra/contents/00-Index|characteristic polynomials]].)

**Stability condition.** The AR(2) is stable **iff** $|\lambda_1| < 1$ and $|\lambda_2| < 1$ — both roots strictly inside the unit circle. Under this condition the process admits an $MA(\infty)$ representation

$$
Y_t = \sum_{j=0}^{\infty}\psi_j W_{t-j}
$$

with $\psi_j \to 0$ as $j\to\infty$.

**Partial fractions.** Invert the factored polynomial:

$$
Y_t = \frac{1}{(1-\lambda_1 L)(1-\lambda_2 L)}W_t
= \frac{1}{\lambda_1-\lambda_2}\left[\frac{\lambda_1}{1-\lambda_1 L} - \frac{\lambda_2}{1-\lambda_2 L}\right]W_t
$$

(Verify by putting the bracket over a common denominator: $\tfrac{\lambda_1(1-\lambda_2 L) - \lambda_2(1-\lambda_1 L)}{(1-\lambda_1L)(1-\lambda_2L)} = \tfrac{\lambda_1-\lambda_2}{(1-\lambda_1L)(1-\lambda_2L)}$.)

**Geometric expansion.** Each term expands as $\dfrac{1}{1-\lambda L} = 1 + \lambda L + \lambda^2 L^2 + \cdots$, giving

$$
Y_t = \left[\frac{\lambda_1}{\lambda_1-\lambda_2}(1+\lambda_1 L + \lambda_1^2 L^2+\cdots) - \frac{\lambda_2}{\lambda_1-\lambda_2}(1+\lambda_2 L+\lambda_2^2 L^2+\cdots)\right]W_t
$$

Collecting the coefficient of $L^j$:

$$
Y_t = \sum_{j=0}^{\infty}\big(c_1\lambda_1^j + c_2\lambda_2^j\big)W_{t-j},
\qquad
c_1 = \frac{\lambda_1}{\lambda_1-\lambda_2},
\quad
c_2 = -\frac{\lambda_2}{\lambda_1-\lambda_2}
$$

Note $c_1 + c_2 = \frac{\lambda_1-\lambda_2}{\lambda_1-\lambda_2} = 1$ ✓, matching Proposition 1.2 at $p=2$. **The lag-polynomial route and the eigenvalue route give the identical answer** — which they must, since the eigenvalues of $F$ *are* the roots of the lag polynomial.

##### Special cases

$$
\psi_j = c_1\lambda_1^j + c_2\lambda_2^j
\qquad\text{(distinct real roots)}
$$

$$
\psi_j = (j+1)\lambda^j
\qquad\text{(repeated root } \lambda_1=\lambda_2=\lambda\text{)}
$$

$$
\psi_j = R^j\big(A\cos j\theta + B\sin j\theta\big)
\qquad\text{(complex pair } \lambda = Re^{\pm i\theta}\text{)}
$$

> [!note] Why the repeated root gets an extra $j$
> With $\lambda_1 = \lambda_2$ the partial-fraction formula blows up ($\lambda_1-\lambda_2 = 0$ in the denominator). The correct expansion is $\frac{1}{(1-\lambda L)^2} = \sum_j (j+1)\lambda^j L^j$. The factor $(j+1)$ means a repeated root decays **more slowly initially** than a single root of the same size — the multiplier first rises, then falls. Same structure as repeated eigenvalues in a non-diagonalisable matrix.

---

#### 4.8 Order $p$: the general result

$$
y_t = \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + w_t
$$

**Characteristic equation:**

$$
\lambda^p - \phi_1\lambda^{p-1} - \phi_2\lambda^{p-2} - \cdots - \phi_p = 0
$$

**Stability:** all $|\lambda_i| < 1$ $\Longrightarrow$ multipliers converge, the process is stable, an $MA(\infty)$ representation exists.

**Weights and multipliers:**

$$
c_i = \frac{\lambda_i^{\,p-1}}{\displaystyle\prod_{k\neq i}(\lambda_i-\lambda_k)},
\qquad
\frac{\partial y_{t+j}}{\partial w_t} = \sum_{i=1}^{p}c_i\lambda_i^{\,j},
\quad j=0,1,2,\ldots
$$

Each root is a distinct **dynamic component**. If $|\lambda_i|<1$ that component decays; if any single $|\lambda_i| > 1$ the whole process is explosive — **one bad root is enough**.

#### 4.9 Computing multipliers by recursion (the practical method)

You rarely need closed forms. The multipliers **obey the same difference equation as the process itself**:

$$
\psi_0 = 1,
\qquad
\psi_1 = \phi_1,
\qquad
\psi_j = \phi_1\psi_{j-1} + \phi_2\psi_{j-2} + \cdots + \phi_p\psi_{j-p}
\quad (j \ge p)
$$

with $\psi_k = 0$ for $k < 0$. This is why the practical way to compute an IRF is to **simulate the model with $w_0 = 1$ and $w_t = 0$ for $t > 0$**, starting from zero initial conditions — the resulting path *is* $\{\psi_j\}$. Three lines of code, no eigenvalues required:

```python
def ar_irf(phis, horizon=36):
    """Impulse response of an AR(p) to a one-unit shock at j = 0."""
    p = len(phis)
    psi = np.zeros(horizon)
    for j in range(horizon):
        psi[j] = (1.0 if j == 0 else 0.0) + sum(
            phis[k] * psi[j - k - 1] for k in range(p) if j - k - 1 >= 0
        )
    return psi
```

**Key insight:** stability of the AR process $\Longleftrightarrow$ convergence of its multipliers. They are two descriptions of the same eigenvalue condition. The IRFs computed here for a scalar AR are the direct ancestor of the multivariate IRFs in [[07 - SARIMA and Vector Autoregression]] and the structurally identified IRFs in [[10 - Structural Vector Autoregression]].

---

## ✏️ Exercises

> These follow the lecture's own problem set (Questions 1–3), extended where the slides leave the answer as an exercise.

### Exercise 1 — Classify by stability

Let $\varepsilon_t \sim WN(0,1)$. Determine whether each process is stable (stationary), and state why.

1. $y_t = 0.5\,y_{t-1} + \varepsilon_t$
2. $y_t = 2.5\,y_{t-1} + \varepsilon_t$
3. $y_t = \varepsilon_t + 0.5\,\varepsilon_{t-1} - 0.6\,\varepsilon_{t-2}$
4. $y_t = 10 + 0.7\,y_{t-1} - 0.2\,y_{t-2} + \varepsilon_t$
5. $y_t = 0.5\,y_{t-1} - 0.8\,y_{t-2} + \varepsilon_t$

> [!example]- Solution
> **(1)** AR(1) with $\phi = 0.5$. Inverse root $\lambda = 0.5$, $|\lambda| = 0.5 < 1$ → **stable**. Multipliers $\psi_j = 0.5^j$ decay monotonically; long-run cumulative effect $= 1/(1-0.5) = 2$.
>
> **(2)** AR(1) with $\phi = 2.5$, so $\lambda = 2.5 > 1$ → **unstable / explosive**. A shock is amplified by 2.5× each period; no stationary solution exists (going forward in time), and no Wold representation.
>
> **(3)** This is an **MA(2)**, not an AR. A finite MA is *always* stationary — it is a finite weighted sum of white-noise terms, so its mean, variance and autocovariances are trivially time-invariant regardless of the coefficients. **Stable, always.** (The relevant question for an MA is *invertibility*, not stability — see Exercise 4.)
>
> **(4)** AR(2) with $\phi_1 = 0.7,\ \phi_2 = -0.2$; the intercept $10$ shifts the mean but does not affect stability. Discriminant $\Delta = 0.49 + 4(-0.2) = -0.31 < 0$ → **complex roots**.
> $$\lambda_{1,2} = \frac{0.7 \pm i\sqrt{0.31}}{2} = 0.35 \pm 0.2784\,i,\qquad R = \sqrt{\lambda_1\bar\lambda_1} = \sqrt{-\phi_2} = \sqrt{0.2} \approx 0.4472$$
> $R < 1$ → **stable, with damped oscillation**. Angle $\theta = \arctan(0.2784/0.35) \approx 0.6720$ rad, so cycle length $T = 2\pi/\theta \approx 9.35$ periods. The oscillation is heavily damped ($0.4472^j$), so in practice it is barely visible past a couple of cycles.
> Check the triangle: $\phi_2 = -0.2 < 1 - 0.7 = 0.3$ ✓; $-0.2 < 1 + 0.7 = 1.7$ ✓; $-1 < -0.2 < 1$ ✓.
> Unconditional mean: $\mu = \dfrac{10}{1 - 0.7 + 0.2} = \dfrac{10}{0.5} = 20$.
>
> **(5)** AR(2) with $\phi_1 = 0.5,\ \phi_2 = -0.8$. $\Delta = 0.25 - 3.2 = -2.95 < 0$ → complex roots, $R = \sqrt{-\phi_2} = \sqrt{0.8} \approx 0.894 < 1$ → **stable, oscillatory**, but only lightly damped. $\theta = \arccos\!\big(\phi_1/(2R)\big) = \arccos(0.5/1.789) \approx 1.2843$ rad → $T \approx 4.89$ periods. Pronounced ~5-period cycles that take many periods to die out.
>
> **Shortcut worth memorising:** for a **complex-root AR(2)**, $R = \sqrt{-\phi_2}$ and $\cos\theta = \phi_1/(2R)$. So the stationarity check reduces to $|\phi_2| < 1$, and the cycle length follows immediately.

---

### Exercise 2 — Wold representation and IRF

For the stable processes in Exercise 1, derive the Wold representation
$$y_t = \sum_{j=0}^{\infty}\psi_j\varepsilon_{t-j}, \qquad \psi_j = \frac{\partial y_{t+j}}{\partial\varepsilon_t}$$
and describe the shape of the impulse response.

> [!example]- Solution
> **(1) $y_t = 0.5y_{t-1}+\varepsilon_t$.** Invert directly:
> $$y_t = \frac{1}{1-0.5L}\varepsilon_t = \sum_{j=0}^\infty 0.5^j\varepsilon_{t-j} \qquad \psi_j = 0.5^j$$
> IRF: $1,\;0.5,\;0.25,\;0.125,\dots$ — smooth geometric decay, all positive, essentially zero by $j\approx 10$.
>
> **(3) MA(2).** It is *already* in Wold form:
> $$\psi_0 = 1,\quad \psi_1 = 0.5,\quad \psi_2 = -0.6,\quad \psi_j = 0 \;\; \forall j \ge 3$$
> IRF: exactly three non-zero bars, then **hard zero**. This finite cut-off is the defining visual signature of an MA process and is what lets you read $q$ off an ACF plot in [[05 - ACF, PACF and the Box-Jenkins Methodology]].
>
> **(4) $\phi_1 = 0.7,\ \phi_2 = -0.2$.** Use the recursion $\psi_j = 0.7\psi_{j-1} - 0.2\psi_{j-2}$:
>
> | $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
> |---|---|---|---|---|---|---|---|
> | $\psi_j$ | 1 | 0.7 | 0.29 | 0.063 | $-0.0139$ | $-0.0223$ | $-0.0128$ |
>
> ($\psi_2 = 0.7(0.7) - 0.2(1) = 0.29$; $\psi_3 = 0.7(0.29)-0.2(0.7) = 0.063$; $\psi_4 = 0.7(0.063)-0.2(0.29) = -0.0139$; …)
> Positive for the first four lags, then a small negative dip — one damped cycle of ~9 periods, and effectively dead by $j\approx 8$.
>
> **(5) $\phi_1 = 0.5,\ \phi_2 = -0.8$.** Recursion $\psi_j = 0.5\psi_{j-1} - 0.8\psi_{j-2}$:
>
> | $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
> |---|---|---|---|---|---|---|---|---|
> | $\psi_j$ | 1 | 0.5 | $-0.55$ | $-0.675$ | $0.1025$ | $0.5913$ | $0.2137$ | $-0.3661$ |
>
> Clear sign changes with a period of roughly 5 lags, and an envelope shrinking like $0.894^j$ — slow decay. Compare the two AR(2)s: **same qualitative mechanism (complex roots), completely different persistence**, and the difference is entirely $|\phi_2|$.

---

### Exercise 3 — Stationarity, invertibility and moments

Let $\varepsilon_t \sim WN(0,1)$ and consider
$$\text{(a) } y_t = 0.5\,y_{t-1}+\varepsilon_t \qquad\qquad \text{(b) } y_t = -0.2\,y_{t-1}+0.48\,y_{t-2}+\varepsilon_t$$

1. Are they stationary? Justify using the characteristic roots.
2. Are they invertible?
3. Compute $\mathbb{E}(y_t)$, $\mathrm{Var}(y_t)$, the autocovariances $\gamma_j$ and autocorrelations $\rho_j$ for $j=1,2,3$.
4. Find the coefficients of $\varepsilon_t,\varepsilon_{t-1},\varepsilon_{t-2},\varepsilon_{t-3}$ in the $MA(\infty)$ representation.

> [!example]- Solution
> **(a) AR(1), $\phi = 0.5$.**
>
> *Stationary?* $\lambda = 0.5$, $|\lambda|<1$ ✓ (equivalently the characteristic root $z = 1/0.5 = 2$ lies outside the unit circle).
>
> *Invertible?* Invertibility is a property of the **MA** part. A pure AR has no MA polynomial ($\theta(L)=1$), so it is trivially invertible. The meaningful direction here is the reverse: a *stationary* AR can be inverted into an $MA(\infty)$, which it can, since $|\phi|<1$.
>
> *Moments.* $\mathbb{E}(y_t)=0$ (no intercept). Taking variances of $y_t = 0.5y_{t-1}+\varepsilon_t$ under stationarity ($\gamma_0$ the same on both sides):
> $$\gamma_0 = \phi^2\gamma_0 + \sigma^2 \;\Rightarrow\; \gamma_0 = \frac{\sigma^2}{1-\phi^2} = \frac{1}{1-0.25} = \frac{4}{3} \approx 1.3333$$
> For an AR(1), $\gamma_j = \phi^j\gamma_0$ and $\rho_j = \phi^j$:
>
> | $j$ | 1 | 2 | 3 |
> |---|---|---|---|
> | $\gamma_j$ | $0.6667$ | $0.3333$ | $0.1667$ |
> | $\rho_j$ | $0.5$ | $0.25$ | $0.125$ |
>
> *$MA(\infty)$ coefficients:* $\psi_j = 0.5^j$ → $1,\;0.5,\;0.25,\;0.125$.
>
> ---
> **(b) AR(2), $\phi_1 = -0.2$, $\phi_2 = 0.48$.**
>
> *Stationary?* $\Delta = \phi_1^2+4\phi_2 = 0.04 + 1.92 = 1.96 > 0$ → **real roots**:
> $$\lambda_{1,2} = \frac{-0.2 \pm \sqrt{1.96}}{2} = \frac{-0.2 \pm 1.4}{2} = \{0.6,\; -0.8\}$$
> Both $|\lambda_i| < 1$ ✓ → **stationary**, with monotone-plus-alternating decay (the $-0.8$ root alternates in sign, the $0.6$ root does not). Triangle check: $0.48 < 1-(-0.2)=1.2$ ✓, $0.48 < 1+(-0.2)=0.8$ ✓, $-1<0.48<1$ ✓. Note the polynomial factors as $(1-0.6L)(1+0.8L)$.
>
> *Invertible?* Again, no MA part → trivially yes.
>
> *Moments.* $\mathbb{E}(y_t) = 0$. Use the **Yule–Walker** equations. Divide the model by $\gamma_0$ after multiplying by $y_{t-j}$ and taking expectations:
> $$\rho_1 = \frac{\phi_1}{1-\phi_2} = \frac{-0.2}{1-0.48} = \frac{-0.2}{0.52} \approx -0.3846$$
> $$\rho_2 = \phi_1\rho_1 + \phi_2 = (-0.2)(-0.3846)+0.48 = 0.5569$$
> $$\rho_3 = \phi_1\rho_2 + \phi_2\rho_1 = (-0.2)(0.5569)+(0.48)(-0.3846) = -0.2960$$
> Variance:
> $$\gamma_0 = \frac{\sigma^2}{1-\phi_1\rho_1-\phi_2\rho_2} = \frac{1}{1-(-0.2)(-0.3846)-(0.48)(0.5569)} = \frac{1}{1-0.0769-0.2673} \approx 1.5250$$
> Hence $\gamma_1 \approx -0.5865$, $\gamma_2 \approx 0.8493$, $\gamma_3 \approx -0.4514$.
>
> *$MA(\infty)$ coefficients* via $\psi_j = -0.2\psi_{j-1} + 0.48\psi_{j-2}$:
> $$\psi_0 = 1,\quad \psi_1 = -0.2,\quad \psi_2 = 0.04+0.48 = 0.52,\quad \psi_3 = -0.104 - 0.096 = -0.200$$
> (Cross-check with the closed form: $\lambda_1=0.6,\lambda_2=-0.8$ give $c_1 = \tfrac{0.6}{1.4} = 0.4286$, $c_2 = -\tfrac{-0.8}{1.4} = 0.5714$, $c_1+c_2=1$ ✓, and $\psi_2 = 0.4286(0.36)+0.5714(0.64) = 0.52$ ✓.)
>
> > [!warning] $\rho_1 \neq \phi_1$ for an AR(2)
> > This is a classic exam trap. Only for an AR(1) does the first autocorrelation equal the coefficient. For AR(2), $\rho_1 = \phi_1/(1-\phi_2)$, because $y_{t-1}$ is itself correlated with $y_{t-2}$. Separating the *direct* effect of lag 1 from this indirect channel is precisely the job of the **PACF** in [[05 - ACF, PACF and the Box-Jenkins Methodology]].

---

### Exercise 4 — Invertibility of an MA process

The lecture asks about invertibility but the slides never define it. Fill the gap: state the invertibility condition for $y_t = \varepsilon_t + \theta\varepsilon_{t-1}$, then decide whether $y_t = \varepsilon_t + 0.5\varepsilon_{t-1} - 0.6\varepsilon_{t-2}$ (Exercise 1.3) is invertible.

> [!example]- Solution
> **Definition.** An MA process is **invertible** if it can be rewritten as a convergent $AR(\infty)$ — i.e. today's shock can be recovered from the observed history of $y$. For $y_t = (1+\theta L)\varepsilon_t$:
> $$\varepsilon_t = \frac{1}{1+\theta L}y_t = y_t - \theta y_{t-1} + \theta^2 y_{t-2} - \cdots$$
> which converges iff $|\theta| < 1$. In general, an MA($q$) is invertible iff **all roots of $\theta(L)=0$ lie outside the unit circle** — the mirror image of the AR stationarity condition.
>
> **Why it matters.** Without invertibility the model is not *identified*: $y_t = \varepsilon_t + 2\varepsilon_{t-1}$ (with $\sigma^2=1$) and $y_t = u_t + 0.5u_{t-1}$ (with $\sigma_u^2=4$) have **identical** autocovariance functions. Any MA has an invertible twin with the same second-moment structure, and by convention we always report that one. It also means forecasting is possible from observed data alone.
>
> **The given process.** $\theta(L) = 1 + 0.5L - 0.6L^2$. Setting $\theta(z)=0$:
> $$-0.6z^2 + 0.5z + 1 = 0 \;\Longleftrightarrow\; 0.6z^2 - 0.5z - 1 = 0$$
> $$z = \frac{0.5 \pm \sqrt{0.25 + 2.4}}{1.2} = \frac{0.5 \pm 1.6279}{1.2} = \{1.7733,\; -0.9399\}$$
> The root $z_2 = -0.9399$ has $|z_2| < 1$ → **inside** the unit circle → **not invertible**. (Equivalently: the inverse roots are $1/1.7733 = 0.564$ and $1/(-0.9399) = -1.064$, and $|-1.064| > 1$.)
>
> So the process from Exercise 1.3 is **stationary but not invertible** — a clean demonstration that the two properties are independent. `statsmodels` will still fit it, but the estimated parameters are not the ones you would want to report.

---

### Exercise 5 — Simulation and IRF

$w_t \stackrel{iid}{\sim} N(0,1)$, $t = 0,\dots,T$ with $T = 50$.

**Part 1 — AR(1).** For $y_t = \phi y_{t-1} + w_t$, $y_{-1}=0$, and each $\phi \in \{-2.5,\,-0.8,\,0,\,0.6,\,1\}$: simulate and plot $\{y_t\}_{t=0}^{50}$, comment on stability, and plot $\psi_j$ for $j=0,\dots,10$.

**Part 2 — AR(2).** For $y_t = \phi_1 y_{t-1} + \phi_2 y_{t-2} + w_t$, $y_{-1}=0$, $y_{-2}=-1$: do the same for (i) $\phi_1=0.6,\ \phi_2=0.2$ and (ii) $\phi_1=-0.6,\ \phi_2=2.5$.

> [!example]- Solution
> ```python
> import numpy as np
> import matplotlib.pyplot as plt
>
> rng = np.random.default_rng(42)
> T = 50
>
> def simulate_ar(phis, T, init, rng):
>     p = len(phis)
>     w = rng.standard_normal(T + 1)
>     y = np.zeros(T + 1)
>     hist = list(init)                      # most recent last
>     for t in range(T + 1):
>         y[t] = sum(phis[k] * hist[-1 - k] for k in range(p)) + w[t]
>         hist.append(y[t])
>     return y
>
> def irf(phis, H=11):
>     p, psi = len(phis), np.zeros(H)
>     for j in range(H):
>         psi[j] = (1.0 if j == 0 else 0.0) + sum(
>             phis[k] * psi[j-k-1] for k in range(p) if j-k-1 >= 0)
>     return psi
> ```
>
> **Part 1 results.**
>
> | $\phi$ | $|\lambda|$ | Verdict | What the plot looks like |
> |---|---|---|---|
> | $-2.5$ | 2.5 | Explosive | Wild sign-alternating blow-up; by $t=50$ the values are astronomically large ($\sim 2.5^{50}\approx 10^{20}$). Plot on a log scale or the earlier observations vanish. |
> | $-0.8$ | 0.8 | Stationary | Jagged, rapidly alternating around 0. $\psi_j = (-0.8)^j$ flips sign every lag, decaying. |
> | $0$ | 0 | Stationary (white noise) | Pure noise, no persistence. $\psi_0=1$, all later $\psi_j = 0$. |
> | $0.6$ | 0.6 | Stationary | Smooth, gently wandering around 0. $\psi_j = 0.6^j$ decays monotonically; $\approx 0.006$ by $j=10$. |
> | $1$ | 1 | **Random walk** — non-stationary | No mean reversion; variance $\mathrm{Var}(y_t)=t\sigma^2$ grows without bound. $\psi_j = 1$ for all $j$ — **shocks are permanent**. |
>
> The $\phi=1$ case is the boundary and deserves particular attention: it is not explosive, but it is not stationary either. The unit-root tests in [[04 - AR, MA and ARMA Processes]] exist precisely to detect it.
>
> **Part 2(i) — $\phi_1=0.6,\ \phi_2=0.2$.** $\Delta = 0.36+0.8 = 1.16>0$ → real roots $\lambda = \frac{0.6\pm 1.077}{2} = \{0.8385,\,-0.2385\}$, both inside the unit circle → **stable**. Triangle check: $0.2 < 1-0.6 = 0.4$ ✓. IRF: $1,\;0.6,\;0.56,\;0.456,\;0.386,\;0.323,\dots$ — the dominant root $0.8385$ takes over, giving slow monotone decay with no oscillation. The series wanders persistently but always returns.
>
> **Part 2(ii) — $\phi_1=-0.6,\ \phi_2=2.5$.** **Not stable.** $\phi_2 = 2.5 > 1$ violates the triangle condition immediately. Explicitly: $\Delta = 0.36 + 10 = 10.36$, $\lambda = \frac{-0.6\pm 3.219}{2} = \{1.3096,\,-1.9096\}$. Both roots exceed 1 in modulus; the dominant one, $-1.9096$, alternates sign. The simulated series explodes with sign flips, growing roughly like $1.91^t$. IRF: $1,\;-0.6,\;2.86,\;-3.216,\;9.08,\dots$ — magnitudes increasing, sign alternating.
>
> **What to take away from the plots:** the *shape* of an IRF is a complete fingerprint of the roots. Monotone decay → real positive dominant root. Alternating decay → real negative root. Smooth sine wave → complex pair. Growth of any kind → a root outside the unit circle. You should be able to work backwards from an IRF plot to a qualitative description of the roots, and that is a very common exam question.

---

## 📝 Summary

- **Weak (covariance) stationarity** — constant mean, constant variance, autocovariance depending only on the lag $h$ — is all that AR/MA/ARMA models require. Strict stationarity constrains the whole joint distribution and is rarely checked; the two coincide for Gaussian processes.
- **White noise** is uncorrelated, not necessarily independent — the gap that GARCH exploits.
- The **Wold decomposition** guarantees every stationary process equals a deterministic part plus $\sum_{j\ge0}\psi_j\varepsilon_{t-j}$. ARMA models are compact parameterisations of that infinite sum, and everything reduces to finding the $\psi_j$.
- The **lag operator** $L^k y_t = y_{t-k}$ converts recursions into polynomial algebra: $(1-\phi_1L-\cdots-\phi_pL^p)y_t = \varepsilon_t$, and $(1-L)$ is the differencing operator.
- **Dynamic multipliers** $\psi_j = \partial y_{t+j}/\partial w_t$ *are* the impulse response function. For AR(1), $\psi_j = \phi^j$ with long-run cumulative effect $1/(1-\phi)$ when $|\phi|<1$.
- An AR($p$) becomes a first-order vector system $\xi_t = F\xi_{t-1}+V_t$ with $F$ the **companion matrix**; $\psi_j = (F^j)_{11}$, and the eigenvalues of $F$ are the roots of $\lambda^p - \phi_1\lambda^{p-1}-\cdots-\phi_p = 0$. Diagonalising gives $\psi_j = \sum_i c_i\lambda_i^j$ with $\sum_i c_i = 1$.
- **Stability $\Leftrightarrow$ all inverse roots inside the unit circle** ($|\lambda_i|<1$) $\Leftrightarrow$ all characteristic roots outside it ($|z_i|>1$). One violating root makes the whole process explosive.
- **Real roots → monotone decay; complex roots → damped cycles** $\psi_j = R^j[A\cos j\theta + B\sin j\theta]$ with modulus $R$ setting the decay rate and period $T = 2\pi/\theta$. For an AR(2) with complex roots, $R=\sqrt{-\phi_2}$ and $\cos\theta = \phi_1/(2R)$; the **stability triangle** $\{\phi_2<1\pm\phi_1,\; |\phi_2|<1\}$ is the full stationarity region.
- In practice, compute IRFs by the **recursion** $\psi_j = \sum_i \phi_i\psi_{j-i}$ with $\psi_0=1$ — no eigenvalues needed.

---

## ⚠️ Important Notes

> [!warning] "Inside" or "outside" the unit circle?
> The single biggest source of confusion in this course. Both statements are correct — they refer to different objects:
> - **Characteristic roots $z$** solve $1-\phi_1 z - \cdots - \phi_p z^p = 0$ → stability requires $|z| > 1$ (**outside**).
> - **Inverse roots / eigenvalues $\lambda = 1/z$** solve $\lambda^p - \phi_1\lambda^{p-1}-\cdots-\phi_p = 0$ → stability requires $|\lambda| < 1$ (**inside**).
>
> The lecture's problem set uses the "outside" phrasing while the derivations use the "inside" phrasing. Always identify which polynomial is being solved before applying a rule.

> [!warning] Stationarity ≠ invertibility
> - **Stationarity** is about the **AR** side (roots of $\phi(L)$).
> - **Invertibility** is about the **MA** side (roots of $\theta(L)$).
>
> A finite MA is always stationary regardless of its coefficients; an AR is always invertible. Exercise 1.3 gives a process that is stationary but *not* invertible. Don't apply the stability test to an MA and conclude it's non-stationary.

> [!warning] Don't confuse $\phi_1$ with $\rho_1$
> For AR(1) they coincide ($\rho_1 = \phi$). For AR(2) onward they do not: $\rho_1 = \phi_1/(1-\phi_2)$. The ACF mixes direct and indirect dependence; disentangling them is the PACF's job.

> [!tip] The AR(2) cheat sheet
> Memorise these — they turn most exam questions into arithmetic:
> - Stationarity: $\phi_2 < 1-\phi_1$, $\phi_2 < 1+\phi_1$, $-1<\phi_2<1$.
> - Roots real iff $\phi_1^2 + 4\phi_2 > 0$; complex (⇒ cycles) iff $\phi_1^2+4\phi_2 < 0$, which **requires $\phi_2 < 0$**.
> - Complex case: $R = \sqrt{-\phi_2}$, $\cos\theta = \phi_1/(2R)$, period $T = 2\pi/\theta$.
> - Unconditional mean with intercept $\alpha$: $\mu = \alpha/(1-\phi_1-\phi_2)$.
> - Yule–Walker: $\rho_1 = \phi_1/(1-\phi_2)$, $\rho_2 = \phi_1\rho_1+\phi_2$, $\rho_k = \phi_1\rho_{k-1}+\phi_2\rho_{k-2}$.

> [!note] The repeated-root case is easy to forget
> Proposition 1.2's formula for $c_i$ **divides by $(\lambda_i-\lambda_k)$** and therefore fails when roots coincide. The correct multiplier is $\psi_j = (j+1)\lambda^j$ — it rises before it falls. If an exam gives you $\phi_1^2 + 4\phi_2 = 0$ exactly, this is what is being tested.

> [!note] Explosive $\neq$ non-stationary, and $\phi=1$ is neither
> Three distinct regimes, often collapsed by mistake:
> - $|\lambda| < 1$: stationary, shocks decay.
> - $|\lambda| = 1$: **unit root** — non-stationary but not explosive; shocks are permanent; variance grows linearly in $t$. This is the random walk, and the object of ADF/KPSS testing.
> - $|\lambda| > 1$: explosive; shocks are amplified; essentially never a sensible model for economic data.

> [!warning] A note on the intercept
> An intercept $\alpha$ changes the **mean** ($\mu = \alpha/(1-\sum\phi_i)$) but has **no effect on stability**, which depends only on the $\phi_i$. Exercise 1.4's "$10 +$" is a distractor. But watch the denominator: as $\sum\phi_i \to 1$, the implied mean explodes — another symptom of approaching a unit root.

> [!warning] Gaps in the source slides
> - **HTML extraction destroyed every `<` sign in inline math.** The slides' HTML uses `\(|\phi| < 1\)` inline, and the `<` is parsed as the start of a tag, truncating the rest of the line. Conditions such as "$|\phi| < 1$", "$|\lambda_i| < 1$", "$R < 1$" and the stability-triangle inequalities were **reconstructed from context**. The mathematics is standard and unambiguous, but the *exact* wording of these slides could not be recovered.
> - **The stability-triangle figure contradicts its own caption** (see the warning in §4.6). The colour regions drawn by the plotting code are not the real-root/complex-root split the text describes. Verify with the lecturer before relying on the figure.
> - **Slide s17/s18 contains typos**: $\frac{\partial y_{t+2}}{\sigma_t}$ and $\frac{\partial y_{t+3}}{\sigma_t}$ should read $\partial w_t$ in the denominator, not $\sigma_t$. The two slides are also exact duplicates of each other.
> - **Duplicate slides throughout**: s56/s59 and s57/s60 are identical repeats of the problem-set slides; s45/s46 restate the same AR(2) stability condition twice. This is a slide-deck artefact, not additional content.
> - **Invertibility is asked about but never defined** in the deck (Question 2 asks "are these processes invertible?" with no prior definition). Exercise 4 above fills the gap from standard theory.
> - **No worked solutions** to the problem set are provided in the notebook. All solutions above are my own derivations — check the arithmetic independently before an exam.
> - **The final cell is a broken `nbconvert` command** pointing at a Colab URL; it contains no lecture content.
> - **Figures are generated by code, not stored** — the notebook has no saved outputs, so the actual plotted IRFs and the stability triangle were reconstructed from the plotting code rather than seen.

---

**Previous:** [[02 - Trend, Seasonality and Decomposition]] · **Next:** [[04 - AR, MA and ARMA Processes]] · **Index:** [[00-Index]]

#time-series #stationarity #difference-equations #impulse-response #lag-operator
