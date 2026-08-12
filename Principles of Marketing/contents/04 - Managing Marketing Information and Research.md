---
subject: Principles of Marketing
chapter: 4
tags: [ds, marketing, marketing-research, sampling, ab-testing, big-data, marketing-analytics, crm]
source: "Kotler & Armstrong, *Principles of Marketing*, Pearson 2017, ch. 4"
---

# Managing Marketing Information and Research

> [!warning] ⚠️ THE DS-CRITICAL CHAPTER
> **This is where marketing meets the rest of the degree.** **Kotler describes causal research as an experiment, sampling as a choice of "type", and analytics as "digging out meaningful patterns" — and supplies no statistics for any of the three.** **The vault already holds all of them, and [[00-Index]] flagged this chapter as the place to connect them.**

**Four results.**

**§3 — ⚠️ Kotler's causal research *is* an A/B test, described correctly and completely, with no sample size.** *(Computed: detecting a **half-point lift on a 5% baseline needs ~31,000 per group**. And $n\propto1/\delta^2$, so **halving the effect you want to detect quadruples the sample**.)*

**§4 — ⚠️ the line between his probability and nonprobability samples is not a menu choice, it is a hard boundary.** **A nonprobability sample has no sampling distribution, so *no margin of error can be computed from it at all*.** **A convenience sample of 10,000 supports less inference than a probability sample of 400.**

**§5 — ⚠️ "digging out meaningful patterns in big data" manufactures false positives.** *(Computed: testing **20 segments gives a 64.2% chance** of a "significant" result when nothing is happening; **1,000 segments yields 50 expected false hits**.)*

**§7 — the public-policy section has aged best**, and the asymmetry is the one a DS graduate will stand in: **consumers consent to the *collection* and almost never to the *inference*.**

## 📘 Main Knowledge

### 1. The marketing information system — three sources

**An MIS *assesses* information needs, *develops* the needed information, and *delivers insights*.**

> [!warning] ⚠️ Kotler's opening point is the opposite of what students expect
> **The problem is not too little data.**
> - **"Simply collecting and storing huge amounts of data has little value."**
> - **"It's actually [about getting] big *insights* from big data. It's throwing away 99.999 percent of that data to find things that are actionable."**
> - **⚠️ "*Right* data trumps *big* data."**

| source | |
|---|---|
| **internal databases** | cheap and already yours — **but collected for *other* purposes** (accounting, operations), so often incomplete, stale and in the wrong form. **The cost is zero and the fit is poor.** |
| **competitive marketing intelligence** | systematic monitoring of publicly available information about competitors and the market |
| **marketing research** | the systematic design, collection, analysis and reporting of data relevant to a **specific situation** |

> [!note] ⚠️ Only the third can be *designed*
> **Marketing research is the only source commissioned to answer a particular question** — which is why the rest of the chapter is about it, and why §2's first step is the hardest.

### 2. The four-step research process — and the three objectives

1. **Define** the problem and research objectives
2. **Develop** the research plan
3. **Implement** — collect and analyse
4. **Interpret** and report

> [!warning] ⚠️ Kotler: step 1 is "often the hardest step"
> **Managers know something is wrong without knowing the cause — and a perfectly executed study of the wrong question is worthless.** **This is [[01 - Marketing, Customer Value and Engagement|ch. 01]]'s marketing myopia inside the research process.**

| objective | what it does | best method |
|---|---|---|
| **exploratory** | gather preliminary information that helps **define** the problem and **suggest hypotheses** | **observation** |
| **descriptive** | describe things — market potential, demographics, attitudes. **Answers "what" and "how many"** | **survey** |
| **causal** | test hypotheses about **cause and effect** | **experiment** |

> [!warning] ⚠️ The three are a pipeline, not a menu
> **Exploratory generates the hypothesis, descriptive measures its prevalence, causal tests whether it is *true*.**
>
> **Skipping to descriptive gives precise measurements of the wrong quantity. Stopping before causal gives correlations.**
>
> *(Kotler's own matching is exactly right: "observation is best suited for exploratory research, surveys… for descriptive research, [experiments] for causal information." **The pipeline reading is what makes §5's multiplicity problem tractable** — see below.)*

### 3. ⚠️ Causal research is an A/B test — and there are no statistics in the chapter

**Kotler's own definition of experimental research:**

> **"selecting *matched groups* of subjects, giving them *different treatments*, *controlling* unrelated factors, and *checking for differences* in group responses."**

**⚠️ That is an A/B test, described correctly and completely — and then he says nothing about how many subjects, how big a difference counts, or how often you will be wrong.** *(His only guidance is **"large samples give more reliable results than small samples"** — true, and unusable.)*

$$n\ \text{per group}=\frac{2\left(z_{\alpha/2}+z_\beta\right)^2\bar p(1-\bar p)}{\delta^2}$$

*(Computed at 80% power, $\alpha=0.05$ two-sided:)*

| baseline | lift to detect | **n per group** | total | weeks at 1,000/day |
|---|---|---|---|---|
| 5% | 1.0 pts | **8,159** | 16,318 | 2.3 |
| **5%** | **0.5 pts** | **31,235** | 62,469 | **8.9** |
| 5% | 0.2 pts | **189,939** | 379,878 | **54.3** |
| 2% | 0.5 pts | 13,810 | 27,620 | 3.9 |
| 20% | 2.0 pts | 6,511 | 13,021 | 1.9 |
| 20% | 1.0 pts | 25,583 | 51,167 | 7.3 |

> [!warning] ⚠️ Detecting a half-point lift on a 5% baseline needs about 31,000 people per group
> **A focus group of eight cannot detect anything. A survey of 400 can only detect very large effects.**
>
> **And note the shape: $n\propto1/\delta^2$, so ⚠️ *halving the effect you want to detect quadruples the sample*.** **That single fact governs whether a test is worth running**, and it is why "let's just try it and see" fails for small improvements.

> [!warning] ⚠️ The corollary Kotler's framework cannot reach
> **An experiment that is too small does not give a *weak* answer — it gives a *random* one.**
>
> **Underpowered tests do not err toward "no effect".** **When they *do* reach significance, the estimated effect is *inflated*, because only large sample-noise excursions clear the bar.** **⇒ a small test that "worked" is the most dangerous result of all.**
>
> *(The apparatus is [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics ch. 07]]'s, and the design question — how to allocate subjects — is [[Data Preparation and Visualization/contents/00-Index|Data Preparation]]'s.)*

### 4. ⚠️ The sampling plan — and the boundary Kotler states as a "type"

**Three questions: *who* (the sampling unit), *how many* (sample size), *how chosen* (sampling procedure).** *(Table 4.2, which survived extraction complete:)*

| class | type | what it means |
|---|---|---|
| **probability** | **simple random** | every member has a **known and equal** chance |
| **probability** | **stratified random** | population split into mutually exclusive groups; random samples from each |
| **probability** | **cluster (area)** | population split into groups; a sample **of groups** is drawn |
| **nonprobability** | convenience | the **easiest** members to obtain information from |
| **nonprobability** | judgment | members the researcher **judges** to be good prospects |
| **nonprobability** | quota | a **prescribed number** in each of several categories |

> [!warning] ⚠️ Kotler presents these as six options on a menu. They are not.
> **The line between the two blocks is a hard boundary, and it is the most important thing in this chapter for a Data Science reader.**
>
> - **A *probability* sample has a known selection probability for every member.** **That is what makes a *sampling distribution* exist — and therefore what makes a confidence interval, a standard error and a p-value mean anything.**
> - **A *nonprobability* sample has none.** **⚠️ So no margin of error can be computed from it — not a large one, *not any*.** **The arithmetic can still be performed and the output is not an estimate of anything.**
>
> **⇒ a convenience sample of 10,000 supports no inference that a probability sample of 400 would not support better. *Size does not repair selection.*** **And §3's arithmetic assumed probability sampling throughout — every number in it is void otherwise.**

> [!note] The honest use of nonprobability samples
> **They are *exploratory* (§2): they generate hypotheses.** **Kotler's focus groups are a nonprobability method and he correctly calls that work *qualitative*.** **⚠️ The error is not *using* them — it is *quoting a percentage from one*.**

### 5. ⚠️ Testing many things at once — the failure mode of "big data"

**Kotler's analytics section is about "digging out meaningful patterns in big data".** **⚠️ Digging through enough data guarantees patterns whether or not any are real, and he does not say so.**

*(Computed — $k$ independent tests at $\alpha=0.05$ on hypotheses that are **all false**:)*

| segments tested | **P(at least one false "discovery")** | expected false hits |
|---|---|---|
| 1 | 5.0% | 0.1 |
| 10 | 40.1% | 0.5 |
| **20** | **64.2%** | 1.0 |
| 50 | 92.3% | 2.5 |
| 100 | 99.4% | 5.0 |
| **1,000** | **100.0%** | **50.0** |

> [!warning] ⚠️ Test twenty segments and you are more likely than not to find a "significant" one even if nothing is happening
> **Test a thousand and you expect fifty.** **That is not a flaw in the data — it is what $\alpha$ *means*.**
>
> **⇒ "right data trumps big data" is truer than Kotler's source knows.** **His quote treats the discarded 99.999% as *waste*. It is worse than waste — *searching it* is what manufactures the false positives.**
>
> **The discipline required is not better mining. It is deciding the hypothesis *before* looking — §2's exploratory → causal pipeline — or correcting for the number of looks.**

> [!note] Which is why §2's ordering matters rather than being a taxonomy
> **Exploratory research is *allowed* to trawl precisely because its output is a hypothesis to be tested on *fresh* data, not a conclusion.**

### 6. Research approaches, contact methods, instruments

| approach | gets at | limit |
|---|---|---|
| **observational** *(incl. **ethnographic**)* | **what people DO**, not what they say | **feelings, attitudes and motives "cannot be observed"**; long-run or infrequent behaviour is impractical |
| **survey** | **descriptive** information — the most widely used | people **cannot** answer, **won't** answer, or answer **to seem helpful or clever** |
| **experimental** | **causal** — §3 | sample size, and everything in §3 |

> [!warning] ⚠️ The survey limits are bias sources, and the third is not fixed by a larger sample
> **"Answering to seem helpful or clever" is *social desirability bias*.** **It is a *systematic* error, so it does not shrink with $n$** — a bigger survey measures the same wrong thing more precisely.

**Contact methods**: mail, telephone, personal (individual and **focus group**), **online**. **Online is cheapest and fastest, and ⚠️ its weakness is precisely §4's — who is on your list, and who chose to respond.**

**Instruments**:

| | |
|---|---|
| **closed-ended questions** | choices given; **easy to interpret and tabulate** — for **descriptive** work |
| **open-ended questions** | own words; **"often reveal more"** and are **"especially useful in exploratory research"** |

> [!note] The choice of question type is the objective again
> **Open for exploratory, closed for descriptive.** *(And Kotler's wording rules are real methodology: simple, direct, unbiased wording; logical order; interest first; **difficult and personal questions last** "so that respondents do not become defensive.")*

**Mechanical instruments**: people meters, checkout scanners, GPS tracking, and **neuromarketing** — EEG and MRI plus biometrics *(heart rate, respiration, sweat, facial and eye movement)*.

> [!warning] ⚠️ Neuromarketing is the purest case of §5's hazard
> **Many channels, many time points, small samples.** **Kotler's Shelter Pet example reads *second-by-second* EEG and eye-tracking across a whole advertisement** — **that is hundreds of implicit comparisons per subject.** **Treat such findings as exploratory.**

### 7. CRM, big data, and the public-policy problem

**Customer relationship management (CRM)** = **"managing detailed information about individual customers and carefully managing customer *touch points* to maximize customer loyalty."**

> [!note] ⚠️ CRM is ch. 01's customer lifetime value made operational
> **You cannot compute CLV per customer without customer-level data** — and **[[01 - Marketing, Customer Value and Engagement|ch. 01]] §4 showed the CLV number is only as good as its retention estimate**, which is exactly what CRM data supplies.

**Marketing analytics** = **"the analysis tools, technologies, and processes by which marketers dig out meaningful patterns in big data to gain customer insights and gauge marketing performance."**

> [!note] Kotler's examples are named DS problems, unnamed
> **His Netflix case is a *recommender system*; his Kraft case is *segmentation and targeting*.** **Neither is identified as such** — the connections are [[00-Index]]'s enrichment plan, developed in [[07 - Segmentation, Targeting and Positioning|ch. 07]] and [[12 - Integrated Marketing Communications and Digital Marketing|ch. 12]].

**The public-policy section is the one that has aged best, and it sits last.** **Kotler's own caption on behavioural targeting — *"sophisticated online research or 'just a little creepy'?"* — is the whole modern privacy debate in one line.** **He separates two harms:**

| | |
|---|---|
| **intrusion on privacy** | being tracked at all |
| **misuse of findings** | what is done with the inference |

> [!warning] ⚠️ And the asymmetry is where a Data Science graduate will be standing
> **Consumers consent to the *collection* and almost never to the *inference*.** **Nothing in a cookie notice says "we will deduce your pregnancy from your purchases."**
>
> **⇒ the ethical question sits with the *analytics*, not the data capture** — which is precisely the job this degree trains for.

## ✏️ Exercises

**1. (The process.)** (a) Give the four steps and three objectives. (b) Why is step 1 hardest? (c) Match methods to objectives.

> [!example]- Solution
> **(a)** **Define the problem and objectives → develop the research plan → implement → interpret and report.** **Objectives: exploratory (define the problem, suggest hypotheses), descriptive (what and how many), causal (cause and effect).**
>
> **(b) Because a perfectly executed study of the wrong question is worthless.**
>
> **Kotler calls it "often the hardest step": managers know something is wrong without knowing the cause.** **⚠️ This is [[01 - Marketing, Customer Value and Engagement|ch. 01]]'s marketing myopia inside the research process** — asking "why are sales of our drill bits falling?" when the question is "are people still buying holes?"
>
> **And the failure is invisible downstream: steps 2–4 can all be executed impeccably on a badly framed question, and nothing in the output announces the problem.**
>
> **(c) Observation → exploratory; survey → descriptive; experiment → causal.**
>
> **⚠️ But the three objectives are a *pipeline*, not a menu.** **Exploratory generates a hypothesis, descriptive measures its prevalence, causal tests whether it is true.**
>
> - **Skipping to descriptive** gives precise measurement of the wrong quantity.
> - **Stopping before causal** gives correlations — and §5 shows why that is worse than it sounds, since trawling data guarantees correlations.
>
> *(The pipeline reading is also what makes exploratory work legitimate: it is *allowed* to trawl because its output is a hypothesis to be tested on fresh data.)*

**2. (Hard — causal research.)** (a) What is Kotler's definition, and what is missing? (b) Compute the sample sizes. (c) What is the danger of a small test?

> [!example]- Solution
> **(a) It is a correct and complete description of an A/B test, with no statistics.**
>
> **"Selecting *matched groups* of subjects, giving them *different treatments*, *controlling* unrelated factors, and *checking for differences* in group responses."** **Every element of experimental design is there — randomisation into comparable groups, a manipulated variable, control of confounders, and a comparison.**
>
> **⚠️ What is missing is everything quantitative: how many subjects, how large a difference counts as a difference, and how often the procedure will mislead you.** **His only guidance — "large samples give more reliable results than small samples" — is true and unusable.**
>
> **(b)** $n\ \text{per group}=2(z_{\alpha/2}+z_\beta)^2\bar p(1-\bar p)/\delta^2$, at 80% power and $\alpha=0.05$:
>
> | baseline | lift | **n per group** |
> |---|---|---|
> | 5% | 1.0 pt | **8,159** |
> | **5%** | **0.5 pt** | **31,235** |
> | 5% | 0.2 pt | **189,939** |
> | 20% | 1.0 pt | 25,583 |
>
> **⚠️ Detecting a half-point lift on a 5% baseline needs about 31,000 per group — 62,000 in total, or nine weeks at a thousand subjects a day.**
>
> **And the shape matters more than any single row: $n\propto1/\delta^2$, so *halving the detectable effect quadruples the sample*.** **That is what decides whether a test is worth running at all**, and it is why small improvements cannot be validated by "trying it and seeing".
>
> **(c) It gives a random answer, not a weak one — and an inflated one when it "works".**
>
> **⚠️ Underpowered tests do not err toward "no effect".** **When they do reach significance, the estimated effect is *exaggerated*, because only large excursions of sampling noise clear the threshold.**
>
> **⇒ a small test that came out positive is the most dangerous result available**: it is simultaneously the least reliable and the most likely to be acted on. **Kotler's framework has no way to express this**, because it has no concept of power. *(The apparatus is [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics ch. 07]]'s.)*

**3. (Hard — sampling.)** (a) Give the six types. (b) What separates the two blocks? (c) Does a big convenience sample help?

> [!example]- Solution
> **(a)** **Probability: simple random, stratified random, cluster.** **Nonprobability: convenience, judgment, quota.**
>
> **(b) Whether a selection probability exists — and it is a hard boundary, not a preference.**
>
> **A probability sample has a *known* selection probability for every population member.** **⚠️ That is what makes a sampling distribution exist — and therefore what makes a standard error, a confidence interval and a p-value refer to anything.**
>
> **A nonprobability sample has no such probability.** **So there is no sampling distribution, and ⚠️ *no margin of error can be computed from it at all* — not a large one, not any.**
>
> **The arithmetic can still be performed.** **A convenience sample will happily yield "62% ± 3%", and the ±3% is not wrong so much as *meaningless*: it answers a question about a random sample that was never drawn.**
>
> **(c) No. ⚠️ Size does not repair selection.**
>
> **A convenience sample of 10,000 supports no inference that a probability sample of 400 would not support better.** **Increasing $n$ shrinks *sampling* error, which a nonprobability sample does not have in a usable form; it does nothing to *selection* bias, which is what such a sample does have.**
>
> **⇒ growing a biased sample makes the estimate more precise and no more accurate** — it converges confidently on the wrong number. *(This is the same structure as §6's social-desirability bias: a systematic error is not reduced by more observations.)*
>
> **⚠️ And note the dependency: every figure in §3 assumed probability sampling.** **Run the sample-size formula, recruit by convenience, and the 31,000 figure is void along with everything computed from it.**
>
> **The legitimate use of nonprobability samples is *exploratory*.** **Kotler's focus groups are nonprobability and he correctly calls that work qualitative.** **The error is not using them — it is quoting a percentage from one.**

**4. (Hard — big data.)** (a) What does "right data trumps big data" mean? (b) Compute the multiplicity problem. (c) What discipline does it require?

> [!example]- Solution
> **(a) On Kotler's reading, that most collected data is waste.**
>
> **His sources say the job is "throwing away 99.999 percent of that data to find things that are actionable", and that "simply collecting and storing huge amounts of data has little value".** **The stated problem is *volume without insight*.**
>
> **(b) ⚠️ But the real problem is worse — searching is what manufactures the findings.**
>
> *(Computed: $k$ independent tests at $\alpha=0.05$ on hypotheses that are all false:)*
>
> | segments tested | P(≥1 false "discovery") | expected false hits |
> |---|---|---|
> | 10 | 40.1% | 0.5 |
> | **20** | **64.2%** | 1.0 |
> | 100 | 99.4% | 5.0 |
> | **1,000** | **100.0%** | **50.0** |
>
> **Test twenty segments and you are more likely than not to find a "significant" one when nothing whatever is happening.** **Test a thousand and you expect fifty.**
>
> **⚠️ That is not a defect in the data or the tools — it is what $\alpha$ means.** **A 5% false-positive rate per test *is* one false positive per twenty tests, by construction.**
>
> **(c) Fix the hypothesis before looking, or pay for the looking.**
>
> **Two legitimate disciplines:**
> - **Decide the hypothesis in advance** — which is exactly §2's exploratory → causal pipeline, where exploratory work produces a hypothesis and *fresh data* tests it;
> - **or correct for the number of comparisons** *(Bonferroni, false-discovery-rate control)*, which is the [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics]] apparatus.
>
> **⚠️ What is not legitimate is finding the pattern and testing it on the data that suggested it.** **That is guaranteed to confirm.**
>
> **And this reframes Kotler's quote: the discarded 99.999% is not waste, it is the *search space* — and its size is precisely what determines how many spurious patterns the search will return.** *(Neuromarketing, §6, is the extreme case: second-by-second EEG and eye-tracking across a whole advertisement is hundreds of implicit comparisons per subject.)*

**5. (CRM and ethics.)** (a) What is CRM for? (b) Name the DS problems in his examples. (c) What is the ethical asymmetry?

> [!example]- Solution
> **(a) ⚠️ It makes [[01 - Marketing, Customer Value and Engagement|ch. 01]]'s customer lifetime value operational.**
>
> **CRM is "managing detailed information about individual customers and carefully managing customer touch points to maximize customer loyalty."**
>
> **You cannot compute CLV *per customer* without customer-level data.** **And [[01 - Marketing, Customer Value and Engagement|ch. 01]] §4 showed the CLV figure is only as good as its retention estimate — which moved the answer from \$50,000 to \$3,571.** **⇒ CRM data is what turns that estimate from an assumption into a measurement**, which is why the two chapters belong together.
>
> *(It also supplies what [[01 - Marketing, Customer Value and Engagement|ch. 01]] §5's four relationship groups need: classifying a customer as a true friend or a barnacle requires forecast profitability and loyalty at the individual level.)*
>
> **(b) A recommender system and a segmentation problem.**
>
> **His Netflix case — using analytics "to fuel recommendations to subscribers, decide what programming to offer, and even develop its own exclusive content" — is a *recommender system*.** **His Kraft case is *segmentation and targeting*.** **Neither is named.**
>
> *(Per [[00-Index]]'s enrichment plan these are developed where they belong: segmentation as clustering in [[07 - Segmentation, Targeting and Positioning|ch. 07]], recommenders and attribution in [[12 - Integrated Marketing Communications and Digital Marketing|ch. 12]].)*
>
> **(c) Consumers consent to the collection and almost never to the inference.**
>
> **Kotler separates two harms — *intrusion on privacy* (being tracked at all) and *misuse of findings* (what is done with the inference) — and his caption on behavioural targeting, "sophisticated online research or 'just a little creepy'?", is the modern privacy debate in one line.**
>
> **⚠️ The asymmetry is that consent attaches to the first and not the second.** **A cookie notice discloses that purchases are recorded. Nothing in it says "we will deduce your pregnancy, your illness or your job loss from them."**
>
> **⇒ the ethical question sits with the *analytics*, not the data capture** — and that is exactly where a Data Science graduate stands. **The person who builds the model is the person making the decision that no notice covered.**

## 📝 Summary

- **An MIS assesses needs, develops information, delivers insights.** **⚠️ The problem is not too little data: "right data trumps big data."**
- **Three sources: internal databases** *(free, poor fit — collected for other purposes)*, **competitive intelligence**, and **marketing research** — **⚠️ the only one that can be *designed*.**
- **Four steps: define → develop → implement → interpret.** **⚠️ Step 1 is hardest and its failure is invisible downstream.**
- **Three objectives are a PIPELINE: exploratory (hypothesis) → descriptive (prevalence) → causal (truth).** **Observation / survey / experiment respectively.**
- **⚠️ Kotler's causal research IS an A/B test, described completely, with no statistics.**
- **⚠️ Computed: a half-point lift on a 5% baseline needs ~31,000 per group** — nine weeks at 1,000/day. **A focus group of eight detects nothing.**
- **⚠️ $n\propto1/\delta^2$: halving the detectable effect quadruples the sample.**
- **⚠️ An underpowered test gives a RANDOM answer, and an INFLATED one when it "works"** — the most dangerous result available.
- **Six sample types, three probability and three nonprobability.**
- **⚠️ THE BOUNDARY IS HARD, NOT A MENU CHOICE: a nonprobability sample has no sampling distribution, so NO margin of error can be computed from it at all.**
- **⚠️ Size does not repair selection** — a convenience sample of 10,000 supports less inference than a probability sample of 400, and §3's arithmetic is void without probability sampling.
- **Nonprobability samples are legitimately *exploratory*. The error is quoting a percentage from one.**
- **⚠️ Computed: testing 20 segments gives a 64.2% chance of a false "discovery"; 1,000 segments yields 50 expected false hits.** **That is what $\alpha$ means.**
- **⚠️ So the discarded 99.999% is not waste — it is the SEARCH SPACE, and searching it manufactures the false positives.**
- **The discipline: fix the hypothesis before looking, or correct for the number of looks.**
- **Survey bias sources: cannot answer, won't answer, answer to seem helpful.** **⚠️ The third is systematic and does not shrink with $n$.**
- **Open questions for exploratory, closed for descriptive.** **Difficult and personal questions last.**
- **⚠️ Neuromarketing is §5's hazard in its purest form** — hundreds of implicit comparisons per subject.
- **CRM makes [[01 - Marketing, Customer Value and Engagement|ch. 01]]'s CLV operational** — it supplies the retention estimate that moved the answer by a factor of fourteen.
- **His Netflix case is a recommender system and his Kraft case is segmentation** — neither named.
- **⚠️ Consumers consent to the COLLECTION and almost never to the INFERENCE** — so the ethical question sits with the analytics.

## ⚠️ Important Notes

1. **⚠️ More data is not the goal.** Right data beats big data.
2. **Internal data is free and was collected for something else.**
3. **Only commissioned research can be *designed* to answer your question.**
4. **⚠️ A flawless study of the wrong question is worthless, and nothing downstream flags it.**
5. **⚠️ Exploratory → descriptive → causal is a pipeline.** Correlation is where you stop, not where you arrive.
6. **Kotler's causal research is an A/B test.** Recognise it.
7. **⚠️ "Large samples are more reliable" is not a sample size.** Compute it.
8. **⚠️ Halving the detectable effect quadruples the sample.**
9. **⚠️ An underpowered significant result is *inflated*, not merely uncertain.**
10. **Focus groups cannot detect effects.** They generate hypotheses.
11. **⚠️ Probability versus nonprobability is a hard boundary**, not a menu.
12. **No margin of error exists for a nonprobability sample.**
13. **⚠️ Size does not repair selection bias.** It converges confidently on the wrong number.
14. **Never quote a percentage from a convenience sample.**
15. **⚠️ Testing 20 things at $\alpha=0.05$ gives a 64% chance of a false find.**
16. **The search space size determines the false-positive count.**
17. **⚠️ Never test a hypothesis on the data that suggested it.**
18. **Social desirability bias is systematic** — a bigger survey measures the same wrong thing more precisely.
19. **Difficult questions last, or respondents become defensive.**
20. **⚠️ Neuromarketing findings are exploratory** whatever the technology's precision.
21. **CRM is what makes per-customer CLV computable.**
22. **⚠️ Consent covers collection, not inference.** That gap is the analyst's problem.

> [!warning] Gaps in the source material
> **Extraction clean.** **⚠️ TABLE 4.2 (six sample types with definitions) SURVIVED COMPLETE** and is reproduced in §4 — **the second Kotler table to come through intact.**
>
> **All figures are images and lost** — **Figure 4.1 (the marketing information system), Figure 4.2 (the marketing research process)**. **Checked per [[Monetary and Financial Theories/contents/03 - The Behavior of Interest Rates|Monetary Theories ch. 03]]'s rule: both are process lists rendered as diagrams and the prose names every element**, so §1 and §2 reproduce them completely. **The photographic examples carry no analytical content.**
>
> **No erratum and no discrepancy.** **This chapter states almost no numbers** — its content is definitional and procedural — **so there is nothing to recompute against.** **Everything quantitative in this note is an addition, computed from standard statistics rather than checked against Kotler.**
>
> **⚠️ SCOPE NOTE — this is the chapter [[00-Index]] designated DS-critical, so the enrichment is heavier here than elsewhere and is proportionately larger relative to the source.** **That is deliberate and is flagged below.**
>
> **Additions beyond the source.**
>
> - **⚠️ §3's sample-size computation is the note's principal addition and the one [[00-Index]] promised.** **Kotler defines experimental research as an A/B test, correctly and completely, and offers "large samples give more reliable results than small samples" as his only quantitative guidance.** **The formula, the table, the $n\propto1/\delta^2$ scaling and the winner's-curse warning about underpowered tests are all mine**, drawn from [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Mathematical Statistics ch. 07]]'s apparatus.
> - **⚠️ §4's reading of the probability/nonprobability line as a *hard boundary* rather than a menu choice is mine**, and it is the sharpest correction in the chapter. **Kotler's Table 4.2 lists six types in two labelled blocks and says nothing about what the label implies.** **The consequences — that no margin of error exists for a nonprobability sample, that size does not repair selection, and that §3's arithmetic is void without probability sampling — follow immediately and are not in the book.**
> - **⚠️ §5's multiplicity computation is mine.** **Kotler's analytics section celebrates "digging out meaningful patterns in big data" and quotes approvingly that the job is discarding 99.999% of it.** **Computing $1-0.95^k$ shows the discarded portion is the *search space*, so searching it is what generates the spurious findings** — which inverts the quote's meaning. **The identification of neuromarketing as the extreme case is also mine.**
> - **§6's note that social-desirability bias is *systematic* and therefore not reduced by sample size is mine**, and it parallels §4's point about selection.
> - **§7's observation that consent attaches to *collection* and not to *inference* is mine**, as is the identification of Kotler's Netflix and Kraft examples as a recommender system and a segmentation problem.
> - **§2's reading of the three research objectives as a *pipeline* — and the point that this is what licenses exploratory trawling — is mine.**
> - **⚠️ Deliberately compressed:** the extended Real Marketing cases on Domino's and Netflix; the international-research and small-business sections; the detailed contact-method comparison table *(retained as one line in §6)*; and the CRM vendor discussion. **The public-policy section is kept in full because it is the part of the chapter that has aged best.**

**Previous:** [[03 - Analyzing the Marketing Environment]] · **Next:** [[05 - Consumer Markets and Buyer Behavior]]
