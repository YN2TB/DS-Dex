---
subject: Probability Theory
chapter: 10
tags: [ds, probability, simulation, monte-carlo, inverse-transform, rejection-sampling, variance-reduction]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 10 (pp. 462–479)"
---

# Simulation

> [!abstract] What this chapter is for
> **The escape hatch.** When a probability cannot be computed — and most real ones cannot — you can *estimate* it by running the experiment many times. **The strong law of large numbers ([[08 - Limit Theorems|ch. 08]]) guarantees the estimate converges; the central limit theorem tells you how far off it is.** That is the whole justification for Monte Carlo, and it is why this chapter belongs at the end of the book rather than in a computing course.
>
> Ross's opening question is the right one: *what is the probability of winning a game of solitaire?* There are $52!$ orderings, no way to characterise the winning ones, and no route to an exact answer. **But you can play it 100,000 times.**
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Random numbers, random permutations | Everything is built from $U(0,1)$ |
> | **2** | **Inverse transform** and **rejection** | The two general recipes for any distribution |
> | **3** | Discrete distributions | The same two ideas, plus tricks per family |
> | **4** | **Variance reduction** | **The estimator's variance is the deliverable** — a 60× reduction is a 60× saving in compute |
>
> **The chapter's real lesson is §4.** Anyone can average $n$ simulated values; the skill is arranging for those values to have small variance. **A 60-fold variance reduction is worth more than a 60-fold faster computer**, and Exercise 5 achieves exactly that with two lines of change.

---

## 📘 Main Knowledge

### 1. Random numbers, and the random permutation

**Everything starts from a uniform.** A *random number* means a $U(0,1)$ variate; a computer produces **pseudorandom** ones, typically by a linear congruential recursion

$$X_{n+1}=(aX_n+c)\bmod m,\qquad U_n=X_n/m$$

starting from a **seed** $X_0$. **The sequence is completely deterministic** — which is a feature: setting the seed makes a simulation reproducible.

> [!warning] "Pseudorandom" is a real caveat, not a formality
> A linear congruential generator has **period at most $m$**, and its output lies on a lattice of hyperplanes in higher dimensions — which is why old generators (notoriously RANDU) produced catastrophically wrong answers in 3-D simulations while passing 1-D tests.
>
> **Modern practice: use a Mersenne Twister or PCG, never a hand-rolled LCG, and always record the seed.** A simulation whose seed you did not record is not reproducible, and an unreproducible number is not a result.

> [!example] Example 1a — generating a random permutation
> To draw uniformly from all $n!$ orderings of $1,\dots,n$:
>
> 1. Start with any permutation $X(1),\dots,X(n)$.
> 2. Set $I=n$.
> 3. Generate $U$ and set $N=\lfloor IU\rfloor+1$.
> 4. Swap $X(N)$ and $X(I)$.
> 5. Decrease $I$ by 1; if $I>1$ go to step 3.
>
> **This is the Fisher–Yates shuffle**, and it is $O(n)$ with each of the $n!$ orderings exactly equally likely. **The key sub-step is $N=\lfloor kU\rfloor+1$**, which makes $N$ uniform on $\{1,\dots,k\}$ because $kU$ is uniform on $(0,k)$.
>
> **The standard application is randomised assignment.** To split $n$ subjects into groups of sizes $n_1,\dots,n_m$, permute $1,\dots,n$ and cut the permutation into consecutive blocks. **This is how treatment assignment in an experiment should be done** — the alternative, ad-hoc assignment, is exactly how confounding enters ([[Econometrics/contents/00-Index|Econometrics]]).

> [!warning] The naive shuffle is wrong, and the bug is invisible
> A very common mistake is to loop $i=1,\dots,n$ and swap $X(i)$ with $X(\text{random over all } n)$. **That produces $n^n$ equally likely execution paths mapping onto $n!$ permutations, and $n^n$ is not divisible by $n!$ for $n\ge3$ — so some permutations are strictly more likely than others.**
>
> **Fisher–Yates draws from $\{1,\dots,I\}$, shrinking each step**, giving exactly $n!$ paths and a uniform result. **The two versions differ by one character and the biased one looks fine to the eye.**

---

### 2. Simulating continuous random variables

#### 2a. The inverse transform method

> [!important] Proposition 2.1
> If $U\sim U(0,1)$ and $F$ is a continuous distribution function, then
> $$Y=F^{-1}(U)\quad\text{has distribution function } F$$

**The proof is one line:** $P\{F^{-1}(U)\le a\}=P\{U\le F(a)\}=F(a)$, using that $F$ is monotone.

> [!tip] The picture
> **$F$ maps the $x$-axis onto $(0,1)$ in a way that stretches high-density regions and compresses low-density ones.** Running it backwards from a uniform therefore drops points into $x$-space in proportion to the density. **Pick a height uniformly on the $y$-axis of the cdf plot, read across to the curve, then down.**

| Target | $F(x)$ | Simulator |
|---|---|---|
| Exponential$(\lambda)$ | $1-e^{-\lambda x}$ | $X=-\tfrac1\lambda\log U$ |
| Pareto$(a,\lambda)$ | $1-(a/x)^\lambda$ | $X=aU^{-1/\lambda}$ |
| Weibull$(\alpha,\beta)$ | $1-e^{-(x/\beta)^\alpha}$ | $X=\beta(-\log U)^{1/\alpha}$ |
| $F(x)=x^n$ on $(0,1)$ | $x^n$ | $X=U^{1/n}$ |
| Gamma$(n,\lambda)$, $n$ integer | — | $X=-\tfrac1\lambda\log\!\left(\prod_{i=1}^n U_i\right)$ |

**Note the exponential trick:** $-\log(1-U)$ is exponential, and since $1-U$ has the same distribution as $U$, **$-\log U$ works and is one subtraction cheaper.** The gamma line then follows because a $\Gamma(n,\lambda)$ is a sum of $n$ independent exponentials ([[06 - Jointly Distributed Random Variables|ch. 06 §3b]]) — **and summing logs is taking the log of a product.**

> [!warning] The method requires an invertible $F$ in closed form — and the normal has none
> $$\Phi(x)=\frac1{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}dt$$
> **has no elementary inverse.** Numerical inversion exists and is used in practice, but it is why §2b and §2c exist at all. **The most important distribution in the book is the one the simplest method cannot handle.**

#### 2b. The rejection method

Suppose you can simulate from a density $g$, want a density $f$, and know a constant $c$ with $\dfrac{f(y)}{g(y)}\le c$ for all $y$.

> [!important] The rejection algorithm
> 1. Generate $Y$ from $g$ and an independent $U\sim U(0,1)$.
> 2. **If $U\le\dfrac{f(Y)}{c\,g(Y)}$, set $X=Y$; otherwise return to step 1.**
>
> **Proposition 2.2:** $X$ has density $f$.
> **Remark (b):** each pass accepts with probability exactly $1/c$, so the **number of iterations is Geometric with mean $c$.**

> [!tip] The geometry, and why $c$ is the whole story
> **Draw $c\,g$ as an envelope over $f$.** Throw a point uniformly under the envelope; keep it if it also lands under $f$. **The fraction kept is $\dfrac{\text{area under }f}{\text{area under }cg}=\dfrac1c$.**
>
> **So $c$ is the cost, and it must be $\ge1$** (both densities integrate to 1). **Choose $g$ to hug the shape of $f$** — the closer the fit, the closer $c$ is to 1. **A badly matched envelope is fatal: if $c=100$, 99% of the work is discarded.** And **if $f/g$ is unbounded, no $c$ exists and the method fails outright** — which happens whenever $f$ has heavier tails than $g$.

> [!example] Example 2c — a normal by rejection
> Simulate $|Z|$, whose density is $f(x)=\sqrt{2/\pi}\,e^{-x^2/2}$ on $(0,\infty)$, using an $\text{Exp}(1)$ envelope $g(x)=e^{-x}$:
> $$\frac{f(x)}{g(x)}=\sqrt{\tfrac{2e}{\pi}}\,\exp\!\left\{-\tfrac{(x-1)^2}2\right\}\ \le\ \sqrt{\tfrac{2e}{\pi}}=c=1.3155$$
> so $\dfrac{f(x)}{c\,g(x)}=\exp\{-(x-1)^2/2\}$, and the test $U\le e^{-(Y-1)^2/2}$ is equivalent to $-\log U\ge(Y-1)^2/2$. Since $-\log U$ is itself $\text{Exp}(1)$:
>
> > **Step 1.** Generate $Y_1\sim\text{Exp}(1)$.
> > **Step 2.** Generate $Y_2\sim\text{Exp}(1)$.
> > **Step 3.** If $Y_2-(Y_1-1)^2/2>0$, set $Y=Y_2-(Y_1-1)^2/2$ and continue; else go to Step 1.
> > **Step 4.** Generate $U$; set $Z=Y_1$ if $U\le\tfrac12$, else $Z=-Y_1$.
>
> **The elegant part is Step 3.** By memorylessness, the *excess* $Y_2-(Y_1-1)^2/2$ is itself $\text{Exp}(1)$ **and independent of $Z$** — so the algorithm produces a free exponential alongside each normal, which can be recycled as the next $Y_1$. **The result is $1.64=2(1.32)-1$ exponentials per normal.**
>
> **$c=1.32$ means only 24% of work is wasted** — an unusually good envelope, because the exponential's tail matches the normal's reasonably well on $(0,\infty)$.

#### 2c. Box–Muller and the polar method

From [[06 - Jointly Distributed Random Variables|ch. 06 §7]] (Example 7b): if $X,Y$ are independent standard normals, their polar coordinates satisfy $R^2\sim\text{Exp}(\tfrac12)$ independent of $\Theta\sim U(0,2\pi)$. Inverting:

$$\boxed{\ X=\sqrt{-2\log U_1}\,\cos(2\pi U_2),\qquad Y=\sqrt{-2\log U_1}\,\sin(2\pi U_2)\ }$$

**This is the Box–Muller transform** — two uniforms in, two independent standard normals out, **exactly, with no rejection at all.** Its weakness is the two trigonometric evaluations.

> [!important] The polar (Marsaglia) method removes the trigonometry
> 1. Generate $U_1,U_2$; set $V_1=2U_1-1$, $V_2=2U_2-1$, $S=V_1^2+V_2^2$.
> 2. **If $S>1$, go back to step 1.**
> 3. Return $\displaystyle X=\sqrt{\frac{-2\log S}{S}}\,V_1,\qquad Y=\sqrt{\frac{-2\log S}{S}}\,V_2$.
>
> **The trick:** conditional on landing in the unit disc, $\cos\Theta=V_1/R$ and $\sin\Theta=V_2/R$ come free from the coordinates, **and $S=R^2$ is itself uniform on $(0,1)$ and independent of $\Theta$** — so it doubles as the third random number.

**Cost:** acceptance probability $\pi/4=.785$, so $4/\pi=1.273$ iterations and $2.546$ random numbers per **pair** of normals, plus one log, one square root, one division and $4.546$ multiplications. **Trading 27% wasted uniforms for two eliminated trig calls was a good deal in 1970 and is roughly a wash today** — but the method is still standard, and it is the reason "generate a point in the square, reject outside the circle" is the canonical rejection picture.

**Chi-squared (Example 2e):** since $Z_1^2+Z_2^2\sim\text{Exp}(\tfrac12)$,

$$\chi^2_{2k}=-2\log\!\left(\prod_{i=1}^k U_i\right),\qquad \chi^2_{2k+1}=Z^2-2\log\!\left(\prod_{i=1}^k U_i\right)$$

---

### 3. Simulating discrete distributions

**The discrete inverse transform:** with $P\{X=x_j\}=P_j$, set

$$X=x_j\quad\text{when}\quad \sum_{i<j}P_i<U\le\sum_{i\le j}P_i$$

i.e. **walk along the cumulative probabilities until you pass $U$.**

> [!tip] Order the outcomes by decreasing probability
> The expected number of comparisons is $\sum_j j\,P_j$, which is **minimised by putting the most likely value first**. *(Exercise 2 measures the saving: 2.80 comparisons versus 2.15 on a four-point distribution — a 23% cut for zero cost.)* **For a large alphabet, use a binary search on the cumulative table, or the alias method for $O(1)$.**

| Distribution | Method |
|---|---|
| **Geometric$(p)$** | $X=1+\left\lfloor\dfrac{\log U}{\log(1-p)}\right\rfloor$ |
| **Binomial$(n,p)$** | Count how many of $U_1,\dots,U_n$ are $<p$ |
| **Poisson$(\lambda)$** | $X=\max\left\{n:\prod_{i=1}^n U_i\ge e^{-\lambda}\right\}$ |

> [!tip] Why the Poisson recipe works — it *is* the Poisson process
> Taking logs turns $\prod U_i\ge e^{-\lambda}$ into $\sum(-\log U_i)\le\lambda$, and each $-\log U_i$ is $\text{Exp}(1)$. **So $X$ counts how many unit-rate exponential interarrivals fit into a time interval of length $\lambda$ — which is exactly $N(\lambda)$ for a rate-1 Poisson process** ([[09 - Additional Topics in Probability|ch. 09 §1]]).
>
> **The algorithm is not a formula but a re-enactment of the process**, and that is the general lesson: **the cheapest simulator usually comes from the distribution's construction, not from its density.** The binomial recipe is the same idea (a binomial *is* $n$ Bernoulli trials), as is the gamma-from-exponentials of §2a.

---

### 4. Variance reduction

To estimate $\theta=\mathbb{E}[g(X_1,\dots,X_n)]$, generate $k$ independent replicates $Y_1,\dots,Y_k$ of $g(\mathbf X)$ and average. Then $\mathbb{E}[\bar Y]=\theta$ and

$$\mathbb{E}[(\bar Y-\theta)^2]=\mathrm{Var}(\bar Y)=\frac{\mathrm{Var}(Y_i)}{k}$$

> [!important] The variance *is* the deliverable
> **Unbiasedness is free; precision is what costs.** Since the error scales as $\sigma/\sqrt k$, **cutting the standard error in half requires 4× the work — or one good idea.** A method that reduces $\mathrm{Var}(Y_i)$ by a factor of 60 is worth a 60× faster computer.

#### 4a. Antithetic variables

$$\mathrm{Var}\!\left(\frac{Y_1+Y_2}2\right)=\frac{\mathrm{Var}(Y_1)}2+\frac{\mathrm{Cov}(Y_1,Y_2)}2$$

so **negatively correlated replicates beat independent ones.** If $Y_1=g(F_1^{-1}(U_1),\dots,F_n^{-1}(U_n))$, take

$$Y_2=g\big(F_1^{-1}(1-U_1),\dots,F_n^{-1}(1-U_n)\big)$$

**$1-U$ is uniform (so $Y_2$ has the right distribution) and is perfectly negatively correlated with $U$.** It is provably beneficial whenever $g$ is monotone — and there is a bonus: **you reuse the uniforms instead of generating new ones.**

#### 4b. Conditioning (Rao–Blackwellisation)

From the conditional variance formula ([[07 - Properties of Expectation|ch. 07 §4b]]),

$$\mathrm{Var}(\mathbb{E}[Y\mid Z])\le\mathrm{Var}(Y)\qquad\text{while}\qquad \mathbb{E}\big[\mathbb{E}[Y\mid Z]\big]=\mathbb{E}[Y]$$

> [!important] **Whenever you can compute part of the answer analytically, do — never simulate what you can integrate.**
> $\mathbb{E}[Y\mid Z]$ is always at least as good an estimator as $Y$, with equality only when $\mathrm{Var}(Y\mid Z)\equiv0$.

> [!example] Example 4a — estimating $\pi$, three ways
> With $V_i=2U_i-1$, the point $(V_1,V_2)$ is uniform on the square of area 4, and $P\{V_1^2+V_2^2\le1\}=\pi/4$.
>
> | Estimator | Idea | Variance |
> |---|---|---|
> | $I=\mathbb{1}\{V_1^2+V_2^2\le1\}$ | count points in the circle | $.16855$ |
> | $\mathbb{E}[I\mid V_1]=\sqrt{1-V_1^2}$ | **integrate out $V_2$** | $.04982$ |
> | $\tfrac12\!\left[\sqrt{1-U^2}+\sqrt{1-(1-U)^2}\right]$ | conditioning **+** antithetic | $.00686$ |
>
> **Conditioning alone gives a 3.4× reduction; adding antithetic variables gives 24.6× overall** — the same accuracy for one twenty-fourth of the work. *(All three variances verified by exact integration.)*
>
> **Why conditioning helps here is worth seeing.** The crude estimator is a coin flip — it throws away everything about *where* the point landed and keeps one bit. **Conditioning on $V_1$ replaces that bit with the exact conditional probability $\sqrt{1-V_1^2}$**, which is the same on average and far less variable.
>
> Ross's simulated estimates of $\pi$ with $n=10{,}000$: $3.1612$, $3.128448$, $3.139578$ — and $3.143288$ with $n=64{,}000$ using the last method.

#### 4c. Control variates

If $\mathbb{E}[f(\mathbf X)]=\mu$ is **known**, then for any constant $a$,

$$W=g(\mathbf X)+a\big[f(\mathbf X)-\mu\big]$$

is still unbiased for $\mathbb{E}[g(\mathbf X)]$, and

$$\mathrm{Var}(W)=\mathrm{Var}[g]+a^2\mathrm{Var}[f]+2a\,\mathrm{Cov}[g,f]$$

is minimised at

$$a^*=-\frac{\mathrm{Cov}[f,g]}{\mathrm{Var}[f]}\qquad\Longrightarrow\qquad \boxed{\ \mathrm{Var}(W)=\mathrm{Var}[g]\left(1-\rho^2_{f,g}\right)\ }$$

> [!tip] This is regression, and it is the same formula as ch. 07
> **$a^*$ is exactly the least-squares slope of $g$ on $f$, and the residual variance is $\sigma_g^2(1-\rho^2)$** — identical to the best-linear-predictor formula of [[07 - Properties of Expectation|ch. 07 §5a]]. **A control variate subtracts off the part of the noise that a known quantity can predict.**
>
> **The practical wrinkle:** $\mathrm{Cov}[f,g]$ and $\mathrm{Var}[f]$ are usually unknown, so they are **estimated from the same simulated data** — which introduces a small bias but recovers nearly all the theoretical gain. **Choose $f$ strongly correlated with $g$ and with a known mean.**

**A related idea from the exercises: importance sampling.** To estimate $\int_0^1 g(x)\,dx$, simulate $X$ from a density $f$ and average $g(X)/f(X)$. **Choosing $f$ shaped like $g$ makes the ratio nearly constant, hence low-variance** — and unlike the methods above, importance sampling can also make *rare events* estimable by sampling them more often than they occur.

---

## ✏️ Exercises

> [!question] Exercise 1 — the inverse transform *(warm-up)*
> Give a method using a single random number $U$ for each of the following.
>
> (i) $X\sim\text{Exp}(2)$.
> (ii) $F(x)=x^3$ on $(0,1)$.
> (iii) Weibull: $F(x)=1-e^{-(x/\beta)^\alpha}$, $x>0$.
> (iv) Pareto: $F(x)=1-(a/x)^\lambda$, $x>a$.
> (v) $f(x)=Ce^x$ on $(0,1)$ — find $C$ first.
> (vi) Explain why this method cannot be used directly for the normal.

> [!example]- Solution
> **(i)** $1-e^{-2x}=u\Rightarrow x=-\tfrac12\log(1-u)$, and since $1-U\overset{d}{=}U$: $\boxed{X=-\tfrac12\log U}$
>
> **(ii)** $x^3=u\Rightarrow \boxed{X=U^{1/3}}$
>
> **(iii)** $1-e^{-(x/\beta)^\alpha}=u\Rightarrow (x/\beta)^\alpha=-\log(1-u)\Rightarrow \boxed{X=\beta(-\log U)^{1/\alpha}}$
> **Note $\alpha=1$ recovers the exponential** — the Weibull is a power-transformed exponential, which is why its hazard rate is a power of $t$ ([[05 - Continuous Random Variables|ch. 05]]).
>
> **(iv)** $1-(a/x)^\lambda=u\Rightarrow (a/x)^\lambda=1-u\Rightarrow \boxed{X=aU^{-1/\lambda}}$
> *(Check: $P\{aU^{-1/\lambda}>x\}=P\{U<(a/x)^\lambda\}=(a/x)^\lambda$ ✓.)*
>
> **(v)** $\int_0^1Ce^xdx=C(e-1)=1$, so $C=\dfrac1{e-1}$. Then $F(x)=\dfrac{e^x-1}{e-1}$, and
> $$\frac{e^x-1}{e-1}=u\ \Longrightarrow\ \boxed{X=\log\big(1+U(e-1)\big)}$$
>
> **(vi)** **$\Phi$ has no closed-form inverse** — it is not an elementary function. Numerical inversion is possible (and is what `scipy.stats.norm.ppf` does), but the *analytic* route is closed, which is exactly why Box–Muller, the polar method and rejection all exist.

> [!question] Exercise 2 — discrete distributions
> (i) Give an inverse-transform algorithm for $p=(.15,.20,.35,.30)$ on $\{1,2,3,4\}$, and compute the expected number of comparisons.
> (ii) Reorder to minimise that number. How much is saved?
> (iii) Derive the geometric simulator $X=1+\left\lfloor\frac{\log U}{\log(1-p)}\right\rfloor$, and evaluate it at $p=.3$, $U=.5$.
> (iv) Explain why $X=\max\{n:\prod_1^n U_i\ge e^{-\lambda}\}$ is Poisson$(\lambda)$.

> [!example]- Solution
> **(i)** Cumulative: $.15,\ .35,\ .70,\ 1.00$. Return 1 if $U\le.15$; 2 if $.15<U\le.35$; 3 if $.35<U\le.70$; else 4.
> $$\mathbb{E}[\#\text{comparisons}]=1(.15)+2(.20)+3(.35)+4(.30)=\boxed{2.80}$$
>
> **(ii)** Order by decreasing probability: $(.35,.30,.20,.15)$ on values $(3,4,2,1)$:
> $$1(.35)+2(.30)+3(.20)+4(.15)=\boxed{2.15}$$
> **A 23% saving for no cost at all** — just a sort done once. **For an alphabet of thousands, use binary search on the cumulative table ($O(\log n)$) or the alias method ($O(1)$).**
>
> **(iii)** $X=j$ iff $\sum_{i<j}P_i<U\le\sum_{i\le j}P_i$, i.e. $1-(1-p)^{j-1}<U\le1-(1-p)^j$, i.e. $(1-p)^j\le1-U<(1-p)^{j-1}$. Replacing $1-U$ by $U$:
> $$X=\min\{j:(1-p)^j\le U\}=\min\left\{j:j\ge\frac{\log U}{\log(1-p)}\right\}=1+\left\lfloor\frac{\log U}{\log(1-p)}\right\rfloor$$
> **The inequality flips because $\log(1-p)<0$** — the single most likely place to make a sign error here.
>
> At $p=.3$, $U=.5$: $\dfrac{\log.5}{\log.7}=\dfrac{-.6931}{-.3567}=1.943$, so $X=1+\lfloor1.943\rfloor=\boxed{2}$.
>
> **(iv)** Take logs: $\prod_1^n U_i\ge e^{-\lambda}\iff\sum_1^n(-\log U_i)\le\lambda$. Each $-\log U_i\sim\text{Exp}(1)$, so **$X$ is the largest number of unit-rate exponential gaps fitting inside an interval of length $\lambda$** — which is $N(\lambda)$ for a rate-1 Poisson process, i.e. $\text{Poisson}(\lambda)$ ([[09 - Additional Topics in Probability|ch. 09 §1]]). $\blacksquare$
>
> **The moral: simulate the *construction*, not the formula.** Every efficient recipe in this chapter comes from re-enacting how the distribution arises.

> [!question] Exercise 3 — the rejection method
> (i) Devise a rejection algorithm for $f(x)=30(x^2-2x^3+x^4)$ on $(0,1)$, using $g=U(0,1)$. Identify the distribution, find $c$, and give the acceptance probability and the expected number of uniform pairs per accepted value.
> (ii) Devise a rejection algorithm for $f(x)=\tfrac{15}{64}x^2(4-x^2)$ on $[0,2]$ using $g(x)=x/2$. Find $c$ exactly.
> (iii) State the two ways rejection sampling can fail.

> [!example]- Solution
> **(i)** Factorise: $f(x)=30x^2(1-x)^2$ — **this is Beta$(3,3)$**, since $B(3,3)=\frac{\Gamma(3)\Gamma(3)}{\Gamma(6)}=\frac{2!\,2!}{5!}=\frac1{30}$ ([[06 - Jointly Distributed Random Variables|ch. 06 §7]]).
>
> With $g\equiv1$, $c=\max_x f(x)$. By symmetry the maximum is at $x=\tfrac12$:
> $$c=30\left(\tfrac12\right)^2\left(\tfrac12\right)^2=\frac{30}{16}=\boxed{1.875}$$
> **Algorithm:** generate $U_1,U_2$; if $U_2\le\dfrac{30U_1^2(1-U_1)^2}{1.875}=16U_1^2(1-U_1)^2$, return $X=U_1$; else repeat.
>
> Acceptance probability $=1/c=\boxed{.533}$; expected iterations $=c=\boxed{1.875}$, i.e. **3.75 uniforms per accepted value.** **Nearly half the work is discarded** — the uniform envelope is a poor fit to a bell-shaped Beta.
>
> **(ii)** $\dfrac{f(x)}{g(x)}=\dfrac{15}{64}x^2(4-x^2)\cdot\dfrac2x=\dfrac{15}{32}x(4-x^2)=\dfrac{15}{32}(4x-x^3)$.
> Setting the derivative to zero: $4-3x^2=0\Rightarrow x=\dfrac2{\sqrt3}$. Then $x(4-x^2)=\dfrac2{\sqrt3}\cdot\dfrac83=\dfrac{16}{3\sqrt3}$, so
> $$c=\frac{15}{32}\cdot\frac{16}{3\sqrt3}=\frac{5}{2\sqrt3}=\frac{5\sqrt3}{6}=\boxed{1.4434}$$
> Acceptance probability $=\dfrac6{5\sqrt3}=\boxed{.693}$ — **noticeably better than (i), because $g(x)=x/2$ rises with $f$ instead of being flat.**
>
> **(iii)**
> - **$c$ too large.** The algorithm still works but wastes a fraction $1-1/c$ of all effort. **This is the usual failure, and it worsens sharply in high dimensions** — envelopes that fit well in 1-D can have $c$ growing exponentially in the number of variables, which is why MCMC ([[09 - Additional Topics in Probability|ch. 09 §2]]) displaces rejection for hard problems.
> - **$f/g$ unbounded — no $c$ exists.** This happens whenever **$f$ has heavier tails than $g$**, e.g. trying to sample a Cauchy using a normal envelope. **Always check the tail ratio before the mode.**

> [!question] Exercise 4 — three ways to simulate a normal *(medium–hard)*
> Compare the Box–Muller, rejection, and polar methods on cost.
>
> (i) Write down Box–Muller. What does it cost per pair of normals?
> (ii) The rejection method of Example 2c has $c=\sqrt{2e/\pi}$. Compute it and the acceptance rate.
> (iii) The polar method rejects points outside the unit disc. Find the acceptance probability and the expected number of uniforms per pair of normals.
> (iv) Which would you use, and why is the polar method's rejection *not* wasteful in the way Exercise 3(i)'s was?

> [!example]- Solution
> **(i)** $X=\sqrt{-2\log U_1}\cos(2\pi U_2)$, $Y=\sqrt{-2\log U_1}\sin(2\pi U_2)$.
> **Cost: exactly 2 uniforms, 1 log, 1 square root, 1 sine, 1 cosine — with no rejection at all.** The two normals are exactly (not approximately) standard and independent.
>
> **(ii)** $c=\sqrt{2e/\pi}=\sqrt{2(2.71828)/3.14159}=\boxed{1.3155}$, so the acceptance rate is $1/c=\boxed{.760}$ and the mean number of iterations is $1.3155$.
> **With the exponential-recycling trick of §2b, this comes to $1.64$ exponentials per normal.**
>
> **(iii)** The point $(V_1,V_2)$ is uniform on a square of area 4; it is accepted if it lands in the unit disc, of area $\pi$:
> $$P\{\text{accept}\}=\frac\pi4=\boxed{.7854},\qquad \mathbb{E}[\text{iterations}]=\frac4\pi=\boxed{1.273}$$
> Each iteration uses 2 uniforms, so **$2\times1.273=2.546$ uniforms per pair of normals**, plus 1 log, 1 square root, 1 division and $4.546$ multiplications.
>
> **(iv)** **The polar method, in most implementations.** Compare per **pair** of normals:
>
> | Method | Uniforms | Transcendental calls | Rejection |
> |---|---|---|---|
> | Box–Muller | $2.000$ | log, sqrt, **sin, cos** | none |
> | Rejection (§2b) | ~$3.3$ | log ×2 | 24% |
> | **Polar** | $2.546$ | log, sqrt | **21%** |
>
> **The polar method trades 0.55 extra uniforms for two eliminated trigonometric calls** — a clear win when trig was expensive, and roughly a wash on modern hardware with vectorised `sin`/`cos`.
>
> **Why the rejection here is cheap, unlike Exercise 3(i):** the rejected work is **two multiplications and a comparison** — no evaluation of $f$, no logarithm, no square root. In Exercise 3(i) each rejected trial cost a full evaluation of a quartic. **The cost of a rejection matters as much as the rate**, and the polar method is engineered so that rejections are nearly free.
>
> **In practice: use your library.** NumPy and most modern runtimes use the **ziggurat** algorithm, a refined rejection scheme with acceptance above 99%.

> [!question] Exercise 5 — variance reduction *(hard)*
> Estimate $\theta=\displaystyle\int_0^1 e^x\,dx=e-1=1.71828$ by simulation.
>
> (i) **Crude Monte Carlo:** use $Y=e^U$. Verify it is unbiased and compute $\mathrm{Var}(Y)$.
> (ii) **Antithetic variables:** use $Y=\tfrac12(e^U+e^{1-U})$. Compute its variance and the reduction factor **per uniform generated**.
> (iii) **Control variate:** use $W=e^U+a(U-\tfrac12)$. Find the optimal $a^*$ and the resulting variance.
> (iv) How many crude simulations are needed to match the precision of 1,000 antithetic ones?

> [!example]- Solution
> **(i)** $\mathbb{E}[e^U]=\int_0^1e^u\,du=e-1=\theta$ ✓ — unbiased.
> $$\mathrm{Var}(e^U)=\mathbb{E}[e^{2U}]-\theta^2=\frac{e^2-1}2-(e-1)^2=3.19453-2.95249=\boxed{.24204}$$
>
> **(ii)** $\mathbb{E}[Y]=\tfrac12(\theta+\theta)=\theta$ ✓. With $\mathrm{Cov}(e^U,e^{1-U})=\mathbb{E}[e^Ue^{1-U}]-\theta^2=e-(e-1)^2=-.23421$:
> $$\mathrm{Var}(Y)=\tfrac12\mathrm{Var}(e^U)+\tfrac12\mathrm{Cov}(e^U,e^{1-U})=\frac{.24204-.23421}2=\boxed{.003912}$$
> **Reduction factor $=\dfrac{.24204}{.003912}=\boxed{61.9\times}$, and this is per uniform** — the antithetic estimator uses **one** $U$ to produce both terms. *(All values verified by exact integration.)*
>
> **The strong negative covariance is the whole effect: $-.234$ against a variance of $.242$ almost cancels it.** It works because $e^u$ is **monotone**, so $e^U$ and $e^{1-U}$ move in opposite directions — high draws are paired with low ones, and the pair's average is nearly constant.
>
> **(iii)** $\mathbb{E}[U-\tfrac12]=0$, so $W$ is unbiased for every $a$. With
> $$\mathrm{Cov}(e^U,U)=\mathbb{E}[Ue^U]-\tfrac12\theta=1-.85914=.14086,\qquad \mathrm{Var}(U)=\tfrac1{12}$$
> $$a^*=-\frac{\mathrm{Cov}(e^U,U)}{\mathrm{Var}(U)}=-12(.14086)=\boxed{-1.6903}$$
> $$\mathrm{Var}(W)=\mathrm{Var}(e^U)-\frac{\mathrm{Cov}^2}{\mathrm{Var}(U)}=.24204-12(.14086)^2=.24204-.23809=\boxed{.003940}$$
> a $\boxed{61.4\times}$ reduction. *(Confirmed by direct integration of $W^2$.)*
>
> **The two methods land within 1% of each other, by different routes.** Antithetic exploits monotonicity; the control variate exploits $\rho(e^U,U)=.9918$ — **$U$ predicts $e^U$ almost perfectly over $[0,1]$, and $W$ subtracts off exactly the predictable part.** $1-\rho^2=.0163$, matching the reduction.
>
> **(iv)** Matching standard errors requires $\dfrac{.24204}{n_{\text{crude}}}=\dfrac{.003912}{1000}$:
> $$n_{\text{crude}}=1000\times61.9=\boxed{61{,}900}$$
>
> > [!important] What this exercise is really showing
> > **Two lines of code bought a 62× speed-up.** No faster hardware, no better random number generator — just a change in *which* random variable is averaged.
> >
> > **And it is not a special trick.** Both methods generalise: **antithetic variables work for any monotone $g$**, and **control variates work whenever some correlated quantity has a known mean.** The control-variate formula $\mathrm{Var}=\sigma_g^2(1-\rho^2)$ is literally the best-linear-predictor result of [[07 - Properties of Expectation|ch. 07 §5a]] — **variance reduction is regression applied to your own simulation output.**
> >
> > **The same lesson in the $\pi$ example (§4b):** conditioning alone gave $3.4\times$; conditioning plus antithetic gave $24.6\times$. **The techniques compose.**

---

## 📝 Summary

- **Simulation is the strong law turned into a method:** average $n$ replicates, and the estimate converges to $\theta$; the CLT gives the error bar $\sigma/\sqrt n$. **This is the escape hatch when a probability is intractable.**
- **Everything is built from $U(0,1)$.** Pseudorandom generators are deterministic given a seed — **record the seed**, and never hand-roll a linear congruential generator.
- **Fisher–Yates ($N=\lfloor IU\rfloor+1$, swap, decrement $I$) gives a uniform random permutation in $O(n)$.** The naive variant that draws from all $n$ positions each step is **biased**, because $n^n$ paths cannot map evenly onto $n!$ outcomes.
- **Inverse transform: $X=F^{-1}(U)$.** One uniform, exact, no waste — available whenever $F$ can be inverted in closed form (exponential, Pareto, Weibull, power laws, gamma via a product of uniforms). **Not available for the normal.**
- **Rejection: draw $Y\sim g$ and accept with probability $f(Y)/[c\,g(Y)]$, where $f/g\le c$.** The number of iterations is Geometric with mean $c$, **so $c$ is the entire cost**. Choose $g$ to hug $f$; **if $f$ has heavier tails than $g$, no $c$ exists and the method fails.**
- **Box–Muller** converts two uniforms into two exact independent normals via polar coordinates. **The polar (Marsaglia) method** removes the trigonometry by rejecting points outside the unit disc — acceptance $\pi/4=.785$, so $2.546$ uniforms per pair. **Rejections there are nearly free**, which is why a 21% rejection rate is acceptable.
- **Discrete inverse transform: walk the cumulative probabilities.** **Order outcomes by decreasing probability** — a free 23% saving in Exercise 2. Binary search or the alias method for large alphabets.
- **The best discrete simulators re-enact the construction:** a binomial is $n$ Bernoulli trials; a **Poisson$(\lambda)$ is the number of unit exponential gaps fitting in $[0,\lambda]$**, hence $\max\{n:\prod U_i\ge e^{-\lambda}\}$.
- **The estimator's variance is the deliverable.** Halving the standard error costs 4× the work — or one good idea.
- **Antithetic variables:** pair $g(U)$ with $g(1-U)$. Guaranteed to help for monotone $g$, reuses the uniforms, and gave a **62× reduction** in Exercise 5.
- **Conditioning (Rao–Blackwell): $\mathrm{Var}(\mathbb{E}[Y\mid Z])\le\mathrm{Var}(Y)$ always.** **Never simulate what you can integrate.** Conditioning on $V_1$ in the $\pi$ example gave $3.4\times$, and $24.6\times$ combined with antithetic.
- **Control variates: $W=g(\mathbf X)+a[f(\mathbf X)-\mu]$ with $a^*=-\mathrm{Cov}[f,g]/\mathrm{Var}[f]$, giving $\mathrm{Var}(W)=\sigma_g^2(1-\rho^2)$** — the best-linear-predictor formula of ch. 07. **Variance reduction is regression on your own output.**
- **The techniques compose**, and none of them changes the answer — only its precision.

---

## ⚠️ Important Notes

> [!warning] Pseudorandom is not random, and the seed is part of the result
> **Linear congruential generators have a finite period and lattice structure in higher dimensions** — RANDU, shipped for years by IBM, produced points lying on 15 planes in 3-D and invalidated a generation of simulations that tested fine in 1-D.
>
> **Three rules.** Use a modern generator (Mersenne Twister, PCG, PhiloX). **Record the seed** — an unreproducible simulation is not a result. And **never reuse a stream across supposedly independent runs**, which is the parallel-computing version of the same bug.

> [!warning] The naive shuffle is biased, and the bug is silent
> ```
> for i in 1..n:  swap(X[i], X[random(1..n)])     # WRONG
> for i in n..2:  swap(X[i], X[random(1..i)])     # Fisher–Yates
> ```
> **The first has $n^n$ equally likely paths onto $n!$ outcomes, and $n!\nmid n^n$ for $n\ge3$** — so some permutations are strictly more likely. **The output looks shuffled and passes casual inspection.** This exact bug shipped in a browser vendor's ballot randomiser.

> [!warning] Rejection sampling's cost is $c$, and $c$ explodes in high dimensions
> **The expected number of iterations is exactly $c$.** A well-matched envelope gives $c\approx1.3$ (the normal in §2b); a flat envelope on a peaked target gives $c=1.875$ (Exercise 3); **a mismatched envelope in $d$ dimensions routinely gives $c$ growing exponentially in $d$.**
>
> **This is why rejection sampling is a 1-D and 2-D technique, and why MCMC ([[09 - Additional Topics in Probability|ch. 09 §2]]) exists.** MCMC gives up independence between draws in exchange for not needing a global envelope at all.
>
> **And check the tails first.** $f/g$ unbounded means no $c$ exists — a normal envelope can never cover a Cauchy, however you scale it.

> [!warning] Simulation error is $\sigma/\sqrt n$, and it must be reported
> **A simulated number without an error bar is not a number.** Quoting "$\hat\pi=3.1612$" from 10,000 draws while the standard error is $\pm.004$ overstates the precision by two digits.
>
> **Always report $\hat\theta\pm1.96\,s/\sqrt n$**, and remember the $\sqrt n$: **three more decimal places costs a million times the work.** This is the CLT of [[08 - Limit Theorems|ch. 08]] applied to your own output, and it is what makes §4 worth the effort.

> [!warning] Never simulate what you can integrate
> $$\mathrm{Var}\big(\mathbb{E}[Y\mid Z]\big)\ \le\ \mathrm{Var}(Y)\qquad\text{always}$$
> **Any part of the calculation you can do analytically should be done analytically** — the conditional-expectation estimator is never worse and is usually much better.
>
> **The $\pi$ example is the canonical illustration:** the crude estimator keeps one bit per simulated point (inside/outside), while conditioning on $V_1$ keeps the exact conditional probability. **Same expectation, one-third the variance** — and combined with antithetic variables, one twenty-fourth.

> [!warning] Variance reduction changes precision, never the answer
> **Every method here is unbiased by construction:** antithetic pairs have the right marginal distribution, $\mathbb{E}[\mathbb{E}[Y\mid Z]]=\mathbb{E}[Y]$, and $\mathbb{E}[f(\mathbf X)-\mu]=0$. **So there is no bias–variance trade-off being made** — the gain is free.
>
> **The one caveat is the estimated $a^*$ in control variates.** Estimating $\mathrm{Cov}[f,g]$ from the same data introduces a small bias, which vanishes as $n$ grows and is worth accepting for the variance gain. **Antithetic variables and conditioning have no such caveat at all.**

> [!warning] Antithetic variables need monotonicity
> **$Y_1$ and $Y_2$ are guaranteed negatively correlated only when $g$ is monotone in each argument.** For a non-monotone $g$ — say $g(u)=(u-\tfrac12)^2$ — the antithetic pair is **perfectly positively correlated** ($g(U)=g(1-U)$ identically), and the method **doubles** the variance per uniform instead of halving it.
>
> **Check monotonicity before pairing**, or estimate the covariance from a pilot run.

> [!note] Cross-subject connections
> - [[05 - Continuous Random Variables|Ch. 05]] — **the inverse transform is the probability integral transform**, and §7's change-of-variables is why it works.
> - [[06 - Jointly Distributed Random Variables|Ch. 06]] — **Box–Muller is Example 7b**; Example 2g's random-subset algorithm is a simulation method stated four chapters early; the gamma-from-exponentials fact is §3b.
> - [[07 - Properties of Expectation|Ch. 07]] — **the conditional variance formula is §4b, and the control-variate formula $\sigma_g^2(1-\rho^2)$ is the best-linear-predictor result verbatim.**
> - [[08 - Limit Theorems|Ch. 08]] — **the strong law is why simulation converges and the CLT is the error bar.** Everything in §4 is an attempt to shrink the $\sigma$ in $\sigma/\sqrt n$.
> - [[09 - Additional Topics in Probability|Ch. 09]] — the Poisson simulator **is** the Poisson process; **MCMC is §2 of that chapter turned into an algorithm**, and it is what replaces rejection sampling in high dimensions.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — **the bootstrap is this chapter applied to a sampling distribution**; permutation tests are Fisher–Yates plus a test statistic.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — random initialisation, dropout, data shuffling and stochastic gradient descent all rest on §1; **variational inference and MCMC are §4's descendants**; Thompson sampling is simulation used as a decision rule.
> - [[Econometrics/contents/00-Index|Econometrics]] — Monte Carlo studies of estimator properties are exactly this chapter; **randomised assignment is Example 1a.**
> - [[Optimization/contents/00-Index|Optimization]] — simulated annealing and stochastic search are optimisation built on these primitives.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Source typos:**
> - **§10.2, introducing Example 2b:** "The results of Example 2a can also be utilized to **stimulate** a gamma random variable" — *simulate*.
> - **Example 2e** ends "where $Z, U_1,\dots,U_n$ are independent" — **it should be $U_1,\dots,U_k$**, since the product in the displayed formula runs to $k$, not $n$.
> - **Proposition 2.2's proof** writes "Letting $X$ approach $\infty$" where the variable being taken to infinity is $x$, the argument of $P\{X\le x\}$.
> - **Example 4a** switches between $\nu$ and $V_1$ for the same quantity mid-derivation (`P{V₂² ≤ 1 − V₁²|V₁ = ν}`), and Problem 10.14 then writes $V$ with no subscript for $V_1$.
> - **Problem 10.9** lists the two branches of a piecewise $F$ with **identical formulas** for $0<x\le1$ and $x>1$; the second branch is evidently meant to be different (most likely $\tfrac13(1-e^{-3x})+\tfrac23$), so **the problem as printed is unanswerable.**
>
> **Figures are images and cannot be extracted:**
> - **Figure 10.1** (the rejection-method flowchart) extracts as a jumble of its box labels — `Generate Y , g`, `Start`, `Generate a random number U`, `Is U < f(Y)/cg(Y)`, `Yes Set X = Y`, `No` — **with all arrows and the loop-back edge lost.** The logic is fully stated in the algorithm text, so nothing is missing mathematically, but **the flowchart is the clearest statement of the method and it is gone.**
> - **Figure 10.2** (the unit disc inscribed in the square $[-1,1]^2$, with the point $(V_1,V_2)$, radius $R$ and angle $\theta$) extracts as `(1, 1) (1, 21) (–1, 1) (21, 21) R V2 V1 V1² 1 u = 1V2² = (0, 0) = (V1, V2)` — **where every `2` before a `1` is a mangled minus sign, `u` is a mangled $\theta$, and every `5` is `=`.** Reconstructed: the corners are $(\pm1,\pm1)$ and the condition is $V_1^2+V_2^2\le1$. **This figure carries the entire geometric intuition for both the polar method and the $\pi$ estimate**, and it is the chapter's most significant loss.
> - **The table of $\pi$ estimates** (§10.4.2) survives with its numbers intact — $3.1612$, $3.128448$, $3.139578$ at $n=10{,}000$, and $3.143288$ at $n=64{,}000$ — **but these are outputs of one particular simulation run and cannot be reproduced or checked without the seed**, which is not given. **I have quoted them as illustrative rather than as verified values**, and instead computed the three estimators' **exact variances** by integration, which is both checkable and more informative.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and checked against numeric answers):
> - **`…` is `≤`**, **`Ú` is `≥`**, **`q` is `∞`**, **`Z` is `≠`**, **`K` is `≡`**, **`*` is `×`**, **`5` is `=`**, **`2` is `−`** (in figure labels) — the same substitution set as chapters 1–9.
> - **`/H9008` is $\Theta$**, as in [[09 - Additional Topics in Probability|ch. 09]] — the third distinct encoding the source uses for a Greek capital, after `/Theta1` in ch. 06.
> - **`−2l o gU1` is $-2\log U_1$** — the source's letter-spacing inside `log` breaks the word throughout §§10.2–10.4, and it appears in nearly every displayed formula in the polar-method derivation.
>
> **Verification performed:** every numeric claim in the chapter was independently recomputed. Confirmed: **$c=\sqrt{2e/\pi}=1.3155$** and the derived "$1.64=2(1.32)-1$ exponentials per normal" (Example 2c); the polar method's **$4/\pi=1.2732$ iterations and $2.546$ uniforms per pair** (Example 2d); and, for Example 4a's three estimators of $\pi/4$, the **exact variances by integration** — $\tfrac\pi4(1-\tfrac\pi4)=.16855$ for the crude indicator, $\tfrac23-\tfrac{\pi^2}{16}=.049816$ for the conditioned estimator (**a $3.38\times$ reduction**), and $.006858$ for conditioned-plus-antithetic (**$24.6\times$**). **These variance figures are not in the source** — Ross reports only single simulated point estimates — **so they are my additions, and they are what actually justify his claim that each method "improves upon" the last.** The exercise figures ($\mathrm{Var}(e^U)=.24204$, antithetic $.003912$, control-variate $.003940$, $a^*=-1.6903$) were likewise verified by exact integration.
>
> **One scope note:** this is the shortest chapter in the book (18 pages) and is a **catalogue rather than a development.** Three substantial omissions worth naming: **(a) no error analysis** — the chapter never states that a simulation estimate needs a confidence interval, which is the single most important practical point and which I have added in the notes above; **(b) no MCMC**, so the reader is left with rejection sampling as the only general method for hard targets, with no indication that it collapses in high dimensions; **(c) importance sampling appears only as Problem 10.16**, despite being the one technique here that can handle rare events. **I have flagged all three rather than developing them**, since each needs its own chapter and Ross's *Simulation* (reference [1] at the end of the chapter) is the intended sequel.

#probability #simulation #monte-carlo #inverse-transform #rejection-sampling #box-muller #variance-reduction #antithetic-variables #control-variates
