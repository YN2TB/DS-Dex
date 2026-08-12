---
subject: Optimization
chapter: 08
tags: [ds, optimization, least-squares, normal-equations, pseudoinverse, recursive-least-squares, kaczmarz, condition-number, qr-decomposition]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 12"
---

# Least Squares and Linear Equations

> [!abstract] What this chapter is for
> **This is the one optimization problem with a closed-form answer, and it is also the most-solved problem in data science.** Every regression, every projection, every "fit a model by minimising squared error" is this chapter.
>
> $$\text{Overdetermined }(m>n):\quad \min_{\mathbf x}\lVert A\mathbf x-\mathbf b\rVert^2\ \Longrightarrow\ \boxed{\mathbf x^*=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b}$$
> $$\text{Underdetermined }(m<n):\quad \min\lVert\mathbf x\rVert\ \text{s.t.}\ A\mathbf x=\mathbf b\ \Longrightarrow\ \boxed{\mathbf x^*=A^{\mathsf T}(AA^{\mathsf T})^{-1}\mathbf b}$$
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1–2** | The normal equations and their geometry | **Least squares is orthogonal projection** onto $\mathcal R(A)$ |
> | **3** | The underdetermined case | The **pseudoinverse**, and $p>n$ regression |
> | **4** | **Never form $A^{\mathsf T}A$** | $\kappa(A^{\mathsf T}A)=\kappa(A)^2$ — **QR or SVD instead** |
> | **5** | **Recursive least squares** | Update the fit as data arrives — **the ancestor of online learning** |
> | **6** | **Kaczmarz's algorithm** | One equation at a time — **the ancestor of SGD** |
> | **7** | Regularised least squares | Ridge, and the complete picture |
>
> **§4 is the one that will save you.** The formula in the box above is the right *mathematics* and the wrong *algorithm*, and Exercise 5 exhibits a $3\times2$ problem where it fails outright in double precision.

---

## 📘 Main Knowledge

### 1. The overdetermined problem and the normal equations

Consider $A\mathbf x=\mathbf b$ with $A\in\mathbb R^{m\times n}$, **$m>n$** (more equations than unknowns) and $\operatorname{rank}A=n$ (full column rank).

**If $\mathbf b\notin\mathcal R(A)$ the system is inconsistent** — no exact solution exists. So instead ask for the $\mathbf x$ minimising the residual:

$$\min_{\mathbf x\in\mathbb R^n}\ \lVert A\mathbf x-\mathbf b\rVert^2$$

> [!important] Lemma 12.1
> For $A\in\mathbb R^{m\times n}$ with $m\ge n$: $\ \operatorname{rank}A=n\iff\operatorname{rank}A^{\mathsf T}A=n$, i.e. $A^{\mathsf T}A$ is invertible.
>
> **Proof.** ($\Rightarrow$) If $A^{\mathsf T}A\mathbf x=\mathbf 0$ then $\lVert A\mathbf x\rVert^2=\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=0$, so $A\mathbf x=\mathbf 0$, so $\mathbf x=\mathbf 0$ by full rank. ($\Leftarrow$) If $A\mathbf x=\mathbf 0$ then $A^{\mathsf T}A\mathbf x=\mathbf 0$, so $\mathbf x=\mathbf 0$. $\blacksquare$
>
> **The identity $\lVert A\mathbf x\rVert^2=\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x$ is the whole proof, and it is used again in §4 and §7.**

> [!important] Theorem 12.1 — the normal equations
> The unique minimiser of $\lVert A\mathbf x-\mathbf b\rVert^2$ solves
> $$A^{\mathsf T}A\,\mathbf x=A^{\mathsf T}\mathbf b\qquad\text{(the \textbf{normal equations})}$$
> so $\mathbf x^*=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$.
>
> **Proof (the completion-of-squares one).** With $\mathbf x^*=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$,
> $$\lVert A\mathbf x-\mathbf b\rVert^2=\lVert A(\mathbf x-\mathbf x^*)\rVert^2+\lVert A\mathbf x^*-\mathbf b\rVert^2+2\big[A(\mathbf x-\mathbf x^*)\big]^{\mathsf T}(A\mathbf x^*-\mathbf b)$$
> and the cross term vanishes:
> $$(\mathbf x-\mathbf x^*)^{\mathsf T}A^{\mathsf T}\big[A(A^{\mathsf T}A)^{-1}A^{\mathsf T}-I\big]\mathbf b=(\mathbf x-\mathbf x^*)^{\mathsf T}\big[A^{\mathsf T}-A^{\mathsf T}\big]\mathbf b=0$$
> Hence $\lVert A\mathbf x-\mathbf b\rVert^2=\lVert A(\mathbf x-\mathbf x^*)\rVert^2+\lVert A\mathbf x^*-\mathbf b\rVert^2>\lVert A\mathbf x^*-\mathbf b\rVert^2$ for $\mathbf x\ne\mathbf x^*$. $\blacksquare$

> [!note] The optimization proof is shorter, and it is the one this subject is about
> $$f(\mathbf x)=\lVert A\mathbf x-\mathbf b\rVert^2=\tfrac12\mathbf x^{\mathsf T}\big(2A^{\mathsf T}A\big)\mathbf x-\mathbf x^{\mathsf T}\big(2A^{\mathsf T}\mathbf b\big)+\mathbf b^{\mathsf T}\mathbf b$$
> **A quadratic with Hessian $2A^{\mathsf T}A\succ0$**, hence strictly convex ([[02 - Convex Sets and Convex Functions|ch. 02]]). The FONC $\nabla f=2A^{\mathsf T}A\mathbf x-2A^{\mathsf T}\mathbf b=\mathbf 0$ is therefore **necessary and sufficient**, and its unique solution is $\mathbf x^*$. $\blacksquare$
>
> **So least squares is exactly the quadratic minimisation of chapters 05–07, with $Q=2A^{\mathsf T}A$** — which is why $\kappa(A^{\mathsf T}A)$ has already appeared twice and will appear again in §4.

---

### 2. The geometry: least squares is orthogonal projection

The columns of $A$ span $\mathcal R(A)$, an $n$-dimensional subspace of $\mathbb R^m$. **The problem is: find the point of $\mathcal R(A)$ closest to $\mathbf b$.**

> [!important] Proposition 12.1
> Let $\mathbf h\in\mathcal R(A)$ be such that $\mathbf h-\mathbf b\perp\mathcal R(A)$. Then
> $$\mathbf h=A\mathbf x^*=\underbrace{A(A^{\mathsf T}A)^{-1}A^{\mathsf T}}_{\textbf{the orthogonal projector }P}\mathbf b$$
>
> **Proof.** $\mathbf h=\sum_ix_i\mathbf a_i$, and orthogonality to each column gives $\langle\mathbf h,\mathbf a_i\rangle=\langle\mathbf b,\mathbf a_i\rangle$ for all $i$, i.e. the $n\times n$ system
> $$\begin{pmatrix}\langle\mathbf a_1,\mathbf a_1\rangle&\cdots&\langle\mathbf a_n,\mathbf a_1\rangle\\ \vdots&&\vdots\\ \langle\mathbf a_1,\mathbf a_n\rangle&\cdots&\langle\mathbf a_n,\mathbf a_n\rangle\end{pmatrix}\mathbf x=\begin{pmatrix}\langle\mathbf b,\mathbf a_1\rangle\\ \vdots\\ \langle\mathbf b,\mathbf a_n\rangle\end{pmatrix}$$
> **which is exactly $A^{\mathsf T}A\mathbf x=A^{\mathsf T}\mathbf b$.** The matrix on the left is the **Gram matrix**. $\blacksquare$

> [!important] The three statements are one statement
> $$\underbrace{\mathbf x^*\ \text{minimises}\ \lVert A\mathbf x-\mathbf b\rVert}_{\textbf{optimization}}\iff \underbrace{A^{\mathsf T}(A\mathbf x^*-\mathbf b)=\mathbf 0}_{\textbf{algebra: normal equations}}\iff \underbrace{A\mathbf x^*-\mathbf b\perp\mathcal R(A)}_{\textbf{geometry: residual}\perp\textbf{columns}}$$
>
> **The middle one *is* $\nabla f=\mathbf 0$, and it *is* the orthogonality statement.** Reading $A^{\mathsf T}\mathbf e=\mathbf 0$ as "the residual is orthogonal to every column of $A$" is the most useful sentence in the chapter — it explains why OLS residuals are uncorrelated with every regressor, which [[Econometrics/contents/00-Index|Econometrics]] states as a property of OLS and which is really just the FONC.

**Projectors** (§12.1 continued):
$$P_{\mathcal R(A)}=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}\quad(m>n)\qquad\qquad P_{\mathcal N(A)}=I-A^{\mathsf T}(AA^{\mathsf T})^{-1}A\quad(m<n)$$
In statistics $P_{\mathcal R(A)}$ is the **hat matrix** $H=X(X^{\mathsf T}X)^{-1}X^{\mathsf T}$, because $\hat{\mathbf y}=H\mathbf y$.

> [!example]- Worked example — line fitting (C&Ż 12.2), verified
> Fit $y=mt+c$ to $(2,3)$, $(3,4)$, $(4,15)$. With $A=\begin{psmallmatrix}2&1\\3&1\\4&1\end{psmallmatrix}$ and $\mathbf b=(3,4,15)^{\mathsf T}$:
> $$A^{\mathsf T}A=\begin{pmatrix}29&9\\9&3\end{pmatrix},\quad \det=6,\quad A^{\mathsf T}\mathbf b=\begin{pmatrix}78\\22\end{pmatrix}\ \Longrightarrow\ \boxed{m^*=6,\ \ c^*=-\tfrac{32}{3}}$$
> **Check the geometry:** $\mathbf e=A\mathbf x^*-\mathbf b=\left(-\tfrac53,\ \tfrac{10}3,\ -\tfrac53\right)^{\mathsf T}$, and $A^{\mathsf T}\mathbf e=\mathbf 0$ exactly ✔ — the residual is orthogonal to both columns.
>
> *(Note $\operatorname{rank}A=2<\operatorname{rank}[A\,|\,\mathbf b]=3$, confirming $\mathbf b\notin\mathcal R(A)$ and the system is inconsistent — which is why we are minimising rather than solving.)*

---

### 3. The underdetermined case and the pseudoinverse

Now take $A\in\mathbb R^{m\times n}$ with **$m<n$** and $\operatorname{rank}A=m$: **fewer equations than unknowns**, so infinitely many exact solutions. Pick the smallest:

$$\min\ \lVert\mathbf x\rVert\quad\text{subject to}\quad A\mathbf x=\mathbf b$$

> [!important] Theorem 12.2
> The unique minimum-norm solution is
> $$\mathbf x^*=A^{\mathsf T}(AA^{\mathsf T})^{-1}\mathbf b$$
>
> **Proof.** For any feasible $\mathbf x$, $\lVert\mathbf x\rVert^2=\lVert\mathbf x-\mathbf x^*\rVert^2+\lVert\mathbf x^*\rVert^2+2\mathbf x^{*\mathsf T}(\mathbf x-\mathbf x^*)$, and the cross term is
> $$\mathbf b^{\mathsf T}(AA^{\mathsf T})^{-1}\big[A\mathbf x-(AA^{\mathsf T})(AA^{\mathsf T})^{-1}\mathbf b\big]=\mathbf b^{\mathsf T}(AA^{\mathsf T})^{-1}[\mathbf b-\mathbf b]=0$$
> so $\lVert\mathbf x\rVert^2=\lVert\mathbf x-\mathbf x^*\rVert^2+\lVert\mathbf x^*\rVert^2>\lVert\mathbf x^*\rVert^2$ unless $\mathbf x=\mathbf x^*$. $\blacksquare$
>
> **Note the proof is the *same* proof as Theorem 12.1** with the roles of $A$ and $A^{\mathsf T}$ swapped — the two cases are dual.

> [!important] Both formulas are the **pseudoinverse**
> $$A^+=\begin{cases}(A^{\mathsf T}A)^{-1}A^{\mathsf T}&m>n,\ \operatorname{rank}A=n\quad\text{(left inverse)}\\[4pt] A^{\mathsf T}(AA^{\mathsf T})^{-1}&m<n,\ \operatorname{rank}A=m\quad\text{(right inverse)}\end{cases}$$
> and in **both** cases $\mathbf x^*=A^+\mathbf b$. **The general definition, valid for any $A$ of any rank, is via the SVD:** if $A=U\Sigma V^{\mathsf T}$ then $A^+=V\Sigma^+U^{\mathsf T}$ with $\Sigma^+$ obtained by inverting the non-zero singular values.
>
> **This is the object [[Linear Algebra/contents/00-Index|the Linear Algebra notes flag as absent from Nicholson]]** — the SVD is what unifies these two formulas, handles rank-deficient $A$, and is what a numerical library actually computes.

> [!note] Why $p>n$ regression lands here
> With more features than observations, $X\in\mathbb R^{n\times p}$ with $p>n$, **OLS has infinitely many solutions** ([[02 - Convex Sets and Convex Functions|ch. 02]] Exercise 4). $\mathbf x^*=X^+\mathbf y$ picks the **minimum-norm** one — and that is exactly what gradient descent from $\boldsymbol\beta_0=\mathbf 0$ converges to, since every gradient lies in $\mathcal R(X^{\mathsf T})$.
>
> **This is the cleanest example of "implicit regularisation": the algorithm chooses among the optima, and the choice it makes is a minimum-norm one.**

---

### 4. **Never form the normal equations**

> [!warning] The single most important practical fact in this chapter
> $$\boxed{\kappa\big(A^{\mathsf T}A\big)=\kappa(A)^2}$$
> because the eigenvalues of $A^{\mathsf T}A$ are the **squares of the singular values** of $A$.
>
> **Forming $A^{\mathsf T}A$ squares the condition number and therefore halves the number of correct digits.** With $\kappa(A)=10^8$ — unremarkable for a design matrix with correlated features — $\kappa(A^{\mathsf T}A)=10^{16}$, which exceeds the reciprocal of double precision. **The matrix is then numerically singular even though the problem is perfectly well posed.**

> [!example]- The failure is not hypothetical — a $3\times2$ example
> **Läuchli's matrix** with $\varepsilon=10^{-8}$:
> $$A=\begin{pmatrix}1&1\\ \varepsilon&0\\ 0&\varepsilon\end{pmatrix},\qquad \mathbf b=\begin{pmatrix}2\\ \varepsilon\\ \varepsilon\end{pmatrix},\qquad\text{exact solution }\mathbf x^*=(1,1)^{\mathsf T}$$
> $$\kappa(A)=1.41\times10^8\qquad\kappa(A^{\mathsf T}A)=5.96\times10^{16}\qquad\varepsilon_{\text{mach}}=2.2\times10^{-16}$$
> **In double precision $1+\varepsilon^2$ rounds to $1$, so**
> $$A^{\mathsf T}A=\begin{pmatrix}1+\varepsilon^2&1\\1&1+\varepsilon^2\end{pmatrix}\ \longrightarrow\ \begin{pmatrix}1&1\\1&1\end{pmatrix}\quad\textbf{singular}$$
>
> | Method | Result |
> |---|---|
> | **Normal equations** | **`LinAlgError: Singular matrix` — it does not merely lose accuracy, it fails** |
> | **QR** | $(1,\ 1)$ — error $0$ |
> | **SVD (`lstsq`)** | $(1,\ 1)$ — error $5\times10^{-16}$ |
>
> *(All verified.)*

> [!important] What to do instead
> | Method | Cost | Works up to |
> |---|---|---|
> | Normal equations + Cholesky | $mn^2+\tfrac13n^3$ | $\kappa(A)\lesssim10^{8}$ |
> | **QR (Householder)** | $2mn^2-\tfrac23n^3$ | $\kappa(A)\lesssim10^{16}$ |
> | **SVD** | $\sim2mn^2+11n^3$ | any $\kappa$, **any rank** |
>
> **QR:** write $A=QR$ with $Q$ orthonormal and $R$ upper triangular. Then $\lVert A\mathbf x-\mathbf b\rVert=\lVert R\mathbf x-Q^{\mathsf T}\mathbf b\rVert$ **because orthogonal maps preserve norms**, and $R\mathbf x=Q^{\mathsf T}\mathbf b$ is a triangular back-substitution. **$A^{\mathsf T}A$ is never formed, so $\kappa$ is never squared.**
>
> **QR costs roughly twice the normal equations and buys eight digits.** *(`numpy.linalg.lstsq`, `scipy.linalg.lstsq`, R's `lm()` and every serious library use QR or SVD. If you have written `inv(X.T @ X) @ X.T @ y`, replace it with `np.linalg.lstsq(X, y)`.)*

> [!note] The same fact, three times in this subject
> - **Here:** don't square $\kappa$ by forming $A^{\mathsf T}A$.
> - **[[05 - Gradient Methods|Ch. 05]]:** gradient descent on $\lVert A\mathbf x-\mathbf b\rVert^2$ takes $O(\kappa(A)^2)$ iterations, because the Hessian is $A^{\mathsf T}A$.
> - **[[07 - Conjugate Direction Methods|Ch. 07]]:** CG on the normal equations takes $O(\kappa(A))$ iterations. **LSQR** is the variant that works with $A$ directly and never squares anything — the right iterative method for large sparse least squares.
>
> **Polynomial fitting makes the point vividly:** for a Vandermonde matrix on 30 points, $\kappa$ goes $1.1\times10^2$ (degree 3), $1.9\times10^4$ (degree 6), $3.5\times10^6$ (degree 9), $7.5\times10^8$ (degree 12) — and **$\kappa(V^{\mathsf T}V)$ is the square of each**, hitting $10^{17}$ by degree 12. *(Verified; the ratio $\kappa(V^{\mathsf T}V)/\kappa(V)^2$ is exactly $1.000$ until it exceeds machine precision.)* **This is why polynomial regression uses orthogonal polynomials.**

---

### 5. Recursive least squares — updating a fit as data arrives

**Given a fit to $m$ data points, a new point arrives. Refitting from scratch costs $O(mn^2)$. Updating costs $O(n^2)$.**

Let $G_k=\sum_{i\le k}A_i^{\mathsf T}A_i$ be the accumulated Gram matrix. From $\mathbf x^{(0)}=G_0^{-1}A_0^{\mathsf T}\mathbf b^{(0)}$ and new data $(A_1,\mathbf b^{(1)})$:

$$G_1=G_0+A_1^{\mathsf T}A_1,\qquad A_0^{\mathsf T}\mathbf b^{(0)}=G_0\mathbf x^{(0)}=\big(G_1-A_1^{\mathsf T}A_1\big)\mathbf x^{(0)}$$

and substituting into $\mathbf x^{(1)}=G_1^{-1}\left[A_0^{\mathsf T}\mathbf b^{(0)}+A_1^{\mathsf T}\mathbf b^{(1)}\right]$ gives the **update form**:

> [!important] The RLS algorithm
> $$G_{k+1}=G_k+A_{k+1}^{\mathsf T}A_{k+1}$$
> $$\mathbf x^{(k+1)}=\mathbf x^{(k)}+G_{k+1}^{-1}A_{k+1}^{\mathsf T}\underbrace{\big(\mathbf b^{(k+1)}-A_{k+1}\mathbf x^{(k)}\big)}_{\textbf{the innovation}}$$
>
> **If the new data agree with the old fit, the innovation is zero and nothing changes.** The correction is proportional to how surprising the new observation is.

**To avoid inverting $G_{k+1}$ each step, propagate $P_k=G_k^{-1}$ directly** via the **Sherman–Morrison–Woodbury** formula
$$(A+UV)^{-1}=A^{-1}-(A^{-1}U)(I+VA^{-1}U)^{-1}(VA^{-1})$$

giving, for a **single new row** $\mathbf a_{k+1}^{\mathsf T}$ and scalar $b_{k+1}$:

$$\boxed{P_{k+1}=P_k-\frac{P_k\mathbf a_{k+1}\mathbf a_{k+1}^{\mathsf T}P_k}{1+\mathbf a_{k+1}^{\mathsf T}P_k\mathbf a_{k+1}}},\qquad \mathbf x^{(k+1)}=\mathbf x^{(k)}+P_{k+1}\mathbf a_{k+1}\big(b_{k+1}-\mathbf a_{k+1}^{\mathsf T}\mathbf x^{(k)}\big)$$

**Cost per observation: $O(n^2)$, with no matrix inversion and no need to store past data.**

> [!important] What RLS is, in modern language
> **It is the exact online least-squares learner**, and it is the ancestor of a family:
>
> | RLS | Descendant |
> |---|---|
> | innovation $b-\mathbf a^{\mathsf T}\mathbf x$ | prediction error / residual |
> | gain $P_{k+1}\mathbf a_{k+1}$ | learning rate, **but adaptive and per-direction** |
> | $P_k=G_k^{-1}$ | the inverse covariance of the estimate |
> | Sherman–Morrison update | the **Kalman filter's** covariance update — RLS *is* the Kalman filter for a static state |
> | forgetting factor $\lambda$ ($G_{k+1}=\lambda G_k+\mathbf a\mathbf a^{\mathsf T}$) | exponential moving average, concept drift |
>
> **Note the resemblance to [[06 - Newton and Quasi-Newton Methods|ch. 06]]:** $P_k$ is a running inverse-Hessian, updated by a rank-one correction with Sherman–Morrison. **RLS is a quasi-Newton method for a problem whose Hessian happens to be exactly known.**

---

### 6. Kaczmarz's algorithm — one equation at a time

**For $A\mathbf x=\mathbf b$ with $m<n$ (consistent, underdetermined), cycle through the rows:**

$$\mathbf x^{(k+1)}=\mathbf x^{(k)}+\mu\,\frac{b_{i}-\mathbf a_{i}^{\mathsf T}\mathbf x^{(k)}}{\mathbf a_{i}^{\mathsf T}\mathbf a_{i}}\,\mathbf a_{i},\qquad i=(k\bmod m)+1$$

**Geometrically: project the current iterate onto the hyperplane $\{\mathbf x:\mathbf a_i^{\mathsf T}\mathbf x=b_i\}$** (exactly, when $\mu=1$), then move to the next hyperplane and repeat.

> [!important] Theorem 12.3
> If $0<\mu<2$ and $\mathbf x^{(0)}=\mathbf 0$, then $\mathbf x^{(k)}\to A^{\mathsf T}(AA^{\mathsf T})^{-1}\mathbf b$ — **the minimum-norm solution.**
>
> **The key inequality in the proof:**
> $$\lVert\mathbf x^{(k+1)}-\mathbf x^*\rVert^2=\lVert\mathbf x^{(k)}-\mathbf x^*\rVert^2-\mu(2-\mu)\big(\mathbf a_{i}^{\mathsf T}(\mathbf x^{(k)}-\mathbf x^*)\big)^2$$
> **The subtracted term is non-negative exactly when $0<\mu<2$**, so the distance to $\mathbf x^*$ is non-increasing — a monotone bounded sequence, hence convergent. Summing shows $\sum_k\big(\mathbf a_i^{\mathsf T}(\mathbf x^{(k)}-\mathbf x^*)\big)^2<\infty$, so each row's residual $\to0$; a Bolzano–Weierstrass argument then identifies the limit.
>
> **The condition $0<\mu<2$ is exactly [[05 - Gradient Methods|ch. 05]] §4's step-size condition in disguise** — the same "$2$" appears for the same reason.
>
> **If $\mathbf x^{(0)}\ne\mathbf 0$ the limit is the feasible point closest to $\mathbf x^{(0)}$** — the algorithm's starting point determines which solution it finds. *Implicit regularisation again.*

> [!important] Kaczmarz is stochastic gradient descent
> Minimising $f_i(\mathbf x)=\tfrac12\big(\mathbf a_i^{\mathsf T}\mathbf x-b_i\big)^2$ — the loss from a **single** data point — gives
> $$\nabla f_i(\mathbf x)=\mathbf a_i\big(\mathbf a_i^{\mathsf T}\mathbf x-b_i\big)$$
> so a gradient step on $f_i$ with step $\mu/\lVert\mathbf a_i\rVert^2$ **is exactly the Kaczmarz update.**
>
> **Kaczmarz (1937) is therefore SGD on a least-squares objective**, twenty years before Robbins–Monro and seventy before deep learning. **Randomising the row order rather than cycling gives *randomized Kaczmarz*, whose expected convergence rate — proved by Strohmer and Vershynin in 2009 — is one of the sharpest results known for any stochastic method.**
>
> **The chapter therefore contains both ancestors:** RLS is [[06 - Newton and Quasi-Newton Methods|second-order]] online learning, Kaczmarz is first-order online learning, and the modern split between Adam-like and SGD-like methods is the same split.

---

### 7. Regularised least squares — the complete picture

Adding $\lambda\lVert\mathbf x\rVert^2$ gives **ridge regression**, whose normal equations are

$$\big(A^{\mathsf T}A+\lambda I\big)\mathbf x=A^{\mathsf T}\mathbf b\qquad\Longrightarrow\qquad \mathbf x_\lambda^*=\big(A^{\mathsf T}A+\lambda I\big)^{-1}A^{\mathsf T}\mathbf b$$

> [!important] What $\lambda$ does, collected from four chapters
> | Effect | Chapter |
> |---|---|
> | **Existence** — makes $f$ coercive, so a minimiser exists | [[01 - The Optimization Problem\|ch. 01]] |
> | **Uniqueness** — makes $f$ strictly convex for any $A$, including $p>n$ | [[02 - Convex Sets and Convex Functions\|ch. 02]] |
> | **Conditioning** — $\kappa\to\dfrac{\sigma_{\max}^2+\lambda}{\sigma_{\min}^2+\lambda}$, so gradient methods converge faster | [[05 - Gradient Methods\|ch. 05]] |
> | **Invertibility** — $A^{\mathsf T}A+\lambda I\succ0$ always, so the linear solve never fails | this chapter |
> | **Bias–variance trade-off** | [[Econometrics/contents/00-Index\|Econometrics]] / [[Mathematical Statistics/contents/00-Index\|Math Stats]] |
>
> **Four of the five are optimization facts and hold for every $\lambda>0$ unconditionally. Only the fifth is statistical, and only it depends on choosing $\lambda$ well.**

**The whole family, in one table:**

| Problem | Penalty | Solution |
|---|---|---|
| **OLS**, full rank | none | $(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ |
| **OLS**, rank-deficient | none | $A^+\mathbf b$ (minimum norm) |
| **Ridge** | $\lambda\lVert\mathbf x\rVert_2^2$ | $(A^{\mathsf T}A+\lambda I)^{-1}A^{\mathsf T}\mathbf b$ |
| **LASSO** | $\lambda\lVert\mathbf x\rVert_1$ | **no closed form** — convex but non-smooth, needs [[12 - Convex Programming and Constrained Algorithms\|ch. 12]] |

> [!note] Why the LASSO row has no formula
> $\lVert\mathbf x\rVert_1$ is convex but **not differentiable at zero**, so the FONC $\nabla f=\mathbf 0$ does not apply — one needs subgradients ([[02 - Convex Sets and Convex Functions|ch. 02]] §4). **That non-differentiability is not a defect; it is the entire mechanism by which the LASSO produces exact zeros and hence variable selection.** Ridge, being smooth, shrinks coefficients but never zeroes them.

---

## ✏️ Exercises

> [!question] Exercise 1 — line fitting *(easy)*
> Fit $y=mt+c$ by least squares to $(1,2)$, $(2,3)$, $(3,5)$, $(4,6)$.
> **(a)** Set up $A$, $\mathbf b$ and the normal equations.
> **(b)** Solve for $m^*$ and $c^*$.
> **(c)** Compute the residual and verify it is orthogonal to both columns of $A$.

> [!example]- Solution
> **(a)** $$A=\begin{pmatrix}1&1\\2&1\\3&1\\4&1\end{pmatrix},\qquad \mathbf b=\begin{pmatrix}2\\3\\5\\6\end{pmatrix},\qquad \mathbf x=\begin{pmatrix}m\\c\end{pmatrix}$$
> $$A^{\mathsf T}A=\begin{pmatrix}\sum t_i^2&\sum t_i\\ \sum t_i&4\end{pmatrix}=\begin{pmatrix}30&10\\10&4\end{pmatrix},\qquad A^{\mathsf T}\mathbf b=\begin{pmatrix}\sum t_iy_i\\ \sum y_i\end{pmatrix}=\begin{pmatrix}47\\16\end{pmatrix}$$
> since $\sum t_iy_i=2+6+15+24=47$ and $\sum y_i=16$.
>
> **(b)** $\det(A^{\mathsf T}A)=120-100=20$, so
> $$\mathbf x^*=\frac1{20}\begin{pmatrix}4&-10\\-10&30\end{pmatrix}\begin{pmatrix}47\\16\end{pmatrix}=\frac1{20}\begin{pmatrix}188-160\\-470+480\end{pmatrix}=\frac1{20}\begin{pmatrix}28\\10\end{pmatrix}=\boxed{\left(m^*,c^*\right)=(1.4,\ 0.5)}$$
> so the line of best fit is $y=1.4t+0.5$.
>
> **(c)** Fitted values $1.9,\ 3.3,\ 4.7,\ 6.1$, so
> $$\mathbf e=A\mathbf x^*-\mathbf b=(-0.1,\ 0.3,\ -0.3,\ 0.1)^{\mathsf T}$$
> $$A^{\mathsf T}\mathbf e=\begin{pmatrix}1(-0.1)+2(0.3)+3(-0.3)+4(0.1)\\ -0.1+0.3-0.3+0.1\end{pmatrix}=\begin{pmatrix}-0.1+0.6-0.9+0.4\\0\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\ \checkmark$$
>
> > [!tip]- Always run this check on a hand computation
> > **$A^{\mathsf T}\mathbf e=\mathbf 0$ gives $n$ independent equations that any correct least-squares solution must satisfy**, and they cost nothing to verify. A slip anywhere in $A^{\mathsf T}A$, $A^{\mathsf T}\mathbf b$ or the solve shows up here immediately.
> >
> > **The two rows also have statistical names.** The second row, $\sum e_i=0$, is why including an intercept forces the residuals to have mean zero. The first row, $\sum t_ie_i=0$, is why the residuals are uncorrelated with the regressor. **Neither is an assumption about the data — both are the FONC.**

---

> [!question] Exercise 2 — least squares as projection *(easy–medium)*
> Let $A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix}$ and $\mathbf b=(6,0,0)^{\mathsf T}$.
> **(a)** Find $\mathbf x^*$ and the projection $\mathbf h=A\mathbf x^*$.
> **(b)** Compute the projector $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ and verify $P^2=P$ and $P=P^{\mathsf T}$.
> **(c)** Verify $\mathbf b-\mathbf h\perp\mathcal R(A)$ and interpret $\lVert\mathbf b-\mathbf h\rVert$.

> [!example]- Solution
> **(a)** $$A^{\mathsf T}A=\begin{pmatrix}3&3\\3&5\end{pmatrix},\quad\det=6,\qquad A^{\mathsf T}\mathbf b=\begin{pmatrix}6\\0\end{pmatrix}$$
> $$\mathbf x^*=\frac16\begin{pmatrix}5&-3\\-3&3\end{pmatrix}\begin{pmatrix}6\\0\end{pmatrix}=\frac16\begin{pmatrix}30\\-18\end{pmatrix}=\boxed{(5,\ -3)^{\mathsf T}}$$
> $$\mathbf h=A\mathbf x^*=(5,\ 2,\ -1)^{\mathsf T}$$
>
> **(b)** $$P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}=\frac16\begin{pmatrix}5&2&-1\\2&2&2\\-1&2&5\end{pmatrix}$$
> - **Symmetric** by inspection ✔ — and structurally, since $(A^{\mathsf T}A)^{-1}$ is symmetric.
> - **Idempotent:** $P^2=A(A^{\mathsf T}A)^{-1}\underbrace{A^{\mathsf T}A(A^{\mathsf T}A)^{-1}}_{=I}A^{\mathsf T}=P$ ✔ — **projecting twice is projecting once.**
> - $\operatorname{tr}P=\frac{5+2+5}{6}=2=n$ ✔ — **the trace of a projector is the dimension of the subspace it projects onto**, i.e. the number of fitted parameters. *(In statistics this is the "degrees of freedom" of the fit.)*
>
> Checking: $P\mathbf b=\frac16(30,12,-6)^{\mathsf T}=(5,2,-1)^{\mathsf T}=\mathbf h$ ✔.
>
> **(c)** $$\mathbf e=\mathbf b-\mathbf h=(1,\ -2,\ 1)^{\mathsf T}$$
> $$\mathbf a_1^{\mathsf T}\mathbf e=1-2+1=0\ \checkmark,\qquad \mathbf a_2^{\mathsf T}\mathbf e=0-2+2=0\ \checkmark$$
>
> $\lVert\mathbf e\rVert=\sqrt6\approx2.449$ is **the distance from $\mathbf b$ to the plane $\mathcal R(A)$** — the smallest achievable residual, and the square root of the minimised objective. *(In regression it is the residual sum of squares: $\lVert\mathbf e\rVert^2=6$.)*
>
> **The Pythagorean identity that makes all of this work:**
> $$\lVert\mathbf b\rVert^2=\lVert\mathbf h\rVert^2+\lVert\mathbf e\rVert^2:\qquad 36=30+6\ \checkmark$$
> **This is the ANOVA decomposition of statistics** — total sum of squares $=$ explained $+$ residual — and it is nothing more than Pythagoras applied to an orthogonal projection.

---

> [!question] Exercise 3 — the minimum-norm solution *(medium)*
> Find the point of $\mathbb R^3$ closest to the origin on the intersection of the planes
> $$x_1+2x_2-x_3=1,\qquad 4x_1+x_2+3x_3=0$$
> **(a)** Formulate as a minimum-norm problem and solve.
> **(b)** Verify both constraints and that $\mathbf x^*\in\mathcal R(A^{\mathsf T})$.
> **(c)** Why is $\mathbf x^*\perp\mathcal N(A)$, and what does that mean geometrically?

> [!example]- Solution
> **(a)** $$\min\lVert\mathbf x\rVert\ \text{ s.t. }\ A\mathbf x=\mathbf b,\qquad A=\begin{pmatrix}1&2&-1\\4&1&3\end{pmatrix},\quad\mathbf b=\begin{pmatrix}1\\0\end{pmatrix}$$
> Here $m=2<n=3$ and $\operatorname{rank}A=2$, so Theorem 12.2 applies.
> $$AA^{\mathsf T}=\begin{pmatrix}1+4+1&4+2-3\\4+2-3&16+1+9\end{pmatrix}=\begin{pmatrix}6&3\\3&26\end{pmatrix},\qquad\det=156-9=147$$
> $$(AA^{\mathsf T})^{-1}\mathbf b=\frac1{147}\begin{pmatrix}26&-3\\-3&6\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix}=\frac1{147}\begin{pmatrix}26\\-3\end{pmatrix}$$
> $$\mathbf x^*=A^{\mathsf T}\cdot\frac1{147}\begin{pmatrix}26\\-3\end{pmatrix}=\frac1{147}\begin{pmatrix}26-12\\52-3\\-26-9\end{pmatrix}=\frac1{147}\begin{pmatrix}14\\49\\-35\end{pmatrix}=\boxed{\left(\tfrac2{21},\ \tfrac13,\ -\tfrac5{21}\right)}$$
> *(Verified: $\approx(0.09524,\ 0.33333,\ -0.23810)$ with $\lVert\mathbf x^*\rVert=0.42056$.)*
>
> **(b)** $\ \tfrac2{21}+\tfrac23+\tfrac5{21}=\tfrac{2+14+5}{21}=1$ ✔ and $\tfrac8{21}+\tfrac13-\tfrac{15}{21}=\tfrac{8+7-15}{21}=0$ ✔.
>
> **$\mathbf x^*\in\mathcal R(A^{\mathsf T})$ by construction** — it is written as $A^{\mathsf T}(\text{something})$, i.e. a linear combination of the two plane normals $(1,2,-1)$ and $(4,1,3)$.
>
> **(c)** By the fundamental theorem of linear algebra ([[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]), $\mathcal R(A^{\mathsf T})=\mathcal N(A)^\perp$. So $\mathbf x^*\perp\mathcal N(A)$.
>
> **Geometrically:** the feasible set is the **line** $\{\mathbf x_p+\mathbf v:\mathbf v\in\mathcal N(A)\}$ — a particular solution plus the null-space direction. **The point of a line closest to the origin is the foot of the perpendicular**, i.e. the point whose position vector is orthogonal to the line's direction. **That direction is $\mathcal N(A)$, so $\mathbf x^*$ must have zero component along it — which is exactly $\mathbf x^*\in\mathcal R(A^{\mathsf T})$.**
>
> **The two theorems of this chapter are one theorem seen from two sides:**
>
> | | $m>n$ (Thm 12.1) | $m<n$ (Thm 12.2) |
> |---|---|---|
> | Ask | closest point *in* $\mathcal R(A)$ to $\mathbf b$ | closest point *on* $\{A\mathbf x=\mathbf b\}$ to $\mathbf 0$ |
> | Answer | residual $\perp\mathcal R(A)$ | solution $\perp\mathcal N(A)$ |
> | Formula | $(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ | $A^{\mathsf T}(AA^{\mathsf T})^{-1}\mathbf b$ |
>
> **Both say: orthogonality characterises the closest point.**

---

> [!question] Exercise 4 — recursive least squares *(medium–hard)*
> Take $A_0=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$, $\mathbf b^{(0)}=(1,1,1)^{\mathsf T}$, then two new rows: $\mathbf a_1^{\mathsf T}=(2,1)$ with $b_1=3$, and $\mathbf a_2^{\mathsf T}=(3,1)$ with $b_2=4$.
> **(a)** Compute $P_0=(A_0^{\mathsf T}A_0)^{-1}$ and $\mathbf x^{(0)}$.
> **(b)** Apply RLS twice.
> **(c)** Verify against the batch solution on all five rows.
> **(d)** Count the arithmetic, and say what RLS is in machine-learning terms.

> [!example]- Solution
> **(a)** $A_0^{\mathsf T}A_0=\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $\det=3$, so
> $$P_0=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix},\qquad A_0^{\mathsf T}\mathbf b^{(0)}=\begin{pmatrix}2\\2\end{pmatrix},\qquad \mathbf x^{(0)}=P_0\begin{pmatrix}2\\2\end{pmatrix}=\boxed{\left(\tfrac23,\ \tfrac23\right)}$$
>
> **(b) Update 1** with $\mathbf a_1=(2,1)^{\mathsf T}$, $b_1=3$:
> $$P_0\mathbf a_1=\tfrac13(4-1,\ -2+2)^{\mathsf T}=(1,\ 0)^{\mathsf T},\qquad \mathbf a_1^{\mathsf T}P_0\mathbf a_1=2$$
> $$P_1=P_0-\frac{(1,0)^{\mathsf T}(1,0)}{1+2}=\begin{pmatrix}\tfrac23&-\tfrac13\\-\tfrac13&\tfrac23\end{pmatrix}-\begin{pmatrix}\tfrac13&0\\0&0\end{pmatrix}=\boxed{\begin{pmatrix}\tfrac13&-\tfrac13\\-\tfrac13&\tfrac23\end{pmatrix}}$$
> Innovation: $b_1-\mathbf a_1^{\mathsf T}\mathbf x^{(0)}=3-(\tfrac43+\tfrac23)=1$, and $P_1\mathbf a_1=(\tfrac13,\ \mathbf 0)^{\mathsf T}$... computing: $P_1\mathbf a_1=(\tfrac23-\tfrac13,\ -\tfrac23+\tfrac23)^{\mathsf T}=(\tfrac13,0)^{\mathsf T}$, so
> $$\mathbf x^{(1)}=\left(\tfrac23,\tfrac23\right)+1\cdot\left(\tfrac13,0\right)=\boxed{\left(1,\ \tfrac23\right)}$$
>
> **Update 2** with $\mathbf a_2=(3,1)^{\mathsf T}$, $b_2=4$: $\ P_1\mathbf a_2=(\tfrac23,\ -\tfrac13)^{\mathsf T}$, $\mathbf a_2^{\mathsf T}P_1\mathbf a_2=2-\tfrac13=\tfrac53$, so
> $$P_2=P_1-\frac{1}{1+\tfrac53}\begin{pmatrix}\tfrac49&-\tfrac29\\-\tfrac29&\tfrac19\end{pmatrix}=\boxed{\begin{pmatrix}\tfrac16&-\tfrac14\\-\tfrac14&\tfrac58\end{pmatrix}}$$
> Innovation $=4-(3+\tfrac23)=\tfrac13$, and $P_2\mathbf a_2=(\tfrac14,\ -\tfrac18)^{\mathsf T}$, giving
> $$\mathbf x^{(2)}=\left(1,\tfrac23\right)+\tfrac13\left(\tfrac14,-\tfrac18\right)=\boxed{\left(\tfrac{13}{12},\ \tfrac58\right)}=(1.08333,\ 0.625)$$
>
> **(c)** Batch on all five rows: $A=\begin{psmallmatrix}1&0\\0&1\\1&1\\2&1\\3&1\end{psmallmatrix}$, $\mathbf b=(1,1,1,3,4)^{\mathsf T}$ gives $(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b=(1.083333,\ 0.625)$ ✔ **— identical.**
>
> **RLS is exact, not an approximation.** It computes the same answer as batch least squares, by a different route.
>
> **(d) Cost per new observation:** $P_k\mathbf a$ is $O(n^2)$; the outer product and update are $O(n^2)$; the innovation is $O(n)$. **Total $O(n^2)$ per observation, with no inversion and no storage of past data.**
>
> Refitting from scratch after $m$ observations costs $O(mn^2+n^3)$, so **RLS is a factor of $m$ cheaper** — and its memory is $O(n^2)$ regardless of how much data has arrived.
>
> **In modern terms:** RLS is **exact online learning for a convex quadratic loss**. The step $P_{k+1}\mathbf a_{k+1}$ is an adaptive, per-direction gain — **not a scalar learning rate but a matrix one, and it is the inverse Hessian** ([[06 - Newton and Quasi-Newton Methods|ch. 06]]). **RLS is to SGD what Newton is to gradient descent**, and the resemblance is not an analogy: $P_k=G_k^{-1}$ *is* the inverse of the accumulated Hessian, maintained by the same Sherman–Morrison update that ch. 06 used for BFGS.
>
> *(Adding a forgetting factor, $G_{k+1}=\lambda G_k+\mathbf a\mathbf a^{\mathsf T}$ with $\lambda\lesssim1$, downweights old data and lets the fit track a drifting target. That single change turns RLS into the standard adaptive-filtering algorithm, and it is the same idea as an exponential moving average in Adam.)*

---

> [!question] Exercise 5 — why the formula is not the algorithm *(hard)*
> **(a)** Prove $\kappa_2(A^{\mathsf T}A)=\kappa_2(A)^2$ for full-column-rank $A$.
> **(b)** For the Läuchli matrix $A=\begin{psmallmatrix}1&1\\ \varepsilon&0\\0&\varepsilon\end{psmallmatrix}$ with $\varepsilon=10^{-8}$ and $\mathbf b=(2,\varepsilon,\varepsilon)^{\mathsf T}$, compute $\kappa(A)$ and $\kappa(A^{\mathsf T}A)$, and predict what happens in double precision.
> **(c)** Compare the normal equations, QR and SVD on this problem.
> **(d)** Why does QR avoid the problem?
> **(e)** State the rule, and where else in this subject the same fact appears.

> [!example]- Solution
> **(a)** Let $A=U\Sigma V^{\mathsf T}$ be the SVD with singular values $\sigma_1\ge\cdots\ge\sigma_n>0$. Then
> $$A^{\mathsf T}A=V\Sigma^{\mathsf T}U^{\mathsf T}U\Sigma V^{\mathsf T}=V\Sigma^{\mathsf T}\Sigma V^{\mathsf T}=V\operatorname{diag}(\sigma_1^2,\dots,\sigma_n^2)V^{\mathsf T}$$
> **so the eigenvalues of $A^{\mathsf T}A$ are exactly $\sigma_i^2$.** Since $\kappa_2(A)=\sigma_1/\sigma_n$ and $A^{\mathsf T}A$ is symmetric positive definite,
> $$\kappa_2(A^{\mathsf T}A)=\frac{\sigma_1^2}{\sigma_n^2}=\kappa_2(A)^2\qquad\blacksquare$$
>
> **(b)** Computed: $\kappa(A)=1.4142\times10^{8}$ and $\kappa(A^{\mathsf T}A)=5.96\times10^{16}$. *(Indeed $(1.4142\times10^8)^2=2\times10^{16}$, the discrepancy being the rounding already present in the computed $A^{\mathsf T}A$.)*
>
> Exactly, $A^{\mathsf T}A=\begin{psmallmatrix}1+\varepsilon^2&1\\1&1+\varepsilon^2\end{psmallmatrix}$ with $\det=(1+\varepsilon^2)^2-1=2\varepsilon^2+\varepsilon^4\approx2\times10^{-16}$. **But $\varepsilon^2=10^{-16}$ is below $\varepsilon_{\text{mach}}=2.2\times10^{-16}$, so $\operatorname{fl}(1+\varepsilon^2)=1$** and the *computed* matrix is
> $$\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad\text{determinant }0$$
> **Prediction: the normal equations will be exactly singular.**
>
> **(c)** *(All verified.)*
>
> | Method | Result | Error |
> |---|---|---|
> | **Normal equations** | **`LinAlgError: Singular matrix`** | total failure |
> | **QR** | $(1.0,\ 1.0)$ | $0$ |
> | **SVD (`lstsq`)** | $(1.0,\ 1.0)$ | $5.0\times10^{-16}$ |
>
> **The problem is perfectly well posed** — $\kappa(A)=1.4\times10^8$ leaves eight digits of accuracy available — **and the normal equations destroy all of them.** This is not a marginal loss of precision; the method does not run.
>
> **(d)** Write $A=QR$ with $Q^{\mathsf T}Q=I$. Because orthogonal transformations preserve the Euclidean norm,
> $$\lVert A\mathbf x-\mathbf b\rVert=\lVert Q(R\mathbf x)-\mathbf b\rVert=\lVert R\mathbf x-Q^{\mathsf T}\mathbf b\rVert$$
> so the problem reduces to the triangular system $R\mathbf x=Q^{\mathsf T}\mathbf b$. **The quantity actually factorised is $A$, whose condition number is $\kappa(A)$; $A^{\mathsf T}A$ never appears.**
>
> **The deeper reason: orthogonal matrices have condition number 1**, so they cannot amplify error. **Every stable numerical linear algebra algorithm is built out of orthogonal transformations for exactly this reason** — Householder reflections and Givens rotations in QR, and both plus a bidiagonalisation in the SVD.
>
> **(e) The rule: never form $A^{\mathsf T}A$ when you can factorise $A$.**
> ```python
> #  ✘  loses half the digits, fails at κ(A) ≳ 10⁸
> beta = np.linalg.inv(X.T @ X) @ X.T @ y
> #  ✔  QR/SVD, works to κ(A) ≈ 10¹⁶, handles rank deficiency
> beta = np.linalg.lstsq(X, y, rcond=None)[0]
> ```
>
> **The same fact, three more times in this subject:**
> 1. **[[05 - Gradient Methods|Ch. 05]]** — gradient descent on $\lVert A\mathbf x-\mathbf b\rVert^2$ has Hessian $2A^{\mathsf T}A$, so it needs $O(\kappa(A)^2)$ iterations. Exercise 3(d) there computed $3.45\times10^6$ iterations for $\kappa(A)=10^3$.
> 2. **[[07 - Conjugate Direction Methods|Ch. 07]]** — CG on the normal equations needs $O(\sqrt{\kappa(A^{\mathsf T}A)})=O(\kappa(A))$ iterations. **LSQR** applies the same Krylov idea to $A$ directly and never squares.
> 3. **§7 above** — ridge regression's $\lambda$ improves $\kappa(A^{\mathsf T}A)$ from $\sigma_1^2/\sigma_n^2$ to $(\sigma_1^2+\lambda)/(\sigma_n^2+\lambda)$, which is why it rescues numerically borderline fits and not only statistically borderline ones.
>
> **And the practical warning sign:** if a regression package reports a coefficient with an implausible magnitude and an enormous standard error, **check $\kappa(X)$ before checking the model.** [[Econometrics/contents/00-Index|Econometrics]] calls this multicollinearity; **numerically it is a large $\kappa$ and it is the same phenomenon.**

---

## 📝 Summary

- **Overdetermined ($m>n$, full column rank):** $\min\lVert A\mathbf x-\mathbf b\rVert^2$ has the unique solution of the **normal equations** $A^{\mathsf T}A\mathbf x=A^{\mathsf T}\mathbf b$. $A^{\mathsf T}A$ is invertible iff $A$ has full column rank.
- **Three equivalent statements:** $\mathbf x^*$ minimises the residual $\iff A^{\mathsf T}(A\mathbf x^*-\mathbf b)=\mathbf 0\iff$ **the residual is orthogonal to every column of $A$.** The middle one is the FONC; the last is why OLS residuals are uncorrelated with the regressors.
- **Least squares is orthogonal projection** onto $\mathcal R(A)$, with projector $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ (the hat matrix): symmetric, idempotent, $\operatorname{tr}P=n$. **Pythagoras on that projection is the ANOVA decomposition.**
- **Underdetermined ($m<n$, full row rank):** the minimum-norm solution is $A^{\mathsf T}(AA^{\mathsf T})^{-1}\mathbf b$, and it is the unique solution orthogonal to $\mathcal N(A)$. **Both formulas are the pseudoinverse $A^+$**, whose general form needs the SVD.
- **$\kappa(A^{\mathsf T}A)=\kappa(A)^2$, so forming the normal equations halves the available digits.** On a $3\times2$ example with $\kappa(A)=1.4\times10^8$ the normal equations are **exactly singular in double precision** while QR and SVD return the exact answer. **Use `lstsq`, not `inv(X.T @ X)`.**
- **Recursive least squares** updates the fit for each new observation in $O(n^2)$ via Sherman–Morrison, with a correction proportional to the **innovation** $b-\mathbf a^{\mathsf T}\mathbf x$. **It is exact online learning, and $P_k$ is a running inverse Hessian — RLS is to SGD what Newton is to gradient descent.**
- **Kaczmarz's algorithm** projects onto one constraint hyperplane at a time and converges to the minimum-norm solution for $0<\mu<2$. **It is stochastic gradient descent on a per-example squared loss, published in 1937.**
- **Ridge regression** $(A^{\mathsf T}A+\lambda I)\mathbf x=A^{\mathsf T}\mathbf b$ buys existence, uniqueness, conditioning and invertibility unconditionally, and a bias–variance trade-off only if $\lambda$ is chosen well. **The LASSO has no closed form because $\lVert\cdot\rVert_1$ is non-smooth — which is precisely why it produces exact zeros.**

---

## ⚠️ Important Notes

> [!warning] The six errors
> 1. **Computing `inv(X.T @ X) @ X.T @ y`.** Exercise 5. Use `lstsq`.
> 2. **Assuming $A^{\mathsf T}A$ is invertible.** It is iff $A$ has full column rank — which fails whenever $p>n$ or two features are collinear.
> 3. **Using the wrong pseudoinverse formula.** $(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ for tall $A$; $A^{\mathsf T}(AA^{\mathsf T})^{-1}$ for wide $A$. Swapping them gives a singular matrix.
> 4. **Forgetting to verify $A^{\mathsf T}\mathbf e=\mathbf 0$.** It is $n$ free checks on any hand computation — and it caught a slip in Exercise 1.
> 5. **Fitting a high-degree polynomial in the monomial basis.** $\kappa$ of a Vandermonde matrix grows exponentially in the degree; use orthogonal polynomials.
> 6. **Treating a large coefficient with a huge standard error as a modelling result.** Check $\kappa(X)$ first.

> [!tip] Which algorithm
> | Situation | Method |
> |---|---|
> | $m,n$ small, $\kappa(A)$ modest, quick calculation | normal equations (by hand, fine) |
> | **General dense least squares** | **QR** — the default |
> | Rank-deficient, or $\kappa$ unknown | **SVD** — also gives $A^+$ and the minimum-norm solution |
> | $A$ large and sparse | **LSQR / LSMR** (CG applied without squaring $\kappa$) |
> | Data arriving one point at a time | **RLS**, or Kaczmarz/SGD if $n$ is very large |
> | $p>n$, or collinear features | **ridge** — and then any of the above |

> [!note] Where this chapter connects
> - **[[02 - Convex Sets and Convex Functions|Ch. 02]] Exercise 4** is this chapter's ridge case, done as a convexity problem.
> - **[[05 - Gradient Methods|Ch. 05]]** and **[[07 - Conjugate Direction Methods|ch. 07]]** — least squares is *the* quadratic on which those methods are analysed, with $Q=2A^{\mathsf T}A$.
> - **[[06 - Newton and Quasi-Newton Methods|Ch. 06]]** — Sherman–Morrison appears in both chapters for the same reason, and **Gauss–Newton** solves a nonlinear least-squares problem by a sequence of linear ones.
> - **[[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]** supplies orthogonal projection, the four fundamental subspaces and QR; **the SVD needed for §3's general pseudoinverse is [[Linear Algebra/contents/00-Index|absent from Nicholson]]** and must be taken from Strang.
> - **[[Econometrics/contents/00-Index|Econometrics]]** — OLS *is* §1, the hat matrix is §2, multicollinearity is §4's $\kappa$, and ridge is §7.
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]** — the Gauss–Markov theorem says this $\mathbf x^*$ is BLUE under the usual assumptions; **the optimization and the statistics are separate claims about the same formula.**
> - **[[Machine Learning/contents/00-Index|Machine Learning]]** — §5 and §6 are the ancestors of online and stochastic learning respectively.

---

> [!warning] Gaps in the source material
> **Source.** Chong & Żak ch. 12 entirely; Luenberger & Ye has no counterpart chapter, so **there was no second source and everything was verified computationally instead.**
>
> **OCR damage:**
> - **`ΊΖ(Α)`, `1Z(A)`, `11(A)`, `H(A)` are all $\mathcal R(A)$** (the range); `λί(Α)`, `Λ/*(Α)`, `N(A)` are $\mathcal N(A)$; `\\Ax - b\\` is $\lVert A\mathbf x-\mathbf b\rVert$; `A A` with no superscript is $A^{\mathsf T}A$; `AT6`, `A b`, `Alb` are $A^{\mathsf T}\mathbf b$; `(ΑτΑ)~λ` and `{Al A)~LAlb` are $(A^{\mathsf T}A)^{-1}$ and $(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$.
> - **The transpose superscript is lost almost everywhere**, which for a chapter about $A^{\mathsf T}A$ versus $AA^{\mathsf T}$ is the worst possible failure. **Every formula here was reconstructed from the dimensions** ($A^{\mathsf T}A$ is $n\times n$, $AA^{\mathsf T}$ is $m\times m$) and then verified numerically.
> - **All matrices lose their brackets and row structure**, so the Gram-matrix display in Proposition 12.1 and every worked example's data had to be reassembled.
> - **In Example 12.3 the data table is destroyed.** It extracts as `sp si s2 no rn ri2 n3 ri4 | 12 14 7 8 6 3` — **eight labels and six values.** The values were **recovered from the book's own arithmetic**: the printed $A^{\mathsf T}A=\begin{psmallmatrix}6&1\\1&6\end{psmallmatrix}$ forces $\lVert\mathbf s\rVert^2=6$ and $s_0s_2=1$, giving $\mathbf s=(1,2,1)$; and the printed sums $4+14+8$ and $8+12+3$ then force $\mathbf r=(4,7,8,6,3)$. **With those values everything reproduces**, including $A^{\mathsf T}\mathbf b=(26,23)$ and $\mathbf x^*=\tfrac1{35}(133,112)=(3.8,3.2)$.
> - **Figures 12.1 (the orthogonal projection of $\mathbf b$ onto $\mathcal R(A)$), 12.2 (the fitted line through the three data points) and 12.3 (the two-path wireless channel) are images and are lost.** **Figure 12.1 is §2's entire argument.**
>
> **Verification performed.** Every worked example was recomputed with `numpy`:
> - **Example 12.1** (concrete mixing): $A^{\mathsf T}A=\begin{psmallmatrix}0.34&0.32\\0.32&0.54\end{psmallmatrix}$, $A^{\mathsf T}\mathbf b=(3.9,3.9)$, $\det=0.0812$, and $\mathbf x^*=(10.5665,\ 0.9606)$ — the book prints $(10.6,\ 0.96)$ ✔.
> - **Example 12.2** (line fitting): $A^{\mathsf T}A=\begin{psmallmatrix}29&9\\9&3\end{psmallmatrix}$, $\det=6$, $A^{\mathsf T}\mathbf b=(78,22)$, $\mathbf x^*=(6,\ -\tfrac{32}3)$ ✔, and the residual $\left(-\tfrac53,\tfrac{10}3,-\tfrac53\right)$ satisfies $A^{\mathsf T}\mathbf e=\mathbf 0$ exactly.
> - **Example 12.3** (attenuation estimation): as reconstructed above, $\mathbf x^*=(3.8,\ 3.2)$ ✔.
> - **Example 12.6** (RLS): $P_0=\tfrac13\begin{psmallmatrix}2&-1\\-1&2\end{psmallmatrix}$, $\mathbf x^{(0)}=(\tfrac23,\tfrac23)$; $P_1=\begin{psmallmatrix}1/3&-1/3\\-1/3&2/3\end{psmallmatrix}$, $\mathbf x^{(1)}=(1,\tfrac23)$; $P_2=\begin{psmallmatrix}1/6&-1/4\\-1/4&5/8\end{psmallmatrix}$, $\mathbf x^{(2)}=(\tfrac{13}{12},\tfrac58)$ — **every printed value reproduces**, and the batch solve on all five rows gives the identical $(1.083333,\ 0.625)$.
> - **Example 12.7** (minimum norm): $\mathbf x^*=\left(\tfrac2{21},\tfrac13,-\tfrac5{21}\right)$, satisfying both plane equations exactly.
> - **Exercise 5**: the Läuchli experiment — $\kappa(A)=1.4142\times10^8$, $\kappa(A^{\mathsf T}A)=5.96\times10^{16}$, the computed $A^{\mathsf T}A$ equal to $\begin{psmallmatrix}1&1\\1&1\end{psmallmatrix}$ with determinant exactly $0$, the normal equations raising `Singular matrix`, and QR and SVD returning $(1,1)$. **The Vandermonde table** ($\kappa=1.1\times10^2,\ 1.9\times10^4,\ 3.5\times10^6,\ 7.5\times10^8$ for degrees $3,6,9,12$, with $\kappa(V^{\mathsf T}V)/\kappa(V)^2=1.000$) was computed the same way.
>
> **No mathematical error was found in Chong & Żak ch. 12.**
>
> **Scope and additions.**
> - **§4 is entirely my own addition and is the most important section in the chapter.** **Chong & Żak present $\mathbf x^*=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ as the answer and never mention conditioning, QR, or the SVD anywhere in ch. 12.** For a 2013 optimization textbook this is a defensible scope decision — numerical linear algebra is another subject — **but a Data Science reader who implements the printed formula will get wrong answers on real design matrices**, so the omission had to be filled. The Läuchli example, the QR/SVD comparison and the Vandermonde table are mine.
> - **The reading of RLS as online learning and of Kaczmarz as SGD is my own** (§§5–6). Chong & Żak present both as linear-algebra algorithms of the 1930s–50s and make no connection to anything modern; **the connections are exact, not analogies** — the Kaczmarz update *is* a gradient step on a single-example squared loss, and $P_k$ *is* an inverse Hessian.
> - **§7's table collecting what $\lambda$ does across four chapters is my own synthesis**, as is the note on why the LASSO has no closed form.
> - **The pseudoinverse framing of §3, and the observation that the two theorems are one theorem** (Exercise 3's table), are mine; the book presents them in separate sections without remarking on the duality, despite giving literally the same proof twice.
> - **§2's identification of $P$ with the hat matrix and of Pythagoras with the ANOVA decomposition** (Exercise 2) is mine, connecting to [[Econometrics/contents/00-Index|Econometrics]].

#optimization #least-squares #normal-equations #pseudoinverse #orthogonal-projection #recursive-least-squares #kaczmarz #condition-number #qr-decomposition #ridge-regression
