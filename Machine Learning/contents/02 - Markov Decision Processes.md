---
subject: Machine Learning
chapter: 02
tags: [ds, reinforcement-learning, mdp, bellman-equation, value-function, markov]
source: "lecture-2-mdp.pdf — David Silver, UCL (Lecture 2 of 10)"
---

# Markov Decision Processes

> [!note] Where this sits in the course
> **The mathematical foundation of the entire course.** [[01 - Introduction to Reinforcement Learning]] introduced the agent, environment, policy, value function, and model informally; this lecture makes all of it precise. Every algorithm in Lectures 3–10 is a way of solving the Bellman equations defined here.
>
> The build is deliberate: **Markov Process → Markov Reward Process → Markov Decision Process**, adding one ingredient at a time.

## 📘 Main Knowledge

> Markov decision processes formally describe an environment for reinforcement learning **where the environment is fully observable** — the current state completely characterises the process.
>
> **Almost all RL problems can be formalised as MDPs:** optimal control primarily deals with continuous MDPs · partially observable problems can be converted into MDPs · **bandits are MDPs with one state**.

---

## Part 1 — Markov Processes

### The Markov property

> **"The future is independent of the past given the present."**
>
> A state $S_t$ is **Markov** if and only if
> $$\mathbb{P}[S_{t+1} \mid S_t] = \mathbb{P}[S_{t+1} \mid S_1, \dots, S_t]$$
>
> The state captures all relevant information from the history. **Once the state is known, the history may be thrown away** — the state is a **sufficient statistic** of the future.

### State transition matrix

For a Markov state $s$ and successor $s'$:
$$\mathcal{P}_{ss'} = \mathbb{P}[S_{t+1} = s' \mid S_t = s]$$

$$\mathcal{P} = \begin{bmatrix} \mathcal{P}_{11} & \cdots & \mathcal{P}_{1n} \\ \vdots & & \vdots \\ \mathcal{P}_{n1} & \cdots & \mathcal{P}_{nn} \end{bmatrix}$$

**Each row sums to 1** — from any state, the transition probabilities form a distribution.

### Markov Process

> A **Markov Process** (or **Markov Chain**) is a tuple $\langle \mathcal{S}, \mathcal{P} \rangle$:
> - $\mathcal{S}$ is a (finite) set of states
> - $\mathcal{P}$ is a state transition probability matrix
>
> A **memoryless random process** — a sequence of random states $S_1, S_2, \dots$ with the Markov property.

**No rewards, no actions.** Just a system wandering between states.

### The Student Markov Chain

The running example throughout the lecture. States: **Class 1, Class 2, Class 3, Pass, Pub, Facebook, Sleep**.

$$\mathcal{P} = \begin{array}{c|ccccccc} & C1 & C2 & C3 & Pass & Pub & FB & Sleep \\\hline C1 & & 0.5 & & & & 0.5 & \\ C2 & & & 0.8 & & & & 0.2 \\ C3 & & & & 0.6 & 0.4 & & \\ Pass & & & & & & & 1.0 \\ Pub & 0.2 & 0.4 & 0.4 & & & & \\ FB & 0.1 & & & & & 0.9 & \\ Sleep & & & & & & & 1 \end{array}$$

**Sample episodes** starting from $S_1 = C1$:
```
C1  C2  C3  Pass  Sleep
C1  FB  FB  C1  C2  Sleep
C1  C2  C3  Pub  C2  C3  Pass  Sleep
C1  FB  FB  C1  C2  C3  Pub  C1  FB  FB  FB  C1  C2  C3  Pub  C2  Sleep
```

Note **Sleep is absorbing** ($\mathcal{P}_{\text{Sleep,Sleep}} = 1$) — it terminates the episode. And Facebook is a trap with a 0.9 self-loop: once distracted, the student tends to stay distracted.

---

## Part 2 — Markov Reward Processes

> A **Markov Reward Process** is a Markov chain **with values** — a tuple $\langle \mathcal{S}, \mathcal{P}, \mathcal{R}, \gamma \rangle$:
> - $\mathcal{R}$ is a reward function, $\mathcal{R}_s = \mathbb{E}[R_{t+1} \mid S_t = s]$
> - $\gamma$ is a **discount factor**, $\gamma \in [0,1]$

**Student MRP rewards:** Class 1, 2, 3 give $R = -2$ · Facebook gives $R = -1$ · Pub gives $R = +1$ · **Pass gives $R = +10$** · Sleep gives $R = 0$.

### Return

> The **return** $G_t$ is the total discounted reward from time-step $t$:
> $$G_t = R_{t+1} + \gamma R_{t+2} + \dots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

- The discount $\gamma \in [0,1]$ is the **present value of future rewards**
- The value of receiving reward $R$ after $k+1$ time-steps is $\gamma^k R$
- **This values immediate reward above delayed reward**
- **$\gamma$ close to 0 leads to "myopic" evaluation; $\gamma$ close to 1 leads to "far-sighted" evaluation**

**$G_t$ is a random variable** — one number per sampled episode, not an expectation. That distinction is the whole reason value functions exist.

### Why discount?

- **Mathematically convenient** to discount rewards
- **Avoids infinite returns** in cyclic Markov processes
- Uncertainty about the future may not be fully represented
- If the reward is financial, **immediate rewards may earn more interest**
- **Animal/human behaviour shows preference for immediate reward**
- **It is sometimes possible to use undiscounted** Markov reward processes (e.g. if all sequences terminate)

The second reason is the load-bearing one: the Student chain has cycles (Facebook's self-loop, the Pub loop), so with $\gamma = 1$ an episode could in principle run forever and accumulate unbounded negative reward.

### Value function

> The **state value function** $v(s)$ of an MRP is the **expected return** starting from state $s$:
> $$v(s) = \mathbb{E}[G_t \mid S_t = s]$$

**Sample returns** from $C1$ with $\gamma = \tfrac12$:
```
C1 C2 C3 Pass Sleep         →  -2 - 2(½) - 2(¼) + 10(⅛)  = -2.25
C1 FB FB C1 C2 Sleep        →  -2 - 1(½) - 1(¼) - 2(⅛) - 2(1/16) = -3.125
C1 C2 C3 Pub C2 C3 Pass ... →  -3.41
C1 FB FB C1 C2 C3 Pub C1 ...→  -3.20
```

**Different episodes from the same state give different returns.** $v(C1)$ is their expectation.

**How $\gamma$ changes the value function** — the same MRP, three discounts:

| State | $\gamma = 0$ | $\gamma = 0.9$ | $\gamma = 1$ |
|---|---|---|---|
| Class 1 | −2 | −5.0 | **−13** |
| Class 2 | −2 | 0.9 | 1.5 |
| Class 3 | −2 | 4.1 | 4.3 |
| Pass | +10 | 10 | 10 |
| Pub | +1 | 1.9 | +0.8 |
| Facebook | −1 | −7.6 | **−23** |
| Sleep | 0 | 0 | 0 |

At $\gamma = 0$ the value is just the immediate reward — the agent is completely myopic. At $\gamma = 1$ Facebook's value collapses to −23, because the far-sighted agent fully accounts for the cost of the 0.9 self-loop trapping it for many steps.

### The Bellman Equation for MRPs

**The central decomposition of the whole course.** The value function splits into **immediate reward** plus **discounted value of the successor state**:

$$\begin{aligned} v(s) &= \mathbb{E}[G_t \mid S_t = s] \\ &= \mathbb{E}[R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots \mid S_t = s] \\ &= \mathbb{E}[R_{t+1} + \gamma(R_{t+2} + \gamma R_{t+3} + \dots) \mid S_t = s] \\ &= \mathbb{E}[R_{t+1} + \gamma G_{t+1} \mid S_t = s] \\ &= \boxed{\mathbb{E}[R_{t+1} + \gamma v(S_{t+1}) \mid S_t = s]} \end{aligned}$$

Expanding the expectation over successor states:
$$v(s) = \mathcal{R}_s + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}_{ss'}\, v(s')$$

**Worked check** (Student MRP, $\gamma = 1$, state Class 3):
$$4.3 = -2 + 0.6 \times 10 + 0.4 \times 0.8$$

### Matrix form and direct solution

$$v = \mathcal{R} + \gamma \mathcal{P} v$$

**The Bellman equation is linear**, so it can be solved directly:
$$(I - \gamma \mathcal{P})v = \mathcal{R} \quad\Longrightarrow\quad v = (I - \gamma\mathcal{P})^{-1}\mathcal{R}$$

- **Computational complexity is $O(n^3)$** for $n$ states
- **Direct solution only possible for small MRPs**
- Iterative methods for large MRPs: **Dynamic Programming** ([[03 - Planning by Dynamic Programming]]), **Monte-Carlo evaluation** and **Temporal-Difference learning** ([[04 - Model-Free Prediction]])

See [[Linear Algebra/contents/00-Index|Linear Algebra]] for matrix inversion.

---

## Part 3 — Markov Decision Processes

> A **Markov Decision Process** is a Markov reward process **with decisions** — a tuple $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$:
> - $\mathcal{A}$ is a finite set of **actions**
> - $\mathcal{P}^a_{ss'} = \mathbb{P}[S_{t+1} = s' \mid S_t = s, A_t = a]$
> - $\mathcal{R}^a_s = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$

**Transitions and rewards now depend on the action**, which is what makes control possible.

**Student MDP** — the states become decision points with actions **Study, Facebook, Quit, Sleep, Pub**.

### Policies

> A **policy** $\pi$ is a distribution over actions given states:
> $$\pi(a \mid s) = \mathbb{P}[A_t = a \mid S_t = s]$$
>
> - A policy **fully defines the behaviour** of an agent
> - **MDP policies depend on the current state, not the history**
> - Policies are **stationary** (time-independent): $A_t \sim \pi(\cdot \mid S_t), \forall t > 0$

**Fixing a policy collapses an MDP back to an MRP:**

Given an MDP $\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma\rangle$ and a policy $\pi$:
- The state sequence $S_1, S_2, \dots$ is a **Markov process** $\langle \mathcal{S}, \mathcal{P}^\pi\rangle$
- The state and reward sequence is a **Markov reward process** $\langle \mathcal{S}, \mathcal{P}^\pi, \mathcal{R}^\pi, \gamma\rangle$

$$\mathcal{P}^\pi_{s,s'} = \sum_{a \in \mathcal{A}} \pi(a\mid s)\,\mathcal{P}^a_{ss'} \qquad \mathcal{R}^\pi_s = \sum_{a \in \mathcal{A}} \pi(a\mid s)\,\mathcal{R}^a_s$$

**This is why the lecture builds MP → MRP → MDP.** Evaluating a policy in an MDP *is* solving the induced MRP, so all the MRP machinery carries over unchanged.

### Two value functions

> The **state-value function** $v_\pi(s)$ is the expected return starting from $s$ and then following $\pi$:
> $$v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$$
>
> The **action-value function** $q_\pi(s,a)$ is the expected return starting from $s$, **taking action $a$**, and then following $\pi$:
> $$q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a]$$

**Student MDP state values** for the uniform random policy $\pi(a\mid s) = 0.5$, $\gamma = 1$: Facebook −2.3 · Class 1 −1.3 · Class 2 2.7 · Class 3 7.4 · Sleep 0.

### Bellman Expectation Equations

The same decomposition, now for both value functions:

$$v_\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma v_\pi(S_{t+1}) \mid S_t = s]$$
$$q_\pi(s,a) = \mathbb{E}_\pi[R_{t+1} + \gamma q_\pi(S_{t+1}, A_{t+1}) \mid S_t = s, A_t = a]$$

**The four backup relations** — the lecture derives these as one-step and two-step lookaheads:

**$v$ in terms of $q$** (average over actions the policy might take):
$$v_\pi(s) = \sum_{a\in\mathcal{A}} \pi(a\mid s)\, q_\pi(s,a)$$

**$q$ in terms of $v$** (immediate reward plus expected successor value):
$$q_\pi(s,a) = \mathcal{R}^a_s + \gamma \sum_{s'\in\mathcal{S}} \mathcal{P}^a_{ss'}\, v_\pi(s')$$

**Substituting each into the other gives the two-step forms:**
$$v_\pi(s) = \sum_{a\in\mathcal{A}} \pi(a\mid s)\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'} v_\pi(s')\right)$$
$$q_\pi(s,a) = \mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}\sum_{a'\in\mathcal{A}} \pi(a'\mid s')\, q_\pi(s',a')$$

**Worked check** (Student MDP, Class 3, $\pi = 0.5$ uniform):
$$7.4 = 0.5\big(1 + 0.2(-1.3) + 0.4(2.7) + 0.4(7.4)\big) + 0.5 \times 10$$

**Matrix form** — using the induced MRP:
$$v_\pi = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v_\pi \quad\Longrightarrow\quad v_\pi = (I - \gamma\mathcal{P}^\pi)^{-1}\mathcal{R}^\pi$$

### Optimal value functions

> The **optimal state-value function** is the maximum over all policies:
> $$v_*(s) = \max_\pi v_\pi(s)$$
> The **optimal action-value function**:
> $$q_*(s,a) = \max_\pi q_\pi(s,a)$$
>
> The optimal value function specifies **the best possible performance in the MDP**. **An MDP is "solved" when we know the optimal value function.**

**Student MDP optima** ($\gamma=1$): $v_*$ = Facebook 6 · Class 1 6 · Class 2 8 · Class 3 10 · Sleep 0.
$q_*$ values include: Facebook/Facebook 5, Facebook/Quit 6, Class 1/Study 6, Class 3/Study 10, **Class 3/Pub 8.4**, Class 2/Sleep 0.

### Optimal policy

Define a **partial ordering** over policies: $\pi \ge \pi'$ if $v_\pi(s) \ge v_{\pi'}(s)$ for **all** $s$.

> **Theorem.** For any Markov Decision Process:
> - There exists an **optimal policy $\pi_*$** that is better than or equal to all other policies, $\pi_* \ge \pi, \forall\pi$
> - **All optimal policies achieve the optimal value function**, $v_{\pi_*}(s) = v_*(s)$
> - All optimal policies achieve the optimal action-value function, $q_{\pi_*}(s,a) = q_*(s,a)$

**Finding an optimal policy** — maximise over $q_*$:
$$\pi_*(a\mid s) = \begin{cases} 1 & \text{if } a = \arg\max_{a\in\mathcal{A}} q_*(s,a) \\ 0 & \text{otherwise}\end{cases}$$

> **There is always a deterministic optimal policy for any MDP.**
> **If we know $q_*(s,a)$, we immediately have the optimal policy.**

That last line is why so many algorithms target $q_*$ directly — Q-learning and Sarsa in [[05 - Model-Free Control]].

### Bellman Optimality Equations

$$v_*(s) = \max_a q_*(s,a)$$
$$q_*(s,a) = \mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}\, v_*(s')$$

Combining:
$$\boxed{v_*(s) = \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'} v_*(s')\right)}$$
$$\boxed{q_*(s,a) = \mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}\max_{a'} q_*(s',a')}$$

**Worked check** (Student MDP, Class 1):
$$6 = \max\{-2 + 8,\; -1 + 6\}$$

> **Solving the Bellman Optimality Equation:**
> - **It is non-linear** (because of the $\max$)
> - **No closed form solution** in general
> - Many iterative solution methods: **Value Iteration, Policy Iteration** ([[03 - Planning by Dynamic Programming]]), **Q-learning, Sarsa** ([[05 - Model-Free Control]])

**The $\max$ is the entire difficulty of RL.** The expectation equation is linear and invertible; the optimality equation is not, and every algorithm in the rest of the course is a way around that.

---

## Part 4 — Extensions (marked "no exam")

**Infinite and continuous MDPs:** countably infinite state/action spaces are straightforward · continuous spaces have a closed form for the **linear quadratic model (LQR)** · **continuous time** requires partial differential equations and the **Hamilton–Jacobi–Bellman (HJB) equation**, the limiting case of the Bellman equation as the time-step → 0.

**POMDPs** — an MDP with hidden states; a hidden Markov model with actions. A tuple $\langle\mathcal{S},\mathcal{A},\mathcal{O},\mathcal{P},\mathcal{R},\mathcal{Z},\gamma\rangle$ where $\mathcal{O}$ is a set of observations and $\mathcal{Z}$ an observation function.

A **belief state** $b(h)$ is a probability distribution over states conditioned on the history:
$$b(h) = \big(\mathbb{P}[S_t = s^1\mid H_t = h], \dots, \mathbb{P}[S_t = s^n\mid H_t = h]\big)$$

Both the history $H_t$ and the belief state $b(H_t)$ **satisfy the Markov property**, so a POMDP reduces to an (infinite) history tree or a belief tree.

**Average reward MDPs.** An **ergodic** Markov process is **recurrent** (each state visited infinitely often) and **aperiodic** (no systematic period), and has a limiting stationary distribution $d^\pi(s) = \sum_{s'} d^\pi(s')\mathcal{P}_{s's}$.

An MDP is ergodic if the chain induced by any policy is ergodic, giving an **average reward per time-step independent of the start state**:
$$\rho^\pi = \lim_{T\to\infty}\frac{1}{T}\mathbb{E}\left[\sum_{t=1}^{T} R_t\right]$$

with an average-reward Bellman equation $\tilde v_\pi(s) = \mathbb{E}_\pi[(R_{t+1}-\rho^\pi) + \tilde v_\pi(S_{t+1})\mid S_t = s]$.

## ✏️ Exercises

**1.** Verify the Bellman equation at Class 3 in the Student MRP ($\gamma=1$): $4.3 = -2 + 0.6\times10 + 0.4\times0.8$. Then explain what changes at $\gamma = 0$ and $\gamma = 0.9$.

> [!example]- Solution
> **The verification.** From Class 3, the immediate reward is $\mathcal{R}_{C3} = -2$. Transitions: **Pass with probability 0.6** (where $v = 10$) and **Pub with probability 0.4** (where $v = 0.8$).
> $$v(C3) = \mathcal{R}_{C3} + \gamma\sum_{s'}\mathcal{P}_{C3,s'}v(s') = -2 + 1\cdot(0.6 \times 10 + 0.4 \times 0.8) = -2 + 6 + 0.32 = 4.32 \approx 4.3\;\checkmark$$
>
> **The key point: this is a *self-consistency* condition, not a formula for computing $v$.** The equation relates $v(C3)$ to $v(\text{Pass})$ and $v(\text{Pub})$, but $v(\text{Pub})$ in turn depends on $v(C1), v(C2), v(C3)$ — including the value we started with. All seven equations must hold **simultaneously**, which is why the matrix solution $v = (I-\gamma\mathcal{P})^{-1}\mathcal{R}$ is needed rather than substitution.
>
> **At $\gamma = 0$:** every value collapses to its immediate reward, so $v(C3) = -2$. The agent is entirely myopic — the +10 for passing is invisible from one step away. Every state's value is just $\mathcal{R}_s$.
>
> **At $\gamma = 0.9$:** $v(C3) = 4.1$, slightly below the $\gamma=1$ value of 4.3, because the +10 reward arrives one step later and is worth $0.9\times10 = 9$.
>
> **Where $\gamma$ matters most is Facebook: −1 at $\gamma=0$, −7.6 at $\gamma=0.9$, −23 at $\gamma=1$.** The immediate cost of Facebook is only −1, but the 0.9 self-loop means the expected time spent there is $1/(1-0.9) = 10$ steps. A myopic agent sees a cheap distraction; a far-sighted one sees a trap. **This is exactly what discounting controls — how much of the future's structure the value function can see.**

**2.** Explain why fixing a policy turns an MDP into an MRP, and why that matters for the course structure.

> [!example]- Solution
> An MDP is *not yet* a random process — at each state there is a **choice**, and until the choice rule is specified the dynamics are undetermined. A policy supplies the rule.
>
> **The averaging:**
> $$\mathcal{P}^\pi_{s,s'} = \sum_a \pi(a\mid s)\mathcal{P}^a_{ss'} \qquad \mathcal{R}^\pi_s = \sum_a \pi(a\mid s)\mathcal{R}^a_s$$
> Marginalising out the action leaves transition and reward functions that depend on state alone — precisely the definition of an MRP $\langle\mathcal{S},\mathcal{P}^\pi,\mathcal{R}^\pi,\gamma\rangle$.
>
> **Why it matters structurally — three consequences:**
>
> **1. Policy evaluation is a solved problem.** Since $v_\pi$ is the value function of the induced MRP, it satisfies a **linear** Bellman equation with the closed-form solution $v_\pi = (I-\gamma\mathcal{P}^\pi)^{-1}\mathcal{R}^\pi$. **Prediction is easy** — as [[01 - Introduction to Reinforcement Learning]] promised.
>
> **2. Control is genuinely harder, and the reduction shows why.** The optimality equation contains $\max_a$, which does *not* correspond to any fixed policy's induced MRP — it changes which action is taken as the values change. That is what makes it **non-linear with no closed form**.
>
> **3. It licenses the whole algorithmic strategy of the course.** Because evaluation is tractable and improvement is easy given values, **control is solved by alternating them** — evaluate the current policy (an MRP problem), then improve it greedily, then re-evaluate the *new* induced MRP. That loop is **policy iteration** ([[03 - Planning by Dynamic Programming]]) and generalised policy iteration underlies Lectures 4–7 as well.
>
> The MP → MRP → MDP build is therefore not merely pedagogical: each layer's machinery is *reused* by the next.

**3.** The Bellman Expectation Equation is linear with a closed-form solution; the Bellman Optimality Equation is not. Explain precisely why, and what follows.

> [!example]- Solution
> **Expectation equation:**
> $$v_\pi(s) = \sum_a \pi(a\mid s)\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_\pi(s')\right)$$
> Every operation is a **weighted sum with fixed weights** — $\pi(a\mid s)$ and $\mathcal{P}^a_{ss'}$ are constants. So $v_\pi$ appears **linearly**, giving $v_\pi = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v_\pi$ and hence $v_\pi = (I-\gamma\mathcal{P}^\pi)^{-1}\mathcal{R}^\pi$.
>
> **Optimality equation:**
> $$v_*(s) = \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_*(s')\right)$$
> The $\max$ is **not a linear operator**: $\max(x+y) \ne \max(x) + \max(y)$ in general. It cannot be written as a matrix, so there is no $(I - \gamma\mathcal{P})^{-1}$ to invert.
>
> **Why the $\max$ is unavoidable.** It encodes the *choice* — the agent takes the best action, not an average over actions. Averaging (expectation) is linear; maximising is not. **Optimisation is what makes control hard**, and the non-linearity is its algebraic signature.
>
> **What follows — the whole rest of the course:**
> - **Iterative methods** rather than direct solution: **value iteration** applies the optimality backup repeatedly until convergence; **policy iteration** alternates linear evaluation with greedy improvement. Both are [[03 - Planning by Dynamic Programming]].
> - **Model-free methods** when $\mathcal{P}$ and $\mathcal{R}$ are unknown, so even the matrix cannot be written: **Q-learning** (which uses $\max_{a'}q(s',a')$, the sampled optimality backup) and **Sarsa** (which uses the actual next action, a sampled expectation backup) — [[05 - Model-Free Control]].
>
> **The Q-learning / Sarsa distinction is exactly the optimality-vs-expectation distinction**, sampled. Recognising that makes the two algorithms obvious rather than arbitrary.
>
> **A note on tractability:** even the linear solution is $O(n^3)$ and needs the full model, so it is only practical for small MRPs. Iterative methods are needed for scale regardless, and function approximation ([[06 - Value Function Approximation]]) for state spaces too large to enumerate.

**4.** Verify $6 = \max\{-2+8,\, -1+6\}$ at Class 1 in the Student MDP, and derive the optimal policy from $q_*$.

> [!example]- Solution
> At **Class 1** ($\gamma=1$) there are two actions:
> - **Study** — reward −2, leading deterministically to Class 2 where $v_* = 8$. So $q_*(C1,\text{Study}) = -2 + 8 = 6$.
> - **Facebook** — reward −1, leading to the Facebook state where $v_* = 6$. So $q_*(C1,\text{FB}) = -1 + 6 = 5$.
>
> $$v_*(C1) = \max\{6,\, 5\} = 6\;\checkmark$$
>
> **The optimal policy follows immediately** by $\pi_*(a\mid s) = 1$ iff $a = \arg\max_a q_*(s,a)$:
>
> | State | $q_*$ values | $\pi_*$ |
> |---|---|---|
> | Facebook | FB 5, **Quit 6** | **Quit** |
> | Class 1 | **Study 6**, FB 5 | **Study** |
> | Class 2 | **Study 8**, Sleep 0 | **Study** |
> | Class 3 | **Study 10**, Pub 8.4 | **Study** |
>
> The optimal student always studies, and quits Facebook immediately if distracted. Intuitive — but note it is *derived*, not assumed.
>
> **Two things worth extracting:**
>
> **Facebook is instructive.** Staying on Facebook costs only −1 immediately versus Quit's 0, so a myopic agent would stay. But staying returns to Facebook with probability 0.9, so $q_*(\text{FB},\text{FB}) = -1 + 6 = 5 < 6$. The one-step comparison already encodes the whole future — **that is what makes the Bellman equation powerful.**
>
> **Class 3 shows a near-tie:** Study gives 10, Pub gives 8.4. The Pub action is stochastic (0.2/0.4/0.4 back to C1/C2/C3) and its +1 reward does not compensate for the delay. A small change in the reward structure would flip the optimal action — which is the sensitivity that makes reward design consequential ([[01 - Introduction to Reinforcement Learning]]).
>
> **The general lesson:** knowing $q_*$ gives the optimal policy for free, with no search and no model. Knowing $v_*$ alone does **not** — you would need $\mathcal{P}$ and $\mathcal{R}$ to do a one-step lookahead. This is precisely why model-free control learns $q$ rather than $v$.

**5.** (Advanced) The theorem states there is always a **deterministic** optimal policy. Prove the intuition, and explain when stochastic policies are nonetheless necessary.

> [!example]- Solution
> **The intuition.** Fix $q_*$. For any state $s$, a stochastic policy achieves
> $$v_\pi(s) = \sum_a \pi(a\mid s)\, q_*(s,a)$$
> — a **convex combination** (weighted average) of the $q_*$ values. A weighted average can never exceed the maximum of the values being averaged:
> $$\sum_a \pi(a\mid s)q_*(s,a) \;\le\; \max_a q_*(s,a)$$
> with equality **iff all probability mass sits on maximising actions**. So putting probability 1 on $\arg\max_a q_*(s,a)$ is at least as good as any randomisation, in every state.
>
> Randomising can only help if you are uncertain *which* action is best — but $q_*$ resolves that uncertainty exactly. **Stochasticity buys nothing once you know the optimal values.**
>
> *(The full proof requires showing $v_*$ is well defined and that the greedy policy attains it — via the Bellman optimality operator being a contraction, which [[03 - Planning by Dynamic Programming]] establishes.)*
>
> **When stochastic policies are nonetheless necessary — four cases:**
>
> **1. Partial observability.** In a POMDP the agent's observation does not determine the state, so two genuinely different states can look identical. A deterministic policy must take the same action in both, and can get stuck; randomising escapes. **The theorem holds for MDPs only.**
>
> **2. Exploration.** During *learning* the agent does not know $q_*$, so it must randomise to discover it — $\epsilon$-greedy, softmax. The theorem is about the *final* policy, not the learning process. This is the exploration/exploitation tension of [[09 - Exploration and Exploitation]].
>
> **3. Adversarial and multi-agent settings.** In rock-paper-scissors a deterministic policy is exploitable; the Nash equilibrium is uniformly random. Such games are not MDPs — the environment is another optimising agent, so the stationarity assumption fails. See [[10 - Case Study - RL in Classic Games]].
>
> **4. Function approximation.** With approximated values, small parameter changes flip a greedy $\arg\max$ discontinuously, causing instability. Policy gradient methods parameterise $\pi$ directly and *smoothly*, which is one reason they exist despite this theorem — [[07 - Policy Gradient Methods]].
>
> **The practical significance:** because a deterministic optimal policy exists, we can search the finite space of deterministic policies rather than the infinite space of distributions, and a greedy improvement step is guaranteed not to lose. Both facts underpin policy iteration.

## 📝 Summary

- **MDPs formalise fully observable RL environments.** Bandits are one-state MDPs; POMDPs can be converted to MDPs over belief states.
- **Markov:** $\mathbb{P}[S_{t+1}\mid S_t] = \mathbb{P}[S_{t+1}\mid S_1,\dots,S_t]$ — the state is a sufficient statistic of the future.
- **Build order:** Markov Process $\langle\mathcal{S},\mathcal{P}\rangle$ → **+ rewards** = MRP $\langle\mathcal{S},\mathcal{P},\mathcal{R},\gamma\rangle$ → **+ actions** = MDP $\langle\mathcal{S},\mathcal{A},\mathcal{P},\mathcal{R},\gamma\rangle$.
- **Return $G_t = \sum_k \gamma^k R_{t+k+1}$ is a random variable; value $v(s) = \mathbb{E}[G_t\mid S_t=s]$ is its expectation.**
- **Discounting** avoids infinite returns in cyclic processes, and $\gamma$ controls myopic (→0) vs far-sighted (→1) evaluation.
- **Bellman equation:** value = immediate reward + discounted successor value. $v = \mathcal{R} + \gamma\mathcal{P}v$.
- **Fixing a policy reduces an MDP to an MRP** — which is why policy evaluation is linear and has a closed form $v_\pi = (I-\gamma\mathcal{P}^\pi)^{-1}\mathcal{R}^\pi$, at $O(n^3)$.
- **Two value functions:** $v_\pi(s)$ and $q_\pi(s,a)$, related by $v_\pi(s) = \sum_a\pi(a\mid s)q_\pi(s,a)$ and $q_\pi(s,a) = \mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_\pi(s')$.
- **An MDP is "solved" when $v_*$ is known.** There always exists a **deterministic** optimal policy, and knowing $q_*$ gives it immediately.
- **The Bellman Optimality Equation is non-linear** because of the $\max$ — no closed form, hence value iteration, policy iteration, Q-learning, and Sarsa.

## ⚠️ Important Notes

**$G_t$ is a random variable; $v(s)$ is its expectation.** Confusing the sampled return with the value function is the most common early error — the four sample episodes from $C1$ give four different returns.

**The Bellman equation is a consistency condition, not a computation.** All $n$ equations hold simultaneously and must be solved jointly; you cannot evaluate one state's value in isolation.

**$\gamma$ is part of the problem specification, not a tuning knob.** Changing it changes which policy is optimal — the Facebook trap is cheap at $\gamma=0$ and catastrophic at $\gamma=1$.

**Discounting is required when the process has cycles.** With $\gamma = 1$ and a self-loop, returns can be unbounded.

**Policies in an MDP depend only on the current state, and are stationary.** History-dependent or time-varying policies buy nothing — which is exactly what the Markov property guarantees.

**The $\max$ makes the optimality equation non-linear**, and that single fact generates every algorithm in the rest of the course.

**Q-learning uses $\max_{a'}$ (an optimality backup); Sarsa uses the actual $a'$ (an expectation backup).** The distinction mirrors the two Bellman equations exactly.

**Knowing $v_*$ does not give you the policy without a model.** You would need $\mathcal{P}$ and $\mathcal{R}$ to look ahead. **Knowing $q_*$ does** — hence model-free control learns $q$.

**The deterministic-optimal-policy theorem holds for MDPs only.** Partial observability, adversarial games, and the need to explore all require stochastic policies.

**Direct solution is $O(n^3)$ and requires the full model.** Practical only for small MRPs; everything real needs iteration and often function approximation.

**Rows of $\mathcal{P}$ sum to 1**; a matrix that fails this is not a valid transition model, and iterative methods will silently diverge.

> [!warning] Gaps in the source slides
> David Silver's slides extract exceptionally well — **all definitions, theorems, and equations survived**. The losses are diagrams only:
> - **Slides 7–9, 11, 16–18, 21, 25, 29, 35, 38–39, 42, 47** — the **Student Markov Chain / MRP / MDP state diagrams** are images. The transition probabilities, rewards, and value numbers all extracted (and are reproduced above), but **the graph structure — which state leads to which — is only partially recoverable** from the transition matrix on slide 9 and the worked examples. Consult the original PDF for the diagrams.
> - **Slides 20, 31–34, 43–46** — the **backup diagrams** (the small tree figures showing one-step lookahead) are images; the equations they illustrate all extracted.
> - **Slide 53** — the history tree / belief tree figure for POMDPs.
> - **Slide 13** truncates at *"It is sometimes possible to use undiscounted Markov reward"* — presumably "…processes, e.g. if all sequences terminate."
> - **Slide 51** truncates at *"$\mathcal{Z}$ is an observat…"* — the observation function definition $\mathcal{Z}^a_{s'o} = \mathbb{P}[O_{t+1}=o\mid S_{t+1}=s', A_t=a]$ is standard.
> - **Slide 53** truncates at *"A POMDP can be reduced to"* — the second reduction is to an (infinite) **belief state tree**.
> - **Slide 15** truncates mid-table on the fourth sample return.
>
> **Slides 49–56 are explicitly marked "no exam"** — infinite/continuous MDPs, POMDPs, and average-reward MDPs are background material.
>
> The lecture closes with Rich Sutton: *"The only stupid question is the one you were afraid to ask but never did."*

---
**Previous:** [[01 - Introduction to Reinforcement Learning]] · **Next:** [[03 - Planning by Dynamic Programming]]
