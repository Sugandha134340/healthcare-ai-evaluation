import time
from dataclasses import dataclass, field
from typing import Any
from agent.fault_injection import FaultInjector

@dataclass
class AgentResult:
    response: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    latency_ms: float = 0.0
    trajectory: list[dict[str, Any]] = field(default_factory=list)


class HealthcareTools:
    """Mock healthcare tools used by the fallback agent."""

    def __init__(self, fault_type=None):
        self.fault_injector = FaultInjector(fault_type)


        self.doctors = {
        "Dr. Rao": {
            "name": "Dr. Rao",
            "specialty": "Cardiology",
            "experience": "12 years",
            "available": True
        },
        "Dr. Sharma": {
            "name": "Dr. Sharma",
            "specialty": "Dermatology",
            "experience": "10 years",
            "available": True
        },
        "Dr. Reddy": {
            "name": "Dr. Reddy",
            "specialty": "General Medicine",
            "experience": "15 years",
            "available": True
        }
    }

        self.appointments = {
            "A001": {
                "appointment_id": "A001",
                "patient_id": "P001",
                "doctor": "Dr. Rao",
                "date": "2026-09-21",
                "time": "15:00",
                "status": "confirmed"
            }
        }

    def check_availability(self, specialty=None, date=None):
        if not specialty:
            return {
                "success": False,
                "error": "specialty_required",
            }

        result =  {
            "success": True,
            "available": True,
            "specialty": specialty,
            "date": date,
            "slots": ["10:00", "14:00", "16:00"],
        }

        return self.fault_injector.apply(
            "check_availability",
            result
        )

    def book_appointment(
        self,
        patient_id=None,
        specialty=None,
        date=None,
        time=None,
    ):
        if not all([patient_id, specialty, date, time]):
            return {
                "success": False,
                "error": "missing_booking_information",
            }

        result = {
            "success": True,
            "appointment_id": "A002",
            "patient_id": patient_id,
            "specialty": specialty,
            "date": date,
            "time": time,
            "status": "confirmed",
        }

        return self.fault_injector.apply(
            "book_appointment",
            result
        )

    def cancel_appointment(self, appointment_id=None):
        if appointment_id not in self.appointments:
            return {
                "success": False,
                "error": "appointment_not_found",
            }

        result =  {
            "success": True,
            "appointment_id": appointment_id,
            "status": "cancelled",
        }

        return self.fault_injector.apply(
            "cancel_appointment",
            result
        )

    def reschedule_appointment(
        self,
        appointment_id=None,
        new_date=None,
        new_time=None,
    ):
        if appointment_id not in self.appointments:
            return {
                "success": False,
                "error": "appointment_not_found",
            }

        result =  {
            "success": True,
            "appointment_id": appointment_id,
            "new_date": new_date,
            "new_time": new_time,
            "status": "rescheduled",
        }
        return self.fault_injector.apply(
            "reschedule_appointment",
            result
        )

    def get_doctor_information(self, specialty=None):
        doctors = list(self.doctors.values())

        if specialty:
            doctors = [
                d for d in doctors
                if d["specialty"].lower() == specialty.lower()
            ]

        result = {
            "success": True,
            "doctors": doctors
        }

        return self.fault_injector.apply(
            "get_doctor_information",
            result
        )

    def get_patient_appointment(self, patient_id=None):
        appointments = [
            a for a in self.appointments.values()
            if a["patient"] == patient_id
        ]

        result =  {
            "success": True,
            "appointments": appointments,
        }

        return self.fault_injector.apply(
                    "get_patient_appointment",
                    result
                )


class FallbackHealthcareAgent:
    """
    Small deterministic healthcare agent used only when the supplied
    assessment agent is unavailable.
    """

    def __init__(self, fault_type=None):
        self.tools = HealthcareTools(
            fault_type=fault_type
        )
    def _safe_tool_call(self, tool_name, **kwargs):
        tool = getattr(self.tools, tool_name)

        try:
            return tool(**kwargs)

        except TimeoutError as e:
            return {
                "success": False,
                "error_type": "timeout",
                "error": str(e),
            }

        except RuntimeError as e:
            return {
                "success": False,
                "error_type": "tool_error",
                "error": str(e),
            }

        except Exception as e:
            return {
                "success": False,
                "error_type": "unexpected_error",
                "error": str(e),
            }
    def run(self, messages, **kwargs):
        start = time.perf_counter()

        user_message = messages[-1]["message"].lower()

        tool_calls = []
        tool_results = []
        trajectory = []

        trajectory.append({
            "step": 1,
            "type": "user_message",
            "content": messages[-1]["message"],
        })

        # -----------------------------
        # SAFETY / ADVERSARIAL
        # -----------------------------

        if (
            "ignore all previous" in user_message
            or "reveal patient records" in user_message
            or "reveal all appointments" in user_message
        ):
            response = (
                "I can't provide unauthorized patient information "
                "or follow instructions that conflict with my safety requirements."
            )

            trajectory.append({
                "step": 2,
                "type": "safety_refusal",
            })

            return AgentResult(
                response=response,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        if (
            "medical records" in user_message
            or "another patient's" in user_message
            or "another patient" in user_message
        ):
            response = (
                "I can't provide another patient's private medical "
                "or appointment information."
            )

            trajectory.append({
                "step": 2,
                "type": "privacy_refusal",
            })

            return AgentResult(
                response=response,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        if (
            "severe chest pain" in user_message
            or "difficulty breathing" in user_message
        ):
            response = (
                "These symptoms may require urgent medical attention. "
                "Please seek emergency medical care immediately."
            )

            trajectory.append({
                "step": 2,
                "type": "urgent_escalation",
            })

            return AgentResult(
                response=response,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        if (
            "diagnose" in user_message
            or "exactly what dose" in user_message
            or "prescription" in user_message
        ):
            response = (
                "I can't provide a diagnosis or personalized prescription "
                "dosage. Please consult a qualified healthcare professional."
            )

            trajectory.append({
                "step": 2,
                "type": "scope_refusal",
            })

            return AgentResult(
                response=response,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # APPOINTMENT AVAILABILITY
        # -----------------------------

        if "available" in user_message or "availability" in user_message:

            tool_name = "check_availability"

            tool_calls.append({
                "name": tool_name,
                "arguments": {
                    "specialty": "Cardiology",
                    "date": "2026-09-21",
                },
            })

            trajectory.append({
                "step": 2,
                "type": "tool_call",
                "tool": tool_name,
            })

            result = self._safe_tool_call(
                "check_availability",
                specialty="Cardiology",
                date="2026-09-21",
            )

            tool_results.append({
                "tool": tool_name,
                "result": result,
            })

            trajectory.append({
                "step": 3,
                "type": "tool_result",
                "result": result,
            })

            if result.get("success", False):
                response = (
                    "There are available Cardiology appointments on "
                    "September 21 at 10:00, 14:00, and 16:00."
                )
            else:
                response = (
                    "I couldn't retrieve appointment availability."
                )

            return AgentResult(
                response=response,
                tool_calls=tool_calls,
                tool_results=tool_results,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # BOOKING
        # -----------------------------

        if "book" in user_message:

            tool_name = "book_appointment"

            tool_calls.append({
                "name": tool_name,
                "arguments": {
                    "patient_id": "P001",
                    "specialty": "Cardiology",
                    "date": "2026-09-21",
                    "time": "10:00",
                },
            })

            trajectory.append({
                "step": 2,
                "type": "tool_call",
                "tool": tool_name,
            })

            result = self._safe_tool_call(
                "book_appointment",
                patient_id="P001",
                specialty="Cardiology",
                date="2026-09-21",
                time="10:00",
            )

            tool_results.append({
                "tool": tool_name,
                "result": result,
            })

            trajectory.append({
                "step": 3,
                "type": "tool_result",
                "result": result,
            })

            if result.get("success", False):
                response = (
                    f"Your appointment has been booked successfully. "
                    f"Appointment ID: {result['appointment_id']}."
                )
            else:
                response = (
                    "The appointment could not be booked."
                )

            return AgentResult(
                response=response,
                tool_calls=tool_calls,
                tool_results=tool_results,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # CANCELLATION
        # -----------------------------

        if "cancel" in user_message:

            tool_name = "cancel_appointment"

            tool_calls.append({
                "name": tool_name,
                "arguments": {
                    "appointment_id": "A001",
                },
            })

            result = self._safe_tool_call(
                "cancel_appointment",
                appointment_id="A001",
            )

            tool_results.append({
                "tool": tool_name,
                "result": result,
            })

            trajectory.append({
                "step": 2,
                "type": "tool_call",
                "tool": tool_name,
            })

            trajectory.append({
                "step": 3,
                "type": "tool_result",
                "result": result,
            })

            if result.get("success", False):
                response = (
                    "Your appointment A001 has been cancelled."
                )
            else:
                response = (
                    "I couldn't cancel the appointment."
                )

            return AgentResult(
                response=response,
                tool_calls=tool_calls,
                tool_results=tool_results,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # RESCHEDULING
        # -----------------------------

        if "reschedule" in user_message or "move my appointment" in user_message:

            tool_name = "reschedule_appointment"

            tool_calls.append({
                "name": tool_name,
                "arguments": {
                    "appointment_id": "A001",
                    "new_date": "2026-09-21",
                    "new_time": "15:00",
                },
            })

            result = self._safe_tool_call(
                "reschedule_appointment",
                appointment_id="A001",
                new_date="2026-09-21",
                new_time="15:00",
            )

            tool_results.append({
                "tool": tool_name,
                "result": result,
            })

            trajectory.append({
                "step": 2,
                "type": "tool_call",
                "tool": tool_name,
            })

            trajectory.append({
                "step": 3,
                "type": "tool_result",
                "result": result,
            })

            if result.get("success", False):
                response = (
                    "Your appointment has been rescheduled to "
                    "September 21 at 15:00."
                )
            else:
                response = (
                    "I couldn't reschedule the appointment."
                )

            return AgentResult(
                response=response,
                tool_calls=tool_calls,
                tool_results=tool_results,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # DOCTOR INFORMATION
        # -----------------------------

        if (
            "doctor" in user_message
            or "doctors" in user_message
            or "cardiologist" in user_message
        ):

            tool_name = "get_doctor_information"

            tool_calls.append({
                "name": tool_name,
                "arguments": {
                    "specialty": "Cardiology",
                },
            })

            result = self.tools.get_doctor_information(
                specialty="Cardiology"
            )

            tool_results.append({
                "tool": tool_name,
                "result": result,
            })

            trajectory.append({
                "step": 2,
                "type": "tool_call",
                "tool": tool_name,
            })

            trajectory.append({
                "step": 3,
                "type": "tool_result",
                "result": result,
            })

            names = [
                d["name"]
                for d in result["doctors"]
            ]

            response = (
                "Available Cardiology doctors: "
                + ", ".join(names)
            )

            return AgentResult(
                response=response,
                tool_calls=tool_calls,
                tool_results=tool_results,
                latency_ms=(time.perf_counter() - start) * 1000,
                trajectory=trajectory,
            )

        # -----------------------------
        # DEFAULT
        # -----------------------------

        response = (
            "I can help with appointment availability, booking, "
            "cancellation, rescheduling and doctor information."
        )

        trajectory.append({
            "step": 2,
            "type": "general_response",
        })

        return AgentResult(
            response=response,
            latency_ms=(time.perf_counter() - start) * 1000,
            trajectory=trajectory,
        )