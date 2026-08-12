---
subject: Calculus
chapter: 04
tags: [ds, calculus, integral, riemann-sum, fundamental-theorem, substitution, net-change, average-value]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 5 (pp. 371–434)"
---

# Integrals

> [!abstract] What this chapter is for
> **The integral answers a question that looks nothing like differentiation: how do you add up infinitely many infinitely small things?**
>
> $$\int_a^bf(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^nf(x_i^*)\,\Delta x$$
>
> **Area, distance travelled, total accumulated change, probability, expected value — all are this limit.** And then the chapter's central result says something no one had a right to expect:
>
> $$\boxed{\ \text{integration and differentiation are inverse operations}\ }$$
>
> **The Fundamental Theorem of Calculus is genuinely surprising.** Nothing in "slope of a tangent" and nothing in "area under a curve" suggests the two are related, and for two thousand years nobody knew they were. **It is what turns integration from an intractable limit into a solvable problem.**
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Riemann sums | The definition — and why it is unusable in practice |
> | **2** | The definite integral | Properties, signed area, and what "$dx$" is doing |
> | **3** | **The Fundamental Theorem** | Both halves, and why they are different statements |
> | **4** | Indefinite integrals, net change | $\int_a^bF'=F(b)-F(a)$ — **total change from a rate** |
> | **5** | **Substitution** | The chain rule, run backwards |
>
> **For a data-science reader the payoff is [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]] onward**, where every density integrates to 1, every expectation is an integral, and every one of them is improper.

---

## 📘 Main Knowledge

### 1. Riemann sums and the definite integral

**Partition $[a,b]$ into $n$ subintervals of width $\Delta x=\frac{b-a}{n}$, pick a sample point $x_i^*$ in each, and add up the rectangles:**

$$\sum_{i=1}^n f(x_i^*)\,\Delta x$$

> [!important] Definition
> $$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^n f(x_i^*)\,\Delta x$$
> **when the limit exists and is independent of how the $x_i^*$ are chosen.** Then $f$ is **integrable** on $[a,b]$.
>
> **Every continuous function is integrable**, as is every bounded function with finitely many discontinuities.

> [!example] $\displaystyle\int_0^1x^2\,dx$ from the definition
> With right endpoints $x_i=\frac in$:
> $$\sum_{i=1}^n\left(\frac in\right)^2\frac1n=\frac1{n^3}\sum_{i=1}^ni^2=\frac1{n^3}\cdot\frac{n(n+1)(2n+1)}6=\frac{2n^2+3n+1}{6n^2}$$
> $$\longrightarrow\ \boxed{\tfrac13}\quad\text{as }n\to\infty$$
> *(Verified.)*
>
> **This took a summation formula for $\sum i^2$ and a limit — for one of the simplest possible integrands.** For $\int_0^1 e^{x^2}dx$ there is no such formula, and the definition is simply unusable. **That is the problem the Fundamental Theorem solves.**

> [!important] Properties of the definite integral
> $$\int_a^b(f\pm g)=\int_a^bf\pm\int_a^bg,\qquad \int_a^bcf=c\int_a^bf,\qquad \int_a^bc\,dx=c(b-a)$$
> $$\int_a^cf+\int_c^bf=\int_a^bf,\qquad \int_b^af=-\int_a^bf,\qquad \int_a^af=0$$
> **Comparison:** if $f\ge g$ on $[a,b]$ then $\int_a^bf\ge\int_a^bg$; if $m\le f\le M$ then
> $$m(b-a)\le\int_a^bf\le M(b-a)$$

> [!warning] The integral is **signed** area
> **Area below the $x$-axis counts negative.** So
> $$\int_0^2(x^2-1)\,dx=\tfrac23\qquad\text{but the total area between the curve and the axis is }2$$
> *(Both verified.)* **To get geometric area, integrate $|f|$ — which means splitting at every zero of $f$:**
> $$\int_0^1(1-x^2)\,dx+\int_1^2(x^2-1)\,dx=\tfrac23+\tfrac43=2$$
>
> **"Area" and "integral" are different questions, and the difference is exactly the sign convention.** *(It is also why $\int$ can be zero for a function that is nowhere zero.)*

---

### 2. The Fundamental Theorem of Calculus

> [!important] FTC Part 1 — differentiation undoes integration
> If $f$ is continuous on $[a,b]$, then $\ g(x)=\displaystyle\int_a^xf(t)\,dt$ is continuous on $[a,b]$, differentiable on $(a,b)$, and
> $$\boxed{\ g'(x)=f(x)\ }$$
> **— every continuous function has an antiderivative, namely its own accumulation function.**

> [!important] FTC Part 2 — the evaluation theorem
> If $f$ is continuous on $[a,b]$ and $F$ is **any** antiderivative of $f$, then
> $$\boxed{\ \int_a^bf(x)\,dx=F(b)-F(a)\ }$$

> [!tip] The two halves say different things, and both are needed
> | | Statement | What it gives you |
> |---|---|---|
> | **Part 1** | $\frac{d}{dx}\int_a^xf=f(x)$ | **antiderivatives exist** |
> | **Part 2** | $\int_a^bf=F(b)-F(a)$ | **how to compute** the integral |
>
> **Part 1 is the existence theorem** and is what makes Part 2 non-vacuous: it guarantees there is *something* to find. **Part 2 is what you actually use**, and it converts an infinite limit of sums into a subtraction — provided you can find $F$.
>
> **That proviso is the entire content of [[05 - Techniques of Integration|ch. 05]].** Differentiation is mechanical; its inverse is a search.

> [!example] Part 1 in action — where no antiderivative is available
> $$\frac{d}{dx}\int_1^x\sqrt{1+t^3}\,dt=\sqrt{1+x^3}$$
> **$\sqrt{1+t^3}$ has no elementary antiderivative**, so the integral cannot be evaluated in closed form — **yet its derivative is instant.** *(Attempting the integral symbolically returns hypergeometric functions; the FTC gives the answer in one line.)*
>
> **With a variable upper limit that is itself a function, chain the rule:**
> $$\frac{d}{dx}\int_0^{x^2}\sin t\,dt=\sin(x^2)\cdot2x$$
> *(Verified.)*

> [!example] Part 2 in action
> $$\int_0^1x^2\,dx=\left[\frac{x^3}3\right]_0^1=\tfrac13,\qquad \int_0^\pi\sin x\,dx=\big[-\cos x\big]_0^\pi=2,\qquad \int_1^e\frac{dx}x=\big[\ln x\big]_1^e=1$$
> *(All verified.)* **The first reproduces the Riemann-sum computation of §1 in one line.**

---

### 3. Indefinite integrals and net change

**The indefinite integral is the general antiderivative:**

$$\int f(x)\,dx=F(x)+C\quad\text{means}\quad F'=f$$

> [!warning] Two different objects, one symbol
> | | Object | Answer |
> |---|---|---|
> | $\displaystyle\int_a^bf(x)\,dx$ | **definite** | a **number** |
> | $\displaystyle\int f(x)\,dx$ | **indefinite** | a **family of functions** |
>
> **They are connected only by the FTC**, and confusing them produces the two commonest errors: **forgetting $+C$** on an indefinite integral, and **leaving an $x$ in the answer** to a definite one.

> [!important] The Net Change Theorem
> $$\int_a^bF'(x)\,dx=F(b)-F(a)$$
> **— the integral of a rate of change is the total change.**

> [!tip] This is the reading that makes integration mean something
> | $F'$ is | $\int_a^bF'$ is |
> |---|---|
> | velocity | **displacement** (signed) |
> | speed $=\lvert v\rvert$ | **distance travelled** |
> | marginal cost | total additional cost |
> | rate of water flow | total volume |
> | a probability **density** | a **probability** |
>
> **The velocity/speed pair is the sign convention again**: $\int v$ counts backward motion negatively; $\int|v|$ does not. **Same distinction as area versus signed area.**
>
> **The last row is the one that matters downstream**: a density $f$ is the derivative of the cdf $F$, so $P(a\le X\le b)=\int_a^bf=F(b)-F(a)$ **is the Net Change Theorem** ([[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]]).

> [!important] Average value, and the MVT for integrals
> $$f_{\text{avg}}=\frac1{b-a}\int_a^bf(x)\,dx$$
> and if $f$ is continuous, **$f(c)=f_{\text{avg}}$ for some $c\in[a,b]$.**
>
> **Example:** $x^2$ on $[0,3]$ has average value $\frac13\int_0^3x^2dx=\frac13\cdot9=3$, attained at $c=\sqrt3\approx1.732$. *(Verified.)*
>
> **This is the continuous analogue of an arithmetic mean, and it is exactly $\mathbb{E}[X]$ when $f$ is a density** — the integral $\int xf(x)dx$ of [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]].

---

### 4. The Substitution Rule

> [!important] The rule
> $$\boxed{\ \int f\big(g(x)\big)g'(x)\,dx=\int f(u)\,du\quad\text{where }u=g(x),\ du=g'(x)\,dx\ }$$
> **and for definite integrals, change the limits:**
> $$\int_a^bf\big(g(x)\big)g'(x)\,dx=\int_{g(a)}^{g(b)}f(u)\,du$$

> [!tip] Substitution is the chain rule read backwards
> **The chain rule says $\frac{d}{dx}F(g(x))=F'(g(x))g'(x)$. Substitution says: if you see that pattern, undo it.**
>
> **So the search is always for an inner function whose derivative is also present** (up to a constant). **If it is not present, substitution will not help** — and that is when [[05 - Techniques of Integration|ch. 05]]'s other methods are needed.

> [!example] Three substitutions *(all verified)*
> **Indefinite.** $\displaystyle\int2x\sqrt{1+x^2}\,dx$: take $u=1+x^2$, $du=2x\,dx$:
> $$\int\sqrt u\,du=\tfrac23u^{3/2}+C=\tfrac23(1+x^2)^{3/2}+C$$
>
> **Definite, changing the limits.** $\displaystyle\int_0^2x\sqrt{1+x^2}\,dx$: with $u=1+x^2$, $du=2x\,dx$, and $x=0\mapsto u=1$, $x=2\mapsto u=5$:
> $$\tfrac12\int_1^5\sqrt u\,du=\tfrac12\cdot\tfrac23\left[u^{3/2}\right]_1^5=\tfrac13\left(5\sqrt5-1\right)\approx3.393$$
>
> **A standard one worth knowing.** $\displaystyle\int\tan x\,dx=\int\frac{\sin x}{\cos x}dx$: take $u=\cos x$, $du=-\sin x\,dx$:
> $$-\int\frac{du}u=-\ln|u|+C=-\ln|\cos x|+C=\ln|\sec x|+C$$

> [!warning] Change the limits, or convert back — never neither
> $$\int_0^2x\sqrt{1+x^2}\,dx\ \ne\ \left[\tfrac13(1+u)^{3/2}\right]_0^2$$
> **After substituting, the variable is $u$ and the old limits refer to $x$.** Either
> - **change the limits** to $u$-values (usually cleaner), or
> - **substitute back** to $x$ before evaluating.
>
> **Doing neither is the single most common error in the chapter**, and it produces a wrong number rather than a visible mistake.

> [!important] Symmetry shortcuts
> For $f$ continuous on $[-a,a]$:
> $$f\text{ even}\ \Rightarrow\ \int_{-a}^af=2\int_0^af,\qquad f\text{ odd}\ \Rightarrow\ \int_{-a}^af=0$$
> *(Verified: $\int_{-2}^2x^3dx=0$ and $\int_{-2}^2x^2dx=\tfrac{16}3=2\int_0^2x^2dx$.)*
>
> **Spotting oddness saves the whole computation**, and it is used constantly in probability — every odd moment of a symmetric distribution vanishes for exactly this reason.

---

## ✏️ Exercises

> [!question] Exercise 1 — the definition and basic evaluation *(warm-up)*
> (i) Compute $\int_0^1x^2\,dx$ from the Riemann-sum definition, using $\sum_{i=1}^ni^2=\frac{n(n+1)(2n+1)}6$.
> (ii) Evaluate the same integral by the FTC.
> (iii) Evaluate $\int_0^\pi\sin x\,dx$ and $\int_1^e\frac{dx}{x}$.
> (iv) Explain why the answer to (i) took a page and (ii) took a line.

> [!example]- Solution
> **(i)** With $\Delta x=\frac1n$ and right endpoints $x_i=\frac in$:
> $$\sum_{i=1}^n\left(\frac in\right)^2\frac1n=\frac1{n^3}\cdot\frac{n(n+1)(2n+1)}{6}=\frac{2n^2+3n+1}{6n^2}$$
> $$\lim_{n\to\infty}\frac{2n^2+3n+1}{6n^2}=\frac{2}{6}=\boxed{\tfrac13}$$
> *(Verified.)*
>
> **(ii)** $\displaystyle\int_0^1x^2dx=\left[\frac{x^3}{3}\right]_0^1=\tfrac13-0=\boxed{\tfrac13}$ ✓
>
> **(iii)** $\big[-\cos x\big]_0^\pi=-(-1)-(-1)=\boxed{2}$ and $\big[\ln x\big]_1^e=1-0=\boxed{1}$. *(Both verified.)*
>
> **(iv)** **Because the FTC replaced a limit of sums with a subtraction.**
>
> Method (i) needed a closed form for $\sum i^2$ — **and no such formula exists for $\sum e^{(i/n)^2}$, or for most integrands.** The definition is a *definition*, not a method.
>
> **This is the whole reason the FTC is called fundamental.** It is not that it makes the computation shorter; it is that it makes an entire class of computations *possible*.

> [!question] Exercise 2 — the Fundamental Theorem, Part 1
> Differentiate.
> (i) $\displaystyle g(x)=\int_1^x\sqrt{1+t^3}\,dt$
> (ii) $\displaystyle h(x)=\int_0^{x^2}\sin t\,dt$
> (iii) $\displaystyle k(x)=\int_x^5 e^{t^2}\,dt$
> (iv) $\displaystyle m(x)=\int_{x}^{x^2}\frac{dt}{t}$ — **and check your answer by evaluating the integral first.**

> [!example]- Solution
> **(i)** Directly by FTC 1: $\ g'(x)=\boxed{\sqrt{1+x^3}}$
>
> **$\sqrt{1+t^3}$ has no elementary antiderivative** — attempting the integral symbolically produces hypergeometric functions. **The derivative is nonetheless immediate**, which is precisely what FTC 1 is for.
>
> **(ii)** Variable limit $u=x^2$, so chain: $\ h'(x)=\sin(x^2)\cdot2x=\boxed{2x\sin(x^2)}$ *(verified)*
>
> **(iii)** The variable is the **lower** limit. Flip it:
> $$k(x)=-\int_5^xe^{t^2}dt\ \Longrightarrow\ k'(x)=\boxed{-e^{x^2}}$$
> **The minus sign is the whole exercise**, and it comes from $\int_b^a=-\int_a^b$.
>
> **(iv)** Split at any convenient point, say 1:
> $$m(x)=\int_x^1\frac{dt}t+\int_1^{x^2}\frac{dt}t=-\int_1^x\frac{dt}t+\int_1^{x^2}\frac{dt}t$$
> $$m'(x)=-\frac1x+\frac1{x^2}\cdot2x=-\frac1x+\frac2x=\boxed{\frac1x}$$
>
> **Check by evaluating first:** $m(x)=\big[\ln|t|\big]_x^{x^2}=\ln x^2-\ln x=2\ln x-\ln x=\ln x$, and $\frac{d}{dx}\ln x=\frac1x$ ✓
>
> **The general rule, worth extracting:**
> $$\frac{d}{dx}\int_{a(x)}^{b(x)}f(t)\,dt=f\big(b(x)\big)b'(x)-f\big(a(x)\big)a'(x)$$

> [!question] Exercise 3 — substitution
> Evaluate.
> (i) $\displaystyle\int2x\sqrt{1+x^2}\,dx$
> (ii) $\displaystyle\int_0^1xe^{x^2}\,dx$
> (iii) $\displaystyle\int\tan x\,dx$
> (iv) $\displaystyle\int_0^2x\sqrt{1+x^2}\,dx$ — **by changing the limits, and again by substituting back.**
> (v) Why does $u=x^2$ fail for $\displaystyle\int\sqrt{1+x^2}\,dx$?

> [!example]- Solution
> **(i)** $u=1+x^2$, $du=2x\,dx$:
> $$\int\sqrt u\,du=\tfrac23u^{3/2}+C=\boxed{\tfrac23(1+x^2)^{3/2}+C}$$
> *(Verified.)*
>
> **(ii)** $u=x^2$, $du=2x\,dx$, and $x:0\to1$ gives $u:0\to1$:
> $$\tfrac12\int_0^1e^u\,du=\tfrac12\big[e^u\big]_0^1=\boxed{\frac{e-1}{2}\approx0.859}$$
> *(Verified.)*
>
> **(iii)** $u=\cos x$, $du=-\sin x\,dx$:
> $$\int\frac{\sin x}{\cos x}dx=-\int\frac{du}{u}=-\ln|u|+C=\boxed{-\ln|\cos x|+C}$$
> *(Verified.)*
>
> **(iv) Changing the limits.** $u=1+x^2$; $x=0\mapsto u=1$, $x=2\mapsto u=5$:
> $$\tfrac12\int_1^5u^{1/2}du=\tfrac13\big[u^{3/2}\big]_1^5=\tfrac13\left(5\sqrt5-1\right)\approx3.393$$
>
> **Substituting back.** The antiderivative is $\tfrac13(1+x^2)^{3/2}$, so
> $$\tfrac13\big[(1+x^2)^{3/2}\big]_0^2=\tfrac13\left(5^{3/2}-1\right)=\tfrac13\left(5\sqrt5-1\right)$$
> **Same answer** ✓ *(verified)*.
>
> **Changing the limits is usually better** — it avoids re-expressing a possibly messy antiderivative, and it makes it impossible to forget which variable the limits belong to.
>
> **(v)** With $u=x^2$ we would need $du=2x\,dx$, **but there is no $x$ factor in $\int\sqrt{1+x^2}\,dx$.**
>
> **Substitution requires the inner function's derivative to be present** (up to a constant). Here it is not, and no amount of rearranging will produce it. **This integral needs trigonometric substitution** ([[05 - Techniques of Integration|ch. 05]]) — the presence or absence of that $x$ is the entire difference between (i) and (v).

> [!question] Exercise 4 — net change, area, and symmetry
> (i) A particle has velocity $v(t)=t^2-4$ m/s for $0\le t\le3$. Find its **displacement** and the **distance travelled**.
> (ii) Find the area between $y=x^2-1$ and the $x$-axis on $[0,2]$, and compare with $\int_0^2(x^2-1)dx$.
> (iii) Evaluate $\int_{-2}^2x^3\,dx$ and $\int_{-2}^2x^2\,dx$ using symmetry.
> (iv) Find the average value of $f(x)=x^2$ on $[0,3]$ and the point where it is attained.

> [!example]- Solution
> **(i)** **Displacement** is the signed integral:
> $$\int_0^3(t^2-4)\,dt=\left[\frac{t^3}3-4t\right]_0^3=9-12=\boxed{-3\ \text{m}}$$
> **Distance travelled** integrates $|v|$. Since $v<0$ on $[0,2)$ and $v>0$ on $(2,3]$:
> $$\int_0^2(4-t^2)dt+\int_2^3(t^2-4)dt=\left(8-\tfrac83\right)+\left(\tfrac{19}3-4\right)=\tfrac{16}3+\tfrac73=\boxed{\tfrac{23}3\approx7.67\ \text{m}}$$
>
> **The particle went backwards $\tfrac{16}3$ m, then forwards $\tfrac73$ m, ending 3 m behind where it started.** **Displacement and distance are genuinely different questions**, and only one of them is an ordinary integral.
>
> **(ii)** $\int_0^2(x^2-1)dx=\tfrac83-2=\boxed{\tfrac23}$, while the **area** is
> $$\int_0^1(1-x^2)dx+\int_1^2(x^2-1)dx=\tfrac23+\tfrac43=\boxed{2}$$
> *(Both verified.)* **The curve is below the axis on $[0,1]$, and the integral subtracts that part while the area adds it.**
>
> **(iii)** $x^3$ is **odd**, so $\int_{-2}^2x^3dx=\boxed{0}$ with no computation.
> $x^2$ is **even**, so $\int_{-2}^2x^2dx=2\int_0^2x^2dx=2\cdot\tfrac83=\boxed{\tfrac{16}3}$. *(Both verified.)*
>
> **Checking parity before integrating is free and frequently decisive.** In probability it is why every odd central moment of a symmetric distribution is zero — including the skewness.
>
> **(iv)** $$f_{\text{avg}}=\frac1{3-0}\int_0^3x^2dx=\frac13\cdot9=\boxed{3}$$
> attained where $c^2=3$, i.e. $c=\sqrt3\approx1.732$ *(verified)*.
>
> **Note $\sqrt3>1.5$: the average is attained past the midpoint**, because $x^2$ grows faster later. **The average value is not the value at the average point** — a distinction that is exactly Jensen's inequality ([[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]]).

> [!question] Exercise 5 — what the FTC does and does not give *(hard)*
> (a) (i) Define $E(x)=\int_0^xe^{-t^2}dt$. Show $E$ is increasing and concave down for $x>0$, and find $E'(0)$ and $E''(x)$.
> (ii) Why can $E$ not be written with elementary functions, and does that stop you analysing it?
>
> (b) (i) A student writes $\int_{-1}^1\frac{dx}{x^2}=\left[-\frac1x\right]_{-1}^1=-1-1=-2$. **Find the error.**
> (ii) What is the correct answer?
>
> (c) Prove the Net Change Theorem is equivalent to FTC Part 2.

> [!example]- Solution
> **(a)(i)** By FTC 1, $E'(x)=e^{-x^2}$.
> - **$E'>0$ everywhere**, so $E$ is increasing on all of $\mathbb{R}$.
> - $E'(0)=e^0=\boxed{1}$.
> - $E''(x)=\dfrac{d}{dx}e^{-x^2}=\boxed{-2xe^{-x^2}}$, which is **negative for $x>0$** — so $E$ is concave down there (and concave up for $x<0$, with an **inflection at $0$**).
>
> **(ii)** **$e^{-t^2}$ has no elementary antiderivative** — this is a theorem (Liouville), not a failure of ingenuity.
>
> **And it stops nothing.** From $E'=e^{-x^2}$ alone we obtained monotonicity, concavity, the inflection point, and the tangent slope at 0. **We can also bound it, expand it as a series ([[06 - Sequences, Series and Taylor Approximation|ch. 06]]), and integrate it numerically ([[05 - Techniques of Integration|ch. 05]]).**
>
> **$E$ is, up to scaling, the error function** — and $\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x}e^{-t^2/2}dt$ is the standard normal cdf $\Phi$. **Every $\Phi$ value in [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]] is a numerically-evaluated instance of this integral**, which is exactly why normal tables exist.
>
> **(b)(i)** **$\frac1{x^2}$ is not continuous on $[-1,1]$ — it blows up at $x=0$, which is inside the interval.** FTC Part 2 requires continuity on the closed interval, so **the theorem simply does not apply.**
>
> **The answer $-2$ is visibly absurd on its own terms:** $\frac1{x^2}>0$ everywhere it is defined, so any sensible notion of the integral must be positive. **A negative answer to a positive integrand is the diagnostic.**
>
> **(ii)** The integral is **improper** and must be split at the singularity:
> $$\int_{-1}^1\frac{dx}{x^2}=\lim_{b\to0^-}\int_{-1}^b\frac{dx}{x^2}+\lim_{a\to0^+}\int_a^1\frac{dx}{x^2}$$
> Each piece diverges: $\int_a^1x^{-2}dx=\frac1a-1\to+\infty$. **So the integral diverges — it does not exist.** *(Improper integrals are [[05 - Techniques of Integration|ch. 05 §5]].)*
>
> **(c)** The two are the same statement read in opposite directions.
>
> **FTC 2 $\Rightarrow$ Net Change:** given $F$, set $f=F'$. Then $F$ is an antiderivative of $f$, so FTC 2 gives $\int_a^bF'=\int_a^bf=F(b)-F(a)$.
>
> **Net Change $\Rightarrow$ FTC 2:** given $f$ continuous and $F$ any antiderivative, then $F'=f$, so Net Change gives $F(b)-F(a)=\int_a^bF'=\int_a^bf$. $\blacksquare$
>
> > [!important] Why the same theorem is stated twice
> > **The two versions have different *inputs*.** FTC 2 starts from a function you want to integrate and looks for an antiderivative. **Net Change starts from a rate you already have** — velocity, marginal cost, a density — and asks for the accumulated total.
> >
> > **Almost every application is the second kind**, which is why Stewart states it separately even though it is mathematically identical. **In [[Probability Theory/contents/05 - Continuous Random Variables|probability]] the density *is* the rate and the cdf *is* the accumulation**, so $P(a\le X\le b)=F(b)-F(a)$ is nothing but the Net Change Theorem.

---

## 📝 Summary

- **The definite integral is a limit of Riemann sums** $\sum f(x_i^*)\Delta x$, and **every continuous function is integrable.** Computing one from the definition requires a closed form for the sum, which almost never exists — **so the definition is a definition, not a method.**
- **The integral is *signed* area.** For geometric area, split at the zeros of $f$ and integrate $|f|$: $\int_0^2(x^2-1)dx=\tfrac23$ while the area is $2$.
- **FTC Part 1: $\frac{d}{dx}\int_a^xf=f(x)$** — every continuous function has an antiderivative. **FTC Part 2: $\int_a^bf=F(b)-F(a)$** — an infinite limit becomes a subtraction. **Part 1 is existence, Part 2 is computation, and both are needed.**
- **With a variable limit, chain:** $\frac{d}{dx}\int_{a(x)}^{b(x)}f=f(b(x))b'(x)-f(a(x))a'(x)$. **A variable *lower* limit contributes a minus sign.**
- **FTC 1 works even when no elementary antiderivative exists** — $\frac{d}{dx}\int_1^x\sqrt{1+t^3}\,dt=\sqrt{1+x^3}$ is immediate although the integral is not elementary.
- **The definite integral is a number; the indefinite integral is a family of functions.** Forgetting $+C$ and leaving an $x$ in a definite answer are the two errors this distinction prevents.
- **Net Change Theorem: $\int_a^bF'=F(b)-F(a)$** — the integral of a rate is the total change. **Velocity $\to$ displacement, speed $\to$ distance, density $\to$ probability.**
- **Average value $f_{\text{avg}}=\frac1{b-a}\int_a^bf$ is attained somewhere** (MVT for integrals), **but not at the midpoint** — for $x^2$ on $[0,3]$ it is at $\sqrt3$, not $1.5$.
- **Substitution is the chain rule backwards:** look for an inner function whose derivative is also present. **If it is not present, substitution cannot work** — which is exactly the difference between $\int2x\sqrt{1+x^2}dx$ and $\int\sqrt{1+x^2}dx$.
- **For definite integrals, change the limits or substitute back — never neither.**
- **Symmetry is free:** odd integrands vanish on symmetric intervals, even ones double.
- **FTC 2 requires continuity on the closed interval.** Applying it across a singularity gives a confidently wrong answer — $\int_{-1}^1x^{-2}dx$ "$=-2$" for a strictly positive integrand.

---

## ⚠️ Important Notes

> [!warning] Signed area is not area
> $$\int_a^bf\ \text{counts area below the axis as negative}$$
> **A nowhere-zero function can have integral zero** ($\int_{-1}^1x\,dx=0$ has integrand vanishing only at one point; $\int_0^{2\pi}\sin x\,dx=0$ with $\sin$ vanishing only three times).
>
> **For geometric area, find the zeros, split, and integrate $|f|$.** The same distinction is displacement versus distance, and net change versus gross change.

> [!warning] Definite and indefinite integrals are different objects
> | Error | Looks like |
> |---|---|
> | forgetting $+C$ | $\int2x\,dx=x^2$ |
> | leaving $x$ in a definite answer | $\int_0^1 2x\,dx=x^2$ |
>
> **The first loses every solution but one** — fatal in a differential equation, where $C$ carries the initial condition. **The second is dimensionally incoherent**: a definite integral is a number.

> [!warning] Change the limits when you substitute
> $$\int_0^2x\sqrt{1+x^2}\,dx\ \xrightarrow{\ u=1+x^2\ }\ \tfrac12\int_{\mathbf 1}^{\mathbf 5}\sqrt u\,du$$
> **The limits $0$ and $2$ were $x$-values; after substituting, the variable is $u$.**
>
> **Two legitimate options: change the limits (cleaner) or convert back to $x$ before evaluating.** Doing neither gives a wrong *number*, with nothing visibly wrong on the page.

> [!warning] FTC Part 2 needs continuity on the whole closed interval
> $$\int_{-1}^1\frac{dx}{x^2}\ \text{“}=-2\text{”}$$
> is wrong because $\frac1{x^2}$ is undefined at $0$, which lies inside $[-1,1]$. **The correct answer is that the integral diverges.**
>
> **The diagnostic is worth internalising: a positive integrand cannot have a negative integral.** Before applying the FTC, **check the integrand is defined and continuous throughout** — and if it is not, the integral is improper ([[05 - Techniques of Integration|ch. 05]]).

> [!warning] Not every integral has an elementary antiderivative
> $$\int e^{-x^2}dx,\qquad \int\frac{\sin x}{x}dx,\qquad \int\sqrt{1+x^3}\,dx,\qquad \int\frac{dx}{\ln x}$$
> **None of these can be written with elementary functions** — a theorem, not a shortage of cleverness.
>
> **This does not make them intractable.** FTC 1 gives their derivatives; series give their values ([[06 - Sequences, Series and Taylor Approximation|ch. 06]]); numerical methods give their numbers ([[05 - Techniques of Integration|ch. 05]]). **The first of them is the normal distribution**, which is used constantly and tabulated precisely because it cannot be evaluated in closed form.

> [!note] Cross-subject connections
> - [[02 - Derivatives|Ch. 02]] — **substitution is the chain rule backwards**; the FTC says the two operations are inverse.
> - [[03 - Applications of Differentiation|Ch. 03]] — the **MVT** is what makes "$+C$" the complete answer, and antiderivative tables are shared.
> - [[05 - Techniques of Integration|Ch. 05]] — the search for antiderivatives that FTC 2 requires, plus **improper integrals**, which Exercise 5(b) needs.
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — series evaluate the integrals no antiderivative can; the integral test for convergence runs the other way.
> - [[09 - Multiple Integrals and Change of Variables|Ch. 09]] — Riemann sums in two and three dimensions, with **substitution becoming the Jacobian.**
> - [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]] — **a density is a rate and the cdf its accumulation**, so $P(a\le X\le b)=F(b)-F(a)$ **is** the Net Change Theorem; $\mathbb{E}[X]=\int xf(x)dx$ is an average value; **and $\Phi$ is Exercise 5(a)'s non-elementary integral.**
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — every normal-table lookup evaluates $\int e^{-t^2/2}dt$ numerically.
> - [[Econometrics/contents/00-Index|Econometrics]] — consumer surplus, cumulative impulse responses and integrated processes are all net-change integrals.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **This chapter suffers a specific new failure: integral signs and their limits detach completely.** A displayed $\int_a^b f(x)\,dx$ extracts as `y` on one line, `b` and `a` on others, and `f sxd dx` on a fourth — **so the limits of integration must be inferred from position, and in a page with several integrals they interleave.** **Every integral quoted in these notes was recomputed symbolically rather than read off.**
>
> **Figures lost — and in this chapter one of them is the argument.** Gone entirely: **the Riemann-sum rectangle pictures** (§5.1–5.2), which are how the definition is motivated and the only reason "$\sum f(x_i^*)\Delta x$" means anything; the **area-function animation** of the §5.2 Discovery Project, which is the visual proof of FTC 1; every **signed-area diagram** showing regions above and below the axis; and the velocity-versus-time graphs of §5.4 that distinguish displacement from distance. **The Riemann-sum picture in particular has no adequate verbal substitute** — I have given the algebra and the limit, but the image of rectangles filling a region under a curve is what makes the definition obvious rather than arbitrary.
>
> **Verification performed:** every integral, sum and numerical value in this chapter was computed symbolically with `sympy`. Confirmed: the Riemann sum $\frac{2n^2+3n+1}{6n^2}\to\tfrac13$ **and its agreement with the FTC evaluation**; $\int_0^\pi\sin=2$ and $\int_1^e\frac{dx}x=1$; $\frac{d}{dx}\int_0^{x^2}\sin t\,dt=2x\sin(x^2)$; all three substitutions, with the definite one $\tfrac13(5\sqrt5-1)\approx3.393$ **checked both by changing the limits and by substituting back**; **the signed integral $\tfrac23$ against the true area $2$ for $x^2-1$ on $[0,2]$**; the displacement $-3$ and distance $\tfrac{23}3$ in Exercise 4(i); both symmetry results; and the average value $3$ attained at $\sqrt3$. **No error was found in the text's mathematics.**
>
> **Scope note:** **§5.1 (the area and distance problems) is compressed**, since its content is the motivation for a definition given fully in §5.2, and its value was almost entirely in the figures. **Stewart's ch. 6 (Applications of Integration) is excluded from these notes altogether** — see [[00-Index]] — **but §6.1 (areas between curves) is folded into §1 and Exercise 4 above**, because the area-versus-signed-area distinction genuinely belongs with the definition rather than in a later applications chapter.

#calculus #integral #riemann-sum #fundamental-theorem #substitution #net-change #average-value #signed-area
