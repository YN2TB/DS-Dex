---
subject: Macroeconomics & Microeconomics
chapter: 4
tags: [ds, economics, microeconomics, externalities, coase, pigovian-tax, public-goods, commons]
source: "Mankiw, *Principles of Microeconomics* 6e, ch. 10–11"
---

# Externalities, Public Goods and Common Resources

**[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Chapter 03]] showed markets maximising total surplus. This chapter is about when they do not** — and every failure in it turns out to be a failure of **property rights**.

**Four results.**

**§2 — a corrective tax is the exact opposite of ch. 03's tax.** *(Computed: a tax equal to the external cost restores the social optimum with **zero** deadweight loss, and raises \$800 of revenue while doing it.)* **A tax is not inherently distorting; it is distorting only when the market was already right.**

**§3 — tradable permits beat a uniform mandate by 40%, and the saving is invariant to the target.** *(Computed algebraically: the cost ratio is $n^2/[\sum c_i \sum 1/c_i]$, **the target cancels**, and by Cauchy–Schwarz permits are **never** worse — the gain is exactly the *dispersion* of abatement costs.)*

**§4 — the Coase theorem, and the third appearance of one structure.** *(Verified on Mankiw's example: the dog stays or goes according to whether benefit exceeds cost, **whoever holds the legal right**; the right determines only who pays whom.)* **Efficiency is fixed by fundamentals; distribution is fixed by institutional detail; the two are independent** — exactly as in [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]] and [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]].

**§6 — the tragedy of the commons, computed.** *(One owner reaches the social optimum **exactly**; at 1,000 users the commons produces **0.4%** of what it could.)*

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]] for the operator cipher.

## 📘 Main Knowledge

### 1. Externalities: private cost is not social cost

**An externality is a cost or benefit falling on a bystander.** The decision-maker weighs only *their* costs and benefits, so the market quantity is wrong.

*(Computed — private value $P = 100-Q$, private cost $P = Q$, plus a \$20 external cost per unit:)*

| | condition | quantity |
|---|---|---|
| **market** | private value = **private** cost | **50** |
| **social optimum** | private value = **social** cost | **40** |

$$\text{deadweight loss}=\tfrac12\times10\times20=\mathbf{100}$$

> [!note] The efficient level of pollution is not zero
> **The optimum is where marginal value equals marginal *social* cost — which is a positive quantity.** On every unit between 40 and 50 the social cost exceeds the buyer's value, and those units get made anyway **because the person deciding does not pay the whole cost.**
>
> **But below 40, the good is worth more than it costs society, pollution included.** *"Eliminate the externality"* is not the efficient goal, and Mankiw is explicit about it. **Zero pollution would require zero production.**

**Negative externalities** (pollution, congestion) ⇒ the market produces **too much**.
**Positive externalities** (research, vaccination, education) ⇒ the market produces **too little**, and the corrective policy is a **subsidy**.

### 2. ⚠️ The corrective (Pigovian) tax — the opposite of ch. 03's tax

*(Computed:)*

| tax | quantity | deadweight loss |
|---|---|---|
| \$0 | 50 | **100** |
| \$10 | 45 | 25 |
| **\$20 = external cost** | **40** | **0** |
| \$30 | 35 | 25 |

**A tax equal to the external cost makes the decision-maker face the social cost.** The externality is **internalised** and the market then finds the right quantity by itself.

> [!warning] A tax is not inherently distorting
> **[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Ch. 03]] computed that a tax on an efficient market *creates* deadweight loss** — $\tfrac12 t^2\frac{bc}{b+c}$, growing with the square of the rate. **Here a tax on an *inefficient* market *removes* it.**
>
> **Same instrument, opposite sign, and the difference is entirely whether the market was right to begin with.**
>
> **And note the corrective tax raises revenue while improving efficiency** *(computed: \$20 × 40 = **\$800**)*. **That is the "double dividend"** and it is why economists are so much more enthusiastic about carbon taxes than about taxes in general — **it is the one tax whose deadweight loss is negative.**
>
> **Over-correcting is also costly**: a \$30 tax produces the same DWL as no tax at \$10 too little. **The target is the external cost, not the maximum feasible tax.**

### 3. ⚠️ Permits versus a uniform mandate

**Three firms with different abatement costs, target: cut emissions by 90 units.** *(Computed — marginal abatement cost $=c_i\times$ units abated:)*

**(a) Uniform mandate — each cuts 30:**

| firm | $c_i$ | abates | cost |
|---|---|---|---|
| A (modern) | 2 | 30 | 900 |
| B (average) | 6 | 30 | 2 700 |
| C (old) | 12 | 30 | 5 400 |
| | | **90** | **9 000** |

**(b) Tradable permits — each abates until marginal cost = permit price:**

| firm | abates | cost |
|---|---|---|
| A | **60.00** | 3 600 |
| B | 20.00 | 1 200 |
| C | **10.00** | 600 |
| | **90** | **5 400** |

**Permit price settles at \$120. Saving: 3 600 — 40% cheaper for the same environmental result.**

> [!warning] The saving does not depend on the target
> $$\text{mandate}=\frac{T^2}{2n^2}\sum c_i \qquad \text{permits}=\frac{T^2}{2\sum 1/c_i} \qquad \text{ratio}=\frac{n^2}{\sum c_i\sum 1/c_i}$$
>
> **$T$ cancels.** *(Verified at targets of 30, 90 and 150 — the saving is **40.0%** in every case.)*
>
> **And by Cauchy–Schwarz, $\sum c_i\sum 1/c_i \ge n^2$ always, with equality only if every $c_i$ is identical.** So **permits are never worse than a mandate**, and **the gain is exactly the dispersion of abatement costs.** A uniform mandate is optimal only when firms are alike — which they never are.
>
> **The efficiency condition is that *marginal* abatement costs are equalised across firms.** A single price does that automatically; a uniform quantity rule cannot do it at all, because it forces the expensive abater to do as much as the cheap one.

> [!note] A tax and a permit system are the same thing from two sides
> **The tax fixes the *price* of emitting and lets the quantity adjust. Permits fix the *quantity* and let the price adjust.** In a world of certainty they are identical.
>
> **They differ only in which uncertainty you face.** If abatement costs turn out higher than expected: a **tax** gives you less abatement than planned but caps the cost; **permits** give you the abatement you wanted at a price that can spike. **Choose according to which error is worse** — and that is the whole carbon-tax versus cap-and-trade debate in one line.

### 4. ⚠️ The Coase theorem

> **If private parties can bargain over the allocation of resources at no cost, the private market will solve the problem of externalities and allocate resources efficiently.**

*(Verified on Mankiw's example — Dick's dog barks and disturbs Jane:)*

| Dick's benefit | Jane's cost | efficient outcome | what happens |
|---|---|---|---|
| \$500 | \$800 | **remove the dog** | Jane offers \$600; Dick accepts. **Both better off.** ✓ |
| \$1 000 | \$800 | **keep the dog** | Dick needs > \$1 000, Jane offers ≤ \$800 → **no deal**, and that *is* efficient ✓ |

**Now switch the legal right to Jane** *(computed across four cases)*:

| Dick's benefit | Jane's cost | right to **Dick** | right to **Jane** | same? |
|---|---|---|---|---|
| \$500 | \$800 | removes dog | removes dog | **yes** |
| \$1 000 | \$800 | keeps dog | keeps dog | **yes** |
| \$900 | \$800 | keeps dog | keeps dog | **yes** |
| \$700 | \$800 | removes dog | removes dog | **yes** |

> [!warning] The allocation is the same either way. Only who pays whom changes.
> **If Dick holds the right, Jane pays him to remove the dog. If Jane holds it, Dick pays her to keep it.** The dog stays or goes according to whether benefit exceeds cost, **and nothing else.**
>
> **The initial distribution of rights is not irrelevant — it determines the distribution of well-being.** It just does not determine the *allocation*.

> [!warning] ⚠️ The third appearance of one structure
> | chapter | what fixes the **allocation** | what fixes the **split** |
> |---|---|---|
> | [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage\|01]] | comparative advantage — *whether* there are gains and *who* specialises | **the price** *(total gain constant at 10 oz across the whole range)* |
> | [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade\|03]] | the tax **wedge** — quantity and both prices *(the statute is irrelevant)* | **relative elasticities**, $\eta_s/(\eta_s+\eta_d)$ |
> | **04** | **benefit vs cost** — the dog stays iff benefit > cost | **the property right** |
>
> **One principle: efficiency is determined by the fundamentals — costs, values, elasticities. Distribution is determined by the institutional detail — the price, the statute, the property right. And the two are independent.**
>
> **Which is why so many policy arguments are really about distribution while being conducted entirely in the language of efficiency.** Recognising that is worth more than any single result in these four chapters.

**Why private bargaining fails in practice** — Mankiw's list, and it is the point rather than a caveat:

- **transaction costs** — lawyers, time, enforcement;
- **bargaining failure** — each side holds out for a better split *(and §4's table shows why: the efficient outcome is fixed, so the entire negotiation is about the split)*;
- **⚠️ coordination** — with many parties, agreement is impossible.

> [!note] Coase is not an argument that government is unnecessary
> **The third failure is the one that matters.** Two neighbours can bargain; **ten thousand downwind residents and forty power stations cannot.** And that is precisely the case where externalities are large.
>
> **So Coase reframes the question rather than answering it: the relevant variable is transaction costs.** Where bargaining is cheap, **assign rights clearly and let the parties trade** — which is exactly what §3's tradable permits do. Where it is not, **regulate or tax.**
>
> **Read that way, §3 and §4 are the same idea**: permits are a Coasean solution installed by statute, creating a market where transaction costs had prevented one.

### 5. The four types of goods

| | **excludable** | **not excludable** |
|---|---|---|
| **rival** | **private goods** — ice cream, clothing | **⚠️ common resources** — fish, congested roads |
| **not rival** | **club goods** — cable TV, uncrowded toll roads | **⚠️ public goods** — national defence, basic research |

**Excludable** = you can stop non-payers from using it. **Rival** = one person's use reduces what is left for others.

> [!warning] The two failures are the two non-excludable boxes, and they fail in opposite directions
> | | problem | result |
> |---|---|---|
> | **public goods** | **free riding** — everyone benefits whether they pay or not | **too little** is provided |
> | **common resources** | **overuse** — everyone bears only a fraction of the cost | **too much** is consumed |
>
> **Both are failures of property rights**, which is why Mankiw pairs them in one chapter and titles his conclusion *"The Importance of Property Rights."*
>
> **A public good's central difficulty is that the efficient quantity requires knowing everyone's willingness to pay — and nobody has any incentive to report it honestly.** The free-rider problem is therefore not merely a funding problem; **it is an information problem**, which is why cost–benefit analysis for public goods is genuinely hard rather than merely tedious.

### 6. ⚠️ The tragedy of the commons, computed

**$N$ herders share a pasture. Value per cow $=100-Q$ (falling as the total herd $Q$ grows); cost per cow $=20$.**

**Social optimum:** maximise $Q(100-Q)-20Q$, giving $Q^*=\mathbf{40}$ and total surplus **1600**.

**Each herder instead maximises their own return, taking the others' herds as given** — so each ignores the damage their extra cow does to everyone else. *(Symmetric equilibrium: $q=(100-20)/(N+1)$.)*

| $N$ | each adds | **total herd** | surplus per cow | **total surplus** | vs optimum |
|---|---|---|---|---|---|
| **1** | 40.000 | **40.000** | 40.000 | **1600.00** | **100.0%** |
| 2 | 26.667 | 53.333 | 26.667 | 1422.22 | 88.9% |
| 4 | 16.000 | 64.000 | 16.000 | 1024.00 | 64.0% |
| 10 | 7.273 | 72.727 | 7.273 | 528.93 | 33.1% |
| 50 | 1.569 | 78.431 | 1.569 | 123.03 | 7.7% |
| **1000** | 0.080 | **79.920** | 0.080 | **6.39** | **0.4%** |

> [!warning] One owner reaches the social optimum exactly; a thousand destroy 99.6% of the value
> **At $N=1$ the herder *is* society** — he bears the full cost of degrading his own pasture, so he chooses $Q=40$ and captures the whole 1600. **Private ownership internalises the externality automatically.**
>
> **As $N$ grows the herd expands toward 80** — the point where value minus cost is zero and **the last cow is worth exactly nothing** — and the surplus collapses.
>
> **The mechanism: each herder receives the *full* value of his own extra cow but bears only $1/N$ of the degradation it causes.** The externality he ignores is $\frac{N-1}{N}$ of the damage, which approaches 100% as $N$ grows.
>
> **This is an $N$-player prisoners' dilemma** ([[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]) and the same individually-rational / collectively-disastrous gap as [[02 - Supply, Demand and Elasticity|ch. 02]]'s farmers.
>
> **Every remedy re-creates excludability**: private ownership, grazing permits, fishing quotas, congestion charges, or a tax. **Note that §3's tradable permits solve *both* of this chapter's failures with one mechanism** — which is why they are the workhorse instrument of environmental policy.

## ✏️ Exercises

**1. (Externalities and remedies.)** (a) Why does the market get the quantity wrong? (b) What tax fixes it, and how does it relate to ch. 03's tax? (c) Why do permits beat a mandate?

> [!example]- Solution
> **(a) Because the decision-maker does not face the whole cost.**
>
> *(Computed: with a \$20 external cost, the market produces **50** where the optimum is **40**, and the deadweight loss is **100**.)*
>
> **On every unit between 40 and 50, the social cost exceeds the buyer's value** — those trades destroy value and happen anyway, because the bystander's loss appears in nobody's calculation.
>
> **⚠️ But the optimum is not zero.** Below 40 the good is worth more than it costs society, pollution included. **The efficient quantity of a negative externality is positive**, and treating "eliminate it" as the goal gets the answer as wrong in one direction as ignoring it does in the other.
>
> *(Positive externalities are the mirror image: too little is produced, and the remedy is a subsidy. Research and vaccination are the standard cases.)*
>
> **(b) A tax equal to the external cost — and it is ch. 03's tax with the sign reversed.**
>
> *(Computed: \$20 tax → $Q=40$, **DWL = 0**; \$10 → DWL 25; \$30 → DWL 25.)*
>
> **The tax makes the private cost equal the social cost.** Then the ordinary market mechanism — which [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] showed maximises surplus — produces the right answer, because it is now maximising the *right* surplus.
>
> **The contrast with ch. 03 is the point:**
>
> | | ch. 03 | ch. 04 |
> |---|---|---|
> | market before the tax | **efficient** | **inefficient** |
> | effect of the tax | **creates** DWL, $\tfrac12t^2\frac{bc}{b+c}$ | **removes** DWL |
> | revenue | raised at a cost | raised **and** efficiency improved |
>
> **So "taxes distort" is true only of taxes on markets that were already right.** *(Computed: the corrective tax raises **\$800** while eliminating the loss — the "double dividend", and the reason a carbon tax is a different animal from a sales tax.)*
>
> **And over-correcting is symmetric**: \$30 costs exactly as much as \$10 was insufficient. **The target is the external cost, not the largest defensible number.**
>
> **(c) Because permits equalise *marginal* abatement costs and a mandate cannot.**
>
> *(Computed: mandate **9 000**, permits **5 400** — a **40%** saving for identical abatement. The cheap abater does 60 units, the expensive one 10.)*
>
> **The mandate forces the firm with a \$12 cost to abate as much as the firm with a \$2 cost.** Permits let the cheap abater do more and sell the difference — **both firms gain, and the environment gets the same result.**
>
> **⚠️ And the saving is invariant to the target** *(verified at 30, 90 and 150 — **40.0%** every time)*:
>
> $$\text{ratio}=\frac{n^2}{\sum c_i\sum 1/c_i}$$
>
> **$T$ cancels entirely.** By **Cauchy–Schwarz** $\sum c_i\sum 1/c_i\ge n^2$, so **permits are never worse**, with equality only when all firms are identical.
>
> **The gain is precisely the dispersion of abatement costs** — which means the case for tradability is strongest exactly where firms differ most, and that is the usual situation.

**2. (Hard — Coase.)** (a) State and verify the theorem. (b) What does the assignment of rights change? (c) Why does bargaining fail? (d) What is the wider pattern?

> [!example]- Solution
> **(a) With costless bargaining, private parties reach the efficient allocation on their own.**
>
> *(Verified on both of Mankiw's cases:)*
>
> - **Benefit \$500, cost \$800** — efficient to remove the dog. Any payment between \$500 and \$800 works; Mankiw's \$600 leaves **both** better off. ✓
> - **Benefit \$1 000, cost \$800** — efficient to keep it. Dick needs more than \$1 000 and Jane will not offer above \$800, **so no deal** — and the *absence* of a deal is the efficient outcome. ✓
>
> **The second case is the more instructive one.** A failed negotiation is not a market failure here; **it is the market correctly declining to make a change that would destroy value.**
>
> **(b) Who pays whom — and nothing else.**
>
> *(Computed across four benefit/cost pairs: the outcome is identical whether Dick or Jane holds the right, in every case.)*
>
> **If Dick has the right to keep a barking dog, Jane must buy him out. If Jane has the right to quiet, Dick must buy her off.** Either way the dog stays exactly when benefit exceeds cost.
>
> **The rights assignment is far from irrelevant — it determines the distribution of well-being.** It simply does not determine the allocation. **Those are two different questions, and Coase separates them cleanly.**
>
> **(c) Transaction costs, hold-out, and — decisively — numbers.**
>
> - **Transaction costs**: lawyers, drafting, monitoring, enforcement. If these exceed the gain, no deal is worth doing.
> - **Bargaining failure**: since the efficient outcome is fixed, **the entire negotiation is about the split** — so both sides have an incentive to hold out, and holding out sometimes kills a deal that should have happened.
> - **⚠️ Coordination**: two neighbours can bargain. **Ten thousand downwind residents and forty power stations cannot** — and that is exactly where externalities are largest.
>
> **So Coase does not show that government is unnecessary. It shows that the relevant variable is transaction costs.**
>
> **Where bargaining is cheap: assign rights clearly and let people trade.** Where it is not: **tax or regulate.** *(And §3's permits are a Coasean solution installed by statute — a market created where transaction costs had prevented one. Read that way, §3 and §4 are one idea.)*
>
> **(d) Efficiency and distribution are determined by different things, and this is the third time.**
>
> | chapter | fixes the **allocation** | fixes the **split** |
> |---|---|---|
> | [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage\|01]] | comparative advantage | the price |
> | [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade\|03]] | the tax wedge *(not the statute)* | relative elasticities |
> | **04** | benefit vs cost | the property right |
>
> **In each case the efficient outcome is pinned down by fundamentals, and an institutional variable — price, statute, right — moves surplus between parties without changing what happens.**
>
> **Two things follow.**
>
> **First, a practical one: when analysing a policy, separate the two questions before arguing.** *"Does this change what gets produced?"* and *"Does this change who gets it?"* have different answers and different evidence.
>
> **Second, and more useful: many policy debates conducted in the language of efficiency are really about distribution.** Arguing about who should hold a right, or who should remit a tax, is arguing about the split — **and the efficiency claims deployed on both sides are frequently beside the point.** [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Ch. 03]] made the same observation about tariffs, where the gains are concentrated and the losses diffuse.

**3. (Public goods and commons.)** (a) Classify goods and say why two boxes fail. (b) Compute the tragedy of the commons. (c) What fixes it?

> [!example]- Solution
> **(a) Two dimensions — excludability and rivalry — and the failures are the non-excludable boxes.**
>
> | | excludable | **not excludable** |
> |---|---|---|
> | **rival** | private goods | **common resources** |
> | not rival | club goods | **public goods** |
>
> **Excludability is what makes a market possible at all**: if you cannot stop non-payers, you cannot charge, and no private firm will supply.
>
> **The two failures run in opposite directions:**
> - **Public goods → free riding → too little.** Everyone benefits whether they pay or not, so nobody pays.
> - **Common resources → overuse → too much.** Everyone bears only a fraction of the cost of their own use.
>
> **The public-good problem is also an information problem**, which is the part usually missed. **The efficient quantity depends on the sum of everyone's willingness to pay, and nobody has any incentive to state theirs honestly** — understate it if you will be charged, overstate it if you will not. **So cost–benefit analysis for public goods is hard in principle, not merely in practice.**
>
> **(b) One owner is efficient; many owners destroy nearly everything.**
>
> *(Computed — social optimum $Q^*=40$ with surplus **1600**:)*
>
> | $N$ | total herd | total surplus | vs optimum |
> |---|---|---|---|
> | **1** | 40.0 | **1600.00** | **100.0%** |
> | 4 | 64.0 | 1024.00 | 64.0% |
> | 10 | 72.7 | 528.93 | 33.1% |
> | **1000** | **79.9** | **6.39** | **0.4%** |
>
> **At $N=1$ the herder is society and reaches the optimum exactly.** As $N$ grows the herd expands toward **80** — where the marginal cow is worth exactly nothing — and the surplus vanishes.
>
> **The mechanism, stated precisely: each herder captures the full value of his extra cow and bears only $1/N$ of the degradation.** The externality he ignores is $\frac{N-1}{N}$ of the damage. **At $N=2$ he ignores half of it; at $N=1000$, 99.9%.**
>
> **This is an $N$-player prisoners' dilemma.** Every herder would be better off if all restrained themselves, and each is individually better off not restraining — **the same structure as [[02 - Supply, Demand and Elasticity|ch. 02]]'s farmers, who collectively want less output and individually want more.**
>
> **(c) Anything that re-creates excludability.**
>
> | remedy | mechanism |
> |---|---|
> | **private ownership** | makes $N=1$ — the sole owner internalises everything |
> | **quotas / permits** | caps total use and (if tradable) allocates it efficiently |
> | **corrective tax / congestion charge** | makes each user face the marginal social cost |
> | **regulation** | crude, but works where the others are unenforceable |
>
> **The unifying observation: all four are property-rights solutions.** Mankiw closes the chapter with exactly this point, and it is why he pairs public goods and common resources — **both are what happens when nobody owns the thing.**
>
> **And note §3's permits appear again here.** Tradable permits fix the pollution externality *and* the commons problem with one instrument, because both are "too much of something nobody owns." **That is why permits are the workhorse of environmental policy rather than a special case.**
>
> *(The honest limitation: assigning ownership is not always possible or acceptable. You cannot privatise the atmosphere, and privatising fisheries or water raises distributional questions §4 shows the efficiency analysis is silent about.)*

## 📝 Summary

- **An externality is a cost or benefit falling on a bystander**, so the private calculation omits it. *(Computed: a \$20 external cost makes the market produce **50** where **40** is optimal, with DWL **100**.)*
- **⚠️ The efficient level of a negative externality is positive, not zero.** Below the optimum the good is worth more than it costs society.
- **Negative externality → overproduction → tax. Positive externality → underproduction → subsidy.**
- **⚠️ A corrective tax equal to the external cost restores the optimum exactly** *(computed: DWL **0** at $t=\$20$, and **25** at either \$10 or \$30 — over-correcting costs as much as under-correcting)*.
- **⚠️ This is ch. 03's tax with the sign reversed.** There a tax on an efficient market **created** DWL ($\tfrac12t^2\frac{bc}{b+c}$); here a tax on an inefficient one **removes** it. **A tax distorts only when the market was already right.**
- **The corrective tax raises revenue *while* improving efficiency** *(\$800)* — the "double dividend".
- **⚠️ Tradable permits beat a uniform mandate by 40%** *(computed: 9 000 vs 5 400 for identical abatement)*, because they **equalise marginal abatement costs** and a quantity rule cannot.
- **⚠️ And the saving is invariant to the target** — the ratio is $n^2/[\sum c_i\sum 1/c_i]$ and **$T$ cancels** *(verified at 30, 90, 150)*. **By Cauchy–Schwarz permits are never worse; the gain is exactly the dispersion of abatement costs.**
- **A tax and a permit system are the same instrument from two sides** — the tax fixes the price, permits fix the quantity. **The choice is about which uncertainty you fear**, which is the whole carbon-tax vs cap-and-trade debate.
- **⚠️ The Coase theorem: with costless bargaining, private parties reach the efficient allocation** *(verified on both of Mankiw's cases, including the one where **no deal** is the efficient outcome)*.
- **⚠️ The allocation is identical whoever holds the legal right** *(verified across four cases)*; **the right determines only who pays whom.**
- **⚠️ Third appearance of one structure: efficiency is fixed by fundamentals, distribution by institutional detail, and the two are independent** — [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]] (price), [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] (statute/elasticities), ch. 04 (property right). **Many efficiency arguments are really distributional arguments.**
- **Bargaining fails from transaction costs, hold-out, and above all *numbers*** — and the many-party case is exactly where externalities are largest. **So Coase reframes the question as one about transaction costs; §3's permits are a Coasean market installed by statute.**
- **Four goods: excludable × rival.** The two **non-excludable** boxes fail, in **opposite directions** — public goods are **underprovided** (free riding), common resources **overused**.
- **The free-rider problem is an information problem**: the efficient quantity needs everyone's willingness to pay, and nobody will report it honestly.
- **⚠️ Tragedy of the commons, computed: one owner reaches the optimum exactly (1600); at $N=1000$ the commons yields 6.39 — 0.4% of what it could.** The herd expands toward 80, where the last cow is worth nothing.
- **Each user captures the full value of his own use and bears $1/N$ of the damage** — ignoring $\frac{N-1}{N}$ of it. **An $N$-player prisoners' dilemma.**
- **Every remedy re-creates excludability**, and **tradable permits solve both of this chapter's failures with one mechanism.**

## ⚠️ Important Notes

1. **⚠️ The efficient quantity of pollution is not zero.** Set marginal value equal to marginal *social* cost.
2. **Positive externalities need subsidies, not taxes.** Check the sign before prescribing.
3. **⚠️ Set the corrective tax equal to the external cost** — over-correcting is symmetric with under-correcting.
4. **⚠️ "Taxes distort" applies only to markets that were efficient already.** A Pigovian tax has negative deadweight loss.
5. **A corrective tax raises revenue and improves efficiency simultaneously** — genuinely unusual.
6. **⚠️ Permits equalise marginal abatement costs; mandates equalise quantities.** Only the first is efficient.
7. **⚠️ The permit advantage is invariant to the target and equals the dispersion of costs** ($n^2/[\sum c\sum 1/c]$, Cauchy–Schwarz).
8. **Tax = fix the price; permits = fix the quantity.** Identical under certainty; the choice is about which uncertainty bites.
9. **⚠️ Under Coase the allocation is independent of who holds the right.** Only the distribution moves.
10. **A failed negotiation can be the efficient outcome** — the second Mankiw case.
11. **⚠️ Coase's binding constraint is transaction costs, and the killer is *many parties*.** Two neighbours bargain; ten thousand residents cannot.
12. **⚠️ Separate "what gets produced" from "who gets it" before arguing.** Many efficiency debates are distributional.
13. **Excludability is what makes a market possible.** Non-excludable goods fail in one of two opposite ways.
14. **The free-rider problem is an information problem**, not only a funding one.
15. **⚠️ In a commons, each user ignores $\frac{N-1}{N}$ of the damage.** The gap grows with $N$, and full dissipation is the limit.
16. **All commons remedies re-create excludability**, and permits address both failures at once.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters precisely** *(Micro 6e, PDF pp. 221–258 — ch. 10 pp. 221–242, ch. 11 pp. 243–258)*. **Per the deduplication rule in [[00-Index]], micro chapters 10–22 come from the Micro 6e volume**, which is the only book containing them.
>
> **⚠️ THE OPERATOR CIPHER applies** — see [[00-Index]]. This chapter is comparatively light on formulas, so the exposure is smaller than [[02 - Supply, Demand and Elasticity|ch. 02]]'s, but **nothing was transcribed.** **Mankiw's Coase figures reproduce exactly** — the \$500/\$800 and \$1,000/\$800 cases, and the \$600 payment.
>
> **⚠️ Every figure is lost.** Mankiw's externality analysis is conducted in diagrams — **the social-cost curve above the supply curve, the shaded deadweight-loss triangle, and the permit-market supply-and-demand panel are all images.** What survives is captions and stray axis labels.
>
> **So every area and quantity here is computed from an explicitly stated linear market** ($P=100-Q$, $P=Q$, \$20 external cost) rather than read off a diagram. **The market, the three firms' abatement costs and the commons parameters are mine; the definitions, the Coase example and the qualitative results are Mankiw's.**
>
> **No erratum.** Every result the prose states reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §3's permit-versus-mandate calculation is mine.** **Mankiw argues that tradable permits are more efficient and never computes it.** The 40% saving, the **invariance of the saving to the target** ($T$ cancels), and the **Cauchy–Schwarz argument that permits are never worse — with the gain equal to the dispersion of abatement costs** — are all additions, and the last two are the parts that make the result general rather than anecdotal.
> - **⚠️ §2's contrast with [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]** — the same instrument creating deadweight loss in one chapter and removing it in the next — **is my cross-chapter link**, as is the observation that over-correcting is symmetric with under-correcting.
> - **⚠️ §4's identification of the third appearance of the efficiency/distribution structure is mine and is the chapter's most valuable content.** Mankiw notes that the rights assignment does not affect the allocation; **he does not connect it to the price indeterminacy of ch. 01 or the statutory irrelevance of ch. 03.** The generalisation — *efficiency is fixed by fundamentals, distribution by institutional detail, and the two are independent* — is the addition.
> - **The reading of §3's permits as "a Coasean market installed by statute"**, making §§3–4 one idea rather than two, is mine.
> - **⚠️ §6's computation of the tragedy of the commons is mine.** **Mankiw tells the story qualitatively and gives no model.** The $N$-player Nash equilibrium, the finding that **$N=1$ reaches the social optimum exactly**, the collapse to **0.4%** at $N=1000$, and the statement that each user ignores $\frac{N-1}{N}$ of the damage, are additions.
> - **The observation that the free-rider problem is an *information* problem** — the efficient quantity requires truthful willingness-to-pay that nobody will supply — is an addition.
> - **The note that tradable permits solve both of the chapter's failures with one mechanism** is mine.
>
> **Deliberately compressed.** **Mankiw ch. 10's case studies and FYI boxes** (the ethanol subsidy debate, gasoline-tax discussion, and the various regulatory examples) are represented by the analytical content. **The extended treatment of command-and-control regulation versus market-based policy** is condensed into §3, which quantifies the comparison the prose makes. **Ch. 11's cost–benefit analysis section** — including the value-of-a-life discussion — is noted in §5's information point rather than treated separately; it is genuinely important and belongs with public-policy material rather than the price-theory core. **The "Are Lighthouses Public Goods?" and congestion case studies** illustrate §5's taxonomy and are not reproduced. **[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Ch. 03]] already owns the surplus and deadweight-loss machinery**, so it is used here rather than re-derived. **Micro ch. 12 (The Design of the Tax System) is excluded from this subject's scope** — see [[00-Index]]'s omissions table.

**Previous:** [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade]] · **Next:** [[05 - Production Costs and Competitive Markets]]
