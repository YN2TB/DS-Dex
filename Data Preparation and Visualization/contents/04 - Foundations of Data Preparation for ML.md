---
subject: Data Preparation and Visualization
chapter: 04
tags: [ds, data-preparation, data-leakage, machine-learning, workflow]
source: "Foundation of Data preparation for ML.pdf — Dr. Nguyen Tuan Long, NEU (deck is UNNUMBERED in the source)"
---

# Foundations of Data Preparation for Machine Learning

> [!warning] A note on this chapter's number
> This deck is **unnumbered in the source material** — it is not labelled "Lesson 4". I have placed it at position 04 because it is the natural bridge from Part 1 to Part 2: it introduces the five task groups that [[06 - Data Cleaning]], [[07 - Data Transformation]], and [[08 - Feature Selection]] then develop in detail, and it states the data leakage principle those chapters depend on.
>
> **The lecturer's actual Lesson 4 is missing from the provided material.** The numbered sequence runs 0, 1, 2, 3, **5**, 6, 7, 8, 9. Do not assume this deck fills that gap — ask what Lesson 4 covered. See [[00-Index]].

> [!note] Where this sits in the course
> The map for **Part 2 — Becoming a Data Architect**. Short, conceptual, and worth reading before the three chapters that implement it.

## 📘 Main Knowledge

### 1. The role of data preparation

> A Machine Learning project is **not a straight line, but an iterative cycle.**

That framing matters: you do not clean data once and move on. Evaluating algorithms reveals problems in the data, which sends you back to preparation, which changes what the algorithms can do.

**The four steps of a project:**

| Step | What happens |
|---|---|
| **1. Define Problem** | Understand the problem, collect data, choose a metric |
| **2. Prepare Data** | Clean, transform, and select features — **the foundation for the next steps** |
| **3. Evaluate Algorithms** | Test multiple models, use cross-validation |
| **4. Finalize Model** | Train the final model and deploy it |

Choosing the **metric** in step 1, before touching data, is easy to skip and consequential — accuracy on an imbalanced problem can look excellent while the model is useless.

### 2. The data preparation process — five task groups

| # | Task group | Covered in |
|---|---|---|
| 1 | **Data Cleaning** | [[06 - Data Cleaning]] |
| 2 | **Feature Selection** | [[08 - Feature Selection]] |
| 3 | **Data Transforms** | [[07 - Data Transformation]] |
| 4 | **Feature Engineering** | This chapter; also [[05 - String Manipulation and Time Series Data]] |
| 5 | **Dimensionality Reduction** | *Not covered in the provided slides* |

**Feature engineering** — creating new features from existing data:

- Split a date-month-year column into separate day, month, and year features.
- Combine population and area to create `population_density`.

Both examples have already appeared: `.dt.year` / `.dt.dayofweek` extraction and the US-states population-density exercise are both in [[05 - String Manipulation and Time Series Data]] and [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]].

> [!warning] Feature engineering vs. dimensionality reduction
> These are opposites, and both belong in a good workflow. Feature engineering **adds** columns encoding domain knowledge the raw data only implies. Dimensionality reduction **removes** columns, either by selecting a subset (feature selection) or by projecting onto fewer derived axes (PCA). You expand to capture signal, then contract to control noise and cost.
>
> **Dimensionality reduction has no content in the provided slides** — slide 11 is a title only. PCA is the standard technique; see [[Machine Learning/contents/00-Index|Machine Learning]] and [[Linear Algebra/contents/00-Index|Linear Algebra]] (it is an eigendecomposition of the covariance matrix).

### 3. Data leakage — "the MOST IMPORTANT concept"

The slides' own emphasis:

> **Misunderstanding this can make your model completely useless in practice.**
>
> **Data Leakage:** occurs when information from the test set is accidentally "leaked" into the model training process.

**The comparison, side by side:**

| ❌ Incorrect | ✅ Correct |
|---|---|
| 1. Take the **entire** dataset | 1. **Split** raw data into train and test |
| 2. Prepare the data (e.g. scaling) | 2. **Fit** — learn transform parameters **only on the train set** |
| 3. Split into train/test | 3. **Transform** — apply to *both* train and test |
| 4. Train the model | 4. Train the model |
| **Problem:** information (min, max) from the test set has leaked into the preparation step | |

### **The Golden Rule: SPLIT FIRST, PREPARE LATER.**

The three-word version of the fit/transform discipline: **fit on train, transform on both.** Every scikit-learn transformer is built around this split precisely because the distinction is the difference between an honest model and a useless one.

Why it destroys a model: a scaler fitted on all the data encodes the test set's min and max. The reported test score is then optimistic — the model has already seen, in a diffuse way, the data it is being judged on. In production, where genuinely unseen data arrives, that advantage evaporates and performance collapses.

**The key takeaways slide:**

1. Data preparation is an **iterative process** and the foundation of a project.
2. Master the five task groups: Cleaning, Selection, Transforms, Engineering, Reduction.
3. **Always split data before preparation** to avoid data leakage.
4. **Using a Pipeline is a best practice** → [[09 - Building Pipelines]].

## ✏️ Exercises

**1.** Name the five task groups and give one concrete operation from each.

> [!example]- Solution
> 1. **Data Cleaning** — drop duplicate rows; remove zero-variance columns; impute missing values with the median.
> 2. **Feature Selection** — `SelectKBest(f_classif, k=10)` to keep the 10 features most associated with the target.
> 3. **Data Transforms** — `StandardScaler` on numeric columns; `OneHotEncoder` on nominal ones.
> 4. **Feature Engineering** — split `InvoiceDate` into `year`, `month`, `dayofweek`; compute `population / area` as `population_density`.
> 5. **Dimensionality Reduction** — PCA to project 60 correlated features onto 10 principal components.
>
> Note the overlap between 2 and 5: feature selection *is* a form of dimensionality reduction — it reduces by **choosing a subset of the original columns**, which keeps every remaining feature interpretable. PCA reduces by **constructing new axes** that are linear combinations of all originals, which is more powerful but destroys interpretability: "principal component 3" has no business meaning.

**2.** The slides call a machine learning project "an iterative cycle, not a straight line." Give two concrete ways step 3 (Evaluate Algorithms) sends you back to step 2 (Prepare Data).

> [!example]- Solution
> **(a) A large train/test performance gap points back to preparation.** 99% training accuracy against 70% test accuracy signals overfitting, and one of the usual causes is too many features relative to samples. The fix lives in step 2 — more aggressive feature selection, or dimensionality reduction. Sometimes the diagnosis is worse and more interesting: a feature that is *too* predictive often turns out to be leakage of a different kind, such as a column that is only populated *after* the outcome is known (`cancellation_date` predicting churn).
>
> **(b) Feature importances reveal preparation problems.** If `customer_id` ranks among the top features, you have accidentally fed the model a row identifier. If a one-hot column dominates, you may have a category that perfectly separates the classes — again, likely leakage. If a whole family of engineered features ranks at zero, the engineering was wasted effort and the time is better spent elsewhere.
>
> A third route worth knowing: **the choice of algorithm changes what preparation is needed.** Deciding in step 3 to try SVM or KNN rather than a random forest suddenly makes scaling mandatory, because those models are distance-based while trees are scale-invariant. The steps are coupled in both directions.

**3.** (Advanced) A colleague argues: *"I fitted the scaler on all the data, but scaling doesn't use the target variable `y` at all — so no information about the answer leaked. My test score is valid."* Rebut this precisely.

> [!example]- Solution
> The premise is true and the conclusion is false. Leakage does not require the *target* — it requires **any** information from the held-out data influencing training.
>
> `StandardScaler.fit()` computes $\mu$ and $\sigma$ from every row it sees, including the test rows. Every training value is then expressed relative to statistics that partly describe the test set. The model is trained in a coordinate system defined using data it was supposed to be blind to.
>
> **Why this makes the test score invalid:** the test score is meant to estimate performance on *genuinely unseen* data. In production, a new record arrives and must be scaled using **only** parameters fixed at training time. If those parameters were computed with test data included, the test-time conditions were more favourable than production will ever be, and the score is an overestimate. The number answers a question nobody asked.
>
> **How large is the effect?** Usually small for `StandardScaler` on large, homogeneous datasets — which is exactly what makes this argument seductive. But it grows severe when:
> - The dataset is **small** (each test row moves $\mu$ and $\sigma$ noticeably).
> - The transform is **more adaptive** — `MinMaxScaler` depends on the single most extreme value, so one test outlier changes the scaling of every training row. `QuantileTransformer` and `PowerTransformer`'s fitted $\lambda$ are worse still.
> - The step is **supervised** — `SelectKBest` and RFE *do* use `y`, and fitting them on everything can produce impressive cross-validated accuracy on **pure random noise**.
>
> **The decisive practical point:** correctness should not depend on estimating how much a shortcut costs you. `Pipeline` makes the correct version *easier to write* than the incorrect one, so there is no reason to take the risk:
> ```python
> pipe = Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression())])
> cross_val_score(pipe, X, y, cv=5)   # re-fits the scaler per fold, automatically
> ```
> See [[09 - Building Pipelines]].

## 📝 Summary

- **A machine learning project is an iterative cycle**, not a pipeline of one-way steps: Define Problem → Prepare Data → Evaluate Algorithms → Finalize Model, with evaluation feeding back into preparation.
- **Data preparation is the foundation** on which every later step rests.
- **Five task groups:** Data Cleaning, Feature Selection, Data Transforms, Feature Engineering, Dimensionality Reduction.
- **Feature engineering adds derived columns** (date parts, ratios like population density); **dimensionality reduction removes them.** Both belong in a mature workflow.
- **Data leakage is the most important concept in the course** — test-set information reaching the training process makes a model useless in practice while its scores look excellent.
- **The Golden Rule: SPLIT FIRST, PREPARE LATER.** Split → fit on train only → transform both → train.
- **Use a Pipeline.** It makes the correct order structural rather than a matter of discipline.

## ⚠️ Important Notes

**Leakage does not require the target variable.** Any statistic learned from held-out data — a mean, a min/max, a category list, a fitted $\lambda$ — is leakage. "It's unsupervised, so it's safe" is wrong.

**Leakage severity scales with how adaptive the transform is.** `StandardScaler` on large data leaks mildly; `MinMaxScaler` depends on a single extreme value; supervised selectors like `SelectKBest` and RFE leak badly enough to make random noise look predictive.

**There is a second kind of leakage the slides do not mention: *target leakage* in the data itself** — a feature that would not be available at prediction time in production. `cancellation_date` predicts churn perfectly and is worthless, because you only have it after the customer has already left. No split discipline protects against this; only understanding what each column means and *when* it becomes known. Ask of every feature: *would I actually have this at the moment I need to predict?*

**Feature selection reduces dimensionality while preserving interpretability;** PCA reduces further but produces components with no business meaning. Choose according to whether you must explain the model.

**The metric is chosen in step 1, before data preparation.** On imbalanced problems, accuracy is misleading — a model predicting "no fraud" always can score 99.8%.

**Iteration is expected, but re-checking the test set is not.** Cycling between preparation and evaluation is correct practice — provided you evaluate on cross-validation folds of the *training* data. Every time you look at the test score and change something, you leak a little information through your own decisions. Touch the test set once, at the end.

> [!warning] Gaps in the source slides
> This deck is heavily diagram-based; the following have **titles only, no extractable content**:
> - **Slides 3–4** — the iterative ML project cycle diagrams
> - **Slide 7** — Data Cleaning overview
> - **Slide 8** — Feature Selection overview
> - **Slide 9** — Data Transforms overview
> - **Slide 11** — **Dimensionality Reduction** — the *only* treatment of this task group anywhere in the provided material, and it is an image. **PCA, SVD, and t-SNE appear nowhere in the extractable slides.** If dimensionality reduction is examinable, this is a real gap: ask the lecturer.
>
> Slides 7–9 being images is less costly, since [[06 - Data Cleaning]], [[07 - Data Transformation]], and [[08 - Feature Selection]] cover those areas in full.
>
> The deck is unnumbered and its position here is my editorial choice — see the warning at the top.

---
**Previous:** [[03 - Data Aggregation and Group Operations]] · **Next:** [[05 - String Manipulation and Time Series Data]]
