---
subject: Data Preparation and Visualization
chapter: 08
tags: [ds, feature-selection, scikit-learn, statistics, dimensionality-reduction]
source: "Lesson_8_Feature Selection.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Feature Selection

> [!note] Where this sits in the course
> Closes **Part 2 — Becoming a Data Architect**. [[07 - Data Transformation]] created features; this chapter decides which ones **deserve to stay**. Note the tension: `PolynomialFeatures` can turn 60 columns into 1,891, and this is the chapter that prunes them back.

## 📘 Main Knowledge

### What and why

**Feature selection** = reducing the number of input variables used to build a predictive model.

Three motivations:

- **Reduce overfitting, improve generalisation** — simpler models memorise less noise.
- **Cut computation time and cost** — fewer features train and predict faster.
- **Improve interpretability** — a model with 10 understood features is vastly more explainable than one with 500. This matters for trust and for justifying decisions to stakeholders or regulators.

### The taxonomy

The first split is **whether the target variable is used**:

- **Unsupervised** — ignores the target. General cleaning: drop low-variance or highly correlated features. (`VarianceThreshold` from [[06 - Data Cleaning]] lives here.)
- **Supervised** — uses the target to eliminate irrelevant variables. Three families:

| Family | How it works | Speed | Sees interactions? |
|---|---|---|---|
| **Filter** | Statistical tests score each feature against the target, *before* modelling | Fast | **No** |
| **Wrapper** | Searches feature subsets by measuring a model's actual performance | Slow | Yes |
| **Embedded** | Selection happens *inside* model training (LASSO, Random Forest) | Moderate | Yes |

The filter family's blindness to interactions is its defining weakness: two features that are useless alone but powerful together will both be discarded.

---

## Part I — Filter methods

Score each input against the target with a statistical test. **The right test depends on the data types of the input and the output.**

### Categorical input → Categorical output: Chi-Squared (χ²)

A hypothesis test for association between two categorical variables.

- **H₀:** the two variables are **independent** — the feature is unrelated to the target.
- **H₁:** the two variables are **dependent** — the feature is related.

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

where $O$ is the observed frequency and $E$ the expected frequency under independence. **A higher χ² is stronger evidence against H₀**, so a higher score means a more useful feature.

*Advantages:* simple, fast, interpretable. *Disadvantage:* requires expected frequencies not be too small (the usual rule is $E \ge 5$ per cell). Theory in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

### Numerical input → Categorical output: ANOVA F-test

Tests whether a numerical variable's **mean differs significantly across the target's classes**. If a feature's average value varies a lot between classes, it separates them well.

$$F = \frac{\text{variance between groups}}{\text{variance within groups}}$$

**Larger F → more distinct groups → more important feature.**

*Pros:* very effective at finding linear relationships (differences in means). *Cons:* assumes normality and equal variance across groups — though it is fairly robust in practice.

### Numerical input → Numerical output: Pearson correlation

$$r_{xy} = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2}\sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2}}$$

Ranges $[-1, +1]$. *Pros:* fast, interpretable, gives magnitude **and** direction. *Cons:* **captures only linear relationships.**

Alternatives for this case:
- **Spearman's rank coefficient** — monotonic relationships, including non-linear ones.
- **Mutual information** — general statistical dependency of any form.

### The decision matrix

| Input type | Output type | Recommended test | sklearn function |
|---|---|---|---|
| Categorical | Categorical | Chi-Squared, Mutual Information | `chi2`, `mutual_info_classif` |
| Numerical | Categorical | ANOVA F-test, Mutual Information | `f_classif`, `mutual_info_classif` |
| Numerical | Numerical | Pearson correlation | `f_regression` |

**Memorise this table.** Picking the wrong test is the most common mistake in the chapter.

### `SelectKBest`

```python
from sklearn.feature_selection import SelectKBest, chi2

selector = SelectKBest(score_func=chi2, k=4)
X_selected = selector.fit_transform(X, y)
```

- **`score_func`** — `chi2`, `f_classif`, `f_regression`, `mutual_info_classif`, `mutual_info_regression`
- **`k`** — number of top features to keep (default 10). `k='all'` bypasses selection, which is useful when tuning `k` in a parameter search.

**Lab 1 result** (Breast Cancer, `SelectKBest(chi2, k=4)`): selected feature indices `[3, 4, 5, 8]`, accuracy **0.747**.

---

## Part II — Wrapper methods

Search for the best feature *subset* by evaluating a specific model's performance on each candidate. The method "wraps" around the algorithm.

### Why heuristics are necessary

For $N$ features there are $2^N - 1$ non-empty subsets. At $N = 60$ (the Sonar dataset) that is ~$10^{18}$ — testing them all is impossible. So wrappers use **stepwise search**:

- **Forward selection** — start empty; repeatedly add the feature that improves performance most.
- **Backward elimination** — start with everything; repeatedly remove the least important feature. **RFE is the prime example.**

### Recursive Feature Elimination (RFE)

1. Train a model on **all** features. The model must expose feature importance (`coef_` or `feature_importances_`).
2. Find and **eliminate the least important** feature.
3. Repeat with the remaining features until $k$ remain.

```python
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier

rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=5, step=1)
```

| Parameter | Meaning |
|---|---|
| `estimator` | Any supervised model exposing `coef_` or `feature_importances_` |
| `n_features_to_select` | Integer = absolute count; float in (0,1) = fraction; `None` = half |
| `step` | ≥1 = features removed per iteration; float = percentage removed per iteration |

*Pros:* often outperforms filter methods, because it **accounts for feature interactions** — importance is recomputed after each removal, so it sees how features behave together.
*Cons:* computationally expensive; **risk of overfitting** unless paired with cross-validation.

---

## Part III — Embedded methods

Selection happens as part of training. Efficient and powerful.

### 1. Coefficients as importance

Linear models assign a coefficient per feature; $|\text{coefficient}|$ serves as an importance score.

```python
model_lr = LogisticRegression(solver='lbfgs')
model_lr.fit(X_clf, y_clf)
importance_lr = model_lr.coef_[0]
```

> [!warning] Data **must be scaled** for coefficients to be comparable.
> An unscaled coefficient reflects the feature's *units*, not its importance. A feature in millimetres gets a coefficient 1,000× smaller than the same feature in metres. Without [[07 - Data Transformation]]'s `StandardScaler` first, this ranking is meaningless.

### 2. Tree-based importance

`DecisionTree` and `RandomForest` compute importance from how much each feature improves node **purity** (e.g. reduction in Gini impurity) when chosen for a split.

```python
model_rf = RandomForestClassifier(random_state=1)
model_rf.fit(X_clf, y_clf)
importance_rf = model_rf.feature_importances_
```

*Powerful* — captures non-linear interactions. *But* **biased toward high-cardinality categorical features and continuous numerical features**, simply because they offer more possible split points, not because they carry more signal.

### 3. Permutation importance

**Model-agnostic.** Randomly shuffle one feature's values and measure how much performance drops. The feature whose shuffling hurts most is the most important. **One of the most reliable methods.**

```python
from sklearn.inspection import permutation_importance

results_perm = permutation_importance(model_rf, X_clf, y_clf,
                                      scoring='accuracy', n_repeats=10,
                                      random_state=1, n_jobs=-1)
importance_perm = results_perm.importances_mean
```

Shuffling breaks the feature's relationship with the target while preserving its distribution — so any performance loss is attributable to that feature alone. It works on **any** fitted model and avoids the cardinality bias of tree importances.

### General advice (the lecturer's recommended workflow)

1. **Start with filter methods** for a quick overview and to eliminate obviously irrelevant features.
2. **Use embedded methods** (e.g. Random Forest importance) for a more reliable ranking.
3. **If performance is the priority and you have the compute, use wrappers like `RFECV`** to fine-tune the final set.

## ✏️ Exercises

**1.** For each scenario, name the correct filter test and the sklearn function: (a) predicting customer churn (yes/no) from age, income, tenure; (b) predicting house price from square metres and room count; (c) predicting product category from brand and colour.

> [!example]- Solution
> **(a) Numerical input → Categorical output → ANOVA F-test → `f_classif`.** The test asks whether mean age/income/tenure differ between churners and non-churners.
>
> **(b) Numerical → Numerical → Pearson correlation → `f_regression`.** Note `f_regression` computes an F-statistic derived directly from Pearson's $r$; they rank features identically.
>
> **(c) Categorical → Categorical → Chi-Squared → `chi2`.** Tests whether brand and colour are independent of product category.
>
> ```python
> SelectKBest(score_func=f_classif,    k=5).fit_transform(X, y)   # (a)
> SelectKBest(score_func=f_regression, k=5).fit_transform(X, y)   # (b)
> SelectKBest(score_func=chi2,         k=5).fit_transform(X, y)   # (c)
> ```
> One critical constraint for (c): **`chi2` requires non-negative inputs.** Categorical features must be ordinal- or one-hot-encoded first (both produce non-negative values), and `chi2` must never be applied after `StandardScaler`, which produces negatives and causes it to raise.

**2.** Explain why filter methods are described as "blind to feature interactions", with a concrete example where a filter method discards a genuinely useful feature.

> [!example]- Solution
> Filter methods score each feature **independently** against the target. A feature that is uninformative alone but valuable in combination gets a low score and is dropped before any model sees it.
>
> **Concrete example — XOR.** Let $x_1, x_2 \in \{0,1\}$ be independent coin flips and let $y = x_1 \oplus x_2$:
>
> | $x_1$ | $x_2$ | $y$ |
> |---|---|---|
> | 0 | 0 | 0 |
> | 0 | 1 | 1 |
> | 1 | 0 | 1 |
> | 1 | 1 | 0 |
>
> Consider $x_1$ alone: when $x_1 = 0$, $y$ is 0 or 1 with equal frequency; likewise for $x_1 = 1$. Its χ² score is ≈ 0 and its correlation with $y$ is exactly 0. Same for $x_2$. A filter method discards **both** — yet together they determine $y$ **perfectly**.
>
> A realistic version: neither `height` nor `weight` alone may predict a health outcome well, but BMI $= w/h^2$ does. Same for drug interactions, or `income` and `household_size` predicting purchasing power.
>
> **What to use instead:** wrapper methods (RFE re-evaluates importance jointly after each removal) or embedded methods (trees split on one feature *conditional* on prior splits, which is exactly how interactions get captured). This is why the lecturer's advice puts filters **first** — as a cheap prefilter — and never as the final word.

**3.** Compare RFE with `SelectKBest` on the same dataset. Why might RFE give better model performance, and what is the danger?

> [!example]- Solution
> ```python
> from sklearn.pipeline import Pipeline
> from sklearn.model_selection import cross_val_score
>
> pipe_filter = Pipeline([('sel', SelectKBest(f_classif, k=5)),
>                         ('clf', LogisticRegression(max_iter=1000))])
>
> pipe_rfe = Pipeline([('sel', RFE(LogisticRegression(max_iter=1000),
>                                  n_features_to_select=5)),
>                      ('clf', LogisticRegression(max_iter=1000))])
>
> cross_val_score(pipe_filter, X, y, cv=5).mean()
> cross_val_score(pipe_rfe,    X, y, cv=5).mean()
> ```
> **Why RFE usually wins:** `SelectKBest` scores all features once, in isolation, and takes the top $k$ — so it happily selects five features that are highly correlated *with each other*, giving five copies of the same information. RFE removes one feature at a time and **recomputes importance on what remains**, so once a redundant twin is gone its partner's importance rises appropriately. RFE optimises the *subset*; `SelectKBest` optimises each feature separately.
>
> **The danger — selection bias / leakage.** If you run RFE on the **whole dataset** and then cross-validate, the selection already saw the validation folds and the score is optimistically biased. The selector **must sit inside the Pipeline**, as above, so it is re-fitted on each training fold. This is the same leakage principle as [[06 - Data Cleaning]], applied to selection.
>
> Second danger: `n_features_to_select=5` is a guess. Use `RFECV`, which cross-validates the number itself:
> ```python
> from sklearn.feature_selection import RFECV
> rfecv = RFECV(estimator=LogisticRegression(max_iter=1000), cv=5, scoring='accuracy')
> rfecv.fit(X, y)
> rfecv.n_features_                 # chosen automatically
> ```

**4.** You rank features by `LogisticRegression` coefficients and find `income` (coefficient 0.00003) ranked far below `n_children` (coefficient 2.1). Is `n_children` really more important? Then explain why `RandomForest.feature_importances_` might also mislead you.

> [!example]- Solution
> **No — the comparison is invalid because the data was not scaled.**
>
> A coefficient is "change in log-odds per **one unit** of the feature." One unit of `income` is **one dollar**; one unit of `n_children` is **an entire child**. Moving income by $1 should barely register. Rescale: a $10,000 income change shifts the log-odds by $0.00003 \times 10{,}000 = 0.3$, which is a substantial effect that the raw coefficient completely hid.
>
> ```python
> pipe = Pipeline([('scaler', StandardScaler()),
>                  ('clf', LogisticRegression())])
> pipe.fit(X_train, y_train)
> importance = np.abs(pipe.named_steps['clf'].coef_[0])   # now comparable
> ```
> After standardising, every coefficient means "change in log-odds per **one standard deviation**" — a common unit, so magnitudes are finally comparable.
>
> **Why tree importances also mislead:** `feature_importances_` measures total impurity reduction, and a feature offers more impurity reduction simply by offering **more places to split**. A continuous variable or a high-cardinality categorical (say `postcode` with 5,000 levels) has vastly more candidate split points than a binary flag, so it accumulates importance through sheer opportunity rather than genuine signal. Tree importance is **biased toward high-cardinality and continuous features**.
>
> It is also computed on **training** data, so a feature the model overfits to scores highly even if it generalises poorly.
>
> **Permutation importance fixes both.** It measures the actual performance drop when a feature is scrambled, it is model-agnostic, and — computed on a **held-out set** — it reflects generalisation rather than memorisation:
> ```python
> permutation_importance(model, X_test, y_test, scoring='accuracy',
>                        n_repeats=10, random_state=1, n_jobs=-1)
> ```
> One caveat it does *not* fix: with two highly correlated features, shuffling either one alone leaves the model able to lean on its twin, so **both** appear unimportant. Drop correlated features before interpreting, or use a grouped permutation.

**5.** (Advanced) Build a complete, leakage-free feature selection workflow implementing the lecturer's three-stage advice, and explain why every stage must sit inside the Pipeline.

> [!example]- Solution
> ```python
> import numpy as np
> from sklearn.pipeline import Pipeline
> from sklearn.preprocessing import StandardScaler
> from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif, RFECV
> from sklearn.ensemble import RandomForestClassifier
> from sklearn.model_selection import cross_val_score, train_test_split
> from sklearn.inspection import permutation_importance
>
> X_train, X_test, y_train, y_test = train_test_split(
>     X, y, test_size=0.2, random_state=42, stratify=y)
>
> # STAGE 1 — unsupervised + filter: cheap removal of the obviously useless
> # STAGE 3 — wrapper: RFECV picks the final subset size by cross-validation
> pipeline = Pipeline([
>     ('variance', VarianceThreshold(threshold=0)),
>     ('scaler',   StandardScaler()),
>     ('filter',   SelectKBest(score_func=f_classif, k=30)),
>     ('rfecv',    RFECV(estimator=RandomForestClassifier(random_state=1),
>                        cv=5, scoring='accuracy', n_jobs=-1)),
>     ('model',    RandomForestClassifier(random_state=1))
> ])
>
> scores = cross_val_score(pipeline, X_train, y_train, cv=5)
> print(f"CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
>
> pipeline.fit(X_train, y_train)
>
> # STAGE 2 — reliable ranking, measured on HELD-OUT data
> perm = permutation_importance(pipeline, X_test, y_test,
>                               scoring='accuracy', n_repeats=10,
>                               random_state=1, n_jobs=-1)
> ```
> **Why the ordering:** the cheap unsupervised filter runs first so the expensive wrapper faces 30 features instead of hundreds — RFECV on raw high-dimensional data is often computationally infeasible. Scaling precedes `SelectKBest`/RFECV because both the F-test and coefficient-based importance assume comparable scales.
>
> **Why everything must be inside the Pipeline — this is the whole point.** Feature selection is a *fitted* operation: it learns which columns to keep **from the target**. Run it once on all of `X_train` and then cross-validate, and every fold's "validation" data already influenced which columns exist. The reported score is inflated, sometimes dramatically — with many noise features you can produce impressive cross-validated accuracy on data that is **pure random noise**, purely by selecting features on the full set first.
>
> Inside the Pipeline, `cross_val_score` re-fits the variance filter, the scaler, `SelectKBest`, and RFECV on each training fold independently. Different folds may select different features — that is correct, and the variability is itself information about how stable your selection is.
>
> **One deliberate exception:** permutation importance runs on `X_test` *after* fitting. That is not leakage — nothing is fitted there, we are only *measuring* a finished model — and using held-out data is exactly what makes the ranking reflect generalisation rather than memorisation.

## 📝 Summary

- **Feature selection reduces overfitting, cost, and opacity** — fewer, better-understood inputs.
- **Unsupervised ignores the target; supervised uses it**, split into filter / wrapper / embedded.
- **Filters are fast but blind to interactions** — XOR-like features score zero individually yet determine the target jointly.
- **Match the test to the data types:** χ² (cat→cat), ANOVA F (num→cat), Pearson (num→num). Mutual information works for any of them and captures non-linear dependence.
- **`SelectKBest(score_func, k)`** is the common interface; `k='all'` disables selection for parameter searches.
- **Exhaustive search is impossible** ($2^N - 1$ subsets), so wrappers use forward selection or backward elimination.
- **RFE recursively drops the weakest feature**, recomputing importance each round — so it sees interactions, at high computational cost.
- **Embedded methods:** linear coefficients (**require scaling**), tree importances (**biased toward high-cardinality/continuous**), permutation importance (**model-agnostic and most reliable**).
- **Workflow:** filter for a quick cut → embedded for a reliable ranking → `RFECV` to finalise if compute allows.
- **All selection must happen inside the Pipeline**, or cross-validation scores are optimistically biased.

## ⚠️ Important Notes

**Feature selection is a fitted operation and leaks like any other.** Selecting on the full dataset before cross-validating produces inflated scores — badly enough that pure noise can appear predictive. The selector belongs inside the `Pipeline`.

**`chi2` requires non-negative features.** It will raise after `StandardScaler`. Order matters: encode → `chi2`, never scale → `chi2`. Use `MinMaxScaler` if scaling is required beforehand.

**Filter methods cannot see interactions.** Two features that are useless alone and decisive together are both discarded. Never let a filter make the final decision.

**Filters ignore redundancy too.** `SelectKBest(k=5)` will happily return five near-identical correlated features, since each is scored in isolation. RFE and embedded methods handle this; filters do not.

**Linear coefficients are meaningless as importances without scaling.** They carry the feature's units. Always `StandardScaler` first, then compare $|\text{coef}|$.

**Tree `feature_importances_` is biased toward high-cardinality and continuous features**, which offer more split points regardless of signal. It is also computed on training data, so it rewards overfitting.

**Permutation importance should be computed on held-out data.** On training data it measures memorisation. It is also unreliable when features are strongly correlated — the model compensates using the unshuffled twin, so both look unimportant.

**Pearson only detects linear relationships.** A perfect parabolic relationship ($y = x^2$ over a symmetric range) has $r = 0$. Use Spearman for monotonic non-linear relationships, or mutual information for any dependency.

**χ² needs adequate expected frequencies.** The usual guidance is $E \ge 5$ per cell; rare categories violate it and make the statistic unreliable. Merge rare levels first.

**ANOVA assumes normality and equal group variances.** It is fairly robust, but heavily skewed features should be transformed first ([[07 - Data Transformation]]) or scored with `mutual_info_classif` instead.

**RFE's `n_features_to_select` is a guess — use `RFECV`.** It cross-validates the subset size instead of you inventing one.

**Run cheap methods before expensive ones.** RFECV over hundreds of raw features is often computationally infeasible; a filter down to ~30 first makes it tractable.

> [!warning] Gaps in the source slides
> Several slides are diagrams or contain only a title:
> - **Slide 4** — "Overview of Feature Selection Techniques" (image)
> - **Slide 6** — "Diagrams Filter methods" (image)
> - **Slides 15 (Lab 3), 20 (Lab 4)** — title only; task descriptions not recoverable
> - **Slides 25, 26** — "Feature Selection" and "Summary" are images. The lecturer's own summary slide is therefore **not** captured; my Summary above is reconstructed from the body of the lesson.
>
> **Numbering in the source is inconsistent** — on-slide numbers run ahead of PDF page numbers from slide 8 onward (e.g. the page labelled "9" is the 8th page), and section headings skip (1.1 → 1.3, with no 1.2). At least one sub-slide appears to be missing from the deck.
>
> **Lab results captured:** Lab 1 (Breast Cancer, `SelectKBest(chi2, k=4)`) selected indices `[3, 4, 5, 8]` with accuracy **0.747**. Lab 2 uses the Pima Indians Diabetes dataset with `f_classif, k=4`. Neither dataset file is in `documents/`; both are widely available (Pima: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv`).

---
**Previous:** [[07 - Data Transformation]] · **Next:** [[09 - Building Pipelines]]
