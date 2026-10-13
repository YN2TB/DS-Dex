---
subject: Time-series Analysis
chapter: 02
tags: [ds, time-series, moving-average, exponential-smoothing, holt-winters, ets, decomposition]
source: "Lecture_2_DSEB.ipynb — Tran Thi Ha, Faculty of Mathematical Economics, NEU (2025)"
---

# Estimating Trend and Decomposing Time Series

[[01 - What is a Time Series]] named the components; this lecture estimates them with smoothing methods, before any probability model ([[03 - Stationarity and Difference Equations]]). Outline: estimating the trend (moving averages, smoothing); decomposing into trend, seasonal and irregular parts; additive and multiplicative frameworks; seasonal adjustment.

## 📘 Main Knowledge

### Moving averages

Moving averages smooth a series, reducing short-run fluctuations to show the underlying movement.

- **Simple (one-sided)**: $y^{MA(3)}_t=\frac13(y_t+y_{t-1}+y_{t-2})$. Uses current and past values only, so the first two values are missing. It approximates the trend locally but doesn't remove it in the econometric sense; it is for exploration and plots.
- **Centred**: $y^{CMA(3)}_t=\frac13(y_{t-1}+y_t+y_{t+1})$; in general $\frac1{2m+1}\sum_{j=-m}^my_{t+j}$. A better local trend estimate, but it needs future values, so it can't be used for real-time forecasting.
- **Weighted**: $y^{WMA(5)}_t=\frac1{10}(y_{t-2}+2y_{t-1}+4y_t+2y_{t+1}+y_{t+2})$: more weight near $t$; the weights sum to the divisor.

Larger windows smooth more but lose more data at the ends. One-sided averages lag a trending series; centred ones don't but need the future.

**Double moving average** (for a linear trend): $Y^{MA(k)(2)}_t=\frac1k\sum_{j=0}^{k-1}Y^{MA(k)}_{t-j}$, missing for the first $2k$ observations (strictly $2k-2$). A single MA lags a linear trend by a fixed amount and the double MA lags it again, so their gap measures the slope:
$$\hat b_n=\frac{2(Y^{MA(k)}_n-Y^{MA(k)(2)}_n)}{k-1},\qquad \hat Y_{n+h}=Y^{MA(k)}_n+\hat b_n\,h.$$

### Simple exponential smoothing

$$\hat y_t=\alpha y_t+(1-\alpha)\hat y_{t-1},\qquad0<\alpha<1.$$
A weighted average of the new observation and the previous smoothed value; larger α reacts faster, smaller α smooths more. Expanding,
$$\hat Y_t=\alpha\sum_{i\ge0}(1-\alpha)^iY_{t-i};$$
subtracting $(1-\alpha)\hat Y_{t-1}$ cancels every term but $\alpha Y_t$, giving the recursion. The weights are geometric and sum to 1, and the whole past is carried in one number. SES extracts a level; it has no trend or seasonality.

### Decomposition and seasonal adjustment

**Decomposition** is a framework: additive $Y_t=T_t+S_t+C_t+I_t$ or multiplicative $Y_t=T_t\times S_t\times C_t\times I_t$, with trend, seasonal, **cyclical** and irregular components. Seasonal patterns have a fixed known period; cycles (business cycles) have variable length. **Seasonal adjustment** is the practical step of removing $S_t$: $Y^{SA}_t=Y_t-S_t$ or $Y_t/S_t$.

**Classical additive** ($Y_t=T_t+S_t+I_t$, period $m$, 12 monthly or 4 quarterly):
1. Trend-cycle by a centred $2\times m$ moving average:
$$T_t=Y^*_t=\frac1{2m}\Big[Y_{t-m/2}+2\big(Y_{t-m/2+1}+\dots+Y_{t+m/2-1}\big)+Y_{t+m/2}\Big].$$
With even $m$, half-weights on the two ends centre the average while covering exactly one cycle.
2. Detrend, $d_t=Y_t-Y^*_t$, and average each season over the years: $\bar d_j=(d_{j^*}+d_{j^*+m}+\dots)/h$. Noise averages out; the repeating seasonal effect remains.
3. Normalize the indices to sum to zero; the irregular part is $I_t=Y_t-T_t-S_t$.

**Classical multiplicative** ($Y_t=T_t\times S_t\times I_t$): the same steps with ratios. Detrend by $Y_t/Y^*_t$ and average by season, $r_j=\frac1{h-1}\big(\frac{Y_{j^*}}{Y^*_{j^*}}+\frac{Y_{j^*+m}}{Y^*_{j^*+m}}+\dots\big)$; normalize to average 1.

Use additive when seasonal swings have constant size, multiplicative when they grow with the level (most economic series). Since $\ln(T\cdot S\cdot I)=\ln T+\ln S+\ln I$, an additive decomposition of $\ln Y_t$ is a multiplicative decomposition of $Y_t$. Classical decomposition leaves the cycle inside the trend ("trend-cycle").

### Holt and Holt–Winters

Additive seasonality: $Y_t=\text{Level}_t+\text{Seasonal}_t+\varepsilon_t$; multiplicative: $Y_t=\text{Level}_t\times\text{Seasonal}_t+\varepsilon_t$.

**Holt's linear trend** (level $l_t$, slope $b_t$):
$$l_t=\alpha Y_t+(1-\alpha)(l_{t-1}+b_{t-1}),\qquad b_t=\beta(l_t-l_{t-1})+(1-\beta)b_{t-1},\qquad\hat Y_{t+h\mid t}=l_t+hb_t.$$
Each line is SES applied to a different quantity; the forecast extrapolates linearly.

**Holt–Winters, additive seasonality**:
$$l_t=\alpha(Y_t-s_{t-m})+(1-\alpha)(l_{t-1}+b_{t-1}),\quad b_t=\beta(l_t-l_{t-1})+(1-\beta)b_{t-1},\quad s_t=\gamma(Y_t-l_t)+(1-\gamma)s_{t-m},$$
$$\hat Y_{t+h\mid t}=l_t+hb_t+s_{t+h-mk},$$
where $k$ makes $t+h-mk$ fall in the last observed cycle. The level is updated with the deseasonalized observation, and each season is updated from its own value one cycle earlier ($s_{t-m}$).

**Holt–Winters, multiplicative seasonality**: subtraction by $s$ becomes division and the forecast multiplies:
$$l_t=\alpha\frac{Y_t}{s_{t-m}}+(1-\alpha)(l_{t-1}+b_{t-1}),\quad b_t\ \text{as above},\quad s_t=\gamma\frac{Y_t}{l_t}+(1-\gamma)s_{t-m},\quad\hat Y_{t+h\mid t}=(l_t+hb_t)s_{t+h-mk}.$$

### ETS

Modern practice writes Holt–Winters as an **ETS (error, trend, seasonal)** state-space model: E additive or multiplicative; T none, additive or multiplicative; S none, additive or multiplicative.

| Method | ETS |
|---|---|
| simple exponential smoothing | ETS(A,N,N) |
| Holt's linear trend | ETS(A,A,N) |
| Holt–Winters additive | ETS(A,A,A) |
| Holt–Winters multiplicative | ETS(A,A,M) |

States $\ell_t$, $b_t$, $s_t$; the observed $y_t$ is generated by the latent states plus random error. Implemented in `statsmodels` and R's `forecast`.

**ETS(A,A,A)**, error-correction form:
$$\hat y_{t\mid t-1}=\ell_{t-1}+b_{t-1}+s_{t-m},\quad e_t=y_t-\hat y_{t\mid t-1},$$
$$\ell_t=\ell_{t-1}+b_{t-1}+\alpha e_t,\quad b_t=b_{t-1}+\beta e_t,\quad s_t=s_{t-m}+\gamma e_t.$$
Every state moves by a multiple of the same forecast error: state ← state + gain × error, the shape of the Kalman filter ([[06 - The Kalman Filter and State-Space Models]]). This reproduces the Holt–Winters forecasts exactly when $\beta_{ETS}=\alpha\beta_{HW}$ and $\gamma_{ETS}=(1-\alpha)\gamma_{HW}$ (checked numerically).

**ETS(A,A,M)**: $\hat y_{t\mid t-1}=(\ell_{t-1}+b_{t-1})s_{t-m}$, and
$$\ell_t=\ell_{t-1}+b_{t-1}+\alpha\frac{e_t}{s_{t-m}},\quad b_t=b_{t-1}+\beta\frac{e_t}{s_{t-m}},\quad s_t=s_{t-m}+\gamma\frac{e_t}{\ell_{t-1}+b_{t-1}}.$$
The scaled error keeps the seasonal factor dimensionless (see the erratum note on the level and trend lines).

What ETS adds to the Holt–Winters recipes: an error distribution, hence a likelihood (MLE of parameters and initial states, [[Mathematical Statistics/contents/05 - Point Estimation|Point Estimation]]), model comparison by AIC, and prediction intervals.

## ✏️ Exercises

**1.** Why does classical decomposition use a centred moving average, even though it can't be used to forecast?

> [!example]- Solution
> A one-sided average lags a trending series, so $d_t=Y_t-Y^*_t$ would keep part of the trend, and that leftover would be attributed to whichever seasons fall later. Decomposition describes history, where the "future" values are known, so using them is fine; forecasting is where it would leak. The price: a $2\times12$ MA loses six values at each end, including the most recent trend estimate, which is why forecasting uses one-sided smoothing.

**2.** Derive the SES recursion from its weighted-sum form. What does it show?

> [!example]- Solution
> Subtracting $(1-\alpha)\hat Y_{t-1}=\alpha\sum_{i\ge1}(1-\alpha)^iY_{t-i}$ from $\hat Y_t=\alpha\sum_{i\ge0}(1-\alpha)^iY_{t-i}$ leaves $\alpha Y_t$. The weights sum to $\alpha/(1-(1-\alpha))=1$, so the estimate is unbiased in level, and one stored number summarizes the whole past ($O(1)$ memory). The mean age of the weights is $(1-\alpha)/\alpha$, the same as a simple average of $2/\alpha-1$ periods: α = 0.1 behaves like a 19-period average. Written as $\hat Y_t=\hat Y_{t-1}+\alpha(Y_t-\hat Y_{t-1})$ it is an error-correction update.

**3.** When should decomposition be additive or multiplicative? How can you tell, and what is the log alternative?

> [!example]- Solution
> Plot the series: a seasonal band of constant width suggests additive; a band that widens with the level suggests multiplicative. Fitting the wrong form leaves seasonality in the residuals (early peaks under-fitted, later ones over-fitted, or vice versa). Taking logs turns a multiplicative structure into an additive one and often stabilizes the variance too, but needs strictly positive data (not net exports or profit).

**4.** In Holt–Winters, why is the seasonal update based on $s_{t-m}$ rather than $s_{t-1}$?

> [!example]- Solution
> December is comparable only with last December, not with November. The seasonal component is $m$ separate smoothed series, each updated once per cycle. Consequences: seasonal indices adapt slowly (with γ = 0.1 it takes years); initial values persist, so they should be estimated (as `statsmodels` does); and you need at least two full cycles of data. $Y_t-l_t$ is this period's excess over the deseasonalized level. Order matters: the level uses the old $s_{t-m}$, the seasonal update uses the new $l_t$.

**5.** (Advanced) The ETS updates reproduce Holt–Winters. What does the ETS framework add?

> [!example]- Solution
> Holt–Winters is an algorithm; ETS is a statistical model with an explicit error term. That gives prediction intervals (forecast variance at each horizon), maximum likelihood estimation of the smoothing parameters and initial states, and comparison of specifications by AIC/AICc (R's `ets()` searches the admissible models). It also shows which combinations are well defined (multiplicative errors with additive seasonality can misbehave). The error-correction form makes the common structure visible: each state is corrected by a gain times the same forecast error, as in the Kalman filter, where the gains are derived from noise variances instead of being fitted.

## 📝 Summary

- Moving averages smooth but don't detrend; one-sided ones lag, centred ones need future data.
- Larger windows: smoother, more data lost at the ends.
- Double MA estimates a linear trend's slope from the lag between single and double averages.
- SES: geometric weights, one recursion; α sets responsiveness.
- Decomposition: trend, seasonal, cyclical, irregular; seasonal adjustment removes $S_t$.
- Classical decomposition: centred MA → detrend by difference or ratio → average by season → remainder.
- Additive for constant swings, multiplicative for proportional ones (or additive on logs).
- Holt adds a trend, Holt–Winters a seasonal component, updated from $s_{t-m}$.
- ETS turns these recipes into state-space models with likelihoods and intervals.

## ⚠️ Important Notes

1. Smoothing is not detrending; differencing is ([[03 - Stationarity and Difference Equations]]).
2. Centred moving averages leak the future into forecasts.
3. An even-period MA needs half-weights at the ends.
4. Centred MAs lose the most recent values.
5. WMA weights must sum to the divisor.
6. Seasonality left in the residuals means the wrong form.
7. Logs need positive data.
8. Holt–Winters needs at least two seasonal cycles.
9. Seasonal indices adapt slowly; initialization persists.
10. Holt's trend extrapolates without limit (hence damped trends).
11. Smoothing alone gives no prediction intervals.
12. Classical decomposition assumes a fixed seasonal pattern (STL and X-13 relax this).

> [!warning] Gaps in the source material
> - Slides are HTML cells in a Colab notebook; the LaTeX extracted well, but no plots were saved, and every slide carries a MathJax loader script (removed).
> - Truncated: slides 1, 2, 4–5 (the α constraint, completed as $0<\alpha<1$), 10, 11 (seasonal averaging formula), 12, 16 (β constraint). Step 3 of the additive decomposition isn't shown; the standard step is given. Slides 6–9, 13–14 are code or figures.
> - $C_t$ is named but never estimated.
> - Erratum (slide 22, ETS(A,A,M)): the level and trend updates are printed as $\ell_{t-1}+b_{t-1}+\alpha e_t$ and $b_{t-1}+\beta e_t$. Substituting $y_t=(\ell_{t-1}+b_{t-1})s_{t-m}+e_t$ into the lecture's own multiplicative Holt–Winters level equation gives $\ell_t=\ell_{t-1}+b_{t-1}+\alpha e_t/s_{t-m}$, and likewise $\beta e_t/s_{t-m}$ (Hyndman & Athanasopoulos). The seasonal line is correct.
> - The slides give $\alpha,\beta,\gamma\in(0,1)$ for ETS without noting that ETS's β and γ are reparameterizations of Holt–Winters' ($\beta_{ETS}=\alpha\beta_{HW}$, $\gamma_{ETS}=(1-\alpha)\gamma_{HW}$).

**Previous:** [[01 - What is a Time Series]] · **Next:** [[03 - Stationarity and Difference Equations]]
