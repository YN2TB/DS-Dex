---
subject: Monetary and Financial Theories
chapter: 9
tags: [ds, economics, monetary-policy, taylor-rule, inflation-targeting, zero-lower-bound, time-inconsistency, federal-funds-rate]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 16–17"
---

# Tools and Conduct of Monetary Policy

**[[03 - The Behavior of Interest Rates|Ch. 03]] §7 showed the interest-rate *level* does not measure the policy stance. [[08 - Central Banks and the Money Supply Process|Ch. 08]] showed the central bank controls the base but not $M$.** **This chapter needs different apparatus than either — and gets it.**

**Four results.**

**§1 — ⚠️ the market for reserves is a *corridor*, and there is an exact condition under which open market operations stop working entirely.** *(Modelled: once nonborrowed reserves exceed the quantity demanded at the floor, **the funds rate is pinned at $i_{or}$ and adding \$1,700bn of reserves changes it by zero.**)* **That is the post-2008 world — and it is [[08 - Central Banks and the Money Supply Process|ch. 08]]'s collapsed multiplier seen from the other side.**

**§6 — ⚠️ THE TAYLOR PRINCIPLE IS A STABILITY CONDITION, not a rule of thumb.** *(Simulated: at $\phi=1.5$ an inflation shock decays; at $\phi=1.0$ it **never goes away**; below 1 it **grows without limit**.)* **Mishkin says "serious instability then results" and does not show it. It is a one-line dynamic system.**

**§7 — the reason not to automate the rule undercuts it from inside.** **Nobody observes the output gap** — so two economists with the same rule and different potential-output estimates get different answers, **and neither can be checked in real time.**

**§8 — why the world switched from aggregates to interest rates.** **It is not fashion: it is one of three instrument criteria failing, and [[01 - The Financial System and What Money Is|ch. 01]] and [[08 - Central Banks and the Money Supply Process|ch. 08]] are the two halves of the evidence.**

## 📘 Main Knowledge

### 1. ⚠️ The market for reserves — a corridor, not a curve

**[[03 - The Behavior of Interest Rates|Ch. 03]]'s supply-and-demand apparatus applied to *reserves*; the price is the federal funds rate $i_{ff}$.** **But both curves have a flat segment, and that is the whole modern story.**

| curve | shape | why |
|---|---|---|
| **demand $R^d$** | slopes down while $i_{ff}>i_{or}$, **then FLAT at $i_{or}$** | the opportunity cost of holding reserves is $i_{ff}-i_{or}$; **no bank lends overnight below what the Fed pays it**, so it piles up excess reserves indefinitely ⇒ **$i_{or}$ is a FLOOR** |
| **supply $R^s$** | vertical at $NBR$ while $i_{ff}<i_d$, **then FLAT at $i_d$** | nobody borrows from the Fed when the market is cheaper; **above $i_d$ banks borrow at $i_d$ and lend at $i_{ff}$ without limit** ⇒ **$i_d$ is a CEILING** |

$$\boxed{\ i_{or}\ \le\ i_{ff}\ \le\ i_d\ }$$

> [!note] The Fed does not set the funds rate directly
> **It sets a *corridor* and lets the market clear inside it.** **Both standing facilities are set at a fixed spread to the target, so the whole corridor moves when the target moves.**

*(Modelled — floor $i_{or}=0.25\%$, ceiling $i_d=0.75\%$. **The numbers are mine; the structure is Mishkin's.**)*

| nonborrowed reserves | funds rate | regime |
|---|---|---|
| 500 | **0.75%** | **CEILING** — discount window caps it |
| 700 | 0.50% | interior — OMOs move the rate |
| 799 | 0.25% | interior |
| **800** | **0.25%** | **FLOOR — OMOs do nothing** |
| 1,500 | **0.25%** | FLOOR |
| **2,600** | **0.25%** | **FLOOR** |

> [!warning] ⚠️ Once reserves are abundant, open market operations have no effect at all
> **Adding \$1,700bn of reserves changes the funds rate by zero.**
>
> **That is exactly the post-2008 world — and [[08 - Central Banks and the Money Supply Process|ch. 08]] measured it: the excess-reserves ratio went from below 0.001 to 1.5625.**
>
> **⚠️ So ch. 08's collapsed multiplier and this chapter's dead open market operations are the same fact seen from two sides: *reserves stopped being scarce*.**
>
> **And it explains why the interest paid *on* reserves became the instrument.** **In a floor system the Fed sets the rate by *announcement* — changing $i_{or}$ — rather than by trading.** **⇒ the *quantity* of reserves is then free to be used for something else, which is what made QE possible.**

### 2. The three conventional tools — and why only one is used

| tool | verdict |
|---|---|
| **open market operations** | **complete control** over volume, **flexible and precise**, easily reversed, implemented quickly — **the dominant tool, until §1's floor regime** |
| **discount policy** | **its unique value is not rate-setting** — it is the **lender of last resort** |
| **reserve requirements** | **barely used** |

> [!warning] ⚠️ Discount policy exists for ch. 07's stage two
> **A lender of last resort lets a *solvent* bank borrow against good collateral instead of dumping it into a fire sale.** *(**[[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]] computed the cascade it prevents**: 9.82% equity, every asset performing, zero defaults, **insolvent at 48.5% withdrawals**.)*
>
> **The cost is moral hazard** — [[06 - Asymmetric Information and Financial Structure|ch. 06]] again, and [[07 - Financial Crises|ch. 07]]'s safety-net point. **A bank expecting rescue takes more risk.** **Which is why the discount rate is a *penalty* rate above target: you may borrow, but not cheaply.**

**Reserve requirements are blunt** *(a small change in $rr$ moves deposits enormously — [[08 - Central Banks and the Money Supply Process|ch. 08]]'s multiplier)*, **disruptive to liquidity management, and a tax on banks.** **Several central banks have abolished them.**

> [!note] ⚠️ So of three "tools", one is for crises, one is obsolete, and the third stopped working when reserves became abundant
> **That is why §3 exists.**

### 3. Nonconventional tools — at the zero lower bound

**When $i_{ff}$ is at or near zero it cannot be cut further.**

| tool | mechanism |
|---|---|
| **liquidity provision** | new facilities, wider collateral, wider counterparties — **discount policy generalised** |
| **large-scale asset purchases (QE)** | buy long bonds and MBS to push down **long** rates when the short rate is stuck |
| **⚠️ forward guidance** | **promise to keep rates low — works only through expectations** |
| **negative interest rates** | on reserves, to push banks to lend |

> [!warning] ⚠️ Forward guidance is a time-inconsistent promise, and that is the whole difficulty
> **A central bank saying "we will keep rates low even after inflation rises" is promising to do something it will not *want* to do when the time comes.** *(§4's time-inconsistency problem, applied to the bank's own announcement.)*
>
> **⇒ credibility is the binding constraint, and it is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s rational expectations doing the work**: the promise moves the economy only insofar as people believe it, and they believe it only if the bank has not reneged before.

> [!warning] ⚠️ And note what QE does *not* do
> **[[08 - Central Banks and the Money Supply Process|Ch. 08]]: QE raised the base 350% and M1 about 105%, because banks held the reserves.** **⇒ asset purchases work through *asset prices and term premia* ([[04 - The Risk and Term Structure of Interest Rates|ch. 04]]), not through the money multiplier.** **Judging QE by monetary aggregates misreads what it is.**

*(Negative rates are no longer hypothetical — [[02 - The Meaning of Interest Rates|ch. 02]]'s Global box records them in Japan, the US, Sweden, Denmark, the Eurozone and Switzerland.)*

### 4. Goals, the nominal anchor, and time inconsistency

**Six goals**: **price stability**, high employment and output, economic growth, financial-market stability, interest-rate stability, foreign-exchange stability. **Price stability is increasingly treated as primary.**

> [!note] Why inflation is costly — Mishkin's list
> **It degrades the information in a price** (relative prices become hard to read); **it makes planning hard**; and **it strains the social fabric** as groups compete to keep their incomes up. *([[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] computed the costs — shoeleather, menu, tax distortions, arbitrary redistribution — and [[02 - The Meaning of Interest Rates|ch. 02]] added the after-tax wedge $i\cdot t$ that grows with inflation. **Cross-linked, not re-derived.**)*

**A *nominal anchor* is a nominal variable tied down to pin the price level.** **Its subtler job is to limit the time-inconsistency problem.**

> [!warning] ⚠️ The time-inconsistency problem
> **A discretionary expansion raises output in the *short* run. But wage- and price-setters *anticipate* it and raise their expectations. So the long-run result is higher inflation with no extra output.**
>
> **⚠️ The structure is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s rational expectations exactly: you cannot systematically fool people who are forecasting you.** **A policy that works *once* stops working once it is *expected*.**
>
> **And the deep point: the central bank does not have to *want* to inflate.** **Knowing that it *would* be tempted is enough for the public to expect inflation — so the bad outcome arrives without anyone acting.** **⇒ that is why a *rule* beats *discretion* here: it removes the temptation rather than resisting it.**
>
> *(Mishkin's analogy is a parenting manual: a parent who gives in to a tantrum teaches the child to throw tantrums. **The solution is a rule announced in advance, which is what a nominal anchor is.**)*

### 5. ⚠️ The Taylor rule

$$i_{ff}^{\text{target}}=\pi+r^*+a(\pi-\pi^*)+b\cdot(\text{output gap})$$

**Taylor's values: $r^*=2\%$, $\pi^*=2\%$, $a=b=\tfrac12$.**

*(Verified — inflation 3%, output 1% above potential:)*
$$3+2+\tfrac12(1)+\tfrac12(1)=\mathbf{6.00\%}\ ✓$$

*(Computed across states:)*

| inflation | output gap | funds-rate target | **implied REAL rate** |
|---|---|---|---|
| 2% | 0% | 4.00% | **2.00%** |
| 3% | 1% | 6.00% | 3.00% |
| 1% | −2% | 1.50% | **0.50%** |
| **0%** | **−4%** | **−1.00%** | **−1.00%** |
| 5% | 2% | 9.50% | 4.50% |
| **−1%** | **−6%** | **−3.50%** | −2.50% |

> [!note] ⚠️ Read the last column — the rule is a formula for the REAL stance
> **The prescribed real rate is $r^*+a(\pi-\pi^*)+b\cdot y$, which falls below 2% exactly when inflation is below target or output below potential.** **The nominal number is an output, not the object.**
>
> **And the bottom rows are the zero lower bound**: **the rule asks for a negative nominal rate**, which is precisely why §3 exists.

### 6. ⚠️ The Taylor principle as a stability condition

**Written generally, $i=c+\phi\pi+b\cdot y$, Taylor's rule has $\phi=1+a=1.5$.** **The *Taylor principle* is $\phi>1$: raise the nominal rate by *more* than inflation rises.**

**Mishkin states the consequence in words — "serious instability then results" — and does not show it. It is a one-line dynamic system:**

$$r=i-\pi=c+(\phi-1)\pi+b\,y\qquad\Rightarrow\qquad \frac{dr}{d\pi}=\phi-1$$
$$\pi_{t+1}-\pi^*=\big[1-k(\phi-1)\big](\pi_t-\pi^*)$$

*(Simulated — a 1-point inflation shock above a 2% target, $k=0.5$:)*

| $\phi$ | $dr/d\pi$ | factor | path | |
|---|---|---|---|---|
| **1.50** | +0.50 | 0.750 | 3.00, 2.75, 2.56, 2.42, 2.32, 2.24, … | **converges** |
| 1.30 | +0.30 | 0.850 | 3.00, 2.85, 2.72, 2.61, … | converges |
| **1.00** | **0.00** | **1.000** | **3.00, 3.00, 3.00, 3.00, …** | **DRIFTS** |
| **0.90** | −0.10 | 1.050 | 3.00, 3.05, 3.10, 3.16, 3.22, … | **EXPLODES** |
| **0.80** | **−0.20** | 1.100 | **3.00, 3.10, 3.21, 3.33, 3.46, 3.61, 3.77, 3.95, 4.14** | **EXPLODES** |

> [!warning] ⚠️ The principle is the condition for the equilibrium to exist
> **At $\phi=1.5$ the shock decays. At $\phi=1.0$ it never goes away. Below 1 it grows without limit.**
>
> **The mechanism is visible in column 2: when $\phi<1$, a *rise* in inflation *lowers* the real interest rate — which is a monetary *easing* — which raises inflation further.**
>
> **⚠️ So "the Fed raised rates in the 1970s" is not a defence. It raised them by *less than inflation rose*, which is an easing.** **That is Mishkin's account of the Great Inflation, and it is [[02 - The Meaning of Interest Rates|ch. 02]]'s real-versus-nominal distinction deciding a decade of policy.**
>
> *(Compare ch. 02 directly: **"US nominal rates were high in the 1970s while real rates were often negative."** **The Taylor principle is the policy rule that would have prevented that, stated in ch. 02's own units.**)*

### 7. Why not put the rule on autopilot?

| objection | |
|---|---|
| **1. nobody knows the output gap** | potential output is **estimated, not observed**, and heavily revised after the fact |
| 2. the coefficients are not constants | the economy changes |
| **3. policy is forward-looking** | it acts with **long and variable lags**, so a rule using *current* data uses the wrong information set |
| 4. crises change the mapping | when credit spreads blow out *([[04 - The Risk and Term Structure of Interest Rates|ch. 04]]: +360 bp)*, the same funds rate transmits differently |

> [!warning] ⚠️ Objection 1 undercuts the rule from inside
> **Two economists using the same rule and different potential-output estimates get different answers, and neither can be checked in real time.**
>
> **⇒ that is [[01 - The Financial System and What Money Is|ch. 01]]'s measurement-boundary result once more: a policy built on a measure inherits the judgement in the measure.** *(GDP and the CPI; the unemployment rate; which M?; which leg?; flows or stocks?; and now **the output gap**.)*

> [!note] The correct use — which the FOMC actually makes
> **The rule is a *benchmark*, not an instruction.** **If your proposed setting is far from it, you should be able to say why.** **In the 1970s there was no good answer.**
>
> *(Mishkin's own summary: monetary policy "is as much an art as it is a science". **The rule leaves out all of the art — which is both its weakness and exactly what makes it a useful check on judgement.**)*

### 8. Inflation targeting, and the linkage chain

**Inflation targeting = a public numerical target + an institutional commitment to price stability as the primary goal + an information-inclusive approach + heavy transparency + accountability.**

| advantages | disadvantages |
|---|---|
| **does not depend on a stable money-demand relationship** | **signals are delayed** — inflation responds with long lags |
| readily understood by the public | can be **too rigid** |
| **reduces time inconsistency** by making the commitment public and checkable | may permit too much output volatility |

> [!warning] ⚠️ The first advantage is exactly what ch. 08 showed had failed
> **[[08 - Central Banks and the Money Supply Process|Ch. 08]] found the multiplier collapsed from 1.60 to 0.73 *and* velocity fell 29%.** **Inflation targeting sidesteps both by targeting the goal directly rather than an intermediate aggregate.**
>
> *(Which is why nobody practises **strict** targeting. The term of art is **flexible inflation targeting** — a target, plus discretion about the horizon over which to return to it.)*

**The linkage chain:**

$$\textbf{TOOLS}\to\textbf{POLICY INSTRUMENTS}\to\textbf{INTERMEDIATE TARGETS}\to\textbf{GOALS}$$

*(OMOs, discount policy, reserve requirements, $i_{or}$ → the federal funds rate → monetary aggregates or long rates → price stability, high employment.)*

**Three criteria for choosing an instrument: *measurability*, *controllability*, and *a predictable effect on goals*.** *(Mishkin's test of the third is memorable: **a central bank could set the price of tea in China and control it completely — what good would that do?**)*

> [!warning] ⚠️ Scoring the candidates with the vault's own results
> | | measurability | controllability | **predictable effect** |
> |---|---|---|---|
> | **reserve aggregates** | **poor** *([[01 - The Financial System and What Money Is|ch. 01]]: which M?)* | good | **FAILED** *([[08 - Central Banks and the Money Supply Process|ch. 08]]: 1.60 → 0.73)* |
> | **short-term interest rate** | **excellent** — observed continuously | **excellent** *(§1, inside the corridor)* | imperfect but better |
>
> **⇒ the worldwide switch from aggregates to interest rates is not fashion. It is criterion 3 failing for one candidate — and [[01 - The Financial System and What Money Is|ch. 01]] and [[08 - Central Banks and the Money Supply Process|ch. 08]] are the two halves of the evidence.**

## ✏️ Exercises

**1. (Hard — the corridor.)** (a) Why does each curve have a flat segment? (b) When do open market operations stop working? (c) What does that imply?

> [!example]- Solution
> **(a) Because each flat segment is a *standing facility* offering an unlimited quantity at a fixed price.**
>
> **Demand goes flat at $i_{or}$**: the opportunity cost of holding reserves is $i_{ff}-i_{or}$, so as $i_{ff}$ falls the quantity demanded rises. **But no bank will lend overnight *below* what the Fed pays it to do nothing — so at $i_{ff}=i_{or}$ demand becomes infinitely elastic.** ⇒ **$i_{or}$ is a floor.**
>
> **Supply is vertical at $NBR$ while $i_{ff}<i_d$** (nobody borrows from the Fed when the market is cheaper), **and goes flat at $i_d$**: above the discount rate, banks borrow at $i_d$ and lend at $i_{ff}$ without limit. ⇒ **$i_d$ is a ceiling.**
>
> **⇒ $i_{or}\le i_{ff}\le i_d$. The Fed sets a *corridor* and lets the market clear inside it**, and since both facilities sit at fixed spreads to the target, the whole corridor moves together.
>
> **(b) Once nonborrowed reserves exceed the quantity demanded at the floor.**
>
> *(Modelled with $i_{or}=0.25\%$, $i_d=0.75\%$: at $NBR=799$ the rate is 0.25%; at 800, 1,500 and 2,600 it is **0.25% at every level**.)* **Adding \$1,700bn changes the rate by zero.**
>
> **The equilibrium has moved onto the flat part of the demand curve, where quantity is irrelevant to price.**
>
> **(c) That reserves stopped being scarce — which is ch. 08's finding restated.**
>
> **[[08 - Central Banks and the Money Supply Process|Ch. 08]] measured the excess-reserves ratio going from below 0.001 to 1.5625.** **⚠️ That collapsed multiplier and these dead open market operations are the *same fact* seen from two sides.**
>
> **Three consequences.**
> - **The instrument changes.** In a floor system the Fed sets the rate **by announcement** — changing $i_{or}$ — not by trading.
> - **⚠️ The *quantity* of reserves is thereby freed for other uses**, which is precisely what made QE possible: the balance sheet could quintuple without disturbing the policy rate.
> - **And the textbook mechanism is suspended.** "The Fed buys bonds, reserves rise, the funds rate falls" is true only in the scarce-reserve regime, **and nothing in the sentence says so.**

**2. (Tools.)** (a) Why are open market operations the preferred conventional tool? (b) What is discount policy actually for? (c) Why are reserve requirements barely used?

> [!example]- Solution
> **(a) Control, precision, reversibility, speed.**
>
> **The Fed has complete control over the volume; operations can be any size in either direction; they are easily reversed if a mistake is made; and they are implemented quickly with no administrative delay.** **No other tool has all four.**
>
> *(But §1 is the qualification: these advantages are about the **instrument**, and an instrument with perfect properties is useless if the transmission has gone flat.)*
>
> **(b) Being the lender of last resort.**
>
> **Its value is not rate-setting.** **[[07 - Financial Crises|Ch. 07]]'s stage two is a bank panic driven by fire sales, and a lender of last resort lets a *solvent* bank borrow against good collateral instead of dumping it.**
>
> **[[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]] computed exactly what this prevents: a bank with 9.82% equity, every asset performing and *zero defaults*, went insolvent at 48.5% withdrawals.** **⚠️ The run created the insolvency; a discount window breaks the loop by removing the need to sell.**
>
> **The cost is moral hazard** *([[06 - Asymmetric Information and Financial Structure|ch. 06]], and [[07 - Financial Crises|ch. 07]]'s finding that the safety net is part of stage *one* as well as the cure for stage two)*. **Which is why the discount rate is a *penalty* rate set above target: the facility must be available but unattractive.**
>
> **(c) Because they are blunt, disruptive and a tax.**
>
> **Blunt:** [[08 - Central Banks and the Money Supply Process|ch. 08]]'s multiplier shows a small change in $rr$ moves deposits enormously — there is no fine-tuning available.
> **Disruptive:** a bank that suddenly must hold more reserves has a liquidity problem it did not plan for.
> **A tax:** required reserves earning nothing are a levy on deposit-taking, which pushes activity toward institutions that do not take deposits — **[[07 - Financial Crises|ch. 07]]'s shadow banking system, and its point that safety nets attach to funding forms rather than functions.**
>
> **⇒ several central banks have abolished them.** **⚠️ So of three "tools", one is for crises, one is obsolete, and the third stopped working when reserves became abundant** — which is why nonconventional tools are not an emergency footnote but the main sequence.

**3. (Hard — the Taylor rule and principle.)** (a) Verify the rule. (b) Show the Taylor principle is a stability condition. (c) What does it say about the 1970s?

> [!example]- Solution
> **(a) 6.00%.**
>
> $$i=\pi+r^*+\tfrac12(\pi-\pi^*)+\tfrac12 y=3+2+\tfrac12(1)+\tfrac12(1)=\mathbf{6.00\%}\ ✓$$
>
> **⚠️ And the rule is really a formula for the *real* stance**: the implied real rate is $r^*+a(\pi-\pi^*)+by$, which falls below $r^*$ exactly when inflation is below target or output below potential. *(Computed: at $\pi=1\%$, $y=-2\%$ the rule asks for a nominal 1.50% and a **real 0.50%**; at $\pi=0\%$, $y=-4\%$ it asks for a **negative nominal rate** — which is §3's zero lower bound arriving as an arithmetic fact rather than a special case.)*
>
> **(b) Because the sign of the real-rate response is $\phi-1$.**
>
> **Write the rule as $i=c+\phi\pi+by$, so Taylor's version has $\phi=1+a=1.5$.** Then
> $$r=i-\pi=c+(\phi-1)\pi+by\qquad\Rightarrow\qquad\frac{dr}{d\pi}=\phi-1$$
> **and inflation responding to the real-rate gap gives $\pi_{t+1}-\pi^*=[1-k(\phi-1)](\pi_t-\pi^*)$.**
>
> | $\phi$ | $dr/d\pi$ | factor | outcome |
> |---|---|---|---|
> | **1.5** | +0.50 | 0.750 | **converges** |
> | **1.0** | 0.00 | 1.000 | **drifts — never returns** |
> | **0.8** | **−0.20** | 1.100 | **explodes: 3.00 → 4.14 in eight periods** |
>
> **⚠️ So the principle is not a rule of thumb — it is the condition for the equilibrium to exist.** **Below $\phi=1$, a rise in inflation *lowers* the real rate, which is an easing, which raises inflation further.** **The system has no resting point.**
>
> **(c) That "the Fed raised rates" is not a defence.**
>
> **⚠️ It raised them by *less than inflation rose*, which is an easing.** **The nominal rate went up and the real rate went down.**
>
> **This is [[02 - The Meaning of Interest Rates|ch. 02]]'s real-versus-nominal distinction deciding a decade of policy** — and ch. 02 recorded the fact independently: **"US nominal rates were high in the 1970s while real rates were often negative."** **The Taylor principle is the rule that would have prevented it, stated in ch. 02's own units.**
>
> *(And it explains why Mishkin's Figure 5 shows the rule describing Fed behaviour well **after 1987 and badly during the 1970s**: the rule is not merely a poor *description* of that period, it is a statement of what was being done wrong.)*

**4. (Goals and time inconsistency.)** (a) Why is price stability primary? (b) State the time-inconsistency problem. (c) Why does it not require a dishonest central bank?

> [!example]- Solution
> **(a) Because inflation degrades the price system itself.**
>
> **Mishkin's three costs: relative prices become hard to read, so the *information* in a price is degraded; planning becomes hard; and inflation strains the social fabric as groups compete to keep their incomes up.** *(Cross-linked rather than re-derived: [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] computed shoeleather, menu, tax-distortion and redistribution costs, and [[02 - The Meaning of Interest Rates|ch. 02]] added the after-tax wedge $i\cdot t$ that widens with inflation at an unchanged statutory rate.)*
>
> **The first cost is the deepest and is easy to miss.** **A price is a signal about relative scarcity; general inflation adds noise to every signal at once**, so the whole allocation mechanism works worse. **That is a cost even for someone whose income keeps pace perfectly.**
>
> **(b) Discretionary expansion buys short-run output and delivers long-run inflation with no output gain.**
>
> **The bank is tempted to expand because output rises in the short run. But wages and prices are set on *expectations* of policy. When people expect expansion, they raise wages and prices immediately** — so the price level rises and output does not.
>
> **⚠️ The structure is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s rational expectations exactly: you cannot systematically fool people who are forecasting you.** **A policy that works *once* stops working once it is *expected*** — which is also ch. 05's implication 1, that changing how a variable moves changes how expectations of it are formed.
>
> **(c) Because being *tempted* is enough.**
>
> **⚠️ The central bank does not have to want to inflate, or intend to, or ever actually do it.** **If the public knows the bank *would* be tempted — and would face political pressure to give in — they will expect inflation and set wages accordingly.** **The bad outcome then arrives with nobody having acted.**
>
> **⇒ that is why a *rule* beats *discretion* here, and the reason is unusual: the rule's value is not that it produces better decisions, but that it *removes the temptation* rather than requiring anyone to resist it.**
>
> *(Mishkin's analogy is a parenting manual — a parent who gives in to a tantrum teaches the child to throw tantrums, and the fix is a rule announced in advance. **A nominal anchor is that rule**, and it is why §8's inflation target is *public and numerical*: a private intention cannot do the job, because the mechanism runs entirely through what other people believe.)*
>
> **And this is exactly why §3's forward guidance is hard.** **"We will keep rates low even after inflation rises" is a promise to do something the bank will not want to do when the time comes** — a time-inconsistent promise, so it moves the economy only to the extent that the bank's past behaviour makes it credible.

**5. (Strategy.)** (a) What is inflation targeting and what does it avoid? (b) Give the linkage chain and the three criteria. (c) Why did the world switch from aggregates to interest rates?

> [!example]- Solution
> **(a) A public numerical target with transparency and accountability — and it avoids depending on money demand.**
>
> **Five elements: a public numerical target; an institutional commitment to price stability as the *primary* goal; an information-inclusive approach; heavy transparency; accountability.**
>
> **⚠️ Its central advantage is that it does not require a stable money-demand relationship — which is exactly the assumption [[08 - Central Banks and the Money Supply Process|ch. 08]] showed had failed**, twice over: **the multiplier collapsed from 1.60 to 0.73 and velocity fell 29% over the decade.** **Targeting the goal directly sidesteps both.**
>
> **It also attacks §4's time-inconsistency problem structurally**: a public, numerical, checkable commitment is harder to abandon quietly than a private intention.
>
> **The disadvantages are real: signals are delayed (inflation responds with long lags, so you learn you were wrong late); it can be too rigid; and it may permit excessive output volatility.** **⇒ nobody practises *strict* targeting — the term of art is *flexible* inflation targeting**, a target plus discretion over the horizon for returning to it.
>
> **(b) Tools → instruments → intermediate targets → goals; measurability, controllability, predictable effect.**
>
> $$\text{OMOs, discount policy, }rr,\ i_{or}\ \to\ \text{federal funds rate}\ \to\ \text{aggregates / long rates}\ \to\ \text{price stability, employment}$$
>
> **The three criteria apply to the choice of instrument, and the third is the one that bites.** *(Mishkin's test: **a central bank could set the price of tea in China and control it perfectly — what good would that do?** **Controllability without a link to the goal is worthless.**)*
>
> **(c) Because criterion 3 failed for aggregates, and this vault has both halves of the evidence.**
>
> | | measurability | controllability | **predictable effect** |
> |---|---|---|---|
> | **reserve aggregates** | **poor** | good | **FAILED** |
> | **short rate** | excellent | excellent | imperfect but better |
>
> - **Measurability fails first**: [[01 - The Financial System and What Money Is|ch. 01]]'s *which M?* — feeding M1 versus M2 into the quantity theory gave inflation forecasts **8 points apart from the same economy**.
> - **Controllability fails next**: [[08 - Central Banks and the Money Supply Process|ch. 08]] — the central bank sets the base precisely and does not set $M$, because $m=(1+c)/(rr+e+c)$ belongs to three players.
> - **And the predictable effect fails last**: the multiplier went from 1.60 to 0.73 while velocity fell 29%.
>
> **⚠️ So the switch is not fashion and not ideology. It is a measured failure of a specific criterion**, and the interest rate wins not because it is a good instrument in the abstract but because it is **observed continuously** and **controllable inside §1's corridor**.
>
> *(With the honest caveat that §1 supplies: even that controllability is regime-dependent. **In a floor system the Fed controls the rate by announcement rather than by trading** — a different mechanism wearing the same name.)*

## 📝 Summary

- **⚠️ The market for reserves is a *corridor*: $i_{or}\le i_{ff}\le i_d$.** **Demand goes flat at the interest paid on reserves (a floor); supply goes flat at the discount rate (a ceiling).** **The Fed sets the corridor, not the rate.**
- **⚠️ Once reserves are abundant, open market operations have *no effect at all*** *(modelled: adding \$1,700bn moves the rate by zero)* — **and that is [[08 - Central Banks and the Money Supply Process|ch. 08]]'s collapsed multiplier seen from the other side. Reserves stopped being scarce.**
- **⇒ in a floor system the rate is set by *announcement*, freeing the quantity of reserves for QE.**
- **Three conventional tools: OMOs (control, precision, reversibility, speed), discount policy (**lender of last resort**), reserve requirements (**blunt, disruptive, a tax — barely used**).**
- **⚠️ Discount policy exists for [[07 - Financial Crises|ch. 07]]'s stage two** — it lets a *solvent* bank borrow instead of fire-selling. **[[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]] computed what it prevents: insolvency at 48.5% withdrawals with zero defaults.** **The cost is moral hazard; hence a penalty rate.**
- **Nonconventional tools at the zero lower bound**: liquidity provision, **QE**, **forward guidance**, negative rates.
- **⚠️ Forward guidance is a time-inconsistent promise** — it works only through expectations, so **credibility is the binding constraint.**
- **⚠️ QE works through asset prices and term premia, not the multiplier** *([[08 - Central Banks and the Money Supply Process|ch. 08]]: base +350%, M1 +105%)*. **Judging it by aggregates misreads it.**
- **A nominal anchor pins the price level and limits time inconsistency.**
- **⚠️ Time inconsistency: expansion works once and stops working once expected** — [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s rational expectations. **And the bank need not *want* to inflate; being *tempted* is enough.**
- **Taylor rule verified: $3+2+\tfrac12(1)+\tfrac12(1)=\mathbf{6.00\%}$** ✓. **It is a formula for the *real* stance, and at low inflation it asks for a negative nominal rate.**
- **⚠️ THE TAYLOR PRINCIPLE IS A STABILITY CONDITION** *(simulated: $\phi=1.5$ converges, $\phi=1.0$ drifts forever, $\phi=0.8$ explodes 3.00 → 4.14 in eight periods)*. **Mishkin asserts the instability and does not show it.**
- **⚠️ "The Fed raised rates in the 1970s" is not a defence — it raised them by less than inflation rose, which is an easing.** [[02 - The Meaning of Interest Rates|Ch. 02]]'s distinction deciding a decade.
- **Four reasons not to automate the rule** — **⚠️ and the first undercuts it from inside: nobody observes the output gap**, so the rule inherits a judgement. **Measurement-boundary result again.**
- **The correct use is as a *benchmark*: if you deviate, be able to say why.** In the 1970s there was no answer.
- **Inflation targeting avoids depending on money demand** — **exactly the assumption [[08 - Central Banks and the Money Supply Process|ch. 08]] showed failed twice.** **In practice, *flexible* inflation targeting.**
- **⚠️ Three instrument criteria: measurability, controllability, predictable effect.** **Aggregates fail all three in sequence — [[01 - The Financial System and What Money Is|ch. 01]] and [[08 - Central Banks and the Money Supply Process|ch. 08]] are the evidence** — **so the switch to interest rates is a measured failure, not a fashion.**

## ⚠️ Important Notes

1. **⚠️ The Fed sets a corridor, not a rate.** Both bounds are standing facilities offering unlimited quantity at a fixed price.
2. **A flat segment on either curve suspends the usual comparative static.**
3. **⚠️ "The Fed buys bonds, the funds rate falls" is true only under scarce reserves** — and nothing in the sentence says so.
4. **In a floor system the instrument is $i_{or}$, and it works by announcement.**
5. **⚠️ Abundant reserves are what made QE possible** — the quantity was freed from rate-setting duty.
6. **Discount policy is a crisis tool, not a rate tool.**
7. **⚠️ A penalty rate is the design answer to moral hazard** — available but unattractive.
8. **Reserve requirements tax deposit-taking**, pushing activity toward the shadow system.
9. **⚠️ The zero lower bound is where the Taylor rule asks for a negative number**, not a separate topic.
10. **Forward guidance is a promise the bank will later want to break.** Credibility is everything.
11. **⚠️ Do not judge QE by monetary aggregates.** It runs through term premia.
12. **⚠️ Time inconsistency needs no bad intent** — the *expectation* of temptation is sufficient.
13. **A rule's virtue is removing temptation, not improving judgement.**
14. **⚠️ The Taylor rule prescribes a real stance.** The nominal number is an output.
15. **⚠️ $\phi>1$ is a stability condition.** Below it, higher inflation *eases* policy.
16. **Raising nominal rates during inflation may still be an easing.** Always compute the real rate.
17. **⚠️ The output gap is unobservable**, so two honest users of the same rule disagree.
18. **Use the rule as a benchmark demanding justification for deviation.**
19. **Strict inflation targeting is not practised** — flexibility over the horizon is the norm.
20. **⚠️ Controllability without a link to the goal is worthless** — the price of tea in China.

> [!warning] Gaps in the source material
> **Two long chapters compressed into one note, and the extraction was adequate for prose but poor for the analytical figures.**
>
> **⚠️ ALL TWELVE FIGURES ARE LOST, and — checked per [[03 - The Behavior of Interest Rates|ch. 03]]'s rule — the prose does NOT name their data points.** **The losses divide into three kinds.**
> - **⚠️ The market-for-reserves diagrams (ch. 16 Figures 1–6) are the significant loss.** They carry the corridor model and every comparative static in it — the response to an open market operation, to a discount-rate change, and to a change in the interest on reserves. **Mishkin describes each shift in words, and §1 reproduces that reasoning; but the diagrams have no numbers on either axis, so nothing can be recovered.** **§1's numerical corridor is therefore MY construction** — the floor, ceiling and demand slope are assumed figures chosen to display the three regimes. **The *structure* (where each curve is flat and why) is Mishkin's; the numbers are mine and are labelled as such.**
> - **Data series** — **Figure 7** (the Fed's balance sheet 2007–2017), **ch. 17 Figure 1** (inflation and targets for New Zealand, Canada and the UK) and **Figure 5** (the Taylor rule against the actual funds rate, 1960–2017). **⚠️ Figure 5 is the empirical basis for the chapter's central historical claim** — that the rule tracks Fed behaviour well after 1987 and badly in the 1970s. **That claim is retained on Mishkin's authority and the accompanying prose; the series are not reconstructed.**
> - **Schematics** — ch. 17's Figures 2–4 (the linkage chain and instrument comparisons) are flowcharts whose content is verbal, and §8 reproduces it. **No loss.**
>
> **No table survives in either chapter to test** — unusually, these two chapters carry their content in prose and figures rather than tables.
>
> **No erratum found, and no discrepancy.** **Mishkin's only worked numerical example — the Taylor rule at 3% inflation and a 1% output gap — reproduces exactly at 6.00%.**
>
> **⚠️ SCOPE NOTE — two chapters in one note, so both are compressed.** **Deliberately reduced:** *Inside the Fed* on the trading desk and on Fed watchers; the detailed mechanics of repos and reverse repos; **the ECB's operational framework and monetary-policy strategy** *(retained only as the note that it exists — [[10 - Foreign Exchange and the International Financial System|ch. 10]] and [[00-Index]]'s boundary put European institutional detail outside this scope)*; the country-by-country inflation-targeting histories (New Zealand, Canada, the UK); Bernanke's advocacy; and **the "should central banks try to stop asset-price bubbles?" debate**, which is genuinely interesting but belongs with [[07 - Financial Crises|ch. 07]]'s material and would duplicate it. **The lessons-from-the-crisis section is folded into §3 and §8.**
>
> **Additions beyond the source.**
>
> - **⚠️ §6 is the note's principal addition.** **Mishkin states the Taylor principle, asserts that violating it produces "serious instability", and points at the 1970s.** **He never writes the dynamic system.** Deriving $\pi_{t+1}-\pi^*=[1-k(\phi-1)](\pi_t-\pi^*)$ and simulating it **converts an assertion into a demonstration** — and shows the sharper fact that $\phi=1$ is not merely "worse" but a knife-edge at which shocks *never* decay. **The link to [[02 - The Meaning of Interest Rates|ch. 02]]'s independently-recorded observation that 1970s real rates were negative is mine**, and it is what makes the principle concrete rather than technical.
> - **⚠️ §1's numerical corridor is mine**, built to make visible the one thing the figures cannot show: **the exact point at which open market operations stop working.** **The identification of that regime with [[08 - Central Banks and the Money Supply Process|ch. 08]]'s excess-reserves ratio — same fact, two sides — is my synthesis**, and neither chapter states it.
> - **§5's table of the rule across states, and the observation that it is a formula for the *real* stance whose bottom rows *are* the zero lower bound, are mine.** Mishkin computes one case.
> - **⚠️ §8's scoring of the two instrument candidates against the three criteria is mine.** **Mishkin lists the criteria and separately reports the worldwide switch to interest rates.** **Scoring aggregates explicitly — measurability failing in [[01 - The Financial System and What Money Is|ch. 01]], controllability in [[08 - Central Banks and the Money Supply Process|ch. 08]], predictable effect in both — turns "central banks now use interest rates" into a conclusion with evidence attached**, and it is the point at which the subject's first eight chapters assemble into one argument.
> - **§7's observation that the unobservable output gap is another instance of the measurement-boundary result is mine.**
> - **§3's framing of forward guidance as a *time-inconsistent promise*, and the warning that QE should not be judged by monetary aggregates, are my syntheses** of material Mishkin presents in separate sections.
> - **§2's summary — one tool is for crises, one is obsolete, and the third stopped working — is mine**, and it is why the nonconventional tools are treated here as the main sequence rather than as an emergency appendix.

**Previous:** [[08 - Central Banks and the Money Supply Process]] · **Next:** [[10 - Foreign Exchange and the International Financial System]]
