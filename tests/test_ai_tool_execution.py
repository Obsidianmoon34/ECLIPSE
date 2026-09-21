from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.ai_service import AIService
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_ai_tool_execution():
    state = EclipseState()

    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    ai = AIService()

    assistant = AssistantService(
        state,
        registry,
        ai_service=ai,
    )

    controller.glasses_put_on()

    # Ask the real AI model to select a device tool.
    response = ai.generate_with_tools(
        "Set my lens tint to 65%.",
        registry,
    )

    # Execute the model-generated tool request.
    results = assistant.execute_ai_tool_calls(
        response
    )

    assert len(results) == 1, (
        f"Expected one tool result, got: {results}"
    )

    result = results[0]

    assert result["type"] == "tool_result"
    assert result["tool_name"] == "set_lens_tint"
    assert result["result"]["success"] is True

    # Verify that the actual simulated device state changed.
    assert state.lens_tint_percent == 65
    assert state.auto_tint_enabled is False

    print(
        f"Selected tool: {result['tool_name']}"
    )

    print(
        f"Lens tint: {state.lens_tint_percent}%"
    )

    print(
        f"Execution result: {result['result']['message']}"
    )

    print(
        "\nAI tool execution test passed!"
    )


if __name__ == "__main__":
    test_ai_tool_execution()