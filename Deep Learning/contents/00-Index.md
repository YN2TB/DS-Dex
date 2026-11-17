---
subject: Deep Learning
chapter: 00
tags: [ds, moc, deep-learning]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning (PyTorch edition); lecture slides by Dr. Nguyễn Thị Kim Ngân"
---

# Deep Learning — Map of Content

Notes for the Deep Learning course (Data Science, NEU). Sources: Zhang, Lipton, Li & Smola, *Dive into Deep Learning* (D2L), Cambridge University Press edition, PyTorch; and the lecturer's slides (Dr. Nguyễn Thị Kim Ngân), 16 decks in `slides/`.

## Scope

The eight topics come from the user's own syllabus (`note/Index.md`). D2L chapters are used as material for them; where a topic spans several chapters they are merged.

**Deep rework (done 2026-11-16).** Each note follows its D2L sections one by one, with their worked examples, D2L's PyTorch code and the printed outputs, recomputed where possible. Status 📗 = reworked.

**Slides merged (2026-11-17).** The full slide set turned up after the rework. The slides follow D2L closely (often its MXNet edition) and use Keras for case studies. Each note ends its main part with a "From the lecture slides" block holding only what the slides add: other notation, worked examples, Keras/MXNet code, YOLO, Luong attention, BERT/GPT. Slide errors are listed below (S1–S15). Status 📘 = reworked and checked against the slides.

| # | Note | Covers | Status |
|---|---|---|---|
| 01 | [[01 - Introduction to Deep Learning]] | data, model, objective, optimizer; kinds of learning; decisions vs argmax; why deep learning took off; derivatives, gradients, chain rule, autograd; lecture definitions | 📘 |
| 02 | [[02 - Linear Regression]] | squared loss as MLE; normal equations; minibatch SGD; Module/DataModule/Trainer; scratch and concise code; generalization; weight decay; lecture: samples-as-columns normal equation, house example, GD demo and exercises, NSE/R²/MAE/RMSE | 📘 |
| 03 | [[03 - Logistic Regression]] | softmax, cross-entropy, information theory; Fashion-MNIST, Classifier, scratch and concise code, LogSumExp; test-set size; distribution shift and corrections; lecture: binary logistic regression by MLE (study-hours fit), one-vs-rest, softmax gradient $\frac1N\mathbf X\mathbf E^\top$ | 📘 |
| 04 | [[04 - Neural Network]] | MLPs, activations, implementation, backprop, memory, vanishing/exploding gradients, initialization, dropout, Kaggle workflow; modules, parameters, custom layers, file I/O, GPUs; GD, Newton, SGD, minibatches, momentum to Adam, schedules; lecture: error-term backprop, MXNet ↔ PyTorch, Leaky ReLU, Keras BN/dropout, transfer learning | 📘 |
| 05 | [[05 - Convolutional Neural Network]] | convolution, padding, stride, channels, pooling with code; LeNet → AlexNet, VGG, NiN, GoogLeNet, batch/layer norm, ResNet, ResNeXt, DenseNet with code; design spaces and RegNet; lecture: Keras MNIST case study, data augmentation/synthesis/transfer overview | 📘 |
| 06 | [[06 - Object Detection]] | augmentation and fine-tuning with code; boxes, IoU, anchors, labelling, NMS with code; multiscale anchors; banana dataset; TinySSD with training and losses; R-CNN family; lecture: R-CNN/Faster R-CNN numbers, YOLO v1 | 📘 |
| 07 | [[07 - Recurrent Neural Network]] | sequence models and the sine experiment; text pipeline and Vocab; n-grams, Zipf, perplexity, partitioning; RNN, BPTT, clipping, LSTM, GRU, deep and bidirectional, each with code; lecture framing | 📘 |
| 08 | [[08 - Sequence to Sequence]] | MT data and loaders; encoder–decoder, GRU seq2seq, masked loss, BLEU; beam search; attention lookup, Nadaraya–Watson, masked softmax, additive and dot-product; Bahdanau; multi-head; positional encoding; Transformer, all with code; lecture: context-vector notation, attention by hand, Luong attention, BERT and GPT | 📘 |

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

### Lecture slides

Lecturer: Dr. Nguyễn Thị Kim Ngân. Course outline (deck 1): introduction, linear regression, logistic regression, gradient descent, neural networks, CNNs, RNNs, GANs.

**Assessment (deck 1):**
- Classwork 50%: attendance 10%; midterm 40% (exercises, in-class project or test).
- Final exam 50%: project or computer test.

**Reading list (deck 1):**
- Prince, *Understanding Deep Learning* (MIT Press 2023).
- Chollet, *Deep Learning with Python* (Manning 2017).
- D2L in Vietnamese (*Đắm mình trong học sâu*, d2l-vi).
- Nguyễn Thanh Tuấn, *Deep learning cơ bản*.
- machinelearningcoban.com.

| Deck | Pages | Note |
|---|---|---|
| 1 Introduction | 22 | 01 §11 |
| 2.1 Linear Regression | 18 | 02 §15, §17 |
| 2.2 Gradient Descent | 25 | 02 §16, ex. 6 |
| 3.1 Logistic Regression | 18 | 03 §15 |
| 3.2 Softmax Regression | 15 | 03 §16 |
| 4.1 Neural Network | 20 | 04 §33 |
| 4.2 Computing in deep learning (MXNet) | 14 | 04 §34 (and §15–17) |
| 4.3 Optimal Training | 29 | 04 §35 |
| 5.1 CNN | 44 | 05 §2–8, §19 |
| 5.2 Modern CNNs | 29 | 05 §9–16, §19 |
| 5.3 CNN Techniques | 17 | 05 §20 (and 06 §1–2) |
| 6 Object Detection | 33 | 06 §11, §13–14 |
| 7 RNN | 33 | 07 §6–11, §12 |
| 8 Encoder–Decoder | 15 | 08 §1–3, §11 |
| 9 Attention Mechanism | 28 | 08 §4–10, §12–13 |
| 10 GAN | 17 | not written: not examined (user, 2026-11-17) |

### Not covered

| D2L chapter | Reason |
|---|---|
| 2 Preliminaries (except 2.4–2.5) | covered by [[Linear Algebra/contents/00-Index\|Linear Algebra]], [[Probability Theory/contents/00-Index\|Probability Theory]], [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| 13 Computational Performance; 14.9–14.14 segmentation, style transfer, Kaggle | engineering ([[MLOps/contents/00-Index\|MLOps]]) or beyond the detection topic |
| 15–16 NLP | belongs to the separate (currently blocked) NLP subject; only the BERT overview (15.8, 15.10) is used, in 08 §13 |
| 17 Reinforcement Learning | covered in [[Machine Learning/contents/00-Index\|Machine Learning]] |
| 18 Gaussian Processes | not deep learning, not on the list |
| 19 Hyperparameter Optimization | MLOps territory |
| 20 GANs | the lecture has a GAN deck (10), but it is not examined (user, 2026-11-17); write it from deck 10 and D2L ch. 20 only if asked |
| Appendices | maths duplicates; tools not examinable |

> [!note] Settled by the slides (2026-11-17)
> GANs have a deck but are not examined. NLP appears only as BERT/GPT inside the attention deck, covered in 08 §13.

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

## Errata

Found during the deep rework by running D2L's own code (PyTorch 2.11).

| # | Where | D2L's code | What actually happens | Note |
|---|---|---|---|---|
| E1 | §6.5.2 `MyLinear` | `forward` uses `self.weight.data`, `self.bias.data` | output has no gradient; `backward()` raises an error, so the layer cannot be trained | printed forward values are fine (ch. 04 §19) |
| E2 | §12.11.3 multi-factor run | plots the schedule by stepping the same optimizer and scheduler 30 times, then trains | learning rate is already 0.125 and stays 0.125 for all 30 epochs | the printed 0.889 is a constant-rate run (ch. 04 §32) |

## Slide errors

Found while checking the lecture slides against D2L, the original papers and my own recomputation. They are flagged where they occur in the notes.

| # | Deck, page | Slide says | Correct | Note |
|---|---|---|---|---|
| S1 | 2.1 p14 | $\mathbf X$ gives house 4 age 36 | 30 (as in the table; the slide's $\mathbf w$ matches 30) | 02 §15 |
| S2 | 2.1 p15 | $\bar{\mathbf x}=[x_0,\dots,x_N]$ | index runs over features $m$ | 02 §15 |
| S3 | 2.2 p3–4 | a local minimum is where $f'=0$ | necessary only; also needs the sign change | 02 §16 |
| S4 | 2.2 p22 | $\frac1N\sum_j\mathbf x^{(j)}\nabla J_j$ | one $\mathbf x^{(j)}$ too many | 02 §16 |
| S5 | 2.1 p17 | $R^2$ as squared correlation, next to NSE | fine as a definition, but it ignores bias and scale | 02 §17 |
| S6 | 3.2 p15 | $-\frac1N(\sum\log a+\frac\lambda2\Vert\mathbf W\Vert_F^2)$ | penalty must be added: $-\frac1N\sum\log a+\frac\lambda2\Vert\mathbf W\Vert_F^2$ | 03 §16 |
| S7 | 4.1 p14–20 | two weight conventions without comment | both valid; don't mix | 04 §33 |
| S8 | 4.3 p12 | $\lambda$ small "to ensure the solution … is too far" | "is not too far" | 04 §35 |
| S9 | 4.3 p26 | $\mathbf x-\eta\operatorname{diag}(\mathbf H)^{-1}\nabla f$ called Newton | diagonal preconditioning (D2L §12.3.3) | 04 §35 |
| S10 | 5.1 p20 | avg(3,4,6,7) = 7, avg(4,5,7,8) = 8 | 5 and 6 (the slide's figure is right) | 05 §19 |
| S11 | 5.1 p39 | diagram: 28×28×32 maps, flatten 6,272 | the code (padding `valid`) gives 4,608; 6,272 needs `same` | 05 §19 |
| S12 | 6 p11 | R-CNN 53.3% "vs. 33% of previous methods" | the paper claims >30% *relative* gain; previous best ≈ 41% | 06 §13 |
| S13 | 6 p22 | Faster R-CNN 73.2% vs Fast R-CNN 66.9% | different training sets (07+12 vs 07); like-for-like 73.2 vs 70.0; COCO "42%" is AP@0.5 | 06 §13 |
| S14 | 6 p26 | YOLO backbone Darknet-19/53, neck FPN/PAN | later versions (v2, v3, v4+); v1 is 24 conv + 2 FC | 06 §14 |
| S15 | 8 p12; 9 p20, p27 | $O(\vert\mathcal Y\vert^{T})$; self vs multi-head as alternatives; GPT sketch with cross-attention | $T'$; independent axes; decoder-only has no cross-attention | 08 §11–13 |

S12–S14 rely on the original papers as I know them; I have not checked those papers against a PDF.

## Discrepancies (declined as errata)

A discrepancy is logged only after ruling out extraction errors, my own arithmetic, and alternative conventions.

| # | Where | D2L says | Finding | Verdict |
|---|---|---|---|---|
| D1 | §1.5, under Table 1.5.1 | compute has "outpaced" data growth | both grew $10^{10}$ over 1970–2020; true only from 2000 | declined: fine as a claim about recent decades |
| D2 | Table 1.5.1 | Iris = 100 examples | Iris has 150 | declined: table is rounded to powers of ten |
| D3 | §3.7.3–3.7.4 | caption `'L2 norm of w: '` | prints $\tfrac12\Vert \mathbf w\Vert ^2$, not the norm | mislabel only; code is correct |
| D4 | §3.7.4 vs §3.7.3 | concise 0.012314 vs scratch 0.001473 "look similar" | different loss scaling and initialization; 40 updates cannot forget the init | not comparable; both outputs correct (ch. 02 §11, §14) |
| D5 | §4.6.1 | Hoeffding ≈15,000 vs asymptotic 10,000 | one-sided vs two-sided; like-for-like 18,444 | declined: conclusion unchanged |
| D6 | §4.7.3 | confusion matrix as a joint frequency | the equation needs $c_{ij}=P(\hat y=i\mid y=j)$ | imprecise wording (ch. 03 §14.4) |
| D7 | §12.9.2 | $\rho=0.9$ gives "half-life of 10" | half-life 6.58; 10 is the effective sample size | loose terminology (ch. 04 §29) |
| D8 | §8.1.2 | AlexNet's dense layers need "nearly 1GB" | 208.0 MB of weights; 832.1 MB with gradients + Adam | true of training memory, not weights (ch. 05 §9) |
| D9 | §9.2.5 | n-gram Zipf exponent smaller, "depending on the sequence length" | unigram 0.7184, bigram 0.5703, trigram 0.6447 | smaller than unigram holds; not monotone, but ten ranks cannot decide (ch. 07 §4) |
| D10 | §12.3.3 | calls $\vert e^{(k+1)}\vert \le c(e^{(k)})^2$ "linear convergence" | standard name is quadratic; linear is $\vert e^{(k+1)}\vert \le\alpha\vert e^{(k)}\vert $ | names swapped, maths correct (ch. 04 §23) |
| D11 | §8.6.5 vs code | `ResNeXtBlock(..., groups, ...)` described as the number of groups $g$ | code passes `bot_channels // groups` to the conv, so the argument is the group width (`ResNeXtBlock(32, 16, 1)` has 2 groups) | naming inconsistency; §8.8 uses group width, matching the code (ch. 05 §15) |
| D12 | §9.3.3 prose vs code | random offset $d$ each epoch, non-overlapping subsequences covering the corpus | code uses all stride-1 windows, no offset; train = windows starting 0–9,999 (tokens 0–10,031, 5.8% of the book), val = 10,000–14,999; 32 tokens shared | demo loader; prose describes a different scheme (ch. 07 §5) |
| D13 | §10.7.8 | $p_n^{1/2^n}$ rising with $n$ means BLEU "assigns a greater weight" to long n-grams | exponent of $\log p_n$ is $1/2^n$, so long n-grams count less (factors 0.707 → 0.958 at $p_n=0.5$); original BLEU uses $p_n^{1/N}$, not $p_n^{1/n}$ | interpretation reversed; formula correct (ch. 08 §2) |
| D14 | §10.8.3 | the $L^\alpha$ denominator "penalizes long sequences" | the raw log-probability sum penalizes length; dividing by $L^\alpha$ favours longer candidates | wording reversed; formula correct (ch. 08 §3) |
