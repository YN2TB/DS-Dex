---
subject: Monetary and Financial Theories
chapter: 11
tags: [ds, economics, quantity-theory, velocity, money-demand, liquidity-trap, is-curve, aggregate-demand, hyperinflation]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 20–22"
---

# Money Demand and the Monetary Policy Framework

> [!warning] ⚠️ THIS PAYS [[08 - Central Banks and the Money Supply Process|CH. 08]]'s REMAINING DEBT
> **Ch. 08 found the quantity theory failed in *two* places and repaired only one.** **The multiplier collapsed 1.60 → 0.73 — fixed there.** **Velocity fell 29% over 2007–17 — deferred here.** **§5 settles it, and with it the last of [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s three criteria for monetary targeting.**

**Four results.**

**§2 — ⚠️ a SIXTH dropped cross term, and hyperinflation is where it breaks.** *(Computed: at 2,000,000% money growth the approximation understates inflation by **222,223 percentage points**.)* **⚠️ And the irony is the point: the quantity theory is *most convincing* in hyperinflations and its standard algebraic form is *least accurate* there.**

**§3 — Zimbabwe, and the result Mishkin does not draw.** *(Computed: prices doubled every **26 days** officially, **22** unofficially — and at 2 million percent Zimbabwe was **20,000 times past** the revenue-maximising inflation rate [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] computed.)* **⇒ the printing was not even raising much revenue.**

**§5 — the debt paid, and one cause behind two failures.** **Money demand is interest-sensitive *and* has been unstable since 1973** — **and the culprit is financial innovation, exactly what [[01 - The Financial System and What Money Is|ch. 01]] blamed for the measurement failure.** **One cause, two failures; Mishkin never connects them.**

**§7 — ⚠️ THE SLOPE OF THE AGGREGATE DEMAND CURVE IS THE CENTRAL BANK'S REACTION COEFFICIENT.** *(Recovered algebraically: $Y=11.0-\lambda\pi$.)* **Mishkin draws AD as a fixed object of the economy. It is nothing of the kind — the central bank is inside the curve.**

## 📘 Main Knowledge

### 1. The equation of exchange — an identity, and what turns it into a theory

$$V=\frac{P\times Y}{M}\qquad\Longrightarrow\qquad \boxed{\ M\times V=P\times Y\ }$$

*(Verified: nominal GDP \$10tn against a money supply of \$2tn gives $V=\mathbf{5}$ — the average dollar is spent five times a year.)*

> [!warning] ⚠️ This is an identity — true by definition, and it says nothing
> **A rise in $M$ could be exactly offset by a fall in $V$.** **To get a *theory* you must add an assumption about velocity.**

**Fisher's assumption:** **velocity is determined by *institutions* — payment technology, credit cards, how often people are paid — which change only slowly.** **So $V$ is constant in the short run:**

$$P\times Y=M\times\bar V\qquad\text{and}\qquad M^d=k\times PY,\quad k=1/\bar V$$

> [!note] ⚠️ Look at what that last equation says
> **Money demand depends *only* on income. Interest rates do not enter.** **That is the sharp claim the rest of the chapter attacks, and it is the entire difference between Fisher and Keynes.**

*(The worked chain, all verified: $M$ doubling from \$2tn to \$4tn gives $PY=\$20$tn; and $P=MV/Y$ gives **1.0** then **2.0**. **With $Y$ fixed at full employment, doubling $M$ doubles $P$ exactly.**)*

### 2. ⚠️ The quantity theory of inflation — and a sixth cross term

**Mishkin: "the percentage change of a product of two variables is *approximately* equal to the sum of the percentage changes."** Applied to $MV=PY$ with $\%\Delta V=0$:

$$\boxed{\ \pi=\%\Delta M-\%\Delta Y\ }$$

*(Verified: money growth 5% with output growth 3% gives **2%**; money growth 10% gives **7%**.)*

> [!warning] ⚠️ But the step is an approximation, and it is the sixth in this subject
> $$\text{exact: }\pi=\frac{(1+g_M)(1+g_V)}{1+g_Y}-1\qquad\text{approximate: }\pi=g_M+g_V-g_Y$$
>
> | money growth | output growth | approx | **exact** | error |
> |---|---|---|---|---|
> | 5% | +3% | 2.0% | 1.9% | +0.1 pts |
> | 10% | +3% | 7.0% | 6.8% | +0.2 pts |
> | 100% | −5% | 105.0% | **110.5%** | **−5.5 pts** |
> | **1,500%** | −10% | 1,510% | **1,678%** | **−168 pts** |
> | **2,000,000%** | −10% | 2,000,010% | **2,222,233%** | **−222,223 pts** |
>
> **At ordinary rates the error is a fraction of a point and the approximation is entirely safe.** **At Zimbabwean rates it understates inflation by about 11% of the answer.**
>
> **⚠️ And the irony is the thing worth keeping.** **The quantity theory is at its *most convincing* in hyperinflations — that is where money growth so dominates everything else that the theory is unarguable — and that is exactly where its standard algebraic form is *least accurate*.** **The economics is right and the arithmetic is wrong, in the same case.**
>
> **Sixth instance.** *([[02 - The Meaning of Interest Rates|Ch. 02]]'s Fisher equation; ch. 02's duration/convexity; [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s arithmetic-versus-geometric average; [[07 - Financial Crises|ch. 07]]'s debt deflation; [[10 - Foreign Exchange and the International Financial System|ch. 10]]'s interest parity; this.)* **Always ask what the neglected term is proportional to.**

### 3. Zimbabwe — what those numbers mean

**The mechanism is [[07 - Financial Crises|ch. 07]]'s path B in its purest form.** **Farms expropriated in 2000 → agricultural output collapses → tax revenue collapses.** **Raising taxes was politically impossible; borrowing was impossible because nobody trusted the government.** **⇒ only the printing press was left.**

> [!note] Criminalising inflation
> **In February 2007 the central bank outlawed price increases on many commodities.** **Mishkin: "criminalizing inflation cannot stop inflation when the central bank keeps on printing money."** **⚠️ The price is not the disease.**

*(Computed from his own figures:)*

| | monthly price factor | **prices double every** |
|---|---|---|
| March 2007: **1,500%** | ×1.260 | 91 days |
| 2008 official: **2,000,000%** | ×2.283 | **26 days** |
| 2008 unofficial: **10,000,000%** | ×2.610 | **22 days** |

**A wage negotiated at the start of a month was worth half as much by the end of it** — which is why the bank ended up issuing a **\$100 trillion note** that "could not even buy you a bottle of beer."

> [!warning] ⚠️ And here is the result Mishkin does not draw, using Macro/Micro's own computation
> **[[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] modelled the inflation tax with Cagan money demand and found revenue *peaks at 100% inflation* and falls thereafter, because people stop holding money.**
>
> *(So Zimbabwe at 1,500% was **15 times** past the revenue-maximising rate, and at 2,000,000% it was **20,000 times** past it.)*
>
> **⇒ the printing was not even raising much revenue.** **Past the peak, printing faster collects *less*.** **The government was destroying its currency to obtain a shrinking real transfer** — which is why hyperinflations end, and end abruptly. *(Zimbabwe dollarized in 2009 — and [[10 - Foreign Exchange and the International Financial System|ch. 10]] §8 explains why that is the ultimate commitment device: it cannot easily be reversed.)*

### 4. Theories of money demand — and where interest rates enter

| theory | money demand | velocity |
|---|---|---|
| **Fisher / Cambridge** | $M^d=k\cdot PY$ — **transactions only, no interest rate** | **constant** |
| **Keynes (liquidity preference)** | $M^d/P=f(i,Y)$ — three motives | **not constant** |
| **Baumol–Tobin** | even *transactions* demand is interest-sensitive | not constant |
| **Friedman (modern quantity theory)** | permanent income + relative returns | **predictable, not constant** |

**Keynes's three motives:** **transactions** and **precautionary** (both proportional to income), and **⚠️ speculative — which depends on the interest rate**, because money competes with bonds as a store of wealth and a higher rate raises the opportunity cost of holding money *([[03 - The Behavior of Interest Rates|ch. 03]]'s liquidity preference)*.

> [!warning] ⚠️ And therefore velocity is not an institutional constant
> **$V=Y/f(i,Y)$ rises with the interest rate.** **Since interest rates are procyclical, *velocity is procyclical*.** **It is not a slow-moving feature of payment technology at all.**

**Baumol–Tobin goes further**: **even the transactions motive is interest-sensitive**, because holding cash to transact has an opportunity cost. **Keynes had conceded the speculative motive; this takes the other two as well.**

**Friedman's restoration**: money demand depends on **permanent income** and on the return on money *relative* to other assets — **and because banks compete, those returns move together, so the differential is stable.** **⇒ velocity becomes *predictable* rather than *constant***, which is a weaker claim but a usable one.

> [!note] ⚠️ Note the shape of the whole argument
> **Nobody disputes the identity.** **The entire debate is about one function — is money demand stable, and does it depend on interest rates — because that function is what turns an identity into a theory.**
>
> *(Summary Table 1 lists **seven** determinants: interest rates (−), income (+), payment technology (−), wealth (+), riskiness of other assets (+), inflation risk (−), liquidity of other assets (−). **Six more than Fisher allowed.**)*

### 5. ⚠️ Paying ch. 08's debt — is velocity stable?

**Mishkin's empirical section answers the two questions that decide it, and both answers go against the quantity theory.**

**(1) Is money demand sensitive to interest rates?** **"The evidence for the interest sensitivity of the demand for money is remarkably consistent… the demand for money *is* sensitive to interest rates."** **⇒ velocity moves with rates ⇒ not constant.**

> [!warning] ⚠️ And at the zero lower bound it becomes infinitely sensitive — the liquidity trap
> **Money demand goes *flat*, so a change in the money supply moves the interest rate *not at all*.**
>
> **⇒ that is [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s floor system in a different diagram.** **There, an open market operation could not move the funds rate because supply ran into a flat demand curve; here it is the same flatness named from the money-demand side.**
>
> **⚠️ [[08 - Central Banks and the Money Supply Process|Ch. 08]]'s collapsed multiplier, [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s dead open market operations and ch. 11's liquidity trap are one phenomenon described three ways.**

**(2) Is money demand stable?** **"Until the early 1970s, the evidence strongly supported the stability of the money demand function. However, *after 1973*, the rapid pace of **financial innovation**, which changed the items that could be used as money, led to substantial instability."**

> [!warning] ⚠️ One cause, two failures — and Mishkin never puts them together
> **[[01 - The Financial System and What Money Is|Ch. 01]]: financial innovation moved assets across the M1/M2 boundary, so the *measure* stopped meaning the same thing.**
> **Ch. 11: the same innovation moved the money-demand *function*, so velocity stopped being predictable.**
>
> **The same historical process broke the numerator and the relationship it was supposed to feed.**

> [!warning] ⚠️ So all three conditions for monetary targeting are now settled — and all three failed
> | criterion | chapter | verdict |
> |---|---|---|
> | **stable measure** | [[01 - The Financial System and What Money Is\|ch. 01]] | **FAILED** — M1 vs M2 gave inflation forecasts **8 points apart** |
> | **controllable $M$** | [[08 - Central Banks and the Money Supply Process\|ch. 08]] | **FAILED** — multiplier **1.60 → 0.73**, and it belongs to three players |
> | **stable velocity** | **ch. 11** | **FAILED** — unstable since 1973; **−29%** over 2007–17 |
>
> **Mishkin's conclusion, now fully earned: "the instability of money demand has led to a downgrading of the focus on money supply in the conduct of monetary policy."**
>
> **⚠️ And note the *logic* of the switch.** If money demand is unstable then the money supply is not closely linked to spending, and so — his words — **"the level of interest rates set by the Fed will provide *more information* about the stance of monetary policy than will the money supply."** **The interest rate wins by default, not on merit.**

### 6. ⚠️ The IS–MP–AD model, recovered algebraically

> [!note] The three-panel figure is lost — but the prose names every point
> **As in [[03 - The Behavior of Interest Rates|ch. 03]], Mishkin walks through three inflation rates and states the resulting interest rate and output at each.** **So all three curves are recoverable.**

**MP curve** *(stated by Mishkin)*: $r=\bar r+\lambda\pi=1.0+0.5\pi$

**IS curve** *(recovered — $r$ falls 0.5 pt as $Y$ rises \$0.5tn, so the slope is −1)*: $Y=12.0-r$

**AD curve** *(derived by substitution)*: $Y=12-(1.0+0.5\pi)=\mathbf{11.0-0.5\pi}$

| $\pi$ | **$r$** | **$Y$** | book |
|---|---|---|---|
| 1.0% | **1.5%** | **\$10.5tn** | ✓ |
| 2.0% | **2.0%** | **\$10.0tn** | ✓ |
| 3.0% | **2.5%** | **\$9.5tn** | ✓ |

**All nine points reproduce. The whole model is three lines.**

> [!warning] ⚠️ The chain is the content
> **MP turns inflation into a real interest rate; IS turns the real interest rate into output; AD is their composition.**
>
> **⇒ aggregate demand slopes downward *not* because of any wealth effect or direct interest-rate effect on spending, but because the central bank raises real rates when inflation rises.** **The central bank is inside the curve.**

### 7. ⚠️ The slope of AD is a policy choice

**Generally, with IS: $Y=A-r$ and MP: $r=\bar r+\lambda\pi$:**

$$Y=(A-\bar r)-\lambda\pi\qquad\Longrightarrow\qquad \boxed{\ \frac{dY}{d\pi}=-\lambda\ }$$

| $\lambda$ | AD curve | $Y$ at $\pi=1\%$ | at 3% | swing | |
|---|---|---|---|---|---|
| **0.00** | $Y=11.0$ | 11.00 | 11.00 | **0.00** | **VERTICAL — no response** |
| 0.25 | $Y=11.0-0.25\pi$ | 10.75 | 10.25 | 0.50 | accommodative |
| **0.50** | $Y=11.0-0.50\pi$ | 10.50 | 9.50 | 1.00 | **Mishkin's case** |
| 1.00 | $Y=11.0-1.00\pi$ | 10.00 | 8.00 | 2.00 | aggressive |
| 2.00 | $Y=11.0-2.00\pi$ | 9.00 | 5.00 | **4.00** | very aggressive |

> [!warning] ⚠️ So the slope of the aggregate demand curve is the central bank's reaction coefficient
> **Mishkin draws AD as a fixed object of the economy. It is nothing of the kind.**
>
> **At $\lambda=0$ the central bank does not respond to inflation at all and *AD is vertical* — inflation has no effect on output.**
>
> **⚠️ And $\lambda<0$ is [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §6's unstable case, arriving in a new costume.** There, simulating $\pi_{t+1}-\pi^*=[1-k(\phi-1)](\pi_t-\pi^*)$ showed the system explodes once the coefficient on inflation drops below one. **Here the same failure appears as an *upward-sloping AD curve*.**
>
> **Mishkin's own chain:** $\pi\uparrow\Rightarrow r\downarrow\Rightarrow Y\uparrow\Rightarrow\pi\uparrow\Rightarrow\cdots$ — **"inflation would keep rising and eventually spin out of control. Indeed, this is exactly what happened in the 1970s."**

> [!warning] ⚠️ The Taylor principle has now appeared three times in this subject, in three costumes
> 1. **as a rule of thumb** — raise nominal rates by more than inflation *([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §5)*;
> 2. **as a stability condition** on a difference equation *(ch. 09 §6)*;
> 3. **as the sign of the slope of aggregate demand** *(here)*.
>
> **Mishkin's own footnote carefully separates the *principle* from the *rule* — and does not note that the principle is what makes his AD curve slope the right way.**

> [!note] And this is where the recorded boundary pays off
> **[[00-Index]] assigns AD–AS to [[Macroeconomics & Microeconomics/contents/14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|Macro/Micro ch. 14]] (M 23 is excluded here).** **But the AD curve *arrives* in this subject, built from monetary machinery.** **Macro/Micro drew it; this subject says where its slope comes from.**

## ✏️ Exercises

**1. (The quantity theory.)** (a) Derive velocity and the equation of exchange. (b) What turns the identity into a theory? (c) Verify the inflation version.

> [!example]- Solution
> **(a) $V=PY/M$, hence $MV=PY$.**
>
> *(Verified: \$10tn of nominal GDP against \$2tn of money gives $V=5$ — the average dollar is spent five times a year.)*
>
> **⚠️ But $MV=PY$ is an *identity*, true by definition.** **It cannot tell you that a rise in $M$ raises $PY$, because the rise might be offset by a fall in $V$.** **An identity constrains; it does not explain.**
>
> **(b) An assumption about velocity.**
>
> **Fisher's: velocity is set by *institutions* — payment technology, credit cards, pay frequency — which change slowly, so $V$ is constant in the short run.** **Then $PY=M\bar V$, and adding flexible prices (so $Y$ sits at full employment) gives $P=M\bar V/\bar Y$.**
>
> *(Verified: doubling $M$ from \$2tn to \$4tn gives $PY=\$20$tn, and $P$ goes from **1.0** to **2.0** — exactly proportional.)*
>
> **⚠️ And note the equivalent statement of Fisher's assumption: $M^d=k\cdot PY$ with $k=1/\bar V$ — money demand depends *only on income*, and interest rates do not enter.** **That is the claim §4 and §5 attack, and everything in the chapter turns on it.**
>
> **(c) $\pi=\%\Delta M-\%\Delta Y$.**
>
> *(Verified: 5% money growth with 3% output growth gives **2%**; 10% gives **7%**.)*
>
> **The derivation uses $\%\Delta(xy)\approx\%\Delta x+\%\Delta y$ and then sets $\%\Delta V=0$.** **⚠️ Both steps are assumptions, and they fail in different places** — the first at high growth rates (exercise 2), the second after 1973 (exercise 4).

**2. (Hard — the approximation.)** (a) What exactly is dropped? (b) How large is the error? (c) Why is the case where it matters most also the theory's best case?

> [!example]- Solution
> **(a) The products of growth rates.**
>
> **Exactly, $(1+g_M)(1+g_V)=(1+\pi)(1+g_Y)$, so $\pi=(1+g_M)(1+g_V)/(1+g_Y)-1$.** **The approximation $\pi\approx g_M+g_V-g_Y$ drops every cross product.**
>
> **(b) Negligible at ordinary rates, enormous at hyperinflation.**
>
> | $g_M$ | $g_Y$ | approx | exact | error |
> |---|---|---|---|---|
> | 5% | +3% | 2.0% | 1.9% | +0.1 |
> | 100% | −5% | 105.0% | **110.5%** | **−5.5** |
> | 1,500% | −10% | 1,510% | **1,678%** | **−168** |
> | **2,000,000%** | −10% | 2,000,010% | **2,222,233%** | **−222,223** |
>
> **At Zimbabwean rates the approximation understates inflation by about 11% of the answer.**
>
> *(Note the sign flips: at low money growth with positive output growth the approximation over-states; with falling output it under-states. **The error is not a bias in one direction, which makes it harder to allow for informally.**)*
>
> **(c) ⚠️ Because hyperinflation is where money growth swamps everything else.**
>
> **The quantity theory's weakest link is the assumption that $V$ is stable and $Y$ is unaffected.** **In a hyperinflation, money growth is so vast that no plausible movement in $V$ or $Y$ could account for the price level — so the theory becomes *unarguable* precisely there.** **Mishkin's Zimbabwe application is chosen for exactly that reason.**
>
> **And that is the same regime in which its standard algebraic form is least accurate.** **The economics is right and the arithmetic is wrong, in the same case.**
>
> **⚠️ Sixth instance of this pattern in the subject** — the Fisher equation, duration, the arithmetic-versus-geometric average, [[07 - Financial Crises|ch. 07]]'s debt deflation, [[10 - Foreign Exchange and the International Financial System|ch. 10]]'s interest parity, and this. **In every case a product of two small quantities is dropped, and in every case the approximation fails exactly where both quantities get large.** **The rule that survives: always ask what the neglected term is proportional to.**

**3. (Hard — Zimbabwe.)** (a) Trace the mechanism. (b) What do the inflation numbers mean concretely? (c) Was the printing raising revenue?

> [!example]- Solution
> **(a) [[07 - Financial Crises|Ch. 07]]'s path B in its purest form.**
>
> **Farms expropriated in 2000 → agricultural output collapses → tax revenue collapses.** **Raising taxes was politically impossible in a depressed economy; borrowing was impossible because nobody trusted the government.** **⇒ only the printing press was left.**
>
> **⚠️ The February 2007 response is the diagnostic moment: the central bank *outlawed price increases*.** **Mishkin: "criminalizing inflation cannot stop inflation when the central bank keeps on printing money."** **The price is a symptom, not the disease** — and price controls under monetary expansion produce shortages rather than stability.
>
> **(b) Prices doubled every three to four weeks.**
>
> | | monthly factor | **doubling time** |
> |---|---|---|
> | Mar 2007: 1,500% | ×1.260 | 91 days |
> | 2008 official: 2,000,000% | ×2.283 | **26 days** |
> | 2008 unofficial: 10,000,000% | ×2.610 | **22 days** |
>
> **A wage negotiated at the start of a month was worth half as much by the end of it.** **⚠️ Which is what makes hyperinflation destructive in a way that the headline number does not convey**: it is not that things are expensive, it is that **no contract denominated in the currency can survive its own term**, so the price system stops carrying information at all *([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §4's first cost of inflation, taken to its limit)*.
>
> *(Hence the \$100 trillion note that "could not even buy you a bottle of beer.")*
>
> **(c) No — and this is the result Mishkin does not draw.**
>
> **[[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] modelled the inflation tax with Cagan money demand and found revenue *peaks at 100% inflation*, falling thereafter because people stop holding money.**
>
> *(So Zimbabwe at 1,500% was **15 times** past the peak; at 2,000,000%, **20,000 times** past it.)*
>
> **⚠️ Past the peak, printing faster collects *less*.** **The government was destroying its currency to obtain a *shrinking* real transfer.**
>
> **That explains something the narrative alone does not: why hyperinflations end, and end abruptly.** **They are not stable equilibria that someone eventually decides to leave — they are self-defeating**, and the revenue that motivated them evaporates. *(Zimbabwe dollarized in 2009, which [[10 - Foreign Exchange and the International Financial System|ch. 10]] §8 identifies as the ultimate commitment device precisely because it cannot easily be reversed.)*

**4. (Hard — money demand.)** (a) Contrast the theories. (b) Is money demand interest-sensitive and stable? (c) What does that settle?

> [!example]- Solution
> **(a) They differ over one function.**
>
> | | money demand | velocity |
> |---|---|---|
> | **Fisher** | $M^d=k\,PY$ — **no interest rate** | constant |
> | **Keynes** | $f(i,Y)$ — transactions, precautionary, **speculative** | not constant |
> | **Baumol–Tobin** | even transactions demand is interest-sensitive | not constant |
> | **Friedman** | permanent income + relative returns | **predictable** |
>
> **Keynes's speculative motive is the wedge: money competes with bonds as a store of wealth, so a higher interest rate raises the opportunity cost of holding money.** **⚠️ And then $V=Y/f(i,Y)$ rises with the interest rate — and since rates are procyclical, *velocity is procyclical*.** **It is not an institutional constant at all.**
>
> **Baumol–Tobin takes the remaining ground**: holding cash to transact also has an opportunity cost, so even the motive Fisher thought was purely mechanical responds to interest rates.
>
> **Friedman's is the interesting middle position.** **He does not claim velocity is *constant* — he claims it is *predictable*, because money's return and other assets' returns move together as banks compete.** **⚠️ That is a much weaker claim, and it is the one that has to survive (b).**
>
> **(b) Sensitive, yes; stable, not since 1973.**
>
> **Sensitivity: "the evidence for the interest sensitivity of the demand for money is remarkably consistent."** **⚠️ And at the zero lower bound it becomes *infinite* — the liquidity trap, where money demand is flat and a change in the money supply moves the interest rate not at all.**
>
> **Stability: "until the early 1970s, the evidence strongly supported the stability of the money demand function. However, after 1973, the rapid pace of financial innovation… led to substantial instability."**
>
> **(c) It settles the last of [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s three criteria — and all three failed.**
>
> | criterion | chapter | verdict |
> |---|---|---|
> | stable measure | [[01 - The Financial System and What Money Is\|ch. 01]] | **FAILED** — forecasts 8 pts apart |
> | controllable $M$ | [[08 - Central Banks and the Money Supply Process\|ch. 08]] | **FAILED** — 1.60 → 0.73 |
> | **stable velocity** | **ch. 11** | **FAILED** — unstable since 1973 |
>
> **⚠️ And the same cause appears twice.** **[[01 - The Financial System and What Money Is|Ch. 01]] blamed *financial innovation* for moving assets across the M1/M2 boundary so the measure stopped meaning the same thing; ch. 11 blames the same innovation for moving the money-demand function so velocity stopped being predictable.** **One historical process broke both the numerator and the relationship it fed — and Mishkin never puts them together.**
>
> **⚠️ Also worth noting the *logic* of the resulting switch.** **Mishkin's argument is not that interest rates are a good instrument** — it is that **"if the money demand function is unstable and so the money supply is not closely linked to aggregate spending, then the level of interest rates set by the Fed will provide *more information* about the stance of monetary policy than will the money supply."** **The interest rate wins by default.** *(Which is the honest reading of [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §8's scoring too: it scored better on all three criteria, but the decisive fact was the other candidate's collapse.)*

**5. (Hard — IS–MP–AD.)** (a) Recover the model. (b) Why does AD slope down? (c) What determines its slope, and what happens if the sign flips?

> [!example]- Solution
> **(a) Three lines, and all nine points reproduce.**
>
> **MP** *(stated)*: $r=1.0+0.5\pi$. **IS** *(recovered — $r$ falls 0.5 pt as $Y$ rises \$0.5tn)*: $Y=12.0-r$. **AD** *(substitution)*: $Y=11.0-0.5\pi$.
>
> | $\pi$ | $r$ | $Y$ |
> |---|---|---|
> | 1.0% | 1.5% | \$10.5tn ✓ |
> | 2.0% | 2.0% | \$10.0tn ✓ |
> | 3.0% | 2.5% | \$9.5tn ✓ |
>
> *(The figure is lost, but as in [[03 - The Behavior of Interest Rates|ch. 03]] the prose names every point — so the model is recoverable rather than merely described.)*
>
> **(b) ⚠️ Because the central bank raises real rates when inflation rises.**
>
> **Not because of a wealth effect, not because of a direct interest-rate effect on spending — those are the textbook AD story elsewhere.** **Here the chain is explicit: MP maps inflation to the real rate; IS maps the real rate to output; AD is their composition.**
>
> **⇒ the central bank is *inside* the aggregate demand curve.** **Without a monetary policy rule there is no AD curve at all** — which is a substantive change from the older presentation in which AD is a property of private behaviour.
>
> **(c) The slope is $-\lambda$, the reaction coefficient — and if it flips, so does stability.**
>
> $$Y=(A-\bar r)-\lambda\pi\quad\Longrightarrow\quad \frac{dY}{d\pi}=-\lambda$$
>
> | $\lambda$ | swing in $Y$ from $\pi=1\%$ to 3% | |
> |---|---|---|
> | **0.00** | **0.00** | **AD is VERTICAL** |
> | 0.50 | 1.00 | Mishkin's case |
> | 2.00 | **4.00** | very aggressive |
>
> **⚠️ So the slope of aggregate demand is a policy choice, not a fact about the economy.** **A more aggressive central bank makes AD steeper; one that ignores inflation makes it vertical.**
>
> **And $\lambda<0$ makes AD slope *upward*, which is [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §6's unstable case in a new costume.** **Mishkin's chain: $\pi\uparrow\Rightarrow r\downarrow\Rightarrow Y\uparrow\Rightarrow\pi\uparrow\Rightarrow\cdots$ — "inflation would keep rising and eventually spin out of control. Indeed, this is exactly what happened in the 1970s."**
>
> **⚠️ So the Taylor principle has now appeared three times in three costumes**: as a rule of thumb ([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §5), as a stability condition on a difference equation (ch. 09 §6), and as the sign of AD's slope (here). **Mishkin's footnote carefully separates the principle from the rule and never observes that the principle is what makes his own AD curve slope the right way.**

## 📝 Summary

- **$MV=PY$ is an IDENTITY** — true by definition. **An assumption about velocity is what turns it into a theory.**
- **Fisher: velocity is institutional and slow-moving, so $V$ is constant** ⇒ $M^d=k\,PY$ ⇒ **money demand depends only on income and interest rates do not enter.** *(Verified: $V=5$; doubling $M$ doubles $P$ from 1.0 to 2.0.)*
- **$\pi=\%\Delta M-\%\Delta Y$** *(verified: 2% and 7%)*.
- **⚠️ SIXTH dropped cross term** *(computed: error **−5.5 pts** at 100% money growth, **−222,223 pts** at 2,000,000%)*. **⚠️ And the quantity theory is most convincing exactly where its algebra is least accurate.**
- **Zimbabwe is [[07 - Financial Crises|ch. 07]]'s path B in pure form** — output collapse → revenue collapse → no taxing, no borrowing → **the printing press.** **Criminalising price increases in Feb 2007 changed nothing.**
- **⚠️ Prices doubled every 26 days officially, 22 unofficially** *(computed)* — **no contract can survive its own term.**
- **⚠️ And Zimbabwe was 20,000 times past the revenue-maximising inflation rate** *(using [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s peak at 100%)* — **so the printing was collecting *less*, which is why hyperinflations end abruptly.**
- **Keynes adds the SPECULATIVE motive** ⇒ $M^d=f(i,Y)$ ⇒ **⚠️ $V$ rises with the interest rate, and since rates are procyclical, velocity is procyclical.**
- **Baumol–Tobin: even *transactions* demand is interest-sensitive. Friedman: velocity is *predictable*, not constant.**
- **⚠️ Nobody disputes the identity — the whole debate is about one function**, and Summary Table 1 lists **seven** determinants where Fisher allowed one.
- **⚠️ CH. 08's DEBT PAID: money demand IS interest-sensitive and HAS been unstable since 1973.** **⇒ velocity is unpredictable.**
- **⚠️ At the ZLB money demand goes FLAT — the liquidity trap** — **which is [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s floor system in a different diagram.** **[[08 - Central Banks and the Money Supply Process|Ch. 08]]'s multiplier, ch. 09's dead OMOs and ch. 11's liquidity trap are one phenomenon described three ways.**
- **⚠️ ALL THREE monetary-targeting criteria are now settled and ALL THREE FAILED** — stable measure ([[01 - The Financial System and What Money Is|ch. 01]]), controllable $M$ ([[08 - Central Banks and the Money Supply Process|ch. 08]]), stable $V$ (here).
- **⚠️ And ONE CAUSE produced two of them: financial innovation broke the *measure* (ch. 01) and the *function* (ch. 11).** **Mishkin never connects them.**
- **The interest rate wins by default** — it "provides more information about the stance of policy", not because it is intrinsically better.
- **⚠️ IS–MP–AD recovered algebraically** *(all nine points reproduce)*: **MP $r=1.0+0.5\pi$, IS $Y=12-r$, AD $Y=11.0-0.5\pi$.**
- **⚠️ AD slopes down because the central bank raises real rates when inflation rises — the central bank is INSIDE the curve.**
- **⚠️ THE SLOPE OF AD IS THE REACTION COEFFICIENT $\lambda$.** **At $\lambda=0$ AD is vertical; at $\lambda<0$ it slopes upward and the system explodes** — [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §6's instability in a new costume.
- **⚠️ The Taylor principle has now appeared three times in three costumes**: a rule of thumb, a stability condition, and the sign of AD's slope.

## ⚠️ Important Notes

1. **⚠️ $MV=PY$ explains nothing by itself.** Every use of it smuggles in an assumption about $V$.
2. **Fisher's real claim is that interest rates do not affect money demand.** Everything else follows.
3. **⚠️ $\pi=\%\Delta M-\%\Delta Y$ is an approximation twice over** — dropped cross terms, and $\%\Delta V=0$.
4. **The cross-term error is not one-signed** — it over-states at low growth and under-states when output falls.
5. **⚠️ Hyperinflation is the theory's best case and the algebra's worst.**
6. **Price controls under monetary expansion produce shortages, not stability.**
7. **⚠️ Hyperinflation destroys contracts, not just savings** — nothing survives its own term.
8. **⚠️ Past 100% inflation, printing faster collects less.** That is why hyperinflations end abruptly.
9. **Keynes's speculative motive is the wedge** that makes velocity a variable.
10. **⚠️ Velocity is procyclical**, because interest rates are.
11. **Friedman claims predictability, not constancy** — a weaker and more defensible position.
12. **⚠️ The liquidity trap is flat money demand**, and it is the same flatness as ch. 09's floor system.
13. **⚠️ All three monetary-targeting criteria failed**, and the subject has now computed each.
14. **One cause — financial innovation — broke two of the three.**
15. **⚠️ AD has no existence without a monetary policy rule.**
16. **⚠️ The slope of AD is a policy choice, not a fact about the economy.**
17. **$\lambda<0$ gives an upward-sloping AD and an explosive economy.**
18. **⚠️ The same result can look like a rule, a stability condition, or a slope.** Recognise it in all three forms.

> [!warning] Gaps in the source material
> **Three chapters compressed into one note. Extraction was good for prose and for both summary tables.**
>
> **⚠️ SUMMARY TABLE 1 (seven determinants of money demand, with directions and reasons) and ch. 21's SUMMARY TABLE 1 (IS-curve shift factors) both survived complete.** **Ninth confirmation of the vault's rule.**
>
> **All figures are lost, and the losses split the usual two ways.**
> - **⚠️ Data series — real losses.** **Figure 1** (inflation against money growth, ten-year averages and cross-country) and **Figure 2** (annual US inflation and money growth, 1965–2016) are **the empirical case for the quantity theory**, and ch. 21's **Figure 3** (the Vietnam War buildup). **Their conclusions are retained on Mishkin's authority — the long-run relationship holds, the short-run one is weak — and no series is reconstructed.**
> - **⚠️ Analytical diagrams — mostly recovered.** The IS, MP and AD panels have no numbers on their axes, **but the prose names every point of the three-panel derivation (Figure 4)**, so §6 rebuilds all three curves algebraically and **all nine points reproduce.** *(This is [[03 - The Behavior of Interest Rates|ch. 03]]'s recovery working for a fourth time, and it is why that rule is worth keeping: check the prose before recording a figure as lost.)*
>
> **No erratum and no discrepancy.** **Every stated figure reproduces** — velocity of 5, the doubled price level, both inflation examples, the MP curve at three points, and the nine points of the AD derivation.
>
> **⚠️ SCOPE NOTE — three chapters in one note, so the compression is heavy.** **Deliberately reduced:** the **full derivation of the IS curve** from planned expenditure (consumption function, the multiplier, the *FYI* on the meaning of "investment") — **[[Macroeconomics & Microeconomics/contents/13 - Open-Economy Macroeconomics|Macro/Micro ch. 13]] owns the expenditure multiplier per [[00-Index]]'s boundary**, and it is cross-linked rather than repeated; the **Vietnam War and 2009 stimulus applications**, which illustrate IS shifts without adding to the mechanism; the detailed catalogue of IS-shift factors *(retained as Summary Table 1's content)*; and the **algebraic AD appendix**, which §6 supersedes by recovering the model from the prose. **Ch. 23's AD–AS analysis is excluded from this subject entirely — [[Macroeconomics & Microeconomics/contents/14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|Macro/Micro ch. 14]] owns it.**
>
> **Additions beyond the source.**
>
> - **⚠️ §5 is the note's principal obligation and it discharges [[08 - Central Banks and the Money Supply Process|ch. 08]]'s deferral.** **Mishkin reports the two empirical findings — interest sensitivity and post-1973 instability — in a short section and draws the policy conclusion.** **Assembling them into the third row of [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s criteria table, so that all three conditions for monetary targeting are seen to have failed with a computed verdict attached to each, is my synthesis.** **So is the observation that *financial innovation* is the common cause of [[01 - The Financial System and What Money Is|ch. 01]]'s measurement failure and ch. 11's stability failure** — **one historical process breaking both the numerator and the relationship it fed, which Mishkin never connects.**
> - **⚠️ §7 is the note's best analytical addition.** **Mishkin gives the MP curve with numbers, derives AD graphically, and treats the resulting curve as an object.** **Writing $Y=(A-\bar r)-\lambda\pi$ shows the slope *is* the policy coefficient** — so AD is vertical at $\lambda=0$ and upward-sloping at $\lambda<0$. **The identification of that last case with [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §6's simulated instability, and of the Taylor principle appearing three times in three costumes, is mine.**
> - **⚠️ §2's error table is mine.** **Mishkin writes "approximately" and moves on.** **Computing the error at hyperinflation rates gives the sixth instance of the subject's cross-term pattern — and the observation that the theory's best case is its algebra's worst case is the part worth keeping.**
> - **⚠️ §3's doubling times and the inflation-tax comparison are mine.** **Mishkin gives the inflation rates and the \$100 trillion note as colour.** **Converting them to a 26-day doubling time says what the number *means*; and comparing against [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s computed revenue peak at 100% shows Zimbabwe was 20,000 times past it — which explains why hyperinflations self-terminate**, a fact his narrative reports without accounting for.
> - **§4's observation that velocity is *procyclical* under Keynes, and that the entire Fisher–Keynes–Friedman debate is about one function rather than about the identity, is mine.**
> - **§5's identification of the liquidity trap with [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s floor system and [[08 - Central Banks and the Money Supply Process|ch. 08]]'s collapsed multiplier — one phenomenon, three descriptions — is my synthesis.**

**Previous:** [[10 - Foreign Exchange and the International Financial System]] · **Next:** [[12 - Monetary Policy Theory, Expectations and Transmission]]
