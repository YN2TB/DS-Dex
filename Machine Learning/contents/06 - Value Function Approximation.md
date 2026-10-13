---
subject: Machine Learning
chapter: 06
tags: [ds, reinforcement-learning, function-approximation, dqn, deadly-triad, lstd]
source: "lecture-6-value-function-approximation-.pdf — David Silver, UCL (Lecture 6 of 10)"
---

# Value Function Approximation

Part II, RL in practice. Part I used a lookup table with one entry per state; this lecture drops that, which makes RL usable on real problems and brings new instabilities.

## 📘 Main Knowledge

### Why approximate

Backgammon has about $10^{20}$ states, Go about $10^{170}$, a helicopter a continuous state space. Tables need too much memory, and learning each state separately is too slow. Instead estimate
$$\hat v(s,\mathbf w)\approx v_\pi(s)\quad\text{or}\quad\hat q(s,a,\mathbf w)\approx q_\pi(s,a),$$
which **generalizes** from seen to unseen states. Architectures: state → $\hat v$; state and action → $\hat q$; state → $\hat q$ for every action (one pass gives all action values, as in DQN).

Approximators: linear features, neural networks, decision trees, nearest neighbours, Fourier/wavelet bases. The lecture uses differentiable ones (linear, neural) and needs training methods that cope with non-stationary, non-i.i.d. data.

### Incremental methods

Gradient descent moves against the gradient, $\Delta\mathbf w=-\frac12\alpha\nabla_{\mathbf w}J(\mathbf w)$. With $J(\mathbf w)=\mathbb E_\pi[(v_\pi(S)-\hat v(S,\mathbf w))^2]$, stochastic gradient descent samples:
$$\Delta\mathbf w=\alpha\big(v_\pi(S)-\hat v(S,\mathbf w)\big)\nabla_{\mathbf w}\hat v(S,\mathbf w).$$

**Linear approximation**: features $\mathbf x(S)$ (distances to landmarks, market trends, chess piece configurations), $\hat v(S,\mathbf w)=\mathbf x(S)^\top\mathbf w$. The objective is quadratic, so SGD reaches the global optimum, and
$$\Delta\mathbf w=\alpha\big(v_\pi(S)-\hat v(S,\mathbf w)\big)\mathbf x(S):$$
step size × prediction error × feature value.

**Table lookup** is linear approximation with one-hot features $\mathbf x(S)=(\mathbb 1(S=s_1),\dots,\mathbb 1(S=s_n))^\top$, so $\hat v(s_i)=w_i$.

**Targets**: there is no supervisor, so substitute one for $v_\pi$:

| Method | Target |
|---|---|
| MC | $G_t$ (unbiased, noisy) |
| TD(0) | $R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w)$ (biased) |
| TD(λ) | $G^\lambda_t$ |

with $\Delta\mathbf w=\alpha(\text{target}-\hat v(S_t,\mathbf w))\nabla_{\mathbf w}\hat v(S_t,\mathbf w)$. MC is supervised learning on $\langle S_t,G_t\rangle$ and converges to a local optimum, even with non-linear approximation. Linear TD(0), $\Delta\mathbf w=\alpha\delta\,\mathbf x(S)$, converges close to the global optimum. Backward linear TD(λ): $E_t=\gamma\lambda E_{t-1}+\mathbf x(S_t)$, $\Delta\mathbf w=\alpha\delta_tE_t$; the trace is over features.

The TD target contains $\hat v(S_{t+1},\mathbf w)$, which depends on the parameters being updated, and TD ignores that dependence. It is a **semi-gradient** method.

**Control**: approximate evaluation $\hat q(\cdot,\cdot,\mathbf w)\approx q_\pi$ plus ε-greedy improvement. Linear: $\hat q(S,A,\mathbf w)=\mathbf x(S,A)^\top\mathbf w$, $\Delta\mathbf w=\alpha(\text{target}-\hat q)\mathbf x(S,A)$, with targets $G_t$, $R_{t+1}+\gamma\hat q(S_{t+1},A_{t+1},\mathbf w)$ (Sarsa) or the action-value λ-return. Example: Mountain Car with coarse coding and radial basis functions, and a study of λ ("should we bootstrap?").

### Convergence

**Baird's counterexample**: off-policy TD with linear approximation can make the parameters grow without bound.

Prediction (✓ converges, ✗ may not):

| | Algorithm | Table | Linear | Non-linear |
|---|---|---|---|---|
| on-policy | MC | ✓ | ✓ | ✓ |
| | TD(0), TD(λ) | ✓ | ✓ | ✗ |
| | Gradient TD | ✓ | ✓ | ✓ |
| off-policy | MC | ✓ | ✓ | ✓ |
| | TD(0), TD(λ) | ✓ | ✗ | ✗ |
| | Gradient TD | ✓ | ✓ | ✓ |

TD does not follow the gradient of any objective function, which is why it can diverge off-policy or with non-linear approximation. **Gradient TD** follows the true gradient of the projected Bellman error and converges.

Control:

| Algorithm | Table | Linear | Non-linear |
|---|---|---|---|
| MC control | ✓ | (✓) | ✗ |
| Sarsa | ✓ | (✓) | ✗ |
| Q-learning | ✓ | ✗ | ✗ |
| Gradient Q-learning | ✓ | ✓ | ✗ |

(✓) = chatters around the near-optimal value function.

### Batch methods

Gradient descent uses each transition once, which is not sample efficient. Batch methods find the best-fitting value function for all experience.

**Least squares**: given $\mathcal D=\{\langle s_t,v^\pi_t\rangle\}$, minimize $LS(\mathbf w)=\sum_t(v^\pi_t-\hat v(s_t,\mathbf w))^2$. SGD with **experience replay** (sample $\langle s,v^\pi\rangle$ from $\mathcal D$, update) converges to the least-squares solution.

**DQN** uses experience replay and fixed Q-targets: act ε-greedily; store $(s_t,a_t,r_{t+1},s_{t+1})$ in $\mathcal D$; sample a random mini-batch; compute Q-learning targets with old fixed parameters $\mathbf w^-$; minimize
$$\mathcal L_i(\mathbf w_i)=\mathbb E_{s,a,r,s'\sim\mathcal D_i}\Big[\big(r+\gamma\max_{a'}Q(s',a';\mathbf w_i^-)-Q(s,a;\mathbf w_i)\big)^2\Big].$$
In Atari: Q learned end to end from pixels (the last 4 frames), outputs for 18 joystick/button positions, reward = change in score, one architecture and set of hyperparameters for all games.

| Mean score | Replay + fixed Q | Replay only | Fixed Q only | Neither |
|---|---|---|---|---|
| Breakout | 316.81 | 240.73 | 10.16 | 3.17 |
| Enduro | 1006.3 | 831.25 | 141.89 | 29.1 |
| River Raid | 7446.62 | 4102.81 | 2867.66 | 1453.02 |
| Seaquest | 2894.4 | 822.55 | 1003 | 275.81 |
| Space Invaders | 1088.94 | 826.33 | 373.22 | 301.99 |

**Linear least squares directly**: at the minimum the expected update is zero, $\sum_t\mathbf x(s_t)(v^\pi_t-\mathbf x(s_t)^\top\mathbf w)=0$, so
$$\mathbf w=\Big(\sum_t\mathbf x(s_t)\mathbf x(s_t)^\top\Big)^{-1}\sum_t\mathbf x(s_t)v^\pi_t.$$
For $N$ features: $O(N^3)$ directly, $O(N^2)$ incrementally with Sherman–Morrison. Substituting targets:

| Algorithm | Solution |
|---|---|
| LSMC | $\mathbf w=(\sum\mathbf x(S_t)\mathbf x(S_t)^\top)^{-1}\sum\mathbf x(S_t)G_t$ |
| LSTD | $\mathbf w=(\sum\mathbf x(S_t)(\mathbf x(S_t)-\gamma\mathbf x(S_{t+1}))^\top)^{-1}\sum\mathbf x(S_t)R_{t+1}$ |
| LSTD(λ) | $\mathbf w=(\sum E_t(\mathbf x(S_t)-\gamma\mathbf x(S_{t+1}))^\top)^{-1}\sum E_tR_{t+1}$ |

LSMC and LSTD converge on-policy with linear approximation, and LSTD also converges off-policy.

**LSPI**: control experience comes from many policies, so evaluating $q_\pi$ must be off-policy (as in Q-learning, use the successor action the target policy would take). **LSTDQ**:
$$\mathbf w=\Big(\sum_t\mathbf x(S_t,A_t)\big(\mathbf x(S_t,A_t)-\gamma\mathbf x(S_{t+1},\pi(S_{t+1}))\big)^\top\Big)^{-1}\sum_t\mathbf x(S_t,A_t)R_{t+1}$$
```
function LSPI-TD(D, π0)
    π' ← π0
    repeat
        π ← π'
        Q ← LSTDQ(π, D)
        for all s: π'(s) ← argmax_a Q(s,a)
    until π ≈ π'
    return π
```
It re-evaluates the same experience $\mathcal D$ under each new policy. LSPI converges with chattering (✓) for linear approximation. Example: Chain Walk (Lagoudakis & Parr).

## ✏️ Exercises

**1.** Why is table lookup a special case of linear approximation, and what does that say about Part I?

> [!example]- Solution
> With one-hot features $\hat v(s_i)=w_i$, and the update changes only $w_i$: exactly the tabular rule. Part I's algorithms are linear approximation with non-overlapping features. That is why their convergence was clean: updating one state can't disturb another. It also shows the cost: no generalization, so every state must be visited. Overlapping features generalize but make updates interfere, which is where every divergence in this lecture comes from.

**2.** Explain the deadly triad using the convergence tables.

> [!example]- Solution
> Divergence needs function approximation, bootstrapping and off-policy learning together. MC (no bootstrapping) is ✓ everywhere; on-policy linear TD is ✓; tables are ✓; off-policy linear TD is ✗ (Baird).
> The TD target contains $\mathbf w$ but TD doesn't differentiate through it, so it minimizes no objective. With overlapping features, updating $\mathbf w$ for $s$ moves $\hat v(s')$, which moves the target for $s$: a feedback loop. On-policy, states are updated in the proportions they're visited, which keeps the loop in check; off-policy breaks that. Gradient TD restores convergence by descending a real objective. Q-learning with a neural network has all three ingredients, hence DQN's tricks.

**3.** Why is control harder than prediction under approximation? What does "chatters" mean?

> [!example]- Solution
> On-policy linear TD converges for prediction; linear Sarsa only chatters. The policy changes whenever $\mathbf w$ does, so the target moves; the greedy argmax is a step function, so tiny updates can flip actions and shift the state distribution; and with noisy $\hat q$, argmax favours overestimated actions, so the exact-$q$ improvement theorem no longer applies. "Chatters" means $\mathbf w$ keeps moving in a bounded region near the optimum while the policy switches among near-optimal choices: stable performance, not divergence. Q-learning (off-policy) is ✗ even with linear features. Remedies: decay ε and α, better features, or policy gradients ([[07 - Policy Gradient Methods]]).

**4.** Explain DQN's experience replay and fixed Q-targets, and read the ablation table.

> [!example]- Solution
> Replay trains on random mini-batches from memory: it breaks the correlation between consecutive frames, reuses each transition many times, and averages over past policies. Fixed targets compute $r+\gamma\max_{a'}Q(s',a';\mathbf w^-)$ with frozen $\mathbf w^-$, so each update is a regression towards a fixed target and the network stops chasing itself.
> Replay matters most: Breakout 316.81 or 240.73 with replay vs 10.16 or 3.17 without, about 31–100×. Fixed targets add more on top (316.81/240.73 = 1.32 on Breakout; 2894.4/822.55 = 3.5 on Seaquest) but help little without replay (10.16 vs 3.17). The two tricks complement each other.

**5.** (Advanced) Compare LSTD with incremental TD, and explain LSPI's advantage.

> [!example]- Solution
> Incremental TD: $O(N)$ per step and memory, needs a tuned α, uses each sample once, diverges off-policy. LSTD: solves the fixed point directly, no step size, uses all data at once, converges off-policy with linear features; but $O(N^2)$ memory and $O(N^2)$–$O(N^3)$ time, and linear only: hundreds of features, not millions of weights.
> LSPI evaluates each new policy on the same dataset, because LSTDQ uses $\hat q(S_{t+1},\pi(S_{t+1}))$ for the target policy's action (off-policy). On-policy Sarsa must collect new data after each change. When data are expensive (a real robot), LSPI can iterate offline on what it has.

## 📝 Summary

- Tables don't scale; approximation generalizes across states.
- Table lookup = linear approximation with one-hot features.
- Linear: update = α × error × features; global optimum for supervised targets.
- Targets: $G_t$ (MC), $R+\gamma\hat v$ (TD), $G^\lambda_t$.
- TD is semi-gradient and can diverge.
- Deadly triad: approximation + bootstrapping + off-policy.
- Gradient TD converges everywhere; linear Sarsa chatters; Q-learning can diverge.
- DQN = experience replay + fixed Q-targets.
- LSTD solves directly and converges off-policy; LSPI reuses one dataset.

## ⚠️ Important Notes

1. TD with approximation is not gradient descent.
2. To fix divergence, remove a leg of the triad.
3. Off-policy linear TD can explode, not just converge slowly.
4. Q-learning with a neural net has all three legs.
5. Replay is the bigger DQN trick; fixed targets help mostly on top of it.
6. Control is harder than prediction under approximation.
7. Chattering is not divergence.
8. argmax over noisy estimates favours overestimates (the origin of Double Q-learning).
9. LSTD's cost depends on features, not states.
10. LSPI's power comes from LSTDQ being off-policy.
11. Under approximation, traces are vectors over features.

> [!warning] Gaps in the source slides
> - The ✓/✗ marks in the convergence tables (slides 30–32, 46, 52) didn't extract. The tables above follow the standard results (Sutton & Barto ch. 11) and the slide text ("TD can diverge when off-policy or using non-linear function approximation"; "(✓) = chatters"). Check them against the PDF before an exam.
> - Images: slides 25–27 (Mountain Car: coarse coding and RBFs are named but not defined; the λ study is lost), 28–29 (Baird's counterexample), 7, 11, 21, 40 (DQN vs human chart), 47, 53–55 (Chain Walk).
> - Truncated: slides 6, 12, 14, 16–20, 24, 35, 38, 44, 48, 49; completed with the standard statements ("local optimum", "close to the global optimum").
> - References: Mnih et al., *Nature* 2015 (DQN); Lagoudakis & Parr, *JMLR* 2003 (LSPI).

**Previous:** [[05 - Model-Free Control]] · **Next:** [[07 - Policy Gradient Methods]]
