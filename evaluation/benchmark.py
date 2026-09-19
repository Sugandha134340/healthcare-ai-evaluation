import json
from pathlib import Path

from simulator.runner import (
    ConversationSimulator,
    load_scenarios,
)

from evaluation.evaluator import evaluate_scenario
from evaluation.metrics import calculate_metrics


def serialize_result(result):
    """Convert AgentResult into JSON-serializable data."""

    return {
        "response": result.response,
        "tool_calls": result.tool_calls,
        "tool_results": result.tool_results,
        "latency_ms": result.latency_ms,
        "trajectory": result.trajectory,
    }


def run_benchmark():

    scenarios = load_scenarios()

    simulator = ConversationSimulator()

    evaluated_results = []

    # --------------------------------
    # Run scenarios
    # --------------------------------

    for scenario in scenarios:

        print(
            f"Evaluating {scenario['id']}..."
        )

        result = simulator.run_scenario(
            scenario
        )

        evaluation = evaluate_scenario(
            scenario,
            result
        )

        evaluated_results.append({
            "scenario": scenario,
            "result": result,
            "evaluation": evaluation,
        })

    # --------------------------------
    # Calculate metrics
    # --------------------------------

    metrics = calculate_metrics(
        evaluated_results
    )

    # --------------------------------
    # Print benchmark summary
    # --------------------------------

    print()
    print("=" * 50)
    print("BENCHMARK RESULTS")
    print("=" * 50)

    print(
        f"Total scenarios: "
        f"{metrics['total_scenarios']}"
    )

    print(
        f"Task completion rate: "
        f"{metrics['task_completion_rate']:.2f}%"
    )

    print(
        f"Tool accuracy: "
        f"{metrics['tool_accuracy']:.2f}%"
    )

    print(
        f"Hallucination rate: "
        f"{metrics['hallucination_rate']:.2f}%"
    )

    print(
        f"Safety failure rate: "
        f"{metrics['safety_failure_rate']:.2f}%"
    )

    print(
        f"P95 latency: "
        f"{metrics['p95_latency_ms']:.2f} ms"
    )

    # --------------------------------
    # Save benchmark report
    # --------------------------------

    report = {
        "metrics": metrics,
        "results": [],
    }

    for item in evaluated_results:

        report["results"].append({
            "scenario": item["scenario"],
            "result": serialize_result(
                item["result"]
            ),
            "evaluation": item["evaluation"],
        })

    output_path = Path(
        "reports/benchmark/results.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2
        )

    print()
    print(
        f"Saved benchmark report to "
        f"{output_path}"
    )

    return report


if __name__ == "__main__":
    run_benchmark()