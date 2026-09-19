from agent.client import AgentClient


def test_booking_regression():
    client = AgentClient()

    result = client.run([
        {
            "role": "user",
            "message": "I want to book an appointment with Dr. Rao tomorrow."
        }
    ])

    tool_names = [
        call["name"]
        for call in result.tool_calls
    ]

    assert "book_appointment" in tool_names


def test_cancellation_regression():
    client = AgentClient()

    result = client.run([
        {
            "role": "user",
            "message": "Cancel my appointment A001."
        }
    ])

    tool_names = [
        call["name"]
        for call in result.tool_calls
    ]

    assert "cancel_appointment" in tool_names


def test_rescheduling_regression():
    client = AgentClient()

    result = client.run([
        {
            "role": "user",
            "message": "Reschedule my appointment A001 to tomorrow."
        }
    ])

    tool_names = [
        call["name"]
        for call in result.tool_calls
    ]

    assert "reschedule_appointment" in tool_names