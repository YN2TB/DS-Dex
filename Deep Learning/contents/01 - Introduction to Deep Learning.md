---
subject: Deep Learning
chapter: 1
tags: [ds, deep-learning, machine-learning, foundations, calculus, autograd]
source: "Zhang, Lipton, Li & Smola, Dive into Deep Learning, ch. 1 (§1.1–1.8, book pp. 1–29); §2.4 Calculus and §2.5 Automatic Differentiation (pp. 54–65)"
---

# Introduction to Deep Learning

D2L ch. 1 sets up the vocabulary of machine learning and the history behind deep learning. §2.4–2.5 add the two tools every later chapter uses: derivatives and automatic differentiation. This note follows the book section by section.

## 📘 Main Knowledge

### 1. Why machine learning (§1 intro)

Most programs are rigid rules. For an e-commerce site a developer can list the events (add to cart, empty-cart purchase, …), write a rule for each and test the corner cases before any customer arrives. D2L's rule of thumb: **if you can write a solution that works 100% of the time, you do not need machine learning.**

Some tasks resist rule-writing:

- predicting tomorrow's weather from satellite images and past weather;
- answering a free-text factoid question;
- outlining every person in an image;
- recommending products a user would like but would not find by browsing.

There are two reasons. Sometimes the pattern **changes over time**, so there is no fixed right answer. Sometimes the mapping (pixels → categories) is **too complicated** and runs on principles we cannot state, even though our brains do it without effort.

**Machine learning** is the study of algorithms that improve with experience (observational data or interaction with an environment). The e-commerce program stays the same no matter how much data it sees; a learning program gets better.

### 2. A motivating example: the wake word (§1.1)

"Hey Siri" starts a chain of models: wake-word detection, speech transcription, intent recognition, route planning, travel-time prediction.

Writing a wake-word detector by hand is hopeless. A microphone records about **44,000 samples per second**, each an amplitude, and no rule maps raw audio to {yes, no}. But we can *recognize* the word ourselves, so we can **label** a large dataset of snippets. Then:

1. Define a flexible program whose behaviour depends on **parameters** ("knobs").
2. Use the data to choose the parameters that score best on a performance measure.

| Term | Meaning |
|---|---|
| **model** | the program with its parameters fixed |
| **family of models** | every input–output mapping reachable by turning the knobs |
| **learning algorithm** | the meta-program that uses data to choose the parameters |

The same family should handle "Alexa" and "Apricot" (similar tasks, different knob settings). Different inputs or outputs (images → captions, English → Chinese) may need a different family.

**The training loop** (Fig. 1.1.2):

1. Start with a randomly initialized model that does nothing useful.
2. Grab some data (snippets and labels).
3. Tweak the knobs so the model does better on those examples.
4. Repeat 2–3 until the model is good.

D2L calls this **programming with data**: a cat detector learns to output a large positive number for cats, a large negative number for dogs, and something near 0 when unsure.

### 3. The four key components (§1.2)

| # | Component | What it is | Later chapters |
|---|---|---|---|
| 1 | Data | the examples we learn from | [[02 - Linear Regression]], [[06 - Object Detection]] |
| 2 | Model | how to transform the data | all |
| 3 | Objective function | how well (or badly) the model does | [[02 - Linear Regression]], [[03 - Logistic Regression]] |
| 4 | Optimization algorithm | adjusts parameters to improve the objective | [[04 - Neural Network]] |

#### 3.1 Data

- An **example** (data point, instance, sample) has **features** (covariates, inputs). In supervised learning we predict a special attribute, the **label** (target), which is *not* an input.
- Image: three grids of red, green and blue brightness. A $200\times200$ colour photo is $200\times200\times3=120{,}000$ numbers.
- Health records: age, vital signs, comorbidities, medications, procedures; label = survived 30 days or not.
- When every example has the same number of features, inputs are **fixed-length vectors** and that length is the **dimensionality**.

Not all data is fixed-length. Web images differ in resolution; reviews run from "it stinks!" to pages. Cropping to a standard size loses information. Handling **varying-length data** gracefully is a major advantage of deep learning ([[07 - Recurrent Neural Network]], [[08 - Sequence to Sequence]]).

More data lets us train more powerful models and rely less on assumptions. Many exciting deep models do not work at all without large datasets; on small data some are no better than traditional methods.

The data must also be **right**: garbage in, garbage out. Two failure modes in sensitive uses (predictive policing, résumé screening, lending):

1. **Under-representation**: a skin-cancer model that never saw dark skin.
2. **Inherited prejudice**: a résumé screener trained on past hiring decisions automates past injustice.

Both can happen without anyone intending or noticing it.

#### 3.2 Models

A model ingests data of one type and outputs predictions, possibly of another type (photo → smile score; sensor readings → anomaly score). We focus on **statistical models estimated from data**. Deep learning differs from classical methods mainly in its models: many successive transformations chained top to bottom, hence *deep*.

#### 3.3 Objective functions

To say a model improved we need a formal measure. By convention **lower is better**; any higher-is-better score becomes one by flipping the sign. Hence the name **loss function**.

- Regression: **squared error** $(\hat y-y)^2$.
- Classification: we care about **error rate**, but it is not differentiable, so we optimize a **surrogate objective** (cross-entropy).

During optimization the loss is a function of the **parameters**, with the training data held constant.

**Training vs test set.** Doing well on training data does not guarantee doing well on new data. Split the data into a **training set** (fit parameters) and a **test set** (held out for evaluation), and report both. A student who memorizes practice questions fails the real exam: a model that fits training data but fails on unseen data is **overfitting**.

#### 3.4 Optimization algorithms

Popular deep learning optimizers are based on **gradient descent**: for each parameter, check how the training loss would change under a small perturbation, then move the parameter in the direction that lowers the loss ([[04 - Neural Network]] §optimizers).

### 4. Kinds of machine learning problems (§1.3)

#### 4.1 Supervised learning

Given features and labels, produce a model that predicts labels from features: estimate $P(\text{label}\mid\text{features})$. Examples: cancer vs not from a CT image; a French translation of an English sentence; next month's stock price from this month's reports. Most successful industrial ML is supervised.

The process (Fig. 1.3.1): collect examples, label a random subset (from records, or human annotators), feed the training set to a **supervised learning algorithm**, a function that takes a dataset and outputs another function (the learned model), then predict on unseen inputs.

**What decides the problem type is the form of the target**, not the algorithm.

| Type | Question | Target | Typical loss |
|---|---|---|---|
| Regression | how much? how many? | a number | squared error |
| Classification | which one? | one of $k$ classes | cross-entropy |
| Tagging (multi-label) | which ones? | a subset of classes | per-label cross-entropy |
| Search | in what order? | a ranking | ranking losses |
| Recommendation | which, for this user? | personalized score | rating/ranking losses |
| Sequence learning | variable in, variable out | a sequence | [[08 - Sequence to Sequence]] |

**Regression.** Houses as rows, features as columns: (sq. footage, bedrooms, bathrooms, minutes to centre) might be $[600,1,1,60]$ in New York and $[3000,4,3,10]$ in Pittsburgh. The label is the sale price. Other examples: movie ratings (the \$1M Netflix prize, 2009), hospital length of stay, hours of surgery, rainfall in the next six hours.

D2L's **contractor**: 3 hours cost \$350, 2 hours cost \$250. Assume cost $=w\cdot\text{hours}+b$:
$$3w+b=350,\quad 2w+b=250\;\Longrightarrow\;w=100,\;b=50$$
\$100 per hour plus \$50 to show up. Two points fix two parameters exactly. When other factors cause variation, no exact fit exists and we **minimize the distance** between predictions and observations, usually squared error. Squared error corresponds to assuming **Gaussian noise** ([[02 - Linear Regression]]).

**Classification.** A bank's cheque-scanning app must decide which character each image patch shows: a *which one?* question. **Binary** classification has two classes ({cat, dog}); **multiclass** has more ({0–9, a, b, c, …}). A hard assignment is hard to optimize, so the model outputs a **probability per class**: "0.9 cat" means 90% sure. The loss is **cross-entropy** ([[03 - Logistic Regression]]).

> [!warning] The most likely class is not the decision
> A classifier says $P(\text{death cap})=0.2$, so it is 80% sure the mushroom is safe. Still, do not eat it. Expected loss:
> $$\mathbb E[\text{loss}\mid\text{eat}]=0.2\times\infty+0.8\times0=\infty,\qquad \mathbb E[\text{loss}\mid\text{discard}]=0.2\times0+0.8\times1=0.8$$
> A decision needs both the probabilities and the cost of each outcome. (The mushroom in Fig. 1.3.2 is a death cap.)

With a finite penalty $L$ for eating a poisonous mushroom and cost 1 for discarding a good one, eat only if
$$pL<(1-p)\iff p<\frac1{L+1}.$$
At $L=4$ the threshold is exactly 0.2; at $L=100$ it is 0.99%; at $L=1000$, 0.0999%. Taking the argmax class is optimal only when all errors cost the same (0–1 loss).

**Hierarchical classification**: not all errors are equal. Mistaking a poodle for a schnauzer is mild; a poodle for a dinosaur is bad. The relevant hierarchy depends on use: rattlesnake and garter snake are close on the phylogenetic tree, but confusing them can be fatal.

**Tagging (multi-label classification).** A photo of the *Town Musicians of Bremen* shows a cat, a rooster, a dog and a donkey; forcing one class is wrong. Classes that are not mutually exclusive need **multi-label classification**. Blog posts carry 5–10 correlated tags ("cloud computing" with "AWS"). PubMed articles are tagged from MeSH, about **28,000** tags, with roughly a one-year lag; ML can provide provisional tags (BioASQ competitions).

**Search.** The aim is less "is this page relevant?" than "which relevant pages should be shown first?". Score every item and return the top ones. **PageRank**, Google's original scorer, oddly did not depend on the query: a relevance filter chose candidates, PageRank ordered them by authority. Modern engines learn query-dependent scores.

**Recommender systems.** Like search, but **personalized**. Feedback is **explicit** (ratings, reviews) or **implicit** (skipping a song, which may mean dislike or just bad context). The simplest systems predict a score (expected stars, purchase probability) and recommend the top items. Two conceptual flaws:

1. **Censored feedback**: people rate what they feel strongly about, so 1- and 5-star ratings are common and 3-star rare.
2. **Feedback loops**: purchases follow the current recommender; an item pushed more sells more, looks better and gets pushed more.

**Sequence learning.** So far each example was forgotten after prediction (observations assumed independent). Video frames, sentences and ICU monitoring need context: the model ingests and/or emits sequences. **Sequence-to-sequence** learning has variable-length input and output. Special cases:

| Case | Alignment | Example |
|---|---|---|
| Tagging and parsing | aligned, same length, same order | part-of-speech tagging; named entities: "Tom has dinner in Washington with Sally" → `Ent - - - Ent - Ent` |
| Automatic speech recognition | output much shorter | audio at 8–16 kHz → transcript; thousands of samples per word, no 1:1 match |
| Text to speech | output much longer | text → audio |
| Machine translation | unaligned, order can change | German puts verbs last: "Haben Sie sich schon dieses grossartige Lehrwerk angeschaut?" ≠ word-by-word "Have you yourself already this excellent textbook looked at?" |

Related harder problems: reading order of a web page (2-D layout analysis) and dialogue (world knowledge, long-range conversation state).

#### 4.2 Unsupervised and self-supervised learning

Supervised learning is a job with a dictatorial boss who says exactly what to do. Unsupervised learning is a boss who hands you a data dump and says "do some data science with it". Possible questions:

- **Clustering**: a few prototypes that summarize the data (landscapes, dogs, babies, cats, mountains; users with similar browsing).
- **Subspace estimation**: a few parameters capturing the relevant properties (a ball's trajectory by velocity, diameter and mass; tailors' body measurements). Linear case: **PCA** ([[Linear Algebra/contents/00-Index|Linear Algebra]]).
- **Representation learning**: embed objects in Euclidean space so symbolic relations hold: "Rome" − "Italy" + "France" = "Paris".
- **Causality and probabilistic graphical models**: root causes from data on prices, pollution, crime, education, salaries.
- **Deep generative models**: estimate the data density, explicitly or implicitly, then score examples or sample new ones. Variational autoencoders (2014), GANs (2014), normalizing flows (2014, 2017), diffusion models (2015, 2019–2021).

**Self-supervised learning** uses part of the unlabeled data as supervision: predict randomly masked words from their context (BERT, 2018); predict the relative position of two crops of an image; predict an occluded part; tell whether two images are perturbations of the same one. The learned representation is then **fine-tuned** on a downstream task.

#### 4.3 Interacting with an environment

Supervised and unsupervised learning grab data once and never touch the environment again: **offline learning** (Fig. 1.3.6). Simple, but limited. An **agent** that acts changes its future observations. New questions:

- Does the environment remember what we did?
- Does it want to help (a user speaking into a recognizer)?
- Does it want to beat us (spammers adapting to filters)?
- Does it shift over time, naturally or in response to our tools?

These lead to **distribution shift**: training and test data differ. D2L's example: homework written by TAs, exam written by the lecturer ([[03 - Logistic Regression]] §distribution shift).

#### 4.4 Reinforcement learning

Applications: robotics, dialogue, game AI. **Deep RL** examples: the deep Q-network that beat humans at Atari from pixels (2015) and AlphaGo (2016).

At each time step the agent gets an **observation**, chooses an **action** (sent through an actuator) and receives a **reward**. Its behaviour is a **policy**, a function from observations to actions. RL seeks good policies.

RL is very general. Classification can be recast as RL: one action per class, reward = the supervised loss. But RL also handles what supervised learning cannot:

- **Credit assignment**: in chess the reward comes only at the end (+1 win, −1 loss); which moves deserve it? Same for an employee promoted on October 11 after a year of choices.
- **Partial observability**: a cleaning robot trapped in one of many identical closets must use earlier observations to know where it is.
- **Exploration vs exploitation**: use the best known policy, or try others and give up short-term reward for knowledge.

| Special case | Condition |
|---|---|
| Markov decision process | environment fully observed |
| Contextual bandit | state does not depend on previous actions |
| Multi-armed bandit | no state; actions with initially unknown rewards |

RL itself is developed in [[Machine Learning/contents/00-Index|Machine Learning]].

### 5. Roots (§1.4)

The statistical tools are old:

- **Bernoulli distribution** (Jacob Bernoulli, 1655–1705); **Gaussian distribution** and the **least mean squares** algorithm (Gauss, 1777–1855), still used in insurance and medical diagnostics. Ohm's law is a perfect linear model.
- **Jacob Köbel** (1460–1533) estimated "one foot" by averaging the feet of 16 men leaving church, later dropping the shortest and longest foot: an early **trimmed mean**. (Mine: dropping one per tail keeps 14 of 16 values and tolerates one corrupted measurement.)
- **Ronald Fisher** (1890–1962): linear discriminant analysis, the Fisher information matrix, the **Iris** dataset (1936). He was also a eugenicist, a reminder that data science has a long record of misuse.
- **Claude Shannon** (1916–2001): information theory. **Alan Turing** (1912–1954): "Can machines think?" (1950) and the Turing test, where a machine is intelligent if a human judge cannot tell its text replies from a human's.
- **Donald Hebb** (1904–1985), *The Organization of Behavior* (1949): neurons learn by positive reinforcement (the **Hebbian rule**). This inspired Rosenblatt's perceptron and laid foundations for stochastic gradient descent: reinforce good behaviour, diminish bad.

**Neural networks** are named after biology (Bain 1873, Sherrington 1890). The biology is now loose, but two principles remain in most networks:

1. **Alternating linear and nonlinear processing units**, called layers ([[04 - Neural Network]]).
2. **The chain rule (backpropagation)** to adjust all parameters at once (§10 below; [[04 - Neural Network]]).

**The winter, about 1995–2005.** Training was computationally very expensive (RAM was plentiful but compute scarce), and datasets were small: Iris was still a benchmark, MNIST's 60,000 digits were "huge". Kernel methods, decision trees and graphical models did better empirically, trained in less than weeks and had strong theoretical guarantees.

### 6. The road to deep learning (§1.5)

The change came from data (the web, companies with hundreds of millions of users, cheap sensors, cheap storage by Kryder's law) and compute (Moore's law, and above all **GPUs** built for games). D2L's Table 1.5.1:

| Decade | Dataset | Memory | FLOP/s |
|---|---|---|---|
| 1970 | 100 (Iris) | 1 KB | 100 KF (Intel 8080) |
| 1980 | 1 K (Boston house prices) | 100 KB | 1 MF (Intel 80186) |
| 1990 | 10 K (optical character recognition) | 10 MB | 10 MF (Intel 80486) |
| 2000 | 10 M (web pages) | 100 MB | 1 GF (Intel Core) |
| 2010 | 10 G (advertising) | 1 GB | 1 TF (NVIDIA C2050) |
| 2020 | 1 T (social network) | 100 GB | 1 PF (NVIDIA DGX-2) |

D2L draws two claims: memory has not kept pace with data, and compute has outpaced data. So models must be memory-efficient and can spend more compute on optimizing parameters. The sweet spot moved from (generalized) linear models and kernel methods to deep networks. MLPs (McCulloch & Pitts, 1943), CNNs (LeCun et al., 1998), LSTM (Hochreiter & Schmidhuber, 1997) and Q-learning (Watkins & Dayan, 1992) were "rediscovered" after years dormant.

Checking the table (my analysis):

| | 1970 | 2020 | growth |
|---|---|---|---|
| data (examples) | $10^2$ | $10^{12}$ | $10^{10}$ |
| memory (bytes) | $10^3$ | $10^{11}$ | $10^{8}$ |
| compute (FLOP/s) | $10^5$ | $10^{15}$ | $10^{10}$ |
| memory per example | 10 B | 0.1 B | ÷100 |
| compute per example | 1000 | 1000 | ×1 |

The memory claim holds (100× less memory per example). The compute claim holds only from 2000 (compute per example was 100 in 2000, 1000 in 2020). The memory result is what matters: with 0.1 byte of RAM per example a kernel method cannot even store its $O(n^2)$ pairwise matrix, while a fixed-size network streams examples past its parameters.

**Ideas, not just resources** (D2L's list):

- **Dropout** (2014): capacity control by injecting noise during training ([[04 - Neural Network]]).
- **Attention** (Bahdanau et al., 2014): increase a model's memory and complexity *without adding parameters*, via a learnable pointer structure. A translator stores a pointer to intermediate states instead of squeezing the whole sentence into one fixed-size vector, which helps long sequences ([[08 - Sequence to Sequence]]).
- **Transformer** (2017): built only from attention, with superior **scaling**: better with more data, parameters and compute (Kaplan et al., 2020). Used in NLP, vision, speech, RL and graph networks; one pretrained Transformer can play Atari, caption images, chat and control a robot (Reed et al., 2022).
- **Language models** scaled up and **aligned with human intent** (Ouyang et al., 2022) give ChatGPT.
- **Multi-stage designs** (memory networks, neural programmer-interpreter): an internal state modified repeatedly, like a chain of reasoning steps.
- **GANs** (2014): replace the sampler with any differentiable algorithm, trained until a discriminator (effectively a two-sample test) cannot tell fake from real. Galloping zebras, fake celebrity faces, photorealistic images from sketches.
- **Diffusion models**: learn to reverse a process that gradually adds noise; they started replacing GANs (DALL-E 2, Imagen).
- **Parallel and distributed training**: SGD wants small minibatches, GPUs want big ones. 1,024 GPUs × 32 images ≈ 32,000 per batch; work by Li (2017), You et al. (2017) and Jia et al. (2018) reached 64,000 and cut ResNet-50 on ImageNet from days to under 7 minutes.
- **Parallel simulation for RL**: superhuman Go, Atari, StarCraft, MuJoCo physics. RL works best with plenty of (state, action, reward) tuples, which simulators provide.
- **Frameworks**: Caffe, Torch, Theano → TensorFlow (Keras), CNTK, Caffe2, MXNet → imperative tools started by Chainer: PyTorch, Gluon, JAX. Logistic regression was a CMU PhD homework in 2014; now it takes under 10 lines.

### 7. Success stories (§1.6)

Long-standing and hidden: mail sorting by OCR since the 1990s (the origin of MNIST), cheque reading, credit scoring, fraud checks behind PayPal, Stripe, AliPay, Visa and MasterCard, chess programs, search and recommendation.

Recent and visible:

- **Assistants** (Siri, Alexa, Google Assistant), with speech recognition at human parity on some tasks (Xiong et al., 2018).
- **Object recognition**: ImageNet top-5 error 28% in 2010 → 2.25% in 2017, i.e. 2,800 → 225 mistakes per 10,000 images (12.4× fewer).
- **Games**: TD-Gammon (temporal-difference RL), Deep Blue (parallel search with special hardware), AlphaGo (deep learning + Monte Carlo tree sampling, human parity in 2015), Libratus in poker (large, partially observed state).
- **Self-driving**: partial autonomy (Tesla, NVIDIA, Waymo). Deep learning handles mainly perception; the rest is engineered.

**On AI risk**, D2L argues sentient AI is far off: systems are built for specific goals, and no tools exist for AGI that improves and redesigns itself. The pressing concerns are automation of routine jobs and racial, gender or age **bias** when models drive consequential decisions (credit, bail).

### 8. The essence of deep learning (§1.7)

Deep learning is ML with **many-layered neural networks**: models that learn many layers of transformations. All ML has several computing stages (feature processing first); what is new is that **the layers are learned jointly from data**.

- **End-to-end training.** Instead of tuning components separately, build the whole system and tune it jointly. Computer vision used to separate **feature engineering** (Canny edge detector 1987, SIFT 2004) from the model; learned filters replaced them with better accuracy ([[05 - Convolutional Neural Network]] shows a CNN learning an edge detector). Deep learning replaces both the shallow model and the feature engineering, which erased the boundaries between vision, speech, NLP and medical informatics.
- **From parametric to nonparametric models.** Scarce data needs simplifying assumptions; abundant data allows flexible models that fit better, at the cost of interpretation (like physics moving from hand-solved approximations to numerical simulation).
- **Empiricism.** Accepting suboptimal solutions and nonconvex optimization, and trying methods before proving them.
- **Open source**: tools, models and trained networks shared across academia and industry.

**Summary in D2L's words (§1.8).** Machine learning uses experience to improve at a task. **Representation learning** finds how to represent data automatically; deep learning is multi-level representation learning. Progress came from abundant data, GPU compute and efficient frameworks.

### 9. Calculus (§2.4)

**Archimedes and limits.** Inscribe an $n$-gon in a circle of radius $r$: $n$ triangles, height → $r$, base → $2\pi r/n$, so the area → $n\cdot r\cdot\tfrac12(2\pi r/n)=\pi r^2$. (Check with $r=1$: $n=6$ gives 2.598, $n=12$ gives 3.000, $n=96$ gives 3.1394, $n=1000$ gives 3.14157.) Limits are the root of differential and integral calculus. Differential calculus tells us how to change a function by changing its arguments, which is what optimization does with the loss. The real goal, doing well on unseen data, is **generalization**.

#### 9.1 Derivatives

For $f:\mathbb R\to\mathbb R$:
$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.$$
If the limit exists, $f$ is **differentiable** at $x$. Accuracy and AUC are not differentiable, so we optimize a differentiable **surrogate**.

D2L's example: $f(x)=3x^2-4x$ at $x=1$.

| $h$ | $(f(1+h)-f(1))/h$ |
|---|---|
| 0.1 | 2.30000 |
| 0.01 | 2.03000 |
| 0.001 | 2.00300 |
| 0.0001 | 2.00030 |
| 0.00001 | 2.00003 |

So $f'(1)=2$. (Mine: the quotient is exactly $2+3h$, so the error shrinks linearly in $h$. The central difference $(f(1+h)-f(1-h))/2h$ is exactly 2 for any $h$ because $f$ is quadratic.)

Notation: $f'(x)=y'=\frac{dy}{dx}=\frac{df}{dx}=\frac{d}{dx}f(x)=Df(x)=D_xf(x)$.

Common derivatives and rules:

| | |
|---|---|
| $\frac{d}{dx}C=0$ | constant |
| $\frac{d}{dx}x^n=nx^{n-1}$ ($n\ne0$) | power |
| $\frac{d}{dx}e^x=e^x$ | exponential |
| $\frac{d}{dx}\ln x=x^{-1}$ | logarithm |
| $\frac{d}{dx}[Cf]=C\frac{df}{dx}$ | constant multiple rule |
| $\frac{d}{dx}[f+g]=f'+g'$ | sum rule |
| $\frac{d}{dx}[fg]=fg'+gf'$ | product rule |
| $\frac{d}{dx}\frac fg=\frac{gf'-fg'}{g^2}$ | quotient rule |

So $\frac{d}{dx}[3x^2-4x]=6x-4$, which is 2 at $x=1$. The derivative is the **slope**: the tangent line at $x=1$ is $y=2x-3$ (since $f(1)=-1$).

D2L also builds plotting helpers (`use_svg_display`, `set_figsize`, `set_axes`, `plot`) and saves them to the `d2l` package with the `#@save` comment; they are only used for figures.

#### 9.2 Partial derivatives and gradients

For $y=f(x_1,\dots,x_n)$:
$$\frac{\partial y}{\partial x_i}=\lim_{h\to0}\frac{f(x_1,\dots,x_i+h,\dots,x_n)-f(x_1,\dots,x_i,\dots,x_n)}{h},$$
computed by treating the other variables as constants. Notation: $\frac{\partial y}{\partial x_i}=\frac{\partial f}{\partial x_i}=\partial_{x_i}f=\partial_if=f_{x_i}=f_i=D_if=D_{x_i}f$.

The **gradient** of $f:\mathbb R^n\to\mathbb R$ stacks the partials:
$$\nabla_{\mathbf x}f(\mathbf x)=\left[\partial_{x_1}f(\mathbf x),\dots,\partial_{x_n}f(\mathbf x)\right]^\top.$$

Rules used throughout the book:

| Function | Gradient |
|---|---|
| $\mathbf A\mathbf x$, $\mathbf A\in\mathbb R^{m\times n}$ | $\nabla_{\mathbf x}\mathbf A\mathbf x=\mathbf A^\top$ |
| $\mathbf x^\top\mathbf A$ | $\nabla_{\mathbf x}\mathbf x^\top\mathbf A=\mathbf A$ |
| $\mathbf x^\top\mathbf A\mathbf x$, $\mathbf A$ square | $(\mathbf A+\mathbf A^\top)\mathbf x$ |
| $\|\mathbf x\|^2=\mathbf x^\top\mathbf x$ | $2\mathbf x$ |
| $\|\mathbf X\|_F^2$ | $2\mathbf X$ |

(Checked with autograd: $\mathbf A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$, $\mathbf x=(1,-1)$ gives $(\mathbf A+\mathbf A^\top)\mathbf x=(-3,-3)$.)

#### 9.3 Chain rule

Deep networks are nested functions. If $y=f(u)$ and $u=g(x)$:
$$\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}.$$
If $y=f(\mathbf u)$ with $u_j=g_j(\mathbf x)$, $j=1..m$:
$$\frac{\partial y}{\partial x_i}=\sum_{j=1}^m\frac{\partial y}{\partial u_j}\frac{\partial u_j}{\partial x_i},\qquad\text{so}\qquad\nabla_{\mathbf x}y=\mathbf A\,\nabla_{\mathbf u}y,$$
where $\mathbf A\in\mathbb R^{n\times m}$ holds the derivatives of $\mathbf u$ with respect to $\mathbf x$. Each gradient step is a **vector–matrix product**, which is why linear algebra is central to deep learning.

**Discussion.** The composition rules are mechanical, so gradients can be computed **automatically**. A function is evaluated by walking its dependency graph **forward**; gradients are computed by walking it **backward**. That backward walk is **backpropagation**.

### 10. Automatic differentiation (§2.5)

Frameworks offer **autograd**. As data passes through each function, the framework builds a **computational graph** recording how each value depends on others; to get derivatives it works backward through the graph with the chain rule (**backpropagation**). History: Wengert (1964); the core of modern backprop in Speelpenning's 1980 thesis; Griewank (1989). Backprop is not the only option: Julia uses forward-mode propagation.

#### 10.1 A simple function

```python
import torch
x = torch.arange(4.0)          # tensor([0., 1., 2., 3.])
x.requires_grad_(True)         # or torch.arange(4.0, requires_grad=True)
x.grad                         # None by default
y = 2 * torch.dot(x, x)        # tensor(28., grad_fn=<MulBackward0>)
y.backward()
x.grad                         # tensor([ 0.,  4.,  8., 12.])
x.grad == 4 * x                # all True, since ∇(2xᵀx) = 4x
```

The gradient has the same shape as `x`. Its buffer is allocated once and reused, since training takes gradients with respect to the same parameters many times.

**Gradients accumulate.** PyTorch adds a new gradient to the stored one, which is useful for summing several objectives. Reset with `x.grad.zero_()`:

```python
x.grad.zero_()
y = x.sum(); y.backward()
x.grad                         # tensor([1., 1., 1., 1.])
```

Without the reset, the result would be $4\mathbf x+\mathbf 1=[1,5,9,13]$ (checked).

#### 10.2 Backward for non-scalar variables

For vector $\mathbf y$ the full derivative is the **Jacobian**. Usually we want the gradient of the *sum* of per-example losses instead. Calling `backward` on a non-scalar raises an error unless you pass a vector $\mathbf v$ (argument named `gradient`); PyTorch then computes $\mathbf v^\top\partial_{\mathbf x}\mathbf y$:

```python
x.grad.zero_()
y = x * x
y.backward(gradient=torch.ones(len(y)))   # faster: y.sum().backward()
x.grad                                     # tensor([0., 2., 4., 6.])
```

(With $\mathbf v=(1,0,0,1)$ the result is $(0,0,0,6)$: only components 1 and 4 count.)

#### 10.3 Detaching computation

Sometimes an intermediate value should be treated as a constant. With `y = x * x` and `u = y.detach()`, `u` has the same value but no history, so gradients do not flow through it:

```python
x.grad.zero_()
y = x * x
u = y.detach()
z = u * x
z.sum().backward()
x.grad == u                    # all True: gradient is u = [0, 1, 4, 9]
```

Without the detach, $z=x^3$ and the gradient would be $3x^2=[0,3,12,27]$. The graph leading to `y` still exists, so `y.sum().backward()` afterwards gives `2 * x`.

#### 10.4 Gradients and Python control flow

Autograd works even when the graph is built through loops, conditionals and function calls:

```python
def f(a):
    b = a * 2
    while b.norm() < 1000:
        b = b * 2
    if b.sum() > 0:
        c = b
    else:
        c = 100 * b
    return c

a = torch.randn(size=(), requires_grad=True)
d = f(a)
d.backward()
a.grad == d / a                # tensor(True)
```

Each run builds a specific graph for that input. $f$ is linear in $a$ with a piecewise scale, so the gradient equals $d/a$. (Checked: $a=0.3$ gives $d=1228.8$ and gradient 4096; $a=-0.3$ gives gradient 409,600, the extra ×100 from the `else` branch; $a=1500$ skips the loop and gives 2.) Dynamic control flow is common, e.g. text graphs depend on input length.

**Four steps to remember:** (i) attach gradients to the variables you differentiate with respect to; (ii) record the computation of the target; (iii) run backpropagation; (iv) read the gradient.

## ✏️ Exercises

> [!example]- **1.** *(Easy) The contractor*
> **(a)** \$350 for 3 hours, \$250 for 2 hours, cost $=w\cdot\text{hours}+b$. Find $w,b$ and predict 5 hours.
> **(b)** A third invoice: \$500 for 4 hours. Show no line fits all three, then find the least-squares line and its 5-hour prediction.
> **(c)** What does (b) tell you?
>
> ---
> **(a)** Subtract: $w=100$, then $b=50$. Five hours: \$550.
>
> **(b)** The line from (a) predicts \$450 for 4 hours, not \$500. Minimizing $\sum_i(wh_i+b-c_i)^2$ over $(3,350),(2,250),(4,500)$ gives $w=125$, $b=-\tfrac{25}{3}\approx-8.33$. Residuals $+\tfrac{50}{3},-\tfrac{25}{3},-\tfrac{25}{3}$ sum to zero; SSE $=\tfrac{1250}{3}\approx416.67$. Five hours: $\tfrac{1850}{3}\approx\$616.67$.
>
> **(c)** A negative call-out fee is physically meaningless: something outside the feature affects cost. With more examples than parameters there is no exact solution, and the objective function decides which imperfect fit to prefer.

> [!example]- **2.** *(Easy) Classify the problem*
> Name the problem type and say what an example, its features and its label are.
> (a) Predicting surgery duration. (b) Auto-tagging blog posts. (c) Transcribing a 3-second audio clip. (d) A robot vacuum learning a new flat. (e) Predicting hidden words in Wikipedia.
>
> ---
> **(a)** Regression. Example: one surgery; features: patient and procedure data; label: minutes.
>
> **(b)** Tagging (multi-label). The label is a subset of tags (a binary vector). Tags are correlated, which plain multiclass classification cannot express.
>
> **(c)** Sequence-to-sequence (speech recognition). 3 s at 44 kHz is 132,000 samples mapping to a few words, with no one-to-one alignment.
>
> **(d)** Reinforcement learning, probably partially observed. Actions change what the agent sees next and it gets rewards, not correct answers.
>
> **(e)** Self-supervised learning. Example: a sentence with a masked token; label: the hidden word (BERT's objective).

> [!example]- **3.** *(Medium) Decisions are not argmax*
> A classifier gives $P(\text{malignant})=p$. Missing a cancer costs $L$; an unnecessary follow-up costs 1.
> **(a)** Above what $p$ should you refer? **(b)** Evaluate for $L=4,100,1000$. **(c)** At $L=100$ a colleague says the model is 97% sure it is benign, so discharge. Respond. **(d)** Which of the four components does $L$ belong to?
>
> ---
> **(a)** Refer costs $(1-p)$, discharge costs $pL$. Refer if $p>1/(L+1)$.
>
> **(b)** 20%, 0.990%, 0.0999%.
>
> **(c)** $p=3\%>0.990\%$: refer. The colleague used a 50% threshold, which assumes $L=1$.
>
> **(d)** The objective function. Argmax is optimal only under 0–1 loss; the mushroom is the case $L=\infty$, where any positive $p$ means discard.

> [!example]- **4.** *(Medium) Derivatives and gradients*
> **(a)** For $f(x)=3x^2-4x$, show the forward-difference quotient at $x=1$ equals $2+3h$. Check D2L's printed value at $h=0.01$.
> **(b)** Differentiate $f(x)=x^x$ for $x>0$.
> **(c)** Find the tangent line of $f(x)=x^3-\tfrac1x$ at $x=1$.
> **(d)** Gradient of $f(\mathbf x)=3x_1^2+5e^{x_2}$.
> **(e)** Gradient of $f(\mathbf x)=\|\mathbf x\|_2$. What happens at $\mathbf x=\mathbf 0$? Compare with $\|\mathbf x\|_2^2$.
>
> ---
> **(a)** $f(1+h)-f(1)=3(1+2h+h^2)-4(1+h)-(-1)=2h+3h^2$; divide by $h$: $2+3h$. At $h=0.01$: 2.03, matching the printout.
>
> **(b)** $x^x=e^{x\ln x}$, so $f'(x)=x^x(\ln x+1)$.
>
> **(c)** $f(1)=0$, $f'(x)=3x^2+1/x^2$, $f'(1)=4$. Tangent: $y=4x-4$.
>
> **(d)** $\nabla f=[6x_1,\;5e^{x_2}]^\top$.
>
> **(e)** $\nabla\|\mathbf x\|_2=\mathbf x/\|\mathbf x\|_2$, a unit vector. At $\mathbf 0$ it is undefined: the norm is a cone with a kink (in 1-D, $|x|$ has slope $-1$ on the left and $+1$ on the right). $\|\mathbf x\|^2$ has gradient $2\mathbf x$, which is $\mathbf 0$ there. This is one reason weight decay uses the squared norm ([[02 - Linear Regression]]).

> [!example]- **5.** *(Hard) Autograd by hand*
> $f(x)=\log(x^2)\sin x+\tfrac1x$ (D2L §2.5 exercises 5–8).
> **(a)** Draw the dependency graph with intermediate variables. **(b)** Run it forward at $x=2$. **(c)** Run it backward and get $f'(2)$; check against the closed form. **(d)** For a loss $\ell:\mathbb R^n\to\mathbb R$, why is backward (reverse) mode preferred to forward mode? **(e)** In the detach example with $\mathbf x=[0,1,2,3]$, what does `x.grad` hold with and without `detach`?
>
> ---
> **(a)** $a=x^2$, $b=\log a$, $c=\sin x$, $d=bc$, $e=1/x$, $f=d+e$. $x$ feeds $a$, $c$ and $e$.
>
> **(b)** $a=4$, $b=1.38629$, $c=0.90930$, $d=1.26055$, $e=0.5$, $f=1.76055$.
>
> **(c)** From the output: $\partial f/\partial d=\partial f/\partial e=1$; $\partial d/\partial b=c$, $\partial d/\partial c=b$; $\partial b/\partial a=1/a=0.25$; $\partial a/\partial x=2x=4$; $\partial c/\partial x=\cos2=-0.41615$; $\partial e/\partial x=-1/x^2=-0.25$. Sum the three paths into $x$:
> $$0.90930\cdot0.25\cdot4+1.38629\cdot(-0.41615)-0.25=0.90930-0.57690-0.25=0.08240.$$
> Closed form $f'(x)=\tfrac{2\sin x}{x}+2\ln x\cos x-\tfrac1{x^2}$ gives 0.082395 at $x=2$; PyTorch agrees.
>
> **(d)** Reverse mode gets all $n$ partials of one scalar output in one backward pass. Forward mode carries the derivative with respect to one input per pass, so it needs $n$ passes (millions for a network). Forward mode wins when there are few inputs and many outputs, and it needs no stored intermediates; reverse mode must keep the forward activations in memory.
>
> **(e)** With detach: $\mathbf u=[0,1,4,9]$ (u is a constant, $\partial(ux)/\partial x=u$). Without: $3x^2=[0,3,12,27]$.

## 📝 Summary

- Use ML when you cannot write the rule but can judge the answer; the model is a program with parameters chosen from data ("programming with data").
- Four components: data, model, objective (lower is better; surrogate when the real metric has no gradient), optimizer (gradient descent). The loss is a function of the parameters with data fixed.
- The form of the target sets the problem type: regression, classification, tagging, search, recommendation, sequence learning (aligned tagging, ASR, TTS, translation).
- Decide by expected loss, not argmax: with penalty $L$ act only when $p<1/(L+1)$.
- Unsupervised: clustering, subspaces, embeddings, causality, generative models; self-supervised learning makes labels from the data. RL adds actions, credit assignment, partial observability and exploration; MDP / contextual bandit / multi-armed bandit are its special cases.
- Two biological ideas survive: alternating linear/nonlinear layers and backpropagation. The 1995–2005 winter was a lack of compute and data; memory per example has since fallen 100×, which favours fixed-size networks over kernel methods.
- Deep learning = many layers learned jointly, end to end, replacing hand-made features.
- Calculus: derivative as limit, sum/product/quotient/chain rules, gradient as stacked partials, $\nabla\mathbf x^\top\mathbf A\mathbf x=(\mathbf A+\mathbf A^\top)\mathbf x$. Autograd records the graph forward and applies the chain rule backward; gradients accumulate, `detach` cuts the graph, control flow is fine.

## ⚠️ Important Notes

1. "Deep" means layers learned jointly, not just many processing steps.
2. The label must not leak into the features (target leakage, see [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]]).
3. "Lower is better" is only a sign convention.
4. We minimize a surrogate (cross-entropy) because error rate, accuracy and AUC have no useful gradient, so the loss is never exactly what we care about.
5. Most likely class ≠ best action. Decisions need probabilities and costs.
6. Two points fixing two parameters is algebra; learning starts when the system is over-determined.
7. Multiclass (exactly one class) and multi-label (any subset) are different problems; a Bremen-musicians photo breaks a multiclass model.
8. Recommender data is censored and shaped by the current recommender (feedback loops); offline accuracy can mislead.
9. Speech recognition and translation are both seq2seq, but ASR is ordered while translation reorders words.
10. RL special cases are defined by the state: fully observed → MDP; state independent of actions → contextual bandit; no state → multi-armed bandit.
11. Exam answer for the winter: scarce compute and small data; kernel methods were faster and had guarantees.
12. Table 1.5.1 is order-of-magnitude (Iris listed as 100, really 150). Do not quote it more precisely than it claims.
13. Attention was first sold on parameter efficiency (more memory without more parameters), not accuracy.
14. PyTorch **accumulates** gradients: forget `x.grad.zero_()` (or `optimizer.zero_grad()`) and every step adds to the last.
15. `backward()` on a non-scalar needs a `gradient` vector, or call `.sum()` first. Calling `backward()` twice on the same graph raises an error because the graph is freed after the first pass.
16. The forward-difference quotient has error $O(h)$; don't read 2.003 as "the derivative is 2.003".
17. $\|\mathbf x\|_2$ is not differentiable at $\mathbf 0$; $\|\mathbf x\|_2^2$ is.

> [!warning] Gaps in the source material
> - **Figures:** all of ch. 1's figures (wake word, training loop, supervised learning, death cap, Bremen musicians, Amazon recommendations, audio, RL loop, Köbel) and the §2.4 circle and tangent plots are images. Their content is stated in the prose. Table 1.5.1 extracted intact.
> - **Formulas:** the text layer turns `∞` into `1`, drops minus and multiplication signs and writes `:` for decimal points. The mushroom formula and all §2.4 formulas were rebuilt from the prose; the derivative table, gradient rules and every autograd output were rerun (sympy, PyTorch 2.11) and match the book.
> - **Added by me:** the threshold $1/(L+1)$; the per-example ratios from Table 1.5.1 (D2L's compute claim holds only from 2000; logged as declined discrepancy D1 in [[00-Index]]); the Archimedes numerical check; the $2+3h$ error and central-difference remark; the accumulated-gradient value [1,5,9,13]; the weighted-`v` and control-flow values; exercise answers.
> - **Not covered:** installation, notation, §2.1–2.3 and §2.6 (tensors, preprocessing, linear algebra, probability: see [[Linear Algebra/contents/00-Index|Linear Algebra]] and [[Probability Theory/contents/00-Index|Probability Theory]]), §2.7 documentation.

**Previous:** [[00-Index]] · **Next:** [[02 - Linear Regression]]
