from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.assistant_router import AssistantRouter
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_assistant_router():
    state = EclipseState()

    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    router = AssistantRouter(registry)

    # Test a simulated AI tool selection.
    result = router.handle_tool_call(
        name="set_lens_tint",
        arguments={"percent": 40},
    )

    assert result["type"] == "tool_result"
    assert result["tool_name"] == "set_lens_tint"

    assert result["result"]["success"] is True
    assert state.lens_tint_percent == 40

    # Test a general conversational response.
    response = router.handle_text_response(
        "The sky appears blue because shorter "
        "wavelengths of sunlight scatter more "
        "strongly in Earth's atmosphere."
    )

    assert response["type"] == "text_response"

    assert "sky appears blue" in response["message"]

    # Test an unknown tool.
    invalid = router.handle_tool_call(
        name="unknown_tool",
        arguments={},
    )

    assert invalid["type"] == "error"

    print("Assistant router test passed!")


if __name__ == "__main__":
    test_assistant_router()