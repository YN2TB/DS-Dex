# CLAUDE.md — Deep Learning

Subject-specific context. Read this plus the root `CLAUDE.md`; nothing else.

## Status

**🚧 In progress.** `00-Index.md` written. Chapters: **01–03 done**, 04–08 pending. **Next: ch. 04 — Neural Network (D2L ch. 5 + ch. 6 + ch. 12 optimizers).**

## Source

| | |
|---|---|
| Book | Zhang, Lipton, Li & Smola, *Dive into Deep Learning* (D2L), Cambridge UP print edition |
| File | `documents/Dive into Deep Learning.pdf` |
| Pages | 1185 PDF pages; 20 chapters + Appendix A (Mathematics) + Appendix B (Tools) |
| Framework | PyTorch (this printing is the PyTorch edition) |
| **Page offset** | **PDF page = book page + 40.** Verified: book p. 83 = PDF p. 123; book p. 87 = PDF p. 127. Front matter is roman-numbered separately (Notation = PDF p. 37). |

**There is exactly one source and no slides.** But the scope is *not* an editorial guess — see below.

## Scope — given by the user, not chosen by me

`note/Index.md` (user-written, in the user's own folder) lists **eight course topics**. That is the syllabus, so the vault's usual "pick a standard scope and flag it for confirmation" procedure does **not** apply here. The eight notes are built to that list; D2L chapters are the *raw material*, mapped onto it.

| Note | User's topic | D2L sections used |
|---|---|---|
| 01 | Introduction to Deep Learning | ch. 1 entire; ch. 2.4–2.5 (calculus, autodiff) as needed |
| 02 | Linear Regression | 3.1–3.7 (incl. minibatch SGD, generalization, weight decay) |
| 03 | Logistic Regression | 4.1–4.7 (softmax regression = multiclass logistic, cross-entropy, information theory, distribution shift) |
| 04 | Neural Network | ch. 5 entire (MLP, activations, forward/backprop, vanishing & exploding gradients, init, dropout); ch. 6 (parameter management, custom layers); ch. 12 optimizers (momentum, AdaGrad, RMSProp, Adam) folded in as *training* |
| 05 | Convolutional Neural Network | ch. 7 entire; ch. 8 (AlexNet, VGG, NiN, GoogLeNet, batch norm, ResNet, DenseNet) |
| 06 | Object Detection | 14.1–14.8 (augmentation, fine-tuning, bounding boxes, anchor boxes, IoU, NMS, multiscale, SSD, R-CNN family) |
| 07 | Recurrent Neural Network | ch. 9 entire; 10.1–10.4 (LSTM, GRU, deep, bidirectional) |
| 08 | Sequence2sequence | 10.5–10.8 (MT, encoder–decoder, seq2seq, BLEU, beam search); **plus ch. 11.1–11.7 attention & Transformer** |

**Two scope calls that are mine and are flagged in `00-Index.md`:**
1. **Optimizers (D2L ch. 12) have no topic of their own**, so momentum/AdaGrad/RMSProp/Adam go inside note 04 rather than being dropped. A DL course that never names Adam would be strange.
2. **Attention and the Transformer (ch. 11) are folded into note 08.** Seq2seq without attention stops the story exactly where the field turned. Labelled as an extension in that note's gaps callout.

**Not covered, with reasons**, in `00-Index.md`: ch. 13 (computational performance / multi-GPU), 15–16 (NLP pretraining & applications — the vault has a separate blocked NLP subject), 17 (RL — already covered by `Machine Learning` ch. 01–10), 18 (Gaussian processes), 19 (HPO), 20 (GANs), Appendices A–B.

## ⚠️ Extraction quirks — READ BEFORE QUOTING ANY FORMULA

Prose and code extract well. **Display mathematics is mangled destructively and silently.** Confirmed on PDF pp. 37, 127, 128.

| In the PDF text | Actually means | Note |
|---|---|---|
| *(nothing)* | `←` assignment arrow | **DELETED.** `(w; b) (w; b)` is $(\mathbf w,b)\leftarrow(\mathbf w,b)$ |
| *(nothing)* | `−` minus sign | **DELETED.** `b  y(i)` is $b - y^{(i)}$ |
| *(nothing)* | `η`, and fraction bars | **DELETED.** `  \n jBj` is $\frac{\eta}{|\mathcal B|}$ |
| `;` | `,` | in subscripts and tuples: `xi; j` is $x_{i,j}$; `(w; b)` is $(\mathbf w, b)$ |
| `j` | `|` | `jBj` is $|\mathcal B|$; `E[Y j X]` is $E[Y\mid X]$ |
| `:` | `.` | **decimal points.** `0:2` is $0.2$ — reads as a ratio if you miss it |
| `1` | `∞` | **⚠️ AND `1` also still means literal 1, in the same passage.** See the worked case below. |
| `!` | `→` | `!1` is $\to\infty$; `! max(a,b)` is $\to\max(a,b)$ |
| *(nothing)* | `λ` | **DELETED**, like `η`. `1RealSoftMax(a; b)` is $\lambda^{-1}\mathrm{RealSoftMax}(\lambda a,\lambda b)$ |
| `2` | `∈` | `i2B t` is $i \in \mathcal B_t$ |
| `@` | `∂` | `@(w;b)l` is $\partial_{(\mathbf w,b)}\ell$ |
| `1 1` | `1 × 1` | multiplication sign deleted (TOC 7.4.3) |
| superscripts inline | flattened | `w⊤x(i)` is $\mathbf w^\top \mathbf x^{(i)}$ |
| **bold / blackboard** | **lost entirely** | the notation page prints scalar `x`, vector `x`, matrix `X`, tensor `X` — **all four extract as the same glyph.** Type must be inferred from context. |

**⚠️ THE CIPHER IS NOT A FIXED SUBSTITUTION — exactly the Mankiw hazard, found on book p. 10 (PDF p. 51).** Two adjacent sentences of the mushroom example:

- `0:21 + 0:8 0 =1` is $0.2 \times \infty + 0.8 \times 0 = \infty$ — here **`1` is `∞`**
- `0:2 0 + 0:8 1 = 0:8` is $0.2 \times 0 + 0.8 \times 1 = 0.8$ — here **`1` is a genuine 1**

Both are ASCII `0x31`. Verified by codepoint inspection. **There is no mechanical decoder — you must know the mathematics to read the formula.**

**⇒ THE RULE, same one Mankiw forced in Macro/Micro: never transcribe a formula from the extraction. Reconstruct it from the prose and the mathematics, then verify numerically against the book's own printed figures.** A deleted minus sign turns a correct equation into a plausible wrong one with no visible damage — exactly the vault's recurring "plausible wrong answer with no error" failure.

Other quirks:
- **Inter-word spaces collapse in justified paragraphs** (`Insummary,minibatchSGDproceeds…`). Harmless — readable, and word boundaries are unambiguous.
- **Code blocks extract with correct tokens but indentation is LOST** — same hazard as Goodrich in DSA. A `for` body appears flush left. Never copy a listing verbatim; re-indent from the logic.
- **`ﬁ ﬂ ﬀ` ligatures survive as single glyphs** (`deﬁne`, `diﬀerent`) — cosmetic.
- **All figures are images and never extract.** D2L is figure-heavy (architecture diagrams). Apply the vault's figure rule: label-schematics are often reconstructable because the prose names every box; plotted curves are lost.
- **Printed code *outputs* extract** (e.g. `'0.16781 sec '`), which makes several claims numerically checkable.

## Errata

**None filed. Six discrepancies investigated and declined** (all logged in `contents/00-Index.md`): D1 the "compute outpaced data" sentence under Table 1.5.1; D2 Iris listed as 100 in an order-of-magnitude table; D3 the `'L2 norm of w: '` caption that prints ½‖w‖²; D4 the concise-vs-scratch weight-decay values that are 8.4× apart and not comparable; **D5** the 15,000-vs-10,000 test-set comparison that mixes a one-sided Hoeffding bound with a two-sided asymptotic interval (like-for-like is 18,444); **D6** the confusion matrix described as a joint frequency when the linear system needs the column-conditional one.

## Findings worth keeping

- **ch. 01 — THE SOURCE'S PROSE AND ITS OWN TABLE DISAGREE, and dividing the columns is what exposes it.** Table 1.5.1 over 1970–2020: data ×10¹⁰, compute ×10¹⁰, memory ×10⁸. So D2L's "memory has not kept pace" is **true and equals exactly 100×**, while "compute has outpaced datasets" is **false over the span — the ratio is 1.000** (true only from 2000 on). Per example: **memory fell from 10 B to 0.1 B (÷100) while compute is 1000 FLOP/s in both 1970 and 2020 — literally unchanged.** ⇒ the shift from kernel methods to deep nets was forced by the **memory** collapse, not a compute windfall: a kernel method needs O(n²) pairwise structure and at n = 10¹² with 0.1 B/example that is arithmetically impossible. *Deep networks won because they stream data they cannot store.* **This is the vault's standing "divide the source's adjacent figures" move and it paid on the first chapter of the subject.**
- **ch. 01 — a claim the source ASSERTS, verified by computing the case (the vault's standing template).** D2L dates the neural-network winter to **1995–2005** and blames cost. Test it against D2L's *own* memory column: one dense layer from 1 s of 44 kHz audio into 1,000 hidden units is **44,001,000 parameters = 176 MB at fp32** — short of the 1990 row by **17.6×**, still short of the 2000 row by **1.76×**, and first fitting in the **2010** row. The $200\times200\times3$ image version is **480 MB**, exceeding the entire 2000 budget by 4.8×. **The dating is corroborated and its mechanism sharpened, and it settles the "rediscovery" question: MLPs (1943), CNNs (1998), LSTM (1997) were resource-blocked, not idea-blocked.** Counting only forward weights makes this a *lower* bound (gradients + Adam state ≈ 3–4× more).
- **ch. 01 — generalise the toy example before believing its magnitude (Marketing's template, reused).** D2L computes the mushroom decision once, at $L=\infty$. Replacing it with a finite penalty gives **eat iff $p < 1/(L+1)$** — the tolerable risk falls like $1/L$: 20% at $L=4$, 0.99% at $L=100$, 0.0999% at $L=1000$. D2L's own 0.2 sits exactly at indifference for $L=4$. **`argmax` is optimal only under 0–1 loss; reporting the most likely class silently asserts $L=1$.**
- **ch. 02 — THE VAULT'S "ACCURATE NUMBER THAT MEANS SOMETHING ELSE" PATTERN, in a new setting, and it is the best result of the subject so far.** D2L's weight-decay experiment (d=200, n=20, true wᵢ=0.01) prints `l2_penalty(w)` = **0.009889** for λ=0, labelling that run "a textbook case of overfitting". **The true value of that printed quantity is exactly ½·200·0.01² = 0.0100 — the overfitting run is 1.11% from the truth.** Reproduced independently in NumPy over 200 seeds (0.01007, within 1.8%), which also gives what D2L never prints: **‖ŵ − w_true‖ = 0.1907, LARGER than ‖w_true‖ = 0.1414 itself, at cosine 0.092 ≈ 84.7° away.** The λ=3 run is 7× too short and yet closer (0.1410), twice as aligned (0.195), and generalizes 1.76× better (val 0.01096 vs 0.01924). ⇒ ***a norm is one number summarizing 200 and is blind to direction; with 20 examples in 200 dimensions the fit is pinned only inside the 20-dim span of the data and the other 180 directions are noise.*** **Hunt for more cases where a summary statistic is exactly right while the thing it summarizes is exactly wrong** — this is the same structure as Commercial Banking's correlation results.
- **ch. 02 — READ WHAT THE CODE PRINTS, NOT WHAT THE CAPTION SAYS.** D2L prints `'L2 norm of w: '` but computes `(w**2).sum()/2` = **½‖w‖², not ‖w‖**. Printed values differ 6.72×; the actual norms differ **2.59×**. *New general rule: when a source prints a number, find the line that computed it.*
- **ch. 02 — TWO NUMBERS PRINTED ADJACENTLY THAT CANNOT BE COMPARED.** Concise `wd=3` prints **0.012314** vs scratch `λ=3`'s **0.001473** — 8.4× apart at the same nominal λ, and the book says only "the plot looks similar". Cause, established by simulation: `nn.MSELoss` omits the ½ (halves effective λ) **and** `nn.LazyLinear` starts at ½‖w‖² ≈ 0.1667 vs scratch's 0.0100, and **40 SGD updates for 200 parameters cannot forget the initialization** — pure decay predicts 0.1667×(1−ηλ)^80 = 0.0146; full simulation gives 0.0140 vs printed 0.0123. ⇒ ***before interpreting any trained quantity, ask how many steps produced it.***
- **ch. 02 — the vectorization benchmark, divided (the standing "divide adjacent figures" move).** `0.16781 sec` vs `0.00180 sec` ⇒ **93.23×**; per element **16.781 µs vs 0.180 µs**, so at ~10⁹ adds/sec one addition is **0.0060% of the loop's cost — 99.994% is interpreter overhead** — and only **0.56%** of the vectorized cost. Book says "order-of-magnitude speedups" and never divides.
- **ch. 03 — THE SAME RULE FIRED TWICE IN UNRELATED SETTINGS, TWO CHAPTERS APART: NEVER REPORT RANK OR INVERTIBILITY WHERE CONDITIONING DECIDES THE ANSWER.** D2L says label-shift correction works "if our classifier is sufficiently accurate, then the confusion matrix C will be invertible". Built the worked example the book omits: C with κ=1.50 recovers p=(0.2,0.3,0.5) exactly from μ=Cp and gives weights β=(0.4,1.0,2.5). **With a near-useless classifier, κ=104, adding 0.005 of sampling noise to μ returns p̂=(0.100,0.800,0.100) — error 0.648 against 0.0098, a 65.9× amplification — and p̂ is still a VALID PROBABILITY VECTOR: non-negative, sums to 1, nothing errors.** Pairs exactly with ch. 02 ex. 4 (full-rank design, det=4, κ=312, a 0.1 nudge moving w by 0.20 and flipping a coefficient's sign). ⇒ ***hunt for a third setting; this is the vault's "plausible wrong answer with no error" finding in linear-algebra form.***
- **ch. 03 — the naive label-shift estimate understates exactly the class the shift made important.** Using the model's mean output μ directly as the label distribution gives (0.225,0.335,0.440) vs truth (0.2,0.3,0.5): **+12.5% / +11.7% / −12.0%**. The confusion matrix is what separates "what the model said" from "what is there".
- **ch. 03 — cross-chapter check on ch. 01's Table 1.5.1, and it HALF FAILS.** D2L §4.2 says a 1995 Sun SPARCStation 5 (**64 MB, 5 MFLOPS**) was state of the art for ML at Bell Labs. Against the table's 1990 row (10 MB, 10 MF): memory 6.4× — sensible — but **compute 0.5×, i.e. the 1995 machine was slower than the table's 1990 figure ⇒ the table's compute column is optimistic.** Also: MNIST's 60,000 28×28 images are **47.04 MB = 73.5% of that machine's entire RAM**, and **2.94× the whole machine as float32** — an independent second data point for ch. 01 ex. 5's "the winter was a memory constraint" argument.
- **ch. 03 — two more cipher entries, both new: `!` is `→`, and `λ` is DELETED like η.** D2L ex. 5.4 extracts as `Showthatfor !1 wehave 1RealSoftMax(a; b)! max(a; b)` = "for λ→∞ we have λ⁻¹RealSoftMax(λa,λb)→max(a,b)" — **three deletions and two substitutions in one line.** The `1`-means-`∞` hazard recurs in ex. 7.3 ("temperature approach `1`").
- **ch. 03 — D2L's own test-set arithmetic all checks out and its aside is the useful part.** Bernoulli variance ≤0.25 ⇒ **2,500** for one sd of 0.01, **10,000** for two, Hoeffding **14,979**. The line worth keeping: *"thousands of applied deep learning papers get published every year making a big deal out of error rate improvements of 0.01 or less"* — which on a 10,000-example test set is the width of the interval. **Caveat the book supplies: near zero error the Bernoulli variance collapses and 0.01 is real.**
- **ch. 02 — full rank is a yes/no test and conditioning is what bites.** A 4×3 design with corr(area,age)=0.894 is *full rank* (det=4) and already κ(XᵀX)=**312**; a 0.1 nudge in one label moves w by **0.2016**, ridge (λ=1) cuts that to **0.0278** — **7.25×** — and **flips the sign of a coefficient** (−1.5 → +0.857). SVD form: ridge shrinks direction j by **σⱼ²/(σⱼ²+λ)** = 0.977 / 0.401 / 0.121 here. *D2L's exercise 4 asks what goes wrong and gives no answer.*
