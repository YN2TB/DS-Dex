---
subject: Machine Learning
chapter: 00
tags: [ds, moc, index, reinforcement-learning, machine-learning]
source: "intro_rl.pdf — David Silver, UCL (10-lecture RL course)"
---

# Machine Learning — Index

> [!warning] What this subject's slides actually cover
> **The `documents/slides/` folder contains David Silver's UCL Reinforcement Learning course** — 10 lectures, ~480 pages. It does **not** cover supervised or unsupervised learning at all.
>
> The two textbooks in `documents/` do cover classical ML:
> - **James, Witten, Hastie & Tibshirani, *An Introduction to Statistical Learning*** (Springer 2015)
> - **Kevin Murphy, *Machine Learning: A Probabilistic Perspective*** (MIT Press 2012)
>
> **No slides accompany either textbook**, so the notes below are RL-only. If your course also examines supervised learning, that material must come from ISL/Murphy directly — see the gap note at the bottom.

## 🗺️ Map of Content

### Part I — Elementary Reinforcement Learning

| # | Chapter | One-line description |
|---|---|---|
| 01 | [[01 - Introduction to Reinforcement Learning]] | Agent, environment, reward hypothesis; policy/value/model; the four problems within RL |
| 02 | [[02 - Markov Decision Processes]] | **The mathematical foundation** — Markov Process → MRP → MDP, and the Bellman equations |
| 03 | [[03 - Planning by Dynamic Programming]] | Policy evaluation, policy iteration, value iteration; the contraction mapping proofs |
| 04 | [[04 - Model-Free Prediction]] | Monte-Carlo and Temporal-Difference learning; TD(λ) and eligibility traces |
| 05 | [[05 - Model-Free Control]] | ε-greedy and GLIE; **Sarsa** (on-policy) and **Q-learning** (off-policy) |

### Part II — Reinforcement Learning in Practice

| # | Chapter | One-line description |
|---|---|---|
| 06 | [[06 - Value Function Approximation]] | Scaling beyond lookup tables; **the deadly triad**; DQN; least-squares methods |
| 07 | [[07 - Policy Gradient Methods]] | Parameterising the policy directly; REINFORCE; actor-critic; natural gradient |
| 08 | [[08 - Integrating Learning and Planning]] | Learning a **model**; Dyna; **Monte-Carlo Tree Search** |
| 09 | [[09 - Exploration and Exploitation]] | Bandits and regret; **UCB**; Thompson sampling; Bayes-adaptive RL |
| 10 | [[10 - Case Study - RL in Classic Games]] | Self-play, minimax, TD-Gammon, TreeStrap — everything combined |

---

## 🎯 The course's spine

### What makes RL different

> - **There is no supervisor, only a reward signal**
> - **Feedback is delayed, not instantaneous**
> - **Time really matters** (sequential, **non-i.i.d.** data)
> - **The agent's actions affect the subsequent data it receives**

Each point breaks an assumption that the rest of statistics and machine learning rely on — which is why RL needs its own theory rather than borrowing supervised learning's.

### The two Bellman equations generate everything

[[02 - Markov Decision Processes]] introduces two equations, and **the entire course is ways of solving them**:

$$\textbf{Expectation: } v_\pi(s) = \sum_a\pi(a\mid s)\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_\pi(s')\right) \qquad \textbf{linear, closed form}$$

$$\textbf{Optimality: } v_*(s) = \max_a\left(\mathcal{R}^a_s + \gamma\sum_{s'}\mathcal{P}^a_{ss'}v_*(s')\right) \qquad \textbf{non-linear, no closed form}$$

**The $\max$ is the entire difficulty of RL.** The single most useful table in the course, from [[05 - Model-Free Control]]:

| Bellman equation | **Full Backup (DP)** | **Sample Backup (TD)** |
|---|---|---|
| **Expectation for $v_\pi$** | Iterative Policy Evaluation | TD Learning |
| **Expectation for $q_\pi$** | Q-Policy Iteration | **Sarsa** |
| **Optimality for $q_*$** | Q-Value Iteration | **Q-Learning** |

Read **horizontally**: replacing the expectation with a sample turns a planning algorithm into a learning algorithm. Read **vertically**: the choice of Bellman equation is the difference between Sarsa and Q-learning.

### Three axes that organise the field

| Axis | Poles | Where discussed |
|---|---|---|
| **What the agent represents** | Value / Policy / Both (actor-critic) | [[01 - Introduction to Reinforcement Learning]], [[07 - Policy Gradient Methods]] |
| **Model** | Model-free / Model-based | [[01 - Introduction to Reinforcement Learning]], [[08 - Integrating Learning and Planning]] |
| **Backup depth** | Shallow (TD) ↔ Deep (MC), via TD(λ) | [[04 - Model-Free Prediction]] |

Plus the **bootstrapping × sampling** grid: MC samples but does not bootstrap; DP bootstraps but does not sample; **TD does both**; exhaustive search does neither.

### Prediction before control, always

**Prediction** (evaluate a given policy) is easy — the expectation equation is linear. **Control** (find the best policy) is hard — the optimality equation is not. Control is therefore built by **iterating prediction**: evaluate, improve greedily, repeat. That loop — **Generalised Policy Iteration** — is introduced in [[03 - Planning by Dynamic Programming]] and reappears in every subsequent lecture.

---

## 📚 Textbooks

**For the RL slides** (both free online, cited on slide 5 of Lecture 1):
- **Sutton & Barto, *An Introduction to Reinforcement Learning*** (MIT Press, 1998) — [free](http://webdocs.cs.ualberta.ca/~sutton/book/the-book.html). The standard reference; nearly every example in the slides is from it.
- **Szepesvári, *Algorithms for Reinforcement Learning*** (Morgan & Claypool, 2010) — [free](http://www.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf)

**In `documents/` but not covered by any slides:**
- **ISL** — James, Witten, Hastie & Tibshirani (2015) — regression, classification, resampling, regularisation, trees, SVMs, unsupervised learning
- **Murphy** (2012) — the probabilistic treatment; graphical models, Bayesian methods, deep learning

---

## 🔗 Cross-subject connections

| Topic | Links to |
|---|---|
| Expectation, variance, distributions, Markov chains | [[Probability Theory/contents/00-Index\|Probability Theory]] |
| Estimators, bias–variance, MLE, Fisher information, Cramér–Rao | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| Gradient descent, function approximation, features, overfitting | [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] |
| Matrix inversion, eigenvalues, contraction mappings | [[Linear Algebra/contents/00-Index\|Linear Algebra]] |
| Convex optimisation, gradient methods, Nelder–Mead | [[Optimization/contents/00-Index\|Optimization]] |
| Deploying and monitoring learned policies | [[MLOps/contents/00-Index\|MLOps]] |
| Dynamic programming, graph search, tree search | [[Data Structures and Algorithms/contents/00-Index\|Data Structures and Algorithms]] |

---

## ⚠️ Gaps in the source material

> [!warning] Coverage gap: no supervised or unsupervised learning
> **The slides are RL-only.** Nothing in `documents/slides/` covers regression, classification, clustering, dimensionality reduction, SVMs, trees, or neural networks as supervised learners. If those are examinable, work directly from **ISL** (accessible, applied) or **Murphy** (rigorous, probabilistic) — both are in `documents/`.

> [!warning] Extraction quality
> **Silver's slides are LaTeX Beamer and extracted unusually well** — far better than the PowerPoint-based subjects in this vault. **All definitions, theorems, proofs, and equations survived** except where noted below. The consistent loss is **figures**: every diagram, plot, and worked-example illustration is an image.
>
> **The most costly individual losses:**
>
> **1. [[06 - Value Function Approximation]] — the ✓/✗ marks in every convergence table failed to extract** (slides 30, 31, 32, 46, 52). Those tables are highly examinable; the versions in the note are **reconstructed** from Sutton & Barto Ch. 11 plus the surrounding text. **Verify against the original PDF.**
>
> **2. [[08 - Integrating Learning and Planning]] — slides 42–46, the five-slide MCTS walkthrough, are entirely images.** The step-by-step growth of the search tree is not recoverable. The **Dyna-Q pseudocode (slide 27)** is also an image.
>
> **3. [[05 - Model-Free Control]] — the boxed pseudocode for Sarsa, Sarsa(λ), and Q-learning (slides 22, 29, 38) are all images.** The update rules appear in text elsewhere, but the complete algorithm listings do not.
>
> **4. [[07 - Policy Gradient Methods]] — the Policy Gradient Theorem statement itself is truncated** (slide 20), cut at *"for any of the policy objective functions $J =$"*.
>
> **5. [[09 - Exploration and Exploitation]] — the Lai–Robbins lower bound is truncated** at $\lim_{t\to\infty}$ (slide 14).
>
> **6. [[02 - Markov Decision Processes]] — the Student MDP state diagrams are images.** The transition matrix, rewards, and value numbers extracted, but the graph structure is only partially recoverable.
>
> **7. [[10 - Case Study - RL in Classic Games]] — the final "successful recipe" table is cut at "Go"**, so the last rows are lost.
>
> Each chapter's own `⚠️ Gaps` callout lists its specific truncations.

> [!note] Course admin is UCL's, not NEU's
> Lecture 1 slides 3–5 give the original UCL arrangements — Thursdays 9:30–11:00, 50% coursework / 50% exam, Assignment A on RL and Assignment B on kernels. **These are not NEU's assessment terms.** Note also that the UCL course paired RL with a *kernels* half that is absent here.

---

## 📌 The one-page revision path

1. **RL breaks four assumptions** — no supervisor, delayed feedback, non-i.i.d. data, actions affect future data — [[01 - Introduction to Reinforcement Learning]]
2. **Markov: the state is a sufficient statistic of the future.** MP → MRP → MDP — [[02 - Markov Decision Processes]]
3. **Bellman expectation is linear (closed form); Bellman optimality is not (the `max`)** — [[02 - Markov Decision Processes]]
4. **Fixing a policy reduces an MDP to an MRP**, which is why prediction is easy and control is built by iterating it — [[02 - Markov Decision Processes]], [[03 - Planning by Dynamic Programming]]
5. **Greedy improvement never hurts; when it stops, you are optimal** — [[03 - Planning by Dynamic Programming]]
6. **Both Bellman operators are γ-contractions**, giving unique fixed points and a linear rate — [[03 - Planning by Dynamic Programming]]
7. **MC = unbiased, high variance; TD = biased, low variance.** TD bootstraps and samples — [[04 - Model-Free Prediction]]
8. **Model-free control needs $Q$, not $V$** (improving from $V$ requires a model) — [[05 - Model-Free Control]]
9. **Sarsa uses $Q(S',A')$; Q-learning uses $\max_{a'}Q(S',a')$** — the two Bellman equations, sampled — [[05 - Model-Free Control]]
10. **The deadly triad:** function approximation + bootstrapping + off-policy. Any two are safe — [[06 - Value Function Approximation]]
11. **The likelihood ratio trick** turns a gradient into a sampleable expectation — [[07 - Policy Gradient Methods]]
12. **A baseline is free because $\sum_a\pi = 1$**; the best one gives the advantage function — [[07 - Policy Gradient Methods]]
13. **Model learning is supervised learning**, and simulation-based search solves only the sub-MDP from now — [[08 - Integrating Learning and Planning]]
14. **ε-greedy has linear regret; UCB achieves the logarithmic lower bound** — [[09 - Exploration and Exploitation]]
15. **Fixing the opponents reduces a game to an MDP; Nash is the fixed point of self-play** — [[10 - Case Study - RL in Classic Games]]

### The recurring pattern

**Almost every algorithm in this course is Generalised Policy Iteration with a different evaluation step substituted in.** DP evaluation → policy iteration. MC evaluation → MC control. TD evaluation → Sarsa. Function approximation → approximate control. A critic → actor-critic. Simulated experience → Dyna and MCTS. **Recognise the skeleton and the ten lectures collapse into one idea with nine variations.**
