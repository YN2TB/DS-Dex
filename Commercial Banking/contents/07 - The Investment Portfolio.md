---
subject: Commercial Banking
chapter: 7
tags: [ds, banking, investments, yield, ytm, duration, convexity, barbell, tax, pledging]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 10"
---

# The Investment Portfolio

**A bank's securities portfolio earns less than its loans, and that is the point.** §6 computes the give-up: **3.75 percentage points**, costing a bank like ch. 05's about **1,222 thousand a year** on a 20% allocation. Nobody holds it for the return. It is held for **liquidity, for pledging, and for a place to put money when loan demand is weak** — and the pledging requirement is a hard legal constraint, not a preference.

**Two results carry the chapter.**

**§1 shows the same T-bill having three different "yields"** — 7.91%, 8.19% and 8.44% — depending only on which convention is used, and **the smallest of the three is the one that gets quoted.**

**§5 is the one worth keeping.** Three portfolios with **identical duration of exactly 5.0000 years** have convexities of **26.70, 32.63 and 40.94**, and **the barbell beats the bullet at every non-zero shock in both directions.** That is [[06 - Hedging with Derivatives|ch. 06]] §2's convexity leak, turned from an accident into a portfolio choice.

> [!warning] An error in the source, verified
> **R&H states a yield to maturity of 10.74% for a bond whose own stated equation gives 10.68%.** Substituting the book's figure prices the note at **\$898.07, not \$900**. Five conventions tested; none reproduces it. **See the errata table in `00-Index.md`.**

## 📘 Main Knowledge

### 1. ⚠️ Three yields, one instrument

*(Computed — a 91-day T-bill, par \$10,000, bought for \$9,800:)*

| measure | formula | value |
|---|---|---|
| **bank discount rate** | $\frac{\text{par}-P}{\textbf{par}}\times\frac{\textbf{360}}{n}$ | **7.9121%** |
| bond-equivalent yield | $\frac{\text{par}-P}{\textbf{P}}\times\frac{\textbf{365}}{n}$ | 8.1857% |
| effective annual yield | $\left(\frac{\text{par}}{P}\right)^{365/n}-1$ | **8.4407%** |

> [!warning] The quoted number is the smallest of the three
> **Same instrument, same cash flows, three answers, spanning 0.53 percentage points** — and **the bank discount rate is the one quoted in the market.**
>
> **Two conventions both push it downward.** It divides the gain by **par** (larger than what you actually paid) and annualises over a **360-day** year (shorter than the real one). Neither is an error; both are conventions from an era of hand calculation.
>
> **The bank discount rate is a price-quoting convention, not a rate of return.** T-bills are issued at a discount and the "rate" is really a way of expressing the price. **Never compare it to a bond's YTM** — the comparison is biased by roughly half a point at these levels, always in the same direction, and it silently makes bills look worse than they are.

### 2. Yield to maturity and holding-period yield

**YTM is the discount rate equating price with the promised cash flows** — and it assumes the security is *held to maturity*.

$$P=\sum_{t=1}^{n}\frac{C}{(1+\text{YTM})^t}+\frac{F}{(1+\text{YTM})^n}$$

> [!warning] ⚠️ R&H's worked example is wrong — verified
> **The book's example** (p. 332): a \$1,000 par T-note, 8% coupon (\$80), 5 years, priced at \$900. **It states YTM = 10.74%.**
>
> *(Computed: **YTM = 10.6842%**, which prices the note at exactly \$900.000000. **At the book's 10.74% the note prices at \$898.07** — its own stated equation is not satisfied.)*
>
> **Four alternative conventions were tested before concluding this** *(all computed)*:
>
> | convention | result |
> |---|---|
> | annual coupons, $n=5$ — **as stated** | **10.6842%** ✓ prices at 900.00 |
> | semiannual coupons, bond-equivalent $2y$ | 10.6299% |
> | semiannual, effective annual | 10.9123% |
> | shortcut: (coupon + accretion)/avg price | 10.5263% |
> | shortcut: (coupon + accretion)/cost | 11.1111% |
>
> **None reproduces 10.74%.**
>
> **And extraction is ruled out** (the discipline [[03 - Bank Financial Statements|ch. 03]] established). The displayed equation *is* garbled — its first coupon renders as `$30` — **but the surrounding prose independently states "8 percent coupon rate (or 1,000 × 0.08 = \$80)", "mature in five years" and "current price is \$900".** The inputs are unambiguous without the equation.
>
> **The correct value is 10.68%.**

**Holding-period yield** is the same calculation for an investor who *sells early*:

$$P=\sum_{t=1}^{h}\frac{C}{(1+\text{HPY})^t}+\frac{P_h}{(1+\text{HPY})^h}$$

*(Verified — the same note sold after 2 years for \$950: **HPY = 11.5154%**, and R&H's 11.51% is that figure truncated. Its footnote gives the calculator inputs — `N=2, PV=−900, Pmt=80, FV=950` — which match exactly.)*

> [!note] The asymmetry is instructive
> **Where R&H showed its working, the number is right. Where it said only "solving using a financial calculator or software reveals", the number is wrong.** A worked calculation invites checking; an appeal to a calculator does not.

**Why HPY exceeds YTM here:** the note was bought at \$900 and sold at \$950, so the price recovery arrived in two years instead of five. *(Computed: the break-even sale price is **\$934.04** — sell above it and HPY > YTM, below it and HPY < YTM.)*

> [!note] The officer's real question
> **YTM and HPY are equal only if the security is held to maturity.** A bank's securities are exactly the assets it sells when loan demand rises or deposits run off — **so the relevant number is almost never the YTM.**
>
> **The question is not "what is the yield" but "what is the yield given when I will be forced to sell"** — and the forced-sale date is set by [[08 - Liquidity and Reserves Management|liquidity needs]], not by the investments officer.

### 3. Tax: the lowest gross yield can win

*(Verified — R&H's comparison at a 35% marginal rate:)*

| instrument | gross yield | taxed? | **after tax** |
|---|---|---|---|
| Aaa corporate bonds | 7.00% | yes | 4.55% |
| prime-rated loans | 6.00% | yes | 3.90% |
| **Aaa municipal bonds** | **5.50%** | **no** | **5.50%** |

**The lowest gross yield wins, by 0.95 points.** *(All three figures match the book.)*

**The tax-equivalent yield** inverts the question:

$$\text{TEY}=\frac{\text{tax-exempt yield}}{1-t}=\frac{5.50\%}{1-0.35}=\mathbf{8.4615\%}$$

*(Book says 8.46% ✓.)* **A taxable bond must yield 8.46% to match a 5.50% municipal.**

> [!note] The break-even tax rate explains a whole market's history
> *(Computed: $0.07(1-t)=0.055\Rightarrow t^*=\mathbf{21.43\%}$.)*
>
> | marginal rate | corporate after tax | municipal | winner |
> |---|---|---|---|
> | 46% *(pre-1986)* | 3.78% | 5.50% | **municipal** |
> | 35% | 4.55% | 5.50% | **municipal** |
> | **21%** | **5.53%** | 5.50% | **corporate** |
> | 0% | 7.00% | 5.50% | corporate |
>
> **R&H reports that banks once held nearly a quarter of all state and local debt and that their share collapsed. This is the arithmetic of it.** The top corporate bracket fell from 46% to 35%, fewer issues qualified, and interest on borrowings to buy municipals stopped being fully deductible.
>
> **Nothing about the bonds changed.** Which is [[06 - Hedging with Derivatives|ch. 06]]'s lesson in another key: **the ranking of two investments reversed with no change in either investment** — there it was correlation, here it is the tax rate. **A ranking that depends on a parameter outside the assets is not a property of the assets.**
>
> *(Tax-exempt institutions — credit unions, mutual funds — face none of this, which is why they hold different portfolios than banks do. R&H also notes **bank-qualified bonds**, issued by governments placing under \$10mn a year, which preserve an 80% interest deduction.)*

### 4. What the officer is actually choosing between

R&H lists ten factors: **expected return, tax exposure, interest-rate risk, credit risk, business risk, liquidity risk, call risk, prepayment risk, inflation risk, and pledging requirements.**

> [!note] Three of these are options written against the bank
> **Call risk** (the issuer redeems when rates fall), **prepayment risk** (mortgage borrowers refinance when rates fall) and **the call feature generally** all share one structure: **the counterparty gets to choose, and chooses when it hurts the bank.**
>
> **That is negative convexity** — the same quantity as §5, with the sign reversed. **A callable bond's price rises less than a straight bond's when rates fall, because the call caps it**, while falling just as far when rates rise. **[[06 - Hedging with Derivatives|Ch. 06]] §7's rule applies exactly: a written option has unbounded downside, and a bank holding callable or mortgage-backed paper has written one without being paid a visible premium for it.**

### 5. ⚠️ Maturity strategy: identical duration, different convexity

R&H describes five strategies — **ladder** (equal amounts in each maturity), **front-end load** (all short), **back-end load** (all long), **barbell** (split between short and long), and **rate expectations** (shift with the forecast).

**The interesting comparison holds duration constant so that only the *shape* differs.** *(Computed — three portfolios of zeros, all yielding 6%, all with Macaulay duration of exactly 5.0000 years:)*

| portfolio | duration | **convexity** |
|---|---|---|
| **bullet** — all 5-year | 5.0000 | **26.6999** |
| **ladder** — equal weights, 1–9 years | 5.0000 | 32.6332 |
| **barbell** — 50% 1-year, 50% 9-year | 5.0000 | **40.9398** |

**The barbell has 53.3% more convexity than the bullet at identical duration.** *(Exact value change per \$1:)*

| shock | bullet | ladder | barbell | **barbell − bullet** |
|---|---|---|---|---|
| −3.0% | +15.4365% | +15.7539% | +16.1986% | **+0.7620%** |
| −1.0% | +4.8535% | +4.8849% | +4.9289% | +0.0754% |
| 0.0% | 0.0000% | 0.0000% | 0.0000% | 0.0000% |
| +1.0% | −4.5864% | −4.5583% | −4.5191% | +0.0673% |
| **+3.0%** | **−13.0245%** | −12.7985% | **−12.4820%** | **+0.5425%** |

> [!warning] The barbell wins at every non-zero shock, in both directions
> **Not "usually" and not "on average" — at every shock tested, up and down.** Duration is identical, so the first-order effect cancels exactly and **what is left is pure convexity.**
>
> **This is [[06 - Hedging with Derivatives|ch. 06]] §2's quantity, with the sign flipped.** There, shorting a 9-year contract against a 1.94-year exposure made the bank *short* convexity by accident and it lost in both directions. **Here the bank can be *long* convexity on purpose.** Same mathematics; one is a mistake and the other is a strategy.
>
> **So why does anyone hold a bullet? Because convexity is not free.** *(Computed — how far rates must move for the barbell's convexity to repay a yield give-up:)*
>
> | yield given up | barbell wins if rates move more than |
> |---|---|
> | 0.00% | *any* move — it dominates outright |
> | 0.05% | ±0.86% |
> | 0.10% | ±1.23% |
> | 0.20% | ±1.76% |
>
> **An efficient market must therefore charge for convexity**, because otherwise everybody would hold the barbell. **The price is a lower yield, and how much lower is a question about the shape of the yield curve — which this subject deliberately does not answer** *(see the boundary in `00-Index.md`; term-structure theory belongs to [[Monetary and Financial Theories/contents/00-Index|Mishkin]])*.

**And the reason smaller banks actually run ladders is not convexity at all.** *(Computed — cash thrown off at par each year, with no security sold:)*

| year | bullet | **ladder** | barbell |
|---|---|---|---|
| 1 | 0% | **11.11%** | 50% |
| 2–4 | 0% | **11.11%** each | 0% |
| 5 | 100% | **11.11%** | 0% |

> [!note] The ladder is a liquidity strategy, not a yield strategy
> **11.11% of the portfolio matures every year, at par, with no sale — and therefore no realised capital loss no matter where rates are.** The bullet delivers nothing for four years and then everything.
>
> **That is why R&H reports the ladder is "particularly popular among smaller institutions": it requires no rate forecast and no trading desk.** A strategy whose main virtue is that it cannot be got badly wrong is a good strategy for an institution that cannot afford to get it badly wrong.
>
> **The rate-expectations strategy is the opposite** — R&H's own summary concedes it "maximizes the potential for earnings (and also for losses)". **It is not a portfolio strategy; it is a directional bet on rates**, and it should be recognised and capitalised as one.

### 6. Why hold the portfolio at all

*(Computed — a bank earning 7.25% on loans and 3.50% on Treasuries, on ch. 05's \$163mn balance sheet:)*

| allocation | securities held | **annual give-up** |
|---|---|---|
| 10% | 16 300 | 611 |
| **20%** | **32 600** | **1 222** |
| 30% | 48 900 | 1 834 |

**The give-up is 3.75 percentage points, and it is deliberate.** R&H's reasons: **liquidity, pledging, income stabilisation, diversification away from the local loan book, and somewhere to put funds when loan demand is weak.**

> [!warning] Pledging is a constraint, not a preference
> **Government deposits must be collateralised by securities.** A pledged security is **encumbered** — it cannot be sold to meet a liquidity need.
>
> *(Computed: with 35% of a 32,600 portfolio pledged, **only 21,190 is genuinely available.**)*
>
> **So a liquidity ratio computed from total securities overstates the bank's position** — by more than a third here. **[[08 - Liquidity and Reserves Management|Ch. 08]] has to net this out**, and it is a standard way for a bank to look more liquid on paper than it is.
>
> **This also explains why banks hold low-yielding Treasuries specifically.** They are not chosen for return; **they are the collateral the rules accept**, and [[10 - Capital Adequacy and Basel|ch. 10]] gives them a zero risk weight on top. **The portfolio's composition is largely determined by regulation, and reading it as a set of investment choices misreads it.**

## ✏️ Exercises

**1. (Yields.)** (a) Why do three measures give three answers on one T-bill, and which is quoted? (b) When do YTM and HPY differ? (c) Verify R&H's YTM example.

> [!example]- Solution
> **(a) Because they differ in what they divide by and how long they think a year is.**
>
> *(Computed on a 91-day bill, par \$10,000, price \$9,800:)*
>
> | | divides by | year | result |
> |---|---|---|---|
> | bank discount rate | **par** | **360** | **7.9121%** |
> | bond-equivalent | price | 365 | 8.1857% |
> | effective annual | price, compounded | 365 | **8.4407%** |
> >
> **The bank discount rate is quoted, and it is the smallest** — 0.53 points below the effective yield. **Both of its conventions bias it downward**: par exceeds the price actually paid, and a 360-day year annualises over a shorter period than the real one.
>
> **It is a price-quoting convention, not a return.** Bills are sold at a discount with no coupon, so the "rate" is a way of stating the price. **Comparing it to a coupon bond's YTM understates the bill by roughly half a point** — consistently, in one direction, which is what makes it dangerous rather than merely imprecise.
>
> **(b) Whenever the security is not held to maturity.**
>
> **YTM assumes every promised cash flow is received on schedule.** HPY replaces the remaining flows with an actual sale price. *(Computed on R&H's note: **HPY = 11.5154%** against **YTM = 10.6842%**, because it was bought at \$900 and sold at \$950 after two years — the price recovery arrived in two years instead of five. The break-even sale price is **\$934.04**.)*
>
> **This matters more for a bank than for most investors**, because **securities are precisely the assets a bank sells when it needs cash** — loan demand rises, deposits run off, a pledge is called. **The sale date is set by [[08 - Liquidity and Reserves Management|liquidity]], not by the investments officer**, and it will tend to arrive when rates have risen and prices have fallen. **So the realised HPY is systematically worse than the YTM the security was bought on**, and a portfolio evaluated on YTM is being evaluated on a number it will not earn.
>
> **(c) The book's figure is wrong; the correct YTM is 10.68%.**
>
> *(Computed: **10.6842%**, which prices the note at exactly \$900.000000. **The book's 10.74% prices it at \$898.07** — it does not satisfy the equation the book itself prints.)*
>
> **Before concluding this, four other conventions were tested** *(computed: semiannual bond-equivalent 10.6299%, semiannual effective annual 10.9123%, and two shortcut approximations at 10.5263% and 11.1111%)*. **None gives 10.74%.**
>
> **And extraction was ruled out** — [[03 - Bank Financial Statements|ch. 03]]'s rule. The printed equation *is* corrupted in extraction (its first coupon appears as `$30`), **but the prose states the inputs independently and unambiguously**: 8% coupon on \$1,000 par = \$80, five years, price \$900. **The equation is not needed to know what was intended.**
>
> **Recorded in the errata table in `00-Index.md` — the first entry for this subject.**

**2. (Hard — maturity strategy.)** (a) Compare the three portfolios. (b) Why does the barbell win? (c) Why does anyone hold a bullet? (d) Why do small banks ladder? (e) What is the rate-expectations strategy really?

> [!example]- Solution
> **(a) Identical duration, different convexity.**
>
> *(Computed — all three yielding 6%, all with Macaulay duration exactly 5.0000 years: **bullet 26.6999, ladder 32.6332, barbell 40.9398** — the barbell has **53.3%** more convexity than the bullet.)*
>
> **Holding duration constant is what makes the comparison mean anything.** Comparing a 2-year portfolio to an 8-year one only rediscovers that long bonds move more. **Fixing duration cancels the first-order effect exactly and isolates the second.**
>
> **(b) Because convexity is a one-sided benefit and the barbell has more of it.**
>
> *(Computed: the barbell beats the bullet at **every** non-zero shock — +0.0673% at +1%, **+0.5425% at +3%**, **+0.7620% at −3%**.)*
>
> **The mechanism is that price is a convex function of yield** ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] §5), so **a portfolio spread across short and long maturities gains more from the long leg than it loses from the short one.** Convexity grows roughly with the *square* of maturity, so splitting 50/50 between 1 and 9 years gives an average maturity of 5 but an average of $t(t+1)$ far above $5\times6$.
>
> **[[06 - Hedging with Derivatives|Ch. 06]] §2 is the same quantity with the sign flipped.** There the bank shorted a 9-year futures contract against a 1.94-year net exposure, **sold convexity it did not owe, and lost in both directions.** Here it buys convexity and gains in both. **One is a modelling accident and the other is a decision — the mathematics does not distinguish them, which is exactly why it has to be checked for.**
>
> **(c) Because the market charges for convexity.**
>
> *(Computed — how far rates must move for the convexity gain to repay a yield give-up: **0.05% → ±0.86%**; **0.10% → ±1.23%**; **0.20% → ±1.76%**.)*
>
> **If the barbell dominated at an equal yield, nobody would hold anything else** — and that cannot be an equilibrium. **So the barbell must yield less, and the give-up is the price of the optionality.**
>
> **How much less depends on the shape of the yield curve** — a steep curve makes the long leg attractive and the short leg cheap; a flat or inverted one changes the whole calculation. **That is term-structure theory, and this subject deliberately does not derive it** *(the boundary recorded in `00-Index.md` assigns it to [[Monetary and Financial Theories/contents/00-Index|Mishkin]])*.
>
> **The honest summary: the barbell is a bet that rates will move a lot; the bullet is a bet that they will not.** Both are bets, and calling one "the safe choice" is wrong — **they have identical duration, so neither is safer in the sense the duration gap measures.**
>
> **(d) Because the ladder solves a different problem — liquidity, not yield.**
>
> *(Computed: the ladder matures **11.11% of the portfolio every year, at par, with no sale.** The bullet delivers nothing for four years and then 100%.)*
>
> **Maturing at par means no realised capital loss, whatever rates have done.** That is worth a great deal to an institution that cannot afford to be forced into selling at a loss — and it is exactly the risk [[08 - Liquidity and Reserves Management|ch. 08]] is about.
>
> **It also requires no rate forecast and no trading desk**, which is why R&H finds it "particularly popular among smaller institutions". **A strategy whose main virtue is that it cannot be got badly wrong suits an institution that cannot afford to get it badly wrong** — and that is a real argument, not a second-best one.
>
> **(e) A directional bet on rates, and it should be capitalised as one.**
>
> R&H's own summary of the rate-expectations strategy concedes it **"maximizes the potential for earnings (and also for losses)."**
>
> **The other four strategies are structural — they set a shape and hold it. This one shortens or lengthens the portfolio according to a forecast**, which means its returns come from being right about rates rather than from any property of the portfolio.
>
> **That is a trading position held in the investment portfolio**, and the danger is presentational: it appears in the same line of the balance sheet as the ladder, is described in the same language, and is governed by the same policy — **while being an entirely different activity.** [[06 - Hedging with Derivatives|Ch. 06]]'s closing note applies: *a hedged position is not a riskless one, and this is how a portfolio desk becomes a trading desk without anybody deciding to.*

**3. (Tax and purpose.)** (a) How can the lowest gross yield win? (b) What is TEY and what does the break-even rate explain? (c) Why hold a portfolio that yields less than loans? (d) What does pledging do to a liquidity ratio?

> [!example]- Solution
> **(a) Because municipal interest is exempt from federal income tax.**
>
> *(Verified against R&H at a 35% rate: corporate **7.00% → 4.55%**, prime loans **6.00% → 3.90%**, municipal **5.50% → 5.50%**. The municipal wins by **0.95 points** on the lowest gross yield of the three.)*
>
> **A taxed institution should rank investments on after-tax return, and only a tax-exempt one can rank on gross.** This is why credit unions and mutual funds — tax-exempt — hold visibly different portfolios from banks: **the same security genuinely has a different value to them.**
>
> **(b) TEY converts a tax-exempt yield into its taxable equivalent, and the break-even rate explains the collapse of bank municipal holdings.**
>
> $$\text{TEY}=\frac{\text{tax-exempt yield}}{1-t}=\frac{5.50\%}{0.65}=\mathbf{8.4615\%}\quad\text{✓ (book: 8.46\%)}$$
>
> **A taxable bond must yield 8.46% to match a 5.50% municipal at a 35% rate.**
>
> *(Computed — the break-even: $0.07(1-t)=0.055\Rightarrow t^*=\mathbf{21.43\%}$. At 46% the municipal wins by 1.72 points; at 35% by 0.95; **at 21% the corporate wins.**)*
>
> **R&H reports banks once holding nearly a quarter of all state and local debt, and their share collapsing. The arithmetic is the explanation**, and it has three parts: **the top bracket fell from 46% to 35%** (moving toward the 21.43% break-even), **the interest deduction on borrowings used to buy municipals was largely repealed in 1986**, and **fewer issues qualified** as private-activity rules tightened.
>
> **Nothing about the bonds changed.** Same issuers, same credit, same coupons — **and the entire investor base left.** [[06 - Hedging with Derivatives|Ch. 06]] found the same shape in tranche ratings: **a ranking that depends on a parameter outside the assets is not a property of the assets**, and will reverse without warning when that parameter moves.
>
> **(c) Because return is not what it is for.**
>
> *(Computed: loans 7.25% vs Treasuries 3.50% — a **3.75 point** give-up. A 20% allocation on a \$163mn balance sheet costs **1,222 thousand a year**.)*
>
> **A bank that wanted return would lend the money.** The portfolio exists for:
>
> 1. **Liquidity** — assets saleable without the discount a loan would take ([[08 - Liquidity and Reserves Management|ch. 08]]).
> 2. **Pledging** — government deposits *must* be collateralised. **This is a legal requirement, not a choice.**
> 3. **Income stabilisation** — securities income does not move with the local credit cycle.
> 4. **Credit diversification** — [[02 - Organization, Structure and Market Entry|ch. 02]] showed a bank's loan book is concentrated in one region; Treasuries are not.
> 5. **Somewhere to put money** when loan demand is weak.
>
> **The give-up is the price of all five**, and it should be read as an expense rather than as underperformance.
>
> **(d) It overstates it, badly.**
>
> *(Computed: with 35% of a 32,600 portfolio pledged, **only 21,190 is genuinely available** — a third of the apparent liquidity is encumbered.)*
>
> **A pledged security cannot be sold to meet a liquidity need**, so any ratio built on *total* securities is measuring something the bank does not have. **[[08 - Liquidity and Reserves Management|Ch. 08]] must net encumbered securities out**, and this is a standard way for a bank to look more liquid on paper than in fact — **the 2023 failures turned partly on exactly this distinction.**
>
> **It also explains the portfolio's composition, not just its size.** Treasuries yield least and are held most, because **they are the collateral the rules accept** and [[10 - Capital Adequacy and Basel|ch. 10]] assigns them a zero risk weight. **Much of what looks like investment choice is regulation**, and reading the portfolio as a set of free decisions misreads it.

## 📝 Summary

- **⚠️ One T-bill, three yields** *(computed: bank discount **7.9121%**, bond-equivalent **8.1857%**, effective annual **8.4407%**)*. **The quoted one is the smallest**, because it divides by par and uses a 360-day year — both biasing downward. **It is a price convention, not a return.**
- **⚠️ R&H's YTM example is wrong: 10.74% stated, 10.68% correct.** *(The book's figure prices the note at **\$898.07**, not \$900; four alternative conventions tested and none reproduces it; extraction ruled out because the prose states the inputs independently.)* **First entry in this subject's errata table.**
- **HPY is verified at 11.5154%** (book truncates to 11.51%) — **and the book showed its working there.** Where it appealed to "a financial calculator", it was wrong.
- **YTM assumes hold-to-maturity; HPY is what actually happens.** *(Break-even sale price **\$934.04**.)* **A bank's securities are exactly what it sells under pressure**, so the sale date is set by liquidity — and tends to arrive when prices are low.
- **The lowest gross yield can win after tax** *(verified: municipal 5.50% beats corporate 7.00% by **0.95 points** at a 35% rate)*, and **TEY = 5.50%/(1−0.35) = 8.4615%** ✓.
- **The break-even tax rate is 21.43%** — which explains why banks' share of the municipal market collapsed when the top bracket fell 46% → 35%. **Nothing about the bonds changed.**
- **⚠️ The chapter's result: three portfolios with duration of exactly 5.0000 years have convexities of 26.70 (bullet), 32.63 (ladder) and 40.94 (barbell)** — **the barbell beats the bullet at *every* non-zero shock, in both directions** *(+0.5425% at +3%, +0.7620% at −3%)*.
- **This is [[06 - Hedging with Derivatives|ch. 06]] §2 with the sign flipped**: there the bank was *short* convexity by accident and lost both ways; here it can be *long* convexity on purpose. **Same mathematics — one a mistake, one a strategy.**
- **Convexity is not free** *(computed: a 0.10% yield give-up needs a ±1.23% move to repay)*. **An efficient market must charge for it**, and how much is a term-structure question this subject leaves to Mishkin.
- **The ladder is a liquidity strategy, not a yield strategy** — **11.11% matures every year at par with no sale and no realised loss.** It needs no forecast and no trading desk, which is why small banks use it.
- **The rate-expectations strategy is a directional bet on rates** held inside the investment portfolio, in the same balance-sheet line and under the same policy as the ladder.
- **⚠️ Call and prepayment risk are written options** — the counterparty chooses, and chooses when it hurts. **That is negative convexity, and the bank was never paid a visible premium for it.**
- **The portfolio yields 3.75 points less than loans on purpose** *(a 20% allocation costs **1,222** a year on a \$163mn bank)*. It is held for **liquidity, pledging, income stability, credit diversification, and a place to park funds.**
- **⚠️ Pledging is a hard constraint** — *(computed: 35% encumbered leaves only **21,190** of a 32,600 portfolio available)*. **A liquidity ratio built on total securities overstates the position by a third**, and [[08 - Liquidity and Reserves Management|ch. 08]] must net it out.

## ⚠️ Important Notes

1. **⚠️ Never compare a bank discount rate to a YTM.** The bias is about half a point, always in the same direction.
2. **Convert to effective annual yield before comparing any two instruments** with different conventions or day counts.
3. **⚠️ R&H's p. 332 YTM of 10.74% is wrong — use 10.68%.** Substituting the book's figure prices the note at \$898.07.
4. **YTM = HPY only if held to maturity.** For a bank, that is the exception.
5. **The forced-sale date is set by liquidity needs, not by the investments officer** — and correlates with rates being high and prices low.
6. **Rank on after-tax return if the institution is taxed.** The lowest gross yield frequently wins.
7. **$\text{TEY}=\text{tax-exempt yield}/(1-t)$** — and it moves whenever the tax rate does, with no change in any security.
8. **⚠️ A ranking that depends on a parameter outside the assets is not a property of the assets.** Tax rates here; default correlation in [[06 - Hedging with Derivatives|ch. 06]].
9. **Compare portfolios at *equal duration*.** Comparing different durations only rediscovers that long bonds move more.
10. **⚠️ At equal duration, more convexity is strictly better — which is why it costs yield.** If a portfolio appears to dominate at equal yield, look for the charge.
11. **⚠️ Call and prepayment risk are negative convexity.** A callable or mortgage-backed holding is a written option ([[06 - Hedging with Derivatives|ch. 06]] §7).
12. **The ladder's virtue is that maturities arrive at par** — no sale, no realised loss, no forecast needed.
13. **The rate-expectations strategy is a trading position.** Recognise it, limit it, and capitalise it as one.
14. **⚠️ Pledged securities are encumbered and cannot meet a liquidity need.** Net them out of every liquidity ratio.
15. **Much of the portfolio's composition is regulation, not choice** — Treasuries are the collateral the rules accept and carry a zero risk weight ([[10 - Capital Adequacy and Basel|ch. 10]]).
16. **The yield give-up on securities is an expense, not underperformance.** It buys the five things in §6.

> [!warning] Gaps in the source material
> **R&H ch. 10 extracts cleanly as prose** *(PDF pp. 339–376; book page $n$ = PDF page $n+18$)*. The instrument survey, the ten choice factors, the tax discussion and the five maturity strategies all came through readably. *(The four standing extraction hazards in `00-Index.md` apply.)*
>
> **⚠️ Displayed equations are unreliable in this chapter.** Equation (10-1) renders its first coupon as `$30` where the prose says `$80`. **The prose is trustworthy and the display maths is not** — which is why §2's erratum was checked against the prose rather than the equation.
>
> **Exhibits 10-2 and 10-3 — the maturity-strategy diagrams — are lost**, as expected of graphical exhibits. **Their axis labels survive as noise** (`aJ "0 ;j - cil ] ;;,`), from which the *percentages* were recoverable (20% in each of five buckets for the ladder; 30/70 front-end; the back-end and barbell splits) but nothing else. **The three portfolios in §5 are mine**, constructed to hold duration constant — which the book's diagrams do not do.
>
> **Verified from the book: five figures.** After-tax yields **4.55% / 3.90% / 5.50%** ✓, **TEY 8.46%** ✓, and **HPY 11.51%** ✓ (truncated from 11.5154%). **One figure fails: the YTM of 10.74%** — see the errata table.
>
> **All other figures are mine**: the 91-day T-bill in §1, the three portfolios in §5, and the loan/Treasury yields and pledging fraction in §6. **The formulas — YTM, HPY, the bank discount rate, after-tax yield and TEY — are the book's.**
>
> **Additions beyond the source.**
>
> - **⚠️ §1 is mine and is the chapter's most practically useful addition.** R&H mentions the bank discount method and the 360-day convention in passing and **never computes the three measures side by side.** Doing so shows the quoted rate is the *smallest*, by 0.53 points, with both conventions biasing the same way.
> - **§2's erratum** is the result of applying the vault's verify-every-number rule; **the four-convention test and the extraction check follow [[03 - Bank Financial Statements|ch. 03]]'s discipline of ruling out my own error first.** The break-even sale price of \$934.04, and the observation that the forced-sale date correlates adversely with rates, are additions.
> - **§3's break-even tax rate of 21.43%** is mine. R&H reports the collapse in bank municipal holdings and lists three causes; **computing the break-even shows how close the 35% bracket already is to it**, and makes the history arithmetic rather than narrative.
> - **§4's observation that call, prepayment and call risk are all *written options* — negative convexity** — is mine, and links them to ch. 06 §7.
> - **⚠️ §5 is the chapter's main addition.** R&H presents the five strategies descriptively, with diagrams and advantage/disadvantage lists, and **never holds duration constant** — so its comparison cannot separate "longer" from "differently shaped". **Fixing duration at 5.0000 years isolates convexity, and the finding that the barbell dominates at every shock, together with the yield give-up needed to restore equilibrium, is not in the source.** The link back to ch. 06 §2 (same quantity, opposite sign) is mine.
> - **§5's ladder cash-flow table**, showing the strategy's real virtue is par maturities rather than yield, is mine; R&H's advantage list says "strengthens liquidity" without quantifying it.
> - **§6's yield give-up and the encumbrance calculation** are mine. **R&H lists pledging as one of ten factors and does not connect it to the liquidity ratio**, which is where it actually bites.
>
> **Deliberately compressed.** **The instrument survey (R&H §§10-2 to 10-6)** — T-bills, notes, bonds, agencies, CDs, commercial paper, bankers' acceptances, municipals, corporates, structured notes, stripped securities — **is compressed to the principles that distinguish them**; it is reference material, largely US-specific, and Table 10-2's advantage/disadvantage grid is partly lost to extraction anyway. **Securitised assets and CMOs** are covered in [[06 - Hedging with Derivatives|ch. 06]], which owns them. **The bank-qualified bond calculation (eq. 10-5)** is noted but not worked — it depends on US tax provisions that have since changed. **Yield-curve shape and term-structure theory** are used and flagged but not derived, per the boundary in `00-Index.md`. **The 9/11 settlement-fails case study** is omitted as historical colour, though its point — that a liquid market can stop settling — belongs with [[08 - Liquidity and Reserves Management|ch. 08]].

**Previous:** [[06 - Hedging with Derivatives]] · **Next:** [[08 - Liquidity and Reserves Management]]
