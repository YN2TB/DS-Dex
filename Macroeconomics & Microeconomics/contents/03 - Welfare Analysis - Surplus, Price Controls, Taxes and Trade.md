---
subject: Macroeconomics & Microeconomics
chapter: 3
tags: [ds, economics, microeconomics, surplus, deadweight-loss, tax-incidence, laffer, tariffs]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 6–9"
---

# Welfare Analysis: Surplus, Price Controls, Taxes and Trade

**This chapter builds the toolkit the rest of microeconomics reuses.** Consumer and producer surplus turn "the market allocates efficiently" from a slogan into an area you can measure, and **deadweight loss** turns "this policy is costly" into a number.

**Four results, and all four are one calculation.**

**§4 — who legally pays a tax is irrelevant.** *(Computed: levying \$20 on sellers and levying it on buyers give **identical** prices and quantities.)* The law says who writes the cheque; it cannot say who bears the cost.

**§4b — the burden falls on whoever cannot escape.** *(Computed: buyers bear **50% / 75% / 90%** as demand becomes progressively more inelastic, and the share is exactly $\eta_s/(\eta_s+\eta_d)$ in every case.)*

**§5 — deadweight loss grows with the *square* of the tax.** Mankiw argues this geometrically; *(computed algebraically: $DWL = \tfrac12 t^2\,\frac{bc}{b+c}$, and $DWL/t^2$ is **constant at 0.2500** across every tax from \$10 to \$80)*.

**§6 — the Laffer curve, which Mankiw draws and never locates.** *(Computed: revenue peaks at $t^*=\$50$, where **deadweight loss is 50% of the revenue raised** — and the cost per dollar collected passes 1.0 *before* the peak.)*

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]] for the operator cipher.

## 📘 Main Knowledge

### 1. Consumer and producer surplus

| | definition | area |
|---|---|---|
| **consumer surplus** | willingness to pay − price paid | under demand, **above** price |
| **producer surplus** | price received − cost | above supply, **below** price |

*(Computed on $Q_d = 100-P$, $Q_s = P$ — equilibrium $P^*=\$50$, $Q^*=50$:)*

$$CS=\tfrac12\times50\times(100-50)=\mathbf{1250}\qquad PS=\tfrac12\times50\times50=\mathbf{1250}$$
$$\textbf{total surplus}=\mathbf{2500}$$

> [!note] The curves are sorted schedules, and that is the whole efficiency argument
> **The *height* of the demand curve at quantity $Q$ is the willingness to pay of the $Q$th buyer**, and the height of supply is the $Q$th seller's cost. **So demand is a list of valuations sorted high-to-low and supply is a list of costs sorted low-to-high.**
>
> **Efficiency then follows immediately**: the market gives the good to the buyers who value it most, produces it with the sellers who make it cheapest, and trades **every** unit whose value exceeds its cost and **no** unit where it does not.
>
> **That is all "markets are efficient" means** — and §2 is careful about what it does *not* mean.

*(Verified — total surplus at various quantities, computed unit by unit:)*

| quantity | total surplus |
|---|---|
| 30 | 2100 |
| 40 | 2400 |
| **50** | **2500 — maximum** |
| 60 | 2400 |
| 70 | 2100 |

**Below $Q^*$, units whose value exceeds cost go untraded. Above it, units are made whose cost exceeds their value.** Both are losses, which is why the equilibrium is the peak.

> [!warning] What efficiency does *not* mean
> **Total surplus adds a rich person's dollar to a poor person's dollar.** An allocation can maximise surplus and be grotesquely unequal — **efficiency is silent on distribution**, which is Principle 1's trade-off from [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]].
>
> **And it assumes the demand curve measures true value** — which fails when buyers are misinformed, and when there are [[04 - Externalities, Public Goods and Common Resources|externalities]] (ch. 04's whole subject).

### 2. Price controls

*(Computed on the same market:)*

| policy | $Q_d$ | $Q_s$ | result | **units traded** | **deadweight loss** |
|---|---|---|---|---|---|
| **ceiling** at \$30 | 70 | 30 | **shortage** of 40 | 30 | **400** |
| **floor** at \$70 | 30 | 70 | **surplus** of 40 | 30 | **400** |

> [!note] The short side of the market always decides
> **A binding control reduces the quantity traded whichever way it binds.** A ceiling makes sellers unwilling; a floor makes buyers unwilling. **Nobody is forced to trade, so the smaller of $Q_d$ and $Q_s$ is what happens.**
>
> **The deadweight loss is the value of the trades that no longer occur.**
>
> **But note what the model does not say.** A ceiling still transfers surplus **to the buyers who are served** — they get the good below its market price. **"Inefficient" is not "nobody gains", and that is exactly why price controls are politically durable**: the winners are identifiable and the losers are the people who could not buy at all.
>
> **A shortage also means non-price rationing appears** — queues, waiting lists, discrimination by the seller. **Those are real costs the triangle does not capture**, so 400 is a lower bound.

### 3. Taxes and deadweight loss

**A tax drives a *wedge* between the price buyers pay and the price sellers receive.** The quantity falls, and the surplus lost exceeds the revenue raised — **the excess is the deadweight loss.**

$$\text{DWL}=\tfrac12\times t\times \Delta Q$$

### 4. ⚠️ Who pays the tax does not depend on who pays it

*(Computed — a \$20 tax, worked both ways:)*

| levied on | buyers pay | sellers keep | quantity |
|---|---|---|---|
| **sellers** | \$60 | \$40 | 40 |
| **buyers** | \$60 | \$40 | 40 |

**Identical. ✓**

> [!warning] The law names who writes the cheque and cannot name who bears the cost
> **The price adjusts until the market clears, and the price is what allocates the burden.** Legislating that sellers remit the tax simply shifts the supply curve; legislating that buyers remit it shifts the demand curve; **the wedge, the quantity and both effective prices come out the same.**
>
> **This is the most useful single result in the chapter.** It is why *"your employer pays half your payroll tax"* is an accounting statement with no economic content — **the split is determined by §4b, not by the statute.**

### 4b. ⚠️ What *does* determine the split: relative elasticities only

$$\text{buyers' share}=\frac{\eta_s}{\eta_s+\eta_d}$$

*(Computed — a \$20 tax in four markets, each row checked against the formula:)*

| market | $\eta_d$ | $\eta_s$ | **buyers bear** | sellers bear | more inelastic |
|---|---|---|---|---|---|
| symmetric | 1.000 | 1.000 | **50.0%** | 50.0% | neither |
| inelastic demand | 0.333 | 1.000 | **75.0%** | 25.0% | **demand** |
| inelastic supply | 3.000 | 1.000 | 25.0% | **75.0%** | **supply** |
| very inelastic demand | 0.111 | 1.000 | **90.0%** | 10.0% | **demand** |

> [!warning] The more inelastic side bears more of the tax
> **Elasticity is the ability to escape.** Whoever can most easily walk away does — and the burden lands on whoever cannot.
>
> **This is [[02 - Supply, Demand and Elasticity|ch. 02]]'s elasticity doing the work**, and it converts a qualitative claim into a prediction: **to know who really pays a tax, estimate the two elasticities.** Mankiw states it in words and draws two diagrams; it is one formula.
>
> *(Practical instance: labour supply is quite inelastic and labour demand is more elastic, so most of a payroll tax lands on **workers** in the form of lower wages — regardless of which half the employer remits.)*

### 5. ⚠️ Deadweight loss grows with the square of the tax

**Mankiw argues this geometrically — a triangle's area goes with the square of its size, so doubling the tax quadruples the loss. Here it is algebraically**, which also delivers the elasticity dependence he only describes:

$$\Delta Q=t\cdot\frac{bc}{b+c}\qquad\Rightarrow\qquad \boxed{\text{DWL}=\tfrac12\,t^2\cdot\frac{bc}{b+c}}$$

*(Computed:)*

| tax $t$ | quantity | revenue | **DWL** | $DWL/t^2$ | ratio to $t=10$ |
|---|---|---|---|---|---|
| 10 | 45 | 450 | 25 | **0.2500** | 1.00× |
| 20 | 40 | 800 | 100 | **0.2500** | **4.00×** |
| 30 | 35 | 1050 | 225 | **0.2500** | **9.00×** |
| 40 | 30 | 1200 | 400 | **0.2500** | 16.00× |
| 50 | 25 | 1250 | 625 | **0.2500** | 25.00× |
| 80 | 10 | 800 | 1600 | **0.2500** | 64.00× |

**$DWL/t^2$ is constant at 0.2500, exactly $\tfrac12\cdot\frac{bc}{b+c}$.** Doubling the tax multiplies the loss by 4; tripling by 9. **Mankiw's claim, verified rather than asserted.**

> [!warning] And deadweight loss rises with elasticity — but the comparison must hold the equilibrium fixed
> **A market with steeper curves is not automatically a less elastic market**, because elasticity depends on the point as well as the slope. *(A supply curve through the origin has unit elasticity everywhere, whatever its slope.)*
>
> *(Computed with all four markets passing through the same point $(P,Q)=(50,50)$, so that $\eta_d = b$ and $\eta_s = c$ exactly:)*
>
> | market | $\eta_d$ | $\eta_s$ | quantity lost | **DWL at $t=\$20$** |
> |---|---|---|---|---|
> | both inelastic | 0.500 | 0.500 | 5.00 | **50** |
> | unit elastic | 1.000 | 1.000 | 10.00 | **100** |
> | both elastic | 3.000 | 3.000 | 30.00 | **300** |
> | very elastic | 6.000 | 6.000 | 60.00 | **600** |
>
> **The more responsive either side is, the more trades the tax kills — and the DWL is the value of exactly those lost trades.**
>
> **Corollary (Ramsey): to raise revenue with least damage, tax the most inelastic things.** **And that is efficient and regressive at the same time**, because necessities are inelastic. **The efficiency case and the fairness case point in opposite directions**, which is the central tension of tax design and the reason it is never settled.

### 6. ⚠️ The Laffer curve, located

**Revenue is $R(t)=t\cdot Q(t)$ — a *quadratic* in $t$, so it must rise, peak and fall.**

$$\frac{dR}{dt}=\frac{c(A-2bt)}{b+c}=0\;\Longrightarrow\;t^*=\frac{A}{2b}=\mathbf{\$50}$$

*(Computed: at $t^*$ the quantity is **25 — exactly half** the free-market 50, revenue is **1250**, and deadweight loss is **625**.)*

> [!warning] At the revenue-maximising tax, deadweight loss is 50% of the revenue raised
> **Collecting \$1250 destroys \$625 of surplus.** The peak of the Laffer curve is nowhere near a good place to be.
>
> *(Computed — the cost per dollar collected:)*
>
> | $t$ | revenue | DWL | **DWL per \$1 of revenue** |
> |---|---|---|---|
> | 10 | 450 | 25 | 0.056 |
> | 30 | 1050 | 225 | 0.214 |
> | **50** | **1250** | 625 | **0.500** ← revenue peak |
> | 70 | 1050 | 1225 | **1.167** |
> | 90 | 450 | 2025 | **4.500** |
>
> **The cost per dollar rises without limit, and it passes 1.0 *before* the revenue peak.** Long before a tax stops raising money, it destroys more value than it collects.
>
> **That is the honest reading of the Laffer curve and it is not the one usually quoted.** The interesting question is never *"where does revenue peak"* — it is **"where does the marginal cost of public funds become unacceptable"**, and that point comes much earlier.

### 7. Trade and tariffs

*(Computed — world price \$30, below the domestic equilibrium of \$50:)*

| | $Q_d$ | $Q_s$ | imports | CS | PS | gov | **total** |
|---|---|---|---|---|---|---|---|
| **free trade** | 70 | 30 | **40** | 2450 | 450 | — | **2900** |
| **\$10 tariff** | 60 | 40 | **20** | 1800 | 800 | 200 | **2800** |
| **change** | | | | **−650** | **+350** | **+200** | **−100** |

$$\textbf{deadweight loss}=\underbrace{50}_{\text{production side}}+\underbrace{50}_{\text{consumption side}}=\mathbf{100}$$

> [!note] Two distinct inefficiencies, and one political lesson
> **Production side:** domestic output expands to producers whose cost exceeds the world price — **we make what we should have bought.**
> **Consumption side:** buyers who valued the good above the world price stop buying it.
>
> **And the political economy is in the numbers.** Producers gain **350** and the government **200**; consumers lose **650**. **The gains are concentrated on a few identifiable firms and the losses are spread thinly over everybody** — so the beneficiaries lobby and the losers do not notice. **That asymmetry, not the economics, is why tariffs persist.**
>
> *(This completes [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s comparative advantage: ch. 01 showed trade creates gains, and this measures what a tariff destroys.)*

## ✏️ Exercises

**1. (Surplus and controls.)** (a) Define the surpluses and explain why equilibrium maximises the total. (b) What does efficiency *not* mean? (c) Analyse a ceiling and a floor.

> [!example]- Solution
> **(a) Because the curves are sorted schedules.**
>
> *(Computed: $CS = PS = \mathbf{1250}$, total **2500** — and checked unit by unit that 50 units maximises it: 2100 at $Q=30$, 2400 at 40, **2500 at 50**, 2400 at 60, 2100 at 70.)*
>
> **The height of demand at quantity $Q$ is the $Q$th buyer's willingness to pay; the height of supply is the $Q$th seller's cost.** So the market trades exactly those units where value exceeds cost.
>
> **Below $Q^*$**: units whose value exceeds cost go untraded — a loss.
> **Above $Q^*$**: units are produced whose cost exceeds their value — also a loss.
>
> **This is why the equilibrium is a maximum and not merely a resting point**, and it is the formal content of [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 6.
>
> **(b) It says nothing about distribution, and it assumes the demand curve measures value.**
>
> **Total surplus adds everyone's dollars equally**, so an allocation can maximise it and be extremely unequal. **Efficiency and equity are different criteria** — Principle 1's trade-off.
>
> **And the framework assumes willingness to pay measures true benefit.** That fails when buyers are misinformed, when they are not the ones affected ([[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s externalities), and when ability to pay differs so much that willingness reflects budget rather than value.
>
> **Both caveats matter for anyone doing policy work with these tools**, because a deadweight-loss number looks objective and rests on assumptions that are frequently false.
>
> **(c) Both reduce quantity; the short side decides.**
>
> *(Computed: a **ceiling at \$30** gives $Q_d=70$, $Q_s=30$ — a **shortage of 40**, only 30 trade, DWL **400**. A **floor at \$70** gives $Q_d=30$, $Q_s=70$ — a **surplus of 40**, again only 30 trade, DWL **400**.)*
>
> **Nobody can be forced to trade, so the smaller quantity is what happens.** A ceiling makes sellers unwilling; a floor makes buyers unwilling. **A control that is not binding — a ceiling above equilibrium — does nothing at all.**
>
> **Two things the triangle misses:**
> - **A shortage triggers non-price rationing** — queues, waiting lists, favouritism. Those are real costs, so 400 is a **lower bound.**
> - **Buyers who are still served genuinely gain.** "Inefficient" is not "nobody benefits", which is precisely why such policies survive: **the winners are identifiable and the losers are the people who never got served.**
>
> *(The two standard cases: rent control is a ceiling — shortages, queues, deteriorating quality; the minimum wage is a floor — a surplus of labour, i.e. unemployment among the least skilled. [[11 - Unemployment|Ch. 11]] returns to the second.)*

**2. (Hard — taxes.)** (a) Show incidence is independent of who remits. (b) What determines the split? (c) Why does DWL grow with $t^2$? (d) Where does revenue peak, and what does that imply?

> [!example]- Solution
> **(a) Compute it both ways and the answers coincide.**
>
> *(Computed for a \$20 tax: levied on **sellers** → buyers pay \$60, sellers keep \$40, $Q=40$. Levied on **buyers** → buyers pay \$60, sellers keep \$40, $Q=40$. **Identical.**)*
>
> **A tax on sellers shifts supply up by $t$; a tax on buyers shifts demand down by $t$. Different diagrams, same wedge** — and the wedge is what determines the outcome.
>
> **The economics: the statute fixes who remits, and then the price moves.** Since the price is what allocates the burden, **the legal assignment is undone by the market before it can have any effect.**
>
> **The practical consequence is worth stating plainly: "employers pay half your payroll tax" describes a cheque, not a burden.**
>
> **(b) The relative elasticities, and nothing else.**
>
> $$\text{buyers' share}=\frac{\eta_s}{\eta_s+\eta_d}$$
>
> *(Verified in four markets: **50%** when symmetric; **75%** when $\eta_d = 0.333$; **25%** when $\eta_d = 3$; **90%** when $\eta_d = 0.111$.)*
>
> **Elasticity is the ability to escape.** The responsive side adjusts its quantity and avoids the price change; **the unresponsive side has nowhere to go and absorbs it.**
>
> **So predicting the incidence of a real tax is an estimation problem, not a legal one** — which is where [[Econometrics/contents/00-Index|econometrics]] enters. *(Labour supply is fairly inelastic and labour demand more elastic, so payroll taxes fall mainly on workers.)*
>
> **(c) Because DWL is a triangle whose base *and* height are both proportional to $t$.**
>
> $$\Delta Q = t\cdot\frac{bc}{b+c}\qquad \text{DWL}=\tfrac12 t\,\Delta Q=\tfrac12 t^2\cdot\frac{bc}{b+c}$$
>
> *(Verified: $DWL/t^2$ is **constant at 0.2500** for every tax from \$10 to \$80, and the loss ratios are exactly **4.00×** at double and **9.00×** at triple.)*
>
> **Mankiw makes this argument geometrically and it is correct. The algebra adds the second half of the story** — the coefficient $\frac{bc}{b+c}$ — **which is where elasticity enters.**
>
> *(Computed with the equilibrium held fixed so the elasticities genuinely differ: DWL of **50 / 100 / 300 / 600** at elasticities of **0.5 / 1 / 3 / 6**.)*
>
> **⚠️ Holding the equilibrium fixed matters.** Comparing markets with different slopes is not the same as comparing different elasticities — **a supply curve through the origin has unit elasticity whatever its slope.** The comparison only isolates elasticity if both curves pass through the same point.
>
> **The policy corollary is Ramsey's: tax inelastic things.** **And that is simultaneously efficient and regressive**, since necessities are inelastic. **Efficiency and fairness point in opposite directions here**, which is why tax design is a genuine dilemma rather than a technical problem.
>
> **(d) At $t^* = A/2b = \$50$ — and the peak is a terrible place to be.**
>
> **Revenue $R(t) = t\,Q(t)$ is a quadratic**, so it must rise, peak, and fall. *(Computed: $t^*=\$50$, where quantity is **exactly half** its free-market level, revenue is **1250**, and DWL is **625**.)*
>
> **So at the revenue-maximising tax, the deadweight loss is 50% of the revenue.**
>
> *(Computed — DWL per dollar of revenue: **0.056** at $t=10$, **0.214** at 30, **0.500** at the peak, **1.167** at 70, **4.500** at 90.)*
>
> **The cost per dollar rises without limit and passes 1.0 before the revenue peak** — beyond that point the tax destroys more value than it raises while still raising more money.
>
> **This is the honest reading of the Laffer curve.** The usual framing asks whether a country is on the "wrong side"; **the better question is the marginal cost of public funds, which is unacceptable long before revenue turns down.** *(Mankiw draws the curve and never locates its peak — the location is the interesting part.)*

**3. (Trade.)** (a) Compute the effect of a tariff. (b) What are the two inefficiencies? (c) Why do tariffs persist?

> [!example]- Solution
> **(a) Total surplus falls by 100.**
>
> *(Computed — world price \$30, \$10 tariff:)*
>
> | | free trade | tariff | change |
> |---|---|---|---|
> | domestic price | \$30 | \$40 | |
> | imports | 40 | **20** | halved |
> | consumer surplus | 2450 | 1800 | **−650** |
> | producer surplus | 450 | 800 | **+350** |
> | government revenue | 0 | 200 | **+200** |
> | **total** | **2900** | **2800** | **−100** |
>
> **The transfers cancel; the −100 is a genuine loss to nobody's benefit.**
>
> **(b) A production distortion and a consumption distortion.**
>
> $$\text{DWL}=\underbrace{50}_{\text{production}}+\underbrace{50}_{\text{consumption}}=100$$
>
> - **Production side** — domestic output rises from 30 to 40, and those extra units cost more to make than the world price. **We produce what we should have bought.**
> - **Consumption side** — quantity demanded falls from 70 to 60, and those buyers valued the good above the world price. **Trades worth making do not happen.**
>
> **Note that the government's 200 is *not* a loss — it is a transfer.** The loss is only the two triangles, which is why a tariff is less damaging than a quota that transfers the same amount to foreign exporters.
>
> **(c) Because the gains are concentrated and the losses are diffuse.**
>
> **Producers gain 350 and the government 200; consumers lose 650.** *(Computed.)*
>
> **The losers outnumber the winners and lose less each.** A domestic producer's gain is large, identifiable and worth lobbying for; a consumer's loss is small, spread across many goods, and not worth anyone's time to oppose. **So the political process hears from one side.**
>
> **That asymmetry — not any economic argument — is the durable explanation for protection**, and it generalises far beyond trade: **any policy with concentrated benefits and diffuse costs is politically favoured regardless of its total effect.**
>
> **The honest caveats on the other side**, which Mankiw gives fairly: the jobs argument (real for specific workers, though the model says the loss is smaller than the gain elsewhere), national security, infant industry, and using tariff threats as bargaining leverage. **The economics establishes that free trade raises the total; it does not establish that every displaced worker is compensated** — which is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]] §6's distinction between the size of the gain and its distribution, arriving again.

## 📝 Summary

- **Consumer surplus = willingness to pay − price; producer surplus = price − cost.** *(Computed: **1250** each, total **2500**.)*
- **The demand curve is valuations sorted high-to-low and supply is costs sorted low-to-high** — which is why the market trades every unit where value exceeds cost and no other. *(Verified: total surplus peaks at $Q^*=50$.)*
- **⚠️ Efficiency is silent on distribution** and assumes willingness to pay measures true value. Both assumptions fail routinely.
- **Binding price controls always cut the quantity traded** — the short side decides. *(Computed: ceiling and floor each leave 30 units trading with DWL **400**.)* **Non-price rationing makes that a lower bound**, and the buyers still served do gain — which is why such policies survive.
- **⚠️ Who legally pays a tax is irrelevant** *(verified: levying \$20 on sellers and on buyers give identical prices and quantities)*. **The statute names who writes the cheque, not who bears the cost.**
- **⚠️ The burden splits by relative elasticity: buyers' share $=\eta_s/(\eta_s+\eta_d)$** *(verified at **50% / 75% / 25% / 90%** across four markets)*. **The more inelastic side bears more — elasticity is the ability to escape.**
- **⚠️ $\text{DWL} = \tfrac12 t^2\cdot\frac{bc}{b+c}$ — quadratic in the tax** *(verified: $DWL/t^2$ **constant at 0.2500**; doubling the tax gives **4.00×** the loss, tripling **9.00×**)*.
- **DWL rises with elasticity** *(computed with the equilibrium held fixed: **50 / 100 / 300 / 600** at elasticities **0.5 / 1 / 3 / 6**)*. **⚠️ The comparison only isolates elasticity if both curves pass through the same point** — different slopes are not different elasticities.
- **Ramsey's corollary: tax inelastic things.** **Efficient and regressive at once**, since necessities are inelastic — so the efficiency and fairness cases point opposite ways.
- **⚠️ Revenue peaks at $t^*=\$50$, where quantity is exactly halved and DWL is 50% of revenue** *(computed)*. **Mankiw draws the Laffer curve and never locates its peak.**
- **⚠️ DWL per dollar of revenue rises without limit and passes 1.0 *before* the peak** *(computed: 0.056 → 0.500 at the peak → 4.500)*. **The right question is the marginal cost of public funds, not where revenue turns down.**
- **A tariff costs 100 in this market** *(computed: consumers −650, producers +350, government +200)*, split into a **production distortion** (we make what we should have bought) and a **consumption distortion**.
- **⚠️ Tariffs persist because gains are concentrated and losses diffuse** — which generalises to any policy with that shape.

## ⚠️ Important Notes

1. **Surplus is an *area*; the curve heights are valuations and costs.** Getting the height interpretation right makes every diagram computable.
2. **⚠️ Efficiency ≠ fairness.** Total surplus weights everyone's dollar equally.
3. **A deadweight-loss figure looks objective and rests on the assumption that demand measures value.**
4. **A non-binding price control does nothing.** Check which side of equilibrium it sits on first.
5. **⚠️ The short side of the market determines the quantity** under any binding control.
6. **Shortages produce non-price rationing**, so the DWL triangle understates the cost.
7. **⚠️ Never infer tax incidence from the statute.** Compute it from elasticities.
8. **⚠️ Buyers' share $=\eta_s/(\eta_s+\eta_d)$** — memorise the direction: **inelastic side pays.**
9. **⚠️ DWL is quadratic in the tax rate.** Two small taxes do far less damage than one twice as large.
10. **DWL rises with elasticity** — so broad-based low-rate taxes beat narrow high-rate ones.
11. **⚠️ Hold the equilibrium fixed when comparing elasticities.** A steeper curve is not necessarily less elastic.
12. **The Ramsey rule is efficient and regressive simultaneously.** Say so when quoting it.
13. **⚠️ The Laffer peak is not a target.** DWL per dollar exceeds 1 before you reach it.
14. **Tariff revenue is a transfer, not a loss.** Only the two triangles are deadweight.
15. **⚠️ Concentrated gains and diffuse losses predict policy better than efficiency does.**
16. **Trade raises the total and does not compensate the displaced** — the size and the distribution of a gain are separate questions ([[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]).

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly** *(Macro 2017, PDF pp. 142–217 for chs. 6–9)*, and the outline located all four chapters precisely.
>
> **⚠️ THE OPERATOR CIPHER applies throughout** — see [[00-Index]]. **Nothing was transcribed**: every relationship here was reconstructed from prose and verified numerically. **All of Mankiw's stated results reproduce** — the tax-incidence equivalence, the geometric square rule (his "double the tax and DWL rises by a factor of 4" is confirmed exactly), and the qualitative Laffer shape.
>
> **⚠️ This is the most figure-dependent chapter so far and every figure is lost.** Mankiw's welfare analysis is conducted almost entirely in shaded areas: **the surplus diagrams, the price-control panels, Figure 6's five-panel deadweight-loss/revenue sequence, Figure 9's two incidence panels, and the tariff diagram are all images.** What survives is captions and callout fragments — *"1. When the demand curve is inelastic . . ."* — which **look like content and are not**.
>
> **So every area in this note is computed from an explicitly stated linear market ($Q_d = 100-P$, $Q_s = P$) rather than read off a diagram.** The market is mine; **the definitions, the formulas and the qualitative results are Mankiw's.**
>
> **No erratum.** Every result the prose states reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §4b's incidence formula $\eta_s/(\eta_s+\eta_d)$ is mine.** **Mankiw shows two diagrams and says the more inelastic side bears more; he never computes a share.** The four-market table turns a qualitative claim into a prediction.
> - **⚠️ §5's algebraic derivation $\text{DWL}=\tfrac12 t^2\frac{bc}{b+c}$ is mine.** Mankiw's geometric argument for the square rule is correct and complete as far as it goes; **the algebra additionally yields the elasticity coefficient**, which is what connects the square rule to his separate qualitative claim about elasticity.
> - **⚠️ The warning that comparing slopes is not comparing elasticities** — and the reconstruction holding the equilibrium fixed so that $\eta_d = b$ exactly — **is mine, and it corrected an error in my own first attempt** at this section.
> - **⚠️ §6 locates the Laffer peak.** **Mankiw draws the curve and never solves for $t^*$.** The findings that the quantity is exactly halved at the peak, that DWL is **50%** of revenue there, and that **DWL per dollar passes 1.0 before the peak**, are all additions — and the last one reframes what the curve is actually useful for.
> - **The Ramsey corollary**, and the observation that it makes efficiency and equity point in opposite directions, is an addition.
> - **§7's concentrated-gains/diffuse-losses framing** is stated by Mankiw for tariffs; **the generalisation to any policy of that shape is mine.**
> - **The note that a tariff is less damaging than an equivalent quota** (because the revenue is a transfer rather than a gift to foreign exporters) is an addition.
>
> **Deliberately compressed.** **Mankiw ch. 6's extended case studies** (rent control, the minimum wage) are compressed to the analytical points in §2 and Exercise 1(c) — **the minimum wage is treated properly in [[11 - Unemployment|ch. 11]]**, which has the labour-market apparatus. **Ch. 8's discussion of the elasticity of labour supply and the size of the US tax distortion** is represented by §5's general result. **Ch. 9's arguments for restricting trade** (jobs, national security, infant industry, unfair competition, bargaining chip) are summarised in Exercise 3(c) rather than treated individually; they are political arguments whose economic content is the single distributional point. **The gains-from-trade case where a country *exports* rather than imports** is the mirror image of §7 and is not repeated. **Import quotas and the equivalence between tariffs and quotas** are noted but not worked separately.

**Previous:** [[02 - Supply, Demand and Elasticity]] · **Next:** [[04 - Externalities, Public Goods and Common Resources]]
