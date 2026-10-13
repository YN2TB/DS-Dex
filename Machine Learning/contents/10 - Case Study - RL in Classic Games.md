---
subject: Machine Learning
chapter: 10
tags: [ds, reinforcement-learning, self-play, minimax, td-gammon, game-theory]
source: "lecture-10-case-study-rl-in-classic-games.pdf — David Silver, UCL (Lecture 10 of 10)"
---

# Case Study: RL in Classic Games

The last lecture puts the earlier techniques together in programs that beat human champions. Why games: simple rules and deep concepts, studied for centuries, a meaningful IQ test, the "Drosophila of AI", microcosms of real-world issues, and fun.

## 📘 Main Knowledge

| Game | Level | Program | RL program and its level |
|---|---|---|---|
| Checkers | perfect | Chinook | Chinook (superhuman) |
| Chess | superhuman | Deep Blue | KnightCap / Meep (international master) |
| Othello | superhuman | Logistello | Logistello |
| Backgammon | superhuman | TD-Gammon | TD-Gammon |
| Scrabble | superhuman | Maven | Maven |
| Go | grandmaster (9×9, 19×19) | MoGo, Crazy Stone, Zen | same |
| Poker (heads-up limit Hold'em) | superhuman | Polaris | SmooCT |

Chess is the one game where RL lags behind hand-built search.

### Game theory

If the other players fix their policies $\pi^{-i}$, the **best response** $\pi^i_*(\pi^{-i})$ is optimal against them. A **Nash equilibrium** is a joint policy where every player's policy is a best response, so no one wants to deviate.

- Best response is a single-agent RL problem: the other players become part of the environment, and the game becomes an MDP.
- Nash equilibrium is a fixed point of self-play RL: agents generate games against each other and each learns a best response.

**Two-player zero-sum games**: alternating players with $R^1+R^2=0$, solved by game-tree search (planning) or self-play RL. **Perfect-information** (Markov) games are fully observed: chess, checkers, Othello, backgammon, Go. **Imperfect-information** games are partially observed: Scrabble, poker.

### Minimax search

With joint policy $\pi=\langle\pi^1,\pi^2\rangle$, $v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]$. The **minimax value** maximizes white's return while minimizing black's, $v_*(s)=\max_{\pi^1}\min_{\pi^2}v_\pi(s)$; it is unique, and a minimax policy achieves it. Depth-first game-tree search finds it (Shannon, *Programming a Computer for Playing Chess*, run on paper). In the slide example, leaf values +5, +9, −6, −4, −4, −2, +7, +3 are backed up through alternating max and min layers to a root value of −2.

The tree grows exponentially, so search to a fixed depth and estimate leaf values with an **evaluation function** $v(s,\mathbf w)\approx v_*(s)$. **Binary-linear value function**: binary features $\mathbf x(s)$ (one per piece) and weights $\mathbf w$ (piece values), $v(s,\mathbf w)=\mathbf x(s)\cdot\mathbf w$ ([[06 - Value Function Approximation]]).

- **Deep Blue**: 8,000 handcrafted features, binary-linear value with weights mostly hand-tuned; parallel alpha-beta on 480 special-purpose VLSI chess chips, 200 million positions per second, 16–40 ply. Beat Kasparov 4–2 in 1997.
- **Chinook**: binary-linear value with 21 knowledge-based features × 4 game phases; alpha-beta plus **retrograde analysis** (search backwards from won positions, storing them in tables), so it plays perfectly in the endgame. Beat Marion Tinsley in 1994.

Both used hand-tuned weights; can RL learn them?

### Self-play RL

$$\text{MC: }\Delta\mathbf w=\alpha(G_t-v(S_t,\mathbf w))\nabla_{\mathbf w}v,\quad\text{TD(0): }\Delta\mathbf w=\alpha(v(S_{t+1},\mathbf w)-v(S_t,\mathbf w))\nabla_{\mathbf w}v,\quad\text{TD}(\lambda)\text{: target }G^\lambda_t.$$

**Afterstates.** In deterministic games $v_*$ suffices because the rules give the successor: $q_*(s,a)=v_*(\text{succ}(s,a))$, with $A_t=\arg\max_av_*(\text{succ}(S_t,a))$ for white and $\arg\min$ for black. Model-free control needed $Q$ only because it lacked a model ([[05 - Model-Free Control]]).

**Logistello** (Othello) built its own features: starting from raw inputs ("black stone at C1?"), it formed 1.5 million conjunctions/disjunctions, with a binary-linear value. It used generalized policy iteration: self-play games → Monte Carlo evaluation (regress on outcomes) → greedy improvement. It beat world champion Takeshi Murakami 6–0.

**TD-Gammon** (backgammon): random initial weights, self-play, non-linear TD with a neural network ($\delta_t=v(S_{t+1},\mathbf w)-v(S_t,\mathbf w)$, $\Delta\mathbf w=\alpha\delta_t\nabla_{\mathbf w}v$), greedy improvement with no exploration. It always converged in practice ("not true for other games"). No expert knowledge gave strong intermediate play; hand-crafted features, advanced (1991); 2-ply search, strong master (1993); 3-ply search, superhuman (1998). It beat world champion Luigi Villa 7–1 (1992).

### Combining RL and minimax search

Simple TD (update towards the successor's value with greedy selection) made Othello and backgammon superhuman but did poorly in chess and checkers: tactics hide a position's value without search (checkmates are hard to see). Can we learn from minimax search values?

- **TD root**: update the value towards the successor's search value, $v(S_t,\mathbf w)\leftarrow v_+(S_{t+1},\mathbf w)=v(l_+(S_{t+1}),\mathbf w)$, where $v_+(s)=\text{minimax}_{s'\in\text{leaves}(s)}v(s',\mathbf w)$ and $l_+(s)$ is the leaf achieving it. **Samuel's checkers player** (1959), the first TD algorithm, learned by self-play and beat an amateur.
- **TD leaf**: update the search value itself, i.e. the leaf the search relied on: $v(l_+(S_t),\mathbf w)\leftarrow v(l_+(S_{t+1}),\mathbf w)$. **KnightCap** (chess), trained against an expert from standard piece values, reached master level in a small number of games, but did not work in self-play or without good starting weights. A later **Chinook** trained by self-play with TD leaf (material weights fixed) matched or beat its hand-tuned weights.
- **TreeStrap**: update every node in the search tree towards its deeper search value, $v(s,\mathbf w)\leftarrow v(l_+(s),\mathbf w)$ for all $s\in\text{nodes}(S_t)$. **Meep** (chess), binary-linear with 2,000 features from random weights: won 13/15 games against international masters, effective in self-play and from random weights.

### Simulation-based search

Self-play RL can replace search: simulate self-play games from the root and apply RL; MC control becomes MCTS. The most effective variant is **UCT**, which uses UCB at each node ([[08 - Integrating Learning and Planning]], [[09 - Exploration and Exploitation]]); self-play UCT converges on the minimax values. MCTS is the best method in Go, Hex, Lines of Action and Amazons; simple MC search is enough in Scrabble and backgammon.

**Maven** (Scrabble): evaluates moves by score + $v(\text{rack})$, a binary-linear function of one-, two- and three-letter rack features (`Q??????`, `QU?????`, `III????`) learned by MC policy iteration; searches by imagining $n$ steps of self-play. Beat world champion Adam Logan 9–5; analysis put its error rate at 3 points per game.

### Imperfect information

Players have different information states, so separate search trees, with one node per information state (what the player knows, e.g. cards seen). Many real states share an information state, and states can be aggregated further by similarity. Methods: iterative forward search such as **counterfactual regret minimization** ("perfect" play in heads-up limit Hold'em), and self-play RL such as **Smooth UCT** (3 silver medals in two- and three-player limit Hold'em).

**Smooth UCT** applies MCTS to the information-state tree, inspired by fictitious play: agents respond to opponents' **average** behaviour, $\pi_{avg}(a\mid s)=N(s,a)/N(s)$, choosing by UCT with some probability and by $\pi_{avg}$ otherwise.

### The recipe

| Program | Game | Features | Value function | RL | Training | Search |
|---|---|---|---|---|---|---|
| Meep | chess | binary (pieces, pawns, …) | linear | TreeStrap | self-play / expert | αβ |
| Chinook | checkers | binary (pieces, …) | linear | TD leaf | self-play | αβ |
| Logistello | Othello | binary (disc configurations) | linear | MC | self-play | αβ |
| TD-Gammon | backgammon | binary (checker counts) | neural network | TD(λ) | self-play | αβ / MC |

(The Go row is cut off in the source.) Binary features → linear or neural value → a TD variant → self-play → search when deciding.

## ✏️ Exercises

**1.** How does a game reduce to an MDP, and why is Nash equilibrium the fixed point of self-play?

> [!example]- Solution
> With the opponents' policies fixed, their moves are just part of the transition dynamics, so the best response is the optimal policy of an MDP and lectures 1–9 apply. But opponents also learn, so the MDP keeps changing. Self-play repeats best responses; it stops changing when every policy is already a best response, which is the definition of a Nash equilibrium. Policy iteration is the analogous fixed-point iteration, but self-play need not converge: best responses can cycle (rock → paper → scissors). Responding to the opponents' average (fictitious play, Smooth UCT) damps this; zero-sum perfect-information games have the minimax structure to help.

**2.** Explain afterstates and why deterministic games can use $V$ rather than $Q$.

> [!example]- Solution
> Improving from $V$ needs a model; in a deterministic game the rules are the model, so $q_*(s,a)=v_*(\text{succ}(s,a))$ and greedy selection compares afterstate values. Benefits: $|\mathcal A|$ times fewer values (~35 moves in chess), and transpositions (different moves reaching the same position) share one value instead of separate $Q$ entries. In backgammon the successor depends on the dice, so TD-Gammon evaluates the position before the roll and averages over the 21 possible rolls.

**3.** Explain TD root → TD leaf → TreeStrap, and why chess needed it when backgammon didn't.

> [!example]- Solution
> In backgammon static features predict the outcome well and the dice smooth out tactics; in chess a quiet position can lose to a forced mate, so static successor values are a corrupted target. TD root learns from search values but updates the root, which the search didn't evaluate. TD leaf updates the leaf that determined the search value; KnightCap reached master level but needed an expert opponent and sensible piece values, since it gets one update per move. TreeStrap updates every searched node towards its deeper value, turning one search into thousands of training examples, which is why Meep learns from random weights in self-play. It is bootstrapping from a better estimate of the same quantity, here deeper in the tree instead of later in time.

**4.** TD-Gammon used no exploration and converged despite the deadly triad. Why?

> [!example]- Solution
> The dice force the game into positions the agent wouldn't choose, so state coverage comes from the environment; ε-greedy exists to ensure such coverage. Chess is deterministic, so greedy self-play can repeat the same lines.
> It used non-linear approximation and bootstrapping, which can diverge ([[06 - Value Function Approximation]]). Plausible reasons it didn't: the dice make the value function smooth; self-play is on-policy, so states are updated in the proportions visited; and the features suit the game. The lecture's "not true for other games" is the point: it worked for this domain, and later methods (replay, fixed targets) were needed elsewhere.

**5.** (Advanced) How do imperfect-information games differ, and what does responding to average behaviour achieve?

> [!example]- Solution
> Each player searches a tree of their own information states; many real states look the same (a POMDP, like aliasing in [[07 - Policy Gradient Methods]]). There is no single position to evaluate, only beliefs, and the beliefs depend on the opponent's strategy (which hands would bet like this). Deterministic strategies are exploitable (always bluff / never bluff), so equilibria are mixed.
> Best-responding to the opponent's current policy can oscillate. Fictitious play best-responds to the historical average and converges to Nash in two-player zero-sum games; Smooth UCT brings this into MCTS, and the visit-count average is itself a mixed strategy. CFR reached near-perfect heads-up limit Hold'em; Smooth UCT won silver medals.

## 📝 Summary

- Fixing opponents turns a game into an MDP; Nash equilibrium is the fixed point of self-play.
- Zero-sum: $R^1+R^2=0$; minimax value $\max\min v_\pi$ by depth-limited search with a learned or hand-tuned evaluation function.
- Deep Blue and Chinook: hand-tuned binary-linear weights plus massive search.
- Afterstates let deterministic games use $V$.
- Logistello (MC + GPI) and TD-Gammon (neural TD, self-play, no exploration) reached superhuman play.
- Simple TD fails in chess; TD root → TD leaf → TreeStrap learn from search, TreeStrap from every node.
- UCT = MCTS + UCB; Maven used MC rollouts.
- Imperfect information: information-state trees, mixed strategies, CFR and Smooth UCT.
- Recipe: binary features, linear/neural value, TD variant, self-play, search.

## ⚠️ Important Notes

1. Self-play can cycle; averaging stabilizes it.
2. Afterstates require a known model.
3. In stochastic games the afterstate value averages over chance outcomes.
4. TD-Gammon's lack of exploration relies on the dice.
5. Its convergence under the deadly triad is domain-specific.
6. Simple TD fails when static evaluation misses tactics.
7. TreeStrap's strength is the number of updates per move.
8. KnightCap needed an expert opponent and good starting weights.
9. Imperfect-information games need mixed strategies.
10. With hidden information, evaluation depends on the opponent model.

> [!warning] Gaps in the source slides
> - Slides 12–15 (minimax example tree) are images; the leaf and backed-up values extracted, but their positions in the tree did not, so only the root value is stated.
> - Slide 17's chess figure is an image (its arithmetic extracted garbled). Slides 24, 27 (TD-Gammon network; "New TD-Gammon Results" title only), 30, 32, 35 (TD root/leaf/TreeStrap diagrams) are images. Slide 28 and slide 40 are extracts from other papers.
> - Slide 44's recipe table stops at "Go"; the Go row is lost.
> - Truncated: slides 5, 7, 8, 10, 18–21, 33, 37, 41–43; completed from context ("unique minimax value function", "converges on the minimax values").
> - References: Shannon (1950); Samuel (1959); Tesauro (TD-Gammon); Baxter, Tridgell & Weaver (KnightCap); Veness, Silver, Uther & Blair (2009, TreeStrap); Buro (Logistello); Schaeffer (Chinook); Sheppard (2002, Maven); Heinrich & Silver (Smooth UCT).

**Previous:** [[09 - Exploration and Exploitation]] · **Back to** [[00-Index]]
