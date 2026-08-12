---
subject: Calculus
chapter: 05
tags: [ds, calculus, integration-by-parts, trigonometric-substitution, partial-fractions, numerical-integration, improper-integrals]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., ch. 7 (pp. 485–558)"
---

# Techniques of Integration

> [!abstract] What this chapter is for
> **[[04 - Integrals|Chapter 4]] reduced integration to "find an antiderivative". This chapter is the search.**
>
> **Differentiation is an algorithm: apply the rules and you are done. Integration is not.** Every rule of differentiation runs backwards into a *technique* — a pattern to recognise, which may or may not apply:
>
> | Differentiation rule | Reversed |
> |---|---|
> | chain rule | **substitution** ([[04 - Integrals\|ch. 04]]) |
> | product rule | **integration by parts** |
> | — | trigonometric substitution, partial fractions |
>
> **And there is no rule for "the integral of a product", because none exists.** That asymmetry is the whole reason this chapter is a list of tricks rather than a procedure.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **Integration by parts** | The product rule reversed; **$\int u\,dv=uv-\int v\,du$** |
> | **2–3** | Trigonometric integrals and substitution | For $\sqrt{a^2\pm x^2}$ and $\sqrt{x^2-a^2}$ |
> | **4** | **Partial fractions** | Every rational function *can* be integrated |
> | **5** | Strategy | How to decide which to try |
> | **6** | **Numerical integration** | When no antiderivative exists — **which is usually** |
> | **7** | **Improper integrals** | Infinite limits or infinite integrands |
>
> **§7 is the section a data-science reader cannot skip.** Every probability density on $(0,\infty)$ or $\mathbb{R}$ integrates to 1 **improperly**, every expectation is an improper integral, and the convergence tests here are what decide whether a distribution has a mean at all.

---

## 📘 Main Knowledge

### 1. Integration by parts

> [!important] The formula
> From the product rule $(uv)'=u'v+uv'$, integrating and rearranging:
> $$\boxed{\ \int u\,dv=uv-\int v\,du\ }\qquad\qquad \int_a^bu\,dv=\big[uv\big]_a^b-\int_a^bv\,du$$

> [!tip] Choosing $u$: **LIATE**
> **Pick $u$ to be whichever type comes first in the list — that is the one you want to *differentiate* away:**
>
> | | Type | Example |
> |---|---|---|
> | **L** | Logarithmic | $\ln x$ |
> | **I** | Inverse trigonometric | $\arctan x$ |
> | **A** | Algebraic | $x^2$ |
> | **T** | Trigonometric | $\sin x$ |
> | **E** | Exponential | $e^x$ |
>
> **The logic: $u$ gets differentiated and $dv$ gets integrated, so choose $u$ to be the thing that *simplifies* when differentiated and $dv$ to be the thing you can integrate.** $\ln x$ has no elementary integral you would want but differentiates to $1/x$; $e^x$ integrates trivially. **LIATE is a heuristic, not a theorem — but it is right almost always.**

> [!example] Four standard applications *(all verified)*
> **The basic one.** $\displaystyle\int xe^x\,dx$ with $u=x$, $dv=e^x dx$:
> $$xe^x-\int e^x\,dx=(x-1)e^x+C$$
>
> **The trick one.** $\displaystyle\int\ln x\,dx$ — take $u=\ln x$, $dv=dx$:
> $$x\ln x-\int x\cdot\frac1x\,dx=x(\ln x-1)+C$$
> **Nothing looked like a product, and it was one: $\ln x=\ln x\cdot1$.** The same move gives $\int\arctan x\,dx=x\arctan x-\tfrac12\ln(1+x^2)+C$.
>
> **The circular one.** $\displaystyle\int e^x\sin x\,dx$: apply parts **twice** and the original integral reappears:
> $$I=e^x\sin x-e^x\cos x-I\ \Longrightarrow\ I=\tfrac12e^x(\sin x-\cos x)+C$$
> **Solving for $I$ algebraically is the technique**, not a failure of the method.
>
> **A definite one.** $\displaystyle\int_0^1xe^x\,dx=\big[(x-1)e^x\big]_0^1=0-(-1)=1$.

> [!important] Reduction formulas
> Repeated parts gives recursions such as
> $$\int\sin^nx\,dx=-\frac1n\sin^{n-1}x\cos x+\frac{n-1}n\int\sin^{n-2}x\,dx$$
> **Each application lowers the power by 2** until reaching $\int\sin x$ or $\int dx$.

---

### 2. Trigonometric integrals and substitution

> [!important] Trigonometric integrals — the two cases
> For $\int\sin^mx\cos^nx\,dx$:
> - **one power odd:** peel off one factor, convert the rest with $\sin^2+\cos^2=1$, substitute.
> - **both powers even:** use the half-angle identities $\sin^2x=\tfrac{1-\cos2x}2$, $\cos^2x=\tfrac{1+\cos2x}2$.

> [!important] Trigonometric substitution — the three patterns
> | Expression | Substitute | Identity used |
> |---|---|---|
> | $\sqrt{a^2-x^2}$ | $x=a\sin\theta$ | $1-\sin^2=\cos^2$ |
> | $\sqrt{a^2+x^2}$ | $x=a\tan\theta$ | $1+\tan^2=\sec^2$ |
> | $\sqrt{x^2-a^2}$ | $x=a\sec\theta$ | $\sec^2-1=\tan^2$ |
>
> **The point is always the same: make the radical disappear** by turning $a^2-x^2$ into $a^2\cos^2\theta$, and so on.

> [!example] $\displaystyle\int\sqrt{1-x^2}\,dx$
> With $x=\sin\theta$, $dx=\cos\theta\,d\theta$:
> $$\int\cos^2\theta\,d\theta=\tfrac12\theta+\tfrac14\sin2\theta+C=\tfrac12\arcsin x+\tfrac12x\sqrt{1-x^2}+C$$
> *(Verified.)* **And the definite version is a sanity check:**
> $$\int_0^1\sqrt{1-x^2}\,dx=\frac\pi4$$
> — **a quarter of the unit circle**, exactly as the geometry demands *(verified)*.

> [!warning] Substitution back is not optional, and the triangle is how you do it
> **After integrating in $\theta$ you must return to $x$.** Draw the right triangle implied by the substitution: for $x=\sin\theta$, opposite $=x$ and hypotenuse $=1$, so $\cos\theta=\sqrt{1-x^2}$.
>
> **Forgetting this leaves an answer in a variable the question never mentioned** — and it is where most marks are lost in this section.

---

### 3. Partial fractions

> [!important] The method
> **Every rational function $P/Q$ can be integrated in elementary terms.** The recipe:
> 1. **If $\deg P\ge\deg Q$, divide first** (long division) to get a polynomial plus a proper fraction.
> 2. **Factor $Q$** into linear and irreducible quadratic factors.
> 3. **Decompose:**
>
> | Factor of $Q$ | Contributes |
> |---|---|
> | $(x-a)$ | $\dfrac{A}{x-a}$ |
> | $(x-a)^k$ | $\dfrac{A_1}{x-a}+\cdots+\dfrac{A_k}{(x-a)^k}$ |
> | $x^2+bx+c$ (irreducible) | $\dfrac{Ax+B}{x^2+bx+c}$ |
> | $(x^2+bx+c)^k$ | one such term per power |
>
> 4. **Integrate each piece:** $\int\frac{dx}{x-a}=\ln|x-a|$, $\int\frac{dx}{x^2+a^2}=\frac1a\arctan\frac xa$.

> [!example] $\displaystyle\int\frac{x+5}{x^2+x-2}\,dx$
> $x^2+x-2=(x-1)(x+2)$, and
> $$\frac{x+5}{(x-1)(x+2)}=\frac{2}{x-1}-\frac{1}{x+2}$$
> so the integral is $\boxed{2\ln|x-1|-\ln|x+2|+C}$. *(Both the decomposition and the integral verified.)*
>
> **To find the constants quickly, multiply through and substitute the roots:** at $x=1$, $6=3A$ so $A=2$; at $x=-2$, $3=-3B$ so $B=-1$.

> [!tip] This is the one genuinely *complete* technique in the chapter
> **Everything else is a pattern that may or may not apply. Partial fractions always works on a rational function** — the algorithm never fails, though the algebra can be laborious.
>
> **It is also how [[06 - Sequences, Series and Taylor Approximation|generating functions]] are inverted, how Laplace transforms are undone, and how a linear recurrence's closed form is extracted** — the same decomposition, used to split a ratio into geometric pieces.

---

### 4. Strategy

> [!important] The order to try things
> 1. **Simplify algebraically** — expand, use identities, rationalise. *(Often the whole answer.)*
> 2. **Look for an obvious substitution** — is an inner function's derivative present?
> 3. **Classify by form:**
> | Form | Try |
> |---|---|
> | rational | **partial fractions** |
> | contains $\sqrt{a^2\pm x^2}$ | **trigonometric substitution** |
> | product of unlike types | **by parts** (LIATE) |
> | powers of trig functions | **trigonometric identities** |
> 4. **Try again with a different substitution.**
> 5. **Accept that it may not be elementary** — go numerical (§5) or use a series ([[06 - Sequences, Series and Taylor Approximation|ch. 06]]).

> [!warning] Most integrals are not elementary, and this is a theorem
> $$\int e^{-x^2}dx,\qquad \int\frac{\sin x}{x}dx,\qquad \int\frac{dx}{\ln x},\qquad \int\sqrt{1+x^3}\,dx$$
> **None can be written with elementary functions** (Liouville's theorem). **This is not a gap in the technique list — it is a proof that no technique list can be complete.**
>
> **The first of them is the normal distribution.** Its non-elementarity is precisely why $\Phi$ is tabulated rather than evaluated, and why [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]] leans on tables and software.

---

### 5. Numerical integration

> [!important] The three rules
> With $\Delta x=\frac{b-a}n$ and $x_i=a+i\Delta x$:
> $$M_n=\Delta x\sum f\!\left(\bar x_i\right)\quad\text{(midpoint)}$$
> $$T_n=\frac{\Delta x}2\Big[f(x_0)+2f(x_1)+\cdots+2f(x_{n-1})+f(x_n)\Big]$$
> $$S_n=\frac{\Delta x}3\Big[f(x_0)+4f(x_1)+2f(x_2)+4f(x_3)+\cdots+4f(x_{n-1})+f(x_n)\Big]\quad(n\text{ even})$$
>
> **Trapezoid fits straight lines; Simpson fits parabolas** through consecutive triples — hence the $1,4,2,4,\dots,4,1$ pattern.

> [!important] Error bounds
> $$|E_T|\le\frac{K(b-a)^3}{12n^2},\qquad |E_M|\le\frac{K(b-a)^3}{24n^2},\qquad \boxed{|E_S|\le\frac{K_4(b-a)^5}{180n^4}}$$
> where $K\ge|f''|$ and $K_4\ge|f^{(4)}|$ on $[a,b]$.

> [!example] $\displaystyle\int_0^1e^{-x^2}dx$ with $n=10$ *(all verified)*
> | Method | Value | Error |
> |---|---|---|
> | Trapezoid | $0.7462108$ | $6.1\times10^{-4}$ |
> | **Simpson** | $0.7468249$ | $\mathbf{8.2\times10^{-7}}$ |
> | True | $0.7468241$ | — |
>
> **Simpson is 750 times more accurate for exactly the same ten function evaluations.**
>
> **The reason is the exponents: $n^{-2}$ versus $n^{-4}$.** Doubling $n$ improves the trapezoid rule fourfold and Simpson's rule **sixteen**fold. **Choosing the better method beats buying a faster computer**, which is the recurring lesson of numerical analysis.

> [!tip] Numerical integration is the normal case, not the fallback
> **The integrand you meet in practice is usually a data-defined function or a non-elementary expression**, and no antiderivative is available even in principle. **Every $\Phi$ value, every Bayesian posterior expectation, every option price is a numerical integral.**
>
> **And in high dimensions all of this fails.** Simpson's rule in $d$ dimensions needs $n^d$ evaluations — **which is why [[Probability Theory/contents/10 - Simulation|Monte Carlo]] takes over: its $O(n^{-1/2})$ error is terrible in one dimension and dimension-independent, so it wins for $d\gtrsim4$.**

---

### 6. Improper integrals

> [!important] Two types
> **Type 1 — infinite interval:**
> $$\int_a^\infty f=\lim_{t\to\infty}\int_a^tf,\qquad \int_{-\infty}^\infty f=\int_{-\infty}^cf+\int_c^\infty f$$
> **Type 2 — infinite integrand:** if $f$ is unbounded at $b$,
> $$\int_a^bf=\lim_{t\to b^-}\int_a^tf$$
>
> **The integral *converges* if the limit exists and is finite, and *diverges* otherwise.**

> [!important] The $p$-test — the single most useful fact in the section
> $$\int_1^\infty\frac{dx}{x^p}\ \text{converges}\iff \boxed{p>1}$$
> $$\int_0^1\frac{dx}{x^p}\ \text{converges}\iff \boxed{p<1}$$
>
> **The two go opposite ways, and the borderline $p=1$ diverges in both.**

> [!tip] Why the thresholds differ
> **At $\infty$ the tail must decay fast enough; at 0 the blow-up must be mild enough.** $\frac1x$ fails both: it decays too slowly at infinity and blows up too fast at 0 — **and it is exactly the borderline case, which is why $\ln$ appears there.**
>
> **The consequence in probability is immediate.** A density behaving like $x^{-p}$ in the tail has
> $$\mathbb{E}[X]=\int xf(x)\,dx\sim\int x^{1-p}\,dx$$
> **which converges only if $p>2$.** *That* is why heavy-tailed distributions can fail to have a mean — the **Cauchy** density decays like $x^{-2}$, so its mean integral is exactly the divergent borderline ([[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]]).

> [!example] The standard results *(all verified)*
> $$\int_1^\infty\frac{dx}{x^2}=1,\qquad \int_1^\infty\frac{dx}{x}=\infty,\qquad \int_0^1\frac{dx}{\sqrt x}=2,\qquad \int_0^1\frac{dx}{x}=\infty$$
> $$\int_0^\infty e^{-x}dx=1,\qquad \int_0^\infty x^2e^{-x}dx=2,\qquad \int_{-\infty}^\infty e^{-x^2}dx=\sqrt\pi$$
>
> **The last is remarkable: an integral with no elementary antiderivative has an exact, and beautiful, value.** *(It is evaluated by a change to polar coordinates — [[09 - Multiple Integrals and Change of Variables|ch. 09]] — which is the only elementary route.)* **Rescaled, it is why the normal density's constant is $\frac1{\sqrt{2\pi}}$.**
>
> **And $\int_0^\infty x^ne^{-x}dx=n!$** is the Gamma function, which is where the gamma distribution's normalising constant comes from.

> [!important] The Comparison Test
> If $0\le g\le f$ on $[a,\infty)$:
> - $\int_a^\infty f$ converges $\Rightarrow$ $\int_a^\infty g$ converges;
> - $\int_a^\infty g$ diverges $\Rightarrow$ $\int_a^\infty f$ diverges.
>
> **Use it when the integral cannot be evaluated but can be bounded** — e.g. $\int_1^\infty e^{-x^2}dx$ converges because $e^{-x^2}\le e^{-x}$ for $x\ge1$.

---

## ✏️ Exercises

> [!question] Exercise 1 — integration by parts *(warm-up)*
> (i) $\displaystyle\int xe^x\,dx$  (ii) $\displaystyle\int\ln x\,dx$  (iii) $\displaystyle\int x\sin x\,dx$
> (iv) $\displaystyle\int e^x\sin x\,dx$ — **and explain why the method appears to fail before it succeeds.**
> (v) $\displaystyle\int_0^1 x e^x\,dx$

> [!example]- Solution
> **(i)** $u=x$, $dv=e^xdx$ (LIATE: **A** before **E**), so $du=dx$, $v=e^x$:
> $$xe^x-\int e^x dx=\boxed{(x-1)e^x+C}$$
> *(Verified.)* **Choosing the other way round would give $\int\frac{x^2}2e^xdx$ — worse.**
>
> **(ii)** There is no visible product, but $\ln x=\ln x\cdot1$. Take $u=\ln x$, $dv=dx$:
> $$x\ln x-\int x\cdot\frac1x dx=\boxed{x(\ln x-1)+C}$$
> *(Verified.)* **"Take $dv=dx$" is the standard move for any function you can differentiate but not integrate** — it also gives $\int\arctan x\,dx=x\arctan x-\tfrac12\ln(1+x^2)+C$ *(verified)*.
>
> **(iii)** $u=x$, $dv=\sin x\,dx$: $\ \boxed{-x\cos x+\sin x+C}$ *(verified)*.
>
> **(iv)** Call the integral $I$ and apply parts with $u=e^x$, $dv=\sin x\,dx$:
> $$I=-e^x\cos x+\int e^x\cos x\,dx$$
> Apply parts **again** to the new integral:
> $$I=-e^x\cos x+e^x\sin x-\int e^x\sin x\,dx=-e^x\cos x+e^x\sin x-I$$
> **The original integral has come back** — which looks like total failure. **But it is now an equation:**
> $$2I=e^x(\sin x-\cos x)\ \Longrightarrow\ \boxed{I=\tfrac12e^x(\sin x-\cos x)+C}$$
> *(Verified — sympy's $-\tfrac{\sqrt2}2e^x\cos(x+\tfrac\pi4)$ is the same expression.)*
>
> **The essential detail: use the *same* choice of $u$ both times.** Switching (taking $u=\cos x$ on the second pass) undoes the first application and returns $I=I$.
>
> **(v)** $\big[(x-1)e^x\big]_0^1=0-(-1)=\boxed{1}$ *(verified)*.

> [!question] Exercise 2 — trigonometric substitution and partial fractions
> (i) $\displaystyle\int\sqrt{1-x^2}\,dx$, and hence $\displaystyle\int_0^1\sqrt{1-x^2}\,dx$. **Check the definite answer geometrically.**
> (ii) $\displaystyle\int\frac{x+5}{x^2+x-2}\,dx$
> (iii) $\displaystyle\int\frac{dx}{x^2-1}$
> (iv) Which substitution suits $\displaystyle\int\frac{dx}{x^2\sqrt{x^2+4}}$, and why?

> [!example]- Solution
> **(i)** $x=\sin\theta$, $dx=\cos\theta\,d\theta$, $\sqrt{1-x^2}=\cos\theta$:
> $$\int\cos^2\theta\,d\theta=\int\frac{1+\cos2\theta}2d\theta=\frac\theta2+\frac{\sin2\theta}4+C$$
> Since $\sin2\theta=2\sin\theta\cos\theta=2x\sqrt{1-x^2}$:
> $$\boxed{\tfrac12\arcsin x+\tfrac12x\sqrt{1-x^2}+C}$$
> *(Verified.)* Evaluating from 0 to 1: $\tfrac12\cdot\tfrac\pi2+0-0=\boxed{\tfrac\pi4}$ *(verified)*.
>
> **Geometric check: $y=\sqrt{1-x^2}$ on $[0,1]$ is a quarter of the unit circle, of area $\tfrac{\pi\cdot1^2}4=\tfrac\pi4$** ✓ — **and a check like this catches a sign or factor error instantly.**
>
> **(ii)** $(x-1)(x+2)$, so write $\frac{x+5}{(x-1)(x+2)}=\frac A{x-1}+\frac B{x+2}$. Multiplying up: $x+5=A(x+2)+B(x-1)$. **Substituting the roots:** $x=1$ gives $6=3A$, so $A=2$; $x=-2$ gives $3=-3B$, so $B=-1$.
> $$\int\left(\frac2{x-1}-\frac1{x+2}\right)dx=\boxed{2\ln|x-1|-\ln|x+2|+C}$$
> *(Both the decomposition and the integral verified.)*
>
> **(iii)** $\frac1{x^2-1}=\frac1{(x-1)(x+1)}=\frac{1/2}{x-1}-\frac{1/2}{x+1}$ *(verified)*, so
> $$\boxed{\tfrac12\ln\left|\frac{x-1}{x+1}\right|+C}$$
>
> **(iv)** The radical is $\sqrt{x^2+4}=\sqrt{2^2+x^2}$ — **the $a^2+x^2$ pattern, so $x=2\tan\theta$**, using $1+\tan^2\theta=\sec^2\theta$ to turn it into $2\sec\theta$.
> $$\int\frac{2\sec^2\theta\,d\theta}{4\tan^2\theta\cdot2\sec\theta}=\frac14\int\frac{\cos\theta}{\sin^2\theta}d\theta=-\frac1{4\sin\theta}+C=\boxed{-\frac{\sqrt{x^2+4}}{4x}+C}$$
> *(Verified — sympy's $-\tfrac14\sqrt{1+4/x^2}$ is the same.)*
>
> **The final step back to $x$ used the triangle:** opposite $x$, adjacent 2, hypotenuse $\sqrt{x^2+4}$, so $\sin\theta=\frac{x}{\sqrt{x^2+4}}$.

> [!question] Exercise 3 — numerical integration
> Estimate $\displaystyle\int_0^1e^{-x^2}dx$ with $n=10$.
> (i) By the trapezoid rule.  (ii) By Simpson's rule.
> (iii) Compare with the true value $0.7468241328$.
> (iv) How large must $n$ be for the trapezoid rule to match Simpson's $n=10$ accuracy?

> [!example]- Solution
> **(i)** With $h=0.1$:
> $$T_{10}=\frac{h}{2}\left[f(0)+2\big(f(0.1)+\cdots+f(0.9)\big)+f(1)\right]=\boxed{0.7462108}$$
>
> **(ii)** $$S_{10}=\frac h3\left[f(0)+4f(0.1)+2f(0.2)+4f(0.3)+\cdots+4f(0.9)+f(1)\right]=\boxed{0.7468249}$$
>
> *(Both verified.)*
>
> **(iii)** | Method | Error |
> |---|---|
> | Trapezoid | $6.1\times10^{-4}$ |
> | **Simpson** | $\mathbf{8.2\times10^{-7}}$ |
>
> **Simpson is $\approx750$ times more accurate using exactly the same eleven function values.** The only difference is the weighting.
>
> **(iv)** Trapezoid error scales as $n^{-2}$, so to improve by a factor of 750 needs $n$ larger by $\sqrt{750}\approx27$:
> $$n\approx270$$
> **Twenty-seven times the work for the same answer.**
>
> > [!important] The exponent is what matters, not the constant
> > $$|E_T|\sim n^{-2},\qquad |E_S|\sim n^{-4}$$
> > **Doubling $n$ helps the trapezoid rule by $4\times$ and Simpson by $16\times$.** As accuracy requirements tighten, the gap widens without limit — **so choosing the right method dominates every constant-factor optimisation.**
> >
> > **The same reasoning runs the other way in high dimensions.** Simpson in $d$ dimensions costs $n^d$ evaluations for error $n^{-4}$, i.e. error $\sim N^{-4/d}$ in total work $N$ — **catastrophic for large $d$.** Monte Carlo's $N^{-1/2}$ is worse in one dimension and **independent of $d$**, so it wins from about $d=8$ onward ([[Probability Theory/contents/10 - Simulation|Probability ch. 10]]).

> [!question] Exercise 4 — improper integrals
> Determine convergence, and evaluate where possible.
> (i) $\displaystyle\int_1^\infty\frac{dx}{x^2}$ and $\displaystyle\int_1^\infty\frac{dx}{x}$
> (ii) $\displaystyle\int_0^1\frac{dx}{\sqrt x}$ and $\displaystyle\int_0^1\frac{dx}{x}$
> (iii) $\displaystyle\int_0^\infty e^{-x}dx$ and $\displaystyle\int_0^\infty x^2e^{-x}dx$
> (iv) $\displaystyle\int_1^\infty e^{-x^2}dx$ — **converges or not? You cannot evaluate it.**
> (v) State the $p$-test for both types and explain why the inequalities point opposite ways.

> [!example]- Solution
> **(i)** $$\int_1^\infty x^{-2}dx=\lim_{t\to\infty}\left[-\frac1x\right]_1^t=\lim_{t\to\infty}\left(1-\frac1t\right)=\boxed{1}$$
> $$\int_1^\infty x^{-1}dx=\lim_{t\to\infty}\big[\ln x\big]_1^t=\lim_{t\to\infty}\ln t=\boxed{\infty}$$
> *(Both verified.)* **$1/x$ decays, and not fast enough** — the borderline case.
>
> **(ii)** $$\int_0^1x^{-1/2}dx=\lim_{a\to0^+}\big[2\sqrt x\big]_a^1=\boxed{2},\qquad \int_0^1x^{-1}dx=\boxed{\infty}$$
> *(Both verified.)*
>
> **(iii)** $$\int_0^\infty e^{-x}dx=\boxed{1},\qquad \int_0^\infty x^2e^{-x}dx=\boxed{2}$$
> *(Both verified.)* **The second is $\Gamma(3)=2!$**, and in general $\int_0^\infty x^ne^{-x}dx=n!$ — **which is where the gamma distribution's normalising constant comes from** ([[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]]).
>
> **(iv) Converges, by comparison.** For $x\ge1$ we have $x^2\ge x$, so $e^{-x^2}\le e^{-x}$, and
> $$\int_1^\infty e^{-x^2}dx\le\int_1^\infty e^{-x}dx=e^{-1}<\infty$$
> **Convergence is settled without evaluating anything** — which is fortunate, since $e^{-x^2}$ has no elementary antiderivative.
>
> *(The full integral over $\mathbb{R}$ does have a closed form: $\int_{-\infty}^\infty e^{-x^2}dx=\sqrt\pi$ — verified — but only via a two-dimensional polar-coordinate trick, [[09 - Multiple Integrals and Change of Variables|ch. 09]].)*
>
> **(v)** $$\int_1^\infty\frac{dx}{x^p}\text{ converges}\iff p>1,\qquad \int_0^1\frac{dx}{x^p}\text{ converges}\iff p<1$$
>
> **The two conditions are opposite because the danger is at opposite ends.**
> - **At $\infty$**, the integrand must **decay fast enough** — so a *large* $p$ helps.
> - **At 0**, the integrand must **not blow up too fast** — so a *small* $p$ helps.
>
> **$p=1$ fails both**, sitting exactly on each boundary, which is why $\int\frac{dx}x$ gives a logarithm — the function that grows more slowly than any positive power and still without bound.
>
> > [!important] This is where distributions lose their means
> > **If a density behaves like $x^{-p}$ in the tail, then $\mathbb{E}[X]=\int xf(x)dx\sim\int x^{1-p}dx$ converges only for $p>2$**, and $\mathbb{E}[X^2]$ only for $p>3$.
> >
> > **The Cauchy density $\frac1{\pi(1+x^2)}$ decays like $x^{-2}$ — exactly the borderline — so its mean does not exist**, and the law of large numbers fails for it ([[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]]).
> >
> > **A "heavy-tailed" distribution is one whose $p$ is small enough for the $p$-test to fail**, and every warning about heavy tails in statistics traces back to this one inequality.

> [!question] Exercise 5 — strategy and limits of the method *(hard)*
> (a) For each, say which technique applies and why, **without evaluating**:
> (i) $\int x^2\ln x\,dx$ (ii) $\int\frac{x^3}{x^2+1}dx$ (iii) $\int\frac{dx}{\sqrt{9-x^2}}$ (iv) $\int\frac{2x}{x^2+1}dx$ (v) $\int e^{x^2}dx$
>
> (b) Show $\int_0^\infty\frac{dx}{1+x^2}=\frac\pi2$, and deduce $\int_{-\infty}^\infty\frac{dx}{\pi(1+x^2)}=1$.
>
> (c) For the Cauchy density $f(x)=\frac1{\pi(1+x^2)}$, show $\int_{-\infty}^\infty xf(x)\,dx$ **diverges**, and explain why writing $\lim_{t\to\infty}\int_{-t}^{t}xf(x)\,dx=0$ does **not** rescue it.

> [!example]- Solution
> **(a)(i) By parts**, $u=\ln x$ (LIATE: **L** first), $dv=x^2dx$. **The log must be differentiated away.**
>
> **(ii) Long division first** — the numerator's degree exceeds the denominator's:
> $$\frac{x^3}{x^2+1}=x-\frac{x}{x^2+1}$$
> then the second piece is a substitution $u=x^2+1$. **Step 1 of the partial-fractions recipe, and skipping it makes the problem look harder than it is.**
>
> **(iii) Trigonometric substitution** $x=3\sin\theta$ — the $\sqrt{a^2-x^2}$ pattern. *(It is $\arcsin\frac x3+C$.)*
>
> **(iv) Plain substitution** $u=x^2+1$: the numerator is exactly $du$. **Recognising this before reaching for partial fractions saves the whole computation** — it is $\ln(x^2+1)+C$.
>
> **(v) None of them.** $e^{x^2}$ has **no elementary antiderivative** (Liouville). **Go numerical, or use the series $\sum\frac{x^{2n}}{n!}$ and integrate term by term** ([[06 - Sequences, Series and Taylor Approximation|ch. 06]]).
>
> **Note the contrast between (iv) and (ii):** both are rational, and one needs no machinery at all. **Always look for a substitution before classifying.**
>
> **(b)** $$\int_0^\infty\frac{dx}{1+x^2}=\lim_{t\to\infty}\big[\arctan x\big]_0^t=\lim_{t\to\infty}\arctan t=\boxed{\frac\pi2}$$
> By symmetry the integrand is even, so $\int_{-\infty}^\infty\frac{dx}{1+x^2}=\pi$ and therefore
> $$\int_{-\infty}^\infty\frac{dx}{\pi(1+x^2)}=\frac\pi\pi=\boxed{1}$$
> **— the Cauchy density is a genuine probability density.**
>
> **(c)** For the mean we need $\int_{-\infty}^\infty\frac{x}{\pi(1+x^2)}dx$, which by definition is the **sum of two separate limits**:
> $$\int_0^\infty\frac{x\,dx}{\pi(1+x^2)}=\lim_{t\to\infty}\frac{1}{2\pi}\ln(1+t^2)=+\infty$$
> and the left half is $-\infty$. **Both halves diverge, so the integral does not exist.**
>
> **Why the symmetric limit does not help.** It is true that
> $$\lim_{t\to\infty}\int_{-t}^{t}\frac{x\,dx}{\pi(1+x^2)}=0$$
> since the integrand is odd. **But that is a *different* quantity — the Cauchy principal value — and it is not what $\int_{-\infty}^\infty$ means.**
>
> **The definition requires the two halves to converge *independently*, and for good reason: otherwise the answer would depend on how you take the limit.** Using $\int_{-t}^{2t}$ instead gives
> $$\frac1{2\pi}\ln\frac{1+4t^2}{1+t^2}\ \longrightarrow\ \frac{\ln4}{2\pi}\ne0$$
> **— a different "answer" from an equally natural limiting procedure.** A quantity that changes when you rearrange the limit is not a number.
>
> > [!important] This is exactly why the Cauchy has no mean
> > **Not "the mean is 0 by symmetry" — the mean does not exist.** The symmetry is real, and it is not enough.
> >
> > **The consequences are severe and are the standard cautionary tale:** the sample mean of $n$ Cauchy variables is Cauchy for **every** $n$, so it never concentrates, the law of large numbers fails, and the central limit theorem does not apply ([[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]]).
> >
> > **And it is decided entirely by the $p$-test.** The density decays like $x^{-2}$; the mean integrand therefore decays like $x^{-1}$; and $p=1$ is precisely the divergent borderline of §6.

---

## 📝 Summary

- **Differentiation is an algorithm; integration is a search.** Each differentiation rule reverses into a *technique*, and **there is no rule for the integral of a product** — hence a list of patterns rather than a procedure.
- **Integration by parts $\int u\,dv=uv-\int v\,du$ is the product rule reversed.** Choose $u$ by **LIATE** — the thing that simplifies when differentiated. **$dv=dx$ handles $\ln x$ and $\arctan x$**, which look like non-products.
- **When parts returns the original integral, solve for it algebraically** ($\int e^x\sin x$) — using the *same* choice of $u$ both times.
- **Trigonometric substitution kills radicals:** $\sqrt{a^2-x^2}\to a\sin\theta$, $\sqrt{a^2+x^2}\to a\tan\theta$, $\sqrt{x^2-a^2}\to a\sec\theta$. **Draw the triangle to substitute back.**
- **Partial fractions is the one complete technique** — every rational function integrates in elementary terms. **Divide first if $\deg P\ge\deg Q$**, factor, decompose, integrate.
- **Strategy: simplify, then look for a substitution, then classify by form.** Recognising $\int\frac{2x}{x^2+1}dx$ as a substitution rather than a partial-fractions problem saves the whole computation.
- **Most integrals are not elementary** — $e^{-x^2}$, $\frac{\sin x}x$, $\frac1{\ln x}$, $\sqrt{1+x^3}$ — **and this is a theorem**, so no list of techniques can be complete.
- **Numerical integration:** trapezoid error $\sim n^{-2}$, **Simpson $\sim n^{-4}$.** On $\int_0^1e^{-x^2}$ with $n=10$, Simpson beats the trapezoid rule **750-fold on identical function evaluations**; matching it would need $n\approx270$.
- **In high dimensions all quadrature fails** ($n^d$ evaluations), which is why **Monte Carlo**, with its dimension-independent $N^{-1/2}$, takes over.
- **Improper integrals are limits**, of Type 1 (infinite interval) or Type 2 (infinite integrand). $$\boxed{\int_1^\infty x^{-p}\text{ converges}\iff p>1;\qquad \int_0^1x^{-p}\text{ converges}\iff p<1}$$ **The inequalities point opposite ways because the danger is at opposite ends, and $p=1$ fails both.**
- **The comparison test settles convergence without evaluation** — $\int_1^\infty e^{-x^2}\le\int_1^\infty e^{-x}<\infty$.
- **The $p$-test is why heavy-tailed distributions lack means.** A density decaying like $x^{-p}$ has a mean only if $p>2$; **the Cauchy sits exactly on the borderline, so its mean does not exist** — and "zero by symmetry" is not a rescue, because the two halves must converge independently.

---

## ⚠️ Important Notes

> [!warning] Choose $u$ so that it *simplifies*, and keep the choice consistent
> **LIATE picks $u$ correctly almost always** — but the reason matters more than the mnemonic: **$u$ is differentiated, so it should get simpler; $dv$ is integrated, so it must be integrable.**
>
> **In a circular case ($\int e^x\sin x$), switching the choice on the second application undoes the first** and returns the vacuous $I=I$. **Use the same type for $u$ throughout.**

> [!warning] Substitute back — and check a definite answer against geometry when you can
> **After a trigonometric substitution the answer is in $\theta$ and the question was in $x$.** Draw the triangle.
>
> **And where a geometric reading exists, use it as a check.** $\int_0^1\sqrt{1-x^2}dx$ must be $\tfrac\pi4$ because it is a quarter-circle; **an answer that is not catches every sign and factor error at once.**

> [!warning] Look for a substitution before classifying by type
> $$\int\frac{2x}{x^2+1}dx=\ln(x^2+1)+C\quad\text{(one line)}$$
> **A partial-fractions attack on this would first note $x^2+1$ is irreducible, then produce $\frac{Ax+B}{x^2+1}$, then rediscover the substitution.** The rational-function classification is correct and unhelpful.
>
> **Similarly, divide before decomposing** whenever $\deg P\ge\deg Q$ — $\frac{x^3}{x^2+1}=x-\frac x{x^2+1}$ is two easy integrals.

> [!warning] "No elementary antiderivative" is a theorem, not a failure
> $$\int e^{-x^2}dx,\qquad\int\frac{\sin x}xdx,\qquad\int\frac{dx}{\ln x},\qquad\int\sqrt{1+x^3}\,dx$$
> **Liouville proved no elementary expression exists.** Time spent searching is time wasted.
>
> **What to do instead:** bound it (comparison), expand it (series — [[06 - Sequences, Series and Taylor Approximation|ch. 06]]), or compute it (numerically). **The first of these integrals is the normal distribution**, used constantly and never in closed form.

> [!warning] Improper integrals must be split at **every** singularity, and each piece must converge on its own
> $$\int_{-1}^1\frac{dx}{x^2}\ \ne\ \left[-\frac1x\right]_{-1}^1$$
> **The FTC does not apply across a singularity** ([[04 - Integrals|ch. 04]], Exercise 5(b)), and the naive computation gives $-2$ for a strictly positive integrand.
>
> **And for $\int_{-\infty}^\infty$, the two halves must converge separately.** The symmetric limit $\lim_t\int_{-t}^t$ is the **Cauchy principal value** — a different and weaker notion, which can assign a "value" that changes if you take the limit as $\int_{-t}^{2t}$ instead. **A number that depends on how you approached it is not a number.**

> [!warning] The exponent in an error bound beats every constant
> | | Error | Doubling $n$ |
> |---|---|---|
> | Trapezoid | $n^{-2}$ | $4\times$ better |
> | Simpson | $n^{-4}$ | $16\times$ better |
> | Monte Carlo | $N^{-1/2}$ | $1.4\times$ better |
>
> **In one dimension Simpson dominates. In $d$ dimensions it needs $n^d$ points and its effective rate collapses to $N^{-4/d}$, while Monte Carlo stays at $N^{-1/2}$ regardless of $d$.**
>
> **So the "worst" method wins in high dimensions** — the single most important fact about numerical integration for anyone doing Bayesian computation or high-dimensional expectation.

> [!note] Cross-subject connections
> - [[04 - Integrals|Ch. 04]] — the FTC creates the search this chapter conducts; substitution is the technique this chapter extends.
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — **series evaluate the non-elementary integrals**, and the integral test runs the comparison the other way; the $p$-test here is the $p$-series test there.
> - [[09 - Multiple Integrals and Change of Variables|Ch. 09]] — **$\int_{-\infty}^\infty e^{-x^2}dx=\sqrt\pi$ is proved there**, by squaring the integral and changing to polar coordinates.
> - [[Probability Theory/contents/05 - Continuous Random Variables|Probability ch. 05]] — **every density integrates to 1 improperly**; $\Gamma(n+1)=\int_0^\infty x^ne^{-x}dx=n!$ gives the gamma normalisation; the $p$-test decides whether a mean exists.
> - [[Probability Theory/contents/08 - Limit Theorems|Probability ch. 08]] — **the Cauchy's missing mean (Exercise 5(c)) is why the LLN and CLT fail for it.**
> - [[Probability Theory/contents/10 - Simulation|Probability ch. 10]] — Monte Carlo integration, and why it displaces quadrature in high dimensions.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — moment generating functions are improper integrals whose *existence* is exactly a convergence question; every normal-table value is a numerical quadrature.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — Bayesian posterior expectations are high-dimensional integrals, which is why MCMC exists rather than quadrature.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** (`s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash — **full key in [[00-Index]]**). **This chapter adds a new casualty: the substitution tables.** §7.3's three-row table of trigonometric substitutions, which is the section's entire content, extracts as an unstructured run in which the expression, the substitution and the identity interleave — **and since `2` is both "minus" and "two", $\sqrt{a^2-x^2}$ and $\sqrt{a^2+x^2}$ are not reliably distinguishable from the extraction alone.** **I reconstructed the table from the worked examples and verified each substitution by carrying it out.**
>
> **Figures lost, and two of them do real work:**
> - **The reference triangles of §7.3** — the whole method for substituting back depends on drawing a right triangle with sides $x$, $a$ and $\sqrt{a^2\pm x^2}$. **Without the picture, "$\sin\theta=x/\sqrt{x^2+4}$" is an assertion the reader must take on trust.** I have stated the triangles in words, which is a poor substitute.
> - **§7.7's trapezoid and Simpson diagrams**, showing straight lines and parabolas fitted to the curve. **The $1,4,2,4,\dots,1$ weighting pattern is inexplicable without them** — it is *why* Simpson's rule is what it is.
> - Also gone: every area diagram in §7.8 showing a region of infinite extent but finite area, which is the visual content of "an improper integral can converge".
>
> **Verification performed:** every integral in this chapter was computed symbolically with `sympy` and every numerical claim independently evaluated. Confirmed: all five by-parts examples, **including the circular case $\int e^x\sin x=\tfrac12e^x(\sin x-\cos x)$** (sympy's $-\tfrac{\sqrt2}2e^x\cos(x+\tfrac\pi4)$ is the same expression) and $\int_0^1xe^x=1$; $\int\sqrt{1-x^2}$ and its definite value $\tfrac\pi4$ **checked against the quarter-circle area**; the partial-fraction decompositions of $\frac{x+5}{x^2+x-2}$ and $\frac1{x^2-1}$ and both integrals; the trigonometric substitution for $\int\frac{dx}{x^2\sqrt{x^2+4}}$; **all seven improper integrals** ($1$, $\infty$, $2$, $\infty$, $1$, $2$, $\sqrt\pi$); and **the numerical experiment on $\int_0^1e^{-x^2}dx$ with $n=10$ — trapezoid $0.7462108$, Simpson $0.7468249$, true $0.7468241$, giving errors $6.1\times10^{-4}$ and $8.2\times10^{-7}$ and the 750-fold ratio quoted.** **No error was found in the text's mathematics.**
>
> **Scope note:** **§7.2 (trigonometric integrals) is compressed to its two-case rule**, since the material is drill on identities and nothing downstream needs $\int\sin^7x\cos^4x\,dx$. **§7.6 (integration using tables and technology) is omitted** — it is a guide to a printed table of integrals and to a computer-algebra interface, and both are better served by `sympy` today. **§7.5 (strategy) is kept and given prominence**, because deciding *which* technique to try is the actual skill and Stewart is unusually good on it. **§7.7 and §7.8 are expanded relative to Stewart's weighting**, because numerical integration and improper integrals are the two sections a data-science reader will use every week and the trigonometric ones are the two they will never use again.

#calculus #integration-by-parts #trigonometric-substitution #partial-fractions #numerical-integration #simpsons-rule #improper-integrals #p-test
