from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_tool_definitions():
    state = EclipseState()
    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    definitions = registry.get_tool_definitions()

    assert len(definitions) == 1

    lens_tool = definitions[0]

    assert lens_tool["name"] == "set_lens_tint"

    parameters = lens_tool["parameters"]

    assert parameters["required"] == ["percent"]

    percent = parameters["properties"]["percent"]

    assert percent["type"] == "integer"
    assert percent["minimum"] == 0
    assert percent["maximum"] == 100

    # Verify that the definition corresponds to an executable tool.
    result = registry.execute_tool(
        "set_lens_tint",
        percent=40,
    )

    assert result["success"] is True
    assert state.lens_tint_percent == 40

    print("Tool definition test passed!")


if __name__ == "__main__":
    test_tool_definitions()