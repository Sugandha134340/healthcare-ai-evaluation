# RCA-002: Missing Input and Ambiguity Handling

## Finding
**Finding ID:** FIND-002
**Severity:** High
**Affected scenarios:** F006, F008, E001, E002, E003, E004

## Observed Behavior
The agent attempted workflows despite missing, ambiguous, or contradictory information:
- F006: appointment lookup did not invoke the expected appointment-lookup tool.
- F008: duplicate-booking scenario proceeded with a booking.
- E001: missing date resulted in a doctor-information call.
- E002: missing doctor resulted in a booking attempt.
- E003: ambiguous request resulted in doctor-information retrieval.
- E004: contradictory request resulted in a booking attempt.

## Expected Behavior
The agent should identify required missing information, ambiguity, or contradiction before executing an appointment action. When information is insufficient, it should ask a clarification question or safely decline the action rather than inventing or assuming missing values.

## Root Cause
The evaluation evidence indicates insufficient input-validation and ambiguity-resolution logic before tool execution.

## Impact
This can cause incorrect appointments, unintended state changes, and poor conversational reliability.

## Evidence
Benchmark evaluation marked all six affected scenarios as failures. The affected scenarios collectively contributed substantially to the observed task-completion and tool-accuracy gaps.

## Recommended Remediation
1. Define required parameters for each appointment operation.
2. Validate required parameters before calling tools.
3. Detect ambiguous or contradictory user requests.
4. Ask targeted clarification questions when required information is missing.
5. Add negative tests to ensure appointment-changing tools are not called with incomplete inputs.

## Regression Recommendation
For each required appointment parameter, include a missing-parameter test and assert that no state-changing appointment tool is invoked until the information is supplied.

## Status
Open — evaluation finding; no agent remediation applied.
