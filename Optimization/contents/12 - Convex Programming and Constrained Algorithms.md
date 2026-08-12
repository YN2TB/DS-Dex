---
subject: Optimization
chapter: 12
tags: [ds, optimization, convex-programming, kkt, projected-gradient, penalty-methods, barrier-methods, interior-point, semidefinite-programming, duality-gap]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 22–23 (with ch. 14 and 24 summarised); Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 12–13 and §5.5"
---

# Convex Programming and Constrained Algorithms

[[11 - Constrained Optimization - Lagrange and KKT|Chapter 11]] ended with three loose ends, and this chapter closes all of them.

First, **KKT is only necessary** — it flags candidates, and chapter 11's own Example 21.5 produced a unique, regular KKT point that was not a minimizer. Second, **SOSC delivers only *strict local***, so nothing so far licenses the word "global". Third, [[10 - Duality|ch. 10]]'s beautiful zero duality gap was proved for linear programs only, and chapter 11 warned that in general a **duality gap** can open.

**One hypothesis fixes all three: convexity.** Under it, local minimizers are global, first-order conditions become *sufficient*, and the duality gap closes. That is the first half of this chapter.

The second half is the part that actually runs on a computer. Chapters 04–08 gave algorithms for unconstrained problems, and every one of them can walk straight out of the feasible set. **This chapter converts them into constrained algorithms** by three devices — project the iterate back, penalise leaving, or build a wall that cannot be crossed — and those three devices are, respectively, projected/proximal gradient, penalty methods, and interior-point methods. Between them they cover essentially all constrained optimization done in practice, including most of what a machine-learning system does when it trains under a constraint.

## 📘 Main Knowledge

### 1. Convexity makes local global

Recall from [[02 - Convex Sets and Convex Functions|ch. 02]] that a **convex programming problem** is
$$\text{minimize } f(\mathbf x)\quad\text{subject to}\quad \mathbf x\in\Omega,$$
with $f$ convex and $\Omega$ convex. Linear programs qualify; so do quadratic objectives with linear constraints.

**Theorem.** *Let $f:\Omega\to\mathbb R$ be convex on a convex $\Omega$. Then $\mathbf x^\star$ is a **global** minimizer if and only if it is a **local** minimizer.*

*Proof (⟸, by contraposition).* Suppose $\mathbf x^\star$ is not global, so $f(\mathbf y)<f(\mathbf x^\star)$ for some $\mathbf y\in\Omega$. Convexity gives, for all $\alpha\in(0,1)$,
$$f\big(\alpha\mathbf y+(1-\alpha)\mathbf x^\star\big)\le\alpha f(\mathbf y)+(1-\alpha)f(\mathbf x^\star)=\alpha\big(f(\mathbf y)-f(\mathbf x^\star)\big)+f(\mathbf x^\star)<f(\mathbf x^\star).$$
Letting $\alpha\to0$ produces points **arbitrarily close to $\mathbf x^\star$** with strictly smaller value, so $\mathbf x^\star$ is not even a local minimizer. $\blacksquare$

Two immediate companions:

- **Sublevel sets are convex.** For convex $g$, the set $\Gamma_c=\{\mathbf x\in\Omega:g(\mathbf x)\le c\}$ is convex — if $g(\mathbf x),g(\mathbf y)\le c$ then $g(\alpha\mathbf x+(1-\alpha)\mathbf y)\le\alpha g(\mathbf x)+(1-\alpha)g(\mathbf y)\le c$. (The converse fails: quasiconvex functions have convex sublevel sets without being convex.)
- **The set of global minimizers is convex** — take $c=\min f$ in the above. So a convex program's solution is a *convex set*: either a unique point, or a whole face's worth. **Never assume a convex program has a unique solution** unless $f$ is *strictly* convex ([[02 - Convex Sets and Convex Functions|ch. 02]] §6).

### 2. First-order conditions become sufficient

This is the payoff, and it is why convexity is the dividing line of the whole subject.

**Lemma.** *If $f$ is convex and $C^1$ on a convex $\Omega$, and $Df(\mathbf x^\star)(\mathbf x-\mathbf x^\star)\ge0$ for all $\mathbf x\in\Omega$, then $\mathbf x^\star$ is a global minimizer.*

*Proof.* Convexity gives the supporting-hyperplane inequality $f(\mathbf x)\ge f(\mathbf x^\star)+Df(\mathbf x^\star)(\mathbf x-\mathbf x^\star)$ ([[02 - Convex Sets and Convex Functions|ch. 02]] §4), and the hypothesis kills the last term. $\blacksquare$

**The whole difficulty of nonconvex optimization is contained in that one line.** A gradient tells you about $f$ *near* $\mathbf x^\star$; convexity promotes it into a statement about $f$ *everywhere*, because the tangent plane lies globally below the graph.

Since $\mathbf x-\mathbf x^\star$ is a feasible direction whenever $\mathbf x\in\Omega$ (by convexity of $\Omega$), the lemma restates as: **if $\mathbf d^{\mathsf T}\nabla f(\mathbf x^\star)\ge0$ for every feasible direction $\mathbf d$, then $\mathbf x^\star$ is a global minimizer.** Compare [[03 - Unconstrained Optimality Conditions|ch. 03]]'s FONC, which was *necessary* only. **Corollary:** for convex $f$ on convex $\Omega$, $\nabla f(\mathbf x^\star)=\mathbf 0$ ⟹ $\mathbf x^\star$ is a global minimizer.

Now the two theorems this chapter exists for.

> [!note] Theorem — the Lagrange condition is sufficient
> Let $f\in C^1$ be convex on $\Omega=\{\mathbf x:\mathbf h(\mathbf x)=\mathbf 0\}$ with **$\Omega$ convex** (e.g. $\mathbf h(\mathbf x)=A\mathbf x-\mathbf b$). If there exist $\mathbf x^\star\in\Omega$ and $\boldsymbol\lambda^\star$ with $Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)=\mathbf 0^{\mathsf T}$, then $\mathbf x^\star$ is a **global** minimizer.

> [!note] Theorem — the KKT conditions are sufficient
> Let $f\in C^1$ be convex on $\Omega=\{\mathbf x:\mathbf h(\mathbf x)=\mathbf 0,\ \mathbf g(\mathbf x)\le\mathbf 0\}$ with **$\Omega$ convex**. If there exist $\mathbf x^\star\in\Omega$, $\boldsymbol\lambda^\star$, $\boldsymbol\mu^\star$ with
> $$\text{(1) }\boldsymbol\mu^\star\ge\mathbf 0,\qquad\text{(2) }Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)+\boldsymbol\mu^{\star\mathsf T}D\mathbf g(\mathbf x^\star)=\mathbf 0^{\mathsf T},\qquad\text{(3) }\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0,$$
> then $\mathbf x^\star$ is a **global** minimizer of $f$ over $\Omega$.

*Proof of the second (the first is the special case $\boldsymbol\mu^\star=\mathbf 0$).* For $\mathbf x\in\Omega$, convexity gives $f(\mathbf x)\ge f(\mathbf x^\star)+Df(\mathbf x^\star)(\mathbf x-\mathbf x^\star)$; substituting (2),
$$f(\mathbf x)\ \ge\ f(\mathbf x^\star)-\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)(\mathbf x-\mathbf x^\star)-\boldsymbol\mu^{\star\mathsf T}D\mathbf g(\mathbf x^\star)(\mathbf x-\mathbf x^\star).$$
Both correction terms are handled by moving along the segment towards $\mathbf x$, which stays in $\Omega$ by convexity. For the equality part: $\mathbf h(\mathbf x^\star+\alpha(\mathbf x-\mathbf x^\star))=\mathbf 0$ for all $\alpha\in(0,1)$, so subtracting $\boldsymbol\lambda^{\star\mathsf T}\mathbf h(\mathbf x^\star)=0$, dividing by $\alpha$ and letting $\alpha\to0$ gives the directional derivative $\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)(\mathbf x-\mathbf x^\star)=0$. For the inequality part: $\mathbf g(\mathbf x^\star+\alpha(\mathbf x-\mathbf x^\star))\le\mathbf 0$, and premultiplying by $\boldsymbol\mu^{\star\mathsf T}\ge\mathbf 0^{\mathsf T}$ (condition 1) then subtracting $\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0$ (condition 3) and letting $\alpha\to0$ gives $\boldsymbol\mu^{\star\mathsf T}D\mathbf g(\mathbf x^\star)(\mathbf x-\mathbf x^\star)\le0$. Hence $f(\mathbf x)\ge f(\mathbf x^\star)$. $\blacksquare$

**Notice exactly where each KKT condition was used.** Condition 1 ($\boldsymbol\mu^\star\ge\mathbf 0$) preserved an inequality's direction; condition 3 (complementary slackness) cancelled a term. Neither is decoration. And notice what regularity is *not* needed for: **this is a sufficiency theorem, so no constraint qualification appears.** Regularity was needed in chapter 11 to prove multipliers *exist*; here they are handed to you.

> [!warning] The feasible set must be convex, and that means $\mathbf h$ **affine**, not merely convex
> Both theorems assume $\Omega$ convex. For inequalities this is easy: **if every $g_j$ is convex then $\{\mathbf g\le\mathbf 0\}$ is convex**, being an intersection of convex sublevel sets (§1). But for equalities, **$\{\mathbf h=\mathbf 0\}$ is convex essentially only when $\mathbf h$ is affine.** A convex nonlinear $h$ gives a curved surface, which is not convex: $\{x_1^2+x_2^2-1=0\}$ is a circle, and $h$ is convex. **So "convex program" means convex objective, convex inequality constraints, and *affine* equality constraints** — that is the standard definition and the reason it is stated that way.

> [!example]- Worked example — proving a strategy optimal with one KKT check (C&Ż Example 22.7)
> A bank account starts at $0$. At the start of month $k$ you deposit $x_k\ge0$; the monthly rate is $r>0$, compounded. Maximize the balance after $n$ months subject to total deposits $\le D$.
>
> Since $y_k=(1+r)(y_{k-1}+x_k)$ with $y_0=0$, unrolling gives $y_n=(1+r)^nx_1+(1+r)^{n-1}x_2+\cdots+(1+r)x_n$. So with $\mathbf c=\big((1+r)^n,\dots,(1+r)\big)$ and $\mathbf e=(1,\dots,1)$ the problem is
> $$\text{maximize } \mathbf c^{\mathsf T}\mathbf x\quad\text{subject to}\quad \mathbf e^{\mathsf T}\mathbf x\le D,\ \ \mathbf x\ge\mathbf 0$$
> — **a linear program, hence a convex program.** Intuitively you should deposit everything in month 1 so it compounds longest. To *prove* it, exhibit KKT multipliers at $\mathbf x^\star=(D,0,\dots,0)$:
> $$\mu^{(1)}=(1+r)^n,\qquad \boldsymbol\mu^{(2)}=(1+r)^n\mathbf e-\mathbf c\ \ge\ \mathbf 0,$$
> the inequality holding because $(1+r)^n\ge(1+r)^k$ for every $k\le n$. Complementary slackness: $\mu^{(1)}(\mathbf e^{\mathsf T}\mathbf x^\star-D)=0$ ✓ and $\boldsymbol\mu^{(2)\mathsf T}\mathbf x^\star=\big((1+r)^n-(1+r)^n\big)D=0$ ✓ — the first component of $\boldsymbol\mu^{(2)}$ vanishes exactly, which is what lets $x_1^\star>0$.
>
> Verified with $r=0.05$, $n=4$, $D=1000$: `linprog` returns $\mathbf x^\star=(1000,0,0,0)$ with value $1215.50625=(1.05)^4\cdot1000$ ✓, and $\boldsymbol\mu^{(2)}=(0,\ 0.057881,\ 0.113006,\ 0.165506)\ge\mathbf 0$ ✓ with $\boldsymbol\mu^{(2)\mathsf T}\mathbf x^\star=0$ ✓.
>
> **This is the pattern to internalise.** Guess the answer, verify KKT, invoke convexity, done — a *proof of global optimality* from arithmetic, with no algorithm run and no search performed. It is the same certificate idea as [[10 - Duality|ch. 10]] §4, now available for nonlinear problems.

### 3. When the duality gap closes

[[11 - Constrained Optimization - Lagrange and KKT|Chapter 11]] §12 defined the **dual function** $q(\boldsymbol\lambda,\boldsymbol\mu)=\inf_{\mathbf x\in\Omega}l(\mathbf x,\boldsymbol\lambda,\boldsymbol\mu)$ and noted that **weak duality $q\le f^\star$ always holds**, while strong duality can fail. Here is what rescues it.

Luenberger & Ye's route is through the **primal function**
$$\omega(\mathbf y)=\inf\{f(\mathbf x):\mathbf h(\mathbf x)=\mathbf y,\ \mathbf x\in\Omega\},$$
the optimal value as a function of the right-hand side, so that $\omega(\mathbf 0)=f^\star$. **Proposition: if $\Omega$ is convex, $f$ convex and $\mathbf h$ affine, then $\omega$ is convex.** The proof is three lines of chaining infima:
$$\omega(\alpha\mathbf y_1+(1-\alpha)\mathbf y_2)\le\inf\{f(\mathbf x):\mathbf x=\alpha\mathbf x_1+(1-\alpha)\mathbf x_2,\ \mathbf h(\mathbf x_i)=\mathbf y_i\}\le\alpha\omega(\mathbf y_1)+(1-\alpha)\omega(\mathbf y_2).$$

Now separate the **epigraph** of $\omega$ from the vertical ray below $f^\star$ at $\mathbf y=\mathbf 0$. A convex function's epigraph is convex, so a supporting hyperplane exists; its slope is $-\boldsymbol\lambda$, and the separation inequality says exactly that $\mathbf x^\star$ minimizes the **Lagrangian relaxation** $\min_{\mathbf x\in\Omega}f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf h(\mathbf x)$ — i.e. $q(\boldsymbol\lambda)=f^\star$, **no gap.** These are called **zero-order conditions** because no derivative appears anywhere; they hold for nondifferentiable $f$, which is why they matter for LASSO and hinge losses.

**So the geometry is:** the duality gap is the vertical distance between $\omega(\mathbf 0)$ and the best supporting hyperplane at $\mathbf 0$. A convex $\omega$ has one *through* the point; a nonconvex $\omega$ can dip away from every hyperplane, and the shortfall **is** the gap. This is the same separating-hyperplane argument that proved strong duality in [[10 - Duality|ch. 10]] §5 — LP is just the case where $\omega$ is piecewise linear.

**Convexity alone is not quite enough** — one also needs the hyperplane to be non-vertical, which is what a **constraint qualification** buys. The standard one is:

> [!note] Slater's condition
> There exists a **strictly feasible** point: some $\bar{\mathbf x}$ in the relative interior of $\Omega$ with $g_j(\bar{\mathbf x})<0$ for all nonlinear $g_j$ (affine constraints only need $\le$).

**Convex + Slater ⟹ strong duality and the existence of KKT multipliers.** So the complete picture, assembled across three chapters:

| Problem class | KKT necessary? | KKT sufficient? | Duality gap |
|---|---|---|---|
| Linear program | **yes**, always (full-rank $A$) | **yes** | **zero**, always ([[10 - Duality\|ch. 10]]) |
| Convex + Slater | **yes** | **yes** | **zero** |
| Convex, Slater fails | may fail | **yes** | may be positive |
| Smooth, regular point | **yes** ([[11 - Constrained Optimization - Lagrange and KKT\|ch. 11]]) | **no** | may be positive |
| Smooth, irregular point | **may fail** | **no** | may be positive |

**The bottom two rows are where most of machine learning actually lives** — which is why "training converged" is not a claim of optimality, and why convex formulations retain their appeal despite being less expressive. Exercise 5 constructs both a finite and an infinite gap.

### 4. Semidefinite programming and linear matrix inequalities

**Semidefinite programming (SDP)** minimizes a linear objective subject to a **linear matrix inequality**. Given symmetric $F_0,\dots,F_n\in\mathbb R^{m\times m}$, the affine matrix function
$$F(\mathbf x)=F_0+x_1F_1+\cdots+x_nF_n$$
gives the constraint
$$F(\mathbf x)\succeq0,\qquad\text{meaning}\qquad \mathbf z^{\mathsf T}F(\mathbf x)\mathbf z\ge0\ \ \text{for all }\mathbf z\in\mathbb R^m,$$
i.e. $F(\mathbf x)$ is positive semidefinite. Despite the name, $F$ is **affine, not linear** — the constant $F_0$ is there. The set $\{\mathbf x:F(\mathbf x)\succeq0\}$ is **convex**: it is an intersection over all $\mathbf z$ of the half-spaces $\{\mathbf x:\mathbf z^{\mathsf T}F(\mathbf x)\mathbf z\ge0\}$, each convex because $\mathbf x\mapsto\mathbf z^{\mathsf T}F(\mathbf x)\mathbf z$ is affine. **So SDP is a convex program and everything in §§1–3 applies.**

**SDP generalises LP** exactly as matrix inequalities generalise componentwise ones: take all $F_i$ diagonal and $F(\mathbf x)\succeq0$ becomes $n$ scalar inequalities. The hierarchy is
$$\text{LP}\ \subset\ \text{QP}\ \subset\ \text{SOCP}\ \subset\ \text{SDP}\ \subset\ \text{convex programming},$$
and interior-point methods (§8) solve all of them in polynomial time. In data science SDP appears as the **relaxation of hard problems** — Max-Cut, the Lovász theta function, low-rank matrix completion via the nuclear norm, kernel learning, and sum-of-squares certificates. *(The relaxation framing is my addition; Chong & Żak present LMIs as a control-theory tool.)*

### 5. Projections: turning any unconstrained algorithm into a constrained one

Every algorithm in chapters 05–07 has the form $\mathbf x^{(k+1)}=\mathbf x^{(k)}+\alpha_k\mathbf d^{(k)}$, and **nothing stops the iterate leaving $\Omega$.** The simplest repair is to put it back:

$$\boxed{\ \mathbf x^{(k+1)}=\Pi\big[\mathbf x^{(k)}+\alpha_k\mathbf d^{(k)}\big],\qquad \Pi[\mathbf x]=\arg\min_{\mathbf z\in\Omega}\|\mathbf z-\mathbf x\|\ }$$

$\Pi[\mathbf x]$ is the **closest point of $\Omega$ to $\mathbf x$**. It is well defined for **closed convex** $\Omega$ (existence by Weierstrass, [[01 - The Optimization Problem|ch. 01]]; uniqueness by strict convexity of $\|\cdot\|^2$ on a convex set) — and for nonconvex $\Omega$ the $\arg\min$ may not be unique, so the projected method is not even well posed. **This is one more place convexity is not a convenience but a requirement.**

Applied to the gradient method, this is the **projected gradient algorithm**
$$\mathbf x^{(k+1)}=\Pi\big[\mathbf x^{(k)}-\alpha_k\nabla f(\mathbf x^{(k)})\big].$$

**Projections you should know by heart** *(this table is my addition — Chong & Żak give only the box case):*

| $\Omega$ | $\Pi[\mathbf x]$ | cost |
|---|---|---|
| **Box** $\{l_i\le x_i\le u_i\}$ | clip componentwise: $\min(u_i,\max(l_i,x_i))$ | $O(n)$ |
| **Nonnegative orthant** $\{\mathbf x\ge\mathbf 0\}$ | $\max(x_i,0)$ | $O(n)$ |
| **Euclidean ball** $\{\|\mathbf x\|\le R\}$ | $\mathbf x$ if $\|\mathbf x\|\le R$, else $R\mathbf x/\|\mathbf x\|$ | $O(n)$ |
| **Sphere** $\{\|\mathbf x\|=1\}$ | $\mathbf x/\|\mathbf x\|$ (undefined at $\mathbf 0$) | $O(n)$ |
| **Affine set** $\{A\mathbf x=\mathbf b\}$ | $\mathbf x-A^{\mathsf T}(AA^{\mathsf T})^{-1}(A\mathbf x-\mathbf b)$ | one solve |
| **Probability simplex** $\{\mathbf x\ge\mathbf 0,\ \mathbf 1^{\mathsf T}\mathbf x=1\}$ | sort-and-threshold: $\max(x_i-\tau,0)$ with $\tau$ chosen so the sum is 1 | $O(n\log n)$ |
| **$\ell_1$ ball** $\{\|\mathbf x\|_1\le t\}$ | soft-threshold with a bisection on the threshold | $O(n\log n)$ |

> [!warning] Projection can be as hard as the original problem
> $\Pi$ is itself defined by an optimization problem, and it need not be easier than the one you started with. Chong & Żak's own example: for $\min\|\mathbf x\|^2$ subject to $\mathbf x\in\Omega$, the answer is literally $\Pi[\mathbf 0]$. **So if $\mathbf 0\notin\Omega$, computing one projection is exactly solving the original problem.** Projected methods pay off only when $\Omega$ is one of the sets above — which, fortunately, covers most constraints that arise in practice.

**For linear equality constraints there is a clean closed form.** Take
$$\text{minimize } f(\mathbf x)\quad\text{subject to}\quad A\mathbf x=\mathbf b,\qquad A\in\mathbb R^{m\times n},\ \operatorname{rank}A=m<n,$$
and let $P=I_n-A^{\mathsf T}(AA^{\mathsf T})^{-1}A$ be the **orthogonal projector** onto $\mathcal N(A)$ — the same matrix as [[08 - Least Squares and Linear Equations|ch. 08]]'s hat matrix, complemented, with $P=P^{\mathsf T}$ and $P^2=P$. Two facts:

- **$\mathcal N(P)=\mathcal R(A^{\mathsf T})$ and $\mathcal R(P)=\mathcal N(A)$.** *(Proof of the first: if $P\mathbf v=\mathbf 0$ then $\mathbf v=A^{\mathsf T}(AA^{\mathsf T})^{-1}A\mathbf v\in\mathcal R(A^{\mathsf T})$; conversely $P A^{\mathsf T}\mathbf u=A^{\mathsf T}\mathbf u-A^{\mathsf T}(AA^{\mathsf T})^{-1}AA^{\mathsf T}\mathbf u=\mathbf 0$.)*
- **Hence the Lagrange condition is exactly $P\nabla f(\mathbf x^\star)=\mathbf 0$.** Indeed $P\nabla f=\mathbf 0\iff\nabla f\in\mathcal R(A^{\mathsf T})\iff\exists\boldsymbol\lambda^\star:\nabla f(\mathbf x^\star)+A^{\mathsf T}\boldsymbol\lambda^\star=\mathbf 0$, which with $A\mathbf x=\mathbf b$ is [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]]'s condition. **A beautifully compact restatement, and it doubles as the stopping criterion.**

The projected step then simplifies — the projection can be pushed onto the *gradient* instead of the point:
$$\Pi\big[\mathbf x^{(k)}-\alpha_k\nabla f(\mathbf x^{(k)})\big]=\mathbf x^{(k)}-\alpha_kP\nabla f(\mathbf x^{(k)})\qquad\text{(for feasible }\mathbf x^{(k)}).$$
**Feasibility is preserved automatically**, since $A\mathbf x^{(k+1)}=A\mathbf x^{(k)}-\alpha_kAP\nabla f=\mathbf b-\mathbf 0=\mathbf b$. And $-P\nabla f$ is the **steepest feasible descent direction**: for any feasible unit $\mathbf d=P\mathbf v$,
$$\langle\nabla f,\mathbf d\rangle=\langle\nabla f,P^{\mathsf T}\mathbf v\rangle=\langle P\nabla f,\mathbf v\rangle\le\|P\nabla f\|\,\|\mathbf v\|$$
by Cauchy–Schwarz, with equality iff $\mathbf v\parallel P\nabla f$ — the same argument as [[05 - Gradient Methods|ch. 05]] §2, now restricted to $\mathcal N(A)$. A Taylor expansion using $P=P^{\mathsf T}P$ gives
$$f\big(\mathbf x-\alpha P\nabla f(\mathbf x)\big)=f(\mathbf x)-\alpha\|P\nabla f(\mathbf x)\|^2+o(\alpha),$$
so **the projected steepest descent method is a genuine descent method** whenever $P\nabla f(\mathbf x^{(k)})\ne\mathbf 0$, and it stops precisely at points satisfying the Lagrange condition — which by §2 are **global** minimizers when $f$ is convex.

> [!example]- Worked example — projected gradient is the power method in disguise (C&Ż Example 23.1)
> $$\text{minimize } \tfrac12\mathbf x^{\mathsf T}Q\mathbf x\quad\text{subject to}\quad \|\mathbf x\|^2=1,\qquad Q=Q^{\mathsf T}>0.$$
> Here $\Pi[\mathbf x]=\mathbf x/\|\mathbf x\|$, so with fixed step $\alpha$ the iteration is
> $$\mathbf x^{(k+1)}=\beta_k(I-\alpha Q)\mathbf x^{(k)},\qquad \beta_k=1/\|(I-\alpha Q)\mathbf x^{(k)}\| .$$
> **That is the power method applied to $I-\alpha Q$.** Expanding $\mathbf x^{(k)}$ in eigenvectors of $Q$, the coefficient of $\mathbf v_i$ is multiplied by $(1-\alpha\lambda_i)$ each step, so
> $$\frac{y_i^{(k)}}{y_1^{(k)}}=\frac{y_i^{(0)}}{y_1^{(0)}}\left(\frac{1-\alpha\lambda_i}{1-\alpha\lambda_1}\right)^{\!k}\longrightarrow0\quad\text{for }i>1,$$
> since $\lambda_i>\lambda_1$ and $\alpha<1/\lambda_{\max}$ make the ratio $<1$ in magnitude. **So $\mathbf x^{(k)}\to\mathbf v_1$, the eigenvector of the *smallest* eigenvalue** — correct, since we are minimizing. Convergence needs $y_1^{(0)}\ne0$: **the start must not be orthogonal to $\mathbf v_1$.**
>
> **And the method can fail for arbitrarily small $\alpha>0$** (part b): if $\mathbf x^{(0)}$ is *any* eigenvector then $(I-\alpha Q)\mathbf x^{(0)}=(1-\alpha\lambda_i)\mathbf x^{(0)}$, which normalises back to $\mathbf x^{(0)}$. **Every eigenvector is a fixed point**, so starting at the wrong one leaves you stuck forever, however small the step. That is a KKT point that is not a minimizer — [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §7's middle eigenvector, met again as an algorithmic trap. *(Note $\|\mathbf x\|^2=1$ is not a convex constraint, which is exactly why this pathology is available.)*
>
> Verified with $Q=\operatorname{tridiag}(1,3,1)$, eigenvalues $\{1.585786,3,4.414214\}$ and $\alpha=0.9/\lambda_{\max}=0.2039$: from a generic start the iteration converges to $\pm(0.5,0.707107,0.5)$ with $\mathbf x^{\mathsf T}Q\mathbf x=1.58578644=\lambda_{\min}$ ✓; started at the top eigenvector it holds $\mathbf x^{\mathsf T}Q\mathbf x=4.4142135624=\lambda_{\max}$ for every iteration ✓.

### 6. Primal–dual (Lagrangian) algorithms

A second idea: since [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §5 showed the Lagrange condition is stationarity of $l(\mathbf x,\boldsymbol\lambda)=f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf h(\mathbf x)$, run gradient descent on $\mathbf x$ and gradient **ascent** on $\boldsymbol\lambda$ simultaneously:

$$\mathbf x^{(k+1)}=\mathbf x^{(k)}-\alpha_k\big(\nabla f(\mathbf x^{(k)})+D\mathbf h(\mathbf x^{(k)})^{\mathsf T}\boldsymbol\lambda^{(k)}\big),\qquad \boldsymbol\lambda^{(k+1)}=\boldsymbol\lambda^{(k)}+\beta_k\,\mathbf h(\mathbf x^{(k)}).$$

**Descent in $\mathbf x$, ascent in $\boldsymbol\lambda$** — because §5 of chapter 11 warned that $(\mathbf x^\star,\boldsymbol\lambda^\star)$ is a **saddle point**, so you cannot descend in both. The $\boldsymbol\lambda$-update is transparent: a violated constraint ($h_i\ne0$) raises its own price until the $\mathbf x$-update takes it seriously.

For inequality constraints, $l(\mathbf x,\boldsymbol\mu)=f(\mathbf x)+\boldsymbol\mu^{\mathsf T}\mathbf g(\mathbf x)$ and
$$\boldsymbol\mu^{(k+1)}=\big[\boldsymbol\mu^{(k)}+\beta_k\,\mathbf g(\mathbf x^{(k)})\big]_+,\qquad [\cdot]_+=\max\{\cdot,0\}\ \text{componentwise},$$
i.e. a **projected** ascent step, the projection enforcing $\boldsymbol\mu\ge\mathbf 0$ — projection onto the nonnegative orthant, from §5's table.

**Fixed points are exactly Lagrange/KKT points** (immediate by inspection: $\mathbf x$ unchanged ⟺ stationarity; $\boldsymbol\lambda$ unchanged ⟺ $\mathbf h=\mathbf 0$; and for inequalities the clipped update is stationary iff complementary slackness plus feasibility hold). And convergence is **local and linear**:

**Theorem.** *If $L(\mathbf x^\star,\boldsymbol\lambda^\star)>0$ on the relevant subspace and $\mathbf x^\star$ is regular, then for sufficiently small $\alpha,\beta$ there is a neighbourhood of $(\mathbf x^\star,\boldsymbol\lambda^\star)$ from which the algorithm converges, with at least linear order.*

The proof is worth knowing in outline because it explains the step-size restriction. Stack $\mathbf w=(\mathbf x,\boldsymbol\lambda)$ so the iteration is $\mathbf w^{(k+1)}=U(\mathbf w^{(k)})$ with
$$DU(\mathbf w)=I+\alpha M,\qquad M=\begin{bmatrix}-L(\mathbf x,\boldsymbol\lambda)&-D\mathbf h(\mathbf x)^{\mathsf T}\\ D\mathbf h(\mathbf x)&0\end{bmatrix}.$$
By the mean value theorem $\|\mathbf w^{(k+1)}-\mathbf w^\star\|\le\|G(\mathbf w^{(k)})\|\,\|\mathbf w^{(k)}-\mathbf w^\star\|$, so it suffices that $\|DU(\mathbf w^\star)\|<1$, i.e. that **$M$'s eigenvalues lie in the open left half-plane.** For an eigenpair $(\lambda,\mathbf w)$ of $M$, $\Re(\mathbf w^HM\mathbf w)=\Re(\lambda)\|\mathbf w\|^2$; but the off-diagonal blocks are skew-adjoint, so their contributions cancel and
$$\Re(\mathbf w^HM\mathbf w)=-\Re\big(\mathbf x^HL(\mathbf x^\star,\boldsymbol\lambda^\star)\mathbf x\big)<0$$
whenever $\mathbf x\ne\mathbf 0$ — which regularity guarantees, since $\mathbf x=\mathbf 0$ would force $D\mathbf h(\mathbf x^\star)^{\mathsf T}\boldsymbol\lambda=\mathbf 0$ and hence $\boldsymbol\lambda=\mathbf 0$, contradicting $\mathbf w\ne\mathbf 0$. **So the skew structure is what makes the saddle point attracting** — and it works only for small $\alpha$, since $I+\alpha M$ has spectral radius $<1$ only then. The inequality-constrained proof adds two phases: inactive multipliers hit zero in **finite** time and stay there, after which the active block converges linearly. *(The projection is a **nonexpansive** map, $\|\Pi[\mathbf u]-\Pi[\mathbf v]\|\le\|\mathbf u-\mathbf v\|$, which is why inserting it cannot spoil the contraction — a fact worth remembering in its own right.)*

**In ML this is everywhere**, under other names: the multiplier update is exactly how a **Lagrangian penalty is tuned automatically** in constrained deep learning (fairness constraints, calibration, KL budgets in TRPO/PPO/RLHF). The saddle-point structure is also why **GAN training is delicate** — it is the same min–max, without the convexity that would make it well behaved.

### 7. Penalty methods

The third idea abandons the constraint set entirely and pays a fine for leaving it. Replace
$$\text{minimize } f(\mathbf x)\ \text{ s.t. }\ \mathbf x\in\Omega \qquad\text{by}\qquad \text{minimize } q(\gamma,\mathbf x)=f(\mathbf x)+\gamma P(\mathbf x)$$
where $\gamma>0$ is the **penalty parameter** and $P$ a **penalty function**: (i) continuous, (ii) $P\ge0$, (iii) $P(\mathbf x)=0$ **iff** $\mathbf x$ is feasible. The new problem is **unconstrained**, so every method of chapters 04–07 applies unchanged.

For $\mathbf g(\mathbf x)\le\mathbf 0$ the standard choices are
$$P(\mathbf x)=\sum_j g_j^+(\mathbf x),\quad g_j^+=\max\{0,g_j\}\qquad\text{(\textbf{absolute value} penalty)}$$
$$P(\mathbf x)=\sum_j\big(g_j^+(\mathbf x)\big)^2\qquad\text{(\textbf{Courant–Beltrami} penalty)}$$
The first is $\sum|g_j|$ over the *violated* constraints only. **It is generally not differentiable** where $g_j=0$ — e.g. $g_1=x-2$ gives a kink in $P$ at $x=2$ — which rules out gradient methods; the squared form is differentiable and is the default. (An equality $h=0$ can be written $\|h\|^2\le0$, so treating only inequalities is not restrictive.)

**The theory says larger $\gamma$ is better.** Let $\gamma_k\nearrow$ and let $\mathbf x^{(k)}$ minimize $q(\gamma_k,\cdot)$. Then:

$$\text{(1) }q(\gamma_{k+1},\mathbf x^{(k+1)})\ge q(\gamma_k,\mathbf x^{(k)}),\quad \text{(2) }P(\mathbf x^{(k+1)})\le P(\mathbf x^{(k)}),\quad \text{(3) }f(\mathbf x^{(k+1)})\ge f(\mathbf x^{(k)}),$$
$$\text{(4) }f(\mathbf x^\star)\ \ge\ q(\gamma_k,\mathbf x^{(k)})\ \ge\ f(\mathbf x^{(k)}).$$

Read them together and the mechanism is clear. **(2): iterates become steadily more feasible. (3): and steadily more expensive.** The two are the same trade-off seen twice. **(4) is the useful one: $f(\mathbf x^{(k)})$ is a *lower* bound on the true optimal value** — the penalty iterate is infeasible, so it cheats and undershoots; and $q(\gamma_k,\mathbf x^{(k)})$ is a *better* lower bound that increases towards $f^\star$. So penalty methods, like [[10 - Duality|ch. 10]]'s dual, generate certified bounds along the way. *(Proofs are short: each follows from the defining inequality $q(\gamma_k,\mathbf x^{(k)})\le q(\gamma_k,\mathbf x^{(k+1)})$, plus $P(\mathbf x^\star)=0$ for (4).)*

> [!example]- Worked example — penalty method on the sphere, and a book error (C&Ż Example 23.3)
> $$\text{minimize } \mathbf x^{\mathsf T}Q\mathbf x\ \text{ s.t. }\ \|\mathbf x\|^2=1,\qquad P(\mathbf x)=(\|\mathbf x\|^2-1)^2 .$$
> The unconstrained surrogate is $\min\ \mathbf x^{\mathsf T}Q\mathbf x+\gamma(\|\mathbf x\|^2-1)^2$, whose FONC reads
> $$2Q\mathbf x_\gamma+4\gamma(\|\mathbf x_\gamma\|^2-1)\mathbf x_\gamma=\mathbf 0 \qquad\Longrightarrow\qquad Q\mathbf x_\gamma=\lambda_\gamma\mathbf x_\gamma,\quad \lambda_\gamma=2\gamma(1-\|\mathbf x_\gamma\|^2).$$
> **So $\mathbf x_\gamma$ is an eigenvector of $Q$ for every $\gamma$** — agreeing with [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §7's exact solution, which is a reassuring consistency check. Rearranging,
> $$\|\mathbf x_\gamma\|^2-1=-\frac{\lambda_\gamma}{2\gamma}=O(1/\gamma),$$
> so **the iterate is infeasible by $O(1/\gamma)$** and approaches the sphere from inside.
>
> **⚠️ The book gets this last step wrong.** Chong & Żak write "$\lambda_\gamma=2\gamma(1-\|\mathbf x_\gamma\|^2)\le\lambda_{\max}$, hence $\|\mathbf x_\gamma\|^2-1=-\lambda_{\max}/(2\gamma)=O(1/\gamma)$." The **bound** is fine but the **equality is not**: the correct value is $-\lambda_\gamma/(2\gamma)$, and for a *minimization* problem $\lambda_\gamma\to\lambda_{\min}$, not $\lambda_{\max}$. Verified with $Q=\operatorname{tridiag}(1,3,1)$ ($\lambda_{\min}=1.585786$, $\lambda_{\max}=4.414214$):
>
> | $\gamma$ | $\|\mathbf x_\gamma\|^2-1$ | $\lambda_\gamma$ | $-\lambda_{\min}/2\gamma$ | $-\lambda_{\max}/2\gamma$ |
> |---|---|---|---|---|
> | $10$ | $-0.0792893$ | $1.585786$ | $-0.0792893$ ✓ | $-0.2207107$ ✗ |
> | $100$ | $-0.0079289$ | $1.585787$ | $-0.0079289$ ✓ | $-0.0220711$ ✗ |
> | $10^4$ | $-0.0000793$ | $1.585865$ | $-0.0000793$ ✓ | $-0.0002207$ ✗ |
>
> The book's expression is wrong by a factor of $\lambda_{\max}/\lambda_{\min}=2.78$ here — **which is exactly the [[05 - Gradient Methods|condition number]]**, so the error is unbounded across problems. **Only the $O(1/\gamma)$ conclusion survives.** Note also that $\gamma\cdot(\|\mathbf x_\gamma\|^2-1)\to-\lambda_{\min}/2$ is essentially constant down the table — the signature of exact $O(1/\gamma)$ behaviour.

> [!warning] Why $\gamma\to\infty$ is a trap in practice
> The theory wants $\gamma$ large; numerics want it small. As $\gamma$ grows the surrogate's Hessian becomes dominated by $\gamma\nabla^2P$, whose curvature across the constraint is $O(\gamma)$ while curvature along it stays $O(1)$ — so the **condition number grows like $\gamma$** and, by [[05 - Gradient Methods|ch. 05]]'s Kantorovich rate, gradient methods slow to a crawl and Newton's method loses accuracy to round-off. **This is why you solve a sequence of problems with increasing $\gamma$, warm-starting each from the last**, rather than jumping to $\gamma=10^{12}$. It is also why **augmented Lagrangian** methods (which add the penalty *to the Lagrangian*, keeping $\boldsymbol\lambda$ around so $\gamma$ need not blow up) displaced pure penalty methods. Exercise 3 exhibits the $O(1/\gamma)$ error concretely.

### 8. Barrier methods and interior-point methods

The fourth idea inverts the third: instead of penalising the outside, make the **boundary infinitely expensive from within**.

A **barrier function** $B$ on the interior of $S=\{\mathbf x:g_i(\mathbf x)\le0\}$ satisfies (i) continuous, (ii) $B\ge0$, (iii) **$B(\mathbf x)\to\infty$ as $\mathbf x$ approaches the boundary.** The set must be **robust** — a nonempty interior from which every boundary point is approachable — or there is no interior to search. Two standard barriers:

$$B(\mathbf x)=-\sum_i\frac1{g_i(\mathbf x)}\qquad\text{and}\qquad \boxed{\ B(\mathbf x)=-\sum_i\log\big(-g_i(\mathbf x)\big)\ }$$

The second, the **logarithmic barrier**, is the one used by every interior-point LP solver. Solve
$$\text{minimize } f(\mathbf x)+\mu B(\mathbf x)\quad\text{over the interior of }S,\qquad \mu\searrow0$$
(equivalently $f+\tfrac1cB$ with $c\nearrow\infty$). **Although formally constrained, this is computationally unconstrained:** an iterative descent method started at an interior point can never reach the boundary, because the objective blows up there. The constraint enforces itself. Convergence mirrors the penalty case — any limit point of $\{\mathbf x^{(k)}\}$ solves the original problem.

**The sequence of solutions $\mathbf x(\mu)$ traces the central path.** As $\mu\to0$ it converges to the optimum; as $\mu\to\infty$ it converges to the **analytic center** of the feasible set, the point maximizing $\prod_i(-g_i(\mathbf x))$ — the "most interior" point. Interior-point methods **follow this path** from the analytic center towards the optimum, taking Newton steps ([[06 - Newton and Quasi-Newton Methods|ch. 06]]) on the barrier subproblem and decreasing $\mu$ geometrically.

**Why this matters historically and practically.** [[09 - Linear Programming and the Simplex Method|Chapter 09]] §7 noted that simplex is exponential in the worst case (Klee–Minty) but excellent in practice. Interior-point methods are **polynomial-time**, and because the log barrier keeps iterates strictly inside they are blind to the exponentially many vertices simplex might visit — the central path cuts through the interior. In practice: simplex still wins on small and mid-sized LPs and warm-starts beautifully (which is why the [[10 - Duality|dual simplex]] is used for re-solves after a right-hand-side change), while interior-point wins on large sparse problems, and is the *only* practical option for QP, SOCP and SDP. Modern solvers ship both. Exercise 4 computes a central path in closed form.

> [!note] Penalty vs barrier in one line
> **Penalty methods approach the optimum from *outside* the feasible set** (infeasible iterates, feasible in the limit). **Barrier methods approach from *inside*** (always feasible, optimal in the limit). If your constraints are hard — a physical limit, a probability that must stay in $[0,1]$, a matrix that must stay positive definite — **use a barrier**, because a penalty method will hand you a slightly infeasible answer.

### 9. The rest of the landscape

*(This section is my own; it collects what the four books either scatter or omit, and closes the promises made in `00-Index.md`.)*

**Proximal gradient / ISTA.** The projected gradient step generalises beautifully. For $\min f(\mathbf x)+r(\mathbf x)$ with $f$ smooth and $r$ convex but possibly nondifferentiable, iterate
$$\mathbf x^{(k+1)}=\operatorname{prox}_{\alpha r}\big(\mathbf x^{(k)}-\alpha\nabla f(\mathbf x^{(k)})\big),\qquad \operatorname{prox}_{\alpha r}(\mathbf v)=\arg\min_{\mathbf z}\Big\{r(\mathbf z)+\tfrac1{2\alpha}\|\mathbf z-\mathbf v\|^2\Big\}.$$
Taking $r=$ the indicator function of $\Omega$ (zero on $\Omega$, $+\infty$ off it) recovers **projection exactly** — so projection is a special case of the prox operator. Taking $r=\lambda\|\mathbf x\|_1$ gives $\operatorname{prox}=$ **soft-thresholding**, $\operatorname{sign}(v_i)\max(|v_i|-\alpha\lambda,0)$, and the algorithm is **ISTA** — the standard LASSO solver. Its accelerated version, **FISTA**, attains the $O(1/k^2)$ optimal rate for this class. **This is the single most useful algorithm in this chapter for a data scientist**, and none of the four books contains it.

**ADMM** splits $\min f(\mathbf x)+r(\mathbf z)$ s.t. $\mathbf x=\mathbf z$ and alternates an $\mathbf x$-step, a $\mathbf z$-step and a multiplier update — an augmented Lagrangian method (§7) with a splitting. It parallelises across data and is the workhorse of distributed convex optimization.

**Mirror descent** replaces the Euclidean projection with a Bregman projection matched to the geometry — on the probability simplex this yields multiplicative updates and $O(\sqrt{\log n/k})$ rates instead of $O(\sqrt{n/k})$. It is why exponentiated-gradient and boosting-style updates look the way they do.

**Sequential quadratic programming (SQP)** is the standard general-purpose NLP method: at each iterate, minimize a quadratic model of the Lagrangian subject to *linearised* constraints. The subproblem is exactly the equality-constrained QP of C&Ż §20.6, whose closed form is $\mathbf x^\star=Q^{-1}A^{\mathsf T}(AQ^{-1}A^{\mathsf T})^{-1}\mathbf b$ — **the reason that formula is worth having.** SQP with a BFGS approximation to $L$ ([[06 - Newton and Quasi-Newton Methods|ch. 06]]) is what `scipy.optimize.minimize(method='SLSQP')` runs.

**Global search heuristics** (C&Ż ch. 14) — Nelder–Mead, simulated annealing, particle swarm, genetic algorithms — abandon derivatives and guarantees in exchange for the ability to escape local minima. **They have no convergence theory worth the name**, and for the one place a DS reader meets them, hyperparameter tuning, **random search and Bayesian optimization have displaced them** (random search beats grid search because good hyperparameters are usually low-dimensional in effect; Bayesian optimization adds a surrogate model). Nelder–Mead remains a reasonable default for a low-dimensional, noisy, derivative-free objective, and is `scipy`'s fallback.

**Multiobjective optimization** (C&Ż ch. 24) asks what to do with several objectives at once. A point is **Pareto optimal** if no other feasible point improves one objective without worsening another; the set of their images is the **Pareto front**. The standard reduction is **scalarisation** — minimize $\sum_iw_if_i(\mathbf x)$ with $\mathbf w>\mathbf 0$, which recovers points on the *convex* part of the front but **provably misses non-convex regions**, so the $\varepsilon$-constraint method (optimize one objective, bound the rest) is used when the front's shape matters. **A DS reader meets this constantly and rarely by name:** the precision–recall and ROC curves *are* Pareto fronts; so is the accuracy-versus-fairness trade-off, the bias–variance trade-off, and the loss-versus-latency trade-off in model selection. **Choosing a threshold on an ROC curve is choosing a point on a Pareto front**, and the fact that no single point is "optimal" is a theorem, not a failure of analysis.

**What to reach for, in practice:**

| Problem | Method |
|---|---|
| Smooth, unconstrained, medium $n$ | BFGS / L-BFGS ([[06 - Newton and Quasi-Newton Methods\|ch. 06]]) |
| Smooth, unconstrained, huge $n$, stochastic | SGD + momentum / Adam ([[05 - Gradient Methods\|ch. 05]] §8) |
| Simple constraints (box, ball, simplex) | projected gradient (§5) |
| Smooth $+$ nonsmooth regulariser | proximal gradient / FISTA (§9) |
| LP | simplex or interior-point ([[09 - Linear Programming and the Simplex Method\|ch. 09]], §8) |
| QP, SOCP, SDP | interior-point (§8) |
| General smooth NLP | SQP or interior-point (§9) |
| Constraint that must be tuned automatically | augmented Lagrangian / primal–dual (§§6–7) |
| Nonconvex, derivative-free, low $n$ | Nelder–Mead, Bayesian optimization (§9) |

**And the two questions to ask before any of it:** *is it convex?* — if yes, any KKT point is the global answer and you can stop worrying; and *what does the dual say?* — because it certifies the answer and prices every constraint.

## ✏️ Exercises

**1. (Convexity turns a guess into a proof.)** Consider
$$\text{minimize } f(\mathbf x)=x_1^2+2x_2^2-2x_1-8x_2 \quad\text{subject to}\quad x_1+x_2\le3,\ \ x_1\ge0,\ \ x_2\ge0 .$$
(a) Verify the problem is convex. (b) Show that $\mathbf x^\star=(1,2)$ satisfies the KKT conditions. (c) State precisely what conclusion you may now draw, and which theorem licenses it.

> [!example]- Solution
> **(a)** $\nabla^2f=\begin{bmatrix}2&0\\0&4\end{bmatrix}\succ0$, so $f$ is (strictly) convex by [[02 - Convex Sets and Convex Functions|ch. 02]]'s Hessian test. The feasible set is the intersection of three half-spaces, hence a **convex** polyhedron; equivalently all three $g_j$ are affine and therefore convex, so §1 applies. **This is a convex program** — indeed a QP.
>
> **(b)** With $g_1=x_1+x_2-3$, $g_2=-x_1$, $g_3=-x_2$ we need $\boldsymbol\mu\ge\mathbf 0$. At $\mathbf x^\star=(1,2)$:
> $$\nabla f(\mathbf x^\star)=(2x_1-2,\ 4x_2-8)=(0,\ 0).$$
> The gradient vanishes. Check feasibility: $g_1=1+2-3=0$ (**active**), $g_2=-1<0$, $g_3=-2<0$. So take
> $$\mu_1^\star=\mu_2^\star=\mu_3^\star=0 .$$
> Stationarity: $(0,0)+0=\mathbf 0$ ✓. Dual feasibility: $\boldsymbol\mu^\star=\mathbf 0\ge\mathbf 0$ ✓. Complementary slackness: $\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0$ ✓ (every term is zero). Primal feasibility ✓. **All five KKT conditions hold**, with $f(\mathbf x^\star)=1+8-2-16=-9$.
>
> **(c)** By the **KKT sufficiency theorem** (§2), $\mathbf x^\star=(1,2)$ is a **global** minimizer of $f$ over the feasible set. Because $f$ is *strictly* convex it is the **unique** global minimizer.
>
> **Three things worth noticing.** (i) The unconstrained minimizer happens to be feasible, so all multipliers are zero — the constraints cost nothing, and by the sensitivity result of [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §11 every shadow price is $0$: relaxing the budget $3$ would not help. (ii) $g_1$ is **active with $\mu_1^\star=0$** — a degenerate constraint, the same phenomenon as [[10 - Duality|ch. 10]] Exercise 4 and ch. 11 §8. The optimum sits exactly on the wall without pushing against it. (iii) **Without convexity, (b) would prove nothing at all** — merely that $(1,2)$ is a candidate. Convexity is doing all the work in (c).

**2. (Projections, and a projected gradient step.)** Compute $\Pi[\mathbf v]$ for $\mathbf v=(2,-1,0.5)$ onto each of: (a) the box $[0,1]^3$; (b) the unit ball $\{\|\mathbf x\|\le1\}$; (c) the affine set $\{\mathbf x:x_1+x_2+x_3=1\}$; (d) the probability simplex. (e) Then take one projected gradient step on $\min\|\mathbf x\|^2$ over the box, from $\mathbf x^{(0)}=(0.8,0.9,0.2)$ with $\alpha=0.5$.

> [!example]- Solution
> **(a) Box $[0,1]^3$** — clip each coordinate: $\Pi[\mathbf v]=(\mathbf{1},\ \mathbf{0},\ \mathbf{0.5})$.
>
> **(b) Unit ball.** $\|\mathbf v\|=\sqrt{4+1+0.25}=\sqrt{5.25}=2.291288$. Since $>1$, scale to the boundary:
> $$\Pi[\mathbf v]=\mathbf v/\|\mathbf v\|=(0.872872,\ -0.436436,\ 0.218218),$$
> which has norm $1$ ✓.
>
> **(c) Affine set** $A=[1,1,1]$, $b=1$, so $AA^{\mathsf T}=3$ and $A\mathbf v-b=1.5-1=0.5$:
> $$\Pi[\mathbf v]=\mathbf v-A^{\mathsf T}(AA^{\mathsf T})^{-1}(A\mathbf v-b)=\mathbf v-\tfrac{0.5}3(1,1,1)=(\mathbf{1.833\overline3},\ \mathbf{-1.1\overline6},\ \mathbf{0.3\overline3}),$$
> summing to $1$ ✓. Note this is **not** the answer to (d) — it ignores $\mathbf x\ge\mathbf 0$.
>
> **(d) Probability simplex.** Find $\tau$ with $\sum_i\max(v_i-\tau,0)=1$. Sort descending: $(2,\ 0.5,\ -1)$. Try keeping only the top coordinate: $\tau=2-1=1$, and then $\max(0.5-1,0)=0$ ✓, $\max(-1-1,0)=0$ ✓, so the sum is exactly $1$ and the guess is consistent. Hence
> $$\Pi[\mathbf v]=(\mathbf 1,\ \mathbf 0,\ \mathbf 0).$$
> **A sanity check that this is genuinely closest:** its squared distance is $1+1+0.25=2.25$, while the (c) answer is infeasible and, e.g., $(0.75,0,0.25)$ gives $1.5625+1+0.0625=2.625>2.25$ ✓.
>
> **(e) One projected gradient step.** $f=\|\mathbf x\|^2$, $\nabla f=2\mathbf x$, so
> $$\mathbf x^{(0)}-\alpha\nabla f(\mathbf x^{(0)})=(0.8,0.9,0.2)-0.5\cdot(1.6,1.8,0.4)=(0,\ 0,\ 0),$$
> and $\Pi[(0,0,0)]=(0,0,0)$, which is already in the box. So $\mathbf x^{(1)}=(\mathbf 0,\mathbf 0,\mathbf 0)$ — and it is the exact global minimizer, since $\mathbf 0$ minimizes $\|\mathbf x\|^2$ and lies in $[0,1]^3$. *(With $\alpha=0.5$ the step is exact for this $f$ because $\mathbf x-\tfrac12\cdot2\mathbf x=\mathbf 0$; that is Newton's method on a quadratic in disguise, [[06 - Newton and Quasi-Newton Methods|ch. 06]].)*
>
> **The lesson of (c) versus (d):** projections do **not** compose. Projecting onto $\{\mathbf 1^{\mathsf T}\mathbf x=1\}$ and then onto $\{\mathbf x\ge\mathbf 0\}$ gives $(1.8\overline3,0,0.3\overline3)$, which is not on the simplex and is not the projection onto the intersection. **Projecting onto an intersection is a genuinely harder problem than projecting onto each piece** — which is exactly why the simplex needs its own sort-and-threshold algorithm, and why ADMM (§9) exists.

**3. (Penalty method — the $O(1/\gamma)$ error, exactly.)** Apply the penalty method with $P(x)=\big(\max\{0,1-x\}\big)^2$ to
$$\text{minimize } x^2\quad\text{subject to}\quad x\ge1 .$$
Find $x_\gamma$ in closed form, compute the infeasibility, take $\gamma\to\infty$, and state two practical conclusions.

> [!example]- Solution
> The true answer is $x^\star=1$, $f^\star=1$ (the objective increases away from the origin, so it is pushed to the boundary). The surrogate is
> $$q(\gamma,x)=x^2+\gamma(1-x)^2\qquad\text{(valid where }x<1\text{, which is where the iterate will sit)}.$$
> Then $q'=2x-2\gamma(1-x)=0$ gives $2x(1+\gamma)=2\gamma$, so
> $$\boxed{\ x_\gamma=\frac{\gamma}{\gamma+1}\ },\qquad f(x_\gamma)=\frac{\gamma^2}{(\gamma+1)^2},\qquad \text{infeasibility }=1-x_\gamma=\frac1{\gamma+1}.$$
> $q''=2+2\gamma>0$, so this is the global minimizer of the (strictly convex) surrogate.
>
> | $\gamma$ | $x_\gamma$ | $1-x_\gamma$ | $1/\gamma$ |
> |---|---|---|---|
> | $1$ | $0.5$ | $0.5$ | $1$ |
> | $10$ | $0.90909091$ | $0.09090909$ | $0.1$ |
> | $100$ | $0.99009901$ | $0.00990099$ | $0.01$ |
> | $1000$ | $0.99900100$ | $0.00099900$ | $0.001$ |
>
> As $\gamma\to\infty$, $x_\gamma\to1=x^\star$ ✓, with $1-x_\gamma=\tfrac1\gamma-\tfrac1{\gamma^2}+O(\gamma^{-3})=O(1/\gamma)$ ✓ (all verified symbolically).
>
> **Two practical conclusions.**
> 1. **Every penalty iterate is infeasible**, and the infeasibility decays only as $O(1/\gamma)$ — so $\gamma=10^6$ buys about six digits, no more. Confirm against §7's Lemma: $f(x_\gamma)=\gamma^2/(\gamma+1)^2<1=f(x^\star)$ ✓, the iterate undershoots the true value, exactly as part (4) predicts. **If feasibility is non-negotiable, use a barrier method instead** (§8, Exercise 4).
> 2. **The surrogate becomes ill-conditioned.** $q''(x)=2+2\gamma$ grows linearly in $\gamma$, so in $n$ dimensions the condition number of the penalised Hessian grows like $\gamma$ and, by [[05 - Gradient Methods|ch. 05]]'s Kantorovich rate, iteration counts grow with it. Hence the standard practice: **solve a sequence with $\gamma_k\nearrow$, warm-starting each from the previous solution**, and prefer an augmented Lagrangian if high accuracy is needed.

**4. (Barrier method and the central path.)** Apply the logarithmic barrier to
$$\text{minimize } -x\quad\text{subject to}\quad 0\le x\le1 .$$
Derive $x(\mu)$ in closed form, evaluate the limits $\mu\to0$ and $\mu\to\infty$, and compare the convergence with Exercise 3.

> [!example]- Solution
> The true answer is $x^\star=1$, $f^\star=-1$. Writing the constraints as $g_1=x-1\le0$ and $g_2=-x\le0$, the log barrier is $B(x)=-\log(1-x)-\log x$, so the subproblem is
> $$\text{minimize } \phi_\mu(x)=-x-\mu\log(1-x)-\mu\log x\quad\text{on }(0,1).$$
> Stationarity: $-1+\dfrac\mu{1-x}-\dfrac\mu x=0$. Multiplying by $x(1-x)>0$:
> $$-x(1-x)+\mu x-\mu(1-x)=0\ \Longrightarrow\ x^2+(2\mu-1)x-\mu=0,$$
> and taking the root in $(0,1)$:
> $$\boxed{\ x(\mu)=\tfrac12-\mu+\tfrac12\sqrt{1+4\mu^2}\ }$$
>
> | $\mu$ | $x(\mu)$ | $f=-x(\mu)$ | $f-f^\star$ |
> |---|---|---|---|
> | $1$ | $0.61803399$ | $-0.61803399$ | $0.38196601$ |
> | $0.5$ | $0.70710678$ | $-0.70710678$ | $0.29289322$ |
> | $0.1$ | $0.90990195$ | $-0.90990195$ | $0.09009805$ |
> | $0.01$ | $0.99009999$ | $-0.99009999$ | $0.00990001$ |
> | $0.001$ | $0.99900100$ | $-0.99900100$ | $0.00099900$ |
>
> **Limits** (verified symbolically): $x(\mu)\to\mathbf 1=x^\star$ as $\mu\to0$ ✓, and $x(\mu)\to\tfrac12$ as $\mu\to\infty$ — the **analytic center** of $[0,1]$, the point maximizing $(-g_1)(-g_2)=x(1-x)$ ✓, matching §8 and Luenberger & Ye's remark that the path emanates from the analytic center. *(Amusingly $x(1)=0.618034$ is the golden ratio conjugate, the same constant that ran [[04 - One-Dimensional Search Methods|ch. 04]]'s golden section search — a coincidence of quadratics, not a connection.)*
>
> **The central path runs from $\tfrac12$ to $1$ as $\mu:\infty\to0$**, and an interior-point method follows it, decreasing $\mu$ geometrically and taking a Newton step at each value.
>
> **Comparison with Exercise 3.** Both converge at first order in their parameter — error $\approx\mu$ here, $\approx1/\gamma$ there. The decisive difference is the **side**:
>
> | | penalty (Ex. 3) | barrier (Ex. 4) |
> |---|---|---|
> | iterates | **infeasible**, $x_\gamma<1$ | **strictly feasible**, $0<x(\mu)<1$ |
> | bound on $f^\star$ | lower ($f(x_\gamma)<f^\star$) | upper ($f(x(\mu))>f^\star$) |
> | parameter | $\gamma\to\infty$ | $\mu\to0$ |
> | conditioning | degrades as $\gamma$ | degrades as $1/\mu$ |
>
> Both become ill-conditioned in the limit — $\phi_\mu''(x)=\mu\big(\tfrac1{(1-x)^2}+\tfrac1{x^2}\big)$ blows up as $x\to1$ — which is why practical interior-point methods do **not** solve each subproblem to high accuracy, but take one or two Newton steps per $\mu$ and rely on the path's smoothness. **The choice between them is decided by whether infeasible answers are acceptable**: they are not, if $x$ is a probability, a variance, or a physical capacity.

**5. (Hard — duality gaps, finite and infinite.)** (a) Show that
$$\text{minimize } x^3\quad\text{subject to}\quad x\ge1,\qquad x\in\mathbb R$$
has an **infinite** duality gap. (b) For
$$\text{minimize } -x^2\quad\text{subject to}\quad -1\le x\le1,\qquad x\in\Omega=[-2,2],$$
compute the dual function in closed form and the exact gap. (c) Say precisely which hypothesis of §3 fails in each case, and what convexity would have delivered.

> [!example]- Solution
> **(a)** The feasible set is $[1,\infty)$ and $x^3$ increases there, so $f^\star=1$ at $x^\star=1$. With $g=1-x\le0$ the dual function is
> $$q(\mu)=\inf_{x\in\mathbb R}\big\{x^3+\mu(1-x)\big\}=-\infty\quad\text{for every }\mu\ge0,$$
> because $x^3\to-\infty$ as $x\to-\infty$ and the linear term cannot rescue it. Hence
> $$\sup_{\mu\ge0}q(\mu)=-\infty\ <\ 1=f^\star:\qquad\textbf{an infinite duality gap.}$$
> Verified numerically: $\inf_{[-50,50]}\{x^3+\mu(1-x)\}$ is $-124{,}974.5$, $-124{,}949.0$, $-124{,}898.0$, $-124{,}490.0$ for $\mu=0.5,1,2,10$ — diverging as the interval widens, for every $\mu$.
>
> **Weak duality still holds** ($-\infty\le1$), exactly as [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §12 promised — it holds unconditionally. It is simply **useless**: a dual bound of $-\infty$ tells you nothing.
>
> **(b)** With $g_1=x-1\le0$, $g_2=-x-1\le0$ and $\Omega=[-2,2]$, the true optimum is $f^\star=-1$ at $x=\pm1$. Now
> $$q(\mu_1,\mu_2)=\min_{x\in[-2,2]}\big\{-x^2+(\mu_1-\mu_2)x\big\}-\mu_1-\mu_2 .$$
> The bracketed function is **concave** in $x$, so on an interval its minimum is at an **endpoint**. Writing $c=\mu_1-\mu_2$, the two endpoint values are $-4-2c$ and $-4+2c$, so the minimum is $-4-2|c|$ and
> $$\boxed{\ q(\mu_1,\mu_2)=-4-2|\mu_1-\mu_2|-\mu_1-\mu_2\ }$$
> Every term after $-4$ is $\le0$ for $\boldsymbol\mu\ge\mathbf 0$, so the supremum is attained at $\boldsymbol\mu=\mathbf 0$:
> $$\sup_{\boldsymbol\mu\ge\mathbf 0}q=-4\ <\ -1=f^\star,\qquad\textbf{duality gap}=3 .$$
> Verified against a direct grid minimisation: $q(0,0)=-4$, $q(1,0)=q(0,1)=-7$, $q(0.5,0.5)=-5$, $q(2,2)=-8$ — all matching the closed form exactly.
>
> **The mechanism is visible in the algebra.** Because $-x^2$ is concave, the Lagrangian's minimum jumps to a **vertex of $\Omega$** ($x=\pm2$) rather than sitting where the constraints bite; raising $\boldsymbol\mu$ to punish that only pays the $-\mu_1-\mu_2$ toll without moving the minimiser. So the dual is stuck at the value of the *relaxation*, and the gap measures how far the vertex is from the truth.
>
> **(c) Which hypothesis fails.** §3 requires **$f$ convex, $g_j$ convex, $\Omega$ convex, $\mathbf h$ affine**, plus Slater. In both cases $\Omega$, the constraints and Slater are fine — $x=1.5$ is strictly feasible in (a), $x=0$ in (b). **The failure is convexity of the objective**: $x^3$ is neither convex nor bounded below, and $-x^2$ is strictly *concave*. Correspondingly the **primal function $\omega(y)$ is nonconvex**, so its epigraph has no supporting hyperplane at $y=0$ that reaches the point $(f^\star,\mathbf 0)$, and the shortfall *is* the gap (§3).
>
> **What convexity would have delivered:** zero gap, so $\sup q=f^\star$ exactly; KKT conditions that are **sufficient and global** (§2); and a dual solution that certifies the answer and prices the constraints ([[10 - Duality|ch. 10]] §4, §9). All three are lost together — they are the same theorem.
>
> **Why this matters beyond the exercise.** Lagrangian relaxation is the standard source of bounds in **integer programming** (branch-and-bound) and **nonconvex QP**, and those bounds are loose for exactly this reason. It is also the honest reason a trained neural network comes with **no optimality certificate at all**: the objective is wildly nonconvex, so there is no dual bound to check it against. **"The loss stopped decreasing" is a statement about the algorithm, not about the problem** — and the whole of this chapter's first half is the account of when you may say more.

## 📝 Summary

- **Convexity is the dividing line of the subject.** For $f$ convex on convex $\Omega$: **local minimizers are global**; sublevel sets are convex; and **the set of minimizers is convex** — so a convex program need not have a *unique* solution unless $f$ is strictly convex.
- **First-order conditions become sufficient.** The one line that does it: convexity gives $f(\mathbf x)\ge f(\mathbf x^\star)+Df(\mathbf x^\star)(\mathbf x-\mathbf x^\star)$, promoting a local gradient statement into a global one. Hence **the Lagrange condition and the KKT conditions are sufficient for a global minimizer** — and, being sufficiency theorems, they need **no constraint qualification**.
- **"Convex program" means convex objective, convex inequality constraints, and *affine* equality constraints.** A convex nonlinear $h$ gives a curved $\{\mathbf h=\mathbf 0\}$, which is not convex.
- **The duality gap closes under convexity + Slater.** Via the **primal function** $\omega(\mathbf y)=\inf\{f:\mathbf h=\mathbf y\}$: convexity makes $\omega$ convex, hence supported by a hyperplane at $\mathbf 0$ whose slope is $-\boldsymbol\lambda$ — the same separating-hyperplane argument as [[10 - Duality|ch. 10]] §5, and it needs **no derivatives** ("zero-order conditions").
- **Weak duality always holds; strong duality is the special case.** Gaps are real and can be **infinite** (Exercise 5). This is why Lagrangian relaxation gives *bounds* in integer and nonconvex programming, and why a trained network has no optimality certificate.
- **SDP** minimizes a linear objective under a linear matrix inequality $F(\mathbf x)=F_0+\sum x_iF_i\succeq0$. The feasible set is convex (an intersection of half-spaces over all $\mathbf z$), and $\text{LP}\subset\text{QP}\subset\text{SOCP}\subset\text{SDP}$.
- **Four ways to make an unconstrained algorithm respect constraints:** **project** the iterate back ($\Pi[\mathbf x]=\arg\min_{\mathbf z\in\Omega}\|\mathbf z-\mathbf x\|$, well defined only for closed convex $\Omega$); run **primal–dual** descent-ascent on the Lagrangian; **penalise** infeasibility; or erect a **barrier** on the boundary.
- **For linear equality constraints, $P=I-A^{\mathsf T}(AA^{\mathsf T})^{-1}A$ does everything:** the step is $\mathbf x^{(k+1)}=\mathbf x^{(k)}-\alpha_kP\nabla f(\mathbf x^{(k)})$, feasibility is automatic, $-P\nabla f$ is the steepest *feasible* descent direction, and **the Lagrange condition is exactly $P\nabla f(\mathbf x^\star)=\mathbf 0$** — which doubles as the stopping test.
- **Primal–dual methods are descent in $\mathbf x$, ascent in $\boldsymbol\lambda$** (with $[\cdot]_+$ clipping for $\boldsymbol\mu\ge\mathbf 0$). Fixed points are exactly KKT points; convergence is local and linear, and works because the off-diagonal blocks of $M$ are skew, so $\Re(\mathbf w^HM\mathbf w)=-\Re(\mathbf x^HL\mathbf x)<0$.
- **Penalty methods:** $\min f+\gamma P$ with $P\ge0$ vanishing exactly on $\Omega$. As $\gamma_k\nearrow$: iterates become **more feasible and more expensive**, and $f(\mathbf x^{(k)})\le q(\gamma_k,\mathbf x^{(k)})\le f^\star$ gives **increasing lower bounds**. Error is $O(1/\gamma)$ and **conditioning degrades like $\gamma$** — hence a warm-started sequence, or an augmented Lagrangian.
- **Barrier methods:** $\min f+\mu B$ with $B\to\infty$ at the boundary; the log barrier $-\sum\log(-g_i)$ is standard. Formally constrained but **computationally unconstrained**. The solutions trace the **central path** from the **analytic center** ($\mu\to\infty$) to the optimum ($\mu\to0$); following it is the **interior-point method**, which is polynomial-time and the only practical route for QP/SOCP/SDP.
- **Penalty converges from outside, barrier from inside.** If feasibility is non-negotiable, use a barrier.
- **Beyond the books:** projection is the special case $r=\iota_\Omega$ of the **prox operator**, so **proximal gradient / ISTA / FISTA** handles smooth-plus-nonsmooth (LASSO); **ADMM** splits and parallelises; **mirror descent** matches the geometry; **SQP** solves general NLPs via linearised-constraint QPs. **Pareto fronts** are what ROC and precision–recall curves *are*, and scalarisation provably misses their nonconvex parts.

## ⚠️ Important Notes

1. **Ask "is it convex?" first, every time.** The answer changes what a solver's output *means*: under convexity a KKT point is the global answer; without it, it is a candidate and nothing more. This single question is the most valuable thing in the chapter.
2. **Convex ⟹ local is global, but not ⟹ unique.** Only *strict* convexity gives uniqueness. A linear objective on a polytope typically has a whole face of optima — as [[09 - Linear Programming and the Simplex Method|ch. 09]]'s multiple-optima case showed.
3. **Check the *equality* constraints are affine before calling a problem convex.** $\{h=0\}$ convex essentially requires $h$ affine; $x_1^2+x_2^2=1$ has a perfectly convex $h$ and a thoroughly nonconvex feasible set. Reviewers and solvers both miss this.
4. **Sufficiency theorems need no constraint qualification; necessity theorems do.** Regularity ([[11 - Constrained Optimization - Lagrange and KKT|ch. 11]]) is needed to prove multipliers *exist*. If someone hands you multipliers and the problem is convex, you are done — no regularity check required.
5. **Slater's condition is about *strict* feasibility.** A convex problem whose feasible set has empty interior can have a positive gap. Check for a strictly feasible point, not merely a feasible one.
6. **Weak duality is unconditional; never quote strong duality for a nonconvex problem.** And a dual bound of $-\infty$ is legal, correct, and useless (Exercise 5a).
7. **Projection requires closed convex $\Omega$.** Otherwise $\arg\min_{\mathbf z\in\Omega}\|\mathbf z-\mathbf x\|$ may be non-unique and the projected method is not well posed. This is a genuine restriction, not a technicality.
8. **Projections do not compose.** Projecting onto $\Omega_1$ then $\Omega_2$ is *not* projecting onto $\Omega_1\cap\Omega_2$ (Exercise 2). Projecting onto an intersection is a separate, harder problem — which is why the simplex has its own algorithm and why ADMM exists.
9. **A projection can be as expensive as the original problem.** For $\min\|\mathbf x\|^2$ over $\Omega$ the answer *is* $\Pi[\mathbf 0]$. Projected methods pay off only for the sets in §5's table; check that yours is one of them before designing around them.
10. **Every eigenvector is a fixed point of §5's projected iteration**, so a bad start leaves you stuck for any step size (C&Ż Example 23.1b). This is a nonconvex constraint ($\|\mathbf x\|=1$) doing exactly what nonconvexity does — a warning that "the algorithm stopped" and "the algorithm succeeded" are different claims.
11. **Penalty iterates are infeasible, by $O(1/\gamma)$.** If the constraint is a probability, a variance, a physical capacity, or anything that breaks the model when violated, **use a barrier method.** Do not ship a penalty method's answer as feasible.
12. **Do not jump to a huge $\gamma$ (or tiny $\mu$).** Conditioning degrades like $\gamma$ (or $1/\mu$), so a single aggressive solve is slower *and* less accurate than a warm-started sequence. Interior-point solvers take only one or two Newton steps per $\mu$ for precisely this reason.
13. **Prefer an augmented Lagrangian to a pure penalty** when accuracy matters: keeping $\boldsymbol\lambda$ in the objective means $\gamma$ need not diverge, so the ill-conditioning of Note 12 never arrives.
14. **Descent in $\mathbf x$, ascent in $\boldsymbol\lambda$ — never descent in both.** The Lagrangian is linear in its multipliers and has a saddle point, not a minimum, at the solution ([[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] §5). Getting this backwards diverges immediately, and it is the structural reason min–max training in ML is delicate.
15. **For a smooth loss plus an $\ell_1$ penalty, reach for FISTA, not a generic NLP solver.** Proximal gradient exploits structure a general method cannot see, and the prox of $\lambda\|\cdot\|_1$ is one line of soft-thresholding. This is the most immediately useful algorithm in the chapter and appears in none of the four source books.
16. **Every ROC curve is a Pareto front.** No point on it is "optimal"; choosing a threshold is choosing a trade-off, and the absence of a single best answer is a theorem. Be suspicious of any scalarisation (a single weighted score) that hides the choice — and remember it **provably cannot reach nonconvex parts of the front.**
17. **The two questions worth asking about any optimization problem you meet:** *is it convex?* and *what does the dual say?* The first tells you whether an answer is trustworthy; the second certifies it and prices every constraint. Between them they are most of what these twelve chapters were for.

> [!warning] Gaps in the source material
> **A genuine error found in Chong & Żak.** **Example 23.3(c)** states "$\lambda_\gamma=2\gamma(1-\|\mathbf x_\gamma\|^2)\le\lambda_{\max}$, hence $\|\mathbf x_\gamma\|^2-1=-\lambda_{\max}/(2\gamma)=O(1/\gamma)$." The **bound** is correct but the **equality is wrong** — the correct value is $-\lambda_\gamma/(2\gamma)$, and for a *minimization* problem $\lambda_\gamma\to\lambda_{\min}$, not $\lambda_{\max}$. Verified numerically with $Q=\operatorname{tridiag}(1,3,1)$: at $\gamma=10^4$ the true infeasibility is $-7.929\times10^{-5}=-\lambda_{\min}/(2\gamma)$, whereas the book's expression gives $-2.207\times10^{-4}$ — **wrong by the factor $\lambda_{\max}/\lambda_{\min}=2.78$, i.e. by the condition number, so the discrepancy is unbounded across problems.** Only the $O(1/\gamma)$ conclusion survives. Added to the errata table in `00-Index.md`. §7's version of the example states the corrected form and shows the numbers.
> **Extraction damage.** The scanned OCR substitutions of `../CLAUDE.md` apply throughout, and **all matrices again lose their bracket and row structure**. Chapter 23's algorithm displays are the worst affected: the update equations of §23.4 extract with **the $\boldsymbol\lambda$-update line missing entirely** (the text runs "the update equation for is a gradient algorithm for maximizing"), and were reconstructed from the surrounding prose plus the derivative $DU(\mathbf w)=I+\alpha M$ that survives two pages later. Example 23.1's eigenvector expansion extracts with corrupted superscripts throughout ($y_1^{(k)}$ as `y[k)`, `»ί0)`) and was re-derived. **Every reconstruction in this chapter was checked by reproducing the book's own printed conclusion.**
> **Figures lost.** All are images: Figure 23.1 ($g^+$ for the absolute-value penalty), and Luenberger & Ye's Figures 13.2 (robust vs non-robust sets — the entire justification of the robustness hypothesis in §8), 13.3 (the barrier function) and 11.6 (the primal function, which is the whole picture behind §3's separating-hyperplane argument). §§3, 7 and 8 give the algebra and describe the geometry in words; **the pictures are not reconstructed.** Chong & Żak §22.4's semidefinite-programming examples are also heavily matrix-based and largely unreadable, which is one reason §4 is a short survey rather than a worked treatment.
> **Verification performed.** Every numeric claim recomputed before writing. C&Ż Ex 22.7 (bank account: `linprog` gives $\mathbf x^\star=(1000,0,0,0)$, value $1215.50625$ at $r=0.05,n=4,D=1000$; $\boldsymbol\mu^{(2)}=(0,0.057881,0.113006,0.165506)\ge\mathbf 0$; $\boldsymbol\mu^{(2)\mathsf T}\mathbf x^\star=0$); Ex 23.1 (projected gradient with $\alpha=0.9/\lambda_{\max}$ converges to $\pm(0.5,0.707107,0.5)$ with $\mathbf x^{\mathsf T}Q\mathbf x=\lambda_{\min}=1.58578644$, and holds $\lambda_{\max}=4.4142135624$ for every iteration when started at the top eigenvector); Ex 23.3 (the four-row table in §7). All five exercises verified — Exercises 3 and 4 symbolically with `sympy` (including both limits of the central path, $x\to1$ and $x\to\tfrac12$), Exercise 5 by closed form **and** independent grid minimisation over $[-2,2]$ agreeing at five test multipliers. **No error was found in Chong & Żak ch. 22 or in Luenberger & Ye ch. 12–13**; the single defect is Example 23.3(c) above.
> **Additions beyond all four sources.** §5's **table of projections onto common sets** (only the box case is in the books). §9 **in its entirety**: proximal gradient, ISTA/FISTA, soft-thresholding, the observation that projection is the prox of an indicator function, ADMM, mirror descent, the SQP framing of C&Ż §20.6's closed form, and the final "what to reach for" table. The **SDP-as-relaxation** framing in §4 (Max-Cut, nuclear norm, Lovász theta) — Chong & Żak present LMIs purely as a control-theory device. §3's **summary table of problem classes** and the explicit statement of **Slater's condition**, which neither book states in this form. §7's and §8's **conditioning warnings** and the penalty-versus-barrier comparison. The **ROC/precision–recall curves as Pareto fronts** identification in §9, and the ML readings throughout (§6's connection to TRPO/RLHF and GANs). Exercise 5's finite-gap construction is my own.
> **Deliberately summarised rather than covered.** **C&Ż ch. 14** (global search heuristics), **ch. 18–19** (Khachiyan, Karmarkar, integer LP), **ch. 24** (multiobjective optimization) and **L&Y ch. 5–6** (interior-point theory, conic programming) are compressed into §§8–9 as promised in `00-Index.md`, with reasons recorded there. **L&Y §§12.2–12.7** (feasible direction, active set and reduced gradient methods, with convergence rates) are omitted: active-set methods are described in [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] Exercise 3's closing remark, and the reduced-gradient method is a variable-elimination variant of §5's projected gradient. **C&Ż §23.4's full convergence proofs** are given in outline only — the four-claim induction for the inequality-constrained case runs three pages and its structure, not its bookkeeping, is what matters. **Léonard & Long remains unreadable** (no text layer), so optimal control is absent from the whole subject; **flag this to the lecturer if the course covers it.**

**Previous:** [[11 - Constrained Optimization - Lagrange and KKT]] · **Next:** [[00-Index|back to the index]]
