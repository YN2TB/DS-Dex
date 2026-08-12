---
subject: Optimization
chapter: 01
tags: [ds, optimization, minimizer, standard-form, convergence-rate, iterative-algorithms]
source: "Chong & Żak, *An Introduction to Optimization* 4e, §§6.1, 8.3; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 1"
---

# The Optimization Problem

> [!abstract] What this chapter is for
> **Almost every quantitative task in this degree is an optimization problem wearing a disguise.** OLS minimises squared residuals; maximum likelihood maximises $\ell(\theta)$; training a network minimises a loss; a firm maximises profit subject to a budget. **This chapter sets up the object they all share and the vocabulary for talking about the algorithms that solve it.**
>
> | § | Question | Short answer |
> |---|---|---|
> | **1** | What *is* an optimization problem? | $\min f(\mathbf x)$ subject to $\mathbf x\in\Omega$ — and everything else is notation |
> | **2** | What counts as a solution? | **Global, local, strict** — and they are genuinely different things |
> | **3** | Does a solution exist? | **Weierstrass**: continuous $f$ on a *compact* $\Omega$. Drop either hypothesis and it can fail |
> | **4** | Which problems are hard? | **Convex vs non-convex, not linear vs nonlinear** |
> | **5** | How do algorithms work? | $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k$ — **all of them** |
> | **6** | How fast? | **Order of convergence.** Linear vs quadratic is the difference between 40 steps and 6 |
>
> **§6 is the section that repays study.** "Converges" is nearly worthless information on its own; the whole comparative theory of chapters 04–08 is about *how fast*.

---

## 📘 Main Knowledge

### 1. The standard form

> [!important] The problem
> $$\begin{aligned}\text{minimize}\quad & f(\mathbf x)\\ \text{subject to}\quad & \mathbf x\in\Omega\end{aligned}$$
>
> - $f:\mathbb R^n\to\mathbb R$ is the **objective function** (or **cost function**, or **performance index**)
> - $\mathbf x=[x_1,\dots,x_n]^{\mathsf T}$ is the vector of **decision variables**
> - $\Omega\subseteq\mathbb R^n$ is the **constraint set** or **feasible set**
>
> If $\Omega=\mathbb R^n$ the problem is **unconstrained**. Otherwise "$\mathbf x\in\Omega$" is a **set constraint**.

**Constraints usually arrive as functions rather than as a set.** The general form is

$$\Omega=\{\mathbf x: \mathbf h(\mathbf x)=\mathbf 0,\ \mathbf g(\mathbf x)\le\mathbf 0\}$$

with $m$ **equality constraints** $h_i$ and $p$ **inequality constraints** $g_j$; these are **functional constraints**. Chapters 09–12 are entirely about what those two families do to the problem.

> [!tip] Three normalisations that cost nothing
> **Everything can be put in the form above, so there is no loss of generality.**
>
> 1. **Maximisation is minimisation.** $\arg\max f=\arg\min(-f)$, and $\max f=-\min(-f)$. **Only the optimal *value* changes sign; the optimal *point* does not.**
> 2. **A $\ge$ constraint is a $\le$ constraint.** $g(\mathbf x)\ge0\iff -g(\mathbf x)\le0$.
> 3. **An equality is two inequalities.** $h=0\iff h\le0$ and $-h\le0$. *(Legal, but usually a bad idea — it destroys the regularity conditions of ch. 11 and doubles the constraint count.)*
>
> **Every textbook picks a convention and every textbook picks a different one.** Chong & Żak minimise with $g\le0$; economics texts maximise with $g\ge0$; solvers vary. **The sign of the multipliers in ch. 11 depends entirely on which you chose**, and mixing conventions is the single most common source of sign errors in the subject.

---

### 2. Minimizers: three definitions, and the differences matter

> [!important] Definitions
> Let $\mathbf x^*\in\Omega$.
>
> | Term | Condition |
> |---|---|
> | **Global minimizer** | $f(\mathbf x^*)\le f(\mathbf x)$ for all $\mathbf x\in\Omega$ |
> | **Strict global minimizer** | $f(\mathbf x^*)<f(\mathbf x)$ for all $\mathbf x\in\Omega$, $\mathbf x\ne\mathbf x^*$ |
> | **Local minimizer** | there is $\varepsilon>0$ with $f(\mathbf x^*)\le f(\mathbf x)$ for all $\mathbf x\in\Omega$ within distance $\varepsilon$ |
> | **Strict local minimizer** | as above with $<$ for $\mathbf x\ne\mathbf x^*$ |
>
> **Maximizers are defined symmetrically; both are called *extremizers*.**

**Three distinctions worth being pedantic about:**

- **Minimizer vs minimum.** The **minimizer** is the *point* $\mathbf x^*$; the **minimum** is the *value* $f(\mathbf x^*)$. There can be many minimizers and only one minimum.
- **Local vs global is the central difficulty of the subject.** **Every algorithm in chapters 04–08 finds local minimizers.** Nothing in them can tell you whether the point found is global — that information comes only from **convexity** (ch. 02) or from exhaustive search.
- **Non-uniqueness is normal.** $f(\mathbf x)=(\mathbf a^{\mathsf T}\mathbf x-b)^2$ with $n>1$ has a whole hyperplane of global minimizers. **If there are many, finding any one of them suffices** — but "the" optimum is then a misleading phrase, and in machine learning the choice among them (which the algorithm makes implicitly) is exactly what regularisation is for.

> [!warning] The word "optimal" hides an assumption
> Calling $\mathbf x^*$ *optimal* asserts a global property. **What an algorithm actually returns is a point where it stopped moving**, and those are two different claims. Chapter 03 makes the gap precise: **stationarity is necessary, never sufficient.**

---

### 3. Does a minimizer exist?

> [!important] Weierstrass' extreme value theorem
> **If $f$ is continuous and $\Omega$ is non-empty, closed and bounded (i.e. compact), then $f$ attains both a global minimum and a global maximum on $\Omega$.**

**All three hypotheses are needed, and each fails in a way you will meet:**

| Failure | Example | What goes wrong |
|---|---|---|
| $\Omega$ not **bounded** | $f(x)=e^{-x}$ on $[0,\infty)$ | $\inf f=0$, never attained |
| $\Omega$ not **closed** | $f(x)=x$ on $(0,1)$ | $\inf f=0$, not in the set |
| $f$ not **continuous** | $f(x)=x$ for $x>0$, $f(0)=1$, on $[0,1]$ | $\inf f=0$, not attained |

> [!note] Why this matters in practice, not just in proofs
> **Unbounded feasible sets are the normal case in statistics** — $\theta\in\mathbb R^p$, $\sigma>0$ — and unbounded likelihoods are a real phenomenon, not a pathology. **The likelihood of a two-component normal mixture is unbounded**: send one component's mean to a data point and its variance to zero and $\ell\to\infty$. There is no maximum; the "MLE" everyone reports is a well-behaved *local* maximizer chosen by the algorithm. See [[Mathematical Statistics/contents/00-Index|Math Stats]].
>
> **The optimization-theoretic content of "add a penalty term" is often exactly this**: $+\lambda\lVert\boldsymbol\theta\rVert^2$ makes the sublevel sets bounded, so Weierstrass applies and a minimizer exists. **Regularisation buys existence before it buys anything statistical.**

---

### 4. The taxonomy, and what actually makes a problem hard

| Class | Form | Difficulty |
|---|---|---|
| **Linear program (LP)** | $f$ and all constraints affine | **Easy** — polynomial time, solved at scale (ch. 09–10) |
| **Convex quadratic program (QP)** | $f=\tfrac12\mathbf x^{\mathsf T}Q\mathbf x+\mathbf c^{\mathsf T}\mathbf x$ with $Q\succeq0$, affine constraints | **Easy** |
| **General convex program** | convex $f$, convex $\Omega$ | **Easy** — a local minimum is global (ch. 12) |
| **Smooth non-convex** | differentiable, no convexity | **Local guarantees only** |
| **Integer / combinatorial** | $\mathbf x\in\mathbb Z^n$ | **NP-hard in general, even when everything is linear** |
| **Non-smooth** | $f$ not differentiable | Needs subgradients; harder than smooth, not hopeless |

> [!important] The folk theory is wrong
> **"Linear is easy, nonlinear is hard" is not the dividing line.** Integer *linear* programming is NP-hard; convex *quadratic* programming is easy. **The line is convexity, and secondarily smoothness.**
>
> **The version to remember:** a problem is tractable when local information (a gradient) reliably tells you about global structure. **Convexity is exactly the property that makes that true.**

**Size is a separate axis.** Luenberger & Ye's classification, updated: *small* (a handful of variables — solvable by hand), *intermediate* (up to a few thousand — any general-purpose solver), *large-scale* (millions of variables, and **only if the structure is sparse**). **Modern deep learning sits far past the right edge of that table** — hundreds of millions of variables, dense, non-convex — which is why it uses none of the algorithms in chapters 06–07 and only a modified version of chapter 05's.

---

### 5. Iterative algorithms: one template, many methods

Except for the simplex method, **nothing in this subject solves a problem in closed form.** Every algorithm generates a sequence $\mathbf x_0,\mathbf x_1,\mathbf x_2,\dots$ intended to approach $\mathbf x^*$, and every one has the same shape:

$$\boxed{\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k}$$

- $\mathbf d_k$ is the **search direction** — where to go
- $\alpha_k>0$ is the **step size** or **step length** — how far

**A *descent* direction is one with $\mathbf d_k^{\mathsf T}\nabla f(\mathbf x_k)<0$**: moving along it decreases $f$, at least for small enough steps. That inequality is the whole reason $-\nabla f$ is the obvious first choice (ch. 05).

**The methods differ only in how $\mathbf d_k$ is chosen and how much curvature information that costs** — see the table in [[00-Index|the index]]. **Chapter 04 is about $\alpha_k$; chapters 05–07 are about $\mathbf d_k$.**

> [!note] Three questions to ask of any algorithm, in this order
> 1. **Is each step a descent step?** (Does $f$ actually decrease?)
> 2. **Does the sequence converge at all, from any starting point?** — *global convergence analysis*.
> 3. **How fast, once it is close?** — *local convergence analysis*, §6.
>
> **These are independent.** An algorithm can decrease $f$ at every step and converge to nothing useful; it can converge globally but so slowly as to be worthless. Luenberger & Ye's line is the right attitude: *"One good theory is worth a thousand computer runs."*

**Stopping.** No algorithm reaches $\mathbf x^*$ exactly, so it stops on a criterion:

$$\lVert\nabla f(\mathbf x_k)\rVert<\varepsilon,\qquad \lVert\mathbf x_{k+1}-\mathbf x_k\rVert<\varepsilon,\qquad |f(\mathbf x_{k+1})-f(\mathbf x_k)|<\varepsilon$$

> [!warning] Absolute stopping criteria are scale-dependent and therefore wrong
> **Multiplying $f$ by 1000 multiplies every gradient by 1000** and changes nothing about the problem — but it changes when your algorithm stops. **Use relative tests:**
> $$\frac{|f(\mathbf x_{k+1})-f(\mathbf x_k)|}{\max\{1,|f(\mathbf x_k)|\}}<\varepsilon \qquad\text{or}\qquad \frac{\lVert\nabla f(\mathbf x_k)\rVert}{\max\{1,\lVert\nabla f(\mathbf x_0)\rVert\}}<\varepsilon$$
> **And a small gradient does not mean a small error.** In an ill-conditioned problem the two can be many orders of magnitude apart — precisely what ch. 05's condition number measures.

---

### 6. **Rate of convergence** — the quantity that decides everything

> [!important] Order of convergence (Chong & Żak §8.3)
> Let $\mathbf x_k\to\mathbf x^*$. The **order of convergence** is the number $p$ for which
> $$0<\lim_{k\to\infty}\frac{\lVert\mathbf x_{k+1}-\mathbf x^*\rVert}{\lVert\mathbf x_k-\mathbf x^*\rVert^{\,p}}<\infty$$
> (with $0/0$ read as $0$). If the limit is $0$ for **every** $p>0$, the order is $\infty$.

| Order | Name | Behaviour of the error $e_k$ |
|---|---|---|
| $p=1$, limit $\gamma\in(0,1)$ | **Linear** (geometric) | $e_k\approx\gamma^k$ — **a fixed number of digits per step** |
| $p=1$, limit $0$ | **Superlinear** | Faster than any fixed ratio |
| $p=2$ | **Quadratic** | $e_{k+1}\approx ce_k^2$ — **the number of correct digits doubles each step** |

**Worked examples** (all four are Chong & Żak's, verified):

| Sequence | Order |
|---|---|
| $x_k=1/k$ | **1** (linear) |
| $x_k=\gamma^k$, $0<\gamma<1$ | **1** (linear, ratio $\gamma$) |
| $x_k=\gamma^{(q^k)}$, $q>1$ | **$q$** |
| $x_k=1$ for all $k$ (i.e. exact after finitely many steps) | **$\infty$** |

> [!important] Why linear vs quadratic is not a small difference
> Start at error $\tfrac12$ and ask for $10^{-12}$:
>
> | Method | Recurrence | Steps needed |
> |---|---|---|
> | Linear, $\gamma=0.9$ | $e_{k+1}=0.9\,e_k$ | **256** |
> | Linear, $\gamma=0.5$ | $e_{k+1}=0.5\,e_k$ | **39** |
> | Superlinear, $p=1.618$ (secant) | $e_{k+1}=e_k^{1.618}$ | **8** |
> | Quadratic, $p=2$ (Newton) | $e_{k+1}=e_k^{2}$ | **6** |
>
> The quadratic sequence is $\tfrac12,\ \tfrac14,\ 6.3\times10^{-2},\ 3.9\times10^{-3},\ 1.5\times10^{-5},\ 2.3\times10^{-10},\ 5.4\times10^{-20}$. **It goes past double precision in seven steps.**
>
> **But read the $\gamma=0.9$ row again.** Linear convergence with a ratio near 1 is *linear convergence* and is also *useless*. **The ratio matters as much as the order** — and for steepest descent that ratio is set by the condition number (ch. 05), which is why an ill-conditioned problem can take thousands of iterations for an algorithm whose convergence theorem looks perfectly respectable.

> [!note] The order can be read off a big-$O$ statement
> **Theorem (C&Ż 8.5).** If $\lVert\mathbf x_{k+1}-\mathbf x^*\rVert=O\!\left(\lVert\mathbf x_k-\mathbf x^*\rVert^{p}\right)$ then the order of convergence is **at least** $p$; if the $O$ is a little-$o$, the order **strictly exceeds** $p$.
>
> **This is how Newton's method is proved quadratic in ch. 06** — you never compute the limit, you just bound the error by a constant times the previous error squared. **No convergent sequence has order below 1.**

---

## ✏️ Exercises

> [!question] Exercise 1 — normalising a problem *(easy)*
> Convert to the standard minimisation form $\min\mathbf c^{\mathsf T}\mathbf y$ subject to $A\mathbf y=\mathbf b$, $\mathbf y\ge\mathbf 0$:
> $$\begin{aligned}\text{maximize}\quad & 3x_1+6x_2+x_3\\ \text{subject to}\quad & x_1+x_2+x_3\le10\\ & x_1-x_2\ge2\\ & x_1+2x_3=6\\ & x_1\ge0,\quad x_2\le0,\quad x_3\ \text{free}\end{aligned}$$
> State the transformation for each variable, then confirm that the two problems have the same optimal value.

> [!example]- Solution
> **Four separate normalisations, one per irregularity.**
>
> **(i) Maximise $\to$ minimise.** Minimise $-3x_1-6x_2-x_3$; negate the optimal value at the end.
>
> **(ii) A non-positive variable.** Put $x_2'=-x_2\ge0$, so $x_2=-x_2'$.
>
> **(iii) A free variable.** Put $x_3=x_3^+-x_3^-$ with $x_3^+,x_3^-\ge0$. *(Every real number is a difference of two non-negatives.)*
>
> **(iv) Inequalities $\to$ equalities.** Add a **slack** to a $\le$ and subtract a **surplus** from a $\ge$:
> $$x_1+x_2+x_3+s_1=10,\qquad x_1-x_2-s_2=2,\qquad s_1,s_2\ge0$$
>
> **Assembling**, with $\mathbf y=(x_1,\ x_2',\ x_3^+,\ x_3^-,\ s_1,\ s_2)^{\mathsf T}\ge\mathbf 0$:
> $$\text{minimize}\quad -3x_1+6x_2'-x_3^++x_3^-$$
> $$\begin{aligned} x_1-x_2'+x_3^+-x_3^-+s_1&=10\\ x_1+x_2'\phantom{{}+x_3^+-x_3^-}\ -s_2&=2\\ x_1\phantom{{}-x_2'}+2x_3^+-2x_3^-\phantom{{}+s_1}&=6\end{aligned}$$
>
> **Check.** Both forms optimise to $\mathbf x^*=(14,\,0,\,-4)$ with value $\boxed{38}$; the standard form returns $\mathbf y^*=(14,0,0,4,0,12)$ and objective $-38$, and $x_3=x_3^+-x_3^-=0-4=-4\ \checkmark$.
>
> **Note the price.** Three variables became six, and one inequality-constrained problem became an equality-constrained one. **The simplex method of ch. 09 requires this form**, so the cost is unavoidable there — but the free-variable split in particular is worth avoiding when a solver accepts bounds directly, because $x_3^+$ and $x_3^-$ are never both positive at an optimum and the split makes the basis matrix rank-deficient in a way that hurts numerically.

---

> [!question] Exercise 2 — global, local, strict *(easy–medium)*
> Let $f(x)=3x^4-4x^3-12x^2+5$.
> **(a)** Find and classify all local minimizers and maximizers on $\Omega=\mathbb R$. Which is global?
> **(b)** Now take $\Omega=[-2,1]$. Where is the global minimizer, and what is $f'$ there?
> **(c)** What does (b) say about the usefulness of "$f'(x^*)=0$" as a test?

> [!example]- Solution
> **(a)** $f'(x)=12x^3-12x^2-24x=12x(x-2)(x+1)$, so the critical points are $x=-1,0,2$. With $f''(x)=36x^2-24x-24$:
>
> | $x$ | $f(x)$ | $f''(x)$ | Classification |
> |---|---|---|---|
> | $-1$ | $0$ | $36>0$ | **strict local minimizer** |
> | $0$ | $5$ | $-24<0$ | strict local maximizer |
> | $2$ | $-27$ | $72>0$ | **strict local minimizer** |
>
> Since $f\to+\infty$ as $x\to\pm\infty$, the global minimum is the smaller of the two local ones: $\boxed{x^*=2,\ f(x^*)=-27}$, a **strict global minimizer**. **$x=-1$ is a strict local minimizer that is not global** — exactly the situation every algorithm in this subject can be trapped by.
>
> There is **no global maximizer**: $\sup f=+\infty$ and $\Omega=\mathbb R$ is unbounded, so Weierstrass does not apply.
>
> **(b)** On $[-2,1]$ the compact set makes both extrema exist. Candidates are the interior critical points $-1,0$ and the endpoints $-2,1$:
> $$f(-2)=37,\quad f(-1)=0,\quad f(0)=5,\quad f(1)=-8$$
> The global minimizer is $\boxed{x^*=1}$, an **endpoint**, with $f(1)=-8$. And
> $$f'(1)=12-12-24=-24\ne0$$
>
> **(c) The stationarity test finds nothing at $x=1$.** The minimizer sits on the boundary, where $f$ is still decreasing but the feasible set runs out. **A constrained minimizer need not be a critical point** — the correct first-order condition on a constrained set is the one in ch. 03,
> $$\mathbf d^{\mathsf T}\nabla f(\mathbf x^*)\ge0\quad\text{for every \emph{feasible} direction }\mathbf d$$
> which at $x=1$ reads $d\cdot(-24)\ge0$ for the only feasible direction $d<0$ — satisfied. **$\nabla f=\mathbf 0$ is the special case of that condition when $\mathbf x^*$ is interior**, and using it in the boundary case is one of the standard errors of the subject.

---

> [!question] Exercise 3 — order of convergence *(medium)*
> Determine the order of convergence of each sequence, and the limiting ratio where the order is 1.
> **(a)** $x_k=\dfrac{1}{k}$  **(b)** $x_k=\left(\tfrac13\right)^k$  **(c)** $x_k=\left(\tfrac12\right)^{3^k}$  **(d)** $x_k=\dfrac{1}{k!}$  **(e)** $x_k=2+10^{-2^k}$

> [!example]- Solution
> Each converges; write $e_k=|x_k-x^*|$ and test $\lim e_{k+1}/e_k^{\,p}$.
>
> **(a)** $x^*=0$, $e_k=1/k$. With $p=1$: $\dfrac{1/(k+1)}{1/k}=\dfrac{k}{k+1}\to1$. The limit is $1$, which is finite and non-zero, so the **order is 1**. **But the ratio is $1$, not less than 1** — this is *sublinear* in the practical sense and is disastrously slow: to gain one decimal digit you need ten times as many steps. *(Compare: $\sum 1/k$ diverging.)*
>
> **(b)** $x^*=0$, $e_k=3^{-k}$. $\dfrac{3^{-(k+1)}}{3^{-k}}=\tfrac13$ — finite and non-zero, so **order 1, ratio $\gamma=\tfrac13$: linear.** With any $p>1$ the ratio $\to\infty$; with $p<1$ it $\to0$. **This is what "linear convergence" should mean** — a fixed factor per step, here $\log_{10}3\approx0.48$ digits per iteration.
>
> **(c)** $x^*=0$, $e_k=\gamma^{(3^k)}$ with $\gamma=\tfrac12$. Then
> $$\frac{e_{k+1}}{e_k^{\,p}}=\frac{\gamma^{3^{k+1}}}{\gamma^{p\cdot3^k}}=\gamma^{3^k(3-p)}$$
> which $\to0$ if $p<3$, $\to\infty$ if $p>3$, and equals $1$ if $p=3$. **Order 3 (cubic).** *(This is C&Ż's general example $\gamma^{(q^k)}$, which has order exactly $q$.)*
>
> **(d)** $x^*=0$, $e_k=1/k!$. $\dfrac{e_{k+1}}{e_k}=\dfrac{k!}{(k+1)!}=\dfrac{1}{k+1}\to0$, so the order is **not** 1 with a non-zero limit. For $p>1$: $\dfrac{e_{k+1}}{e_k^p}=\dfrac{(k!)^p}{(k+1)!}\to\infty$ for every $p>1$. **So no $p$ gives a finite non-zero limit: the order is 1, superlinearly.** **"Superlinear" is the honest description** — faster than any fixed geometric ratio, slower than quadratic. This is the rate of a good quasi-Newton method (ch. 06).
>
> **(e)** $x^*=2$, $e_k=10^{-2^k}$. By the computation in (c) with $\gamma=10^{-1}$, $q=2$: **order 2, quadratic.** The errors are $10^{-2},10^{-4},10^{-8},10^{-16},\dots$ — **the digit count doubles**, which is the signature of Newton's method.

---

> [!question] Exercise 4 — how many iterations? *(medium)*
> An algorithm is stopped when the error falls below $10^{-12}$, starting from $e_0=\tfrac12$.
> **(a)** How many steps for a linearly convergent method with ratio $\gamma=0.5$? With $\gamma=0.9$?
> **(b)** How many for a quadratically convergent method with $e_{k+1}=e_k^2$?
> **(c)** A colleague reports that their new method "is proved to converge." What have they told you, and what have they not?

> [!example]- Solution
> **(a)** Linear: $e_k=\gamma^k e_0$, so solve $\gamma^k\cdot\tfrac12<10^{-12}$:
> $$k>\frac{\ln(2\times10^{-12})}{\ln\gamma}$$
> - $\gamma=0.5$: $k>\dfrac{-26.94}{-0.6931}=38.9$, so $\boxed{39}$ steps.
> - $\gamma=0.9$: $k>\dfrac{-26.94}{-0.1054}=255.6$, so $\boxed{256}$ steps.
>
> **A ratio change from 0.5 to 0.9 costs a factor of 6.5 in work** — and 0.9 is not an unusual ratio. For steepest descent on a problem with condition number $\kappa=40$, ch. 05's rate $\left(\frac{\kappa-1}{\kappa+1}\right)^2\approx0.90$ is *exactly* this case.
>
> **(b)** Quadratic: $e_k=e_0^{2^k}=2^{-2^k}$.
> $$\tfrac12,\ \tfrac14,\ 6.25\times10^{-2},\ 3.91\times10^{-3},\ 1.53\times10^{-5},\ 2.33\times10^{-10},\ 5.42\times10^{-20}$$
> so $\boxed{6}$ steps — and the 6th overshoots the target by eight orders of magnitude. **The last step of a quadratically convergent method does more than all the previous ones combined.**
>
> **(c)** They have told you the algorithm has **global convergence**: from a suitable start the iterates approach a stationary point. **They have told you nothing about the rate**, and therefore nothing about whether it is usable. From (a), "converges" spans everything from 6 iterations to more than the age of the universe.
>
> **Three further things the claim does not include, all of which matter more in practice:**
> 1. **Cost per iteration.** Newton is quadratic in iteration count and $O(n^3)$ per iteration. **For $n=10^6$, six Newton steps are unaffordable and ten thousand gradient steps are routine.** The right comparison is *total arithmetic*, not iterations.
> 2. **Converges to what.** For a non-convex $f$, to *a* stationary point — possibly a saddle, and almost never certifiably global.
> 3. **Under what hypotheses.** Rate theorems are typically **local** (they assume you are already near $\mathbf x^*$) and stated **for quadratics**. Neither assumption holds where the work actually happens.

---

> [!question] Exercise 5 — existence *(hard)*
> **(a)** For each pair, say whether Weierstrass guarantees a global minimizer, and whether one exists:
> (i) $f(x)=e^{-x}$, $\Omega=[0,\infty)$; (ii) $f(x)=x$, $\Omega=(0,1)$; (iii) $f(x)=x^2$, $\Omega=\mathbb R$; (iv) $f(x)=\frac{1}{1+x^2}$, $\Omega=\mathbb R$.
> **(b)** Case (iii) has a minimizer although Weierstrass does not apply. State a condition on $f$ that rescues the conclusion on an unbounded $\Omega$, and prove it.
> **(c)** Use (b) to explain, in optimization terms, why adding $\lambda\lVert\boldsymbol\theta\rVert^2$ to a loss is sometimes doing something *before* it does anything statistical.

> [!example]- Solution
> **(a)**
>
> | | $\Omega$ closed? | bounded? | $f$ cts? | Weierstrass? | Minimizer exists? |
> |---|---|---|---|---|---|
> | (i) $e^{-x}$ on $[0,\infty)$ | ✔ | ✘ | ✔ | **No** | **No** — $\inf f=0$, approached as $x\to\infty$, never attained |
> | (ii) $x$ on $(0,1)$ | ✘ | ✔ | ✔ | **No** | **No** — $\inf f=0\notin\Omega$ |
> | (iii) $x^2$ on $\mathbb R$ | ✔ | ✘ | ✔ | **No** | **Yes** — $x^*=0$ |
> | (iv) $\frac{1}{1+x^2}$ on $\mathbb R$ | ✔ | ✘ | ✔ | **No** | **No** — $\inf f=0$ as $\lvert x\rvert\to\infty$; *(the global **maximizer** $x=0$ does exist)* |
>
> **(iii) and (iv) are the instructive pair.** They differ in exactly one respect: **$x^2$ grows at infinity and $\frac{1}{1+x^2}$ decays there.**
>
> **(b) Coercivity.** Call $f:\mathbb R^n\to\mathbb R$ **coercive** if
> $$f(\mathbf x)\to+\infty\quad\text{whenever}\quad\lVert\mathbf x\rVert\to\infty$$
>
> > **Claim.** *A continuous coercive $f$ attains a global minimum on any non-empty closed $\Omega\subseteq\mathbb R^n$.*
> >
> > **Proof.** Fix any $\mathbf x_0\in\Omega$ and set $c=f(\mathbf x_0)$. By coercivity there is $R>0$ with $f(\mathbf x)>c$ whenever $\lVert\mathbf x\rVert>R$. **So no point outside the ball of radius $R$ can be a minimizer**, and
> > $$\inf_{\Omega}f=\inf_{\Omega\cap\bar B_R}f$$
> > The set $\Omega\cap\bar B_R$ is closed (intersection of closed sets), bounded, and non-empty (it contains $\mathbf x_0$) — **hence compact.** Weierstrass applies to it, giving $\mathbf x^*$ attaining the infimum over $\Omega\cap\bar B_R$, which by the display equals the infimum over all of $\Omega$. $\blacksquare$
>
> **The move is the one worth remembering: coercivity lets you replace an unbounded feasible set with a compact sublevel set, for free.** Checking: $x^2$ is coercive ✔; $\frac{1}{1+x^2}$ is not ✘; $e^{-x}$ on $[0,\infty)$ is not ✘.
>
> **(c)** Take a loss $L(\boldsymbol\theta)$ that is bounded below but **not coercive** — the log-likelihood of a separable logistic regression is the standard case, where pushing $\lVert\boldsymbol\theta\rVert\to\infty$ in the separating direction drives the loss down towards its infimum without ever reaching it. **There is no minimizer.** An optimizer run on it does not fail loudly; it produces weights that grow without bound and stops when the gradient underflows.
>
> Now add a ridge penalty:
> $$L_\lambda(\boldsymbol\theta)=L(\boldsymbol\theta)+\lambda\lVert\boldsymbol\theta\rVert^2,\qquad\lambda>0$$
> Since $L$ is bounded below by some $m$, we get $L_\lambda(\boldsymbol\theta)\ge m+\lambda\lVert\boldsymbol\theta\rVert^2\to\infty$. **$L_\lambda$ is coercive, so by (b) a global minimizer exists.**
>
> **So the first thing regularisation does is make the problem well-posed.** The bias–variance story usually told about it is real but comes second; **before it improves the estimator it creates one.** (For a convex $L$ the penalty also makes $L_\lambda$ *strictly* convex, which upgrades existence to **uniqueness** — see ch. 02.) This is also why ridge regression is defined for $p>n$ while OLS is not: $X^{\mathsf T}X$ is singular, but $X^{\mathsf T}X+\lambda I$ is not.

---

## 📝 Summary

- **The standard problem is $\min f(\mathbf x)$ subject to $\mathbf x\in\Omega$.** Maximisation, $\ge$ constraints and equalities all convert into it at no cost, **but conventions differ between books and mixing them flips the sign of every multiplier in ch. 11.**
- **Minimizers come in four flavours** — global/local $\times$ strict/non-strict. The **minimizer** is the point, the **minimum** is the value, and **every algorithm in chapters 04–08 finds local minimizers only.**
- **Weierstrass** guarantees a minimizer for continuous $f$ on a **compact** $\Omega$. **Coercivity ($f\to\infty$ as $\lVert\mathbf x\rVert\to\infty$) rescues the conclusion on unbounded sets**, and is why a ridge penalty makes an ill-posed problem well-posed.
- **The tractability line is convexity, not linearity.** Integer *linear* programming is NP-hard; convex quadratic programming is easy. Convexity is precisely the property that makes local information globally reliable.
- **Every algorithm has the form $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf d_k$** and differs only in how much curvature it buys. Ask three separate questions: is it a descent step, does it converge globally, and how fast locally.
- **Stopping criteria must be relative**, because scaling $f$ scales every gradient without changing the problem. **A small gradient does not mean a small error.**
- **Order of convergence $p$**: $\lim\lVert e_{k+1}\rVert/\lVert e_k\rVert^p$ finite and non-zero. **Linear ($p=1$, ratio $\gamma<1$) gives a fixed number of digits per step; quadratic ($p=2$) doubles the digit count each step.**
- **From error $\tfrac12$ to $10^{-12}$: 256 steps at $\gamma=0.9$, 39 at $\gamma=0.5$, 6 with quadratic convergence.** **The ratio matters as much as the order**, and for steepest descent that ratio is set by the condition number.

---

## ⚠️ Important Notes

> [!warning] The six confusions worth pre-empting
> 1. **Minimizer vs minimum.** Point vs value. An answer to "find the minimum" is a number; to "find the minimizer" is a vector.
> 2. **$\arg\max f=\arg\min(-f)$, but $\max f=-\min(-f)$.** The *point* is unchanged, the *value* flips sign. Forgetting the second is a reliable way to report the wrong number.
> 3. **"Converges" $\ne$ "works."** See Exercise 4(c).
> 4. **Iteration count $\ne$ cost.** Newton needs fewer iterations *and* is unusable at $n=10^6$. Always compare total arithmetic.
> 5. **Rate theorems are local and usually stated for quadratics.** Quoting $\left(\frac{\kappa-1}{\kappa+1}\right)^2$ for a general $f$ far from the optimum is an abuse of the theorem.
> 6. **Non-uniqueness is normal and is not an error.** When the minimizer is not unique, *which* one an algorithm returns is a property of the algorithm, not of the problem — and in machine learning that implicit choice has a name: implicit regularisation.

> [!tip] The reading that makes the rest of the subject cohere
> **Everything after this chapter is one of two things:**
> - **A condition** telling you whether a point could be optimal (ch. 03, 11) or certifying that it is (ch. 02, 10, 12);
> - **An algorithm** choosing $\mathbf d_k$ and $\alpha_k$ (ch. 04–08, 09, 12).
>
> **When a new method appears, ask only: what is its search direction, what is its step rule, what does it assume, and what is its order of convergence.** Four answers describe any method in this book.

> [!note] Where this chapter reappears
> - **[[Calculus/contents/08 - Multivariable Optimization|Calculus ch. 08]]** is the prerequisite: gradients, Hessians and the single-constraint Lagrange condition. **This subject is that chapter made general and made algorithmic.**
> - **[[Mathematical Statistics/contents/00-Index|Math Stats]]** — MLE is $\min-\ell(\theta)$; the existence discussion of §3 is why unbounded likelihoods are a real problem, not a curiosity.
> - **[[Machine Learning/contents/00-Index|Machine Learning]]** — the size discussion of §4 is why deep learning uses ch. 05's method and none of ch. 06–07's.
> - **[[Econometrics/contents/00-Index|Econometrics]]** — every estimator beyond OLS (GMM, MLE, NLS) is an iterative optimization of exactly this shape.

---

> [!warning] Gaps in the source material
> **This chapter is drawn from two books whose extraction quality is opposite**, and the split is deliberate: **all prose and structure from Chong & Żak §§6.1 and 8.3; all displayed statements checked against Luenberger & Ye ch. 1, which extracts cleanly.**
>
> **Chong & Żak's OCR damage in the source passages:**
> - The **definition of order of convergence** (§8.3, p. 150) extracts with the numerator and denominator of the limit on separate lines and the limit's subscript detached: `0 < hm VTM ^ < °°- k^oo \\xW -x*\\P` — **the fraction bar, the superscript $(k+1)$ and the norm bars are all lost.** The statement above was reconstructed and its four worked examples recomputed.
> - `x^`, `x(fc)`, `χ(*+1>`, `a5*` all mean $\mathbf x^{(k)}$ or $\mathbf x^*$; `\\·\\` is $\lVert\cdot\rVert$; `G` is $\in$; `φ` is $\ne$; `—►` is $\to$. **The Hessian display in §6.2 (p. 83) collapses entirely** — `d2f`, `dx„dx\`, `Sw` with no rows, brackets or order.
> - **Every figure is an image and all are lost**, including Figure 6.1 (the picture distinguishing strict global, strict local and non-strict local minimizers) — **which is the entire content of §2 above**, and which I have had to give as a table and a worked polynomial instead.
>
> **Luenberger & Ye extracts cleanly**, with one recurring artefact: in displayed problem statements **the subscript on a constraint function prints as $j$ while the running index prints as $i$** — `h j(x) = 0, i = 1, 2, ..., m` and `g j(x) ≤ 0, j = 1, 2, p` on p. 4, and `x j, i = 1, 2` on p. 2. **The surrounding prose has it right** ("$f$, $h_i$, $i=1,\dots,m$, and $g_j$, $j=1,\dots,p$"), so this is a font/extraction artefact, not an error in the book. Note also the dropped ellipsis in `j = 1, 2, p`.
>
> **Verification performed.** Every number in this note was computed independently:
> - **Exercise 1**: both the original and the standard form solved with `scipy.optimize.linprog` — **both give $\mathbf x^*=(14,0,-4)$ and optimal value 38**, and the recovered $x_3=x_3^+-x_3^-=-4$ matches.
> - **Exercise 2**: $f'=12x(x-2)(x+1)$ factored symbolically; all values of $f$, $f'$ and $f''$ at $-2,-1,0,1,2$ confirmed exactly.
> - **Exercises 3–4**: every order-of-convergence limit evaluated symbolically, and the iteration counts (39, 256, 8, 6) computed by direct simulation of the recurrences.
> - **The quadratic error sequence** $\tfrac12,\tfrac14,6.25\times10^{-2},3.91\times10^{-3},1.53\times10^{-5},2.33\times10^{-10},5.42\times10^{-20}$ verified term by term.
>
> **No error was found in either book's mathematics in the sections used.**
>
> **Scope and additions.**
> - **§3 (existence) is expanded well beyond both books.** Chong & Żak **do** state Weierstrass (Theorem 4.2, in the geometry review) but give it one sentence, cite the proof to two other books, and never return to it; Luenberger & Ye mention compactness only in passing. **The three-way failure table, the coercivity theorem and its proof in Exercise 5(b) are my own**, as is the connection to unbounded likelihoods and to regularisation. It is included because **"does a solution exist" is the first question and neither book treats it as one.**
> - **§4's taxonomy table is my own synthesis.** Both books organise by *chapter* (linear / unconstrained / constrained) rather than by difficulty, so the observation that **convexity and not linearity is the tractability boundary** — obvious in a modern treatment, and the single most useful thing in the chapter — has to be assembled from material spread across both.
> - **The stopping-criterion discussion in §5 is my own addition.** Chong & Żak give stopping rules only inside individual algorithms and never note that absolute criteria are scale-dependent.
> - **The iteration-count table in §6 is my own**, built to make the point that the *ratio* matters as much as the *order* — a point both books make implicitly through their convergence theorems and neither makes explicitly.

#optimization #minimizer #standard-form #weierstrass #coercivity #convergence-rate #iterative-algorithms
