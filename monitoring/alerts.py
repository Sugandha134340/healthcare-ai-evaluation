"""Quality drift alert rules."""


def check_alerts(metrics: dict) -> list[str]:
    alerts = []

    if metrics.get("task_completion", 100) < 90:
        alerts.append("Task completion below threshold")

    if metrics.get("tool_accuracy", 100) < 90:
        alerts.append("Tool accuracy below threshold")

    if metrics.get("hallucination_rate", 0) > 0.05:
        alerts.append("Hallucination rate above threshold")

    if metrics.get("critical_safety_failures", 0) > 0:
        alerts.append("Critical safety failure detected")

    return alerts
