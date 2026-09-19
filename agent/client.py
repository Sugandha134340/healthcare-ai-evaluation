from agent.fallback_agent import (
    FallbackHealthcareAgent,
    AgentResult,
)


class AgentClient:
    """
    Unified interface for the evaluation framework.

    Currently uses the fallback agent.
    Later this can be replaced with the supplied assessment agent.
    """

    def __init__(self, fault_type=None):
        self.agent = FallbackHealthcareAgent(
            fault_type=fault_type
        )

    def run(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> AgentResult:

        return self.agent.run(
            messages,
            **kwargs,
        )