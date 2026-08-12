---
subject: Machine Learning
chapter: 08
tags: [ds, reinforcement-learning, model-based, dyna, mcts, tree-search]
source: "lecture-8-integrating-learning-and-planning.pdf — David Silver, UCL (Lecture 8 of 10)"
---

# Integrating Learning and Planning

> [!note] Where this sits in the course
> The third thing an agent can learn.
> - **Previous lectures:** learn the **value function** directly from experience
> - **Last lecture:** learn the **policy** directly from experience ([[07 - Policy Gradient Methods]])
> - **This lecture:** **learn the *model* directly from experience, and use planning** to construct a value function or policy — **integrating learning and planning into a single architecture**
>
> It closes the loop opened in [[01 - Introduction to Reinforcement Learning]], where learning and planning were presented as two separate problems.

## 📘 Main Knowledge

> **Model-Free RL** — no model; learn the value function (and/or policy) from experience.
> **Model-Based RL** — **learn a model from experience**, then **plan** the value function (and/or policy) from the model.

> **Advantages of Model-Based RL:**
> - **Can efficiently learn the model by supervised learning methods**
> - **Can reason about model uncertainty**
>
> **Disadvantages:**
> - **First learn a model, then construct a value function ⇒ two sources of approximation error**

**The efficiency argument is the important one.** A model is learned from *every* transition, densely and by ordinary supervised regression, whereas a value function learns only from the sparse reward signal. In many problems the dynamics are far easier to learn than the values.

---

## Part 1 — Model-Based RL

### What is a model?

> A model $\mathcal{M}$ is a representation of an MDP $\langle\mathcal{S},\mathcal{A},\mathcal{P},\mathcal{R}\rangle$ parametrised by $\eta$. **We assume $\mathcal{S}$ and $\mathcal{A}$ are known**, so $\mathcal{M} = \langle\mathcal{P}_\eta, \mathcal{R}_\eta\rangle$ represents transitions $\mathcal{P}_\eta \approx \mathcal{P}$ and rewards $\mathcal{R}_\eta \approx \mathcal{R}$:
> $$S_{t+1} \sim \mathcal{P}_\eta(S_{t+1}\mid S_t,A_t) \qquad R_{t+1} = \mathcal{R}_\eta(R_{t+1}\mid S_t,A_t)$$
> **Typically we assume conditional independence between state transitions and rewards.**

### Model learning is supervised learning

> **Goal:** estimate $\mathcal{M}_\eta$ from experience $\{S_1,A_1,R_2,\dots,S_T\}$. **This is a supervised learning problem:**
> $$S_1,A_1 \to R_2,S_2 \qquad S_2,A_2 \to R_3,S_3 \qquad \dots \qquad S_{T-1},A_{T-1}\to R_T,S_T$$
>
> - **Learning $s,a \to r$ is a regression problem**
> - **Learning $s,a \to s'$ is a density estimation problem**
> - **Pick a loss function** — mean-squared error, KL divergence, … — and find $\eta$ minimising it *(truncated)*

**This is the key structural insight of the lecture.** Model learning is genuinely i.i.d. supervised learning — the pathologies of [[01 - Introduction to Reinforcement Learning]] (delayed reward, credit assignment, non-stationarity) do not apply, because each transition is its own labelled example. All the machinery of [[Data Preparation and Visualization/contents/00-Index|supervised learning]] applies directly.

**Model families:** Table Lookup · Linear Expectation · Linear Gaussian · Gaussian Process · Deep Belief Network · …

### Table lookup model

The model is an explicit MDP, counting visits $N(s,a)$:
$$\hat{\mathcal{P}}^a_{s,s'} = \frac{1}{N(s,a)}\sum_{t=1}^{T}\mathbb{1}(S_t,A_t,S_{t+1} = s,a,s') \qquad \hat{\mathcal{R}}^a_s = \frac{1}{N(s,a)}\sum_{t=1}^{T}\mathbb{1}(S_t,A_t = s,a)R_t$$

> **Alternatively:** at each time-step record the tuple $\langle S_t,A_t,R_{t+1},S_{t+1}\rangle$; **to sample the model, randomly pick a tuple matching $\langle s,a,\cdot,\cdot\rangle$.**

The second form is a **non-parametric** model — it stores experience and replays it. Simple, exact on observed transitions, and the direct ancestor of experience replay in [[06 - Value Function Approximation]].

### Planning with a model

> Given $\mathcal{M}_\eta = \langle\mathcal{P}_\eta,\mathcal{R}_\eta\rangle$, **solve the MDP $\langle\mathcal{S},\mathcal{A},\mathcal{P}_\eta,\mathcal{R}_\eta\rangle$ using your favourite planning algorithm** — value iteration, policy iteration, tree search ([[03 - Planning by Dynamic Programming]]).

**Sample-based planning** — *"a simple but powerful approach"*:

> **Use the model only to generate samples.** Sample experience from the model:
> $$S_{t+1}\sim\mathcal{P}_\eta(S_{t+1}\mid S_t,A_t) \qquad R_{t+1} = \mathcal{R}_\eta(R_{t+1}\mid S_t,A_t)$$
> **Apply model-free RL to the samples** — Monte-Carlo control, Sarsa, Q-learning.
>
> **Sample-based planning methods are often more efficient.**

**Why sampling beats exact planning even with a perfect model:** DP's full-width backups cost $O(|\mathcal{S}|)$ per state and suffer the curse of dimensionality ([[03 - Planning by Dynamic Programming]]). Sampling costs $O(1)$ per backup and concentrates effort on states the model says are actually likely.

### The AB example revisited

The same 8 episodes from [[04 - Model-Free Prediction]]:
```
Real experience          Sampled experience
A, 0, B, 0               B, 1
B, 1                     B, 0
B, 1                     B, 1
B, 1                     A, 0, B, 1
B, 1                     B, 1
B, 1                     A, 0, B, 1
B, 1                     B, 1
B, 0                     B, 0
```
> e.g. Monte-Carlo learning on the **sampled** experience: **$V(A) = 1$, $V(B) = 0.75$.**

**This is a striking result.** Batch MC on the *real* data gave $V(A) = 0$; batch TD gave $0.75$ ([[04 - Model-Free Prediction]]). **MC applied to model-generated data gives $V(A) = 1$** — because the model says A→B always, and the sampled episodes from A happened to draw B's reward of 1 more often than not.

The lesson: **model-based sampling recovers the Markov inference that TD makes**, by construction — the model *is* the maximum-likelihood MDP. The value depends on which episodes were sampled, so with more samples it converges toward $0.75$.

### Inaccurate models

> Given an imperfect model $\langle\mathcal{P}_\eta,\mathcal{R}_\eta\rangle \ne \langle\mathcal{P},\mathcal{R}\rangle$, **performance of model-based RL is limited to the optimal policy for the approximate MDP.** i.e. **model-based RL is only as good as the estimated model.** When the model is inaccurate, planning computes a **suboptimal policy**.
>
> **Solution 1: when the model is wrong, use mo** *(truncated — "model-free RL")*
> *(Solution 2, standard: reason explicitly about model uncertainty)*

---

## Part 2 — Integrated Architectures: Dyna

> **Two sources of experience:**
> - **Real experience** — sampled from the environment (the **true** MDP): $S'\sim\mathcal{P}^a_{s,s'}$, $R = \mathcal{R}^a_s$
> - **Simulated experience** — sampled from the model (the **approximate** MDP): $S'\sim\mathcal{P}_\eta(S'\mid S,A)$, $R = \mathcal{R}_\eta(R\mid S,A)$

| Architecture | What it does |
|---|---|
| **Model-Free RL** | No model. Learn value function (and/or policy) from **real** experience |
| **Model-Based RL** (sample-based planning) | Learn a model from **real** experience. Plan value function from **simulated** experience |
| **Dyna** | Learn a model from real experience. **Learn *and* plan the value function from *both* real and simulated experience** |

**Dyna's insight is that the two are the same operation.** Both real and simulated transitions are $\langle s,a,r,s'\rangle$ tuples, and the same learning rule consumes either — so there is no reason to choose.

**Dyna-Q** interleaves: take a real action, update $Q$ from it, update the model from it, then perform $n$ planning steps by sampling remembered $\langle s,a\rangle$ pairs from the model and applying the same Q-learning update. **The value of $n$ trades real experience against computation.**

**Dyna-Q on a Simple Maze** shows the payoff: with $n=50$ planning steps the maze is solved in a handful of real episodes, versus dozens for $n=0$ (plain Q-learning).

**Dyna-Q with an inaccurate model** — two scenarios:
- **"The changed environment is harder"** — a previously open path is blocked. The agent's model is now wrong and optimistic; it takes time to unlearn, but it does recover.
- **"The changed environment is easier"** — a new shortcut opens. **This is the harder case**: the agent has no reason to revisit the region, so it may never discover the improvement. **Dyna-Q+** addresses it by adding an exploration bonus for state-action pairs not tried recently.

---

## Part 3 — Simulation-Based Search

> **Forward search** algorithms select the best action by **lookahead**, building a search tree with the **current state $s_t$ at the root**, using a model of the MDP to look ahead.
>
> **No need to solve the whole MDP — just the sub-MDP starting from now.**

**That is the central idea of the whole section.** [[03 - Planning by Dynamic Programming]] computed $v_*$ for *every* state. But an agent only needs to act *here*, and most of the state space is irrelevant to the current decision.

> **Simulation-based search** = the forward search paradigm using **sample-based planning**: simulate episodes of experience from now with the model, and **apply model-free RL to the simulated episodes**:
> $$\{s^k_t, A^k_t, R^k_{t+1}, \dots, S^k_T\}_{k=1}^{K} \sim \mathcal{M}_\nu$$
>
> - **Monte-Carlo control → Monte-Carlo search**
> - **Sarsa → TD search**

### Simple Monte-Carlo search

Given a model $\mathcal{M}_\nu$ and simulation policy $\pi$, **for each action $a$**, simulate $K$ episodes from the current real state:
$$Q(s_t,a) = \frac{1}{K}\sum_{k=1}^{K}G_t \;\overset{P}{\to}\; q_\pi(s_t,a) \qquad a_t = \arg\max_{a\in\mathcal{A}}Q(s_t,a)$$

**Its weakness is that $\pi$ never improves** — every simulation uses the same fixed policy, so the evaluation is of $q_\pi$, not $q_*$.

### Monte-Carlo Tree Search (MCTS)

**Evaluation:** simulate $K$ episodes from $s_t$ using the current simulation policy, **build a search tree containing visited states and actions**, and evaluate by mean return:
$$Q(s,a) = \frac{1}{N(s,a)}\sum_{k=1}^{K}\sum_{u=t}^{T}\mathbb{1}(S_u,A_u = s,a)G_u \;\overset{P}{\to}\; q_\pi(s,a)$$

**Simulation — the crucial difference from simple MC search:**

> **In MCTS, the simulation policy $\pi$ improves.** Each simulation has **two phases**:
> - **Tree policy (improves):** pick actions to maximise $Q(S,A)$
> - **Default policy (fixed):** pick actions randomly
>
> **Repeat for each simulation:** evaluate states $Q(S,A)$ by Monte-Carlo evaluation, then **improve the tree policy**, e.g. by $\epsilon$-greedy *(truncated)*

**MCTS is GPI applied to the sub-MDP from now.** Inside the tree, where statistics exist, it acts greedily and improves; beyond the tree, where it knows nothing, it plays randomly to termination. The tree grows toward promising lines — a **highly selective best-first search**.

> **Advantages of MC Tree Search:**
> - **Highly selective best-first search**
> - **Evaluates states dynamically** (unlike e.g. DP)
> - **Uses sampling to break the curse of dimensionality**
> - **Works for "black-box" models** (only requires samples)
> - **Computationally efficient, anytime, parallelisable**

**"Anytime"** matters practically: you can stop after any number of simulations and take the best action found so far, so the algorithm adapts to whatever time budget it is given.

### Case study: the Game of Go

> The ancient oriental game of Go is **2500 years old**, considered **the hardest classic board game** and **a grand challenge task for AI (John McCarthy)**. **Traditional game-tree search has failed in Go.**

**Rules:** usually 19×19 (also 13×13, 9×9) · simple rules, complex strategy · black and white place stones alternately · surrounded stones are captured and removed · **the player with more territory wins**.

**Position evaluation** — the reward is undiscounted and terminal only:
$$R_t = 0 \text{ for all } t < T \qquad R_T = \begin{cases}1 & \text{if Black wins}\\ 0 & \text{if White wins}\end{cases}$$
Policy $\pi = \langle\pi_B,\pi_W\rangle$ selects moves for **both** players, so:
$$v_\pi(s) = \mathbb{E}_\pi[R_T\mid S=s] = \mathbb{P}[\text{Black wins}\mid S=s] \qquad v_*(s) = \max_{\pi_B}\min_{\pi_W}v_\pi(s)$$

**The value function is literally a win probability**, and $v_*$ is a **minimax** value — the two-player structure enters through the $\max\min$.

**Monte-Carlo evaluation in Go:** from the current position, run simulations to the end and count wins. The slide's example: outcomes 1, 1, 0, 0 → $V(s) = 2/4 = 0.5$.

**Why this works where traditional search failed:** Go has a branching factor around 250 and no reliable hand-crafted evaluation function. MCTS needs **neither** — it replaces the evaluation function with random rollouts to termination, and replaces exhaustive search with selective sampling.

The **computer Go progress chart** (2006–2011) shows MoGo, CrazyStone, Fuego, Zen, Erica climbing from ~10 kyu to ~1 kyu — a transformation driven entirely by MCTS.

### Temporal-Difference search

> **Simulation-based search using TD instead of MC (bootstrapping).**
> - **MC tree search applies MC control to the sub-MDP from now**
> - **TD search applies Sarsa to the sub-MDP from now**

> For **model-free RL**, bootstrapping is helpful — TD reduces variance but increases bias, is usually more efficient, and TD(λ) can be much more efficient than MC.
> **For simulation-based search, bootstrapping is also helpful** — TD search reduces variance but increases bias, and **is usually more efficient** *(truncated)*.

**TD search:** simulate episodes from the current real state $s_t$; estimate $Q(s,a)$; **for each step of simulation update by Sarsa**, $\Delta Q(S,A) = \alpha(R + \gamma Q(S',A') - Q(S,A))$; select actions $\epsilon$-greedily. **May also use function approximation for $Q$** — which is what lets it generalise across positions rather than treating each tree node independently.

### Dyna-2

> **The agent stores two sets of feature weights:**
> - **Long-term memory** — updated from **real** experience using **TD learning**. *General domain knowledge that applies to any episode.*
> - **Short-term (working) memory** — updated from **simulated** experience using **TD search**. *Specific local knowledge about the current situation.*

An elegant separation: what is true in general versus what matters here and now. The agent adds them to select actions, so search refines general knowledge locally without corrupting it.

## ✏️ Exercises

**1.** Explain why model learning is a supervised learning problem, and why that is an advantage.

> [!example]- Solution
> **The reduction.** Experience $\{S_1,A_1,R_2,S_2,\dots\}$ decomposes into input-output pairs:
> $$\underbrace{(S_t,A_t)}_{\text{input}} \to \underbrace{(R_{t+1},S_{t+1})}_{\text{output}}$$
> - $s,a \to r$ is **regression** (predict a scalar)
> - $s,a \to s'$ is **density estimation** (predict a distribution)
>
> Standard losses apply — MSE for the reward, KL divergence for the transition distribution — and any function approximator can be used: linear, Gaussian process, neural network.
>
> **Why this is a genuine advantage — three reasons:**
>
> **1. The RL pathologies disappear.** [[01 - Introduction to Reinforcement Learning]] listed four things that make RL hard: no supervisor, delayed feedback, non-i.i.d. data, and actions affecting future data. **Model learning has a supervisor** — the next state *is* the label, available immediately. There is **no credit assignment problem**: the transition $(s,a)\to s'$ is complete in itself. The data is still collected non-i.i.d., but each *example* is a self-contained supervised pair.
>
> **2. Every transition is informative.** A value function learns only from reward, which in Go is a single bit at the end of a 200-move game. A model learns something from **every single transition** — the reward signal's sparsity is irrelevant to it. This is why the lecture says the model can be learned **efficiently**.
>
> **3. Decades of supervised learning transfer directly.** Regularisation, cross-validation, architecture search, uncertainty estimation — all applicable, which is not true of value learning where the target is bootstrapped and moving.
>
> **The catch is the stated disadvantage: "two sources of approximation error."** The model is approximate, and the value function planned from it is approximate, so errors compound. Worse, planning **amplifies** model error — the planner will actively seek out states where the model is optimistically wrong, because those look best. That is exactly the inaccurate-model problem, and it is why Dyna keeps learning from real experience too.

**2.** Explain the AB example result: why does model-based sampling give $V(A) = 1$ when batch MC gave $0$ and batch TD gave $0.75$?

> [!example]- Solution
> **Three methods, three answers, on identical data.**
>
> **Batch MC on real experience: $V(A) = 0$.** A was visited once, in episode 1, and the return from A was $0 + 0 = 0$. MC reports the mean of observed returns from A — one sample of 0. It minimises MSE on what was actually seen ([[04 - Model-Free Prediction]]).
>
> **Batch TD on real experience: $V(A) = 0.75$.** TD builds the maximum-likelihood MDP: A→B with probability 1, and $V(B) = 6/8 = 0.75$, so $V(A) = 0 + 0.75$.
>
> **Model-based sampling: $V(A) = 1$ in this instance.** The table-lookup model is *the same* maximum-likelihood MDP that TD converges to — A→B always, B gives reward 1 with probability 6/8. So sampling from it produces episodes like `A, 0, B, 1`. In the sampled batch shown, **both** episodes visiting A drew $B$'s reward of 1, giving $V(A) = 1$.
>
> **The crucial point: the difference between 1 and 0.75 is sampling noise, not a different method.** The model-based estimate is an MC estimate *of the model's* value function, and the model's true $V(A)$ is 0.75. With more sampled episodes it converges to 0.75 — **the same answer as TD**.
>
> **This is the deep connection the example is making.** Batch TD's answer *is* the answer you get by planning with the maximum-likelihood model. TD's Markov inference and model-based planning are two routes to the same place: TD reaches it implicitly through bootstrapping, model-based RL reaches it explicitly by building the MDP and solving it.
>
> **Why bother with the model, then?** Because you can generate **unlimited** simulated experience from it. TD extracts its answer from 8 episodes and stops; the model can produce 8 million, letting a model-free algorithm converge far past what the real data alone supports. **That is Dyna's entire premise** — and the reason Dyna-Q solves the maze in a fraction of the real episodes plain Q-learning needs.

**3.** Explain Dyna and why the "changed environment is easier" case is harder than "harder".

> [!example]- Solution
> **Dyna interleaves three operations** on every real step:
> 1. Act in the real environment, observe $\langle s,a,r,s'\rangle$
> 2. **Direct RL** — update $Q$ from the real transition
> 3. **Model learning** — update the model from the real transition
> 4. **Planning** — repeat $n$ times: sample a previously-seen $\langle s,a\rangle$, query the model for $\langle r,s'\rangle$, and apply **the same Q-learning update**
>
> **The unification is the point:** steps 2 and 4 use an identical update rule; only the source of the transition differs. Real and simulated experience are interchangeable inputs to one learner. $n$ controls how much computation is spent per unit of real experience — and since real experience is usually the scarce resource, large $n$ is a huge win.
>
> **The two inaccurate-model scenarios:**
>
> **"Harder" — a path is blocked.** The model still believes the old path works, so planning keeps recommending it. But **the agent tries it, in reality, and fails** — receiving a real transition that contradicts the model. The model is corrected, and planning follows. **Recovery is automatic**, because the agent's own optimism drives it to the place where the error is exposed. There is a transient period of poor performance, then it adapts.
>
> **"Easier" — a shortcut opens.** The model has no record of the new path and predicts nothing about it. Planning therefore never recommends going there, so **the agent never visits it, so it never learns the shortcut exists.** The agent settles on its old, now-suboptimal route and stays there indefinitely.
>
> **The asymmetry is systematic:** an over-optimistic model is **self-correcting** (it sends you to be disappointed); a **pessimistic or ignorant** model is **self-reinforcing** (it keeps you away from the evidence). This is a form of the feedback-loop trap noted in [[MLOps/contents/09 - CI-CD with GitHub Actions|CI/CD]] — a system that shapes the data it later learns from.
>
> **Dyna-Q+ is the standard fix:** add an exploration bonus $\kappa\sqrt{\tau}$ to the modelled reward, where $\tau$ is the time since $(s,a)$ was last tried. Long-unvisited actions become increasingly attractive, so the agent periodically re-checks its assumptions. This is [[09 - Exploration and Exploitation]]'s optimism-under-uncertainty principle applied to a model rather than to values.

**4.** Explain MCTS and why it succeeded in Go where traditional game-tree search failed.

> [!example]- Solution
> **MCTS in four repeated steps**, per simulation:
> - **Selection** — from the root, follow the **tree policy**, picking actions to maximise $Q(S,A)$ while inside the tree
> - **Expansion** — on leaving the tree, add a new node
> - **Simulation (rollout)** — follow the fixed **default policy** (random) to termination
> - **Backup** — propagate the outcome, updating $Q(s,a)$ as the mean return through each visited node
>
> **The two policies are the design.** The tree policy **improves** as statistics accumulate — it is GPI applied to the sub-MDP from now. The default policy is fixed and cheap, providing an evaluation where no statistics exist yet.
>
> **Why traditional search failed in Go — two blockers:**
>
> **1. Branching factor.** Chess has ~35 legal moves; Go has ~250. Alpha-beta search to depth $d$ costs $b^d$, so a depth that is routine in chess is impossible in Go.
>
> **2. No evaluation function.** Alpha-beta needs a heuristic to score non-terminal positions. Chess has an obvious one — count material. **Go has nothing comparable**: stones are never captured in most positions, territory is implicit and contested, and decades of effort produced no reliable static evaluator. This is the deeper problem, and it is why the lecture says *"traditional game-tree search has failed in Go."*
>
> **How MCTS removes both:**
>
> **It replaces the evaluation function with random rollouts.** Rather than judging a position statically, play it out to the end — where the rules give an unambiguous winner. $v_\pi(s) = \mathbb{P}[\text{Black wins}\mid S=s]$ is estimated by counting: 1,1,0,0 → 0.5. **No domain knowledge required.** This is why it *"works for black-box models — only requires samples."*
>
> **It replaces exhaustive search with selective sampling.** Alpha-beta expands the tree uniformly to a fixed depth; MCTS is *"highly selective best-first"*, spending simulations where $Q$ is promising. Sampling *"breaks the curse of dimensionality"* — the branching factor no longer sets the cost, the simulation budget does.
>
> **Two further practical advantages the lecture lists:** it is **anytime** (stop whenever and take the best move found), and **parallelisable** (simulations are independent).
>
> **The historical evidence** is the 2006–2011 progress chart: MoGo, CrazyStone, Fuego, Zen and Erica climbing from ~10 kyu to ~1 kyu after decades of stagnation. **A single algorithmic idea moved the field roughly nine ranks.** AlphaGo later added learned policy and value networks in place of random rollouts — but the MCTS skeleton is the one described here.

**5.** (Advanced) Compare Dyna, MCTS, and TD search. What does Dyna-2 combine, and why?

> [!example]- Solution
> | | **Dyna** | **MCTS / TD search** |
> |---|---|---|
> | Scope | **Global** — improves $Q$ everywhere | **Local** — solves the sub-MDP from $s_t$ |
> | When | Between real steps, continuously | Before each action, from scratch |
> | Persists? | Yes — knowledge accumulates | **No** — the tree is usually discarded |
> | Samples from | Remembered $\langle s,a\rangle$ pairs | The **current state** forward |
> | Backup | Q-learning (MCTS: MC; TD search: Sarsa) | |
>
> **The key difference is *where* the simulations start.** Dyna samples from anywhere it has been, improving a global value function. Simulation-based search always starts **from now**, concentrating every simulation on the decision at hand — *"no need to solve the whole MDP, just the sub-MDP starting from now."*
>
> **MCTS vs TD search** is exactly the MC-vs-TD distinction of [[04 - Model-Free Prediction]], transplanted into the search: *"MC tree search applies MC control to the sub-MDP from now; TD search applies Sarsa."* The trade-off is identical — TD **reduces variance, increases bias, and is usually more efficient** — and the lecture states explicitly that this holds for search just as it does for learning.
>
> TD search has a further advantage MCTS lacks: **it can use function approximation for $Q$**, so information generalises across similar positions rather than being tied to individual tree nodes. A tabular tree learns nothing about a position it has not visited; an approximator does.
>
> **Dyna-2 combines the global and local views** with **two sets of feature weights**:
> - **Long-term memory** — updated from **real** experience by TD learning. *"General domain knowledge that applies to any episode."*
> - **Short-term (working) memory** — updated from **simulated** experience by TD search. *"Specific local knowledge about the current situation."*
>
> **Why the separation is necessary.** If search results were written into the long-term weights, then knowledge specific to *this* position — which is often sharply local and sometimes based on an inaccurate model — would corrupt general knowledge that took much more experience to acquire. Keeping them separate lets search **refine** the general estimate locally, and then **discard** the refinement when the situation changes.
>
> The value used for acting is the sum of both, so the agent benefits from everything it has ever learned *plus* everything it has just computed about this position. **It is the same idea as a prior plus a local update** — and it is the architecture that produced the strongest TD-search results in Go.

## 📝 Summary

- **Model-based RL learns a model from experience, then plans with it** — a third thing to learn, alongside value functions and policies.
- **Model learning is supervised learning:** $s,a \to r$ is regression, $s,a \to s'$ is density estimation. Every transition is informative, unlike sparse rewards.
- **Its cost is two sources of approximation error**, and planning tends to **amplify** model error by seeking out optimistically-wrong states.
- **Table lookup models** count transitions, or simply store and replay tuples.
- **Sample-based planning** uses the model only to generate samples, then applies model-free RL — often more efficient than exact planning.
- **Model-based sampling recovers batch TD's answer** on the AB example, because the table-lookup model *is* the maximum-likelihood MDP.
- **Model-based RL is only as good as the model.** When the model is wrong, fall back to model-free RL or reason about uncertainty.
- **Dyna learns and plans from both real and simulated experience** using the same update rule; $n$ planning steps per real step trades computation for real experience.
- **An "easier" changed environment is harder than a "harder" one** — an ignorant model is self-reinforcing, an optimistic one is self-correcting.
- **Simulation-based search solves only the sub-MDP from now**, building a tree rooted at the current state.
- **MCTS** improves its **tree policy** while keeping a fixed random **default policy** — highly selective, dynamic, sampling-based, black-box compatible, anytime, parallelisable.
- **MCTS transformed computer Go** by replacing the missing evaluation function with random rollouts and exhaustive search with selective sampling.
- **TD search** applies Sarsa instead of MC to the sub-MDP; **Dyna-2** keeps a long-term memory from real experience and a short-term memory from search.

## ⚠️ Important Notes

**Model-based RL has two error sources, and planning amplifies the second.** A planner actively searches for states where the model is optimistically wrong, because those look best — so model error is not merely additive.

**"Model-based RL is only as good as the estimated model."** Performance is capped by the optimal policy *of the approximate MDP*, not of the real one.

**An ignorant model is more dangerous than a wrong one.** If the model predicts nothing about a region, planning never sends the agent there, and the error is never corrected. Dyna-Q+'s exploration bonus exists for this.

**Model learning escapes RL's usual difficulties** — supervised targets, no credit assignment, dense signal — which is why it can be far more sample-efficient than value learning.

**Sample-based planning is often better than exact planning even with a perfect model**, because full-width backups suffer the curse of dimensionality while sampling costs $O(1)$.

**In Dyna, real and simulated transitions use the identical update rule.** The only difference is provenance, which is why the architecture is so simple.

**Simulation-based search does not need to solve the whole MDP** — only the sub-MDP from the current state. Most of the state space is irrelevant to the decision at hand.

**MCTS's two policies play different roles.** The tree policy improves (it is GPI); the default policy is fixed and exists only to provide a cheap terminal evaluation.

**MCTS needs no evaluation function**, which is precisely why it succeeded in Go where alpha-beta failed. Rollouts to termination replace domain knowledge.

**MCTS is anytime and parallelisable** — stop after any budget and take the best move; simulations are independent.

**TD search trades variance for bias inside the search**, exactly as TD does inside learning — and it can use function approximation, which tabular MCTS cannot.

**Dyna-2 separates long- and short-term memory** so that position-specific search results do not corrupt hard-won general knowledge.

> [!warning] Gaps in the source slides
> Silver's slides extract well, **but this lecture is unusually figure-heavy and several algorithm listings are lost:**
> - **⚠️ Slide 27 — the Dyna-Q algorithm pseudocode is entirely an image.** The interleaving of direct RL, model learning, and $n$ planning steps is described in the surrounding text but **the actual algorithm is not recoverable**. See Sutton & Barto Ch. 8.
> - **Slides 10, 26 — "Model-Based RL" and the "Dyna Architecture" diagrams are images.** Slide 10 is title-only.
> - **Slides 28–30** — **Dyna-Q on a Simple Maze** and both **inaccurate-model** experiments are images; only the captions *"the changed environment is harder"* / *"easier"* extracted. **The learning curves showing the effect of $n$ are lost.**
> - **Slides 42–46 — "Applying Monte-Carlo Tree Search (1)–(5)" are five consecutive image-only slides.** This is the step-by-step walkthrough of how the tree grows, and **none of it is captured** — the single most costly gap in the lecture.
> - **Slides 7–8** — the model-free and model-based agent diagrams.
> - **Slides 32–33** — the search tree figures.
> - **Slide 41** — the Go Monte-Carlo evaluation figure; the outcomes (1,1,0,0 → 0.5) extracted.
> - **Slide 48** — the computer Go progress chart; program names and kyu rankings extracted but not the plot.
> - **Slide 53 — "Results of TD search in Go"** is title-only.
> - **Truncations:** slide 12 (cut at $\mathbb{P}[S_{t+1}$), slide 13 (cut at *"find parameters $\eta$ that mini"*), slide 20 (**cut at *"Solution 1: when model is wrong, use mo"*** — "model-free RL"; **Solution 2 is entirely missing**), slides 23–25 (Dyna definition cut at *"real and simulated exp"*, repeated three times as overlay duplicates), slide 35 (cut at $\arg\max_a Q(s$), slide 36 (cut at $q$), slide 37 (cut at *"$\epsilon$-greedy("*), slide 50 (cut at *"TD search is usually more efficient"*).
> - **Slides 5/6, 23/24/25 are overlay duplicates.**
>
> **References:** Dyna is Sutton (1990); Dyna-2 is Silver, Sutton & Müller (2008). The Go material anticipates AlphaGo (Silver et al., Nature 2016), which replaced random rollouts with learned policy and value networks.

---
**Previous:** [[07 - Policy Gradient Methods]] · **Next:** [[09 - Exploration and Exploitation]]
