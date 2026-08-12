---
subject: Optimization
chapter: 05
tags: [ds, optimization, gradient-descent, steepest-descent, condition-number, convergence-rate, kantorovich, preconditioning, sgd]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 8; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, §§8.2–8.4"
---

# Gradient Methods

> [!abstract] What this chapter is for
> **This is the chapter a data-science reader needs most.** Every model trained by gradient descent — which is every model — is running the algorithm of §2, and its behaviour is governed by the single number derived in §5.
>
> $$\boxed{\mathbf x_{k+1}=\mathbf x_k-\alpha_k\nabla f(\mathbf x_k)}$$
>
> | § | Question | Answer |
> |---|---|---|
> | **1** | Why $-\nabla f$? | Cauchy–Schwarz: it is the direction of steepest decrease |
> | **3** | How to choose $\alpha_k$ exactly? | Line search; closed form for quadratics; **consecutive steps are orthogonal** |
> | **4** | Can $\alpha$ be fixed? | Yes, **iff $0<\alpha<2/\lambda_{\max}$** — and the bound is sharp |
> | **5** | **How fast?** | $\left(\dfrac{\kappa-1}{\kappa+1}\right)^2$ per step, $\kappa=\dfrac{\lambda_{\max}}{\lambda_{\min}}$ — **and this bound is attained** |
> | **7** | What if $\kappa$ is bad? | **Rescale.** Everything in chapters 06–07 is an automatic way of doing so |
> | **8** | What do modern optimizers actually do? | **Stochastic gradients** — which none of these books covers |
>
> **§5 is the chapter.** "Gradient descent is slow" is not a vague complaint; it is the precise statement that the error contracts by $\left(\frac{\kappa-1}{\kappa+1}\right)^2$ per iteration, so **$\kappa=100$ needs 346 iterations for six digits and $\kappa=10^4$ needs 34,539.**

---

## 📘 Main Knowledge

### 1. Why the negative gradient

**Claim: among all unit directions, $\nabla f/\lVert\nabla f\rVert$ maximises the rate of increase of $f$.**

The rate of increase in direction $\mathbf d$ with $\lVert\mathbf d\rVert=1$ is $\langle\nabla f(\mathbf x),\mathbf d\rangle$ ([[03 - Unconstrained Optimality Conditions|ch. 03]] §1). By **Cauchy–Schwarz**,

$$\langle\nabla f(\mathbf x),\mathbf d\rangle\ \le\ \lVert\nabla f(\mathbf x)\rVert\,\lVert\mathbf d\rVert=\lVert\nabla f(\mathbf x)\rVert$$

with equality exactly when $\mathbf d=\nabla f(\mathbf x)/\lVert\nabla f(\mathbf x)\rVert$. **So $+\nabla f$ is the steepest ascent direction and $-\nabla f$ the steepest descent direction.** $\blacksquare$

**And a step along it really does decrease $f$.** By Taylor,
$$f\big(\mathbf x-\alpha\nabla f(\mathbf x)\big)=f(\mathbf x)-\alpha\lVert\nabla f(\mathbf x)\rVert^2+o(\alpha)$$
so if $\nabla f(\mathbf x)\ne\mathbf 0$ then for all sufficiently small $\alpha>0$, $f(\mathbf x-\alpha\nabla f(\mathbf x))<f(\mathbf x)$.

> [!warning] "Steepest" is a statement about an infinitesimal step, and that is the whole problem
> **The negative gradient is optimal only in the limit $\alpha\to0$.** For any finite step it may be a poor direction, and §6 shows it can be arbitrarily poor.
>
> **It is also not coordinate-free.** The gradient depends on the inner product you measure "steepness" with; **rescaling the variables changes the direction of $-\nabla f$**, even though it does not change the problem. §7 turns this defect into a technique.

---

### 2. The algorithm, and the three ways to pick $\alpha_k$

$$\mathbf x_{k+1}=\mathbf x_k-\alpha_k\mathbf g_k,\qquad \mathbf g_k:=\nabla f(\mathbf x_k)$$

| Choice of $\alpha_k$ | Name | Cost per step | §|
|---|---|---|---|
| $\arg\min_{\alpha>0}f(\mathbf x_k-\alpha\mathbf g_k)$ | **steepest descent** (exact line search) | a full 1-D minimisation | 3 |
| $\alpha_k=\alpha$ constant | **fixed-step-size gradient method** | one gradient | 4 |
| Armijo backtracking | **inexact line search** | 1–5 function evaluations | [[04 - One-Dimensional Search Methods\|ch. 04]] §9 |

**Chong & Żak's framing of the trade-off is exactly right:** small steps with frequent re-evaluation of the gradient give a laborious path; large steps give a zig-zag path but fewer gradient evaluations. **Neither extreme is right, and §5 explains why the middle is also not very good.**

> [!note] Stopping criteria (and why they must be relative)
> $$\frac{\lVert\mathbf x_{k+1}-\mathbf x_k\rVert}{\max\{1,\lVert\mathbf x_k\rVert\}}<\varepsilon \qquad\text{or}\qquad \frac{\lvert f(\mathbf x_{k+1})-f(\mathbf x_k)\rvert}{\max\{1,\lvert f(\mathbf x_k)\rvert\}}<\varepsilon \qquad\text{or}\qquad \lVert\nabla f(\mathbf x_k)\rVert<\varepsilon$$
> **The $\max\{1,\cdot\}$ guards against dividing by something near zero**, and the relative form guards against scale dependence: multiplying $f$ by $1000$ changes nothing about the problem but changes when an absolute test fires. *(See [[01 - The Optimization Problem|ch. 01]] §5.)*
>
> **These criteria apply to every algorithm in chapters 05–08**, not just this one.

---

### 3. Steepest descent: the exact line search

**Two structural facts hold for any $f$.**

> [!important] Proposition 1 — consecutive steps are orthogonal
> $$\big\langle\mathbf x_{k+1}-\mathbf x_k,\ \mathbf x_{k+2}-\mathbf x_{k+1}\big\rangle=0$$
>
> **Proof.** The two displacements are $-\alpha_k\mathbf g_k$ and $-\alpha_{k+1}\mathbf g_{k+1}$, so the inner product is $\alpha_k\alpha_{k+1}\langle\mathbf g_k,\mathbf g_{k+1}\rangle$. Now $\alpha_k$ minimises $\phi_k(\alpha)=f(\mathbf x_k-\alpha\mathbf g_k)$, so by the FONC and the chain rule
> $$0=\phi_k'(\alpha_k)=\nabla f(\mathbf x_k-\alpha_k\mathbf g_k)^{\mathsf T}(-\mathbf g_k)=-\langle\mathbf g_{k+1},\mathbf g_k\rangle\qquad\blacksquare$$

**This is not a technicality — it is the picture of the algorithm.** Every step is perpendicular to the previous one, so the path is a staircase of right angles. **$-\nabla f(\mathbf x_{k+1})$ is parallel to the tangent plane of the level set at $\mathbf x_{k+1}$**, which is exactly why the method cannot see around a curved valley (§6).

> [!important] Proposition 2 — the descent property
> If $\nabla f(\mathbf x_k)\ne\mathbf 0$ then $f(\mathbf x_{k+1})<f(\mathbf x_k)$.
>
> **Proof.** $\phi_k'(0)=-\lVert\mathbf g_k\rVert^2<0$, so $\phi_k$ strictly decreases at $0$; hence $f(\mathbf x_{k+1})=\phi_k(\alpha_k)\le\phi_k(\bar\alpha)<\phi_k(0)=f(\mathbf x_k)$ for some small $\bar\alpha>0$. $\blacksquare$

#### The quadratic case, where everything is computable

Let
$$f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x-\mathbf b^{\mathsf T}\mathbf x,\qquad Q=Q^{\mathsf T}\succ0$$
Then $\nabla f(\mathbf x)=Q\mathbf x-\mathbf b$, $\nabla^2f=Q$, and the unique minimizer is $\mathbf x^*=Q^{-1}\mathbf b$.

> [!note] Why $Q$ may be assumed symmetric at no cost
> For any $A$, $\mathbf x^{\mathsf T}A\mathbf x=(\mathbf x^{\mathsf T}A\mathbf x)^{\mathsf T}=\mathbf x^{\mathsf T}A^{\mathsf T}\mathbf x$, so
> $$\mathbf x^{\mathsf T}A\mathbf x=\tfrac12\mathbf x^{\mathsf T}(A+A^{\mathsf T})\mathbf x$$
> and $A+A^{\mathsf T}$ is symmetric. **Every quadratic form has a unique symmetric representative, and only that one has the right eigenvalues** — using a non-symmetric $A$ and reading off its eigenvalues is a standard error.

**The exact step size has a closed form.** Setting $\phi_k'(\alpha)=0$:

$$\boxed{\alpha_k=\frac{\mathbf g_k^{\mathsf T}\mathbf g_k}{\mathbf g_k^{\mathsf T}Q\,\mathbf g_k}},\qquad \mathbf x_{k+1}=\mathbf x_k-\frac{\mathbf g_k^{\mathsf T}\mathbf g_k}{\mathbf g_k^{\mathsf T}Q\,\mathbf g_k}\,\mathbf g_k$$

**No line search is needed for a quadratic** — which is why every convergence result in §5 is stated for quadratics and only then extended.

---

### 4. Fixed step size: exactly how large may $\alpha$ be?

> [!important] Theorem (C&Ż 8.3)
> For the quadratic $f$ above and $\mathbf x_{k+1}=\mathbf x_k-\alpha\mathbf g_k$ with $\alpha$ constant:
> $$\mathbf x_k\to\mathbf x^*\ \text{ for every }\mathbf x_0\qquad\Longleftrightarrow\qquad \boxed{0<\alpha<\frac{2}{\lambda_{\max}(Q)}}$$

**The necessity half is the illuminating one.** Since $\mathbf b=Q\mathbf x^*$,

$$\mathbf x_{k+1}-\mathbf x^*=\mathbf x_k-\mathbf x^*-\alpha Q(\mathbf x_k-\mathbf x^*)=(I-\alpha Q)(\mathbf x_k-\mathbf x^*)=(I-\alpha Q)^{k+1}(\mathbf x_0-\mathbf x^*)$$

**Gradient descent on a quadratic is exactly repeated multiplication by $I-\alpha Q$.** Start with $\mathbf x_0-\mathbf x^*$ an eigenvector of $Q$ for $\lambda_{\max}$ and

$$\lVert\mathbf x_{k+1}-\mathbf x^*\rVert=\lvert1-\alpha\lambda_{\max}\rvert^{\,k+1}\lVert\mathbf x_0-\mathbf x^*\rVert$$

which diverges unless $\lvert1-\alpha\lambda_{\max}\rvert<1$, i.e. $0<\alpha<2/\lambda_{\max}$. $\blacksquare$

> [!important] The eigenvalue reading — this is the whole mechanism
> In the eigenbasis of $Q$, the error component along eigenvector $i$ is multiplied by $(1-\alpha\lambda_i)$ every step, **independently of the others.** So:
>
> | | requires |
> |---|---|
> | **Stability** (no direction blows up) | $\alpha<2/\lambda_{\max}$ — **set by the *steepest* direction** |
> | **Speed** (the slowest direction shrinks) | $\alpha$ large — but capped by the line above |
>
> **The steepest direction limits the step and the flattest direction sets the speed, and $\kappa$ is the ratio between them.** That single sentence is why §5's rate is what it is.
>
> **The optimal fixed step balances the two extremes**, making $1-\alpha\lambda_{\min}=-(1-\alpha\lambda_{\max})$:
> $$\alpha^\star=\frac{2}{\lambda_{\min}+\lambda_{\max}}\qquad\text{giving contraction }\ \frac{\kappa-1}{\kappa+1}\ \text{ per step in }\lVert\mathbf x_k-\mathbf x^*\rVert$$

> [!example]- Worked example (C&Ż 8.4) — verified
> For $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}\begin{pmatrix}8&2\sqrt2\\2\sqrt2&10\end{pmatrix}\mathbf x+\dots$, the eigenvalues are $6$ and $12$ (trace $18$, determinant $80-8=72=6\times12$). **So the fixed-step method converges from every $\mathbf x_0$ iff $0<\alpha<2/12=1/6$.**
>
> *(The optimal fixed step would be $2/18=1/9$, with per-step contraction $(2-1)/(2+1)=1/3$ since $\kappa=2$.)*

**In machine learning this theorem is the learning rate.** $\alpha\ge2/\lambda_{\max}$ is exactly the regime where training loss diverges, and $\lambda_{\max}$ of the loss Hessian is what sets the "maximum stable learning rate" that practitioners find by trial and error.

---

### 5. **Convergence rate and the condition number**

Work with $V(\mathbf x)=\tfrac12(\mathbf x-\mathbf x^*)^{\mathsf T}Q(\mathbf x-\mathbf x^*)$, which differs from $f$ by a constant.

> [!important] Lemma (C&Ż 8.1 / L&Y Lemma 2) — exact, not a bound
> For steepest descent on the quadratic,
> $$V(\mathbf x_{k+1})=\left(1-\frac{(\mathbf g_k^{\mathsf T}\mathbf g_k)^2}{(\mathbf g_k^{\mathsf T}Q\mathbf g_k)(\mathbf g_k^{\mathsf T}Q^{-1}\mathbf g_k)}\right)V(\mathbf x_k)$$
>
> **Everything now depends on bounding that Rayleigh-type quotient below.**

> [!important] Kantorovich's inequality
> For $Q=Q^{\mathsf T}\succ0$ with extreme eigenvalues $a=\lambda_{\min}$, $A=\lambda_{\max}$, and any $\mathbf x\ne\mathbf 0$:
> $$\frac{(\mathbf x^{\mathsf T}\mathbf x)^2}{(\mathbf x^{\mathsf T}Q\mathbf x)(\mathbf x^{\mathsf T}Q^{-1}\mathbf x)}\ \ge\ \frac{4aA}{(a+A)^2}$$

> [!important] **Theorem (Steepest descent, quadratic case)**
> For every $\mathbf x_0$, steepest descent converges to $\mathbf x^*$, and at every step
> $$\boxed{V(\mathbf x_{k+1})\ \le\ \left(\frac{A-a}{A+a}\right)^2V(\mathbf x_k)=\left(\frac{\kappa-1}{\kappa+1}\right)^2V(\mathbf x_k)},\qquad \kappa:=\frac{\lambda_{\max}(Q)}{\lambda_{\min}(Q)}$$
>
> **Proof.** Combine the Lemma and Kantorovich: $1-\dfrac{4aA}{(A+a)^2}=\dfrac{(A-a)^2}{(A+a)^2}$. $\blacksquare$

> [!warning] Two books, two bounds, and the difference matters
> **Chong & Żak (Theorem 8.4) prove the weaker bound**
> $$V(\mathbf x_{k+1})\le\left(1-\frac1\kappa\right)V(\mathbf x_k)$$
> using only Rayleigh's inequality. **Luenberger & Ye (Theorem 2, §8.2) prove the Kantorovich bound above**, which is strictly sharper: at $\kappa=10$, $1-1/\kappa=0.900$ against $\left(\frac{9}{11}\right)^2=0.669$.
>
> **These notes use the Kantorovich bound**, because it is standard, because it is tight, and because — as Exercise 4 shows — **it is actually attained.** The weaker bound is not wrong, merely loose.

> [!important] $\kappa$ is the condition number, and it is the only thing that matters
> $$\kappa=\frac{\lambda_{\max}}{\lambda_{\min}}=\lVert Q\rVert\,\lVert Q^{-1}\rVert\ \ge\ 1$$
>
> | $\kappa$ | Contraction per step | **Iterations for 6 digits** |
> |---|---|---|
> | $1$ | $0$ | **1** (exact in one step) |
> | $2$ | $0.111$ | $7$ |
> | $10$ | $0.669$ | $35$ |
> | $100$ | $0.9608$ | $346$ |
> | $1000$ | $0.99601$ | $3\,454$ |
> | $10^4$ | $0.99960$ | $34\,539$ |
>
> **The count grows linearly in $\kappa$: roughly $3.45\,\kappa$ iterations for six digits.** *(Since $-\ln\left(\frac{\kappa-1}{\kappa+1}\right)^2\approx4/\kappa$ for large $\kappa$, the count is $\approx\frac{6\ln10}{4/\kappa}=3.45\kappa$.)*
>
> **This is the practical meaning of "gradient descent is slow"** — not that the rate is linear rather than quadratic, but that the *ratio* is within $O(1/\kappa)$ of $1$. Compare [[01 - The Optimization Problem|ch. 01]] §6: a ratio of $0.9996$ is technically linear convergence and practically a stall.

> [!warning] A single bad eigenvalue is enough
> **$\kappa$ is a ratio of extremes and ignores everything in between.** If $n-1$ eigenvalues are equal and one is far away, $\kappa$ is huge and convergence is slow, even though the problem is "almost" perfectly conditioned. **One abnormal eigenvalue destroys steepest descent** — Luenberger & Ye say this explicitly, and it is why real loss surfaces with a few very flat directions are so hard.

---

### 6. The zig-zag, geometrically

The level sets of the quadratic are ellipsoids whose axes point along the eigenvectors of $Q$, with **the axis for eigenvalue $\lambda_i$ having length $\propto1/\sqrt{\lambda_i}$.** So

$$\kappa\ \text{large}\quad\Longleftrightarrow\quad\text{the ellipsoids are eccentric}\quad\Longleftrightarrow\quad\text{a long narrow valley}$$

**Why the method zig-zags.** In a narrow valley the gradient points mostly *across* the valley, not along it — the steep walls dominate the shallow floor. Steepest descent crosses to the other wall, and by Proposition 1 the next step is perpendicular, crossing back. **The iterates bounce between the walls and creep along the floor.**

$$\kappa=1:\ \text{circular contours},\ \nabla f\ \text{points at the centre},\ \textbf{one step suffices}$$

> [!note] Chong & Żak's two-line demonstration
> $f(x_1,x_2)=x_1^2+x_2^2$ has $\kappa=1$ and steepest descent solves it in **one** step from any $\mathbf x_0$.
>
> $f(x_1,x_2)=\dfrac{x_1^2}{5}+x_2^2$ has $\kappa=5$ and the method "shuffles ineffectively back and forth in a narrow valley."
>
> **Same algorithm, same dimension, same smoothness. Only $\kappa$ changed.**

---

### 7. What to do about $\kappa$ — and where chapters 06–08 come from

**Since $\kappa$ is a property of the coordinate system as much as of the problem, change coordinates.**

Substituting $\mathbf x=T\mathbf y$ turns $Q$ into $T^{\mathsf T}QT$. Choosing $T$ to make $T^{\mathsf T}QT$ well conditioned is **preconditioning**, and in the ideal case $T=Q^{-1/2}$ gives $T^{\mathsf T}QT=I$, $\kappa=1$, **convergence in one step.**

> [!important] Every method in chapters 06–07 is a preconditioner in disguise
> | Method | Effective preconditioner | Cost |
> |---|---|---|
> | Steepest descent | $I$ — none | $O(n)$ |
> | **Diagonal scaling / feature standardisation** | $\operatorname{diag}(Q)^{-1}$ | $O(n)$ |
> | **Conjugate gradient** ([[07 - Conjugate Direction Methods\|ch. 07]]) | builds $Q$-conjugate directions implicitly | $O(n)$ |
> | **Quasi-Newton / BFGS** ([[06 - Newton and Quasi-Newton Methods\|ch. 06]]) | an accumulated approximation to $Q^{-1}$ | $O(n^2)$ |
> | **Newton** ([[06 - Newton and Quasi-Newton Methods\|ch. 06]]) | $Q^{-1}$ exactly | $O(n^3)$ |
>
> **Newton's method is steepest descent with $\kappa$ set to 1** — that is the whole reason it converges quadratically, and the whole reason it costs $O(n^3)$.

> [!tip] The data-science translation: **this is why you standardise your features**
> For least squares, $Q=X^{\mathsf T}X$, so $\kappa(Q)=\kappa(X)^2$. **If one feature is measured in millimetres and another in kilometres, $\kappa$ is enormous and gradient descent crawls** — and the fix costs one line:
> $$x_j\leftarrow\frac{x_j-\bar x_j}{s_j}$$
> **Feature standardisation is a diagonal preconditioner.** It is usually presented as a statistical nicety; **it is really this theorem.** *(And $\kappa(X^{\mathsf T}X)=\kappa(X)^2$ is also why one should never form the normal equations numerically — see [[08 - Least Squares and Linear Equations|ch. 08]].)*
>
> **The same theorem explains ridge regression's third benefit** from [[02 - Convex Sets and Convex Functions|ch. 02]]: adding $\lambda I$ moves $\kappa$ from $\lambda_{\max}/\lambda_{\min}$ to $(\lambda_{\max}+\lambda)/(\lambda_{\min}+\lambda)$, which is strictly smaller. **Regularisation *is* preconditioning.**

---

### 8. What modern practice actually does — **and what these books do not contain**

> [!warning] None of the four textbooks in this folder covers stochastic gradient descent
> **The algorithms in §§2–5 are deterministic and full-batch**: every step evaluates $\nabla f$ on all the data. **At $n=10^6$ parameters and $10^7$ training examples that is impossible**, and no book here addresses it. **This section is my own addition** and is flagged as such.

**The modification is small and its consequences are large.** Write $f(\mathbf x)=\frac1N\sum_{i=1}^N f_i(\mathbf x)$ — an average over training examples. **Stochastic gradient descent** replaces $\nabla f$ by the gradient of a random sample:

$$\mathbf x_{k+1}=\mathbf x_k-\alpha_k\nabla f_{i_k}(\mathbf x_k),\qquad i_k\ \text{drawn at random}$$

$\mathbb E[\nabla f_{i_k}]=\nabla f$, so **the step is right on average and wrong every time.**

> [!important] What survives the change to stochastic gradients, and what does not
> | Result of this chapter | Survives? |
> |---|---|
> | $-\nabla f$ is the steepest descent direction (§1) | ✔ in expectation |
> | **Descent property $f(\mathbf x_{k+1})<f(\mathbf x_k)$** (§3) | ✘ **fails** — SGD routinely increases the loss |
> | Exact line search (§3) | ✘ meaningless — there is no $\phi_k$ to minimise |
> | **Stability requires $\alpha<2/\lambda_{\max}$** (§4) | ✔ **essentially intact** — this is the learning-rate ceiling |
> | Linear convergence at rate $\left(\frac{\kappa-1}{\kappa+1}\right)^2$ (§5) | ✘ **replaced by $O(1/k)$** — the gradient noise does not vanish |
> | $\kappa$ governs difficulty (§5–7) | ✔ **and more strongly than before** |
>
> **The rate loss is the fundamental one.** A constant step size makes SGD converge only to a *noise ball* around $\mathbf x^*$ whose radius is $O(\alpha)$. To converge exactly, the steps must decay under the **Robbins–Monro conditions**
> $$\sum_k\alpha_k=\infty\qquad\text{(steps sum to enough distance)}\qquad\qquad \sum_k\alpha_k^2<\infty\qquad\text{(noise is summable)}$$
> — satisfied by $\alpha_k=c/k$ but **not** by $\alpha_k=$ const. **This is what a learning-rate schedule is, and why every training run has one.**

**The two standard repairs, both readable as fixes to problems in this chapter:**

| Method | Update | Fixes |
|---|---|---|
| **Momentum** | $\mathbf v_{k+1}=\beta\mathbf v_k+\mathbf g_k$, $\ \mathbf x_{k+1}=\mathbf x_k-\alpha\mathbf v_{k+1}$ | **the zig-zag of §6.** Oscillating components cancel across steps; consistent ones accumulate. Improves the $\kappa$-dependence from $O(\kappa)$ to $O(\sqrt\kappa)$ |
| **Adam / RMSProp** | per-coordinate $\alpha$ scaled by $1/\sqrt{\text{running mean of }g_j^2}$ | **the conditioning of §7.** It is an *adaptive diagonal preconditioner* estimated from the gradient history |

> [!important] The honest summary
> **Adam is not a new idea; it is §7's diagonal preconditioner with the scaling estimated online, applied to §8's stochastic gradients.** Momentum is a device for the §6 zig-zag. **Everything a modern optimizer does is a response to a phenomenon in this chapter** — which is why the chapter is worth reading even though its algorithms are not the ones you will run.
>
> **What is genuinely missing from the classical theory is the non-convexity**, not the stochasticity. [[02 - Convex Sets and Convex Functions|Chapter 02]] §6 is what fails for a neural network, and no amount of momentum repairs it.

---

## ✏️ Exercises

> [!question] Exercise 1 — steepest descent on a quadratic, by hand *(easy)*
> Let $f(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x$ with $Q=\operatorname{diag}(1,10)$ and $\mathbf x_0=(1,1)^{\mathsf T}$.
> **(a)** Compute $\alpha_0$ from the closed form and find $\mathbf x_1$.
> **(b)** Compute $\alpha_1$ and $\mathbf x_2$, and verify that the two steps are orthogonal.
> **(c)** What is $\kappa$, and what does the theorem of §5 predict? What is the actual ratio?

> [!example]- Solution
> **(a)** $\mathbf g_0=Q\mathbf x_0=(1,10)^{\mathsf T}$.
> $$\alpha_0=\frac{\mathbf g_0^{\mathsf T}\mathbf g_0}{\mathbf g_0^{\mathsf T}Q\mathbf g_0}=\frac{1+100}{1+1000}=\frac{101}{1001}=0.100899$$
> $$\mathbf x_1=\mathbf x_0-\alpha_0\mathbf g_0=(1,1)-0.100899(1,10)=\boxed{(0.899101,\ -0.008991)}$$
> *(This is the same computation as [[04 - One-Dimensional Search Methods|ch. 04]]'s Exercise 5 — the exact line search on this $f$.)*
>
> **(b)** $\mathbf g_1=Q\mathbf x_1=(0.899101,\ -0.089910)^{\mathsf T}$.
> $$\alpha_1=\frac{0.899101^2+0.089910^2}{0.899101^2+10(0.089910)^2}=0.918182,\qquad \mathbf x_2=\boxed{(0.073563,\ 0.073563)}$$
>
> **Orthogonality:** $\mathbf x_1-\mathbf x_0=(-0.100899,\ -1.008991)$ and $\mathbf x_2-\mathbf x_1=(-0.825538,\ 0.082554)$.
> $$\langle\cdot,\cdot\rangle=(-0.100899)(-0.825538)+(-1.008991)(0.082554)=0.083297-0.083297=0\ \checkmark$$
> *(Verified numerically to $2.6\times10^{-16}$.)*
>
> **(c)** $\kappa=10/1=10$, so the theorem predicts
> $$\frac{V(\mathbf x_{k+1})}{V(\mathbf x_k)}\le\left(\frac{9}{11}\right)^2=0.669421$$
> **Actual:** $V(\mathbf x_0)=5.5$, $V(\mathbf x_1)=0.404595$, giving a ratio of $\boxed{0.073563}$ — **nine times better than the bound.**
>
> **The bound is not tight here, and Exercise 4 explains why: this starting point is lucky.** *(Notice also that the ratio is exactly $0.073563$ at every subsequent step too, and that $x_2$ has returned to the diagonal $x_1=x_2$ — the iteration is self-similar, contracting by a fixed factor with period 2. That periodicity is the zig-zag.)*

---

> [!question] Exercise 2 — the fixed step size *(easy–medium)*
> With the same $f$ and $Q=\operatorname{diag}(1,10)$, use $\mathbf x_{k+1}=\mathbf x_k-\alpha\mathbf g_k$ with $\alpha$ constant.
> **(a)** For which $\alpha$ does the method converge from every $\mathbf x_0$?
> **(b)** What is the best fixed $\alpha$, and what contraction does it give?
> **(c)** What happens at $\alpha=0.2$ exactly, and at $\alpha=0.21$?
> **(d)** Relate all this to the learning rate of a training run.

> [!example]- Solution
> **(a)** By §4's theorem, $0<\alpha<2/\lambda_{\max}=2/10=\boxed{0.2}$.
>
> **(b)** The error components contract by $\lvert1-\alpha\rvert$ and $\lvert1-10\alpha\rvert$. Minimising the larger of the two means equalising them with opposite signs:
> $$1-\alpha=-(1-10\alpha)\ \Longrightarrow\ \alpha^\star=\frac{2}{1+10}=\frac{2}{11}=\boxed{0.181818}$$
> giving contraction $\left\lvert1-\tfrac2{11}\right\rvert=\tfrac9{11}=0.8182=\dfrac{\kappa-1}{\kappa+1}$ per step **in $\lVert\mathbf x_k-\mathbf x^*\rVert$** — equivalently $\left(\tfrac9{11}\right)^2$ in $V$, matching §5. *(Verified: from $(1,1)$, 200 steps give $\lVert\mathbf x\rVert=5.3\times10^{-18}$.)*
>
> **(c)**
> - **$\alpha=0.2$ exactly:** the $\lambda_{\max}$ component is multiplied by $1-0.2(10)=-1$ every step. **The iterate oscillates forever without converging or diverging** — verified: after 200 steps $\lVert\mathbf x\rVert=1.000$ exactly. **This is why the theorem's inequality is strict.**
> - **$\alpha=0.21$:** the factor is $-1.1$, so that component grows by 10% per step. After 200 steps $\lVert\mathbf x\rVert=1.9\times10^8$ — **divergence**, and the divergence is entirely in the *steepest* direction.
>
> **(d)** This is the learning rate, exactly.
>
> | Observation in training | Explanation from (a)–(c) |
> |---|---|
> | "The loss went to NaN" | $\alpha>2/\lambda_{\max}$ — divergence along the sharpest curvature direction |
> | "The loss oscillates without improving" | $\alpha\approx2/\lambda_{\max}$ — the boundary case of (c) |
> | "Training is stable but glacially slow" | $\alpha\ll\alpha^\star$, or $\alpha^\star$ itself is small because $\kappa$ is large |
> | "Halving the learning rate fixed it" | moved $\alpha$ back inside $(0,2/\lambda_{\max})$ |
> | "Learning-rate warmup helped" | $\lambda_{\max}$ is largest early in training, so the ceiling starts low and rises |
>
> **The maximum stable learning rate is $2/\lambda_{\max}$ of the loss Hessian, and it is found empirically because $\lambda_{\max}$ is not computable at scale.** *(In deep learning this is the "edge of stability" phenomenon: training tends to sit at $\lambda_{\max}\approx2/\alpha$, right at the boundary.)*

---

> [!question] Exercise 3 — how bad is a bad condition number? *(medium)*
> **(a)** Derive the number of steepest-descent iterations needed to reduce the error by a factor $10^{-6}$, as a function of $\kappa$.
> **(b)** Tabulate it for $\kappa=1,2,10,10^2,10^3,10^4$.
> **(c)** Show that for large $\kappa$ the count is $\approx3.45\,\kappa$.
> **(d)** A design matrix $X$ has $\kappa(X)=10^3$. What is $\kappa(X^{\mathsf T}X)$, and what does that mean for fitting by gradient descent?

> [!example]- Solution
> **(a)** With contraction $c=\left(\dfrac{\kappa-1}{\kappa+1}\right)^2$ per step, we need $c^{\,m}\le10^{-6}$, i.e.
> $$m\ \ge\ \frac{6\ln10}{-\ln c}=\frac{6\ln10}{-2\ln\!\left(\frac{\kappa-1}{\kappa+1}\right)}$$
>
> **(b)**
>
> | $\kappa$ | $c=\left(\frac{\kappa-1}{\kappa+1}\right)^2$ | Iterations $m$ |
> |---|---|---|
> | $1$ | $0$ | $1$ |
> | $2$ | $0.1111$ | $7$ |
> | $10$ | $0.6694$ | $35$ |
> | $100$ | $0.96079$ | $346$ |
> | $1000$ | $0.996008$ | $3\,454$ |
> | $10^4$ | $0.9996000$ | $34\,539$ |
>
> **(c)** For large $\kappa$, $\ln\dfrac{\kappa-1}{\kappa+1}=\ln\!\left(1-\dfrac{2}{\kappa+1}\right)\approx-\dfrac{2}{\kappa}$, so $-\ln c\approx\dfrac4\kappa$ and
> $$m\approx\frac{6\ln10}{4/\kappa}=\frac{6\ln10}{4}\,\kappa=3.4539\,\kappa$$
> **Checking against the table: $3.4539\times10^3=3454$ ✔ and $3.4539\times10^4=34\,539$ ✔ — exact to four figures.**
>
> **$m$ is linear in $\kappa$, so a ten-fold worsening of the conditioning costs a ten-fold increase in iterations.** *(Contrast conjugate gradient, [[07 - Conjugate Direction Methods|ch. 07]], where the count goes as $\sqrt\kappa$ — for $\kappa=10^4$ that is 100 times fewer iterations.)*
>
> **(d)** $$\kappa(X^{\mathsf T}X)=\kappa(X)^2=10^6$$
> since the eigenvalues of $X^{\mathsf T}X$ are the squared singular values of $X$. By (c), gradient descent on $\lVert\mathbf y-X\boldsymbol\beta\rVert^2$ would need
> $$m\approx3.45\times10^6\ \text{iterations}$$
> for six digits. **Three and a half million passes over the data to fit a linear regression.**
>
> **Three consequences, all of them standard practice explained by one theorem:**
> 1. **Never fit least squares by gradient descent when you can factorise.** QR or SVD on $X$ works with $\kappa(X)=10^3$, not $\kappa(X)^2=10^6$ — this is [[08 - Least Squares and Linear Equations|ch. 08]]'s central point.
> 2. **Standardise the features.** Much of a large $\kappa(X)$ is usually just differing units, and §7's diagonal preconditioner removes it for $O(n)$ work.
> 3. **Add a ridge penalty.** $\kappa(X^{\mathsf T}X+\lambda I)=\dfrac{\sigma_{\max}^2+\lambda}{\sigma_{\min}^2+\lambda}$, which for $\lambda$ comparable to $\sigma_{\min}^2$ cuts $\kappa$ by orders of magnitude.

---

> [!question] Exercise 4 — is the bound tight? *(hard)*
> The theorem of §5 is an inequality. Exercise 1 found a ratio of $0.0736$ against a bound of $0.6694$ — a factor of nine.
> **(a)** Using the exact Lemma, write the ratio as a function of $\mathbf g_k$ and find exactly when Kantorovich holds with **equality**, for $Q=\operatorname{diag}(a,A)$ in $\mathbb R^2$.
> **(b)** Translate that into a condition on $\mathbf x_k$ for $Q=\operatorname{diag}(1,10)$, and verify.
> **(c)** Why was $\mathbf x_0=(1,1)$ so lucky?
> **(d)** What does this say about how to read the theorem?

> [!example]- Solution
> **(a)** By the Lemma the exact ratio is
> $$\frac{V(\mathbf x_{k+1})}{V(\mathbf x_k)}=1-\frac{(\mathbf g^{\mathsf T}\mathbf g)^2}{(\mathbf g^{\mathsf T}Q\mathbf g)(\mathbf g^{\mathsf T}Q^{-1}\mathbf g)}$$
> With $Q=\operatorname{diag}(a,A)$ and $\mathbf g=(g_1,g_2)$, put $\xi_i=g_i^2/\lVert\mathbf g\rVert^2$ so $\xi_1+\xi_2=1$. The quotient becomes
> $$\frac{1}{(\xi_1a+\xi_2A)\left(\frac{\xi_1}{a}+\frac{\xi_2}{A}\right)}$$
> The Kantorovich proof shows the minimum over $\xi$ occurs at $\xi_1a+\xi_2A=\dfrac{a+A}{2}$ — **the convex combination of eigenvalues must land exactly halfway between them.** Solving,
> $$\xi_1a+\xi_2A=\frac{a+A}{2}\ \Longrightarrow\ \xi_1=\xi_2=\tfrac12\ \Longrightarrow\ \boxed{\lvert g_1\rvert=\lvert g_2\rvert}$$
>
> **The worst case is when the gradient has *equal components* along the extreme eigen-directions.** *(In $\mathbb R^n$: all the gradient's weight split evenly between the $\lambda_{\min}$ and $\lambda_{\max}$ eigenspaces, none in between.)*
>
> **(b)** Since $\mathbf g=Q\mathbf x$ gives $g_1=x_1$ and $g_2=10x_2$, the condition $\lvert g_1\rvert=\lvert g_2\rvert$ becomes
> $$\boxed{\lvert x_1\rvert=10\,\lvert x_2\rvert}$$
> **Verified**, starting from three such points:
>
> | $\mathbf x_0$ | ratio at every step |
> |---|---|
> | $(10,\ 1)$ | $0.669421$ |
> | $(10,\ -1)$ | $0.669421$ |
> | $(1,\ 0.1)$ | $0.669421$ |
> | $(1,\ 1)$ *(Exercise 1)* | $0.073563$ |
>
> **The bound $\left(\frac{9}{11}\right)^2=0.669421$ is attained exactly, and attained at every iteration — the algorithm stays on the worst case once it starts there.** *(That persistence is not an accident: the exact-line-search step preserves the ratio $\lvert g_1\rvert/\lvert g_2\rvert$ up to sign for a diagonal $Q$ in $\mathbb R^2$.)*
>
> **(c)** At $\mathbf x_0=(1,1)$ we get $\mathbf g_0=(1,10)$, so $\xi_2=\dfrac{100}{101}=0.990$ and
> $$\xi_1a+\xi_2A=\frac{1+1000}{101}=9.911$$
> which is nowhere near the worst-case value $\dfrac{a+A}{2}=5.5$. **The gradient is almost entirely in the $\lambda_{\max}$ direction, which is the *easy* case** — a gradient aligned with a single eigenvector is an eigenvector, and by C&Ż's Lemma 8.3 the method then converges **in one step** along that direction. $(1,1)$ is close to that happy situation.
>
> **(d) The theorem is a worst-case bound and the worst case is real.** Three consequences:
> 1. **You cannot rely on being lucky.** Akaike's result, quoted by Luenberger & Ye, is that when $\kappa$ is unfavourable the method converges *close to the bound* for almost all starting points. **The bound is the typical behaviour, not a pessimistic outlier.**
> 2. **A good ratio on one problem proves nothing.** Exercise 1's $0.0736$ would suggest gradient descent handles $\kappa=10$ effortlessly. It does not.
> 3. **The worst case is triggered by a gradient that splits its weight between the extremes** — which is exactly what happens in a valley, where the iterate has a large component along the steep direction *and* a persistent one along the flat one. **The zig-zag of §6 and the worst case of Kantorovich are the same phenomenon.**

---

> [!question] Exercise 5 — preconditioning, and why you standardise features *(medium–hard)*
> Continue with $f(\mathbf x)=\tfrac12(x_1^2+10x_2^2)$.
> **(a)** Substitute $\mathbf x=T\mathbf y$ with $T=\operatorname{diag}(1,1/\sqrt{10})$. Write $f$ in terms of $\mathbf y$ and find the new condition number.
> **(b)** How many steepest-descent steps does the transformed problem need?
> **(c)** Generalise: for what $T$ is $\kappa=1$ always achievable, and what does that $T$ cost?
> **(d)** A regression has features "age (years)" $\in[20,70]$ and "income (VND)" $\in[10^7,10^9]$. Estimate $\kappa(X^{\mathsf T}X)$ before standardisation, and explain the effect of standardising.
> **(e)** In what sense are Newton's method, BFGS and Adam all answers to this exercise?

> [!example]- Solution
> **(a)** With $x_1=y_1$ and $x_2=y_2/\sqrt{10}$,
> $$f=\tfrac12\left(y_1^2+10\cdot\frac{y_2^2}{10}\right)=\tfrac12(y_1^2+y_2^2)$$
> The new Hessian is $T^{\mathsf T}QT=I$, so $\boxed{\kappa=1}$. *(Verified: $T^{\mathsf T}QT=I$ exactly.)*
>
> **(b) One.** By §5's theorem the contraction is $\left(\frac{1-1}{1+1}\right)^2=0$, and directly: $\mathbf g=\mathbf y$, so $\alpha=\frac{\mathbf y^{\mathsf T}\mathbf y}{\mathbf y^{\mathsf T}\mathbf y}=1$ and $\mathbf y_1=\mathbf y_0-\mathbf y_0=\mathbf 0$. **Verified: from $\mathbf y_0=(1,\sqrt{10})$ the first step lands exactly on the minimizer.**
>
> **A problem that needed 35 iterations now needs 1, and nothing about it changed except the units of $x_2$.**
>
> **(c)** $T=Q^{-1/2}$ (from the spectral decomposition, [[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]) gives $T^{\mathsf T}QT=Q^{-1/2}QQ^{-1/2}=I$ for any $Q\succ0$.
>
> **The cost is the catch: computing $Q^{-1/2}$ needs the full eigendecomposition, $O(n^3)$ and $O(n^2)$ storage.** For $n=10^6$ that is $10^{18}$ operations — **more expensive than the $3.45\kappa$ iterations it would save, by a wide margin.** *(And for a non-quadratic $f$, $Q=\nabla^2f(\mathbf x)$ changes at every point, so it would have to be redone each step.)*
>
> **The entire design space of chapters 06–07 is: how much of $Q^{-1/2}$ can I afford?**
>
> **(d)** Take the two features' typical magnitudes as $10^{1.5}$ (age) and $10^{8}$ (income). Since $X^{\mathsf T}X$ has entries scaling as products of feature magnitudes, its diagonal entries differ by roughly
> $$\left(\frac{10^{8}}{10^{1.5}}\right)^{2}=10^{13}$$
> so $\kappa(X^{\mathsf T}X)\sim10^{13}$ — **wildly beyond anything gradient descent can handle** (Exercise 3 would predict $\sim10^{13}$ iterations), and beyond double-precision accuracy ($\approx10^{16}$) for solving the normal equations too.
>
> **After standardising**, both columns have mean 0 and variance 1, the diagonal of $X^{\mathsf T}X$ is constant, and $\kappa$ reduces to whatever genuine collinearity exists between age and income — typically a small number.
>
> **The point: almost all of the original $\kappa$ was an artefact of the units.** Standardisation is usually taught as a statistical convention; **it is the diagonal preconditioner of §7, and it is doing optimization work, not statistical work.** *(Note also that $\kappa$ is invariant to rotation but not to scaling — which is precisely why a diagonal fix is so effective and so cheap.)*
>
> **(e)** All three estimate a preconditioner under a different budget:
>
> | Method | Estimate of $Q^{-1}$ | Cost/step | Requires |
> |---|---|---|---|
> | **Feature standardisation** | $\operatorname{diag}(Q)^{-1}$, computed once from the data | $O(n)$, once | nothing |
> | **Adam** | $\operatorname{diag}$ built from a running mean of $g_j^2$ | $O(n)$ | nothing — **estimated online** |
> | **BFGS** | a rank-2-updated full matrix from gradient differences | $O(n^2)$ | gradient history |
> | **Newton** | $\nabla^2f(\mathbf x_k)^{-1}$ exactly | $O(n^3)$ | the Hessian |
>
> **Read down the table and the budget rises while the approximation improves.** Deep learning sits in the first two rows because $n$ is in the millions; classical optimization sits in the last two because $n$ is in the hundreds.
>
> **So Adam is not a fundamentally new algorithm. It is this exercise, solved online, with a diagonal budget.** *(And that also explains its known weakness: a diagonal preconditioner cannot fix ill-conditioning that lives in a rotated basis — if the bad directions are not aligned with the coordinate axes, no diagonal $T$ helps.)*

---

## 📝 Summary

- **$-\nabla f$ is the steepest descent direction by Cauchy–Schwarz**, but only for an infinitesimal step — and it depends on the coordinate system, which §7 exploits.
- **The algorithm is $\mathbf x_{k+1}=\mathbf x_k-\alpha_k\mathbf g_k$**, with $\alpha_k$ from an exact line search, a fixed constant, or Armijo backtracking.
- **Exact steepest descent makes consecutive steps orthogonal** ($\langle\mathbf g_k,\mathbf g_{k+1}\rangle=0$) and always decreases $f$. For a quadratic, $\alpha_k=\dfrac{\mathbf g_k^{\mathsf T}\mathbf g_k}{\mathbf g_k^{\mathsf T}Q\mathbf g_k}$ in closed form.
- **A fixed step converges from every $\mathbf x_0$ iff $0<\alpha<2/\lambda_{\max}$**, because the iteration is repeated multiplication by $I-\alpha Q$ and the error component along eigenvector $i$ is scaled by $(1-\alpha\lambda_i)$. **The best fixed step is $2/(\lambda_{\min}+\lambda_{\max})$.**
- **The rate is $\left(\dfrac{\kappa-1}{\kappa+1}\right)^2$ per step** (Kantorovich), with $\kappa=\lambda_{\max}/\lambda_{\min}$. **The bound is attained** — from any point where the gradient splits its weight evenly between the extreme eigen-directions.
- **Iterations for six digits $\approx3.45\,\kappa$**: 35 at $\kappa=10$, 346 at $100$, 34,539 at $10^4$. **A single abnormal eigenvalue is enough to ruin the method.**
- **Large $\kappa$ means eccentric level sets, and eccentric level sets mean zig-zag** — the gradient points across the valley, not along it.
- **Preconditioning fixes $\kappa$.** $T=Q^{-1/2}$ gives $\kappa=1$ and one-step convergence, at $O(n^3)$. **Feature standardisation is the cheap diagonal version, and ridge regularisation is another.** Newton, BFGS, CG and Adam are the same idea at four different budgets.
- **Stochastic gradients (not in any of these books) keep the stability ceiling and $\kappa$-dependence but destroy the descent property and the linear rate**, requiring a decaying schedule with $\sum\alpha_k=\infty$, $\sum\alpha_k^2<\infty$.

---

## ⚠️ Important Notes

> [!warning] The six errors
> 1. **Reading eigenvalues off a non-symmetric $Q$.** Symmetrise first: $\tfrac12(A+A^{\mathsf T})$.
> 2. **Using $\alpha\ge2/\lambda_{\max}$.** Divergence, and it starts in the steepest direction. At exactly $2/\lambda_{\max}$ you get permanent oscillation.
> 3. **Confusing the two convergence bounds.** Chong & Żak's $1-1/\kappa$ and Kantorovich's $\left(\frac{\kappa-1}{\kappa+1}\right)^2$ are both valid; the second is sharp.
> 4. **Concluding from one good run that the bound is pessimistic.** Exercise 4: the bound is attained, and Akaike's result says it is typical when $\kappa$ is bad.
> 5. **Applying the quadratic rate to a general $f$ far from $\mathbf x^*$.** These are local results with $Q=\nabla^2f(\mathbf x^*)$.
> 6. **Forgetting $\kappa(X^{\mathsf T}X)=\kappa(X)^2$.** Forming the normal equations squares the conditioning — the reason [[08 - Least Squares and Linear Equations|ch. 08]] prefers QR.

> [!tip] The chapter in one diagram
> ```
>                    κ = λmax / λmin
>                          │
>        ┌─────────────────┼─────────────────┐
>        │                 │                 │
>    κ small           κ large          κ enormous
>        │                 │                 │
>   converges in       zig-zag,          hopeless:
>   a few steps       ~3.45κ iters      standardise,
>                                       regularise, or
>                                       change method
> ```
> **Before blaming the optimizer, compute (or estimate) $\kappa$.** Most "gradient descent doesn't work" problems are conditioning problems with a one-line fix.

> [!note] Where this chapter is used
> - **[[06 - Newton and Quasi-Newton Methods|Ch. 06]]** and **[[07 - Conjugate Direction Methods|ch. 07]]** exist entirely to beat the $\kappa$-dependence: CG reduces it to $\sqrt\kappa$, Newton removes it.
> - **[[08 - Least Squares and Linear Equations|Ch. 08]]** — $\kappa(X^{\mathsf T}X)=\kappa(X)^2$ is why least squares is solved by factorisation, not by the normal equations.
> - **[[02 - Convex Sets and Convex Functions|Ch. 02]]** — ridge regularisation's third benefit, improving $\kappa$, is this chapter's theorem.
> - **[[Machine Learning/contents/00-Index|Machine Learning]]** — §8 is the bridge: learning rate $=\alpha$, learning-rate schedule $=$ Robbins–Monro, Adam $=$ diagonal preconditioner.
> - **[[Econometrics/contents/00-Index|Econometrics]]** — **multicollinearity *is* a large $\kappa$**, and the instability of the OLS coefficients it causes is the statistical face of the same matrix fact.
> - **[[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]** supplies Rayleigh's inequality, the spectral decomposition, and $Q^{-1/2}$.

---

> [!warning] Gaps in the source material
> **Source split.** Structure and the algorithm follow **Chong & Żak ch. 8**; **the convergence theorem is Luenberger & Ye's** (§8.2), because it is the sharp one and because their extraction is clean.
>
> **The one substantive divergence between the two books, and it is not an error in either.** Chong & Żak's Theorem 8.4 gives $V(\mathbf x_{k+1})\le\left(1-\frac1\kappa\right)V(\mathbf x_k)$, derived from Rayleigh's inequality alone. Luenberger & Ye's Theorem 2 gives $\left(\frac{\kappa-1}{\kappa+1}\right)^2$, derived from **Kantorovich's inequality**, which Chong & Żak never state. **At $\kappa=10$ these are $0.900$ and $0.669$.** Both are correct upper bounds; **only the second is attained** (Exercise 4 verifies attainment). **These notes use Luenberger & Ye's and say so at the point of use** — a student comparing the two books would otherwise think one of them is wrong.
>
> **Chong & Żak OCR damage:**
> - **`ak`, `α^`, `afc`, `<*fc`, `ctk`, `α&` are all $\alpha_k$**; `gW`, `g^`, `g(k)`, `flfW`, `β(*+ΐ)` are $\mathbf g^{(k)}$ or $\mathbf x^{(k+1)}$; `7fc` and `7^` are $\gamma_k$; `Amax`, `Amin`, `Xmin` are $\lambda_{\max},\lambda_{\min}$; `r` is used for $\kappa$.
> - **Every displayed fraction collapses.** The closed-form step size arrives as `Oik = gWTQg(k)'` with the numerator on a previous line; Lemma 8.1's $\gamma_k$ is spread across three fragments. **All formulas were reconstructed and re-derived.**
> - **The quadratic in Example 8.4 is unreadable** — `f{X)=xAi 2fL+xTM+24` — **but the symmetrised matrix $\begin{psmallmatrix}8&2\sqrt2\\2\sqrt2&10\end{psmallmatrix}$ survives and is self-checking**: trace $18$ and determinant $80-8=72$ give eigenvalues $6$ and $12$, exactly as printed.
> - **Figures 8.1–8.7 are all images and all lost.** The losses are severe: **Figure 8.2 (the orthogonal-step staircase), Figure 8.6 (circular contours, one-step convergence) and Figure 8.7 (the narrow-valley zig-zag)** are the pictures that *are* §§3 and 6. Figures 8.3–8.5 (plots of $\phi_k(\alpha)$ for Example 8.1) are also gone.
>
> **Luenberger & Ye extracts cleanly**, including the Kantorovich proof and Theorem 2, with two artefacts: `Q−l` for $Q^{-1}$ in Lemma 2, and `/enc-118` marking the end of each proof.
>
> **Verification performed.** Every number was recomputed with `numpy`:
> - **C&Ż Example 8.1** (steepest descent on $(x_1-4)^4+(x_2-3)^2+4(x_3+5)^4$): all three step sizes reproduce — $\alpha_0=3.967\times10^{-3}$, $\alpha_1=0.5000$, $\alpha_2=16.29$ — and so do all three iterates, ending at $(4.000,\ 3.000,\ -5.003)$ against the printed $(4.000,\ 3.000,\ -5.002)$ *(a hand-rounding difference in the last digit)*.
> - **C&Ż Example 8.4**: eigenvalues exactly $6$ and $12$, so the range $0<\alpha<1/6$ is right.
> - **C&Ż Example 8.7**: $x^{(k)}=(1/2)^{2^k-1}$ verified term by term, order of convergence $2$.
> - **L&Y's $4\times4$ example**: eigenvalues $\{0.52,\ 0.76,\ 0.88,\ 0.94\}$, so $a=0.52$ and $A=0.94$ as printed. **The book's $r=1.8$ is rounded** — the exact value is $1.8077$, and the exact ratio is $0.0828$ rather than the printed $0.081$, which is what $r=1.8$ gives. **A rounding presentation, not an error.**
> - **Exercises 1–5**: all step sizes, iterates, orthogonality checks (to $2.6\times10^{-16}$), the full $\kappa$/iteration table, the divergence behaviour at $\alpha=0.2$ and $0.21$, and the attainment of the Kantorovich bound from $(10,1)$, $(10,-1)$ and $(1,0.1)$ — **all confirming $0.669421$ exactly at every step.**
>
> **No mathematical error was found in either book in these chapters.**
>
> **Scope and additions.**
> - **§8 (stochastic gradients, momentum, Adam, Robbins–Monro) is entirely my own addition and is not in any of the four textbooks in this folder.** It is included because **the gap is not cosmetic**: a Data Science reader will run SGD and Adam and never run exact steepest descent, and leaving the connection unstated would make the chapter look irrelevant when it is in fact the foundation. **The table of what survives and what fails under stochasticity is mine**, and readers should treat it as a summary of standard modern results (Robbins–Monro 1951; Bottou et al.) rather than as anything derived here.
> - **§7's preconditioning table and the reading of Newton/BFGS/CG/Adam as four budgets for approximating $Q^{-1/2}$ is my own framing.** Luenberger & Ye discuss scaling in §10.6 and Chong & Żak not at all; **neither connects it to feature standardisation**, which is the form a DS reader will meet it in.
> - **The $\kappa$-versus-iterations table and the $m\approx3.45\kappa$ asymptotic are my own**, computed and checked. Both books state the ratio and neither converts it into a number of iterations, which is what makes the result concrete.
> - **Exercise 4 (attainment of the bound) is my own**, including the derivation that the worst case requires $\lvert g_1\rvert=\lvert g_2\rvert$. The books assert sharpness — Luenberger & Ye cite Akaike — without exhibiting a worst-case starting point.
> - **Exercise 2(d)'s translation table into training diagnostics is mine**, as is the "edge of stability" remark.

#optimization #gradient-descent #steepest-descent #condition-number #kantorovich #convergence-rate #preconditioning #learning-rate #sgd #adam
