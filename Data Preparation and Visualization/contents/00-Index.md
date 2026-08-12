---
subject: Data Preparation and Visualization
chapter: 00
tags: [ds, moc, index, data-wrangling, pandas, visualization]
source: "Lesson 0 Coures Introduction - From Raw Data to Bussiness Decisions.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Preparation & Visualization — Index

**Lecturer:** Dr. Nguyen Tuan Long (`ntlong@neu.edu.vn`)

> From Raw Data to Business Decisions.

## 🗺️ Map of Content

### Part 1 — Mastering the Tools (Pandas)
*Learn to use Pandas, the Swiss Army knife for data scientists, to "wrangle" data.*

| # | Chapter | One-line description |
|---|---|---|
| 01 | [[01 - Getting Started with Pandas]] | Series, DataFrame, Index; selection with `[]`/`.loc`/`.iloc`/masks; alignment, `apply`/`map`, descriptive stats |
| 02 | [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]] | Reading files and APIs, diagnosing dtypes, handling missing values, `concat` vs `merge` |
| 03 | [[03 - Data Aggregation and Group Operations]] | Split-apply-combine; `agg`/`filter`/`transform`/`apply`; MultiIndex, pivot tables, quick plots |

### Part 2 — Becoming a Data Architect (Data Preparation)
*Apply advanced techniques to optimise the "fuel" for Machine Learning models.*

| # | Chapter | One-line description |
|---|---|---|
| 04 | [[04 - Foundations of Data Preparation for ML]] | The five task groups, the iterative project cycle, and the Golden Rule of data leakage |
| 05 | [[05 - String Manipulation and Time Series Data]] | The `.str` accessor and regex; `DatetimeIndex`, partial string indexing, `.dt` feature engineering |
| 06 | [[06 - Data Cleaning]] | Zero-variance features, duplicates, outliers (σ / IQR / LOF), four imputation strategies |
| 07 | [[07 - Data Transformation]] | Scaling, encoding, power and quantile transforms, discretisation, polynomial features, target transforms |
| 08 | [[08 - Feature Selection]] | Filter (χ², ANOVA F, Pearson), wrapper (RFE), and embedded (coefficients, trees, permutation) methods |
| 09 | [[09 - Building Pipelines]] | `ColumnTransformer`, full workflows, cross-validation, `GridSearchCV`, deployment with `joblib` |

### Part 3 — Turning Analysis into Impact (Visualization & Storytelling)
*An analysis is only valuable if others can understand it and act upon it.*

| # | Chapter | One-line description |
|---|---|---|
| 10 | [[10 - Visualization with Matplotlib and Seaborn]] | Figure/Axes/Axis, the OO interface, subplot layouts; Seaborn distributions, pair plots, facets, heatmaps |
| 11 | [[11 - Chart Design and Data Storytelling]] | Data relationships → chart choice; per-chart design rules; the 10 do's and don'ts |

---

## 🎯 Course framing

### The motivating problem

A retail company is losing customers and wants to know why. You are handed three files:

- `transactions.csv` — purchase history
- `user_logs.xlsx` — web browsing history
- `support_tickets.json` — customer feedback

**The challenge:** combine all three to answer questions like *"Are the customers who complained about 'slow shipping' the same ones who viewed product X but didn't buy it?"*

### The governing principle

> ### "Garbage In, Garbage Out"
>
> Machine learning models are powerful **engines** — but the most powerful engine fails on low-quality **fuel**. **Data quality is the ceiling on the performance of any algorithm.**
>
> A project's success is determined not by the complexity of the algorithm, but by the quality of the data preparation process.

The technical expression of this principle is **data leakage**, introduced in [[04 - Foundations of Data Preparation for ML]] and enforced structurally in [[09 - Building Pipelines]]. It is the single most important idea in the course.

### Tools

- **Environment:** Jupyter Notebook
- **Libraries:** Pandas, Matplotlib & Seaborn, Scikit-learn

### Textbooks

1. **Python Data Science Handbook**, 2nd ed. — Jake VanderPlas → chapters [[01 - Getting Started with Pandas]]–[[03 - Data Aggregation and Group Operations]], [[10 - Visualization with Matplotlib and Seaborn]]
2. **Data Preparation for Machine Learning** — Jason Brownlee → chapters [[06 - Data Cleaning]]–[[08 - Feature Selection]]
3. **Python for Data Analysis**, 3rd ed. — Wes McKinney → Part 1
4. **Storytelling with Data** — Cole Nussbaumer Knaflic → [[11 - Chart Design and Data Storytelling]]

None of these are in `documents/` — they must be sourced separately.

---

## 🔗 Cross-subject connections

| Topic | Links to |
|---|---|
| Correlation, covariance, descriptive statistics | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| χ² and ANOVA F-tests, hypothesis testing | [[Mathematical Statistics/contents/00-Index\|Mathematical Statistics]] |
| Models, cross-validation, Random Forest, PCA | [[Machine Learning/contents/00-Index\|Machine Learning]] |
| Pandas/Python fundamentals | [[Programming for Data Science (Python)/contents/00-Index\|Programming for Data Science]] |
| `DatetimeIndex`, resampling, forecasting | [[Time-series Analysis/contents/00-Index\|Time-series Analysis]] |
| Dummy variable trap, multicollinearity | [[Econometrics/contents/00-Index\|Econometrics]] |
| PCA as eigendecomposition | [[Linear Algebra/contents/00-Index\|Linear Algebra]] |
| Deploying and monitoring the saved pipeline | [[MLOps/contents/00-Index\|MLOps]] |

---

## ⚠️ Gaps in the source material

> [!warning] Known gaps — verify these with the lecturer
> **1. Lesson 4 is missing entirely.** The numbered decks run **0, 1, 2, 3, 5, 6, 7, 8, 9**. Nothing in `documents/slides/` is labelled Lesson 4, and no deck's content obviously fills the jump from *Data Aggregation* (3) to *String Manipulation and Time Series* (5). **Ask what Lesson 4 covered.**
>
> **2. Chapter 04 is my placement, not the lecturer's.** `Foundation of Data preparation for ML.pdf` is **unnumbered**. I placed it at 04 because it thematically bridges Parts 1 and 2 — it is *not* a recovered Lesson 4.
>
> **3. Dimensionality reduction has no content.** It is named as one of the five task groups, but its slide is an image. **PCA, SVD, and t-SNE appear nowhere in the extractable material.**
>
> **4. The Seaborn half of the visualization deck is almost entirely images.** Joint plots, factor/bar plots, heatmaps, and the Iris and correlation practices have no recoverable text. Reconstructed code in [[10 - Visualization with Matplotlib and Seaborn]] is marked as such.
>
> **5. Lesson 7 poses eight "Question:" prompts it never answers** — clearly in-class discussion points, and strongly exam-flavoured. I have answered them in that chapter's exercises; treat those as reconstructions and check against your lecture notes.
>
> **6. Missing datasets.** `OnlineRetail.xlsx` / `.csv` is referenced by Lessons 2 and 5 through hyperlinks whose URLs did not survive extraction, and is not in `documents/`. `pokemon_df` (Lesson on Seaborn) is likewise absent. Everything else resolves — Brownlee's GitHub datasets, the UCI URLs, and `sns.load_dataset()` built-ins.
>
> **7. Several Lab tasks are title-only images** — Lesson 7 Labs #4–#6 (Sonar), Lesson 8 Labs 3–4, and the Matplotlib "California Cities" practice.

---

## 📌 The one-page revision path

If you have limited time before an exam, these are the load-bearing ideas:

1. **`.loc` is inclusive, `.iloc` is exclusive** — [[01 - Getting Started with Pandas]]
2. **`concat` stacks, `merge` joins on keys; many-to-many multiplies rows** — [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]]
3. **`agg` / `filter` / `transform` / `apply` differ by output shape** — [[03 - Data Aggregation and Group Operations]]
4. **SPLIT FIRST, PREPARE LATER** — [[04 - Foundations of Data Preparation for ML]]
5. **`.str.contains(na=False)`; `.dt` on columns, bare attributes on the index** — [[05 - String Manipulation and Time Series Data]]
6. **IQR beats σ for outliers because outliers inflate σ** — [[06 - Data Cleaning]]
7. **Scaling changes units; power transforms change shape** — [[07 - Data Transformation]]
8. **Filters are blind to feature interactions** — [[08 - Feature Selection]]
9. **Pass the whole pipeline to `cross_val_score`** — [[09 - Building Pipelines]]
10. **Bars need a zero baseline; lines don't** — [[11 - Chart Design and Data Storytelling]]
