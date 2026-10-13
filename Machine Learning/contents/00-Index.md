---
subject: Machine Learning
chapter: 00
tags: [ds, moc, index, reinforcement-learning, machine-learning]
source: "intro_rl.pdf — David Silver, UCL (10-lecture RL course)"
---

# Machine Learning: Index

> [!warning] The slides are a reinforcement learning course
> `documents/slides/` holds David Silver's UCL Reinforcement Learning course (10 lectures, ~480 pages). It doesn't cover supervised or unsupervised learning. `documents/` also has ISL (James, Witten, Hastie & Tibshirani, 2015) and Murphy (*Machine Learning: A Probabilistic Perspective*, 2012), with no slides; if classical ML is examined, work from those.

## Map of content

| # | Chapter | Topics | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to Reinforcement Learning]] | agent, environment, reward; policy, value, model; learning vs planning | ✅ |
| 02 | [[02 - Markov Decision Processes]] | Markov process → MRP → MDP; Bellman equations | ✅ |
| 03 | [[03 - Planning by Dynamic Programming]] | policy evaluation, policy and value iteration, contraction | ✅ |
| 04 | [[04 - Model-Free Prediction]] | Monte Carlo, TD, TD(λ), eligibility traces | ✅ |
| 05 | [[05 - Model-Free Control]] | ε-greedy, GLIE, Sarsa, Q-learning | ✅ |
| 06 | [[06 - Value Function Approximation]] | linear and neural approximation, deadly triad, DQN, LSTD, LSPI | ✅ |
| 07 | [[07 - Policy Gradient Methods]] | REINFORCE, actor-critic, advantage, natural gradient | ✅ |
| 08 | [[08 - Integrating Learning and Planning]] | model learning, Dyna, MCTS, TD search | ✅ |
| 09 | [[09 - Exploration and Exploitation]] | bandits, regret, UCB, Thompson sampling, Bayes-adaptive RL | ✅ |
| 10 | [[10 - Case Study - RL in Classic Games]] | game theory, minimax, self-play, TD-Gammon, TreeStrap | ✅ |

Part I (01–05): elementary RL. Part II (06–10): RL in practice.

## The core ideas

RL differs from supervised learning: no supervisor, only rewards; delayed feedback; sequential, non-i.i.d. data; actions affect future data.

The course solves two equations from ch. 02:
$$v_\pi(s)=\sum_a\pi(a\mid s)\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_\pi(s')\Big)\ \text{(linear)},\qquad v_*(s)=\max_a\Big(\mathcal R^a_s+\gamma\sum_{s'}\mathcal P^a_{ss'}v_*(s')\Big)\ \text{(non-linear)}.$$

| Bellman equation | Full backup (DP) | Sample backup (TD) |
|---|---|---|
| expectation, $v_\pi$ | iterative policy evaluation | TD learning |
| expectation, $q_\pi$ | Q-policy iteration | Sarsa |
| optimality, $q_*$ | Q-value iteration | Q-learning |

Most algorithms are generalized policy iteration with a different evaluation step: DP, MC, TD, function approximation, a critic, simulated experience.

| Axis | Options | Chapters |
|---|---|---|
| what is learned | value / policy / both | 01, 07 |
| model | model-free / model-based | 01, 08 |
| backup depth | TD ↔ MC via λ | 04 |
| bootstrapping × sampling | DP, MC, TD, exhaustive search | 04 |

**Textbooks** (free online): Sutton & Barto, *Reinforcement Learning: An Introduction*; Szepesvári, *Algorithms for Reinforcement Learning*.

## Cross-subject links

| Topic | Subject |
|---|---|
| Markov chains, expectation | [[Probability Theory/contents/00-Index\|Probability Theory]] |
| MLE, Fisher information, bias–variance, hypothesis tests | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| matrix inversion, contraction | [[Linear Algebra/contents/00-Index\|Linear Algebra]] |
| gradient methods, Nelder–Mead | [[Optimization/contents/00-Index\|Optimization]] |
| neural networks | [[Deep Learning/contents/00-Index\|Deep Learning]] |
| dynamic programming, tree search | [[Data Structures and Algorithms/contents/00-Index\|Data Structures and Algorithms]] |
| deploying and monitoring models | [[MLOps/contents/00-Index\|MLOps]] |

## Gaps in the source material

The Beamer slides extract well; figures are lost. The costliest gaps:
1. ch. 06: the ✓/✗ marks in the convergence tables (slides 30–32, 46, 52) didn't extract; the tables follow Sutton & Barto ch. 11. Check against the PDF.
2. ch. 08: the five-slide MCTS walkthrough (42–46) and the Dyna-Q pseudocode (27) are images.
3. ch. 05: the Sarsa, Sarsa(λ) and Q-learning pseudocode boxes are images.
4. ch. 07: the policy gradient theorem's equation is cut off (slide 20).
5. ch. 02: the Student MDP diagrams are images (numbers survive).
6. ch. 10: the recipe table stops at "Go".

Lecture 1's admin slides describe UCL's assessment (50% coursework, including an assignment on kernels, 50% exam), not NEU's.

**Errata found in the 2026-10-09 rewrite** (checked by recomputation):

| # | Lecture | Slide | Printed | Correct |
|---|---|---|---|---|
| E1 | 2 | 47 | $q_*(\text{C3},\text{Pub})=8.4$ | $1+0.2(6)+0.4(8)+0.4(10)=9.4$ (the +1 Pub reward was left out; optimal policy unchanged) |
| E2 | 9 | 20 | UCB1: $\lim L_t\le8\log t\sum\Delta_a$ | $8\sum\frac{\log t}{\Delta_a}+(1+\frac{\pi^2}3)\sum\Delta_a$ (Auer et al. 2002) |

Also noted: Lecture 2's γ = 1 values −13 and −23 are rounded from −12.54 and −22.54; Lecture 3 shows −1.7 for the exact −1.75; Lecture 9's Beta labelling counts losses in α.
