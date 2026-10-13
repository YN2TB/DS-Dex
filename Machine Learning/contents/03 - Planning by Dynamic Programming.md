---
subject: Machine Learning
chapter: 03
tags: [ds, reinforcement-learning, dynamic-programming, policy-iteration, value-iteration, contraction]
source: "lecture-3-planning-by-dynamic-programming-.pdf — David Silver, UCL (Lecture 3 of 10)"
---

# Planning by Dynamic Programming

[[02 - Markov Decision Processes]] wrote the Bellman equations; this lecture solves them with a known model. That is planning, not learning. Lectures 4–5 drop the model but keep the structure built here.

## 📘 Main Knowledge

### Dynamic programming

"Dynamic": a sequential problem; "programming": optimizing a program, i.e. a policy. DP breaks a problem into subproblems, solves them and combines the solutions. It needs **optimal substructure** (the optimal solution decomposes) and **overlapping subproblems** (solutions recur and can be cached). MDPs have both: the Bellman equation is the recursion and the value function is the cache.

| | Input | Output |
|---|---|---|
| Prediction | MDP and policy π (or the induced MRP) | $v_\pi$ |
| Control | MDP | $v_*$ and $\pi_*$ |

Other DP uses: scheduling, sequence alignment, shortest paths, Viterbi, lattice models ([[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]]).

### Iterative policy evaluation

Apply the Bellman expectation backup repeatedly, $v_1\to v_2\to\dots\to v_\pi$, with **synchronous** backups (every state updated from the previous iterate):
$$v_{k+1}(s)=\sum_a\pi(a\mid s)\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_k(s')\Big),\qquad v_{k+1}=\mathcal R^\pi+\gamma\mathcal P^\pi v_k$$

**Small Gridworld**: 4×4 grid, γ = 1, episodic; states 1–14 plus a terminal state in two corners; moves off the grid leave the state unchanged; reward −1 per step; uniform random policy (0.25 each direction).

| $k$ | first row of $v_k$ |
|---|---|
| 0 | 0, 0, 0, 0 |
| 1 | 0, −1, −1, −1 |
| 2 | 0, −1.75, −2, −2 |
| 3 | 0, −2.4, −2.9, −3.0 |
| 10 | 0, −6.1, −8.4, −9.0 |
| ∞ | 0, −14, −20, −22 |

$v_\pi(s)$ is minus the expected number of steps to termination. The greedy policy with respect to $v_k$ is already optimal at $k=3$, long before the values converge.

### Policy iteration

Evaluate the policy ($v_\pi$), then improve it greedily ($\pi'=\text{greedy}(v_\pi)$), and repeat. In general this needs several rounds but always converges to $\pi_*$.

**Jack's Car Rental**: two locations, up to 20 cars each (21² = 441 states); move up to 5 cars overnight; \$10 per car rented (if available); requests and returns are Poisson, $\mathbb P(n)=\frac{\lambda^n}{n!}e^{-\lambda}$, with means 3/3 at location 1 and 4/2 at location 2. (Sutton & Barto Example 4.2.)

**Why greedy improvement works.** For deterministic π, let $\pi'(s)=\arg\max_aq_\pi(s,a)$. Then $q_\pi(s,\pi'(s))=\max_aq_\pi(s,a)\ge q_\pi(s,\pi(s))=v_\pi(s)$, and applying this one step further each time:
$$v_\pi(s)\le\mathbb E_{\pi'}[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s]\le\mathbb E_{\pi'}[R_{t+1}+\gamma q_\pi(S_{t+1},\pi'(S_{t+1}))\mid S_t=s]\le\dots\le v_{\pi'}(s).$$
If improvement stops, $\max_aq_\pi(s,a)=v_\pi(s)$: the Bellman optimality equation holds, so $v_\pi=v_*$ and π is optimal.

**Does evaluation need to converge?** Stop at ε-convergence, or after $k$ sweeps ($k=3$ was enough in the gridworld). With $k=1$ (update the policy every sweep) you get value iteration. **Generalized policy iteration**: any evaluation method combined with any improvement method. Lectures 4–7 plug in Monte Carlo, TD and function approximation.

### Value iteration

**Principle of optimality**: an optimal policy is an optimal first action followed by an optimal policy from the successor. Formally, π achieves $v_*(s)$ iff it achieves $v_*(s')$ for every state $s'$ reachable from $s$.

So if the subproblems $v_*(s')$ are solved, a one-step lookahead gives $v_*(s)$: start from final rewards and work backwards. This still works in loopy, stochastic MDPs. In the shortest-path example the values spread out from the goal one step per iteration ($V_1$: 0 at the goal, −1 next to it; full grid by $V_7$).

$$v_{k+1}(s)=\max_a\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_k(s')\Big),\qquad v_{k+1}=\max_a\big(\mathcal R^a+\gamma\mathcal P^av_k\big)$$
There is no explicit policy, and intermediate value functions may correspond to no policy.

| Problem | Bellman equation | Algorithm |
|---|---|---|
| prediction | expectation | iterative policy evaluation |
| control | expectation + greedy improvement | policy iteration |
| control | optimality | value iteration |

Cost per iteration: $O(mn^2)$ for $m$ actions and $n$ states with $v$; $O(m^2n^2)$ with $q$.

### Extensions

**Asynchronous DP** backs up states individually in any order; it can save a lot of computation and converges as long as every state keeps being selected.
- **In-place** value iteration keeps one copy of $v$ instead of two, so new values are used within the same sweep (usually faster).
- **Prioritized sweeping** backs up the state with the largest Bellman error $\big|\max_a(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v(s'))-v(s)\big|$, then updates its predecessors' errors; needs reverse dynamics and a priority queue.
- **Real-time DP** backs up only states the agent actually visits ($S_t$ after each step).

**Full-width vs sample backups.** DP considers every successor and action, using the model. It handles medium problems (millions of states) but suffers **Bellman's curse of dimensionality**: $n$ grows exponentially with the number of state variables. **Sample backups** use sampled transitions $\langle S,A,R,S'\rangle$ instead: model-free, constant cost per backup regardless of $n$. This is the bridge to [[04 - Model-Free Prediction]].

**Approximate DP**: represent $\hat v(s,\mathbf w)$. Fitted value iteration samples states $\tilde{\mathcal S}$, computes targets $\tilde v_k(s)=\max_a(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}\hat v(s',\mathbf w_k))$, and trains $\hat v(\cdot,\mathbf w_{k+1})$ on them ([[06 - Value Function Approximation]]).

### Contraction mapping

Why do these algorithms converge, to a unique solution, and how fast? Treat value functions as points in $\mathbb R^{|\mathcal S|}$ with the ∞-norm $\|u-v\|_\infty=\max_s|u(s)-v(s)|$.

The expectation operator $T^\pi(v)=\mathcal R^\pi+\gamma\mathcal P^\pi v$ is a γ-contraction:
$$\|T^\pi(u)-T^\pi(v)\|_\infty=\|\gamma\mathcal P^\pi(u-v)\|_\infty\le\gamma\|u-v\|_\infty.$$
Rewards cancel, and rows of $\mathcal P^\pi$ are probability distributions, so averaging can't increase the largest difference.

**Contraction mapping theorem**: on a complete metric space, a γ-contraction converges to a unique fixed point at linear rate γ. Hence iterative policy evaluation converges to $v_\pi$ and policy iteration to $v_*$. The optimality operator $T^*(v)=\max_a(\mathcal R^a+\gamma\mathcal P^av)$ is also a γ-contraction with fixed point $v_*$, so value iteration converges to $v_*$.

## ✏️ Exercises

**1.** In Small Gridworld the greedy policy is optimal at $k=3$ but the values converge only as $k\to\infty$. Why, and what follows?

> [!example]- Solution
> Greedy choice depends on the ordering of successor values, not their size. By $k=3$ states nearer the exit already rank higher, although the values (−2.4 to −3.0) are far from the final −14 to −22. Each sweep moves information only one more step, so magnitudes converge slowly.
> Consequences: running evaluation to convergence is often wasted; $k=1$ gives value iteration; any approximate evaluation can be used (GPI). This early optimality isn't guaranteed in general (near-ties take longer), but policy iteration recovers because it re-evaluates each new policy.

**2.** Prove greedy improvement never makes a policy worse, and that when it stops the policy is optimal.

> [!example]- Solution
> One step: $q_\pi(s,\pi'(s))=\max_aq_\pi(s,a)\ge q_\pi(s,\pi(s))=v_\pi(s)$. Applying it at each later step replaces $v_\pi$ by $q_\pi(\cdot,\pi'(\cdot))$ and unrolls to $v_{\pi'}(s)$, so $v_{\pi'}\ge v_\pi$.
> If nothing improves, $v_\pi(s)=\max_aq_\pi(s,a)$, which is the Bellman optimality equation; its solution is unique (contraction), so $v_\pi=v_*$. Values rise monotonically and there are finitely many ($m^n$) deterministic policies, so policy iteration terminates. The proof needs the exact $v_\pi$; approximate evaluation weakens it ([[06 - Value Function Approximation]]).

**3.** Compare policy iteration and value iteration. When is each preferable?

> [!example]- Solution
> | | Policy iteration | Value iteration |
> |---|---|---|
> | Equation | expectation + greedy | optimality |
> | Policy | explicit throughout | only at the end |
> | Iterations | few | many |
> | Cost per iteration | high (full evaluation) | one sweep |
> | Intermediate $v$ | a real $v_\pi$ | may match no policy |
>
> They are the ends of one range (evaluate $k$ sweeps: $k=\infty$ vs $k=1$). Policy iteration suits cheap evaluation and the need for a valid policy if stopped early; value iteration suits expensive evaluation and simple code. Both cost $O(mn^2)$ per sweep and need the model.

**4.** Explain the curse of dimensionality and how sample backups escape it.

> [!example]- Solution
> $n$ grows exponentially with state variables: 10 binary variables give 1,024 states, 20 give about a million (DP's practical limit), 30 a billion; Backgammon has about $10^{20}$ states, Go about $10^{170}$. Each full-width backup sums over all successors for every state and action.
> Sampling replaces the sum with one transition (unbiased, constant cost, more variance), visits only states the agent reaches (as in real-time DP), and needs no model, only interaction. It doesn't solve storage: you can't keep a table of $10^{170}$ values, which needs function approximation.

**5.** (Advanced) Explain the contraction argument and why γ is the convergence rate.

> [!example]- Solution
> Rewards cancel in $T^\pi(u)-T^\pi(v)$, and a stochastic matrix is non-expansive in the ∞-norm (a weighted average can't exceed the maximum), so the factor γ is all that remains. (It is not a contraction in the Euclidean norm.) The theorem gives a unique fixed point, convergence from any start, and $\|v_k-v_\pi\|_\infty\le\gamma^k\|v_0-v_\pi\|_\infty$.
> γ near 1 means each state's value depends on the distant future, so information must travel far and convergence is slow; at γ = 1 the argument fails. Small Gridworld (γ = 1) converges because it is episodic with guaranteed termination. When function approximation breaks contraction, divergence becomes possible (the deadly triad).

## 📝 Summary

- DP needs optimal substructure and overlapping subproblems; MDPs have both.
- DP assumes a known model: planning.
- Policy evaluation: $v_{k+1}=\mathcal R^\pi+\gamma\mathcal P^\pi v_k$.
- Policy iteration: evaluate, improve greedily; improvement never hurts, and stopping means optimal.
- Truncated evaluation → value iteration; generalized policy iteration is the template for later lectures.
- Value iteration applies the optimality backup; no explicit policy until the end.
- $O(mn^2)$ per sweep; asynchronous variants: in-place, prioritized sweeping, real-time.
- Sample backups break the curse of dimensionality.
- Both Bellman operators are γ-contractions in the ∞-norm: unique fixed points, linear rate γ.

## ⚠️ Important Notes

1. DP needs $\mathcal P$ and $\mathcal R$.
2. The greedy policy often converges long before the values.
3. Value iteration's intermediate values may match no policy.
4. The improvement proof assumes exact evaluation.
5. "Millions of states" is only about 20 binary features.
6. In-place DP is faster as well as smaller.
7. Prioritized sweeping needs predecessor information.
8. Asynchronous DP needs every state to keep being updated.
9. The contraction proof relies on the ∞-norm.
10. At γ = 1 it fails; episodic termination is what saves Small Gridworld.
11. Convergence slows as γ → 1.

> [!warning] Gaps in the source slides
> - Images: slides 8 and 24 (backup diagrams), 9–11 (gridworld layout and greedy-policy arrows; value arrays extracted jumbled and were recomputed), 13 and 19 (iteration diagrams), 15 (Jack's Car Rental policy plots), 22 (shortest-path grids).
> - Truncated: slides 4, 16 (end of the improvement proof), 18, 26 ($q$-based complexity), 32, 34; completed from context.
> - The slide shows −1.7 at $k=2$; the exact value is −1.75.
> - Slide 25 links an online value-iteration demo.

**Previous:** [[02 - Markov Decision Processes]] · **Next:** [[04 - Model-Free Prediction]]
