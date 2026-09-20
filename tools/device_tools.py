from app.eclipse_controller import EclipseController
from tools.tool_registry import ToolRegistry
from tools.tool_definitions import DEVICE_TOOL_DEFINITIONS


def register_device_tools(
    registry: ToolRegistry,
    controller: EclipseController,
):
    registry.register_tool(
        "set_lens_tint",
        controller.set_lens_tint,
    )

    for definition in DEVICE_TOOL_DEFINITIONS:
        registry.register_definition(definition)