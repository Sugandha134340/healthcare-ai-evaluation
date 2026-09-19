"""Benchmark metric calculations."""

import math


def percentage(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0

    return round((numerator / denominator) * 100, 2)


def task_completion(results):
    values = [
        r["evaluation"]["task_completed"]
        for r in results
        if r["evaluation"].get("task_completed") is not None
    ]

    return percentage(
        sum(bool(v) for v in values),
        len(values),
    )


def tool_accuracy(results):
    values = [
        r["evaluation"]["tool_correct"]
        for r in results
        if r["evaluation"].get("tool_correct") is not None
    ]

    return percentage(
        sum(bool(v) for v in values),
        len(values),
    )


def hallucination_rate(results):
    if not results:
        return 0.0

    hallucinations = sum(
        bool(r["evaluation"].get("hallucination"))
        for r in results
    )

    return percentage(hallucinations, len(results))


def safety_failure_rate(results):
    safety_results = [
        r["evaluation"]["safety_pass"]
        for r in results
        if r["evaluation"].get("safety_pass") is not None
    ]

    if not safety_results:
        return 0.0

    failures = sum(
        not bool(result)
        for result in safety_results
    )

    return percentage(failures, len(safety_results))


def p95_latency(results):
    latencies = [
        r["result"].latency_ms
        for r in results
        if hasattr(r["result"], "latency_ms")
    ]

    if not latencies:
        return 0.0

    latencies.sort()

    index = max(
        0,
        math.ceil(0.95 * len(latencies)) - 1
    )

    return round(latencies[index], 2)


def calculate_metrics(results):
    """Calculate all benchmark metrics."""

    return {
        "total_scenarios": len(results),
        "task_completion_rate": task_completion(results),
        "tool_accuracy": tool_accuracy(results),
        "hallucination_rate": hallucination_rate(results),
        "safety_failure_rate": safety_failure_rate(results),
        "p95_latency_ms": p95_latency(results),
    }