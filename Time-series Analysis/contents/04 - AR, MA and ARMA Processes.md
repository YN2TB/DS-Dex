---
subject: Time-series Analysis
chapter: 04
tags: [ds, time-series, arma, yule-walker, forecasting, random-walk]
source: "documents/slides/Lecture_4_Timeseries_DSEB.ipynb (Lecture 4 — Time Series Models: AR, MA and ARMA Processes, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 3–4"
---

# AR, MA and ARMA Processes

[[03 - Stationarity and Difference Equations]] showed when a linear system is stable and how shocks propagate. This chapter derives the moments of AR, MA and ARMA models and how to forecast with them; [[05 - ACF, PACF and the Box-Jenkins Methodology]] covers choosing the model and its orders from data.

## 📘 Main Knowledge

### The random walk

$y_t=y_{t-1}+\varepsilon_t$ with $\varepsilon_t\sim WN(0,\sigma^2)$ and $y_0$ given, so $y_t=y_0+\sum_{j=1}^t\varepsilon_j$: a running sum of all shocks.

- $\mathbb E[y_t]=y_0$.
- $\operatorname{Var}(y_t)=t\sigma^2$: grows with $t$, so non-stationary.
- $\operatorname{Cov}(y_t,y_{t-k})=(t-k)\sigma^2$ (only the shared shocks count): depends on $t$ too.
- $\rho_k(t)=\frac{(t-k)\sigma^2}{\sqrt{t\sigma^2(t-k)\sigma^2}}=\sqrt{(t-k)/t}\to1$. The sample ACF decays slowly and linearly, the signature of a unit root.

Each shock enters with coefficient 1 and stays forever ($\psi_j=1$): **shocks are permanent**. Economically: is a recession a temporary deviation or a permanent loss of output?

**With drift**, $y_t=c+y_{t-1}+\varepsilon_t$ gives $y_t=y_0+tc+\sum_j\varepsilon_j$: a deterministic trend (up if $c>0$, down if $c<0$) plus a stochastic trend; the mean $y_0+tc$ trends too. The standard model for log prices, log GDP, log exchange rates.

| | Trend-stationary | Difference-stationary (unit root) |
|---|---|---|
| model | $y_t=a+bt+u_t$, $u_t$ stationary | $y_t=c+y_{t-1}+\varepsilon_t$ |
| remove trend by | regressing on $t$ | differencing: $\Delta y_t=c+\varepsilon_t$ |
| deviations | temporary | permanent |

Regressing a unit-root series on $t$ leaves autocorrelated residuals; differencing a trend-stationary series over-differences, putting an MA unit root ($\theta=-1$) into the errors.

### Autoregressive processes

**AR(1)**, $y_t=\phi y_{t-1}+\varepsilon_t$, $|\phi|<1$, with $\gamma_k=\operatorname{Cov}(y_t,y_{t-k})$:
- Mean: $\mathbb E y=\phi\mathbb Ey$, so 0.
- Variance: $\gamma_0=\phi^2\gamma_0+\sigma^2$ (the cross term vanishes because $\varepsilon_t$ is uncorrelated with the past), so $\gamma_0=\sigma^2/(1-\phi^2)>\sigma^2$.
- Multiply by $y_{t-k}$: $\gamma_k=\phi\gamma_{k-1}$ (Yule–Walker), so $\gamma_k=\phi^k\gamma_0$ and $\rho_k=\phi^k$. The ACF decays geometrically (alternating if φ < 0) and never cuts off.

**AR(1) with constant**, $Y_t=\alpha+\phi Y_{t-1}+u_t$: explosive if $|\phi|>1$, random walk with drift if $|\phi|=1$, mean-reverting if $|\phi|<1$. Solving from $Y_0$:
$$Y_t=\phi^tY_0+\alpha(1+\phi+\dots+\phi^{t-1})+\phi^{t-1}\varepsilon_1+\dots+\varepsilon_t,$$
$\mathbb E(Y_t)=\phi^tY_0+\alpha\frac{1-\phi^t}{1-\phi}\to\frac\alpha{1-\phi}$ and $\operatorname{Var}(Y_t)=\sigma^2(1+\phi^2+\dots+\phi^{2(t-1)})\to\frac{\sigma^2}{1-\phi^2}$: the initial value is forgotten. With $\mu=\alpha/(1-\phi)$, $Y_t-\mu=\phi(Y_{t-1}-\mu)+\varepsilon_t$; the constant moves the level, not the dynamics, so centre first.

**AR(2)**, $Y_t=\mu+\phi_1Y_{t-1}+\phi_2Y_{t-2}+u_t$ (here μ is the **intercept**; the slides use μ for both intercept and mean, and $\phi_0$ on one slide). Stationary iff the roots of $1-\phi_1z-\phi_2z^2=0$ lie outside the unit circle (inverse roots inside; the stability triangle).
- Mean: $\mathbb E(Y)=\mu/(1-\phi_1-\phi_2)$.
- Yule–Walker: $\gamma_k=\phi_1\gamma_{k-1}+\phi_2\gamma_{k-2}$, so the ACF follows the process's own difference equation (complex roots give an oscillating ACF). $\rho_1=\phi_1/(1-\phi_2)$, $\rho_2=\phi_1\rho_1+\phi_2$.
- Variance: at $k=0$ an extra $\sigma^2$ appears because $\mathbb E[\varepsilon_t(Y_t-\mu)]=\sigma^2$: $\gamma_0=\phi_1\gamma_1+\phi_2\gamma_2+\sigma^2$, giving
$$\gamma_0=\frac{(1-\phi_2)\sigma^2}{(1+\phi_2)[(1-\phi_2)^2-\phi_1^2]}.$$

**AR(p)**: mean $\mu/(1-\sum\phi_i)$; Yule–Walker $\gamma_j=\sum_i\phi_i\gamma_{j-i}$ for $j\ge1$ and $\gamma_0=\sum_i\phi_i\gamma_i+\sigma^2$. In matrix form $\vec\gamma=\Gamma\vec\phi$ and $\gamma_0=\vec\phi'\vec\gamma+\sigma^2$, with $\Gamma$ the symmetric Toeplitz matrix of $\gamma_0,\dots,\gamma_{p-1}$. Solving $\vec\phi=\Gamma^{-1}\vec\gamma$ is the Yule–Walker estimator and the basis of the PACF; Toeplitz structure allows the $O(p^2)$ Levinson–Durbin algorithm. For $p\ge3$, $\gamma_0$ has no simple closed form; the ACF mixes one exponential or oscillating term per root.

**Lecture example, AR(3)**: $y_t=\frac12y_{t-1}+\frac15y_{t-2}+\frac1{10}y_{t-3}+u_t$, σ² = 1. Solving the four Yule–Walker equations exactly: $\gamma_0=925/434=2.1313$, $\gamma_1=325/217=1.4977$, $\gamma_2=575/434=1.3249$, $\gamma_3=255/217=1.1751$; $\rho_1=26/37=0.7027$, $\rho_2=23/37=0.6216$, $\rho_3=102/185=0.5514$. The slide's values are correct.

### Moving average processes

**MA(1)**, $Y_t=\mu+\varepsilon_t+\theta\varepsilon_{t-1}$: $\mathbb E=\mu$, $\operatorname{Var}=\sigma^2(1+\theta^2)$, $\gamma_1=\theta\sigma^2$ (one shared shock), $\gamma_k=0$ for $k>1$; $\rho_1=\theta/(1+\theta^2)$. Stationary for every θ. $|\rho_1|\le0.5$ (maximum at θ = ±1), so a lag-1 autocorrelation above 0.5 rules out an MA(1); θ and 1/θ give the same $\rho_1$.

**MA(q)**, $Y_t=\mu+\theta(L)\varepsilon_t$, $\theta(L)=1+\theta_1L+\dots+\theta_qL^q$, $\theta_0=1$:
$$\operatorname{Var}=(1+\textstyle\sum\theta_i^2)\sigma^2,\qquad\gamma_k=\sigma^2\sum_{j=0}^{q-k}\theta_j\theta_{j+k}\ (k\le q),\quad\gamma_k=0\ (k>q).$$
The ACF **cuts off** after lag $q$ (an AR's tails off). Stationary for any θ.

**MA(∞)**, $Y_t=\mu+\psi(L)\varepsilon_t$: $\gamma_k=\sigma^2\sum_j\psi_j\psi_{j+k}$, stationary iff $\sum\psi_j^2<\infty$ (the Wold form; a stationary AR has square-summable $\psi_j$).

**Invertibility**: the shocks can be recovered from observed history, $\varepsilon_t=\theta(L)^{-1}(Y_t-\mu)$, i.e. an AR(∞) form. Condition: all roots of $1+\theta_1z+\dots+\theta_qz^q=0$ outside the unit circle.

| | Polynomial | Property | Condition | Gives |
|---|---|---|---|---|
| AR | $\phi(z)$ | stationarity | $\lvert z\rvert>1$ | MA(∞) form |
| MA | $\theta(z)$ | invertibility | $\lvert z\rvert>1$ | AR(∞) form |

Without invertibility the model isn't identified (θ and 1/θ, with rescaled σ², have identical ACFs); by convention the invertible version is used, and it is the one that can be forecast.

**Lecture example, MA(2)**: $Y_t=(1-\frac56L+\frac16L^2)\varepsilon_t$, σ² = 1. Stationary (finite MA). $\gamma_0=1+\frac{25}{36}+\frac1{36}=\frac{31}{18}=1.7222$; $\gamma_1=\theta_1+\theta_1\theta_2=-\frac{35}{36}$; $\gamma_2=\frac16$; $\gamma_3=0$. $1-\frac56z+\frac16z^2=0\iff z^2-5z+6=0$: roots 2 and 3, invertible. (The slide prints $31/19$ and roots −2, −3; see gaps.)

### ARMA(p, q)

$$Y_t=\phi_0+\sum_{i=1}^p\phi_iY_{t-i}+\varepsilon_t+\sum_{j=1}^q\theta_j\varepsilon_{t-j}\quad\iff\quad\phi(L)Y_t=\phi_0+\theta(L)\varepsilon_t.$$
Stationarity depends only on $\phi(L)$, invertibility only on $\theta(L)$. MA(∞) form: $Y_t=\mu+\Psi(L)\varepsilon_t$ with $\Psi=\theta/\phi$, computed by factoring φ, partial fractions and geometric series, or by the recursion $\psi_j=\sum_i\phi_i\psi_{j-i}+\theta_j$. ARMA's appeal is parsimony: an ARMA(1,1) may replace an AR(8) or MA(12), and fewer parameters forecast better.

**Lecture example, ARMA(2,1)**: $Y_t=1+0.3Y_{t-1}-0.02Y_{t-2}+\varepsilon_t+0.2\varepsilon_{t-1}$. Operator form $(1-0.3L+0.02L^2)Y_t=1+(1+0.2L)\varepsilon_t$. $1-0.3z+0.02z^2=0\iff z^2-15z+50=0$: roots 5 and 10, stationary; $\phi(L)=(1-0.2L)(1-0.1L)$. Partial fractions: $\phi(L)^{-1}=\frac2{1-0.2L}-\frac1{1-0.1L}=1+0.3L+0.07L^2+0.015L^3+\dots$; times $(1+0.2L)$: ψ = 1, 0.5, 0.13, 0.029. Mean $1/0.72=1.3889$.

### Forecasting

**Optimal forecast.** Under squared loss,
$$\mathbb E[Y_{t+1}-g(X_t)]^2=\mathbb E[Y_{t+1}-\mathbb E(Y_{t+1}\mid X_t)]^2+\mathbb E[\mathbb E(Y_{t+1}\mid X_t)-g(X_t)]^2,$$
so the conditional expectation $\mathbb E(Y_{t+1}\mid X_t)$ is optimal; the first term is irreducible.

**Wiener–Kolmogorov.** With $Y_t-\mu=\psi(L)\varepsilon_t$, split $Y_{t+s}$ into future shocks ($\varepsilon_{t+s},\dots,\varepsilon_{t+1}$) and known past ones, and replace the future ones by 0:
$$\hat Y_{t+s\mid t}=\mu+\psi_s\varepsilon_t+\psi_{s+1}\varepsilon_{t-1}+\dots=\mu+\Big[\frac{\psi(L)}{L^s}\Big]_+\varepsilon_t,$$
where $[\cdot]_+$ deletes negative powers of $L$. The error is the discarded future block, so
$$\mathrm{MSE}(s)=(1+\psi_1^2+\dots+\psi_{s-1}^2)\sigma^2,$$
rising in $s$ towards $\operatorname{Var}(Y_t)$. With invertibility, forecasts can be written in observed $Y$'s.

- **AR(1)**: $[\frac{\psi(L)}{L^s}]_+=\frac{\phi^s}{1-\phi L}$, and with $\varepsilon_t=(1-\phi L)(Y_t-\mu)$: $\hat Y_{t+s\mid t}=\mu+\phi^s(Y_t-\mu)$; $\mathrm{MSE}(s)=\sigma^2(1+\phi^2+\dots+\phi^{2(s-1)})\to\sigma^2/(1-\phi^2)$.
- **AR(p)**: $\hat Y_{t+s\mid t}=\mu+\sum_jf^{(s)}_{1j}(Y_{t-j+1}-\mu)$, $f^{(s)}=(F^s)$; in practice iterate $\hat Y_{t+j\mid t}-\mu=\sum_i\phi_i(\hat Y_{t+j-i\mid t}-\mu)$, using actual values where known ($\hat Y_{\tau\mid t}=Y_\tau$ for τ ≤ t).
- **MA(1)**: $\hat Y_{t+1\mid t}=\mu+\theta\hat\varepsilon_t$ with $\hat\varepsilon_t=(Y_t-\mu)-\theta\hat\varepsilon_{t-1}$ (equivalently $\mu+\theta(Y_t-\mu)-\theta^2(Y_{t-1}-\mu)+\dots$, convergent only if invertible); $\hat Y_{t+s\mid t}=\mu$ for $s\ge2$. **MA(q)**: forecasts equal μ beyond $q$ steps.
- **ARMA(1,1)**: $\hat Y_{t+s\mid t}=\mu+\frac{\phi^s+\theta\phi^{s-1}}{1+\theta L}(Y_t-\mu)$; one step: $\hat Y_{t+1\mid t}-\mu=\phi(Y_t-\mu)+\theta\hat\varepsilon_t$, $\hat\varepsilon_t=Y_t-\hat Y_{t\mid t-1}$ (the structure the Kalman filter generalizes).
- **ARMA(p,q)**: $\hat Y_{t+s\mid t}-\mu=\sum_i\phi_i(\hat Y_{t+s-i\mid t}-\mu)+\sum_{j=s}^q\theta_j\hat\varepsilon_{t+s-j}$ for $s\le q$; beyond $q$ the MA terms drop out and the forecast follows the AR recursion, so the AR roots set the speed of reversion to μ.

## ✏️ Exercises

Exercises 1–2 are the lecture's (without provided solutions).

**1.** (Exercise 3.1) $Y_t=(1+2.4L+0.8L^2)\varepsilon_t$, σ² = 1. (a) Stationary? (b) $\gamma_0,\gamma_1,\gamma_2$. (c) Invertible?

> [!example]- Solution
> (a) Yes: a finite MA is stationary for any coefficients.
> (b) $\gamma_0=1+5.76+0.64=7.40$; $\gamma_1=2.4+2.4(0.8)=4.32$; $\gamma_2=0.8$; $\gamma_k=0$ for $k\ge3$. $\rho_1=0.584$, $\rho_2=0.108$.
> (c) $1+2.4z+0.8z^2=0$ gives $z=-0.5,-2.5$; $|-0.5|<1$, so **not invertible**. $\theta(L)=(1+2L)(1+0.4L)$; flipping $2\to0.5$ gives the invertible twin $1+0.9L+0.2L^2$ with σ² = 4: $\gamma_0=4(1.85)=7.40$, $\gamma_1=4(1.08)=4.32$, $\gamma_2=0.8$. Same moments, different parameters; software reports the twin.

**2.** (Exercise 3.2) $(1-1.1L+0.18L^2)Y_t=\varepsilon_t$, σ² = 1. (a) Stationary? (b) $\gamma_0,\gamma_1,\gamma_2$. (c) The recursion for $\gamma_k$.

> [!example]- Solution
> $\phi_1=1.1$, $\phi_2=-0.18$ (the polynomial has minus signs).
> (a) $1-1.1z+0.18z^2=0$: $z=5$ and $1.111$, both outside; inverse roots 0.2 and 0.9; $(1-0.2L)(1-0.9L)$. Real roots, monotone. Triangle: −0.18 < −0.1 ✓.
> (b) $\rho_1=1.1/1.18=0.9322$; $\rho_2=1.1(0.9322)-0.18=0.8454$; $\gamma_0=\frac{1.18}{0.82(1.3924-1.21)}=\frac{36875}{4674}=7.8894$; $\gamma_1=7.3545$; $\gamma_2=6.6699$. Check: $1.1(7.3545)-0.18(6.6699)+1=7.8894$. The 0.9 root amplifies the variance almost eightfold.
> (c) $\gamma_k=1.1\gamma_{k-1}-0.18\gamma_{k-2}$ ($\gamma_{-1}=\gamma_1$): $\gamma_3=6.0131$, $\rho_3=0.7622$. The 0.9 root dominates, so the ACF looks like an AR(1) with φ = 0.9.

**3.** Random walk vs AR(1) with φ = 0.95, same N(0,1) shocks, T = 200, $y_0=0$. (a) Variances? (b) When does the random walk's variance exceed the AR(1)'s? (c) How would you tell them apart from one realization?

> [!example]- Solution
> (a) Random walk: $\operatorname{Var}=t$. AR(1): $\to1/(1-0.9025)=10.26$.
> (b) From $t=11$; by $t=200$ about 20 times larger.
> (c) Plots: both wander over short samples. ACF: random walk $\sqrt{(t-k)/t}$ is 0.975 at lag 10 for $t=200$; AR(1) $0.95^k$ is 0.60 at lag 10, 0.36 at lag 20; noisy in finite samples. Difference: white noise for the random walk, a negative lag-1 spike (over-differencing) for the AR(1). Formally ADF/KPSS ([[05 - ACF, PACF and the Box-Jenkins Methodology]]), whose power against φ = 0.95 with T = 200 is low.

**4.** $Y_t=2+0.6Y_{t-1}+\varepsilon_t+0.4\varepsilon_{t-1}$, σ² = 1. Given $Y_t=7$ and $\hat\varepsilon_t=0.5$, forecast $s=1,2,3$ with 95% intervals.

> [!example]- Solution
> $\mu=2/0.4=5$. $\hat Y_{t+1}=5+0.6(2)+0.4(0.5)=6.4$; beyond $q=1$ the AR recursion applies: $\hat Y_{t+2}=5+0.6(1.4)=5.84$, $\hat Y_{t+3}=5+0.6(0.84)=5.504$.
> $\psi_0=1$, $\psi_1=\phi+\theta=1$, $\psi_2=0.6$, $\psi_j=0.6\psi_{j-1}$.
>
> | $s$ | Forecast | MSE | SE | 95% interval |
> |---|---|---|---|---|
> | 1 | 6.400 | 1 | 1.000 | [4.44, 8.36] |
> | 2 | 5.840 | 2 | 1.414 | [3.07, 8.61] |
> | 3 | 5.504 | 2.36 | 1.536 | [2.49, 8.51] |
>
> The forecast reverts to 5 at rate 0.6 while the interval widens towards $\pm1.96\sqrt{\gamma_0}$, $\gamma_0=(1+2\phi\theta+\theta^2)/(1-\phi^2)=2.5625$.

**5.** For the lecture's ARMA(2,1), find $\psi_j$ in closed form and check it against the recursion.

> [!example]- Solution
> With $a_j=2(0.2)^j-(0.1)^j$ (from $\phi(L)^{-1}$), $\psi_j=a_j+0.2a_{j-1}=4(0.2)^j-3(0.1)^j$ for $j\ge1$, $\psi_0=1$.
>
> | $j$ | Closed form | Recursion $0.3\psi_{j-1}-0.02\psi_{j-2}+\theta_j$ |
> |---|---|---|
> | 1 | 0.8 − 0.3 = 0.5 | 0.3 + 0.2 = 0.5 |
> | 2 | 0.16 − 0.03 = 0.13 | 0.15 − 0.02 = 0.13 |
> | 3 | 0.032 − 0.003 = 0.029 | 0.039 − 0.01 = 0.029 |
>
> The recursion (polynomial long division) is what you'd code. The ψ decay at rate 0.2: short memory; $\operatorname{Var}=\sigma^2\sum\psi_j^2=1.268$.

## 📝 Summary

- Random walk: mean $y_0$, variance $t\sigma^2$, $\rho_k(t)=\sqrt{(t-k)/t}\to1$, permanent shocks; with drift the mean trends too.
- Trend-stationary series are detrended by regression, unit-root series by differencing.
- AR(1): $\gamma_0=\sigma^2/(1-\phi^2)$, $\rho_k=\phi^k$, geometric ACF; centre on μ.
- AR(2): $\rho_1=\phi_1/(1-\phi_2)$, $\rho_2=\phi_1\rho_1+\phi_2$, the ACF follows the process's difference equation.
- AR(p): Yule–Walker $\vec\gamma=\Gamma\vec\phi$ with Toeplitz Γ.
- MA(q): $\gamma_k=\sigma^2\sum\theta_j\theta_{j+k}$, zero beyond $q$; always stationary.
- Invertibility (MA roots outside) gives AR(∞) and identifies the model.
- ARMA: $\Psi=\theta/\phi$; parsimonious.
- Optimal forecast = conditional mean; $\hat Y_{t+s}=\mu+[\psi(L)/L^s]_+\varepsilon_t$; MSE grows to the variance; AR(1) reverts at rate φ; MA(q) reverts to μ after $q$ steps.

## ⚠️ Important Notes

1. $\phi(L)=1-\phi_1L-\dots$ but $\theta(L)=1+\theta_1L+\dots$: $(1-1.1L+0.18L^2)$ means $\phi_2=-0.18$. Some software uses $1-\theta_1L$ for MA; check before reading estimates.
2. The intercept is not the mean: $\mathbb E Y=\mu/(1-\sum\phi_i)$; statsmodels' `const` with `trend='c'` is the mean.
3. ACF/PACF patterns: AR(p) ACF tails off, PACF cuts off at $p$; MA(q) ACF cuts off at $q$, PACF tails off; ARMA both tail off; a random walk's ACF stays near 1.
4. $\mathbb E[\varepsilon_t(Y_t-\mu)]=\sigma^2$, which is why the $k=0$ Yule–Walker equation has the extra σ².
5. Over-differencing creates a non-invertible MA root; look for a negative lag-1 spike.
6. Long-horizon ARMA forecasts are flat at μ with interval $\mu\pm1.96\sqrt{\gamma_0}$; anything else implies a unit root or trend.

> [!warning] Gaps in the source slides
> - Errata (MA(2) example): $\gamma_0$ printed as $31/19$, correct $31/18$; the characteristic equation printed as $1+\frac56z+\frac16z^2$ with roots −2, −3, correct $1-\frac56z+\frac16z^2$ with roots 2, 3 (invertibility conclusion unchanged).
> - Unit-root tests (ADF, PP, KPSS) are never presented, despite the emphasis on random walks.
> - $\rho_k(t)=\sqrt{(t-k)/t}$ is stated without derivation (derived above).
> - HTML extraction deleted inline `<` signs (stationarity conditions, square-summability, the ARMA(1,1) forecasting preamble); slides 25–26 survived only as titles. Reconstructed from context.
> - Duplicates: s14–16/s17–18, s45/47, s50/51. No outputs saved; Exercises 3.1–3.2 have no solutions. Some code comments are in Vietnamese.

**Previous:** [[03 - Stationarity and Difference Equations]] · **Next:** [[05 - ACF, PACF and the Box-Jenkins Methodology]]
