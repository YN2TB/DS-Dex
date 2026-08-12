---
subject: Calculus
chapter: 02
tags: [ds, calculus, derivative, chain-rule, implicit-differentiation, linear-approximation, differentials]
source: "Stewart, Clegg & Watson, *Calculus: Early Transcendentals*, 9th ed., §§2.7–2.8 and ch. 3 (pp. 140–278)"
---

# Derivatives

> [!abstract] What this chapter is for
> **The derivative has three descriptions, and the third is the one that survives into higher dimensions.**
>
> | Reading | Statement | Where it is used |
> |---|---|---|
> | **Slope** | slope of the tangent at $a$ | drawing graphs |
> | **Rate** | instantaneous rate of change | physics, economics, biology |
> | **Linear approximation** | $f(a+h)\approx f(a)+f'(a)h$ | **everything else** |
>
> **The third reading is what generalises.** In several variables there is no "the" tangent line, but there is still a best linear approximation — and it is the gradient ([[07 - Partial Derivatives and the Gradient|ch. 07]]). **Read the derivative this way from the start and the rest of the degree costs you nothing extra.**
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | The definition | A limit that is $\tfrac00$ at the point — which is why [[01 - Functions, Limits and Continuity\|ch. 01]] came first |
> | **2** | The rules | Power, product, quotient, and the derivatives of $e^x$, $\ln$, trig |
> | **3** | **The chain rule** | **The single most important formula in the chapter** — and backpropagation |
> | **4** | Implicit & logarithmic differentiation | Differentiate a curve you cannot solve for $y$ |
> | **5** | **Linear approximation and differentials** | $f(a+h)\approx f(a)+f'(a)h$, and error propagation |
>
> **If you learn one thing here, learn the chain rule properly** — not as a formula to apply but as "multiply the local rates along the composition". That reading is exactly what a neural network's gradient computation is.

---

## 📘 Main Knowledge

### 1. The derivative

> [!important] Definition
> $$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}=\lim_{x\to a}\frac{f(x)-f(a)}{x-a}$$
> when the limit exists; $f$ is then **differentiable at $a$**.

**The quotient is $\tfrac00$ at $h=0$** — which is precisely the indeterminate form [[01 - Functions, Limits and Continuity|ch. 01]] was built to handle. **Calculus could not begin before limits existed.**

**Notation:** $f'(x)$, $\dfrac{dy}{dx}$, $\dfrac{df}{dx}$, $Df$, $\dot y$ — all the same object. **$\frac{dy}{dx}$ is a single symbol, not a fraction**, though the chain rule and substitution both make it *behave* like one.

> [!important] Differentiable $\Rightarrow$ continuous, but not conversely
> If $f'(a)$ exists then $f$ is continuous at $a$: $\ f(x)-f(a)=\dfrac{f(x)-f(a)}{x-a}\cdot(x-a)\to f'(a)\cdot0=0$.
>
> **The converse fails in three distinct ways** *(all verified in Exercise 5)*:
> | Failure | Example at $0$ |
> |---|---|
> | **Corner** — one-sided derivatives differ | $\lvert x\rvert$ |
> | **Vertical tangent** — the limit is $\pm\infty$ | $x^{1/3}$ |
> | **Wild oscillation** | $x\sin\frac1x$ (extended by $0$) |
>
> **"Smooth" is strictly stronger than "unbroken".**

---

### 2. The differentiation rules

> [!important] The algebra rules
> $$(cf)'=cf',\qquad (f\pm g)'=f'\pm g'$$
> $$\boxed{(fg)'=f'g+fg'}\qquad\qquad \boxed{\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}}$$

> [!warning] The product rule is **not** $f'g'$
> **This is the most common single error in the subject.** $(x\cdot x)'=2x$, while $x'\cdot x'=1$.
>
> **A mnemonic for the quotient rule that also fixes the sign:** *"low d-high minus high d-low, over low squared"* — and **the minus sign is why the quotient rule is not symmetric**, unlike the product rule.

> [!important] The basic derivatives
> | $f$ | $f'$ | | $f$ | $f'$ |
> |---|---|---|---|---|
> | $x^n$ | $nx^{n-1}$ (**all real $n$**) | | $\sin x$ | $\cos x$ |
> | $e^x$ | $e^x$ | | $\cos x$ | $-\sin x$ |
> | $a^x$ | $a^x\ln a$ | | $\tan x$ | $\sec^2x$ |
> | $\ln x$ | $1/x$ | | $\arcsin x$ | $1/\sqrt{1-x^2}$ |
> | $\log_a x$ | $1/(x\ln a)$ | | $\arctan x$ | $1/(1+x^2)$ |
>
> *(All verified.)*

> [!tip] Why $e$ is the base that matters
> **$e$ is defined by $\lim_{h\to0}\frac{e^h-1}{h}=1$** — the base for which the exponential's own derivative is itself. Every other base pays a toll of $\ln a$.
>
> **Two consequences worth carrying forward.** $\frac{d}{dx}\ln x=\frac1x$ makes the logarithm the antiderivative of $1/x$, which is the one power the power rule cannot integrate ([[04 - Integrals|ch. 04]]). And **$\frac{d}{dx}\ln f=\frac{f'}{f}$ is the *relative* rate of change** — which is exactly an elasticity in [[Econometrics/contents/00-Index|Econometrics]] and the score function in [[Mathematical Statistics/contents/05 - Point Estimation|Math Stats ch. 05]].

---

### 3. The chain rule

> [!important] The Chain Rule
> $$\boxed{\ \frac{d}{dx}f\big(g(x)\big)=f'\big(g(x)\big)\cdot g'(x)\ }\qquad\text{or}\qquad \frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}$$

> [!tip] Read it as "rates multiply"
> **If $y$ changes 3 times as fast as $u$, and $u$ changes 5 times as fast as $x$, then $y$ changes 15 times as fast as $x$.** In Leibniz notation the $du$'s appear to cancel — **they do not, but the notation was designed so that they look as though they do, and it is a reliable guide.**
>
> **The linear-approximation reading makes it a theorem rather than a mnemonic:** near a point, $g$ acts like multiplication by $g'(x)$ and $f$ like multiplication by $f'(g(x))$. **Composing two multiplications multiplies the factors.**

> [!important] Nesting is just more factors
> $$\frac{d}{dx}f\big(g(h(x))\big)=f'\big(g(h(x))\big)\cdot g'\big(h(x)\big)\cdot h'(x)$$
> **and this continues to any depth — one factor per layer, each evaluated at that layer's input.**

> [!important] Backpropagation is this formula
> **A neural network is a composition $f_L\circ\cdots\circ f_2\circ f_1$ of a hundred or more layers**, and the gradient of the loss with respect to an early weight is a product of a hundred factors.
>
> **Two facts follow immediately:**
> - **Computing right-to-left costs $O(\text{depth})$ instead of $O(\text{depth}^2)$** — this is the entire algorithmic content of backpropagation, and it is why the "backward pass" exists.
> - **A product of many factors each slightly below 1 vanishes; each slightly above 1 explodes.** **Vanishing and exploding gradients are the chain rule's arithmetic, nothing more** ([[Machine Learning/contents/00-Index|Machine Learning]]).

**Worked examples** *(all verified)*:

$$\frac{d}{dx}\sin(x^2)=2x\cos(x^2),\qquad \frac{d}{dx}(3x^2+1)^5=30x(3x^2+1)^4,\qquad \frac{d}{dx}e^{\sin3x}=3\cos(3x)\,e^{\sin3x}$$

---

### 4. Implicit and logarithmic differentiation

> [!important] Implicit differentiation
> **When a curve is given by an equation you cannot (or need not) solve for $y$**, differentiate both sides with respect to $x$, treating $y$ as a function of $x$ — **so every $y$-term picks up a factor of $\frac{dy}{dx}$ by the chain rule** — then solve for $\frac{dy}{dx}$.

> [!example] The folium of Descartes: $x^3+y^3=6xy$
> Differentiating: $\ 3x^2+3y^2\dfrac{dy}{dx}=6y+6x\dfrac{dy}{dx}$, so
> $$\frac{dy}{dx}=\frac{x^2-2y}{2x-y^2}$$
> At $(3,3)$: $\ \dfrac{9-6}{6-9}=\boxed{-1}$, giving the tangent $y=-x+6$. *(Verified.)*
>
> **Solving $x^3+y^3=6xy$ for $y$ requires the cubic formula and produces three branches.** Implicit differentiation gets the tangent in two lines and never needs any of that.

> [!important] Logarithmic differentiation
> **For products of many factors, powers with variable exponents, or messy quotients:** take $\ln$ of both sides, differentiate implicitly, and multiply back by $y$.
>
> $$y=x^x\ \Rightarrow\ \ln y=x\ln x\ \Rightarrow\ \frac{y'}{y}=\ln x+1\ \Rightarrow\ \boxed{y'=x^x(\ln x+1)}$$
> *(Verified.)*

> [!warning] $x^x$ is neither a power nor an exponential
> **The power rule needs a constant exponent; the exponential rule needs a constant base.** $x^x$ has neither, so **both rules are wrong**, and answers like $x\cdot x^{x-1}$ or $x^x\ln x$ are the two standard errors.
>
> **The general fix is $u^v=e^{v\ln u}$**, which turns any variable-base-variable-exponent expression into something the chain rule handles.

---

### 5. Linear approximation and differentials

> [!important] The linearization
> $$L(x)=f(a)+f'(a)(x-a),\qquad f(x)\approx L(x)\ \text{ for }x\text{ near }a$$
> **The tangent line *is* the best linear approximation** — this is the definition of the derivative rearranged.

**Differentials:** $dy=f'(x)\,dx$ estimates the change in $y$ produced by a change $dx$ in $x$.

> [!example] $\sqrt{4.02}$
> Linearize $f(x)=\sqrt x$ at $a=4$: $f'(x)=\frac1{2\sqrt x}$, so $f'(4)=\frac14$ and
> $$\sqrt{4.02}\approx2+\tfrac14(0.02)=2.005$$
> **True value $2.00499377$; error $6.2\times10^{-6}$.** *(Verified.)*
>
> **The error is $\approx\frac12|f''|h^2$, so halving $h$ quarters it** — which is why linearization is excellent nearby and useless far away. **[[06 - Sequences, Series and Taylor Approximation|Ch. 06]] makes this exact.**

> [!important] Relative error propagates by multiplying the exponent
> Differentials give a clean rule for **error propagation**. For $y=x^n$,
> $$\frac{dy}{y}=n\,\frac{dx}{x}$$
> **A 1% error in the radius of a sphere gives a 3% error in its volume** ($V=\frac43\pi r^3$). *(Verified.)*
>
> **This is why measurement error in an input is not the same as error in an output**, and it is the deterministic cousin of the **delta method** in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]], where $\mathrm{Var}\big(g(X)\big)\approx\big(g'(\mu)\big)^2\mathrm{Var}(X)$ is this same first-order expansion applied to a random variable.

**Useful linearizations near $0$** — all first-order Taylor polynomials in advance:

$$(1+x)^k\approx1+kx,\qquad e^x\approx1+x,\qquad \ln(1+x)\approx x,\qquad \sin x\approx x$$

---

## ✏️ Exercises

> [!question] Exercise 1 — the rules *(warm-up)*
> Differentiate, naming the rule used.
> (i) $f(x)=3x^4-2x^2+7$
> (ii) $f(x)=(x^2+1)(x^3-2x)$ — **by the product rule and by expanding first.** Compare.
> (iii) $f(x)=\dfrac{x^2+1}{x-1}$
> (iv) $f(x)=x^x$

> [!example]- Solution
> **(i) Power rule term by term:** $f'(x)=\boxed{12x^3-4x}$
>
> **(ii) Product rule:**
> $$f'=2x(x^3-2x)+(x^2+1)(3x^2-2)=2x^4-4x^2+3x^4+x^2-2=\boxed{5x^4-3x^2-2}$$
> **By expanding first:** $f=x^5-x^3-2x$, so $f'=5x^4-3x^2-2$ ✓ — *(both verified, and they agree)*.
>
> **Expanding is easier here and impossible in general** — you cannot expand $\sin(x)\cdot e^{x^2}$. **The product rule earns its keep when the factors are not polynomials.**
>
> **(iii) Quotient rule:**
> $$f'=\frac{2x(x-1)-(x^2+1)(1)}{(x-1)^2}=\boxed{\frac{x^2-2x-1}{(x-1)^2}}$$
> *(Verified.)* **Note the numerator does not factor and the answer is not simplifiable** — that is normal, and trying to force it is wasted effort.
>
> **(iv) Neither power nor exponential rule applies.** Logarithmic differentiation:
> $$\ln y=x\ln x\ \Rightarrow\ \frac{y'}y=\ln x+1\ \Rightarrow\ \boxed{y'=x^x(\ln x+1)}$$
> *(Verified.)* **Sanity check:** $y'=0$ when $\ln x=-1$, i.e. $x=1/e$ — and $x^x$ does indeed have its minimum there.

> [!question] Exercise 2 — the chain rule
> Differentiate.
> (i) $\sin(x^2)$ and $\sin^2 x$ — **and explain why they differ.**
> (ii) $(3x^2+1)^5$
> (iii) $e^{\sin3x}$
> (iv) $\sin\big(\cos(\tan x)\big)$
> (v) If $F=f\circ g\circ h$ with $h(1)=2$, $g(2)=3$, $h'(1)=4$, $g'(2)=5$, $f'(3)=6$, find $F'(1)$.

> [!example]- Solution
> **(i)** $$\frac{d}{dx}\sin(x^2)=\cos(x^2)\cdot2x=\boxed{2x\cos(x^2)}$$
> $$\frac{d}{dx}\sin^2x=\frac{d}{dx}\big(\sin x\big)^2=2\sin x\cdot\cos x=\boxed{\sin2x}$$
> *(Both verified.)*
>
> **They differ because the compositions are in opposite orders.** $\sin(x^2)$ is *square then sine*; $\sin^2x$ is *sine then square*. **The notation hides this and the chain rule does not** — the outer function is whichever is applied last.
>
> **(ii)** $5(3x^2+1)^4\cdot6x=\boxed{30x(3x^2+1)^4}$ *(verified)*
>
> **(iii)** $e^{\sin3x}\cdot\cos(3x)\cdot3=\boxed{3\cos(3x)\,e^{\sin3x}}$ *(verified)* — **three layers, three factors.**
>
> **(iv)** Three layers again, working outward-in:
> $$\boxed{-\cos\big(\cos(\tan x)\big)\cdot\sin(\tan x)\cdot\sec^2x}$$
> *(Verified.)* **Each factor is a derivative evaluated at that layer's input** — write the layers down before differentiating and the bookkeeping cannot go wrong.
>
> **(v)** $F'(x)=f'\big(g(h(x))\big)\cdot g'\big(h(x)\big)\cdot h'(x)$, so
> $$F'(1)=f'(3)\cdot g'(2)\cdot h'(1)=6\cdot5\cdot4=\boxed{120}$$
>
> > [!important] This is a forward and a backward pass
> > **Notice the two directions.** You first go *forwards* to find where to evaluate ($h(1)=2$, then $g(2)=3$); then you multiply the derivatives *backwards*.
> >
> > **That is exactly backpropagation: a forward pass to record the intermediate values, then a backward pass multiplying local derivatives.** With three layers it is arithmetic; with three hundred it is the reason deep learning is computationally feasible at all.

> [!question] Exercise 3 — implicit and logarithmic differentiation
> (i) For $x^2+y^2=25$, find $\frac{dy}{dx}$ and the tangent at $(3,4)$. Check against the geometry.
> (ii) For the folium $x^3+y^3=6xy$, find $\frac{dy}{dx}$ and the tangent at $(3,3)$.
> (iii) Differentiate $y=(x^2+1)^{\sin x}$.
> (iv) Where does the folium have a horizontal tangent?

> [!example]- Solution
> **(i)** $2x+2y\frac{dy}{dx}=0$, so $\frac{dy}{dx}=-\frac xy$. At $(3,4)$: $\boxed{-\tfrac34}$, giving $y-4=-\tfrac34(x-3)$.
>
> **Geometric check: the radius to $(3,4)$ has slope $\tfrac43$, and the tangent to a circle is perpendicular to the radius** — and $-\tfrac34$ is indeed the negative reciprocal ✓. *(Verified.)*
>
> **(ii)** $3x^2+3y^2y'=6y+6xy'$, so $y'(3y^2-6x)=6y-3x^2$ and
> $$\frac{dy}{dx}=\frac{2y-x^2}{y^2-2x}=\frac{x^2-2y}{2x-y^2}$$
> At $(3,3)$: $\dfrac{9-6}{6-9}=\boxed{-1}$, tangent $y=-x+6$. *(Verified.)*
>
> **(iii)** Variable base **and** variable exponent — logarithmic differentiation:
> $$\ln y=\sin x\cdot\ln(x^2+1)$$
> $$\frac{y'}y=\cos x\cdot\ln(x^2+1)+\sin x\cdot\frac{2x}{x^2+1}$$
> $$\boxed{y'=(x^2+1)^{\sin x}\left[\cos x\,\ln(x^2+1)+\frac{2x\sin x}{x^2+1}}\right]$$
> *(Verified — sympy's form is algebraically identical.)*
>
> **The two terms have a clean reading: one from the exponent varying, one from the base varying.** Every "$u^v$" derivative has exactly this two-term shape.
>
> **(iv)** A horizontal tangent needs $\frac{dy}{dx}=0$, i.e. $x^2=2y$, so $y=\frac{x^2}2$. Substituting into the curve:
> $$x^3+\frac{x^6}8=6x\cdot\frac{x^2}2=3x^3\ \Longrightarrow\ \frac{x^6}8=2x^3\ \Longrightarrow\ x^3=16$$
> So $x=16^{1/3}=2\sqrt[3]2\approx2.520$ and $y=\frac{x^2}2\approx3.175$ *(and the trivial solution $x=0$, at the origin, where the curve crosses itself and the formula degenerates)*.
>
> **The point of the exercise: implicit differentiation locates features of a curve you could never graph by solving for $y$.**

> [!question] Exercise 4 — linear approximation and error
> (i) Linearize $f(x)=\sqrt x$ at $a=4$ and estimate $\sqrt{4.02}$. Compute the error.
> (ii) Estimate $\sqrt{4.5}$ with the same linearization. What happened?
> (iii) The radius of a sphere is measured as $10\,$cm with a possible error of $0.1\,$cm. Estimate the resulting error in the computed volume, absolutely and relatively.
> (iv) Show $(1+x)^k\approx1+kx$ near 0, and use it to estimate $1.02^{10}$.

> [!example]- Solution
> **(i)** $L(x)=2+\tfrac14(x-4)$, so $\sqrt{4.02}\approx2.005$.
> $$\text{true}=2.004993766,\qquad \text{error}=6.2\times10^{-6}$$
> *(Verified.)*
>
> **(ii)** $L(4.5)=2+\tfrac14(0.5)=2.125$, while $\sqrt{4.5}=2.121320$ — **error $3.7\times10^{-3}$, six hundred times larger.**
>
> **The step grew by a factor of 25 and the error by a factor of $\approx600\approx25^2$.** **Linearization error scales like $h^2$**, so it is superb nearby and degrades fast — which is exactly why [[06 - Sequences, Series and Taylor Approximation|ch. 06]] adds higher-order terms.
>
> **(iii)** $V=\tfrac43\pi r^3$ gives $dV=4\pi r^2\,dr$, so with $r=10$, $dr=0.1$:
> $$dV=4\pi(100)(0.1)=40\pi\approx\boxed{126\ \text{cm}^3}$$
> Relatively,
> $$\frac{dV}{V}=3\frac{dr}{r}=3(0.01)=\boxed{3\%}$$
> *(Verified.)*
>
> **The relative form is the useful one and it needs no numbers at all: the exponent multiplies the relative error.** A 1% error in a length is 2% in an area and 3% in a volume.
>
> **(iv)** $f(x)=(1+x)^k$ has $f(0)=1$ and $f'(0)=k$ *(verified)*, so $L(x)=1+kx$.
>
> With $k=10$, $x=0.02$: $\ 1.02^{10}\approx1+0.2=1.20$. **True value $1.21899$** — a 1.6% underestimate, because $x=0.02$ times $k=10$ is not really small.
>
> **This approximation is the reason "10% growth for 7 years roughly doubles" works**, and the reason it drifts: the error grows with $kx$, and compound-interest rules of thumb fail once rates or horizons get large.

> [!question] Exercise 5 — differentiability *(hard)*
> **(a)** Show each is continuous at 0 but not differentiable there, and name the failure.
> (i) $f(x)=|x|$  (ii) $g(x)=x^{1/3}$  (iii) $k(x)=x\sin\frac1x$ for $x\ne0$, $k(0)=0$
>
> **(b)** Let $F(x)=x^2\sin\frac1x$ for $x\ne0$, $F(0)=0$.
> (i) Show $F$ **is** differentiable at 0 and find $F'(0)$.
> (ii) Find $F'(x)$ for $x\ne0$.
> (iii) Show $F'$ is **not continuous at 0** — so a differentiable function need not have a continuous derivative.

> [!example]- Solution
> **(a)(i)** $|x|\to0=f(0)$, so continuous. But
> $$\lim_{h\to0^+}\frac{|h|}{h}=1,\qquad \lim_{h\to0^-}\frac{|h|}{h}=-1$$
> **The one-sided derivatives differ, so the limit does not exist — a *corner*.**
>
> **(ii)** $x^{1/3}$ is continuous everywhere, but
> $$\frac{h^{1/3}-0}{h}=h^{-2/3}\longrightarrow+\infty$$
> **The tangent is *vertical*: the slope exists geometrically and is not a number.**
>
> **(iii)** Continuous at 0 by the squeeze theorem ($|k(x)|\le|x|$ — [[01 - Functions, Limits and Continuity|ch. 01]], Exercise 2). But
> $$\frac{k(h)-k(0)}{h}=\frac{h\sin\frac1h}{h}=\sin\frac1h$$
> **which oscillates forever and has no limit** ([[01 - Functions, Limits and Continuity|ch. 01]], Exercise 5(b)). **Not differentiable — wild oscillation, with no tangent of any kind, vertical or otherwise.**
>
> **(b)(i)** Straight from the definition:
> $$F'(0)=\lim_{h\to0}\frac{h^2\sin\frac1h-0}{h}=\lim_{h\to0}h\sin\frac1h=0$$
> by the squeeze theorem. **So $\boxed{F'(0)=0}$** — the extra factor of $h$ is exactly what (a)(iii) lacked.
>
> **(ii)** For $x\ne0$, product and chain rules:
> $$F'(x)=2x\sin\frac1x+x^2\cos\frac1x\cdot\left(-\frac1{x^2}\right)=\boxed{2x\sin\frac1x-\cos\frac1x}$$
> *(Verified.)*
>
> **(iii)** As $x\to0$ the first term $\to0$ (squeeze), **but $\cos\frac1x$ oscillates between $-1$ and $1$ forever.** Evaluating:
> | $x$ | $0.1$ | $0.01$ | $0.001$ | $0.0001$ |
> |---|---|---|---|---|
> | $F'(x)$ | $0.730$ | $-0.872$ | $-0.561$ | $0.952$ |
>
> *(Verified.)* **$\lim_{x\to0}F'(x)$ does not exist, while $F'(0)=0$ — so $F'$ is not continuous at 0.**
>
> > [!important] Why this example matters
> > **$F$ is differentiable everywhere, and $F'$ is not continuous.** So the classes are strictly nested:
> > $$\text{differentiable}\ \subsetneq\ \text{continuous},\qquad \text{continuously differentiable }(C^1)\ \subsetneq\ \text{differentiable}$$
> >
> > **This is why theorems specify "$C^1$" or "$f''$ continuous" rather than just "differentiable".** Clairaut's theorem on mixed partials ([[07 - Partial Derivatives and the Gradient|ch. 07]]) and the second-derivative test ([[03 - Applications of Differentiation|ch. 03]]) both need continuity of derivatives, not mere existence — and examples like this one are why.
> >
> > **In applied terms:** an optimizer that assumes a smoothly-varying gradient can fail on a function that is differentiable but whose gradient jumps around, which is one reason ReLU networks — differentiable almost everywhere with a discontinuous derivative — behave differently from smooth ones.

---

## 📝 Summary

- **$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$** — slope, rate, and **best linear approximation**. **The third reading is the one that survives into several variables.**
- **Differentiable $\Rightarrow$ continuous, never the reverse.** Failure comes as a **corner** ($|x|$), a **vertical tangent** ($x^{1/3}$), or **oscillation** ($x\sin\frac1x$).
- **$(fg)'=f'g+fg'$ and $\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$** — the product rule is **not** $f'g'$, and the quotient rule's minus sign makes it order-sensitive.
- **$\frac{d}{dx}e^x=e^x$ defines $e$**, and $\frac{d}{dx}\ln f=\frac{f'}{f}$ is the **relative** rate of change — an elasticity, and the score function.
- $$\boxed{\frac{d}{dx}f(g(x))=f'(g(x))\,g'(x)}$$ **— rates multiply, one factor per layer, each evaluated at that layer's input.** **This is backpropagation**, and it explains both the forward/backward two-pass structure and vanishing/exploding gradients.
- **Implicit differentiation** treats $y$ as a function of $x$, so every $y$-term gains a $\frac{dy}{dx}$ — and it finds tangents to curves that cannot be solved for $y$ at all.
- **Logarithmic differentiation** handles products of many factors and **variable-base-variable-exponent** expressions like $x^x$, where **both** the power rule and the exponential rule are wrong.
- **$f(x)\approx f(a)+f'(a)(x-a)$**, with error $\approx\frac12|f''|h^2$ — **excellent nearby, degrading quadratically.** $\sqrt{4.02}$ is right to six decimals; $\sqrt{4.5}$ to two.
- **Differentials propagate error:** $\frac{dy}{y}=n\frac{dx}{x}$ for $y=x^n$, so **1% in a radius is 3% in a volume.** This is the deterministic form of the delta method.
- **The standard linearizations $(1+x)^k\approx1+kx$, $e^x\approx1+x$, $\ln(1+x)\approx x$, $\sin x\approx x$** are first-order Taylor polynomials, and they are behind every rule of thumb about small rates.

---

## ⚠️ Important Notes

> [!warning] The product rule, and the missing inner derivative
> $$(fg)'\ne f'g'\qquad\qquad \frac{d}{dx}\sin(x^2)\ne\cos(x^2)$$
> **These two are the most frequent errors in the subject, and the second is worse** because the answer *looks* right.
>
> **A habit that prevents it: name the layers before differentiating.** For $\sin(x^2)$ write "outer $=\sin$, inner $=x^2$" and produce one factor for each. **With three layers (Exercise 2(iv)) there is no other reliable method.**

> [!warning] $\frac{dy}{dx}$ is not a fraction — except where it is
> **It is a single symbol.** But it *behaves* like a fraction in exactly two places, and both are theorems rather than notation:
> - **the chain rule** $\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}$;
> - **separable equations and substitution**, where $du=g'(x)dx$ ([[04 - Integrals|ch. 04]]).
>
> **Everywhere else the analogy misleads** — $\frac{d^2y}{dx^2}$ is not $\left(\frac{dy}{dx}\right)^2$, and $\frac{\partial y}{\partial x}$'s in several variables genuinely do **not** cancel ([[07 - Partial Derivatives and the Gradient|ch. 07]]).

> [!warning] $x^x$ obeys neither rule
> $$\frac{d}{dx}x^x\ne x\cdot x^{x-1}\qquad\text{and}\qquad \frac{d}{dx}x^x\ne x^x\ln x$$
> **The power rule needs a constant exponent; the exponential rule needs a constant base.** The answer is $x^x(\ln x+1)$, with **both** terms present.
>
> **The universal fix: rewrite $u^v$ as $e^{v\ln u}$.** It never fails and it explains why the answer has two terms.

> [!warning] Linear approximation degrades quadratically
> | Step $h$ | error for $\sqrt{4+h}$ |
> |---|---|
> | $0.02$ | $6.2\times10^{-6}$ |
> | $0.5$ | $3.7\times10^{-3}$ |
>
> **A 25-fold larger step gave a $\approx600$-fold larger error** — the $h^2$ law.
>
> **So "linearize and forget" is safe only for genuinely small perturbations.** Compound-growth rules of thumb, the delta method, and Newton's method all inherit this: **they are excellent locally and give no warning when you have strayed too far.**

> [!warning] Differentiable does not mean $C^1$
> $F(x)=x^2\sin\frac1x$ (with $F(0)=0$) is differentiable everywhere, and $F'$ is **discontinuous** at 0 (Exercise 5(b)).
>
> **This is why theorem hypotheses say "continuously differentiable" or "$f''$ continuous"** — Clairaut's theorem, the second-derivative test and Taylor's theorem with remainder all need more than mere existence of the derivatives.
>
> **When a theorem's hypothesis mentions continuity of a derivative, it is not boilerplate.**

> [!note] Cross-subject connections
> - [[01 - Functions, Limits and Continuity|Ch. 01]] — the derivative is a $\tfrac00$ limit, which is why limits had to come first; the squeeze theorem does the work in Exercise 5.
> - [[03 - Applications of Differentiation|Ch. 03]] — $f'$ locates extrema, $f''$ decides their type, and **Newton's method is linear approximation solved for the root.**
> - [[06 - Sequences, Series and Taylor Approximation|Ch. 06]] — the linearization is the degree-1 Taylor polynomial; **the $h^2$ error law becomes an exact remainder formula.**
> - [[07 - Partial Derivatives and the Gradient|Ch. 07]] — the multivariable chain rule is this one with a sum over paths; **the gradient is the linear-approximation reading generalised.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **backpropagation is the chain rule** with a forward pass to record activations and a backward pass to multiply local derivatives; **vanishing and exploding gradients are products of many factors.**
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — the **delta method** is Exercise 4(iii) with a random variable; the **score function** is $\frac{d}{d\theta}\ln L=\frac{L'}{L}$.
> - [[Econometrics/contents/00-Index|Econometrics]] — an **elasticity** is $\frac{d\ln y}{d\ln x}$, and log-linear coefficients are read as approximate percentages **because $\ln(1+x)\approx x$.**
> - [[Optimization/contents/00-Index|Optimization]] — gradient descent steps along the linear approximation; Newton's method uses the quadratic one.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The extraction cipher applies throughout** — `s`/`d` for parentheses, `−` for `=`, isolated ` 1 `/` 2 ` for $+$/$-$, `l` for $\to$, `y` for the fraction slash. **The full key is in [[00-Index]].** **In this chapter the cipher is particularly destructive**, because a derivative formula is mostly signs and exponents: `f 9sxd − 2x` is $f'(x)=2x$, with the prime rendered as `9`. **Every derivative quoted in these notes was recomputed symbolically rather than read from the extraction.**
>
> **Figures lost — and here the losses are pedagogically central.** Gone entirely: the secant-lines-approaching-a-tangent animation frames (§2.7), which are the *motivation* for the whole definition; the graphs of $f$ beside $f'$ (§2.8) that make "where $f$ is increasing, $f'>0$" visible; **the corner, vertical-tangent and oscillation pictures** for the three failures of differentiability; the folium of Descartes (§3.5), whose self-intersection at the origin explains why the implicit formula degenerates there; and the zoom-in sequences showing a curve becoming indistinguishable from its tangent (§3.10) — **which is the single best argument for the linear-approximation reading and has no verbal substitute.**
>
> **Verification performed:** every derivative, tangent and numerical estimate in this chapter was computed symbolically with `sympy` and, where numerical, cross-checked. Confirmed: all eight basic derivatives in the table of §2; the product-rule example **both ways** ($5x^4-3x^2-2$ by the rule and by expanding); the quotient-rule example; all four chain-rule examples including the three-layer nesting; **the folium's derivative $\frac{x^2-2y}{2x-y^2}$ and its value $-1$ at $(3,3)$**; the circle's $-\frac34$ at $(3,4)$ and its perpendicularity to the radius; $\frac{d}{dx}x^x=x^x(\ln x+1)$; the logarithmic derivative of $(x^2+1)^{\sin x}$; **both linear-approximation errors ($6.2\times10^{-6}$ at $h=0.02$ and $3.7\times10^{-3}$ at $h=0.5$)**; the sphere's 3% relative error; $1.02^{10}=1.21899$ against the estimate $1.20$; and **all four tabulated values of $F'(x)$ near 0 in Exercise 5**, confirming the oscillation. **No error was found in the text's mathematics.**
>
> **Scope note:** **§3.3 (trigonometric derivatives) is compressed to its table**, since the geometric proof via $\lim_{\theta\to0}\frac{\sin\theta}\theta=1$ is standard and the results are what get used. **§3.7 (rates of change in the sciences), §3.8 (exponential growth and decay), §3.9 (related rates) and §3.11 (hyperbolic functions) are omitted.** §§3.7–3.9 are applications of rules already covered — related-rates problems in particular are implicit differentiation plus a word problem, and no downstream subject in this vault needs them. **§3.8's exponential model $y'=ky\Rightarrow y=y_0e^{kt}$ is worth knowing and appears in [[Linear Algebra/contents/03 - Determinants and Diagonalization|Linear Algebra ch. 03]]** as the continuous-time dynamical system. **Hyperbolic functions are used nowhere downstream** except as activation functions, where only $\tanh$ and its derivative $1-\tanh^2$ matter.

#calculus #derivative #chain-rule #product-rule #implicit-differentiation #logarithmic-differentiation #linear-approximation #differentials
