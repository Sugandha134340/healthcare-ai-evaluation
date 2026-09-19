# Healthcare AI Evaluation & Quality Engineering

Evaluation and quality-engineering framework for a healthcare voice/LLM agent.

## Objective

Determine whether a healthcare AI agent is behaving correctly, consistently, safely and reliably enough for release.

## Selected healthcare context

Adinath-Jagtap/hospital-management-system:
https://github.com/Adinath-Jagtap/hospital-management-system

See `docs/project-selection.md`.

## Current status

The supplied target agent was not included with the project requirements received so far. The framework therefore uses an adapter boundary so the supplied agent can be connected later. A clearly labelled fallback agent can be used to demonstrate the evaluation infrastructure if the target agent is not provided.

## Structure

- `datasets/` — scenarios and golden regression dataset
- `simulator/` — reusable conversation execution
- `agent/` — target-agent adapter
- `evaluation/` — metrics, judges, benchmark and regression logic
- `tests/` — automated functional, edge, integration, safety and adversarial tests
- `monitoring/` — dashboard and alerts
- `reports/` — benchmark, findings and RCA artifacts
- `docs/` — methodology and reproducibility documentation

## Planned commands

```bash
pip install -r requirements.txt
pytest
streamlit run monitoring/dashboard.py
```

## Required final demonstration

1. Selected healthcare project
2. Evaluation architecture
3. Automated tests
4. Conversation simulation
5. Benchmark
6. Failure discovery
7. Tool failure
8. Regression detection
9. Quality-drift alert
10. Root-cause analysis
