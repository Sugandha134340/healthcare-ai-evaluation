"""Deterministic evaluation logic.

This will be expanded after the target agent interface is known.
"""


def evaluate(scenario: dict, result: dict) -> dict:
    expected_tool = scenario["expected"].get("primary_tool")
    actual_tools = result.get("actual", {}).get("tool_calls", [])
    actual_tool_names = [
        t.get("name") or t.get("tool") for t in actual_tools
        if isinstance(t, dict)
    ]

    tool_correct = expected_tool in actual_tool_names if expected_tool else True

    return {
        **result,
        "expected_tool": expected_tool,
        "tool_correct": tool_correct,
        "task_completed": None,
        "hallucination": None,
        "safety_failure": None,
    }
