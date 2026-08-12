---
subject: Data Preparation and Visualization
chapter: 09
tags: [ds, scikit-learn, pipeline, cross-validation, data-leakage, deployment]
source: "Lesson_9_Pipeline.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Building Pipelines — The Comprehensive ML Workflow

> [!note] Where this sits in the course
> The **capstone of Part 2**. Every technique from [[06 - Data Cleaning]], [[07 - Data Transformation]], and [[08 - Feature Selection]] gets assembled into a single object that can be fitted, cross-validated, saved, and deployed. This is the chapter that turns a notebook into something production-ready.
>
> The slides pose numbered questions **and answer them** — unusually, the lecturer's own answers are recoverable here, and they are reproduced verbatim below because they read like exam answers.

## 📘 Main Knowledge

### The running dataset

Deliberately messy — missing values, numeric, nominal, and ordinal columns all at once:

```python
data = {
    'age':       [25, 30, 45, 55, np.nan, 35, 60, 65, 70, 22, 48, 52],
    'income':    [50000, 60000, 100000, 80000, 120000, 75000, np.nan,
                  200000, 180000, 45000, 90000, 110000],
    'city':      ['Hanoi', 'HCMC', 'Hanoi', 'Danang', ...],      # nominal
    'education': ['Bachelor', 'Master', 'PhD', ...],             # ORDINAL
    'gender':    ['Male', 'Female', ...],                        # nominal
    'target':    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]
}
```

### Part 1 — `train_test_split`: the mandatory first step

Isolate a test set **before anything else**, to prevent data leakage. All `.fit()` happens on training data only; the test set is unseen data reserved for final evaluation.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% held out
    random_state=42,    # reproducibility
    stratify=y          # preserve class balance — CRITICAL for classification
)
```

> [!question]- Lecturer's Q&A #1
> **Why must we split before any preprocessing (scaling, imputation)?**
> To prevent Data Leakage from the test set into the training process.
>
> **What is the purpose of `stratify=y`?**
> To ensure the class proportions (e.g. % of 0s and 1s) in `y_train` and `y_test` match the original `y`.
>
> **What happens if you forget `random_state`?**
> You get a different split every run, making results non-reproducible.

### Part 2 — The basic Pipeline

Think of it as an **assembly line**. For numerical data: impute → scale → train. A `Pipeline` bundles those into one object.

```python
simple_numerical_steps = [
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler()),
    ('model',   LogisticRegression(random_state=42))
]
simple_num_pipeline = Pipeline(steps=simple_numerical_steps)

numeric_features = ['age', 'income']
simple_num_pipeline.fit(X_train[numeric_features], y_train)
score = simple_num_pipeline.score(X_test[numeric_features], y_test)
```

> [!question]- Lecturer's Q&A #2
> **Main benefit of a Pipeline?**
> It automates the process and prevents data leakage by correctly calling `fit_transform` on train data and only `transform` on test data.
>
> **Required format for `steps`?**
> A list of `(name, object)` tuples, e.g. `('imputer', SimpleImputer(...))`.
>
> **What if we ran `simple_pipe.fit(X_train, y_train)` with the full `X_train`?**
> It would crash. `StandardScaler` would receive string columns like `'city'` and fail.

That last answer motivates the whole next section.

### Part 3 — Mixed data types and `ColumnTransformer`

Real data needs **different treatment per column type**:

| Type | Examples | Needs |
|---|---|---|
| **Numerical** | `age`, `income` | Imputation, Scaling |
| **Nominal** (no order) | `city`, `gender` | Imputation, One-Hot Encoding |
| **Ordinal** (has order) | `education` | Imputation, Ordinal Encoding |

`ColumnTransformer` applies different sub-pipelines to different columns **in parallel**.

**Step 1 — define sub-pipelines:**

```python
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler())
])

nominal_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot',  OneHotEncoder(handle_unknown='ignore'))
])

education_order = ['Bachelor', 'Master', 'PhD']
ordinal_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('ordinal', OrdinalEncoder(categories=[education_order],
                               handle_unknown='use_encoded_value',
                               unknown_value=-1))
])
```

**Step 2 — combine.** Each transformer is a tuple `(name, sub_pipeline, columns)`:

```python
numeric_features = ['age', 'income']
nominal_features = ['city', 'gender']
ordinal_features = ['education']

preprocessor = ColumnTransformer(transformers=[
    ('num',         numeric_transformer, numeric_features),
    ('cat_nominal', nominal_transformer, nominal_features),
    ('cat_ordinal', ordinal_transformer, ordinal_features)
])
```

> [!question]- Lecturer's Q&A #3 and #4
> **Nominal vs Ordinal?**
> A nominal feature has no inherent order (e.g. `city`). An ordinal feature has a meaningful order (e.g. `education`: Bachelor < Master).
>
> **Why can't we use `OrdinalEncoder` for `city`?**
> It would create a fake mathematical relationship (e.g. Danang (2) > Hanoi (0)), which can confuse the model.
>
> **Main purpose of `ColumnTransformer`?**
> To apply different transformation pipelines to different subsets of columns in parallel.
>
> **What does `handle_unknown='ignore'` do?**
> It prevents an error if the model sees a new category in the test data (e.g. a new city) that it never saw during training.
>
> **Why put `SimpleImputer` inside the sub-pipelines?**
> To prevent data leakage — the median (numbers) and most_frequent (categories) are learned only from the training folds.
>
> **What happens to columns not listed in any transformer, and how do you keep them?**
> By default they are **dropped** (`remainder='drop'`). Set `remainder='passthrough'` to keep them.

### Part 4 — The full workflow

Chain everything: preprocess → select → model.

```python
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('selector',     SelectKBest(score_func=f_classif, k=6)),
    ('model',        LogisticRegression(random_state=42))
])
```

After preprocessing there are **8 features**: 2 numeric + 5 one-hot (city 3 + gender 2) + 1 ordinal. `SelectKBest(k=6)` keeps the best 6 of those 8.

> [!question]- Lecturer's Q&A #5
> **Purpose of `full_pipeline`?**
> To chain all steps (preprocessing, selection, modelling) into a single object you can `fit` and `predict` with.
>
> **Does step order matter?**
> **Yes, absolutely.** Data must be cleaned/transformed before features can be selected, and features must be selected before the model is trained.
>
> **What does `('selector', SelectKBest(k=6))` do?**
> Selects the top 6 features most strongly related to the target, scored by `f_classif` (ANOVA F-test).
>
> **(Advanced) What if I want `f_classif` on numeric features and `chi2` on categorical ones?**
> You can't, with a single `SelectKBest` after the preprocessor. Remove the `('selector', ...)` step from the main Pipeline and move `SelectKBest` **inside the sub-pipelines** — `SelectKBest(f_classif)` in `numeric_transformer`, `SelectKBest(chi2)` in `nominal_transformer`.

That last answer is the elegant one: because `chi2` requires non-negative input, it cannot run after `StandardScaler` — so the test must be applied *within* the branch whose data suits it. See [[08 - Feature Selection]].

### Part 5 — Reliable evaluation with cross-validation

A single `train_test_split` score can be lucky or unlucky.

- **K-Fold** splits the data into $k$ folds, trains on $k-1$ and tests on the remaining one, repeating $k$ times.
- **`cross_val_score`** automates it.

```python
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

cv_scores = cross_val_score(full_pipeline, X, y, cv=kfold, scoring='accuracy')

print(f"Scores: {cv_scores}")
print(f"Mean Accuracy: {cv_scores.mean():.4f}")
print(f"Standard Deviation: {cv_scores.std():.4f}")
```

> [!question]- Lecturer's Q&A #6
> **Why is `cross_val_score` better than a single split?**
> A single split might be 'lucky' or 'unlucky'. CV gives a more stable, reliable estimate by averaging over 5 different splits.
>
> **What object should be passed as the estimator?**
> The **`full_pipeline`**. This is critical to prevent data leakage during cross-validation.
>
> **What does a high standard deviation of `cv_scores` tell us?**
> Performance was inconsistent across folds — the model is **unstable**.

### Hyperparameter tuning with `GridSearchCV`

```python
grid = GridSearchCV(
    estimator,      # model or pipeline to tune
    param_grid,     # parameter combinations to try
    scoring=None,   # metric: accuracy, f1, r2, ...
    cv=None,        # number of CV folds, e.g. cv=5
    n_jobs=-1,      # use all CPU cores
    verbose=1
)
```

For a bare estimator, parameter names are plain:

```python
param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf'], 'gamma': [0.01, 0.001]}
```

**For a Pipeline, use the `stepname__parameter` double-underscore syntax:**

```python
param_grid = {
    'scaler__with_std': [True, False],
    'model__C':         [0.1, 1.0, 10.0],
    'model__penalty':   ['l2']
}
```

The double underscore is how sklearn addresses a parameter *inside* a named step. It nests: `preprocessor__num__imputer__strategy` reaches the imputer strategy in the `num` branch of the `ColumnTransformer`.

### Part 6 — Deployment with `joblib`

When deploying, **save the entire Pipeline, not just the model** — this guarantees new data is preprocessed exactly as the training data was.

```python
import joblib

joblib.dump(full_pipeline, 'final_model_pipeline.joblib')
loaded_pipeline = joblib.load('final_model_pipeline.joblib')
```

> [!question]- Lecturer's Q&A #7
> **Why save the `full_pipeline` rather than the model?**
> The pipeline contains all preprocessing steps (imputer, scaler, encoders). Saving it ensures new data is processed exactly like the training data, preventing errors.
>
> **Which joblib functions?**
> `joblib.dump()` to save, `joblib.load()` to load.
>
> **What must be true of `X_new` at prediction time?**
> It must have the **exact same column names and structure** as the original `X_train` — even if it contains missing values.

That last point is the payoff of the whole design: the deployed pipeline accepts *raw, messy* data with missing values and text columns, because every cleaning step travelled with it.

## ✏️ Exercises

**1.** You run `pipeline.fit(X_train, y_train)` where the pipeline is `[SimpleImputer, StandardScaler, LogisticRegression]` and `X_train` contains `city` and `education`. Predict the error and fix it.

> [!example]- Solution
> It **crashes**. `SimpleImputer(strategy='median')` cannot compute a median of `'Hanoi'`, and `StandardScaler` cannot compute a mean of strings — you get a `ValueError: could not convert string to float: 'Hanoi'`.
>
> A flat `Pipeline` applies **every step to every column**. It has no way to express "scale these, encode those."
>
> **Fix — `ColumnTransformer`:**
> ```python
> preprocessor = ColumnTransformer(transformers=[
>     ('num', numeric_transformer, ['age', 'income']),
>     ('cat', nominal_transformer, ['city', 'gender']),
>     ('ord', ordinal_transformer, ['education'])
> ])
> pipeline = Pipeline([('preprocessor', preprocessor),
>                      ('model', LogisticRegression(random_state=42))])
> pipeline.fit(X_train, y_train)   # works on the full frame
> ```
> The quick-and-dirty alternative — `pipeline.fit(X_train[numeric_features], y_train)` — works but throws away `city`, `gender`, and `education` entirely, discarding real predictive signal.

**2.** In the `ColumnTransformer` above, `education` is handled with `OrdinalEncoder(categories=[education_order])` while `city` uses `OneHotEncoder`. Explain both choices, and say what goes wrong if they are swapped.

> [!example]- Solution
> **`education` is ordinal:** Bachelor < Master < PhD is a real ordering, so integers 0/1/2 encode genuine information. The model can learn "more education → higher target" as a single monotonic relationship, in one coefficient.
>
> **`city` is nominal:** Hanoi, HCMC, and Danang have no order. One-hot gives each its own binary column and its own coefficient, with no ordering implied.
>
> **Swapping them breaks things in two different ways.**
>
> *Ordinal-encoding `city`* invents a fake ordering — `Danang=0, HCMC=1, Hanoi=2` implies Hanoi > HCMC > Danang and that the gap Danang→HCMC equals HCMC→Hanoi. A linear model acts on that arithmetic and produces nonsense. (Note the encoding would be **alphabetical** by default, so the fake ordering isn't even a meaningful one.)
>
> *One-hot-encoding `education`* is less catastrophic but wasteful: it discards the ordering, spends 3 columns instead of 1, and forces the model to learn each level independently — meaning it cannot generalise that PhD continues the trend beyond Master. With little data per level, that hurts.
>
> Note the explicit `categories=[education_order]`. Without it `OrdinalEncoder` sorts **alphabetically**: `Bachelor=0, Master=1, PhD=2` — which happens to be correct here **by luck**. With `['High School', 'Bachelor', 'Master', 'PhD']` alphabetical order gives `Bachelor=0, High School=1, Master=2, PhD=3`, ranking High School above Bachelor. **Always pass `categories=`.**

**3.** Explain why `cross_val_score(full_pipeline, X, y, cv=kfold)` is leakage-free, whereas preprocessing `X` first and then cross-validating the model alone is not.

> [!example]- Solution
> **The wrong way:**
> ```python
> X_processed = preprocessor.fit_transform(X)          # sees ALL data
> cross_val_score(LogisticRegression(), X_processed, y, cv=5)
> ```
> `fit_transform(X)` computes medians, means, standard deviations, and category lists from **every row** — including rows that will serve as validation data in each fold. Every "held-out" fold was already involved in defining the transformation applied to it. The score comes out optimistically biased.
>
> **The right way:**
> ```python
> cross_val_score(full_pipeline, X, y, cv=kfold)
> ```
> `cross_val_score` **clones the pipeline for each fold** and re-fits it from scratch on that fold's training portion only. Fold 3's median is computed without ever seeing fold 3's validation rows.
>
> Concretely, in fold 1: `imputer.fit_transform(X_train_fold1)` learns the median of *that* subset, then `imputer.transform(X_val_fold1)` applies it. In fold 2 an entirely new median is computed. Different folds may even select different features if `SelectKBest` is in the pipeline — that is correct behaviour, and the spread across folds tells you how stable your workflow is.
>
> This is why Q&A #6's answer — "pass the `full_pipeline`" — is emphasised. Passing a bare model to `cross_val_score` after preprocessing everything is the single most common way people accidentally inflate their reported accuracy.

**4.** Write a `GridSearchCV` that tunes the imputation strategy for numeric features, the number of selected features, and the regularisation strength `C`, all within `full_pipeline`. Explain the naming syntax.

> [!example]- Solution
> ```python
> from sklearn.model_selection import GridSearchCV
>
> param_grid = {
>     'preprocessor__num__imputer__strategy': ['mean', 'median'],
>     'selector__k':                          [4, 6, 8],
>     'model__C':                             [0.01, 0.1, 1.0, 10.0]
> }
>
> grid = GridSearchCV(full_pipeline, param_grid, scoring='accuracy',
>                     cv=5, n_jobs=-1, verbose=1)
> grid.fit(X_train, y_train)
>
> grid.best_params_
> grid.best_score_
> grid.best_estimator_.score(X_test, y_test)   # honest final number
> ```
> **The `__` syntax walks the nesting, one level per double underscore:**
>
> `preprocessor__num__imputer__strategy`
> → step `'preprocessor'` (the ColumnTransformer)
> → its transformer named `'num'`
> → that sub-pipeline's step `'imputer'`
> → that object's `strategy` parameter.
>
> This is why every step needs a **name** — the names are the address. Use `full_pipeline.get_params().keys()` to list every tunable path when you are unsure.
>
> Grid size: 2 × 3 × 4 = 24 combinations × 5 folds = **120 fits**. That multiplies fast, which is why `n_jobs=-1` matters and why `RandomizedSearchCV` is preferred for large grids.
>
> Critically, the *entire pipeline* is re-fitted for each combination on each fold — so tuning the imputation strategy is itself leakage-free. Tuning a preprocessing choice honestly is something you simply cannot do without this structure.

**5.** (Advanced) You deploy `final_model_pipeline.joblib`. A month later, production predictions fail with `ValueError`. The incoming data has the same columns but in a different order, and contains a city (`'Hue'`) never seen in training. Diagnose both issues and explain which the pipeline already handles.

> [!example]- Solution
> **The new city is already handled** — thanks to `handle_unknown='ignore'` on the `OneHotEncoder`. `'Hue'` produces all-zeros across the city columns instead of raising. The row is treated as "none of the known cities", which is a reasonable degradation. Without that parameter it would raise `Found unknown categories`.
>
> Similarly, `OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)` maps an unseen education level to −1 rather than crashing. Both are deliberate production-hardening choices in the lecturer's code.
>
> **Column order is the real bug.** `ColumnTransformer` selects by **name**, so ordering *should* be tolerated — but only if you pass a DataFrame. The failure modes:
> - If production passes a **numpy array**, positional order is all there is, and shuffled columns silently feed `income` into the `age` transformer. **No error — just wrong predictions**, which is worse than a crash.
> - If a column is **missing or renamed**, `ColumnTransformer` raises `KeyError`.
> - sklearn ≥ 1.0 records `feature_names_in_` at fit time and warns or raises when the incoming frame disagrees.
>
> **The fix — validate the contract at the boundary:**
> ```python
> expected = loaded_pipeline.feature_names_in_
> missing = set(expected) - set(X_new.columns)
> if missing:
>     raise ValueError(f"Missing required columns: {missing}")
> X_new = X_new[expected]      # reorder to the training layout
> predictions = loaded_pipeline.predict(X_new)
> ```
> This is Q&A #7's third answer in practice: `X_new` must have the same column names and structure as `X_train`. Missing *values* are fine — the imputer handles them. Missing or reordered *columns* are not.
>
> Two further production concerns the slides do not raise. **Version pinning:** a joblib file is not guaranteed to load across scikit-learn versions; record the version alongside the artefact. And **`'Hue'` mapping to all-zeros is silent** — if a whole new region appears, predictions quietly degrade with no error. Log unknown-category rates in production; a rising rate is the signal that the model needs retraining.

## 📝 Summary

- **`train_test_split` first, always.** `stratify=y` preserves class balance; `random_state` makes it reproducible.
- **A `Pipeline` is a list of `(name, object)` tuples** that calls `fit_transform` on train and `transform` on test — leakage prevention by construction.
- **A flat Pipeline applies every step to every column**, so it crashes on mixed data.
- **`ColumnTransformer` routes different sub-pipelines to different columns** — `(name, pipeline, columns)`. Unlisted columns are **dropped** unless `remainder='passthrough'`.
- **Nominal → `OneHotEncoder`, ordinal → `OrdinalEncoder(categories=[...])`.** Order in a Pipeline matters: preprocess → select → model.
- **`handle_unknown='ignore'`** keeps unseen categories from crashing production.
- **`cross_val_score(full_pipeline, ...)`** — pass the *whole* pipeline, or cross-validation leaks. High `std` across folds means an unstable model.
- **`GridSearchCV` addresses nested parameters with `step__param`**, nesting further with more double underscores.
- **`joblib.dump(pipeline)` saves the entire workflow**, so deployed code accepts raw data. `X_new` must match `X_train`'s columns exactly.

## ⚠️ Important Notes

**Pass the pipeline — not the model — to `cross_val_score` and `GridSearchCV`.** This is the single highest-value rule in the chapter. Preprocessing everything first and cross-validating the bare model is the standard way people accidentally report inflated accuracy.

**`ColumnTransformer` drops unlisted columns silently.** `remainder='drop'` is the default, so forgetting a column means losing it with no warning. Use `remainder='passthrough'` deliberately.

**Always pass `categories=` to `OrdinalEncoder`.** Alphabetical is the default and it is usually wrong. `['High School', 'Bachelor', 'Master', 'PhD']` sorts to put High School above Bachelor.

**Set `handle_unknown='ignore'` (OneHot) and `handle_unknown='use_encoded_value'` (Ordinal).** Without them a category that appears only in production raises at `transform` time — a failure that never shows up in testing.

**`chi2` cannot follow `StandardScaler`** — it requires non-negative input. Put the selector *inside* the appropriate sub-pipeline, per the lecturer's advanced answer, rather than after the preprocessor.

**Step order is semantic, not stylistic.** Scale before polynomial expansion, preprocess before selection, select before modelling. A Pipeline will not warn you about a nonsensical order.

**`GridSearchCV` cost multiplies.** Parameters × values × folds. 24 combinations at `cv=5` is 120 fits. Use `n_jobs=-1`, and `RandomizedSearchCV` once the grid grows.

**Never tune on the test set.** Run `GridSearchCV` on `X_train`; touch `X_test` exactly once, at the end, via `best_estimator_.score(X_test, y_test)`. Repeatedly checking the test score turns it into a training set.

**Save the pipeline, not the model.** A saved bare model requires you to re-implement every preprocessing step at inference — and any discrepancy produces silently wrong predictions rather than an error.

**Column order matters when the input is a numpy array.** `ColumnTransformer` selects by name only for DataFrames. Reorder explicitly with `X_new[pipeline.feature_names_in_]` before predicting.

**Pin your scikit-learn version alongside the `.joblib` file.** Pickled estimators are not guaranteed to load across versions.

**Unknown categories degrade silently.** `handle_unknown='ignore'` maps an unseen city to all-zeros — no error, quietly worse predictions. Monitor the unknown-category rate in production as a retraining trigger.

> [!warning] Gaps in the source slides
> - **Slide 12** — the `ColumnTransformer` architecture diagram is an image.
> - **Slide 21** — the `GridSearchCV` parameter comments are written in **Vietnamese**; I have translated them inline.
> - **Slide numbering repeats** — two consecutive slides are both headed "Question 4" (PDF pages 15 and 17); I have renumbered the Q&A blocks sequentially.
> - Cross-validation on slide 19 is demonstrated on the **entire `X, y`** rather than `X_train`. The slide notes both are valid, but be aware: using all of `X` gives the most general performance estimate and leaves no untouched holdout. For hyperparameter tuning, run CV on `X_train` and keep `X_test` sealed.
> - The sample dataset has only **12 rows**, so any accuracy figures from it are illustrative, not meaningful.

---
**Previous:** [[08 - Feature Selection]] · **Next:** [[10 - Visualization with Matplotlib and Seaborn]]
