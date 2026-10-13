---
subject: Machine Learning
chapter: 08
tags: [ds, reinforcement-learning, model-based, dyna, mcts, tree-search]
source: "lecture-8-integrating-learning-and-planning.pdf — David Silver, UCL (Lecture 8 of 10)"
---

# Integrating Learning and Planning

Earlier lectures learned a value function or a policy from experience. This one learns a **model** from experience and plans with it, combining learning and planning (separate problems in [[01 - Introduction to Reinforcement Learning]]) in one architecture.

## 📘 Main Knowledge

**Model-free RL** learns a value function and/or policy from experience. **Model-based RL** learns a model from experience, then plans a value function and/or policy from it. Advantages: the model can be learned efficiently by supervised learning (every transition is a labelled example, unlike sparse rewards), and the agent can reason about model uncertainty. Disadvantage: two sources of approximation error (model, then value function).

### Models

A model $\mathcal M_\eta=\langle\mathcal P_\eta,\mathcal R_\eta\rangle$ represents an MDP with known $\mathcal S,\mathcal A$: $S_{t+1}\sim\mathcal P_\eta(S_{t+1}\mid S_t,A_t)$, $R_{t+1}=\mathcal R_\eta(R_{t+1}\mid S_t,A_t)$, usually assuming transitions and rewards are conditionally independent.

**Model learning is supervised learning**: from $S_1,A_1\to R_2,S_2$; $S_2,A_2\to R_3,S_3$; … learning $s,a\to r$ is regression and $s,a\to s'$ is density estimation. Choose a loss (MSE, KL divergence) and minimize it. Model families: table lookup, linear expectation, linear Gaussian, Gaussian process, deep belief network, …

**Table lookup**: count visits,
$$\hat{\mathcal P}^a_{ss'}=\frac1{N(s,a)}\sum_t\mathbb 1(S_t,A_t,S_{t+1}=s,a,s'),\qquad\hat{\mathcal R}^a_s=\frac1{N(s,a)}\sum_t\mathbb 1(S_t,A_t=s,a)R_t,$$
or store every tuple $\langle S_t,A_t,R_{t+1},S_{t+1}\rangle$ and, to sample, pick a stored tuple matching $\langle s,a,\cdot,\cdot\rangle$ (a non-parametric model, like experience replay).

### Planning with a model

Solve the MDP $\langle\mathcal S,\mathcal A,\mathcal P_\eta,\mathcal R_\eta\rangle$ with value iteration, policy iteration or tree search ([[03 - Planning by Dynamic Programming]]). **Sample-based planning**, simple and powerful: use the model only to generate samples and apply model-free RL (MC control, Sarsa, Q-learning) to them. It is often more efficient: backups cost $O(1)$ and focus on likely states.

**AB example revisited** (data from [[04 - Model-Free Prediction]]). Real: `A,0,B,0`; six times `B,1`; `B,0`. Sampled from the table model: `B,1`; `B,0`; `B,1`; `A,0,B,1`; `B,1`; `A,0,B,1`; `B,1`; `B,0`. MC on the sampled data gives $V(A)=1$, $V(B)=0.75$. The model is the maximum-likelihood MDP, whose true $V(A)$ is 0.75 (batch TD's answer); with more samples the estimate approaches it.

**Inaccurate models**: performance is limited to the optimal policy of the approximate MDP; planning on a wrong model gives a suboptimal policy. Solution 1: when the model is wrong, use model-free RL. (Solution 2 is cut off; the standard answer is to reason explicitly about model uncertainty.)

### Dyna

Two sources of experience: **real** (from the true MDP) and **simulated** (from the model).

| Architecture | Learns |
|---|---|
| model-free RL | value function / policy from real experience |
| model-based RL (sample-based planning) | a model from real experience; plans from simulated experience |
| **Dyna** | a model from real experience; learns **and** plans the value function from both |

Real and simulated transitions are both $\langle s,a,r,s'\rangle$ tuples, consumed by the same update.

**Dyna-Q**: take a real step; update $Q$ (Q-learning) and the model from it; then $n$ times, sample a previously seen $(s,a)$, query the model, and apply the same Q-learning update. $n$ trades computation for real experience. On a simple maze, $n=50$ learns in a few episodes where $n=0$ (plain Q-learning) needs dozens.

With an inaccurate model: if the environment becomes **harder** (a path is blocked), the agent tries the old path, fails, and corrects its model. If it becomes **easier** (a shortcut opens), the model never predicts it, the agent never goes there, and it may never find it. **Dyna-Q+** adds an exploration bonus (in Sutton & Barto, $\kappa\sqrt\tau$ for time τ since the pair was tried).

### Simulation-based search

**Forward search** builds a tree rooted at the current state $s_t$ and looks ahead with the model. There is no need to solve the whole MDP, only the sub-MDP starting now. **Simulation-based search** simulates episodes from now with the model, $\{s_t^k,A^k_t,R^k_{t+1},\dots,S^k_T\}_{k=1}^K\sim\mathcal M_\nu$, and applies model-free RL: MC control gives MC search, Sarsa gives TD search.

**Simple MC search**: for each action $a$, simulate $K$ episodes from $s_t$ with a fixed policy π; $Q(s_t,a)=\frac1K\sum_kG_t\to q_\pi(s_t,a)$; take $\arg\max_aQ(s_t,a)$. The simulation policy never improves.

**Monte Carlo tree search**: simulate $K$ episodes from $s_t$, build a tree of the visited states and actions, and evaluate each node by its mean return,
$$Q(s,a)=\frac1{N(s,a)}\sum_{k=1}^K\sum_{u=t}^T\mathbb 1(S_u,A_u=s,a)G_u.$$
Each simulation has a **tree policy**, which improves (maximize $Q$, e.g. ε-greedy), and a **default policy** beyond the tree, which is fixed (random rollouts). So MCTS is policy iteration on the sub-MDP from now.

Advantages: highly selective best-first search; evaluates states dynamically (unlike DP); sampling breaks the curse of dimensionality; works for black-box models (needs only samples); efficient, anytime and parallelizable.

### Case study: Go

Go is 2,500 years old, considered the hardest classic board game and a grand challenge for AI (John McCarthy); traditional game-tree search failed. Usually 19×19 (also 13×13, 9×9); players alternate placing stones; surrounded stones are captured; more territory wins.

Reward is terminal only: $R_T=1$ if Black wins, 0 if White wins. With $\pi=\langle\pi_B,\pi_W\rangle$,
$$v_\pi(s)=\mathbb E_\pi[R_T\mid S=s]=\mathbb P[\text{Black wins}\mid S=s],\qquad v_*(s)=\max_{\pi_B}\min_{\pi_W}v_\pi(s).$$
MC evaluation plays simulations to the end and counts wins (1, 1, 0, 0 → $V(s)=0.5$). Programs using MCTS (MoGo, CrazyStone, Fuego, Zen, Erica) climbed from about 10 kyu to about 1 kyu between 2006 and 2011.

### TD search and Dyna-2

**TD search** applies Sarsa to the sub-MDP from now: simulate from $s_t$, update every simulated step with $\Delta Q(S,A)=\alpha(R+\gamma Q(S',A')-Q(S,A))$, act ε-greedily; $Q$ may use function approximation, so it generalizes across positions. As in learning, bootstrapping in search reduces variance, increases bias, and is usually more efficient.

**Dyna-2** keeps two sets of feature weights: **long-term memory**, updated from real experience by TD learning (general knowledge for any episode), and **short-term (working) memory**, updated from simulated experience by TD search (knowledge of the current situation). Actions use their sum.

## ✏️ Exercises

**1.** Why is model learning a supervised problem, and why is that an advantage?

> [!example]- Solution
> Experience splits into pairs $(S_t,A_t)\to(R_{t+1},S_{t+1})$: regression for the reward, density estimation for the next state, with ordinary losses and any approximator. The label arrives immediately with no credit assignment, every transition teaches something (a Go value function gets one bit per game), and standard supervised tools (regularization, validation) apply.
> The cost is two layers of approximation, and planning amplifies model error: the planner seeks states where the model is optimistically wrong because they look best. Hence Dyna keeps learning from real experience too.

**2.** In the AB example, why does model-based sampling give $V(A)=1$ when batch MC gave 0 and batch TD 0.75?

> [!example]- Solution
> Batch MC averages the single observed return from A: 0. Batch TD solves the maximum-likelihood MDP: A → B always, $V(B)=0.75$, so $V(A)=0.75$. The table model is that same MDP; both sampled episodes from A happened to draw reward 1 from B, so MC on the samples gives 1. That is sampling noise around the model's true value 0.75, TD's answer. TD reaches the maximum-likelihood answer implicitly; model-based RL builds the MDP explicitly. The model's advantage is that it can generate unlimited simulated experience, which is Dyna's premise.

**3.** Explain Dyna, and why an environment that becomes easier is harder to adapt to than one that becomes harder.

> [!example]- Solution
> Each real step: act and observe; update $Q$ from the real transition; update the model; then $n$ planning updates with the same rule on simulated transitions. Large $n$ saves scarce real experience.
> Blocked path: the model is optimistic, so the agent goes there, fails for real, and corrects the model; recovery is automatic. New shortcut: the model knows nothing about it, planning never sends the agent there, so it never learns. An optimistic error corrects itself; an unexplored region stays unexplored. Dyna-Q+ makes long-untried actions attractive so the agent rechecks them, optimism under uncertainty ([[09 - Exploration and Exploitation]]).

**4.** Explain MCTS and why it succeeded in Go where traditional game-tree search failed.

> [!example]- Solution
> Each simulation: select with the tree policy inside the tree, expand a node, roll out with the default policy to the end, back up the result into node averages. The tree policy improves as statistics accumulate.
> Traditional search failed because Go's branching factor (~250, vs ~35 in chess) makes depth-limited alpha-beta infeasible, and Go has no reliable static evaluation (unlike material in chess). MCTS replaces the evaluation function with rollouts to a terminal position the rules can score, and replaces uniform expansion with selective sampling, so the simulation budget, not the branching factor, sets the cost. It is anytime and parallel. AlphaGo later replaced random rollouts with learned policy and value networks on the same skeleton.

**5.** (Advanced) Compare Dyna, MCTS and TD search. What does Dyna-2 combine?

> [!example]- Solution
> | | Dyna | MCTS / TD search |
> |---|---|---|
> | Scope | global $Q$ | sub-MDP from $s_t$ |
> | Simulations start | at remembered $(s,a)$ | at the current state |
> | Knowledge kept | accumulates | tree usually discarded |
> | Update | Q-learning | MC (MCTS) / Sarsa (TD search) |
>
> MCTS vs TD search is MC vs TD inside the search: TD has lower variance, more bias, usually better efficiency, and can use function approximation, so positions it hasn't visited still get estimates.
> Dyna-2 keeps general long-term weights (TD from real data) and local short-term weights (TD search). Keeping them separate stops position-specific (possibly model-biased) results from overwriting general knowledge; their sum acts like a prior plus a local correction.

## 📝 Summary

- Model-based RL learns $\langle\mathcal P_\eta,\mathcal R_\eta\rangle$ and plans with it.
- Model learning is supervised: regression and density estimation.
- Two sources of error; planning exploits model errors.
- Sample-based planning: model-free RL on simulated data.
- The table model is the maximum-likelihood MDP (batch TD's answer).
- Model-based RL is only as good as its model.
- Dyna learns and plans from real and simulated experience with one update.
- Ignorant models self-reinforce; Dyna-Q+ adds an exploration bonus.
- Simulation-based search solves the sub-MDP from now; MCTS has an improving tree policy and a fixed rollout policy.
- MCTS transformed computer Go; TD search uses Sarsa; Dyna-2 splits long- and short-term memory.

## ⚠️ Important Notes

1. Planning amplifies model error.
2. Performance is capped by the approximate MDP.
3. A model that knows nothing about a region keeps the agent away from it.
4. Model learning avoids credit assignment and sparse rewards.
5. Sampling beats full-width planning even with a perfect model.
6. Dyna uses the same update for real and simulated data.
7. Search needs only the sub-MDP from now.
8. MCTS: tree policy improves, default policy is fixed.
9. MCTS needs no evaluation function; it is anytime and parallel.
10. TD search trades variance for bias and can generalize.
11. Dyna-2 keeps local search results out of general knowledge.

> [!warning] Gaps in the source slides
> - The Dyna-Q pseudocode (slide 27) and the Dyna architecture (26) are images; see Sutton & Barto ch. 8. Slide 10 is a title only.
> - Slides 28–30 (Dyna-Q maze and changed-environment curves) are images; only the captions survive.
> - Slides 42–46, the five-step MCTS walkthrough, are images: the costliest loss in this lecture.
> - Also images: slides 7–8, 32–33, 41 (outcomes survive), 48 (Go progress chart; names and ranks survive); slide 53 ("Results of TD search in Go") is a title.
> - Truncated: slides 12, 13, 20 (solution 1 cut; solution 2 missing), 23–25, 35–37, 50.
> - References: Sutton (1990, Dyna); Silver, Sutton & Müller (2008, Dyna-2); Silver et al., *Nature* 2016 (AlphaGo).

**Previous:** [[07 - Policy Gradient Methods]] · **Next:** [[09 - Exploration and Exploitation]]
