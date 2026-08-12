---
subject: Optimization
chapter: 11
tags: [ds, optimization, lagrange-multipliers, kkt, constrained-optimization, tangent-space, sensitivity, maximum-entropy]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 20–21; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 11"
---

# Constrained Optimization: Lagrange and KKT

[[03 - Unconstrained Optimality Conditions|Chapter 03]] characterised minimizers of an unconstrained function: $\nabla f(\mathbf x^\star)=\mathbf 0$, plus a condition on the Hessian. [[09 - Linear Programming and the Simplex Method|Chapters 09]]–[[10 - Duality|10]] characterised minimizers of a *linear* function over a *linear* feasible set. This chapter closes the gap: **a nonlinear objective over a nonlinear feasible set.**

The obstacle is easy to state. At a constrained minimizer, $\nabla f(\mathbf x^\star)$ is essentially never zero — you have stopped not because the ground is flat but because a wall is in the way. Chapter 03's condition is simply false here, and something must replace it.

The replacement is one of the most reused ideas in applied mathematics. It says: **at a constrained minimizer, the gradient of the objective must be a combination of the gradients of the constraints.** Push in any direction the constraints allow, and $f$ cannot decrease — which forces $\nabla f$ to lie entirely in the directions the constraints forbid. The coefficients of that combination are the **Lagrange multipliers**, and — as [[10 - Duality|ch. 10]] should make you suspect — they turn out to be prices.

## 📘 Main Knowledge

### 1. The problem, and why chapter 03's conditions fail

The general nonlinear program:

$$\begin{aligned}\text{minimize }\quad & f(\mathbf x)\\ \text{subject to }\quad & \mathbf h(\mathbf x)=\mathbf 0 && (m\text{ equality constraints})\\ & \mathbf g(\mathbf x)\le\mathbf 0 && (p\text{ inequality constraints})\end{aligned}$$

with $f:\mathbb R^n\to\mathbb R$, $\mathbf h:\mathbb R^n\to\mathbb R^m$, $\mathbf g:\mathbb R^n\to\mathbb R^p$, and $m<n$. Any point satisfying all constraints is **feasible**; the set of all of them is the **feasible set**. Maximization needs no separate treatment, since $\max f=-\min(-f)$.

**Everything so far is a special case.** Linear programming is $f=\mathbf c^{\mathsf T}\mathbf x$, $\mathbf h=A\mathbf x-\mathbf b$, $\mathbf g=-\mathbf x$. [[08 - Least Squares and Linear Equations|Least squares with a norm constraint]], the [[02 - Convex Sets and Convex Functions|convex programs]] of ch. 02, and every regularised model in machine learning live in this form too.

Why chapter 03 does not apply, concretely. Consider

$$\text{minimize } (x_1-1)^2+x_2-2 \quad\text{subject to}\quad x_2-x_1=1,\ \ x_1+x_2\le2 .$$

Substituting the equality gives $f=x_1^2-x_1$ on the feasible segment $x_1\le\tfrac12$, minimized at $x_1=\tfrac12$ with value $-\tfrac14$, so $\mathbf x^\star=\left(\tfrac12,\tfrac32\right)$. But $\nabla f(\mathbf x^\star)=(2x_1-2,1)\big|_{\mathbf x^\star}=(-1,1)\ne\mathbf 0$. **Chapter 03's first-order condition is violated at the true minimizer.** It is not a weaker condition here; it is the wrong condition. (This is Chong & Żak's Example 20.1, and §8 solves it properly.)

The reason is that chapter 03's proof needed *every* direction to be available, so that $\nabla f\ne\mathbf 0$ would give a descent direction $-\nabla f$ you could actually follow. Under constraints most directions are unavailable. **So the first job is to say exactly which directions remain** — and that is a question about the geometry of the feasible set.

### 2. The geometry of a constraint surface

Take equality constraints only for now, and let

$$S=\{\mathbf x\in\mathbb R^n:\mathbf h(\mathbf x)=\mathbf 0\},\qquad \mathbf h\in C^1 .$$

$S$ is a **surface** in $\mathbb R^n$. Each of the $m$ equations removes one degree of freedom, so we expect $\dim S=n-m$ — but only if the constraints are genuinely independent, which is what the next definition demands.

> [!note] Definition — regular point
> A feasible $\mathbf x^\star$ is a **regular point** of the constraints if the gradients $\nabla h_1(\mathbf x^\star),\dots,\nabla h_m(\mathbf x^\star)$ are **linearly independent** — equivalently, if the Jacobian
> $$D\mathbf h(\mathbf x^\star)=\begin{bmatrix}\nabla h_1(\mathbf x^\star)^{\mathsf T}\\ \vdots\\ \nabla h_m(\mathbf x^\star)^{\mathsf T}\end{bmatrix}\in\mathbb R^{m\times n} \quad\text{has full rank }m.$$

Now the two subspaces that do all the work. Both are objects from [[05 - Gradient Methods|Linear Algebra ch. 05]] attached to the Jacobian.

> [!note] Definition — tangent and normal spaces
> $$T(\mathbf x^\star)=\{\mathbf y:D\mathbf h(\mathbf x^\star)\mathbf y=\mathbf 0\}=\mathcal N\big(D\mathbf h(\mathbf x^\star)\big) \qquad\text{(the \textbf{tangent space})}$$
> $$N(\mathbf x^\star)=\{D\mathbf h(\mathbf x^\star)^{\mathsf T}\mathbf z:\mathbf z\in\mathbb R^m\}=\mathcal R\big(D\mathbf h(\mathbf x^\star)^{\mathsf T}\big)=\operatorname{span}\big[\nabla h_1(\mathbf x^\star),\dots,\nabla h_m(\mathbf x^\star)\big] \quad\text{(the \textbf{normal space})}$$

So $T$ is the **nullspace** of the Jacobian and $N$ is the **row space** — and those are orthogonal complements, which is the whole reason this machinery works:

**Lemma.** $T(\mathbf x^\star)=N(\mathbf x^\star)^\perp$ and $T(\mathbf x^\star)^\perp=N(\mathbf x^\star)$, hence $\mathbb R^n=N(\mathbf x^\star)\oplus T(\mathbf x^\star)$: **every direction splits uniquely into a tangential part and a normal part.**

At a regular point $\dim T=n-m$ and $\dim N=m$. Both pass through the origin, being subspaces; when drawing pictures one shifts them to $\mathbf x^\star$ and calls the results the tangent and normal **planes**, $T(\mathbf x^\star)+\mathbf x^\star$ and $N(\mathbf x^\star)+\mathbf x^\star$.

**Why $T$ deserves the name "tangent".** Define a **curve** on $S$ as a continuously parameterised family $\{\mathbf x(t)\in S:t\in(a,b)\}$; it is differentiable if $\dot{\mathbf x}(t)$ exists, and $\dot{\mathbf x}(t^\star)$ is the velocity — geometrically, a vector tangent to the curve at $\mathbf x(t^\star)$.

**Theorem.** *If $\mathbf x^\star\in S$ is regular, then $\mathbf y\in T(\mathbf x^\star)$ **if and only if** there is a differentiable curve in $S$ through $\mathbf x^\star$ with derivative $\mathbf y$ there.*

*Proof (⟸, the easy and useful direction).* If $\mathbf x(t)\in S$ for all $t$ then $\mathbf h(\mathbf x(t))=\mathbf 0$ identically; differentiating with the chain rule gives $D\mathbf h(\mathbf x(t))\dot{\mathbf x}(t)=\mathbf 0$, so at $t^\star$, $D\mathbf h(\mathbf x^\star)\mathbf y=\mathbf 0$, i.e. $\mathbf y\in T(\mathbf x^\star)$. $\blacksquare$

The converse — that *every* $\mathbf y\in T$ is realised by an actual curve — needs the **implicit function theorem**, and **this is exactly where regularity is used**. Both books cite the proof rather than giving it.

> [!note] The whole point in one sentence
> $T(\mathbf x^\star)$ is the linearised set of directions you may move in without immediately leaving the feasible set. It replaces "all of $\mathbb R^n$" from [[03 - Unconstrained Optimality Conditions|ch. 03]], and every condition below is chapter 03's condition **restricted to $T$**.

> [!example]- Worked example — computing $T$ and $N$ (C&Ż Example 20.4)
> Let $S=\{\mathbf x\in\mathbb R^3:h_1=x_1=0,\ h_2=x_1-x_2=0\}$, which is the **$x_3$-axis**. Then
> $$D\mathbf h(\mathbf x)=\begin{bmatrix}\nabla h_1^{\mathsf T}\\ \nabla h_2^{\mathsf T}\end{bmatrix}=\begin{bmatrix}1&0&0\\1&-1&0\end{bmatrix},$$
> whose rows are independent at every $\mathbf x$, so **all points of $S$ are regular.** Then
> $$T(\mathbf x)=\{\mathbf y:y_1=0,\ y_1-y_2=0\}=\{(0,0,a)^{\mathsf T}:a\in\mathbb R\}$$
> — the $x_3$-axis, of dimension $n-m=3-2=1$ ✓ — and
> $$N(\mathbf x)=\operatorname{span}\big[(1,0,0),\,(1,-1,0)\big]=\text{the }x_1x_2\text{-plane},$$
> of dimension $m=2$. Every vector in $T$ is orthogonal to every vector in $N$, and $T\oplus N=\mathbb R^3$ ✓. Here the surface, its tangent space and the $x_3$-axis all coincide because the constraints are linear; for curved constraints (e.g. C&Ż Example 20.2's $h=x_2-x_3^2$) $T$ is only the *linearisation* of $S$ at the point.
>
> **Regularity depends on how you write the constraints, not just on the set they define.** The same $x_3$-axis is cut out by $h_1=x_1^2=0$, $h_2=(x_1-x_2)^2=0$ — but now $\nabla h_1=(2x_1,0,0)=\mathbf 0$ everywhere on $S$, so **no point of $S$ is regular** and none of this chapter's theorems apply. Nothing about the geometry changed; only the algebra did. Exercise 4 shows what goes wrong when you ignore this.

### 3. The Lagrange condition

**Start with $n=2$, $m=1$**, where the whole theorem is visible. Let $h:\mathbb R^2\to\mathbb R$ and let $\mathbf x^\star$ minimize $f$ on the curve $\{h=0\}$, parameterised near $\mathbf x^\star$ by $\mathbf x(t)$ with $\mathbf x(t^\star)=\mathbf x^\star$.

**Two orthogonality facts, both by the chain rule.**
1. $h$ is constant on the curve, so $\tfrac{d}{dt}h(\mathbf x(t))=\nabla h(\mathbf x(t))^{\mathsf T}\dot{\mathbf x}(t)=0$: **$\nabla h(\mathbf x^\star)\perp\dot{\mathbf x}(t^\star)$.**
2. $\phi(t)=f(\mathbf x(t))$ has an unconstrained minimum at $t^\star$, so $\phi'(t^\star)=\nabla f(\mathbf x^\star)^{\mathsf T}\dot{\mathbf x}(t^\star)=0$: **$\nabla f(\mathbf x^\star)\perp\dot{\mathbf x}(t^\star)$.**

In $\mathbb R^2$ the orthogonal complement of a nonzero vector is one-dimensional, so **$\nabla f(\mathbf x^\star)$ and $\nabla h(\mathbf x^\star)$ are parallel.** If $\nabla h(\mathbf x^\star)\ne\mathbf 0$ there is a scalar $\lambda^\star$ with

$$\nabla f(\mathbf x^\star)+\lambda^\star\nabla h(\mathbf x^\star)=\mathbf 0 .$$

Note that step 2 used only that $t^\star$ is a *local extremum*, so **the same conclusion holds at maximizers.** The general statement:

> [!note] Theorem (Lagrange)
> Let $\mathbf x^\star$ be a local minimizer (or maximizer) of $f$ subject to $\mathbf h(\mathbf x)=\mathbf 0$, with $m<n$, and let $\mathbf x^\star$ be a **regular** point. Then there exists $\boldsymbol\lambda^\star\in\mathbb R^m$ with
> $$Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)=\mathbf 0^{\mathsf T}, \qquad\text{i.e.}\qquad \nabla f(\mathbf x^\star)=-\sum_{i=1}^m\lambda_i^\star\nabla h_i(\mathbf x^\star).$$

*Proof.* The claim is $\nabla f(\mathbf x^\star)\in\mathcal R(D\mathbf h(\mathbf x^\star)^{\mathsf T})=N(\mathbf x^\star)$, and by the Lemma of §2, $N=T^\perp$, so it suffices to show $\nabla f(\mathbf x^\star)\perp T(\mathbf x^\star)$. Take any $\mathbf y\in T(\mathbf x^\star)$. By the theorem of §2 (**regularity used here**) there is a differentiable curve on $S$ with $\mathbf x(t^\star)=\mathbf x^\star$, $\dot{\mathbf x}(t^\star)=\mathbf y$. Then $\phi(t)=f(\mathbf x(t))$ has a local minimum at $t^\star$, so by [[03 - Unconstrained Optimality Conditions|ch. 03]]'s first-order condition $\phi'(t^\star)=0$, and the chain rule gives $\nabla f(\mathbf x^\star)^{\mathsf T}\mathbf y=0$. As $\mathbf y\in T$ was arbitrary, $\nabla f(\mathbf x^\star)\in T(\mathbf x^\star)^\perp=N(\mathbf x^\star)$. $\blacksquare$

**So the compact form of the necessary condition is $\nabla f(\mathbf x^\star)\in N(\mathbf x^\star)$.** If $\nabla f$ has any component inside $T$, that component is a feasible descent (or ascent) direction and $\mathbf x^\star$ cannot be an extremizer.

The **Lagrange condition** used in practice is the pair

$$\nabla f(\mathbf x^\star)+D\mathbf h(\mathbf x^\star)^{\mathsf T}\boldsymbol\lambda^\star=\mathbf 0,\qquad \mathbf h(\mathbf x^\star)=\mathbf 0,$$

which is $n+m$ equations in the $n+m$ unknowns $(\mathbf x^\star,\boldsymbol\lambda^\star)$ — a determined system, which is why the method is usable.

> [!warning] Necessary, not sufficient
> Points satisfying the Lagrange condition are **candidates**. Chong & Żak's Figure 20.12 shows four configurations satisfying it: a maximizer, two minimizers, and **a point that is neither**. Always classify afterwards — by §6's second-order conditions, by comparing values across candidates, or by a convexity argument.

### 4. Regularity is not a technicality

Drop regularity and the theorem is simply false. Chong & Żak's Example 20.5: minimize $f(x)=x$ subject to

$$h(x)=\begin{cases}x^2 & x<0\\ 0 & 0\le x\le1\\ (x-1)^2 & x>1.\end{cases}$$

The feasible set is $[0,1]$ and $x^\star=0$ is clearly the minimizer. But $f'(x^\star)=1$ and $h'(x^\star)=0$, so **no $\lambda$ whatsoever satisfies $f'+\lambda h'=0$.** The Lagrange condition fails at the true minimizer — because $\nabla h(x^\star)=0$ makes $x^\star$ irregular, and the theorem does not apply.

The mechanism is always the same: **when $\nabla h$ degenerates, the normal space $N$ collapses** and stops being large enough to contain $\nabla f$. Constraint qualifications (regularity here; Slater's condition in [[12 - Convex Programming and Constrained Algorithms|ch. 12]]) exist exactly to rule this out. Exercise 4 constructs the standard cusp example.

### 5. The Lagrangian: the condition *is* unconstrained stationarity

Define the **Lagrangian** $l:\mathbb R^n\times\mathbb R^m\to\mathbb R$,

$$\boxed{\ l(\mathbf x,\boldsymbol\lambda)=f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf h(\mathbf x)\ }$$

and differentiate with respect to the **whole** argument $(\mathbf x,\boldsymbol\lambda)$:

$$D_{\mathbf x}l(\mathbf x,\boldsymbol\lambda)=Df(\mathbf x)+\boldsymbol\lambda^{\mathsf T}D\mathbf h(\mathbf x),\qquad D_{\boldsymbol\lambda}l(\mathbf x,\boldsymbol\lambda)=\mathbf h(\mathbf x)^{\mathsf T}.$$

Setting both to zero recovers *exactly* the Lagrange condition — stationarity from the $\mathbf x$-block, feasibility from the $\boldsymbol\lambda$-block. So

$$Dl(\mathbf x^\star,\boldsymbol\lambda^\star)=\mathbf 0^{\mathsf T}.$$

**The constrained first-order condition for $f$ is the unconstrained first-order condition for $l$.** That is why the Lagrangian is worth introducing rather than just remembering the formula: it converts a constrained problem in $n$ variables into an unconstrained stationarity problem in $n+m$, letting all of chapters 03–07 be reused.

> [!warning] $(\mathbf x^\star,\boldsymbol\lambda^\star)$ is a saddle point, not a minimum, of $l$
> It is stationary in $(\mathbf x,\boldsymbol\lambda)$ jointly, but $l$ is *linear* in $\boldsymbol\lambda$, so it can never have a genuine minimum there — pushing $\boldsymbol\lambda$ along any direction with $\boldsymbol\lambda^{\mathsf T}\mathbf h\ne0$ decreases $l$ without bound. **Never hand a Lagrangian to a minimizer and expect it to work.** This is precisely why constrained algorithms ([[12 - Convex Programming and Constrained Algorithms|ch. 12]]) use penalty, barrier, or primal–dual schemes instead of naively minimizing $l$ — and, in ML, why GAN-style min–max training is hard for the same structural reason.

### 6. Second-order conditions

Assume $f,\mathbf h\in C^2$ and let $L(\mathbf x,\boldsymbol\lambda)$ be the **Hessian of the Lagrangian with respect to $\mathbf x$**:

$$L(\mathbf x,\boldsymbol\lambda)=F(\mathbf x)+[\boldsymbol\lambda H(\mathbf x)],\qquad [\boldsymbol\lambda H(\mathbf x)]:=\lambda_1H_1(\mathbf x)+\cdots+\lambda_mH_m(\mathbf x),$$

with $F$ the Hessian of $f$ and $H_k$ the Hessian of $h_k$.

> [!note] Second-order necessary conditions (SONC)
> If $\mathbf x^\star$ is a regular local minimizer, there is $\boldsymbol\lambda^\star$ with
> 1. $Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)=\mathbf 0^{\mathsf T}$, and
> 2. $\mathbf y^{\mathsf T}L(\mathbf x^\star,\boldsymbol\lambda^\star)\mathbf y\ge0$ **for all $\mathbf y\in T(\mathbf x^\star)$.**

> [!note] Second-order sufficient conditions (SOSC)
> If $f,\mathbf h\in C^2$ and there are $\mathbf x^\star,\boldsymbol\lambda^\star$ with
> 1. $Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)=\mathbf 0^{\mathsf T}$, and
> 2. $\mathbf y^{\mathsf T}L(\mathbf x^\star,\boldsymbol\lambda^\star)\mathbf y>0$ **for all $\mathbf y\in T(\mathbf x^\star)$, $\mathbf y\ne\mathbf 0$**,
>
> then $\mathbf x^\star$ is a **strict** local minimizer. (For a maximizer: $L$ negative definite on $T$.)

*Sketch of the SONC proof, because the trick is instructive.* Take $\mathbf y\in T$ and a twice-differentiable curve realising it. Then $t^\star$ minimizes $\phi(t)=f(\mathbf x(t))$, so $\phi''(t^\star)\ge0$, which by the chain rule reads $\mathbf y^{\mathsf T}F(\mathbf x^\star)\mathbf y+Df(\mathbf x^\star)\ddot{\mathbf x}(t^\star)\ge0$. **The unwanted $\ddot{\mathbf x}$ term is removed by differentiating the constraint twice**: $\boldsymbol\lambda^{\star\mathsf T}\mathbf h(\mathbf x(t))\equiv0$ gives $\mathbf y^{\mathsf T}[\boldsymbol\lambda^\star H(\mathbf x^\star)]\mathbf y+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)\ddot{\mathbf x}(t^\star)=0$. Add the two; the $\ddot{\mathbf x}$ terms combine into $\big(Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)\big)\ddot{\mathbf x}(t^\star)$, which is **zero by the Lagrange condition**. What survives is $\mathbf y^{\mathsf T}L\mathbf y\ge0$. $\blacksquare$

**Two things to notice.** First, $L$ plays exactly the role $F$ played in [[03 - Unconstrained Optimality Conditions|ch. 03]] — **but the constraint curvature enters**, via $[\boldsymbol\lambda H]$. Curved constraints change the second-order test even when $f$ is a perfect quadratic. Second, definiteness is required **only on $T$**, not on $\mathbb R^n$: $L$ may be indefinite on $\mathbb R^n$ and still certify a strict local minimizer. §8's worked example has $L$ merely positive *semi*definite on $\mathbb R^2$ and positive definite on $T$.

**How to test "positive definite on a subspace" in practice.** Two routes:
- **Basis reduction.** Build a matrix $E$ whose columns are a basis of $T$ (e.g. from a QR or SVD of $D\mathbf h$, [[08 - Least Squares and Linear Equations|ch. 08]]) and test the $(n-m)\times(n-m)$ matrix $E^{\mathsf T}LE$ by the usual eigenvalue or leading-minor tests. Cheapest and most direct.
- **Projected Hessian test** (Luenberger & Ye §11.6). With $A=D\mathbf h$ of full row rank, let $P_A=I-A^{\mathsf T}(AA^{\mathsf T})^{-1}A$ be the orthogonal projector onto $\mathcal N(A)$ — **the same projector as [[08 - Least Squares and Linear Equations|ch. 08]]'s hat matrix, complemented.** Then: *$L$ is positive definite on $T$ if and only if $P_ALP_A$ is positive semidefinite and has rank $n-m$.* No basis needed, but you work with $n\times n$ matrices. Note the two-part conclusion — semidefiniteness alone is not enough, because $P_ALP_A$ is *always* singular on $N$.

### 7. The generalized eigenvalue problem — where PCA comes from

This is the most reusable worked example in the chapter, so it gets its own section.

Consider maximizing a **Rayleigh quotient** with $Q=Q^{\mathsf T}>0$ and $P=P^{\mathsf T}>0$:

$$\text{maximize }\ \frac{\mathbf x^{\mathsf T}Q\mathbf x}{\mathbf x^{\mathsf T}P\mathbf x}.$$

The objective is **scale-invariant** — replacing $\mathbf x$ by $t\mathbf x$ cancels $t^2$ top and bottom — so solutions come in whole rays and the problem as posed has no isolated maximizer. Normalise by imposing $\mathbf x^{\mathsf T}P\mathbf x=1$:

$$\text{maximize } \mathbf x^{\mathsf T}Q\mathbf x \quad\text{subject to}\quad \mathbf x^{\mathsf T}P\mathbf x=1 .$$

With $f=\mathbf x^{\mathsf T}Q\mathbf x$ and $h=1-\mathbf x^{\mathsf T}P\mathbf x$, the Lagrangian is $l=\mathbf x^{\mathsf T}Q\mathbf x+\lambda(1-\mathbf x^{\mathsf T}P\mathbf x)$ and stationarity gives $2\mathbf x^{\mathsf T}Q-2\lambda\mathbf x^{\mathsf T}P=\mathbf 0^{\mathsf T}$, i.e.

$$Q\mathbf x=\lambda P\mathbf x \qquad\Longleftrightarrow\qquad P^{-1}Q\mathbf x=\lambda\mathbf x .$$

**The Lagrange condition is a generalized eigenvalue problem.** Every candidate is an eigenvector of $P^{-1}Q$, and its multiplier is the corresponding eigenvalue. Moreover, using the constraint,

$$\lambda^\star=\lambda^\star\,\mathbf x^{\star\mathsf T}P\mathbf x^\star=\mathbf x^{\star\mathsf T}Q\mathbf x^\star=\text{the objective value},$$

so **the multiplier *is* the optimal value**, and the maximum is the largest generalized eigenvalue.

> [!example]- Verified instance (Chong & Żak Examples 20.8–20.9)
> $Q=\begin{bmatrix}4&0\\0&1\end{bmatrix}$, $P=\begin{bmatrix}2&0\\0&1\end{bmatrix}$, so $P^{-1}Q=\begin{bmatrix}2&0\\0&1\end{bmatrix}$ with eigenvalues $\{2,1\}$. The maximum is $\lambda^\star=2$, attained at the eigenvector for $2$ normalised so $\mathbf x^{\mathsf T}P\mathbf x=1$: $2x_1^2=1$, so $\mathbf x^\star=\pm\left(\tfrac1{\sqrt2},0\right)$. Ratio check: $\mathbf x^{\star\mathsf T}Q\mathbf x^\star/\mathbf x^{\star\mathsf T}P\mathbf x^\star=2/1=2$ ✓.
>
> **Second-order check.** $L(\mathbf x^\star,\lambda^\star)=2Q-2\lambda^\star P=\begin{bmatrix}0&0\\0&-2\end{bmatrix}$, and
> $$T(\mathbf x^\star)=\{\mathbf y:\mathbf x^{\star\mathsf T}P\mathbf y=0\}=\{\mathbf y:(\sqrt2,0)\mathbf y=0\}=\{(0,a)^{\mathsf T}\},$$
> giving $\mathbf y^{\mathsf T}L\mathbf y=-2a^2<0$ for $\mathbf y\ne\mathbf 0$: **negative definite on $T$**, so $\pm\mathbf x^\star$ are strict local maximizers. Note $L$ is only negative *semi*definite on $\mathbb R^2$ — the restriction to $T$ is doing real work. Every value verified numerically.

**Why this matters far beyond this chapter.** Set $P=I$ and $Q=$ the sample covariance matrix: you have just derived **PCA** — the first principal direction is the unit vector maximizing explained variance, hence the top eigenvector of the covariance matrix, with the multiplier equal to the variance explained ([[08 - Least Squares and Linear Equations|Linear Algebra ch. 08]] §10 derives the same result from the spectral theorem). Keep $P$ general and you have **Fisher's linear discriminant** ($Q$ = between-class scatter, $P$ = within-class scatter), **canonical correlation analysis**, and the **spectral clustering** relaxation. All are one Lagrange condition.

### 8. Inequality constraints: the KKT conditions

Now restore $\mathbf g(\mathbf x)\le\mathbf 0$. The single new idea is that **an inequality constraint either matters or it does not.**

> [!note] Definitions — active set, regularity
> $g_j(\mathbf x)\le0$ is **active** at $\mathbf x^\star$ if $g_j(\mathbf x^\star)=0$, and **inactive** if $g_j(\mathbf x^\star)<0$. Equality constraints are active by convention. Let $J(\mathbf x^\star)=\{j:g_j(\mathbf x^\star)=0\}$ be the **active index set**. Then $\mathbf x^\star$ is a **regular point** if
> $$\nabla h_i(\mathbf x^\star)\ (1\le i\le m)\quad\text{and}\quad \nabla g_j(\mathbf x^\star)\ (j\in J(\mathbf x^\star))$$
> are linearly independent. **Only active inequality constraints count** towards regularity.

An inactive constraint has slack around it, so locally it might as well not exist — a small move in any direction keeps it satisfied. An active constraint behaves like an equality, **but only in one direction**: you may move off it into the interior, but not through it. That asymmetry is the entire difference between Lagrange and KKT, and it shows up as a **sign condition on the multiplier**.

> [!note] Theorem (Karush–Kuhn–Tucker)
> Let $f,\mathbf h,\mathbf g\in C^1$ and let $\mathbf x^\star$ be a **regular** local minimizer of $f$ subject to $\mathbf h(\mathbf x)=\mathbf 0$, $\mathbf g(\mathbf x)\le\mathbf 0$. Then there exist $\boldsymbol\lambda^\star\in\mathbb R^m$ and $\boldsymbol\mu^\star\in\mathbb R^p$ such that
>
> | | condition | name |
> |---|---|---|
> | 1 | $\boldsymbol\mu^\star\ge\mathbf 0$ | **dual feasibility** |
> | 2 | $Df(\mathbf x^\star)+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h(\mathbf x^\star)+\boldsymbol\mu^{\star\mathsf T}D\mathbf g(\mathbf x^\star)=\mathbf 0^{\mathsf T}$ | **stationarity** |
> | 3 | $\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0$ | **complementary slackness** |
> | 4 | $\mathbf h(\mathbf x^\star)=\mathbf 0$ | primal feasibility |
> | 5 | $\mathbf g(\mathbf x^\star)\le\mathbf 0$ | primal feasibility |

**Compare that table with [[10 - Duality|ch. 10]].** Three of the four names were introduced there, in the linear case, and they mean the same things. Condition 3 unpacks componentwise exactly as it did: since $\mu_j^\star\ge0$ and $g_j(\mathbf x^\star)\le0$, every term of the sum $\sum_j\mu_j^\star g_j(\mathbf x^\star)$ is $\le0$, so the sum vanishing forces each term to vanish:

$$g_j(\mathbf x^\star)<0\ \Longrightarrow\ \mu_j^\star=0 \qquad\text{i.e.}\qquad \textbf{inactive constraints have zero multiplier.}$$

Active constraints may have $\mu_j^\star>0$ or $\mu_j^\star=0$ (the **degenerate** case — same phenomenon as ch. 10's tight-but-unpriced constraint).

*Proof sketch.* If $\mathbf x^\star$ is a regular local minimizer of the original problem, it is also one of the problem with the *active* constraints imposed as **equalities** — the inactive ones cannot bind locally. Lagrange's theorem then supplies $\boldsymbol\lambda^\star,\boldsymbol\mu^\star$ satisfying stationarity, with $\mu_j^\star=0$ off the active set. **Only $\boldsymbol\mu^\star\ge\mathbf 0$ remains**, and it is proved by contradiction: if some active $\mu_j^\star<0$, regularity provides $\mathbf y$ in the tangent space of *all the other* active constraints with $Dg_j(\mathbf x^\star)\mathbf y<0$. Postmultiplying stationarity by $\mathbf y$ leaves $Df(\mathbf x^\star)\mathbf y=-\mu_j^\star Dg_j(\mathbf x^\star)\mathbf y<0$. Following a curve with that velocity keeps $g_j<0$ (feasible, since we are moving *into* the region) while strictly decreasing $f$ — contradicting minimality. $\blacksquare$

**The sign condition is the geometry of one-sided constraints.** At the minimizer $\nabla f(\mathbf x^\star)=-\sum_{j\in J}\mu_j^\star\nabla g_j(\mathbf x^\star)$ with $\mu_j^\star\ge0$: since each $\nabla g_j$ points *out* of the feasible region, $\nabla f$ must point *into* it. Descent directions all lead outside — which is exactly what being blocked by a wall means. Reverse a sign and $\nabla f$ would have a feasible descent direction.

> [!example]- Worked example — the problem from §1, solved properly (C&Ż Example 21.6)
> $$\text{minimize } f=(x_1-1)^2+x_2-2 \quad\text{s.t.}\quad h=x_2-x_1-1=0,\ \ g=x_1+x_2-2\le0.$$
> $Dh=[-1,1]$ and $Dg=[1,1]$ are independent everywhere, so **all feasible points are regular.** With $Df=[2x_1-2,\ 1]$ the KKT conditions are
> $$[2x_1-2-\lambda+\mu,\ \ 1+\lambda+\mu]=\mathbf 0^{\mathsf T},\quad \mu(x_1+x_2-2)=0,\quad \mu\ge0,\quad x_2-x_1-1=0,\quad x_1+x_2\le2.$$
>
> **Enumerate on $\mu$ — this is the standard method.**
> - **Try $\mu>0$.** Then $g=0$, giving four linear equations; solving yields $x_1=\tfrac12,x_2=\tfrac32,\lambda=-1,\mu=0$. **But $\mu=0$ contradicts $\mu>0$**, so this branch yields nothing.
> - **Try $\mu=0$.** Then $2x_1-2-\lambda=0$, $1+\lambda=0$, $x_2-x_1-1=0$ give $\lambda^\star=-1$, $x_1^\star=\tfrac12$, $x_2^\star=\tfrac32$. Check the ignored inequality: $x_1+x_2=2\le2$ ✓ (feasible, and in fact **active**).
>
> So the unique KKT point is $\mathbf x^\star=\left(\tfrac12,\tfrac32\right)$, $\lambda^\star=-1$, $\mu^\star=0$, with $f=-\tfrac14$ ✓ — matching the direct substitution in §1.
>
> **Second-order check.** $L(\mathbf x^\star,\lambda^\star,\mu^\star)=F+\lambda^\star H+\mu^\star G=\begin{bmatrix}2&0\\0&0\end{bmatrix}$, since $h$ and $g$ are affine and contribute nothing. Because $\mu^\star=0$, the active $g$ **does not enter** $\tilde T$:
> $$\tilde T(\mathbf x^\star,\boldsymbol\mu^\star)=\{\mathbf y:Dh(\mathbf x^\star)\mathbf y=0\}=\{(a,a)^{\mathsf T}:a\in\mathbb R\},\qquad \mathbf y^{\mathsf T}L\mathbf y=2a^2>0 .$$
> **Positive definite on $\tilde T$, so $\mathbf x^\star$ is a strict local minimizer** — even though $L$ is only positive *semi*definite on $\mathbb R^2$. (Had we used $T(\mathbf x^\star)$, with both constraints active, we would have got $T=\{\mathbf 0\}$ and the test would have been vacuous. §9 explains why $\tilde T$ is the right set.)
>
> **This is a degenerate inequality**: $g$ is active yet $\mu^\star=0$. Geometrically, the constrained optimum along the line happens to sit exactly where the wall is — the wall is touching but not pushing. Compare [[10 - Duality|ch. 10]] Exercise 4, where the same degeneracy made shadow prices one-sided.

### 9. Second-order conditions with inequalities — and why $\tilde T\ne T$

Define $L(\mathbf x,\boldsymbol\lambda,\boldsymbol\mu)=F(\mathbf x)+[\boldsymbol\lambda H(\mathbf x)]+[\boldsymbol\mu G(\mathbf x)]$, with $G_k$ the Hessian of $g_k$. Two subspaces now matter:

$$T(\mathbf x^\star)=\{\mathbf y:D\mathbf h\mathbf y=\mathbf 0,\ Dg_j\mathbf y=0\ \forall j\in J(\mathbf x^\star)\}\quad\text{— \textbf{all} active constraints}$$
$$\tilde T(\mathbf x^\star,\boldsymbol\mu^\star)=\{\mathbf y:D\mathbf h\mathbf y=\mathbf 0,\ Dg_j\mathbf y=0\ \forall j\in J(\mathbf x^\star,\boldsymbol\mu^\star)\}\quad\text{— only \textbf{positively priced} ones}$$

where $J(\mathbf x^\star,\boldsymbol\mu^\star)=\{j:g_j(\mathbf x^\star)=0,\ \mu_j^\star>0\}\subseteq J(\mathbf x^\star)$, hence $T(\mathbf x^\star)\subseteq\tilde T(\mathbf x^\star,\boldsymbol\mu^\star)$.

- **SONC:** the KKT conditions hold, **and** $\mathbf y^{\mathsf T}L\mathbf y\ge0$ for all $\mathbf y\in T(\mathbf x^\star)$. *(Proof: treat active constraints as equalities and apply §6.)*
- **SOSC:** the KKT conditions hold, **and** $\mathbf y^{\mathsf T}L\mathbf y>0$ for all $\mathbf y\in\tilde T(\mathbf x^\star,\boldsymbol\mu^\star)$, $\mathbf y\ne\mathbf 0$. Then $\mathbf x^\star$ is a **strict** local minimizer.

**The asymmetry is deliberate and easy to get wrong.** The *necessary* condition uses the smaller set $T$ — a weaker demand, as it must be. The *sufficient* condition uses the larger set $\tilde T$ — a stronger demand, as it must be. **Using $T$ in SOSC would be wrong**, and using $\tilde T$ in SONC would claim more than is true. When no active inequality is degenerate, $J=J(\cdot,\boldsymbol\mu^\star)$ and the two coincide; degeneracy is exactly what separates them, and it is the reason §8's example needed $\tilde T$ to reach a verdict.

> [!example]- Worked example — a KKT point that is not a minimizer (C&Ż Example 21.5)
> $$\text{minimize } x_1x_2 \quad\text{s.t.}\quad x_1+x_2\ge2,\ \ x_2\ge x_1.$$
> Write $g_1=2-x_1-x_2\le0$, $g_2=x_1-x_2\le0$. With $Df=[x_2,x_1]$, KKT stationarity is $x_2-\mu_1+\mu_2=0$, $x_1-\mu_1-\mu_2=0$.
>
> **(b)** One checks $\mu_1\ne0$ and $\mu_2=0$, leaving the single KKT point $\mathbf x^\star=(1,1)$, $\mu_1^\star=1$, $\mu_2^\star=0$ (verified: $Dg_1=[-1,-1]$, $Dg_2=[1,-1]$ are independent, so $\mathbf x^\star$ is **regular**).
>
> **(c)** Both constraints are active, so $T(\mathbf x^\star)=\{\mathbf y:-y_1-y_2=0,\ y_1-y_2=0\}=\{\mathbf 0\}$ and **SONC holds vacuously.**
>
> **(d)** But $\mu_2^\star=0$, so $J(\mathbf x^\star,\boldsymbol\mu^\star)=\{1\}$ and $\tilde T=\{\mathbf y:y_1=-y_2\}$. Since $g_1,g_2$ are affine, $L=F=\begin{bmatrix}0&1\\1&0\end{bmatrix}$. Take $\mathbf y=(1,-1)\in\tilde T$: $\mathbf y^{\mathsf T}L\mathbf y=-2<0$. **SOSC fails.**
>
> **(e)** And indeed $\mathbf x^\star$ is **not** a local minimizer. Both $(1+t,1+t)$ and $(1-t,1+t)$ are feasible for $t>0$, but $f=(1+t)^2>1$ along the first and $f=1-t^2<1$ along the second. At $t=0.1$: $1.21$ versus $0.99$ ✓ (verified numerically).
>
> **The lesson:** SONC passing tells you nothing when $T=\{\mathbf 0\}$ — it is a test with no content. The degenerate constraint $\mu_2^\star=0$ is precisely what lets $\tilde T$ be bigger than $T$ and detect the failure. **Whenever $T$ collapses to $\{\mathbf 0\}$, go straight to $\tilde T$.**

### 10. Signs: the four cases, and the one table worth having

Chong & Żak's Theorem 21.1 is stated for **min / $\mathbf g\le\mathbf 0$**. Textbooks, solvers and lecturers differ, so here is the complete map. In each row, "stationarity" means $Df+\boldsymbol\lambda^{\mathsf T}D\mathbf h+\boldsymbol\mu^{\mathsf T}D\mathbf g=\mathbf 0^{\mathsf T}$ and only the sign restriction on $\boldsymbol\mu$ changes:

| Problem | constraint | $\boldsymbol\mu$ |
|---|---|---|
| **minimize** $f$ | $\mathbf g(\mathbf x)\le\mathbf 0$ | $\boldsymbol\mu^\star\ge\mathbf 0$ |
| **minimize** $f$ | $\mathbf g(\mathbf x)\ge\mathbf 0$ | $\boldsymbol\mu^\star\le\mathbf 0$ |
| **maximize** $f$ | $\mathbf g(\mathbf x)\le\mathbf 0$ | $\boldsymbol\mu^\star\le\mathbf 0$ |
| **maximize** $f$ | $\mathbf g(\mathbf x)\ge\mathbf 0$ | $\boldsymbol\mu^\star\ge\mathbf 0$ |

Complementary slackness $\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0$ and the feasibility conditions are unchanged in all four. **$\boldsymbol\lambda$ is always free**, whatever the row.

**Do not memorise this either** — every row follows from the first by negating $f$ or $\mathbf g$, which is how the table was made. What is worth remembering is the *invariant*: **$-\nabla f$ must lie in the cone spanned by the outward normals of the active constraints.** That sentence is sign-convention-free and always true.

> [!example]- Worked example — the nonnegativity-constrained problem (C&Ż Example 21.4)
> $$\text{minimize } f=x_1^2+x_2^2+x_1x_2-3x_1 \quad\text{s.t.}\quad x_1\ge0,\ x_2\ge0.$$
> Written with $\mathbf g(\mathbf x)=\mathbf x\ge\mathbf 0$ this is row 2, so $\boldsymbol\mu\le\mathbf 0$. With $Df=[2x_1+x_2-3,\ x_1+2x_2]$:
> $$2x_1+x_2+\mu_1=3,\qquad x_1+2x_2+\mu_2=0,\qquad \mu_1x_1+\mu_2x_2=0,\qquad \mathbf x\ge\mathbf 0,\ \boldsymbol\mu\le\mathbf 0.$$
> - **Try $\mu_1=0$, $x_2=0$:** then $x_1^\star=\tfrac32$ and $\mu_2^\star=-\tfrac32\le0$ ✓. All conditions hold. $f=-\tfrac94$.
> - **Try $\mu_2=0$, $x_1=0$:** then $x_2^\star=0$ and $\mu_1^\star=3>0$, **violating $\boldsymbol\mu\le\mathbf 0$.** Rejected.
>
> Verified independently: $\nabla f=\mathbf 0$ gives $(2,-1)$, which is **infeasible**; on the boundary $x_2=0$, $f=x_1^2-3x_1$ is minimized at $x_1=\tfrac32$ with $f=-\tfrac94$; on $x_1=0$, $f=x_2^2\ge0$. So $\left(\tfrac32,0\right)$ is the global minimizer ✓.
>
> **The general case is worth extracting.** For $\min f$ subject to $\mathbf x\ge\mathbf 0$, eliminating $\boldsymbol\mu$ leaves
> $$\nabla f(\mathbf x)\ge\mathbf 0,\qquad \mathbf x^{\mathsf T}\nabla f(\mathbf x)=0,\qquad \mathbf x\ge\mathbf 0,$$
> i.e. **each coordinate has either $x_i=0$ or $\partial f/\partial x_i=0$.** This is a *complementarity problem*, and it is the exact nonlinear analogue of ch. 10's $\mathbf r^{\mathsf T}\mathbf x=0$. It also describes what non-negative matrix factorisation and non-negative least squares are actually solving.

### 11. Sensitivity: the multipliers are prices again

[[10 - Duality|Chapter 10]] showed that LP dual variables are shadow prices. The same is true here, and it is the reason multipliers are worth reporting rather than discarding.

> [!note] Sensitivity theorem
> Let $f,\mathbf h\in C^2$ and consider the perturbed family
> $$\text{minimize } f(\mathbf x)\quad\text{subject to}\quad \mathbf h(\mathbf x)=\mathbf c .$$
> Suppose at $\mathbf c=\mathbf 0$ there is a local solution $\mathbf x^\star$, regular, satisfying SOSC with multiplier $\boldsymbol\lambda$. Then for all $\mathbf c$ near $\mathbf 0$ there is a solution $\mathbf x(\mathbf c)$ depending continuously on $\mathbf c$, with $\mathbf x(\mathbf 0)=\mathbf x^\star$, and
> $$\boxed{\ \nabla_{\mathbf c}\,f(\mathbf x(\mathbf c))\big|_{\mathbf c=\mathbf 0}=-\boldsymbol\lambda^{\mathsf T}\ }$$
> With inequalities $\mathbf g(\mathbf x)\le\mathbf d$ added and no active inequality degenerate, also $\nabla_{\mathbf d}f\big|_{\mathbf 0}=-\boldsymbol\mu^{\mathsf T}$.

*Proof idea.* Apply the **implicit function theorem** to the system $\nabla f(\mathbf x)+D\mathbf h(\mathbf x)^{\mathsf T}\boldsymbol\lambda=\mathbf 0$, $\mathbf h(\mathbf x)=\mathbf c$. Its Jacobian at the solution is the **KKT matrix**
$$\begin{bmatrix}L(\mathbf x^\star)&D\mathbf h(\mathbf x^\star)^{\mathsf T}\\ D\mathbf h(\mathbf x^\star)&0\end{bmatrix},$$
which is nonsingular precisely because $\mathbf x^\star$ is regular and $L$ is positive definite on $T$ — **that is what SOSC is for here.** Differentiability of $\mathbf x(\mathbf c)$ follows, and two chain-rule steps give the formula. $\blacksquare$

**So $-\lambda_i$ is the marginal cost of tightening constraint $i$**: relax $h_i=0$ to $h_i=c_i$ and the optimal value changes by $-\lambda_ic_i$ to first order. Everything ch. 10 §9 said carries over — it is a *derivative*, so it is local; it needs non-degeneracy to be two-sided; and it is only a subgradient at a kink.

> [!warning] The sign trap between chapters 10 and 11
> With $l=f+\boldsymbol\lambda^{\mathsf T}\mathbf h$, the multiplier is **minus** the shadow price. So for the LP $\min\mathbf c^{\mathsf T}\mathbf x$ s.t. $A\mathbf x=\mathbf b$, $\mathbf x\ge\mathbf 0$:
> $$\boldsymbol\lambda=-\mathbf y,$$
> where $\mathbf y$ is ch. 10's dual vector. Verified on ch. 10's own example: the LP with $A=\begin{psmallmatrix}1&1&1&0\\1&3&0&1\end{psmallmatrix}$, $\mathbf b=(4,6)$, $\mathbf c=(-2,-3,0,0)$ has $\mathbf y^\star=(-1.5,-0.5)$ and hence $\boldsymbol\lambda^\star=(1.5,0.5)$.
> **Many texts define $l=f-\boldsymbol\lambda^{\mathsf T}\mathbf h$ to make $\boldsymbol\lambda$ the price directly.** Neither is wrong; check which one you are reading before comparing numbers with anybody. Chong & Żak and Luenberger & Ye both use $+$, so these notes do too.

### 12. Where this goes: the Lagrangian dual, and the ML connection

*(§12 is largely my own; the sources are noted inline.)*

**KKT contains the LP dual as a special case.** Apply the theorem to $\min\mathbf c^{\mathsf T}\mathbf x$ s.t. $A\mathbf x=\mathbf b$, $\mathbf x\ge\mathbf 0$ — so $\mathbf h=A\mathbf x-\mathbf b$, $\mathbf g=-\mathbf x$, $D\mathbf g=-I$. Stationarity reads $\mathbf c+A^{\mathsf T}\boldsymbol\lambda-\boldsymbol\mu=\mathbf 0$. Substituting $\mathbf y=-\boldsymbol\lambda$:

$$\boldsymbol\mu=\mathbf c-A^{\mathsf T}\mathbf y\ \ge\ \mathbf 0 \qquad\Longrightarrow\qquad A^{\mathsf T}\mathbf y\le\mathbf c,$$

which is **exactly ch. 10's dual feasibility**, and $\boldsymbol\mu$ is exactly the **reduced-cost vector** $\mathbf r$. Complementary slackness $\boldsymbol\mu^{\mathsf T}\mathbf x=0$ is ch. 10's $\mathbf r^{\mathsf T}\mathbf x=0$. And

$$\mathbf c^{\mathsf T}\mathbf x=(A^{\mathsf T}\mathbf y+\boldsymbol\mu)^{\mathsf T}\mathbf x=\mathbf y^{\mathsf T}A\mathbf x+\boldsymbol\mu^{\mathsf T}\mathbf x=\mathbf y^{\mathsf T}\mathbf b+0,$$

which is **strong duality**. All of chapter 10's structure falls out of the KKT conditions in four lines. (Verified numerically on ch. 10's example: $\boldsymbol\mu=(0,0,1.5,0.5)\ge\mathbf 0$, $\boldsymbol\mu^{\mathsf T}\mathbf x^\star=0$, $\mathbf y^{\mathsf T}\mathbf b=\mathbf c^{\mathsf T}\mathbf x^\star=-9$.)

**And the dual generalises.** Ch. 10 §1 built the dual by taking nonnegative combinations of constraints; the nonlinear version defines the **dual function**

$$q(\boldsymbol\lambda,\boldsymbol\mu)=\inf_{\mathbf x}\ l(\mathbf x,\boldsymbol\lambda,\boldsymbol\mu)=\inf_{\mathbf x}\ \big\{f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf h(\mathbf x)+\boldsymbol\mu^{\mathsf T}\mathbf g(\mathbf x)\big\},\qquad \boldsymbol\mu\ge\mathbf 0 .$$

**Weak duality $q(\boldsymbol\lambda,\boldsymbol\mu)\le f^\star$ holds always**, for any problem whatsoever, convex or not — the one-line proof of ch. 10 §4 goes through unchanged, since at a feasible $\mathbf x$ we have $\boldsymbol\lambda^{\mathsf T}\mathbf h=0$ and $\boldsymbol\mu^{\mathsf T}\mathbf g\le0$. What can fail is *strong* duality: the gap $f^\star-\max q$ may be strictly positive, a **duality gap**, and that is the whole difference between this chapter and the linear case.

**Luenberger & Ye §11.9 shows what closes it**, via the **primal function**

$$\omega(\mathbf y)=\inf\{f(\mathbf x):\mathbf h(\mathbf x)=\mathbf y,\ \mathbf x\in\Omega\},$$

the optimal value as a function of the right-hand side, with $\omega(\mathbf 0)$ the original problem. **If $f$ is convex, $\Omega$ convex and $\mathbf h$ affine, then $\omega$ is convex** — and one then separates the epigraph of $\omega$ from the vertical line below $f^\star$ by a hyperplane whose slope is $-\boldsymbol\lambda$, proving that $\mathbf x^\star$ also minimizes the **Lagrangian relaxation** $\min_{\mathbf x\in\Omega}f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf h(\mathbf x)$. This needs **no derivatives at all** — hence "zero-order conditions" — and it is the same separating hyperplane that proved strong duality in ch. 10 §5. **Convexity is what makes $\omega$ have a supporting hyperplane at $\mathbf 0$, and that is the real content of [[12 - Convex Programming and Constrained Algorithms|ch. 12]].**

**Why a data scientist should care about this chapter specifically:**

- **Maximum entropy ⟹ exponential families.** Luenberger & Ye's Example 3: maximize $-\sum_ip_i\log p_i$ subject to $\sum_ip_i=1$ and $\sum_ix_ip_i=m$. The Lagrange condition gives $-\log p_i-1+\lambda+\mu x_i=0$, so $p_i=\exp\{(\lambda-1)+\mu x_i\}$ — **an exponential family, with the multipliers as its natural parameters.** (Note $p_i>0$ automatically, so the nonnegativity constraints are inactive and can be safely ignored, as the book does.) Verified: with $\mathbf x=(1,2,3)$ and $m=2$ this returns the uniform distribution $\left(\tfrac13,\tfrac13,\tfrac13\right)$ and entropy $\log3=1.0986$; with $m=1.5$ it returns $(0.6162,0.2676,0.1162)$, entropy $0.9012$, at $\mu=-0.8341$. **This single calculation is where the softmax, logistic regression, Boltzmann distributions, and the entire exponential family come from** — the softmax *is* the maximum-entropy distribution subject to matching expected features.
- **Markowitz portfolio theory** (their Example 5) is Lagrange with two equality constraints: minimize $\mathbf w^{\mathsf T}\Sigma\mathbf w$ subject to $\mathbf w^{\mathsf T}\bar{\mathbf r}=\bar r$ and $\mathbf 1^{\mathsf T}\mathbf w=1$, giving $n+2$ linear equations. Adding $\mathbf w\ge\mathbf 0$ (no short selling) turns it into a KKT problem, which is why real portfolio optimisers are quadratic programs.
- **The SVM** is the canonical KKT computation in ML: the multipliers $\alpha_i$ are the $\boldsymbol\mu$ of this chapter, **the support vectors are exactly the points with $\alpha_i>0$ — complementary slackness**, and the kernel trick works because the dual function depends on the data only through inner products.
- **Ridge and LASSO**: the penalty form $\min\|\mathbf y-X\boldsymbol\beta\|^2+\lambda\|\boldsymbol\beta\|_q$ and the constraint form $\min\|\mathbf y-X\boldsymbol\beta\|^2$ s.t. $\|\boldsymbol\beta\|_q\le t$ are a Lagrangian pair, and $\lambda$ is the multiplier. **That is why $\lambda$ and $t$ trace out the same solution path** ([[08 - Least Squares and Linear Equations|ch. 08]] §7).
- **Constrained deep learning** — fairness constraints, calibration constraints, KL-constrained policy updates in RLHF and TRPO — is all solved by Lagrangian methods, usually a primal–dual gradient scheme on $l(\mathbf x,\boldsymbol\lambda)$ with the multiplier updated by gradient *ascent*. Section 5's warning applies: this is a saddle-point problem, which is why such training is delicate.

## ✏️ Exercises

**1. (Lagrange, and the sensitivity theorem checked.)** Solve
$$\text{minimize } x_1^2+x_2^2 \quad\text{subject to}\quad x_1+2x_2=5,$$
and verify the sensitivity theorem by solving the perturbed family $x_1+2x_2=5+c$ explicitly and differentiating.

> [!example]- Solution
> With $f=x_1^2+x_2^2$ and $h=x_1+2x_2-5$, stationarity $\nabla f+\lambda\nabla h=\mathbf 0$ gives
> $$2x_1+\lambda=0,\qquad 2x_2+2\lambda=0\qquad\Longrightarrow\qquad x_1=-\tfrac\lambda2,\ \ x_2=-\lambda .$$
> Substituting into the constraint: $-\tfrac\lambda2-2\lambda=5$, so $-\tfrac52\lambda=5$ and $\lambda^\star=-2$. Hence
> $$\mathbf x^\star=(1,2),\qquad f^\star=1+4=5 .$$
> This is the squared distance from the origin to the line — check geometrically: $\operatorname{dist}=|{-5}|/\sqrt{1+4}=\sqrt5$, and $(\sqrt5)^2=5$ ✓. Second-order: $L=F+\lambda H=2I$ (the constraint is affine, $H=0$), positive definite on all of $\mathbb R^2$, so SOSC holds and $\mathbf x^\star$ is a strict local minimizer — in fact global, since $f$ is convex and the constraint affine ([[02 - Convex Sets and Convex Functions|ch. 02]]).
>
> **Sensitivity.** Redo it with $h=x_1+2x_2-5-c$:
> $$\mathbf x^\star(c)=\left(1+\tfrac c5,\ 2+\tfrac{2c}5\right),\qquad \lambda(c)=-2-\tfrac{2c}5,\qquad f^\star(c)=\tfrac{c^2}5+2c+5 .$$
> Then
> $$\frac{df^\star}{dc}\bigg|_{c=0}=2 \qquad\text{and}\qquad -\lambda(0)=2 .\qquad\textbf{Equal} \ \checkmark$$
> Exactly as the theorem promises. Note that $f^\star(c)$ is genuinely nonlinear in $c$ — the multiplier gives only the *derivative* at $c=0$, and the $c^2/5$ term is the error you incur by extrapolating. This is the nonlinear counterpart of ch. 10's "shadow prices are valid only within a range": there, the error came from a change of basis; here, from curvature.

**2. (Rayleigh quotient — the PCA computation.)** Find the maximum of $\mathbf x^{\mathsf T}Q\mathbf x$ subject to $\|\mathbf x\|=1$ for
$$Q=\begin{bmatrix}2&1&0\\1&2&1\\0&1&2\end{bmatrix},$$
using the Lagrange condition. Give the maximizer, the maximum value and the multiplier, and say what each means if $Q$ were a covariance matrix.

> [!example]- Solution
> Take $f=\mathbf x^{\mathsf T}Q\mathbf x$ and $h=\mathbf x^{\mathsf T}\mathbf x-1$. Since we are maximizing, minimize $-f$; either way stationarity gives
> $$2Q\mathbf x=2\lambda'\mathbf x\qquad\Longrightarrow\qquad Q\mathbf x=\lambda'\mathbf x,$$
> so **every candidate is an eigenvector of $Q$**, and (using $\|\mathbf x\|=1$) $f=\mathbf x^{\mathsf T}Q\mathbf x=\lambda'\|\mathbf x\|^2=\lambda'$: **the eigenvalue is the objective value.** So the maximum is the largest eigenvalue.
>
> $Q$ is the classic tridiagonal $2,1$ matrix, whose eigenvalues are $2+2\cos\frac{k\pi}{4}=2,\ 2\pm\sqrt2$ for $k=1,2,3$. Numerically: $\{0.585786,\ 2,\ 3.414214\}$ ✓.
> $$\lambda'_{\max}=2+\sqrt2\approx3.414214,\qquad \mathbf x^\star=\pm\tfrac12\left(1,\sqrt2,1\right)^{\mathsf T}\approx\pm(0.5,\ 0.707107,\ 0.5)^{\mathsf T}.$$
> Check: $\|\mathbf x^\star\|^2=\tfrac14(1+2+1)=1$ ✓, and $\mathbf x^{\star\mathsf T}Q\mathbf x^\star=3.414214$ ✓ (both verified numerically).
>
> Second-order: $L=-2Q+2\lambda' I$ for the minimization of $-f$, so on $T(\mathbf x^\star)=\{\mathbf y:\mathbf x^{\star\mathsf T}\mathbf y=0\}$ — the span of the other two eigenvectors — $\mathbf y^{\mathsf T}L\mathbf y=2\sum_{k\ne\max}(\lambda'_{\max}-\lambda'_k)c_k^2>0$ since $\lambda'_{\max}$ is strictly largest. **SOSC holds**, and $\pm\mathbf x^\star$ are strict maximizers of $f$.
>
> **Interpretation if $Q$ were a covariance matrix.** $\mathbf x^\star$ is the **first principal direction**; $\lambda'_{\max}=2+\sqrt2$ is the **variance explained along it**; and the multiplier being equal to the optimal value is why PCA's "explained variance" is read straight off the spectrum. The total variance is $\operatorname{tr}Q=6$, so this direction captures $3.4142/6=56.9\%$. **Note also what the multiplier being an eigenvalue tells you: the Lagrange condition has $n$ solutions, one per eigenvector, and only the extreme ones are extremizers** — the middle eigenvector $\lambda'=2$ is a KKT point that is neither a max nor a min, the situation §3's warning describes. Cross-reference: [[08 - Least Squares and Linear Equations|Linear Algebra ch. 08]] §10.

**3. (KKT with inequalities — enumerate the active sets.)** Solve
$$\text{minimize } (x_1-3)^2+(x_2+1)^2 \quad\text{subject to}\quad x_1+x_2\le2,\ \ x_1\ge0,\ \ x_2\ge0 .$$
Find all KKT points, verify regularity and SOSC, and identify the minimizer.

> [!example]- Solution
> This is the projection of the point $(3,-1)$ onto the triangle with vertices $(0,0),(2,0),(0,2)$. Write $g_1=x_1+x_2-2$, $g_2=-x_1$, $g_3=-x_2$, all $\le0$; then $\boldsymbol\mu\ge\mathbf 0$ and $\nabla f=\big(2(x_1-3),\ 2(x_2+1)\big)$.
>
> **Case A — no constraint active.** $\nabla f=\mathbf 0$ gives $(3,-1)$, which violates $x_2\ge0$. **Rejected.**
>
> **Case B — only $g_1$ active.** Solve $2(x_1-3)+\mu_1=0$, $2(x_2+1)+\mu_1=0$, $x_1+x_2=2$. Subtracting the first two gives $x_1-3=x_2+1$, i.e. $x_1=x_2+4$; with $x_1+x_2=2$ this yields $x_2=-1$, $x_1=3$, $\mu_1=0$. **But $x_2=-1<0$ is infeasible.** Rejected. *(Note this is just Case A again — $\mu_1=0$ means $g_1$ was not really active. That is the usual signal that a branch was mis-specified.)*
>
> **Case C — $g_1$ and $g_3$ active** ($x_1+x_2=2$, $x_2=0$, so $\mathbf x=(2,0)$). Then $\nabla f=(-2,2)$, $\nabla g_1=(1,1)$, $\nabla g_3=(0,-1)$. Stationarity:
> $$(-2,2)+\mu_1(1,1)+\mu_3(0,-1)=(0,0)\ \Longrightarrow\ \begin{cases}-2+\mu_1=0\\ 2+\mu_1-\mu_3=0\end{cases}\ \Longrightarrow\ \mu_1^\star=2,\ \ \mu_3^\star=4 .$$
> **Both $\ge0$** ✓, and $g_2=-2<0$ so $\mu_2^\star=0$ ✓. **Regular?** $\nabla g_1=(1,1)$, $\nabla g_3=(0,-1)$ have $\det\begin{psmallmatrix}1&0\\1&-1\end{psmallmatrix}=-1\ne0$: independent ✓. So $\mathbf x^\star=(2,0)$ is a KKT point, with $f=1+1=\mathbf 2$.
>
> **Case D — other active sets** ($g_2$ active, or all three) put $x_1=0$, giving $f\ge9$; and the vertex $(0,2)$ gives $f=9+9=18$. None competes.
>
> **SOSC.** $g_1,g_2,g_3$ are all affine, so their Hessians vanish and $L=F=2I$, positive definite on **all** of $\mathbb R^2$ — hence on $\tilde T$, whatever it is. (Here both active multipliers are positive, so $\tilde T=T=\{\mathbf y:y_1+y_2=0,\ y_2=0\}=\{\mathbf 0\}$ and the condition is vacuous; the $L=2I$ observation is the honest reason.) **$\mathbf x^\star=(2,0)$ is a strict local minimizer**, and since $f$ is convex on a convex set it is the **global** minimizer ([[02 - Convex Sets and Convex Functions|ch. 02]]).
>
> Verified two ways: `scipy.optimize.minimize` returns $(2,0)$ with $f=2$, and a brute-force sweep of $200{,}001$ points along the triangle's boundary finds a minimum of exactly $2.0$ at $(2,0)$.
>
> **Two takeaways.** (i) $\mathbf x^\star$ is a **vertex** of the feasible set even though $f$ is not linear — the target lies "past the corner", and the perpendicular feet onto both adjacent edges fall outside their segments. (ii) **Enumerating active sets is the honest way to solve small KKT problems by hand**, and it is what an active-set QP solver does mechanically. With $p$ inequalities there are $2^p$ subsets, which is exactly why active-set methods scale badly and why [[12 - Convex Programming and Constrained Algorithms|interior-point methods]] displaced them.

**4. (Regularity, and the limits of necessity.)** (a) Show that the Lagrange condition **fails at the true minimizer** of
$$\text{minimize } x_1 \quad\text{subject to}\quad h(\mathbf x)=x_1^3-x_2^2=0,$$
and explain precisely which hypothesis is violated. (b) Explain why a KKT point need not be a minimizer, using §9's example, and state what you must check.

> [!example]- Solution
> **(a)** The feasible set is $\{x_1^3=x_2^2\}$, i.e. $x_1=x_2^{2/3}\ge0$ — a **cusp** at the origin, opening rightwards. Since $x_1\ge0$ on the feasible set with equality only at the origin, the minimizer is
> $$\mathbf x^\star=(0,0),\qquad f^\star=0 .$$
> Now test the Lagrange condition. $\nabla f=(1,0)$ everywhere, and $\nabla h=(3x_1^2,\ -2x_2)$, so
> $$\nabla h(\mathbf 0)=(0,0).$$
> The condition $\nabla f(\mathbf x^\star)+\lambda\nabla h(\mathbf x^\star)=\mathbf 0$ becomes $(1,0)+\lambda(0,0)=(1,0)\ne\mathbf 0$: **no $\lambda$ works, for any $\lambda$ whatsoever.** The Lagrange condition fails at the genuine minimizer.
>
> **Which hypothesis?** *Regularity.* The theorem requires $\nabla h_1(\mathbf x^\star),\dots,\nabla h_m(\mathbf x^\star)$ to be linearly independent; with $m=1$ that just means $\nabla h(\mathbf x^\star)\ne\mathbf 0$, and here it is $\mathbf 0$. So $\mathbf x^\star$ is not a regular point and **the theorem does not apply** — it makes no claim, rather than making a false one.
>
> **The mechanism, geometrically.** Regularity is what guarantees $N(\mathbf x^\star)$ has dimension $m$; here it collapses to $\{\mathbf 0\}$, and $\nabla f\in N$ becomes $\nabla f=\mathbf 0$, which is false. Equivalently, the *linearised* tangent space $T=\mathcal N(D\mathbf h(\mathbf 0))=\mathbb R^2$ is far too big — it suggests every direction is available, when in truth the cusp permits only the rightward ones. **The linearisation lies about the geometry, and that is exactly what a constraint qualification forbids.** (Chong & Żak's Example 20.5 makes the same point with a piecewise-defined $h$ that is flat on an interval.)
>
> Note the cure: the *same feasible set* is the image of $t\mapsto(t^2,t^3)$, and posed that way the problem is $\min t^2$ over $t\in\mathbb R$, which chapter 03 handles at once. **Regularity is a property of how you write the constraints, not of the set** — as §2's worked example also showed.
>
> **(b)** The KKT conditions are **necessary, not sufficient** — they are satisfied at minimizers, maximizers, and saddle-like points alike, just as $\nabla f=\mathbf 0$ is in [[03 - Unconstrained Optimality Conditions|ch. 03]]. §9's example is the concrete demonstration: $\min x_1x_2$ subject to $x_1+x_2\ge2$, $x_2\ge x_1$ has the **unique** KKT point $\mathbf x^\star=(1,1)$ with $\mu_1^\star=1,\mu_2^\star=0$, and it is regular — yet it is **not a local minimizer**, since moving along the feasible direction $(-1,1)$ gives $f=1-t^2<1$.
>
> **What you must check**, in order:
> 1. **Feasibility and the sign of $\boldsymbol\mu$** — the cheapest filters, and they eliminate most branches (see Exercise 3 Cases A–B).
> 2. **SOSC on $\tilde T$**, not on $T$. In this example SONC on $T$ passes *vacuously* because both constraints are active and $T=\{\mathbf 0\}$; only the larger $\tilde T=\{y_1=-y_2\}$, available because $\mu_2^\star=0$ is degenerate, detects $\mathbf y^{\mathsf T}L\mathbf y=-2<0$. **Whenever $T$ collapses to $\{\mathbf 0\}$, treat a SONC "pass" as no information at all.**
> 3. **A global argument if you need a global claim.** SOSC gives only *strict local*. Convexity of $f$ and of the feasible set upgrades it to global ([[02 - Convex Sets and Convex Functions|ch. 02]]) — which is what [[12 - Convex Programming and Constrained Algorithms|ch. 12]] is about. Failing that, compare values across all KKT points, and check that a minimizer exists at all (Weierstrass or coercivity, [[01 - The Optimization Problem|ch. 01]]).

**5. (Hard — derive the LP dual from KKT.)** Apply the KKT theorem to the linear program
$$\text{minimize } \mathbf c^{\mathsf T}\mathbf x \quad\text{subject to}\quad A\mathbf x=\mathbf b,\ \ \mathbf x\ge\mathbf 0,$$
and recover from it: the dual feasibility condition of [[10 - Duality|ch. 10]], the identification of the multipliers with reduced costs, complementary slackness, and strong duality. State the sign relation between $\boldsymbol\lambda$ and ch. 10's $\mathbf y$.

> [!example]- Solution
> **Set-up.** Match the chapter's standard form: $f(\mathbf x)=\mathbf c^{\mathsf T}\mathbf x$, $\mathbf h(\mathbf x)=A\mathbf x-\mathbf b$, and $\mathbf g(\mathbf x)=-\mathbf x\le\mathbf 0$. The derivatives are $\nabla f=\mathbf c$, $D\mathbf h=A$, $D\mathbf g=-I$.
>
> **KKT conditions.** With multipliers $\boldsymbol\lambda\in\mathbb R^m$ (free) and $\boldsymbol\mu\in\mathbb R^n$:
> $$\text{(1) }\boldsymbol\mu\ge\mathbf 0,\qquad \text{(2) }\mathbf c+A^{\mathsf T}\boldsymbol\lambda-\boldsymbol\mu=\mathbf 0,\qquad \text{(3) }\boldsymbol\mu^{\mathsf T}(-\mathbf x)=0,\qquad \text{(4) }A\mathbf x=\mathbf b,\qquad \text{(5) }\mathbf x\ge\mathbf 0 .$$
>
> **Substitute $\mathbf y=-\boldsymbol\lambda$.** This is the sign relation, and it is forced by the convention $l=f+\boldsymbol\lambda^{\mathsf T}\mathbf h$; see §11's warning. Condition (2) becomes
> $$\boxed{\ \boldsymbol\mu=\mathbf c-A^{\mathsf T}\mathbf y\ }$$
>
> **(i) Dual feasibility.** Combining this with (1): $\mathbf c-A^{\mathsf T}\mathbf y\ge\mathbf 0$, i.e.
> $$A^{\mathsf T}\mathbf y\le\mathbf c \quad\Longleftrightarrow\quad \mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T},$$
> **which is precisely the constraint of ch. 10's asymmetric dual** $\max\{\mathbf y^{\mathsf T}\mathbf b:\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}\}$. So the nonnegativity of the KKT multipliers on $\mathbf x\ge\mathbf 0$ *is* dual feasibility. Note $\mathbf y$ is unrestricted in sign, matching the asymmetric form ✓.
>
> **(ii) The multipliers are the reduced costs.** $\boldsymbol\mu=\mathbf c-A^{\mathsf T}\mathbf y$ is exactly ch. 10 §7's $\mathbf r^{\mathsf T}=\mathbf c^{\mathsf T}-\mathbf y^{\mathsf T}A$. So $\mu_j$ is the reduced cost of variable $j$ — the per-unit penalty for forcing activity $j$ into the plan — and (1) says all reduced costs are nonnegative, which is the **simplex optimality test** of [[09 - Linear Programming and the Simplex Method|ch. 09]].
>
> **(iii) Complementary slackness.** Condition (3) is $\boldsymbol\mu^{\mathsf T}\mathbf x=0$, i.e. $\mathbf r^{\mathsf T}\mathbf x=0$ — verbatim ch. 10 §7. Componentwise, since $\mu_j\ge0$ and $x_j\ge0$ every term is $\ge0$, so **$\mu_jx_j=0$ for every $j$: each variable is either zero or has zero reduced cost.** That is "basic variables have zero reduced cost; variables with nonzero reduced cost are nonbasic."
>
> **(iv) Strong duality.** Using (2) then (3) then (4):
> $$\mathbf c^{\mathsf T}\mathbf x=(A^{\mathsf T}\mathbf y+\boldsymbol\mu)^{\mathsf T}\mathbf x=\mathbf y^{\mathsf T}(A\mathbf x)+\underbrace{\boldsymbol\mu^{\mathsf T}\mathbf x}_{=0}=\mathbf y^{\mathsf T}\mathbf b .$$
> **The primal and dual objective values are equal** — ch. 10's duality theorem, in one line, as a corollary of KKT.
>
> **Numerical check** on ch. 10's own example, $A=\begin{bmatrix}1&1&1&0\\1&3&0&1\end{bmatrix}$, $\mathbf b=(4,6)$, $\mathbf c=(-2,-3,0,0)$:
>
> | quantity | value |
> |---|---|
> | $\mathbf x^\star$ | $(3,1,0,0)$ |
> | $\mathbf y^\star$ (solver marginals) | $(-1.5,-0.5)$ |
> | $\boldsymbol\lambda^\star=-\mathbf y^\star$ | $(1.5,0.5)$ |
> | $\boldsymbol\mu^\star=\mathbf c-A^{\mathsf T}\mathbf y^\star$ | $(0,0,1.5,0.5)\ \ge\mathbf 0$ ✓ |
> | $\boldsymbol\mu^{\star\mathsf T}\mathbf x^\star$ | $0$ ✓ |
> | $\mathbf c^{\mathsf T}\mathbf x^\star=\mathbf y^{\star\mathsf T}\mathbf b$ | $-9$ ✓ |
>
> The reduced costs of the two slacks are $1.5$ and $0.5$, exactly the shadow prices ch. 10 §9 computed — **the loose end from ch. 09, now closed twice over.**
>
> **What this exercise really shows.** Chapters 09–10 are not a separate theory; they are **this** theory specialised to the case where $f$ and all constraints are affine, so that (a) every point is regular whenever $A$ has full row rank, (b) all the Hessians vanish and the second-order conditions carry no information, and (c) convexity is automatic, so KKT is not merely necessary but **sufficient and global**. That last point is what [[12 - Convex Programming and Constrained Algorithms|ch. 12]] generalises.

## 📝 Summary

- **[[03 - Unconstrained Optimality Conditions|Ch. 03]]'s condition is false under constraints.** $\nabla f(\mathbf x^\star)\ne\mathbf 0$ at a constrained minimizer; you stop because a wall blocks you, not because the ground is flat.
- **Two subspaces do all the work.** At a feasible $\mathbf x^\star$, the **tangent space** $T=\mathcal N(D\mathbf h)$ holds the locally available directions and the **normal space** $N=\mathcal R(D\mathbf h^{\mathsf T})=\operatorname{span}[\nabla h_i]$ holds the forbidden ones. They are orthogonal complements, $\dim T=n-m$, and **every condition below is chapter 03's condition restricted to $T$.**
- **Regularity** ($\nabla h_i(\mathbf x^\star)$ linearly independent; for inequalities, only **active** ones count) is what makes the linearisation honest. **Without it the theory is simply false** — Exercise 4's cusp is a genuine minimizer at which no multiplier exists. It is a property of the *representation*, not the set.
- **Lagrange condition:** at a regular local extremizer there is $\boldsymbol\lambda^\star$ with $\nabla f(\mathbf x^\star)+D\mathbf h(\mathbf x^\star)^{\mathsf T}\boldsymbol\lambda^\star=\mathbf 0$ — compactly, **$\nabla f(\mathbf x^\star)\in N(\mathbf x^\star)$.** With feasibility that is $n+m$ equations in $n+m$ unknowns.
- **The Lagrangian $l=f+\boldsymbol\lambda^{\mathsf T}\mathbf h$ converts the constrained first-order condition into unconstrained stationarity**, $Dl(\mathbf x^\star,\boldsymbol\lambda^\star)=\mathbf 0^{\mathsf T}$. But $(\mathbf x^\star,\boldsymbol\lambda^\star)$ is a **saddle point**, never a minimum — $l$ is linear in $\boldsymbol\lambda$.
- **Second order:** with $L=F+[\boldsymbol\lambda H]$ (**constraint curvature enters**), SONC is $L\succeq0$ on $T$ and SOSC is $L\succ0$ on $T$ ⟹ strict local minimizer. Definiteness is needed **only on $T$**; $L$ can be indefinite on $\mathbb R^n$. Test via a basis of $T$, or the projected Hessian test ($P_ALP_A$ semidefinite **and** of rank $n-m$).
- **The Rayleigh quotient is the chapter's most reusable example:** $\max\mathbf x^{\mathsf T}Q\mathbf x$ s.t. $\mathbf x^{\mathsf T}P\mathbf x=1$ has Lagrange condition $P^{-1}Q\mathbf x=\lambda\mathbf x$, **the multiplier equals the optimal value**, and the answer is the largest generalized eigenvalue. **This is PCA** (with $P=I$), Fisher's discriminant, CCA and spectral clustering.
- **KKT** adds inequalities via the **active set**. Five conditions: $\boldsymbol\mu^\star\ge\mathbf 0$; stationarity $Df+\boldsymbol\lambda^{\star\mathsf T}D\mathbf h+\boldsymbol\mu^{\star\mathsf T}D\mathbf g=\mathbf 0^{\mathsf T}$; $\boldsymbol\mu^{\star\mathsf T}\mathbf g(\mathbf x^\star)=0$; and the two feasibility conditions. **Inactive constraints have zero multiplier.** The sign-free invariant: **$-\nabla f$ lies in the cone of outward normals of the active constraints.**
- **SONC uses $T$, SOSC uses the larger $\tilde T$** (dropping degenerate active constraints with $\mu_j^\star=0$). They coincide when no active inequality is degenerate. **When $T=\{\mathbf 0\}$ a SONC pass carries no information** — go to $\tilde T$.
- **Sensitivity: $\nabla_{\mathbf c}f^\star=-\boldsymbol\lambda^{\mathsf T}$** — the multipliers are marginal prices, as in [[10 - Duality|ch. 10]]. Watch the sign: **$\boldsymbol\lambda=-\mathbf y$** relative to ch. 10's dual vector under the convention $l=f+\boldsymbol\lambda^{\mathsf T}\mathbf h$.
- **KKT contains all of chapter 10.** Applied to an LP it yields dual feasibility, the reduced costs as multipliers, complementary slackness and strong duality in four lines (Exercise 5). **Weak duality $q(\boldsymbol\lambda,\boldsymbol\mu)\le f^\star$ holds for every problem, convex or not**; only *strong* duality needs convexity, which is [[12 - Convex Programming and Constrained Algorithms|ch. 12]].

## ⚠️ Important Notes

1. **Never write $\nabla f(\mathbf x^\star)=\mathbf 0$ for a constrained problem.** It is the single most common error, and it is not an approximation — it is a different, false, statement. The correct condition is $\nabla f(\mathbf x^\star)\in N(\mathbf x^\star)$.
2. **Check regularity before invoking the theorem, and check it at the candidate point.** Regularity is local: a problem can have regular and irregular feasible points. Only **active** inequality constraints enter the test — including inactive ones will make regularity fail spuriously.
3. **Count equations before solving.** Lagrange gives $n+m$ equations in $n+m$ unknowns. If your system is over- or under-determined you have mis-specified something — usually by forgetting $\mathbf h(\mathbf x^\star)=\mathbf 0$, which is half the condition, not an afterthought.
4. **Solve KKT problems by enumerating active sets, and be systematic.** For each candidate active set: assume those constraints hold with equality, solve stationarity, then **check the two things that reject most branches** — feasibility of the ignored constraints, and the sign of $\boldsymbol\mu$. A branch that returns $\mu_j=0$ for a constraint you assumed active is telling you the branch was really a different one.
5. **A branch yielding $\mu_j<0$ is rejected, not repaired.** It does not mean "flip the sign"; it means that active set is not optimal. Similarly a solution violating an ignored constraint is discarded outright.
6. **Complementary slackness gives implications, not equivalences.** $g_j(\mathbf x^\star)<0\Rightarrow\mu_j^\star=0$ is valid. The converse is **not**: $\mu_j^\star=0$ with $g_j(\mathbf x^\star)=0$ is the degenerate case and it really occurs — §8's worked example has exactly that. This is the same trap as ch. 10's Important Note 7.
7. **Degeneracy ($g_j$ active with $\mu_j^\star=0$) is where things get subtle.** It separates $T$ from $\tilde T$, breaks the two-sidedness of sensitivity, and makes the dual optimum non-unique. It is the nonlinear face of the same phenomenon ch. 10's Exercise 4 exposed. **Notice it and say so** rather than reporting a clean number.
8. **The second-order test lives on a subspace, and which subspace matters.** $L\succ0$ on $\mathbb R^n$ is sufficient but far too strong; $L\succ0$ on $T$ is what SOSC needs for equality constraints; **$L\succ0$ on $\tilde T$ is what it needs with inequalities.** Mixing these up produces both false positives and false negatives.
9. **Constraint curvature enters $L$ via $[\boldsymbol\lambda H]+[\boldsymbol\mu G]$.** For affine constraints these vanish and $L=F$, which is why LP's second-order conditions are empty. For a *curved* constraint the second-order test changes even when $f$ is a perfect quadratic — do not skip the constraint Hessians.
10. **KKT is necessary, not sufficient.** Candidates include maximizers and points that are neither (§9's example is a unique, regular KKT point that is not a minimizer). Always classify afterwards, and remember SOSC delivers only *strict local*. **Convexity is what upgrades KKT to sufficient and global** ([[12 - Convex Programming and Constrained Algorithms|ch. 12]]).
11. **Confirm a minimizer exists before hunting for it.** Lagrange and KKT find critical points of a problem that may have no solution at all. Weierstrass or a coercivity argument ([[01 - The Optimization Problem|ch. 01]]) settles existence; without it, a "solution" to the KKT system can be meaningless.
12. **Never hand a Lagrangian to an unconstrained minimizer.** $(\mathbf x^\star,\boldsymbol\lambda^\star)$ is a saddle point of $l$, which is unbounded below in $\boldsymbol\lambda$. This is a structural fact, not a numerical difficulty, and it is why penalty, barrier and primal–dual methods exist — and why min–max training in ML is delicate.
13. **Fix your sign convention and state it.** $l=f+\boldsymbol\lambda^{\mathsf T}\mathbf h$ (Chong & Żak, Luenberger & Ye, these notes) makes $\boldsymbol\lambda$ **minus** the shadow price; $l=f-\boldsymbol\lambda^{\mathsf T}\mathbf h$ makes it the price. Relative to [[10 - Duality|ch. 10]]'s dual vector, $\boldsymbol\lambda=-\mathbf y$. Before comparing a multiplier with a textbook, a solver, or a classmate, establish whose convention is in play.
14. **Report the multipliers.** Like LP duals they are free output and they carry the sensitivity information — the marginal cost of every constraint. `scipy.optimize.minimize` exposes them; most QP and NLP solvers do too. Discarding them throws away half the answer.
15. **You have already used this chapter.** The softmax and every exponential family are the maximum-entropy Lagrange calculation (§12); PCA, Fisher's LDA and spectral clustering are §7; support vectors are complementary slackness; and the equivalence of ridge/LASSO's penalty and constraint forms is a Lagrangian pair. **If a derivation in an ML paper produces multipliers out of nowhere, it is doing §8 in shorthand.**

> [!warning] Gaps in the source material
> **Extraction damage.** Chong & Żak ch. 20–21 is scanned; on top of the standard OCR substitutions in `../CLAUDE.md`, this pair of chapters loses **all Jacobian and Hessian matrices' bracket and row structure** — e.g. Example 20.9's $L(\mathbf x^\star,\lambda^\star)$ extracts as `p ° . v y 10 —2J`. Every matrix in this chapter was reconstructed by hand and then verified by reproducing the book's own printed conclusion. Theorem statements and proofs survived well; the multiplier symbols $\lambda$/$\mu$ are frequently corrupted (`μ\`, `M5`, `ß*`, `/x2`) and were disambiguated from context.
> **Luenberger & Ye §11.6's Example 3 is a casualty of the reverse problem** — it is born-digital but its display matrices unroll into ~90 lines of single digits and bracket fragments. The projected-Hessian material in §6 is stated in general form; the book's worked $3\times3$ instance is not reproduced because its two matrices cannot be read with confidence.
> **All figures in both chapters are images and are lost.** This is more damaging here than anywhere else in the subject, because **Chong & Żak ch. 20–21 is taught through pictures**: Figures 20.1 (the graphical solution used in §1 and §8), 20.2–20.3 (surfaces in $\mathbb R^3$), 20.4–20.9 (curves, tangent and normal planes), **20.12 (the four configurations satisfying the Lagrange condition, including the non-extremizer)**, 20.13 (where the condition fails), **21.1 (the geometric reading of KKT — the single most useful figure in the chapter)**, 21.3 and 21.4. §2, §3, §8 and §10 state the geometric content in words and algebra; **the figures themselves are not reconstructed.** Figure 21.2 (a circuit diagram) is also lost, though §21.2's worked example is fully recoverable from the prose and was re-derived.
> **Verification performed.** Every numeric claim was recomputed with `sympy`, `numpy` and `scipy` before being written. C&Ż: Ex 20.1/21.6 (KKT solve returns $\mathbf x^\star=(\tfrac12,\tfrac32)$, $\lambda^\star=-1$, $\mu^\star=0$, $g$ **active**, $f=-\tfrac14$, matching the direct substitution $f=x_1^2-x_1$ on $x_1\le\tfrac12$); Ex 20.6 (the box is a cube, side $\sqrt{A/6}$); Ex 20.7 (on the ellipse $f=1-x_2^2$, so max $1$ at $(\pm1,0)$ and min $\tfrac12$ at $(0,\pm1/\sqrt2)$); Ex 20.8–20.9 (eigenvalues of $P^{-1}Q$ are $\{2,1\}$; $\mathbf x^\star=(1/\sqrt2,0)$; $L=\operatorname{diag}(0,-2)$; $\mathbf y^{\mathsf T}L\mathbf y=-2$ on $T$); Ex 21.2 (a: $dp/dR=400(10-R)/(10+R)^3$, $R^\star=10$, $p=10\,$W, $\mu=0$; b: $R^\star=0$, $p=40\,$W, $\mu=8$); Ex 21.4 ($\nabla f=\mathbf 0$ gives the infeasible $(2,-1)$; boundary minimum $(\tfrac32,0)$, $f=-\tfrac94$, $\mu_2^\star=-\tfrac32$); Ex 21.5 (unique KKT point $(1,1)$ with $\boldsymbol\mu^\star=(1,0)$; $L=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$; $\mathbf y^{\mathsf T}L\mathbf y=-2$ on $\tilde T$; and $f=0.99<1$ along $(1-t,1+t)$ at $t=0.1$, confirming it is not a minimizer). L&Y: the sensitivity theorem's sign was confirmed symbolically on Exercise 1 ($df^\star/dc|_0=2=-\lambda(0)$), and the entropy example's exponential solution was solved numerically for $\mathbf x=(1,2,3)$ at $m=2$ and $m=1.5$. All five exercises were verified, Exercise 3 additionally by a $200{,}001$-point brute-force sweep. **No mathematical error was found in either book's treatment** — consistent with the subject's pattern that C&Ż's defects cluster in its numerical-methods chapters (errata table in `00-Index.md`).
> **Additions beyond the sources.** §7's identification of the Rayleigh-quotient result with **PCA, Fisher's LDA, CCA and spectral clustering** is mine — Chong & Żak present Examples 20.8–20.9 as pure algebra and never mention a statistical application, which badly undersells the most DS-relevant result in the chapter. §10's four-case sign table is assembled from C&Ż's scattered derivations, and the "$-\nabla f$ lies in the cone of outward normals" invariant is my own framing. **§12 is largely mine**: the four-line derivation of the LP dual from KKT (Exercise 5) appears in neither book, nor does the explicit cross-reference of the five KKT conditions to [[10 - Duality|ch. 10]]'s theorems; L&Y §11.9 supplies the primal function and Lagrangian relaxation but never connects them back to its own ch. 4. The **machine-learning discussion** — softmax and exponential families as maximum entropy, SVM support vectors as complementary slackness, ridge/LASSO as a Lagrangian pair, and constrained deep learning as primal–dual ascent — is entirely an addition; the books predate or ignore all of it. The saddle-point warning in §5 and the practical subspace-testing advice in §6 are also mine. **The Markowitz portfolio example is L&Y's own (Example 5), lightly reframed.**
> **Not covered.** C&Ż §20.6 (minimizing a quadratic subject to $A\mathbf x=\mathbf b$, with the closed form $\mathbf x^\star=Q^{-1}A^{\mathsf T}(AQ^{-1}A^{\mathsf T})^{-1}\mathbf b$) is **omitted here because [[08 - Least Squares and Linear Equations|ch. 08]] §5 already derives the $Q=I$ case as the minimum-norm solution**; the general result and its optimal-control application (C&Ż Example 20.10) are noted in `00-Index.md` instead. L&Y §11.4's **hanging-chain** example is omitted as a physics application with no DS analogue. L&Y §11.6's detailed eigenvalue-in-tangent-subspace theory beyond the projected Hessian test is graduate material and out of scope.

**Previous:** [[10 - Duality]] · **Next:** [[12 - Convex Programming and Constrained Algorithms]]
