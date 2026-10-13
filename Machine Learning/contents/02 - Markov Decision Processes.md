---
subject: Machine Learning
chapter: 02
tags: [ds, reinforcement-learning, mdp, bellman-equation, value-function, markov]
source: "lecture-2-mdp.pdf — David Silver, UCL (Lecture 2 of 10)"
---

# Markov Decision Processes

The mathematical base of the course: every later algorithm solves the Bellman equations defined here. The lecture builds Markov process → Markov reward process → Markov decision process, adding one ingredient at a time.

MDPs describe fully observable environments (the current state characterizes the process). Almost all RL problems can be cast as MDPs: optimal control uses continuous MDPs, partially observable problems can be converted, and bandits are one-state MDPs.

## 📘 Main Knowledge

### Markov processes

A state is **Markov** iff $\mathbb P[S_{t+1}\mid S_t]=\mathbb P[S_{t+1}\mid S_1,\dots,S_t]$. The **transition matrix** $\mathcal P_{ss'}=\mathbb P[S_{t+1}=s'\mid S_t=s]$ has rows summing to 1. A **Markov process** (chain) $\langle\mathcal S,\mathcal P\rangle$ is a memoryless random sequence of states, with no rewards or actions ([[Probability Theory/contents/00-Index|Probability Theory]]).

**Student Markov chain** (states C1, C2, C3, Pass, Pub, FB, Sleep):

| from \ to | C1 | C2 | C3 | Pass | Pub | FB | Sleep |
|---|---|---|---|---|---|---|---|
| C1 | | 0.5 | | | | 0.5 | |
| C2 | | | 0.8 | | | | 0.2 |
| C3 | | | | 0.6 | 0.4 | | |
| Pass | | | | | | | 1.0 |
| Pub | 0.2 | 0.4 | 0.4 | | | | |
| FB | 0.1 | | | | | 0.9 | |
| Sleep | | | | | | | 1 |

Sample episodes from C1: `C1 C2 C3 Pass Sleep`; `C1 FB FB C1 C2 Sleep`; `C1 C2 C3 Pub C2 C3 Pass Sleep`; … Sleep is absorbing; FB's 0.9 self-loop is a trap.

### Markov reward processes

An **MRP** $\langle\mathcal S,\mathcal P,\mathcal R,\gamma\rangle$ adds rewards $\mathcal R_s=\mathbb E[R_{t+1}\mid S_t=s]$ and a discount $\gamma\in[0,1]$. Student rewards: classes −2, FB −1, Pub +1, Pass +10, Sleep 0.

**Return**: $G_t=R_{t+1}+\gamma R_{t+2}+\dots=\sum_{k\ge0}\gamma^kR_{t+k+1}$, a random variable. A reward after $k+1$ steps is worth $\gamma^kR$; γ near 0 is myopic, near 1 far-sighted.

Why discount: mathematical convenience; avoids infinite returns in cyclic processes; future uncertainty; interest on money; humans and animals prefer immediate reward. Undiscounted MRPs are possible when all sequences terminate.

**Value function**: $v(s)=\mathbb E[G_t\mid S_t=s]$. Sample returns from C1 with γ = ½: −2.25, −3.125, −3.41, −3.20 for the four episodes; $v(\text{C1})$ is their expectation.

| State | γ = 0 | γ = 0.9 | γ = 1 |
|---|---|---|---|
| C1 | −2 | −5.0 | −13 (−12.54) |
| C2 | −2 | 0.9 | 1.5 |
| C3 | −2 | 4.1 | 4.3 |
| Pass | 10 | 10 | 10 |
| Pub | 1 | 1.9 | 0.8 |
| FB | −1 | −7.6 | −23 (−22.54) |
| Sleep | 0 | 0 | 0 |

(Brackets: exact values; the slide rounds to integers.) At γ = 0 values are immediate rewards; at γ = 1, FB's value reflects the expected 10 steps stuck in the loop.

### Bellman equation for MRPs

$$v(s)=\mathbb E[R_{t+1}+\gamma G_{t+1}\mid S_t=s]=\mathbb E[R_{t+1}+\gamma v(S_{t+1})\mid S_t=s]=\mathcal R_s+\gamma\sum_{s'}\mathcal P_{ss'}v(s')$$
Value = immediate reward + discounted value of the successor. Check (γ = 1, C3): $-2+0.6(10)+0.4(0.8)=4.32$.

Matrix form $v=\mathcal R+\gamma\mathcal Pv$ is linear, so $v=(I-\gamma\mathcal P)^{-1}\mathcal R$: $O(n^3)$, practical only for small MRPs. Large ones use dynamic programming ([[03 - Planning by Dynamic Programming]]), Monte Carlo and TD ([[04 - Model-Free Prediction]]).

### Markov decision processes

An **MDP** $\langle\mathcal S,\mathcal A,\mathcal P,\mathcal R,\gamma\rangle$ adds actions: $\mathcal P^a_{ss'}=\mathbb P[S_{t+1}=s'\mid S_t=s,A_t=a]$, $\mathcal R^a_s=\mathbb E[R_{t+1}\mid S_t=s,A_t=a]$.

Student MDP (γ = 1):

| State | Action → reward, next state |
|---|---|
| FB | Facebook → −1, FB; Quit → 0, C1 |
| C1 | Facebook → −1, FB; Study → −2, C2 |
| C2 | Sleep → 0, end; Study → −2, C3 |
| C3 | Study → +10, end; Pub → +1, then C1/C2/C3 with 0.2/0.4/0.4 |

A **policy** $\pi(a\mid s)=\mathbb P[A_t=a\mid S_t=s]$ fully defines behaviour. MDP policies depend on the current state only and are stationary.

**A fixed policy turns an MDP into an MRP**:
$$\mathcal P^\pi_{ss'}=\sum_a\pi(a\mid s)\mathcal P^a_{ss'},\qquad \mathcal R^\pi_s=\sum_a\pi(a\mid s)\mathcal R^a_s$$
So evaluating a policy is solving an MRP.

**Value functions**: $v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]$; $q_\pi(s,a)=\mathbb E_\pi[G_t\mid S_t=s,A_t=a]$ (take $a$, then follow π). For the uniform random policy: FB −2.3, C1 −1.3, C2 2.7, C3 7.4.

### Bellman expectation equations

$$v_\pi(s)=\sum_a\pi(a\mid s)\,q_\pi(s,a),\qquad q_\pi(s,a)=\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_\pi(s')$$
Substituting:
$$v_\pi(s)=\sum_a\pi(a\mid s)\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_\pi(s')\Big),\qquad q_\pi(s,a)=\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}\sum_{a'}\pi(a'\mid s')q_\pi(s',a')$$
Check (C3, uniform): $0.5\big(1+0.2(-1.3)+0.4(2.7)+0.4(7.4)\big)+0.5(10)=7.39$. Matrix form: $v_\pi=(I-\gamma\mathcal P^\pi)^{-1}\mathcal R^\pi$.

### Optimality

$v_*(s)=\max_\pi v_\pi(s)$, $q_*(s,a)=\max_\pi q_\pi(s,a)$: the best possible performance. An MDP is **solved** when $v_*$ is known. Student MDP: $v_*$ = FB 6, C1 6, C2 8, C3 10.

Order policies by $\pi\ge\pi'$ iff $v_\pi(s)\ge v_{\pi'}(s)$ for all $s$. **Theorem**: every MDP has an optimal policy $\pi_*\ge\pi$ for all π, and all optimal policies achieve $v_*$ and $q_*$. Acting greedily on $q_*$ is optimal, so there is always a **deterministic** optimal policy, and knowing $q_*$ gives it immediately.

### Bellman optimality equations

$$v_*(s)=\max_a\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_*(s')\Big),\qquad q_*(s,a)=\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}\max_{a'}q_*(s',a')$$
Check (C1): $v_*=\max\{-2+8,\,-1+6\}=6$.

The max makes these **non-linear** with no closed form in general, so they are solved iteratively: value and policy iteration ([[03 - Planning by Dynamic Programming]]), Q-learning and Sarsa ([[05 - Model-Free Control]]).

### Extensions (marked "no exam")

- Infinite and continuous MDPs: LQR has a closed form; continuous time leads to the Hamilton–Jacobi–Bellman equation.
- **POMDPs** $\langle\mathcal S,\mathcal A,\mathcal O,\mathcal P,\mathcal R,\mathcal Z,\gamma\rangle$ with observations and an observation function $\mathcal Z^a_{s'o}=\mathbb P[O_{t+1}=o\mid S_{t+1}=s',A_t=a]$. The **belief state** $b(h)=(\mathbb P[S_t=s^1\mid H_t=h],\dots)$ and the history are both Markov, so a POMDP reduces to a history tree or a belief tree.
- **Average-reward MDPs**: an ergodic chain (recurrent, aperiodic) has a stationary distribution $d^\pi(s)=\sum_{s'}d^\pi(s')\mathcal P_{s's}$ and an average reward $\rho^\pi=\lim_T\frac1T\mathbb E[\sum_{t=1}^TR_t]$ independent of the start, with $\tilde v_\pi(s)=\mathbb E_\pi[(R_{t+1}-\rho^\pi)+\tilde v_\pi(S_{t+1})\mid S_t=s]$.

## ✏️ Exercises

**1.** Verify the Bellman equation at C3 in the Student MRP (γ = 1). What changes at γ = 0 and γ = 0.9?

> [!example]- Solution
> $-2+0.6(10)+0.4(0.8)=4.32\approx4.3$. This is a consistency condition: $v(\text{Pub})$ itself depends on $v(\text{C3})$, so all equations must be solved together (the matrix inverse).
> At γ = 0, $v(\text{C3})=-2$; the +10 is invisible. At γ = 0.9, $v(\text{C3})=4.09$. FB moves most: −1, −7.6, −22.5 as γ goes 0, 0.9, 1, because its self-loop keeps the student there $1/(1-0.9)=10$ steps on average.

**2.** Why does fixing a policy turn an MDP into an MRP, and why does that matter?

> [!example]- Solution
> Averaging over actions with π leaves transitions and rewards that depend on the state only: an MRP $\langle\mathcal S,\mathcal P^\pi,\mathcal R^\pi,\gamma\rangle$. So policy evaluation is linear with a closed form. The optimality equation's max changes the action as values change and matches no fixed MRP, which is why control is harder. Control is then solved by alternating evaluation and greedy improvement (policy iteration).

**3.** Why is the expectation equation linear with a closed form and the optimality equation not?

> [!example]- Solution
> In the expectation equation, π and $\mathcal P$ are fixed weights, so $v_\pi=\mathcal R^\pi+\gamma\mathcal P^\pi v_\pi$ can be inverted. The max is not linear ($\max(x+y)\ne\max x+\max y$) and can't be written as a matrix. Hence iterative methods (value iteration, policy iteration) and, without a model, sampled backups: Q-learning samples the optimality backup ($\max_{a'}$), Sarsa the expectation backup (the actual next action).

**4.** Verify $v_*(\text{C1})=6$ and derive the optimal policy from $q_*$.

> [!example]- Solution
> $q_*(\text{C1},\text{Study})=-2+8=6$, $q_*(\text{C1},\text{FB})=-1+6=5$, so $v_*=6$.
>
> | State | $q_*$ | $\pi_*$ |
> |---|---|---|
> | FB | Facebook 5, Quit 6 | Quit |
> | C1 | Study 6, Facebook 5 | Study |
> | C2 | Study 8, Sleep 0 | Study |
> | C3 | Study 10, Pub 9.4 | Study |
>
> $q_*(\text{C3},\text{Pub})=1+0.2(6)+0.4(8)+0.4(10)=9.4$ (the slide shows 8.4, leaving out the +1). Staying on Facebook costs only 1 now but loops back; the one-step comparison already includes the future. With $q_*$ the policy needs no model; with only $v_*$ you need $\mathcal P$ and $\mathcal R$ to look ahead, which is why model-free control learns $q$.

**5.** (Advanced) Why is there always a deterministic optimal policy? When are stochastic policies still needed?

> [!example]- Solution
> For any π, $\sum_a\pi(a\mid s)q_*(s,a)\le\max_aq_*(s,a)$: a weighted average can't beat the maximum, with equality only when all mass is on maximizing actions. Once $q_*$ is known, randomizing gains nothing. (The full proof uses the contraction property in [[03 - Planning by Dynamic Programming]].)
> Stochastic policies are still needed under partial observability (two states look alike), during learning (exploration, [[09 - Exploration and Exploitation]]), in games against adversaries (rock–paper–scissors equilibrium is uniform; not an MDP), and with function approximation, where smooth parameterized policies avoid unstable argmax flips ([[07 - Policy Gradient Methods]]).

## 📝 Summary

- MP $\langle\mathcal S,\mathcal P\rangle$ → MRP (+ rewards, γ) → MDP (+ actions).
- Return $G_t$ is random; value is its expectation.
- γ trades myopia for far-sightedness and keeps cyclic returns finite.
- Bellman: value = immediate reward + discounted successor value; $v=(I-\gamma\mathcal P)^{-1}\mathcal R$ at $O(n^3)$.
- A fixed policy reduces an MDP to an MRP, so evaluation is linear.
- $v_\pi=\sum_a\pi q_\pi$; $q_\pi=\mathcal R+\gamma\mathcal Pv_\pi$.
- A deterministic optimal policy exists; greedy on $q_*$.
- The optimality equation is non-linear: iterative solution.

## ⚠️ Important Notes

1. $G_t$ is a sample; $v(s)$ is an expectation.
2. Bellman equations hold jointly; solve them together.
3. γ is part of the problem: it changes which policy is optimal.
4. With cycles and γ = 1, returns can be unbounded.
5. MDP policies depend only on the current state.
6. The max causes the non-linearity.
7. Q-learning ↔ optimality backup; Sarsa ↔ expectation backup.
8. $v_*$ without a model doesn't give the policy; $q_*$ does.
9. The deterministic-policy theorem is for MDPs only.
10. Transition rows must sum to 1.

> [!warning] Gaps in the source slides
> - The Student chain/MRP/MDP diagrams and backup diagrams are images (slides 7–9, 11, 16–18, 20–21, 25, 29, 31–35, 38–39, 42–47); probabilities, rewards and values extracted. Slide 53's tree figure is an image.
> - Truncated: slide 13 (undiscounted MRPs), 15 (fourth sample return, recomputed), 51 (observation function), 53 (belief-tree reduction); completed with standard definitions.
> - Erratum (slide 47): $q_*(\text{C3},\text{Pub})$ is printed as 8.4; with the +1 Pub reward it is $1+0.2(6)+0.4(8)+0.4(10)=9.4$. The optimal policy (Study) is unchanged.
> - The γ = 1 Student MRP values −13 and −23 are rounded from −12.54 and −22.54 (checked by solving the linear system).
> - Slides 49–56 are marked "no exam".

**Previous:** [[01 - Introduction to Reinforcement Learning]] · **Next:** [[03 - Planning by Dynamic Programming]]
