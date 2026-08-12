---
subject: Data Preparation and Visualization
chapter: 06
tags: [ds, data-cleaning, outliers, imputation, scikit-learn, data-leakage]
source: "Lesson_6_Data Cleaning.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Cleaning

> [!note] Where this sits in the course
> First chapter of **Part 2 — Becoming a Data Architect**. The tone changes here: [[01 - Getting Started with Pandas]] through [[05 - String Manipulation and Time Series Data]] were about *manipulating* data with Pandas. From now on the target is an **ML model**, the library shifts to **scikit-learn**, and every decision is judged by whether it improves the model without leaking information into it.

## 📘 Main Knowledge

### Why cleaning is crucial

**"Garbage In, Garbage Out"** — the course's founding principle, from Lesson 0. Models learn patterns from whatever they are given; flawed, noisy, or incorrect data produces unreliable models no algorithm can rescue. Data quality is the **ceiling** on performance.

Clean data buys you: better accuracy, more robust and generalisable models, and fewer errors during training.

The lesson has four parts: **basic cleaning → outliers → missing data → pipelines**, and that order is the recommended workflow.

---

## Part 1 — Basic cleaning

Two cheap, high-value steps that come first.

### Zero-variance features

A feature whose values are all identical has variance

$$\operatorname{Var}(X) = \frac{\sum_{i=1}^{N}(x_i - \mu)^2}{N} = 0$$

and therefore carries **no information** — there is nothing for a model to learn from a column that never changes.

```python
from sklearn.feature_selection import VarianceThreshold

transformer = VarianceThreshold(threshold=0)
data_transformed = transformer.fit_transform(df_oil)

retained_cols = transformer.get_feature_names_out(input_features=df_oil.columns)
data_cleaned = pd.DataFrame(data_transformed, columns=retained_cols)
```

`VarianceThreshold` **only works on numerical data**. Raising `threshold` above 0 also removes *near*-constant features.

**For categorical columns**, use `nunique()` — a column where every entry is `'USA'` is equally useless:

```python
df_oil.drop(columns=df_oil.columns[df_oil.nunique() == 1])
```

### Duplicate rows

Exact copies of each other. The risk is twofold: they **overweight** whatever pattern they contain, and — if duplicates land on both sides of a train/test split — they cause **data leakage**, since the model is tested on rows it literally memorised.

```python
df_oil.duplicated().sum()      # how many
df_oil.drop_duplicates()       # remove them
```

---

## Part 2 — Handling outliers

Observations significantly different from the rest. Causes: measurement error, data-entry mistakes, or **genuinely rare events**. They skew statistics and disproportionately drag model parameters.

That third cause is why "outlier" ≠ "delete". A fraudulent transaction is an outlier *and* the entire thing you are trying to predict.

### Method 1 — Standard deviation

Assumes a Gaussian distribution. Flags points more than $k$ standard deviations from the mean:

$$\text{lower} = \mu - k\sigma \qquad \text{upper} = \mu + k\sigma$$

$k = 3$ is the common rule (covering ~99.7% of a normal distribution); the slides use $k = 2$ to make outliers visible in a tiny demo set.

```python
data_col = df_housing['MEDV']
mean, std = data_col.mean(), data_col.std()
cut_off = std * 2
lower, upper = mean - cut_off, mean + cut_off

outliers = df_housing[(data_col < lower) | (data_col > upper)]
data_cleaned_outlier = df_housing[(data_col >= lower) & (data_col <= upper)]
```

**Use when:** data is normally or near-normally distributed.

### Method 2 — Interquartile range (IQR)

Distribution-free and robust:

$$\text{IQR} = Q_3 - Q_1 \qquad \text{lower} = Q_1 - 1.5 \times \text{IQR} \qquad \text{upper} = Q_3 + 1.5 \times \text{IQR}$$

```python
Q1, Q3 = data_col.quantile(0.25), data_col.quantile(0.75)
IQR = Q3 - Q1
lower_iqr, upper_iqr = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

outliers_iqr = df_housing[(data_col < lower_iqr) | (data_col > upper_iqr)]
```

**Use when:** data is skewed, or you want a method that extreme values cannot corrupt.

> [!tip] Why IQR beats standard deviation in practice
> The mean and standard deviation are **themselves inflated by the outliers you are hunting**. One extreme value pulls $\mu$ toward it and enlarges $\sigma$, widening the very bounds meant to catch it — the outlier hides behind its own influence. Quartiles are positional, so extreme values cannot move them. This is the same robustness argument behind the $\hat\sigma \approx 0.74 \times \text{IQR}$ estimator in [[03 - Data Aggregation and Group Operations]].
>
> It is also the boundary rule behind the whiskers on a boxplot — see [[10 - Visualization with Matplotlib and Seaborn]].

### Method 3 — Local Outlier Factor (LOF)

Both methods above are **univariate** — one column at a time. LOF is **multivariate**: it finds points whose *local density* is much lower than their neighbours'.

This catches a different species of outlier. A house of 200 m² is unremarkable. A price of $50,000 is unremarkable. A 200 m² house at $50,000 is anomalous — and no single-column method can see it.

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor()
yhat = lof.fit_predict(df_housing)
mask = yhat != -1                      # LOF: 1 = inlier, -1 = outlier
df_housing[mask]
```

| Parameter | Default | Role |
|---|---|---|
| `n_neighbors` | 20 | Neighbours used for the local density estimate. The main tuning knob. |
| `contamination` | `'auto'` | Expected proportion of outliers; sets the decision threshold. |

> [!warning] Correct train/test usage — this is examinable
> - **Training data:** `yhat_train = lof.fit_predict(X_train)` → learn the distribution and **remove** the flagged rows.
> - **Test data:** `yhat_test = lof.predict(X_test)` → **predict only**. Do not re-fit, and **do not remove outliers from the test set**.
> - **Never** fit on the combined dataset before splitting. That is **data leakage**.
>
> The asymmetry has a reason: the test set stands in for production data, and in production you cannot delete inconvenient rows. Cleaning the test set flatters your metrics and the model then fails in the real world.

---

## Part 3 — Handling missing data

Most ML algorithms **cannot accept `NaN` at all** — they raise rather than cope. Four strategies, in ascending sophistication.

The demo dataset uses `?` as its missing marker, which `read_csv` must be told about (compare [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]]):

```python
df_horse = pd.read_csv(io.StringIO(csv_horse), na_values='?')
```

### Strategy 1 — Removal

```python
df_horse.isnull().sum()
data_dropped = df_horse.dropna()
```
**Pro:** quick and simple. **Con:** potentially severe data loss, and **bias** if the missingness is not random.

### Strategy 2 — Statistical imputation

Replace with a column summary.

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')
data_imputed_mean = imputer.fit_transform(df_horse)
```

| Parameter | Options |
|---|---|
| `strategy` | `'mean'` (default), `'median'`, `'most_frequent'`, `'constant'` |
| `fill_value` | The value used when `strategy='constant'` |

`'median'` is safer for skewed data; `'most_frequent'` is the only one of the four that works on categorical columns.

### Strategy 3 — KNN imputation

Multivariate: find the $k$ most similar rows and average their values for the missing field.

```python
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=2, weights='uniform')
data_imputed_knn = knn_imputer.fit_transform(df_horse)
```

| Parameter | Default | Role |
|---|---|---|
| `n_neighbors` | 5 | Number of neighbours |
| `weights` | `'uniform'` | `'uniform'` = equal weight; `'distance'` = closer neighbours count more |

Preserves relationships between features that `SimpleImputer` destroys — but requires scaled features, since distance is meaningless across mismatched units.

### Strategy 4 — Iterative imputation (MICE)

Treats imputation as a **modelling problem**: each feature with gaps is regressed on all the others, repeatedly, until values stabilise.

```python
from sklearn.experimental import enable_iterative_imputer   # required import
from sklearn.impute import IterativeImputer

iter_imputer = IterativeImputer(max_iter=10, random_state=0)
data_imputed_iter = iter_imputer.fit_transform(df_horse)
```

| Parameter | Default | Role |
|---|---|---|
| `estimator` | `BayesianRidge()` | The regressor; `RandomForestRegressor` also works |
| `max_iter` | 10 | Maximum imputation rounds |
| `random_state` | — | For reproducibility |

Still marked **experimental** in scikit-learn, hence the mandatory `enable_iterative_imputer` import.

---

## Part 4 — Automating with pipelines

### The danger: data leakage

**Data leakage** is any use of information from outside the training set to build the model.

The canonical example is exactly what everything above invites you to do: **compute an imputation mean over the whole dataset, then split into train/test**. The mean now encodes test-set values; the model has seen data it will be judged on. Test scores come out optimistic and the model fails in production.

The same trap applies to scaling, encoding, feature selection, and outlier removal — every step that *learns a parameter from data*.

### The solution: `sklearn.pipeline.Pipeline`

A Pipeline chains transformers and a final estimator into one object, and enforces the correct fitting discipline automatically:

```python
steps = [('imputer', SimpleImputer()), ('model', RandomForestClassifier())]
pipeline = Pipeline(steps)
pipeline.fit(X_train, y_train)
```

**Full worked example:**

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Prepare — drop rows whose TARGET is missing (never impute the target)
df_clean = df_lab3.dropna(subset=['outcome'])
X = df_clean.drop('outcome', axis=1)
y = df_clean['outcome']

# 2. Split FIRST
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 3. Build the pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('model', RandomForestClassifier(random_state=42))
])

# 4. Fit — sklearn calls imputer.fit_transform(X_train), then model.fit(...)
pipeline.fit(X_train, y_train)

# 5. Predict — sklearn calls imputer.transform(X_test), NOT fit_transform
y_pred = pipeline.predict(X_test)
accuracy_score(y_test, y_pred)
```

**The whole point is step 5.** On training data the imputer calls `fit_transform` (learn the medians, then apply). On test data it calls `transform` only (apply the *training* medians). You get that for free and cannot forget it. Pipelines are developed further in [[09 - Building Pipelines]].

The components:

- **`train_test_split`** — splits into train and test so evaluation happens on unseen data, preventing the model from being scored on what it memorised.
- **`SimpleImputer`** — first step; guarantees complete data reaches the model.
- **`RandomForestClassifier`** — final estimator; many decision trees whose outputs are merged. See [[Machine Learning/contents/00-Index|Machine Learning]].

## ✏️ Exercises

**1.** In the oil-spill sample below, identify which columns should be dropped and why, then write code that removes both zero-variance columns and duplicate rows.
> ```python
> csv_data = '''f_1,f_2,f_3,f_4,f_5
> 1,25.4,3.8,0,10
> 2,22.3,4.1,0,12
> 3,26.1,3.7,0,10
> 4,24.8,3.9,0,11
> 2,22.3,4.1,0,12'''
> ```

> [!example]- Solution
> **`f_4` is zero-variance** — every value is 0, so $\operatorname{Var}(f_4) = 0$ and it can tell a model nothing. **Row 5 duplicates row 2** exactly.
>
> ```python
> df_oil = pd.read_csv(io.StringIO(csv_data))
>
> df_oil.duplicated().sum()          # 1
> df_oil = df_oil.drop_duplicates()
> df_oil = df_oil.drop(columns=df_oil.columns[df_oil.nunique() == 1])
> ```
> Order matters slightly: dropping duplicates first is cheaper, and in edge cases removing rows can *create* a newly constant column.
>
> Using `nunique() == 1` rather than `VarianceThreshold` here is deliberate — it works on categorical columns too, whereas `VarianceThreshold` is numeric-only. The scikit-learn equivalent:
> ```python
> transformer = VarianceThreshold(threshold=0)
> transformer.fit_transform(df_oil)
> ```
> Note `f_1` looks like an ID column (1,2,3,4). It has high variance so no automated check catches it, but feeding a row identifier to a model is useless at best and leakage at worst. Automated checks do not replace looking at your columns.

**2.** For the `MEDV` column of the housing sample, compute the outlier bounds under both the 2σ rule and the IQR rule. Which flags the injected outlier row (`MEDV = 500`), and which is more trustworthy here?

> [!example]- Solution
> The six `MEDV` values are 24, 21.6, 34.7, 33.4, 36.2, **500**.
>
> **Standard deviation:** mean ≈ 108.3, std ≈ 192.2, so with $k=2$ the bounds are roughly **[−276, 492]**. The mean has been dragged from ~30 to 108 and the std inflated to 192 **by the single outlier itself**. With $k=3$ the upper bound exceeds 685 and 500 is comfortably "normal".
>
> **IQR:** $Q_1 \approx 24$, $Q_3 \approx 36.2$, so IQR ≈ 12.2 and bounds are ≈ **[5.7, 54.5]**. 500 is flagged decisively.
>
> ```python
> Q1, Q3 = data_col.quantile(0.25), data_col.quantile(0.75)
> IQR = Q3 - Q1
> lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
> df_housing[(data_col < lower) | (data_col > upper)]
> ```
> **IQR is far more trustworthy.** This is *masking*: the outlier corrupts the very statistics used to detect it, so the σ-method nearly misses it — and would miss it entirely at the standard $k=3$. Quartiles are positional and cannot be moved by one extreme value. That is exactly why the slides had to weaken the rule to $k=2$ to make the demo work at all.

**3.** Explain why `LocalOutlierFactor` can find outliers that neither the σ-method nor IQR can, and write the correct train/test usage.

> [!example]- Solution
> σ and IQR are **univariate** — each examines one column alone. LOF is **multivariate**: it compares each point's local density to its neighbours', so it detects anomalous *combinations* of otherwise ordinary values.
>
> Concretely: `RM = 12` (12 rooms) is large but plausible; `MEDV = 500` is extreme; but a house with 12 rooms priced at 500 *and* `CRIM = 0.9` in a high-tax district forms a combination that exists nowhere else in the data. Only a density method sees it.
>
> ```python
> from sklearn.neighbors import LocalOutlierFactor
>
> lof = LocalOutlierFactor(n_neighbors=20)
>
> # TRAIN: fit_predict, then remove flagged rows
> yhat_train = lof.fit_predict(X_train)
> X_train_clean = X_train[yhat_train != -1]
> y_train_clean = y_train[yhat_train != -1]
>
> # TEST: predict only — do NOT re-fit, do NOT remove
> yhat_test = lof.predict(X_test)
> ```
> Two rules to memorise. **Never `fit` on the combined data before splitting** — the model would learn what "normal" means using test rows, which is leakage. And **never delete outliers from the test set**: the test set simulates production, where you cannot discard awkward inputs. A model evaluated on a sanitised test set reports a score it will never reproduce in reality.
>
> Caveat: `LocalOutlierFactor` needs `novelty=True` at construction for `.predict()` to be available on new data — with the default `novelty=False` only `fit_predict` exists.

**4.** The `horse-colic` data uses `?` for missing values. Load it correctly, then compare `SimpleImputer(strategy='mean')` against `KNNImputer` on `rectal_temp`. When would the difference matter?

> [!example]- Solution
> ```python
> df_horse = pd.read_csv(url, header=None, names=col_names, na_values='?')
> ```
> Without `na_values='?'`, every affected column loads as `object`, `.isnull()` reports zero missing, and both imputers fail on non-numeric input. The chapter's entire premise depends on this one argument.
>
> ```python
> from sklearn.impute import SimpleImputer, KNNImputer
>
> mean_imp = SimpleImputer(strategy='mean')
> knn_imp  = KNNImputer(n_neighbors=5)
>
> a = pd.DataFrame(mean_imp.fit_transform(df_num), columns=df_num.columns)
> b = pd.DataFrame(knn_imp.fit_transform(df_num),  columns=df_num.columns)
> ```
> `SimpleImputer` writes the **same value** into every gap — say 38.2 °C for all missing temperatures. That shrinks the variance and flattens `rectal_temp`'s correlation with `pulse` and `outcome` toward zero, weakening exactly the signal a model needs.
>
> `KNNImputer` finds horses with similar pulse, respiratory rate, and pain, and averages *their* temperatures — so a horse with pulse 164 receives a fever-range estimate rather than the population average. The relationship survives.
>
> **When it matters:** whenever the missing feature is correlated with observed features (usually), and whenever the missingness is not random. In clinical data especially, *the fact that a measurement is missing is itself informative* — a vet skips a reading on an animal too distressed to handle. Consider adding a `was_missing` indicator column alongside the imputed value.
>
> **Critical prerequisite:** KNN uses distances, so features must be **scaled first** or whichever column has the largest units dominates the neighbour search. `hospital_number` in the low hundred-thousands would swamp a temperature around 38. Scaling is [[07 - Data Transformation]].

**5.** (Advanced) The code below reports 95% accuracy but the model performs terribly in production. Identify every leakage bug and rewrite it correctly.
> ```python
> df = pd.read_csv('horse-colic.csv', na_values='?')
> imputer = SimpleImputer(strategy='mean')
> df_imputed = imputer.fit_transform(df)
> lof = LocalOutlierFactor()
> df_clean = df_imputed[lof.fit_predict(df_imputed) != -1]
> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
> model = RandomForestClassifier().fit(X_train, y_train)
> ```

> [!example]- Solution
> **Three leaks, all from the same root cause: preprocessing happens before the split.**
>
> 1. **`imputer.fit_transform(df)` on the full dataset.** The means are computed from training *and* test rows, so every imputed training value carries test information.
> 2. **`lof.fit_predict(df_imputed)` on the full dataset.** The notion of "normal" is learned partly from test rows.
> 3. **Outliers removed from what becomes the test set.** The test set is now easier than reality — the single biggest source of the inflated 95%.
>
> A fourth, subtler bug: the target `outcome` is still inside `df` when the imputer runs, so **missing targets get imputed** rather than dropped. You would be training on invented labels.
>
> **Correct version:**
> ```python
> df = pd.read_csv('horse-colic.csv', header=None, names=col_names, na_values='?')
>
> # Drop rows with a missing TARGET — never impute labels
> df = df.dropna(subset=['outcome'])
> X, y = df.drop('outcome', axis=1), df['outcome']
>
> # SPLIT FIRST — before any learned transformation
> X_train, X_test, y_train, y_test = train_test_split(
>     X, y, test_size=0.3, random_state=42, stratify=y)
>
> # Outlier removal: training set only
> lof = LocalOutlierFactor()
> keep = lof.fit_predict(SimpleImputer(strategy='median').fit_transform(X_train)) != -1
> X_train, y_train = X_train[keep], y_train[keep]
>
> # Everything learned from data goes INSIDE the pipeline
> pipeline = Pipeline([
>     ('imputer', SimpleImputer(strategy='median')),
>     ('model', RandomForestClassifier(random_state=42))
> ])
> pipeline.fit(X_train, y_train)
> accuracy_score(y_test, pipeline.predict(X_test))
> ```
> The honest accuracy will be **noticeably lower**, and that is the point — it is the number that survives contact with production.
>
> Note that outlier removal sits *outside* the pipeline. It cannot go inside: pipelines transform features but cannot drop rows, since that would desynchronise `X` from `y`. Row removal is done manually, on the training set only, after the split.
>
> Two extras worth adopting: `stratify=y` preserves class proportions in both splits, and `random_state=42` makes the result reproducible. Better still, evaluate with `cross_val_score(pipeline, X, y, cv=5)` — cross-validation re-fits the pipeline on each fold, so the leakage protection holds across every split rather than one arbitrary one.

## 📝 Summary

- **Order of operations:** basic cleaning (zero-variance, duplicates) → outliers → missing data → wrap in a Pipeline.
- **Zero-variance features carry no information**; `VarianceThreshold` for numeric, `nunique() == 1` for categorical.
- **Duplicate rows overweight patterns and can leak** across a train/test split.
- **σ-method assumes normality; IQR does not.** IQR is more robust because outliers inflate the mean and std used to detect them.
- **LOF is multivariate** — it catches anomalous *combinations* that no single-column rule can see.
- **Fit outlier detectors and imputers on training data only.** Never remove outliers from the test set: it must mimic production.
- **Four imputation strategies, ascending:** `dropna` → `SimpleImputer` → `KNNImputer` (needs scaled features) → `IterativeImputer` (MICE, experimental).
- **`Pipeline` enforces `fit_transform` on train and `transform` on test automatically** — the whole defence against leakage in one object.

## ⚠️ Important Notes

**Data leakage is the theme of this chapter, not a footnote.** Any step that *learns a parameter from data* — mean, median, scaling range, category list, feature ranking, density model — must be fitted on the training split alone. If your test accuracy looks too good, suspect leakage before celebrating.

**Split before you clean.** The rule is mechanical: `train_test_split` comes first, everything learned comes after.

**Never impute the target variable.** Drop rows with a missing label (`dropna(subset=['outcome'])`). Imputing `y` means training on fabricated answers.

**Outlier ≠ error.** Fraud, equipment failure, and market crashes are outliers *and* the events you most want to model. Investigate before deleting; in fraud or anomaly detection, deleting outliers deletes the entire signal.

**The σ-method suffers from masking.** The outlier inflates the very mean and std used to catch it. In Exercise 2 the 2σ bound reaches 492 against an outlier of 500 — a near miss, and a clean miss at the standard 3σ.

**`VarianceThreshold` is numeric-only** and will error on `object` columns. Use `nunique()` for categoricals.

**Variance is scale-dependent.** A column measured in kilometres has 10⁶× the variance of the same column in millimetres. `threshold > 0` is only meaningful on scaled data — `threshold=0` is safe regardless.

**`KNNImputer` and `LOF` both require scaled features.** They are distance-based, so an unscaled large-magnitude column (an ID, a price in VND) dominates the metric and makes the result meaningless.

**`IterativeImputer` needs `from sklearn.experimental import enable_iterative_imputer` first.** Import it and the class import fails.

**`LocalOutlierFactor` needs `novelty=True` to expose `.predict()`.** With the default, only `fit_predict` exists and the documented test-set workflow will raise `AttributeError`.

**Pipelines cannot drop rows.** They transform features only. Outlier *removal* changes the row count and would desynchronise `X` from `y`, so it must be done manually on the training set, outside the pipeline.

**Missingness itself can be informative.** If values are missing not at random (a test skipped because the patient was too ill), imputation destroys that signal. Add a binary `was_missing` indicator alongside the imputed value.

**Prefer `cross_val_score(pipeline, X, y, cv=5)` over a single split.** One 70/30 split gives one noisy estimate; cross-validation re-fits the pipeline per fold, keeping the leakage guarantee while averaging over the randomness.

> [!warning] Gaps in the source slides
> - **Slide 2** — the Part 1/2/3/4 overview diagram is an image.
> - **Slides 14, 16** — the illustrations of the normal-distribution σ-bands and the IQR/boxplot bounds are images; the formulas above come from the slide text.
> - **Slides 11, 20, 30** reference dataset documentation as "link" with no extractable URL. The data files themselves resolve:
>   - oil-spill: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/oil-spill.csv`
>   - housing: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/housing.csv`
>   - horse-colic: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/horse-colic.csv`
> - **Slide 20** gives the housing column descriptions in **Vietnamese**; they are the standard Boston Housing fields (CRIM = per-capita crime rate, RM = average rooms per dwelling, MEDV = median home value in $1000s, etc.).
> - The slides' source is Jason Brownlee, *Data Preparation for Machine Learning* — one of the four course texts from Lesson 0.

---
**Previous:** [[05 - String Manipulation and Time Series Data]] · **Next:** [[07 - Data Transformation]]
