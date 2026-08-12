---
subject: Probability Theory
chapter: 09
tags: [ds, probability, poisson-process, markov-chain, stationary-distribution, entropy, information-theory, coding]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 9 (pp. 442–461)"
---

# Additional Topics in Probability

> [!abstract] What this chapter is for
> **Four topics that each open onto a whole field.** Chapters 1–8 studied random *variables*; this chapter studies random **processes** — collections of random variables indexed by time — and then makes a sharp turn into **information theory**.
>
> | § | Topic | Opens onto |
> |---|---|---|
> | **1** | **The Poisson process** | queueing theory, reliability, arrival modelling |
> | **2** | **Markov chains** | stochastic processes, MCMC, PageRank, reinforcement learning |
> | **3** | **Entropy** | information theory, decision trees, cross-entropy loss |
> | **4** | **Coding theory** | compression, error-correcting codes, channel capacity |
>
> **The unifying thread is that all four are payoffs on machinery already built.** The Poisson process is the exponential's memorylessness ([[05 - Continuous Random Variables|ch. 05]]) plus Poisson thinning ([[06 - Jointly Distributed Random Variables|ch. 06]]). Markov chains are conditional distributions ([[06 - Jointly Distributed Random Variables|ch. 06 §4]]) iterated, with the strong law ([[08 - Limit Theorems|ch. 08]]) supplying the long-run interpretation. **Entropy is an expectation** — of $-\log p$.
>
> **§3–4 are the theoretical origin of cross-entropy loss**, the objective function behind essentially every classifier in [[Machine Learning/contents/00-Index|Machine Learning]].

---

## 📘 Main Knowledge

### 1. The Poisson process

Write $f(h)=o(h)$ when $\lim_{h\to0}f(h)/h=0$ — "negligible even compared with $h$."

> [!important] Definition
> $\{N(t),\,t\ge0\}$, counting events in $[0,t]$, is a **Poisson process with rate $\lambda$** if
>
> | | Condition | Name |
> |---|---|---|
> | (i) | $N(0)=0$ | starts at zero |
> | (ii) | counts in disjoint intervals are **independent** | independent increments |
> | (iii) | the distribution of a count depends only on the interval's **length** | stationary increments |
> | (iv) | $P\{N(h)=1\}=\lambda h+o(h)$ | events occur at rate $\lambda$ |
> | (v) | $P\{N(h)\ge2\}=o(h)$ | **events occur one at a time** |

**Everything else follows from these five local assumptions.**

> [!tip] Reading the axioms as modelling assumptions
> Each condition is a substantive claim about the world, and each can fail:
> - **(ii) independent increments** fails when arrivals cluster — a rumour, a viral post, an outage cascade.
> - **(iii) stationary increments** fails whenever there is a rush hour. **This is the most commonly violated assumption in practice**, and the fix is a *non-homogeneous* Poisson process with a time-varying $\lambda(t)$.
> - **(v) one at a time** fails when arrivals come in batches — a bus of customers, a burst of packets.
>
> **Before fitting a Poisson model, ask which of these five is being assumed away.**

**Lemma 1.1** ($P\{N(t)=0\}=e^{-\lambda t}$) comes from a differential equation: $P_0(t+h)=P_0(t)[1-\lambda h+o(h)]$ gives $P_0'(t)=-\lambda P_0(t)$, hence $P_0(t)=e^{-\lambda t}$.

> [!important] The three descriptions are equivalent
> | Object | Distribution |
> |---|---|
> | **Counts** $N(t)$ | Poisson$(\lambda t)$ |
> | **Interarrival times** $T_1,T_2,\dots$ | i.i.d. Exponential$(\lambda)$ (Proposition 1.1) |
> | **Arrival times** $S_n=\sum_{i\le n}T_i$ | Gamma$(n,\lambda)$ |
>
> **The bridge between counts and times is the single most useful identity:**
> $$N(t)\ge n\iff S_n\le t$$
> — "at least $n$ events by time $t$" and "the $n$th event happened by time $t$" are *the same event*. Theorem 1.1 ($P\{N(t)=n\}=e^{-\lambda t}(\lambda t)^n/n!$) is this identity plus one integration by parts.

> [!tip] Why exponential interarrivals, intuitively
> $P\{T_1>t\}=P\{N(t)=0\}=e^{-\lambda t}$ — immediately exponential. And **independence of $T_2$ from $T_1$ is the independent-increments assumption**, which is the process-level version of **memorylessness** ([[05 - Continuous Random Variables|ch. 05]]).
>
> **The circle closes here.** Ch. 05 showed the exponential is the *unique* memoryless distribution; ch. 06 showed Poisson thinning and that arrivals conditioned on the count are uniform order statistics. **All of it is the same object viewed from different angles**, and the Poisson process is that object.

> [!example] Two facts worth having at your fingertips
> - **Conditional on $N(t)=n$, the $n$ arrival times are distributed as the order statistics of $n$ i.i.d. $U(0,t)$** ([[06 - Jointly Distributed Random Variables|ch. 06 §7]], Example 7e). **$\lambda$ disappears** — given how many arrived, *when* they arrived carries no rate information. This is the sharpest statement of "completely at random in time."
> - **Superposition and thinning.** Independent Poisson processes with rates $\lambda_1,\lambda_2$ superpose to a Poisson process with rate $\lambda_1+\lambda_2$; independently marking each event with probability $p$ splits one process into **independent** processes with rates $\lambda p$ and $\lambda(1-p)$ ([[06 - Jointly Distributed Random Variables|ch. 06 §2]], Example 2b).

---

### 2. Markov chains

> [!important] Definition
> $X_0,X_1,\dots$ taking values in $\{0,1,\dots,M\}$ is a **Markov chain** with transition probabilities $P_{ij}$ if
> $$P\{X_{n+1}=j\mid X_n=i,\ X_{n-1}=i_{n-1},\dots,X_0=i_0\}=P_{ij}$$
> **The past is irrelevant given the present.** Necessarily $P_{ij}\ge0$ and $\sum_j P_{ij}=1$ — **each row of the transition matrix is a probability distribution.**

The joint distribution factors into a product along the path:

$$P\{X_0=i_0,\dots,X_n=i_n\}=P\{X_0=i_0\}\,P_{i_0i_1}P_{i_1i_2}\cdots P_{i_{n-1}i_n}$$

> [!warning] "Memoryless" here means something different from ch. 05
> **The Markov property does not say the past has no effect** — it says the past acts **only through the current state**. If $X_n$ encodes enough, arbitrarily long-range dependence is compatible with the Markov property.
>
> **The standard trick: enlarge the state space.** Weather depending on the last *two* days is not Markov on $\{$rain, dry$\}$ — **but it is Markov on the four states $\{$(rain,rain), (rain,dry), (dry,rain), (dry,dry)$\}$.** *"Is it Markov?"* is really *"Markov with respect to which state description?"*, and the answer can always be made yes at the price of a bigger state space. **That price is the curse of dimensionality**, and it is why the question matters.

> [!example] Four standard chains
> | Chain | States | Transitions |
> |---|---|---|
> | **Weather (2a)** | rain / dry | $P_{00}=\alpha$, $P_{10}=\beta$ |
> | **Gambler's ruin (2b)** | fortune $0,\dots,M$ | $P_{i,i+1}=p=1-P_{i,i-1}$; $P_{00}=P_{MM}=1$ |
> | **Ehrenfest urns (2c)** | molecules in urn 1 | $P_{i,i+1}=\frac{M-i}M$, $P_{i,i-1}=\frac iM$ |
> | **Random walk (2d)** | all integers | $P_{i,i+1}=p=1-P_{i,i-1}$ |
>
> **The Ehrenfest chain is a model of diffusion** — pick a random molecule and move it to the other urn — and it is the standard toy demonstration of how irreversible-looking macroscopic behaviour (equalisation) arises from reversible microscopic rules.

#### 2a. Chapman–Kolmogorov and the limiting distribution

$$P^{(n)}_{ij}=P\{X_{n+m}=j\mid X_m=i\},\qquad \boxed{P^{(n)}_{ij}=\sum_{k}P^{(r)}_{ik}P^{(n-r)}_{kj}}\quad\text{for }0<r<n$$

**In matrix language this says $\mathbf{P}^{(n)}=\mathbf{P}^n$** — $n$-step transitions are the $n$th matrix power. *(That is why linear algebra is the natural language for Markov chains; see [[Linear Algebra/contents/00-Index|Linear Algebra]].)*

> [!important] Theorem 2.1 — the limiting/stationary distribution
> A chain is **ergodic** if $P^{(n)}_{ij}>0$ for all $i,j$ for some $n$. For an ergodic chain, $\pi_j=\lim_{n\to\infty}P^{(n)}_{ij}$ exists, **does not depend on the starting state $i$**, and the $\pi_j$ are the unique non-negative solution of
> $$\pi_j=\sum_{k=0}^{M}\pi_k P_{kj},\qquad \sum_{j=0}^{M}\pi_j=1$$

**Read the balance equation as bookkeeping:** the long-run rate of entering state $j$ is the sum, over all $k$, of (time spent in $k$) × (rate of moving $k\to j$). **In matrix form, $\boldsymbol\pi=\boldsymbol\pi\mathbf P$ — $\boldsymbol\pi$ is a left eigenvector of $\mathbf P$ with eigenvalue 1.**

> [!tip] $\pi_j$ is also the long-run *fraction of time* in state $j$
> This second interpretation comes from the **strong law of large numbers** ([[08 - Limit Theorems|ch. 08]]), and it is **valid even when the chain is not ergodic** — which matters, because periodic chains have no limit $\lim_n P^{(n)}_{ij}$ but do have long-run proportions.
>
> **This is the fact that makes MCMC possible:** to sample from a hard distribution $\pi$, build a chain whose stationary distribution is $\pi$ and run it. **The samples are not independent, but their time-average converges to the right answer.**

> [!example] Example 2e — the weather chain
> With $P_{00}=\alpha$ (rain follows rain) and $P_{10}=\beta$ (rain follows dry):
> $$\pi_0=\frac{\beta}{1+\beta-\alpha},\qquad \pi_1=\frac{1-\alpha}{1+\beta-\alpha}$$
> With $\alpha=.6$, $\beta=.3$: $\pi_0=\tfrac37$ — **it rains 3 days in 7 in the long run, regardless of today's weather.**
>
> **A useful closed form for the two-state chain:** the non-unit eigenvalue is $\alpha-\beta$, so
> $$P^{(n)}_{00}=\pi_0+(1-\pi_0)(\alpha-\beta)^n$$
> **The memory of the initial state decays geometrically at rate $|\alpha-\beta|$** — the *second* eigenvalue governs how fast a chain forgets, which in MCMC is the mixing time.

> [!example] Example 2f — the Ehrenfest stationary distribution
> $$\pi_j=\binom Mj\left(\tfrac12\right)^M,\qquad j=0,\dots,M$$
> — **exactly Binomial$(M,\tfrac12)$**, as though each molecule independently chose an urn by a fair coin. **The overwhelming majority of the time the two urns are nearly balanced**, which is the probabilistic content of the second law of thermodynamics: equalisation is not forced, merely overwhelmingly likely.
>
> > [!warning]- But the Ehrenfest chain is **not** ergodic in Ross's sense
> > The number of molecules changes by exactly $\pm1$ each step, **so parity alternates and $P^{(n)}_{ij}=0$ whenever $n$ and $j-i$ have opposite parity.** Condition (2.1) therefore fails for **every** $n$, and $\lim_n P^{(n)}_{ij}$ **does not exist** — the chain is *periodic with period 2*.
> >
> > **Ross nonetheless invokes Theorem 2.1 here.** The conclusion is still correct, but by the *other* justification he gives — $\pi_j$ as a long-run proportion of time, which he explicitly notes holds without ergodicity. **The stated proof does not apply; the result does.** *(Flagged in the gaps callout.)*

---

### 3. Surprise, uncertainty, and entropy

**How surprised should you be that an event of probability $p$ occurred?** Ross derives the answer from four axioms on a surprise function $S(p)$:

| | Axiom | Meaning |
|---|---|---|
| 1 | $S(1)=0$ | certainty is not surprising |
| 2 | $S$ strictly decreasing | rarer is more surprising |
| 3 | $S$ continuous | small change in $p$, small change in surprise |
| 4 | $S(pq)=S(p)+S(q)$ | **surprise from independent events adds** |

> [!important] Theorem 3.1
> Axioms 1–4 force $$S(p)=-C\log_2 p$$ for a positive constant $C$; taking $C=1$ measures surprise in **bits**.

**Axiom 4 is where the logarithm comes from** — it is the only continuous function turning products into sums. **The choice is not arbitrary: it is forced.**

$$\boxed{\ H(X)=-\sum_{i=1}^n p_i\log_2 p_i\ }\qquad(0\log0:=0)$$

> [!tip] Three readings of the same number
> | Reading | $H(X)$ is… |
> |---|---|
> | **Surprise** | the average surprise on learning $X$ |
> | **Uncertainty** | how much you don't know about $X$ beforehand |
> | **Information** | how much you learn by observing $X$ |
>
> **These are one quantity seen from three sides**, and §4 adds a fourth, entirely operational reading: **the minimum average number of bits needed to transmit $X$.**

**$H(X)$ is maximised when all $p_i$ are equal**, at $H=\log_2 n$ — maximum uncertainty is uniform, as intuition demands.

**Joint and conditional entropy:**

$$H(X,Y)=-\sum_i\sum_j p(x_i,y_j)\log p(x_i,y_j),\qquad H_Y(X)=\sum_j H_{Y=y_j}(X)\,p_Y(y_j)$$

> [!important] The two structural theorems
> **Proposition 3.1 (chain rule):** $\ H(X,Y)=H(Y)+H_Y(X)$
> — *the uncertainty in the pair is the uncertainty in $Y$ plus what remains in $X$ once $Y$ is known.*
>
> **Theorem 3.2 (information never hurts):** $\ H_Y(X)\le H(X)$, **with equality iff $X$ and $Y$ are independent.**

**Theorem 3.2's proof is the workhorse inequality $\ln x\le x-1$ (Lemma 3.1)** applied to $p(x_i)/p(x_i\mid y_j)$ — the same device that proves the noiseless coding theorem in §4, and, in modern language, that relative entropy (KL divergence) is non-negative.

> [!tip] The quantity $H(X)-H_Y(X)$ has a name
> It is the **mutual information** $I(X;Y)$: how much observing $Y$ reduces uncertainty about $X$. **Theorem 3.2 says $I(X;Y)\ge0$, with equality exactly under independence** — so mutual information is a *dependence* measure that, unlike correlation ([[07 - Properties of Expectation|ch. 07]]), detects **any** kind of dependence, not merely linear.
>
> **This is the split criterion in decision-tree learning ("information gain")** and the definition of channel capacity in §4.

---

### 4. Coding theory and entropy

Encode each value of $X$ as a binary string, with the **prefix condition**: no codeword is an extension of another. *(Without it, `0`, `1`, `00`, `01` is ambiguous — a received `001` cannot be parsed.)*

> [!example] Two codes for the same variable
> $P=(\tfrac12,\tfrac14,\tfrac18,\tfrac18)$ on $x_1,\dots,x_4$:
>
> | Code | $x_1$ | $x_2$ | $x_3$ | $x_4$ | Average bits |
> |---|---|---|---|---|---|
> | Fixed-length | `00` | `01` | `10` | `11` | $2$ |
> | Variable-length | `0` | `10` | `110` | `111` | $\tfrac12(1)+\tfrac14(2)+\tfrac18(3)+\tfrac18(3)=\mathbf{1.75}$ |
>
> **Give the common outcomes the short codewords.** This is Morse code's principle, and it is the entire idea of compression.

> [!important] Lemma 4.1 — the Kraft inequality
> A prefix code with codeword lengths $n_1,\dots,n_N$ exists **if and only if**
> $$\sum_{i=1}^N\left(\tfrac12\right)^{n_i}\le1$$
> **This converts a combinatorial question ("does such a code exist?") into an arithmetic one.**

> [!important] Theorem 4.1 — the noiseless coding theorem
> For **any** prefix code assigning $n_i$ bits to $x_i$,
> $$L=\sum_i n_i\,p(x_i)\ \ge\ H(X)$$
> **Entropy is a hard floor on compression.** Moreover, choosing $n_i=\lceil-\log_2 p(x_i)\rceil$ always achieves
> $$H(X)\le L<H(X)+1$$

**This is the fourth reading of entropy, and the one that makes it a physical quantity rather than a definition:** $H(X)$ is *the* number of bits per symbol, achievable to within 1 and not improvable.

> [!example] Example 4a — the bound is attained
> For $P=(\tfrac12,\tfrac14,\tfrac18,\tfrac18)$, $H(X)=1.75$ exactly, and the variable-length code above achieves $L=1.75$. **No scheme can do better.** *(Equality holds precisely when every $p_i$ is a power of $\tfrac12$ — then $-\log_2 p_i$ is already an integer and no rounding is needed.)*

> [!example] Example 4b — compressing a biased coin
> Ten independent flips with $P(\text{heads})=p$. Since the flips are independent, $H(X)=10\,H(p)$:
> - **$p=\tfrac12$: $H=10$ bits.** **No compression is possible** — send the raw 10 bits. **A fair coin is incompressible.**
> - **$p=\tfrac14$: $H=8.11$ bits**, so some code achieves $L<9.11$. Coding *pairs* of flips as `0`/`10`/`110`/`111` gives
> $$L=5\left[1\cdot\tfrac9{16}+2\cdot\tfrac3{16}+3\cdot\tfrac3{16}+3\cdot\tfrac1{16}\right]=\tfrac{135}{16}=8.44\text{ bits}$$
> **Coding in blocks beats coding symbol by symbol** — and taking longer and longer blocks drives $L$ down toward $H$. **That is the whole idea behind every modern compressor.**
>
> **The moral: compressibility is exactly departure from uniformity.** Data with no structure cannot be compressed, and "this file compressed by 60%" is a measurement of its entropy.

#### 4a. Noisy channels

A **binary symmetric channel** transmits each bit correctly with probability $p$, independently. With $p=.8$, the raw bit-error rate is $.20$.

**Repetition coding** — send each bit 3 times, decode by majority — reduces the error to $(.2)^3+3(.2)^2(.8)=.104$, and 17 repetitions reduce it to $.0026$. **But the transmission rate falls to $\tfrac13$ and $\tfrac1{17}$.**

| Repetitions | Error per bit | Rate |
|---|---|---|
| 1 | $.20$ | $1$ |
| 3 | $.104$ | $.33$ |
| 17 | $.0026$ | $.059$ |

> [!important] Theorem 4.2 — Shannon's noisy coding theorem
> **There is a number $C^*$ — the channel capacity — such that for any rate $R<C^*$ and any $\varepsilon>0$, some coding–decoding scheme achieves rate $R$ with per-bit error below $\varepsilon$.** For the binary symmetric channel,
> $$C^*=1+p\log_2 p+(1-p)\log_2(1-p)=1-H(p)$$

> [!tip] Why this is one of the great results of the twentieth century
> **The table above suggests an inescapable trade-off: driving error to 0 drives rate to 0.** Shannon proved that intuition wrong. **Below capacity, arbitrarily reliable communication is possible at a fixed positive rate.**
>
> With $p=.8$, $C^*=.278$ — **so a rate of $0.27$ with essentially zero error is achievable**, whereas repetition coding needed rate $.059$ for an error of only $.0026$. **Repetition is a spectacularly bad code**, and the theorem says vastly better ones exist. *(It does not say what they are; constructing capacity-approaching codes took another fifty years, ending with turbo and LDPC codes.)*
>
> **And notice $C^*=1-H(p)$:** capacity is one bit per use *minus the entropy the noise injects.* Entropy is not an analogy here — it is the accounting unit.

---

## ✏️ Exercises

> [!question] Exercise 1 — the Poisson process *(warm-up)*
> Calls arrive at a helpdesk according to a Poisson process with rate $\lambda=4$ per hour.
>
> (i) Find $P\{\text{no calls in a given 30-minute period}\}$.
> (ii) Find $P\{\text{exactly 3 calls in a 2-hour period}\}$.
> (iii) Find the expected time until the 5th call, and the distribution of that time.
> (iv) Given that exactly 2 calls arrived in the first hour, find the probability that **both** arrived in the first 20 minutes.
> (v) Same conditioning: find the probability that **at least one** arrived in the first 30 minutes.

> [!example]- Solution
> **(i)** $N(0.5)\sim\text{Poisson}(4\times0.5=2)$, so $P\{N(.5)=0\}=e^{-2}=\boxed{.1353}$.
>
> **(ii)** $N(2)\sim\text{Poisson}(8)$, so $P\{N(2)=3\}=e^{-8}\dfrac{8^3}{3!}=\boxed{.0286}$.
>
> **(iii)** $S_5\sim\Gamma(5,4)$, so $\mathbb{E}[S_5]=\dfrac54=\boxed{1.25\text{ hours}}$ with density $f(x)=\dfrac{4e^{-4x}(4x)^4}{4!}$.
> **The mean is just $5\times\tfrac1\lambda$** — five independent exponential waits.
>
> **(iv)** **Do not use the rate.** Conditional on $N(1)=2$, the two arrival times are i.i.d. $U(0,1)$ (§1). Hence
> $$P\{\text{both in first }20\text{ min}\}=\left(\tfrac13\right)^2=\boxed{\tfrac19}$$
>
> **(v)** $P\{\text{at least one in first }30\text{ min}\}=1-\left(\tfrac12\right)^2=\boxed{\tfrac34}$.
>
> > [!tip] The point of (iv)–(v)
> > **$\lambda=4$ never entered.** Once the count is fixed, the *positions* are uniform and carry no information about the rate — the conditional uniformity property of [[06 - Jointly Distributed Random Variables|ch. 06 §7]]. **Recognising when to switch from "counts" to "conditionally uniform positions" turns hard integrals into one-line binomial calculations.**

> [!question] Exercise 2 — a three-state Markov chain
> Each day Buffy is cheerful (c), so-so (s), or gloomy (g), with
> $$\mathbf P=\begin{pmatrix}.7 & .2 & .1\\ .4 & .3 & .3\\ .2 & .4 & .4\end{pmatrix}$$
> (rows and columns in the order c, s, g).
>
> (i) Verify that $\mathbf P$ is a valid transition matrix and that the chain is ergodic.
> (ii) Find the long-run proportion of days Buffy is cheerful.
> (iii) Interpret $\pi$ in two different ways.

> [!example]- Solution
> **(i)** Each row sums to 1 and all entries are positive, so **$P^{(1)}_{ij}>0$ already** — ergodic with $n=1$.
>
> **(ii)** Solve $\pi=\pi\mathbf P$ with $\sum\pi_j=1$:
> $$\pi_c=.7\pi_c+.4\pi_s+.2\pi_g,\quad \pi_s=.2\pi_c+.3\pi_s+.4\pi_g,\quad \pi_c+\pi_s+\pi_g=1$$
> $$\boxed{\pi=\left(\tfrac{30}{59},\ \tfrac{16}{59},\ \tfrac{13}{59}\right)=(.5085,\ .2712,\ .2203)}$$
> **Buffy is cheerful about 51% of days.** *(Check: $.7(30)+.4(16)+.2(13)=21+6.4+2.6=30$ ✓, and similarly for the other two — the integers $30,16,13$ summing to 59 make the verification exact.)*
>
> **The practical route: write the balance equations, drop one (they are redundant, since the rows sum to 1), and replace it with the normalisation.**
>
> **(iii)** Two readings:
> - **Limiting probability:** for large $n$, $P\{X_n=\text{c}\}\approx.5085$ **whatever her mood on day 0** — the chain forgets its start.
> - **Long-run fraction of time:** over a long stretch, about 51% of days are cheerful. **This is the strong law applied to the chain** ([[08 - Limit Theorems|ch. 08]]).
>
> **The second reading survives when the first fails** (periodic chains), which is exactly the Ehrenfest situation in §2a.

> [!question] Exercise 3 — transient behaviour and doubly stochastic chains
> The weather is a two-state chain with $\alpha=P\{\text{rain}\mid\text{rain}\}=.7$ and $\beta=P\{\text{rain}\mid\text{dry}\}=.4$.
>
> (i) Find the long-run proportion of rainy days.
> (ii) Given that it rains today, find $P\{\text{rain 3 days from now}\}$, and compare with (i).
> (iii) Show that $P^{(n)}_{00}=\pi_0+(1-\pi_0)(\alpha-\beta)^n$, and say what governs the rate of forgetting.
> (iv) A transition matrix is **doubly stochastic** if its *columns* also sum to 1. Show that an ergodic doubly stochastic chain on $\{0,\dots,M\}$ has $\pi_j=\frac1{M+1}$ for every $j$.

> [!example]- Solution
> **(i)** $\pi_0=\dfrac{\beta}{1+\beta-\alpha}=\dfrac{.4}{.7}=\boxed{\tfrac47=.5714}$
>
> **(ii)** $P^{(3)}_{00}=\boxed{.583}$ — **already within 1.2 percentage points of the limit after just three days.**
>
> **(iii)** The matrix $\begin{pmatrix}\alpha & 1-\alpha\\ \beta & 1-\beta\end{pmatrix}$ has eigenvalues $1$ and $\alpha-\beta$. Writing $P^{(n)}_{00}=A+B(\alpha-\beta)^n$ and matching $n=0$ ($P^{(0)}_{00}=1$) and $n\to\infty$ ($\to\pi_0$) gives $A=\pi_0$, $B=1-\pi_0$:
> $$P^{(n)}_{00}=\pi_0+(1-\pi_0)(\alpha-\beta)^n=\tfrac47+\tfrac37(0.3)^n$$
> At $n=3$: $\tfrac47+\tfrac37(.027)=.5714+.0116=.583$ ✓
>
> **The second-largest eigenvalue $|\alpha-\beta|$ controls the rate of forgetting**, geometrically. Here $|\alpha-\beta|=.3$, so memory of today's weather dies by a factor of 3.3 each day. **If $\alpha=\beta$ the chain forgets instantly (the days are independent); if $\alpha-\beta\to1$ it barely forgets at all.**
>
> > [!tip] This is the **spectral gap**, and it is the central quantity in MCMC
> > **The stationary distribution tells you *where* a chain ends up; the second eigenvalue tells you *how long* to wait.** A chain with a tiny spectral gap has the right stationary distribution and is useless in practice — this is exactly the diagnosis behind "the sampler hasn't mixed."
>
> **(iv)** Try $\pi_j=\frac1{M+1}$ for all $j$ and check the balance equation:
> $$\sum_{k=0}^{M}\pi_k P_{kj}=\frac1{M+1}\sum_{k=0}^{M}P_{kj}=\frac1{M+1}\cdot1=\pi_j\ ✓$$
> using **column** sums $=1$. Normalisation is immediate, and by uniqueness (Theorem 2.1) this is *the* stationary distribution. $\blacksquare$
>
> **Interpretation: symmetric shuffling equalises.** A doubly stochastic chain spreads probability without preferring any state — which is why card shuffles (each of which is doubly stochastic) converge to the uniform distribution over all orderings.

> [!question] Exercise 4 — entropy
> (i) Find the entropy of the **sum** of two fair dice, and compare it with the entropy of the **pair**. Explain the relationship.
> (ii) A coin with $P(\text{heads})=\tfrac23$ is flipped 6 times. Find the entropy of the outcome.
> (iii) In (ii), what is the minimum average number of bits needed to transmit the outcome, and what is achievable?
> (iv) Show that a fair coin's outcome is incompressible.

> [!example]- Solution
> **(i)** The sum $S$ has $p_s=\dfrac{6-|7-s|}{36}$ for $s=2,\dots,12$, giving
> $$H(S)=-\sum_{s=2}^{12}p_s\log_2 p_s=\boxed{3.274\text{ bits}}$$
> The **pair** $(X_1,X_2)$ has $H=2\log_2 6=\boxed{5.170\text{ bits}}$ (independent, so entropies add).
>
> **$3.274<5.170$, and this is forced:** the sum is a *function* of the pair, and $H(f(X))\le H(X)$ — **applying a function can only destroy information, never create it.** Concretely, $1.896$ bits are lost, which is exactly the average uncertainty about *which* pair produced a given sum.
>
> **(ii)** With independent flips, entropies add:
> $$H(X)=6\,H\!\left(\tfrac23\right)=6\left[-\tfrac23\log_2\tfrac23-\tfrac13\log_2\tfrac13\right]=6(0.9183)=\boxed{5.510\text{ bits}}$$
>
> **(iii)** By the noiseless coding theorem, **no code averages fewer than $5.510$ bits**, and some code achieves $L<6.510$. **The naive code sends 6 bits (one per flip)** — already inside that window, so the guaranteed gain from symbol-by-symbol coding is nothing.
>
> **To do better, code in blocks** as in Example 4b: block coding drives $L$ toward $5.51$, a **saving of about 8%** over the raw 6 bits. **The bias is mild, so the compressible margin is small** — which is exactly what $H(\tfrac23)=.918$ bits per flip (versus 1) says.
>
> **(iv)** For $p=\tfrac12$, $H(\tfrac12)=1$ bit per flip, so $n$ flips have $H=n$ bits and **no code can average fewer than $n$ bits** — while the raw encoding achieves exactly $n$. **A fair coin is incompressible.**
>
> > [!tip] The general principle
> > **Compressibility is departure from uniformity, and entropy measures it exactly.** Random noise cannot be compressed; structured data can, and the achievable ratio is $H(X)/\log_2 n$. **Any claimed universal compressor is impossible by counting** — this is entropy stated as a theorem rather than a slogan.

> [!question] Exercise 5 — coding and channel capacity *(hard)*
> **(a)** $X$ takes three values with $p=(.5,.3,.2)$.
> (i) Find $H(X)$.
> (ii) Give a prefix code and compute its average length $L$. Verify $H\le L<H+1$.
> (iii) Can a prefix code with lengths $(1,2,3)$ exist? With lengths $(1,1,2)$? Use the Kraft inequality.
>
> **(b)** A binary symmetric channel transmits each bit correctly with probability $p=.9$.
> (i) Find the channel capacity $C^*$.
> (ii) Compute the bit-error probability and rate of the 3-fold repetition code.
> (iii) Compare with Shannon's theorem and say what it promises.

> [!example]- Solution
> **(a)(i)** $$H(X)=-\big[.5\log_2.5+.3\log_2.3+.2\log_2.2\big]=.5+.5211+.4644=\boxed{1.4855\text{ bits}}$$
>
> **(ii)** Assign the shortest codeword to the most likely value:
> $$x_1\to\texttt{0},\qquad x_2\to\texttt{10},\qquad x_3\to\texttt{11}$$
> This is a prefix code, and
> $$L=.5(1)+.3(2)+.2(2)=\boxed{1.5\text{ bits}}$$
> **Check:** $1.4855\le1.5<2.4855$ ✓. **The code is within $0.0145$ bits of the theoretical floor — 99.0% efficient**, and no prefix code on single symbols can do better, since all codeword lengths are integers.
>
> **(iii)** Kraft:
> - Lengths $(1,2,3)$: $\tfrac12+\tfrac14+\tfrac18=\tfrac78\le1$ ✓ — **such a code exists** (e.g. `0`, `10`, `110`), though it is worse here: $L=.5+.6+.6=1.7$.
> - Lengths $(1,1,2)$: $\tfrac12+\tfrac12+\tfrac14=\tfrac54>1$ ✗ — **impossible.** Two one-bit codewords already exhaust `0` and `1`, leaving nothing that is not an extension of one of them.
>
> **The Kraft inequality settles existence by arithmetic alone, without constructing anything.**
>
> **(b)(i)** $$C^*=1+p\log_2 p+(1-p)\log_2(1-p)=1-H(.9)=1-.469=\boxed{.531\text{ bits per use}}$$
>
> **(ii)** Majority decoding of 3 copies fails when 2 or 3 of them flip:
> $$P\{\text{bit error}\}=(.1)^3+3(.1)^2(.9)=.001+.027=\boxed{.028},\qquad \text{rate}=\boxed{\tfrac13=.333}$$
>
> **(iii)** Repetition coding buys an error of $.028$ at rate $.333$. **Shannon's theorem says that at any rate below $C^*=.531$ — including $.5$, which is 50% faster — the error can be made *arbitrarily small*, not merely $.028$.**
>
> > [!important] What the theorem does and does not give
> > **It does:** prove that reliable communication at a fixed positive rate is possible, refuting the intuition that error $\to0$ forces rate $\to0$. The table in §4a suggests a hopeless trade-off; Shannon showed the trade-off is bounded by $C^*$ and not by 0.
> >
> > **It does not:** exhibit a code. The proof is a *random coding* argument — it shows the **average** code over a random ensemble is good, hence some code is good, without saying which. **This is exactly the probabilistic method of [[07 - Properties of Expectation|ch. 07 §1c]]**, deployed on the most consequential problem it has ever been used for. **Constructing codes that actually approach capacity took nearly fifty years** (turbo codes, LDPC), and they are what makes modern wireless and storage work.

---

## 📝 Summary

- **A Poisson process is defined by five *local* conditions** — starts at 0, independent increments, stationary increments, rate $\lambda$, one event at a time — **and everything else is derived.** Each condition is a modelling assumption that can and does fail (clustering, rush hours, batch arrivals).
- **Three equivalent descriptions:** counts $N(t)\sim\text{Poisson}(\lambda t)$; interarrival times i.i.d. $\text{Exp}(\lambda)$; arrival times $S_n\sim\Gamma(n,\lambda)$. **The bridge is $N(t)\ge n\iff S_n\le t$.**
- **Conditional on $N(t)=n$, the arrival times are the order statistics of $n$ i.i.d. $U(0,t)$ — $\lambda$ disappears.** Superposition adds rates; independent thinning splits one process into independent ones.
- **A Markov chain forgets everything except the current state**, so $P\{X_0=i_0,\dots,X_n=i_n\}$ factors along the path, and $n$-step probabilities are matrix powers (Chapman–Kolmogorov).
- **"Not Markov" usually means "not Markov *in these states*."** Enlarging the state space restores the property — at the cost of dimension.
- **For an ergodic chain, $\pi_j=\lim_n P^{(n)}_{ij}$ exists, is independent of the start, and uniquely solves $\pi=\pi\mathbf P$, $\sum\pi_j=1$** — so $\pi$ is a left eigenvector for eigenvalue 1. **$\pi_j$ is also the long-run fraction of time in state $j$, and this second reading survives when ergodicity fails.**
- **The second-largest eigenvalue governs how fast a chain forgets its start** — geometrically, at rate $|\lambda_2|^n$. For the two-state chain, $P^{(n)}_{00}=\pi_0+(1-\pi_0)(\alpha-\beta)^n$. **This spectral gap, not the stationary distribution, is what determines whether an MCMC sampler is usable.**
- **An ergodic doubly stochastic chain has the uniform stationary distribution.**
- **Four axioms on "surprise" force $S(p)=-\log_2 p$**, and hence $H(X)=-\sum p_i\log_2 p_i$. **The logarithm is not a convention — Axiom 4 (surprise adds over independent events) admits no other continuous solution.** $H$ is maximised at the uniform distribution, where $H=\log_2 n$.
- **Chain rule: $H(X,Y)=H(Y)+H_Y(X)$. Information never hurts: $H_Y(X)\le H(X)$, with equality iff $X\perp Y$** — so mutual information $I(X;Y)=H(X)-H_Y(X)$ detects **any** dependence, not just linear.
- **Kraft: a prefix code with lengths $n_i$ exists iff $\sum 2^{-n_i}\le1$** — existence by arithmetic.
- **Noiseless coding theorem: $L\ge H(X)$ for every code, and $H(X)\le L<H(X)+1$ is achievable.** **Entropy is the number of bits per symbol.** A fair coin is incompressible; **compressibility is exactly departure from uniformity**, and block coding closes the sub-1-bit gap.
- **Shannon's noisy coding theorem: below capacity $C^*=1-H(p)$, arbitrarily reliable transmission is possible at a fixed positive rate.** Repetition coding (error $\to0$, rate $\to0$) is spectacularly suboptimal. **The proof is a probabilistic-method argument and exhibits no code.**

---

## ⚠️ Important Notes

> [!warning] The Poisson assumptions are testable, and stationarity is the one that usually fails
> | Condition | Fails when | Fix |
> |---|---|---|
> | Independent increments | arrivals cluster or cascade | Hawkes / self-exciting process |
> | **Stationary increments** | **there is a rush hour** | **non-homogeneous $\lambda(t)$** |
> | One at a time | arrivals come in batches | compound Poisson |
>
> **The diagnostic: for a genuine Poisson process, $\mathrm{Var}(N(t))=\mathbb{E}[N(t)]$.** Over-dispersion ($\mathrm{Var}>\mathbb{E}$) is the usual symptom of clustering or a varying rate, and the standard remedy is the negative binomial ([[08 - Limit Theorems|ch. 08 §4d]]). **Fitting a Poisson to over-dispersed counts understates the variance and produces confidence intervals that are far too narrow.**

> [!warning] The Markov property is relative to the state space
> **Whether a process is Markov is not a property of the process alone.** Two-day-dependent weather is not Markov on $\{$rain, dry$\}$ and *is* Markov on the four ordered pairs.
>
> **So the real question is never "is it Markov?" but "what must the state include?"** — and the answer is a modelling decision with a cost, since state-space size grows exponentially in the memory length. **This is precisely the design question in reinforcement learning ("what is the state?") and in hidden Markov models.**

> [!warning] Ergodicity is a hypothesis, not a formality — and periodicity breaks it
> **Theorem 2.1 requires $P^{(n)}_{ij}>0$ for all $i,j$ for some $n$.** Two ways it fails:
> - **Periodicity.** The Ehrenfest chain moves $\pm1$ each step, so parity alternates and $P^{(n)}_{ij}=0$ for every $n$ of the wrong parity. **$\lim_n P^{(n)}_{ij}$ does not exist.**
> - **Reducibility.** Gambler's ruin has absorbing states 0 and $M$; you can never leave them, so the limit depends entirely on where you started.
>
> **In both cases the "long-run fraction of time" interpretation still holds** — which is why the Ehrenfest answer $\pi_j=\binom Mj2^{-M}$ is correct despite the theorem not applying. **Check periodicity and irreducibility before quoting a limiting distribution.** *(Ross applies Theorem 2.1 to Ehrenfest anyway — see the gaps callout.)*

> [!warning] Entropy's logarithm is forced, and its base is a unit
> **Axiom 4 — $S(pq)=S(p)+S(q)$ for independent events — admits only $-C\log p$** among continuous decreasing functions. **The logarithm is derived, not chosen.**
>
> **The base is a choice of unit, not of substance:** base 2 gives **bits**, base $e$ gives **nats**, base 10 gives **digits**, and they differ by a constant factor. **Coding theory uses bits because channels are binary; machine-learning libraries use nats because derivatives are cleaner.** Converting is multiplication by $\log_2 e=1.4427$ — but reporting a cross-entropy in the wrong unit is a 44% error in a number people compare across papers.

> [!warning] Conditioning reduces entropy *on average*, not always
> **$H_Y(X)\le H(X)$ is a statement about the average $\sum_j H_{Y=y_j}(X)p_Y(y_j)$.**
>
> **A particular observation can increase your uncertainty:** learning $Y=y_j$ for some specific unlikely $y_j$ may leave $H_{Y=y_j}(X)>H(X)$. **What cannot happen is for this to hold on average.** *(This is the discrete analogue of "conditioning reduces variance on average" — the law of total variance in [[07 - Properties of Expectation|ch. 07]].)*

> [!warning] Entropy is a floor on compression that no cleverness evades
> $$L\ \ge\ H(X)\qquad\text{for every prefix code}$$
> **Claims of a universal compressor that shrinks arbitrary data are impossible by counting**, quite apart from entropy: there are more $n$-bit strings than shorter ones.
>
> **Two practical corollaries.** Already-compressed or encrypted data has near-maximal entropy and **will not compress further** — and re-compressing it usually makes it larger. And **compression ratio is an entropy measurement**: it tells you how much structure the data actually has.

> [!warning] Shannon's theorem is an existence proof
> **It guarantees a code exists below capacity; it does not produce one.** The proof averages over a random ensemble of codes and concludes some member is good — **the probabilistic method of [[07 - Properties of Expectation|ch. 07 §1c]]**.
>
> **The practical gap was enormous:** capacity was known in 1948, and codes approaching it (turbo, LDPC) arrived in the 1990s. **"It exists" and "we can build it" are separated by decades here** — a healthy corrective to reading existence theorems as engineering advice.

> [!note] Cross-subject connections
> - [[05 - Continuous Random Variables|Ch. 05]] — **the Poisson process is memorylessness made into a process**; the exponential's uniqueness is why interarrivals must be exponential.
> - [[06 - Jointly Distributed Random Variables|Ch. 06]] — Poisson thinning (Example 2b) and conditional uniformity of arrivals (Example 7e) **are** §1 here; conditional distributions are §2.
> - [[07 - Properties of Expectation|Ch. 07]] — **entropy is an expectation**, $\mathbb{E}[-\log p(X)]$; Shannon's proof is the probabilistic method; mutual information is the dependence measure correlation fails to be.
> - [[08 - Limit Theorems|Ch. 08]] — **the strong law is what makes $\pi_j$ a long-run fraction of time**, and hence what makes MCMC valid.
> - [[10 - Simulation|Ch. 10]] — simulating a Poisson variable by multiplying uniforms until the product drops below $e^{-\lambda}$ **is** simulating a Poisson process; MCMC is §2 turned into an algorithm.
> - [[Linear Algebra/contents/00-Index|Linear Algebra]] — $\pi=\pi\mathbf P$ is a **left eigenvector** problem; Perron–Frobenius guarantees existence and uniqueness; the **spectral gap** is the mixing rate. **PageRank is the stationary distribution of a doubly-stochastic-ised web graph.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **cross-entropy loss is §3**; information gain is the decision-tree split criterion; MDPs are Markov chains with actions, and "what is the state?" is the design question §2 raises.
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — Markov chains are the discrete-state ancestor of AR models; both ask how quickly the past is forgotten.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — likelihood ratios and KL divergence are the continuous analogues of §3, and $\ln x\le x-1$ is the same workhorse inequality.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — **Huffman coding constructs the optimal prefix code** whose optimality §4 bounds.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **A theorem applied outside its hypotheses.** Example 2f computes the Ehrenfest stationary distribution and says *"By Theorem 2.1, these quantities will be the unique solution of…"* — **but the Ehrenfest chain is periodic with period 2** (the count changes by exactly $\pm1$ each step, so $P^{(n)}_{ij}=0$ whenever $n$ and $j-i$ have opposite parity), and therefore **fails the ergodicity condition (2.1) for every $n$.** The limit $\lim_n P^{(n)}_{ij}$ does not exist. **The answer $\pi_j=\binom Mj 2^{-M}$ is nevertheless correct**, by the *other* justification Ross gives two pages earlier — that $\pi_j$ is the long-run proportion of time, which he explicitly notes "is generally valid even when the chain is not ergodic." **The citation is wrong; the result is right.** *(Flagged in §2a and in the notes above.)*
>
> **Source typos:**
> - **§9.2** states the transition probabilities as "$P_{ij}$, $0\le i\le M$, $0\le j\le N$" — **there is no $N$ in this chapter**; it should be $0\le j\le M$.
> - **Theorem 3.1** concludes "$S(p)=-C\log_2 p$ where $C$ is an arbitrary positive **integer**" — it should be an arbitrary positive **constant**. $C=S(\tfrac12)$ has no reason to be an integer, and the very next sentence ("It is usual to let $C$ equal 1") makes the intent clear.
> - **Problem 9.7 and 9.11** print `∏_j` where $\pi_j$ is meant — the capital-pi/lower-case-pi confusion is in the typesetting, since the same symbol appears correctly as `π` in the body text.
> - **Example 4a**'s displayed entropy writes the last two (equal) terms as a single `¼ log(1/8)`, which is arithmetically correct ($2\times\tfrac18=\tfrac14$) but reads as an error at first glance.
>
> **Figures and tables:**
> - **The transition-matrix displays in §9.2 lose all their bracket structure** — the $2\times2$ weather matrix extracts as bare numbers `α 1 − α β 1 − β` with no delimiters, and the general $(M+1)\times(M+1)$ matrix extracts as a column of stray box-drawing characters. **Reconstructed from the surrounding text**, which states the entries explicitly.
> - **The encode/decode diagram for 3-fold repetition** (§9.4) extracts as an unstructured jumble of `000 001 010 100 → 0` and `111 110 101 011 → 1` with the braces detached. **The majority-rule content is recoverable** and is stated in the text, so nothing is lost.
> - **Table 9.1** extracts with its two columns interleaved (`.20 1 / .10 .33 (= 1/3) / .01 .06 (= 1/17)`); **reconstructed and verified** — $1/3=.333$ and $1/17=.0588$ ✓.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and checked against numeric answers):
> - **`…` is `≤`**, **`Ú` is `≥`**, **`q` is `∞`**, **`Z` is `≠`**, **`K` is `≡`**, **`3` is `⟺`** (in Theorem 1.1's `N(t) Ú n 3 Sn … t`), **`*` is `×`** (Example 2f's `π1 * 1/M`), **`%` is `→`** (the code assignments `x1 % 00` in §9.4) — the same substitution set as chapters 1–8, plus two new ones (`3` and `%`).
> - **`/H9008` is $\Theta$** in the chapter-10 cross-references, where earlier chapters used `/Theta1` — **a third distinct encoding for the same character**, joining `/Phi1` and `/H9278` for $\Phi$ noted in [[08 - Limit Theorems|ch. 08]].
> - **`ln x` versus `log x`:** the source's footnote establishes that **`log` means $\log_2$ throughout this chapter** while `ln` is natural log. **This is easy to miss and changes every numerical answer by a factor of 1.44** — I have written $\log_2$ explicitly throughout these notes.
>
> **Verification performed:** every numeric claim in the chapter was independently recomputed. Confirmed: $\pi_0=\tfrac37$ for $\alpha=.6$, $\beta=.3$ (2e); the Ehrenfest stationary distribution satisfies the balance equations (2f); $H(X)=1.75$ for $P=(\tfrac12,\tfrac14,\tfrac18,\tfrac18)$ (4a); $H(X)=8.113$ for ten flips at $p=\tfrac14$ and the pair-code average $\tfrac{135}{16}=8.4375$ (4b); the 3-fold repetition error $(.2)^3+3(.2)^2(.8)=.104$; **the claim that 17 repetitions push the error below $.01$ — the exact value is $.0026$** ✓; the Table 9.1 rates $\tfrac13$ and $\tfrac1{17}$; and the capacity $C^*=1+.8\log_2.8+.2\log_2.2=.278$ for $p=.8$. **All agree with the text. The only defect found is the misapplied ergodicity hypothesis documented above.**
>
> **One scope note:** this chapter is a set of previews rather than a development — **the Poisson process gets 3 pages, Markov chains 6, and neither treats classification of states, recurrence, transience, hitting times, or absorption probabilities.** Notably, **gambler's ruin appears as Example 2b with no analysis at all**, even though [[03 - Conditional Probability and Independence|ch. 03]] solved it by conditioning and [[07 - Properties of Expectation|ch. 07]] computed its expected duration. **I have flagged this rather than filling it in**, since a genuine treatment needs the recurrence/transience machinery of a stochastic-processes course, and Ross's own *Introduction to Probability Models* is the intended sequel (it is reference [3] at the end of the chapter).

#probability #poisson-process #markov-chain #stationary-distribution #entropy #information-theory #coding #channel-capacity
