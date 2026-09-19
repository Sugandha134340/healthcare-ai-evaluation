from simulator.runner import (
    ConversationSimulator,
    load_scenarios,
)


def main():

    scenarios = load_scenarios()

    simulator = ConversationSimulator()

    results = simulator.run_all(
        scenarios
    )

    simulator.save_results(
        results,
        "reports/simulation_results.json"
    )

    print()
    print("=" * 50)
    print("SIMULATION COMPLETE")
    print("=" * 50)
    print(f"Scenarios executed: {len(results)}")
    print(
        "Results saved to "
        "reports/simulation_results.json"
    )


if __name__ == "__main__":
    main()