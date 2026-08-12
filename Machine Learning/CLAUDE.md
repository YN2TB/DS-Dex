# Machine Learning — subject context

**Status: ✅ complete for what the slides cover** (2026-07-27). `contents/00-Index.md` plus chapters 01–10.

## ⚠️ Read this first: this subject is Reinforcement Learning

**The slides are David Silver's UCL Reinforcement Learning course** (10 lectures, ~480 pages) — not a general ML course. The notes follow them: MDPs, dynamic programming, MC/TD learning, Sarsa/Q-learning, function approximation, policy gradients, model-based RL/MCTS, bandits, self-play games.

**There is a real coverage gap.** Nothing in the slides covers supervised or unsupervised learning — no regression, classification, clustering, SVMs, trees, or neural networks as supervised learners. `documents/` holds **ISL** (James/Witten/Hastie/Tibshirani) and **Murphy** for that material, but **no slides accompany either textbook**.

**So: if the user asks about regression or classification, point at ISL/Murphy — the notes do not cover it.** If the exam covers classical ML, those chapters still need writing from the textbooks directly, as a textbook-only scope decision (see root `../CLAUDE.md`). That would be new files numbered after 10, or a renumbering — ask the user which.

## Chapters

01 Introduction to Reinforcement Learning · 02 Markov Decision Processes · 03 Planning by Dynamic Programming · 04 Model-Free Prediction · 05 Model-Free Control · 06 Value Function Approximation · 07 Policy Gradient Methods · 08 Integrating Learning and Planning · 09 Exploration and Exploitation · 10 Case Study — RL in Classic Games

## Extraction

**Silver's LaTeX Beamer slides extracted better than any other source in this vault** — all definitions, theorems, proofs and equations survived. Only figures were lost. Three costly exceptions:

- the **✓/✗ marks in Lecture 6's convergence tables** did not extract — reconstructed from Sutton & Barto ch. 11 and **flagged as unverified**
- Lecture 8's **five-slide MCTS walkthrough is image-only**
- the **Sarsa / Q-learning pseudocode boxes** in Lecture 5 are images

## Other note

Lecture 1's admin slides give **UCL's** assessment terms (50% coursework, Assignment B on kernels), not NEU's. Ignored in the notes.

Cross-subject: ch. 02 and ch. 04 lean on `Probability Theory/contents/09 - Additional Topics in Probability.md` (Markov chains); ch. 06–07 on `Optimization/contents/05 - Gradient Methods.md` (SGD).
