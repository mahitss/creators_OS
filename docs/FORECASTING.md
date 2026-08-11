# Statistical Forecasting & Model Evaluation

## Non-Speculative Time-Series Forecasting
Generates baseline projections (`moving_average`, `exponential_smoothing`, `trend_extrapolation`) with explicit uncertainty intervals and expiration timestamps (`expires_at`). Tracks prediction accuracy via `MAE`, `RMSE`, and `MAPE` (`ForecastEvaluation`). Insufficient historical data points (< 3) trigger an `insufficient_data` return instead of speculative guessing.
