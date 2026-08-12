---
subject: Optimization
chapter: 03
tags: [ds, optimization, fonc, sonc, sosc, feasible-direction, hessian, stationary-point]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 6"
---

# Unconstrained Optimality Conditions

> [!abstract] What this chapter is for
> **[[01 - The Optimization Problem|Chapter 01]] asked what a minimizer is. This chapter asks how you would recognise one.**
>
> The answer comes in three conditions of increasing strength, and **the gap between "necessary" and "sufficient" is the whole story:**
>
> | Condition | Says | Status |
> |---|---|---|
> | **FONC** | $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$ for every feasible direction; **$\nabla f(\mathbf x^*)=\mathbf 0$ if $\mathbf x^*$ is interior** | **Necessary, never sufficient** |
> | **SONC** | if additionally $\mathbf d^{\mathsf T}\nabla f=0$, then $\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\mathbf d\ge0$ | **Necessary, never sufficient** |
> | **SOSC** | $\nabla f(\mathbf x^*)=\mathbf 0$ **and** $\nabla^2f(\mathbf x^*)\succ0$ | **Sufficient, not necessary** |
>
> **Nothing here is both.** Necessary conditions generate candidates and eliminate impostors; the sufficient condition confirms some of the survivors and is silent about the rest. **Closing the gap entirely requires [[02 - Convex Sets and Convex Functions|convexity]]** — which is why chapter 02 came first.
>
> **The subtlety worth the effort is §1–§2: on a *constrained* set the first-order condition is not $\nabla f=\mathbf 0$.** That is a special case, valid only in the interior, and using it on a boundary is the standard error.

---

## 📘 Main Knowledge

### 1. Feasible directions and the directional derivative

> [!important] Definition (C&Ż 6.2)
> A vector $\mathbf d\in\mathbb R^n$, $\mathbf d\ne\mathbf 0$, is a **feasible direction at $\mathbf x\in\Omega$** if there exists $\alpha_0>0$ such that
> $$\mathbf x+\alpha\mathbf d\in\Omega\quad\text{for all }\alpha\in[0,\alpha_0]$$
>
> **In words: you can take at least a short step in that direction without leaving the feasible set.**

**Where you stand determines which directions are feasible:**

| Position | Feasible directions |
|---|---|
| **Interior point** | **all** of $\mathbb R^n\setminus\{\mathbf 0\}$ |
| On a boundary face $x_i\ge0$ with $x_i=0$ | those with $d_i\ge0$ |
| At a corner of $\{\mathbf x\ge\mathbf 0\}$ | those with $\mathbf d\ge\mathbf 0$ |
| On a curved equality set like $\{x_1^2+x_2^2=1\}$ | **none at all** |

**That last row is not a curiosity — it is a warning, and §3 develops it.**

**The directional derivative** of $f$ at $\mathbf x$ in the direction $\mathbf d$ is
$$\frac{\partial f}{\partial\mathbf d}(\mathbf x)=\lim_{\alpha\to0}\frac{f(\mathbf x+\alpha\mathbf d)-f(\mathbf x)}{\alpha}=\boxed{\mathbf d^{\mathsf T}\nabla f(\mathbf x)}$$

The boxed identity is the chain rule applied to $\varphi(\alpha)=f(\mathbf x+\alpha\mathbf d)$ at $\alpha=0$ — see [[Calculus/contents/07 - Partial Derivatives and the Gradient|Calculus ch. 07]]. **If $\lVert\mathbf d\rVert=1$ it is the rate of increase of $f$ at $\mathbf x$ in the direction $\mathbf d$**; without normalisation it also scales with $\lVert\mathbf d\rVert$, which does not matter for any *sign* test below.

---

### 2. The first-order necessary condition

> [!important] FONC (C&Ż Theorem 6.1)
> Let $f\in C^1$ on $\Omega\subseteq\mathbb R^n$. **If $\mathbf x^*$ is a local minimizer of $f$ over $\Omega$, then for every feasible direction $\mathbf d$ at $\mathbf x^*$,**
> $$\boxed{\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ \ge\ 0}$$
>
> **Proof.** Put $\varphi(\alpha)=f(\mathbf x^*+\alpha\mathbf d)$. Taylor's theorem gives
> $$f(\mathbf x^*+\alpha\mathbf d)-f(\mathbf x^*)=\alpha\,\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)+o(\alpha)$$
> Since $\mathbf x^*$ is a local minimizer and $\mathbf d$ is feasible, the left side is $\ge0$ for all sufficiently small $\alpha>0$. Dividing by $\alpha>0$ and letting $\alpha\to0$ forces $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$. $\blacksquare$

**Read it as: from a minimizer, $f$ cannot decrease in any direction you are allowed to move.** Not "increases" — $\ge$, not $>$: moving sideways along a flat valley floor is permitted.

> [!important] Corollary — the interior case (C&Ż 6.1)
> If $\mathbf x^*$ is a local minimizer **and an interior point** of $\Omega$, then
> $$\nabla f(\mathbf x^*)=\mathbf 0$$
>
> **Proof.** All directions are feasible, so both $\mathbf d$ and $-\mathbf d$ qualify, giving $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$ **and** $-\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$, hence $=0$, for every $\mathbf d$. Only the zero vector is orthogonal to everything. $\blacksquare$

> [!warning] This is the corollary, not the theorem — and confusing them is the chapter's main hazard
> **"Set the gradient to zero" is a *special case* that holds only at interior points.** At a boundary point the correct condition is the inequality, and it is genuinely weaker: **a constrained minimizer routinely has $\nabla f\ne\mathbf 0$.**
>
> [[01 - The Optimization Problem|Chapter 01's]] Exercise 2 is the one-dimensional version: the minimizer of $3x^4-4x^3-12x^2+5$ on $[-2,1]$ is the endpoint $x=1$, where $f'(1)=-24$. The direction $d<0$ is the only feasible one, and $d\cdot(-24)>0$ ✔.
>
> **A point $\mathbf x$ with $\nabla f(\mathbf x)=\mathbf 0$ is called a *stationary* or *critical* point.** The words "stationary point" and "minimizer" are not synonyms in either direction on a constrained set.

**Worked example (C&Ż 6.3, adapted).** Minimise $f(\mathbf x)=x_1^2+2x_2^2+3x_1-4x_2+1$ over $\Omega=\{\mathbf x:x_1\ge0,\ x_2\ge0\}$, so $\nabla f=[2x_1+3,\ 4x_2-4]^{\mathsf T}$.

| Point | $\nabla f$ | Feasible directions | FONC? |
|---|---|---|---|
| $(1,1)$ | $[5,0]$ | all (interior) | **No** — needs $\nabla f=\mathbf 0$ |
| $(0,1)$ | $[3,0]$ | $d_1\ge0$, $d_2$ free | **Yes** — $\mathbf d^{\mathsf T}\nabla f=3d_1\ge0$ |
| $(0,0)$ | $[3,-4]$ | $d_1\ge0,\ d_2\ge0$ | **No** — $\mathbf d=(0,1)$ gives $-4$ |
| $(2,0)$ | $[7,-4]$ | $d_1$ free, $d_2\ge0$ | **No** — $\mathbf d=(0,1)$ gives $-4$ |

**Note that the unconstrained minimizer is $(-\tfrac32,1)$, which is outside $\Omega$.** The constrained solution $(0,1)$ sits on the boundary, has non-zero gradient, and would be missed entirely by a naive $\nabla f=\mathbf 0$ search.

---

### 3. Two ways the FONC gives you nothing

**These are the opposite failure modes, and both are common.**

**(a) The set has no feasible directions at all** (C&Ż Example 6.5). Take $\Omega=\{\mathbf x:x_1^2+x_2^2=1\}$, the unit circle. **No point of a curved equality-constrained set has any feasible direction** — every straight step off the circle leaves it immediately. The FONC's hypothesis is vacuously satisfied, so:

> **Every point of $\Omega$ satisfies the FONC, and the condition eliminates nothing.**

**The fix is to reparameterise.** With $x_1=\cos\theta$, $x_2=\sin\theta$ the problem becomes unconstrained in $\theta$, and $h(\theta)=f(\mathbf g(\theta))$ has $h'(\theta^*)=0$, which by the chain rule reads

$$\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)=0\qquad\text{for every }\mathbf d\ \textbf{tangent}\text{ to }\Omega\text{ at }\mathbf x^*$$

**Feasible directions have been replaced by *tangent* directions, and the inequality by an equality** — because a tangent direction and its negative are both admissible. **This is the whole idea of [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]]**: the Lagrange condition is exactly "$\nabla f$ is orthogonal to the tangent space", i.e. parallel to the normal space spanned by the $\nabla h_i$.

**(b) The condition holds at a point that is not a minimizer.** $f(x)=x^3$ has $f'(0)=0$ and $f''(0)=0$, so $x=0$ passes both first- and second-order necessary tests and is not a minimizer of anything.

> [!important] The two failures are complementary, and both are structural
> **The FONC is a filter, not a test.** It can be too coarse (case a: it rejects nothing) or too permissive (case b: it accepts non-minimizers). **What it is genuinely good at is *elimination*** — any point failing it is definitely not a local minimizer, and that is how it is used in practice.

---

### 4. The second-order necessary condition

> [!important] SONC (C&Ż Theorem 6.2)
> Let $f\in C^2$ on $\Omega$, let $\mathbf x^*$ be a local minimizer, and let $\mathbf d$ be a feasible direction at $\mathbf x^*$. **If $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)=0$, then**
> $$\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\,\mathbf d\ \ge\ 0$$
>
> **Proof (contradiction).** Suppose some feasible $\mathbf d$ has $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)=0$ and $\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\mathbf d<0$. Taylor's theorem for $\varphi(\alpha)=f(\mathbf x^*+\alpha\mathbf d)$ gives
> $$\varphi(\alpha)-\varphi(0)=\underbrace{\varphi'(0)}_{=0}\alpha+\varphi''(0)\frac{\alpha^2}{2}+o(\alpha^2)=\underbrace{\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\mathbf d}_{<0}\frac{\alpha^2}{2}+o(\alpha^2)$$
> which is negative for small $\alpha>0$ — contradicting local minimality. $\blacksquare$

> [!important] Corollary — the interior case (C&Ż 6.2)
> If $\mathbf x^*$ is an interior local minimizer of $f\in C^2$, then
> $$\nabla f(\mathbf x^*)=\mathbf 0\qquad\textbf{and}\qquad \nabla^2f(\mathbf x^*)\succeq0\ \ (\text{positive \textbf{semi}definite})$$

**The logic of the hypothesis is worth pausing on.** The second-order condition only bites in directions where the first-order term vanishes. **If $\mathbf d^{\mathsf T}\nabla f>0$, the linear term already guarantees an increase and curvature is irrelevant** — this is exactly the structure that reappears in [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]], where the second-order condition is imposed only on the tangent space.

---

### 5. The second-order sufficient condition

> [!important] SOSC, interior case (C&Ż Theorem 6.3)
> Let $f\in C^2$ and let $\mathbf x^*$ be an **interior** point with
> $$\text{(i) }\nabla f(\mathbf x^*)=\mathbf 0\qquad\text{(ii) }\nabla^2f(\mathbf x^*)\succ0\ \ (\textbf{positive definite})$$
> **Then $\mathbf x^*$ is a strict local minimizer.**
>
> **Proof.** By Rayleigh's inequality ([[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]), $\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\mathbf d\ge\lambda_{\min}\lVert\mathbf d\rVert^2$ with $\lambda_{\min}>0$. Taylor with (i) gives
> $$f(\mathbf x^*+\mathbf d)-f(\mathbf x^*)=\tfrac12\mathbf d^{\mathsf T}\nabla^2f(\mathbf x^*)\mathbf d+o(\lVert\mathbf d\rVert^2)\ \ge\ \tfrac{\lambda_{\min}}{2}\lVert\mathbf d\rVert^2+o(\lVert\mathbf d\rVert^2)$$
> **The quadratic term dominates the remainder for small $\lVert\mathbf d\rVert$**, so the difference is strictly positive. $\blacksquare$

> [!warning] Exactly one word changes between SONC and SOSC
> $$\textbf{SONC: }\nabla^2f\succeq0\ \text{(necessary)}\qquad\qquad\textbf{SOSC: }\nabla^2f\succ0\ \text{(sufficient)}$$
> **Semidefinite versus definite. The entire logical difference between "must hold" and "guarantees" sits in that one symbol** — and the boundary case $\nabla^2f\succeq0$ but not $\succ0$ is precisely where neither theorem decides:
>
> | at $x=0$ | $f=x^4$ | $f=-x^4$ | $f=x^3$ |
> |---|---|---|---|
> | $f'(0)$ | 0 | 0 | 0 |
> | $f''(0)$ | 0 | 0 | 0 |
> | Truth | strict min | strict **max** | neither |
>
> **All three points pass FONC and SONC identically and fail SOSC identically, and the three answers are all different.** No amount of examining these two conditions can separate them.

**The one-dimensional repair is a third-order condition** (C&Ż Exercise 6.5). If $0$ is an interior local minimizer with $f'(0)=f''(0)=0$, then necessarily $f'''(0)=0$ — see Exercise 4.

---

### 6. Putting it together

> [!important] The decision procedure at an **interior** point
> ```mermaid
> flowchart TD
>     A["Candidate x*"] --> B{"∇f(x*) = 0 ?"}
>     B -->|No| C["NOT a local minimizer<br/>(FONC fails)"]
>     B -->|Yes| D{"∇²f(x*) ≻ 0 ?"}
>     D -->|Yes| E["STRICT local minimizer<br/>(SOSC)"]
>     D -->|No| F{"∇²f(x*) ⪰ 0 ?"}
>     F -->|No| G["NOT a local minimizer<br/>(SONC fails)"]
>     F -->|Yes| H["UNDECIDED<br/>need higher order, or convexity"]
> ```

| $\nabla f(\mathbf x^*)$ | $\nabla^2f(\mathbf x^*)$ | Verdict |
|---|---|---|
| $\ne\mathbf 0$ | anything | **Not** a local minimizer |
| $=\mathbf 0$ | positive definite | **Strict local** minimizer |
| $=\mathbf 0$ | indefinite | **Not** a local minimizer — a **saddle** |
| $=\mathbf 0$ | negative definite | Strict local **maximizer** |
| $=\mathbf 0$ | positive semidefinite, singular | **Undecided** |

> [!important] And the one row that changes everything
> **If $f$ is convex** ([[02 - Convex Sets and Convex Functions|ch. 02]] §6), the table collapses:
> $$\nabla f(\mathbf x^*)=\mathbf 0\quad\Longrightarrow\quad \mathbf x^*\text{ is a \textbf{global} minimizer}$$
> **No Hessian needed, no "strict local" hedging, no undecided row.** Convexity does not merely close the necessary–sufficient gap; it upgrades the conclusion from *local* to *global*, which no amount of derivative information can do on its own.

**On the boundary the same logic runs with feasible directions in place of all directions**, and the table becomes a case analysis over which constraints are active. **[[11 - Constrained Optimization - Lagrange and KKT|Chapter 11]] systematises this** — the KKT conditions are the FONC written so that the case analysis is automatic.

---

### 7. Why these conditions do not constitute an algorithm

Chong & Żak close chapter 6 with the observation that motivates everything after it:

> [!warning] Solving the FONC directly is usually harder than the original problem
> **For $f$ with $n=20$ variables:**
> - The FONC is a system of **20 simultaneous nonlinear equations**, which generally has many solutions and no closed form.
> - Applying SONC or SOSC needs the Hessian: $\dfrac{n(n+1)}{2}=\dfrac{20\cdot21}{2}=\mathbf{210}$ distinct second derivatives at every candidate.
>
> **And $n=20$ is a small problem.** At $n=10^6$ the Hessian has $5\times10^{11}$ distinct entries and cannot be stored, let alone factorised.
>
> **This is why chapters 04–08 exist.** They abandon the idea of solving the optimality conditions and instead *search* — generating $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k$ and using the conditions of this chapter only as a **stopping test** ($\lVert\nabla f\rVert$ small) and as the **theoretical target** the search is aimed at.

> [!note] What an algorithm can and cannot verify
> | Quantity | Cost | Practical at $n=10^6$? |
> |---|---|---|
> | $f(\mathbf x)$ | 1 evaluation | ✔ |
> | $\nabla f(\mathbf x)$ | $\approx$ 1–3 evaluations (reverse-mode autodiff) | ✔ |
> | $\nabla^2f(\mathbf x)\mathbf v$ (Hessian-vector product) | $\approx$ 2 gradient evaluations | ✔ |
> | Full $\nabla^2f(\mathbf x)$ | $O(n^2)$ storage | ✘ |
> | Eigenvalues of $\nabla^2f$ | $O(n^3)$ | ✘ |
>
> **So a large-scale optimizer can test the FONC and never the SONC or SOSC.** In practice, "it converged" means "$\lVert\nabla f\rVert$ got small" — **a first-order statement only, which by §5's table cannot distinguish a minimum from a saddle.** That is not a minor caveat in high dimensions, where saddles vastly outnumber minima ([[Calculus/contents/08 - Multivariable Optimization|Calculus ch. 08]]).

---

## ✏️ Exercises

> [!question] Exercise 1 — FONC on a constrained set *(easy)*
> Minimise $f(\mathbf x)=x_1^2+2x_2^2+3x_1-4x_2+1$ over $\Omega=\{\mathbf x:x_1\ge0,\ x_2\ge0\}$.
> **(a)** Find the unconstrained stationary point. Is it feasible?
> **(b)** Test the FONC at $(1,1)$, $(0,1)$, $(0,0)$ and $(2,0)$.
> **(c)** Which point solves the problem, and is it a stationary point?

> [!example]- Solution
> $$\nabla f(\mathbf x)=\begin{bmatrix}2x_1+3\\4x_2-4\end{bmatrix}$$
>
> **(a)** $\nabla f=\mathbf 0$ gives $x_1=-\tfrac32$, $x_2=1$. **Not feasible** — $x_1<0$. **So the constrained solution cannot be found by setting the gradient to zero.**
>
> **(b)**
>
> | Point | $\nabla f$ | Feasible $\mathbf d$ | $\mathbf d^{\mathsf T}\nabla f$ | FONC |
> |---|---|---|---|---|
> | $(1,1)$ | $[5,0]$ | all — interior | $5d_1$, negative for $d_1<0$ | **fails** |
> | $(0,1)$ | $[3,0]$ | $d_1\ge0$, $d_2$ free | $3d_1\ge0$ **always** | **holds** |
> | $(0,0)$ | $[3,-4]$ | $d_1\ge0,\ d_2\ge0$ | $3d_1-4d_2$; $\mathbf d=(0,1)\Rightarrow-4$ | **fails** |
> | $(2,0)$ | $[7,-4]$ | $d_1$ free, $d_2\ge0$ | $7d_1-4d_2$; $\mathbf d=(0,1)\Rightarrow-4$ | **fails** |
>
> **At $(1,1)$ the interior corollary applies and $\nabla f\ne\mathbf 0$ settles it immediately** — no need to hunt for a bad direction.
>
> **(c)** Only $(0,1)$ survives, and it is the global minimizer: $f$ is convex (Hessian $\operatorname{diag}(2,4)\succ0$ everywhere) and $\Omega$ is convex, so by [[02 - Convex Sets and Convex Functions|ch. 02]] §6 the FONC is **sufficient** here.
> $$\boxed{\mathbf x^*=(0,1),\quad f(\mathbf x^*)=0+2+0-4+1=-1}$$
>
> **And $\nabla f(\mathbf x^*)=[3,0]^{\mathsf T}\ne\mathbf 0$.** The solution is not a stationary point. **This is the normal situation on a boundary and it is the single most important thing in the chapter.**
>
> *(Geometrically: $f$ still wants to decrease in the $-x_1$ direction, but the wall $x_1\ge0$ prevents it. The leftover gradient component pointing into the wall is what becomes a **Lagrange multiplier** in ch. 11 — here $\mu=3$, the "price" of the constraint $x_1\ge0$.)*

---

> [!question] Exercise 2 — classify every critical point *(easy–medium)*
> Let $f(x_1,x_2)=x_1^3+x_2^3-3x_1x_2$. Find all stationary points and classify each using SONC/SOSC. Is any of them a global minimizer?

> [!example]- Solution
> $$\nabla f=\begin{bmatrix}3x_1^2-3x_2\\3x_2^2-3x_1\end{bmatrix}=\mathbf 0\ \Longrightarrow\ x_2=x_1^2\ \text{and}\ x_1=x_2^2$$
> Substituting, $x_1=x_1^4$, so $x_1(x_1^3-1)=0$ and $x_1\in\{0,1\}$ (over the reals). **Stationary points: $(0,0)$ and $(1,1)$.**
>
> $$\nabla^2f=\begin{pmatrix}6x_1&-3\\-3&6x_2\end{pmatrix}$$
>
> | Point | Hessian | Eigenvalues | Verdict |
> |---|---|---|---|
> | $(0,0)$ | $\begin{pmatrix}0&-3\\-3&0\end{pmatrix}$ | $\{3,-3\}$ — **indefinite** | **SONC fails** $\Rightarrow$ not a minimizer. A **saddle**. |
> | $(1,1)$ | $\begin{pmatrix}6&-3\\-3&6\end{pmatrix}$ | $\{9,3\}$ — **positive definite** | **SOSC holds** $\Rightarrow$ **strict local minimizer**, $f=-1$ |
>
> *(Eigenvalues of $\begin{psmallmatrix}a&b\\b&a\end{psmallmatrix}$ are $a\pm b$, so $6\pm3$ and $0\pm3$.)*
>
> **Is $(1,1)$ global? No.** Along $x_2=0$, $f(x_1,0)=x_1^3\to-\infty$ as $x_1\to-\infty$. **The function is unbounded below, so it has no global minimizer at all** — consistent with [[01 - The Optimization Problem|ch. 01]] §3, since $f$ is not coercive.
>
> **Two lessons.** SOSC is a purely **local** statement and says nothing about behaviour far away. And $f$ is not convex — its Hessian is indefinite at $(0,0)$ — so [[02 - Convex Sets and Convex Functions|ch. 02]]'s upgrade to global is unavailable. **An algorithm started near $(1,1)$ converges there and reports success; started near $(-10,0)$ it diverges. Both behaviours are correct.**

---

> [!question] Exercise 3 — definitely, definitely not, or possibly *(medium)*
> For each specification, decide whether $\mathbf x^*$ is **(i)** definitely a local minimizer, **(ii)** definitely not, or **(iii)** possibly. Justify each.
> **(a)** $\Omega=\{x_1\ge1\}$, $\mathbf x^*=(1,2)$, $\nabla f(\mathbf x^*)=[1,1]^{\mathsf T}$
> **(b)** $\Omega=\{x_1\ge1,\ x_2\ge2\}$, $\mathbf x^*=(1,2)$, $\nabla f(\mathbf x^*)=[1,0]^{\mathsf T}$
> **(c)** $\Omega=\{x_1\ge0,\ x_2\ge0\}$, $\mathbf x^*=(1,2)$, $\nabla f(\mathbf x^*)=\mathbf 0$, $\nabla^2f(\mathbf x^*)=I$
> **(d)** $\Omega=\{x_1\ge1,\ x_2\ge2\}$, $\mathbf x^*=(1,2)$, $\nabla f(\mathbf x^*)=[1,0]^{\mathsf T}$, $\nabla^2f(\mathbf x^*)=\operatorname{diag}(1,-1)$

> [!example]- Solution
> **(a) Definitely not (ii).** At $(1,2)$ the constraint $x_1\ge1$ is active, so feasible directions are those with $d_1\ge0$ and $d_2$ **free**. Take $\mathbf d=(0,-1)$:
> $$\mathbf d^{\mathsf T}\nabla f=(0)(1)+(-1)(1)=-1<0$$
> **FONC fails.** *(The point is on a wall, but $f$ decreases along the wall — so you can slide down it.)*
>
> **(b) Possibly (iii).** Now both constraints are active, so feasible directions need $d_1\ge0$ **and** $d_2\ge0$. Then
> $$\mathbf d^{\mathsf T}\nabla f=d_1\cdot1+d_2\cdot0=d_1\ge0\ \ \checkmark$$
> **FONC holds.** But with no second-order information we cannot conclude more. **Note the difference from (a): the same gradient direction is fatal at a wall and harmless at a corner**, because the corner removes the escape route.
>
> *(Careful: the $d_2$ direction has $\mathbf d^{\mathsf T}\nabla f=0$, so the SONC would bite there if we had the Hessian — see (d).)*
>
> **(c) Definitely (i).** $\mathbf x^*=(1,2)$ is an **interior** point of $\{x_1\ge0,x_2\ge0\}$, since both coordinates are strictly positive. So the interior conditions apply: $\nabla f=\mathbf 0$ ✔ and $\nabla^2f=I\succ0$ ✔. **SOSC holds, so $\mathbf x^*$ is a strict local minimizer.**
>
> **This is the only part where a definite *positive* answer is possible**, because SOSC is the only sufficient condition available.
>
> **(d) Definitely not (ii).** The FONC holds, exactly as in (b). Now apply the **SONC**: it must be checked in every feasible direction with $\mathbf d^{\mathsf T}\nabla f=0$. The direction $\mathbf d=(0,1)$ is feasible ($d_1=0\ge0$, $d_2=1\ge0$) and has $\mathbf d^{\mathsf T}\nabla f=0$, so we require $\mathbf d^{\mathsf T}\nabla^2f\,\mathbf d\ge0$. But
> $$\begin{bmatrix}0&1\end{bmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix}\begin{bmatrix}0\\1\end{bmatrix}=-1<0$$
> **SONC fails, so $\mathbf x^*$ is not a local minimizer.** *(Moving along the corner's second edge, $f$ is flat to first order and curves downward.)*
>
> > [!tip]- The general procedure this exercise drills
> > 1. **Which constraints are active at $\mathbf x^*$?** That determines the cone of feasible directions.
> > 2. **Is $\mathbf x^*$ interior?** If so, use $\nabla f=\mathbf 0$ and be done with step 3.
> > 3. **Look for a single feasible $\mathbf d$ with $\mathbf d^{\mathsf T}\nabla f<0$.** One suffices to reject.
> > 4. **If none exists, check curvature on the directions where $\mathbf d^{\mathsf T}\nabla f=0$** — that is where SONC lives.
> > 5. **Only SOSC (interior) can give a definite yes.** Otherwise the honest answer is "possibly".

---

> [!question] Exercise 4 — necessary is not sufficient, and a third-order repair *(medium)*
> **(a)** Show that $x=0$ satisfies the FONC and SONC for all three of $f(x)=x^3$, $f(x)=x^4$ and $f(x)=-x^4$ on $\mathbb R$, and identify what $x=0$ actually is in each case.
> **(b)** State and prove a **third-order necessary condition (TONC)**: if $f\in C^3$ and $0$ is an interior local minimizer with $f'(0)=f''(0)=0$, what must $f'''(0)$ be?
> **(c)** Give an $f$ satisfying FONC, SONC and TONC at $0$ which is nonetheless not a local minimizer.
> **(d)** If $f$ is a **cubic polynomial** and $0$ satisfies FONC, SONC and TONC, is that sufficient?

> [!example]- Solution
> **(a)**
>
> | $f$ | $f'(0)$ | $f''(0)$ | FONC | SONC | Truth |
> |---|---|---|---|---|---|
> | $x^3$ | 0 | 0 | ✔ | ✔ ($0\ge0$) | **neither** — an inflection |
> | $x^4$ | 0 | 0 | ✔ | ✔ | **strict local (and global) minimizer** |
> | $-x^4$ | 0 | 0 | ✔ | ✔ | **strict local maximizer** |
>
> **All three are indistinguishable at first and second order, and all three answers differ.** This is the definitive demonstration that the necessary conditions are not sufficient. *(Note also that $x^4$ is strictly convex yet has $f''(0)=0$ — so SOSC is not necessary either.)*
>
> **(b) TONC: $f'''(0)=0$.**
>
> **Proof.** By Taylor's theorem with $f'(0)=f''(0)=0$,
> $$f(x)-f(0)=\frac{f'''(0)}{6}x^3+o(x^3)$$
> Suppose $f'''(0)\ne0$. Because $x^3$ **changes sign** at the origin, choose $x$ small with the sign making $\dfrac{f'''(0)}{6}x^3<0$ — i.e. $x<0$ if $f'''(0)>0$, and $x>0$ if $f'''(0)<0$. For $\lvert x\rvert$ small the cubic term dominates the $o(x^3)$ remainder, so $f(x)<f(0)$, contradicting local minimality. Hence $f'''(0)=0$. $\blacksquare$
>
> **The structural point: odd-order terms can always be made negative by choosing the side.** That is why every odd derivative must vanish at an interior minimizer, while even ones need only be non-negative — the general pattern behind FONC ($f'=0$), TONC ($f'''=0$), and so on.
>
> **(c) $f(x)=-x^4$.** Then $f'(0)=f''(0)=f'''(0)=0$, so FONC, SONC and TONC all hold, and $0$ is a strict local **maximizer**. *(Verified: the first three derivatives of $-x^4$ all vanish at 0.)*
>
> **Adding one more condition never finishes the job** — for any $k$, the function $-x^{2k}$ passes all conditions up to order $2k-1$. **No finite list of derivative conditions is sufficient in general**, and $e^{-1/x^2}$ (all derivatives zero at $0$, [[Calculus/contents/06 - Sequences, Series and Taylor Approximation|Calculus ch. 06]]) shows the limit of the whole approach.
>
> **(d) Yes.** Write $f(x)=a_3x^3+a_2x^2+a_1x+a_0$. The three conditions give
> $$f'(0)=a_1=0,\qquad f''(0)=2a_2\ge0,\qquad f'''(0)=6a_3=0$$
> so $a_3=0$, $a_1=0$, and $f(x)=a_2x^2+a_0$ with $a_2\ge0$.
> - If $a_2>0$: $0$ is a **strict global** minimizer.
> - If $a_2=0$: $f$ is constant, so $0$ is a (non-strict) global minimizer.
>
> **Either way $0$ is a local minimizer, so the conditions are sufficient.** $\blacksquare$
>
> **Why the restriction to cubics rescues it:** the conditions *force the cubic term to vanish*, collapsing $f$ to a quadratic — where second-order information is complete. **The counterexample in (c) needed a quartic**, which the hypothesis excludes. **The general moral is that sufficiency always comes from controlling the remainder**, and the only two ways to do it are a strict inequality (SOSC) or a global structural assumption (convexity).

---

> [!question] Exercise 5 — the conditions used as a method, and where it breaks *(hard)*
> A mobile phone sits at position $x$ on a line. Two base stations are located so that the squared distance to the primary is $1+x^2$ and to the neighbour is $1+(2-x)^2$. Received power is the reciprocal of squared distance, and the **signal-to-interference ratio** is
> $$f(x)=\frac{1+(2-x)^2}{1+x^2}$$
> **(a)** Maximise $f$ over $\mathbb R$ using the FONC. Give the exact optimal position and value.
> **(b)** The FONC produced two candidates. What in the theory of this chapter tells you which is which, and what does not?
> **(c)** Now suppose the same problem in $n=20$ dimensions. Count the work needed to apply FONC, SONC and SOSC, and say why chapters 04–08 exist.

> [!example]- Solution
> **(a)** By the quotient rule,
> $$f'(x)=\frac{-2(2-x)(1+x^2)-2x\big(1+(2-x)^2\big)}{(1+x^2)^2}=\frac{4(x^2-2x-1)}{(1+x^2)^2}$$
> The denominator never vanishes, so $f'(x)=0\iff x^2-2x-1=0$, giving
> $$x=1\pm\sqrt2$$
> Evaluating:
> $$f(1-\sqrt2)=3+2\sqrt2\approx5.8284,\qquad f(1+\sqrt2)=3-2\sqrt2\approx0.1716$$
> $$\boxed{x^*=1-\sqrt2\approx-0.4142,\qquad f(x^*)=3+2\sqrt2\approx5.83}$$
>
> *(A pleasing check: the two values multiply to $(3+2\sqrt2)(3-2\sqrt2)=9-8=1$ — they are reciprocals, which is forced by the symmetry $f(x)f(2-x)=1$ of the construction.)*
>
> **(b) The theory narrowed the search from a continuum to two points, and then stopped.**
>
> - **The FONC is what did the work**: it reduced an optimisation over all of $\mathbb R$ to solving one quadratic. **This is its real use — generating a finite candidate list.**
> - **Choosing between the two candidates was done by *evaluating $f$*, not by any condition in this chapter.** A second-order test would confirm each is a local max/min respectively, but **would still not establish which is global** — that needs either exhaustive comparison (possible here, because the list is finite) or convexity/concavity (unavailable: $f$ is neither).
> - **Existence had to be argued separately.** $\Omega=\mathbb R$ is unbounded, so Weierstrass does not apply; here $f\to1$ as $\lvert x\rvert\to\infty$ and $f>1$ at the candidate, so the maximum is attained. **Without that check the two roots might both have been non-optimal.**
>
> **(c)** For $f:\mathbb R^{20}\to\mathbb R$:
>
> | Step | Work |
> |---|---|
> | **FONC** | solve **20 simultaneous nonlinear equations** — no closed form, generally many roots, and even *counting* the roots is hard |
> | **Hessian** | $\dfrac{n(n+1)}{2}=\dfrac{20\cdot21}{2}=\mathbf{210}$ distinct second partial derivatives, **at every candidate** |
> | **SONC/SOSC** | classify a $20\times20$ symmetric matrix — $O(n^3)$ per candidate |
>
> **And $n=20$ is tiny.** A modest regression has $n=10^3$ ($5\times10^5$ Hessian entries); a network has $n=10^8$ and the Hessian would need $\sim10^{16}$ numbers.
>
> **So the conditions of this chapter are not a method.** What survives into practice is:
> 1. **The FONC as a stopping test** — stop when $\lVert\nabla f\rVert$ is small, which is cheap (one gradient) at any $n$.
> 2. **The FONC as the target** — every algorithm in chapters 04–08 is a scheme for driving $\nabla f$ to zero without ever solving $\nabla f=\mathbf 0$.
> 3. **SOSC as theory only** — it tells us *what* the algorithms are converging to and is used in the convergence proofs of ch. 06, but is never evaluated at scale.
>
> **The uncomfortable consequence, stated plainly:** at large $n$ an optimizer reports success on a **first-order** criterion, and by (a) of Exercise 4 a first-order criterion cannot distinguish a minimum from a saddle from an inflection. **"The gradient is small" is the only thing that is ever actually verified.**

---

## 📝 Summary

- **A feasible direction at $\mathbf x$** is one you can step along without leaving $\Omega$. **Interior points admit all directions; boundary points admit a cone; a curved equality set admits none.**
- **FONC:** at a local minimizer, $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$ for every feasible $\mathbf d$. **The familiar $\nabla f=\mathbf 0$ is only the interior corollary**, and a constrained minimizer routinely has $\nabla f\ne\mathbf 0$.
- **SONC:** in feasible directions where $\mathbf d^{\mathsf T}\nabla f=0$, curvature must satisfy $\mathbf d^{\mathsf T}\nabla^2f\,\mathbf d\ge0$; interior version, $\nabla^2f\succeq0$. **Curvature only matters where the linear term is silent.**
- **SOSC (interior):** $\nabla f=\mathbf 0$ **and** $\nabla^2f\succ0$ $\Rightarrow$ **strict local** minimizer. **The gap between SONC and SOSC is exactly $\succeq$ versus $\succ$.**
- **Nothing here is both necessary and sufficient.** $x^3$, $x^4$ and $-x^4$ pass FONC and SONC identically at $0$ and are respectively an inflection, a minimum and a maximum.
- **No finite list of derivative conditions can be sufficient in general** ($-x^{2k}$ defeats every list of length $2k-1$), though it can be for a restricted class such as cubics.
- **Convexity closes the gap and more:** for convex $f$ on convex $\Omega$, $\nabla f(\mathbf x^*)=\mathbf 0$ alone implies $\mathbf x^*$ is a **global** minimizer.
- **These conditions are not an algorithm.** At $n=20$ the FONC is 20 nonlinear equations and the Hessian has 210 entries; at $n=10^6$ the Hessian cannot be stored. **Chapters 04–08 search instead of solving, and use the FONC only as a stopping test.**

---

## ⚠️ Important Notes

> [!warning] The five errors
> 1. **Using $\nabla f=\mathbf 0$ on a boundary.** It is a corollary for interior points. On the boundary, use the inequality over feasible directions — and expect $\nabla f\ne\mathbf 0$ at the answer.
> 2. **Forgetting the SONC's hypothesis.** It applies **only** to feasible directions with $\mathbf d^{\mathsf T}\nabla f=0$. Testing curvature in a direction where the gradient term is already positive proves nothing.
> 3. **Confusing $\succeq$ with $\succ$.** Semidefinite is necessary; definite is sufficient. Swapping them turns a true theorem into a false one in both directions.
> 4. **Treating "stationary point" as "minimizer".** Saddles, maxima and inflections are stationary too — and in high dimensions saddles are the overwhelming majority.
> 5. **Expecting a *global* conclusion from a local test.** SOSC certifies a neighbourhood and nothing beyond it. Exercise 2's $(1,1)$ is a textbook strict local minimizer of a function that is unbounded below.

> [!tip] The compressed procedure
> ```
> interior?  ── yes ─→  ∇f = 0 ?  ── no ──→  reject
>    │                      │
>    no                    yes
>    │                      ↓
>    ↓                  ∇²f ≻ 0 ?  ── yes ─→  STRICT LOCAL MIN
> find one feasible d        │
> with dᵀ∇f < 0             no
>    │                       ↓
>   found ──→ reject     ∇²f ⪰ 0 ?  ── no ──→ reject (saddle/max)
>    │                       │
>  not found                yes
>    │                       ↓
>    ↓                   UNDECIDED
> check dᵀ∇²f d ≥ 0
> on directions with
> dᵀ∇f = 0
> ```
> **And above all: if $f$ is convex, stop at "$\nabla f=\mathbf 0$" and the answer is global.**

> [!note] Where this chapter is used
> - **[[04 - One-Dimensional Search Methods|Ch. 04]]–[[08 - Least Squares and Linear Equations|08]]** all target the FONC without solving it, and use $\lVert\nabla f\rVert<\varepsilon$ as their stopping test.
> - **[[06 - Newton and Quasi-Newton Methods|Ch. 06]]** is literally Newton's method applied to the equation $\nabla f(\mathbf x)=\mathbf 0$ — **the FONC solved iteratively.**
> - **[[11 - Constrained Optimization - Lagrange and KKT|Ch. 11]]** generalises §3(a): where there are no feasible directions, tangent directions take over, and the FONC becomes the Lagrange/KKT condition.
> - **[[02 - Convex Sets and Convex Functions|Ch. 02]] §6** is what makes these conditions sufficient, and **[[12 - Convex Programming and Constrained Algorithms|ch. 12]]** applies that to KKT.
> - **[[Calculus/contents/08 - Multivariable Optimization|Calculus ch. 08]]** is the unconstrained two-variable special case, with the discriminant $D=f_{xx}f_{yy}-f_{xy}^2$ standing in for definiteness of $\nabla^2f$.
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]** — the MLE score equation $\nabla\ell(\hat\theta)=\mathbf 0$ **is** the FONC, and the observed information $-\nabla^2\ell$ is the SOSC check.

---

> [!warning] Gaps in the source material
> **This chapter is entirely Chong & Żak ch. 6** — the one chapter of theirs with no counterpart in Luenberger & Ye, who present optimality conditions inside their algorithm chapters rather than separately. **So there was no clean second source to check displayed formulas against, and everything was verified computationally instead.**
>
> **OCR damage in ch. 6:**
> - **The Hessian display on p. 83 is destroyed** — it extracts as a scatter of `d2f`, `dx„dx\`, `Sw`, `a2/` with no brackets, no rows and no order. **The matrix had to be reconstructed from the definition.**
> - **`V/` is $\nabla f$, `£>/` and `D f` are $Df$, `F(x)` is the Hessian**, `/` alone is $f$, `G` and `£` are $\in$, `φ` is $\ne$, `—►` is $\to$, `W1` and `Mn` and `!lcl"` are all $\mathbb R^n$, and `#i`, `x\|`, `£i`, `as*`, `a5*`, `cc*`, `ceo` are all $x_i$ or $\mathbf x^*$.
> - **Definition 6.2's constant is mangled twice in one sentence**: `there exists ctQ > 0 such that x + ad G Ω for all a G [0, ao]` — `ctQ` and `ao` are the same symbol $\alpha_0$.
> - **The directional-derivative display is scrambled into a single line** with the limit, the numerator and the denominator interleaved: `Άχ) = lim /(* + ad)-/(a;). od a->o a`. **Reconstructed from the definition.**
> - **In Theorem 6.2's statement, $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)$ prints as `dTWf(x*)`** — a $\nabla$ read as a `W`. Elsewhere in the same proof it is correct, so this is inconsistent OCR rather than a book typo.
> - **Every figure is an image and all are lost.** The losses here are heavy because the chapter's whole argument is geometric: **Figure 6.2 (feasible vs infeasible directions — the definition), Figure 6.3 (the FONC on a constrained set, showing one point satisfying it and one not), Figure 6.4 (the level sets of Example 6.3), Figures 6.6–6.8 (the graphs of $x^3$, $x_1^2-x_2^2$ and $x_1^2+x_2^2$ that make the necessary-vs-sufficient point visually).** §§1–5 above substitute tables and a flowchart.
>
> **Verification performed.** Every claim was recomputed with `sympy`:
> - **C&Ż Example 6.4** (the cellular problem, used as Exercise 5): the derivative simplifies **exactly** to $4(x^2-2x-1)/(1+x^2)^2$ as printed, with roots $1\pm\sqrt2$, and $f(1-\sqrt2)=5.8284=3+2\sqrt2$ against $f(1+\sqrt2)=0.1716=3-2\sqrt2$, confirming the book's conclusion that $1-\sqrt2$ is optimal.
> - **Exercise 1**: the gradient at all four test points, and the unconstrained stationary point $(-\tfrac32,1)$.
> - **Exercise 2**: both stationary points, both Hessians and both eigenvalue pairs $\{3,-3\}$ and $\{9,3\}$.
> - **Exercise 4**: the first three derivatives of $-x^4$ all vanish at $0$.
> - **§7's counts**: $n(n+1)/2=210$ for $n=20$, as the book states.
>
> **No mathematical error was found in Chong & Żak ch. 6.**
>
> **Scope and additions.**
> - **§3's framing — that the FONC fails in two *opposite* ways — is my own.** Chong & Żak give both examples (6.5 for the no-feasible-directions case, 6.6 for the $x^3$ case) several pages apart and do not connect them. **Pairing them is what makes the "filter, not a test" reading available**, and it is what motivates ch. 11.
> - **§5's three-function table ($x^4$, $-x^4$, $x^3$) is my own construction.** The book gives $x^3$ only; adding the other two shows that the undecided case contains *all three* possible answers, which is a stronger and more memorable statement.
> - **§6's flowchart and decision table are my own**, as is the observation that convexity collapses the entire table to one row.
> - **§7's cost table (what an optimizer can actually evaluate at $n=10^6$) is entirely my own addition.** Chong & Żak make the $n=20$/210-derivatives point in a single closing paragraph and stop there. **Extending it to Hessian-vector products, autodiff costs, and the consequence that large-scale optimizers verify only a first-order criterion** connects this chapter to how optimization is actually practised, which the 2013 text does not attempt.
> - **The third-order condition of Exercise 4 is C&Ż's Exercise 6.5**, stated without solution in the book; **the proof, the "odd derivatives must vanish" generalisation, and the $e^{-1/x^2}$ remark are mine.**

#optimization #fonc #sonc #sosc #feasible-direction #stationary-point #hessian #necessary-vs-sufficient
