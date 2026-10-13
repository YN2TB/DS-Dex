---
subject: Time-series Analysis
chapter: 03
tags: [ds, time-series, stationarity, difference-equations, impulse-response]
source: "documents/slides/lecture 3_timeseries_DSEB.ipynb (Lecture 3 — Basic Concepts and Difference Equations, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 1–3"
---

# Stationarity and Difference Equations

[[02 - Trend, Seasonality and Decomposition]] removed trend and seasonality; what is left is modelled here. AR, MA and ARMA models ([[04 - AR, MA and ARMA Processes]]) are special cases of the difference equations in this chapter, so its lag-operator algebra and characteristic roots underpin the rest of the course.

## 📘 Main Knowledge

### Stationarity

Stationarity lets one realization be treated like repeated draws from a fixed structure.

- **Strict**: the joint distribution of $(X_{t_1},\dots,X_{t_k})$ equals that of $(X_{t_1+\tau},\dots,X_{t_k+\tau})$ for every shift τ.
- **Weak (covariance)**: $\mathbb E[X_t]=\mu$, $\operatorname{Var}(X_t)=\sigma^2$, $\operatorname{Cov}(X_t,X_{t+h})=\gamma(h)$ depending only on the lag $h$.

AR, MA and ARMA models need only weak stationarity. For a Gaussian process the two coincide; otherwise strict implies weak only if second moments exist (an i.i.d. Cauchy process is strictly but not weakly stationary).

**White noise** $\varepsilon_t\sim WN(0,\sigma^2)$: mean 0, variance σ², $\operatorname{Cov}(\varepsilon_t,\varepsilon_s)=0$ for $t\ne s$. It requires zero correlation, not independence: GARCH residuals are white noise while their squares are autocorrelated ([[09 - ARCH, GARCH and Extensions]]).

### Wold decomposition

Every covariance-stationary process can be written
$$y_t=\sum_{j=0}^\infty\psi_j\varepsilon_{t-j}+\eta_t,$$
with white noise $\varepsilon_t$, **dynamic multipliers** $\psi_j$ (normalized $\psi_0=1$, $\sum\psi_j^2<\infty$), and a deterministic part $\eta_t$ (perfectly predictable from the infinite past). So an MA(∞) representation always exists, and ARMA models are parsimonious approximations of it.

### The lag operator

$L^ky_t=y_{t-k}$. It is linear, powers add ($L^kL^m=L^{k+m}$), $(1-L)y_t=\Delta y_t$, $\Delta^k=(1-L)^k$, it acts on noise ($L\varepsilon_t=\varepsilon_{t-1}$), polynomials multiply ($(1-aL)(1-bL)=1-(a+b)L+abL^2$), and $(1-L)^{-1}y_t=y_t+y_{t-1}+\dots$ when convergent. Example: $y=[10,12,15,18,20]$ gives $Ly=[–,10,12,15,18]$ and $\Delta y=[–,2,3,3,2]$; each difference loses an observation.

An AR(2) $y_t=a_1y_{t-1}+a_2y_{t-2}+\varepsilon_t$ becomes $(1-a_1L-a_2L^2)y_t=\varepsilon_t$, and an AR(1) inverts to its Wold form by a geometric series: $y_t=(1-aL)^{-1}\varepsilon_t=\sum_ja^j\varepsilon_{t-j}$. The same algebra gives compact AR/MA/ARIMA/SARIMA/VAR notation, stability analysis and impulse responses.

### Difference equations

Order $p$: $Y_t=\alpha+\sum_{i=1}^p\beta_iY_{t-i}+\varepsilon_t$, or $(1-\beta_1L-\dots-\beta_pL^p)Y_t=\alpha+\varepsilon_t$.

**First order**, $y_t=\phi y_{t-1}+w_t$. Repeated substitution gives
$$y_t=\phi^ty_0+\sum_{i=0}^{t-1}\phi^iw_{t-i}.$$
The initial value fades if $|\phi|<1$; each past shock survives with weight $\phi^{\text{age}}$ (Wold with $\psi_j=\phi^j$).

**Dynamic multiplier** (impulse response): $\partial y_{t+j}/\partial w_t=\phi^j$. Cumulative effect over $h$ periods $\sum_{j=0}^h\phi^j=\frac{1-\phi^{h+1}}{1-\phi}$; long-run effect $\frac1{1-\phi}$ if $|\phi|<1$.

| φ | $\psi_j=\phi^j$ |
|---|---|
| $0<\phi<1$ | smooth decay |
| $-1<\phi<0$ | alternating decay |
| $\phi=1$ | constant: random walk, permanent shocks |
| $\phi>1$ | monotone explosion |
| $\phi<-1$ | alternating explosion |

(The lecture plots φ ∈ {0.8, −0.8, 1.1, −1.1}.)

**Second order**, $y_t=\phi_1y_{t-1}+\phi_2y_{t-2}+w_t$. Substitution gives $\psi_1=\phi_1$, $\psi_2=\phi_1^2+\phi_2$, $\psi_3=\phi_1^3+2\phi_1\phi_2$, which doesn't scale; two better routes follow.

### Companion matrix

Stack the lags: $\begin{bmatrix}y_t\\y_{t-1}\end{bmatrix}=\begin{bmatrix}\phi_1&\phi_2\\1&0\end{bmatrix}\begin{bmatrix}y_{t-1}\\y_{t-2}\end{bmatrix}+\begin{bmatrix}w_t\\0\end{bmatrix}$, a first-order vector system $\mathbf y_t=F\mathbf y_{t-1}+\mathbf w_t$, so $\partial y_{t+j}/\partial w_t=(F^j)_{11}$. The same idea underlies state-space models ([[06 - The Kalman Filter and State-Space Models]]) and VARs ([[07 - SARIMA and Vector Autoregression]]).

For AR($p$), $\xi_t=(Y_t,\dots,Y_{t-p+1})'$, $\xi_t=F\xi_{t-1}+V_t$ with
$$F=\begin{bmatrix}\phi_1&\phi_2&\cdots&\phi_p\\1&0&\cdots&0\\&\ddots&&\vdots\\0&\cdots&1&0\end{bmatrix},\quad V_t=(W_t,0,\dots,0)'.$$
Then $\xi_t=F^{t+1}\xi_{-1}+F^tV_0+\dots+V_t$ and $\partial Y_{t+j}/\partial W_t=f^{(j)}_{11}$.

**Proposition 1.1**: the eigenvalues of $F$ are the roots of $\lambda^p-\phi_1\lambda^{p-1}-\dots-\phi_p=0$.

With distinct eigenvalues, $F=T\Lambda T^{-1}$, $F^j=T\Lambda^jT^{-1}$, and
$$\psi_j=c_1\lambda_1^j+\dots+c_p\lambda_p^j,\qquad\sum c_i=1\ (\psi_0=1).$$
**Proposition 1.2**: $c_i=\lambda_i^{p-1}/\prod_{k\ne i}(\lambda_i-\lambda_k)$. For AR(1), $c_1=1$ and $\psi_j=\phi^j$. Each root is a dynamic mode; the process is stable iff all $|\lambda_i|<1$, and one root outside is enough to make it explosive.

### AR(2): real and complex roots

$\lambda^2-\phi_1\lambda-\phi_2=0$ gives $\lambda_{1,2}=\frac{\phi_1\pm\sqrt{\phi_1^2+4\phi_2}}2$.

| Object | Equation | Stable when |
|---|---|---|
| characteristic roots $z$ | $1-\phi_1z-\phi_2z^2=0$ | $\lvert z\rvert>1$ (outside the unit circle) |
| inverse roots $\lambda=1/z$ (eigenvalues of $F$) | $\lambda^2-\phi_1\lambda-\phi_2=0$ | $\lvert\lambda\rvert<1$ (inside) |

Same condition, two conventions; check which polynomial is meant. (statsmodels' `arroots` are the $z$.)

**Real roots** ($\phi_1^2+4\phi_2>0$): with all $|\lambda_i|<1$, adjustment is monotone (an alternating component if a root is negative).

**Complex roots** ($\phi_1^2+4\phi_2<0$, which needs $\phi_2<0$): $\lambda=a\pm bi=Re^{\pm i\theta}$, with $R=\sqrt{-\phi_2}$ and $\cos\theta=\phi_1/(2R)$. The weights $c,\bar c$ are conjugates too. With $c=u+iv$ and De Moivre, $\lambda^j=R^j(\cos j\theta+i\sin j\theta)$, the imaginary parts of $c\lambda^j+\bar c\bar\lambda^j$ cancel:
$$\psi_j=2R^j\big[u\cos j\theta-v\sin j\theta\big]=R^j\big[A\cos j\theta+B\sin j\theta\big].$$
A sine wave with envelope $R^j$ and period $T=2\pi/\theta$: damped if $R<1$, persistent if $R=1$, explosive if $R>1$. This is how linear models produce cycles (output gaps, exchange rates overshooting); real roots give only monotone adjustment, so cycles need at least an AR(2). Conversely $\phi_1=2R\cos\theta$, $\phi_2=-R^2$; the lecture plots θ = π/6 (period 12) with R ∈ {0.9, 1.0, 1.1}.

**Stability triangle**: the AR(2) is stable iff
$$\phi_2<1+\phi_1,\qquad\phi_2<1-\phi_1,\qquad-1<\phi_2<1,$$
a triangle with vertices (−2,−1), (2,−1), (0,1). Inside it, the parabola $\phi_2=-\phi_1^2/4$ separates real roots (above) from complex roots (below).

### Lag-polynomial route

Factor $1-\phi_1L-\phi_2L^2=(1-\lambda_1L)(1-\lambda_2L)$ with $\phi_1=\lambda_1+\lambda_2$, $\phi_2=-\lambda_1\lambda_2$. If $|\lambda_1|,|\lambda_2|<1$, partial fractions give
$$Y_t=\frac1{\lambda_1-\lambda_2}\Big[\frac{\lambda_1}{1-\lambda_1L}-\frac{\lambda_2}{1-\lambda_2L}\Big]W_t=\sum_j\big(c_1\lambda_1^j+c_2\lambda_2^j\big)W_{t-j},$$
$c_1=\frac{\lambda_1}{\lambda_1-\lambda_2}$, $c_2=-\frac{\lambda_2}{\lambda_1-\lambda_2}$, the same as Proposition 1.2. Special cases: distinct real roots $c_1\lambda_1^j+c_2\lambda_2^j$; a repeated root $\psi_j=(j+1)\lambda^j$ (from $(1-\lambda L)^{-2}$; it rises before it falls); a complex pair $R^j(A\cos j\theta+B\sin j\theta)$.

### In practice: the recursion

The multipliers satisfy the model's own difference equation: $\psi_0=1$, $\psi_j=\phi_1\psi_{j-1}+\dots+\phi_p\psi_{j-p}$ with $\psi_k=0$ for $k<0$. Equivalently, simulate with $w_0=1$, all later shocks 0, from zero initial values.

```python
def ar_irf(phis, horizon=36):
    psi = np.zeros(horizon)
    for j in range(horizon):
        psi[j] = (j == 0) + sum(phis[k] * psi[j-k-1] for k in range(len(phis)) if j-k-1 >= 0)
    return psi
```
Stability ⇔ convergent multipliers. These scalar IRFs lead to the VAR IRFs of [[07 - SARIMA and Vector Autoregression]] and [[10 - Structural Vector Autoregression]].

## ✏️ Exercises

Exercises 1–3 and 5 are the lecture's problem set (no solutions were provided); Exercise 4 fills in invertibility, which the slides ask about but don't define.

**1.** With $\varepsilon_t\sim WN(0,1)$, which are stable? (1) $y_t=0.5y_{t-1}+\varepsilon_t$; (2) $y_t=2.5y_{t-1}+\varepsilon_t$; (3) $y_t=\varepsilon_t+0.5\varepsilon_{t-1}-0.6\varepsilon_{t-2}$; (4) $y_t=10+0.7y_{t-1}-0.2y_{t-2}+\varepsilon_t$; (5) $y_t=0.5y_{t-1}-0.8y_{t-2}+\varepsilon_t$.

> [!example]- Solution
> (1) λ = 0.5: stable; long-run effect 2.
> (2) λ = 2.5: explosive.
> (3) A finite MA is always stationary (for MAs the question is invertibility, Exercise 4).
> (4) $\phi_1^2+4\phi_2=-0.31$: complex roots $0.35\pm0.2784i$, $R=\sqrt{0.2}=0.4472$: stable, heavily damped. θ = 0.6719 rad, period 9.35. Triangle: −0.2 < 0.3, −0.2 < 1.7, |−0.2| < 1. The intercept moves the mean, $\mu=10/(1-0.7+0.2)=20$, not stability.
> (5) $\phi_1^2+4\phi_2=-2.95$: complex, $R=\sqrt{0.8}=0.8944$: stable but lightly damped. θ = 1.2875 rad, period 4.88.
> For a complex-root AR(2), $R=\sqrt{-\phi_2}$, so stability reduces to $|\phi_2|<1$.

**2.** Give the Wold representation and IRF shape of the stable processes in Exercise 1.

> [!example]- Solution
> (1) $\psi_j=0.5^j$: 1, 0.5, 0.25, 0.125, … smooth decay.
> (3) Already Wold: 1, 0.5, −0.6, then exactly 0. This cut-off is how an ACF reveals an MA's order ([[05 - ACF, PACF and the Box-Jenkins Methodology]]).
> (4) $\psi_j=0.7\psi_{j-1}-0.2\psi_{j-2}$: 1, 0.7, 0.29, 0.063, −0.0139, −0.0223, −0.0129: one shallow dip, gone by about lag 8.
> (5) $\psi_j=0.5\psi_{j-1}-0.8\psi_{j-2}$: 1, 0.5, −0.55, −0.675, 0.1025, 0.5913, 0.2136, −0.3662: clear ~5-period oscillation decaying like $0.894^j$. Same mechanism as (4), very different persistence, set by $|\phi_2|$.

**3.** For (a) $y_t=0.5y_{t-1}+\varepsilon_t$ and (b) $y_t=-0.2y_{t-1}+0.48y_{t-2}+\varepsilon_t$: stationarity, invertibility, mean, variance, $\gamma_j$ and $\rho_j$ for $j=1,2,3$, and the first four MA(∞) coefficients.

> [!example]- Solution
> (a) λ = 0.5 (root $z=2$): stationary. A pure AR has $\theta(L)=1$, so it is trivially invertible. $\mathbb E=0$; $\gamma_0=\sigma^2/(1-\phi^2)=4/3$; $\gamma_j=\phi^j\gamma_0$: 0.6667, 0.3333, 0.1667; $\rho_j$: 0.5, 0.25, 0.125. $\psi_j$: 1, 0.5, 0.25, 0.125.
> (b) $\phi_1^2+4\phi_2=1.96$: real roots 0.6 and −0.8, both inside: stationary; $(1-0.6L)(1+0.8L)$. Invertible (pure AR). Yule–Walker: $\rho_1=\phi_1/(1-\phi_2)=-0.3846$, $\rho_2=\phi_1\rho_1+\phi_2=0.5569$, $\rho_3=\phi_1\rho_2+\phi_2\rho_1=-0.2960$; $\gamma_0=1/(1-\phi_1\rho_1-\phi_2\rho_2)=1.5250$; $\gamma_1=-0.5865$, $\gamma_2=0.8493$, $\gamma_3=-0.4514$. $\psi$: 1, −0.2, 0.52, −0.2 (check: $c_1=0.6/1.4=0.4286$, $c_2=0.5714$, $\psi_2=0.4286(0.36)+0.5714(0.64)=0.52$).
> For an AR(2), $\rho_1\ne\phi_1$: lag 1 also carries the indirect effect through lag 2, which the PACF separates.

**4.** State the invertibility condition for $y_t=\varepsilon_t+\theta\varepsilon_{t-1}$, then check $y_t=\varepsilon_t+0.5\varepsilon_{t-1}-0.6\varepsilon_{t-2}$.

> [!example]- Solution
> Invertible means the MA can be written as a convergent AR(∞), recovering shocks from observed data: $\varepsilon_t=(1+\theta L)^{-1}y_t=y_t-\theta y_{t-1}+\theta^2y_{t-2}-\dots$, which needs $|\theta|<1$. Generally all roots of $\theta(z)=0$ must lie outside the unit circle. Without it the model isn't identified: $\varepsilon_t+2\varepsilon_{t-1}$ with σ² = 1 and $u_t+0.5u_{t-1}$ with σ² = 4 have the same autocovariances; by convention the invertible one is reported.
> $1+0.5z-0.6z^2=0$ has roots 1.7732 and −0.9399; the second is inside, so the process is **not invertible** (inverse roots 0.5639 and −1.0639). Stationary but not invertible: the two properties are independent.

**5.** Simulate $T=50$ with $w_t\sim N(0,1)$. Part 1: AR(1) with φ ∈ {−2.5, −0.8, 0, 0.6, 1}, $y_{-1}=0$; plot paths and $\psi_j$, $j\le10$. Part 2: AR(2) with $y_{-1}=0$, $y_{-2}=-1$, for (i) (0.6, 0.2) and (ii) (−0.6, 2.5).

> [!example]- Solution
> ```python
> rng = np.random.default_rng(42)
> def simulate_ar(phis, T, init, rng):
>     w = rng.standard_normal(T + 1); hist = list(init); y = np.zeros(T + 1)
>     for t in range(T + 1):
>         y[t] = sum(phis[k] * hist[-1 - k] for k in range(len(phis))) + w[t]
>         hist.append(y[t])
>     return y
> ```
> | φ | Verdict | Path and IRF |
> |---|---|---|
> | −2.5 | explosive | alternating blow-up, about $2.5^{50}\approx7.9\times10^{19}$ by $t=50$ (use a log scale) |
> | −0.8 | stationary | jagged, alternating; $\psi_j=(-0.8)^j$ |
> | 0 | white noise | no persistence; $\psi_0=1$, then 0 |
> | 0.6 | stationary | smooth wandering; $\psi_{10}\approx0.006$ |
> | 1 | random walk | no mean reversion, $\operatorname{Var}(y_t)=t\sigma^2$; $\psi_j=1$ |
>
> (i) Roots 0.8385 and −0.2385: stable (0.2 < 0.4 in the triangle); IRF 1, 0.6, 0.56, 0.456, 0.3856, 0.3226: slow monotone decay from the dominant root.
> (ii) $\phi_2=2.5>1$ breaks the triangle; roots 1.3093 and −1.9093: explosive with sign flips; IRF 1, −0.6, 2.86, −3.216, 9.08.
> An IRF's shape identifies the roots: monotone decay (positive real), alternating (negative real), sine wave (complex pair), growth (a root outside).

## 📝 Summary

- Weak stationarity (constant mean and variance, autocovariance depending only on the lag) is what ARMA needs; it equals strict stationarity for Gaussian processes.
- White noise is uncorrelated, not necessarily independent.
- Wold: every stationary process = deterministic part + $\sum\psi_j\varepsilon_{t-j}$.
- The lag operator turns recursions into polynomials; $(1-L)$ differences.
- Multipliers $\psi_j=\partial y_{t+j}/\partial w_t$ are the IRF; AR(1): $\phi^j$, long-run $1/(1-\phi)$.
- Companion matrix: $\psi_j=(F^j)_{11}=\sum c_i\lambda_i^j$; eigenvalues = roots of $\lambda^p-\phi_1\lambda^{p-1}-\dots-\phi_p$.
- Stable ⇔ all $|\lambda_i|<1$ ⇔ all $|z_i|>1$.
- Real roots: monotone; complex roots: damped cycles with $R=\sqrt{-\phi_2}$, period $2\pi/\theta$; AR(2) stability triangle.
- Compute IRFs with the recursion $\psi_j=\sum\phi_i\psi_{j-i}$.

## ⚠️ Important Notes

1. "Roots outside" refers to $z$, "inside" to $\lambda=1/z$.
2. Stationarity concerns the AR polynomial, invertibility the MA polynomial.
3. A finite MA is always stationary; a pure AR is always invertible.
4. $\rho_1=\phi_1$ only for AR(1); for AR(2), $\rho_1=\phi_1/(1-\phi_2)$.
5. AR(2) cheat sheet: triangle conditions; complex iff $\phi_1^2+4\phi_2<0$; $R=\sqrt{-\phi_2}$; mean $\alpha/(1-\phi_1-\phi_2)$; Yule–Walker $\rho_k=\phi_1\rho_{k-1}+\phi_2\rho_{k-2}$.
6. Repeated roots: $\psi_j=(j+1)\lambda^j$; Proposition 1.2 fails there.
7. Three regimes: $|\lambda|<1$ stationary, $|\lambda|=1$ unit root (non-stationary, not explosive), $|\lambda|>1$ explosive.
8. The intercept changes the mean, not stability; the mean blows up as $\sum\phi_i\to1$.

> [!warning] Gaps in the source slides
> - HTML extraction deleted every `<` inside inline maths, cutting conditions such as $|\phi|<1$, $|\lambda_i|<1$, $R<1$ and the triangle inequalities. These were reconstructed (standard results).
> - The stability-triangle figure contradicts its caption: the code shades yellow a region above the slanted edges (outside the triangle, explosive) and colours the whole interior green, while the caption says yellow = real roots, green = complex roots. The real/complex boundary is the parabola $\phi_2=-\phi_1^2/4$. Trust the inequalities.
> - Slides s17/s18 (duplicates) write $\partial y_{t+2}/\sigma_t$ where $\partial w_t$ is meant. Slides s45/46, s56/59, s57/60 are duplicates.
> - Invertibility is asked about but never defined (Exercise 4). No solutions are given; all of the above are derived and checked numerically.
> - No outputs saved; figures were reconstructed from the plotting code. The final cell is a broken `nbconvert` command.

**Previous:** [[02 - Trend, Seasonality and Decomposition]] · **Next:** [[04 - AR, MA and ARMA Processes]]
