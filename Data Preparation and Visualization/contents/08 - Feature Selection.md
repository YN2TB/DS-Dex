---
subject: Data Preparation and Visualization
chapter: 08
tags: [ds, feature-selection, scikit-learn, statistics, dimensionality-reduction]
source: "Lesson_8_Feature Selection.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Feature Selection

Closes Part 2. [[07 - Data Transformation]] created features (`PolynomialFeatures` can turn 60 columns into 1,891); this chapter decides which to keep.

## 📘 Main Knowledge

### What and why

**Feature selection** reduces the number of input variables. Reasons:
- less overfitting, better generalization;
- less computation;
- easier interpretation (10 understood features vs 500), important for stakeholders and regulators.

### Taxonomy

- **Unsupervised**: ignores the target; drop low-variance or highly correlated features (`VarianceThreshold`, [[06 - Data Cleaning]]).
- **Supervised**: uses the target.

| Family | How | Speed | Sees interactions? |
|---|---|---|---|
| Filter | statistical test of each feature vs the target, before modelling | fast | no |
| Wrapper | searches subsets using a model's performance | slow | yes |
| Embedded | selection inside training (LASSO, random forest) | moderate | yes |

Filters score features one at a time, so two features useful only together are both discarded.

### Part I: Filter methods

The test depends on the input and output types.

**Categorical → categorical: chi-squared**
- H₀: feature and target independent; H₁: dependent.
$$\chi^2 = \sum \frac{(O - E)^2}{E}$$
($O$ observed, $E$ expected counts under independence). Higher χ² → stronger evidence of association → more useful feature. Needs expected counts not too small (usually $E\ge5$). See [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

**Numerical → categorical: ANOVA F-test**: does the feature's mean differ across classes?
$$F = \frac{\text{variance between groups}}{\text{variance within groups}}$$
Larger F → better separation. Assumes normality and equal variances (fairly robust).

**Numerical → numerical: Pearson correlation**
$$r_{xy} = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2}\sqrt{\sum(y_i - \bar{y})^2}}\in[-1,1]$$
Fast, gives size and direction, but only linear relationships. Alternatives: Spearman (monotonic), mutual information (any dependence).

| Input | Output | Test | sklearn |
|---|---|---|---|
| categorical | categorical | χ², mutual information | `chi2`, `mutual_info_classif` |
| numerical | categorical | ANOVA F, mutual information | `f_classif`, `mutual_info_classif` |
| numerical | numerical | Pearson | `f_regression` |

```python
from sklearn.feature_selection import SelectKBest, chi2
X_selected = SelectKBest(score_func=chi2, k=4).fit_transform(X, y)
```
`score_func`: `chi2`, `f_classif`, `f_regression`, `mutual_info_classif`, `mutual_info_regression`. `k` (default 10); `k='all'` keeps everything (useful when tuning `k`).

Lab 1 (Breast Cancer, `SelectKBest(chi2, k=4)`): selected indices `[3, 4, 5, 8]`, accuracy 0.747.

### Part II: Wrapper methods

Evaluate feature subsets with a specific model. With $N$ features there are $2^N-1$ subsets (≈ $1.15\times10^{18}$ for the 60-feature Sonar data), so wrappers search stepwise:
- **forward selection**: start empty, add the most helpful feature each time;
- **backward elimination**: start with all, remove the least important each time (RFE).

**Recursive Feature Elimination (RFE)**
1. Fit a model on all features (it must expose `coef_` or `feature_importances_`).
2. Remove the least important feature.
3. Repeat until $k$ remain.

```python
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=5, step=1)
```

| Parameter | Meaning |
|---|---|
| `estimator` | model with `coef_` or `feature_importances_` |
| `n_features_to_select` | integer count, fraction in (0, 1), or `None` (half) |
| `step` | features removed per round (int) or share removed (float) |

Often better than filters because importance is recomputed after each removal (interactions, redundancy), but expensive and can overfit without cross-validation.

### Part III: Embedded methods

**Coefficients**: |coefficient| of a linear model as importance.
```python
model_lr = LogisticRegression(solver='lbfgs').fit(X_clf, y_clf)
importance_lr = model_lr.coef_[0]
```
Features must be scaled first; otherwise coefficients reflect units (millimetres vs metres differ by 1,000×).

**Tree importance**: total improvement in node purity (e.g. Gini) from splits on each feature.
```python
model_rf = RandomForestClassifier(random_state=1).fit(X_clf, y_clf)
importance_rf = model_rf.feature_importances_
```
Captures non-linear effects but is biased toward continuous and high-cardinality features (more possible split points).

**Permutation importance**: shuffle one feature and measure the drop in performance. Model-agnostic and among the most reliable.
```python
from sklearn.inspection import permutation_importance
results_perm = permutation_importance(model_rf, X_clf, y_clf, scoring='accuracy',
                                      n_repeats=10, random_state=1, n_jobs=-1)
importance_perm = results_perm.importances_mean
```
Shuffling breaks the link to the target but keeps the feature's distribution, so the drop is due to that feature.

**Lecturer's workflow**
1. Filter methods first, to remove obviously irrelevant features quickly.
2. Embedded methods (e.g. random forest importance) for a more reliable ranking.
3. If performance matters and compute allows, a wrapper such as `RFECV` to finalize.

## ✏️ Exercises

**1.** Name the filter test and sklearn function: (a) churn (yes/no) from age, income, tenure; (b) house price from area and rooms; (c) product category from brand and colour.

> [!example]- Solution
> (a) Numerical → categorical: ANOVA F, `f_classif`. (b) Numerical → numerical: Pearson, `f_regression` (its F statistic is derived from $r$ and ranks features the same way). (c) Categorical → categorical: χ², `chi2`.
>
> `chi2` needs non-negative inputs: encode categories (ordinal or one-hot) and never apply it after `StandardScaler`.

**2.** Why are filters "blind to interactions"? Give an example.

> [!example]- Solution
> Each feature is scored alone. With $x_1, x_2\in\{0,1\}$ independent coin flips and $y=x_1\oplus x_2$ (XOR):
>
> | $x_1$ | $x_2$ | $y$ |
> |---|---|---|
> | 0 | 0 | 0 |
> | 0 | 1 | 1 |
> | 1 | 0 | 1 |
> | 1 | 1 | 0 |
>
> For either feature alone, $y$ is 0 or 1 equally often at each value: χ² ≈ 0, correlation 0. A filter drops both, yet together they determine $y$ exactly. Realistic cases: height and weight vs BMI; income and household size vs purchasing power. Wrappers (RFE) and trees (conditional splits) can capture this, which is why filters come first and are not the final word.

**3.** Compare RFE with `SelectKBest`. Why might RFE do better, and what is the danger?

> [!example]- Solution
> ```python
> pipe_filter = Pipeline([('sel', SelectKBest(f_classif, k=5)),
>                         ('clf', LogisticRegression(max_iter=1000))])
> pipe_rfe = Pipeline([('sel', RFE(LogisticRegression(max_iter=1000), n_features_to_select=5)),
>                      ('clf', LogisticRegression(max_iter=1000))])
> cross_val_score(pipe_filter, X, y, cv=5).mean(); cross_val_score(pipe_rfe, X, y, cv=5).mean()
> ```
> `SelectKBest` may pick five highly correlated features (the same information five times). RFE recomputes importance after each removal, so once a redundant twin is removed the other keeps its importance; it optimizes the subset.
>
> Danger: running RFE on the whole dataset before cross-validation leaks (the selection saw the validation folds). Keep the selector inside the pipeline. Also, `n_features_to_select=5` is a guess; `RFECV(estimator=..., cv=5)` chooses it by cross-validation (`rfecv.n_features_`).

**4.** `income` has coefficient 0.00003 and `n_children` 2.1 in an unscaled logistic regression. Is `n_children` more important? Why might random-forest importances also mislead?

> [!example]- Solution
> Not necessarily: a coefficient is the change in log-odds per unit. One unit of income is \$1; one unit of `n_children` is a whole child. A \$10,000 change gives $0.00003\times10{,}000=0.3$ in log-odds, a sizeable effect. Standardize first so each coefficient means "per standard deviation":
> ```python
> pipe = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression())]).fit(X_train, y_train)
> importance = np.abs(pipe.named_steps['clf'].coef_[0])
> ```
> Tree importances favour continuous and high-cardinality features (e.g. a postcode with 5,000 levels has many split points) and are computed on training data, so they reward overfitting. Permutation importance on held-out data avoids both:
> ```python
> permutation_importance(model, X_test, y_test, scoring='accuracy', n_repeats=10, random_state=1, n_jobs=-1)
> ```
> It still undervalues correlated features: shuffle one and the model uses its twin, so both look unimportant.

**5.** (Advanced) Build a leakage-free workflow following the lecturer's three stages, and explain why every stage is inside the pipeline.

> [!example]- Solution
> ```python
> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
> pipeline = Pipeline([
>     ('variance', VarianceThreshold(threshold=0)),
>     ('scaler', StandardScaler()),
>     ('filter', SelectKBest(score_func=f_classif, k=30)),
>     ('rfecv', RFECV(estimator=RandomForestClassifier(random_state=1), cv=5, scoring='accuracy', n_jobs=-1)),
>     ('model', RandomForestClassifier(random_state=1))])
> scores = cross_val_score(pipeline, X_train, y_train, cv=5)
> pipeline.fit(X_train, y_train)
> perm = permutation_importance(pipeline, X_test, y_test, scoring='accuracy',
>                               n_repeats=10, random_state=1, n_jobs=-1)
> ```
> The cheap filters reduce the input so RFECV only sees 30 features. Selection learns from the target, so doing it once on all training data before cross-validation inflates scores (pure noise can look predictive). Inside the pipeline, each fold refits every step; different folds may select different features, which shows how stable the selection is. Permutation importance on `X_test` is fine because nothing is fitted there.

## 📝 Summary

- Feature selection reduces overfitting, cost and complexity.
- Unsupervised vs supervised (filter, wrapper, embedded).
- Filters are fast but ignore interactions and redundancy.
- χ² (cat → cat), ANOVA F (num → cat), Pearson (num → num); mutual information for any type and non-linear dependence.
- `SelectKBest(score_func, k)`; `k='all'` for tuning.
- Wrappers search stepwise; RFE removes the weakest feature and recomputes.
- Embedded: coefficients (scale first), tree importances (biased), permutation importance (reliable, use held-out data).
- Workflow: filter → embedded ranking → `RFECV`; all inside a pipeline.

## ⚠️ Important Notes

1. Selection is fitted and leaks like any other step; keep it in the pipeline.
2. `chi2` needs non-negative features; use it after encoding (or `MinMaxScaler`), not after `StandardScaler`.
3. Filters cannot see interactions and may keep redundant features.
4. Unscaled coefficients are not importances.
5. Tree importances favour high-cardinality/continuous features and reflect training fit.
6. Compute permutation importance on held-out data; beware correlated features.
7. Pearson misses non-linear relations: $y=x^2$ on a symmetric range has $r=0$.
8. χ² is unreliable with small expected counts; merge rare levels.
9. Transform skewed features before ANOVA or use mutual information.
10. Use `RFECV` instead of guessing the number of features.
11. Run cheap methods before expensive ones.

> [!warning] Gaps in the source slides
> - Slide 4 (overview), slide 6 (filter diagram), slides 15 and 20 (Labs 3–4, titles only), slides 25–26 (feature selection, summary) are images; the summary above is mine.
> - On-slide numbers run ahead of PDF pages from slide 8, and headings skip 1.2; a sub-slide appears to be missing.
> - Lab 2 uses Pima Indians Diabetes with `f_classif, k=4` (`https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv`); neither lab dataset is in `documents/`.

**Previous:** [[07 - Data Transformation]] · **Next:** [[09 - Building Pipelines]]
