# RCA-001: Incorrect Intent Routing

## Finding
**Finding ID:** FIND-001
**Severity:** Medium
**Affected scenarios:** F005, I004

## Observed Behavior
- F005 (doctor information) invoked `check_availability` instead of `get_doctor_information`.
- I004 (empty tool result) also routed to `check_availability` instead of the expected doctor-information workflow.

## Expected Behavior
The agent should identify the user's requested task and invoke the corresponding healthcare tool. Doctor-information requests should route to `get_doctor_information`.

## Root Cause
The evaluation evidence indicates an intent-routing gap: the agent selected an availability workflow for requests whose expected workflow was doctor information.

## Impact
Incorrect routing can produce irrelevant information and prevents the requested task from being completed reliably. In a healthcare workflow, this can also create misleading user expectations about what information was retrieved.

## Evidence
Benchmark evaluation recorded:
- F005: `tool_correct=False`, `task_completed=True`.
- I004: `tool_correct=False`, `task_completed=False`.

## Recommended Remediation
1. Strengthen intent classification and tool-selection rules for doctor-information requests.
2. Add explicit negative examples distinguishing doctor information from appointment availability.
3. Add regression tests that assert the expected tool for each supported intent.
4. Add evaluation cases for closely related intents.

## Regression Recommendation
Assert that doctor-information prompts invoke `get_doctor_information` and do not invoke `check_availability`.

## Status
Open — evaluation finding; no agent remediation applied.
