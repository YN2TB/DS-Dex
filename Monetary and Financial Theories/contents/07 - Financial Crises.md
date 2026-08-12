---
subject: Monetary and Financial Theories
chapter: 7
tags: [ds, economics, financial-crises, debt-deflation, bank-panic, currency-mismatch, emerging-markets, leverage]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 12–13"
---

# Financial Crises

**This chapter is [[06 - Asymmetric Information and Financial Structure|ch. 06]] run forwards in time.** **Every box in Mishkin's crisis diagram routes through one sentence — *adverse selection and moral hazard problems worsen and lending contracts*.** **A crisis is what happens when the information problems ch. 06 described stop being solved.**

**Five results.**

**§2 — ⚠️ THE CHAPTER'S BEST FINDING, and it comes from a mismatch.** Mishkin's debt-deflation example gives net worth falling from \$10m to **\$1m**. *(Computed exactly: it falls to **\$0** — he used the approximation $D(1+\pi)$ where the exact figure is $D/(1-\pi)$.)* **⚠️ The approximation error is exactly \$1m — which is precisely the difference between "the firm survives, barely" and "the firm is insolvent."** **Fourth dropped cross term in the subject, and by far the most consequential.**

**§3 — what Table 1 says once you divide the columns.** *(Computed: **the average country has spent 8.3% of its modern history in a banking crisis — about one year in twelve.** And **"most crises" and "most time in crisis" are different rankings**: France has the most episodes, the US the most years.)*

**§4 — the repo spiral.** *(Computed: **a 20% asset-price fall combined with haircuts going 0 → 50% cuts borrowing capacity by 60%.**)* **This is a bank run on institutions with no deposits and no deposit insurance — which is why the safety net did not stop it.**

**§6 — ⚠️ currency mismatch IS debt deflation in a second currency.** *(Computed: a 10% devaluation wipes out a firm with 10% equity, exactly as a 10% deflation does. **Same equation.**)* **Mishkin puts them in two separate chapters and never says so — and the policy corollary reverses the standard advice.**

**§7 — the chaebol arithmetic.** *(Computed: at a **0.2% return on assets** and 80% debt at 8%, a chaebol loses **6.2% of assets a year** and exhausts 20% equity in **3.2 years**.)* **⚠️ The loans were not risky — they were arithmetically unrepayable, and everyone could see it.**

## 📘 Main Knowledge

### 1. The three stages

| stage | advanced economies | emerging economies |
|---|---|---|
| **one** | **initial phase** — credit boom/bust, asset-price boom/bust, or rising uncertainty | **initial phase** — mismanaged liberalization **(path A)** or **severe fiscal imbalances (path B)** |
| **two** | **banking crisis** | **⚠️ currency crisis** |
| **three** | **debt deflation** *(sometimes)* | **full-fledged financial crisis** |

**Stage one, three possible starts:**

- **Credit boom and bust.** **Financial innovation or *financial liberalization* lets institutions lend into businesses they cannot yet price.** *(Mishkin: "lenders may not have the expertise, or the incentives, to manage risk appropriately… credit booms eventually outstrip the ability of institutions — **and government regulators** — to screen and monitor.")* **Losses mount, net worth falls, institutions *deleverage*, the boom becomes a crash.**
- **Asset-price boom and bust.** **A bubble bursts; firms' net worth and collateral fall, so they have less "skin in the game"** ⇒ **moral hazard rises** ⇒ lenders tighten. *(This is [[06 - Asymmetric Information and Financial Structure|ch. 06]] §8's threshold being crossed at scale.)*
- **Increase in uncertainty.** **Screening becomes impossible.** *(Mishkin's roll-call: Ohio Life 1857, Jay Cooke 1873, Grant and Ward 1884, Knickerbocker Trust 1907, Bank of the United States 1930, and **Bear Stearns, Lehman Brothers and AIG in 2008**.)*

> [!warning] ⚠️ Stage two is CB ch. 08's computed run
> **The source of contagion is asymmetric information: depositors cannot tell good banks from bad, so they run on *both*.** **Fire sales then push prices down far enough to make more banks insolvent.**
>
> **[[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]] already computed this**: a bank with **9.82% equity, every asset performing and zero defaults**, went **insolvent at 48.5% withdrawals**. **⇒ the run does not *reveal* insolvency, it *creates* it** — which is exactly why Mishkin says panics produce "runs on banks, both good and bad".

> [!note] The safety net is part of the mechanism, not only the cure
> **Deposit insurance "weakens market discipline and increases the moral hazard incentive for banks to take on greater risk".** **Insured savers supply funds to undisciplined banks.** **⇒ the institution that prevents stage two contributes to stage one** — which is why [[00-Index]] folds Mishkin's ch. 10 deposit-insurance material into [[06 - Asymmetric Information and Financial Structure|ch. 06]] rather than treating it as pure remedy.

### 2. ⚠️ Debt deflation — and the approximation that changes the answer

**Debt is fixed in *nominal* terms; assets are real. So an unanticipated fall in the price level raises the real value of liabilities and leaves assets alone.**

**Mishkin's example: a firm with \$100m of assets, \$90m of long-term liabilities, hence \$10m of net worth. The price level falls 10%.**

| | Mishkin | **exact** |
|---|---|---|
| real value of liabilities | \$99m | **\$100m** |
| real value of assets | \$100m | \$100m |
| **real net worth** | **\$1m** | **\$0** |

> [!warning] ⚠️ He used $D(1+\pi)$ where the exact figure is $D/(1-\pi)$
> $$\text{exact}=\frac{D}{1-\pi}=D\left(1+\pi+\pi^2+\cdots\right)\qquad\text{approximation}=D(1+\pi)$$
> $$\text{error}=\frac{D\pi^2}{1-\pi}=\frac{90\times0.01}{0.90}=\mathbf{\$1\text{m}}$$
>
> **⚠️ And \$1m is exactly the whole remaining net worth.** **The approximation is the difference between "the firm survives, barely" and "the firm is insolvent."**
>
> **This is the fourth dropped cross term in this subject** — [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation (dropping $r\pi^e$), ch. 02's duration (dropping convexity), [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s arithmetic-versus-geometric average, and now this. **⚠️ It is by far the most consequential, because the error straddles zero.**
>
> **Not filed as an erratum.** **The approximation is standard, and it *understates* Mishkin's own point** — the exact arithmetic makes debt deflation worse, not better. **But it is the sharpest available demonstration of why the vault's rule matters: *always ask what the neglected term is proportional to*, because "small" is a statement about magnitude and not about consequence.**

**Generalising** — with assets $A$, nominal debt $D$, equity $E=A-D$:

$$E_{\text{new}}=A-\frac{D}{1-\pi}\qquad\qquad \frac{\Delta E}{E}\approx-\frac{D}{E}\,\pi$$

| leverage $D/E$ | equity | after 10% deflation | equity lost | **wipe-out at** |
|---|---|---|---|---|
| 1.0 | 50.0 | 44.44 | 11.1% | 50.00% |
| 4.0 | 20.0 | 11.11 | 44.4% | 20.00% |
| **9.0** | **10.0** | **0.00** | **100.0%** | **10.00%** |
| 19.0 | 5.0 | −5.56 | 211.1% | **5.00%** |

> [!warning] ⚠️ The loss is amplified by leverage, and the wipe-out threshold is $\pi^*=E/A$
> **A firm with 10% equity is destroyed by a 10% deflation.** **Nothing on the balance sheet changed** — no loan defaulted, no asset was sold, no decision was made. **The price index moved.**
>
> *(Same mathematics as [[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|CB ch. 09]]'s capital adequacy, where a small write-down consumes a large fraction of equity. **The novelty is the trigger.**)*
>
> **And it is [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher result with the sign flipped and applied to a *balance sheet* rather than a *return*:** ch. 02 found unexpected **inflation** transfers from lender to borrower; **deflation transfers from borrower to lender**, and the transfer is levered.

**The Great Depression, from Mishkin's own figures:**

| | | |
|---|---|---|
| US stocks, Oct–Dec 1929 | 100 → 60 | **−40.0%** ✓ |
| US stocks, to trough | 100 → 10 | −90.0% |
| wheat, Sep 1929–Sep 1930 | \$1.37 → \$0.87 | **−36.5%** ✓ *(book: 37%)* |
| commodity index 1920–1932 | 231 → 74 | **−68.0%** |
| **world imports, Jan 1929 – Jan 1932** | \$2,998m → \$992m | **−66.9%** |

**1,860 US banks failed between August 1931 and January 1932 alone.** **German unemployment reached 6 million in 1932 — 25% of the workforce.** *(Kindleberger's summary, which Mishkin quotes: **"new lending stopped because of falling prices, and prices kept falling because of no new lending."**)*

### 3. ⚠️ Table 1 — what it says once you divide the columns

*(Reinhart & Rogoff, banking crises since independence or 1800 — the table survived extraction complete. **The last two columns are computed.**)*

| country | crises | since 1945 | % of years | **years in crisis** | **avg length** |
|---|---|---|---|---|---|
| Argentina | 9 | 4 | 8.8 | 19.1 | 2.12 yr |
| Brazil | 11 | 3 | 9.1 | 19.7 | 1.80 yr |
| Canada | 8 | 1 | 8.5 | 18.4 | 2.31 yr |
| **France** | **15** | 1 | 11.5 | 25.0 | **1.66 yr** |
| Germany | 8 | 2 | 6.2 | 13.5 | 1.68 yr |
| **Russia** | **2** | 2 | **1.0** | **2.2** | 1.08 yr |
| United Kingdom | 12 | 4 | 9.2 | 20.0 | 1.66 yr |
| **United States** | 13 | 2 | **13.0** | **28.2** | **2.17 yr** |
| **MEAN** | **9.3** | 2.2 | **8.3** | **17.9** | **1.93 yr** |

> [!warning] ⚠️ The average country has spent about 8% of its modern history in a banking crisis
> **Roughly one year in twelve.** **Crises are not rare events interrupting normal times — on this evidence they are a *recurring feature* of banking**, which is what a chapter organised around asymmetric information should predict.

> [!warning] ⚠️ "Most crises" and "most time in crisis" are different rankings
> **Mishkin names the two extremes — Russia the most stable, the US with the most years in crisis — and stops.** *(Computed:)*
>
> - **France has the most *episodes* (15) but only 1.66 years each;**
> - **the US has the most *years* (28.2) because its crises run longest (2.17 years each).**
>
> **⇒ the running theme again: *which number?*** **A table printing both invites you to conflate them, and they answer different questions** — frequency versus duration. *(Same shape as [[01 - The Financial System and What Money Is|ch. 01]]'s "which M?", [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s "which leg?".)*
>
> **And note the post-1945 column: for most countries crises since 1945 are a small fraction of the total** *(1 of 15 for France, 2 of 13 for the US)*. **The post-war regulatory settlement did something** — which is what §9's long-term responses are about.

### 4. ⚠️ The repo spiral — a run without depositors

**The shadow banking system — hedge funds, investment banks, other non-depository firms — funded itself with *repurchase agreements*, posting assets as collateral.** **The lender's protection is the *haircut*.** *(Mishkin's example: borrow \$100m, post \$105m of mortgage-backed securities ⇒ a 5% haircut.)*

**"At the start of the crisis, haircuts were close to zero, but eventually they rose to nearly 50%… financial institutions could borrow only half as much with the same amount of collateral."**

$$\text{borrowing capacity}=(1-h)\times\text{collateral value}$$

*(Computed — **both terms fell at once**, which is the whole mechanism:)*

| collateral value | haircut | capacity | vs. start |
|---|---|---|---|
| 1.00 | 0% | 1.000 | — |
| 0.90 | 20% | 0.720 | −28.0% |
| **0.80** | **50%** | **0.400** | **−60.0%** |
| 0.70 | 50% | 0.350 | −65.0% |

> [!warning] ⚠️ A 20% asset-price fall becomes a 60% credit contraction
> **The haircut does the larger part of the work — and a haircut is not a price.** **It is a judgement about uncertainty**, which is [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s adverse selection priced into a margin.
>
> **And it is self-reinforcing:** less borrowing → fire sales → lower prices → higher haircuts → less borrowing. *(Mishkin: the fire sales "led to a further decline in financial institutions' asset values… forcing financial institutions to scramble even more for liquidity.")*
>
> **⚠️ This is a bank run.** **The runners are repo lenders instead of depositors, and the withdrawal takes the form of a higher haircut rather than a queue — but the arithmetic is [[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]]'s cascade.** **It happened to institutions with no deposits and no deposit insurance, which is precisely why the safety net did not stop it.**

### 5. The 2007–2009 crisis — three causes, all of them ch. 06 failures

| cause | which ch. 06 failure |
|---|---|
| **financial innovation** — securitisation, then CDOs | complexity outrunning the ability to price |
| **agency problems** — the **originate-to-distribute** model | **the principal–agent problem, with the agent's stake at *zero*** |
| **credit-rating conflicts** | agencies rated the products they helped structure |

> [!note] The AAA was wrong even without dishonesty
> **[[Commercial Banking/contents/06 - Hedging with Derivatives|CB ch. 06]] computed it: mean pool loss is 5.00% at *every* correlation while senior-tranche loss goes 0.0000% → 1.8044%.** **Nothing about the loans had to change.** **⇒ the modelling error and the conflict of interest are separate failures, and either would have sufficed.**

> [!warning] ⚠️ And the borrower side is ch. 06 §8's threshold crossed
> **When a house is "underwater" the owner's equity is *negative*, so the critical net worth is breached and walking away is rational.** *(Mishkin: "tremendous incentives to walk away from their homes and just send the keys back to the lender.")* **The moral hazard did not require anyone to behave badly — the arithmetic changed sign.**

**The figures the chapter states:**

| | |
|---|---|
| Spanish household debt / national income, 2007 peak | **154.4%** *(almost doubled from 2000)* |
| Spanish housing, €2,101/m² peak → 2014 | −31% in six years |
| **Iceland: krona 54.5/CHF → 103/CHF** *(Dec 2007 – Oct 2008)* | **foreign-currency mortgage debt doubled** |
| Iceland mortgage debt / GDP, end-2006 → end-2008 | **75.5% → 129%** |
| repo haircuts | ~0% → **~50%** |
| Bear Stearns sale to Bank of America, March 2008 | **60% below its value a year earlier** |
| ratings downgrades triggering BNP Paribas, 7 Aug 2007 | **>\$10bn** |
| US GDP, two quarters after Lehman | **−5.4%, then −6.4%** annual rate |
| US unemployment, late 2009 | **over 10%** |
| credit spreads during the crisis | **+400 bp** *([[04 - The Risk and Term Structure of Interest Rates|ch. 04]] measured the Baa–Treasury leg at +360 bp)* |

> [!warning] ⚠️ Iceland is the bridge between the chapter's two halves
> *(Computed: **the krona fell by a factor of 1.89** while **mortgage debt/GDP rose by a factor of 1.71**.)* **The two moves are of the same order, and only "a small but significant chunk" of Icelandic mortgages were foreign-denominated** *(the rest of the gap is a falling GDP)*.
>
> **⇒ the debt ratio rose largely because the *currency* fell, not because anyone borrowed more.** **That is §6's currency mismatch happening inside an *advanced* economy** — and Mishkin reports it without labelling it as the mechanism his next chapter is built on.

*(**Northern Rock**, September 2007 — the first UK bank run in over a century, and it **relied on short-term repo borrowing rather than deposits for funding.** The point of §4 in one institution.)*

### 6. ⚠️ Currency mismatch IS debt deflation in a second currency

$$\textbf{currency mismatch}=\text{debts in foreign currency, assets and revenues in domestic currency}$$

*(Computed — a firm with 100 pesos of assets and dollar debt worth 90 pesos:)*

| devaluation | dollar debt in pesos | assets | **net worth** |
|---|---|---|---|
| 0% | 90.0 | 100.0 | **10.0** |
| **10%** | **100.0** | 100.0 | **0.0** |
| 25% | 120.0 | 100.0 | **−20.0** |
| 50% | 180.0 | 100.0 | **−80.0** |

> [!warning] ⚠️ Compare §2. They are the same equation.
> $$\textbf{debt deflation:}\quad\text{real debt}=\frac{D}{1-\pi}\qquad\text{assets real, unchanged}$$
> $$\textbf{currency mismatch:}\quad\text{peso debt}=\frac{D}{1-d}\qquad\text{assets in pesos, unchanged}$$
>
> **A 10% deflation and a 10% devaluation both wipe out a firm with 10% equity.** **One mechanism — *nominal debt revalued against unchanged assets* — and Mishkin puts it in two separate chapters without ever saying so.**

> [!warning] ⚠️ And the policy corollary reverses the standard advice
> **For an advanced economy a devaluation is *expansionary* — exports cheapen.** **For an emerging economy with currency mismatch it is *contractionary*, because it destroys the net worth of every borrower simultaneously.**
>
> **⇒ that is why the "twin crises" exist as a category**, and why the emerging-market sequence has a currency crisis where the advanced sequence has a banking crisis.
>
> **It also explains the rock and a hard place.** **Raise rates to defend the currency and you destroy already-weak banks** *(and, via [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s Stiglitz–Weiss cliff, worsen adverse selection: "when interest rates rise, high-risk firms are most willing to pay the high interest rates")*. **Don't, and the currency goes, which destroys every borrower.** **There is no good option — and speculators can see that, which is what makes the attack "an almost sure-thing bet."**

*(Mishkin's own contrast: **the dollar was never threatened by speculative attack during 2007–08, and the euro's external value held during the Eurozone crisis.** **Advanced economies are not immune — the UK and Italy were forced out of the European Monetary System in 1992 — but their crises do not usually run through the currency.**)*

### 7. ⚠️ South Korea — Table 2, and the chaebol arithmetic

**Before the crisis South Korea's fundamentals were strong: inflation below 5%, real growth near 7%, low unemployment, a slight budget surplus.** **The crisis came down path A — *mismanaged financial liberalization*.**

*(Table 2, external debt as % of GDP — survived extraction complete. **The share column is computed.**)*

| year | total | short-term | **short-term share** |
|---|---|---|---|
| 1993 | 11.4% | 5.0% | **43.9%** |
| 1994 | 12.5% | 6.7% | 53.6% |
| 1995 | 14.1% | 8.1% | 57.4% |
| 1996 | 17.5% | 10.2% | 58.3% |
| **1997** | **28.2%** | **16.5%** | **58.5%** |

**Growth 1993→1997: total ×2.47, short-term ×3.30, long-term ×1.83.**

> [!warning] ⚠️ That is a policy, visible in the data
> **Mishkin: the government "effectively allowed unlimited short-term foreign borrowing by financial institutions but maintained quantity restrictions on long-term borrowing."** **He adds that this "made no economic sense" but "made complete political sense" — the chaebols needed the money, and short-term funds are easier to raise.**
>
> **⚠️ Short-term capital is exactly the kind that can leave.** **So the policy did not merely permit a build-up of debt — it *selected for the most run-prone form of it*.** **Table 2 is that policy's fingerprint.**

**The chaebols.** **Family conglomerates with sales near 50% of GDP, politically powerful, and deemed *too big to fail*.** **Return on assets "never much more than 3%" against a US comparable of 15–20%, falling to **0.2% in 1996**; only the top five were profitable at all, and ranks 6–30 were often negative.**

*(Computed — a chaebol with 80% debt at 8%:)*

| ROA | annual profit | 20% equity exhausted in |
|---|---|---|
| **15.0%** | +8.60% | never — solvent |
| 3.0% | −3.40% | 5.9 yr |
| 1.0% | −5.40% | 3.7 yr |
| **0.2%** | **−6.20%** | **3.2 yr** |

> [!warning] ⚠️ The loans were not risky — they were arithmetically unrepayable
> **At a 0.2% return on assets and 80% debt at 8%, a chaebol loses 6.2% of its assets every year and exhausts 20% equity in 3.2 years.** **No forecast is required; this is arithmetic on published figures.**
>
> **Mishkin says exactly this: "any banker would pull back on lending to these conglomerates *if there were no government safety net*."**
>
> **⚠️ Which is the chapter's sharpest single point: the lending was not a mistake. It was a correct response to a guarantee.** **The chaebols were too big to fail, so the banks were lending to the *government* while appearing to lend to the firms.** **[[06 - Asymmetric Information and Financial Structure|Ch. 06]]'s moral hazard, with the taxpayer as the party bearing it.**

**The rest follows mechanically:** **Hanbo (14th largest chaebol) failed 23 January 1997; five more of the top 30 failed within the year; the stock market fell over 50%; then the won collapsed and Table 2's short-term debt could not be rolled.**

### 8. Argentina — the control experiment

> [!warning] ⚠️ Mishkin does not call it one, but that is what it is
> **"In contrast to Mexico and the East Asian countries, Argentina had a *well-supervised banking system*, and a lending boom *did not occur* before Argentina's crisis. The banks were in surprisingly good shape."**

**So the crisis came entirely down path B — *severe fiscal imbalances*.** **The provinces control a large share of public spending while the federal government raises the revenue, so provinces overspend and are periodically bailed out ⇒ perennial deficits.** **The 1998 recession cut tax revenue further.** **The government coerced banks into absorbing its debt; when investors doubted repayment, the debt's value collapsed and blew holes in the balance sheets of the best-supervised banks in the region.** **A full bank panic began in November 2001, with deposit outflows running near \$1bn a day.**

> [!warning] ⚠️ The lesson the pairing delivers: good bank supervision is not sufficient
> **Korea's crisis came *through* the banks; Argentina's came through the *sovereign* and used the banks as a transmission channel.** **A supervisor watching only lending standards would have given Argentina a clean bill of health in 2000.**
>
> *(And the mechanism is [[02 - The Meaning of Interest Rates|ch. 02]]'s: the banks held government bonds, and a fall in the bond price **is** a rise in the yield. **The losses were securities losses — [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]]'s and [[Commercial Banking/contents/07 - The Investment Portfolio|ch. 07]]'s territory — arriving through a fiscal door.**)*

*(Table 1 — Mexico and Thailand — also survived complete:)*

| | Mex 92 | 93 | 94 | **95** | Th 95 | 96 | 97 | **98** |
|---|---|---|---|---|---|---|---|---|
| GDP growth (%) | 3.5 | 2.7 | 4.9 | **−6.3** | 8.1 | 5.6 | −2.7 | **−7.6** |
| net govt lending (% GDP) | 0.1 | 0.1 | −0.6 | −3.9 | **3.0** | **2.7** | −1.7 | −6.3 |
| **current account (% GDP)** | **−8.9** | −6.8 | −8.1 | **−0.4** | **−8.0** | −8.0 | −2.0 | **+12.5** |

> [!warning] ⚠️ Read the current-account row
> **It goes from −8.9% to −0.4% in Mexico and from −8.0% to +12.5% in Thailand.** **A current-account deficit is financed by capital *inflows*; when they stop, the deficit must close — and it closes by imports collapsing, which is the GDP row.**
>
> **⇒ the "improvement" in the external balance and the collapse in output are the *same event*.** **A country cannot choose to run a smaller deficit painlessly when the financing disappears** — which is the **sudden stop** in one phrase.
>
> **And note Thailand's fiscal row: surpluses of 3.0% and 2.7% right up to the crisis.** **Thailand's government was not the problem — which is why Argentina is a different *path*, not a different degree.**

### 9. What was done, and what remains

**Intervention:** liquidity injections by the ECB and the Fed, bailouts, recapitalisation, guarantees. *(Credit spreads rose over 400 bp during the crisis and their narrowing marks the recovery.)*

**Latvia's "expansionary contraction"** — a banking sector 60% foreign-owned; €7.5bn (**37% of GDP**) to recapitalise; **25% of state workers laid off, 40% salary cuts**; GDP falling over 25% — and then growth resumed. **Mishkin presents it as controversial, correctly: one country is one observation.**

**Long-term responses:** higher capital and liquidity requirements, **macroprudential** regulation, resolution regimes for too-big-to-fail, consumer protection, international coordination through Basel.

> [!note] The LIBOR scandal
> **A benchmark set by *submission* rather than by *transaction* is an invitation.** **[[06 - Asymmetric Information and Financial Structure|Ch. 06]]'s asymmetric information inside the plumbing itself.**

> [!warning] ⚠️ The prevention list for emerging markets is ch. 06's tool list, plus one
> **Better accounting and disclosure; stronger property rights and contract enforcement; prudential supervision with resources and independence** — all of which [[06 - Asymmetric Information and Financial Structure|ch. 06]] identified.
>
> **The one this chapter adds is SEQUENCING: liberalise *after* the supervisory apparatus exists, not before.** **South Korea did it in the other order**, and §7's Table 2 is what that looks like in data.

## ✏️ Exercises

**1. (Debt deflation.)** (a) Work Mishkin's example exactly. (b) Generalise it. (c) What does the discrepancy with his figure teach?

> [!example]- Solution
> **(a) Net worth falls to zero, not to \$1m.**
>
> **A firm with \$100m assets and \$90m long-term liabilities has \$10m net worth. The price level falls 10%.**
>
> $$\text{real debt}=\frac{90}{1-0.10}=\mathbf{\$100\text{m}}\qquad\Rightarrow\qquad \text{net worth}=100-100=\mathbf{\$0}$$
>
> **Mishkin gives \$99m and \$1m.** **He used $D(1+\pi)=90\times1.1=99$ rather than $D/(1-\pi)$.**
>
> **The economics is unaffected in direction: debt is fixed in nominal terms and assets are real, so deflation raises the real burden of debt while leaving assets alone.** *(It is [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher result with the sign flipped — unexpected **inflation** transfers from lender to borrower, deflation from borrower to lender — applied to a balance sheet rather than a return.)*
>
> **(b) The loss is amplified by leverage; the wipe-out threshold is $\pi^*=E/A$.**
>
> $$E_{\text{new}}=A-\frac{D}{1-\pi}\qquad\qquad\frac{\Delta E}{E}\approx-\frac{D}{E}\pi$$
>
> | $D/E$ | equity | after 10% deflation | lost |
> |---|---|---|---|
> | 1.0 | 50.0 | 44.44 | 11.1% |
> | 4.0 | 20.0 | 11.11 | 44.4% |
> | **9.0** | **10.0** | **0.00** | **100.0%** |
> | 19.0 | 5.0 | −5.56 | 211.1% |
>
> **A firm with 10% equity is destroyed by a 10% deflation; one with 50% equity survives to 50%.**
>
> **⚠️ And nothing on the balance sheet changed.** **No loan defaulted, no asset was sold, no decision was made — the price index moved.** *(Same mathematics as [[Commercial Banking/contents/09 - Managing Deposits and Nondeposit Funding|CB ch. 09]]'s capital adequacy; the novelty is the trigger.)*
>
> **(c) That "small" is a statement about magnitude, not about consequence.**
>
> **The approximation error is $D\pi^2/(1-\pi)=\$1\text{m}$ — about 1.1% of the debt.** **⚠️ But \$1m is exactly the whole remaining net worth**, so the approximation is the difference between *"the firm survives, barely"* and *"the firm is insolvent."*
>
> **This is the fourth dropped cross term in the subject** — the Fisher equation ($r\pi^e$), duration (convexity), the arithmetic-versus-geometric average, and this — **and it is the most consequential, because the error straddles zero.**
>
> **⚠️ It is not an erratum.** **The approximation is standard, and it *understates* Mishkin's own argument: the exact arithmetic makes debt deflation worse.** **But it is the sharpest available case for the vault's rule — always ask what the neglected term is proportional to**, because a term that is negligible against the *debt* need not be negligible against the *equity*, and equity is what determines survival.

**2. (Hard — Table 1.)** (a) What does the table say once you divide the columns? (b) Which country is worst? (c) What does the post-1945 column suggest?

> [!example]- Solution
> **(a) The average country has spent 8.3% of its modern history in a banking crisis.**
>
> *(Computed from the table's own columns over ~217 years:)*
>
> | | crises | % of years | **years in crisis** | **avg length** |
> |---|---|---|---|---|
> | France | **15** | 11.5 | 25.0 | 1.66 yr |
> | United States | 13 | **13.0** | **28.2** | **2.17 yr** |
> | Russia | **2** | **1.0** | **2.2** | 1.08 yr |
> | **MEAN** | **9.3** | **8.3** | **17.9** | **1.93 yr** |
>
> **About one year in twelve.** **⚠️ Crises are not rare events that interrupt normal times — on this evidence they are a recurring feature of banking**, which is precisely what a theory built on asymmetric information should predict. *(If crises were exogenous shocks you would expect no such regularity across eleven countries with different histories, laws and currencies.)*
>
> **(b) It depends which question you are asking — and that is the point.**
>
> - **France has the most *episodes*: 15.**
> - **The US has the most *years*: 28.2, because its crises last longest (2.17 years against France's 1.66).**
>
> **Mishkin names the two extremes — Russia most stable, the US with the most years — and stops.** **⚠️ Dividing the columns shows "frequency" and "duration" give different rankings**, and a table printing both invites conflation.
>
> **Same shape as the subject's running theme** — *which M?* ([[01 - The Financial System and What Money Is|ch. 01]]), *which interest rate?* ([[02 - The Meaning of Interest Rates|ch. 02]]), *which curve moved?* ([[03 - The Behavior of Interest Rates|ch. 03]]), *which leg?* ([[04 - The Risk and Term Structure of Interest Rates|ch. 04]]), *flows or stocks?* ([[06 - Asymmetric Information and Financial Structure|ch. 06]]).
>
> *(A caution on Russia's "1.0%": two crises since 1800 in a country whose banking system was **abolished for seventy years** is not evidence of stability. **The denominator is a judgement** — the same measurement-boundary point again, and Mishkin's "most stable banking system in the sample" reads that number without qualification.)*
>
> **(c) That the post-war regulatory settlement did something.**
>
> **For most countries crises since 1945 are a small fraction of the total** — **1 of 15 for France, 2 of 13 for the US, 1 of 8 for Canada.** **Roughly seventy post-war years contain far fewer crises than the preceding 145.**
>
> **⚠️ But be careful what this shows.** It is consistent with deposit insurance, capital regulation and lender-of-last-resort facilities working — **and also with those institutions *suppressing* crises rather than preventing them**, which §1 warns about when it notes that deposit insurance "weakens market discipline and increases the moral hazard incentive". **The table cannot distinguish these**, and 2007–09 is one observation on the side of suppression.

**3. (Hard — the repo spiral.)** (a) Compute the borrowing-capacity collapse. (b) Why is it self-reinforcing? (c) Why did the safety net not stop it?

> [!example]- Solution
> **(a) A 20% price fall plus haircuts of 50% cuts capacity by 60%.**
>
> $$\text{borrowing capacity}=(1-h)\times\text{collateral value}$$
>
> | value | haircut | capacity | change |
> |---|---|---|---|
> | 1.00 | 0% | 1.000 | — |
> | 0.90 | 20% | 0.720 | −28.0% |
> | **0.80** | **50%** | **0.400** | **−60.0%** |
>
> **Both terms fell at once**, which is the whole mechanism — **and the haircut does the larger part of the work.**
>
> **⚠️ A haircut is not a price.** **It is a judgement about uncertainty** — [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s adverse selection priced into a margin. **So a lender who cannot tell good collateral from bad demands more of it from everyone**, which is the lemons problem expressed as a percentage.
>
> **(b) Because the output of each round is the input to the next.**
>
> **Less borrowing capacity → institutions must sell assets to fund themselves → selling quickly requires lowering the price → collateral is worth less *and* looks riskier → haircuts rise → less borrowing capacity.**
>
> *(Mishkin: the fire sales "led to a further decline in financial institutions' asset values. This decline lowered the value of collateral further, raising haircuts and thereby forcing financial institutions to scramble even more for liquidity.")*
>
> **⚠️ Nothing stops the loop from inside.** **Each participant is behaving prudently — protecting itself against a collateral value it can no longer assess — and the aggregate of prudent responses is the collapse.**
>
> **(c) Because it was a run on institutions the safety net was not built for.**
>
> **This is a bank run: the runners are repo lenders instead of depositors, and the withdrawal takes the form of a higher haircut rather than a queue at the door.** **The arithmetic is [[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]]'s cascade — a solvent institution forced to liquidate at fire-sale prices becomes insolvent.**
>
> **⚠️ But the shadow banking system has no deposits and therefore no deposit insurance**, and it is "not as tightly regulated as banks". **The instrument that had made runs on *banks* rare for seventy years simply did not apply.**
>
> **Northern Rock is the demonstration in one institution: the first UK bank run in over a century, at a lender that "had relied on short-term borrowing in the repo market rather than deposits for its funding."** **⇒ the protection attaches to a *funding form*, not to a *function*** — so financial innovation that moves the function outside the form moves it outside the protection. *(Which is the deep reason §9's long-term responses concentrate on resolution regimes and macroprudential rules rather than on more deposit insurance.)*

**4. (Hard — currency mismatch.)** (a) Compute the effect of a devaluation. (b) What is the relationship to §2? (c) What follows for policy?

> [!example]- Solution
> **(a) A 10% devaluation wipes out a firm with 10% equity.**
>
> *(A firm with 100 pesos of assets and dollar debt worth 90 pesos:)*
>
> | devaluation | peso debt | assets | net worth |
> |---|---|---|---|
> | 0% | 90.0 | 100.0 | **10.0** |
> | **10%** | **100.0** | 100.0 | **0.0** |
> | 50% | 180.0 | 100.0 | **−80.0** |
>
> **Debts are in foreign currency; assets and revenues are in domestic currency.** **A devaluation raises the peso value of the debt and leaves the assets alone.**
>
> **(b) ⚠️ They are the same equation.**
>
> $$\textbf{debt deflation:}\ \frac{D}{1-\pi}\qquad\qquad\textbf{currency mismatch:}\ \frac{D}{1-d}$$
>
> **In both cases nominal debt is revalued against unchanged assets, and the damage is amplified by leverage.** **A 10% deflation and a 10% devaluation destroy the same firm.**
>
> **⚠️ Mishkin puts them in two separate chapters — advanced economies and emerging economies — and never says they are one mechanism.** *(Iceland is the case that makes it visible: **the krona fell by a factor of 1.89** and **mortgage debt/GDP rose by a factor of 1.71** — the debt ratio rose because the *currency* fell, not because anyone borrowed more. **An advanced economy experiencing the emerging-economy mechanism.**)*
>
> **(c) The standard advice reverses sign.**
>
> **For an advanced economy a devaluation is *expansionary* — exports cheapen, and domestic-currency debts are unaffected.** **For an emerging economy with currency mismatch it is *contractionary*, because it destroys the net worth of every borrower simultaneously**, which worsens adverse selection and moral hazard and collapses lending.
>
> **⇒ that is why "twin crises" exist as a category**, and why the emerging-market sequence has a *currency* crisis where the advanced sequence has a *banking* crisis.
>
> **⚠️ And it explains the rock and a hard place.** **Raise rates to defend the currency and you destroy already-weak banks** — *and* worsen adverse selection, since "when interest rates rise, high-risk firms are most willing to pay the high interest rates", which is [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s Stiglitz–Weiss cliff. **Don't raise them, and the currency goes, which destroys every borrower.**
>
> **There is no good option, and *speculators can see that*** — which is exactly what makes the attack "an almost sure-thing bet". **The one-way bet exists because the government's constraint is public information.**

**5. (South Korea and Argentina.)** (a) What does Table 2 show? (b) Do the chaebol arithmetic. (c) What does pairing the two countries establish?

> [!example]- Solution
> **(a) A policy, visible in the data.**
>
> | year | total | short-term | **share** |
> |---|---|---|---|
> | 1993 | 11.4% | 5.0% | **43.9%** |
> | **1997** | **28.2%** | **16.5%** | **58.5%** |
>
> **Total debt grew ×2.47; short-term grew ×3.30; long-term only ×1.83.**
>
> **Mishkin explains why: the government "effectively allowed unlimited short-term foreign borrowing by financial institutions but maintained quantity restrictions on long-term borrowing."** **He calls this economically senseless and politically sensible** — the chaebols needed money, and short-term funds are easier to raise abroad because long-term lending is riskier for the creditor.
>
> **⚠️ Short-term capital is precisely the kind that can leave.** **So the policy did not merely permit a build-up of debt — it selected for the most run-prone form of it.** **Table 2 is the fingerprint**, and the crisis came when that debt could not be rolled.
>
> **(b) The loans were arithmetically unrepayable.**
>
> **Top-30 chaebol return on assets was "never much more than 3%" against a US comparable of 15–20%, and fell to 0.2% in 1996.**
>
> *(Computed at 80% debt costing 8%:)*
>
> | ROA | annual profit | 20% equity gone in |
> |---|---|---|
> | 15.0% | +8.60% | never |
> | 3.0% | −3.40% | 5.9 yr |
> | **0.2%** | **−6.20%** | **3.2 yr** |
>
> **At 0.2% ROA a chaebol loses 6.2% of its assets every year.** **No forecast is required — this is arithmetic on published figures.**
>
> **⚠️ So the lending was not a mistake; it was a correct response to a guarantee.** **The chaebols were "too big to fail", so the banks were lending to the *government* while appearing to lend to the firms** — [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s moral hazard with the taxpayer bearing it. **Mishkin says it outright: "any banker would pull back on lending to these conglomerates *if there were no government safety net*."**
>
> **(c) That good bank supervision is not sufficient.**
>
> **Argentina is the control experiment.** **"Argentina had a well-supervised banking system, and a lending boom did not occur… The banks were in surprisingly good shape."** **Its crisis came entirely down path B — fiscal imbalances**: provinces spending against federal revenue, perennial deficits, a 1998 recession cutting tax receipts, and a government coercing banks into holding its debt. **When investors doubted repayment, the debt's collapse blew holes in the best-supervised banks in the region.**
>
> **⚠️ Korea's crisis came *through* the banks; Argentina's came through the *sovereign* and used the banks as a transmission channel.** **A supervisor watching only lending standards would have passed Argentina in 2000.**
>
> **Thailand's fiscal row confirms the paths are genuinely distinct: surpluses of 3.0% and 2.7% right up to its crisis.** **Thailand's government was not the problem; Argentina's banks were not the problem.** **Two different diseases, one syndrome.**
>
> *(And Table 1's current-account row supplies the third lesson: Mexico goes −8.9% → −0.4% and Thailand −8.0% → +12.5%. **A deficit is financed by capital inflows; when they stop it must close, and it closes by imports collapsing — which is the GDP row.** **The "improvement" in the external balance and the collapse in output are the same event** — the sudden stop.)*

## 📝 Summary

- **A crisis is [[06 - Asymmetric Information and Financial Structure|ch. 06]] run forwards in time.** **Every box in the diagram routes through *adverse selection and moral hazard worsen and lending contracts*.**
- **Three stages.** Advanced: initial phase → **banking crisis** → *debt deflation*. Emerging: initial phase (**liberalization** or **fiscal imbalance**) → **currency crisis** → full crisis.
- **Stage two is [[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]]'s computed run** — 9.82% equity, zero defaults, insolvent at 48.5% withdrawals. **The run creates insolvency rather than revealing it**, which is why panics hit good banks too.
- **⚠️ Mishkin's debt-deflation figure uses $D(1+\pi)$ where the exact value is $D/(1-\pi)$** *(computed: net worth falls to **\$0**, not \$1m)*. **The \$1m error is the entire remaining net worth** — **fourth dropped cross term in the subject and the most consequential, because it straddles zero.** **Not an erratum: it *understates* his own point.**
- **⚠️ Debt deflation is leverage amplification** *(computed: $\Delta E/E\approx-(D/E)\pi$; wipe-out at $\pi^*=E/A$)* — **and nothing on the balance sheet changed.**
- **Great Depression figures verified**: stocks **−40%** by end-1929 and **−90%** to trough; wheat **−36.5%**; **world imports −66.9%**; **1,860 US banks failed in six months**; German unemployment 25%.
- **⚠️ Table 1: the average country spends 8.3% of its history in a banking crisis** *(computed)* — **one year in twelve.** **And "most crises" ≠ "most time in crisis"**: France has the most episodes, the US the longest ones (2.17 yr).
- **⚠️ The repo spiral: a 20% price fall plus haircuts 0→50% cuts borrowing capacity 60%** *(computed)*, **and it is self-reinforcing.** **A haircut is adverse selection priced into a margin.**
- **⚠️ It was a bank run on institutions with no deposits and no deposit insurance** — **the protection attaches to a funding form, not a function.** Northern Rock is the demonstration.
- **The 2007–09 causes are all ch. 06 failures** — innovation outrunning pricing, **originate-to-distribute (agent's stake = zero)**, rating conflicts. **And underwater homeowners are ch. 06 §8's threshold crossed.**
- **⚠️ Iceland is the bridge** *(computed: krona ×1.89, mortgage debt/GDP ×1.71)* — **the debt ratio rose because the currency fell.**
- **⚠️ CURRENCY MISMATCH IS DEBT DEFLATION IN A SECOND CURRENCY** *(computed: a 10% devaluation and a 10% deflation destroy the same firm)*. **Mishkin splits one mechanism across two chapters.**
- **⚠️ So devaluation is expansionary for an advanced economy and CONTRACTIONARY for an emerging one** — **the standard advice reverses sign**, which is why "twin crises" exist.
- **The rock and a hard place is a one-way bet** — raise rates and kill the banks, don't and lose the currency, **and speculators can see the constraint.**
- **⚠️ Korea's Table 2: the short-term share rose 43.9% → 58.5%** *(computed)* — **a policy that selected for the most run-prone debt.**
- **⚠️ The chaebol arithmetic: at 0.2% ROA, 20% equity is gone in 3.2 years** *(computed)*. **The loans were unrepayable, not risky — a correct response to a guarantee.**
- **⚠️ Argentina is the control: well-supervised banks, no lending boom, crisis anyway.** **Good supervision is not sufficient.**
- **The sudden stop**: a current account going −8.0% → +12.5% *and* GDP going −7.6% **are the same event.**
- **The prevention list is ch. 06's tool list plus SEQUENCING** — liberalise *after* the supervisory apparatus exists. **Korea did it the other way round.**

## ⚠️ Important Notes

1. **Every crisis mechanism routes through adverse selection and moral hazard.** If you cannot name which, you have not identified the mechanism.
2. **⚠️ Financial liberalization is beneficial long-run and dangerous short-run.** The chapter's policy content is about *order*, not direction.
3. **Deposit insurance is part of stage one as well as the cure for stage two.**
4. **⚠️ A run creates insolvency; it does not merely reveal it.**
5. **Contagion's source is asymmetric information** — depositors run on good banks because they cannot identify the bad ones.
6. **⚠️ Real debt is $D/(1-\pi)$, not $D(1+\pi)$.** The difference is small against the debt and can be total against the equity.
7. **⚠️ Always ask what a neglected term is proportional to.** Fourth instance in this subject.
8. **Debt deflation needs no default and no decision** — only a price index.
9. **The wipe-out threshold is $\pi^*=E/A$.** Leverage sets how much deflation a firm can survive.
10. **⚠️ Frequency and duration are different rankings.** Do not read "most crises" as "worst".
11. **A denominator is a judgement** — Russia's 1.0% covers seventy years with no private banking system.
12. **⚠️ A haircut is a judgement about uncertainty, not a price**, and it moves with the collateral value, not against it.
13. **Fire sales are individually prudent and collectively catastrophic.**
14. **⚠️ Safety nets attach to funding forms, not functions.** Innovation moves the function outside the protection.
15. **Originate-to-distribute sets the agent's stake to zero** — the extreme case of ch. 06's wedge.
16. **⚠️ Underwater means negative equity, so walking away is rational**, not dishonest.
17. **⚠️ Devaluation is expansionary for advanced economies and contractionary under currency mismatch.**
18. **Twin crises exist because currency and balance sheets are linked by denomination.**
19. **⚠️ Short-term foreign debt is the run-prone kind.** The *composition* matters more than the level.
20. **⚠️ Unrepayable ≠ risky.** Check whether the borrower can service debt from operations before asking about probabilities.
21. **Guarantees make bad lending rational.** Look for who bears the loss before calling a lender foolish.
22. **⚠️ Good bank supervision is not sufficient** — Argentina had it.
23. **A sudden stop shows up as an *improving* external balance.** The improvement is the damage.
24. **⚠️ Sequencing is the addition** — liberalise after supervision, not before.

> [!warning] Gaps in the source material
> **Two long chapters, and the extraction was good for prose and excellent for tables.**
>
> **⚠️ ALL THREE TABLES SURVIVED COMPLETE** — **ch. 12's Table 1** (banking crises across 11 countries × 3 columns), **ch. 13's Table 1** (Mexico and Thailand, 3 indicators × 8 years) and **ch. 13's Table 2** (South Korea's external debt, 2 rows × 5 years). **Sixth confirmation of the vault's rule: graphical exhibits are lost; tables set as text survive whole.** **All three are used here, and the derived columns (years in crisis, average length, short-term share) are computed from them.**
>
> **⚠️ ALL SIXTEEN FIGURES ARE LOST**, and unlike [[03 - The Behavior of Interest Rates|ch. 03]] **the prose does not name their data points** — checked, per the rule that chapter established. **The losses divide into two kinds.**
> - **Schematics** — the two **Figure 1**s (sequence of events in advanced and emerging crises) are flowcharts whose content is entirely stated in the prose, and §1 reproduces it. **No loss.**
> - **⚠️ Data series** — Great Depression stock indices and asset prices (ch. 12 Figures 2–3), Spanish and other housing series (Figures 4–5), **credit spreads through the crisis (Figure 6)**, and **the entire South Korean and Argentine picture** (ch. 13 Figures 2–12: inflation, real GDP growth, unemployment, the stock market, exchange rates, interest rates). **These are real losses.** **Only the values Mishkin states in prose or captions are retained** — inflation below 5% rising to nearly 10%; growth near 7% falling below −6%; unemployment below 3% rising above 8%; the stock market falling over 50%; Argentine growth falling at over 15% annually. **No series is reconstructed**, and no chart is drawn from a verbal description.
>
> **⚠️ ONE DISCREPANCY INVESTIGATED AND NOT FILED — the coffee price, ch. 12 p. 326.** The text reads *"the price of coffee decreased from \$.22 per lb to \$.10 per lb — a 46% decline"*. *(Computed: \$0.22 → \$0.10 is **−54.5%**, not −46%. To obtain −46% the end price would need to be ≈\$0.118 or the start ≈\$0.185.)* **Not filed**: **the wheat figure in the same sentence checks perfectly** (\$1.37 → \$0.87 = −36.5%, printed as 37%), which makes a mis-extracted digit in the `$.10` / `$.22` format more likely than an arithmetic error by the author — **and rule 4 requires ruling out my own extraction first.** **Recorded because the figure should not be quoted without checking the page image.**
>
> **⚠️ ONE APPROXIMATION RECORDED, NOT FILED — the debt-deflation example, ch. 12 p. 327** *(§2)*. **Mishkin computes real liabilities as $90\text{m}\times1.1=\$99\text{m}$ where the exact figure is $90/0.9=\$100\text{m}$, giving net worth of \$1m rather than \$0.** **The approximation $D(1+\pi)$ for $D/(1-\pi)$ is standard and its error here is 1.1% of the debt — but that error is 100% of the remaining equity.** **Not an erratum** *(the approximation is conventional, and it understates rather than overstates his own conclusion)*, **but it is the subject's fourth dropped cross term and the most consequential.** **Full entry in [[00-Index]]'s not-filed table.**
>
> **Nothing else mismatched.** The Great Depression percentages, the Iceland and Spain ratios, the Korean debt table, the crisis-spread figures and both applications' narrative arithmetic all check.
>
> **⚠️ SCOPE NOTE.** [[00-Index]] assigns **two chapters (M 12 and M 13) to this single note**, so both are compressed. **Deliberately reduced to their conclusions:** the detailed institutional history of the European sovereign debt crisis; the mechanics of CDO and CDS construction *(the risk result is [[Commercial Banking/contents/06 - Hedging with Derivatives|CB ch. 06]]'s and is cross-linked rather than repeated)*; the "Was the Fed to Blame for the Housing Bubble?" debate *(which belongs with [[09 - Tools and Conduct of Monetary Policy|ch. 09]])*; the full Basel III provisions and the international regulatory agenda *(prudential supervision is [[Commercial Banking/contents/10 - Capital Adequacy and Basel|CB ch. 10]]'s per the recorded boundary)*; and the China "noncrisis" and Latvia boxes, which are retained only as one-line cases.
>
> **Additions beyond the source.**
>
> - **⚠️ §2's exact computation is the note's most valuable addition, and it arrived as a *mismatch*.** **Recomputing Mishkin's own example to check it is what surfaced the approximation** — the vault's verification rule doing exactly what it exists for. **The generalisation ($\Delta E/E\approx-(D/E)\pi$, wipe-out at $\pi^*=E/A$) and the leverage table are mine**; Mishkin gives one worked case and no formula.
> - **⚠️ §6 is the note's principal analytical addition. The identification of currency mismatch and debt deflation as ONE MECHANISM is mine.** **Mishkin develops them in two chapters, with different names, different regions and different diagrams, and never observes that both are $D/(1-x)$ against unchanged assets.** **The policy corollary — that devaluation is expansionary for one economy and contractionary for the other, so the standard advice reverses sign — follows from the identification and is what makes it worth having.** *(The Iceland calculation showing the bridge in an advanced economy is also mine.)*
> - **⚠️ §3's derived columns are mine.** **Mishkin prints Table 1, names the two extremes, and moves on.** Dividing the columns yields **the 8.3% average** *(crises as a recurring feature, not an interruption)* and **the frequency-versus-duration distinction**, neither of which he draws. **The caution about Russia's denominator is also mine.**
> - **⚠️ §4's borrowing-capacity arithmetic is mine.** Mishkin states haircuts rose "to nearly 50%" and that institutions "could borrow only half as much". **Combining the haircut with the simultaneous collateral-price fall gives the 60% figure and shows the haircut does the larger part of the work.** **The identification of a haircut as adverse selection priced into a margin, and of the whole episode as a run on a funding form the safety net did not cover, is my synthesis.**
> - **⚠️ §7's chaebol arithmetic is mine and is the sharpest thing in the emerging-market half.** **Mishkin gives the ROA figures and the qualitative judgement; computing that a 0.2% ROA firm at 80% leverage exhausts its equity in 3.2 years converts "poor profitability" into "arithmetically unrepayable", which is what makes his own point about the safety net decisive.** **The short-term-share column of Table 2, and the reading of it as a policy fingerprint, are also mine.**
> - **§8's framing of Argentina as a *control experiment*, and of the current-account row as the sudden stop, are mine.** **Mishkin contrasts the two countries without naming what the contrast establishes.**
> - **The identification of Table 1's frequency/duration split as the sixth instance of the subject's "which number?" theme is my synthesis.**

**Previous:** [[06 - Asymmetric Information and Financial Structure]] · **Next:** [[08 - Central Banks and the Money Supply Process]]
