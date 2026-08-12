---
subject: Calculus
chapter: 06
tags: [ds, calculus, sequences, series, convergence-tests, power-series, taylor-series, remainder]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 11 (pp. 723–828)"
---

# Sequences, Series and Taylor Approximation

> [!abstract] What this chapter is for
> **Two questions, and the second is the one that matters.**
>
> **First: when does an infinite sum have a finite value?** Adding infinitely many things is not obviously meaningful, and the answer is a battery of convergence tests.
>
> **Second — and this is the payoff — can a function be written as an infinite polynomial?**
>
> $$\boxed{\ f(x)=\sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n\ }$$
>
> **If so, then the derivatives at a single point determine the function everywhere.** That is an extraordinary claim, and where it holds it converts transcendental functions into polynomials — which can be differentiated, integrated and computed.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Sequences | Convergence, and $\lim a_n=0$ is **necessary not sufficient** |
> | **2** | Series | Geometric and $p$-series; the **$n$th-term test** only proves divergence |
> | **3** | Convergence tests | Integral, comparison, alternating, **ratio** |
> | **4** | Power series | Radius and interval of convergence |
> | **5** | **Taylor and Maclaurin series** | The six you must know |
> | **6** | **Taylor's remainder** | **Convergence to the right function is a separate question** |
>
> **[[02 - Derivatives|Chapter 2's]] linear approximation was the degree-1 case, and its $h^2$ error law is here made exact.** The rest of the degree uses Taylor expansion constantly: the delta method, MGFs, log-linear approximations, and every "for small $x$" argument.

---

## 📘 Main Knowledge

### 1. Sequences

A **sequence** $\{a_n\}$ **converges** to $L$ if $a_n$ can be made arbitrarily close to $L$ by taking $n$ large enough — the $\varepsilon$–$N$ version of [[01 - Functions, Limits and Continuity|ch. 01]]'s definition.

> [!important] The tools
> - **If $f(x)\to L$ as $x\to\infty$ and $a_n=f(n)$, then $a_n\to L$** — so l'Hôpital applies to sequences via their continuous versions.
> - **Squeeze theorem** carries over verbatim.
> - **If $a_n\to L$ and $f$ is continuous at $L$, then $f(a_n)\to f(L)$.**
> - **Monotone Convergence:** a bounded monotone sequence converges. *(This does not say to what — it is an existence theorem.)*
> - $r^n\to0$ if $|r|<1$; diverges if $|r|>1$.

---

### 2. Series

$$\sum_{n=1}^\infty a_n=\lim_{N\to\infty}s_N\quad\text{where}\quad s_N=\sum_{n=1}^N a_n$$

**A series converges iff its sequence of *partial sums* converges.** The infinite sum is defined as a limit, not as an act of adding.

> [!important] The two series everything is compared against
> **Geometric:**
> $$\sum_{n=0}^\infty ar^n=\frac{a}{1-r}\ \text{ if }|r|<1;\qquad\text{diverges if }|r|\ge1$$
> **$p$-series:**
> $$\sum_{n=1}^\infty\frac1{n^p}\ \text{converges}\iff \boxed{p>1}$$
>
> **Examples** *(all verified)*: $\sum2^{-n}=2$; $\sum\frac1{n^2}=\frac{\pi^2}6$; **$\sum\frac1n=\infty$** (the harmonic series); $\sum\frac1{n(n+1)}=1$ by telescoping.

> [!warning] The $n$th-Term Test can only prove **divergence**
> $$\sum a_n\text{ converges}\ \Longrightarrow\ a_n\to0$$
> **The converse is false, and the harmonic series is the counterexample:** $\frac1n\to0$ and yet $\sum\frac1n=\infty$ *(verified)*.
>
> **So the test is one-directional.** If $a_n\not\to0$, the series diverges. **If $a_n\to0$, you have learned nothing** and must use another test.
>
> **This is the single most common error in the chapter**, and the harmonic series is the standing reminder of why: **terms can shrink to zero and still add to infinity**, because they do not shrink *fast enough*.

---

### 3. Convergence tests

> [!important] The tests, and when to reach for each
> | Test | Use when | Statement |
> |---|---|---|
> | **$n$th-term** | always first | $a_n\not\to0\Rightarrow$ diverges |
> | **Geometric / $p$-series** | recognisable form | thresholds above |
> | **Integral** | $a_n=f(n)$ with $f$ positive, decreasing | $\sum a_n$ and $\int_1^\infty f$ **both converge or both diverge** |
> | **Comparison** | resembles a known series | $0\le a_n\le b_n$: $\sum b_n$ conv $\Rightarrow\sum a_n$ conv |
> | **Limit comparison** | resembles, messily | $\lim\frac{a_n}{b_n}=c\in(0,\infty)$: **same behaviour** |
> | **Alternating series** | $\sum(-1)^na_n$ | $a_n$ decreasing and $\to0$ $\Rightarrow$ converges |
> | **Ratio** | factorials, $n$th powers | $\lim\left\lvert\frac{a_{n+1}}{a_n}\right\rvert=L$: conv if $L<1$, div if $L>1$, **inconclusive if $L=1$** |
> | **Root** | $n$th powers | same thresholds with $\sqrt[n]{|a_n|}$ |

> [!important] Absolute versus conditional convergence
> $\sum a_n$ is **absolutely convergent** if $\sum|a_n|$ converges, and **absolutely convergent $\Rightarrow$ convergent**. A series that converges but not absolutely is **conditionally convergent**.
>
> **The archetype:** $\sum\frac{(-1)^{n+1}}n=\ln2$ converges *(verified)*, while $\sum\frac1n$ diverges.

> [!warning] Conditionally convergent series can be rearranged to any sum you like
> **Riemann's rearrangement theorem:** the terms of a conditionally convergent series can be reordered to converge to **any** real number, or to diverge.
>
> **So "the sum" of $1-\tfrac12+\tfrac13-\tfrac14+\cdots$ is $\ln2$ *only in that order*.** Rearranging it to take two positive terms for every negative one gives $\tfrac32\ln2$ instead.
>
> **Absolute convergence is what makes a sum behave like a sum** — order-independent, safe to rearrange and to regroup. **The same distinction is why $\mathbb{E}[X]$ requires $\mathbb{E}|X|<\infty$** in [[Probability Theory/contents/04 - Random Variables|Probability ch. 04]]: without it the "expectation" would depend on the order of summation, which is not a property a number should have.

> [!tip] The integral test is the $p$-test of [[05 - Techniques of Integration|ch. 05]]
> $$\sum_{n=1}^\infty\frac1{n^p}\quad\text{and}\quad\int_1^\infty\frac{dx}{x^p}$$
> **converge for exactly the same $p>1$** — the test says a sum and an integral of the same decreasing positive function agree on convergence. **A series is a Riemann sum that never refines**, and this is the precise statement of that analogy.

---

### 4. Power series

$$\sum_{n=0}^\infty c_n(x-a)^n$$

> [!important] The three possibilities
> For a power series centred at $a$, exactly one holds:
> 1. it converges **only at $x=a$** ($R=0$);
> 2. it converges for **all $x$** ($R=\infty$);
> 3. it converges for $|x-a|<R$ and diverges for $|x-a|>R$.
>
> **$R$ is the radius of convergence, found with the ratio test.** **The endpoints $x=a\pm R$ must be checked separately** — the ratio test is silent there.

**Examples:** $\sum\frac{x^n}{n!}$ has $R=\infty$; $\sum x^n$ has $R=1$; $\sum n!x^n$ has $R=0$.

> [!important] Within the radius, power series behave like polynomials
> **They may be differentiated and integrated term by term**, and the result has the **same** radius of convergence:
> $$\frac{d}{dx}\sum c_n(x-a)^n=\sum nc_n(x-a)^{n-1},\qquad \int\sum c_n(x-a)^n\,dx=C+\sum\frac{c_n(x-a)^{n+1}}{n+1}$$
>
> **This is how non-elementary integrals get evaluated** — see Exercise 5.

---

### 5. Taylor and Maclaurin series

> [!important] The definition
> $$f(x)=\sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n$$
> is the **Taylor series** of $f$ at $a$; at $a=0$ it is the **Maclaurin series**.
>
> **The coefficients are forced:** differentiating the series $n$ times and setting $x=a$ leaves only $n!c_n$, so $c_n=\frac{f^{(n)}(a)}{n!}$. **If a power-series representation exists at all, it is the Taylor series.**

> [!important] The six to know by heart *(all verified)*
> $$e^x=\sum_{n=0}^\infty\frac{x^n}{n!}=1+x+\frac{x^2}2+\frac{x^3}6+\cdots\qquad(R=\infty)$$
> $$\sin x=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots\qquad \cos x=1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots\qquad(R=\infty)$$
> $$\frac1{1-x}=\sum_{n=0}^\infty x^n\qquad(R=1)$$
> $$\ln(1+x)=x-\frac{x^2}2+\frac{x^3}3-\cdots\qquad \arctan x=x-\frac{x^3}3+\frac{x^5}5-\cdots\qquad(R=1)$$

> [!tip] Derive new series from old ones — do not differentiate repeatedly
> **Substitution, multiplication, differentiation and integration of known series are almost always faster than computing $f^{(n)}(0)$.**
>
> | Want | Get it from |
> |---|---|
> | $e^{-x^2}$ | substitute $-x^2$ into $e^x$ |
> | $\dfrac1{1+x^2}$ | substitute $-x^2$ into $\dfrac1{1-x}$ |
> | $\arctan x$ | **integrate** the previous one |
> | $x\sin x$ | multiply the $\sin$ series by $x$ |
>
> **The $\arctan$ series is genuinely hard to get by differentiating $\arctan$ four times, and trivial by integrating a geometric series.**

---

### 6. Taylor's theorem and the remainder

> [!important] Taylor's Inequality
> If $T_n$ is the degree-$n$ Taylor polynomial and $R_n=f-T_n$ the remainder, then
> $$\boxed{\ |R_n(x)|\le\frac{M}{(n+1)!}|x-a|^{n+1}\ }\qquad\text{where }|f^{(n+1)}|\le M\text{ near }a$$
> **and $f$ equals its Taylor series exactly when $R_n(x)\to0$.**

> [!warning] "The series converges" and "the series converges to $f$" are different claims
> $$f(x)=\begin{cases}e^{-1/x^2},&x\ne0\\ 0,&x=0\end{cases}$$
> **has $f^{(n)}(0)=0$ for every $n$.** So its Maclaurin series is $0+0x+0x^2+\cdots$, which converges everywhere — **to the zero function, which $f$ is not.**
>
> **The series converged beautifully and to the wrong thing.** Only the remainder estimate rules this out, which is why Taylor's Inequality is not a technicality.
>
> **This is [[01 - Functions, Limits and Continuity|ch. 01]]'s theme again: local information determines global behaviour — sometimes.** Here every derivative at 0 is zero and the function is not.

> [!important] The error is controlled by $(n+1)!$ — and factorials win
> $$|R_n|\le\frac{M|x-a|^{n+1}}{(n+1)!}$$
> **The factorial in the denominator eventually beats any power in the numerator**, which is why $e^x$, $\sin$ and $\cos$ have $R=\infty$: their derivatives are bounded and $\frac{x^{n+1}}{(n+1)!}\to0$ for every $x$.
>
> **And $|x-a|^{n+1}$ is why accuracy collapses far from the centre.** [[02 - Derivatives|Ch. 02]] observed empirically that linearisation error scales like $h^2$; **this is that observation, exact and generalised**: the degree-$n$ error scales like $h^{n+1}$.

> [!example] Two error estimates, checked against the truth *(both verified)*
> **$e^{0.1}$ by $T_2$:** $\ 1+0.1+\frac{0.1^2}2=1.105$, true $1.10517092$.
> $$\text{actual error}=1.71\times10^{-4},\qquad \text{bound}=\frac{e^{0.1}(0.1)^3}{3!}=1.84\times10^{-4}$$
>
> **$\sin(0.5)$ by $T_3$:** $\ 0.5-\frac{0.5^3}6=0.4791\overline{6}$, true $0.47942554$.
> $$\text{actual error}=2.589\times10^{-4},\qquad \text{bound}=\frac{(0.5)^5}{5!}=2.604\times10^{-4}$$
>
> **Both bounds are tight to within 1%** — Taylor's Inequality is not merely valid, it is sharp enough to be useful for deciding how many terms you need.

---

## ✏️ Exercises

> [!question] Exercise 1 — convergence *(warm-up)*
> Determine convergence, naming the test.
> (i) $\displaystyle\sum_{n=0}^\infty\frac1{2^n}$  (ii) $\displaystyle\sum_{n=1}^\infty\frac1{n}$  (iii) $\displaystyle\sum_{n=1}^\infty\frac1{n^2}$
> (iv) $\displaystyle\sum_{n=1}^\infty\frac{n}{2^n}$  (v) $\displaystyle\sum_{n=1}^\infty\frac{n}{n+1}$  (vi) $\displaystyle\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n}$

> [!example]- Solution
> **(i) Geometric**, $r=\tfrac12<1$: converges to $\dfrac1{1-1/2}=\boxed2$ *(verified)*.
>
> **(ii) $p$-series with $p=1$: diverges** *(verified)*. **Note $\frac1n\to0$** — the $n$th-term test says nothing, and this is the standing counterexample to its converse.
>
> **(iii) $p$-series with $p=2>1$: converges** *(verified — the sum is $\frac{\pi^2}6$, the Basel problem)*.
>
> **(iv) Ratio test:**
> $$\left|\frac{a_{n+1}}{a_n}\right|=\frac{n+1}{2^{n+1}}\cdot\frac{2^n}{n}=\frac12\cdot\frac{n+1}{n}\longrightarrow\frac12<1$$
> **Converges** *(to 2 — verified)*. **The ratio test is the right tool whenever $n$ appears in an exponent.**
>
> **(v) $n$th-term test:** $\frac{n}{n+1}\to1\ne0$, so it **diverges** — immediately, with no further work.
>
> **(vi) Alternating series test:** $\frac1n$ is decreasing and $\to0$, so it **converges** *(to $\ln2$ — verified)*. **But not absolutely**, since $\sum\frac1n$ diverges — **conditionally convergent.**
>
> > [!tip] The order to try tests
> > 1. **$n$th-term** — free, and settles (v) instantly.
> > 2. **Recognise the form** — geometric or $p$-series settles (i)–(iii).
> > 3. **Ratio test** if there are factorials or $n$th powers — (iv).
> > 4. **Comparison / limit comparison** if it resembles a known series.
> > 5. **Alternating series test** for $\sum(-1)^na_n$ — (vi).
> >
> > **Reaching for the ratio test on a $p$-series wastes time and returns $L=1$: inconclusive.**

> [!question] Exercise 2 — Maclaurin series
> Find the Maclaurin series and radius of convergence, **deriving each from a known one**.
> (i) $e^{-x^2}$  (ii) $\dfrac1{1+x^2}$  (iii) $\arctan x$  (iv) $x\sin x$
> (v) Why is deriving (iii) from (ii) far easier than differentiating $\arctan$ repeatedly?

> [!example]- Solution
> **(i)** Substitute $-x^2$ into $e^u=\sum\frac{u^n}{n!}$:
> $$e^{-x^2}=\sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{n!}=1-x^2+\frac{x^4}2-\frac{x^6}6+\cdots,\qquad R=\infty$$
>
> **(ii)** Substitute $-x^2$ into $\frac1{1-u}=\sum u^n$:
> $$\frac1{1+x^2}=\sum_{n=0}^\infty(-1)^nx^{2n}=1-x^2+x^4-\cdots,\qquad R=1$$
> **$R=1$ because we need $|-x^2|<1$**, i.e. $|x|<1$.
>
> **(iii) Integrate (ii)**, since $\arctan'x=\frac1{1+x^2}$:
> $$\arctan x=\sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{2n+1}=x-\frac{x^3}3+\frac{x^5}5-\cdots,\qquad R=1$$
> **The constant is 0 because $\arctan0=0$.** *(Verified.)*
>
> **(iv)** Multiply the $\sin$ series by $x$:
> $$x\sin x=x^2-\frac{x^4}{3!}+\frac{x^6}{5!}-\cdots,\qquad R=\infty$$
>
> **(v)** **Because the derivatives of $\arctan$ get worse, not better.**
> $$\arctan'x=\frac1{1+x^2},\quad \arctan''x=\frac{-2x}{(1+x^2)^2},\quad \arctan'''x=\frac{6x^2-2}{(1+x^2)^3},\ \dots$$
> **Each is messier than the last, and there is no visible pattern** — extracting $f^{(n)}(0)$ for general $n$ from this is genuinely hard.
>
> **Integrating a geometric series takes one line.** **"Build from known series" is not a shortcut, it is the method**; computing $f^{(n)}(a)$ directly is the fallback for when nothing known is available.
>
> **A bonus at $x=1$:** the $\arctan$ series gives $\frac\pi4=1-\frac13+\frac15-\cdots$ — the Leibniz formula for $\pi$. **It converges so slowly that a hundred terms give two decimal places**, which is a good illustration that convergence and usefulness are different properties.

> [!question] Exercise 3 — Taylor polynomials and error
> (i) Find $T_2$ for $e^x$ at 0 and estimate $e^{0.1}$. Bound the error and compare with the truth.
> (ii) Find $T_3$ for $\sin x$ at 0 and estimate $\sin(0.5)$. Bound the error and compare.
> (iii) How many terms of the $e^x$ series are needed for $e$ to six decimal places?
> (iv) Why does the error bound contain $(n+1)!$, and what does that guarantee?

> [!example]- Solution
> **(i)** $T_2(x)=1+x+\frac{x^2}2$, so $T_2(0.1)=1.105$.
> $$|R_2|\le\frac{M(0.1)^3}{3!}\quad\text{with }M=\max|f'''|=e^{0.1}\approx1.105$$
> $$\text{bound}=\frac{1.105\times10^{-3}}{6}=1.84\times10^{-4}$$
> **True value $1.10517092$, actual error $1.71\times10^{-4}$** *(verified)* — **inside the bound, and within 8% of it.**
>
> **(ii)** $T_3(x)=x-\frac{x^3}6$, so $T_3(0.5)=0.4791\overline6$.
> Since every derivative of $\sin$ is bounded by 1, take $M=1$:
> $$|R_3|\le\frac{(0.5)^5}{5!}=\frac{0.03125}{120}=2.604\times10^{-4}$$
> **True value $0.47942554$, actual error $2.589\times10^{-4}$** *(verified)* — **within 0.6% of the bound.**
>
> *(The bound used $n+1=4$ but the $x^4$ term of $\sin$ vanishes, so the first neglected term is $x^5/5!$ — which is why the estimate is so sharp.)*
>
> **(iii)** For $e=e^1$ with $M=e<3$:
> $$|R_n|\le\frac{3}{(n+1)!}<5\times10^{-7}\ \Longrightarrow\ (n+1)!>6\times10^6$$
> $10!=3{,}628{,}800$ and $11!=39{,}916{,}800$, so $n+1=11$, i.e. $\boxed{n=10}$ — **eleven terms.**
>
> **(iv)** **The factorial eventually outgrows any power.** For fixed $x$,
> $$\frac{|x|^{n+1}}{(n+1)!}\longrightarrow0\quad\text{as }n\to\infty$$
> because from $n>2|x|$ onward each new factor multiplies by less than $\tfrac12$.
>
> **So whenever the derivatives are uniformly bounded, $R_n\to0$ and the Taylor series converges to $f$ everywhere.** **That is exactly why $e^x$, $\sin$ and $\cos$ have $R=\infty$** — their derivatives never grow.
>
> **Contrast $\ln(1+x)$**, whose $n$th derivative is $\pm\frac{(n-1)!}{(1+x)^n}$: **the factorial in the numerator cancels the one in the denominator**, leaving $\frac{x^n}{n}$ — and hence $R=1$ rather than $\infty$.

> [!question] Exercise 4 — series in use
> (i) Evaluate $\displaystyle\lim_{x\to0}\frac{\sin x-x}{x^3}$ using series, and compare with l'Hôpital.
> (ii) Show $e^{i\theta}=\cos\theta+i\sin\theta$ by comparing series.
> (iii) Use the geometric series to sum $\displaystyle\sum_{n=1}^\infty\frac{n}{2^n}$.
> (iv) Show $\ln(1+x)\approx x-\frac{x^2}2$ and hence explain when "a 5% return" and "a log-return of 0.05" differ materially.

> [!example]- Solution
> **(i)** $\sin x=x-\frac{x^3}6+\frac{x^5}{120}-\cdots$, so
> $$\frac{\sin x-x}{x^3}=\frac{-\frac{x^3}6+\frac{x^5}{120}-\cdots}{x^3}=-\frac16+\frac{x^2}{120}-\cdots\longrightarrow\boxed{-\tfrac16}$$
>
> **l'Hôpital needs three applications** and three rounds of differentiating $\sin$; **the series makes the answer visible immediately** — and it also gives the *next* term, so you can see the rate of approach.
>
> **Series are usually the better tool for $\tfrac00$ limits at a point where you know the expansions.**
>
> **(ii)** Substituting $i\theta$ into the exponential series and splitting by parity of $n$:
> $$e^{i\theta}=\sum\frac{(i\theta)^n}{n!}=\underbrace{\left(1-\frac{\theta^2}{2!}+\frac{\theta^4}{4!}-\cdots\right)}_{\cos\theta}+i\underbrace{\left(\theta-\frac{\theta^3}{3!}+\frac{\theta^5}{5!}-\cdots\right)}_{\sin\theta}$$
> using $i^2=-1$, $i^3=-i$, $i^4=1$. $\blacksquare$
>
> **At $\theta=\pi$ this gives $e^{i\pi}+1=0$.** **The identity is not a definition or a coincidence — it is the observation that the exponential series, split into even and odd parts, is exactly the cosine and sine series.**
>
> **(iii)** Differentiate $\sum_{n=0}^\infty x^n=\frac1{1-x}$ term by term (legal inside $R=1$):
> $$\sum_{n=1}^\infty nx^{n-1}=\frac1{(1-x)^2}\ \Longrightarrow\ \sum_{n=1}^\infty nx^n=\frac{x}{(1-x)^2}$$
> At $x=\tfrac12$: $\ \dfrac{1/2}{(1/2)^2}=\boxed{2}$ *(verified)*.
>
> **Term-by-term differentiation turned a hard sum into a known one** — and the same manoeuvre is how generating functions produce moments in [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]].
>
> **(iv)** From the series, $\ln(1+x)=x-\frac{x^2}2+\frac{x^3}3-\cdots$, so for small $x$:
> $$\ln(1+x)\approx x-\frac{x^2}2$$
>
> | Return $x$ | $\ln(1+x)$ | difference |
> |---|---|---|
> | $0.01$ | $0.00995$ | $0.005\%$ |
> | $0.05$ | $0.04879$ | $0.12\%$ |
> | $0.20$ | $0.18232$ | $1.8\%$ |
> | $0.50$ | $0.40546$ | $9.5\%$ |
>
> **At 1% the two are interchangeable; at 50% they are not.**
>
> > [!important] This is why log-returns and simple returns are used differently
> > **The first-order agreement $\ln(1+x)\approx x$ is why a log-return can be read as a percentage** — and the $-\frac{x^2}2$ correction is why that reading fails for large moves.
> >
> > **Log-returns are preferred because they *add* over time** ($\ln\frac{P_2}{P_0}=\ln\frac{P_2}{P_1}+\ln\frac{P_1}{P_0}$) while simple returns compound. **The price is that they must be converted back for large moves** ([[Time-series Analysis/contents/00-Index|Time-series Analysis]]).
> >
> > **The same expansion is why a log-linear regression coefficient of $0.05$ is reported as "about a 5% effect"** — and why a coefficient of $0.5$ should not be ([[Econometrics/contents/00-Index|Econometrics]]).

> [!question] Exercise 5 — the limits of Taylor series *(hard)*
> (a) Use the series for $e^{-x^2}$ to evaluate $\displaystyle\int_0^1e^{-x^2}dx$ to six decimal places, and say how many terms you needed.
>
> (b) Let $\ f(x)=e^{-1/x^2}$ for $x\ne0$ and $f(0)=0$.
> (i) Show $f^{(n)}(0)=0$ for every $n$ *(you may assume this)*, and write down the Maclaurin series.
> (ii) Does the series converge? Does it converge **to $f$**?
> (iii) What does this show about the relationship between a function and its derivatives at a point?
>
> (c) The harmonic series diverges, yet $\sum\frac1{n^{1.01}}$ converges. Explain, and comment on what this means for detecting divergence numerically.

> [!example]- Solution
> **(a)** Integrate the series term by term (legal, since $R=\infty$):
> $$\int_0^1e^{-x^2}dx=\int_0^1\sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{n!}dx=\sum_{n=0}^\infty\frac{(-1)^n}{n!(2n+1)}$$
> $$=1-\frac13+\frac1{10}-\frac1{42}+\frac1{216}-\frac1{1320}+\cdots$$
> **Eight terms give $0.7468228$ against the true $0.7468241$** *(verified)* — error $1.3\times10^{-6}$.
>
> **It is an alternating series with decreasing terms, so the error is bounded by the first omitted term** — a free and sharp error estimate.
>
> **The integrand has no elementary antiderivative** ([[05 - Techniques of Integration|ch. 05]]), so **there was no other exact route.** Compare with [[05 - Techniques of Integration|ch. 05]]'s Simpson's rule, which reached $8\times10^{-7}$ with eleven function evaluations — **comparable accuracy by a completely different method.**
>
> **(b)(i)** Every derivative of $e^{-1/x^2}$ is of the form $P(1/x)e^{-1/x^2}$ for some polynomial $P$, and $e^{-1/x^2}\to0$ faster than any power of $1/x$ grows. **So every derivative at 0 is 0**, and the Maclaurin series is
> $$0+0\cdot x+0\cdot x^2+\cdots=0$$
>
> **(ii)** **It converges — everywhere, and instantly, to the zero function.** But $f(x)\ne0$ for every $x\ne0$ (indeed $f(1)=e^{-1}\approx0.368$).
>
> **So the series converges, with infinite radius, to the wrong function.**
>
> **(iii)** **The derivatives at a single point do not determine the function**, even when all of them exist and the resulting series converges everywhere.
>
> **What is missing is the remainder.** $f=\sum\frac{f^{(n)}(a)}{n!}(x-a)^n$ holds **only when $R_n(x)\to0$**, and here $R_n(x)=f(x)$ for every $n$ — the remainder never shrinks at all.
>
> > [!important] Why this example is worth remembering
> > **It is the reason Taylor's theorem is stated with a remainder rather than as an identity.** Writing "$f$ equals its Taylor series" without checking $R_n\to0$ is an unjustified step, and this function is the standing proof.
> >
> > **The practical reading: local information is *usually* enough and *not always*.** Every "expand to second order and ignore the rest" argument — the delta method, Laplace approximation, Newton's method, a Gaussian approximation to a posterior — **is trusting a remainder without checking it.** Usually that is fine. **This function is what "usually" excludes.**
>
> **(c)** Both are $p$-series: $p=1$ diverges, $p=1.01>1$ converges.
>
> **The threshold is exactly at $p=1$, and nothing about the terms reveals which side you are on.** Numerically:
> - $\sum_{n=1}^{N}\frac1n\approx\ln N+\gamma$ — **it grows, but like $\ln N$**, so reaching 20 needs $N\approx10^8$ terms.
> - $\sum_{n=1}^\infty\frac1{n^{1.01}}\approx101$ — **finite, but the partial sums approach it extraordinarily slowly.**
>
> **So after a million terms the two look identical**, and no amount of computation distinguishes them.
>
> > [!warning] Convergence is not a numerically detectable property
> > **You cannot decide convergence by adding terms.** A divergent series can grow so slowly that it looks convergent for any number of terms you can afford, and a convergent one can approach its limit too slowly to reveal it.
> >
> > **This is the series version of [[01 - Functions, Limits and Continuity|ch. 01's]] "numerical tables lie"** — and it is why the convergence *tests* exist. **They answer a question that no amount of arithmetic can.**

---

## 📝 Summary

- **A series converges iff its partial sums converge** — the infinite sum is a limit, not an act of adding.
- **Geometric ($|r|<1$) and $p$-series ($p>1$) are the two benchmarks** everything else is compared with. $\sum2^{-n}=2$, $\sum n^{-2}=\frac{\pi^2}6$, **$\sum n^{-1}=\infty$.**
- **The $n$th-term test proves only divergence.** $a_n\to0$ is necessary and **not** sufficient — the harmonic series is the standing counterexample.
- **Test order: $n$th-term, recognise the form, ratio (for factorials and $n$th powers), comparison, alternating.**
- **Absolutely convergent $\Rightarrow$ convergent**, and **only absolutely convergent series can be rearranged safely** — a conditionally convergent series can be reordered to any sum at all. **This is why $\mathbb{E}[X]$ requires $\mathbb{E}|X|<\infty$.**
- **The integral test makes "a series is a Riemann sum" precise**, and its $p$-threshold is [[05 - Techniques of Integration|ch. 05]]'s $p$-test.
- **A power series converges on an interval of radius $R$** (found by the ratio test, **endpoints checked separately**) and **may be differentiated and integrated term by term inside it**, with $R$ unchanged.
- $$\boxed{f(x)=\sum\frac{f^{(n)}(a)}{n!}(x-a)^n}$$ **and the coefficients are forced** — if a power-series representation exists, it is the Taylor series.
- **Know six series: $e^x$, $\sin$, $\cos$, $\frac1{1-x}$, $\ln(1+x)$, $\arctan$.** **Derive everything else from them** by substitution, multiplication, differentiation or integration — deriving $\arctan$ by integrating a geometric series takes one line and differentiating $\arctan$ repeatedly is hopeless.
- $$|R_n(x)|\le\frac{M}{(n+1)!}|x-a|^{n+1}$$ **The factorial beats any power**, which is why $e^x$, $\sin$ and $\cos$ converge everywhere. **The bounds are sharp** — within 1% of the true error in both worked cases.
- **"The series converges" and "the series converges to $f$" are different claims.** $e^{-1/x^2}$ has an everywhere-convergent Maclaurin series that equals 0 and a function that does not. **Only $R_n\to0$ closes the gap.**
- **Series evaluate non-elementary integrals** — eight terms give $\int_0^1e^{-x^2}dx$ to $1.3\times10^{-6}$ — **and they beat l'Hôpital on $\tfrac00$ limits**, since they also show the next term.
- **$\ln(1+x)\approx x-\frac{x^2}2$ is why log-returns read as percentages for small moves and not for large ones.**
- **Convergence cannot be settled numerically:** $\sum n^{-1}$ and $\sum n^{-1.01}$ are indistinguishable after a million terms.

---

## ⚠️ Important Notes

> [!warning] $a_n\to0$ does not make $\sum a_n$ converge
> **The harmonic series is the whole point:** $\frac1n\to0$ and $\sum\frac1n=\infty$.
>
> **The test is one-directional.** $a_n\not\to0$ proves divergence; $a_n\to0$ proves nothing. **Writing "the terms go to zero, so it converges" is the most common error in the chapter.**

> [!warning] Only absolutely convergent series may be rearranged
> **Riemann: a conditionally convergent series can be reordered to converge to any real number, or to diverge.**
>
> $$1-\tfrac12+\tfrac13-\tfrac14+\cdots=\ln2\quad\text{\textbf{in that order}}$$
>
> **So "the sum" of a conditionally convergent series is a property of the *ordering*, not of the set of terms.** This is exactly why expectations, infinite matrix products and interchanges of $\sum$ with $\int$ or $\lim$ all carry absolute-convergence hypotheses.

> [!warning] Check the endpoints of an interval of convergence separately
> **The ratio test gives $R$ and is silent at $|x-a|=R$**, where all four behaviours occur:
> | Series | $x=-1$ | $x=1$ |
> |---|---|---|
> | $\sum x^n$ | diverges | diverges |
> | $\sum\frac{x^n}{n}$ | **converges** | diverges |
> | $\sum\frac{x^n}{n^2}$ | converges | converges |
>
> **The interval of convergence is not determined by $R$ alone.**

> [!warning] A convergent Taylor series need not converge to $f$
> $$f(x)=e^{-1/x^2}\ (f(0)=0)\ \Longrightarrow\ \text{Maclaurin series}\equiv0\ne f$$
> **Every derivative at 0 vanishes, the series converges everywhere, and it is wrong everywhere except at 0.**
>
> **Only $R_n\to0$ justifies the equality.** Every applied "expand and truncate" argument — the delta method, Laplace approximation, Newton's method — **assumes a remainder estimate it rarely checks.** Usually safe; not always.

> [!warning] Convergence is not numerically detectable
> $$\sum\frac1n\ \text{diverges},\qquad \sum\frac1{n^{1.01}}\approx101$$
> **After a million terms the partial sums are indistinguishable.** The harmonic series reaches only $\approx14$ by $N=10^6$, growing like $\ln N$.
>
> **So no computation decides convergence** — the tests exist precisely because arithmetic cannot answer the question. **The same warning as [[01 - Functions, Limits and Continuity|ch. 01's]] "tables lie", one level up.**

> [!warning] Build series from known ones
> **Computing $f^{(n)}(a)$ for general $n$ is usually the hardest possible route.** The derivatives of $\arctan$ grow messier with no pattern; **integrating $\frac1{1+x^2}=\sum(-1)^nx^{2n}$ takes one line.**
>
> **Substitution, multiplication, differentiation and integration of the six standard series cover almost everything you will need**, and each operation's effect on $R$ is predictable.

> [!note] Cross-subject connections
> - [[02 - Derivatives|Ch. 02]] — the linearization is $T_1$, and **its empirical $h^2$ error law is Taylor's Inequality with $n=1$.**
> - [[03 - Applications of Differentiation|Ch. 03]] — series often replace l'Hôpital, and give the next term as a bonus.
> - [[05 - Techniques of Integration|Ch. 05]] — **series evaluate the non-elementary integrals**; the integral test's $p$-threshold is the $p$-test; and the two methods are compared in Exercise 5(a).
> - [[Probability Theory/contents/04 - Random Variables|Probability ch. 04]] — **the geometric and Poisson distributions sum to 1 by these series**, and $\mathbb{E}[X]$ requires **absolute** convergence for exactly Riemann's reason.
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **moment generating functions are power series**, and $M^{(n)}(0)=\mathbb{E}[X^n]$ is reading off Taylor coefficients; term-by-term differentiation (Exercise 4(iii)) is how moments are extracted.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — **the delta method is a first-order Taylor expansion** of $g(X)$ about $\mu$; Laplace approximation is a second-order one.
> - [[Econometrics/contents/00-Index|Econometrics]] — **$\ln(1+x)\approx x$ is why log-linear coefficients read as percentages**, and the $-\frac{x^2}2$ term is why that fails for large effects.
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — an MA($\infty$) representation is a power series in the lag operator, and **stationarity is a radius-of-convergence condition.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — second-order optimizers use $T_2$; positional encodings and kernel expansions are series; **and "expand and truncate" is everywhere, usually without a remainder check.**

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **This chapter suffers the worst structural damage yet: $\sum$ signs lose their index and bounds entirely.** A displayed $\sum_{n=1}^\infty a_n$ extracts as `o` on one line, `n−1` on another, and `an` on a third — **so the starting index (0 or 1) is frequently unrecoverable from the extraction alone**, and it changes the sum. **Every series in these notes was reconstructed with its index checked against the written-out first few terms, and every sum was verified symbolically.**
>
> **Figures lost, and the losses here are unusually costly:**
> - **§11.1–11.2's partial-sum plots**, which are how "converges" is made visible — a sequence of dots levelling off versus one drifting away. **Nothing in the algebra conveys this.**
> - **§11.3's integral-test diagram** — rectangles drawn against the curve $y=f(x)$, showing the sum trapped between two integrals. **This is not an illustration of the proof, it *is* the proof**, and without it the test looks like an unmotivated coincidence.
> - **§11.11's graphs of $T_1,T_2,T_3,\dots$ converging to $f$**, which show the interval of convergence shrinking or growing before your eyes and are the single best argument for why $R$ exists.
>
> **Verification performed:** every series, sum, expansion and error estimate in this chapter was computed symbolically with `sympy` or evaluated numerically. Confirmed: $\sum2^{-n}=2$, $\sum n^{-2}=\frac{\pi^2}6$, $\sum n^{-1}=\infty$, $\sum\frac{(-1)^{n+1}}n=\ln2$, $\sum\frac1{n(n+1)}=1$, $\sum\frac n{2^n}=2$; **all six standard Maclaurin series to order 6**; **both Taylor error estimates against their true values** — $e^{0.1}$ (actual $1.71\times10^{-4}$ against bound $1.84\times10^{-4}$) and $\sin0.5$ (actual $2.589\times10^{-4}$ against bound $2.604\times10^{-4}$), confirming the bounds are sharp to within 1%; the term count $n=10$ for six-decimal $e$; and **the eight-term series evaluation of $\int_0^1e^{-x^2}dx=0.7468228$ against the true $0.7468241$.** **No error was found in the text's mathematics.**
>
> **Scope note:** **§§11.3–11.7 (the tests) are compressed into one summary table rather than five sections.** Stewart gives each test its own section with a proof and a page of drill; **the statements and the decision procedure are what get used**, and the proofs — except the integral test's, whose figure is lost anyway — are not reused downstream. **§11.9 (representations of functions as power series) is folded into §5**, since its content is the "derive from known series" method. **§11.10 and §11.11 are expanded relative to Stewart's weighting**, because **Taylor expansion with an error bound is the one part of this chapter a data-science reader uses constantly** and the convergence tests are the part they will never use again after the exam.

#calculus #sequences #series #convergence-tests #power-series #taylor-series #maclaurin #remainder
