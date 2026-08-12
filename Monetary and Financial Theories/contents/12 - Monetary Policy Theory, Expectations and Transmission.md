---
subject: Monetary and Financial Theories
chapter: 12
tags: [ds, economics, monetary-policy, lucas-critique, credibility, transmission-mechanisms, tobins-q, divine-coincidence]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 24–26"
---

# Monetary Policy Theory, Expectations and Transmission

**The last chapter of the subject, and it closes on itself.** **Its four concluding lessons are, in order, [[02 - The Meaning of Interest Rates|ch. 02]]'s real-versus-nominal distinction, [[03 - The Behavior of Interest Rates|ch. 03]]'s unsolved stance problem, [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s nonconventional tools, and [[07 - Financial Crises|ch. 07]]'s debt deflation — with the answers attached.**

**Four results.**

**§1 — the trade-off exists in only one of three cases.** **The *divine coincidence* — stabilising inflation automatically stabilises output — holds for demand shocks and for permanent supply shocks.** **⚠️ It fails only for *temporary* supply shocks** — which is why "flexible" inflation targeting is the practice.

**§4 — Tobin's $q$ has a threshold at exactly 1.** *(Computed: at $q=0.50$, \$100m of equity buys **\$200m of capital second-hand but only \$100m by building** — so firms acquire and aggregate investment in new capital stops, with no change in interest rates required.)*

**§5 — ⚠️ the nine channels, counted.** *(**5 of 9 run through asset prices other than short rates**; **5 of 9 are "credit view"** and **3 of those show moral hazard and adverse selection explicitly in the chain**; and **exactly one uses *nominal* rates**.)*

**§6 — ⚠️ LESSON 2 SOLVES A QUESTION OPEN SINCE CH. 03.** **"If short-term interest rates are low or even zero and yet stock prices are low, housing prices are low, and the value of the domestic currency is high, monetary policy is clearly *tight*, not easy."**

## 📘 Main Knowledge

### 1. ⚠️ The divine coincidence — when is there a trade-off?

**Mishkin runs three cases through [[11 - Money Demand and the Monetary Policy Framework|ch. 11]]'s AD–AS machinery.**

| shock | what moves | gaps | **trade-off?** |
|---|---|---|---|
| **aggregate demand** | AD shifts | same direction | **NO** |
| **permanent supply** | AS *and* LRAS shift | potential output itself moved | **NO** |
| **temporary supply** | AS shifts, **LRAS fixed** | **opposite directions** | **⚠️ YES** |

- **Demand shock:** output and inflation move together, **so stabilising inflation also stabilises output.**
- **Permanent supply shock:** **potential output moves too, so no output gap ever opens** — closing the inflation gap closes everything.
- **Temporary supply shock:** **inflation rises and output falls at once. You must choose.**

> [!warning] ⚠️ The divine coincidence holds in every case but one
> **The famous "inflation versus unemployment trade-off" is not a general feature of the economy — it is what a *temporary supply shock* does.**
>
> **And for that one case there are three responses, none of them free:**
>
> | response | cost |
> |---|---|
> | **no response** | a painful period of low output *and* high inflation, self-correcting eventually |
> | **stabilise inflation** | tighten — driving output down **further** now, then reverse as AS shifts back |
> | **stabilise output** | ease — accepting higher inflation now |
>
> **⚠️ Which is why *flexible* inflation targeting ([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §8) is the practice.** **A strict targeter must pick the middle row every time; the flexibility is precisely discretion over this case.**

### 2. The Lucas critique

**Standard practice: feed policy options — 4%? 6%? — into an econometric model estimated on past data, read off unemployment and inflation, choose the best.**

> [!warning] ⚠️ Lucas: the model's coefficients were estimated under the *old* regime
> **Change the policy and the public changes how it forms expectations — so the coefficients themselves move.** **The model predicts the effect of a policy that, once adopted, is no longer the policy modelled.**

**Mishkin's worked case is [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s.** **The term structure equation relates the long rate to *current and past* short rates — but ch. 04 established that the long rate is an average of *expected future* short rates plus a term premium.** **⇒ a regression on past short rates works only while the process generating short rates is unchanged.** **Change the reaction function and the estimated equation is worthless.**

> [!note] ⚠️ This is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s implication 1 made lethal
> **There: "if there is a change in the way a variable moves, the way expectations of it are formed will change as well."** **Here: therefore every estimated relationship is conditional on a regime, and evaluating a *regime change* with one is circular.**
>
> **And note what the critique does *not* say.** **It does not say models are useless** — it says models *without* rational expectations cannot evaluate policy *changes*. **Forecasting within a stable regime is fine.**

### 3. Credibility — and why it is worth real money

**[[09 - Tools and Conduct of Monetary Policy|Ch. 09]] §4 established time inconsistency: a discretionary expansion is anticipated, so it buys inflation and no output.** **Credibility is the fix, and it has two payoffs.**

**(1) ⚠️ Credibility makes supply shocks cheaper.** **If wage- and price-setters believe the central bank will not accommodate, an oil shock does not feed into expected inflation — so AS shifts up *less* and the output loss is smaller.**

> [!warning] A tale of three oil price shocks — as close to a controlled experiment as monetary economics gets
> **The 1973–75 and 1978–80 shocks produced stagflation.** **The 2000s oil price rises — *larger* on some measures — did not.** **The difference is entirely expectations: by then the nominal anchor held.**
>
> **⇒ the same shock, three times, with different outcomes, and the varying input is credibility.**

**(2) ⚠️ Credibility makes disinflation cheaper.** **A credible announcement lowers expected inflation immediately, shifting AS *down* at the same moment AD shifts left — so inflation falls at a smaller output cost.** **Without it you get the Volcker recession.**

*(Bolivia ended a hyperinflation almost overnight once the regime change was believed. **Reagan's deficits *undermined* credibility**, because large future deficits imply future monetisation.)*

> [!note] ⚠️ So credibility is not a soft virtue
> **It is a parameter that multiplies the cost of every shock and every disinflation.** **And it is why [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s nominal anchor, ch. 09's central bank independence, and [[10 - Foreign Exchange and the International Financial System|ch. 10]]'s currency boards all exist — three technologies for buying the same thing.**

### 4. Tobin's $q$ — an investment rule with a threshold

$$q=\frac{\text{market value of firms}}{\text{replacement cost of capital}}$$

**The logic is an arbitrage and the threshold is exactly 1.**

| $q$ | \$100m of equity issued buys | verdict |
|---|---|---|
| 2.00 | \$50.0m of new capital | build — new capital is cheap |
| 1.20 | \$83.3m | build |
| **1.00** | \$100.0m | **indifferent** |
| 0.80 | \$125.0m | **acquire, do not build** |
| **0.50** | **\$200.0m** | **⚠️ acquire, do not build** |

> [!warning] ⚠️ At $q=0.50$ a firm can buy \$200m of capital second-hand for what \$100m of building costs
> **So it acquires an existing firm instead.** **Aggregate investment in *new* capital collapses while share prices are low — and no change in interest rates is required for this to happen.**

> [!note] The monetary link, already quantified in ch. 05
> **Expansionary policy raises stock prices → raises $q$ → raises investment.**
>
> **⚠️ And [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]] §4 already computed the first step**: with the Gordon model, **a half-point easing that moves both $k_e$ and $g$ raises equity by 9.1%, and a two-point easing by 50.0%.** **Ch. 05 computed the magnitude; this chapter names what it is *for*.**
>
> *(The **wealth channel** is the household twin: higher stock prices raise financial wealth, which raises lifetime resources, which raises consumption. **Same first step, different final spender.**)*

### 5. ⚠️ The nine transmission channels — counted

*(Mishkin's Figure 1 is a schematic and it extracted intact — every channel with its full chain.)*

| channel | group | runs through | then |
|---|---|---|---|
| **traditional interest-rate** | interest rate | **real** rates | → investment |
| **exchange rate / net exports** | asset price | **real** rates | → exchange rate → net exports |
| **Tobin's $q$** | asset price | stock prices | → $q$ → investment |
| **wealth effects** | asset price | stock prices | → financial wealth → consumption |
| **bank lending** | **credit view** | bank deposits | → bank loans → investment |
| **balance sheet** | **credit view** | stock prices | → ***MH/AS*** → lending → investment |
| **cash flow** | **credit view** | **⚠️ NOMINAL rates** | → cash flow → ***MH/AS*** → lending |
| **unanticipated price level** | **credit view** | price surprise | → ***MH/AS*** → lending → investment |
| **household liquidity** | **credit view** | stock prices | → wealth → distress probability → housing, durables |

**Mishkin's own grouping: 1 traditional, 1 exchange rate, 2 "other asset price effects", 5 "credit view".**

> [!warning] ⚠️ Three counts, and each is a result
> **(1) Five of the nine are "credit view", and three of those show *moral hazard and adverse selection* explicitly in the chain.** **That is [[06 - Asymmetric Information and Financial Structure|ch. 06]]'s apparatus sitting *inside* the monetary transmission mechanism.**
> **⇒ monetary policy works partly by changing how severe the asymmetric-information problem is** — which is why [[07 - Financial Crises|ch. 07]]'s crises *disable* monetary policy rather than merely coinciding with it.
>
> **(2) Five of the nine run through asset prices other than short rates** — **stock prices alone carry four.** **⇒ reading the stance off the short rate ignores most of the mechanism.** *(§6.)*
>
> **(3) ⚠️ Exactly one channel uses *nominal* interest rates: cash flow.** **Everything else runs on real rates — and the exception has a reason: debt service is contractually *nominal*, so a firm's cash flow responds to the nominal rate whatever inflation does.**
> **⚠️ That is a genuine qualification to Lesson 1 below, which says to use real rates. One channel legitimately does not.**
>
> *(And note the **cash flow** and **unanticipated price level** channels are [[07 - Financial Crises|ch. 07]]'s debt deflation arriving as *monetary transmission*: nominal debt, real assets, and the gap doing the damage.)*

### 6. ⚠️ The four lessons — and ch. 03's problem finally solved

**LESSON 1. Do not equate a fall in short-term *nominal* rates with easing.** **Associate easing and tightening with **real** rates.**

> [!note] [[02 - The Meaning of Interest Rates|Ch. 02]]'s distinction as a policy warning
> **And [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §6's 1970s finding is the case in point: nominal rates rose while real rates fell, which was an *easing*.**

**LESSON 2. ⚠️ Other asset prices carry information about the stance.** Mishkin's own test, and the sharpest sentence in the chapter:

> **"If short-term interest rates are low or even zero and yet stock prices are low, housing prices are low, and the value of the domestic currency is high, monetary policy is clearly *tight*, not easy."**

> [!warning] ⚠️ This closes a question open since ch. 03
> | | |
> |---|---|
> | **[[03 - The Behavior of Interest Rates\|ch. 03]] §7** | the **level** of the interest rate does not measure the stance — low rates may mean weak demand rather than easy policy. **Problem posed, unsolved.** |
> | **[[09 - Tools and Conduct of Monetary Policy\|ch. 09]] §8** | the **slope** of the yield curve carries information the level does not. **Partial answer.** |
> | **ch. 12, lesson 2** | read the **whole vector** of asset prices — short rates, long rates, equities, housing, the exchange rate. **Answer.** |
>
> **And §5 explains *why* it works: five of the nine channels run through those very prices.** **⇒ they are not *proxies* for the stance — they are *part of* it.**

**LESSON 3. Monetary policy is not impotent at the zero lower bound.** **Open market purchases need not be in short-term government securities; buying private securities lowers credit spreads ([[04 - The Risk and Term Structure of Interest Rates|ch. 04]]) directly; and a commitment to future expansion raises inflation expectations and reflates asset prices.**

> [!note] [[09 - Tools and Conduct of Monetary Policy|Ch. 09]]'s nonconventional tools, justified rather than asserted
> **The ZLB argument is exactly [[11 - Money Demand and the Monetary Policy Framework|ch. 11]]'s liquidity trap: the *traditional* channel is dead — but eight others are not.** *(Mishkin: aggressive nonconventional policy "helped prevent the Great Recession from turning into a Great Depression.")*

**LESSON 4. ⚠️ Avoid unanticipated price-level movements — and deflation is at least as bad as inflation.**

> [!warning] ⚠️ Because ch. 07's debt deflation is a transmission channel running in reverse
> **An unanticipated fall in the price level raises real debt against unchanged assets — [[07 - Financial Crises|ch. 07]] §2 computed net worth going from \$10m to \$0 — which worsens moral hazard and adverse selection and collapses lending.**
>
> **⇒ "price stability" means *stability*, not *low* inflation. A negative inflation rate is not a bonus.** **Mishkin: "central banks must work very hard to prevent price deflation."**

> [!warning] ⚠️ And that is the subject closing on itself
> **The four lessons are, in order: [[02 - The Meaning of Interest Rates|ch. 02]]'s real-versus-nominal distinction, [[03 - The Behavior of Interest Rates|ch. 03]]'s unsolved stance problem, [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s nonconventional tools, and [[07 - Financial Crises|ch. 07]]'s debt deflation.** **The last chapter is a list of the earlier ones, with the answers attached.**

## ✏️ Exercises

**1. (Hard — the divine coincidence.)** (a) When is there a trade-off? (b) Why do the other cases escape it? (c) What follows for policy design?

> [!example]- Solution
> **(a) Only for a *temporary* supply shock.**
>
> | shock | trade-off |
> |---|---|
> | aggregate demand | **no** |
> | permanent supply | **no** |
> | **temporary supply** | **YES** |
>
> **⚠️ So the famous "inflation versus unemployment trade-off" is not a general property of the economy.** **It is what one particular kind of shock does.**
>
> **(b) Because in the other two, the two gaps close together.**
>
> **A demand shock moves output and inflation in the *same* direction** — a boom raises both, a slump lowers both. **So the policy that returns inflation to target also returns output to potential. Nothing is given up.**
>
> **A *permanent* supply shock moves LRAS as well**, so **potential output itself has changed.** **The output gap never opens** — the economy's capacity moved to meet the new output level, and closing the inflation gap closes everything.
>
> **⚠️ A *temporary* supply shock is different precisely because LRAS does *not* move.** **Short-run AS shifts up, so inflation rises *and* output falls simultaneously — the two gaps open in opposite directions, and no single interest rate closes both.**
>
> **(c) That discretion is needed for exactly one case — which is what "flexible" targeting means.**
>
> **Three responses, none free:** **no response** (a painful period of low output *and* high inflation, self-correcting eventually); **stabilise inflation** (tighten, driving output down *further* now); **stabilise output** (ease, accepting higher inflation now).
>
> **⚠️ A *strict* inflation targeter must choose the second every time.** **The "flexibility" in flexible inflation targeting ([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §8) is precisely discretion over this case** — the horizon over which to return to target.
>
> **⇒ so flexible targeting is not a weakening of the regime for convenience.** **It is a response to a specific structural fact about one class of shock**, and the framework identifies exactly which one.

**2. (The Lucas critique.)** (a) State it. (b) Work Mishkin's example. (c) What does it *not* say?

> [!example]- Solution
> **(a) Estimated coefficients are conditional on the policy regime that generated the data.**
>
> **The practice was to feed policy options into a model estimated on past data and read off the outcomes.** **⚠️ But when the policy changes, the public changes how it forms expectations — so the coefficients themselves move.** **The model predicts the effect of a policy that, once adopted, is no longer the policy modelled.**
>
> **(b) The term structure equation.**
>
> **Macroeconometric models related the long rate to *current and past* short rates — an important equation, because it is the *long* rate that drives aggregate demand.**
>
> **But [[04 - The Risk and Term Structure of Interest Rates|ch. 04]] established the long rate is an average of *expected future* short rates plus a term premium.** **The past-short-rate regression works only as a proxy, and only while the process generating short rates is unchanged.**
>
> **⚠️ Change the central bank's reaction function — which is exactly what a policy evaluation contemplates — and the relationship between past and future short rates changes, so the estimated equation is worthless for the question being asked.**
>
> *(This is a good example because the failure is not subtle: ch. 04 showed the long rate is *forward*-looking, and the equation is *backward*-looking. It worked only because the two coincided under a stable regime.)*
>
> **(c) It does not say models are useless.**
>
> **It says models *without* rational expectations cannot be used to evaluate policy *changes*.** **Forecasting within a stable regime is fine** — the coefficients are stable precisely because the regime is.
>
> **⚠️ And this is [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]]'s implication 1 made lethal.** **There it was an observation: "if there is a change in the way a variable moves, the way expectations of it are formed will change as well."** **Here it becomes a constraint on the entire practice of policy evaluation** — because the thing a policymaker most wants to evaluate is a *change*, which is exactly the case the models cannot handle.

**3. (Hard — credibility.)** (a) What are its two payoffs? (b) What is the evidence? (c) Why does this justify earlier chapters' institutions?

> [!example]- Solution
> **(a) Cheaper supply shocks and cheaper disinflations.**
>
> **⚠️ Supply shocks:** if wage- and price-setters believe the bank will not accommodate, **the shock does not feed into expected inflation, so AS shifts up *less* and the output loss is smaller.** **The same physical shock costs less.**
>
> **⚠️ Disinflation:** a credible announcement lowers expected inflation *immediately*, **shifting AS down at the same moment AD shifts left.** **So inflation falls with a smaller output cost.** **Without credibility, expected inflation only falls after the recession has proved the bank's seriousness — the Volcker recession.**
>
> **(b) Three oil shocks, and two hyperinflation endings.**
>
> **⚠️ The oil shocks are the strongest evidence in the chapter.** **1973–75 and 1978–80 produced stagflation. The 2000s oil price rises — *larger* on some measures — did not.** **The difference is entirely expectations: by then the nominal anchor held.**
>
> **⇒ the same shock, three times, with different outcomes, and the varying input is credibility.** **That is as close to a controlled experiment as monetary economics gets** — the shock is externally generated, roughly comparable in size, and the institutional environment differs.
>
> *(Bolivia ended a hyperinflation almost overnight once the regime change was believed — consistent with [[11 - Money Demand and the Monetary Policy Framework|ch. 11]] §3's finding that hyperinflations are self-defeating and end abruptly. **And Reagan's deficits *undermined* credibility**, because large future deficits imply future monetisation — [[07 - Financial Crises|ch. 07]]'s path B seen as an expectations problem.)*
>
> **(c) Because they are three technologies for buying the same thing.**
>
> **⚠️ Credibility is not a soft virtue — it is a parameter that multiplies the cost of every shock and every disinflation.** **That reframes several earlier institutions as investments in it:**
>
> - **[[09 - Tools and Conduct of Monetary Policy|Ch. 09]]'s nominal anchor** — a public, checkable commitment;
> - **ch. 09's central bank independence** — removing the political temptation rather than resisting it;
> - **[[10 - Foreign Exchange and the International Financial System|Ch. 10]]'s currency boards and dollarization** — commitment bought by making exit hard.
>
> **All three cost something** *(ch. 10: a currency board surrenders the lender of last resort, which killed Argentina's)*. **The justification for paying is here: what they buy is a cheaper response to every future shock.**

**4. (Hard — transmission.)** (a) Explain Tobin's $q$. (b) Set out the nine channels. (c) What do the counts show?

> [!example]- Solution
> **(a) An arbitrage with a threshold at exactly 1.**
>
> $$q=\frac{\text{market value of firms}}{\text{replacement cost of capital}}$$
>
> **If $q>1$ the market pays more for a firm's capital than it costs to build — so issue equity and build.** **If $q<1$, capital is cheaper to buy second-hand by acquiring a firm.**
>
> *(Computed: at $q=0.50$, **\$100m of equity buys \$200m of capital second-hand but only \$100m by building**.)*
>
> **⚠️ So aggregate investment in *new* capital collapses whenever share prices are low — and no change in interest rates is required for this to happen.** **That is the point of the channel: it is a route from monetary policy to investment that does not run through the cost of borrowing at all.**
>
> **The monetary link:** easing raises stock prices → raises $q$ → raises investment. **And [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]] §4 already quantified the first step** — a half-point easing raises equity **9.1%**, a two-point easing **50.0%**. **Ch. 05 computed the magnitude; this chapter says what it is for.**
>
> **(b) Nine, in four groups.**
>
> | group | channels |
> |---|---|
> | **traditional** | interest rate → investment |
> | **exchange rate** | real rates → exchange rate → net exports |
> | **other asset prices** | **Tobin's $q$**, **wealth effects** |
> | **credit view** | **bank lending**, **balance sheet**, **cash flow**, **unanticipated price level**, **household liquidity** |
>
> **(c) Three counts, three results.**
>
> **⚠️ (1) Five of nine are "credit view", and three show *moral hazard and adverse selection* explicitly in the chain.** **[[06 - Asymmetric Information and Financial Structure|Ch. 06]]'s apparatus is sitting inside the monetary transmission mechanism.**
> **⇒ monetary policy works partly by changing how severe the asymmetric-information problem is** — **which is why [[07 - Financial Crises|ch. 07]]'s crises *disable* monetary policy rather than merely coinciding with it.** A crisis raises the very frictions several channels operate through.
>
> **⚠️ (2) Five of nine run through asset prices other than short rates**, and **stock prices alone carry four of them** (Tobin's $q$, wealth, balance sheet, household liquidity). **⇒ reading the stance off the short rate ignores most of the mechanism.**
>
> **⚠️ (3) Exactly one channel uses *nominal* rates: cash flow.** **Everything else runs on real rates.** **The exception is principled — debt service is contractually nominal, so a firm's cash flow responds to the nominal rate whatever inflation does** — and it is **a genuine qualification to Lesson 1**, which says to use real rates. **One channel legitimately does not.**
>
> *(And note the **cash flow** and **unanticipated price level** channels are [[07 - Financial Crises|ch. 07]]'s debt deflation arriving as monetary transmission: nominal debt, real assets, and the gap between them doing the damage.)*

**5. (The four lessons.)** (a) State them. (b) Which earlier question does lesson 2 answer? (c) Why is deflation singled out?

> [!example]- Solution
> **(a)**
> 1. **Do not equate falling short-term *nominal* rates with easing** — use **real** rates.
> 2. **Other asset prices carry information about the stance.**
> 3. **Monetary policy is not impotent at the zero lower bound.**
> 4. **Avoid unanticipated price-level movements — and deflation is at least as bad as inflation.**
>
> **(b) ⚠️ [[03 - The Behavior of Interest Rates|Ch. 03]] §7's, which has been open for nine chapters.**
>
> | | |
> |---|---|
> | **[[03 - The Behavior of Interest Rates\|ch. 03]] §7** | the **level** of rates does not measure the stance — low rates may mean weak demand, not easy policy. **Posed, unsolved.** |
> | **[[09 - Tools and Conduct of Monetary Policy\|ch. 09]] §8** | the **slope** of the yield curve carries information the level does not. **Partial.** |
> | **ch. 12** | read the **whole vector** — short rates, long rates, equities, housing, the currency. **Answered.** |
>
> **Mishkin's test is the sharpest sentence in the chapter: "if short-term interest rates are low or even zero and yet stock prices are low, housing prices are low, and the value of the domestic currency is high, monetary policy is clearly *tight*, not easy."**
>
> **⚠️ And §5 explains *why* the test works.** **Five of the nine channels run through exactly those prices** — **so they are not *proxies* for the stance, they are *part of* it.** **A stance measure that omits them is not imprecise; it is measuring a fraction of the mechanism.**
>
> **(c) Because deflation is a transmission channel running in reverse.**
>
> **[[07 - Financial Crises|Ch. 07]] §2 computed it: an unanticipated fall in the price level raises real debt against unchanged assets — net worth \$10m → \$0 at 10% deflation and 90% leverage.** **That worsens moral hazard and adverse selection and collapses lending**, which is precisely the *unanticipated price level* channel of §5 with the sign reversed.
>
> **⚠️ So "price stability" means *stability*, not *low* inflation.** **A negative inflation rate is not a bonus** — Mishkin: **"central banks must work very hard to prevent price deflation."**
>
> *(This also explains why inflation targets are set at 2% rather than 0%: the target must leave room for the price level to fall below expectation without going negative, and — from [[09 - Tools and Conduct of Monetary Policy|ch. 09]] — room for the real rate to fall before the nominal rate hits zero.)*
>
> **⚠️ And notice that the four lessons are the subject's own earlier chapters in order** — ch. 02's real-versus-nominal distinction, ch. 03's stance problem, ch. 09's nonconventional tools, ch. 07's debt deflation. **The final chapter is a list of the earlier ones with the answers attached.**

## 📝 Summary

- **⚠️ The *divine coincidence* — stabilising inflation also stabilises output — holds for demand shocks and for PERMANENT supply shocks.** **It fails only for TEMPORARY supply shocks**, where the gaps open in opposite directions.
- **⇒ the "inflation–unemployment trade-off" is not a general feature of the economy; it is what one class of shock does** — **and *flexible* inflation targeting is discretion over exactly that case.**
- **The Lucas critique: estimated coefficients are conditional on the regime that generated the data.** **Change the policy and the public changes how it forms expectations, so the coefficients move.**
- **Mishkin's example is [[04 - The Risk and Term Structure of Interest Rates|ch. 04]]'s term structure equation** — backward-looking, when the long rate is forward-looking. **⚠️ It does *not* say models are useless: forecasting within a stable regime is fine.**
- **⚠️ Credibility has two payoffs**: **cheaper supply shocks** (the shock does not feed into expectations) and **cheaper disinflations** (AS shifts down as AD shifts left).
- **⚠️ Three oil shocks are the evidence** — 1973–75 and 1978–80 gave stagflation; the *larger* 2000s rises did not. **Same shock, different anchor.**
- **⇒ credibility is a parameter that multiplies the cost of every shock**, which justifies [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s anchor, ch. 09's independence and [[10 - Foreign Exchange and the International Financial System|ch. 10]]'s currency boards as three ways of buying it.
- **Tobin's $q$ = market value / replacement cost, with a threshold at exactly 1.** *(Computed: at $q=0.50$, **\$100m of equity buys \$200m of capital second-hand but only \$100m by building**.)* **⇒ investment in new capital stops with no change in interest rates.**
- **[[05 - The Stock Market, Rational Expectations and Efficient Markets|Ch. 05]] already quantified the first step** — a half-point easing raises equity **9.1%**, two points **50.0%**. **Ch. 05 gave the magnitude; ch. 12 names its purpose.**
- **⚠️ NINE CHANNELS: 1 traditional, 1 exchange rate, 2 other-asset-price, 5 credit view.**
- **⚠️ Five of nine run through asset prices other than short rates; stock prices alone carry four.**
- **⚠️ Three show *moral hazard and adverse selection* explicitly** — **[[06 - Asymmetric Information and Financial Structure|ch. 06]]'s apparatus inside the transmission mechanism**, which is why crises *disable* policy rather than coincide with it.
- **⚠️ Exactly one channel uses NOMINAL rates — cash flow — because debt service is contractually nominal.** **A genuine qualification to Lesson 1.**
- **Lesson 1: use *real* rates.** [[02 - The Meaning of Interest Rates|Ch. 02]]'s distinction as a policy warning, with the 1970s as the case.
- **⚠️ Lesson 2 CLOSES [[03 - The Behavior of Interest Rates|CH. 03]] §7's OPEN QUESTION**: **low short rates with low equities, low housing and a strong currency mean policy is TIGHT.** **Level → slope ([[09 - Tools and Conduct of Monetary Policy|ch. 09]]) → whole vector (here).**
- **Lesson 3: policy is not impotent at the ZLB** — the *traditional* channel dies, eight others do not.
- **⚠️ Lesson 4: deflation is at least as bad as inflation**, because [[07 - Financial Crises|ch. 07]]'s debt deflation is the *unanticipated price level* channel in reverse. **"Price stability" means stability, not low inflation.**
- **⚠️ The four lessons are ch. 02, ch. 03, ch. 09 and ch. 07 in order** — **the last chapter is a list of the earlier ones with the answers attached.**

## ⚠️ Important Notes

1. **⚠️ The output–inflation trade-off exists only for temporary supply shocks.** Do not generalise it.
2. **A permanent supply shock moves potential output**, so no gap opens.
3. **⚠️ "Flexible" targeting is discretion over one specific case**, not general laxity.
4. **The Lucas critique bites on policy *changes*, not on forecasting.**
5. **⚠️ A backward-looking equation for a forward-looking variable works only while the regime is stable.**
6. **Credibility is a parameter, not a virtue.** It multiplies every shock's cost.
7. **⚠️ The same oil shock cost very different amounts in 1973 and 2005.** The difference was the anchor.
8. **Deficits can undermine monetary credibility** by implying future monetisation.
9. **⚠️ Tobin's $q$ has a threshold at exactly 1.** Below it, firms acquire rather than build.
10. **The $q$ channel needs no change in interest rates** — it runs on equity prices.
11. **Wealth effects are the household twin of $q$** — same first step, different spender.
12. **⚠️ Five of nine channels bypass short-term rates entirely.**
13. **⚠️ Three channels run through asymmetric information**, which is why a crisis disables policy.
14. **⚠️ Only the cash-flow channel uses nominal rates** — because debt service is nominal.
15. **⚠️ Never read the stance off the short rate alone.** Read the vector.
16. **Low rates plus low asset prices plus a strong currency = TIGHT policy.**
17. **⚠️ The ZLB kills one channel, not nine.**
18. **⚠️ Deflation is not "very low inflation".** It is a distinct mechanism that destroys net worth.
19. **A 2% target is not a target for *some* inflation** — it is room for error in both directions.

> [!warning] Gaps in the source material
> **Three chapters compressed into one note, and the extraction pattern is by now familiar.**
>
> **⚠️ FIGURE 1 OF CH. 26 — THE TRANSMISSION-CHANNEL SCHEMATIC — EXTRACTED COMPLETELY**, with all nine channels, their full chains, their four group headings and their three final destinations. **§5 is built directly on it.** *(This is the [[10 - Foreign Exchange and the International Financial System|ch. 10]] trilemma-triangle case again: **a schematic whose content is entirely its labels survives, because the labels are text.** Worth recording as a third category alongside "data series — lost" and "shift diagrams — content is in the prose".)*
>
> **⚠️ ALL OTHER FIGURES ARE LOST, AND THIS TIME THE [[03 - The Behavior of Interest Rates|CH. 03]] RECOVERY DOES NOT WORK — checked.** **Ch. 24's sixteen AD–AS figures carry no numbers at all**; they are shift diagrams whose axes are labelled $\pi_T$, $Y^P$ and so on. **Their content is the *direction* of each shift, which the prose states in full and §1 reproduces.** **Nothing is reconstructible and nothing is lost that the prose does not carry.**
>
> **The genuine data losses are ch. 24's Figure 11 (inflation and unemployment, 1965–82) and ch. 25's Figure 3 (the three oil shocks).** **⚠️ The second is the empirical basis for §3's central claim** — that the 2000s oil shocks were larger and cheaper. **That claim is retained on Mishkin's authority and the accompanying prose; no series is reconstructed.**
>
> **No table survives to test in ch. 24 or ch. 25** — both carry their content in prose and diagrams. **No erratum and no discrepancy: this chapter states almost no numbers, and the ones it does (the oil-shock chronology, the policy dates) are narrative rather than computational.**
>
> **⚠️ SCOPE NOTE — the heaviest compression in the subject, and [[00-Index]] anticipated it.** **The index records that ch. 25 is taken "in part — the new-classical/new-Keynesian survey omitted, time-inconsistency kept."** **Also deliberately reduced:** the **full AD–AS graphical apparatus of ch. 24** *(sixteen figures; [[Macroeconomics & Microeconomics/contents/14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|Macro/Micro ch. 14]] owns AD–AS per the recorded boundary, and M 23 is excluded from this subject entirely)*; the **activist/nonactivist debate** and its Obama-stimulus box; the **cost-push versus demand-pull inflation** diagrams *(which restate §1's supply and demand shocks)*; the **Abenomics and Japanese-policy application**; the **political business cycle** and Nixon boxes *([[09 - Tools and Conduct of Monetary Policy|ch. 09]] §8 has the argument)*; the Swiss monetary-targeting box *([[11 - Money Demand and the Monetary Policy Framework|ch. 11]] §5 has the finding)*; and ch. 26's **Great Recession application and consumer-balance-sheet FYI** *([[07 - Financial Crises|ch. 07]] owns the crisis)*.
>
> **Additions beyond the source.**
>
> - **⚠️ §5's three counts are the note's principal addition.** **Mishkin draws the nine channels and discusses them one at a time.** **Counting them — five running through non-short-rate asset prices, five in the credit-view group with three showing moral hazard and adverse selection explicitly, and exactly one using *nominal* rates — turns a catalogue into three results.** **The nominal-rate count is the sharpest: it identifies a *principled exception* to the chapter's own Lesson 1**, which Mishkin states without qualification.
> - **⚠️ §6's identification of Lesson 2 as the answer to [[03 - The Behavior of Interest Rates|ch. 03]] §7's open question is mine**, and it is the note's organising claim. **Ch. 03 posed the problem (the *level* does not measure the stance), [[09 - Tools and Conduct of Monetary Policy|ch. 09]] §8 gave a partial answer (the *slope*), and this chapter completes it (the whole *vector*).** **Mishkin states lesson 2 without reference to either earlier discussion**, and the three-stage progression is my synthesis. **So is the observation that §5's channel counts explain *why* the test works** — those prices are part of the mechanism, not proxies for it.
> - **§1's tabulation of when the trade-off exists, and the observation that flexible inflation targeting is discretion over exactly one case, are mine.** Mishkin works the cases separately and does not summarise the pattern.
> - **§4's $q$ arithmetic is mine** — the threshold at 1 is his, but the table showing that at $q=0.50$ a firm can buy \$200m of capital second-hand for \$100m of building cost makes the *magnitude* of the incentive visible. **The link back to [[05 - The Stock Market, Rational Expectations and Efficient Markets|ch. 05]] §4's computed 9.1% and 50.0% equity responses is mine**: ch. 05 computed the size of the first step and this chapter names its purpose, but neither chapter refers to the other.
> - **§3's framing of credibility as *a parameter that multiplies the cost of every shock*, and of [[09 - Tools and Conduct of Monetary Policy|ch. 09]]'s anchor, ch. 09's independence and [[10 - Foreign Exchange and the International Financial System|ch. 10]]'s currency boards as three technologies for buying it, is mine.**
> - **§2's observation that the term-structure example fails because a *backward*-looking equation was used for a *forward*-looking variable is mine.**
> - **⚠️ The closing observation — that the four lessons are [[02 - The Meaning of Interest Rates|ch. 02]], [[03 - The Behavior of Interest Rates|ch. 03]], [[09 - Tools and Conduct of Monetary Policy|ch. 09]] and [[07 - Financial Crises|ch. 07]] in order, so the final chapter is a list of the earlier ones with the answers attached — is my synthesis**, and it is the reason this note is arranged around the lessons rather than around the three source chapters.

**Previous:** [[11 - Money Demand and the Monetary Policy Framework]] · **Next:** *(end of subject — see [[00-Index]])*
