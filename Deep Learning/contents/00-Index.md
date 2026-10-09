---
subject: Deep Learning
chapter: 00
tags: [ds, moc, deep-learning]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning (PyTorch edition)"
---

# Deep Learning — Map of Content

Notes for the Deep Learning course (Data Science, NEU). Single source: Zhang, Lipton, Li & Smola, *Dive into Deep Learning* (D2L), Cambridge University Press edition, PyTorch.

## Scope

The eight topics come from the user's own syllabus (`note/Index.md`). D2L chapters are used as material for them; where a topic spans several chapters they are merged.

| # | Note | Covers | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to Deep Learning]] | data, model, objective, optimizer; kinds of learning; decisions vs argmax; why deep learning took off | ✅ |
| 02 | [[02 - Linear Regression]] | squared loss as MLE; normal equations; minibatch SGD; generalization; weight decay | ✅ |
| 03 | [[03 - Logistic Regression]] | softmax, cross-entropy, information theory; test-set size; distribution shift and corrections | ✅ |
| 04 | [[04 - Neural Network]] | MLPs, activations, backprop, vanishing/exploding gradients, initialization, dropout; optimizers through Adam | ✅ |
| 05 | [[05 - Convolutional Neural Network]] | convolution, padding, stride, channels, pooling; LeNet → AlexNet, VGG, NiN, GoogLeNet, batch norm, ResNet, DenseNet | ✅ |
| 06 | [[06 - Object Detection]] | augmentation, fine-tuning; anchors, IoU, NMS; multiscale detection, SSD; R-CNN family | ✅ |
| 07 | [[07 - Recurrent Neural Network]] | sequence models, tokenization, perplexity; RNN, BPTT, clipping; LSTM, GRU, deep and bidirectional | ✅ |
| 08 | [[08 - Sequence to Sequence]] | encoder–decoder, BLEU, beam search; attention, multi-head self-attention, Transformer | ✅ |

### Mapping to D2L

| Note | D2L sections |
|---|---|
| 01 | ch. 1; 2.4–2.5 |
| 02 | 3.1–3.7 |
| 03 | 4.1–4.7 |
| 04 | ch. 5, ch. 6, ch. 12 |
| 05 | ch. 7, ch. 8 |
| 06 | 14.1–14.8 |
| 07 | ch. 9; 10.1–10.4 |
| 08 | 10.5–10.8; 11.1–11.7 |

Two additions beyond the topic list:
1. **Optimizers (ch. 12) are in note 04.** The syllabus has no optimizer topic, but every later model is trained with momentum or Adam.
2. **Attention and the Transformer (11.1–11.7) are in note 08.** Seq2seq leads directly into attention.

### Not covered

| D2L chapter | Reason |
|---|---|
| 2 Preliminaries | covered by [[Linear Algebra/contents/00-Index\|Linear Algebra]], [[Probability Theory/contents/00-Index\|Probability Theory]], [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]]; only 2.4–2.5 used |
| 6 Builders' Guide | framework mechanics; useful parts are in note 04 |
| 13 Computational Performance | engineering, closer to [[MLOps/contents/00-Index\|MLOps]] |
| 15–16 NLP | belongs to the separate (currently blocked) NLP subject |
| 17 Reinforcement Learning | covered in [[Machine Learning/contents/00-Index\|Machine Learning]] |
| 18 Gaussian Processes | not deep learning, not on the list |
| 19 Hyperparameter Optimization | MLOps territory |
| 20 GANs | not on the list; the most likely addition if the course covers it |
| Appendices | maths duplicates; tools not examinable |

> [!question] Worth checking with the lecturer
> If GANs or NLP are examined in this course, D2L ch. 20 or ch. 15–16 would need adding.

## Source hazard

> [!warning] Do not copy formulas from the PDF text
> The text layer deletes minus signs, arrows, $\eta$, $\lambda$, $\times$ and fraction bars, writes `;` for `,`, `j` for `|`, `2` for `∈`, `@` for `∂`, `:` for decimal points, and uses `1` for both $\infty$ and 1. Scalars, vectors and matrices all look the same. Example (book p. 87): `(w; b) (w; b)   jBj ∑ i2B t @(w;b)l(i)(w; b)` is
> $$(\mathbf w, b) \leftarrow (\mathbf w, b) - \frac{\eta}{|\mathcal B|}\sum_{i \in \mathcal B_t} \partial_{(\mathbf w, b)} \ell^{(i)}(\mathbf w, b)$$
> All formulas in these notes were rebuilt from the prose and checked numerically. Figures are images and do not extract; code loses its indentation.

## Cross-subject links

| Subject | Relationship |
|---|---|
| [[Machine Learning/contents/00-Index\|Machine Learning]] | owns reinforcement learning |
| [[Optimization/contents/00-Index\|Optimization]] | convexity and convergence theory; this subject uses the algorithms |
| [[Probability Theory/contents/00-Index\|Probability Theory]] | MLE and Gaussians behind the losses |
| [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] | estimation and testing behind generalization |
| [[Linear Algebra/contents/00-Index\|Linear Algebra]] | matrices, rank, conditioning |
| [[Calculus/contents/00-Index\|Calculus]] | the chain rule behind backprop |
| [[MLOps/contents/00-Index\|MLOps]] | training infrastructure and deployment |
| [[Data Preparation and Visualization/contents/00-Index\|Data Preparation and Visualization]] | preprocessing and augmentation |
| Computer Vision | overlaps ch. 05–06; this subject owns learned models, Computer Vision owns image formation, geometry and classical features |

## Discrepancies (none filed as errata)

A discrepancy is logged only after ruling out extraction errors, my own arithmetic, and alternative conventions.

| # | Where | D2L says | Finding | Verdict |
|---|---|---|---|---|
| D1 | §1.5, under Table 1.5.1 | compute has "outpaced" data growth | both grew $10^{10}$ over 1970–2020; true only from 2000 | declined: fine as a claim about recent decades |
| D2 | Table 1.5.1 | Iris = 100 examples | Iris has 150 | declined: table is rounded to powers of ten |
| D3 | §3.7.3–3.7.4 | caption `'L2 norm of w: '` | prints $\tfrac12\|\mathbf w\|^2$, not the norm | mislabel only; code is correct |
| D4 | §3.7.4 vs §3.7.3 | concise 0.012314 vs scratch 0.001473 "look similar" | different loss scaling and initialization; 40 updates cannot forget the init | not comparable; both outputs correct (ch. 02 §10) |
| D5 | §4.6.1 | Hoeffding ≈15,000 vs asymptotic 10,000 | one-sided vs two-sided; like-for-like 18,444 | declined: conclusion unchanged |
| D6 | §4.7.3 | confusion matrix as a joint frequency | the equation needs $c_{ij}=P(\hat y=i\mid y=j)$ | imprecise wording (ch. 03 §11.4) |
| D7 | §12.9.2 | $\rho=0.9$ gives "half-life of 10" | half-life 6.58; 10 is the effective sample size | loose terminology (ch. 04 §18) |
| D8 | §8.1.2 | AlexNet's dense layers need "nearly 1GB" | 208.0 MB of weights; 832.1 MB with gradients + Adam | true of training memory, not weights (ch. 05 §9) |
| D9 | §9.2.5 | n-gram Zipf exponent smaller, "depending on the sequence length" | unigram 0.7184, bigram 0.5703, trigram 0.6447 | smaller than unigram holds; not monotone, but ten ranks cannot decide (ch. 07 §4) |
