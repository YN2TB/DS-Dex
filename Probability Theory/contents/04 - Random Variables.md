---
subject: Probability Theory
chapter: 04
tags: [ds, probability, random-variables, expectation, variance, binomial, poisson]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 4 (pp. 131–200)"
---

# Random Variables

> [!abstract] What this chapter is for
> **Chapters 1–3 dealt with *events*. This chapter moves to *numbers*.**
>
> Most of the time we do not care about the full outcome of an experiment — **we care about some numerical summary of it.** Not *which* dice came up what, but their **sum**; not *which* trials succeeded, but **how many**. A **random variable** is exactly that: a real-valued function on the sample space.
>
> **Two payoffs follow immediately.** First, numbers can be **averaged** — giving expectation and variance, two numbers that summarise a whole distribution. Second, wildly different experiments turn out to produce **the same distribution**, so a handful of named families covers most of what you will ever meet.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1–2** | Random variables, **pmf**, distribution function | A random variable is a *function*, not an outcome |
> | **3–4** | **Expectation**, $\mathbb{E}[g(X)]$ | The "law of the unconscious statistician" |
> | **5** | **Variance** | $\mathrm{Var}(X)=\mathbb{E}[X^2]-(\mathbb{E}[X])^2$ |
> | **6** | **Bernoulli and binomial** | Counting successes in $n$ independent trials |
> | **7** | **Poisson** | The limit of the binomial when $n$ is large and $p$ small |
> | **8** | Geometric, negative binomial, **hypergeometric** | Waiting times; sampling *without* replacement |
> | **9** | **Expectation of sums** | Linearity + indicators = the chapter's most powerful tool |
> | **10** | The cumulative distribution function | |

---

## 📘 Main Knowledge

### 1. Random variables and the probability mass function

> [!important] Definition
> A **random variable** is a real-valued function defined on the sample space. **Its value is determined by the outcome, so it is itself random.**
>
> A random variable taking at most countably many values is **discrete**, and its **probability mass function** is
> $$p(a)=P\{X=a\}$$
> **Since $X$ must take one of its possible values, $\displaystyle\sum_i p(x_i)=1$.**

> [!tip] The mental model
> **The random variable is the *function*; the pmf is the induced distribution.** Two different experiments can produce the same pmf — and once they do, **everything probabilistic about them is identical.** That is why the named families of §6–§8 are worth learning: they are the distributions that keep recurring.

The **cumulative distribution function** is

$$F(b)=P\{X\le b\}=\sum_{x\le b}p(x)$$

> [!note] Properties of $F$ (§10)
> - **Non-decreasing**
> - $\lim_{b\to\infty}F(b)=1$ and $\lim_{b\to-\infty}F(b)=0$
> - **Right-continuous**
>
> **All probability questions about $X$ can be answered from $F$.** For a discrete $X$, $F$ is a **step function** that jumps at each possible value, with **jump size equal to $p(x)$**:
> $$P\{X=a\}=F(a)-F(a^-)$$

---

### 2. Expected value

> [!important] Definition
> $$\boxed{\mathbb{E}[X]=\sum_{x:\,p(x)>0}x\,p(x)}$$
> **A weighted average of the possible values, each weighted by its probability.**

**Two motivations, both worth holding:**

**The arithmetic one.** If $p(0)=p(1)=\tfrac12$ then $\mathbb{E}[X]=\tfrac12$ — the ordinary average. If $p(0)=\tfrac13$, $p(1)=\tfrac23$, then $\mathbb{E}[X]=\tfrac23$ — **the value 1 gets twice the weight because it is twice as likely.**

**The frequency one.** Think of $X$ as your winnings per game. Playing repeatedly, you win $x_i$ a proportion $p(x_i)$ of the time, so **your average winnings per game is $\sum_ix_ip(x_i)=\mathbb{E}[X]$.** *(Justified properly by the strong law of large numbers, [[08 - Limit Theorems|ch. 08]].)*

> [!note] The physical analogy — worth carrying
> **Expectation is the centre of gravity.** Put masses $p(x_i)$ at positions $x_i$ on a weightless rod; **it balances at $\mathbb{E}[X]$.**
>
> The proof is one line: balance requires the torques to cancel, $\sum_i(x_i-\mathbb{E}[X])p(x_i)=0$, **which is immediate from the definition.**
>
> *(Ross's Figure 4.4: $p(-1)=.10$, $p(0)=.25$, $p(1)=.30$, $p(2)=.35$ balances at $\mathbf{0.9}$ ✓)*

| Example | Question | Answer |
|---|---|---|
| **3a** | Roll of a fair die | $\mathbb{E}[X]=\tfrac{1+\cdots+6}{6}=\mathbf{\tfrac72}$ |
| **3b** | **Indicator** $I=1$ if $A$ occurs, else 0 | $\mathbb{E}[I]=\mathbf{P(A)}$ |

> [!important] Example 3b is the most important line in the chapter
> $$\boxed{\mathbb{E}[I_A]=P(A)}$$
> **The expected value of an indicator is the probability of the event.** This looks trivial. Combined with linearity (§7), **it becomes the single most powerful computational device in the book** — see Example 9d and the exercises.

> [!example] Example 3c — which question to answer first
> A quiz contestant may attempt question $i$ (worth $V_i$, known with probability $P_i$) but may continue to the other question **only if the first is answered correctly.**
>
> Trying question 1 first gives expected winnings $V_1P_1(1-P_2)+(V_1+V_2)P_1P_2$; trying question 2 first gives $V_2P_2(1-P_1)+(V_1+V_2)P_1P_2$. **The common term cancels**, so question 1 should go first iff
> $$\boxed{\frac{V_1P_1}{1-P_1}\ge\frac{V_2P_2}{1-P_2}}$$
>
> **Numerical case:** $V_1=\$200$ at $P_1=.6$; $V_2=\$100$ at $P_2=.8$.
> $$\frac{200(.6)}{.4}=\mathbf{300} \qquad\text{versus}\qquad \frac{100(.8)}{.2}=\mathbf{400}$$
> **Attempt the cheaper question 2 first** — because being more likely to survive it matters more than its lower value.
>
> **The quantity $\dfrac{VP}{1-P}$ is value × odds of success.** *(Exactly the odds of [[03 - Conditional Probability and Independence|ch. 03 §2c]].)*

> [!example] Example 3d — the size-biased bus (a genuinely useful idea)
> 120 students on three buses: **36, 40, 44.** Pick a *student* at random and let $X$ be the size of *their* bus.
> $$\mathbb{E}[X]=36\left(\tfrac{36}{120}\right)+40\left(\tfrac{40}{120}\right)+44\left(\tfrac{44}{120}\right)=\tfrac{1208}{30}=\mathbf{40.27}$$
> **But the average bus holds $120/3=40$ students.**
>
> > [!important] This is a general phenomenon, not a quirk
> > *"The more students there are on a bus, the more likely it is that a randomly chosen student would have been on that bus. As a result, buses with many students are given more weight."*
> >
> > **Sampling *units* and sampling *groups* give different answers.** The same effect explains:
> > - **Class-size paradox** — the average class a student experiences is bigger than the average class the university runs
> > - **The friendship paradox** — your friends have more friends than you do, on average
> > - **Waiting-time / inspection paradox** — the bus interval you land in is longer than the average interval
> >
> > **Whenever a sampling scheme is proportional to size, expect an upward bias.** *This is one of the most frequently missed traps in applied data work.*

---

### 3. Expectation of a function of a random variable

**You could find the pmf of $g(X)$ and then apply the definition** — but there is a better way.

> [!example] Example 4a — doing it the long way
> $P\{X=-1\}=.2$, $P\{X=0\}=.5$, $P\{X=1\}=.3$. **Find $\mathbb{E}[X^2]$.**
>
> Let $Y=X^2$: then $P\{Y=1\}=.2+.3=.5$ and $P\{Y=0\}=.5$, so $\mathbb{E}[X^2]=\mathbf{.5}$.
>
> **Note:** $\mathbb{E}[X]=-.2+.3=.1$, so $(\mathbb{E}[X])^2=.01$.
> $$\boxed{\mathbb{E}[X^2]=.5\ \ne\ (\mathbb{E}[X])^2=.01}$$
> **A warning to keep permanently: $\mathbb{E}[g(X)]\ne g(\mathbb{E}[X])$ in general.**

> [!important] Proposition 4.1 — the law of the unconscious statistician
> $$\boxed{\mathbb{E}[g(X)]=\sum_i g(x_i)\,p(x_i)}$$
> **You never need the pmf of $g(X)$ — just weight $g$ at each $x_i$ by $p(x_i)$.**

**Proof.** Group the terms of $\sum_ig(x_i)p(x_i)$ by the distinct values $y_j$ of $g$:

$$\sum_ig(x_i)p(x_i)=\sum_j\sum_{i:g(x_i)=y_j}y_j\,p(x_i)=\sum_jy_j\!\!\sum_{i:g(x_i)=y_j}\!\!p(x_i)=\sum_jy_jP\{g(X)=y_j\}=\mathbb{E}[g(X)]\ \blacksquare$$

*Check against Example 4a:* $(-1)^2(.2)+0^2(.5)+1^2(.3)=.5$ ✓

> [!important] Corollary 4.1 — linearity for a single variable
> $$\boxed{\mathbb{E}[aX+b]=a\mathbb{E}[X]+b}$$
> **Proof: split $\sum(ax+b)p(x)$ into $a\sum xp(x)+b\sum p(x)$.** $\blacksquare$
>
> **This is the only case where $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ generally holds — because $g$ is linear.**

**Terminology.** $\mathbb{E}[X]$ is the **mean** or **first moment**; $\mathbb{E}[X^n]$ is the **$n$th moment**, computed by Proposition 4.1 as $\sum_xx^np(x)$.

> [!note] Example 4b — the newsvendor problem
> Profit $b$ per unit sold, loss $\ell$ per unit unsold; demand has pmf $p(i)$. **Stocking $s+1$ beats stocking $s$ whenever**
> $$\sum_{i=0}^{s}p(i)<\frac{b}{b+\ell} \tag{4.1}$$
> **The left side increases in $s$ and the right is constant**, so the optimum is $s^*+1$ where $s^*$ is the largest $s$ satisfying (4.1).
>
> **In words: stock up to the quantile $\dfrac{b}{b+\ell}$ of demand.** *(This is the classical newsvendor solution, and it is the basis of inventory theory and of quantile regression's loss function.)*

> [!note] Example 4c — utility, and why expectation is the right criterion
> Faced with two risky actions over consequences $C_1,\dots,C_n$: **assign the worst consequence $c$ value 0, the best $C$ value 1, and value each $C_i$ by the *indifference probability* $u(C_i)$** — the $u$ making you indifferent between receiving $C_i$ for sure and a gamble giving $C$ with probability $u$, $c$ otherwise.
>
> **Then action 1 beats action 2 iff $\sum_ip_iu(C_i)>\sum_iq_iu(C_i)$.**
>
> > **"The worth of an action can be measured by the expected value of the utility of its consequence."**
> >
> > **This is why decision theory maximises expected *utility*, not expected *money*.** People are risk-averse in money precisely because $u$ is concave — see [[Microeconomics/contents/00-Index|Microeconomics]].

---

### 4. Variance

**Expectation says where the distribution sits; it says nothing about spread.** Ross's illustration: $W\equiv0$; $Y=\pm1$ with probability $\tfrac12$ each; $Z=\pm100$ with probability $\tfrac12$ each. **All three have mean 0, and they could hardly be more different.**

> [!important] Definition
> $$\boxed{\mathrm{Var}(X)=\mathbb{E}[(X-\mu)^2]}, \qquad \mu=\mathbb{E}[X]$$
> and expanding,
> $$\boxed{\mathrm{Var}(X)=\mathbb{E}[X^2]-(\mathbb{E}[X])^2}$$
>
> The **standard deviation** is $\mathrm{SD}(X)=\sqrt{\mathrm{Var}(X)}$.

> [!note] Why squares rather than absolute values
> The natural measure of spread is $\mathbb{E}[|X-\mu|]$. **Ross is candid: "it turns out to be mathematically inconvenient to deal with this quantity, so a more tractable quantity is usually considered."**
>
> **Squares are chosen for tractability, not because they are more meaningful.** They are differentiable everywhere, they expand cleanly, and they make variance additive over independent variables ([[07 - Properties of Expectation|ch. 07]]). *(The absolute-deviation version reappears as **LAD/median regression** in [[Econometrics/contents/00-Index|Econometrics]], and as the reason the median minimises $\mathbb{E}|X-c|$ while the mean minimises $\mathbb{E}(X-c)^2$.)*

> [!important] The scaling rule
> $$\boxed{\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)}$$
> **Shifts do not change spread; scaling changes it by $a^2$.** Contrast $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$ — **the constant $b$ survives in the mean and vanishes from the variance.**

---

### 5. The Bernoulli and binomial random variables

> [!important] Bernoulli and binomial
> A **Bernoulli($p$)** variable takes value 1 with probability $p$ and 0 with probability $1-p$.
>
> If $n$ **independent** trials each succeed with probability $p$, the number of successes $X$ is **binomial$(n,p)$**:
> $$\boxed{p(i)=\binom nip^i(1-p)^{n-i}, \qquad i=0,1,\dots,n}$$
>
> $$\boxed{\mathbb{E}[X]=np \qquad\qquad \mathrm{Var}(X)=np(1-p)}$$

**Why the formula is right.** Any *specific* sequence with $i$ successes has probability $p^i(1-p)^{n-i}$ by independence, and **there are $\binom ni$ such sequences** — the same count as [[01 - Combinatorial Analysis|ch. 01 §4]]. *The probabilities sum to 1 by the binomial theorem: $\sum_i\binom nip^i(1-p)^{n-i}=[p+(1-p)]^n=1$.*

| Example | Setup | Result |
|---|---|---|
| **6a** | 5 fair coins | $p(i)=\binom5i/32$, i.e. $\tfrac1{32},\tfrac5{32},\tfrac{10}{32},\tfrac{10}{32},\tfrac5{32},\tfrac1{32}$ |
| **6b** | Screws defective w.p. $.01$, packs of 10, refund if $\ge2$ defective | $1-(.99)^{10}-10(.01)(.99)^9\approx\mathbf{.004}$ — only $0.4\%$ replaced |
| **6d** | Two hybrid parents, 4 children; $P(3\text{ show dominant})$ | Binomial$(4,\tfrac34)$: $\binom43(\tfrac34)^3(\tfrac14)=\mathbf{\tfrac{27}{64}}$ |

> [!example] Example 6c — chuck-a-luck is not a fair game
> Bet on a number; roll 3 dice; **win $i$ units if it shows $i$ times, lose 1 unit if it never shows.** The count is binomial$(3,\tfrac16)$:
>
> | Winnings | Probability |
> |---|---|
> | $-1$ | $\tfrac{125}{216}$ |
> | $+1$ | $\tfrac{75}{216}$ |
> | $+2$ | $\tfrac{15}{216}$ |
> | $+3$ | $\tfrac1{216}$ |
>
> $$\mathbb{E}[X]=\frac{-125+75+30+3}{216}=\boxed{-\tfrac{17}{216}}\approx-0.079$$
> **The player loses about 7.9 units per 100 played.**
>
> > **The game *looks* fair** — "your number comes up, you win; it doesn't, you lose 1" — **and the asymmetry is buried in the fact that a miss is far more likely than any single hit.** *Casino games are designed to have exactly this property.*

> [!example] Example 6f — when is more redundancy better?
> A system works if **at least half** its components work, each independently with probability $p$.
>
> **A 5-component system beats a 3-component system iff**
> $$10p^3(1-p)^2+5p^4(1-p)+p^5>3p^2(1-p)+p^3$$
> which reduces to $3(p-1)^2(2p-1)>0$, i.e.
> $$\boxed{p>\tfrac12}$$
> **And in general, $2k+1$ components beat $2k-1$ if and only if $p>\tfrac12$.**
>
> > [!important] The lesson generalises far beyond hardware
> > **Adding components helps only if each is better than a coin flip.** If $p<\tfrac12$, **more components make the system *worse*** — you are adding more wrong opinions.
> >
> > *(Check: at $p=.6$, $P_5=.683>P_3=.648$ ✓; at $p=.4$, $P_5=.317<P_3=.352$ ✓; at $p=.5$ both are exactly $.5$ ✓)*
> >
> > **This is Condorcet's jury theorem**, and it is why **ensemble methods in machine learning require base learners better than chance** — bagging a set of worse-than-random classifiers degrades performance.
>
> **The clean proof of the general case** conditions on $X$, the number of the first $2k-1$ that work:
> $$P_{2k+1}=P\{X\ge k+1\}+P\{X=k\}[1-(1-p)^2]+P\{X=k-1\}p^2$$
> — *the extra two components matter only in the two borderline cases.*

> [!note] Example 6e — the jury problem has no answer as stated
> 12 jurors, each correct with probability $\theta$, 8 votes needed to convict. **$P(\text{correct verdict})$?**
>
> *"The problem, as stated, is incapable of solution, for there is not yet enough information."* The answer depends on $\alpha=P(\text{guilty})$:
> $$\alpha\sum_{i=8}^{12}\binom{12}{i}\theta^i(1-\theta)^{12-i}+(1-\alpha)\sum_{i=5}^{12}\binom{12}{i}\theta^i(1-\theta)^{12-i}$$
> **Note the asymmetric thresholds:** acquitting an innocent defendant needs only 5 correct jurors (to block the 8), while convicting a guilty one needs 8. **Same as [[03 - Conditional Probability and Independence|ch. 03]]'s Example 3m: a problem can be genuinely underdetermined, and the honest answer is to say so.**

---

### 6. The Poisson random variable

> [!important] Definition
> $$\boxed{p(i)=P\{X=i\}=e^{-\lambda}\frac{\lambda^i}{i!}, \qquad i=0,1,2,\dots}$$
> $$\boxed{\mathbb{E}[X]=\lambda \qquad\qquad \mathrm{Var}(X)=\lambda}$$
>
> *(It is a valid pmf since $\sum_i\lambda^i/i!=e^{\lambda}$.)*

> [!important] The Poisson limit of the binomial — the reason it matters
> **Let $X\sim$ binomial$(n,p)$ and set $\lambda=np$. Then**
> $$P\{X=i\}=\frac{n(n-1)\cdots(n-i+1)}{n^i}\cdot\frac{\lambda^i}{i!}\cdot\frac{(1-\lambda/n)^n}{(1-\lambda/n)^i}$$
> **For $n$ large and $\lambda$ moderate, the three factors tend to $1$, $\lambda^i/i!$, and $e^{-\lambda}$**, giving
> $$P\{X=i\}\approx e^{-\lambda}\frac{\lambda^i}{i!}$$
>
> **In words: many trials, each unlikely to succeed, but a moderate expected number of successes → Poisson.**

> [!tip] Why $\mathbb{E}=\mathrm{Var}=\lambda$ is unsurprising
> The binomial has mean $np=\lambda$ and variance $np(1-p)=\lambda(1-p)\approx\lambda$ **because $p$ is small.** The limit inherits both. *(Ross verifies both directly by summing the series; the key step in $\mathbb{E}[X^2]=\lambda(\lambda+1)$ is recognising the two inner sums as $\mathbb{E}[X]$ and $\sum p(i)=1$.)*
>
> **This equality is a genuine diagnostic:** if count data has variance far exceeding its mean, it is **overdispersed** and the Poisson model is wrong ([[Econometrics/contents/00-Index|Econometrics]], negative binomial regression).

**Ross's list of things that are approximately Poisson** — all for the same reason:

1. Misprints on a page 2. People surviving to age 100 3. Wrong phone numbers dialled in a day 4. Packages of dog biscuits sold daily 5. Customers entering a post office 6. Vacancies in the federal judiciary 7. $\alpha$-particles emitted by radioactive material

**In each case: a large number of near-independent opportunities, each with tiny probability.**

| Example | Setup | Answer |
|---|---|---|
| **7a** | Typos per page, $\lambda=\tfrac12$; $P(\ge1)$ | $1-e^{-1/2}\approx\mathbf{.393}$ |
| **7b** | 10 items, $p=.1$; $P(\le1\text{ defective})$ | Exact $\mathbf{.7361}$; Poisson$(1)$ gives $2e^{-1}\approx\mathbf{.7358}$ |
| **7c** | $\alpha$-particles, mean $3.2$; $P(\le2)$ | $e^{-3.2}\big(1+3.2+\tfrac{3.2^2}{2}\big)\approx\mathbf{.3799}$ |

> [!note] How good is the approximation? Look at Example 7b
> **With $n=10$ — hardly "large" — the Poisson gives $.7358$ against the exact $.7361$: an error of $3\times10^{-4}$.** The approximation is far better than its derivation suggests.

#### 6a. The Poisson paradigm

> [!important] The Poisson paradigm
> *"Consider $n$ events, with $p_i$ equal to the probability that event $i$ occurs. **If all the $p_i$ are "small" and the trials are either independent or at most "weakly dependent," then the number of these events that occur approximately has a Poisson distribution with mean $\sum_ip_i$.**"*
>
> **Neither equal probabilities nor exact independence is required.** That is what makes it so widely applicable.

**Two beautiful confirmations, both revisiting [[02 - Axioms of Probability|ch. 02]]:**

> [!example] The matching problem, seen through Poisson eyes
> With $E_i$ = "person $i$ gets their own hat": $P(E_i)=\tfrac1n$ and $P(E_i\mid E_j)=\tfrac1{n-1}$ — **dependent, but only just, for large $n$.** So the number of matches should be approximately Poisson with mean $n\times\tfrac1n=\mathbf{1}$.
>
> **And indeed [[03 - Conditional Probability and Independence|ch. 03]]'s Example 2f derived exactly $P(k\text{ matches})\to e^{-1}/k!$.** ✓
>
> **The Poisson paradigm predicts in one line what took a full inclusion–exclusion argument.**

> [!example] The birthday problem, re-derived — and then extended
> Run a "trial" for each of the $\binom n2$ **pairs**; trial $(i,j)$ succeeds if $i$ and $j$ share a birthday, with probability $\tfrac1{365}$. **The pair events are weakly dependent** (indeed pairwise independent), so the number of matching pairs is approximately Poisson with mean
> $$\lambda=\binom n2\Big/365=\frac{n(n-1)}{730}$$
> $$P(\text{no shared birthday})\approx\exp\left\{-\frac{n(n-1)}{730}\right\}$$
> **This is below $\tfrac12$ when $n(n-1)\ge730\log2\approx\mathbf{505.997}$** — and $23\times22=506$, giving $n=\mathbf{23}$ ✓, **in exact agreement with the combinatorial answer of [[02 - Axioms of Probability|ch. 02]].** *(At $n=22$: $22\times21=462<506$.)*
>
> > [!important] Now the payoff — the extension the exact method cannot easily reach
> > **What if we want no *three* people sharing a birthday?** Combinatorially this is hard. **With the paradigm it is immediate:** run a trial per **triple**, each succeeding with probability $(1/365)^2$:
> > $$\lambda=\binom n3\left(\frac1{365}\right)^2=\frac{n(n-1)(n-2)}{799{,}350}$$
> > $$P(\text{no triple})\approx\exp\left\{-\frac{n(n-1)(n-2)}{799{,}350}\right\}$$
> > Below $\tfrac12$ when $n(n-1)(n-2)\ge799{,}350\log2\approx554{,}067$, i.e. **$n\ge84$.**
> > *(Check: $n=83$ gives $551{,}286<554{,}067$; $n=84$ gives $571{,}704>554{,}067$ ✓)*
> >
> > **23 people for a shared birthday, 84 for a shared triple.** **The paradigm turns an intractable combinatorial problem into two lines of arithmetic — that is why it is worth learning as a technique rather than a fact.**

> [!warning] The paradigm has limits — Example 7d
> For "is there a run of $k$ consecutive heads in $n$ flips?", let $H_i$ = "flips $i,\dots,i+k-1$ are all heads", each with probability $p^k$. **Tempting — but wrong:** *"such is not the case, because, although the events all have small probabilities, **some of their dependencies are too great** for the Poisson distribution."*
>
> **Overlapping windows are strongly dependent** ($H_i$ and $H_{i+1}$ share $k-1$ flips). **"Weakly dependent" is a real condition, not a formality.**

---

### 7. Other discrete distributions

> [!important] Geometric($p$) — trials until the **first** success
> $$p(n)=(1-p)^{n-1}p, \qquad n=1,2,\dots$$
> $$\boxed{\mathbb{E}[X]=\frac1p \qquad\qquad \mathrm{Var}(X)=\frac{1-p}{p^2}}$$
> **and $P\{X>n\}=(1-p)^n$** — *"no success in the first $n$ trials."*

> [!important] Negative binomial($r,p$) — trials until the **$r$th** success
> $$p(n)=\binom{n-1}{r-1}p^r(1-p)^{n-r}, \qquad n=r,r+1,\dots$$
> $$\boxed{\mathbb{E}[X]=\frac rp \qquad\qquad \mathrm{Var}(X)=\frac{r(1-p)}{p^2}}$$
> **Reading the pmf:** the $n$th trial must be a success, and exactly $r-1$ of the previous $n-1$ must be successes. **Geometric is the case $r=1$.**

> [!important] Hypergeometric($n,N,m$) — sampling **without** replacement
> $n$ balls drawn from $N$, of which $m$ are white:
> $$p(i)=\frac{\binom mi\binom{N-m}{n-i}}{\binom Nn}$$
> $$\boxed{\mathbb{E}[X]=\frac{nm}{N} \qquad\qquad \mathrm{Var}(X)=\frac{nm}{N}\left[\frac{(n-1)(m-1)}{N-1}+1-\frac{nm}{N}\right]}$$

> [!important] The relationship you must keep straight
> | Sampling | Distribution |
> |---|---|
> | **With** replacement (independent trials) | **Binomial**$(n,p)$ |
> | **Without** replacement (finite population) | **Hypergeometric**$(n,N,m)$ |
>
> **With $p=m/N$, both have the same mean $np=nm/N$.** But the hypergeometric variance carries a **finite-population correction** — **it is smaller**, because sampling without replacement is more informative.
>
> **And when $N$ and $m$ are large relative to $n$, the hypergeometric $\to$ binomial:** *"no matter which balls have previously been selected, when $m$ and $N$ are large, each additional selection will be white with probability approximately $p$."*

| Example | Setup | Answer |
|---|---|---|
| **8g** | Throws of a die until a 1 appears | Geometric$(\tfrac16)$: $\mathbb{E}=\mathbf{6}$, $\mathrm{Var}=\mathbf{30}$ |
| **8i** | Lots of 10; inspect 3, accept iff all good. 30% of lots have 4 defectives, 70% have 1 | $P(\text{accept})=\tfrac{\binom63}{\binom{10}3}(.3)+\tfrac{\binom93}{\binom{10}3}(.7)=\tfrac{54}{100}$, so **46% rejected** |

> [!example] Example 8h — capture–recapture, and a first maximum likelihood estimate
> Catch $m$ animals, mark, release; later catch $n$ and observe $i$ marked. **Then $X\sim$ hypergeometric, and we want the $N$ that makes the observed $i$ most likely.**
>
> Ross computes the ratio
> $$\frac{P_i(N)}{P_i(N-1)}=\frac{(N-m)(N-n)}{N(N-m-n+i)}$$
> **which exceeds 1 exactly when $N\le\dfrac{mn}{i}$.** So $P_i(N)$ rises then falls, and the maximum is at
> $$\boxed{\hat N=\left\lfloor\frac{mn}{i}\right\rfloor}$$
>
> **With $m=50$, $n=40$, $i=4$: $\hat N=\mathbf{500}$.**
>
> > **This is a *maximum likelihood estimate*** — the chapter's first, named as such. **And it agrees with the naive intuition:** the marked fraction in the population, $m/N$, should match the marked fraction in the second catch, $i/n$ — giving $N=mn/i$ ✓
> >
> > **A rigorous optimisation and a back-of-envelope proportion give the same answer here. They very often do not** ([[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]).

> [!note] Example 8e — the Banach match problem
> A mathematician carries two matchboxes of $N$ matches, choosing one at random each time. **When he first finds a box empty, what is the distribution of the number remaining in the other?** *A classic negative-binomial calculation, included here as a flag rather than developed — it is a favourite exam problem.*

---

### 8. Expected value of sums — the chapter's most powerful tool

> [!important] Proposition 9.1 and Corollary 9.2
> $$\mathbb{E}[X]=\sum_{s\in S}X(s)\,p(s)$$
> and hence, **for any random variables at all**,
> $$\boxed{\mathbb{E}\left[\sum_{i=1}^{n}X_i\right]=\sum_{i=1}^{n}\mathbb{E}[X_i]}$$

> [!important] Read the words "any random variables at all"
> **No independence is required. None.** The proof simply pushes the sum inside the sum over sample points — **it never touches the joint distribution.**
>
> **Contrast variance, which does *not* add unless the variables are uncorrelated** ([[07 - Properties of Expectation|ch. 07 §4]]). **Knowing exactly which identities need independence is worth more than any distributional formula.**

> [!tip] Linearity + indicators = the standard technique
> **To find $\mathbb{E}[N]$ where $N$ counts something:**
> 1. **Write $N=\sum_iI_i$** with $I_i$ the indicator of the $i$th thing happening
> 2. **$\mathbb{E}[I_i]=P(\text{$i$th thing happens})$** (Example 3b)
> 3. **Sum**, ignoring all dependence
>
> **This converts intractable counting problems into a list of easy marginal probabilities.**

| Example | Question | Via indicators |
|---|---|---|
| **9c** | Sum of $n$ fair dice | $\mathbb{E}=n\cdot\tfrac72$ |
| **9d** | Successes in $n$ trials, trial $i$ succeeding w.p. $p_i$ | $\mathbb{E}=\sum_ip_i$ **(trials need not be independent)** |

> [!example] The binomial mean in one line
> $X=\sum_{i=1}^nI_i$ where $I_i$ indicates success on trial $i$. Then
> $$\mathbb{E}[X]=\sum_{i=1}^{n}\mathbb{E}[I_i]=\sum_{i=1}^{n}p=np$$
> **Compare the direct route: $\sum_i i\binom nip^i(1-p)^{n-i}$, which requires an index shift and a re-summation.** *Same for the hypergeometric mean $nm/N$ — trivial by indicators, tedious directly.*

> [!example] Expected number of matches, instantly
> In the hat problem, $I_i$ indicates that person $i$ gets their own hat, so $\mathbb{E}[I_i]=\tfrac1n$ and
> $$\mathbb{E}[\text{matches}]=n\cdot\tfrac1n=\boxed{1} \quad\text{for every } n$$
> **The $I_i$ are dependent — and it does not matter in the slightest.** *(Consistent with the Poisson(1) approximation of §6a ✓)*

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — pmf, cdf, expectation, variance**

Three fair coins are flipped; $X$ is the number of heads.

**(i)** Write the pmf of $X$ and verify it sums to 1.

**(ii)** Write the cdf $F(b)$ and sketch its shape in words. Find $P\{X\le1.5\}$ and $P\{0<X\le2\}$.

**(iii)** Compute $\mathbb{E}[X]$ and $\mathbb{E}[X^2]$ from the definition, then $\mathrm{Var}(X)$.

**(iv)** Check your answers against the binomial formulas.

**(v)** Recover $P\{X=2\}$ from $F$ alone, and state the general rule.

> [!example]- Solution
> **(i)** $X\sim$ binomial$(3,\tfrac12)$, so $p(i)=\binom3i/8$:
>
> | $i$ | 0 | 1 | 2 | 3 |
> |---|---|---|---|---|
> | $p(i)$ | $\tfrac18$ | $\tfrac38$ | $\tfrac38$ | $\tfrac18$ |
>
> **Sum $=\tfrac{1+3+3+1}{8}=1$** ✓
>
> ---
> **(ii)** $$F(b)=\begin{cases}0 & b<0\\ \tfrac18 & 0\le b<1\\ \tfrac12 & 1\le b<2\\ \tfrac78 & 2\le b<3\\ 1 & b\ge3\end{cases}$$
> **A step function**: flat between the possible values, jumping at $0,1,2,3$ by $\tfrac18,\tfrac38,\tfrac38,\tfrac18$. **Right-continuous** — at $b=1$ the value is already $\tfrac12$, not $\tfrac18$.
>
> $$P\{X\le1.5\}=F(1.5)=\mathbf{\tfrac12} \qquad P\{0<X\le2\}=F(2)-F(0)=\tfrac78-\tfrac18=\mathbf{\tfrac34}$$
>
> ---
> **(iii)** $$\mathbb{E}[X]=0\cdot\tfrac18+1\cdot\tfrac38+2\cdot\tfrac38+3\cdot\tfrac18=\tfrac{0+3+6+3}{8}=\mathbf{\tfrac32}$$
> $$\mathbb{E}[X^2]=0+1\cdot\tfrac38+4\cdot\tfrac38+9\cdot\tfrac18=\tfrac{3+12+9}{8}=\mathbf{3}$$
> $$\mathrm{Var}(X)=3-\left(\tfrac32\right)^2=3-\tfrac94=\mathbf{\tfrac34}$$
>
> ---
> **(iv)** $np=3\cdot\tfrac12=\tfrac32$ ✓ and $np(1-p)=3\cdot\tfrac12\cdot\tfrac12=\tfrac34$ ✓
>
> ---
> **(v)** $$P\{X=2\}=F(2)-F(2^-)=\tfrac78-\tfrac12=\mathbf{\tfrac38}\ ✓$$
>
> **General rule:** $$\boxed{P\{X=a\}=F(a)-F(a^-)}$$
> **— the size of the jump in $F$ at $a$.** **A discrete distribution is entirely encoded in the jumps of its cdf**, which is why "all probability questions about $X$ can be answered from $F$."

---

**Exercise 2 — Functions of a random variable**

$X$ has pmf $P\{X=-2\}=.1$, $P\{X=-1\}=.2$, $P\{X=0\}=.4$, $P\{X=1\}=.2$, $P\{X=2\}=.1$.

**(i)** Find $\mathbb{E}[X]$ and $\mathrm{Var}(X)$.

**(ii)** Find $\mathbb{E}[X^2]$ using Proposition 4.1, and confirm $\mathbb{E}[X^2]\ne(\mathbb{E}[X])^2$.

**(iii)** Find $\mathbb{E}[|X|]$. Is $\mathbb{E}[|X|]=|\mathbb{E}[X]|$?

**(iv)** Let $Y=3X+5$. Find $\mathbb{E}[Y]$ and $\mathrm{Var}(Y)$ **without** computing $Y$'s pmf.

**(v)** A student claims $\mathbb{E}[1/X]=1/\mathbb{E}[X]$. **Give two separate reasons this fails here.**

> [!example]- Solution
> **(i)** By symmetry about 0, $\mathbb{E}[X]=\mathbf{0}$. *(Check: $-.2-.2+0+.2+.2=0$ ✓)*
> $$\mathbb{E}[X^2]=4(.1)+1(.2)+0(.4)+1(.2)+4(.1)=.4+.2+.2+.4=\mathbf{1.2}$$
> $$\mathrm{Var}(X)=1.2-0^2=\mathbf{1.2}$$
>
> ---
> **(ii)** Already done: $\mathbb{E}[X^2]=\mathbf{1.2}$ while $(\mathbb{E}[X])^2=\mathbf{0}$.
>
> > **They could hardly differ more.** In fact $\mathbb{E}[X^2]\ge(\mathbb{E}[X])^2$ **always**, since the difference is $\mathrm{Var}(X)\ge0$. *(This is Jensen's inequality for the convex function $g(x)=x^2$.)*
>
> ---
> **(iii)** $$\mathbb{E}[|X|]=2(.1)+1(.2)+0(.4)+1(.2)+2(.1)=\mathbf{0.8}$$
> **while $|\mathbb{E}[X]|=0$.** **Emphatically not equal.**
>
> **The reason is the same as (ii): $|\cdot|$ is not linear.** Positive and negative deviations cancel inside $\mathbb{E}[\cdot]$ but not inside $|\cdot|$.
>
> ---
> **(iv)** By **Corollary 4.1** and the scaling rule — no pmf needed:
> $$\mathbb{E}[Y]=3(0)+5=\mathbf{5} \qquad\qquad \mathrm{Var}(Y)=3^2(1.2)=\mathbf{10.8}$$
>
> **Note the asymmetry: the $+5$ shifts the mean and leaves the variance untouched.**
>
> ---
> **(v)** **Two independent reasons:**
>
> **1. $1/x$ is not defined at $x=0$**, and $P\{X=0\}=.4$ — **so $\mathbb{E}[1/X]$ does not exist at all** for this $X$.
>
> **2. Even where it does exist, the identity is false**, because $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ **holds only for linear $g$** (Corollary 4.1). For the strictly convex $g(x)=1/x$ on $x>0$, Jensen's inequality gives $\mathbb{E}[1/X]>1/\mathbb{E}[X]$ whenever $X$ is non-degenerate.
>
> > **The recurring theme of §3: expectation passes through *linear* functions and nothing else.**
> > $$\mathbb{E}[aX+b]=a\mathbb{E}[X]+b\ ✓ \qquad \mathbb{E}[X^2]\ne(\mathbb{E}[X])^2 \qquad \mathbb{E}[1/X]\ne1/\mathbb{E}[X] \qquad \mathbb{E}[|X|]\ne|\mathbb{E}[X]|$$
> >
> > *(Applied corollary: the average of ratios is not the ratio of averages — a mistake that appears constantly in reported statistics.)*

---

**Exercise 3 — The binomial in quality control**

A factory produces items defective with probability $.05$, independently. A batch of 20 is inspected.

**(i)** Find $P\{0\text{ defective}\}$, $P\{\le1\}$ and $P\{\ge2\}$.

**(ii)** Find $\mathbb{E}[X]$, $\mathrm{Var}(X)$ and $\mathrm{SD}(X)$.

**(iii)** Which value of $X$ is most likely? Verify by computing $P\{X=0\},\dots,P\{X=3\}$.

**(iv)** The factory improves to $p=.01$ but batches grow to 100. **Has $P\{\ge2\}$ improved?** Answer without heavy computation, then check.

**(v)** In Example 6f, explain why $p>\tfrac12$ is exactly the right threshold, and give a machine-learning analogue.

> [!example]- Solution
> **(i)** $X\sim$ binomial$(20,.05)$:
> $$P\{X=0\}=(.95)^{20}=\mathbf{.3585}$$
> $$P\{X\le1\}=(.95)^{20}+20(.05)(.95)^{19}=\mathbf{.7358}$$
> $$P\{X\ge2\}=1-.7358=\mathbf{.2642}$$
>
> ---
> **(ii)** $$\mathbb{E}[X]=20(.05)=\mathbf{1} \qquad \mathrm{Var}(X)=20(.05)(.95)=\mathbf{0.95} \qquad \mathrm{SD}(X)=\mathbf{0.975}$$
> **Note $\mathrm{Var}\approx\mathbb{E}$** — as expected, since $p$ is small and $np(1-p)\approx np$. *(This is precisely the regime where the Poisson takes over.)*
>
> ---
> **(iii)** The mode of a binomial is $\lfloor(n+1)p\rfloor=\lfloor21\times.05\rfloor=\lfloor1.05\rfloor=\mathbf{1}$.
>
> | $k$ | $P\{X=k\}$ |
> |---|---|
> | 0 | $.35849$ |
> | **1** | $\mathbf{.37735}$ |
> | 2 | $.18868$ |
> | 3 | $.05958$ |
>
> **$k=1$ is the mode**, just ahead of $k=0$ ✓
>
> ---
> **(iv)** **Predict first: $\lambda=np=100(.01)=1$ is unchanged**, and for small $p$ the distribution depends almost entirely on $\lambda$. **So $P\{\ge2\}$ should be nearly identical, not better.**
>
> **Check:** $P\{X\le1\}=(.99)^{100}+100(.01)(.99)^{99}=.7358$, so $P\{\ge2\}=\mathbf{.2642}$ — **the same to four decimal places.**
>
> > **Both cases are Poisson(1) in disguise**, where $P\{\le1\}=2e^{-1}=.7358$. **Halving the defect rate while quintupling the batch size buys nothing.** *The quantity that governs quality here is the expected number of defects per batch, not the defect rate.*
>
> ---
> **(v)** **A component is worth adding only if it is right more often than wrong.**
>
> Formally, the extra pair of components changes the outcome only in the two borderline cases ($X=k$, needing one of the two to work; $X=k-1$, needing both). **The algebra reduces to $3(p-1)^2(2p-1)>0$, and since $(p-1)^2>0$, the sign is entirely that of $2p-1$.**
>
> **Machine-learning analogue: ensembles.** Bagging or majority-voting $M$ classifiers improves accuracy **only if each base learner beats chance.** **Combining worse-than-random classifiers makes things monotonically worse** — the majority reliably votes for the wrong answer, and more voters make that more reliable.
>
> > **This is Condorcet's jury theorem (1785)**, and it is the theoretical justification for random forests and for boosting's requirement of "weak learners" — where *weak* means **slightly better than chance**, never worse.

---

**Exercise 4 — The Poisson approximation and paradigm**

**(i)** For $(n,p)=(10,.1)$, $(100,.01)$ and $(1000,.001)$ — all with $\lambda=1$ — compute the exact binomial $P\{X\le2\}$ and the Poisson approximation. Tabulate the errors.

**(ii)** State precisely what the errors show about the approximation's accuracy.

**(iii)** For $X\sim$ Poisson$(3)$, find $P\{X=0\}$, $P\{X\le2\}$ and $P\{X\ge5\}$.

**(iv)** Use the Poisson paradigm to find the smallest group for which the chance that some two share a birthday exceeds $\tfrac12$, and confirm it agrees with the exact answer.

**(v)** **Why does the paradigm fail for the longest-run problem (Example 7d)?** State the condition that is violated.

> [!example]- Solution
> **(i)**
>
> | $n$ | $p$ | Binomial $P\{X\le2\}$ | Poisson$(1)$ | Error |
> |---|---|---|---|---|
> | 10 | $.1$ | $.929809$ | $.919699$ | $1.0\times10^{-2}$ |
> | 100 | $.01$ | $.920627$ | $.919699$ | $9.3\times10^{-4}$ |
> | 1000 | $.001$ | $.919791$ | $.919699$ | $9.2\times10^{-5}$ |
>
> ---
> **(ii)** **The error falls by roughly a factor of 10 each time $n$ rises by a factor of 10** — i.e. **the error is $O(1/n)$ for fixed $\lambda$.**
>
> **Two practical readings:**
> - **Even $n=10$ gives an error of only 1%** — usable for rough work
> - **What matters is $p$ being small, not $n$ being large per se.** All three rows have the same $\lambda$; only $p$ changes.
>
> *(Consistent with Ross's Example 7b, where $n=10$, $p=.1$ gave $.7361$ against $.7358$.)*
>
> ---
> **(iii)** $X\sim$ Poisson$(3)$, $p(k)=e^{-3}3^k/k!$:
> $$P\{X=0\}=e^{-3}=\mathbf{.04979}$$
> $$P\{X\le2\}=e^{-3}\left(1+3+\tfrac92\right)=8.5e^{-3}=\mathbf{.42319}$$
> $$P\{X\ge5\}=1-e^{-3}\left(1+3+4.5+4.5+3.375\right)=\mathbf{.18474}$$
>
> ---
> **(iv)** Run a trial per **pair**; each succeeds with probability $\tfrac1{365}$, and the pairs are weakly (indeed pairwise independently) dependent:
> $$\lambda=\binom n2\Big/365=\frac{n(n-1)}{730}, \qquad P(\text{no match})\approx e^{-\lambda}$$
> This is $\le\tfrac12$ iff $n(n-1)\ge730\log2\approx\mathbf{505.997}$.
> $$n=22:\ 22\times21=462<506 \qquad\qquad n=23:\ 23\times22=506\ge506\ ✓$$
> **So $n=\mathbf{23}$** — exactly the exact-combinatorial answer of [[02 - Axioms of Probability|ch. 02]] ✓
>
> *(The approximation gives $e^{-506/730}=.499998$ against the exact $.4927$ — accurate to about $0.7$ percentage points, and it identifies the same threshold.)*
>
> ---
> **(v)** **The violated condition is "weakly dependent."**
>
> The events $H_i$ = "flips $i$ through $i+k-1$ are all heads" **overlap heavily**: $H_i$ and $H_{i+1}$ share $k-1$ of their $k$ flips, so
> $$P(H_{i+1}\mid H_i)=p \qquad\text{versus}\qquad P(H_{i+1})=p^k$$
> **A factor of $p^{-(k-1)}$ — enormous.** *"Some of their dependencies are too great for the Poisson distribution."*
>
> > **Contrast the birthday pairs**, where $P(E_{ij}\mid E_{kl})=P(E_{ij})=\tfrac1{365}$ for disjoint pairs and only mildly different when they share a person.
> >
> > **The general test: does knowing one event occurred substantially change the odds of a neighbouring one?** For hat matches and birthday pairs, barely. **For overlapping windows in a sequence, drastically.** *(Runs and clustering problems generally need the Chen–Stein method or direct recursion, not the naive paradigm.)*

---

**Exercise 5 — Waiting times, sampling, and indicators**

**(i)** A fair die is rolled until a 1 appears. Find $\mathbb{E}$, $\mathrm{Var}$, $P\{X>3\}$ and $P\{X=4\}$.

**(ii)** Now roll until the **third** 1 appears. Find $\mathbb{E}$ and $\mathrm{Var}$.

**(iii)** From 50 components of which 10 are defective, 5 are drawn without replacement. Find $\mathbb{E}[X]$ and $P\{X=0\}$; compare with the binomial approximation.

**(iv)** $n$ people randomly select hats. **Using indicators, find the expected number who get their own hat**, and comment on the role of independence.

**(v)** $k$ coupons are collected from $n$ equally likely types. **Find the expected number of distinct types collected**, and evaluate at $n=10$, $k=20$.

> [!example]- Solution
> **(i)** Geometric$(p=\tfrac16)$:
> $$\mathbb{E}[X]=\frac1p=\mathbf{6} \qquad \mathrm{Var}(X)=\frac{1-p}{p^2}=\frac{5/6}{1/36}=\mathbf{30}$$
> $$P\{X>3\}=\left(\tfrac56\right)^3=\mathbf{\tfrac{125}{216}}\approx.579 \qquad P\{X=4\}=\left(\tfrac56\right)^3\tfrac16=\mathbf{\tfrac{125}{1296}}\approx.096$$
> **Note $\mathrm{SD}=\sqrt{30}\approx5.5$, almost as large as the mean** — the geometric is extremely spread out. *(Its median is 4 while its mean is 6: a strongly right-skewed distribution.)*
>
> ---
> **(ii)** Negative binomial$(r=3,p=\tfrac16)$:
> $$\mathbb{E}[X]=\frac rp=\mathbf{18} \qquad \mathrm{Var}(X)=\frac{r(1-p)}{p^2}=\mathbf{90}$$
> **Both are exactly $r$ times the geometric values** — because the waiting time for the $r$th success is a **sum of $r$ independent geometrics**, and both mean and variance add over independent variables ([[07 - Properties of Expectation|ch. 07]]).
>
> ---
> **(iii)** Hypergeometric with $N=50$, $m=10$, $n=5$:
> $$\mathbb{E}[X]=\frac{nm}{N}=\frac{5\times10}{50}=\mathbf{1}$$
> $$P\{X=0\}=\frac{\binom{10}{0}\binom{40}{5}}{\binom{50}{5}}=\mathbf{.31056}$$
> **Binomial approximation** with $p=m/N=0.2$: $P\{X=0\}=(0.8)^5=\mathbf{.32768}$.
>
> > **The approximation is about 5% too high**, because $n/N=5/50=10\%$ of the population is sampled — **not small enough for the "each draw is like the last" heuristic.**
> >
> > **The means agree exactly** ($np=nm/N=1$); only the spread differs. **Sampling without replacement is *less* variable**, which is the finite-population correction. *(Rule of thumb: the binomial approximation is safe when $n<0.05N$.)*
>
> ---
> **(iv)** Let $I_i=1$ if person $i$ gets their own hat. **Each person is equally likely to get any hat**, so $\mathbb{E}[I_i]=P(I_i=1)=\tfrac1n$. By linearity:
> $$\mathbb{E}\left[\sum_{i=1}^nI_i\right]=\sum_{i=1}^n\frac1n=\boxed{1}$$
> **for every $n$.**
>
> > **The $I_i$ are certainly *not* independent** — if the first $n-1$ people get their own hats, the last one must too, so $P(I_n=1\mid I_1=\cdots=I_{n-1}=1)=1\ne\tfrac1n$.
> >
> > **Linearity of expectation does not care.** *"$\mathbb{E}[\sum X_i]=\sum\mathbb{E}[X_i]$ for **any** random variables."*
> >
> > **Compare the alternatives:** the direct route needs the full inclusion–exclusion pmf of [[02 - Axioms of Probability|ch. 02]]'s Example 5m. **The indicator route is one line.** ✓ *(And it matches the Poisson(1) mean predicted by the paradigm.)*
>
> ---
> **(v)** Let $I_j=1$ if type $j$ appears at least once. **Type $j$ is missed by a single coupon with probability $1-\tfrac1n$, so missed entirely with probability $(1-\tfrac1n)^k$:**
> $$\mathbb{E}[I_j]=1-\left(1-\frac1n\right)^k$$
> $$\boxed{\mathbb{E}[\text{distinct types}]=n\left[1-\left(1-\frac1n\right)^k\right]}$$
>
> **At $n=10$, $k=20$:** $10\left[1-(0.9)^{20}\right]=10(1-.1216)=\mathbf{8.78}$
>
> > **20 coupons yield only about 8.8 of the 10 types** — the last few are the expensive ones. *(Collecting all 10 takes $10H_{10}\approx29.3$ coupons on average — the **coupon collector's problem**, solved by the same indicator technique applied to waiting times.)*
> >
> > **The $I_j$ are again dependent** (collecting many of type 1 makes the others less likely), **and again it is irrelevant.**
> >
> > **This is the template to remember:** *count something* → *write it as a sum of indicators* → *find each marginal probability* → *add them up*. **It is the most reusable technique in the chapter and it is developed much further in [[07 - Properties of Expectation|ch. 07 §2]].**

---

## 📝 Summary

- **A random variable is a real-valued function on the sample space**, described by its **pmf** $p(a)=P\{X=a\}$ (summing to 1) or its **cdf** $F(b)=P\{X\le b\}$ — non-decreasing, right-continuous, with limits 0 and 1. **For discrete $X$, $F$ is a step function and $P\{X=a\}=F(a)-F(a^-)$.**
- **$\mathbb{E}[X]=\sum_xxp(x)$** is a probability-weighted average — equivalently the **centre of gravity** of the distribution, or long-run average winnings. **$\mathbb{E}[I_A]=P(A)$ for an indicator**, which is the seed of the chapter's most powerful technique.
- **Size-biased sampling (Example 3d):** the bus of a randomly chosen *student* averages $40.27$ students while the average *bus* holds $40$. **Sampling proportional to size always inflates the mean** — the class-size, friendship and inspection paradoxes are all this effect.
- **Proposition 4.1:** $\mathbb{E}[g(X)]=\sum_ig(x_i)p(x_i)$ — **no need for the pmf of $g(X)$.** **Corollary 4.1:** $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$. **These are the only functions that pass through:** $\mathbb{E}[X^2]\ne(\mathbb{E}[X])^2$, $\mathbb{E}[1/X]\ne1/\mathbb{E}[X]$, $\mathbb{E}[|X|]\ne|\mathbb{E}[X]|$.
- **$\mathrm{Var}(X)=\mathbb{E}[(X-\mu)^2]=\mathbb{E}[X^2]-(\mathbb{E}[X])^2$**, with $\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$. **Squares are used for tractability, not meaning** — Ross says so explicitly.
- **Binomial$(n,p)$:** $p(i)=\binom nip^i(1-p)^{n-i}$, $\mathbb{E}=np$, $\mathrm{Var}=np(1-p)$. **Counts successes in $n$ independent trials.** Adding components to a majority-vote system helps **if and only if $p>\tfrac12$** (Example 6f — Condorcet's jury theorem).
- **Poisson$(\lambda)$:** $p(i)=e^{-\lambda}\lambda^i/i!$, with **$\mathbb{E}=\mathrm{Var}=\lambda$.** It is the **limit of the binomial when $n$ is large, $p$ small, $\lambda=np$ moderate** — and the approximation is excellent even at $n=10$.
- **The Poisson paradigm:** for $n$ events with small probabilities that are independent **or weakly dependent**, the number occurring is approximately Poisson with mean $\sum_ip_i$. **It reproduces the birthday answer ($n=23$) and the matching answer ($e^{-1}$) in one line each, and extends to problems the exact methods cannot reach** (no three sharing a birthday: $n=84$). **It fails when dependence is strong** — e.g. overlapping runs.
- **Geometric($p$):** trials to the first success; $\mathbb{E}=1/p$, $\mathrm{Var}=(1-p)/p^2$, $P\{X>n\}=(1-p)^n$. **Negative binomial($r,p$):** trials to the $r$th success; $\mathbb{E}=r/p$, $\mathrm{Var}=r(1-p)/p^2$ — **exactly $r$ times the geometric, being a sum of $r$ of them.**
- **Hypergeometric** is the *without-replacement* counterpart of the binomial: same mean $nm/N$, **smaller variance** (finite-population correction), and it **converges to the binomial when $n\ll N$.** Its maximum likelihood estimate gives **capture–recapture: $\hat N=\lfloor mn/i\rfloor$.**
- **Linearity of expectation, $\mathbb{E}[\sum X_i]=\sum\mathbb{E}[X_i]$, holds for *any* random variables — dependence is irrelevant.** Combined with indicators, it computes expected counts (matches, distinct coupons, binomial and hypergeometric means) in one line each. **Variance has no such property.**

---

## ⚠️ Important Notes

> [!warning] $\mathbb{E}[g(X)]\ne g(\mathbb{E}[X])$ — except for linear $g$
> **This single fact generates a large fraction of all errors in applied probability.**
>
> | Wrong | Right |
> |---|---|
> | $\mathbb{E}[X^2]=(\mathbb{E}[X])^2$ | differ by $\mathrm{Var}(X)\ge0$ |
> | $\mathbb{E}[1/X]=1/\mathbb{E}[X]$ | differ, and $\mathbb{E}[1/X]$ may not exist |
> | $\mathbb{E}[\sqrt X]=\sqrt{\mathbb{E}[X]}$ | $\le$, by concavity |
> | *"average of ratios = ratio of averages"* | **false, and common in reported statistics** |
>
> **The general statement is Jensen's inequality:** $\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])$ for convex $g$, $\le$ for concave. **Only linear $g$ gives equality — that is Corollary 4.1.**

> [!warning] Size-biased sampling inflates the mean, and it is everywhere
> **Example 3d: buses of 36, 40, 44. Average bus size 40; average size of *a random student's* bus, 40.27.**
>
> **The mechanism: larger groups contribute more sampling units, so they are over-represented.** Real instances:
> - **Class sizes** — universities report the mean class, students experience the size-biased one
> - **Friendship paradox** — your friends have more friends than you, because popular people appear in more friend lists
> - **Waiting times** — the gap you arrive during is longer than the average gap
> - **Survey sampling** — sampling households by person over-represents large households
>
> **Whenever the sampling probability is proportional to size, expect an upward bias.** **Ask: am I sampling units, or groups?**

> [!warning] Linearity of expectation needs no independence — variance does
> $$\mathbb{E}\left[\sum X_i\right]=\sum\mathbb{E}[X_i] \quad\textbf{always} \qquad\qquad \mathrm{Var}\left(\sum X_i\right)=\sum\mathrm{Var}(X_i) \quad\textbf{only if uncorrelated}$$
>
> **The hat-matching indicators are strongly dependent, and $\mathbb{E}[\text{matches}]=1$ regardless.**
>
> **This asymmetry is the single most useful structural fact in the chapter.** **When you need an expected count, use indicators and ignore dependence entirely. When you need a variance, you must handle the covariances** ([[07 - Properties of Expectation|ch. 07 §4]]).

> [!warning] With or without replacement — binomial or hypergeometric?
> | Sampling | Distribution | Variance |
> |---|---|---|
> | **With** replacement | Binomial$(n,p)$ | $np(1-p)$ |
> | **Without** replacement | Hypergeometric | **smaller** (finite-population correction) |
>
> **Both have mean $np$ with $p=m/N$** — so **checking the mean will never reveal the error.** Only the spread differs, which means **confidence intervals built on the wrong model are wrong even though the point estimate is right.**
>
> **Rule of thumb: the binomial approximation is safe when $n<0.05N$.** In Exercise 5(iii) with $n/N=10\%$, the error in $P\{X=0\}$ was already 5%.

> [!warning] "Weakly dependent" in the Poisson paradigm is a genuine condition
> **It works spectacularly** for hat matches and birthday pairs — reproducing exact answers and extending to intractable variants.
>
> **It fails** for runs of consecutive heads, because overlapping windows share most of their flips: $P(H_{i+1}\mid H_i)=p$ versus $P(H_{i+1})=p^k$.
>
> **The test: does one event occurring substantially change a neighbouring event's odds?** **Small probabilities alone are not enough** — Ross is explicit that Example 7d's events all have small probability and the paradigm still fails.

> [!warning] $\mathbb{E}=\mathrm{Var}$ is a testable claim, not a curiosity
> **For Poisson data, mean and variance must be equal.** Real count data frequently has **variance $\gg$ mean** — *overdispersion* — which means the Poisson model is wrong.
>
> **Usual causes:** unobserved heterogeneity (a mixture of Poissons with different $\lambda$), or clustering (arrivals in bursts). **The standard fix is the negative binomial**, which is exactly a Poisson with a random $\lambda$.
>
> **Fitting a Poisson to overdispersed data leaves the mean estimate roughly right and the standard errors badly too small** — the same failure mode as heteroskedasticity in [[Econometrics/contents/00-Index|Econometrics]].

> [!warning] Redundancy helps only above the halfway point
> **Example 6f: a $(2k+1)$-component majority system beats a $(2k-1)$-component one if and only if $p>\tfrac12$.**
>
> **Below $\tfrac12$, adding components makes the system reliably *worse*** — a majority of unreliable voters converges on the wrong answer.
>
> **In machine learning this is why boosting demands "weak learners" that are *better than chance*, and why averaging a pool of below-chance models degrades rather than improves.** *(At exactly $p=\tfrac12$ every system size gives $.5$ — no amount of aggregation extracts signal from noise.)*

> [!warning] Some problems are genuinely underdetermined — say so
> **Example 6e (the jury) cannot be solved without $\alpha=P(\text{guilty})$**, exactly as [[03 - Conditional Probability and Independence|ch. 03]]'s Example 3m could not be solved without the observation mechanism.
>
> *"The problem, as stated, is incapable of solution, for there is not yet enough information."*
>
> **Identifying the missing assumption is a complete and correct answer.** **Inventing a plausible-looking number to fill the gap is not** — and in the jury case the missing quantity is a prior probability of guilt, which is precisely what a court is supposed to determine.

> [!note] Cross-subject connections
> - [[03 - Conditional Probability and Independence|Ch. 03]] — **the binomial pmf was already derived there** (Example 4f) and the Poisson(1) already appeared in the matching problem (Example 2f). **This chapter names and systematises them.**
> - [[05 - Continuous Random Variables|Ch. 05]] — the same programme with integrals replacing sums; **$\sum_xg(x)p(x)$ becomes $\int g(x)f(x)\,dx$** and nothing else changes conceptually.
> - [[07 - Properties of Expectation|Ch. 07]] — **develops the indicator technique of §8 into the chapter's central method**, and adds the covariance machinery that variance needs.
> - [[08 - Limit Theorems|Ch. 08]] — **justifies the frequency motivation for $\mathbb{E}[X]$** (strong law) and gives the normal approximation to the binomial (CLT).
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — Example 8h's $\hat N=mn/i$ is the book's **first maximum likelihood estimate**; every named distribution here is a sampling model there.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — Example 6f is the theory behind **ensembles**; the geometric distribution governs rejection sampling; the Poisson governs rare-event and count models.
> - [[Econometrics/contents/00-Index|Econometrics]] — Poisson and negative binomial regression for count outcomes; the $\mathbb{E}=\mathrm{Var}$ check is a standard specification test.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Figures are images and cannot be extracted:**
> - **Figure 4.4** (the centre-of-gravity rod) — only the labels survive: `210 2^ 1`, `p(21) 5 .10, p(0) 5 .25, p(2) 5 .35p(1) 5 .30,`, `^ 5 center of gravity 5 .9`. **The `5` characters are mangled `=` signs and the `2`s are mangled minus signs**, so this reads $p(-1)=.10$, $p(0)=.25$, $p(1)=.30$, $p(2)=.35$, centre of gravity $=.9$. **I verified the arithmetic: $-1(.10)+0(.25)+1(.30)+2(.35)=0.90$ ✓** — the reconstruction is correct.
> - **Figure 4.6(a) and (b)** (Mendel's yellow/green seed crosses) — the genetics diagram is lost; only fragments `Pure yellow`, `y, y g, g`, `Hybrid`, `y1, g2y1, y2 y2, g1` and four $\tfrac14$ labels extract. **The text states the $\tfrac14,\tfrac14,\tfrac12$ genotype probabilities explicitly**, so Example 6d is fully reconstructible.
> - **Figures 4.1–4.3, 4.5, 4.7, 4.8** (cdf plots and pmf bar charts) are images with no recoverable content beyond their captions. **Their content is described in the surrounding prose.**
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and cross-checked against numeric answers):
> - **`q` is `∞`**, **`…` is `≤`**, **`Ú` is `≥`**, **`Z` is `≠`**, **`L` is `≈`**, **`(` and `)` are sometimes `⊂`/`⊃`** — the same substitution set as chapters 2–3.
> - **`K` is the extraction of `≡`** in Example 8h: `( m i )( N − m n − i ) / ( N n ) K Pi(N)` means $\dots\equiv P_i(N)$.
> - **`/Box` is the end-of-proof symbol** $\square$, appearing at the end of Proposition 4.1's proof.
> - **`ℓ` survives** in Example 4b but **superscripts detach throughout**: `4 5 − 4` for $4^5-4$, `p 2(1 − p)2` for $p^2(1-p)^2$, `(1 − p)n−i` for $(1-p)^{n-i}$.
> - **Binomial coefficients extract across four lines** and **fractions as numerator-newline-denominator**, as in chapters 1–3.
>
> **A minor numerical presentation issue:** Example 3d gives the answer as `1208/30 = 40.2667`. **This is correct but unreduced** — $\tfrac{1208}{30}=\tfrac{604}{15}$. Verified: $604/15=40.2\overline{6}$ ✓.
>
> **Verification performed:** every numeric claim in Examples 3a–9e was independently recomputed — $\tfrac72$; $400>300$; $\tfrac{1208}{30}=40.267$ vs average 40; centre of gravity $.9$; $\mathbb{E}[X^2]=.5$ vs $(\mathbb{E}[X])^2=.01$; the five-coin pmf; $.004266\approx.004$; the chuck-a-luck pmf $\tfrac{125}{216},\tfrac{75}{216},\tfrac{15}{216},\tfrac1{216}$ and $\mathbb{E}=-\tfrac{17}{216}$; $\tfrac{27}{64}$; the $p>\tfrac12$ threshold (checked at $p=.4,.5,.6$); $1-e^{-1/2}=.3935$; $.7361$ vs $.7358$; $.3799$; $730\log2=505.997$ with $23\times22=506$; $799{,}350\log2=554{,}067$ with $n=84$; $\hat N=500$; and $P(\text{accept})=\tfrac{54}{100}$. **All agree with the text. No arithmetic errors were found in this chapter.**
>
> **One place where the text is thinner than the topic warrants:** the **negative binomial variance** $r(1-p)/p^2$ is derived in Example 8f via a moment computation, **but the far more illuminating fact — that a negative binomial is a *sum of $r$ independent geometrics*, which makes both the mean and the variance immediate — is not stated in this chapter.** *(It follows from [[07 - Properties of Expectation|ch. 07]]'s additivity results.)* **I have flagged the connection in §7 and Exercise 5(ii)**, since it makes both formulas memorable rather than arbitrary.

#probability #random-variables #expectation #variance #binomial #poisson
