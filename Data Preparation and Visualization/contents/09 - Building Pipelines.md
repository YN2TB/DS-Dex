---
subject: Data Preparation and Visualization
chapter: 09
tags: [ds, scikit-learn, pipeline, cross-validation, data-leakage, deployment]
source: "Lesson_9_Pipeline.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Building Pipelines: The Complete ML Workflow

Capstone of Part 2: cleaning ([[06 - Data Cleaning]]), transformation ([[07 - Data Transformation]]) and selection ([[08 - Feature Selection]]) combined into one object that can be fitted, cross-validated, tuned, saved and deployed. The slides answer their own questions; the lecturer's answers are kept in the Q&A boxes.

## 📘 Main Knowledge

### The running dataset

Missing values plus numeric, nominal and ordinal columns:

```python
data = {
    'age':       [25, 30, 45, 55, np.nan, 35, 60, 65, 70, 22, 48, 52],
    'income':    [50000, 60000, 100000, 80000, 120000, 75000, np.nan, 200000, 180000, 45000, 90000, 110000],
    'city':      ['Hanoi', 'HCMC', 'Hanoi', 'Danang', ...],   # nominal
    'education': ['Bachelor', 'Master', 'PhD', ...],          # ordinal
    'gender':    ['Male', 'Female', ...],                     # nominal
    'target':    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]}
```

### 1. Split first

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

> [!question]- Lecturer's Q&A 1
> **Why split before preprocessing?** To prevent leakage from the test set into training.
> **Purpose of `stratify=y`?** Class proportions in `y_train` and `y_test` match the original `y`.
> **Forgetting `random_state`?** A different split each run; results not reproducible.

### 2. A basic pipeline

A pipeline is an assembly line: impute → scale → model.

```python
simple_num_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(random_state=42))])
numeric_features = ['age', 'income']
simple_num_pipeline.fit(X_train[numeric_features], y_train)
score = simple_num_pipeline.score(X_test[numeric_features], y_test)
```

> [!question]- Lecturer's Q&A 2
> **Main benefit?** Automates the process and prevents leakage: `fit_transform` on train, `transform` on test.
> **Format of `steps`?** A list of `(name, object)` tuples.
> **Fitting on the full `X_train`?** It crashes: `StandardScaler` receives string columns like `city`.

### 3. Mixed types: `ColumnTransformer`

| Type | Examples | Needs |
|---|---|---|
| numerical | age, income | imputation, scaling |
| nominal | city, gender | imputation, one-hot encoding |
| ordinal | education | imputation, ordinal encoding |

```python
numeric_transformer = Pipeline([('imputer', SimpleImputer(strategy='median')),
                                ('scaler', StandardScaler())])
nominal_transformer = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                                ('onehot', OneHotEncoder(handle_unknown='ignore'))])
ordinal_transformer = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
                                ('ordinal', OrdinalEncoder(categories=[['Bachelor', 'Master', 'PhD']],
                                                           handle_unknown='use_encoded_value',
                                                           unknown_value=-1))])
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, ['age', 'income']),
    ('cat_nominal', nominal_transformer, ['city', 'gender']),
    ('cat_ordinal', ordinal_transformer, ['education'])])
```

Each entry is `(name, transformer, columns)`; the branches run in parallel.

> [!question]- Lecturer's Q&A 3–4
> **Nominal vs ordinal?** Nominal has no order (city); ordinal has a meaningful order (Bachelor < Master).
> **Why not `OrdinalEncoder` for city?** It creates a fake numeric relationship (Danang 2 > Hanoi 0).
> **Purpose of `ColumnTransformer`?** Apply different pipelines to different column subsets in parallel.
> **`handle_unknown='ignore'`?** No error when the test data contains a new category (a new city).
> **Why put `SimpleImputer` inside the sub-pipelines?** The median/most frequent values are learned only from training data.
> **Columns not listed?** Dropped by default (`remainder='drop'`); use `remainder='passthrough'` to keep them.

### 4. Full workflow

```python
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('selector', SelectKBest(score_func=f_classif, k=6)),
    ('model', LogisticRegression(random_state=42))])
```

After preprocessing there are 8 features: 2 numeric + 5 one-hot (3 cities + 2 genders) + 1 ordinal; `SelectKBest(k=6)` keeps 6.

> [!question]- Lecturer's Q&A 5
> **Purpose of `full_pipeline`?** One object for preprocessing, selection and modelling, with `fit` and `predict`.
> **Does order matter?** Yes: transform before selecting, select before training.
> **What does the selector do?** Keeps the 6 features most related to the target by the ANOVA F-test.
> **(Advanced) `f_classif` for numeric and `chi2` for categorical features?** Not with one selector after the preprocessor. Put `SelectKBest(f_classif)` inside `numeric_transformer` and `SelectKBest(chi2)` inside `nominal_transformer`.

(`chi2` needs non-negative input, so it cannot follow `StandardScaler`; it must go in the branch whose data suits it.)

### 5. Cross-validation

One split can be lucky or unlucky. K-fold trains on $k-1$ folds and tests on the remaining one, $k$ times.

```python
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(full_pipeline, X, y, cv=kfold, scoring='accuracy')
print(cv_scores.mean(), cv_scores.std())
```

> [!question]- Lecturer's Q&A 6
> **Why better than one split?** Averaging over 5 splits gives a more stable estimate.
> **What estimator to pass?** The `full_pipeline`; essential to prevent leakage.
> **High standard deviation?** Performance varies across folds: the model is unstable.

**Tuning with `GridSearchCV`**

```python
grid = GridSearchCV(estimator, param_grid, scoring=None, cv=None, n_jobs=-1, verbose=1)
param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf'], 'gamma': [0.01, 0.001]}   # bare estimator
param_grid = {'scaler__with_std': [True, False], 'model__C': [0.1, 1.0, 10.0],
              'model__penalty': ['l2']}                                             # pipeline
```

In a pipeline, parameters are addressed as `stepname__parameter`, nesting further with more double underscores (`preprocessor__num__imputer__strategy`).

### 6. Deployment with `joblib`

Save the whole pipeline, not just the model, so new data is processed exactly like the training data.

```python
import joblib
joblib.dump(full_pipeline, 'final_model_pipeline.joblib')
loaded_pipeline = joblib.load('final_model_pipeline.joblib')
```

> [!question]- Lecturer's Q&A 7
> **Why save the pipeline?** It contains the imputer, scaler and encoders, so new data is processed identically.
> **Functions?** `joblib.dump()` and `joblib.load()`.
> **Requirement on `X_new`?** The same column names and structure as `X_train` (missing values are fine).

## ✏️ Exercises

**1.** A pipeline `[SimpleImputer, StandardScaler, LogisticRegression]` is fitted on `X_train` that includes `city` and `education`. What happens? Fix it.

> [!example]- Solution
> It fails with `ValueError: could not convert string to float: 'Hanoi'`: a flat pipeline applies every step to every column. Fix with a `ColumnTransformer`:
> ```python
> preprocessor = ColumnTransformer([('num', numeric_transformer, ['age', 'income']),
>                                   ('cat', nominal_transformer, ['city', 'gender']),
>                                   ('ord', ordinal_transformer, ['education'])])
> pipeline = Pipeline([('preprocessor', preprocessor), ('model', LogisticRegression(random_state=42))])
> pipeline.fit(X_train, y_train)
> ```
> Fitting on numeric columns only also runs but throws away `city`, `gender` and `education`.

**2.** Why is `education` ordinal-encoded and `city` one-hot encoded? What if they were swapped?

> [!example]- Solution
> Education has a real order, so 0/1/2 carries information and one coefficient captures the trend. City has no order, so each city gets its own column.
>
> Ordinal-encoding city invents an order (alphabetically Danang 0, HCMC 1, Hanoi 2) and equal gaps that a linear model will use. One-hot encoding education is less harmful but wastes columns and loses the ordering, so the model cannot extend the trend beyond the levels seen.
>
> `Bachelor < Master < PhD` happens to be alphabetical; with `High School` added, alphabetical order puts High School above Bachelor. Always pass `categories=`.

**3.** Why is `cross_val_score(full_pipeline, X, y, cv=kfold)` leakage-free, but preprocessing `X` first and cross-validating the model is not?

> [!example]- Solution
> ```python
> X_processed = preprocessor.fit_transform(X)                 # uses all rows
> cross_val_score(LogisticRegression(), X_processed, y, cv=5)  # optimistic
> ```
> Here medians, means, standard deviations and category lists come from all rows, including each fold's validation rows.
>
> `cross_val_score(full_pipeline, ...)` clones the pipeline and refits it on each fold's training part only, so fold 3's median never sees fold 3's validation rows. With `SelectKBest` inside, folds may select different features; the spread shows how stable the workflow is.

**4.** Tune the numeric imputation strategy, the number of selected features and `C` inside `full_pipeline`.

> [!example]- Solution
> ```python
> param_grid = {'preprocessor__num__imputer__strategy': ['mean', 'median'],
>               'selector__k': [4, 6, 8],
>               'model__C': [0.01, 0.1, 1.0, 10.0]}
> grid = GridSearchCV(full_pipeline, param_grid, scoring='accuracy', cv=5, n_jobs=-1, verbose=1)
> grid.fit(X_train, y_train)
> grid.best_params_, grid.best_score_
> grid.best_estimator_.score(X_test, y_test)    # final, honest score
> ```
> `preprocessor__num__imputer__strategy` = step `preprocessor` → transformer `num` → step `imputer` → parameter `strategy`. `full_pipeline.get_params().keys()` lists every path. $2\times3\times4=24$ combinations × 5 folds = 120 fits; use `RandomizedSearchCV` for bigger grids. Each fit refits the whole pipeline, so even tuning the imputer is leakage-free.

**5.** (Advanced) A month after deployment, predictions fail. Incoming data has the same columns in a different order and a new city `'Hue'`. Which issue does the pipeline already handle?

> [!example]- Solution
> The new city is handled: `OneHotEncoder(handle_unknown='ignore')` gives all zeros for the city columns (and `OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)` maps an unseen education level to −1).
>
> Column order is handled only if the input is a DataFrame, because `ColumnTransformer` selects by name. With a numpy array, shuffled columns silently send `income` to the `age` branch (wrong predictions, no error). A missing or renamed column raises `KeyError`. Validate at the boundary:
> ```python
> expected = loaded_pipeline.feature_names_in_
> missing = set(expected) - set(X_new.columns)
> if missing:
>     raise ValueError(f"Missing required columns: {missing}")
> predictions = loaded_pipeline.predict(X_new[expected])
> ```
> Also record the scikit-learn version with the `.joblib` file, and monitor the share of unknown categories: unseen cities degrade predictions silently.

## 📝 Summary

- Split first; `stratify=y` and `random_state` for balanced, reproducible splits.
- A pipeline is a list of `(name, object)` steps; it fits on train and only transforms test.
- A flat pipeline applies each step to all columns; `ColumnTransformer` routes columns to sub-pipelines and drops unlisted ones unless `remainder='passthrough'`.
- Nominal → `OneHotEncoder(handle_unknown='ignore')`; ordinal → `OrdinalEncoder(categories=...)`.
- Order: preprocess → select → model.
- Pass the whole pipeline to `cross_val_score` and `GridSearchCV`; parameters use `step__param`.
- Save the whole pipeline with `joblib`; new data must have the training columns.

## ⚠️ Important Notes

1. Pass the pipeline, not a bare model, to cross-validation and grid search.
2. `ColumnTransformer` silently drops unlisted columns.
3. Always pass `categories=` to `OrdinalEncoder`.
4. Set `handle_unknown` on both encoders, or unseen production categories raise errors.
5. `chi2` cannot follow `StandardScaler`; put it inside the right branch.
6. A pipeline does not check whether the step order makes sense.
7. Grid search cost = combinations × folds.
8. Tune on `X_train`; use `X_test` once at the end.
9. Save the pipeline, not just the model.
10. Reorder numpy inputs (or use DataFrames) to match `feature_names_in_`.
11. Pin the scikit-learn version with saved models.
12. Monitor unknown-category rates in production.

> [!warning] Gaps in the source slides
> - Slide 12 (ColumnTransformer diagram) is an image.
> - Slide 21's GridSearchCV comments are in Vietnamese; translated inline.
> - Two slides are both headed "Question 4"; Q&A blocks renumbered.
> - Slide 19 cross-validates on all of `X, y`; for tuning, run CV on `X_train` and keep `X_test` untouched.
> - The sample dataset has 12 rows, so its accuracies are only illustrative.

**Previous:** [[08 - Feature Selection]] · **Next:** [[10 - Visualization with Matplotlib and Seaborn]]
