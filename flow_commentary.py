"""
Auto-drafts commentary for flagged flow months. Same design as the
top-level commentary.py: state the driver only if it's on file in the
event log, otherwise draft an objective description and route for
analyst review rather than guessing.
"""

import pandas as pd
from flow_event_log import load_event_log

FLAGGED_PATH = "flagged_flow_variances.csv"
OUT_PATH = "flow_commentary_draft.csv"

def format_month(m: str) -> str:
    return pd.to_datetime(m).strftime("%B %Y")

def build_commentary(row, event_log: pd.DataFrame) -> str:
    match = event_log[
        (event_log["category"] == row["category"])
        & (event_log["month"] == pd.to_datetime(row["month"]).strftime("%Y-%m"))
    ]
    month_str = format_month(row["month"])
    base = f"{row['category']} net flow was {row['flag_reason']} in {month_str}."
    if len(match) > 0:
        return f"{base} Driver: {match.iloc[0]['driver']}."
    return f"{base} Driver: pending analyst review — no known one-off cause on file."

def generate(flagged: pd.DataFrame) -> pd.DataFrame:
    event_log = load_event_log()
    flagged = flagged[flagged["flagged"]].copy()
    flagged["commentary"] = flagged.apply(lambda r: build_commentary(r, event_log), axis=1)
    flagged["has_known_driver"] = flagged["commentary"].apply(
        lambda c: "pending analyst review" not in c
    )
    return flagged

if __name__ == "__main__":
    flagged = pd.read_csv(FLAGGED_PATH)
    result = generate(flagged)
    cols = ["category", "month", "commentary", "has_known_driver"]
    result[cols].to_csv(OUT_PATH, index=False)

    print(f"Wrote {len(result)} commentary rows to {OUT_PATH}\n")
    known = result["has_known_driver"].sum()
    print(f"{known} of {len(result)} flagged rows matched a known driver "
          f"({known/len(result):.0%}) — the rest routed for analyst review.\n")
    for _, r in result.iterrows():
        print(f"- {r['commentary']}")
