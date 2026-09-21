import json

from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from services.ai_service import AIService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_ai_tool_selection():
    state = EclipseState()
    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    ai = AIService()

    response = ai.generate_with_tools(
        "Set my lens tint to 65%.",
        registry,
    )

    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    assert len(tool_calls) == 1, (
        "Expected exactly one tool call."
    )

    tool_call = tool_calls[0]

    assert tool_call.name == "set_lens_tint"

    arguments = json.loads(
        tool_call.arguments
    )

    assert arguments["percent"] == 65

    # Tool selection must not execute the command.
    assert state.lens_tint_percent != 65

    print(
        f"Selected tool: {tool_call.name}"
    )

    print(
        f"Arguments: {arguments}"
    )

    print(
        "AI tool selection test passed!"
    )


if __name__ == "__main__":
    test_ai_tool_selection()