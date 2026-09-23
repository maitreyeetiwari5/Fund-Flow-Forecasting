"""
Event log adapted for fund flows. Unlike the top-level project's
scripted/synthetic events, this one entry is a REAL, documented driver
sourced from the ICI Fact Book footnote (see SOURCE.md) — not invented
for the demo. Everything else flagged with no matching entry here is
honestly routed to "pending analyst review," same principle as the
original project.
"""

import pandas as pd

EVENT_LOG = [
    {"category": "Equity", "month": "2025-07",
     "driver": "ICI Fact Book: outflow driven by activity in a handful of "
               "collective investment trusts (CITs), not individual investor "
               "redemptions (Fig. 3.4 footnote)"},
]

def load_event_log() -> pd.DataFrame:
    return pd.DataFrame(EVENT_LOG)
