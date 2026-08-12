---
subject: Macroeconomics & Microeconomics
chapter: 6
tags: [ds, economics, microeconomics, monopoly, oligopoly, price-discrimination, cournot, prisoners-dilemma]
source: "Mankiw, *Principles of Microeconomics* 6e, ch. 15–17"
---

# Monopoly, Oligopoly and Monopolistic Competition

**[[05 - Production Costs and Competitive Markets|Chapter 05]] derived every result from one assumption: the firm is a *price taker*. This chapter removes it.**

**A firm facing a downward-sloping demand curve has $MR < P$. It sets $MR = MC$, so $P > MC$ — and that single inequality is the whole of market power.**

**Four results.**

**§2 — $MR = P(1-1/e)$ unifies this chapter with [[02 - Supply, Demand and Elasticity|ch. 02]].** *(Verified at nine quantities.)* Ch. 02 found revenue peaks where $e=1$; here it peaks where $MR=0$. **They are the same statement** — and it yields a result Mankiw never states: **a monopolist never operates on the inelastic part of its demand curve.**

**§4 — perfect price discrimination is *efficient*.** *(Computed: it produces the **competitive** quantity of 8 with **zero** deadweight loss, while transferring **all 32** of the surplus to the seller.)* **The fourth appearance of the subject's organising result.**

**§6 — Cournot oligopoly with $N$ firms is [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s tragedy of the commons.** *(Identical formula $q=(a-c)/(N+1)$; **identical percentages at every matching $N$** — 100.0%, 88.9%, 33.1%, 7.7%, 0.4%.)* **Same mathematics, opposite normative verdicts.**

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]] for the operator cipher.

## 📘 Main Knowledge

### 1. Monopoly revenue — verified

**A monopoly is the sole seller, protected by a barrier to entry**: a resource monopoly, a government-created monopoly (patents, copyright), or a **natural monopoly** — where one firm can supply the market more cheaply than two, because average total cost is still falling at the relevant scale.

*(Verified — Mankiw's Table 1, demand $P = 11 - Q$:)*

| $Q$ | $P$ | **TR** | AR | **MR** |
|---|---|---|---|---|
| 0 | 11 | 0 | — | — |
| 1 | 10 | 10 | 10 | 10 |
| 2 | 9 | 18 | 9 | 8 |
| 3 | 8 | 24 | 8 | 6 |
| 4 | 7 | 28 | 7 | 4 |
| **5** | 6 | **30** | 6 | 2 |
| **6** | 5 | **30** | 5 | **0** |
| 7 | 4 | 28 | 4 | −2 |
| 8 | 3 | 24 | 3 | −4 |

> [!note] AR = P at every quantity — the demand curve *is* the average-revenue curve
> $$AR=\frac{TR}{Q}=\frac{P\cdot Q}{Q}=P$$
> **True for any firm, competitive or not.** It is why one curve can be read as either, and why the monopoly diagram has a demand curve and a *separate*, lower, marginal-revenue curve.

> [!warning] ⚠️ The table ties at TR = 30 — the third time in this subject
> *(Solved exactly: $TR = Q(11-Q)$, $\frac{dTR}{dQ}=11-2Q=0 \Rightarrow Q^*=5.5$, $P=5.5$, **$TR = 30.25$** — above both tabulated 30s. And $MR=0$ exactly there, which the table shows *between* the two rows.)*
>
> **[[02 - Supply, Demand and Elasticity|Ch. 02]]'s total revenue tied at \$24; [[05 - Production Costs and Competitive Markets|ch. 05]]'s ATC tied at 1.30; this ties at 30.** **A tie in a discrete table means the optimum lies between the grid points** — treat it as an instruction to solve the continuous problem.

### 2. ⚠️ Why marginal revenue is below price

**Selling one more unit has two effects** *(Mankiw's framing)*:

- **output effect** — one more unit sold at price $P$: **$+P$**
- **price effect** — the price falls on **all** units already being sold: **$Q\cdot\frac{dP}{dQ} < 0$**

**A competitive firm has no price effect** — it can sell any quantity at the market price — **so $MR = P$. A monopolist has one, so $MR < P$.**

$$MR=\frac{d(PQ)}{dQ}=P+Q\frac{dP}{dQ}=P\!\left[1+\frac{Q}{P}\frac{dP}{dQ}\right]=\boxed{P\!\left(1-\frac{1}{e}\right)}$$

*(Verified at nine quantities against $MR = 11-2Q$ computed directly — all match:)*

| $Q$ | $P$ | $e$ | $MR = P(1-1/e)$ |
|---|---|---|---|
| 2 | 9.0 | 4.5000 | 7.0000 |
| 4 | 7.0 | 1.7500 | 3.0000 |
| **5.5** | **5.5** | **1.0000** | **0.0000** |
| 6 | 5.0 | 0.8333 | −1.0000 |
| 8 | 3.0 | 0.3750 | −5.0000 |

> [!warning] This unifies [[02 - Supply, Demand and Elasticity|ch. 02]] with this chapter
> | elasticity | $MR$ | selling more… |
> |---|---|---|
> | $e>1$ (elastic) | $MR>0$ | **raises** revenue |
> | $e=1$ (unit) | $MR=0$ | revenue at its **maximum** |
> | $e<1$ (inelastic) | $MR<0$ | **lowers** revenue |
>
> **Ch. 02 found "total revenue peaks where $e=1$". This chapter finds "total revenue peaks where $MR=0$". $MR = P(1-1/e)$ shows they are the same statement.**
>
> **And it yields a result Mankiw never states: a monopolist never operates on the inelastic part of its demand curve.** There $MR < 0 \le MC$, so cutting output would **raise** revenue *and* **cut** cost — strictly better. **A profit-maximising monopolist always sits where $e > 1$.**
>
> *(Practical use: if you observe a firm with pricing power facing inelastic demand, either it is not maximising profit or you have mismeasured the elasticity.)*

### 3. Monopoly outcome and deadweight loss

*(Computed — demand $P = 11-Q$, constant $MC = 3$:)*

| | rule | $Q$ | $P$ |
|---|---|---|---|
| **competitive** | $P = MC$ | **8** | **\$3** |
| **monopoly** | $MR = MC$ | **4** | **\$7** |

| | consumer surplus | producer surplus | **total** |
|---|---|---|---|
| competitive | **32** | 0 | **32** |
| monopoly | 8 | 16 | **24** |

$$\textbf{deadweight loss}=\tfrac12\times4\times4=\mathbf{8}$$

*(Verified: $32 - 24 = 8$ ✓)*

> [!note] The monopolist's profit is a transfer, not a loss
> **Of the 24 points of surplus consumers lose, 16 become producer surplus — a transfer — and only 8 vanish.** The deadweight loss is exactly the trades that stop happening because $P > MC$.
>
> **[[05 - Production Costs and Competitive Markets|Ch. 05]] showed a competitive firm produces where $P = MC$; a monopolist sets $MR = MC$ and $MR < P$, so $P > MC$ always.** **That inequality *is* the inefficiency**, and everything else in the chapter follows from it.
>
> **A monopolist has no supply curve.** Ch. 05's supply curve existed because $P = MC$ pinned quantity to price; here quantity depends on the *shape* of demand, not just its height. **Asking "how much would a monopolist supply at \$7?" has no answer** without knowing the whole demand curve.

**Policy responses**, in Mankiw's order: **antitrust** (block mergers, break up firms), **regulation** (but marginal-cost pricing makes a natural monopoly lose money, since $MC <$ ATC when ATC is falling), **public ownership**, and **doing nothing** — on the view that government failure may exceed market failure.

### 4. ⚠️ Price discrimination: efficient *and* extractive

**Perfect price discrimination** — charging each buyer exactly their willingness to pay — means **$MR = P$ for every unit**, so the firm sells until $P = MC$.

*(Computed:)*

| | quantity | consumer surplus | producer surplus | **DWL** |
|---|---|---|---|---|
| competitive | **8** | 32 | 0 | **0** |
| single-price monopoly | 4 | 8 | 16 | **8** |
| **perfect discrimination** | **8** | **0** | **32** | **0** |

> [!warning] Perfect price discrimination produces the *efficient* quantity
> **Same output as perfect competition, zero deadweight loss — and the entire surplus goes to the seller.**
>
> **So "efficient" and "good for consumers" are different claims, and here they point in opposite directions.** Every mutually beneficial trade happens; the buyer simply captures none of the gain.
>
> **⚠️ This is the fourth appearance of the subject's organising result:**
>
> | chapter | what fixes the **allocation** | what fixes the **split** |
> |---|---|---|
> | [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage\|01]] | comparative advantage | the **price** |
> | [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade\|03]] | the tax **wedge** *(the statute is irrelevant)* | **elasticities** |
> | [[04 - Externalities, Public Goods and Common Resources\|04]] | benefit vs cost | the **property right** |
> | **06** | **$P = MC$ under discrimination** | **the pricing scheme** |
>
> **Efficiency and distribution are independent. Again.**

**Real discrimination is imperfect** and requires: **market power**, the ability to **segment** buyers by willingness to pay, and prevention of **resale**. *(Cinema and airline pricing, quantity discounts, coupons — a coupon is a device that makes buyers sort themselves by how much their time is worth.)*

### 5. Oligopoly: the Jack and Jill duopoly

*(Verified — Mankiw's demand schedule gives $P = 120 - Q$ (10 gal → \$110, 20 gal → \$100 ✓), with $MC = 0$:)*

| | $Q$ | $P$ | total profit | each |
|---|---|---|---|---|
| **competitive** ($P=MC$) | **120** | \$0 | \$0 | \$0 |
| **monopoly / cartel** | **60** | **\$60** | **\$3 600** | \$1 800 |
| **duopoly (Nash)** | **80** | **\$40** | **\$3 200** | **\$1 600** |

**The duopoly lands between monopoly and competition** — more output and a lower price than a cartel, less output and a higher price than competition.

> [!warning] Why the cartel breaks — the deviation pays
> *(Computed from the cartel agreement of 30 gallons each:)*
>
> | | $Q$ | $P$ | cheater | loyal |
> |---|---|---|---|---|
> | both keep the deal | 60 | \$60 | \$1 800 | \$1 800 |
> | one cheats to 35 | 65 | \$55 | **\$1 925** | \$1 650 |
> | **one cheats to 40** | 70 | \$50 | **\$2 000** | **\$1 500** |
>
> **Cheating from 30 to 40 raises the cheater's profit from \$1 800 to \$2 000.** Both parties reason identically, so **both cheat**, and they land at the Nash outcome of **\$1 600 each — worse for both than the cartel.**
>
> **That is a prisoners' dilemma**, and it explains why cartels are unstable **without any need for antitrust law to break them.** The self-interest that creates the cartel's appeal is the same self-interest that destroys it.
>
> **⚠️ Third appearance of individually-rational / collectively-disastrous**: [[02 - Supply, Demand and Elasticity|ch. 02]]'s farmers (each wants to grow more; collectively they want less), [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s commons, and now the cartel. **In ch. 02 and ch. 04 the outcome was bad; here it is *good* — because the victims are the colluding firms and the beneficiaries are buyers.**

### 6. ⚠️ Oligopoly with $N$ firms *is* the tragedy of the commons

$$\text{Cournot: } q_i=\frac{a-c}{N+1}\qquad Q=\frac{N(a-c)}{N+1}\;\longrightarrow\;a-c \text{ as } N\to\infty$$

*(Computed:)*

| $N$ | each firm | total $Q$ | price | total profit | **vs monopoly** |
|---|---|---|---|---|---|
| **1** | 60.000 | 60.000 | 60.000 | 3 600.00 | **100.0%** |
| 2 | 40.000 | 80.000 | 40.000 | 3 200.00 | **88.9%** |
| 3 | 30.000 | 90.000 | 30.000 | 2 700.00 | 75.0% |
| 5 | 20.000 | 100.000 | 20.000 | 2 000.00 | 55.6% |
| 10 | 10.909 | 109.091 | 10.909 | 1 190.08 | **33.1%** |
| 50 | 2.353 | 117.647 | 2.353 | 276.82 | **7.7%** |
| **1000** | 0.120 | 119.880 | 0.120 | 14.37 | **0.4%** |

> [!warning] The identical formula — and identical numbers — as [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s commons
> **Ch. 04's $N$ herders each chose $q=(V-C)/(N+1)$, total $Q=N(V-C)/(N+1)$.** **This is the same expression**, and the "vs optimum" column there reads **100.0%, 88.9%, 33.1%, 7.7%, 0.4%** at $N = 1, 2, 10, 50, 1000$ — **exactly the percentages above.**
>
> **The two chapters tell opposite stories about one piece of mathematics:**
>
> | | more participants → | verdict |
> |---|---|---|
> | **[[04 - Externalities, Public Goods and Common Resources\|ch. 04]]** | more output | **disaster** — the commons is destroyed |
> | **ch. 06** | more output | **good** — competition, $P\to MC$ |
>
> **The model cannot tell them apart, and it should not.** In both cases each actor ignores the effect of their own output on everyone else's price or yield. **Whether that ignored externality is a *bad* (congestion) or a *good* (lower prices for buyers) is not in the mathematics** — it is a fact about who the third parties are.
>
> **Mankiw makes exactly this point in words** — that the oligopolists' self-interest hurts *them* and helps buyers — **and never notices it is the same equilibrium he wrote down two chapters earlier.**
>
> **The transferable lesson: an equilibrium is not good or bad on its own.** The welfare verdict comes from who bears the externality, and that must be supplied from outside the model.

**With enough firms, oligopoly becomes competition.** $N=1$ is monopoly; $N\to\infty$ gives $P\to MC$ and zero profit. **Market structure is a spectrum, not three boxes.**

> [!note] What sustains collusion, and why antitrust is not simple
> **Repetition is the key.** In a one-shot game, cheating dominates. **Repeated indefinitely, cooperation can be sustained by the threat of future punishment** — which is why collusion is more common in stable markets with few, long-lived firms.
>
> **And Mankiw is careful that some practices which *look* anticompetitive are contested**: resale price maintenance, predatory pricing (which requires recouping the losses later, and is hard to distinguish from ordinary competition), and tying. **"This firm is large" is not an antitrust argument.**

### 7. Monopolistic competition: $P > MC$ *and* zero profit

**Many firms, differentiated products, free entry.** Each firm's product is distinctive, so **it faces a downward-sloping demand curve** and sets $MR = MC$, giving $P > MC$. **But free entry competes profit to zero, as in [[05 - Production Costs and Competitive Markets|ch. 05]].**

**Both can hold only if demand is *tangent* to ATC:**

$$P = ATC \;\text{(zero profit)} \qquad\text{and}\qquad P > MC \;\text{(markup)}$$

**Which forces production on the downward-sloping part of ATC — below efficient scale. That gap is *excess capacity*.**

| structure | $P$ vs $MC$ | long-run profit | at efficient scale? |
|---|---|---|---|
| **perfect competition** ([[05 - Production Costs and Competitive Markets\|ch. 05]]) | $P = MC$ | zero | **yes** |
| **monopolistic competition** | $P > MC$ | **zero** | **no — excess capacity** |
| **monopoly** | $P > MC$ | positive | no |

> [!note] Monopoly's inefficiency with competition's zero profit
> **Firms are not getting rich, and the inefficiency is real anyway.** That combination is what makes monopolistic competition awkward: **there is no profit to tax away and no obvious intervention.**
>
> **And the welfare verdict is genuinely ambiguous** — Mankiw is careful here in a way he is not about monopoly. **The markup and excess capacity are costs; product variety is a benefit the surplus triangle does not measure.** A new restaurant imposes a *business-stealing* externality on rivals and confers a *product-variety* externality on consumers, and **nothing says which is larger.**
>
> **So unlike [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s externalities or §3's monopoly, there is no clean policy conclusion** — which is the honest answer and worth stating as one.

## ✏️ Exercises

**1. (Monopoly.)** (a) Why is $MR < P$? (b) Derive the elasticity relation and its consequence. (c) Compute the deadweight loss. (d) Why has a monopolist no supply curve?

> [!example]- Solution
> **(a) Because raising sales requires cutting the price on *every* unit.**
>
> **Two effects:** the **output effect** ($+P$ from the extra unit) and the **price effect** ($Q\cdot dP/dQ < 0$, the revenue lost on units already being sold).
>
> **A competitive firm has no price effect — it sells all it wants at the market price — so $MR = P$.** *(That is precisely [[05 - Production Costs and Competitive Markets|ch. 05]]'s price-taking assumption.)* **A monopolist faces the whole market demand curve, so the price effect is real and $MR < P$.**
>
> *(Verified in Mankiw's Table 1: at $Q=4$ the price is \$7 but $MR$ is \$4 — the \$3 difference is exactly the \$1 given up on each of the first three units.)*
>
> **(b) $MR = P(1-1/e)$, and a monopolist never sits on the inelastic portion.**
>
> $$MR=P+Q\frac{dP}{dQ}=P\!\left[1+\frac{Q}{P}\frac{dP}{dQ}\right]=P\!\left(1-\frac1e\right)$$
>
> *(Verified at nine quantities against $MR = 11-2Q$.)*
>
> **This unifies the chapter with [[02 - Supply, Demand and Elasticity|ch. 02]]**: $MR>0 \iff e>1$, and revenue peaks where $MR=0 \iff e=1$. **Two statements of one fact.**
>
> **⚠️ The consequence Mankiw omits: $e>1$ always at the optimum.** If $e<1$ then $MR<0\le MC$, so reducing output would **raise revenue and lower cost simultaneously** — strictly better. **A profit-maximising firm with market power is never on the inelastic branch.**
>
> **Useful diagnostically**: an estimated elasticity below 1 for a price-setting firm means either the firm is not maximising or the estimate is wrong.
>
> **(c) 8 — and most of what consumers lose is a transfer.**
>
> *(Computed with $P=11-Q$, $MC=3$: competitive $Q=8$ at \$3; monopoly $Q=4$ at \$7.)*
>
> | | CS | PS | total |
> |---|---|---|---|
> | competitive | 32 | 0 | **32** |
> | monopoly | 8 | 16 | **24** |
>
> **Consumers lose 24; producers gain 16; 8 disappears.** *(Verified: $32-24=8$.)*
>
> **The distinction matters for policy.** The transfer is a distributional question; **only the triangle is a pure loss.** A policy that merely moved the 16 back to consumers would not address the inefficiency at all — **which is [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s efficiency/distribution split showing up in how one reads the diagram.**
>
> **(d) Because quantity depends on the *shape* of demand, not just the price.**
>
> **A supply curve answers "how much at price $P$?" — and for a competitive firm $P=MC$ answers it directly.** A monopolist chooses $Q$ where $MR=MC$ and *then* reads the price off demand. **Two different demand curves passing through the same price can give different monopoly quantities**, so no function from price to quantity exists.
>
> **This is not a technicality**: it means the supply-and-demand apparatus of [[02 - Supply, Demand and Elasticity|ch. 02]] simply does not apply to a monopolised market, and questions phrased in its terms have no answer.

**2. (Hard — price discrimination.)** (a) Why is perfect discrimination efficient? (b) What does that show? (c) What does real discrimination require?

> [!example]- Solution
> **(a) Because the price effect disappears.**
>
> **A single-price monopolist restricts output because selling one more unit forces a price cut on *all* units.** A perfect discriminator cuts the price only for the marginal buyer, **so $MR = P$ for every unit** — exactly the competitive firm's condition — and it therefore sells until $P = MC$.
>
> *(Computed: quantity **8**, the same as perfect competition; **DWL 0**; and producer surplus **32**, the entire social surplus.)*
>
> **Every mutually beneficial trade occurs.** The buyers simply capture none of the gain.
>
> **(b) That "efficient" and "good for consumers" are different claims — the fourth time.**
>
> | | quantity | CS | PS | DWL |
> |---|---|---|---|---|
> | competitive | 8 | **32** | 0 | 0 |
> | single-price monopoly | 4 | 8 | 16 | **8** |
> | perfect discrimination | **8** | **0** | **32** | **0** |
>
> **Compared with a single-price monopoly, discrimination *raises* total surplus (24 → 32) and *lowers* consumer surplus (8 → 0).** **Both statements are true and they are usually confused.**
>
> **⚠️ This is the subject's organising result again** — [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]] (price), [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] (statute/elasticities), [[04 - Externalities, Public Goods and Common Resources|ch. 04]] (property right), **and now the pricing scheme.** **Efficiency is fixed by whether the right trades happen; distribution by an institutional variable; and the two move independently.**
>
> **The practical consequence: a welfare argument about price discrimination must say which measure it means.** Airline pricing that looks exploitative may be expanding output — **and the passengers on cheap seats exist only because the expensive seats do.**
>
> **(c) Market power, segmentation, and no resale.**
>
> 1. **Market power** — a price taker cannot discriminate.
> 2. **A way to sort buyers by willingness to pay** — directly (student discounts) or by **self-selection** (coupons, advance-purchase fares, hardback then paperback). **A coupon is a device that sorts buyers by the value of their time**, which correlates with willingness to pay.
> 3. **No resale** — otherwise low-price buyers become arbitrageurs. *(This is why services discriminate more easily than goods.)*
>
> **Real discrimination is imperfect**, so it lands between the two extremes: **more output than a single price, less surplus extracted than perfect discrimination.** **Whether it raises or lowers total surplus depends on how much output expands**, and that is an empirical question rather than a theoretical one.

**3. (Oligopoly.)** (a) Compute the duopoly outcomes. (b) Why do cartels fail? (c) What is the relation to ch. 04? (d) What is monopolistic competition's verdict?

> [!example]- Solution
> **(a) Between monopoly and competition.**
>
> *(Verified — $P = 120 - Q$, $MC = 0$:)*
>
> | | $Q$ | $P$ | total profit |
> |---|---|---|---|
> | competitive | 120 | \$0 | \$0 |
> | cartel | 60 | \$60 | **\$3 600** |
> | **duopoly (Nash)** | **80** | **\$40** | **\$3 200** |
>
> **Each duopolist earns \$1 600 against \$1 800 under the cartel** — so both would prefer to collude, and neither can be trusted to.
>
> **(b) Because deviating is individually profitable at the cartel quantity.**
>
> *(Computed from 30 each: cheating to 40 raises the cheater's profit from **\$1 800 to \$2 000**, while the loyal partner falls to \$1 500.)*
>
> **The cheater captures the full gain on the extra 10 gallons and bears only half the price fall.** Both reason identically, both cheat, and both end at **\$1 600 — worse than the \$1 800 they could have had.**
>
> **A prisoners' dilemma**, and it means **cartels are unstable on their own** — competition authorities are pushing on something already falling over. *(Which also explains why real cartels invest so heavily in monitoring and punishment: those are attempts to convert a one-shot game into a repeated one.)*
>
> **⚠️ Third appearance of individually-rational / collectively-disastrous**: [[02 - Supply, Demand and Elasticity|ch. 02]]'s farmers, [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s commons, and this. **But the sign of the welfare verdict flips: here the "disaster" falls on the colluders and the benefit on buyers.**
>
> **(c) It is literally the same equilibrium.**
>
> $$\text{Cournot: } q_i=\frac{a-c}{N+1} \qquad\qquad \text{Ch. 04 commons: } q_i=\frac{V-C}{N+1}$$
>
> *(And the numbers match exactly: profit as a share of the monopoly benchmark reads **100.0%, 88.9%, 33.1%, 7.7%, 0.4%** at $N = 1, 2, 10, 50, 1000$ — **identical to ch. 04's "vs optimum" column at the same $N$.**)*
>
> **In both settings each actor captures the full benefit of their own output and bears only $1/N$ of the cost it imposes on the others** — congestion in ch. 04, a lower price here.
>
> **The mathematics is identical and the verdicts are opposite**, because the party bearing the externality differs: **other herders (who are also the users we care about) versus consumers (whom we are happy to see gain).**
>
> **The transferable lesson: an equilibrium is not good or bad by itself.** The welfare judgement requires knowing who the affected third parties are, **and that information is not in the model.** *(A useful check on any "the market equilibrium is efficient/inefficient" claim: ask whose surplus the externality lands on.)*
>
> **(d) Genuinely ambiguous, and that is the answer.**
>
> **Monopolistic competition has $P > MC$ (monopoly's inefficiency) and zero profit (competition's discipline)**, which forces production below efficient scale — **excess capacity.**
>
> **Two externalities pull opposite ways when a firm enters:**
> - **business-stealing** — it takes customers from rivals (negative, and rivals do not count it);
> - **product-variety** — consumers gain an option they value (positive, and the entrant does not capture it).
>
> **Nothing in the theory says which dominates**, so there is no clean prescription — unlike [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s externalities (tax them) or §3's monopoly (antitrust).
>
> **And the markup is not a scandal**: with zero economic profit, firms are earning the normal return ([[05 - Production Costs and Competitive Markets|ch. 05]] §6). **The inefficiency is real and there is nobody getting rich from it**, which is exactly why it is hard to do anything about.

## 📝 Summary

- **This chapter removes [[05 - Production Costs and Competitive Markets|ch. 05]]'s price-taking assumption.** A downward-sloping firm demand curve gives $MR < P$; the firm sets $MR = MC$; **so $P > MC$ — and that inequality is the whole of market power.**
- **Mankiw's Table 1 verified.** **$AR = P$ at every quantity — the demand curve *is* the average-revenue curve.**
- **⚠️ The table ties at TR = 30 for $Q=5$ and $Q=6$ — the third discrete tie in this subject** *(exact peak: $Q^*=5.5$, $TR=30.25$, where $MR=0$)*. **[[02 - Supply, Demand and Elasticity|Ch. 02]] tied at \$24, [[05 - Production Costs and Competitive Markets|ch. 05]] at 1.30. A tie means solve the continuous problem.**
- **Two effects of selling more: the output effect ($+P$) and the price effect ($Q\,dP/dQ$).** A competitive firm has no price effect.
- **⚠️ $MR = P(1-1/e)$** *(verified at nine quantities)* **unifies this chapter with [[02 - Supply, Demand and Elasticity|ch. 02]]**: revenue peaks where $MR=0$ *and* where $e=1$ — the same statement.
- **⚠️ A monopolist never operates on the inelastic part of demand** — there $MR<0\le MC$, so cutting output raises revenue *and* cuts cost. **Mankiw never states this.**
- **Monopoly deadweight loss = 8** *(computed: competitive $Q=8$ at \$3; monopoly $Q=4$ at \$7; CS 32→8, PS 0→16)*. **The profit is a transfer; only the triangle is lost.**
- **A monopolist has no supply curve** — quantity depends on the shape of demand, not just its height.
- **⚠️ Perfect price discrimination is *efficient*** *(computed: quantity **8** — the competitive level — **DWL 0**, and **all 32** of the surplus to the seller)*. **"Efficient" and "good for consumers" point in opposite directions here.**
- **⚠️ Fourth appearance of the organising result**: allocation fixed by fundamentals, split fixed by an institutional variable — **price ([[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]), statute ([[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]), property right ([[04 - Externalities, Public Goods and Common Resources|ch. 04]]), pricing scheme (ch. 06).**
- **Real discrimination needs market power, segmentation, and no resale.** A coupon sorts buyers by the value of their time.
- **Jack and Jill verified**: competitive $Q=120$ at \$0; cartel $Q=60$ at \$60 (**\$3 600**); **duopoly $Q=80$ at \$40 (\$3 200)** — between the two.
- **⚠️ Cartels fail because deviation pays** *(computed: cheating from 30 to 40 raises the cheater from **\$1 800 to \$2 000**)*. Both cheat and both end worse. **A prisoners' dilemma — cartels are unstable without antitrust.**
- **⚠️ Cournot with $N$ firms *is* [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s tragedy of the commons** — identical formula $q=(a-c)/(N+1)$ and **identical percentages** (100.0%, 88.9%, 33.1%, 7.7%, 0.4%). **Same mathematics, opposite verdicts, because the externality lands on different people.**
- **An equilibrium is not good or bad by itself** — the welfare judgement needs to know who bears the externality, and that is not in the model.
- **Monopolistic competition: $P > MC$ *and* zero profit ⇒ excess capacity.** **Monopoly's inefficiency with competition's zero profit**, and the verdict is genuinely ambiguous — business-stealing versus product-variety externalities.

## ⚠️ Important Notes

1. **$P > MC$ is market power.** Everything else in the chapter follows from it.
2. **$AR = P$ always**, for any firm — the demand curve doubles as the average-revenue curve.
3. **⚠️ A tie in a discrete table means the optimum is between the rows.** Third occurrence — solve the continuous problem.
4. **⚠️ $MR = P(1-1/e)$.** Learn it: it links revenue, elasticity and market power in one expression.
5. **⚠️ A price-setting firm always operates where $e>1$.** An estimate below 1 means an error somewhere.
6. **The monopolist's profit is a transfer; only the triangle is deadweight.** Do not conflate them in a policy argument.
7. **⚠️ A monopolist has no supply curve.** Questions phrased in supply-and-demand terms have no answer.
8. **Marginal-cost pricing bankrupts a natural monopoly** ($MC <$ ATC while ATC falls) — which is why regulation is hard.
9. **⚠️ Perfect price discrimination is efficient and takes all the surplus.** State which welfare measure you mean.
10. **Discrimination requires market power, segmentation, and no resale.** Missing any one kills it.
11. **Imperfect discrimination expands output** — cheap seats exist because expensive ones do.
12. **⚠️ Cartels collapse from within.** Each member gains by cheating at the agreed quantity.
13. **Repetition sustains collusion**; one-shot games do not. Expect collusion in stable, concentrated, long-lived markets.
14. **⚠️ Cournot oligopoly and the tragedy of the commons are the same equilibrium.** The verdict differs only in who bears the externality.
15. **Ask whose surplus an externality lands on** before calling an equilibrium good or bad.
16. **Market structure is a spectrum in $N$**, not three boxes.
17. **⚠️ Monopolistic competition has no clean policy conclusion.** Business-stealing and product-variety externalities offset, and the theory does not say by how much.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located all three chapters** *(Micro 6e, PDF pp. 325–398 — ch. 15 pp. 325–354, ch. 16 pp. 355–374, ch. 17 pp. 375–398)*. **Per the deduplication rule in [[00-Index]], micro chapters 10–22 come from the Micro 6e volume.**
>
> **⚠️ TABLE 1 (the monopoly revenue schedule) SURVIVED COMPLETELY** — all five columns and nine rows. **This is the second Mankiw table in this subject to extract whole** *(after [[05 - Production Costs and Competitive Markets|ch. 05]]'s cost table)*, further confirming that **numeric tables set as text survive while diagrams do not.**
>
> **The ch. 17 demand schedule for the Jack and Jill example did *not* extract as a table**, but the prose states two of its points explicitly (10 gallons → \$110, 20 → \$100), **which determines the linear demand curve $P = 120 - Q$** — and that reproduces the competitive quantity of 120 gallons the prose also states. **The reconstruction is therefore verified against the source rather than assumed.**
>
> **⚠️ THE OPERATOR CIPHER applies** — see [[00-Index]]. Nothing was transcribed. *(Table 1's header shows the cipher clearly: `TR ∙ P ∙ Q` and `MR ∙ ΔTR / ΔQ`, where `∙` stands for `=` and `×`.)*
>
> **⚠️ Every figure is lost, and this chapter is unusually diagram-dependent.** **The monopoly diagram (demand, MR, MC, ATC with the profit rectangle and DWL triangle), the natural-monopoly cost curve, the price-discrimination panels, and the monopolistic-competition tangency diagram are all images.** The tangency condition in §7 is *only* ever shown as a picture in the source — **so it is stated algebraically here ($P = ATC$ and $P > MC$ simultaneously, forcing production on the falling branch of ATC).**
>
> **No erratum.** Every value Mankiw tabulates or states reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §2's derivation of $MR = P(1-1/e)$ is mine and is the chapter's main unification.** Mankiw gives the output/price-effect intuition and never writes the relation. **It shows ch. 02's "revenue peaks at $e=1$" and this chapter's "revenue peaks at $MR=0$" are one statement**, and yields **the result that a monopolist never operates on the inelastic branch** — which Mankiw does not state anywhere.
> - **§1's identification of the third discrete tie**, and the general rule that a tie signals an interior optimum, is mine *(established in [[02 - Supply, Demand and Elasticity|ch. 02]] and [[05 - Production Costs and Competitive Markets|ch. 05]])*.
> - **§3's observation that a monopolist has no supply curve** is standard intermediate material that Mankiw omits; it is included because it explains why [[02 - Supply, Demand and Elasticity|ch. 02]]'s apparatus stops applying.
> - **⚠️ §4's identification of perfect price discrimination as the *fourth* appearance of the efficiency/distribution split is mine.** Mankiw notes that perfect discrimination is efficient and raises total surplus; **he does not connect it to the tax-incidence or Coase results.**
> - **⚠️ §6 is the chapter's strongest finding and is entirely mine.** **Mankiw presents the duopoly arithmetically and the commons narratively, two chapters apart, and never notices they are the same equilibrium.** The $N$-firm Cournot solution, the demonstration that **the percentages are identical to ch. 04's at every matching $N$**, and the conclusion that **the welfare verdict comes from outside the model** are additions.
> - **§5's explicit deviation table** (cheating from 30 to 40 raising profit \$1 800 → \$2 000) is computed; Mankiw argues it in prose.
> - **§7's algebraic statement of the tangency condition** — since the diagram is lost — and the framing that monopolistic competition combines "monopoly's inefficiency with competition's zero profit" are mine.
>
> **Deliberately compressed.** **Mankiw ch. 15's case studies** (drug patents, the diamond market, the Microsoft antitrust case) illustrate the barriers-to-entry taxonomy and are represented by it. **The detailed treatment of natural-monopoly regulation** (average-cost pricing, rate-of-return regulation and its incentive problems) is compressed to §3's note; it is a public-utilities topic. **Ch. 16's advertising and brand-name debate** is noted in §7's ambiguity discussion rather than developed — the arguments are qualitative and unresolved. **Ch. 17's game-theory section** beyond the prisoners' dilemma (the arms race, common-resources and advertising games, and the tit-for-tat tournament) is compressed to §6's repetition note, since all are instances of the same dilemma. **The antitrust controversies** (resale price maintenance, predatory pricing, tying) are summarised in §6's note; each turns on facts rather than theory.

**Previous:** [[05 - Production Costs and Competitive Markets]] · **Next:** [[07 - Factor Markets and the Theory of Consumer Choice]]
