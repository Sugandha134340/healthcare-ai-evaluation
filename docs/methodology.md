# Evaluation Methodology

## 1. Scenario execution

Each scenario contains a category, conversation, expected behavior and severity if the behavior fails.

The simulator executes the scenario against the target agent and records a structured result.

## 2. Deterministic evaluation

Where possible, evaluation uses deterministic assertions:

- expected tool selected
- required arguments present
- tool result reflected in final response
- operation succeeded or failed as expected
- unauthorized information was not returned
- required escalation/refusal occurred
- latency threshold

## 3. Qualitative evaluation

An LLM judge may be used for qualitative properties such as response completeness, tone and appropriateness. If used, it must be validated against the human-labelled examples supplied with the assessment.

## 4. Benchmark metrics

Initial metrics:

- Task completion rate
- Tool-call accuracy
- Hallucination rate
- Safety failure rate
- p50 latency
- p95 latency

Metrics are reported separately rather than collapsed into one score.

## 5. Regression testing

A stable golden dataset is run against a baseline. A deliberately degraded prompt/configuration is then evaluated. A regression is reported when a meaningful metric deteriorates or a critical safety failure appears.

## 6. Severity

Findings are classified according to potential healthcare impact. Critical safety failures are kept visible independently of aggregate benchmark performance.
