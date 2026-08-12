---
subject: Probability Theory
chapter: 07
tags: [ds, probability, expectation, covariance, correlation, conditional-expectation, mgf, multivariate-normal]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 7 (pp. 315–405)"
---

# Properties of Expectation

> [!abstract] What this chapter is for
> **This is the most powerful chapter in the book.** Chapters 4–6 built distributions; this one shows that **you can very often get the answer without ever finding the distribution.**
>
> Three tools do almost all the work, and each one is a way of *avoiding* a hard calculation:
>
> | Tool | Statement | What it lets you skip |
> |---|---|---|
> | **Linearity** | $\mathbb{E}\!\left[\sum X_i\right]=\sum\mathbb{E}[X_i]$ — **no independence needed** | finding the distribution of the sum |
> | **Conditioning** | $\mathbb{E}[X]=\mathbb{E}\big[\mathbb{E}[X\mid Y]\big]$ | solving the whole problem at once |
> | **Generating functions** | $M(t)=\mathbb{E}[e^{tX}]$ determines the distribution | convolution integrals |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **2** | Expectation of sums | **Linearity holds always.** The indicator trick turns counting problems into one-line answers |
> | **3** | Moments of counts | $\mathbb{E}\!\left[\binom Xk\right]=\sum P(A_{i_1}\cdots A_{i_k})$ — variances from the same trick |
> | **4** | Covariance and correlation | $\mathrm{Var}\!\left(\sum X_i\right)=\sum\mathrm{Var}+2\sum_{i<j}\mathrm{Cov}$; $\rho$ measures **linearity only** |
> | **5** | Conditional expectation | $\mathbb{E}[X\mid Y]$ is a **random variable**; the tower property and $\mathrm{Var}(X)=\mathbb{E}[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(\mathbb{E}[X\mid Y])$ |
> | **6** | Prediction | **$\mathbb{E}[Y\mid X]$ is the best predictor under squared error** — full stop |
> | **7** | Moment generating functions | Sums $\to$ products; MGFs determine distributions |
> | **8** | Normal properties | Multivariate normal; **$\bar X\perp S^2$ and $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$** |
>
> **§6 is the theoretical foundation of all of supervised learning:** minimising mean squared error means estimating a conditional expectation. **§8.2 is the theorem that makes the $t$-test legal.**

---

## 📘 Main Knowledge

### 1. Expectation of sums — linearity, and the indicator trick

> [!important] Proposition 2.1 and its consequence
> $$\mathbb{E}[g(X,Y)]=\sum_y\sum_x g(x,y)p(x,y)\qquad\text{or}\qquad \iint g(x,y)f(x,y)\,dx\,dy$$
> and therefore, whenever the individual expectations are finite,
> $$\boxed{\ \mathbb{E}[X_1+\dots+X_n]=\mathbb{E}[X_1]+\dots+\mathbb{E}[X_n]\ }$$

> [!warning] Linearity requires **no** assumptions about dependence
> This is the single most useful fact in probability, and it is constantly under-used because people assume it needs independence. **It does not.** The $X_i$ may be as tangled as you like.
>
> Contrast with variance, which **does** need it:
> $$\mathrm{Var}\!\left(\sum X_i\right)=\sum\mathrm{Var}(X_i)\quad\textbf{only if uncorrelated}$$
> **Linearity is free; additivity of variance is not.**

Also worth stating: if $X\ge Y$ pointwise then $\mathbb{E}[X]\ge\mathbb{E}[Y]$ (apply $\mathbb{E}[X-Y]\ge0$), and if $P\{a\le X\le b\}=1$ then $a\le\mathbb{E}[X]\le b$.

#### 1a. The indicator trick

> [!tip] The single most valuable technique in the chapter
> **To find the expected *number* of things that happen:**
> 1. Write $X=\sum_i I_i$ where $I_i=\mathbb{1}\{A_i\text{ occurs}\}$.
> 2. Note $\mathbb{E}[I_i]=P(A_i)$.
> 3. Conclude $\mathbb{E}[X]=\sum_i P(A_i)$.
>
> **Step 3 needs no independence** — so the $A_i$ may overlap, conflict, or be wildly dependent. **This converts almost every "expected number of…" problem into a list of single-event probabilities.**

The payoff is a sequence of results that were painful in [[04 - Random Variables|ch. 04]] and are now one line each:

| Problem | Decomposition | $\mathbb{E}[X]$ |
|---|---|---|
| **Binomial** | $X_i=\mathbb{1}\{$trial $i$ succeeds$\}$ | $np$ |
| **Negative binomial** | $X_i=$ trials between success $i-1$ and $i$ | $r/p$ |
| **Hypergeometric** | $Y_i=\mathbb{1}\{i$th draw is white$\}$ | $nm/N$ |
| **Matching (hats)** | $X_i=\mathbb{1}\{$person $i$ gets own hat$\}$ | $N\cdot\tfrac1N=\mathbf{1}$ |
| **Coupon collector** | $X_i=$ extra coupons after $i$ distinct types | $N\sum_{k=1}^{N}\tfrac1k$ |

> [!example] The matching problem — the cleanest demonstration
> $N$ people throw their hats in a pile and each takes one at random. **The expected number who get their own hat is exactly 1, for every $N$.**
>
> The $X_i$ are **strongly dependent** (if $N-1$ people got their own hat, so did the last), and the exact distribution of $X$ is a genuinely awkward inclusion–exclusion object ([[02 - Axioms of Probability|ch. 02]]). **None of that matters** — $\mathbb{E}[X_i]=1/N$ and there are $N$ terms.
>
> §2 below shows the **variance is also exactly 1**, for every $N$ — the count behaves like a Poisson(1) even before you prove that it converges to one.

> [!example] The coupon collector — why the last few coupons are so expensive
> $$\mathbb{E}[X]=N\left(1+\tfrac12+\dots+\tfrac1N\right)\approx N\log N + \gamma N$$
> With $N=50$: about $\mathbf{225}$ coupons for 50 types. **The first half of the set costs $\approx N\log 2\approx35$; the last single coupon alone costs $N=50$ on average.**
>
> **The $\log N$ factor is the whole story:** collecting is not linear in $N$, and the tail dominates. *(This is exactly the "coupon collector bound" that appears in randomised-algorithm analysis and in estimating how long a crawler needs to see every page.)*

> [!example] Runs, and quicksort
> **Runs** (Example 2k): with $n$ ones and $m$ zeros randomly permuted, $I_i=\mathbb{1}\{$a run of 1s starts at position $i\}$ gives
> $$\mathbb{E}[R(1)]=\frac{n}{n+m}+\frac{nm}{n+m},\qquad \mathbb{E}[R(1)+R(0)]=1+\frac{2nm}{n+m}$$
> *(Checked by brute force at $n=6,m=4$: $3.0$ and $2.8$, total $5.8$ ✓.)*
>
> **Quicksort** (Example 2m): let $I(i,j)=\mathbb{1}\{$the $i$th and $j$th smallest are ever directly compared$\}$. Values $i,\dots,j$ stay in one bracket until one of them is chosen as pivot, and $i$ and $j$ are compared **iff that pivot is $i$ or $j$** — probability $\dfrac2{j-i+1}$. Hence
> $$\mathbb{E}[\#\text{comparisons}]=\sum_{i<j}\frac{2}{j-i+1}\approx 2n\log n$$
> **This is the $O(n\log n)$ average-case bound for quicksort, derived in half a page with no recurrence relation.** It is the standard example of probability paying off in algorithm analysis ([[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]]).

#### 1b. Two identities worth knowing

$$\mathbb{E}[X]=\sum_{i=1}^{\infty}P\{X\ge i\}\qquad\text{for non-negative integer-valued }X$$

*(Proof: $X=\sum_i\mathbb{1}\{X\ge i\}$.)* This is the discrete twin of $\mathbb{E}[X]=\int_0^\infty P\{X>t\}dt$ from [[05 - Continuous Random Variables|ch. 05]], and it is often far easier than summing $xp(x)$.

$$P\!\left(\bigcup_i A_i\right)=\mathbb{E}\!\left[1-\prod_i(1-I_i)\right]$$

Expanding the product **recovers inclusion–exclusion**, and applying $X\ge Y$ to $X=\sum I_i$, $Y=\mathbb{1}\{X\ge1\}$ **recovers Boole's inequality** — two results from ch. 02 falling out of linearity.

#### 1c. The probabilistic method

> [!tip] Proving something exists by averaging
> If $S$ is a random element of a finite set $A$ and $m=\max_{s\in A}f(s)$, then
> $$m\ \ge\ \mathbb{E}[f(S)]$$
> **with strict inequality unless $f(S)$ is constant.** So *computing an average proves that some element beats it.*
>
> - **Hamiltonian paths (Example 2q):** in a random round-robin tournament each of the $n!$ orderings is a Hamiltonian path with probability $(1/2)^{n-1}$, so $\mathbb{E}[f(S)]=n!/2^{n-1}$ — **hence some tournament has more than $n!/2^{n-1}$ Hamiltonian paths**, though the argument exhibits none of them.
> - **Chipmunks (Example 2r):** 15 chipmunks in 52 circular trees; a random 7-tree neighbourhood houses $\mathbb{E}[X]=15\cdot\tfrac7{52}=\tfrac{105}{52}>2$ of them, **so some 7-tree block houses at least 3.**
>
> **This is a genuinely different mode of proof** — non-constructive, and the ancestor of much of modern combinatorics.

---

### 2. Moments of the number of events that occur

The indicator trick extends past the mean. If $X=\sum_{i=1}^n I_i$ counts how many of $A_1,\dots,A_n$ occur, then $\binom Xk$ counts the $k$-subsets that *all* occur, so

$$\boxed{\ \mathbb{E}\!\left[\binom Xk\right]=\sum_{i_1<\dots<i_k}P(A_{i_1}A_{i_2}\cdots A_{i_k})\ }$$

For $k=2$ this gives $\mathbb{E}[X^2]-\mathbb{E}[X]=2\sum_{i<j}P(A_iA_j)$, hence the variance.

> [!important] Variances of the standard counting distributions, all from one formula
> | Distribution | $P(A_iA_j)$ | $\mathrm{Var}(X)$ |
> |---|---|---|
> | Binomial | $p^2$ | $np(1-p)$ |
> | Hypergeometric | $\dfrac mN\dfrac{m-1}{N-1}$ | $\dfrac{mn}N\!\left[\dfrac{(n-1)(m-1)}{N-1}+1-\dfrac{mn}N\right]$ |
> | Matching | $\dfrac1{N(N-1)}$ | $\mathbf{1}$ |
>
> **The matching problem again: $\mathbb{E}[X(X-1)]=1$, so $\mathbb{E}[X^2]=2$ and $\mathrm{Var}(X)=1$.** More strikingly, $\mathbb{E}[X(X-1)\cdots(X-k+1)]=1$ for **every** $k$ — **all the factorial moments equal 1, which is exactly the signature of a Poisson(1)**, confirming the ch. 04 limit.

> [!example] Example 3e — the negative hypergeometric
> Draw without replacement from $n$ special and $m$ ordinary balls until $r$ special ones appear; let $Y$ be the number of draws. **Do not use the pmf.** Instead let $A_i=\{$ordinary ball $i$ comes out before the $r$th special one$\}$: among the $n+1$ balls consisting of $o_i$ and the $n$ special ones, $o_i$ is equally likely to be in any position, so $P(A_i)=\frac r{n+1}$. Hence
> $$\mathbb{E}[Y]=r+\frac{mr}{n+1}=\frac{r(n+m+1)}{n+1},\qquad \mathrm{Var}(Y)=\frac{mr(n+1-r)(n+m+1)}{(n+1)^2(n+2)}$$
> **Cards you must turn over to see the first spade: $\tfrac{53}{14}=3.79$. To see the first ace: $\tfrac{53}{5}=10.6$.** *(Both verified.)* **The mean, not the median — half the time you see an ace much sooner.**

---

### 3. Covariance, variance of sums, and correlation

> [!important] Proposition 4.1
> If $X\perp Y$ then $\mathbb{E}[g(X)h(Y)]=\mathbb{E}[g(X)]\,\mathbb{E}[h(Y)]$ for **all** $g,h$.

$$\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mathbb{E}X)(Y-\mathbb{E}Y)\big]=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]$$

**Properties (Proposition 4.2):** symmetric; $\mathrm{Cov}(X,X)=\mathrm{Var}(X)$; $\mathrm{Cov}(aX,Y)=a\,\mathrm{Cov}(X,Y)$; and **bilinearity**, which is the one that does the work:

$$\mathrm{Cov}\!\left(\sum_{i=1}^n X_i,\ \sum_{j=1}^m Y_j\right)=\sum_{i=1}^n\sum_{j=1}^m \mathrm{Cov}(X_i,Y_j)$$

Setting $Y_j=X_j$ gives the master variance formula:

$$\boxed{\ \mathrm{Var}\!\left(\sum_{i=1}^n X_i\right)=\sum_{i=1}^n\mathrm{Var}(X_i)+2\!\!\sum_{i<j}\!\mathrm{Cov}(X_i,X_j)\ }$$

which collapses to $\sum\mathrm{Var}(X_i)$ when the $X_i$ are **pairwise** uncorrelated — note that pairwise is enough here, unlike for most independence arguments.

#### 3a. Uncorrelated is weaker than independent

> [!warning] $\mathrm{Cov}=0$ does **not** imply independence
> Ross's minimal counterexample: $P\{X=-1\}=P\{X=0\}=P\{X=1\}=\tfrac13$ and $Y=\mathbb{1}\{X=0\}$. Then $XY\equiv0$ and $\mathbb{E}[X]=0$, so $\mathrm{Cov}(X,Y)=0$ — **yet $Y$ is a deterministic function of $X$.**
>
> **Covariance detects only the *linear* component of a relationship.** A perfectly deterministic but symmetric relationship is invisible to it. **The one exception is the bivariate normal** ([[06 - Jointly Distributed Random Variables|ch. 06 §5b]]), where $\rho=0$ really does give independence.

#### 3b. Correlation

$$\rho(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sqrt{\mathrm{Var}(X)\mathrm{Var}(Y)}},\qquad -1\le\rho\le1$$

> [!tip] Why $|\rho|\le1$, in one line each way
> $0\le\mathrm{Var}\!\left(\frac X{\sigma_x}+\frac Y{\sigma_y}\right)=2[1+\rho]$ gives $\rho\ge-1$; $0\le\mathrm{Var}\!\left(\frac X{\sigma_x}-\frac Y{\sigma_y}\right)=2[1-\rho]$ gives $\rho\le1$. **A variance being non-negative is the whole proof.**
>
> **And the equality case is exact:** $\rho=\pm1$ $\iff$ $Y=a+bX$ with $\mathrm{sign}(b)=\mathrm{sign}(\rho)$ — because zero variance means constant with probability 1.

> [!example] Three covariances worth memorising
> - **Indicators (Example 4d):** $\mathrm{Cov}(I_A,I_B)=P(AB)-P(A)P(B)=P(B)\big[P(A\mid B)-P(A)\big]$. **So the sign of the covariance is the sign of "does $B$ make $A$ more likely?"** — the cleanest possible statement of what covariance means.
> - **Multinomial (Example 4f):** $\mathrm{Cov}(N_i,N_j)=-mp_ip_j$ for $i\ne j$. **Always negative** — the categories compete for a fixed number of trials.
> - **Sample mean and deviation (Example 4e):** $\mathrm{Cov}(X_i-\bar X,\ \bar X)=0$. **The deviations are uncorrelated with the mean** — the reason $\bar X$ and $S^2$ can be independent (§7).

> [!example] Example 4a — why $S^2$ divides by $n-1$
> For i.i.d. $X_i$ with mean $\mu$, variance $\sigma^2$:
> $$\mathrm{Var}(\bar X)=\frac{\sigma^2}{n},\qquad \mathbb{E}[S^2]=\sigma^2\ \text{ where } S^2=\frac{\sum_i(X_i-\bar X)^2}{n-1}$$
> The proof rests on the identity $\sum_i(X_i-\bar X)^2=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2$: taking expectations gives $n\sigma^2-\sigma^2=(n-1)\sigma^2$.
>
> **So the $n-1$ is not a convention — it is exactly the correction for having estimated $\mu$ by $\bar X$.** Dividing by $n$ gives an estimator biased *low* by a factor $\frac{n-1}n$, because the sample is always closer to its own mean than to the truth. **One degree of freedom was spent.**

> [!example] Example 4c — the finite-population correction
> Sampling $n$ of $N$ people without replacement, with $\bar v$ the population proportion in favour:
> $$\mathbb{E}\!\left[\frac Sn\right]=\bar v,\qquad \mathrm{Var}\!\left(\frac Sn\right)=\frac{N-n}{n(N-1)}\,p(1-p)$$
> **The factor $\frac{N-n}{N-1}$ is the finite-population correction.** Two consequences that matter for real surveys:
> - **When $n=N$ the variance is exactly 0** — a census has no sampling error.
> - **When $N\gg n$ the factor is $\approx1$**, so the variance is $\frac{p(1-p)}n$ — **which does not depend on $N$ at all.** *This is why a national poll needs about the same sample size as a city poll,* the single most counter-intuitive fact in survey sampling.

---

### 4. Conditional expectation

$$\mathbb{E}[X\mid Y=y]=\sum_x x\,p_{X\mid Y}(x\mid y)\qquad\text{or}\qquad\int_{-\infty}^{\infty} x\,f_{X\mid Y}(x\mid y)\,dx$$

**Every property of ordinary expectation carries over** — linearity, $\mathbb{E}[g(X)\mid Y=y]$, all of it — because a conditional expectation *is* an ordinary expectation, taken on the reduced sample space $\{Y=y\}$.

> [!important] $\mathbb{E}[X\mid Y]$ is a random variable
> Write $\mathbb{E}[X\mid Y]$ for the function of $Y$ whose value at $Y=y$ is $\mathbb{E}[X\mid Y=y]$. **Since $Y$ is random, so is $\mathbb{E}[X\mid Y]$** — this is the conceptual leap of the chapter, and the reason the next two formulas even make sense.

#### 4a. The tower property

$$\boxed{\ \mathbb{E}[X]=\mathbb{E}\big[\mathbb{E}[X\mid Y]\big]\ }\qquad\text{i.e.}\qquad \mathbb{E}[X]=\sum_y\mathbb{E}[X\mid Y=y]P\{Y=y\}$$

**Read it as a weighted average of conditional answers** — it is the law of total probability with expectations in place of probabilities. The technique it licenses is: *find a variable that, if you knew it, would make the problem easy; condition on it; average back.*

> [!example] Example 5c — the trapped miner
> Three doors: one leads out in 3 hours, the others return him after 5 and 7 hours. Each choice is uniform and independent.
> $$\mathbb{E}[X]=\tfrac13\big(3+(5+\mathbb{E}[X])+(7+\mathbb{E}[X])\big)\ \Longrightarrow\ \mathbb{E}[X]=\mathbf{15}\text{ hours}$$
> **The self-referential step is the point:** returning to the cell resets the problem exactly, so the *remaining* expected time is again $\mathbb{E}[X]$. **The answer, 15, is far larger than the average door time $(3+5+7)/3=5$** — because bad doors get chosen repeatedly.

> [!example] Example 5d/5q — sums of a random number of terms
> If $N$ is independent of the i.i.d. sequence $X_i$:
> $$\mathbb{E}\!\left[\sum_{i=1}^N X_i\right]=\mathbb{E}[N]\,\mathbb{E}[X],\qquad \mathrm{Var}\!\left(\sum_{i=1}^N X_i\right)=\mathbb{E}[N]\,\mathrm{Var}(X)+(\mathbb{E}[X])^2\,\mathrm{Var}(N)$$
> **The mean is what you'd guess; the variance is not.** 50 customers on average spending \$8 each gives \$400 — but the variance has **two** sources, and when $N$ is highly variable the *second* term dominates. **Forgetting the $(\mathbb{E}X)^2\mathrm{Var}(N)$ term is the standard error in insurance and queueing calculations.** *(Exercise 3 makes the size of the effect concrete.)*

> [!example] Example 5i — gambler's ruin among $r$ players
> $r$ players with fortunes $n_i$ summing to $n$; each stage two players are picked and a fair unit is transferred. Conditioning gives $m_j=1+\tfrac12m_{j+1}+\tfrac12m_{j-1}$, whose solution is $m_i=i(n-i)$ — **the expected number of games between two players is the product of their fortunes.** Summing over players and halving (each stage involves two):
> $$\mathbb{E}[X]=\tfrac12\left(n^2-\sum_{i=1}^r n_i^2\right)$$
> **Remarkably, this does not depend on how the pairs are chosen at each stage** — though the *distribution* of the number of stages does. *(Verified by simulation for $r=3$, $n=(1,1,2)$: formula 5, simulated 5.005.)*

> [!example] Example 5k — the best-prize (secretary) problem
> $n$ prizes arrive in random order; you see only relative ranks and must accept or reject irrevocably. **Strategy: reject the first $k$, then take the first one better than all of them.** Conditioning on the position of the best prize,
> $$P_k(\text{best})=\frac kn\sum_{i=k+1}^{n}\frac1{i-1}\approx\frac kn\log\frac nk$$
> maximised at $k=n/e$, giving success probability $\approx\boxed{1/e\approx.36788}$.
>
> **Most people expect this to vanish as $n\to\infty$; it does not.** Even the crude "skip half" rule succeeds with probability $>\tfrac14$ for any $n$. **This is the origin of the $37\%$ rule in optimal-stopping folklore.**

> [!example] Example 5l — a uniform prior makes the count uniform
> If $U\sim U(0,1)$ and $X\mid U=p\ \sim\ \text{Bin}(n,p)$, then
> $$P\{X=i\}=\binom ni\int_0^1 p^i(1-p)^{n-i}dp=\frac1{n+1},\qquad i=0,\dots,n$$
> **Every count is equally likely.** The slick argument: let $U,U_1,\dots,U_n$ be i.i.d. uniforms and $X=\#\{i:U_i<U\}$; **$U$ is equally likely to be any of the $n+1$ ranks**, so $X$ is uniform. **Mixing a binomial over a uniform $p$ flattens it completely** — a useful antidote to the intuition that averaging always concentrates.

#### 4b. Conditional variance

$$\mathrm{Var}(X\mid Y)=\mathbb{E}\big[(X-\mathbb{E}[X\mid Y])^2\ \big|\ Y\big]=\mathbb{E}[X^2\mid Y]-(\mathbb{E}[X\mid Y])^2$$

> [!important] Proposition 5.2 — the conditional variance formula (the law of total variance)
> $$\boxed{\ \mathrm{Var}(X)=\underbrace{\mathbb{E}\big[\mathrm{Var}(X\mid Y)\big]}_{\text{within-group variance}}+\underbrace{\mathrm{Var}\big(\mathbb{E}[X\mid Y]\big)}_{\text{between-group variance}}\ }$$

**This is the ANOVA decomposition**, and in machine learning it is the **bias–variance-style split of unexplained vs explained variation**: the second term is the variance a predictor using $Y$ can remove; the first is the irreducible remainder. **In [[Econometrics/contents/00-Index|Econometrics]] it is the population version of "total sum of squares = explained + residual."**

> [!example] Example 5p — a Poisson count observed at a random time
> Arrivals are Poisson at rate $\lambda$; the train arrives at $Y\sim U(0,T)$. Then $\mathbb{E}[N(Y)]=\lambda T/2$ and
> $$\mathrm{Var}(N(Y))=\underbrace{\lambda\frac T2}_{\mathbb{E}[\mathrm{Var}]}+\underbrace{\lambda^2\frac{T^2}{12}}_{\mathrm{Var}(\mathbb{E})}$$
> **The second term is the extra variability created purely by not knowing when the train comes**, and for large $T$ it dominates. **Randomness in *when you look* can matter more than the randomness you are looking at.**

---

### 5. Conditional expectation and prediction

> [!important] Proposition 6.1 — the best predictor
> Among all functions $g$,
> $$\mathbb{E}\big[(Y-g(X))^2\big]\ \ge\ \mathbb{E}\big[(Y-\mathbb{E}[Y\mid X])^2\big]$$
> **The conditional expectation $\mathbb{E}[Y\mid X]$ minimises mean squared error.**

The intuitive proof: with no data, the constant minimising $\mathbb{E}[(Y-c)^2]$ is $c=\mathbb{E}[Y]$. **Observing $X=x$ changes nothing except that every probability is now conditional** — so the answer becomes $\mathbb{E}[Y\mid X=x]$.

> [!tip] Why this proposition is the foundation of supervised learning
> **Every regression, every neural network trained on squared error, is estimating $\mathbb{E}[Y\mid X]$** — that function is the *target*, and the only questions are how to approximate it from data and how much data you need. **"Choose the loss, and the loss chooses the target":** squared error targets the conditional **mean**; absolute error targets the conditional **median**; pinball loss targets a conditional **quantile** ([[05 - Continuous Random Variables|ch. 05]]). See [[Machine Learning/contents/00-Index|Machine Learning]].

#### 5a. The best *linear* predictor

When the joint distribution is unknown or $\mathbb{E}[Y\mid X]$ is intractable, restrict to $g(x)=a+bx$. Minimising over $a,b$:

$$\boxed{\ \hat Y=\mu_y+\rho\frac{\sigma_y}{\sigma_x}(X-\mu_x),\qquad \text{MSE}=\sigma_y^2(1-\rho^2)\ }$$

Three readings of the same two formulas:

- **The slope is $b=\mathrm{Cov}(X,Y)/\sigma_x^2$** — the population least-squares coefficient.
- **$\rho^2$ is the fraction of variance removed**; $|\rho|$ near 1 makes the MSE near zero.
- **Only means, variances and $\rho$ are needed** — no distributional assumption at all.

> [!important] When linear is optimal
> **$\mathbb{E}[Y\mid X]$ is linear in $X$ for the bivariate normal** ([[06 - Jointly Distributed Random Variables|ch. 06 §5b]]), so there the best linear predictor *is* the best predictor. **In general it is not** — Exercise 5 gives an example with $\rho=.968$ where the true relationship is exactly deterministic yet linear prediction still errs.

> [!example] Example 6b — signal plus noise, and shrinkage
> Signal $S\sim N(\mu,\sigma^2)$, received $R=S+\text{noise}$ with noise $\sim N(0,1)$. Then
> $$\mathbb{E}[S\mid R=r]=\underbrace{\frac{1}{1+\sigma^2}}_{\text{weight on prior}}\mu+\underbrace{\frac{\sigma^2}{1+\sigma^2}}_{\text{weight on data}}r,\qquad \mathrm{Var}(S\mid R=r)=\frac{\sigma^2}{1+\sigma^2}$$
> **The estimate is a weighted average of the prior mean and the observation, weighted inversely by their variances.** Noisy channel ($\sigma^2$ small relative to 1) $\Rightarrow$ trust the prior; clean channel $\Rightarrow$ trust the data.
>
> **This is the Kalman filter's update step, shrinkage estimation, and ridge regression, all in one formula** — and the posterior variance is *smaller than either input variance*, which is what "information accumulates" means quantitatively.

> [!example] Example 6c — optimal quantisation
> To discretise $X$ into levels $y_i$ on intervals $(a_i,a_{i+1}]$ minimising $\mathbb{E}[(X-Y)^2]$: take $y_i=\mathbb{E}[X\mid a_i<X\le a_{i+1}]$ — **the conditional mean of each bin, not its midpoint.** Then $\mathbb{E}[Y]=\mathbb{E}[X]$ and
> $$\mathrm{Var}(Y)=\mathrm{Var}(X)-\mathbb{E}[(X-Y)^2]$$
> **Quantisation preserves the mean and strictly loses variance.** This is the theory behind Lloyd–Max quantisers and, in a straight line, **behind $k$-means: each centroid should be the mean of its cluster.**

---

### 6. Moment generating functions

$$M(t)=\mathbb{E}[e^{tX}],\qquad M^{(n)}(0)=\mathbb{E}[X^n]$$

Differentiating under the expectation gives $M'(t)=\mathbb{E}[Xe^{tX}]$, so $M'(0)=\mathbb{E}[X]$, $M''(0)=\mathbb{E}[X^2]$, and so on — hence the name.

| Distribution | $M(t)$ | Mean | Variance |
|---|---|---|---|
| Bin$(n,p)$ | $(pe^t+1-p)^n$ | $np$ | $np(1-p)$ |
| Poisson$(\lambda)$ | $\exp\{\lambda(e^t-1)\}$ | $\lambda$ | $\lambda$ |
| Geometric$(p)$ | $\dfrac{pe^t}{1-(1-p)e^t}$ | $\dfrac1p$ | $\dfrac{1-p}{p^2}$ |
| NegBin$(r,p)$ | $\left[\dfrac{pe^t}{1-(1-p)e^t}\right]^r$ | $\dfrac rp$ | $\dfrac{r(1-p)}{p^2}$ |
| Uniform$(a,b)$ | $\dfrac{e^{tb}-e^{ta}}{t(b-a)}$ | $\dfrac{a+b}2$ | $\dfrac{(b-a)^2}{12}$ |
| Exp$(\lambda)$ | $\dfrac{\lambda}{\lambda-t}$, $t<\lambda$ | $\dfrac1\lambda$ | $\dfrac1{\lambda^2}$ |
| Gamma$(s,\lambda)$ | $\left(\dfrac{\lambda}{\lambda-t}\right)^{s}$ | $\dfrac s\lambda$ | $\dfrac s{\lambda^2}$ |
| $N(\mu,\sigma^2)$ | $\exp\left\{\mu t+\dfrac{\sigma^2t^2}2\right\}$ | $\mu$ | $\sigma^2$ |
| $\chi^2_n$ | $(1-2t)^{-n/2}$ | $n$ | $2n$ |

> [!important] The two properties that make MGFs worth learning
> 1. **Independence turns sums into products:** $X\perp Y\Rightarrow M_{X+Y}(t)=M_X(t)M_Y(t)$.
> 2. **Uniqueness:** if $M$ is finite near $t=0$ it determines the distribution completely.
>
> **Together these replace every convolution integral of [[06 - Jointly Distributed Random Variables|ch. 06 §3]] with a multiplication.** All four closure results — normal, Poisson, gamma, binomial — become one-line checks:
> $$\exp\!\left\{\mu_1t+\tfrac{\sigma_1^2t^2}2\right\}\exp\!\left\{\mu_2t+\tfrac{\sigma_2^2t^2}2\right\}=\exp\!\left\{(\mu_1{+}\mu_2)t+\tfrac{(\sigma_1^2{+}\sigma_2^2)t^2}2\right\}$$
> **And it makes the *shared-parameter* requirement obvious:** $\left(\frac{\lambda_1}{\lambda_1-t}\right)^{s}\left(\frac{\lambda_2}{\lambda_2-t}\right)^{t'}$ simplifies only when $\lambda_1=\lambda_2$.

> [!example] Example 7j — MGF of a random sum
> $Y=\sum_{i=1}^N X_i$ with $N$ independent of the $X_i$: conditioning gives $\mathbb{E}[e^{tY}\mid N]=(M_X(t))^N$, so
> $$M_Y(t)=\mathbb{E}\big[(M_X(t))^N\big]$$
> Differentiating twice recovers $\mathbb{E}[Y]=\mathbb{E}[N]\mathbb{E}[X]$ and $\mathrm{Var}(Y)=\mathbb{E}[N]\mathrm{Var}(X)+(\mathbb{E}[X])^2\mathrm{Var}(N)$ — **the §4a results, obtained mechanically.** When $N$ is Poisson this is the **compound Poisson**, the standard model for aggregate insurance claims.

**Joint MGFs** are defined by $M(t_1,\dots,t_n)=\mathbb{E}[e^{t_1X_1+\dots+t_nX_n}]$, and

$$X_1,\dots,X_n \text{ independent} \iff M(t_1,\dots,t_n)=M_{X_1}(t_1)\cdots M_{X_n}(t_n)$$

which gives a two-line proof that $X+Y\perp X-Y$ for independent normals (Example 7l), and a two-line proof of Poisson thinning (Example 7m).

---

### 7. Additional properties of normal random variables

#### 7a. The multivariate normal

$X_1,\dots,X_m$ are **multivariate normal** if each is a linear combination of the same independent standard normals $Z_1,\dots,Z_n$ (plus a constant). Then every $\sum t_iX_i$ is itself normal, so

$$M(t_1,\dots,t_m)=\exp\left\{\sum_i t_i\mu_i+\frac12\sum_i\sum_j t_it_j\,\mathrm{Cov}(X_i,X_j)\right\}$$

> [!important] The defining feature
> **The joint distribution is completely determined by the mean vector and the covariance matrix.** Nothing else about the variables matters. For $m=2$ this reduces to the bivariate normal of ch. 06 — and it is where $\rho$ in that density is *shown* to be the correlation (Example 5f).
>
> **This is why covariance matrices are ubiquitous in practice** (PCA, Gaussian processes, Kalman filters, portfolio theory): under a multivariate normal model, second moments are the entire model.

> [!example] Example 8a — the difference of correlated normals
> $$P\{X<Y\}=\Phi\!\left(\frac{\mu_y-\mu_x}{\sqrt{\sigma_x^2+\sigma_y^2-2\rho\sigma_x\sigma_y}}\right)$$
> **Note the $-2\rho\sigma_x\sigma_y$:** positive correlation *shrinks* the variability of the difference. **This is the entire statistical justification for paired designs** — pairing induces positive correlation, which shrinks the standard error of the difference ([[Mathematical Statistics/contents/08 - Inferences on Two Samples|Mathematical Statistics ch. 08]]).

#### 7b. The sample mean and sample variance

> [!important] Proposition 8.1 — the theorem that makes the $t$-test legal
> If $X_1,\dots,X_n$ are i.i.d. $N(\mu,\sigma^2)$, then
> 1. $\bar X\sim N\!\left(\mu,\ \dfrac{\sigma^2}{n}\right)$
> 2. $\dfrac{(n-1)S^2}{\sigma^2}\sim\chi^2_{n-1}$
> 3. **$\bar X$ and $S^2$ are independent.**

The proof is a beautiful three-step argument:

1. $\mathrm{Cov}(\bar X, X_i-\bar X)=0$ (Example 4e), and **for jointly multivariate normal variables zero covariance *is* independence** — so $\bar X$ is independent of the entire vector of deviations, hence of $S^2$.
2. Divide the identity $\sum(X_i-\bar X)^2=\sum(X_i-\mu)^2-n(\bar X-\mu)^2$ by $\sigma^2$:
$$\frac{(n-1)S^2}{\sigma^2}+\left(\frac{\bar X-\mu}{\sigma/\sqrt n}\right)^2=\sum_{i=1}^n\left(\frac{X_i-\mu}{\sigma}\right)^2$$
3. The right side is $\chi^2_n$ with MGF $(1-2t)^{-n/2}$; the second left term is $\chi^2_1$ with $(1-2t)^{-1/2}$; **independence lets us divide**, leaving $(1-2t)^{-(n-1)/2}$ — a $\chi^2_{n-1}$.

> [!tip] Where the "lost degree of freedom" physically goes
> **Step 2 is the whole story:** the $n$ squared deviations from $\mu$ split into deviations from $\bar X$ plus one term for $\bar X$ itself. **The $n-1$ in $S^2$ and the $n-1$ degrees of freedom are literally the same subtraction.**
>
> And **step 3 needs independence to divide the MGFs** — so property (3) is not a bonus, it is load-bearing. Combined with §5c of ch. 06, $\dfrac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1}$: a standard normal over an independent $\sqrt{\chi^2/\text{df}}$. **That is the one-sample $t$-statistic, and Proposition 8.1 is its entire justification.**
>
> **This is also the sharpest statement of why normality matters in small samples:** independence of $\bar X$ and $S^2$ holds *only* for the normal.

#### 7c. A note on the general definition

For random variables that are neither discrete nor continuous (e.g. $W$ equal to 1 with probability $\tfrac12$ and uniform on $[0,1]$ otherwise), expectation is defined by a **Stieltjes integral** $\mathbb{E}[X]=\int x\,dF(x)$, which reduces to a sum or an ordinary integral in the two familiar cases. **It is a unification device, not new mathematics** — but it is why measure-theoretic probability states one theorem where this book states two.

---

## ✏️ Exercises

> [!question] Exercise 1 — the indicator trick *(warm-up)*
> A fair die is rolled 12 times. Let $Y$ be the number of **distinct** faces that appear.
>
> (i) Find $\mathbb{E}[Y]$.
> (ii) Explain why the indicators you used are **not** independent, and why this does not affect (i).
> (iii) Find $\mathrm{Var}(Y)$.
> (iv) How many rolls are needed before *all six* faces are expected to have appeared?

> [!example]- Solution
> **(i)** Let $A_i=\{$face $i$ never appears$\}$, so $P(A_i)=(5/6)^{12}$. With $X=\#\{$missing faces$\}=\sum_{i=1}^6 \mathbb{1}_{A_i}$,
> $$\mathbb{E}[Y]=6-\mathbb{E}[X]=6\left[1-\left(\tfrac56\right)^{12}\right]=6(1-.11216)=\boxed{5.327}$$
>
> **(ii)** They are dependent: knowing face 1 is missing makes the other faces *more* likely to appear (the 12 rolls are concentrated on five faces), so $P(A_j\mid A_i)=(4/5)^{12}<P(A_j)$. **Negatively dependent.** **Linearity does not care** — $\mathbb{E}[\sum I_i]=\sum P(A_i)$ requires nothing about the joint behaviour. *(This is the point of the exercise.)*
>
> **(iii)** Dependence *does* matter here. Using $\mathbb{E}[X(X-1)]=2\sum_{i<j}P(A_iA_j)$ with $P(A_iA_j)=(4/6)^{12}$:
> $$\mathrm{Var}(Y)=\mathrm{Var}(X)=30\left(\tfrac46\right)^{12}+6\left(\tfrac56\right)^{12}-36\left(\tfrac56\right)^{24}=\boxed{.4513}\quad(\mathrm{SD}=.672)$$
> *(Confirmed against an exact dynamic-programming computation over the number of distinct faces.)* **A standard deviation of only 0.67 on a maximum of 6 — after 12 rolls the answer is almost always 5 or 6.**
>
> **(iv)** This is the **coupon collector**: $\mathbb{E}=6\left(1+\tfrac12+\tfrac13+\tfrac14+\tfrac15+\tfrac16\right)=6\cdot\tfrac{49}{20}=\boxed{14.7}$ rolls.
> **Note $14.7\gg12$** — consistent with (i), where 12 rolls left 0.67 faces missing on average. **The last face alone costs 6 rolls in expectation.**

> [!question] Exercise 2 — covariance algebra
> $\mathrm{Var}(X)=4$, $\mathrm{Var}(Y)=9$, $\rho(X,Y)=0.5$. Compute:
>
> (i) $\mathrm{Cov}(X,Y)$
> (ii) $\mathrm{Var}(X+Y)$ and $\mathrm{Var}(X-Y)$
> (iii) $\mathrm{Var}(2X-3Y+5)$
> (iv) $\mathrm{Cov}(X,\ X+Y)$ and $\rho(X,\ X+Y)$
> (v) A colleague reports $\rho=0.5$ and concludes "$X$ explains half the variation in $Y$." Correct them.

> [!example]- Solution
> **(i)** $\mathrm{Cov}=\rho\sigma_x\sigma_y=0.5\times2\times3=\boxed{3}$
>
> **(ii)** $\mathrm{Var}(X+Y)=4+9+2(3)=\boxed{19}$; $\mathrm{Var}(X-Y)=4+9-2(3)=\boxed{7}$.
> **Positive correlation inflates the sum and deflates the difference** — the mirror image of the independent case, where both equal 13.
>
> **(iii)** $\mathrm{Var}(2X-3Y+5)=4\mathrm{Var}(X)+9\mathrm{Var}(Y)-2(2)(3)\mathrm{Cov}(X,Y)=16+81-36=\boxed{61}$.
> **The $+5$ contributes nothing** — variance is unaffected by shifts. **The cross term picks up the *product* of the coefficients, including their signs.**
>
> **(iv)** By bilinearity, $\mathrm{Cov}(X,X+Y)=\mathrm{Var}(X)+\mathrm{Cov}(X,Y)=4+3=\boxed{7}$, and
> $$\rho(X,X+Y)=\frac{7}{\sqrt{4\cdot19}}=\frac{7}{8.718}=\boxed{.803}$$
> **A variable is strongly correlated with any sum it is part of** — which is why plotting a component against a total ("spurious correlation with a ratio or a total") is misleading by construction.
>
> **(v)** Wrong twice over. **First, the fraction of variance explained is $\rho^2=0.25$, not $\rho$** — a quarter, not a half. **Second, "explains" imports causation that a covariance cannot supply**; $\rho$ is symmetric in $X$ and $Y$, so the same number equally supports "$Y$ explains $X$."

> [!question] Exercise 3 — conditioning
> (i) A rat in a maze faces three passages, chosen independently and afresh each time. Passage 1 (probability $.3$) reaches food in 2 minutes; passage 2 (probability $.5$) returns it to the start after 3 minutes; passage 3 (probability $.2$) returns it after 5 minutes. Find the expected time to reach food.
> (ii) A shop serves $N\sim\text{Poisson}(30)$ customers a day; each spends an amount with mean \$25 and standard deviation \$10, independently of everything else. Find the mean and standard deviation of the day's takings.
> (iii) Repeat (ii) supposing the shop serves **exactly** 30 customers. Compare, and say which source of variability dominates.

> [!example]- Solution
> **(i)** Condition on the first choice. Returning to the start resets the problem, so the *remaining* expected time is again $\mathbb{E}[T]$:
> $$\mathbb{E}[T]=.3(2)+.5(3+\mathbb{E}[T])+.2(5+\mathbb{E}[T])$$
> $$\mathbb{E}[T]=3.1+0.7\,\mathbb{E}[T]\quad\Longrightarrow\quad \mathbb{E}[T]=\frac{3.1}{0.3}=\boxed{10.33\text{ minutes}}$$
> **Compare the average passage duration, $3.1$ minutes.** The answer is more than three times larger, because the rat keeps re-entering the same bad passages. **The multiplier is $1/P(\text{escape})=1/0.3$.**
>
> **(ii)** With $\mathbb{E}[N]=\mathrm{Var}(N)=30$, $\mathbb{E}[X]=25$, $\mathrm{Var}(X)=100$:
> $$\mathbb{E}\!\left[\sum_1^N X_i\right]=30\times25=\boxed{\$750}$$
> $$\mathrm{Var}=\underbrace{30\times100}_{3{,}000}+\underbrace{25^2\times30}_{18{,}750}=21{,}750\quad\Longrightarrow\quad \mathrm{SD}=\boxed{\$147.48}$$
>
> **(iii)** With $N\equiv30$ the second term vanishes: $\mathrm{Var}=3{,}000$, $\mathrm{SD}=\$54.77$.
>
> > [!warning] **The number of customers contributes 86% of the variance**
> > $18{,}750/21{,}750=.862$. **Uncertainty in *how many* customers arrive matters roughly six times more than uncertainty in *how much each spends*** — and ignoring it understates the standard deviation by a factor of 2.7.
> >
> > **The general rule from $\mathrm{Var}=\mathbb{E}[N]\mathrm{Var}(X)+(\mathbb{E}[X])^2\mathrm{Var}(N)$:** the count term is multiplied by the *square of the mean*, so whenever individual amounts are large relative to their own spread, **count variability dominates.** This is why insurers model claim *frequency* at least as carefully as claim *severity*.

> [!question] Exercise 4 — moment generating functions
> (i) A random variable has $M(t)=(0.4e^t+0.6)^{15}$. Identify its distribution, mean and variance.
> (ii) $Y$ has $M_Y(t)=e^{2(e^t-1)}(1-2t)^{-3}$ for $t<\tfrac12$. What is $Y$? Find $\mathbb{E}[Y]$ and $\mathrm{Var}(Y)$.
> (iii) Derive $\mathbb{E}[X]$ and $\mathrm{Var}(X)$ for $X\sim\text{Exp}(\lambda)$ from $M(t)=\lambda/(\lambda-t)$.
> (iv) Use the normal MGF to show $\mathbb{E}[e^X]=e^{\mu+\sigma^2/2}$ for $X\sim N(\mu,\sigma^2)$, and say what this means for a lognormal.

> [!example]- Solution
> **(i)** This is $(pe^t+1-p)^n$ with $p=0.4$, $n=15$: **Binomial$(15, 0.4)$**, so $\mathbb{E}=6$, $\mathrm{Var}=15(.4)(.6)=\boxed{3.6}$.
> **Recognition beats differentiation** — the whole point of the uniqueness theorem.
>
> **(ii)** A **product** of MGFs means a **sum of independent** variables:
> $$e^{2(e^t-1)}\to\text{Poisson}(2),\qquad (1-2t)^{-3}=(1-2t)^{-6/2}\to\chi^2_6$$
> So $Y=P+C$ with $P\sim\text{Poisson}(2)\perp C\sim\chi^2_6$, and
> $$\mathbb{E}[Y]=2+6=\boxed{8},\qquad \mathrm{Var}(Y)=2+12=\boxed{14}$$
> *(Note $Y$ is neither discrete nor continuous — exactly the sort of variable §7c's Stieltjes integral exists for.)*
>
> **(iii)** $M'(t)=\dfrac{\lambda}{(\lambda-t)^2}$, $M''(t)=\dfrac{2\lambda}{(\lambda-t)^3}$, so
> $$\mathbb{E}[X]=M'(0)=\tfrac1\lambda,\qquad \mathbb{E}[X^2]=M''(0)=\tfrac2{\lambda^2},\qquad \mathrm{Var}=\tfrac2{\lambda^2}-\tfrac1{\lambda^2}=\boxed{\tfrac1{\lambda^2}}$$
> **$M(t)$ exists only for $t<\lambda$** — the MGF's domain is not incidental; a distribution whose MGF is finite near 0 has all moments and exponentially light tails, which is why the Cauchy has no MGF at all.
>
> **(iv)** $M_X(t)=\exp\{\mu t+\sigma^2t^2/2\}$, so $\mathbb{E}[e^X]=M_X(1)=e^{\mu+\sigma^2/2}$.
>
> > [!warning] The lognormal trap, in one formula
> > If $\log Y\sim N(\mu,\sigma^2)$ then $\mathbb{E}[Y]=e^{\mu+\sigma^2/2}$, **not $e^\mu$** — and $e^\mu$ is the *median*.
> > $$\frac{\text{mean}}{\text{median}}=e^{\sigma^2/2}$$
> > With $\sigma=1$ the mean is 65% above the median. **Fitting a model in logs and exponentiating the fitted value gives the median, not the mean** — the $e^{\sigma^2/2}$ correction is exactly Jensen's inequality ([[05 - Continuous Random Variables|ch. 05]]) made quantitative, and forgetting it systematically understates levels in [[Econometrics/contents/00-Index|Econometrics]].

> [!question] Exercise 5 — prediction *(hard)*
> **(a)** A signal $S\sim N(10,\,4)$ is transmitted and received as $R=S+W$ with $W\sim N(0,1)$ independent. The value $r=12$ is received.
> (i) Find the best predictor of $S$ and its mean squared error.
> (ii) Express the answer as a weighted average and interpret the weights.
>
> **(b)** Let $X\sim U(0,1)$ and $Y=X^2$ — an **exactly deterministic** relationship.
> (i) Find $\mathbb{E}[Y\mid X]$ and its MSE.
> (ii) Find $\rho(X,Y)$.
> (iii) Find the best *linear* predictor of $Y$ and its MSE.
> (iv) Verify the conditional variance formula on this example.
> (v) What is the moral?

> [!example]- Solution
> **(a)(i)** By Example 6b with $\mu=10$, $\sigma^2=4$, $r=12$:
> $$\mathbb{E}[S\mid R=12]=\frac{\mu+r\sigma^2}{1+\sigma^2}=\frac{10+48}{5}=\boxed{11.6},\qquad \mathrm{Var}(S\mid R)=\frac{\sigma^2}{1+\sigma^2}=\frac45=\boxed{0.8}$$
>
> **(ii)** $11.6=0.2\times10+0.8\times12$. **The weights are $\frac{1}{1+\sigma^2}$ on the prior mean and $\frac{\sigma^2}{1+\sigma^2}$ on the observation — inversely proportional to the two variances** (1 for the noise, 4 for the signal). The channel is clean relative to the signal's own spread, so the data get 80% of the weight.
>
> **Two things to notice.** The estimate $11.6$ lies **strictly between** $10$ and $12$ — the observation is **shrunk toward the prior**, which is what "shrinkage estimator" means. And the posterior variance $0.8$ is **smaller than both** the prior variance (4) and the noise variance (1): combining two noisy sources beats either alone.
>
> **(b)(i)** $\mathbb{E}[Y\mid X]=\mathbb{E}[X^2\mid X]=X^2=Y$ exactly, so the MSE is $\boxed{0}$. **The best predictor is perfect.**
>
> **(ii)** With $\mathbb{E}[X^k]=\tfrac1{k+1}$:
> $$\mathrm{Var}(X)=\tfrac1{12},\quad \mathbb{E}[Y]=\tfrac13,\quad \mathrm{Var}(Y)=\tfrac15-\tfrac19=\tfrac4{45},\quad \mathrm{Cov}(X,Y)=\tfrac14-\tfrac12\cdot\tfrac13=\tfrac1{12}$$
> $$\rho^2=\frac{(1/12)^2}{(1/12)(4/45)}=\frac{15}{16}\quad\Longrightarrow\quad \rho=\frac{\sqrt{15}}4=\boxed{.9682}$$
>
> **(iii)** $b=\dfrac{\mathrm{Cov}}{\mathrm{Var}(X)}=\dfrac{1/12}{1/12}=1$ and $a=\tfrac13-\tfrac12=-\tfrac16$, so
> $$\hat Y_{\text{lin}}=X-\tfrac16,\qquad \text{MSE}=\sigma_y^2(1-\rho^2)=\tfrac4{45}\cdot\tfrac1{16}=\boxed{\tfrac1{180}\approx.00556}$$
>
> **(iv)** $\mathrm{Var}(Y\mid X)=0$ (given $X$, $Y$ is determined), so
> $$\mathrm{Var}(Y)=\underbrace{\mathbb{E}[\mathrm{Var}(Y\mid X)]}_{0}+\underbrace{\mathrm{Var}(\mathbb{E}[Y\mid X])}_{\mathrm{Var}(X^2)=4/45}=\tfrac4{45}\ ✓$$
> **All of the variance is "between-group" and none is "within-group"** — the signature of a deterministic relationship.
>
> **(v)**
> > [!warning] $\rho$ measures *linearity*, not *dependence* — and $\rho=.97$ is not "almost perfect"
> > The relationship here is **exactly deterministic**: $Y$ is a function of $X$ with zero error. **Yet $\rho=.968$, not 1**, and the best linear predictor still has positive MSE. $\rho=1$ requires an exactly *straight-line* relationship, not merely an exact one.
> >
> > **Run the comparison the other way and it is worse.** A high $\rho$ is not evidence that a linear model is adequate — and $\rho=0$ is not evidence of independence ($Y=X^2$ with $X$ symmetric about 0 gives $\rho=0$ with the same perfect determinism). **The number $\rho$ answers exactly one question: how well does a straight line fit?**
> >
> > **The practical rule: plot the data.** A residual-versus-fitted plot would show the curvature here instantly, while $R^2=.94$ would not. This is the [[Data Preparation and Visualization/contents/00-Index|Data Prep & Visualization]] lesson stated in probability.

---

## 📝 Summary

- **$\mathbb{E}[\sum X_i]=\sum\mathbb{E}[X_i]$ always — no independence required.** This is the most under-used fact in probability. Variance is different: $\mathrm{Var}(\sum X_i)=\sum\mathrm{Var}(X_i)+2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$, and only pairwise-uncorrelated variables let the cross terms go.
- **The indicator trick handles almost every "expected number of…" problem:** write $X=\sum\mathbb{1}_{A_i}$ and read off $\mathbb{E}[X]=\sum P(A_i)$. It gives the binomial, negative binomial and hypergeometric means in one line each; the **matching problem's mean of exactly 1**; the **coupon collector's $N\log N$**; and quicksort's **$2n\log n$** average comparisons.
- **The same trick gives higher moments:** $\mathbb{E}\!\left[\binom Xk\right]=\sum_{i_1<\dots<i_k}P(A_{i_1}\cdots A_{i_k})$. For the matching problem *every* factorial moment is 1 — the fingerprint of a Poisson(1).
- **The probabilistic method proves existence by averaging:** $\max_s f(s)\ge\mathbb{E}[f(S)]$, with strict inequality unless $f(S)$ is constant. Non-constructive, and often the only available argument.
- **$\mathrm{Cov}(X,Y)=\mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y]$ is bilinear**, and $\rho=\mathrm{Cov}/(\sigma_x\sigma_y)\in[-1,1]$ with $|\rho|=1$ iff $Y=a+bX$ exactly. **Independence $\Rightarrow$ $\rho=0$; the converse is false** except for the bivariate normal.
- **$\mathbb{E}[S^2]=\sigma^2$ is why we divide by $n-1$** — the sample sits closer to its own mean than to $\mu$, and the identity $\sum(X_i-\bar X)^2=\sum(X_i-\mu)^2-n(\bar X-\mu)^2$ measures the shortfall exactly.
- **The finite-population correction $\frac{N-n}{N-1}$ is $\approx1$ whenever $N\gg n$** — so poll precision depends on the *sample* size, not on the population size.
- **$\mathbb{E}[X\mid Y]$ is a random variable, and $\mathbb{E}[X]=\mathbb{E}[\mathbb{E}[X\mid Y]]$.** Conditioning solves the miner (15 hours), the random sum ($\mathbb{E}[N]\mathbb{E}[X]$), gambler's ruin among $r$ players ($\frac12(n^2-\sum n_i^2)$), and the secretary problem ($1/e$).
- **The conditional variance formula $\mathrm{Var}(X)=\mathbb{E}[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(\mathbb{E}[X\mid Y])$ splits variation into within- and between-group parts.** For a random sum this gives $\mathbb{E}[N]\mathrm{Var}(X)+(\mathbb{E}[X])^2\mathrm{Var}(N)$ — **and the second term usually dominates.**
- **$\mathbb{E}[Y\mid X]$ is the minimiser of $\mathbb{E}[(Y-g(X))^2]$ over all functions $g$.** Restricting to linear $g$ gives $\mu_y+\rho\frac{\sigma_y}{\sigma_x}(X-\mu_x)$ with MSE $\sigma_y^2(1-\rho^2)$ — **equal to the best predictor only when $\mathbb{E}[Y\mid X]$ happens to be linear**, as it is for the bivariate normal.
- **$M(t)=\mathbb{E}[e^{tX}]$ generates moments by differentiation, turns independent sums into products, and determines the distribution uniquely.** All four convolution-closure results become one-line MGF multiplications, and the shared-parameter conditions become visible.
- **Multivariate normal distributions are determined entirely by their mean vector and covariance matrix.** Hence, for them, **zero covariance is independence**.
- **Proposition 8.1:** for i.i.d. normals, $\bar X\sim N(\mu,\sigma^2/n)$, $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$, **and the two are independent.** This is precisely what makes $\frac{\bar X-\mu}{S/\sqrt n}$ a $t_{n-1}$ variable, and hence what makes the $t$-test valid.

---

## ⚠️ Important Notes

> [!warning] Linearity is free; everything else has conditions
> | Statement | Needs independence? |
> |---|---|
> | $\mathbb{E}[X+Y]=\mathbb{E}[X]+\mathbb{E}[Y]$ | **No** |
> | $\mathbb{E}[XY]=\mathbb{E}[X]\mathbb{E}[Y]$ | **Yes** (uncorrelated suffices) |
> | $\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)$ | **Yes** (uncorrelated suffices) |
> | $M_{X+Y}=M_XM_Y$ | **Yes** |
>
> **The first row is why the indicator trick works on wildly dependent events**, and why the matching problem has mean 1 without any of the hard combinatorics.

> [!warning] $\rho=0$ is not independence, and $\rho^2$ — not $\rho$ — is "variance explained"
> **Two separate errors that travel together.**
>
> - $\mathrm{Cov}=0$ detects only the *linear* component. Ross's counterexample has $Y$ a deterministic function of $X$ and $\rho=0$. **Exercise 5 has $\rho=.968$ with a perfect deterministic relationship** — so $\rho$ fails in both directions.
> - **"$\rho=0.5$ means half the variation is explained" is wrong: $\rho^2=0.25$.** And "explained" is not causal — $\rho$ is symmetric in its arguments.
>
> **The remedy is a scatterplot, every time.** Curvature, outliers, and non-constant spread are all invisible to $\rho$.

> [!warning] For a random sum, the count usually contributes most of the variance
> $$\mathrm{Var}\!\left(\sum_{i=1}^N X_i\right)=\mathbb{E}[N]\,\mathrm{Var}(X)+(\mathbb{E}[X])^2\,\mathrm{Var}(N)$$
> **The second term carries $(\mathbb{E}[X])^2$**, so whenever individual values are large relative to their spread it dominates — **86% of the variance in Exercise 3.** Treating $N$ as fixed at its mean understated the standard deviation by a factor of 2.7 there.
>
> **This is the standard failure in aggregate-loss, demand and capacity modelling:** people model the size of each item carefully and treat the count as known.

> [!warning] The $n-1$ in $S^2$ is a theorem, not a convention
> $$\mathbb{E}\!\left[\frac{\sum(X_i-\bar X)^2}{n-1}\right]=\sigma^2,\qquad \mathbb{E}\!\left[\frac{\sum(X_i-\bar X)^2}{n}\right]=\frac{n-1}n\sigma^2$$
> **Dividing by $n$ is biased low, by exactly the factor $\frac{n-1}n$** — noticeable at $n=5$ (20% low), negligible at $n=1000$.
>
> **The mechanism, stated once:** $\sum(X_i-\bar X)^2=\sum(X_i-\mu)^2-n(\bar X-\mu)^2$. The sample is always *closer to its own mean* than to the true mean, and the second term is exactly how much closer. **One parameter estimated, one degree of freedom gone.**

> [!warning] Squared-error loss targets the conditional *mean*, and that is a choice
> **$\mathbb{E}[Y\mid X]$ is optimal only under squared error.** Change the loss and you change the target:
>
> | Loss | Optimal predictor |
> |---|---|
> | $(Y-g)^2$ | conditional **mean** |
> | $\|Y-g\|$ | conditional **median** |
> | pinball at level $\tau$ | conditional **$\tau$-quantile** |
>
> **For skewed targets — incomes, claim sizes, waiting times — the conditional mean can be a poor summary**, and a model trained on squared error will chase the tail. **Choosing the loss is choosing what question you are answering**, not a technical detail.

> [!warning] The best *linear* predictor is not the best predictor
> $$\hat Y_{\text{lin}}=\mu_y+\rho\frac{\sigma_y}{\sigma_x}(X-\mu_x),\qquad \text{MSE}=\sigma_y^2(1-\rho^2)$$
> **These coincide only when $\mathbb{E}[Y\mid X]$ is genuinely linear in $X$** — guaranteed for the bivariate normal, and not otherwise. In Exercise 5, the true predictor has MSE $0$ and the best linear predictor has MSE $\tfrac1{180}$, **despite $\rho=.968$.**
>
> **Corollary for practice: a linear model can have high $R^2$ and still be the wrong functional form.** $R^2$ compares you to the *mean*, not to the truth.

> [!warning] MGFs need not exist, and where they exist matters
> $M(t)$ must be finite **in an interval around $t=0$** for the uniqueness theorem to apply. The exponential's MGF exists only for $t<\lambda$; **the Cauchy and other heavy-tailed distributions have no MGF at all**, which is precisely why their moments fail to exist and why the LLN breaks for them ([[05 - Continuous Random Variables|ch. 05]], [[08 - Limit Theorems|ch. 08]]).
>
> **Rule of thumb: a finite MGF near 0 means exponentially light tails.** When that fails, use the characteristic function $\mathbb{E}[e^{itX}]$, which always exists.

> [!warning] Independence of $\bar X$ and $S^2$ is a normal-only fact — and the $t$-test depends on it
> Proposition 8.1's third clause is not decoration: **the MGF argument divides $(1-2t)^{-n/2}$ by $(1-2t)^{-1/2}$, which is only legal because the two pieces are independent.** And $\frac{\bar X-\mu}{S/\sqrt n}$ is a $t_{n-1}$ variable only because the numerator's normal and the denominator's $\chi^2$ are independent.
>
> **For non-normal data $\bar X$ and $S^2$ are generally dependent**, so the small-sample $t$ distribution is not exact. **The CLT rescues the test for large $n$ ([[08 - Limit Theorems|ch. 08]]), not for small $n$** — which is where the normality assumption actually bites.

> [!note] Cross-subject connections
> - [[04 - Random Variables|Ch. 04]] / [[05 - Continuous Random Variables|Ch. 05]] — **every mean and variance computed there by summing or integrating is re-derived here in a line** by indicators or MGFs.
> - [[06 - Jointly Distributed Random Variables|Ch. 06]] — §6's MGF products replace §3's convolutions; §5b's bivariate normal is where $\rho$ is *proved* to be the correlation (Example 5f).
> - [[08 - Limit Theorems|Ch. 08]] — **the MGF is the engine of the CLT proof**, and Chebyshev's inequality needs only the variances computed here.
> - [[09 - Additional Topics in Probability|Ch. 09]] — conditional expectation is the definition of a martingale, and the tower property is the tool for Markov chains.
> - [[Mathematical Statistics/contents/05 - Point Estimation|Mathematical Statistics ch. 05]] — **$\mathbb{E}[S^2]=\sigma^2$ is unbiasedness**; §4c is the finite-population correction behind every survey standard error.
> - [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics ch. 07]] — **Proposition 8.1 *is* the $t$-test's validity proof.**
> - [[Econometrics/contents/00-Index|Econometrics]] — §5 is the population regression function; the conditional variance formula is the total/explained/residual sum-of-squares decomposition; Exercise 4(iv) is the log-transform retransformation bias.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **Proposition 6.1 is why squared-error training estimates $\mathbb{E}[Y\mid X]$**; Example 6c is $k$-means; Example 6b is shrinkage and the Kalman update.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — Example 2m is the $O(n\log n)$ average-case analysis of quicksort; the coupon-collector bound recurs throughout randomised algorithms.
> - [[Linear Algebra/contents/00-Index|Linear Algebra]] — the covariance matrix of §7a is symmetric positive semi-definite, and **$\mathrm{Var}(a^\top X)=a^\top\Sigma a\ge0$ is exactly that statement**; PCA is its eigendecomposition.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Source typos** (not extraction artefacts):
> - **The chapter Summary misstates the master variance formula**, printing
> $$\mathrm{Var}\!\left(\sum_i X_i\right)=\sum_i\mathrm{Var}(X_i)+2\sum\sum_{i<j}\mathrm{Cov}(X_i,\mathbf{Y_j})$$
> — **it should be $\mathrm{Cov}(X_i,X_j)$.** The body of §7.4 states it correctly; only the summary is wrong. **This is the most consequential typo in the chapter, because the summary is what gets memorised.**
> - **Example 5n** prints `fY (y} dy` — a brace for a parenthesis.
> - **Example 7j** says "independent of the sequence $X$, $i\ge1$" — should be $X_i$.
> - **Example 2j** (the duck hunters) never states the assumption it uses — that each hunter's target choice is uniform over the 10 ducks, giving $P\{$hunter hits duck $i\}=p/10$. It is stated only as "each chooses his target at random."
>
> **Figures are images and cannot be extracted:**
> - **Figure 7.1** (the two-dimensional random walk showing positions 0, 1, 2 after successive unit steps) extracts as `1 2 0 1 1 0 5 initial position / 1 5 position after first step / 2 5 position after second step` — **where every `5` is a mangled `=`.** The caption is recoverable; the picture of the path is not. **Example 2l's result $\mathbb{E}[D^2]=n$ is fully derived in the text**, so nothing is lost mathematically.
> - **Tables 7.1 and 7.2** (the MGF reference tables) extract with their columns interleaved — e.g. the Poisson row reads `exp{λ(et − 1)} λλ`, which is $M(t)$, mean $\lambda$, variance $\lambda$. **I have reconstructed both tables into a single table in §6 and checked every entry against the derivations in the text.**
> - **The cross-reference in the text to "Tables 7.1 and 7.2 (on page 364)" is wrong** — the tables appear on pages 375 and 377.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and checked against numeric answers):
> - **`…` is `≤`**, **`Ú` is `≥`**, **`q` is `∞`**, **`Z` is `≠`**, **`L` is `≈`**, **`K` is `≡`**, **`*` is `⇔`** (in Example 5k's `g′(x) = 0 * log(n/x) = 1 * x = n/e`, which is $g'(x)=0\iff\log(n/x)=1\iff x=n/e$), and **`;` is `±`** (Example 6c's `i = 0, ;1, ;2,...`). **`50 * $8`** in Example 5d is $50\times\$8$.
> - **Binomial coefficients extract across four lines** and **fractions as numerator-newline-denominator**, as in chapters 1–6.
> - **`/Gamma1` is $\Gamma$, `/Theta1` is $\Theta$, `/Phi1` is $\Phi$** — the same substitutions as earlier chapters. **`ℓ`** survives correctly in Example 4f.
> - **`v_j` is used for $\nu_j$** in the proof of Proposition 4.2 while §4c uses `v_i` for genuine data values — **an unfortunate collision in the source, not the extraction.**
>
> **Verification performed:** every numeric claim in the chapter was independently recomputed. Confirmed: $\mathbb{E}|X-Y|=L/3$ by double integration (2a); the run formulas $\mathbb{E}[R(1)]=3.0$, $\mathbb{E}[R(0)]=2.8$, total $5.8$ **by brute-force enumeration of all $\binom{10}6$ arrangements** (2k); $\mathbb{E}[X]=1$ and $\mathrm{Var}(X)=1$ for the match problem (2h, 3c); $105/52=2.019>2$ (2r); the negative-hypergeometric means $\tfrac{53}{14}=3.786$ for the first spade and $\tfrac{53}5=10.6$ for the first ace (3e); **all four craps figures** — $\mathbb{E}[R]=3.3758$, $p=.49293$ (matching the exact $\tfrac{244}{495}$), $\mathbb{E}[R\mid\text{win}]=2.9383$, $\mathbb{E}[R\mid\text{lose}]=3.8010$ (5e); **Example 5g's formula $\mathbb{E}[N_j\mid N_i>0]=np_j\frac{1-(1-p_i)^{n-1}}{1-(1-p_i)^n}$ against exact enumeration of the multinomial** at $n=4$, $p=(.2,.3,.5)$ — both $.99187$; **Example 5i's $\mathbb{E}[X]=\tfrac12(n^2-\sum n_i^2)$ against 200,000 simulations** for $r=3$, $n=(1,1,2)$ — formula $5$, simulated $5.005$; and $1/e=.36788$ (5k). **All agree with the text; no arithmetic errors were found in this chapter.**
>
> **One scope note:** §§7.2.1 (the probabilistic method), 7.2.2 (the max–min identity) and 7.9 (Stieltjes integrals) are starred as optional. **I have kept 7.2.1 in full** — it is a genuinely different proof technique and appears constantly in algorithm analysis — **and reduced 7.2.2 and 7.9 to short notes.** The max–min identity's main payoff, coupon collecting with unequal probabilities, is more usefully learned in its integral form $\mathbb{E}[X]=\int_0^\infty\!\big(1-\prod_i(1-e^{-p_ix})\big)dx$, which the source gives at the end of Example 2s.

#probability #expectation #covariance #correlation #conditional-expectation #variance-decomposition #mgf #multivariate-normal #prediction
