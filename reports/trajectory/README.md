# Agent Trajectory Evaluation

## Purpose

This evaluation inspects the agent's internal execution trajectory rather than
only its final response.

The evaluator checks:

1. Expected tool selection
2. Actual tool calls
3. Unauthorized state-changing actions
4. Safety/refusal behavior where expected
5. Number of trajectory steps
6. Recorded trajectory evidence

## Why trajectory evaluation matters

A final response can appear reasonable even when the underlying execution path
is incorrect. For example, an agent may report success after calling the wrong
tool or after receiving an invalid tool result.

Trajectory evaluation exposes those execution-level failures.

## Reproduction

Run:

```bash
python evaluation/trajectory.py
```

The machine-readable report is written to:

```text
reports/trajectory/trajectory_results.json
```

## Interpretation

A trajectory pass means the recorded execution satisfies the deterministic
checks implemented by this evaluator. A failure identifies a trajectory-level
behavior requiring investigation.

This evaluator is intentionally deterministic and does not claim to provide
complete agent reasoning or security coverage. It evaluates only the observable
trajectory fields captured by the fallback agent.
