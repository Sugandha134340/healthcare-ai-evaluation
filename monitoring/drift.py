"""Metric drift detection for healthcare-agent evaluation."""

import json
from pathlib import Path


DEFAULT_THRESHOLDS = {
    "task_completion_rate": 5.0,
    "tool_accuracy": 5.0,
    "hallucination_rate": 2.0,
    "safety_failure_rate": 2.0,
}


def load_metrics(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_drift(baseline, current, thresholds=None):
    thresholds = thresholds or DEFAULT_THRESHOLDS
    alerts = []

    for metric, threshold in thresholds.items():
        if metric not in baseline or metric not in current:
            continue

        baseline_value = float(baseline[metric])
        current_value = float(current[metric])
        delta = current_value - baseline_value

        # For completion/accuracy, a decrease is degradation.
        if metric in {"task_completion_rate", "tool_accuracy"}:
            if delta <= -threshold:
                alerts.append({
                    "metric": metric,
                    "baseline": baseline_value,
                    "current": current_value,
                    "delta": round(delta, 2),
                    "threshold": threshold,
                    "severity": "high",
                    "message": f"{metric} decreased beyond threshold",
                })

        # For failure/error rates, an increase is degradation.
        elif metric in {"hallucination_rate", "safety_failure_rate"}:
            if delta >= threshold:
                alerts.append({
                    "metric": metric,
                    "baseline": baseline_value,
                    "current": current_value,
                    "delta": round(delta, 2),
                    "threshold": threshold,
                    "severity": "high",
                    "message": f"{metric} increased beyond threshold",
                })

    return alerts


def save_alerts(alerts, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "drift_detected": bool(alerts),
        "alert_count": len(alerts),
        "alerts": alerts,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return payload


if __name__ == "__main__":
    baseline_path = "reports/monitoring/baseline_metrics.json"
    current_path = "reports/monitoring/current_metrics.json"
    output_path = "reports/monitoring/drift_alert.json"

    baseline = load_metrics(baseline_path)
    current = load_metrics(current_path)

    alerts = detect_drift(baseline, current)
    result = save_alerts(alerts, output_path)

    if result["drift_detected"]:
        print("DRIFT ALERT")
        for alert in alerts:
            print(
                f"- {alert['metric']}: "
                f"{alert['baseline']} -> {alert['current']} "
                f"(delta={alert['delta']})"
            )
    else:
        print("No metric drift detected.")