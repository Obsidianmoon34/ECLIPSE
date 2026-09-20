from app.eclipse_controller import EclipseController
from models.system_state import EclipseState
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_lens_tint():
    state = EclipseState()

    controller = EclipseController(state)

    registry = ToolRegistry()

    register_device_tools(
        registry,
        controller,
    )

    # Test a valid tint percentage
    result = registry.execute_tool(
        "set_lens_tint",
        percent=40,
    )

    assert result["success"] is True
    assert result["tint_percent"] == 40

    assert state.lens_tint_percent == 40
    assert state.auto_tint_enabled is False

    # Test the minimum tint percentage
    registry.execute_tool(
        "set_lens_tint",
        percent=0,
    )

    assert state.lens_tint_percent == 0

    # Test the maximum tint percentage
    registry.execute_tool(
        "set_lens_tint",
        percent=100,
    )

    assert state.lens_tint_percent == 100

    # Test an invalid tint percentage
    try:
        registry.execute_tool(
            "set_lens_tint",
            percent=150,
        )

    except ValueError:
        pass

    else:
        raise AssertionError(
            "Invalid tint percentage was accepted."
        )
    
    assert state.lens_tint_percent == 100

    print("Lens tint tool test passed!")


if __name__ == "__main__":
    test_lens_tint()