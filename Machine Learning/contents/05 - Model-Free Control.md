---
subject: Machine Learning
chapter: 05
tags: [ds, reinforcement-learning, sarsa, q-learning, epsilon-greedy, off-policy]
source: "lecture-5-model-free-control-.pdf — David Silver, UCL (Lecture 5 of 10)"
---

# Model-Free Control

> [!note] Where this sits in the course
> The **culmination of Part I**. [[04 - Model-Free Prediction]] estimated $v_\pi$ for an unknown MDP; this lecture **optimises** it. Everything here is Generalised Policy Iteration ([[03 - Planning by Dynamic Programming]]) with the evaluation step replaced by MC or TD — and it delivers the two most-used algorithms in RL: **Sarsa** and **Q-learning**.

## 📘 Main Knowledge

**Problems that can be modelled as MDPs:** elevator · parallel parking · ship steering · bioreactor · helicopter · aeroplane logistics · Robocup soccer · Quake · portfolio management · protein folding · robot walking · Game of Go.

> For most of these, either:
> - **The MDP model is unknown, but experience can be sampled**, or
> - **The MDP model is known, but too big to use, except by samples**
>
> Model-free control can solve *(truncated)* both.

That second bullet is easy to miss and important: Go's rules are perfectly known, yet DP is impossible because $|\mathcal{S}| \approx 10^{170}$. **Model-free methods are needed even when a model exists.**

### On-policy vs off-policy

> **On-policy learning** — *"Learn on the job."* Learn about policy $\pi$ from experience **sampled from $\pi$**.
>
> **Off-policy learning** — *"Look over someone's shoulder."* Learn about policy $\pi$ from experience **sampled from $\mu$**.

---

## Part 1 — On-Policy Monte-Carlo Control

### Why $Q$ rather than $V$

Generalised Policy Iteration alternates evaluation and improvement. Substituting MC evaluation raises an immediate problem:

> **Greedy policy improvement over $V(s)$ requires a model of the MDP:**
> $$\pi'(s) = \arg\max_{a\in\mathcal{A}} \mathcal{R}^a_s + \mathcal{P}^a_{ss'}V(s')$$
>
> **Greedy policy improvement over $Q(s,a)$ is model-free:**
> $$\pi'(s) = \arg\max_{a\in\mathcal{A}} Q(s,a)$$

**This is the reason model-free control learns action-values.** Improving a policy from $V$ needs a one-step lookahead, which needs $\mathcal{P}$ and $\mathcal{R}$. $Q$ already stores the answer for each action, so the $\arg\max$ needs nothing. It is exactly the point [[02 - Markov Decision Processes]] made — *"if we know $q_*$, we immediately have the optimal policy."*

### The exploration problem

> **There are two doors in front of you.**
> - You open the **left** door and get reward 0 → $V(\text{left}) = 0$
> - You open the **right** door and get reward +1 → $V(\text{right}) = +1$
> - You open the **right** door and get reward +3 → $V(\text{right}) = +2$
> - You open the **right** door and get reward +2 → $V(\text{right}) = +2$
> - …
>
> **Are you sure you've chosen the best door?**

**No** — the left door was tried once and may have been unlucky. Pure greedy action selection can lock onto a suboptimal action forever, because it never gathers the evidence that would change its mind.

### ε-greedy exploration

> The **simplest idea for ensuring continual exploration**. All $m$ actions are tried with non-zero probability: with probability $1-\epsilon$ choose the greedy action, with probability $\epsilon$ choose an action at random.
>
> $$\pi(a\mid s) = \begin{cases}\epsilon/m + 1 - \epsilon & \text{if } a^* = \arg\max_{a\in\mathcal{A}} Q(s,a) \\ \epsilon/m & \text{otherwise}\end{cases}$$

> **Theorem.** For any $\epsilon$-greedy policy $\pi$, the $\epsilon$-greedy policy $\pi'$ with respect to $q_\pi$ is an improvement: $v_{\pi'}(s) \ge v_\pi(s)$.
>
> $$\begin{aligned} q_\pi(s,\pi'(s)) &= \sum_{a\in\mathcal{A}}\pi'(a\mid s)q_\pi(s,a) \\ &= \frac{\epsilon}{m}\sum_{a\in\mathcal{A}}q_\pi(s,a) + (1-\epsilon)\max_{a\in\mathcal{A}}q_\pi(s,a) \\ &\ge \frac{\epsilon}{m}\sum_{a\in\mathcal{A}}q_\pi(s,a) + (1-\epsilon)\sum_{a\in\mathcal{A}}\frac{\pi(a\mid s) - \epsilon/m}{1-\epsilon}q_\pi(s,a) \\ &= \sum_{a\in\mathcal{A}}\pi(a\mid s)q_\pi(s,a) = v_\pi(s)\end{aligned}$$
>
> Therefore by the policy improvement theorem, $v_{\pi'}(s) \ge v_\pi(s)$.

**This theorem is what makes exploration safe.** Without it, adding randomness to a greedy policy might destroy the monotone-improvement guarantee of [[03 - Planning by Dynamic Programming]]. The proof shows the $\max$ dominates *any* weighted average of $q$ values — including the one the old policy produces.

### GLIE

> **Greedy in the Limit with Infinite Exploration (GLIE).**
> - **All state-action pairs are explored infinitely many times:** $\lim_{k\to\infty}N_k(s,a) = \infty$
> - **The policy converges on a greedy policy:** $\lim_{k\to\infty}\pi_k(a\mid s) = \mathbb{1}(a = \arg\max_{a'}Q_k(s,a'))$
>
> For example, **$\epsilon$-greedy is GLIE if $\epsilon$ reduces to zero at $\epsilon_k = \tfrac1k$.**

The two conditions pull in opposite directions and GLIE reconciles them: explore enough to guarantee correct values, but stop exploring eventually so the policy becomes optimal rather than merely near-optimal.

**GLIE Monte-Carlo Control** — sample the $k$th episode using $\pi$, then for each $S_t, A_t$ in the episode:
$$N(S_t,A_t) \leftarrow N(S_t,A_t) + 1$$
$$Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \frac{1}{N(S_t,A_t)}\big(G_t - Q(S_t,A_t)\big)$$
Then improve: $\epsilon \leftarrow 1/k$, $\pi \leftarrow \epsilon\text{-greedy}(Q)$.

> **Theorem.** GLIE Monte-Carlo control converges to the optimal action-value function, $Q(s,a) \to q_*(s,a)$.

Note the loop runs **every episode**, not after full evaluation — approximate evaluation is enough, exactly as GPI permits.

---

## Part 2 — On-Policy TD: Sarsa

> TD has several advantages over MC — **lower variance, online, incomplete sequences**. **Natural idea: use TD instead of MC in the control loop.** Apply TD to $Q(S,A)$, use $\epsilon$-greedy improvement, and **update every time-step**.

### Sarsa

$$\boxed{Q(S,A) \leftarrow Q(S,A) + \alpha\big(R + \gamma Q(S',A') - Q(S,A)\big)}$$

**The name is the update's ingredients: $S, A, R, S', A'$.** It requires knowing the *actual next action* $A'$ — which is why it is on-policy.

**On-policy control with Sarsa** — every **time-step**:
- **Policy evaluation:** Sarsa, $Q \approx q_\pi$
- **Policy improvement:** $\epsilon$-greedy

The loop now turns once per *step* rather than once per episode — the fastest possible GPI.

> **Theorem.** Sarsa converges to the optimal action-value function, $Q(s,a) \to q_*(s,a)$, under:
> - **GLIE** sequence of policies $\pi_t(a\mid s)$
> - **Robbins–Monro** sequence of step-sizes $\alpha_t$:
> $$\sum_{t=1}^{\infty}\alpha_t = \infty \qquad \sum_{t=1}^{\infty}\alpha_t^2 < \infty$$

The Robbins–Monro conditions say the steps must be **large enough in total to reach anywhere** (first condition) but **shrink fast enough to settle** (second). $\alpha_t = 1/t$ satisfies both; a constant $\alpha$ satisfies the first but not the second, so it never fully converges — it tracks instead, which is often what you want in a non-stationary problem.

### Windy Gridworld

**Reward = −1 per time-step until reaching the goal; undiscounted.** A crosswind pushes the agent upward in some columns, so the shortest path must account for the drift.

### n-step Sarsa and Sarsa(λ)

Exactly parallel to [[04 - Model-Free Prediction]], with $Q$ in place of $V$:

| $n$ | $n$-step Q-return |
|---|---|
| $n=1$ (**Sarsa**) | $q^{(1)}_t = R_{t+1} + \gamma Q(S_{t+1})$ |
| $n=2$ | $q^{(2)}_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 Q(S_{t+2})$ |
| $n=\infty$ (**MC**) | $q^{(\infty)}_t = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{T-1}R_T$ |

$$q^{(n)}_t = R_{t+1} + \dots + \gamma^{n-1}R_{t+n} + \gamma^n Q(S_{t+n}) \qquad Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \alpha\big(q^{(n)}_t - Q(S_t,A_t)\big)$$

**Forward-view Sarsa(λ):**
$$q^\lambda_t = (1-\lambda)\sum_{n=1}^{\infty}\lambda^{n-1}q^{(n)}_t \qquad Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \alpha\big(q^\lambda_t - Q(S_t,A_t)\big)$$

**Backward view — one eligibility trace per *state-action pair*:**
$$E_0(s,a) = 0 \qquad E_t(s,a) = \gamma\lambda E_{t-1}(s,a) + \mathbb{1}(S_t=s, A_t=a)$$
$$\delta_t = R_{t+1} + \gamma Q(S_{t+1},A_{t+1}) - Q(S_t,A_t) \qquad Q(s,a) \leftarrow Q(s,a) + \alpha\delta_t E_t(s,a)$$

The Gridworld comparison shows the practical payoff: **one-step Sarsa updates only the last action after reaching the goal, while Sarsa(λ) propagates credit back along the whole successful path in a single episode.**

---

## Part 3 — Off-Policy Learning

> **Evaluate target policy $\pi(a\mid s)$** to compute $v_\pi(s)$ or $q_\pi(s,a)$, **while following behaviour policy $\mu(a\mid s)$.**
>
> **Why is this important?**
> - **Learn from observing humans or other agents**
> - **Re-use experience** generated from old policies $\pi_1, \pi_2, \dots, \pi_{t-1}$
> - **Learn about the optimal policy while following an exploratory policy**
> - **Learn about multiple policies while following one policy**

The third bullet is the crucial one: it resolves the exploration/exploitation conflict by **separating the policy you learn about from the policy you act with**.

### Importance sampling

$$\mathbb{E}_{X\sim P}[f(X)] = \sum P(X)f(X) = \sum Q(X)\frac{P(X)}{Q(X)}f(X) = \mathbb{E}_{X\sim Q}\left[\frac{P(X)}{Q(X)}f(X)\right]$$

**For off-policy Monte-Carlo** — multiply corrections along the **whole episode**:
$$G^{\pi/\mu}_t = \frac{\pi(A_t\mid S_t)}{\mu(A_t\mid S_t)}\frac{\pi(A_{t+1}\mid S_{t+1})}{\mu(A_{t+1}\mid S_{t+1})}\cdots\frac{\pi(A_T\mid S_T)}{\mu(A_T\mid S_T)}G_t$$
$$V(S_t) \leftarrow V(S_t) + \alpha\big(G^{\pi/\mu}_t - V(S_t)\big)$$

> **Cannot use if $\mu$ is zero when** *(truncated — "$\pi$ is non-zero")*.

**For off-policy TD** — only a **single** correction is needed:
$$V(S_t) \leftarrow V(S_t) + \alpha\left(\frac{\pi(A_t\mid S_t)}{\mu(A_t\mid S_t)}\big(R_{t+1} + \gamma V(S_{t+1})\big) - V(S_t)\right)$$

> **Much lower variance than Monte-Carlo importance sampling — policies only need to be similar over a single step.**

**Off-policy MC with importance sampling is essentially unusable in practice.** Multiplying dozens of ratios produces variance that explodes exponentially with episode length (Exercise 3).

### Q-Learning

> We now consider off-policy learning of action-values $Q(s,a)$. **No importance sampling is required.**
>
> - The next action is chosen using the behaviour policy, $A_{t+1} \sim \mu(\cdot\mid S_t)$
> - But we consider an **alternative successor action** $A' \sim \pi(\cdot\mid S_t)$
> - And update $Q(S_t,A_t)$ towards the value of the **alternative** action:
> $$Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \alpha\big(R_{t+1} + \gamma Q(S_{t+1},A') - Q(S_t,A_t)\big)$$

**Why no importance sampling is needed:** $Q(S_{t+1}, A')$ can be evaluated for *any* action without having taken it, because $Q$ stores a value per action. There is no distribution to correct — we simply look up the entry we want.

**Off-policy control with Q-learning** — allow **both** policies to improve:
- The **target** policy $\pi$ is **greedy** w.r.t. $Q$: $\pi(S_{t+1}) = \arg\max_{a'}Q(S_{t+1},a')$
- The **behaviour** policy $\mu$ is e.g. **$\epsilon$-greedy** w.r.t. $Q$

The target then simplifies:
$$R_{t+1} + \gamma Q(S_{t+1}, A') = R_{t+1} + \gamma Q\big(S_{t+1}, \arg\max_{a'}Q(S_{t+1},a')\big) = R_{t+1} + \gamma\max_{a'}Q(S_{t+1},a')$$

$$\boxed{Q(S,A) \leftarrow Q(S,A) + \alpha\big(R + \gamma\max_{a'}Q(S',a') - Q(S,A)\big)}$$

> **Theorem.** Q-learning control converges to the optimal action-value function, $Q(s,a) \to q_*(s,a)$.

**Cliff Walking** is the standard example contrasting Sarsa and Q-learning (Exercise 4).

---

## Part 4 — The unifying summary

**Every algorithm in Lectures 3–5 is one of six cells:**

| Bellman equation | **Full Backup (DP)** | **Sample Backup (TD)** |
|---|---|---|
| **Expectation for $v_\pi(s)$** | Iterative Policy Evaluation | **TD Learning** |
| **Expectation for $q_\pi(s,a)$** | Q-Policy Iteration | **Sarsa** |
| **Optimality for $q_*(s,a)$** | Q-Value Iteration | **Q-Learning** |

$$\begin{array}{ll}
V(s) \leftarrow \mathbb{E}[R + \gamma V(S')\mid s] & V(S) \xleftarrow{\alpha} R + \gamma V(S') \\
Q(s,a) \leftarrow \mathbb{E}[R + \gamma Q(S',A')\mid s,a] & Q(S,A) \xleftarrow{\alpha} R + \gamma Q(S',A') \\
Q(s,a) \leftarrow \mathbb{E}[R + \gamma\max_{a'}Q(S',a')\mid s,a] & Q(S,A) \xleftarrow{\alpha} R + \gamma\max_{a'}Q(S',a')
\end{array}$$

where $x \xleftarrow{\alpha} y \equiv x \leftarrow x + \alpha(y - x)$.

**Read the table two ways.** *Horizontally:* replacing the expectation with a sample turns a DP algorithm into a TD algorithm — that is the whole model-free move. *Vertically:* the choice of Bellman equation determines the algorithm — **expectation gives Sarsa, optimality gives Q-learning.** The distinction anticipated in [[02 - Markov Decision Processes]] is exactly this.

## ✏️ Exercises

**1.** Explain why model-free control must learn $Q(s,a)$ rather than $V(s)$.

> [!example]- Solution
> **Because greedy improvement from $V$ requires a model, and greedy improvement from $Q$ does not.**
>
> From $V$:
> $$\pi'(s) = \arg\max_a \left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}V(s')\right)$$
> To evaluate this you must know, **for each action you did not take**, what reward it would give and where it would lead. That is precisely $\mathcal{R}$ and $\mathcal{P}$ — the model we assumed unavailable.
>
> From $Q$:
> $$\pi'(s) = \arg\max_a Q(s,a)$$
> A table lookup. **$Q$ has already absorbed the one-step lookahead** — $q_\pi(s,a)$ is by definition "the value of taking $a$ then following $\pi$", so the model's contribution is baked in during learning.
>
> **The trade-off is size.** $Q$ has $|\mathcal{S}| \times |\mathcal{A}|$ entries against $V$'s $|\mathcal{S}|$ — a factor of $m$ more to store and $m$ times more experience to fill. Model-free control pays that cost because there is no alternative.
>
> **A second, subtler reason.** Even with a model, $Q$ is more convenient for control because the improvement step is $O(m)$ rather than $O(mn)$. This is why the summary table has *"Q-Policy Iteration"* and *"Q-Value Iteration"* as the DP counterparts of Sarsa and Q-learning — the $q$-form is natural for control in both worlds.
>
> This is the same observation [[02 - Markov Decision Processes]] made: knowing $v_*$ does not give the policy without a model; **knowing $q_*$ does.**

**2.** Explain GLIE and why both conditions are necessary. What goes wrong if either fails?

> [!example]- Solution
> **GLIE = Greedy in the Limit with Infinite Exploration**, two conditions:
> 1. **Infinite exploration:** $\lim_{k\to\infty}N_k(s,a) = \infty$ — every state-action pair is tried infinitely often
> 2. **Greedy in the limit:** $\lim_{k\to\infty}\pi_k(a\mid s) = \mathbb{1}(a = \arg\max Q_k)$ — the policy becomes greedy
>
> **If exploration fails** (e.g. $\epsilon = 0$ from the start): some $(s,a)$ pairs are never sampled, so $Q(s,a)$ is never updated and remains at its initialisation. If the true $q_*(s,a)$ for an untried action is high, we never find out. **The two-doors example is exactly this failure** — a greedy agent that gets 0 from the left door and +1 from the right never opens the left door again, and if the left door's true mean were +5 it would never know.
>
> Formally, convergence proofs for MC and Sarsa require every $Q(s,a)$ to receive infinitely many updates; without it the estimates are simply undefined in the limit.
>
> **If greediness fails** (e.g. $\epsilon$ fixed at 0.1 forever): $Q \to q_*$ correctly — the values converge fine. But **the policy never becomes optimal**, because it keeps taking a random action 10% of the time. The agent knows the answer and refuses to act on it. In Cliff Walking that costs real reward, permanently.
>
> **The tension is genuine, and GLIE resolves it by decaying.** $\epsilon_k = 1/k$ works because $\sum 1/k$ diverges — so exploration continues infinitely often — while $1/k \to 0$ — so the policy becomes greedy. Both conditions hold simultaneously.
>
> **Note the parallel with Robbins–Monro for step sizes:** $\sum\alpha_t = \infty$ (enough total movement) and $\sum\alpha_t^2 < \infty$ (eventual settling). GLIE is the same shape of condition applied to exploration rather than to learning rate, and **Sarsa's convergence theorem requires both.**
>
> **In practice both are often violated deliberately.** Constant $\epsilon$ and constant $\alpha$ are standard, because real problems are non-stationary and you *want* continued exploration and continued adaptation. You trade the convergence guarantee for the ability to track a changing environment — the same trade as constant-$\alpha$ MC in [[04 - Model-Free Prediction]].

**3.** Explain why off-policy Monte-Carlo with importance sampling is impractical, while off-policy TD is workable and Q-learning needs no correction at all.

> [!example]- Solution
> **Off-policy MC** multiplies a correction ratio at **every step** of the episode:
> $$G^{\pi/\mu}_t = \prod_{k=t}^{T}\frac{\pi(A_k\mid S_k)}{\mu(A_k\mid S_k)}\, G_t$$
>
> **The variance explodes multiplicatively.** Suppose $\pi$ is greedy and $\mu$ is $\epsilon$-greedy with $\epsilon = 0.1$, $m = 4$ actions. When $\mu$ happens to take the greedy action, the ratio is $1/0.925 \approx 1.08$; when it explores, $\pi$ assigns probability **0** and the ratio is **0** — the entire return is discarded. Over a 100-step episode, the chance that $\mu$ *never* explores is $0.925^{100} \approx 0.04\%$. **About 99.96% of episodes contribute nothing**, and the rare surviving ones carry enormous weight.
>
> Even with both policies stochastic, the product of many ratios has variance growing exponentially in episode length. Estimates become useless.
>
> Note also the constraint: **"cannot use if $\mu$ is zero when $\pi$ is non-zero"** — the behaviour policy must have *coverage* of everything the target policy might do, or the ratio is undefined.
>
> **Off-policy TD needs only one ratio**, because the target $R_{t+1} + \gamma V(S_{t+1})$ spans a single step:
> $$V(S_t) \leftarrow V(S_t) + \alpha\left(\frac{\pi(A_t\mid S_t)}{\mu(A_t\mid S_t)}(R_{t+1} + \gamma V(S_{t+1})) - V(S_t)\right)$$
> **"Policies only need to be similar over a single step."** One ratio has bounded variance; a hundred multiplied ratios do not. This is the same bias/variance logic as MC-vs-TD in [[04 - Model-Free Prediction]], amplified.
>
> **Q-learning needs no correction whatsoever**, which is the elegant part. Importance sampling exists to correct for *sampling actions from the wrong distribution*. But $Q(S_{t+1}, a')$ is a **stored value for a specific action** — we can read off the value of the greedy action without having taken it, and without knowing how likely $\mu$ was to take it.
>
> Formally, the Q-learning target $\max_{a'}Q(S',a')$ contains no expectation over $\pi$ at all. It is a deterministic function of $S'$. The only sampled quantity is $S'$ itself, which comes from $\mathcal{P}$ — **and $\mathcal{P}$ is the same regardless of which policy is acting**. Nothing needs correcting.
>
> **This is why Q-learning is the workhorse off-policy algorithm** and why importance-sampling variants are largely of theoretical interest.

**4.** *(Cliff Walking)* On a gridworld where a shortest path runs alongside a cliff (falling gives −100 and resets), Sarsa learns a safe path away from the edge while Q-learning learns the optimal path along it — yet Sarsa gets more reward during learning. Explain.

> [!example]- Solution
> **The two algorithms are estimating different things, and both are correct about what they estimate.**
>
> **Q-learning** uses $\max_{a'}Q(S',a')$ — the value of the **greedy** policy. It learns $q_*$: the optimal path hugs the cliff, because that is genuinely shortest **if you act greedily**. Q-learning is right.
>
> **Sarsa** uses $Q(S',A')$ where $A'$ is the **action actually taken** — which, under $\epsilon$-greedy, is sometimes random. So Sarsa learns $q_\pi$ for the **$\epsilon$-greedy policy**, and under that policy walking beside a cliff is genuinely dangerous: with probability $\epsilon$ you step off and lose 100. Sarsa is also right — about a different policy.
>
> **The paradox resolves once you see they answer different questions.** Q-learning: *"what is the best path if I act perfectly?"* Sarsa: *"what is the best path given that I sometimes act randomly?"*
>
> **During learning, Sarsa earns more reward** because it accounts for its own exploration. Q-learning walks the cliff edge and falls off $\epsilon$ of the time, repeatedly paying −100. **Yet Q-learning's learned policy is better** — deploy both with $\epsilon = 0$ and Q-learning's path wins.
>
> **The practical guidance:**
> - **Sarsa when the exploration is real and its costs are real** — a physical robot that will actually fall, a live trading system. You want a policy robust to your own randomness.
> - **Q-learning when exploration is a training artefact** you will switch off — a simulator, a game. You want $q_*$ regardless of how you gathered the data.
>
> **This is precisely the expectation-vs-optimality distinction from the summary table**, made concrete. Sarsa samples the **Bellman expectation equation** (evaluate the policy being followed); Q-learning samples the **Bellman optimality equation** (evaluate the best policy). The `max` versus the actual `A'` is the entire difference between the two algorithms and between the two Bellman equations of [[02 - Markov Decision Processes]].
>
> **A footnote worth knowing:** as $\epsilon \to 0$ under GLIE, Sarsa's answer converges to Q-learning's, since the policy it evaluates becomes the greedy one. The divergence is a finite-$\epsilon$ phenomenon.

**5.** (Advanced) Explain the six-cell summary table and what each axis represents.

> [!example]- Solution
> | Bellman equation | **Full Backup (DP)** | **Sample Backup (TD)** |
> |---|---|---|
> | Expectation for $v_\pi$ | Iterative Policy Evaluation | TD Learning |
> | Expectation for $q_\pi$ | Q-Policy Iteration | **Sarsa** |
> | Optimality for $q_*$ | Q-Value Iteration | **Q-Learning** |
>
> **The horizontal axis: expectation vs sample.**
> $$V(s) \leftarrow \mathbb{E}[R + \gamma V(S')\mid s] \qquad\text{versus}\qquad V(S) \xleftarrow{\alpha} R + \gamma V(S')$$
> Moving right replaces $\mathbb{E}[\cdot]$ — which requires knowing $\mathcal{P}$ and summing over all successors — with **one sampled transition**, incorporated at learning rate $\alpha$. This single substitution:
> - makes the algorithm **model-free**
> - makes each backup **$O(1)$** instead of $O(|\mathcal{S}|)$, breaking the curse of dimensionality ([[03 - Planning by Dynamic Programming]])
> - introduces **variance**, which $\alpha$ averages away
>
> **The vertical axis: which Bellman equation, and over $v$ or $q$.**
> - **Rows 1→2** switch from $v$ to $q$. Necessary for **model-free control**, since improving from $v$ needs a model (Exercise 1).
> - **Rows 2→3** switch from the **expectation** equation to the **optimality** equation — from $Q(S',A')$ to $\max_{a'}Q(S',a')$. This is **on-policy → off-policy**: evaluating the policy you follow versus evaluating the greedy policy regardless of what you follow.
>
> **What the table accomplishes pedagogically.** Six algorithms that look unrelated in isolation are revealed as **two choices**: *how do I compute the backup* (exactly or by sampling) and *which Bellman equation am I solving* (expectation over $v$, expectation over $q$, or optimality over $q$). Sarsa and Q-learning differ in exactly one cell position, and that difference is exactly one symbol in the update rule.
>
> **The empty seventh cell is instructive too:** there is no "optimality equation for $v_*$" row in the sample column, because sampling $\max_a(\mathcal{R}^a_s + \gamma\sum\mathcal{P}^a_{ss'}v(s'))$ would require the model to evaluate the $\max$ — you cannot take a max over actions you did not sample without knowing their values. **That is why model-free control uses $q$**, closing the loop back to Exercise 1.
>
> This table is the single most useful summary of Part I, and it is worth reproducing from memory before an exam.

## 📝 Summary

- **Model-free control optimises an unknown MDP**, and is needed even for *known* models that are too large for DP (Go).
- **On-policy** learns about $\pi$ from $\pi$; **off-policy** learns about $\pi$ from $\mu$.
- **Control must learn $Q(s,a)$, not $V(s)$** — greedy improvement from $V$ requires a model; from $Q$ it is a lookup.
- **Pure greedy action selection can lock onto a suboptimal action forever** (the two-doors example).
- **$\epsilon$-greedy** explores with probability $\epsilon$, and the **$\epsilon$-greedy policy improvement theorem** guarantees it still improves.
- **GLIE** = infinite exploration **and** eventual greediness; $\epsilon_k = 1/k$ satisfies both. **GLIE MC control converges to $q_*$.**
- **Sarsa:** $Q(S,A) \xleftarrow{\alpha} R + \gamma Q(S',A')$ — on-policy, updated every time-step. Converges under **GLIE + Robbins–Monro** step sizes.
- **Sarsa(λ)** uses one eligibility trace **per state-action pair** and propagates credit along the whole path in a single episode.
- **Importance sampling** corrects for the wrong sampling distribution; over a full episode the variance explodes, over one TD step it is manageable.
- **Q-learning needs no importance sampling**, because $Q(S',a')$ can be read for any action without taking it.
- **Q-learning:** $Q(S,A) \xleftarrow{\alpha} R + \gamma\max_{a'}Q(S',a')$ — off-policy, converges to $q_*$.
- **The six-cell table** organises everything: expectation vs sample backup × which Bellman equation.

## ⚠️ Important Notes

**Greedy improvement from $V$ requires a model.** This single fact forces all model-free control onto $Q$, at a factor-$m$ cost in table size and sample requirements.

**Without exploration, convergence guarantees fail entirely.** Untried state-action pairs keep their initial values forever — the two-doors trap.

**GLIE needs *both* conditions.** Fixed $\epsilon$ converges to correct values but a permanently suboptimal policy; $\epsilon = 0$ may converge to the wrong values.

**Sarsa's convergence needs Robbins–Monro step sizes** ($\sum\alpha_t = \infty$, $\sum\alpha_t^2 < \infty$). Constant $\alpha$ violates the second condition — it tracks rather than converges, which is usually desirable in practice but voids the theorem.

**Sarsa and Q-learning differ by one symbol and answer different questions.** Sarsa evaluates the policy being followed (including its exploration); Q-learning evaluates the greedy policy. On Cliff Walking they learn genuinely different paths, and both are correct.

**Choose Sarsa when exploration costs are real** (physical robots, live systems); **Q-learning when exploration is a training artefact** you will switch off.

**Off-policy MC with importance sampling is essentially unusable.** The product of per-step ratios has variance growing exponentially with episode length; most episodes contribute zero.

**Importance sampling requires coverage:** $\mu(a\mid s) > 0$ wherever $\pi(a\mid s) > 0$, or the ratio is undefined.

**Q-learning avoids importance sampling because $Q$ stores per-action values.** There is no distribution over actions in its target to correct — only the state transition, which is policy-independent.

**Sarsa(λ) needs a trace per state-action pair**, so memory is $|\mathcal{S}|\times|\mathcal{A}|$ — the same as $Q$ itself, doubling storage.

**Q-learning's convergence theorem assumes tabular representation.** With function approximation, the combination of bootstrapping, off-policy learning, and approximation is the **deadly triad** and can diverge — [[06 - Value Function Approximation]].

> [!warning] Gaps in the source slides
> Silver's slides extract very well; **all update rules, theorems, and proofs survived.** Losses are figures:
> - **Slides 22, 29, 38 — the boxed pseudocode for the Sarsa, Sarsa(λ), and Q-learning algorithms are entirely images.** The update rules appear elsewhere in text, but **the complete algorithm listings (initialisation, loop structure, termination) are not recoverable** — consult Sutton & Barto Ch. 6–7 or the original PDF.
> - **Slides 17–18** — the Blackjack MC control results (optimal policy and value surfaces).
> - **Slides 24–25 (Windy Gridworld)** — the grid layout with wind strengths and the Sarsa learning curve are images; only the reward structure extracted.
> - **Slide 30 — the Sarsa(λ) Gridworld comparison** showing one-step vs λ credit propagation is an image. **This is the clearest visual argument for eligibility traces and it is lost.**
> - **Slide 40 — Cliff Walking** is entirely an image: the grid, the two learned paths, and the reward-per-episode curves. The example is famous enough to reconstruct (Sutton & Barto Example 6.6), which I have done in Exercise 4, but **the lecture's own figures are not captured.**
> - **Slides 6–9, 13–14, 21** — the GPI cycle diagrams; the captions extracted and are reproduced above.
> - **Slides 20, 37, 41** — the backup diagrams.
> - **Slide 39 — "Q-Learning Demo"** is title-only.
> - **Truncations:** slide 4 (cut at *"Model-free control can so…"*), slide 28 (**the Sarsa(λ) update cut at $E_t($**), slide 33 (**cut at *"Cannot use if $\mu$ is zero when"*** — the completion is "$\pi$ is non-zero").
>
> Windy Gridworld and Cliff Walking are both from Sutton & Barto Ch. 6 (Examples 6.5 and 6.6).

---
**Previous:** [[04 - Model-Free Prediction]] · **Next:** [[06 - Value Function Approximation]]
