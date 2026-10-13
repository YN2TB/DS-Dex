---
subject: Time-series Analysis
chapter: 10
tags: [ds, time-series, svar, identification, blanchard-quah, irf, fevd, causality]
source: "documents/slides/Lecture10_SVAR.ipynb (Lecture 10 — Structural Vector Autoregression, Dr. Thi Ha Tran); Blanchard–Quah (1989); Amisano–Giannini (1997); Enders, *Applied Econometric Time Series*"
---

# Structural Vector Autoregression

In [[07 - SARIMA and Vector Autoregression]] the Cholesky ordering turned out to be an economic assumption. This chapter treats identification directly. The data give Σ, with $n(n+1)/2$ distinct numbers; we want $P$ with $n^2$ numbers such that $\Sigma=PP'$. Infinitely many $P$ fit, so economic theory must supply the missing restrictions. Last chapter of the subject.

## 📘 Main Knowledge

### The identification problem

In the reduced-form VAR $Y_t=a_0+A_1Y_{t-1}+\dots+A_pY_{t-p}+u_t$ with $\mathbb E(u_tu_t')=\Sigma$ not diagonal, an innovation in one variable carries information about the others, so we can't tell which causes which. Reduced-form residuals are fine for forecasting but have no structural meaning.

If $\Sigma=PP'$ with $P$ non-singular, $w_t=P^{-1}u_t$ has $\mathbb E(w_tw_t')=I$, and
$$Y_t=\mu+\sum_s\Phi_su_{t-s}=\mu+\sum_s\Theta_sw_{t-s},\qquad\Theta_s=\Phi_sP.$$
The orthogonal **structural shocks** permit causal interpretation; structural decomposition splits VAR residuals into interpretable shocks. Two families: **short-run** SVARs restrict contemporaneous relations; **long-run** SVARs restrict cumulative effects. Different identifications imply different economic interpretations.

### Short-run SVAR (AB model)

$$A(I-A_1L-\dots-A_pL^p)Y_t=B\varepsilon_t\quad\Rightarrow\quad Au_t=B\varepsilon_t,\qquad\varepsilon_t\sim N(0,I).$$
The impact matrix is $P_{sr}=A^{-1}B$, so $u_t=P_{sr}\varepsilon_t$; from $A\Sigma A'=BB'$, $\Sigma=P_{sr}P_{sr}'$. $B$ gives the size of the structural shocks, $A^{-1}$ spreads them through contemporaneous relations, $A^{-1}B$ is the total immediate effect.

**Structural IRFs**: $\Theta^{sr}_s=\Phi_sA^{-1}B$, $\Theta^{sr}_0=P_{sr}$: the effect on variable $i$ of a one-time unit structural shock $j$ after $s$ periods. The $\Phi_s$ are reduced-form; all identifying content sits in the single matrix $P_{sr}$.

**Two-variable structural VAR(1)**: current values on the left,
$$Y_{1t}-\alpha_{12}Y_{2t}=c_1+\phi_{11}Y_{1,t-1}+\phi_{12}Y_{2,t-1}+b_{11}\varepsilon_{1t},\quad-\alpha_{21}Y_{1t}+Y_{2t}=c_2+\phi_{21}Y_{1,t-1}+\phi_{22}Y_{2,t-1}+b_{22}\varepsilon_{2t},$$
i.e. $AY_t=c+\Phi Y_{t-1}+B\varepsilon_t$ with $A=\begin{bmatrix}1&-\alpha_{12}\\-\alpha_{21}&1\end{bmatrix}$, $B=\operatorname{diag}(b_{11},b_{22})$. Premultiplying by $A^{-1}$ gives the reduced form with $u_t=A^{-1}B\varepsilon_t$. With $B=I$ and $A=\begin{bmatrix}1&b_{12}\\b_{21}&1\end{bmatrix}$,
$$u_t=\frac1{1-b_{12}b_{21}}\begin{bmatrix}1&-b_{12}\\-b_{21}&1\end{bmatrix}\varepsilon_t:$$
each residual mixes both shocks (and $b_{12}b_{21}\ne1$ is needed).

### Counting restrictions

- General AB model: $2n^2$ parameters, Σ gives $n(n+1)/2$, so at least $2n^2-n(n+1)/2$ restrictions.
- With $B=I$ (or diagonal variances) and unit diagonal in $A$: $n(n-1)/2$ restrictions.

Plainly: Σ gives $n(n+1)/2$ equations, $P_{sr}$ has $n^2$ unknowns; the shortfall $n(n-1)/2$ (1, 3, 6 for $n$ = 2, 3, 4) must come from outside the data. This is the order condition: necessary, not sufficient; Amisano–Giannini (1997) check local identification (the rank condition). Restrictions in the wrong places fail even if the count is right.

Why infinitely many: if $\Sigma=PP'$ and $Q$ is orthogonal, $(PQ)(PQ)'=\Sigma$. The orthogonal matrices form an $n(n-1)/2$-dimensional set, matching the shortfall; identification chooses the rotation.

### Cholesky as a recursive SVAR

Ordering $z$ before $y$ means $b_{21}=0$: $\varepsilon_{yt}=u_{yt}+b_{12}u_{zt}$, $\varepsilon_{zt}=u_{zt}$, and a $y$ shock has no contemporaneous effect on $z$. In $n$ dimensions, with $A$'s diagonal normalized to 1, Cholesky sets all entries above the diagonal to zero: exactly $n(n-1)/2$ restrictions, so exactly identified. Variable 1 responds to nothing within the period, variable 2 only to 1, and so on. Convention in macro: slow variables first (output, prices), fast ones last (interest rates, asset prices); defensible quarterly, not daily.

**Lecture example.** Residuals:

| $t$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $u_{yt}$ | 1.0 | −0.5 | 0.0 | −1.0 | 0.5 |
| $u_{zt}$ | 0.5 | −1.0 | 0.0 | −0.5 | 1.0 |

$\Sigma=\begin{bmatrix}0.5&0.4\\0.4&0.5\end{bmatrix}$ (dividing by 5), correlation 0.8. Write $\varepsilon_t=P_{SR}u_t$ with $P_{SR}=\begin{bmatrix}1&p_{12}\\p_{21}&1\end{bmatrix}$ (this maps residuals to shocks, the inverse direction of $P_{sr}$) and require $P_{SR}\Sigma P_{SR}'$ diagonal: three equations, four unknowns, one restriction needed.

- **$p_{21}=0$** ($z$ first): $0.4+0.5p_{12}=0$, $p_{12}=-0.8$; $\operatorname{var}\varepsilon_y=0.5-0.64+0.32=0.18$, $\operatorname{var}\varepsilon_z=0.5$; $\varepsilon_y=u_y-0.8u_z$ = 0.6, 0.3, 0, −0.6, −0.3; $\varepsilon_z=u_z$.
- **$p_{12}=0$** ($y$ first; not on the slides): $p_{21}=-0.8$; $\varepsilon_y=u_y$, $\varepsilon_z=u_z-0.8u_y$ = −0.3, −0.6, 0, 0.3, 0.6.

In period 1, $\varepsilon_z$ is +0.5 under one ordering and −0.3 under the other: the structural story reverses. With correlation 0.8, ordering decides a great deal; justify it with theory. A quick diagnostic: look at the residual correlation matrix first.

### Beyond Cholesky

| Restriction | Fixes |
|---|---|
| coefficient | one contemporaneous effect (e.g. $\alpha_{12}=0$) |
| variance | the size of a structural shock |
| symmetry | equal effects across equations or countries |
| sign | the direction of responses |

Sign restrictions (e.g. a monetary tightening raises the rate and lowers output and prices for a few quarters) are weaker than zeros and widely used, but they set-identify: a range of IRFs from random rotations of $P$ that satisfy the signs (Uhlig 2005).

```python
from statsmodels.tsa.vector_ar.svar_model import SVAR
A = np.array([[1, 0, 0], [np.nan, 1, 0], [np.nan, np.nan, 1]])   # NaN = free
B = np.diag([np.nan, np.nan, np.nan])
res = SVAR(data, svar_type="AB", A=A, B=B).fit(maxlags=2)
impact = np.linalg.inv(res.A) @ res.B       # P_sr
res.irf(20).plot()
```

### Long-run SVAR

If the VAR is stable, $Y_t=C(L)\varepsilon_t$ with $C(L)=(I-A_1L-\dots-A_pL^p)^{-1}A^{-1}B$. With $C(L)=C_0+C_1L+\dots$, the cumulative effect is $C(1)=C_0+C_1+\dots$; for a VAR(1), $C_k=\Phi^kA^{-1}B$ and
$$C(1)=(I-\Phi)^{-1}A^{-1}B\qquad\big(\text{VAR}(p):\ (I-\textstyle\sum A_i)^{-1}A^{-1}B\big).$$
Long-run SVARs restrict $C$, usually by exclusions: $C(1,2)=0$ means shock 2 has no long-run effect on variable 1. $I-\sum A_i$ is $-\Pi$ of the VECM and $\Phi(1)$ of the VAR. Long-run claims ("no permanent effect") often follow directly from theory and don't depend on data frequency: demand shocks can't permanently change output.

### Blanchard–Quah

$x_t=(\Delta y_t,z_t)'$ with $y_t$ $I(1)$ (log real GNP) and $z_t$ stationary (unemployment). Bivariate moving average: $x_t=\sum_kC_k\varepsilon_{t-k}$, where $c_{ij}(k)$ is the effect of shock $j$ on variable $i$ after $k$ periods.

With orthogonal unit-variance shocks, $e_{1t}=c_{11}(0)\varepsilon_{1t}+c_{12}(0)\varepsilon_{2t}$, $e_{2t}=c_{21}(0)\varepsilon_{1t}+c_{22}(0)\varepsilon_{2t}$, giving three conditions:
$$\operatorname{var}e_1=c_{11}(0)^2+c_{12}(0)^2,\quad\operatorname{var}e_2=c_{21}(0)^2+c_{22}(0)^2,\quad\mathbb E(e_1e_2)=c_{11}(0)c_{21}(0)+c_{12}(0)c_{22}(0).$$
The fourth comes from the long run. Writing $x_t=[1-A(L)L]^{-1}e_t$ and requiring $\varepsilon_1$'s cumulative effect on $\Delta y_t$ to vanish:
$$\Big[1-\sum_ka_{22}(k)\Big]c_{11}(0)+\Big[\sum_ka_{12}(k)\Big]c_{21}(0)=0.$$
Since $y$ is the sum of its differences, zero cumulative effect on $\Delta y$ means no permanent effect on $y$: $\varepsilon_1$ is a demand shock, $\varepsilon_2$ (unrestricted) the supply shock that moves long-run output.

Procedure: (1) test for trends and unit roots (no unit root in $y$, no point proceeding); make both variables $I(0)$; choose lags; check residuals; compute $\operatorname{var}e_1$, $\operatorname{var}e_2$, $\operatorname{cov}$, $1-\sum a_{22}(k)$, $\sum a_{12}(k)$. (2) Solve the four equations for the $c_{ij}(0)$. (3) Recover the shock series and compute IRFs, FEVDs and **historical decompositions** (e.g. set all $\varepsilon_1$ to zero: $\Delta y_t=\sum_kc_{12}(k)\varepsilon_{2,t-k}$ isolates the permanent component, answering what drove a particular episode).

| | Short-run SVAR | Long-run (BQ) | Cholesky |
|---|---|---|---|
| restricts | impact $A^{-1}B$ | cumulative $C(1)$ | impact, recursively |
| claim | "x doesn't react to y within the period" | "x has no permanent effect on y" | an ordering |
| depends on frequency | yes | no | yes |
| needs a unit root | no | yes | no |

## ✏️ Exercises

The deck has no exercises; these are constructed.

**1.** For $n$ = 2–5, count Σ's distinct elements, $P_{sr}$'s unknowns, and the restrictions needed. Does Cholesky supply the right number?

> [!example]- Solution
> | $n$ | Σ | $P_{sr}$ | needed | Cholesky zeros |
> |---|---|---|---|---|
> | 2 | 3 | 4 | 1 | 1 |
> | 3 | 6 | 9 | 3 | 3 |
> | 4 | 10 | 16 | 6 | 6 |
> | 5 | 15 | 25 | 10 | 10 |
>
> Cholesky is always exactly identified. Under-identified: no unique IRFs. Exactly identified: unique but untestable (you can't test the ordering). Over-identified: surplus restrictions testable by LR against the unrestricted Σ, with df = number of surplus restrictions. Ten defensible timing restrictions for five variables are hard to find, which is why large SVARs fall back on recursion or signs.

**2.** For the lecture's Σ, find the Cholesky factor under both orderings and the share of $y$'s impact variance from each shock.

> [!example]- Solution
> $y$ first: $L_A=\begin{bmatrix}0.7071&0\\0.5657&0.4243\end{bmatrix}$. $z$ first (original labels): $L_B=\begin{bmatrix}0.4243&0.5657\\0&0.7071\end{bmatrix}$ (check $L_BL_B'=\Sigma$).
> Impact variance of $y$ (0.50): A gives 100% / 0%; B gives 36% / 64%. The contested share is $\rho^2=0.64$: with ρ = 0.2 only 4% would be at stake. Report both; if the conclusion changes, move to theory-based, long-run or sign restrictions.

**3.** Quarterly $(\Delta y_t,\pi_t,i_t)$. (a) How many restrictions? (b) A recursive scheme and its defence. (c) A non-recursive restriction and what it buys.

> [!example]- Solution
> (a) 3.
> (b) Order $(\Delta y,\pi,i)$: output doesn't respond within the quarter to inflation or rates (planning lags); inflation doesn't respond to the rate within the quarter (sticky prices); the rate responds to both (the central bank's reaction function), so the third shock is a monetary policy shock (as in Christiano–Eichenbaum–Evans). Credible quarterly, not at daily frequency.
> (c) With money growth instead of the rate, impose a money-demand income elasticity of 1 ($a_{31}=-1$): a coefficient restriction with a magnitude from theory. Added to two other restrictions it over-identifies the system, making one restriction testable (LR, χ²(1)). Alternatively, sign restrictions on a monetary shock give a set of IRFs.

**4.** VAR(1) in $(\Delta y_t,z_t)'$ with $\hat\Phi=\begin{bmatrix}0.3&-0.2\\0.1&0.6\end{bmatrix}$, $\hat\Sigma=\begin{bmatrix}0.8&0.3\\0.3&0.5\end{bmatrix}$. Impose that shock 2 has no long-run effect on $y$. Find $(I-\Phi)^{-1}$, $C(1)$ and $P_{sr}$, and interpret.

> [!example]- Solution
> $I-\Phi=\begin{bmatrix}0.7&0.2\\-0.1&0.4\end{bmatrix}$ (det 0.30), $(I-\Phi)^{-1}=\begin{bmatrix}1.3333&-0.6667\\0.3333&2.3333\end{bmatrix}$.
> $C(1)=(I-\Phi)^{-1}P_{sr}$ must be lower triangular, and $C(1)C(1)'=\Omega_{LR}=(I-\Phi)^{-1}\Sigma[(I-\Phi)^{-1}]'=\begin{bmatrix}1.1111&0.4444\\0.4444&3.2778\end{bmatrix}$, so $C(1)$ is its Cholesky factor: $\begin{bmatrix}1.0541&0\\0.4216&1.7607\end{bmatrix}$.
> $P_{sr}=(I-\Phi)C(1)=\begin{bmatrix}0.8222&0.3521\\0.0632&0.7043\end{bmatrix}$; check $P_{sr}P_{sr}'=\Sigma$.
> $P_{sr}$ isn't triangular: shock 2 moves $\Delta y$ on impact (0.352) but its cumulative effect is zero. So shock 1 is supply (permanent, $C(1)_{11}=1.054$), shock 2 demand (temporary). A short-run zero would have wrongly forbidden the impact effect. The method is Cholesky applied to $\Omega_{LR}$, which is what the notebook's long-run code computes.

**5.** Show Cholesky is a short-run SVAR, and why $P_{sr}$ equals the Cholesky factor of Σ.

> [!example]- Solution
> Take $A$ unit lower triangular and $B$ diagonal: $n(n-1)/2+n=n(n+1)/2$ parameters, exactly identified. $A^{-1}$ is unit lower triangular too, so $P_{sr}=A^{-1}B$ is lower triangular with diagonal $b_{ii}$. A positive-definite Σ has a unique lower-triangular factor with positive diagonal, so (with $b_{ii}>0$ fixing signs) $P_{sr}=L$. Then $B=\operatorname{diag}(L)$ and $A^{-1}=LB^{-1}$.
> So Cholesky is the SVAR whose restrictions say variable $i$ doesn't respond within the period to shocks $j>i$. Exact identification means the data can't test it, and the $n!$ orderings all fit Σ perfectly; only theory can choose.

## 📝 Summary

- Σ fixes $P$ only up to a rotation; theory must supply $n(n-1)/2$ restrictions.
- Reduced-form residuals mix structural shocks; SVAR recovers orthogonal shocks via $u_t=P_{sr}\varepsilon_t$.
- AB model: $Au_t=B\varepsilon_t$, $P_{sr}=A^{-1}B$, structural IRFs $\Phi_sA^{-1}B$.
- Order condition necessary, rank condition (Amisano–Giannini) needed too.
- Cholesky = recursive SVAR, exactly identified, untestable; the contested share is ρ².
- Alternatives: coefficient, variance, symmetry, sign restrictions; over-identification allows tests.
- Long-run SVAR restricts $C(1)=(I-\sum A_i)^{-1}A^{-1}B$; Blanchard–Quah separates temporary demand from permanent supply shocks; $C(1)$ = Cholesky factor of the long-run covariance.
- Identified shocks give IRFs, FEVDs and historical decompositions.

## ⚠️ Important Notes

1. The slides define $P$ both ways: $u=P_{sr}\varepsilon$ in §2, $\varepsilon=P_{SR}u$ in the example (unit diagonal). Check which before interpreting.
2. Restriction counts can be right and placement wrong; statsmodels' SVAR may fail to converge.
3. A well-fitting exactly identified SVAR says nothing about its ordering.
4. Report the identifying assumptions in words, the residual correlations, IRFs under at least two schemes, and bootstrapped bands; say so if conclusions aren't robust.
5. Short-run restrictions suit timing arguments, long-run ones theory about permanent effects (needing a unit root), sign restrictions directions without magnitudes.
6. Long-run IRFs depend on $(I-\sum\hat A_i)^{-1}$, imprecise near a unit root (Faust–Leeper 1997).
7. Statistics gives dynamics; identifying assumptions turn them into causal claims.

> [!warning] Gaps in the source slides
> - Only Cholesky "Case 2" ($p_{21}=0$) is shown; Case 1 is worked above to show that ordering matters.
> - The Blanchard–Quah algebra is never applied to numbers; Exercise 4 fills this. The code loads `lutkepohl2.dta` and `m1gdp.dta` from stata-press.com (reproducible), but no outputs are saved.
> - Structural FEVD is listed on the title slide but not covered (it is the ch. 07 formula with $\Theta^{sr}_s$ in place of $\Phi_s$). Sign restrictions get one bullet; confidence bands are never mentioned.
> - The two counting slides use different set-ups without saying so (both correct).
> - A few inline `<` signs were lost; one comment is in Vietnamese.

**Previous:** [[09 - ARCH, GARCH and Extensions]] · **Index:** [[00-Index]]
