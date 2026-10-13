---
subject: Machine Learning
chapter: 07
tags: [ds, reinforcement-learning, policy-gradient, reinforce, actor-critic, advantage-function]
source: "lecture-7-policy-gradient-methods.pdf — David Silver, UCL (Lecture 7 of 10)"
---

# Policy Gradient Methods

[[06 - Value Function Approximation]] parameterized the value function and derived a policy from it. Here we parameterize the policy directly, $\pi_\theta(s,a)=\mathbb P[a\mid s,\theta]$, model-free. This addresses two problems left open: the discontinuous argmax (chattering) and continuous actions, where $\max_a$ is impractical.

## 📘 Main Knowledge

| | Value function | Policy |
|---|---|---|
| value-based | learned | implicit (e.g. ε-greedy) |
| policy-based | none | learned |
| actor-critic | learned | learned |

**Advantages**: better convergence (the policy changes smoothly with θ), works in high-dimensional or continuous action spaces (a Gaussian policy just outputs a mean), can learn stochastic policies. **Disadvantages**: usually converges to a local optimum; evaluating a policy is inefficient and high-variance.

### Stochastic policies

**Rock–paper–scissors**: a deterministic policy is exploited; the uniform random policy is the Nash equilibrium.

**Aliased gridworld**: the agent can't tell the two grey states apart (features like $\phi(s,a)=\mathbb 1(\text{wall to N},a=\text{E})$). A deterministic policy moves W in both or E in both and can get stuck; value-based RL learns a near-deterministic policy and wanders the corridor. The optimal stochastic policy moves E or W with probability 0.5 each in grey states and reaches the goal in a few steps with high probability. Aliasing makes the problem partially observable, so the deterministic-optimal-policy theorem of [[02 - Markov Decision Processes]] doesn't apply.

### Objectives

| Setting | Objective |
|---|---|
| episodic: start value | $J_1(\theta)=V^{\pi_\theta}(s_1)$ |
| continuing: average value | $J_{avV}(\theta)=\sum_sd^{\pi_\theta}(s)V^{\pi_\theta}(s)$ |
| continuing: average reward per step | $J_{avR}(\theta)=\sum_sd^{\pi_\theta}(s)\sum_a\pi_\theta(s,a)\mathcal R^a_s$ |

$d^{\pi_\theta}$ is the stationary distribution under $\pi_\theta$. Maximizing $J$ is an optimization problem: without gradients (hill climbing, Nelder–Mead, genetic algorithms) or, more efficiently, with them (gradient ascent, conjugate gradient, quasi-Newton). The lecture uses gradients and the problem's sequential structure.

### Finite differences

$\Delta\theta=\alpha\nabla_\theta J(\theta)$, estimating each component by perturbation: $\frac{\partial J}{\partial\theta_k}\approx\frac{J(\theta+\epsilon u_k)-J(\theta)}{\epsilon}$. That takes $n$ evaluations for $n$ parameters: simple, noisy, inefficient, but works even for non-differentiable policies. **AIBO** (Kohl & Stone 2004): gait parameters were sent to the robot, which timed itself walking between landmarks and reported back; the physical dynamics can't be differentiated, so finite differences fit.

### Monte Carlo policy gradient

**Likelihood ratio trick**: for differentiable $\pi_\theta$,
$$\nabla_\theta\pi_\theta(s,a)=\pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a).$$
$\nabla_\theta\log\pi_\theta(s,a)$ is the **score function**. The trick turns a gradient into an expectation under $\pi_\theta$, which can be estimated by running the policy.

- **Softmax** (discrete): $\pi_\theta(s,a)\propto e^{\phi(s,a)^\top\theta}$, score $\phi(s,a)-\mathbb E_{\pi_\theta}[\phi(s,\cdot)]$.
- **Gaussian** (continuous): $a\sim\mathcal N(\mu(s),\sigma^2)$ with $\mu(s)=\phi(s)^\top\theta$, score $\frac{(a-\mu(s))\phi(s)}{\sigma^2}$.

Both are "feature minus expected feature".

**One-step MDP**: $s\sim d(s)$, reward $r=\mathcal R_{s,a}$, $J(\theta)=\sum_sd(s)\sum_a\pi_\theta(s,a)\mathcal R_{s,a}$, so
$$\nabla_\theta J(\theta)=\sum_sd(s)\sum_a\pi_\theta(s,a)\nabla_\theta\log\pi_\theta(s,a)\mathcal R_{s,a}=\mathbb E_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,r].$$

**Policy gradient theorem** (Sutton et al. 1999): for any differentiable policy and any of the three objectives,
$$\nabla_\theta J(\theta)=\mathbb E_{\pi_\theta}\big[\nabla_\theta\log\pi_\theta(s,a)\,Q^{\pi_\theta}(s,a)\big].$$
There is no term for how the policy changes the state distribution, so the gradient can be estimated from trajectories without a model.

**REINFORCE**: use the return $v_t$ as an unbiased sample of $Q^{\pi_\theta}(s_t,a_t)$:
```
function REINFORCE
    initialise θ arbitrarily
    for each episode {s1,a1,r2,…,s_{T-1},a_{T-1},r_T} ~ π_θ:
        for t = 1 to T-1:
            θ ← θ + α ∇_θ log π_θ(s_t,a_t) v_t
    return θ
```
Puck World: some runs converged to substantially suboptimal local optima.

### Actor-critic

MC policy gradient has high variance, so a **critic** estimates $Q_w(s,a)\approx Q^{\pi_\theta}(s,a)$. The critic updates $w$; the actor updates θ in the direction the critic suggests:
$$\nabla_\theta J(\theta)\approx\mathbb E_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\,Q_w(s,a)].$$
The critic solves policy evaluation, so MC, TD, TD(λ) and least squares (ch. 04, 06) all apply.

**QAC** with linear $Q_w(s,a)=\phi(s,a)^\top w$:
```
initialise s, θ; sample a ~ π_θ
for each step:
    sample r = R^a_s and s' ~ P^a_s·;  sample a' ~ π_θ(s',·)
    δ = r + γ Q_w(s',a') − Q_w(s,a)
    θ ← θ + α ∇_θ log π_θ(s,a) Q_w(s,a)
    w ← w + β δ φ(s,a)
    a ← a', s ← s'
```

**Compatible function approximation.** An approximate critic biases the gradient (with aliased features, could it still solve the gridworld?). **Theorem**: if (1) $\nabla_wQ_w(s,a)=\nabla_\theta\log\pi_\theta(s,a)$ and (2) $w$ minimizes $\varepsilon=\mathbb E_{\pi_\theta}[(Q^{\pi_\theta}(s,a)-Q_w(s,a))^2]$, the gradient is exact. Proof: at the minimum $\mathbb E[(Q^\theta-Q_w)\nabla_wQ_w]=0$; by (1) $\mathbb E[(Q^\theta-Q_w)\nabla_\theta\log\pi_\theta]=0$, so $\mathbb E[Q^\theta\nabla_\theta\log\pi_\theta]=\mathbb E[Q_w\nabla_\theta\log\pi_\theta]$.

**Baselines.** For any $B(s)$,
$$\mathbb E_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)B(s)]=\sum_sd^{\pi_\theta}(s)B(s)\nabla_\theta\sum_a\pi_\theta(s,a)=0,$$
so subtracting it leaves the expectation unchanged and can reduce variance. With $B(s)=V^{\pi_\theta}(s)$ you get the **advantage** $A^{\pi_\theta}(s,a)=Q^{\pi_\theta}(s,a)-V^{\pi_\theta}(s)$ and $\nabla_\theta J=\mathbb E[\nabla_\theta\log\pi_\theta\,A^{\pi_\theta}]$.

Estimating the advantage: two critics, $A=Q_w-V_v$; or the **TD error**. For the true $V^{\pi_\theta}$, $\delta^{\pi_\theta}=r+\gamma V^{\pi_\theta}(s')-V^{\pi_\theta}(s)$ satisfies $\mathbb E[\delta^{\pi_\theta}\mid s,a]=Q^{\pi_\theta}(s,a)-V^{\pi_\theta}(s)=A^{\pi_\theta}(s,a)$, so $\nabla_\theta J=\mathbb E[\nabla_\theta\log\pi_\theta\,\delta^{\pi_\theta}]$. In practice $\delta=r+\gamma V_v(s')-V_v(s)$, with one parameter vector.

**Targets at different time scales.** Critics: MC $v_t$, TD(0) $r+\gamma V(s')$, TD(λ). Actors: MC $\Delta\theta=\alpha(v_t-V_v(s_t))\nabla_\theta\log\pi_\theta$; TD $\Delta\theta=\alpha(r+\gamma V_v(s_{t+1})-V_v(s_t))\nabla_\theta\log\pi_\theta$; with traces, $e_{t+1}=\lambda e_t+\nabla_\theta\log\pi_\theta(s,a)$, $\Delta\theta=\alpha\delta e_t$ (as printed; with discounting the decay is γλ, as in ch. 04).

**Natural policy gradient.** The vanilla gradient depends on the parameterization (e.g. raising all softmax scores equally changes θ but not the policy). The natural gradient is the ascent direction closest to the vanilla gradient for a small fixed change in the policy:
$$\nabla^{nat}_\theta\pi_\theta(s,a)=G_\theta^{-1}\nabla_\theta\pi_\theta(s,a),\qquad G_\theta=\mathbb E_{\pi_\theta}[\nabla_\theta\log\pi_\theta\nabla_\theta\log\pi_\theta^\top],$$
with $G_\theta$ the Fisher information matrix ([[Mathematical Statistics/contents/05 - Point Estimation|Point Estimation]]). **Natural actor-critic**: with compatible $\nabla_wA_w(s,a)=\nabla_\theta\log\pi_\theta(s,a)$, $\nabla_\theta J=\mathbb E[\nabla_\theta\log\pi_\theta\nabla_\theta\log\pi_\theta^\top w]=G_\theta w$, so $\nabla^{nat}_\theta J=w$: move the actor in the direction of the critic's parameters. Snake robot: off-policy NAC 10/10 successful runs, mean episode length 20.6; on-policy NAC 7/10, 145.7.

### Summary of forms

| Algorithm | $\nabla_\theta J(\theta)=\mathbb E_{\pi_\theta}[\nabla_\theta\log\pi_\theta(s,a)\times\cdot]$ |
|---|---|
| REINFORCE | $v_t$ |
| Q actor-critic | $Q_w(s,a)$ |
| advantage actor-critic | $A_w(s,a)$ |
| TD actor-critic | $\delta$ |
| TD(λ) actor-critic | $\delta e$ |
| natural actor-critic | $G_\theta^{-1}\nabla_\theta J(\theta)=w$ |

Each gives a stochastic gradient ascent algorithm; they differ only in how $Q^{\pi_\theta}$ is estimated.

## ✏️ Exercises

**1.** (Aliased gridworld) Why does value-based RL fail and policy-based RL succeed? Relate this to the deterministic-optimal-policy theorem.

> [!example]- Solution
> The grey states share a feature vector, so they get the same $Q$ values and a greedy policy takes the same action in both, although they need opposite moves. It gets stuck; ε-greedy escapes only by accident and slowly. A policy network can learn P(E) = P(W) = 0.5 there, deliberately. The theorem assumes the agent sees the state; aliased features make it a POMDP. With real sensors and approximate features this is the usual situation, so stochastic policies can strictly beat deterministic ones.

**2.** Explain the likelihood ratio trick and why policy gradients rest on it.

> [!example]- Solution
> $\nabla\pi=\pi\nabla\log\pi$. Without it, $\nabla J=\sum_sd(s)\sum_a\nabla_\theta\pi_\theta(s,a)\mathcal R_{s,a}$ is weighted by $\nabla\pi$, not a probability, so it can't be sampled without the model. With it, π becomes the weight and the gradient is $\mathbb E_\pi[\nabla\log\pi\cdot r]$: average $\nabla\log\pi(s,a)\,r$ over samples from the running policy. It is model-free and on-policy, and the score has closed forms for softmax and Gaussian policies. The score points towards making the taken action more likely; multiplying by $r$ reinforces what worked. It is the same score function as in maximum likelihood.

**3.** Why does a baseline reduce variance without bias? Why the advantage?

> [!example]- Solution
> $B(s)$ factors out of the sum over actions, leaving $\nabla_\theta\sum_a\pi=\nabla_\theta1=0$. If every action in a state returns about +100, REINFORCE pushes all of them up; subtracting $V\approx100$ leaves the differences (+2, −3), which carry the signal. The advantage measures how much better than the policy's own average an action is (its mean under π is 0). The TD error estimates it without bias, so one critic $V_v$ suffices, and its δ serves both the critic and the actor: the basis of A2C/A3C. A baseline that depends on the action would introduce bias.

**4.** State the compatible function approximation theorem. What problem does it solve?

> [!example]- Solution
> Replacing $v_t$ by a learned $Q_w$ reduces variance but biases the gradient, possibly steering the actor wrong (aliased critic features). If $\nabla_wQ_w=\nabla_\theta\log\pi_\theta$ and $w$ minimizes the MSE, the gradient is exact (proof above). Condition 1 means $Q_w(s,a)=\nabla_\theta\log\pi_\theta(s,a)^\top w$: the critic must be linear in the score features (for softmax, $\phi(s,a)-\mathbb E[\phi]$). Its error may be large, but it is orthogonal to the score, the only direction the gradient uses. It also yields $\nabla^{nat}J=w$.

**5.** (Advanced) Compare value-based, policy-based and actor-critic methods.

> [!example]- Solution
> | | Value-based | Policy-based | Actor-critic |
> |---|---|---|---|
> | learns | $Q$ | π | both |
> | continuous actions | ✗ | ✓ | ✓ |
> | stochastic optimum | ✗ | ✓ | ✓ |
> | variance | low | high | medium |
> | bias | can diverge | unbiased (REINFORCE) | biased unless compatible |
> | data reuse | off-policy replay | on-policy | mostly on-policy |
> | convergence | chatters / diverges | smooth, local | local |
>
> Value-based fits few discrete actions and data reuse (DQN on Atari). Policy-based fits continuous or stochastic problems (TRPO, PPO). Actor-critic combines a critic that cuts variance with a smooth actor that avoids argmax jumps. The table of forms runs from unbiased high-variance ($v_t$) to lower-variance biased (δ, δe), like MC vs TD. Policy gradients are on-policy, so old data needs importance sampling; off-policy actor-critics (DDPG, SAC) and PPO's clipping address this.

## 📝 Summary

- Parameterize $\pi_\theta$ directly: smooth convergence, continuous actions, stochastic policies; but local optima and high variance.
- Stochastic optima: rock–paper–scissors, aliased gridworld.
- Objectives: start value, average value, average reward.
- Finite differences: $n$ evaluations, no gradient needed.
- Likelihood ratio: $\nabla\pi=\pi\nabla\log\pi$; score functions for softmax and Gaussian.
- Policy gradient theorem: $\nabla J=\mathbb E[\nabla\log\pi\,Q^\pi]$, no state-distribution term.
- REINFORCE uses returns; actor-critic adds a critic.
- Compatible approximation makes the gradient exact.
- Baselines are free; $V^\pi$ gives the advantage; the TD error estimates it.
- Natural gradient = Fisher-preconditioned; with compatible features it equals $w$.

## ⚠️ Important Notes

1. Greedy value-based policies can't represent stochastic optima.
2. Aliasing breaks the deterministic-policy theorem.
3. ε-greedy noise is not a learned stochastic policy.
4. The likelihood ratio trick is what makes the gradient samplable.
5. The policy gradient theorem has no $\nabla d^\pi$ term.
6. REINFORCE: unbiased, high variance, local optima.
7. Baselines must not depend on the action.
8. Actor-critic is biased unless compatible.
9. Compatibility fixes the critic's features.
10. Policy gradients are on-policy.
11. The vanilla gradient depends on parameterization; the natural gradient doesn't.
12. High variance forces small steps (hence TRPO/PPO limit steps in policy space).

> [!warning] Gaps in the source slides
> - Slide 20's statement of the policy gradient theorem is cut off before the equation; the standard form (Sutton et al. 1999) is given. Check against the PDF.
> - Images: slides 4, 7–9 (aliased gridworld), 12; slides 14–15 (AIBO), 22 (Puck World), 38–40 (snake robot) are extracts from cited papers, with figures as images (the NAC table survives).
> - Truncated: slides 10, 11, 13, 21, 23, 25 (QAC pseudocode, completed), 26–32, 34, 41.
> - The actor trace on slide 34 decays by λ only, without γ.
> - References: Sutton, McAllester, Singh & Mansour (NIPS 1999); Kakade (2002); Peters & Schaal (natural actor-critic); Kohl & Stone (2004).

**Previous:** [[06 - Value Function Approximation]] · **Next:** [[08 - Integrating Learning and Planning]]
