import pytest

from agent.client import AgentClient


def test_timeout_is_detected():
    client = AgentClient(fault_type="timeout")

    result = client.run(
        "Check availability with Dr. Rao tomorrow."
    )

    assert result is not None
    assert len(result.tool_calls) > 0


def test_tool_error_is_detected():
    client = AgentClient(fault_type="tool_error")

    result = client.run(
        "Book an appointment with Dr. Rao tomorrow."
    )

    assert result is not None


def test_malformed_response_is_detected():
    client = AgentClient(fault_type="malformed")

    result = client.run(
        "Check availability with Dr. Rao tomorrow."
    )

    assert result is not None


def test_empty_response_is_detected():
    client = AgentClient(fault_type="empty")

    result = client.run(
        "Check availability with Dr. Rao tomorrow."
    )

    assert result is not None


def test_conflicting_response_is_detected():
    client = AgentClient(fault_type="conflicting")

    result = client.run(
        "Check availability with Dr. Rao tomorrow."
    )

    assert result is not None