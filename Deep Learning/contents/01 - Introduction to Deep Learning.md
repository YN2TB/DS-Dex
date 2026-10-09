---
subject: Deep Learning
chapter: 1
tags: [ds, deep-learning, machine-learning, foundations]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning, ch. 1 (book pp. 1–29); §2.4–2.5 for calculus and autodiff"
---

# Introduction to Deep Learning

## 📘 Main Knowledge

### 1. When machine learning is needed

Most software is a fixed set of rules written by a developer who can list and test every case. D2L's rule of thumb: if you can write a solution that works 100% of the time, you do not need machine learning.

Rule-writing fails in two situations:

1. The right answer changes over time (tomorrow's weather).
2. We can do the task but cannot say how (recognizing a cat in pixels, hearing a wake word).

In the second case we cannot write the program, but we can judge its output, so we can label data. Machine learning uses this: write a flexible program with adjustable parameters and let data choose them.

### 2. The four components

| # | Component | What it is | Later chapters |
|---|---|---|---|
| 1 | Data | the examples we learn from | [[02 - Linear Regression]], [[06 - Object Detection]] |
| 2 | Model | maps inputs to outputs | all |
| 3 | Objective function | a number measuring how badly the model does | [[02 - Linear Regression]], [[03 - Logistic Regression]] |
| 4 | Optimization algorithm | adjusts parameters to reduce the objective | [[04 - Neural Network]] |

Vocabulary:

- An **example** (data point, sample) is one observation; its **features** (covariates, inputs) are what we see; its **label** (target) is what we predict. The label is not an input.
- A program with fixed parameters is a **model**; varying the parameters gives a **family of models**; the procedure that picks parameters from data is the **learning algorithm**.
- If every example has the same number of features, that number is the **dimensionality**. A $200\times200$ colour image has $200 \times 200 \times 3 = 120{,}000$ values; one second of 44 kHz audio has 44,000.

Many inputs have variable length (images of different sizes, reviews of different lengths). Cropping to a fixed size loses information. Handling variable-length data well is one advantage of deep learning; see [[07 - Recurrent Neural Network]] and [[08 - Sequence to Sequence]].

Data quality affects more than accuracy. A skin-cancer model trained without dark-skinned patients fails on them; a résumé screener trained on past hiring decisions reproduces past bias. This can happen without anyone intending it.

### 3. Objective functions

By convention the objective is defined so that lower is better, which is why it is called a **loss**. A "higher is better" score becomes a loss by flipping the sign.

- **Regression** uses squared error $(\hat y - y)^2$, justified by Gaussian noise in [[02 - Linear Regression]].
- **Classification** really cares about error rate, but error rate is a step function with zero gradient almost everywhere. We optimize a differentiable surrogate, cross-entropy ([[03 - Logistic Regression]]).

During optimization the loss is a function of the parameters, with the training data held fixed.

**Training and test sets.** Training performance is like a score on practice exams; a student who memorizes the practice questions fails new ones. That is overfitting ([[02 - Linear Regression]], [[04 - Neural Network]]).

**Optimization.** Almost every deep learning optimizer descends from gradient descent: compute how the loss changes with each parameter and move each one in the direction that lowers it.

### 4. Kinds of learning problems

#### 4.1 Supervised learning

Given features and labels, learn to predict labels from features, i.e. estimate $P(\text{label} \mid \text{features})$. Most industrial ML is supervised.

| Problem type | Question | Target | Typical loss |
|---|---|---|---|
| Regression | how much? | a number | squared error |
| Classification | which one? | one of $k$ classes | cross-entropy |
| Tagging (multi-label) | which ones? | a subset of classes | per-label cross-entropy |
| Search / ranking | in what order? | a permutation | ranking losses |
| Recommendation | which, for this user? | personalized score | rating/ranking losses |
| Sequence learning | variable in, variable out | a sequence | [[08 - Sequence to Sequence]] |

The problem type is set by the form of the target, not by the algorithm.

D2L's contractor example: \$350 for 3 hours and \$250 for 2 hours, with cost $= w\cdot\text{hours} + b$:
$$3w + b = 350,\quad 2w + b = 250 \;\Longrightarrow\; w = 100,\; b = 50$$
Two points determine two parameters exactly. With more data than parameters there is usually no exact solution, and we minimize squared error instead. That move from solving to minimizing is where [[02 - Linear Regression]] begins.

**Classification** models output a probability per class. In hierarchical classification some mistakes are worse than others: confusing two dog breeds is cheap, confusing a rattlesnake with a garter snake is not.

> [!warning] The most likely class is not the decision
> D2L's mushroom: the classifier says $P(\text{death cap}) = 0.2$, so it is 80% sure the mushroom is safe.
> $$\mathbb{E}[\text{loss} \mid \text{eat}] = 0.2 \times \infty + 0.8 \times 0 = \infty,\qquad \mathbb{E}[\text{loss} \mid \text{discard}] = 0.2 \times 0 + 0.8 \times 1 = 0.8$$
> Discard it. Decisions need the probabilities and the costs. Reporting the argmax class assumes every mistake costs the same (0–1 loss).

With a finite penalty $L$ for eating a poisonous mushroom and cost 1 for discarding a good one, eat only if
$$pL < (1-p) \iff p < \frac{1}{L+1}$$
At $L=4$ the threshold is exactly 0.2; at $L=100$ it is 0.99%; at $L=1000$, 0.0999%. The acceptable risk falls roughly like $1/L$, which is why screening and fraud problems are not thresholded at 0.5.

#### 4.2 Unsupervised and self-supervised learning

No labels; the questions depend on what you want to know:

- **Clustering**: summarize the data with a few prototypes.
- **Subspace estimation**: a few parameters capturing the important variation (linear case: PCA, see [[Linear Algebra/contents/00-Index|Linear Algebra]]).
- **Embeddings**: representations where relations hold, e.g. "Rome" − "Italy" + "France" ≈ "Paris".
- **Causality and graphical models**: causes, not just correlations.
- **Deep generative models**: estimate the data density and score or sample examples. VAEs (2014), GANs (2014), normalizing flows, and diffusion models (2015, 2020), which have largely replaced GANs in systems such as DALL·E 2 and Imagen.

**Self-supervised learning** creates labels from unlabeled data: predict masked words (BERT), predict the relative position of two image crops, or decide whether two images are perturbations of the same one. The learned representation is then fine-tuned on a downstream task.

#### 4.3 Interacting with an environment

The settings above are offline: collect data once, fit, done. Once a model's actions affect the world, new questions arise: does the environment remember past actions, does it cooperate or work against you (a spammer), does it change over time? These lead to **distribution shift**, where training and test data differ. D2L's analogy: homework written by the TAs, exam written by the lecturer. See [[03 - Logistic Regression]].

#### 4.4 Reinforcement learning

An agent takes actions, receives observations and rewards, and follows a **policy** (observations → actions). Supervised learning is a special case (one action per class, reward = negative loss). RL adds:

- **Credit assignment**: in chess the only reward may be win/lose at the end, and you must work out which moves earned it.
- **Partial observability**: the agent may not see the full state.
- **Exploration vs. exploitation**.

| Setting | Condition |
|---|---|
| RL | general case |
| Markov decision process | environment fully observed |
| Contextual bandit | state does not depend on previous actions |
| Multi-armed bandit | no state, only actions with unknown rewards |

RL is covered in full in [[Machine Learning/contents/00-Index|Machine Learning]] and not developed here.

### 5. Origins

The statistical tools are old: the Bernoulli distribution (Jacob Bernoulli, 1655–1705), the Gaussian and least squares (Gauss, 1777–1855). Jacob Köbel (1460–1533) estimated the length of a foot by averaging the feet of 16 men leaving church, then improved it by dropping the shortest and longest feet: an early trimmed mean. (Mine: dropping one per tail keeps 87.5% of the sample and tolerates one corrupt measurement, a breakdown point of 1/16 = 6.25%.)

Fisher (1890–1962) gave us linear discriminant analysis, the Fisher information and the Iris dataset (1936); D2L notes he was also a eugenicist. Shannon founded information theory, and Turing (1950) proposed the Turing test.

**The name "neural network" is historical.** Hebb (1949) proposed that neurons learn by reinforcement, which inspired Rosenblatt's perceptron and, eventually, SGD. Two ideas survive from the biology, and they are the core of the course:

1. Alternating linear and nonlinear layers ([[04 - Neural Network]]).
2. Using the chain rule (backpropagation) to update all parameters at once ([[04 - Neural Network]], [[Calculus/contents/00-Index|Calculus]]).

**The winter, 1995–2005.** Neural networks fell out of favour because training was expensive and datasets were small (Iris was still a benchmark, MNIST's 60,000 images counted as huge). Kernel methods, decision trees and graphical models worked better under those limits, trained quickly, and came with theoretical guarantees.

### 6. Why deep learning took off

Data grew (the web, sensors, cheap storage), and compute grew (Moore's law, GPUs built for games). D2L's Table 1.5.1:

| Decade | Dataset (examples) | Memory | FLOP/s |
|---|---|---|---|
| 1970 | 100 (Iris) | 1 KB | 100 KF (Intel 8080) |
| 1980 | 1 K (Boston house prices) | 100 KB | 1 MF (Intel 80186) |
| 1990 | 10 K (OCR) | 10 MB | 10 MF (Intel 80486) |
| 2000 | 10 M (web pages) | 100 MB | 1 GF (Intel Core) |
| 2010 | 10 G (advertising) | 1 GB | 1 TF (NVIDIA C2050) |
| 2020 | 1 T (social network) | 100 GB | 1 PF (NVIDIA DGX-2) |

D2L concludes that memory has not kept up with data, and that compute has outpaced data. Dividing the columns (my analysis):

- From 1970 to 2020, data grew $10^{10}$, memory $10^{8}$, compute $10^{10}$.
- Memory per example fell from 10 B to 0.1 B, a 100× drop. The first claim holds.
- Compute per example is 1000 FLOP/s in both 1970 and 2020. The second claim holds only from 2000 on (it dips to 100 in 2000–2010).

| Decade | Data | Memory | Compute |
|---|---|---|---|
| 1970→80 | ×10 | ×100 | ×10 |
| 1980→90 | ×10 | ×100 | ×10 |
| 1990→2000 | ×1000 | ×10 | ×100 |
| 2000→10 | ×1000 | ×10 | ×1000 |
| 2010→20 | ×100 | ×100 | ×1000 |

The memory result supports D2L's main conclusion. With 0.1 byte of RAM per example you cannot store the data, let alone the $O(n^2)$ pairwise structure of a kernel method. A neural network of fixed size can stream examples past it, so its memory cost depends on parameters, not data size.

Many core ideas waited for resources: MLPs (McCulloch & Pitts, 1943), LSTM (1997), CNNs (LeCun et al., 1998), Q-learning (1992).

**Genuinely new ideas** of the deep learning era:

- **Dropout** (2014): regularization by injecting noise during training ([[04 - Neural Network]]).
- **Attention** (Bahdanau et al., 2014): increase a model's memory without adding parameters, using a learnable pointer into stored states instead of one fixed-size summary ([[08 - Sequence to Sequence]]).
- **Transformer** (2017): attention only, scales well with data, parameters and compute ([[08 - Sequence to Sequence]]).
- **Large language models**, aligned to human intent (ChatGPT, Ouyang et al. 2022).
- **GANs** (2014): a generator trained until a discriminator cannot tell fake from real.
- **Diffusion models**: learn to reverse a noising process.
- **Distributed training**: 1,024 GPUs × 32 images = 32,768 per batch; batches of 64,000 cut ResNet-50 on ImageNet from days to under 7 minutes.
- **Frameworks**: Caffe/Torch/Theano → TensorFlow/CNTK/MXNet → imperative tools (Chainer, PyTorch, Gluon, JAX).

### 7. Applications

ML has been used for decades in mail sorting (the origin of MNIST), cheque reading, credit scoring and fraud detection. More visible results: voice assistants, speech recognition at human parity on some tasks, games (TD-Gammon, Deep Blue, AlphaGo in 2015, Libratus in poker), and partial self-driving where deep learning handles mainly perception.

ImageNet top-5 error fell from 28% (2010) to 2.25% (2017): 12.44× fewer errors, or 2,800 → 225 mistakes per 10,000 images. (Human top-5 error is usually quoted around 5%.)

D2L's view on AI risk: current systems are built for specific goals and cannot redesign themselves. The real concerns are everyday ones: job automation and bias in consequential decisions.

### 8. What deep learning is

Deep learning is machine learning with many-layered neural networks. Every ML pipeline has several stages; what is different here is that **all layers are learned jointly from data** (end-to-end training).

Before deep learning, computer vision relied on hand-designed features such as the Canny edge detector (1987) and SIFT (2004), fed into a shallow model. Learned filters replaced them with better accuracy; [[05 - Convolutional Neural Network]] shows a trained CNN learning edge detectors by itself.

Consequences:

1. One toolkit now covers vision, speech, NLP and medical data, because domain-specific feature engineering is gone.
2. A move from parametric models with strong assumptions to flexible models fitted to large data, often at the cost of interpretability.
3. Acceptance of nonconvex optimization and of trying methods before proving them.

## ✏️ Exercises

> [!example]- **1.** *(Easy) The contractor*
> **(a)** \$350 for 3 hours, \$250 for 2 hours, cost $= w\cdot\text{hours}+b$. Find $w, b$ and predict 5 hours.
> **(b)** A third invoice: \$500 for 4 hours. Show no line fits all three, then find the least-squares line and its 5-hour prediction.
> **(c)** What does (b) tell you?
>
> ---
> **(a)** Subtracting the equations: $w=100$, then $b=50$. Five hours: \$550.
>
> **(b)** The line from (a) predicts \$450 for 4 hours, not \$500. Minimizing $\sum_i (wh_i+b-c_i)^2$ over $(3,350),(2,250),(4,500)$ gives $w=125$, $b=-\tfrac{25}{3}\approx-8.33$. Residuals $+\tfrac{50}{3}, -\tfrac{25}{3}, -\tfrac{25}{3}$ sum to zero; SSE $=\tfrac{1250}{3}\approx 416.67$. Five hours: $\tfrac{1850}{3}\approx\$616.67$.
>
> **(c)** The negative intercept is physically meaningless, a sign that something outside the features affects cost. With more examples than parameters there is no exact solution, and the objective function decides which imperfect fit to prefer.

> [!example]- **2.** *(Easy) Classify the problem*
> Name the problem type and say what an example, its features and its label are.
> (a) Predicting surgery duration. (b) Auto-tagging blog posts. (c) Transcribing a 3-second audio clip. (d) A robot vacuum learning a new flat. (e) Predicting hidden words in Wikipedia.
>
> ---
> **(a)** Regression. Example: one surgery; features: patient and procedure data; label: minutes.
>
> **(b)** Tagging (multi-label). Label is a subset of tags (a binary vector). Tags are correlated, which plain multi-class classification cannot express.
>
> **(c)** Sequence-to-sequence (speech recognition). 3 s at 44 kHz is 132,000 samples mapping to a few words, with no one-to-one alignment.
>
> **(d)** Reinforcement learning, likely partially observed. Actions change what the agent sees next and it gets rewards, not correct answers.
>
> **(e)** Self-supervised learning. Example: a sentence with a masked token; label: the hidden word (BERT's objective).

> [!example]- **3.** *(Medium) Decisions are not argmax*
> A classifier gives $P(\text{malignant}) = p$. Missing a cancer costs $L$; an unnecessary follow-up costs 1.
> **(a)** Above what $p$ should you refer? **(b)** Evaluate for $L = 4, 100, 1000$. **(c)** At $L=100$ a colleague says the model is 97% sure it is benign, so discharge. Respond. **(d)** Which of the four components does $L$ belong to?
>
> ---
> **(a)** Refer costs $(1-p)$, discharge costs $pL$. Refer if $p > 1/(L+1)$.
>
> **(b)** 20%, 0.990%, 0.0999%.
>
> **(c)** $p = 3\% > 0.990\%$: refer. The colleague used a 50% threshold, which assumes $L=1$.
>
> **(d)** The objective function. Argmax is optimal only under 0–1 loss; the mushroom is the case $L=\infty$, where any positive $p$ means discard.

> [!example]- **4.** *(Medium–hard) Audit Table 1.5.1*
> **(a)** Total 1970→2020 growth of data, memory, compute. **(b)** Test D2L's two claims. **(c)** Memory and compute per example in 1970 and 2020. **(d)** Why is D2L's conclusion (kernel methods → deep networks) still right?
>
> ---
> **(a)** Data $10^2\to10^{12}$ ($10^{10}$); memory $10^3\to10^{11}$ B ($10^8$); compute $10^5\to10^{15}$ ($10^{10}$).
>
> **(b)** Memory lagging data: true, by a factor of 100. Compute outpacing data: false over the full span (ratio 1.000); true only after 2000.
>
> **(c)** Memory: 10 B → 0.1 B per example. Compute: 1000 → 1000 FLOP/s per example.
>
> **(d)** It rests on the memory result. A kernel method needs $O(n^2)$ storage ($10^{24}$ entries at $n=10^{12}$); a fixed-size network streams data and needs memory only for its parameters.

> [!example]- **5.** *(Hard) Recompute the winter*
> Test D2L's 1995–2005 dating against Table 1.5.1.
> **(a)** One second of 44 kHz audio into a dense layer of 1,000 units: parameters and float32 bytes? **(b)** When does it first fit in RAM? **(c)** Same for a $200\times200\times3$ image. **(d)** What does this say about the dating? **(e)** Why is this a lower bound?
>
> ---
> **(a)** $44{,}000\times1{,}000+1{,}000 = 44{,}001{,}000$ parameters ≈ 176 MB.
>
> **(b)** 1990 (10 MB) is 17.6× too small, 2000 (100 MB) 1.76× too small; it first fits in 2010 (1 GB).
>
> **(c)** 120,001,000 parameters ≈ 480 MB; also first fits in 2010.
>
> **(d)** It supports the dating: naive networks on raw input did not fit in memory until the 2000s. The ideas existed long before the resources.
>
> **(e)** It counts only one layer's weights. Training also stores gradients, optimizer state (two more copies for Adam) and activations, roughly 3–4× more. A convolutional layer ([[05 - Convolutional Neural Network]]) replaces these millions of weights with a few hundred shared ones.

## 📝 Summary

- Use ML when you cannot write the rule but can judge the answer.
- Four components: data, model, objective (lower is better), optimizer (usually gradient descent). The loss is a function of the parameters with data fixed.
- Supervised learning estimates $P(\text{label}\mid\text{features})$: regression, classification, tagging, ranking, recommendation, sequence learning. The target's form decides the type.
- Decide by expected loss, not argmax: with penalty $L$, act only when $p < 1/(L+1)$.
- Self-supervised learning creates labels from unlabeled data, then fine-tunes. RL adds actions, credit assignment and exploration; MDP ⊃ contextual bandit ⊃ multi-armed bandit.
- From the biology, two ideas remain: alternating linear/nonlinear layers and backpropagation.
- The 1995–2005 winter was a resource limit: one dense layer on raw audio needs ~176 MB and fits in RAM only by 2010.
- In Table 1.5.1 compute per example is unchanged since 1970 while memory per example fell 100×; the memory squeeze pushed the field from kernel methods to networks that stream data.
- Deep learning = many layers learned jointly (end to end), replacing hand-made features.

## ⚠️ Important Notes

1. "Deep" means layers learned jointly, not just many processing steps.
2. The label must not leak into the features (target leakage, see [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]]).
3. "Lower is better" is only a sign convention.
4. We minimize a surrogate (cross-entropy) because error rate has no useful gradient, so the loss is never exactly what we care about.
5. Most likely class ≠ best action. Decisions need probabilities and costs.
6. Two points fixing two parameters is algebra; learning starts when the system is over-determined.
7. A fitted parameter can be optimal and physically impossible (negative call-out fee). That says something about the features.
8. Residuals of a fit with an intercept always sum to zero. It checks your algebra, not your model.
9. Fixed-length input is a modelling choice with a cost (cropping loses information).
10. Bias enters through data: under-representation and inherited prejudice are different failures, and test accuracy on the same biased data will not reveal either.
11. Offline learning assumes predictions do not change the data. Feedback loops break that. Recommender ratings are also censored: people rate what they feel strongly about, so 3-star ratings are rare.
12. RL special cases are defined by the state: fully observed → MDP; state independent of actions → contextual bandit; no state → multi-armed bandit.
13. Exam answer for the winter: scarce compute and small data; kernel methods were faster and had guarantees.
14. Table 1.5.1 is order-of-magnitude (Iris listed as 100, really 150). Do not quote it more precisely than it claims.
15. Attention was first sold on parameter efficiency, not accuracy.

> [!warning] Gaps in the source material
> - **Figures:** all ten are images (wake word, training loop, death cap, RL loop, Köbel, etc.). All are illustrations whose content the prose states, so nothing is lost. Table 1.5.1 extracted intact.
> - **Formulas:** the text layer turns `∞` into `1` (and also keeps real `1`s), deletes minus and multiplication signs, and prints `.` as `:`. The mushroom formulas were rebuilt from the prose and checked.
> - **Added by me:** the finite-penalty threshold $1/(L+1)$; the column ratios and per-example figures from Table 1.5.1 (one of D2L's two claims fails over the full span; logged as a declined discrepancy since it holds for recent decades); the memory test of the winter in exercise 5; Köbel's breakdown point; the ImageNet ratio and the ~5% human figure; the 1024 × 32 check.
> - **Not covered:** D2L's fuller history, installation, RL beyond the taxonomy, and ch. 2 preliminaries (in [[Linear Algebra/contents/00-Index|Linear Algebra]] and [[Probability Theory/contents/00-Index|Probability Theory]]; calculus and autodiff appear where first used).
> - Literature claims and timings are quoted as D2L gives them.

**Previous:** [[00-Index]] · **Next:** [[02 - Linear Regression]]
