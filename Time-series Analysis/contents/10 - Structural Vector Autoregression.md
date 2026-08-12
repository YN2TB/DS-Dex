---
subject: Time-series Analysis
chapter: 10
tags: [ds, time-series, svar, identification, blanchard-quah, irf, fevd, causality]
source: "documents/slides/Lecture10_SVAR.ipynb (Lecture 10 — Structural Vector Autoregression, Dr. Thi Ha Tran); Blanchard–Quah (1989); Amisano–Giannini (1997); Enders, *Applied Econometric Time Series*"
---

# Structural Vector Autoregression

> [!abstract] Where this sits in the course
> [[07 - SARIMA and Vector Autoregression]] built a VAR, produced impulse responses, and then had to admit that **the Cholesky ordering was an economic assumption smuggled in as a matrix factorisation.** This chapter confronts that head-on.
>
> **The whole subject of SVAR is one question:** the data give you $\Sigma$, a symmetric matrix with $n(n+1)/2$ distinct numbers. You want $P$, an $n\times n$ matrix with $n^2$ numbers, satisfying $\Sigma = PP'$. There are more unknowns than equations, so **infinitely many $P$'s fit equally well.** Economic theory must supply the missing restrictions. Everything below is a catalogue of ways to supply them.
>
> This is the final chapter of the subject.

---

## 📘 Main Knowledge

### 1. The identification problem

Recall the reduced-form VAR($p$):

$$
Y_t = a_0+A_1Y_{t-1}+\cdots+A_pY_{t-p}+u_t,
\qquad
\Phi(L)Y_t = a_0+u_t
$$
$$
\mathbb{E}(u_t)=0,
\qquad
\mathbb{E}(u_tu_t')=\Omega,
\qquad
\mathbb{E}(u_tu_s')=0 \;\; (t\neq s)
$$

**The problem.** $\Sigma$ is **not** restricted to be diagonal. An innovation in one variable therefore contains information about innovations in the others, so causal interpretation of IRFs is problematic: **we cannot tell whether a shock to variable 1 causes variable 2, or the reverse.**

**The fix, in outline.** Suppose there is a non-singular $P$ with

$$
\Sigma = PP'
\qquad\Longrightarrow\qquad
w_t = P^{-1}u_t,
\qquad
\mathbb{E}(w_tw_t') = P^{-1}\Sigma(P^{-1})' = I_n
$$

Rewriting the MA($\infty$) representation:

$$
Y_t = \mu+\sum_{s=0}^\infty\Phi_su_{t-s}
= \mu+\sum_{s=0}^\infty\Phi_sPP^{-1}u_{t-s}
= \mu+\sum_{s=0}^\infty\Theta_sw_{t-s},
\qquad
\Theta_s = \Phi_sP
$$

**$w_t$ are orthogonal shocks, and they permit causal interpretation.**

> [!important] Why reduced-form residuals are not structural shocks
> In a reduced-form VAR the residuals are correlated: $\mathbb{E}(u_tu_t')=\Sigma$. If $\Sigma$ is not diagonal, an innovation in one equation carries information about innovations in others. **Reduced-form residuals are useful for forecasting but have no automatic structural economic interpretation.**
>
> SVAR introduces **structural shocks** $\varepsilon_t$ that are economically meaningful and mutually uncorrelated, $\mathbb{E}(\varepsilon_t\varepsilon_t')=I$, and recovers them from $u_t$ via $u_t = P\varepsilon_t$. **Structural decomposition means decomposing VAR residuals into economically interpretable shocks.**

**SVAR models provide a framework for estimation and inference about a broad class of matrices $P$**, from which structural IRFs and structural FEVDs follow. There are **two main types**:

| Type | Identifies $P$ by restricting… |
|---|---|
| **Short-run SVAR** | **Contemporaneous** correlations |
| **Long-run SVAR** | **Long-run cumulative effects** of shocks |

**Different identification strategies imply different economic interpretations.**

---

### 2. Short-run SVAR

#### The AB model

Take the reduced-form VAR $(I_K-A_1L-\cdots-A_pL^p)Y_t = u_t$. The associated **short-run SVAR** is

$$
A\big(I_K-A_1L-\cdots-A_pL^p\big)Y_t = B\varepsilon_t
$$

Combining with the reduced form gives the **key contemporaneous relation**:

$$
\boxed{\;Au_t = B\varepsilon_t\;}
$$

where $A$ and $B$ are non-singular $n\times n$ parameter matrices and

$$
\varepsilon_t\sim N(0,I_n),
\qquad
\mathbb{E}(\varepsilon_t\varepsilon_s')=0 \;\; (t\neq s)
$$

**Identification is achieved by imposing restrictions on $A$ and $B$.**

#### The contemporaneous impact matrix

$$
\boxed{\;P_{sr} = A^{-1}B\;}
\qquad\Longrightarrow\qquad
u_t = P_{sr}\varepsilon_t
$$

To see the link to $\Sigma$: from $Au_t=B\varepsilon_t$, form $Au_tu_t'A' = B\varepsilon_t\varepsilon_t'B'$ and take expectations:

$$
A\Sigma A' = BB'
\qquad\Longrightarrow\qquad
\Sigma = A^{-1}BB'(A^{-1})' = P_{sr}P_{sr}'
$$

**Reading the pieces:** $B$ gives the **direct size** of structural shocks (and scales them to unit variance); $A^{-1}$ **spreads** those shocks through contemporaneous relations; $A^{-1}B$ gives the **total immediate effect**.

#### Structural IRFs

If the VAR is stable it has an MA($\infty$) representation $Y_t = \mu+\sum_s\Phi_su_{t-s}$. Substituting $u_t = A^{-1}B\varepsilon_t$:

$$
Y_t = \mu+\sum_{s=0}^\infty\Phi_sA^{-1}B\,\varepsilon_{t-s} = \mu+\sum_{s=0}^\infty\Theta_s^{sr}\varepsilon_{t-s}
$$

$$
\boxed{\;\Theta_s^{sr} = \Phi_sA^{-1}B\;},
\qquad
\Theta_0^{sr} = P_{sr}
$$

**IRF = dynamic multiplier × structural impact matrix.** A structural IRF measures the effect on variable $i$ of a one-time unit increase in structural shock $j$ after $s$ periods.

Note that the $\Phi_s$ — computed by the recursion $\Phi_s = A_1\Phi_{s-1}+\cdots+A_p\Phi_{s-p}$ of [[07 - SARIMA and Vector Autoregression]] — are **entirely reduced-form** and identification-free. **All the identifying content sits in the single matrix $P_{sr}$**, which post-multiplies every horizon. This is why arguments about identification are arguments about one $n\times n$ matrix, not about the dynamics.

#### A two-variable structural VAR(1)

$$
\begin{aligned}
Y_{1t}-\alpha_{12}Y_{2t} &= c_1+\phi_{11}Y_{1,t-1}+\phi_{12}Y_{2,t-1}+b_{11}\varepsilon_{1t}\\
-\alpha_{21}Y_{1t}+Y_{2t} &= c_2+\phi_{21}Y_{1,t-1}+\phi_{22}Y_{2,t-1}+b_{22}\varepsilon_{2t}
\end{aligned}
$$

**Current variables appear on the left-hand side** — that is what makes this *structural*. The coefficients measure contemporaneous interaction:

$$
\alpha_{12}: Y_{2t}\to Y_{1t},
\qquad
\alpha_{21}: Y_{1t}\to Y_{2t}
$$

In matrix form:

$$
\underbrace{\begin{bmatrix}1&-\alpha_{12}\\-\alpha_{21}&1\end{bmatrix}}_{A}
\begin{bmatrix}Y_{1t}\\Y_{2t}\end{bmatrix}
= \begin{bmatrix}c_1\\c_2\end{bmatrix}
+ \begin{bmatrix}\phi_{11}&\phi_{12}\\\phi_{21}&\phi_{22}\end{bmatrix}
\begin{bmatrix}Y_{1,t-1}\\Y_{2,t-1}\end{bmatrix}
+ \underbrace{\begin{bmatrix}b_{11}&0\\0&b_{22}\end{bmatrix}}_{B}
\begin{bmatrix}\varepsilon_{1t}\\\varepsilon_{2t}\end{bmatrix}
$$

compactly $AY_t = c+\Phi Y_{t-1}+B\varepsilon_t$. **$A$ sits on the left because it describes simultaneous relations among current variables.**

**Premultiplying by $A^{-1}$** gives the reduced form:

$$
Y_t = A^{-1}c+A^{-1}\Phi Y_{t-1}+A^{-1}B\varepsilon_t
= \tilde c+\tilde\Phi Y_{t-1}+u_t,
\qquad
u_t = A^{-1}B\varepsilon_t
$$

#### Residuals are mixtures

Take the simplest normalisation, $B = I$ (unit structural variances) and

$$
A = \begin{bmatrix}1&b_{12}\\b_{21}&1\end{bmatrix}
\qquad\Longrightarrow\qquad
\begin{bmatrix}u_{yt}\\u_{zt}\end{bmatrix}
= \frac{1}{1-b_{12}b_{21}}\begin{bmatrix}1&-b_{12}\\-b_{21}&1\end{bmatrix}
\begin{bmatrix}\varepsilon_{yt}\\\varepsilon_{zt}\end{bmatrix}
$$

**$u_{yt}$ and $u_{zt}$ are not pure shocks — they are composites of $\varepsilon_{yt}$ and $\varepsilon_{zt}$.** IRFs computed directly from $u_t$ can therefore be economically misleading. (Note also the factor $1/(1-b_{12}b_{21})$: the system is only invertible if $b_{12}b_{21}\neq1$, the usual simultaneous-equations rank condition.)

---

### 3. Counting restrictions — the order condition

#### Two ways to count, depending on the normalisation

**Version 1 — the general AB model.** $A$ and $B$ together hold $2n^2$ parameters; the covariance matrix $\Sigma$ provides only

$$
\frac{n(n+1)}{2}
\qquad\text{free (distinct) parameters}
$$

so at most that many can be identified. **Identification therefore requires at least**

$$
\boxed{\;2n^2-\frac{n(n+1)}{2}\;\text{ restrictions}\;}
$$

**Version 2 — the A model with normalisations.** Fix $B=I$ and normalise the diagonal of $A$ to 1, leaving $n^2-n$ unknown off-diagonal parameters plus $n$ structural variances. Matching against the $n(n+1)/2$ distinct elements of $\Sigma$ leaves

$$
\boxed{\;\frac{n^2-n}{2} = \frac{n(n-1)}{2}\;\text{ restrictions needed}\;}
$$

> [!important] The counting, said plainly
> **$\Sigma$ is symmetric, so it gives you $n(n+1)/2$ equations. $P_{sr}$ has $n^2$ unknowns. The shortfall is**
> $$n^2-\frac{n(n+1)}{2} = \frac{n(n-1)}{2}$$
> — exactly the number of entries above the diagonal. **You must supply that many restrictions from outside the data.** For $n=2$ that is 1; for $n=3$ it is 3; for $n=4$ it is 6.
>
> This is the **order condition** — necessary, not sufficient. **Amisano–Giannini (1997)** provide a method to check **local identification** (the rank condition). **Not all sets of restrictions lead to a valid SVAR** — you can impose the right *number* of restrictions in the wrong *places* and still fail.

#### Identification through the covariance matrix

Since $u_t = P_{sr}\varepsilon_t$ and $\mathbb{E}(\varepsilon_t\varepsilon_t')=I$:

$$
\Sigma = \mathbb{E}(u_tu_t') = P_{sr}\,\mathbb{E}(\varepsilon_t\varepsilon_t')\,P_{sr}' = P_{sr}P_{sr}'
$$

**The observed object is $\Sigma$; the unknown structural object is $P_{sr}$; and many $P_{sr}$ satisfy $\Sigma = P_{sr}P_{sr}'$.**

> [!note] Why infinitely many, precisely
> If $\Sigma = PP'$ and $Q$ is any orthogonal matrix ($QQ'=I$), then $(PQ)(PQ)' = PQQ'P' = PP' = \Sigma$. So **$PQ$ works just as well as $P$, for every orthogonal $Q$.** The set of orthogonal $n\times n$ matrices has dimension $n(n-1)/2$ — exactly the shortfall counted above. The data pin down $P$ only up to an arbitrary rotation, and **identification is the process of choosing which rotation, using economic theory.**

---

### 4. Cholesky as a recursive SVAR

Cholesky decomposition **imposes a recursive ordering.** If $z_t$ is ordered before $y_t$, then $z_t$ is contemporaneously prior, which corresponds to

$$
b_{21}=0
$$

Then the structural shocks are recovered as

$$
\varepsilon_{yt} = u_{yt}+b_{12}u_{zt},
\qquad
\varepsilon_{zt} = u_{zt}
$$

**The restriction $b_{21}=0$ means a structural shock to $y_t$ has no contemporaneous effect on $z_t$.** That is a strong economic assumption. **If the ordering has no theoretical foundation, the identified shocks may simply be wrong.**

#### In $n$ dimensions

Write the general structural system

$$
AY_t = c+\Gamma Y_{t-1}+\varepsilon_t,
\qquad
A = \begin{bmatrix}
1&b_{12}&\cdots&b_{1n}\\
b_{21}&1&\cdots&b_{2n}\\
\vdots&\vdots&\ddots&\vdots\\
b_{n1}&b_{n2}&\cdots&1
\end{bmatrix}
$$

with the diagonal normalised to one, and $u_t = A^{-1}\varepsilon_t$.

**Cholesky identification sets every element above the main diagonal to zero:**

$$
b_{12}=b_{13}=\cdots=b_{1n}=0,
\qquad
b_{23}=\cdots=b_{2n}=0,
\qquad\ldots\qquad
b_{n-1,n}=0
$$

The number of zero restrictions is exactly $\dfrac{n^2-n}{2}$, so **the Cholesky system is exactly identified** — the order condition holds with equality, no more and no less.

> [!important] **Cholesky is not just a statistical method; it imposes economic assumptions.**
> The recursive structure says: variable 1 responds to nothing contemporaneously; variable 2 responds only to variable 1; variable 3 to variables 1 and 2; and so on. **The result depends entirely on the chosen ordering.** [[07 - SARIMA and Vector Autoregression]] Exercise 3 showed the same data yielding an FEVD of 99.6% or 63.7% for the same quantity depending on the order.
>
> The convention in macro is to order **slow-moving** variables first (output, prices — which cannot respond within the quarter) and **fast-moving** ones last (interest rates, asset prices — which respond immediately to everything). That convention is itself an economic claim, and it is defensible for quarterly data and indefensible for daily.

> [!example] A structural decomposition, worked end to end
> Estimate a two-variable reduced-form VAR and obtain the residuals:
>
> | $t$ | 1 | 2 | 3 | 4 | 5 |
> |---|---|---|---|---|---|
> | $u_{yt}$ | 1.0 | $-0.5$ | 0.0 | $-1.0$ | 0.5 |
> | $u_{zt}$ | 0.5 | $-1.0$ | 0.0 | $-0.5$ | 1.0 |
>
> **Sample covariance matrix** (dividing by $T=5$; each series has mean 0):
> $$\Sigma = \begin{bmatrix}0.5&0.4\\0.4&0.5\end{bmatrix},
> \qquad
> \rho(u_{yt},u_{zt}) = \frac{0.4}{0.5} = \mathbf{0.8}$$
> (I recomputed these from the residuals — $\sum u_y^2 = 2.5$, $\sum u_z^2 = 2.5$, $\sum u_yu_z = 2.0$, all divided by 5. ✓)
>
> **The residuals are strongly correlated, so they cannot be read as independent structural shocks.**
>
> **Set-up.** Write $\varepsilon_t = P_{SR}u_t$ (note: here $P_{SR}$ maps residuals *to* shocks — the inverse of the $P_{sr}$ in §2; see the notation warning at the end). Requiring the structural covariance to be diagonal:
> $$\Sigma_\varepsilon = P_{SR}\Sigma P_{SR}'
> \quad\text{diagonal},
> \qquad
> P_{SR} = \begin{bmatrix}1&p_{12}\\ p_{21}&1\end{bmatrix}$$
> **Three independent equations** (the distinct entries of $\Sigma$), **four unknowns** ($p_{12}$, $p_{21}$, $\mathrm{var}\,\varepsilon_y$, $\mathrm{var}\,\varepsilon_z$) — **one restriction needed**, matching $n(n-1)/2 = 1$.
>
> ---
> **Cholesky Case 2 — impose $p_{21}=0$** ($z$ ordered first, so $z$'s shock is not contaminated).
>
> The off-diagonal condition is $0.5p_{21}+0.4+p_{12}(0.4p_{21}+0.5) = 0$, which at $p_{21}=0$ becomes
> $$0 = 0.4+0.5p_{12}
> \qquad\Longrightarrow\qquad
> p_{12} = \mathbf{-0.8}$$
> $$\mathrm{var}(\varepsilon_y) = 0.5+2(0.4)(-0.8)+0.5(0.64) = 0.5-0.64+0.32 = \mathbf{0.18}$$
> $$\mathrm{var}(\varepsilon_z) = \mathbf{0.5}$$
> $$P_{SR} = \begin{bmatrix}1&-0.8\\0&1\end{bmatrix}
> \qquad\Longrightarrow\qquad
> \varepsilon_{yt} = u_{yt}-0.8u_{zt},
> \quad
> \varepsilon_{zt} = u_{zt}$$
>
> **The recovered shocks:**
>
> | $t$ | 1 | 2 | 3 | 4 | 5 |
> |---|---|---|---|---|---|
> | $\varepsilon_{yt}$ | 0.6 | 0.3 | 0.0 | $-0.6$ | $-0.3$ |
> | $\varepsilon_{zt}$ | 0.5 | $-1.0$ | 0.0 | $-0.5$ | 1.0 |
>
> (Check $t=2$: $-0.5-0.8(-1.0) = -0.5+0.8 = 0.3$ ✓. All five verified.)
>
> ---
> **Case 1 — the other ordering, $p_{12}=0$** (the slides omit this; here it is).
>
> $0.5p_{21}+0.4 = 0 \Rightarrow p_{21} = -0.8$, so $\varepsilon_{zt} = u_{zt}-0.8u_{yt}$, $\varepsilon_{yt}=u_{yt}$, with $\mathrm{var}(\varepsilon_y)=0.5$, $\mathrm{var}(\varepsilon_z)=0.18$:
>
> | $t$ | 1 | 2 | 3 | 4 | 5 |
> |---|---|---|---|---|---|
> | $\varepsilon_{yt}$ | 1.0 | $-0.5$ | 0.0 | $-1.0$ | 0.5 |
> | $\varepsilon_{zt}$ | $-0.3$ | $-0.6$ | 0.0 | 0.3 | 0.6 |
>
> **Compare the two.** Under Case 2, $\varepsilon_{y1}=0.6$; under Case 1, $\varepsilon_{y1}=1.0$. Under Case 2, $\varepsilon_{z1}=0.5$; under Case 1, $\varepsilon_{z1}=-0.3$ — **the sign flips.** Period 1 goes from "both shocks positive" to "a positive $y$ shock and a negative $z$ shock". Any narrative built on these shocks reverses with the ordering.
>
> **⇒ Changing the ordering changes the structural shocks.**

**Why ordering matters so much here.** The residual correlation is $0.8$ — very high. **Different orderings assign contemporaneous effects differently across shocks:** $b_{12}=0$ gives $y$ contemporaneous priority; $b_{21}=0$ gives $z$ priority. **Structural IRFs and FEVDs can change substantially.** Cholesky identification should be **justified by economic theory, not chosen mechanically.**

> [!tip] The one diagnostic worth running before anything else
> **Look at the residual correlation matrix.** If the off-diagonals are near zero, the ordering barely matters and any identification gives similar answers. If they are large (say $|\rho|>0.3$), the ordering is doing heavy lifting and **you must justify it or report robustness across orderings.** This is a thirty-second check that most applied work skips.

---

### 5. Beyond Cholesky

Cholesky is only **one** type of identifying restriction. Since a two-variable system has three independent equations and four unknowns, **any** valid additional restriction identifies the model. Alternatives:

| Restriction type | What it fixes |
|---|---|
| **Coefficient restrictions** | One contemporaneous effect (e.g. $\alpha_{12}=0$: $Y_2$ does not affect $Y_1$ within the period) |
| **Variance restrictions** | The size of one structural shock |
| **Symmetry restrictions** | Equal effects across equations or countries |
| **Sign restrictions** | The expected *direction* of responses |

**The key idea is to use economic theory to impose restrictions that recover meaningful structural shocks.**

> [!note] Sign restrictions are the modern workhorse
> Zero restrictions are strong — they claim an effect is *exactly* nil. **Sign restrictions** instead require only that, say, a contractionary monetary shock raises the interest rate and lowers output and prices for a few quarters. These are far more defensible theoretically. The cost: sign restrictions are **set-identifying**, not point-identifying — they deliver a *range* of admissible IRFs (drawn by randomly rotating $P$ and keeping the rotations that satisfy the signs) rather than a single line. The slides list them without elaboration; Uhlig (2005) is the standard reference.

```python
from statsmodels.tsa.vector_ar.svar_model import SVAR
import numpy as np

# A-model: NaN marks a free parameter, numbers are imposed restrictions
A = np.array([[1,   0,   0],
              [np.nan, 1, 0],
              [np.nan, np.nan, 1]])          # recursive (Cholesky-equivalent)
B = np.diag([np.nan, np.nan, np.nan])        # diagonal, free scales

res = SVAR(data, svar_type="AB", A=A, B=B).fit(maxlags=2)
impact = np.linalg.inv(res.A) @ res.B         # P_sr = A^{-1}B
res.irf(20).plot()
```

---

### 6. Long-run SVAR

#### The idea

Start from the short-run SVAR $A(I_K-A_1L-\cdots-A_pL^p)Y_t = B\varepsilon_t$. If the VAR is stable, rewrite it as

$$
Y_t = C(L)\varepsilon_t,
\qquad
C(L) = \big(I_K-A_1L-\cdots-A_pL^p\big)^{-1}A^{-1}B
$$

with $\Sigma = A^{-1}BB'(A^{-1})'$ as before. **In a long-run SVAR, restrictions are imposed on the elements of $C$**, usually as exclusion restrictions. For example

$$
C(1,2) = 0
$$

means **the long-run response of variable 1 to the structural shock driving variable 2 is zero.**

#### Why $C(1)$ measures long-run effects

Expand the lag polynomial $C(L) = C_0+C_1L+C_2L^2+\cdots$, so

$$
Y_t = C_0\varepsilon_t+C_1\varepsilon_{t-1}+C_2\varepsilon_{t-2}+\cdots
$$

The **total cumulative effect** of a shock is obtained by setting $L=1$:

$$
\boxed{\;C(1) = C_0+C_1+C_2+\cdots\;}
$$

**$C(1)$ measures the long-run effect of structural shocks on the variables.**

**Computing it.** From $Y_t = \Phi Y_{t-1}+A^{-1}B\varepsilon_t$ (writing the VAR(1) case for clarity), $C(L) = (I-\Phi L)^{-1}A^{-1}B$. The matrix geometric expansion $(I-\Phi L)^{-1} = I+\Phi L+\Phi^2L^2+\cdots$ gives

$$
C_0 = A^{-1}B,
\qquad
C_1 = \Phi A^{-1}B,
\qquad
C_2 = \Phi^2A^{-1}B,
\qquad\ldots
$$

and summing the geometric series,

$$
\boxed{\;C(1) = (I-\Phi)^{-1}A^{-1}B\;}
$$

For a general VAR($p$), $(I-\Phi)^{-1}$ becomes $\big(I-\sum_{i=1}^pA_i\big)^{-1}$.

> [!important] The connection to the rest of the course
> $\big(I-\sum_iA_i\big)$ is exactly $-\Pi$ from [[08 - VECM and Cointegration]], and $\Phi(1)$ from [[07 - SARIMA and Vector Autoregression]]. **The same matrix appears in three chapters wearing three hats:** the long-run matrix of a VECM, the value of the lag polynomial at $z=1$, and the inverse of the long-run multiplier here. Its singularity is what signals unit roots; its inverse is what accumulates shocks forever.

> [!tip] Why long-run restrictions are often more defensible
> A short-run restriction claims "shock $j$ has no effect on variable $i$ **this quarter**" — an assertion about data timing that is hard to defend and depends on the sampling frequency. A long-run restriction claims "shock $j$ has no **permanent** effect on variable $i$" — which is often a direct implication of theory. The canonical example: standard macro theory says **demand shocks cannot permanently change the level of output** (only supply/technology shocks can), a restriction that holds regardless of whether you use monthly or quarterly data.

---

### 7. The Blanchard–Quah decomposition

The canonical long-run SVAR.

#### Set-up

$$
x_t = \begin{bmatrix}\Delta y_t\\ z_t\end{bmatrix}
$$

where $y_t$ is $I(1)$ (so its difference is used) and $z_t$ is stationary. In the original application $y_t$ = log real GNP and $z_t$ = the unemployment rate.

With structural shocks $\varepsilon_t = (\varepsilon_{1t},\varepsilon_{2t})'$, the **bivariate moving-average (BMA)** representation writes the variables as accumulated effects of current and past structural shocks:

$$
x_t = C(L)\varepsilon_t = \sum_{k=0}^\infty C_k\varepsilon_{t-k},
\qquad
C_k = \begin{bmatrix}c_{11}(k)&c_{12}(k)\\ c_{21}(k)&c_{22}(k)\end{bmatrix}
$$

Row by row:

$$
\Delta y_t = \sum_{k=0}^\infty c_{11}(k)\varepsilon_{1,t-k}+\sum_{k=0}^\infty c_{12}(k)\varepsilon_{2,t-k}
$$
$$
z_t = \sum_{k=0}^\infty c_{21}(k)\varepsilon_{1,t-k}+\sum_{k=0}^\infty c_{22}(k)\varepsilon_{2,t-k}
$$

**Interpretation:** $c_{ij}(k)$ = the effect of shock $j$ on variable $i$ after $k$ periods. So $c_{11}(0)$ is $\varepsilon_{1t}\to\Delta y_t$ immediately, $c_{11}(2)$ is $\varepsilon_{1t}\to\Delta y_{t+2}$, and the BMA describes the whole dynamic response path. **Main idea: a stationary VAR ⇒ an infinite MA representation.**

#### Four restrictions

With $\mathbb{E}\varepsilon_{1t}\varepsilon_{2t}=0$ and the normalisation $\mathrm{var}(\varepsilon_1)=\mathrm{var}(\varepsilon_2)=1$, the reduced-form residuals satisfy

$$
e_{1t} = c_{11}(0)\varepsilon_{1t}+c_{12}(0)\varepsilon_{2t},
\qquad
e_{2t} = c_{21}(0)\varepsilon_{1t}+c_{22}(0)\varepsilon_{2t}
$$

giving three moment conditions:

$$
\textbf{(1)}\quad \mathrm{var}(e_1) = c_{11}(0)^2+c_{12}(0)^2
$$
$$
\textbf{(2)}\quad \mathrm{var}(e_2) = c_{21}(0)^2+c_{22}(0)^2
$$
$$
\textbf{(3)}\quad \mathbb{E}(e_{1t}e_{2t}) = c_{11}(0)c_{21}(0)+c_{12}(0)c_{22}(0)
$$

**Three equations, four unknowns** — a fourth identifying restriction is still needed. **In Blanchard–Quah it comes from the long-run assumption that one structural shock has no long-run effect on $y_t$.**

#### Deriving the fourth restriction

Write the VAR as $x_t = A(L)Lx_t+e_t$, so $[1-A(L)L]x_t = e_t$ and $x_t = [1-A(L)L]^{-1}e_t$. With $D = \det[1-A(L)L]$, the inverse of the $2\times2$ matrix gives

$$
\begin{bmatrix}\Delta y_t\\ z_t\end{bmatrix}
= \frac1D\begin{bmatrix}1-A_{22}(L)L & A_{12}(L)L\\ A_{21}(L)L & 1-A_{11}(L)L\end{bmatrix}
\begin{bmatrix}e_{1t}\\ e_{2t}\end{bmatrix}
$$

so the first equation is

$$
\Delta y_t = \frac1D\left\{\left[1-\sum_{k=0}^\infty a_{22}(k)L^{k+1}\right]e_{1t}+\sum_{k=0}^\infty a_{12}(k)L^{k+1}e_{2t}\right\}
$$

Substituting $e_{1t}$ and $e_{2t}$ in terms of the structural shocks and requiring **the coefficient on $\varepsilon_{1t}$ to vanish in the long run** (set $L=1$):

$$
\boxed{\;\left[1-\sum_{k=0}^\infty a_{22}(k)\right]c_{11}(0)+\left[\sum_{k=0}^\infty a_{12}(k)\right]c_{21}(0) = 0\;}
\tag{Restriction 4}
$$

**$\{\varepsilon_{1t}\}$ then has only temporary effects on $\Delta y_t$, and hence on $y_t$.**

> [!important] Why "no long-run effect on $\Delta y$" means "no permanent effect on $y$"
> Because $y_t$ is $I(1)$, its **level** is the running sum of its differences. A shock with a *permanent* effect on the level of $y$ must have a **non-zero cumulative** effect on $\Delta y$; a shock whose cumulative effect on $\Delta y$ is zero moves $y$ temporarily and lets it return. So imposing $\sum_k c_{11}(k) = 0$ says: **$\varepsilon_1$ is a demand shock — it moves output temporarily but leaves its long-run path untouched.** $\varepsilon_2$, unrestricted, is then the supply/technology shock that *does* shift the long-run level.
>
> This is the entire economic content of Blanchard–Quah, and it is why the restriction is stated on the differenced variable but interpreted on the level.

#### The identification procedure

**Step 1 — preliminaries.**

- **Pretest** for time trends and unit roots. **If $\{y_t\}$ has no unit root, there is no reason to proceed** — the whole permanent/transitory distinction presupposes a stochastic trend.
- Transform both variables so they are $I(0)$.
- Perform **lag-length tests**; the VAR residuals must pass standard white-noise diagnostics.
- The reduced-form residuals $e_{1t},e_{2t}$ may still be correlated with each other — that is expected and is what identification resolves.

From the estimated VAR, compute

$$
\mathrm{var}(e_1),\quad \mathrm{var}(e_2),\quad \mathrm{cov}(e_1,e_2),
\qquad
1-\sum_{k=0}^pa_{22}(k),
\qquad
\sum_{k=0}^pa_{12}(k)
$$

**Step 2 — solve the four equations** for $c_{11}(0),c_{12}(0),c_{21}(0),c_{22}(0)$. Once the four impact coefficients are identified, the contemporaneous mapping from structural shocks to reduced-form residuals is fully pinned down.

**Step 3 — recover the shocks and analyse.** Inverting

$$
e_{1,t-j} = c_{11}(0)\varepsilon_{1,t-j}+c_{12}(0)\varepsilon_{2,t-j},
\qquad
e_{2,t-j} = c_{21}(0)\varepsilon_{1,t-j}+c_{22}(0)\varepsilon_{2,t-j}
$$

backs out the entire structural shock series period by period. These then give:

- **Impulse response functions**
- **Forecast error variance decompositions**
- **Historical decompositions**

**The key advantage is that the shocks now have a clear economic meaning** — Blanchard and Quah use the framework to obtain the response of the change in log real GNP to a typical **supply-side shock**.

> [!note] Historical decomposition — the most underused tool here
> Set all $\{\varepsilon_{1t}\}$ to zero and keep the actual $\{\varepsilon_{2t}\}$. Then the permanent changes in $\{y_t\}$ are
> $$\Delta y_t = \sum_{k=0}^\infty c_{12}(k)\varepsilon_{2,t-k}$$
> **isolating the contribution of the permanent structural disturbance.** This answers questions IRFs cannot: not "what would a typical shock do?" but "**what actually drove the 2008 recession?**" — decomposing the realised path into the contributions of each identified shock. It is the natural output of an SVAR and appears far too rarely in student work.

#### The three-way comparison

| | Short-run SVAR | Long-run SVAR / BQ | Cholesky |
|---|---|---|---|
| **Restricts** | Contemporaneous impact $P_{sr}=A^{-1}B$ | Cumulative effect $C(1)$ | $P_{sr}$, recursively |
| **Typical claim** | "$x$ does not react to $y$ within the period" | "$x$ has no permanent effect on $y$" | "an ordering of contemporaneous priority" |
| **Depends on data frequency?** | **Yes** — heavily | No | **Yes** |
| **Needs a unit root?** | No | **Yes** (in the level variable) | No |
| **Special case of** | — | — | Short-run SVAR with $A$ lower-triangular |

---

## ✏️ Exercises

### Exercise 1 — Count the restrictions

For $n=2,3,4,5$: how many distinct elements does $\Sigma$ have, how many unknowns are in $P_{sr}$, and how many restrictions are needed? Verify that Cholesky supplies exactly the right number.

> [!example]- Solution
> | $n$ | $\Sigma$: $\frac{n(n+1)}2$ | $P_{sr}$: $n^2$ | Restrictions needed: $\frac{n(n-1)}2$ | Cholesky zeros (above diagonal) |
> |---|---|---|---|---|
> | 2 | 3 | 4 | **1** | 1 ✓ |
> | 3 | 6 | 9 | **3** | 3 ✓ |
> | 4 | 10 | 16 | **6** | 6 ✓ |
> | 5 | 15 | 25 | **10** | 10 ✓ |
>
> **Cholesky always supplies exactly $n(n-1)/2$ zeros** — the number of entries strictly above the diagonal of an $n\times n$ matrix — so a recursive SVAR is always **exactly identified**: no more, no fewer.
>
> **Three regimes worth naming:**
> - **Under-identified** (fewer than $n(n-1)/2$ restrictions): infinitely many structural models fit; no unique IRFs.
> - **Exactly identified** ($=n(n-1)/2$): a unique solution, and the restrictions are **untestable** — they exhaust the available information, so there is nothing left over to check them against. **This is the uncomfortable truth about Cholesky:** you cannot test the ordering, only assume it.
> - **Over-identified** ($>n(n-1)/2$): the extra restrictions **are** testable, by a likelihood-ratio test comparing the restricted structural model against the unrestricted $\Sigma$, with $\chi^2$ degrees of freedom equal to the number of surplus restrictions.
>
> **Over-identification is a feature, not a bug.** It is the only way to get evidence for or against your identifying assumptions from the data.
>
> Note also how fast the burden grows: a 5-variable SVAR needs **10** theory-justified restrictions. Finding ten defensible claims about contemporaneous macroeconomic timing is genuinely hard, which is why large SVARs usually fall back on recursiveness or sign restrictions.

---

### Exercise 2 — Two orderings, two answers

For the residual data in §4 ($\Sigma = \begin{bmatrix}0.5&0.4\\0.4&0.5\end{bmatrix}$), compute the Cholesky factor $L$ (with $\Sigma=LL'$) under both orderings, give $\Theta_0 = L$ for each, and compute the share of $y$'s impact variance attributed to each shock.

> [!example]- Solution
> **Ordering A — $y$ first.** $\Sigma = LL'$ with $L$ lower triangular:
> $$\ell_{11} = \sqrt{0.5} = 0.7071,
> \quad
> \ell_{21} = \frac{0.4}{0.7071} = 0.5657,
> \quad
> \ell_{22} = \sqrt{0.5-0.5657^2} = \sqrt{0.18} = 0.4243$$
> $$L_A = \begin{bmatrix}0.7071&0\\ 0.5657&0.4243\end{bmatrix}$$
>
> **Ordering B — $z$ first.** Permute, factor, permute back; in original labelling the impact matrix is **upper** triangular:
> $$L_B = \begin{bmatrix}0.4243&0.5657\\ 0&0.7071\end{bmatrix}$$
> Check: $L_BL_B' = \begin{bmatrix}0.18+0.32 & 0.5657(0.7071)\\ \cdot & 0.5\end{bmatrix} = \begin{bmatrix}0.5&0.4\\0.4&0.5\end{bmatrix}$ ✓
>
> **Impact variance of $y$ (row 1), decomposed:**
>
> | Ordering | from shock 1 | from shock 2 | total |
> |---|---|---|---|
> | **A** ($y$ first) | $0.7071^2 = 0.50$ → **100%** | $0^2 = 0$ → **0%** | 0.50 |
> | **B** ($z$ first) | $0.4243^2 = 0.18$ → **36%** | $0.5657^2 = 0.32$ → **64%** | 0.50 |
>
> **On impact, $y$ is either 100% self-driven or 64% driven by $z$'s shock, depending purely on the ordering.** The total variance $0.50$ is invariant — it is the observed $\mathrm{var}(u_y)$ — but its attribution is entirely an artefact of the assumption.
>
> **Why it is this extreme here.** The residual correlation is $0.8$. The variable ordered first is credited with *all* of the shared variation; the one ordered second gets only the orthogonal residual. With $\rho = 0.8$, the shared part is $\rho^2 = 64\%$ of the variance — exactly the number in the table. **The share at stake is $\rho^2$**, which is a useful rule of thumb: with $\rho = 0.2$, only 4% is contested and the ordering scarcely matters; with $\rho = 0.8$, most of the answer is assumption.
>
> **What to do.** Report both. If the qualitative conclusion survives (e.g. "the response is positive and dies out within a year" holds either way), say so and proceed. If it does not, you have not identified anything — move to a theory-based short-run restriction, a long-run restriction, or sign restrictions.

---

### Exercise 3 — Design a short-run SVAR

You have a quarterly three-variable system: output growth $\Delta y_t$, inflation $\pi_t$, and the policy interest rate $i_t$. (a) How many restrictions do you need? (b) Propose a recursive identification and defend the ordering. (c) Propose one **non**-recursive restriction and explain what it buys.

> [!example]- Solution
> **(a)** $n=3$, so $n(n-1)/2 = \mathbf{3}$ restrictions.
>
> **(b) Recursive: order $(\Delta y_t,\;\pi_t,\;i_t)$.** This makes $A$ lower triangular:
> $$A = \begin{bmatrix}1&0&0\\ a_{21}&1&0\\ a_{31}&a_{32}&1\end{bmatrix}$$
> imposing exactly the three zeros above the diagonal.
>
> **The three assumptions, stated as economics:**
> 1. **Output does not respond within the quarter to inflation or to the interest rate.** Defence: production plans, investment projects and hiring take time; the standard "information/planning lag" argument, and the reason output is conventionally ordered first in monetary VARs (Christiano–Eichenbaum–Evans).
> 2. **Inflation does not respond within the quarter to the interest rate**, though it responds to output. Defence: price stickiness — menu costs and staggered contracts mean firms do not reprice within a quarter in response to a policy move.
> 3. **The interest rate responds to everything contemporaneously.** Defence: this is a **monetary policy reaction function** — the central bank observes current output and inflation (or good nowcasts of them) and sets rates accordingly. Ordering the policy instrument last is standard precisely so that the third structural shock can be read as a **monetary policy shock**: the part of the rate move not explained by the systematic response to $y$ and $\pi$.
>
> **The ordering is the standard slow-to-fast convention**, and it is defensible at quarterly frequency. At monthly or daily frequency assumption 1 becomes far less credible — output responds to a rate cut within three months more plausibly than within three days is irrelevant, but the point is that **the credibility of a short-run restriction depends on the data frequency**, and this ordering would not survive at daily frequency.
>
> **(c) A non-recursive restriction: a money-demand equation.** Suppose we replace $i_t$ with money growth $\Delta m_t$ and impose a theoretical money-demand relation with a *known* income elasticity of 1:
> $$\Delta m_t - \Delta y_t = \text{(other terms)}$$
> i.e. $a_{31} = -1$ rather than free. This is a **coefficient restriction** (§5) rather than a zero, and it is non-recursive because it does not correspond to any triangular ordering.
>
> **What it buys.** Two things. First, the restriction comes from theory with an explicit magnitude, not merely from a timing assumption — it is a stronger and more falsifiable claim. Second, **if you impose it *in addition to* two other restrictions you would have made anyway, the system becomes over-identified**, and the surplus restriction can be **tested** by a likelihood-ratio comparison against the unrestricted $\Sigma$ ($\chi^2$ with 1 degree of freedom). Under exact identification — the recursive scheme in (b) — no such test exists.
>
> **A third option worth mentioning:** impose **sign restrictions** instead. Require only that a contractionary monetary shock raises $i_t$, and lowers $\Delta y_t$ and $\pi_t$, for (say) four quarters. Far weaker and more defensible than any zero, but delivers a *set* of admissible IRFs rather than a single one.

---

### Exercise 4 — Long-run restriction by hand

A bivariate VAR(1) in $x_t = (\Delta y_t,\;z_t)'$ has
$$\hat\Phi = \begin{bmatrix}0.3&-0.2\\ 0.1&0.6\end{bmatrix},
\qquad
\hat\Sigma = \begin{bmatrix}0.8&0.3\\ 0.3&0.5\end{bmatrix}$$
Impose the Blanchard–Quah restriction that shock 2 has no long-run effect on $y$. (a) Compute $(I-\Phi)^{-1}$. (b) Find the required structure of $C(1)$. (c) Solve for $P_{sr}$. (d) Interpret.

> [!example]- Solution
> **(a)**
> $$I-\Phi = \begin{bmatrix}0.7&0.2\\ -0.1&0.4\end{bmatrix},
> \qquad
> \det = 0.28+0.02 = 0.30$$
> $$(I-\Phi)^{-1} = \frac{1}{0.30}\begin{bmatrix}0.4&-0.2\\ 0.1&0.7\end{bmatrix}
> = \begin{bmatrix}1.3333&-0.6667\\ 0.3333&2.3333\end{bmatrix}$$
>
> **(b)** The long-run impact matrix is $C(1) = (I-\Phi)^{-1}P_{sr}$. "Shock 2 has no long-run effect on $y$" means the cumulative response of $\Delta y$ to $\varepsilon_2$ is zero:
> $$C(1)_{12} = 0
> \qquad\Longrightarrow\qquad
> C(1) \text{ is \textbf{lower triangular}}$$
>
> **(c)** Combine the two conditions:
> $$C(1)C(1)' = (I-\Phi)^{-1}P_{sr}P_{sr}'\big[(I-\Phi)^{-1}\big]' = (I-\Phi)^{-1}\Sigma\big[(I-\Phi)^{-1}\big]'$$
> Call this $\Omega_{LR}$ — the **long-run covariance matrix**, computable entirely from reduced-form estimates:
> $$(I-\Phi)^{-1}\Sigma = \begin{bmatrix}1.3333&-0.6667\\0.3333&2.3333\end{bmatrix}\begin{bmatrix}0.8&0.3\\0.3&0.5\end{bmatrix}
> = \begin{bmatrix}0.8667&0.0667\\ 0.9667&1.2667\end{bmatrix}$$
> $$\Omega_{LR} = \begin{bmatrix}0.8667&0.0667\\0.9667&1.2667\end{bmatrix}\begin{bmatrix}1.3333&0.3333\\-0.6667&2.3333\end{bmatrix}
> = \begin{bmatrix}1.1111&0.4444\\ 0.4444&3.2778\end{bmatrix}$$
>
> Since $C(1)$ is lower triangular and $C(1)C(1)'=\Omega_{LR}$, **$C(1)$ is the Cholesky factor of $\Omega_{LR}$:**
> $$c_{11} = \sqrt{1.1111} = 1.0541,
> \quad
> c_{21} = \frac{0.4444}{1.0541} = 0.4216,
> \quad
> c_{22} = \sqrt{3.2778-0.1778} = \sqrt{3.1000} = 1.7607$$
> $$C(1) = \begin{bmatrix}1.0541&0\\ 0.4216&1.7607\end{bmatrix}$$
> Then recover the contemporaneous impact matrix:
> $$P_{sr} = (I-\Phi)\,C(1) = \begin{bmatrix}0.7&0.2\\-0.1&0.4\end{bmatrix}\begin{bmatrix}1.0541&0\\0.4216&1.7607\end{bmatrix}
> = \begin{bmatrix}0.8222&0.3521\\ 0.0632&0.7043\end{bmatrix}$$
> **Verify:** $P_{sr}P_{sr}' = \begin{bmatrix}0.6760+0.1240 & 0.0520+0.2480\\ \cdot & 0.0040+0.4960\end{bmatrix} = \begin{bmatrix}0.800&0.300\\0.300&0.500\end{bmatrix} = \Sigma$ ✓
>
> **(d) Interpretation.**
>
> **The key contrast with a Cholesky SVAR:** $P_{sr}$ is **not** triangular — $(P_{sr})_{12} = 0.3521 \neq 0$. **Shock 2 *does* affect $\Delta y$ on impact**, and quite substantially. What is zero is its *cumulative* effect: the shock moves output up initially and then the subsequent responses exactly cancel it out.
>
> That is precisely the intended economics. Under the BQ reading:
> - **$\varepsilon_1$ is the supply/technology shock** — the only one with a permanent effect on the level of $y$ ($C(1)_{11} = 1.0541$).
> - **$\varepsilon_2$ is the demand shock** — it moves output in the short run ($0.3521$ on impact) but its effect dies out completely ($C(1)_{12}=0$).
>
> **A short-run restriction could not deliver this.** Cholesky would have forced the *impact* effect to zero, which is exactly the wrong claim: demand shocks obviously move output immediately; the theoretical content is that they cannot move it *permanently*.
>
> **Practical note:** the procedure is "Cholesky, but applied to $\Omega_{LR}$ instead of $\Sigma$" — which is precisely what `statsmodels`' long-run SVAR code does (`P = inv(C_u_1) @ D` in the lecture's notebook, where `C_u_1` is $(I-\Phi)^{-1}$). Recognising it as a Cholesky-in-disguise makes the implementation obvious.

---

### Exercise 5 — Cholesky as a special case

Show that Cholesky identification is a short-run SVAR with a particular $A$ and $B$, and explain why $P_{sr}$ then equals the Cholesky factor of $\Sigma$.

> [!example]- Solution
> **The claim.** Take $A$ **lower triangular with unit diagonal** and $B$ **diagonal**:
> $$A = \begin{bmatrix}1&0&\cdots&0\\ a_{21}&1&\cdots&0\\ \vdots&\vdots&\ddots&\vdots\\ a_{n1}&a_{n2}&\cdots&1\end{bmatrix},
> \qquad
> B = \mathrm{diag}(b_{11},\ldots,b_{nn})$$
>
> **Step 1 — count.** $A$ has $n(n-1)/2$ free parameters below the diagonal; $B$ has $n$. Total $n(n-1)/2+n = n(n+1)/2$ — **exactly the number of distinct elements in $\Sigma$.** Exactly identified. ✓
>
> **Step 2 — the structure of $P_{sr}$.** $A$ is lower triangular with unit diagonal, so $A^{-1}$ is also **lower triangular with unit diagonal** (the inverse of a unit lower-triangular matrix is unit lower-triangular). Multiplying by a diagonal $B$ on the right scales the columns and preserves triangularity:
> $$P_{sr} = A^{-1}B \quad\text{is lower triangular, with diagonal } (b_{11},\ldots,b_{nn})$$
>
> **Step 3 — uniqueness.** We require $\Sigma = P_{sr}P_{sr}'$ with $P_{sr}$ lower triangular. **The Cholesky decomposition theorem** says: for a symmetric positive-definite $\Sigma$, there is a **unique** lower-triangular $L$ with positive diagonal such that $\Sigma = LL'$. Imposing $b_{ii}>0$ (a harmless normalisation — it just fixes each structural shock's sign so that a "positive shock" means positive), we get
> $$\boxed{\;P_{sr} = L,\;\text{the Cholesky factor of }\Sigma\;}$$
>
> **Step 4 — recover $A$ and $B$ separately.** $B = \mathrm{diag}(L)$ and $A = B L^{-1}$… more simply, $A^{-1} = LB^{-1}$, i.e. $L$ with each column divided by its diagonal entry, which is unit lower-triangular as required. ✓
>
> **Why this matters conceptually.** Cholesky is not a neutral statistical operation that happens to produce orthogonal shocks. **It is the short-run SVAR whose restrictions are: "variable $i$ does not respond contemporaneously to any shock $j>i$."** Writing it as an $A$ matrix makes the assumptions visible; calling it "a Cholesky decomposition" hides them behind linear algebra.
>
> **Two consequences worth stating:**
> 1. **Exact identification means the restrictions are untestable.** You have used up every degree of freedom in $\Sigma$; nothing is left to check the ordering against. Any claim that "the Cholesky results confirm the ordering" is empty.
> 2. **The $n!$ orderings give $n!$ different exactly-identified models, all fitting $\Sigma$ perfectly.** The data cannot choose among them. Only theory can — which is the entire message of this chapter, and a fitting note on which to end the subject.

---

## 📝 Summary

- **The identification problem:** the reduced-form VAR delivers $\Sigma$ with $n(n+1)/2$ distinct elements, but $P_{sr}$ has $n^2$ unknowns. Since $\Sigma = PP' = (PQ)(PQ)'$ for any orthogonal $Q$, **the data pin $P$ down only up to a rotation.** Economic theory must supply $n(n-1)/2$ restrictions.
- **Reduced-form residuals $u_t$ are mixtures of structural shocks** and have no automatic economic meaning. SVAR recovers orthogonal, interpretable $\varepsilon_t$ with $\mathbb{E}(\varepsilon_t\varepsilon_t')=I$ via $u_t = P_{sr}\varepsilon_t$.
- **Short-run SVAR (AB model):** $Au_t = B\varepsilon_t$, giving $P_{sr}=A^{-1}B$, $A\Sigma A' = BB'$, and $\Sigma = P_{sr}P_{sr}'$. Structural IRFs are $\Theta_s^{sr} = \Phi_sA^{-1}B$ — **reduced-form dynamics times the structural impact matrix**, so all identifying content lives in one $n\times n$ matrix.
- **Order condition:** at least $2n^2-\tfrac{n(n+1)}2$ restrictions on $(A,B)$, or equivalently $\tfrac{n(n-1)}2$ after normalising $A$'s diagonal and $B$. Necessary but not sufficient — check local identification (Amisano–Giannini 1997).
- **Cholesky is a recursive short-run SVAR** with $A$ unit-lower-triangular and $B$ diagonal, supplying exactly $\tfrac{n(n-1)}2$ zeros, so it is **exactly identified — and therefore untestable**. Its results depend entirely on the ordering; the contested share of the impact variance is $\rho^2$, the squared residual correlation.
- **Alternatives to Cholesky:** coefficient, variance, symmetry and sign restrictions. Over-identifying restrictions are **testable** by likelihood ratio, which is the only way to get evidence about identification from data.
- **Long-run SVAR:** restrict $C(1) = \big(I-\sum_iA_i\big)^{-1}A^{-1}B$, the **cumulative** effect matrix. Long-run restrictions are frequency-independent and often more theoretically defensible than contemporaneous ones.
- **Blanchard–Quah:** with $x_t=(\Delta y_t,z_t)'$ and $y_t\sim I(1)$, three moment conditions plus the restriction that $\varepsilon_1$ has **no long-run effect on $y$** identify the four impact coefficients. In practice, $C(1)$ is the Cholesky factor of $\Omega_{LR} = (I-\Phi)^{-1}\Sigma[(I-\Phi)^{-1}]'$, and $P_{sr} = (I-\Phi)C(1)$ — generally **not** triangular, so demand shocks can move output on impact while leaving it unchanged in the long run.
- Identified shocks support **IRFs, FEVDs and historical decompositions** — the last being the tool that says what actually drove a particular episode, not merely what a typical shock does.

---

## ⚠️ Important Notes

> [!warning] $P$ is defined in two opposite directions in this lecture
> §2 defines $P_{sr} = A^{-1}B$ with $u_t = P_{sr}\varepsilon_t$ — **shocks to residuals**. The worked example in §4 writes $\varepsilon_t = P_{SR}u_t$ — **residuals to shocks**, i.e. the *inverse* matrix. The slides use both without flagging the switch, and the capitalisation ($P_{sr}$ vs $P_{SR}$) is the only clue.
>
> **How to tell them apart:** if the matrix has 1's on the diagonal it is the $\varepsilon = Pu$ direction; if its diagonal entries are the shock standard deviations it is the $u = P\varepsilon$ direction. Check before interpreting any coefficient.

> [!warning] The order condition is necessary, not sufficient
> Counting $n(n-1)/2$ restrictions is not enough — they must also be *placed* so that the system is locally identified. A classic failure: imposing two zeros in the same row of $A$ in a 3-variable system leaves another parameter unidentified even though the count is right. **Use software that checks the rank condition** (`statsmodels`' `SVAR` will fail to converge or return a singular Hessian), and consult Amisano–Giannini for the formal criterion.

> [!warning] Exactly-identified restrictions cannot be tested
> This is the most important practical caveat in the chapter. Under exact identification the structural model reproduces $\Sigma$ perfectly *by construction*, so goodness of fit says nothing about whether the ordering is right. **A well-fitting recursive SVAR is not evidence for its ordering.** Only over-identifying restrictions generate testable implications.

> [!tip] Report robustness, always
> The minimum standard for credible SVAR work:
> 1. State the identifying assumptions **as economics**, in words, before showing any output.
> 2. Report the **residual correlation matrix** — it tells the reader how much is at stake.
> 3. Show IRFs under **at least two orderings** (or two identification schemes).
> 4. Report **confidence bands** (bootstrapped — asymptotic bands are unreliable for IRFs at long horizons).
> 5. If the qualitative conclusion is not robust, **say so** rather than picking the ordering that gives the desired answer.

> [!note] Short-run vs long-run — which to choose
> - **Short-run restrictions** are natural when the timing argument is strong: information lags, price stickiness, or an institutional decision sequence. They are frequency-dependent — an assumption that is credible quarterly may be absurd daily.
> - **Long-run restrictions** are natural when theory speaks about *permanent* effects: long-run money neutrality, demand shocks not shifting potential output, purchasing power parity. They require a genuine unit root in the level variable and are frequency-independent.
> - **Sign restrictions** are natural when theory gives directions but not magnitudes — increasingly the default in modern macro.
>
> The three are combinable, and combining them typically produces over-identification, which is desirable.

> [!warning] Long-run restrictions have a known weakness
> $C(1) = \big(I-\sum_iA_i\big)^{-1}P_{sr}$ requires estimating the **infinite** cumulative sum, which depends on $\big(I-\sum\hat A_i\big)^{-1}$. When the system is near a unit root, that inverse is near-singular and its estimate is very imprecise. **Long-run identified IRFs can have enormous sampling uncertainty** — the well-known Faust–Leeper (1997) critique of Blanchard–Quah-style identification. Bootstrapped bands are essential, and if they are wide, say so.

> [!note] Where the whole subject lands
> This chapter closes a loop opened in [[03 - Stationarity and Difference Equations]]. There, a dynamic multiplier $\partial y_{t+j}/\partial w_t$ was a well-defined derivative because there was only one shock. In a multivariate system that derivative is **not well defined** until you say what "holding the other shocks constant" means — and the data cannot tell you.
>
> **Statistics gives you dynamics; economics gives you causation.** Every model in this subject computes dynamics honestly. Only the identifying assumptions — stated, defended, and tested where possible — turn them into claims about the world.

> [!warning] Gaps in the source slides
> - **Cholesky Case 1 is missing.** The example jumps from setting up the identification problem straight to "Cholesky Case 2: setting $p_{21}=0$", with no Case 1 slide. I have worked Case 1 out in §4 ($p_{12}=0 \Rightarrow p_{21}=-0.8$, giving a *sign-flipped* $\varepsilon_z$ series) because the whole point of the example — that ordering matters — cannot be seen from one case alone.
> - **No numerical long-run / Blanchard–Quah example.** The BQ algebra is derived in full but never applied to numbers; the code cells load `m1gdp.dta` from Stata Press and their output is not saved. Exercise 4 is my own construction to fill this.
> - **All data files are external and their outputs unsaved.** `lutkepohl2.dta` and `m1gdp.dta` are fetched from `stata-press.com` at runtime — so they are at least *reproducible*, unlike the missing local files of chapters 7–9 — but **no results, figures or IRF plots are stored in the notebook.** Nothing from the applied sections can be checked as written.
> - **FEVD appears on the title slide and is never covered.** The lecture promises "Forecast Error Variance Decomposition" among its topics; no slide derives or computes a *structural* FEVD. The reduced-form version is in [[07 - SARIMA and Vector Autoregression]]; the structural version is the same formula with $\Phi_s$ replaced by $\Theta_s^{sr}$.
> - **Sign restrictions are listed and not explained.** One bullet ("A sign restriction imposes the expected direction of responses") for what is now the dominant identification approach in applied macro.
> - **No confidence bands anywhere.** IRFs are presented as point estimates throughout, with no mention of bootstrap inference — a serious omission, since SVAR IRFs routinely have bands wide enough to include zero.
> - **The two restriction-counting slides use different set-ups** without saying so: one counts $2n^2$ parameters in the general AB model, the other $n^2-n$ after normalising. Both are correct; the transition is unexplained and reads as a contradiction. §3 disentangles them.
> - **HTML extraction truncated every inline `<`**, though this deck suffered less than the others. One code comment is in Vietnamese (`Chọn biến` — *select variables*).
> - **No exercises are provided.** All five above are my own construction.

---

**Previous:** [[09 - ARCH, GARCH and Extensions]] · **Index:** [[00-Index]]

#time-series #svar #identification #blanchard-quah #irf #fevd #cholesky #causality
