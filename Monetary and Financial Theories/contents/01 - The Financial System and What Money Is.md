---
subject: Monetary and Financial Theories
chapter: 1
tags: [ds, economics, money, financial-system, intermediaries, monetary-aggregates, liquidity]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 2–3"
---

# The Financial System and What Money Is

**The financial system exists to channel funds from savers to borrowers** — because the person with the surplus and the person with the productive opportunity are usually not the same person. **[[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] treated that market abstractly; this subject supplies the machinery underneath it.**

**Two results.**

**§3 — indirect finance dominates everywhere, and the reason is asymmetric information.** Transaction costs and risk-sharing matter, **but the reason that carries the whole subject is that borrowers know more than lenders** — which gives adverse selection before the deal and moral hazard after it. **[[06 - Asymmetric Information and Financial Structure|Ch. 06]] develops it.**

**§6 — "which M?" is not an academic question.** *(Computed: [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s quantity theory gives inflation forecasts **8 percentage points apart from the same data** depending on which aggregate you feed it.)* **That is why the Fed abandoned monetary targeting.**

> [!warning] ⚠️ Displayed formulas reconstructed — see [[00-Index]] for the parenthesis fault. *(Prose arithmetic is reliable in this book.)*

## 📘 Main Knowledge

### 1. What financial markets do

$$\textbf{channel funds from those with surplus funds to those with a shortage}$$

> [!note] Why that raises efficiency
> **The saver and the person with a productive investment opportunity are usually different people.** Without a mechanism connecting them, **the saving sits idle and the project is not built.**
>
> **This is the institutional content of [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s loanable-funds market** — that chapter drew a supply and a demand curve; this one asks *what actually moves the money.*

| route | mechanism |
|---|---|
| **direct finance** | borrowers sell securities to lenders in markets |
| **indirect finance** | a **financial intermediary** borrows from savers and lends to borrowers |

**§3 is about why the second dominates, and that is the chapter's real question.**

### 2. The structure of financial markets — four cuts

| | |
|---|---|
| **debt vs equity** | debt is a contractual claim to fixed payments; **equity is a *residual* claim** — paid last |
| **primary vs secondary** | primary raises new funds for the issuer; **secondary trading gives the issuer nothing** |
| **exchanges vs OTC** | one location versus many dealers |
| **money vs capital** | maturity **under** one year versus **over** |

> [!note] Why secondary markets matter even though the issuer gets no money
> **Two reasons, and both are about the primary market:**
> 1. **They make securities liquid**, which makes them easier to sell when first issued;
> 2. **they determine the price** at which the issuer can raise new funds.
>
> **So a secondary market is not a sideshow — it is what makes the primary market work.**

> [!note] Money-market instruments are a liquidity buffer, not an investment
> **Short maturity means smaller price fluctuations and greater liquidity** — which is exactly [[Commercial Banking/contents/07 - The Investment Portfolio|Commercial Banking ch. 07]]'s finding that a bank's securities portfolio **yields 3.75 points less than its loans on purpose.** *(It is held for liquidity, pledging and collateral, not for return.)*

### 3. ⚠️ Why intermediaries dominate

**Indirect finance is far more important than direct finance in every developed economy.** Households do not mostly buy bonds and shares directly — **they deposit with banks and buy fund units.** Three reasons:

**1. Transaction costs — economies of scale.**

*(Illustrated: a standard loan contract costing \$500 to draft is \$500 per contract for an individual and a few dollars per contract for a bank writing thousands. **Same document.**)*

**2. Risk sharing (asset transformation).** The intermediary **creates the assets savers want** — safe, liquid, small — **out of the assets borrowers issue** — risky, illiquid, large. Plus **diversification**.

> [!note] The diversification result is already computed elsewhere
> **[[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] computed $\sigma/\sqrt{n}$ and the correlation formula $\sigma\sqrt{(1+\rho)/2}$** — and [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]] derived the same expression for bank mergers. **Not re-derived here.** The institutional point is that **a bank *sells* that service** to savers who could not achieve it individually.

**3. ⚠️ Asymmetric information — the one that carries the subject.**

| | when | problem |
|---|---|---|
| **adverse selection** | **before** the transaction | the borrowers most eager to borrow are the worst risks |
| **moral hazard** | **after** the transaction | the borrower has an incentive to take risks the lender would not want |

**Intermediaries specialise in screening (adverse selection) and monitoring (moral hazard).** **[[06 - Asymmetric Information and Financial Structure|Ch. 06]] develops this into a theory of financial structure**, and it is the analytical spine of the whole subject.

### 4. What money is

$$\textbf{money} = \text{anything generally accepted in payment for goods and services or repayment of debts}$$

> [!warning] Money is not wealth and not income
> **Wealth** is all assets; **income** is a flow per period. **Money is a *stock*, and a narrow one.** *(Mishkin is careful about this and it is the most common confusion in the subject — "he has a lot of money" almost always means wealth.)*

| function | |
|---|---|
| **medium of exchange** | eliminates the **double coincidence of wants**, lowering transaction costs |
| **unit of account** | reduces the number of prices that must be quoted |
| **store of value** | shared with every other asset — and money is a **poor** one under inflation |

> [!note] The unit-of-account saving, computed
> **With $N$ goods a barter economy needs $N(N-1)/2$ relative prices; with money it needs $N$.**
>
> | goods | barter prices | with money | saving |
> |---|---|---|---|
> | 10 | 45 | 10 | 4× |
> | 100 | 4 950 | 100 | 50× |
> | **1 000** | **499 500** | **1 000** | **500×** |
>
> **Mishkin makes the point without the arithmetic**, and the arithmetic is what shows the saving grows with $N$ rather than being a fixed convenience.

> [!note] Only the medium-of-exchange function is unique to money
> **Which is why *liquidity* orders the aggregates in §5** — and it is the same conclusion [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] reached. **The medium-of-exchange function is also what makes specialisation possible**, so money is what lets [[Macroeconomics & Microeconomics/contents/01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|comparative advantage]] actually be realised.

### 5. The monetary aggregates

*(Verified — Mishkin's Table 1, Federal Reserve H.6, 3 July 2017, \$bn:)*

| | |
|---|---|
| currency | 1 481.5 |
| traveler's checks | 2.0 |
| demand deposits | 1 501.5 |
| other checkable deposits | 574.8 |
| **TOTAL M1** | **3 559.8** ✓ |
| small-denomination time deposits | 357.7 |
| savings deposits and MMDAs | 8 923.9 |
| money-market mutual fund shares (retail) | 673.7 |
| **TOTAL M2** | **13 515.1** ✓ |

**The aggregates are ordered by liquidity**: M1 is what can be spent immediately; M2 adds assets convertible quickly and cheaply.

> [!warning] Most "money" is bank deposits, not currency
> *(Computed: currency is **41.6% of M1** and only **11.0% of M2**; M1 is **26.3% of M2**.)*
>
> **Currency is about a ninth of M2. So the money supply is mostly created by *banks*** — which is exactly what [[08 - Central Banks and the Money Supply Process|ch. 08]]'s money supply process is about, and why [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s money multiplier matters at all.

### 6. ⚠️ Which M? — and why it is not academic

**Mishkin's point: if the aggregates do not move together, the choice matters for policy.** *(Here is why, quantitatively — feeding each into [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s quantity theory, $\text{inflation}=\%\Delta M-\%\Delta Y$ with real growth at 3%:)*

| M1 growth | M2 growth | inflation via **M1** | via **M2** | **gap** |
|---|---|---|---|---|
| 6% | 6% | 3% | 3% | 0 |
| 8% | 5% | 5% | 2% | **+3 pts** |
| **12%** | **4%** | **9%** | **1%** | **+8 pts** |
| 2% | 7% | −1% | 4% | **−5 pts** |

> [!warning] The same data gives inflation forecasts 8 points apart
> **That is not a measurement quibble.** **It is why the Fed largely abandoned monetary targeting in the 1980s–90s**: financial innovation — money-market funds, sweep accounts — kept moving assets across the M1/M2 boundary, **so the aggregates stopped being comparable over time.**
>
> **⚠️ And the deeper point recurs throughout this vault: the boundary of a measure is a judgement, and any policy built on it inherits that judgement.** [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]] said it about GDP and the CPI; [[Macroeconomics & Microeconomics/contents/11 - Unemployment|ch. 11]] said it about the unemployment rate; **here it is about money itself.**

## ✏️ Exercises

**1. (The financial system.)** (a) What do financial markets do and why does it matter? (b) Distinguish the four structural cuts. (c) Why do secondary markets matter if the issuer gets nothing?

> [!example]- Solution
> **(a) They channel funds from savers to borrowers, and it matters because those are different people.**
>
> **Someone with surplus funds and someone with a productive investment opportunity are usually not the same person.** Without a mechanism connecting them, **the saving sits idle and the project is not built** — so the financial system raises economic efficiency directly.
>
> **This is the institutional content of [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s loanable-funds market.** That chapter drew supply and demand curves and computed crowding out; **this subject asks what actually moves the money, and §3 shows the answer is mostly *not* the securities markets.**
>
> **(b) Debt/equity, primary/secondary, exchange/OTC, money/capital.**
>
> | cut | distinction | why it matters |
> |---|---|---|
> | **debt vs equity** | fixed claim vs **residual** claim | equity holders are paid **last**, so they demand more — and [[06 - Asymmetric Information and Financial Structure\|ch. 06]] explains why debt dominates |
> | **primary vs secondary** | new issue vs existing securities | only the primary market raises funds for the issuer |
> | **exchange vs OTC** | one location vs many dealers | affects liquidity and price transparency |
> | **money vs capital** | maturity under vs over one year | money-market instruments are **more liquid and less price-volatile** |
>
> **The money/capital distinction connects directly to [[Commercial Banking/contents/07 - The Investment Portfolio|Commercial Banking ch. 07]]**, which computed that a bank's securities portfolio **gives up 3.75 percentage points of yield** — it is held for liquidity and pledging, not return.
>
> **(c) Because they make the primary market work.**
>
> **Two reasons, both about the primary market:**
> 1. **Liquidity** — a security you can resell is easier to sell in the first place, so secondary trading raises the price the issuer can get;
> 2. **Price discovery** — the secondary price *determines* the terms on which new funds can be raised.
>
> **So a secondary market is not a sideshow to real finance**; it is the reason the primary market functions. *(This also explains why companies care about their share price even though they receive nothing when it trades — it sets the cost of any future issue.)*

**2. (Hard — intermediation.)** (a) Why does indirect finance dominate? (b) Which reason carries the subject? (c) What is already computed elsewhere?

> [!example]- Solution
> **(a) Transaction costs, risk sharing, and asymmetric information.**
>
> **1. Transaction costs — economies of scale.** *(Illustrated: a \$500 contract costs \$500 each for an individual and a few dollars each for a bank writing thousands — the same document.)* **Intermediaries also develop expertise that lowers costs further**, which individuals cannot amortise.
>
> **2. Risk sharing / asset transformation.** The intermediary **creates the assets savers want out of the assets borrowers issue** — turning risky, illiquid, large claims into safe, liquid, small ones — and **diversifies**.
>
> **3. Asymmetric information.** Borrowers know more about their own prospects than lenders do.
>
> **(b) Asymmetric information — and it is the analytical spine of the whole subject.**
>
> | | timing | problem |
> |---|---|---|
> | **adverse selection** | **before** the deal | the most eager borrowers are the worst risks — so a lender who cannot tell them apart may not lend at all |
> | **moral hazard** | **after** the deal | the borrower has an incentive to take risks the lender would not accept |
>
> **Intermediaries exist because they specialise in *screening* (adverse selection) and *monitoring* (moral hazard)** — activities with large fixed costs and no natural market, since information produced about a borrower is easily copied.
>
> **⚠️ And this vault has already computed one instance.** **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|Commercial Banking ch. 11]] modelled a lender whose expected return is *humped* — peaking at an 18% loan rate, so beyond it charging more earns less, because the rate itself induces default.** That is Stiglitz–Weiss credit rationing, **and it is adverse selection and moral hazard doing exactly what (b) describes.** **[[06 - Asymmetric Information and Financial Structure|Ch. 06]] here supplies the theory that computation was an instance of.**
>
> **(c) Diversification, present value, and the credit-rationing curve.**
>
> **[[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] computed $\sigma/\sqrt{n}$ and $\sigma\sqrt{(1+\rho)/2}$**; **[[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]] derived the same formula for bank mergers**; **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]] computed the credit-rationing curve.**
>
> **None of it is re-derived here** — the recorded boundary says this subject supplies the *institutional* reasoning and cross-links the computations. **The point that belongs here is that a bank *sells* diversification as a service** to savers who cannot achieve it individually.

**3. (Money.)** (a) Define money and distinguish it from wealth and income. (b) What do the three functions do? (c) Verify the aggregates and explain why "which M" matters.

> [!example]- Solution
> **(a) Anything generally accepted in payment — a narrow stock.**
>
> | | |
> |---|---|
> | **money** | a **stock** of the things accepted in payment |
> | **wealth** | a **stock** of *all* assets |
> | **income** | a **flow** per period |
>
> **"He has a lot of money" almost always means wealth**, and the confusion matters because the quantity theory ([[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]) is about the narrow stock, not about wealth.
>
> **(b) Medium of exchange, unit of account, store of value — and only the first is unique.**
>
> **Medium of exchange** eliminates the **double coincidence of wants** and so lowers transaction costs. **This is what makes specialisation possible**, so money is what lets [[Macroeconomics & Microeconomics/contents/01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|comparative advantage]] be realised rather than remaining a theoretical gain.
>
> **Unit of account** reduces the number of prices. *(Computed: $N$ goods need $N(N-1)/2$ relative prices under barter and $N$ with money — **499,500 versus 1,000** at a thousand goods, a **500× saving**, and the ratio grows with $N$.)*
>
> **Store of value** is shared with every asset, and **money is a poor one under inflation** — which is [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s inflation-tax computation, where revenue peaks at 100% inflation because people stop holding money.
>
> **Because only the first function is unique, *liquidity* is what orders the aggregates.**
>
> **(c) Both verify, and the choice changes inflation forecasts by 8 points.**
>
> *(Verified against Mishkin's Table 1: **M1 = 3,559.8** and **M2 = 13,515.1**, both summing exactly.)*
>
> *(Computed: currency is **41.6% of M1** and **11.0% of M2**.)* **⚠️ So most money is bank deposits** — which is why [[08 - Central Banks and the Money Supply Process|ch. 08]]'s money supply process exists as a topic at all, and why the central bank's control is indirect.
>
> **And the choice of aggregate is consequential.** *(Computed by feeding each into the quantity theory: M1 growing at 12% while M2 grows at 4% gives inflation forecasts of **9% and 1% — eight points apart from the same economy**.)*
>
> **That is why the Fed largely abandoned monetary targeting.** **Financial innovation — money-market funds, sweep accounts — kept moving assets across the M1/M2 boundary**, so a given aggregate stopped meaning the same thing over time. **The series broke, not the theory.**
>
> **⚠️ And the general lesson recurs across this vault: the boundary of a measure is a judgement, and policy built on it inherits that judgement.** [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living|Macro/Micro ch. 08]] made it about GDP and the CPI (the substitution bias), [[Macroeconomics & Microeconomics/contents/11 - Unemployment|ch. 11]] about the unemployment rate (discouraged workers). **Here it is about money itself — and this is the case where the measurement problem actually killed a policy regime.**

## 📝 Summary

- **Financial markets channel funds from savers to borrowers**, and it matters because they are different people — **the institutional content of [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s loanable-funds market.**
- **Direct finance** sells securities to lenders; **indirect finance** goes through an intermediary — **and indirect dominates everywhere.**
- **Four structural cuts**: debt/equity *(equity is a **residual** claim)*, primary/secondary, exchange/OTC, money/capital.
- **Secondary markets matter although the issuer gets nothing** — they make securities **liquid** and they **set the price** at which new funds can be raised.
- **Money-market instruments are a liquidity buffer, not an investment** — [[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]] computed the **3.75-point** yield give-up.
- **Intermediaries dominate for three reasons**: **transaction costs** (economies of scale in contracting), **risk sharing** (asset transformation and diversification), and **⚠️ asymmetric information**.
- **⚠️ Asymmetric information is the one that carries the subject** — **adverse selection *before*** the deal, **moral hazard *after***. Intermediaries specialise in screening and monitoring.
- **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]] already computed an instance** — the humped return curve peaking at 18%, where charging more earns less. **[[06 - Asymmetric Information and Financial Structure|Ch. 06]] supplies the theory it was an instance of.**
- **Money is a narrow *stock*** — not wealth (all assets) and not income (a flow).
- **Three functions, and only the medium-of-exchange one is unique to money** — which is why **liquidity** orders the aggregates.
- **The unit-of-account saving grows with $N$** *(computed: **499,500 barter prices versus 1,000** at a thousand goods — a **500×** saving)*.
- **Aggregates verified**: **M1 = 3,559.8**, **M2 = 13,515.1** ✓.
- **⚠️ Most money is bank deposits** *(computed: currency is **41.6% of M1** but only **11.0% of M2**)* — which is why [[08 - Central Banks and the Money Supply Process|ch. 08]] exists.
- **⚠️ "Which M" changes inflation forecasts by 8 percentage points from the same data** *(computed via the quantity theory)* — **and that is why the Fed abandoned monetary targeting**, because financial innovation kept moving assets across the boundary.
- **The boundary of a measure is a judgement, and policy inherits it** — GDP, the CPI, the unemployment rate, and now money.

## ⚠️ Important Notes

1. **The financial system's function is *channelling funds*.** Everything else is mechanism.
2. **Equity is a residual claim** — paid last, which is why it is expensive and why [[06 - Asymmetric Information and Financial Structure|ch. 06]] finds debt dominates.
3. **Only the primary market raises funds.** Secondary trading gives the issuer nothing directly.
4. **⚠️ Secondary markets still determine the issuer's cost of capital** — which is why firms care about the share price.
5. **Short maturity ⇒ more liquid and less price-volatile.** That is why banks hold money-market instruments.
6. **⚠️ Indirect finance dominates**, and any theory of finance must explain why.
7. **⚠️ Adverse selection is *before*, moral hazard is *after*.** Getting the timing right is half of using them correctly.
8. **Information about a borrower is easily copied**, which is why producing it has no natural market and intermediaries do it instead.
9. **Money ≠ wealth ≠ income.** Money is a narrow stock.
10. **Only the medium-of-exchange function is unique to money.**
11. **⚠️ Liquidity is what orders M1 and M2** — the aggregates are a liquidity ranking, not a list.
12. **⚠️ Most money is bank deposits, not currency.** Central-bank control is therefore indirect.
13. **⚠️ Which aggregate you use changes the answer** — up to 8 percentage points of inflation here.
14. **Financial innovation breaks monetary aggregates over time.** A series can stop meaning what it meant.
15. **⚠️ The boundary of a measure is a judgement** — the vault's fourth instance, and the one that killed a policy regime.

> [!warning] Gaps in the source material
> **Mishkin's prose extracts cleanly and the outline located both chapters precisely** *(PDF pp. 73–113 for chs. 2–3)*.
>
> **⚠️ THE PARENTHESIS FAULT applies to displayed equations** — see [[00-Index]]. **This chapter has almost no displayed maths**, so the exposure is minimal; **the arithmetic here is all inline and extracts correctly.**
>
> **⚠️ Table 1 (the monetary aggregates) survived extraction completely** — all eight lines with their values, **and both totals sum exactly.** *(This is the pattern the vault has now confirmed across three subjects: **graphical exhibits are lost; numeric tables set as text survive.** Verify by summation before trusting.)*
>
> **Every figure is lost**, including the money-supply time series and the chart comparing M1 and M2 growth rates — **the latter is the figure §6's argument rests on**, so the divergence is illustrated with constructed growth rates rather than the book's data.
>
> **No erratum.** Both aggregate totals reproduce exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §6 is the chapter's main addition.** **Mishkin observes that if M1 and M2 do not move together the choice of aggregate matters, and stops there.** Feeding each into [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s quantity theory shows the same economy giving **inflation forecasts eight points apart** — which turns an observation into a reason, and explains why monetary targeting was abandoned rather than merely noting that it was.
> - **§4's unit-of-account computation** — $N(N-1)/2$ barter prices against $N$ with money, a **500× saving at a thousand goods** — is mine. **Mishkin states the function without quantifying it**, and the arithmetic shows the benefit *grows* with the number of goods rather than being a fixed convenience.
> - **§5's proportions** (currency at **41.6% of M1** and **11.0% of M2**) are computed to make the point that **most money is bank deposits**, which is the motivation for [[08 - Central Banks and the Money Supply Process|ch. 08]].
> - **§3's scale illustration of contracting costs** is mine; Mishkin argues economies of scale verbally.
> - **The cross-links are the chapter's other addition**, and they implement the boundary recorded in [[00-Index]]: **the diversification result belongs to [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] and [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|CB ch. 02]]**, and **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]]'s humped return curve is a computed instance of the adverse selection and moral hazard this chapter introduces.** *(Naming that connection now is what makes [[06 - Asymmetric Information and Financial Structure|ch. 06]] a theory chapter rather than a repetition.)*
> - **The identification of "which M" as the vault's fourth measurement-boundary case** — after GDP, the CPI and the unemployment rate — **and the observation that this is the one where the measurement problem actually killed a policy regime**, is my synthesis.
>
> **Deliberately compressed.** **Mishkin ch. 2's catalogues of money-market and capital-market instruments** (T-bills, negotiable CDs, commercial paper, repos, fed funds; stocks, mortgages, corporate bonds, government securities) are compressed to the maturity distinction — they are reference lists, largely US-specific, and **[[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]] already surveys the ones a bank holds.** **The internationalisation section** (Eurobonds, Eurocurrencies, world stock markets) is noted; **[[10 - Foreign Exchange and the International Financial System|ch. 10]] owns international finance.** **The regulation-of-the-financial-system section** is deferred to [[06 - Asymmetric Information and Financial Structure|ch. 06]], which has the asymmetric-information apparatus that makes it intelligible. **Ch. 3's history of payment systems** (commodity money, fiat, cheques, electronic payment, e-money) is compressed to the functions; **the "are we heading for a cashless society" discussion** is an application. **The measurement-revision discussion** (how the Fed revises the aggregates) supports §6's point and is represented by it.

**Previous:** [[00-Index]] · **Next:** [[02 - The Meaning of Interest Rates]]
