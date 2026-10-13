---
subject: Machine Learning
chapter: 04
tags: [ds, reinforcement-learning, monte-carlo, temporal-difference, td-lambda, eligibility-traces]
source: "lecture-4-model-free-prediction-.pdf — David Silver, UCL (Lecture 4 of 10)"
---

# Model-Free Prediction

From planning to learning. Last lecture solved a known MDP ([[03 - Planning by Dynamic Programming]]); this one estimates the value function of an **unknown** MDP; the next optimizes it ([[05 - Model-Free Control]]).

## 📘 Main Knowledge

### Monte Carlo learning

MC learns from complete episodes, without a model and without bootstrapping, using the simplest idea: **value = mean return**. It only works for episodic MDPs (every episode must end).

Goal: learn $v_\pi$ from episodes $S_1,A_1,R_2,\dots,S_k\sim\pi$, where $G_t=R_{t+1}+\gamma R_{t+2}+\dots+\gamma^{T-1}R_T$ and $v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]$. MC uses the empirical mean return instead of the expected return.

- **First-visit MC**: at the first visit to $s$ in an episode, $N(s)\mathrel{+}=1$, $S(s)\mathrel{+}=G_t$, $V(s)=S(s)/N(s)$. By the law of large numbers $V(s)\to v_\pi(s)$.
- **Every-visit MC**: the same at every visit; also converges.

**Blackjack**: 200 states (sum 12–21 × dealer card ace–10 × usable ace or not); actions stick or twist; stick gives +1, 0, −1 against the dealer; twist gives −1 if bust, else 0. Evaluated policy: stick on 20 or 21. Writing the transition model is hard, sampling a hand is easy: the model-free advantage.

**Incremental mean**: $\mu_k=\mu_{k-1}+\frac1k(x_k-\mu_{k-1})$. So after each episode, $N(S_t)\mathrel{+}=1$, $V(S_t)\leftarrow V(S_t)+\frac1{N(S_t)}(G_t-V(S_t))$. For non-stationary problems use a constant step to forget old episodes:
$$V(S_t)\leftarrow V(S_t)+\alpha\big(G_t-V(S_t)\big).$$

### Temporal-difference learning

TD learns from incomplete episodes by **bootstrapping**: it updates a guess towards a guess.
$$\text{MC: }V(S_t)\leftarrow V(S_t)+\alpha(G_t-V(S_t))\qquad\text{TD(0): }V(S_t)\leftarrow V(S_t)+\alpha\big(R_{t+1}+\gamma V(S_{t+1})-V(S_t)\big)$$
$R_{t+1}+\gamma V(S_{t+1})$ is the **TD target**, $\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t)$ the **TD error**. The target is the Bellman equation's right-hand side with one sampled transition instead of the model's expectation.

**Driving home**:

| State | Elapsed | Predicted to go | Predicted total |
|---|---|---|---|
| leaving office | 0 | 30 | 30 |
| reach car, raining | 5 | 35 | 40 |
| exit highway | 20 | 15 | 35 |
| behind truck | 30 | 10 | 40 |
| home street | 40 | 3 | 43 |
| arrive home | 43 | 0 | 43 |

MC moves every prediction towards the final 43 once home. TD moves each prediction towards the next one immediately: when it starts raining, the office estimate moves towards 40 at once.

**MC vs TD**: TD can learn before the outcome (online, every step) and without it (incomplete sequences), and works in continuing tasks; MC needs complete episodes.

**Bias and variance**: $G_t$ is an unbiased estimate of $v_\pi(S_t)$, and so is the true TD target $R_{t+1}+\gamma v_\pi(S_{t+1})$. The actual TD target uses $V$, so it is biased, but its variance is much lower: one random action, transition and reward instead of many.

| MC | TD |
|---|---|
| high variance, zero bias | low variance, some bias |
| converges well, even with function approximation | usually more efficient; TD(0) converges to $v_\pi$, but not always with function approximation |
| insensitive to initial values | more sensitive to initial values |

### Batch MC and TD: the AB example

Two states A, B, no discounting, 8 episodes: `A,0,B,0`; six times `B,1`; once `B,0`. Both methods give $V(B)=6/8=0.75$; they disagree on $V(A)$ (Exercise 2).

- Batch **MC** converges to the minimum mean-squared-error fit to observed returns, $\sum_k\sum_t(G^k_t-V(s^k_t))^2$: $V(A)=0$.
- Batch **TD(0)** converges to the value of the maximum-likelihood Markov model, with $\hat{\mathcal P}^a_{ss'}$ the observed transition frequencies and $\hat{\mathcal R}^a_s$ the observed mean rewards: $V(A)=0.75$.

TD exploits the Markov property and is usually more efficient in Markov environments; MC is usually better in non-Markov environments.

### Unified view

| | Bootstraps | Samples | Backup |
|---|---|---|---|
| DP | ✓ | ✗ | shallow, full-width |
| MC | ✗ | ✓ | deep, sampled |
| TD | ✓ | ✓ | shallow, sampled |
| exhaustive search | ✗ | ✗ | deep, full-width |

### TD(λ)

**n-step returns**: $G^{(n)}_t=R_{t+1}+\gamma R_{t+2}+\dots+\gamma^{n-1}R_{t+n}+\gamma^nV(S_{t+n})$, with $V(S_t)\leftarrow V(S_t)+\alpha(G^{(n)}_t-V(S_t))$. $n=1$ is TD, $n=\infty$ is MC; intermediate $n$ often does better than both.

**λ-return** (forward view): average all $n$-step returns with weights $(1-\lambda)\lambda^{n-1}$ (summing to 1):
$$G^\lambda_t=(1-\lambda)\sum_{n=1}^\infty\lambda^{n-1}G^{(n)}_t,\qquad V(S_t)\leftarrow V(S_t)+\alpha(G^\lambda_t-V(S_t)).$$
λ = 0 gives TD(0), λ = 1 gives MC. Like MC, it needs complete episodes.

**Eligibility traces** (backward view): the forward view is the theory, the backward view the mechanism, which updates online from incomplete sequences. Credit assignment ("did the bell or the light cause the shock?") uses a frequency heuristic and a recency heuristic; the trace combines them:
$$E_0(s)=0,\qquad E_t(s)=\gamma\lambda E_{t-1}(s)+\mathbb 1(S_t=s).$$
Each step, every state is updated in proportion to the TD error and its trace:
$$V(s)\leftarrow V(s)+\alpha\,\delta_t\,E_t(s).$$

At λ = 0 only the current state has a trace, giving TD(0). At λ = 1, over an episode the total TD(1) update equals the MC update.

**Theorem**: the sums of offline updates are identical for forward and backward TD(λ):
$$\sum_{t=1}^T\alpha\delta_tE_t(s)=\sum_{t=1}^T\alpha(G^\lambda_t-V(S_t))\mathbb 1(S_t=s).$$
At λ = 1 the TD errors telescope:
$$\delta_t+\gamma\delta_{t+1}+\dots+\gamma^{T-1-t}\delta_{T-1}=R_{t+1}+\gamma R_{t+2}+\dots+\gamma^{T-1-t}R_T-V(S_t)=G_t-V(S_t),$$
because each $+\gamma^kV(S_{t+k})$ cancels the next line's $-\gamma^kV(S_{t+k})$. For general λ, $(\gamma\lambda)^k$ replaces $\gamma^k$.

| | λ = 0 | 0 < λ < 1 | λ = 1 |
|---|---|---|---|
| offline: backward = forward? | = TD(0) | = forward TD(λ) | = MC |
| online: backward = forward? | = | ≠ | ≠ |

**Exact online TD(λ)** (Sutton & van Seijen, ICML 2014) uses a modified trace and achieves exact equivalence online.

## ✏️ Exercises

**1.** What does "TD updates a guess towards a guess" mean? Why does bootstrapping add bias but reduce variance?

> [!example]- Solution
> The target $R_{t+1}+\gamma V(S_{t+1})$ contains another estimate. If $V(S_{t+1})$ is wrong (it starts as an arbitrary initial value), the target is systematically wrong: bias. But $G_t$ depends on every later action, transition and reward, while the TD target depends on one of each. In the driving example the MC target is whatever today's trip took (35, 43, 60 minutes…), the TD target 5 + 35 = 40.
> Bias shrinks as $V$ improves; variance from the environment doesn't. So TD is usually more efficient, but more sensitive to initialization, and with function approximation bootstrapping can diverge ([[06 - Value Function Approximation]]).

**2.** (AB example) Find batch MC and batch TD(0) values of $V(A)$. Why do they differ, and which is right?

> [!example]- Solution
> $V(B)=6/8=0.75$ for both.
> MC: A appears once, with return 0 + 0 = 0, so $V(A)=0$ (the best fit to observed returns).
> TD: the fitted Markov model says A → B with probability 1 and reward 0, so $V(A)=0+V(B)=0.75$, using what seven other episodes say about B.
> If the environment is Markov, TD is right and the A episode was unlucky. If not (the B reached from A behaves differently), MC's refusal to infer is safer.

**3.** Explain the unified view. Where does exhaustive search fit?

> [!example]- Solution
> Bootstrapping: does the update use an estimate? Sampling: does it use samples instead of the full expectation? Exhaustive search does neither: it expands every branch to termination, exact and almost always infeasible.
> Sampling makes backups constant-cost and model-free; bootstrapping removes the dependence on episode length (continuing tasks). TD has both; its price is bias and instability under approximation. TD(λ) is a dial on the depth axis, and the best setting is usually between the ends.

**4.** Show that the eligibility-trace update reduces to TD(0) at λ = 0, and explain the two heuristics.

> [!example]- Solution
> With λ = 0, $E_t(s)=\mathbb 1(S_t=s)$, so only $S_t$ changes: $V(S_t)\leftarrow V(S_t)+\alpha\delta_t$, which is TD(0).
> Recency: the decay $\gamma\lambda E_{t-1}$ shrinks old credit. Frequency: each visit adds 1. Recency alone credits only the last state; frequency alone ignores timing; the trace combines them. γ is in the decay because credit should fall at the same rate as the discount on the reward being credited. The backward view stores one number per state and updates everything from one TD error, so it runs online.

**5.** (Advanced) Explain the telescoping proof of forward/backward equivalence. Why does it hold offline but not online?

> [!example]- Solution
> Writing $\delta_t,\gamma\delta_{t+1},\gamma^2\delta_{t+2},\dots$ in a column, each $+\gamma^kV(S_{t+k})$ cancels the next line's $-\gamma^kV(S_{t+k})$, leaving $G_t-V(S_t)$, the MC error (or $G^\lambda_t-V(S_t)$ with $(\gamma\lambda)^k$).
> Offline, updates are applied at the end of the episode, so every $V$ in the δ's is the same frozen value and the cancellation is exact. Online, $V(S_{t+1})$ changes between $\delta_t$ and $\delta_{t+1}$, so the terms no longer cancel. The gap is small for small α; exact online TD(λ) removes it.

## 📝 Summary

- Model-free prediction estimates $v_\pi$ from experience alone.
- MC: mean of complete returns; episodic tasks only; first- and every-visit both converge.
- Constant α forgets old episodes (non-stationary problems).
- TD(0): target $R_{t+1}+\gamma V(S_{t+1})$; online, incomplete episodes, continuing tasks.
- MC: unbiased, high variance; TD: biased, low variance, usually more efficient.
- Batch MC fits returns; batch TD fits the maximum-likelihood Markov model.
- DP bootstraps, MC samples, TD does both.
- n-step and λ-returns interpolate between TD and MC.
- Eligibility traces combine recency and frequency; forward and backward views agree offline.

## ⚠️ Important Notes

1. MC needs episodes that terminate.
2. TD's bias shrinks as $V$ improves; MC's variance doesn't.
3. Constant-α MC tracks change but no longer converges to the exact mean.
4. Batch MC and TD answer differently on the same data; neither is a bug.
5. TD's advantage assumes the Markov property.
6. Bootstrapping with function approximation can diverge.
7. TD is more sensitive to initial values.
8. The best n or λ is usually in between.
9. The forward view can't run online.
10. Equivalence is exact only for offline updates (or exact online TD(λ)).
11. Traces decay by γλ, not λ.

> [!warning] Gaps in the source slides
> - Images: slide 9 (Blackjack value surfaces), 15 (driving home MC vs TD plots; the table on slide 14 survives), 19–20, 33, 38 (random-walk learning curves comparing n and λ), 26–28, 30 (backup diagrams and the unified-view figure, rebuilt as a table), 31, 36.
> - Truncated: slide 8 (twist reward, completed as "−1 if the sum exceeds 21"), 13, 16, 24 ($\hat{\mathcal R}$ formula), 34, 47, 48 (the trace rule for repeated visits).
> - Slides 22–23 extracted identically, so the AB answer slide's text is lost; the answers above are computed.
> - Reference: van Seijen & Sutton, *True Online TD(λ)*, ICML 2014.

**Previous:** [[03 - Planning by Dynamic Programming]] · **Next:** [[05 - Model-Free Control]]
