# Machine Learning: subject context

**Status: ✅ complete for what the slides cover** (2026-07-27), rewritten concisely 2026-10-09. `contents/00-Index.md` plus chapters 01–10.

## This subject is reinforcement learning

The slides are David Silver's UCL RL course (10 lectures): MDPs, DP, MC/TD, Sarsa/Q-learning, function approximation, policy gradients, model-based RL and MCTS, bandits, games. Nothing covers supervised or unsupervised learning. `documents/` has ISL and Murphy for that, without slides. If the user asks about regression or classification, point to ISL/Murphy. If classical ML is examinable, it needs a textbook-only scope decision (see root `CLAUDE.md`) and new chapters after 10 or a renumbering: ask the user which.

## Chapters

01 Introduction to Reinforcement Learning · 02 Markov Decision Processes · 03 Planning by Dynamic Programming · 04 Model-Free Prediction · 05 Model-Free Control · 06 Value Function Approximation · 07 Policy Gradient Methods · 08 Integrating Learning and Planning · 09 Exploration and Exploitation · 10 Case Study - RL in Classic Games

## Extraction

Beamer slides: definitions, theorems, proofs and equations extract well; figures don't. Costly exceptions: the ✓/✗ marks in Lecture 6's convergence tables (reconstructed from Sutton & Barto ch. 11, flagged), Lecture 8's MCTS walkthrough, Lecture 5's pseudocode boxes. Lecture 1's admin slides describe UCL's assessment, not NEU's.

## Errata (found 2026-10-09)

- E1, Lecture 2 slide 47: $q_*(\text{C3},\text{Pub})$ printed 8.4, correct 9.4.
- E2, Lecture 9 slide 20: UCB1 regret bound printed $8\log t\sum\Delta_a$; correct $8\sum\log t/\Delta_a+(1+\pi^2/3)\sum\Delta_a$.

Cross-subject: ch. 02 and 04 lean on `Probability Theory/contents/09 - Additional Topics in Probability.md` (Markov chains); ch. 06–07 on `Optimization/contents/05 - Gradient Methods.md`.
