---
subject: Macroeconomics & Microeconomics
chapter: 1
tags: [ds, economics, microeconomics, opportunity-cost, comparative-advantage, ppf, marginal-analysis]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 1–3"
---

# Ten Principles, Thinking Like an Economist, and Comparative Advantage

**Economics is the study of how society manages scarce resources.** Scarcity is the whole premise: if nothing were scarce there would be no trade-offs, and with no trade-offs there is nothing to decide.

**The chapter's result is that trade creates value out of nothing.** *(Computed: Frank and Ruby, working the same hours with the same skills and the same technology, produce **2 more ounces of meat and 4 more ounces of potatoes** simply by reallocating who does what. Both then end up with more of **both** goods.)*

**And the reason is counterintuitive.** Ruby is faster at *both* jobs — she has an **absolute advantage** in everything — and it makes no difference whatsoever. *(Computed: multiplying Ruby's productivity by 2, 5 or 10 leaves the trade pattern **exactly unchanged**, because an opportunity cost is a **ratio** of two times and the scale factor cancels.)*

**§3 does what Mankiw explicitly declines to do.** The book says the price at which trade occurs is "beyond the scope of this chapter". *(Computed: the total gain is a constant **10 ounces of potatoes at every price in the feasible range** — the price does not create or destroy value, it only divides it.)*

> [!warning] ⚠️ Every equation here was reconstructed, not transcribed
> The source's arithmetic operators extract as digits (`5`→`=`, `1`→`+`, `2`→`−`, `3`→`×`). **See the cipher table in [[00-Index]] before opening the PDF.**

## 📘 Main Knowledge

### 1. The ten principles

**How people make decisions**

1. **People face trade-offs.** *"There is no such thing as a free lunch."* The classic is efficiency vs equality — policies that redistribute the pie usually shrink it.
2. **The cost of something is what you give up to get it** — **opportunity cost**, and §2 shows it is the load-bearing idea of the whole chapter.
3. **Rational people think at the margin.** Compare the *marginal* benefit to the *marginal* cost, never the average.
4. **People respond to incentives.** Change the payoff and behaviour changes — often in ways the policy did not intend.

**How people interact**

5. **Trade can make everyone better off.** *(§2 computes it.)*
6. **Markets are usually a good way to organise economic activity** — Adam Smith's invisible hand.
7. **Governments can sometimes improve market outcomes** — when there is **market failure** ([[04 - Externalities, Public Goods and Common Resources|ch. 04]]) or a distributional objective.

**How the economy as a whole works**

8. **A country's standard of living depends on its ability to produce goods and services** — productivity ([[09 - Production and Growth|ch. 09]]).
9. **Prices rise when the government prints too much money** ([[12 - The Monetary System and Inflation|ch. 12]]).
10. **Society faces a short-run trade-off between inflation and unemployment** ([[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]]).

> [!note] Principle 3 is a derivative, and Mankiw never says so
> **"Think at the margin" means: compare $\dfrac{d(\text{benefit})}{dx}$ with $\dfrac{d(\text{cost})}{dx}$, and act if the first exceeds the second.**
>
> **That single instruction generates most of the results in this subject** — $P = MC$ for a competitive firm ([[05 - Production Costs and Competitive Markets|ch. 05]]), $MR = MC$ for a monopolist ([[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]), hire until the marginal revenue product equals the wage ([[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]).
>
> **Mankiw is deliberately calculus-free and states this in words for 800 pages.** Recognising it as [[Calculus/contents/00-Index|differentiation]] makes the whole subject shorter, not longer. *(Labelled as an addition — see the gaps callout.)*
>
> **The practical form worth remembering: sunk costs are irrelevant.** A cost that does not change with the decision has a marginal value of zero, so it drops out of the derivative. **Average cost includes it; marginal cost does not** — which is why decisions made on average cost are wrong.

### 2. Thinking like an economist

**Economists use models — deliberate simplifications.** Mankiw's two are the **circular-flow diagram** and the **production possibilities frontier**.

| | |
|---|---|
| **positive statements** | claims about *how the world is* — testable |
| **normative statements** | claims about *how the world ought to be* — not testable |

> [!note] Why economists appear to disagree more than they do
> **Mankiw's explanation is that disagreements are of two kinds** — differing *positive* judgements about how the world works (testable in principle, hard in practice) and differing *normative* values (not resolvable by evidence at all).
>
> **The distinction matters for anyone who works with data**: an argument that looks empirical is often normative underneath, and no amount of estimation will settle it. **[[Econometrics/contents/00-Index|Econometrics]] can decide the first kind and cannot touch the second.**

### 3. The production possibilities frontier

**The PPF shows the combinations of two goods an economy can produce with its available resources.** Points *on* it are efficient; points *inside* are wasteful; points *outside* are unattainable.

*(Computed — Frank and Ruby each work 480 minutes a day:)*

| producer | min/oz meat | min/oz potatoes | **max meat** | **max potatoes** |
|---|---|---|---|---|
| **Frank** | 60 | 15 | **8** | **32** |
| **Ruby** | 20 | 10 | **24** | **48** |

**Ruby is faster at both.** She has an **absolute advantage** — the ability to produce a good using fewer inputs — **in both goods.**

> [!note] The PPF is a constraint, and its slope is the opportunity cost
> **Frank's frontier is $60M + 15P = 480$, i.e. $M = 8 - P/4$, so $\dfrac{dM}{dP} = -\tfrac14$.**
> **Ruby's is $20M + 10P = 480$, i.e. $M = 24 - P/2$, so $\dfrac{dM}{dP} = -\tfrac12$.**
>
> **The opportunity cost *is* the derivative of the frontier.** *(Verified against the intercepts above.)*
>
> **These frontiers are straight lines because each producer's productivity is constant** — the cost of a potato does not depend on how many are already grown. **A bowed-out PPF is one whose slope steepens**, i.e. rising opportunity cost, which is **diminishing marginal product seen from the output side** ([[05 - Production Costs and Competitive Markets|ch. 05]]).

### 4. ⚠️ Opportunity cost and comparative advantage

$$\text{opportunity cost of 1 oz of }X=\frac{\text{time for }X}{\text{time for the other good}}$$

*(Verified against Mankiw's Table 1:)*

| producer | 1 oz **meat** costs | 1 oz **potatoes** costs |
|---|---|---|
| **Frank** | 4 oz potatoes | **¼ oz meat** |
| **Ruby** | **2 oz potatoes** | ½ oz meat |

**Comparative advantage** is the ability to produce a good at a *lower opportunity cost*. **Frank has it in potatoes (¼ < ½); Ruby has it in meat (2 < 4).**

> [!warning] Nobody can have a comparative advantage in both goods
> **The two columns are reciprocals of each other** — if one good costs you a lot, the other necessarily costs you little. So **a high opportunity cost in one good forces a low one in the other**, and comparative advantage is always split.
>
> **This is why "we're worse at everything" is never an argument against trade.** It cannot be true in the sense that matters.

### 5. ⚠️ The gains, computed

*(Verified end to end against Mankiw's Figure 2:)*

**Without trade** — each splits the day evenly:

| | meat | potatoes |
|---|---|---|
| Frank | 4 | 16 |
| Ruby | 12 | 24 |
| **total** | **16** ✓ | **40** ✓ |

**With specialisation** — Frank grows only potatoes; Ruby splits her day 360 min meat / 120 min potatoes *(verified: sums to 480)*:

| | meat | potatoes |
|---|---|---|
| Frank | 0 | 32 |
| Ruby | 18 | 12 |
| **total** | **18** ✓ | **44** ✓ |

> [!warning] Specialisation created 2 oz of meat and 4 oz of potatoes out of nothing
> **Same two people, same hours, same technology, same skills. Only the *allocation* changed.**
>
> **This is the single most important idea in the chapter**, and it is why economists are near-unanimous about the gains from trade in a way they are about almost nothing else.

**Then they trade — Frank gives 15 oz potatoes for 5 oz meat:**

| | meat before → after | potatoes before → after | **gain** |
|---|---|---|---|
| **Frank** | 4 → **5** | 16 → **17** | **+1 meat, +1 potatoes** |
| **Ruby** | 12 → **13** | 24 → **27** | **+1 meat, +3 potatoes** |

**Both end up with more of *both* goods, and nobody gave anything up.** *(And it is not a trick: the gains sum to exactly the 2 meat and 4 potatoes that specialisation created.)*

### 6. ⚠️ The price — which Mankiw declines to determine

**The book states only that the price must lie between the two opportunity costs — between 2 and 4 oz of potatoes per oz of meat — and says the rest is "beyond the scope of this chapter."**

*(Computed — Frank buys 5 oz of meat at a price of $P$ oz of potatoes each:)*

| $P$ | Frank's surplus | Ruby's surplus | **total** | |
|---|---|---|---|---|
| **2.0** | 10.0 | **0.0** | **10.0** | Ruby gains nothing |
| 2.5 | 7.5 | 2.5 | **10.0** | |
| **3.0** | 5.0 | 5.0 | **10.0** | **Mankiw's deal — an even split** |
| 3.5 | 2.5 | 7.5 | **10.0** | |
| **4.0** | **0.0** | 10.0 | **10.0** | Frank gains nothing |

> [!warning] The total gain is constant at 10 oz of potatoes, whatever the price
> **The price does not create or destroy value. It only divides it.**
>
> **That is why the range is $[2,4]$:** below 2, Ruby would rather keep her meat than sell it that cheaply; above 4, Frank would rather grow his own. **Outside the range one party is worse off than not trading, and refuses.**
>
> **Mankiw's $P=3$ is the midpoint, so his two parties split the gain evenly — but that is a choice of example, not a result.** Nothing in the theory of comparative advantage picks a point in the interval.
>
> **So: comparative advantage determines *whether* there are gains and *who* specialises. It says nothing about *who captures them*.** The split is bargaining power, and that is precisely why the book defers it. **A great many disputes about trade are about the split, not the gains** — and the theory that establishes the gains is silent on the question being argued about.

### 7. ⚠️ Absolute advantage is irrelevant — proved by scaling

**Mankiw asserts that gains rest on comparative rather than absolute advantage. It can be demonstrated.**

*(Computed — multiply *both* of Ruby's productivities by $k$:)*

| $k$ | Ruby's min/oz (meat, potatoes) | Ruby's opportunity costs | trade pattern |
|---|---|---|---|
| 1 | (20.00, 10.00) | meat = 2 pot, pot = ½ meat | Frank → potatoes, Ruby → meat |
| 2 | (10.00, 5.00) | meat = 2 pot, pot = ½ meat | **unchanged** |
| 5 | (4.00, 2.00) | meat = 2 pot, pot = ½ meat | **unchanged** |
| 10 | (2.00, 1.00) | meat = 2 pot, pot = ½ meat | **unchanged** |

**Because an opportunity cost is a *ratio* of two times, $k$ cancels exactly.**

**The only thing that changes the trade pattern is changing the *ratio*:**

| Ruby's min/oz meat | her opp. cost of potatoes | vs Frank's ¼ | who grows potatoes? |
|---|---|---|---|
| 20 | ½ | > | **Frank** |
| **40** | **¼** | **=** | **neither — the gains vanish entirely** |
| 45 | 2/9 | < | **Ruby** |
| 60 | 1/6 | < | **Ruby** |

> [!warning] Difference is the source of the gain — not skill, not wealth, not productivity
> **At 40 minutes per ounce of meat the two have identical opportunity costs and there is nothing to gain from trading at all.** Not a small gain — *zero*.
>
> **So a country that is worse at everything still has a comparative advantage in something**, and two countries that are *equally good at everything in the same proportions* have nothing to trade however skilled they both are.
>
> **This is the result that makes the theory politically counterintuitive and analytically robust.**

### 8. The same structure, already met in this vault

**[[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|Commercial Banking ch. 09]] verified an interest-rate swap:**

| | fixed | floating |
|---|---|---|
| low-rated borrower | 11.50% | prime + 1.75% |
| high-rated borrower | **9.00%** | **prime + 0.00%** |
| **quality spread** | **2.50%** | **1.75%** |

$$\text{total gain}=2.50\%-1.75\%=\mathbf{0.75\%}$$

> [!note] The swap is comparative advantage in a finance costume
> **The high-rated borrower can borrow more cheaply in *both* markets — an absolute advantage in everything, exactly like Ruby.** And exactly like Ruby, it makes no difference.
>
> **The gain exists because the advantage is *bigger* in one market than the other** (2.50% vs 1.75%) — a difference of ratios, precisely as here. **Equalise the two spreads and the gain is zero**, exactly as equalising the opportunity costs in §7 killed it.
>
> **And the split — 0.50% to one party, 0.25% to the other — is bargaining, not theory**, the same indeterminacy as §6.
>
> **Neither book mentions the other.** Recognising them as one result is worth more than either alone. *(This is my cross-link — see the gaps callout.)*

## ✏️ Exercises

**1. (Opportunity cost and the PPF.)** (a) Define opportunity cost and compute it for both producers. (b) Why is the PPF a straight line here? (c) What does its slope mean? (d) Why can't anyone have a comparative advantage in both goods?

> [!example]- Solution
> **(a) What you give up to get something — measured as a ratio of production times.**
>
> $$\text{opp. cost of 1 oz of }X=\frac{\text{minutes for }X}{\text{minutes for the other good}}$$
>
> *(Verified against Mankiw's Table 1: **Frank** — 1 oz meat costs **4 oz potatoes**, 1 oz potatoes costs **¼ oz meat**; **Ruby** — 1 oz meat costs **2 oz potatoes**, 1 oz potatoes costs **½ oz meat**.)*
>
> **The intuition: spending 15 minutes growing a potato is 15 minutes not spent on meat, and Frank needs 60 minutes per ounce of meat — so a potato costs him 15/60 = ¼ ounce of meat.**
>
> **Note that opportunity cost is not a money price and need not involve money at all.** It is the *best forgone alternative*, which is why it is the correct cost concept for any decision — including ones with no market.
>
> **(b) Because each producer's productivity is constant.**
>
> Frank always needs 15 minutes per potato, whether it is his first or his thirty-second. **So the rate at which he converts meat into potatoes never changes, and the frontier is linear.**
>
> **A bowed-out (concave) PPF arises when resources are not equally suited to both uses** — moving the first workers from meat to potatoes is cheap, moving the last is expensive. **That is rising opportunity cost, which is diminishing marginal product viewed from the output side** ([[05 - Production Costs and Competitive Markets|ch. 05]]).
>
> **Real economies have bowed-out frontiers; Mankiw uses lines here to make the trade arithmetic clean.**
>
> **(c) The slope *is* the opportunity cost.**
>
> $$\text{Frank: }60M+15P=480\;\Rightarrow\;M=8-\tfrac{P}{4}\;\Rightarrow\;\frac{dM}{dP}=-\tfrac14$$
> $$\text{Ruby: }20M+10P=480\;\Rightarrow\;M=24-\tfrac{P}{2}\;\Rightarrow\;\frac{dM}{dP}=-\tfrac12$$
>
> *(Verified against the intercepts: Frank 8 meat / 32 potatoes, Ruby 24 meat / 48 potatoes.)*
>
> **So "opportunity cost" and "slope of the constraint" are the same object**, and this is where the subject connects to [[Calculus/contents/00-Index|Calculus]] and to [[Optimization/contents/00-Index|constrained optimisation]] — the PPF is a budget constraint in production space. **Mankiw never writes the derivative.**
>
> **(d) Because the two opportunity costs are reciprocals.**
>
> $$\text{opp. cost of meat}=\frac{1}{\text{opp. cost of potatoes}}$$
>
> **If your opportunity cost of one good is high, your opportunity cost of the other is *necessarily* low.** So comparing two producers, whoever has the lower cost in one good must have the higher cost in the other.
>
> **The only exception is a tie** — if both producers have identical ratios, neither has a comparative advantage in anything, and §7 shows the gains from trade are then exactly zero.
>
> **This is why "we are worse at everything, so we cannot compete" is not a coherent position.** It confuses absolute with comparative advantage, and only the latter determines what you should do.

**2. (Hard — the gains and the price.)** (a) Compute the gains from specialisation. (b) Where do they come from? (c) What determines the price, and what does the theory *not* say? (d) Why is absolute advantage irrelevant?

> [!example]- Solution
> **(a) Two extra ounces of meat and four extra ounces of potatoes.**
>
> *(Verified against Mankiw's Figure 2: without trade, totals of **16 meat and 40 potatoes**; with specialisation, **18 meat and 44 potatoes**.)*
>
> **After trading 15 oz of potatoes for 5 oz of meat:**
>
> | | meat | potatoes |
> |---|---|---|
> | Frank | 4 → **5** | 16 → **17** |
> | Ruby | 12 → **13** | 24 → **27** |
>
> **Both have more of both goods.** The individual gains (+1/+1 and +1/+3) sum to exactly the +2 meat and +4 potatoes that specialisation created.
>
> **(b) From reallocation, not from production of anything new.**
>
> **Nobody worked harder, learned a skill, or bought a machine.** The same 960 person-minutes produced more because each minute was spent where it was worth most.
>
> **The mechanism: before trade, Frank was spending half his day on meat — a task at which his opportunity cost is 4 potatoes per ounce, the highest in the economy.** Moving that time to potatoes converts a high-cost activity into a low-cost one. **The gain is the difference between the opportunity costs, multiplied by the quantity reallocated.**
>
> **This is why the gain vanishes when the opportunity costs are equal (§7): there is no difference left to exploit.**
>
> **(c) The price must lie between the two opportunity costs — and the theory says nothing more.**
>
> *(Computed: the total gain is **10 oz of potatoes at every price in [2, 4]**. At $P=2$ Ruby captures nothing; at $P=4$ Frank captures nothing; at Mankiw's $P=3$ they split it evenly.)*
>
> **Why the bounds:** below 2, Ruby does better keeping her meat and growing her own potatoes; above 4, Frank does better growing potatoes and making his own meat. **Outside the range, one party prefers autarky and there is no deal.**
>
> **Why the total is constant:** the gain from trade is created by *specialisation*, which has already happened before any price is quoted. **The price is purely distributive** — it moves surplus between the parties without changing how much there is.
>
> **What the theory does not say: who gets it.** Mankiw's even split at $P=3$ is an arbitrary choice of example. **The determination requires bargaining theory or a market with many participants**, which is why the book defers it — honestly.
>
> **This distinction is worth carrying into any argument about trade.** The claim "trade makes both countries better off" is about the *total* and is very robust. The claim "trade makes *everyone* better off" is about the *split* and does not follow — **the gains are real and their distribution is a separate question the theory does not answer.**
>
> **(d) Because opportunity cost is a ratio, and scaling cancels.**
>
> *(Computed: multiplying **both** of Ruby's productivities by $k = 2, 5, 10$ leaves her opportunity costs at exactly 2 and ½ — **the trade pattern never changes.**)*
>
> $$\frac{20/k}{10/k}=\frac{20}{10}=2\quad\text{for every }k$$
>
> **So absolute advantage can be made arbitrarily large in either direction without altering who should specialise in what.**
>
> **What *does* matter is the ratio** *(computed: holding Ruby's potato time at 10 min and varying her meat time)*:
>
> | Ruby's min/oz meat | her opp. cost of potatoes | who grows potatoes? |
> |---|---|---|
> | 20 | ½ | Frank |
> | **40** | **¼ — identical to Frank's** | **nobody: gains are zero** |
> | 60 | 1/6 | **Ruby** |
>
> **Difference is the source of gain.** Not skill, not wealth, not absolute productivity — **difference**. Two equally-proportioned economies have nothing to trade however capable they are, and two very unequal ones have a great deal to trade however far apart they are.
>
> **And [[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|Commercial Banking ch. 09]]'s swap is the same result**: the high-rated borrower is cheaper in *both* markets, and the entire gain comes from its advantage being **bigger in one than the other** (2.50% vs 1.75%). **Equalise the spreads and the swap creates nothing** — the exact analogue of the 40-minute row above.

**3. (Principles and method.)** (a) What does "think at the margin" mean formally? (b) Why are sunk costs irrelevant? (c) Positive vs normative — why does it matter for data work?

> [!example]- Solution
> **(a) Compare derivatives, not totals or averages.**
>
> **Act if $\dfrac{d(\text{benefit})}{dx} > \dfrac{d(\text{cost})}{dx}$, and stop where they are equal.**
>
> **That instruction generates most of this subject's results**: $P = MC$ for a competitive firm, $MR = MC$ for a monopolist, hire until marginal revenue product equals the wage, consume until the marginal utility per dollar is equal across goods.
>
> **They are all the same first-order condition applied to different objective functions** — which is [[Optimization/contents/00-Index|Optimization]] ch. 11's constrained optimisation, and it is why the subject is far more unified than a calculus-free presentation makes it look.
>
> **(b) Because a cost that does not vary with the decision differentiates to zero.**
>
> **If a cost is the same whichever option you choose, it appears identically in both branches and cancels.** Formally, it is a constant in the objective function, and $\frac{d}{dx}(\text{constant}) = 0$.
>
> **The practical consequence is the one people get wrong: money already spent should have no influence on what to do next.** Continuing a failing project "because we have already invested so much" is exactly the error — **the investment is gone under every option, so it cannot distinguish between them.**
>
> **And note the connection to (a):** average cost *includes* the sunk component and marginal cost does not. **Decisions made on average cost are systematically wrong**, which is a recurring theme in [[05 - Production Costs and Competitive Markets|ch. 05]].
>
> **(c) Because an argument that looks empirical is often normative underneath.**
>
> | | |
> |---|---|
> | **positive** | how the world *is* — in principle testable |
> | **normative** | how the world *ought to be* — not testable |
>
> **"A minimum wage reduces employment among low-skilled workers" is positive** — hard to establish, but data can bear on it. **"A minimum wage should be raised" is normative** and no dataset settles it, because it depends on how you weigh the gains to those who keep their jobs against the losses to those who do not.
>
> **For anyone doing applied work this is the most useful distinction in the chapter.** [[Econometrics/contents/00-Index|Econometrics]] can decide the first kind of question and cannot touch the second, and **a great deal of apparent disagreement about evidence is actually disagreement about values wearing an empirical costume.**
>
> **Mankiw's own framing is that economists disagree for both reasons** — differing positive judgements about how the world works, and differing normative values. **Separating the two before arguing is most of the work.**

## 📝 Summary

- **Economics is about scarcity**, and scarcity means trade-offs. The ten principles organise the subject at three scales: how people decide, how they interact, how the economy works as a whole.
- **⚠️ "Rational people think at the margin" is differentiation** — compare $d(\text{benefit})/dx$ to $d(\text{cost})/dx$. **Mankiw states this in words for the whole book and never writes a derivative.**
- **Sunk costs are irrelevant because a constant differentiates to zero.** Average cost includes them; marginal cost does not — which is why decisions made on average cost are wrong.
- **Positive statements are testable; normative ones are not.** [[Econometrics/contents/00-Index|Econometrics]] can settle the first kind only, and much apparent disagreement about evidence is disagreement about values.
- **The PPF is a constraint and ⚠️ its slope is the opportunity cost** *(verified: Frank $M = 8 - P/4$, slope $-\tfrac14$; Ruby $M = 24 - P/2$, slope $-\tfrac12$)*. **Straight because productivity is constant; a bowed-out frontier is rising opportunity cost, i.e. diminishing marginal product.**
- **Absolute advantage** = fewer inputs. **Comparative advantage** = lower opportunity cost. *(Verified against Table 1: Frank ¼ oz meat per potato vs Ruby's ½; Ruby 2 oz potatoes per meat vs Frank's 4.)*
- **⚠️ Nobody can have a comparative advantage in both goods**, because the two opportunity costs are reciprocals.
- **⚠️ Specialisation created 2 oz of meat and 4 oz of potatoes out of nothing** *(verified: totals 16→18 and 40→44)*. **Same people, same hours, same technology — only the allocation changed.**
- **After trade both parties have more of *both* goods** *(computed: Frank +1/+1, Ruby +1/+3, summing exactly to what specialisation created)*.
- **⚠️ The price must lie between the two opportunity costs, and the total gain is constant at 10 oz across the whole range** *(computed)*. **The price does not create value — it only divides it.**
- **So comparative advantage says *whether* there are gains and *who* specialises, and nothing about *who captures them*.** Mankiw's even split is a choice of example. **"Trade raises the total" is robust; "trade helps everyone" does not follow.**
- **⚠️ Absolute advantage is irrelevant, proved by scaling** *(computed: multiplying both of Ruby's productivities by 2, 5 or 10 leaves the trade pattern exactly unchanged, because $k$ cancels from a ratio)*.
- **⚠️ Difference is the source of the gain.** *(Computed: at 40 min/oz meat the two have identical opportunity costs and **the gains from trade are exactly zero**.)* Not skill, not wealth — difference.
- **[[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|Commercial Banking ch. 09]]'s interest-rate swap is this result in a finance costume**: the high-rated borrower is cheaper in *both* markets, the **0.75%** gain comes entirely from the spread difference (2.50% vs 1.75%), and equalising the spreads destroys it.

## ⚠️ Important Notes

1. **Opportunity cost is the *best forgone alternative*, not a money price.** It applies to decisions with no market at all.
2. **⚠️ Compute opportunity cost as a ratio of the two production times** — and check that the two goods' costs are reciprocals.
3. **⚠️ Absolute advantage tells you nothing about who should specialise.** Compare ratios, never levels.
4. **A producer worse at everything still has a comparative advantage in something.** It is arithmetically forced.
5. **⚠️ Equal opportunity costs ⇒ zero gains from trade.** Difference is the entire source.
6. **The gains come from reallocation, not from new resources.** Nothing is produced that was not possible before.
7. **⚠️ The price is distributive only.** It moves surplus between parties; it does not change the total.
8. **The feasible price range is bounded by the two opportunity costs** — outside it, someone prefers autarky.
9. **⚠️ "Trade raises the total" and "trade helps everyone" are different claims.** The theory supports only the first.
10. **The slope of the PPF is the opportunity cost** — and a bowed-out PPF means it rises with quantity.
11. **⚠️ Think at the margin: compare derivatives, not averages or totals.**
12. **Sunk costs drop out of every decision** because they differentiate to zero.
13. **Separate positive from normative before arguing.** No dataset settles a normative question.
14. **Models are deliberately false.** Judge them by what they predict, not by their realism.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline is excellent** — chapters and sections locate precisely, so extraction is targeted. *(Macro 2017, PDF pp. 34–93 for chs. 1–3.)*
>
> **⚠️ THE OPERATOR CIPHER is the dominant hazard and it affects every equation in the book**: `5`→`=`, `1`→`+`, `2`→`−`, `3`→`×`, **context-dependent**. **No formula in this note was transcribed** — each was reconstructed from the surrounding prose and then verified against the book's own worked arithmetic. **See [[00-Index]] for the full cipher table and the worked decoding examples.**
>
> **⚠️ Every figure is lost**, which is severe here: **Figure 1 (the two production possibilities frontiers) and Figure 2 (the gains from trade) are the chapter's core exposition** and both are images. What survives is captions and stray axis labels.
>
> **This is why §§3–5 recompute the entire example from the stated minute-per-ounce inputs rather than reading it off the figures** — and the recomputation reproduces every figure the prose states (16/40 without trade, 18/44 with, the Table 1 opportunity costs, and the individual gains). **The reconstruction is therefore verified, not assumed.**
>
> **Also lost:** Mankiw's circular-flow diagram (ch. 2) and the bowed-out PPF used to illustrate rising opportunity cost. **Both are described in words here**; the bowed-out case is treated analytically in §3's note rather than pictorially.
>
> **Minor faults observed:** `today's` → `todayrs`; the fraction `1/3` extracts as `1/1/1 3/3/`; short phrases occasionally duplicate.
>
> **No erratum.** Every figure Mankiw states in prose reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §6 is the chapter's main addition.** **Mankiw explicitly declines to determine the price** ("the precise answers to these questions are beyond the scope of this chapter"). **Computing the surplus split across the whole feasible range — and showing the total is constant at 10 oz — establishes that the price is purely distributive**, which is not in the source and which sharpens what the theory does and does not claim.
> - **⚠️ §7's scaling proof is mine.** Mankiw *asserts* that gains rest on comparative rather than absolute advantage; **multiplying both of Ruby's productivities by $k$ and showing the ratio is invariant proves it**, and the second table — finding the exact point (40 min/oz) at which the gains vanish — shows that **difference, not ability, is the source.**
> - **§3's derivation of the PPF slope as $dM/dP$**, and the identification of a bowed-out frontier as diminishing marginal product, are additions — **Mankiw is deliberately calculus-free.** Likewise §1's note that Principle 3 *is* differentiation and that sunk costs are irrelevant *because* constants differentiate to zero.
> - **⚠️ §8's identification of [[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|Commercial Banking ch. 09]]'s interest-rate swap as comparative advantage** is my cross-subject link. **Neither book mentions the other**, and the structural match is exact: absolute advantage in both markets, a gain arising purely from the difference of spreads, and an indeterminate split.
> - **The framing that "trade raises the total" and "trade helps everyone" are different claims** — the first supported by the theory, the second not — is mine.
>
> **Deliberately compressed.** **Mankiw ch. 1's extended discussion of each principle** (the efficiency–equality trade-off, incentive case studies, the invisible hand) is compressed to the statements plus the analytical content; the case studies are illustrations rather than results. **Ch. 2's circular-flow diagram** is described but not reconstructed — it is an accounting identity that [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]] states properly as $Y = C + I + G + NX$. **Ch. 2's appendix on graphing** is omitted as prerequisite material. **The "economist as policy adviser" material and the FYI boxes on why economists disagree** are compressed into §2's note. **Ch. 3's applications to international trade** are deferred to [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]], which owns the surplus apparatus needed to evaluate tariffs.

**Previous:** [[00-Index]] · **Next:** [[02 - Supply, Demand and Elasticity]]
