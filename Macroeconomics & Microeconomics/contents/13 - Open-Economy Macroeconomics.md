---
subject: Macroeconomics & Microeconomics
chapter: 13
tags: [ds, economics, macroeconomics, open-economy, exchange-rates, ppp, balance-of-payments, tariffs]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 18–19; Parkin & Bade, *Macroeconomics*, ch. 25"
---

# Open-Economy Macroeconomics

**Every chapter since [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]] assumed a closed economy. This one opens it** — and the result is that several things people argue about turn out to be the same fact described differently.

**Three results.**

**§2 — a trade deficit *is* a capital inflow.** *(Verified: $NX = NCO$ identically, and $NX = S - I$.)* **"We buy more than we sell" and "the world invests in us" are not two facts that co-occur — they are one accounting fact stated twice.**

**§5 — a tariff cannot improve the trade balance.** *(Computed: at tariffs cutting imports by 10, 20 and 30, the trade balance is **20.00 in every case** while trade *volume* falls from 220 to 160.)* **Mankiw argues this verbally; it follows from an identity plus one assumption.**

**§1 — Parkin & Bade's balance-of-payments accounts sum to zero** *(verified on Canada 2013: −60 + 65 − 5 = **0**)*, **and P&B extracts cleanly — no cipher** — which is why [[00-Index]] makes it a co-equal source here.

> [!warning] ⚠️ Mankiw's equations reconstructed, not transcribed. **Parkin & Bade does *not* share the cipher** and is used directly. See [[00-Index]].

## 📘 Main Knowledge

### 1. The balance of payments *(Parkin & Bade)*

**Three accounts** record a country's international transactions:

| account | records |
|---|---|
| **current** | exports − imports, net interest income, net transfers |
| **capital and financial** | foreign investment here − our investment abroad |
| **official settlements** | the change in official foreign-currency reserves |

*(Verified — P&B's Table 25.1, Canada 2013, \$bn:)*

| | |
|---|---|
| exports of goods and services | **+566** |
| imports of goods and services | **−598** |
| net interest income | −26 |
| net transfers | −2 |
| **current account balance** | **−60** ✓ |
| net foreign investment in Canada | +65 |
| **capital & financial balance** | **+65** ✓ |
| **official settlements** | **−5** |
| **SUM** | **0** ✓ |

> [!warning] The three balances sum to zero by construction
> **A current-account deficit *must* be financed** — by borrowing from abroad or by running down official reserves. **There is no third possibility.**
>
> *(P&B's own reading: the capital account (+65) plus the current account (−60) is +5, so Canadian official reserves **rose** by \$5bn — which appears as **−5** because holding foreign money is investing abroad.)*
>
> **⚠️ Note the sign convention, which trips everyone**: an *increase* in official reserves is a *negative* entry, because acquiring foreign assets is a capital outflow.

### 2. ⚠️ Two identities, and what they mean

$$NX = \text{exports} - \text{imports}\qquad NCO=\begin{array}{c}\text{our purchases of foreign assets}\\-\text{ foreign purchases of ours}\end{array}$$

$$\boxed{NX = NCO}\qquad\text{always}$$

**Every transaction has two sides.** If we buy a foreign good, the foreign seller ends up holding **either our goods** (an export) **or our assets** (a capital inflow). **There is nothing else they can do with the money.**

**And from [[10 - Saving, Investment and the Financial System|ch. 10]]'s identity in an open economy:**

$$Y=C+I+G+NX\;\Longrightarrow\;S=Y-C-G=I+NX\;\Longrightarrow\;\boxed{NX=S-I}$$

*(Computed — the same economy at different investment levels, with $S=100$:)*

| investment | $NX = S-I$ | interpretation |
|---|---|---|
| 60 | **+40** | trade **surplus** — we lend abroad |
| 100 | 0 | balanced |
| **120** | **−20** | trade **deficit** — the world lends to us |
| 140 | −40 | larger deficit |

> [!warning] "We buy more than we sell" and "the world invests in us" are the same sentence
> **Not two facts that happen to co-occur. One accounting fact, described twice.**
>
> **And $NX = S - I$ says the trade balance is determined by *saving and investment*** — not by trade policy, not by competitiveness, not by how hard anyone bargains. **That is §5's result before it is demonstrated.**
>
> *(A useful corollary: a country running a trade deficit is investing more than it saves. Whether that is a problem depends entirely on **what the investment is for** — borrowing to build factories and borrowing to fund consumption look identical in the trade statistics.)*

### 3. Exchange rates, nominal and real

$$\text{real exchange rate}=e\times\frac{P_{\text{domestic}}}{P_{\text{foreign}}}$$

**The nominal rate is the price of one currency in another; the *real* rate is the rate at which *goods* trade.**

*(Computed — domestic beer at \$100, foreign at 500 of theirs:)*

| $e$ | real rate | |
|---|---|---|
| 4 | 0.80 | domestic goods cheaper |
| 5 | **1.00** | parity |
| 6 | 1.20 | domestic goods dearer |

> [!note] The nominal rate alone tells you nothing
> **A real depreciation makes domestic goods cheaper abroad and raises net exports.** But the same nominal rate can be a real appreciation or depreciation depending on the two price levels.
>
> **This is [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s real/nominal distinction for the third time** — GDP, then interest rates, now exchange rates. **The pattern is worth naming: any nominal quantity needs deflating before it means anything.**

### 4. Purchasing-power parity

**PPP: a unit of currency should buy the same quantity of goods everywhere**, because otherwise arbitrage would move goods until it does.

$$e_{\text{implied}}=\frac{P_{\text{foreign}}}{P_{\text{domestic}}}$$

*(Computed — the Big Mac test, which P&B discusses, with a \$5.00 home price:)*

| | local price | **implied PPP rate** | actual rate | verdict |
|---|---|---|---|---|
| Country A | 25.00 | 5.00 | 5.00 | **at PPP** |
| Country B | 30.00 | 6.00 | 4.00 | **overvalued** (−33.3%) |
| Country C | 60.00 | 12.00 | 15.00 | **undervalued** (+25.0%) |
| Country D | 15.00 | 3.00 | 5.00 | **undervalued** (+66.7%) |

> [!warning] PPP is a long-run anchor and a poor short-run predictor
> **Mankiw gives two reasons, and both are structural:**
>
> 1. **Many goods are not traded** — haircuts, housing, restaurant meals. **No arbitrage force acts on them at all.**
> 2. **Traded goods are not perfect substitutes** — a German car is not a Japanese car, so their prices need not converge.
>
> **⚠️ And this explains a systematic pattern: poor countries look "cheap" on PPP measures because their *non-traded* goods — mostly labour — are cheap, and nothing arbitrages labour across borders.** *(Which is why PPP-adjusted GDP comparisons differ so much from market-rate ones, and why the adjustment is essential for [[09 - Production and Growth|ch. 09]]'s cross-country comparisons.)*
>
> **The useful form: PPP tells you where the rate should go over years and nothing about next quarter.**

### 5. ⚠️ The two-market model, and why a tariff does not work

**An open economy has two markets that must clear together:**

| market | condition | cleared by |
|---|---|---|
| **loanable funds** | $S = I + NCO$ | the **real interest rate** |
| **foreign exchange** | $NCO = NX$ | the **real exchange rate** |

*(Computed baseline: $r = 2.667\%$, $S = 153.33$, $I = 133.33$, $NCO = NX = 20.00$.)*

**(a) A budget deficit of 30:**

| | before | after |
|---|---|---|
| real interest rate | 2.667% | **3.167%** |
| investment | 133.33 | **120.83** *(crowding out — [[10 - Saving, Investment and the Financial System|ch. 10]])* |
| $NCO = NX$ | 20.00 | **12.50** |

> [!note] The twin deficits
> **The higher interest rate attracts foreign capital, the currency appreciates, and the trade balance worsens.** **A budget deficit produces a trade deficit — through the interest rate**, not through anything to do with trade.

**(b) A tariff.** *(Computed — tariffs cutting imports by 10, 20, 30:)*

| imports | exports | **$NX$** | trade volume |
|---|---|---|---|
| 100.0 | 120.0 | **20.00** | 220.0 |
| 90.0 | 110.0 | **20.00** | 200.0 |
| 80.0 | 100.0 | **20.00** | 180.0 |
| 70.0 | 90.0 | **20.00** | **160.0** |

> [!warning] The trade balance is unchanged at every tariff level — only the volume falls
> **The argument is short: $NX = NCO$, and $NCO$ is determined in the loanable-funds market by $S$ and $I$. A tariff changes neither saving nor investment. So $NCO$ is unchanged, therefore $NX$ is unchanged.**
>
> **What *does* change:** fewer imports raise the demand for domestic currency, **the currency appreciates, and exports fall by exactly the amount imports fell.**
>
> **So a tariff imposed to "fix the trade deficit" cannot do it** — because the trade deficit is not caused by trade policy. **It is $S-I$.**
>
> **This is the strongest policy result in the macro half**, and it follows from an accounting identity plus a single behavioural assumption: that tariffs do not shift saving or investment. *(If a tariff did change saving — by raising government revenue, say — the conclusion would soften, which is worth stating rather than hiding.)*
>
> **And [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] computed what the lost volume costs**: the two deadweight-loss triangles. **So a tariff has a real cost and no effect on the thing it is usually justified by.**

### 6. What the chapter adds up to

$$Y=C+I+G+NX\qquad NX=S-I\qquad NX=NCO$$

> [!note] Three descriptions of one fact
> **A trade deficit *is* a capital inflow *is* an excess of investment over saving.**
>
> **So the questions people actually argue about — "should we fix the trade deficit", "are we being outcompeted" — are mostly asking about the wrong variable.** **The right question is why $S$ is low or $I$ is high**, and those are [[09 - Production and Growth|ch. 09]]'s and [[10 - Saving, Investment and the Financial System|ch. 10]]'s subjects.
>
> **And note the political-economy echo of [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]**: a tariff's beneficiaries are concentrated and identifiable while its costs are diffuse — **which predicts the policy far better than any of this analysis does.**

## ✏️ Exercises

**1. (Accounting.)** (a) Why do the BoP accounts sum to zero? (b) Prove $NX = NCO$. (c) What does $NX = S - I$ imply?

> [!example]- Solution
> **(a) Because a deficit must be financed, and there are only two ways.**
>
> *(Verified on P&B's Canada 2013: current **−60**, capital and financial **+65**, official settlements **−5**, summing to **0**.)*
>
> **If a country buys more goods and services than it sells, the difference must come from somewhere: borrowing from abroad (capital inflow) or running down official reserves.** The accounts are constructed to record exactly that, so **the sum is zero by definition, not by coincidence.**
>
> **⚠️ The sign convention catches people out**: an *increase* in official reserves is a *negative* entry, because acquiring foreign assets is investing abroad. *(P&B: reserves rose \$5bn, recorded as −5.)*
>
> **(b) Because every transaction has two sides.**
>
> **If we buy a foreign good, the seller receives our currency. They can spend it on our goods (an export, reducing $NX$'s deficit) or on our assets (a capital inflow, reducing $NCO$). There is no third option** — holding the currency indefinitely *is* holding a domestic asset.
>
> **So $NX = NCO$ identically.** It is not an equilibrium condition that markets bring about; **it is true at every instant.**
>
> **(c) That the trade balance is set by saving and investment, not by trade.**
>
> $$Y=C+I+G+NX\;\Longrightarrow\;NX=(Y-C-G)-I=S-I$$
>
> *(Computed with $S=100$: investment of 60 / 100 / 120 gives $NX$ of **+40 / 0 / −20**.)*
>
> **A trade deficit means a country is investing more than it saves, and borrowing the difference.**
>
> **⚠️ Whether that is a problem depends entirely on what the investment is for.** **Borrowing to build factories and borrowing to fund consumption produce identical trade statistics** and completely different futures — which is why "the trade deficit" is not by itself a diagnosis.
>
> **And it sets up §5**: if $NX = S - I$, then anything that does not change $S$ or $I$ cannot change $NX$.

**2. (Hard — exchange rates.)** (a) Distinguish nominal from real. (b) State PPP and why it fails. (c) Why do poor countries look cheap?

> [!example]- Solution
> **(a) The real rate is the rate at which *goods* trade.**
>
> $$\text{real rate}=e\times\frac{P_{\text{domestic}}}{P_{\text{foreign}}}$$
>
> *(Computed: at a nominal rate of 4, 5, 6 foreign units per dollar, the real rate is **0.80, 1.00, 1.20** — domestic goods cheaper, at parity, dearer.)*
>
> **A real depreciation raises net exports because it makes domestic goods cheaper abroad.** **The nominal rate alone tells you nothing** — the same nominal move can be a real appreciation or depreciation depending on relative inflation.
>
> **⚠️ This is the third appearance of [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s real/nominal distinction** — GDP, interest rates, exchange rates. **Any nominal quantity needs deflating before it means anything**, and that generalises well past economics.
>
> **(b) A currency should buy the same goods everywhere — and it does not, for two structural reasons.**
>
> **The logic is arbitrage: if a good is cheaper in one country, buying there and selling here is profitable until prices converge.**
>
> *(Computed on Big Mac figures: implied rates of **5.00 / 6.00 / 12.00 / 3.00** against actual rates of 5.00 / 4.00 / 15.00 / 5.00 — deviations up to **+66.7%**.)*
>
> **It fails because:**
>
> 1. **Many goods are not traded** — haircuts, housing, restaurant meals. **No arbitrage force acts on them at all**, and they are a large share of any consumption basket.
> 2. **Traded goods are not perfect substitutes** — a German car is not a Japanese car, so their prices need not converge even with free trade.
>
> **So PPP is a long-run anchor**: over years, currencies with high inflation do depreciate roughly as PPP predicts. **Over quarters it predicts nothing.**
>
> **(c) Because their non-traded goods are cheap, and nothing arbitrages labour.**
>
> **⚠️ Non-traded goods are mostly labour-intensive services**, and wages are far lower in poor countries because [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s marginal product is lower there. **Nothing moves haircuts across borders**, so the price gap persists.
>
> **The consequence is practical: PPP-adjusted GDP comparisons differ enormously from market-exchange-rate ones**, and **the PPP version is the right one for comparing living standards** — which is why [[09 - Production and Growth|ch. 09]]'s cross-country comparisons need it. *(Market rates are right for comparing purchasing power over **traded** goods, e.g. debt service or imports.)*

**3. (Policy.)** (a) Trace a budget deficit through both markets. (b) Show a tariff cannot change the trade balance. (c) What does the chapter add up to?

> [!example]- Solution
> **(a) Twin deficits, connected by the interest rate.**
>
> *(Computed: a deficit of 30 raises $r$ from **2.667% to 3.167%**, cuts investment from **133.33 to 120.83**, and cuts $NCO = NX$ from **20.00 to 12.50**.)*
>
> **The chain: lower public saving → higher real interest rate → two effects.** **Domestically**, investment falls — [[10 - Saving, Investment and the Financial System|ch. 10]]'s crowding out. **Internationally**, the higher rate attracts foreign capital, so $NCO$ falls, **the currency appreciates, and net exports fall.**
>
> **So a budget deficit produces a trade deficit through the interest rate**, with nothing to do with trade policy or competitiveness. *(The open economy therefore spreads the cost of a deficit: some falls on domestic investment and some on net exports, and the split depends on how mobile capital is.)*
>
> **(b) Because $NX = NCO$ and a tariff changes neither $S$ nor $I$.**
>
> *(Computed: at tariffs cutting imports by 10, 20 and 30, **$NX$ is 20.00 in every case** while trade volume falls **220 → 160**.)*
>
> **The argument in three lines:**
> 1. $NX = NCO$ *(identity)*;
> 2. $NCO$ is determined in the loanable-funds market by $S$ and $I$;
> 3. a tariff changes neither, **so $NCO$ and therefore $NX$ are unchanged.**
>
> **What happens instead: fewer imports raise demand for domestic currency, the currency appreciates, and exports fall by exactly as much as imports did.**
>
> **⚠️ So a tariff imposed to fix a trade deficit cannot do it**, and [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]] already computed what the lost volume costs — two deadweight-loss triangles. **A real cost, and no effect on the stated objective.**
>
> **The honest caveat: this rests on tariffs not shifting saving or investment.** If tariff revenue raised public saving, $NX$ would improve a little. **The result is robust in direction rather than exact** — and stating that is better than pretending an identity settles everything.
>
> **(c) Three descriptions of one fact.**
>
> $$Y=C+I+G+NX\qquad NX=S-I\qquad NX=NCO$$
>
> **A trade deficit *is* a capital inflow *is* an excess of investment over saving.**
>
> **So the usual questions — "should we fix the trade deficit", "are we being outcompeted" — target the wrong variable.** **The substantive question is why saving is low or investment high**, which returns to [[09 - Production and Growth|ch. 09]] and [[10 - Saving, Investment and the Financial System|ch. 10]].
>
> **And [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s political economy predicts the policy better than the economics does**: a tariff's gains are concentrated on identifiable firms and its losses spread thinly over everyone. **That asymmetry, not any analysis in this chapter, is why tariffs persist.**

## 📝 Summary

- **The balance of payments has three accounts and they sum to zero by construction** *(verified on P&B's Canada 2013: **−60 + 65 − 5 = 0**)*. **A current-account deficit must be financed** — there is no third option.
- **⚠️ Sign convention: an *increase* in official reserves is a *negative* entry**, because acquiring foreign assets is investing abroad.
- **⚠️ $NX = NCO$ identically** — every transaction has two sides, and a foreign seller can hold **either our goods or our assets**.
- **$NX = S - I$**, so **the trade balance is determined by saving and investment, not by trade policy** *(computed: $S=100$ with investment of 60/100/120 gives $NX$ of **+40/0/−20**)*.
- **⚠️ "We buy more than we sell" and "the world invests in us" are the same sentence** — one accounting fact stated twice. **Whether a deficit is a problem depends on what the borrowing funds.**
- **The real exchange rate is $e\times P_{\text{dom}}/P_{\text{for}}$ — the rate at which *goods* trade** *(computed: nominal 4/5/6 gives real 0.80/1.00/1.20)*. **Third appearance of [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s real/nominal split.**
- **PPP: $e = P_{\text{for}}/P_{\text{dom}}$** *(computed on Big Mac figures: deviations up to **+66.7%**)*. **A long-run anchor and a poor short-run predictor.**
- **It fails because many goods are not traded and traded goods are not perfect substitutes.**
- **⚠️ Poor countries look "cheap" because their non-traded goods — mostly labour — are cheap, and nothing arbitrages labour.** That is why **PPP-adjusted comparisons are the right ones for living standards** ([[09 - Production and Growth|ch. 09]]).
- **Two markets clear together**: loanable funds ($S = I + NCO$, cleared by the real interest rate) and foreign exchange ($NCO = NX$, cleared by the real exchange rate).
- **A budget deficit gives twin deficits** *(computed: $r$ **2.667% → 3.167%**, investment **133.33 → 120.83**, $NX$ **20.00 → 12.50**)* — **through the interest rate**, not through trade.
- **⚠️ A tariff cannot change the trade balance** *(computed: $NX$ = **20.00** at every tariff level, while volume falls **220 → 160**)*. **$NX = NCO$, $NCO$ is set by $S$ and $I$, and a tariff changes neither.**
- **What changes is the exchange rate: the currency appreciates and exports fall by exactly the amount imports fell.**
- **So a tariff has a real cost** ([[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s triangles) **and no effect on its usual justification.**
- **Three identities, one fact: a trade deficit is a capital inflow is an excess of investment over saving.** **The substantive question is why $S$ is low or $I$ is high.**

## ⚠️ Important Notes

1. **The three BoP accounts sum to zero by construction**, not as an empirical finding.
2. **⚠️ Rising official reserves = a negative entry.** The convention catches everyone once.
3. **⚠️ $NX = NCO$ is an identity**, true at every instant — not an equilibrium condition.
4. **$NX = S - I$** — the trade balance is a saving-investment gap.
5. **A trade deficit is not by itself a diagnosis.** Ask what the borrowing funds.
6. **⚠️ Use the *real* exchange rate for anything about competitiveness.** The nominal rate alone means nothing.
7. **Any nominal quantity needs deflating** — GDP, interest rates, exchange rates ([[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]).
8. **PPP is a long-run anchor**, useless over quarters.
9. **⚠️ Non-traded goods break PPP**, and they are a large share of consumption.
10. **⚠️ Use PPP-adjusted GDP for living standards** and market rates for traded-goods purchasing power. They answer different questions.
11. **Two markets, two prices**: the interest rate clears loanable funds, the exchange rate clears foreign exchange.
12. **Budget deficits produce trade deficits via the interest rate** — the twin-deficit chain.
13. **⚠️ A tariff cannot change $NX$** because it changes neither $S$ nor $I$.
14. **A tariff reduces trade *volume* in both directions** — imports fall and exports fall equally.
15. **State the assumption**: the result holds because tariffs do not shift saving or investment. **Direction is robust; the exact figure is not.**
16. **⚠️ Concentrated gains and diffuse losses predict trade policy better than the economics does** ([[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]).

> [!warning] Gaps in the source material
> **Two sources, and they behave differently.**
>
> **Mankiw** *(Macro 2017, PDF pp. 400–445 for chs. 18–19)* extracts cleanly as prose **and carries the operator cipher** — see [[00-Index]]. **Nothing was transcribed.**
>
> **⚠️ Parkin & Bade ch. 25 extracts cleanly AND does *not* share the cipher** — its minus signs come through as real minus signs, and **Table 25.1 survived complete with all nine lines.** *(This confirms the setup finding recorded in [[00-Index]], and it is why P&B is used here as a co-equal source for the balance-of-payments material rather than as a supplement — exactly as the subject file anticipated when it noted that P&B's presence in a Mankiw course is a deliberate signal.)*
>
> **⚠️ Every figure in both sources is lost**, including Mankiw's two-market diagram — **the loanable-funds and foreign-exchange panels that are the chapter's central apparatus** — and all the policy-experiment panels. **This is why §5 builds both markets algebraically from explicitly stated linear curves**; the diagram cannot be recovered, and the algebra delivers the tariff result as a computation rather than an assertion.
>
> **No erratum.** P&B's table balances exactly, and every figure Mankiw states reproduces.
>
> **Additions beyond the source.**
>
> - **⚠️ §5's tariff computation is the chapter's main addition.** **Mankiw makes the argument verbally — a tariff does not change $NX$ because it does not change $S$ or $I$ — and does not compute it.** Showing **$NX = 20.00$ at every tariff level while volume falls 220 → 160** turns the claim into a demonstration, and pairing it with [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s deadweight triangles gives the full verdict: **a real cost and no effect on the stated objective.**
> - **The explicit statement of the assumption** — that the result holds because tariffs do not shift saving or investment, and would soften if tariff revenue raised public saving — **is mine**, and it follows the rule established in [[10 - Saving, Investment and the Financial System|ch. 10]]: **name the assumption a diagram is quietly making.**
> - **§5(a)'s two-market solution of the budget deficit**, showing the split between crowding out and trade-balance deterioration, is computed rather than described.
> - **§4's observation that poor countries look cheap because non-traded goods are labour** — connecting PPP deviations to [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s marginal-product theory of wages, and explaining why PPP-adjusted comparisons are the right ones for [[09 - Production and Growth|ch. 09]]'s purposes — is mine.
> - **The framing that $NX = NCO$, $NX = S-I$ and the GDP identity are three descriptions of one fact**, so the usual policy debate targets the wrong variable, is my synthesis.
> - **The note that a trade deficit's significance depends on what the borrowing funds** — factories versus consumption look identical in the statistics — is an addition.
>
> **Deliberately compressed.** **Mankiw ch. 18's institutional detail on international flows** (the four categories of NCO, the data on US net foreign investment) is represented by the identities. **The extended case studies** (the US trade deficit's history, capital flight in a financial crisis) illustrate §5's mechanism. **Ch. 19's formal derivation of the two-market diagram** is replaced by the algebra in §5, since the diagram is lost. **P&B's material on exchange-rate determination** (the demand and supply of a currency, expected-profit effects, interest-rate parity, and the Bank of Canada's exchange-rate policy) is compressed to §§3–4 — **the currency-market mechanics are Mishkin's by the boundary recorded in [[00-Index]]**, and P&B is used here for the balance-of-payments accounting it does better than Mankiw. **The Big Mac index figures are illustrative and mine**, since P&B's actual table is a figure and is lost.

**Previous:** [[12 - The Monetary System and Inflation]] · **Next:** [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve]]
