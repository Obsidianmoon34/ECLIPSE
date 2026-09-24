from app.eclipse_controller import EclipseController
from communication.command_handler import CommandHandler
from communication.protocol import create_command
from models.system_state import EclipseState
from services.assistant_service import AssistantService
from tools.device_tools import register_device_tools
from tools.tool_registry import ToolRegistry


def test_command_handler():
    state = EclipseState()
    controller = EclipseController(state)

    registry = ToolRegistry()
    register_device_tools(registry, controller)

    assistant = AssistantService(
        state,
        registry,
    )

    handler = CommandHandler(assistant)

    # Simulate putting on the glasses.
    controller.glasses_put_on()

    # Simulate a lens tint command from the phone.
    command = create_command(
        request_id="phone-001",
        name="set_lens_tint",
        arguments={"percent": 65},
    )

    result = handler.handle_command(command)

    assert result["type"] == "command_result"
    assert result["request_id"] == "phone-001"
    assert result["success"] is True

    assert state.lens_tint_percent == 65
    assert state.auto_tint_enabled is False

    print("Lens tint command passed!")

    # Reject an unsupported command.
    unsupported = create_command(
        request_id="phone-002",
        name="delete_everything",
        arguments={},
    )

    result = handler.handle_command(unsupported)

    assert result["success"] is False
    assert result["message"] == "Command is not permitted."

    print("Unsupported command rejection passed!")

    # Reject an invalid tint percentage.
    invalid_tint = create_command(
        request_id="phone-003",
        name="set_lens_tint",
        arguments={"percent": 150},
    )

    result = handler.handle_command(invalid_tint)

    assert result["success"] is False
    assert state.lens_tint_percent == 65

    print("Invalid tint rejection passed!")

    # Reject an unsupported protocol version.
    invalid_version = create_command(
        request_id="phone-004",
        name="set_lens_tint",
        arguments={"percent": 30},
    )

    invalid_version["version"] = 999

    result = handler.handle_command(invalid_version)

    assert result["success"] is False
    assert state.lens_tint_percent == 65

    print("Protocol version rejection passed!")

    # Reject commands while the glasses are not worn.
    controller.glasses_removed()

    unworn_command = create_command(
        request_id="phone-005",
        name="set_lens_tint",
        arguments={"percent": 30},
    )

    result = handler.handle_command(unworn_command)

    assert result["success"] is False
    assert state.lens_tint_percent == 65

    print("Unworn device rejection passed!")

    print("\nCommand handler test passed!")


if __name__ == "__main__":
    test_command_handler()