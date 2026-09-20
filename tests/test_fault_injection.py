from agent.client import AgentClient


def test_timeout_is_detected():
    client = AgentClient(fault_type="timeout")

    result = client.run([
        {
            "role": "user",
            "message": "Check availability with Dr. Rao tomorrow."
        }
    ])

    assert result.tool_results
    assert result.tool_results[0]["result"]["success"] is False
    assert "timeout" in result.tool_results[0]["result"]["error"].lower()


def test_tool_error_is_detected():
    client = AgentClient(fault_type="tool_error")

    result = client.run([
        {
            "role": "user",
            "message": "Book an appointment with Dr. Rao tomorrow."
        }
    ])

    assert result.tool_results
    assert result.tool_results[0]["result"]["success"] is False
    assert "tool error" in result.tool_results[0]["result"]["error"].lower()


def test_malformed_response_is_detected():
    client = AgentClient(fault_type="malformed")

    result = client.run([
        {
            "role": "user",
            "message": "Check availability with Dr. Rao tomorrow."
        }
    ])

    assert result.tool_results
    tool_result = result.tool_results[0]["result"]

    assert tool_result.get("corrupted") is True
    assert "unexpected_field" in tool_result


def test_empty_response_is_detected():
    client = AgentClient(fault_type="empty")

    result = client.run([
        {
            "role": "user",
            "message": "Check availability with Dr. Rao tomorrow."
        }
    ])

    assert result.tool_results
    assert result.tool_results[0]["result"] == {}


def test_conflicting_response_is_detected():
    client = AgentClient(fault_type="conflicting")

    result = client.run([
        {
            "role": "user",
            "message": "Check availability with Dr. Rao tomorrow."
        }
    ])

    assert result.tool_results
    tool_result = result.tool_results[0]["result"]

    assert tool_result.get("conflict") is True
    assert tool_result.get("status") == "conflicting_status"