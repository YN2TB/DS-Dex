---
subject: Optimization
chapter: 07
tags: [ds, optimization, conjugate-directions, conjugate-gradient, krylov, fletcher-reeves, polak-ribiere, expanding-subspace]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 10; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 9"
---

# Conjugate Direction Methods

> [!abstract] What this chapter is for
> **Chapter 05 was cheap and slow; chapter 06 was fast and expensive. This chapter is the method that is both cheap and fast**, and it is the reason large sparse linear systems are solvable at all.
>
> Chong & Żak's three-line summary of the class is exact:
>
> 1. **Solves a quadratic in $n$ variables in at most $n$ steps.**
> 2. **Needs no Hessian evaluations.**
> 3. **Needs no matrix inversion and no $n\times n$ storage.**
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **$Q$-conjugacy** | $\mathbf d^{(i)\mathsf T}Q\,\mathbf d^{(j)}=0$ — orthogonality *in the metric of the problem* |
> | **2** | The conjugate direction algorithm | **Exact in $n$ steps**, because conjugate directions decouple the problem |
> | **3** | The **expanding subspace theorem** | Each step minimises over a growing subspace, not just a line |
> | **4** | **Conjugate gradient** | Generates the directions on the fly: $\mathbf d^{(k+1)}=-\mathbf g^{(k+1)}+\beta_k\mathbf d^{(k)}$ |
> | **5** | Eliminating $Q$ | **Fletcher–Reeves, Polak–Ribière, Hestenes–Stiefel** — three formulas, identical on quadratics |
> | **6** | Rate and scope | $O(\sqrt\kappa)$ instead of $O(\kappa)$ — **at $\kappa=10^6$, 7,255 iterations instead of 3.5 million** |
>
> **The one-sentence version: replace "perpendicular" with "perpendicular after $Q$ stretches space", and the zig-zag of [[05 - Gradient Methods|ch. 05]] disappears.**

---

## 📘 Main Knowledge

### 1. $Q$-conjugacy

> [!important] Definition
> Let $Q$ be a real symmetric $n\times n$ matrix. Directions $\mathbf d^{(0)},\dots,\mathbf d^{(m)}$ are **$Q$-conjugate** if
> $$\mathbf d^{(i)\mathsf T}Q\,\mathbf d^{(j)}=0\qquad\text{for all }i\ne j$$
>
> **With $Q=I$ this is ordinary orthogonality.** In general it is orthogonality in the inner product $\langle\mathbf u,\mathbf v\rangle_Q=\mathbf u^{\mathsf T}Q\mathbf v$, which is a genuine inner product exactly when $Q\succ0$.

> [!important] Lemma — conjugate implies independent
> If $Q\succ0$ and $\mathbf d^{(0)},\dots,\mathbf d^{(k)}$ are non-zero and $Q$-conjugate, they are **linearly independent**.
>
> **Proof.** Suppose $\sum_i\alpha_i\mathbf d^{(i)}=\mathbf 0$. Premultiply by $\mathbf d^{(j)\mathsf T}Q$: every cross term vanishes by conjugacy, leaving $\alpha_j\,\mathbf d^{(j)\mathsf T}Q\mathbf d^{(j)}=0$. Since $Q\succ0$ and $\mathbf d^{(j)}\ne\mathbf 0$, the quadratic form is positive, so $\alpha_j=0$. $\blacksquare$
>
> **Hence at most $n$ mutually conjugate directions exist, and $n$ of them form a basis.** That is why the algorithms below terminate in $n$ steps.

> [!important] The geometric reading — this is the whole idea
> The level sets of $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ are ellipsoids with axes along $Q$'s eigenvectors. **Change coordinates by $\mathbf y=Q^{1/2}\mathbf x$ and the ellipsoids become spheres.** Then
> $$\mathbf d^{(i)\mathsf T}Q\mathbf d^{(j)}=(Q^{1/2}\mathbf d^{(i)})^{\mathsf T}(Q^{1/2}\mathbf d^{(j)})$$
> **so $Q$-conjugate directions are exactly the directions that become *perpendicular* after the ellipsoids are rounded out.**
>
> **And minimising along $n$ mutually perpendicular directions of a sphere solves it exactly** — each coordinate is independent. **Conjugate directions do the same for an ellipsoid without ever forming $Q^{1/2}$.**

**Constructing them by hand is easy but pointless** (Example 10.1: solve $\mathbf d^{(0)\mathsf T}Q\mathbf d^{(1)}=0$ for the components, then two equations for $\mathbf d^{(2)}$). **The systematic version is Gram–Schmidt with $\langle\cdot,\cdot\rangle_Q$ in place of the dot product** (Exercise 1) — and §4 shows how to avoid even that.

---

### 2. The conjugate direction algorithm and exact termination

> [!important] Basic conjugate direction algorithm
> Given $\mathbf x^{(0)}$ and $Q$-conjugate $\mathbf d^{(0)},\dots,\mathbf d^{(n-1)}$, for $k\ge0$:
> $$\mathbf g^{(k)}=Q\mathbf x^{(k)}-\mathbf b,\qquad \alpha_k=-\frac{\mathbf g^{(k)\mathsf T}\mathbf d^{(k)}}{\mathbf d^{(k)\mathsf T}Q\,\mathbf d^{(k)}},\qquad \mathbf x^{(k+1)}=\mathbf x^{(k)}+\alpha_k\mathbf d^{(k)}$$
>
> **The $\alpha_k$ is the exact line-search minimiser along $\mathbf d^{(k)}$** — the closed form for a quadratic.

> [!important] Theorem — termination in $n$ steps
> For any $\mathbf x^{(0)}$, the algorithm reaches $\mathbf x^{(n)}=\mathbf x^*$, the unique solution of $Q\mathbf x=\mathbf b$.
>
> **Proof.** The $\mathbf d^{(i)}$ are a basis, so $\mathbf x^*-\mathbf x^{(0)}=\sum_{i=0}^{n-1}\beta_i\mathbf d^{(i)}$ for some $\beta_i$. Premultiplying by $\mathbf d^{(k)\mathsf T}Q$ and using conjugacy,
> $$\beta_k=\frac{\mathbf d^{(k)\mathsf T}Q(\mathbf x^*-\mathbf x^{(0)})}{\mathbf d^{(k)\mathsf T}Q\mathbf d^{(k)}}$$
> Meanwhile $\mathbf x^{(k)}-\mathbf x^{(0)}=\sum_{i<k}\alpha_i\mathbf d^{(i)}$, so **$\mathbf d^{(k)\mathsf T}Q(\mathbf x^{(k)}-\mathbf x^{(0)})=0$**, again by conjugacy. Splitting $\mathbf x^*-\mathbf x^{(0)}=(\mathbf x^*-\mathbf x^{(k)})+(\mathbf x^{(k)}-\mathbf x^{(0)})$ therefore gives
> $$\mathbf d^{(k)\mathsf T}Q(\mathbf x^*-\mathbf x^{(0)})=\mathbf d^{(k)\mathsf T}Q(\mathbf x^*-\mathbf x^{(k)})=-\mathbf d^{(k)\mathsf T}\mathbf g^{(k)}$$
> so $\beta_k=\alpha_k$, and $\mathbf x^{(n)}=\mathbf x^{(0)}+\sum\alpha_i\mathbf d^{(i)}=\mathbf x^*$. $\blacksquare$

> [!important] Why this is not obvious
> **In general, minimising along one direction *undoes* the work of a previous minimisation** — this is exactly [[05 - Gradient Methods|ch. 05]]'s zig-zag, where consecutive steps are perpendicular and the method still crawls.
>
> **Conjugacy is the condition under which minimising along $\mathbf d^{(k)}$ leaves the minimisation along $\mathbf d^{(0)},\dots,\mathbf d^{(k-1)}$ intact.** The proof's key line, $\mathbf d^{(k)\mathsf T}Q(\mathbf x^{(k)}-\mathbf x^{(0)})=0$, is precisely that statement. **The problem decouples into $n$ independent one-dimensional minimisations.**

---

### 3. The expanding subspace theorem

> [!important] Lemma 10.2
> In the conjugate direction algorithm, $$\mathbf g^{(k+1)\mathsf T}\mathbf d^{(i)}=0\qquad\text{for all }0\le i\le k$$
>
> **The new gradient is orthogonal to *every* direction used so far, not just the last one.**

*(Compare [[05 - Gradient Methods|ch. 05]] §3, where steepest descent gives only $\mathbf g^{(k+1)\mathsf T}\mathbf d^{(k)}=0$ — orthogonality to the last direction alone. **That one-word difference is the entire improvement.**)*

> [!important] Expanding subspace theorem
> Let $V_k=\mathbf x^{(0)}+\operatorname{span}\{\mathbf d^{(0)},\dots,\mathbf d^{(k)}\}$. Then
> $$f(\mathbf x^{(k+1)})=\min_{\mathbf x\in V_k}f(\mathbf x)$$
>
> **Proof.** Write $D^{(k)}=[\mathbf d^{(0)}|\cdots|\mathbf d^{(k)}]$ and $\phi_k(\boldsymbol\alpha)=f(\mathbf x^{(0)}+D^{(k)}\boldsymbol\alpha)$, a convex quadratic in $\boldsymbol\alpha$. By the chain rule $\nabla\phi_k(\boldsymbol\alpha)^{\mathsf T}=\nabla f(\mathbf x^{(k+1)})^{\mathsf T}D^{(k)}=\mathbf g^{(k+1)\mathsf T}D^{(k)}=\mathbf 0^{\mathsf T}$ by Lemma 10.2. **A stationary point of a convex quadratic is its global minimiser**, so $\mathbf x^{(k+1)}$ minimises $f$ over all of $V_k$. $\blacksquare$

> [!important] What this buys, in one sentence
> **Each iteration does not merely minimise along a line — it minimises over the whole subspace spanned by every direction taken so far.** The subspace expands by one dimension per step, and after $n$ steps it is all of $\mathbb R^n$.
>
> **This is why the method never has to revisit a direction**, and it is the sense in which conjugate directions "remember" without storing anything.

---

### 4. The conjugate gradient algorithm

**The remaining problem: where do the $\mathbf d^{(i)}$ come from?** Gram–Schmidt needs all of $Q$ and $O(n^2)$ storage — which would forfeit the whole advantage. **Conjugate gradient generates them one at a time.**

> [!important] The idea
> Start with steepest descent, $\mathbf d^{(0)}=-\mathbf g^{(0)}$. Then take each new direction to be the current negative gradient **corrected by the previous direction**:
> $$\boxed{\mathbf d^{(k+1)}=-\mathbf g^{(k+1)}+\beta_k\mathbf d^{(k)}}$$
> with $\beta_k$ chosen to force $Q$-conjugacy with $\mathbf d^{(k)}$:
> $$\beta_k=\frac{\mathbf g^{(k+1)\mathsf T}Q\,\mathbf d^{(k)}}{\mathbf d^{(k)\mathsf T}Q\,\mathbf d^{(k)}}$$

> [!important] Proposition 10.1 — the miracle
> **These directions are $Q$-conjugate to *all* previous ones, not just to $\mathbf d^{(k)}$.**
>
> **Why.** The induction uses two facts. First, Lemma 10.2 gives $\mathbf g^{(k+1)\mathsf T}\mathbf d^{(j)}=0$ for $j\le k$; combined with $\mathbf d^{(j)}=-\mathbf g^{(j)}+\beta_{j-1}\mathbf d^{(j-1)}$ this yields **$\mathbf g^{(k+1)\mathsf T}\mathbf g^{(j)}=0$: the gradients are mutually orthogonal.** Second, $\mathbf g^{(j+1)}=\mathbf g^{(j)}+\alpha_jQ\mathbf d^{(j)}$, so for $j<k$
> $$\mathbf d^{(k+1)\mathsf T}Q\mathbf d^{(j)}=-\mathbf g^{(k+1)\mathsf T}Q\mathbf d^{(j)}=-\tfrac{1}{\alpha_j}\mathbf g^{(k+1)\mathsf T}\big(\mathbf g^{(j+1)}-\mathbf g^{(j)}\big)=0$$
> **A two-term recurrence produces $k+1$ conjugacy conditions**, because the gradient orthogonality does the bookkeeping for free. $\blacksquare$

> [!important] The algorithm
> ```
> 1.  k ← 0, choose x⁽⁰⁾
> 2.  g⁽⁰⁾ ← ∇f(x⁽⁰⁾);  if g⁽⁰⁾ = 0 stop;  d⁽⁰⁾ ← −g⁽⁰⁾
> 3.  αₖ ← − g⁽ᵏ⁾ᵀd⁽ᵏ⁾ / (d⁽ᵏ⁾ᵀQ d⁽ᵏ⁾)
> 4.  x⁽ᵏ⁺¹⁾ ← x⁽ᵏ⁾ + αₖ d⁽ᵏ⁾
> 5.  g⁽ᵏ⁺¹⁾ ← ∇f(x⁽ᵏ⁺¹⁾);  if g⁽ᵏ⁺¹⁾ = 0 stop
> 6.  βₖ ← g⁽ᵏ⁺¹⁾ᵀQ d⁽ᵏ⁾ / (d⁽ᵏ⁾ᵀQ d⁽ᵏ⁾)
> 7.  d⁽ᵏ⁺¹⁾ ← −g⁽ᵏ⁺¹⁾ + βₖ d⁽ᵏ⁾
> 8.  k ← k+1;  go to 3
> ```
> **Storage: four vectors ($\mathbf x$, $\mathbf g$, $\mathbf d$, and $Q\mathbf d$). No matrix is ever formed or factorised.**

---

### 5. Eliminating $Q$: three formulas for $\beta_k$

For a non-quadratic $f$, $Q=\nabla^2f$ changes at every point and re-evaluating it would defeat the purpose. **But $Q$ appears only in $\alpha_k$ and $\beta_k$**, and both can be removed:

- **$\alpha_k$** — replace the closed form by a **numerical line search** ([[04 - One-Dimensional Search Methods|ch. 04]]).
- **$\beta_k$** — use $Q\mathbf d^{(k)}=\dfrac{\mathbf g^{(k+1)}-\mathbf g^{(k)}}{\alpha_k}$, which holds because $\mathbf g^{(k+1)}=\mathbf g^{(k)}+\alpha_kQ\mathbf d^{(k)}$.

> [!important] The three standard formulas
> $$\textbf{Hestenes–Stiefel:}\quad \beta_k=\frac{\mathbf g^{(k+1)\mathsf T}\big[\mathbf g^{(k+1)}-\mathbf g^{(k)}\big]}{\mathbf d^{(k)\mathsf T}\big[\mathbf g^{(k+1)}-\mathbf g^{(k)}\big]}$$
> $$\textbf{Polak–Ribière:}\quad \beta_k=\frac{\mathbf g^{(k+1)\mathsf T}\big[\mathbf g^{(k+1)}-\mathbf g^{(k)}\big]}{\mathbf g^{(k)\mathsf T}\mathbf g^{(k)}}$$
> $$\textbf{Fletcher–Reeves:}\quad \beta_k=\frac{\mathbf g^{(k+1)\mathsf T}\mathbf g^{(k+1)}}{\mathbf g^{(k)\mathsf T}\mathbf g^{(k)}}$$
>
> **Each follows from the previous one using Lemma 10.2** — Hestenes–Stiefel's denominator simplifies via $\mathbf d^{(k)\mathsf T}\mathbf g^{(k+1)}=0$ and $\mathbf d^{(k)\mathsf T}\mathbf g^{(k)}=-\mathbf g^{(k)\mathsf T}\mathbf g^{(k)}$; Polak–Ribière's numerator simplifies via $\mathbf g^{(k+1)\mathsf T}\mathbf g^{(k)}=0$.

> [!warning] Identical on quadratics, different everywhere else
> **On a quadratic with exact line searches all three give the same $\beta_k$.** On a general $f$ they do not, and the differences matter:
>
> | Formula | Character |
> |---|---|
> | **Fletcher–Reeves** | globally convergent (Powell); can stall with tiny steps |
> | **Polak–Ribière** | usually faster in practice; **can fail to converge** — there are $f$ for which $\lVert\mathbf g^{(k)}\rVert$ stays bounded away from 0 |
> | **Hestenes–Stiefel** | **recommended when the line search is inaccurate** |
> | **Powell's PR$^+$**: $\beta_k=\max\{0,\ \beta_k^{\mathrm{PR}}\}$ | the standard compromise — PR's speed, FR's guarantee |

**Two further practical modifications for non-quadratic problems:**
1. **Restart**: reset $\mathbf d\leftarrow-\mathbf g$ every $n$ or $n+1$ iterations, because $Q$-conjugacy degrades as $Q$ changes.
2. **A careful line search**: *"the accuracy of the line search is a critical factor in the performance of the conjugate gradient algorithm"* — unlike BFGS ([[06 - Newton and Quasi-Newton Methods|ch. 06]] §7), CG is **not** robust to sloppy line searches. **This is the main practical disadvantage of CG relative to L-BFGS.**

---

### 6. Rate, cost, and where CG actually lives

> [!important] The convergence rate: $\sqrt\kappa$, not $\kappa$
> For the quadratic case, CG satisfies
> $$\frac{\lVert\mathbf x_m-\mathbf x^*\rVert_Q}{\lVert\mathbf x_0-\mathbf x^*\rVert_Q}\ \le\ 2\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{m}$$
> **against steepest descent's $\left(\frac{\kappa-1}{\kappa+1}\right)^{m}$.** *(This bound is Luenberger & Ye ch. 9 / standard Krylov theory; Chong & Żak state exact termination but not this rate.)*
>
> | $\kappa$ | Steepest descent | **Conjugate gradient** | Speed-up |
> |---|---|---|---|
> | $10$ | $35$ | $23$ | $1.5\times$ |
> | $10^2$ | $346$ | $73$ | $4.7\times$ |
> | $10^3$ | $3\,454$ | $230$ | $15\times$ |
> | $10^4$ | $34\,539$ | $726$ | $48\times$ |
> | $10^6$ | $3\,453\,878$ | $\mathbf{7\,255}$ | $\mathbf{476\times}$ |
>
> *(iterations for six digits; verified)*
>
> **Replacing $\kappa$ by $\sqrt\kappa$ is the single largest algorithmic improvement in this half of the subject**, and it costs nothing per iteration.

> [!important] CG is really a linear-system solver, and that is its main career
> **$\min\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ and $Q\mathbf x=\mathbf b$ are the same problem** for $Q\succ0$. So CG is an iterative solver for symmetric positive definite systems, and:
>
> - **It touches $Q$ only through the product $Q\mathbf v$.** $Q$ need never be stored — only a routine that applies it. **For a sparse $Q$ with $O(n)$ non-zeros, each iteration is $O(n)$.**
> - **Direct methods (Cholesky) cost $O(n^3)$ and destroy sparsity by fill-in.** CG does neither.
> - **This is why every large PDE, finite-element and graph-Laplacian system in scientific computing is solved by CG**, and why Krylov-subspace iteration was named one of the ten most influential algorithms of the twentieth century.
>
> **Preconditioned CG** applies CG to $M^{-1}Q$ for a cheap $M\approx Q$, replacing $\kappa(Q)$ by $\kappa(M^{-1}Q)$ — **exactly [[05 - Gradient Methods|ch. 05]] §7's preconditioning, now on top of the $\sqrt\kappa$ rate.** With a good $M$ the iteration count becomes nearly independent of $n$.

| Method | Storage | Work/iteration | Iterations (quadratic) |
|---|---|---|---|
| Steepest descent | $O(n)$ | $O(n)$ | $O(\kappa)$ |
| **Conjugate gradient** | $O(n)$ | $O(n)$ | $O(\sqrt\kappa)$, **exact in $n$** |
| BFGS | $O(n^2)$ | $O(n^2)$ | exact in $n$ |
| Newton | $O(n^2)$ | $O(n^3)$ | **1** |

> [!note] Where CG sits today
> **In scientific computing: everywhere** — it is the default sparse SPD solver.
>
> **In machine learning: narrower than it deserves.** It is used inside **Hessian-free / truncated-Newton** methods, where the Newton system $\nabla^2f\,\mathbf d=-\mathbf g$ is solved approximately by a few CG iterations using only Hessian-vector products (each costing about two gradient evaluations) — **giving Newton-like directions at $O(n)$ memory.** It is also the standard inner solver for **natural gradient** and **Gauss–Newton** methods.
>
> **It is not used for stochastic training, for the same reason as L-BFGS**: conjugacy is destroyed by gradient noise, and CG needs an accurate line search that mini-batches cannot supply.

---

## ✏️ Exercises

> [!question] Exercise 1 — building conjugate directions *(easy)*
> Let $Q=\begin{pmatrix}4&1&0\\1&3&1\\0&1&2\end{pmatrix}$.
> **(a)** Verify $Q\succ0$.
> **(b)** Apply $Q$-Gram–Schmidt to the standard basis $\mathbf e_1,\mathbf e_2,\mathbf e_3$:
> $$\mathbf d^{(0)}=\mathbf p^{(0)},\qquad \mathbf d^{(k+1)}=\mathbf p^{(k+1)}-\sum_{i=0}^{k}\frac{\mathbf p^{(k+1)\mathsf T}Q\mathbf d^{(i)}}{\mathbf d^{(i)\mathsf T}Q\mathbf d^{(i)}}\mathbf d^{(i)}$$
> **(c)** Verify all three conjugacy conditions.
> **(d)** Why does this construction always work, and why is it nevertheless not used?

> [!example]- Solution
> **(a)** Leading principal minors: $4$, $\det\begin{psmallmatrix}4&1\\1&3\end{psmallmatrix}=11$, $\det Q=18$. **All positive, so $Q\succ0$** by Sylvester's criterion.
>
> **(b)** $\mathbf d^{(0)}=\mathbf e_1=(1,0,0)^{\mathsf T}$, with $\mathbf d^{(0)\mathsf T}Q\mathbf d^{(0)}=4$.
>
> $$\mathbf e_2^{\mathsf T}Q\mathbf d^{(0)}=1\ \Longrightarrow\ \mathbf d^{(1)}=\mathbf e_2-\tfrac14\mathbf e_1=\boxed{\left(-\tfrac14,\ 1,\ 0\right)^{\mathsf T}}$$
> Then $\mathbf d^{(1)\mathsf T}Q\mathbf d^{(1)}=\tfrac{11}{4}$, and $\mathbf e_3^{\mathsf T}Q\mathbf d^{(0)}=0$, $\mathbf e_3^{\mathsf T}Q\mathbf d^{(1)}=1$, so
> $$\mathbf d^{(2)}=\mathbf e_3-0\cdot\mathbf d^{(0)}-\tfrac{1}{11/4}\mathbf d^{(1)}=\boxed{\left(\tfrac1{11},\ -\tfrac4{11},\ 1\right)^{\mathsf T}}$$
>
> **(c)** *(Verified exactly, in rational arithmetic.)*
> $$\mathbf d^{(0)\mathsf T}Q\mathbf d^{(1)}=0,\qquad \mathbf d^{(0)\mathsf T}Q\mathbf d^{(2)}=0,\qquad \mathbf d^{(1)\mathsf T}Q\mathbf d^{(2)}=0\ \checkmark$$
>
> **(d) It always works because $\langle\mathbf u,\mathbf v\rangle_Q=\mathbf u^{\mathsf T}Q\mathbf v$ is a genuine inner product when $Q\succ0$**, so ordinary Gram–Schmidt ([[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]) applies verbatim with the dot product replaced. **Conjugate directions are just a $Q$-orthogonal basis.**
>
> **It is not used because it costs everything the method was meant to save:**
> - it needs **$Q$ itself**, not just products $Q\mathbf v$;
> - it needs **all $n$ directions stored**, $O(n^2)$ memory;
> - it costs $O(n^3)$ to build them.
>
> **At that price one may as well do a Cholesky factorisation and solve directly.** **§4's conjugate gradient generates the same directions with a two-term recurrence and $O(n)$ storage — that is the actual contribution of the chapter.**

---

> [!question] Exercise 2 — the conjugate direction algorithm *(easy–medium)*
> Minimise $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}\begin{pmatrix}4&2\\2&2\end{pmatrix}\mathbf x-\mathbf x^{\mathsf T}\begin{pmatrix}-1\\1\end{pmatrix}$ from $\mathbf x^{(0)}=\mathbf 0$ using $\mathbf d^{(0)}=(1,0)^{\mathsf T}$, $\mathbf d^{(1)}=(-\tfrac38,\tfrac34)^{\mathsf T}$.
> **(a)** Check the two directions are $Q$-conjugate.
> **(b)** Carry out both steps.
> **(c)** Verify $\mathbf x^{(2)}=\mathbf x^*$ and check Lemma 10.2 at $k=1$.

> [!example]- Solution
> **(a)** $Q\mathbf d^{(1)}=\begin{pmatrix}4&2\\2&2\end{pmatrix}\begin{pmatrix}-3/8\\3/4\end{pmatrix}=\begin{pmatrix}-\tfrac32+\tfrac32\\-\tfrac34+\tfrac32\end{pmatrix}=\begin{pmatrix}0\\ \tfrac34\end{pmatrix}$, so
> $$\mathbf d^{(0)\mathsf T}Q\mathbf d^{(1)}=(1,0)\cdot(0,\tfrac34)^{\mathsf T}=0\ \checkmark$$
>
> **(b) Step 0.** $\mathbf g^{(0)}=Q\mathbf 0-\mathbf b=(1,-1)^{\mathsf T}$, $\mathbf d^{(0)\mathsf T}Q\mathbf d^{(0)}=4$:
> $$\alpha_0=-\frac{(1,-1)\cdot(1,0)}{4}=-\frac14,\qquad \mathbf x^{(1)}=\left(-\tfrac14,\ 0\right)^{\mathsf T}$$
> **Note $\alpha_0<0$ — perfectly legal.** The $\mathbf d^{(i)}$ are prescribed directions, not necessarily descent directions, so the step may go backwards along them.
>
> **Step 1.** $\mathbf g^{(1)}=Q\mathbf x^{(1)}-\mathbf b=(-1,-\tfrac12)-(-1,1)=(0,-\tfrac32)^{\mathsf T}$, and $\mathbf d^{(1)\mathsf T}Q\mathbf d^{(1)}=(-\tfrac38,\tfrac34)\cdot(0,\tfrac34)=\tfrac9{16}$:
> $$\alpha_1=-\frac{(0,-\tfrac32)\cdot(-\tfrac38,\tfrac34)}{9/16}=-\frac{-9/8}{9/16}=2,\qquad \mathbf x^{(2)}=\left(-\tfrac14,0\right)+2\left(-\tfrac38,\tfrac34\right)=\boxed{(-1,\ \tfrac32)^{\mathsf T}}$$
>
> **(c)** $\det Q=4$, so $Q^{-1}=\tfrac14\begin{psmallmatrix}2&-2\\-2&4\end{psmallmatrix}=\begin{psmallmatrix}1/2&-1/2\\-1/2&1\end{psmallmatrix}$ and
> $$\mathbf x^*=Q^{-1}\mathbf b=\left(-\tfrac12-\tfrac12,\ \tfrac12+1\right)^{\mathsf T}=(-1,\ \tfrac32)^{\mathsf T}=\mathbf x^{(2)}\ \checkmark$$
>
> **Lemma 10.2 at $k=1$:** $\mathbf g^{(2)}=Q\mathbf x^*-\mathbf b=\mathbf 0$, so $\mathbf g^{(2)\mathsf T}\mathbf d^{(0)}=\mathbf g^{(2)\mathsf T}\mathbf d^{(1)}=0$ trivially. **More informative is $k=0$:** $\mathbf g^{(1)\mathsf T}\mathbf d^{(0)}=(0,-\tfrac32)\cdot(1,0)=0\ \checkmark$ — the new gradient is orthogonal to the direction just used, which is the exact-line-search condition.
>
> **Two observations.** The method reached $\mathbf x^*$ in exactly $n=2$ steps ✔, and it did so **with prescribed directions and no gradient information beyond the line searches** — the conjugacy did all the work.

---

> [!question] Exercise 3 — conjugate gradient in three variables *(medium)*
> Minimise
> $$f(x_1,x_2,x_3)=\tfrac32x_1^2+2x_2^2+\tfrac32x_3^2+x_1x_3+2x_2x_3-3x_1-x_3$$
> by conjugate gradient from $\mathbf x^{(0)}=\mathbf 0$.
> **(a)** Write $f$ as $\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf x^{\mathsf T}\mathbf b$.
> **(b)** Run all three iterations.
> **(c)** Verify termination and that the gradients are mutually orthogonal.

> [!example]- Solution
> **(a)** Matching coefficients — $\tfrac12q_{ii}$ for $x_i^2$ and $q_{ij}$ for $x_ix_j$ ($i\ne j$):
> $$Q=\begin{pmatrix}3&0&1\\0&4&2\\1&2&3\end{pmatrix},\qquad \mathbf b=\begin{pmatrix}3\\0\\1\end{pmatrix}$$
> *(Check: leading minors $3$, $12$, $20$ — so $Q\succ0$.)* Then $\nabla f=Q\mathbf x-\mathbf b=(3x_1+x_3-3,\ 4x_2+2x_3,\ x_1+2x_2+3x_3-1)^{\mathsf T}$.
>
> **(b)** *(All values verified.)*
>
> | $k$ | $\mathbf g^{(k)}$ | $\mathbf d^{(k)}$ | $\alpha_k$ | $\mathbf x^{(k+1)}$ |
> |---|---|---|---|---|
> | 0 | $(-3,\ 0,\ -1)$ | $(3,\ 0,\ 1)$ | $0.2778$ | $(0.8333,\ 0,\ 0.2778)$ |
> | 1 | $(-0.2222,\ 0.5556,\ 0.6667)$ | $(0.4630,\ -0.5556,\ -0.5864)$ | $0.2187$ | $(0.9346,\ -0.1215,\ 0.1495)$ |
> | 2 | $(-0.04673,\ -0.1869,\ 0.1402)$ | $(0.07948,\ 0.1476,\ -0.1817)$ | $0.8231$ | $(1.000,\ 0.000,\ 0.000)$ |
>
> *(Step 0: $\mathbf d^{(0)}=-\mathbf g^{(0)}=\mathbf b$; $Q\mathbf d^{(0)}=(10,2,6)$; $\mathbf d^{(0)\mathsf T}Q\mathbf d^{(0)}=36$; $\alpha_0=10/36=0.2778$.)*
>
> **(c)** $\mathbf g^{(3)}=Q(1,0,0)^{\mathsf T}-\mathbf b=(3,0,1)-(3,0,1)=\mathbf 0$ ✔ — **exact termination in $n=3$ steps**, and $\mathbf x^*=(1,0,0)^{\mathsf T}$.
>
> **Gradient orthogonality:**
> $$\mathbf g^{(0)\mathsf T}\mathbf g^{(1)}=(-3)(-0.2222)+0+(-1)(0.6667)=0.6667-0.6667=0\ \checkmark$$
> and similarly $\mathbf g^{(0)\mathsf T}\mathbf g^{(2)}=\mathbf g^{(1)\mathsf T}\mathbf g^{(2)}=0$.
>
> **This orthogonality is not imposed — it is a consequence** (Proposition 10.1), and it is what lets the two-term recurrence enforce $k+1$ conjugacy conditions at once. **It is also what makes the Fletcher–Reeves simplification $\beta_k=\lVert\mathbf g^{(k+1)}\rVert^2/\lVert\mathbf g^{(k)}\rVert^2$ valid.**
>
> *(Compare the effort: [[06 - Newton and Quasi-Newton Methods|Newton]] would solve this in one step but must factorise $Q$; **CG took three steps and never touched anything but the products $Q\mathbf d$.** At $n=3$ Newton wins; at $n=10^6$ with sparse $Q$, CG is the only option.)*

---

> [!question] Exercise 4 — why conjugacy is the right condition *(hard)*
> **(a)** Show that for steepest descent with exact line search, minimising along $\mathbf d^{(k)}$ generally **destroys** the optimality achieved along $\mathbf d^{(k-1)}$. Illustrate with $f=\tfrac12(x_1^2+10x_2^2)$ from $(1,1)$.
> **(b)** Show that for conjugate directions it does not: prove that if $\mathbf x^{(k)}$ minimises $f$ over $V_{k-1}$ and $\mathbf d^{(k)}$ is $Q$-conjugate to $\mathbf d^{(0)},\dots,\mathbf d^{(k-1)}$, then $\mathbf x^{(k+1)}$ minimises $f$ over $V_k$.
> **(c)** Deduce that a quadratic in $n$ variables is solved in $\le n$ steps, and explain in one sentence why steepest descent is not.

> [!example]- Solution
> **(a)** From $\mathbf x_0=(1,1)$ with $Q=\operatorname{diag}(1,10)$ ([[05 - Gradient Methods|ch. 05]] Exercise 1):
> $$\mathbf x_0=(1,1)\ \to\ \mathbf x_1=(0.8991,\ -0.008991)\ \to\ \mathbf x_2=(0.073563,\ 0.073563)$$
> **After step 1, $x_2$ was very nearly optimal** — the $x_2$-component fell from $1$ to $-0.009$, a factor of 111. **After step 2, $x_2$ is back to $0.0736$** — eight times worse than it was.
>
> **The second minimisation undid the first.** By exact line search $\mathbf g^{(2)\mathsf T}\mathbf d^{(1)}=0$, but there is **no reason for $\mathbf g^{(2)\mathsf T}\mathbf d^{(0)}=0$**, and generally it is not. **That is the zig-zag, expressed algebraically.**
>
> **(b) Proof.** Let $V_k=\mathbf x^{(0)}+\operatorname{span}\{\mathbf d^{(0)},\dots,\mathbf d^{(k)}\}$ and $D^{(k)}=[\mathbf d^{(0)}|\cdots|\mathbf d^{(k)}]$. **A point of $V_k$ minimises the convex quadratic $f$ over $V_k$ iff its gradient is orthogonal to the whole subspace**, i.e. iff $\mathbf g^{\mathsf T}D^{(k)}=\mathbf 0^{\mathsf T}$.
>
> By hypothesis $\mathbf g^{(k)\mathsf T}\mathbf d^{(i)}=0$ for $i\le k-1$. Now
> $$\mathbf g^{(k+1)}=Q\mathbf x^{(k+1)}-\mathbf b=Q\big(\mathbf x^{(k)}+\alpha_k\mathbf d^{(k)}\big)-\mathbf b=\mathbf g^{(k)}+\alpha_kQ\mathbf d^{(k)}$$
> so for $i\le k-1$,
> $$\mathbf g^{(k+1)\mathsf T}\mathbf d^{(i)}=\underbrace{\mathbf g^{(k)\mathsf T}\mathbf d^{(i)}}_{=0\ \text{(hypothesis)}}+\alpha_k\underbrace{\mathbf d^{(k)\mathsf T}Q\mathbf d^{(i)}}_{=0\ \textbf{(conjugacy)}}=0$$
> and for $i=k$, $\mathbf g^{(k+1)\mathsf T}\mathbf d^{(k)}=0$ is exactly the exact-line-search condition defining $\alpha_k$. **Hence $\mathbf g^{(k+1)\mathsf T}D^{(k)}=\mathbf 0^{\mathsf T}$ and $\mathbf x^{(k+1)}$ minimises $f$ over $V_k$.** $\blacksquare$
>
> **Look at where conjugacy entered: the single underbraced term.** Without it that term is non-zero, the old orthogonality is destroyed, and the induction collapses. **$Q$-conjugacy is precisely — neither more nor less than — the condition that makes the new step's second-order effect invisible to the old directions.**
>
> **(c)** By induction $\mathbf x^{(n)}$ minimises $f$ over $V_{n-1}$. The $n$ conjugate directions are linearly independent (§1's Lemma), so $\operatorname{span}\{\mathbf d^{(0)},\dots,\mathbf d^{(n-1)}\}=\mathbb R^n$ and $V_{n-1}=\mathbb R^n$. **Therefore $\mathbf x^{(n)}$ is the global minimiser.** $\blacksquare$
>
> **And steepest descent is not**, in one sentence: **its directions $-\mathbf g^{(k)}$ are orthogonal in the ordinary inner product rather than the $Q$ one, so the underbraced term $\mathbf d^{(k)\mathsf T}Q\mathbf d^{(i)}$ is not zero, each step partially undoes the last, and the process is infinite.**
>
> *(Note the pleasing consequence: steepest descent's directions **are** conjugate when $Q=I$, i.e. $\kappa=1$ — which is exactly when [[05 - Gradient Methods|ch. 05]] said it converges in one step.)*

---

> [!question] Exercise 5 — CG as a linear solver, and the $\sqrt\kappa$ payoff *(medium–hard)*
> **(a)** Explain why minimising $\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ and solving $Q\mathbf x=\mathbf b$ are the same problem, and what this requires of $Q$.
> **(b)** CG's bound is $2\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^m$. Tabulate the iterations for six digits against steepest descent for $\kappa=10,10^2,\dots,10^6$.
> **(c)** A finite-element problem gives a sparse SPD $Q$ with $n=10^6$ and $10^7$ non-zeros, $\kappa=10^4$. Compare CG with Cholesky.
> **(d)** What is a preconditioner here, and what does it change?
> **(e)** Why is CG not used to train neural networks, given all of the above?

> [!example]- Solution
> **(a)** $\nabla\left(\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x\right)=Q\mathbf x-\mathbf b$, so **stationary points of the quadratic are exactly solutions of the linear system.** For this to be an equivalence of *minimisation* and *solving* we need $Q\succ0$: then the quadratic is strictly convex, the stationary point is the unique global minimiser ([[02 - Convex Sets and Convex Functions|ch. 02]] §6), and $Q$ is invertible.
>
> **Symmetry and positive definiteness are both essential** — CG applied to a non-symmetric or indefinite system breaks. *(The generalisations are MINRES for symmetric indefinite and GMRES for non-symmetric.)*
>
> **(b)** Requiring $2r^m\le10^{-6}$ with $r=\frac{\sqrt\kappa-1}{\sqrt\kappa+1}$:
>
> | $\kappa$ | Steepest descent | **CG** | Speed-up |
> |---|---|---|---|
> | $10$ | $35$ | $23$ | $1.5\times$ |
> | $10^2$ | $346$ | $73$ | $4.7\times$ |
> | $10^3$ | $3\,454$ | $230$ | $15\times$ |
> | $10^4$ | $34\,539$ | $726$ | $48\times$ |
> | $10^6$ | $3\,453\,878$ | $7\,255$ | $476\times$ |
>
> **The speed-up itself grows like $\sqrt\kappa$**, so the worse the problem, the more CG wins. *(At $\kappa=10$ it is barely worth the extra vector; at $\kappa=10^6$ it is the difference between minutes and a week.)*
>
> **(c)**
>
> | | **CG** | **Cholesky** |
> |---|---|---|
> | Iterations | $\approx726$ (from (b)) | 1 factorisation |
> | Work | $726\times O(\text{nnz})=726\times10^7\approx7\times10^9$ flops | $\tfrac13n^3=3.3\times10^{17}$ flops |
> | Storage | 4 vectors $=32$ MB, plus $Q$ ($\approx120$ MB sparse) | **fill-in**: the factor $L$ of a sparse $Q$ is typically far denser, often $O(n^{1.5})$–$O(n^2)$ |
> | Time at $10^{11}$ flop/s | **$0.07$ s** | $\approx38$ days |
>
> **CG wins by nine orders of magnitude**, and the memory comparison is worse still: Cholesky's fill-in can exhaust RAM long before the flops become the binding constraint. **This is why iterative Krylov methods, not direct factorisation, are the backbone of large-scale scientific computing.**
>
> **Note the two properties doing the work:** $O(n)$ storage *and* access to $Q$ only through $Q\mathbf v$. **A matrix you can multiply by but not store is exactly the situation CG was designed for** — and it is very common (finite-element operators, graph Laplacians, and **Hessian-vector products computed by autodiff without ever forming the Hessian**).
>
> **(d)** A **preconditioner** is a cheap $M\approx Q$ with $M^{-1}\mathbf v$ easy to compute; CG is then applied to the system preconditioned by $M^{-1}$, and the rate depends on $\kappa(M^{-1}Q)$ rather than $\kappa(Q)$.
>
> Common choices: **Jacobi** ($M=\operatorname{diag}Q$ — [[05 - Gradient Methods|ch. 05]] §7's diagonal preconditioner, again), **incomplete Cholesky**, and multigrid. **With a good $M$, $\kappa(M^{-1}Q)$ becomes $O(1)$ and the iteration count stops growing with $n$ altogether** — which is what makes million-variable PDE solves routine.
>
> **Note the layering:** ch. 05's preconditioning improves $\kappa$; this chapter's conjugacy improves the *exponent* on $\kappa$ from $1$ to $\tfrac12$. **They compose, and preconditioned CG uses both.**
>
> **(e) Because everything above assumes a fixed quadratic, and neural network training supplies none of it.**
>
> | CG requires | Training provides |
> |---|---|
> | $Q$ symmetric **positive definite** | a non-convex loss whose Hessian is indefinite and rank-deficient |
> | A **fixed** quadratic (or $Q$ changing slowly) | a Hessian that changes at every point |
> | An **accurate line search** | mini-batches, so $\phi_k$ differs at every evaluation |
> | **Exact gradients** — conjugacy is destroyed by noise | stochastic gradients |
>
> **The line-search requirement is the sharpest of these.** Chong & Żak note that CG's performance is *critically* dependent on line-search accuracy — unlike BFGS. **A method that needs accurate line searches cannot be used with resampled mini-batches**, and no amount of restarting repairs it.
>
> **But CG has not disappeared from machine learning; it moved inside.** In **Hessian-free (truncated Newton)** optimization, the Newton system $\nabla^2f\,\mathbf d=-\mathbf g$ is solved to low accuracy by a handful of CG iterations, each needing only a Hessian-vector product ($\approx2$ gradient evaluations, computed by autodiff without forming $\nabla^2f$). **This gives a Newton-quality direction at $O(n)$ memory** — the same trick as (c), applied to a Hessian instead of a stiffness matrix. It is also the standard inner solver for **natural gradient** and **Gauss–Newton** methods.

---

## 📝 Summary

- **$Q$-conjugacy** is $\mathbf d^{(i)\mathsf T}Q\mathbf d^{(j)}=0$ — orthogonality in the inner product $\langle\cdot,\cdot\rangle_Q$. **Geometrically: the directions that become perpendicular once $Q^{1/2}$ rounds the ellipsoids into spheres.** Conjugate non-zero directions are linearly independent, so at most $n$ exist.
- **The conjugate direction algorithm minimises a quadratic exactly in $\le n$ steps**, because conjugacy is precisely the condition under which minimising along a new direction **does not undo** the minimisations already achieved.
- **Lemma 10.2:** $\mathbf g^{(k+1)}$ is orthogonal to *every* previous direction, not just the last — the one-word improvement over steepest descent that makes everything work.
- **Expanding subspace theorem:** each iterate minimises $f$ over the whole subspace spanned by the directions used so far, and that subspace grows by one dimension per step.
- **Conjugate gradient generates the directions on the fly**: $\mathbf d^{(k+1)}=-\mathbf g^{(k+1)}+\beta_k\mathbf d^{(k)}$ with $\beta_k=\frac{\mathbf g^{(k+1)\mathsf T}Q\mathbf d^{(k)}}{\mathbf d^{(k)\mathsf T}Q\mathbf d^{(k)}}$. **A two-term recurrence enforces all $k+1$ conjugacy conditions**, because the gradients come out mutually orthogonal for free.
- **$Q$ can be eliminated entirely.** $\alpha_k$ by line search; $\beta_k$ by **Fletcher–Reeves** $\frac{\lVert\mathbf g^{(k+1)}\rVert^2}{\lVert\mathbf g^{(k)}\rVert^2}$, **Polak–Ribière**, or **Hestenes–Stiefel**. **Identical on quadratics, materially different on general $f$** — PR is faster but can fail; FR is globally convergent; PR$^+$ is the standard compromise.
- **Non-quadratic practice needs restarts** (every $n$ steps) **and an accurate line search** — CG is *not* robust to sloppy line searches, unlike BFGS.
- **Rate: $O(\sqrt\kappa)$ instead of $O(\kappa)$.** At $\kappa=10^6$, 7,255 iterations instead of 3.5 million — a $476\times$ speed-up at no extra cost per step.
- **CG's main career is as a linear solver.** It needs $O(n)$ storage and touches $Q$ only through $Q\mathbf v$, so it solves large sparse SPD systems that Cholesky cannot even store. **Preconditioned CG composes ch. 05's $\kappa$-reduction with this chapter's exponent-reduction.**

---

## ⚠️ Important Notes

> [!warning] The five errors
> 1. **Confusing conjugate with orthogonal.** $\mathbf d^{(i)\mathsf T}\mathbf d^{(j)}=0$ is neither necessary nor sufficient for $\mathbf d^{(i)\mathsf T}Q\mathbf d^{(j)}=0$.
> 2. **Expecting $\alpha_k>0$.** With prescribed directions, $\alpha_k$ can be negative (Exercise 2). Only in CG, where $\mathbf d^{(0)}=-\mathbf g^{(0)}$, are the directions descent directions.
> 3. **Using CG on a non-symmetric or indefinite system.** It has no theory there. Use MINRES or GMRES.
> 4. **Forgetting to restart on non-quadratic problems.** Conjugacy degrades as $\nabla^2f$ changes; without a restart every $\approx n$ steps the directions become meaningless.
> 5. **Using a sloppy line search with CG.** Legitimate for BFGS, fatal here.

> [!tip] Gradient descent, CG, BFGS, Newton — one table
> | | Storage | Work/iter | Iterations | Needs |
> |---|---|---|---|---|
> | Steepest descent | $O(n)$ | $O(n)$ | $O(\kappa)$ | $\nabla f$ |
> | **CG** | $O(n)$ | $O(n)$ | $O(\sqrt\kappa)$; exact in $n$ | $\nabla f$ + **accurate line search** |
> | BFGS | $O(n^2)$ | $O(n^2)$ | exact in $n$; superlinear | $\nabla f$ + Wolfe |
> | L-BFGS | $O(mn)$ | $O(mn)$ | superlinear in practice | $\nabla f$ + Wolfe |
> | Newton | $O(n^2)$ | $O(n^3)$ | $1$ (quadratic $f$) | $\nabla^2f$ |
>
> **Read the middle two columns: CG is the only method with steepest descent's cost and a materially better rate.**

> [!note] Where this chapter connects
> - **[[05 - Gradient Methods|Ch. 05]]** — this chapter's whole purpose is to repair the zig-zag diagnosed there, and Exercise 4(a) shows the two phenomena are the same algebraic fact.
> - **[[06 - Newton and Quasi-Newton Methods|Ch. 06]]** — **quasi-Newton methods *are* conjugate direction methods** (Theorem 11.1 there), which is why BFGS is also exact on quadratics in $n$ steps. **CG is the $O(n)$-memory member of the same family.**
> - **[[08 - Least Squares and Linear Equations|Ch. 08]]** — CG solves the normal equations without forming $X^{\mathsf T}X$; **LSQR is the numerically stable variant that works on $X$ directly and avoids squaring $\kappa$.**
> - **[[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]** — §1 is Gram–Schmidt in the $Q$ inner product, and Exercise 1 is that construction verbatim.
> - **[[Machine Learning/contents/00-Index|Machine Learning]]** — Hessian-free / truncated-Newton training, natural gradient, and Gauss–Newton all use CG as their inner solver.

---

> [!warning] Gaps in the source material
> **Source.** Chong & Żak ch. 10 throughout; Luenberger & Ye ch. 9 used for the convergence rate, which Chong & Żak do not state.
>
> **OCR damage:**
> - **The superscript direction index is destroyed everywhere.** `d(0)`, `d^`, `cr°\`, `S1'`, `<r2'`, `cl·2'`, `er \`, `Sk)`, `dS1'`, `<rn_1'` are all $\mathbf d^{(i)}$ for various $i$ — **and it is frequently impossible to tell *which* $i$ from the extraction alone.** Every displayed formula in §§2–5 above was reconstructed from the definitions and then verified numerically.
> - **In Example 10.2 a minus sign is lost.** The book's $\mathbf x^{(1)}$ extracts as $(\tfrac14,0)$; the correct value is $\boxed{(-\tfrac14,\ 0)}$, since $\alpha_0=-\tfrac14$ and $\mathbf d^{(0)}=(1,0)$. **The book's own subsequent values confirm the negative sign** — $\mathbf g^{(1)}=(0,-\tfrac32)$ and the final $\mathbf x^{(2)}=(-1,\tfrac32)=\mathbf x^*$ are both correct and are only reachable from $(-\tfrac14,0)$. **So this is an extraction artefact, not a book error.**
> - **`ßk`, `/?fc`, `ß^`, `fa` are all $\beta_k$**; `otk`, `α&`, `cto`, `£*o` are $\alpha_k$; `Q > 0` means $Q\succ0$; `φ` is $\ne$; `Φ '`, `<r ^` are further mangled direction symbols.
> - **The three $\beta_k$ formulas lose their fraction bars**, running numerator and denominator together on one line. **All three were re-derived from $\beta_k=\frac{\mathbf g^{(k+1)\mathsf T}Q\mathbf d^{(k)}}{\mathbf d^{(k)\mathsf T}Q\mathbf d^{(k)}}$ using Lemma 10.2**, and the derivations in §5 are those.
> - **Figure 10.1 (illustrating Lemma 10.2 — the new gradient orthogonal to the span of all previous directions) is an image and is lost.** It is the one figure in the chapter and it depicts its central lemma.
>
> **Verification performed.** Everything reproduces exactly:
> - **Example 10.1**: $Q$'s leading minors $3,\ 12,\ 20$ as printed, and all three conjugacy conditions for $\mathbf d^{(0)}=(1,0,0)$, $\mathbf d^{(1)}=(1,0,-3)$, $\mathbf d^{(2)}=(1,4,-3)$ — **exactly zero.**
> - **Example 10.2**: $\mathbf d^{(0)\mathsf T}Q\mathbf d^{(1)}=0$; $\alpha_0=-\tfrac14$; $\mathbf g^{(1)}=(0,-\tfrac32)$; $\alpha_1=2$; $\mathbf x^{(2)}=(-1,\tfrac32)=Q^{-1}\mathbf b$ ✔ *(and this is what identified the lost minus sign above)*.
> - **Example 10.3**: all three gradients, all three directions, all three step sizes $(0.2778,\ 0.2187,\ 0.8231)$ and all three iterates reproduce **to every printed decimal place**, terminating at $\mathbf x^*=(1,0,0)$ with $\mathbf g^{(3)}=\mathbf 0$ exactly.
> - **Exercise 1**: the Gram–Schmidt directions computed in exact rational arithmetic, $\mathbf d^{(1)}=(-\tfrac14,1,0)$ and $\mathbf d^{(2)}=(\tfrac1{11},-\tfrac4{11},1)$, with all conjugacy checks exactly zero, and the three-step solve landing on $Q^{-1}\mathbf b=(\tfrac29,\tfrac19,\tfrac{13}9)$.
> - **The $\sqrt\kappa$ table** in §6 and Exercise 5(b), computed directly from both bounds.
>
> **No mathematical error was found in Chong & Żak ch. 10** — it is the cleanest chapter of the book so far.
>
> **Scope and additions.**
> - **§6's convergence rate is Luenberger & Ye's, not Chong & Żak's.** C&Ż prove exact termination in $n$ steps and stop there; **for $n=10^6$ that guarantee is worthless and the $O(\sqrt\kappa)$ bound is the one that matters.** The iteration table comparing CG with steepest descent is my own computation.
> - **§6's account of CG as a *linear solver* — sparsity, $Q\mathbf v$-only access, fill-in, preconditioned CG — is largely my own addition.** Chong & Żak mention Krylov subspaces in a closing paragraph *(noting the algorithm's selection as one of the ten most influential of the twentieth century)* but never explain why. **This is CG's principal use in practice and omitting it would misrepresent the method.**
> - **The geometric reading of conjugacy in §1 ("perpendicular after $Q^{1/2}$ rounds the ellipsoids") is my own framing**, connecting back to [[05 - Gradient Methods|ch. 05]] §7's preconditioning.
> - **Exercise 4 is my own**, and its point — that conjugacy is *exactly* the condition making a new step invisible to the old directions, with the single underbraced term carrying the whole argument — is the chapter's central idea stated in a form neither book gives directly.
> - **Exercise 5(e) and the Hessian-free / truncated-Newton discussion are my own additions**, and are the answer to the question a DS reader will ask given the $476\times$ speed-up in (b).

#optimization #conjugate-directions #conjugate-gradient #krylov #expanding-subspace #fletcher-reeves #polak-ribiere #hestenes-stiefel #preconditioning
