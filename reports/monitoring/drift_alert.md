# Monitoring and Drift Alert Demonstration

## Purpose

The evaluation framework includes metric monitoring to detect degradation between
an established benchmark baseline and a subsequent evaluation snapshot.

This demonstration uses the measured benchmark metrics as the baseline and a
separately created degraded snapshot to verify that the alerting mechanism works.

## Baseline

The baseline was produced by the 30-scenario benchmark:

| Metric | Baseline |
|---|---:|
| Task completion rate | 38.89% |
| Tool accuracy | 50.00% |
| Hallucination rate | 0.00% |
| Safety failure rate | 16.67% |
| P95 latency | 0.03 ms |

## Demonstration Snapshot

The following values are intentionally degraded for testing the monitoring logic:

| Metric | Demonstration |
|---|---:|
| Task completion rate | 30.00% |
| Tool accuracy | 40.00% |
| Hallucination rate | 0.00% |
| Safety failure rate | 20.00% |
| P95 latency | 0.04 ms |

These values are simulated monitoring input and are not production measurements.

## Alert Thresholds

| Metric | Alert condition |
|---|---|
| Task completion rate | decrease >= 5 percentage points |
| Tool accuracy | decrease >= 5 percentage points |
| Hallucination rate | increase >= 2 percentage points |
| Safety failure rate | increase >= 2 percentage points |

## Result

The monitoring script detected drift in:

- Task completion rate: -8.89 percentage points
- Tool accuracy: -10.00 percentage points
- Safety failure rate: +3.33 percentage points

No hallucination-rate alert was generated because the demonstration value
remained unchanged.

## Reproducibility

Run:

```bash
python monitoring/drift.py