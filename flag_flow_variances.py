"""
Flags months where a category's actual flow breached its calibrated
absolute-$ threshold vs. trailing forecast. Adapted from controls.py.
"""

import pandas as pd

FORECAST_PATH = "forecast_vs_actual_flows.csv"
THRESHOLDS_PATH = "flow_threshold_calibration.csv"
OUT_PATH = "flagged_flow_variances.csv"

def flag_variances(df: pd.DataFrame, thresholds: pd.DataFrame) -> pd.DataFrame:
    df = df.merge(thresholds[["category", "calibrated_threshold_billions"]], on="category")
    df["flagged"] = (
        df["variance_vs_forecast"].notna()
        & (df["variance_vs_forecast"].abs() > df["calibrated_threshold_billions"])
    )

    def reason(row):
        if not row["flagged"]:
            return ""
        direction = "above" if row["variance_vs_forecast"] > 0 else "below"
        return (
            f"${abs(row['variance_vs_forecast']):.0f}B {direction} trend forecast "
            f"(threshold: ${row['calibrated_threshold_billions']:.0f}B)"
        )

    df["flag_reason"] = df.apply(reason, axis=1)
    return df

if __name__ == "__main__":
    forecast_df = pd.read_csv("forecast_vs_actual_flows.csv")
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)
    result = flag_variances(forecast_df, thresholds_df)
    result.to_csv(OUT_PATH, index=False)

    flagged = result[result["flagged"]]
    n_scored = result["variance_vs_forecast"].notna().sum()
    print(f"Wrote {len(result)} rows to {OUT_PATH}")
    print(f"{len(flagged)} of {n_scored} scoreable rows flagged ({len(flagged)/n_scored:.1%})\n")
    print(flagged[["category", "month", "net_flow_billions", "forecast", "flag_reason"]].to_string(index=False))
