---
subject: Machine Learning
chapter: 06
tags: [ds, reinforcement-learning, function-approximation, dqn, deadly-triad, lstd]
source: "lecture-6-value-function-approximation-.pdf — David Silver, UCL (Lecture 6 of 10)"
---

# Value Function Approximation

> [!note] Where this sits in the course
> **Opens Part II — RL in Practice.** Part I ([[01 - Introduction to Reinforcement Learning]]–[[05 - Model-Free Control]]) assumed a **lookup table** with one entry per state. This lecture removes that assumption, which is what makes RL applicable to real problems — and introduces the instability that comes with it.

## 📘 Main Knowledge

### The scaling problem

> RL can be used to solve **large** problems:
> - **Backgammon: $10^{20}$ states**
> - **Computer Go: $10^{170}$ states**
> - **Helicopter: continuous state space**
>
> **How can we scale up the model-free methods for prediction and control from the last two lectures?**

> **So far we have represented the value function by a lookup table** — every state $s$ has an entry $V(s)$, or every pair $(s,a)$ has an entry $Q(s,a)$.
>
> **Problem with large MDPs:**
> - **There are too many states and/or actions to store in memory**
> - **It is too slow to learn the value of each state individually**
>
> **Solution:** estimate the value function with **function approximation** *(truncated)*:
> $$\hat{v}(s,\mathbf{w}) \approx v_\pi(s) \qquad\text{or}\qquad \hat{q}(s,a,\mathbf{w}) \approx q_\pi(s,a)$$

**The second bullet is the deeper one.** Even if you could store $10^{170}$ numbers, you would need to *visit* each state to learn its value. Function approximation **generalises** — updating $\mathbf{w}$ from one state changes the estimate for all similar states, so experience transfers to states never seen.

**Three architectures** (slide 7):
- $\hat{v}(s,\mathbf{w})$ — state in, one value out
- $\hat{q}(s,a,\mathbf{w})$ — state and action in, one value out
- $\hat{q}(s,a_1,\mathbf{w}), \dots, \hat{q}(s,a_m,\mathbf{w})$ — state in, **all** action values out

The third is what DQN uses: one forward pass gives every action's value, so the $\arg\max$ costs nothing extra.

**Which function approximator?** Linear combinations of features · neural network · decision tree · nearest neighbour · Fourier/wavelet bases · …

> **We consider *differentiable* function approximators** — linear and neural network. Furthermore, **we require a training method suitable for non-stationary, non-i.i.d. data.**

That last requirement is the RL-specific constraint from [[01 - Introduction to Reinforcement Learning]], and it rules out most off-the-shelf supervised learning.

---

## Part 1 — Incremental Methods

### Gradient descent

Let $J(\mathbf{w})$ be differentiable. The gradient is $\nabla_\mathbf{w}J(\mathbf{w}) = \left(\frac{\partial J}{\partial w_1}, \dots, \frac{\partial J}{\partial w_n}\right)^\top$, and to find a local minimum we adjust in the direction of the negative gradient:
$$\Delta\mathbf{w} = -\tfrac12\alpha\nabla_\mathbf{w}J(\mathbf{w})$$

**Goal:** find $\mathbf{w}$ minimising the mean-squared error between $\hat{v}(s,\mathbf{w})$ and the true $v_\pi(s)$:
$$J(\mathbf{w}) = \mathbb{E}_\pi\big[(v_\pi(S) - \hat{v}(S,\mathbf{w}))^2\big]$$
$$\Delta\mathbf{w} = \alpha\,\mathbb{E}_\pi\big[(v_\pi(S) - \hat{v}(S,\mathbf{w}))\nabla_\mathbf{w}\hat{v}(S,\mathbf{w})\big]$$

**Stochastic gradient descent samples the gradient:**
$$\Delta\mathbf{w} = \alpha\big(v_\pi(S) - \hat{v}(S,\mathbf{w})\big)\nabla_\mathbf{w}\hat{v}(S,\mathbf{w})$$

### Linear function approximation

Represent the state by a **feature vector** $\mathbf{x}(S) = (x_1(S), \dots, x_n(S))^\top$ — e.g. distance of a robot from landmarks · trends in the stock market · piece and pawn configurations in chess.

$$\hat{v}(S,\mathbf{w}) = \mathbf{x}(S)^\top\mathbf{w} = \sum_{j=1}^{n}x_j(S)w_j$$

> The objective is **quadratic in $\mathbf{w}$**, so **stochastic gradient descent converges on the global optimum**, and the update is particularly simple:
> $$\nabla_\mathbf{w}\hat{v}(S,\mathbf{w}) = \mathbf{x}(S) \qquad \Delta\mathbf{w} = \alpha\big(v_\pi(S) - \hat{v}(S,\mathbf{w})\big)\mathbf{x}(S)$$

**Update = step-size × prediction error × feature value.** Worth memorising.

**Table lookup is a special case** of linear approximation, using **one-hot features**:
$$\mathbf{x}^{table}(S) = \big(\mathbb{1}(S=s_1), \dots, \mathbb{1}(S=s_n)\big)^\top$$
so $\hat{v}(S,\mathbf{w}) = w_i$ for state $s_i$. **Everything in Part I is the degenerate case of this lecture**, which is why the convergence results there were so clean — with one-hot features, updating one state cannot disturb any other.

### Substituting a target

> **We have assumed the true $v_\pi(s)$ is given by a supervisor. But in RL there is no supervisor, only rewards.** In practice we **substitute a target**:

| Method | Target | Update |
|---|---|---|
| **MC** | $G_t$ | $\Delta\mathbf{w} = \alpha(G_t - \hat{v}(S_t,\mathbf{w}))\nabla_\mathbf{w}\hat{v}(S_t,\mathbf{w})$ |
| **TD(0)** | $R_{t+1} + \gamma\hat{v}(S_{t+1},\mathbf{w})$ | $\Delta\mathbf{w} = \alpha(R_{t+1} + \gamma\hat{v}(S_{t+1},\mathbf{w}) - \hat{v}(S_t,\mathbf{w}))\nabla_\mathbf{w}\hat{v}(S_t,\mathbf{w})$ |
| **TD(λ)** | $G^\lambda_t$ | $\Delta\mathbf{w} = \alpha(G^\lambda_t - \hat{v}(S_t,\mathbf{w}))\nabla_\mathbf{w}\hat{v}(S_t,\mathbf{w})$ |

**MC:** the return is an **unbiased, noisy** sample of $v_\pi(S_t)$, so we can apply **supervised learning** to the training data $\langle S_1,G_1\rangle, \langle S_2,G_2\rangle, \dots$ **MC evaluation converges to a** *(truncated — local optimum, even with non-linear approximation)*.

**TD(0):** the target is a **biased** sample, but supervised learning still applies to $\langle S_1, R_2 + \gamma\hat{v}(S_2,\mathbf{w})\rangle, \dots$. For linear TD(0):
$$\Delta\mathbf{w} = \alpha\big(R + \gamma\hat{v}(S',\mathbf{w}) - \hat{v}(S,\mathbf{w})\big)\mathbf{x}(S) = \alpha\delta\,\mathbf{x}(S)$$
**Linear TD(0) converges (clos…)** *(truncated — "close to the global optimum")*.

**Backward-view linear TD(λ):** $\delta_t = R_{t+1} + \gamma\hat{v}(S_{t+1},\mathbf{w}) - \hat{v}(S_t,\mathbf{w})$, with traces $E_t = \gamma\lambda E_{t-1} + \mathbf{x}(S_t)$ and $\Delta\mathbf{w} = \alpha\delta_t E_t$. **The trace is now over *features*, not states.**

> [!warning] The targets are not real supervised learning
> The TD target contains $\hat{v}(S_{t+1},\mathbf{w})$ — which **depends on the parameters being updated**. So $\nabla_\mathbf{w}$ of the true objective would include a term for how the *target* moves, and TD ignores it. This makes TD a **semi-gradient** method, and it is the technical reason for the divergence results below.

### Control with function approximation

Same GPI skeleton as [[05 - Model-Free Control]]: **approximate policy evaluation** $\hat{q}(\cdot,\cdot,\mathbf{w}) \approx q_\pi$, then **$\epsilon$-greedy improvement**.

$$J(\mathbf{w}) = \mathbb{E}_\pi\big[(q_\pi(S,A) - \hat{q}(S,A,\mathbf{w}))^2\big]$$

With linear approximation over state-action features $\mathbf{x}(S,A)$:
$$\hat{q}(S,A,\mathbf{w}) = \mathbf{x}(S,A)^\top\mathbf{w} \qquad \Delta\mathbf{w} = \alpha\big(q_\pi(S,A) - \hat{q}(S,A,\mathbf{w})\big)\mathbf{x}(S,A)$$

with the same target substitutions — $G_t$ for MC, $R_{t+1} + \gamma\hat{q}(S_{t+1},A_{t+1},\mathbf{w})$ for TD(0) (**Sarsa**), and the action-value λ-return for TD(λ).

**Mountain Car** is the running example: linear Sarsa with **coarse coding** and with **radial basis functions**, plus a **study of λ — "should we bootstrap?"**

### Convergence — and Baird's counterexample

**Baird's counterexample** demonstrates **parameter divergence**: off-policy TD with linear function approximation can make $\mathbf{w}$ grow without bound. The values do not merely converge slowly or to the wrong answer — **they explode.**

**Convergence of prediction algorithms** *(the ✓/✗ marks did not extract — see the gaps warning; this is the standard table)*:

| | Algorithm | Table Lookup | Linear | Non-Linear |
|---|---|---|---|---|
| **On-Policy** | MC | ✓ | ✓ | ✓ |
| | TD(0) | ✓ | ✓ | ✗ |
| | TD(λ) | ✓ | ✓ | ✗ |
| **Off-Policy** | MC | ✓ | ✓ | ✓ |
| | TD(0) | ✓ | ✗ | ✗ |
| | TD(λ) | ✓ | ✗ | ✗ |

> **TD does not follow the gradient of any objective function. This is why TD can diverge when off-policy or using non-linear function approximation.**
>
> **Gradient TD follows the true gradient of the projected Bellman error** — and converges in all cases.

| | Algorithm | Table Lookup | Linear | Non-Linear |
|---|---|---|---|---|
| **On-Policy** | MC · TD · **Gradient TD** | ✓ | ✓ | ✓ / ✗ / **✓** |
| **Off-Policy** | MC · TD · **Gradient TD** | ✓ | ✓ / ✗ / **✓** | ✓ / ✗ / **✓** |

**Convergence of control algorithms:**

| Algorithm | Table Lookup | Linear | Non-Linear |
|---|---|---|---|
| Monte-Carlo Control | ✓ | **(✓)** | ✗ |
| Sarsa | ✓ | **(✓)** | ✗ |
| Q-learning | ✓ | ✗ | ✗ |
| Gradient Q-learning | ✓ | ✓ | ✗ |

> **(✓) = chatters around near-optimal value function**

**Note that control is strictly worse than prediction** — even on-policy Sarsa only "chatters" with linear approximation, because the policy keeps changing as $\mathbf{w}$ changes, so the target keeps moving.

---

## Part 2 — Batch Methods

> **Gradient descent is simple and appealing, but it is not sample efficient.** Batch methods seek to find the **best fitting value function given the agent's experience** ("training data").

Incremental methods use each transition once and discard it. When experience is expensive — a real robot, a real market — that is wasteful.

### Least squares prediction

Given experience $\mathcal{D} = \{\langle s_1, v^\pi_1\rangle, \dots, \langle s_T, v^\pi_T\rangle\}$, find $\mathbf{w}$ minimising
$$LS(\mathbf{w}) = \sum_{t=1}^{T}\big(v^\pi_t - \hat{v}(s_t,\mathbf{w})\big)^2$$

**Stochastic Gradient Descent with Experience Replay:** repeat — (1) sample $\langle s, v^\pi\rangle \sim \mathcal{D}$; (2) apply $\Delta\mathbf{w} = \alpha(v^\pi - \hat{v}(s,\mathbf{w}))\nabla_\mathbf{w}\hat{v}(s,\mathbf{w})$. **Converges to the least squares solution** $\mathbf{w}^\pi = \arg\min_\mathbf{w}LS(\mathbf{w})$.

### Deep Q-Networks (DQN)

> **DQN uses experience replay and fixed Q-targets:**
> - Take action $a_t$ according to an **$\epsilon$-greedy** policy
> - **Store transition $(s_t,a_t,r_{t+1},s_{t+1})$ in replay memory $\mathcal{D}$**
> - **Sample a random mini-batch** of transitions $(s,a,r,s')$ from $\mathcal{D}$
> - **Compute Q-learning targets w.r.t. old, fixed parameters $\mathbf{w}^-$**
> - Optimise MSE between the Q-network and the Q-learning target *(truncated)*

$$\mathcal{L}_i(\mathbf{w}_i) = \mathbb{E}_{s,a,r,s'\sim\mathcal{D}_i}\left[\left(r + \gamma\max_{a'}Q(s',a';\mathbf{w}_i^-) - Q(s,a;\mathbf{w}_i)\right)^2\right]$$

**The two tricks are what make Q-learning work with a neural network** — see Exercise 4.

**DQN in Atari:**
> - **End-to-end learning of $Q(s,a)$ from pixels $s$**
> - **Input state is a stack of raw pixels from the last 4 frames**
> - **Output is $Q(s,a)$ for 18 joystick/button positions**
> - **Reward is the change in score for that step**
> - **Network architecture and hyperparameters fixed across all games**

That last point is the headline result: **one algorithm, one architecture, no per-game tuning**, across dozens of games.

**How much does DQN help?** (mean scores)

| | Replay + Fixed-Q | Replay + Q-learning | No replay + Fixed-Q | No replay + Q-learning |
|---|---|---|---|---|
| **Breakout** | **316.81** | 240.73 | 10.16 | 3.17 |
| **Enduro** | **1006.3** | 831.25 | 141.89 | 29.1 |
| **River Raid** | **7446.62** | 4102.81 | 2867.66 | 1453.02 |
| **Seaquest** | **2894.4** | 822.55 | 1003 | 275.81 |
| **Space Invaders** | **1088.94** | 826.33 | 373.22 | 301.99 |

**Replay matters enormously** (Breakout: 316 vs 10, a 30× difference); **fixed targets help substantially on top** (316 vs 240).

### Linear least squares — the direct solution

> Experience replay finds the least squares solution **but may take many iterations.** With linear approximation we can **solve directly.**

At the minimum, the expected update must be zero:
$$\mathbb{E}_\mathcal{D}[\Delta\mathbf{w}] = 0 \;\Rightarrow\; \sum_{t=1}^{T}\mathbf{x}(s_t)\big(v^\pi_t - \mathbf{x}(s_t)^\top\mathbf{w}\big) = 0$$
$$\mathbf{w} = \left(\sum_{t=1}^{T}\mathbf{x}(s_t)\mathbf{x}(s_t)^\top\right)^{-1}\sum_{t=1}^{T}\mathbf{x}(s_t)v^\pi_t$$

> **For $N$ features, direct solution time is $O(N^3)$. Incremental solution is $O(N^2)$ using Sherman–Morrison.**

Note the cost depends on the **number of features**, not the number of states — which is exactly the point of function approximation.

**Since we do not know $v^\pi_t$, substitute noisy or biased samples:**

| Algorithm | Target | Solution |
|---|---|---|
| **LSMC** | $v^\pi_t \approx G_t$ | $\mathbf{w} = \left(\sum\mathbf{x}(S_t)\mathbf{x}(S_t)^\top\right)^{-1}\sum\mathbf{x}(S_t)G_t$ |
| **LSTD** | $v^\pi_t \approx R_{t+1} + \gamma\hat{v}(S_{t+1},\mathbf{w})$ | $\mathbf{w} = \left(\sum\mathbf{x}(S_t)(\mathbf{x}(S_t)-\gamma\mathbf{x}(S_{t+1}))^\top\right)^{-1}\sum\mathbf{x}(S_t)R_{t+1}$ |
| **LSTD(λ)** | $v^\pi_t \approx G^\lambda_t$ | $\mathbf{w} = \left(\sum E_t(\mathbf{x}(S_t)-\gamma\mathbf{x}(S_{t+1}))^\top\right)^{-1}\sum E_t R_{t+1}$ |

**Crucially, LSTD converges even off-policy with linear approximation** (marked ✓ where TD is ✗) — solving directly avoids the semi-gradient instability.

### Least Squares Policy Iteration (LSPI)

> For control we also want to improve the policy, and **this experience is generated from many policies — so to evaluate $q_\pi(S,A)$ we must learn off-policy.** Same idea as Q-learning: use experience from $\pi_{old}$, consider the alternative successor action *(truncated)*.

**LSTDQ:**
$$\delta = R_{t+1} + \gamma\hat{q}(S_{t+1},\pi(S_{t+1}),\mathbf{w}) - \hat{q}(S_t,A_t,\mathbf{w})$$
$$\mathbf{w} = \left(\sum_{t=1}^{T}\mathbf{x}(S_t,A_t)\big(\mathbf{x}(S_t,A_t)-\gamma\mathbf{x}(S_{t+1},\pi(S_{t+1}))\big)^\top\right)^{-1}\sum_{t=1}^{T}\mathbf{x}(S_t,A_t)R_{t+1}$$

```
function LSPI-TD(D, π₀)
    π' ← π₀
    repeat
        π ← π'
        Q ← LSTDQ(π, D)
        for all s ∈ S do
            π'(s) ← argmax_{a∈A} Q(s,a)
        end for
    until (π ≈ π')
    return π
end function
```

> **It repeatedly re-evaluates the same experience $\mathcal{D}$ with different policies.**

That is LSPI's defining property: **one fixed dataset, reused for every policy iteration** — maximum sample efficiency. **Chain Walk** is the worked example.

## ✏️ Exercises

**1.** Explain why table lookup is a special case of linear function approximation, and what that tells us about Part I.

> [!example]- Solution
> With **one-hot features** $\mathbf{x}^{table}(S) = (\mathbb{1}(S=s_1), \dots, \mathbb{1}(S=s_n))^\top$, exactly one component is 1 and the rest are 0. So
> $$\hat{v}(s_i,\mathbf{w}) = \mathbf{x}(s_i)^\top\mathbf{w} = w_i$$
> **Each parameter *is* a state's value.** The linear update
> $$\Delta\mathbf{w} = \alpha(v_\pi(S) - \hat{v}(S,\mathbf{w}))\mathbf{x}(S)$$
> has $\mathbf{x}(S)$ zero everywhere except position $i$, so **only $w_i$ changes** — reproducing the tabular update exactly.
>
> **What this tells us — three things:**
>
> **1. Part I's algorithms are unchanged, only re-parameterised.** Sarsa and Q-learning with one-hot features *are* tabular Sarsa and Q-learning. Nothing new was introduced; the representation was generalised.
>
> **2. It explains why Part I's convergence results were so clean.** With one-hot features the updates are **completely decoupled** — changing $w_i$ cannot affect any other state's estimate. There is no interference, so no instability. **Every divergence problem in this lecture arises from features that *overlap*.**
>
> **3. It shows what generalisation costs.** Table lookup has **zero generalisation** — visiting $s_1$ teaches nothing about $s_2$, however similar. That is why it needs $|\mathcal{S}|$ visits and cannot scale. Overlapping features buy generalisation, and the price is that updates now interfere: improving one state's estimate can degrade another's.
>
> **The trade-off is the whole lecture in miniature.** Table lookup: perfectly stable, hopelessly unscalable. Rich features: scalable, potentially divergent. Everything between is a choice about how much interference to accept for how much generalisation.

**2.** Explain the deadly triad using the convergence tables. Which combinations diverge, and why?

> [!example]- Solution
> **The three ingredients** — reading across the tables, divergence requires all of:
> 1. **Function approximation** (beyond table lookup)
> 2. **Bootstrapping** (TD, not MC)
> 3. **Off-policy** learning
>
> **Any two are safe; all three can diverge.**
>
> Reading the prediction table confirms it:
> - **MC is ✓ everywhere** — it does not bootstrap, so one leg is missing regardless of the others.
> - **On-policy TD is ✓ with linear** — off-policy leg missing.
> - **Off-policy TD with linear is ✗** — all three present. **Baird's counterexample.**
> - **Table lookup is ✓ everywhere** — approximation leg missing (Exercise 1).
>
> **Why the combination is fatal.** The lecture gives the crucial diagnosis: **"TD does not follow the gradient of any objective function."**
>
> The TD update *looks* like gradient descent on $(\text{target} - \hat{v})^2$, but the target $R + \gamma\hat{v}(S',\mathbf{w})$ **contains $\mathbf{w}$**. True gradient descent would differentiate through it; TD does not. This makes TD a **semi-gradient** method — it is not minimising anything, so there is no objective whose decrease guarantees stability.
>
> With **table lookup** this does not matter: updates are decoupled, so a change to one state cannot feed back. With **function approximation** it does: updating $\mathbf{w}$ for state $s$ changes $\hat{v}(s')$, which changes the target for $s$, which changes $\mathbf{w}$ again. A **positive feedback loop**.
>
> **On-policy learning contains the loop** because the states you update are the states you visit, in the proportions you visit them — the distribution is self-consistent. **Off-policy breaks that**: you update states in proportions unrelated to how the behaviour policy visits them, so the feedback can amplify without correction. In Baird's counterexample the parameters grow without bound.
>
> **Gradient TD fixes it** by following the true gradient of the **projected Bellman error** — a genuine objective function — restoring convergence in every cell.
>
> **Why this matters practically:** Q-learning is off-policy and bootstraps, so Q-learning with a neural network has all three legs. **DQN is exactly this combination**, which is why it needed the stabilising tricks of Exercise 4.

**3.** Why is control harder than prediction under function approximation? Explain "chatters around near-optimal".

> [!example]- Solution
> Compare the tables. **Prediction:** on-policy TD with linear approximation is **✓** — full convergence. **Control:** Sarsa with linear is only **(✓)** — *"chatters around near-optimal"*. Same algorithm family, same representation, weaker guarantee.
>
> **Three compounding reasons:**
>
> **1. The target moves because the policy moves.** In prediction, $\pi$ is fixed, so $v_\pi$ is a fixed function and we approximate a stationary target. In control, $\epsilon$-greedy improvement changes $\pi$ **every time $\mathbf{w}$ changes**, so the function being approximated shifts continuously. You are chasing a target that moves when you step toward it.
>
> **2. Small parameter changes cause discontinuous policy changes.** The greedy $\arg\max$ is a step function of $\mathbf{w}$. A tiny update that flips the ordering of two nearly-equal $\hat{q}$ values changes the policy **discretely**, which changes the state distribution, which changes what is learned. This is the source of "chattering" — the policy oscillates between neighbouring choices without settling.
>
> **3. Approximation error is not uniform.** With a table, greedy improvement is guaranteed correct because $Q$ is exact. With approximation, $\hat{q}$ has error, and $\arg\max$ **selects for over-estimation** — actions whose values happen to be over-estimated are exactly the ones chosen. The policy improvement theorem of [[03 - Planning by Dynamic Programming]] assumed exact $q_\pi$ and no longer applies.
>
> **What "chatters" means concretely:** $\mathbf{w}$ does not converge to a point. It moves within a bounded region near the optimum, and the induced policy keeps switching between a few near-optimal alternatives. **Performance is good and stable; the parameters are not.** This is very different from divergence — nothing explodes, and the practical behaviour is acceptable.
>
> **Q-learning is worse still — ✗ even with linear approximation** — because it is off-policy, adding the third leg of the deadly triad on top of the control problems above.
>
> **Practical mitigations:** decay $\epsilon$ and $\alpha$ (GLIE and Robbins–Monro from [[05 - Model-Free Control]]), use richer features so near-ties are rarer, or use **policy gradient methods** ([[07 - Policy Gradient Methods]]) which parameterise $\pi$ smoothly and avoid the discontinuous $\arg\max$ entirely. That is a major motivation for the next lecture.

**4.** Explain DQN's two innovations — experience replay and fixed Q-targets — and interpret the ablation table.

> [!example]- Solution
> **DQN is Q-learning with a neural network — the full deadly triad.** Both tricks exist to make that combination stable.
>
> **Experience replay.** Store transitions $(s_t,a_t,r_{t+1},s_{t+1})$ in a memory $\mathcal{D}$ and train on **random mini-batches** rather than on the current transition. Two benefits:
>
> - **Breaks correlation.** Consecutive frames in Atari are nearly identical, so sequential training gives highly correlated gradients — violating the i.i.d. assumption SGD relies on. Random sampling restores approximate independence. This is the non-i.i.d. problem from [[01 - Introduction to Reinforcement Learning]], solved directly.
> - **Sample efficiency.** Each transition is reused many times instead of once — the batch-methods motivation, *"gradient descent is not sample efficient."*
>
> It also **smooths the data distribution** over many past policies, which dampens the feedback loop of Exercise 2.
>
> **Fixed Q-targets.** Compute targets using **old, frozen parameters $\mathbf{w}^-$**, updated only periodically:
> $$\mathcal{L}(\mathbf{w}) = \mathbb{E}\left[\left(r + \gamma\max_{a'}Q(s',a';\mathbf{w}^-) - Q(s,a;\mathbf{w})\right)^2\right]$$
> **This directly attacks the semi-gradient problem.** With $\mathbf{w}^-$ frozen, the target is a **constant** during the update, so the loss becomes a genuine supervised regression with a fixed objective — momentarily restoring the guarantees that semi-gradient TD lacks. Without it, updating $Q(s,a)$ also moves $Q(s',a')$, and the network chases its own tail.
>
> **The ablation table:**
>
> | Breakout | Replay+Fixed-Q **316.81** | Replay only 240.73 | Fixed-Q only 10.16 | Neither **3.17** |
>
> **Replay is the dominant factor.** Comparing the two replay columns against the two non-replay columns: 316 and 240 versus 10 and 3 — a **30–100× difference** on Breakout, and consistently large across all five games. Without replay, the algorithm barely learns at all.
>
> **Fixed targets add a substantial further gain**, roughly 30% on Breakout and 3.5× on Seaquest (2894 vs 822). Notably, **fixed-Q alone barely helps** (10.16 vs 3.17) — it is only valuable once replay has fixed the correlation problem. **The two are complementary, not independent.**
>
> **The broader significance:** *"network architecture and hyperparameters fixed across all games"* — one algorithm learning dozens of games from raw pixels with no per-game tuning, which is what made DQN a landmark. It is also an honest illustration that the deadly triad is a **practical engineering problem**, not merely a theoretical caveat: without these two tricks, the exact same algorithm fails.

**5.** (Advanced) Compare LSTD with incremental TD, and explain LSPI's advantage.

> [!example]- Solution
> **Incremental TD** processes each transition once with $\Delta\mathbf{w} = \alpha\delta\mathbf{x}(S)$: $O(N)$ per step, $O(N)$ memory, and needs a well-tuned $\alpha$.
>
> **LSTD solves for the fixed point directly:**
> $$\mathbf{w} = \left(\sum_t\mathbf{x}(S_t)(\mathbf{x}(S_t)-\gamma\mathbf{x}(S_{t+1}))^\top\right)^{-1}\sum_t\mathbf{x}(S_t)R_{t+1}$$
> $O(N^3)$ direct or $O(N^2)$ incrementally via Sherman–Morrison, and $O(N^2)$ memory for the matrix.
>
> **LSTD's advantages:**
> - **No step-size parameter.** No $\alpha$ to tune, and no sensitivity to getting it wrong.
> - **Far more sample efficient.** It extracts the least-squares solution from the data in one shot rather than converging toward it over many passes.
> - **Converges off-policy with linear approximation** — ✓ where incremental TD is ✗. Solving the fixed-point equation directly sidesteps the semi-gradient feedback loop that causes divergence.
>
> **Its costs:** $O(N^2)$ memory and $O(N^2$–$N^3)$ computation make it infeasible for the large $N$ that neural networks use. **LSTD is for hundreds of features, not millions of weights** — and it is restricted to *linear* approximation, since the closed form depends on linearity.
>
> **LSPI's advantage is sample reuse.** The pseudocode's key property: *"it repeatedly re-evaluates experience $\mathcal{D}$ with different policies."*
> ```
> repeat
>     π ← π'
>     Q ← LSTDQ(π, D)         ← same D, every iteration
>     π'(s) ← argmax_a Q(s,a)
> until π ≈ π'
> ```
> **One fixed dataset serves every policy iteration.** Incremental Sarsa must gather *fresh* experience after each policy change, because it is on-policy. LSPI evaluates a completely new policy on **old data**, because LSTDQ is off-policy — it uses $\hat{q}(S_{t+1},\pi(S_{t+1}))$, the value of the action the *target* policy would take, not the one that was taken.
>
> **When this matters:** whenever experience is expensive. A robot that takes hours to gather 10,000 transitions can run LSPI to convergence on them offline, trying many policies, without any further interaction. That is the extreme case of the batch-methods argument, and it is why LSPI remains relevant despite scaling limits.
>
> **The trade-off summary:** LSTD/LSPI buy **sample efficiency and stability** at the cost of **computational scalability**; incremental methods with neural networks buy **scalability** at the cost of needing tricks like replay and fixed targets to remain stable.

## 📝 Summary

- **Lookup tables cannot scale** — too much memory, and too slow to learn each state individually. Function approximation **generalises** experience across states.
- **Table lookup is linear approximation with one-hot features**, which is why Part I's convergence was so clean: no interference between updates.
- **Linear approximation:** $\hat{v}(S,\mathbf{w}) = \mathbf{x}(S)^\top\mathbf{w}$, update = $\alpha \times$ error $\times$ feature. The objective is quadratic, so SGD finds the **global** optimum.
- **Substitute a target for $v_\pi$:** $G_t$ (MC, unbiased), $R + \gamma\hat{v}(S',\mathbf{w})$ (TD, biased), $G^\lambda_t$ (TD(λ)).
- **TD does not follow the gradient of any objective function** — it is semi-gradient, which is why it can diverge.
- **The deadly triad:** function approximation + bootstrapping + off-policy. **Any two are safe; all three can diverge** (Baird's counterexample).
- **MC converges everywhere; on-policy TD converges with linear; off-policy TD with linear diverges.** **Gradient TD** converges in all cases by following the projected Bellman error.
- **Control is weaker than prediction** — Sarsa with linear approximation only "**chatters** around near-optimal", because the target moves as the policy changes and $\arg\max$ is discontinuous.
- **Batch methods reuse experience.** **DQN = experience replay + fixed Q-targets**, which is what makes Q-learning work with a neural network.
- **LSTD solves the fixed point directly** — no step size, sample efficient, **converges off-policy** — at $O(N^2$–$N^3)$ cost.
- **LSPI re-evaluates one fixed dataset under many policies**, the extreme of sample efficiency.

## ⚠️ Important Notes

**TD with function approximation is not gradient descent.** The target depends on $\mathbf{w}$ and TD ignores that dependence. There is no objective function being minimised, so no stability guarantee.

**The deadly triad needs all three legs.** Diagnosing a divergence means asking which leg to remove: use MC (no bootstrapping), go on-policy, or use Gradient TD.

**Off-policy TD with linear approximation can diverge — parameters grow without bound.** This is not slow convergence or bias; it is explosion. Baird's counterexample is small and deliberate.

**Q-learning with a neural network has all three legs.** DQN works because of replay and fixed targets, not despite the triad.

**Experience replay is the larger of DQN's two tricks** — 30–100× on Breakout. Fixed targets add a further substantial gain, but barely help without replay.

**Control is strictly harder than prediction under approximation.** Even on-policy Sarsa only chatters, because greedy improvement is discontinuous in $\mathbf{w}$ and the target is non-stationary.

**"Chatters" ≠ diverges.** Performance stays near-optimal while parameters oscillate — acceptable in practice, unlike divergence.

**The $\arg\max$ selects for over-estimation.** With noisy $\hat{q}$, greedy improvement systematically picks actions whose values are over-estimated — a bias absent from the tabular case, and the origin of Double Q-learning.

**LSTD's cost is in the number of features, not states** — $O(N^2)$ memory, $O(N^3)$ direct solution. Infeasible for neural networks, ideal for modest linear feature sets.

**LSTD converges off-policy where incremental TD does not**, because solving the fixed-point equation avoids the semi-gradient feedback loop.

**LSPI's power is reusing one dataset across all policy iterations**, made possible because LSTDQ is off-policy. On-policy methods must re-collect after every policy change.

**Eligibility traces under function approximation are over features, not states** — $E_t = \gamma\lambda E_{t-1} + \mathbf{x}(S_t)$, a vector of the same dimension as $\mathbf{w}$.

> [!warning] Gaps in the source slides
> Silver's slides extract well, **but this lecture has one unusually costly loss:**
>
> **⚠️ The ✓/✗ symbols in every convergence table (slides 30, 31, 32, 46, 52) failed to extract** — they appear as blank boxes. **The tables in this note are reconstructed from the standard results** (Sutton & Barto Ch. 11, Table 11.1) and from the surrounding text, which does state the key facts explicitly (*"TD can diverge when off-policy or using non-linear function approximation"*, *"() = chatters around near-optimal"*). **Verify the marks against the original PDF before an exam — these tables are highly examinable.**
>
> Other losses, all figures:
> - **Slides 25–27 (Mountain Car)** — linear Sarsa with **coarse coding**, with **radial basis functions**, and the **"Study of λ: Should We Bootstrap?"** plot are entirely images. **Coarse coding and RBFs are named but never defined in text**, and the λ study — the empirical evidence on bootstrapping — is lost.
> - **Slides 28–29 (Baird's counterexample)** — both the MDP structure and the parameter-divergence plot are images. **The counterexample is referenced as the justification for the whole convergence discussion, but its content is not recoverable.**
> - **Slide 7** — the three function-approximation architectures diagram; labels extracted.
> - **Slide 11** — the gradient descent figure, with garbled caption text.
> - **Slide 40** — DQN Atari results figure (the score-vs-human bar chart).
> - **Slides 21, 47** — the GPI cycle diagrams.
> - **Slides 53–55 (Chain Walk / LSPI)** — the MDP figure and the per-iteration value and policy plots are images from the Lagoudakis & Parr LSPI paper; axis labels extracted but not the content.
> - **Truncations:** slide 6 (cut at *"function app"*), slide 12 (SGD update cut), slide 14 (cut at "Up"), slide 16 (TD update cut at $\hat v(S_t$), slide 17 (**cut at *"Monte-Carlo evaluation converges to a"*** — "local optimum"), slide 18 (**cut at *"Linear TD(0) converges (clos"*** — "close to global optimum"), slides 19–20 (**backward-view TD(λ) update cut mid-line** — duplicated overlay slides, both truncated identically), slide 24 (forward-view TD(λ) control target cut), slide 35 ($LS(\mathbf{w})$ formula cut), slide 38 (DQN loss cut at "targe"), slide 44 (cut at *"solve direc"*), slide 48 (dataset definition cut), slide 49 (cut at *"Consider alternative successor actio"*).
> - **Slides 4/5, 19/20, 36/37 are duplicate overlay pairs.**
>
> **References:** DQN — Mnih et al., *Human-level control through deep reinforcement learning*, Nature 2015. LSPI — Lagoudakis & Parr, *Least-Squares Policy Iteration*, JMLR 2003 (the Chain Walk figures are from this paper).

---
**Previous:** [[05 - Model-Free Control]] · **Next:** [[07 - Policy Gradient Methods]]
