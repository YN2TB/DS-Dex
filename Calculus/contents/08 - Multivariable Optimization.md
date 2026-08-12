---
subject: Calculus
chapter: 08
tags: [ds, calculus, optimization, critical-points, hessian, saddle-point, lagrange-multipliers, constrained-optimization]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., §§14.7–14.8 (pp. 1008–1028)"
---

# Multivariable Optimization

> [!abstract] What this chapter is for
> **Every fitted model is a minimisation over several variables**, so this short chapter is the one a data-science reader will use most often.
>
> **Two problems, and the second is the interesting one:**
>
> | Problem | Condition |
> |---|---|
> | **Unconstrained:** minimise $f(\mathbf x)$ | $\nabla f=\mathbf 0$, then check the **Hessian** |
> | **Constrained:** minimise $f$ subject to $g=c$ | $\boxed{\nabla f=\lambda\nabla g}$ |
>
> **The constrained condition is not an extra rule to memorise** — it follows in one line from [[07 - Partial Derivatives and the Gradient|ch. 07's]] fact that the gradient is perpendicular to level sets.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Critical points | $\nabla f=\mathbf 0$ — necessary, **never sufficient** |
> | **2** | **The second-derivative test** | $D=f_{xx}f_{yy}-f_{xy}^2$; **$D<0$ means a saddle** |
> | **3** | The Hessian | The test, stated properly and generalised to $n$ variables |
> | **4** | Closed bounded regions | The Extreme Value Theorem, and **the boundary** |
> | **5** | **Lagrange multipliers** | Constrained optimisation, and what $\lambda$ *means* |
>
> **The saddle point is the genuinely new phenomenon.** In one variable a critical point is a max, a min, or an inflection; **in two or more there is a fourth possibility with no 1-D analogue**, and it is the dominant feature of high-dimensional loss surfaces.

---

## 📘 Main Knowledge

### 1. Critical points

> [!important] Definitions and Fermat's theorem
> $f$ has a **local maximum** at $(a,b)$ if $f(a,b)\ge f(x,y)$ for all $(x,y)$ near $(a,b)$; similarly for minima.
>
> **If $f$ has a local extremum at $(a,b)$ and the partials exist there, then**
> $$f_x(a,b)=f_y(a,b)=0,\qquad\text{i.e.}\qquad \nabla f(a,b)=\mathbf 0$$
> Such a point is a **critical point**.

**The reason is [[03 - Applications of Differentiation|ch. 03's]] Fermat theorem applied one variable at a time**: at a local max, the single-variable function $x\mapsto f(x,b)$ has a local max at $x=a$, so its derivative $f_x(a,b)$ vanishes.

> [!warning] $\nabla f=\mathbf 0$ is necessary and not sufficient — and the failure mode is new
> **In one variable the possibilities were max, min, or inflection. Here there is a fourth:**
> $$f(x,y)=x^2-y^2$$
> has $\nabla f(0,0)=\mathbf 0$, **rises along the $x$-axis and falls along the $y$-axis** — a **saddle point**.
>
> **A saddle is a minimum in some directions and a maximum in others**, which is impossible in one dimension. **And it is the typical critical point in high dimensions**: for a random symmetric Hessian, all $n$ eigenvalues having the same sign becomes exponentially unlikely as $n$ grows.
>
> **This is why "stuck in a local minimum" is largely the wrong worry for deep networks** — saddle points vastly outnumber local minima, and the practical difficulty is the flat regions around them ([[Machine Learning/contents/00-Index|Machine Learning]]).

---

### 2. The Second Derivatives Test

> [!important] The test (two variables)
> Suppose the second partials are continuous near $(a,b)$ and $\nabla f(a,b)=\mathbf 0$. Let
> $$D=D(a,b)=f_{xx}f_{yy}-\big(f_{xy}\big)^2$$
> | Case | Conclusion |
> |---|---|
> | $D>0$ and $f_{xx}>0$ | **local minimum** |
> | $D>0$ and $f_{xx}<0$ | **local maximum** |
> | $D<0$ | **saddle point** |
> | $D=0$ | **no conclusion** |

> [!tip] $D$ is a determinant, and that is the whole explanation
> $$D=\det\begin{bmatrix}f_{xx}&f_{xy}\\ f_{yx}&f_{yy}\end{bmatrix}=\det H$$
> **— the determinant of the Hessian.** By [[Linear Algebra/contents/03 - Determinants and Diagonalization|Linear Algebra ch. 03]] the determinant is the product of the eigenvalues, so
>
> | $\det H$ | Eigenvalues | Shape |
> |---|---|---|
> | $>0$, $f_{xx}>0$ | both **positive** | bowl — **minimum** |
> | $>0$, $f_{xx}<0$ | both **negative** | dome — **maximum** |
> | $<0$ | **opposite signs** | **saddle** |
> | $=0$ | at least one **zero** | degenerate — test fails |
>
> **"Opposite signs" is exactly "up in one direction, down in another"** — the eigenvectors are the directions and the eigenvalues are the curvatures. **The mysterious formula $f_{xx}f_{yy}-f_{xy}^2$ is just $\lambda_1\lambda_2$.**

> [!example] $f(x,y)=x^4+y^4-4xy+1$ *(all verified)*
> $$\nabla f=(4x^3-4y,\ 4y^3-4x)=\mathbf 0\ \Longrightarrow\ y=x^3\text{ and }x=y^3\ \Longrightarrow\ x^9=x$$
> giving the real critical points $(0,0)$, $(1,1)$, $(-1,-1)$.
>
> With $f_{xx}=12x^2$, $f_{yy}=12y^2$, $f_{xy}=-4$:
> | Point | $D$ | $f_{xx}$ | Conclusion | $f$ |
> |---|---|---|---|---|
> | $(0,0)$ | $-16$ | $0$ | **saddle** | $1$ |
> | $(1,1)$ | $128$ | $12$ | **local min** | $-1$ |
> | $(-1,-1)$ | $128$ | $12$ | **local min** | $-1$ |
>
> **Two minima and a saddle between them** — the standard picture, and one that gradient descent can traverse in either direction depending on where it starts.

---

### 3. The Hessian, in $n$ variables

> [!important] The general statement
> $$H=\big[f_{x_ix_j}\big]_{n\times n}$$
> is **symmetric** whenever the second partials are continuous (Clairaut, [[07 - Partial Derivatives and the Gradient|ch. 07]]), so by the **spectral theorem** ([[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]) it has real eigenvalues and an orthonormal eigenbasis. At a critical point:
>
> | $H$ | Eigenvalues | Conclusion |
> |---|---|---|
> | **positive definite** | all $>0$ | **local minimum** |
> | **negative definite** | all $<0$ | **local maximum** |
> | **indefinite** | mixed signs | **saddle** |
> | singular | some $=0$ | inconclusive |

> [!tip] The second-order Taylor expansion is why
> Near a critical point,
> $$f(\mathbf a+\mathbf h)\approx f(\mathbf a)+\underbrace{\nabla f\cdot\mathbf h}_{=0}+\tfrac12\mathbf h^{\mathsf T}H\mathbf h$$
> **so the behaviour is decided entirely by the quadratic form $\mathbf h^{\mathsf T}H\mathbf h$** — which is positive for all $\mathbf h\ne\mathbf 0$ exactly when $H$ is positive definite.
>
> **This is [[06 - Sequences, Series and Taylor Approximation|ch. 06's]] Taylor expansion and [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08's]] positive definiteness meeting**, and it is why the second-derivative test looks like a definiteness test: because it *is* one.
>
> **Practical test:** all **leading principal minors** positive $\Rightarrow$ positive definite. In two variables those are $f_{xx}$ and $\det H$ — **exactly the conditions in §2.**

> [!important] The eigenvalues also predict how hard the optimisation will be
> **The condition number $\kappa=\lambda_{\max}/\lambda_{\min}$ of the Hessian controls gradient descent's convergence rate.** A large $\kappa$ means a long narrow valley: the steepest direction points across the valley rather than along it, and the iteration zig-zags.
>
> **This is the quantitative version of [[07 - Partial Derivatives and the Gradient|ch. 07's]] warning that "steepest is not fastest"**, and it is why Newton-type methods (which multiply by $H^{-1}$ and so make $\kappa=1$) converge in far fewer steps.

---

### 4. Absolute extrema on a closed bounded region

> [!important] The Extreme Value Theorem and the method
> **A continuous $f$ on a closed bounded region $D\subseteq\mathbb{R}^2$ attains an absolute max and min.** To find them:
> 1. find the values at all **critical points inside $D$**;
> 2. find the extreme values **on the boundary** of $D$;
> 3. take the largest and smallest.

> [!warning] The boundary is where the answer usually is, and $\nabla f\ne\mathbf 0$ there
> **A constrained optimum sits on the boundary, where the gradient need not vanish** — $f$ would keep increasing if only the region allowed it.
>
> **So step 2 is a genuinely different problem**, and it is a *constrained* one: optimise $f$ along a curve. **That is precisely what §5 solves**, and it is why Lagrange multipliers and the boundary case are the same topic.
>
> **The applied version of this warning:** in a constrained fit — non-negative coefficients, a probability simplex, a norm ball — **the optimum frequently lies on the boundary, and a solver that only looks for $\nabla f=\mathbf 0$ will never find it.** *(This is exactly why LASSO produces exact zeros.)*

---

### 5. Lagrange multipliers

> [!important] The method
> To find extrema of $f(\mathbf x)$ subject to $g(\mathbf x)=k$, solve
> $$\boxed{\ \nabla f=\lambda\nabla g\ }\qquad\text{together with}\qquad g(\mathbf x)=k$$
> **for $\mathbf x$ and $\lambda$, then evaluate $f$ at each solution.**
>
> **With two constraints $g=k$, $h=c$:** $\ \nabla f=\lambda\nabla g+\mu\nabla h$.

> [!tip] Why it is true — one line from [[07 - Partial Derivatives and the Gradient|ch. 07]]
> **At a constrained optimum, moving along the constraint curve cannot increase $f$ to first order.** So $\nabla f$ has **no component along the curve**, i.e. $\nabla f$ is perpendicular to the constraint curve.
>
> **But $\nabla g$ is also perpendicular to that curve** — it is a level set of $g$. **Two vectors perpendicular to the same curve in the plane are parallel**, hence $\nabla f=\lambda\nabla g$. $\blacksquare$
>
> **Geometrically: at the optimum the level curves of $f$ and the constraint curve are *tangent*.** Sliding along the constraint, you are momentarily travelling along a contour of $f$ — and if you were crossing contours you could still improve.

> [!example] Three worked problems *(all verified)*
> **Maximise $xy$ subject to $x+y=10$.** $\nabla f=(y,x)$, $\nabla g=(1,1)$:
> $$y=\lambda,\quad x=\lambda,\quad x+y=10\ \Longrightarrow\ x=y=5,\ \lambda=5,\ f_{\max}=25$$
>
> **Closest point on $x+2y=5$ to the origin.** Minimise $x^2+y^2$:
> $$2x=\lambda,\ 2y=2\lambda,\ x+2y=5\ \Longrightarrow\ (x,y)=(1,2),\ \lambda=2,\ \text{distance}=\sqrt5$$
>
> **Extrema of $x^2+2y^2$ on the unit circle $x^2+y^2=1$:**
> $$(\pm1,0)\ \text{with}\ f=1,\ \lambda=1;\qquad (0,\pm1)\ \text{with}\ f=2,\ \lambda=2$$
> **So the minimum is 1 and the maximum is 2.**

> [!important] What $\lambda$ means — and it is not a bookkeeping device
> $$\boxed{\ \lambda=\frac{d f_{\text{opt}}}{dk}\ }$$
> **— $\lambda$ is the rate at which the optimal value improves as the constraint is relaxed.**
>
> **The names it goes by elsewhere are all the same quantity:**
> | Field | Name |
> |---|---|
> | Economics | **shadow price**, marginal utility of income |
> | Optimisation | **dual variable** |
> | Machine learning | the regularisation trade-off in a constrained formulation |
>
> **In the third example above, $\lambda$ equalled the optimal value of $f$ at each solution** — a coincidence of that particular homogeneous problem, but a useful reminder that $\lambda$ carries information rather than being discarded.

> [!warning] Lagrange finds candidates, not answers
> **The method produces points where the tangency condition holds. It does not say which are maxima, which are minima, and which are neither.**
>
> **Compare the values of $f$ at every solution**, and — if the constraint set is unbounded — **check that an extremum exists at all.** (Minimising $x$ on the line $y=0$ has a stationary condition with no solution, because there is no minimum.)
>
> **Two further requirements:** $\nabla g\ne\mathbf 0$ at the candidate (otherwise the tangency argument collapses), and the constraint set must be regular enough that "perpendicular to the constraint" is meaningful.

---

## ✏️ Exercises

> [!question] Exercise 1 — critical points and the second-derivative test *(warm-up)*
> (i) Find and classify the critical points of $f(x,y)=x^4+y^4-4xy+1$.
> (ii) Classify the critical point of $g(x,y)=x^2-y^2$ at the origin.
> (iii) Show the test is inconclusive for $h(x,y)=x^4+y^4$ at the origin, and classify the point anyway.
> (iv) Why is there no one-variable analogue of a saddle point?

> [!example]- Solution
> **(i)** $\nabla f=(4x^3-4y,\ 4y^3-4x)=\mathbf 0$ gives $y=x^3$ and $x=y^3$, so $x=x^9$, i.e. $x(x^8-1)=0$ and (over $\mathbb{R}$) $x\in\{0,1,-1\}$. **Critical points $(0,0)$, $(1,1)$, $(-1,-1)$.**
>
> With $f_{xx}=12x^2$, $f_{yy}=12y^2$, $f_{xy}=-4$, so $D=144x^2y^2-16$:
> | Point | $D$ | $f_{xx}$ | Type |
> |---|---|---|---|
> | $(0,0)$ | $-16$ | $0$ | **saddle** |
> | $(1,1)$ | $128$ | $12$ | **local min**, $f=-1$ |
> | $(-1,-1)$ | $128$ | $12$ | **local min**, $f=-1$ |
>
> *(All verified.)* **Note $f_{xx}=0$ at the saddle and the test still decides**, because $D<0$ alone is conclusive.
>
> **(ii)** $\nabla g=(2x,-2y)=\mathbf 0$ at the origin, and $D=(2)(-2)-0=\boxed{-4<0}$ — **a saddle** *(verified)*.
>
> **Directly: $g(x,0)=x^2$ has a minimum along the $x$-axis, and $g(0,y)=-y^2$ has a maximum along the $y$-axis.** The Hessian's eigenvalues are $2$ and $-2$ — opposite signs, as the classification requires.
>
> **(iii)** $\nabla h=(4x^3,4y^3)=\mathbf 0$ at the origin, and $h_{xx}=12x^2$, $h_{yy}=12y^2$, $h_{xy}=0$, so
> $$D(0,0)=0\cdot0-0=0\quad\Longrightarrow\quad\textbf{inconclusive}$$
>
> **But $h(x,y)=x^4+y^4>0$ for every $(x,y)\ne(0,0)$ and $h(0,0)=0$ — so it is an absolute minimum**, established by inspection rather than by the test.
>
> **$D=0$ means the quadratic term vanishes in some direction and the fourth-order term decides.** The test only sees second derivatives, so it cannot.
>
> **(iv)** **In one dimension there is only one direction to move (and its reverse), so a critical point is a max, a min, or neither.** "Increasing one way and decreasing another" is impossible when there is only one way.
>
> **In two or more dimensions there are infinitely many directions, and $f$ can curve up along some and down along others** — the Hessian's eigenvalues can differ in sign. $\boxed{\text{Saddles need}\ \ge2\ \text{dimensions}}$
>
> > [!important] And in high dimensions saddles dominate
> > **For a critical point to be a local minimum, *all* $n$ eigenvalues of the Hessian must be positive.** If the signs were independent coin flips, that has probability $2^{-n}$ — **so in a network with millions of parameters, essentially every critical point is a saddle.**
> >
> > **This is why the "local minima" framing of deep-learning difficulty is largely wrong.** The real obstacles are the flat plateaus around saddles, where $\|\nabla f\|$ is small but no minimum has been reached.

> [!question] Exercise 2 — the Hessian
> (i) Write the Hessian of $f(x,y)=x^4+y^4-4xy+1$ and evaluate it at each critical point.
> (ii) Find the eigenvalues at $(1,1)$ and confirm the classification.
> (iii) Explain why the Hessian is symmetric, and what that buys you.
> (iv) State the $n$-variable version of the second-derivative test.

> [!example]- Solution
> **(i)** $$H=\begin{bmatrix}12x^2&-4\\-4&12y^2\end{bmatrix}$$
> $$H(0,0)=\begin{bmatrix}0&-4\\-4&0\end{bmatrix},\qquad H(\pm1,\pm1)=\begin{bmatrix}12&-4\\-4&12\end{bmatrix}$$
>
> **(ii)** For $\begin{bmatrix}12&-4\\-4&12\end{bmatrix}$: eigenvalues satisfy $(12-\lambda)^2=16$, so
> $$\lambda=12\pm4=16,\ 8$$
> **Both positive $\Rightarrow$ positive definite $\Rightarrow$ local minimum** ✓ — agreeing with $D=\lambda_1\lambda_2=128>0$ and $f_{xx}=12>0$.
>
> *(At the origin the eigenvalues are $\pm4$ — opposite signs, hence a saddle, and $\det=-16$ ✓.)*
>
> **The eigenvectors are $(1,-1)$ and $(1,1)$: the surface curves most sharply along $(1,-1)$ (curvature 16) and least along $(1,1)$ (curvature 8).** The condition number is $16/8=2$ — well conditioned, so gradient descent from nearby converges quickly.
>
> **(iii)** **Clairaut's theorem** ([[07 - Partial Derivatives and the Gradient|ch. 07]]): $f_{xy}=f_{yx}$ when both are continuous.
>
> **What it buys, by [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08's]] spectral theorem:**
> - **all eigenvalues are real** — so "positive", "negative" and "mixed" are the only possibilities, with no complex case to worry about;
> - **there is an orthonormal eigenbasis** — so the principal curvature directions are mutually perpendicular;
> - **the definiteness tests apply** — leading principal minors, Cholesky, and so on.
>
> **Without symmetry none of the classification machinery would exist.**
>
> **(iv)** At a critical point with $H$ the Hessian:
> $$H\text{ positive definite}\Rightarrow\text{local min};\quad \text{negative definite}\Rightarrow\text{local max};\quad \text{indefinite}\Rightarrow\text{saddle};\quad\text{singular}\Rightarrow\text{inconclusive}$$
> **and in practice one checks the leading principal minors** — which for $n=2$ reduces to "$f_{xx}>0$ and $\det H>0$", exactly §2.

> [!question] Exercise 3 — Lagrange multipliers
> (i) Maximise $f(x,y)=xy$ subject to $x+y=10$.
> (ii) Find the point on $x+2y=5$ closest to the origin.
> (iii) Find the extreme values of $f(x,y)=x^2+2y^2$ on the unit circle.
> (iv) In (i), interpret $\lambda$ by re-solving with the constraint $x+y=11$.

> [!example]- Solution
> **(i)** $\nabla f=(y,x)$, $\nabla g=(1,1)$, so $y=\lambda$ and $x=\lambda$; with $x+y=10$:
> $$\boxed{x=y=5,\quad \lambda=5,\quad f_{\max}=25}$$
> *(Verified.)* **Sanity check: among rectangles of fixed perimeter, the square has the largest area** ✓
>
> **(ii)** Minimise $x^2+y^2$ (the *squared* distance — a monotone transform, [[03 - Applications of Differentiation|ch. 03]]) subject to $x+2y=5$:
> $$2x=\lambda,\quad 2y=2\lambda,\quad x+2y=5$$
> From the first two, $y=2x$; substituting, $x+4x=5$ so $x=1$, $y=2$, $\lambda=2$.
> $$\boxed{(1,2),\quad \text{distance}=\sqrt5}$$
> *(Verified.)*
>
> **Geometric check: the closest point is the foot of the perpendicular from the origin, and $(1,2)$ is parallel to the line's normal $(1,2)$** ✓ — **which is exactly what $\nabla f\parallel\nabla g$ says here.**
>
> **(iii)** $\nabla f=(2x,4y)$, $\nabla g=(2x,2y)$:
> $$2x=2\lambda x,\qquad 4y=2\lambda y,\qquad x^2+y^2=1$$
> From the first: $x=0$ **or** $\lambda=1$. From the second: $y=0$ **or** $\lambda=2$.
> - $\lambda=1\Rightarrow y=0\Rightarrow x=\pm1$: $f=1$
> - $\lambda=2\Rightarrow x=0\Rightarrow y=\pm1$: $f=2$
>
> $$\boxed{\min=1\text{ at }(\pm1,0);\qquad \max=2\text{ at }(0,\pm1)}$$
> *(Verified.)*
>
> **Note the case split.** Dividing by $x$ in the first equation would silently assume $x\ne0$ and lose half the solutions — **the standard error in Lagrange problems.**
>
> **This is also an eigenvalue problem in disguise:** $\nabla f=\lambda\nabla g$ reads $\begin{bmatrix}1&0\\0&2\end{bmatrix}\mathbf x=\lambda\mathbf x$, **so the multipliers are the eigenvalues of the quadratic form and the extreme values are $\lambda_{\min}$ and $\lambda_{\max}$** — exactly [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08's]] result that $\max_{\|\mathbf x\|=1}\mathbf x^{\mathsf T}A\mathbf x=\lambda_{\max}$, **which is the theorem that makes PCA work.**
>
> **(iv)** With $x+y=11$ the same argument gives $x=y=5.5$ and $f_{\max}=30.25$.
> $$\Delta f_{\max}=30.25-25=5.25\qquad\text{against}\qquad \lambda\cdot\Delta k=5\times1=5$$
> **Close, and exact in the limit:** $f_{\max}(k)=k^2/4$, so $\frac{df_{\max}}{dk}=\frac k2=5$ at $k=10$ ✓
>
> > [!important] $\lambda$ is the price of the constraint
> > **"Relaxing the budget by one unit is worth $\lambda$ units of objective."** In the example, one more unit of perimeter buys about 5 more units of area.
> >
> > **This is the *shadow price* of economics and the *dual variable* of optimisation** — and it is why $\lambda$ should be reported, not discarded. In a resource-allocation problem it tells you what an extra unit of the scarce resource is worth, which is often the answer the question was really asking ([[Microeconomics/contents/00-Index|Microeconomics]]).

> [!question] Exercise 4 — applied optimisation
> (i) Find the box of maximum volume with surface area $12$.
> (ii) Fit a least-squares line to $(1,1)$, $(2,3)$, $(3,4)$ **by minimising the sum of squared residuals directly.**
> (iii) Verify your answer against the normal equations of [[Linear Algebra/contents/05 - The Vector Space Rn|Linear Algebra ch. 05]].
> (iv) Why does the least-squares objective have a unique minimum here?

> [!example]- Solution
> **(i)** Maximise $V=abc$ subject to $g=2(ab+bc+ac)=12$. Lagrange gives
> $$bc=2\lambda(b+c),\qquad ac=2\lambda(a+c),\qquad ab=2\lambda(a+b)$$
> Subtracting the first two: $c(b-a)=2\lambda(b-a)$, so $a=b$ or $c=2\lambda$; pursuing the symmetry gives $a=b=c$. Then $6a^2=12$, so
> $$\boxed{a=b=c=\sqrt2,\qquad V_{\max}=2\sqrt2\approx2.83}$$
> *(Verified.)*
>
> **The cube is optimal, as symmetry suggests** — and the Lagrange conditions are what turn that intuition into a proof rather than a guess.
>
> **(ii)** Minimise $S(m,b)=\sum(mx_i+b-y_i)^2$ over the three points:
> $$S=(m+b-1)^2+(2m+b-3)^2+(3m+b-4)^2$$
> Setting $\frac{\partial S}{\partial m}=\frac{\partial S}{\partial b}=0$ gives a $2\times2$ linear system with solution
> $$\boxed{m=\tfrac32,\qquad b=-\tfrac13}$$
> *(Verified.)* **The fitted line is $y=1.5x-\tfrac13$.**
>
> **(iii)** The normal equations $M^{\mathsf T}M\mathbf z=M^{\mathsf T}\mathbf y$ with $M=\begin{bmatrix}1&1\\1&2\\1&3\end{bmatrix}$, $\mathbf y=(1,3,4)$:
> $$M^{\mathsf T}M=\begin{bmatrix}3&6\\6&14\end{bmatrix},\qquad M^{\mathsf T}\mathbf y=\begin{bmatrix}8\\19\end{bmatrix}$$
> Solving: $3b+6m=8$ and $6b+14m=19$, giving $m=\tfrac32$, $b=-\tfrac13$ ✓ — **identical.**
>
> **The two derivations are the same computation.** Setting $\nabla S=\mathbf 0$ *is* the normal equations; **calculus and linear algebra reach it from opposite directions** — "the gradient of the squared error vanishes" versus "the residual is orthogonal to the column space".
>
> **(iv)** The Hessian of $S$ is
> $$H=2M^{\mathsf T}M=\begin{bmatrix}6&12\\12&28\end{bmatrix}$$
> which is **positive definite** ($6>0$ and $\det=168-144=24>0$). **A positive-definite Hessian everywhere means $S$ is strictly convex, so the critical point is the unique global minimum.**
>
> **And $M^{\mathsf T}M$ is positive definite precisely because the columns of $M$ are independent** ([[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]]) — **i.e. because the $x_i$ are not all equal.** **That single condition is what guarantees least squares has one answer**, and its failure is perfect multicollinearity ([[Econometrics/contents/00-Index|Econometrics]]).

> [!question] Exercise 5 — why the method works *(hard)*
> (a) Prove that at a constrained extremum of $f$ subject to $g=k$, we have $\nabla f=\lambda\nabla g$ (assuming $\nabla g\ne\mathbf 0$).
>
> (b) (i) Show that $\lambda=\dfrac{df_{\text{opt}}}{dk}$.
> (ii) Interpret this for a firm maximising output subject to a budget.
>
> (c) (i) Give a Lagrange problem where the method finds a point that is **neither** a maximum nor a minimum.
> (ii) Give one where the method finds nothing because **no extremum exists**.
> (iii) What must you always do after solving the Lagrange equations?

> [!example]- Solution
> **(a)** Let $\mathbf r(t)$ parametrise the constraint set $g=k$ with $\mathbf r(0)=\mathbf a$, the constrained extremum. Then $t\mapsto f(\mathbf r(t))$ has an ordinary local extremum at $t=0$, so by [[03 - Applications of Differentiation|Fermat]],
> $$0=\frac{d}{dt}f(\mathbf r(t))\bigg|_{t=0}=\nabla f(\mathbf a)\cdot\mathbf r'(0)$$
> **So $\nabla f(\mathbf a)$ is perpendicular to every curve in the constraint set — i.e. to its tangent space.**
>
> **But $\nabla g(\mathbf a)$ is perpendicular to that same tangent space** ([[07 - Partial Derivatives and the Gradient|ch. 07]], since the constraint set is a level set of $g$). In the plane, the orthogonal complement of a tangent line is one-dimensional, **so the two gradients are parallel:**
> $$\nabla f(\mathbf a)=\lambda\nabla g(\mathbf a)\quad\text{for some scalar }\lambda\qquad\blacksquare$$
>
> **The hypothesis $\nabla g\ne\mathbf 0$ is needed** — otherwise $\nabla g$ spans nothing and the conclusion is vacuous.
>
> **(b)(i)** Let $\mathbf x(k)$ be the optimiser as $k$ varies, and $f_{\text{opt}}(k)=f(\mathbf x(k))$. Differentiating by the chain rule:
> $$\frac{df_{\text{opt}}}{dk}=\nabla f\cdot\frac{d\mathbf x}{dk}=\lambda\,\nabla g\cdot\frac{d\mathbf x}{dk}$$
> And differentiating the constraint $g(\mathbf x(k))=k$:
> $$\nabla g\cdot\frac{d\mathbf x}{dk}=1$$
> **Substituting:** $\ \dfrac{df_{\text{opt}}}{dk}=\lambda$ $\blacksquare$
>
> **(ii)** For a firm maximising output $f$ subject to a budget $g=k$:
> $$\lambda=\frac{\text{extra output}}{\text{extra budget}}$$
> **— the marginal product of money, or the *shadow price* of the budget constraint.**
>
> **The decision rule follows immediately:** if $\lambda$ exceeds the cost of borrowing, borrow more. **A budget constraint with a large $\lambda$ is one worth relaxing**, and one with $\lambda=0$ is not binding at all.
>
> **(c)(i)** **Extremise $f(x,y)=x^3$ subject to $x+y=0$.** Then $\nabla f=(3x^2,0)$ and $\nabla g=(1,1)$, so $\nabla f=\lambda\nabla g$ needs $0=\lambda$ and $3x^2=\lambda=0$, giving $(0,0)$.
>
> **But along the constraint $y=-x$, $f=x^3$ takes both signs arbitrarily close to the origin** — the point is neither a max nor a min. **It is the constrained analogue of $x^3$'s inflection.**
>
> **(ii)** **Maximise $f(x,y)=x$ subject to $y=0$.** Then $\nabla f=(1,0)$ and $\nabla g=(0,1)$ are never parallel, **so the Lagrange system has no solution.**
>
> **Correctly so: $x$ is unbounded above on that line, and no maximum exists.** **The constraint set is closed but not bounded**, so the EVT does not apply.
>
> **(iii) Always do two things.**
>
> **First, check an extremum exists.** If the constraint set is **closed and bounded**, the EVT guarantees it. If not — as in (ii) — you must argue separately, or accept that there may be nothing to find.
>
> **Second, evaluate $f$ at every candidate and compare.** The method returns a list of points satisfying a *necessary* condition; **which is the maximum, which the minimum, and which neither is decided by comparing values, not by the equations.**
>
> > [!important] The pattern is the same as every other optimisation theorem in the degree
> > | Theorem | Gives | Does not give |
> > |---|---|---|
> > | EVT | an extremum **exists** | where |
> > | Fermat / $\nabla f=\mathbf 0$ | **candidates** | which is which |
> > | Second-derivative test | **local** classification | global |
> > | Lagrange | **candidates** under a constraint | existence or classification |
> >
> > **Existence, location and classification are three separate questions**, and no single theorem answers more than one. **This is the same discipline as [[03 - Applications of Differentiation|ch. 03]]'s closing warning**, and it is why a numerical optimiser reporting "converged" has answered only the middle question.

---

## 📝 Summary

- **$\nabla f=\mathbf 0$ defines a critical point — necessary, never sufficient.**
- **The saddle point is the genuinely new phenomenon**: a minimum in some directions and a maximum in others, impossible in one variable. **In high dimensions saddles vastly outnumber minima**, since all $n$ Hessian eigenvalues sharing a sign becomes exponentially unlikely.
- **Second-derivative test:** with $D=f_{xx}f_{yy}-f_{xy}^2=\det H$, $\ D>0$ and $f_{xx}>0$ gives a **minimum**, $D>0$ and $f_{xx}<0$ a **maximum**, **$D<0$ a saddle**, and $D=0$ nothing. **$D$ is the product of the Hessian's eigenvalues**, which is why the signs mean what they do.
- **The Hessian is symmetric (Clairaut), hence orthogonally diagonalizable with real eigenvalues** — which is what makes definiteness the right classification, via the second-order Taylor expansion $f\approx f(\mathbf a)+\tfrac12\mathbf h^{\mathsf T}H\mathbf h$.
- **In $n$ variables: positive definite $\Rightarrow$ min, negative definite $\Rightarrow$ max, indefinite $\Rightarrow$ saddle**, tested by leading principal minors. **The condition number $\lambda_{\max}/\lambda_{\min}$ predicts how slowly gradient descent will converge.**
- **On a closed bounded region, check interior critical points *and* the boundary** — and **the boundary is usually where the answer is**, with $\nabla f\ne\mathbf 0$ there.
- $$\boxed{\nabla f=\lambda\nabla g\quad\text{with}\quad g=k}$$ **is one line from "the gradient is perpendicular to level sets"**: at the optimum, the level curve of $f$ is tangent to the constraint.
- **$\lambda=\dfrac{df_{\text{opt}}}{dk}$** — the **shadow price**: how much the optimal value improves per unit of relaxed constraint. **It is an answer, not bookkeeping.**
- **Lagrange returns candidates only.** Compare $f$ at each, check that an extremum exists (EVT needs closed *and* bounded), and require $\nabla g\ne\mathbf 0$. **Never divide by a variable without splitting into cases** — that is how half the solutions get lost.
- **Least squares by calculus and by the normal equations are the same computation**: $\nabla S=\mathbf 0$ *is* $M^{\mathsf T}M\mathbf z=M^{\mathsf T}\mathbf y$, and **the Hessian $2M^{\mathsf T}M$ is positive definite exactly when the columns are independent** — which is why the fit is unique.
- **Constrained extremes of a quadratic form on the unit sphere are its eigenvalues** — the same theorem that underlies PCA.

---

## ⚠️ Important Notes

> [!warning] $D<0$ means a saddle, and there is no one-variable version of this
> **The second-derivative test in several variables has a case the single-variable test does not**, and it is the most common one in practice.
>
> **Do not import single-variable intuition:** "$f_{xx}>0$ so it is a minimum" is **wrong** — $x^2-y^2$ has $f_{xx}=2>0$ at a saddle. **Both conditions ($D>0$ *and* the sign of $f_{xx}$) are needed, in that order.**

> [!warning] $D=0$ decides nothing
> $x^4+y^4$ (minimum), $-x^4-y^4$ (maximum) and $x^3-3xy^2$ (a monkey saddle) **all have $D=0$ at the origin.**
>
> **The test sees only second derivatives**, so when those vanish in some direction the higher-order terms decide and the test is blind. **Fall back on direct inspection or on examining $f$ along well-chosen curves.**

> [!warning] The boundary is a separate problem, and usually the important one
> **On a closed region, interior critical points are only half the method.** A constrained optimum sits on the boundary, where $\nabla f\ne\mathbf 0$ — **so an algorithm that stops when the gradient vanishes will never find it.**
>
> **This is why constrained problems need their own machinery** (Lagrange, and KKT conditions for inequalities), and **why LASSO's $L^1$ constraint produces exact zeros**: the optimum lands on a corner of the constraint region, where the objective's gradient is decidedly non-zero.

> [!warning] Do not divide by a variable when solving the Lagrange equations
> $$2x=2\lambda x\quad\text{gives}\quad x=0\ \textbf{ or }\ \lambda=1$$
> **Dividing by $x$ keeps only the second branch and silently discards every solution with $x=0$.** In Exercise 3(iii) that would have lost the maximum entirely.
>
> **Factor, then case-split.** The same discipline as [[03 - Applications of Differentiation|ch. 03's]] parameter-dependent pivots.

> [!warning] Lagrange gives candidates; existence and classification are separate questions
> | Failure | Example |
> |---|---|
> | A candidate that is **neither** max nor min | $x^3$ on $x+y=0$ |
> | **No solution** because no extremum exists | maximise $x$ on $y=0$ |
> | $\nabla g=\mathbf 0$ so the argument collapses | a constraint with a cusp |
>
> **Always: check the constraint set is closed and bounded (then the EVT applies), then compare $f$ at every candidate.** The equations are a necessary condition and nothing more.

> [!warning] Report $\lambda$ — it is often the answer
> **$\lambda=\frac{df_{\text{opt}}}{dk}$ is the marginal value of the constraint.** Discarding it throws away the economically interesting half of the solution: whether the constraint is worth relaxing, and by how much.
>
> **A binding constraint has $\lambda\ne0$; a slack one has $\lambda=0$** — which is the complementary-slackness condition of KKT, met here in its simplest form.

> [!note] Cross-subject connections
> - [[03 - Applications of Differentiation|Ch. 03]] — this is that chapter in several variables: **Fermat becomes $\nabla f=\mathbf 0$, the second-derivative test becomes the Hessian, and $x^3$'s inflection becomes the saddle.**
> - [[07 - Partial Derivatives and the Gradient|Ch. 07]] — **$\nabla f\perp$ level set is the entire proof of the Lagrange condition**; Clairaut is why the Hessian is symmetric.
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — **the second-order Taylor expansion is why definiteness classifies critical points.**
> - [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]] — **positive definiteness, the spectral theorem, and $\max_{\|\mathbf x\|=1}\mathbf x^{\mathsf T}A\mathbf x=\lambda_{\max}$** — which is Exercise 3(iii) and the theorem behind PCA.
> - [[Linear Algebra/contents/05 - The Vector Space Rn|Linear Algebra ch. 05]] — **least squares from both directions**: $\nabla S=\mathbf 0$ and the normal equations are the same system.
> - [[Optimization/contents/00-Index|Optimization]] — **this chapter is its foundation.** KKT generalises Lagrange to inequalities, duality generalises $\lambda$, and the condition number governs every first-order method's rate.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **training is this chapter at scale**; saddle points and plateaus rather than local minima are the real obstacle; **regularisation is a constrained problem whose $\lambda$ is the penalty weight.**
> - [[Mathematical Statistics/contents/05 - Point Estimation|Math Stats ch. 05]] — **maximum likelihood with several parameters is $\nabla\ln L=\mathbf 0$ plus a Hessian check**, and the negative Hessian is the observed information matrix.
> - [[Microeconomics/contents/00-Index|Microeconomics]] — **utility maximisation subject to a budget is the archetypal Lagrange problem**, and $\lambda$ is the marginal utility of income.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **The specific casualty here is the discriminant $D=f_{xx}f_{yy}-(f_{xy})^2$**, whose subscripts detach so that $f_{xx}$, $f_{xy}$ and $f_{yy}$ become indistinguishable runs of letters — **and since the isolated ` 2 ` is a minus sign, the squared term and the subtraction are not reliably separable.** **The formula was reconstructed from the worked examples and verified by recomputing every classification.**
>
> **Figures lost, and in this chapter the losses are severe:**
> - **The saddle-surface picture** (§14.7) — the image of a horse's saddle or a mountain pass **is the definition** for most readers, and no verbal description substitutes for it.
> - **The contour maps showing $f$'s level curves tangent to the constraint curve** (§14.8). **This diagram is the entire proof of the Lagrange condition**, and §5 above has to assert in words what one picture makes obvious.
> - **The 3-D plots of every worked example**, including the two-minima-with-a-saddle surface of $x^4+y^4-4xy+1$.
> - **§14.7's Discovery Project on quadratic approximations**, whose figures show the Taylor paraboloid fitting the surface at a critical point — the visual justification for the second-derivative test.
>
> **Verification performed:** every critical point, classification, eigenvalue and Lagrange solution in this chapter was computed symbolically with `sympy`. Confirmed: **all three real critical points of $x^4+y^4-4xy+1$ with their $D$ values ($-16$, $128$, $128$) and function values ($1$, $-1$, $-1$)**; $D=-4$ for $x^2-y^2$ at the origin; **all three Lagrange problems** — $x=y=5$ with $\lambda=5$ and $f=25$; $(1,2)$ with $\lambda=2$ and distance $\sqrt5$; and $(\pm1,0)$ with $\lambda=1$, $(0,\pm1)$ with $\lambda=2$ on the unit circle; **the cube $a=b=c=\sqrt2$ for the surface-area-12 box**; and **the least-squares fit $m=\tfrac32$, $b=-\tfrac13$ computed both by $\nabla S=\mathbf 0$ and by the normal equations**, which agree exactly. **No error was found in the text's mathematics.**
>
> **Scope note:** **this is the shortest chapter in these notes because Stewart devotes only 21 pages to it** — §§14.7–14.8 — **which is a serious under-weighting for a data-science reader.** For comparison, he spends 34 pages on trigonometric integrals and substitution (ch. 7) and 19 on curve sketching (§§4.5–4.6), neither of which is used again in this vault. **I have therefore expanded the treatment well beyond Stewart's**: the Hessian in $n$ variables, the eigenvalue reading of the discriminant, the condition number, the prevalence of saddles in high dimensions, the interpretation of $\lambda$ as a shadow price, and the identity of the calculus and linear-algebra derivations of least squares are **all additions**, drawn from the connections to [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]] and [[Optimization/contents/00-Index|Optimization]] rather than from Stewart. **Stewart's §14.8 treatment of two constraints is stated but not developed**, since one constraint covers everything downstream until KKT.

#calculus #optimization #critical-points #hessian #saddle-point #second-derivative-test #lagrange-multipliers #shadow-price
