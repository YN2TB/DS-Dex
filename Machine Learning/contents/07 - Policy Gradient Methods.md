---
subject: Machine Learning
chapter: 07
tags: [ds, reinforcement-learning, policy-gradient, reinforce, actor-critic, advantage-function]
source: "lecture-7-policy-gradient-methods.pdf — David Silver, UCL (Lecture 7 of 10)"
---

# Policy Gradient Methods

> [!note] Where this sits in the course
> **The other branch of the taxonomy.** [[06 - Value Function Approximation]] parameterised the *value* function and derived the policy from it; this lecture **parameterises the policy directly**. It is the answer to two problems [[06 - Value Function Approximation]] left open — the discontinuous $\arg\max$ that causes chattering, and continuous action spaces where $\max_a$ is impossible.

## 📘 Main Knowledge

> In the last lecture we approximated the value function using parameters $\theta$, and a policy was generated **from** it (e.g. $\epsilon$-greedy). **In this lecture we will directly parametrise the policy:**
> $$\pi_\theta(s,a) = \mathbb{P}[a\mid s,\theta]$$
> We focus again on **model-free** reinforcement learning.

**The three families** (from [[01 - Introduction to Reinforcement Learning]]'s taxonomy):

| | Value Function | Policy |
|---|---|---|
| **Value Based** | Learnt | **Implicit** (e.g. $\epsilon$-greedy) |
| **Policy Based** | **None** | Learnt |
| **Actor-Critic** | Learnt | Learnt |

### Advantages and disadvantages

> **Advantages:**
> - **Better convergence properties**
> - **Effective in high-dimensional or continuous action spaces**
> - **Can learn stochastic policies**
>
> **Disadvantages:**
> - **Typically converge to a local rather than global optimum**
> - **Evaluating a policy is typically inefficient and high variance**

**Why convergence is better:** the policy changes *smoothly* with $\theta$, so a small parameter update makes a small behavioural change. Value-based methods pass through an $\arg\max$, so an arbitrarily small change to $\hat q$ can flip the policy discontinuously — the "chattering" of [[06 - Value Function Approximation]].

**Why continuous actions work:** $\max_a Q(s,a)$ requires searching over actions, which is infeasible for a continuum. A Gaussian policy simply outputs a mean.

### Why stochastic policies matter

**Rock-Paper-Scissors.** In iterated play, **a deterministic policy is easily exploited**; **a uniform random policy is optimal (the Nash equilibrium)**. Value-based methods, which converge to a deterministic greedy policy, cannot represent the solution at all.

**Aliased Gridworld** — the more instructive example.

> **The agent cannot differentiate the grey states.** Features are of the form $\phi(s,a) = \mathbb{1}(\text{wall to N}, a = \text{move E})$, for all N, E, S, W.
>
> Compare **value-based** RL, $Q_\theta(s,a) = f(\phi(s,a),\theta)$, with **policy-based** RL, $\pi_\theta(s,a) = g(\phi(s,a),\theta)$.

> **Under aliasing, an optimal *deterministic* policy will either move W in both grey states, or move E in both.** Either way, **it can get stuck and never reach the money.** Value-based RL learns a near-deterministic policy, so **it will traverse the corridor for a long time.**
>
> **An optimal *stochastic* policy will randomly move E or W in grey states:**
> $$\pi_\theta(\text{wall to N and S, move E}) = 0.5 \qquad \pi_\theta(\text{wall to N and S, move W}) = 0.5$$
> **It will reach the goal in a few steps with high probability. Policy-based RL can learn the optimal stochastic policy.**

**This is the deterministic-optimal-policy theorem of [[02 - Markov Decision Processes]] failing in exactly the way predicted** — it holds for MDPs, and state aliasing makes this effectively a POMDP. When two genuinely different states look identical, a deterministic policy must treat them identically and can be trapped; randomising escapes.

### Policy objective functions

> **Goal:** given $\pi_\theta(s,a)$, find the best $\theta$. **But how do we measure the quality of a policy?**

| Setting | Objective |
|---|---|
| **Episodic** — start value | $J_1(\theta) = V^{\pi_\theta}(s_1) = \mathbb{E}_{\pi_\theta}[v_1]$ |
| **Continuing** — average value | $J_{avV}(\theta) = \sum_s d^{\pi_\theta}(s)V^{\pi_\theta}(s)$ |
| **Continuing** — average reward per time-step | $J_{avR}(\theta) = \sum_s d^{\pi_\theta}(s)\sum_a \pi_\theta(s,a)\mathcal{R}^a_s$ |

where $d^{\pi_\theta}(s)$ is the **stationary distribution** of the Markov chain induced by $\pi_\theta$ — the ergodicity material from [[02 - Markov Decision Processes]].

> Policy-based RL is an **optimisation problem**: find $\theta$ maximising $J(\theta)$.
> - **Without gradients:** hill climbing · simplex / amoeba / Nelder-Mead · genetic algorithms
> - **With gradients** (greater efficiency): gradient descent · conjugate gradient · quasi-Newton
>
> We focus on gradient descent, and on methods that exploit **sequential structure** *(truncated)*.

---

## Part 1 — Finite Difference Policy Gradient

$$\Delta\theta = \alpha\nabla_\theta J(\theta), \qquad \nabla_\theta J(\theta) = \left(\frac{\partial J}{\partial\theta_1}, \dots, \frac{\partial J}{\partial\theta_n}\right)^\top$$

**Estimate each partial derivative numerically** by perturbing $\theta$ by $\epsilon$ in the $k$th dimension:
$$\frac{\partial J(\theta)}{\partial\theta_k} \approx \frac{J(\theta + \epsilon u_k) - J(\theta)}{\epsilon}$$
where $u_k$ is the unit vector in dimension $k$.

> **Uses $n$ evaluations to compute the policy gradient in $n$ dimensions. Simple, no** *(truncated — "noisy, inefficient — but sometimes effective; works for arbitrary policies, even if non-differentiable")*.

**AIBO example** — training a Sony AIBO robot to walk. Parameters were sent to the robot, which **timed itself walking between two fixed landmarks**; more efficient parameters gave a faster gait and a better score, which the robot **sent back to the host computer**. Slides show gaits *before training, during training, after training*.

**Finite differences work on a real robot precisely because they need no gradient** — the "policy" includes the physical dynamics of the robot, which nobody can differentiate.

---

## Part 2 — Monte-Carlo Policy Gradient

### The score function and the likelihood ratio trick

> Assume $\pi_\theta$ is **differentiable** whenever it is non-zero, and that we know $\nabla_\theta\pi_\theta(s,a)$. **Likelihood ratios exploit the identity:**
> $$\nabla_\theta\pi_\theta(s,a) = \pi_\theta(s,a)\frac{\nabla_\theta\pi_\theta(s,a)}{\pi_\theta(s,a)} = \pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)$$
>
> **The score function is $\nabla_\theta\log\pi_\theta(s,a)$.**

**This trick is the whole foundation of policy gradients.** It converts a gradient of a probability into $\pi_\theta \times$ (something), which means the gradient can be written as an **expectation under $\pi_\theta$** — and therefore **estimated by sampling from the policy we are already running.**

**Softmax policy** (discrete actions) — weight actions by $\phi(s,a)^\top\theta$, with probability proportional to the exponentiated weight:
$$\pi_\theta(s,a) \propto e^{\phi(s,a)^\top\theta} \qquad \nabla_\theta\log\pi_\theta(s,a) = \phi(s,a) - \mathbb{E}_{\pi_\theta}[\phi(s,\cdot)]$$

**Gaussian policy** (continuous actions) — mean $\mu(s) = \phi(s)^\top\theta$, variance $\sigma^2$ fixed or parameterised, $a \sim \mathcal{N}(\mu(s),\sigma^2)$:
$$\nabla_\theta\log\pi_\theta(s,a) = \frac{(a - \mu(s))\phi(s)}{\sigma^2}$$

Both score functions read as **"feature minus expected feature"** — the update pushes probability toward actions whose features exceed the average, scaled by how good the outcome was.

### One-step MDPs

For a one-step MDP starting in $s \sim d(s)$ and terminating with reward $r = \mathcal{R}_{s,a}$:
$$J(\theta) = \mathbb{E}_{\pi_\theta}[r] = \sum_{s\in\mathcal{S}}d(s)\sum_{a\in\mathcal{A}}\pi_\theta(s,a)\mathcal{R}_{s,a}$$
$$\nabla_\theta J(\theta) = \sum_s d(s)\sum_a \pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)\mathcal{R}_{s,a} = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,r\big]$$

**Note what happened: $\nabla_\theta$ of an expectation became an expectation of a gradient**, which is exactly what makes sampling possible.

### The Policy Gradient Theorem

> The policy gradient theorem **generalises the likelihood ratio approach to multi-step MDPs**, replacing the instantaneous reward $r$ with the **long-term value $Q^\pi(s,a)$**. It applies to the start-state, average-reward, and average-value objectives.
>
> **Theorem.** For any differentiable policy $\pi_\theta(s,a)$, for any of the policy objective functions:
> $$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,Q^{\pi_\theta}(s,a)\big]$$
> *(statement truncated in source; this is the standard form)*

**The theorem's importance is what it does *not* contain: $\nabla_\theta d^{\pi_\theta}(s)$.** Changing the policy changes which states you visit, and one would expect the gradient to include a term for that — which would be intractable, since it requires the model. **The theorem proves that term vanishes.** You can estimate the gradient purely from sampled trajectories.

### REINFORCE

Use the return $v_t$ as an **unbiased sample** of $Q^{\pi_\theta}(s_t,a_t)$:
$$\Delta\theta_t = \alpha\nabla_\theta\log\pi_\theta(s_t,a_t)\,v_t$$

```
function REINFORCE
    Initialise θ arbitrarily
    for each episode {s₁,a₁,r₂,…,s_{T-1},a_{T-1},r_T} ~ π_θ do
        for t = 1 to T-1 do
            θ ← θ + α ∇_θ log π_θ(s_t,a_t) v_t
        end for
    end for
    return θ
end function
```

**Puck World** is the running example, with the cited figure noting **runs that converged to substantially suboptimal local minima** — the "local rather than global optimum" disadvantage made concrete.

---

## Part 3 — Actor-Critic

> **Monte-Carlo policy gradient still has high variance.** We use a **critic** to estimate the action-value function, $Q_w(s,a) \approx Q^{\pi_\theta}(s,a)$.
>
> **Actor-critic algorithms maintain two sets of parameters:**
> - **Critic** — updates action-value function parameters $w$
> - **Actor** — updates policy parameters $\theta$, **in the direction suggested by the critic**
>
> Actor-critic algorithms follow an **approximate** policy gradient *(truncated)*:
> $$\nabla_\theta J(\theta) \approx \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,Q_w(s,a)\big]$$

> **The critic is solving a familiar problem: policy evaluation.** *How good is $\pi_\theta$ for the current $\theta$?* This was explored in the previous two lectures — Monte-Carlo evaluation, TD learning, TD(λ), least-squares evaluation.

**Everything from [[04 - Model-Free Prediction]] and [[06 - Value Function Approximation]] is reusable as the critic.**

### Action-value actor-critic (QAC)

With linear approximation $Q_w(s,a) = \phi(s,a)^\top w$: the **critic** updates $w$ by linear TD(0), the **actor** updates $\theta$ by policy gradient.

```
function QAC
    Initialise s, θ; sample a ~ π_θ
    for each step do
        Sample reward r = R^a_s; sample transition s' ~ P^a_{s,·}
        Sample action a' ~ π_θ(s',a')
        δ = r + γ Q_w(s',a') − Q_w(s,a)
        θ = θ + α ∇_θ log π_θ(s,a) Q_w(s,a)
        w ← w + β δ φ(s,a)
        a ← a', s ← s'
    end for
end function
```

### Compatible function approximation

> **Approximating the policy gradient introduces bias**, and a biased gradient may not find the right solution — *"e.g. if $Q_w(s,a)$ uses aliased features, can we solve the gridworld example?"* **But if we choose the value function approximation carefully, we can avoid introducing any bias.**

> **Theorem (Compatible Function Approximation).** If:
> 1. **The value function approximator is compatible to the policy:** $\nabla_w Q_w(s,a) = \nabla_\theta\log\pi_\theta(s,a)$
> 2. **The value function parameters minimise the mean-squared error:** $\varepsilon = \mathbb{E}_{\pi_\theta}[(Q^{\pi_\theta}(s,a) - Q_w(s,a))^2]$
>
> **Then the policy gradient is exact:** $\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)Q_w(s,a)]$

**Proof.** At the minimum of $\varepsilon$, the gradient w.r.t. $w$ is zero:
$$\mathbb{E}_{\pi_\theta}\big[(Q^\theta - Q_w)\nabla_w Q_w\big] = 0 \;\overset{\text{(cond. 1)}}{\Longrightarrow}\; \mathbb{E}_{\pi_\theta}\big[(Q^\theta - Q_w)\nabla_\theta\log\pi_\theta\big] = 0$$
$$\Longrightarrow\; \mathbb{E}_{\pi_\theta}[Q^\theta\nabla_\theta\log\pi_\theta] = \mathbb{E}_{\pi_\theta}[Q_w\nabla_\theta\log\pi_\theta]$$
**So $Q_w$ can be substituted directly into the policy gradient** without introducing bias. ∎

### Baselines and the advantage function

> **Subtract a baseline $B(s)$ from the policy gradient. This can reduce variance without changing the expectation:**
> $$\mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)B(s)] = \sum_s d^{\pi_\theta}(s)\sum_a \nabla_\theta\pi_\theta(s,a)B(s) = \sum_s d^{\pi_\theta}B(s)\nabla_\theta\underbrace{\sum_a \pi_\theta(s,a)}_{=1} = 0$$
>
> **A good baseline is $B(s) = V^{\pi_\theta}(s)$**, giving the **advantage function**:
> $$A^{\pi_\theta}(s,a) = Q^{\pi_\theta}(s,a) - V^{\pi_\theta}(s) \qquad \nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)A^{\pi_\theta}(s,a)\big]$$

**The baseline is free because $\sum_a\pi_\theta(s,a) = 1$ always**, so its gradient is zero. Any function of $s$ alone can be subtracted without bias — and $V^\pi$ is the choice that minimises variance.

**Estimating the advantage — two ways:**

**(1) Two approximators:** $V_v(s) \approx V^{\pi_\theta}(s)$ and $Q_w(s,a) \approx Q^{\pi_\theta}(s,a)$, giving $A(s,a) = Q_w(s,a) - V_v(s)$.

**(2) The TD error — much simpler.** For the true $V^{\pi_\theta}$, the TD error
$$\delta^{\pi_\theta} = r + \gamma V^{\pi_\theta}(s') - V^{\pi_\theta}(s)$$
is an **unbiased estimate of the advantage function**:
$$\mathbb{E}_{\pi_\theta}[\delta^{\pi_\theta}\mid s,a] = \mathbb{E}[r + \gamma V^{\pi_\theta}(s')\mid s,a] - V^{\pi_\theta}(s) = Q^{\pi_\theta}(s,a) - V^{\pi_\theta}(s) = A^{\pi_\theta}(s,a)$$
$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,\delta^{\pi_\theta}\big]$$

**In practice we use the approximate TD error** $\delta = r + \gamma V_v(s') - V_v(s)$, requiring **only one parameter vector $v$** rather than two.

### Critics and actors at different time-scales

**Critics** can use any target from [[06 - Value Function Approximation]]: MC ($v_t$), TD(0) ($r+\gamma V(s')$), forward-view TD(λ) ($v^\lambda_t$), backward-view TD(λ) with traces.

**Actors** likewise:
$$\text{MC: } \Delta\theta = \alpha(v_t - V_v(s_t))\nabla_\theta\log\pi_\theta(s_t,a_t) \qquad \text{Actor-critic: } \Delta\theta = \alpha(r + \gamma V_v(s_{t+1}) - V_v(s_t))\nabla_\theta\log\pi_\theta(s_t,a_t)$$

**With eligibility traces** — by equivalence with TD(λ), substituting $\phi(s) = \nabla_\theta\log\pi_\theta(s,a)$:
$$\delta = r_{t+1} + \gamma V_v(s_{t+1}) - V_v(s_t) \qquad e_{t+1} = \lambda e_t + \nabla_\theta\log\pi_\theta(s,a) \qquad \Delta\theta = \alpha\delta e$$

### Natural policy gradient

> Gradient ascent can follow **any** ascent direction, and a good one can significantly speed convergence. Also, **a policy can often be reparametrised without changing action probabilities** — e.g. increasing the score of all actions in a softmax policy. **The vanilla gradient is sensitive to these reparametrisations.**

> **The natural policy gradient is parametrisation independent.** It finds the ascent direction closest to the vanilla gradient **when changing the policy by a small, fixed amount**:
> $$\nabla^{nat}_\theta\pi_\theta(s,a) = G_\theta^{-1}\nabla_\theta\pi_\theta(s,a)$$
> where $G_\theta$ is the **Fisher information matrix**:
> $$G_\theta = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)^\top\big]$$

The Fisher information matrix is the same object as in [[Mathematical Statistics/contents/05 - Point Estimation|Point Estimation]] — it measures how sharply the distribution responds to parameter changes, and here it converts "distance in parameter space" into "distance in policy space".

**Natural Actor-Critic** — using compatible function approximation $\nabla_w A_w(s,a) = \nabla_\theta\log\pi_\theta(s,a)$:
$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta\,\nabla_\theta\log\pi_\theta^\top w\big] = G_\theta w \quad\Longrightarrow\quad \boxed{\nabla^{nat}_\theta J(\theta) = w}$$

> **i.e. update actor parameters in the direction of critic parameters.**

A remarkably clean result: the natural gradient *is* the critic's parameter vector, so the expensive Fisher matrix inversion cancels entirely.

**Snake domain** — natural actor-critic on a snake-like robot with a central pattern generator. Off-policy NAC achieved **10/10 successful learning runs with average episode length 20.6**, versus on-policy NAC's **7/10 and 145.7**.

### Summary of policy gradient algorithms

> **The policy gradient has many equivalent forms:**
>
> $$\begin{aligned}\nabla_\theta J(\theta) &= \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,v_t] &&\textbf{REINFORCE} \\ &= \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,Q_w(s,a)] &&\textbf{Q Actor-Critic} \\ &= \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,A_w(s,a)] &&\textbf{Advantage Actor-Critic} \\ &= \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,\delta] &&\textbf{TD Actor-Critic} \\ &= \mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,\delta e] &&\textbf{TD(λ) Actor-Critic} \\ G_\theta^{-1}\nabla_\theta J(\theta) &= w &&\textbf{Natural Actor-Critic}\end{aligned}$$
>
> **Each leads to a stochastic** *(truncated — "gradient ascent algorithm")*.

**Everything differs only in how $Q^{\pi_\theta}(s,a)$ is estimated** — by the return, a learned $Q$, an advantage, a TD error, or an eligibility-trace-weighted TD error. The score function $\nabla_\theta\log\pi_\theta$ is common to all.

## ✏️ Exercises

**1.** *(Aliased Gridworld)* Explain why value-based RL fails and policy-based RL succeeds, and connect this to the deterministic-optimal-policy theorem.

> [!example]- Solution
> **The setup:** two grey states look identical to the agent, because the features $\phi(s,a) = \mathbb{1}(\text{wall to N}, a = \text{move E})$ cannot distinguish them — both have walls to the north and south.
>
> **Why value-based RL fails.** It learns $Q_\theta(s,a) = f(\phi(s,a),\theta)$ and acts greedily. Since both grey states produce **the same feature vector**, they get the **same $Q$ values**, so the greedy policy takes the **same action** in both. But the two states need *opposite* actions — one requires moving east, the other west. A deterministic policy moving W in both gets stuck on the left; moving E in both gets stuck on the right. **The agent oscillates in the corridor for a long time.**
>
> $\epsilon$-greedy escapes eventually, by taking a random action with probability $\epsilon$ — but that is an accident of exploration, not a learned solution, and it is slow.
>
> **Why policy-based RL succeeds.** $\pi_\theta$ outputs a **probability distribution**, so it can learn $\mathbb{P}(\text{E}) = \mathbb{P}(\text{W}) = 0.5$ in the aliased states. From either grey state, the agent has a 50% chance of moving the right way each step, reaching the goal in a few steps with high probability. **The stochasticity is optimal, and it is learned deliberately rather than injected as exploration noise.**
>
> **The connection to [[02 - Markov Decision Processes]].** That lecture proved *"there is always a deterministic optimal policy for any MDP"* — and the proof is correct. But it assumes the agent observes the **state**. Here the agent observes **features that alias two distinct states**, so from its perspective this is a **POMDP**, not an MDP. The theorem's precondition fails.
>
> This is exactly the first exception noted in that chapter's Exercise 5: *"in a POMDP the agent's observation does not determine the state, so two genuinely different states can look identical... randomising escapes."* The Aliased Gridworld is that abstract point made concrete.
>
> **The practical lesson:** partial observability is the normal case in real problems (a robot's sensors, a trading agent's price feed). Whenever your features cannot fully identify the state — which is almost always — **stochastic policies can strictly dominate deterministic ones**, and only policy-based methods can represent them.

**2.** Explain the likelihood ratio trick and why it is the foundation of policy gradient methods.

> [!example]- Solution
> **The identity:**
> $$\nabla_\theta\pi_\theta(s,a) = \pi_\theta(s,a)\frac{\nabla_\theta\pi_\theta(s,a)}{\pi_\theta(s,a)} = \pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)$$
> using $\nabla\log f = \nabla f / f$.
>
> **Why it is foundational — it converts a gradient into an expectation we can sample.**
>
> Without it, the one-step gradient is
> $$\nabla_\theta J(\theta) = \sum_s d(s)\sum_a \nabla_\theta\pi_\theta(s,a)\mathcal{R}_{s,a}$$
> **This cannot be estimated by sampling**, because it is a sum weighted by $\nabla_\theta\pi_\theta$ — which is not a probability distribution. To evaluate it you would need to enumerate all states and actions, and know $d(s)$ and $\mathcal{R}_{s,a}$ — i.e. the model.
>
> Applying the identity:
> $$\nabla_\theta J(\theta) = \sum_s d(s)\sum_a \pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)\mathcal{R}_{s,a} = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,r\big]$$
> **Now $\pi_\theta(s,a)$ appears as a weight, so the sum *is* an expectation under the policy we are running.** Every sampled $(s,a,r)$ gives an unbiased estimate — just compute $\nabla_\theta\log\pi_\theta(s,a) \times r$ and average.
>
> **Three consequences:**
> - **Model-free.** No $\mathcal{P}$ or $\mathcal{R}$ needed; run the policy and observe.
> - **On-policy sampling suffices.** The expectation is under $\pi_\theta$ itself, so no importance sampling is required.
> - **The score function is computable in closed form** for standard policy classes — $\phi(s,a) - \mathbb{E}[\phi]$ for softmax, $(a-\mu(s))\phi(s)/\sigma^2$ for Gaussian.
>
> **The intuition of the update** $\Delta\theta \propto \nabla_\theta\log\pi_\theta(s,a) \cdot r$: the score function points in the direction that **increases the probability of the action just taken**; multiplying by $r$ means we move that way when the reward was good and the opposite way when it was bad. **Reinforce what worked.** Hence the name.
>
> The same trick appears throughout statistics and machine learning — it is the score function of [[Mathematical Statistics/contents/05 - Point Estimation|maximum likelihood estimation]], reused for a different purpose.

**3.** Explain why subtracting a baseline reduces variance without introducing bias, and why the advantage function is the natural choice.

> [!example]- Solution
> **Why no bias — the proof turns on $\sum_a\pi_\theta(s,a) = 1$:**
> $$\mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)B(s)] = \sum_s d^{\pi_\theta}(s)\sum_a \nabla_\theta\pi_\theta(s,a)B(s) = \sum_s d^{\pi_\theta}(s)B(s)\nabla_\theta\underbrace{\sum_a\pi_\theta(s,a)}_{=1} = \nabla_\theta 1 = 0$$
> Since $B(s)$ does not depend on $a$, it factors out of the inner sum, leaving the gradient of a constant. **Any function of $s$ alone can be subtracted for free.**
>
> **Why it reduces variance.** The REINFORCE update is $\nabla_\theta\log\pi_\theta \cdot v_t$, and $v_t$ can be large in absolute terms while carrying little information. If every action in a state yields a return around +100, the raw update pushes *all* actions' probabilities up strongly — the useful signal (which action was *relatively* better) is swamped by a large common offset.
>
> Subtracting $V^\pi(s) \approx 100$ leaves only the deviations — perhaps $+2$ and $-3$ — so the update magnitude reflects the **actual differences between actions** rather than the state's overall value. The estimator's mean is unchanged; its variance collapses.
>
> This is the same idea as centring a variable before regression, and it matters more here because the lecture lists *"evaluating a policy is inefficient and high variance"* as policy gradient's main weakness.
>
> **Why $V^\pi(s)$ specifically.** It gives the **advantage function** $A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$, which answers exactly the right question: *"how much better than average is this action, in this state?"* Since $V^\pi(s) = \sum_a\pi(a|s)Q^\pi(s,a)$ is the policy's own average, the advantage is **positive for above-average actions and negative for below-average ones**, and its expectation under $\pi$ is zero. That is the variance-minimising baseline in practice.
>
> **The elegant implementation:** you do not need to estimate $Q$ and $V$ separately. The **TD error is an unbiased estimate of the advantage**:
> $$\mathbb{E}[\delta^\pi\mid s,a] = \mathbb{E}[r + \gamma V^\pi(s')\mid s,a] - V^\pi(s) = Q^\pi(s,a) - V^\pi(s) = A^\pi(s,a)$$
> So one value function $V_v(s)$ suffices, and the critic's TD error — already computed for its own update — doubles as the actor's advantage estimate. **This is why TD Actor-Critic is the standard practical algorithm** and the basis of A2C/A3C.

**4.** Explain the Compatible Function Approximation Theorem and what problem it solves.

> [!example]- Solution
> **The problem.** REINFORCE uses the true return $v_t$, an unbiased sample of $Q^\pi$, so its gradient is unbiased — but high variance. Actor-critic replaces $v_t$ with a *learned* $Q_w(s,a)$, cutting variance but **introducing bias**, since $Q_w \ne Q^{\pi_\theta}$.
>
> The lecture poses the danger sharply: *"a biased policy gradient may not find the right solution — e.g. if $Q_w(s,a)$ uses aliased features, can we solve the gridworld example?"* If the critic's features cannot distinguish the grey states, its $Q$ estimates are wrong there, and the actor is pushed in a wrong direction. **The variance reduction could cost you the solution.**
>
> **The theorem's answer.** If:
> 1. $\nabla_w Q_w(s,a) = \nabla_\theta\log\pi_\theta(s,a)$ — the critic is **compatible** with the policy
> 2. $w$ minimises $\mathbb{E}_{\pi_\theta}[(Q^{\pi_\theta} - Q_w)^2]$
>
> then **the policy gradient is exact** — zero bias, despite using an approximation.
>
> **The proof is short and worth following.** At the MSE minimum, $\nabla_w\varepsilon = 0$:
> $$\mathbb{E}[(Q^\theta - Q_w)\nabla_w Q_w] = 0$$
> Condition 1 substitutes $\nabla_\theta\log\pi_\theta$ for $\nabla_w Q_w$:
> $$\mathbb{E}[(Q^\theta - Q_w)\nabla_\theta\log\pi_\theta] = 0 \;\Longrightarrow\; \mathbb{E}[Q^\theta\nabla_\theta\log\pi_\theta] = \mathbb{E}[Q_w\nabla_\theta\log\pi_\theta]$$
> The left side is the true policy gradient; the right is what actor-critic computes. **They are equal.** ∎
>
> **What condition 1 means concretely.** $\nabla_w Q_w = \nabla_\theta\log\pi_\theta$ integrates to $Q_w(s,a) = \nabla_\theta\log\pi_\theta(s,a)^\top w$ — the critic must be **linear in the score function**. So the critic's features are dictated by the policy's parameterisation: for a softmax policy, the critic uses $\phi(s,a) - \mathbb{E}[\phi(s,\cdot)]$ as its features.
>
> **Why the error does not matter.** $Q_w$ may be a poor approximation of $Q^\pi$ overall, but the compatibility condition guarantees its error is **orthogonal to the score function** — precisely the direction the policy gradient projects onto. The approximation is wrong only in directions the actor never looks.
>
> **The payoff appears in the natural gradient:** with compatible approximation, $\nabla_\theta J(\theta) = G_\theta w$, so $\nabla^{nat}_\theta J(\theta) = w$ — **the natural gradient is just the critic's weights**, and the Fisher matrix inversion vanishes.

**5.** (Advanced) Compare value-based, policy-based, and actor-critic methods. When is each appropriate?

> [!example]- Solution
> | | **Value-based** | **Policy-based** | **Actor-Critic** |
> |---|---|---|---|
> | Learns | $Q$ | $\pi$ | Both |
> | Policy | Implicit via $\arg\max$ | Explicit, parameterised | Explicit |
> | Continuous actions | ✗ (needs $\max_a$) | ✓ | ✓ |
> | Stochastic optimal policies | ✗ | ✓ | ✓ |
> | Variance | Low | **High** | Medium |
> | Bias | Can diverge (triad) | Unbiased (REINFORCE) | Biased unless compatible |
> | Sample efficiency | Good (off-policy replay) | **Poor** (on-policy) | Medium |
> | Convergence | Chatters / diverges | Local optimum, smooth | Local optimum |
>
> **Value-based when:** actions are discrete and few, you want sample efficiency from experience replay, and off-policy reuse matters. **DQN on Atari** is the archetype — 18 discrete actions, replay buffers, and a deterministic optimal policy is fine.
>
> **Policy-based when:** actions are **continuous** (robot torques, steering angles), the optimal policy is **stochastic** (partial observability, adversarial games), or you need smooth, monotone policy improvement. **REINFORCE is rarely used alone** in practice — its variance is prohibitive — but the family (TRPO, PPO) dominates continuous control.
>
> **Actor-critic when:** essentially always, in practice. It is the **combination that fixes each method's weakness**:
> - The critic's bootstrapping **cuts the actor's variance** — policy gradient's main flaw
> - The actor's smooth parameterisation **avoids the $\arg\max$ discontinuity** — value-based methods' main flaw in [[06 - Value Function Approximation]]
> - Compatible approximation removes the bias the critic would otherwise introduce
>
> **The bias/variance framing unifies the whole progression** of the summary table: REINFORCE ($v_t$) is unbiased with maximum variance; Q Actor-Critic ($Q_w$) trades bias for lower variance; Advantage/TD Actor-Critic ($A_w$ or $\delta$) reduces variance further with a baseline; TD(λ) Actor-Critic ($\delta e$) tunes the trade-off continuously via $\lambda$. **Each row is one step along the same axis** — exactly the MC-vs-TD spectrum of [[04 - Model-Free Prediction]], applied to the actor.
>
> **The remaining weakness is sample efficiency.** Policy gradients are fundamentally **on-policy** — the likelihood ratio expectation is under $\pi_\theta$, so data from an old policy is invalid without importance sampling (with the variance problems of [[05 - Model-Free Control]]). This is why value-based DQN can reuse a million-transition replay buffer while A3C must keep collecting fresh data, and it is the gap modern methods (PPO's clipped surrogate, off-policy actor-critics like DDPG and SAC) work to close.

## 📝 Summary

- **Policy gradient methods parameterise $\pi_\theta(s,a)$ directly** rather than deriving a policy from a value function.
- **Advantages:** better convergence (smooth, no $\arg\max$), works in **continuous action spaces**, can learn **stochastic policies**. **Disadvantages:** local optima, high variance.
- **Stochastic policies are sometimes strictly optimal** — Rock-Paper-Scissors (Nash equilibrium) and **Aliased Gridworld** (where the deterministic-optimal theorem fails because aliasing makes it a POMDP).
- **Objectives:** start value $J_1$, average value $J_{avV}$, average reward $J_{avR}$.
- **Finite differences** need $n$ evaluations and no gradient — usable on physical robots (AIBO).
- **Likelihood ratio trick:** $\nabla_\theta\pi_\theta = \pi_\theta\nabla_\theta\log\pi_\theta$, converting a gradient into a **sampleable expectation**. $\nabla_\theta\log\pi_\theta$ is the **score function**.
- **Score functions:** softmax $\phi(s,a) - \mathbb{E}[\phi]$; Gaussian $(a-\mu(s))\phi(s)/\sigma^2$.
- **Policy Gradient Theorem:** $\nabla_\theta J = \mathbb{E}[\nabla_\theta\log\pi_\theta \cdot Q^{\pi_\theta}]$ — crucially, **no term for how the state distribution changes**.
- **REINFORCE** uses the return $v_t$ as an unbiased sample of $Q^{\pi_\theta}$.
- **Actor-critic** adds a critic to cut variance; the critic is just policy evaluation from Lectures 4 and 6.
- **Compatible Function Approximation Theorem:** if $\nabla_w Q_w = \nabla_\theta\log\pi_\theta$ and $w$ minimises MSE, **the gradient is exact — no bias.**
- **A baseline $B(s)$ is free** because $\sum_a\pi_\theta = 1$; the best choice is $V^\pi$, giving the **advantage function**.
- **The TD error is an unbiased estimate of the advantage**, so one value function suffices.
- **Natural policy gradient** $G_\theta^{-1}\nabla_\theta J$ is parametrisation-independent; with compatible approximation **it equals the critic's weights $w$.**

## ⚠️ Important Notes

**Value-based methods cannot represent a stochastic optimal policy.** Greedy action selection is deterministic by construction, so Rock-Paper-Scissors and Aliased Gridworld are unsolvable in principle, not merely in practice.

**The deterministic-optimal-policy theorem requires a genuine MDP.** Feature aliasing makes the problem a POMDP and the theorem does not apply — which is the normal situation with function approximation.

**$\epsilon$-greedy randomness is not the same as a learned stochastic policy.** It is uniform noise applied everywhere; an optimal stochastic policy randomises *where it should* and acts decisively elsewhere.

**The likelihood ratio trick is what makes the gradient estimable.** Without it the gradient is a sum weighted by $\nabla_\theta\pi_\theta$, which is not a distribution and cannot be sampled.

**The Policy Gradient Theorem's significance is the term it lacks.** There is no $\nabla_\theta d^{\pi_\theta}(s)$ — the effect of the policy on the state distribution vanishes, which is why the gradient is model-free.

**REINFORCE is unbiased but has very high variance** and converges slowly to local optima. The Puck World figure explicitly shows runs trapped in *"substantially suboptimal local minima"*.

**A baseline is free only if it does not depend on the action.** $B(s)$ is fine; $B(s,a)$ introduces bias.

**Actor-critic introduces bias unless the approximation is compatible.** A critic with aliased features can push the actor in the wrong direction — the lecture raises this as a live danger.

**Compatibility forces the critic's features to be the score function.** You cannot choose the critic's representation freely and still claim exactness.

**Policy gradients are inherently on-policy.** The expectation is under $\pi_\theta$, so old data is invalid without importance sampling — which is why they are far less sample-efficient than DQN with replay.

**The vanilla gradient is sensitive to reparameterisation.** Rescaling parameters that leave the policy unchanged changes the gradient direction; the natural gradient fixes this.

**Higher variance in the actor means smaller usable step sizes**, which is the practical reason plain REINFORCE is rarely used and modern methods (TRPO, PPO) constrain the step in policy space rather than parameter space.

> [!warning] Gaps in the source slides
> Silver's slides extract well; **all derivations and proofs survived**. Losses:
> - **⚠️ Slide 20 — the Policy Gradient Theorem statement itself is truncated** at *"for any of the policy objective functions $J =$"*. **The theorem's equation did not extract.** The form given above is the standard one (Sutton et al., 1999) and matches the surrounding text, but **verify against the original.**
> - **Slides 7–9 (Aliased Gridworld)** — the grid figures showing the aliased states and the red-arrow deterministic policy are images; the text is complete enough to follow the argument.
> - **Slides 14–15 (AIBO)** — the text is OCR of a *cited paper's* prose, not Silver's own slide; the gait figures (before/during/after training) are images.
> - **Slide 22 (Puck World)** — the figure and caption are from the cited policy-gradient-estimation paper; the learning curves are images.
> - **Slides 38–40 (Snake domain)** — likewise OCR of the source paper (Fig. 3, Fig. 4, Table 1); the off-NAC vs on-NAC comparison table extracted.
> - **Slides 4, 12** — the taxonomy diagram and the gradient ascent figure (with garbled caption).
> - **Truncations:** slide 10 (cut at *"$d^{\pi_\theta}(s)$ is stati"* — "stationary distribution"), slide 11 (cut at *"methods that exploit sequ"*), slide 13 (cut at *"Simple, no"*), slide 21 (REINFORCE pseudocode cut at "e"), slide 23 (cut at *"approximate policy gra"*), slide 25 (**QAC pseudocode cut mid-line at $\nabla_\theta\log\pi_\theta(s$** — the critic update and loop closing are reconstructed above), slide 26 (cut at *"exact policy grad"*), slide 27 (**theorem conclusion cut at $\nabla_\theta J(\theta)$**), slide 28 (proof cut at *"substituted directly into the policy"*), slide 29 (cut at *"using the advantage f"*), slide 30 (cut at *"And updating b"*), slide 31 (cut at *"In practice we can use"*), slide 32 (cut at *"For backward-view TD"*), slide 34 (trace update cut), slide 41 (**summary cut at *"Each leads a stochas"***).
>
> **References:** the Policy Gradient Theorem is Sutton, McAllester, Singh & Mansour (NIPS 1999). Natural policy gradient is Kakade (2002); Natural Actor-Critic is Peters & Schaal. The AIBO work is Kohl & Stone (2004).

---
**Previous:** [[06 - Value Function Approximation]] · **Next:** [[08 - Integrating Learning and Planning]]
