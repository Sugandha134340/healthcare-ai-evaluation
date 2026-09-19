"""Conversation simulator entry point."""

import json
from pathlib import Path
from agent.client import AgentClient


def load_scenarios(path: str = "datasets/scenarios.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class ConversationSimulator:
    def __init__(self, agent: AgentClient):
        self.agent = agent

    def run(self, scenario: dict):
        result = self.agent.run(scenario["conversation"])
        return {
            "scenario_id": scenario["id"],
            "category": scenario["category"],
            "expected": scenario["expected"],
            "actual": {
                "response": result.response,
                "tool_calls": result.tool_calls,
                "tool_results": result.tool_results,
            },
            "latency_ms": result.latency_ms,
            "trajectory": result.trajectory,
        }
