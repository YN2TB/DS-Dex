---
subject: Monetary and Financial Theories
chapter: 10
tags: [ds, economics, exchange-rates, purchasing-power-parity, interest-parity, trilemma, balance-of-payments, fixed-exchange-rates]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 18–19"
---

# Foreign Exchange and the International Financial System

**An exchange rate is a *price* in the long run and an *asset price* in the short run — and the chapter is organised around that split.** **[[07 - Financial Crises|Ch. 07]] §6 already supplied the result that matters most here: currency mismatch is debt deflation in a second currency, so devaluation is contractionary for an emerging economy.**

**Four results.**

**§2 — ⚠️ all six rows of the Big Mac table verified.** *(All six implied PPP rates reproduce exactly; four of six index values do, and **the other two are fully explained by rounding in the printed exchange rate** — Japan's index requires 0.008434, which rounds to the printed 0.0084.)*

**§4 — ⚠️ a FIFTH dropped cross term, and this time Mishkin computes it himself.** *(Verified: 7.12% exact against 7% approximate.)* **It is algebraically identical to [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation.**

**§5 — ⚠️ THE TRILEMMA IS ONE LINE FROM THE INTEREST PARITY CONDITION.** **Mishkin gives both and never connects them.** *(A credible fixed rate makes $E^e_{t+1}=E_t$, so parity collapses to $i_D=i_F$ **exactly** — which is the denial of monetary independence.)* **⇒ it is an algebraic identity, not a list of trade-offs.**

**§6 — a sterilized intervention is a *nothing*.** **If the monetary base is unchanged, parity pins the exchange rate exactly where it was.** **"The central bank intervened to support the currency" is either a monetary policy change in disguise or it is nothing — and the difference is invisible from outside.**

## 📘 Main Knowledge

### 1. Purchasing power parity — the long run

$$\textbf{PPP}=\text{a basket of goods costs the same in both countries once converted}$$

*(Mishkin's example, verified: a basket costs \$100 in the US and 10,000 yen in Japan ⇒ the PPP rate is **100 yen per dollar**. Check: \$100 × 100 = 10,000 yen, and 10,000 × \$0.01 = \$100.)*

**Now Japan's price level rises 10% and the US is unchanged:** **the Japanese basket costs 11,000 yen, so the PPP rate becomes 110 yen/\$ — the dollar appreciates 10%** ✓.

> [!warning] ⚠️ The key insight
> **If one country's price level rises relative to another's by $x\%$, its currency depreciates by $x\%$.**
>
> **This is [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s quantity theory with an open economy attached: money growth → inflation → depreciation.** **⇒ PPP is what makes the exchange rate a *monetary* variable in the long run.**

**The real exchange rate** = the price of domestic goods relative to foreign goods in a common currency. *(Verified: a \$50 New York basket against a Tokyo basket costing 7,500 yen at 100 yen/\$ = \$75 gives **0.6667**, the book's 0.66.)*

> [!note] Below 1.0 means domestic goods are cheaper
> **PPP predicts the real exchange rate is always 1.0 in the long run**, **so any deviation from 1 measures how far PPP is from holding.** *(Mishkin: a low real dollar rate is "why New York is overwhelmed by so many foreign tourists going on shopping sprees.")*

### 2. ⚠️ The Big Mac index — all six rows verified

**The Economist's "lighthearted guide to whether currencies are at their correct level".** **A US Big Mac cost \$4.93 in January 2017.**

$$\text{implied PPP rate}=\frac{\$4.93}{\text{local price}}\qquad\qquad\text{index}=\frac{\text{actual}}{\text{implied}}-1$$

| country | local price | actual | **implied PPP** | book | **index** | book |
|---|---|---|---|---|---|---|
| **Japan** | 370 yen | 0.0084 | **0.013324** ✓ | 0.0133 | −36.96% | −36.7 |
| **Venezuela** | 132 bolivars | 0.0050 | **0.037348** ✓ | 0.0373 | −86.61% | −86.5 |
| China | 17.60 yuan | 0.1525 | **0.280114** ✓ | 0.2801 | **−45.56%** ✓ | −45.6 |
| **Switzerland** | 6.50 francs | 0.9913 | **0.758462** ✓ | 0.7585 | **+30.70%** ✓ | +30.7 |
| Canada | 5.84 C\$ | 0.7096 | **0.844178** ✓ | 0.8442 | **−15.94%** ✓ | −15.9 |
| Euro area | 3.72 euros | 1.0750 | **1.325269** ✓ | 1.3253 | **−18.88%** ✓ | −18.9 |

> [!note] All six implied rates reproduce exactly; the two index gaps are rounding
> *(Diagnosed: **Japan's index requires an actual rate of 0.008434, which rounds to the printed 0.0084; Venezuela's requires 0.005042, which rounds to 0.0050.**)* **Column 3 is printed to four decimals and that is enough to account for both gaps.** **Not filed** *(rule 4: rule out rounding and conventions first)*.

*(And Mishkin's two prose cross-checks are exact: **6.50 × 0.9913 = \$6.44**, which is **30.7%** above \$4.93; and **132 × 0.0050 = \$0.66**, the "66 cents".)*

> [!warning] ⚠️ What the table actually shows — read columns 2 and 3 together
> **Japan has the highest local price (370) and the lowest exchange rate (0.0084); the euro area has the lowest local price (3.72) and the highest rate (1.0750).** **That inverse relationship *is* PPP working.**
>
> **The deviations are what the index measures** — Switzerland **+30.7%** (overvalued; an expensive place to visit) down to Venezuela **−86.5%** (undervalued; a 66-cent Big Mac).
>
> **⚠️ And the index is a joke that works *because of* its own flaw.** **A Big Mac is the purest possible nontraded good — ship it and you get food poisoning — so it is exactly the case where PPP should fail worst.** **That the ordering still comes out right is the evidence.**

### 3. How badly does PPP do? — in Mishkin's own numbers

| period | relative price move | **PPP predicts** | **actual** | verdict |
|---|---|---|---|---|
| **1973–2017** | UK prices **+69%** vs US | dollar **+69%** | dollar **+95%** | **right sign, 26 pts off** |
| **1985–1987** | UK prices **rose** vs US | dollar appreciates | dollar **−40%** | **⚠️ WRONG SIGN** |

> [!warning] ⚠️ PPP is directionally right over 44 years and wrong in sign over 3
> **It is not a bad theory; it is a *long-run* theory, and using it at a short horizon is a category error rather than an inaccuracy.**

**Three reasons it fails in the short run — and all three are about the *goods*, not the currency:**

1. **Many goods are nontraded** — housing, land, restaurant meals, haircuts, golf lessons. **Their prices enter the price level but not the exchange rate.**
2. **Similar goods are not identical** — a Toyota is not a Chevrolet, so their prices need not equalise.
3. **Trade barriers** — tariffs and quotas. *(US sugar, Japanese rice.)*

> [!note] ⚠️ PPP fails for the same reason the Big Mac index works
> **The basket contains things that cannot move.**

**Four long-run factors** *(Summary Table 2 — one mechanism: anything raising relative demand for domestic goods appreciates the currency)*:

| factor ↑ | exchange rate |
|---|---|
| **domestic price level** | **depreciates** |
| trade barriers | appreciates |
| **import demand** | **depreciates** |
| export demand | appreciates |
| **productivity** | **appreciates** |

### 4. ⚠️ Interest parity — the short run, and a fifth cross term

**In the short run an exchange rate is an *asset price*, so [[03 - The Behavior of Interest Rates|ch. 03]]'s theory of portfolio choice applies.** **The relative expected return on domestic assets is $i_D-i_F+(E^e_{t+1}-E_t)/E_t$, and with capital mobility and perfect substitutes it must be zero:**

$$\boxed{\ i_D=i_F-\frac{E^e_{t+1}-E_t}{E_t}\ }$$

**The domestic interest rate equals the foreign rate *plus the expected appreciation of the foreign currency*.**

> [!warning] ⚠️ A higher domestic interest rate is not a free lunch
> *(Mishkin's example: $i_D=5\%$ against $i_F=3\%$ requires the foreign currency to be expected to appreciate **2%** — equivalently, the dollar to depreciate 2%.)* **The interest advantage is *compensation* for an expected depreciation, and in equilibrium it is exactly offset.**

> [!warning] ⚠️ A fifth dropped cross term — and this time Mishkin computes it himself
> *(Verified against his footnote 1:)*
> $$\text{exact}=i_D\!\left(\frac{E^e}{E}\right)+\frac{E^e-E}{E}=0.04\times1.03+0.03=\mathbf{7.12\%}$$
> $$\text{approximate}=i_D+\frac{E^e-E}{E}=0.04+0.03=\mathbf{7.00\%}$$
> **The dropped term is $i_D\times$(expected appreciation) $=0.12$ points.**
>
> **⚠️ This is algebraically identical to [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation** — $(1+i)=(1+r)(1+\pi^e)$ there, $(1+i_D)(E^e/E)$ here. **Same move, same neglected product, same domain of validity.** *(The others: duration/convexity, the arithmetic-versus-geometric average in [[04 - The Risk and Term Structure of Interest Rates|ch. 04]], and [[07 - Financial Crises|ch. 07]]'s debt deflation.)*
>
> **⚠️ And note that this is the *only* one of the five where the source computes its own error.** **The error grows with both factors, so it is worst for a high-interest currency expected to move a lot — exactly [[07 - Financial Crises|ch. 07]]'s emerging-market case.**

**Solving parity for the exchange rate:**

$$E_t=\frac{E^e_{t+1}}{i_F-i_D+1}$$

| $i_D$ | $i_F$ | $E_t$ *(for $E^e=100$)* | vs baseline |
|---|---|---|---|
| **5%** | 3% | 102.04 | — |
| 6% | 3% | 103.09 | **+1.03%** |
| 7% | 3% | 104.17 | +2.08% |
| 5% | 8% | 97.09 | **−4.85%** |

> [!note] The response is about one-for-one, not amplified
> **A one-point rise in the domestic rate appreciates the currency by roughly 1%.** **Unlike [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s Gordon model — whose denominator was a *small difference* — here the denominator is close to 1, so nothing explodes.**

> [!warning] ⚠️ But look at the numerator
> **$E_t$ is proportional to $E^e_{t+1}$, the expected future rate, which nobody observes.** **So today's exchange rate is almost entirely a statement about expectations.**
>
> **⇒ that is why [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s random walk applies to exchange rates — Mishkin says so in his own Global box** — **and why exchange rates are far more volatile than the slow-moving long-run fundamentals of §1.**

### 5. ⚠️ The trilemma, derived from interest parity

**Mishkin gives the *policy trilemma* as a triangle: a country cannot have all three of**

1. **free capital mobility**
2. **a fixed exchange rate**
3. **an independent monetary policy**

**— and must pick two.** **He presents it as a separate diagram.**

> [!warning] ⚠️ But it is one line from the equation he has just given
> $$\text{free capital mobility}\ \Rightarrow\ i_D=i_F-\frac{E^e_{t+1}-E_t}{E_t}$$
> $$\text{a CREDIBLE fixed rate}\ \Rightarrow\ E^e_{t+1}=E_t\ \Rightarrow\ \text{the last term is ZERO}$$
> $$\therefore\quad\boxed{\ i_D=i_F\ \text{exactly}\ }$$
>
> **And $i_D=i_F$ *is* the denial of (3).** **The domestic interest rate is not a policy choice; it is whatever the foreign one happens to be.**
>
> **⚠️ So the trilemma is not an empirical regularity or a list of trade-offs. It is an algebraic identity — two of the three assumptions *force* the third to fail.**

| option | country | gives up | keeps |
|---|---|---|---|
| **1** | **United States** | the fixed exchange rate | free capital + independent policy |
| **2** | **Hong Kong** | **independent monetary policy** | free capital + fixed rate |
| **3** | **China (1994–2005)** | **free capital mobility** | fixed rate + independent policy |

> [!note] ⚠️ Each corner is a chapter of this subject
> - **Option 1 is [[09 - Tools and Conduct of Monetary Policy|ch. 09]]**: an independent policy needs a floating rate, which is *why* a Taylor rule is even possible.
> - **Option 2 is §8's currency board and dollarization** — **and [[07 - Financial Crises|ch. 07]]'s Argentina is what happens when you take option 2 and then need option 3.**
> - **Option 3 is capital controls, and China's \$4 trillion of reserves is the price of holding that corner.**

> [!warning] ⚠️ The honest caveat — the derivation assumes the peg is CREDIBLE
> **It needs $E^e=E$.** **When credibility goes, $E^e$ moves away from $E$ and the parity gap reopens as a speculative attack** — **which is [[07 - Financial Crises|ch. 07]]'s stage two, and the September 1992 sterling crisis.** **The trilemma binds hardest exactly when the peg is doubted.**

### 6. ⚠️ Intervention — and why a sterilized one is a nothing

**A central bank buying its own currency *sells* foreign assets. Both sides of its balance sheet fall by the same amount:**

| assets | liabilities |
|---|---|
| foreign assets (international reserves) **−\$1bn** | currency in circulation (or reserves) **−\$1bn** |

> [!note] An unsterilized FX intervention is an open market operation under another name
> **It changes the monetary base one-for-one** *([[08 - Central Banks and the Money Supply Process|ch. 08]]'s $MB=C+R$; nothing new is needed)*.
>
> - **buy domestic currency ⇒ reserves down, base down ⇒ currency appreciates**
> - **sell domestic currency ⇒ reserves up, base up ⇒ currency depreciates**

**A *sterilized* intervention is the same trade plus an offsetting open market operation, so the monetary base is unchanged.**

> [!warning] ⚠️ And then nothing happens
> **If the base is unchanged, $i_D$ is unchanged and $E^e$ is unchanged — so interest parity pins $E_t$ exactly where it was.** **The central bank has swapped the *composition* of its assets and moved no price at all.**
>
> **Mishkin's footnote 2 is careful and worth keeping.** **A *portfolio balance effect* is possible in principle, but "empirical evidence has not revealed this portfolio balance effect to be significant."** **What *can* work is signalling — and in his own words, "the future change in monetary policy, *not the sterilized intervention*, is the source of the exchange rate effect."**
>
> **⚠️ ⇒ "the central bank intervened to support the currency" is either a monetary policy change in disguise or it is nothing.** **There is no third possibility, and the distinction is invisible from outside. *Ask whether it was sterilized.***

### 7. The balance of payments — one quantity with two names

*(US 2016, \$bn — verified:)*

| | |
|---|---|
| trade balance | **−505** |
| net investment income | **+173** |
| transfers | **−120** |
| **CURRENT ACCOUNT** | **−452** ✓ |
| **financial account** | **+452** *(official −378 + statistical discrepancy 74)* |
| **SUM** | **0** |

> [!warning] ⚠️ The identity is exact by construction
> **A current account deficit *is* a capital inflow.** **These are not two facts that happen to offset — they are one fact described twice.**
>
> **⇒ "the US borrows from abroad to fund its trade deficit" is not a causal claim but a restatement.** **The economics lies entirely in *which one drives the other*, and the identity is silent on that.**
>
> **And [[07 - Financial Crises|ch. 07]]'s sudden stop is this identity turning hostile.** **When the financing stops, the current account *must* close** — its Table 1 showed Thailand's going **−8.0% → +12.5%** while GDP fell **7.6%**. **The "improvement" in the external balance *is* the damage.**

> [!note] ⚠️ And a measurement boundary, again
> **The statistical discrepancy is \$74bn, which Mishkin includes in the financial account because "many experts believe it is primarily the result of large hidden capital flows."** **That is a judgement — and it is 16% of the reported current account deficit.** *([[01 - The Financial System and What Money Is|Ch. 01]]'s result once more.)*

### 8. Fixed rates, China, and currency boards

> [!warning] ⚠️ The asymmetry is the whole story of fixed-rate collapse
> **To defend an *undervalued* currency the central bank sells its own currency and buys foreign assets — accumulating reserves without limit, because it can print.**
> **To defend an *overvalued* one it must buy its own currency with reserves — and reserves are finite.**
>
> **⇒ a country defending a strong currency can hold out indefinitely; one defending a weak currency runs out.** **Speculators know which side they are on** — [[07 - Financial Crises|ch. 07]]'s "almost sure-thing bet", and the September 1992 sterling crisis.

**China — the undervalued case.** **Pegged at 12 cents per yuan from 1994. Rapid productivity growth and below-US inflation raised the yuan's long-run value** *(§3's productivity factor)*, **so the peg became increasingly undervalued.**

- **Reserves reached \$4 trillion by 2014, falling to \$3 trillion by 2017.**
- **July 2005: the peg was loosened, the yuan revalued 2.1%, and the reference switched from the dollar to a basket.**

> [!warning] ⚠️ Note which corner of the trilemma that is
> **China kept the fixed rate *and* an independent policy, so it had to give up capital mobility — and Mishkin says exactly this: "because the Chinese authorities created substantial roadblocks to capital mobility, they were able to sterilize most of their exchange rate interventions."** **Sterilization at that scale is only possible *behind capital controls*.**
>
> **And it still leaked**: the interventions "led to a rapidly growing money supply that produced inflationary pressures." **⇒ the trilemma was binding even with the controls.**

**Currency boards and dollarization — option 2 taken to the limit.** **A currency board backs the domestic currency 100% with a foreign one and commits to convert on demand.** **Advantages over a plain peg: transparency, and a stronger commitment** *([[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s time-inconsistency problem solved by removing the instrument entirely)*.

> [!warning] ⚠️ But it also removes the lender of last resort — and that is what killed Argentina's
> **With no ability to create money, the central bank could not stop [[07 - Financial Crises|ch. 07]]'s stage-two bank panic; and with no monetary policy it could not fight the recession that began in 1998.**
>
> **Dollarization goes further: a currency board can be abandoned, an adopted currency cannot easily be.** **⚠️ The commitment is stronger precisely *because* the exit is harder — the same logic as [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s nominal anchor, and it carries the same cost.**

## ✏️ Exercises

**1. (PPP.)** (a) Work Mishkin's example. (b) What is the real exchange rate? (c) How well does PPP do, and why?

> [!example]- Solution
> **(a) 100 yen per dollar, rising to 110 when Japanese prices rise 10%.**
>
> **A basket costs \$100 in the US and 10,000 yen in Japan ⇒ the PPP rate is 10,000/100 = **100 yen/\$**.** *(Check both ways: \$100 × 100 = 10,000 yen; 10,000 × \$0.01 = \$100.)*
>
> **If Japan's price level rises 10%, the Japanese basket costs 11,000 yen and the PPP rate becomes 110 yen/\$ — the dollar appreciates 10%** ✓.
>
> **⚠️ The general statement: if a country's price level rises relative to another's by $x\%$, its currency depreciates by $x\%$.**
>
> *(And this makes the exchange rate a **monetary** variable in the long run — [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s quantity theory with an open economy attached: money growth → inflation → depreciation.)*
>
> **(b) The price of domestic goods relative to foreign goods in one currency.**
>
> *(Verified: a \$50 New York basket against a Tokyo basket costing 7,500 yen at 100 yen/\$ = \$75 gives **0.6667**, the book's 0.66.)*
>
> **Below 1.0 means domestic goods are cheaper — the currency is undervalued in PPP terms.** **⚠️ PPP predicts the real exchange rate is always 1.0 in the long run, so *any deviation from 1 is a measure of PPP's failure*.** **That makes it the natural summary statistic**, and it is what the Big Mac index reports in percentage form.
>
> **(c) Right over decades, wrong in sign over years.**
>
> | period | PPP predicts | actual |
> |---|---|---|
> | **1973–2017** | dollar +69% | **+95%** — right sign, 26 pts off |
> | **1985–1987** | dollar appreciates | **−40%** — **wrong sign** |
>
> **⚠️ So it is a *long-run* theory, and using it at short horizons is a category error rather than an inaccuracy.**
>
> **Three reasons, all about the goods rather than the currency**: **many goods are nontraded** (housing, haircuts, restaurant meals — their prices enter the price level but not the exchange rate); **similar goods are not identical** (a Toyota is not a Chevrolet); **and trade barriers exist** (US sugar, Japanese rice).
>
> **⚠️ Which is the same reason the Big Mac index works: the basket contains things that cannot move.**

**2. (Hard — the Big Mac index.)** (a) Verify the table. (b) What does it show? (c) Why is a Big Mac a strange and yet good choice?

> [!example]- Solution
> **(a) All six implied rates exact; two index values differ by rounding.**
>
> **Implied PPP rate $=\$4.93/\text{local price}$; index $=\text{actual}/\text{implied}-1$.**
>
> | | implied | book | index | book |
> |---|---|---|---|---|
> | Japan | 0.013324 ✓ | 0.0133 | −36.96% | −36.7 |
> | Switzerland | 0.758462 ✓ | 0.7585 | **+30.70%** ✓ | +30.7 |
> | Canada | 0.844178 ✓ | 0.8442 | **−15.94%** ✓ | −15.9 |
> | Euro area | 1.325269 ✓ | 1.3253 | **−18.88%** ✓ | −18.9 |
>
> **⚠️ The two gaps are printed-rounding, not error.** *(Japan's index requires an actual rate of **0.008434**, which rounds to the printed 0.0084; Venezuela's requires **0.005042**, rounding to 0.0050.)* **Not filed** — rule 4 requires ruling out rounding first.
>
> *(And the two prose cross-checks are exact: **6.50 × 0.9913 = \$6.44**, 30.7% above \$4.93; **132 × 0.0050 = \$0.66**.)*
>
> **(b) That PPP holds in ordering and fails in level.**
>
> **Read columns 2 and 3 together: Japan has the *highest* local price (370 yen) and the *lowest* exchange rate (0.0084); the euro area the *lowest* price (3.72) and the *highest* rate (1.0750).** **⚠️ That inverse relationship is PPP working** — a currency in which things are expensive to buy is a currency that trades cheaply per unit.
>
> **The *deviations* are what the index reports**: Switzerland **+30.7%** overvalued, Venezuela **−86.5%** undervalued.
>
> **(c) It is the purest possible nontraded good, which is exactly why the result is informative.**
>
> **Ship a Big Mac and you get food poisoning.** **So arbitrage — the mechanism that is supposed to *enforce* the law of one price — cannot operate at all**, and this is the case where PPP should fail worst.
>
> **⚠️ That the ordering still comes out right is therefore stronger evidence than a tradable good would give.** **If PPP survives in the worst case, the long-run mechanism is not arbitrage in *that* good** — it is the general price level moving, which is §1's monetary story.
>
> *(The index is also honest about its own limits in a way most indicators are not: it is published as "lighthearted", and the deviations it reports are simultaneously the theory's failures and its most useful output — Switzerland really is expensive to visit.)*

**3. (Hard — interest parity.)** (a) State and interpret the condition. (b) What does Mishkin's footnote 1 show? (c) What determines today's exchange rate?

> [!example]- Solution
> **(a) $i_D=i_F-(E^e_{t+1}-E_t)/E_t$ — the interest advantage is compensation.**
>
> **An exchange rate is an asset price, so [[03 - The Behavior of Interest Rates|ch. 03]]'s portfolio choice applies.** **With free capital mobility and perfect substitutes, the relative expected return must be zero, which gives the condition.**
>
> **⚠️ Read it as: the domestic rate equals the foreign rate *plus the expected appreciation of the foreign currency*.** *(Mishkin's case: $i_D=5\%$ against $i_F=3\%$ requires the foreign currency to appreciate 2%, i.e. the dollar to depreciate 2%.)*
>
> **So a higher domestic interest rate is not a free lunch — it is exactly offset in expectation.** **A country cannot attract capital by paying more unless investors expect its currency to fall by the difference**, which is the same no-arbitrage logic as [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s expectations theory of the term structure, applied across currencies rather than across maturities.
>
> **(b) A fifth dropped cross term — and the only one he computes himself.**
>
> $$\text{exact}=i_D\!\left(\tfrac{E^e}{E}\right)+\tfrac{E^e-E}{E}=0.04(1.03)+0.03=\mathbf{7.12\%}$$
> $$\text{approximate}=0.04+0.03=\mathbf{7.00\%}$$
>
> **The dropped term is $i_D\times$(expected appreciation) = 0.12 points.**
>
> **⚠️ Algebraically identical to [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation** — $(1+i)=(1+r)(1+\pi^e)$ there, $(1+i_D)(E^e/E)$ here. **Same move, same neglected product.**
>
> **⚠️ And the contrast is instructive: this is the *fifth* such approximation in the subject and the *only* one where the source states its own error.** *(The others — the Fisher equation, duration, [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s arithmetic average, [[07 - Financial Crises|ch. 07]]'s debt deflation — are all stated without one, and ch. 07's turned out to straddle zero.)*
>
> **The error grows with both factors, so it is worst for a high-interest currency expected to move a lot — precisely [[07 - Financial Crises|ch. 07]]'s emerging-market case, where both are large.**
>
> **(c) Almost entirely the *expected future* rate.**
>
> $$E_t=\frac{E^e_{t+1}}{i_F-i_D+1}$$
>
> *(Computed: a one-point rise in $i_D$ appreciates the currency by about **1%** — **roughly one-for-one, not amplified**, because the denominator is close to 1. Unlike [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s Gordon model, whose denominator was a small *difference*, nothing explodes here.)*
>
> **⚠️ But $E_t$ is *proportional* to $E^e_{t+1}$, which nobody observes.** **So today's rate is overwhelmingly a statement about expectations, and the interest differential is a second-order adjustment to it.**
>
> **⇒ two consequences.** **First, [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s random walk applies to exchange rates** — Mishkin says so in his own Global box, by the same arbitrage argument: a predictable 1% weekly move would be a >50% annualised return. **Second, exchange rates are far more volatile than §1's slow-moving fundamentals**, because expectations can jump and price levels cannot.

**4. (Hard — the trilemma.)** (a) State it. (b) Derive it from §4. (c) What does the derivation add, and what does it assume?

> [!example]- Solution
> **(a) Free capital mobility, a fixed exchange rate, an independent monetary policy — pick two.**
>
> | option | country | gives up |
> |---|---|---|
> | 1 | **United States** | the fixed rate |
> | 2 | **Hong Kong** | **independent monetary policy** |
> | 3 | **China (1994–2005)** | **free capital mobility** |
>
> **(b) It is one line from interest parity.**
>
> $$\text{free capital mobility}\ \Rightarrow\ i_D=i_F-\frac{E^e_{t+1}-E_t}{E_t}$$
> $$\text{a credible fixed rate}\ \Rightarrow\ E^e_{t+1}=E_t\ \Rightarrow\ \text{last term}=0$$
> $$\therefore\ i_D=i_F\ \textbf{exactly}$$
>
> **And $i_D=i_F$ is precisely the denial of monetary independence — the domestic rate is not chosen, it is inherited.**
>
> **(c) It converts a trade-off into an identity — and it assumes credibility.**
>
> **⚠️ Mishkin presents the trilemma as a triangle diagram, several sections after giving the interest parity condition, and never connects them.** **Presented as a diagram it looks like an empirical regularity or a menu of policy trade-offs; derived, it is *algebra*.** **Two of the three assumptions do not merely make the third *difficult* — they make it false.**
>
> **That matters for how you argue about it.** **A country cannot "try harder" to hold all three, and a policy proposal that appears to achieve all three contains an error or a hidden capital control.**
>
> **⚠️ The assumption is that the peg is *credible*, so that $E^e=E$.** **When credibility goes, $E^e$ moves away from $E$, the parity gap reopens, and the required $i_D$ jumps** — **which is a speculative attack.** *([[07 - Financial Crises|Ch. 07]]'s stage two, and the September 1992 sterling crisis.)*
>
> **So the trilemma binds hardest exactly when the peg is doubted** — and this also explains [[07 - Financial Crises|ch. 07]]'s "rock and a hard place": **a government defending a doubted peg must raise $i_D$ enough to compensate for an expected devaluation, which is precisely the rate rise that destroys its banks.**
>
> *(And each corner is a chapter here: option 1 is [[09 - Tools and Conduct of Monetary Policy|ch. 09]] — an independent policy needs a floating rate, which is why a Taylor rule is possible at all; option 2 is §8's currency board; option 3 is capital controls, and China's \$4 trillion is what holding that corner cost.)*

**5. (Intervention and the balance of payments.)** (a) What does an unsterilized intervention do? (b) A sterilized one? (c) Explain the balance-of-payments identity.

> [!example]- Solution
> **(a) It changes the monetary base one-for-one.**
>
> **A central bank buying its own currency sells foreign assets, and both sides of its balance sheet fall by \$1bn** — international reserves on the asset side, currency or bank reserves on the liability side.
>
> **⚠️ So an unsterilized FX intervention *is* an open market operation wearing a different name.** *([[08 - Central Banks and the Money Supply Process|Ch. 08]]'s $MB=C+R$; nothing new is required.)*
>
> - **buy domestic currency ⇒ base falls ⇒ currency appreciates**
> - **sell domestic currency ⇒ base rises ⇒ currency depreciates**
>
> **(b) Nothing.**
>
> **A sterilized intervention adds an offsetting open market operation, so the base is unchanged.** **⚠️ But if the base is unchanged, $i_D$ is unchanged and $E^e$ is unchanged — and interest parity then pins $E_t$ exactly where it was.** **The central bank has changed the *composition* of its assets and moved no price.**
>
> **Mishkin's footnote 2 is scrupulous about the two escape routes and closes both.** **A *portfolio balance effect* could work in principle, but "empirical evidence has not revealed this portfolio balance effect to be significant."** **Signalling *can* work — but then, in his words, "the future change in monetary policy, **not the sterilized intervention**, is the source of the exchange rate effect."**
>
> **⚠️ ⇒ "the central bank intervened to support the currency" is either a monetary policy change in disguise or it is nothing.** **There is no third possibility, and the distinction is invisible from outside — so the question to ask is always *was it sterilized?***
>
> **(c) The two accounts sum to zero by construction.**
>
> | | \$bn |
> |---|---|
> | trade balance | −505 |
> | net investment income | +173 |
> | transfers | −120 |
> | **current account** | **−452** ✓ |
> | **financial account** | **+452** |
>
> **⚠️ A current account deficit *is* a capital inflow.** **They are not two facts that happen to offset — they are one fact described twice.**
>
> **⇒ "the US borrows from abroad to fund its trade deficit" is a restatement, not an explanation.** **The economics is entirely in which side drives the other, and the identity cannot tell you.**
>
> **And [[07 - Financial Crises|ch. 07]]'s sudden stop is this identity turning hostile: when the financing stops, the current account *must* close, and it closes through collapsing imports.** *(Thailand: **−8.0% → +12.5%** while GDP fell 7.6%. **The "improvement" in the external balance is the damage.**)*
>
> *(One caution: the **statistical discrepancy is \$74bn** and Mishkin folds it into the financial account because "many experts believe it is primarily the result of large hidden capital flows." **That is a judgement, and it is 16% of the reported current account deficit** — [[01 - The Financial System and What Money Is|ch. 01]]'s measurement-boundary result once again.)*

## 📝 Summary

- **An exchange rate is a *price* in the long run (PPP) and an *asset price* in the short run (interest parity).**
- **PPP verified**: a \$100 / 10,000-yen basket implies **100 yen/\$**, and a 10% Japanese price rise appreciates the dollar **10%**. **⇒ if a country's price level rises $x\%$ relative to another's, its currency depreciates $x\%$** — **the quantity theory with an open economy attached.**
- **Real exchange rate = domestic prices / foreign prices in one currency** *(verified: 50/75 = **0.6667**)*. **PPP predicts it equals 1.0, so deviations measure PPP's failure.**
- **⚠️ All six Big Mac implied rates reproduce exactly; four of six index values do, and the other two are explained by rounding in the printed exchange rate** *(Japan requires 0.008434, which rounds to 0.0084)*. **Not filed.**
- **⚠️ The table's content is the inverse ordering of columns 2 and 3 — that *is* PPP working** — while the deviations run from **Switzerland +30.7%** to **Venezuela −86.5%**.
- **⚠️ A Big Mac is the purest nontraded good, so it is where PPP should fail worst — which is why the ordering surviving is the evidence.**
- **⚠️ PPP is directionally right over 44 years (+69% predicted, +95% actual) and WRONG IN SIGN over 3 (1985–87: −40%).** **A long-run theory misused at short horizons is a category error, not an inaccuracy.**
- **Three reasons it fails short-run, all about the goods**: **nontraded goods**, non-identical goods, **trade barriers.**
- **⚠️ Interest parity: $i_D=i_F-(E^e_{t+1}-E_t)/E_t$** — **a higher domestic rate is compensation for an expected depreciation, not a free lunch.**
- **⚠️ FIFTH dropped cross term, and the only one the source computes itself** *(verified: **7.12%** exact against **7.00%** approximate)*. **Algebraically identical to [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation.**
- **$E_t=E^e_{t+1}/(i_F-i_D+1)$** — **the interest response is about one-for-one, not amplified**, but **⚠️ $E_t$ is proportional to the unobservable $E^e_{t+1}$**, which is why exchange rates follow a random walk and are far more volatile than fundamentals.
- **⚠️ THE TRILEMMA IS ONE LINE FROM INTEREST PARITY**: free capital mobility + a credible fixed rate ⇒ $i_D=i_F$ **exactly**, which is the denial of monetary independence. **⇒ an algebraic identity, not a menu of trade-offs.**
- **Each corner is a chapter**: option 1 = [[09 - Tools and Conduct of Monetary Policy|ch. 09]], option 2 = currency boards, option 3 = capital controls.
- **⚠️ The derivation assumes credibility. When the peg is doubted, $E^e$ separates from $E$ and the gap reopens as a speculative attack** — [[07 - Financial Crises|ch. 07]]'s stage two.
- **An unsterilized intervention is an open market operation under another name** — it moves the base one-for-one.
- **⚠️ A STERILIZED intervention is a nothing.** **Base unchanged ⇒ $i_D$ and $E^e$ unchanged ⇒ parity pins $E_t$ where it was.** **Mishkin closes both escape routes himself.**
- **⚠️ Balance of payments: −505 + 173 − 120 = −452, exactly offset by +452.** **A current account deficit IS a capital inflow — one fact, two names** — **and [[07 - Financial Crises|ch. 07]]'s sudden stop is the identity turning hostile.**
- **⚠️ Fixed-rate collapse is asymmetric**: defending a *strong* currency can go on forever (you can print), defending a *weak* one cannot (reserves are finite). **Speculators know which side they are on.**
- **China: pegged at 12 cents, \$4tn of reserves by 2014, revalued 2.1% in 2005** — **and it held option 3, which is why sterilization at that scale was possible at all. It still leaked into inflation.**
- **⚠️ A currency board removes the lender of last resort, and that is what killed Argentina's.** **Dollarization commits harder precisely because exit is harder — the same logic and the same cost as [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s nominal anchor.**

## ⚠️ Important Notes

1. **Long run = PPP; short run = interest parity.** Using either at the wrong horizon is the standard error.
2. **⚠️ PPP makes the exchange rate a *monetary* variable in the long run.**
3. **The real exchange rate is the summary statistic** — PPP says it equals 1.
4. **⚠️ Never read the Big Mac index as a forecast.** It measures a deviation, not a direction of travel.
5. **PPP fails on *nontraded* goods**, which are a large share of any price index.
6. **⚠️ PPP was wrong in sign over 1985–87.** Directional correctness is a long-horizon property only.
7. **⚠️ A high interest rate compensates for expected depreciation.** In equilibrium there is no carry profit.
8. **The interest-parity approximation drops $i_D\times$ appreciation** — fifth instance, and worst where both are large.
9. **⚠️ Today's exchange rate is mostly the expected future one.** That is why it jumps.
10. **Exchange rates follow a random walk** for [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s reason, not as a separate fact.
11. **⚠️ The trilemma is algebra.** You cannot try harder; a proposal achieving all three hides a capital control.
12. **The trilemma needs a *credible* peg.** Losing credibility is what turns it into a crisis.
13. **An unsterilized intervention is an open market operation.** Same balance sheet, different label.
14. **⚠️ Ask whether an intervention was sterilized.** If it was, expect nothing.
15. **⚠️ The current account and financial account are one quantity.** The identity explains nothing by itself.
16. **A "sudden stop" shows up as an improving external balance.** The improvement is the damage.
17. **⚠️ Defending a weak currency is finite; defending a strong one is not.**
18. **Reserve accumulation is the price of option 3**, not a sign of strength.
19. **⚠️ A currency board buys commitment by surrendering the lender of last resort.** Argentina paid that price.

> [!warning] Gaps in the source material
> **Two chapters in one note. Extraction was good for prose and for the one table; the figures are lost as usual.**
>
> **⚠️ TABLE 1 (the Big Mac index) SURVIVED COMPLETE** — six countries × four numeric columns — **and every figure in it is verified above.** **Summary Tables 2 and 3 (long-run and short-run factors) also came through.** **Eighth confirmation of the vault's rule: graphical exhibits are lost; tables set as text survive whole.**
>
> **All twelve figures are lost, and — checked per [[03 - The Behavior of Interest Rates|ch. 03]]'s rule — the prose does not name their data points.**
> - **The supply-and-demand diagrams for the FX market** (ch. 18 Figures 2–6, ch. 19 Figures 2–4) are shift diagrams with unlabelled axes; **their content is the direction of a shift, which the prose states and this note reproduces.**
> - **⚠️ The data series are real losses**: **Figure 1** (PPP, US/UK 1973–2017), **Figure 7** (the crisis and the dollar), **Figure 8** (Brexit and the pound), and **ch. 19 Figure 3** (the September 1992 sterling market). **Only the values Mishkin states in prose survive** — the +69%/+95% and −40% episodes, and the qualitative accounts of the crisis, Brexit and 1992. **No series is reconstructed.**
> - **⚠️ THE TRILEMMA TRIANGLE (ch. 19 Figure 4) is the interesting case.** **The diagram itself is lost, but its labels extracted intact** — the three sides and the three country examples (US, Hong Kong, China) — **and the prose states the trade-off in full.** **So its content is fully recovered, and §5 goes further by deriving it.** *(This is the one figure where the ch. 06 refinement applies: labels are usable **because** the prose independently confirms them.)*
>
> **No erratum.** **⚠️ Two discrepancies investigated and NOT filed**, both in Table 1: **Japan's index prints −36.7% where the columns give −36.96%, and Venezuela's prints −86.5% where they give −86.61%.** *(Diagnosed: **the index requires actual rates of 0.008434 and 0.005042, both of which round to the printed four-decimal values.**)* **So the printed exchange rates are rounded and the indices are computed from unrounded ones — an internal rounding difference, not an error.** **The other four rows and both prose cross-checks reproduce exactly.** **Recorded in [[00-Index]].**
>
> **⚠️ SCOPE NOTE — two chapters compressed.** **Deliberately reduced:** the mechanics and vocabulary of the FX market itself (spot versus forward, who trades, transaction sizes); the *Inside the Fed* account of a day at the New York Fed's FX desk; **the full history of exchange-rate regimes** (the gold standard, Bretton Woods, the EMS) — **retained only where it carries a result**; **the "should we worry about the US current account deficit?" and "will the euro survive?" boxes**; the detailed IMF-role and capital-controls debates; and **the Brexit and 2008-dollar applications**, which illustrate §4's mechanism without adding to it. **[[00-Index]]'s boundary also places European monetary institutions outside this scope.**
>
> **Additions beyond the source.**
>
> - **⚠️ §5 is the note's principal addition and the best thing in the chapter.** **Mishkin states the interest parity condition in one chapter's appendix and presents the policy trilemma as a triangle in the next, and never connects them.** **Deriving $i_D=i_F$ from a credible peg plus capital mobility turns a menu of trade-offs into an algebraic identity** — which changes how it should be argued about, since **two of the three assumptions do not make the third difficult, they make it false.** **The observation that the derivation's credibility assumption is exactly what fails in [[07 - Financial Crises|ch. 07]]'s speculative attack — and that this explains ch. 07's "rock and a hard place" — is also mine.**
> - **⚠️ §6's conclusion that a sterilized intervention is a *nothing* is mine**, though it follows from Mishkin's own footnote. **He presents sterilized and unsterilized intervention as two options with different effects and then concedes in a footnote that the portfolio balance effect is empirically insignificant and that any signalling effect is really the future policy change.** **Putting those together gives a sharper rule than the text states: ask whether it was sterilized, and if it was, expect nothing.**
> - **§2's verification of all six Big Mac rows, the diagnosis of the two rounding gaps, and the observation that the index works *because* a Big Mac is the purest nontraded good, are mine.** **Mishkin verifies two rows in prose and does not check the rest.**
> - **§3's side-by-side table of PPP's two episodes is mine** — he states both outcomes pages apart, and juxtaposing them is what makes the horizon-dependence visible as **right-sign-over-44-years, wrong-sign-over-3.**
> - **⚠️ §4's identification of the interest-parity approximation as the *fifth* dropped cross term, and as algebraically identical to [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation, is mine** — as is the observation that **it is the only one of the five where the source computes its own error.**
> - **§4's contrast between this denominator (close to 1, so no amplification) and [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s Gordon model (a small difference, so violent amplification) is mine**, and it is what identifies the *numerator* as the volatile part.
> - **§7's framing of the balance of payments as "one quantity with two names", and the link to [[07 - Financial Crises|ch. 07]]'s sudden stop, are mine.**
> - **§8's statement of the defence asymmetry — printing is unlimited, reserves are finite — as the general explanation of fixed-rate collapse is mine**, as is the observation that **China's sterilization was only possible behind capital controls, i.e. that the trilemma explains the \$4 trillion.**

**Previous:** [[09 - Tools and Conduct of Monetary Policy]] · **Next:** [[11 - Money Demand and the Monetary Policy Framework]]
