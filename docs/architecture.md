# Evaluation Architecture

```text
Scenario Dataset
      |
      v
Conversation Simulator
      |
      v
Agent Adapter
   |       |
   |       +--> Fallback Agent (temporary)
   |
   +----------> Supplied Healthcare Agent (when provided)
      |
      v
Responses + Tool Calls + Latency
      |
      v
Evaluation Engine
   |       |       |
   v       v       v
Functional Safety Integration
Testing    Testing Testing
      |
      v
Benchmark Pipeline
      |
      v
Golden Dataset / Regression
      |
      v
Monitoring + Quality Drift Alert
      |
      v
Findings + Root Cause Analysis
      |
      v
Quality Gates
```

## Design principle

The target agent is accessed through an adapter interface. This prevents the evaluation framework from depending on a particular implementation.

The adapter will expose a normalized result containing:

- conversation messages
- tool calls
- tool results
- final response
- latency
- optional trajectory information

This allows the same scenarios and evaluation logic to work with the supplied agent or a temporary fallback implementation.
