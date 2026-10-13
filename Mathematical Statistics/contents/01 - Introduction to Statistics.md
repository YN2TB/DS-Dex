---
subject: Mathematical Statistics
chapter: 01
tags: [ds, statistics, data-types, sampling, probability]
source: "MS_Lec01_Intro.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Introduction to Statistics

Mathematical Statistics for the Actuary Bachelor Degree. Reading: Devore & Berk ch. 1 (pp. 1–9); Miller & Miller ch. 1 (pp. 1–29). Course map in [[00-Index]].

## 📘 Main Knowledge

### What statistics is

| Opinion | Statistics |
|---|---|
| "It seems there are more female than male students at NEU." | "Of 20,000 NEU students, 13,000 are female (65%) and 7,000 male (35%)." |
| "Older customers spend less on high-tech products." | Average spending: age 20–29 → 35; 30–39 → 28; 40+ → 23 |

Statistics quantifies: it states a magnitude that can be checked and compared. Uses: understanding the business environment, informing decisions, prediction and forecasting, in business, economics and management.

**"Is statistics the fact? Yes, but no."** Results depend on the input data, statistics can be biased, and untested results lead to wrong decisions. Always ask whether the data are accurate and the method appropriate (compare "garbage in, garbage out" in [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]]).

**Process**: gather → process → present → analyse → infer.

**Branches**
- **Descriptive statistics**: organize, summarize and present data ([[02 - Tables and Charts]], [[03 - Descriptive Statistics]]).
- **Inferential statistics**: predict, forecast and test claims from data ([[04 - Sampling Distributions]] onward).

Probability underlies inference, which is why [[Probability Theory/contents/00-Index|Probability Theory]] is a prerequisite; mathematical statistics is the probability-based treatment.

### Data sources

**Primary data**: collected by the investigator for the purpose (surveys, questionnaires, records).

| Advantages | Disadvantages |
|---|---|
| relevant | costly |
| flexible | non-response, missing information |
| detailed | measurement and survey errors |

**Secondary data**: collected earlier or by others (government, organizations; published, online, purchased).

| Advantages | Disadvantages |
|---|---|
| official, accurate | may not fit the purpose |
| large, cheap | cannot ask further questions |

### Population and sample

(Slide 15 is a diagram; standard definitions.)
- **Population**: all units of interest; its summaries are **parameters** (μ, σ, p), fixed but usually unknown.
- **Sample**: the observed subset; its summaries are **statistics** ($\bar x$, $s$, $\hat p$), known but varying from sample to sample.

Inference uses sample statistics to make claims about population parameters.

### Dataset structure

Observations (rows) × variables (columns) → values (cells):

| No. | Name | Sex | Age | English mark | Maths score |
|---|---|---|---|---|---|
| 1 | Anderson | M | 19 | A | 8 |
| 2 | Becky | F | 20 | C | 9 |
| 3 | Charles | M | 20 | B | 7 |

This is the layout of a Pandas DataFrame ([[Data Preparation and Visualization/contents/01 - Getting Started with Pandas|Getting Started with Pandas]]).

### Types of variables

**Qualitative (categorical)**
- **Nominal**: values cannot be compared (name, address, career).
- **Ordinal**: values can be ordered but not calculated (rank, level, shoe size).
- **Binary**: exactly two values (yes/no, pass/fail).

Qualitative variables can be coded as numbers, but that does not make them quantitative.

**Quantitative (cardinal, scale)**
- Discrete (number of items, score, age) vs continuous (time, length).
- Interval (only + and −) vs ratio (also × and ÷).

The slides note that the quantitative sub-types do not matter for software calculations.

| Type | Permitted operations |
|---|---|
| nominal | listing, grouping |
| ordinal | listing, grouping, sorting |
| scale | listing, grouping, sorting, calculating |

Decision tree (slide 20):
```
More than 2 values? ──No──→ Binary
        │Yes
   Comparable? ──No──→ Nominal
        │Yes
Can be calculated? ──No──→ Ordinal
        │Yes
      Scale
```

### Probability revision

Slides 24–27 (probability, random variables, distributions) are equation images. The examples survive:

- **Example 1.1 (problem of points)**: A and B each stake \$50 on a best-of-9 series with no draws, equal chances each match. They stop at 4:3 after 7 matches. How should the money be divided?
- **Example 1.2 (meeting problem)**: two people arrive independently and uniformly between times 0 and 1 hour; each waits 20 minutes. Probability they meet?
- **Example 1.3 ("đề" gamble)**: expected value and variance of the net benefit from staking 1 million VND in a day; compare 10 million in one day with 1 million a day for 10 days.

## ✏️ Exercises

**1.** Classify and give the permitted operations: (a) student ID; (b) T-shirt size (S/M/L); (c) temperature in °C; (d) annual income in VND; (e) whether a customer churned.

> [!example]- Solution
> (a) Nominal: numeric codes, but averages or comparisons mean nothing; listing and grouping only.
> (b) Ordinal: S < M < L can be sorted, but L − M has no size.
> (c) Interval: differences are meaningful, ratios are not (0 °C is not "no temperature", so 40 °C is not twice as hot as 20 °C). Kelvin is a ratio scale.
> (d) Ratio: true zero; 40 million is twice 20 million.
> (e) Binary; coded 0/1, its mean is the churn rate.

**2.** Population vs sample, parameter vs statistic. Why do we need inference?

> [!example]- Solution
> Population: all 20,000 students; sample: the 200 observed. Parameters (Greek letters) are fixed and unknown; statistics (Latin letters) are known but random. A census is often impossible (too expensive, slow, or destructive, e.g. testing light bulbs to failure). Since $\bar x\neq\mu$ in general, inference quantifies how far off $\bar x$ is likely to be, using its sampling distribution ([[04 - Sampling Distributions]]).

**3.** Give an example where correct arithmetic supports a wrong decision.

> [!example]- Solution
> An email survey of a mailing list finds 85% satisfied, but dissatisfied customers have already unsubscribed: the sampled population differs from the target population. The *Literary Digest* 1936 poll asked 2.4 million people (from phone books and car registrations, i.e. wealthier voters) and predicted Landon would beat Roosevelt; Roosevelt won easily. A large biased sample is worse than a small unbiased one. Other cases: survivorship bias, Simpson's paradox, confounding.

**4.** (Example 1.1) Divide the \$100 fairly.

> [!example]- Solution
> Divide in proportion to each player's probability of winning if play continued (Pascal and Fermat). A needs 1 more win, B needs 2.
>
> | Match 8 | Match 9 | Winner |
> |---|---|---|
> | A | — | A |
> | B | A | A |
> | B | B | B |
>
> $P(B)=(1/2)^2=1/4$, $P(A)=3/4$: A gets \$75, B \$25. Splitting 4:3 (\$57.14/\$42.86) ignores how close each is to winning.

**5.** (Example 1.3) Compare 10 million on one day with 1 million a day for 10 days in an independent gamble with per-unit mean μ and variance σ².

> [!example]- Solution
> Means are equal: $E[10X]=10\mu=E[\sum_{i=1}^{10}X_i]$ (linearity, no independence needed).
> Variances differ: $\operatorname{Var}(10X)=100\sigma^2$, $\operatorname{Var}(\sum X_i)=10\sigma^2$ (independence), so the standard deviation falls by $\sqrt{10}\approx3.16$.
>
> Spreading reduces risk only if the bets are independent; with covariances, $\operatorname{Var}(\sum X_i)=\sum\sigma_i^2+2\sum_{i<j}\operatorname{Cov}(X_i,X_j)$. And it cannot change a negative mean: lottery-type games have $\mu<0$, so spreading makes the loss more certain (law of large numbers). Diversification is a variance strategy, not a return strategy.

## 📝 Summary

- Statistics quantifies, but depends on data quality and method ("yes, but no").
- Descriptive vs inferential; mathematical statistics is grounded in probability.
- Primary data: relevant, costly. Secondary data: cheap, official, may not fit.
- Population/parameter (fixed, unknown) vs sample/statistic (known, random).
- Dataset = observations × variables.
- Nominal, ordinal, binary (qualitative); discrete/continuous and interval/ratio (quantitative).
- The variable type decides the permitted operations, and so which summaries and tests are valid.

## ⚠️ Important Notes

1. Numeric codes (IDs, postcodes) are nominal; don't average them.
2. Interval vs ratio depends on whether zero means "none".
3. Mode works for all types, median needs ordinal, mean needs interval or ratio ([[03 - Descriptive Statistics]], [[09 - Non-parametric Testing]]).
4. A larger sample does not fix sampling bias.
5. Age is recorded as discrete but is continuous underneath; the distinction is about measurement.
6. $\operatorname{Var}(cX)=c^2\operatorname{Var}(X)$; variances add only for independent (uncorrelated) variables.
7. Choosing the analysis after seeing the data (p-hacking) misleads even with correct arithmetic.

> [!warning] Gaps in the source slides
> - Slide 15 (population and sample) is a diagram; slide 21 ("Dimension") has a title only.
> - Slides 24–27 (probability revision) are equation images: see [[Probability Theory/contents/00-Index|Probability Theory]] or Devore ch. 2–4.
> - Slide 4 (purposes) is a diagram; slides 7–8 contain empty embedded objects.
> - Tools (slide 3): Excel with the Data Analysis Toolpak, SPSS, R, a calculator; data at `www.mfe.edu.vn/buiduonghai`.
> - Exercise set: [1] ch. 1 (p. 8) 1, 2; [4] ch. 1 (p. 27) 1.1–1.8; the VHLSS data and SME questionnaire. Textbook [4] (Anderson et al., *Statistics for Business and Economics*, 12th ed.) is not in `documents/`.
> - Example 1.2 is stated but not solved in the slides (answer: $1-(2/3)^2=5/9$).

**Next:** [[02 - Tables and Charts]]
