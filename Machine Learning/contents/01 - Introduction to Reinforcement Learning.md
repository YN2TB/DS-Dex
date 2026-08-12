---
subject: Machine Learning
chapter: 01
tags: [ds, reinforcement-learning, mdp, agent, reward, exploration]
source: "intro_rl.pdf — David Silver, UCL (Lecture 1 of 10)"
---

# Introduction to Reinforcement Learning

> [!note] Course context
> The Machine Learning slides in this vault are **David Silver's UCL Reinforcement Learning course** (10 lectures). The `documents/` folder also holds two classical ML textbooks — **ISL** (James, Witten, Hastie, Tibshirani) and **Murphy's *Machine Learning: A Probabilistic Perspective*** — which cover supervised and unsupervised learning; the slides do not. See [[00-Index]].
>
> **Textbooks for the RL portion** (both free online):
> - **Sutton & Barto, *An Introduction to Reinforcement Learning*** (MIT Press, 1998) — the standard reference
> - **Szepesvári, *Algorithms for Reinforcement Learning*** (Morgan & Claypool, 2010)

## 📘 Main Knowledge

### What makes RL different

**The three branches of machine learning:** Supervised Learning · Unsupervised Learning · **Reinforcement Learning**.

> **What makes reinforcement learning different from other ML paradigms?**
>
> - **There is no supervisor, only a reward signal**
> - **Feedback is delayed, not instantaneous**
> - **Time really matters** (sequential, **non-i.i.d.** data)
> - **The agent's actions affect the subsequent data it receives**

Each point breaks an assumption the rest of statistics and ML rely on. The **i.i.d. assumption** underpins the sampling theory of [[Mathematical Statistics/contents/04 - Sampling Distributions|Sampling Distributions]] and the train/test split of [[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]] — and RL violates it by construction, because the agent generates its own data.

**RL sits at the intersection of many fields:** Computer Science (machine learning) · Neuroscience (reward system) · Psychology (classical/operant conditioning) · Mathematics (operations research) · Engineering (optimal control) · Economics (bounded rationality).

**Examples:** fly stunt manoeuvres in a helicopter · defeat the world champion at Backgammon · manage an investment portfolio · control a power station · make a humanoid robot walk · play Atari games better than humans.

---

### Rewards

> A **reward** $R_t$ is a **scalar** feedback signal indicating how well the agent is doing at step $t$. **The agent's job is to maximise cumulative reward.**

> **Definition (Reward Hypothesis)**
> **All goals can be described by the maximisation of expected cumulative reward.**
>
> *Do you agree with this statement?*

That question is deliberately provocative — see Exercise 1.

**Examples of rewards:**

| Task | Reward |
|---|---|
| Helicopter stunts | + for following the desired trajectory, − for crashing |
| Backgammon | +/− for winning/losing a game |
| Investment portfolio | + for each \$ in the bank |
| Power station | + for producing power, − for exceeding safety thresholds |
| Humanoid walking | + for forward motion, − for falling over |

### Sequential decision making

> **Goal:** select actions to maximise **total future reward**.
> - Actions may have **long-term consequences**
> - **Reward may be delayed**
> - It may be better to **sacrifice immediate reward to gain more long-term reward**

*Examples:* a financial investment may take months to mature · refuelling a helicopter might prevent a crash in several hours · blocking an opponent's moves might help winning chances many moves later.

**This is the credit assignment problem**, and it is why RL is hard: when reward finally arrives, which of the hundred preceding actions deserves the credit?

---

### Agent and environment

At each step $t$:

| The agent | The environment |
|---|---|
| Executes action $A_t$ | Receives action $A_t$ |
| Receives observation $O_t$ | Emits observation $O_{t+1}$ |
| Receives scalar reward $R_t$ | Emits scalar reward $R_{t+1}$ |

*$t$ increments at each environment step.*

### History and state

> The **history** is the sequence of observations, actions, and rewards:
> $$H_t = O_1, R_1, A_1, \dots, A_{t-1}, O_t, R_t$$
> i.e. all observable variables up to time $t$ — the sensorimotor stream of a robot or embodied agent.

What happens next depends on the history: the agent selects actions, the environment selects observations and rewards.

> **State is the information used to determine what happens next.** Formally, state is a function of the history:
> $$S_t = f(H_t)$$

**Three distinct states:**

- **Environment state $S_t^e$** — the environment's **private** representation, whatever data it uses to pick the next observation and reward. **Not usually visible to the agent**, and even if visible may contain irrelevant information.
- **Agent state $S_t^a$** — the agent's **internal** representation, whatever information it uses to pick the next action. **This is the information used by RL algorithms.** It can be any function of history: $S_t^a = f(H_t)$.
- **Information state (Markov state)** — contains all useful information from the history.

> **Definition:** A state $S_t$ is **Markov** if and only if
> $$\mathbb{P}[S_{t+1} \mid S_t] = \mathbb{P}[S_{t+1} \mid S_1, \dots, S_t]$$
>
> **"The future is independent of the past given the present."**
> $$H_{1:t} \to S_t \to H_{t+1:\infty}$$
>
> Once the state is known, **the history may be thrown away** — the state is a **sufficient statistic** of the future.

The environment state $S_t^e$ is Markov. The history $H_t$ is Markov (trivially — it contains everything).

**Choosing the agent state is a design decision.** The **rat example** poses it: given a sequence of lights, bells, and levers, what if the agent state is the last 3 items? The counts of each item? The complete sequence? Each gives a different agent that generalises differently — and can disagree about what happens next.

### Observability

**Fully observable** — the agent directly observes the environment state:
$$O_t = S_t^a = S_t^e$$
Agent state = environment state = information state. **Formally this is a Markov Decision Process (MDP)** — the subject of [[02 - Markov Decision Processes]] and the majority of the course.

**Partially observable** — the agent observes the environment indirectly:
- A robot with camera vision isn't told its absolute location
- A trading agent only observes current prices
- A poker agent only observes public cards

Now agent state ≠ environment state. **Formally a partially observable Markov decision process (POMDP)**, and the agent must construct its own state representation — e.g. the complete history $S_t^a = H_t$ *(further options truncated in source)*.

---

### Inside an RL agent

> An RL agent may include one or more of these components:
> - **Policy** — the agent's behaviour function
> - **Value function** — how good is each state and/or action
> - **Model** — the agent's representation of the environment

**Policy** — a map from state to action:
$$\text{Deterministic: } a = \pi(s) \qquad \text{Stochastic: } \pi(a\mid s) = \mathbb{P}[A_t = a \mid S_t = s]$$

**Value function** — a **prediction of future reward**, used to evaluate the goodness of states and therefore to select between actions:
$$v_\pi(s) = \mathbb{E}_\pi\big[R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots \mid S_t = s\big]$$

The discount factor $\gamma$ appears here without explanation; it is developed in [[02 - Markov Decision Processes]].

**Model** — predicts what the environment will do next. $\mathcal{P}$ predicts the next state, $\mathcal{R}$ the next immediate reward:
$$\mathcal{P}^a_{ss'} = \mathbb{P}[S_{t+1} = s' \mid S_t = s, A_t = a] \qquad \mathcal{R}^a_s = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$$

### The maze example

The running illustration: **rewards** −1 per time-step · **actions** N, E, S, W · **states** the agent's location.

- **Policy** — arrows in each cell showing $\pi(s)$
- **Value function** — a number in each cell giving $v_\pi(s)$, ranging from −24 near the start to −1 next to the goal
- **Model** — the grid layout represents the transition model $\mathcal{P}^a_{ss'}$; the numbers represent the immediate reward $\mathcal{R}^a_s$ (here −1 everywhere)

> The agent may have an internal model of the environment — dynamics (how actions change state) and rewards. **The model may be imperfect.**

Because reward is −1 per step, maximising cumulative reward means **minimising the number of steps** — the value function is (minus) the distance to the goal.

### RL agent taxonomy

**By what the agent represents:**

| Type | Policy | Value Function |
|---|---|---|
| **Value Based** | No policy (**implicit**) | ✓ |
| **Policy Based** | ✓ | ✗ |
| **Actor Critic** | ✓ | ✓ |

**By whether it has a model:**

| Type | Model |
|---|---|
| **Model Free** | ✗ (policy and/or value function only) |
| **Model Based** | ✓ (plus policy and/or value function) |

These two axes generate the full taxonomy, and they organise the whole course: [[04 - Model-Free Prediction]] and [[05 - Model-Free Control]] are value-based and model-free; [[07 - Policy Gradient Methods]] is policy-based; [[08 - Integrating Learning and Planning]] is model-based.

---

### Problems within RL

**Learning vs Planning** — two fundamental problems in sequential decision making:

| **Reinforcement Learning** | **Planning** |
|---|---|
| The environment is **initially unknown** | A model of the environment **is known** |
| The agent **interacts** with the environment | The agent performs **computations with its model**, without external interaction |
| The agent improves its policy | The agent improves its policy |
| | *a.k.a. deliberation, reasoning, introspection, pondering, thought, search* |

**Atari illustrates both.** As *learning*: the rules are unknown, so the agent learns directly from interactive game-play — picking joystick actions, seeing pixels and scores. As *planning*: the rules are known, the emulator can be queried (a **perfect model inside the agent's brain**), so the agent can ask *"if I take action $a$ from state $s$, what would the next state be, and what would the score be?"* and **plan ahead via tree search**.

**Exploration and Exploitation** — RL is like trial-and-error learning:

> The agent should discover a good policy from its experiences of the environment, **without losing too much reward along the way.**
>
> - **Exploration** finds more information about the environment
> - **Exploitation** exploits known information to maximise reward
> - **It is usually important to explore as well as exploit**

| Domain | Exploitation | Exploration |
|---|---|---|
| Restaurant selection | Go to your favourite restaurant | Try a new restaurant |
| Online banner ads | Show the most successful advert | Show a different advert |
| Oil drilling | Drill at the best known location | Drill at a new location |
| Game playing | Play the move you believe is best | Play an experimental move |

Developed fully in [[09 - Exploration and Exploitation]].

**Prediction vs Control:**
- **Prediction** — **evaluate the future**, *given a policy*
- **Control** — **optimise the future**, *find the best policy*

The Gridworld example poses both: *"What is the value function for the uniform random policy?"* (prediction) versus *"What is the optimal value function over all possible policies, and what is the optimal policy?"* (control).

**This distinction structures the entire course.** Prediction is always the easier problem, and control is typically built on top of it — [[04 - Model-Free Prediction]] before [[05 - Model-Free Control]].

### Course outline

**Part I: Elementary Reinforcement Learning**
1. Introduction to RL
2. Markov Decision Processes
3. Planning by Dynamic Programming
4. Model-Free Prediction
5. Model-Free Control

**Part II: Reinforcement Learning in Practice**
1. Value Function Approximation
2. Policy Gradient Methods
3. Integrating Learning and Planning
4. Exploration and Exploitation
5. Case study — RL in games

## ✏️ Exercises

**1.** *(Slide 13)* The Reward Hypothesis states that **all goals can be described by the maximisation of expected cumulative reward**. **Do you agree?** Argue both sides.

> [!example]- Solution
> **The case for.** It is remarkably general. Any goal expressible as a preference ordering over outcomes can, under mild consistency conditions, be represented by a utility function — the von Neumann–Morgenstern result from decision theory. Winning a game, walking without falling, maximising portfolio value, keeping a power station within safety limits: all of the lecture's examples reduce cleanly to scalar reward. And the hypothesis is *productive* — it gives the entire field a single well-defined optimisation target, which is why one algorithm can play Atari, fly helicopters, and manage portfolios.
>
> **The case against — four genuine problems:**
>
> **1. Scalarisation destroys information.** Real goals are usually multi-objective: a self-driving car must be safe *and* fast *and* comfortable *and* legal. Collapsing these into one number requires choosing exchange rates between them — how many seconds of delay equal one unit of risk? — and that choice is a value judgement smuggled in as a technical parameter. Different weightings give different optimal policies, and there is no reward signal that tells you the weighting is wrong.
>
> **2. Specifying reward is genuinely hard, and mis-specification is catastrophic.** This is **reward hacking**: the agent maximises the reward you wrote rather than the goal you meant. A boat-racing agent that gets points for hitting targets learns to circle forever collecting the same targets instead of finishing. A cleaning robot rewarded for "no visible mess" learns to hide mess. The hypothesis says goals *can* be expressed as reward; it does not say doing so is easy or safe.
>
> **3. Some goals resist scalar expression.** Deontological constraints ("never do X, regardless of consequences") are awkward — you can approximate them with a large negative reward, but that is still a price rather than a prohibition, and a sufficiently large positive reward elsewhere will buy it. Process-based goals ("act fairly") are similar.
>
> **4. It presumes the objective is known in advance.** In many real settings it is exactly what we are uncertain about — which motivates **inverse RL** (infer reward from observed behaviour) and preference-based methods like RLHF, which learn a reward model rather than assuming one.
>
> **The honest position:** the hypothesis is a productive modelling assumption, not a metaphysical claim. It has enabled the field; its failure modes are the subject of AI safety research — the same territory as [[MLOps/contents/11 - Robust AI|Robust AI]]'s concern with systems that optimise the wrong thing confidently.

**2.** *(Slide 22, rat example)* An agent sees a sequence of lights, bells, and levers. Consider three candidate agent states: (a) the last 3 items, (b) counts of lights, bells, and levers, (c) the complete sequence. Discuss the trade-offs.

> [!example]- Solution
> The exercise makes a point that recurs throughout RL: **the agent state is a design choice, and it determines what the agent can possibly learn.**
>
> **(a) Last 3 items.** Compact, so learning is fast and generalisation across situations is easy. But it is **not Markov** in general: if the true dynamics depend on something 4 steps back, this agent literally cannot represent the distinction, and no amount of data fixes it. It will see identical states leading to different outcomes and conclude the environment is stochastic when it is merely partially observed.
>
> **(b) Counts.** Also compact, and invariant to *order*. That is a strength if order genuinely does not matter — it generalises across many histories that are equivalent — and a fatal weakness if it does. "Bell then lever" and "lever then bell" become indistinguishable.
>
> **(c) Complete sequence.** **Guaranteed Markov** (the history is always Markov, as slide 21 notes) so nothing is lost. But it is useless in practice: the state space grows exponentially with time, every state is visited **at most once**, and there is nothing to generalise from. An agent that has never seen the exact current history has no basis for acting.
>
> **The trade-off is the central tension:** richer state ⇒ more nearly Markov ⇒ but larger state space and worse generalisation. Poorer state ⇒ better generalisation ⇒ but the Markov property fails and the agent is systematically blind.
>
> **Why this matters for the rest of the course.** Almost everything in Part I *assumes* full observability and a Markov state, because [[02 - Markov Decision Processes]] onward depends on it — the Bellman equations only hold under the Markov property. Part II's [[06 - Value Function Approximation]] is precisely the machinery for handling state spaces too large to enumerate, which is what option (c) forces on you.
>
> Note this is the same modelling tension as feature engineering in supervised learning ([[Data Preparation and Visualization/contents/08 - Feature Selection|Feature Selection]]): too few features lose signal, too many destroy generalisation. RL's version is harder because the consequence of a bad state representation is not merely poor accuracy but a **provably unlearnable problem**.

**3.** Explain the difference between **learning** and **planning**, and between **prediction** and **control**. Why are these two distinctions independent?

> [!example]- Solution
> **Learning vs planning is about whether you have a model.**
> - **Learning** — the environment is unknown, so the agent must **interact** with it to gather information. Every mistake costs real reward.
> - **Planning** — a model is known, so the agent can **compute** without interacting. Mistakes during planning are free; you can simulate a disastrous action and simply not take it.
>
> **Prediction vs control is about whether the policy is given.**
> - **Prediction** — given a policy $\pi$, evaluate it: what is $v_\pi(s)$?
> - **Control** — find the best policy: what is $v_*(s)$ and $\pi_*$?
>
> **They are independent because they answer different questions**, giving four combinations — and the course covers all four:
>
> | | **Prediction** | **Control** |
> |---|---|---|
> | **Planning** (model known) | Policy evaluation via DP — [[03 - Planning by Dynamic Programming]] | Policy/value iteration — [[03 - Planning by Dynamic Programming]] |
> | **Learning** (model unknown) | MC and TD evaluation — [[04 - Model-Free Prediction]] | Sarsa, Q-learning — [[05 - Model-Free Control]] |
>
> The lecture's own Gridworld slides pose both prediction (*"what is the value function for the uniform random policy?"*) and control (*"what is the optimal value function and policy?"*) on the same environment, making clear they are separate questions about one problem.
>
> **Why prediction always comes first.** Control is typically built by *iterating* prediction: evaluate the current policy, improve it greedily with respect to the resulting values, repeat. That loop — **generalised policy iteration** — is the organising idea of Part I, and it is why every control lecture follows a prediction lecture.
>
> **The Atari example shows learning and planning on the same task**: unknown rules means learning from pixels; a queryable emulator means planning by tree search. [[08 - Integrating Learning and Planning]] combines them — learn a model from experience, then plan with it.

**4.** Categorise each agent using both taxonomies (value/policy/actor-critic and model-free/model-based): (a) an agent storing $Q(s,a)$ for every state-action pair, acting greedily; (b) an agent with a neural network mapping states to action probabilities, no value estimates; (c) a chess engine using known rules and tree search.

> [!example]- Solution
> **(a) Value-based, model-free.** It stores only a value function; the policy is **implicit** — "take $\arg\max_a Q(s,a)$" is derived from the values rather than stored separately. That is exactly the lecture's *"No Policy (Implicit)"*. It is model-free because $Q$ says how good actions are without predicting what the environment will do. **Q-learning** is the canonical example — [[05 - Model-Free Control]].
>
> **(b) Policy-based, model-free.** The network *is* the policy $\pi(a\mid s)$, parameterised directly, with no value function and no model. This is **REINFORCE** and its relatives — [[07 - Policy Gradient Methods]].
>
> Worth noting why anyone would give up value functions: policy-based methods handle **continuous action spaces** naturally (you cannot take $\arg\max$ over a continuum) and can learn **stochastic** optimal policies, which value-based greedy methods cannot represent.
>
> **(c) Model-based**, and value-based in the loose sense — the position evaluation function serves as a value function while the policy is implicit in the search. The chess engine has a **perfect model** (the rules) and uses it to plan. By slide 37's definitions this is **planning, not learning** — no interaction with an external environment is required. Classical Deep Blue is nearly pure planning; **AlphaZero** adds learning, using self-play to improve both a value network and a policy network while still planning with the known rules. That combination is [[10 - Case Study - RL in Classic Games]].
>
> **The two axes are genuinely independent**, which is why the lecture presents them as separate slides before combining them: (a) and (b) are both model-free but differ on the first axis; (c) shares (a)'s value-based character but differs on the second. An **actor-critic** agent stores both a policy and a value function and can be either model-free or model-based.

**5.** (Advanced) Explain why RL's violation of the i.i.d. assumption makes it fundamentally harder than supervised learning, and what problems this creates.

> [!example]- Solution
> Slide 8 lists four distinguishing features, and three of them are consequences of one fact: **the agent generates its own data.**
>
> **In supervised learning** the dataset is fixed and drawn i.i.d. from a distribution. That single assumption licenses everything: a train/test split gives an unbiased performance estimate ([[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]]), sampling theory gives confidence intervals ([[Mathematical Statistics/contents/04 - Sampling Distributions|Sampling Distributions]]), and gradient descent converges because each minibatch is an unbiased estimate of the full gradient.
>
> **In RL none of that holds**, and four concrete problems follow:
>
> **1. The data distribution depends on the policy — which is changing.** Improve the policy and the agent visits different states, so the distribution shifts *because you learned*. This is a moving target: you are optimising against a distribution that your optimisation alters. Formally it breaks the stationarity that convergence proofs assume.
>
> **2. Samples are correlated.** Consecutive states in a trajectory are highly dependent — $s_{t+1}$ is usually adjacent to $s_t$. Gradient estimates from a trajectory are therefore correlated, which inflates variance and destabilises learning. **Experience replay** exists precisely to break this correlation by sampling randomly from a buffer.
>
> **3. Credit assignment over time.** Supervised learning gets an immediate, per-example error signal. RL may act for hundreds of steps before any reward, and must then determine which actions mattered — slide 15's *"reward may be delayed"*. There is no label saying "step 47 was the mistake."
>
> **4. Exploration is required, and costs reward.** A supervised learner cannot improve its dataset; an RL agent must actively choose to visit states it knows little about, **sacrificing reward to gain information**. Slide 40 states the constraint exactly: discover a good policy *"without losing too much reward along the way."* No analogue exists in supervised learning.
>
> **A fifth, subtler problem: the deadly triad.** Combining function approximation, bootstrapping (updating estimates from other estimates), and off-policy learning can cause divergence — a failure mode with no supervised counterpart, and the reason [[06 - Value Function Approximation]] is a whole lecture rather than a footnote.
>
> **What this means practically:** RL has no clean equivalent of a held-out test set, no straightforward confidence intervals on performance, and far worse sample efficiency — often millions of interactions where supervised learning needs thousands of examples. It is why RL succeeds first in domains with cheap simulation (games) and remains hard in domains where interaction is expensive or dangerous (robotics, medicine).

## 📝 Summary

- **RL differs from other ML in four ways:** no supervisor (only reward), delayed feedback, **time matters (non-i.i.d.)**, and the agent's actions affect the data it receives.
- **Reward Hypothesis:** all goals can be described by maximising expected cumulative reward. Reward is **scalar**.
- **Sequential decision making** means accepting lower immediate reward for higher long-term reward.
- **History $H_t$** is everything observed; **state $S_t = f(H_t)$** is what determines what happens next.
- **Three states:** environment (private), agent (used by the algorithm), information/Markov (a sufficient statistic of the future).
- **Markov:** $\mathbb{P}[S_{t+1}\mid S_t] = \mathbb{P}[S_{t+1}\mid S_1,\dots,S_t]$ — *"the future is independent of the past given the present."*
- **Fully observable ⇒ MDP; partially observable ⇒ POMDP.**
- **Three agent components:** **policy** (behaviour, $\pi(a\mid s)$), **value function** (predicted future reward, $v_\pi(s)$), **model** ($\mathcal{P}^a_{ss'}$ and $\mathcal{R}^a_s$).
- **Two taxonomies:** value-based / policy-based / actor-critic, and model-free / model-based.
- **Learning** (environment unknown, interact) vs **Planning** (model known, compute).
- **Exploration** (gain information) vs **Exploitation** (maximise reward) — you need both.
- **Prediction** (evaluate a given policy) vs **Control** (find the best policy).

## ⚠️ Important Notes

**Reward must be scalar.** Multi-objective goals require choosing exchange rates between objectives, and that choice is a value judgement disguised as a hyperparameter.

**Reward specification is where RL projects fail.** The agent maximises the reward you *wrote*, not the goal you *meant* — reward hacking. A well-optimised wrong objective is worse than a poorly optimised right one.

**The agent state is a design decision that determines what is learnable.** Too coarse and the Markov property fails, making the problem unlearnable in principle; too rich and every state is visited once, making generalisation impossible.

**The Markov property is an assumption about your state representation, not about the world.** Any environment becomes Markov with a rich enough state; the question is whether *your* state is.

**Almost all of Part I assumes full observability.** The Bellman equations require the Markov property; partial observability breaks them, which is why POMDPs are largely out of scope.

**"Value-based" does not mean "no policy" — it means the policy is implicit** in the value function, via $\arg\max_a Q(s,a)$.

**Learning ≠ control and planning ≠ prediction.** These are independent axes, giving four distinct problem settings.

**Prediction is always easier than control**, and control is typically built by iterating prediction. Skipping to control without understanding evaluation is why the course order matters.

**Exploration costs real reward.** Unlike supervised learning, gathering information is not free — the agent must pay for what it learns.

**RL data is correlated and non-stationary**, so supervised-learning intuitions about convergence, unbiased gradient estimates, and held-out evaluation do not transfer.

**Sample efficiency is RL's central practical weakness.** Millions of interactions are common, which is why success concentrates in domains with cheap simulation.

> [!warning] Gaps in the source slides
> David Silver's slides are LaTeX Beamer and extracted **unusually well** — nearly all mathematical content survived, unlike the PowerPoint-based subjects in this vault. The losses are figures only:
> - **Slides 10, 11, 12** — the helicopter manoeuvres, bipedal robots, and Atari illustrations are images with titles only.
> - **Slides 6, 7** — the "Many Faces of RL" and "Branches of ML" diagrams extracted as scattered labels, reconstructed above.
> - **Slides 16, 17, 19, 20** — the agent–environment loop diagrams; the accompanying text survived.
> - **Slide 22 (rat example)** — the three questions survived but **the stimulus sequence itself is an image**, so the specific lights/bells/levers pattern is unknown.
> - **Slide 28** — "Example: Value Function in Atari" is title-only.
> - **Slides 30–33 (maze example)** — the grid figures are images; the value numbers on slide 32 and reward numbers on slide 33 extracted.
> - **Slides 34–36** — the taxonomy diagrams; labels extracted and reconstructed as tables.
> - **Slides 44–45 (Gridworld)** — the value arrays extracted but the grid layout is an image.
> - **Slide 24** truncates at *"Complete history: $S_t^a = H$"* — the **remaining POMDP state-representation options are lost** (Sutton & Barto covers beliefs over environment states and recurrent representations).
>
> **Admin (UCL original):** Thursdays 9:30–11:00 · assessment 50% coursework, 50% exam · Assignment A on RL, Assignment B on kernels. **These are the original UCL course's arrangements, not NEU's** — check your own assessment structure.
>
> **Textbooks, both free online:** [Sutton & Barto](http://webdocs.cs.ualberta.ca/~sutton/book/the-book.html) · [Szepesvári](http://www.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf)

---
**Next:** [[02 - Markov Decision Processes]]
