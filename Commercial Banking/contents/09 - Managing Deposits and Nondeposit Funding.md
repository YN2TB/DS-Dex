---
subject: Commercial Banking
chapter: 9
tags: [ds, banking, deposits, marginal-cost, funding, deposit-insurance, funds-gap, hot-money]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 12–13"
---

# Managing Deposits and Nondeposit Funding

[[08 - Liquidity and Reserves Management|Chapter 08]] proved that **liquidity risk lives in the funding mix** — moving \$50mn from core deposits into hot money raised the liquidity requirement by **87%** with the balance sheet unchanged. **This chapter is about buying that funding, and it closes the loop.**

**The examinable core is marginal cost**, and its one idea is that **raising the posted rate reprices the entire deposit book, not just the new money.** *(Verified: moving from 7.0% to 7.5% costs \$2.00mn to raise \$25mn — a **marginal** rate of **8.0%** while the **average** paid is 7.5%.)*

**Two findings go beyond the source.**

**§2 — R&H's own conclusion does not follow from its own table.** The book says the 8.5% deposit rate "is clearly the best choice." *(Computed: profit is **1.50 at 8.0% and 1.50 at 8.5%** — identical.)* At the optimum, marginal cost equals marginal revenue, so **the last \$25mn contributes exactly zero** — while enlarging the balance sheet by a third and buying hot money.

**§3 discharges ch. 08's obligation.** Deposits bought with a posted rate increase *are* hot money, and ch. 08 requires liquid reserves behind them. *(Computed: a liquidity reserve of just **15.4%** makes the 8.0% rate unprofitable; **30.8%** kills 7.5%; ch. 08's own 95% weight means **no rate increase pays at all.**)*

**The quoted rate is not the cost of a deposit.**

## 📘 Main Knowledge

### 1. Deposits, and why the composition matters more than the total

**Deposits split along two axes that mostly coincide:**

| | **core** | **hot money** |
|---|---|---|
| typical | small checking, savings | large CDs, brokered deposits, fed funds purchased |
| insured? | yes | mostly **not** |
| rate-sensitive? | no | **yes** |
| ch. 08 liquidity weight | **15%** | **95%** |

**Cost-plus pricing** *(R&H eq. 12-1)* charges each service its own way:

$$\text{unit price}=\text{operating expense per unit}+\text{allocated overhead}+\text{profit margin}$$

> [!note] Implicit interest, and why it existed
> **Before 1980, Regulation Q capped deposit rates**, so banks competed on everything *except* rate: free services, branch convenience, and — famously — **toasters**. The gap between the true cost of providing services and the fees charged is the **implicit interest rate**.
>
> **R&H's judgement is that this distorted resource allocation**, and it is right in an instructive way: **a price ceiling does not stop competition, it redirects it into forms that are harder to measure and usually less efficient.** Building branches to pay interest in kind is a worse way to pay interest.
>
> **Deregulation (1980) moved the pricing decision from regulators to banks**, and the result was **unbundling** — each service priced to recover its own cost.

### 2. ⚠️ Marginal cost: the examinable calculation

$$\text{marginal cost}=r_{\text{new}}V_{\text{new}}-r_{\text{old}}V_{\text{old}}\qquad\text{marginal cost rate}=\frac{\Delta\text{total cost}}{\Delta\text{funds raised}}$$

*(Verified — R&H's Table 12-2 in full: **five rows, four computed columns each, all exact.** The bank can invest new funds at 10%.)*

| deposits | rate | total cost | marginal cost | **MC rate** | MR − MC | **profit** |
|---|---|---|---|---|---|---|
| 25 | 7.0% | 1.75 | 1.75 | 7.0% | +3.0% | 0.75 |
| 50 | 7.5% | 3.75 | **2.00** | **8.0%** | +2.0% | 1.25 |
| **75** | **8.0%** | 6.00 | 2.25 | 9.0% | +1.0% | **1.50** |
| **100** | **8.5%** | 8.50 | 2.50 | **10.0%** | **0.0%** | **1.50** |
| 125 | 9.0% | 11.25 | 2.75 | 11.0% | −1.0% | 1.25 |

> [!note] Why the marginal rate exceeds the average — the whole point
> **Moving from 7.0% to 7.5% raises \$25mn at a cost of \$2.00mn, which is an 8.0% marginal rate, while the average rate paid is only 7.5%.**
>
> **Because the bank must pay the new 7.5% to the depositors who were already content at 7.0%.** A posted rate is a price offered to everybody. **The rate rise reprices the whole book, not just the new money.**
>
> **So marginal cost always exceeds average cost when the rate is rising**, and the gap widens as the existing book grows relative to the new money. **A bank with a large deposit base faces a far higher marginal cost than a small one for the same rate increase** — which is a real barrier to a big bank competing on rate, and a real advantage to a new entrant.

> [!warning] R&H's stated conclusion does not follow from its own table
> **The book: "The 8.5 percent deposit rate is clearly the best choice."**
>
> *(Computed: **profit at 8.0% = 1.50; profit at 8.5% = 1.50.** They are equal.)*
>
> **This is not an arithmetic error — every figure in the table is correct.** It is a *conclusion* the numbers do not support. **At the optimum the marginal cost rate equals marginal revenue (10% = 10%), which means the last \$25mn contributes exactly nothing.** That is what the first-order condition *says*: at the optimum the marginal increment is worth zero.
>
> **And the tie is broken against 8.5% on every other dimension.** For identical profit, the 8.5% rate leaves the bank with:
>
> - **a balance sheet a third larger** (\$100mn of new deposits instead of \$75mn);
> - **\$25mn more hot money**, carrying [[08 - Liquidity and Reserves Management|ch. 08]]'s liquidity risk;
> - **\$25mn more rate-sensitive liabilities**, widening [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s negative repricing gap.
>
> **Zero extra profit, three extra risks. The 8.0% rate is strictly better.**
>
> **The general lesson is worth more than the example: an optimum found by setting marginal cost equal to marginal revenue is flat at the top.** Being *at* the optimum and being just short of it are worth the same — so the decision should be made on whatever the objective function left out. **Here it left out risk.**

### 3. ⚠️ What the hot money actually costs

**[[08 - Liquidity and Reserves Management|Ch. 08]] §3 requires a liquidity reserve behind hot money**, held in liquid assets yielding about **3.50%** ([[07 - The Investment Portfolio|ch. 07]]) rather than the 10% assumed above. So:

$$MR_{\text{eff}}=(1-h)\times10.00\%+h\times3.50\%$$

*(Computed — re-solving for the best offer rate at each liquidity weight $h$:)*

| $h$ | $MR_{\text{eff}}$ | **best offer rate** | deposits raised | profit |
|---|---|---|---|---|
| 0.00 *(R&H's assumption)* | 10.000% | **8.50%** | \$100mn | 1.50 |
| 0.15 | 9.025% | 8.00% | \$75mn | 0.77 |
| 0.30 | 8.050% | 7.50% | \$50mn | 0.27 |
| **0.50** | 6.750% | **do not raise rates at all** | — | — |
| **0.95** *(ch. 08's weight for hot money)* | 3.825% | **do not raise rates at all** | — | — |

*(The exact break-points: **the 8.0% rate fails once $h>15.38\%$**; **7.5% fails once $h>30.77\%$**; **7.0% fails once $h>46.15\%$.** The 8.5% rate requires $h=0$ — no reserve whatsoever.)*

> [!warning] The quoted rate is not the cost of a deposit
> **R&H computes marginal cost on the liability side alone and holds marginal revenue fixed at 10%.** But **buying hot money changes the asset side too**, because ch. 08 requires it to be held liquid — and liquid assets yield 3.50%, not 10%.
>
> **A liquidity reserve of only 15.4% is enough to make the book's 8.0% rate unprofitable.** At ch. 08's own weight for hot money — 95% — **no rate increase pays at all.**
>
> **This is the point of the ch. 08 / ch. 09 pair.** Ch. 08 showed liquidity risk lives in the funding mix; ch. 09 shows what the mix costs to change. **The true cost of a deposit is the rate paid *plus* the yield drag of the liquidity that must sit behind it** — and the second term is frequently larger than the first.
>
> **A bank pricing deposits off the marginal-cost table alone will systematically overpay for hot money**, because the table's marginal revenue is computed as though the new funds could be lent out in full. They cannot.

### 4. Historical average cost, and the door it lets losses through

*(Computed — a bank funded 80% at an old 4.00% and 20% at today's 7.00%:)*

| | |
|---|---|
| historical average cost | **4.60%** |
| marginal cost | **7.00%** |

**A loan yielding 6.00%:**

| measured against | margin | verdict |
|---|---|---|
| historical average (4.60%) | **+1.40%** | *looks profitable* |
| **marginal cost (7.00%)** | **−1.00%** | **is a loss** |

*(And the error is one-signed and grows with the rate: at 5% today's rate the understatement is 0.80 points; at 7%, **2.40 points**; at 9%, **4.00 points**.)*

> [!note] The repricing gap arriving through the pricing policy
> **Pricing loans off historical average cost in a rising-rate market books assets that are unprofitable the moment they are funded.**
>
> **This is [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s repricing gap coming in through a different door.** There the loss arrived because liabilities repriced faster than assets; here it arrives because the *pricing decision* used a stale cost of funds. **Same loss, different mechanism** — and the second one is worse, because it is a policy choice rather than a structural exposure, and it looks like profitable growth while it happens.
>
> **The symmetric error exists too**: in a *falling*-rate market, historical average cost overstates the cost of funds and the bank turns down loans that would have been profitable. **The error is one-signed *given the direction of rates*, not one-signed absolutely.**

### 5. Nondeposit funding and the available funds gap

**When deposits are inadequate, banks buy funds** — fed funds purchased, repurchase agreements, the discount window, negotiable CDs, Eurodollars, commercial paper, and long-term debt.

> [!note] The customer relationship doctrine is what drives this
> **R&H's argument: a lender must never refuse a good loan for lack of funding**, because refusal loses the customer and every future service sold to them. **So the funding is found rather than the loan declined** — which converts a *deposit* constraint into a *cost* problem, and is exactly the reasoning behind [[08 - Liquidity and Reserves Management|ch. 08]]'s 100% liquidity weight on undrawn loan capacity.

$$\text{AFG}=\text{loans and investments desired}-\text{deposits and other funds available}$$

*(Verified — R&H's example, book p. 433:)*

| uses | |
|---|---|
| new loan requests | 150 |
| Treasury securities to buy | 75 |
| **expected credit-line drawings** | **135** |
| **total** | **360** |

| sources | |
|---|---|
| deposits received today | 185 |
| deposits expected this week | 100 |
| **total** | **285** |

$$\text{AFG}=360-285=\mathbf{\$75\text{mn}}\;✓$$

> [!warning] The second-largest use is a claim the bank does not control
> **Credit-line drawings are 135 — nearly as large as the entire new loan book.** These are **commitments the bank has already made and the *borrower* chooses when to exercise.**
>
> **[[08 - Liquidity and Reserves Management|Ch. 08]] measured them at 70.9% of industry assets** and identified them as [[06 - Hedging with Derivatives|ch. 06]] §7's category: **a written option, correlated the wrong way** — drawn when borrowers are short of cash, which is when the bank is too.
>
> **So the funds gap is driven substantially by a timing decision that belongs to somebody else**, which is why R&H recommends adding a buffer on top of it.

### 6. Deposit insurance: why core deposits are cheap *and* sticky

> **A major reason depository institutions are able to sell deposits at relatively low rates of interest compared to interest rates offered on other financial instruments is because of government-supplied deposit insurance.** — R&H, p. 408

*(Computed — insured core deposits at 1.25% against uninsured wholesale funding at 4.50%, a **3.25 point** difference, on ch. 05's \$147mn of funding:)*

| core share of funding | **annual value of the difference** |
|---|---|
| 50% | 2 388.75 |
| 70% | 3 344.25 |
| **85%** | **4 060.88** |

> [!warning] This is a transfer, not a margin
> **The depositor accepts a low rate because the *government* guarantees the money — not because the bank is safe.** So the funding advantage is not earned by the bank; it is a subsidy, and it is large: **on an 85%-core funding base it is worth more than a quarter of this bank's equity every year.**
>
> **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] made the argument and this prices it.** The insurance removes the depositor's reason to monitor the bank, so **the discipline has to come from somewhere else — which is what [[10 - Capital Adequacy and Basel|ch. 10]]'s capital requirements are.** Risk-based insurance premiums (well-capitalised A-rated institutions pay least) are an attempt to charge for the subsidy directly.
>
> **And it explains ch. 08's funding-mix result in one line.** Core deposits are **cheap *and* sticky for the same reason** — they are insured. **So a bank replacing them with hot money pays twice: a higher rate, and a higher liquidity reserve behind it** (§3).

**The coverage limit is per depositor per institution** *(R&H's table: \$2,500 in 1934 → \$100,000 from 1980 → **\$250,000** from 2008, made permanent by Dodd-Frank in 2010)*.

> [!note] Which is why a large corporate balance is not a core deposit
> **A \$10mn corporate account is 97.5% uninsured**, so it behaves like hot money regardless of what the balance sheet calls it. **A bank funded by a few large accounts has core deposits on paper and hot money in reality.**
>
> **[[08 - Liquidity and Reserves Management|Ch. 08]]'s classification is doing all the work, and it is management's own judgement** — which is exactly the weakness ch. 08 flagged, now with a concrete way to test it: **ask what fraction of the deposit base is above the insurance limit.** That number is not a matter of judgement, and it is the one that mattered in 2023.

## ✏️ Exercises

**1. (Marginal cost.)** (a) Verify the table and explain why marginal exceeds average. (b) Is 8.5% "clearly the best choice"? (c) What does the liquidity reserve do to the answer?

> [!example]- Solution
> **(a) Because a posted rate is offered to everyone, so it reprices the existing book.**
>
> *(Verified: all five rows and four computed columns of Table 12-2 — total cost, marginal cost, marginal cost rate and profit — match exactly.)*
>
> $$\text{MC}=r_{\text{new}}V_{\text{new}}-r_{\text{old}}V_{\text{old}}=0.075(50)-0.070(25)=3.75-1.75=\mathbf{2.00}$$
> $$\text{MC rate}=\frac{2.00}{25}=\mathbf{8.0\%}\quad\text{while the average paid is }7.5\%$$
>
> **The 0.5 point difference is what the bank pays the depositors who were already content at 7.0%.** They did not need the extra half point; they get it anyway, because the rate is posted.
>
> **Two consequences worth carrying:**
>
> 1. **Marginal cost exceeds average cost whenever the rate is rising**, and the gap widens with the size of the existing book. **A large bank faces a much higher marginal cost than a small one for the same rate rise** — real protection for incumbents against rate competition, and a real advantage for a new entrant with nothing to reprice.
> 2. **The rule is to raise the rate while MC rate < MR**, not while the rate is below the investment yield. **Judging by the posted rate (8.5% < 10%, so it looks fine) rather than the marginal rate (10% = 10%, so it is the limit) is the standard error.**
>
> **(b) No — it is tied with 8.0%, and worse on every other dimension.**
>
> *(Computed: **profit is 1.50 at both** 8.0% and 8.5%.)*
>
> **This is not an arithmetic error — the table is right — but the book's conclusion is not supported by it.** At the optimum, MC rate = MR = 10%, so **the final \$25mn adds exactly as much cost as revenue and contributes zero.** That is what a first-order condition means; **an optimum located by setting MC = MR is flat at the top.**
>
> **And the tie breaks against 8.5%:**
>
> | | 8.0% | 8.5% |
> |---|---|---|
> | profit | 1.50 | 1.50 |
> | new deposits | \$75mn | **\$100mn** |
> | hot money taken on ([[08 - Liquidity and Reserves Management|ch. 08]]) | less | **more** |
> | rate-sensitive liabilities ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]) | less | **more** |
>
> **Zero extra profit, three extra risks.**
>
> **The transferable lesson: when an optimum is flat, decide on what the objective function omitted.** Here the objective was profit and the omission was risk — and [[04 - Measuring and Evaluating Bank Performance|ch. 04]] found the identical structure, where three banks with the same 12.000% ROE differed 3.3× in fragility. **Optimising a single number is safe only when you know what the number leaves out.**
>
> **(c) It moves the optimum down, and can eliminate it entirely.**
>
> **Deposits bought with a posted rate increase are, by [[08 - Liquidity and Reserves Management|ch. 08]]'s definition, hot money** — interest-sensitive funds that arrived for a rate and will leave for a better one. **Ch. 08 requires liquid reserves behind them**, and liquid assets yield ~3.50%, not 10%.
>
> $$MR_{\text{eff}}=(1-h)(10.00\%)+h(3.50\%)$$
>
> *(Computed: **$h=0.15$ → best rate 8.00%**, profit 0.77; **$h=0.30$ → 7.50%**, profit 0.27; **$h\ge0.50$ → do not raise rates at all.** Exact break-points: 8.0% fails above $h=15.38\%$, 7.5% above $30.77\%$, 7.0% above $46.15\%$.)*
>
> **At ch. 08's own 95% weight for hot money, no rate increase is profitable.**
>
> **R&H's error is structural, not arithmetic: it computes marginal cost on the liability side and holds marginal revenue constant.** But **the funding decision changes the asset side** — the new money cannot be fully lent, because a large part of it must sit in liquid assets against the possibility that it leaves.
>
> **So: the cost of a deposit is the rate paid plus the yield drag of the liquidity behind it, and the second term is often larger.** A bank pricing off the marginal-cost table alone **systematically overpays for exactly the funding it should least want.**

**2. (Hard — cost of funds and the funding mix.)** (a) Why is historical average cost dangerous? (b) What is the AFG and what drives it? (c) Why are core deposits cheap? (d) When is a "core deposit" not one?

> [!example]- Solution
> **(a) Because it prices today's loans with yesterday's funding cost.**
>
> *(Computed: a bank funded 80% at 4.00% and 20% at 7.00% has a historical average cost of **4.60%** against a marginal cost of **7.00%**. A 6.00% loan shows a **+1.40%** margin on the first and **−1.00%** on the second.)*
>
> **The bank books the loan believing it earns 1.40 points and it loses 1.00.** *(And the gap widens with rates: **2.40 points** understatement at a 7% marginal rate, **4.00 points** at 9%.)*
>
> **This is [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s repricing gap arriving through the pricing policy rather than the balance sheet.** Same loss, different door — **and this door is worse, because it is a policy choice rather than a structural exposure, and because it presents as profitable growth while it happens.** A bank with a *zero* repricing gap can still do this.
>
> **The symmetric error matters too.** When rates are *falling*, historical average cost **overstates** the cost of funds, and the bank declines loans that would have been profitable. **The bias follows the direction of rates**, so a bank using historical cost is wrong in both regimes — too aggressive in one and too timid in the other, which is the worst possible pairing.
>
> **The rule: price assets off the marginal cost of the funds that will actually finance them.**
>
> **(b) The AFG is desired uses minus expected sources — and a third of it is outside the bank's control.**
>
> *(Verified: $(150+75+135)-(185+100)=360-285=\mathbf{75}$ ✓)*
>
> **The second-largest single item is expected credit-line drawings at 135** — nearly as large as the entire new loan demand. **These are commitments already made, exercised at the borrower's option.**
>
> **[[08 - Liquidity and Reserves Management|Ch. 08]] found the industry holding these at 70.9% of total assets** and classified them as [[06 - Hedging with Derivatives|ch. 06]] §7's **written option, correlated the wrong way**: borrowers draw when they are short of cash, which is when the bank is short too. **So the funds gap is largest exactly when funding is hardest to buy.**
>
> **Which is why R&H tells banks to add a buffer to the AFG estimate**, and why the **customer relationship doctrine** — never refuse a good loan for lack of funding — is both correct commercially and a source of exactly this exposure. **It converts a quantity constraint into a price constraint**, and [[08 - Liquidity and Reserves Management|ch. 08]] §5 showed the price is zero until it is infinite.
>
> **(c) Because the government, not the bank, guarantees them.**
>
> *(Computed: insured core deposits at 1.25% against uninsured wholesale funding at 4.50% — a **3.25 point** difference, worth **4,060.88 a year** on an 85%-core funding base of \$147mn.)*
>
> **That is more than a quarter of this bank's equity, every year, and the bank did nothing to earn it.** It is a transfer from the insurance fund — and ultimately the taxpayer — to the bank and its depositors.
>
> **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] argued this and here it is priced.** The insurance removes the depositor's incentive to monitor, so **market discipline has to be replaced by regulatory discipline** — [[10 - Capital Adequacy and Basel|ch. 10]]'s capital rules. **Risk-based insurance premiums** (well-capitalised, A-rated institutions pay the least) are an attempt to charge the subsidy back directly, and they are why capital adequacy shows up in the *funding cost* and not only in the regulator's report.
>
> **And it explains ch. 08's central result in one line: core deposits are cheap *and* sticky for the same reason.** Insurance removes both the need for a high rate and the reason to run. **So a bank that swaps core deposits for hot money pays twice — a higher rate now, and a higher liquidity reserve behind it forever (§3).**
>
> **(d) When it is above the insurance limit.**
>
> **Coverage is \$250,000 per depositor per institution** *(R&H's table: \$2,500 in 1934, \$100,000 from 1980, \$250,000 from 2008 and permanent under Dodd-Frank)*.
>
> **So a \$10mn corporate account is 97.5% uninsured**, and its holder has every reason to behave exactly like a hot-money investor — monitoring the bank, and leaving fast. **It sits in the "deposits" line of the balance sheet and is nothing like a core deposit.**
>
> **[[08 - Liquidity and Reserves Management|Ch. 08]] flagged that the 95/30/15 classification is management's own judgement, and this is the concrete test:** what fraction of the deposit base sits above the insurance limit? **That number is not a matter of opinion.**
>
> **It is also what made 2023 different from 1933.** A depositor base that is large, concentrated, uninsured, well-informed and electronically connected **solves ch. 08's coordination problem very quickly** — the run is faster, not less rational. **A bank can have 90% of its funding in "deposits" and almost none of it in core deposits**, and every ratio in this subject will look fine.

## 📝 Summary

- **Deposits split into core (small, insured, rate-insensitive, 15% liquidity weight) and hot money (large, uninsured, rate-sensitive, 95% weight)** — and the split matters more than the total.
- **Regulation Q's rate ceiling redirected competition rather than stopping it** — into branches, free services and toasters. **A price ceiling produces competition in forms that are harder to measure and usually less efficient.**
- **⚠️ The examinable calculation is marginal cost** *(R&H Table 12-2 verified in full — five rows, four computed columns each, all exact)*: **moving 7.0% → 7.5% costs 2.00 to raise 25, an 8.0% marginal rate against a 7.5% average.**
- **The reason is that a posted rate reprices the whole book, not just the new money.** So **marginal cost exceeds average cost whenever rates rise**, and the gap grows with the existing book — **protecting large incumbents from rate competition and favouring new entrants.**
- **⚠️ R&H says 8.5% "is clearly the best choice"; profit is 1.50 at both 8.0% and 8.5%.** Not an arithmetic error — **a conclusion its own table does not support.** At the optimum MC = MR, so **the last \$25mn contributes exactly zero.**
- **And the tie breaks against 8.5%**: same profit, but a **third larger balance sheet**, more hot money ([[08 - Liquidity and Reserves Management|ch. 08]]) and more rate-sensitive liabilities ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]). **Zero extra profit, three extra risks.**
- **⚠️ An optimum found by setting MC = MR is flat at the top** — so decide on whatever the objective function omitted. Here it omitted risk, exactly as [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s identical 12.000% ROEs hid a 3.3× difference in fragility.
- **⚠️ Ch. 08's obligation discharged: rate-bought deposits are hot money, and the liquidity behind them destroys the case.** *(Computed: $MR_{\text{eff}}=(1-h)10\%+h\,3.5\%$; **the 8.0% rate fails once $h>15.38\%$**, 7.5% above 30.77%, and **at ch. 08's 95% weight no rate increase pays at all.**)*
- **The quoted rate is not the cost of a deposit.** It is the rate **plus the yield drag of the liquidity that must sit behind it** — and the second term is frequently larger. **R&H computes marginal cost on the liability side alone and holds marginal revenue fixed.**
- **⚠️ Historical average cost misprices loans** *(computed: 4.60% historical vs 7.00% marginal makes a 6.00% loan look **+1.40%** profitable when it is **−1.00%**; the error reaches **4.00 points** at a 9% marginal rate)*.
- **That is the repricing gap arriving through the pricing policy** — worse than the structural version, because it is a choice and it looks like profitable growth. **The bias follows the direction of rates**, so the bank is too aggressive when rates rise and too timid when they fall.
- **AFG = desired uses − expected sources** *(verified: $360-285=\mathbf{75}$)*. **The second-largest use is credit-line drawings at 135** — a written option the *borrower* exercises, drawn precisely when the bank is also short.
- **The customer relationship doctrine converts a quantity constraint into a price constraint** — and ch. 08 showed that price is zero until it is infinite.
- **⚠️ Deposit insurance is why core deposits are cheap, and it is a transfer, not a margin** *(computed: a **3.25 point** advantage worth **4,060.88 a year** on an 85%-core funding base — more than a quarter of this bank's equity)*.
- **It also explains why core deposits are cheap *and* sticky: the same insurance removes both the need for a high rate and the reason to run.** So swapping core for hot money **costs twice.**
- **⚠️ Coverage is \$250,000 per depositor per institution, so a \$10mn corporate account is 97.5% uninsured** and behaves like hot money whatever the balance sheet calls it. **The fraction of deposits above the limit is the one classification test that is not a matter of judgement** — and it is what mattered in 2023.

## ⚠️ Important Notes

1. **⚠️ Use marginal cost, never the posted rate, to decide whether to raise deposit rates.** Judging 8.5% against a 10% investment yield is the standard error; the relevant comparison is the *marginal* rate.
2. **A posted rate reprices the entire book.** This is the whole reason marginal exceeds average.
3. **The marginal-cost penalty grows with the size of the existing deposit base** — a structural advantage for small entrants.
4. **⚠️ An optimum where MC = MR is flat.** Being just short of it costs nothing; decide the margin on what the objective omitted.
5. **⚠️ Deposits bought with a rate increase are hot money by definition** — they arrived for a rate and will leave for a better one.
6. **⚠️ Add the liquidity drag to the marginal cost of hot money.** A 15.4% reserve is enough to reverse R&H's answer.
7. **A funding decision is also an asset decision.** New hot money cannot be fully lent out.
8. **⚠️ Never price loans off historical average cost.** In a rising market it books losses as growth; in a falling one it declines good business.
9. **A zero repricing gap does not protect against the pricing-policy version of the same loss.**
10. **Add a buffer to the AFG** — a large part of it is credit-line drawings the borrower times.
11. **⚠️ Unused commitments are written options correlated the wrong way** ([[06 - Hedging with Derivatives|ch. 06]] §7, [[08 - Liquidity and Reserves Management|ch. 08]] §6).
12. **The customer relationship doctrine is commercially right and creates the exposure** — it turns "we have no funds" into "we will pay whatever it costs".
13. **⚠️ Deposit insurance is a subsidy, not a skill.** It is why the funding is cheap and why the regulator sets the capital.
14. **Risk-based insurance premiums put capital adequacy into the funding cost**, not just the supervisor's report.
15. **⚠️ Test the core-deposit classification by the insurance limit.** Deposits above \$250,000 are hot money regardless of their label.
16. **A bank can be 90% deposit-funded and hold almost no core deposits** — and every ratio in this subject will look fine.

> [!warning] Gaps in the source material
> **R&H ch. 12–13 extract well** *(PDF pp. 415–~500; book page $n$ = PDF page $n+18$)*. **Table 12-2 — the chapter's examinable core — came through complete with every figure**, as did the FDIC coverage-limit table and the funds-gap example. **This is the third consecutive chapter where a numeric table set as text survived whole**, confirming the rule [[08 - Liquidity and Reserves Management|ch. 08]] settled. *(The four standing hazards in `00-Index.md` apply; the comma-for-hyphen fault appears as "Cost Plus Profit", "deposit~related", "Norul.eposit".)*
>
> **Verified from the book: 22 checks, all exact.** Table 12-2's five rows × four computed columns (total cost, marginal cost, marginal cost rate, profit), the 8.0% marginal cost rate worked in the prose, and the available funds gap of **\$75mn**. **No erratum — every figure R&H prints is correct.**
>
> **⚠️ But one stated *conclusion* is not supported by the book's own table** (§2): "The 8.5 percent deposit rate is clearly the best choice", when profit is **identical at 8.0% and 8.5%**. **This is recorded here rather than in the errata table because the arithmetic is right** — the errata table is for numbers, and this is an inference. **It is the same category as [[02 - Organization, Structure and Market Entry|ch. 02]]'s finding that R&H's own cost-curve evidence undercuts its consolidation narrative: the data are sound and the sentence drawn from them is not.**
>
> **Figures that are mine**: the liquidity weights and 3.50% liquid yield in §3 (both from [[07 - The Investment Portfolio|ch. 07]] and [[08 - Liquidity and Reserves Management|ch. 08]]), the 80/20 funding split in §4, and the core/wholesale rates in §6. **Table 12-2, the cost-plus formula, the AFG formula, the FDIC table and the marginal-cost definitions are the book's.**
>
> **Additions beyond the source.**
>
> - **⚠️ §2's finding that R&H's conclusion does not follow from its own table** is mine, as is the general lesson (**an optimum at MC = MR is flat, so decide the margin on what the objective omitted**) and the link to [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s identical-ROE result.
> - **⚠️ §3 is the chapter's main addition and discharges [[08 - Liquidity and Reserves Management|ch. 08]]'s explicit obligation.** **R&H computes marginal cost on the liability side alone and holds marginal revenue fixed at 10%**, never connecting it to the liquidity reserve its own ch. 11 requires behind hot money. **The $MR_{\text{eff}}$ formulation, the re-solved optimum at each $h$, and the exact break-points (15.38%, 30.77%, 46.15%) are not in the source** — and they reverse the book's recommendation.
> - **The observation that the marginal-cost penalty grows with the existing deposit base**, giving small entrants a structural advantage in rate competition, is mine.
> - **§4's quantification of the historical-vs-marginal error across rate levels**, and the framing that it is [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s repricing gap arriving through the pricing policy — including the symmetric error in a falling market — are additions. R&H makes the qualitative point well and does not compute it.
> - **§5's observation that credit-line drawings are the second-largest item in the AFG** and are a written option timed by the borrower ([[06 - Hedging with Derivatives|ch. 06]], [[08 - Liquidity and Reserves Management|ch. 08]]) is mine.
> - **§6's pricing of the deposit-insurance subsidy** is mine — R&H states the mechanism in one sentence and never quantifies it — as is **the test for a genuine core deposit (the fraction above the insurance limit)** and the note on why 2023's depositor base solved ch. 08's coordination problem faster.
>
> **Deliberately compressed.** **R&H ch. 12's survey of deposit types** (demand, NOW, MMDA, savings, time, CD variants, IRA/Keogh) is compressed to the core/hot distinction that carries the analysis; the detail is US-specific and product names date quickly. **The full FDIC coverage rules** — joint accounts, pass-through insurance, ownership categories, the Designated Reserve Ratio — are compressed to the limit and the risk-based premium, which are the parts that affect bank behaviour. **Conditional and relationship pricing, and the Truth in Savings APY disclosure**, are noted rather than worked: the mechanics are straightforward and the interesting content is the marginal-cost decision. **Basic (lifeline) banking** is a policy debate rather than a management technique and is omitted. **Ch. 13's individual nondeposit instruments** (fed funds mechanics, RP collateral conventions, discount-window tiers, Eurodollar settlement) are compressed to the five choice factors and the funds gap — the arithmetic is common to all of them, and the discount-window and reserve mechanics have changed materially since the 9th edition.

**Previous:** [[08 - Liquidity and Reserves Management]] · **Next:** [[10 - Capital Adequacy and Basel]]
