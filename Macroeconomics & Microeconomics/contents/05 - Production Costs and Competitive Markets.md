---
subject: Macroeconomics & Microeconomics
chapter: 5
tags: [ds, economics, microeconomics, costs, marginal-cost, competitive-firm, shutdown, sunk-cost]
source: "Mankiw, *Principles of Microeconomics* 6e, ch. 13–14"
---

# Production Costs and Competitive Markets

**[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Chapter 03]] treated the supply curve as given. This chapter derives it** — and the answer is that **a competitive firm's marginal-cost curve *is* its supply curve.**

**Three results.**

**§2 — Mankiw's cost table ties at ATC = 1.30 for both Q = 5 and Q = 6, and the tie is the signal.** *(Recovering the underlying cost function — $TC = 3 + 0.1Q^2 + 0.2Q$, which **reproduces all 11 rows exactly** — puts the true efficient scale at $Q^*=\sqrt{30}=\mathbf{5.4772}$ with $ATC=\mathbf{1.2954}$, below both grid values.)* **[[02 - Supply, Demand and Elasticity|Ch. 02]] saw exactly this with total revenue.**

**§3 — one derivative proves what Mankiw only tabulates.** $\frac{d(ATC)}{dQ}=\frac{MC-ATC}{Q}$, so **MC cuts ATC precisely at its minimum** — and this is not a fact about costs at all, but about averages.

**§5 — shutting down and exiting have *different* thresholds, and between them a firm should lose money on purpose.** *(Computed: at $P=\$0.80$ producing loses \$2.10 while shutting down loses \$3.00 — **producing saves \$0.90**.)* That is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s sunk-cost principle in its most useful form.

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]] for the operator cipher.

## 📘 Main Knowledge

### 1. Costs, and what "cost" means

> [!note] Economic cost includes opportunity cost — which is why "profit" means two things
> **Explicit costs** require an outlay; **implicit costs** do not. **The owner's forgone salary and the forgone return on their capital are real costs** ([[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 2).
>
> $$\text{accounting profit}=\text{revenue}-\text{explicit costs}$$
> $$\textbf{economic profit}=\text{revenue}-\text{explicit}-\textbf{implicit costs}$$
>
> **Economic profit is the smaller number, and it is the one that drives decisions.** §6's "zero profit" result is unintelligible until this distinction is in place.

**The production function** relates inputs to output, and it exhibits **diminishing marginal product**: each additional worker adds less than the last, because they share a fixed amount of capital.

> [!note] Diminishing marginal product *is* rising marginal cost
> **They are the same fact seen from two sides.** If the next worker adds less output, then the next unit of output requires more labour — **so it costs more.**
>
> **This is why the total-cost curve gets steeper and why MC slopes up**, and it is also why [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s production possibilities frontier bows outward. *(Same phenomenon, three presentations.)*

### 2. ⚠️ Conrad's Coffee Shop — verified, then solved

*(Verified — Mankiw's Table 2, **all 50 internal checks pass**: every AFC, AVC, ATC and MC matches the book, and $ATC = AFC + AVC$ holds at every quantity.)*

| $Q$ | TC | VC | AFC | AVC | **ATC** | MC |
|---|---|---|---|---|---|---|
| 0 | 3.00 | 0.00 | — | — | — | — |
| 1 | 3.30 | 0.30 | 3.00 | 0.30 | 3.30 | 0.30 |
| 2 | 3.80 | 0.80 | 1.50 | 0.40 | 1.90 | 0.50 |
| 3 | 4.50 | 1.50 | 1.00 | 0.50 | 1.50 | 0.70 |
| 4 | 5.40 | 2.40 | 0.75 | 0.60 | 1.35 | 0.90 |
| **5** | 6.50 | 3.50 | 0.60 | 0.70 | **1.30** | 1.10 |
| **6** | 7.80 | 4.80 | 0.50 | 0.80 | **1.30** | 1.30 |
| 7 | 9.30 | 6.30 | 0.43 | 0.90 | 1.33 | 1.50 |
| 8 | 11.00 | 8.00 | 0.38 | 1.00 | 1.38 | 1.70 |
| 9 | 12.90 | 9.90 | 0.33 | 1.10 | 1.43 | 1.90 |
| 10 | 15.00 | 12.00 | 0.30 | 1.20 | 1.50 | 2.10 |

**Three shapes worth naming.** **AFC falls continuously** (a fixed cost spread over more units — "spreading the overhead"). **AVC rises** (diminishing marginal product). **ATC is U-shaped** because it is their sum: the first effect dominates at low output, the second at high.

> [!warning] The table ties at ATC = 1.30, and a tie means the optimum is between
> **The marginal costs run 0.30, 0.50, 0.70, … — an arithmetic sequence with common difference 0.20.** So the underlying continuous cost function is
>
> $$TC(Q)=3+0.1Q^2+0.2Q$$
>
> *(Verified: it reproduces **all 11 rows of the table exactly**.)*
>
> **Now the efficient scale can be located rather than bracketed:**
>
> $$ATC(Q)=\frac{3}{Q}+0.1Q+0.2\qquad \frac{d(ATC)}{dQ}=-\frac{3}{Q^2}+0.1=0\;\Rightarrow\;Q^*=\sqrt{30}$$
>
> $$Q^*=\mathbf{5.4772}\qquad ATC(Q^*)=\mathbf{1.2954}$$
>
> **Below the 1.30 the table shows at both $Q=5$ and $Q=6$ — and $\sqrt{30}$ sits exactly between them.**
>
> **[[02 - Supply, Demand and Elasticity|Ch. 02]] hit precisely this**: total revenue tied at \$24 for $P=3$ and $P=4$ because the true peak was at 3.5. **A tie in a discrete table is not a coincidence — it is what a grid does when it straddles an interior optimum**, and it is a reliable signal to solve the continuous problem.

### 3. ⚠️ Why marginal cost cuts average total cost at its minimum

**Mankiw shows this in a table and asserts it. One derivative proves it:**

$$\frac{d(ATC)}{dQ}=\frac{d}{dQ}\!\left(\frac{TC}{Q}\right)=\frac{Q\cdot MC-TC}{Q^2}=\boxed{\frac{MC-ATC}{Q}}$$

| | |
|---|---|
| $MC < ATC$ | $ATC$ is **falling** |
| $MC = ATC$ | $ATC$ is at its **minimum** |
| $MC > ATC$ | $ATC$ is **rising** |

*(Verified at $Q^*=\sqrt{30}$: $MC = ATC = 1.2954$ exactly. And across the range:)*

| $Q$ | MC | ATC | MC − ATC | direction |
|---|---|---|---|---|
| 4 | 1.0000 | 1.3500 | −0.3500 | falling |
| 5 | 1.2000 | 1.3000 | −0.1000 | falling |
| **5.4772** | **1.2954** | **1.2954** | **0.0000** | **minimum** |
| 6 | 1.4000 | 1.3000 | +0.1000 | rising |
| 8 | 1.8000 | 1.3750 | +0.4250 | rising |

> [!note] This is not a fact about costs — it is a fact about averages
> **Any average is pulled down by a marginal value below it and pushed up by one above it.** Your grade average falls exactly when the next test scores below it, and rises when it scores above. **The MC/ATC diagram is that arithmetic fact, drawn.**
>
> **The same argument works for AVC** — replace $TC$ with $VC$ and nothing else changes.
>
> **Stating it this way makes it memorable and makes the diagram unnecessary**, which matters because the diagram is one of the ones lost to extraction.

### 4. The competitive firm: produce where $P = MC$

**A competitive firm is a price taker, so its marginal revenue *is* the price.** Profit is maximised where $MR = MC$, hence where $P = MC$.

*(Computed:)*

| price | $Q$ from $P=MC$ | revenue | total cost | **profit** |
|---|---|---|---|---|
| \$0.20 | 0.00 | 0.00 | 3.00 | −3.00 |
| \$0.80 | 3.00 | 2.40 | 4.50 | −2.10 |
| **\$1.2954** | **5.4772** | 7.0954 | 7.0954 | **0.0000** |
| \$1.60 | 7.00 | 11.20 | 9.30 | +1.90 |
| \$2.40 | 11.00 | 26.40 | 17.30 | +9.10 |

> [!warning] The marginal-cost curve *is* the firm's supply curve
> **As the price rises, the firm's chosen quantity traces out MC exactly.** That is what a supply curve *is* — the quantity offered at each price. **So supply is not a separate object needing separate justification; it is the marginal-cost curve relabelled.**
>
> **And this closes a loop opened in [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]**, which asserted that "the height of the supply curve is the seller's cost" in order to define producer surplus. **That assertion is this result.**

### 5. ⚠️ Shutting down and exiting are different decisions

| | horizon | fixed cost is | rule |
|---|---|---|---|
| **shut down** | short run | **sunk** — paid either way | **shut down if $P < AVC$** |
| **exit** | long run | avoidable by leaving | **exit if $P < ATC$** |

*(Computed: $AVC(Q)=0.1Q+0.2$ is increasing, so **min AVC = \$0.20**; **min ATC = \$1.2954**.)*

$$\textbf{between \$0.20 and \$1.2954 the firm loses money and should keep producing}$$

| price | $Q$ | profit if producing | loss if shut down | better to |
|---|---|---|---|---|
| \$0.15 | 0.00 | −3.0000 | −3.0000 | **shut down** |
| \$0.50 | 1.50 | −2.7750 | −3.0000 | **produce** |
| **\$0.80** | 3.00 | **−2.1000** | **−3.0000** | **produce — saves \$0.90** |
| \$1.10 | 4.50 | −0.9750 | −3.0000 | **produce** |
| \$1.60 | 7.00 | +1.9000 | −3.0000 | produce |

> [!warning] "We are losing money, so we should stop" is the wrong answer
> **At \$0.80 the firm loses \$2.10 by producing and would lose \$3.00 by shutting down. Producing is better by \$0.90 — losing money is the right decision.**
>
> **This is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s sunk-cost principle in its most useful application.** The fixed cost is identical under both options, so it **differentiates to zero** and drops out of the comparison entirely. **Including it produces exactly the wrong answer.**
>
> **The practical form: compare *variable* cost to revenue for a stay-or-stop decision in the short run, and *total* cost only when the fixed cost can actually be escaped.** The test is not "is this cost large" but **"does this cost differ between my options."**
>
> *(A restaurant open through a quiet January, a factory running below break-even during a recession, an airline flying a half-empty route — all correct, for this reason.)*

### 6. The long run: entry and exit drive profit to zero

*(Computed:)*

| price | $Q$ | profit | what happens next |
|---|---|---|---|
| \$1.10 | 4.500 | −0.9750 | **exit** until $P$ rises |
| **\$1.2954** | **5.4772** | **0.0000** | **equilibrium** |
| \$1.50 | 6.500 | +1.2250 | **entry** until $P$ falls |
| \$2.00 | 9.000 | +5.1000 | **entry** until $P$ falls |

> [!note] Three things become true at once, and that is the efficiency result
> **In long-run equilibrium:**
> $$P=MC=\text{minimum }ATC$$
>
> - **$P = MC$** — the firm is maximising profit;
> - **$P = $ min $ATC$** — free entry has competed profit away;
> - **so every firm operates at its *efficient scale*.**
>
> **The good is produced at the lowest possible cost *and* sold at that cost.** **That is the precise content of [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s claim that competitive markets are efficient** — and [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]] is what happens when the firm is not a price taker.
>
> **⚠️ "Zero profit" does not mean the owner earns nothing.** Economic cost already includes the opportunity cost of the owner's capital and time (§1), so **zero *economic* profit means earning exactly the normal return available elsewhere.** Accounting profit is positive. **Firms stay in business indefinitely earning zero economic profit, and that is not a paradox.**

> [!note] Economies of scale, and where the U-shape comes from
> **Economies of scale** — long-run ATC falling with output — come from **specialisation**; **diseconomies** come from **coordination problems** as the organisation grows. **Constant returns lie between.**
>
> **This is a *long-run* phenomenon and distinct from §2's short-run U-shape**, which comes from spreading a fixed cost against diminishing marginal product. **The two are frequently conflated**: the short-run U exists because one input is fixed; the long-run U exists because organisations get harder to run.

## ✏️ Exercises

**1. (Costs.)** (a) Verify the cost relationships. (b) Why is ATC U-shaped? (c) Prove MC cuts ATC at its minimum and find the efficient scale.

> [!example]- Solution
> **(a) All of them hold.**
>
> *(Verified against Mankiw's Table 2 — **50 checks**, all passing:)*
>
> $$TC=FC+VC\qquad AFC=\frac{FC}{Q}\qquad AVC=\frac{VC}{Q}\qquad ATC=\frac{TC}{Q}=AFC+AVC$$
> $$MC=\frac{\Delta TC}{\Delta Q}=\frac{\Delta VC}{\Delta Q}$$
>
> **Note that MC can be computed from either TC or VC** — they differ by a constant, which differentiates away. **That is the same fact that makes §5 work.**
>
> **(b) Because it is the sum of a falling curve and a rising one.**
>
> - **AFC falls continuously** — a fixed \$3.00 spread over more units (3.00 → 0.30 across the table). *"Spreading the overhead."*
> - **AVC rises** — diminishing marginal product means each extra unit takes more input (0.30 → 1.20).
>
> **At low output the first effect dominates and ATC falls; at high output the second dominates and ATC rises.** The minimum is where they balance.
>
> **⚠️ The long-run U-shape is a different phenomenon** (§6): it comes from specialisation giving way to coordination problems, not from a fixed input. **Conflating them is common and wrong.**
>
> **(c) $\frac{d(ATC)}{dQ}=\frac{MC-ATC}{Q}$, and the efficient scale is $\sqrt{30}$.**
>
> $$\frac{d}{dQ}\!\left(\frac{TC}{Q}\right)=\frac{Q\cdot MC-TC}{Q^2}=\frac{MC-ATC}{Q}$$
>
> **Since $Q>0$, the sign of the derivative is the sign of $MC-ATC$.** So ATC falls while MC is below it, rises while MC is above it, and is stationary exactly where they meet. **That is the whole proof.**
>
> **⚠️ And it is not about costs.** Any average behaves this way: **it is dragged toward whatever the marginal value is.** A batting average, a grade average, a running mean — all identical.
>
> **For the efficient scale, Mankiw's table is not enough.** *(It ties at ATC = 1.30 for $Q=5$ and $Q=6$.)* **Recovering the cost function from the MC sequence — which increases by a constant 0.20, so $TC = 3+0.1Q^2+0.2Q$, verified to reproduce all 11 rows exactly — gives:**
>
> $$\frac{d(ATC)}{dQ}=-\frac{3}{Q^2}+0.1=0\;\Rightarrow\;Q^*=\sqrt{30}=\mathbf{5.4772},\qquad ATC=\mathbf{1.2954}$$
>
> **Below both tabulated values, and exactly between them.** **[[02 - Supply, Demand and Elasticity|Ch. 02]] met the same situation** — a discrete tie signalling an interior optimum — **so treat a tie as an instruction to solve the continuous problem.**

**2. (Hard — the firm's decisions.)** (a) Why $P = MC$? (b) Why is MC the supply curve? (c) Distinguish shutting down from exiting, and explain the sunk-cost logic. (d) Why is losing money sometimes correct?

> [!example]- Solution
> **(a) Because for a price taker, marginal revenue equals the price.**
>
> **The firm is small enough that it can sell any quantity at the market price, so each extra unit adds exactly $P$ to revenue.** Profit rises while $P > MC$ and falls while $P < MC$, so the maximum is at $P = MC$.
>
> **This is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 3 in its cleanest form** — set marginal benefit equal to marginal cost.
>
> **⚠️ The condition also requires MC to be *rising*.** Where MC slopes down, $P = MC$ locates a profit *minimum*. **Mankiw's diagram shows two intersections and only the upward-sloping one is the answer** — a second-order condition he states in words.
>
> **(b) Because the profit-maximising quantity at each price traces out MC exactly.**
>
> *(Computed: as $P$ goes \$0.80 → \$1.60 → \$2.40, the chosen $Q$ goes 3 → 7 → 11, which is precisely $MC^{-1}$.)*
>
> **A supply curve is nothing more than "quantity offered at each price", so the marginal-cost curve relabelled is the supply curve.**
>
> **This closes a loop from [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]**, which needed "the height of supply is the seller's cost" in order to define producer surplus **and simply asserted it.** Here it is derived. *(Strictly, supply is the part of MC above min AVC — below that the firm shuts down, per (c).)*
>
> **(c) They differ in whether the fixed cost is escapable.**
>
> | | fixed cost | rule |
> |---|---|---|
> | **shut down** (short run) | **sunk** — paid either way | $P < AVC$ |
> | **exit** (long run) | avoidable | $P < ATC$ |
>
> **In the short run the fixed cost is identical under both options — produce or not, you pay the rent — so it cannot distinguish between them.** Formally it is a constant in the objective function and **differentiates to zero.**
>
> **So the short-run comparison is revenue against *variable* cost only**, which gives $P < AVC$ as the shutdown rule.
>
> **In the long run the lease ends and the fixed cost becomes avoidable, so it re-enters the comparison** and the test becomes $P < ATC$.
>
> **⚠️ "Sunk" is not a property of a cost; it is a property of a cost *relative to a decision*.** The same \$3.00 is sunk for tonight's opening decision and not sunk for next year's lease renewal. **The test is never "is this cost large" but "does this cost differ between my options."**
>
> **(d) Because the alternative loses more.**
>
> *(Computed at $P=\$0.80$: producing loses **\$2.10**; shutting down loses the full fixed cost, **\$3.00**. Producing is better by **\$0.90**.)*
>
> **Between min AVC (\$0.20) and min ATC (\$1.2954) — a wide range — the firm makes a loss and should keep producing anyway**, because revenue is covering all the variable cost and contributing something toward the fixed cost that must be paid regardless.
>
> **"We're losing money, so we should stop" is the classic error**, and it is exactly the sunk-cost fallacy wearing the opposite costume: **the usual version continues a bad project because of money already spent; this version abandons a good one for the same reason.** Both mistakes come from letting an unavoidable cost enter a decision it cannot affect.
>
> **The everyday cases are all correct**: a restaurant staying open through a quiet January, a factory running below break-even in a recession, an airline flying a half-empty route. **Each covers its variable costs and contributes to overhead that is owed either way.**
>
> **And the decision reverses when the fixed cost becomes escapable** — which is why firms often continue for years and then exit abruptly when a lease expires.

**3. (Long run.)** (a) Why does profit go to zero? (b) What does zero profit mean? (c) What becomes true at once, and why does it matter?

> [!example]- Solution
> **(a) Because entry and exit are free, and both move the price toward min ATC.**
>
> *(Computed: at \$1.50 firms earn +1.2250 → entry → price falls. At \$1.10 they lose 0.9750 → exit → price rises. **Only \$1.2954 = min ATC is a resting point.**)*
>
> **Positive profit attracts entrants, which increases market supply and pushes the price down. Losses drive firms out, which reduces supply and pushes the price up.** The process stops only when profit is zero — **so the long-run price is pinned to the minimum of average total cost, and nothing else.**
>
> **Note what this means for the long-run market supply curve: it is horizontal at min ATC** (with identical firms). **The market supplies any quantity at that price**, because the quantity adjusts through the *number of firms* rather than through each firm's output.
>
> **(b) Earning exactly the normal return available elsewhere.**
>
> **Economic cost includes the opportunity cost of the owner's capital and time (§1), so those returns are already subtracted before "profit" is computed.** Zero economic profit therefore means the owner is doing exactly as well as their next-best alternative — **and accounting profit is positive.**
>
> **This is why firms persist indefinitely at "zero profit" without it being a paradox**, and why the term misleads almost everyone who meets it first in an accounting context.
>
> **It also explains why economic profit is the right signal for entry**: it measures whether resources are worth *more here than elsewhere*, which is exactly the allocation question.
>
> **(c) $P = MC = $ min $ATC$, and that is the efficiency claim made precise.**
>
> - **$P = MC$** — the firm maximises profit, so the value of the last unit to buyers equals its cost;
> - **$P = $ min $ATC$** — free entry has competed away profit;
> - **therefore every firm operates at its efficient scale** ($Q^*=\sqrt{30}$ here).
>
> **The good is produced at the lowest possible cost, and sold at that cost.**
>
> **This is what [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] meant by "competitive markets maximise total surplus", now derived rather than asserted** — ch. 03 established that trading where value exceeds cost maximises surplus; **this chapter shows that a competitive firm's own profit motive produces exactly that behaviour.**
>
> **And it sets up [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]] precisely.** Every step used **price taking**. A firm facing a downward-sloping demand curve has $MR < P$, so it sets $MR = MC$ and therefore **$P > MC$** — the source of the deadweight loss ch. 06 computes. **The competitive result is the benchmark against which market power is measured.**

## 📝 Summary

- **Economic cost includes implicit (opportunity) costs**, so **economic profit < accounting profit**. §6's zero-profit result is unintelligible without this.
- **Diminishing marginal product and rising marginal cost are the same fact from two sides** — and the same fact that bows [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s PPF outward.
- **Mankiw's Table 2 verified in full — 50 checks**, including $ATC=AFC+AVC$ at every quantity.
- **AFC falls, AVC rises, ATC is U-shaped** because it is their sum.
- **⚠️ The table ties at ATC = 1.30 for $Q=5$ and $Q=6$, and the tie signals an interior optimum.** *(Recovering $TC=3+0.1Q^2+0.2Q$ — verified to reproduce **all 11 rows** — gives $Q^*=\sqrt{30}=\mathbf{5.4772}$, $ATC=\mathbf{1.2954}$, below both.)* **[[02 - Supply, Demand and Elasticity|Ch. 02]] met the identical situation with total revenue.**
- **⚠️ $\dfrac{d(ATC)}{dQ}=\dfrac{MC-ATC}{Q}$ — one derivative proves MC cuts ATC at its minimum** *(verified: $MC=ATC=1.2954$ exactly at $Q^*$)*.
- **And it is a fact about averages, not costs**: any average is pulled toward the marginal value. **Your grade average falls exactly when the next test scores below it.**
- **A competitive firm produces where $P = MC$** (with MC rising — the downward-sloping intersection is a profit *minimum*).
- **⚠️ The marginal-cost curve *is* the supply curve** — which derives what [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] assumed when defining producer surplus.
- **⚠️ Shut down if $P < AVC$ (short run); exit if $P < ATC$ (long run).** The difference is whether the fixed cost is escapable.
- **⚠️ Between min AVC (\$0.20) and min ATC (\$1.2954) the firm loses money and should keep producing** *(computed: at \$0.80, producing loses \$2.10 against \$3.00 shut down — **saving \$0.90**)*.
- **"We're losing money, so we should stop" is the sunk-cost fallacy inverted.** The fixed cost is identical under both options, so it differentiates to zero. **"Sunk" is a property of a cost *relative to a decision*, not of the cost itself.**
- **Entry and exit drive economic profit to zero**, pinning the long-run price to **min ATC** and making long-run market supply horizontal.
- **⚠️ Zero economic profit means earning the normal return elsewhere** — accounting profit is positive, and firms persist indefinitely.
- **In long-run equilibrium $P = MC = $ min $ATC$ simultaneously** — the good is made at the lowest possible cost *and* sold at that cost. **That is ch. 03's efficiency claim, derived.**
- **Every step assumed price taking** — which is exactly what [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]] removes.

## ⚠️ Important Notes

1. **⚠️ Use economic cost, not accounting cost.** The owner's forgone salary and capital return are real costs.
2. **Diminishing marginal product ⇒ rising MC.** One phenomenon, two names.
3. **MC can be computed from TC or VC** — they differ by a constant.
4. **AFC always falls; AVC generally rises; ATC is U-shaped as their sum.**
5. **⚠️ A tie in a discrete table means the optimum lies between the grid points.** Solve the continuous problem. *(Second occurrence — see [[02 - Supply, Demand and Elasticity|ch. 02]].)*
6. **⚠️ $d(ATC)/dQ = (MC-ATC)/Q$** — the whole MC/ATC picture in one line.
7. **The average-marginal rule is arithmetic, not economics.** It applies to any average.
8. **⚠️ $P = MC$ requires MC to be *rising*.** The other intersection is a profit minimum.
9. **The MC curve above min AVC is the firm's supply curve.**
10. **⚠️ Shutdown compares $P$ to AVC; exit compares $P$ to ATC.** Using the wrong one is the classic error.
11. **⚠️ "Sunk" is relative to a decision, not intrinsic to a cost.** Ask whether the cost differs between the options.
12. **⚠️ Losing money can be correct.** Compare the loss from producing to the loss from stopping — not to zero.
13. **Firms often continue for years and exit abruptly** — because the fixed cost becomes escapable only at a lease boundary.
14. **⚠️ Zero economic profit ≠ zero accounting profit.** It means the normal return, and it is a stable state.
15. **Long-run market supply is horizontal at min ATC** with free entry and identical firms.
16. **Short-run and long-run U-shapes have different causes** — a fixed input versus organisational coordination. Do not conflate them.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters precisely** *(Micro 6e, PDF pp. 285–324 — ch. 13 pp. 285–304, ch. 14 pp. 305–324)*. **Per the deduplication rule in [[00-Index]], micro chapters 10–22 come from the Micro 6e volume.**
>
> **⚠️ TABLE 2 SURVIVED EXTRACTION COMPLETELY** — all eight columns and eleven rows, with every AFC, AVC, ATC and MC value intact. **This is the first Mankiw table in this subject to come through whole**, and it confirms the rule settled in [[Commercial Banking/contents/00-Index|Commercial Banking]]: **graphical exhibits are lost; numeric tables set as text survive.** *(All 50 internal checks pass.)*
>
> **⚠️ THE OPERATOR CIPHER applies to the prose formulas** — see [[00-Index]]. Nothing was transcribed.
>
> **⚠️ Every figure is lost, and two of them are central here.** **Figure 3 (Conrad's total-cost curve) and the cost-curve diagram showing MC cutting ATC and AVC at their minima are images**, as is Figure 2 (marginal cost as the supply curve) and the shutdown/exit graphics. What survives is captions and axis labels — *"Total Cost $15.00 14.00 13.00 …"* — **which look like data and are only tick marks.**
>
> **This is why §3 proves the MC/ATC result algebraically rather than describing the picture** — the algebra is both checkable and, arguably, clearer than the diagram it replaces.
>
> **No erratum.** Every value Mankiw tabulates reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §2's recovery of the continuous cost function is mine and is the chapter's main addition.** **Mankiw's table cannot locate the efficient scale — it ties at 1.30.** Noticing that the marginal costs form an arithmetic sequence gives $TC=3+0.1Q^2+0.2Q$, **which reproduces all 11 rows exactly** and yields $Q^*=\sqrt{30}$, $ATC=1.2954$. **The link to [[02 - Supply, Demand and Elasticity|ch. 02]]'s identical tie — and the general rule that a tie signals an interior optimum — is mine.**
> - **⚠️ §3's derivation $d(ATC)/dQ=(MC-ATC)/Q$ is mine.** **Mankiw tabulates the relationship and asserts it; he is deliberately calculus-free.** The observation that **this is a fact about averages rather than costs** — with the grade-average analogy — is the part that makes it stick.
> - **The identification of diminishing marginal product, rising MC and [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s bowed PPF as one phenomenon** is an addition.
> - **§4's note that $P=MC$ requires the *rising* branch** (a second-order condition) is stated in Mankiw's prose but not as a condition; making it explicit is mine.
> - **§5's framing that "sunk" is a property of a cost *relative to a decision*** — and that "we're losing money so we should stop" is the sunk-cost fallacy inverted — is mine. **Mankiw gives the shutdown rule and the farmer example without generalising the principle.**
> - **§6's observation that long-run market supply is horizontal because quantity adjusts through the *number of firms*** is an addition, as is the closing link to [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]: **every step used price taking, and removing it gives $MR<P$ and hence $P>MC$.**
> - **The warning that short-run and long-run U-shapes have different causes** is mine; Mankiw presents both without flagging the conflation.
>
> **Deliberately compressed.** **Mankiw ch. 13's Caroline's Cookie Factory example** is omitted — it makes the same points as Conrad's table, which extracted completely and is therefore verifiable. **The extended treatment of the production function and total-product curve** is compressed to §1's note, since the figures are lost and the analytical content is "diminishing marginal product ⇒ rising MC". **Ch. 14's derivation of the market supply curve with a fixed number of firms** is represented by §4's result plus §6's long-run discussion. **The case studies** (near-empty restaurants, mini-mills, the market for milk) illustrate §5's shutdown logic and are represented by it. **Economies of scale** are noted in §6 rather than developed; the long-run cost curve is a figure and is lost.

**Previous:** [[04 - Externalities, Public Goods and Common Resources]] · **Next:** [[06 - Monopoly, Oligopoly and Monopolistic Competition]]
