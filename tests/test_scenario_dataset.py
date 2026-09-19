import json
from pathlib import Path

def test_scenario_dataset_exists():
    path = Path("datasets/scenarios.json")
    assert path.exists()
    scenarios = json.loads(path.read_text())
    assert len(scenarios) >= 30

def test_required_categories_exist():
    scenarios = json.loads(Path("datasets/scenarios.json").read_text())
    categories = {s["category"] for s in scenarios}
    assert {"functional", "edge_case", "integration", "safety", "adversarial"} <= categories

def test_prompt_injection_exists():
    scenarios = json.loads(Path("datasets/scenarios.json").read_text())
    assert any(s["id"] == "A001" for s in scenarios)
