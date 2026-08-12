---
subject: Optimization
chapter: 02
tags: [ds, optimization, convexity, convex-set, convex-function, hessian, jensen, polyhedron]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 4 and §§22.1–22.3; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 7"
---

# Convex Sets and Convex Functions

> [!abstract] What this chapter is for
> **This is the chapter that decides which problems in the rest of the subject are solvable.** [[01 - The Optimization Problem|Chapter 01]] claimed that convexity, not linearity, is the tractability boundary. **This chapter says what convexity is and proves why that claim is true.**
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Convex sets | The segment between any two points stays inside |
> | **2** | Hyperplanes, halfspaces, polyhedra | The geometry chapters 09–10 live in — **and a naming clash between two books in this folder** |
> | **3** | Convex functions | Three equivalent definitions; use whichever is convenient |
> | **4** | **Recognising convexity** | **$\nabla^2f\succeq0$** — and a calculus of operations that preserve it |
> | **5** | Strict convexity | Upgrades *existence* of a minimizer to *uniqueness* |
> | **6** | **Why any of it matters** | **Local $\Rightarrow$ global, and $\nabla f=\mathbf 0$ becomes sufficient** |
>
> **§6 is the payoff and §4 is the tool.** Everything else is scaffolding for those two.

---

## 📘 Main Knowledge

### 1. Convex sets

> [!important] Definition
> A set $\Theta\subseteq\mathbb R^n$ is **convex** if for every $\mathbf u,\mathbf v\in\Theta$ and every $\alpha\in(0,1)$,
> $$\alpha\mathbf u+(1-\alpha)\mathbf v\in\Theta$$
> **In words: the line segment joining any two points of the set lies entirely inside the set.**

The point $\alpha\mathbf u+(1-\alpha)\mathbf v$ is a **convex combination** of $\mathbf u$ and $\mathbf v$; the segment itself is $\{\alpha\mathbf u+(1-\alpha)\mathbf v:\alpha\in[0,1]\}$. Taking $\alpha=0$ and $\alpha=1$ recovers the endpoints, which is why $\alpha$ can be restricted to the open interval without weakening the definition.

**Examples of convex sets** — worth memorising, because every convexity proof reduces to recognising one of these:

| Set | Description |
|---|---|
| $\varnothing$, $\{\mathbf a\}$, $\mathbb R^n$ | trivially |
| a line, a ray, a line segment | |
| any **subspace** | |
| a **hyperplane** $\{\mathbf x:\mathbf u^{\mathsf T}\mathbf x=v\}$ | §2 |
| a **halfspace** $\{\mathbf x:\mathbf u^{\mathsf T}\mathbf x\le v\}$ | §2 |
| a **linear variety** $\{\mathbf x:A\mathbf x=\mathbf b\}$ | the solution set of a linear system |
| a **ball** $\{\mathbf x:\lVert\mathbf x-\mathbf c\rVert\le r\}$ | for any norm |
| the **non-negative orthant** $\{\mathbf x:\mathbf x\ge\mathbf 0\}$ | |

> [!important] Operations that preserve convexity (C&Ż Theorem 4.1)
> If $\Theta,\Theta_1,\Theta_2$ are convex and $\beta\in\mathbb R$:
> - **Scaling.** $\beta\Theta=\{\beta\mathbf v:\mathbf v\in\Theta\}$ is convex.
> - **Sum.** $\Theta_1+\Theta_2=\{\mathbf v_1+\mathbf v_2:\mathbf v_i\in\Theta_i\}$ is convex.
> - **Intersection.** $\bigcap_{\Theta\in\mathcal C}\Theta$ is convex, **for any collection $\mathcal C$, finite or not.**
>
> **Each proof is one line**: take two points in the result, write them in terms of points of the ingredients, and use convexity of the ingredients on the same $\alpha$.

> [!warning] Union is not on that list, and the omission is the whole point
> $[0,1]\cup[2,3]$ is a union of two convex sets and is not convex. **Feasible sets built from "or" conditions are essentially never convex** — which is exactly why disjunctive constraints ("either this machine runs or that one does") force you into integer programming and out of the tractable world.
>
> **Intersection being closed under arbitrary collections is what makes §2 work:** a polyhedron is an intersection of halfspaces, so it is convex without any further argument.

**Extreme points.** A point $\mathbf x\in\Theta$ is an **extreme point** if it is not a convex combination of two *other* points of $\Theta$ — i.e. it is not in the interior of any segment lying in $\Theta$. **Every boundary point of a disk is extreme; the corners of a polygon are extreme and the edge interiors are not.** [[09 - Linear Programming and the Simplex Method|Chapter 09]] is built on the fact that a linear objective attains its optimum at an extreme point.

---

### 2. Hyperplanes, halfspaces and polyhedra

Let $\mathbf u\in\mathbb R^n$, $\mathbf u\ne\mathbf 0$, and $v\in\mathbb R$.

$$\underbrace{H=\{\mathbf x:\mathbf u^{\mathsf T}\mathbf x=v\}}_{\textbf{hyperplane}}\qquad \underbrace{H_+=\{\mathbf x:\mathbf u^{\mathsf T}\mathbf x\ge v\}}_{\textbf{positive halfspace}}\qquad \underbrace{H_-=\{\mathbf x:\mathbf u^{\mathsf T}\mathbf x\le v\}}_{\textbf{negative halfspace}}$$

**A hyperplane has dimension $n-1$**: a line in $\mathbb R^2$, an ordinary plane in $\mathbb R^3$. It is a subspace **only if $v=0$**; otherwise it is a translate of one.

> [!note] $\mathbf u$ is the normal, and the proof is two lines
> Pick any $\mathbf a\in H$, so $\mathbf u^{\mathsf T}\mathbf a=v$. Then for any $\mathbf x$,
> $$\mathbf u^{\mathsf T}\mathbf x-v=\mathbf u^{\mathsf T}\mathbf x-\mathbf u^{\mathsf T}\mathbf a=\mathbf u^{\mathsf T}(\mathbf x-\mathbf a)$$
> so $\mathbf x\in H\iff\mathbf u\perp(\mathbf x-\mathbf a)$. **The hyperplane is the set of points whose displacement from any of its points is orthogonal to $\mathbf u$** — which is the [[Linear Algebra/contents/04 - Vector Geometry|Linear Algebra ch. 04]] equation of a plane, and the reason $\nabla f$ pointing normal to a level set ([[Calculus/contents/07 - Partial Derivatives and the Gradient|Calculus ch. 07]]) is the same statement linearised.

**A supporting hyperplane** at a boundary point $\mathbf y$ of a convex $\Theta$ is a hyperplane through $\mathbf y$ with all of $\Theta$ on one side. **Separating and supporting hyperplane theorems are the geometric engine behind duality** ([[10 - Duality|ch. 10]]) — a dual feasible point *is* a separating hyperplane.

> [!warning] **"Polytope" and "polyhedron" mean opposite things in the two books in this folder**
> **This is a genuine terminological conflict and it will confuse you if you read both.**
>
> | | Intersection of finitely many halfspaces | Bounded version of it |
> |---|---|---|
> | **Chong & Żak §4.5** | **"convex polytope"** | **"polyhedron"** |
> | **Bertsimas & Tsitsiklis §2.1**, and essentially all modern usage | **"polyhedron"** | **"polytope"** |
>
> **The modern convention is the second one**, and these notes use it throughout:
> $$\textbf{polyhedron } P=\{\mathbf x:A\mathbf x\ge\mathbf b\}\ \text{ (any intersection of halfspaces)};\qquad \textbf{polytope}=\text{a bounded polyhedron}$$
> **Mnemonic: a polytope is a *finite* object, and "-tope" is the shorter word.** Chong & Żak's usage is older and now non-standard; when their chapters 15–19 say "polyhedron" they mean what everyone else calls a polytope.

**Faces, edges, vertices.** The boundary of a $k$-dimensional polyhedron consists of finitely many $(k-1)$-dimensional polyhedra, its **faces**. A $0$-dimensional face is a **vertex**, a $1$-dimensional face an **edge**. **Vertices are exactly the extreme points**, and [[09 - Linear Programming and the Simplex Method|ch. 09]] shows they are exactly the *basic feasible solutions* — the same objects seen geometrically, combinatorially and algebraically.

---

### 3. Convex functions: three equivalent definitions

> [!important] Definition via the epigraph
> The **graph** of $f:\Omega\to\mathbb R$ is $\left\{\begin{bmatrix}\mathbf x\\f(\mathbf x)\end{bmatrix}:\mathbf x\in\Omega\right\}\subseteq\mathbb R^{n+1}$, and the **epigraph** is everything on or above it:
> $$\operatorname{epi}(f)=\left\{\begin{bmatrix}\mathbf x\\\beta\end{bmatrix}:\mathbf x\in\Omega,\ \beta\ge f(\mathbf x)\right\}$$
> **$f$ is convex on $\Omega$ if $\operatorname{epi}(f)$ is a convex set.**

**This definition is the conceptually right one** — it makes convexity of a *function* a special case of convexity of a *set*, so §1's theorems apply directly. It also has a pleasant consequence:

> **Theorem (C&Ż 22.1).** *If $f$ is convex on $\Omega$ then $\Omega$ is a convex set.*
>
> *(Contrapositive: if $\Omega$ has a "gap", the epigraph has one directly above it.)* **So "convex function" silently includes "convex domain"** — you never have to say both.

> [!important] The working definition (C&Ż Theorem 22.2)
> $f$ defined on a convex $\Omega$ is convex **if and only if** for all $\mathbf x,\mathbf y\in\Omega$ and all $\alpha\in(0,1)$,
> $$\boxed{f\big(\alpha\mathbf x+(1-\alpha)\mathbf y\big)\ \le\ \alpha f(\mathbf x)+(1-\alpha)f(\mathbf y)}$$
>
> **In words: the chord lies on or above the graph.** This is the form you actually compute with, and many books take it as the definition.

> [!important] Strict convexity and concavity
> - $f$ is **strictly convex** if the inequality is strict ($<$) for all $\mathbf x\ne\mathbf y$ and $\alpha\in(0,1)$ — **the chord lies strictly above the graph except at its endpoints.**
> - $f$ is **(strictly) concave** if $-f$ is (strictly) convex — the chord lies *below*.
>
> **A function can be both convex and concave: exactly the affine functions $\mathbf a^{\mathsf T}\mathbf x+b$.** That is why linear programs are simultaneously convex minimisations and concave maximisations, and why LP has such a symmetric duality theory.

**Jensen's inequality** is the same statement for $m$ points, or for a random variable:
$$f\left(\sum_i\alpha_i\mathbf x_i\right)\le\sum_i\alpha_if(\mathbf x_i)\quad\left(\alpha_i\ge0,\ \textstyle\sum\alpha_i=1\right)\qquad\text{and}\qquad \boxed{f\big(\mathbb E[X]\big)\le\mathbb E\big[f(X)\big]}$$

**The probabilistic form is used constantly** — see [[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]].

---

### 4. **Recognising convexity** — the practical section

You will almost never verify the chord inequality directly. **There are two calculus tests and one algebra of operations.**

> [!important] First-order condition (C&Ż Theorem 22.4)
> For $f\in C^1$ on an open convex $\Omega$: $f$ is convex **iff** for all $\mathbf x,\mathbf y\in\Omega$,
> $$f(\mathbf y)\ \ge\ f(\mathbf x)+\nabla f(\mathbf x)^{\mathsf T}(\mathbf y-\mathbf x)$$
>
> **In words: the tangent plane at every point lies below the graph.** The right-hand side is exactly the linear approximation of [[Calculus/contents/02 - Derivatives|Calculus ch. 02]], so this says: **a convex function is one whose linear approximation is always a global underestimate.**

**That reading is the most useful one in the chapter**, and it is where the punchline of §6 comes from: if the tangent at $\mathbf x^*$ is flat *and* lies below everything, then $f(\mathbf y)\ge f(\mathbf x^*)$ for every $\mathbf y$ — globally, immediately.

> [!note] Non-differentiable functions have this too — the subgradient
> If $f$ is not differentiable, a vector $\mathbf g$ is a **subgradient** at $\mathbf x$ when
> $$f(\mathbf y)\ge f(\mathbf x)+\mathbf g^{\mathsf T}(\mathbf y-\mathbf x)\quad\text{for all }\mathbf y$$
> i.e. **any vector that makes the first-order condition true.** A convex function has at least one at every interior point; at a kink it has infinitely many. **This is what makes the LASSO tractable**: $\lVert\boldsymbol\beta\rVert_1$ is convex and non-differentiable at zero, and subgradient methods handle it. See [[12 - Convex Programming and Constrained Algorithms|ch. 12]].

> [!important] Second-order condition (C&Ż Theorem 22.5) — **the test you will actually use**
> For $f\in C^2$ on an open convex $\Omega$:
> $$f\ \text{convex on }\Omega\quad\Longleftrightarrow\quad \nabla^2f(\mathbf x)\succeq0\ \ \text{(positive semidefinite) for every }\mathbf x\in\Omega$$
> and $f$ is **concave** iff $\nabla^2f\preceq0$ everywhere.
>
> **One-way strengthening:** $\nabla^2f(\mathbf x)\succ0$ everywhere $\Rightarrow$ $f$ strictly convex. **The converse is false** — $f(x)=x^4$ is strictly convex with $f''(0)=0$.

**How to check definiteness** (from [[Linear Algebra/contents/07 - Linear Transformations|Linear Algebra ch. 07]]):

| Test | Positive definite | Positive semidefinite |
|---|---|---|
| **Eigenvalues** | all $>0$ | all $\ge0$ |
| **Leading principal minors** | all $>0$ | **not sufficient** — need *all* principal minors $\ge0$ |

> [!warning] The minor test is asymmetric and this trips people up
> **For positive *definiteness*, the $n$ leading principal minors suffice (Sylvester's criterion).** For positive *semi*definiteness they do not: $\begin{pmatrix}0&0\\0&-1\end{pmatrix}$ has leading minors $0$ and $0$, both $\ge0$, and is negative semidefinite. **For the semidefinite case, use eigenvalues.**

> [!important] The calculus of convexity — usually faster than any Hessian
> If $f,f_1,\dots,f_k$ are convex, so are:
>
> | Operation | Condition |
> |---|---|
> | $\alpha f$ | $\alpha\ge0$ |
> | $f_1+f_2$, and $\sum_ic_if_i$ | $c_i\ge0$ |
> | $\max\{f_1,\dots,f_k\}$ | always — **even for infinitely many** |
> | $f(A\mathbf x+\mathbf b)$ | any affine map — **composition with affine preserves convexity** |
> | $g(f(\mathbf x))$ | $g$ convex **and non-decreasing** |
> | $\sup_{\mathbf y}f(\mathbf x,\mathbf y)$ | $f$ convex in $\mathbf x$ for each $\mathbf y$ |
>
> **Two are missing on purpose:** the **product** of convex functions need not be convex ($x\cdot x^2=x^3$), and the **minimum** of convex functions need not be convex ($\min\{x^2,(x-4)^2\}$ has two valleys).

> [!tip] The standard build
> **Almost every convex loss in machine learning is assembled from this table, not verified by a Hessian:**
> $$\underbrace{\tfrac1n\sum_{i=1}^n}_{\text{non-negative sum}}\underbrace{\ell\big(\underbrace{\mathbf x_i^{\mathsf T}\boldsymbol\beta}_{\text{affine}}\big)}_{\text{convex}\circ\text{affine}}+\underbrace{\lambda\lVert\boldsymbol\beta\rVert}_{\text{norm, convex}}$$
> Squared loss, hinge loss, logistic loss and $\varepsilon$-insensitive loss are all convex in one variable; composing with an affine map and summing keeps them convex. **This is why linear models have well-posed training problems and neural networks do not** — inserting a non-affine layer breaks the second row of the table.

---

### 5. Strict convexity buys uniqueness

> [!important] Theorem
> **If $f$ is strictly convex on a convex $\Omega$, it has at most one global minimizer.**
>
> **Proof.** Suppose $\mathbf x^*\ne\mathbf y^*$ both attain the minimum $m$. Their midpoint is in $\Omega$ by convexity, and by strict convexity
> $$f\!\left(\tfrac12\mathbf x^*+\tfrac12\mathbf y^*\right)<\tfrac12 f(\mathbf x^*)+\tfrac12 f(\mathbf y^*)=m$$
> contradicting minimality of $m$. $\blacksquare$

**Combine with [[01 - The Optimization Problem|ch. 01]]'s existence results and you get the complete statement:**

$$\underbrace{\text{coercive + continuous}}_{\textbf{a minimizer exists}}\ +\ \underbrace{\text{strictly convex}}_{\textbf{at most one}}\quad\Longrightarrow\quad\textbf{exactly one global minimizer}$$

**This is the situation ridge regression engineers deliberately.** With $L(\boldsymbol\beta)=\lVert\mathbf y-X\boldsymbol\beta\rVert^2+\lambda\lVert\boldsymbol\beta\rVert^2$ the Hessian is $2(X^{\mathsf T}X+\lambda I)$, which is positive definite for every $\lambda>0$ **regardless of the rank of $X$** — so the problem has exactly one solution even when $p>n$ and OLS has infinitely many. See Exercise 4.

---

### 6. **Why convexity matters**

> [!important] Theorem (C&Ż 22.6) — local implies global
> Let $f$ be convex on a convex $\Omega$. **Then $\mathbf x^*$ is a global minimizer if and only if it is a local minimizer.**
>
> **Proof (contrapositive).** If $\mathbf x^*$ is not global, some $\mathbf y$ has $f(\mathbf y)<f(\mathbf x^*)$. For every $\alpha\in(0,1)$,
> $$f\big(\alpha\mathbf y+(1-\alpha)\mathbf x^*\big)\le\alpha f(\mathbf y)+(1-\alpha)f(\mathbf x^*)=f(\mathbf x^*)+\alpha\big(f(\mathbf y)-f(\mathbf x^*)\big)<f(\mathbf x^*)$$
> Letting $\alpha\to0$ gives points **arbitrarily close to $\mathbf x^*$ with strictly smaller value**, so $\mathbf x^*$ is not even a local minimizer. $\blacksquare$

**This single theorem is why the whole subject splits in two.** Every algorithm in chapters 04–08 detects local minimizers. **On a convex problem that is the same thing as solving it; on a non-convex problem it is not, and no amount of extra iterations fixes the difference.**

> [!important] Corollaries — the first-order condition becomes *sufficient*
> Let $f$ be convex and $C^1$ on a convex $\Omega$.
>
> | | Statement |
> |---|---|
> | **C&Ż 22.7** | If $\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0$ for every feasible direction $\mathbf d$ at $\mathbf x^*$, then $\mathbf x^*$ is a **global** minimizer |
> | **C&Ż 22.2** | If $\nabla f(\mathbf x^*)=\mathbf 0$, then $\mathbf x^*$ is a **global** minimizer |
> | **C&Ż 22.8** | The **Lagrange condition** is sufficient for a global minimizer (convex $\Omega$) |
> | **C&Ż 22.9** | The **KKT conditions** are sufficient for a global minimizer |
>
> **The proof of every one is the same move**: the first-order condition of §4 says $f(\mathbf x)\ge f(\mathbf x^*)+\nabla f(\mathbf x^*)^{\mathsf T}(\mathbf x-\mathbf x^*)$, and the hypothesis makes the last term $\ge0$.

> [!important] The full picture
> | | Non-convex | Convex |
> |---|---|---|
> | $\nabla f=\mathbf 0$ | **necessary only** — could be a max or a saddle | **necessary and sufficient**, and global |
> | Local minimizer | may not be global | **is** global |
> | Number of minimizers | arbitrary | **the set of them is convex** (C&Ż Cor. 22.1) |
> | Can an algorithm certify optimality? | **no** | **yes** — see duality, [[10 - Duality|ch. 10]] |

**Two more facts that get used constantly:**

- **Sublevel sets are convex** (C&Ż Lemma 22.1): $\{\mathbf x\in\Omega:f(\mathbf x)\le c\}$ is convex for every $c$. This is why $\{\mathbf g(\mathbf x)\le\mathbf 0\}$ is a convex feasible set when every $g_j$ is convex — it is an intersection of sublevel sets.
- **The set of global minimizers is convex** — it is the sublevel set at $c=\min f$.

> [!warning] The converse of the sublevel-set lemma is false, and it has a name
> **Convex sublevel sets do not imply a convex function.** A function with all sublevel sets convex is called **quasiconvex**, and it is strictly weaker: $f(x)=\sqrt{|x|}$ is quasiconvex and not convex.
>
> **Quasiconvexity is not enough for anything in §6.** Local minima need not be global for a quasiconvex function *(consider a function with a flat stretch)*, and the first-order condition is not sufficient. **Checking "the level curves look convex" is therefore not a test of convexity** — this is one of the more common errors in the subject.

> [!note] The honest position on deep learning
> **Training loss surfaces are not convex, so nothing in §6 applies to them.** Gradient descent on a network returns a stationary point of an unknown landscape with no certificate of any kind.
>
> **What is true instead is empirical**: in very high dimensions most stationary points are saddles rather than poor local minima ([[Calculus/contents/08 - Multivariable Optimization|Calculus ch. 08]]), and many local minima found in practice have similar loss values. **These are observations, not theorems**, and the gap between them and §6 is the honest reason deep learning is an experimental subject.

---

## ✏️ Exercises

> [!question] Exercise 1 — proving sets convex *(easy)*
> **(a)** Show that the ball $B=\{\mathbf x\in\mathbb R^n:\lVert\mathbf x\rVert\le r\}$ is convex.
> **(b)** Show that the linear variety $V=\{\mathbf x:A\mathbf x=\mathbf b\}$ is convex.
> **(c)** Deduce that $\{\mathbf x:A\mathbf x=\mathbf b,\ \mathbf x\ge\mathbf 0,\ \lVert\mathbf x\rVert\le r\}$ is convex, without any further computation.
> **(d)** Give two convex sets whose union is not convex.

> [!example]- Solution
> **(a)** Let $\mathbf u,\mathbf v\in B$ and $\alpha\in(0,1)$. By the triangle inequality and absolute homogeneity of the norm,
> $$\lVert\alpha\mathbf u+(1-\alpha)\mathbf v\rVert\le\lVert\alpha\mathbf u\rVert+\lVert(1-\alpha)\mathbf v\rVert=\alpha\lVert\mathbf u\rVert+(1-\alpha)\lVert\mathbf v\rVert\le\alpha r+(1-\alpha)r=r$$
> so $\alpha\mathbf u+(1-\alpha)\mathbf v\in B$. $\blacksquare$
>
> **Note the proof used only the norm axioms**, so it holds for $\lVert\cdot\rVert_1$, $\lVert\cdot\rVert_\infty$ and every other norm. **The $\ell_1$ ball being convex is what makes the LASSO a convex problem**; $\lVert\boldsymbol\beta\rVert_0$ (the count of non-zeros) is not a norm, its "ball" is not convex, and best-subset selection is correspondingly NP-hard.
>
> **(b)** Let $\mathbf u,\mathbf v\in V$, so $A\mathbf u=A\mathbf v=\mathbf b$. Then by linearity
> $$A\big(\alpha\mathbf u+(1-\alpha)\mathbf v\big)=\alpha A\mathbf u+(1-\alpha)A\mathbf v=\alpha\mathbf b+(1-\alpha)\mathbf b=\mathbf b$$
> so the combination is in $V$. $\blacksquare$ *(Note $\alpha+(1-\alpha)=1$ is exactly what makes this work — it would fail for arbitrary linear combinations unless $\mathbf b=\mathbf 0$.)*
>
> **(c)** The set is $V\cap\{\mathbf x\ge\mathbf 0\}\cap B$. The first is convex by (b), the third by (a), and $\{\mathbf x\ge\mathbf 0\}=\bigcap_{i=1}^n\{\mathbf x:x_i\ge0\}$ is an intersection of $n$ halfspaces. **By C&Ż Theorem 4.1(c) the intersection of convex sets is convex, so the whole thing is convex.** $\blacksquare$
>
> **This is the standard move and it is why §1's closure properties matter more than any individual proof.** The feasible set of a linear program is exactly of this shape.
>
> **(d)** $\Theta_1=[0,1]$ and $\Theta_2=[2,3]$ in $\mathbb R$. Both are convex; their union is not, since $\tfrac12\cdot1+\tfrac12\cdot2=1.5\notin\Theta_1\cup\Theta_2$.
>
> **In two dimensions the same failure is the reason "either constraint A or constraint B" cannot be written as a convex feasible set** and forces a binary variable — the boundary between linear programming and integer programming.

---

> [!question] Exercise 2 — convex, concave or neither *(easy–medium)*
> Classify each on all of $\mathbb R^n$ using the Hessian, and say whether it is *strictly* convex/concave.
> **(a)** $f(\mathbf x)=3x_1^2+2x_2^2+x_3^2+2x_1x_2-x_2x_3$
> **(b)** $f(\mathbf x)=-x_1^2-4x_2^2+4x_1x_2$
> **(c)** $f(\mathbf x)=x_1^2-x_2^2$
> **(d)** $f(\mathbf x)=x_1x_2$

> [!example]- Solution
> **(a)** $$\nabla^2f=\begin{pmatrix}6&2&0\\2&4&-1\\0&-1&2\end{pmatrix}$$
> Leading principal minors: $\Delta_1=6$, $\Delta_2=24-4=20$, $\Delta_3=6(8-1)-2(4-0)+0=42-8=34$. **All positive $\Rightarrow$ positive definite** (Sylvester), confirmed by the eigenvalues $\{7.290,\ 3.294,\ 1.416\}$.
> $$\boxed{\text{strictly convex on }\mathbb R^3}$$
>
> **(b)** $$\nabla^2f=\begin{pmatrix}-2&4\\4&-8\end{pmatrix}$$
> Eigenvalues $\{0,-10\}$: **negative semidefinite, not definite.** So $f$ is **concave but not strictly concave**. Indeed $f(\mathbf x)=-(x_1-2x_2)^2$, which is $0$ along the whole line $x_1=2x_2$ — a flat direction, hence the zero eigenvalue.
>
> **This is the shape of a rank-deficient least-squares problem**, and the flat direction is exactly the non-uniqueness of the minimizer.
>
> **(c)** $$\nabla^2f=\begin{pmatrix}2&0\\0&-2\end{pmatrix}$$
> Eigenvalues $\{2,-2\}$: **indefinite**, so **neither convex nor concave.** The origin is a **saddle point** — the canonical one.
>
> **(d)** $$\nabla^2f=\begin{pmatrix}0&1\\1&0\end{pmatrix}$$
> Eigenvalues $\{1,-1\}$: **indefinite**, so **neither.** *(Leading minors $0$ and $-1$: the failure of $\Delta_2<0$ already settles it.)*
>
> **This is the example that proves the product rule is missing from §4's table.** $g(x_1)=x_1$ and $h(x_2)=x_2$ are both convex (affine, in fact), and their product is not.
>
> **Restricting the domain does not help**, which is worth checking: on $\Omega=\{\mathbf x>\mathbf 0\}$, take $\mathbf x=(1,2)$, $\mathbf y=(2,1)$, $\alpha=\tfrac12$. The midpoint is $(1.5,1.5)$ with $f=2.25$, while $\tfrac12f(\mathbf x)+\tfrac12f(\mathbf y)=\tfrac12(2)+\tfrac12(2)=2$. **Since $2.25>2$ the chord lies *below* the graph, so $f$ is not convex there either** — this is C&Ż's Example 22.4.

---

> [!question] Exercise 3 — the calculus of convexity *(medium)*
> Let $f_1,f_2:\Omega\to\mathbb R$ be convex on a convex $\Omega$.
> **(a)** Prove $f_1+f_2$ is convex, and that $cf_1$ is convex for $c\ge0$.
> **(b)** Prove $M(\mathbf x)=\max\{f_1(\mathbf x),f_2(\mathbf x)\}$ is convex.
> **(c)** Show by counterexample that $f_1f_2$ and $\min\{f_1,f_2\}$ need not be convex.
> **(d)** Prove: if $g:\mathbb R\to\mathbb R$ is convex and **non-decreasing** and $f$ is convex, then $g\circ f$ is convex. Where does "non-decreasing" get used?

> [!example]- Solution
> Throughout let $\mathbf x,\mathbf y\in\Omega$, $\alpha\in(0,1)$, and write $\mathbf z=\alpha\mathbf x+(1-\alpha)\mathbf y$.
>
> **(a)** Add the two chord inequalities:
> $$f_1(\mathbf z)+f_2(\mathbf z)\le\big[\alpha f_1(\mathbf x)+(1-\alpha)f_1(\mathbf y)\big]+\big[\alpha f_2(\mathbf x)+(1-\alpha)f_2(\mathbf y)\big]=\alpha(f_1+f_2)(\mathbf x)+(1-\alpha)(f_1+f_2)(\mathbf y)$$
> For $cf_1$, multiply the inequality by $c\ge0$ — **and this is exactly where non-negativity is needed: multiplying by a negative number reverses the inequality and produces a concave function.** $\blacksquare$
>
> **(b)** For each $i$, $f_i(\mathbf z)\le\alpha f_i(\mathbf x)+(1-\alpha)f_i(\mathbf y)\le\alpha M(\mathbf x)+(1-\alpha)M(\mathbf y)$, using $f_i\le M$ pointwise and $\alpha,1-\alpha\ge0$. **The right-hand side does not depend on $i$**, so it also bounds the maximum:
> $$M(\mathbf z)=\max_i f_i(\mathbf z)\le\alpha M(\mathbf x)+(1-\alpha)M(\mathbf y)\qquad\blacksquare$$
>
> **The argument never used that there are only two functions**, so it works for **any** family, finite or infinite. **This is the deepest entry in §4's table**: it is why $\lVert\mathbf x\rVert_\infty=\max_i|x_i|$ is convex, why the hinge loss $\max\{0,1-yf\}$ is convex, and — via $\sup_{\mathbf y}$ — why **every dual function in [[10 - Duality|ch. 10]] is concave regardless of the primal problem**.
>
> **(c)** **Product:** $f_1(x)=x$ and $f_2(x)=x^2$ are convex on $\mathbb R$ (second derivatives $0$ and $2$). Their product is $x^3$, with $(x^3)''=6x<0$ for $x<0$ — **not convex.**
>
> **Minimum:** $f_1(x)=x^2$ and $f_2(x)=(x-4)^2$ are convex; $\min\{f_1,f_2\}$ equals $x^2$ for $x\le2$ and $(x-4)^2$ for $x\ge2$. Its values at $x=0,2,4$ are $0,4,0$, so the chord from $(0,0)$ to $(4,0)$ lies at height $0$ **below** the graph's value $4$ at the midpoint. **Not convex** — it has two separate valleys, which is precisely the pathology §6 rules out.
>
> **(d)** Since $f$ is convex, $f(\mathbf z)\le\alpha f(\mathbf x)+(1-\alpha)f(\mathbf y)$. Apply $g$ to both sides:
> $$g\big(f(\mathbf z)\big)\ \underbrace{\le}_{\textbf{$g$ non-decreasing}}\ g\big(\alpha f(\mathbf x)+(1-\alpha)f(\mathbf y)\big)\ \underbrace{\le}_{\textbf{$g$ convex}}\ \alpha g(f(\mathbf x))+(1-\alpha)g(f(\mathbf y))\qquad\blacksquare$$
>
> **Monotonicity is used in the first step and convexity in the second, and neither can be dropped.** Counterexample without monotonicity: $g(t)=t^2$ is convex but decreasing on $t<0$; with $f(x)=x^2-1$ (convex), $g(f(x))=(x^2-1)^2$ has minima at $x=\pm1$ and a local max at $0$ — **not convex.**
>
> **This rule is the workhorse.** $e^{f}$, $\log\!\big(1+e^{f}\big)$ and $(f_+)^2$ are convex whenever $f$ is, which is where the logistic and squared-hinge losses come from.

---

> [!question] Exercise 4 — strict convexity, uniqueness, and ridge regression *(medium–hard)*
> Let $X\in\mathbb R^{n\times p}$ and $\mathbf y\in\mathbb R^n$, and consider
> $$L_\lambda(\boldsymbol\beta)=\lVert\mathbf y-X\boldsymbol\beta\rVert^2+\lambda\lVert\boldsymbol\beta\rVert^2$$
> **(a)** Compute $\nabla L_\lambda$ and $\nabla^2L_\lambda$.
> **(b)** For $\lambda=0$, when is $L_0$ strictly convex? What happens when $p>n$?
> **(c)** Show that for every $\lambda>0$, $L_\lambda$ is strictly convex **for any $X$ whatsoever**, and write down its unique minimizer.
> **(d)** Explain what has been bought, and what it cost.

> [!example]- Solution
> **(a)** Expanding, $L_\lambda(\boldsymbol\beta)=\mathbf y^{\mathsf T}\mathbf y-2\mathbf y^{\mathsf T}X\boldsymbol\beta+\boldsymbol\beta^{\mathsf T}X^{\mathsf T}X\boldsymbol\beta+\lambda\boldsymbol\beta^{\mathsf T}\boldsymbol\beta$, so
> $$\nabla L_\lambda(\boldsymbol\beta)=-2X^{\mathsf T}\mathbf y+2\big(X^{\mathsf T}X+\lambda I\big)\boldsymbol\beta,\qquad \boxed{\nabla^2L_\lambda=2\big(X^{\mathsf T}X+\lambda I\big)}$$
> **The Hessian is constant** — $L_\lambda$ is a quadratic, so its curvature does not vary. Convexity is therefore a single matrix question, not a pointwise one.
>
> **(b)** $X^{\mathsf T}X\succeq0$ always, since $\boldsymbol\beta^{\mathsf T}X^{\mathsf T}X\boldsymbol\beta=\lVert X\boldsymbol\beta\rVert^2\ge0$. **So $L_0$ is always convex.** It is *strictly* convex iff $X^{\mathsf T}X\succ0$, i.e. iff $\lVert X\boldsymbol\beta\rVert^2>0$ for all $\boldsymbol\beta\ne\mathbf 0$, i.e. iff $X$ has **full column rank $p$**.
>
> **When $p>n$ this is impossible**: $\operatorname{rank}(X)\le n<p$, so $X$ has a non-trivial null space. Any $\mathbf v\in\mathcal N(X)$ gives $\lVert X\mathbf v\rVert^2=0$, so $X^{\mathsf T}X$ is singular and $L_0$ is convex but **flat along an $(p-\operatorname{rank} X)$-dimensional affine subspace of minimizers.** *(Verified: with $n=5$, $p=8$ and random $X$, $\operatorname{rank}(X^{\mathsf T}X)=5<8$ and its smallest eigenvalue is $0$ to machine precision.)*
>
> **OLS has no unique solution when $p>n$** — and by §6's Corollary 22.1 the solution set is convex, which here means it is an affine subspace.
>
> **(c)** For any $\boldsymbol\beta\ne\mathbf 0$,
> $$\boldsymbol\beta^{\mathsf T}\big(X^{\mathsf T}X+\lambda I\big)\boldsymbol\beta=\lVert X\boldsymbol\beta\rVert^2+\lambda\lVert\boldsymbol\beta\rVert^2\ \ge\ \lambda\lVert\boldsymbol\beta\rVert^2>0$$
> **so $\nabla^2L_\lambda\succ0$ regardless of $X$**, and $L_\lambda$ is strictly convex. *(Equivalently: the eigenvalues of $X^{\mathsf T}X+\lambda I$ are $\mu_i+\lambda\ge\lambda>0$ where $\mu_i\ge0$ are those of $X^{\mathsf T}X$. In the $n=5,p=8$ example above the smallest eigenvalue moves from $0$ to exactly $\lambda=0.7$.)*
>
> Setting $\nabla L_\lambda=\mathbf 0$ and invoking §6's Corollary 22.2 (**stationary + convex $\Rightarrow$ global**):
> $$\boxed{\hat{\boldsymbol\beta}_\lambda=\big(X^{\mathsf T}X+\lambda I\big)^{-1}X^{\mathsf T}\mathbf y}$$
> and by §5 this is the **unique** global minimizer.
>
> **(d) What was bought.** Three things at once, in this order:
> 1. **Invertibility.** $X^{\mathsf T}X+\lambda I$ is non-singular for every $X$, so the estimator is *defined* when OLS is not.
> 2. **Uniqueness**, by §5.
> 3. **Conditioning.** The condition number drops from $\mu_{\max}/\mu_{\min}$ (infinite when $X$ is rank-deficient) to $(\mu_{\max}+\lambda)/(\mu_{\min}+\lambda)$, **which bounds how slowly gradient descent will converge** — see [[05 - Gradient Methods|ch. 05]]. This is the same phenomenon [[Econometrics/contents/00-Index|Econometrics]] calls multicollinearity.
>
> **What it cost.** $\hat{\boldsymbol\beta}_\lambda$ is a **biased** estimator, and the bias grows with $\lambda$. **The optimization-theoretic gain is unconditional; the statistical gain is a bias–variance trade-off that holds only for some $\lambda$** — which is why $\lambda$ is chosen by cross-validation and not by any argument in this chapter.

---

> [!question] Exercise 5 — Jensen, and two consequences *(hard)*
> **(a)** State Jensen's inequality for a convex $f$ and prove the finite form by induction.
> **(b)** Use the concavity of $\log$ to prove the **weighted AM–GM inequality**: for $x_i>0$ and weights $\alpha_i\ge0$ with $\sum\alpha_i=1$,
> $$\prod_i x_i^{\alpha_i}\ \le\ \sum_i\alpha_ix_i$$
> **(c)** Show that the logistic regression negative log-likelihood
> $$\ell(\boldsymbol\beta)=\sum_{i=1}^n\log\!\big(1+e^{-y_i\mathbf x_i^{\mathsf T}\boldsymbol\beta}\big),\qquad y_i\in\{-1,+1\}$$
> is convex in $\boldsymbol\beta$, **twice** — once with §4's table and once with the Hessian. What does this tell you that the neural-network case does not enjoy?

> [!example]- Solution
> **(a) Statement.** For convex $f$, weights $\alpha_i\ge0$ with $\sum_{i=1}^m\alpha_i=1$, and $\mathbf x_i\in\Omega$:
> $$f\left(\sum_{i=1}^m\alpha_i\mathbf x_i\right)\le\sum_{i=1}^m\alpha_if(\mathbf x_i)$$
>
> **Proof by induction on $m$.** $m=2$ is the definition. Assume it for $m$, and take $m+1$ points with $\sum_{i=1}^{m+1}\alpha_i=1$. If $\alpha_{m+1}=1$ there is nothing to prove, so assume $s=\sum_{i=1}^m\alpha_i=1-\alpha_{m+1}>0$ and write
> $$\sum_{i=1}^{m+1}\alpha_i\mathbf x_i=s\underbrace{\left(\sum_{i=1}^m\frac{\alpha_i}{s}\mathbf x_i\right)}_{=\ \mathbf z,\ \text{a convex combination}}+\ \alpha_{m+1}\mathbf x_{m+1}$$
> The weights $\alpha_i/s$ sum to 1, so $\mathbf z\in\Omega$ and the two-point case applies:
> $$f\left(\sum_{i=1}^{m+1}\alpha_i\mathbf x_i\right)\le s\,f(\mathbf z)+\alpha_{m+1}f(\mathbf x_{m+1})\ \underbrace{\le}_{\text{induction on }\mathbf z}\ s\sum_{i=1}^m\frac{\alpha_i}{s}f(\mathbf x_i)+\alpha_{m+1}f(\mathbf x_{m+1})=\sum_{i=1}^{m+1}\alpha_if(\mathbf x_i)\ \ \blacksquare$$
>
> **Probabilistic form:** taking $\alpha_i$ to be a probability distribution and passing to the limit gives $f(\mathbb E[X])\le\mathbb E[f(X)]$, with the inequality reversed for concave $f$.
>
> **(b)** $\log$ is concave on $(0,\infty)$, since $(\log x)''=-1/x^2<0$. Applying Jensen **with the inequality reversed**:
> $$\log\left(\sum_i\alpha_ix_i\right)\ \ge\ \sum_i\alpha_i\log x_i=\log\left(\prod_i x_i^{\alpha_i}\right)$$
> Exponentiating (which is increasing, so preserves $\ge$):
> $$\sum_i\alpha_ix_i\ \ge\ \prod_ix_i^{\alpha_i}\qquad\blacksquare$$
> **With $\alpha_i=1/m$ this is the classical AM–GM inequality**, $\frac{x_1+\cdots+x_m}{m}\ge\sqrt[m]{x_1\cdots x_m}$. **Equality holds iff all $x_i$ are equal**, because $\log$ is *strictly* concave.
>
> **(c) Route 1 — the table of §4, in four steps.**
> 1. $g(t)=\log(1+e^{t})$ is convex: $g''(t)=\dfrac{e^t}{(1+e^t)^2}>0$ for all $t$.
> 2. $\mathbf \beta\mapsto -y_i\mathbf x_i^{\mathsf T}\boldsymbol\beta$ is **affine**.
> 3. **Convex $\circ$ affine is convex**, so each term $\log\!\big(1+e^{-y_i\mathbf x_i^{\mathsf T}\boldsymbol\beta}\big)$ is convex in $\boldsymbol\beta$.
> 4. **A non-negative sum of convex functions is convex**, so $\ell$ is convex. $\blacksquare$
>
> **No matrices were needed.** This is the point of §4's table.
>
> **Route 2 — the Hessian.** Write $p_i=\sigma(\mathbf x_i^{\mathsf T}\boldsymbol\beta)$ with $\sigma(t)=1/(1+e^{-t})$. Differentiating twice gives
> $$\nabla^2\ell(\boldsymbol\beta)=X^{\mathsf T}DX,\qquad D=\operatorname{diag}\big(p_i(1-p_i)\big)$$
> Since $0<p_i<1$, every diagonal entry is **strictly positive**, so for any $\mathbf v$,
> $$\mathbf v^{\mathsf T}X^{\mathsf T}DX\mathbf v=\sum_i p_i(1-p_i)\,(\mathbf x_i^{\mathsf T}\mathbf v)^2\ \ge\ 0$$
> **so $\nabla^2\ell\succeq0$ and $\ell$ is convex.** *(Verified numerically: for random $X\in\mathbb R^{20\times4}$ and random $\boldsymbol\beta$, the Hessian's eigenvalues are $\{1.65,\ 3.40,\ 4.98,\ 6.62\}$ — all positive.)* It is **strictly** convex iff $X$ has full column rank; note the Hessian **depends on $\boldsymbol\beta$**, unlike the quadratic case in Exercise 4.
>
> **What this buys, and what a network does not get.** Because $\ell$ is convex:
> - **any stationary point is a global minimum** (§6, Cor. 22.2);
> - **the starting point of the optimizer is irrelevant** to the answer;
> - **two people fitting the same model to the same data get the same coefficients**, so the fit is a property of the data rather than of the software;
> - a duality gap gives a **certificate**: you can bound how far from optimal you are ([[10 - Duality|ch. 10]]).
>
> **Now insert one hidden layer.** The map $\boldsymbol\beta\mapsto\mathbf x^{\mathsf T}\boldsymbol\beta$ is replaced by $W_2\,\phi(W_1\mathbf x)$, which is **not affine in the parameters**. Step 2 of Route 1 fails, and every consequence above fails with it. **Not one of the four bullets survives** — which is the precise, structural reason a neural network's training run is a different kind of object from a logistic regression's, and why reporting a network's result requires reporting the seed.

---

## 📝 Summary

- **A set is convex if the segment between any two of its points stays inside.** Hyperplanes, halfspaces, balls, linear varieties and the non-negative orthant are convex; **arbitrary intersections, sums and non-negative scalings preserve convexity, and unions do not.**
- **A polyhedron is an intersection of finitely many halfspaces; a polytope is a bounded one.** **Chong & Żak use these two words in the opposite sense** to Bertsimas & Tsitsiklis and to modern practice — check which book you are reading.
- **A function is convex iff its epigraph is a convex set**, equivalently iff **the chord lies above the graph**: $f(\alpha\mathbf x+(1-\alpha)\mathbf y)\le\alpha f(\mathbf x)+(1-\alpha)f(\mathbf y)$. **Jensen's inequality is the same statement for many points, or for $\mathbb E$.**
- **First-order test:** $f(\mathbf y)\ge f(\mathbf x)+\nabla f(\mathbf x)^{\mathsf T}(\mathbf y-\mathbf x)$ — **the linear approximation is a global underestimate.** **Second-order test:** $\nabla^2f\succeq0$ everywhere. $\nabla^2f\succ0$ implies strict convexity but not conversely ($x^4$).
- **The calculus of convexity is usually faster than any Hessian:** non-negative sums, maxima (over any family), affine precomposition, and $g\circ f$ with $g$ convex **non-decreasing**. **Products and minima are not preserved.**
- **Strict convexity gives at most one global minimizer.** With coercivity from [[01 - The Optimization Problem|ch. 01]], **exactly one** — which is what a ridge penalty manufactures, for any $X$, including $p>n$.
- **Local implies global for convex problems**, the set of minimizers is convex, sublevel sets are convex, and **$\nabla f=\mathbf 0$, the Lagrange condition and the KKT conditions all become *sufficient*.**
- **Convex sublevel sets do not imply a convex function** — that is quasiconvexity, and none of the results above hold for it.

---

## ⚠️ Important Notes

> [!warning] The six errors this chapter is designed to prevent
> 1. **Checking convexity by looking at level curves.** That tests **quasiconvexity**, which gives you nothing. Use the Hessian or §4's table.
> 2. **Using leading principal minors to test *semi*definiteness.** Sylvester's criterion is for definiteness only; $\operatorname{diag}(0,-1)$ passes and is negative semidefinite. **For $\succeq$, use eigenvalues.**
> 3. **Confusing "positive definite" with "positive entries."** $\begin{pmatrix}1&2\\2&1\end{pmatrix}$ has all-positive entries and eigenvalues $3,-1$.
> 4. **Assuming products of convex functions are convex.** $x\cdot x^2=x^3$.
> 5. **Forgetting the monotonicity hypothesis in $g\circ f$.** $g(t)=t^2$ with $f(x)=x^2-1$ gives a non-convex composition.
> 6. **Mixing the two books' polytope/polyhedron conventions.**

> [!tip] How to check convexity in practice, in order of cost
> 1. **Is it built from known-convex pieces by the operations in §4?** Norms, affine functions, $\max$, non-negative sums, $\log(1+e^t)$, $e^t$, $-\log t$, $t\log t$. **This settles most real cases in seconds.**
> 2. **Is it a quadratic?** Then the Hessian is constant and you have a single matrix to classify.
> 3. **Otherwise compute $\nabla^2f$** and test definiteness **at every point of the domain**, not just at a critical point.
> 4. **To disprove convexity, one counterexample suffices** — a single triple $\mathbf x,\mathbf y,\alpha$ violating the chord inequality.

> [!note] Where this chapter is used
> - **[[03 - Unconstrained Optimality Conditions|Ch. 03]]** gives conditions that are necessary in general; **§6 here is what upgrades them to sufficient.**
> - **[[09 - Linear Programming and the Simplex Method|Ch. 09]]** lives entirely in §2's geometry — the feasible set is a polyhedron, and the optimum is at an extreme point.
> - **[[10 - Duality|Ch. 10]]** is built on separating hyperplanes, and its dual function is concave **because of Exercise 3(b)'s infinite-family maximum rule.**
> - **[[11 - Constrained Optimization - Lagrange and KKT|Ch. 11]]–[[12 - Convex Programming and Constrained Algorithms|12]]**: KKT is necessary in ch. 11 and **sufficient** in ch. 12, and this chapter is the difference.
> - **[[Machine Learning/contents/00-Index|Machine Learning]]** — Exercise 5(c) is the structural reason linear models are reproducible and networks are not.
> - **[[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]]** — Jensen's inequality, in the $\mathbb E$ form.

---

> [!warning] Gaps in the source material
> **Source split.** Definitions, theorem statements and proof structure follow **Chong & Żak ch. 4 and §§22.1–22.3**, whose prose extracts adequately. **Every displayed matrix and every fraction had to be reconstructed** (see below) and checked numerically.
>
> **Chong & Żak OCR damage in these sections:**
> - **Every matrix loses its brackets and row structure.** The Hessian of Example 22.6 arrives as `F(x) 8 6 1 6 6 0 1 0 10` with no delimiters; the reader must guess it is $3\times3$. **All three of Example 22.6's matrices were reconstructed and re-verified.**
> - **`Θ` and `Ω` interchange freely with `θ`, `©`, `0` and `G`**, so `u,v G Θ` is $\mathbf u,\mathbf v\in\Theta$ and `©i + Θ2` is $\Theta_1+\Theta_2$. In the proof of Theorem 4.1 the variable `x` is repeatedly OCR'd as `05`, `05i`, `θ52` and `α;`.
> - **`φ` is $\ne$, `—►` is $\to$, `\\·\\` is $\lVert\cdot\rVert$, `£` and `G` are both $\in$**, and `M.3`, `W1`, `Mn`, `Rn` are all $\mathbb R^n$ for varying $n$.
> - **Fractions are silently deleted.** In Example 22.5 the matrix $Q$ for $f(\mathbf x)=x_1x_2$ extracts as $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ — **which gives $\mathbf x^{\mathsf T}Q\mathbf x=2x_1x_2$, not $x_1x_2$.** The correct matrix is $\tfrac12\begin{pmatrix}0&1\\1&0\end{pmatrix}$, and **the book's own printed answer $(\mathbf y-\mathbf x)^{\mathsf T}Q(\mathbf y-\mathbf x)=-1$ confirms it**: with the $\tfrac12$ the value is $-1$; without it, $-2$. **So this is an extraction artefact, not an error in the book** — but it is exactly the kind that would go unnoticed, since both matrices are symmetric and both give the same conclusion.
> - **Every figure is an image and all are lost.** The casualties matter here more than usual: **Figures 4.4/4.5 (convex vs non-convex sets), 4.6 (intersection), 4.10/4.11 (polytopes), 22.4 (graph and epigraph), 22.5 (the chord inequality) and 22.6 (the tangent lying below the graph)** — that is, **the pictures that *are* the definitions.** §§1, 3 and 4 above have to state in words what six figures show at a glance. **Figures 22.1–22.3, which motivate the whole chapter by showing three ways constraints can behave, are also lost.**
>
> **Verification performed.** Every numeric claim was recomputed with `sympy` and `numpy`:
> - **C&Ż Example 22.6**, all three parts: the Hessian $\begin{psmallmatrix}8&6&1\\6&6&0\\1&0&10\end{psmallmatrix}$, its leading minors $8,\ 12,\ 114$ **(all as printed)** and its eigenvalues $\{13.26,\ 9.87,\ 0.871\}$, confirming positive definiteness; $f''=-16$ for $-8x^2$; and $\begin{psmallmatrix}-2&2\\2&-2\end{psmallmatrix}$ with eigenvalues $\{0,-4\}$, confirming negative *semi*definiteness.
> - **C&Ż Examples 22.4 and 22.5**: the chord violation at $\alpha=\tfrac12$ ($2.25>2$) and the quadratic-form value $-1$, which is what identified the missing $\tfrac12$ above.
> - **All four parts of Exercise 2**: Hessians, leading minors and eigenvalues.
> - **Exercise 4**: with $n=5$, $p=8$ and random $X$, $\operatorname{rank}(X^{\mathsf T}X)=5$ and $\lambda_{\min}(X^{\mathsf T}X)=0$; adding $\lambda=0.7$ moves the smallest eigenvalue to exactly $0.7$, and the ridge solution exists and is unique.
> - **Exercise 5(c)**: the logistic Hessian's eigenvalues $\{1.65,\ 3.40,\ 4.98,\ 6.62\}$, all positive.
> - **Log-sum-exp convexity** was checked by 20,000 random midpoint tests with **zero violations**, before being used in the discussion.
>
> **One genuine defect, and it is terminological rather than mathematical.** **Chong & Żak §4.5 defines "convex polytope" as an intersection of finitely many halfspaces and "polyhedron" as a bounded polytope — the reverse of the standard convention, and the reverse of Bertsimas & Tsitsiklis §2.1, which sits in the same `documents/` folder.** Neither book is *wrong* internally; the older usage is defensible. **But a student reading both will silently import the wrong meaning**, and since ch. 09–10 draw on both books this had to be resolved. **These notes use the modern convention throughout and say so at the point of first use.**
>
> **Otherwise no mathematical error was found in either book in the sections used.**
>
> **Scope and additions.**
> - **§4's "calculus of convexity" table is my own.** Chong & Żak prove only the two easiest closure properties (non-negative scaling and sums, Theorem 22.3) and relegate $\max$ to Exercise 22.6. **The affine-precomposition and monotone-composition rules — which are how convexity is actually established in practice — appear in neither book**, and Exercise 3 supplies proofs.
> - **§5 (strict convexity $\Rightarrow$ uniqueness) is stated and proved here but in neither source.** Chong & Żak define strict convexity (Definition 22.4) and never use it; Luenberger & Ye's ch. 7 is a general-theory chapter that does not reach it. **It is included because combined with [[01 - The Optimization Problem|ch. 01]]'s coercivity result it gives the complete existence-and-uniqueness statement**, which is the actual justification for ridge regression as an optimization technique.
> - **The subgradient remark in §4 is Chong & Żak's** (they define it in one paragraph after Theorem 22.4 and never return to it); **the connection to the LASSO is mine.**
> - **§6's closing note on deep learning, the quasiconvexity warning, and all of Exercise 5(c) are my own additions.** No book in this folder discusses non-convex training, and stating plainly which guarantees are lost seemed more useful than leaving the reader to infer it.

#optimization #convexity #convex-set #convex-function #epigraph #hessian #jensen #polyhedron #strict-convexity
