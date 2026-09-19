import json
from pathlib import Path
import time
from agent.client import AgentClient

def load_scenarios(path="datasets/scenarios.json"):
        import json

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

class ConversationSimulator:

    def __init__(self):
        pass



    def run_scenario(self, scenario):

        # Determine whether this scenario requires
        # simulated integration failure.
        fault_type = None

        if scenario["category"] == "integration":

            fault_map = {
                "tool_timeout": "timeout",
                "tool_error": "tool_error",
                "malformed_response": "malformed",
                "empty_result": "empty",
                "conflicting_data": "conflicting"
            }

            fault_type = fault_map.get(
                scenario.get("subcategory")
            )

        # Create an agent specifically for this scenario.
        agent = AgentClient(
            fault_type=fault_type
        )

        # Run the conversation.
        result = agent.run(
            scenario["conversation"]
        )

        return result

    def run_all(self, scenarios):

        results = []

        for scenario in scenarios:
            print(
                f"Evaluating {scenario['scenario_id']}..."
            )

            result = self.run_scenario(scenario)

            results.append({
                "scenario": scenario,
                "result": result
            })

        return results

    def save_results(self, results, output_path):

        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        serializable_results = []

        for item in results:

            result = item["result"]

            serializable_results.append({
                "scenario": item["scenario"],
                "result": {
                    "response": result.response,
                    "tool_calls": result.tool_calls,
                    "tool_results": result.tool_results,
                    "latency_ms": result.latency_ms,
                    "trajectory": result.trajectory
                }
            })

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                serializable_results,
                f,
                indent=2
            )