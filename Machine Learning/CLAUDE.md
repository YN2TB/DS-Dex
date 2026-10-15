# Machine Learning

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## This subject is reinforcement learning

The slides are David Silver's UCL RL course (10 lectures): MDPs, DP, MC/TD, Sarsa/Q-learning, function approximation, policy gradients, model-based RL and MCTS, bandits, games. Nothing covers supervised or unsupervised learning. `documents/` has ISL and Murphy for that, without slides. If the user asks about regression or classification, point to ISL/Murphy. If classical ML is examinable, it needs a textbook-only scope decision (see root `CLAUDE.md`) and new chapters after 10 or a renumbering: ask the user which.

## Extraction

Beamer slides: definitions, theorems, proofs and equations extract well; figures don't. Costly exceptions: the ✓/✗ marks in Lecture 6's convergence tables (reconstructed from Sutton & Barto ch. 11, flagged), Lecture 8's MCTS walkthrough, Lecture 5's pseudocode boxes. Lecture 1's admin slides describe UCL's assessment, not NEU's.

## Errata

E1 (Lecture 2) and E2 (Lecture 9): `contents/00-Index.md`.

Cross-subject: ch. 02 and 04 lean on `Probability Theory/contents/09 - Additional Topics in Probability.md` (Markov chains); ch. 06–07 on `Optimization/contents/05 - Gradient Methods.md`.
