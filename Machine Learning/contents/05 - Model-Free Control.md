---
subject: Machine Learning
chapter: 05
tags: [ds, reinforcement-learning, sarsa, q-learning, epsilon-greedy, off-policy]
source: "lecture-5-model-free-control-.pdf — David Silver, UCL (Lecture 5 of 10)"
---

# Model-Free Control

The end of Part I. [[04 - Model-Free Prediction]] estimated $v_\pi$ without a model; here we optimize it. It is generalized policy iteration ([[03 - Planning by Dynamic Programming]]) with MC or TD as the evaluation step, and it produces Sarsa and Q-learning.

## 📘 Main Knowledge

Examples of MDPs: elevators, parallel parking, ship steering, bioreactors, helicopters, logistics, RoboCup, Quake, portfolios, protein folding, walking robots, Go. Usually either the model is unknown but experience can be sampled, or the model is known but too big to use except by sampling (Go's rules are known, but it has about $10^{170}$ states). Model-free control handles both.

- **On-policy**: learn about π from experience sampled from π ("learn on the job").
- **Off-policy**: learn about π from experience sampled from another policy μ ("look over someone's shoulder").

### On-policy Monte Carlo control

Greedy improvement over $V$ needs a model, $\pi'(s)=\arg\max_a\big(\mathcal R^a_s+\sum_{s'}\mathcal P^a_{ss'}V(s')\big)$; over $Q$ it doesn't, $\pi'(s)=\arg\max_aQ(s,a)$. So model-free control learns action values.

**Exploration problem**: two doors. Left gives 0 once; right gives +1, +3, +2, … Greedy picks right forever, but the left door was tried only once.

**ε-greedy**: with probability $1-\epsilon$ take the greedy action, otherwise a random one (of $m$):
$$\pi(a\mid s)=\begin{cases}\epsilon/m+1-\epsilon & a=\arg\max_{a'}Q(s,a')\\ \epsilon/m & \text{otherwise}\end{cases}$$

**Theorem**: the ε-greedy policy π′ with respect to $q_\pi$ improves on any ε-greedy π:
$$q_\pi(s,\pi'(s))=\frac\epsilon m\sum_aq_\pi(s,a)+(1-\epsilon)\max_aq_\pi(s,a)\ge\frac\epsilon m\sum_aq_\pi(s,a)+(1-\epsilon)\sum_a\frac{\pi(a\mid s)-\epsilon/m}{1-\epsilon}q_\pi(s,a)=v_\pi(s),$$
since the max is at least any weighted average (the weights $\frac{\pi(a\mid s)-\epsilon/m}{1-\epsilon}$ are non-negative and sum to 1). By the policy improvement theorem, $v_{\pi'}\ge v_\pi$.

**GLIE** (greedy in the limit with infinite exploration): every state–action pair is explored infinitely often, $N_k(s,a)\to\infty$, and the policy becomes greedy, $\pi_k(a\mid s)\to\mathbb 1(a=\arg\max_{a'}Q_k(s,a'))$. ε-greedy with $\epsilon_k=1/k$ is GLIE.

**GLIE MC control**: after episode $k$, for each $(S_t,A_t)$: $N\mathrel{+}=1$, $Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\frac1N(G_t-Q(S_t,A_t))$; then $\epsilon\leftarrow1/k$, $\pi\leftarrow\epsilon\text{-greedy}(Q)$. It converges to $q_*$. Improvement happens every episode, without full evaluation.

### Sarsa (on-policy TD)

TD has lower variance, works online and on incomplete sequences, so use it in the control loop and update every step:
$$Q(S,A)\leftarrow Q(S,A)+\alpha\big(R+\gamma Q(S',A')-Q(S,A)\big).$$
The name lists the ingredients $S,A,R,S',A'$; using the actual next action makes it on-policy. Evaluation by Sarsa and ε-greedy improvement alternate at every time step.

**Theorem**: Sarsa converges to $q_*$ given GLIE policies and **Robbins–Monro** step sizes, $\sum_t\alpha_t=\infty$ and $\sum_t\alpha_t^2<\infty$ (large enough in total to reach anywhere, shrinking fast enough to settle). $\alpha_t=1/t$ satisfies both; constant α fails the second and keeps tracking instead.

**Windy Gridworld**: −1 per step, undiscounted; an upward wind in some columns pushes the agent (Sutton & Barto Example 6.5).

**n-step Sarsa and Sarsa(λ)**, as in ch. 04 with $Q$:
$$q^{(n)}_t=R_{t+1}+\dots+\gamma^{n-1}R_{t+n}+\gamma^nQ(S_{t+n},A_{t+n}),\qquad q^\lambda_t=(1-\lambda)\sum_n\lambda^{n-1}q^{(n)}_t.$$
Backward view with one trace per state–action pair:
$$E_t(s,a)=\gamma\lambda E_{t-1}(s,a)+\mathbb 1(S_t=s,A_t=a),\quad \delta_t=R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t),\quad Q(s,a)\leftarrow Q(s,a)+\alpha\delta_tE_t(s,a).$$
After one successful episode in a gridworld, one-step Sarsa updates only the last action; Sarsa(λ) passes credit back along the whole path.

### Off-policy learning

Evaluate a target policy π while following a behaviour policy μ. Uses: learn from humans or other agents; reuse experience from old policies; learn the optimal policy while exploring; learn about several policies at once.

**Importance sampling**: $\mathbb E_{X\sim P}[f(X)]=\mathbb E_{X\sim Q}\big[\frac{P(X)}{Q(X)}f(X)\big]$.
- Off-policy MC multiplies ratios over the whole episode: $G^{\pi/\mu}_t=\prod_{k=t}^{T}\frac{\pi(A_k\mid S_k)}{\mu(A_k\mid S_k)}G_t$, then $V(S_t)\leftarrow V(S_t)+\alpha(G^{\pi/\mu}_t-V(S_t))$. It can't be used where μ is zero but π isn't, and its variance is huge.
- Off-policy TD needs one ratio: $V(S_t)\leftarrow V(S_t)+\alpha\big(\frac{\pi(A_t\mid S_t)}{\mu(A_t\mid S_t)}(R_{t+1}+\gamma V(S_{t+1}))-V(S_t)\big)$. Much lower variance: the policies only need to be similar over one step.

### Q-learning

Off-policy learning of $Q$ with no importance sampling: act with $A_{t+1}\sim\mu$, but update towards an alternative action $A'\sim\pi$:
$$Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\big(R_{t+1}+\gamma Q(S_{t+1},A')-Q(S_t,A_t)\big).$$
Let the target π be greedy in $Q$ and μ ε-greedy. Then $Q(S_{t+1},A')=\max_{a'}Q(S_{t+1},a')$:
$$Q(S,A)\leftarrow Q(S,A)+\alpha\big(R+\gamma\max_{a'}Q(S',a')-Q(S,A)\big).$$
**Theorem**: Q-learning control converges to $q_*$. Cliff Walking contrasts it with Sarsa (Exercise 4).

### Summary table

| Bellman equation | Full backup (DP) | Sample backup (TD) |
|---|---|---|
| expectation, $v_\pi$ | iterative policy evaluation | TD learning |
| expectation, $q_\pi$ | Q-policy iteration | Sarsa |
| optimality, $q_*$ | Q-value iteration | Q-learning |

$$V(S)\xleftarrow\alpha R+\gamma V(S'),\qquad Q(S,A)\xleftarrow\alpha R+\gamma Q(S',A'),\qquad Q(S,A)\xleftarrow\alpha R+\gamma\max_{a'}Q(S',a'),$$
where $x\xleftarrow\alpha y$ means $x\leftarrow x+\alpha(y-x)$; the DP versions replace the sample by $\mathbb E[\cdot\mid s]$ or $\mathbb E[\cdot\mid s,a]$. Across: sampling replaces the expectation (model-free). Down: the Bellman equation chosen (expectation gives Sarsa, optimality Q-learning).

## ✏️ Exercises

**1.** Why must model-free control learn $Q(s,a)$ rather than $V(s)$?

> [!example]- Solution
> Improving from $V$ needs the reward and next state of every untaken action, which is the model. $Q$ already contains the one-step lookahead, so improvement is a lookup. The cost: $|\mathcal S|\times|\mathcal A|$ entries instead of $|\mathcal S|$, and correspondingly more experience. Even with a model, $q$ makes the improvement step cheaper, hence Q-policy and Q-value iteration in the table.

**2.** Explain GLIE. What goes wrong if either condition fails?

> [!example]- Solution
> Without infinite exploration, some pairs are never updated and keep their initial values; in the two-doors example the left door might really average +5 and the agent would never know. Without greediness in the limit (ε fixed at 0.1), $Q$ converges but the agent keeps acting randomly 10% of the time and never follows the optimal policy. $\epsilon_k=1/k$ satisfies both because $\sum1/k$ diverges while $1/k\to0$, the same pattern as Robbins–Monro step sizes. In practice constant ε and α are common, giving up the guarantee in order to track a changing environment.

**3.** Why is off-policy MC with importance sampling impractical, off-policy TD workable, and Q-learning free of correction?

> [!example]- Solution
> Take π greedy and μ ε-greedy (ε = 0.1, 4 actions). μ takes the greedy action with probability 0.925 (ratio $1/0.925=1.08$); otherwise π's probability is 0 and the whole return is zeroed. Over 100 steps only $0.925^{100}\approx0.04\%$ of episodes survive, with huge weights. In general the product of many ratios has variance growing exponentially with episode length, and coverage ($\mu>0$ wherever $\pi>0$) is required.
> Off-policy TD uses one ratio, with bounded variance.
> Q-learning's target $\max_{a'}Q(S',a')$ reads stored values for any action without taking it; the only sampled quantity, $S'$, comes from $\mathcal P$, which doesn't depend on the policy. Nothing needs correcting.

**4.** (Cliff Walking) The shortest path runs along a cliff (falling: −100 and back to the start). Sarsa learns a safe path away from the edge, Q-learning the edge path, yet Sarsa earns more reward during learning. Why?

> [!example]- Solution
> Q-learning's max target learns $q_*$, the value of acting greedily, and the edge path is optimal for a greedy agent. Sarsa's target uses the action actually taken, so it learns the value of the ε-greedy policy, for which walking along the edge means occasionally stepping off. Both are correct about different policies.
> During learning, Q-learning falls off ε of the time; Sarsa avoids that. With ε = 0, Q-learning's path is better. Use Sarsa when exploration really happens and its costs are real (a physical robot), Q-learning when exploration is a training device you'll switch off (a simulator). Under GLIE, as ε → 0, Sarsa's answer approaches Q-learning's. (Sutton & Barto Example 6.6.)

**5.** (Advanced) Explain the six-cell table.

> [!example]- Solution
> Across: replacing $\mathbb E[\cdot]$ with one sampled transition at rate α makes the method model-free, makes backups $O(1)$ instead of $O(|\mathcal S|)$, and adds variance that α averages out.
> Down: row 1 → 2 switches from $v$ to $q$, needed for model-free improvement; row 2 → 3 switches from the expectation to the optimality equation ($Q(S',A')$ → $\max_{a'}Q(S',a')$), i.e. on-policy → off-policy.
> There is no sample-backup cell for the optimality equation in $v$: $\max_a(\mathcal R^a_s+\gamma\sum\mathcal P^a_{ss'}v(s'))$ needs the model to evaluate actions not taken, which again is why model-free control uses $q$.

## 📝 Summary

- Model-free control is needed for unknown models and for known models too big for DP.
- On-policy learns about the policy it follows; off-policy about another.
- Control learns $Q$: improving from $V$ needs a model.
- ε-greedy explores and still guarantees improvement.
- GLIE: infinite exploration and eventual greediness; GLIE MC control converges to $q_*$.
- Sarsa: $Q\xleftarrow\alpha R+\gamma Q(S',A')$, converges under GLIE + Robbins–Monro.
- Sarsa(λ): one trace per state–action pair.
- Importance sampling over an episode explodes; over one TD step it is manageable.
- Q-learning: $Q\xleftarrow\alpha R+\gamma\max_{a'}Q(S',a')$, off-policy, no correction, converges to $q_*$.

## ⚠️ Important Notes

1. Improving from $V$ requires a model.
2. Without exploration, untried actions keep their initial values.
3. GLIE needs both conditions.
4. Constant α tracks rather than converges.
5. Sarsa and Q-learning differ by one symbol and evaluate different policies.
6. Sarsa when exploration costs are real; Q-learning when exploration will be switched off.
7. Off-policy MC with importance sampling is practically unusable.
8. Importance sampling needs coverage.
9. Sarsa(λ) doubles storage (a trace per pair).
10. Q-learning's guarantee is tabular; with function approximation it can diverge ([[06 - Value Function Approximation]]).

> [!warning] Gaps in the source slides
> - The pseudocode boxes for Sarsa, Sarsa(λ) and Q-learning (slides 22, 29, 38) are images; full listings are in Sutton & Barto ch. 6–7.
> - Images: slides 17–18 (Blackjack control results), 24–25 (Windy Gridworld layout and curve), 30 (Sarsa(λ) gridworld comparison), 40 (Cliff Walking), 6–9, 13–14, 21 (GPI diagrams), 20, 37, 41 (backup diagrams); slide 39 ("Q-Learning Demo") is a title.
> - Truncated: slide 4, slide 28 (the Sarsa(λ) update), slide 33 (completed as "cannot use if μ is zero when π is non-zero").

**Previous:** [[04 - Model-Free Prediction]] · **Next:** [[06 - Value Function Approximation]]
