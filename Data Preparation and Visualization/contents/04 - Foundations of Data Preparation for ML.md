---
subject: Data Preparation and Visualization
chapter: 04
tags: [ds, data-preparation, data-leakage, machine-learning, workflow]
source: "Foundation of Data preparation for ML.pdf — Dr. Nguyen Tuan Long, NEU (deck is UNNUMBERED in the source)"
---

# Foundations of Data Preparation for Machine Learning

> [!warning] Chapter number
> This deck is not numbered in the source. I placed it at 04 because it introduces the five task groups developed in [[06 - Data Cleaning]], [[07 - Data Transformation]] and [[08 - Feature Selection]], and the data-leakage rule they depend on. The lecturer's actual Lesson 4 is missing (the decks run 0, 1, 2, 3, 5, 6, 7, 8, 9); ask what it covered. See [[00-Index]].

The map for Part 2 (Becoming a Data Architect).

## 📘 Main Knowledge

### 1. The role of data preparation

The slides: an ML project is "not a straight line, but an iterative cycle." Evaluating models reveals data problems, which sends you back to preparation.

| Step | What happens |
|---|---|
| 1. Define problem | understand the problem, collect data, choose a metric |
| 2. Prepare data | clean, transform, select features; the foundation for the rest |
| 3. Evaluate algorithms | test several models with cross-validation |
| 4. Finalize model | train the final model and deploy it |

Choose the metric in step 1: on an imbalanced problem, accuracy can look excellent while the model is useless.

### 2. Five task groups

| # | Task group | Covered in |
|---|---|---|
| 1 | Data cleaning | [[06 - Data Cleaning]] |
| 2 | Feature selection | [[08 - Feature Selection]] |
| 3 | Data transforms | [[07 - Data Transformation]] |
| 4 | Feature engineering | this chapter; [[05 - String Manipulation and Time Series Data]] |
| 5 | Dimensionality reduction | not in the provided slides |

**Feature engineering** creates new features: split a date into day, month and year; combine population and area into `population_density` (both done in ch. 02 and ch. 05).

Feature engineering **adds** columns that encode domain knowledge; dimensionality reduction **removes** columns, by selecting a subset (feature selection) or projecting onto fewer derived axes (PCA). Slide 11 (dimensionality reduction) is a title only; PCA is an eigendecomposition of the covariance matrix, see [[Linear Algebra/contents/00-Index|Linear Algebra]] and [[Machine Learning/contents/00-Index|Machine Learning]].

### 3. Data leakage

The slides call it the most important concept: "Misunderstanding this can make your model completely useless in practice." **Data leakage** occurs when information from the test set reaches the training process.

| Incorrect | Correct |
|---|---|
| 1. take the entire dataset | 1. split into train and test |
| 2. prepare it (e.g. scaling) | 2. fit transform parameters on the train set only |
| 3. split into train/test | 3. apply the fitted transform to both sets |
| 4. train the model | 4. train the model |
| test-set min/max leaked into preparation | |

**Golden rule: split first, prepare later.** Fit on train, transform both. A scaler fitted on all data encodes the test set's statistics, so the test score is optimistic; on truly new data in production the advantage disappears.

Key takeaways (slides): preparation is iterative and foundational; master the five task groups; always split before preparing; use a pipeline ([[09 - Building Pipelines]]).

## ✏️ Exercises

**1.** Name the five task groups with one operation each.

> [!example]- Solution
> 1. Cleaning: drop duplicates, remove zero-variance columns, impute with the median.
> 2. Feature selection: `SelectKBest(f_classif, k=10)`.
> 3. Transforms: `StandardScaler` on numeric columns, `OneHotEncoder` on nominal ones.
> 4. Feature engineering: split `InvoiceDate` into year, month, day of week; `population / area`.
> 5. Dimensionality reduction: PCA from 60 correlated features to 10 components.
>
> Feature selection is a form of dimensionality reduction that keeps original, interpretable columns; PCA builds new axes from all columns, which is more powerful but loses interpretability.

**2.** Give two ways step 3 (evaluation) sends you back to step 2 (preparation).

> [!example]- Solution
> (a) A large train/test gap (99% vs 70%) suggests overfitting, often from too many features; the fix is more feature selection or dimensionality reduction. A feature that is "too predictive" may be leakage, e.g. `cancellation_date` predicting churn.
>
> (b) Feature importances reveal problems: `customer_id` ranking high means an identifier was fed to the model; one dominant one-hot column may mean leakage; engineered features with zero importance were wasted effort.
>
> Also, the algorithm choice changes preparation: switching to SVM or KNN makes scaling necessary (distance-based), while trees do not need it.

**3.** (Advanced) A colleague says: "I fitted the scaler on all the data, but scaling doesn't use `y`, so nothing leaked." Rebut this.

> [!example]- Solution
> Leakage does not need the target; any information from held-out data used in training counts. `StandardScaler.fit()` computes μ and σ from all rows, including test rows, so training data is expressed using test statistics. In production, new data is scaled with parameters fixed at training time, so the test conditions were more favourable than reality and the score overestimates performance.
>
> The effect is small for `StandardScaler` on large data, but grows when the data are small, the transform is more adaptive (`MinMaxScaler` depends on one extreme value; `QuantileTransformer`, fitted λ in `PowerTransformer`), or the step is supervised (`SelectKBest`, RFE can make pure noise look predictive).
>
> A pipeline makes the correct version easy:
> ```python
> pipe = Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression())])
> cross_val_score(pipe, X, y, cv=5)   # refits the scaler in each fold
> ```

## 📝 Summary

- An ML project is iterative: define → prepare → evaluate → finalize, with evaluation feeding back.
- Five task groups: cleaning, feature selection, transforms, feature engineering, dimensionality reduction.
- Feature engineering adds derived columns; dimensionality reduction removes them.
- Data leakage: test information reaching training makes scores optimistic and the model unreliable.
- Split first, prepare later: fit on train, transform both; use pipelines.

## ⚠️ Important Notes

1. Leakage does not require the target: any statistic learned from held-out data (mean, min/max, category list, λ) leaks.
2. The more adaptive the transform, the worse the leak; supervised selectors are worst.
3. **Target leakage** (not in the slides): a feature not available at prediction time, like `cancellation_date` for churn. Splitting cannot catch it; ask whether you would have the value when predicting.
4. Feature selection keeps interpretability; PCA does not.
5. Choose the metric before preparing data; on imbalanced data accuracy misleads (always predicting "no fraud" can score 99.8%).
6. Iterate using cross-validation on training data; look at the test set once, at the end.

> [!warning] Gaps in the source slides
> - Slides 3–4 (project cycle), 7 (cleaning), 8 (selection), 9 (transforms) and 11 (dimensionality reduction) are titles/diagrams only. PCA, SVD and t-SNE appear nowhere in the extractable slides; if examinable, ask the lecturer.
> - The deck's position as chapter 04 is my choice.

**Previous:** [[03 - Data Aggregation and Group Operations]] · **Next:** [[05 - String Manipulation and Time Series Data]]
