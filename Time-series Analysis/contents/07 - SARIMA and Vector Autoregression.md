---
subject: Time-series Analysis
chapter: 07
tags: [ds, time-series, sarima, var, irf, granger-causality, cholesky, fevd]
source: "documents/slides/Lecture07_DSEB_SARIMA_VAR.ipynb (Lecture 7 — Seasonal ARIMA and Vector Autoregression, Dr. Thi Ha Tran); Hamilton, *Time Series Analysis*, Ch. 10–11"
---

# SARIMA and Vector Autoregression

Two extensions of ARIMA: **SARIMA** adds dynamics at a seasonal frequency (one variable); **VAR** adds several variables, each depending on the lags of all. VARs bring impulse responses, Granger causality and variance decomposition, and the identification problem of [[10 - Structural Vector Autoregression]]. $I(1)$ variables go to [[08 - VECM and Cointegration]].

## 📘 Main Knowledge

### SARIMA

$$\phi(L)\,\Phi(L^s)\,(1-L)^d(1-L^s)^DX_t=\theta(L)\,\Theta(L^s)\,\varepsilon_t,$$
with non-seasonal AR $\phi(L)=1-\phi_1L-\dots-\phi_pL^p$, seasonal AR $\Phi(L^s)=1-\Phi_1L^s-\dots-\Phi_PL^{Ps}$, non-seasonal MA $\theta(L)=1+\theta_1L+\dots$, seasonal MA $\Theta(L^s)=1+\Theta_1L^s+\dots$. Written SARIMA$(p,d,q)\times(P,D,Q)_s$: lower case non-seasonal, upper case seasonal; $s$ = 4 (quarterly), 12 (monthly), 7 (daily, weekly cycle), 52 (weekly).

| Operator | Role |
|---|---|
| $(1-L)^d$ | removes the trend |
| $(1-L^s)^D$ | removes the seasonal component |
| $\Phi_P(L^s)$ | seasonal AR persistence (this January depends on last January) |
| $\Theta_Q(L^s)$ | seasonal structure in the noise |

Seasonality can be in $Y_t$ or in the shocks; seasonal shocks aren't white noise and need SAR/SMA terms, so a seasonal difference alone may not suffice. $(1-L^{12})Y_t=Y_t-Y_{t-12}$ is the year-on-year change (not $(1-L)^{12}$).

**SARIMA(1,1,1)×(1,1,1)$_s$**: $(1-\phi L)(1-\Phi L^s)(1-L)(1-L^s)X_t=(1+\theta L)(1+\Theta L^s)Z_t$. Differencing: $X_t-X_{t-1}-X_{t-s}+X_{t-s-1}$. Expanded:
$$\begin{aligned}X_t=\;&X_{t-1}+X_{t-s}-X_{t-s-1}+\phi(X_{t-2}+X_{t-s-1}-X_{t-s-2})+\Phi(X_{t-s-1}+X_{t-2s}-X_{t-2s-1})\\&-\phi\Phi(X_{t-s-2}+X_{t-2s-1}-X_{t-2s-2})+Z_t+\theta Z_{t-1}+\Theta Z_{t-s}+\theta\Theta Z_{t-s-1}.\end{aligned}$$
Regular lags $t-1,t-2$; seasonal $t-s,t-2s$; cross lags $t-s-1$, $t-s-2$, $t-2s-1$. With $s=12$ it reaches lag 26 with four parameters: the cross coefficients are products ($\theta\Theta$), not free parameters. This multiplicative restriction is what makes it estimable.

**ARIMA(1,1,1)×(2,2,2)$_4$** (lecture): $(1-L)(1-L^4)^2=1-L-2L^4+2L^5+L^8-L^9$, so $Y_t=X_t-X_{t-1}-2X_{t-4}+2X_{t-5}+X_{t-8}-X_{t-9}$. AR: $(1-\phi_1L)(1-\Phi_1L^4-\Phi_2L^8)=1-\phi_1L-\Phi_1L^4-\Phi_2L^8+\phi_1\Phi_1L^5+\phi_1\Phi_2L^9$. MA: $1+\theta_1L+\Theta_1L^4+\Theta_2L^8+\theta_1\Theta_1L^5+\theta_1\Theta_2L^9$. So
$$Y_t=\phi_1Y_{t-1}+\Phi_1Y_{t-4}+\Phi_2Y_{t-8}-\phi_1\Phi_1Y_{t-5}-\phi_1\Phi_2Y_{t-9}+\varepsilon_t+\theta_1\varepsilon_{t-1}+\Theta_1\varepsilon_{t-4}+\Theta_2\varepsilon_{t-8}+\theta_1\Theta_1\varepsilon_{t-5}+\theta_1\Theta_2\varepsilon_{t-9}.$$
AR cross terms flip sign when moved across; MA cross terms keep $+$. Six parameters.

**Identifying seasonal orders** (read ACF/PACF at lags $s,2s,\dots$ as well; standard practice, not on the slides):

| At seasonal lags | Suggests |
|---|---|
| ACF spike at $s$ only | SMA(1), $Q=1$ |
| ACF decaying over $s,2s,3s$ | SAR, $P\ge1$ |
| PACF spike at $s$ only | SAR(1) |
| seasonal ACF near 1, not decaying | seasonal difference, $D=1$ |

$D$ is rarely above 1, $P$ and $Q$ rarely above 1–2. The "airline model" SARIMA(0,1,1)×(0,1,1)$_{12}$ fits many monthly series with two parameters.

**Quarterly GDP application** (lecture):
```python
y = df.set_index("Quaterly")["GDP"]
adfuller(y.dropna()); adfuller(y.diff().dropna()); adfuller(y.diff().diff().dropna())
y_diff = y.diff().diff(4).dropna()      # (1-L)(1-L^4) y; diff(4) is the seasonal difference
auto_arima(y, seasonal=True, m=4, max_p=4, max_q=4, max_P=2, max_Q=2, trace=True)
```
Selected (AIC 1838.244): SARIMA(1,1,1)×(1,1,1)$_4$ with φ = 0.4705 (depends on the last quarter), θ = −0.9886 (short-term shocks corrected next quarter), Φ = 0.9581 (strong annual persistence), Θ = −0.4809 (same-quarter shocks partly reversed). Ljung–Box p = 0.46 (adequate); Jarque–Bera p = 0.00 (fat tails).

Caveats: θ ≈ −1 cancels against $(1-L)$, a sign of over-differencing (try $d=0$ with a trend); Φ ≈ 1 on top of a seasonal difference suggests $D=1$ may be unnecessary or seasonal dummies would do. Non-normal residuals leave point estimates consistent but make intervals too narrow (bootstrap them; fat tails also motivate [[09 - ARCH, GARCH and Extensions|GARCH]]).

### The VAR model

For an $n$-vector of endogenous variables:
$$Y_t=a_0+A_1Y_{t-1}+\dots+A_pY_{t-p}+u_t\iff\Phi(L)Y_t=a_0+u_t,\quad\Phi(L)=I_n-A_1L-\dots-A_pL^p,$$
$\mathbb E(u_t)=0$, $\mathbb E(u_tu_t')=\Omega$, $\mathbb E(u_tu_s')=0$ for $t\ne s$. $\Omega$ is symmetric positive definite; off-diagonal $\sigma_{ij}$ are contemporaneous correlations across equations (errors are uncorrelated over time, not across equations).

Parameters: $pn^2$ in the $A_i$, $n$ in $a_0$, $n(n+1)/2$ in Ω. $pn^2$ grows fast (n = 2, p = 2: 8; n = 3, p = 4: 36; n = 5, p = 4: 100; n = 8, p = 4: 256), which is why applied VARs rarely exceed 4–6 variables and why Bayesian VARs shrink coefficients.

A VAR is one system: each variable responds to lags of all, errors correlate through Ω, and IRFs, Granger causality and joint forecasts follow. To save parameters: **incomplete VARs** (zero restrictions, e.g. $y_2$ never affecting $y_1$: 6 instead of 8 parameters in a bivariate VAR(2)) or **linear restrictions** ($a^{(1)}_{11}=a^{(2)}_{11}$, $a^{(1)}_{12}+a^{(2)}_{12}=0$, …).

The VAR imposes no doubtful a priori restrictions (Sims 1980), but with unrestricted Ω it has no causal reading: reduced-form shocks are mixtures of structural shocks. Causal analysis needs orthogonal shocks, $u_t=P\varepsilon_t$ with $\mathbb E(\varepsilon_t\varepsilon_t')=I$: recursive (Cholesky) or theory-based (SVAR).

### Stability

$Y_t$ is covariance stationary iff all roots of $\det(I_n-A_1z-\dots-A_pz^p)=0$ (a scalar polynomial of degree $np$) lie outside the unit circle. A root on the circle means a unit root; if the variables are $I(1)$, use a VECM. In companion form, a VAR(2) is a VAR(1) in $X_t=(Y_t',Y_{t-1}')'$ with $F=\begin{pmatrix}A_1&A_2\\I&0\end{pmatrix}$; stable ⇔ all eigenvalues of $F$ inside the unit circle (= 1: unit root; > 1: explosive).

**Lecture example**: $A_1=\begin{bmatrix}0.727002&45.224458\\0.000049&0.983537\end{bmatrix}$. $\det(I-A_1z)=1-1.710539z+0.712817z^2$, roots 1.0082 and 1.3915: stable, but 1.0082 is within 1% of a unit root (consider a VECM), and the very different coefficient sizes suggest rescaling the variables.

### Estimation

With $X_t=(1,Y'_{t-1},\dots,Y'_{t-p})'$ and $B=[c,A_1,\dots,A_p]$ ($m\times(1+mp)$), stacking the $T=n-p$ usable periods gives $Y=XB'+E$ and
$$\hat B'=(X'X)^{-1}X'Y,\qquad\hat\Omega=\frac{\hat E'\hat E}{T-(1+mp)}.$$
Every equation has the same regressors, so system GLS (SUR) reduces to OLS equation by equation: consistent and efficient. MLE gives the same $\hat B$; its covariance divides by $T$.

Layout example (lecture): $Y_1,\dots,Y_5=(1,0),(2,1),(3,1),(4,2),(5,3)$ with $p=2$: $Y$ has rows (3,1), (4,2), (5,3); $X$ rows (1, 2,1, 1,0), (1, 3,1, 2,1), (1, 4,2, 3,1). Three observations for five parameters per equation: for layout only. The lecture's VAR(2) on 15 observations gives $\hat\Omega=\begin{bmatrix}1.8864&-0.4716\\-0.4716&1.6236\end{bmatrix}$ (error correlation −0.27), also illustrative.

**Lag length**: too few lags leave autocorrelated residuals; too many waste degrees of freedom. With $k=m^2p+m$:
$$\text{AIC}=\ln\det\Sigma_{E(p)}+\frac{2k}T,\quad\text{BIC}=\ln\det\Sigma_{E(p)}+\frac{k\ln T}T,\quad\text{HQ}=\ln\det\Sigma_{E(p)}+\frac{2k\ln\ln T}T.$$
AIC picks the largest $p$, BIC the smallest, HQ in between; BIC is often preferred for parsimony, AIC for forecasting. **LR test**: $\mathrm{LR}(p)=T[\ln\det\Sigma_{E(p-1)}-\ln\det\Sigma_{E(p)}]\sim\chi^2(m^2)$ under "lag $p$ not needed".

### Granger causality

$Y_j$ **Granger-causes** $Y_i$ if past $Y_j$ helps predict $Y_i$ given the other variables. Test $H_0$: all lags of $Y_j$ are zero in the $Y_i$ equation (other variables stay: conditional causality) with χ², F or Wald statistics; a block test drops all other variables. It measures predictive content, not economic causation (Christmas card sales "Granger-cause" Christmas).

### Impulse responses and Cholesky

For a stable VAR, $Y_t=\mu+\sum_j\Psi_j\varepsilon_{t-j}$ with $\Psi_0=I$, $\Psi_j=A_1\Psi_{j-1}+\dots+A_p\Psi_{j-p}$, and $\partial Y_{i,t+h}/\partial\varepsilon_{j,t}=(\Psi_h)_{ij}$. Because reduced-form shocks are correlated, "move $\varepsilon_j$ alone" isn't meaningful.

**Cholesky**: $\Sigma_\varepsilon=LL'$ with $L$ lower triangular; $u_t=L^{-1}\varepsilon_t$ has $\operatorname{Cov}(u_t)=L^{-1}LL'(L^{-1})'=I$. Orthogonalized IRFs $\Phi_s=\Psi_sL$. For 2×2: $\ell_{11}=\sigma_1$, $\ell_{21}=\sigma_{12}/\sigma_1$, $\ell_{22}=\sqrt{\sigma_2^2-\sigma_{12}^2/\sigma_1^2}$. Lower-triangular $L$ means the first variable doesn't respond within the period to the second shock: the ordering is an identifying assumption. A recursive VAR uses Cholesky; a structural VAR uses theory ([[10 - Structural Vector Autoregression]]).

**FEVD**: the $h$-step error is $\Phi_0u_{t+h}+\dots+\Phi_{h-1}u_{t+1}$, $\mathrm{MSE}=\sum_{s<h}\Phi_s\Phi_s'$, and
$$\mathrm{FEVD}_{ij}(h)=\frac{\sum_{s<h}(\Phi_s)_{ij}^2}{\sum_k\sum_{s<h}(\Phi_s)_{ik}^2},$$
each row summing to 100%.

**Example 7.1** (lecture): $A=\begin{pmatrix}0.5&0.1\\0.2&0.4\end{pmatrix}$, $\Sigma_\varepsilon=\begin{pmatrix}4&2\\2&3\end{pmatrix}$. $\Psi_h=A^h$; $L=\begin{pmatrix}2&0\\1&\sqrt2\end{pmatrix}$; $\Phi_0=L$; $\Phi_1=AL=\begin{pmatrix}1.10&0.141\\0.80&0.566\end{pmatrix}$. Shock 1 moves $y_1$ by 2 and $y_2$ by 1 on impact, then decays. Shock 2 moves $y_2$ by 1.414 and $y_1$ by 0 on impact by construction, 0.141 after one period. FEVD of $y_1$ at $h=2$: shock 1 $4+1.21=5.21$, shock 2 $0.02$; 99.62% vs 0.38%. At short horizons this mostly restates the ordering.

### Workflow

1. Objective (interactions, policy, forecasting). 2. Variables, all $I(0)$. 3. Lag length (AIC/BIC/HQ, LR). 4. OLS estimation; check stability and residuals. 5. IRFs, FEVD, Granger causality. 6. Forecasts and their accuracy. If variables are $I(1)$ and cointegrated: VECM; $I(1)$ and not cointegrated: VAR in differences.

**Applied example** (lecture): `INDVN` (economic activity) and `Interest_rate`. ADF −2.68 (p = 0.078) and −3.37 (p = 0.012); both treated as $I(0)$, VAR in levels; BIC selects VAR(1). Cholesky IRFs: an income shock raises income temporarily; an interest-rate shock affects income with a lag, small then peaking then fading (via investment and demand); an income shock slightly raises rates (tightening). Shocks are mostly temporary. Note that p = 0.078 doesn't reject a unit root at 5%; with the 1.0082 root, a KPSS check and a VECM are worth considering.

```python
from statsmodels.tsa.api import VAR
model = VAR(data)
p = model.select_order(maxlags=12).selected_orders["bic"]
res = model.fit(p)
print(all(abs(r) > 1 for r in res.roots))      # statsmodels gives roots z: stable if |z| > 1
res.irf(24).plot(orth=True)
res.fevd(10).summary()
res.test_causality(caused="INDVN", causing=["Interest_rate"], kind="f")
```

## ✏️ Exercises

**1.** Expand the airline model SARIMA(0,1,1)×(0,1,1)$_{12}$. Which shock lags appear, and how many parameters?

> [!example]- Solution
> $(1-L)(1-L^{12})=1-L-L^{12}+L^{13}$: $W_t=(X_t-X_{t-1})-(X_{t-12}-X_{t-13})$, this month's change minus the same change a year earlier. $(1+\theta L)(1+\Theta L^{12})$: $W_t=\varepsilon_t+\theta\varepsilon_{t-1}+\Theta\varepsilon_{t-12}+\theta\Theta\varepsilon_{t-13}$. Lags 0, 1, 12, 13; two parameters plus σ². An unrestricted MA(13) would need 13. The ACF of $W_t$ is non-zero only at lags 1, 11, 12, 13 (the "shoulders" at 11 and 13).

**2.** Monthly retail sales ($n=144$), differenced once. ACF of $\Delta Y_t$: −0.42 at lag 1, near 0 at 2–11, 0.68 at 12, 0.51 at 24, 0.39 at 36. PACF: spikes at 1 and 12. Model, and next steps?

> [!example]- Solution
> Seasonal ACF decays geometrically (ratios 0.75, 0.76) with a single PACF spike at 12: seasonal AR(1). All exceed the band ±0.167, and 0.68 is large, so try a seasonal difference first; if the seasonal ACF then shows a single negative spike at 12, you have over-differenced (go back to $P=1$, $D=0$). The lone negative lag-1 spike suggests $q=1$. Candidates: (0,1,1)×(1,1,0)$_{12}$, (0,1,1)×(0,1,1)$_{12}$, (0,1,1)×(1,0,0)$_{12}$. Compare AIC only with equal $d$, $D$; Ljung–Box up to lag 24 (two seasons); watch for θ or Θ near −1; check out-of-sample RMSE on the last 12–24 months.

**3.** Redo Example 7.1 with $y_2$ ordered first. Compare $\mathrm{FEVD}_{1\cdot}(2)$.

> [!example]- Solution
> Reordered covariance $\begin{pmatrix}3&2\\2&4\end{pmatrix}$, Cholesky $\begin{pmatrix}1.7321&0\\1.1547&1.6330\end{pmatrix}$; in the original labels the impact matrix is upper triangular, $\begin{pmatrix}1.6330&1.1547\\0&1.7321\end{pmatrix}$ (check: times its transpose gives Σ). $\Phi_1=\begin{pmatrix}0.8165&0.7506\\0.3266&0.9238\end{pmatrix}$.
> $y_1$ at $h=2$: shock 1 $2.667+0.667=3.333$, shock 2 $1.333+0.563=1.897$; total 5.230 (unchanged). FEVD 63.7% / 36.3%, against 99.6% / 0.4%. Same data, different assumption. Invariant: total MSE and the non-orthogonalized $\Psi_h=A^h$. The cause is the error correlation $2/\sqrt{12}=0.577$; with diagonal Σ ordering wouldn't matter. Always report robustness to ordering.

**4.** Bivariate VAR(2), 100 usable observations. The $y_1$ equation has $SSR_{UR}=42.5$ (5 parameters); dropping both lags of $y_2$ gives $SSR_R=47.8$. Does $y_2$ Granger-cause $y_1$?

> [!example]- Solution
> $F=\frac{(47.8-42.5)/2}{42.5/95}=5.92>F_{0.05}(2,95)=3.09$, $p=0.004$: reject; $y_2$ Granger-causes $y_1$ (Wald: $2F=11.85>5.99$). The restricted SSR is 12.5% higher. Not proof of economic causation: a common driver with different lags, anticipation (asset prices), or temporal aggregation could produce it. The reverse test uses the $y_2$ equation; outcomes can be one-way, two-way (feedback) or none, and "none" still allows contemporaneous correlation through Ω.

**5.** Three-variable VAR, $n=120$ quarters; $\ln\det\Sigma_E$ = −2.410, −2.598, −2.641, −2.679 for $p=1..4$. Choose $p$.

> [!example]- Solution
> $k=9p+3$, $T=120-p$.
>
> | $p$ | AIC | BIC | HQ |
> |---|---|---|---|
> | 1 | −2.208 | **−1.928** | **−2.095** |
> | 2 | **−2.242** | −1.749 | −2.042 |
> | 3 | −2.128 | −1.420 | −1.841 |
> | 4 | −2.007 | −1.081 | −1.631 |
>
> LR vs $\chi^2_{0.05}(9)=16.92$: 2 vs 1: 22.18, reject; 3 vs 2: 5.03; 4 vs 3: 4.41. AIC and LR choose 2, BIC and HQ choose 1. I'd take $p=2$: the LR test rejects $p=1$, the 1→2 gain (0.188) is four times the 2→3 gain, and one quarterly lag is implausibly short. Then check residual autocorrelation, stability, and whether IRFs differ between the two. Underfitting is the more dangerous error.

## 📝 Summary

- SARIMA multiplies regular and seasonal polynomials; cross-lag coefficients are products, which keeps it parsimonious.
- Read ACF/PACF at seasonal lags; Ljung–Box past two seasons.
- VAR: each variable on lags of all; errors correlated across equations; $pn^2$ parameters.
- Stable iff roots of $\det(I-A_1z-\dots)$ lie outside the unit circle; $I(1)$ → VECM.
- OLS equation by equation is efficient (same regressors).
- Lags by AIC/BIC/HQ or LR ($\chi^2(m^2)$).
- Granger causality = predictive content.
- Orthogonalized IRFs $\Phi_s=\Psi_sL$; Cholesky ordering is an assumption; FEVD splits forecast variance by shock.

## ⚠️ Important Notes

1. The Cholesky zero is imposed, not found (99.6% vs 63.7% in Exercise 3).
2. VAR variables must be $I(0)$; levels VARs on $I(1)$ data are spurious unless handled as a VECM.
3. statsmodels' `roots` are $z$: stable means $|z|>1$.
4. `.diff(4)` is the seasonal difference, not four differences.
5. Granger causality can come from anticipation, omitted variables or aggregation.
6. Aim for about 10 observations per parameter per equation: $T\ge10(1+np)$.
7. Short-horizon FEVD mostly reflects the ordering.

> [!warning] Gaps in the source slides
> - All data files (`GDP_week1.xlsx`, the 15-observation dataset, the INDVN/interest-rate file) are missing and no outputs were saved, so the applied results can't be reproduced. Example 7.1 and the VAR(1) stability determinant were checked independently and are correct.
> - How to read seasonal ACF/PACF lags isn't covered (the table above is standard practice), nor are seasonal unit-root tests (HEGY, OCSB, Canova–Hansen; pmdarima uses OCSB).
> - Typos: the error vector written $(u_{1t},\nu_{2t},\dots)'$; "sindicates" for "indicates".
> - Inline `<` signs were lost (stability conditions); reconstructed.
> - FEVD is shown only at $h=2$ for one variable. Several code comments are in Vietnamese.

**Previous:** [[06 - The Kalman Filter and State-Space Models]] · **Next:** [[08 - VECM and Cointegration]]
