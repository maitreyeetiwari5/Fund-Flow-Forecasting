"""
Segment benchmarking layer — the "competitor flow analysis" analog
described in the JD, adapted to real, freely available data.

There's no public company-level Net New Assets series, so this uses
industry segments instead of named firms: index (passive) mutual funds
vs. the total industry, both annual, 2016-2025 (ICI Fact Book Figures
3.3 and 3.8). It answers the same underlying question an NNA analyst
asks about named competitors — "who's gaining share of flows, and is
the trend accelerating or reversing" — one level up, at the
active-vs-passive segment instead of the firm level.
"""

import pandas as pd

IN_PATH = "flow_annual.csv"
OUT_PATH = "segment_benchmark.csv"

def benchmark(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values("year")
    df["index_share_of_total_pct"] = (
        df["index_fund_flow_billions"] / df["total_industry_flow_billions"].abs()
    ) * 100
    df["index_flow_yoy_change"] = df["index_fund_flow_billions"].diff()
    df["momentum"] = df["index_flow_yoy_change"].apply(
        lambda x: "accelerating inflow" if x > 20
        else "decelerating / reversing" if x < -20
        else "stable"
    )
    return df

if __name__ == "__main__":
    df = pd.read_csv(IN_PATH)
    result = benchmark(df)
    result.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH}\n")
    print(result[["year", "total_industry_flow_billions", "index_fund_flow_billions",
                   "index_flow_yoy_change", "momentum"]].to_string(index=False))

    print("\nHeadline: index mutual funds swung from +$32B in 2024 to -$357B")
    print("in 2025 — a reversal of nearly $390B — even as investors kept")
    print("pouring into passive vehicles overall via ETFs (Fact Book notes")
    print("equity ETFs took in $956B in 2025). The index MUTUAL FUND wrapper")
    print("specifically lost share, largely on the same CIT-driven activity")
    print("flagged in the July equity anomaly above — a real example of one")
    print("root cause explaining signals across two different views of the")
    print("same data (category-level and segment-level).")
