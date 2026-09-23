# Fund Flow Forecasting & Segment Benchmarking

An extension of the top-level [Finance Forecast & Variance Automation project](https://github.com/maitreyeetiwari5/FPA-Variance-Automation) - same forecast/calibration/commentary architecture, retargeted from budget-vs-actual data to real US mutual fund industry net-flow data, plus a new segment-benchmarking layer.

**[Live dashboard](https://public.tableau.com/app/profile/maitreyee.tiwari4070/viz/FundFlowForecastingSegmentBenchmarking/FundFlowForecastingSegmentBenchmarking?publish=yes)** - flow vs. forecast trends by category, flagged-anomaly detail with drafted commentary, and the active-vs-passive segment benchmark, all on one dashboard.

## Problem

An NNA (Net New Assets) analytics function forecasts flows, flags surprises, and explains what drove them, on a recurring cadence, across categories, for senior stakeholders. That's a real, ongoing FP&A-style problem, but it needs real flow data to build against, not another synthetic dataset. There's no free firm-level NNA data, so this project uses real published US mutual fund industry data instead, and is honest about that substitution rather than papering over it.

## Data

Real figures transcribed from the ICI 2026 Investment Company Fact Book. See [`SOURCE.md`](SOURCE.md) for exact figures/citations and an honest note on what's a direct substitute vs. an adapted proxy (in particular: segment benchmarking instead of named-competitor benchmarking, since there's no free company-level NNA data).

## Pipeline

Run in order (from this directory):

| Step | Script | Output |
| --- | --- | --- |
| 1 | `forecast_flows.py` | `forecast_vs_actual_flows.csv` - trailing 3-month moving-average forecast per category |
| 2 | `calibrate_flow_thresholds.py` | `flow_threshold_calibration.csv` - robust (median + MAD) $ thresholds per category |
| 3 | `flag_flow_variances.py` | `flagged_flow_variances.csv` - months that breached their calibrated threshold |
| 4 | `flow_commentary.py` (+ `flow_event_log.py`) | `flow_commentary_draft.csv` - drafted commentary; known driver pulled from the event log, unknowns routed for analyst review |
| 5 | `benchmark_segments.py` | `segment_benchmark.csv` - active vs. passive annual flow-share trend |
| 6 | `build_dashboard_export.py` | `dashboard_export_monthly.csv`, `dashboard_export_annual.csv` - joined, dashboard-ready tables used by the Tableau dashboard above |

```bash
python forecast_flows.py
python calibrate_flow_thresholds.py
python flag_flow_variances.py
python flow_commentary.py
python benchmark_segments.py
python build_dashboard_export.py
```

## Key design choices

- **Forecast method:** the same trailing 3-month moving average as the top-level project, for the same reason, any analyst can reconstruct the number by hand.
- **Threshold calibration:** thresholds are learned per category from historical variance (median + scaled MAD), same as the top-level project, but calibrated on absolute $ variance rather than percent. Flow series cross zero monthly, so percent-of-forecast blows up near zero and would swamp calibration with noise.
- **Commentary generation:** the tool never invents a cause for a flagged variance. It checks a known-events log and states the driver only when one is on file, otherwise it drafts an objective description and marks it "pending analyst review" - same discipline as the top-level project, tested here on real anomalies instead of scripted ones.
- **Benchmarking scope:** done at the market-segment level (active vs. passive mutual funds), not named competitors, since firm-level NNA data isn't publicly available for free. See `SOURCE.md` for the honest framing to use if this comes up in an interview.

## Results (2025 monthly, 3 categories = 36 data points, 27 scoreable)

- 2 of 27 scoreable months flagged (7.4%), thresholds calibrated per category from each series' own historical variance, not a flat rule
- 1 of 2 flagged months matched a documented driver (July equity outflow, CIT-driven per Fact Book footnote); the other (April bond outflow) had no matching event on file and was honestly routed for analyst review rather than guessed at
- Segment benchmarking found index mutual funds swung from +$32B (2024) to -$357B (2025), a ~$390B reversal, while the broader industry moved differently over the same period, pointing to a fund-wrapper-level shift rather than a simple passive-vs-active demand reversal

## Stack

Python (pandas) for the forecast/calibration/commentary/benchmarking pipeline. Tableau Public for the published dashboard.

## What's different from the top-level project (and why)

- No "budget" concept exists for macro fund flows, so this version flags on forecast deviation only, not budget variance.
- Thresholds are calibrated on absolute $ variance, not percent, for the reason above.
- The event log here is seeded with one real, documented driver sourced from an ICI Fact Book footnote, not a scripted/synthetic event.

## Note on the data

All figures are real, published industry data, see `SOURCE.md` for exact sources and page/figure references. Nothing here is synthetic or simulated.
