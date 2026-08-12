---
subject: Mathematical Statistics
chapter: 01
tags: [ds, statistics, data-types, sampling, probability]
source: "MS_Lec01_Intro.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Introduction to Statistics

> [!note] Course context
> Mathematical Statistics for the **Actuary Bachelor Degree**. Reading for this lecture: **[1] Devore & Berk, Ch. 1, pp. 1–9** and **[2] Miller & Miller, Ch. 1, pp. 1–29**. See [[00-Index]] for the full course map.

## 📘 Main Knowledge

### What is statistics?

The lecture opens by contrasting **opinion** with **statistics**:

| Opinion | Statistics |
|---|---|
| "It seems there are more female students than male at NEU." | "Of 20,000 NEU students, 13,000 are female (65%) and 7,000 male (35%)." |
| "In general, the older the customer, the less they spend on high-tech products." | Age 20–29 → 35; 30–39 → 28; 40+ → 23 (average expense) |

The difference is **quantification**: an opinion asserts a direction, a statistic states a magnitude that can be checked, compared, and acted on.

**What statistics is for:**

- Understand the business environment
- Provide information for decision making
- Predict and forecast
- Applicable across business, economics, and management

### Is statistics "the fact"?

> **Yes, but No!**

A crucial caveat stated early:

- Statistics depends on the **information** fed into it.
- **Statistics may be biased.**
- Without testing for correctness, decisions based on it will be wrong.

So every statistical problem carries two questions: **Is the data accurate?** and **Is the method appropriate?** This is the same "Garbage In, Garbage Out" principle that governs [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]].

### The statistical process

1. **Gathering** data
2. **Processing** data
3. **Presenting** information
4. **Analyzing** data → higher-level informational results
5. **Inferring** information

### Branches of statistics

- **Descriptive Statistics** — organise, summarise, and present data in a convenient and informative way. → [[02 - Tables and Charts]], [[03 - Descriptive Statistics]]
- **Inferential Statistics** — predict, forecast, and verify knowledge by analysing data. → [[04 - Sampling Distributions]] onward

The lecture places these in a hierarchy: **Probability** underpins **Inferential Statistics**; *Data* feeds **Descriptive Statistics**. "Normal Statistics" covers description and basic inference, while **Mathematical Statistics** is the probability-grounded treatment — which is this course.

That dependency is why [[Probability Theory/contents/00-Index|Probability Theory]] is a prerequisite: inference is impossible without a probability model for how samples behave.

### Data sources

**Primary data** — observed or collected by the investigator for a specific purpose (surveys, questionnaires, records). Yields *raw data* which must then be processed.

| Advantages | Disadvantages |
|---|---|
| Relevant to the purpose | Costly |
| Flexible | Non-response, missing information |
| Deep information | Errors from measurement and survey method |

**Secondary data** — collected in the past or by other parties (government, organisations, institutes; published, online, or purchased).

| Advantages | Disadvantages |
|---|---|
| Official, high accuracy | May not be relevant to the purpose |
| Bigger data, less expense | Cannot survey further information |

The trade-off is essentially **relevance versus cost**. Primary data answers exactly your question expensively; secondary data answers a neighbouring question cheaply.

### Population and sample

*(Slide 15 is a diagram with no extractable text; the standard definitions are reconstructed here.)*

- **Population** — the entire set of units of interest. Its numerical summaries are **parameters** (μ, σ, p) — fixed but usually unknown.
- **Sample** — a subset actually observed. Its summaries are **statistics** ($\bar{x}$, $s$, $\hat{p}$) — known, but varying from sample to sample.

**The whole point of inferential statistics is using the sample statistic to make a defensible claim about the unknown population parameter.** The machinery for that begins in [[04 - Sampling Distributions]].

### Structure of a classical dataset

A dataset consists of **Observation – Variable – Value**:

| | No. | Name | Sex | Age | English Mark | Maths Score | … |
|---|---|---|---|---|---|---|---|
| **Observations** | 1 | Anderson | M | 19 | A | 8 | … |
| | 2 | Becky | F | 20 | C | 9 | … |
| | 3 | Charles | M | 20 | B | 7 | |

Rows are **observations** (units); columns are **variables**; each cell is a **value**. This is exactly the "tidy data" layout a Pandas DataFrame encodes — see [[Data Preparation and Visualization/contents/01 - Getting Started with Pandas|Getting Started with Pandas]].

### Types of variable

The central classification of the lecture.

**Qualitative (Categorical):**

- **Nominal** — incomparable values. *Examples:* name, address, career.
- **Ordinal** — comparable values, but not calculable. *Examples:* rank, level, shoe size.
- **Binary (dichotomous)** — a special case with exactly two values. *Examples:* Yes/No, Pass/Fail, gender.

Qualitative variables **can be coded into numbers** — but coding does not make them quantitative.

**Quantitative (Cardinal, Scale):**

- **Discrete vs Continuous** — discrete: number of items, score, age. Continuous: time, length.
- **Interval vs Ratio** — interval permits only **plus and minus**; ratio also permits **multiply and divide**.

> The classification of quantitative variables is **not important in software calculations**.

**The operations each type permits** (slide 19) — this is the practical payoff of the taxonomy:

| Type | Permitted operations |
|---|---|
| **Nominal** | Listing, Grouping |
| **Ordinal** | Listing, Grouping, **Sorting** |
| **Discrete / Continuous (Scale)** | Listing, Grouping, Sorting, **Calculating** (+, −, ×, ÷) |

**The decision tree** (slide 20):

```
More than 2 values? ──No──→ Binary
        │Yes
        ▼
   Comparable? ──No──→ Nominal
        │Yes
        ▼
Can be calculated? ──No──→ Ordinal
        │Yes
        ▼
      Scale
```

### Revision: probability

Slides 24–27 revise probability, random variables, and discrete/continuous distributions — **all four slides are equation images with no extractable text**. The examples, however, survive:

**Example 1.1 — The Problem of Points.** Players A and B each contribute \$50 to a game with no draws; each is equally likely to win any match. They intend to play 9 matches, winner-takes-all. After 7 matches the score is A:B = 4:3. **How should the money be distributed?**

**Example 1.2 — The meeting problem.** A couple arrange to meet at place A between times 0 and 1 (hour). Each waits only 20 minutes. **Find the probability that they meet.**

**Example 1.3 — The "đề" gamble.** Find the expected value and variance of the net benefit from playing 1 million VND in one day. Compare playing 10 million in one day against 1 million a day for 10 days. **Is "don't put all your eggs in one basket" good advice?**

## ✏️ Exercises

**1.** Classify each variable and state which operations are permitted: (a) student ID number; (b) T-shirt size (S/M/L); (c) temperature in °C; (d) annual income in VND; (e) whether a customer churned.

> [!example]- Solution
> **(a) Student ID — Nominal.** Numeric in appearance only: ID 20200150 is not "greater than" 20200149 in any meaningful sense, and their average is meaningless. Listing and grouping only. This is the classic trap — *coded by numbers* does not mean quantitative.
>
> **(b) T-shirt size — Ordinal.** S < M < L is a genuine order, so sorting is valid; but L − M has no defined magnitude, so arithmetic is not.
>
> **(c) Temperature in °C — Interval.** Addition and subtraction are valid (a 5° rise is meaningful), but **multiplication and division are not**: 40 °C is *not* "twice as hot" as 20 °C, because 0 °C is an arbitrary origin, not an absence of temperature. In Kelvin, which has a true zero, it becomes a **ratio** variable.
>
> **(d) Income — Ratio.** It has a true zero (no income), so 40 million really is twice 20 million. All operations valid.
>
> **(e) Churn — Binary**, a special case of nominal. Coded 0/1 it gains a useful property: **its mean is the churn rate**, an idiom used constantly in [[Data Preparation and Visualization/contents/03 - Data Aggregation and Group Operations|Data Aggregation]].

**2.** Distinguish population from sample, and parameter from statistic. Why is inference necessary at all?

> [!example]- Solution
> The **population** is every unit of interest — all 20,000 NEU students. A **sample** is the subset observed, say 200 of them.
>
> A **parameter** describes the population (μ, σ, p). It is **fixed but unknown**. A **statistic** describes the sample ($\bar{x}$, $s$, $\hat{p}$). It is **known but random** — a different sample yields a different value.
>
> The convention is worth memorising: **Greek letters for parameters, Latin for statistics.**
>
> **Why inference is necessary:** a census is usually impossible — too expensive, too slow, or destructive (testing every lightbulb's lifetime destroys the entire stock). So we observe a sample and must reason backwards to the population.
>
> The difficulty is that $\bar{x} \neq \mu$ in general. Inference exists to quantify *how far off* $\bar{x}$ is likely to be, which requires knowing how $\bar{x}$ varies across hypothetical repeated samples. That distribution — the **sampling distribution** — is the subject of [[04 - Sampling Distributions]] and the bridge from probability into statistics.

**3.** The lecture insists "Statistics is the fact? Yes, but No!" Give a concrete example where technically correct statistics support a wrong decision.

> [!example]- Solution
> **Selection bias example.** A company surveys customers about satisfaction via an email to its mailing list and finds 85% satisfied. The arithmetic is flawless. The conclusion — "our customers are satisfied" — is wrong, because dissatisfied customers have already unsubscribed. The population sampled ("current subscribers") is not the population of interest ("all customers"). **The number is accurate; the inference is not.**
>
> The historical case is the *Literary Digest* poll of 1936, which surveyed 2.4 million people — a colossal sample — and predicted Landon would beat Roosevelt. Roosevelt won in a landslide. The sample was drawn from telephone directories and car registrations, which in 1936 meant wealthier voters. **A large biased sample is worse than a small unbiased one, because size lends false confidence.**
>
> Other routes to the same failure: **survivorship bias** (analysing only surviving funds shows excellent average returns because the failures left the dataset); **Simpson's paradox** (a treatment can appear better in every subgroup yet worse overall); and **confounding** (ice cream sales correlate with drownings — both are caused by summer).
>
> This is precisely the lecture's pair of questions: *Accuracy of data?* and *Appropriate method?* Both must be answered before the number means anything.

**4.** *(Example 1.1 — the Problem of Points)* A and B each stake \$50, play to a best-of-9, and stop after 7 matches with the score 4:3. How should the \$100 be divided fairly?

> [!example]- Solution
> **The naive answers are both wrong.** Splitting 4:3 (\$57.14 / \$42.86) ignores how close each player is to *winning*; giving everything to A ignores that B could still win.
>
> The correct principle — Pascal and Fermat's, and the historical origin of probability theory — is that each player should receive the stake **in proportion to their probability of winning if play continued.**
>
> To win the best-of-9, a player needs **5** wins. A has 4 and needs **1** more; B has 3 and needs **2** more. At most 2 further matches are needed. Enumerate them (each equally likely, probability ¼):
>
> | Match 8 | Match 9 | Winner |
> |---|---|---|
> | A | — | **A** (reaches 5 immediately) |
> | B | A | **A** |
> | B | B | **B** |
>
> Writing all four equally likely paths: A wins outright in 2 of 4 (½), plus B-then-A (¼) → $P(A) = \tfrac{3}{4}$, $P(B) = \tfrac{1}{4}$.
>
> **A receives \$75, B receives \$25.**
>
> The insight generalises: fairness is governed by **expected value**, not by the score so far. B is only one match behind but needs to win *twice consecutively*, and $(\tfrac12)^2 = \tfrac14$.

**5.** *(Example 1.3 — diversification)* Compare staking 10 million VND on one day against 1 million a day for 10 days in a fair-odds gamble. Does "don't put all your eggs in one basket" hold?

> [!example]- Solution
> Let $X_i$ be the net return per 1 million staked on day $i$, with mean $\mu$ and variance $\sigma^2$, and assume days are independent.
>
> **Expected value is identical.** By linearity — which holds *regardless of independence*:
> $$\mathbb{E}[10X] = 10\mu \qquad \mathbb{E}\Big[\textstyle\sum_{i=1}^{10} X_i\Big] = 10\mu$$
>
> **Variance is not.**
> $$\operatorname{Var}(10X) = 10^2\sigma^2 = 100\sigma^2 \qquad \operatorname{Var}\Big(\textstyle\sum_{i=1}^{10} X_i\Big) = 10\sigma^2$$
>
> The constant comes out of the variance **squared**, whereas independent variances merely add. Spreading the stake gives the **same expected outcome with one-tenth the variance** — standard deviation smaller by $\sqrt{10} \approx 3.16$.
>
> **So yes, the advice is sound** — with two important qualifications.
>
> First, **independence is essential**. For correlated bets, $\operatorname{Var}(\sum X_i) = \sum\sigma_i^2 + 2\sum_{i<j}\operatorname{Cov}(X_i, X_j)$, and with perfect positive correlation the benefit vanishes entirely. This is why diversifying across ten stocks in one sector achieves far less than it appears to.
>
> Second — and this is the sting for the "đề" example — **diversification reduces variance but cannot change a negative mean.** Lottery-style games have $\mu < 0$ by construction. Spreading the stake makes you lose *more reliably*, converging on the expected loss instead of retaining a small chance of a large win. By the Law of Large Numbers, the ten-day gambler's average outcome tends toward $\mu < 0$ almost surely.
>
> **Diversification is a variance strategy, not a returns strategy.** It is worth doing when $\mu > 0$ and pointless when $\mu < 0$.

## 📝 Summary

- **Statistics quantifies** what opinion merely asserts — but it is only as good as its data and method. *"Yes, but No!"*
- **Two branches:** Descriptive (organise, summarise, present) and Inferential (predict, forecast, verify). Mathematical Statistics is the probability-grounded treatment of both.
- **Primary data** is relevant but costly; **secondary data** is cheap and official but may not fit your question.
- **Population/parameter (unknown, fixed) vs sample/statistic (known, random).** Greek letters for parameters, Latin for statistics.
- **A dataset is Observations × Variables**, each cell a Value.
- **Qualitative:** Nominal (no order) and Ordinal (order, no arithmetic); Binary is the two-valued special case.
- **Quantitative:** Discrete vs Continuous; Interval (± only) vs Ratio (also × ÷, has a true zero).
- **Variable type determines permitted operations** — listing, grouping, sorting, calculating — and therefore which chart and which test are legitimate.
- **Coding a category as a number does not make it quantitative.**

## ⚠️ Important Notes

**Numeric ≠ quantitative.** Student IDs, postcodes, and phone numbers are nominal. The single most common error in applied statistics is computing a mean of something that has no meaningful mean. It is the same mistake as `OrdinalEncoder` on nominal data in [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]].

**Interval vs ratio hinges on whether zero means "none".** 0 °C does not mean "no temperature", so 40 °C is not twice 20 °C. 0 VND does mean "no money", so ratios are valid. Kelvin is ratio; Celsius is interval.

**Variable type dictates which statistical test is valid.** The mode is defined for all types; the median needs at least ordinal; the mean needs at least interval. This determines everything in [[03 - Descriptive Statistics]] and drives the test-selection matrix in [[09 - Non-parametric Testing]].

**A large sample does not fix a biased one.** The *Literary Digest* surveyed 2.4 million people and got the 1936 election wrong. Bias is a property of the sampling *method*; increasing $n$ reduces variance around the wrong answer.

**Age is listed as discrete here, though it is genuinely continuous** — we simply record it in whole years. Many "discrete" variables are continuous quantities measured coarsely; the distinction is about measurement, not the underlying quantity.

**Diversification lowers variance, not the mean.** $\operatorname{Var}(cX) = c^2\operatorname{Var}(X)$ but $\operatorname{Var}(\sum X_i) = \sum\operatorname{Var}(X_i)$ **only under independence**. Correlated risks do not diversify.

**"Statistics may be biased" applies to the analyst too.** Choosing which comparison to report after seeing the data ("p-hacking") produces technically correct statistics that mislead. Decide the analysis before looking.

> [!warning] Gaps in the source slides
> - **Slide 15 — "Population and Sample"** is a diagram; my definitions are reconstructed from standard usage.
> - **Slide 21 — "Dimension"** has a title only; content unknown.
> - **Slides 24–27 — the entire probability revision** (Probability, Random variable, Discrete distribution, Continuous distribution) are **equation images with no extractable text**. The formulas for expectation, variance, and the standard distributions are therefore **not captured**. This is a significant gap: consult [[Probability Theory/contents/00-Index|Probability Theory]] or Devore Ch. 2–4.
> - **Slide 4** ("Purposes of Studying") is a diagram whose fragments suggest a path from theory and class examples toward a statistics job or actuarial certification.
> - **Slides 7–8** contain empty cells where charts or links were embedded.
>
> **Course materials** (slide 3): Microsoft Excel with the Data Analysis Toolpak, IBM SPSS, R, and a calculator. Data and additional material at `www.mfe.edu.vn/buiduonghai` → *Program* → *Class*.
>
> **Exercises set:** [1] Ch. 1 (p. 8) 1, 2 · [4] Ch. 1 (p. 27) 1.1–1.8 · plus reading the VHLSS data (variables, province code) and the SME Main questionnaire (types of variables). **Note textbook [4] — Anderson et al., *Statistics for Business and Economics*, 12th ed. — is NOT in `documents/`**, but is cited throughout the exercise sets.

---
**Next:** [[02 - Tables and Charts]]
