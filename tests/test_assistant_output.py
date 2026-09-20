from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_assistant_output():
    state = EclipseState()

    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(registry, controller)

    assistant = AssistantService(state, registry)

    controller.glasses_put_on()

    # Test a simulated AI tool request.
    result = assistant.process_assistant_output({
        "type": "tool_call",
        "name": "set_lens_tint",
        "arguments": {
            "percent": 40,
        },
    })

    assert result["type"] == "tool_result"
    assert result["result"]["success"] is True
    assert state.lens_tint_percent == 40

    # Test a simulated conversational response.
    response = assistant.process_assistant_output({
        "type": "text_response",
        "message": "The sky appears blue because of Rayleigh scattering.",
    })

    assert response["type"] == "text_response"
    assert "Rayleigh scattering" in response["message"]

    # Test an invalid tool request.
    invalid = assistant.process_assistant_output({
        "type": "tool_call",
        "name": "unknown_tool",
        "arguments": {},
    })

    assert invalid["type"] == "error"

    # Test an invalid output type.
    unknown = assistant.process_assistant_output({
        "type": "unsupported",
    })

    assert unknown["type"] == "error"

    print("Assistant output integration test passed!")


if __name__ == "__main__":
    test_assistant_output()