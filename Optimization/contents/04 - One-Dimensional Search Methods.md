---
subject: Optimization
chapter: 04
tags: [ds, optimization, line-search, golden-section, fibonacci, bisection, newton-method, secant-method, armijo, wolfe-conditions]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 7; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, §8.1"
---

# One-Dimensional Search Methods

> [!abstract] What this chapter is for
> **Every multivariable algorithm in chapters 05–08 has this chapter inside its loop.** Each of them computes a search direction $\mathbf d_k$ and then asks *how far along it should I go?* — which is a one-dimensional minimisation of
> $$\phi_k(\alpha)=f(\mathbf x_k+\alpha\mathbf d_k)$$
>
> **The methods split by what information they use, and that is the only thing that distinguishes them:**
>
> | § | Method | Uses | Reduction per step | Convergence |
> |---|---|---|---|---|
> | **3** | **Golden section** | $f$ only | $0.618$ | linear |
> | **4** | **Fibonacci** | $f$ only | $F_N/F_{N+1}$ — **provably optimal** | linear |
> | **5** | **Bisection** | $f'$ only | $0.5$ | linear |
> | **6** | **Newton** | $f'$ and $f''$ | — | **quadratic** |
> | **7** | **Secant** | $f'$ only | — | **superlinear, $p=\varphi\approx1.618$** |
>
> **§9 is the section that matters most in practice**, and it inverts the whole chapter: **modern methods deliberately do *not* minimise $\phi_k$.** They stop as soon as the step is "good enough" by the **Armijo, Goldstein or Wolfe conditions**, because iterating the outer problem is a better use of the same arithmetic.

---

## 📘 Main Knowledge

### 1. Why one dimension deserves a chapter

Two reasons, and the second is the operative one:

1. **These are the simplest instances of every idea in the subject** — bracketing, interpolation, and the trade-off between derivative information and cost.
2. **They are subroutines.** [[01 - The Optimization Problem|Chapter 01's]] template $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k$ needs an $\alpha_k$ at every single iteration, and choosing it *is* a one-dimensional problem — one that will be solved thousands of times.

**The derivative of the line function comes from the chain rule** ([[Calculus/contents/07 - Partial Derivatives and the Gradient|Calculus ch. 07]]):

$$\boxed{\phi_k'(\alpha)=\mathbf d_k^{\mathsf T}\nabla f(\mathbf x_k+\alpha\mathbf d_k)}$$

**So a line search that uses $\phi'$ needs only the gradient of $f$, never its Hessian** — which is why the secant and Wolfe machinery of §§7 and 9 scale to large problems.

---

### 2. Unimodality and bracketing

> [!important] Unimodal
> $f$ is **unimodal** on $[a_0,b_0]$ if it has exactly one local minimizer there. Equivalently, it decreases to $x^*$ and increases afterwards.

**This is the only assumption the bracket-shrinking methods make** — no differentiability, no convexity, not even continuity in the strictest treatments. It is what makes the following comparison valid:

> **If $a<p<q<b$ and $f(p)<f(q)$, then $x^*\in[a,q]$. If $f(p)>f(q)$, then $x^*\in[p,b]$.**

**One comparison of two interior values discards part of the interval.** Note that **one interior point is not enough**: knowing $f(p)$ alone tells you nothing about which side $x^*$ lies on.

**Getting an initial bracket** (§7.7). It suffices to find $a<c<b$ with $f(c)<f(a)$ and $f(c)<f(b)$. Pick three points; if the middle is not lowest, step further in the downhill direction, **expanding the step each time** — typically by a factor $2-\rho\approx1.618$, chosen so the point already evaluated lands exactly where the golden-section method wants it.

---

### 3. Golden section search

**Aim: shrink the bracket using only *one* new function evaluation per step.**

Place two symmetric interior points at
$$p=a+\rho(b-a),\qquad q=a+(1-\rho)(b-a),\qquad \rho<\tfrac12$$

After comparing, one of the two survives inside the new interval. **For the survivor to land exactly where the next step wants a point**, take the unit interval and require $\rho(1-\rho)=1-2\rho$, i.e.

$$\rho^2-3\rho+1=0\quad\Longrightarrow\quad \rho=\frac{3-\sqrt5}{2}\approx0.381966$$

*(The other root exceeds $\tfrac12$ and is rejected.)*

> [!important] Why "golden"
> $$1-\rho=\frac{\sqrt5-1}{2}\approx0.618034\qquad\text{and}\qquad \frac{\rho}{1-\rho}=\frac{1-\rho}{1}$$
> **The shorter piece is to the longer as the longer is to the whole** — the golden section of the ancient Greek geometers. Equivalently $1-\rho=1/\varphi$ where $\varphi=\tfrac{1+\sqrt5}{2}$ is the golden ratio.

**After the first step, each iteration costs one new evaluation and multiplies the bracket width by $1-\rho\approx0.618$.** So $N$ steps give

$$\text{final width}=(0.618034)^N\times(b_0-a_0)$$

> [!example]- Worked example — verified line by line
> Minimise $f(x)=x^4-14x^3+60x^2-70x$ on $[0,2]$ to within $0.3$. Need $(0.61803)^N\le0.3/2=0.15$; since $0.618^3=0.236$ and $0.618^4=0.1459$, take $N=4$.
>
> | Iter | Bracket | $p$ | $f(p)$ | $q$ | $f(q)$ | New bracket |
> |---|---|---|---|---|---|---|
> | 1 | $[0,\ 2]$ | $0.7639$ | $-24.36$ | $1.2361$ | $-18.96$ | $[0,\ 1.2361]$ |
> | 2 | $[0,\ 1.2361]$ | $0.4721$ | $-21.10$ | $0.7639$ | $-24.36$ | $[0.4721,\ 1.2361]$ |
> | 3 | $[0.4721,\ 1.2361]$ | $0.7639$ | $-24.36$ | $0.9443$ | $-23.59$ | $[0.4721,\ 0.9443]$ |
> | 4 | $[0.4721,\ 0.9443]$ | $0.6525$ | $-23.84$ | $0.7639$ | $-24.36$ | $\boxed{[0.6525,\ 0.9443]}$ |
>
> Final width $0.2918<0.3$ ✔. **The true minimizer is $x^*=0.78088$**, comfortably inside. **Note that only the italicised value in each row is new** — the other was inherited from the previous iteration, which is the whole point of the $\rho$ derivation.

---

### 4. Fibonacci search — the optimal bracket method

**What if $\rho$ is allowed to change from step to step?** Write $\rho_k$ for the ratio at step $k$. The one-new-evaluation requirement becomes
$$\rho_{k+1}(1-\rho_k)=1-2\rho_k\quad\Longrightarrow\quad \rho_{k+1}=1-\frac{\rho_k}{1-\rho_k}$$

**Many sequences satisfy this** — the constant sequence $\rho_k=(3-\sqrt5)/2$ is golden section. **Which one shrinks the bracket most in $N$ steps?** That is itself a constrained optimization problem:

$$\text{minimize }\ \prod_{k=1}^N(1-\rho_k)\quad\text{subject to}\quad \rho_{k+1}=1-\frac{\rho_k}{1-\rho_k},\ \ 0\le\rho_k\le\tfrac12$$

> [!important] The answer is the Fibonacci sequence
> With $F_{-1}=0$, $F_0=1$, $F_{k+1}=F_k+F_{k-1}$:
> $$\rho_k=1-\frac{F_{N-k+1}}{F_{N-k+2}},\qquad k=1,\dots,N$$
> and the total reduction factor is
> $$\prod_{k=1}^N(1-\rho_k)=\frac{F_1}{F_{N+1}}=\frac{1}{F_{N+1}}$$
>
> | $F_1$ | $F_2$ | $F_3$ | $F_4$ | $F_5$ | $F_6$ | $F_7$ | $F_8$ |
> |---|---|---|---|---|---|---|---|
> | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 |

**Fibonacci beats golden section**, and it is provably the best any method of this kind can do: for $N=4$, $1/F_5=1/8=0.125$ against $0.618^4=0.1459$.

> [!warning] The last iteration degenerates, and the fix is a fudge
> $\rho_N=1-\dfrac{F_1}{F_2}=1-\dfrac12=\dfrac12$. **At $\rho=\tfrac12$ the two interior points coincide at the midpoint and no comparison is possible.**
>
> The remedy is to use $\rho_N=\tfrac12-\varepsilon$ for a small $\varepsilon>0$, placing the last point just off centre. The worst-case reduction becomes
> $$\frac{1+2\varepsilon}{F_{N+1}}$$
>
> **This is the honest reason golden section is used in practice and Fibonacci is not.** Fibonacci needs $N$ decided *in advance* (the $\rho_k$ depend on it), it needs a different ratio at every step, and it needs the $\varepsilon$ patch — **all to gain about 15%.** Golden section is stateless, terminates whenever you like, and is within a constant factor of optimal.

---

### 5. Bisection — the first method to use derivatives

If $f\in C^1$, evaluate $f'$ at the midpoint $x^{(k)}=\tfrac{a_k+b_k}{2}$:

$$f'(x^{(k)})>0\ \Rightarrow\ x^*\in[a_k,x^{(k)}];\qquad f'(x^{(k)})<0\ \Rightarrow\ x^*\in[x^{(k)},b_k];\qquad f'=0\ \Rightarrow\ \text{done}$$

**The bracket halves every step: reduction $(1/2)^N$ — better than golden section's $0.618^N$.**

> [!note] The comparison is not free, and this is the chapter's recurring theme
> **Bisection buys a better rate by requiring $f'$.** For the same problem to accuracy $0.3$ on $[0,2]$: golden section needs $N=4$ (since $0.618^4=0.146\le0.15$), bisection needs $N=3$ (since $0.5^3=0.125\le0.15$).
>
> **Whether that is a win depends entirely on what a derivative costs.** With automatic differentiation a gradient costs a small multiple of a function evaluation, so it usually is. **With a black-box simulator or a physical experiment, $f'$ may not exist at any price** — and then golden section is not merely convenient, it is the only option.

---

### 6. Newton's method in one dimension

**The idea: replace $f$ by the quadratic that matches it to second order, and minimise that instead.**

$$q(x)=f(x^{(k)})+f'(x^{(k)})(x-x^{(k)})+\tfrac12f''(x^{(k)})(x-x^{(k)})^2$$

Setting $q'(x)=0$ and calling the result $x^{(k+1)}$:

$$\boxed{x^{(k+1)}=x^{(k)}-\frac{f'(x^{(k)})}{f''(x^{(k)})}}$$

> [!important] The second reading: Newton is a root-finder aimed at the FONC
> Put $g=f'$. Then the iteration is
> $$x^{(k+1)}=x^{(k)}-\frac{g(x^{(k)})}{g'(x^{(k)})}$$
> which is **Newton's method of tangents** for solving $g(x)=0$: draw the tangent to $g$ at $x^{(k)}$ and take its $x$-intercept.
>
> **So minimising $f$ by Newton is solving [[03 - Unconstrained Optimality Conditions|ch. 03's]] FONC iteratively** — exactly as promised there. **And this is why the method is indifferent to minima versus maxima**: $f'=0$ is all it knows about.

> [!warning] Newton fails in three distinct ways, and all three matter
> 1. **$f''(x^{(k)})<0$.** The fitted quadratic opens *downward*, so its stationary point is a **maximum** and the step moves uphill. Newton converges happily to maxima and saddles.
> 2. **$f''(x^{(k)})\approx0$.** The step $-f'/f''$ blows up and the iterate is thrown far away.
> 3. **A bad starting point.** Even where $f''>0$ everywhere, the step can overshoot the region where the quadratic model is any good.
>
> **Newton is fast and local: it converges quadratically near a minimizer with $f''>0$, and offers no guarantee at all from far away.** Every practical implementation therefore *safeguards* it — bracket it, or damp the step with a line search, or modify $f''$ when it is not positive ([[06 - Newton and Quasi-Newton Methods|ch. 06's]] Levenberg–Marquardt).

> [!example]- Worked example — verified
> Minimise $f(x)=\tfrac12x^2-\sin x$ from $x^{(0)}=0.5$, stopping when $\lvert x^{(k+1)}-x^{(k)}\rvert<10^{-5}$. Here $f'(x)=x-\cos x$ and $f''(x)=1+\sin x>0$ near the solution.
>
> | $k$ | $x^{(k)}$ | $f'(x^{(k)})$ |
> |---|---|---|
> | 0 | $0.500000$ | $-3.78\times10^{-1}$ |
> | 1 | $0.755222$ | $2.71\times10^{-2}$ |
> | 2 | $0.739142$ | $9.46\times10^{-5}$ |
> | 3 | $0.739085$ | $1.18\times10^{-9}$ |
>
> **The exponent of $f'$ roughly doubles each step — the signature of quadratic convergence** ([[01 - The Optimization Problem|ch. 01]] §6). Three steps take the error from $10^{-1}$ to $10^{-9}$. The limit $x^*=0.7390851\ldots$ is the unique root of $x=\cos x$, and $f''(x^*)=1.6736>0$ confirms a strict minimizer by SOSC.

---

### 7. The secant method and the quadratic-fit family

**If $f''$ is unavailable, approximate it from two gradient values:**

$$f''(x^{(k)})\approx\frac{f'(x^{(k)})-f'(x^{(k-1)})}{x^{(k)}-x^{(k-1)}}$$

Substituting into Newton gives the **secant method**:

$$\boxed{x^{(k+1)}=x^{(k)}-\frac{x^{(k)}-x^{(k-1)}}{f'(x^{(k)})-f'(x^{(k-1)})}\,f'(x^{(k)})}$$

**It needs two starting points and one gradient evaluation per step**, and — like Newton — never evaluates $f$ itself.

> [!important] The unifying view: all of §§6–7 are *quadratic fit* methods
> | Method | Fits a quadratic that matches | Data needed |
> |---|---|---|
> | **Newton** | $f'$ and $f''$ at $x^{(k)}$ | 1 point, 2 derivatives |
> | **Secant** | $f'$ at $x^{(k)}$ and $x^{(k-1)}$ | 2 points, 1st derivative |
> | **Inverse parabolic interpolation** | $f$ at $x^{(k)},x^{(k-1)},x^{(k-2)}$ | 3 points, no derivatives |
>
> **Each row trades a derivative for a remembered point.** That single trade is the whole design space, and [[06 - Newton and Quasi-Newton Methods|ch. 06's]] quasi-Newton methods are its multivariable version: BFGS approximates $\nabla^2f$ from a history of gradients exactly as the secant method approximates $f''$ from two.

**The secant method's order of convergence is the golden ratio**, $p=\varphi=\tfrac{1+\sqrt5}{2}\approx1.618$ — **superlinear but not quadratic**. It is slower per step than Newton and cheaper per step, and which wins depends on the cost of $f''$.

> [!tip] Brent's method is what a library actually calls
> **Golden section is robust but slow; parabolic interpolation is fast but can diverge.** Brent's method interleaves them — it attempts a parabolic step, and falls back to a golden-section step whenever the parabolic one is not safely inside the bracket. **The result keeps golden section's guarantees and interpolation's speed**, and is what `scipy.optimize.minimize_scalar` uses by default.

---

### 8. Line search inside a multivariable method

Given $\mathbf x_k$ and a direction $\mathbf d_k$, the **exact line search** chooses

$$\alpha_k=\arg\min_{\alpha>0}\ \phi_k(\alpha),\qquad \phi_k(\alpha)=f(\mathbf x_k+\alpha\mathbf d_k)$$

using any method of §§3–7 — with $\phi_k'(\alpha)=\mathbf d_k^{\mathsf T}\nabla f(\mathbf x_k+\alpha\mathbf d_k)$ if a derivative-based method is chosen.

> [!warning] Exact line search is almost always the wrong thing to do
> Chong & Żak's own summary, and it is worth taking seriously:
> 1. **Minimising $\phi_k$ exactly is expensive** — many evaluations of $f$ per outer iteration.
> 2. **The minimizer of $\phi_k$ may not exist** (e.g. $\phi_k$ decreasing without bound along $\mathbf d_k$).
> 3. **Experience says the arithmetic is better spent on more outer iterations.** $\mathbf d_k$ is only a local guess at a good direction; polishing $\alpha_k$ to eight digits optimises a quantity that will be discarded next step.
>
> **So practical methods do an *inexact* line search: find any $\alpha_k$ that decreases $f$ "enough", and move on.**

---

### 9. **Inexact line search: the Armijo, Goldstein and Wolfe conditions**

**Two things must be prevented: a step that is too long (overshooting, so $f$ barely decreases or increases) and a step that is too short (progress stalls).** Each condition below addresses one or both. Fix constants $\varepsilon\in(0,1)$, $\gamma>1$, $\eta\in(\varepsilon,1)$.

> [!important] The conditions
> **Armijo — sufficient decrease** (rules out steps that are too long):
> $$\phi_k(\alpha_k)\ \le\ \phi_k(0)+\varepsilon\,\alpha_k\,\phi_k'(0)$$
> **Armijo — not too short:**
> $$\phi_k(\gamma\alpha_k)\ >\ \phi_k(0)+\varepsilon\,\gamma\,\alpha_k\,\phi_k'(0)$$
> **Goldstein** (replaces the second Armijo inequality):
> $$\phi_k(\alpha_k)\ \ge\ \phi_k(0)+\eta\,\alpha_k\,\phi_k'(0)$$
> **Wolfe — curvature condition** (uses the derivative instead of the value):
> $$\phi_k'(\alpha_k)\ \ge\ \eta\,\phi_k'(0)$$
> **Strong Wolfe:**
> $$\big\lvert\phi_k'(\alpha_k)\big\rvert\ \le\ \eta\,\big\lvert\phi_k'(0)\big\rvert$$

**How to read the Armijo condition.** Since $\phi_k'(0)=\mathbf d_k^{\mathsf T}\nabla f(\mathbf x_k)<0$ for a descent direction, the right-hand side is a line through $(0,\phi_k(0))$ with slope $\varepsilon\phi_k'(0)$ — **a shallower version of the true initial slope.** Armijo says: *achieve at least the fraction $\varepsilon$ of the decrease that the initial slope promises.* **Typical $\varepsilon=10^{-4}$ — very undemanding**, precisely because its job is only to exclude disasters.

**How to read the Wolfe condition.** $\phi_k'(\alpha_k)\ge\eta\phi_k'(0)$ with $\eta\in(0,1)$ says the slope at the new point must be **substantially less steep** than at the start — you have travelled far enough that the function is flattening out. **Typical $\eta=0.9$ for gradient-type methods, $\eta=0.1$ for Newton-type.**

> [!important] Armijo backtracking — the algorithm you will actually implement
> ```
> α ← 1                       (or any initial guess)
> while φ(α) > φ(0) + ε·α·φ'(0):
>     α ← τ·α                 (τ ∈ (0,1), typically 0.5)
> return α
> ```
> **Four lines, one function evaluation per trial, no bracketing, no derivatives beyond $\phi'(0)$ which you already have.** It terminates in finitely many steps whenever $\mathbf d_k$ is a descent direction, because Armijo holds for all sufficiently small $\alpha$.
>
> **This is what almost every real optimizer does**, and it is why §§3–5's elegant bracket methods are rarely called from inside a multivariable algorithm.

> [!note] Why the Wolfe conditions specifically
> **Armijo alone is enough for gradient descent** to converge. **The Wolfe curvature condition is needed for quasi-Newton methods** (ch. 06): it is exactly the condition guaranteeing $\mathbf s_k^{\mathsf T}\mathbf y_k>0$, which is what keeps the BFGS Hessian approximation positive definite. **Without it, BFGS can produce a non-descent direction and break.**

---

## ✏️ Exercises

> [!question] Exercise 1 — golden section by hand *(easy)*
> Minimise $f(x)=x^2+\dfrac{4}{x}$ on $[1,3]$ using golden section search. Carry out **four** iterations, tabulating the bracket and both interior points. Verify that each bracket width equals $2(0.618034)^k$, and check that the true minimizer lies in the final bracket.

> [!example]- Solution
> $\rho=\tfrac{3-\sqrt5}{2}=0.381966$, $1-\rho=0.618034$. Interior points $p=a+\rho(b-a)$, $q=a+(1-\rho)(b-a)$.
>
> | Iter | $[a,b]$ | width | $p$ | $f(p)$ | $q$ | $f(q)$ | Test | New $[a,b]$ | $2(0.618)^k$ |
> |---|---|---|---|---|---|---|---|---|---|
> | 1 | $[1,\ 3]$ | $2.0000$ | $1.7639$ | $5.3791$ | $2.2361$ | $6.7889$ | $f(p)<f(q)$ | $[1,\ 2.2361]$ | $1.2361$ |
> | 2 | $[1,\ 2.2361]$ | $1.2361$ | $1.4721$ | $4.8843$ | $1.7639$ | $5.3791$ | $f(p)<f(q)$ | $[1,\ 1.7639]$ | $0.7639$ |
> | 3 | $[1,\ 1.7639]$ | $0.7639$ | $1.2918$ | $4.7652$ | $1.4721$ | $4.8843$ | $f(p)<f(q)$ | $[1,\ 1.4721]$ | $0.4721$ |
> | 4 | $[1,\ 1.4721]$ | $0.4721$ | $1.1803$ | $4.7821$ | $1.2918$ | $4.7652$ | $f(p)>f(q)$ | $\boxed{[1.1803,\ 1.4721]}$ | $0.2918$ |
>
> **Every width matches $2(0.618034)^k$ exactly** ✔ — the reduction is deterministic and independent of $f$.
>
> **True minimizer:** $f'(x)=2x-4/x^2=0\Rightarrow x^3=2\Rightarrow x^*=2^{1/3}=1.259921$, with $f(x^*)=4.762203$. **It lies inside $[1.1803,1.4721]$** ✔.
>
> **Two things to notice.**
> - **Iterations 2, 3 and 4 each needed only one new evaluation** — $q$ in iteration 2 is $p$ from iteration 1, and so on. Four iterations cost **five** evaluations, not eight. *That is the entire purpose of the $\rho^2-3\rho+1=0$ derivation.*
> - **The bracket is not centred on $x^*$.** Golden section guarantees the *width*, not the location — after four steps we know $x^*$ to within $\pm0.15$ and nothing more.

---

> [!question] Exercise 2 — how many iterations? *(easy–medium)*
> The initial bracket has width $2$ and you want the final width below $10^{-4}$.
> **(a)** How many iterations for golden section, Fibonacci and bisection?
> **(b)** How many function or derivative evaluations does each cost?
> **(c)** Which would you choose, and on what does the answer depend?

> [!example]- Solution
> **(a)** Require final width $\le10^{-4}$, i.e. reduction factor $\le5\times10^{-5}$.
>
> | Method | Factor | Condition | $N$ |
> |---|---|---|---|
> | **Golden section** | $0.618034^N$ | $N\ge\dfrac{\ln(5\times10^{-5})}{\ln0.618034}=20.6$ | $\boxed{21}$ |
> | **Bisection** | $0.5^N$ | $N\ge\dfrac{\ln(5\times10^{-5})}{\ln0.5}=14.3$ | $\boxed{15}$ |
> | **Fibonacci** | $1/F_{N+1}$ | $F_{N+1}\ge2\times10^{4}$; $F_{20}=17711$, $F_{21}=28657$ | $\boxed{20}$ |
>
> **(b)** Golden section: 2 evaluations for the first iteration, 1 thereafter $=\mathbf{22}$ evaluations of $f$. Fibonacci: same accounting $=\mathbf{21}$ evaluations of $f$. Bisection: **15 evaluations of $f'$**.
>
> **(c) The comparison is not 22 versus 15 — it is 22 evaluations of $f$ versus 15 evaluations of $f'$**, and those are different currencies.
>
> | Situation | Choice | Why |
> |---|---|---|
> | $f$ is a black box (simulator, experiment, tabulated data) | **Golden section** | $f'$ is unavailable at any price |
> | $f'$ available by autodiff | **Bisection or secant** | a gradient costs $\approx2$–$3$ function evaluations, so 15 gradients $\approx$ 40 evaluations — but see below |
> | Inside a multivariable method | **Neither: Armijo backtracking** (§9) | 21 iterations to polish one $\alpha_k$ is indefensible when the direction itself is a guess |
> | $f$ smooth, good starting point, $f''$ cheap | **Newton** | $\approx5$ iterations for the same accuracy |
>
> **Fibonacci is optimal and still loses to bisection**, because optimality is only within the class of methods that compare function values. **Changing the information used beats optimising within a fixed information set** — the single most transferable lesson of the chapter.

---

> [!question] Exercise 3 — Newton in one dimension, and its failures *(medium)*
> Let $f(x)=x^2+\dfrac{4}{x}$ on $x>0$, as in Exercise 1.
> **(a)** Write out the Newton iteration for minimising $f$.
> **(b)** Run it from $x^{(0)}=3$ for five steps. What happens on the first step, and why?
> **(c)** For which $x>0$ is $f''(x)>0$? What would happen if Newton were applied to this $f$ starting from $x^{(0)}<0$?
> **(d)** State one safeguard that fixes the behaviour in (b).

> [!example]- Solution
> **(a)** $f'(x)=2x-\dfrac{4}{x^2}$ and $f''(x)=2+\dfrac{8}{x^3}$, so
> $$x^{(k+1)}=x^{(k)}-\frac{2x^{(k)}-4/(x^{(k)})^2}{2+8/(x^{(k)})^3}$$
>
> **(b)** With $x^*=2^{1/3}=1.259921$:
>
> | $k$ | $x^{(k)}$ | error |
> |---|---|---|
> | 0 | $3.000000$ | $1.74$ |
> | 1 | $\mathbf{0.580645}$ | $0.679$ |
> | 2 | $0.830331$ | $0.430$ |
> | 3 | $1.089561$ | $0.170$ |
> | 4 | $1.234988$ | $2.49\times10^{-2}$ |
> | 5 | $1.259421$ | $5.00\times10^{-4}$ |
>
> **The first step overshoots wildly**, jumping from $3$ to $0.58$ — past the minimizer and most of the way to the singularity at $0$. The reason: at $x=3$, $f''(3)=2+8/27=2.296$ is small (the function is nearly flat there), while $f'(3)=5.56$ is large. **A large gradient divided by a small curvature is a huge step**, and the quadratic model that justified it is only valid near $x=3$.
>
> **After the overshoot the method recovers and the error ratio improves at every step**, reaching quadratic behaviour by $k=4$–$5$: $2.49\times10^{-2}\to5.00\times10^{-4}$ is very nearly a squaring.
>
> **This is Newton's characteristic profile: an erratic global phase followed by an explosively fast local one.**
>
> **(c)** $f''(x)=2+8/x^3>0\iff x^3>-4\iff x>-4^{1/3}=-1.5874$. **So $f''>0$ on all of $x>0$** — the function is strictly convex there, which is why the method converged despite the bad first step.
>
> **For $x^{(0)}<-1.5874$**, $f''<0$: the fitted parabola opens downward, its stationary point is a **maximum**, and Newton steps toward it. The method would converge to $x=-2^{1/3}$, a local *maximum* of $f$ on $x<0$. **Newton solves $f'=0$ and cannot tell a minimum from a maximum** — precisely [[03 - Unconstrained Optimality Conditions|ch. 03's]] point that the FONC is not sufficient.
>
> **(d) Any one of three, in increasing order of sophistication:**
> 1. **Cap the step**: $x^{(k+1)}=x^{(k)}-\min\{1,\Delta/\lvert s_k\rvert\}s_k$ for a trust radius $\Delta$.
> 2. **Damp with a line search**: take $d_k=-f'/f''$ as a *direction* and choose the length by Armijo backtracking (§9). **This is what real implementations do**, and it converts Newton from a fixed iteration into an instance of $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k$.
> 3. **Modify the curvature**: replace $f''$ by $\max\{f'',\delta\}$ for some $\delta>0$, guaranteeing a descent direction. **This is the one-dimensional Levenberg–Marquardt** of [[06 - Newton and Quasi-Newton Methods|ch. 06]].
>
> **All three keep Newton's quadratic local rate and remove the global misbehaviour** — the standard pattern for every second-order method in this subject.

---

> [!question] Exercise 4 — the secant method and its golden order *(medium–hard)*
> Continue with $f(x)=x^2+4/x$, so $g(x)=f'(x)=2x-4/x^2$ and $x^*=2^{1/3}$.
> **(a)** Write the secant iteration and run it from $x^{(-1)}=1$, $x^{(0)}=3$.
> **(b)** Estimate the order of convergence empirically from the error sequence.
> **(c)** The theoretical order is $\varphi=\tfrac{1+\sqrt5}2$. Sketch why the exponents satisfy a Fibonacci-like recursion.
> **(d)** Newton needs $f''$ and converges with $p=2$; secant needs only $f'$ and converges with $p\approx1.618$. When is secant the better choice?

> [!example]- Solution
> **(a)** $$x^{(k+1)}=x^{(k)}-\frac{x^{(k)}-x^{(k-1)}}{g(x^{(k)})-g(x^{(k-1)})}\,g(x^{(k)})$$
>
> Errors $e_k=\lvert x^{(k)}-2^{1/3}\rvert$:
> $$2.70\times10^{-1},\ \ 2.02\times10^{-1},\ \ 4.29\times10^{-2},\ \ 7.18\times10^{-3},\ \ 2.42\times10^{-4},\ \ 1.37\times10^{-6},\ \ 2.64\times10^{-10},\ \ 4.44\times10^{-16}$$
>
> **(b)** If $e_{k+1}\approx Ce_k^{\,p}$ then $p\approx\dfrac{\ln e_{k+1}}{\ln e_k}$ for small errors. Successive estimates:
> $$1.22,\quad 1.97,\quad 1.57,\quad 1.69,\quad 1.62,\quad 1.63$$
> **The estimates oscillate around and settle on $\approx1.62$** ✔, matching $\varphi=1.618034$. *(The oscillation is characteristic: the secant method alternates between "good" and "less good" steps because each step uses one fresh and one stale point.)*
>
> **Note $e_7=4.44\times10^{-16}$ — machine precision — reached in seven steps**, against golden section's 21 iterations for a mere $10^{-4}$ in Exercise 2.
>
> **(c)** Suppose $e_{k+1}\approx Ce_ke_{k-1}$, which is the standard secant error relation (the method interpolates $g$ through two points, so the interpolation error carries one factor from each). Posit $e_k\approx Ae_{k-1}^{\,p}$. Then
> $$e_{k+1}\approx Ae_k^{\,p}\quad\text{and}\quad e_{k+1}\approx Ce_ke_{k-1}=Ce_k\left(\frac{e_k}{A}\right)^{1/p}$$
> Matching the powers of $e_k$ on both sides gives
> $$p=1+\frac1p\quad\Longleftrightarrow\quad p^2-p-1=0\quad\Longrightarrow\quad p=\frac{1+\sqrt5}{2}=\varphi$$
>
> **The exponent obeys $p_{k+1}=p_k+p_{k-1}$ — the Fibonacci recursion — because each new error inherits one factor from each of the two previous ones.** *(A pleasing coincidence of the chapter: the golden ratio governs both the optimal bracket ratio in §3 and the secant convergence order, for entirely unrelated reasons.)*
>
> **(d) Compare cost per digit, not order.** Let $c_f$ be the cost of $f'$ and $c_h$ the cost of $f''$.
>
> | | Newton | Secant |
> |---|---|---|
> | Order | $2$ | $1.618$ |
> | Cost/step | $c_f+c_h$ | $c_f$ |
> | Digits gained per unit cost | $\dfrac{\log2}{c_f+c_h}$ | $\dfrac{\log1.618}{c_f}$ |
>
> **Secant wins when** $\dfrac{\log1.618}{c_f}>\dfrac{\log2}{c_f+c_h}$, i.e. when $c_h>0.44\,c_f$ — **secant is better unless the second derivative costs less than about 44% of the first.**
>
> **In one dimension $f''$ is often cheap and Newton wins. In $n$ dimensions the analogous comparison is decisive**: the Hessian costs $O(n^2)$ storage and $O(n^3)$ to factorise against $O(n)$ for a gradient, so **the multivariable descendant of the secant method — BFGS — displaces Newton almost everywhere** ([[06 - Newton and Quasi-Newton Methods|ch. 06]]).

---

> [!question] Exercise 5 — inexact line search *(hard)*
> Let $f(\mathbf x)=\tfrac12(x_1^2+10x_2^2)$, $\mathbf x_0=(1,1)^{\mathsf T}$, and take the steepest-descent direction $\mathbf d=-\nabla f(\mathbf x_0)$.
> **(a)** Write $\phi(\alpha)=f(\mathbf x_0+\alpha\mathbf d)$ explicitly and find the exact minimizer $\alpha^*$.
> **(b)** Run **Armijo backtracking** with $\varepsilon=0.1$, starting at $\alpha=1$ and halving. Tabulate every trial.
> **(c)** Compare the accepted step with $\alpha^*$: how much worse is it, and how much cheaper?
> **(d)** Check the Wolfe and strong Wolfe conditions at the accepted step with $\eta=0.9$.
> **(e)** State the general principle this exercise illustrates.

> [!example]- Solution
> **(a)** $\nabla f(\mathbf x)=(x_1,\ 10x_2)^{\mathsf T}$, so $\nabla f(\mathbf x_0)=(1,10)^{\mathsf T}$ and $\mathbf d=(-1,-10)^{\mathsf T}$. Then
> $$\phi(\alpha)=\tfrac12\Big[(1-\alpha)^2+10(1-10\alpha)^2\Big]$$
> $$\phi(0)=\tfrac12(1+10)=5.5,\qquad \phi'(0)=\mathbf d^{\mathsf T}\nabla f(\mathbf x_0)=-1-100=-101$$
> Differentiating, $\phi'(\alpha)=-(1-\alpha)-100(1-10\alpha)=1001\alpha-101$, so
> $$\boxed{\alpha^*=\frac{101}{1001}=0.100899},\qquad \phi(\alpha^*)=0.404595$$
>
> *(Sanity check: $\phi'(0)=-101$ is very steep and $\phi''=1001$ is very large — this is a badly scaled problem, deliberately. It is [[05 - Gradient Methods|ch. 05's]] running example, with condition number $\kappa=10$.)*
>
> **(b)** Armijo requires $\phi(\alpha)\le\phi(0)+\varepsilon\alpha\phi'(0)=5.5-10.1\alpha$.
>
> | Trial | $\alpha$ | $\phi(\alpha)$ | Bound $5.5-10.1\alpha$ | Verdict |
> |---|---|---|---|---|
> | 1 | $1$ | $405.000$ | $-4.600$ | reject |
> | 2 | $0.5$ | $80.125$ | $0.450$ | reject |
> | 3 | $0.25$ | $11.531$ | $2.975$ | reject |
> | 4 | $0.125$ | $\mathbf{0.695}$ | $4.238$ | **ACCEPT** |
>
> **Four function evaluations, and the first three are cheap rejections.**
>
> **(c)**
>
> | | $\alpha$ | $\phi$ | new $\mathbf x$ |
> |---|---|---|---|
> | Armijo | $0.125$ | $0.6953$ | $(0.875,\ -0.250)$ |
> | Exact | $0.1009$ | $0.4046$ | $(0.8991,\ -0.0090)$ |
>
> **The Armijo step leaves $f$ at $0.695$ instead of $0.405$ — about 72% higher.** But it cost **4 function evaluations**; an exact line search to 4 significant figures by golden section would need $\approx15$–20 evaluations, or several secant iterations plus a bracketing phase.
>
> **Per unit of arithmetic, Armijo is far ahead**: $f$ dropped from $5.5$ to $0.695$ — a factor of 8 — for four evaluations. *(And note that the exact step overshoots $x_2$ almost exactly to zero, which looks impressive but is an artefact of this quadratic; on a general $f$ the extra precision buys nothing lasting.)*
>
> **(d)** At $\alpha=0.125$: $\phi'(0.125)=1001(0.125)-101=24.125$.
> - **Wolfe:** $\phi'(\alpha)\ge\eta\phi'(0)$, i.e. $24.125\ge0.9\times(-101)=-90.9$ ✔ **(satisfied, easily)**.
> - **Strong Wolfe:** $\lvert\phi'(\alpha)\rvert\le\eta\lvert\phi'(0)\rvert$, i.e. $24.125\le90.9$ ✔ **(satisfied)**.
>
> **Both hold, so this step is acceptable to a BFGS implementation** — which matters, because the Wolfe condition is exactly what guarantees BFGS's Hessian approximation stays positive definite (§9).
>
> *(Observe $\phi'(0.125)=+24.1>0$: the accepted point is **past** the minimizer of $\phi$, on the upslope. Armijo permits this — it only demands sufficient decrease, not that you stop at the bottom.)*
>
> **(e) The principle: $\alpha_k$ does not deserve precision, because $\mathbf d_k$ does not deserve it either.**
>
> The direction $\mathbf d_k$ is a *local* guess — for steepest descent it is the best direction only in an infinitesimal neighbourhood, and here it is a demonstrably poor one: $\mathbf d=(-1,-10)$ points **39° away** from $(-1,-1)$, the direction that actually leads to the minimizer, thanks to $\kappa=10$. **Minimising exactly along a mediocre direction is a precise answer to the wrong question.**
>
> **The right allocation is: spend a few evaluations to guarantee real progress, then recompute the direction.** Formally, the Armijo and Wolfe conditions are exactly strong enough to prove global convergence (via Zoutendijk's condition) and no stronger — **they are the minimum a line search must deliver, and modern practice delivers exactly that minimum.**

---

## 📝 Summary

- **Every multivariable method contains a line search**: minimise $\phi_k(\alpha)=f(\mathbf x_k+\alpha\mathbf d_k)$, with $\phi_k'(\alpha)=\mathbf d_k^{\mathsf T}\nabla f(\mathbf x_k+\alpha\mathbf d_k)$ **needing only the gradient**.
- **Bracket methods assume only unimodality.** Two interior points and one comparison discard part of the interval; one point tells you nothing.
- **Golden section** uses $\rho=\tfrac{3-\sqrt5}2\approx0.382$, chosen so each step reuses a point and costs **one** new evaluation. Reduction $0.618^N$.
- **Fibonacci** is provably optimal among value-comparison methods, with reduction $1/F_{N+1}$, **but requires $N$ in advance and needs an $\varepsilon$ patch at the last step** — it beats golden section by about 15% and is rarely worth it.
- **Bisection** halves the bracket per step using $f'$. **A better rate bought with better information** — the recurring trade of the chapter.
- **Newton** fits a quadratic matching $f'$ and $f''$: $x^{(k+1)}=x^{(k)}-f'/f''$. **Quadratically convergent near a minimizer with $f''>0$, and unreliable far away** — it converges to maxima and saddles just as happily, since it only solves $f'=0$.
- **Secant** replaces $f''$ by a difference of two gradients. **Order $\varphi\approx1.618$**, and it is the one-dimensional ancestor of BFGS. **Newton, secant and inverse parabolic interpolation are the same idea trading a derivative for a remembered point.**
- **Exact line search is the wrong default**: expensive, sometimes non-existent, and wasteful because $\mathbf d_k$ is itself only a guess.
- **Use inexact conditions instead.** **Armijo** demands sufficient decrease $\phi(\alpha)\le\phi(0)+\varepsilon\alpha\phi'(0)$; **Wolfe** adds a curvature condition $\phi'(\alpha)\ge\eta\phi'(0)$ needed to keep quasi-Newton updates positive definite. **Armijo backtracking is four lines of code and is what real optimizers use.**

---

## ⚠️ Important Notes

> [!warning] The six errors
> 1. **Applying a bracket method to a non-unimodal $f$.** The comparison logic is simply false, and the method converges confidently to nothing in particular.
> 2. **Using golden section's $\rho$ as $0.618$.** $\rho=0.382$; $1-\rho=0.618$. Both numbers appear and swapping them inverts the interval.
> 3. **Forgetting that Newton's method has no idea what it is converging to.** $f'=0$ includes maxima and inflections.
> 4. **Using Newton unsafeguarded.** It needs a step cap, a line search, or a curvature modification — see Exercise 3(d).
> 5. **Doing an exact line search inside a multivariable method.** Almost always a waste; see Exercise 5(e).
> 6. **Choosing $\varepsilon$ too large in Armijo.** $\varepsilon$ near 1 demands almost the full linear decrease, which is achievable only for tiny $\alpha$ — the line search then returns useless steps and the outer method stalls. **Use $\varepsilon=10^{-4}$.**

> [!tip] Which method, in one table
> | You have | Problem shape | Use |
> |---|---|---|
> | $f$ only, black box | standalone 1-D | **golden section**, or **Brent** if you can call a library |
> | $f$ and $f'$ | standalone 1-D | **secant**, bracketed |
> | $f$, $f'$, $f''$, good start | standalone 1-D | **Newton**, safeguarded |
> | anything | **inside a multivariable method** | **Armijo backtracking** — nothing else |

> [!note] Where this chapter is used
> - **[[05 - Gradient Methods|Ch. 05]]–[[08 - Least Squares and Linear Equations|08]]** call §9 at every iteration. Exercise 5's $f=\tfrac12(x_1^2+10x_2^2)$ is ch. 05's running example.
> - **[[06 - Newton and Quasi-Newton Methods|Ch. 06]]** is §§6–7 in $n$ dimensions: Newton with $\nabla^2f$ in place of $f''$, and **BFGS as the multivariable secant method**. The Wolfe condition of §9 is what makes BFGS work.
> - **[[03 - Unconstrained Optimality Conditions|Ch. 03]]** — Newton here *is* the FONC solved iteratively, as promised there.
> - **[[Calculus/contents/03 - Applications of Differentiation|Calculus ch. 03]]** covers Newton's method for root-finding and its quadratic convergence; **§6 here is the same algorithm applied to $f'$ rather than $f$.**
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]** — Newton–Raphson for the MLE score equation is §6 verbatim, and **Fisher scoring replaces $f''$ by its expectation**, which is exactly the secant method's trade of exactness for cheapness.

---

> [!warning] Gaps in the source material
> **Source.** Chapter 7 of Chong & Żak, with §9's Wolfe/Goldstein material cross-checked against Luenberger & Ye §8.1. **Chong & Żak state the inexact-line-search conditions in half a page and do not analyse them**; Luenberger & Ye develop them properly, so the discussion in §9 leans on the latter.
>
> **OCR damage:**
> - **The superscript iteration index is destroyed everywhere.** `x^`, `x(fc)`, `χ^+^`, `x(fe+1)`, `χ^~^`, `x^k_1\` are all $x^{(k)}$ or a neighbour of it, and **`fc` is invariably `k`.** In the secant formula the two indices $k$ and $k-1$ are frequently indistinguishable in the extraction.
> - **Every displayed fraction collapses.** The Newton update extracts as `f"{xwy` on one line with the numerator elsewhere; the secant formula loses its main fraction bar entirely. **All formulas here were reconstructed from the definitions and re-derived.**
> - **`ρ` reads as `p` and `P` throughout**, and `pfc` is $\rho_k$; `Λ/5` and `\/5` and `^5` are all $\sqrt5$; `ε` reads as `e`, `g` and `£`; `η` as `n`; `γ` as `7`; `φ` as `0` (so `0fc(afc)` is $\phi_k(\alpha_k)$ and `0!b(O)` is $\phi_k'(0)$); `α` as `a`, `ct`, `ο:` and `<*`.
> - **The Fibonacci table survives** but `F_i = 0` and `Fo = 1` print as `F_i` and `Fo`.
> - **Every figure is an image and all are lost** — Figures 7.1 (a unimodal function), 7.2–7.4 (**the geometric derivation of $\rho$**, which is where the equation $\rho(1-\rho)=1-2\rho$ comes from), 7.5 (the Fibonacci step diagram), 7.6–7.7 (**Newton succeeding with $f''>0$ and failing with $f''<0$ — the picture that makes §6's warning obvious**), 7.8–7.10 (tangent and secant root-finding), 7.11 (bracketing by expanding steps) and 7.12 (line search in $\mathbb R^n$). **The derivations in §§3–4 above had to be given algebraically because their figures carried the argument.**
>
> **Verification performed.** Every number was recomputed with `numpy` and `sympy`:
> - **Example 7.1** (golden section): $\rho=0.381966$, all four iterations, all eight function values, and the final width $0.2918<0.3$ — **every printed value reproduces exactly.** The true minimizer $0.780884$ was computed independently and lies in the final bracket.
> - **Example 7.3** (bisection): $0.5^3=0.125\le0.15$ and $0.5^2=0.25>0.15$, so $N=3$ ✔.
> - **Example 7.4** (Newton on $\tfrac12x^2-\sin x$): all iterates reproduce; $f''(x^{(3)})=1.6736$ matches the printed $1.673$ ✔. *(The printed $f'(x^{(4)})=-8.6\times10^{-6}$ does not match the exact iteration, which reaches $\lvert f'\rvert<10^{-9}$ by step 3; the discrepancy is consistent with the book carrying 4-decimal intermediates by hand, and the limit $0.7390851$ is correct either way.)*
> - **Exercises 1–5**: all values, including the empirical secant order $\approx1.62$, the Armijo table, and the Wolfe checks.
>
> **Two genuine errors found in Chong & Żak ch. 7**, both in worked examples, both verified:
>
> **1. Example 7.5 (Newton for root-finding) contains an arithmetic error that propagates.** The book prints
> $$x^{(1)}=12-\frac{102.6}{146.65}=11.33$$
> **but $102.6/146.65=0.699625$, so $x^{(1)}=11.3004$, not $11.33$.** This is not an OCR artefact: **the book's *next* step uses $14.73/116.11$, and $g(11.33)=14.7276$ with $g'(11.33)=116.1047$ — the values at $11.33$, not at $11.30$** *(at $11.30$ they would be $11.264$ and $114.80$)*. **So the erroneous value was genuinely carried forward.** The book then prints $x^{(2)}=11.21$, whereas $11.33-14.73/116.11=11.2031$, which rounds to $11.20$. **The true root is exactly $11.2$** ($g$ factors with roots $-1.5$, $2.5$, $11.2$), and the correct iteration gives $11.3004\to11.2019$. **The error is masked because Newton is self-correcting** — which is itself worth noticing.
>
> **2. Example 7.6 (secant for root-finding) uses the wrong pair of points on its second step.** With $x^{(-1)}=13$, $x^{(0)}=12$, the book prints $x^{(1)}=11.40$ **(correct — the exact value is $11.4016$)** and $x^{(2)}=11.25$. **But the secant recursion applied to the two most recent iterates, $x^{(0)}=12$ and $x^{(1)}=11.4016$, gives $x^{(2)}=11.2272$, i.e. $11.23$.** The printed $11.25$ is reproduced exactly by pairing $x^{(-1)}=13$ with $x^{(1)}$ instead ($11.2537$), **so the likely cause is retaining the stale point $x^{(-1)}$ rather than discarding it.** *(Using the two most recent iterates is the definition of the method, and is what makes its order $\varphi$ rather than 1.)*
>
> **Both errors are in examples, not in any stated theorem**, and neither affects the theory. **They are recorded because a student checking their own arithmetic against the book would conclude, wrongly, that they had made a mistake.**
>
> **Scope and additions.**
> - **§9's reading of the Armijo and Wolfe conditions is my own.** Chong & Żak list all five conditions in a single paragraph with no interpretation and no algorithm; **the geometric reading (Armijo = "achieve fraction $\varepsilon$ of the promised decrease", Wolfe = "get far enough that the slope flattens"), the backtracking pseudocode, the typical parameter values, and the remark that Wolfe is what keeps BFGS positive definite are all added** from Luenberger & Ye and standard practice.
> - **The cost-per-digit comparison in Exercise 4(d) is my own**, as is the derivation of $p=\varphi$ from $e_{k+1}\approx Ce_ke_{k-1}$ — Chong & Żak assert the secant method's order nowhere in ch. 7.
> - **Exercise 2's "different currencies" point and the summary table of §Which method are mine.** The book compares reduction factors without ever noting that comparing $f$-evaluations to $f'$-evaluations is not comparing like with like.
> - **The Brent's-method remark is Chong & Żak's** (one sentence, citing Brent); the note that it is `scipy`'s default is mine.

#optimization #line-search #golden-section #fibonacci-search #bisection #newton-method #secant-method #armijo #wolfe-conditions #backtracking
