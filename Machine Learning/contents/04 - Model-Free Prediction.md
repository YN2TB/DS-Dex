---
subject: Machine Learning
chapter: 04
tags: [ds, reinforcement-learning, monte-carlo, temporal-difference, td-lambda, eligibility-traces]
source: "lecture-4-model-free-prediction-.pdf — David Silver, UCL (Lecture 4 of 10)"
---

# Model-Free Prediction

> [!note] Where this sits in the course
> **The transition from planning to learning.**
> - **Last lecture:** planning by DP — *solve a known MDP* ([[03 - Planning by Dynamic Programming]])
> - **This lecture:** model-free **prediction** — *estimate the value function of an **unknown** MDP*
> - **Next lecture:** model-free **control** — *optimise* the value function of an unknown MDP ([[05 - Model-Free Control]])
>
> The prediction/control split is from [[01 - Introduction to Reinforcement Learning]]; the sample-backup idea was foreshadowed at the end of [[03 - Planning by Dynamic Programming]].

## 📘 Main Knowledge

---

## Part 1 — Monte-Carlo Learning

> - MC methods **learn directly from episodes of experience**
> - MC is **model-free**: no knowledge of MDP transitions / rewards
> - MC learns from **complete episodes: no bootstrapping**
> - MC uses **the simplest possible idea: value = mean return**
> - **Caveat: can only apply MC to episodic MDPs — all episodes must terminate**

**Goal:** learn $v_\pi$ from episodes of experience under $\pi$: $S_1, A_1, R_2, \dots, S_k \sim \pi$.

Recall $G_t = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-1}R_T$ and $v_\pi(s) = \mathbb{E}_\pi[G_t\mid S_t = s]$.

> **Monte-Carlo policy evaluation uses the *empirical mean* return instead of the *expected* return.**

That one substitution is the whole method. [[02 - Markov Decision Processes]] defined $v$ as an expectation we could not compute without a model; MC simply estimates it by averaging samples.

**First-visit MC** — to evaluate state $s$, at **the first** time-step $t$ that $s$ is visited in an episode:
- Increment counter $N(s) \leftarrow N(s) + 1$
- Increment total return $S(s) \leftarrow S(s) + G_t$
- Value is estimated by mean return $V(s) = S(s)/N(s)$
- **By the law of large numbers, $V(s) \to v_\pi(s)$ as $N(s) \to \infty$**

**Every-visit MC** — identical, but applied at **every** time-step $s$ is visited. Also converges.

### Blackjack example

- **States (200):** current sum (12–21) · dealer's showing card (ace–10) · usable ace? (yes/no)
- **Actions:** *stick* (stop receiving cards, terminate) · *twist* (take another card, no replacement)
- **Reward for stick:** +1 if sum > dealer, 0 if equal, −1 if less
- **Reward for twist:** −1 if bust *(truncated in source)*, 0 otherwise

Policy evaluated: *stick if sum ≥ 20, otherwise twist*.

**Blackjack is the ideal MC example** because the transition dynamics are hopelessly complicated to write down (card counting without replacement) while *sampling* an episode is trivial — deal cards. That is exactly the model-free advantage.

### Incremental Monte-Carlo

**The incremental mean** — the mean of a sequence can be computed without storing it:
$$\mu_k = \frac{1}{k}\sum_{j=1}^{k}x_j = \frac{1}{k}\big(x_k + (k-1)\mu_{k-1}\big) = \mu_{k-1} + \frac{1}{k}(x_k - \mu_{k-1})$$

**Incremental MC updates** — after episode $S_1,A_1,R_2,\dots,S_T$, for each state $S_t$ with return $G_t$:
$$N(S_t) \leftarrow N(S_t) + 1 \qquad V(S_t) \leftarrow V(S_t) + \frac{1}{N(S_t)}\big(G_t - V(S_t)\big)$$

> In **non-stationary** problems it can be useful to track a **running mean**, i.e. **forget old episodes**:
> $$V(S_t) \leftarrow V(S_t) + \alpha\big(G_t - V(S_t)\big)$$

Replacing $1/N$ with a constant $\alpha$ turns the exact average into an exponentially weighted one — essential when the environment changes, and the form every subsequent algorithm uses.

---

## Part 2 — Temporal-Difference Learning

> - TD methods **learn directly from episodes of experience**
> - TD is **model-free**
> - **TD learns from *incomplete* episodes, by bootstrapping**
> - **TD updates a guess towards a guess**

**The two updates side by side:**

$$\text{MC: } \quad V(S_t) \leftarrow V(S_t) + \alpha\big(\underbrace{G_t}_{\text{actual return}} - V(S_t)\big)$$

$$\text{TD(0): } \quad V(S_t) \leftarrow V(S_t) + \alpha\big(\underbrace{R_{t+1} + \gamma V(S_{t+1})}_{\text{estimated return}} - V(S_t)\big)$$

- $R_{t+1} + \gamma V(S_{t+1})$ is the **TD target**
- $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ is the **TD error**

**The TD target is the right-hand side of the Bellman equation, sampled.** DP computed $\mathbb{E}_\pi[R_{t+1} + \gamma v(S_{t+1})]$ exactly using the model; TD uses one sampled transition instead.

### Driving Home example

| State | Elapsed Time | Predicted Time to Go | Predicted Total Time |
|---|---|---|---|
| leaving office | 0 | 30 | 30 |
| reach car, raining | 5 | 35 | 40 |
| exit highway | 20 | 15 | 35 |
| behind truck | 30 | 10 | 40 |
| home street | 40 | 3 | 43 |
| arrive home | 43 | 0 | 43 |

**MC waits until you arrive home (43 minutes) and revises every earlier prediction toward 43. TD revises each prediction toward the *next* prediction, immediately.** When it starts raining and the estimate jumps from 30 to 40, TD updates the "leaving office" estimate at once — it does not need to know how the journey ends to learn that rain is bad news.

### MC vs TD

> - **TD can learn *before* knowing the final outcome** — online, after every step. **MC must wait until the end of the episode.**
> - **TD can learn *without* the final outcome** — from incomplete sequences. **MC can only learn from complete sequences.**
> - **TD works in continuing (non-terminating) environments. MC only works for episodic** ones.

### Bias/variance trade-off

- The return $G_t$ is an **unbiased** estimate of $v_\pi(S_t)$
- The **true** TD target $R_{t+1} + \gamma v_\pi(S_{t+1})$ is **unbiased**
- The **actual** TD target $R_{t+1} + \gamma V(S_{t+1})$ is **biased** — it uses the current estimate $V$, not the truth
- **The TD target has much lower variance** than the return: the return depends on **many** random actions, transitions, and rewards; the TD target depends on **one**

| **MC** | **TD** |
|---|---|
| **High variance, zero bias** | **Low variance, some bias** |
| Good convergence properties (**even with function approximation**) | Usually **more efficient** than MC |
| Not very sensitive to initial value | TD(0) converges to $v_\pi(s)$ — **but not always with function approximation** |
| Very simple to understand and use | **More sensitive to initial value** |

The parenthetical warnings about function approximation are the seed of the "deadly triad" in [[06 - Value Function Approximation]].

### Batch MC and TD — the AB example

Both converge as experience $\to\infty$. **But what about the batch solution for finite experience?** Repeatedly sample episodes and apply MC or TD(0).

**Two states A, B; no discounting; 8 episodes:**
```
A, 0, B, 0
B, 1
B, 1
B, 1
B, 1
B, 1
B, 1
B, 0
```
**What is $V(A)$ and $V(B)$?**

$V(B) = 6/8 = 0.75$ — both methods agree. **$V(A)$ is where they diverge** (Exercise 2).

> **MC converges to the solution with minimum mean-squared error** — the best fit to the observed returns:
> $$\sum_{k=1}^{K}\sum_{t=1}^{T_k}\big(G^k_t - V(s^k_t)\big)^2$$
> **In the AB example, $V(A) = 0$.**
>
> **TD(0) converges to the solution of the maximum likelihood Markov model** — the solution to the MDP $\langle\mathcal{S},\mathcal{A},\hat{\mathcal{P}},\hat{\mathcal{R}},\gamma\rangle$ that best fits the data:
> $$\hat{\mathcal{P}}^a_{s,s'} = \frac{1}{N(s,a)}\sum_{k=1}^{K}\sum_{t=1}^{T_k}\mathbb{1}(s^k_t, a^k_t, s^k_{t+1} = s,a,s')$$

> **TD exploits the Markov property** — usually more efficient in Markov environments.
> **MC does not exploit the Markov property** — usually more effective in **non-Markov** environments.

### Unified view

| | **Bootstrapping** (update involves an estimate) | **Sampling** (update samples an expectation) |
|---|---|---|
| **MC** | No | **Yes** |
| **DP** | **Yes** | No |
| **TD** | **Yes** | **Yes** |

$$\text{MC: } V(S_t) \leftarrow V(S_t) + \alpha(G_t - V(S_t)) \qquad \text{deep, sampled}$$
$$\text{TD: } V(S_t) \leftarrow V(S_t) + \alpha(R_{t+1} + \gamma V(S_{t+1}) - V(S_t)) \qquad \text{shallow, sampled}$$
$$\text{DP: } V(S_t) \leftarrow \mathbb{E}_\pi[R_{t+1} + \gamma V(S_{t+1})] \qquad \text{shallow, full-width}$$

**TD is the combination of both ideas**, which is why it is the most practically important. The two axes — depth of backup, and full-width vs sampled — organise the whole field, and exhaustive search sits at the fourth corner (deep and full-width).

---

## Part 3 — TD(λ)

### n-step returns

Let the TD target look $n$ steps into the future:

| $n$ | Return |
|---|---|
| $n = 1$ (**TD**) | $G^{(1)}_t = R_{t+1} + \gamma V(S_{t+1})$ |
| $n = 2$ | $G^{(2)}_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 V(S_{t+2})$ |
| ⋮ | |
| $n = \infty$ (**MC**) | $G^{(\infty)}_t = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-1}R_T$ |

$$G^{(n)}_t = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{n-1}R_{t+n} + \gamma^n V(S_{t+n})$$
$$V(S_t) \leftarrow V(S_t) + \alpha\big(G^{(n)}_t - V(S_t)\big)$$

**MC and TD are the two endpoints of one spectrum**, and intermediate $n$ usually beats both.

### The λ-return (forward view)

> We can **average** $n$-step returns over different $n$ — e.g. $\tfrac12 G^{(2)} + \tfrac12 G^{(4)}$. **Can we efficiently combine information from all time-steps?**

> The **λ-return** $G^\lambda_t$ combines **all** $n$-step returns using weight $(1-\lambda)\lambda^{n-1}$:
> $$G^\lambda_t = (1-\lambda)\sum_{n=1}^{\infty}\lambda^{n-1}G^{(n)}_t$$
>
> **Forward-view TD(λ):**
> $$V(S_t) \leftarrow V(S_t) + \alpha\big(G^\lambda_t - V(S_t)\big)$$

The weights decay geometrically and sum to 1. **$\lambda = 0$ recovers TD(0); $\lambda = 1$ recovers MC.**

> **Forward view looks into the future to compute $G^\lambda_t$. Like MC, it can only be computed from complete episodes.**

### Eligibility traces (backward view)

> **Forward view provides theory; backward view provides mechanism** — update **online, every step, from incomplete sequences**.

> **Credit assignment problem: did bell or light cause shock?**
> - **Frequency heuristic:** assign credit to the most **frequent** states
> - **Recency heuristic:** assign credit to the most **recent** states
> - **Eligibility traces combine both:**
> $$E_0(s) = 0 \qquad E_t(s) = \gamma\lambda E_{t-1}(s) + \mathbb{1}(S_t = s)$$

The trace **decays** by $\gamma\lambda$ each step (recency) and **increments** on each visit (frequency).

> **Backward view TD(λ):** keep an eligibility trace for every state $s$, and update $V(s)$ for **every** state in proportion to the TD error and the trace:
> $$\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \qquad V(s) \leftarrow V(s) + \alpha\delta_t E_t(s)$$

**One TD error updates every state at once**, weighted by how "responsible" each is — which is what makes it online and incremental.

### Forward/backward equivalence

**TD(λ) and TD(0):** when $\lambda = 0$, $E_t(s) = \mathbb{1}(S_t = s)$, so only the current state is updated — **exactly the TD(0) update** $V(S_t) \leftarrow V(S_t) + \alpha\delta_t$.

**TD(λ) and MC:** when $\lambda = 1$, credit is deferred until the end of the episode. **Over an episode, the total update for TD(1) equals the total update for MC.**

> **Theorem.** The sum of **offline** updates is identical for forward-view and backward-view TD(λ):
> $$\sum_{t=1}^{T}\alpha\delta_t E_t(s) = \sum_{t=1}^{T}\alpha\big(G^\lambda_t - V(S_t)\big)\mathbb{1}(S_t = s)$$

**The mechanism is telescoping.** At $\lambda = 1$, the discounted sum of TD errors collapses into the MC error:
$$\begin{aligned}\delta_t + \gamma\delta_{t+1} + \gamma^2\delta_{t+2} + \dots + \gamma^{T-1-t}\delta_{T-1} &= R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \\ &\quad + \gamma R_{t+2} + \gamma^2 V(S_{t+2}) - \gamma V(S_{t+1}) \\ &\quad + \dots \\ &= R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-1-t}R_T - V(S_t) \\ &= G_t - V(S_t)\end{aligned}$$

**Every intermediate $V$ term cancels with its neighbour** — the $+\gamma V(S_{t+1})$ from one line against the $-\gamma V(S_{t+1})$ from the next. For general $\lambda$ the same telescoping yields the λ-error $G^\lambda_t - V(S_t)$, with $(\gamma\lambda)^k$ in place of $\gamma^k$.

**Summary of equivalences:**

| Offline updates | $\lambda = 0$ | $\lambda \in (0,1)$ | $\lambda = 1$ |
|---|---|---|---|
| Backward view | TD(0) | TD(λ) | TD(1) |
| | **=** | **=** | **=** |
| Forward view | TD(0) | Forward TD(λ) | **MC** |

| Online updates | $\lambda = 0$ | $\lambda \in (0,1)$ | $\lambda = 1$ |
|---|---|---|---|
| Backward view | TD(0) | TD(λ) | TD(1) |
| | **=** | **≠** | **≠** |
| Forward view | TD(0) | Forward TD(λ) | MC |
| | **=** | **=** | **=** |
| **Exact Online** | Exact Online TD(0) | Exact Online TD(λ) | Exact Online TD(1) |

> **NEW: Exact online TD(λ) achieves perfect equivalence** by using a slightly different form of eligibility trace — **Sutton and van Seijen, ICML 2014**.

## ✏️ Exercises

**1.** Explain what "TD updates a guess towards a guess" means, and why bootstrapping introduces bias but reduces variance.

> [!example]- Solution
> **The phrase describes the TD target.** $V(S_t)$ is a guess at $v_\pi(S_t)$. The target $R_{t+1} + \gamma V(S_{t+1})$ contains $V(S_{t+1})$ — **another guess**. So we adjust one estimate toward a quantity built from a different estimate. MC, by contrast, updates a guess toward $G_t$, an actual observed outcome.
>
> **Why this introduces bias.** If $V(S_{t+1})$ is wrong — and initially it is, being whatever we initialised it to — then the target is systematically wrong. Formally: the **true** TD target $R_{t+1} + \gamma v_\pi(S_{t+1})$ is unbiased by the Bellman equation, but we do not have $v_\pi$; substituting the current estimate makes $\mathbb{E}[\text{target}] \ne v_\pi(S_t)$.
>
> **Why it reduces variance — dramatically.** $G_t$ accumulates randomness from **every** action, transition, and reward for the rest of the episode. Over 100 steps, that is hundreds of random variables compounding. The TD target contains **one** random action, **one** transition, **one** reward — everything beyond is absorbed into the deterministic (if biased) $V(S_{t+1})$.
>
> **The Driving Home example makes it concrete.** The MC target for "leaving office" is the actual 43 minutes, which on another day might be 35 or 60 depending on traffic, weather, and luck — high variance. The TD target is 5 + 35 = 40, reflecting only what was learned in the first five minutes.
>
> **Why the trade-off usually favours TD.** Bias **decreases as $V$ improves** — it is a transient property of a converging estimate. Variance does not decrease; it is a permanent property of the environment's stochasticity. So TD trades a shrinking problem for a persistent one, which is why it is *"usually more efficient than MC"*.
>
> **The caveats matter, though.** Bias makes TD **more sensitive to initialisation** — a bad $V_0$ propagates before washing out. And with **function approximation**, bootstrapping can cause divergence rather than mere bias, because the errors feed back through shared parameters. That is why the lecture notes MC has good convergence *"even with function approximation"* while TD *"not always"* does — the deadly triad of [[06 - Value Function Approximation]].

**2.** *(AB example)* Given the 8 episodes, compute $V(A)$ under batch MC and batch TD(0). Explain why they differ and which is "right".

> [!example]- Solution
> **$V(B) = 0.75$** under both: B appears 8 times with returns 1,1,1,1,1,1,0 (and 0 in the first episode) — $6/8$.
>
> **$V(A)$ splits the methods.**
>
> **Batch MC: $V(A) = 0$.** A is visited once, in episode 1, and that episode's return from A is $0 + 0 = 0$. MC's answer is the mean of observed returns from A — a single sample of 0. It **minimises mean-squared error on the observed data**, and 0 is the best fit to the one return we saw.
>
> **Batch TD(0): $V(A) = 0.75$.** TD builds the **maximum likelihood Markov model** from the data:
> - From A, we observed one transition: **A → B with probability 1**, reward 0
> - From B, the value is 0.75
>
> So $V(A) = 0 + \gamma V(B) = 0.75$ (no discounting).
>
> **Why they differ — the Markov assumption.** TD *believes the data forms an MDP*. It reasons: "A always leads to B; B is worth 0.75; therefore A is worth 0.75." It uses information about B gathered from **seven other episodes** to inform its estimate of A. **MC refuses to make that inference** — it only knows what happened *from A*, and that was 0.
>
> **Which is right?** Neither, absolutely — and that is the point.
>
> **If the environment is genuinely Markov, TD is right.** The single episode from A was unlucky; A really does lead to B, and B really is worth 0.75. TD generalises correctly and will converge faster.
>
> **If the environment is not Markov, MC is right.** Perhaps A → B is a *different kind of* B — the state representation is inadequate and A's successor genuinely behaves differently. MC makes no such assumption and reports exactly what was observed.
>
> **This is the lecture's conclusion:** *"TD exploits the Markov property — usually more efficient in Markov environments. MC does not — usually more effective in non-Markov environments."* The AB example is the cleanest possible demonstration, because the two answers differ maximally on eight tiny episodes.

**3.** Explain the unified view (bootstrapping × sampling) and where exhaustive search fits.

> [!example]- Solution
> Two independent binary choices:
>
> **Bootstrapping — does the update use an estimate of a later value?**
> **Sampling — does the update use sampled transitions rather than the full expectation?**
>
> | | Bootstraps | Samples | Backup shape |
> |---|---|---|---|
> | **DP** | ✓ | ✗ | shallow, full-width |
> | **MC** | ✗ | ✓ | **deep**, sampled |
> | **TD** | ✓ | ✓ | shallow, sampled |
> | **Exhaustive search** | ✗ | ✗ | **deep, full-width** |
>
> **The fourth corner is exhaustive search** — expand the complete tree of all trajectories to termination, considering every branch with its true probability. No estimates (it reaches real terminal rewards), no sampling (it enumerates everything). It is exact and almost always computationally impossible.
>
> **Reading the axes:**
>
> **Sampling breaks the curse of dimensionality.** Full-width backups cost $O(|\mathcal{S}|)$ per state; sampled backups cost $O(1)$ — the point at the end of [[03 - Planning by Dynamic Programming]]. It also removes the need for a model, since you can sample without being able to write $\mathcal{P}$ down.
>
> **Bootstrapping breaks the dependence on episode length.** Deep backups need the episode to finish; shallow ones need one step. That is why TD works in continuing tasks and MC does not.
>
> **TD takes both**, which is why it dominates in practice — constant cost per update, model-free, and online. Its price is bias, and instability under function approximation.
>
> **The view also explains TD(λ) as a continuous dial on the depth axis.** $\lambda = 0$ is fully shallow (TD), $\lambda = 1$ fully deep (MC), and intermediate values interpolate. The best $\lambda$ is usually neither endpoint — which is the real argument for TD(λ) existing at all.

**4.** Show that the eligibility trace update reduces to TD(0) at $\lambda=0$, and explain the two heuristics it combines.

> [!example]- Solution
> **At $\lambda = 0$:**
> $$E_t(s) = \gamma\lambda E_{t-1}(s) + \mathbb{1}(S_t = s) = 0 + \mathbb{1}(S_t = s) = \mathbb{1}(S_t = s)$$
> The trace is 1 for the current state and 0 everywhere else — it has no memory. The update
> $$V(s) \leftarrow V(s) + \alpha\delta_t E_t(s)$$
> therefore changes only $S_t$:
> $$V(S_t) \leftarrow V(S_t) + \alpha\delta_t$$
> **which is exactly TD(0).**
>
> **The two heuristics**, motivated by the credit assignment question *"did bell or light cause shock?"*:
>
> **Recency** — the **decay** term $\gamma\lambda E_{t-1}(s)$. Each step, every trace shrinks by $\gamma\lambda$, so states visited long ago have small traces and receive little credit. A stimulus 20 steps before the shock is less likely to be responsible than one 2 steps before.
>
> **Frequency** — the **increment** $+\mathbb{1}(S_t = s)$. Each visit adds 1, so a state visited repeatedly accumulates a larger trace. A bell that rang five times before the shock is more suspicious than one that rang once.
>
> **Combining them is the insight.** Recency alone would credit only the last state (that is $\lambda=0$); frequency alone would ignore timing entirely. The trace multiplies them: credit ∝ how often *and* how recently.
>
> **Why the decay is $\gamma\lambda$ and not just $\lambda$.** The $\gamma$ accounts for discounting — a reward $k$ steps later is worth $\gamma^k$, so credit for causing it should decay at that rate too. The $\lambda$ is the extra tunable decay that interpolates toward MC. Their product gives the $(\gamma\lambda)^{t-k}$ that appears in the equivalence proof.
>
> **The computational point:** the backward view needs only **one number per state** and updates everything from **one** TD error per step. The forward view needs the whole future to compute $G^\lambda_t$. Same algorithm, but only the backward view can run online.

**5.** (Advanced) Explain the telescoping argument proving forward/backward equivalence, and why the equivalence holds offline but not online.

> [!example]- Solution
> **The telescoping.** Write out the discounted sum of TD errors at $\lambda=1$:
> $$\begin{aligned}\delta_t &= R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \\ \gamma\delta_{t+1} &= \gamma R_{t+2} + \gamma^2 V(S_{t+2}) - \gamma V(S_{t+1}) \\ \gamma^2\delta_{t+2} &= \gamma^2 R_{t+3} + \gamma^3 V(S_{t+3}) - \gamma^2 V(S_{t+2})\end{aligned}$$
>
> **Each line's $+\gamma^k V(S_{t+k})$ cancels the next line's $-\gamma^k V(S_{t+k})$.** Every intermediate value estimate vanishes, leaving only the first $-V(S_t)$ and the rewards:
> $$\sum_{k=0}^{T-1-t}\gamma^k\delta_{t+k} = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-1-t}R_T - V(S_t) = G_t - V(S_t)$$
>
> **This is the MC error.** So accumulating TD errors along a trajectory *is* computing the MC update — incrementally, without waiting.
>
> For general $\lambda$ the same cancellation occurs with $(\gamma\lambda)^k$, yielding $G^\lambda_t - V(S_t)$. The mechanism is identical; only the decay rate differs.
>
> **Why offline equivalence holds.** *Offline* means updates are **accumulated during the episode but applied in batch at the end**. So the $V$ values appearing in every $\delta_t$ are the **same** throughout the episode — frozen. The telescoping is pure algebra on fixed numbers, and it is exact.
>
> **Why online equivalence fails.** *Online* means $V$ is updated **at every step**. Now the $V(S_{t+1})$ used in $\delta_t$ is not the same $V(S_{t+1})$ used a moment later in $\delta_{t+1}$ — it has already been changed by the update. **The terms no longer cancel**, because they are no longer the same quantity.
>
> The lecture's summary table records this precisely: online, forward and backward TD(λ) are **≠** for $\lambda > 0$, while both still equal TD(0) at $\lambda = 0$ (where there is nothing to telescope).
>
> **How much does it matter?** In practice the discrepancy is small for small $\alpha$ — the values barely move within one episode, so the approximation is good. But it is a genuine gap between the theory (forward view) and the mechanism (backward view).
>
> **Exact online TD(λ)** (Sutton & van Seijen, ICML 2014) closes it with a modified trace that explicitly compensates for the intra-episode changes to $V$, achieving **perfect equivalence with online updates** — the bottom row of the table, where every column reads **=**.

## 📝 Summary

- **Model-free prediction estimates $v_\pi$ for an unknown MDP** — no $\mathcal{P}$, no $\mathcal{R}$, only experience.
- **MC: value = mean return.** Learns from **complete episodes**, no bootstrapping, **episodic tasks only**.
- **First-visit and every-visit MC** both converge by the law of large numbers.
- **Incremental mean** $\mu_k = \mu_{k-1} + \frac{1}{k}(x_k - \mu_{k-1})$; replacing $1/k$ with constant $\alpha$ forgets old episodes — needed for non-stationary problems.
- **TD(0): update a guess toward a guess.** Target $R_{t+1} + \gamma V(S_{t+1})$, error $\delta_t$. Learns **online, from incomplete sequences, in continuing tasks**.
- **MC is unbiased with high variance; TD is biased with low variance.** TD is usually more efficient, but more sensitive to initialisation and to function approximation.
- **Batch MC minimises MSE on observed returns; batch TD finds the maximum-likelihood Markov model.** Hence **TD exploits the Markov property, MC does not**.
- **Unified view:** MC samples but does not bootstrap; DP bootstraps but does not sample; **TD does both**; exhaustive search does neither.
- **$n$-step returns interpolate between TD ($n=1$) and MC ($n=\infty$).**
- **λ-return** $G^\lambda_t = (1-\lambda)\sum_n \lambda^{n-1}G^{(n)}_t$ averages all $n$-step returns geometrically.
- **Eligibility traces** $E_t(s) = \gamma\lambda E_{t-1}(s) + \mathbb{1}(S_t=s)$ combine **recency** (decay) and **frequency** (increment), giving an online mechanism for the forward view.
- **Forward and backward TD(λ) are equivalent offline**, by telescoping of TD errors; **online they differ** unless exact online TD(λ) is used.

## ⚠️ Important Notes

**MC requires episodes to terminate.** It cannot be applied to continuing tasks at all — a hard restriction, not a preference.

**The MC bias/variance claim is about the *estimator*, not the algorithm's error.** MC is unbiased but can be badly wrong on any given sample; TD is biased but its bias shrinks as $V$ improves, while MC's variance does not shrink.

**Constant-$\alpha$ MC is not the same as first-visit MC.** Using $\alpha$ instead of $1/N$ gives an exponentially weighted average that tracks a changing environment — and no longer converges to the exact mean.

**Batch MC and batch TD converge to different answers on the same data.** The AB example gives $V(A) = 0$ versus $0.75$. Neither is a bug; they optimise different criteria.

**TD's advantage depends on the Markov property actually holding.** In a non-Markov environment TD's inference is unjustified and MC is more reliable.

**Bootstrapping plus function approximation is dangerous.** MC converges even with function approximation; TD does not always. This is the deadly triad, and it is why the caveat appears twice in this lecture.

**TD is more sensitive to initial values** because the bootstrapped target propagates the initialisation before it washes out.

**The best $n$ (or $\lambda$) is usually neither endpoint.** Both TD(0) and MC are typically outperformed by intermediate values — which is the entire justification for TD(λ).

**Forward-view TD(λ) cannot run online** — computing $G^\lambda_t$ needs the whole future. Only the backward view is implementable incrementally.

**Forward/backward equivalence is exact only for offline updates.** Online, the $V$ values change mid-episode and the telescoping breaks. Exact online TD(λ) repairs it.

**The eligibility trace decays by $\gamma\lambda$, not $\lambda$.** The $\gamma$ is not optional — it makes the credit decay match the discounting of the reward being credited.

> [!warning] Gaps in the source slides
> Silver's slides extract very well; **all equations, theorems, and the telescoping derivations survived.** Losses are figures:
> - **Slide 9** — the Blackjack value function surface plots after MC learning (usable/no-usable ace) are images.
> - **Slide 15 — "Driving Home: MC vs TD"** is the pair of plots showing which predictions each method revises; only the captions extracted. **This is the lecture's clearest visual intuition and it is lost** — the data table on slide 14 survived, so the example is reconstructible.
> - **Slides 19–20 (Random Walk)** and **slide 33 (Large Random Walk)** and **slide 38 (Forward-View TD(λ) on Large Random Walk)** — the learning-curve plots comparing MC, TD, and various $n$ and $\lambda$ are **entirely images**. These are the empirical evidence that intermediate $n$/$\lambda$ beats both endpoints, and none of it is captured.
> - **Slides 26–28, 30** — the backup diagrams and the **Unified View of RL** figure (the two-axis map of DP/MC/TD/exhaustive search) are images; I have reconstructed the unified view as a table.
> - **Slides 31, 36** — the $n$-step prediction diagram and the TD(λ) weighting function plot.
> - **Truncations:** slide 8 (**the twist reward is cut at *"-1 if"*** — standard is "−1 if sum > 21, 0 otherwise"), slide 13 (cut at *"$\delta_t = \dots$ i"* — "is called the TD error"), slide 16 (cut at *"MC only works for episodic"*), slide 24 ($\hat{\mathcal{R}}$ formula cut), slide 34 (cut at "One backup"), slide 47 (the general-λ telescoping cut mid-line), slide 48 (**cut at *"For multiple visits to s, E"*** — the trace accumulation rule for repeat visits is lost).
> - **Slides 22 and 23 are duplicates** — the Beamer overlay showing the AB example question then (presumably) the answer; both extracted identically, so **the answer slide's content is not recoverable**.
>
> **Reference:** Sutton and van Seijen, *True Online TD(λ)*, ICML 2014.

---
**Previous:** [[03 - Planning by Dynamic Programming]] · **Next:** [[05 - Model-Free Control]]
