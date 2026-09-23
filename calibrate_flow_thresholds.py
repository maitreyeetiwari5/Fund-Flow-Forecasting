"""
Threshold calibration for fund-flow categories — same robust-statistic
approach as the top-level project's calibrate_thresholds.py, adapted
to flag on ABSOLUTE variance ($B) rather than percent variance.

Why absolute instead of percent here: the top-level project's budget
figures are never near zero, so percent variance is stable. Monthly
fund flows routinely cross zero (small forecast, e.g. -$1.3B), so a
percent-of-forecast metric explodes near the zero crossing (a $2B
surprise against a $0.1B forecast reads as 2000%) and would swamp the
calibration with noise unrelated to the anomaly we actually want to
catch. Absolute $ variance avoids that division-by-near-zero problem
and is also just a more natural unit for "how many billions off trend
was this."

new_threshold = median(|variance_$B|) + K * MAD_scaled
"""

import pandas as pd

IN_PATH = "forecast_vs_actual_flows.csv"
OUT_PATH = "flow_threshold_calibration.csv"

K = 2.5

def mad_scaled(series: pd.Series) -> float:
    med = series.median()
    mad = (series - med).abs().median()
    return mad * 1.4826

def calibrate(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for category, grp in df.groupby("category"):
        vf = grp["variance_vs_forecast"].abs().dropna()
        median_abs = vf.median()
        scaled_mad = mad_scaled(grp["variance_vs_forecast"].dropna())
        threshold = median_abs + K * scaled_mad
        rows.append({
            "category": category,
            "median_abs_variance_billions": round(median_abs, 1),
            "mad_scaled_billions": round(scaled_mad, 1),
            "calibrated_threshold_billions": round(threshold, 1),
        })
    return pd.DataFrame(rows).sort_values("category")

if __name__ == "__main__":
    df = pd.read_csv(IN_PATH)
    table = calibrate(df)
    print(table.to_string(index=False))
    table.to_csv(OUT_PATH, index=False)
    print(f"\nWrote {OUT_PATH}")

