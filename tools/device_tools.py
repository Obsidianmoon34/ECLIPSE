from app.eclipse_controller import EclipseController
from tools.tool_registry import ToolRegistry


def register_device_tools(
    registry: ToolRegistry,
    controller: EclipseController,
):
    registry.register_tool(
        "set_lens_tint",
        controller.set_lens_tint,
    )