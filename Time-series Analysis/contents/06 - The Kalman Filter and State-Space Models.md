---
subject: Time-series Analysis
chapter: 06
tags: [ds, time-series, kalman-filter, state-space, mle, latent-variables]
source: "documents/slides/Lecture6_KalmanFilter.ipynb (Lecture 6 — Kalman Filter, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 13"
---

# The Kalman Filter and State-Space Models

[[05 - ACF, PACF and the Box-Jenkins Methodology]] said "estimate by MLE"; the Kalman filter is how the likelihood of ARMA models is computed. State-space form is also the general frame for SARIMA, VAR and structural models.

## 📘 Main Knowledge

### Why the Kalman filter

It (1) estimates latent states from noisy or partial observations (inflation trend, output gap, a satellite's position); (2) gives optimal one-step forecasts in linear-Gaussian models; (3) computes the log-likelihood for MLE of ARMA, SARIMAX or linearized DSGE models; (4) handles missing data and multivariate systems. Workflow: predict → update → likelihood. The filter alternates between predicting with the model and correcting with the data, weighting each by its uncertainty.

### State-space form

$$\text{state: }\xi_{t+1}=F\xi_t+v_{t+1},\qquad\text{observation: }y_t=A'x_t+H'\xi_t+w_t,$$
with state $\xi_t$ ($r\times1$, possibly unobserved), transition $F$ ($r\times r$), observations $y_t$ ($n\times1$), exogenous or predetermined $x_t$ ($k\times1$), $A'$ ($n\times k$), $H'$ ($n\times r$). The state equation says how the world evolves; the observation equation how it is seen.

Assumptions: $\mathbb E(v_tv_\tau')=Q$ and $\mathbb E(w_tw_\tau')=R$ at $t=\tau$, zero otherwise; $\mathbb E(v_tw_\tau')=0$ for all $t,\tau$; $x_t$ carries no information about future shocks beyond past $y$. Iterating, $\xi_t=v_t+Fv_{t-1}+\dots+F^{t-2}v_2+F^{t-1}\xi_1$.

### ARMA models in state-space form

**AR(p)**: state $\xi_t=(y_t-\mu,\dots,y_{t-p+1}-\mu)'$, $F$ = the companion matrix ([[03 - Stationarity and Difference Equations]]), $v_{t+1}=(\varepsilon_{t+1},0,\dots,0)'$, $y_t=\mu+[1\ 0\cdots0]\xi_t$, $R=0$, $Q$ with σ² in position (1,1) only. An AR(p) is a first-order Markov system in $p$ dimensions.

**MA(1), representation A**: the shocks are the hidden state, $\xi_t=(\varepsilon_t,\varepsilon_{t-1})'$:
$$\xi_t=\begin{bmatrix}0&0\\1&0\end{bmatrix}\xi_{t-1}+\begin{bmatrix}\varepsilon_t\\0\end{bmatrix},\qquad y_t=\mu+[1\ \ \theta]\xi_t,\qquad Q=\begin{bmatrix}\sigma^2&0\\0&0\end{bmatrix},\ R=0.$$
This is how a model with unobserved regressors is estimated: infer them as a state.

**MA(1), representation B**: $\tilde\xi_t=(\varepsilon_t+\theta\varepsilon_{t-1},\ \theta\varepsilon_t)'$, $\tilde F=\begin{bmatrix}0&1\\0&0\end{bmatrix}$, $\tilde v_{t+1}=(\varepsilon_{t+1},\theta\varepsilon_{t+1})'$, $y_t=\mu+[1\ 0]\tilde\xi_t$ (Hamilton 13.1.19–20). Both give identical forecasts and likelihoods: representations aren't unique, so states aren't identified, and a singular $Q$ is fine.

### The recursions

$\hat\xi_{t\mid s}$ is the estimate of $\xi_t$ given data to $s$, $P_{t\mid s}$ its error covariance; $t\mid t-1$ is the prior, $t\mid t$ the posterior.

1. **Predict**: $\hat\xi_{t\mid t-1}=F\hat\xi_{t-1\mid t-1}$, $P_{t\mid t-1}=FP_{t-1\mid t-1}F'+Q$. Uncertainty is propagated and grows.
2. **Innovation**: $\hat y_{t\mid t-1}=A'x_t+H'\hat\xi_{t\mid t-1}$, $v_t=y_t-\hat y_{t\mid t-1}$, $S_t=H'P_{t\mid t-1}H+R$ (state uncertainty plus measurement noise).
3. **Update**: $K_t=P_{t\mid t-1}HS_t^{-1}$, $\hat\xi_{t\mid t}=\hat\xi_{t\mid t-1}+K_tv_t$, $P_{t\mid t}=(I-K_tH')P_{t\mid t-1}$. Uncertainty shrinks.
4. **Forecast**: $\hat\xi_{t+1\mid t}=F\hat\xi_{t\mid t}$, $P_{t+1\mid t}=FP_{t\mid t}F'+Q$, $\hat y_{t+1\mid t}=A'x_{t+1}+H'\hat\xi_{t+1\mid t}$, with forecast MSE $S_{t+1}=H'P_{t+1\mid t}H+R$.

$K_t$ minimizes the posterior MSE, so the filter is the best linear estimator (best overall under Gaussian noise). Large state uncertainty → large gain → trust the data; large measurement noise → small gain → trust the model. It is recursive Bayesian updating: prior $N(\hat\xi_{t\mid t-1},P_{t\mid t-1})$, posterior $N(\hat\xi_{t\mid t},P_{t\mid t})$.

**Missing data**: if $y_t$ is missing, skip the update ($\hat\xi_{t\mid t}=\hat\xi_{t\mid t-1}$, $P_{t\mid t}=P_{t\mid t-1}$); uncertainty grows and the recursion continues.

### Example: the MA(1)

With representation A, $P_{t\mid t-1}=\operatorname{diag}(\sigma^2,p_t)$, where σ² is the uncertainty about the new shock and $p_t$ the remaining uncertainty about the previous one. Then
$$S_t=\sigma^2+\theta^2p_t,\qquad K_t=\frac1{\sigma^2+\theta^2p_t}\begin{bmatrix}\sigma^2\\\theta p_t\end{bmatrix},\qquad v_t=y_t-\mu-\hat\varepsilon_{t\mid t-1}-\theta\hat\varepsilon_{t-1\mid t-1},$$
$$\hat\varepsilon_{t\mid t}=\hat\varepsilon_{t\mid t-1}+\frac{\sigma^2}{S_t}v_t,\qquad\hat\varepsilon_{t-1\mid t}=\hat\varepsilon_{t-1\mid t-1}+\frac{\theta p_t}{S_t}v_t.$$
The surprise is split between the new and the previous shock, and the estimate of a past shock is revised. If $p_t=0$, $S_t=\sigma^2$.

**Numbers** (lecture): μ = 2, θ = 0.5, σ² = 1; start $\hat\xi_{1\mid0}=0$, $P_{1\mid0}=I$ (simple initialization for illustration); observe $y_1=3$. $\hat y_{1\mid0}=2$, $v_1=1$, $S_1=1+0.25=1.25$, $K_1=(0.8,0.4)'$, $\hat\xi_{1\mid1}=(0.8,0.4)'$: only 0.8 of the surprise goes to $\varepsilon_1$, and the pre-sample shock is revised to 0.4. Then $\hat\xi_{2\mid1}=F\hat\xi_{1\mid1}=(0,0.8)'$ and $\hat y_{2\mid1}=2+0.5(0.8)=2.4$.

### Maximum likelihood

Dependent data use the prediction-error decomposition:
$$f(y_1,\dots,y_T)=f(y_1)\prod_{t\ge2}f(y_t\mid y_{t-1},\dots,y_1).$$
With $y_t\mid Y_{t-1}\sim N(\hat y_{t\mid t-1},S_t)$,
$$\ell=-\frac12\sum_{t=1}^T\Big(\log2\pi+\log S_t+\frac{v_t^2}{S_t}\Big)$$
(multivariate: $\log|S_t|$ and $v_t'S_t^{-1}v_t$). For given parameters the filter produces $v_t$ and $S_t$, which is all the likelihood needs. The filter evaluates the likelihood; an outer optimizer (BFGS; L-BFGS, the default in most packages; Nelder–Mead for irregular surfaces) proposes new parameters, often over hundreds of filter passes.

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
y = np.array([1.0, 0.2, -0.1, 0.6, 0.3, -0.2, 0.4, 0.1])
res = SARIMAX(y, order=(0, 0, 1), trend="c",
              enforce_invertibility=True, enforce_stationarity=True).fit(disp=False)
res.params, res.llf
res.filter_results.filtered_state       # ξ̂_{t|t}
res.filter_results.predicted_state      # ξ̂_{t|t-1}
res.filter_results.forecasts_error      # v_t
res.filter_results.forecasts_error_cov  # S_t
```

The notebook's hard-coded $v_t$ and $S_t$ reproduce the likelihood: $\ell_t=-\frac12(\log2\pi+\log S_t+v_t^2/S_t)$, summed. $S_t$ falls from 0.1388 to 0.0781: the filter is learning about the pre-sample shocks. In a time-invariant model $P_{t\mid t-1}$ converges to the solution of a discrete algebraic Riccati equation, the gain becomes constant, and the filter becomes the fixed-gain recursion $\hat\varepsilon_t=(y_t-\mu)-\theta\hat\varepsilon_{t-1}$ of ch. 04. The difference is a start-up effect: exact vs conditional MLE.

## ✏️ Exercises

The deck has no exercises; these are constructed.

**1.** Put $y_t=0.6y_{t-1}-0.2y_{t-2}+\varepsilon_t+0.4\varepsilon_{t-1}$ (σ² = 1) in state-space form.

> [!example]- Solution
> Dimension $r=\max(p,q+1)=2$. Harvey form: $F=\begin{bmatrix}0.6&1\\-0.2&0\end{bmatrix}$, $v_t=(1,0.4)'\varepsilon_t$, so $Q=\begin{bmatrix}1&0.4\\0.4&0.16\end{bmatrix}$ (rank 1); $H'=[1\ 0]$, $R=0$.
> Check: $\xi_{1t}=0.6\xi_{1,t-1}+\xi_{2,t-1}+\varepsilon_t$ and $\xi_{2t}=-0.2\xi_{1,t-1}+0.4\varepsilon_t$; substituting the lagged second equation gives $y_t=0.6y_{t-1}-0.2y_{t-2}+\varepsilon_t+0.4\varepsilon_{t-1}$ (also confirmed by simulation). Stacking lags and shocks separately ($r=3$) also works.

**2.** Continue the MA(1) example: observe $y_2=1.5$. Find $P_{1\mid1}$, $P_{2\mid1}$, $S_2$, $K_2$, $\hat\xi_{2\mid2}$, $\hat y_{3\mid2}$.

> [!example]- Solution
> $P_{1\mid1}=(I-K_1H')P_{1\mid0}=\begin{bmatrix}0.2&-0.4\\-0.4&0.8\end{bmatrix}$: the variance of $\varepsilon_1$'s estimate fell from 1 to 0.2; the negative covariance says a larger $\varepsilon_1$ means a smaller $\varepsilon_0$.
> $P_{2\mid1}=FP_{1\mid1}F'+Q=\operatorname{diag}(1,0.2)$, so $p_2=0.2$.
> $v_2=1.5-2.4=-0.9$; $S_2=1+0.25(0.2)=1.05$ (down from 1.25).
> $K_2=(1,0.1)'/1.05=(0.9524,0.0952)'$; $\hat\xi_{2\mid2}=(0,0.8)'+K_2(-0.9)=(-0.8571,0.7143)'$: $\hat\varepsilon_1$ revised from 0.8 to 0.714.
> $\hat\xi_{3\mid2}=(0,-0.8571)'$, $\hat y_{3\mid2}=2-0.4286=1.571$.
> The gain on the new shock rose (0.80 → 0.95) and on the old fell (0.40 → 0.095). The fixed-gain recursion from $\hat\varepsilon_1=0.8$ would give $\hat\varepsilon_2=-0.5-0.4=-0.9$; the filter gives −0.857 because it is still unsure about $\varepsilon_1$. The gap closes as $p_t\to0$.

**3.** Local level model: $\mu_{t+1}=\mu_t+\eta_t$, $y_t=\mu_t+\varepsilon_t$. (a) $F,H',Q,R$? (b) Show the steady-state gain depends only on $q=\sigma^2_\eta/\sigma^2_\varepsilon$. (c) Limits as $q\to0$ and $q\to\infty$?

> [!example]- Solution
> (a) $F=H'=1$, $Q=\sigma^2_\eta$, $R=\sigma^2_\varepsilon$.
> (b) $K_t=P_t/(P_t+\sigma^2_\varepsilon)$ and $P_{t+1}=\frac{P_t\sigma^2_\varepsilon}{P_t+\sigma^2_\varepsilon}+\sigma^2_\eta$. In steady state (Riccati) $\bar P^2-\sigma^2_\eta\bar P-\sigma^2_\eta\sigma^2_\varepsilon=0$. With $\bar p=\bar P/\sigma^2_\varepsilon$: $\bar p=\frac{q+\sqrt{q^2+4q}}2$ and $\bar K=\bar p/(\bar p+1)$, a function of the signal-to-noise ratio only.
> (c) $q\to0$: $\bar K\to0$, average all history. $q\to\infty$: $\bar K\to1$, use the latest observation. The steady-state filter $\hat\mu_{t\mid t}=\bar Ky_t+(1-\bar K)\hat\mu_{t-1\mid t-1}$ is simple exponential smoothing with $\alpha=\bar K$ ([[02 - Trend, Seasonality and Decomposition]]); adding a slope state gives Holt, seasonal states Holt–Winters.

**4.** Rebuild the log-likelihood from the notebook's $v_t$ and $S_t$. Why does $S_t$ fall, and why is the first term the largest penalty?

> [!example]- Solution
> | $t$ | $v_t$ | $S_t$ | $\ell_t$ |
> |---|---|---|---|
> | 1 | 0.7517 | 0.1388 | −1.9665 |
> | 2 | 0.3275 | 0.1041 | −0.3029 |
> | 3 | −0.1300 | 0.0926 | 0.1797 |
> | 4 | 0.2542 | 0.0868 | −0.0690 |
> | 5 | 0.2550 | 0.0833 | −0.0666 |
> | 6 | −0.2358 | 0.0810 | −0.0055 |
> | 7 | −0.0505 | 0.0793 | 0.3320 |
> | 8 | −0.1925 | 0.0781 | 0.1188 |
>
> Total $\ell=-1.780$. $S_t=\sigma^2+\theta^2p_t$ falls (44% here) as uncertainty about the previous shock shrinks. At $t=1$ the filter knows nothing, so both $\log S_1$ and $v_1^2/S_1=4.07$ are largest. Exact MLE includes this start-up properly; conditional MLE fixes or drops it. With $T=8$ that matters a lot; with $T=500$ hardly at all. Positive $\ell_t$ values are fine: densities can exceed 1 when $S_t<1$.

**5.** OLS and MLE agree for an AR(1). When is the Kalman filter really needed?

> [!example]- Solution
> (1) MA terms: the lagged shocks are never observed; the filter infers them and handles initialization exactly instead of setting $\hat\varepsilon_0=0$. (2) Unobserved components (output gap, natural rate, trend/cycle): no data column exists. (3) Missing, irregular or mixed-frequency data: skip updates instead of dropping rows or interpolating; quarterly GDP as a monthly series with gaps is the basis of nowcasting. Also time-varying coefficients in the state ($\beta_{t+1}=\beta_t+\eta_t$), dynamic factor models, and automatic forecast variances. For a pure AR with complete data, OLS is conditional MLE and is fine.

## 📝 Summary

- State equation (dynamics) + observation equation (measurement), with covariances $Q$ and $R$ and no cross-correlation.
- ARMA in state-space form: AR uses the companion matrix; MA(1) has the shocks as state; representations aren't unique.
- Predict → innovate → gain → update; the gain weights data against model by precision.
- MA(1): $S_t=\sigma^2+\theta^2p_t$; the filter revises past shock estimates.
- Likelihood from the prediction-error decomposition: $-\frac12\sum(\log2\pi+\log S_t+v_t^2/S_t)$; an outer optimizer maximizes it.
- Missing data: skip the update.
- Steady-state local-level filter = exponential smoothing.

## ⚠️ Important Notes

1. Notation on the slides collides: the state disturbance is $u$, $v$ or $w$ on different slides, $w_t$ is also measurement error, and $v_t$ is also the innovation; $S_t$ and $K_t$ mix $H$ and $H'$. Check dimensions: $F$ $r\times r$, $H'$ $n\times r$, $Q$ $r\times r$, $R$ $n\times n$, $K_t$ $r\times n$, $S_t$ $n\times n$.
2. Filtered states have no meaning unless the representation was chosen to make them meaningful.
3. Initialization is a choice: stationary models use the unconditional mean and variance ($P=FPF'+Q$); non-stationary states need a diffuse prior. $P_{1\mid0}=I$ is for illustration only.
4. A singular $Q$ is normal; $S_t$ must be invertible.
5. Filtering ($\hat\xi_{t\mid t}$), smoothing ($\hat\xi_{t\mid T}$, using all data; for historical latent series) and prediction ($\hat\xi_{t+h\mid t}$) answer different questions.
6. The same filter runs GPS, Apollo navigation, robot SLAM and sensor fusion; non-linear variants are the extended/unscented Kalman and particle filters.

> [!warning] Gaps in the source slides
> - The Kalman smoother isn't covered, though it is the right tool for retrospective latent series (statsmodels: `res.smoothed_state`).
> - Initialization, the steady state and the Riccati equation aren't discussed (the links to exponential smoothing and to exact vs conditional MLE are added above).
> - The `pykalman` cell is cut off mid-argument, and `pykalman` is unmaintained; use `statsmodels.tsa.statespace`.
> - The SARIMAX output wasn't saved; the hard-coded $v_t$, $S_t$ were used as given. Some comments are in Vietnamese. No exercises are provided.

**Previous:** [[05 - ACF, PACF and the Box-Jenkins Methodology]] · **Next:** [[07 - SARIMA and Vector Autoregression]]
