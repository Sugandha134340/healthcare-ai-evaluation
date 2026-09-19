"""Benchmark metric calculations."""


def percentage(numerator: int, denominator: int) -> float:
    return round((numerator / denominator) * 100, 2) if denominator else 0.0


def task_completion(results):
    return percentage(
        sum(bool(r.get("task_completed")) for r in results),
        len(results),
    )


def tool_accuracy(results):
    return percentage(
        sum(bool(r.get("tool_correct")) for r in results),
        sum(bool(r.get("expected_tool")) for r in results),
    )


def hallucination_rate(results):
    return round(
        sum(bool(r.get("hallucination")) for r in results) / len(results),
        4,
    ) if results else 0.0


def safety_failure_rate(results):
    safety = [r for r in results if r.get("category") == "safety"]
    return round(
        sum(bool(r.get("safety_failure")) for r in safety) / len(safety),
        4,
    ) if safety else 0.0
