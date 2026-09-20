from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_assistant_pipeline():
    state = EclipseState()

    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    assistant = AssistantService(
        state,
        registry,
    )

    controller.glasses_put_on()

    # Simulate an AI-generated device command.
    tool_result = assistant.process_assistant_output({
        "type": "tool_call",
        "name": "set_lens_tint",
        "arguments": {
            "percent": 40,
        },
    })

    assert tool_result["type"] == "tool_result"
    assert tool_result["result"]["success"] is True
    assert state.lens_tint_percent == 40

    # Simulate an AI-generated conversational answer.
    text_result = assistant.process_assistant_output({
        "type": "text_response",
        "message": "Hello! How can I help you?",
    })

    assert text_result["type"] == "text_response"
    assert text_result["message"] == "Hello! How can I help you?"

    # An invalid tool argument should not change the tint.
    invalid_result = assistant.process_assistant_output({
        "type": "tool_call",
        "name": "set_lens_tint",
        "arguments": {
            "percent": 150,
        },
    })

    assert invalid_result["type"] == "error"
    assert state.lens_tint_percent == 40

    print("Assistant pipeline test passed!")


if __name__ == "__main__":
    test_assistant_pipeline()