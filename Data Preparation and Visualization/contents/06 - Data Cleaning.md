---
subject: Data Preparation and Visualization
chapter: 06
tags: [ds, data-cleaning, outliers, imputation, scikit-learn, data-leakage]
source: "Lesson_6_Data Cleaning.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Cleaning

First chapter of Part 2 (Becoming a Data Architect). From here the target is an ML model, the library is scikit-learn, and each step is judged by whether it helps the model without leaking information.

## 📘 Main Knowledge

### Why cleaning matters

"Garbage in, garbage out": models learn whatever patterns the data contains, so data quality caps performance. Clean data gives better accuracy, more robust models and fewer training errors.

Recommended order (the lesson's four parts): basic cleaning → outliers → missing data → pipelines.

### Part 1: Basic cleaning

#### Zero-variance features

A constant column has
$$\operatorname{Var}(X) = \frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2 = 0$$
and carries no information.

```python
from sklearn.feature_selection import VarianceThreshold
transformer = VarianceThreshold(threshold=0)
data_transformed = transformer.fit_transform(df_oil)
retained_cols = transformer.get_feature_names_out(input_features=df_oil.columns)
data_cleaned = pd.DataFrame(data_transformed, columns=retained_cols)
```

`VarianceThreshold` works on numeric data only; `threshold > 0` also removes near-constant features. For categorical columns:

```python
df_oil.drop(columns=df_oil.columns[df_oil.nunique() == 1])
```

#### Duplicate rows

Duplicates overweight their pattern and, if copies land in both train and test, leak (the model is tested on rows it saw).

```python
df_oil.duplicated().sum()
df_oil.drop_duplicates()
```

### Part 2: Outliers

Observations very different from the rest, from measurement errors, data-entry mistakes, or genuinely rare events. They distort statistics and model parameters. Rare events are often the target (fraud), so investigate before deleting.

**Method 1: standard deviation** (assumes roughly normal data)
$$\text{lower} = \mu - k\sigma,\qquad \text{upper} = \mu + k\sigma$$
$k=3$ is common (≈99.7% of a normal distribution); the slides use $k=2$ for a small demo.

```python
data_col = df_housing['MEDV']
mean, std = data_col.mean(), data_col.std()
lower, upper = mean - 2 * std, mean + 2 * std
outliers = df_housing[(data_col < lower) | (data_col > upper)]
data_cleaned_outlier = df_housing[(data_col >= lower) & (data_col <= upper)]
```

**Method 2: interquartile range** (no distribution assumption)
$$\text{IQR} = Q_3 - Q_1,\qquad \text{lower} = Q_1 - 1.5\,\text{IQR},\qquad \text{upper} = Q_3 + 1.5\,\text{IQR}$$

```python
Q1, Q3 = data_col.quantile(0.25), data_col.quantile(0.75)
IQR = Q3 - Q1
outliers_iqr = df_housing[(data_col < Q1 - 1.5 * IQR) | (data_col > Q3 + 1.5 * IQR)]
```

IQR is more robust: an outlier pulls the mean toward it and inflates σ, widening the bounds meant to catch it (masking). Quartiles cannot be moved by one extreme value. The same rule draws boxplot whiskers ([[10 - Visualization with Matplotlib and Seaborn]]).

**Method 3: Local Outlier Factor (LOF)**. σ and IQR are univariate. LOF is multivariate: it flags points whose local density is much lower than their neighbours'. A 200 m² house and a \$50,000 price are each ordinary; a 200 m² house at \$50,000 is not.

```python
from sklearn.neighbors import LocalOutlierFactor
lof = LocalOutlierFactor()
yhat = lof.fit_predict(df_housing)     # 1 = inlier, −1 = outlier
df_housing[yhat != -1]
```

| Parameter | Default | Role |
|---|---|---|
| `n_neighbors` | 20 | neighbours for the density estimate (main knob) |
| `contamination` | `'auto'` | expected share of outliers; sets the threshold |

> [!warning] Train/test usage
> - Training data: `lof.fit_predict(X_train)`, then remove flagged rows.
> - Test data: predict only (`lof.predict(X_test)`, needs `novelty=True`); do not refit and do not remove test outliers.
> - Never fit on the combined data before splitting (leakage).
>
> The test set represents production, where you cannot delete awkward rows.

### Part 3: Missing data

Most ML algorithms fail on `NaN`. The demo data uses `?`:

```python
df_horse = pd.read_csv(io.StringIO(csv_horse), na_values='?')
```

**1. Removal**: `df_horse.dropna()`. Quick, but can lose much data and bias the sample if values are not missing at random.

**2. Statistical imputation**
```python
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')       # 'median', 'most_frequent', 'constant' (+ fill_value)
data_imputed_mean = imputer.fit_transform(df_horse)
```
`'median'` suits skewed data; `'most_frequent'` is the only option for categorical columns.

**3. KNN imputation** (multivariate: average the value over the $k$ most similar rows)
```python
from sklearn.impute import KNNImputer
knn_imputer = KNNImputer(n_neighbors=2, weights='uniform')   # default k=5; 'distance' weights nearer rows more
data_imputed_knn = knn_imputer.fit_transform(df_horse)
```
Preserves relationships between features, but needs scaled features.

**4. Iterative imputation (MICE)**: regress each incomplete feature on the others, repeatedly, until values stabilize.
```python
from sklearn.experimental import enable_iterative_imputer   # required
from sklearn.impute import IterativeImputer
iter_imputer = IterativeImputer(max_iter=10, random_state=0)  # estimator=BayesianRidge() by default
data_imputed_iter = iter_imputer.fit_transform(df_horse)
```
Still experimental in scikit-learn.

### Part 4: Pipelines against leakage

**Data leakage** = using information from outside the training set to build the model. Typical case: compute the imputation mean on the whole dataset, then split. The same applies to scaling, encoding, feature selection and outlier removal: any step that learns parameters from data.

A `Pipeline` chains transformers and a final estimator and applies `fit_transform` on training data and `transform` on test data automatically.

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df_clean = df_lab3.dropna(subset=['outcome'])          # never impute the target
X, y = df_clean.drop('outcome', axis=1), df_clean['outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')),
                     ('model', RandomForestClassifier(random_state=42))])
pipeline.fit(X_train, y_train)          # imputer.fit_transform(X_train), then model.fit
y_pred = pipeline.predict(X_test)       # imputer.transform(X_test) with training medians
accuracy_score(y_test, y_pred)
```

More in [[09 - Building Pipelines]]; random forests in [[Machine Learning/contents/00-Index|Machine Learning]].

## ✏️ Exercises

**1.** Which columns/rows should go, and why? Write code to remove them.
> ```python
> csv_data = '''f_1,f_2,f_3,f_4,f_5
> 1,25.4,3.8,0,10
> 2,22.3,4.1,0,12
> 3,26.1,3.7,0,10
> 4,24.8,3.9,0,11
> 2,22.3,4.1,0,12'''
> ```

> [!example]- Solution
> `f_4` is constant (variance 0); row 5 duplicates row 2.
> ```python
> df_oil = pd.read_csv(io.StringIO(csv_data))
> df_oil.duplicated().sum()        # 1
> df_oil = df_oil.drop_duplicates()
> df_oil = df_oil.drop(columns=df_oil.columns[df_oil.nunique() == 1])
> ```
> Drop duplicates first (removing rows can create a new constant column). `nunique()` also works for categorical columns. `f_1` looks like an ID (1, 2, 3, 4); no automatic check flags it, but it should not go into a model.

**2.** For `MEDV` = 24, 21.6, 34.7, 33.4, 36.2, 500, compute the 2σ bounds and the IQR bounds (pandas defaults). Which flags 500?

> [!example]- Solution
> σ-method: mean 108.32, sample sd 191.98, bounds [−275.6, 492.3]. 500 is barely outside; with $k=3$ the upper bound is 684.3 and 500 passes as normal. The outlier itself pulled the mean from about 30 to 108 and inflated σ.
>
> IQR: $Q_1=26.35$, $Q_3=35.825$ (linear interpolation), IQR = 9.475, bounds [12.14, 50.04]. 500 is flagged clearly.
>
> IQR is more trustworthy here: the σ-method suffers from masking.

**3.** Why can LOF find outliers that σ and IQR miss? Write the correct train/test usage.

> [!example]- Solution
> σ and IQR check one column at a time; LOF compares local densities in the full feature space, so it detects unusual combinations of ordinary values (e.g. many rooms, very high price, low crime in a high-tax district).
> ```python
> lof = LocalOutlierFactor(n_neighbors=20, novelty=True)
> lof.fit(X_train)
> keep = lof.predict(X_train) != -1
> X_train_clean, y_train_clean = X_train[keep], y_train[keep]
> yhat_test = lof.predict(X_test)      # inspect only; do not drop test rows
> ```
> (With the default `novelty=False`, only `fit_predict` on the training data is available.) Never fit on combined data; never clean the test set.

**4.** `horse-colic` uses `?` for missing values. Load it correctly and compare `SimpleImputer(mean)` with `KNNImputer` on `rectal_temp`.

> [!example]- Solution
> ```python
> df_horse = pd.read_csv(url, header=None, names=col_names, na_values='?')
> a = SimpleImputer(strategy='mean').fit_transform(df_num)
> b = KNNImputer(n_neighbors=5).fit_transform(df_num)
> ```
> Without `na_values='?'` the columns load as `object` and `isnull()` finds nothing.
>
> The mean imputer puts the same value in every gap, shrinking variance and weakening correlations with `pulse` and `outcome`. KNN uses similar horses (pulse, respiration, pain), so a horse with a very high pulse gets a fever-range temperature. The difference matters when the missing feature correlates with observed ones and when missingness is informative (a vet skips a reading on a distressed animal); add a `was_missing` indicator. KNN needs scaled features, or large-unit columns like `hospital_number` dominate the distance ([[07 - Data Transformation]]).

**5.** (Advanced) This code reports 95% accuracy but fails in production. Find the leaks and fix it.
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
> 1. The imputer is fitted on all rows (test means leak into training values).
> 2. LOF learns "normal" from all rows.
> 3. Outliers are removed from what becomes the test set, making it easier than reality.
> 4. The target `outcome` is still in `df`, so missing labels get imputed.
>
> ```python
> df = pd.read_csv('horse-colic.csv', header=None, names=col_names, na_values='?')
> df = df.dropna(subset=['outcome'])
> X, y = df.drop('outcome', axis=1), df['outcome']
> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
>                                                     random_state=42, stratify=y)
> keep = LocalOutlierFactor().fit_predict(
>     SimpleImputer(strategy='median').fit_transform(X_train)) != -1
> X_train, y_train = X_train[keep], y_train[keep]
> pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')),
>                      ('model', RandomForestClassifier(random_state=42))])
> pipeline.fit(X_train, y_train)
> accuracy_score(y_test, pipeline.predict(X_test))
> ```
> Outlier removal stays outside the pipeline: pipelines cannot drop rows without desynchronizing `X` and `y`. Expect a lower, honest accuracy. `cross_val_score(pipeline, X, y, cv=5)` gives a steadier estimate.

## 📝 Summary

- Order: zero-variance and duplicates → outliers → missing data → pipeline.
- `VarianceThreshold` (numeric) or `nunique() == 1` (categorical) for constant columns; duplicates overweight patterns and can leak.
- σ-method assumes normality and suffers from masking; IQR is robust; LOF finds multivariate outliers.
- Fit detectors and imputers on training data only; never clean the test set.
- Imputation: `dropna` → `SimpleImputer` → `KNNImputer` (scale first) → `IterativeImputer` (MICE).
- Pipelines apply `fit_transform` to train and `transform` to test automatically.

## ⚠️ Important Notes

1. Every step that learns from data must be fitted on the training split only; suspiciously high test accuracy often means leakage.
2. Split before cleaning.
3. Never impute the target; drop rows with missing labels.
4. An outlier is not necessarily an error.
5. `VarianceThreshold` errors on `object` columns.
6. Variance depends on units, so `threshold > 0` only makes sense on scaled data.
7. `KNNImputer` and LOF need scaled features.
8. `IterativeImputer` requires `enable_iterative_imputer` to be imported first.
9. `LocalOutlierFactor` needs `novelty=True` for `.predict()`.
10. Pipelines cannot remove rows.
11. Missingness can be informative; add a `was_missing` indicator.

> [!warning] Gaps in the source slides
> - Slide 2 (overview diagram) and slides 14, 16 (σ-band and IQR illustrations) are images.
> - Slides 11, 20, 30 link to dataset docs without URLs; the data files are at `https://raw.githubusercontent.com/jbrownlee/Datasets/master/` (`oil-spill.csv`, `housing.csv`, `horse-colic.csv`).
> - Slide 20 gives Boston Housing field names in Vietnamese (CRIM = crime rate, RM = rooms, MEDV = median value in \$1000s).
> - Source: Brownlee, *Data Preparation for Machine Learning*.
> - Exercise 2 corrected (2026-10-09): an earlier version gave approximate quartiles (24, 36.2); pandas' default interpolation gives 26.35 and 35.825.

**Previous:** [[05 - String Manipulation and Time Series Data]] · **Next:** [[07 - Data Transformation]]
