---
subject: Deep Learning
chapter: 1
tags: [ds, deep-learning, machine-learning, foundations]
source: "Zhang, Lipton, Li & Smola — Dive into Deep Learning, ch. 1 (book pp. 1–29); §2.4–2.5 for calculus and autodiff"
---

# Introduction to Deep Learning

## 📘 Main Knowledge

### 1. The problem that machine learning exists to solve

Almost every program you use was written as a **rigid set of rules**: an e-commerce site adds a row to a cart table when you click "add to cart", refuses checkout on an empty cart, and so on. A developer can enumerate the cases, test the corner cases, and ship with confidence *before ever seeing a real customer*.

D2L's key framing is a limit statement:

> **When you can devise a solution that works 100% of the time, you should not be worrying about machine learning.**

Machine learning earns its place only where rule-writing fails, and it fails for two distinct reasons:

1. **The rule changes over time.** There is no fixed right answer, so any solution must adapt. (Predicting tomorrow's weather.)
2. **The rule is beyond conscious access.** You perform the task effortlessly and cannot say how. The mapping from pixels to "that is a cat" involves millions of computations following unknown principles.

Reason 2 is the deep one and it contains the trick that makes the whole field work:

> **We do not know how to *write* the program, but we do know how to *judge* its output.** You cannot code a wake-word detector for "Alexa", but you can recognise "Alexa" when you hear it — so you can *label* data.

That asymmetry — **generating a rule is hard, evaluating an instance is easy** — is what we trade on. Instead of writing the program, we write a *flexible* program with adjustable **parameters**, and let data choose them.

### 2. The four components of every learning problem

Whatever the task, the same four objects appear. Memorise these; the rest of the course is variations on them.

| # | Component | What it is | Later chapters |
|---|---|---|---|
| 1 | **Data** | the examples we learn from | [[02 - Linear Regression]], [[06 - Object Detection]] |
| 2 | **Model** | the computational machinery mapping input type → output type | all of them |
| 3 | **Objective function** | a number saying how badly the model is doing | [[02 - Linear Regression]], [[03 - Logistic Regression]] |
| 4 | **Optimization algorithm** | the procedure that adjusts parameters to reduce the objective | [[04 - Neural Network]] |

**Vocabulary, exactly as D2L uses it:**

- An **example** (= data point, data instance, sample) is one observation.
- Its **features** (= covariates, inputs) are the attributes we get to see.
- Its **label** (= target) is the attribute we want to predict, *and it is not part of the model's input*.
- Fix the parameters and the program becomes a **model**; the set of all programs reachable by varying the parameters is a **family of models**; the meta-program that picks parameters from data is the **learning algorithm**.

**Dimensionality.** When every example has the same number of numerical features we have **fixed-length vectors**, and that constant length is the **dimensionality**. A $200\times200$ colour photograph is three grids of brightness values:
$$200 \times 200 \times 3 = 120{,}000 \text{ numbers}$$
One second of microphone audio at ~44 kHz is $44{,}000$ numbers. Both are "one example".

Not everything is fixed-length. Internet images differ in resolution; reviews run from *"it stinks!"* to several pages. Cropping images to a standard size loses the cropped-out information. **Graceful handling of varying-length data is one of deep learning's genuine advantages over classical methods** — and it is the whole subject of [[07 - Recurrent Neural Network]] and [[08 - Sequence to Sequence]].

**Data quality is not a footnote.** *Garbage in, garbage out* — but the consequences run past bad accuracy. A skin-cancer detector that never saw black skin fails on black patients. A resume screener trained on past hiring decisions **automates historical injustice**. D2L is explicit that this happens *without the data scientist conspiring or even being aware*; the failure is structural, not moral.

### 3. Objective functions, and why "lower is better"

We need a formal measure of how good a model is. These are **objective functions**, and by convention we define them so that **lower is better** — which is why they are also called **loss functions**. This is *purely* convention: any "higher is better" score becomes a loss by flipping the sign.

- **Regression** (numerical targets) → **squared error**, $(\hat y - y)^2$. Justified properly in [[02 - Linear Regression]], where it is shown to follow from assuming **Gaussian noise**.
- **Classification** (categorical targets) → we *want* to minimise **error rate**, but error rate is a step function: it is non-differentiable and flat almost everywhere, so gradient methods have nothing to work with. We therefore optimise a **surrogate objective** — **cross-entropy** — and hope it drags error rate down with it. See [[03 - Logistic Regression]].

> [!important] The single most important distinction in this section
> During optimization we treat the loss as **a function of the parameters**, holding the training data **constant**. This is the mental flip that makes everything else work: the data is not the variable, the *weights* are.

**Training vs. test.** We split data into a **training set** (to fit parameters) and a **test set** (held out, for evaluation). D2L's analogy is exact: training performance is your score on practice exams. A student who *memorises the practice questions* looks masterful and collapses on unseen questions. That is **overfitting**, and it is measured, decomposed and controlled in [[02 - Linear Regression]] and [[04 - Neural Network]].

**Optimization.** Nearly all deep learning optimizers descend from **gradient descent**: at each step, ask for each parameter how the training loss would change if you nudged it slightly, then move it in the direction that lowers the loss. Made precise in [[02 - Linear Regression]] (minibatch SGD) and extended to momentum/Adam in [[04 - Neural Network]].

### 4. A taxonomy of learning problems

#### 4.1 Supervised learning

Given features **and** labels, produce a model that predicts labels from features. Probabilistically: **estimate $P(\text{label} \mid \text{features})$.** This one paradigm accounts for the majority of successful industrial ML.

| Problem type | Question it answers | Target | Typical loss |
|---|---|---|---|
| **Regression** | *how much? how many?* | arbitrary numerical value | squared error |
| **Classification** | *which one?* | one of $k$ discrete classes | cross-entropy |
| **Tagging** (multi-label) | *which ones?* | any subset of classes | per-label cross-entropy |
| **Search / ranking** | *in what order?* | a permutation | ranking losses |
| **Recommendation** | *which, for you?* | personalised score | rating/ranking losses |
| **Sequence learning** | *variable in, variable out* | a sequence | see [[08 - Sequence to Sequence]] |

**Regression is defined by the form of the target, not by the algorithm.** A worked instance from D2L, which is genuinely linear regression in miniature:

> A contractor bills **\$350 for 3 hours** and **\$250 for 2 hours**. Assume `cost = w · hours + b`.
> $$3w + b = 350, \qquad 2w + b = 250 \;\Longrightarrow\; w = 100,\; b = 50$$
> **\$100 per hour plus a \$50 call-out charge.** Two equations, two unknowns, solved exactly.

Two data points determined two parameters *exactly*. Usually you cannot: variation comes from factors outside your features, the system is over-determined, and you fall back on **minimising squared distance** rather than solving. That single step — from *solving* to *minimising* — is the entire move into [[02 - Linear Regression]].

**Classification.** Rather than forcing a firm categorical output (hard to optimize), the model outputs **a probability per class**. A classifier that says 0.9 for "cat" is 90% sure. Multi-class extends to $\{0,1,\dots,9,a,b,c,\dots\}$; **hierarchical classification** recognises that not all errors are equal — confusing a poodle with a schnauzer is cheap, confusing it with a dinosaur is not, and mistaking a rattlesnake for a garter snake can be fatal.

> [!warning] The most-likely class is **not** the decision
> This is the single most exam-worthy idea in the chapter. D2L's mushroom example:
>
> A classifier says $P(\text{death cap}) = 0.2$, so it is **80% sure the mushroom is safe**. Do you eat it?
>
> $$\mathbb{E}[\text{loss} \mid \text{eat}] = 0.2 \times \infty + 0.8 \times 0 = \infty$$
> $$\mathbb{E}[\text{loss} \mid \text{discard}] = 0.2 \times 0 + 0.8 \times 1 = 0.8$$
>
> Discard. **The argmax of the posterior said "safe"; the argmin of expected loss said "throw it away".** (The mushroom in D2L's photograph is in fact a death cap.)
>
> **Classification gives you probabilities; decisions require probabilities *and* a loss matrix.** Reporting `argmax` as "the answer" silently assumes 0–1 loss — i.e. that every mistake costs the same.

*Generalising the toy example (mine, not D2L's).* Replace $\infty$ with a finite death-penalty $L$, keeping the cost of discarding an edible mushroom at 1. Eat iff
$$p\,L < (1-p)\cdot 1 \quad\Longleftrightarrow\quad p < \frac{1}{L+1}$$
At $L=4$ the threshold is exactly $p<0.2$ — precisely D2L's numbers, sitting at indifference. At $L=100$ it is $p<0.99\%$; at $L=1000$, $p<0.0999\%$. **The tolerable risk falls like $1/L$** — which is why asymmetric-cost problems (medical screening, fraud, safety) are never solved by thresholding at 0.5.

#### 4.2 Unsupervised and self-supervised learning

The boss hands you a pile of data and says *"do some data science with it"*. Vague, because it is vague. The questions you may ask are limited only by creativity:

- **Clustering** — can a small number of prototypes summarise the data?
- **Subspace estimation** — can a few parameters capture the relevant properties? *If the dependence is linear, this is [[Linear Algebra/contents/00-Index|principal component analysis]].*
- **Representation in Euclidean space** — such that symbolic relations hold, e.g. `"Rome" − "Italy" + "France" = "Paris"`.
- **Causality and probabilistic graphical models** — root causes, not just correlations.
- **Deep generative models** — estimate the data density explicitly or implicitly, then *score* examples by likelihood or *sample* new ones. Lineage: variational autoencoders (2014) → GANs (2014) → normalizing flows → **diffusion models** (2015, 2020), which now largely displace GANs in systems like DALL·E 2 and Imagen.

**Self-supervised learning** deserves separate billing: it manufactures supervision from unlabeled data. Predict randomly **masked words** from context (this is BERT); predict the relative position of two crops of one image; predict whether two examples are perturbations of the same image. The representations learned are then **fine-tuned** on a downstream task — the pattern that drives [[06 - Object Detection]] and essentially all modern practice.

#### 4.3 Interacting with an environment

Everything above is **offline learning**: grab a pile of data, run the pattern recogniser, never touch the environment again. That has real charm — no dynamics to worry about — and it is limiting, because **actions change the world**, whereas predictions do not.

Once you interact, new questions appear: does the environment remember what you did? Does it want to *help* you (a user dictating to a speech recogniser) or *beat* you (a spammer evading a filter)? Do its dynamics shift? These raise **distribution shift** — train and test data differ. D2L's analogy is one every student has lived: **the homework was written by the teaching assistants and the exam was written by the lecturer.** Treated properly in [[03 - Logistic Regression]].

#### 4.4 Reinforcement learning

An agent takes **actions**, receives **observations** and **rewards** over time steps; its behaviour is a **policy**, a function from observations to actions. RL is extraordinarily general — **supervised learning can be recast as RL**: one action per class, reward equal to the negative loss.

It also handles what supervised learning cannot. You are not told the optimal action, only given a reward, and often **not told which action earned it**. In chess, the only real signal is $+1$ or $-1$ at the end of the game — the **credit assignment problem**. (D2L's other example: a promotion on October 11 reflects a year of well-chosen actions, and repeating it means working out *which* ones.) Add **partial observability** (a robot in one of many identical closets) and the **exploration–exploitation** trade-off, and you have the general problem.

**Special cases, in decreasing generality — a hierarchy worth memorising:**

| Setting | Condition | Name |
|---|---|---|
| general | partial observability, state depends on actions | **RL** |
| environment fully observed | | **Markov decision process** |
| state does not depend on previous actions | | **contextual bandit** |
| no state at all, just actions with unknown rewards | | **multi-armed bandit** |

> [!note] Boundary with another subject
> RL is **not** developed further here. [[Machine Learning/contents/00-Index|Machine Learning]] is an RL-only subject in this vault and owns MDPs, value iteration and Q-learning in full. D2L ch. 17 duplicates it.

### 5. Roots — and why the name "neural network" means less than it looks

The core ideas are centuries old: the **Bernoulli** distribution (Jacob Bernoulli, 1655–1705); the **Gaussian** distribution and **least mean squares** (Gauss, 1777–1855), still used from insurance to medical diagnostics. Ohm's law is *perfectly* described by a linear model.

D2L's loveliest example is medieval. **Jacob Köbel (1460–1533)** estimated the length of "one foot" by lining up 16 men leaving a church, measuring their feet, and dividing the sum by 16 — a sample mean. The algorithm was then *improved*: **send away the men with the shortest and longest feet and average the rest.** That is a **trimmed mean**, one of the earliest robust estimators on record. *(Mine: trimming one observation from each tail of 16 retains 87.5% of the sample, discards 6.25% per tail, and gives the estimator a **breakdown point of 1/16 = 6.25%** — it tolerates one arbitrarily corrupt measurement and fails at two. See [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].)*

Then **Fisher** (1890–1962): linear discriminant analysis, the Fisher information matrix, and the **Iris** dataset (1936) still in use. D2L does not soften the coda — *Fisher was also a proponent of eugenics*, a reminder that **morally dubious uses of data science are exactly as old as productive ones.** Also **Shannon** (information theory) and **Turing** (1950, *Computing Machinery and Intelligence*, the Turing test).

**Biological inspiration gave neural networks their name and little else.** Hebb (1949) posited that neurons learn by positive reinforcement — the *Hebbian learning rule* — inspiring Rosenblatt's perceptron and, ultimately, SGD: *reinforce desirable behaviour, diminish undesirable behaviour.* Attempts to build circuits resembling interacting neurons date to Bain (1873) and Sherrington (1890).

> **Over time the interpretation of biology has become less literal, but the name stuck.** What actually survives is two principles, and they are the entire syllabus:
> 1. **The alternation of linear and nonlinear processing units, called layers.** → [[04 - Neural Network]]
> 2. **The use of the chain rule (backpropagation) to adjust all parameters at once.** → [[04 - Neural Network]], and [[Calculus/contents/00-Index|Calculus]] for the chain rule itself.

**The winter, 1995–2005.** Neural network research languished for two reasons: **training was computationally very expensive** (RAM was plentiful, compute was scarce) and **datasets were small** (Fisher's 1936 Iris was still a standard testbed; MNIST's 60,000 digits was considered *huge*). Given scarce data and compute, **kernel methods, decision trees and graphical models were empirically superior** — and they trained in reasonable time with predictable results and strong theoretical guarantees. The neural networks were not wrong; they were **unaffordable**.

### 6. The road to deep learning — reading D2L's own table properly

Data arrived (the Web, billion-user companies, cheap sensors, cheap storage via *Kryder's law*), compute arrived (*Moore's law*, and above all **GPUs built for gaming**). D2L prints **Table 1.5.1**:

| Decade | Dataset (examples) | Memory | Floating-point ops/sec |
|---|---|---|---|
| 1970 | 100 (Iris) | 1 KB | 100 KF (Intel 8080) |
| 1980 | 1 K (Boston house prices) | 100 KB | 1 MF (Intel 80186) |
| 1990 | 10 K (optical character recognition) | 10 MB | 10 MF (Intel 80486) |
| 2000 | 10 M (web pages) | 100 MB | 1 GF (Intel Core) |
| 2010 | 10 G (advertising) | 1 GB | 1 TF (NVIDIA C2050) |
| 2020 | 1 T (social network) | 100 GB | 1 PF (NVIDIA DGX-2) |

D2L draws two conclusions from it and then moves on. **Divide the table's own columns by each other and a sharper — and partly different — picture appears.** Over the full 1970→2020 span:

$$\text{data} \times 10^{10}, \qquad \text{memory} \times 10^{8}, \qquad \text{compute} \times 10^{10}$$

| D2L's claim | Verdict over 1970–2020 |
|---|---|
| "random-access memory has not kept pace with the growth in data" | ✅ **True, and quantified: data outgrew memory by exactly $10^{2} = 100\times$.** |
| "increases in computational power have outpaced the growth in datasets" | ⚠️ **Not over the full span.** Both grew by exactly $10^{10}$ — the ratio is **1.000**. |

Stated per example, the result is striking:

$$\textbf{Memory per example: } 10 \text{ B (1970)} \;\longrightarrow\; 0.1 \text{ B (2020)} \quad (\div 100)$$
$$\textbf{Compute per example: } 1000 \text{ FLOP/s (1970)} \;\longrightarrow\; 1000 \text{ FLOP/s (2020)} \quad (\times 1.00)$$

**By D2L's own table, the FLOP/s available per training example is exactly the same today as in 1970** (dipping to 100 in 2000–2010 and recovering). The claim that compute outpaced data is a statement about the **last decade only** — where compute went $\times1000$ against data's $\times100$:

| Decade | Data | Memory | Compute |
|---|---|---|---|
| 1970→80 | ×10 | ×100 | ×10 |
| 1980→90 | ×10 | ×100 | ×10 |
| 1990→2000 | ×1000 | ×10 | ×100 |
| 2000→10 | ×1000 | ×10 | ×1000 |
| 2010→20 | ×100 | ×100 | ×1000 |

Note the inversion: **memory lags data badly in 1990–2010 and then catches up exactly in 2010–2020**, while compute only pulls ahead from 2000. So the two sentences describe *different decades*, and neither describes the whole table.

**Why this matters rather than being pedantry.** D2L's own inference is the right one and this makes it sharper: since **memory per example collapsed by 100×**, statistical models had to become memory-efficient, and were therefore *free to spend more cycles per parameter*. That is the mechanism that moved the sweet spot from **(generalized) linear models and kernel methods → deep neural networks** — a kernel method must hold pairwise relations among examples, and at $10^{12}$ examples with $0.1$ byte each that is arithmetically impossible. **Deep networks won because they stream data they cannot store.**

It also explains the "rediscovery" pattern: MLPs (McCulloch & Pitts, **1943**), CNNs (LeCun et al., **1998**), LSTM (Hochreiter & Schmidhuber, **1997**) and Q-learning (Watkins & Dayan, **1992**) all lay dormant and were revived once the resources existed. **The ideas were not the bottleneck.**

**What was genuinely new** (not just resources applied to old algorithms):

- **Dropout** (Srivastava et al., 2014) — capacity control by injecting noise through the network during training. → [[04 - Neural Network]]
- **Attention** (Bahdanau et al., 2014) — solved a century-old statistical problem: *increase a system's memory and complexity without increasing the number of learnable parameters*, via a **learnable pointer structure**. Instead of compressing a whole sentence into a fixed-dimensional vector, store a pointer into the intermediate state. → [[08 - Sequence to Sequence]]
- **The Transformer** (Vaswani et al., 2017) — attention alone, with superior **scaling behaviour**: better with more data, more parameters, more compute (Kaplan et al., 2020). One pretrained Transformer can play Atari, caption images, chat and control a robot (Reed et al., 2022). → [[08 - Sequence to Sequence]]
- **Language models** and their scaled capabilities, up to ChatGPT via alignment to human intent (Ouyang et al., 2022).
- **GANs** (Goodfellow et al., 2014) — the crucial innovation was replacing the *sampler* with an arbitrary differentiable algorithm, tuned until a discriminator (effectively a two-sample test) cannot separate fake from real.
- **Diffusion models** — the diffusion process adds noise to data; the model learns the **denoising** process, running it backwards to construct samples from noise.
- **Parallel and distributed training.** The tension: SGD wants *small* minibatches, small batches waste GPUs. Training on 1,024 GPUs at 32 images each is an aggregate minibatch of $1024 \times 32 = 32{,}768 \approx 32{,}000$; pushed to **64,000**, cutting ResNet-50 on ImageNet from **days to under 7 minutes**.
- **Frameworks**, in three generations: Caffe / Torch / Theano → TensorFlow (+Keras) / CNTK / Caffe2 / MXNet → **imperative** tools, ignited by Chainer's NumPy-like syntax and adopted by **PyTorch**, MXNet's Gluon, and JAX.

That division of labour is why *"training a linear logistic regression model"* was a nontrivial CMU PhD homework problem in 2014 and is **under 10 lines of code** today.

### 7. Success stories — with the numbers checked

ML has quietly delivered for decades: OCR mail sorting since the 1990s (the origin of MNIST), cheque reading, credit scoring, fraud detection behind PayPal/Stripe/AliPay/Visa/MasterCard. **Machine learning is pervasive, albeit often hidden from sight.**

The visible advances: intelligent assistants (Siri, Alexa, Google Assistant); speech recognition at **human parity** for some applications (Xiong et al., 2018); games — TD-Gammon → **DeepBlue** beating Kasparov by massive parallelism and special-purpose hardware (Campbell et al., 2002) → **AlphaGo** reaching human parity in 2015 with deep learning + Monte Carlo tree search (Silver et al., 2016) → **Libratus** in poker, where the state space is large **and only partially observed**; and partial vehicle autonomy (Tesla, NVIDIA, Waymo) where *deep learning is used primarily for the visual part and the rest is heavily tuned by engineers*.

**Object recognition, ImageNet top-5 error:**
$$28\% \;(2010,\ \text{Lin et al.}) \;\longrightarrow\; 2.25\% \;(2017,\ \text{Hu et al.})$$
That is a factor of **12.44×**, a **91.96% relative reduction** — or, concretely, **2,800 mistakes per 10,000 images down to 225**. *(Mine, as context: human top-5 error on this benchmark is usually quoted around 5%, so the 2017 figure is well below it.)*

**On the "AI apocalypse".** D2L's position is worth reproducing because it is unusually level-headed for a textbook. Sentient AI deliberately manipulating its creators is not the pressing concern: AI systems are engineered, trained and deployed in a **specific, goal-oriented manner**, and there are at present no tools for artificial general intelligence that improve, reason about, or modify their own architecture. **The pressing concern is the ordinary use of AI in daily life** — automation of routine work with profound consequences where menial jobs provide much employment, and racial/gender/age bias raising real questions of **procedural fairness** when models drive consequential decisions.

### 8. So what actually *is* deep learning?

> **Deep learning is the subset of machine learning concerned with models based on many-layered neural networks.** It is deep in precisely the sense that its models learn many *layers* of transformations.

The obvious objection: *all* machine learning has many layers of computation — the first ones being feature-processing steps. The answer is the definition that matters:

> **What differentiates deep learning is that the operations at each of the many layers of representation are learned JOINTLY from data.**

This is **end-to-end training**: rather than assembling a system from individually tuned components, build the whole system and tune its performance jointly. The historical illustration is exact. In computer vision, **feature engineering** was a separate discipline from model fitting; the **Canny edge detector** (1987) and **Lowe's SIFT** (2004) reigned for over a decade as the way to map images into feature vectors. Applying ML meant hand-crafting a transformation into something a shallow model could digest.

> There is only so much that human ingenuity can accomplish in comparison with **a consistent evaluation over millions of choices carried out automatically by an algorithm**.

When deep learning took over, those hand-built extractors were replaced by **automatically tuned filters** with better accuracy — a claim made concrete in [[05 - Convolutional Neural Network]], where the first layer of a trained CNN is shown to learn edge detectors on its own.

**Three consequences:**

1. **Deep learning replaces both the shallow model *and* the feature engineering** — and by removing domain-specific preprocessing it **erased the boundaries** between computer vision, speech, NLP and medical informatics. One toolkit, many fields. *(This is why this subject and the vault's Computer Vision subject share machinery — see the boundary note in [[00-Index]].)*
2. **A shift from parametric to nonparametric description.** Scarce data forces simplifying assumptions; abundant data lets models fit reality directly. D2L's analogy: physics moved from hand-solved parametric approximations of electron behaviour to numerical simulation of the underlying PDEs — **more accurate, often at the expense of interpretation.**
3. **An acceptance of suboptimal solutions** — nonconvex, nonlinear optimization, and a willingness to *try things before proving them*. This empiricism drove rapid practical progress, sometimes at the cost of re-inventing tools that had existed for decades.

## ✏️ Exercises

> [!example]- **1.** *(Easy — the contractor, and what happens when the data stops being consistent)*
> **(a)** A contractor bills \$350 for 3 hours and \$250 for 2 hours. Assuming `cost = w·hours + b`, find $w$ and $b$, and predict a 5-hour job.
> **(b)** A third invoice arrives: **\$500 for 4 hours.** Show no straight line fits all three exactly, then find the least-squares line and its prediction for 5 hours.
> **(c)** What does the failure in (b) tell you, in the vocabulary of §2?
>
> ---
> **(a)** $3w+b=350$ and $2w+b=250$. Subtracting: $w = 100$; back-substituting, $b = 50$.
> $$\boxed{w=100 \text{ \$/hour}, \quad b=50 \text{ \$ call-out}}$$
> Check: $3(100)+50=350$ ✓, $2(100)+50=250$ ✓. Prediction: $5(100)+50 = \boxed{\$550}$.
>
> **(b)** The first two points force $w=100,b=50$, which predicts $4(100)+50=450 \ne 500$. **No line fits all three.** So minimise $S(w,b)=\sum_i (wh_i+b-c_i)^2$ over $(3,350),(2,250),(4,500)$. Setting $\partial S/\partial w = \partial S/\partial b = 0$:
> $$\boxed{w = 125, \qquad b = -\tfrac{25}{3} \approx -8.33}$$
> Fitted values $\tfrac{1100}{3}, \tfrac{725}{3}, \tfrac{1475}{3} \approx 366.67,\ 241.67,\ 491.67$; residuals $+\tfrac{50}{3}, -\tfrac{25}{3}, -\tfrac{25}{3}$, which **sum to zero** (as they must when an intercept is fitted). $\mathrm{SSE} = \tfrac{1250}{3} \approx 416.67$. Prediction for 5 hours: $\tfrac{1850}{3} \approx \boxed{\$616.67}$.
>
> **(c)** Two things. First, the fitted **intercept is now negative** (−\$8.33) — a "call-out charge" that is physically absurd. That is the signature of **variation arising from factors outside your features** (§4.1): perhaps job 3 needed a part. Second, and more important, the step from **solving** two equations to **minimising** a loss over three is exactly the step from algebra into machine learning: with more examples than parameters the system is over-determined, and the **objective function** (§3) is what tells you which imperfect answer to prefer.

> [!example]- **2.** *(Easy — classify the problem type)*
> For each, name the learning problem type from §4 (regression, binary/multi-class/hierarchical classification, tagging, search, recommendation, sequence-to-sequence, clustering, self-supervised, RL) and say what one **example**, its **features**, and its **label** are.
> (a) Predicting how many minutes a surgery will take.
> (b) Auto-applying tags like "machine learning", "Linux", "AWS" to a blog post.
> (c) Transcribing a 3-second audio clip into text.
> (d) A robot vacuum learning to clean a flat it has never seen.
> (e) Training a model to predict randomly hidden words in Wikipedia.
>
> ---
> **(a) Regression.** *How many?* → arbitrary numerical target. Example = one surgery; features = patient and procedure attributes; label = duration in minutes. Loss: squared error.
>
> **(b) Tagging / multi-label classification.** The classes are **not mutually exclusive** — a post has typically 5–10 tags. Example = one post; features = its text; label = a *subset* of the tag vocabulary (a binary vector, not a single index). Note D2L's point that tags are **correlated** ("cloud computing" pulls "AWS"), which multi-class treatment cannot express.
>
> **(c) Sequence-to-sequence** (automatic speech recognition). Both input and output are variable-length, and **the output is much shorter than the input**: at 44 kHz a 3-second clip is 132,000 samples mapping to perhaps a dozen characters — no 1:1 correspondence. Example = (clip, transcript) pair.
>
> **(d) Reinforcement learning.** The agent takes actions that **change the environment**, and receives rewards rather than labelled correct actions. Note it is likely **partially observed** (§4.4) — one corner of a room looks like another — so it is not a clean MDP.
>
> **(e) Self-supervised learning.** No human labelled anything; the supervision is *manufactured* by masking words the corpus already contains. Example = a sentence with a masked token; features = the surrounding context; label = the hidden word. This is the BERT objective, and the learned representation is then fine-tuned downstream.

> [!example]- **3.** *(Medium — decisions are not argmax)*
> A classifier reports $P(\text{malignant}) = p$ for a biopsy image. Let the cost of missing a malignancy be $L$ and the cost of a false alarm (unnecessary follow-up) be 1.
> **(a)** Derive the threshold on $p$ above which you should refer the patient.
> **(b)** Evaluate it for $L = 4,\ 100,\ 1000$.
> **(c)** At $L=100$, a colleague reports "the model is 97% confident the biopsy is benign, so we discharge." Respond.
> **(d)** Which of the four components in §2 does $L$ belong to, and why does that make this a *modelling* error and not an arithmetic one?
>
> ---
> **(a)** Expected costs: refer $= (1-p)\cdot 1$ (you pay 1 when it was benign); discharge $= p \cdot L$. Refer whenever discharging costs more:
> $$p L > (1-p) \quad\Longleftrightarrow\quad \boxed{p > \frac{1}{L+1}}$$
> **(b)** $L=4 \Rightarrow p > 1/5 = 20\%$. $L=100 \Rightarrow p > 1/101 = 0.990\%$. $L=1000 \Rightarrow p > 1/1001 = 0.0999\%$. **The tolerable risk falls like $1/L$.**
>
> **(c)** 97% benign means $p = 3\%$. The threshold at $L=100$ is $0.990\%$, and $3\% > 0.990\%$ — **refer the patient.** The colleague thresholded at 50% (equivalently, assumed $L=1$: that a missed cancer and an unnecessary scan cost the same). They are wrong by a factor of about 3 in $p$, and by 100 in the assumption underneath it. Note that the model is not at fault and its probability was not disputed — *only the decision rule was*.
>
> **(d)** $L$ belongs to the **objective function**, not the data, model or optimizer. This is the point: `argmax` over the posterior is *itself* a decision rule, and it is the optimal one **only under 0–1 loss** — i.e. only when every error costs the same. Reporting the most likely class is not a neutral act; it silently asserts $L = 1$. The mushroom in §4.1 is the limiting case, $L = \infty$, where the threshold collapses to $p > 0$: **never eat it at any positive probability.**

> [!example]- **4.** *(Medium–hard — audit Table 1.5.1)*
> Using only Table 1.5.1:
> **(a)** Compute the total 1970→2020 growth factor for data, memory and compute.
> **(b)** D2L writes that memory "has not kept pace with the growth in data" and that compute has "outpaced the growth in datasets". Evaluate **both** claims quantitatively.
> **(c)** Compute memory-per-example and compute-per-example in 1970 and 2020.
> **(d)** Reconcile your answer to (b) with the fact that D2L's *conclusion* — the shift from kernel methods to deep networks — is nonetheless correct.
>
> ---
> **(a)** Data: $10^2 \to 10^{12}$, factor $\mathbf{10^{10}}$. Memory: $1\,\text{KB} = 10^3\,\text{B} \to 100\,\text{GB} = 10^{11}\,\text{B}$, factor $\mathbf{10^{8}}$. Compute: $10^5 \to 10^{15}$ FLOP/s, factor $\mathbf{10^{10}}$.
>
> **(b)** **Memory claim: true, and now quantified.** $10^{10}/10^{8} = 100$ — data outgrew memory by exactly two orders of magnitude.
> **Compute claim: not true over the full span.** $10^{10}/10^{10} = \mathbf{1.000}$ — compute and data grew by *identical* factors. Decade by decade the claim holds only from 2000 (compute ×1000 vs data ×1000, then ×1000 vs ×100), and is *false* in 1970–1990 where both grew ×10. The two sentences describe different eras of the same table.
>
> **(c)** Memory per example: $10^3/10^2 = \mathbf{10}$ B in 1970; $10^{11}/10^{12} = \mathbf{0.1}$ B in 2020 — a **100× collapse**. Compute per example: $10^5/10^2 = \mathbf{1000}$ FLOP/s in 1970; $10^{15}/10^{12} = \mathbf{1000}$ FLOP/s in 2020 — **exactly unchanged** (it dips to 100 during 2000–2010 and recovers).
>
> **(d)** The conclusion survives because it rests on the **memory** result, not the compute one. At 0.1 byte of RAM per example you cannot hold the data, still less the $O(n^2)$ pairwise structure a kernel method needs — at $n = 10^{12}$ that is $10^{24}$ entries. What you *can* do is stream examples past a model of fixed size and spend the (constant per example, but enormous in aggregate) compute budget on refining its parameters. **Deep networks won because they are $O(\text{parameters})$ in memory and unbounded in compute** — exactly the shape of the constraint. So D2L's inference is right and its stated reason is the weaker half of the argument.

> [!example]- **5.** *(Hard — recompute the winter)*
> §5 says neural network research languished from **1995 to 2005** because training was too expensive. Test that against Table 1.5.1 rather than taking it on trust.
> **(a)** Consider the wake-word detector of §1: one second of 44 kHz audio into a fully-connected hidden layer of 1,000 units. How many parameters in that layer, and how many bytes at `float32`?
> **(b)** In which decade does that model first fit in RAM?
> **(c)** Repeat for the $200\times200\times3$ image classifier.
> **(d)** What does this say about the 1995–2005 dating, and about the "rediscovery" of MLPs (1943), CNNs (1998) and LSTM (1997)?
> **(e)** Name the assumption in (a) that makes this a *lower* bound on what training actually needs.
>
> ---
> **(a)** A dense layer from $n_{\text{in}}$ to $h$ has $n_{\text{in}}h$ weights plus $h$ biases:
> $$44{,}000 \times 1{,}000 + 1{,}000 = \mathbf{44{,}001{,}000 \text{ parameters}}$$
> At 4 bytes each: $176{,}004{,}000$ B $\approx \mathbf{176\ \text{MB}}$ — **for one layer, storing only the weights.**
>
> **(b)** Against the table: 1990 offers 10 MB (short by **17.6×**), 2000 offers 100 MB (**still short by 1.76×**), 2010 offers 1 GB — **it fits**. So the model becomes storable **between 2000 and 2010**.
>
> **(c)** $120{,}000 \times 1{,}000 + 1{,}000 = 120{,}001{,}000$ parameters $= 480{,}004{,}000$ B $\approx \mathbf{480\ \text{MB}}$. Also first fits in the **2010** row — and it exceeds the entire 2000 budget by 4.8×.
>
> **(d)** The dating is **corroborated, and its mechanism is sharpened**. A naive network on *raw perceptual input* — precisely the regime D2L says deep learning excels at — did not fit in a decade's RAM until the 2000s, which is when the winter ends. And it settles the "rediscovery" question in §6: MLPs (1943), CNNs (1998) and LSTM (1997) were not revived because anyone had a better idea. **The ideas predate their feasibility by decades; the binding constraint was resources.** Note also that this argument is about *memory*, matching exercise 4 — not about FLOP/s, which per example never improved at all.
>
> **(e)** Several, all in the same direction — (a) counts **only the forward weights of a single layer**. Real training additionally stores **activations for the backward pass**, **gradients** (another $\times1$ of the parameters), and **optimizer state** (momentum and second moments: another $\times2$ for Adam, see [[04 - Neural Network]]), plus the minibatch itself. A realistic training footprint is **3–4× the parameter count**, so 176 MB becomes something like 600 MB and the model does not comfortably fit until *well* into the 2010 row. The conclusion is therefore conservative: the true winter was, if anything, **later-ending than this estimate**. *(This is also why [[05 - Convolutional Neural Network]] matters — a convolutional layer replaces those 44 million weights with a few hundred shared ones.)*

## 📝 Summary

- **Machine learning is for problems where you cannot write the rule but can judge the answer.** If a hand-coded solution works 100% of the time, do not use ML.
- **Four components, always:** data (examples, features, labels), a model, an objective function (defined so *lower is better*), and an optimization algorithm — almost always a descendant of gradient descent. During optimization, the **loss is a function of the parameters** and the data is held constant.
- **Supervised learning estimates $P(\text{label}\mid\text{features})$** and splits into regression (*how much?*), classification (*which one?*), tagging (*which ones?*), search, recommendation and sequence learning. **The problem type is fixed by the form of the target, not the algorithm.**
- **`argmax` is not a decision.** Expected loss is. D2L's mushroom is 80% safe and still inedible; generally, with penalty $L$ for the bad outcome, act only when $p < 1/(L+1)$. Reporting the most probable class silently assumes every error costs the same.
- **Unsupervised → self-supervised** is the modern arc: manufacture supervision from unlabeled data (masked words, image crops), then fine-tune downstream. **Reinforcement learning** adds actions that change the world, plus credit assignment, partial observability and exploration; MDP ⊃ contextual bandit ⊃ multi-armed bandit are its progressively simpler special cases.
- **"Neural network" is a historical name.** Two principles survive from the biology: **alternating linear and nonlinear layers**, and **the chain rule (backpropagation) to update everything at once**.
- **The 1995–2005 winter was a resource constraint, not an intellectual one.** By D2L's own Table 1.5.1, a single dense layer on one second of raw audio needs ~176 MB and does not fit in RAM until the 2010 row. MLPs (1943), CNNs (1998) and LSTM (1997) were rediscovered, not invented.
- **Read that table by dividing its columns.** Data grew $10^{10}$, compute $10^{10}$, memory only $10^{8}$: **compute per example is unchanged since 1970, while memory per example fell 100×.** That memory collapse — not a compute windfall — is what moved the field from kernel methods to deep networks.
- **Deep learning = many layers whose operations are learned *jointly*** (end-to-end training). It replaced not just shallow models but the whole discipline of feature engineering (Canny 1987, SIFT 2004), and in doing so **erased the boundaries between vision, speech and NLP**.

## ⚠️ Important Notes

1. **Do not confuse "deep" with "many steps of computation".** Every ML pipeline has many stages. What makes deep learning deep is that **the layers are learned jointly from data**, not stacked and individually tuned. This is the definition to give in an exam.
2. **A label is not a feature.** By definition the label is *not part of the model's input*. Leaking it — or a proxy for it — into the features is the most common way to produce a spectacular training score and a worthless model. (You will meet this again as **target leakage** in [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]].)
3. **"Lower is better" is a convention, not a fact.** Accuracy is a perfectly good objective; it just gets negated. Do not read significance into the sign.
4. **We optimise a surrogate because the thing we want is not differentiable.** Error rate is flat almost everywhere with jumps at the boundaries — its gradient is zero or undefined, so gradient descent is blind to it. Cross-entropy is the differentiable stand-in. **Consequently, the loss you minimise is never quite the quantity you care about**, and the two can diverge.
5. **The most likely class ≠ the right action.** Repeated because it is the chapter's most examinable idea. Decisions need the posterior *and* the loss matrix.
6. **Two data points determining two parameters is algebra, not learning.** The contractor example is solved exactly. Learning begins when the system is over-determined and you must *choose* which imperfect fit to prefer — which is what the objective function is for.
7. **Beware the negative intercept.** In exercise 1(b) the least-squares fit gives a call-out charge of −\$8.33. A fitted parameter can be numerically optimal and physically impossible; that is a signal about your features, not about your arithmetic.
8. **Residuals from a fit with an intercept always sum to zero.** Use it as a check on your algebra — but note it is a *self*-consistency check and therefore weak evidence (the vault's standing rule: verify against something independent of the model that produced the number).
9. **Fixed-length inputs are an assumption you are making, not a property of the world.** Cropping images to a standard size discards the cropped-out information. Text resists it entirely. Choosing a fixed-length representation is a modelling decision with a cost.
10. **Bias enters through the data without anyone intending it.** Under-representation (a skin-cancer model that never saw black skin) and reflected prejudice (a resume screener trained on past hiring) are different failure modes and need different fixes. Neither is detectable by looking at test accuracy on the same biased distribution.
11. **Offline learning quietly assumes your actions do not change the world.** The moment a model's outputs affect the data it will later see — recommender feedback loops, spam filters versus spammers — that assumption breaks and you have **distribution shift**. Note D2L's warning that recommender feedback is **censored**: people rate what they feel strongly about, so five-point scales show many 1s and 5s and conspicuously few 3s. *Absence of a rating is not absence of an opinion.*
12. **RL's specialisations are defined by what the state does, not by the reward.** Fully observed → MDP; state independent of past actions → contextual bandit; no state at all → multi-armed bandit. Students routinely mis-state these; the distinguishing question is always *"does my action change what I will see next?"*
13. **The winter was economic.** If an exam asks why neural networks were abandoned around 1995–2005, the answer is **scarce compute and small datasets**, and the reason kernel methods beat them was that they trained fast **with predictable results and strong theoretical guarantees**. It was a rational choice at the time.
14. **A textbook's prose and its table can disagree.** Table 1.5.1 supports one of D2L's two conclusions and refutes the other. **The habit that catches this is dividing the source's own adjacent figures by each other** — and it is the single most productive habit in this entire vault.
15. **Order-of-magnitude tables are not data.** Table 1.5.1 lists Iris as "100" examples; it actually has 150. That is not an error — every entry is rounded to a power of ten. Do not quote such a table to more precision than it claims, and do not file an erratum against it.
16. **Attention's original selling point was parameter efficiency**, not accuracy: *more memory and complexity without more learnable parameters*. Worth remembering when it reappears in [[08 - Sequence to Sequence]] looking like a purely performance-driven idea.

> [!warning] Gaps in the source material
> **Figures — all lost.** Every figure in this chapter is an image and does not extract: Fig. 1.1.1 (identify a wake word), 1.1.2 (a typical training process), 1.3.1 (supervised learning), 1.3.2 (the death cap photograph), 1.3.3 (the Bremen Town Musicians), 1.3.4 (Amazon recommendations), 1.3.5 (a speech waveform), 1.3.6 (collecting data from an environment), 1.3.7 (the RL interaction loop), 1.4.1 (Köbel measuring 16 feet). **All ten are label-schematics or illustrations whose content the prose states in full**, so nothing conceptual is lost — the four-step training loop, the agent–environment cycle and the supervised pipeline are all written out above from the text. *No figure in this chapter carried plotted data.*
>
> **Table 1.5.1 survived intact** and is reproduced above verbatim — consistent with the vault's standing finding that **numeric tables set as text survive whole while graphical exhibits are destroyed**. Its internal consistency was checked (all growth factors are exact powers of ten).
>
> **Mathematics is reconstructed, never transcribed.** This PDF's text layer deletes minus signs, arrows and multiplication signs, renders `.` as `:` and `∞` as `1`. The mushroom expected-loss line extracts as `0:21 + 0:8 0 =1`, which is $0.2\times\infty + 0.8\times 0 = \infty$ — **and the very next line's `1` is a genuine numeral 1.** Both formulas above were reconstructed from the prose and verified with `sympy`. Full substitution table in this subject's `CLAUDE.md`.
>
> **Added beyond D2L, and labelled as mine throughout:**
> - The **generalisation of the mushroom example** to a finite penalty, giving the threshold $p < 1/(L+1)$ (§4.1 and exercise 3). D2L computes only the single $\infty$ case and draws no rule from it.
> - The **audit of Table 1.5.1** (§6): all growth factors, the per-decade breakdown, memory-per-example and compute-per-example. D2L states two conclusions and computes nothing; **one of the two does not hold over the span of its own table**, which is recorded as a *discrepancy investigated and declined* rather than an erratum — the sentences are defensible as claims about the recent decades.
> - The **parameter-count argument in exercise 5**, which tests D2L's 1995–2005 dating against D2L's own memory column. The book asserts the winter's cause; it does not check it.
> - **Köbel's trimmed mean quantified** — 87.5% retained, 6.25% per tail, breakdown point 1/16. D2L notes only that it is "among the earliest examples of a trimmed mean estimate".
> - The **ImageNet arithmetic** (12.44×, 91.96% relative reduction, 2,800 → 225 errors per 10,000) and the remark that human top-5 error is around 5%. D2L prints 28% and 2.25% adjacently and does not divide them.
> - The **distributed-training check**: $1024\times32 = 32{,}768$, confirming D2L's "about 32,000", and $64{,}000/32 = 2{,}000$ GPUs.
>
> **Not covered here by design:** D2L §1.4's fuller history, and the framework/installation material. **Reinforcement learning is deliberately left at the taxonomy level** — [[Machine Learning/contents/00-Index|Machine Learning]] owns it in this vault. **Chapter 2 (Preliminaries)** is not written as a note: tensors, linear algebra and probability are held by [[Linear Algebra/contents/00-Index|Linear Algebra]] and [[Probability Theory/contents/00-Index|Probability Theory]]; only §2.4–2.5 (calculus, automatic differentiation) are pulled forward, and they are developed where they are first *used*, in [[02 - Linear Regression]] and [[04 - Neural Network]].
>
> **Unverifiable claims left as the source states them:** all citations to the literature (error rates, parity claims, dates of results) are reported as D2L reports them; the printed timings in §1.5 (ResNet-50 "under 7 minutes", "training times were initially of the order of days") are too loosely specified to convert into a speedup factor, so none is quoted.

**Previous:** [[00-Index]] · **Next:** [[02 - Linear Regression]]
