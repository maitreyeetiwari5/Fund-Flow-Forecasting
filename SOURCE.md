# Data source

`flow_monthly_2025.csv` and `flow_annual.csv` are real published figures,
manually transcribed from the Investment Company Institute's **2026
Investment Company Fact Book**, Chapter 3 ("US Mutual Funds"):
https://icifactbook.org/pdf/2026-factbook-ch3.pdf

- Monthly 2025 net new cash flow by category (Equity, Bond, Money Market):
  Figures 3.4, 3.6, 3.12 - billions of USD, rounded as published.
- Annual total industry net new cash flow, 2016-2025: Figure 3.3.
- Annual index mutual fund net new cash flow, 2016-2025: Figure 3.8.

These are industry-wide, not firm-specific - there is no public
company-level "Net New Assets" series available for free, so this
project uses the passive-vs-active industry split as the benchmarking
axis instead of named competitors. That's a legitimate proxy for the
kind of segment-flow-share analysis an NNA analytics team would run,
but it should be described honestly as industry/segment benchmarking,
not competitor-name benchmarking, in interviews.

Two known, documented anomalies are used to seed the event log (see
`flow_event_log.py`):
- July 2025 equity fund outflow of -$367B - the Fact Book footnote
  attributes this to activity in a handful of collective investment
  trusts (CITs), not individual investor redemptions.
- 2025 index fund outflow of -$357B (annual) - same CIT-driven cause,
  per the Figure 3.8 footnote.

Everything else in the pipeline (forecast method, threshold
calibration, flagging, commentary logic) reuses the design from the
top-level project, adapted from a (business_unit, line_item, budget,
actual) schema to a (category, month, actual) schema - there's no
"budget" concept for macro fund flows, so this version forecasts and
flags against trailing-average trend only, not budget variance.
