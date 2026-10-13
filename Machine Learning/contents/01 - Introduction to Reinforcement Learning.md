---
subject: Machine Learning
chapter: 01
tags: [ds, reinforcement-learning, mdp, agent, reward, exploration]
source: "intro_rl.pdf — David Silver, UCL (Lecture 1 of 10)"
---

# Introduction to Reinforcement Learning

The Machine Learning slides are David Silver's UCL Reinforcement Learning course. `documents/` also holds ISL and Murphy for supervised and unsupervised learning, which the slides don't cover ([[00-Index]]). RL textbooks (free online): Sutton & Barto, *Reinforcement Learning: An Introduction*; Szepesvári, *Algorithms for Reinforcement Learning*.

## 📘 Main Knowledge

### What makes RL different

Machine learning has three branches: supervised, unsupervised, reinforcement. RL differs because:
- there is no supervisor, only a reward signal;
- feedback is delayed;
- time matters: data are sequential, not i.i.d.;
- the agent's actions affect the data it receives.

The i.i.d. assumption behind sampling theory ([[Mathematical Statistics/contents/04 - Sampling Distributions|Sampling Distributions]]) and train/test splits fails, because the agent generates its own data. RL draws on computer science, neuroscience (reward system), psychology (conditioning), operations research, optimal control and economics (bounded rationality). Examples: helicopter stunts, Backgammon, portfolios, power stations, walking robots, Atari.

### Rewards

A **reward** $R_t$ is a scalar signal of how well the agent is doing at step $t$; the agent maximizes cumulative reward.

**Reward hypothesis:** all goals can be described by the maximization of expected cumulative reward. (Silver asks: do you agree? See Exercise 1.)

| Task | Reward |
|---|---|
| helicopter | + following the trajectory, − crashing |
| Backgammon | ± for winning/losing |
| portfolio | + per \$ in the bank |
| power station | + producing power, − exceeding safety limits |
| walking robot | + forward motion, − falling |

**Sequential decisions:** actions have long-term consequences and reward may be delayed, so it can pay to give up immediate reward (an investment that matures in months; refuelling to avoid a crash hours later; blocking an opponent). Deciding which earlier actions earned a delayed reward is the **credit assignment** problem.

### Agent and environment

At each step $t$ the agent takes action $A_t$ and receives observation $O_t$ and reward $R_t$; the environment receives $A_t$ and emits $O_{t+1}$, $R_{t+1}$.

**History**: $H_t=O_1,R_1,A_1,\dots,A_{t-1},O_t,R_t$. **State** is the information used to determine what happens next, a function of the history: $S_t=f(H_t)$.

- **Environment state** $S^e_t$: the environment's private data for choosing the next observation and reward; usually invisible to the agent.
- **Agent state** $S^a_t$: what the agent uses to choose actions, and what RL algorithms use; any function of the history.
- **Information (Markov) state**: holds all useful information from the history.

A state is **Markov** iff
$$\mathbb P[S_{t+1}\mid S_t]=\mathbb P[S_{t+1}\mid S_1,\dots,S_t]:$$
the future is independent of the past given the present, so the state is a sufficient statistic and the history can be discarded. $S^e_t$ and $H_t$ are both Markov.

The **rat example**: after a sequence of lights, bells and levers, is the agent state the last three items, the counts of each, or the whole sequence? Each choice predicts something different (Exercise 2).

**Fully observable**: $O_t=S^a_t=S^e_t$, a **Markov decision process** (MDP), [[02 - Markov Decision Processes]]. **Partially observable** (a robot with a camera doesn't know its absolute position; a trader sees only prices; a poker player sees only public cards): a **POMDP**, where the agent builds its own state, e.g. the full history $S^a_t=H_t$ (other options truncated in the source).

### Inside an agent

- **Policy** (behaviour): deterministic $a=\pi(s)$ or stochastic $\pi(a\mid s)=\mathbb P[A_t=a\mid S_t=s]$.
- **Value function** (predicted future reward): $v_\pi(s)=\mathbb E_\pi[R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\dots\mid S_t=s]$, with discount γ ([[02 - Markov Decision Processes]]).
- **Model** (predicts the environment): $\mathcal P^a_{ss'}=\mathbb P[S_{t+1}=s'\mid S_t=s,A_t=a]$, $\mathcal R^a_s=\mathbb E[R_{t+1}\mid S_t=s,A_t=a]$. It may be imperfect.

**Maze example**: reward −1 per step, actions N/E/S/W, state = location. The policy is an arrow per cell; the value function goes from −24 near the start to −1 next to the goal (minus the number of steps left); the model is the grid layout with immediate reward −1 everywhere.

| By representation | Policy | Value function |
|---|---|---|
| value-based | implicit | ✓ |
| policy-based | ✓ | ✗ |
| actor-critic | ✓ | ✓ |

**Model-free** agents have a policy and/or value function but no model; **model-based** agents also have a model. Chapters 04–05 are value-based and model-free, 07 policy-based, 08 model-based.

### Problems within RL

| Reinforcement learning | Planning |
|---|---|
| environment initially unknown | model known |
| agent interacts with it | agent computes with the model (deliberation, search) |
| improves its policy | improves its policy |

Atari as learning: unknown rules, learn from pixels and score. As planning: a queryable emulator ("if I take $a$ in $s$, what next state and score?") allows tree search.

**Exploration vs exploitation**: find a good policy without losing too much reward along the way. Exploration gathers information, exploitation uses it; both are usually needed. Examples: favourite vs new restaurant; best-performing vs new advert; best known vs new drilling site; best vs experimental move ([[09 - Exploration and Exploitation]]).

**Prediction vs control**: prediction evaluates the future for a given policy ("value function of the uniform random policy in Gridworld?"); control finds the best policy ("optimal value function and policy?"). Control is usually built on prediction.

Course: Part I, elementary RL (introduction, MDPs, dynamic programming, model-free prediction, model-free control); Part II, RL in practice (value function approximation, policy gradients, learning and planning, exploration, games).

## ✏️ Exercises

**1.** (Slide 13) Do you agree with the reward hypothesis? Argue both sides.

> [!example]- Solution
> For: preferences satisfying mild consistency axioms can be represented by a utility function (von Neumann–Morgenstern), and all the lecture's examples reduce to scalar reward. One objective lets one algorithm play Atari, fly helicopters and manage portfolios.
> Against:
> 1. Real goals are multi-objective (safe, fast, comfortable, legal); scalarizing needs exchange rates, which are value judgments.
> 2. Mis-specified rewards get exploited (**reward hacking**): a boat-racing agent circles to re-collect targets instead of finishing.
> 3. Absolute constraints ("never do X") become prices that a large enough reward elsewhere can outbid.
> 4. The objective is often unknown, hence inverse RL and learned reward models (RLHF).
>
> It is a productive modelling assumption, not a law; its failures are the subject of AI safety ([[MLOps/contents/11 - Robust AI|Robust AI]]).

**2.** (Slide 22, rat) Compare agent states: (a) last 3 items, (b) counts of lights, bells, levers, (c) complete sequence.

> [!example]- Solution
> (a) Compact and generalizes well, but not Markov if outcomes depend on events 4+ steps back; the agent then sees identical states with different outcomes and mistakes partial observability for randomness.
> (b) Compact and order-invariant: good if order doesn't matter, fatal if it does ("bell then lever" = "lever then bell").
> (c) Always Markov, but the state space grows exponentially and each state is seen once, so nothing generalizes.
> Richer states are closer to Markov but generalize worse. Part I assumes a Markov state (the Bellman equations need it); [[06 - Value Function Approximation]] handles state spaces too large to enumerate.

**3.** Distinguish learning vs planning and prediction vs control. Why are they independent?

> [!example]- Solution
> Learning vs planning: is the model known? Prediction vs control: is the policy given? Four combinations, all in the course:
>
> | | Prediction | Control |
> |---|---|---|
> | planning | DP policy evaluation (ch. 03) | policy/value iteration (ch. 03) |
> | learning | MC, TD (ch. 04) | Sarsa, Q-learning (ch. 05) |
>
> Control usually iterates prediction: evaluate, improve greedily, repeat (generalized policy iteration). Chapter 08 combines learning and planning.

**4.** Classify with both taxonomies: (a) a table of $Q(s,a)$, acting greedily; (b) a network mapping states to action probabilities, no values; (c) a chess engine with known rules and tree search.

> [!example]- Solution
> (a) Value-based (policy implicit: $\arg\max_aQ$), model-free: Q-learning.
> (b) Policy-based, model-free: REINFORCE. Policy methods handle continuous actions and can represent stochastic optimal policies.
> (c) Model-based planning with an evaluation function (value-like) and an implicit policy. Deep Blue is nearly pure planning; AlphaZero adds learning through self-play ([[10 - Case Study - RL in Classic Games]]).

**5.** (Advanced) Why does violating i.i.d. make RL harder than supervised learning?

> [!example]- Solution
> The agent generates its own data, so:
> 1. The data distribution depends on the policy, which keeps changing: a moving target.
> 2. Consecutive samples are correlated, inflating gradient variance (experience replay breaks this up).
> 3. Rewards are delayed: no label says which step was the mistake.
> 4. Exploration costs reward.
> 5. Function approximation + bootstrapping + off-policy learning (the "deadly triad") can diverge ([[06 - Value Function Approximation]]).
>
> So RL lacks a clean held-out test set and needs far more samples, which is why it succeeds first where simulation is cheap (games).

## 📝 Summary

- RL: no supervisor, delayed feedback, sequential non-i.i.d. data, actions affect data.
- Reward hypothesis: goals = maximizing expected cumulative (scalar) reward.
- History $H_t$; state $S_t=f(H_t)$; environment, agent and Markov states.
- Markov: the future is independent of the past given the present.
- Fully observable → MDP; partially observable → POMDP.
- Agent components: policy, value function, model.
- Taxonomies: value-based / policy-based / actor-critic; model-free / model-based.
- Learning vs planning; exploration vs exploitation; prediction vs control.

## ⚠️ Important Notes

1. Reward is scalar; multi-objective goals need exchange rates.
2. The agent optimizes the reward you wrote, not the goal you meant.
3. The agent state is a design choice that determines what can be learned.
4. Markov is a property of your state representation.
5. Part I assumes full observability.
6. Value-based agents have an implicit policy.
7. Learning/planning and prediction/control are independent axes.
8. Prediction comes before control.
9. Exploration costs reward.
10. RL data are correlated and non-stationary.
11. RL is sample-hungry.

> [!warning] Gaps in the source slides
> - Images: slides 10–12 (helicopter, robots, Atari), 16–17 and 19–20 (agent–environment loops; text survives), 22 (the rat's stimulus sequence), 28 (Atari value function, title only), 30–33 (maze grids; numbers survive), 34–36 (taxonomy diagrams), 44–45 (Gridworld layout).
> - Slide 24 is cut after "Complete history: $S^a_t=H_t$"; other POMDP state options (beliefs, recurrent states) are in Sutton & Barto.
> - Admin slides describe UCL's assessment (50% coursework with an assignment on kernels, 50% exam), not NEU's.

**Next:** [[02 - Markov Decision Processes]]
