---
subject: Calculus
chapter: 01
tags: [ds, calculus, functions, limits, continuity, asymptotes, squeeze-theorem, ivt]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 1–2 (pp. 7–170)"
---

# Functions, Limits and Continuity

> [!abstract] What this chapter is for
> **Calculus has exactly one new idea, and this is it.** Everything that follows — derivatives, integrals, series, gradients, Jacobians — is a limit in disguise:
>
> $$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h},\qquad \int_a^bf=\lim_{n\to\infty}\sum_{i=1}^nf(x_i^*)\,\Delta x,\qquad \sum_{n=0}^\infty a_n=\lim_{N\to\infty}\sum_{n=0}^N a_n$$
>
> **The limit answers a question ordinary algebra cannot ask: what does $f(x)$ approach as $x$ approaches $a$, when $f(a)$ itself may be undefined?** That "may be undefined" is the whole point — $\frac{f(a+h)-f(a)}{h}$ is $\frac00$ at $h=0$, and calculus exists to make sense of it.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Functions and models | Domain, transformations, composition, **inverses and logarithms** |
> | **2** | **The limit** | $\lim_{x\to a}f(x)$ ignores $f(a)$ entirely |
> | **3** | Limit laws | Algebra passes through limits — **except where it produces $\tfrac00$** |
> | **4** | The precise definition | $\varepsilon$–$\delta$: "as close as you like, by getting close enough" |
> | **5** | **Continuity** | $\lim_{x\to a}f(x)=f(a)$; the **Intermediate Value Theorem** |
> | **6** | Limits at infinity | Horizontal asymptotes and end behaviour |
>
> **A warning that Stewart makes better than most books and that this chapter takes seriously: numerical tables lie.** Three of his examples produce tables that point confidently at the wrong answer. **§2 below reproduces all three.**

---

## 📘 Main Knowledge

### 1. Functions and models

A **function** $f$ assigns to each element of a **domain** $D$ exactly one element $f(x)$ of the **range**. **The vertical line test** is this statement drawn: a curve is the graph of a function iff no vertical line meets it twice.

**Four representations:** verbal, numerical (a table), visual (a graph), algebraic (a formula). **A modelling problem usually moves between them**, and the ability to do so is more of the subject than any formula.

> [!important] The catalogue of essential functions
> | Type | Form | Notes |
> |---|---|---|
> | **Linear** | $mx+b$ | constant *rate of change* — the reference point for everything |
> | **Polynomial** | $a_nx^n+\cdots+a_0$ | domain $\mathbb{R}$; end behaviour set by $a_nx^n$ |
> | **Power** | $x^a$ | $a$ integer, $1/n$ (roots), or negative (reciprocals) |
> | **Rational** | $P(x)/Q(x)$ | domain excludes the zeros of $Q$ — **the source of asymptotes** |
> | **Trigonometric** | $\sin x,\cos x,\tan x$ | periodic; **radians always** |
> | **Exponential** | $a^x$, $a>0$ | range $(0,\infty)$; **grows faster than any polynomial** |
> | **Logarithmic** | $\log_a x$ | domain $(0,\infty)$; **grows slower than any positive power** |

**Transformations of $y=f(x)$:** $f(x)+c$ shifts up, $f(x+c)$ shifts **left**, $cf(x)$ stretches vertically, $f(cx)$ compresses horizontally by $c$, $-f(x)$ reflects in the $x$-axis, $f(-x)$ in the $y$-axis.

> [!warning] Horizontal transformations run backwards
> **$f(x+2)$ shifts the graph *left* by 2, and $f(2x)$ *compresses* it.** The inside of the function does the opposite of what it looks like, because you must feed in a *smaller* $x$ to get the same output.
>
> **This is the single most common sign error in the chapter**, and it recurs in every substitution later in the course.

**Composition** $(f\circ g)(x)=f(g(x))$ — **do $g$ first.** The domain is $\{x\in D_g:g(x)\in D_f\}$. **Composition is the operation the chain rule differentiates, so getting the order right here pays off in [[02 - Derivatives|ch. 02]].**

> [!important] Inverse functions and logarithms
> $f$ is **one-to-one** ($f(x_1)\ne f(x_2)$ whenever $x_1\ne x_2$ — the **horizontal** line test) iff it has an inverse, defined by
> $$f^{-1}(y)=x\iff f(x)=y$$
> **The graph of $f^{-1}$ is the graph of $f$ reflected in $y=x$**, and $\text{domain}(f^{-1})=\text{range}(f)$.
>
> **The logarithm is defined as the inverse of the exponential:**
> $$\log_a x=y\iff a^y=x,\qquad \ln x=\log_e x$$
> $$\ln(xy)=\ln x+\ln y,\qquad \ln(x^r)=r\ln x,\qquad \log_a x=\frac{\ln x}{\ln a}$$

> [!tip] Why $\ln$ is *the* logarithm for this course
> **Base $e$ is the only base for which $\frac{d}{dx}a^x=a^x$** — every other base picks up a factor of $\ln a$ ([[02 - Derivatives|ch. 02]]). That is the whole reason $e$ is singled out.
>
> **And logs turn products into sums**, which is why they appear everywhere downstream: log-likelihoods ([[Mathematical Statistics/contents/05 - Point Estimation|Math Stats ch. 05]]), log returns ([[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06]]), and elasticities in [[Econometrics/contents/00-Index|Econometrics]], where $\frac{d\ln y}{d\ln x}$ is a percentage-per-percentage rate.

---

### 2. The limit

> [!important] Intuitive definition
> $$\lim_{x\to a}f(x)=L$$
> means **$f(x)$ can be made arbitrarily close to $L$ by taking $x$ sufficiently close to $a$ but not equal to $a$.**

> [!warning] The limit ignores $f(a)$ completely
> **The phrase "but not equal to $a$" is the definition's whole content.** Three functions can share a limit at $a$ and disagree wildly there:
>
> | $f$ near $x=1$ | $f(1)$ | $\lim_{x\to1}f(x)$ |
> |---|---|---|
> | $\dfrac{x^2-1}{x-1}$ | **undefined** | $2$ |
> | $x+1$ | $2$ | $2$ |
> | $x+1$ for $x\ne1$, $f(1)=99$ | $99$ | $2$ |
>
> **This is not a technicality — it is the reason limits exist.** The derivative's difference quotient is $\tfrac00$ at $h=0$, so a notion that *refused* to ignore the value at the point would be useless.

**One-sided limits** $\lim_{x\to a^-}$ and $\lim_{x\to a^+}$ approach from below and above, and

$$\lim_{x\to a}f(x)=L\iff \lim_{x\to a^-}f(x)=L=\lim_{x\to a^+}f(x)$$

> [!important] The three ways a limit fails
> | Failure | Example at $0$ |
> |---|---|
> | **Jump** — one-sided limits differ | $\dfrac{|x|}{x}$: left $-1$, right $+1$ |
> | **Infinite** — grows without bound | $\dfrac1{x^2}$ |
> | **Oscillation** — never settles | $\sin\dfrac1x$ |
>
> **"$\lim=\infty$" is a description of *how* the limit fails, not a value.** It says the function grows beyond every bound, and it is why $x=a$ is a **vertical asymptote**.

#### 2a. Numerical tables lie — three worked cautionary examples

> [!warning] Stewart's best pedagogical point, and it is worth taking seriously
> **Evaluating a function at a sequence of points is *evidence*, not proof — and it can be confidently wrong.** All three of the following are from §2.2, and all three are verified below.

> [!example] Example A — the table converges to the wrong number
> $$\lim_{x\to0}\left(x^3+\frac{\cos5x}{10{,}000}\right)$$
> | $x$ | value |
> |---|---|
> | $1$ | $1.0000284$ |
> | $0.5$ | $0.1249199$ |
> | $0.1$ | $0.0010878$ |
> | $0.05$ | $0.0002219$ |
> | $0.01$ | $0.0001009$ |
>
> **The values plunge toward 0** — and the limit is $\boxed{0.0001}$, since $\cos5x\to1$. *(Verified: the exact limit is $\tfrac1{10000}$.)*
>
> **The table was never going to reveal this**, because $0.0001$ and $0$ are indistinguishable until you look at the fifth decimal place.

> [!example] Example B — the table changes its mind
> $$\lim_{x\to0}\left(x^2-\frac{2^x}{1000}\right)$$
> | $x$ | $1$ | $0.8$ | $0.4$ | $0.1$ | $0.05$ | $0.04$ | $0.02$ | $0.01$ |
> |---|---|---|---|---|---|---|---|---|
> | $f(x)$ | $.998$ | $.638$ | $.159$ | $.00893$ | $.00146$ | $.00057$ | $\mathbf{-.00061}$ | $\mathbf{-.00091}$ |
>
> **The first six values head confidently to 0 from above; then the sign flips.** The true limit is $\boxed{-0.001}$. *(All values verified.)*
>
> **Stop one row earlier and you get the wrong answer with the wrong sign.**

> [!example] Example C — the computer gives 0, and 0 is wrong
> $$\lim_{x\to0}\frac{\tan x-x}{x^3}$$
> | $x$ | $1$ | $0.5$ | $0.1$ | $0.05$ | $0.01$ | $0.005$ |
> |---|---|---|---|---|---|---|
> | $h(x)$ | $.5574$ | $.3704$ | $.33467$ | $.33367$ | $.333347$ | $.333337$ |
>
> **This one converges beautifully to $\boxed{1/3}$** *(verified exactly)*. **But push further and floating-point arithmetic returns exactly 0**, because $\tan x$ and $x$ agree to more digits than a `double` carries, and their difference is annihilated by cancellation before being divided by a tiny $x^3$.
>
> **So the same procedure gives the right answer, then the wrong one, as you refine it.** **Catastrophic cancellation is not a calculus problem; it is a numerical one** — and it is why [[04 - Integrals|ch. 04]]'s and [[05 - Techniques of Integration|ch. 05]]'s numerical methods come with error analysis attached.

---

### 3. Limit laws

> [!important] The Limit Laws
> If $\lim_{x\to a}f(x)$ and $\lim_{x\to a}g(x)$ both exist, then
> $$\lim(f\pm g)=\lim f\pm\lim g,\qquad \lim(cf)=c\lim f,\qquad \lim(fg)=\lim f\cdot\lim g$$
> $$\lim\frac fg=\frac{\lim f}{\lim g}\quad\textbf{provided }\lim g\ne0,\qquad \lim f^n=\left(\lim f\right)^n,\qquad \lim\sqrt[n]{f}=\sqrt[n]{\lim f}$$

> [!important] Direct Substitution Property
> **If $f$ is a polynomial or a rational function and $a$ is in its domain, then**
> $$\lim_{x\to a}f(x)=f(a)$$
> — **just plug in.** The same holds for any function continuous at $a$ (§5), which covers roots, trigonometric, exponential and logarithmic functions on their domains.

> [!tip] So when is a limit actually *work*?
> **Only when direct substitution fails**, and it fails in exactly one interesting way: it produces $\tfrac00$. **Then the numerator and denominator share a factor that must be cancelled first**, and the standard moves are:
>
> | Form | Technique |
> |---|---|
> | $\dfrac{\text{poly}}{\text{poly}}$, both $\to0$ | **factor and cancel** |
> | involving $\sqrt{\ }$ | **multiply by the conjugate** |
> | piecewise or $\lvert\cdot\rvert$ | **split into one-sided limits** |
> | trigonometric | use $\displaystyle\lim_{\theta\to0}\frac{\sin\theta}{\theta}=1$ |
> | anything else | **the Squeeze Theorem**, or l'Hôpital in [[03 - Applications of Differentiation\|ch. 03]] |
>
> **Cancelling is legitimate precisely because the limit ignores $x=a$** — you are dividing by something non-zero at every $x$ the limit actually looks at.

> [!important] The Squeeze Theorem
> If $g(x)\le f(x)\le h(x)$ near $a$ and $\lim_{x\to a}g(x)=\lim_{x\to a}h(x)=L$, then $\lim_{x\to a}f(x)=L$.

**The archetype:** $-x^2\le x^2\sin\frac1x\le x^2$ and both bounds $\to0$, so $\lim_{x\to0}x^2\sin\frac1x=0$ — **even though $\sin\frac1x$ oscillates infinitely fast and has no limit at all.** *(Verified.)*

> [!tip] What the Squeeze Theorem is for
> **Use it when the function itself is unmanageable but is trapped between two that are not.** The bounds do the work; $f$ never has to be evaluated.
>
> **This is the same logic as the sandwich arguments in [[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]]** — bound the thing you cannot compute by things you can.

---

### 4. The precise definition

> [!important] The $\varepsilon$–$\delta$ definition
> $$\lim_{x\to a}f(x)=L$$
> means: **for every $\varepsilon>0$ there is a $\delta>0$ such that**
> $$0<|x-a|<\delta\ \Longrightarrow\ |f(x)-L|<\varepsilon$$

> [!tip] How to read it as a game
> **Your opponent names a tolerance $\varepsilon$ — how close to $L$ they demand. You must name a $\delta$ — how close to $a$ you need $x$ to be. You win if you can always answer, however small $\varepsilon$ is.**
>
> **"$0<|x-a|$" is where "but not equal to $a$" lives**, and it is why the definition never mentions $f(a)$.
>
> **This is the only fully rigorous statement in the chapter**, and it is what everything else rests on. **For computation you will use the limit laws; for proofs you need this.** *(The same $\varepsilon$–$N$ pattern defines convergence of sequences in [[06 - Sequences, Series and Taylor Approximation|ch. 06]] and convergence in probability in [[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]].)*

---

### 5. Continuity

> [!important] Definition
> $f$ is **continuous at $a$** if
> $$\lim_{x\to a}f(x)=f(a)$$
> — which packs in **three** requirements: $f(a)$ is defined, the limit exists, and they agree.

> [!important] Types of discontinuity
> | Type | Example | Fixable? |
> |---|---|---|
> | **Removable** | $\dfrac{x^2-1}{x-1}$ at $x=1$ | **Yes** — redefine $f(1)=2$ |
> | **Jump** | $\dfrac{|x|}{x}$ at $0$ | No |
> | **Infinite** | $\dfrac1{x^2}$ at $0$ | No |

**Continuity is preserved by everything:** sums, differences, products, quotients (where the denominator is non-zero), and **composition** — if $g$ is continuous at $a$ and $f$ at $g(a)$, then $f\circ g$ is continuous at $a$. **Polynomials, rational, root, trigonometric, exponential, logarithmic and inverse-trigonometric functions are continuous on their domains.**

> [!tip] Continuity is what licenses "just plug in"
> **Every direct-substitution computation is an appeal to continuity**, and the reason limits are usually easy is that the standard functions are continuous almost everywhere. **The interesting points are exactly where continuity fails**, which in practice means: where a denominator vanishes, where a piecewise definition switches, and where a root or log leaves its domain.

> [!important] The Intermediate Value Theorem
> If $f$ is **continuous on $[a,b]$** and $N$ lies between $f(a)$ and $f(b)$, then $f(c)=N$ for some $c\in(a,b)$.

> [!tip] The IVT is an existence theorem, and it is the ancestor of bisection
> **It guarantees a root exists; it does not find one.** But it makes the **bisection method** work: if $f(1)<0<f(2)$ there is a root in $(1,2)$; test the midpoint and halve the interval.
>
> **Continuity is essential.** $f(x)=1/x$ takes the values $-1$ at $x=-1$ and $1$ at $x=1$ and is never 0 — because it is not continuous on $[-1,1]$. **A "theorem" whose hypothesis you skipped is not a theorem.**

---

### 6. Limits at infinity

$$\lim_{x\to\infty}f(x)=L$$ means $f(x)$ can be made arbitrarily close to $L$ by taking $x$ large enough; the line $y=L$ is then a **horizontal asymptote**.

> [!important] The technique: divide by the highest power in the denominator
> $$\lim_{x\to\infty}\frac{3x^2-2x+1}{5x^2+x-4}=\lim_{x\to\infty}\frac{3-\tfrac2x+\tfrac1{x^2}}{5+\tfrac1x-\tfrac4{x^2}}=\frac35$$
> using $\lim_{x\to\infty}\frac1{x^r}=0$ for $r>0$. *(Verified.)*
>
> **For a rational function, only the leading terms matter:**
> | Degrees | $\lim_{x\to\pm\infty}$ |
> |---|---|
> | $\deg P<\deg Q$ | $0$ |
> | $\deg P=\deg Q$ | ratio of leading coefficients |
> | $\deg P>\deg Q$ | $\pm\infty$ (no horizontal asymptote) |

> [!warning] $\sqrt{x^2}=|x|$, not $x$ — and this changes the answer as $x\to-\infty$
> $$\lim_{x\to\infty}\frac{\sqrt{2x^2+1}}{3x-5}=\frac{\sqrt2}{3},\qquad \lim_{x\to-\infty}\frac{\sqrt{2x^2+1}}{3x-5}=-\frac{\sqrt2}{3}$$
> *(Both verified.)* **A function can have two different horizontal asymptotes**, and the sign error that misses one is always this: pulling $x$ out of a square root without an absolute value.

**The rates that matter downstream:**

$$\ln x\ \ll\ x^p\ \ll\ e^x\qquad\text{as }x\to\infty\ \ (p>0)$$

**Exponentials beat every power; every positive power beats every logarithm.** *(Proved with l'Hôpital in [[03 - Applications of Differentiation|ch. 03]].)*

---

## ✏️ Exercises

> [!question] Exercise 1 — computing limits *(warm-up)*
> Evaluate, or show the limit does not exist. Name the technique in each case.
> (i) $\displaystyle\lim_{x\to3}\frac{x^2-9}{x-3}$
> (ii) $\displaystyle\lim_{x\to0}\frac{\sqrt{x+4}-2}{x}$
> (iii) $\displaystyle\lim_{x\to2}\frac{x^3-8}{x^2-4}$
> (iv) $\displaystyle\lim_{x\to0}\frac{\sin3x}{5x}$
> (v) $\displaystyle\lim_{x\to0}\frac{|x|}{x}$

> [!example]- Solution
> **(i) Factor and cancel.** $\dfrac{(x-3)(x+3)}{x-3}=x+3$ for $x\ne3$, so the limit is $\boxed{6}$.
>
> **The cancellation is legal precisely because the limit never evaluates at $x=3$.**
>
> **(ii) Conjugate.** Multiply above and below by $\sqrt{x+4}+2$:
> $$\frac{(x+4)-4}{x\left(\sqrt{x+4}+2\right)}=\frac{1}{\sqrt{x+4}+2}\ \longrightarrow\ \frac14$$
> $\boxed{1/4}$ — **the conjugate trick exists to move the vanishing factor from a root into a polynomial where it can cancel.**
>
> **(iii) Factor both.** $\dfrac{(x-2)(x^2+2x+4)}{(x-2)(x+2)}\to\dfrac{4+4+4}{4}=\boxed{3}$
>
> **(iv) Rescale to the standard limit.** $\dfrac{\sin3x}{5x}=\dfrac35\cdot\dfrac{\sin3x}{3x}\to\dfrac35\cdot1=\boxed{3/5}$
>
> **The whole difficulty is making the argument of $\sin$ match the denominator** — $\lim_{\theta\to0}\frac{\sin\theta}\theta=1$ only applies when both are the same $\theta$.
>
> **(v) One-sided limits differ.** For $x>0$, $\frac{|x|}x=1$; for $x<0$, $\frac{|x|}x=-1$. **So $\boxed{\text{the limit does not exist}}$** — a jump discontinuity.
>
> *(All five verified symbolically.)*
>
> > [!tip] The diagnostic that comes first
> > **Substitute. If you get a number, that is the answer.** Only if you get $\tfrac00$ is there work to do — and then the form tells you the technique: polynomials $\Rightarrow$ factor, roots $\Rightarrow$ conjugate, $\lvert\cdot\rvert$ or piecewise $\Rightarrow$ split.
> >
> > **And if substitution gives $\tfrac{c}{0}$ with $c\ne0$, the limit is infinite** — a vertical asymptote, not an indeterminate form. **Do not apply cancellation tricks to it.**

> [!question] Exercise 2 — the Squeeze Theorem
> (i) Evaluate $\displaystyle\lim_{x\to0}x^2\sin\frac1x$, justifying each step.
> (ii) Does $\displaystyle\lim_{x\to0}\sin\frac1x$ exist?
> (iii) Does $\displaystyle\lim_{x\to0}x\sin\frac1x$ exist?
> (iv) Why can the limit laws not be used directly in (i)?

> [!example]- Solution
> **(i)** Since $-1\le\sin\frac1x\le1$ for all $x\ne0$, multiplying by $x^2>0$ gives
> $$-x^2\le x^2\sin\tfrac1x\le x^2$$
> Both bounds $\to0$, so by the Squeeze Theorem the limit is $\boxed{0}$. *(Verified.)*
>
> **(ii) No.** As $x\to0$, $\frac1x\to\infty$ and $\sin\frac1x$ oscillates between $-1$ and $1$ infinitely often. Concretely, $x=\frac1{2\pi n}$ gives 0 while $x=\frac1{2\pi n+\pi/2}$ gives 1, and both sequences $\to0$ — **so no single value is approached.**
>
> **(iii) Yes, and it is 0** — the same squeeze with $-|x|\le x\sin\frac1x\le|x|$.
>
> **(iv)** The Product Law requires **both** factors to have limits, and $\lim_{x\to0}\sin\frac1x$ **does not exist** by (ii). **So the law does not apply, and writing "$0\times(\text{something bounded})=0$" is an assertion, not a citation.**
>
> **The Squeeze Theorem is exactly the tool for "one factor $\to0$, the other misbehaves but stays bounded"** — and that pattern recurs constantly, e.g. in showing a series converges by comparison.

> [!question] Exercise 3 — continuity
> (i) Classify the discontinuities of $f(x)=\dfrac{x^2-1}{x-1}$ and of $g(x)=\dfrac1{x^2-4}$.
> (ii) Find $c$ making $\ h(x)=\begin{cases}x^2+c,&x<2\\ cx+1,&x\ge2\end{cases}$ continuous everywhere.
> (iii) Show $x^3-x-1=0$ has a root in $(1,2)$, and locate it to one decimal place by bisection.
> (iv) Why does the IVT not apply to $f(x)=1/x$ on $[-1,1]$?

> [!example]- Solution
> **(i)** $f$ has a **removable** discontinuity at $x=1$: $f(x)=x+1$ for $x\ne1$, so the limit is 2 and redefining $f(1)=2$ repairs it.
> $g$ has **infinite** discontinuities at $x=\pm2$ — vertical asymptotes, not repairable by any redefinition.
>
> **(ii)** Both pieces are continuous on their own intervals, so only $x=2$ matters. The one-sided limits are $4+c$ (from the left) and $2c+1$ (from the right, which also equals $h(2)$). Setting them equal:
> $$4+c=2c+1\ \Longrightarrow\ \boxed{c=3}$$
> *(Verified.)* **Both sides then equal 7.**
>
> **(iii)** $f(x)=x^3-x-1$ is a polynomial, hence continuous, and
> $$f(1)=-1<0<5=f(2)$$
> **so by the IVT there is a root in $(1,2)$.** Bisecting:
> | interval | midpoint $m$ | $f(m)$ | keep |
> |---|---|---|---|
> | $(1,2)$ | $1.5$ | $+0.875$ | $(1,1.5)$ |
> | $(1,1.5)$ | $1.25$ | $-0.297$ | $(1.25,1.5)$ |
> | $(1.25,1.5)$ | $1.375$ | $+0.225$ | $(1.25,1.375)$ |
> | $(1.25,1.375)$ | $1.3125$ | $-0.0515$ | $(1.3125,1.375)$ |
>
> **So the root is $\approx1.3$** *(the exact value is $1.32472$ — verified)*.
>
> **Each step halves the interval, so bisection gains about $\log_{10}2\approx0.3$ decimal places per iteration** — reliable and slow. **[[03 - Applications of Differentiation|Newton's method]] roughly *doubles* the digits each step, at the cost of needing $f'$ and a good start.**
>
> **(iv)** **$1/x$ is not continuous on $[-1,1]$** — it is not even defined at 0. **The hypothesis fails, so the conclusion is not available**, and indeed $f$ jumps from $-1$ to $1$ without ever taking the value 0.
>
> **This is the standard warning about existence theorems: the hypotheses are not decoration.**

> [!question] Exercise 4 — limits at infinity and asymptotes
> Find all horizontal and vertical asymptotes.
> (i) $\displaystyle f(x)=\frac{3x^2-2x+1}{5x^2+x-4}$
> (ii) $\displaystyle g(x)=\frac{2x^3+1}{x^2-3}$
> (iii) $\displaystyle h(x)=\frac{\sqrt{2x^2+1}}{3x-5}$
> (iv) $\displaystyle k(x)=\sqrt{x^2+1}-x$ as $x\to\infty$

> [!example]- Solution
> **(i)** Equal degrees, so divide by $x^2$:
> $$\lim_{x\to\pm\infty}f(x)=\frac{3}{5}$$
> — **one horizontal asymptote $y=3/5$** *(verified)*. Vertical asymptotes where $5x^2+x-4=(5x-4)(x+1)=0$: $x=4/5$ and $x=-1$.
>
> **(ii)** Numerator degree exceeds denominator degree, so $g\to\pm\infty$: **no horizontal asymptote** *(verified: $+\infty$ as $x\to\infty$)*. Vertical asymptotes at $x=\pm\sqrt3$.
>
> **(iii) The interesting one.** For $x>0$, $\sqrt{2x^2+1}=x\sqrt{2+1/x^2}$, giving $\frac{\sqrt2}{3}$. **For $x<0$, $\sqrt{x^2}=|x|=-x$**, so
> $$\lim_{x\to\infty}h(x)=\frac{\sqrt2}{3},\qquad \lim_{x\to-\infty}h(x)=-\frac{\sqrt2}{3}$$
> — **two different horizontal asymptotes** *(both verified)*. Vertical asymptote at $x=5/3$.
>
> **(iv)** This is $\infty-\infty$, an indeterminate form; **rationalise**:
> $$\sqrt{x^2+1}-x=\frac{(x^2+1)-x^2}{\sqrt{x^2+1}+x}=\frac{1}{\sqrt{x^2+1}+x}\ \longrightarrow\ \boxed{0}$$
> *(Verified.)*
>
> > [!warning] $\infty-\infty$ is indeterminate and the conjugate is the standard fix
> > **Two quantities both growing without bound can have a difference that vanishes, is constant, or explodes** — the form tells you nothing. Here $\sqrt{x^2+1}$ and $x$ differ by less than any $\varepsilon$ eventually, even though each is enormous.
> >
> > **The same manoeuvre — multiply by the conjugate to turn a difference of roots into a quotient — handles every problem of this shape**, and it is worth recognising before reaching for l'Hôpital.

> [!question] Exercise 5 — the precise definition, and a pathology *(hard)*
> **(a)** Prove from the $\varepsilon$–$\delta$ definition that $\displaystyle\lim_{x\to3}(2x-1)=5$.
> **(b)** Prove that $\displaystyle\lim_{x\to0}\sin\frac1x$ does **not** exist, using sequences.
> **(c)** Let $f(x)=\begin{cases}x,&x\text{ rational}\\ 0,&x\text{ irrational}\end{cases}$. Show $f$ is continuous at $0$ and **nowhere else**.

> [!example]- Solution
> **(a)** Given $\varepsilon>0$, we need $\delta>0$ with $0<|x-3|<\delta\Rightarrow|(2x-1)-5|<\varepsilon$.
>
> **Work backwards from the goal:** $|(2x-1)-5|=|2x-6|=2|x-3|$, so requiring this to be $<\varepsilon$ means requiring $|x-3|<\varepsilon/2$.
>
> **So take $\boxed{\delta=\varepsilon/2}$.** Then $0<|x-3|<\delta$ gives $|(2x-1)-5|=2|x-3|<2\delta=\varepsilon$. $\blacksquare$
>
> **The method is always this: start from $|f(x)-L|$, manipulate it into a multiple of $|x-a|$, and read off $\delta$.** The final write-up runs forwards; the discovery runs backwards.
>
> **(b)** Take two sequences approaching 0:
> $$x_n=\frac1{2\pi n}\ \Rightarrow\ \sin\frac1{x_n}=\sin(2\pi n)=0$$
> $$y_n=\frac1{2\pi n+\pi/2}\ \Rightarrow\ \sin\frac1{y_n}=\sin\left(2\pi n+\tfrac\pi2\right)=1$$
> **Both $x_n\to0$ and $y_n\to0$, but the function values go to 0 along one and 1 along the other.** If $\lim_{x\to0}\sin\frac1x=L$ existed, both would have to equal $L$ — so $0=L=1$, a contradiction. $\blacksquare$
>
> **"Find two sequences with different limits" is the standard way to *disprove* a limit**, and it is much easier than arguing with $\varepsilon$ and $\delta$ directly.
>
> **(c) Continuity at 0.** For every $x$, $|f(x)|\le|x|$ (it is either $|x|$ or 0), so
> $$-|x|\le f(x)\le|x|$$
> and the Squeeze Theorem gives $\lim_{x\to0}f(x)=0=f(0)$. **Continuous at 0.**
>
> **Discontinuity everywhere else.** Fix $a\ne0$. Every interval around $a$ contains both rationals and irrationals *(the rationals and irrationals are each dense)*, so arbitrarily close to $a$ the function takes values near $a$ **and** exactly 0. Since $a\ne0$, these do not both approach a single value — **no limit exists at $a$, so $f$ is discontinuous there.** $\blacksquare$
>
> > [!important] What this example is really showing
> > **Continuity is a genuinely *local* property, and it can hold at exactly one point.** No amount of "the graph is one unbroken curve" intuition survives contact with this function, whose graph is two dust clouds — the line $y=x$ with the irrationals removed, and the $x$-axis with the rationals removed.
> >
> > **That is why the $\varepsilon$–$\delta$ definition exists.** The intuitive definition cannot even express what is happening here, let alone decide it. **Pathological examples are what force a definition to be precise**, and this one is the reason "continuous" is not defined as "you can draw it without lifting your pen".

---

## 📝 Summary

- **The limit is the one new idea in calculus**, and every later construction — derivative, integral, series, gradient — is a limit. $\lim_{x\to a}f(x)$ **ignores $f(a)$ entirely**, which is exactly what makes it useful for $\tfrac00$ forms.
- **Horizontal transformations run backwards:** $f(x+2)$ shifts *left*, $f(2x)$ *compresses*.
- **$\ln$ is singled out because $\frac{d}{dx}e^x=e^x$**; logs turn products into sums, which is why they run through statistics and econometrics.
- **A limit fails in three ways:** a **jump** (one-sided limits differ), an **infinity** (a vertical asymptote), or **oscillation**. "$\lim=\infty$" describes a failure, it is not a value.
- **Numerical tables can be confidently wrong** — Stewart's three examples give a table converging to 0 when the answer is $10^{-4}$, a table that changes sign at the seventh row, and a computation that returns exactly 0 through catastrophic cancellation when the answer is $\tfrac13$.
- **The limit laws let algebra pass through limits, and the Direct Substitution Property means "just plug in" for polynomials, rationals and every continuous function.** Work is needed **only** when substitution gives $\tfrac00$ — then factor, rationalise, split, or squeeze.
- **The Squeeze Theorem handles "small times bounded-but-wild"**: $x^2\sin\frac1x\to0$ even though $\sin\frac1x$ has no limit. **The limit laws cannot be used there**, because one factor has no limit.
- **The $\varepsilon$–$\delta$ definition is the only rigorous statement in the chapter** — for every tolerance $\varepsilon$ there is a closeness $\delta$. The clause $0<|x-a|$ is where "ignore $f(a)$" lives.
- **Continuity at $a$ means $\lim_{x\to a}f(x)=f(a)$** — three conditions in one. Discontinuities are **removable**, **jump** or **infinite**, and only the first can be repaired.
- **The IVT guarantees a root exists** when a continuous function changes sign, and it is what makes **bisection** work — reliable, and about $0.3$ decimal places per step.
- **Limits at infinity: divide by the highest power.** For rationals, compare degrees. **$\sqrt{x^2}=|x|$, so a function can have two different horizontal asymptotes**, and $\infty-\infty$ is indeterminate — rationalise.
- **$\ln x\ll x^p\ll e^x$** — exponentials beat powers beat logarithms, and this ordering governs every asymptotic comparison in the degree.

---

## ⚠️ Important Notes

> [!warning] $\lim_{x\to a}f(x)$ and $f(a)$ are different questions
> **They agree exactly when $f$ is continuous at $a$ — which is the definition of continuity, not a general fact.** Three functions agreeing everywhere except at $a$ share a limit there and may have any values at all at $a$ itself.
>
> **Every derivative in [[02 - Derivatives|ch. 02]] depends on this**, since $\frac{f(a+h)-f(a)}{h}$ is undefined at $h=0$ and the limit is taken anyway.

> [!warning] A numerical table is evidence, not proof
> **All three of Stewart's cautionary examples are in §2a above**, and they fail in three different ways: too-slow convergence, a sign change past where you stopped, and floating-point cancellation.
>
> **The practical rules:** get an exact answer algebraically when you can; when you cannot, **watch the trend rather than the last value**, and **be suspicious when a computed difference of two nearly-equal numbers is divided by something tiny.** *(That last is exactly the shape of every difference quotient, which is why numerical differentiation is unstable.)*

> [!warning] $\tfrac00$ is indeterminate; $\tfrac c0$ is not
> | Substitution gives | Meaning |
> |---|---|
> | a number | that is the limit |
> | $\tfrac00$ | **indeterminate** — cancel, rationalise, squeeze, or use l'Hôpital |
> | $\tfrac c0$, $c\ne0$ | **infinite** — a vertical asymptote |
>
> **The other indeterminate forms are $\tfrac\infty\infty$, $0\cdot\infty$, $\infty-\infty$, $0^0$, $1^\infty$, $\infty^0$** — all handled in [[03 - Applications of Differentiation|ch. 03]]. **Applying l'Hôpital's rule to a form that is *not* indeterminate produces a confident wrong answer.**

> [!warning] $\sqrt{x^2}=|x|$
> **The most reliable sign error in the chapter.** When $x\to-\infty$, pulling $x$ out of $\sqrt{2x^2+1}$ gives $-x\sqrt{2+1/x^2}$, and forgetting the minus loses one of the two horizontal asymptotes.
>
> **Check the sign of the limit against a large negative value before believing the algebra.**

> [!warning] Existence theorems need their hypotheses
> **The IVT requires continuity on a *closed* interval**, and $1/x$ on $[-1,1]$ shows what happens without it. The same discipline applies to the Extreme Value Theorem and the Mean Value Theorem in [[03 - Applications of Differentiation|ch. 03]].
>
> **And the IVT is purely existential** — it produces no value of $c$, only a guarantee. **Bisection is the constructive version, and it costs one function evaluation per bit of accuracy.**

> [!warning] "Continuous" does not mean "you can draw it"
> The function that is $x$ on the rationals and $0$ on the irrationals is **continuous at exactly one point** (Exercise 5(c)) and cannot be drawn at all.
>
> **The pen-and-paper intuition is a useful picture for the functions you will meet and a false definition.** It is precisely such examples that force the $\varepsilon$–$\delta$ formulation, and the same discipline resurfaces whenever a "geometrically obvious" claim is asserted without proof.

> [!note] Cross-subject connections
> - [[02 - Derivatives|Ch. 02]] — the derivative **is** a limit, of a quotient that is $\tfrac00$ at the point in question; **differentiability implies continuity but not conversely** ($|x|$ at 0).
> - [[03 - Applications of Differentiation|Ch. 03]] — **l'Hôpital's rule** handles the indeterminate forms this chapter can only factor around; the growth ordering $\ln x\ll x^p\ll e^x$ is proved there; **Newton's method** is bisection's fast cousin.
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — sequence convergence is the same $\varepsilon$ definition with $N$ in place of $\delta$.
> - [[07 - Partial Derivatives and the Gradient|Ch. 07]] — limits in several variables must hold along **every** path, which is a genuinely stronger requirement and where most multivariable limits fail.
> - [[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]] — convergence in probability and almost-sure convergence are $\varepsilon$-definitions of exactly this shape; **squeeze arguments are the standard tool** there too.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — consistency of an estimator is a limit statement; asymptotic arguments are limits at infinity.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — **$O(\cdot)$ notation is a limit at infinity**, and $\ln x\ll x^p\ll e^x$ is the complexity hierarchy; **bisection is binary search.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — the catastrophic cancellation of Example C is why gradients are computed by automatic differentiation rather than finite differences.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction is enciphered, and this chapter is where I established the key.** Stewart's maths font maps glyphs to wrong codepoints: **`s`/`d` are parentheses, `f`/`g` are brackets, `−` is `=`, an isolated ` 1 ` is `+`, an isolated ` 2 ` is `−`, `l` is `→`, `y` is a fraction slash, `<` is `≤`, and `t` is a genuine function name** (Stewart uses $f$ and $t$, not $f$ and $g$). **The full table is in [[00-Index]].**
>
> **The `1`/`2` collision is the dangerous part**, because digits and signs share codepoints. `f sxd − x2 2 s2xy1000d` is $f(x)=x^2-\frac{2^x}{1000}$ — three different meanings for `2` in one formula. **Nothing in these notes is quoted from the extraction without being recomputed**, and every limit, table value and root above was verified symbolically or numerically before being written down.
>
> **Every figure is an image, and this chapter loses more to that than any other so far.** Gone entirely: the graphs illustrating the vertical and horizontal line tests; the catalogue of essential function shapes (§1.2); every transformation picture (§1.3); the reflection-in-$y=x$ diagram for inverses (§1.5); the tangent-and-secant construction that motivates the limit (§2.1); **the three graphs of jump, infinite and oscillating discontinuity**; the $\varepsilon$–$\delta$ box diagram (§2.4), which is the single clearest explanation of the definition in the book; and every asymptote sketch (§2.6). **For a subject taught through pictures this is severe** — I have reconstructed the geometric content in prose and tables throughout, but **the $\varepsilon$–$\delta$ picture in particular has no adequate verbal substitute** and is worth finding elsewhere.
>
> **Verification performed:** all three of Stewart's "tables can lie" examples were reproduced exactly. **Example A** (§2.2 Ex. 3): the five tabulated values $1.0000284,\ 0.1249199,\ 0.0010878,\ 0.0002219,\ 0.0001009$ and the exact limit $\tfrac1{10000}$. **Example B** (§2.2 Ex. 47): all eight tabulated values including **the sign change between $x=0.04$ and $x=0.02$**, and the exact limit $-\tfrac1{1000}$. **Example C** (§2.2 Ex. 48): the six tabulated values converging to the exact limit $\tfrac13$. **All agree with the text**, and Example B's sign change — which is the entire point of the exercise — is confirmed at exactly the row Stewart implies. Every exercise figure in these notes was likewise verified, including all five limits in Exercise 1, the parameter $c=3$, the four bisection steps, the true root $1.32472$, and all four asymptote computations.
>
> **Scope note:** **§2.4 (the precise definition) is given in outline rather than developed.** Stewart spends ten pages on $\varepsilon$–$\delta$ proofs for quadratics and on the precise definitions of infinite limits; **the definition itself is essential and the drill is not**, since no later chapter of these notes constructs an $\varepsilon$–$\delta$ proof. **Exercise 5(a) gives the method once** on the linear case, which is enough to see how it works. **§1.2's catalogue of models and §2.1's tangent/velocity motivation are compressed**, the former because it is reference material and the latter because [[02 - Derivatives|ch. 02]] does the same job with the definition in hand.

#calculus #functions #limits #continuity #squeeze-theorem #intermediate-value-theorem #asymptotes #epsilon-delta
