---
subject: Calculus
chapter: 07
tags: [ds, calculus, partial-derivatives, gradient, chain-rule, directional-derivative, tangent-plane, clairaut]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., §§14.1–14.6 (pp. 933–1007)"
---

# Partial Derivatives and the Gradient

> [!abstract] What this chapter is for
> **This is where calculus becomes usable for data science.** Every model has more than one parameter, so every derivative that matters is a partial derivative and every optimisation is over $\mathbb{R}^n$.
>
> **One object carries the chapter:**
>
> $$\boxed{\ \nabla f=\left(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\right)\ }$$
>
> **The gradient answers three questions at once:**
>
> | Question | Answer |
> |---|---|
> | How fast does $f$ change in direction $\mathbf u$? | $D_{\mathbf u}f=\nabla f\cdot\mathbf u$ |
> | Which direction increases $f$ fastest? | **$\nabla f$ itself**, at rate $\|\nabla f\|$ |
> | What is perpendicular to the level set? | **$\nabla f$** |
>
> **The first is why gradient descent works, the second is why it is called that, and the third is why Lagrange multipliers work** ([[08 - Multivariable Optimization|ch. 08]]).
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Functions of several variables | **Level curves** — the only way to see a surface on paper |
> | **2** | Limits | Must agree along **every** path — much stronger than in 1D |
> | **3** | Partial derivatives | Differentiate in one variable, **hold the others fixed**; Clairaut |
> | **4** | Tangent planes | $f(\mathbf a+\mathbf h)\approx f(\mathbf a)+\nabla f\cdot\mathbf h$ — **[[02 - Derivatives\|ch. 02's]] reading, generalised** |
> | **5** | **The chain rule** | A sum over paths — and this is backpropagation properly stated |
> | **6** | **The gradient** | Steepest ascent, and normal to level sets |

---

## 📘 Main Knowledge

### 1. Functions of several variables

$f:D\subseteq\mathbb{R}^2\to\mathbb{R}$ assigns a number $f(x,y)$ to each point of its domain. Its **graph** is the surface $z=f(x,y)$ in $\mathbb{R}^3$.

> [!important] Level curves are how you actually see a function of two variables
> The **level curves** (contours) are the sets $f(x,y)=k$ for constants $k$. **A contour map is the graph projected onto the plane** — exactly like a topographic map.
>
> | Reading | Meaning |
> |---|---|
> | contours **close together** | the surface is **steep** |
> | contours **far apart** | the surface is **flat** |
> | closed nested contours | a peak or a pit |
> | contours crossing themselves | a saddle |
>
> **For $n\ge3$ variables the graph lives in $\mathbb{R}^{n+1}$ and cannot be drawn at all**, while level sets remain meaningful. **Every intuition you build should be about level sets, not graphs** — that is the one that survives.

---

### 2. Limits and continuity in several variables

$$\lim_{(x,y)\to(a,b)}f(x,y)=L$$ means $f$ can be made arbitrarily close to $L$ by taking $(x,y)$ **sufficiently close to $(a,b)$ from any direction whatsoever.**

> [!warning] The limit must agree along **every** path — and this is genuinely harder than in 1D
> **In one variable there are two approaches (left and right).** In two variables there are infinitely many — every curve through the point.
>
> **The standard counterexample:**
> $$f(x,y)=\frac{xy}{x^2+y^2}$$
> - along $y=0$: $f=0\to0$
> - along $y=x$: $f=\frac{x^2}{2x^2}=\tfrac12\to\tfrac12$
>
> *(Both verified.)* **Two paths, two limits, so $\lim_{(x,y)\to(0,0)}f$ does not exist** — even though every straight line through the origin gives a constant, and every single-variable section looks perfectly well behaved.
>
> **Consequences worth stating:**
> - **To *disprove* a limit, exhibit two paths.** This is easy and is the usual task.
> - **To *prove* one, two paths are never enough** — you need the squeeze theorem, polar coordinates, or an $\varepsilon$–$\delta$ argument.
> - **Even agreement along every *straight line* is insufficient** — there are functions that are constant on every line through the origin and still have no limit, failing along a parabola.

**Continuity, sums, products, quotients and compositions all behave as in [[01 - Functions, Limits and Continuity|ch. 01]]**, and polynomials and rational functions are continuous on their domains.

---

### 3. Partial derivatives

> [!important] Definition
> $$f_x(a,b)=\lim_{h\to0}\frac{f(a+h,b)-f(a,b)}{h},\qquad f_y(a,b)=\lim_{h\to0}\frac{f(a,b+h)-f(a,b)}{h}$$
> **— an ordinary derivative in one variable, with the others held constant.**
>
> **Notation:** $f_x=\dfrac{\partial f}{\partial x}=\partial_xf$. **The curly $\partial$ signals that other variables exist and are being frozen.**

> [!tip] Computing them requires no new technique at all
> **Treat every other variable as a constant and differentiate as usual.** For $f=x^2y+\sin(xy)$:
> $$f_x=2xy+y\cos(xy),\qquad f_y=x^2+x\cos(xy)$$
> *(Verified.)* **In $f_x$, the $y$ in $y\cos(xy)$ came from the chain rule — the inner function $xy$ has $x$-derivative $y$.**

**Higher partials:** $f_{xx}$, $f_{xy}=(f_x)_y$, $f_{yx}=(f_y)_x$, $f_{yy}$.

> [!important] Clairaut's Theorem
> **If $f_{xy}$ and $f_{yx}$ are both continuous near $(a,b)$, then**
> $$\boxed{\ f_{xy}(a,b)=f_{yx}(a,b)\ }$$
> **— mixed partials commute.**

> [!warning] Clairaut needs continuity, and without it the conclusion fails
> **The standard counterexample:**
> $$f(x,y)=\frac{xy(x^2-y^2)}{x^2+y^2}\ \ (f(0,0)=0)\quad\Longrightarrow\quad f_{xy}(0,0)=-1,\qquad f_{yx}(0,0)=1$$
>
> **So the order of differentiation genuinely matters when the hypothesis fails.**
>
> **In practice it almost always holds** — and its consequence is that the **Hessian is symmetric** ([[08 - Multivariable Optimization|ch. 08]]), which by [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]] makes it orthogonally diagonalizable with real eigenvalues. **Every second-order optimisation method depends on that.**

---

### 4. Tangent planes and linear approximation

> [!important] The tangent plane and the linearization
> At $(a,b)$, the tangent plane to $z=f(x,y)$ is
> $$z=f(a,b)+f_x(a,b)(x-a)+f_y(a,b)(y-b)$$
> and in vector form, for $f:\mathbb{R}^n\to\mathbb{R}$,
> $$\boxed{\ f(\mathbf a+\mathbf h)\approx f(\mathbf a)+\nabla f(\mathbf a)\cdot\mathbf h\ }$$

> [!tip] This is exactly [[02 - Derivatives|ch. 02's]] reading, and it is why that reading was worth learning
> **"Slope of the tangent line" has no meaning here — there are infinitely many tangent lines.** But *"best linear approximation"* generalises without change: one number becomes one vector, and multiplication becomes a dot product.
>
> **Everything downstream is this formula.** Gradient descent steps along it; Newton's method adds the next term; the delta method applies it to a random vector; a neural network layer *is* it.

> [!warning] Partial derivatives existing is **not** differentiability
> **In one variable, "the derivative exists" is the whole story. In several, it is not.**
>
> $$f(x,y)=\frac{xy}{x^2+y^2}\ \ (f(0,0)=0)$$
> **has $f_x(0,0)=f_y(0,0)=0$ — both partials exist — and is not even continuous at the origin** (§2).
>
> **Existence of partials says only that $f$ behaves well along two particular lines.** True differentiability requires the linear approximation to be good **in every direction at once**, and the usable sufficient condition is:
>
> > **If $f_x$ and $f_y$ exist and are *continuous* near $(a,b)$, then $f$ is differentiable there.**
>
> **This is why "$C^1$" appears in so many hypotheses** — and it is the multivariable echo of [[02 - Derivatives|ch. 02's]] differentiable-but-not-$C^1$ example.

---

### 5. The chain rule

> [!important] The two main cases
> **One independent variable** ($x=x(t)$, $y=y(t)$):
> $$\frac{dz}{dt}=\frac{\partial z}{\partial x}\frac{dx}{dt}+\frac{\partial z}{\partial y}\frac{dy}{dt}$$
> **Several** ($x=x(s,t)$, $y=y(s,t)$):
> $$\frac{\partial z}{\partial t}=\frac{\partial z}{\partial x}\frac{\partial x}{\partial t}+\frac{\partial z}{\partial y}\frac{\partial y}{\partial t}$$
> **In general: one term per intermediate variable, and multiply along each path.**

> [!tip] Draw the tree, then sum over paths
> **Write $z$ at the top, the intermediate variables below it, the independent ones below those.** Then:
> - **multiply** the derivatives along each path from top to bottom;
> - **add** over all paths.
>
> **In vector form it is a dot product:**
> $$\frac{dz}{dt}=\nabla f\cdot\frac{d\mathbf r}{dt}$$
> **and for $f:\mathbb{R}^n\to\mathbb{R}^m$ it is a matrix product of Jacobians** — which is the form that scales.

> [!important] This is backpropagation, properly stated
> **[[02 - Derivatives|Ch. 02]] gave the single-path chain rule.** With several intermediate variables, **each layer contributes a *sum over paths*, and that sum is a matrix–vector product.**
>
> **A network with layers $\mathbf h_1,\mathbf h_2,\dots$ has**
> $$\frac{\partial L}{\partial \mathbf h_1}=J_2^{\mathsf T}J_3^{\mathsf T}\cdots\nabla L$$
> **— a product of Jacobians.** **Multiplying right-to-left keeps every operation a matrix–vector product; left-to-right would require matrix–matrix products.** *That* is the whole algorithmic content of the backward pass, and it is a statement about associativity of matrix multiplication ([[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02]]).

**Implicit differentiation** falls out: if $F(x,y)=0$ defines $y$ implicitly, then

$$\frac{dy}{dx}=-\frac{F_x}{F_y}$$

---

### 6. Directional derivatives and the gradient

> [!important] Definition and the key formula
> For a **unit** vector $\mathbf u$,
> $$D_{\mathbf u}f(\mathbf a)=\lim_{h\to0}\frac{f(\mathbf a+h\mathbf u)-f(\mathbf a)}h=\boxed{\ \nabla f(\mathbf a)\cdot\mathbf u\ }$$
> — **the rate of change of $f$ in the direction $\mathbf u$.**
>
> **The partials are the special cases $\mathbf u=\mathbf e_i$.**

> [!important] The three consequences — all from one dot product
> Since $\nabla f\cdot\mathbf u=\|\nabla f\|\cos\theta$ for a unit $\mathbf u$ ([[Linear Algebra/contents/04 - Vector Geometry|Linear Algebra ch. 04]]):
>
> | $\theta$ | $D_{\mathbf u}f$ | Meaning |
> |---|---|---|
> | $0$ | $+\|\nabla f\|$ | **$\nabla f$ is the direction of steepest ascent** |
> | $\pi$ | $-\|\nabla f\|$ | $-\nabla f$ is steepest **descent** |
> | $\pi/2$ | $0$ | **$\nabla f$ is perpendicular to the level set** |

> [!tip] Each consequence powers something downstream
> - **Steepest ascent $\Rightarrow$ gradient descent.** The update $\mathbf x\leftarrow\mathbf x-\eta\nabla f$ is "move in the direction that decreases $f$ fastest", and that is a *theorem*, not a heuristic.
> - **$\nabla f\perp$ level set $\Rightarrow$ Lagrange multipliers.** At a constrained optimum the level sets of $f$ and $g$ are tangent, so their normals are parallel: $\nabla f=\lambda\nabla g$ ([[08 - Multivariable Optimization|ch. 08]]).
> - **$\nabla f=\mathbf 0$ $\Rightarrow$ critical point.** No direction increases $f$ to first order.
>
> **And "steepest" is only true *locally* and *for the given scaling*.** Rescaling one variable changes which direction the gradient points — **which is exactly why feature scaling matters so much in gradient-based training**, and why second-order methods that correct for curvature converge so much faster.

> [!example] A worked gradient *(all verified)*
> $f(x,y)=x^2y-y^3$ at $(2,1)$:
> $$\nabla f=(2xy,\ x^2-3y^2)\ \Longrightarrow\ \nabla f(2,1)=(4,1)$$
> - **Steepest ascent** is along $(4,1)$, at rate $\|\nabla f\|=\sqrt{17}\approx4.123$.
> - **In the direction $\mathbf u=\left(\tfrac35,\tfrac45\right)$:**
> $$D_{\mathbf u}f=(4,1)\cdot\left(\tfrac35,\tfrac45\right)=\tfrac{12}5+\tfrac45=\tfrac{16}5=3.2$$
> - **Along $(1,-4)/\sqrt{17}$** (perpendicular to $\nabla f$) the rate is 0 — **that is the tangent to the level curve through $(2,1)$.**

---

## ✏️ Exercises

> [!question] Exercise 1 — partial derivatives *(warm-up)*
> (i) For $f(x,y)=x^2y+\sin(xy)$, find $f_x$ and $f_y$.
> (ii) Verify Clairaut's theorem for this $f$.
> (iii) For $g(x,y,z)=xe^{yz}$, find all three first partials.
> (iv) For the Cobb–Douglas function $P=1.01L^{0.75}K^{0.25}$, show that $L\frac{\partial P}{\partial L}+K\frac{\partial P}{\partial K}=P$.

> [!example]- Solution
> **(i)** Holding $y$ fixed, then $x$ fixed:
> $$f_x=\boxed{2xy+y\cos(xy)},\qquad f_y=\boxed{x^2+x\cos(xy)}$$
> *(Verified.)* **The trailing $y$ and $x$ come from the chain rule on $\sin(xy)$.**
>
> **(ii)** $$f_{xy}=\frac{\partial}{\partial y}\big(2xy+y\cos(xy)\big)=2x+\cos(xy)-xy\sin(xy)$$
> $$f_{yx}=\frac{\partial}{\partial x}\big(x^2+x\cos(xy)\big)=2x+\cos(xy)-xy\sin(xy)$$
> **Equal** ✓ *(verified symbolically)*. **Both are continuous everywhere, so Clairaut applies and this was guaranteed** — the computation is a check on arithmetic, not on the theorem.
>
> **(iii)** $$g_x=e^{yz},\qquad g_y=xze^{yz},\qquad g_z=xye^{yz}$$
>
> **(iv)** $$\frac{\partial P}{\partial L}=0.75\cdot1.01L^{-0.25}K^{0.25},\qquad \frac{\partial P}{\partial K}=0.25\cdot1.01L^{0.75}K^{-0.75}$$
> $$L\frac{\partial P}{\partial L}+K\frac{\partial P}{\partial K}=(0.75+0.25)\cdot1.01L^{0.75}K^{0.25}=P\ ✓$$
> *(Verified symbolically.)*
>
> > [!important] This is Euler's theorem, and it is why the exponents sum to 1
> > **A function with $f(t\mathbf x)=t^kf(\mathbf x)$ is *homogeneous of degree $k$*, and satisfies $\mathbf x\cdot\nabla f=kf$.** Cobb–Douglas with exponents summing to 1 is homogeneous of degree 1 — **constant returns to scale: double both inputs and output doubles.**
> >
> > **The economic reading of the identity: total output is exactly exhausted by paying each factor its marginal product.** $\frac{\partial P}{\partial L}$ is the marginal product of labour, so $L\frac{\partial P}{\partial L}$ is the total wage bill — **and the two factor payments sum to $P$ with nothing left over** ([[Microeconomics/contents/00-Index|Microeconomics]]).

> [!question] Exercise 2 — limits in several variables
> (i) Show $\displaystyle\lim_{(x,y)\to(0,0)}\frac{xy}{x^2+y^2}$ does not exist.
> (ii) For the same $f$ (with $f(0,0)=0$), show $f_x(0,0)$ and $f_y(0,0)$ both exist.
> (iii) Explain why (i) and (ii) together are not a contradiction, and what they show.
> (iv) Show $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^2y}{x^2+y^2}=0$.

> [!example]- Solution
> **(i)** Two paths:
> $$\text{along }y=0:\ f=\frac{0}{x^2}=0\to0;\qquad \text{along }y=x:\ f=\frac{x^2}{2x^2}=\tfrac12\to\tfrac12$$
> *(Both verified.)* **Different limits along different paths, so no limit exists.**
>
> **(ii)** Along the axes $f$ is identically 0:
> $$f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}h=\lim_{h\to0}\frac{0-0}h=0$$
> and $f_y(0,0)=0$ likewise. **Both partials exist and are zero.**
>
> **(iii)** **No contradiction — the two statements are about different things.**
>
> **A partial derivative examines $f$ along one line only.** Here $f$ is identically zero along both axes, so both partials are 0 and see nothing. **The limit examines every direction at once, and along $y=x$ the function is constantly $\tfrac12$.**
>
> **What this shows: in several variables, "the partials exist" is much weaker than "the function is differentiable" — it does not even imply continuity.** In one variable differentiability implies continuity; **here it fails at the first step.**
>
> **The usable repair is $C^1$: if the partials exist and are *continuous*, $f$ is differentiable.**
>
> **(iv)** Squeeze. Since $x^2\le x^2+y^2$,
> $$\left|\frac{x^2y}{x^2+y^2}\right|=|y|\cdot\frac{x^2}{x^2+y^2}\le|y|\longrightarrow0$$
> **so the limit is $\boxed0$** by the Squeeze Theorem.
>
> **Note the asymmetry with (i): the extra factor of $x$ in the numerator is what makes it work** — it supplies a factor that vanishes regardless of direction. **Two paths can disprove a limit; only a bound like this can prove one.**

> [!question] Exercise 3 — the chain rule
> (i) $z=x^2+y^2$ with $x=\cos t$, $y=\sin t$. Find $\frac{dz}{dt}$ two ways.
> (ii) $w=xy+yz$ with $x=s+t$, $y=st$, $z=s-t$. Find $\frac{\partial w}{\partial s}$.
> (iii) $F(x,y)=x^3+y^3-6xy=0$ defines $y$ implicitly. Find $\frac{dy}{dx}$ and check against [[02 - Derivatives|ch. 02]].
> (iv) Explain how the chain rule's "sum over paths" becomes a product of matrices.

> [!example]- Solution
> **(i) By the chain rule:**
> $$\frac{dz}{dt}=2x\frac{dx}{dt}+2y\frac{dy}{dt}=2\cos t(-\sin t)+2\sin t(\cos t)=\boxed0$$
> **By substituting first:** $z=\cos^2t+\sin^2t=1$, so $\frac{dz}{dt}=0$ ✓ *(verified)*.
>
> **The answer is obvious in hindsight — the path is the unit circle, on which $x^2+y^2$ is constant.** **Geometrically the velocity is tangent to the level curve, so $\nabla z\cdot\mathbf r'=0$** — which is §6's third consequence appearing already.
>
> **(ii)** Two intermediate variables depend on $s$ (all three do):
> $$\frac{\partial w}{\partial s}=w_x\frac{\partial x}{\partial s}+w_y\frac{\partial y}{\partial s}+w_z\frac{\partial z}{\partial s}=y(1)+(x+z)(t)+y(1)$$
> With $x+z=2s$ and $y=st$:
> $$=st+2st+st=\boxed{4st}$$
> *(Check by substitution: $w=(s+t)st+st(s-t)=s^2t+st^2+s^2t-st^2=2s^2t$, so $\frac{\partial w}{\partial s}=4st$ ✓.)*
>
> **Three paths from $w$ down to $s$, three terms.** **Missing a path is the standard error**, and drawing the tree prevents it.
>
> **(iii)** $$\frac{dy}{dx}=-\frac{F_x}{F_y}=-\frac{3x^2-6y}{3y^2-6x}=\frac{2y-x^2}{y^2-2x}$$
> **which is exactly the folium result of [[02 - Derivatives|ch. 02]], Exercise 3(ii)** ✓ — and at $(3,3)$ it gives $\frac{6-9}{9-6}=-1$ ✓.
>
> **The implicit-differentiation trick of ch. 02 is a special case of the multivariable chain rule**, and this derivation explains *why* it worked.
>
> **(iv)** **Stack the partials into a Jacobian matrix.** For $\mathbf z=\mathbf f(\mathbf y)$ and $\mathbf y=\mathbf g(\mathbf x)$,
> $$\frac{\partial z_i}{\partial x_k}=\sum_j\frac{\partial z_i}{\partial y_j}\frac{\partial y_j}{\partial x_k}$$
> **is precisely the $(i,k)$ entry of the matrix product $J_{\mathbf f}J_{\mathbf g}$** — the sum over $j$ *is* the sum over paths.
>
> **So the chain rule reads $J_{\mathbf f\circ\mathbf g}=J_{\mathbf f}\,J_{\mathbf g}$**, exactly matching [[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02's]] "matrix multiplication is composition".
>
> > [!important] And this is why backpropagation goes backwards
> > **For a deep composition the gradient is $J_1^{\mathsf T}J_2^{\mathsf T}\cdots J_L^{\mathsf T}\nabla L$.** Matrix multiplication is associative, so you may bracket it either way:
> > - **right-to-left:** every step is a matrix–**vector** product — $O(\text{layers}\times n^2)$;
> > - **left-to-right:** every step is a matrix–**matrix** product — $O(\text{layers}\times n^3)$.
> >
> > **The backward pass is the right-to-left bracketing.** It is not a special algorithm — **it is a choice of association order in a product the chain rule already gave you.**

> [!question] Exercise 4 — the gradient
> Let $f(x,y)=x^2y-y^3$ and $P=(2,1)$.
> (i) Find $\nabla f(P)$.
> (ii) Find $D_{\mathbf u}f(P)$ for $\mathbf u=\left(\tfrac35,\tfrac45\right)$.
> (iii) In which direction does $f$ increase fastest at $P$, and how fast?
> (iv) Find a direction in which $f$ does not change at $P$, and say what it is tangent to.
> (v) Why must $\mathbf u$ be a **unit** vector in (ii)?

> [!example]- Solution
> **(i)** $\nabla f=(2xy,\ x^2-3y^2)$, so $\nabla f(2,1)=\boxed{(4,1)}$ *(verified)*.
>
> **(ii)** $\mathbf u$ is a unit vector ($\tfrac9{25}+\tfrac{16}{25}=1$ ✓), so
> $$D_{\mathbf u}f=(4,1)\cdot\left(\tfrac35,\tfrac45\right)=\tfrac{12}5+\tfrac45=\boxed{\tfrac{16}5=3.2}$$
> *(Verified.)*
>
> **(iii)** **Fastest increase is along $\nabla f=(4,1)$**, i.e. the unit vector $\frac1{\sqrt{17}}(4,1)$, at rate
> $$\|\nabla f\|=\sqrt{16+1}=\boxed{\sqrt{17}\approx4.123}$$
> *(Verified.)* **Note this exceeds the $3.2$ of part (ii)** — as it must, since $\|\nabla f\|$ is the maximum over all directions.
>
> **(iv)** Any direction perpendicular to $\nabla f$: $\ \mathbf v=\frac1{\sqrt{17}}(1,-4)$, since $(4,1)\cdot(1,-4)=0$.
>
> **This is tangent to the level curve of $f$ through $(2,1)$** — the curve $x^2y-y^3=3$. **Moving along a contour does not change altitude, which is the whole content of "$\nabla f\perp$ level set".**
>
> **(v)** **Because $D_{\mathbf u}f=\nabla f\cdot\mathbf u$ measures rate *per unit distance travelled*.** Using $\mathbf w=2\mathbf u$ would give twice the value — not because $f$ changes faster, but because you moved twice as far.
>
> **Normalising is what makes directional derivatives comparable across directions**, exactly as normalising is what makes cosine similarity comparable across vectors ([[Linear Algebra/contents/04 - Vector Geometry|Linear Algebra ch. 04]]).

> [!question] Exercise 5 — linear approximation and level sets *(hard)*
> (a) Let $f(x,y)=x^2+y^2$.
> (i) Find the tangent plane at $(1,2)$.
> (ii) Use it to estimate $f(1.05,1.98)$, and compare with the true value.
> (iii) Verify that $\nabla f(1,2)$ is perpendicular to the level curve through that point.
>
> (b) Show that if $f$ is differentiable, $\nabla f(\mathbf a)$ is perpendicular to the level set of $f$ through $\mathbf a$.
>
> (c) A function has $\nabla f=(3,-4)$ at a point.
> (i) What is the largest possible directional derivative there?
> (ii) In how many directions is $D_{\mathbf u}f=0$?
> (iii) In how many is $D_{\mathbf u}f=3$?

> [!example]- Solution
> **(a)(i)** $f(1,2)=5$, $f_x=2x$ so $f_x(1,2)=2$, $f_y=2y$ so $f_y(1,2)=4$:
> $$\boxed{z=5+2(x-1)+4(y-2)}$$
> *(Verified.)*
>
> **(ii)** With $h=0.05$, $k=-0.02$:
> $$f(1.05,1.98)\approx5+2(0.05)+4(-0.02)=5+0.1-0.08=5.02$$
> **True value:** $1.05^2+1.98^2=1.1025+3.9204=5.0229$.
> $$\text{error}=2.9\times10^{-3}$$
>
> **The error is $h^2+k^2=0.0025+0.0004=0.0029$ exactly** — because $f$ is a quadratic, so the second-order Taylor term *is* the whole error. **The $O(\|\mathbf h\|^2)$ law of [[02 - Derivatives|ch. 02]] appears here in its cleanest possible instance.**
>
> **(iii)** The level curve through $(1,2)$ is $x^2+y^2=5$, a circle. **Its tangent at $(1,2)$ is perpendicular to the radius**, and the radius vector is $(1,2)$. Since $\nabla f(1,2)=(2,4)=2(1,2)$ is parallel to the radius, **it is perpendicular to the tangent** ✓
>
> **(b)** Let $\mathbf r(t)$ be any curve lying in the level set $f=k$ with $\mathbf r(0)=\mathbf a$. Then $f(\mathbf r(t))=k$ for all $t$, so differentiating by the chain rule:
> $$0=\frac{d}{dt}f(\mathbf r(t))=\nabla f(\mathbf r(t))\cdot\mathbf r'(t)$$
> At $t=0$: $\ \nabla f(\mathbf a)\cdot\mathbf r'(0)=0$.
>
> **Since $\mathbf r$ was an arbitrary curve in the level set, $\nabla f(\mathbf a)$ is orthogonal to every tangent vector** — i.e. to the whole tangent plane of the level set. $\blacksquare$
>
> **The proof is three lines and uses only the chain rule**, which is a good sign that the fact is structural rather than accidental.
>
> **(c)(i)** $\|\nabla f\|=\sqrt{9+16}=\boxed5$, attained along $\frac15(3,-4)$.
>
> **(ii)** $D_{\mathbf u}f=0$ requires $\mathbf u\perp\nabla f$. In $\mathbb{R}^2$ there are exactly **two** unit vectors perpendicular to a given one: $\pm\frac15(4,3)$. $\boxed{2}$
>
> *(In $\mathbb{R}^3$ there would be a whole circle of them, and in $\mathbb{R}^n$ a sphere of dimension $n-2$ — the level set's tangent space.)*
>
> **(iii)** $D_{\mathbf u}f=5\cos\theta=3$ gives $\cos\theta=\tfrac35$, so $\theta=\pm53.13°$ — **two** directions, symmetric about $\nabla f$. $\boxed{2}$
>
> > [!important] The picture to keep
> > **As $\mathbf u$ sweeps once around the unit circle, $D_{\mathbf u}f=\|\nabla f\|\cos\theta$ traces a cosine wave from $+\|\nabla f\|$ to $-\|\nabla f\|$.**
> >
> > | Value | Directions |
> > |---|---|
> > | $+\|\nabla f\|$ | 1 (steepest ascent) |
> > | $-\|\nabla f\|$ | 1 (steepest descent) |
> > | anything strictly between | **2** |
> > | $0$ | 2 (tangent to the level curve) |
> >
> > **Every question about rates of change in a direction is this one cosine.** It is also why gradient descent is "optimal" only in the narrow sense of steepest *immediate* decrease — **the direction that goes downhill fastest right now is usually not the direction pointing at the minimum**, which is the entire motivation for momentum and second-order methods ([[Optimization/contents/00-Index|Optimization]]).

---

## 📝 Summary

- **Level curves are how a function of several variables is actually visualised** — close contours mean steep. **For $n\ge3$ the graph cannot be drawn and level sets are all you have**, so build intuition on them.
- **A multivariable limit must agree along every path**, which is far stronger than the two-sided condition in 1D. **Two paths disprove a limit; nothing short of a squeeze or $\varepsilon$–$\delta$ proves one.**
- **Partial derivatives are ordinary derivatives with the other variables frozen** — no new technique.
- **Clairaut: $f_{xy}=f_{yx}$ when both are continuous** — and it genuinely fails without that hypothesis. **Its payoff is that the Hessian is symmetric**, hence orthogonally diagonalizable.
- **Existence of the partials does not imply differentiability, or even continuity** — $\frac{xy}{x^2+y^2}$ has both partials zero at the origin and no limit there. **The usable sufficient condition is $C^1$.**
- $$\boxed{f(\mathbf a+\mathbf h)\approx f(\mathbf a)+\nabla f(\mathbf a)\cdot\mathbf h}$$ **— [[02 - Derivatives|ch. 02's]] "best linear approximation" reading, unchanged except that one number became a vector.** The error is $O(\|\mathbf h\|^2)$.
- **The chain rule is a sum over paths: one term per intermediate variable.** In vector form $\frac{dz}{dt}=\nabla f\cdot\mathbf r'$, and in general **$J_{\mathbf f\circ\mathbf g}=J_{\mathbf f}J_{\mathbf g}$.** **Backpropagation is the right-to-left bracketing of that matrix product** — a choice of association order, not a special algorithm.
- **Implicit differentiation is the chain rule:** $\frac{dy}{dx}=-\frac{F_x}{F_y}$.
- $$\boxed{D_{\mathbf u}f=\nabla f\cdot\mathbf u=\|\nabla f\|\cos\theta}\quad(\mathbf u\text{ a \textbf{unit} vector})$$ **and everything follows:** $\nabla f$ is the direction of **steepest ascent** at rate $\|\nabla f\|$; $-\nabla f$ is steepest descent; **$\nabla f$ is perpendicular to the level set**; and $\nabla f=\mathbf 0$ marks a critical point.
- **Those three facts power gradient descent, Lagrange multipliers, and critical-point analysis respectively.**
- **"Steepest" depends on the scaling of the variables** — which is why feature scaling matters in gradient-based training, and why the steepest immediate direction rarely points at the minimum.
- **Euler's theorem: a degree-$k$ homogeneous function satisfies $\mathbf x\cdot\nabla f=kf$** — for Cobb–Douglas with exponents summing to 1, this is constant returns to scale and exact factor-payment exhaustion.

---

## ⚠️ Important Notes

> [!warning] Two paths is a disproof, never a proof
> **Finding two paths with different limits settles non-existence.** Finding a hundred paths with the *same* limit settles nothing — **there are functions with the same limit along every straight line and no limit at all** (they fail along a parabola).
>
> **To prove a multivariable limit exists you need a bound valid in every direction** — the squeeze theorem, polar coordinates ($r\to0$ uniformly in $\theta$), or $\varepsilon$–$\delta$.

> [!warning] Partials existing is much weaker than differentiability
> $$f(x,y)=\frac{xy}{x^2+y^2}\ (f(0,0)=0)$$
> **has $f_x(0,0)=f_y(0,0)=0$ and is not continuous at the origin.**
>
> **A partial derivative sees $f$ along one line only**, and two lines say nothing about the other infinitely many directions. **In one variable, differentiable $\Rightarrow$ continuous; here even that fails.**
>
> **The practical rule: check that the partials are *continuous* ($C^1$), which does imply differentiability.**

> [!warning] $\mathbf u$ must be a unit vector in $D_{\mathbf u}f=\nabla f\cdot\mathbf u$
> **Otherwise you are measuring rate per step rather than rate per unit distance**, and directions with longer vectors falsely appear steeper.
>
> **Normalise first, every time** — and note that the same discipline makes cosine similarity meaningful and makes "$\|\nabla f\|$ is the maximum rate" true.

> [!warning] Clairaut needs continuity of the mixed partials
> $$f=\frac{xy(x^2-y^2)}{x^2+y^2}\ \Longrightarrow\ f_{xy}(0,0)=-1\ne1=f_{yx}(0,0)$$
> **The order of differentiation is not automatically irrelevant.**
>
> **It almost always is in practice** — and when it is, the Hessian is symmetric, which is what lets [[Linear Algebra/contents/08 - Orthogonality|the spectral theorem]] classify critical points ([[08 - Multivariable Optimization|ch. 08]]). **A hypothesis that usually holds is still a hypothesis.**

> [!warning] Draw the tree before applying the chain rule
> **The commonest error is a missing term** — one path from the top variable to the bottom one that was not counted.
>
> **Procedure: write the dependency tree, multiply along each root-to-leaf path, sum over paths.** In Exercise 3(ii) all three intermediate variables depended on $s$, giving three terms; **noticing only two is the failure mode.**

> [!warning] "Steepest descent" is steepest *now*, and depends on your units
> **$-\nabla f$ is the best direction for an infinitesimal step and generally does not point at the minimum.** On an elongated valley, gradient descent zig-zags across it rather than running along it.
>
> **And rescaling a variable changes the gradient's direction.** Measuring one feature in metres rather than kilometres changes which way is "steepest" — **so unscaled features make gradient descent slow for reasons that have nothing to do with the model.**
>
> **The fixes all amount to correcting for curvature:** feature scaling, momentum, and Newton-type methods that use the Hessian ([[Optimization/contents/00-Index|Optimization]]).

> [!note] Cross-subject connections
> - [[02 - Derivatives|Ch. 02]] — **the linear-approximation reading generalises verbatim**; the single-path chain rule becomes a sum over paths, and its $h^2$ error law becomes $O(\|\mathbf h\|^2)$.
> - [[08 - Multivariable Optimization|Ch. 08]] — $\nabla f=\mathbf 0$ locates critical points, the **Hessian** classifies them, and **$\nabla f\perp$ level set is exactly why $\nabla f=\lambda\nabla g$.**
> - [[09 - Multiple Integrals and Change of Variables|Ch. 09]] — the Jacobian introduced here as a chain-rule matrix becomes the volume factor there.
> - [[Linear Algebra/contents/04 - Vector Geometry|Linear Algebra ch. 04]] — $D_{\mathbf u}f=\|\nabla f\|\cos\theta$ **is** the dot product's geometric formula; "perpendicular to the level set" is the normal vector of a plane.
> - [[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02]] — **$J_{\mathbf f\circ\mathbf g}=J_{\mathbf f}J_{\mathbf g}$ is "matrix multiplication is composition"**, and backpropagation's efficiency is associativity.
> - [[Linear Algebra/contents/08 - Orthogonality|Linear Algebra ch. 08]] — Clairaut makes the Hessian symmetric, hence orthogonally diagonalizable with real eigenvalues.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **gradient descent is §6, backpropagation is §5**, and feature scaling matters because "steepest" is scale-dependent.
> - [[Optimization/contents/00-Index|Optimization]] — this chapter supplies every first-order concept the subject uses.
> - [[Microeconomics/contents/00-Index|Microeconomics]] — marginal products are partials; **Euler's theorem on Cobb–Douglas is factor-payment exhaustion**; an indifference curve is a level set and the MRS is a ratio of partials.
> - [[Econometrics/contents/00-Index|Econometrics]] — a regression coefficient is a partial derivative, which is exactly what "holding the other variables constant" means.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **A new hazard appears in this chapter: `y` is both the fraction slash *and* a variable name.** In `−zyx` the reader must decide between $\partial z/\partial x$ and a product involving the variable $y$ — **and both readings occur on the same page.** Subscripts also detach, so $f_x$, $f_{xy}$ and $f_{yx}$ are frequently indistinguishable in the extraction. **Every partial derivative in these notes was recomputed symbolically rather than read off.**
>
> **Figures lost — and this is the chapter where that hurts most in the whole book.** Stewart's ch. 14 is built on pictures:
> - **Every contour map and every 3-D surface plot** (§14.1) — and **§1 above is entirely about reading contour maps**, which I have had to describe in a table rather than show.
> - **The tangent-plane pictures** (§14.4), including the zoom-in sequence showing a surface flattening into its tangent plane — **the visual argument for linear approximation in 2-D**, with no verbal substitute.
> - **The tree diagrams for the chain rule** (§14.5). **These are the method**, not an illustration of it, and §5's "draw the tree" instruction is a description of a picture the reader cannot see.
> - **The gradient-perpendicular-to-contours diagram** (§14.6), which makes the chapter's central geometric fact obvious in one glance.
>
> **Verification performed:** every partial derivative, limit, gradient and estimate in this chapter was computed symbolically with `sympy`. Confirmed: $f_x$, $f_y$ and **the equality of $f_{xy}$ and $f_{yx}$** for $x^2y+\sin(xy)$; **both path limits ($0$ and $\tfrac12$) for $\frac{xy}{x^2+y^2}$**; the chain-rule result $\frac{dz}{dt}=0$ on the unit circle, checked both ways; $\frac{\partial w}{\partial s}=4st$, checked by substitution; **$\nabla f(2,1)=(4,1)$, $D_{\mathbf u}f=\tfrac{16}5$ and $\|\nabla f\|=\sqrt{17}$**; the tangent plane $z=5+2(x-1)+4(y-2)$ **and its estimate $5.02$ against the true $5.0229$, with the error exactly $h^2+k^2$**; and **Euler's identity $L P_L+K P_K=P$ for Cobb–Douglas**. **No error was found in the text's mathematics.**
>
> **Scope note:** **§14.1's catalogue of quadric surfaces and §14.2's $\varepsilon$–$\delta$ definitions are compressed.** The surfaces are reference material whose value was in the figures, and the formal limit definition is used here only to state that two paths disprove and nothing short of a bound proves. **§14.4's treatment of differentials and error estimation is folded into §4 and Exercise 5(a)** rather than given separately, since it is [[02 - Derivatives|ch. 02's]] error propagation with a gradient in place of a derivative. **§14.5's implicit-differentiation subsection is compressed to the formula $\frac{dy}{dx}=-F_x/F_y$ and one exercise**, because it explains a technique [[02 - Derivatives|ch. 02]] already used.

#calculus #partial-derivatives #gradient #chain-rule #directional-derivative #tangent-plane #clairaut #level-curves
