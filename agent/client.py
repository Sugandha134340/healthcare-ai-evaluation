"""Normalized target-agent adapter.

Replace the implementation once the supplied healthcare AI agent is received.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    response: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    latency_ms: float = 0.0
    trajectory: list[dict[str, Any]] = field(default_factory=list)


class AgentClient:
    def run(self, messages: list[dict[str, str]], **kwargs) -> AgentResult:
        raise NotImplementedError("Connect the supplied healthcare AI agent here.")
