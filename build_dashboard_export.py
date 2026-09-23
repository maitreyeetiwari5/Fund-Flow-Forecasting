"""
Consolidates the pipeline's separate CSVs into two clean, dashboard-ready
tables for Tableau Public / Power BI:

- dashboard_export_monthly.csv: one row per (category, month) with
  actual, forecast, variance, threshold, flagged, and commentary all
  joined together — no need to blend multiple files in Tableau.
- dashboard_export_annual.csv: the segment benchmark table, renamed/
  cleaned for BI import (same data as segment_benchmark.csv).
"""

import pandas as pd

def build_monthly_export():
    forecast = pd.read_csv("forecast_vs_actual_flows.csv")
    flagged = pd.read_csv("flagged_flow_variances.csv")
    commentary = pd.read_csv("flow_commentary_draft.csv")

    df = flagged.copy()  # already has forecast + variance + flagged + flag_reason
    df = df.merge(
        commentary[["category", "month", "commentary", "has_known_driver"]],
        on=["category", "month"], how="left"
    )

    df["commentary"] = df["commentary"].fillna("")
    df["has_known_driver"] = df["has_known_driver"].fillna(False)
    df["month"] = pd.to_datetime(df["month"])

    df = df.rename(columns={
        "net_flow_billions": "actual_flow_billions",
        "forecast": "forecast_flow_billions",
        "variance_vs_forecast": "variance_billions",
    })

    cols = [
        "category", "month", "actual_flow_billions", "forecast_flow_billions",
        "variance_billions", "calibrated_threshold_billions", "flagged",
        "flag_reason", "commentary", "has_known_driver",
    ]
    df = df[cols].sort_values(["category", "month"])
    df.to_csv("dashboard_export_monthly.csv", index=False)
    print(f"Wrote dashboard_export_monthly.csv ({len(df)} rows)")

def build_annual_export():
    df = pd.read_csv("segment_benchmark.csv")
    df = df.rename(columns={
        "total_industry_flow_billions": "industry_total_flow_billions",
        "index_fund_flow_billions": "index_fund_flow_billions",
        "index_flow_yoy_change": "index_flow_yoy_change_billions",
    })
    df.to_csv("dashboard_export_annual.csv", index=False)
    print(f"Wrote dashboard_export_annual.csv ({len(df)} rows)")

if __name__ == "__main__":
    build_monthly_export()
    build_annual_export()
