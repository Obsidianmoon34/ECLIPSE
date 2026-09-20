from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_assistant_tools():
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

    # Simulate putting the glasses on.
    controller.glasses_put_on()

    # Simulate the assistant selecting a tool.
    result = assistant.execute_tool(
        "set_lens_tint",
        percent=40,
    )

    assert result["success"] is True
    assert result["tint_percent"] == 40
    assert state.lens_tint_percent == 40
    assert state.auto_tint_enabled is False

    print("Assistant tool execution test passed!")


if __name__ == "__main__":
    test_assistant_tools()