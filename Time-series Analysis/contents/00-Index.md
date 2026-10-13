---
subject: Time-series Analysis
chapter: 00
tags: [ds, time-series, index, moc]
source: "documents/slides/ (11 Colab notebooks, Dr. Tran Thi Ha, Faculty of Mathematical Economics, NEU)"
---

# Time-series Analysis: Index

Lecturer: Dr. Tran Thi Ha, Faculty of Mathematical Economics, NEU. Assessment (Lecture 1): attendance 10%, computer test (Python) 20%, assignment 20%, final exam 50%. Textbooks in `documents/`: Hamilton, *Time Series Analysis* (the theory behind Lectures 6–10); Peixeiro, *Time Series Forecasting in Python*; Auffarth, *Machine Learning for Time-Series with Python*.

## Chapters

| # | Chapter | Topics | Status |
|---|---|---|---|
| 01 | [[01 - What is a Time Series]] | stocks and flows, lags, growth rates, components, dates in Python | ✅ |
| 02 | [[02 - Trend, Seasonality and Decomposition]] | moving averages, exponential smoothing, decomposition, Holt–Winters, ETS | ✅ |
| 03 | [[03 - Stationarity and Difference Equations]] | stationarity, Wold, lag operator, roots and dynamic multipliers | ✅ |
| 04 | [[04 - AR, MA and ARMA Processes]] | moments, Yule–Walker, invertibility, forecasting | ✅ |
| 05 | [[05 - ACF, PACF and the Box-Jenkins Methodology]] | ACF/PACF, Ljung–Box, ADF/PP/KPSS, ARIMA, AIC/BIC | ✅ |
| 06 | [[06 - The Kalman Filter and State-Space Models]] | state space, filter recursions, likelihood | ✅ |
| 07 | [[07 - SARIMA and Vector Autoregression]] | seasonal ARIMA; VAR, Granger causality, IRF, FEVD | ✅ |
| 08 | [[08 - VECM and Cointegration]] | error correction, rank of Π, Johansen | ✅ |
| 09 | [[09 - ARCH, GARCH and Extensions]] | volatility clustering, GARCH, leverage | ✅ |
| 10 | [[10 - Structural Vector Autoregression]] | identification, short- and long-run SVAR, Blanchard–Quah | ✅ |

Three threads: the univariate mean (01–05, SARIMA), several variables (VAR → VECM → SVAR), and the variance (09). The Kalman filter (06) is the estimation engine under all of them.

Recurring ideas:
1. Any order-$p$ system is order 1 in a bigger space (the companion matrix: multipliers, forecasts, state transitions, VAR stability).
2. Stability: roots $z$ outside, or eigenvalues λ = 1/z inside, the unit circle.
3. Every model filters white noise (Wold); the ψ weights are the impulse responses.
4. Forecasting replaces unknowns by their expectations (Wiener–Kolmogorov, Kalman, GARCH).
5. Statistics gives dynamics; identifying assumptions give causation.

## Choosing a model

| One variable | Model |
|---|---|
| stationary, no seasonality | ARMA |
| unit root | ARIMA |
| seasonal | SARIMA |
| latent states, missing data | state space + Kalman |
| volatility clustering | GARCH family |

| Several variables (test integration first) | Model |
|---|---|
| all $I(0)$ | VAR in levels |
| $I(1)$, not cointegrated | VAR in differences |
| $I(1)$, cointegrated | VECM |
| causal interpretation needed | SVAR |

## Key formulas

$$\rho_k=\gamma_k/\gamma_0;\quad\text{AR(1): }\rho_k=\phi^k,\ \gamma_0=\frac{\sigma^2}{1-\phi^2};\quad\text{AR(2): }\rho_1=\frac{\phi_1}{1-\phi_2},\ \rho_2=\phi_1\rho_1+\phi_2;\quad\text{MA}(q)\text{: }\rho_k=0,\ k>q$$
$$\text{AR(2) stable: }\phi_2<1\pm\phi_1,\ |\phi_2|<1;\quad\text{complex roots: }R=\sqrt{-\phi_2},\ T=2\pi/\theta$$
$$Q^*=n(n+2)\sum_{k\le m}\frac{\hat\rho_k^2}{n-k}\sim\chi^2(m-p-q);\quad\text{bands }\pm2/\sqrt n$$
$$K_t=P_{t\mid t-1}HS_t^{-1};\quad\ell=-\tfrac12\sum(\log2\pi+\log S_t+v_t^2/S_t)$$
$$\Delta Y_t=\alpha\beta'Y_{t-1}+\sum\Gamma_i\Delta Y_{t-i}+\varepsilon_t,\quad\Pi=\sum A_i-I$$
$$\sigma_t^2=\alpha_0+\alpha_1\varepsilon^2_{t-1}+\beta_1\sigma^2_{t-1},\quad\bar\sigma^2=\frac{\alpha_0}{1-\alpha_1-\beta_1}$$
$$\Sigma=P_{sr}P_{sr}',\ P_{sr}=A^{-1}B,\ n(n-1)/2\text{ restrictions}$$

## Cross-subject links

[[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] (tests, estimation) · [[Econometrics/contents/00-Index|Econometrics]] (ch. 10–12: stationarity, unit roots, serial correlation from the regression side) · [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]] (pandas dates, resampling, leakage) · [[Machine Learning/contents/00-Index|Machine Learning]] · [[Linear Algebra/contents/00-Index|Linear Algebra]] (eigenvalues, companion, Toeplitz, Cholesky)

## Source issues

> [!warning] Extraction
> The slides are HTML in Colab cells. Stripping tags removed every `<` inside inline LaTeX, so conditions like $|\phi|<1$, $|\lambda_i|<1$, $R<1$, $\sum(\alpha_i+\beta_i)<1$, $\varepsilon_{t-1}<0$, $\gamma<0$ are reconstructions (standard results). No notebook saved outputs, so no figures survive.

Missing data: `GDP_Trade_Quarterly_Clean.xlsx` (ch. 01), `CPI_PACF.xlsx`, `gdp_Pacf.xlsx` (05), `GDP_week1.xlsx`, the VAR datasets (07), the VECM data (08), `returns5.csv`, `byd.csv` (09). Ch. 10's `lutkepohl2.dta` and `m1gdp.dta` are fetched from stata-press.com and are reproducible. Reported estimates were checked for internal consistency where possible.

**Slide errors** (verified by recomputation):

| Ch. | Error |
|---|---|
| 02 | ETS(A,A,M) level and trend updates omit the division of $e_t$ by $s_{t-m}$ |
| 03 | stability-triangle colours contradict the caption; $\partial y/\sigma_t$ for $\partial y/\partial w_t$ |
| 04 | MA(2) example: $\gamma_0=31/19$ (correct 31/18), roots −2, −3 (correct +2, +3) |
| 05 | Bartlett's variance formula missing the leading 1 and factor 2; no Ljung–Box df adjustment |
| 06 | $v_t$ used for both state noise and innovation; $H$ vs $H'$ inconsistent |
| 10 | $P$ defined in both directions ($u=P\varepsilon$, $\varepsilon=Pu$) |

Verified correct: the AR(3) Yule–Walker values (ch. 04), the CPI PACF (ch. 05), Example 7.1's IRF/FEVD (ch. 07), the VECM Π = αβ′ decompositions and the Johansen critical values (ch. 08: standard values without deterministic terms; an earlier version of these notes wrongly called them non-standard).

**Named but not taught**: IGARCH/FIGARCH, structural FEVD, sign restrictions (one bullet), the Kalman smoother, weak-exogeneity tests, seasonal unit-root tests, IRF confidence bands.

**Syllabus vs files**: from Lecture 6 the syllabus titles differ from the notebooks; the notes follow the notebooks. Two VECM notebooks are complementary. The ARCH deck calls itself Lecture 10, like the SVAR deck. Only Lectures 3 and 4 include exercises (without solutions); other exercises are constructed and checked.
