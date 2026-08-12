---
subject: Commercial Banking
chapter: 6
tags: [ds, banking, derivatives, futures, options, swaps, securitization, cds, correlation, basel]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 8–9"
---

# Hedging with Derivatives

[[05 - Interest-Rate Risk - Gap and Duration|Chapter 05]] §7 ended with a promise: banks do not immunise their balance sheets, because removing the maturity mismatch removes the spread. **They hedge with derivatives instead — an instrument that changes the rate exposure without touching the loan book.**

**This chapter makes good on that promise and then attacks it.** §1 closes ch. 05's exact duration gap of **1.9374 years** with 352 futures contracts and the loans left exactly where they were. §§1b–2 then show what the hedge quietly bought.

**The chapter's result is in §7.** Tranche a pool of loans and vary nothing except the *correlation* between defaults: **the mean pool loss stays at 5.00% in every single case, and the senior tranche's expected loss goes from 0.0000% to 1.8044%.** Nothing about the loans changed. **The AAA rating was a claim about correlation, not about credit quality** — and it is [[02 - Organization, Structure and Market Entry|ch. 02]]'s diversification result reappearing in a place nobody was looking.

**Every one of R&H's seven worked figures was recomputed and every one checks out.** Where this chapter departs from the book, it is by stress-testing the book's own formulas past the range where they hold.

## 📘 Main Knowledge

### 1. Futures: how many contracts, and does it work?

R&H's equation (8-13) sets the futures gain equal to the loss in net worth and solves:

$$N=\frac{\left(D_A-\frac{TL}{TA}D_L\right)\times TA}{D_F\times F_0}=\frac{D_{\text{gap}}\times TA}{D_F\times F_0}$$

**The numerator is ch. 05's duration gap in dollars; the denominator is the dollar sensitivity of one contract.**

*(Verified against R&H's own worked example, book p. 269 — $D_A=4$, $D_L=2$, $TA=\$500$mn, $TL=\$460$mn, T-bond futures with $D_F=9$ and $F_0=\$99{,}700$:)*

$$D_{\text{gap}}=4-0.92\times2=2.16\text{ yrs}\qquad N=\frac{2.16\times500{,}000{,}000}{9\times99{,}700}=1203.6$$

**The book says "about 1,200". ✓** *(Its single-contract example on p. 267 also checks exactly: $-9\times99{,}700\times0.01/1.07=-\$8{,}385.98$, matching the printed figure to the cent.)*

**Now ch. 05's bank** — $D_{\text{gap}}=1.9374$, assets \$163 mn:

$$N=\frac{1.9374\times163{,}000{,}000}{9\times99{,}700}=351.94\longrightarrow\textbf{short 352 contracts}$$

| shock | loss on balance sheet | gain on futures | **net** | % of equity |
|---|---|---|---|---|
| −2.0% | +5 958 | −5 959 | **−1** | −0.01% |
| +1.0% | −2 979 | +2 980 | **+0** | +0.00% |
| **+2.0%** | **−5 958** | **+5 959** | **+1** | **+0.01%** |
| +3.0% | −8 938 | +8 939 | **+1** | +0.01% |

> [!note] ch. 05's 37.24%-of-equity loss is now a rounding error
> **The residual is entirely the rounding of 351.94 contracts to 352.** And the notional shorted is only **21.5% of assets** — the bank did not sell a loan, shorten a maturity, or reprice a deposit.
>
> **That is the whole argument for derivatives, demonstrated:** ch. 05 showed immunising the balance sheet required shortening assets from 3.20 to 1.26 years, abolishing the maturity transformation. **352 contracts achieve the same $D_{\text{gap}}=0$ and leave the business intact.**

### 2. ⚠️ But the hedge is built from duration on *both* sides

[[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] §5 measured how badly duration degrades for large moves. **Equation (8-13) uses duration twice — once for the balance sheet, once for the futures contract — and the two errors do not cancel.**

*(Computed — exact repricing of both legs against the linear model:)*

| shock | exact Δ net worth | duration model | **residual** | % of equity |
|---|---|---|---|---|
| **−5.0%** | +16 968 | +14 896 | **−2 150** | **−13.44%** |
| −2.0% | +6 272 | +5 958 | −291 | −1.82% |
| −1.0% | +3 056 | +2 979 | −69 | −0.43% |
| +1.0% | −2 905 | −2 979 | −61 | −0.38% |
| +2.0% | −5 667 | −5 958 | −233 | −1.46% |
| **+5.0%** | −13 166 | −14 896 | **−1 250** | **−7.81%** |

> [!warning] The hedged bank loses at both ends
> **The residual is negative in every row.** Not "sometimes wrong" — **systematically adverse, in both directions.**
>
> **The mechanism is convexity mismatch.** The bank's net exposure has a duration of 1.94 years; the hedge instrument has a duration of **9**. Convexity grows roughly with the *square* of duration, so **a short position in the 9-year contract sells far more convexity than the balance sheet ever owed.** Short = concave; the balance sheet is convex; the difference is a loss whichever way rates move.
>
> **Equation (8-13) cannot see this.** It matches first derivatives, and by construction it matches them perfectly — the §1 table is essentially exact. **The exposure it leaves behind is entirely second-order, which is precisely why a first-order formula reports success.**
>
> **The practical rule is ch. 05's, sharpened:** match duration *and* check the second order, or hedge with an instrument whose duration is close to the exposure's. **A 300 bp move costs this "fully hedged" bank about 3% of its equity.**

### 3. ⚠️ Basis risk: the assumption (8-13) actually rests on

$$\text{basis}=\text{cash-market price}-\text{futures price}\qquad\text{(R\&H eq. 8-3)}$$

**§1 assumed the futures price moves exactly with the cash market.** *(Computed — letting it move by a factor $b$ instead, at a +2% shock:)*

| $b$ | net | % of equity |
|---|---|---|
| 1.00 | +1 | +0.01% |
| 0.98 | −118 | −0.74% |
| **0.95** | **−297** | **−1.86%** |
| 0.90 | −595 | −3.72% |

> [!note] The hedge exchanged one risk for another
> **A 5% slippage in the basis leaves 1.86% of equity unhedged** — larger than the convexity residual at the same shock.
>
> **R&H puts it correctly and mildly: basis risk is "usually less than interest rate risk in the cash market, so hedging reduces (but usually does not completely eliminate) overall risk exposure."** The point worth extracting is the structural one: **the bank did not remove interest-rate risk. It replaced a large exposure with a smaller one of a different kind** — which is the honest description of every instrument in this chapter.

### 4. The swap, and where its gain comes from

**Two borrowers exchange interest payments.** Neither lends the other money; the **notional principal is never exchanged**; only the *net* interest difference changes hands.

*(Verified — R&H's comparative-advantage table, book p. 280:)*

| | fixed | floating |
|---|---|---|
| low-rated borrower | 11.50% | prime + 1.75% |
| high-rated borrower | 9.00% | prime |
| **quality spread** | **2.50%** | **1.75%** |

$$\text{total gain from trade}=2.50\%-1.75\%=\mathbf{0.75\%}$$

**The book splits it 0.50% to the low-rated borrower and 0.25% to the high-rated one — which sums to 0.75% and exhausts the gain exactly. ✓**

> [!note] The gain is a *difference of spreads*, and it can be zero
> **The high-rated borrower can borrow more cheaply in *both* markets.** Absolute advantage explains nothing. **What creates the gain is that its advantage is bigger in the fixed market (2.50%) than in the floating market (1.75%).**
>
> *(Computed — hold the fixed spread at 2.50% and vary the floating spread:)*
>
> | floating spread | total gain |
> |---|---|
> | 1.75% | 0.75% |
> | 2.25% | 0.25% |
> | **2.50%** | **0.00%** |
>
> **When the two spreads are equal the swap creates nothing.** This is exactly [[Macroeconomics & Microeconomics/contents/00-Index|comparative advantage]], and it is why R&H notes that "some authorities argue these savings are illusory" — an efficient market should arbitrage the difference away.

### 5. The swap as duration surgery

A **pay-fixed / receive-floating** swap is economically *short a fixed-rate bond and long a floater*, so **its value rises when rates rise** — what a positive duration gap needs.

$$NS=\frac{D_{\text{gap}}\times A}{D_{\text{fix}}-D_{\text{flt}}}$$

*(Computed for ch. 05's bank, using ch. 05's own 5-year 6% bond as the fixed leg, $D_{\text{fix}}=4.4651$, and a quarterly-reset floating leg, $D_{\text{flt}}=0.25$:)*

$$NS=\frac{1.9374\times163{,}000}{4.4651-0.25}=\mathbf{74{,}921}\quad(\textbf{46.0\% of assets})$$

| shock | loss on b/s | gain on swap | net |
|---|---|---|---|
| −2.0% | +5 958 | −5 958 | **0** |
| +2.0% | −5 958 | +5 958 | **0** |
| +3.0% | −8 938 | +8 938 | **0** |

**Note that the swap needs 46.0% of assets in notional where the futures hedge needed 21.5%.** *(The hedge notional is inversely proportional to the instrument's net duration: 9 years for the T-bond contract, 4.22 for the swap. The longer the instrument, the less of it you need — and, per §2, the worse the convexity mismatch.)*

### 6. ⚠️ Notional is not exposure

*(Computed:)*

| | |
|---|---|
| swap notional | **74 921** |
| annual net cash at a +2% move | **1 498** — **2.0% of notional** |
| amount at risk if the counterparty fails | only the **net**, never the notional |

> [!warning] $225 trillion is a real number and it does not mean what it looks like
> **R&H reports 1,159 US banks holding derivatives with a combined notional of \$225 trillion in mid-2010, against \$10.7 trillion of assets — a ratio of 21.1×** *(computed)*.
>
> **Notional measures contract size, not money at risk.** The mechanism is **netting**: on each payment date the parties exchange only the *difference* between what they owe each other, so **that difference is the only sum a default can take.**
>
> **This cuts both ways, and both are worth holding.** The headline number is genuinely misleading — but netting only limits the loss *per contract*, and it says nothing about **whether the counterparty can pay at all**, which is §9's problem.

### 7. Options: what the premium buys

**An option is a right, not an obligation** — which makes its payoff *asymmetric* where a futures hedge is symmetric.

*(Computed — the same bank, hedged two ways; the put costs a 1.5% premium = **526**, or **3.29% of equity**:)*

| shock | unhedged | futures-hedged | put-hedged |
|---|---|---|---|
| −3.0% | +8 938 | −1 | **+8 411** |
| −2.0% | +5 958 | −1 | **+5 432** |
| −1.0% | +2 979 | −0 | +2 453 |
| 0.0% | −0 | +0 | −526 |
| +1.0% | −2 979 | +0 | −526 |
| **+2.0%** | **−5 958** | **+1** | **−525** |
| +3.0% | −8 938 | +1 | −525 |

> [!note] Neither is better — the option is a purchase of asymmetry
> **The futures hedge is flat.** It removes the loss *and* the gain: at −3% the bank forgoes 8,938 it would otherwise have made.
>
> **The put hedge is a floor.** It costs the premium in every state of the world and in exchange the bank keeps everything above the strike.
>
> **So the premium is the price of the falling-rate upside**, and whether it is worth paying is a view, not a calculation. **R&H's framing is right: options suit managers who "want downside risk protection but do not want to restrict potential gains."**
>
> **The maximum loss to an option buyer is the premium** — which is why an option *bought* is the only instrument in this chapter with a bounded downside. **Writing** one is a different business entirely, and §9's table says why.

### 8. Caps, floors and collars

**All three are options on an interest rate**, sold heavily to customers as fee income.

*(All three of R&H's examples verified:)*

| | |
|---|---|
| **cap** — \$100mn borrowed, cap 11%, market 12% | rebate $=(0.12-0.11)\times\$100\text{mn}=\mathbf{\$1{,}000{,}000}$ ✓ |
| **floor** — \$10mn loan, floor 7%, prime falls to 6% | rebate $=(0.07-0.06)\times\$10\text{mn}=\mathbf{\$100{,}000}$ ✓ |

**A collar is a purchased cap plus a written floor** *(computed — \$10mn loan, floor 6%, cap 10%)*:

| loan rate | who pays | amount |
|---|---|---|
| 5.0% | customer → bank | 100 000 |
| 8.0% | *no payment* | 0 |
| 12.0% | bank → customer | 200 000 |

> [!note] A collar is cheaper than a cap because it is not free
> **The premium received for writing the floor offsets the premium paid for the cap** — the net can be positive or negative. **What the buyer gave up is the benefit of very low rates.** Cheap protection is always protection with something sold alongside it.

### 9. Securitisation and the cash-flow waterfall

**Pool illiquid loans, move them to a bankruptcy-remote special-purpose entity, and sell securities against the pool.** The originator gets its money back, keeps the servicing fee, and takes the loans off its balance sheet.

*(Verified — R&H's waterfall, book pp. 296–297, on a pool yielding 20%:)*

| | |
|---|---|
| coupon promised to security investors | 7.00% |
| **expected default (charge-off) rate** | **4.00%** |
| servicing fee | 2.00% |
| advisory + underwriting fee | 1.00% |
| liquidity enhancement fee | 1.00% |
| **residual to the originator ("excess spread")** | **5.00%** |
| **sum** | **20.00%** ✓ |

**Now stress it** *(computed)*:

| actual default rate | excess spread left | investors' coupon | short by |
|---|---|---|---|
| 4.00% *(budgeted)* | +5.00% | 7.00% | — |
| 6.00% | +3.00% | 7.00% | — |
| **9.00%** | **0.00%** | **7.00%** | — |
| 10.00% | −1.00% | 6.00% | 1.00% |
| 14.00% | −5.00% | 2.00% | 5.00% |

> [!note] The excess spread is the first-loss piece
> **Defaults can more than double, from the budgeted 4% to 9%, before a single investor loses a cent.** At 9.01% the losses start landing on people who believe they hold a *security*.
>
> **So the originator's 5% "residual" is not a profit margin — it is the equity tranche of a leveraged structure**, and it is wiped out first. That is a very different thing from a fee, and it is reported like a fee.

### 10. ⚠️ Tranching and correlation — the chapter's result

**Divide the pool's losses into tranches: equity absorbs 0–5%, mezzanine 5–20%, senior 20–100%.** The senior tranche is safe because it takes nothing until a fifth of the pool has defaulted — **and that safety is a statement about how likely the loans are to default *together*.**

*(Computed — a one-factor model, $X_i=\sqrt{\rho}\,M+\sqrt{1-\rho}\,Z_i$ with loan $i$ defaulting when $X_i<\Phi^{-1}(p)$; 1,000 loans, $p=5\%$, 200,000 simulations:)*

| $\rho$ | **mean pool loss** | $P(\text{loss}>20\%)$ | equity | mezzanine | **SENIOR** |
|---|---|---|---|---|---|
| **0.00** | **4.9996%** | 0.0000% | 94.498% | 1.831% | **0.0000%** |
| 0.05 | 4.9931% | 0.0135% | 80.789% | 6.356% | 0.0003% |
| 0.20 | 4.9911% | 2.3045% | 62.348% | 11.551% | 0.1764% |
| 0.40 | 4.9924% | 5.8275% | 46.444% | 13.223% | 0.8585% |
| **0.60** | **5.0329%** | 7.6380% | 33.455% | 12.777% | **1.8044%** |

> [!warning] The mean pool loss is 5% in every single row
> **Correlation moves no expected loss into the pool at all. It only moves loss *up the capital structure*** — out of the equity tranche (94.5% → 33.5%) and into the senior one (0.0000% → 1.8044%).
>
> **At $\rho=0$ the senior tranche is genuinely untouchable**: 200 of 1,000 independent loans defaulting when each has a 5% chance is arithmetically almost impossible, and 200,000 simulations produced it zero times. **At $\rho=0.60$, backed by the same loans, with the same 5% average default rate, it is losing real money.**
>
> **So the AAA rating was a claim about correlation, not about credit quality — and nothing about the loans had to change for it to be wrong.** US house prices had never fallen nationally at once; when they did, $\rho$ moved and every senior tranche repriced together.

> [!note] This is [[02 - Organization, Structure and Market Entry|ch. 02]]'s result, in a place nobody was looking
> Ch. 02 derived $\sigma_{\text{comb}}=\sigma\sqrt{(1+\rho)/2}$ to explain why crossing state lines did not diversify a bank. *(Recomputed:)*
>
> | $\rho$ | risk reduction from pooling |
> |---|---|
> | 0.0 | 29.3% |
> | 0.5 | 13.4% |
> | 0.9 | **2.5%** |
> | 1.0 | **0.0%** |
>
> **Same mathematics, same failure, two chapters apart: pooling only diversifies what is not already moving together.** Ch. 02 used it to puncture the case for bank mergers; here it prices a trillion-dollar market. **Notice that both times the *average* was fine and the *joint behaviour* was the whole story.**

### 11. ⚠️ The credit default swap, and wrong-way risk

**A CDS is a put option on a borrower's solvency**: the buyer pays a fee, the seller pays out if default occurs. *(Verified — R&H's example, book p. 313: a 5-year \$100mn construction loan protected for ½% of face → **\$500,000 per year** ✓.)*

**But protection is only worth what the guarantor can pay.** *(Computed — $P(\text{loan defaults})=5\%$, $P(\text{guarantor fails})=2\%$, correlated through a common factor:)*

| $\rho$(loan, guarantor) | **P(paid \| default)** |
|---|---|
| 0.00 | **98.21%** |
| 0.30 | 93.09% |
| 0.60 | 84.08% |
| **0.90** | **65.96%** |

> [!warning] The guarantor is most likely to fail exactly when the claim is made
> **At $\rho=0$ the protection pays 98% of the time it is needed — essentially just $1-q$. At $\rho=0.90$ it pays two times in three.** The buyer paid for insurance and received something worth a third less, **and the shortfall appears only in the state of the world the insurance was bought for.**
>
> **This is wrong-way risk**, and it is why AIG's protection evaporated at the moment it mattered. **The CDS did not destroy the credit risk. It converted credit risk on a *borrower* into counterparty risk on a *guarantor*** — and then the whole market bought from the same few guarantors, which is what made $\rho$ high in the first place.

### 12. What every hedge in this chapter has in common

| instrument | transfers risk to | fails when |
|---|---|---|
| **futures** | a speculator | the basis moves (§3), or convexity is mismatched (§2) |
| **options (bought)** | the option writer | — *the loss is capped at the premium* |
| **swaps** | the counterparty | the counterparty defaults |
| **securitisation** | security investors | default correlation rises (§10) |
| **CDS** | the guarantor | the guarantor fails *with* the borrower (§11) |

> [!warning] None of these destroys risk
> **Each one *moves* it, and each has a state of the world in which the party it was moved to cannot pay.** The 2007–09 crisis was that state for the bottom three rows simultaneously.
>
> **This is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s framing arriving at its sharpest form.** Ch. 01 said the spread and the interest-rate risk are the same thing, so risk is priced rather than avoided. **This chapter shows that hedging does not repeal that** — it relocates the risk to whoever was willing to hold it, and the price of the hedge is exactly the market's estimate of how likely they are to be there.
>
> **The one genuine exception is a *purchased* option**, whose downside is bounded by the premium. **Everything else in the table is a promise from somebody.**

## ✏️ Exercises

**1. (Futures.)** (a) Derive the contract-count formula and apply it. (b) What has the bank achieved that ch. 05 said it could not? (c) Why does the notional differ between the futures and swap hedges?

> [!example]- Solution
> **(a) Set the futures gain equal to the loss in net worth and solve for $N$.**
>
> From ch. 05, $\Delta NW=-D_{\text{gap}}\times\frac{\Delta i}{1+i}\times TA$. One futures contract changes in value by $-D_F\times F_0\times\frac{\Delta i}{1+i}$, so $N$ contracts change by $N$ times that. **Setting the two equal and cancelling $\frac{\Delta i}{1+i}$ — which is why the answer does not depend on the size of the shock:**
> $$N=\frac{D_{\text{gap}}\times TA}{D_F\times F_0}$$
>
> *(Verified on R&H's own example, book p. 269: $D_{\text{gap}}=4-0.92\times2=2.16$, giving $N=2.16\times500{,}000{,}000/(9\times99{,}700)=\textbf{1203.6}$, matching the book's "about 1,200". Its p. 267 single-contract figure also checks to the cent: $-\$8{,}385.98$.)*
>
> **For ch. 05's bank** *(computed)*: $N=1.9374\times163{,}000{,}000/897{,}300=351.94\to$ **short 352 contracts**, and the net across every shock from −2% to +3% is **±1 thousand — pure rounding.**
>
> **Short, not long, because the duration gap is positive**: rising rates hurt, so the bank needs a position that *profits* from rising rates, and a short futures position does. **A negative duration gap would call for a long hedge.**
>
> **(b) $D_{\text{gap}}=0$ without shortening a single loan.**
>
> **Ch. 05 §7 computed the alternative: immunising the balance sheet meant cutting asset duration from 3.20 to 1.26 years or lengthening liabilities from 1.40 to 3.55** — either of which abolishes the maturity transformation that generates the spread ([[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §4).
>
> **352 contracts, with a notional of 21.5% of assets, achieve the same protection and leave the loan book untouched.** That is the entire case for derivatives in bank management, and it is why R&H devotes two chapters to it.
>
> **The secondary advantages R&H notes:** only a margin must be posted rather than the full notional (the mark-to-market process makes this safe for the exchange), commissions are low, and the exchange clearinghouse removes counterparty risk — **which the OTC swap in (c) does not.**
>
> **(c) Because the required notional is inversely proportional to the instrument's duration.**
>
> $$N\times F_0=\frac{D_{\text{gap}}\times TA}{D_F}$$
>
> *(Computed: T-bond futures $D_F=9\Rightarrow$ **21.5%** of assets; the swap's net duration is $4.4651-0.25=4.2151\Rightarrow$ **46.0%** of assets.)*
>
> **The longer the hedging instrument, the less of it you need** — you are buying duration, and a longer instrument sells more per dollar.
>
> **But §2's warning attaches here.** Convexity grows roughly with the *square* of duration, so **the instrument that requires the smallest notional also carries the worst convexity mismatch.** The cheapest hedge on a first-order view is the most wrong on a second-order view, which is not a coincidence — it is the same property seen twice.

**2. (Hard — where the futures hedge actually leaks.)** (a) The §1 table shows a residual of ±1. Why is §2's residual 233 at the same shock? (b) Why is it negative in *both* directions? (c) What is basis risk and how does it compare? (d) What should a bank do?

> [!example]- Solution
> **(a) Because §1 measures the model against itself and §2 measures the model against reality.**
>
> **§1 computes both legs with the duration formula.** The formula was *constructed* to make them cancel, so of course they cancel — **the ±1 residual is the rounding of 351.94 contracts to 352 and nothing else.** A table like §1 can never detect an error in the model it is built from.
>
> **§2 reprices both legs exactly and compares.** *(Computed: at +2% the true net worth change is −5,667 while the model says −5,958; the futures leg is wrong in the other direction; the net is **−233, or −1.46% of equity**.)*
>
> **This is worth stating as a method, because it generalises well beyond banking: a self-consistent calculation is not a verified one.** The vault's rule — recompute every number — means recomputing against something *independent*, which here is exact repricing.
>
> **(b) Because the hedge sells more convexity than the balance sheet owes.**
>
> *(Computed: residual **−13.44%** of equity at −5% and **−7.81%** at +5%.)*
>
> **Ch. 05 §5 established that the price–yield curve is convex, so duration always predicts a worse price than reality — in both directions.** That is a *benefit* to whoever holds the instrument.
>
> **A short position reverses the sign of that benefit.** The bank is short 9-year-duration contracts, and convexity grows roughly with the square of duration, so:
>
> - the **balance sheet** (net duration 1.94) has a little convexity, working *for* the bank;
> - the **short futures leg** (duration 9) has roughly $(9/1.94)^2\approx21\times$ as much per dollar of duration, working *against* it.
>
> **The second effect dominates, so the net is negative whichever way rates move.** The bank has, without intending to, **sold a volatility position** — it now profits from rates staying still and loses from any large move in either direction.
>
> **And equation (8-13) cannot see it**, because it equates first derivatives and the entire residual is second-order. **A first-order formula reports perfect success precisely when the exposure it leaves is purely second-order.**
>
> **(c) Basis is the difference between cash and futures prices, and it is comparable in size.**
>
> $$\text{basis}=\text{cash price}-\text{futures price}$$
>
> **The §1 hedge assumed the futures price tracks the cash market one-for-one.** *(Computed at a +2% shock: $b=0.98\to$ −0.74% of equity; **$b=0.95\to$ −1.86%**; $b=0.90\to$ −3.72%.)*
>
> **So a 5% tracking error costs slightly more than the convexity mismatch at the same shock (1.86% vs 1.46%)** — two independent leaks of comparable size, both invisible to the formula.
>
> **Why the basis moves:** the futures contract references a *specific* deliverable security, and the bank's assets are not that security. Supply and demand in the futures market, the delivery option held by the short, and differing liquidity all cause the two to diverge. **R&H's own framing is the honest one — hedging "reduces (but usually does not completely eliminate) overall risk exposure."**
>
> **(d) Four things, in order of how much they help.**
>
> 1. **Hedge with an instrument whose duration is near the exposure's.** Most of §2's leak comes from hedging a 1.94-year net exposure with a 9-year contract. A shorter contract needs a larger notional (Exercise 1(c)) and mismatches far less.
> 2. **Test the hedge by exact repricing, not by the formula that produced it.** Compute the actual value of both legs at ±100, ±200, ±300 bp — the same rule ch. 05 §5 reached for duration itself.
> 3. **Re-hedge as rates move.** $D_{\text{gap}}$ and $N$ are computed at today's yield and both drift. A static hedge decays; the second-order error is exactly what re-hedging removes.
> 4. **Hold capital against the residual** ([[10 - Capital Adequacy and Basel|ch. 10]]). **A hedged position is not a riskless one**, and treating it as riskless is how a hedging desk becomes a trading desk without anybody deciding to.

**3. (Hard — securitisation and correlation.)** (a) What is securitisation and who bears the first loss? (b) Interpret the tranche table. (c) Why is this ch. 02's result? (d) What does the CDS table add? (e) What is the common failure?

> [!example]- Solution
> **(a) Pool illiquid loans, sell securities against the pool — and the *originator* bears the first loss.**
>
> The originator sells loans to a bankruptcy-remote **special-purpose entity**, which issues securities against them. A **credit rating agency** rates them; **credit and liquidity enhancers** guarantee them; a **servicer** (usually the originator) collects payments. The originator gets its funds back, removes the loans from its balance sheet, and keeps a servicing fee.
>
> *(Verified — R&H's waterfall sums to the 20% gross yield exactly: 7% coupon + 4% expected defaults + 2% servicing + 1% advisory + 1% liquidity + 5% residual.)*
>
> **The 5% residual — the "excess spread" — is the first-loss piece.** *(Computed: defaults can run from the budgeted 4% all the way to **9%** before any investor loses a cent; at 10% the coupon falls to 6%; at 14% to 2%.)*
>
> **So the originator's residual is not a fee, it is the equity tranche of a leveraged structure** — and it is reported alongside genuine fee income, which is exactly what made pre-2007 securitisation look like a fee business rather than a credit business.
>
> **The regulatory point R&H makes in a footnote is worth surfacing:** moving loans off the balance sheet lowers total assets while capital is unchanged, so the **capital ratio improves** ([[10 - Capital Adequacy and Basel|ch. 10]]). **A structure that reduces measured risk without reducing actual risk is a structure that will be used for that reason.**
>
> **(b) The mean pool loss is 5% in every row. Correlation moves loss up the capital structure, not into the pool.**
>
> *(Computed across $\rho$: senior expected loss **0.0000% → 0.0003% → 0.1764% → 0.8585% → 1.8044%**, while equity goes **94.5% → 33.5%** and the mean pool loss never leaves 5%.)*
>
> **The senior tranche's safety was never about credit quality.** It took nothing until 20% of the pool defaulted, and **at $\rho=0$ that is arithmetically almost impossible** — 200 of 1,000 loans each defaulting with probability 5%, which 200,000 simulations produced zero times.
>
> **At $\rho=0.60$ the same tranche, the same loans, the same 5% average default rate, loses real money.** *(And note $P(\text{pool loss}>20\%)$ rising from 0.0000% to 7.6380% — the tail is the entire story, and the mean is blind to it.)*
>
> **So the AAA rating was a claim about correlation, not about credit quality**, and **nothing about the underlying loans had to change for it to be wrong.** US house prices had never fallen nationally at the same time; when they did, $\rho$ moved and every senior tranche in the market repriced together — which is also why the losses were *correlated across institutions*, turning a valuation problem into a systemic one.
>
> **(c) Because it is the same mathematics as [[02 - Organization, Structure and Market Entry|ch. 02]]'s.**
>
> Ch. 02 derived $\sigma_{\text{comb}}=\sigma\sqrt{(1+\rho)/2}$ to explain why banks crossing state lines got no real diversification. *(Recomputed: **29.3%** risk reduction at $\rho=0$, **2.5%** at $\rho=0.9$, **0.0%** at $\rho=1$.)*
>
> **Same principle, two chapters apart, at completely different scales:** ch. 02 used it to puncture the standard rationale for bank mergers; here it prices a trillion-dollar securities market. **Pooling only diversifies what is not already moving together.**
>
> **And in both cases the *average* was fine and the *joint behaviour* was the whole story** — which is the general lesson, and the reason a portfolio model that reports only expected loss is not a risk model.
>
> **(d) That the same failure applies to the instrument sold to fix it.**
>
> *(Verified: R&H's CDS fee, ½% of a \$100mn loan = **\$500,000** per year. Computed: with $P(\text{default})=5\%$ and $P(\text{guarantor fails})=2\%$, the protection pays **98.21%** of the time at $\rho=0$ but only **65.96%** at $\rho=0.90$.)*
>
> **The guarantor is most likely to be insolvent exactly when the claim is made**, because the same recession drives both. **That is wrong-way risk** — and it is not a small correction: a third of the protection's value disappears, and it disappears *only* in the state the buyer was insuring against.
>
> **The CDS did not destroy credit risk. It converted credit risk on a borrower into counterparty risk on a guarantor** — and because the whole market bought from the same few guarantors, **the act of buying protection is what made $\rho$ high.** AIG is the canonical case.
>
> **(e) Every instrument here transfers risk to somebody, and each has a state where that somebody cannot pay.**
>
> | instrument | transfers to | fails when |
> |---|---|---|
> | futures | a speculator | the basis moves; convexity mismatch |
> | **options (bought)** | the writer | **— loss capped at the premium** |
> | swaps | the counterparty | the counterparty defaults |
> | securitisation | investors | correlation rises |
> | CDS | the guarantor | the guarantor fails *with* the borrower |
>
> **2007–09 was that state for the bottom three rows simultaneously**, which is why it was a systemic event rather than a series of losses.
>
> **The purchased option is the one genuine exception**, because its downside is bounded by the premium and requires no promise to be kept. **Everything else on the list is somebody's promise**, and its value is the probability they can honour it — which is highest when you don't need it.
>
> **This is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s framing at full strength: risk in banking is priced, transferred and capitalised — never abolished.** Which is why [[10 - Capital Adequacy and Basel|ch. 10]]'s capital sits behind all of it.

## 📝 Summary

- **The chapter delivers what ch. 05 promised**: 352 short T-bond futures contracts close ch. 05's **1.9374-year duration gap** with a notional of only **21.5% of assets** and **the loan book untouched** — the residual is pure rounding.
- **$N=D_{\text{gap}}\times TA/(D_F\times F_0)$** *(R&H's own example verified: $2.16\times500\text{mn}/(9\times99{,}700)=\mathbf{1203.6}$ vs the book's "about 1,200"; its single-contract figure checks to the cent at **−\$8,385.98**)*.
- **⚠️ But exact repricing shows the hedged bank losing at both ends** *(computed: **−1.46%** of equity at +2%, **−7.81%** at +5%, **−13.44%** at −5%)*. **The hedge shorts a 9-year instrument against a 1.94-year net exposure, selling far more convexity than it owed.** Equation (8-13) matches first derivatives and cannot see it.
- **⚠️ Basis risk leaks a comparable amount**: a 5% tracking error costs **1.86%** of equity at a +2% shock. **The hedge did not remove risk; it exchanged interest-rate risk for basis risk.**
- **Swaps run on comparative advantage** *(verified: quality spreads of 2.50% fixed vs 1.75% floating → a **0.75%** total gain, and the book's 0.50%/0.25% split exhausts it exactly)*. **Equalise the spreads and the gain is zero** — absolute advantage explains nothing.
- **A pay-fixed swap closes the same gap** with a notional of **74,921 = 46.0% of assets**. **Required notional is inversely proportional to instrument duration** — so the instrument needing the least notional carries the worst convexity mismatch.
- **⚠️ Notional is not exposure.** *(Computed: a +2% move exchanges **2.0% of notional** in cash; R&H's **\$225 trillion** across 1,159 banks is **21.1×** their assets.)* **Netting means only the difference is ever at risk** — but netting says nothing about whether the counterparty can pay at all.
- **A futures hedge is flat; a bought option is a floor.** *(Computed: the put costs **526 = 3.29% of equity** in every state and keeps everything above the strike; at −3% the futures-hedged bank forgoes **8,938**.)* **The premium is the price of asymmetry.**
- **Caps, floors and collars all verified** — **\$1,000,000** cap rebate, **\$100,000** floor rebate. **A collar is a purchased cap plus a *written* floor**: cheaper because something was sold.
- **The securitisation waterfall sums to 20% exactly**, and the **5% excess spread is the first-loss piece** — *(computed: defaults can run **4% → 9%** before any investor loses a cent)*. **The originator's residual is an equity tranche reported like a fee.**
- **⚠️ The chapter's result: tranching. Mean pool loss is 5.00% at every correlation; the senior tranche's expected loss goes 0.0000% → 1.8044%** as $\rho$ goes 0 → 0.60. **Correlation moves no loss into the pool — only up the capital structure.** The AAA was a claim about correlation, and **nothing about the loans had to change for it to be wrong.**
- **This is [[02 - Organization, Structure and Market Entry|ch. 02]]'s $\sigma\sqrt{(1+\rho)/2}$ again** *(recomputed: **29.3%** risk reduction at $\rho=0$, **2.5%** at 0.9, **0%** at 1)* — **pooling only diversifies what is not already moving together**, and both times the average was fine while the joint behaviour was everything.
- **⚠️ Wrong-way risk kills the CDS in the state it was bought for** *(computed: protection pays **98.21%** of the time at $\rho=0$, **65.96%** at $\rho=0.90$)*. **It converted credit risk on a borrower into counterparty risk on a guarantor** — and everyone bought from the same few guarantors.
- **⚠️ None of these instruments destroys risk; each moves it, and each has a state where the recipient cannot pay.** **The purchased option is the only exception** — its downside is the premium. **Everything else is somebody's promise.**

## ⚠️ Important Notes

1. **Short hedge for a positive duration gap (rising rates hurt); long hedge for a negative one.** Get this backwards and the hedge doubles the exposure.
2. **$\Delta i/(1+i)$ cancels out of the contract count** — $N$ does not depend on the size of the shock you are hedging.
3. **⚠️ A self-consistent calculation is not a verified one.** Testing a duration hedge with the duration formula always reports success; reprice both legs exactly.
4. **⚠️ Match the instrument's duration to the exposure, not just the dollar sensitivity.** A short position in a long instrument sells convexity and loses in *both* directions.
5. **Re-hedge as rates move.** $D_{\text{gap}}$ and $N$ are computed at today's yield and both drift; a static hedge decays.
6. **Basis risk is what remains after a "perfect" futures hedge**, and it is comparable in size to the convexity residual.
7. **Exchange-traded futures carry clearinghouse protection; OTC forwards and swaps do not.** That difference is the whole of counterparty risk.
8. **Swap gains come from a *difference of spreads*, not from one party being cheaper.** If the fixed and floating quality spreads are equal, there is no gain.
9. **⚠️ Never quote notional as exposure.** The cash at risk is the net payment; the \$225 trillion figure is contract size.
10. **A bought option's maximum loss is the premium. A written one's is unbounded** — the two are not variations on a theme.
11. **A collar is cheaper than a cap because a floor was sold.** There is no free protection; find what was given up.
12. **⚠️ The originator's "excess spread" is an equity tranche, not fee income.** It absorbs the first losses and is reported alongside genuine fees.
13. **⚠️ A tranche's rating is a claim about default correlation.** Expected pool loss is identical across correlations; only the distribution among tranches changes.
14. **Expected loss is not a risk measure for a tranched structure.** $P(\text{pool loss}>20\%)$ moved from 0.0000% to 7.6380% while the mean never left 5%.
15. **⚠️ Buying protection from a counterparty correlated with your risk is wrong-way risk** — and concentration in a few guarantors *creates* that correlation.
16. **Securitisation improves the capital ratio without improving the balance sheet.** Expect any structure that reduces *measured* risk to be used for that reason ([[10 - Capital Adequacy and Basel|ch. 10]]).
17. **A hedged position is not a riskless one.** Treating it as riskless is how a hedging desk becomes a trading desk without anyone deciding to.

> [!warning] Gaps in the source material
> **R&H ch. 8–9 extract well as prose** — the futures mechanics, the swap discussion, the securitisation process and the credit-derivatives material all came through readably. **Book page $n$ = PDF page $n+18$; ch. 8 is PDF pp. 273–310 and ch. 9 pp. 311–338.** *(The four standing extraction hazards in `00-Index.md` all apply; §8-3's text shows the comma-for-hyphen fault heavily — "off,balance,sheet", "mark,to,market", "leverage,adjusted".)*
>
> **⚠️ A new observation: the running headers in these two chapters are OCR'd, not text** — they arrive as *"Loan Sal.es"*, *"Credit Starulbys"*. **The body text is clean, so this affects navigation only, but it confirms the file mixes text-layer and scanned pages.** Do not rely on header matching to locate chapters here.
>
> **Lost, as expected**: Exhibits 8-1 (derivative usage), 8-3 (the trade-off diagrams), 8-7 (the swap schematic), 9-1/9-2 (the securitisation flow), 9-8/9-9/9-11 (swap schematics). **Exhibit 8-1's *figures* survived as a stray column of numbers** and are used in §6; **Exhibits 8-2 and 8-4 (the WSJ futures and options quotes) extracted but are garbled** ("f1.oor brokers", "97,5400" for 97.5400) and are **not** used for any calculation here.
>
> **Every one of R&H's seven worked figures was recomputed and all seven check out:** the 1,200-contract hedge (1203.6), the −\$8,385.98 single-contract change, the 0.75% swap gain and its 0.50/0.25 split, the \$1,000,000 cap rebate, the \$100,000 floor rebate, the 20% waterfall, and the \$500,000 CDS fee. **The errata table stays empty.**
>
> *(Two of these initially reported as mismatches under exact float comparison — `(0.12−0.11)×100mn` is not exactly `1e6` in binary floating point. **The book was right and the test was wrong**; corrected with a tolerance before it reached this note. Flagged because filing a false erratum against a correct source is the worse failure of the two.)*
>
> **Additions beyond the source.** **R&H explains these instruments clearly and its worked examples are sound. What is added is stress-testing its formulas past the range where they hold, and one substantial piece of modelling:**
>
> - **§1 applies eq. (8-13) to ch. 05's bank** rather than to a fresh example, so the two chapters share one balance sheet and the hedge can be checked against a loss the reader already knows.
> - **⚠️ §2 is mine and is the chapter's most useful correction.** R&H presents eq. (8-13) without testing it. **Repricing both legs exactly shows the "fully hedged" bank losing 1.46% of equity at +2% and 7.81% at +5% — negative in both directions.** The diagnosis (a short position in a 9-year instrument against a 1.94-year exposure sells convexity) and the resulting rule (match instrument duration; test by repricing, not by the formula) are additions.
> - **§3 quantifies basis risk.** R&H defines basis and says the risk is "usually less" than cash-market risk; **computing the cost at $b=0.98/0.95/0.90$ makes it comparable to the convexity leak.**
> - **§4's sensitivity of the swap gain to the floating spread** (showing it vanishing at 2.50%) is mine; R&H gives only the single case.
> - **§5's swap-notional formula and §6's notional-vs-cash comparison** are mine. R&H reports the \$225tn notional and explains netting separately; **computing the 21.1× ratio and the 2.0%-of-notional cash flow joins them.**
> - **§7's side-by-side futures/option payoff table** is mine; R&H describes the asymmetry in prose.
> - **§9's stress of the waterfall** (defaults 4% → 14%, showing the 5% excess spread absorbing everything to 9%) is mine. **R&H presents the waterfall as a static list and never asks what happens when the 4% assumption fails**, which is the only interesting question about it.
> - **⚠️ §10 is entirely mine and is the chapter's main result.** R&H describes tranching and says CDO credit risk was hard to estimate and ratings "often not carefully done", but **offers no model and no number.** The one-factor simulation, the finding that **mean pool loss is invariant to correlation while senior-tranche loss is not**, and the link back to ch. 02's $\sigma\sqrt{(1+\rho)/2}$ are additions. *(The one-factor Gaussian copula is standard post-crisis material the 9th edition predates in its exposition.)*
> - **§11's wrong-way-risk calculation** is mine; R&H notes counterparty risk in a CDS but does not correlate the guarantor's failure with the borrower's.
> - **§12's unifying table** — that every instrument transfers risk and each has a state where the recipient cannot pay, with the purchased option as the sole exception — is my framing.
>
> **Deliberately compressed.** **The contract-specification detail** (margins per contract, tick sizes, the 32nds quoting convention, expiry months, exchange listings) is represented by a mention; it is reference material that dates quickly and the WSJ exhibits are garbled anyway. **R&H §8-5 on accounting and regulation** (FAS 133 hedge accounting) is noted only in passing — it is a financial-accounting topic and post-dates by Dodd-Frank changes the 9th edition partly predates. **Loan sales and standby letters of credit (R&H §§9-3, 9-4)** are compressed: their risk-transfer logic is the same as securitisation's and is captured in §12's table, while their pricing belongs with [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s credit material. **Credit-linked notes and total-return swaps** are omitted as variants of the two instruments modelled. **Option *pricing*** (Black–Scholes and its interest-rate analogues) is out of scope for this course and is not in R&H either; §7 takes the premium as given.

**Previous:** [[05 - Interest-Rate Risk - Gap and Duration]] · **Next:** [[07 - The Investment Portfolio]]
