"""
Rolling forecast for fund-flow categories — adapted from the top-level
project's forecast.py.

Same method (trailing 3-month moving average), same reasoning for
choosing it (auditable, no black box). Adapted schema: no "budget"
exists for macro fund flows, so this only forecasts against trailing
trend, not a budget plan.

For each category, month:
- forecast[t]          = mean(actual[t-3], actual[t-2], actual[t-1])
- variance_vs_forecast  = actual[t] - forecast[t]
- variance_pct          = variance_vs_forecast / |forecast[t]|   (abs
  denominator — flow series cross zero, so a plain pct would blow up
  or flip sign near zero; using |forecast| keeps the magnitude
  interpretable as "how far off, relative to the scale of the trend")
"""

import pandas as pd

IN_PATH = "flow_monthly_2025.csv"
OUT_PATH = "forecast_vs_actual_flows.csv"
WINDOW = 3

def build_forecast(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])
    df.sort_values(["category", "month"], inplace=True)

    df["forecast"] = df.groupby("category")["net_flow_billions"].transform(
        lambda s: s.shift(1).rolling(window=WINDOW, min_periods=WINDOW).mean()
    )

    df["variance_vs_forecast"] = df["net_flow_billions"] - df["forecast"]
    df["variance_vs_forecast_pct"] = df["variance_vs_forecast"] / df["forecast"].abs()

    return df

if __name__ == "__main__":
    raw = pd.read_csv(IN_PATH)
    result = build_forecast(raw)
    result.to_csv(OUT_PATH, index=False)

    print(f"Wrote {len(result)} rows to {OUT_PATH}\n")

    valid = result.dropna(subset=["forecast"])
    mape = (valid["variance_vs_forecast"].abs() / valid["net_flow_billions"].abs()).mean() * 100
    print(f"Overall forecast MAPE (trailing 3-month MA): {mape:.1f}%")
    print("(High MAPE is expected here — unlike budget-vs-actual, flow series")
    print(" genuinely swing on market events; that's the whole reason a")
    print(" forecast-deviation signal is useful for flagging surprises.)\n")

    for cat in result["category"].unique():
        sample = result[result["category"] == cat][
            ["month", "net_flow_billions", "forecast", "variance_vs_forecast_pct"]
        ]
        print(f"--- {cat} ---")
        print(sample.to_string(index=False))
        print()
