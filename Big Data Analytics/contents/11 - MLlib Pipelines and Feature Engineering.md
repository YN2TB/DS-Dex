---
subject: Big Data Analytics
chapter: 11
tags: [ds, spark, mllib, pipelines, feature-engineering, scaling, encoding, pca]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 24–25; Karau et al., Learning Spark, ch. 11; user's project notes (note/Project explaination.md)"
---

# MLlib Pipelines and Feature Engineering

## 📘 Main Knowledge

### 1. MLlib and when to use it

MLlib is Spark's machine learning library: preprocessing, feature engineering, supervised and unsupervised models, tuning and evaluation, all running distributed. Two packages:
- `pyspark.ml`: the DataFrame-based API with pipelines (use this);
- `pyspark.mllib`: the older RDD-based API (maintenance mode), still home to some tools such as `RowMatrix.computeSVD`.

Use MLlib when the data is too large for one machine, or to preprocess at scale and produce features for single-node libraries. For small data, scikit-learn on one machine is often simpler and faster. DG also points out that Spark is not a low-latency serving system.

Typical workflow (DG Figure 24-2): gather data → clean and inspect → feature engineering → train models (train/validation split) → evaluate and select → use the model (batch scoring, export, or streaming).

### 2. Structural types

| Type | What it does | Example |
|---|---|---|
| **Transformer** | DataFrame → DataFrame, no learning | `Tokenizer`, `VectorAssembler`, a fitted model |
| **Estimator** | learns from data with `fit()` and returns a transformer (a "Model") | `StandardScaler` (learns means/stds), `StringIndexer`, `LogisticRegression` |
| **Evaluator** | computes a metric on predictions | `BinaryClassificationEvaluator`, `RegressionEvaluator` |
| **Pipeline** | a sequence of stages (transformers and estimators); itself an estimator | `Pipeline(stages=[rForm, lr])` |

Fitting a pipeline fits each estimator in order on the training data and returns a `PipelineModel`; calling `transform` on new data applies exactly the same steps. This prevents **leakage**: scaling statistics, category indexes and vocabularies are learned from training data only.

**Vectors.** Models take features as one vector column of doubles:
```python
from pyspark.ml.linalg import Vectors
denseVec = Vectors.dense(1.0, 2.0, 3.0)
sparseVec = Vectors.sparse(3, [1, 2], [2.0, 3.0])   # size, indices, values
```
Sparse vectors (printed `(size,[indices],[values])`) store only non-zeros; use them when most entries are zero (one-hot, text). `pyspark.ml.linalg` and `pyspark.mllib.linalg` vectors are different types.

### 3. An end-to-end pipeline (DG ch. 24)

```python
from pyspark.ml.feature import RFormula
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml.evaluation import BinaryClassificationEvaluator

train, test = df.randomSplit([0.7, 0.3])
rForm = RFormula()
lr = LogisticRegression().setLabelCol("label").setFeaturesCol("features")
pipeline = Pipeline().setStages([rForm, lr])
params = ParamGridBuilder() \
    .addGrid(rForm.formula, ["lab ~ . + color:value1", "lab ~ . + color:value1 + color:value2"]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
    .addGrid(lr.regParam, [0.1, 2.0]).build()
evaluator = BinaryClassificationEvaluator().setMetricName("areaUnderROC") \
    .setRawPredictionCol("prediction").setLabelCol("label")
tvs = TrainValidationSplit().setTrainRatio(0.75) \
    .setEstimatorParamMaps(params).setEstimator(pipeline).setEvaluator(evaluator)
tvsFitted = tvs.fit(train)
evaluator.evaluate(tvsFitted.transform(test))      # DG prints 0.9166666666666667
tvsFitted.write().overwrite().save("/tmp/modelLocation")
```

The grid has $2\times3\times2=12$ combinations; hyperparameters of preprocessing stages (here the formula) can be tuned along with the model. Load a saved model with the matching model class (`TrainValidationSplitModel.load`, `PipelineModel.load`). Tuning and evaluation are covered in [[12 - MLlib Models, Evaluation and Tuning]].

**RFormula** builds the label and feature vector from an R-style formula: `~` separates label and terms, `+` adds terms, `-` removes, `:` interaction, `.` all other columns, `+ 0` / `- 1` removes the intercept. String columns are one-hot encoded automatically; **numeric columns are just cast to double**, so a numerically coded category is treated as ordered (DG's warning).

**Deployment patterns** (DG): batch scoring of stored data with Spark; precompute results into a key-value store (works for recommendations, not for arbitrary inputs); persist the model and serve it elsewhere (Spark has high startup overhead for single requests); convert to a portable format (e.g. PMML/MLeap); apply models to streams with Structured Streaming.

### 4. Continuous features (DG ch. 25)

| Transformer | Result |
|---|---|
| `Bucketizer(splits=[...])` | fixed bins; splits must cover the data range (use `float("-inf")`, `float("inf")`); `handleInvalid` = keep/skip/error for null/NaN |
| `QuantileDiscretizer(numBuckets=5)` | bins at approximate quantiles (`relativeError`) |
| `StandardScaler` | divides by the (sample) standard deviation; **`withMean=False` by default**, so it does not center unless asked |
| `MinMaxScaler(min, max)` | rescales each component to [min, max] (default [0, 1]) |
| `MaxAbsScaler` | divides by the max absolute value → [−1, 1]; keeps zeros and sparsity |
| `ElementwiseProduct` | multiplies each component by a fixed vector |
| `Normalizer(p)` | scales each **row** vector to unit $p$-norm (p = 1 Manhattan, 2 Euclidean) |

DG's `StandardScaler` output on `[1.0, 0.1, −1.0]` is `[1.1952, 0.02338, −0.5976]`: each value divided by its column's sample standard deviation (0.8367, 4.2778, 1.6733), with no centering (verified in exercise 2).

**Centering sparse vectors is expensive**: subtracting the mean turns every zero into a non-zero, so a sparse vector becomes dense (DG's warning). This is the issue in the user's project: after one-hot encoding, `withMean=True` would blow up memory, while `withStd=True` alone keeps zeros as zeros.

**Choosing a scaler** (from the user's project): with a heavy-tailed variable (one flight delayed 1,000 minutes), min-max squashes all normal values near 0, because one extreme value sets the range; standardization is affected less. A signed log transform, $\operatorname{sign}(x)\log(1+|x|)$, reduces skew while keeping the sign of negative values (early arrivals).

### 5. Categorical features

- `StringIndexer`: maps strings to indices by frequency (most frequent → 0.0). `handleInvalid="skip"`/`"keep"` for labels unseen in training (default: error). `IndexToString` maps back (e.g. predictions to labels).
- `VectorIndexer`: marks vector components with few distinct values as categorical (for tree models).
- `OneHotEncoder`: index → sparse 0/1 vector. By default it **drops the last category** (`dropLast=True`), so $k$ categories give vectors of size $k-1$; the last category is the all-zero vector. DG's output: green (index 1) → `(2,[1],[1.0])`, blue (index 2) → `(2,[],[])`. Dropping one avoids perfect collinearity with the intercept.
- In Spark 3, `OneHotEncoder` is an estimator and handles several columns at once.

### 6. Text features

| Step | Tool |
|---|---|
| split into words | `Tokenizer` (whitespace, lower-case), `RegexTokenizer` (pattern) |
| drop common words | `StopWordsRemover` (built-in lists per language) |
| word combinations | `NGram(n=2)` |
| count words | `CountVectorizer` (learns a vocabulary; `minTF`, `minDF`, `vocabSize`, `binary`) or `HashingTF` (hashes words into `numFeatures` buckets: no vocabulary to store, but collisions and no way back to the word) |
| down-weight common terms | `IDF` (estimator; `minDocFreq`) after TF: TF–IDF |
| dense embeddings | `Word2Vec` (skip-gram; similar words get nearby vectors) |

### 7. Feature manipulation and selection

- `VectorAssembler`: concatenates numeric, boolean and vector columns into one feature vector; used in almost every pipeline. `[1, 2, 3]` → `[1.0, 2.0, 3.0]`.
- `PCA(k)`: projects features onto the top $k$ principal components (fewer, uncorrelated features; less interpretable).
- `Interaction`, `PolynomialExpansion(degree)`: create interaction and power terms. The number of outputs grows quickly: $\binom{n+d}{d}-1$ for $n$ features and degree $d$ (5 for $n=2,d=2$; 19 for $n=3,d=3$).
- `ChiSqSelector`: keeps features most dependent on a categorical label by the χ² test (`numTopFeatures`, `percentile`, `fpr`).
- Custom transformers can be written by subclassing `Transformer`.

**PCA on a distributed matrix** (user's project): `RowMatrix(rdd_of_vectors).computeSVD(k)` (from `pyspark.mllib`) computes the top singular vectors without collecting the data. In mode `"dist-eigs"` it repeatedly multiplies by $A^\top A$ across partitions (an iterative eigen-solver, like power iteration) until the vectors converge or the iteration limit is reached. The share of variance kept by $k$ components is
$$\frac{\lambda_1+\dots+\lambda_k}{\sum_j\lambda_j}$$
(eigenvalues of the covariance matrix = squared singular values of the centered data divided by $n-1$).

## ✏️ Exercises

> [!example]- **1.** *(Easy) Read vectors*
> (a) Write `(5,[1,3],[2.0,4.0])` as a dense vector. (b) A column `color` has values red (most frequent), green, blue. What do `StringIndexer` and `OneHotEncoder` (default settings) produce for each?
>
> ---
> (a) `[0.0, 2.0, 0.0, 4.0, 0.0]`.
> (b) Indices by frequency: red 0.0, then green and blue 1.0 and 2.0 (in DG's data green = 1.0, blue = 2.0). One-hot with `dropLast=True` gives size-2 vectors: red `(2,[0],[1.0])`, green `(2,[1],[1.0])`, blue `(2,[],[])`.

> [!example]- **2.** *(Easy–medium) Reproduce DG's StandardScaler*
> Assume the scaling data are the five vectors [1, 0.1, −1], [2, 1.1, 1], [1, 0.1, −1], [2, 1.1, 1], [3, 10.1, 3]. Compute each column's sample standard deviation and the scaled first and last rows. What does the result tell you about `withMean`?
>
> ---
> Column 1: mean 1.8, squared deviations sum 2.8, $s=\sqrt{2.8/4}=0.8367$. Column 2: mean 2.5, sum 73.2, $s=\sqrt{18.3}=4.2778$. Column 3: mean 0.6, sum 11.2, $s=1.6733$.
>
> First row: $[1/0.8367, 0.1/4.2778, -1/1.6733]=[1.1952, 0.02338, -0.5976]$. Last row: $[3.5857, 2.3610, 1.7928]$. These match DG's printed output exactly, so the values were divided by the sample standard deviation and **not centered**: `withMean` is false by default.

> [!example]- **3.** *(Medium) Why not center sparse features?*
> 1 million rows, a one-hot feature vector of length 10,000 with 10 non-zeros per row. Estimate memory for sparse storage (4-byte index + 8-byte value per non-zero) and after `withMean=True` makes the vectors dense (8 bytes per entry).
>
> ---
> Sparse: $10^6\times10\times12$ bytes = 120 MB. Dense: $10^6\times10{,}000\times8$ bytes = 80 GB, about 667× more. Dividing by the standard deviation keeps zeros at zero, so `withStd=True, withMean=False` preserves sparsity; for centering, use `MaxAbsScaler` or center only dense numeric columns.

> [!example]- **4.** *(Medium–hard) Min-max, standardize or log?*
> Delays (minutes): 5, 10, 15, 20, 1000. Compute min-max scaled values, z-scores (sample sd) and the signed log $\operatorname{sign}(x)\log(1+|x|)$. Which keeps normal flights distinguishable?
>
> ---
> Min-max: $(x-5)/995$ → 0, 0.0050, 0.0101, 0.0151, 1: the four normal flights are squeezed into 1.5% of the range.
>
> Z-scores: mean 210, $s=441.66$ → −0.464, −0.453, −0.442, −0.430, 1.789: still compressed, but the scale is not set by the single extreme value alone.
>
> Signed log: 1.792, 2.398, 2.773, 3.045, 6.909: normal flights are well separated and the outlier is pulled in. For heavy tails, log first, then standardize; the sign factor keeps negative delays (early arrivals) negative.

> [!example]- **5.** *(Hard) PCA and feature explosion*
> (a) A covariance matrix has eigenvalues 4.0, 2.5, 1.0, 0.3, 0.2. How many components keep at least 90% of the variance? (b) How many features does `PolynomialExpansion(degree=2)` create from 2 inputs, and degree 3 from 3 inputs? (c) Why should scaling and PCA be inside the pipeline rather than fitted on all data before splitting?
>
> ---
> (a) Cumulative shares: 0.500, 0.8125, 0.9375, 0.975, 1. Three components keep 93.75%.
>
> (b) $\binom{n+d}{d}-1$: $\binom{4}{2}-1=5$ ($x_1, x_1^2, x_2, x_1x_2, x_2^2$) and $\binom{6}{3}-1=19$. (DG says 4 and 27; see errata.)
>
> (c) Means, standard deviations and principal components fitted on all data use information from the test set (leakage), so test scores look better than real performance. Inside a pipeline they are fitted on the training data only and then applied unchanged to validation/test data.

## 📝 Summary

- Use `pyspark.ml` (DataFrame API). Transformers transform; estimators `fit` and return models; evaluators score; pipelines chain stages and prevent leakage.
- Features go into one vector column (dense or sparse); `VectorAssembler` builds it; `RFormula` does indexing, encoding and assembling from a formula.
- Continuous: Bucketizer, QuantileDiscretizer, StandardScaler (no centering by default, sample sd), MinMaxScaler, MaxAbsScaler, Normalizer (per row).
- Categorical: StringIndexer (by frequency, `handleInvalid`), OneHotEncoder (drops the last category), VectorIndexer.
- Text: Tokenizer, StopWordsRemover, NGram, CountVectorizer/HashingTF + IDF, Word2Vec.
- Selection/manipulation: PCA, interactions, polynomial expansion ($\binom{n+d}{d}-1$ features), ChiSqSelector.
- Centering sparse vectors densifies them; log-transform heavy tails before scaling; `computeSVD` does distributed PCA.

## ⚠️ Important Notes

1. Fit preprocessing inside the pipeline on training data only.
2. `StandardScaler` does not center by default.
3. `withMean=True` on sparse one-hot vectors can explode memory.
4. `OneHotEncoder` drops the last category by default; that category is the zero vector.
5. `StringIndexer` fails on unseen labels unless `handleInvalid` is set.
6. Numeric codes treated as numbers imply an order; cast to string before indexing if the categories are unordered.
7. `HashingTF` collisions map different words to the same feature; increase `numFeatures` (a power of 2).
8. `Normalizer` scales rows, scalers scale columns.
9. Min-max scaling is very sensitive to outliers.
10. Spark models are not built for low-latency single-request serving.

> [!warning] Gaps in the source material
> - **Errata in DG** (logged in [[00-Index]]): E6 the PolynomialExpansion feature counts (says 4 for 2 inputs at degree 2 and 27 for 3 inputs at degree 3; correct 5 and 19).
> - DG's scaling dataset is loaded from a file and not printed in full; exercise 2 assumes the five rows shown, which reproduce all printed outputs exactly.
> - **Added by me:** the min-max/log example, memory estimate for densified vectors, explained-variance example, `MaxAbsScaler` as a centering alternative, Spark 3 changes, and the `computeSVD` explanation (following the user's project notes).
> - DG's evaluator uses `rawPredictionCol="prediction"` (hard 0/1 predictions), which makes AUC less informative; see [[12 - MLlib Models, Evaluation and Tuning]].

**Previous:** [[10 - Workflow Orchestration with Airflow]] · **Next:** [[12 - MLlib Models, Evaluation and Tuning]]
