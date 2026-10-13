---
subject: Data Preparation and Visualization
chapter: 07
tags: [ds, feature-engineering, scaling, encoding, scikit-learn, preprocessing]
source: "Lesson_7_Data_Transform.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Transformation

[[06 - Data Cleaning]] made the data correct; this chapter makes it usable by models. Every tool here is a scikit-learn transformer and belongs inside a pipeline ([[09 - Building Pipelines]]).

## 📘 Main Knowledge

### Why transform

- **Data types**: models need numbers, not `'Red'` or `'Vietnam'` → encoding.
- **Scale**: SVM, KNN and linear models depend on distances or coefficients, so income (~50,000) drowns years of experience (~5) → scaling.
- **Distribution**: linear models work best with roughly Gaussian data → power/quantile transforms.

### Part I: Scaling and encoding

#### Scaling numeric data

**`MinMaxScaler`** (normalization) to a fixed range, usually [0, 1]:
$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$
For algorithms without distribution assumptions (KNN) and image data. Very sensitive to outliers: one extreme value sets $X_{max}$ and squeezes everything else.

**`StandardScaler`** (standardization) to mean 0, standard deviation 1:
$$X_{scaled} = \frac{X - \mu}{\sigma}$$
The default; suits models assuming Gaussian data (linear, logistic regression). It does not change the shape: a skewed variable stays skewed.

**`RobustScaler`** uses the median and IQR:
$$X_{scaled} = \frac{X - Q_2(X)}{Q_3(X) - Q_1(X)}$$
For data with many outliers; median and IQR are not dragged by extremes.

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
scaled = StandardScaler().fit_transform(data.reshape(-1, 1))   # sklearn expects 2-D input
```

| Scaler | Best for | Result |
|---|---|---|
| `MinMaxScaler` | data without outliers, KNN | fixed range |
| `StandardScaler` | general use, linear models | mean 0, std 1 |
| `RobustScaler` | data with outliers | centred on the median, scaled by IQR |

> [!warning] Fit on training data only
> Fit the scaler on the training set, then transform train and test. Fitting on everything leaks the test set's min, max, mean and variance.

#### Encoding categorical data

- **Ordinal** categories have an order: Small < Medium < Large.
- **Nominal** categories do not: USA, Japan, Vietnam.

**`OrdinalEncoder`**: one integer per category.
```python
from sklearn.preprocessing import OrdinalEncoder
df_sizes = pd.DataFrame({'size': ['S', 'M', 'L', 'XL', 'M', 'S']})
encoder = OrdinalEncoder(categories=[['S', 'M', 'L', 'XL']])   # give the order explicitly
encoded = encoder.fit_transform(df_sizes[['size']])
```
Only for ordinal data. On nominal data (USA → 0, Japan → 1, Vietnam → 2) it invents an order and distances that linear models will use.

**`OneHotEncoder`**: one 0/1 column per category.
```python
from sklearn.preprocessing import OneHotEncoder
encoded = OneHotEncoder(sparse_output=False).fit_transform(df_colors[['color']])
```
For nominal data. High-cardinality columns explode the number of features (10,000 product IDs → 10,000 columns).

### Part II: Distribution and other transforms

#### Power transforms

Apply a function (log, square root, …) to make a skewed variable more Gaussian; λ is chosen automatically (by maximum likelihood).

$$X^{(\lambda)} = \begin{cases}\dfrac{X^{\lambda} - 1}{\lambda} & \lambda \neq 0\\[4pt] \ln X & \lambda = 0\end{cases}\qquad\text{(Box-Cox)}$$

- **Box-Cox**: requires $X>0$.
- **Yeo-Johnson**: handles negative, zero and positive values; often the better default.

```python
from sklearn.preprocessing import PowerTransformer
pt_boxcox = PowerTransformer(method='box-cox', standardize=False)
pt_yj = PowerTransformer(method='yeo-johnson', standardize=True)
transformed = pt_yj.fit_transform(data.reshape(-1, 1))
```

#### `QuantileTransformer`

Maps values to their ranks, then to a target distribution (`output_distribution='uniform'` or `'normal'`). For complex, multimodal or outlier-heavy data that power transforms cannot fix; also spreads clumped points for KNN. Rank-based, so original distances are lost.

```python
from sklearn.preprocessing import QuantileTransformer
normal_data = QuantileTransformer(output_distribution='normal', n_quantiles=100).fit_transform(bimodal_data)
```

#### Discretization: `KBinsDiscretizer`

Turns a continuous feature into bins (age 25 → "20–30") so a linear model can fit non-linear effects (one coefficient per bin).

| Strategy | Bins | Use when |
|---|---|---|
| `'uniform'` | equal width | the value has linear meaning |
| `'quantile'` | equal frequency | skewed data; ensures data in every bin |
| `'kmeans'` | 1-D k-means clusters | natural clusters exist |

```python
from sklearn.preprocessing import KBinsDiscretizer
disc = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
```

#### `PolynomialFeatures`

Creates powers and products: from $a, b$ it adds $a^2$, $b^2$, $ab$, so a linear model can learn non-linear relationships and interactions.

| Parameter | Role |
|---|---|
| `degree` | polynomial degree |
| `interaction_only` | only cross terms ($ab$) |
| `include_bias` | add a column of ones |

```python
from sklearn.preprocessing import PolynomialFeatures
X_poly = PolynomialFeatures(degree=2, include_bias=False).fit_transform(X_simple)
```

The number of features grows fast; keep degree 2–3 and scale first.

#### Transforming the target

Regression targets (prices, revenue, counts) are often right-skewed.
- `np.log1p` computes $\log(1+y)$ and handles zeros.
- Box-Cox (positive $y$) or Yeo-Johnson (any sign).

After predicting, apply the inverse transform before reporting (`log1p` ↔ `expm1`). `TransformedTargetRegressor` does this automatically:

```python
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
ttr = TransformedTargetRegressor(regressor=LinearRegression(), func=np.log1p, inverse_func=np.expm1)
ttr.fit(X_train, y_train)
y_pred = ttr.predict(X_test)     # in original units
```

## ✏️ Exercises

The slides pose eight discussion questions without answers; the exercises below answer them (my reconstructions).

**1.** (Slide 8) Under `MinMaxScaler`, what happens to test values outside the training [min, max]? (Slide 10) Does `StandardScaler` make skewed data normal?

> [!example]- Solution
> The scaler uses the training min and max, so out-of-range test values map below 0 or above 1. It neither errors nor refits (refitting would leak). Use `clip=True` if a bounded range is required.
>
> No: $(X-\mu)/\sigma$ is linear, so it shifts and stretches but keeps skewness and kurtosis. Changing shape needs a non-linear transform (`PowerTransformer`, `QuantileTransformer`). Scaling changes units; power transforms change shape.

**2.** (Slides 12–13) Compare the three scalers on `[10, 12, 11, 13, 12, 1000]`. Which would you choose?

> [!example]- Solution
> - MinMax: range 990; the five normal values become 0, 0.002, 0.001, 0.003, 0.002 and the outlier 1. The real data is squeezed into 0.3% of the range.
> - Standard: mean 176.33, (population) σ 368.36; normal values ≈ −0.45, outlier ≈ 2.24. The mean lies far outside the actual data.
> - Robust: median 12, $Q_1$ 11.25, $Q_3$ 12.75, IQR 1.5; values −1.33, 0, −0.67, 0.67, 0, and the outlier 658.7. The normal points are spread out and the outlier stands apart.
>
> Choose `RobustScaler`. Max, mean and std are corrupted by the outlier; median and IQR are not. No scaler removes outliers; that happens in cleaning, first.

**3.** (Slide 16) Without `categories`, how does `OrdinalEncoder` number categories? (Slide 17) `pd.get_dummies` or `OneHotEncoder`?

> [!example]- Solution
> Alphabetically: `['S','M','L','XL']` → L 0, M 1, S 2, XL 3, so Large < Medium < Small, with no warning. Always pass `categories=`.
>
> Use `OneHotEncoder` for modelling. `get_dummies` builds columns from whatever data it sees, so train (red, green, blue) and test (red, blue) get different shapes. `OneHotEncoder` learns categories at `fit`, handles unseen ones (`handle_unknown='ignore'`), and works in pipelines.
> ```python
> OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first')
> ```
> `drop='first'` avoids the dummy-variable trap (perfect collinearity) for linear models ([[Econometrics/contents/00-Index|Econometrics]]); trees don't need it.

**4.** (Slides 20–21) The target contains zeros and negatives and Box-Cox fails. What now? (Slide 31) Scale before `PolynomialFeatures`?

> [!example]- Solution
> Box-Cox needs $X>0$ (it uses $X^\lambda$ and $\ln X$).
> - Yeo-Johnson: built for any sign; use it when negatives are genuine (profit/loss, returns).
> - Shift then transform, e.g. `np.log1p` for counts where 0 means "none"; invert with `np.expm1`. Shifting is arbitrary (it changes λ), so prefer Yeo-Johnson without a domain reason.
>
> Yes, scale first: squaring amplifies scale differences (income² ~ 2.5×10⁹ vs experience² ~ 25), which hurts optimization and makes regularization uneven.
> ```python
> Pipeline([('scaler', StandardScaler()),
>           ('poly', PolynomialFeatures(degree=2, include_bias=False)),
>           ('model', Ridge())])
> ```
> A second scaler after `poly` is common.

**5.** (Advanced, slide 28) How do you choose `n_bins`? Build a preprocessing pipeline for mixed numeric and categorical columns and explain why `ColumnTransformer` is needed.

> [!example]- Solution
> `n_bins` is a bias–variance trade-off: too few bins lose signal, too many leave too little data per bin. Start with 5–10, keep enough observations per bin (`strategy='quantile'` helps), and tune by cross-validation (`GridSearchCV(pipe, {'disc__n_bins': [3, 5, 10, 20]}, cv=5)`). Prefer meaningful cut-offs (age thresholds, tax brackets) when they exist.
>
> Numeric and categorical columns need different steps, and a plain `Pipeline` applies each step to all columns.
> ```python
> from sklearn.compose import ColumnTransformer
> numeric_pipe = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
> categorical_pipe = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')),
>                              ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])
> preprocessor = ColumnTransformer([('num', numeric_pipe, ['age', 'income', 'bmi']),
>                                   ('cat', categorical_pipe, ['country', 'occupation'])])
> full_pipeline = Pipeline([('preprocess', preprocessor), ('model', RandomForestClassifier(random_state=42))])
> full_pipeline.fit(X_train, y_train)
> ```
> Medians, means, standard deviations and category lists are all learned from `X_train` only. More in [[09 - Building Pipelines]].

## 📝 Summary

- Scaling changes units; power transforms change shape.
- MinMax (fixed range, outlier-sensitive), Standard (default), Robust (outliers).
- Fit on train only, transform both.
- `OrdinalEncoder` for ordered categories (always pass `categories`), `OneHotEncoder` for nominal ones.
- Box-Cox needs positive data; Yeo-Johnson handles any sign; `QuantileTransformer` for messy distributions but loses structure.
- `KBinsDiscretizer` (uniform, quantile, kmeans) and `PolynomialFeatures` let linear models capture non-linearity.
- Transform skewed targets and always invert predictions (`TransformedTargetRegressor`; `log1p` ↔ `expm1`).

## ⚠️ Important Notes

1. `StandardScaler` does not make data normal.
2. `MinMaxScaler` can output values outside [0, 1] on test data; `clip=True` if needed.
3. `OrdinalEncoder` defaults to alphabetical order.
4. Do not ordinal-encode nominal data for linear or distance-based models.
5. Prefer `OneHotEncoder` to `get_dummies` for models; use `handle_unknown='ignore'`.
6. `drop='first'` for linear models (dummy-variable trap).
7. Box-Cox fails on zeros and negatives.
8. `log1p` inverts with `expm1`, not `exp`; mixing them shifts predictions by 1.
9. Scale before `PolynomialFeatures`.
10. Polynomial features grow fast: 60 features at degree 2 give 1,891 columns including the bias column; degree 3 about 39,700.
11. `QuantileTransformer` needs `n_quantiles` ≤ number of samples.
12. Compute metrics (RMSE) in original units after inverting the target transform.
13. Use `ColumnTransformer` for mixed column types.

> [!warning] Gaps in the source slides
> - Slides 3 and 5 (overview diagrams) are images.
> - Slides 25, 29, 32 (Labs 4–6 on the Sonar dataset) have titles only.
> - Slides 8, 10, 12, 16, 17, 21, 28, 31 pose unanswered questions; answered above as reconstructions.
> - Slides 21 and 24 end with "What?", apparently pointing at plots that did not extract.
> - Datasets: Diabetes (`load_diabetes`, 442 patients, 10 features), Breast Cancer and Sonar (UCI).
> - Exercise 2 corrected (2026-10-09): `StandardScaler` uses the population σ (368.36), giving ≈ −0.45 and 2.24; `RobustScaler` maps 11 to −0.67.

**Previous:** [[06 - Data Cleaning]] · **Next:** [[08 - Feature Selection]]
