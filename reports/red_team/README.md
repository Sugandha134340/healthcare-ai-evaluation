# AI Red-Team Evaluation Report

## Purpose

This evaluation exercises the healthcare agent with adversarial prompts designed
to test instruction resistance, scope preservation, tool-use safety, and
authorization handling.

The red-team suite contains five scenarios:

- A001 — prompt injection
- A002 — instruction override
- A003 — jailbreak
- A004 — tool manipulation
- A005 — scope manipulation

## Method

Each adversarial scenario is replayed through the same `AgentClient` used by the
benchmark. The evaluator records:

- agent response
- tool calls
- trajectory
- scenario-specific safety checks
- pass/fail verdict

A red-team pass means the observed behavior satisfies the checks defined for
that attack. A failed attack is treated as an evaluation finding.

## Reproduction

Run:

```bash
python red_team.py
```

The machine-readable result is written to:

```text
reports/red_team/red_team_results.json
```

## Interpretation

The red-team evaluation is intentionally separate from the general benchmark.
This makes adversarial behavior visible as its own quality dimension and allows
future attack cases to be added without changing the core benchmark.

The results should be interpreted together with the safety findings in the
benchmark and findings register. In particular, authorization and privacy
failures should be treated as high-risk findings even when the overall
adversarial pass rate is high.

## Limitations

This is a deterministic adversarial test suite rather than an exhaustive
security assessment. It does not establish that the agent is secure against
all prompt-injection, jailbreak, or tool-manipulation techniques.

The suite should be expanded with additional attack variants as the agent,
tools, and healthcare workflows evolve.
