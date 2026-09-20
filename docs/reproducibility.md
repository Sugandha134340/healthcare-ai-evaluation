# Reproducibility

## Environment

The evaluation framework is designed to produce repeatable results from the same scenario dataset, agent implementation, evaluator logic, and quality-gate thresholds.

Dependencies are defined in:

```text
requirements.txt
```

## Local Execution

From the repository root:

```bash
pip install -r requirements.txt
```

Run the automated tests:

```bash
pytest -q
```

Run the benchmark:

```bash
python -m evaluation.benchmark
```

Run the quality gate:

```bash
python -m evaluation.quality_gate
```

Run the red-team evaluation:

```bash
python red_team.py
```

Run trajectory evaluation:

```bash
python -m evaluation.trajectory
```

Run monitoring/drift detection:

```bash
python monitoring/drift.py
```

## CI Execution

GitHub Actions runs the automated test suite, benchmark, and quality gate on pushes to `main` and pull requests targeting `main`.

Evaluation reports are uploaded as workflow artifacts even when a later evaluation step fails.

## Determinism

The fallback healthcare agent uses deterministic tool behavior and fixed scenario inputs. This allows evaluation results to be reproduced without requiring a live healthcare backend.

## Quality Gate

The quality gate applies explicit thresholds to benchmark metrics. A failed quality gate indicates that the evaluated agent does not satisfy the configured release criteria.

The evaluation framework reports failures rather than modifying the agent to make the metrics pass.
