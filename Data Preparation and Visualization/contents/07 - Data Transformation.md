---
subject: Data Preparation and Visualization
chapter: 07
tags: [ds, feature-engineering, scaling, encoding, scikit-learn, preprocessing]
source: "Lesson_7_Data_Transform.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Transformation

> [!note] Where this sits in the course
> Core of **Part 2 — Becoming a Data Architect**. [[06 - Data Cleaning]] made the data *correct*; this chapter makes it *digestible* — reshaping values so the model can actually use them. Everything here is a scikit-learn transformer, and every one of them must live inside a Pipeline ([[09 - Building Pipelines]]) to avoid leakage.

## 📘 Main Knowledge

### Why transform at all

Four distinct reasons, each producing a different tool:

- **Data types** — algorithms require numbers, not `'Red'` or `'Vietnam'`. → *Encoding*
- **Scale sensitivity** — SVM, KNN, and linear regression are distance- or coefficient-based, so a feature measured in tens of thousands drowns one measured in single digits. *Income (50,000) vs. Years of Experience (5)* — the model effectively ignores experience. → *Scaling*
- **Distribution assumptions** — linear models perform best on roughly Gaussian data. → *Power/quantile transforms*
- **Model expectations** generally — raw data rarely suits any algorithm as-is.

---

## Part I — Feature transformation

### Scaling numerical data

**1. `MinMaxScaler` (Normalisation)** — squeeze into a fixed range, usually $[0,1]$:

$$X_{scaled} = \frac{X - X_{min}}{X_{max} - X_{min}}$$

*Use for:* algorithms with no distributional assumptions (KNN), image data (pixels 0–255).
**Major drawback: extremely sensitive to outliers.** One extreme value defines $X_{max}$ and crushes every other point into a sliver of the range.

**2. `StandardScaler` (Standardisation)** — centre at 0 with unit variance:

$$X_{scaled} = \frac{X - \mu}{\sigma}$$

*Use for:* the **default choice**; anything assuming Gaussian data (linear and logistic regression).
**It does not change the shape of the distribution** — only its centre and spread. A skewed distribution stays exactly as skewed afterwards.

**3. `RobustScaler`** — use order statistics instead of moments:

$$X_{scaled} = \frac{X - Q_2(X)}{Q_3(X) - Q_1(X)}$$

*Use for:* data with **many outliers**. Median and IQR cannot be dragged by extremes, so the bulk of the data is scaled sensibly regardless — the same robustness argument as the IQR outlier rule in [[06 - Data Cleaning]].

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

data_reshaped = data.reshape(-1, 1)   # sklearn wants a 2-D column vector
scaler = StandardScaler()
scaled = scaler.fit_transform(data_reshaped)
```

| Scaler | Best for | Characteristic |
|---|---|---|
| `MinMaxScaler` | Data without outliers, KNN | Fixed range, e.g. $[0,1]$ |
| `StandardScaler` | Most general cases, linear models | mean = 0, std = 1 |
| `RobustScaler` | Data with outliers | Median and IQR — outlier-resistant |

> [!warning] The Golden Rule
> **ALWAYS fit the scaler on the training data only**, then use it to transform both train and test. **Never fit on the full dataset.** Fitting on everything leaks the test set's min, max, mean, and variance into training — see [[06 - Data Cleaning]] and [[09 - Building Pipelines]].

### Encoding categorical data

Models need numbers. **Which encoder you use depends on whether the categories have an order.**

- **Ordinal** — meaningful order: `Small < Medium < Large`
- **Nominal** — no intrinsic order: `USA`, `Japan`, `Vietnam`

**`OrdinalEncoder`** — one integer per category (`'S'→0, 'M'→1, 'L'→2`):

```python
from sklearn.preprocessing import OrdinalEncoder

df_sizes = pd.DataFrame({'size': ['S', 'M', 'L', 'XL', 'M', 'S']})
size_order = ['S', 'M', 'L', 'XL']          # declare the order explicitly
encoder = OrdinalEncoder(categories=[size_order])
encoded = encoder.fit_transform(df_sizes[['size']])
```

**Use only on ordinal data.** Applying it to nominal data invents a false ordering — encoding `USA→0, Japan→1, Vietnam→2` tells the model that Japan sits *between* the USA and Vietnam, and that `Vietnam - USA = 2`. Both are meaningless, and a linear model will act on them.

**`OneHotEncoder`** — one binary column per category:

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)   # False → dense numpy array
encoded = encoder.fit_transform(df_colors[['color']])
```

**Use on nominal data.** No false order is created. **Drawback:** high-cardinality features explode the column count — 10,000 product IDs become 10,000 columns. That is the *curse of dimensionality*.

---

## Part II — Distribution and other transforms

### Power transforms

Apply a mathematical function (log, square root, …) to make a skewed distribution more Gaussian. The algorithm **automatically finds the optimal $\lambda$**, usually by maximum likelihood, such that the transformed variable is as normal as possible.

- **Box-Cox** — very effective, but requires **strictly positive** data ($X > 0$).
- **Yeo-Johnson** — generalises Box-Cox to handle negative, zero, and positive values. **Often the better default.**

$$
X^{(\lambda)} = \begin{cases}
\dfrac{X^{\lambda} - 1}{\lambda} & \lambda \neq 0 \\[6pt]
\ln(X) & \lambda = 0
\end{cases}
\qquad \text{(Box-Cox)}
$$

```python
from sklearn.preprocessing import PowerTransformer

pt_boxcox = PowerTransformer(method='box-cox', standardize=False)
pt_yj     = PowerTransformer(method='yeo-johnson', standardize=True)
transformed = pt_yj.fit_transform(data.reshape(-1, 1))
```

### `QuantileTransformer`

Maps values onto their **ranks**, then onto a target distribution:

- `output_distribution='uniform'` → uniform on $[0,1]$
- `output_distribution='normal'` → Gaussian

*Use when:* the distribution is complex, unclear, multi-modal, or so outlier-heavy that a power transform cannot fix it. Also useful for distance-based models like KNN, since it spreads clumped points apart.

**Warning:** it is a rank-based transform, so it **discards information about the original distribution's structure** — distances between points are no longer proportional to their original differences.

```python
from sklearn.preprocessing import QuantileTransformer

qt_normal = QuantileTransformer(output_distribution='normal', n_quantiles=100)
normal_data = qt_normal.fit_transform(bimodal_data)
```

### Discretisation — `KBinsDiscretizer`

Converts a continuous feature into bins (age 25 → bin "20–30"). **Why:** it lets a *linear* model capture non-linear effects, because each bin gets its own coefficient.

Three strategies:

| Strategy | How bins are chosen | Use when |
|---|---|---|
| `'uniform'` | Equal **width** — 0–100 in 5 bins → [0,20], (20,40], … | The value has linear significance |
| `'quantile'` | Equal **frequency** — each bin holds ~the same count | Data is skewed; guarantees enough data per bin |
| `'kmeans'` | 1-D K-Means finds natural clusters | The data has genuine cluster structure |

```python
from sklearn.preprocessing import KBinsDiscretizer

disc = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='quantile')
```

### `PolynomialFeatures`

Builds new features from products and powers of existing ones — from $a, b$ it creates $a^2$, $b^2$, $ab$. This lets a **linear model learn non-linear relationships and interactions**.

| Parameter | Role |
|---|---|
| `degree` | Polynomial degree. Higher → far more features |
| `interaction_only` | `True` → only cross terms ($ab$), no powers ($a^2$) |
| `include_bias` | `True` → adds a constant column of ones |

```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_simple)
```

**Warning:** feature count grows combinatorially — high degrees cause overfitting and heavy computation. **Stick to degree 2 or 3.** And **scale before this step**: squaring an unscaled feature squares its scale problem too.

### Transforming the target variable

In regression the target itself (house price, revenue, counts) is often right-skewed, which violates linear-model assumptions and produces poor predictions.

Common choices:

- **`np.log1p`** — computes $\log(1+y)$; preferred over plain `log` because it **handles zeros**. Excellent for right-skewed positive targets.
- **Box-Cox** — finds optimal $\lambda$ automatically; requires positive $y$.
- **Yeo-Johnson** — the generalisation; handles negative, zero, and positive.

> [!warning] The critical step
> After predicting, you **must apply the inverse transformation** to return to original units. Predicting $\log(\text{price})$ and reporting the raw output means reporting a logarithm as though it were dollars.
> `log(price)` → `exp(prediction)`

`TransformedTargetRegressor` automates this safely:

```python
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression

ttr = TransformedTargetRegressor(
    regressor=LinearRegression(),
    func=np.log1p,          # forward
    inverse_func=np.expm1   # inverse — note expm1 pairs with log1p
)
ttr.fit(X_train, y_train)
y_pred = ttr.predict(X_test)   # already back in original units
```

## ✏️ Exercises

The slides pose eight discussion questions without written answers. Exercises 1–3 answer the most important of them.

**1.** *(Slide 8)* What happens if the test set contains values outside the training set's `[min, max]` range under `MinMaxScaler`? *(Slide 10)* Does `StandardScaler` make a skewed distribution normal?

> [!example]- Solution
> **MinMax out-of-range:** the scaler stores the *training* min and max and applies the same formula regardless, so test values simply **fall outside $[0,1]$**. A test value above the training max maps above 1; below the training min maps below 0. It does **not** error and it does **not** re-scale.
>
> That is the correct behaviour — re-fitting on test data would be leakage — but it breaks anything assuming a bounded range (image pipelines, some neural network activations). Options: `clip=True` to clamp into range, or use `StandardScaler`, which has no bounds to violate.
>
> **StandardScaler and skew: no.** It computes $(X-\mu)/\sigma$ — a *linear* transformation. Linear maps shift and stretch a distribution but cannot change its shape: skewness and kurtosis are unchanged. A right-skewed variable is exactly as right-skewed after standardising, now centred at 0.
>
> To actually change shape you need a **non-linear** transform: `PowerTransformer` or `QuantileTransformer`. This distinction — *scaling changes units, power transforms change shape* — is the cleanest one-line summary of Part I vs Part II.

**2.** *(Slide 12)* Compare all three scalers on `[10, 12, 11, 13, 12, 1000]`. *(Slide 13)* Which would you choose?

> [!example]- Solution
> ```python
> data = np.array([10, 12, 11, 13, 12, 1000]).reshape(-1, 1)
> ```
> **MinMaxScaler** — range is 1000−10 = 990, so the five genuine values map to 0, 0.002, 0.001, 0.003, 0.002, and the outlier to 1.0. **The real data is crushed into the first 0.3% of the range** and becomes indistinguishable. Catastrophic.
>
> **StandardScaler** — mean ≈ 176.3, std ≈ 403. The normal values land around −0.41 and the outlier at ≈ 2.04. Better, but the mean (176) sits far outside the actual data range, and everything real is packed near −0.41.
>
> **RobustScaler** — median = 12, $Q_1$ = 11.25, $Q_3$ = 12.75, IQR = 1.5. Values become −1.33, 0, −0.5, 0.67, 0, and the outlier ≈ 658.7. **The five real points are now properly spread out**, and the outlier is left conspicuously far away — visible rather than dominant.
>
> **Choose `RobustScaler`.** The lesson generalises: MinMax and Standard both compute statistics that the outlier itself corrupts (max, mean, std), while median and IQR are positional and immune. Note that no scaler *removes* the outlier — that is [[06 - Data Cleaning]]'s job, and it should happen first.

**3.** *(Slide 16)* If you do not pass `categories` to `OrdinalEncoder`, how does sklearn assign numbers? *(Slide 17)* Should you use `pd.get_dummies` or `OneHotEncoder`?

> [!example]- Solution
> **Ordinal default: alphabetical (lexicographic) order.** For `['S','M','L','XL']` sklearn sorts to `['L','M','S','XL']` and assigns `L→0, M→1, S→2, XL→3`.
>
> That encodes **Large < Medium < Small**, which is backwards. The encoder ran without warning and produced numbers that look perfectly reasonable. **Always pass `categories=[...]` explicitly** — this is the highest-value habit in the chapter.
>
> **`get_dummies` vs `OneHotEncoder`: use `OneHotEncoder` for modelling.** `pd.get_dummies` is fine for exploration but has a disqualifying flaw: it **derives its columns from whatever data it sees**. If the training set contains `['red','green','blue']` and the test set only `['red','blue']`, you get 3 columns from train and 2 from test — the model receives the wrong shape and crashes, or worse, silently misaligns.
>
> `OneHotEncoder` **learns the category list at `fit` time** and reproduces it exactly at `transform` time, so train and test always agree. It also handles unseen categories (`handle_unknown='ignore'`) and slots into a `Pipeline`. `get_dummies` can do none of this.
>
> ```python
> OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop='first')
> ```
> `drop='first'` removes one column per feature to avoid the **dummy variable trap** — perfect multicollinearity, since the dropped category is implied by all others being 0. Required for linear models, unnecessary for trees. See [[Econometrics/contents/00-Index|Econometrics]].

**4.** *(Slides 20–21)* Your target variable contains zeros and negatives. Box-Cox raises an error. Give two ways to proceed, and explain when each is appropriate. *(Slide 31)* Should you scale before `PolynomialFeatures`?

> [!example]- Solution
> **Box-Cox requires strictly positive input** because it computes $X^\lambda$ and, at $\lambda = 0$, $\ln(X)$ — both undefined for $X \le 0$.
>
> **Option A — use Yeo-Johnson.** It is built for exactly this, applying different formulas on each side of zero. Preferred when negatives are *genuine* (temperature changes, profit/loss, returns).
> ```python
> PowerTransformer(method='yeo-johnson')
> ```
>
> **Option B — shift then Box-Cox:** add a constant so the minimum exceeds 0. Only defensible when values are conceptually positive and zeros mean "none" (counts, spend). `np.log1p` is the standard version of this trick, computing $\log(1+y)$ so that $y=0 \mapsto 0$. Its inverse is `np.expm1`, **not** `np.exp`.
>
> Shifting is arbitrary — the constant changes the fitted $\lambda$ — so **prefer Yeo-Johnson** unless you have a domain reason.
>
> **Scaling before `PolynomialFeatures`: yes, and it is not optional.** Squaring amplifies scale disparity quadratically. With income ~50,000 and experience ~5, the squared terms are ~2.5×10⁹ versus ~25 — a ratio of 10⁸. The interaction term sits somewhere between. Gradient descent cannot converge across that range, and regularisation (which penalises coefficients uniformly) becomes meaningless.
>
> ```python
> Pipeline([('scaler', StandardScaler()),
>           ('poly', PolynomialFeatures(degree=2, include_bias=False)),
>           ('model', Ridge())])
> ```
> Scale → expand → model. Note the polynomial output is itself unscaled, so a second `StandardScaler` after `poly` is common in practice.

**5.** (Advanced) *(Slide 28)* How should you choose `n_bins` for `KBinsDiscretizer`? Then build a complete preprocessing pipeline for a dataset with mixed numeric and categorical columns, and explain why `ColumnTransformer` is required.

> [!example]- Solution
> **Choosing `n_bins` is a bias–variance trade-off.** Too few bins discards real signal (2 bins turn a rich variable into a coin flip); too many leave each bin with too little data to estimate reliably, and at the limit you have recreated the continuous variable with added noise.
>
> Practical guidance: start at **5–10**; ensure each bin holds enough observations (a common floor is ~30, or ≥5% of the data); use `strategy='quantile'` to guarantee this automatically on skewed data; and **tune it with cross-validation** rather than guessing — `n_bins` is a hyperparameter like any other:
> ```python
> GridSearchCV(pipe, {'disc__n_bins': [3, 5, 10, 20]}, cv=5)
> ```
> Prefer domain-meaningful cuts when they exist (legal age thresholds, tax brackets) — an interpretable bin beats a marginally better score.
>
> **Why `ColumnTransformer`:** numeric and categorical columns need *different* treatment. Scaling a one-hot column is pointless; one-hot encoding a float is nonsense. A plain `Pipeline` applies each step to **all** columns, so it cannot express "scale these, encode those."
>
> ```python
> from sklearn.compose import ColumnTransformer
> from sklearn.pipeline import Pipeline
> from sklearn.impute import SimpleImputer
> from sklearn.preprocessing import StandardScaler, OneHotEncoder
>
> numeric_features = ['age', 'income', 'bmi']
> categorical_features = ['country', 'occupation']
>
> numeric_pipe = Pipeline([
>     ('imputer', SimpleImputer(strategy='median')),
>     ('scaler', StandardScaler())
> ])
>
> categorical_pipe = Pipeline([
>     ('imputer', SimpleImputer(strategy='most_frequent')),
>     ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
> ])
>
> preprocessor = ColumnTransformer([
>     ('num', numeric_pipe, numeric_features),
>     ('cat', categorical_pipe, categorical_features)
> ])
>
> full_pipeline = Pipeline([
>     ('preprocess', preprocessor),
>     ('model', RandomForestClassifier(random_state=42))
> ])
> full_pipeline.fit(X_train, y_train)
> ```
> Three details that matter. Each branch imputes with an appropriate strategy — `median` for numbers, `most_frequent` for categories (`mean` is undefined on text). `handle_unknown='ignore'` prevents a crash when the test set contains a category absent from training. And **every statistic — medians, means, standard deviations, category lists — is learned from `X_train` alone**, then replayed on test data. That is the leakage guarantee, and getting it by construction is why this structure is the standard.
>
> Nested pipelines are covered fully in [[09 - Building Pipelines]].

## 📝 Summary

- **Scaling changes units; power transforms change shape.** `StandardScaler` cannot fix skew — it is a linear map.
- **Three scalers:** `MinMaxScaler` (fixed range, outlier-fragile), `StandardScaler` (μ=0, σ=1, the default), `RobustScaler` (median/IQR, for outlier-heavy data).
- **Golden Rule: fit on train only, transform both.** Fitting on the full dataset leaks.
- **Encoding follows the data type:** `OrdinalEncoder` for ordered categories (**always pass `categories=`**), `OneHotEncoder` for unordered ones.
- **Ordinal encoding of nominal data invents a false order** the model will act on.
- **One-hot on high-cardinality features explodes dimensionality.**
- **Box-Cox needs strictly positive data; Yeo-Johnson handles any sign** — the better default. `QuantileTransformer` handles distributions too messy for either, at the cost of discarding structure.
- **`KBinsDiscretizer`** lets linear models capture non-linearity: `uniform` (equal width), `quantile` (equal frequency), `kmeans` (natural clusters).
- **`PolynomialFeatures` adds interactions** — scale first, keep `degree` at 2–3.
- **Transform a skewed target too, and always invert the prediction.** `TransformedTargetRegressor` does it for you; pair `log1p` with `expm1`.

## ⚠️ Important Notes

**`StandardScaler` does not normalise a distribution.** It standardises *location and scale*. Skew survives untouched. Exam-favourite distinction.

**`MinMaxScaler` on test data can produce values outside `[0,1]`.** Correct behaviour, but it breaks bounded-range assumptions. Use `clip=True` if that matters.

**`OrdinalEncoder` defaults to alphabetical order.** `['S','M','L','XL']` becomes `L=0, M=1, S=2, XL=3` — Large ranked below Small, silently. Always pass `categories=[...]`.

**Never apply `OrdinalEncoder` to nominal data.** `USA=0, Japan=1, Vietnam=2` implies Japan lies between the other two and that the difference is meaningful. Tree models tolerate it; linear and distance-based models do not.

**Prefer `OneHotEncoder` over `pd.get_dummies` for modelling.** `get_dummies` produces different columns for different inputs, so train and test can disagree in shape. `OneHotEncoder` locks the category list at `fit`.

**Use `handle_unknown='ignore'`** or a category appearing only in production will raise at `transform` time.

**`drop='first'` for linear models** — otherwise the one-hot columns are perfectly collinear (the dummy variable trap). Unnecessary for tree ensembles.

**Box-Cox fails on zero or negative values.** Use Yeo-Johnson, or `log1p` for count-like data.

**`np.log1p` inverts with `np.expm1`, not `np.exp`.** Mismatching them shifts every prediction by 1 — a bug that produces plausible-looking wrong numbers.

**Scale before `PolynomialFeatures`.** Squaring amplifies scale differences quadratically; degree-2 on unscaled features can span 10⁸.

**`PolynomialFeatures` grows combinatorially.** 60 features at degree 2 → 1,891 columns; at degree 3 → ~39,000. Overfitting and memory both bite. Degree 2–3.

**`QuantileTransformer` destroys distributional structure.** It is rank-based, so relative distances are lost and the result is not interpretable in original units. It also needs enough samples — `n_quantiles` should not exceed the sample count.

**A transformed target must be inverted before reporting or scoring.** RMSE computed on log-scale predictions is not RMSE in dollars, and the error is easy to miss because the number looks reasonable. `TransformedTargetRegressor` prevents it structurally.

**Use `ColumnTransformer` whenever columns are of mixed type.** A plain `Pipeline` applies every step to every column.

> [!warning] Gaps in the source slides
> - **Slides 3, 5** — the "Overview of Data Transform" and "Overview of Data Variable Types" diagrams are images with no extractable text.
> - **Slides 25, 29, 32** (Labs #4, #5, #6, all on the Sonar dataset) contain **only a title** — the task descriptions are images or were never written out. Their content is unknown.
> - **Slides 8, 10, 12, 16, 17, 21, 28, 31** each pose a **"Question:"** the slide text never answers — these are the lecturer's in-class discussion prompts. I have answered the eight of them in Exercises 1–5 above; treat my answers as reconstructions, not as the lecturer's, and check them against your lecture notes since they are strongly exam-flavoured.
> - **Slide 21** ends with a bare "`What?`" and **slide 24** likewise — apparently pointing at an image of transformed-distribution plots that did not extract.
>
> Datasets referenced (all resolvable):
> - Diabetes — `sklearn.datasets.load_diabetes` (442 patients, 10 physiological features)
> - Breast Cancer — `https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer/breast-cancer.data`
> - Sonar — `https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data`

---
**Previous:** [[06 - Data Cleaning]] · **Next:** [[08 - Feature Selection]]
