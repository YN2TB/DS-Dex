---
subject: Time-series Analysis
chapter: 02
tags: [ds, time-series, moving-average, exponential-smoothing, holt-winters, ets, decomposition]
source: "Lecture_2_DSEB.ipynb — Tran Thi Ha, Faculty of Mathematical Economics, NEU (2025)"
---

# Estimating Trend and Decomposing Time Series

> [!note] Where this sits in the course
> [[01 - What is a Time Series]] named the four components; this lecture **estimates** them. The methods here are **descriptive and smoothing-based** — no probability model yet. That arrives with [[03 - Stationarity and Difference Equations]] and the ARMA family.

> **Lecture outline:**
> - **Estimating the trend component** (moving averages, smoothing methods)
> - **Decomposing a time series** into systematic components (trend, seasonal, irregular)
> - **Additive and multiplicative** decomposition frameworks
> - **Adjusting seasonal effects** to reveal underlying patterns
>
> *Understanding structure before forecasting and modeling.*

## 📘 Main Knowledge

---

## Part 1 — Moving Averages

> **Moving averages** are commonly used to **smooth** a time series by reducing short-run fluctuations and highlighting the underlying movement of the data.

### Simple Moving Average (SMA)

$$y^{MA(3)}_t = \frac{1}{3}\left(y_t + y_{t-1} + y_{t-2}\right)$$

> This is a **one-sided moving average**, since it uses only current and past values. As a result, **the first two observations cannot be computed**.
>
> The smoothed series can be interpreted as a **local approximation of the trend**, but it does **not** remove the trend in a strict econometric sense. Moving averages are mainly used for **exploratory analysis and visualization**.

**The caveat matters.** Smoothing makes a trend *visible*; it does not make the series stationary. Detrending in the econometric sense requires differencing — [[03 - Stationarity and Difference Equations]].

### Centered Moving Average (CMA)

$$y^{CMA(3)}_t = \frac{1}{3}\left(y_{t-1} + y_t + y_{t+1}\right)$$

> This symmetric window provides a **better local approximation** of the underlying trend, **but it cannot be used for real-time forecasting.**

General form with window $2m+1$:
$$y^{MA}_t = \frac{1}{2m+1}\sum_{j=-m}^{m} y_{t+j}$$

**The trade-off is fundamental: one-sided averages are usable in real time but lag the series; centered averages track it faithfully but require future data.** A centred average is fine for *describing* history and useless for *forecasting*.

### Weighted Moving Average (WMA)

$$y^{WMA(5)}_t = \frac{1}{10}\left(y_{t-2} + 2y_{t-1} + 4y_t + 2y_{t+1} + y_{t+2}\right)$$

Larger weights on observations closer to $t$. Note the weights sum to 10, matching the divisor — **weights must sum to 1 or the smoothed series is biased in level**.

> **Rule of thumb:** increasing the window size produces a **smoother** series, but results in **greater data loss at the boundaries**.

### Double Moving Average

> If the series exhibits a **linear trend**, the double moving average can be used for forecasting.

$$Y_t^{MA(k)(2)} = \frac{Y_t^{MA(k)} + Y_{t-1}^{MA(k)} + \cdots + Y_{t-k+1}^{MA(k)}}{k}$$

> This series has **no values for the first $2k$ observations.**

**Trend estimate:**
$$\hat{b}_n = \frac{2\left(Y_n^{MA(k)} - Y_n^{MA(k)(2)}\right)}{k-1}$$

**Forecast:**
$$\hat{Y}_{n+h} = Y_n^{MA(k)} + \frac{2\left(Y_n^{MA(k)} - Y_n^{MA(k)(2)}\right)}{k-1}\,h$$

**Why double smoothing works.** A single moving average applied to a linearly trending series **lags behind it** by a predictable amount. Applying the average twice lags again by the same amount, so the *gap between the two* measures the lag — and hence the slope. The formula simply rescales that gap into a slope estimate.

---

## Part 2 — Exponential Smoothing

### Simple Exponential Smoothing (SES)

> **SES** smooths a series by assigning **exponentially decreasing weights** to past observations:
> $$\hat{y}_t = \alpha y_t + (1-\alpha)\hat{y}_{t-1}, \qquad 0 < \alpha < 1$$
>
> The current smoothed value is a **weighted average** of the current observation and the previous smoothed value. **Recent observations receive higher weights; older observations lower weights.**
>
> A **larger $\alpha$** makes the series respond more quickly to new data; a **smaller $\alpha$** produces a smoother series.

**The recursive derivation** — the lecture shows why the recursion is equivalent to an infinite weighted sum. Start from the expanded form:
$$\hat{Y}_t = \alpha Y_t + \alpha(1-\alpha)Y_{t-1} + \alpha(1-\alpha)^2 Y_{t-2} + \cdots = \alpha\sum_{i=0}^{\infty}(1-\alpha)^i Y_{t-i}$$

Multiply the lagged version by $(1-\alpha)$:
$$(1-\alpha)\hat{Y}_{t-1} = \alpha(1-\alpha)Y_{t-1} + \alpha(1-\alpha)^2 Y_{t-2} + \alpha(1-\alpha)^3 Y_{t-3} + \cdots$$

**Subtracting**, every term beyond the first cancels:
$$\hat{Y}_t - (1-\alpha)\hat{Y}_{t-1} = \alpha Y_t \quad\Longrightarrow\quad \boxed{\hat{Y}_t = \alpha Y_t + (1-\alpha)\hat{Y}_{t-1}}$$

**This is the key insight of exponential smoothing:** an infinite weighted history collapses into **one number of state** plus **one new observation**. The recursion carries all the past in $\hat Y_{t-1}$ — an idea that becomes the state-space formulation below, and ultimately the Kalman filter of [[06 - The Kalman Filter and State-Space Models]].

> SES is mainly used for **smoothing** and **level extraction** — it has no trend or seasonal component.

---

## Part 3 — Decomposition

### Decomposition vs seasonal adjustment

> **Time series decomposition** is a **conceptual framework** describing how an observed series can be represented as a combination of components:
> $$\textbf{Additive: } Y_t = T_t + S_t + C_t + I_t \qquad \textbf{Multiplicative: } Y_t = T_t \times S_t \times C_t \times I_t$$
> where $T_t$ is the long-run **trend**, $S_t$ the **seasonal**, $C_t$ the **cyclical**, and $I_t$ the **irregular** component.
>
> **Seasonal adjustment** is a **practical procedure** focused on **removing the seasonal component**:
> $$\textbf{Additive: } Y_t^{SA} = Y_t - S_t \qquad \textbf{Multiplicative: } Y_t^{SA} = \frac{Y_t}{S_t}$$

**Note this is a four-component decomposition**, adding a **cyclical** component to the three in [[01 - What is a Time Series]]. The distinction: **seasonal** patterns repeat over a *fixed, known* period (quarterly, monthly); **cyclical** movements — business cycles — have *variable, unknown* duration. Seasonality can be estimated and removed; cycles generally cannot.

### Classical additive decomposition

Model: $Y_t = T_t + S_t + I_t$.

**Step 1 — trend-cycle via a centered moving average.** With $m$ the seasonal period ($m=12$ monthly, $m=4$ quarterly):
$$T_t = Y_t^* = \frac{1}{2m}\left[Y_{t-\frac{m}{2}} + 2\left(Y_{t-\frac{m}{2}+1} + \cdots + Y_{t+\frac{m}{2}-1}\right) + Y_{t+\frac{m}{2}}\right]$$

**The half-weights on the endpoints are not a detail.** With an *even* period there is no single centred observation, so a plain $m$-term average would be off-centre by half a step. Weighting the two endpoints by ½ and the interior by 1 (the $2\times$ in the numerator, divided by $2m$) produces a genuinely centred average — the standard "$2\times m$-MA".

**Step 2 — detrended values and seasonal means:**
$$d_t = Y_t - Y_t^*$$
For each season $j = 1,\dots,m$, average the corresponding detrended values:
$$\bar{d}_j = \frac{d_{j^*} + d_{j^*+m} + \cdots}{h}$$

**Averaging across years is what separates the systematic seasonal effect from noise** — the irregular component averages toward zero while the seasonal pattern, being identical each year, survives.

**Step 3 —** the seasonal indices are normalised to sum to zero, and $I_t = Y_t - T_t - S_t$ is the remainder.

### Classical multiplicative decomposition

Model: $Y_t = T_t \times S_t \times I_t$.

> The procedure follows the same steps as the additive case, **but uses ratios instead of differences.**

**Step 1** — trend-cycle via the same centered moving average, $T_t = Y_t^*$.

**Step 2** — remove the trend by taking **ratios** $\dfrac{Y_t}{Y_t^*}$, then for each season average them:
$$r_j = \frac{1}{h-1}\left(\frac{Y_{j^*}}{Y_{j^*}^*} + \frac{Y_{j^*+m}}{Y_{j^*+m}^*} + \cdots\right)$$

Multiplicative seasonal indices are normalised to **average 1** (or sum to $m$), the multiplicative analogue of summing to zero.

> [!tip] Which model to choose
> **Additive** when seasonal swings are roughly **constant in size** regardless of the level. **Multiplicative** when seasonal swings **scale with the level** — December sales are always *20% above* trend rather than *always +500 units*.
>
> Most economic and financial series are **multiplicative**, because they grow proportionally. **A quick test: plot the series. If the seasonal amplitude widens as the series rises, use multiplicative — or equivalently, take logs and use additive**, since $\ln(T\times S\times I) = \ln T + \ln S + \ln I$.

---

## Part 4 — Holt–Winters

> Holt–Winters extends exponential smoothing to handle **trend** and **seasonality**.
>
> $$\textbf{Additive seasonality: } Y_t = \text{Level}_t + \text{Seasonal}_t + \varepsilon_t$$
> $$\textbf{Multiplicative seasonality: } Y_t = \text{Level}_t \times \text{Seasonal}_t + \varepsilon_t$$
>
> **Additive:** seasonal swings are roughly constant in size. **Multiplicative:** seasonal swings scale with the series level. Seasonal period is $m$ (12 monthly, 4 quarterly).

### Holt's Linear Trend (no seasonality)

> Holt's method extends SES by allowing for a **time-varying trend**, tracking two components: a **level** and a **trend**.

$$l_t = \alpha Y_t + (1-\alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)b_{t-1}$$
$$\hat{Y}_{t+h\mid t} = l_t + h\,b_t$$

- $l_t$ — **level** (smoothed current value)
- $b_t$ — **trend** (slope) at time $t$
- $\alpha, \beta$ — smoothing parameters

**Each equation is SES applied to a different quantity:** the level equation smooths the observation against the previous level-plus-trend forecast; the trend equation smooths the observed change in level against the previous trend. **The forecast extrapolates linearly**, which is why $h$ appears multiplied by $b_t$.

### Holt–Winters Additive Seasonality

> Used when **seasonal fluctuations have constant magnitude** over time.

$$l_t = \alpha(Y_t - s_{t-m}) + (1-\alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)b_{t-1}$$
$$s_t = \gamma(Y_t - l_t) + (1-\gamma)s_{t-m}$$
$$\hat{Y}_{t+h\mid t} = l_t + h\,b_t + s_{t+h-mk}$$

**Note $Y_t - s_{t-m}$ in the level equation** — the observation is *deseasonalised* before updating the level, using the seasonal index from one full period ago. And $s_{t-m}$ rather than $s_{t-1}$ throughout: **each season is updated only once per cycle**.

### Holt–Winters Multiplicative Seasonality

> Appropriate when **seasonal fluctuations grow proportionally** with the level.

$$l_t = \alpha\frac{Y_t}{s_{t-m}} + (1-\alpha)(l_{t-1} + b_{t-1})$$
$$b_t = \beta(l_t - l_{t-1}) + (1-\beta)b_{t-1}$$
$$s_t = \gamma\frac{Y_t}{l_t} + (1-\gamma)s_{t-m}$$
$$\hat{Y}_{t+h\mid t} = (l_t + h\,b_t)\,s_{t+h-mk}$$

**Every subtraction becomes a division and the final addition becomes multiplication** — the same additive-to-multiplicative translation as in classical decomposition. $s_t$ is now a **seasonal index** (a dimensionless multiplier around 1), not an offset.

---

## Part 5 — The ETS Framework

> In modern time series analysis, Holt–Winters is formulated as an **ETS (Error–Trend–Seasonal)** state-space model:
> - **E** — form of the **error** (Additive or Multiplicative)
> - **T** — form of the **trend** (None, Additive, Multiplicative)
> - **S** — form of the **seasonal** component (None, Additive, Multiplicative)

| Method | ETS notation |
|---|---|
| Simple exponential smoothing | ETS(A, N, N) |
| **Holt's linear trend** | **ETS(A, A, N)** |
| **Holt–Winters (additive)** | **ETS(A, A, A)** |
| **Holt–Winters (multiplicative)** | **ETS(A, A, M)** |

> This is the theoretical framework implemented in **`statsmodels`**, **`forecast` (R)**, and modern forecasting libraries.

**State variables:** $\ell_t$ (level), $b_t$ (trend), $s_t$ (seasonal, period $m$).

> **The key idea: the observed series $y_t$ is generated from these latent states plus a random error term.**

**This reframing is the important conceptual step.** Holt–Winters as originally stated is a set of *ad hoc smoothing recipes*. ETS makes it a **statistical model** with a likelihood — so parameters can be estimated by maximum likelihood ([[Mathematical Statistics/contents/05 - Point Estimation|Point Estimation]]), models compared by AIC, and **prediction intervals** computed. Smoothing formulas alone give point forecasts with no measure of uncertainty.

### ETS(A, A, A) — error-correction form

**One-step-ahead forecast** (what fitted values represent):
$$\hat{y}_{t\mid t-1} = \ell_{t-1} + b_{t-1} + s_{t-m}$$

**Forecast error:**
$$e_t = y_t - \hat{y}_{t\mid t-1}$$

**State updates:**
$$\ell_t = \ell_{t-1} + b_{t-1} + \alpha e_t \qquad b_t = b_{t-1} + \beta e_t \qquad s_t = s_{t-m} + \gamma e_t$$

> Parameters $\alpha,\beta,\gamma \in (0,1)$ control **how strongly the states react to the new information $e_t$.**

**This is algebraically identical to the Holt–Winters recursions**, rewritten so that **every state is updated by a multiple of the same forecast error**. The form is far more revealing: it is an **error-correction** structure, exactly the shape of the Kalman filter update ([[06 - The Kalman Filter and State-Space Models]]) and of the TD error in [[Machine Learning/contents/04 - Model-Free Prediction|reinforcement learning]] — *state ← state + gain × prediction error*.

### ETS(A, A, M) — multiplicative seasonality

$$\hat{y}_{t\mid t-1} = (\ell_{t-1} + b_{t-1})\,s_{t-m} \qquad e_t = y_t - \hat{y}_{t\mid t-1}$$
$$\ell_t = \ell_{t-1} + b_{t-1} + \alpha e_t \qquad b_t = b_{t-1} + \beta e_t \qquad s_t = s_{t-m} + \gamma\frac{e_t}{\ell_{t-1} + b_{t-1}}$$

> Here $s_t$ acts as a seasonal **multiplier**. It is updated using a **scaled** error **so that the seasonal factor remains dimensionless.**

**The division by $(\ell_{t-1}+b_{t-1})$ is essential**: $e_t$ is in the units of $y$, but $s_t$ is a pure ratio. Dividing by the level converts the error into a proportional correction.

## ✏️ Exercises

**1.** Explain the difference between one-sided and centred moving averages, and why the classical decomposition uses a centred one despite it being unusable for forecasting.

> [!example]- Solution
> **One-sided (SMA):** $y^{MA(3)}_t = \frac13(y_t + y_{t-1} + y_{t-2})$ — uses only current and past values, so it is **computable in real time**. But every value it averages is at or before $t$, so **the smoothed series lags the true trend.** For an upward-trending series it sits systematically *below* the level.
>
> **Centred (CMA):** $y^{CMA(3)}_t = \frac13(y_{t-1}+y_t+y_{t+1})$ — symmetric around $t$, so the lag cancels and it gives an unbiased local estimate of the trend. But it needs $y_{t+1}$, which **does not exist at time $t$.**
>
> **Why decomposition uses the centred version anyway:** decomposition is a **descriptive** exercise on *historical* data, not a forecasting exercise. When analysing 2015–2024, the value for 2019 has 2020 available — there is no "future" to wait for. **You may use future data to describe the past; you may not use it to predict the future.**
>
> **The bias would corrupt the seasonal estimates otherwise.** Step 2 computes $d_t = Y_t - Y_t^*$, and if $Y_t^*$ systematically lags, the "detrended" values contain leftover trend which then contaminates the seasonal indices — attributing trend growth to whichever season happens to fall later in the year.
>
> **The cost is boundary data loss.** A centred $2\times12$-MA cannot be computed for the first six or last six observations. Losing a year of a ten-year monthly series is significant, and it means the **most recent trend estimate — the one you most want — is missing**. This is precisely why forecasting methods use one-sided exponential smoothing instead, accepting lag in exchange for a current estimate.
>
> **Note the half-weight endpoints** in the $2\times m$-MA. With $m$ even, a plain $m$-term average has its centre between two observations; the $\frac{1}{2m}[Y_{t-m/2} + 2(\cdots) + Y_{t+m/2}]$ construction restores centring while still averaging exactly one full seasonal cycle — which is what makes the seasonal component cancel out.

**2.** Derive the SES recursion from the infinite weighted-sum form, and explain what the derivation reveals.

> [!example]- Solution
> **Start from the expanded form:**
> $$\hat{Y}_t = \alpha Y_t + \alpha(1-\alpha)Y_{t-1} + \alpha(1-\alpha)^2 Y_{t-2} + \cdots = \alpha\sum_{i=0}^{\infty}(1-\alpha)^i Y_{t-i}$$
>
> **Write the same expression one step earlier and multiply by $(1-\alpha)$:**
> $$(1-\alpha)\hat{Y}_{t-1} = \alpha(1-\alpha)Y_{t-1} + \alpha(1-\alpha)^2 Y_{t-2} + \alpha(1-\alpha)^3 Y_{t-3} + \cdots$$
>
> **Subtract.** Every term on the right matches exactly, leaving only $\alpha Y_t$:
> $$\hat{Y}_t - (1-\alpha)\hat{Y}_{t-1} = \alpha Y_t \quad\Longrightarrow\quad \hat{Y}_t = \alpha Y_t + (1-\alpha)\hat{Y}_{t-1}$$
>
> **What this reveals — three things:**
>
> **1. An infinite history compresses into one number.** The weighted sum stretches back forever, yet the recursion needs only $\hat Y_{t-1}$ and the new observation. **$\hat Y_{t-1}$ is a sufficient statistic for the entire past** — the same idea as the Markov property in [[Machine Learning/contents/02 - Markov Decision Processes|MDPs]], and the seed of the state-space formulation.
>
> **2. The weights are geometric and sum to 1**, since $\alpha\sum_{i\ge0}(1-\alpha)^i = \alpha \cdot \frac{1}{1-(1-\alpha)} = 1$. So the smoothed value is a genuine weighted *average*, unbiased in level.
>
> **3. $\alpha$ has a clear interpretation.** Large $\alpha$ puts most weight on $Y_t$ and discounts the past rapidly — responsive but noisy. Small $\alpha$ spreads weight far back — smooth but slow to react. The **effective memory** is roughly $1/\alpha$ periods, so $\alpha = 0.1$ behaves like a 10-period average.
>
> **Rewriting as error-correction** makes the connection to ETS explicit:
> $$\hat Y_t = \hat Y_{t-1} + \alpha(Y_t - \hat Y_{t-1})$$
> **State ← state + gain × prediction error** — the same shape as the Kalman filter and as TD learning. Every method in this chapter is an instance of it.
>
> This is also why SES is **computationally trivial**: $O(1)$ memory and one multiply-add per observation, regardless of series length. A centred moving average needs the whole window.

**3.** When should you use additive versus multiplicative decomposition? Give a diagnostic and explain the log alternative.

> [!example]- Solution
> **Additive** ($Y_t = T_t + S_t + I_t$) when seasonal swings are **constant in absolute size** — December is always +500 units above trend, whether the trend is at 2,000 or 20,000.
>
> **Multiplicative** ($Y_t = T_t \times S_t \times I_t$) when seasonal swings **scale with the level** — December is always 25% above trend, so the absolute swing grows as the business does.
>
> **The diagnostic is visual and reliable: plot the series and look at the seasonal amplitude over time.**
> - **Constant width band** → additive
> - **Widening (fanning) band** → multiplicative
>
> **Most economic and financial series are multiplicative**, because they grow proportionally. Retail sales, GDP, air passengers, electricity demand all show widening seasonal swings as they grow.
>
> **The consequence of choosing wrong.** Fit an additive model to a multiplicative series and the seasonal index is a **compromise** — too large for the early years, too small for the recent ones. The residuals then show a clear pattern: systematically negative in early peaks, positive in later ones. **Check the residuals for remaining seasonality; if present, you chose the wrong form.**
>
> **The log alternative — often the better route.** Taking logs converts multiplication to addition:
> $$\ln(T_t \times S_t \times I_t) = \ln T_t + \ln S_t + \ln I_t$$
> So **an additive decomposition of $\ln Y_t$ is a multiplicative decomposition of $Y_t$.**
>
> Three reasons this is often preferred: additive methods are simpler and better understood; logs frequently **stabilise the variance** as well as linearise the seasonality, addressing two problems at once; and it connects to the log-returns of [[01 - What is a Time Series]] and the log transformations of [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]].
>
> **The requirement:** logs need **strictly positive** data. A series containing zeros or negatives (net exports, profit/loss) must use a genuinely multiplicative method or `log1p`.

**4.** Explain the Holt–Winters seasonal update $s_t = \gamma(Y_t - l_t) + (1-\gamma)s_{t-m}$ — why $s_{t-m}$ rather than $s_{t-1}$?

> [!example]- Solution
> **Because each season is only comparable to itself one full cycle ago.**
>
> With monthly data ($m=12$), the seasonal index for December should be updated using **last December's** index, not November's. December and November have entirely different seasonal characters; blending them would destroy the pattern rather than refine it.
>
> **So the seasonal component is really $m$ separate exponentially-smoothed series**, one per season, each updated once per cycle:
> - $s_{\text{Jan}}$ updated in January using last January's value
> - $s_{\text{Feb}}$ updated in February using last February's value
> - …
>
> **The consequences of this structure:**
>
> **1. Seasonal indices adapt slowly.** Each index receives one update per year, so with $\gamma = 0.1$ it takes roughly ten *years* to substantially revise a seasonal pattern. That is usually correct — seasonality is a stable structural feature — but it means Holt–Winters is slow to detect a genuine change in seasonal behaviour.
>
> **2. Initialisation matters a great deal.** With only one update per season per cycle, initial seasonal values persist for many periods. Poor initialisation contaminates a long stretch of forecasts, which is why `statsmodels` estimates the initial states rather than guessing them.
>
> **3. You need at least two full cycles of data** — ideally more — before the seasonal component means anything. With 18 months of monthly data, six seasons have been updated once and six not at all.
>
> **Why $Y_t - l_t$ is the target.** The level $l_t$ is the deseasonalised current level, so $Y_t - l_t$ is **what the observation exceeds the level by — the seasonal effect for this period.** The equation smooths that estimate against the previous cycle's, exactly as SES smooths the level.
>
> **Note the ordering matters:** $l_t$ must be computed before $s_t$, since the seasonal update uses the *new* level. And the level update uses $s_{t-m}$, the *old* seasonal index — computing them in the wrong order gives a subtly different (and wrong) model.

**5.** (Advanced) Explain what the ETS state-space framework adds beyond the Holt–Winters recursions, given the update equations are algebraically equivalent.

> [!example]- Solution
> **They are equivalent as point-forecast recipes** — writing $e_t = y_t - (\ell_{t-1}+b_{t-1}+s_{t-m})$ and substituting into the ETS updates recovers the Holt–Winters equations exactly. So why bother?
>
> **Because ETS is a *statistical model* and Holt–Winters is an *algorithm*.** The framework adds an explicit error term $\varepsilon_t$ with an assumed distribution, and that changes what is possible:
>
> **1. Prediction intervals.** Holt–Winters gives a point forecast and nothing else. ETS specifies how the error propagates through the state recursions, so the forecast *variance* at horizon $h$ can be derived. **A forecast without an interval is nearly useless for decisions** — you cannot size inventory or hedge a position from a point estimate.
>
> **2. Maximum likelihood estimation.** With a distributional assumption there is a likelihood, so $\alpha,\beta,\gamma$ and the initial states can be estimated by **MLE** ([[Mathematical Statistics/contents/05 - Point Estimation|Point Estimation]]) rather than by minimising SSE on an ad hoc grid. Initial states become *parameters* rather than guesses.
>
> **3. Model selection by information criteria.** Because there is a likelihood, **AIC/BIC** can compare ETS(A,A,N) against ETS(A,A,A) against ETS(A,A,M) on a principled basis. This is what `statsmodels` and R's `forecast` package automate — the famous `ets()` function searches the 30 admissible ETS specifications and selects by AICc.
>
> **4. It clarifies which combinations are legitimate.** Not all 3×3×3 = 27 (plus damped variants) combinations are well-defined; multiplicative errors with additive seasonality can produce negative values in some regimes. The state-space formulation makes the admissible set explicit.
>
> **The error-correction form is also more revealing** than the original recursions:
> $$\ell_t = \ell_{t-1} + b_{t-1} + \alpha e_t \qquad b_t = b_{t-1} + \beta e_t \qquad s_t = s_{t-m} + \gamma e_t$$
> **Every state is corrected by a multiple of the *same* forecast error**, with $\alpha,\beta,\gamma$ as gains controlling how strongly each state responds to surprise. This is exactly the structure of the **Kalman filter** ([[06 - The Kalman Filter and State-Space Models]]) — where the gains are computed optimally from the noise covariances rather than fitted — and of the **TD update** in [[Machine Learning/contents/04 - Model-Free Prediction|Model-Free Prediction]]. Recognising the shared shape is worth more than memorising three sets of recursions.
>
> **In the multiplicative case the scaling matters:** $s_t = s_{t-m} + \gamma\frac{e_t}{\ell_{t-1}+b_{t-1}}$. Since $s_t$ is dimensionless while $e_t$ carries the units of $y$, dividing by the level is what keeps the seasonal factor a pure ratio.

## 📝 Summary

- **Moving averages smooth but do not detrend** in the econometric sense — they are exploratory tools.
- **One-sided MAs are usable in real time but lag**; **centred MAs are unbiased but need future data.** Decomposition uses centred; forecasting uses one-sided.
- **Larger windows give smoother series but greater boundary data loss.**
- **Double moving average** exploits the fact that a single MA lags a linear trend predictably, using the gap between single and double MA to estimate the slope.
- **SES:** $\hat y_t = \alpha y_t + (1-\alpha)\hat y_{t-1}$ — an infinite geometric weighting collapsed into one recursion. $\alpha$ controls responsiveness; effective memory ≈ $1/\alpha$.
- **Decomposition is a framework** ($Y_t = T_t + S_t + C_t + I_t$ or the product form); **seasonal adjustment is the practical procedure** of removing $S_t$.
- **Seasonal = fixed known period; cyclical = variable unknown duration.**
- **Classical decomposition:** centred MA for trend → detrend by difference (additive) or ratio (multiplicative) → average by season → remainder is irregular.
- **Additive when seasonal swings are constant; multiplicative when they scale with the level.** An additive decomposition of $\ln Y_t$ *is* a multiplicative decomposition of $Y_t$.
- **Holt** adds a trend to SES; **Holt–Winters** adds seasonality, in additive or multiplicative form.
- **Seasonal indices update from $s_{t-m}$, not $s_{t-1}$** — each season is its own smoothed series, updated once per cycle.
- **ETS(E,T,S)** recasts Holt–Winters as a state-space model, enabling **prediction intervals, MLE, and AIC-based model selection**. Its error-correction form is the same *state ← state + gain × error* shape as the Kalman filter.

## ⚠️ Important Notes

**Smoothing is not detrending.** A moving average makes the trend visible; it does not make the series stationary. Differencing does that — [[03 - Stationarity and Difference Equations]].

**Centred moving averages cannot be used for forecasting.** They require $y_{t+1}$. Using one in a forecasting pipeline is a form of leakage.

**A $2\times m$-MA needs half-weights on the endpoints** when $m$ is even, or the average is off-centre by half a period.

**Moving averages lose $2k$ observations for a double MA and $m/2$ at each boundary for a centred MA** — and the missing recent values are exactly the ones you most want.

**Weights in a WMA must sum to the divisor**, or the smoothed series is biased in level.

**Wrong decomposition form leaves seasonality in the residuals.** Check residuals for remaining seasonal pattern; if present, switch between additive and multiplicative.

**Logs require strictly positive data.** Series with zeros or negatives (net exports, profit) cannot use the log-additive route.

**Holt–Winters needs at least two full seasonal cycles**, preferably more. With less, some seasonal indices have never been updated.

**Seasonal indices adapt slowly** — one update per season per cycle — so Holt–Winters is slow to detect genuine changes in seasonal behaviour, and **initialisation persists for years**.

**Order matters in the Holt–Winters recursions:** the level update uses the *old* $s_{t-m}$, and the seasonal update uses the *new* $l_t$.

**Holt's linear trend extrapolates indefinitely** — $\hat Y_{t+h} = l_t + hb_t$ grows without bound. For long horizons this is usually implausible, which is why **damped trend** variants exist.

**Smoothing methods give point forecasts only.** Prediction intervals require the ETS state-space formulation, which is why modern practice uses ETS rather than raw Holt–Winters.

**Classical decomposition assumes the seasonal pattern is constant across the sample.** STL and X-13 allow it to evolve; classical decomposition does not.

> [!warning] Gaps in the source material
> The lecture is a Colab notebook with slides as `%%html` cells. **The LaTeX in this lecture extracted very well** — nearly all formulas survived intact, unlike the PowerPoint-based subjects in this vault.
> - **All plots are code outputs**, not stored content — the smoothing comparisons, decomposition plots, and Holt–Winters fits must be re-run to be seen.
> - **Several slides are truncated by the HTML boundary:** slide 1 (cut at *"rathe"* — "rather than formal detrending"), slide 2 (cut at *"boundaries"*), slide 4 and 5 (**the constraint on $\alpha$ is cut at "$0 <$"** — it is $0 < \alpha < 1$), slide 10 (cut at *"The purpose of seasonal adjus"*), slide 11 (**Step 2's seasonal averaging formula is cut mid-subscript**), slide 12 (cut at $j=1,2$), slide 16 (**the constraint on $\beta$ is cut**).
> - **Every slide carries a trailing MathJax loader script** which extracts as noise (`if (!window.__mathjax_loaded__)...`); I have stripped it.
> - **Slides 6–9, 13–14 produced no extractable slide text** — they are code cells or figures.
> - **Step 3 of the classical additive decomposition is not shown** — the normalisation of seasonal indices and the extraction of $I_t$ are cut off. I have supplied the standard treatment.
> - The **cyclical component $C_t$** is named in the decomposition framework but **never estimated** in either the additive or multiplicative procedure — classical decomposition folds it into the trend, giving a "trend-cycle" component. The slides do not say so explicitly.

---
**Previous:** [[01 - What is a Time Series]] · **Next:** [[03 - Stationarity and Difference Equations]]
