---
subject: Commercial Banking
chapter: 11
tags: [ds, banking, lending, credit-risk, six-cs, loan-pricing, raroc, credit-rationing, concentration]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 16–17"
---

# Lending: Policy, Credit Risk and Business Loans

**Loans are what a bank is for.** [[03 - Bank Financial Statements|Ch. 03]] showed them as the dominant asset; [[10 - Capital Adequacy and Basel|ch. 10]] gave them a 100% risk weight. **This chapter is how they are decided and priced.**

**Two results go beyond the source, and one of them is R&H's own.**

**§5 — the book puts its best insight in a footnote and never computes it.** Footnote 6 on p. 579 observes that charging a high-risk borrower the full risk premium "may *increase* the chances a borrower will default". *(Computed: the expected return is **humped, not increasing** — it peaks at a **18.00%** loan rate and falls thereafter.)* **Beyond that point the lender earns less by charging more, because the rate itself creates the default.** The correct response is not a higher price but a **refusal** — which is why lenders ration credit rather than simply repricing it.

**§6 — the six Cs are all borrower-level, and a loan book can fail without any of them being violated.** *(Computed: 500 loans each with a 2% default probability — the **mean loss is 2.00% at every correlation**, while the 99th-percentile loss goes **3.60% → 17.60%** and the probability of wiping out 9% equity goes **0.0000% → 4.3770%.**)* **That is [[06 - Hedging with Derivatives|ch. 06]]'s tranching result on a loan portfolio**, and it is the gap between credit *analysis* and credit *risk management*.

**All of R&H's pricing arithmetic verified.** RAROC is **not in R&H** and is added, because it is what connects pricing to [[10 - Capital Adequacy and Basel|ch. 10]]'s capital.

## 📘 Main Knowledge

### 1. Lending policy and the six Cs

**A written loan policy** states the desired portfolio composition, lending authority limits, documentation requirements, collateral standards, pricing, and — the part §6 shows is decisive — **concentration limits.**

**The six Cs are the borrower-level screen:**

| | question |
|---|---|
| **Character** | Is the purpose clear and the intention to repay serious? |
| **Capacity** | Does the borrower have the *legal authority* to sign? |
| **Cash** | Is there cash flow to service the debt — from earnings, asset sales, or new borrowing? |
| **Collateral** | Are there assets to pledge, and what is their liquidation value? |
| **Conditions** | What are the industry, competitive and macro conditions? |
| **Control** | Does the loan comply with law, policy and documentation standards? |

> [!note] Character and Capacity cannot be bought with basis points
> **"Cash" is the one that decides most loans**, and R&H is right to stress that **cash flow, not profit, services debt** — a profitable firm with its earnings locked in receivables and inventory cannot pay.
>
> **But note what kind of test the six Cs are: a *screen*, not a price adjustment.** A borrower who fails on Character is not offered a higher rate; they are declined. **§5 shows why that is the mathematically correct response**, and §6 shows what the six Cs *cannot* see.

### 2. Pricing: four methods, all verified

**(a) Cost-plus** *(R&H eq. 17-17)* — build the rate from its components:

| component | |
|---|---|
| marginal cost of loanable funds | 5.00% |
| nonfunds operating costs | 2.00% |
| default-risk premium | 2.00% |
| desired profit margin | 1.00% |
| **loan rate** | **10.00%** ✓ |

> [!note] "Marginal" is doing real work here
> **[[09 - Managing Deposits and Nondeposit Funding|Ch. 09]] §4 showed that pricing off *historical average* cost of funds books losses as growth.** Cost-plus is right to specify the **marginal** cost — and R&H's own criticism of the method is that banks rarely know their costs accurately, which is a fair objection to the *other* three components.

**(b) Price leadership** *(eq. 17-18)* — start from a base rate and add markups:

$$\text{loan rate}=\underbrace{6\%}_{\text{prime}}+\underbrace{2\%}_{\text{default risk}}+\underbrace{2\%}_{\text{term risk}}=\mathbf{10.00\%}\;✓$$

**(c) LIBOR-based** *(eq. 17-19)*:

$$0.40\%+0.125\%+0.125\%=\mathbf{0.65\%}\;✓$$

> [!warning] A 0.25% total markup has to cover everything
> **On a top-quality borrower the entire markup over LIBOR is a quarter of a point** — and out of it must come [[09 - Managing Deposits and Nondeposit Funding|ch. 09]]'s funding costs above LIBOR, operating costs, expected loss, *and* [[10 - Capital Adequacy and Basel|ch. 10]]'s capital charge. **§4 computes that a 100%-weighted corporate loan needs a 2.26% gross spread to clear a 12% hurdle.** Large-corporate lending at these margins is not a profitable business on its own; **it is priced as an entry ticket to the relationship**, which is what §3 is about.
>
> *(LIBOR has since been retired in favour of SOFR and other risk-free rates — the mechanics are identical, and the reason for the change is that LIBOR was a survey of estimates rather than a rate of actual transactions.)*

**(d) Below-prime** — large short-term loans priced off money-market rates plus an eighth to a quarter point, so that **the best corporate borrowers pay *less* than prime.** This produced a **two-tier market**: prime-based pricing for small and medium business, money-market pricing for large.

> [!note] A minor inconsistency in R&H's below-prime example, reported but not filed
> **The book borrows fed funds at "4 percent" and prices the loan at "4.50 percent (or 4.25 percent to cover the money market cost of borrowing + 0.25 percent markup)".** *(Computed: 4.00% + 0.25% = **4.25%**, not 4.50%; the 4.50% figure requires a 4.25% funding cost.)*
>
> **The stated fed funds rate and the stated funding component disagree by 25 bp.** This is **not filed as an erratum**: it is minor, it changes nothing about the method, and **a parenthetical of this shape is exactly the construction this PDF garbles.** Recorded as an observation, per [[03 - Bank Financial Statements|ch. 03]]'s rule that own-extraction must be ruled out first — and here it cannot be.

### 3. ⚠️ Prime-plus vs times-prime: a risk transfer disguised as a convention

**Both quote 12% when prime is 10%.** *(Computed across the range:)*

| prime | prime-plus-2 | **1.2 × prime** | difference |
|---|---|---|---|
| 6% | 8.00% | 7.20% | −0.80% |
| **8%** | **10.00%** | **9.60%** | −0.40% |
| **10%** | **12.00%** | **12.00%** | **0.00%** |
| 15% | 17.00% | 18.00% | +1.00% |
| 20% | 22.00% | 24.00% | +2.00% |

*(R&H's two checks both verify: prime 10 → 15 gives 17% vs 18%; prime 10 → 8 gives 10% vs 9.6%.)*

> [!warning] The formulas agree at exactly one point and nowhere else
> *(Computed: $p+0.02=1.2p$ only at $p=\mathbf{10.00\%}$ — the rate at which they were quoted.)*
>
> **Times-prime has a beta of 1.2 to the base rate; prime-plus has a beta of 1.0.** So **the choice between them is a decision about who bears interest-rate risk**, presented to the customer as a quoting convention.
>
> **And the two effects compound badly.** Times-prime gives the lender more revenue when rates rise — **but §5 shows that a higher rate raises the borrower's default probability.** So in a rate spike the lender gets a larger contractual claim on a borrower who is simultaneously less able to pay. **[[06 - Hedging with Derivatives|Ch. 06]]'s wrong-way risk, inside a loan contract.**

### 4. Customer profitability analysis: pricing the relationship

$$\text{return}=\frac{\text{revenues from the whole relationship}-\text{expenses}}{\text{net loanable funds used in excess of the customer's deposits}}$$

*(Verified — R&H's Black Gold case, a \$1.5mn six-month line with a 20% compensating balance:)*

| revenues | | costs | |
|---|---|---|---|
| loan interest (12%, six months) | 90 000 | deposit interest owed (10%) | 15 000 |
| commitment fees (1%) | 15 000 | cost of funds raised | 80 000 |
| deposit management fee | 45 000 | account activity costs | 25 000 |
| funds transfer charges | 5 000 | funds transfer costs | 1 000 |
| trust services and record keeping | 61 000 | loan processing | 3 000 |
| | | record keeping | 1 000 |
| **total** | **216 000** ✓ | **total** | **125 000** ✓ |

$$\text{net loanable funds}=1{,}500{,}000-\underbrace{270{,}000}_{20\%\text{ balance, net of }10\%\text{ reserves}}=\mathbf{1{,}230{,}000}\;✓$$

$$\text{return}=\frac{216{,}000-125{,}000}{1{,}230{,}000}=\mathbf{7.3984\%}\quad\text{(book: 7.4\%)}\;✓$$

> [!note] Loan interest is only 41.7% of the revenue
> *(Computed: interest is 90,000 of 216,000; **the other 58.3% is fees and services.**)*
>
> **The loan is not the product — the relationship is.** A loan priced on its own here would be repriced or declined; priced with the relationship it clears comfortably. **This is why banks fight for the operating account and not just the credit.**
>
> **And the compensating balance does real work.** *(Computed: it cuts the funds the bank must supply by **270,000 — 18% of the line** — and without it the return falls from 7.40% to **6.07%.**)* **A deposit the customer must leave behind is a rate increase that does not appear in the rate.**
>
> **The honest weakness:** CPA requires accurate cost allocation across products, which is the same thing R&H says banks cannot do — so the method is only as good as the transfer-pricing system behind it.

### 5. ⚠️ RAROC — absent from R&H, and it is what links pricing to capital

$$\text{RAROC}=\frac{\text{revenue}-\text{expected loss}-\text{operating costs}}{\textbf{capital allocated to the loan}}$$

**And [[10 - Capital Adequacy and Basel|ch. 10]] says the capital allocated depends on the risk weight.** *(Computed — the same \$5mn loan at a 3.00% gross spread and 0.50% operating cost, 8% capital against risk-weighted assets, 12% hurdle:)*

| borrower | risk weight | expected loss | **capital** | **RAROC** | |
|---|---|---|---|---|---|
| **sovereign / Treasury** | **0%** | 0.00% | **0** | **infinite** | *no discipline at all* |
| bank counterparty | 20% | 0.10% | 80 000 | 150.00% | pass |
| residential mortgage | 50% | 0.25% | 200 000 | 56.25% | pass |
| corporate (unrated) | 100% | 0.80% | 400 000 | **21.25%** | pass |

**The required gross spread to clear a 12% hurdle** *(computed)*: **0.792%** for a bank counterparty, **1.230%** for a mortgage, **2.260%** for a corporate — **and *any* spread for a sovereign.**

> [!warning] Ch. 10's hole arriving in the pricing system
> **A zero risk weight means zero allocated capital, so RAROC is infinite and every such loan passes any hurdle.** The pricing system tells the bank to make **unlimited** zero-weight loans.
>
> **[[10 - Capital Adequacy and Basel|Ch. 10]] §3 showed that a portfolio of government securities has no credit risk and enormous interest-rate risk — and that the capital rule is blind to the second.** Here the *same* blindness propagates into the loan-pricing model, because RAROC inherits its denominator from the capital rule.
>
> **So the two systems that are supposed to discipline risk-taking share one blind spot, and reinforce each other in it.** That is worse than either failing alone: a bank running RAROC diligently and meeting Basel comfortably can be accumulating exactly the exposure neither measures.
>
> **RAROC is nonetheless the right idea** — it is what makes the six Cs quantitative, converting "riskier borrowers should pay more" into *how much* more. **It is the examinable version of risk-based pricing and it is not in R&H**, which stops at cost-plus and CPA.

### 6. ⚠️ Why lenders ration credit instead of repricing

**R&H's footnote 6 (p. 579) contains the chapter's best idea:**

> Charging high-risk borrowers the full risk premium is not always wise. Indeed, such a policy may **increase** the chances a borrower will default … resulting in the lender's earning a return **less** than earned on prime-quality loans.

**The book states it and never computes it.** *(Modelled: default probability rises with the rate charged, $p(r)=p_0+k(r-r_0)$, with $p_0=1\%$ at $r_0=6\%$, $k=1.10$, and loss given default 60%. Expected return $=r(1-p)-p\cdot LGD$.)*

| rate charged | P(default) | **expected return** |
|---|---|---|
| 6% | 1.00% | 5.3400% |
| 10% | 5.40% | 6.2200% |
| 14% | 9.80% | 6.7480% |
| **18%** | **14.20%** | **6.9240%** ← maximum |
| 22% | 18.60% | 6.7480% |
| 28% | 25.20% | 5.8240% |
| 34% | 31.80% | 4.1080% |

> [!warning] The expected return is humped, not increasing
> *(Computed exactly: the optimum is $r^*=\mathbf{18.00\%}$, at a default probability of **14.20%**. At 34% the lender earns **4.11%** — worse than the 5.34% available at 6%.)*
>
> **Beyond $r^*$ the lender earns less by charging more, because the rate itself creates the default.** A borrower paying 34% must take risks that a borrower paying 6% need not.
>
> **So a lender facing a borrower who "needs" a rate above $r^*$ should not raise the rate — it should refuse the loan.** That is **credit rationing**, and R&H notes it in passing: lenders "use both price *and* credit rationing (i.e., denying some loans regardless of price)".
>
> **This is why the six Cs are a screen rather than a pricing input.** *Character* and *Capacity* have no price at which they become acceptable. **The whole apparatus of credit analysis exists because some risks must be declined, not priced** — and the humped curve is the reason.
>
> **It also explains a fact the footnote mentions in passing**: R&H cites research that the prime rate is **asymmetric**, rising more readily than it falls, so bank-dependent borrowers are more vulnerable to the cycle. **A borrower who cannot go to the open market is a borrower for whom the rationing constraint binds.**

### 7. ⚠️ What the six Cs cannot see

**Every one of the six Cs is a question about *one borrower*. None asks what else is in the portfolio.**

*(Computed — 500 loans, each with a 2% default probability and 100% loss given default, against equity of 9% of the book, under a one-factor correlation model:)*

| $\rho$ | **mean loss** | 99th-percentile loss | **P(loss > equity)** |
|---|---|---|---|
| **0.00** | **1.9996%** | 3.6000% | **0.0000%** |
| 0.05 | 1.9953% | 6.2000% | 0.0740% |
| 0.15 | 2.0003% | 10.8000% | 1.8560% |
| **0.30** | **1.9931%** | **17.6000%** | **4.3770%** |

> [!warning] The mean loss is 2% in every row
> **Correlation adds no expected loss at all. It moves the tail** — the 99th percentile, which is what capital must cover, goes from **3.60% to 17.60%**, and the probability of wiping out a 9% equity base goes from **essentially zero to 4.38%.**
>
> **So a bank can hold 500 separate loans, each individually underwritten to the six Cs, each with an impeccable 2% default probability — and fail, because all 500 borrowers are in the same industry.**
>
> **This is [[06 - Hedging with Derivatives|ch. 06]] §10 exactly, on a loan book instead of a securitisation**, and [[02 - Organization, Structure and Market Entry|ch. 02]]'s $\sigma\sqrt{(1+\rho)/2}$ for the third time in this subject. **Three settings, one mathematics: pooling only diversifies what is not already moving together, and the average is always fine.**
>
> **That is the gap between credit *analysis* and credit *risk management*.** Analysis is borrower-by-borrower and the six Cs cover it well. **Risk management is portfolio-level, and nothing in the six Cs reaches it** — which is why lending policy must set **concentration limits by industry, geography and single-borrower exposure**, and why no amount of good underwriting substitutes for them.

### 8. Loan review and workouts

**Loan review** re-examines loans already on the books — larger loans more often, problem loans more often still. **The point is that a loan's quality is not fixed at origination**, and [[03 - Bank Financial Statements|ch. 03]] showed the consequence: the allowance for loan losses depends on management's *estimate*, and a 140% swing in the provision moved net income by **47%**.

**Loan workouts** recover value from a loan already in trouble. R&H's principles are worth keeping because they are counterintuitive:

- **The objective is maximum recovery, not punishment.** Collateral seizure is usually the *worst* outcome for both parties.
- **Move fast** — problems compound and the borrower's other creditors are also moving.
- **Keep the workout function separate from the officer who made the loan**, because the person who approved it is the worst-placed person to admit it has failed.

> [!note] The separation is a structural fix for a predictable bias
> **This is the same reasoning as [[10 - Capital Adequacy and Basel|ch. 10]]'s objection to Basel II's internal models**: do not ask the party with an interest in the answer to produce it. **Here the conflict is at the level of the individual officer**, and the fix is organisational rather than analytical.

## ✏️ Exercises

**1. (Pricing.)** (a) Compare the four methods. (b) What is the difference between prime-plus and times-prime? (c) Interpret the CPA result. (d) What does RAROC add?

> [!example]- Solution
> **(a) They differ in where the rate comes from, and the later ones concede more to the market.**
>
> *(All verified: **cost-plus 5+2+2+1 = 10.00%**; **price leadership 6+2+2 = 10.00%**; **LIBOR-based 0.40+0.125+0.125 = 0.65%**.)*
>
> | method | rate built from | main weakness |
> |---|---|---|
> | **cost-plus** | the bank's own costs | assumes the bank knows its costs, and ignores competition |
> | **price leadership** | a market base rate + markups | the base rate is somebody else's decision |
> | **LIBOR/SOFR-based** | an international money-market rate | same, and the markup is competed to almost nothing |
> | **CPA** | the whole customer relationship | requires cost allocation the bank cannot do accurately |
>
> **The progression is from "what does it cost us" to "what will the market bear", and it tracks the increase in competition** R&H describes. **Cost-plus is the only one that can price a loan the market has not already priced** — which is why it survives for small business lending and disappears for large corporates.
>
> **The LIBOR example is the one to remember: a 0.25% total markup** on a top-quality borrower, out of which must come funding costs above LIBOR, operating costs, expected loss and [[10 - Capital Adequacy and Basel|capital]]. *(§5 computes that a 100%-weighted corporate loan needs a **2.26%** spread to clear a 12% hurdle.)* **Large-corporate lending does not pay for itself; it is priced as an entry ticket to the relationship** — which is exactly what CPA formalises.
>
> **(b) A different beta to the base rate, presented as a quoting convention.**
>
> *(Computed: identical at prime = **10.00%** and nowhere else. At prime 15%: **17.00% vs 18.00%**. At prime 8%: **10.00% vs 9.60%**. Both of R&H's checks verify.)*
>
> **Times-prime multiplies (beta 1.2); prime-plus adds (beta 1.0).** So **the customer quoted "1.2 × prime" has bought a leveraged position in the base rate** without that being said.
>
> **And it interacts badly with §6.** Times-prime pays the lender more when rates rise — **but a higher rate raises the borrower's default probability.** So in a rate spike the lender acquires a larger contractual claim on a borrower who is less able to pay: **[[06 - Hedging with Derivatives|ch. 06]]'s wrong-way risk, written into a loan contract.** The formula that looks better for the lender is better only if the borrower survives it.
>
> **(c) 7.40%, and the loan is not where the money comes from.**
>
> *(Verified: revenues **216,000**, costs **125,000**, net loanable funds **1,230,000**, return **7.3984%** — the book's 7.4%.)*
>
> **Loan interest is only 41.7% of revenue** *(computed)*; the remaining 58.3% is commitment fees, deposit management, transfers and trust services. **A loan evaluated alone would be repriced or declined; evaluated with the relationship it clears.**
>
> **The compensating balance is a hidden rate increase.** *(Computed: the 20% balance, net of a 10% reserve requirement, cuts the funds the bank must supply by **270,000 — 18% of the line** — and its absence would drop the return from 7.40% to **6.07%**.)* **The customer pays 12% on money it cannot fully use**, which is why the effective rate exceeds the quoted one.
>
> **What CPA gets right: it prices what the bank actually sells.** **What it gets wrong: it needs accurate cost allocation across products**, which R&H elsewhere says banks cannot do — so a CPA answer is only as good as the transfer-pricing behind it, and it is easy to make any relationship look profitable by allocating costs elsewhere.
>
> **(d) The denominator — and with it, [[10 - Capital Adequacy and Basel|ch. 10]].**
>
> **Every method in (a) asks whether the rate covers the costs. RAROC asks whether the return justifies the *capital* the loan consumes**, which is the question a shareholder actually cares about ([[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s ROE).
>
> *(Computed on one \$5mn loan at a 3.00% spread: capital of **0 / 80,000 / 200,000 / 400,000** and RAROC of **infinite / 150.00% / 56.25% / 21.25%** as the risk weight goes 0% / 20% / 50% / 100%. Required spreads to clear a 12% hurdle: **0.792% / 1.230% / 2.260%.**)*
>
> **This is the quantitative form of "riskier borrowers should pay more"** — it says *how much* more, and it does so in units the bank is actually constrained by.
>
> **But note the top row.** **A zero risk weight allocates zero capital, so RAROC is infinite and every such loan passes any hurdle.** [[10 - Capital Adequacy and Basel|Ch. 10]] §3's blind spot propagates directly into the pricing model, because **RAROC inherits its denominator from the capital rule.**
>
> **So the capital rule and the pricing model share one blind spot and reinforce each other in it** — which is worse than either failing alone. **A bank running RAROC diligently and meeting Basel comfortably can be accumulating precisely the exposure neither measures.**
>
> *(RAROC is **not in R&H** — the book stops at cost-plus and CPA. It is added because it is examinable and because it is the link between this chapter and [[10 - Capital Adequacy and Basel|ch. 10]].)*

**2. (Hard — why lenders ration credit.)** (a) Explain and compute R&H's footnote. (b) What follows for pricing policy? (c) How does this relate to the six Cs? (d) Why is the prime rate asymmetric?

> [!example]- Solution
> **(a) The expected return is humped, so past a point charging more earns less.**
>
> **R&H's footnote 6 states it and never computes it.** The mechanism: **the rate charged is not independent of the default probability.** A borrower paying 34% must undertake projects risky enough to service 34%; a borrower paying 6% need not. **The price changes the thing being priced.**
>
> *(Modelled as $p(r)=p_0+k(r-r_0)$ with $p_0=1\%$, $r_0=6\%$, $k=1.10$, LGD 60%, and expected return $r(1-p)-p\cdot LGD$. **The optimum is exactly $r^*=18.00\%$, at a default probability of 14.20% and an expected return of 6.9240%.**)*
>
> | rate | expected return |
> |---|---|
> | 6% | 5.3400% |
> | **18%** | **6.9240%** ← maximum |
> | 28% | 5.8240% |
> | 34% | **4.1080%** |
>
> **At 34% the lender earns less than at 6%** — the rate is nearly six times higher and the return is lower.
>
> **The shape is what matters, not the parameters.** Any model in which the default probability rises with the rate produces a maximum, because **revenue is linear in $r$ while the probability of collecting it falls in $r$.**
>
> **(b) Refuse the loan rather than reprice it.**
>
> **If a borrower's risk requires a rate above $r^*$, no acceptable price exists.** The lender's best response is **credit rationing** — declining regardless of price — and R&H says exactly this: lenders "use both price *and* credit rationing (i.e., denying some loans regardless of price) to regulate the size and composition of their loan portfolios."
>
> **This is why loan markets do not clear like ordinary markets.** In a normal market, excess demand raises the price until it clears. **Here raising the price destroys the product**, so there is a rate ceiling beyond which the lender simply stops, and **some willing borrowers offering to pay more go unserved.**
>
> **Two practical consequences:**
>
> 1. **A rejection rate is a pricing instrument.** R&H notes lenders often "vary their loan rejection rates rather than changing either their base rate or their markups" — **which is now not a quirk but the correct response** to a humped return curve.
> 2. **Beware a loan book with unusually high yields.** [[04 - Measuring and Evaluating Bank Performance|Ch. 04]]'s margin analysis would read it as strength; **§6's curve says it may be a portfolio sitting past $r^*$**, where the yield is high and the expected return is falling.
>
> **(c) The six Cs are the screen the humped curve requires.**
>
> **If some risks must be *declined* rather than priced, the lender needs a way to identify them that is not a price.** That is what the six Cs are.
>
> **Character is the clearest case.** There is no interest rate at which lending to a borrower who does not intend to repay is profitable — the expected return is negative at every price. **So Character is not a risk premium input; it is a gate.** The same is true of Capacity: a signature without legal authority is uncollectible at any rate.
>
> **Cash, Collateral and Conditions are different** — they are matters of degree and *do* map onto a risk premium, which is what §5's RAROC quantifies. **So the six Cs are a mixture of gates and dials**, and treating a gate as a dial is the classic lending error: *"we'll do it at a higher rate."*
>
> **(d) Because the borrowers who cannot leave are the ones for whom rationing binds.**
>
> **R&H cites research finding the prime rate rises more readily than it falls.** The reason connects to (b): **prime-based borrowers are, by construction, the ones without open-market access** — large corporates price off LIBOR/SOFR or issue commercial paper.
>
> **A borrower who can leave disciplines the rate; a borrower who cannot does not.** So the rate is sticky downward for exactly the segment that is captive — and R&H draws the right conclusion, that **bank-dependent borrowers are more vulnerable to business cycles**, paying more precisely when conditions are worst.
>
> **Which closes back on (a): those are also the borrowers most likely to be pushed past $r^*$** by a rate cycle they did not cause — so the asymmetry is not merely unfair, it **manufactures defaults**, and the lender bears them.

**3. (Hard — what credit analysis misses.)** (a) What do the six Cs not ask? (b) Compute the effect. (c) How does this relate to earlier chapters? (d) What is the fix?

> [!example]- Solution
> **(a) What else is in the portfolio.**
>
> **Character, Capacity, Cash, Collateral, Conditions and Control are all questions about *one borrower*.** Even *Conditions*, which looks portfolio-adjacent, asks about **this** borrower's industry — not whether the bank has already lent to two hundred others in it.
>
> **So a bank can approve every loan correctly and assemble a portfolio incorrectly**, and nothing in the credit process will flag it.
>
> **(b) The mean is invariant; the tail is everything.**
>
> *(Computed — 500 loans, each 2% default probability, LGD 100%, equity 9% of the book:)*
>
> | $\rho$ | mean loss | 99th percentile | **P(loss > equity)** |
> |---|---|---|---|
> | 0.00 | 1.9996% | 3.6000% | **0.0000%** |
> | 0.15 | 2.0003% | 10.8000% | 1.8560% |
> | 0.30 | 1.9931% | **17.6000%** | **4.3770%** |
>
> **The mean loss is 2% in every row — correlation adds no expected loss whatsoever.** What moves is the **99th percentile**, which is exactly what capital exists to cover: it nearly **five-folds**, from 3.60% to 17.60%.
>
> **And the probability of losing more than the bank's entire equity goes from zero to 4.38%.** At $\rho=0$ a 9% loss on 500 independent 2% loans is arithmetically almost impossible; at $\rho=0.30$ it happens once in twenty-three.
>
> **Every loan in every row passed the six Cs identically.** Nothing about any borrower changed.
>
> **(c) It is the third appearance of one result.**
>
> | chapter | setting | finding |
> |---|---|---|
> | [[02 - Organization, Structure and Market Entry\|02]] | bank mergers | $\sigma_{\text{comb}}=\sigma\sqrt{(1+\rho)/2}$ — **29.3%** risk reduction at $\rho=0$, **2.5%** at 0.9 |
> | [[06 - Hedging with Derivatives\|06]] | securitisation | mean pool loss **5.00% at every $\rho$**; senior tranche loss **0.0000% → 1.8044%** |
> | **11** | **a loan book** | **mean loss 2.00% at every $\rho$; 99th percentile 3.60% → 17.60%** |
>
> **Three settings, one mathematics, and the same trap each time: the average is fine and the joint behaviour is everything.**
>
> **This is the vault's strongest cross-chapter result** and it generalises well beyond banking: **any risk measure built on expected values is blind to correlation**, and correlation is what turns many small independent risks into one large one. **A model that reports only expected loss is not a risk model.**
>
> **(d) Concentration limits — and they cannot be replaced by better underwriting.**
>
> 1. **Set limits in the loan policy**: by industry, by geography, by single borrower, by collateral type. **These are portfolio constraints and they must be binding**, because §7 shows the loan-by-loan process will never generate them.
> 2. **Measure the tail, not the mean.** [[10 - Capital Adequacy and Basel|Ch. 10]]'s capital covers unexpected loss; the allowance ([[03 - Bank Financial Statements|ch. 03]]) covers expected loss. **A portfolio model reporting only expected loss is measuring the wrong quantity.**
> 3. **Transfer the concentration** — [[06 - Hedging with Derivatives|ch. 06]]'s credit derivatives, loan sales and participations exist for this. **But ch. 06 §11 showed the counterparty fails in the same state**, so this reduces the exposure without eliminating it.
> 4. **Do not mistake diversification of *names* for diversification of *risk*.** 500 borrowers in one industry is one bet made 500 times. **[[02 - Organization, Structure and Market Entry|Ch. 02]] found banks making exactly this error at the level of whole institutions**, crossing state lines and getting no real diversification because the exposures moved together.
>
> **The unifying statement: credit *analysis* is borrower-level and the six Cs do it well; credit *risk management* is portfolio-level and requires a completely different apparatus.** Doing the first excellently is no protection against failing at the second — **which is the honest summary of a great deal of 2008.**

## 📝 Summary

- **The six Cs — Character, Capacity, Cash, Collateral, Conditions, Control — are the borrower-level screen.** *Cash flow, not profit, services debt.* **They are a mixture of gates and dials, and treating a gate as a dial is the classic error.**
- **Four pricing methods, all verified**: **cost-plus** (5+2+2+1 = **10.00%**), **price leadership** (6+2+2 = **10.00%**), **LIBOR-based** (0.40+0.125+0.125 = **0.65%**), and below-prime. **The progression is from "what it costs us" to "what the market bears."**
- **A 0.25% total markup on a top-quality borrower** must cover funding, operating costs, expected loss *and* capital — **so large-corporate lending is priced as an entry ticket to the relationship.**
- *(A minor internal inconsistency in R&H's below-prime example — 4.00% + 0.25% = 4.25%, not the stated 4.50% — is **reported but not filed**, since own-extraction cannot be ruled out for a parenthetical of that shape.)*
- **⚠️ Prime-plus and times-prime agree at exactly one point** *(computed: prime = **10.00%**; at 15% they give 17.00% vs 18.00%, at 8% they give 10.00% vs 9.60%)*. **Times-prime has a beta of 1.2 — a risk transfer presented as a quoting convention**, and it hands the lender a larger claim on a borrower made less able to pay.
- **CPA prices the relationship, not the loan** *(verified: 216,000 − 125,000 over 1,230,000 = **7.3984%**)*. **Loan interest is only 41.7% of revenue**, and **the compensating balance is a hidden rate increase** — without it the return falls to **6.07%**.
- **⚠️ RAROC is not in R&H and is what links pricing to [[10 - Capital Adequacy and Basel|ch. 10]]** *(computed: the same \$5mn loan consumes capital of **0 / 80,000 / 200,000 / 400,000** and returns **infinite / 150.00% / 56.25% / 21.25%**; required spreads **0.792% / 1.230% / 2.260%**)*.
- **⚠️ A zero risk weight gives infinite RAROC**, so the pricing model tells the bank to make unlimited zero-weight loans. **The capital rule and the pricing model share one blind spot and reinforce each other in it.**
- **⚠️ The chapter's best idea is in R&H's footnote 6 and never computed there: the expected return is humped.** *(Computed: it peaks at **$r^*=18.00\%$** with a **14.20%** default probability; at 34% the return is **4.11%**, worse than the 5.34% available at 6%.)*
- **Beyond $r^*$ the lender earns less by charging more, because the rate itself creates the default.** So the correct response to an unacceptable risk is **refusal, not repricing** — **credit rationing**, which is why loan markets do not clear like ordinary markets.
- **A rejection rate is therefore a pricing instrument**, and **a loan book with unusually high yields may be sitting past $r^*$** — high yield, falling expected return.
- **The prime rate is asymmetric because prime-based borrowers are the ones who cannot leave.** Bank-dependent borrowers pay more exactly when conditions are worst — which **manufactures the defaults the lender then bears.**
- **⚠️ The six Cs are all borrower-level and none asks what else is in the portfolio.** *(Computed: 500 loans at 2% default — **mean loss 2.00% at every correlation**, 99th-percentile loss **3.60% → 17.60%**, P(loss > 9% equity) **0.0000% → 4.3770%**.)*
- **500 loans each passing the six Cs can still fail the bank, if all 500 borrowers are in one industry.** **Diversification of *names* is not diversification of *risk*.**
- **⚠️ This is the third appearance of one result** — [[02 - Organization, Structure and Market Entry|ch. 02]]'s $\sigma\sqrt{(1+\rho)/2}$, [[06 - Hedging with Derivatives|ch. 06]]'s tranching, and now a loan book. **The average is always fine and the joint behaviour is everything: any measure built on expected values is blind to correlation.**
- **The fix is concentration limits in the loan policy**, measuring the tail rather than the mean, and recognising that **credit analysis and credit risk management are different disciplines.**
- **Loan review exists because quality is not fixed at origination**, and **workouts are kept separate from the originating officer** — a structural fix for a predictable bias, the same reasoning as [[10 - Capital Adequacy and Basel|ch. 10]]'s objection to self-modelled risk weights.

## ⚠️ Important Notes

1. **Cash flow, not profit, repays a loan.** A profitable firm with earnings locked in receivables cannot pay.
2. **⚠️ Character and Capacity are gates, not dials.** No rate compensates for an intention not to repay or an invalid signature.
3. **Use the *marginal* cost of funds in cost-plus** ([[09 - Managing Deposits and Nondeposit Funding|ch. 09]] §4) — historical average cost books losses as growth.
4. **Cost-plus assumes the bank knows its costs**, which R&H says it usually does not.
5. **⚠️ Times-prime is a leveraged position in the base rate.** Check the beta, not just today's quoted rate.
6. **⚠️ A floating-rate loan transfers interest-rate risk to the borrower and converts it into credit risk for the lender.** It does not remove it.
7. **A compensating balance raises the effective rate above the quoted one** — 7.40% vs 6.07% here.
8. **CPA is only as good as the cost allocation behind it**; any relationship can be made profitable by allocating costs elsewhere.
9. **⚠️ RAROC's denominator comes from the capital rule, so it inherits the rule's blind spots.** Infinite RAROC on zero-weighted assets is not a signal of a good loan.
10. **⚠️ The expected return on a loan is humped.** Past the peak, a higher rate lowers the return.
11. **Refuse rather than reprice when the required rate exceeds $r^*$.** Rationing is the correct response, not a market failure.
12. **⚠️ A high-yielding loan book may be past the peak** — high yield and falling expected return look identical in a margin ratio.
13. **The rejection rate is a portfolio-management instrument**, often better than moving the base rate.
14. **⚠️ None of the six Cs asks about concentration.** Approving every loan correctly does not assemble a correct portfolio.
15. **⚠️ Correlation adds no expected loss and transforms the tail.** Measure the percentile that capital must cover, not the mean.
16. **500 borrowers in one industry is one bet made 500 times.**
17. **Set concentration limits in policy and make them binding** — the loan-by-loan process cannot generate them.
18. **Keep loan workouts separate from the originating officer.** The person who approved it is the worst-placed to admit it failed.

> [!warning] Gaps in the source material
> **R&H ch. 16–17 extract well** *(PDF pp. 539–~610; book page $n$ = PDF page $n+18$)*. **The pricing formulas, the CPA worked example and the six Cs table all came through complete** — Table 16-3's six-column grid survived with all its entries, which is a notable success for a wide table. *(The four standing hazards in `00-Index.md` apply; the comma-for-hyphen fault appears as "Short~ Term", "Long,Term", "Risk,Adjusted".)*
>
> **Verified from the book:** cost-plus (**10%**), price leadership (**10%**), LIBOR-based (**0.65%**), both prime-plus/times-prime comparisons (**17% vs 18%**, **10% vs 9.6%**), and the entire CPA example (revenues **216,000**, costs **125,000**, net loanable funds **1,230,000**, return **7.4%**). **No erratum filed.**
>
> **One inconsistency reported but deliberately not filed** (§2d): the below-prime example borrows fed funds at "4 percent" and then attributes "4.25 percent to cover the money market cost of borrowing", a 25 bp disagreement. **It is minor, it changes nothing, and a parenthetical of that construction is exactly what this PDF garbles — so own-extraction cannot be ruled out**, and [[03 - Bank Financial Statements|ch. 03]]'s rule says it does not get filed.
>
> **⚠️ RAROC is not in Rose & Hudgins.** §5 is entirely an addition. **The `00-Index.md` chapter description promised RAROC before the source was read**; it is included because it is examinable and because it is the only thing that connects loan pricing to [[10 - Capital Adequacy and Basel|ch. 10]]'s capital — **but it should not be attributed to this book.**
>
> **Additions beyond the source.**
>
> - **⚠️ §6 is the chapter's best content and it is R&H's own idea, taken out of a footnote and computed.** The book states that charging the full risk premium can raise the default probability and lower the return; **it never models it.** The humped curve, the exact optimum at **$r^*=18.00\%$**, and the conclusion that **rationing is the correct response rather than a market imperfection** are mine. *(The result is Stiglitz–Weiss credit rationing; the 9th edition gestures at it without naming it.)*
> - **⚠️ §7 is mine** and applies [[06 - Hedging with Derivatives|ch. 06]] §10's method to a loan book. **R&H discusses concentration qualitatively and never computes it.** The finding that **mean loss is invariant to correlation while the 99th percentile nearly five-folds** is the addition, as is the framing that **the six Cs are all borrower-level** and the identification of this as the third appearance of [[02 - Organization, Structure and Market Entry|ch. 02]]'s $\sigma\sqrt{(1+\rho)/2}$.
> - **§5's RAROC treatment**, including the required-spread table and the observation that **a zero risk weight yields infinite RAROC**, propagating [[10 - Capital Adequacy and Basel|ch. 10]] §3's blind spot into the pricing system, is mine.
> - **§3's observation that prime-plus and times-prime coincide at exactly one point**, and that the choice is a risk transfer creating wrong-way risk, is mine; R&H gives two numerical comparisons without generalising.
> - **§4's decomposition of the CPA revenue** (loan interest only **41.7%**) and the calculation of the return **without** the compensating balance (**6.07%**) are mine.
> - **§2's link back to [[09 - Managing Deposits and Nondeposit Funding|ch. 09]]'s marginal-vs-historical cost finding**, and §8's link between workout separation and Basel II's self-modelling problem, are my cross-chapter connections.
> - **The note that LIBOR has been retired in favour of SOFR** is an addition; the 9th edition predates the transition.
>
> **Deliberately compressed.** **R&H ch. 16's regulation of lending** (real-estate lending rules, the Community Reinvestment Act, examiner loan classifications) is compressed to the *Control* C — it is US-specific and has changed. **Ch. 16's sources of credit information and the anatomy of a loan agreement** (covenants, borrower guaranties, events of default) are summarised: important in practice, but the analytical content is thin and the documentation is jurisdictional. **Ch. 17's types of business loan** (working capital, self-liquidating inventory, term, revolving credit, asset-based, syndicated) are compressed to the short-term/long-term distinction that drives the pricing. **⚠️ Ch. 17's financial ratio analysis of a borrower's statements is deliberately not reproduced** — the ratios (liquidity, leverage, coverage, profitability, activity) are the same apparatus [[Principle of Accounting/contents/00-Index|Accounting]] and [[04 - Measuring and Evaluating Bank Performance|ch. 04]] already build, applied to a non-financial firm, and repeating them here would add length without content. **The Black Gold case** is used only for its CPA figures. **Loan-loss provisioning** belongs to [[03 - Bank Financial Statements|ch. 03]], which computed its earnings impact.

**Previous:** [[10 - Capital Adequacy and Basel]] · **Next:** [[12 - Consumer, Credit Card and Real Estate Lending]]
