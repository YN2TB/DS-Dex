---
subject: Optimization
chapter: 06
tags: [ds, optimization, newton-method, quasi-newton, bfgs, dfp, levenberg-marquardt, quadratic-convergence, secant-condition]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 9 and ch. 11; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, §8.5 and ch. 10"
---

# Newton and Quasi-Newton Methods

> [!abstract] What this chapter is for
> **[[05 - Gradient Methods|Chapter 05]] ended with a diagnosis: gradient descent is slow because $\kappa$ is large, and the cure is to precondition by $Q^{-1}$.** This chapter is the two ways of buying that cure.
>
> $$\textbf{Newton: }\ \mathbf x_{k+1}=\mathbf x_k-\big[\nabla^2f(\mathbf x_k)\big]^{-1}\nabla f(\mathbf x_k)\qquad\qquad \textbf{Quasi-Newton: }\ \mathbf x_{k+1}=\mathbf x_k-\alpha_kH_k\nabla f(\mathbf x_k)$$
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1–2** | Newton's method and its rate | **Quadratic convergence** — but only near $\mathbf x^*$, and only if $\nabla^2f(\mathbf x^*)$ is **invertible** |
> | **3** | Its three failure modes | **Not a descent method**; converges happily to maxima; undefined at a singular Hessian |
> | **4** | Damping and **Levenberg–Marquardt** | $(\nabla^2f+\mu I)^{-1}$ **interpolates between Newton and gradient descent** |
> | **5** | Cost | $O(n^2)$ storage, $O(n^3)$ per step — **the reason it lost** |
> | **6–7** | **Quasi-Newton: the secant condition** $H_{k+1}\Delta\mathbf g^{(i)}=\Delta\mathbf x^{(i)}$ | Build $Q^{-1}$ from gradient differences. **DFP, BFGS**, and why BFGS won |
> | **8** | L-BFGS and the modern picture | The $O(n)$ version, and why even it is rarely used in deep learning |
>
> **The single most important warning in the chapter is in §3**, and Chong & Żak's own showcase example demonstrates it without saying so — see Exercise 2.

---

## 📘 Main Knowledge

### 1. Newton's method in $n$ dimensions

**Same idea as [[04 - One-Dimensional Search Methods|ch. 04]] §6: replace $f$ by the quadratic matching it to second order, and minimise that.** Taylor about $\mathbf x_k$, discarding third order and above:

$$f(\mathbf x)\approx q(\mathbf x)=f(\mathbf x_k)+\mathbf g_k^{\mathsf T}(\mathbf x-\mathbf x_k)+\tfrac12(\mathbf x-\mathbf x_k)^{\mathsf T}F_k(\mathbf x-\mathbf x_k)$$

writing $\mathbf g_k=\nabla f(\mathbf x_k)$ and $F_k=\nabla^2f(\mathbf x_k)$. The FONC for $q$ gives $\mathbf 0=\nabla q=\mathbf g_k+F_k(\mathbf x-\mathbf x_k)$, so if $F_k\succ0$ the model's minimiser is

$$\boxed{\mathbf x_{k+1}=\mathbf x_k-F_k^{-1}\mathbf g_k}$$

> [!important] Never invert the Hessian — solve
> **The iteration is implemented in two steps:**
> $$\textbf{1. Solve }\ F_k\,\mathbf d_k=-\mathbf g_k\ \text{ for }\mathbf d_k\qquad\qquad \textbf{2. Set }\ \mathbf x_{k+1}=\mathbf x_k+\mathbf d_k$$
> **Solving an $n\times n$ system by Cholesky costs $\tfrac13n^3$ flops; forming $F_k^{-1}$ costs about three times that and is numerically worse.** ([[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02]].) **Every line of code that writes `inv(H) @ g` should write `solve(H, g)`.**
>
> **So Newton's method is "an efficient linear solver, called once per iteration"** — which is why [[08 - Least Squares and Linear Equations|ch. 08]] matters to it.

**The second reading, as in one dimension.** Setting $\mathbf g=\nabla f$, the iteration is Newton's method for the vector equation $\mathbf g(\mathbf x)=\mathbf 0$, with $F$ the **Jacobian** of $\mathbf g$. **Newton's method solves [[03 - Unconstrained Optimality Conditions|ch. 03's]] FONC iteratively** — and knows nothing else.

---

### 2. Convergence: exact on quadratics, quadratic in general

> [!important] The quadratic case: one step, from anywhere
> If $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ with $Q$ invertible, then $\mathbf g=Q\mathbf x-\mathbf b$, $F=Q$, and from any $\mathbf x_0$:
> $$\mathbf x_1=\mathbf x_0-Q^{-1}(Q\mathbf x_0-\mathbf b)=Q^{-1}\mathbf b=\mathbf x^*$$
> **The order of convergence is $\infty$.** Compare [[05 - Gradient Methods|ch. 05]], where the same problem takes $\approx3.45\kappa$ iterations.
>
> **This is §7 of chapter 05 made literal: Newton is steepest descent preconditioned by $Q^{-1}$, so $\kappa$ becomes 1.**

> [!important] Theorem (C&Ż 9.1) — quadratic convergence
> Suppose $f\in C^3$ and $\mathbf x^*$ satisfies $\nabla f(\mathbf x^*)=\mathbf 0$ with **$F(\mathbf x^*)$ invertible**. Then for all $\mathbf x_0$ sufficiently close to $\mathbf x^*$, Newton's method is well-defined, converges to $\mathbf x^*$, and
> $$\lVert\mathbf x_{k+1}-\mathbf x^*\rVert\ \le\ c_1c_2\lVert\mathbf x_k-\mathbf x^*\rVert^2$$
> so the order of convergence is **at least 2**.
>
> **Proof sketch.** Taylor gives $\lVert\nabla f(\mathbf x)-\nabla f(\mathbf x_k)-F_k(\mathbf x-\mathbf x_k)\rVert\le c_1\lVert\mathbf x-\mathbf x_k\rVert^2$ (this is where $f\in C^3$ is used — the third derivatives are continuous, hence bounded near $\mathbf x^*$). Invertibility of $F(\mathbf x^*)$ plus continuity gives $\lVert F(\mathbf x)^{-1}\rVert\le c_2$ nearby. Then
> $$\mathbf x_{k+1}-\mathbf x^*=F_k^{-1}\big(F_k(\mathbf x_k-\mathbf x^*)-\nabla f(\mathbf x_k)\big)$$
> and taking norms and applying the two bounds gives the result. $\blacksquare$

> [!warning] Read the hypotheses, because both of them fail in practice
> **The theorem assumes (i) $\mathbf x_0$ is already close to $\mathbf x^*$, and (ii) $F(\mathbf x^*)$ is invertible.**
>
> - **(i) is a genuine restriction**: nothing is claimed from a general starting point, and §3 shows the method can move uphill or diverge.
> - **(ii) is the one that catches people.** Chong & Żak state it and then never check it — **including in their own showcase example, where it fails.** See Exercise 2.
> - **And note what the theorem does *not* say: that $\mathbf x^*$ is a minimizer.** The book's own warning: *"if $\mathbf x^*$ is a local maximizer, then Newton's method would converge to it if we start close enough."* **The method solves $\nabla f=\mathbf 0$ and cannot tell what kind of point it found.**

---

### 3. The three ways Newton fails

| Failure | Cause | Symptom |
|---|---|---|
| **Not a descent method** | Even with $F_k\succ0$, the *full* step may overshoot | $f(\mathbf x_{k+1})>f(\mathbf x_k)$ |
| **$F_k$ not positive definite** | $\mathbf d_k=-F_k^{-1}\mathbf g_k$ need not be a descent direction | walks uphill; converges to saddles and maxima |
| **$F_k$ singular or near-singular** | the linear solve is undefined or wildly amplified | step is enormous, or the method crashes |

> [!important] Theorem (C&Ż 9.2) — what positive definiteness *does* buy
> If $F_k\succ0$ and $\mathbf g_k\ne\mathbf 0$, then $\mathbf d_k=-F_k^{-1}\mathbf g_k$ is a **descent direction**: there exists $\bar\alpha>0$ with $f(\mathbf x_k+\alpha\mathbf d_k)<f(\mathbf x_k)$ for all $\alpha\in(0,\bar\alpha)$.
>
> **Proof.** $\phi'(0)=\nabla f(\mathbf x_k)^{\mathsf T}\mathbf d_k=-\mathbf g_k^{\mathsf T}F_k^{-1}\mathbf g_k<0$ because $F_k^{-1}\succ0$. $\blacksquare$
>
> **Note precisely what this gives and what it does not: a descent *direction*, for *small enough* $\alpha$.** It says nothing about $\alpha=1$, which is what plain Newton uses. **Exercise 3 exhibits a positive definite Hessian for which the full Newton step increases $f$.**

---

### 4. Two repairs: damping and Levenberg–Marquardt

> [!important] Damped Newton — fixes failure 1
> $$\mathbf x_{k+1}=\mathbf x_k-\alpha_kF_k^{-1}\mathbf g_k,\qquad \alpha_k=\arg\min_{\alpha>0}f\big(\mathbf x_k-\alpha F_k^{-1}\mathbf g_k\big)$$
> **Take Newton's step as a *direction* and choose the length by line search** ([[04 - One-Dimensional Search Methods|ch. 04]] §9 — Armijo, in practice). By Theorem 9.2 the descent property now holds whenever $F_k\succ0$.
>
> **Crucially, near $\mathbf x^*$ the Armijo condition accepts $\alpha_k=1$**, so damping costs nothing asymptotically and quadratic convergence survives. **Always start the backtracking at $\alpha=1$ for a Newton-type direction.**

> [!important] Levenberg–Marquardt — fixes failures 2 and 3
> $$\boxed{\mathbf x_{k+1}=\mathbf x_k-\big(F_k+\mu_kI\big)^{-1}\mathbf g_k},\qquad\mu_k\ge0$$
>
> **Why it works.** If $F$ has eigenvalues $\lambda_1,\dots,\lambda_n$ with eigenvectors $\mathbf v_i$, then
> $$(F+\mu I)\mathbf v_i=\lambda_i\mathbf v_i+\mu\mathbf v_i=(\lambda_i+\mu)\mathbf v_i$$
> **so $F+\mu I$ has the same eigenvectors and eigenvalues shifted by $\mu$.** Taking $\mu>-\lambda_{\min}$ makes every eigenvalue positive, hence $F+\mu I\succ0$, hence a descent direction.

> [!important] LM interpolates between the two methods of chapters 05 and 06
> $$\mu\to0:\quad \mathbf d\to-F^{-1}\mathbf g\quad\textbf{(Newton)}\qquad\qquad \mu\to\infty:\quad\mathbf d\to-\tfrac1\mu\mathbf g\quad\textbf{(gradient descent, tiny step)}$$
> **$\mu$ is a dial from "trust the curvature completely" to "ignore the curvature entirely."** The standard strategy: **start $\mu$ small, and increase it until the step actually decreases $f$.**
>
> *(This is the same object as ridge regularisation of [[02 - Convex Sets and Convex Functions|ch. 02]] — $\mu I$ added to a matrix to make it positive definite and better conditioned. **Levenberg–Marquardt, ridge regression, and trust-region methods are three faces of one idea.**)*

---

### 5. The cost, and why Newton lost

| Quantity | Cost |
|---|---|
| Storage for $F_k$ | $\tfrac12n^2$ doubles |
| Cholesky factorisation of $F_k$ | $\tfrac13n^3$ flops **per iteration** |
| Evaluating $F_k$ | $O(n^2)$ function-evaluation-equivalents, or $O(n)$ Hessian-vector products |

| $n$ | Hessian storage | Cholesky flops | Time at $10^{11}$ flop/s |
|---|---|---|---|
| $10^2$ | $39$ KB | $3.3\times10^5$ | instant |
| $10^3$ | $3.8$ MB | $3.3\times10^8$ | $3$ ms |
| $10^4$ | $382$ MB | $3.3\times10^{11}$ | $3.3$ s **per iteration** |
| $10^6$ | $3.6$ TB | $3.3\times10^{17}$ | **$926$ hours per iteration** |
| $10^8$ | $35$ PB | $3.3\times10^{23}$ | — |

> [!warning] The quadratic rate is real and it does not help at scale
> **Newton needs $\approx6$ iterations where gradient descent needs $3.45\kappa$.** At $n=10^6$ and $\kappa=100$:
> $$\textbf{Newton: }6\times926\ \text{hours}\qquad\text{versus}\qquad\textbf{gradient descent: }345\ \text{steps}\times O(n)$$
> **This is why every large-scale optimizer is first-order.** The comparison is not "which converges in fewer iterations" — it is total arithmetic, exactly as [[01 - The Optimization Problem|ch. 01]] Exercise 4(c) warned.

---

### 6. Quasi-Newton: the idea

**Keep the shape $\mathbf x_{k+1}=\mathbf x_k-\alpha_kH_k\mathbf g_k$ but build $H_k\approx F^{-1}$ from gradients alone.**

> [!important] Proposition 11.1 — what $H_k$ must satisfy for descent
> If $H_k$ is symmetric **positive definite** and $\mathbf g_k\ne\mathbf 0$, then with $\alpha_k=\arg\min_{\alpha>0}f(\mathbf x_k-\alpha H_k\mathbf g_k)$ we get $\alpha_k>0$ and $f(\mathbf x_{k+1})<f(\mathbf x_k)$.
>
> **Proof.** $f(\mathbf x_k-\alpha H_k\mathbf g_k)=f(\mathbf x_k)-\alpha\,\mathbf g_k^{\mathsf T}H_k\mathbf g_k+o(\alpha)$, and $\mathbf g_k^{\mathsf T}H_k\mathbf g_k>0$ by positive definiteness. $\blacksquare$
>
> **So *positive definiteness of $H_k$ is the design constraint*, and it is what separates the three update formulas of §7.**

> [!important] The secant condition
> For a quadratic with Hessian $Q$, $\mathbf g_{k+1}-\mathbf g_k=Q(\mathbf x_{k+1}-\mathbf x_k)$. Writing $\Delta\mathbf x^{(k)}=\mathbf x_{k+1}-\mathbf x_k$ and $\Delta\mathbf g^{(k)}=\mathbf g_{k+1}-\mathbf g_k$:
> $$\Delta\mathbf g^{(k)}=Q\,\Delta\mathbf x^{(k)}\qquad\Longleftrightarrow\qquad Q^{-1}\Delta\mathbf g^{(k)}=\Delta\mathbf x^{(k)}$$
> **So require the approximation to reproduce what $Q^{-1}$ does on every step taken so far:**
> $$\boxed{H_{k+1}\,\Delta\mathbf g^{(i)}=\Delta\mathbf x^{(i)},\qquad 0\le i\le k}$$
>
> **This is exactly [[04 - One-Dimensional Search Methods|ch. 04]] §7's secant method in $n$ dimensions:** there, $f''$ was approximated from two values of $f'$; here, $Q^{-1}$ is approximated from differences of $\nabla f$.

> [!important] Two consequences, both remarkable
> **1. After $n$ steps, $H_n$ is exactly $Q^{-1}$.** If $[\Delta\mathbf g^{(0)}|\cdots|\Delta\mathbf g^{(n-1)}]$ is non-singular, the $n$ secant conditions determine $H_n$ uniquely:
> $$H_n=\big[\Delta\mathbf x^{(0)}|\cdots|\Delta\mathbf x^{(n-1)}\big]\big[\Delta\mathbf g^{(0)}|\cdots|\Delta\mathbf g^{(n-1)}\big]^{-1}=Q^{-1}$$
>
> **2. Quasi-Newton methods are conjugate direction methods** (Theorem 11.1): the directions $\mathbf d^{(0)},\dots,\mathbf d^{(k)}$ generated are **$Q$-conjugate**. **Hence a quadratic in $n$ variables is solved in at most $n$ steps** — see [[07 - Conjugate Direction Methods|ch. 07]].
>
> **So quasi-Newton is exact on quadratics in $n$ steps, using only gradients.** That is the whole selling point.

**The secant conditions do not determine $H_{k+1}$ uniquely** — there are $n$ equations and $\tfrac12n(n+1)$ unknowns. **The remaining freedom is what the three formulas of §7 spend differently.**

---

### 7. Rank-one, DFP and BFGS

Each computes $H_{k+1}$ by adding a low-rank correction to $H_k$.

> [!important] The three formulas
> **Rank one (SRS)** — correction $a_k\mathbf z^{(k)}\mathbf z^{(k)\mathsf T}$, rank 1:
> $$H_{k+1}=H_k+\frac{\big(\Delta\mathbf x^{(k)}-H_k\Delta\mathbf g^{(k)}\big)\big(\Delta\mathbf x^{(k)}-H_k\Delta\mathbf g^{(k)}\big)^{\mathsf T}}{\Delta\mathbf g^{(k)\mathsf T}\big(\Delta\mathbf x^{(k)}-H_k\Delta\mathbf g^{(k)}\big)}$$
> **Simple, and it does not preserve positive definiteness** — the denominator can be negative or zero. **Not used in practice.**
>
> **DFP** (Davidon–Fletcher–Powell) — rank 2:
> $$H_{k+1}^{\mathrm{DFP}}=H_k+\frac{\Delta\mathbf x^{(k)}\Delta\mathbf x^{(k)\mathsf T}}{\Delta\mathbf x^{(k)\mathsf T}\Delta\mathbf g^{(k)}}-\frac{H_k\Delta\mathbf g^{(k)}\Delta\mathbf g^{(k)\mathsf T}H_k}{\Delta\mathbf g^{(k)\mathsf T}H_k\Delta\mathbf g^{(k)}}$$
> **Preserves positive definiteness** (C&Ż prove it via Cauchy–Schwarz). But "on larger non-quadratic problems it has a tendency to get stuck", because $H_k$ can become nearly singular.
>
> **BFGS** (Broyden–Fletcher–Goldfarb–Shanno, 1970):
> $$H_{k+1}^{\mathrm{BFGS}}=H_k+\left(1+\frac{\Delta\mathbf g^{(k)\mathsf T}H_k\Delta\mathbf g^{(k)}}{\Delta\mathbf g^{(k)\mathsf T}\Delta\mathbf x^{(k)}}\right)\frac{\Delta\mathbf x^{(k)}\Delta\mathbf x^{(k)\mathsf T}}{\Delta\mathbf x^{(k)\mathsf T}\Delta\mathbf g^{(k)}}-\frac{H_k\Delta\mathbf g^{(k)}\Delta\mathbf x^{(k)\mathsf T}+\big(H_k\Delta\mathbf g^{(k)}\Delta\mathbf x^{(k)\mathsf T}\big)^{\mathsf T}}{\Delta\mathbf g^{(k)\mathsf T}\Delta\mathbf x^{(k)}}$$

> [!important] Where BFGS comes from — the duality trick, and it is elegant
> **Instead of approximating $Q^{-1}$ by $H_k$, approximate $Q$ itself by $B_k$.** The secant condition becomes
> $$\Delta\mathbf g^{(i)}=B_{k+1}\Delta\mathbf x^{(i)}$$
> — **the same equation with the roles of $\Delta\mathbf x$ and $\Delta\mathbf g$ swapped.**
>
> **So every update formula has a *dual* (or *complementary*) formula, obtained by interchanging $B\leftrightarrow H$ and $\Delta\mathbf x\leftrightarrow\Delta\mathbf g$.** Applying that swap to DFP gives
> $$B_{k+1}^{\mathrm{BFGS}}=B_k+\frac{\Delta\mathbf g^{(k)}\Delta\mathbf g^{(k)\mathsf T}}{\Delta\mathbf g^{(k)\mathsf T}\Delta\mathbf x^{(k)}}-\frac{B_k\Delta\mathbf x^{(k)}\Delta\mathbf x^{(k)\mathsf T}B_k}{\Delta\mathbf x^{(k)\mathsf T}B_k\Delta\mathbf x^{(k)}}$$
> and inverting it — twice via the **Sherman–Morrison formula**
> $$(A+\mathbf u\mathbf v^{\mathsf T})^{-1}=A^{-1}-\frac{A^{-1}\mathbf u\mathbf v^{\mathsf T}A^{-1}}{1+\mathbf v^{\mathsf T}A^{-1}\mathbf u}$$
> — gives the $H_{k+1}^{\mathrm{BFGS}}$ displayed above.
>
> **BFGS is the dual of DFP. That is the entire derivation.**

| | Rank one | DFP | **BFGS** |
|---|---|---|---|
| Rank of correction | 1 | 2 | 2 |
| Preserves $H_k\succ0$ | ✘ | ✔ | ✔ |
| Satisfies secant condition | ✔ | ✔ | ✔ |
| Conjugate directions, exact in $n$ steps on a quadratic | ✔ | ✔ | ✔ |
| Robust to **inexact** line searches | ✘ | ✘ | **✔** |
| Used in practice | no | rarely | **yes, universally** |

> [!important] Why BFGS won, and it is a practical reason not a theoretical one
> **"The BFGS update is reasonably robust when the line searches are sloppy."** That single property is decisive: it means you can use **Armijo backtracking** instead of an exact line search, saving most of the work per iteration ([[04 - One-Dimensional Search Methods|ch. 04]] §9).
>
> **And this is exactly where the Wolfe curvature condition earns its place.** Positive definiteness of $H_{k+1}$ requires
> $$\Delta\mathbf x^{(k)\mathsf T}\Delta\mathbf g^{(k)}>0$$
> (look at the denominators above), and **the Wolfe condition $\phi_k'(\alpha_k)\ge\eta\phi_k'(0)$ is precisely what guarantees it.** Without Wolfe, BFGS can produce an indefinite $H_k$ and a non-descent direction. **That is why ch. 04 §9 said the curvature condition is needed for quasi-Newton and not for gradient descent.**

---

### 8. L-BFGS, and the honest modern position

> [!important] Limited-memory BFGS
> **$H_k$ is never formed.** BFGS's update expresses $H_k\mathbf g_k$ as a function of $H_0$ and the pairs $\{(\Delta\mathbf x^{(i)},\Delta\mathbf g^{(i)})\}$. **Keep only the last $m$ pairs (typically $m=5$–$20$) and recompute $H_k\mathbf g_k$ by a two-loop recursion.**
>
> | Method | Storage | Work per step |
> |---|---|---|
> | Newton | $\tfrac12n^2$ | $\tfrac13n^3$ |
> | BFGS | $\tfrac12n^2$ | $O(n^2)$ |
> | **L-BFGS ($m=10$)** | $\mathbf{2mn}$ | $O(mn)$ |
> | Gradient descent | $n$ | $O(n)$ |
>
> **At $n=10^6$: Newton needs 3.6 TB, BFGS needs 3.6 TB, L-BFGS needs 153 MB.** *(Verified.)*
>
> **L-BFGS is the default in `scipy.optimize.minimize` and is the right tool for a smooth deterministic problem with $n$ up to millions.**

> [!warning] And yet deep learning does not use it — the reason is stochasticity, not size
> **L-BFGS solves the size problem completely. It does not survive stochastic gradients**, and that is why it is absent from deep learning:
> 1. **The secant pairs are noisy.** $\Delta\mathbf g^{(k)}$ computed from two *different* mini-batches measures batch-to-batch variation, not curvature. The estimate of $Q^{-1}$ is then garbage.
> 2. **Wolfe conditions need a line search**, and a line search needs a consistent $\phi_k$, which a resampled mini-batch does not provide.
> 3. **The Hessian is not positive definite anywhere** in a non-convex landscape, so the whole design constraint of §6 is unavailable.
>
> **So the modern hierarchy is:**
>
> | Problem | Method |
> |---|---|
> | $n$ small, $f$ smooth, deterministic | **Newton** (with damping / LM) |
> | $n$ medium–large, $f$ smooth, deterministic | **L-BFGS** |
> | $n$ huge, $f$ stochastic and non-convex | **SGD with momentum, or Adam** ([[05 - Gradient Methods\|ch. 05]] §8) |
>
> **Adam is a *diagonal* quasi-Newton method whose curvature estimate comes from squared gradients rather than gradient differences** — the same idea as this chapter, at the only budget stochastic optimization allows.

---

## ✏️ Exercises

> [!question] Exercise 1 — Newton on a quadratic *(easy)*
> Let $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ with $Q=\begin{pmatrix}5&-3\\-3&2\end{pmatrix}$ and $\mathbf b=(0,1)^{\mathsf T}$.
> **(a)** Verify $Q\succ0$ and compute $\mathbf x^*$.
> **(b)** Run one Newton step from $\mathbf x_0=(0,0)^{\mathsf T}$.
> **(c)** How many steepest-descent iterations would the same accuracy need?

> [!example]- Solution
> **(a)** Leading minors $5>0$ and $\det Q=10-9=1>0$, so $Q\succ0$ by Sylvester. Then
> $$Q^{-1}=\frac{1}{1}\begin{pmatrix}2&3\\3&5\end{pmatrix},\qquad \mathbf x^*=Q^{-1}\mathbf b=\begin{pmatrix}2&3\\3&5\end{pmatrix}\begin{pmatrix}0\\1\end{pmatrix}=\boxed{(3,\ 5)^{\mathsf T}}$$
>
> **(b)** $\mathbf g_0=Q\mathbf x_0-\mathbf b=(0,-1)^{\mathsf T}$ and $F_0=Q$. Solving $Q\mathbf d_0=-\mathbf g_0=(0,1)^{\mathsf T}$:
> $$\mathbf d_0=Q^{-1}(0,1)^{\mathsf T}=(3,5)^{\mathsf T}\ \Longrightarrow\ \mathbf x_1=(0,0)+(3,5)=(3,5)^{\mathsf T}=\mathbf x^*$$
> **One step, exactly** — as §2 guarantees for any quadratic from any starting point.
>
> **(c)** The eigenvalues of $Q$ satisfy $\lambda^2-7\lambda+1=0$, giving $\lambda=\tfrac{7\pm\sqrt{45}}{2}$, i.e. $6.854$ and $0.1459$. So
> $$\kappa=\frac{6.854}{0.1459}=46.98$$
> By [[05 - Gradient Methods|ch. 05]] Exercise 3, steepest descent would need $\approx3.45\times47\approx\boxed{162\ \text{iterations}}$ for six digits, against Newton's **one**.
>
> **But note the cost asymmetry even here.** Newton's single step required factorising a $2\times2$ matrix. **At $n=2$ that is free; the whole content of §5 is what happens to that comparison as $n$ grows.**

---

> [!question] Exercise 2 — the hypothesis nobody checks *(medium)*
> Chong & Żak's showcase example for Newton's method is the **Powell function**
> $$f(\mathbf x)=(x_1+10x_2)^2+5(x_3-x_4)^2+(x_2-2x_3)^4+10(x_1-x_4)^4$$
> from $\mathbf x_0=(3,-1,0,1)^{\mathsf T}$, with $f(\mathbf x_0)=215$.
> **(a)** Run Newton's method and tabulate $f(\mathbf x_k)$ for $k=0,\dots,7$.
> **(b)** What is the ratio $f(\mathbf x_{k+1})/f(\mathbf x_k)$? Is the convergence quadratic?
> **(c)** Find $\mathbf x^*$ and compute $\nabla^2f(\mathbf x^*)$. What has gone wrong?
> **(d)** What is the general lesson?

> [!example]- Solution
> **(a)** *(All values verified against the book's; the gradient, the Hessian and its inverse at $\mathbf x_0$ reproduce to four decimal places.)*
>
> | $k$ | $\mathbf x_k$ | $f(\mathbf x_k)$ |
> |---|---|---|
> | 0 | $(3,\ -1,\ 0,\ 1)$ | $215$ |
> | 1 | $(1.5873,\ -0.1587,\ 0.2540,\ 0.2540)$ | $31.80$ |
> | 2 | $(1.0582,\ -0.1058,\ 0.1693,\ 0.1693)$ | $6.282$ |
> | 3 | $(0.7055,\ -0.0705,\ 0.1129,\ 0.1129)$ | $1.241$ |
> | 4 | $(0.4703,\ -0.0470,\ 0.0752,\ 0.0752)$ | $0.2451$ |
> | 5 | $(0.3135,\ -0.0314,\ 0.0502,\ 0.0502)$ | $0.04842$ |
> | 6 | $(0.2090,\ -0.0209,\ 0.0334,\ 0.0334)$ | $0.009564$ |
> | 7 | $(0.1394,\ -0.0139,\ 0.0223,\ 0.0223)$ | $0.001889$ |
>
> **(b)** The ratios are
> $$0.1479,\ \ 0.1975,\ \ 0.1975,\ \ 0.1975,\ \ 0.1975,\ \ 0.1975,\ \dots$$
> **A constant ratio is the signature of *linear* convergence, not quadratic.** And the constant is exactly
> $$\left(\frac23\right)^4=0.19753$$
> **Looking at the iterates: each component is multiplied by exactly $\tfrac23$ every step** ($1.5873\to1.0582\to0.7055$). Since $f$ is quartic near the origin, $f$ contracts by $(2/3)^4$. **The method converges linearly with ratio $2/3$ in $\mathbf x$.**
>
> **(c)** From the iterates, $\mathbf x^*=\mathbf 0$ (and indeed $f(\mathbf 0)=0$ with $f\ge0$, so it is the global minimizer). The Hessian there is
> $$\nabla^2f(\mathbf 0)=\begin{pmatrix}2&20&0&0\\20&200&0&0\\0&0&10&-10\\0&0&-10&10\end{pmatrix}$$
> with eigenvalues $\{202,\ 20,\ \mathbf 0,\ \mathbf 0\}$ and $\det=0$.
>
> $$\boxed{F(\mathbf x^*)\ \text{is singular — Theorem 9.1's hypothesis fails.}}$$
>
> *(Structurally: near $\mathbf 0$ the two quadratic terms are $(x_1+10x_2)^2$ and $5(x_3-x_4)^2$, which are rank-deficient — they vanish on a 2-dimensional subspace. The curvature in those two directions comes only from the quartic terms, and quartic curvature vanishes at the origin.)*
>
> **(d) Three lessons, in order of importance.**
> 1. **"Newton's method converges quadratically" is conditional, and the condition is $F(\mathbf x^*)\succ0$** — not merely "$f$ is smooth" or "the method converges."
> 2. **A singular Hessian at the solution is not exotic.** It happens whenever the objective is flat to higher than second order in some direction — which is the generic situation for **over-parameterised models**, where many parameter directions do not affect the loss at all. **Every modern neural network has a massively rank-deficient Hessian at its minima.**
> 3. **Chong & Żak present this example immediately before Theorem 9.1 and never remark that it violates the theorem's hypothesis.** The book is not wrong — it claims nothing about this example's rate — **but a reader would reasonably infer that the observed behaviour is quadratic convergence, and it is not.** *(This is a pedagogical gap, not an error; it is recorded here because checking it takes thirty seconds and changes what the example teaches.)*

---

> [!question] Exercise 3 — Levenberg–Marquardt *(medium)*
> Let $f(\mathbf x)=x_1^2+x_2^4-x_2^2$ and $\mathbf x_0=(0,\ 0.3)^{\mathsf T}$.
> **(a)** Find all stationary points and classify them.
> **(b)** Compute $\nabla f(\mathbf x_0)$ and $\nabla^2f(\mathbf x_0)$. Is the Hessian positive definite?
> **(c)** Take one full Newton step. What happens?
> **(d)** Apply Levenberg–Marquardt for $\mu\in\{0.5,\ 1,\ 2,\ 5,\ 50\}$. For which $\mu$ is $F+\mu I\succ0$, and for which does the step actually decrease $f$?
> **(e)** Explain the discrepancy between those two answers.

> [!example]- Solution
> **(a)** $\nabla f=(2x_1,\ 4x_2^3-2x_2)^{\mathsf T}=\mathbf 0$ gives $x_1=0$ and $x_2(4x_2^2-2)=0$, so $x_2\in\{0,\pm1/\sqrt2\}$.
> $$\nabla^2f=\begin{pmatrix}2&0\\0&12x_2^2-2\end{pmatrix}$$
>
> | Point | $\nabla^2f$ | Verdict |
> |---|---|---|
> | $(0,\ 0)$ | $\operatorname{diag}(2,-2)$ — indefinite | **saddle**, $f=0$ |
> | $(0,\ \pm1/\sqrt2)$ | $\operatorname{diag}(2,4)\succ0$ | **strict global minimizers**, $f=-\tfrac14$ |
>
> **(b)** $\nabla f(\mathbf x_0)=(0,\ 4(0.027)-0.6)^{\mathsf T}=(0,\ -0.492)^{\mathsf T}$ and
> $$\nabla^2f(\mathbf x_0)=\operatorname{diag}(2,\ 12(0.09)-2)=\operatorname{diag}(2,\ -0.92)$$
> Eigenvalues $\{2,\ -0.92\}$: **indefinite, not positive definite.** $f(\mathbf x_0)=-0.0819$.
>
> **(c)** $\mathbf d=-F^{-1}\mathbf g=-\left(0,\ \dfrac{-0.492}{-0.92}\right)=(0,\ -0.5348)$, so
> $$\mathbf x_1=(0,\ -0.2348),\qquad f(\mathbf x_1)=-0.0521$$
> **$f$ increased from $-0.0819$ to $-0.0521$.** And worse: **the step moved *away* from the minimizer at $x_2=+0.7071$, toward the saddle at the origin.** The negative curvature in the $x_2$ direction made Newton treat a downhill direction as uphill and reverse it.
>
> **(d)** $F+\mu I=\operatorname{diag}(2+\mu,\ \mu-0.92)$, so **$F+\mu I\succ0\iff\mu>0.92$.**
>
> | $\mu$ | eigenvalues of $F+\mu I$ | $\succ0$? | $\mathbf x_1$ | $f(\mathbf x_1)$ | decreased? |
> |---|---|---|---|---|---|
> | $0.5$ | $\{-0.42,\ 2.5\}$ | ✘ | $(0,\ -0.8714)$ | $-0.1827$ | **yes** (by luck) |
> | $1$ | $\{0.08,\ 3\}$ | ✔ | $(0,\ 6.45)$ | $+1689$ | **no** |
> | $2$ | $\{1.08,\ 4\}$ | ✔ | $(0,\ 0.7556)$ | $\mathbf{-0.2450}$ | **yes** |
> | $5$ | $\{4.08,\ 7\}$ | ✔ | $(0,\ 0.4206)$ | $-0.1456$ | yes |
> | $50$ | $\{49.08,\ 52\}$ | ✔ | $(0,\ 0.3100)$ | $-0.0869$ | yes |
>
> **$\mu=2$ is nearly perfect: $f=-0.2450$ against the true minimum $-0.25$, in one step.** And as $\mu$ grows, the step shrinks toward the tiny gradient step $-\mathbf g/\mu$ — verified: at $\mu=1000$, $\mathbf d=(0,\ 4.9245\times10^{-4})$ against $-\mathbf g/1000=(0,\ 4.92\times10^{-4})$.
>
> **(e) The two answers differ in *both* directions, and both discrepancies are instructive.**
>
> - **$\mu=1$ is positive definite and still goes uphill.** Theorem 9.2 promises a descent *direction*, i.e. that $f$ decreases for **all sufficiently small $\alpha$** — it says nothing about $\alpha=1$. At $\mu=1$ the smallest eigenvalue is $0.08$, so $(F+\mu I)^{-1}$ has a factor of $12.5$ and the step is huge ($6.15$), landing far outside the region where the quadratic model is valid. **Positive definiteness alone is not enough; you also need a line search.**
> - **$\mu=0.5$ is not positive definite and decreases $f$ anyway.** With $\mu<0.92$ the second diagonal entry is still negative, so the direction is reversed — but the function happens to be symmetric, and the step overshoots all the way past the *other* minimizer at $-0.7071$. **A decrease obtained this way is luck, not a guarantee, and the next step would not be so lucky.**
>
> **The practical algorithm therefore does both:** choose $\mu$ large enough for positive definiteness, **and** run Armijo backtracking on the resulting direction. **That combination — LM for the direction, line search for the length — is what "damped Newton" means in practice, and it is exactly what `scipy`'s trust-region and `least_squares` implementations do.**

---

> [!question] Exercise 4 — BFGS builds $Q^{-1}$ *(hard)*
> Minimise $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x+\log\pi$ with $Q=\begin{pmatrix}5&-3\\-3&2\end{pmatrix}$, $\mathbf b=(0,1)^{\mathsf T}$, using BFGS from $\mathbf x_0=(0,0)^{\mathsf T}$ with $H_0=I$ and exact line searches.
> **(a)** Carry out both iterations, giving $\mathbf d^{(k)}$, $\alpha_k$, $\mathbf x_{k+1}$ and $H_{k+1}$.
> **(b)** Verify that $H_2=Q^{-1}$ and $\mathbf x_2=\mathbf x^*$.
> **(c)** Why must this happen, and what would happen with $n=100$?
> **(d)** Repeat conceptually with DFP. Does the same thing happen? Then why is BFGS preferred?

> [!example]- Solution
> **(a)** $\nabla f(\mathbf x)=Q\mathbf x-\mathbf b$, and for a quadratic the exact step is $\alpha_k=-\dfrac{\mathbf g_k^{\mathsf T}\mathbf d^{(k)}}{\mathbf d^{(k)\mathsf T}Q\mathbf d^{(k)}}$.
>
> **Iteration 0.** $\mathbf g_0=Q\mathbf 0-\mathbf b=(0,-1)^{\mathsf T}$, so $\mathbf d^{(0)}=-H_0\mathbf g_0=(0,1)^{\mathsf T}$.
> $$\alpha_0=-\frac{(0,-1)\cdot(0,1)}{(0,1)Q(0,1)^{\mathsf T}}=-\frac{-1}{2}=\frac12,\qquad \mathbf x_1=(0,\ \tfrac12)^{\mathsf T}$$
> With $\Delta\mathbf x^{(0)}=(0,\tfrac12)$ and $\Delta\mathbf g^{(0)}=Q\Delta\mathbf x^{(0)}=(-\tfrac32,1)$, the BFGS update gives
> $$H_1=\begin{pmatrix}1&1.5\\1.5&2.75\end{pmatrix}$$
>
> **Iteration 1.** $\mathbf g_1=Q\mathbf x_1-\mathbf b=(-1.5,\ 0)^{\mathsf T}$, so $\mathbf d^{(1)}=-H_1\mathbf g_1=(1.5,\ 2.25)^{\mathsf T}$ and $\alpha_1=2$, giving
> $$\mathbf x_2=(0,\ 0.5)+2(1.5,\ 2.25)=(3,\ 5)^{\mathsf T}$$
>
> **(b)** The second BFGS update yields
> $$H_2=\begin{pmatrix}2&3\\3&5\end{pmatrix}=Q^{-1}\ \checkmark\qquad\text{and}\qquad \mathbf x_2=(3,5)^{\mathsf T}=Q^{-1}\mathbf b=\mathbf x^*\ \checkmark$$
> *(Both verified exactly.)*
>
> **(c) It must happen, for two independent reasons, and it is worth seeing both.**
> - **The secant conditions force it.** After $n=2$ steps, $H_2$ satisfies $H_2\Delta\mathbf g^{(i)}=\Delta\mathbf x^{(i)}$ for $i=0,1$. The two $\Delta\mathbf g$'s are linearly independent, so they span $\mathbb R^2$, and a linear map is determined by its action on a basis. Since $Q^{-1}$ satisfies the same equations, $H_2=Q^{-1}$.
> - **The conjugate-direction property forces it** (Theorem 11.1): $\mathbf d^{(0)}$ and $\mathbf d^{(1)}$ are $Q$-conjugate, and **exact line searches along $n$ conjugate directions minimise a quadratic exactly** ([[07 - Conjugate Direction Methods|ch. 07]]).
>
> **At $n=100$: BFGS reaches $\mathbf x^*$ in at most 100 iterations using only gradients**, against Newton's one iteration using the Hessian. **The trade is $n$ gradient evaluations versus one Hessian evaluation plus one $O(n^3)$ solve** — and for a non-quadratic $f$ this is far better than it sounds, because BFGS's approximation keeps improving while a Hessian would have to be recomputed at every point anyway.
>
> **(d) DFP does exactly the same thing here** — I checked: it also gives $H_2=Q^{-1}$ and $\mathbf x_2=(3,5)$. **Both satisfy the secant conditions, so on a quadratic with exact line searches they are indistinguishable.**
>
> **The difference appears only where the assumptions break:**
>
> | | DFP | BFGS |
> |---|---|---|
> | Quadratic $f$, exact line search | identical | identical |
> | **Non-quadratic $f$** | $H_k$ tends to become **nearly singular** and the method stalls | stays well conditioned |
> | **Inexact (sloppy) line search** | degrades badly | **robust** |
>
> **So the preference for BFGS is empirical and about robustness, not about anything provable on quadratics.** *(It is also the reason the Wolfe curvature condition of [[04 - One-Dimensional Search Methods|ch. 04]] §9 exists: it guarantees $\Delta\mathbf x^{\mathsf T}\Delta\mathbf g>0$, which keeps BFGS's denominators positive and $H_{k+1}\succ0$ under an *inexact* line search.)*

---

> [!question] Exercise 5 — the cost accounting *(medium–hard)*
> A smooth convex $f$ has condition number $\kappa=100$. Compare gradient descent, L-BFGS and Newton for $n=10^3$, $n=10^5$ and $n=10^7$. Assume one gradient costs $c$, one Hessian costs $n\cdot c$, a Cholesky factorisation costs $\tfrac13n^3$ flops, the machine does $10^{11}$ flops/s, and 8 bytes per double.
> **(a)** Estimate the iterations each needs for six digits.
> **(b)** Estimate storage.
> **(c)** Which method wins at each $n$?
> **(d)** What does the answer become if the gradients are stochastic?

> [!example]- Solution
> **(a) Iteration counts** *(six digits, $\kappa=100$)*:
>
> | Method | Rate | Iterations |
> |---|---|---|
> | Gradient descent | $\left(\frac{\kappa-1}{\kappa+1}\right)^2=0.9608$ | $\approx3.45\kappa=\mathbf{346}$ |
> | L-BFGS | superlinear in practice | $\approx\mathbf{30}$–$\mathbf{60}$ |
> | Newton | quadratic | $\approx\mathbf{6}$ |
>
> **(b) Storage:**
>
> | $n$ | Gradient descent ($n$) | L-BFGS ($2mn$, $m=10$) | Newton / BFGS ($\tfrac12n^2$) |
> |---|---|---|---|
> | $10^3$ | $8$ KB | $156$ KB | $3.8$ MB |
> | $10^5$ | $800$ KB | $16$ MB | $38$ GB |
> | $10^7$ | $80$ MB | $1.5$ GB | $381$ TB |
>
> **(c) Total cost:**
>
> | $n$ | Gradient descent | L-BFGS | Newton |
> |---|---|---|---|
> | $10^3$ | $346c$ | $\approx45c+O(mn)$ | $6\times(10^3c+3.3\ \text{ms})$ |
> | $10^5$ | $346c$ | $\approx45c$ | $6\times(10^5c+3\,300\ \text{s})$, **38 GB** |
> | $10^7$ | $346c$ | $\approx45c$, $1.5$ GB | **impossible — 381 TB** |
>
> **Verdict:**
> - **$n=10^3$: Newton wins** if $c$ is large (an expensive $f$), since 6 iterations beat 346. The $3.3$ ms factorisation is negligible. **This is the classical regime the books were written for.**
> - **$n=10^5$: L-BFGS wins decisively.** Newton needs $55$ minutes of *linear algebra alone* per iteration and 38 GB of memory; L-BFGS needs 16 MB and $\approx45$ gradients.
> - **$n=10^7$: Newton is impossible and L-BFGS is marginal.** Gradient descent's 346 iterations at $O(n)$ each is the only certainly feasible option — **though 346 is a fixed count independent of $n$, which is exactly why first-order methods scale.**
>
> **The crossover is not about convergence rates at all.** Newton's rate is unbeatable at every $n$; **what changes is that $\tfrac13n^3$ grows faster than anything the rate can save.**
>
> **(d) With stochastic gradients the table is rewritten, and not in anyone's favour.**
> 1. **Gradient descent's rate degrades from linear to $O(1/k)$**, so "346 iterations" becomes a schedule-dependent number that is far larger. **But each iteration now costs a mini-batch, not a full pass**, so wall-clock time usually improves by more than the rate degrades.
> 2. **L-BFGS breaks.** Its secant pairs $(\Delta\mathbf x,\Delta\mathbf g)$ measure batch-to-batch noise rather than curvature, and its line search has no consistent $\phi_k$ to search along. **This is why L-BFGS is standard in scientific computing and absent from deep learning** — the obstacle is noise, not size.
> 3. **Newton is doubly excluded**, by cost and by the non-positive-definite Hessian of a non-convex loss.
>
> **What survives is the diagonal approximation** — Adam and RMSProp — **which is this chapter's idea shrunk to the only budget stochastic optimization permits: $O(n)$ storage, no line search, and a curvature estimate built from squared gradients rather than gradient differences.**

---

## 📝 Summary

- **Newton's method minimises the local quadratic model:** $\mathbf x_{k+1}=\mathbf x_k-F_k^{-1}\mathbf g_k$. **Implement it as *solve* $F_k\mathbf d_k=-\mathbf g_k$, never as an explicit inverse.**
- **On a quadratic it lands on $\mathbf x^*$ in one step from anywhere** — it is [[05 - Gradient Methods|ch. 05]]'s preconditioner $Q^{-1}$ applied exactly, so $\kappa$ becomes 1.
- **Quadratic convergence requires (i) a nearby start and (ii) $F(\mathbf x^*)$ invertible.** **When (ii) fails the rate drops to linear** — Chong & Żak's own Powell example converges linearly with ratio $2/3$ because its Hessian at the minimizer has two zero eigenvalues.
- **It solves $\nabla f=\mathbf 0$ and nothing more**, so it converges to maxima and saddles as readily as to minima.
- **Three failure modes:** the full step may increase $f$ even when $F_k\succ0$; $F_k$ may be indefinite (uphill direction); $F_k$ may be singular (no step at all).
- **Damping fixes the first** (take Newton's direction, line-search the length — and start Armijo at $\alpha=1$ so the quadratic rate survives). **Levenberg–Marquardt fixes the other two**: $(F+\mu I)$ shifts every eigenvalue by $\mu$, and **$\mu$ dials continuously from Newton ($\mu\to0$) to gradient descent ($\mu\to\infty$)**.
- **The cost is $\tfrac12n^2$ storage and $\tfrac13n^3$ flops per iteration.** At $n=10^6$ that is 3.6 TB and 926 hours **per step** — which is why Newton lost, despite an unbeatable rate.
- **Quasi-Newton keeps $\mathbf x_{k+1}=\mathbf x_k-\alpha_kH_k\mathbf g_k$ and builds $H_k\approx Q^{-1}$ from gradients**, via the **secant condition** $H_{k+1}\Delta\mathbf g^{(i)}=\Delta\mathbf x^{(i)}$. After $n$ steps $H_n=Q^{-1}$ exactly, the directions are $Q$-conjugate, and a quadratic is solved in $\le n$ steps.
- **The design constraint is $H_k\succ0$**, which the rank-one formula violates, DFP satisfies, and **BFGS satisfies while also tolerating sloppy line searches** — the reason it is universal. **BFGS is the dual of DFP**, obtained by swapping $\Delta\mathbf x\leftrightarrow\Delta\mathbf g$ and inverting via Sherman–Morrison.
- **L-BFGS stores only the last $m$ secant pairs**, reducing $\tfrac12n^2$ to $2mn$ — 153 MB instead of 3.6 TB at $n=10^6$. **It solves the size problem but not the noise problem**, which is why deep learning uses Adam instead.

---

## ⚠️ Important Notes

> [!warning] The six errors
> 1. **Writing `inv(H) @ g`.** Solve the system: three times cheaper and numerically better.
> 2. **Quoting quadratic convergence without checking $F(\mathbf x^*)$ is non-singular.** Exercise 2.
> 3. **Assuming $F_k\succ0$ makes the full step a descent step.** It makes the *direction* a descent direction; Exercise 3(d) exhibits a positive definite case where $\alpha=1$ goes uphill.
> 4. **Assuming a converged Newton run found a minimum.** It found a stationary point. Check the Hessian's inertia if you can afford to.
> 5. **Using BFGS with an Armijo-only line search.** The **Wolfe curvature condition** is what keeps $\Delta\mathbf x^{\mathsf T}\Delta\mathbf g>0$ and hence $H_k\succ0$.
> 6. **Comparing methods by iteration count.** Compare total arithmetic, as in Exercise 5.

> [!tip] Which method, in one table
> | Situation | Method |
> |---|---|
> | $n\lesssim10^3$, $f$ smooth, Hessian available | **Newton**, damped, with LM when $F$ is indefinite |
> | Nonlinear least squares | **Levenberg–Marquardt** — it was invented for exactly this |
> | $n$ up to $\sim10^7$, smooth, deterministic gradients | **L-BFGS** |
> | Non-convex, stochastic gradients, $n$ huge | **SGD + momentum, or Adam** |
> | $f$ non-smooth | none of these — subgradient or proximal methods, [[12 - Convex Programming and Constrained Algorithms\|ch. 12]] |

> [!note] Where this chapter connects
> - **[[05 - Gradient Methods|Ch. 05]] §7** predicted this chapter exactly: Newton is the $O(n^3)$ preconditioner, BFGS the $O(n^2)$ one, L-BFGS and Adam the $O(n)$ ones.
> - **[[04 - One-Dimensional Search Methods|Ch. 04]]** — §§6–7 there are this chapter in one dimension; **the secant method is BFGS with $n=1$**, and the Wolfe condition of §9 exists for BFGS's sake.
> - **[[07 - Conjugate Direction Methods|Ch. 07]]** — quasi-Newton methods *are* conjugate direction methods (Theorem 11.1), and CG is the $O(n)$ member of the same family.
> - **[[08 - Least Squares and Linear Equations|Ch. 08]]** — Newton's inner step is a linear solve, and **Gauss–Newton and Levenberg–Marquardt are its specialisation to least squares.**
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]** — **Newton–Raphson for the MLE is this chapter**, and **Fisher scoring replaces the observed Hessian by the expected information**, a curvature approximation in exactly the quasi-Newton spirit. The **EM algorithm** is another.
> - **[[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]** supplies the eigenvalue-shift fact that makes Levenberg–Marquardt work, and the Cholesky factorisation that makes the inner solve affordable.

---

> [!warning] Gaps in the source material
> **Source.** Chong & Żak ch. 9 (Newton) and ch. 11 (quasi-Newton), with Luenberger & Ye §8.5 and ch. 10 used to check statements. **Chong & Żak's ch. 10 (conjugate directions) is deliberately deferred to [[07 - Conjugate Direction Methods|ch. 07]] of these notes**, which is why Theorem 11.1's conjugacy result is stated here and proved there.
>
> **OCR damage:**
> - **Every matrix in Example 9.1 loses its brackets and row structure.** The $4\times4$ Hessian and its inverse arrive as unstructured runs of numbers; **both were reconstructed and then verified entry by entry against an independent computation** (see below).
> - **`F(x^)`, `F(xW)`, `F(x{k})`, `Fiaj'^J`, `F(x{ })` are all $F(\mathbf x^{(k)})$**; `g^`, `gW`, `0(1)`, `flfW`, `Ä|(fc)` are $\mathbf g^{(k)}$; `μ^`, `μ&`, `M*J`, `/ifc` are $\mu_k$; `Δα(<)`, `Δατ°\`, `Αχ^`, `AxW` are $\Delta\mathbf x^{(i)}$; `Ag^`, `Δβ<*\`, `A9(n-l)` are $\Delta\mathbf g^{(i)}$.
> - **The BFGS and DFP update formulas lose all their fraction bars**, so the three terms run together on one line: `HDFP = rf , Δα^>Δ*<*>τ HkAg^Ag^Hk k+1 k + Δχ<*>τΔ0<*> Ag^THkAg^`. **Both formulas were reconstructed from the secant condition and then verified numerically** (Exercise 4).
> - **`denniteness` for "definiteness"**, `objection function` for "objective function", `Prom` for "From", `maximizes` for "maximizer" — ordinary OCR word damage in the prose.
> - **Figures 9.1 (the quadratic model touching $f$ at the current point) and 7.6–7.7 (referenced from ch. 9 for the $f''<0$ failure) are images and are lost.** Figure 9.1 in particular *is* §1's derivation.
>
> **Verification performed.** Everything was recomputed with `numpy`:
> - **C&Ż Example 9.1 (Powell function)**: $f(\mathbf x_0)=215$; the gradient $(306,-144,-2,-310)$; the Hessian $\begin{psmallmatrix}482&20&0&-480\\20&212&-24&0\\0&-24&58&-10\\-480&0&-10&490\end{psmallmatrix}$; its inverse to all four printed decimal places; the Newton step $(1.4127,-0.8413,-0.2540,0.7460)$; and $\mathbf x^{(1)},\mathbf x^{(2)}$ with $f=31.80$ and $6.28$ — **all reproduce exactly.**
>   - **One small discrepancy.** The book prints $\mathbf x^{(3)}=(0.7037,\ -0.0704,\ 0.1121,\ 0.1111)$; exact computation gives $(0.7055,\ -0.0705,\ 0.1129,\ 0.1129)$. **The book's third and fourth components differ from each other, whereas the exact iteration keeps $x_3=x_4$ at every step** (as it did at $\mathbf x^{(1)}$ and $\mathbf x^{(2)}$). The printed $f(\mathbf x^{(3)})=1.24$ matches the exact $1.2409$, so this is **accumulated hand-rounding rather than a substantive error.**
>   - **The substantive finding is (c) of Exercise 2**, recorded above: the Hessian at $\mathbf x^*=\mathbf 0$ has eigenvalues $\{202,20,0,0\}$ and is singular, so **Theorem 9.1's hypothesis fails and the convergence is linear with ratio exactly $(2/3)^4=0.19753$ in $f$**, verified over ten iterations. **The book does not remark on this.**
> - **C&Ż Example 11.4 (BFGS)**: $\mathbf d^{(0)}=(0,1)$, $\alpha_0=\tfrac12$, $\mathbf x^{(1)}=(0,\tfrac12)$, $H_1=\begin{psmallmatrix}1&1.5\\1.5&2.75\end{psmallmatrix}$, and $H_2=\begin{psmallmatrix}2&3\\3&5\end{psmallmatrix}=Q^{-1}$ exactly, with $\mathbf x^{(2)}=(3,5)=\mathbf x^*$. **DFP was also run and gives the identical result**, which is the basis of Exercise 4(d).
> - **Exercise 3**: all Newton and Levenberg–Marquardt steps, the eigenvalues of $F+\mu I$ at five values of $\mu$, the uphill step at $\mu=1$, and the $\mu\to\infty$ limit.
> - **§5 and Exercise 5's cost tables**: storage and flop counts computed directly.
>
> **No mathematical error was found in either book in these chapters.**
>
> **Scope and additions.**
> - **§8 (L-BFGS and the modern position) is my own addition.** Chong & Żak's ch. 11 ends with BFGS in 1970 and never mentions limited memory; Luenberger & Ye mention memoryless quasi-Newton (§10.7) but not the two-loop recursion or its use at scale. **The explanation of *why* L-BFGS fails under stochastic gradients — noisy secant pairs, no consistent line search, no positive definiteness — is mine**, and is the answer to the obvious question a DS reader will have.
> - **§5's cost table and Exercise 5 are my own.** The books state that Hessian evaluation is "computationally expensive for large $n$" without quantifying it; **turning that into 3.6 TB and 926 hours per iteration is what makes the trade-off decidable.**
> - **Exercise 2 is my own analysis of the book's own example.** The computation is straightforward; **the point is that the book's showcase for quadratic convergence does not exhibit quadratic convergence, and that the reason (a singular Hessian at the minimizer) is the generic situation for over-parameterised models.**
> - **The framing of Levenberg–Marquardt, ridge regression and trust regions as one idea is mine**, as is the observation in Exercise 3(e) that positive definiteness and an actual decrease are independent conditions.
> - **The reading of Adam as a diagonal quasi-Newton method** (§8) continues [[05 - Gradient Methods|ch. 05]] §7's framing and is likewise my own.

#optimization #newton-method #quasi-newton #bfgs #dfp #levenberg-marquardt #quadratic-convergence #secant-condition #l-bfgs #sherman-morrison
