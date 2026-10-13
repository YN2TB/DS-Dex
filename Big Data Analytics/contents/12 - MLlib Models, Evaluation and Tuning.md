---
subject: Big Data Analytics
chapter: 12
tags: [ds, spark, mllib, regression, glm, elastic-net, classification, trees, evaluation, cross-validation, als, clustering]
source: "Chambers & Zaharia, Spark: The Definitive Guide, ch. 26–29; Karau et al., Learning Spark, ch. 11; user's project notes (note/Project explaination.md)"
---

# MLlib Models, Evaluation and Tuning

## 📘 Main Knowledge

### 1. Parameters in MLlib

DG groups each model's settings into three kinds:
- **model hyperparameters**: the structure of the model (`family`, `elasticNetParam`, `regParam`, `maxDepth`);
- **training parameters**: how training runs (`maxIter`, `tol`, `weightCol`);
- **prediction parameters**: how predictions are made, not affecting training (`threshold`, `thresholds`).

`model.explainParams()` lists them. Default column names: `features`, `label`, `prediction`, `probability`, `rawPrediction`.

**Scalability** (DG Tables 26-1, 27-1): logistic and linear regression handle 1–10 million features; decision trees and GBTs thousands; random forests tens of thousands; generalized linear regression (Spark 2.2) at most **4,096** features. Training examples are effectively unlimited because the optimizers (L-BFGS, SGD, distributed tree building) stream over partitions.

### 2. Linear regression and elastic net

Linear regression assumes the label is a linear combination of features plus Gaussian error. Spark minimizes

$$\frac{1}{2n}\sum_{i=1}^n\left(y_i-x_i^\top\beta\right)^2+\lambda\left[\alpha\|\beta\|_1+\frac{1-\alpha}{2}\|\beta\|_2^2\right]$$

- First term: mean squared error; the ½ cancels the 2 from differentiating.
- `regParam` = $\lambda$: how much to penalize large coefficients (trade-off between fitting the data and keeping coefficients small).
- `elasticNetParam` = $\alpha\in[0,1]$: $\alpha=1$ is pure **lasso** (L1: sets some coefficients exactly to zero, i.e. feature selection), $\alpha=0$ is pure **ridge** (L2: shrinks coefficients but never to zero), in between is elastic net.
- `standardization=True` (default) standardizes features internally so the penalty treats them equally; coefficients are returned on the original scale.

The training summary gives RMSE, $R^2$, residuals and, for the normal-equation solver, p-values (see [[Econometrics/contents/00-Index|Econometrics]]).

### 3. Generalized linear models

`GeneralizedLinearRegression` lets you choose the error distribution (**family**) and the **link** $g$ relating the linear predictor $\eta=x^\top\beta$ to the mean: $g(\mu)=\eta$.

| Family | Response | Links (canonical first) |
|---|---|---|
| Gaussian | continuous | identity, log, inverse |
| Binomial | binary | logit, probit, cloglog |
| Poisson | counts | log, identity, sqrt |
| Gamma | positive continuous | inverse, identity, log |
| Tweedie | zero-inflated continuous | power link |

**Why log is the canonical link for Poisson** (from the user's project notes). Write the pmf in exponential-family form:
$$f(y;\mu)=\frac{e^{-\mu}\mu^y}{y!}\ \Rightarrow\ \log f=y\log\mu-\mu-\log y!,\qquad f(y;\theta,\phi)=\exp\!\left(\frac{y\theta-b(\theta)}{\phi}+c(y,\phi)\right)$$
Matching terms: natural parameter $\theta=\log\mu$, $b(\theta)=e^\theta$, dispersion $\phi=1$. The canonical link is the $g$ with $g(\mu)=\theta$, so $g=\log$. Checks: $b'(\theta)=e^\theta=\mu=E[Y]$ and $b''(\theta)=\mu$, so $\operatorname{Var}(Y)=\mu$. That equality of mean and variance is the real Poisson assumption.

**IRLS** (Spark's `solver="irls"`): with $\mu=e^\eta$, $d\mu/d\eta=\mu$. Each iteration computes weights and a working response
$$W=\frac{(d\mu/d\eta)^2}{\phi V(\mu)}=\mu,\qquad z=\eta+\frac{y-\mu}{\mu}$$
and solves the weighted least squares $(X^\top WX+\lambda I)^{-1}X^\top Wz$. For a canonical link, Fisher scoring equals Newton–Raphson, so it converges in few iterations. The weight $\mu$ means Poisson trusts observations with large means more (coefficient of variation $1/\sqrt\mu$).

If the data are **overdispersed** (variance ≫ mean), Poisson standard errors are too small; consider quasi-Poisson-style corrections, Tweedie, or a negative binomial model outside Spark (added).

### 4. Classification models

| Model | Key points |
|---|---|
| **Logistic regression** | linear model for class probabilities; `family` binomial/multinomial; elastic-net regularization as above; `threshold` (default 0.5) trades false positives vs false negatives; binary summary gives ROC, PR, AUC |
| **Decision tree** | interpretable splits; no scaling needed; overfits easily: control with `maxDepth` (default 5), `maxBins`, `minInstancesPerNode`, `minInfoGain`; `impurity` gini or entropy; `featureImportances` |
| **Random forest** | many trees on bootstrap samples and random feature subsets, averaged; `numTrees`, `featureSubsetStrategy`, `subsamplingRate` |
| **Gradient-boosted trees** | trees trained sequentially to correct previous errors; `maxIter`, `stepSize`; binary labels only in Spark 2.2 |
| **Naive Bayes** | assumes independent features; `modelType` multinomial (counts) or bernoulli (presence); features must be non-negative; `smoothing`; common for text |
| **One-vs-Rest** | wraps a binary classifier for multiclass problems |
| **Multilayer perceptron** | feed-forward neural network (`layers`) |

Regression versions exist for trees, random forests, GBTs, plus isotonic regression and survival regression (AFT).

### 5. Evaluation

| Evaluator | Metrics |
|---|---|
| `BinaryClassificationEvaluator` | `areaUnderROC`, `areaUnderPR` (needs `rawPrediction` or probability scores) |
| `MulticlassClassificationEvaluator` | `f1` (default), `accuracy`, `weightedPrecision`, `weightedRecall` |
| `RegressionEvaluator` | `rmse` (default), `mse`, `r2`, `mae` |
| `ClusteringEvaluator` (2.3+) | silhouette |
| RDD-based `BinaryClassificationMetrics`, `MulticlassMetrics`, `RegressionMetrics`, `RankingMetrics` | detailed metrics (DG: not yet ported to DataFrames in 2.2) |

From a confusion matrix: precision $=TP/(TP+FP)$, recall $=TP/(TP+FN)$, $F_1=2PR/(P+R)$, accuracy $=(TP+TN)/N$. With imbalanced classes prefer PR AUC, F1 or recall at a fixed precision to accuracy.

Note: DG's example sets `rawPredictionCol="prediction"`, i.e. passes hard 0/1 predictions. An ROC curve from hard predictions has a single point, and its AUC equals balanced accuracy $(TPR+TNR)/2$. Pass `rawPrediction` (or probabilities) to get a real AUC.

### 6. Tuning

```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
grid = ParamGridBuilder().addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]).build()
cv = CrossValidator(estimator=pipeline, estimatorParamMaps=grid,
                    evaluator=RegressionEvaluator(metricName="rmse"),
                    numFolds=3, parallelism=4)
cvModel = cv.fit(train)
best = cvModel.bestModel
```

- `TrainValidationSplit`: one split (`trainRatio`, default 0.75); each parameter combination fitted once. Cheaper, noisier.
- `CrossValidator`: $k$ folds; each combination fitted $k$ times; more reliable, $k$ times the cost.
- Both refit the best combination on the full training data at the end.
- Tune the whole pipeline, including preprocessing parameters.
- Keep a separate test set that the tuning never sees.

### 7. Recommendation: ALS

**Alternating least squares** factorizes the user–item rating matrix: each user $u$ and item $i$ get a $k$-dimensional vector (`rank`), and the predicted rating is $\hat r_{ui}=x_u^\top y_i$. ALS alternates between solving for user vectors with item vectors fixed and vice versa (each step is a least-squares problem that parallelizes well).

- Input: `userCol`, `itemCol`, `ratingCol`. **Explicit** ratings (stars) vs **implicit** feedback (`implicitPrefs=True`, `alpha`: views/clicks as confidence).
- Hyperparameters: `rank`, `regParam`, `maxIter`, `numUserBlocks`/`numItemBlocks`.
- **Cold start**: users or items not in training get NaN predictions; `coldStartStrategy="drop"` removes them so RMSE can be computed. ALS also favours popular items; new items get few recommendations.
- `recommendForAllUsers(n)`, `recommendForAllItems(n)`; evaluate with `RegressionEvaluator` (RMSE) or ranking metrics (precision@k, MAP, NDCG).
- Frequent pattern mining: `FPGrowth` for association rules.

### 8. Unsupervised learning

| Model | Idea | Notes |
|---|---|---|
| **k-means** | assign points to the nearest of $k$ centroids, recompute centroids, repeat | choose $k$ (elbow on within-cluster SSE, silhouette); sensitive to initialization (`k-means||` init, several runs) and to scale |
| **Bisecting k-means** | top-down: split clusters repeatedly | often faster, more stable |
| **Gaussian mixture** | each cluster a Gaussian with its own mean and covariance; soft assignments (probabilities) | "soft k-means"; ellipsoid clusters |
| **LDA** | topic model: each document a mixture of topics, each topic a distribution over words | input from `CountVectorizer`; online or EM optimizer; `k` topics, `docConcentration`, `topicConcentration` |

DG's scalability guide: k-means and GMM up to ~50–100 features, LDA thousands of topics.

## ✏️ Exercises

> [!example]- **1.** *(Easy) Classification metrics*
> A model gives TP = 40, FP = 10, FN = 20, TN = 130. Compute precision, recall, F1, accuracy. If you compute AUC from hard 0/1 predictions, what do you get?
>
> ---
> Precision $40/50=0.8$; recall $40/60=0.667$; $F_1=2(0.8)(0.667)/(1.467)=0.727$; accuracy $170/200=0.85$. With hard predictions, TPR = 0.667 and TNR = $130/140=0.929$, so the "AUC" is $(0.667+0.929)/2=0.798$: balanced accuracy, not a real ROC area. Use `rawPrediction`.

> [!example]- **2.** *(Easy–medium) Elastic-net penalty*
> For $\beta=(2,-1,0)$ and $\lambda=0.1$, compute the penalty term $\lambda[\alpha\|\beta\|_1+\frac{1-\alpha}{2}\|\beta\|_2^2]$ for $\alpha=1,\ 0.5,\ 0$. Which setting can make coefficients exactly zero?
>
> ---
> $\|\beta\|_1=3$, $\|\beta\|_2^2=5$. $\alpha=1$: $0.1\times3=0.3$. $\alpha=0.5$: $0.1(1.5+1.25)=0.275$. $\alpha=0$: $0.1\times2.5=0.25$. Any $\alpha>0$ includes the L1 term, which can set coefficients exactly to zero; pure ridge ($\alpha=0$) only shrinks.

> [!example]- **3.** *(Medium) One IRLS step for Poisson*
> A Poisson GLM with log link has $\beta_0=0.5$, $\beta_1=0.2$. For an observation with $x=3$, $y=5$, compute $\eta$, $\mu$, the IRLS weight and working response. Why is the weight equal to $\mu$?
>
> ---
> $\eta=0.5+0.2\times3=1.1$; $\mu=e^{1.1}=3.004$. Weight $W=\mu=3.004$; working response $z=\eta+(y-\mu)/\mu=1.1+1.996/3.004=1.764$. With the canonical log link $d\mu/d\eta=\mu$ and $V(\mu)=\mu$, so $W=\mu^2/\mu=\mu$: observations with larger expected counts get more weight, because under Poisson their relative noise ($1/\sqrt\mu$) is smaller.

> [!example]- **4.** *(Medium–hard) Cost of tuning*
> A grid has 2 formulas × 3 values of `elasticNetParam` × 2 values of `regParam`. How many model fits for `TrainValidationSplit` and for `CrossValidator(numFolds=3)`, counting the final refit? When is the extra cost worth it?
>
> ---
> $2\times3\times2=12$ combinations. TrainValidationSplit: 12 + 1 = 13 fits. CrossValidator: $3\times12+1=37$ fits. Cross-validation is worth it when data is limited or the validation score is noisy (one split could pick a lucky combination); with very large data a single split is usually enough. `parallelism` can fit several models at once.

> [!example]- **5.** *(Hard) Recommendations with ALS*
> (a) A user vector is (1.2, 0.5) and an item vector (2.0, −1.0); what rating does ALS predict? (b) Your test RMSE is NaN. Why, and how do you fix it? (c) The site only has view counts, not ratings. What changes?
>
> ---
> (a) $1.2\times2.0+0.5\times(-1.0)=1.9$.
> (b) Some test users or items were not in the training data, so their predictions are NaN, and RMSE over NaN is NaN. Set `coldStartStrategy="drop"` (and handle new users separately, e.g. popular items or content-based features).
> (c) Use implicit feedback: `implicitPrefs=True`, treating views as confidence (`alpha` controls how fast confidence grows with counts). Evaluate with ranking metrics (precision@k, MAP) rather than RMSE on the counts.

## 📝 Summary

- Parameters: model hyperparameters, training parameters, prediction parameters; check scalability limits (GLR ≤ 4,096 features in Spark 2.2).
- Linear regression with elastic net: MSE/2 + $\lambda[\alpha L_1+\frac{1-\alpha}{2}L_2^2]$; `regParam` = λ, `elasticNetParam` = α (1 lasso, 0 ridge).
- GLMs: family + link; canonical links (Poisson–log, binomial–logit); Poisson assumes Var = mean; IRLS with weight μ and working response $\eta+(y-\mu)/\mu$.
- Classifiers: logistic regression, decision tree, random forest, GBT, naive Bayes, one-vs-rest, MLP.
- Evaluators: binary (AUC ROC/PR, needs scores), multiclass (F1, accuracy), regression (RMSE, R², MAE).
- Tuning: ParamGridBuilder + TrainValidationSplit (cheap) or CrossValidator ($k$× cost); tune the whole pipeline.
- ALS for recommendations (rank, regParam, implicit prefs, cold start); k-means, bisecting k-means, GMM, LDA for unsupervised tasks.

## ⚠️ Important Notes

1. AUC needs scores (`rawPrediction`/probability), not hard predictions.
2. Accuracy is misleading on imbalanced classes.
3. `elasticNetParam=0` is ridge, `=1` is lasso; `regParam=0` means no regularization at all.
4. Poisson regression assumes variance = mean; check for overdispersion.
5. Generalized linear regression in Spark 2.2 accepts at most 4,096 features.
6. Decision trees overfit without depth or node-size limits.
7. GBTs in Spark 2.2 support only binary classification.
8. Naive Bayes requires non-negative features.
9. ALS gives NaN for unseen users/items unless `coldStartStrategy="drop"`.
10. k-means depends on feature scale and initialization; scale features first.
11. Tuning on the test set makes the reported score optimistic.

> [!warning] Gaps in the source material
> - The elastic-net objective, the Poisson exponential-family derivation and IRLS follow the user's project notes; DG describes the parameters but not the mathematics.
> - **Added by me:** the AUC-from-hard-predictions point, overdispersion remedies, `ClusteringEvaluator`, ranking metrics, `parallelism` in tuning, all exercises.
> - DG ch. 28's ALS code and ch. 29's clustering outputs are not reproduced (outputs depend on random initialization).

**Previous:** [[11 - MLlib Pipelines and Feature Engineering]] · **Next:** end of subject (see [[00-Index]])
