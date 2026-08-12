---
subject: Calculus
chapter: 03
tags: [ds, calculus, optimization, extreme-values, mean-value-theorem, lhopital, newtons-method, concavity]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 4 (pp. 279–370)"
---

# Applications of Differentiation

> [!abstract] What this chapter is for
> **The derivative is now a tool rather than a definition, and this chapter is what it is for.** Four things, in descending order of importance for a data-science reader:
>
> | § | Topic | Why it matters downstream |
> |---|---|---|
> | **6** | **Optimization** | **Every fitted model is a minimisation** — [[Optimization/contents/00-Index\|Optimization]], [[Machine Learning/contents/00-Index\|ML]], MLE |
> | **7** | **Newton's method** | The prototype iterative solver; **quadratic convergence** |
> | **4** | **l'Hôpital's rule** | The only systematic tool for indeterminate forms; proves $\ln x\ll x^p\ll e^x$ |
> | **1–3, 5** | Extreme values, MVT, curve shape | The theory that makes the first two legitimate |
>
> **The logical spine is short:**
>
> $$\underbrace{\text{EVT}}_{\text{a max exists}}\ \longrightarrow\ \underbrace{\text{Fermat}}_{\text{it is at a critical point}}\ \longrightarrow\ \underbrace{\text{Closed Interval Method}}_{\text{so check a finite list}}$$
>
> **Everything else — the Mean Value Theorem, the increasing/decreasing tests, concavity — exists to turn *local* derivative information into *global* statements about the function.** That translation is the chapter's real subject, and it is what [[06 - Sequences, Series and Taylor Approximation|Taylor's theorem]] later makes quantitative.

---

## 📘 Main Knowledge

### 1. Extreme values

> [!important] Definitions
> $f$ has an **absolute (global) maximum** at $c$ if $f(c)\ge f(x)$ for **all** $x$ in the domain; a **local (relative) maximum** if $f(c)\ge f(x)$ for all $x$ **near** $c$. Similarly for minima.

> [!important] The Extreme Value Theorem
> **If $f$ is continuous on a *closed, bounded* interval $[a,b]$, then $f$ attains an absolute maximum and an absolute minimum on $[a,b]$.**

> [!warning] Both hypotheses are load-bearing
> | Drop | Example | What goes wrong |
> |---|---|---|
> | **closed** | $f(x)=x$ on $(0,1)$ | never attains a max |
> | **bounded** | $f(x)=x$ on $[0,\infty)$ | no max |
> | **continuous** | $f(x)=1/x$ on $[-1,1]$ | unbounded |
>
> **This is an existence theorem and produces nothing constructive** — it only tells you the search is not futile. **In optimisation it is the reason "does a minimum exist?" is a separate question from "where is it?"**, and unbounded loss surfaces genuinely have no minimum.

> [!important] Fermat's Theorem
> **If $f$ has a local extremum at $c$ and $f'(c)$ exists, then $f'(c)=0$.**
>
> A **critical number** is a $c$ where $f'(c)=0$ **or $f'(c)$ does not exist.**

> [!warning] The converse is false, and this is the trap
> **$f'(c)=0$ does not make $c$ an extremum.** $f(x)=x^3$ has $f'(0)=0$ and no extremum at all — an inflection with a horizontal tangent.
>
> **And "or $f'(c)$ does not exist" is not decoration:** $f(x)=|x|$ has a minimum at 0 where the derivative fails to exist. **A search that only solves $f'=0$ will miss it.**
>
> **In several variables the same trap becomes the saddle point** ([[08 - Multivariable Optimization|ch. 08]]), and there it is far harder to spot.

> [!important] The Closed Interval Method
> To find the absolute extrema of a continuous $f$ on $[a,b]$:
> 1. evaluate $f$ at every **critical number** in $(a,b)$;
> 2. evaluate $f$ at the **endpoints** $a$ and $b$;
> 3. **the largest and smallest of these values are the answers.**
>
> **The EVT guarantees the list is not empty; Fermat guarantees it is complete.**

---

### 2. The Mean Value Theorem

> [!important] Rolle's Theorem and the MVT
> **Rolle.** If $f$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a)=f(b)$, then $f'(c)=0$ for some $c\in(a,b)$.
>
> **MVT.** Under the first two hypotheses,
> $$\boxed{\ f'(c)=\frac{f(b)-f(a)}{b-a}\quad\text{for some }c\in(a,b)\ }$$
> — **at some interior point the instantaneous rate equals the average rate.**

> [!tip] The MVT is the bridge from local to global
> **On its own it looks like a curiosity.** Its importance is that it converts statements about $f'$ (local) into statements about $f$ (global), and **every such translation in the chapter is a corollary:**
>
> | Corollary | Proof |
> |---|---|
> | $f'=0$ on an interval $\Rightarrow f$ constant | $f(x)-f(y)=f'(c)(x-y)=0$ |
> | $f'=g'\Rightarrow f=g+C$ | apply the above to $f-g$ |
> | $f'>0\Rightarrow f$ increasing | $f(x)-f(y)=f'(c)(x-y)>0$ |
>
> **The second is what makes "$+C$" the *complete* answer to an antiderivative** — without the MVT you could not rule out some other function with the same derivative. **[[04 - Integrals|Ch. 04]] depends on it entirely.**

---

### 3. What derivatives say about shape

> [!important] The tests
> | Feature | Test |
> |---|---|
> | **Increasing / decreasing** | $f'>0$ / $f'<0$ on the interval |
> | **Local max at $c$** (First Derivative Test) | $f'$ changes $+\to-$ at $c$ |
> | **Local min at $c$** | $f'$ changes $-\to+$ at $c$ |
> | **Neither** | $f'$ does not change sign |
> | **Concave up / down** | $f''>0$ / $f''<0$ |
> | **Inflection point** | **$f''$ changes sign** |
> | **Second Derivative Test** | $f'(c)=0$ and $f''(c)>0\Rightarrow$ local min; $f''(c)<0\Rightarrow$ local max |

> [!warning] The Second Derivative Test is silent when $f''(c)=0$
> **$f''(c)=0$ tells you nothing.** All three of $x^4$ (min), $-x^4$ (max) and $x^3$ (neither) have $f'(0)=f''(0)=0$.
>
> **Fall back on the First Derivative Test**, which is never inconclusive — it just requires checking the sign of $f'$ on both sides.
>
> **Also: $f''(c)=0$ does not make $c$ an inflection point.** $x^4$ has $f''(0)=0$ and no inflection there, because $f''$ does not *change sign*. **Sign change is the requirement, not vanishing.**

> [!tip] Concavity is what makes optimisation well behaved
> **A function concave up everywhere has at most one local minimum, and it is global.** That is the entire reason **convexity** is the central hypothesis of [[Optimization/contents/00-Index|Optimization]] and of every guarantee in convex machine learning.
>
> **Without it, a local minimum is just a local minimum** — which is why gradient descent on a neural network comes with no guarantee, and why the second-derivative information ($f''$, and the Hessian in [[08 - Multivariable Optimization|ch. 08]]) is worth computing.

---

### 4. l'Hôpital's rule

> [!important] l'Hôpital's Rule
> If $\lim\frac{f}{g}$ is of the form $\dfrac00$ or $\dfrac{\pm\infty}{\pm\infty}$, and $g'\ne0$ near $a$, then
> $$\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}$$
> **provided the right-hand limit exists** (or is $\pm\infty$). **The same holds for $x\to\pm\infty$ and for one-sided limits.**

> [!warning] Check the form first — every time
> **Applying the rule to a non-indeterminate form gives a confidently wrong answer.**
> $$\lim_{x\to0}\frac{x+1}{x+2}=\frac12\qquad\text{but}\qquad \lim_{x\to0}\frac{1}{1}=1$$
> **The form was $\tfrac12$, not $\tfrac00$, so the rule never applied.**
>
> **Two further cautions.** It is $\dfrac{f'}{g'}$, **not** the quotient rule. And **it can loop forever** — $\lim_{x\to\infty}\frac{\sqrt{x^2+1}}{x}$ returns to itself after two applications; the answer (1) comes from dividing by $x$ instead.

> [!important] The seven indeterminate forms, and how to reduce them
> | Form | Fix |
> |---|---|
> | $\tfrac00$, $\tfrac\infty\infty$ | **l'Hôpital directly** |
> | $0\cdot\infty$ | rewrite as $\dfrac{f}{1/g}$ |
> | $\infty-\infty$ | common denominator, or **rationalise** |
> | $0^0$, $1^\infty$, $\infty^0$ | **take $\ln$**, find the limit of $\ln y$, then exponentiate |

> [!example] The results worth memorising *(all verified)*
> $$\lim_{x\to\infty}\frac{\ln x}{x}=0,\qquad \lim_{x\to\infty}\frac{x^2}{e^x}=0,\qquad \lim_{x\to0^+}x\ln x=0,\qquad \lim_{x\to0^+}x^x=1$$
> $$\lim_{x\to\infty}\left(1+\frac1x\right)^x=e,\qquad \lim_{x\to0}\frac{e^x-1-x}{x^2}=\frac12$$
>
> **The first two prove the growth hierarchy $\ln x\ll x^p\ll e^x$** asserted in [[01 - Functions, Limits and Continuity|ch. 01]] — repeated differentiation grinds any power down to a constant while $e^x$ is unchanged.
>
> **The last is the second-order Taylor coefficient of $e^x$ appearing early** ([[06 - Sequences, Series and Taylor Approximation|ch. 06]]).

---

### 5. Curve sketching

> [!important] The checklist
> **Domain · intercepts · symmetry · asymptotes · $f'$ (intervals of increase, local extrema) · $f''$ (concavity, inflections) · sketch.**

**Worked through for $f(x)=x^3-3x^2+1$** *(all verified)*:

$$f'=3x^2-6x=3x(x-2)\ \Rightarrow\ \text{critical numbers }0,2$$
$$f''=6x-6\ \Rightarrow\ \text{inflection at }x=1$$

| $x$ | $0$ | $1$ | $2$ |
|---|---|---|---|
| $f(x)$ | $1$ | $-1$ | $-3$ |
| feature | **local max** ($f''<0$) | **inflection** | **local min** ($f''>0$) |

**Increasing on $(-\infty,0)$ and $(2,\infty)$; decreasing on $(0,2)$; concave down then up.**

> [!tip] Why this section is worth less than it looks
> **Software draws better graphs than any of this.** What survives is the *reasoning*: reading off where a function increases, where it turns, and how it curves, **from the derivatives alone** — which is exactly what you must do in [[08 - Multivariable Optimization|several variables]], where you cannot draw the graph at all.

---

### 6. Optimization problems

> [!important] The procedure
> 1. **Name the quantity to be optimised** and write it as a formula.
> 2. **Use the constraint to eliminate variables** until one is left.
> 3. **State the domain** — this is where the constraint's physical limits go, and it is the most-skipped step.
> 4. Find critical numbers; apply the **Closed Interval Method** or a derivative test.
> 5. **Answer the question that was asked** (often a dimension, not the optimum value).

> [!example] The open box
> A $12\times12$ square of card; cut squares of side $x$ from the corners and fold up. Then
> $$V(x)=x(12-2x)^2=4x^3-48x^2+144x,\qquad 0\le x\le6$$
> $$V'(x)=12x^2-96x+144=12(x-2)(x-6)$$
> Critical numbers $x=2$ and $x=6$; **but $x=6$ is an endpoint giving $V=0$.** Comparing $V(0)=0$, $V(2)=128$, $V(6)=0$:
> $$\boxed{x=2,\quad V_{\max}=128\ \text{cubic units}}$$
> *(Verified.)*
>
> **The domain $[0,6]$ did real work** — it made the Closed Interval Method available and disposed of the spurious critical number.

> [!example] The fence
> $2400\,$ft of fencing, a rectangular field bounded on one side by a river (no fence needed there). Maximise the area.
>
> With $x$ the two perpendicular sides: $2x+y=2400$, so $A=x(2400-2x)$ and $A'=2400-4x=0$ gives
> $$\boxed{x=600,\quad y=1200,\quad A_{\max}=720{,}000\ \text{ft}^2}$$
> *(Verified.)*
>
> **Note $y=2x$** — the optimal rectangle is twice as long as it is deep. **With fencing on all four sides the answer would be a square**; the asymmetry comes entirely from the free side, which is the kind of structural insight the calculus gives and a numerical search does not.

---

### 7. Newton's method

> [!important] The method
> To solve $f(x)=0$: **replace $f$ by its linear approximation and solve that instead.** From $x_n$,
> $$0\approx f(x_n)+f'(x_n)(x-x_n)\quad\Longrightarrow\quad \boxed{\ x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}\ }$$

> [!example] $x^3-x-1=0$ from $x_0=1.5$ *(all iterates verified)*
> | $n$ | $x_n$ | correct digits |
> |---|---|---|
> | 1 | $1.3478260869565$ | 2 |
> | 2 | $1.3252003989509$ | 3 |
> | 3 | $1.3247181739991$ | 6 |
> | 4 | $1.3247179572448$ | 12 |
> | 5 | $1.3247179572447$ | (converged) |
>
> **True root: $1.32471795724474603$.**
>
> **Count the correct digits: 2, 3, 6, 12 — they roughly double each step.** That is **quadratic convergence**, and it is what makes Newton's method the default.
>
> **Compare bisection on the same problem** ([[01 - Functions, Limits and Continuity|ch. 01]], Exercise 3): four steps got one decimal place. **Newton got twelve.**

> [!warning] Newton's method fails, and it fails without warning
> | Failure | Cause |
> |---|---|
> | $f'(x_n)=0$ | division by zero — the tangent is horizontal |
> | Divergence | a bad starting point sends iterates away |
> | Cycling | $x_{n+1}\to x_n\to x_{n+1}$ forever |
> | Wrong root | converges, to a root you did not want |
>
> **The trade-off with bisection is stark and worth naming:**
> | | Bisection | Newton |
> |---|---|---|
> | **Needs** | a sign change | $f'$, and a good start |
> | **Guarantee** | always converges | none |
> | **Speed** | 1 bit per step | **doubles the digits** |
>
> **In practice: bracket with bisection, then polish with Newton.** That hybrid is what production root-finders do, and **the same idea reappears in optimisation** — a safeguarded line search wrapping a Newton step.

---

### 8. Antiderivatives

> [!important] Definition and the key corollary
> $F$ is an **antiderivative** of $f$ if $F'=f$. **By the MVT, any two antiderivatives differ by a constant**, so the general antiderivative is
> $$F(x)+C$$
>
> | $f$ | antiderivative | | $f$ | antiderivative |
> |---|---|---|---|---|
> | $x^n$ ($n\ne-1$) | $\dfrac{x^{n+1}}{n+1}$ | | $\sin x$ | $-\cos x$ |
> | $\dfrac1x$ | $\ln\lvert x\rvert$ | | $\cos x$ | $\sin x$ |
> | $e^x$ | $e^x$ | | $\dfrac1{1+x^2}$ | $\arctan x$ |

> [!warning] $\int\frac1x\,dx=\ln|x|+C$ — the absolute value matters
> **$n=-1$ is the one case the power rule cannot do**, and the antiderivative is the logarithm — **with absolute values**, since $1/x$ is defined for negative $x$ and $\ln x$ is not.
>
> **And "$+C$" is not a formality:** the MVT is what guarantees it captures *every* antiderivative. **It becomes essential in [[04 - Integrals|ch. 04]]** — and forgetting it in a differential equation loses the initial condition, which is the whole solution.

---

## ✏️ Exercises

> [!question] Exercise 1 — extreme values *(warm-up)*
> (i) Find the absolute extrema of $f(x)=x^3-3x^2+1$ on $[-1,3]$.
> (ii) Find the critical numbers of $g(x)=|x^2-4|$.
> (iii) Show $h(x)=x^3$ has a critical number that is not an extremum.
> (iv) Does $f(x)=1/x$ attain a maximum on $(0,1]$? On $[1,2]$?

> [!example]- Solution
> **(i)** $f'=3x(x-2)$, so the critical numbers are $0$ and $2$, both in $[-1,3]$. Evaluate at critical numbers **and endpoints**:
> $$f(-1)=-3,\quad f(0)=1,\quad f(2)=-3,\quad f(3)=1$$
> *(Verified.)* **Absolute max $=1$ (attained twice, at $x=0$ and $x=3$); absolute min $=-3$ (attained twice, at $x=-1$ and $x=2$).**
>
> **Extrema need not be unique, and endpoints compete with critical points** — skipping either would have given a wrong answer here.
>
> **(ii)** $g(x)=|x^2-4|$ is not differentiable where $x^2-4=0$, i.e. $x=\pm2$ — **corners**. Elsewhere $g'=\pm2x$, vanishing at $x=0$.
> $$\text{critical numbers: }\boxed{-2,\ 0,\ 2}$$
> **$x=\pm2$ are minima (value 0) and $x=0$ is a local max (value 4)** — and **the two minima would be invisible to a search that only solved $g'=0$.**
>
> **(iii)** $h'=3x^2=0$ at $x=0$, so 0 is a critical number. But $h$ is increasing on both sides ($h'>0$ for $x\ne0$), so **it is neither a max nor a min** — the tangent is horizontal at an inflection.
>
> **(iv)** On $(0,1]$: **no.** $f\to\infty$ as $x\to0^+$, so there is no maximum. **The EVT does not apply — the interval is not closed.**
> On $[1,2]$: **yes**, max $f(1)=1$ and min $f(2)=\tfrac12$. **Here $f$ is continuous on a closed bounded interval, so the EVT applies** and both are attained at endpoints.

> [!question] Exercise 2 — the Mean Value Theorem
> (i) Verify the MVT for $f(x)=x^3$ on $[0,3]$ and find all valid $c$.
> (ii) Show that if $f'(x)=0$ for all $x$ in an interval, then $f$ is constant there.
> (iii) A car travels 180 km in 2 hours. Show that at some instant its speed was exactly 90 km/h.
> (iv) Why does the MVT fail for $f(x)=|x|$ on $[-1,1]$?

> [!example]- Solution
> **(i)** $f$ is a polynomial, so continuous and differentiable everywhere. The average rate is
> $$\frac{f(3)-f(0)}{3-0}=\frac{27}{3}=9$$
> Solving $f'(c)=3c^2=9$ gives $c=\pm\sqrt3$, and **only $c=\sqrt3\approx1.732$ lies in $(0,3)$.** *(Verified.)*
>
> **(ii)** For any $x<y$ in the interval, apply the MVT on $[x,y]$:
> $$f(y)-f(x)=f'(c)(y-x)=0\cdot(y-x)=0$$
> so $f(y)=f(x)$ for every pair — **$f$ is constant.** $\blacksquare$
>
> **This one-line proof is what licenses "$+C$"**, and hence the whole notion of "the" antiderivative.
>
> **(iii)** Let $s(t)$ be the distance travelled. It is continuous and differentiable (position and speed are), and
> $$\frac{s(2)-s(0)}{2-0}=\frac{180}{2}=90$$
> **By the MVT, $s'(c)=90$ for some $c\in(0,2)$** — at some instant the speedometer read exactly 90.
>
> **This is how average-speed cameras work**, and it is a genuine legal application of the theorem: recording entry and exit times proves an instantaneous speed was attained, without observing it.
>
> **(iv)** The average rate is $\frac{|1|-|-1|}{2}=0$, so the MVT would need $f'(c)=0$ somewhere in $(-1,1)$. **But $f'(x)=\pm1$ everywhere it exists, and never 0.**
>
> **No contradiction: $f$ is not differentiable at $0$**, so the hypothesis fails. **The MVT requires differentiability at *every* interior point, and one exception is enough to destroy it.**

> [!question] Exercise 3 — l'Hôpital's rule
> Evaluate, **first stating the indeterminate form**.
> (i) $\displaystyle\lim_{x\to0}\frac{e^x-1-x}{x^2}$
> (ii) $\displaystyle\lim_{x\to\infty}\frac{\ln x}{x}$ and $\displaystyle\lim_{x\to\infty}\frac{x^2}{e^x}$
> (iii) $\displaystyle\lim_{x\to0^+}x\ln x$
> (iv) $\displaystyle\lim_{x\to\infty}\left(1+\frac1x\right)^x$
> (v) $\displaystyle\lim_{x\to0}\frac{x+1}{x+2}$ — **and what happens if you apply the rule anyway.**

> [!example]- Solution
> **(i) Form $\tfrac00$.** Applying twice:
> $$\lim\frac{e^x-1-x}{x^2}=\lim\frac{e^x-1}{2x}\ (\text{still }\tfrac00)=\lim\frac{e^x}{2}=\boxed{\tfrac12}$$
> *(Verified.)* **Check the form again before each reapplication** — the second step was legal only because $e^x-1\to0$ too.
>
> **(ii) Both $\tfrac\infty\infty$.**
> $$\lim\frac{\ln x}{x}=\lim\frac{1/x}{1}=\boxed{0},\qquad \lim\frac{x^2}{e^x}=\lim\frac{2x}{e^x}=\lim\frac{2}{e^x}=\boxed{0}$$
> *(Both verified.)*
>
> **This proves the growth hierarchy.** Differentiating grinds $x^2$ down to a constant in two steps while $e^x$ is untouched — **so $e^x$ beats every polynomial, and $\ln x$ loses to every positive power.** $\boxed{\ln x\ll x^p\ll e^x}$
>
> **(iii) Form $0\cdot\infty$** — not directly usable. Rewrite as a quotient:
> $$\lim_{x\to0^+}x\ln x=\lim_{x\to0^+}\frac{\ln x}{1/x}=\lim_{x\to0^+}\frac{1/x}{-1/x^2}=\lim_{x\to0^+}(-x)=\boxed{0}$$
> *(Verified.)*
>
> **The choice of which factor to invert matters.** Writing it as $\frac{x}{1/\ln x}$ instead produces a worse expression — **put the factor whose derivative simplifies on top.**
>
> **(iv) Form $1^\infty$.** Take logarithms:
> $$\ln y=x\ln\left(1+\tfrac1x\right)=\frac{\ln(1+1/x)}{1/x}\quad(\text{now }\tfrac00)$$
> $$\longrightarrow\ \frac{\frac{1}{1+1/x}\cdot(-1/x^2)}{-1/x^2}=\frac1{1+1/x}\longrightarrow1$$
> **So $\ln y\to1$ and $y\to\boxed{e}$.** *(Verified.)*
>
> **This is a definition of $e$**, and it is why continuous compounding gives $e^r$.
>
> **(v) Not indeterminate.** Direct substitution gives $\boxed{\tfrac12}$ immediately.
>
> **Applying l'Hôpital anyway gives $\frac11=1$ — wrong.**
>
> > [!warning] The rule is conditional, and the condition is the whole safeguard
> > **l'Hôpital's rule is not "differentiate top and bottom to simplify".** It is a theorem with a hypothesis, and violating the hypothesis produces a plausible-looking wrong number with no warning sign.
> >
> > **Always write the form down before applying it — and again before reapplying it.**

> [!question] Exercise 4 — optimization
> (i) A rectangular field is bounded on one side by a river and fenced on the other three with 2400 ft of fencing. Maximise the area.
> (ii) An open box is made by cutting squares of side $x$ from a $12\times12$ card and folding up. Maximise the volume.
> (iii) Find the point on $y=x^2$ closest to $(0,3)$.
> (iv) In (iii), why is minimising the *squared* distance legitimate?

> [!example]- Solution
> **(i)** With $x$ the two sides perpendicular to the river and $y$ the parallel side: $2x+y=2400$, so
> $$A(x)=x(2400-2x),\qquad 0\le x\le1200$$
> $$A'=2400-4x=0\ \Rightarrow\ x=600$$
> Comparing $A(0)=0$, $A(600)=720{,}000$, $A(1200)=0$:
> $$\boxed{600\times1200\ \text{ft},\quad A_{\max}=720{,}000\ \text{ft}^2}$$
> *(Verified.)* **The optimal shape is $y=2x$, not a square** — the free side changes the answer.
>
> **(ii)** $V(x)=x(12-2x)^2$ on $[0,6]$, with $V'=12(x-2)(x-6)$. Comparing $V(0)=0$, $V(2)=128$, $V(6)=0$:
> $$\boxed{x=2,\quad V_{\max}=128}$$
> *(Verified.)* **$x=6$ is a critical number that is an endpoint and a minimum** — a reminder to evaluate rather than assume.
>
> **(iii)** For a point $(x,x^2)$ on the parabola, minimise
> $$D^2=x^2+(x^2-3)^2=x^4-5x^2+9$$
> $$\frac{d(D^2)}{dx}=4x^3-10x=2x(2x^2-5)=0\ \Rightarrow\ x=0,\ \pm\sqrt{5/2}$$
> Values: $D^2(0)=9$ and $D^2(\pm\sqrt{5/2})=\tfrac{25}4-\tfrac{25}2+9=\tfrac{11}4$.
> $$\boxed{\left(\pm\sqrt{5/2},\ 5/2\right),\quad D=\sqrt{11}/2\approx1.658}$$
> **Two closest points, by symmetry** — and $x=0$ is a *local maximum* of the distance among the critical points, which is easy to mistake for the answer.
>
> **(iv)** $t\mapsto\sqrt t$ is **strictly increasing** on $[0,\infty)$, so $D$ and $D^2$ attain their minima at exactly the same $x$.
>
> **Minimising $D^2$ avoids differentiating a square root**, which would give a messier derivative with no benefit.
>
> > [!important] "Optimise a monotone transform instead" is a general and much-used move
> > **Maximising $\ln L$ instead of $L$** is the same trick — the log-likelihood has the same maximiser as the likelihood and turns products into sums ([[Mathematical Statistics/contents/05 - Point Estimation|Math Stats ch. 05]]).
> >
> > **Squared-error loss instead of absolute error** is a *different* choice, because squaring is not a monotone transform of the *loss surface* — it changes the answer, and that is why it targets the mean rather than the median ([[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]]).
> >
> > **The distinction is worth keeping straight:** transform the *objective* monotonically and the optimum is unchanged; transform the *residuals* and it is not.

> [!question] Exercise 5 — Newton's method *(hard)*
> (i) Derive the iteration from the linear approximation.
> (ii) Apply it to $x^3-x-1=0$ from $x_0=1.5$ for four steps, and count correct digits.
> (iii) Show that Newton's method for $f(x)=x^2-a$ gives $x_{n+1}=\tfrac12\left(x_n+\tfrac a{x_n}\right)$. Compute $\sqrt2$ from $x_0=1$.
> (iv) Give a function and a starting point for which the method **cycles forever**.

> [!example]- Solution
> **(i)** Near $x_n$, $f(x)\approx f(x_n)+f'(x_n)(x-x_n)$. **Setting the approximation to zero and solving:**
> $$0=f(x_n)+f'(x_n)(x-x_n)\ \Longrightarrow\ x=x_n-\frac{f(x_n)}{f'(x_n)}$$
> **Newton's method is "solve the linear approximation instead of the function"** — which is why it needs $f'$, and why it fails when $f'(x_n)=0$ (the linear approximation is then horizontal and has no root).
>
> **(ii)** With $f'=3x^2-1$:
> | $n$ | $x_n$ | correct digits |
> |---|---|---|
> | 1 | $1.34782608695652$ | 2 |
> | 2 | $1.32520039895091$ | 3 |
> | 3 | $1.32471817399905$ | 6 |
> | 4 | $1.32471795724479$ | 12 |
>
> **True root $1.32471795724474603$.** *(All iterates verified.)*
>
> **Digits: 2, 3, 6, 12 — doubling.** That is **quadratic convergence**: if $e_n$ is the error, $e_{n+1}\approx Ce_n^2$. **Each step squares the error.**
>
> **(iii)** With $f=x^2-a$ and $f'=2x$:
> $$x_{n+1}=x_n-\frac{x_n^2-a}{2x_n}=\frac{2x_n^2-x_n^2+a}{2x_n}=\boxed{\frac12\left(x_n+\frac a{x_n}\right)}$$
> From $x_0=1$ with $a=2$:
> $$1\to1.5\to1.41\overline{6}\to1.4142156\ldots\to1.41421356237469$$
> **against $\sqrt2=1.41421356237310$ — 12 correct digits in four steps.**
>
> **This is the Babylonian method, known two thousand years before calculus:** *average your guess with $a$ divided by your guess.* **Newton's method rediscovers it**, which is a good sign that the idea is natural rather than clever.
>
> **(iv)** Take $f(x)=x^3-2x+2$ with $x_0=0$:
> $$f(0)=2,\quad f'(0)=-2\ \Rightarrow\ x_1=0-\frac{2}{-2}=1$$
> $$f(1)=1,\quad f'(1)=1\ \Rightarrow\ x_2=1-\frac11=0$$
> **The iteration cycles $0\to1\to0\to1\to\cdots$ forever**, never approaching the real root near $-1.769$.
>
> > [!important] What the failure modes are really telling you
> > **Newton's method has no globalisation.** It trusts the linear approximation completely, and [[02 - Derivatives|ch. 02]] showed that approximation degrades like $h^2$ — **so a step that lands far away is a step into a region where the model was never valid.**
> >
> > **The standard fixes are all forms of not trusting it fully:** damping (take a fraction of the step), bracketing (keep a sign change and fall back to bisection), and line search (accept the step only if $|f|$ actually decreased).
> >
> > **Every one of these reappears in [[Optimization/contents/00-Index|Optimization]]**, where Newton's method on $f'=0$ is the second-order optimizer and needs exactly the same safeguards — trust regions, damped Newton, and backtracking line search.

---

## 📝 Summary

- **EVT $\to$ Fermat $\to$ Closed Interval Method** is the chapter's spine: a continuous function on a closed bounded interval **attains** its extrema; extrema occur at **critical numbers** ($f'=0$ *or $f'$ undefined*) or endpoints; so checking a finite list suffices.
- **All three EVT hypotheses matter**, and **$f'(c)=0$ does not imply an extremum** ($x^3$) while **an extremum can occur where $f'$ fails to exist** ($|x|$).
- **The MVT converts local information into global statements.** Its corollaries — $f'=0\Rightarrow f$ constant, $f'=g'\Rightarrow f=g+C$, $f'>0\Rightarrow f$ increasing — are what make antiderivatives and monotonicity tests legitimate.
- **$f'$ gives increase/decrease and local extrema; $f''$ gives concavity and inflections.** The **Second Derivative Test is inconclusive when $f''(c)=0$** — fall back on the First Derivative Test, which never is. **An inflection needs $f''$ to *change sign*, not merely vanish.**
- **Concavity is why convexity is central downstream:** a convex function's local minimum is global.
- **l'Hôpital's rule applies only to $\tfrac00$ and $\tfrac{\infty}{\infty}$ — check the form every time, including before reapplying.** The other five forms reduce to these by inverting a factor, combining fractions, or **taking logarithms**.
- **It proves the growth hierarchy $\ln x\ll x^p\ll e^x$**, and gives $\lim(1+1/x)^x=e$ and $\lim x^x=1$.
- **Optimization: name the objective, eliminate variables with the constraint, state the domain, then use the Closed Interval Method.** The domain is the most-skipped step and it does real work.
- **Minimising a monotone transform (e.g. $D^2$ instead of $D$, or $\ln L$ instead of $L$) leaves the optimum unchanged** — a standard and much-used simplification.
- $$\boxed{x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}}$$ **is "solve the linear approximation instead".** It converges **quadratically** — digits double each step (2, 3, 6, 12 on $x^3-x-1$) — but has **no guarantee**: it can divide by zero, diverge, cycle, or find the wrong root. **Bracket with bisection, polish with Newton.**
- **Any two antiderivatives differ by a constant (by the MVT), so "$+C$" is complete.** $\int\frac1x\,dx=\ln|x|+C$ is the one case the power rule cannot handle, **and the absolute value is required.**

---

## ⚠️ Important Notes

> [!warning] Critical numbers include the points where $f'$ does not exist
> $$c\text{ is critical}\iff f'(c)=0\ \textbf{ or }\ f'(c)\text{ does not exist}$$
> **Solving $f'=0$ alone misses corners.** $|x^2-4|$ has minima at $x=\pm2$ that no equation-solving will find (Exercise 1(ii)).
>
> **And endpoints are not critical numbers but must still be checked** — the Closed Interval Method has three sources of candidates, not one.

> [!warning] Check the form before every l'Hôpital application
> $$\lim_{x\to0}\frac{x+1}{x+2}=\frac12\qquad\text{but l'Hôpital "gives" }1$$
> **The rule is a conditional theorem, and violating its hypothesis returns a wrong number silently.**
>
> **Two further failure modes:** it is $\frac{f'}{g'}$ and **not** the quotient rule; and it can **loop forever** ($\frac{\sqrt{x^2+1}}{x}$ returns to itself), where the fix is ordinary algebra.

> [!warning] $f''(c)=0$ decides nothing
> | Function | $f'(0)$ | $f''(0)$ | at $0$ |
> |---|---|---|---|
> | $x^4$ | $0$ | $0$ | **minimum** |
> | $-x^4$ | $0$ | $0$ | **maximum** |
> | $x^3$ | $0$ | $0$ | **neither** |
>
> **Same second-derivative information, three different answers.** Use the First Derivative Test, which is never inconclusive.
>
> **The same applies to inflections: $f''(0)=0$ for $x^4$, and there is no inflection there** — sign change is the criterion.

> [!warning] State the domain in an optimisation problem
> **The physical constraint gives an interval, and the interval is what makes the Closed Interval Method available.** In the box problem, $0\le x\le6$ is what disposes of the critical number $x=6$; without the domain you would compare two critical points and no endpoints.
>
> **In several variables and in machine learning the same issue appears as *feasibility*:** a constrained optimum often sits on the boundary, where the gradient is **not** zero — which is exactly why [[08 - Multivariable Optimization|Lagrange multipliers]] and KKT conditions exist.

> [!warning] Newton's method is fast and unsafe
> | | Bisection | Newton |
> |---|---|---|
> | Guarantee | **always converges** | none |
> | Speed | 1 bit/step | **doubles the digits** |
> | Needs | a sign change | $f'$, and a good start |
>
> **It can divide by zero, diverge, cycle ($x^3-2x+2$ from $x_0=0$), or converge to a root you did not want.**
>
> **The reason is [[02 - Derivatives|ch. 02]]'s $h^2$ error law:** a long step leaves the region where the linear model is valid. **Damping, bracketing and line search are all ways of refusing to take that step**, and they carry over verbatim to second-order optimisation.

> [!warning] Existence and location are different questions
> **The EVT says a maximum exists; it does not say where.** The IVT says a root exists; it does not find one. **Fermat says extrema are among the critical points; it does not say which critical points are extrema.**
>
> **Keeping these separate matters in practice:** an optimisation problem can be well posed with no attainable optimum (an unbounded objective), or have an optimum that no first-order method will locate (on a boundary, or at a non-differentiable point). **"The algorithm converged" and "the answer exists and is what I wanted" are three claims, not one.**

> [!note] Cross-subject connections
> - [[01 - Functions, Limits and Continuity|Ch. 01]] — the EVT and IVT are the two existence theorems continuity buys; **l'Hôpital finally handles the indeterminate forms ch. 01 could only factor around**, and proves the growth ordering asserted there. **Newton is bisection's fast, unsafe cousin.**
> - [[02 - Derivatives|Ch. 02]] — **Newton's method is the linear approximation solved for its root**, and its failure modes are that approximation's $h^2$ error law.
> - [[04 - Integrals|Ch. 04]] — antiderivatives and "$+C$" (justified by the MVT here) are half of the Fundamental Theorem.
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — Taylor's theorem's remainder is proved with the MVT; $\lim\frac{e^x-1-x}{x^2}=\tfrac12$ is a Taylor coefficient met early.
> - [[08 - Multivariable Optimization|Ch. 08]] — critical points become $\nabla f=\mathbf 0$, the second-derivative test becomes the **Hessian**, and **the saddle point is the multivariable version of $x^3$'s failure.**
> - [[Optimization/contents/00-Index|Optimization]] — **this chapter is its first chapter.** Convexity is concavity generalised; Newton's method on $f'=0$ is the second-order optimizer; damping, trust regions and line search all answer the failure modes above.
> - [[Mathematical Statistics/contents/05 - Point Estimation|Math Stats ch. 05]] — **maximum likelihood is this chapter**: differentiate the log-likelihood, set to zero, check the second derivative. **Maximising $\ln L$ instead of $L$ is Exercise 4(iv)'s monotone-transform trick.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — every trained model is an optimisation; **local minima, saddle points and learning-rate schedules are all this chapter's concerns at scale.**
> - [[Microeconomics/contents/00-Index|Microeconomics]] — "marginal cost = marginal revenue" is $f'=0$; the second-order condition is the concavity test.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **In this chapter it is especially destructive for the inequality-heavy material**: the sign charts that organise every First Derivative Test extract as unstructured runs of symbols, and `<` is `≤` while `>` survives, so **the strictness of every inequality had to be re-derived from context.**
>
> **Figures lost, and several were carrying the argument:**
> - **§4.1's graphs of the EVT failing** — one for each dropped hypothesis — are the clearest statement of why the hypotheses matter, and they are gone.
> - **§4.3's paired graphs of $f$, $f'$ and $f''$**, which are the entire point of the section: seeing that $f'$ crosses zero where $f$ turns, and $f''$ crosses zero where $f$ changes curvature.
> - **§4.7's diagrams for every optimisation word problem** — the box, the fence, the can. **These are how you set the problem up**, and a word problem without its picture is materially harder.
> - **§4.8's Newton's-method figures**, including the tangent-line construction and, importantly, **the pictures of the method diverging and cycling.**
> - **§4.5–4.6's curve-sketching gallery**, which is the section's whole content.
>
> **Verification performed:** every limit, critical point, extremum and iterate in this chapter was computed symbolically or numerically. Confirmed: all six l'Hôpital limits ($\tfrac12$, $0$, $0$, $0$, $e$, $1$); the complete analysis of $x^3-3x^2+1$ (critical numbers $0,2$; inflection at $1$; values $1,-1,-3$); the closed-interval extrema on $[-1,3]$ (max 1, min $-3$, **each attained twice**); the fence problem ($x=600$, $A=720{,}000$); the box problem ($x=2$, $V=128$, with $x=6$ a spurious endpoint critical number); the MVT point $c=\sqrt3$ on $[0,3]$; and **all four Newton iterates for $x^3-x-1$ against the true root $1.32471795724474603$, confirming the digit-doubling 2, 3, 6, 12.** The cycling counterexample $x^3-2x+2$ from $x_0=0$ was checked by hand. **No error was found in the text's mathematics.**
>
> **Scope note:** **§4.5 and §4.6 (curve sketching, with and without technology) are compressed to a checklist and one worked example.** Stewart spends nineteen pages on them; **software draws better graphs, and what survives is the reasoning from $f'$ and $f''$**, which is stated in §3 and used in Exercise 1. **§4.2's proof of the MVT via Rolle's theorem is stated rather than proved** — the statement is what gets used, and the proof adds nothing a data-science reader will reuse. **§4.9 (antiderivatives) is given as a short table**, since it is entirely subsumed by [[04 - Integrals|ch. 04]]; it appears here only because Stewart places it here and because the MVT corollary that justifies "$+C$" belongs with the MVT.

#calculus #optimization #extreme-values #mean-value-theorem #lhopital #newtons-method #concavity #antiderivatives
