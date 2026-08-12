---
subject: Machine Learning
chapter: 03
tags: [ds, reinforcement-learning, dynamic-programming, policy-iteration, value-iteration, contraction]
source: "lecture-3-planning-by-dynamic-programming-.pdf — David Silver, UCL (Lecture 3 of 10)"
---

# Planning by Dynamic Programming

> [!note] Where this sits in the course
> [[02 - Markov Decision Processes]] wrote down the Bellman equations; this lecture **solves them**, assuming the model is known. It is therefore **planning, not learning** — the distinction from [[01 - Introduction to Reinforcement Learning]]. Lectures 4–5 drop the model assumption, but they inherit the algorithmic skeleton built here.

## 📘 Main Knowledge

### What is Dynamic Programming?

> **Dynamic** — sequential or temporal component to the problem
> **Programming** — optimising a "program", i.e. a policy (*cf.* linear programming)
>
> A method for solving complex problems by **breaking them into subproblems**, solving the subproblems, and combining the solutions.

**Two required properties:**

- **Optimal substructure** — the principle of optimality applies; the optimal solution can be decomposed into subproblems.
- **Overlapping subproblems** — subproblems recur many times, so **solutions can be cached and reused**.

> **Markov decision processes satisfy both:** the **Bellman equation gives the recursive decomposition**, and the **value function** stores and reuses solutions.

**DP assumes full knowledge of the MDP** and is used for **planning**:

| | Input | Output |
|---|---|---|
| **Prediction** | MDP $\langle\mathcal{S},\mathcal{A},\mathcal{P},\mathcal{R},\gamma\rangle$ and policy $\pi$ (or MRP $\langle\mathcal{S},\mathcal{P}^\pi,\mathcal{R}^\pi,\gamma\rangle$) | Value function $v_\pi$ |
| **Control** | MDP $\langle\mathcal{S},\mathcal{A},\mathcal{P},\mathcal{R},\gamma\rangle$ | Optimal value function $v_*$ **and** optimal policy $\pi_*$ |

**Other DP applications:** scheduling algorithms · string algorithms (sequence alignment) · graph algorithms (shortest path) · graphical models (**Viterbi**) · bioinformatics (lattice models). See [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]].

---

## Part 1 — Policy Evaluation (Prediction)

> **Problem:** evaluate a given policy $\pi$.
> **Solution:** iterative application of the **Bellman expectation backup**, $v_1 \to v_2 \to \dots \to v_\pi$.

Using **synchronous backups**: at each iteration $k+1$, for all states $s \in \mathcal{S}$, update $v_{k+1}(s)$ from $v_k(s')$ where $s'$ is a successor of $s$.

$$v_{k+1}(s) = \sum_{a\in\mathcal{A}}\pi(a\mid s)\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}v_k(s')\right)$$
$$v_{k+1} = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v_k$$

**This is the Bellman expectation equation turned into an assignment.** The equation says $v_\pi = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v_\pi$; the algorithm repeatedly *applies* the right-hand side and converges to the fixed point.

### Small Gridworld

The running example:
- Undiscounted **episodic** MDP ($\gamma = 1$)
- Nonterminal states $1,\dots,14$; one terminal state (shown twice as shaded squares)
- **Actions leading out of the grid leave the state unchanged**
- **Reward is −1 until the terminal state is reached**
- Uniform random policy: $\pi(n\mid\cdot) = \pi(e\mid\cdot) = \pi(s\mid\cdot) = \pi(w\mid\cdot) = 0.25$

Successive value functions $v_k$:

| $k$ | Values (partial) |
|---|---|
| 0 | all 0.0 |
| 1 | all −1.0 |
| 2 | −1.7, −2.0, −2.0, … |
| 3 | −2.4, −2.9, −3.0, … |
| 10 | −6.1, −8.4, −9.0, … |
| ∞ | −14, −20, −22, … |

Because reward is −1 per step, $v_\pi(s)$ is **minus the expected number of steps to termination** under the random policy.

**The crucial observation** — the greedy policy w.r.t. $v_k$ becomes **optimal at $k=3$**, long before the values themselves converge at $k=\infty$. This motivates everything in Part 3.

---

## Part 2 — Policy Iteration (Control)

> Given a policy $\pi$:
> - **Evaluate** the policy: $v_\pi(s) = \mathbb{E}[R_{t+1} + \gamma R_{t+2} + \dots \mid S_t = s]$
> - **Improve** the policy by acting **greedily** with respect to $v_\pi$: $\pi' = \text{greedy}(v_\pi)$
>
> In Small Gridworld the improved policy was already optimal. **In general more iterations are needed — but this process always converges to $\pi_*$.**

**The two alternating steps:**
- **Policy evaluation** — estimate $v_\pi$ (iterative policy evaluation)
- **Policy improvement** — generate $\pi' \ge \pi$ (greedy policy improvement)

### Jack's Car Rental

- **States:** two locations, maximum 20 cars at each
- **Actions:** move up to 5 cars between locations overnight
- **Reward:** \$10 for each car rented (**must be available**)
- **Transitions:** cars returned and requested randomly, **Poisson** with $\mathbb{P}(n) = \frac{\lambda^n}{n!}e^{-\lambda}$
  - 1st location: average requests 3, average returns 3
  - 2nd location: average requests 4, average returns 2

A genuinely non-trivial MDP — 441 states — where the optimal policy is not obvious by inspection. See [[Probability Theory/contents/00-Index|Probability Theory]] for the Poisson distribution.

### Why greedy improvement works

Consider a deterministic policy $a = \pi(s)$. Improve by acting greedily:
$$\pi'(s) = \arg\max_{a\in\mathcal{A}} q_\pi(s,a)$$

**This improves the value from any state over one step:**
$$q_\pi(s,\pi'(s)) = \max_{a\in\mathcal{A}} q_\pi(s,a) \ge q_\pi(s,\pi(s)) = v_\pi(s)$$

**And therefore improves the value function**, $v_{\pi'}(s) \ge v_\pi(s)$, by telescoping the argument:
$$\begin{aligned} v_\pi(s) &\le q_\pi(s,\pi'(s)) = \mathbb{E}_{\pi'}[R_{t+1} + \gamma v_\pi(S_{t+1})\mid S_t = s] \\ &\le \mathbb{E}_{\pi'}[R_{t+1} + \gamma q_\pi(S_{t+1},\pi'(S_{t+1}))\mid S_t = s] \\ &\le \mathbb{E}_{\pi'}[R_{t+1} + \gamma R_{t+2} + \gamma^2 \dots \mid S_t=s] = v_{\pi'}(s)\end{aligned}$$

**The trick is applying the one-step inequality repeatedly**, pushing the switch to $\pi'$ one step further into the future each time.

**When improvement stops:**
$$q_\pi(s,\pi'(s)) = \max_{a\in\mathcal{A}}q_\pi(s,a) = q_\pi(s,\pi(s)) = v_\pi(s)$$

Then the **Bellman optimality equation is satisfied**: $v_\pi(s) = \max_a q_\pi(s,a)$. **Therefore $v_\pi(s) = v_*(s)$ for all $s$, and $\pi$ is optimal.**

This is the whole convergence proof for policy iteration, and it is remarkably short: greedy improvement can only help, and when it stops helping you are provably optimal.

### Modified and generalised policy iteration

> **Does policy evaluation need to converge to $v_\pi$?**
> - Or introduce a stopping condition, e.g. $\epsilon$-convergence of the value function?
> - Or simply **stop after $k$ iterations**? In Small Gridworld **$k=3$ was sufficient** to achieve the optimal policy.
> - **Why not update the policy every iteration, i.e. stop after $k=1$? This is equivalent to value iteration.**

> **Generalised Policy Iteration (GPI):**
> - **Policy evaluation** — *any* policy evaluation algorithm
> - **Policy improvement** — *any* policy improvement algorithm

**GPI is the organising idea of the rest of the course.** Lectures 4–7 all substitute different evaluation methods (Monte-Carlo, TD, function approximation) into this same skeleton.

---

## Part 3 — Value Iteration

### The Principle of Optimality

> Any optimal policy can be subdivided into two components: an **optimal first action** $A_*$, followed by an **optimal policy from the successor state** $S'$.
>
> **Theorem (Principle of Optimality).** A policy $\pi(a\mid s)$ achieves the optimal value from state $s$, $v_\pi(s) = v_*(s)$, **if and only if** for any state $s'$ reachable from $s$, $\pi$ achieves the optimal value from $s'$, $v_\pi(s') = v_*(s')$.

This is exactly the "optimal substructure" property DP requires.

### Deterministic value iteration

> If we know the solution to subproblems $v_*(s')$, then $v_*(s)$ can be found by **one-step lookahead**:
> $$v_*(s) \leftarrow \max_{a\in\mathcal{A}}\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}v_*(s')\right)$$
>
> **Intuition: start with final rewards and work backwards.** Still works with **loopy, stochastic** MDPs.

**Shortest Path example** — the values spread outward from the goal one step per iteration: $V_1$ has 0 at the goal and −1 adjacent, $V_2$ reaches −2, and by $V_7$ the whole grid is filled. The information propagates exactly one step of distance per sweep.

### The algorithm

> **Problem:** find the optimal policy $\pi$.
> **Solution:** iterative application of the **Bellman optimality backup**, $v_1 \to v_2 \to \dots \to v_*$, using synchronous backups.

$$v_{k+1}(s) = \max_{a\in\mathcal{A}}\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}v_k(s')\right)$$
$$v_{k+1} = \max_{a\in\mathcal{A}}\mathcal{R}^a + \gamma\mathcal{P}^a v_k$$

> **Unlike policy iteration, there is no explicit policy. Intermediate value functions may not correspond to any policy.**

That is a genuinely important caveat: $v_3$ in value iteration is not $v_\pi$ for any $\pi$ — it is simply the third iterate. Only at convergence does it become meaningful.

### Summary of synchronous DP algorithms

| Problem | Bellman Equation | Algorithm |
|---|---|---|
| **Prediction** | Bellman **Expectation** Equation | Iterative Policy Evaluation |
| **Control** | Bellman **Expectation** Equation + Greedy Policy Improvement | **Policy Iteration** |
| **Control** | Bellman **Optimality** Equation | **Value Iteration** |

- Algorithms are based on the state-value function $v_\pi(s)$ or $v_*(s)$
- **Complexity $O(mn^2)$ per iteration** for $m$ actions and $n$ states
- Could also apply to the action-value function $q$, at $O(m^2n^2)$ *(truncated in source)*

---

## Part 4 — Extensions

### Asynchronous DP

> Synchronous backups back up **all states in parallel**. **Asynchronous DP backs up states individually, in any order.** Can **significantly reduce computation**, and is **guaranteed to converge if all states continue to be selected**.

**Three ideas:**

**In-place DP** — synchronous value iteration stores **two copies** of the value function:
$$v_{new}(s) \leftarrow \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_{old}(s')\right); \quad v_{old} \leftarrow v_{new}$$
**In-place value iteration stores only one:**
$$v(s) \leftarrow \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v(s')\right)$$
Updates propagate within a sweep rather than between sweeps, so it usually converges **faster** as well as using half the memory.

**Prioritised sweeping** — use the magnitude of the **Bellman error** to guide state selection:
$$\left|\max_{a\in\mathcal{A}}\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v(s')\right) - v(s)\right|$$
Back up the state with the largest remaining error, then update the errors of affected states. **Requires knowledge of reverse dynamics (predecessor states)**, and is implemented efficiently with a **priority queue**.

**Real-time DP** — only back up states **relevant to the agent**, using its experience to guide selection. After each time-step $S_t, A_t, R_{t+1}$, back up $S_t$.

### Full-width vs sample backups

> **DP uses full-width backups:** for each backup, **every successor state and action is considered**, using knowledge of the MDP's transitions and reward function.
>
> DP is effective for **medium-sized problems (millions of states)**. For large problems DP suffers **Bellman's curse of dimensionality** — the number of states $n = |\mathcal{S}|$ grows **exponentially** with the number of state variables.

> **Sample backups** (subsequent lectures) use sample rewards and transitions $\langle S,A,R,S'\rangle$ **instead of** the reward function $\mathcal{R}$ and dynamics $\mathcal{P}$.
>
> **Advantages:**
> - **Model-free** — no advance knowledge of the MDP required
> - **Breaks the curse of dimensionality through sampling**
> - **Cost of backup is constant, independent of $n = |\mathcal{S}|$**

**This slide is the bridge to the rest of the course.** Everything from [[04 - Model-Free Prediction]] onward replaces the sum over successors with a sample.

### Approximate DP

Approximate the value function with a function approximator $\hat{v}(s,\mathbf{w})$ and apply DP to it. **Fitted Value Iteration** repeats at each iteration $k$: sample states $\tilde{\mathcal{S}} \subseteq \mathcal{S}$; for each $s \in \tilde{\mathcal{S}}$ estimate the target using the Bellman optimality equation
$$\tilde{v}_k(s) = \max_{a\in\mathcal{A}}\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}\hat{v}(s',\mathbf{w}_k)\right)$$
then train the next value function $\hat{v}(\cdot,\mathbf{w}_{k+1})$ on those targets. → [[06 - Value Function Approximation]]

---

## Part 5 — Contraction Mapping (the convergence proofs)

> **The technical questions:** How do we know value iteration converges to $v_*$? That iterative policy evaluation converges to $v_\pi$? And therefore that policy iteration converges to $v_*$? **Is the solution unique? How fast do these algorithms converge?**
>
> **These are all resolved by the contraction mapping theorem.**

**The setup.** Consider the vector space $\mathcal{V}$ over value functions, with $|\mathcal{S}|$ dimensions — each point fully specifies a value function. **What does a Bellman backup do to points in this space? It brings value functions closer, so the backups must converge on a unique solution.**

**Distance is measured by the $\infty$-norm** — the largest difference between state values:
$$\|u - v\|_\infty = \max_{s\in\mathcal{S}}|u(s) - v(s)|$$

**The Bellman expectation backup is a contraction.** Define the operator $T^\pi(v) = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v$. It is a **$\gamma$-contraction** — it makes value functions closer by at least $\gamma$:
$$\begin{aligned}\|T^\pi(u) - T^\pi(v)\|_\infty &= \|(\mathcal{R}^\pi + \gamma\mathcal{P}^\pi u) - (\mathcal{R}^\pi + \gamma\mathcal{P}^\pi v)\|_\infty \\ &= \|\gamma\mathcal{P}^\pi(u-v)\|_\infty \\ &\le \|\gamma\mathcal{P}^\pi\|u-v\|_\infty\|_\infty \\ &\le \gamma\|u-v\|_\infty\end{aligned}$$

The $\mathcal{R}^\pi$ terms cancel; then since each row of $\mathcal{P}^\pi$ sums to 1, averaging cannot increase the maximum deviation — so only the factor $\gamma$ survives.

> **Theorem (Contraction Mapping Theorem).** For any metric space $\mathcal{V}$ that is **complete** (closed) under an operator $T(v)$, where $T$ is a **$\gamma$-contraction**:
> - $T$ **converges to a unique fixed point**
> - At a **linear convergence rate of $\gamma$**

**Consequences:**
- $T^\pi$ has a unique fixed point; $v_\pi$ **is** that fixed point (by the Bellman expectation equation). Therefore **iterative policy evaluation converges on $v_\pi$**, and **policy iteration converges on $v_*$**.
- The **Bellman optimality backup** $T^*(v) = \max_{a\in\mathcal{A}}\mathcal{R}^a + \gamma\mathcal{P}^a v$ is **also a $\gamma$-contraction**, $\|T^*(u) - T^*(v)\|_\infty \le \gamma\|u-v\|_\infty$. Its unique fixed point is $v_*$, so **value iteration converges on $v_*$**.

**Note what this buys:** existence, uniqueness, and a convergence *rate*, all from one theorem — and it explains why $\gamma < 1$ matters mathematically, not just for bounding returns.

## ✏️ Exercises

**1.** In Small Gridworld the greedy policy is optimal at $k=3$ while the values converge only at $k=\infty$. Explain why, and what it implies.

> [!example]- Solution
> **Because the greedy policy depends only on the *ordering* of values, not their magnitudes.**
>
> $\pi'(s) = \arg\max_a q(s,a)$ compares successor values. Once $v_k$ has the states ranked correctly — nearer the terminal state is better — the $\arg\max$ picks the right action, even though every value is still far from its converged magnitude. At $k=3$ the values are around −2.4 to −3.0 against final values near −14 to −22: **off by a factor of seven, and the induced policy is already optimal.**
>
> The ordering stabilises quickly because the −1-per-step structure means relative distances to the terminal state are established after only a few sweeps. Magnitudes take much longer, because each sweep only propagates information one step further — the same one-step-per-iteration spread visible in the Shortest Path example.
>
> **Three implications, and the lecture draws all of them:**
>
> **1. Full convergence of evaluation is wasted work.** *"Does policy evaluation need to converge to $v_\pi$?"* — no. Stop early.
>
> **2. Taken to the limit, $k=1$ gives value iteration.** Evaluate for a single sweep, improve immediately, repeat. The lecture states the equivalence explicitly, and it explains why value iteration needs no explicit policy: the improvement is folded into the $\max$.
>
> **3. It licenses Generalised Policy Iteration.** If evaluation need not be exact, *any* approximate evaluation will do — which is what lets Monte-Carlo, TD, and function approximation slot into the same skeleton in Lectures 4–7.
>
> **A caution:** *"optimal at $k=3$"* is observed here, not guaranteed generally. In an MDP with near-ties between actions, the ordering can take many sweeps to settle, and a premature greedy step gives a suboptimal policy. Policy iteration remains correct because it re-evaluates the *new* policy and keeps improving — it recovers from a bad early guess.

**2.** Prove that greedy policy improvement cannot make a policy worse, and explain why the proof implies optimality when improvement stops.

> [!example]- Solution
> **Step 1 — the one-step inequality.** By definition of $\arg\max$:
> $$q_\pi(s,\pi'(s)) = \max_a q_\pi(s,a) \ge q_\pi(s,\pi(s)) = v_\pi(s)$$
> Taking the best action is at least as good as taking the one $\pi$ would take. Note $q_\pi(s,\pi(s)) = v_\pi(s)$ — following $\pi$ from the start *is* $v_\pi$.
>
> **Step 2 — telescoping to a full-trajectory result.** One step is not enough: $\pi'$ acts greedily *everywhere*, so we must show the improvement compounds.
> $$\begin{aligned} v_\pi(s) &\le q_\pi(s,\pi'(s)) = \mathbb{E}_{\pi'}[R_{t+1} + \gamma v_\pi(S_{t+1})\mid S_t = s] \\ &\le \mathbb{E}_{\pi'}[R_{t+1} + \gamma q_\pi(S_{t+1},\pi'(S_{t+1}))\mid S_t=s] \\ &\le \mathbb{E}_{\pi'}[R_{t+1} + \gamma R_{t+2} + \gamma^2 v_\pi(S_{t+2})\mid S_t=s] \\ &\;\;\vdots \\ &\le \mathbb{E}_{\pi'}[R_{t+1} + \gamma R_{t+2} + \dots \mid S_t=s] = v_{\pi'}(s)\end{aligned}$$
> Each line applies Step 1 **one step further into the future**, replacing $v_\pi$ with $q_\pi(\cdot,\pi')$ and unrolling. In the limit, $\pi'$ is followed forever — giving $v_{\pi'}$.
>
> **Step 3 — why stopping implies optimality.** If improvement yields nothing, then
> $$\max_a q_\pi(s,a) = q_\pi(s,\pi(s)) = v_\pi(s)$$
> But $v_\pi(s) = \max_a q_\pi(s,a)$ **is exactly the Bellman optimality equation**. Since that equation has a **unique** solution — by the contraction mapping theorem in Part 5 — and $v_*$ satisfies it, we get $v_\pi = v_*$. **$\pi$ is optimal.**
>
> **This is the whole convergence argument for policy iteration**, and it is unusually clean: improvement never hurts, so values increase monotonically; the policy space is finite (there are $m^n$ deterministic policies); so the process must terminate; and terminating means satisfying the optimality equation.
>
> Note the argument requires the **exact** $v_\pi$. With approximate evaluation the guarantee weakens — which is a real source of instability once function approximation enters in [[06 - Value Function Approximation]].

**3.** Compare policy iteration and value iteration. When is each preferable?

> [!example]- Solution
> | | **Policy Iteration** | **Value Iteration** |
> |---|---|---|
> | Bellman equation | **Expectation** (+ greedy improvement) | **Optimality** |
> | Structure | Evaluate to convergence, then improve | One backup with `max`, repeat |
> | Explicit policy? | **Yes**, maintained throughout | **No** — extracted only at the end |
> | Iterations to converge | **Few** | Many |
> | Cost per iteration | **High** (full evaluation) | Low (one sweep) |
> | Intermediate $v$ meaningful? | Yes — it is $v_\pi$ for the current $\pi$ | **No** — may correspond to no policy |
>
> **They are two ends of one spectrum.** Modified policy iteration truncates evaluation after $k$ sweeps; $k = \infty$ is policy iteration, **$k=1$ is value iteration**. Everything in between is valid, which is the GPI insight.
>
> **When policy iteration wins:** when the policy space is small relative to the value space, or when evaluation is cheap (a small MRP where $(I-\gamma\mathcal{P}^\pi)^{-1}$ is directly computable). It converges in **very few policy improvements** — often a handful even for large problems — because each improvement is a big, informed step.
>
> **When value iteration wins:** when full evaluation is expensive, when you only want $v_*$ and not intermediate policies, and when the implementation must be simple — value iteration is a single loop with a `max`.
>
> **The important caveat about value iteration:** *"intermediate value functions may not correspond to any policy."* Extracting a greedy policy from a partially converged $v_k$ can therefore give something arbitrarily bad — the values are not $v_\pi$ for any $\pi$, so no guarantee attaches to them. Policy iteration always holds a *real* policy with a *real* value function, which matters if you must stop early and deploy.
>
> **Both are $O(mn^2)$ per sweep and both require the full model**, so neither escapes the curse of dimensionality. That is what Part 4's sample backups address.

**4.** Explain the curse of dimensionality and how sample backups escape it.

> [!example]- Solution
> **The curse:** $n = |\mathcal{S}|$ grows **exponentially** with the number of state variables. Ten binary variables give $2^{10} = 1{,}024$ states; twenty give a million; thirty give a billion. For continuous variables discretised into $d$ bins with $k$ dimensions, $n = d^k$.
>
> DP costs $O(mn^2)$ per sweep, so it is quadratic in an already-exponential quantity. Silver puts the practical ceiling at *"millions of states"* — which sounds large and corresponds to only about 20 binary features. Backgammon has $10^{20}$ states; Go has $10^{170}$.
>
> **Why full-width backups cause it.** Each backup considers **every action and every successor state**:
> $$v_{k+1}(s) = \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'\in\mathcal{S}}\mathcal{P}^a_{ss'}v_k(s')\right)$$
> That $\sum_{s'\in\mathcal{S}}$ is a sum over the entire state space, and it must be done for every $s$ and every $a$.
>
> **How sampling escapes it — two independent savings:**
>
> **1. Replace the expectation with a sample.** Instead of summing over all $s'$ weighted by $\mathcal{P}^a_{ss'}$, take **one** transition $\langle S,A,R,S'\rangle$ and use it as an unbiased estimate. **The cost of a backup becomes constant, independent of $n$** — the lecture states this explicitly. You trade exactness for variance, and average the variance away over many samples.
>
> **2. Do not visit every state.** DP sweeps all $n$ states regardless of relevance. An agent following a policy visits only the states it actually reaches, which in most real problems is a vanishingly small, highly structured subset — the **Real-Time DP** idea, generalised. Most of Go's $10^{170}$ positions are unreachable in sensible play.
>
> **The third saving, and the reason it matters practically:** sampling is **model-free**. Full-width backups need $\mathcal{P}^a_{ss'}$ and $\mathcal{R}^a_s$ written down; samples need only the ability to *interact*. This is the shift from planning to learning, and it is why [[04 - Model-Free Prediction]] and [[05 - Model-Free Control]] are the practically important lectures.
>
> **What sampling does not fix:** the *representation* problem. You still cannot store a table of $10^{170}$ values. That needs **function approximation** — [[06 - Value Function Approximation]] — and the combination of sampling *and* approximation is what makes RL work at scale.

**5.** (Advanced) Explain the contraction mapping argument and why $\gamma$ appears in the convergence rate.

> [!example]- Solution
> **The geometry.** Think of a value function as a point in $\mathbb{R}^{|\mathcal{S}|}$ — one coordinate per state. A Bellman backup is a **map** from this space to itself. The claim is that it moves any two points **closer together** by a factor of at least $\gamma$.
>
> **The proof for $T^\pi(v) = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v$:**
> $$\|T^\pi(u) - T^\pi(v)\|_\infty = \|(\mathcal{R}^\pi + \gamma\mathcal{P}^\pi u) - (\mathcal{R}^\pi + \gamma\mathcal{P}^\pi v)\|_\infty = \gamma\|\mathcal{P}^\pi(u-v)\|_\infty \le \gamma\|u-v\|_\infty$$
>
> Two steps matter. **The reward terms cancel** — the backup's constant part contributes nothing to the *distance* between images. And **$\|\mathcal{P}^\pi x\|_\infty \le \|x\|_\infty$** because each row of $\mathcal{P}^\pi$ is a probability distribution: a weighted average of numbers cannot exceed the largest of them in absolute value. So the transition matrix is non-expansive, and **the entire contraction comes from $\gamma$.**
>
> **Why the $\infty$-norm specifically.** The proof needs "averaging cannot increase the maximum", which is exactly a statement about the max-norm. It would fail for the Euclidean norm — $\mathcal{P}^\pi$ is not a contraction in $\|\cdot\|_2$. Choosing the right norm is what makes the proof work.
>
> **What the theorem gives:**
> - **Existence and uniqueness** of a fixed point. So $v_\pi$ is the *only* solution to the Bellman expectation equation — the equation does not merely have $v_\pi$ as *a* solution, it has it as *the* solution.
> - **Convergence from any starting point.** Initialising $v_0$ arbitrarily is fine.
> - **A linear rate of $\gamma$:** $\|v_k - v_\pi\|_\infty \le \gamma^k\|v_0 - v_\pi\|_\infty$. Error shrinks by a constant factor per sweep.
>
> **Why $\gamma$ appearing in the rate is intuitive.** $\gamma$ measures how much the future influences the present. Small $\gamma$ means distant states barely matter, so information need not propagate far and convergence is fast. **$\gamma$ close to 1 means the value of every state depends on the whole future**, so information must traverse the state space — convergence is slow. At $\gamma = 1$ the contraction factor is 1 and **the argument fails entirely**.
>
> That last point explains a subtlety in the lecture: Small Gridworld uses $\gamma = 1$, so this proof does not apply to it. Convergence there relies on the MDP being **episodic** with guaranteed termination, which provides contraction by a different route. **Undiscounted continuing tasks have no such guarantee** — which is why $\gamma < 1$ is standard, and why the average-reward formulation of [[02 - Markov Decision Processes]] needs entirely separate theory.
>
> The same operator-contraction argument reappears throughout RL, and its *failure* under function approximation is the origin of the "deadly triad" in [[06 - Value Function Approximation]].

## 📝 Summary

- **DP requires optimal substructure and overlapping subproblems.** MDPs have both: the Bellman equation gives the recursion, the value function caches solutions.
- **DP assumes a known model, so it is planning, not learning.**
- **Iterative policy evaluation** applies the Bellman *expectation* backup repeatedly: $v_{k+1} = \mathcal{R}^\pi + \gamma\mathcal{P}^\pi v_k$.
- **Policy iteration** = evaluate + greedily improve, repeated. **Greedy improvement never makes a policy worse**, and when it stops improving the Bellman optimality equation is satisfied — so the policy is optimal.
- **Evaluation need not converge fully.** Stopping after $k=1$ gives **value iteration**; this generality is **Generalised Policy Iteration**, the skeleton of Lectures 4–7.
- **Value iteration** applies the Bellman *optimality* backup: $v_{k+1}(s) = \max_a(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_k(s'))$. **No explicit policy**, and intermediate values may correspond to no policy.
- **Complexity $O(mn^2)$ per iteration.**
- **Asynchronous DP** — in-place (one copy, faster), prioritised sweeping (largest Bellman error first, needs reverse dynamics), real-time (follow the agent's experience).
- **Full-width backups suffer the curse of dimensionality; sample backups have constant cost, are model-free, and break it.**
- **Both Bellman operators are $\gamma$-contractions in the $\infty$-norm**, so by the contraction mapping theorem all three algorithms converge to a **unique** fixed point at a **linear rate of $\gamma$**.

## ⚠️ Important Notes

**DP is planning, not learning.** It requires $\mathcal{P}$ and $\mathcal{R}$ in advance. Everything from Lecture 4 onward exists because that assumption usually fails.

**The greedy policy converges long before the values do.** In Small Gridworld, optimal at $k=3$ with values seven times off. Running evaluation to convergence is usually wasted computation.

**Value iteration's intermediate value functions may correspond to no policy.** Extracting a greedy policy from a partially converged $v_k$ carries no guarantee — unlike policy iteration, which always holds a genuine $v_\pi$.

**The policy improvement proof requires the *exact* $v_\pi$.** With approximate evaluation the monotonic improvement guarantee weakens, which is a real source of instability under function approximation.

**Complexity is $O(mn^2)$ per sweep, and $n$ is already exponential in the number of state variables.** "Millions of states" sounds large but is only ~20 binary features.

**In-place DP is not just a memory optimisation** — updates propagate within a sweep, so it usually converges faster than the two-copy version.

**Prioritised sweeping needs reverse dynamics** (which states lead *into* $s$), which is extra information beyond $\mathcal{P}$ and is not always available.

**Asynchronous DP converges only if all states continue to be selected.** A prioritisation scheme that permanently starves some states breaks the guarantee.

**The contraction proof uses the $\infty$-norm specifically**, because it relies on "averaging cannot increase the maximum". It does not hold in the Euclidean norm.

**The contraction argument fails at $\gamma = 1$.** Small Gridworld converges because it is episodic with guaranteed termination, not because of this theorem. Undiscounted *continuing* tasks need separate theory.

**Convergence slows as $\gamma \to 1$**, since the rate is $\gamma$ per sweep. Far-sighted agents are computationally more expensive, not just conceptually harder.

> [!warning] Gaps in the source slides
> Silver's slides extract very well — **all theorems, proofs, and equations survived.** Losses are figures:
> - **Slides 9–11 (Small Gridworld)** — the grid layout is an image, and the value arrays extracted **jumbled across columns** (the $k=1,2,3,10,\infty$ rows are recoverable but the per-cell layout is not). **The greedy-policy arrow diagrams, which are the point of the example, are entirely images.**
> - **Slide 15 — "Policy Iteration in Jack's Car Rental"** is an image; the classic policy/value surface plots are not captured.
> - **Slides 13, 19** — the policy iteration and GPI cycle diagrams.
> - **Slide 22 (Shortest Path)** — the value arrays for $V_1$–$V_7$ extracted but scrambled across the grid; the layout is an image.
> - **Slides 8, 24** — the backup diagrams.
> - **Several truncations:** slide 4 (*"Value function s…"* — presumably "stores and reuses solutions"), slide 16 (**the policy improvement proof's final line is cut at $\gamma^2$**), slide 18 (cut at *"equivalent to value iteration (ne…"* — likely "next section"), slide 26 (**the $q$-based complexity $O(m^2n^2)$ is cut at "Could also"**), slide 32 (cut at "Ev…"), slide 34 (fitted value iteration's training step cut at $\hat v(\cdot,$).
> - **Slide 25** links a [value iteration demo](http://www.cs.ubc.ca/~poole/demos/mdp/vi.html).
>
> **Jack's Car Rental** is from Sutton & Barto Ch. 4 (Example 4.2), where the full policy plots appear.

---
**Previous:** [[02 - Markov Decision Processes]] · **Next:** [[04 - Model-Free Prediction]]
