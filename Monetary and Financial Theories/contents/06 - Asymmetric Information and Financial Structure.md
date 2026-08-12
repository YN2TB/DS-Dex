---
subject: Monetary and Financial Theories
chapter: 6
tags: [ds, economics, asymmetric-information, adverse-selection, moral-hazard, principal-agent, credit-rationing, financial-structure]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 8 (with parts of ch. 10)"
---

# Asymmetric Information and Financial Structure

**This is the subject's analytical spine.** **[[01 - The Financial System and What Money Is|Ch. 01]] §3 named asymmetric information as the reason intermediaries dominate and deferred the theory to here.** **The chapter's method is unusual and worth copying: it states *eight facts* about financial systems worldwide, then derives all eight from two ideas.**

**Five results.**

**§2 — is fact 1 a fact, or a measurement choice?** *(Mishkin's own footnote 1 warns that Figure 1 measures **gross flows**, which overweight every instrument by $T/m$. Computed: correcting for maturity can make **stock the largest category rather than the smallest**.)* **⚠️ The vault's running result in a fifth setting — but note what survives: fact 3.**

**§3 — the lemons market collapses at a cliff, not a slope.** *(Computed: **unless 83.33% of cars are peaches, every peach leaves and the market is 100% lemons**. At $q=0.84$ it works perfectly; at $q=0.83$ it does not work at all.)*

**§6 — why debt beats equity, quantified.** *(Computed: at a 2% default rate, **debt is fifty times cheaper to monitor than equity** for identical cash flows.)*

**§7 — the critical net worth.** *(Computed: Steve gambles below **\$49,495** and does not above it — **reproducing both of Mishkin's own cases**, which he presents without a threshold.)*

**§8 — ⚠️ CASHING IN [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|Commercial Banking ch. 11]].** *(Computed: the lender's return rises to **8.10% at $r=15\%$** then **falls off a cliff to −19.50% one basis point later** — a **27.60-point** drop from raising the rate by 0.01.)* **CB measured a humped curve peaking at $r^*=18\%$ and could not explain it. This is the explanation.**

## 📘 Main Knowledge

### 1. The eight facts

**The chapter's structure: state eight facts true of every financial system in the world, then explain all eight from two ideas.**

| # | fact |
|---|---|
| **1** | **stocks are NOT the most important source of external finance** |
| **2** | marketable securities are not the primary source either |
| **3** | **indirect finance is many times more important than direct** |
| **4** | **banks are the most important source of external funds** |
| **5** | the financial system is among the **most heavily regulated** sectors |
| **6** | only large, well-established firms have easy access to securities markets |
| **7** | **collateral** is prevalent in debt contracts |
| **8** | debt contracts are long documents full of **restrictive covenants** |

*(Figure 1's US column, recovered — all four figures confirmed by the prose:)*

| source | share of external funds |
|---|---|
| bank loans | 18% |
| nonbank loans | 38% |
| **bonds** | **32%** ✓ |
| **stock** | **11%** ✓ |

**Cross-checks all pass: bank + nonbank = 56% ✓ (prose says 56%); stocks + bonds = 43% ✓.**

> [!warning] ⚠️ Only the US column is recovered
> **The other three countries' bars extracted as an unassignable sequence of labels**, and **[[03 - The Behavior of Interest Rates|ch. 03]] established the rule: never take a number from a figure label.** **Germany, Japan and Canada are represented only by the prose-level claims** — bank loans above 70%, 70% and 50% respectively.

> [!note] ⚠️ Fact 3 sharpened — Mishkin's own claim is conservative
> He states that since 1970 **"less than 5% of newly issued corporate bonds and commercial paper, and less than one-third of new issues of stocks, have been sold directly to households"**, so direct finance is **"less than 10%"** of external funding.
>
> *(Computed: $0.05\times32\%+0.333\times11\%=1.60\%+3.67\%=\mathbf{5.27\%}$ — and since both inputs are upper bounds, direct finance is **below 5.3%**.)*
>
> **His "less than 10%" is conservative by roughly a factor of two.** **⇒ about 95% of external business finance is intermediated.** **Fact 3 is not a tendency; it is nearly the whole system.**

### 2. ⚠️ Is fact 1 a fact, or a measurement choice?

> [!warning] Mishkin's footnote 1 raises this and then his text forgets it
> **Figure 1 measures *gross flows* over thirty years.** But:
> - **a \$1,000 share issued once raises \$1,000 permanently — counted once;**
> - **a \$1,000 one-year bond must be reissued every year to keep the \$1,000 — counted thirty times.**
>
> His own words: *"it looks as though debt is 30 times more important than stocks in raising funds, **even though our example indicates that the two methods are actually equally important for the firm**."*

**⇒ the flow measure overweights every instrument by $T/m$, where $m$ is its maturity.** *(Dividing it out — **with maturities I assumed, not Mishkin's data**:)*

| instrument | flow % | assumed maturity | counted $T/m$ times | **stock-equivalent share** |
|---|---|---|---|---|
| bank loans | 18% | 1 yr | 30.0 | **2.3%** |
| nonbank loans | 38% | 3 yr | 10.0 | 14.6% |
| bonds | 32% | 10 yr | 3.0 | **40.9%** |
| **stock** | **11%** | 30 yr | **1.0** | **42.2%** |

> [!warning] ⚠️ On this correction stock is the LARGEST category, not the smallest
> **The maturities are my assumptions, so this is not a claim that fact 1 is false.** **It is a demonstration that fact 1's evidence is measure-dependent** — exactly as Mishkin's footnote warns.
>
> **But notice what does *not* change: fact 3.** **Bank and nonbank loans still swamp direct household purchases, because that comparison does not depend on maturity at all.** **⇒ the robust fact is *intermediation*, not the debt–equity ranking** — which is fortunate, since intermediation is what the chapter goes on to explain.
>
> **⚠️ FIFTH INSTANCE OF THE VAULT'S RUNNING RESULT: the boundary of a measure is a judgement, and everything built on it inherits that judgement.** *(GDP and the CPI — [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]]; the unemployment rate — ch. 11; **"which M?"** — [[01 - The Financial System and What Money Is|ch. 01]]; **"which leg of the spread?"** — [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]; and now **"flows or stocks?"**.)*

### 3. Transaction costs — the first explanation, and the smaller one

**\$5,000 to invest: brokerage commissions are a large fraction of the purchase, some bonds have a \$10,000 minimum denomination, and you cannot diversify.** *(Mishkin: **about half of American households own any securities at all.**)*

| intermediary solution | mechanism |
|---|---|
| **economies of scale** | "the cost of arranging a purchase of 10,000 shares is not much greater than for 50 shares" — bundle many investors |
| **expertise** | technology, systems, and hence **liquidity services** (cheque-writing on a money-market fund) |

> [!note] Necessary but not sufficient
> **Transaction costs explain fact 3 *partly*.** **They do not explain facts 1, 2, 5, 6, 7 or 8** — nothing about scale economies says why *debt* rather than equity, why *collateral*, or why *covenants*. **The rest of the chapter is the real answer.**

### 4. ⚠️ The lemons problem — a cliff, not a slope

$$\textbf{adverse selection}=\text{before the transaction}\qquad\textbf{moral hazard}=\text{after it}$$

**Akerlof's used-car market. Buyers cannot tell peaches from lemons, so they pay the *average* value. Peach owners know their car is undervalued at that price and withdraw. The average then falls, and more withdraw.**

*(Modelled: a peach is worth \$10,000 to a buyer and a lemon \$4,000; a peach owner will not sell below \$9,000; a fraction $q$ are peaches, so buyers pay $4{,}000+6{,}000q$.)*

| $q$ | buyer's price | peach sold? | market |
|---|---|---|---|
| 1.00 | \$10,000 | **YES** | works |
| 0.90 | \$9,400 | YES | works |
| **0.8333** | **\$9,000** | **tie** | **$q^*$** |
| **0.83** | \$8,980 | **no** | **collapses to 100% lemons** |
| 0.50 | \$7,000 | no | collapses |

$$4{,}000+6{,}000q=9{,}000\quad\Longrightarrow\quad q^*=\mathbf{83.33\%}$$

> [!warning] ⚠️ The crucial feature is the discontinuity
> **At $q=0.84$ the market functions completely; at $q=0.83$ it does not function at all.** **There is no intermediate state in which it works "a bit worse".**
>
> **⇒ adverse selection is not merely a friction.** **A small deterioration in average quality does not shrink the market a little — it *unravels* it.**
>
> **This is facts 1 and 2**: good firms will not issue securities at a price set by the average, so the securities market gets the bad firms, so investors stay away, so few securities are sold.
>
> **⚠️ And note who is harmed: the peach *owners*, and the buyers who wanted a peach. The lemon owners do fine.** **The party injured by asymmetric information is the honest one** — which is why the tools in §5 are all ways for good borrowers to *prove* they are good.

### 5. ⚠️ The free-rider problem — why each private fix fails

| fix | verdict |
|---|---|
| **1. buy information** (S&P, Moody's, Value Line) | **fails** |
| **2. government regulation** (SEC, mandatory audits) | **partial** — explains fact 5 |
| **3. financial intermediation** | **⚠️ works** — explains facts 3, 4 |
| **4. collateral and net worth** | works — explains fact 7 |

**Fix 1 fails because of free-riding.** **You pay for information, buy the undervalued good securities — and free-riders see you buying and buy alongside.** **The price is bid up to true value immediately, so you never capture the gain and should never have paid for the information.**

> [!warning] ⚠️ This is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s efficient market hypothesis turned into a problem
> **There, arbitrage eliminating profit opportunities was the mechanism that made prices informative.** **Here, the *same* mechanism destroys the incentive to produce the information in the first place.**
>
> **⇒ markets cannot be perfectly efficient *and* give anyone a reason to gather information.** *(This is the Grossman–Stiglitz paradox in embryo — and it is a genuine tension between two chapters of the same book, which Mishkin does not flag.)*

**Fix 2 is partial.** **Firms still know more than statistics convey, and bad firms have an incentive to look like good ones.** *(**Enron**: a quarter of the energy-trading market, valued at **\$77bn** in August 2000, the **seventh-largest US corporation**; announced a **\$618m** third-quarter loss in October 2001; **bankrupt by December — the largest US bankruptcy to that date — despite \$1.5bn of new financing** from J.P. Morgan Chase and Citigroup.)*

> [!warning] ⚠️ Fix 3 works, and the reason is precise
> **A used-car dealer *buys* the car, produces the information privately, and resells with a guarantee — explicit (a warranty) or implicit (a reputation).** **A bank produces information and makes a *private, non-traded loan*.**
>
> **Because the loan is not traded, nobody can observe it and bid away the return.** **The bank captures the full value of the information it produced.**
>
> **⚠️ This is the sharpest sentence in the chapter: the bank's role as an intermediary holding *mostly non-traded loans* is the key to its success.** **It is not the deposit-taking, not the size, not the branch network — it is the non-tradability.**
>
> **And Mishkin draws a testable corollary that has come true: as information becomes cheaper to acquire, the role of banks should decline.** *(Facts 3 and 4 both note the decline. **This also explains why banks matter more in developing countries** — information about private firms is harder to collect there, so securities markets play a smaller role.)*

**Fix 4: collateral and net worth.** **Adverse selection interferes only if the lender *loses* on default. Collateral caps the loss; net worth does the same and additionally makes default less likely.** *(Hence the lament Mishkin quotes: **"only the people who don't need money can borrow it!"**)*

### 6. ⚠️ Moral hazard in equity — the principal–agent problem

**Steve's ice-cream store costs \$10,000. Steve has \$1,000 (10%); you put in \$9,000 (90%). Hard work earns \$50,000; shirking earns \$0.**

| | Steve | you |
|---|---|---|
| **hard work** | \$5,000 | **\$45,000** |
| **shirking** | a beautiful office and a good tan | **\$0** |

> [!warning] ⚠️ The wedge, computed
> **Steve's effort creates \$50,000 of value and he captures \$5,000 of it.**
>
> - **socially efficient** for him to work if his cost of effort < **\$50,000**
> - **privately worth it** only if his cost of effort < **\$5,000**
>
> **⇒ an entire \$45,000 band in which effort is worth having and does not happen** — and the band is exactly $(1-s)\times\$50{,}000$:
>
> | Steve's share $s$ | he works if cost < | **wasted band** |
> |---|---|---|
> | **10%** | \$5,000 | **\$45,000** |
> | 50% | \$25,000 | \$25,000 |
> | 90% | \$45,000 | \$5,000 |
> | **100%** | \$50,000 | **\$0** |
>
> **At 100% ownership the wedge vanishes** — Mishkin says so; the table shows it is exactly *linear* in the ownership share.
>
> **⚠️ AND HERE IS THE TRAP THE CHAPTER IS REALLY ABOUT.** **The fix — give the manager more equity — directly contradicts the reason outside equity existed. Steve only *had* \$1,000.** **Outside equity is needed because the entrepreneur lacks capital, and outside equity is exactly what creates the agency problem.** *(That tension is why executive stock options exist, and why they never fully solve it.)*

**The dishonest version is worse:** **a cash business lets Steve pocket the \$50,000 and report zero.** **Then you need *costly state verification*.**

| tool | limit |
|---|---|
| **monitoring** (auditing) | **costly state verification**, and subject to the **same free-rider problem** — if others monitor, you needn't, so nobody does ⇒ explains fact 1 |
| **government regulation** | accounting standards, criminal penalties — but fraud is hard to prove ⇒ fact 5 |
| **financial intermediation** | **venture capital**: takes board seats, and the equity is **private and non-marketable**, so no one free-rides ⇒ fact 3 |
| **debt contracts** | §7 ⇒ fact 1 |

### 7. ⚠️ Why debt beats equity — the monitoring arithmetic

**Equity is a claim on profits *in all states*, so the holder must verify profits *in all states*.** **Debt is a fixed payment:**

- **firm pays ⇒ the lender does not care what the profits were;**
- **firm fails ⇒ the lender must verify, and behaves like an equity holder.**

$$\textbf{debt requires state verification only in default}$$

*(Computed — if verification costs $c$ and default probability is $p$:)*

| $p$ | equity | debt | debt cheaper by |
|---|---|---|---|
| 1% | $c$ every period | $0.01c$ | **100×** |
| **2%** | $c$ | $0.02c$ | **50×** |
| 5% | $c$ | $0.05c$ | 20× |
| 25% | $c$ | $0.25c$ | 4× |

> [!warning] ⚠️ At a 2% default rate, debt is fifty times cheaper to monitor than equity — for identical cash flows
> **That is the central reason debt dominates equity in every financial system in the world.** **Not tax, not tradition, but the cost of finding out what happened.**
>
> *(Mishkin's footnote 4 adds the tax code — interest is deductible in the US, dividends are not. **A real effect, but secondary to this one**, since the debt–equity ranking holds in countries with different tax treatments.)*
>
> **And it explains why equity is the *residual* claim of [[01 - The Financial System and What Money Is|ch. 01]]: the claim that requires verification is the one that gets paid last.**

### 8. ⚠️ Moral hazard in debt — and the critical net worth

**Debt does not escape moral hazard; it relocates it.** **A borrower who pays a fixed amount and keeps everything above it wants *more* risk than the lender does — the upside is all his, the downside is largely yours.**

*(Mishkin's case: Steve borrows \$9,000 for an ice-cream store and instead buys chemistry equipment, chasing a 1-in-10 shot at fat-free ice cream. **He says high net worth fixes this and does not say how much is needed.**)*

*(Computed — the project costs \$100,000; Steve puts in $E$ and borrows $100{,}000-E$ at 10%. **Safe** returns \$110,000 certainly; **risky** returns \$600,000 with probability 0.10, else \$0 — expected value \$60,000, so **the risky project destroys value**.)*

| Steve's equity $E$ | payoff SAFE | payoff RISKY | he chooses |
|---|---|---|---|
| **\$1,000** | \$1,100 | **\$49,110** | **RISKY — gambles** |
| \$40,000 | \$44,000 | \$53,400 | RISKY — gambles |
| **≈\$49,495** | \$54,444 | \$54,444 | **threshold** |
| \$60,000 | \$66,000 | \$55,600 | SAFE |
| **\$91,000** | **\$100,100** | \$59,010 | **SAFE** |

$$1.1E=49{,}000+0.11E\quad\Longrightarrow\quad E^*\approx\mathbf{\$49{,}495}$$

> [!warning] ⚠️ The threshold is roughly half the project
> **Below it Steve gambles with your money; above it he does not.** **And this reproduces Mishkin's own two cases exactly** — with \$1,000 in he gambles; with \$91,000 in he does not. **The story is his; the threshold is the thing the story was for.**
>
> **⚠️ And note the lender's position: under the risky project the loan is repaid only 10% of the time.** **The lender does not lose a little — the loan becomes a different instrument entirely, without one word of the contract changing.**

**Restrictive covenants (fact 8), of four kinds:** **discourage undesirable behaviour** (specify what the loan may fund); **encourage desirable behaviour** (life insurance; maintain minimum net worth); **keep collateral valuable** (insurance on the car, no sale before repayment); **provide information** (quarterly accounts, right to audit).

> [!note] Why covenants are not enough — and why banks again
> **It is almost impossible to write covenants ruling out every risky act, and borrowers find loopholes.** **Worse, covenants must be *monitored and enforced*, which is subject to the same free-rider problem** — if you know other bondholders are monitoring, you free-ride, and so does everyone. **⇒ moral hazard remains severe for marketable debt.**
>
> **Banks holding non-traded private loans escape it, for the third time in the chapter.**

### 9. ⚠️ Stiglitz–Weiss — cashing in Commercial Banking ch. 11

> [!warning] The debt this chapter was written to pay
> **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]] computed a lender's expected return as a *humped* function of the loan rate, peaking at $r^*=18\%$, so that past the peak the lender earns less by charging more.** **It took the idea from a Rose & Hudgins footnote and could not explain it.** **This chapter is the explanation, and it is built from Mishkin's own two concepts.**

*(Modelled: a pool of borrowers each wanting \$1 — **80% safe**, whose project returns 1.15 for certain, and **20% risky**, whose project returns 1.40 with probability 0.70 and else 0, expected value 0.98.)*

$$\text{safe applies while }1.15-(1+r)\ge0\ \Rightarrow\ r\le15\%$$
$$\text{risky applies while }0.70[1.40-(1+r)]\ge0\ \Rightarrow\ r\le40\%$$

> [!note] The adverse selection is *derived*, not assumed
> **Safe borrowers leave first because a safe project has less upside to pay a high rate out of.** **Nothing was assumed about who is more rate-sensitive; it follows from the projects.**

| loan rate $r$ | pool | **lender's expected return** |
|---|---|---|
| 6.00% | safe + risky | −0.36% |
| 10.00% | safe + risky | +3.40% |
| **15.00%** | safe + risky | **+8.10%** |
| **15.01%** | **RISKY ONLY** | **−19.49%** |
| 20.00% | risky only | −16.00% |
| 40.00% | risky only | −2.00% |
| 40.01% | nobody borrows | — |

> [!warning] ⚠️ A 27.60-point drop from raising the rate by one basis point
> **The return rises to 8.10% at $r=15\%$, then falls off a cliff to −19.50%.** **And it never recovers**: $0.70(1+r)-1>0$ needs $r>42.9\%$, but nobody borrows above 40%.
>
> **⇒ the lender's optimal rate is 15%, even though borrowers would willingly pay 40%.**
>
> **⚠️ FACED WITH EXCESS DEMAND, THE LENDER DOES NOT RAISE THE PRICE — IT RATIONS THE QUANTITY.** **That is *credit rationing*: a market that does not clear on price, by choice, with no friction you can point at.**

> [!warning] ⚠️ Three connections, all of which this discharges
> **1. [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]]'s $r^*=18\%$ is a smoothed version of this curve.** **With a continuum of borrower types the cliff becomes a hump, but the peak and the reason for it are identical.** **CB *measured* the curve; this chapter says what it *is*.**
>
> **2. The two channels are separable, and CB could not separate them.** **Adverse selection: a higher rate changes *who applies*** (modelled above). **Moral hazard: a higher rate changes *what the same borrower does*** — §8's Steve, switching to chemistry because the fixed payment already eats the safe return. **Both push the same way, and neither is visible in the loan contract.**
>
> **3. ⚠️ This is why [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s loanable-funds diagram is an idealisation.** **There the interest rate clears the market. Here it does not clear the market at all** — and the difference is entirely informational.

### 10. Table 1 — one page, and what the row counts say

*(Mishkin's summary table, which extracted complete:)*

| problem | tool | explains |
|---|---|---|
| **adverse selection** | private production and sale of information | 1, 2 |
| | government regulation to increase information | 5 |
| | **financial intermediation** | **3, 4, 6** |
| | collateral and net worth | 7 |
| **moral hazard in EQUITY** | production of information: monitoring | 1 |
| *(principal–agent)* | government regulation to increase information | 5 |
| | **financial intermediation** | **3** |
| | debt contracts | 1 |
| **moral hazard in DEBT** | collateral and net worth | 6, 7 |
| | monitoring/enforcement of restrictive covenants | 8 |
| | **financial intermediation** | **3, 4** |

> [!warning] ⚠️ Count the rows
> **"Financial intermediation" appears three times, under all three problems.** **"Collateral and net worth" appears twice.**
>
> **⇒ one institution solves every variant of the problem** — **which is why [[01 - The Financial System and What Money Is|ch. 01]]'s answer (intermediaries dominate *because of asymmetric information*) is the right one and not merely one of three.**
>
> **And fact 5 is explained twice, once under each problem.** **Regulation here is not a political fact about finance; it is what an information problem looks like when the private fixes free-ride.**

> [!note] Financial development and growth
> **Where these institutions are missing — poor accounting, weak property rights, unenforceable collateral, no credit information — lending does not happen and growth is low.** **Mishkin calls it *financial repression*.**
>
> **⚠️ Which turns the whole chapter into a growth theory:** **[[Macroeconomics & Microeconomics/contents/09 - Production and Growth|Macro/Micro ch. 09]] found investment drives growth; this chapter says the financial system is what decides whether *saving becomes investment*.**

## ✏️ Exercises

**1. (The eight facts.)** (a) State them and recover Figure 1's US column. (b) Sharpen fact 3. (c) Is fact 1 secure?

> [!example]- Solution
> **(a) Eight facts; the US column is 18 / 38 / 32 / 11.**
>
> **1** stocks are not the most important source of external finance; **2** marketable securities are not the primary source; **3** indirect finance far exceeds direct; **4** banks are the most important source; **5** the system is heavily regulated; **6** only large firms have easy securities access; **7** collateral is prevalent; **8** debt contracts are full of covenants.
>
> | source | share |
> |---|---|
> | bank loans | 18% |
> | nonbank loans | 38% |
> | bonds | 32% |
> | stock | 11% |
>
> *(All four confirmed by the prose: **bank + nonbank = 56%** ✓, **bonds 32%** ✓, **stock 11%** ✓, **stocks + bonds = 43%** ✓.)*
>
> **⚠️ Only the US column is recoverable.** The other countries' bars extracted as an unassignable label sequence, and **[[03 - The Behavior of Interest Rates|ch. 03]]'s rule applies: never take a number from a figure label.**
>
> **(b) Direct finance is under 5.3%, not under 10%.**
>
> **Mishkin gives two bounds — under 5% of new bonds and under one-third of new stock issues go directly to households — and concludes "less than 10%".**
>
> $$0.05\times32\%+0.333\times11\%=1.60\%+3.67\%=\mathbf{5.27\%}$$
>
> **And both inputs are upper bounds, so the truth is below 5.3%.** **His figure is conservative by roughly a factor of two ⇒ about 95% of external business finance is intermediated.**
>
> **⚠️ This matters for how you read the chapter.** **Fact 3 is not "indirect finance is somewhat more common" — it is very nearly the entire system**, which is why the remaining sections spend their effort explaining intermediaries rather than markets.
>
> **(c) No — and Mishkin's own footnote says why.**
>
> **Figure 1 measures *gross flows* over thirty years, so an instrument is counted $T/m$ times.** **A share issued once is counted once; a one-year bond reissued annually is counted thirty times.** **Mishkin: the two "are actually equally important for the firm".**
>
> *(Correcting with **assumed** maturities: stock's stock-equivalent share becomes **42.2%** and bank loans **2.3%** — **stock becomes the largest category rather than the smallest.**)*
>
> **⚠️ This is not a claim that fact 1 is false** — the maturities are mine. **It shows fact 1's evidence is measure-dependent.**
>
> **But notice what survives: fact 3.** **The comparison of intermediated against direct household purchases does not depend on maturity at all**, so it is untouched. **⇒ the robust fact is intermediation, not the debt–equity ranking** — fortunately, since intermediation is what the chapter explains.
>
> *(Fifth instance of the vault's running result: **the boundary of a measure is a judgement**. GDP and the CPI; the unemployment rate; which M?; which leg of the spread?; and now flows or stocks?)*

**2. (Hard — lemons.)** (a) Work the model and find the collapse threshold. (b) Why is the discontinuity the important feature? (c) Who is harmed?

> [!example]- Solution
> **(a) $q^*=83.33\%$.**
>
> *(A peach is worth \$10,000 to a buyer and a lemon \$4,000; a peach owner will not sell below \$9,000; a fraction $q$ are peaches.)* **Buyers pay the average, $4{,}000+6{,}000q$.**
>
> $$4{,}000+6{,}000q\ge9{,}000\quad\Longleftrightarrow\quad q\ge\mathbf{0.8333}$$
>
> | $q$ | price | peach sold? |
> |---|---|---|
> | 0.90 | \$9,400 | **YES** |
> | **0.8333** | **\$9,000** | **tie** |
> | 0.83 | \$8,980 | **no** |
>
> **Below 83.33%, every peach owner withdraws — and then the market is 100% lemons.** *(And the unravelling is self-reinforcing: each withdrawal lowers the average, which lowers the price, which drives out the next-best cars.)*
>
> **(b) Because the market does not degrade — it fails.**
>
> **At $q=0.84$ the market functions completely; at $q=0.83$ it does not function at all.** **There is no intermediate state in which it works "a bit worse".**
>
> **⚠️ So adverse selection is not a friction to be traded off against other costs.** **A small deterioration in average quality does not shrink the market proportionally — it unravels it**, which is why the tools in §5 are about *eliminating* the information asymmetry rather than pricing it.
>
> **Applied to securities, this is facts 1 and 2 directly.** **Irving cannot tell good firms from bad, so he pays a price reflecting the average.** **Good firms know their securities are undervalued and do not issue.** **Only bad firms issue, and Irving — not being stupid — buys nothing.** **The market for corporate securities is thin because of an information problem, not a demand problem.**
>
> **(c) The honest party.**
>
> **The peach owners lose (they cannot sell at a fair price) and the buyers who wanted a peach lose (none is available).** **The lemon owners do fine — they sell at above their car's value.**
>
> **⚠️ This is the structural reason the chapter's tools all take one form: ways for a *good* borrower to prove it is good.** **Collateral, net worth, audited accounts, covenants, and submitting to a bank's scrutiny are all costly signals borne by the honest party** — because the dishonest party has no incentive to fix anything.
>
> *(It also explains **fact 6**: large, well-known corporations have more public information about them, so investors worry less about adverse selection and are willing to buy their securities directly. **A pecking order by reputation.**)*

**3. (Hard — free-riding.)** (a) Why does buying information fail? (b) What exactly makes intermediation work? (c) What tension does (a) create with the previous chapter?

> [!example]- Solution
> **(a) Because you cannot keep the benefit.**
>
> **You pay for information and buy the undervalued good securities.** **Free-riders observe you buying and buy alongside without paying.** **The increased demand bids the price up to true value immediately, so you never capture the gain — and therefore you should never have bought the information.**
>
> **If everyone reasons this way, too little information is produced and adverse selection persists.** **⚠️ The failure is not that information is expensive; it is that information is *non-excludable once acted upon*.**
>
> **Government regulation (fix 2) helps but is partial** — firms still know more than statistics convey, and **bad firms have an incentive to look like good ones.** *(**Enron**: **\$77bn** valuation in August 2000, **seventh-largest US corporation**, a quarter of the energy-trading market; a **\$618m** quarterly loss announced in October 2001; **bankrupt by December despite \$1.5bn of new financing** — the largest US bankruptcy to that date. Mishkin's point: **regulation can lessen asymmetric information but cannot eliminate it**, because managers have enormous incentives to hide problems.)*
>
> **(b) Non-tradability.**
>
> **A used-car dealer *buys* the car, produces the information privately, and resells with a guarantee** — explicit (a warranty) or implicit (its reputation). **Because it owns the car when it produces the information, no one can free-ride.**
>
> **A bank does the same: it produces information about borrowers and makes a *private, non-traded loan*.** **Because the loan is not traded, nobody can observe it and bid away the return, so the bank captures the full value of what it learned.**
>
> **⚠️ This is the chapter's sharpest sentence, and it is worth stating precisely: it is not deposit-taking, size, or branch networks that make banks special — it is that their assets are not traded.** *(It also explains facts 3, 4 **and** the testable corollary Mishkin draws: **as information becomes cheaper to acquire, banks should decline in importance**. They have. And the same logic explains why banks matter *more* in developing countries — information is harder to collect there, so securities markets are smaller.)*
>
> **(c) It contradicts the mechanism [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]] relied on.**
>
> **In ch. 05, arbitrage eliminating unexploited profit opportunities is what makes prices reflect all available information — and it is a *virtue*.** **Here, the identical mechanism destroys the incentive to produce the information in the first place — and it is the *problem*.**
>
> **⚠️ Both cannot be fully true. If prices instantly reflect information, nobody is paid for gathering it; if nobody gathers it, prices cannot reflect it.**
>
> **This is the Grossman–Stiglitz paradox in embryo**, and **Mishkin does not flag the tension between his own two chapters.** *(The resolution economists give is that markets must be **slightly** inefficient — just enough to compensate information production. Which is also why ch. 05's "smart money" rider matters: the return to being smart must be positive, or there is no smart money.)*

**4. (Hard — agency and the debt–equity choice.)** (a) Compute the principal–agent wedge. (b) What trap does the obvious fix run into? (c) Why does debt dominate equity?

> [!example]- Solution
> **(a) Steve captures 10% of the value his effort creates, leaving a \$45,000 band.**
>
> **Hard work earns the store \$50,000, of which Steve gets \$5,000 and you get \$45,000. Shirking earns \$0.**
>
> - **Socially efficient** for Steve to work if his cost of effort < **\$50,000**;
> - **privately worth it** only if his cost of effort < **\$5,000**.
>
> | $s$ | works if cost < | **wasted band** |
> |---|---|---|
> | **10%** | \$5,000 | **\$45,000** |
> | 50% | \$25,000 | \$25,000 |
> | 90% | \$45,000 | \$5,000 |
> | 100% | \$50,000 | **\$0** |
>
> **The band is exactly $(1-s)\times\$50{,}000$ — linear in the ownership share, vanishing at $s=1$.** **Mishkin observes that sole ownership removes the problem; the table shows the relationship is exactly proportional.**
>
> *(And the dishonest version is worse: a cash business lets Steve pocket \$50,000 and report zero, which requires **costly state verification** rather than mere incentive alignment.)*
>
> **(b) The fix contradicts the reason outside equity existed.**
>
> **⚠️ Give the manager more equity and the wedge shrinks — but Steve only *had* \$1,000.** **Outside equity is needed precisely because the entrepreneur lacks capital, and outside equity is exactly what creates the agency problem.**
>
> **So the two objectives are in direct conflict, and no ownership share satisfies both.** *(This is why executive stock options exist — a way to hand managers upside without requiring them to buy it — and why they never fully solve the problem: they change the payoff without changing the capital contribution, so they can encourage effort *and* encourage risk-taking at the same time.)*
>
> **Monitoring is the other tool, and it fails the same way as §5's fix 1**: **if other shareholders monitor, you can free-ride; so can they; so nobody does.** **⇒ moral hazard for common stock is severe, which is an additional explanation of fact 1.** *(Venture capital escapes it exactly as banks do — board seats plus **private, non-marketable** equity.)*
>
> **(c) Because debt requires verification only in default.**
>
> **Equity is a claim on profits in all states, so the holder must verify in all states.** **A debt holder who is paid does not care what the profits were; only in default must they verify.**
>
> *(Computed — verification cost $c$, default probability $p$:)*
>
> | $p$ | equity | debt | cheaper by |
> |---|---|---|---|
> | 1% | $c$ | $0.01c$ | **100×** |
> | **2%** | $c$ | $0.02c$ | **50×** |
> | 25% | $c$ | $0.25c$ | 4× |
>
> **⚠️ At a 2% default rate debt is fifty times cheaper to monitor than equity, for identical cash flows.** **That is the central reason debt dominates equity in every financial system in the world — not tax, not tradition, but the cost of finding out what happened.**
>
> *(Mishkin's footnote 4 adds US interest deductibility. **Real but secondary** — the ranking holds across countries with different tax treatments, which a tax explanation cannot account for.)*
>
> **And it closes a loop with [[01 - The Financial System and What Money Is|ch. 01]]: equity is the *residual* claim, and the claim that requires verification is precisely the one paid last.**

**5. (Hard — credit rationing.)** (a) Build the Stiglitz–Weiss curve. (b) What does the lender do about excess demand? (c) What three earlier results does this discharge?

> [!example]- Solution
> **(a) The return peaks at 15% and falls off a cliff.**
>
> *(80% safe borrowers whose project returns 1.15 for certain; 20% risky whose project returns 1.40 with probability 0.70, else 0.)*
>
> **Safe borrowers apply while $1.15-(1+r)\ge0$, i.e. $r\le15\%$. Risky apply while $0.70[1.40-(1+r)]\ge0$, i.e. $r\le40\%$.**
>
> **⚠️ The adverse selection is *derived*, not assumed** — safe borrowers leave first because a safe project has less upside to pay a high rate out of. **Nothing was assumed about who is more rate-sensitive.**
>
> | $r$ | pool | return |
> |---|---|---|
> | 10.00% | safe + risky | +3.40% |
> | **15.00%** | safe + risky | **+8.10%** |
> | **15.01%** | **risky only** | **−19.49%** |
> | 40.00% | risky only | −2.00% |
>
> **A one-basis-point rise costs 27.60 percentage points of return.** **And it never recovers**: $0.70(1+r)-1>0$ requires $r>42.9\%$, but nobody borrows above 40%.
>
> **(b) It rations quantity instead of raising price.**
>
> **The lender's optimal rate is 15%, though borrowers would willingly pay 40%.** **⚠️ Faced with excess demand, a profit-maximising lender does *not* raise the price — it lends less.**
>
> **That is credit rationing: a market that does not clear on price, by choice, with no friction, no regulation and no irrationality anywhere in it.** **The rate is *chosen* below the market-clearing level because raising it destroys the pool.**
>
> *(Note how counter-intuitive this is against ordinary price theory, and how firmly it follows: the "quality" of what you are buying **depends on the price you offer**, which is not true of apples.)*
>
> **(c) CB ch. 11, the two channels, and Macro/Micro ch. 10.**
>
> **1. ⚠️ [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]]'s $r^*=18\%$ is a smoothed version of this curve.** **With a continuum of borrower types the cliff becomes a hump, but the peak and the reason are identical.** **CB *measured* the curve from a Rose & Hudgins footnote and could not explain it; this chapter says what it is.**
>
> **2. The two channels are separable, and CB could not separate them.**
> - **adverse selection** — a higher rate changes ***who applies*** (modelled above);
> - **moral hazard** — a higher rate changes ***what the same borrower does*** (§8's Steve, switching to chemistry because the fixed payment already consumes the safe return).
>
> **Both push the same way, and neither is visible anywhere in the loan contract.** ⚠️ **That invisibility is the point: a lender examining the document learns nothing about either.**
>
> **3. ⚠️ [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s loanable-funds diagram is an idealisation.** **There the interest rate clears the market by construction. Here it does not clear the market at all**, and the difference is purely informational — no tax, no price control, no rigidity.
>
> *(Which is also why this chapter is a growth theory. **Where the institutions of §5 are missing — poor accounting, weak property rights, unenforceable collateral — rationing is severe and lending does not happen.** Mishkin calls it **financial repression**, and it is the mechanism by which [[Macroeconomics & Microeconomics/contents/09 - Production and Growth|Macro/Micro ch. 09]]'s saving fails to become investment.)*

## 📝 Summary

- **The chapter states eight facts about financial systems worldwide and derives all eight from two ideas** — **adverse selection (*before* the transaction) and moral hazard (*after* it)**.
- **Figure 1's US column recovered and prose-confirmed** — bank loans 18%, nonbank 38%, **bonds 32%**, **stock 11%**; bank + nonbank = 56% ✓, stocks + bonds = 43% ✓.
- **⚠️ Fact 3 sharpened** *(computed: direct finance is **below 5.3%**, not Mishkin's "less than 10%")* — **~95% of external business finance is intermediated.**
- **⚠️ Fact 1 is measure-dependent.** Figure 1 counts *gross flows*, overweighting each instrument by $T/m$ *(computed with assumed maturities: **stock becomes the largest category at 42.2%**)*. **But fact 3 survives untouched — the robust fact is intermediation, not the debt–equity ranking.**
- **Transaction costs explain fact 3 only partly** — nothing about scale economies explains debt-over-equity, collateral, or covenants.
- **⚠️ The lemons market collapses at a cliff** *(computed: $q^*=\mathbf{83.33\%}$; at 0.84 it works completely, at 0.83 not at all)*. **Adverse selection does not shrink a market — it unravels it.**
- **⚠️ The party harmed is the honest one** — peach owners and would-be peach buyers. **Which is why every tool is a way for a good borrower to prove it is good.**
- **Private information production fails to free-riding**; regulation is partial *(Enron: **\$77bn**, seventh-largest US corporation, bankrupt within 16 months)*; **intermediation works.**
- **⚠️ And the reason intermediation works is precise: the loan is NOT TRADED**, so nobody can bid away the return to the information produced. **Not size, not deposits — non-tradability.**
- **⚠️ Free-riding contradicts [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]** — the arbitrage that makes prices informative destroys the incentive to produce information. **Grossman–Stiglitz; Mishkin does not flag it.**
- **⚠️ The principal–agent wedge is exactly $(1-s)\times$ the value created** *(Steve at 10% ownership leaves a **\$45,000** band)* — **and the fix contradicts the reason outside equity existed.**
- **⚠️ Debt beats equity because it needs verification only in default** *(computed: at a 2% default rate, **50× cheaper to monitor**)*. **Not tax, not tradition — the cost of finding out what happened.**
- **⚠️ The critical net worth is ≈\$49,495** *(computed)* — **reproducing both of Mishkin's cases**, which he gives without a threshold. **Below it the loan silently becomes a different instrument.**
- **Covenants come in four kinds and are still not enough** — loopholes, and monitoring them free-rides. **Banks again.**
- **⚠️ Stiglitz–Weiss computed: the return peaks at 8.10% at $r=15\%$ and falls to −19.49% one basis point later — a 27.60-point cliff.** **⇒ the lender rations quantity rather than raising price.**
- **⚠️ [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]]'s $r^*=18\%$ is this curve smoothed** — **CB measured it, this chapter explains it**, and the two channels (*who applies* vs *what they do*) are separable here and were not there.
- **Table 1: "financial intermediation" appears under all three problems** ⇒ **[[01 - The Financial System and What Money Is|ch. 01]]'s answer was the right one, not one of three.**
- **Where these institutions are missing, lending does not happen — *financial repression*** ⇒ **the chapter is a theory of growth.**

## ⚠️ Important Notes

1. **Adverse selection is *before*, moral hazard is *after*.** Everything else follows from the timing.
2. **⚠️ Eight facts, two ideas.** If a proposed explanation accounts for only one fact, it is not the explanation.
3. **Transaction costs are the *lesser* half.** They explain scale, not structure.
4. **⚠️ Fact 1's evidence is a gross-flow measure**, which overweights short maturities by construction.
5. **⚠️ Fact 3 does not depend on the measure** — that is why it is the load-bearing one.
6. **The lemons collapse is discontinuous.** No "slightly worse market" exists.
7. **⚠️ Asymmetric information harms the honest party.** The bad type is never the one seeking a remedy.
8. **Free-riding defeats every fix that produces *public* information.**
9. **⚠️ Non-tradability is what makes a bank a bank.** Private loans cannot be free-ridden.
10. **⚠️ Regulation is not a political fact here** — it is the residue left when private fixes free-ride, which is why fact 5 is explained twice.
11. **The principal–agent wedge is linear in the ownership share** and vanishes only at 100%.
12. **⚠️ The fix for agency conflicts with the reason for outside equity.** No share solves both.
13. **⚠️ Debt's advantage is *verification frequency*, not tax.** Tax is a secondary US-specific effect.
14. **Debt relocates moral hazard, it does not remove it** — fixed payment plus unlimited upside invites risk.
15. **⚠️ There is a threshold net worth**, and below it the borrower's incentives flip entirely.
16. **A moral-hazard shift changes the instrument without changing the contract.** Nothing is observable.
17. **⚠️ Raising the loan rate can lower the lender's return** — through *who applies* and *what they do*.
18. **⚠️ Credit rationing is a choice, not a friction.** The market does not clear on price because clearing on price would destroy the pool.
19. **Loanable funds is an idealisation.** Real credit markets ration.
20. **⚠️ Financial repression is the growth channel** — the system decides whether saving becomes investment.

> [!warning] Gaps in the source material
> **This chapter extracts well** — it is almost entirely prose and narrative examples, and **its one summary table survived complete**.
>
> **⚠️ TABLE 1 (asymmetric-information problems, tools, and which fact each explains) came through with all eleven rows and the eight-fact key intact.** **Fifth confirmation of the vault's rule: graphical exhibits are lost; tables set as text survive whole.**
>
> **⚠️ FIGURE 1 IS PARTIALLY RECOVERED, AND THE BOUNDARY IS WORTH RECORDING.** The bar chart's numeric labels *do* extract as text — but as **an unassignable sequence of sixteen percentages**. **The US column was recovered only because the prose independently states 11%, 32%, 56% and 43%, and the extracted 18 + 38 + 32 + 11 reproduces all four.** **Germany, Japan and Canada are NOT recovered**: their bars cannot be assigned to categories with confidence, so **only the prose-level claims are used** (bank loans above 70%, 70% and 50%). **This applies [[03 - The Behavior of Interest Rates|ch. 03]]'s rule — *never take a number from a figure label* — and refines it: a figure label is usable only when independently confirmed by prose, in which case the prose was sufficient anyway.**
>
> **No erratum found.** Everything Mishkin states numerically reproduces or is consistent: the four US shares and their two subtotals, the Enron figures, and the arithmetic of both Steve examples.
>
> **⚠️ One garbled sentence, not filed.** The transaction-costs section reads *"About one-half of American households own any securities"*, which is missing a qualifier — almost certainly "only about" or "less than". **The sense is clear and no number is at stake**, so it is an extraction or typesetting artifact rather than an erratum. *(Rule 4: rule out your own extraction first.)*
>
> **⚠️ SCOPE NOTE — this note folds in part of Mishkin ch. 10 as [[00-Index]] records.** **The deposit-insurance moral-hazard material belongs here conceptually** and is cross-referenced from §5's discussion of government fixes; **prudential supervision is [[Commercial Banking/contents/10 - Capital Adequacy and Basel|CB ch. 10]]'s**, per the recorded three-way boundary. **The Enron/rating-agency material connects to [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s conflict-of-interest box and is not repeated.**
>
> **Additions beyond the source.**
>
> - **⚠️ §9 is the chapter's principal addition and the reason the chapter was flagged as the subject's spine.** **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]] computed a humped lender-return curve peaking at $r^*=18\%$ from a Rose & Hudgins footnote and could not explain it.** Building an explicit two-type pool from Mishkin's own two concepts **produces the same shape (here a cliff: 8.10% → −19.49%) and separates the two channels — *who applies* versus *what they do* — which CB could not do.** **Neither source connects them**: Rose & Hudgins measures without theory, Mishkin theorises without ever computing a return curve.
> - **⚠️ §2's maturity correction is mine**, though the idea is Mishkin's own footnote 1. **He raises the objection, states that stocks and debt are "actually equally important", and then presents fact 1 as established.** Computing the $T/m$ correction shows how far the ranking can move — **and, more usefully, identifies which fact is robust to it.**
> - **⚠️ §4's lemons model, the threshold $q^*=83.33\%$, and the observation that the failure is *discontinuous*, are mine.** **Mishkin narrates Akerlof verbally.** The threshold turns "the market functions poorly" into "the market has a cliff", **which is the qualitative fact that makes adverse selection different from an ordinary cost.**
> - **⚠️ §7's monitoring arithmetic ($p\cdot c$ against $c$, 50× at a 2% default rate) is mine.** **Mishkin says debt requires "less frequent" verification and leaves it there.** Quantifying it establishes that this, not tax, is the dominant reason debt dominates equity.
> - **⚠️ §8's critical net worth ($E^*\approx\$49{,}495$) is mine.** **Mishkin tells the story twice — at \$1,000 and at \$91,000 — and never says where the switch happens.** **The computed threshold reproduces both of his cases and is what the story was for.**
> - **§6's linearity of the principal–agent wedge in the ownership share, and the observation that the fix contradicts the reason outside equity exists, are mine.**
> - **⚠️ §5's identification of the free-rider problem as contradicting [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s efficient-market mechanism — the Grossman–Stiglitz tension — is my synthesis.** **The two chapters sit ninety pages apart in the same book and Mishkin never notes that one's virtue is the other's obstacle.**
> - **§1's sharpening of fact 3 (below 5.3%, not below 10%) is mine.**
> - **§10's row-count observation — that "financial intermediation" appears under all three problems, which is why [[01 - The Financial System and What Money Is|ch. 01]]'s answer is *the* answer — is my reading of Mishkin's own table.**
> - **The identification of §2 as the fifth instance of the vault's measurement-boundary result is my synthesis.**

**Previous:** [[05 - The Stock Market, Rational Expectations and Efficient Markets]] · **Next:** [[07 - Financial Crises]]
