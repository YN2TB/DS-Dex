---
subject: Deep Learning
chapter: 00
tags: [ds, moc, deep-learning]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning (PyTorch edition)"
---

# Deep Learning — Map of Content

Course notes for **Deep Learning**, Data Science major, NEU. Single source: **Aston Zhang, Zachary C. Lipton, Mu Li & Alexander J. Smola, *Dive into Deep Learning*** (D2L), the Cambridge University Press print edition — 20 chapters, two appendices, PyTorch throughout.

## 🎯 Scope — set by the course syllabus, not chosen here

> [!note] This subject's scope is **not** an editorial guess
> Most textbook-only subjects in this vault required picking a standard scope and flagging it for confirmation against the real syllabus. **Not this one.** The eight topics below are the course's own topic list; D2L's twenty chapters are quarried for material to fill them. Where a topic spans several D2L chapters, they are merged; where D2L has chapters the course does not name, they are omitted and the reason is given.

| # | Note | Covers | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to Deep Learning]] | What learning *is*: data, model, objective, algorithm; supervised / unsupervised / RL; decisions vs. `argmax`; why depth and why now — Table 1.5.1 audited | ✅ |
| 02 | [[02 - Linear Regression]] | Squared loss **as** maximum likelihood under Gaussian noise; normal equations; minibatch SGD; generalization and the IID assumption; weight decay, ridge shrinkage, and why a norm is blind to direction | ✅ |
| 03 | [[03 - Logistic Regression]] | One-hot targets; softmax and its redundant parametrization; cross-entropy as MLE; the $\hat y-y$ gradient and its covariance Hessian; entropy, surprisal, KL; how big a test set must be; adaptive overfitting; covariate / label / concept shift and their corrections | ✅ |
| 04 | [[04 - Neural Network]] | MLPs and why a hidden layer needs a nonlinearity; activation functions; forward- and back-propagation; vanishing/exploding gradients; initialization; dropout; the optimizer family through Adam | ⬜ |
| 05 | [[05 - Convolutional Neural Network]] | Translation invariance and locality as constraints on an MLP; cross-correlation, padding, stride, channels, pooling; LeNet → AlexNet, VGG, NiN, GoogLeNet, batch norm, ResNet, DenseNet | ⬜ |
| 06 | [[06 - Object Detection]] | Image augmentation and fine-tuning; bounding boxes; anchor boxes, IoU, non-maximum suppression; multiscale detection; SSD; the R-CNN family | ⬜ |
| 07 | [[07 - Recurrent Neural Network]] | Sequence models and autoregression; text → tokens → vocabulary; language models and perplexity; RNNs, BPTT, gradient clipping; LSTM, GRU, deep and bidirectional RNNs | ⬜ |
| 08 | [[08 - Sequence to Sequence]] | Machine translation data; the encoder–decoder architecture; seq2seq with teacher forcing; masked loss; BLEU; beam search; **attention, multi-head self-attention and the Transformer** | ⬜ |

## 🧭 How the eight notes map onto D2L

| Note | D2L chapters/sections quarried |
|---|---|
| 01 | ch. 1 (all); 2.4–2.5 for calculus & autodiff |
| 02 | 3.1–3.7 |
| 03 | 4.1–4.7 |
| 04 | ch. 5 (all); ch. 6; ch. 12 optimizers |
| 05 | ch. 7 (all); ch. 8 (all) |
| 06 | 14.1–14.8 |
| 07 | ch. 9 (all); 10.1–10.4 |
| 08 | 10.5–10.8; 11.1–11.7 |

### Two additions beyond a literal reading of the topic list

Both are flagged again in the gaps callout of the note that carries them.

1. **Optimization algorithms (D2L ch. 12) are folded into note 04.** The syllabus gives them no topic of their own, but momentum, AdaGrad, RMSProp and Adam are how every later network in the course is actually trained. Dropping them to honour the letter of the list would leave the notes unable to explain any training run.
2. **Attention and the Transformer (D2L 11.1–11.7) are folded into note 08.** "Sequence2sequence" ends, historically and pedagogically, at the point attention replaced the fixed-length context vector. Stopping before it would end the subject one step short of everything built since 2017.

### What is not covered, and why

| D2L chapter | Why omitted |
|---|---|
| 2 Preliminaries | Tensors, linear algebra, probability — already held by [[Linear Algebra/contents/00-Index\|Linear Algebra]], [[Probability Theory/contents/00-Index\|Probability Theory]] and [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]]. Only 2.4–2.5 (calculus, autodiff) are pulled into note 01, because automatic differentiation is specific to this subject. |
| 6 Builders' Guide | Framework mechanics, not theory. The parts that carry ideas (custom layers, parameter tying, initialization) are absorbed into note 04. |
| 13 Computational Performance | Multi-GPU training, parameter servers, hardware. Engineering, and closer to [[MLOps/contents/00-Index\|MLOps]] than to this course. |
| 15–16 NLP: Pretraining / Applications | word2vec, GloVe, BERT, sentiment analysis, NLI. The vault has a **separate Natural Language Processing subject**; putting them here would duplicate it. *(That subject is currently blocked — `documents/` is empty.)* |
| 17 Reinforcement Learning | MDPs, value iteration, Q-learning — already written in [[Machine Learning/contents/00-Index\|Machine Learning]] ch. 01–10, which is an RL-only subject. |
| 18 Gaussian Processes | A Bayesian nonparametric detour; not deep learning and not on the topic list. |
| 19 Hyperparameter Optimization | Tuning infrastructure (successive halving, async schedulers) — MLOps territory. |
| 20 Generative Adversarial Networks | Generative modelling is a topic the list does not raise. Noted here as the most defensible *addition* if the syllabus turns out to include it. |
| Appendix A Mathematics | Duplicates the maths subjects above. |
| Appendix B Tools | Jupyter, SageMaker, contributing — not examinable. |

> [!question] Worth confirming with the lecturer
> The topic list gives no weighting. If the course spends real time on **GANs or generative models**, note 09 would be the place to add them — D2L ch. 20 is short and self-contained. Likewise, if **NLP** is examined *inside* this course rather than separately, D2L ch. 15–16 would need pulling in.

## ⚠️ Source hazards — the one thing to remember

> [!warning] Never transcribe a formula from this PDF
> The text layer **silently deletes** minus signs, assignment arrows, learning-rate symbols and fraction bars, turns `,` into `;`, `|` into `j`, `∈` into `2`, `∂` into `@`, and **erases the scalar/vector/matrix typography entirely** — the notation page's four distinct symbols for scalar, vector, matrix and tensor all extract as the same glyph.
>
> Example, from book p. 87: the text `(w; b) (w; b)   jBj ∑ i2B t @(w;b)l(i)(w; b)` is
> $$(\mathbf w, b) \leftarrow (\mathbf w, b) - \frac{\eta}{|\mathcal B|}\sum_{i \in \mathcal B_t} \partial_{(\mathbf w, b)} \ell^{(i)}(\mathbf w, b)$$
> Every formula in these notes is therefore **reconstructed from the prose and verified numerically**, never copied. Full substitution table in this subject's `CLAUDE.md`.
>
> Also: **all figures are images and never extract**; **code listings lose their indentation**; inter-word spaces collapse in justified prose (harmless).

## 📐 Conventions in these notes

- Every numeric claim is recomputed (`sympy`/`numpy`) before it is written down, including every exercise answer.
- Formulas are reconstructed and checked against the book's own printed numbers — see the hazard box above.
- Anything reconstructed, assumed, or added beyond D2L is declared in each note's closing `> [!warning] Gaps in the source material` callout.

## 🔗 Cross-subject links

| Subject | Relationship |
|---|---|
| [[Machine Learning/contents/00-Index\|Machine Learning]] | **Owns reinforcement learning** (MDPs, value iteration, Q-learning). D2L ch. 17 is deliberately not duplicated here. |
| [[Optimization/contents/00-Index\|Optimization]] | Owns convexity, gradient-descent convergence theory, constrained optimization. This subject uses the *algorithms* (SGD, momentum, Adam) and points there for the theory. |
| [[Probability Theory/contents/00-Index\|Probability Theory]] | Maximum likelihood, Gaussians — the justification for squared loss in note 02. |
| [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] | Estimation, bias–variance, hypothesis testing behind generalization in notes 02–03. |
| [[Linear Algebra/contents/00-Index\|Linear Algebra]] | Matrix calculus, norms, rank — every layer is an affine map. |
| [[Calculus/contents/00-Index\|Calculus]] | The chain rule *is* backpropagation (note 04). |
| [[Data Structures and Algorithms/contents/00-Index\|Data Structures and Algorithms]] | Complexity counting; the vectorization result in note 01 is the same "measure it, don't assume it" discipline. |
| [[MLOps/contents/00-Index\|MLOps]] | Training infrastructure, deployment, monitoring — where D2L ch. 13 and 19 would go. |
| [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] | Preprocessing and augmentation pipelines feeding note 06. |
| **Computer Vision** | Sister subject (Szeliski). D2L ch. 7–8 and 14 overlap it; **boundary: this subject owns *learned* representations (CNNs, detection heads), Computer Vision owns image formation, geometry, and classical features.** |

## 📋 Errata

**No errata filed. Six discrepancies investigated and declined.** Any discrepancy between a printed number and a recomputation is logged here **only after** ruling out extraction damage, my own arithmetic, and an alternative convention — filing a false erratum against a correct source is the worse failure.

| # | Location | Printed | Recomputed | Verdict |
|---|---|---|---|---|
| D1 | §1.5, prose under Table 1.5.1 | "increases in computational power have **outpaced** the growth in datasets" | Over 1970–2020 both grew by exactly $10^{10}$; the ratio is **1.000**. True only for 2000 onward. | **Declined.** Defensible as a claim about recent decades; the table is explicitly order-of-magnitude. Recorded in ch. 01 §6. |
| D2 | Table 1.5.1, 1970 row | Iris = "100" examples | Iris has **150** | **Declined.** Every cell in the table is rounded to a power of ten; this is the stated convention, not an error. |
| D3 | §3.7.3–3.7.4, printed caption | `'L2 norm of w: '` | The line prints `l2_penalty(w)` = `(w**2).sum()/2`, i.e. **½‖w‖², not ‖w‖** | **Declined as an erratum — recorded as a mislabel.** The code is correct and self-consistent; only the caption is loose. But it matters: the three printed values differ by 6.72× while the norms differ by 2.59×. |
| D4 | §3.7.4 vs §3.7.3 | concise `wd=3` prints **0.012314**; scratch `λ=3` prints **0.001473**; text says "the plot looks similar" | 8.4× apart at the same nominal λ. Cause: `nn.MSELoss` omits the ½ (halving effective λ) **and** `nn.LazyLinear` initializes to ½‖w‖² ≈ 0.1667 vs the scratch `sigma=0.01` start of 0.0100; 40 updates cannot forget it. Simulating the concise config gives 0.0140 vs printed 0.0123. | **Declined.** Both numbers are correct outputs of their own code. The finding is that they are **not comparable** and the book invites the comparison anyway. Full working in ch. 02 §10 and exercise 5. |
| D5 | §4.6.1, the 15,000-vs-10,000 comparison | Hoeffding gives "roughly 15,000" against the asymptotic 10,000 | 14,979 is the **one-sided** bound at δ=0.05, but "two standard deviations ⇒ 95%" is **two-sided**. Like-for-like is **18,444 vs 10,000 (1.84×)**, not 1.50×. | **Declined.** Eq. (4.6.3) is printed one-sided and the arithmetic matches it; only the comparison mixes conventions, and the conclusion ("slightly more conservative") survives either way. |
| D6 | §4.7.3, definition of the confusion matrix | "$c_{ij}$ is the fraction of **total predictions** where the true label was $j$ and the model predicted $i$" | Read literally this is a **joint** frequency, under which $\mathbf{C}p(\mathbf{y})=\mu(\hat{\mathbf{y}})$ is dimensionally wrong. The system requires the **column-conditional** matrix $c_{ij}=P(\hat y=i\mid y=j)$, columns summing to 1. | **Declined as an erratum — recorded as an imprecision.** The intended object is unambiguous from the equation; only the prose is loose. Flagged in ch. 03 §11.4 because getting it wrong silently breaks the correction. |
