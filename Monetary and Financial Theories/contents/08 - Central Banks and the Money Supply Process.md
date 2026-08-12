---
subject: Monetary and Financial Theories
chapter: 8
tags: [ds, economics, central-banking, money-multiplier, monetary-base, quantitative-easing, independence]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 14–15"
---

# Central Banks and the Money Supply Process

> [!warning] ⚠️ THIS DISCHARGES [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s FORWARD REFERENCE — THE LAST OUTSTANDING OBLIGATION IN THE VAULT
> **Macro/Micro ch. 12 used the quantity theory and treated the money multiplier as a macro identity, explicitly deferring central-bank operations to here.** **§7 pays the debt, and what it returns is not a refinement — it is that the deferred object *is not a constant and can be less than one*.**

**[[01 - The Financial System and What Money Is|Ch. 01]] established that currency is only 11.0% of M2, so most money is created by banks and depositors.** **This chapter is the mechanism, and its organising fact is that the central bank is one of *three* players.**

**Four results.**

**§4 — ⚠️ the multiplier was 0.73.** *(Verified against Mishkin: $m=1.75/2.4125=\mathbf{0.7254}$.)* **A "multiplier" that divides, and "high-powered money" that isn't.** *(Decomposed — Mishkin does not: **the excess-reserves ratio did 93% of the collapse from 1.60.**)*

**§5 — the currency-ratio paradox, solved exactly.** *(Computed: $dm/dc$ has the sign of $rr+e-1$, so **the threshold is $e=1-rr=0.90$**, at which $m=1.0000$ **for every value of $c$**.)* **Mishkin calls the result "peculiar", explains it verbally, and stops.**

**§6 — QE.** *(The base rose **over 350%** and the multiplier fell to 0.73 — very nearly offsetting.)* **The Fed created reserves; the *banks* declined to turn them into deposits.**

**§7 — ⚠️ and the discharge is not flattering to the deferring chapter.** *(Computed: assuming a constant multiplier forecasts **14.2% inflation a year**; correcting for the collapse gives **5.5%**; the truth was **1.8%**.)* **This chapter closes two-thirds of the gap — and the rest is velocity, which is [[11 - Money Demand and the Monetary Policy Framework|ch. 11]]'s problem.**

## 📘 Main Knowledge

### 1. Three players — and the central bank is only one

| player | chooses |
|---|---|
| **central bank** | the required reserve ratio $rr$, and the **nonborrowed monetary base** $MB_n$ via open market operations |
| **banks** | **excess reserves** $ER$ and borrowed reserves $BR$ |
| **depositors** | how much **currency** $C$ to hold |

$$MB=C+R=MB_n+BR\qquad\qquad R=RR+ER=rr\cdot D+ER$$

> [!warning] ⚠️ The money supply is a joint outcome of three independent sets of decisions, only one of which the central bank makes
> **That is the whole content of the chapter.** **And it is why [[01 - The Financial System and What Money Is|ch. 01]]'s finding matters: currency is 41.6% of M1 but only 11.0% of M2**, so most of what we call money is created by banks lending and depositors depositing.
>
> **The monetary base is called *high-powered money* because \$1 of it supports more than \$1 of money supply** — **⚠️ which is true only when the multiplier exceeds 1. See §4.**

### 2. The simple deposit multiplier — and what it assumes away

**If banks hold no excess reserves and depositors hold no currency, then $R=rr\cdot D$ exactly:**

$$D=\frac{1}{rr}\times R$$

*(Verified: at $rr=0.10$, deposits of \$1,600bn require **\$160bn** of reserves — which support **ten times** their own value.)*

> [!note] The mechanism is multiple deposit creation
> **Bank A lends its excess reserves; the proceeds are deposited at bank B, which keeps $rr$ and lends the rest; and so on.** **⚠️ Nobody creates money on purpose. The *system* does, and no individual bank can see it happening** — each one merely lends out what it does not need to hold.

> [!warning] ⚠️ But the simple multiplier is wrong, and wrong in a known direction
> **It assumes away exactly the two things the other two players decide**, and both are leakages:
> - **currency undergoes no multiple expansion at all;**
> - **excess reserves are reserves that were *not* lent on.**
>
> **So the simple multiplier is an upper bound, not an estimate.**

### 3. ⚠️ The money multiplier

$$c=\frac{C}{D}\ \text{(depositors)}\qquad e=\frac{ER}{D}\ \text{(banks)}\qquad rr\ \text{(central bank)}$$

$$MB=(rr+e+c)D\ \Rightarrow\ D=\frac{MB}{rr+e+c}\qquad M=(1+c)D$$

$$\boxed{\ m=\frac{1+c}{rr+e+c}\ }\qquad\qquad M=m\times MB$$

*(Mishkin's numerical example, post-crisis, \$bn: $rr=0.10$, $C=1{,}200$, $D=1{,}600$, $ER=2{,}500$, so M1 $=\$2{,}800$bn.)*

$$c=\frac{1200}{1600}=\mathbf{0.75}\ ✓\qquad\qquad e=\frac{2500}{1600}=\mathbf{1.5625}\ \text{(book: 1.56)}\ ✓$$

| case | denominator | multiplier | Mishkin |
|---|---|---|---|
| **baseline** | **2.4125** | **0.72539** | 1.75/2.41 = **0.73** ✓ |
| $rr$ 0.10 → 0.15 | 2.4625 | 0.71066 | 1.75/2.46 = 0.71 ✓ |
| $e$ 1.56 → 3.00 | 3.8500 | 0.45455 | 1.75/3.85 = 0.45 ✓ |
| $c$ 0.75 → 1.50 | **3.1625** | **0.79051** | 2.50/**3.20** = 0.78 |

> [!note] The fourth case — investigated, not filed
> **Three of four reproduce exactly. The fourth prints a denominator of 3.20 where $0.10+1.56+1.50=3.16$** *(which gives 0.79, not 0.78)*.
>
> *(Diagnosed: **rounding $e$ to 1.60 instead of 1.56 reproduces both 3.20 and 0.78 exactly** — $0.10+1.60+1.50=3.20$ and $2.50/3.20=0.7812$.)*
>
> **⇒ an internal rounding inconsistency, not an arithmetic error**, and **the conclusion — that the multiplier *rises* — is unaffected either way.** **Rule 4: rule out alternative conventions before filing.** **Not filed.**

### 4. ⚠️ A multiplier of 0.73 — the "multiplier" that divides

$$m=\frac{1.75}{2.4125}=\mathbf{0.7254}$$

> [!warning] ⚠️ A \$1 increase in the monetary base raises M1 by 73 cents
> **The name "high-powered money" is false in this regime, and "multiplier" is a misnomer.** **The base is *low*-powered.**

**Two reasons the full multiplier falls short of the simple one:** **currency does not multiply**, and **excess reserves are reserves withheld from lending.** **Before 2008 the second was irrelevant** — Mishkin: $e$ was "almost always very close to zero (less than 0.001)" and the multiplier "was around 1.6".

> [!note] Checking his 1.6 against the formula
> *(With $e=0$ and $rr=0.10$, $m=1.6$ requires $c=1.40$ — a **higher** currency ratio than today's 0.75, which is right: before the crisis currency was large relative to checkable deposits. **His figure is consistent with the formula.**)*

**⚠️ Decomposing the collapse from 1.60 to 0.73 — Mishkin does not:**

| step | multiplier | change |
|---|---|---|
| pre-2008: $c=1.40$, $e=0.00$, $rr=0.10$ | **1.6000** | — |
| **then $e$ goes 0.00 → 1.5625** *(banks hoard)* | **0.7837** | **−0.8163** |
| then $c$ goes 1.40 → 0.75 | 0.7254 | −0.0583 |
| **TOTAL** | **0.7254** | **−0.8746** |

> [!warning] ⚠️ The excess-reserves ratio did 93% of the work
> **The collapse of the multiplier is a story about *bank* behaviour** — not about the central bank, and not about depositors.
>
> **Why did banks hoard?** **[[07 - Financial Crises|Ch. 07]] supplies the answer**: after a crisis, uncertainty is high and balance sheets are damaged — **and from 2008 the Fed began *paying interest on excess reserves*.** **⇒ holding reserves became a decision rather than a residual.**
>
> **⚠️ So the central bank lost control of the money supply without losing control of the monetary base.** **It still sets $MB$ precisely; the link from $MB$ to $M$ is what broke.**

### 5. ⚠️ The currency-ratio paradox — and its exact threshold

**Mishkin notes that raising $c$ from 0.75 to 1.50 makes the multiplier *rise*, and calls it "peculiar".** **Currency is supposed to leak *out* of deposit creation.** **He explains it verbally and stops.**

$$m=\frac{1+c}{rr+e+c}\qquad\Rightarrow\qquad \frac{dm}{dc}=\frac{(rr+e+c)-(1+c)}{(rr+e+c)^2}=\frac{rr+e-1}{(rr+e+c)^2}$$

$$\textbf{so }m\textbf{ falls in }c\textbf{ when }rr+e<1\textbf{, and RISES when }rr+e>1$$

*(Computed at $rr=0.10$:)*

| $e$ | $rr+e$ | $m$ at $c=0.75$ | $m$ at $c=1.50$ | |
|---|---|---|---|---|
| 0.0000 | 0.10 | 2.0588 | 1.5625 | falls |
| 0.5000 | 0.60 | 1.2963 | 1.1905 | falls |
| **0.9000** | **1.0000** | **1.0000** | **1.0000** | **flat** |
| 1.2000 | 1.30 | 0.8537 | 0.8929 | **RISES** |
| **1.5625** | 1.66 | **0.7254** | **0.7905** | **RISES** |
| 3.0000 | 3.10 | 0.4545 | 0.5435 | RISES |

> [!warning] ⚠️ At $e=0.90$ the multiplier is exactly 1 and completely insensitive to the currency ratio
> **Every value of $c$ gives $m=1.0000$** *(verified — both columns read 1.0000 on that row)*.
>
> **The intuition, sharpened from Mishkin's:** **when $rr+e>1$, a dollar sitting in a *deposit* immobilises more than a dollar of base** — $rr$ of required reserves *plus* $e$ of excess. **Moving it into currency *releases* that base.**
>
> **⚠️ So when banks hoard hard enough, deposits destroy money and currency creates it. The sign of every policy intuition flips.**
>
> **And this is the vault's pattern again: a comparative static that is "obvious" holds only inside a parameter region, and nothing in the formula announces the boundary.** *(Compare [[03 - The Behavior of Interest Rates|ch. 03]]'s business cycle, where the sign depends on which curve shifts more, and [[02 - The Meaning of Interest Rates|ch. 02]]'s duration, accurate only for small shocks.)*

### 6. Quantitative easing — what it did and did not do

**By 2017 the Fed's lending and asset-purchase programmes had produced "a quintupling of the Fed's balance sheet and an over 350% increase in the monetary base."**

> [!warning] ⚠️ If the multiplier had held, that would have been catastrophic
> *(Computed: with $MB$ up 350% — a factor of 4.5 — and the multiplier unchanged at 1.60, **M1 would have risen 350% too**. With the multiplier falling to 0.73, **M1 rose about 105%** instead — roughly a fifth of what a stable multiplier implies.)*
>
> **⇒ the "money printing will cause hyperinflation" prediction failed for a reason the model supplies: the base rose and the multiplier fell, very nearly offsetting.**
>
> **The Fed created reserves; the *banks* declined to turn them into deposits** — which is §1's three-player point, observed.

### 7. ⚠️ Discharging Macro/Micro ch. 12

**Three things the deferred material returns.**

**(1) The multiplier is not a constant and not a parameter.** **It is $m=(1+c)/(rr+e+c)$ — a function of three decisions by three different players.** **Treating it as fixed is exactly the error [[03 - The Behavior of Interest Rates|ch. 03]] warned about: assuming a sign the model does not deliver.**

**(2) ⚠️ It can be less than 1.** **The phrase "high-powered money" silently assumes $m>1$. Post-2008 it was 0.73.**

**(3) The quantity-theory forecast, run properly.** **[[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] gives $\text{inflation}=\%\Delta M-\%\Delta Y$ — but $\%\Delta M$ is not $\%\Delta MB$ unless $m$ is constant.**

*(Computed over 2007–2017, with the base rising over 350%:)*

| scenario | M1 factor | annualised | minus 2% real growth |
|---|---|---|---|
| **multiplier assumed constant** | ×4.500 | 16.23%/yr | **14.23%** |
| **multiplier falls 1.60 → 0.73** | ×2.053 | 7.46%/yr | **5.46%** |
| **actual US inflation** | | | **~1.8%/yr** |

> [!warning] ⚠️ Assuming a constant multiplier forecasts 14.2% inflation a year. Correcting for the collapse gives 5.5%. The truth was 1.8%.
> **This chapter closes about two-thirds of the gap.**
>
> **⚠️ And the rest is velocity.** *(From $MV=PY$: with $M\times2.05$, $P\times1.20$ and $Y\times1.22$, **velocity must have fallen 29% over the decade — about −3.4% a year.**)*
>
> **⇒ the quantity theory failed in two places at once, and this chapter repairs only one of them.** **The multiplier is not a constant (fixed here); velocity is not a constant either — which is [[11 - Money Demand and the Monetary Policy Framework|ch. 11]]'s job.** **Macro/Micro ch. 12 assumed both were stable.**
>
> **And this is finally the complete answer to [[01 - The Financial System and What Money Is|ch. 01]]'s question of why the Fed abandoned monetary targeting.** **Not merely because the M1/M2 boundary moved, but because *both* links — instrument to $M$, and $M$ to spending — are behavioural relationships that can, and did, collapse.**

### 8. Central bank structure and independence

*(Compressed — see the gaps callout. The results worth keeping:)*

| | |
|---|---|
| **for independence** | monetary policy has **long and variable lags**, so it is vulnerable to a **political business cycle** — expansion before an election, contraction after. And a government that can direct the central bank can finance deficits by printing money *(which is [[07 - Financial Crises|ch. 07]]'s path B)*. |
| **against** | an unelected body making decisions with large distributional consequences is undemocratic, and independence can shade into unaccountability. |

> [!note] ⚠️ The evidence Mishkin reports
> **More independent central banks deliver *lower inflation without worse real performance*.** **That is an empirical claim, and it is why the argument is largely settled in favour of *instrument* independence with a mandate set politically** — the government sets the goal, the central bank picks the tools.
>
> **And [[07 - Financial Crises|ch. 07]]'s emerging-market material is the counter-case: where central banks and supervisors lack independence *and* resources, powerful business interests capture them.** **⇒ independence is not only an anti-inflation device; it is an anti-capture device.**

## ✏️ Exercises

**1. (The base and the simple multiplier.)** (a) Who are the three players and what does each control? (b) Derive the simple deposit multiplier. (c) Why is it wrong?

> [!example]- Solution
> **(a) Central bank, banks, depositors.**
>
> | player | controls |
> |---|---|
> | **central bank** | $rr$, and $MB_n$ through open market operations |
> | **banks** | excess reserves $ER$, borrowed reserves $BR$ |
> | **depositors** | currency holdings $C$ |
>
> **$MB=C+R=MB_n+BR$ and $R=rr\cdot D+ER$.**
>
> **⚠️ The organising fact is that the money supply is a *joint outcome* of three independent sets of decisions, only one of which the central bank makes.** **[[01 - The Financial System and What Money Is|Ch. 01]] showed why this is not a technicality: currency is only 11.0% of M2**, so the overwhelming majority of money is created by the two players the central bank does not control.
>
> **(b) $D=(1/rr)\times R$.**
>
> **If banks hold no excess reserves and depositors no currency, all reserves are required reserves: $R=rr\cdot D$.** *(Verified with Mishkin's figures: at $rr=0.10$, \$1,600bn of deposits requires **\$160bn** of reserves, so \$160bn supports **ten times** itself.)*
>
> **The mechanism is multiple deposit creation** — bank A lends its excess reserves, the proceeds land at bank B, which keeps $rr$ and lends the rest. **⚠️ Nobody creates money deliberately; the *system* does, and no individual bank can observe it**, because each one only ever lends what it does not need to hold.
>
> **(c) Because it assumes away exactly what the other two players decide.**
>
> **Two leakages, both omitted:**
> - **currency undergoes no multiple expansion at all** — a dollar held as cash is a dollar, full stop;
> - **excess reserves are reserves that were not lent on**, so they support no further deposits.
>
> **⚠️ Both push the same way, so the simple multiplier is an *upper bound*, not an estimate.** **And §4 shows the gap is not academic: the bound is 10 and the actual value was 0.73** — off by a factor of fourteen.

**2. (Hard — the money multiplier.)** (a) Derive it. (b) Verify Mishkin's four cases. (c) What does $m<1$ mean?

> [!example]- Solution
> **(a) $m=(1+c)/(rr+e+c)$.**
>
> **Write $C=cD$ and $ER=eD$. Then**
> $$MB=rr\,D+eD+cD=(rr+e+c)D\quad\Rightarrow\quad D=\frac{MB}{rr+e+c}$$
> **and since $M=D+C=(1+c)D$,**
> $$M=\frac{1+c}{rr+e+c}\times MB$$
>
> **Each player owns one symbol: $rr$ the central bank, $e$ the banks, $c$ the depositors.**
>
> **(b) Three of four exactly; the fourth is a rounding inconsistency.**
>
> *(Verified: $c=1200/1600=0.75$ ✓, $e=2500/1600=1.5625$ ✓ against the book's 1.56.)*
>
> | case | computed | Mishkin |
> |---|---|---|
> | baseline | 1.75/**2.4125** = **0.7254** | 1.75/2.41 = 0.73 ✓ |
> | $rr\to0.15$ | 1.75/2.4625 = 0.7107 | 1.75/2.46 = 0.71 ✓ |
> | $e\to3.00$ | 1.75/3.8500 = 0.4545 | 1.75/3.85 = 0.45 ✓ |
> | $c\to1.50$ | 2.50/**3.1625** = **0.7905** | 2.50/**3.20** = 0.78 |
>
> **The fourth denominator should be $0.10+1.56+1.50=3.16$, not 3.20.** *(Diagnosed: **rounding $e$ to 1.60 reproduces both 3.20 and 0.78 exactly.**)*
>
> **⚠️ Not filed as an erratum.** **It is an internal rounding inconsistency — the same class as [[02 - The Meaning of Interest Rates|ch. 02]]'s two annualisation conventions in one footnote — and rule 4 requires ruling out alternative conventions first.** **The conclusion (the multiplier *rises*) is unaffected either way.**
>
> **(c) That the monetary base is *low*-powered.**
>
> **A \$1 increase in the base raises M1 by 73 cents.** **"High-powered money" is false in this regime and "multiplier" is a misnomer** — it divides.
>
> **⚠️ And this is not a curiosity.** **Every textbook statement of the form "the central bank expands the base, so the money supply expands by a multiple" carries an unstated condition, $rr+e+c<1+c$, i.e. $rr+e<1$.** **When banks hoard, the condition fails**, and it failed for roughly a decade in the largest economy in the world.

**3. (Hard — the collapse.)** (a) Check Mishkin's pre-2008 multiplier of 1.6. (b) Decompose the fall to 0.73. (c) Why did banks hoard, and what does it mean for policy?

> [!example]- Solution
> **(a) It is consistent — it implies $c=1.40$.**
>
> **With $e\approx0$ and $rr=0.10$, solving $(1+c)/(0.10+c)=1.6$ gives $c=1.40$.** **That is a *higher* currency ratio than today's 0.75, which is correct: before the crisis currency was large relative to checkable deposits.** **So his stated 1.6 checks out against the formula rather than merely being asserted.**
>
> *(Note the direction: with $e=0$, $m$ is **decreasing** in $c$ — the normal case — so a high pre-crisis $c$ is what makes 1.6 rather than something larger.)*
>
> **(b) The excess-reserves ratio did 93% of it.**
>
> | step | $m$ | change |
> |---|---|---|
> | pre-2008 ($c=1.40$, $e=0$) | **1.6000** | — |
> | **$e$: 0 → 1.5625** | **0.7837** | **−0.8163** |
> | $c$: 1.40 → 0.75 | 0.7254 | −0.0583 |
>
> **⚠️ The collapse is a story about *bank* behaviour.** **Neither the central bank's instrument nor depositors' choices account for it.**
>
> **(c) Because holding reserves stopped being a residual and became a decision.**
>
> **[[07 - Financial Crises|Ch. 07]] supplies two reasons — uncertainty is high after a crisis, and balance sheets are damaged — and there is a third: from 2008 the Fed began *paying interest on excess reserves*.** **A bank comparing a risky loan against a safe, liquid, interest-bearing reserve balance may rationally choose the reserve.**
>
> **⚠️ For policy the consequence is sharp: the central bank lost control of the money supply without losing control of the monetary base.** **It still sets $MB$ to the dollar. What broke is the *link* from $MB$ to $M$** — and that link is a behavioural relationship owned by someone else.
>
> **This is why [[09 - Tools and Conduct of Monetary Policy|ch. 09]] cannot treat the base as the policy variable**, and it is the same lesson [[03 - The Behavior of Interest Rates|ch. 03]] taught about the interest rate: **the thing the central bank controls and the thing it cares about are connected by a relationship that can move.**

**4. (Hard — the paradox.)** (a) Why does raising the currency ratio *raise* the multiplier? (b) Find the exact threshold. (c) What general lesson?

> [!example]- Solution
> **(a) Because when banks hoard hard enough, a deposit immobilises more base than a banknote does.**
>
> **Normally currency is a leakage: a dollar held as cash supports \$1 of money supply, while a dollar deposited supports \$1/$rr$.** **So a higher $c$ lowers $m$.**
>
> **⚠️ But a deposit ties up $rr+e$ dollars of base per dollar of deposit.** **When $rr+e>1$, that is *more than the dollar itself*.** **Moving a dollar from a deposit into currency therefore *releases* base, which supports more deposits elsewhere — and the multiplier rises.**
>
> **(b) $dm/dc$ has the sign of $rr+e-1$; the threshold is $e=1-rr=0.90$.**
>
> $$\frac{dm}{dc}=\frac{(rr+e+c)-(1+c)}{(rr+e+c)^2}=\frac{rr+e-1}{(rr+e+c)^2}$$
>
> **The denominator is always positive, so the sign is entirely $rr+e-1$.**
>
> | $e$ | $rr+e$ | $m(c{=}0.75)$ | $m(c{=}1.50)$ | |
> |---|---|---|---|---|
> | 0.00 | 0.10 | 2.0588 | 1.5625 | falls |
> | **0.90** | **1.00** | **1.0000** | **1.0000** | **flat** |
> | 1.5625 | 1.66 | 0.7254 | 0.7905 | **rises** |
>
> **⚠️ At $e=0.90$ the multiplier equals exactly 1 for *every* value of $c$** *(verified)*. **The currency ratio becomes completely irrelevant** — which makes sense, since at that point a dollar supports exactly one dollar of money whether it is held as cash or as a deposit.
>
> **Mishkin gets the direction right verbally and never writes the derivative**, so he cannot say *where* the switch happens or that $m=1$ is the pivot.
>
> **(c) That an "obvious" comparative static may hold only inside a parameter region, and nothing announces the boundary.**
>
> **"Currency leaks out of deposit creation" is taught as a fact. It is a fact for $rr+e<1$ and false otherwise**, and no textbook statement of it carries the condition.
>
> **⚠️ Third instance of this pattern in the subject.** **[[03 - The Behavior of Interest Rates|Ch. 03]]: the effect of a business-cycle expansion on interest rates depends on which curve shifts more.** **[[02 - The Meaning of Interest Rates|Ch. 02]]: duration is accurate only for small shocks.** **Here: the currency ratio's effect depends on $rr+e$ versus 1.**
>
> **The common structure is that a result derived under implicit parameter assumptions gets remembered without them** — and the assumption is usually the *normal* case, so the failure arrives precisely when conditions are abnormal and the answer matters most.

**5. (Hard — the discharge.)** (a) What did QE do to the money supply? (b) Run the quantity theory properly. (c) What does this say about Macro/Micro ch. 12?

> [!example]- Solution
> **(a) It expanded the base enormously and the money supply far less.**
>
> **By 2017 the Fed's balance sheet had *quintupled* and the monetary base risen *over 350%*.**
>
> *(Computed: with $MB$ ×4.5 and the multiplier unchanged at 1.60, M1 would also have risen 350%. With the multiplier falling to 0.73, **M1 rose about 105%** — roughly a fifth of what a stable multiplier implies.)*
>
> **⚠️ The base rose and the multiplier fell, very nearly offsetting.** **The Fed created reserves; the banks declined to turn them into deposits** — §1's three-player point observed in the largest monetary experiment on record.
>
> *(This is also why the widely-predicted hyperinflation did not arrive. **The prediction was not foolish — it followed from the standard model with one parameter held fixed.** It failed because that parameter was not a parameter.)*
>
> **(b) Two corrections are needed, and this chapter supplies only one.**
>
> | scenario | M1 factor | annualised | minus 2% real |
> |---|---|---|---|
> | multiplier assumed constant | ×4.500 | 16.23%/yr | **14.23%** |
> | multiplier falls 1.60 → 0.73 | ×2.053 | 7.46%/yr | **5.46%** |
> | **actual inflation** | | | **~1.8%/yr** |
>
> **Assuming a constant multiplier forecasts 14.2% inflation a year; correcting gives 5.5%; the truth was 1.8%.** **⇒ this chapter closes about two-thirds of the gap.**
>
> **⚠️ The remainder is velocity.** *(From $MV=PY$ with $M\times2.05$, $P\times1.20$, $Y\times1.22$: **velocity fell 29% over the decade, about −3.4% a year.**)*
>
> **(c) That it assumed two things were stable and both moved.**
>
> **[[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] deferred the money multiplier here and treated velocity as stable.** **Both assumptions failed simultaneously**, and each accounts for roughly half the forecast error.
>
> **⚠️ The right conclusion is not that the quantity theory is wrong.** **$MV=PY$ is an identity; the theory is the claim that $V$ is stable and that $M$ is controllable.** **This chapter shows the second claim fails; [[11 - Money Demand and the Monetary Policy Framework|ch. 11]] examines the first.**
>
> **And it completes [[01 - The Financial System and What Money Is|ch. 01]]'s answer.** There, the Fed abandoned monetary targeting because financial innovation moved assets across the M1/M2 boundary — *a measurement problem*. **Here we can say more: even with a perfectly measured $M$, targeting requires that the central bank can *hit* it (this chapter) and that hitting it *matters* (ch. 11).** **⚠️ All three conditions must hold, and between 2008 and 2017 none of them did.**

## 📝 Summary

- **Three players** — the central bank sets $rr$ and $MB_n$; **banks** choose excess reserves; **depositors** choose currency. **⚠️ The money supply is a joint outcome of three independent decisions.**
- **$MB=C+R=MB_n+BR$**, called **high-powered money** — **⚠️ a name that assumes $m>1$.**
- **The simple deposit multiplier is $1/rr$** *(verified: \$160bn of reserves supports \$1,600bn of deposits at $rr=0.10$)* — **but it assumes away both leakages, so it is an upper bound, not an estimate.**
- **⚠️ $m=(1+c)/(rr+e+c)$**, and **each player owns one symbol.**
- **Mishkin's four cases verified** — 0.73, 0.71, 0.45 exactly. **The fourth prints a denominator of 3.20 where 3.16 is correct; diagnosed as rounding $e$ to 1.60, so not filed.**
- **⚠️ The multiplier was 0.7254 — below one.** **A \$1 increase in the base raises M1 by 73 cents.**
- **⚠️ Decomposed: the excess-reserves ratio did 93% of the collapse from 1.60** *(computed)* — **a story about bank behaviour, not about the central bank.**
- **Banks hoarded because reserves became a *decision*** — high uncertainty, damaged balance sheets, and **interest paid on excess reserves from 2008.**
- **⚠️ The central bank lost control of the money supply without losing control of the base.** The *link* broke.
- **⚠️ The currency-ratio paradox solved: $dm/dc$ has the sign of $rr+e-1$** *(computed)* — **so the threshold is $e=1-rr=0.90$, at which $m=1.0000$ for every $c$.**
- **⚠️ When banks hoard hard enough, deposits destroy money and currency creates it** — the sign of the standard intuition flips, **and nothing in the formula announces the boundary.**
- **QE: the base rose over 350% and M1 about 105%** *(computed)* — **the base rose and the multiplier fell, very nearly offsetting.**
- **⚠️ THE DISCHARGE: assuming a constant multiplier forecasts 14.2% inflation a year; correcting gives 5.5%; the truth was 1.8%** *(computed)*.
- **⚠️ The remainder is velocity, which fell 29% over the decade** *(computed)* — **so the quantity theory failed in two places and this chapter repairs one.** **[[11 - Money Demand and the Monetary Policy Framework|Ch. 11]] handles the other.**
- **Monetary targeting requires three things**: a stable measure ([[01 - The Financial System and What Money Is|ch. 01]]), a controllable $M$ (**this chapter**), and a stable $V$ (ch. 11). **⚠️ Between 2008 and 2017 none held.**
- **Independence: the case is the political business cycle and deficit monetisation; the evidence is lower inflation without worse real performance.** **Modern practice splits *goal* (political) from *instruments* (central bank).**
- **⚠️ Independence is also an anti-*capture* device** — [[07 - Financial Crises|ch. 07]]'s emerging-market case.

## ⚠️ Important Notes

1. **⚠️ The central bank is one of three players.** Any statement beginning "the central bank sets the money supply" is wrong.
2. **The base is what the central bank actually controls.** The money supply is not.
3. **⚠️ "High-powered money" is a claim, not a definition** — it presumes $m>1$.
4. **The simple deposit multiplier is an upper bound.** Both omitted leakages reduce it.
5. **Multiple deposit creation is a system property.** No individual bank creates money.
6. **⚠️ Each symbol in $m$ has an owner.** $rr$ the central bank, $e$ the banks, $c$ the depositors.
7. **⚠️ $m$ can be below 1.** It was 0.73.
8. **The multiplier's collapse was 93% excess reserves** — diagnose before prescribing.
9. **Interest on excess reserves turns hoarding into a rational choice**, not a symptom.
10. **⚠️ Controlling the instrument is not controlling the target.**
11. **⚠️ $dm/dc$ has the sign of $rr+e-1$.** Memorise the condition, not the conclusion.
12. **At $rr+e=1$ the multiplier is exactly 1 and $c$ is irrelevant.**
13. **⚠️ A "known" comparative static may hold only in a parameter region** — third instance in this subject.
14. **QE expanded the base, not the money supply**, because the multiplier moved the other way.
15. **⚠️ The hyperinflation forecast failed because a parameter was assumed, not measured.**
16. **The quantity theory needs $M$ controllable *and* $V$ stable.** Both failed.
17. **⚠️ Monetary targeting needs three conditions**, and it is abandoned when any one fails.
18. **Independence means *instrument* independence** — the goal is set politically.
19. **⚠️ Independence protects against capture as well as against inflation.**

> [!warning] Gaps in the source material
> **Extraction was good.** **The derivation of the multiplier, all four numerical cases, the balance-sheet T-accounts and Summary Table 1 all came through.**
>
> **⚠️ SUMMARY TABLE 1 (which player changes which variable, and the money-supply response) survived complete** — five rows with directions and reasons. **Seventh confirmation of the vault's rule: graphical exhibits are lost; tables set as text survive whole.** *(Its content is reproduced in §1 and §3.)*
>
> **⚠️ The parenthesis fault appears in the displayed algebra** — `c = 5C>D6` is $c=\{C/D\}$ and `m = 1 + c / rr + e + c` is $(1+c)/(rr+e+c)$. **Every formula here was reconstructed from the prose and then checked against Mishkin's own four worked multipliers**; three reproduce exactly and the fourth is diagnosed above, **so the reconstruction is verified rather than assumed.**
>
> **Both figures in ch. 15 are lost** — **Figure 1 (M1 and the monetary base, 2007–2017)** and **Figure 2 (excess reserves and the currency ratio, 2007–2017)**. **⚠️ These are the empirical heart of the QE application**, and the prose does not name their data points *(checked, per [[03 - The Behavior of Interest Rates|ch. 03]]'s rule)*. **Only the stated magnitudes are retained** — the balance sheet quintupling, the base rising over 350%, excess reserves exceeding \$2 trillion, the pre-2008 excess-reserves ratio below 0.001 and multiplier "around 1.6". **§6's arithmetic is built on those stated figures**, and §7's velocity residual uses standard US price and output growth over the period, **flagged as my inputs rather than Mishkin's.**
>
> **Ch. 14's organisational diagrams** (Figures 1–2, the ESCB's structure and its allocation of policy tools) **are schematics whose content is verbal; §8 compresses rather than reconstructs them.**
>
> **No erratum found.** **⚠️ One discrepancy investigated and NOT filed** *(§3)*: the fourth multiplier case prints $0.10+1.56+1.50=3.20$ where the sum is 3.16. *(Diagnosed: **rounding $e$ to 1.60 reproduces both 3.20 and 0.78 exactly.**)* **An internal rounding inconsistency, not an arithmetic error, and the conclusion is unaffected — the same class as [[02 - The Meaning of Interest Rates|ch. 02]]'s two annualisation conventions in one footnote.** **Recorded in [[00-Index]].**
>
> **⚠️ SCOPE NOTE — two chapters in one note, so ch. 14 is heavily compressed.** **Deliberately reduced to §8:** the origins of central banking; the detailed structure of the ESCB, the Federal Reserve System, the Bank of England, the Bank of Japan and the Bank of Canada; the boxes on central bank ownership, the Bundesbank's role, Brexit and the BoE, and non-euro EU central banks; and the structure of central banks in emerging market economies. **These are institutional description rather than analysis, they are jurisdiction-specific, and none of it is required by the chapters that follow.** **What is retained is the *independence* argument and its evidence, because [[09 - Tools and Conduct of Monetary Policy|ch. 09]] and [[12 - Monetary Policy Theory, Expectations and Transmission|ch. 12]] both use it.**
>
> **Additions beyond the source.**
>
> - **⚠️ §4's decomposition is mine and it is the note's most useful addition.** **Mishkin states that the multiplier was "around 1.6" before 2008 and is 0.73 now, and never connects the two figures.** **Checking that 1.6 is consistent with his own formula (it implies $c=1.40$), then decomposing the fall, shows the excess-reserves ratio did 93% of the work** — which converts "the multiplier fell" into "banks stopped lending reserves out", a statement about an identifiable actor.
> - **⚠️ §5's derivative is mine, and it answers a question Mishkin explicitly raises and leaves.** **He calls the currency-ratio result "peculiar" and explains it in words.** **Computing $dm/dc=(rr+e-1)/(rr+e+c)^2$ gives the exact threshold $rr+e=1$ and the fact that $m\equiv1$ there regardless of $c$** — neither of which can be seen from the verbal argument.
> - **⚠️ §7 is written to discharge [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s forward reference, and the three-way quantity-theory comparison is mine.** **Mishkin never runs the quantity theory through his own multiplier.** **The finding that this chapter closes two-thirds of the gap and that the residual is a 29% fall in velocity is my synthesis** — and it is what identifies [[11 - Money Demand and the Monetary Policy Framework|ch. 11]] as the other half of the repair. *(The velocity residual uses standard US price and output growth for 2007–2017; those inputs are mine, not the book's.)*
> - **§6's counterfactual — what M1 would have done had the multiplier held — is mine.** Mishkin describes the QE application qualitatively.
> - **§2's framing of the simple multiplier as an *upper bound* rather than an approximation is mine.**
> - **The identification of §5 as the third instance of "a comparative static that holds only in a parameter region", and of monetary targeting as requiring three separate conditions (stable measure, controllable $M$, stable $V$), are my syntheses.**

**Previous:** [[07 - Financial Crises]] · **Next:** [[09 - Tools and Conduct of Monetary Policy]]
