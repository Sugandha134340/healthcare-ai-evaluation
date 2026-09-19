class FaultInjector:
    """
    Simulates external healthcare-tool failures for evaluation.
    """

    def __init__(self, fault_type=None):
        self.fault_type = fault_type

    def apply(self, tool_name, normal_result):
        if not self.fault_type:
            return normal_result

        if self.fault_type == "timeout":
            raise TimeoutError(f"Simulated timeout for {tool_name}")

        if self.fault_type == "tool_error":
            raise RuntimeError(f"Simulated tool error for {tool_name}")

        if self.fault_type == "malformed":
            return {
                "unexpected_field": "invalid tool response",
                "corrupted": True
            }

        if self.fault_type == "empty":
            return {}

        if self.fault_type == "conflicting":
            if isinstance(normal_result, dict):
                result = normal_result.copy()
                result["status"] = "conflicting_status"
                result["conflict"] = True
                return result

            return {
                "result": normal_result,
                "conflict": True
            }

        return normal_result