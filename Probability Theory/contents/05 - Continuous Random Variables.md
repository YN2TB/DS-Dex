---
subject: Probability Theory
chapter: 05
tags: [ds, probability, continuous, density, normal, exponential, uniform]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 5 (pp. 201–248)"
---

# Continuous Random Variables

> [!abstract] What this chapter is for
> **[[04 - Random Variables|Chapter 4]] again, with integrals in place of sums.** Conceptually almost nothing changes:
>
> $$\sum_x g(x)\,p(x) \qquad\longrightarrow\qquad \int_{-\infty}^{\infty} g(x)\,f(x)\,dx$$
>
> **But two things are genuinely new.** First, $P\{X=a\}=0$ for every $a$ — **a density is not a probability**, and this trips up almost everyone once. Second, this is where the **normal distribution** arrives, and with it the reason a single bell-shaped curve dominates all of statistics.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **Density functions** | $f(a)$ measures *likelihood near $a$*, not probability *at* $a$ |
> | **2** | Expectation and variance | Same definitions, integrals instead of sums |
> | **3** | **Uniform** | And **Bertrand's paradox** — "at random" needs defining |
> | **4** | **Normal** | Standardisation, $\Phi$, and the **normal approximation to the binomial** |
> | **5** | **Exponential** | **Memorylessness** — and it is the *only* such distribution |
> | **6–7** | Gamma, Weibull, Cauchy, Beta, Pareto; functions of $X$ | |

---

## 📘 Main Knowledge

### 1. Density functions

> [!important] Definition
> $X$ is a **continuous random variable** if there exists a non-negative function $f$, the **probability density function**, such that for every set $B$
> $$P\{X\in B\}=\int_B f(x)\,dx$$
> In particular
> $$\boxed{\int_{-\infty}^{\infty}f(x)\,dx=1} \qquad\qquad P\{a\le X\le b\}=\int_a^bf(x)\,dx$$

> [!warning] The consequence that catches everyone
> $$P\{X=a\}=\int_a^af(x)\,dx=\boxed{0}$$
> **Every individual value has probability zero.** Therefore
> $$P\{X<a\}=P\{X\le a\}$$
> — **strict and non-strict inequalities are interchangeable**, which is never true in the discrete case.
>
> **"Probability zero" does not mean "impossible."** $X$ certainly takes *some* value; each particular one just has no mass.

> [!important] What a density actually means
> $$P\left\{a-\tfrac{\varepsilon}{2}\le X\le a+\tfrac{\varepsilon}{2}\right\}=\int_{a-\varepsilon/2}^{a+\varepsilon/2}f(x)\,dx\approx\varepsilon f(a)$$
> **for small $\varepsilon$ and $f$ continuous at $a$.**
>
> > **$f(a)$ is a measure of how likely $X$ is to be *near* $a$ — a probability *per unit length*, not a probability.**
>
> **Hence $f(a)$ may exceed 1** without contradiction. *(A uniform on $(0,\tfrac1{10})$ has $f\equiv10$.)*

**The relation to the cdf:**

$$F(a)=\int_{-\infty}^{a}f(x)\,dx \qquad\Longrightarrow\qquad \boxed{\frac{d}{da}F(a)=f(a)}$$

**The density is the derivative of the distribution function** — the continuous analogue of "the pmf is the jump in $F$."

| Example | Setup | Answers |
|---|---|---|
| **1a** | $f(x)=C(4x-2x^2)$ on $(0,2)$ | $\displaystyle C\int_0^2(4x-2x^2)dx=1\Rightarrow C=\mathbf{\tfrac38}$; $P\{X>1\}=\mathbf{\tfrac12}$ |
| **1b** | $f(x)=\lambda e^{-x/100}$, $x\ge0$ | $\lambda=\mathbf{\tfrac1{100}}$; $P\{50<X<150\}=e^{-1/2}-e^{-3/2}\approx\mathbf{.383}$; $P\{X<100\}=1-e^{-1}\approx\mathbf{.632}$ |
| **1c** | Radio tube, $f(x)=100/x^2$ for $x>100$ | $P(\text{fails by }150)=100\int_{100}^{150}x^{-2}dx=\mathbf{\tfrac13}$; then $\binom52(\tfrac13)^2(\tfrac23)^3=\mathbf{\tfrac{80}{243}}$ |

> [!tip] Example 1c shows the two chapters working together
> **The lifetime is continuous; the count of failures is discrete.** Compute a probability from the density, then feed it into a **binomial** ([[04 - Random Variables|ch. 04 §5]]). **Most applied problems have exactly this shape.**

> [!example] Example 1d — density of $Y=2X$, two ways
> **Method 1 (via the cdf — always works):**
> $$F_Y(a)=P\{2X\le a\}=P\{X\le a/2\}=F_X(a/2) \quad\Longrightarrow\quad f_Y(a)=\tfrac12f_X(a/2)$$
>
> **Method 2 (via the $\varepsilon$-interpretation):**
> $$\varepsilon f_Y(a)\approx P\left\{a-\tfrac\varepsilon2\le2X\le a+\tfrac\varepsilon2\right\}=P\left\{\tfrac a2-\tfrac\varepsilon4\le X\le\tfrac a2+\tfrac\varepsilon4\right\}\approx\tfrac\varepsilon2f_X(a/2)$$
>
> **The $\tfrac12$ is the Jacobian**, and Method 2 explains where it comes from: **stretching by 2 spreads the same probability over twice the length, so the density halves.** *(The general rule is §6.)*

---

### 2. Expectation and variance

> [!important] Definitions — identical to [[04 - Random Variables|ch. 04]] with $\int$ for $\sum$
> $$\boxed{\mathbb{E}[X]=\int_{-\infty}^{\infty}x f(x)\,dx}$$
>
> **Proposition 2.1** (law of the unconscious statistician):
> $$\boxed{\mathbb{E}[g(X)]=\int_{-\infty}^{\infty}g(x)f(x)\,dx}$$
>
> **Corollary 2.1:** $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$
>
> $$\mathrm{Var}(X)=\mathbb{E}[(X-\mu)^2]=\mathbb{E}[X^2]-(\mathbb{E}[X])^2, \qquad \mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$$

> [!note] Ross is explicit that nothing conceptual changes
> *"The proof of Corollary 2.1 for a continuous random variable $X$ is the same as the one given for a discrete random variable. **The only modification is that the sum is replaced by an integral and the probability mass function by a probability density function.**"*
>
> **Every warning from [[04 - Random Variables|ch. 04]] transfers unchanged:** $\mathbb{E}[g(X)]\ne g(\mathbb{E}[X])$ unless $g$ is linear.

> [!example] Example 2c — the stick and the point $p$
> A stick of length 1 is broken at $U\sim$ Uniform$(0,1)$. **Which piece contains a fixed point $p$, and how long is it on average?**
>
> $$L_p(U)=\begin{cases}1-U & U<p\\ U & U>p\end{cases}$$
> $$\mathbb{E}[L_p(U)]=\int_0^p(1-u)\,du+\int_p^1u\,du=\boxed{\tfrac12+p(1-p)}$$
>
> > **The expected length always exceeds $\tfrac12$**, and is **maximised at $p=\tfrac12$**, where it equals $\tfrac34$.
> >
> > **This is a size-biasing effect again** ([[04 - Random Variables|ch. 04]]'s bus problem): **a fixed point is more likely to land in the longer piece**, so conditioning on containing $p$ favours long pieces.

> [!example] Example 2d — when to leave for an appointment
> Cost $c$ per minute early, $k$ per minute late; travel time has density $f$ and cdf $F$. Leaving $t$ minutes before:
> $$\frac{d}{dt}\mathbb{E}[C_t(X)]=(k+c)F(t)-k=0 \quad\Longrightarrow\quad \boxed{F(t^*)=\frac{k}{k+c}}$$
>
> > **Leave at the $\dfrac{k}{k+c}$ quantile of travel time.** If being late is 4× as costly as being early ($k=4c$), leave at the **80th percentile**.
> >
> > **This is exactly [[04 - Random Variables|ch. 04]]'s newsvendor solution** $\sum_{i\le s}p(i)<\tfrac{b}{b+\ell}$, and it is the **quantile-regression / pinball loss** of [[Machine Learning/contents/00-Index|Machine Learning]]. **Asymmetric costs ⟹ optimise a quantile, not a mean.**

---

### 3. The uniform random variable

> [!important] Uniform$(\alpha,\beta)$
> $$f(x)=\frac1{\beta-\alpha} \text{ on } (\alpha,\beta), \qquad F(a)=\frac{a-\alpha}{\beta-\alpha} \text{ on } (\alpha,\beta)$$
> $$\boxed{\mathbb{E}[X]=\frac{\alpha+\beta}{2} \qquad\qquad \mathrm{Var}(X)=\frac{(\beta-\alpha)^2}{12}}$$
>
> **The mean is the midpoint; the variance is the squared length over 12.** And for any subinterval,
> $$P\{a\le X\le b\}=b-a \quad\text{(on the unit interval)}$$
> — **probability equals length.**

| Example | Question | Answer |
|---|---|---|
| **3b** | $X\sim U(0,10)$: $P\{X<3\}$, $P\{X>6\}$, $P\{3<X<8\}$ | $\mathbf{.3}$, $\mathbf{.4}$, $\mathbf{.5}$ |
| **3c** | Buses every 15 min; arrive $U(0,30)$ past 7am. $P(\text{wait}<5)$; $P(\text{wait}>10)$ | Both $\mathbf{\tfrac13}$ |

#### 3a. Bertrand's paradox — "at random" is not self-explanatory

> [!example] Example 3d
> **Draw a "random chord" of a circle. What is $P(\text{chord longer than the inscribed equilateral triangle's side})$?**
>
> *"As stated, the problem is incapable of solution because it is not clear what is meant by a random chord."*
>
> | Formulation | Construction | Answer |
> |---|---|---|
> | **1** | Distance $D$ from centre is $U(0,r)$; chord is long iff $D<r/2$ | $\dfrac{r/2}{r}=\mathbf{\tfrac12}$ |
> | **2** | Angle $\theta$ with a tangent at one endpoint is $U(0°,180°)$; chord is long iff $60°<\theta<120°$ | $\dfrac{120-60}{180}=\mathbf{\tfrac13}$ |
>
> > [!important] Both are correct — and both are physically realisable
> > **Ross's point is not that one is wrong.** *"Random experiments could be performed in such a way that $\tfrac12$ or $\tfrac13$ would be the correct probability."*
> > - **Throw a disc of radius $r$ onto a table ruled with lines $2r$ apart** — the crossing line gives a uniform distance ⟹ $\tfrac12$
> > - **Spin a needle freely about a point on the circle's edge** — uniform angle ⟹ $\tfrac13$
> >
> > **"Choose at random" is meaningless until the *mechanism* is specified.** Exactly the lesson of [[03 - Conditional Probability and Independence|ch. 03]]'s Example 3m (the two-child problem) and [[04 - Random Variables|ch. 04]]'s Example 6e (the jury): **when a problem feels ambiguous, the missing ingredient is usually the sampling mechanism.**
> >
> > *(This matters in practice: "a random point in a high-dimensional region" and "a random rotation" both admit several inequivalent definitions.)*

---

### 4. Normal random variables

> [!important] Normal$(\mu,\sigma^2)$
> $$\boxed{f(x)=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-(x-\mu)^2/2\sigma^2}, \qquad -\infty<x<\infty}$$
> **A bell-shaped curve symmetric about $\mu$**, with $\mathbb{E}[X]=\mu$ and $\mathrm{Var}(X)=\sigma^2$.

> [!important] Standardisation — the only technique you need
> If $X\sim N(\mu,\sigma^2)$ then
> $$\boxed{Z=\frac{X-\mu}{\sigma}\sim N(0,1)}$$
> and writing $\Phi$ for the standard normal cdf,
> $$P\{X\le a\}=\Phi\!\left(\frac{a-\mu}{\sigma}\right)$$
>
> **By symmetry:** $\boxed{\Phi(-x)=1-\Phi(x)}$ — which is why tables list only $x>0$.

> [!example] Example 4b — $X\sim N(3,9)$, so $\sigma=3$
> **(a)** $P\{2<X<5\}=\Phi(\tfrac23)-\Phi(-\tfrac13)=\Phi(\tfrac23)-[1-\Phi(\tfrac13)]\approx\mathbf{.3779}$
> **(b)** $P\{X>0\}=P\{Z>-1\}=\Phi(1)\approx\mathbf{.8413}$
> **(c)** $P\{|X-3|>6\}=2[1-\Phi(2)]\approx\mathbf{.0456}$
>
> **Note (b): $1-\Phi(-1)=\Phi(1)$ uses the symmetry rule**, and (c) uses it to fold two tails into one.

> [!example] Example 4c — grading "on the curve", and the numbers to memorise
> Grades assigned by standard deviations from the mean:
>
> | Grade | Range | Probability |
> |---|---|---|
> | A | $>\mu+\sigma$ | $1-\Phi(1)\approx\mathbf{.1587}$ |
> | B | $\mu$ to $\mu+\sigma$ | $\Phi(1)-\Phi(0)\approx\mathbf{.3413}$ |
> | C | $\mu-\sigma$ to $\mu$ | $\approx\mathbf{.3413}$ |
> | D | $\mu-2\sigma$ to $\mu-\sigma$ | $\Phi(2)-\Phi(1)\approx\mathbf{.1359}$ |
> | F | $<\mu-2\sigma$ | $\Phi(-2)\approx\mathbf{.0228}$ |
>
> **So roughly 16% A, 34% B, 34% C, 14% D, 2% F.**
>
> > **These are the numbers behind the "68–95–99.7 rule":**
> > $$P\{|Z|<1\}\approx\mathbf{.683} \qquad P\{|Z|<2\}\approx\mathbf{.954} \qquad P\{|Z|<3\}\approx\mathbf{.997}$$
> > **Worth memorising** — they let you sanity-check any normal calculation in your head.

| Example | Setup | Answer |
|---|---|---|
| **4d** | Gestation $N(270,100)$; defendant absent 240–290 days before birth | $[1-\Phi(2)]+[1-\Phi(3)]\approx\mathbf{.0241}$ |
| **4e** | Send $\pm2$, standard normal noise, threshold $.5$ | $P(\text{err}\mid1)=1-\Phi(1.5)\approx\mathbf{.0668}$; $P(\text{err}\mid0)=1-\Phi(2.5)\approx\mathbf{.0062}$ |

> [!example] Example 4f — Value at Risk
> **VaR is the value $v$ such that the loss exceeds $v$ with probability only 1%.** For gain $X\sim N(\mu,\sigma^2)$,
> $$.01=P\{-X>v\}=1-\Phi\!\left(\frac{v+\mu}{\sigma}\right) \quad\Longrightarrow\quad \boxed{\mathrm{VaR}=2.33\sigma-\mu}$$
> using $\Phi(2.33)\approx.99$.
>
> > **Among normally-distributed investments, the safest by VaR is the one maximising $\mu-2.33\sigma$** — **a mean–variance trade-off with an explicit exchange rate.**
> >
> > **The caveat every finance course eventually delivers:** this depends entirely on normality, and **real asset returns have far heavier tails**, so normal-based VaR systematically understates extreme losses. *(The Cauchy of §6 is the standard cautionary example.)*

#### 4a. The normal approximation to the binomial

> [!important] The DeMoivre–Laplace limit theorem
> If $S_n$ counts successes in $n$ independent trials with success probability $p$, then for $a<b$
> $$P\left\{a\le\frac{S_n-np}{\sqrt{np(1-p)}}\le b\right\}\ \longrightarrow\ \Phi(b)-\Phi(a) \qquad\text{as } n\to\infty$$
>
> **Standardise the binomial by its own mean and standard deviation, and it becomes standard normal.** *(Proved by DeMoivre in 1733 for $p=\tfrac12$, extended by Laplace in 1812; it is a special case of the CLT, [[08 - Limit Theorems|ch. 08]].)*

> [!important] The continuity correction
> **The binomial is integer-valued; the normal is continuous.** So write
> $$P\{X=i\}=P\{i-\tfrac12<X<i+\tfrac12\}$$
> before approximating. **Similarly $P\{X\ge i\}\to P\{X>i-\tfrac12\}$.**
>
> **It is not optional decoration — it substantially improves accuracy** (see Exercise 4).

> [!important] Which approximation, when?
> | Regime | Use | Condition |
> |---|---|---|
> | $n$ large, $p$ **small** | **Poisson**$(np)$ | $np$ moderate |
> | $n$ large, $p$ **moderate** | **Normal** | $np(1-p)\ge\mathbf{10}$ |
>
> **The governing quantity for the normal is the *variance*, not $n$.** With $p=.001$ you would need $n\approx10{,}000$ before $np(1-p)\ge10$ — which is precisely where the Poisson works instead.

| Example | Setup | Result |
|---|---|---|
| **4g** | 40 fair flips; $P\{X=20\}$ | Normal with correction $\approx\mathbf{.1272}$; exact $\mathbf{.1254}$ |
| **4h** | 450 admitted, each attends w.p. $.3$; $P\{>150\text{ attend}\}$ | $1-\Phi(1.59)\approx\mathbf{.0559}$ |
| **4i** | 100 dieters, no real effect; $P\{\ge65\text{ improve}\}$ | $1-\Phi(2.9)\approx\mathbf{.0019}$ |

> [!important] Example 4i is a hypothesis test in disguise
> **"What is the probability the nutritionist endorses a useless diet?"** Under the null ($p=\tfrac12$), the chance of seeing $\ge65$ improvements out of 100 is $\approx\mathbf{.0019}$.
>
> **That is a $p$-value**, and $.0019$ is exactly the kind of number that leads to rejecting a null hypothesis. **The entire logic of significance testing is present here, three chapters before [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] names it.**

> [!example] Example 4j — how large a sample?
> 52% of NYC residents favour a ban. **$P(\text{a sample majority favours it})$?**
>
> **First, a modelling step worth noticing.** A random sample without replacement makes $S_n$ **hypergeometric** — but $N$ and $.52N$ are huge relative to $n$, so the **binomial approximation to the hypergeometric** applies ([[04 - Random Variables|ch. 04 §7]]), and then the normal approximation to *that*:
> $$P\{S_n>.5n\}\approx\Phi(.04\sqrt n)$$
>
> | $n$ | $.04\sqrt n$ | Probability |
> |---|---|---|
> | 11 | $.1327$ | $\mathbf{.553}$ |
> | 101 | $.4020$ | $\mathbf{.656}$ |
> | 1001 | $1.2655$ | $\mathbf{.897}$ |
>
> **For probability $\ge.95$ we need $.04\sqrt n>1.645$, i.e. $n\ge1691.3$ — so $n=\mathbf{1692}$.**
>
> > **A 52–48 split needs about 1700 people to be detected reliably.** **The $\sqrt n$ is the whole story: halving the margin of error quadruples the required sample.** *This is why political polls are the size they are.*

---

### 5. Exponential random variables

> [!important] Exponential$(\lambda)$
> $$f(x)=\lambda e^{-\lambda x}\ (x\ge0), \qquad\qquad F(a)=1-e^{-\lambda a}, \qquad\qquad P\{X>a\}=e^{-\lambda a}$$
> $$\boxed{\mathbb{E}[X]=\frac1\lambda \qquad\qquad \mathrm{Var}(X)=\frac1{\lambda^2}}$$

**Ross derives the moments from a neat recursion.** Integrating by parts gives $\mathbb{E}[X^n]=\tfrac n\lambda\mathbb{E}[X^{n-1}]$, so $\mathbb{E}[X]=\tfrac1\lambda$ and $\mathbb{E}[X^2]=\tfrac2{\lambda^2}$, hence $\mathrm{Var}=\tfrac2{\lambda^2}-\tfrac1{\lambda^2}=\tfrac1{\lambda^2}$.

> [!note] Note $\mathrm{SD}=\mathbb{E}$
> **The exponential's standard deviation equals its mean** — it is a highly variable, strongly right-skewed distribution. *(Compare the geometric of [[04 - Random Variables|ch. 04 §7]], its discrete analogue, where $\mathrm{SD}\approx\mathbb{E}$ for small $p$.)*

**It arises as a waiting time:** *"the amount of time until an earthquake occurs, or until a new war breaks out, or until a telephone call you receive turns out to be a wrong number."* **The theoretical reason is the Poisson process** ([[09 - Additional Topics in Probability|ch. 09 §1]]).

> [!example] Example 5b — phone booth
> Call length exponential with $\lambda=\tfrac1{10}$ (mean 10 minutes).
> $$P\{X>10\}=e^{-1}\approx\mathbf{.368} \qquad P\{10<X<20\}=e^{-1}-e^{-2}\approx\mathbf{.233}$$

#### 5a. Memorylessness — the defining property

> [!important] Memorylessness
> $X$ is **memoryless** if
> $$\boxed{P\{X>s+t\mid X>t\}=P\{X>s\} \qquad\text{for all } s,t\ge0}$$
>
> **In words: given that it has already survived $t$, the remaining lifetime has the *original* distribution.** *"It is as if the instrument does not remember that it has already been in use."*
>
> Equivalently: $P\{X>s+t\}=P\{X>s\}P\{X>t\}$, **which $e^{-\lambda(s+t)}=e^{-\lambda s}e^{-\lambda t}$ satisfies immediately.**

> [!important] The exponential is the *only* memoryless distribution
> Setting $\bar F(x)=P\{X>x\}$, memorylessness is the functional equation
> $$g(s+t)=g(s)g(t)$$
> **whose only right-continuous solution is $g(x)=e^{-\lambda x}$.** Since every survival function is right-continuous, **$X$ must be exponential.** $\blacksquare$
>
> *(Ross's footnote proves it: $g(m/n)=g(1)^{m/n}$ by iterating the equation, then right-continuity extends this to all real $x$.)*
>
> **This uniqueness is what makes the exponential special.** Any modelling assumption of "constant risk, no ageing" forces the exponential — there is no choice in the matter.

> [!example] Example 5c — Mr Smith at the post office
> Two clerks, both busy (Jones and Brown); Smith waits. **$P(\text{Smith leaves last})$?**
>
> **When Smith reaches a clerk, one of the other two has just left and the other is still being served.** By memorylessness, **that other person's remaining service time is exponential($\lambda$) — exactly as if it were just starting.** So Smith and that person are in a symmetric race:
> $$P(\text{Smith last})=\boxed{\tfrac12}$$
>
> > **A calculation that would otherwise require integrating over the elapsed service time collapses to a symmetry argument.** *That is what memorylessness buys.*

> [!example] Example 5d — the battery, and what happens without memorylessness
> Battery life exponential, mean 10,000 miles. **$P(\text{completes a 5000-mile trip})$?**
> $$P\{\text{remaining}>5\}=e^{-1/2}\approx\mathbf{.607}$$
> **regardless of how many miles the battery has already done.**
>
> > **But if the distribution is not exponential**, the answer is
> > $$P\{\text{life}>t+5\mid\text{life}>t\}=\frac{1-F(t+5)}{1-F(t)}$$
> > **and you need to know $t$.** *"Additional information is needed before the desired probability can be calculated."*
> >
> > **Memorylessness is exactly the assumption that lets you ignore the past — and it is a strong, testable assumption.** Real batteries wear out; **assuming exponential lifetimes for anything that ages will systematically over-predict survival.**

> [!note] The hazard rate (§5.5.1) says the same thing
> $$\lambda(t)=\frac{f(t)}{1-F(t)}$$
> — the **instantaneous failure rate given survival to $t$.** **For the exponential, $\lambda(t)=\lambda$: constant.** *(Increasing hazard = wearing out; decreasing = "burning in". The **Weibull** of §6 is the standard flexible-hazard family.)*

> [!note] The Laplace (double exponential) distribution
> $f(x)=\tfrac\lambda2e^{-\lambda|x|}$ — **symmetric, with exponential tails.**
>
> **Example 5e re-runs the noisy-channel Example 4e with Laplace noise instead of normal:**
>
> | Error | Normal noise | Laplace noise |
> |---|---|---|
> | Message 1 read as 0 | $\mathbf{.0668}$ | $\tfrac12e^{-1.5}\approx\mathbf{.1116}$ |
> | Message 0 read as 1 | $\mathbf{.0062}$ | $\tfrac12e^{-2.5}\approx\mathbf{.0410}$ |
>
> **The Laplace error probabilities are several times larger** — **because its tails are heavier.** *The same decision rule, the same signal strength, and a materially worse system, purely because of the noise distribution's shape.*

---

### 6. Other distributions, and functions of a random variable

> [!important] The families worth knowing
> | Distribution | Density | Notes |
> |---|---|---|
> | **Gamma$(\alpha,\lambda)$** | $\dfrac{\lambda e^{-\lambda x}(\lambda x)^{\alpha-1}}{\Gamma(\alpha)}$ | $\mathbb{E}=\tfrac\alpha\lambda$, $\mathrm{Var}=\tfrac\alpha{\lambda^2}$; **sum of $\alpha$ iid exponentials** when $\alpha$ is an integer |
> | **Weibull** | — | Flexible **hazard rate**; the standard reliability model |
> | **Cauchy** | $\dfrac{1}{\pi[1+(x-\theta)^2]}$ | **No mean and no variance** — the integral diverges |
> | **Beta$(a,b)$** | $\dfrac{x^{a-1}(1-x)^{b-1}}{B(a,b)}$ | Supported on $(0,1)$; $\mathbb{E}=\tfrac a{a+b}$; models proportions |
> | **Pareto** | — | Heavy-tailed; incomes, city sizes, file sizes |

> [!warning] The Cauchy is not a curiosity
> **It has no expectation** — $\int|x|f(x)dx=\infty$. **Consequently the law of large numbers fails for it:** the sample mean of $n$ Cauchy variables is *itself* Cauchy, no matter how large $n$ is. **Averaging buys nothing.**
>
> **It is the standard counterexample to "surely averages always stabilise"** ([[08 - Limit Theorems|ch. 08]]), and heavy-tailed data in practice — financial returns, network traffic, city sizes — behaves uncomfortably like it.

> [!important] §7 — the distribution of $g(X)$
> **The reliable method is always via the cdf**, as in Example 1d:
> $$F_Y(y)=P\{g(X)\le y\}$$
> **then differentiate.** When $g$ is strictly monotone with inverse $g^{-1}$,
> $$\boxed{f_Y(y)=f_X\big(g^{-1}(y)\big)\left|\frac{d}{dy}g^{-1}(y)\right|}$$
>
> **The derivative factor is the Jacobian — and forgetting it is the single most common error in this material.** *(Example 1d's $\tfrac12$ was exactly this.)*

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — Densities from first principles**

Let $f(x)=cx^2$ for $0<x<3$ and 0 otherwise.

**(i)** Find $c$.

**(ii)** Find $F(x)$, and evaluate $F(1)$ and $P\{X>2\}$.

**(iii)** Find $\mathbb{E}[X]$, $\mathbb{E}[X^2]$ and $\mathrm{Var}(X)$.

**(iv)** Find the median and compare with the mean. What does the comparison tell you about the shape?

**(v)** A student writes *"$f(2)=4/9\approx.44$, so $P\{X=2\}\approx.44$."* **State two things wrong with this.**

> [!example]- Solution
> **(i)** $$\int_0^3cx^2\,dx=c\left[\frac{x^3}3\right]_0^3=9c=1 \quad\Longrightarrow\quad c=\mathbf{\tfrac19}$$
>
> ---
> **(ii)** $$F(x)=\int_0^x\tfrac19t^2\,dt=\boxed{\frac{x^3}{27}} \quad (0<x<3)$$
> $$F(1)=\mathbf{\tfrac1{27}}\approx.037 \qquad P\{X>2\}=1-F(2)=1-\tfrac8{27}=\mathbf{\tfrac{19}{27}}\approx.704$$
>
> ---
> **(iii)** $$\mathbb{E}[X]=\int_0^3\tfrac19x^3\,dx=\tfrac19\cdot\tfrac{81}4=\mathbf{\tfrac94}=2.25$$
> $$\mathbb{E}[X^2]=\int_0^3\tfrac19x^4\,dx=\tfrac19\cdot\tfrac{243}5=\mathbf{\tfrac{27}5}=5.4$$
> $$\mathrm{Var}(X)=\tfrac{27}5-\left(\tfrac94\right)^2=\tfrac{27}5-\tfrac{81}{16}=\mathbf{\tfrac{27}{80}}=0.3375$$
>
> ---
> **(iv)** Set $F(m)=\tfrac12$: $\dfrac{m^3}{27}=\tfrac12$, so $m=(13.5)^{1/3}\approx\mathbf{2.381}$.
>
> **The median ($2.381$) exceeds the mean ($2.25$)** — the distribution is **left-skewed**, which matches the density: $f(x)=x^2/9$ **rises steeply toward $x=3$**, piling mass at the right and leaving a thin tail on the left.
>
> > **Rule of thumb: mean $<$ median indicates a left tail; mean $>$ median a right tail.** *(The exponential of Exercise 5 is the opposite case.)*
>
> ---
> **(v)** **Two independent errors:**
>
> **1. $P\{X=2\}=\mathbf{0}$**, as it is for every single point of a continuous distribution. **The density is not a probability.**
>
> **2. Even as an approximation, the units are wrong.** $f(2)$ is a probability **per unit length**: the correct statement is
> $$P\{2-\tfrac\varepsilon2<X<2+\tfrac\varepsilon2\}\approx\varepsilon f(2)=\varepsilon\cdot\tfrac49$$
> **You must multiply by an interval width.**
>
> > **A quick test that the reasoning is wrong: densities can exceed 1.** Here $f(x)=x^2/9$ reaches $f(3)=1$; **rescale the support to $(0,1)$ and it would reach 3.** *"A number greater than 1" cannot be a probability, so it cannot be one at any other value either.*

---

**Exercise 2 — Expectation of a function**

Let $U\sim$ Uniform$(0,1)$.

**(i)** Find $\mathbb{E}[U]$, $\mathbb{E}[U^2]$ and $\mathrm{Var}(U)$.

**(ii)** Find $\mathbb{E}[e^U]$ and compare with $e^{\mathbb{E}[U]}$.

**(iii)** Find $\mathbb{E}\!\left[\dfrac1{1+U}\right]$ and compare with $\dfrac1{\mathbb{E}[1+U]}$.

**(iv)** State the general inequality that explains (ii) and (iii), and give the condition for equality.

**(v)** In Example 2d, a commuter faces $c=1$ (per minute early) and $k=4$ (per minute late). If travel time is Uniform$(20,50)$ minutes, **how early should they leave?**

> [!example]- Solution
> **(i)** $$\mathbb{E}[U]=\tfrac{0+1}2=\mathbf{\tfrac12} \qquad \mathbb{E}[U^2]=\int_0^1u^2du=\mathbf{\tfrac13} \qquad \mathrm{Var}(U)=\tfrac13-\tfrac14=\mathbf{\tfrac1{12}}\approx.0833$$
> *(Consistent with $(\beta-\alpha)^2/12=1/12$ ✓)*
>
> ---
> **(ii)** $$\mathbb{E}[e^U]=\int_0^1e^u\,du=e-1\approx\mathbf{1.7183} \qquad\text{versus}\qquad e^{1/2}\approx\mathbf{1.6487}$$
> **$\mathbb{E}[e^U]>e^{\mathbb{E}[U]}$.**
>
> ---
> **(iii)** $$\mathbb{E}\!\left[\frac1{1+U}\right]=\int_0^1\frac{du}{1+u}=\ln2\approx\mathbf{.6931} \qquad\text{versus}\qquad \frac1{1.5}=\mathbf{.6667}$$
> **Again the expectation of the function exceeds the function of the expectation.**
>
> ---
> **(iv)** **Jensen's inequality.** For a **convex** $g$,
> $$\boxed{\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])}$$
> with the inequality reversed for concave $g$. **Both $e^x$ and $\tfrac1{1+x}$ are convex on the relevant range**, which explains both results.
>
> **Equality holds iff $g$ is linear on the support of $X$, or $X$ is degenerate (constant).**
>
> > **This is Corollary 2.1 seen from the other side:** $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$ is precisely the equality case. **Everything else is an inequality**, and it always leans the same way for a given curvature.
> >
> > **Practical corollary worth carrying:** if you model in logs and report in levels, $\mathbb{E}[e^Y]\ne e^{\mathbb{E}[Y]}$ — **exponentiating a fitted log-mean systematically *understates* the mean.** *(The standard smearing correction in [[Econometrics/contents/00-Index|Econometrics]] exists for exactly this reason.)*
>
> ---
> **(v)** By Example 2d, leave at $t^*$ with $F(t^*)=\dfrac{k}{k+c}=\dfrac{4}{5}=0.8$.
>
> For Uniform$(20,50)$: $F(t)=\dfrac{t-20}{30}=0.8$ gives
> $$t^*=20+0.8(30)=\mathbf{44\text{ minutes}}$$
>
> > **Leave 44 minutes ahead, even though the average trip takes 35.** **The asymmetry in costs ($4:1$) pushes you to the 80th percentile of travel time, not the mean.**
> >
> > **Notice the mean is irrelevant to the answer** — only the quantile matters. *This is the defining feature of asymmetric loss.*

---

**Exercise 3 — The normal distribution**

IQ scores are modelled as $N(100,15^2)$.

**(i)** Find $P\{85<X<115\}$, $P\{70<X<130\}$ and $P\{55<X<145\}$. Relate to a well-known rule.

**(ii)** Find $P\{X>130\}$ and express it as "1 in $k$".

**(iii)** Find the cutoff for the top 5% and the top 1%.

**(iv)** Someone claims a score of 145 "is only 3 standard deviations out, so it's not that unusual." **Respond quantitatively.**

**(v)** For $X\sim N(\mu,\sigma^2)$, show that $P\{|X-\mu|>k\sigma\}$ does not depend on $\mu$ or $\sigma$, and explain why this makes a single table sufficient.

> [!example]- Solution
> **(i)** The bounds are exactly $\mu\pm1\sigma$, $\mu\pm2\sigma$, $\mu\pm3\sigma$:
>
> | Range | $z$ | Probability |
> |---|---|---|
> | $85$–$115$ | $\pm1$ | $\mathbf{.6827}$ |
> | $70$–$130$ | $\pm2$ | $\mathbf{.9545}$ |
> | $55$–$145$ | $\pm3$ | $\mathbf{.9973}$ |
>
> **This is the 68–95–99.7 rule.**
>
> ---
> **(ii)** $$P\{X>130\}=1-\Phi(2)=\mathbf{.02275}$$
> $$\frac1{.02275}\approx44 \quad\Longrightarrow\quad \textbf{about 1 person in 44}$$
>
> ---
> **(iii)** $$\text{Top 5\%}: \mu+1.645\sigma=100+24.67=\mathbf{124.7}$$
> $$\text{Top 1\%}: \mu+2.326\sigma=100+34.90=\mathbf{134.9}$$
>
> ---
> **(iv)** **The claim confuses a small-sounding $z$ with a small probability.**
> $$P\{X>145\}=1-\Phi(3)=\mathbf{.00135} \quad\Longrightarrow\quad \textbf{about 1 in 741}$$
>
> **And the tail falls off far faster than linearly:**
>
> | $z$ | $P\{X>\mu+z\sigma\}$ | 1 in… |
> |---|---|---|
> | 2 | $.02275$ | 44 |
> | 3 | $.00135$ | 741 |
> | 4 | $.0000317$ | 31,600 |
> | 5 | $.000000287$ | 3.5 million |
>
> > **Each extra standard deviation costs roughly an order of magnitude or more.** **"Only 3 sigma" is 1 in 741; "only 5 sigma" is 1 in 3.5 million** — which is why particle physics uses $5\sigma$ as its discovery threshold.
> >
> > **The corollary is a warning:** because normal tails vanish so fast, **a model that assumes normality declares genuinely-occurring extreme events to be essentially impossible.** *This is precisely the criticism of normal-based VaR in Example 4f.*
>
> ---
> **(v)** Standardising, $Z=(X-\mu)/\sigma\sim N(0,1)$, so
> $$P\{|X-\mu|>k\sigma\}=P\{|Z|>k\}=2[1-\Phi(k)]$$
> **which involves only $k$.** $\blacksquare$
>
> > **This is why one table suffices for the entire normal family.** **There is really only one normal distribution** — every other member is a shift and rescale of $N(0,1)$, and **shifts and rescalings do not change probabilities expressed in standard-deviation units.**
> >
> > *(Contrast the gamma family, where the shape parameter $\alpha$ genuinely changes the distribution's form and no single table can cover it.)*

---

**Exercise 4 — Normal approximation to the binomial**

A fair coin is flipped $n$ times; $X$ is the number of heads.

**(i)** For $n=100$, compute $P\{X\ge60\}$ **exactly**, then approximate **with** and **without** the continuity correction. Tabulate the errors.

**(ii)** Repeat for $n=20$ and $P\{X\ge15\}$. Comment on the difference.

**(iii)** State the rule of thumb for when the normal approximation is reliable, and check it in both cases.

**(iv)** Reproduce Example 4g's calculation of $P\{X=20\}$ for $n=40$, and comment on the accuracy.

**(v)** When would you use the **Poisson** approximation instead? Give a case where the normal fails badly.

> [!example]- Solution
> **(i)** $n=100$, $p=\tfrac12$: $\mu=50$, $\sigma=5$.
>
> | Method | Computation | Value | Error |
> |---|---|---|---|
> | **Exact** | $\sum_{k=60}^{100}\binom{100}{k}2^{-100}$ | $\mathbf{.028444}$ | — |
> | **Normal + cc** | $1-\Phi\!\left(\frac{59.5-50}{5}\right)=1-\Phi(1.9)$ | $\mathbf{.028717}$ | $2.7\times10^{-4}$ |
> | **Normal, no cc** | $1-\Phi\!\left(\frac{60-50}{5}\right)=1-\Phi(2)$ | $\mathbf{.022750}$ | $5.7\times10^{-3}$ |
>
> > **The continuity correction reduces the error by a factor of 21.** Without it the approximation is off by 20% of the true value.
>
> ---
> **(ii)** $n=20$, $p=\tfrac12$: $\mu=10$, $\sigma=\sqrt5\approx2.236$.
>
> | Method | Value | Error |
> |---|---|---|
> | **Exact** | $\mathbf{.020695}$ | — |
> | **Normal + cc** | $1-\Phi(2.012)=\mathbf{.022086}$ | $1.4\times10^{-3}$ |
> | **Normal, no cc** | $1-\Phi(2.236)=\mathbf{.012674}$ | $8.0\times10^{-3}$ |
>
> **Both are worse than at $n=100$, and the uncorrected version is now off by 39%.**
>
> > **The correction matters *more* when $n$ is small**, because the $\tfrac12$ is a larger fraction of $\sigma$. **At $n=20$, $\tfrac{0.5}{\sigma}=0.22$; at $n=100$, $0.10$.**
>
> ---
> **(iii)** **The rule is $np(1-p)\ge10$.**
>
> | Case | $np(1-p)$ | Verdict |
> |---|---|---|
> | $n=100$ | $\mathbf{25}$ | ✅ comfortably satisfied — error $2.7\times10^{-4}$ |
> | $n=20$ | $\mathbf{5}$ | ❌ fails — error $1.4\times10^{-3}$, five times larger |
>
> **The rule correctly predicts which case is trustworthy.** *(Note it is a condition on the **variance**, not on $n$ alone: $n=1000$ with $p=.001$ gives $np(1-p)\approx1$ and fails badly.)*
>
> ---
> **(iv)** $n=40$, $p=\tfrac12$: $\mu=20$, $\sigma=\sqrt{10}\approx3.162$.
> $$P\{X=20\}=P\{19.5<X<20.5\}\approx\Phi\!\left(\tfrac{0.5}{\sqrt{10}}\right)-\Phi\!\left(-\tfrac{0.5}{\sqrt{10}}\right)=\Phi(.1581)-\Phi(-.1581)=\mathbf{.1256}$$
> **Exact:** $\binom{40}{20}2^{-40}=\mathbf{.12537}$. **Error $2.6\times10^{-4}$ — excellent.**
>
> > **Note a rounding detail in the source.** Ross rounds $\tfrac{0.5}{\sqrt{10}}=.1581$ to $.16$, giving $\Phi(.16)-\Phi(-.16)=.1272$ against the exact $.1254$.
> >
> > **Using the unrounded value gives $.1256$ — noticeably closer to the truth than the printed $.1272$.** **The approximation is better than the text's arithmetic suggests**; the discrepancy is a table-rounding artefact, not a failure of the method. *(Also note $np(1-p)=10$ here — exactly at the threshold.)*
> >
> > **Without the continuity correction the answer would be $P\{X=20\}\approx0$**, since a continuous distribution assigns zero probability to a point. **For point probabilities the correction is not an improvement — it is the entire calculation.**
>
> ---
> **(v)** **Use the Poisson when $p$ is small and $np$ is moderate** — i.e. when $np(1-p)$ is **too small** for the normal.
>
> **A case where the normal fails badly:** $n=1000$, $p=.001$, so $\mu=1$ and $np(1-p)\approx0.999$.
> - **Poisson$(1)$:** $P\{X=0\}=e^{-1}=\mathbf{.3679}$ — and the exact binomial is $(.999)^{1000}=.3677$ ✓
> - **Normal:** $\sigma\approx1$, so $P\{X=0\}\approx\Phi(0.5)-\Phi(-0.5)=.383$ — and worse, **the normal puts appreciable probability on $X<0$**, which is impossible.
>
> > **The distinction is about *shape*.** With $np(1-p)$ small the binomial is **strongly right-skewed** and bounded below at 0; **the symmetric normal cannot represent that.** The Poisson, itself skewed and supported on $\{0,1,2,\dots\}$, can.
> >
> > **Summary rule:** $p$ small $\to$ **Poisson**; $np(1-p)\ge10$ $\to$ **normal**; both conditions met $\to$ either works.

---

**Exercise 5 — The exponential and memorylessness**

A machine's lifetime is exponential with mean 8 years.

**(i)** Find $\lambda$, $\mathrm{Var}$, and $P\{X>8\}$.

**(ii)** Find $P\{X>12\mid X>4\}$ two ways, and state the property being used.

**(iii)** Find the median and compare with the mean. Find $P\{X<\mathbb{E}[X]\}$.

**(iv)** Three such machines run independently. **Find the expected time until the first failure.**

**(v)** A manager argues: *"This machine has run 6 years already, so it's due to fail — I'll replace it now."* **Evaluate this argument**, and say under what circumstances it *would* be correct.

> [!example]- Solution
> **(i)** $\mathbb{E}[X]=\tfrac1\lambda=8$, so $\lambda=\mathbf{\tfrac18}$.
> $$\mathrm{Var}(X)=\frac1{\lambda^2}=\mathbf{64} \quad(\mathrm{SD}=8) \qquad P\{X>8\}=e^{-8/8}=e^{-1}\approx\mathbf{.368}$$
>
> > **$\mathrm{SD}=\mathbb{E}=8$** — and note that **only 37% of machines survive to the mean lifetime.**
>
> ---
> **(ii)** **By memorylessness, directly:**
> $$P\{X>12\mid X>4\}=P\{X>8\}=e^{-1}\approx\mathbf{.368}$$
>
> **By the definition of conditional probability:**
> $$\frac{P\{X>12\}}{P\{X>4\}}=\frac{e^{-12/8}}{e^{-4/8}}=e^{-1}\approx\mathbf{.368}\ ✓$$
>
> **The property is memorylessness:** $P\{X>s+t\mid X>t\}=P\{X>s\}$, which holds because $e^{-\lambda(s+t)}=e^{-\lambda s}e^{-\lambda t}$.
>
> ---
> **(iii)** Median: $1-e^{-\lambda m}=\tfrac12$ gives
> $$m=\frac{\ln2}{\lambda}=8\ln2\approx\mathbf{5.55\text{ years}}$$
> **against a mean of 8** — **the median is only $69\%$ of the mean.**
> $$P\{X<\mathbb{E}[X]\}=1-e^{-1}\approx\mathbf{.632}$$
>
> > **63% of machines fail before the "average lifetime."** **The exponential is strongly right-skewed: a few very long lifetimes drag the mean above the typical value.**
> >
> > **Reporting the mean of a skewed distribution as "typical" is misleading** — the same reason median income is reported rather than mean income. *(Contrast Exercise 1, where the density leaned the other way and the median exceeded the mean.)*
>
> ---
> **(iv)** Let $T=\min(X_1,X_2,X_3)$. The minimum exceeds $t$ iff **all three** do, so by independence:
> $$P\{T>t\}=\left(e^{-\lambda t}\right)^3=e^{-3\lambda t}$$
> **So $T\sim$ Exponential$(3\lambda)$**, and
> $$\mathbb{E}[T]=\frac1{3\lambda}=\frac83\approx\mathbf{2.67\text{ years}}$$
>
> > **The minimum of independent exponentials is exponential with the rates added.** **Failure rates are what combine, not lifetimes.**
> >
> > **This is why series systems fail so fast** ([[03 - Conditional Probability and Independence|ch. 03]]'s Example 4g): $n$ components each lasting 8 years on average give a system lasting $8/n$ years. **With 10 components, under a year.**
>
> ---
> **(v)** **The argument is wrong under the exponential model.**
>
> By memorylessness, a machine that has run 6 years has **exactly the same remaining-lifetime distribution as a brand-new one**:
> $$P\{X>6+s\mid X>6\}=P\{X>s\}$$
> **Replacing it gains nothing** — the replacement has an identical future. **There is no "due to fail."** *(This is the gambler's fallacy in continuous time.)*
>
> **When would the manager be right?** **When the lifetime distribution has an *increasing hazard rate*:**
> $$\lambda(t)=\frac{f(t)}{1-F(t)} \quad\text{increasing in } t$$
> — **i.e. genuine wear-out.** Then old machines really are riskier and preventive replacement pays. *(Weibull with shape $>1$, §6.)*
>
> > **The whole question turns on which model is right, and that is an empirical matter.** **Exponential = constant hazard = no ageing.**
> >
> > **The practical warning: assuming exponential lifetimes for anything that physically wears out will over-predict survival** — you will schedule too little maintenance and be surprised by the failure rate. **Check whether the hazard is really flat before assuming memorylessness.**

---

## 📝 Summary

- **A continuous random variable has a density $f$ with $\int f=1$ and $P\{X\in B\}=\int_Bf$.** **$P\{X=a\}=0$ for every $a$**, so strict and non-strict inequalities coincide. **$f(a)$ is a probability *per unit length* — it can exceed 1**, and $P\{|X-a|<\varepsilon/2\}\approx\varepsilon f(a)$.
- **$F'(a)=f(a)$** — the density is the derivative of the cdf, the continuous analogue of "the pmf is the jump in $F$."
- **Expectation and variance are unchanged in substance:** $\mathbb{E}[g(X)]=\int g(x)f(x)dx$, $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$, $\mathrm{Var}(X)=\mathbb{E}[X^2]-(\mathbb{E}[X])^2$, $\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$. **Jensen's inequality governs everything non-linear.**
- **Uniform$(\alpha,\beta)$:** $\mathbb{E}=\tfrac{\alpha+\beta}2$, $\mathrm{Var}=\tfrac{(\beta-\alpha)^2}{12}$; probability equals proportional length. **Bertrand's paradox** shows that *"choose a chord at random"* has answers $\tfrac12$ **and** $\tfrac13$ depending on the mechanism — **both physically realisable.**
- **Normal$(\mu,\sigma^2)$:** standardise with $Z=(X-\mu)/\sigma$ and use $\Phi$, with $\Phi(-x)=1-\Phi(x)$. **The 68–95–99.7 rule** follows from $\Phi(1),\Phi(2),\Phi(3)$. **Probabilities in standard-deviation units do not depend on $\mu$ or $\sigma$** — which is why one table covers the whole family.
- **DeMoivre–Laplace:** $\dfrac{S_n-np}{\sqrt{np(1-p)}}\to N(0,1)$. **Apply the continuity correction** ($P\{X\ge i\}\to P\{X>i-\tfrac12\}$) — it cut the error 21-fold at $n=100$ and is the *entire* calculation for point probabilities. **Reliable when $np(1-p)\ge10$.**
- **Two approximations to the binomial, with different domains:** **Poisson** when $p$ is small and $np$ moderate (skewed, bounded at 0); **normal** when $np(1-p)\ge10$ (symmetric). **Using the normal when $np(1-p)\approx1$ fails badly** and even assigns probability to negative counts.
- **Exponential$(\lambda)$:** $\mathbb{E}=\tfrac1\lambda$, $\mathrm{Var}=\tfrac1{\lambda^2}$ (so $\mathrm{SD}=\mathbb{E}$), $P\{X>a\}=e^{-\lambda a}$. **Strongly right-skewed: median $=\tfrac{\ln2}{\lambda}\approx0.69\,\mathbb{E}$, and 63% fail before the mean.**
- **Memorylessness — $P\{X>s+t\mid X>t\}=P\{X>s\}$ — characterises the exponential completely.** It is the **only** distribution with the property, equivalently the only one with **constant hazard rate**. **The minimum of independent exponentials is exponential with rates added.**
- **Assuming memorylessness for something that ages is a substantive error** — it over-predicts survival and understates maintenance needs. **Increasing hazard (Weibull, shape $>1$) is the wear-out model.**
- **The Cauchy has no mean or variance**, so the law of large numbers fails for it: the sample mean of $n$ Cauchys is Cauchy for every $n$. **Heavy tails are not a technicality.**
- **For $Y=g(X)$, work through the cdf** and differentiate; for monotone $g$, $f_Y(y)=f_X(g^{-1}(y))\left|\tfrac{d}{dy}g^{-1}(y)\right|$ — **and the Jacobian is what everyone forgets.**

---

## ⚠️ Important Notes

> [!warning] A density is not a probability
> $$P\{X=a\}=0 \qquad\text{and}\qquad f(a) \text{ may exceed } 1$$
> **$f(a)$ has units of probability *per unit length*.** To get a probability you must integrate — or, for a small interval, multiply: $P\{|X-a|<\varepsilon/2\}\approx\varepsilon f(a)$.
>
> **The self-check: if a quantity can exceed 1, it is not a probability.** A uniform on $(0,\tfrac1{10})$ has $f\equiv10$ everywhere.
>
> **A corollary that trips people up: "probability zero" is not "impossible."** $X$ takes *some* value, and that value had probability zero beforehand.

> [!warning] "At random" is not a specification — Bertrand's paradox
> **The random-chord problem has answers $\tfrac12$ and $\tfrac13$, and both are right**, corresponding to two genuinely different physical experiments.
>
> **This joins a family of warnings across the book:**
> - [[03 - Conditional Probability and Independence|Ch. 03]] Example 3m — the two-child problem needs the *observation* mechanism
> - [[04 - Random Variables|Ch. 04]] Example 6e — the jury problem needs a prior
> - **Here** — a "random chord" needs a *generating* mechanism
>
> **In every case the honest answer is "underdetermined; here is what's missing."** **In higher dimensions this gets worse, not better** — "a random point in a region" and "a random rotation" both have several inequivalent natural definitions.

> [!warning] Use the continuity correction
> **Approximating a discrete distribution by a continuous one requires spreading each integer over a unit interval.**
>
> | $n$ | Exact | With cc | Without cc |
> |---|---|---|---|
> | 100, $P\{X\ge60\}$ | $.02844$ | $.02872$ | $.02275$ (**20% low**) |
> | 20, $P\{X\ge15\}$ | $.02070$ | $.02209$ | $.01267$ (**39% low**) |
>
> **The correction matters more when $n$ is small**, and **for point probabilities $P\{X=i\}$ it is the whole calculation** — without it the answer is identically 0.

> [!warning] Poisson or normal? The answer is about shape, not sample size
> | Regime | Approximation | Why |
> |---|---|---|
> | $p$ small, $np$ moderate | **Poisson**$(np)$ | binomial is skewed and bounded at 0 — so is Poisson |
> | $np(1-p)\ge10$ | **Normal** | binomial is near-symmetric — so is normal |
>
> **The condition is on the variance $np(1-p)$, not on $n$.** With $n=1000$, $p=.001$, $n$ is enormous and **the normal approximation is still bad** — it assigns real probability to negative counts.

> [!warning] Memorylessness is a strong assumption, and it is testable
> **The exponential is the *unique* memoryless distribution** — equivalently the unique one with **constant hazard rate**. So assuming exponential lifetimes is assuming **no wear-out and no burn-in**.
>
> **Anything that physically ages violates it**, and the error is one-directional: **you will over-predict survival and under-schedule maintenance.**
>
> **Check the hazard rate $\lambda(t)=f(t)/[1-F(t)]$ before assuming it is flat.** Increasing hazard $\Rightarrow$ preventive replacement pays; **constant hazard $\Rightarrow$ replacing a working unit gains literally nothing** (Exercise 5(v)).

> [!warning] Mean and median diverge under skew, and the mean is usually the wrong summary
> | Distribution | Relation | Reason |
> |---|---|---|
> | Exponential($\lambda$) | median $=0.69\,\mathbb{E}$ | **right** tail |
> | $f(x)\propto x^2$ on $(0,3)$ | median $>$ mean | **left** tail |
>
> **For the exponential, 63% of observations fall below the mean** — so calling it "typical" misleads about two-thirds of the time.
>
> **This is why incomes, waiting times, file sizes and survival times are reported by median.** *(And why [[Data Preparation and Visualization/contents/00-Index|Data Prep & Visualization]] insists on looking at the distribution before quoting a mean.)*

> [!warning] Normal tails vanish extremely fast — which is both a strength and a trap
> | $z$ | $P\{X>\mu+z\sigma\}$ | 1 in… |
> |---|---|---|
> | 2 | $.0228$ | 44 |
> | 3 | $.00135$ | 741 |
> | 4 | $3.2\times10^{-5}$ | 31,600 |
> | 5 | $2.9\times10^{-7}$ | 3.5 million |
>
> **Each extra sigma costs an order of magnitude or more** — the basis of the $5\sigma$ discovery standard in physics.
>
> **The trap: if the real distribution has heavier tails than normal, the model declares genuinely-occurring events impossible.** **Example 5e makes this concrete** — the same channel, the same threshold, and Laplace noise gives error probabilities **several times** the normal ones. **Normal-based VaR (Example 4f) understates extreme losses for exactly this reason.**

> [!warning] Jensen's inequality, and the log-transform trap
> $$\mathbb{E}[g(X)]\ge g(\mathbb{E}[X]) \text{ for convex } g \qquad \le \text{ for concave}$$
> **Equality only for linear $g$.**
>
> **The most consequential applied instance:** fit a model in logs, then exponentiate the fitted mean to report levels. **$\mathbb{E}[e^Y]>e^{\mathbb{E}[Y]}$**, so this **systematically understates the level** — which is why a smearing or $e^{\sigma^2/2}$ correction is needed ([[Econometrics/contents/00-Index|Econometrics]]).
>
> **Same family of error as $\mathbb{E}[X^2]\ne(\mathbb{E}[X])^2$ from [[04 - Random Variables|ch. 04]]** — expectation passes through linear functions and nothing else.

> [!warning] Do not forget the Jacobian
> For $Y=g(X)$ with $g$ monotone,
> $$f_Y(y)=f_X\big(g^{-1}(y)\big)\left|\frac{d}{dy}g^{-1}(y)\right|$$
> **Example 1d's factor of $\tfrac12$ for $Y=2X$ is exactly this**, and the intuition is that **stretching by 2 spreads the same probability over twice the length, so density halves.**
>
> **When in doubt, always go through the cdf: $F_Y(y)=P\{g(X)\le y\}$, then differentiate.** **It never fails, and it generates the Jacobian automatically.**

> [!note] Cross-subject connections
> - [[04 - Random Variables|Ch. 04]] — **the same programme with sums**; every warning about $\mathbb{E}[g(X)]$ carries over verbatim, and the Poisson/normal approximations bracket the binomial from opposite regimes.
> - [[06 - Jointly Distributed Random Variables|Ch. 06]] — extends densities to several variables; **the Jacobian of §7 becomes the multivariate change-of-variables formula.**
> - [[08 - Limit Theorems|Ch. 08]] — **DeMoivre–Laplace is a special case of the CLT**, which explains *why* the normal is ubiquitous; the Cauchy is the standard counterexample to the LLN.
> - [[09 - Additional Topics in Probability|Ch. 09]] — the **Poisson process** explains why waiting times are exponential in the first place.
> - [[Calculus/contents/00-Index|Calculus]] — this chapter is applied integration: improper integrals, integration by parts (the exponential moments), and change of variables.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — **Example 4i is a hypothesis test** ($p$-value $.0019$); Example 4j is a sample-size calculation; the normal, gamma and beta families are the backbone of everything there.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — Example 2d's quantile rule is **pinball loss**; the Gaussian is the implicit noise model behind squared-error loss, and **Laplace noise corresponds to $L_1$ loss** (Example 5e is the reason $L_1$ is more robust to outliers).

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Figures are images and cannot be extracted:**
> - **Figure 5.2** (the stick split at $U$, showing which substick contains $p$) — only `0 Up 1 (a)`, `0 Up 1 (b)`, `1 2 U` survive. **The two cases $U<p$ and $U>p$ are stated algebraically in the text**, so Example 2c is fully reconstructible.
> - **Figure 5.3** (uniform density and cdf) — the axis labels extract as `1——– – `, `baba`, `ba`, i.e. the mangled $\tfrac1{\beta-\alpha}$, $\beta$, $\alpha$. **Reconstructed from the formulas.**
> - **Figure 5.4** (Bertrand's chord and tangent angle $\theta$) — extracts as `A`, `u` (a mangled $\theta$). **The construction is described in full in the text.**
> - **Figures 5.5, 5.7** (normal density curves and the standard normal) and **Figure 5.6** (binomial pmfs at $(10,.7)$, $(20,.7)$, $(30,.7)$, $(50,.7)$ becoming progressively bell-shaped) — **only axis tick values survive.** Figure 5.6's visual argument that the binomial "becomes more and more normal" is the chapter's motivation for §4a and **cannot be reproduced from the extraction.**
> - **Table 5.1, the standard normal table, is an image.** **Every $\Phi$ value quoted in these notes has therefore been recomputed with `scipy.stats.norm`** rather than read from the source.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and checked against numeric answers):
> - **`/Phi1` is the extraction of $\Phi$** throughout §4 — e.g. `1 − /Phi1(1.5) L .0668` is $1-\Phi(1.5)\approx.0668$.
> - **`q` is `∞`**, **`…` is `≤`**, **`Ú` is `≥`**, **`L` is `≈`**, **`Z` is `≠`** — the same substitution set as chapters 2–4.
> - **Integral limits detach from their signs:** `∫q −q f(x) dx` is $\int_{-\infty}^{\infty}f(x)dx$, and `−e−x/100⏐⏐150 50` is $-e^{-x/100}\big|_{50}^{150}$.
> - **`ϵ` and `ε` both appear for the same epsilon** in Example 1d — an inconsistency in the source, not the extraction.
> - **`ν` and `v` are used interchangeably for VaR** in Example 4f (`.01 = P{−X >ν }` then `ν = VA R= 2.33σ − μ`), which is a genuine typographical inconsistency in the text.
>
> **Two rounding artefacts worth knowing about:**
> - **Example 4g:** Ross rounds $\tfrac{0.5}{\sqrt{10}}=.1581$ to $.16$ and reports the approximation as $.1272$ against the exact $.1254$. **Using the unrounded value gives $.1256$ — three times closer to the truth.** **The printed comparison understates how good the approximation is.** *(Flagged in Exercise 4(iv).)*
> - **Example 4j:** the text prints `/Phi1(1.2665) = .8973` for $n=1001$, but $.04\sqrt{1001}=\mathbf{1.26555}$ — **the digits 5 and 6 appear transposed.** The resulting probability is unaffected to three decimals ($.8972$ vs $.8973$).
>
> **Verification performed:** every numeric claim in Examples 1a–5e was independently recomputed — $C=\tfrac38$ and $P\{X>1\}=\tfrac12$; $\lambda=\tfrac1{100}$, $.383$, $.632$; $\tfrac13$ and $\tfrac{80}{243}$; $\mathrm{Var}=\tfrac1{18}$; the uniform mean/variance formulas; $.3$, $.4$, $.5$; both $\tfrac13$s; **both** Bertrand answers $\tfrac12$ and $\tfrac13$; $.3779$, $.8413$, $.0456$; the five grading probabilities $.1587,.3413,.3413,.1359,.0228$; $.0241$; $.0668$ and $.0062$; $\Phi(2.33)=.9901$; $.1272$ vs exact $.1254$; $.0559$; $.0019$; the three NYC probabilities and $n\ge1692$; $e^{-1}$ and $e^{-1}-e^{-2}$; $e^{-1/2}=.607$; and the Laplace error probabilities $.1116$ and $.0410$. **All agree with the text.** The only discrepancies found are the two rounding artefacts noted above, neither of which is an error in the mathematics.
>
> **One structural gap:** §5.6 (Gamma, Weibull, Cauchy, Beta, Pareto) is a rapid catalogue in the source — **each distribution gets a density, a moment formula, and little motivation.** **The Gamma's key property — that it is the sum of $\alpha$ independent exponentials — is proved only in [[06 - Jointly Distributed Random Variables|ch. 06 §3]]**, so a reader meeting it here has no reason to find it natural. **I have stated the connection in §6 rather than leaving the family unmotivated.**

#probability #continuous #density #normal #exponential #uniform
