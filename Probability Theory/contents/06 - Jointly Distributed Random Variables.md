---
subject: Probability Theory
chapter: 06
tags: [ds, probability, joint-distribution, independence, convolution, order-statistics, bivariate-normal]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 6 (pp. 249–314)"
---

# Jointly Distributed Random Variables

> [!abstract] What this chapter is for
> **Everything so far has described one random variable at a time.** That is almost never enough: height *and* weight, feature *and* label, today's price *and* tomorrow's. This chapter is the machinery for **several random variables at once**, and it is the point at which probability starts to look like statistics.
>
> Three questions organise the whole chapter:
>
> 1. **How do they behave together?** → joint pmf / joint density
> 2. **Does knowing one tell you about the other?** → independence, and conditional distributions when the answer is *yes*
> 3. **What is the distribution of a function of them?** → convolution, order statistics, the Jacobian
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Joint distributions | **Marginals are sums/integrals over the other variable** — and marginals do *not* determine the joint |
> | **2** | Independence | **Factorisation** — but the *region* must factor too |
> | **3** | Sums | **Convolution**; normal, Poisson, gamma and binomial families are closed under it |
> | **4–5** | Conditional distributions | Same definition as [[03 - Conditional Probability and Independence\|ch. 03]], now indexed by a value |
> | **6** | Order statistics | The distribution of the min, max, median and range |
> | **7** | Functions of several variables | **The Jacobian** — [[05 - Continuous Random Variables\|ch. 05 §7]] in $n$ dimensions |
> | **8** | Exchangeability | Symmetric, but **not** independent — the honest weakening of i.i.d. |
>
> **The single most useful result in the chapter is §5's bivariate normal:** the conditional distribution of $Y$ given $X=x$ is *normal, with a mean linear in $x$ and a variance that does not depend on $x$*. **That is the population statement of linear regression** — see [[Econometrics/contents/00-Index|Econometrics]].

---

## 📘 Main Knowledge

### 1. Joint distribution functions

For any two random variables $X$ and $Y$, the **joint cumulative distribution function** is

$$F(a,b) = P\{X\le a,\; Y\le b\},\qquad -\infty<a,b<\infty$$

In principle every probability statement about the pair follows from $F$. The key computational identity — the two-dimensional analogue of $P\{a<X\le b\}=F(b)-F(a)$ — is **inclusion–exclusion on a rectangle**:

$$P\{a_1<X\le a_2,\; b_1<Y\le b_2\} = F(a_2,b_2) - F(a_1,b_2) - F(a_2,b_1) + F(a_1,b_1)$$

> [!note] Why the $+$ at the end
> $F(a_2,b_2)$ counts the whole quadrant. Subtracting $F(a_1,b_2)$ and $F(a_2,b_1)$ removes the two strips you don't want — **but the corner $F(a_1,b_1)$ has now been removed twice**, so it must be added back. This is exactly [[02 - Axioms of Probability|Proposition 4.4]] with two events.

**Marginal distributions** are recovered by letting the other variable run free:

$$F_X(a)=\lim_{b\to\infty}F(a,b),\qquad F_Y(b)=\lim_{a\to\infty}F(a,b)$$

#### 1a. The discrete case

The **joint probability mass function** is $p(x,y)=P\{X=x, Y=y\}$, and the marginals are obtained by summing out:

$$p_X(x)=\sum_j p(x,y_j),\qquad p_Y(y)=\sum_i p(x_i,y)$$

The name is literal: written as a table, **the marginal of $X$ is the row sums and the marginal of $Y$ is the column sums — they live in the margins.**

> [!example] Example 1a — three balls from an urn of 3 red, 4 white, 5 blue
> Let $X$ = number of red, $Y$ = number of white among 3 drawn without replacement. Then
> $$p(i,j)=\frac{\binom3i\binom4j\binom5{3-i-j}}{\binom{12}3}$$
> which is a **multivariate hypergeometric**. With $\binom{12}3=220$:
>
> | $i \backslash j$ | 0 | 1 | 2 | 3 | **row sum $=P\{X=i\}$** |
> |---|---|---|---|---|---|
> | **0** | $\tfrac{10}{220}$ | $\tfrac{40}{220}$ | $\tfrac{30}{220}$ | $\tfrac4{220}$ | $\tfrac{84}{220}$ |
> | **1** | $\tfrac{30}{220}$ | $\tfrac{60}{220}$ | $\tfrac{18}{220}$ | $0$ | $\tfrac{108}{220}$ |
> | **2** | $\tfrac{15}{220}$ | $\tfrac{12}{220}$ | $0$ | $0$ | $\tfrac{27}{220}$ |
> | **3** | $\tfrac1{220}$ | $0$ | $0$ | $0$ | $\tfrac1{220}$ |
> | **col sum $=P\{Y=j\}$** | $\tfrac{56}{220}$ | $\tfrac{112}{220}$ | $\tfrac{48}{220}$ | $\tfrac4{220}$ | |
>
> **Notice the zeros in the upper-right and lower-right.** $X$ and $Y$ are strongly dependent — they compete for the same three draws, so large $X$ forces small $Y$. **The marginals alone would never reveal this.**

> [!warning] Marginals do not determine the joint distribution
> Table 6.1 and a table in which $X$ and $Y$ are *independent* with the same row and column sums are different joint distributions with **identical marginals**. **You cannot reconstruct a joint distribution from its margins** — this is the entire reason joint distributions are a separate object of study, and the reason "correlation is not in the marginals" ([[07 - Properties of Expectation|ch. 07]]).

#### 1b. The jointly continuous case

$X$ and $Y$ are **jointly continuous** if there is a function $f(x,y)$ with

$$P\{(X,Y)\in C\}=\iint_{(x,y)\in C} f(x,y)\,dx\,dy$$

for every region $C$ in the plane. Then

$$f(a,b)=\frac{\partial^2}{\partial a\,\partial b}F(a,b),\qquad
P\{a<X<a+da,\; b<Y<b+db\}\approx f(a,b)\,da\,db$$

and the **marginal densities** integrate out the other variable:

$$f_X(x)=\int_{-\infty}^{\infty}f(x,y)\,dy,\qquad f_Y(y)=\int_{-\infty}^{\infty}f(x,y)\,dx$$

> [!warning] "Marginal" always means *integrate out*, never *set to zero*
> $f_X(x)\ne f(x,0)$. To get the marginal you must **account for every value the other variable could have taken** — that is what integrating does. Setting $y=0$ is a *slice*, and a slice is (after normalising) a **conditional** density, which is §5.

> [!example] Example 1e — a uniform point in a disc of radius $R$
> $f(x,y)=\tfrac1{\pi R^2}$ on $x^2+y^2\le R^2$. Then
> $$f_X(x)=\frac{2}{\pi R^2}\sqrt{R^2-x^2},\qquad |x|\le R$$
> **The marginal of a uniform is not uniform.** The density of $X$ is largest at $x=0$ because the disc is *widest* there — more $y$-values are available. If $D=\sqrt{X^2+Y^2}$ is the distance from the centre,
> $$F_D(a)=\frac{\pi a^2}{\pi R^2}=\frac{a^2}{R^2},\qquad f_D(a)=\frac{2a}{R^2},\qquad \mathbb{E}[D]=\frac{2R}{3}$$
> **$f_D$ increases in $a$: a random point in a disc is far more likely to be near the rim than near the centre**, because area grows like $a^2$. This is the same "area beats proximity" effect that drives Bertrand's paradox in [[05 - Continuous Random Variables|ch. 05]].

#### 1c. The multinomial distribution

$n$ independent trials, each landing in one of $r$ categories with probabilities $p_1,\dots,p_r$ summing to 1. If $X_i$ counts the trials in category $i$,

$$P\{X_1=n_1,\dots,X_r=n_r\}=\frac{n!}{n_1!\,n_2!\cdots n_r!}\,p_1^{n_1}p_2^{n_2}\cdots p_r^{n_r},\qquad \sum n_i=n$$

Two facts worth memorising:

- **$r=2$ gives the binomial** — the multinomial is the binomial with more than two outcomes.
- **Any pooled subset is binomial:** if $N\subset\{1,\dots,r\}$ then $\sum_{i\in N}X_i\sim\text{Bin}\!\left(n,\sum_{i\in N}p_i\right)$, because "landed in $N$" is itself a two-outcome trial.

> [!example] The "no three share a birthday" problem
> Using the multinomial: no set of three shares a birthday iff every day is the birthday of **at most 2** people. Partitioning the 365 days into groups of size $i$ (used twice), $n-2i$ (used once) and $365-n+i$ (unused),
> $$P\{\text{no three alike}\}=\sum_{i=0}^{\lfloor n/2\rfloor}\frac{365!}{i!\,(n-2i)!\,(365-n+i)!}\cdot\frac{n!}{2^i}\left(\frac1{365}\right)^{n}$$
> **The probability is exactly 0 once $n>730$** (pigeonhole: $365\times2$).
>
> > [!warning]- The value printed for $n=88$ is wrong
> > Ross states this sum $\approx.504$ at $n=88$. **Recomputing it in exact log-gamma arithmetic gives $.4889$, confirmed by a 400,000-run simulation ($.4894$).** The value $.504$ is the answer for $n=87$ ($.50055$). **The correct threshold is $n=87$: it is at 88 people that a shared-birthday-triple becomes more likely than not.**
> >
> > Note that this also corrects the **Poisson approximation of [[04 - Random Variables|ch. 04]]**, which gave $n\approx84$ from $\binom n3/365^2=\log2$. **The approximation is off by three people** — a useful calibration of how rough the Poisson paradigm can be when the "rare events" are not quite independent.

---

### 2. Independent random variables

$X$ and $Y$ are **independent** if for all sets $A,B$

$$P\{X\in A,\, Y\in B\}=P\{X\in A\}\,P\{Y\in B\}$$

equivalently, for all $a,b$: $F(a,b)=F_X(a)F_Y(b)$; equivalently $p(x,y)=p_X(x)p_Y(y)$ (discrete) or $f(x,y)=f_X(x)f_Y(y)$ (continuous).

**In words: knowing the value of one does not change the distribution of the other.**

#### 2a. The factorisation criterion — and its trap

> [!important] Proposition 2.1
> $X$ and $Y$ are independent **if and only if** their joint density (or mass function) can be written
> $$f_{X,Y}(x,y)=h(x)\,g(y)\qquad\text{for all }-\infty<x,y<\infty$$
> **The constants need not be right** — normalisation takes care of itself.

The clause **"for all $x,y$"** is doing enormous work, and is where nearly all mistakes happen.

> [!warning] The region must factor too
> Compare Ross's Example 2f:
>
> | Density | Region | Independent? |
> |---|---|---|
> | $6e^{-2x}e^{-3y}$ | $x>0,\ y>0$ | **Yes** — $\text{Exp}(2)\perp\text{Exp}(3)$ |
> | $24xy$ | $0<x,\ 0<y,\ x+y<1$ | **No** |
>
> The second density *looks* factored — $24xy = (24x)(y)$. **But writing it honestly on the whole plane,**
> $$f(x,y)=24xy\cdot\mathbb{1}\{0<x<1,\,0<y<1,\,x+y<1\}$$
> **and the indicator does not factor.** Knowing $X=0.9$ forces $Y<0.1$.
>
> **The test to apply first, before any algebra: is the support a rectangle (possibly infinite)?** If it is not — triangles, discs, $\{y<x\}$ — **the variables are dependent, full stop.**

> [!example] Example 2b — Poisson thinning
> $N\sim\text{Poisson}(\lambda)$ people enter a post office; each is independently male with probability $p$. Then the counts $X$ (male) and $Y$ (female) satisfy
> $$P\{X=i,Y=j\}=e^{-\lambda p}\frac{(\lambda p)^i}{i!}\cdot e^{-\lambda(1-p)}\frac{[\lambda(1-p)]^j}{j!}$$
> **$X$ and $Y$ are independent Poissons with means $\lambda p$ and $\lambda(1-p)$.**
>
> **This is genuinely surprising and genuinely important.** With a *fixed* total $n$, the counts are perfectly negatively dependent ($Y=n-X$). **It is the Poisson randomness of the total that decouples them** — Poisson variability is exactly the amount needed to erase the constraint. This "**Poisson thinning**" property is the foundation of the Poisson process in [[09 - Additional Topics in Probability|ch. 09]].

> [!example] Example 2d — Buffon's needle
> A needle of length $L$ dropped on a floor ruled with parallel lines a distance $D\ge L$ apart. With $X$ = distance from the needle's midpoint to the nearest line ($\sim U(0,D/2)$) and $\Theta$ = angle ($\sim U(0,\pi/2)$), independent, the needle crosses a line iff $X<\tfrac L2\cos\Theta$, giving
> $$P\{\text{cross}\}=\frac{4}{\pi D}\int_0^{\pi/2}\int_0^{(L/2)\cos y}dx\,dy=\frac{2L}{\pi D}$$
> **This is a way of estimating $\pi$ by throwing needles** — historically the first Monte Carlo method, and the ancestor of [[10 - Simulation|ch. 10]].

> [!example] Example 2j — independence you cannot see directly, but can see backwards
> In craps, having thrown a 4, let $N$ be the number of throws until a 4 or 7 appears and $X$ the value that appears. **Is $N$ independent of $X$?** Not obvious.
>
> **Turn the question around.** Given that it took $n$ throws, is the final value more likely to be 4 or 7? Clearly not affected — the first $n-1$ throws were neither 4 nor 7, which says nothing about which comes first at throw $n$. **So $X$ is independent of $N$, hence $N$ is independent of $X$.**
>
> **Independence is symmetric, and one direction is often much easier to see.** Same trick for record values: $P(A_n\mid A_{n+1})=P(A_n)=1/n$ because knowing $X_{n+1}$ beats all of $X_1,\dots,X_n$ says nothing about the internal ordering of the first $n$. **When stuck, swap the roles.**

For $n$ variables, independence means $P\{X_1\in A_1,\dots,X_n\in A_n\}=\prod_i P\{X_i\in A_i\}$ — and, exactly as in [[03 - Conditional Probability and Independence|ch. 03]], **this is genuinely stronger than pairwise independence.**

---

### 3. Sums of independent random variables

If $X\perp Y$ are continuous, the cdf and density of $X+Y$ are given by **convolution**:

$$F_{X+Y}(a)=\int_{-\infty}^{\infty}F_X(a-y)f_Y(y)\,dy
\qquad\Longrightarrow\qquad
\boxed{\,f_{X+Y}(a)=\int_{-\infty}^{\infty}f_X(a-y)f_Y(y)\,dy\,}$$

**Read it as a weighted average:** to land at $a$, $Y$ takes some value $y$ (weight $f_Y(y)$) and $X$ must supply the remainder $a-y$ (density $f_X(a-y)$).

#### 3a. Uniforms — and a beautiful consequence

The sum of two independent $U(0,1)$s has the **triangular density** $f(a)=a$ on $[0,1]$, $2-a$ on $(1,2)$. For $n$ of them, induction on the convolution gives

$$F_n(x)=P\{X_1+\dots+X_n\le x\}=\frac{x^n}{n!},\qquad 0\le x\le 1$$

> [!tip] How many uniforms must you add to exceed 1? On average, $e$.
> Let $N=\min\{n: X_1+\dots+X_n>1\}$. Then $P\{N>n\}=F_n(1)=1/n!$, so
> $$\mathbb{E}[N]=\sum_{n=0}^{\infty}P\{N>n\}=\sum_{n=0}^{\infty}\frac1{n!}=e\approx2.718$$
> **$e$ arriving from an experiment with no exponentials anywhere in it** — one of the prettiest results in the book, and a nice simulation check for [[10 - Simulation|ch. 10]].

#### 3b. Gamma and chi-squared

> [!important] Proposition 3.1 — the gamma family is closed under convolution (at fixed rate)
> $$X\sim\Gamma(s,\lambda),\ Y\sim\Gamma(t,\lambda),\ X\perp Y \quad\Longrightarrow\quad X+Y\sim\Gamma(s+t,\lambda)$$
> **The shape parameters add; the rate must be shared.**

Immediate consequences:

- **The sum of $n$ i.i.d. $\text{Exp}(\lambda)$ is $\Gamma(n,\lambda)$** — because $\text{Exp}(\lambda)=\Gamma(1,\lambda)$. *This is the fact promised but not proved in [[05 - Continuous Random Variables|ch. 05 §6]].*
- **$Z^2\sim\Gamma(\tfrac12,\tfrac12)$ for $Z$ standard normal**, so $\chi^2_n=\sum_{i=1}^n Z_i^2\sim\Gamma\!\left(\tfrac n2,\tfrac12\right)$ with density
$$f_Y(y)=\frac{e^{-y/2}y^{n/2-1}}{2^{n/2}\Gamma(n/2)},\qquad y>0$$
- **A by-product:** $\Gamma\!\left(\tfrac12\right)=\sqrt\pi$, and hence $\Gamma\!\left(\tfrac52\right)=\tfrac32\cdot\tfrac12\cdot\sqrt\pi=\tfrac34\sqrt\pi$.

**The chi-squared distribution is not an arbitrary definition** — it is "the squared length of a standard normal vector", which is why it governs sums of squared residuals throughout [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

#### 3c. Normal random variables — the closure property that runs statistics

> [!important] Proposition 3.2
> $X_i\sim N(\mu_i,\sigma_i^2)$ independent $\Longrightarrow$ $\displaystyle\sum_{i=1}^n X_i \sim N\!\left(\sum\mu_i,\ \sum\sigma_i^2\right)$
>
> **Means add. Variances add. Standard deviations do *not* add.**

> [!warning] The most common numerical error in the whole chapter
> $$\mathrm{SD}(X+Y)=\sqrt{\sigma_X^2+\sigma_Y^2}\ \ne\ \sigma_X+\sigma_Y$$
> and for a **difference** the variances still **add**:
> $$\mathrm{Var}(X-Y)=\sigma_X^2+\sigma_Y^2$$
> **Subtracting independent quantities makes the result *more* variable, not less.** Two sources of noise cannot cancel just because they enter with opposite signs. *(Exercise 3(iii) is built on this.)*

> [!example] Example 3c — the basketball season
> 26 games vs class A ($p=.4$), 18 vs class B ($p=.7$), independent.
> $$\mathbb{E}[X_A]=10.4,\ \mathrm{Var}=6.24;\qquad \mathbb{E}[X_B]=12.6,\ \mathrm{Var}=3.78$$
> By the normal approximation to each binomial plus Proposition 3.2, $X_A+X_B\approx N(23,\,10.02)$, so with the **continuity correction**
> $$P\{X_A+X_B\ge25\}\approx P\!\left\{Z\ge\tfrac{1.5}{\sqrt{10.02}}=.4739\right\}=.3178$$
> and $X_A-X_B\approx N(-2.2,\,10.02)$ gives $P\{X_A>X_B\}\approx P\{Z\ge.8530\}=.1968$.
>
> **Exact binomial convolution gives $.3182$ and $.1958$** — the approximation is excellent for the sum and about half a percentage point off for the difference. **Note $\mathrm{Var}(X_A-X_B)=10.02$, the same as for the sum.**

#### 3d. Lognormal — the standard model for prices

$Y$ is **lognormal** with parameters $\mu,\sigma$ if $\log Y\sim N(\mu,\sigma^2)$, i.e. $Y=e^X$.

> [!example] Example 3d — a security's weekly price ratios
> $S(n)/S(n-1)$ i.i.d. lognormal with $\mu=.0165$, $\sigma=.0730$.
> - **Up in a given week:** $P\{\log\text{ratio}>0\}=\Phi(.0165/.0730)=\Phi(.2260)=.5894$.
> - **Up in *each* of two weeks:** $(.5894)^2=.3474$ by independence.
> - **Higher after two weeks:** the *log* ratios add, so $\log\frac{S(2)}{S(0)}\sim N(.0330,\,2(.0730)^2)$ and
> $$P=\Phi\!\left(\frac{.0330}{.0730\sqrt2}\right)=\Phi(.31965)=.6254$$
>
> **$.6254 \ne .3474$, and the gap is the whole point.** "Up over two weeks" is far more likely than "up in both weeks" — a bad week can be outweighed by a good one. **Confusing the two is a real modelling error in finance.**
>
> **Why lognormal at all:** prices are products of ratios, and **logs turn products into sums** — the one operation the normal family is closed under. This is the model behind Black–Scholes, and the reason returns are analysed in logs; see [[Time-series Analysis/contents/00-Index|Time-series Analysis]].

#### 3e. Poisson and binomial

$$X\sim\text{Poisson}(\lambda_1),\ Y\sim\text{Poisson}(\lambda_2),\ X\perp Y\ \Longrightarrow\ X+Y\sim\text{Poisson}(\lambda_1+\lambda_2)$$
$$X\sim\text{Bin}(n,p),\ Y\sim\text{Bin}(m,p),\ X\perp Y\ \Longrightarrow\ X+Y\sim\text{Bin}(n+m,p)$$

**The binomial result needs no computation at all** — $X+Y$ counts successes in $n+m$ independent trials with the same $p$. *(The algebraic route works too, and lands on Vandermonde's identity from [[01 - Combinatorial Analysis|ch. 01]].)*

> [!warning] The binomial closure requires a **common $p$**
> $\text{Bin}(n,p_1)+\text{Bin}(m,p_2)$ is **not** binomial when $p_1\ne p_2$ — Example 3c is exactly this case, which is why it had to be handled by normal approximation rather than exactly. **Poisson has no such restriction; binomial does.**

---

### 4. Conditional distributions: the discrete case

$$p_{X\mid Y}(x\mid y)=P\{X=x\mid Y=y\}=\frac{p(x,y)}{p_Y(y)}\qquad\text{whenever } p_Y(y)>0$$

**This is just $P(E\mid F)=P(EF)/P(F)$ from [[03 - Conditional Probability and Independence|ch. 03]] with $E=\{X=x\}$, $F=\{Y=y\}$** — nothing new is being defined. If $X\perp Y$ the conditional pmf equals the unconditional one.

> [!example] Example 4b — the binomial hiding inside two Poissons
> $X\sim\text{Poisson}(\lambda_1)\perp Y\sim\text{Poisson}(\lambda_2)$. Then
> $$X\mid \{X+Y=n\}\ \sim\ \text{Bin}\!\left(n,\ \frac{\lambda_1}{\lambda_1+\lambda_2}\right)$$
> **This is the exact converse of Poisson thinning (Example 2b).** Thinning splits a Poisson total into independent Poissons; conditioning on the total puts the binomial back. **The two facts are the same fact read in opposite directions**, and together they are the reason Poisson counts are so pleasant to work with.

> [!example] Example 4d — all orderings are equally likely
> In $n$ independent trials with success probability $p$, **given that there were $k$ successes, each of the $\binom nk$ arrangements of successes and failures has probability $1/\binom nk$**:
> $$P(o\mid X=k)=\frac{p^k(1-p)^{n-k}}{\binom nk p^k(1-p)^{n-k}}=\frac1{\binom nk}$$
> **The value of $p$ cancels entirely.** Conditional on the count, the *pattern* carries no information about $p$ — $X$ is a **sufficient statistic**, which is precisely the concept formalised in [[Mathematical Statistics/contents/05 - Point Estimation|Mathematical Statistics ch. 05]].

---

### 5. Conditional distributions: the continuous case

$$f_{X\mid Y}(x\mid y)=\frac{f(x,y)}{f_Y(y)}\qquad\text{whenever } f_Y(y)>0$$

$$P\{X\in A\mid Y=y\}=\int_A f_{X\mid Y}(x\mid y)\,dx$$

> [!important] Conditioning on a probability-zero event — and why it is legitimate
> $P\{Y=y\}=0$, so $P(E\mid Y=y)$ is *undefined* by the ch. 03 formula. The definition above rescues it as a **limit**:
> $$f_{X\mid Y}(x\mid y)\,dx \approx P\{x\le X\le x+dx \mid y\le Y\le y+dy\}$$
> — condition on a thin *strip*, then let its width go to zero. **The ratio of two vanishing quantities is perfectly well defined even though each is zero**, exactly as a derivative is.
>
> **Geometrically: $f_{X\mid Y}(\cdot\mid y)$ is the slice of the joint density at height $y$, renormalised to integrate to 1.** The slice is the shape; the division by $f_Y(y)$ is the rescaling.

Two structural remarks:

- **The conditional density is where "$X$ given $Y$" acquires meaning at all in continuous problems.** Every regression, every posterior, every filter is a conditional density.
- **Mixed cases work the same way.** If $X$ is continuous and $N$ discrete, $f_{X\mid N}(x\mid n)=\dfrac{P\{N=n\mid X=x\}}{P\{N=n\}}f(x)$ — **which is Bayes' theorem with a density in place of one of the probabilities.**

#### 5a. The $t$-distribution

If $Z\sim N(0,1)$ and $Y\sim\chi^2_n$ are independent, then $T=\dfrac{Z}{\sqrt{Y/n}}$ has the **$t$-distribution with $n$ degrees of freedom**:

$$f_T(t)=\frac{\Gamma\!\left(\frac{n+1}2\right)}{\sqrt{\pi n}\,\Gamma\!\left(\frac n2\right)}\left(1+\frac{t^2}{n}\right)^{-(n+1)/2},\qquad -\infty<t<\infty$$

**The derivation is a template worth learning:** condition on $Y=y$ (making $T$ normal with variance $n/y$), multiply by $f_Y(y)$ to get the *joint* density of $(T,Y)$, then integrate $y$ out.

> [!tip] Why $t$ has fat tails
> $T$ is a normal divided by an independent random scale. **Occasionally that scale comes out small, and dividing by a small number produces a large $T$** — an extra source of variability the normal does not have. That is the entire reason $t$ tables have larger critical values than $z$ tables, and why the two agree as $n\to\infty$ (the denominator concentrates at 1). See [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics ch. 07]].

#### 5b. The bivariate normal — the most important joint distribution there is

$$f(x,y)=\frac1{2\pi\sigma_x\sigma_y\sqrt{1-\rho^2}}\exp\left\{-\frac1{2(1-\rho^2)}\left[\left(\frac{x-\mu_x}{\sigma_x}\right)^2+\left(\frac{y-\mu_y}{\sigma_y}\right)^2-2\rho\frac{(x-\mu_x)(y-\mu_y)}{\sigma_x\sigma_y}\right]\right\}$$

for $\sigma_x,\sigma_y>0$ and $-1<\rho<1$. Completing the square in $x$ gives the three facts that matter:

> [!important] The three consequences
> 1. **Marginals are normal:** $X\sim N(\mu_x,\sigma_x^2)$, $Y\sim N(\mu_y,\sigma_y^2)$.
> 2. **Conditionals are normal:**
> $$Y\mid \{X=x\}\ \sim\ N\!\left(\underbrace{\mu_y+\rho\frac{\sigma_y}{\sigma_x}(x-\mu_x)}_{\text{linear in }x},\ \underbrace{\sigma_y^2(1-\rho^2)}_{\text{free of }x}\right)$$
> 3. **$X\perp Y \iff \rho=0$.**

**Read (2) slowly — it is the population version of simple linear regression.**

- The conditional **mean is linear in $x$** with slope $\rho\sigma_y/\sigma_x$: this is the regression coefficient $\beta_1$.
- The conditional **variance does not depend on $x$**: this is **homoskedasticity**, assumed rather than derived in [[Econometrics/contents/00-Index|Econometrics]].
- $\sigma_y^2(1-\rho^2)$ is the **residual variance**, so $\rho^2$ is the fraction of variance explained — **this is where $R^2$ comes from.**

> [!warning] Fact (3) is special to the bivariate normal, and is routinely over-generalised
> **In general, uncorrelated $\ne$ independent.** ($\rho=0$ only says the *linear* relationship is absent — see [[07 - Properties of Expectation|ch. 07]] for the standard counterexample $Y=X^2$.) **The equivalence holds here because the joint density factors exactly when $\rho=0$**, and that is a property of this density, not of correlation.
>
> **A second, subtler trap: normal marginals do not make a joint distribution bivariate normal.** There exist joint densities with perfectly normal margins that are not bivariate normal at all — so **checking each variable for normality does not verify the model.**

#### 5c. Conditioning inside a set, and conjugacy

For $X$ restricted to a set $A$:
$$f_{X\mid X\in A}(x)=\frac{f(x)}{P(X\in A)}=\frac{f(x)}{\int_A f(y)\,dy},\qquad x\in A$$

> [!example] Example 5f — the Pareto is memoryless in a multiplicative sense
> If $X$ is Pareto$(a,\lambda)$ with $F(x)=1-a^\lambda x^{-\lambda}$, then **given $X>x_0$, $X$ is Pareto$(x_0,\lambda)$** — the *same shape*, rescaled. **This is the heavy-tailed analogue of the exponential's memorylessness** ([[05 - Continuous Random Variables|ch. 05]]) and the reason Pareto models "the rich get richer": conditioning on already being large tells you nothing about *how much* larger.

> [!example] Example 5e — the beta prior, and the birth of Bayesian statistics
> A coin has unknown success probability $X\sim U(0,1)$. Observing $n$ successes in $n+m$ trials,
> $$f_{X\mid N}(x\mid n)\ \propto\ x^n(1-x)^m\qquad\Longrightarrow\qquad X\mid N=n \ \sim\ \text{Beta}(n+1,\ m+1)$$
> Since $U(0,1)=\text{Beta}(1,1)$: **prior Beta$(1,1)$ + data $(n$ successes, $m$ failures$)$ $\to$ posterior Beta$(1+n,\,1+m)$.**
>
> **The beta parameters are literally a running tally of successes and failures.** That is what makes the beta family **conjugate** to the binomial, and it is the cleanest possible illustration of what "updating a belief with data" means — the mechanism behind Bayesian A/B testing and Thompson sampling in [[Machine Learning/contents/00-Index|Machine Learning]].

---

### 6. Order statistics

Let $X_1,\dots,X_n$ be i.i.d. continuous with density $f$ and cdf $F$. Sorting them gives the **order statistics** $X_{(1)}\le X_{(2)}\le\dots\le X_{(n)}$, with $X_{(1)}$ the minimum and $X_{(n)}$ the maximum.

$$f_{X_{(1)},\dots,X_{(n)}}(x_1,\dots,x_n)=n!\,f(x_1)\cdots f(x_n),\qquad x_1<x_2<\dots<x_n$$

**The $n!$ is the whole content:** any one of the $n!$ orderings of the original sample produces the same sorted vector, so the density is $n!$ times larger on the sorted region (and zero elsewhere).

The marginal density of the $j$th smallest:

$$\boxed{\,f_{X_{(j)}}(x)=\frac{n!}{(j-1)!\,(n-j)!}\,[F(x)]^{j-1}\,[1-F(x)]^{n-j}\,f(x)\,}$$

> [!tip] Read the formula, don't memorise it
> For $X_{(j)}$ to sit at $x$: **$j-1$ observations below** ($[F(x)]^{j-1}$), **$n-j$ above** ($[1-F(x)]^{n-j}$), **one exactly at $x$** ($f(x)$), and $\dfrac{n!}{(j-1)!\,1!\,(n-j)!}$ ways to choose who is who. **It is a multinomial with three categories.**

The cdf has an equally direct reading:

$$F_{X_{(j)}}(y)=P\{\text{at least } j \text{ of the } X_i \text{ are} \le y\}=\sum_{k=j}^{n}\binom nk [F(y)]^k[1-F(y)]^{n-k}$$

**Equating the two gives a genuine analytic identity** (Ross's 6.5) linking a binomial sum to an incomplete beta integral.

> [!important] For uniforms, order statistics are beta
> If $X_i\sim U(0,1)$ then $F(x)=x$ and
> $$X_{(j)}\sim\text{Beta}(j,\ n-j+1),\qquad \mathbb{E}[X_{(j)}]=\frac{j}{n+1}$$
> **$n$ uniform points cut $[0,1]$ into $n+1$ gaps of equal expected length $\tfrac1{n+1}$** — the cleanest way to remember it.

**Joint density of two order statistics** ($i<j$, $x_i<x_j$) — same multinomial logic with five groups:

$$f_{X_{(i)},X_{(j)}}(x_i,x_j)=\frac{n!}{(i-1)!\,(j-i-1)!\,(n-j)!}F^{i-1}(x_i)f(x_i)[F(x_j)-F(x_i)]^{j-i-1}f(x_j)[1-F(x_j)]^{n-j}$$

> [!example] Example 6c — the range
> $R=X_{(n)}-X_{(1)}$. In general $P\{R\le a\}=n\int_{-\infty}^{\infty}[F(x+a)-F(x)]^{n-1}f(x)\,dx$; **for $U(0,1)$ this evaluates in closed form:**
> $$f_R(a)=n(n-1)a^{n-2}(1-a),\qquad 0\le a\le1$$
> i.e. **$R\sim\text{Beta}(n-1,2)$, with $\mathbb{E}[R]=\dfrac{n-1}{n+1}$** — the sample range of uniforms creeps up on the true range 1 but never reaches it. **This under-estimation is the standard illustration that the sample range is a biased estimator of the population range** ([[Mathematical Statistics/contents/05 - Point Estimation|Mathematical Statistics ch. 05]]).

> [!example] Example 6a — spacing on a road
> Three people uniformly and independently placed on a road of length 1: $P\{\text{no two within } d\}=(1-2d)^3$ for $d\le\tfrac12$, and in general **$[1-(n-1)d]^n$ for $n$ people, $d\le\tfrac1{n-1}$.**
>
> **The subtraction of $(n-1)d$ is a "remove the mandatory gaps, then place freely" argument** — the same device as stars-and-bars with minimum occupancy from [[01 - Combinatorial Analysis|ch. 01]].

---

### 7. Joint distributions of functions — the Jacobian

Given $Y_1=g_1(X_1,X_2)$, $Y_2=g_2(X_1,X_2)$, suppose the system can be solved uniquely for $x_1,x_2$ and that the **Jacobian determinant**

$$J(x_1,x_2)=\begin{vmatrix}\dfrac{\partial g_1}{\partial x_1} & \dfrac{\partial g_1}{\partial x_2}\\[2mm] \dfrac{\partial g_2}{\partial x_1} & \dfrac{\partial g_2}{\partial x_2}\end{vmatrix}\ne0$$

everywhere. Then

$$\boxed{\,f_{Y_1,Y_2}(y_1,y_2)=f_{X_1,X_2}(x_1,x_2)\,|J(x_1,x_2)|^{-1}\,}$$

**This is [[05 - Continuous Random Variables|ch. 05 §7]] in $n$ dimensions**: $|J|$ measures how much the map stretches area, and density must shrink by exactly that factor to keep total probability at 1. The $n$-variable version is identical with an $n\times n$ determinant.

> [!example] Example 7a — sum and difference of standard normals
> $Y_1=X_1+X_2$, $Y_2=X_1-X_2$ gives $J=-2$ and $f_{Y_1,Y_2}(y_1,y_2)=\tfrac12 f_{X_1,X_2}\!\left(\tfrac{y_1+y_2}2,\tfrac{y_1-y_2}2\right)$. For independent standard normals this collapses to
> $$\frac1{\sqrt{4\pi}}e^{-y_1^2/4}\cdot\frac1{\sqrt{4\pi}}e^{-y_2^2/4}$$
> **$X_1+X_2$ and $X_1-X_2$ are independent $N(0,2)$** — even though both are built from the same two variables.
>
> **And this characterises the normal:** for i.i.d. $X_1,X_2$ with common cdf $F$, **$X_1+X_2\perp X_1-X_2$ if and only if $F$ is normal.** Independence of sum and difference is not a generic fact; it is a normal-only fact.

> [!example] Example 7b — polar coordinates, and how to simulate a normal
> $X,Y$ i.i.d. $N(0,1)$; let $(R,\Theta)$ be their polar coordinates. Then $J=1/r$, and
> $$f(r,\theta)=\frac1{2\pi}\,re^{-r^2/2},\qquad 0<r<\infty,\ 0<\theta<2\pi$$
> **This factors**, so $\Theta\sim U(0,2\pi)$ is independent of $R$, which has the **Rayleigh** density $re^{-r^2/2}$. Moreover $R^2\sim\text{Exp}(\tfrac12)=\chi^2_2$ — **confirming that the exponential with rate $\tfrac12$ *is* the chi-squared with 2 degrees of freedom.**
>
> Since $-2\log U\sim\text{Exp}(\tfrac12)$, this yields the **Box–Muller transform**: from independent $U_1,U_2\sim U(0,1)$,
> $$X_1=\sqrt{-2\log U_1}\,\cos(2\pi U_2),\qquad X_2=\sqrt{-2\log U_1}\,\sin(2\pi U_2)$$
> are independent standard normals. **This is how normal random numbers were generated for decades** — see [[10 - Simulation|ch. 10]].

> [!example] Example 7c — gamma, beta, and a striking independence
> $X\sim\Gamma(\alpha,\lambda)\perp Y\sim\Gamma(\beta,\lambda)$. With $U=X+Y$ and $V=\dfrac{X}{X+Y}$:
> $$U\sim\Gamma(\alpha+\beta,\lambda)\ \perp\ V\sim\text{Beta}(\alpha,\beta)$$
> **The total and the proportion are independent.** If two workers handle $n$ and $m$ exponential jobs, **the share of the work done by worker I is independent of how long the whole job took.**
>
> The same calculation delivers $B(\alpha,\beta)=\dfrac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$ **for free** — a nontrivial analytic identity obtained by a probability argument.

> [!example] Example 7e — Poisson arrival times are uniform order statistics
> $X_i$ i.i.d. $\text{Exp}(\lambda)$, $Y_i=X_1+\dots+X_i$ (the arrival times). Then $J=1$ and
> $$f_{Y_1,\dots,Y_n}(y_1,\dots,y_n)=\lambda^n e^{-\lambda y_n},\qquad 0<y_1<\dots<y_n$$
> Integrating out recovers $Y_n\sim\Gamma(n,\lambda)$, and — the striking part —
> $$f_{Y_1,\dots,Y_{n-1}\mid Y_n}(y_1,\dots,y_{n-1}\mid t)=\frac{(n-1)!}{t^{n-1}}$$
> **Given that the $n$th arrival happened at time $t$, the first $n-1$ arrivals are distributed exactly as the order statistics of $n-1$ independent $U(0,t)$ points.** $\lambda$ has vanished. **This is the defining property of the Poisson process** ([[09 - Additional Topics in Probability|ch. 09]]): conditional on the count, arrivals are "completely at random" in time.

---

### 8. Exchangeable random variables

$X_1,\dots,X_n$ are **exchangeable** if their joint distribution is invariant under every permutation of the indices:

$$P\{X_{i_1}\le x_1,\dots,X_{i_n}\le x_n\}=P\{X_1\le x_1,\dots,X_n\le x_n\}$$

equivalently, in the discrete case, $p(x_1,\dots,x_n)$ is a **symmetric function**.

> [!important] i.i.d. $\Rightarrow$ exchangeable, but **not** conversely
> Exchangeability says the *labels* carry no information — **order does not matter**. It does **not** say the variables are unrelated. **This is the honest weakening of i.i.d.**, and often the assumption you can actually defend.

Consequences and examples:

- **Every $X_i$ has the same marginal distribution.** (Immediate: sum the symmetric joint pmf over the others.)
- **Example 8a — sampling without replacement.** Draw all $n$ balls from an urn with $k$ special ones; $X_i=1$ if the $i$th is special. Then $p(x_1,\dots,x_n)=\dfrac{k!(n-k)!}{n!}$ for every arrangement — symmetric, hence exchangeable. **But manifestly not independent** (the last ball is determined by the first $n-1$). **Corollary: $P\{X_i=1\}=k/n$ for every $i$ — the third card is exactly as likely to be an ace as the first.**
- **Example 8c — Pólya's urn.** Draw a ball, replace it *plus another of the same colour*. Then $X_1,\dots,X_k$ are exchangeable — and **positively** dependent (each red draw makes the next more likely). **Yet $P\{X_i=1\}=\dfrac{n}{n+m}$ for all $i$**, the same as the first draw.
- **Example 8d.** The gaps between the order statistics of $n$ i.i.d. uniforms are exchangeable — **all $n$ spacings have the same distribution, including the two end pieces.**

> [!tip] Why exchangeability earns its own section
> **Pólya's urn is the model of "success breeds success"** — reinforcement, preferential attachment, contagion — and it is the standard example showing that **positive dependence is compatible with identical marginals.** In statistics, **de Finetti's theorem** says an infinite exchangeable sequence is a *mixture* of i.i.d. sequences: exchangeable data behaves like i.i.d. data with a random parameter. **That is precisely the Bayesian setup of Example 5e**, and the deepest reason priors are not arbitrary.

---

## ✏️ Exercises

> [!question] Exercise 1 — a joint pmf from coin tosses *(warm-up)*
> A fair coin is tossed three times. Let $X$ be the number of heads in the **first two** tosses and $Y$ the number of heads in **all three**.
>
> (i) Find the joint pmf $p(x,y)$.
> (ii) Find both marginals. Identify $p_Y$ by name.
> (iii) Are $X$ and $Y$ independent?
> (iv) Find $p_{X\mid Y}(x\mid 2)$ and $\mathbb{E}[X\mid Y=2]$.

> [!example]- Solution
> **(i)** $Y=X+(\text{third toss})$, and the third toss is independent of the first two. So $p(x,y)=P\{X=x\}\cdot\tfrac12$ for $y\in\{x,x+1\}$, and 0 otherwise. With $X\sim\text{Bin}(2,\tfrac12)$:
>
> | $x\backslash y$ | 0 | 1 | 2 | 3 | **$p_X$** |
> |---|---|---|---|---|---|
> | **0** | $\tfrac18$ | $\tfrac18$ | 0 | 0 | $\tfrac14$ |
> | **1** | 0 | $\tfrac14$ | $\tfrac14$ | 0 | $\tfrac12$ |
> | **2** | 0 | 0 | $\tfrac18$ | $\tfrac18$ | $\tfrac14$ |
> | **$p_Y$** | $\tfrac18$ | $\tfrac38$ | $\tfrac38$ | $\tfrac18$ | 1 |
>
> **(ii)** $X\sim\text{Bin}(2,\tfrac12)$ and $Y\sim\text{Bin}(3,\tfrac12)$ — as they must be.
>
> **(iii) No.** $p(0,3)=0$ but $p_X(0)p_Y(3)=\tfrac14\cdot\tfrac18=\tfrac1{32}\ne0$. **A single zero cell with non-zero margins settles it** — you never need to check the whole table. (Intuitively: $X\le Y\le X+1$, so they are nearly deterministic in each other.)
>
> **(iv)** $p_{X\mid Y}(1\mid2)=\dfrac{1/4}{3/8}=\dfrac23$, $p_{X\mid Y}(2\mid2)=\dfrac{1/8}{3/8}=\dfrac13$, so
> $$\mathbb{E}[X\mid Y=2]=1\cdot\tfrac23+2\cdot\tfrac13=\tfrac43$$
> **Sanity check via §4 (Example 4d):** given 2 heads in 3 tosses, the two head-positions are a uniformly random 2-subset of $\{1,2,3\}$, so $X$ is hypergeometric with mean $2\cdot\tfrac23=\tfrac43$ ✓. **Note $\tfrac43>\mathbb{E}[X]=1$** — learning $Y=2$ is good news about $X$, as it should be.

> [!question] Exercise 2 — a density on a non-rectangular region
> $$f(x,y)=c\,e^{-x-2y},\qquad 0<y<x<\infty$$
>
> (i) Find $c$.
> (ii) Find both marginal densities and identify $f_Y$ by name.
> (iii) Are $X$ and $Y$ independent? Answer **before** doing any algebra.
> (iv) Find $f_{X\mid Y}(x\mid y)$ and interpret it.
> (v) Find $P\{X>1\}$ and $\mathbb{E}[X]$.

> [!example]- Solution
> **(iii) first — no.** The support $\{0<y<x\}$ is a **wedge, not a rectangle**: knowing $X=0.1$ forces $Y<0.1$. **By the §2a test the variables are dependent, and no algebra is needed.** (The exponential factors $e^{-x}$ and $e^{-2y}$ are a decoy.)
>
> **(i)**
> $$\int_0^{\infty}\!\!\int_0^{x} c\,e^{-x-2y}\,dy\,dx=c\int_0^\infty e^{-x}\frac{1-e^{-2x}}2dx=\frac c2\left(1-\frac13\right)=\frac c3 \Longrightarrow \boxed{c=3}$$
>
> **(ii)** $\displaystyle f_X(x)=\int_0^x 3e^{-x-2y}dy=\tfrac32 e^{-x}\left(1-e^{-2x}\right)$, $x>0$.
> $\displaystyle f_Y(y)=\int_y^\infty 3e^{-x-2y}dx=3e^{-3y}$, $y>0$ — **$Y\sim\text{Exp}(3)$.**
>
> **(iv)** $f_{X\mid Y}(x\mid y)=\dfrac{3e^{-x-2y}}{3e^{-3y}}=e^{-(x-y)}$ for $x>y$.
> **Given $Y=y$, the excess $X-y$ is $\text{Exp}(1)$ — and the answer does not depend on $y$.** So
> $$X = Y + W,\qquad Y\sim\text{Exp}(3),\ W\sim\text{Exp}(1),\ Y\perp W$$
> **The dependence is entirely a shift.** This is the cleanest way to understand the whole density, and it makes (v) immediate.
>
> **(v)** $\mathbb{E}[X]=\mathbb{E}[Y]+\mathbb{E}[W]=\tfrac13+1=\boxed{\tfrac43}$, and
> $$P\{X>1\}=\int_1^\infty\tfrac32 e^{-x}(1-e^{-2x})dx=\tfrac32e^{-1}-\tfrac12e^{-3}=.5519-.0249=\boxed{.5269}$$
> *(Both confirmed by numerical integration.)*

> [!question] Exercise 3 — sums of independent random variables
> (i) $X\sim\text{Poisson}(3)$ and $Y\sim\text{Poisson}(5)$ are independent. Find $P\{X+Y=4\}$.
> (ii) For the same $X,Y$, find the conditional distribution of $X$ given $X+Y=4$, and $\mathbb{E}[X\mid X+Y=4]$.
> (iii) Adult male heights are $N(70,3^2)$ inches and adult female heights $N(65,2.5^2)$, independent. A man and a woman are chosen at random. **Find the probability that the woman is taller.**
> (iv) In (iii), a student writes $\mathrm{SD}(Y-X)=3-2.5=0.5$ and concludes the probability is $P\{Z>10\}\approx0$. **Diagnose the error.**

> [!example]- Solution
> **(i)** $X+Y\sim\text{Poisson}(8)$ by §3e, so
> $$P\{X+Y=4\}=e^{-8}\frac{8^4}{4!}=e^{-8}\cdot\frac{4096}{24}=\boxed{.0573}$$
>
> **(ii)** By Example 4b, $X\mid\{X+Y=4\}\sim\text{Bin}\!\left(4,\tfrac{3}{3+5}\right)=\text{Bin}(4,\tfrac38)$, so
> $$\mathbb{E}[X\mid X+Y=4]=4\cdot\tfrac38=\boxed{1.5}$$
> **The rate $\lambda_1+\lambda_2=8$ has disappeared** — only the *ratio* $3:5$ survives conditioning. Note $\mathbb{E}[X]=3$ unconditionally, so learning that the total was only 4 revises $X$ sharply downward.
>
> **(iii)** Let $D=Y-X$. Variances **add**:
> $$D\sim N(65-70,\ 2.5^2+3^2)=N(-5,\ 15.25),\qquad \mathrm{SD}=3.905$$
> $$P\{D>0\}=P\left\{Z>\frac{0-(-5)}{3.905}\right\}=P\{Z>1.2804\}=\boxed{.1002}$$
> **About 1 in 10 randomly paired couples has the woman taller** — a much larger number than most people guess, because a 5-inch mean gap is only 1.28 standard deviations of the *difference*.
>
> **(iv) Standard deviations never add or subtract — variances do**, and for a **difference** they still **add**:
> $$\mathrm{Var}(Y-X)=\sigma_Y^2+\sigma_X^2=15.25\quad\text{not}\quad(\sigma_Y-\sigma_X)^2=0.25$$
> The student's method understates the SD by a factor of nearly 8 and turns a 10% event into an impossibility.
>
> > [!warning] The intuition to keep
> > **Combining two independent noisy quantities *always* increases variance, whichever sign they enter with.** The only way a difference gets *less* variable is if the two are **positively correlated** — and independence rules that out. This error, in the form $\mathrm{SD}(\bar X-\bar Y)$, is the single most common mistake in two-sample testing ([[Mathematical Statistics/contents/08 - Inferences on Two Samples|Mathematical Statistics ch. 08]]).

> [!question] Exercise 4 — order statistics
> Let $X_1,\dots,X_5$ be i.i.d. $U(0,1)$.
>
> (i) Write down the density of $X_{(2)}$ and identify it as a named distribution.
> (ii) Find $P\{X_{(2)}<\tfrac12\}$ **two ways** — by integration and by a binomial argument.
> (iii) Find $\mathbb{E}[X_{(2)}]$.
> (iv) Write down the density of the range $R=X_{(5)}-X_{(1)}$ and find $P\{R>0.8\}$.
> (v) Three points are dropped independently and uniformly on a road of length 1. What is the probability that no two are within $0.2$ of each other?

> [!example]- Solution
> **(i)** With $n=5$, $j=2$, $F(x)=x$, $f(x)=1$:
> $$f_{X_{(2)}}(x)=\frac{5!}{1!\,3!}x(1-x)^3=20x(1-x)^3,\qquad 0<x<1$$
> — **$X_{(2)}\sim\text{Beta}(2,4)$.**
>
> **(ii)** *By integration:* $\int_0^{1/2}20x(1-x)^3dx=.8125$.
> *By the binomial argument:* $X_{(2)}<\tfrac12$ iff **at least 2** of the 5 points fall below $\tfrac12$, and the count is $\text{Bin}(5,\tfrac12)$:
> $$\frac{\binom52+\binom53+\binom54+\binom55}{2^5}=\frac{10+10+5+1}{32}=\frac{26}{32}=\boxed{\tfrac{13}{16}=.8125}\ ✓$$
> **The second route is faster and needs no calculus** — for uniforms, always ask "how many fell below?"
>
> **(iii)** $\mathbb{E}[X_{(j)}]=\dfrac{j}{n+1}=\dfrac26=\boxed{\tfrac13}$. **The five points cut $[0,1]$ into six gaps of expected length $\tfrac16$**, and $X_{(2)}$ sits after two of them.
>
> **(iv)** $f_R(a)=n(n-1)a^{n-2}(1-a)=20a^3(1-a)$ on $[0,1]$, i.e. $R\sim\text{Beta}(4,2)$. Then
> $$P\{R>0.8\}=\int_{0.8}^{1}20a^3(1-a)\,da=20\left[\tfrac{a^4}4-\tfrac{a^5}5\right]_{0.8}^{1}=20(.05-.036864)=\boxed{.2627}$$
> Also $\mathbb{E}[R]=\tfrac{n-1}{n+1}=\tfrac46=\tfrac23$: **five points typically span only two-thirds of the interval.** *(A useful corrective — the sample range systematically understates the population range, and it does so badly for small $n$.)*
>
> **(v)** By Example 6a with $n=3$, $d=0.2\le\tfrac12$:
> $$[1-(n-1)d]^n=(1-2(.2))^3=(0.6)^3=\boxed{.216}$$
> **Fewer than a quarter of the time** — points "clump" far more than intuition suggests, which is the same phenomenon as the birthday problem.

> [!question] Exercise 5 — the Jacobian, and the bivariate normal *(hard)*
> **(a)** Let $X$ and $Y$ be independent $\text{Exp}(\lambda)$. Using the change-of-variables formula, find the joint density of
> $$U=X+Y,\qquad V=\frac{X}{X+Y}$$
> and deduce the marginal distribution of each. Are they independent?
>
> **(b)** Let $(X,Y)$ be bivariate normal, where $X$ is a student's score on a midterm with $\mu_x=70$, $\sigma_x=3$, and $Y$ is their final-exam score with $\mu_y=170$, $\sigma_y=20$, and $\rho=0.6$.
> (i) Find the conditional distribution of $Y$ given $X=74$.
> (ii) Find $P\{Y>190\mid X=74\}$.
> (iii) What fraction of the variance in $Y$ is explained by $X$? What is the residual standard deviation?

> [!example]- Solution
> **(a)** The joint density is $f_{X,Y}(x,y)=\lambda^2e^{-\lambda(x+y)}$ on $x,y>0$. With $g_1=x+y$, $g_2=\dfrac{x}{x+y}$:
> $$J=\begin{vmatrix}1 & 1\\[1mm] \dfrac{y}{(x+y)^2} & \dfrac{-x}{(x+y)^2}\end{vmatrix}=\frac{-x-y}{(x+y)^2}=\frac{-1}{x+y}=-\frac1u$$
> Inverting: $x=uv$, $y=u(1-v)$, with $u>0$ and $0<v<1$. Hence $|J|^{-1}=u$ and
> $$f_{U,V}(u,v)=\lambda^2e^{-\lambda u}\cdot u=\underbrace{\left[\lambda^2ue^{-\lambda u}\right]}_{\Gamma(2,\lambda)}\cdot\underbrace{\left[1\right]}_{U(0,1)},\qquad u>0,\ 0<v<1$$
> **The density factors *and* the region is a rectangle $(0,\infty)\times(0,1)$**, so:
> $$U=X+Y\sim\Gamma(2,\lambda),\qquad V=\frac{X}{X+Y}\sim U(0,1),\qquad U\perp V$$
> *(This is Example 7c with $\alpha=\beta=1$, since $\text{Beta}(1,1)=U(0,1)$.)*
>
> **The interpretation is worth more than the algebra.** For two exponential jobs: **the total time and the fraction contributed by the first job are independent, and that fraction is uniform.** Knowing the job took 10 hours tells you *nothing* about the split — and any split is equally likely.
>
> **(b)(i)** By §5b:
> $$\mathbb{E}[Y\mid X=74]=\mu_y+\rho\frac{\sigma_y}{\sigma_x}(x-\mu_x)=170+0.6\cdot\frac{20}{3}\cdot(74-70)=170+16=\boxed{186}$$
> $$\mathrm{Var}(Y\mid X=74)=\sigma_y^2(1-\rho^2)=400(1-0.36)=256\quad\Longrightarrow\quad \mathrm{SD}=16$$
> so $Y\mid X=74\ \sim\ N(186,\,16^2)$.
>
> **(ii)** $P\{Y>190\mid X=74\}=P\left\{Z>\dfrac{190-186}{16}=0.25\right\}=\boxed{.4013}$
>
> **(iii)** $\rho^2=0.36$ — **36% of the variance in final scores is explained by the midterm**, and the residual SD is $\sigma_y\sqrt{1-\rho^2}=20\times0.8=16$.
>
> > [!tip] What this exercise actually is
> > **(b) is linear regression, written out before anyone calls it that.** The slope $\rho\sigma_y/\sigma_x=4$ says *one extra midterm point predicts four extra final points*; $\rho^2=R^2$; and the constant conditional variance is the homoskedasticity assumption. **Everything in [[Econometrics/contents/00-Index|Econometrics]] ch. 2 is this formula with sample estimates substituted for $\mu,\sigma,\rho$.**
> >
> > **Two warnings that follow from the same formula.** First, **regression to the mean**: the student scored $+1.33\sigma_x$ on the midterm but is predicted at $+0.8\sigma_y$ on the final — **$\rho<1$ always pulls the prediction toward the mean**, and mistaking this for a real effect ("the top scorers slacked off") is a classic fallacy. Second, **$\rho=0.6$ sounds strong but explains only 36%** — correlations must be squared before they can be read as explanatory power.

---

## 📝 Summary

- **A joint distribution is not determined by its marginals.** Row and column sums leave the dependence structure completely unspecified — which is why joint distributions are studied in their own right. **Marginals are obtained by summing/integrating the other variable out, never by setting it to zero.**
- **Independence means factorisation — of the density *and* of the support.** $f(x,y)=h(x)g(y)$ **for all $x,y$**. **If the region where $f>0$ is not a rectangle, the variables are dependent**, no matter how the formula looks. Independence is symmetric, so **when one direction is unintuitive, check the other** (Example 2j).
- **Sums of independent variables convolve:** $f_{X+Y}(a)=\int f_X(a-y)f_Y(y)\,dy$. **Four families are closed under it** — normal (means and variances add), Poisson (rates add), gamma at fixed rate (shapes add), binomial at fixed $p$ (trials add). **Everything else needs the integral or an approximation.**
- **Variances add; standard deviations do not — and for a difference the variances still add.** $\mathrm{Var}(X\pm Y)=\sigma_X^2+\sigma_Y^2$ for independent $X,Y$.
- **Poisson thinning and its converse are the same fact:** splitting a Poisson total by an independent coin gives *independent* Poissons; conditioning a sum of Poissons on its total gives a *binomial*. **The Poisson variability in the total is exactly what decouples the parts.**
- **Conditional distributions are ch. 03 with a value instead of an event:** $f_{X\mid Y}(x\mid y)=f(x,y)/f_Y(y)$, defined as a limit of thin strips so that conditioning on the probability-zero event $\{Y=y\}$ is legitimate. **Geometrically: a slice of the joint density, renormalised.**
- **For the bivariate normal, $Y\mid X=x$ is normal with mean $\mu_y+\rho\frac{\sigma_y}{\sigma_x}(x-\mu_x)$ and variance $\sigma_y^2(1-\rho^2)$.** **The mean is linear in $x$ and the variance is free of $x$ — this is linear regression, homoskedasticity, and $R^2=\rho^2$, all in one line.** For *this* distribution only, $\rho=0\iff$ independence.
- **Order statistics:** $f_{X_{(j)}}(x)=\frac{n!}{(j-1)!(n-j)!}F^{j-1}(1-F)^{n-j}f$ — a three-category multinomial. **For uniforms, $X_{(j)}\sim\text{Beta}(j,n-j+1)$ with mean $j/(n+1)$**, and the range is $\text{Beta}(n-1,2)$ with mean $\frac{n-1}{n+1}$ — **the sample range always understates the true range.**
- **The Jacobian formula $f_{Y}(y)=f_X(x)|J|^{-1}$ is the multivariate change of variables.** It delivers: sum and difference of normals are independent (a normal-only property), polar coordinates $\Rightarrow$ **Box–Muller**, and $X+Y\perp X/(X+Y)$ for gammas (total independent of proportion).
- **Conditional on the $n$th Poisson arrival at time $t$, the earlier arrivals are uniform order statistics on $(0,t)$** — $\lambda$ disappears. This is *the* characterisation of the Poisson process.
- **Exchangeable $\ne$ independent.** Exchangeability says the labels carry no information; sampling without replacement and Pólya's urn are exchangeable and strongly dependent. **It is the assumption you can usually defend when i.i.d. is too strong.**

---

## ⚠️ Important Notes

> [!warning] Independence: check the region before you check the formula
> $$f(x,y)=24xy \text{ on } \{x,y>0,\ x+y<1\}$$
> **looks** factored and **is not independent**. Written honestly, $f(x,y)=24xy\cdot\mathbb{1}\{\dots\}$, and the indicator couples $x$ to $y$.
>
> **Procedure, in this order:**
> 1. **Is the support a rectangle (possibly infinite)?** If no → **dependent, stop.**
> 2. If yes, does the formula factor into $h(x)g(y)$? If yes → independent.
>
> **Every triangle, wedge, disc, or $\{y<x\}$ region gives dependence automatically.**

> [!warning] $\mathrm{SD}(X\pm Y)\ne \sigma_X\pm\sigma_Y$
> $$\mathrm{Var}(X+Y)=\mathrm{Var}(X-Y)=\sigma_X^2+\sigma_Y^2 \qquad \text{(independent }X,Y\text{)}$$
> **Differencing does not cancel noise — it compounds it.** In Exercise 3, treating $\mathrm{SD}$ as subtractive turned a 10% probability into 0.
>
> **The general formula, needed as soon as independence fails** ([[07 - Properties of Expectation|ch. 07]]):
> $$\mathrm{Var}(X\pm Y)=\sigma_X^2+\sigma_Y^2\pm2\,\mathrm{Cov}(X,Y)$$
> **Only positive correlation can make a difference less variable.**

> [!warning] The binomial is closed under addition only at a common $p$
> | Sum | Closed? | Condition |
> |---|---|---|
> | Poisson + Poisson | ✅ | none |
> | Normal + Normal | ✅ | none (independent) |
> | Gamma + Gamma | ✅ | **same rate $\lambda$** |
> | Binomial + Binomial | ✅ | **same $p$** |
>
> **Example 3c is precisely the failure case** ($p=.4$ and $p=.7$) — which is why it must be done by normal approximation rather than exactly. **Check the shared-parameter condition before invoking closure.**

> [!warning] $\rho=0$ implies independence *only* for the bivariate normal
> **In general, uncorrelated $\ne$ independent** — $\rho$ measures the *linear* part of the relationship and nothing else. The bivariate normal is a special case where the joint density happens to factor exactly when $\rho=0$.
>
> **And the converse trap: normal marginals do not imply bivariate normality.** There are joint distributions with perfectly normal margins that are not bivariate normal. **Checking each variable's histogram does not validate the model** — you need the *joint* behaviour, e.g. that all linear combinations $aX+bY$ are normal.

> [!warning] Regression to the mean is a property of $\rho<1$, not a phenomenon
> $$\mathbb{E}[Y\mid X=x]-\mu_y=\rho\,\frac{\sigma_y}{\sigma_x}(x-\mu_x)$$
> **In standardised units the prediction is $\rho$ times the input** — so a student $1.33\sigma$ above average on the midterm is predicted only $0.8\sigma$ above on the final.
>
> **Extreme performances are followed by less extreme ones for purely statistical reasons.** Attributing this to complacency, a coaching change, or a "sophomore slump" is one of the most persistent errors in applied work — **and the same arithmetic explains why punishment appears to work and praise appears to backfire.**
>
> **A second reading of the same formula:** $\rho=0.6$ sounds impressive but gives $\rho^2=0.36$. **Always square a correlation before interpreting it as explanatory power.**

> [!warning] Marginal, conditional, and joint are three different objects
> | Object | Formula | Question it answers |
> |---|---|---|
> | **Joint** | $f(x,y)$ | How do they behave together? |
> | **Marginal** | $\int f(x,y)\,dy$ | How does $X$ behave, ignoring $Y$? |
> | **Conditional** | $f(x,y)/f_Y(y)$ | How does $X$ behave when $Y$ is *known* to be $y$? |
>
> **Marginal integrates $Y$ out; conditional fixes $Y$ and renormalises.** Confusing them is the source of most sign errors in Bayesian work, and of Simpson's paradox — **where the marginal and conditional relationships point in opposite directions** ([[Data Preparation and Visualization/contents/00-Index|Data Prep & Visualization]]).

> [!warning] The $n!$ in the order-statistic density is not decoration
> $$f_{X_{(1)},\dots,X_{(n)}}(x_1,\dots,x_n)=n!\,f(x_1)\cdots f(x_n)\quad\text{on } x_1<\dots<x_n$$
> **Dropping the $n!$ gives a density integrating to $1/n!$.** It is there because sorting is many-to-one: **$n!$ different samples produce the same sorted output.**
>
> **The same bookkeeping appears in the single-order-statistic formula** as $\frac{n!}{(j-1)!\,1!\,(n-j)!}$ — a multinomial coefficient for the three groups "below / at / above."

> [!warning] The Jacobian is inverted, and this is easy to get backwards
> $$f_{Y_1,Y_2}(y_1,y_2)=f_{X_1,X_2}(x_1,x_2)\,\big|J(x_1,x_2)\big|^{-1}$$
> where $J$ is the determinant of $\partial g/\partial x$ — **the derivative of the *forward* map, appearing with a negative power.** If you instead compute the Jacobian of the *inverse* map $h$, it appears with a **positive** power. Both are correct; **mixing them is not.**
>
> **The self-check that never fails: does the resulting density integrate to 1?** If a factor is upside-down, this catches it immediately.

> [!note] Cross-subject connections
> - [[03 - Conditional Probability and Independence|Ch. 03]] — **§4–5 are that chapter with a random variable in place of an event**; the limiting definition is the only genuinely new idea.
> - [[05 - Continuous Random Variables|Ch. 05]] — **§7 is its change-of-variables formula in $n$ dimensions**, and §3b finally proves that a $\Gamma(n,\lambda)$ is a sum of $n$ exponentials.
> - [[07 - Properties of Expectation|Ch. 07]] — **covariance and correlation**, which quantify the dependence this chapter only detects; also conditional *expectation* as a random variable.
> - [[08 - Limit Theorems|Ch. 08]] — the CLT is a statement about $\sum X_i$, so §3's closure results are its exactly-solvable special cases.
> - [[09 - Additional Topics in Probability|Ch. 09]] — **Examples 2b and 7e are the Poisson process** in all but name.
> - [[10 - Simulation|Ch. 10]] — **Box–Muller (Example 7b)** and Example 2g's random-subset algorithm are simulation methods stated early.
> - [[Mathematical Statistics/contents/04 - Sampling Distributions|Mathematical Statistics ch. 04]] — **$\chi^2$, $t$ and the normal-sum property are constructed here**; ch. 05's sufficiency is Example 4d.
> - [[Econometrics/contents/00-Index|Econometrics]] — **§5b is the population regression function.** Linearity, homoskedasticity and $R^2$ are theorems about the bivariate normal before they are assumptions about data.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — joint vs conditional modelling is exactly the **generative/discriminative** distinction; the beta–binomial conjugacy of Example 5e underlies Thompson sampling.
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — Example 3d's lognormal random walk is the reason returns are modelled in logs.
> - [[Linear Algebra/contents/00-Index|Linear Algebra]] — the Jacobian is a **determinant**, and $|\det|$ as a volume-scaling factor is exactly the geometric content needed here.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **An arithmetic error in the source, verified three ways.** Ross's variation on the birthday problem (§6.1, Example 1g) states that for $n=88$,
> $$\sum_{i=0}^{44}\frac{365!}{i!\,(88-2i)!\,(277+i)!}\cdot\frac{88!}{2^i}\left(\tfrac1{365}\right)^{88}\approx.504$$
> **Evaluating the sum in exact log-gamma arithmetic gives $.48893$**, confirmed by direct simulation ($.48938$ over 400,000 runs, standard error $\approx.0008$ — the printed value is 18 standard errors away). **The value $.504$ is the answer for $n=87$ ($.50055$).** So the correct statement is that **87 people is the last group size for which a shared-birthday *triple* is less likely than not.** *(Flagged in §1c.)* This also usefully corrects the [[04 - Random Variables|ch. 04]] Poisson estimate of $n\approx84$, which is three people low.
>
> **Source typos** (not extraction artefacts):
> - **Example 3e ends "Thus, $X+X$ has a Poisson distribution with parameter $\lambda_1+\lambda_2$"** — should be $X+Y$.
> - **Example 2e** concludes "it follows from assumption 2 that $\sigma^2=\sigma^2$" — **the subscripts have been lost**; the claim is $\sigma_X^2=\sigma_Y^2$. In the same example $f_X(x)=ke^{-x^2/2\sigma^2}$ is written without its normalising constant two lines before $f_Y$ is given *with* one.
> - **§6.3.1** has "Because the proceeding equation is true for $n=1$" — *preceding*.
> - **Example 2i** slides between $N(0)=10^{30}$ **protons** and $h=10^{30}$ **years** ("suppose that we follow $h$ protons for $c$ years"). **The two are numerically equal only by coincidence of the chosen figures**; the derivation $N(0)-N(c)\to c\log 2$ depends on that coincidence and would not survive different numbers.
>
> **Figures are images and cannot be extracted:**
> - **Figure 6.1** (the disc with the random point $(X,Y)$ and radius $R$) — only `(0, 0)`, `(X, Y)`, `R`, `x`, `y` survive. **The geometry is fully described in the text**, so Example 1e is reconstructible.
> - **Figure 6.2** (Buffon's needle: the right triangle with hypotenuse $L/2$, leg $X$, angle $\theta$) — **extracts as nothing at all**, just the caption. **The condition $X<\tfrac L2\cos\theta$ is stated algebraically in the text**, which is enough to follow the calculation, but **the picture that makes it obvious is lost.**
> - **Figure 6.3** (the triangular density of $X+Y$) — only the tick labels `1`, `12`, `a`, `f(a)`, `0` survive; `12` is a mangled "1  2" on the $a$-axis.
> - **Figure 6.4** (the polar-coordinate diagram for Example 7b) — extracts as `Y X R U`, where **`U` is a mangled $\Theta$** and the caption `•=Random point. (X, Y) = (R, Θ)` is itself garbled (it should indicate the correspondence, not equality).
> - **The diagram in Problem 6.16** (points on a circle contained in a semicircle) is an image with no extractable content.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and checked against numeric answers):
> - **`…` is `≤`**, **`Ú` is `≥`**, **`q` is `∞`**, **`Z` is `≠`**, **`L` is `≈`**, **`K` is `≡`**, **`(` is `⊂`** — the same substitution set as chapters 1–5. In §6.7, `2 * 2 determinant` is "$2\times2$ determinant"; in §6.5c, `/Gamma1` is $\Gamma$ and `/Theta1` is $\Theta$; in Example 8b, `3` is a mangled `⟺`.
> - **Binomial coefficients extract across four lines** (`⎣`, numerator, denominator, `)`), and **fractions extract as numerator-newline-denominator** throughout — e.g. Table 6.1's `10 220` is $\tfrac{10}{220}$.
> - **`<` and `>` survive intact**, unlike the `<`-eating bug in [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — so all the strict inequalities defining regions in §§6–8 are trustworthy as extracted.
>
> **Verification performed:** every numeric claim in Examples 1a–8d was independently recomputed. **Table 6.1** (all ten cells, row sums $84,108,27,1$ and column sums $56,112,48,4$ out of 220) and **Table 6.2** (all ten cells and both sets of margins $.3750,.3875,.2000,.0375$) reproduce exactly. Also confirmed: $e^{-1}(1-e^{-2})=.3181$ and $\tfrac13$ (Example 1d); $\mathbb{E}[D]=\tfrac{2R}3$ (1e); $\tfrac{25}{36}$ (2c); $\tfrac{2L}{\pi D}$ by symbolic integration (2d); $\tfrac34$ (2h); $c\log2=.6931c$, $1.3863$ decays and $P\{0\text{ decays}\}=\tfrac14$ (2i); $\mathbb{E}[N]=e$ (§3.3.1); $\Gamma(\tfrac52)=\tfrac34\sqrt\pi$ (§3.3.2); **all of Example 3c** — $10.4$, $6.24$, $12.6$, $3.78$, mean $23$, variance $10.02$, $z=.4739\to.3178$ and $z=.8530\to.1968$, **against exact binomial convolutions of $.3182$ and $.1958$**; $.5894$, $.3474$, $z=.31965$, $.6254$ (3d); $\tfrac{11}{16}$ (6b); $(1-2d)^3$ (6a); the range density and $\text{Beta}(n-1,2)$ (6c); and the quadratic form $Q=\tfrac{y_1^2}3+\tfrac23y_2^2+\tfrac23y_3^2-\tfrac23y_2y_3$ with $J=3$ (7d). **All agree with the text except the $n=88$ birthday value documented above.**
>
> **One scope note:** §§6.6 and 6.8 are starred as optional in Ross. **I have kept both** — order statistics because the min, max, median and range are unavoidable in applied work, and exchangeability because it is the assumption that actually holds in sampling-without-replacement and reinforcement settings where i.i.d. does not. **Neither is optional for a data-science reader.**

#probability #joint-distribution #independence #convolution #conditional-distribution #order-statistics #bivariate-normal #jacobian #exchangeability
