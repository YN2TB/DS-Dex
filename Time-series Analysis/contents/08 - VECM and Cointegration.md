---
subject: Time-series Analysis
chapter: 08
tags: [ds, time-series, vecm, cointegration, johansen, error-correction]
source: "documents/slides/lecture08_VECM_DSEB.ipynb and VECM_lecture_slides.ipynb (Lecture 8 — Vector Error Correction Model, Dr. Thi Ha Tran); Johansen (1988, 1991)"
---

# VECM and Cointegration

[[07 - SARIMA and Vector Autoregression]] required $I(0)$ variables. When variables are $I(1)$ but move together in the long run, a VAR in levels is spurious and a VAR in differences discards the long-run relation; the VECM keeps both. The idea: $I(1)$ variables can have a stationary linear combination, which is the long-run equilibrium, and deviations from it drive the short-run dynamics.

Two notebooks cover this lecture: `lecture08_VECM_DSEB.ipynb` (57 cells: derivation, Johansen algebra, applied results) and `VECM_lecture_slides.ipynb` (16 cells: overview with VECM IRFs and the model-choice rule). Both are used.

## 📘 Main Knowledge

### Error correction

For a long-run relation $Y_t=\beta_0+\beta_1X_t+\varepsilon_t$ between $I(1)$ variables, differencing gives $\Delta Y_t=\beta_1\Delta X_t+v_t$ with $v_t=\varepsilon_t-\varepsilon_{t-1}$: serially correlated (an MA unit root), short-run effects only, and nothing to enforce the equilibrium $Y^*_t=\beta_0+\beta_1X_{t-1}$ when $Y$ is above or below it.

**Error correction model**:
$$\Delta Y_t=\alpha_1\Delta X_t+\gamma\,EC_{t-1}+\varepsilon_t,\qquad EC_{t-1}=Y_{t-1}-\beta_0-\beta_1X_{t-1},$$
with $\alpha_1$ the short-run effect and γ the speed of adjustment. Expect $\gamma<0$: if $EC_{t-1}>0$, $Y$ is too high and falls; if $EC_{t-1}<0$ it rises. Short-run dynamics and long-run equilibrium in one equation.

### Cointegration

$m$ variables $Y_i\sim I(1)$ are **cointegrated** if some $\beta'Y_t\sim I(0)$: each wanders, but a particular combination doesn't (two random walkers joined by a leash). Examples: short and long interest rates, consumption and income, spot and futures prices.

Following Johansen (1988): β has at least two non-zero elements; scale is irrelevant ($a\beta'Y_t$ is also stationary); there can be $r$ independent cointegrating vectors, $0<r\le m-1$. The columns of the $m\times r$ matrix β are the long-run relations; there are $m-r$ common stochastic trends.

### From VAR to VECM

From a VAR(p), subtract $Y_{t-1}$ and add and subtract partial sums of the $A_i$:
$$\Delta Y_t=\Pi Y_{t-1}+\sum_{i=1}^{p-1}\Gamma_i\Delta Y_{t-i}+\varepsilon_t,\qquad\Pi=\sum_{i=1}^pA_i-I,\qquad\Gamma_i=-\sum_{j=i+1}^pA_j.$$
Π is the long-run matrix and the $\Gamma_i$ the short-run matrices. Everything is stationary except the level term $Y_{t-1}$, which carries the long-run information a differenced VAR would drop. In lag form, $\Gamma(L)\Delta Y_t=\alpha\beta'Y_{t-1}+\varepsilon_t$. The lecture also states a generalized form with MA errors, $\Gamma(L)\Delta Y_t=\alpha\beta'Y_{t-1}+\Theta(L)\varepsilon_t$.

**The rank of Π decides the model.** With rank $r$, $\Pi=\alpha\beta'$ ($\alpha$, β both $m\times r$):

| Rank | Meaning | Model |
|---|---|---|
| $r=0$ | Π = 0, no cointegration | VAR in differences |
| $0<r<m$ | $r$ relations, $m-r$ stochastic trends | VECM |
| $r=m$ | all variables stationary | VAR in levels |

Since $\Phi(1)=I-\sum A_i=-\Pi$, Π singular ⇔ $z=1$ is a root: the rank counts unit roots ($m-r$).

**Reading the terms.** $\beta'Y_{t-1}=(EC_{1,t-1},\dots,EC_{r,t-1})'$ measures last period's deviations ($EC_j=\sum_i\beta_{ij}y_i$; for two variables $y-\beta x$). α sets each variable's response: with α < 0, a positive deviation pushes the variable down. $|\alpha|$ is the speed: α = −0.3 closes 30% per period, half-life $\ln0.5/\ln0.7=1.9$ periods. Signs depend on how β is normalized; flipping β flips α and leaves Π unchanged. What matters is that α and β together pull back towards equilibrium; in multivariate systems some α entries are positive.

### α and β are not unique

For any non-singular $r\times r$ γ, $\alpha\beta'=(\alpha\gamma)(\gamma^{-1}\beta')$. Only the space spanned by β is identified. Example: $\beta=(1,-1)'$ and $(2,-2)'$ both describe $y_t=x_t$. Software normalizes (e.g. first element 1, as in $\beta=(1,-1.0087)'$), and the choice of variable is arbitrary. With $r\ge2$, individual columns aren't interpretable without economic restrictions.

### Estimation

**Unrestricted OLS** (Park & Phillips 1980; Sims, Stock & Watson 1990): estimating the levels VAR without a rank restriction is consistent; then $\hat\Pi=\sum\hat A_i-I$, $\hat\Gamma_i=-\sum_{j>i}\hat A_j$, find the rank and factor $\hat\Pi$. Drawbacks: many steps, α and β only indirectly, hard inference (a free estimate of Π never has exactly reduced rank). Fine only when the cointegrating relations are known.

**Johansen's reduced-rank regression** (MLE with the rank imposed; Johansen 1991):
1. Auxiliary regressions of $\Delta Y_t$ and of $Y_{t-1}$ on the lagged differences, with residuals $R_{0t}$ ("cleaned changes") and $R_{1t}$ ("cleaned levels"): Frisch–Waugh–Lovell partialling out of the short-run terms.
2. Concentrated model $R_{0t}=\alpha\beta'R_{1t}+\varepsilon_t$. With $S_{ij}=\frac1T\sum_tR_{it}R_{jt}'$,
$$\mathrm{CLF}(\alpha,\beta)=k-\frac T2\ln\big|S_{00}-\alpha\beta'S_{10}-S_{01}\beta\alpha'+\alpha\beta'S_{11}\beta\alpha'\big|,\quad k=-\frac{mT}2\ln2\pi.$$
Normalize $\beta'S_{11}\beta=I_r$ (allowed since only the space is identified).
3. Concentrate out α: $\alpha=S_{01}\beta$, leaving $\mathrm{CLF}(\beta)=k-\frac T2\ln|S_{00}-S_{01}\beta\beta'S_{10}|$.
4. Minimize $|I-\beta'S_{10}S_{00}^{-1}S_{01}\beta|$ subject to the normalization; the first-order condition is the generalized eigenvalue problem
$$\big|\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}\big|=0.$$
The eigenvalues $\hat\lambda_1>\dots>\hat\lambda_m$ are squared canonical correlations between cleaned changes and cleaned levels; near-zero ones mean that direction of the levels doesn't predict changes. The rank is the number of significant eigenvalues.
5. $\hat\beta$ = eigenvectors of the $r$ largest; $\hat\alpha=S_{01}\hat\beta(\hat\beta'S_{11}\hat\beta)^{-1}$; $\hat\Gamma_i=B_i-\hat\alpha\hat\beta'C_i$.

### Johansen tests

Do the usual VAR checks first (lags by AIC/BIC/HQ; autocorrelation by LM or Ljung–Box; ARCH or White for heteroskedasticity; Jarque–Bera).

**Deterministic terms**, five standard cases:

| Case | $\Pi Y_{t-1}$ term |
|---|---|
| 1. no trend in $Y$, no intercept in the CE | $\alpha\beta'Y_{t-1}$ |
| 2. no trend in $Y$, intercept in the CE | $\alpha(\beta'Y_{t-1}+\mu_0)$ |
| 3. trend in $Y$, intercept in the CE | $\alpha(\beta'Y_{t-1}+\mu_0)+\theta\gamma_0$ |
| 4. trend in both | $\alpha(\beta'Y_{t-1}+\mu_0+\mu_1t)+\theta\gamma_0$ |
| 5. quadratic trend in $Y$ | $\alpha(\beta'Y_{t-1}+\mu_0+\mu_1t)+\theta(\gamma_0+\gamma_1t)$ |

Terms inside and outside the relation aren't separately identified, so $\alpha'\theta=0$ is imposed. Use centred seasonal dummies for seasonality. The case changes the critical values (statsmodels: `det_order` in `coint_johansen`, `deterministic` in `VECM`); choose it from plots and theory beforehand.

**Trace test**, $H_0$: at most $r$ relations:
$$\lambda_{trace}(r)=-T\sum_{i=r+1}^m\ln(1-\hat\lambda_i).$$
**Maximum eigenvalue test**, $H_0$: $r$ vs $r+1$:
$$\lambda_{\max}(r,r+1)=-T\ln(1-\hat\lambda_{r+1}).$$
Both have non-standard distributions depending on $m$, the deterministic case and $r$; software reports the critical values. Test from $r=0$ upwards; the first non-rejection gives $\hat r$.

**Lecture example** (three variables): $\lambda_{\max}$ = 145.5, 71.4, 0.74 vs 5% critical values 17.8, 11.2, 4.13. Reject $r=0$ and $r=1$; don't reject $r=2$: rank 2, one stochastic trend. These critical values are the standard ones for a three-variable system without deterministic terms (`det_order=-1` in statsmodels: 17.80, 11.22, 4.13); with a constant (`det_order=0`) they would be 21.13, 14.26, 3.84. When trace and max-eigenvalue disagree, the trace test is the usual default, checked against economic sense.

### Worked examples

**VAR(2) → VECM** (lecture): $A_1=\begin{bmatrix}0.5&0.3\\0.2&0.7\end{bmatrix}$, $A_2=\begin{bmatrix}0.1&0.1\\0&0.1\end{bmatrix}$. $\Pi=A_1+A_2-I=\begin{bmatrix}-0.4&0.4\\0.2&-0.2\end{bmatrix}$; row 2 = −0.5 × row 1 (det = 0), rank 1. $\beta'=[1,-1]$, $\alpha=(-0.4,0.2)'$, $\Gamma_1=-A_2$:
$$\Delta y_t=-0.4(y_{t-1}-x_{t-1})-0.1\Delta y_{t-1}-0.1\Delta x_{t-1}+\varepsilon_{1t},\qquad\Delta x_t=0.2(y_{t-1}-x_{t-1})-0.1\Delta x_{t-1}+\varepsilon_{2t}.$$
Equilibrium $y=x$; when $y>x$, $y$ falls (speed 0.4) and $x$ rises (0.2): both adjust, $y$ about two-thirds.

**Two-variable estimated VECM** (lecture):

| Object | Estimate | Reading |
|---|---|---|
| β | $(1,-1.0087)'$ | $y_1\approx1.0087y_2$ in the long run |
| α | $(-0.3423,0.2580)'$ | $y_1$ falls when above equilibrium, $y_2$ rises |
| Π = αβ′ | $\begin{bmatrix}-0.3423&0.3453\\0.2580&-0.2602\end{bmatrix}$ | rank 1 (checks) |
| Γ | $\begin{bmatrix}0.2543&-0.0064\\0.0042&0.1849\end{bmatrix}$ | own lags matter, cross effects negligible |
| $\Sigma_u$ | $\begin{bmatrix}1.0757&0.3786\\0.3786&0.8580\end{bmatrix}$ | error correlation 0.39 |

β is close to (1, −1); $H_0:\beta=(1,-1)'$ can be tested by LR with a standard χ². The variables interact almost entirely through the error-correction term.

**Three-variable VECM with rank 2** (lecture): $\beta=\begin{bmatrix}1&0\\0&1\\-1.0504&-1.0212\end{bmatrix}$, so $EC_1=y_1-1.0504y_3$, $EC_2=y_2-1.0212y_3$, one common trend (plausibly $y_3$).
$$\Pi=\begin{bmatrix}-0.3092&0.3566&-0.0394\\0.1812&-0.3696&0.1871\\0.1118&0.0964&-0.2159\end{bmatrix},\quad\alpha=\begin{bmatrix}-0.3092&0.3566\\0.1812&-0.3696\\0.1118&0.0964\end{bmatrix},\quad\Gamma=\begin{bmatrix}0.1346&0.0418&-0.0189\\0.0204&0.0669&0.0375\\0.0647&0.0111&0.0308\end{bmatrix}.$$
(α is read from Π's first two columns; αβ′ reproduces the third column.) E.g. $\Delta y_{1t}=-0.3092\,EC_{1,t-1}+0.3566\,EC_{2,t-1}+0.1346\Delta y_{1,t-1}+0.0418\Delta y_{2,t-1}-0.0189\Delta y_{3,t-1}+\varepsilon_{1t}$. Parentheses are disequilibria, their coefficients adjustment speeds, the differences short-run effects. $y_1$ and $y_2$ correct their own deviations at 31–37% per period; $y_3$'s row is small, so it barely adjusts (test weak exogeneity, $\alpha_{3\cdot}=0$).

### IRFs and model choice

In a stable VAR all impulse responses die out. In a VECM, with $m-r$ stochastic trends, some shocks have **permanent** effects on levels; what dies out is the response of the cointegrating combinations. VECM IRFs therefore separate permanent from transitory shocks.

| Situation | Model |
|---|---|
| $I(0)$ | VAR in levels |
| $I(1)$, not cointegrated | VAR in differences |
| $I(1)$, cointegrated | VECM |

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM, select_order
lag = select_order(data, maxlags=8, deterministic="ci").bic     # lagged differences
j = coint_johansen(data, det_order=0, k_ar_diff=lag)
j.lr1, j.cvt          # trace statistics, critical values
j.lr2, j.cvm          # max-eigenvalue statistics, critical values
res = VECM(data, k_ar_diff=lag, coint_rank=2, deterministic="ci").fit()
res.beta, res.alpha, res.gamma
res.irf(24).plot()
```
`k_ar_diff` is the number of lagged differences, $p-1$.

## ✏️ Exercises

The decks have no exercises; these are constructed.

**1.** For $A_1=\begin{bmatrix}0.6&0.2\\0.3&0.5\end{bmatrix}$, $A_2=\begin{bmatrix}0.2&0.1\\0.1&0.2\end{bmatrix}$, find Π and its rank. Is there a VECM?

> [!example]- Solution
> $\Pi=\begin{bmatrix}-0.2&0.3\\0.4&-0.3\end{bmatrix}$, det = −0.06 ≠ 0: full rank, so $z=1$ is not a root: no unit root, no cointegration.
> But full rank doesn't mean stationary. $\det(I-A_1z-A_2z^2)=1-1.1z-0.16z^2+0.17z^3+0.03z^4$ has roots 0.9274, 2, −3.594, −5; $|0.9274|<1$ (companion eigenvalue 1.078): the system is **explosive**, and no VAR or VECM is valid.
>
> | Π | Roots of $\det\Phi(z)$ | Verdict |
> |---|---|---|
> | full rank | all outside | stationary: VAR in levels |
> | full rank | some inside | explosive |
> | $0<r<m$ | $m-r$ at 1, rest outside | VECM |
> | 0 | $m$ at 1 | VAR in differences |
>
> Check the roots, not only the rank.

**2.** Quarterly VECM on log consumption, log income and the real interest rate, $r=1$, $\beta=(1,-0.92,0.04)'$, $\alpha=(-0.28,0.05,-0.01)'$, only $\alpha_1$ significant. Interpret; half-life; what next?

> [!example]- Solution
> $c_t=0.92y_t-0.04r_t+$ stationary noise: long-run income elasticity 0.92; higher real rates slightly lower consumption. Consumption adjusts (28% per quarter, correct sign); half-life $\ln0.5/\ln0.72=2.11$ quarters. Income and the rate don't adjust: weakly exogenous; they drive consumption.
> Next: test $\alpha_2=\alpha_3=0$ (LR, χ²(2)); if accepted, a single-equation conditional ECM for consumption is valid. Test $\beta_y=-1$ (proportional consumption, χ²(1)) and $\beta_r=0$; run LM, ARCH and normality checks and look for structural breaks.

**3.** Four variables, $\hat\lambda=(0.41,0.22,0.09,0.02)$, $T=150$; 5% trace critical values 47.9, 29.8, 15.5, 3.84. (a) Trace statistics, (b) $r$, (c) max-eigenvalue check, (d) interpretation.

> [!example]- Solution
> $-150\ln(1-\hat\lambda_i)$ = 79.14, 37.27, 14.15, 3.03.
> (a)–(b) Trace: $r=0$: 133.59 > 47.9; $r\le1$: 54.45 > 29.8; $r\le2$: 17.18 > 15.5; $r\le3$: 3.03 < 3.84 → $\hat r=3$.
> (c) Max-eigenvalue, 5% critical values for $m=4$ with a constant (27.59, 21.13, 14.26, 3.84): reject 79.14 and 37.27; 14.15 < 14.26 → $\hat r=2$. The tests disagree, both at the margin. (These critical values are statsmodels' `det_order=0`; the trace values given match the same case.)
> (d) Two relations are clear, the third borderline. Check whether $\hat\beta_3$ makes economic sense, whether any variable adjusts to it, whether $\hat\beta_3'Y_t$ looks stationary, and sensitivity to lags and deterministic case. Over-stating $r$ imposes false structure; with $\hat\lambda_3=0.09$ I'd lean to $r=2$. At least one stochastic trend exists.

**4.** Two $I(1)$ series are cointegrated with $\beta=(1,-1)'$, $\alpha=(-0.4,0.1)'$. A colleague fits a VAR(1) in differences. What is lost, what happens to the residuals, and when is the colleague right?

> [!example]- Solution
> The error-correction term is omitted: an omitted stationary variable correlated with the regressors, so short-run estimates are biased; the long-run relation and adjustment speed are gone; forecasts let the series drift apart, increasingly with horizon; long-run IRFs are wrong.
> The omitted term is persistent, so residuals are autocorrelated; adding lags hides this partly but can't replace the level term.
> The colleague is right if $r=0$ (hence test first), at very short horizons, or when cointegration evidence is weak in a short sample (imposing a false relation is also costly). With α = −0.4 the loss here is serious; with α = −0.02 it would barely matter.

**5.** Derive the VECM form of a VAR(2).

> [!example]- Solution
> Subtract $Y_{t-1}$: $\Delta Y_t=(A_1-I)Y_{t-1}+A_2Y_{t-2}+\varepsilon_t$. Add and subtract $A_2Y_{t-1}$: $\Delta Y_t=(A_1+A_2-I)Y_{t-1}-A_2(Y_{t-1}-Y_{t-2})+\varepsilon_t$, so $\Pi=A_1+A_2-I$, $\Gamma_1=-A_2$. For VAR(p) repeat from the deepest lag, giving $\Pi=\sum A_i-I$, $\Gamma_i=-\sum_{j>i}A_j$. It is a reparameterization ($p$ level terms become 1 level and $p-1$ difference terms), not an approximation, and $\Phi(1)=-\Pi$ links the rank to the number of unit roots.

## 📝 Summary

- ECM: $\Delta Y_t=\alpha_1\Delta X_t+\gamma EC_{t-1}+\varepsilon_t$, γ < 0 pulls back to equilibrium.
- Cointegration: $I(1)$ variables with a stationary combination $\beta'Y_t$; $r$ relations, $m-r$ trends.
- VECM: $\Delta Y_t=\Pi Y_{t-1}+\sum\Gamma_i\Delta Y_{t-i}+\varepsilon_t$, $\Pi=\alpha\beta'$; rank 0 / between / full → differenced VAR / VECM / levels VAR.
- Only the space of β is identified; normalization is a convention.
- Johansen: partial out short-run terms, solve $|\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}|=0$; rank = significant eigenvalues.
- Trace and max-eigenvalue tests, sequential from $r=0$, with non-standard critical values that depend on the deterministic case.
- VECM IRFs: some shocks permanent on levels; the cointegrating combinations revert.

## ⚠️ Important Notes

1. Order: unit-root tests (all $I(1)$) → lag length on the levels VAR → Johansen with the deterministic case chosen in advance → fit at $\hat r$ → diagnostics.
2. Cointegration is neither correlation nor causation; direction comes from α (weak exogeneity) and theory.
3. Johansen over-rejects in small samples with many variables; check that $\hat\beta'Y_t$ looks stationary, that some α is significant, and robustness to lags.
4. Half-life $=\ln0.5/\ln(1-a)$: a = 0.1 → 6.6 periods; 0.28 → 2.1; 0.5 → 1.
5. Weak exogeneity (a zero row of α) is tested with a standard χ² and allows single-equation ECMs.
6. Tests involving levels of $I(1)$ variables have non-standard (Brownian-motion) distributions; restrictions on β given $r$ are standard χ².
7. Engle–Granger (levels regression, ADF on residuals, ECM in differences) works for two variables and one relation, but can't test $r$ and its normalization matters; Johansen supersedes it.
8. statsmodels' `k_ar_diff` is $p-1$.

> [!warning] Gaps in the source slides
> - Data files are missing and no outputs were saved, so the applied estimates can't be reproduced. Their internal consistency was checked (Π = αβ′ in both examples; the VAR(2)→VECM example is exact).
> - Slide 47 gives only the third row of α numerically; the rest was recovered from slide 53's Π.
> - VECM IRFs are described only qualitatively; weak exogeneity tests and Engle–Granger aren't covered; the generalized VECM with $\Theta(L)$ (slide 19) is never used.
> - Inline `<` signs were lost (γ < 0, the disequilibrium logic, the Johansen decision for $r=2$); reconstructed.
> - Corrected (2026-10-09): earlier notes flagged the slide's critical values 17.8, 11.2, 4.13 as non-standard. They are the standard 5% max-eigenvalue values for three variables with no deterministic terms (statsmodels `det_order=-1`).

**Previous:** [[07 - SARIMA and Vector Autoregression]] · **Next:** [[09 - ARCH, GARCH and Extensions]]
