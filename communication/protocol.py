from models.system_state import EclipseState


PROTOCOL_VERSION = 1


def create_device_status(
    state: EclipseState,
    request_id: str,
) -> dict:
    return {
        "version": PROTOCOL_VERSION,
        "request_id": request_id,
        "type": "device_status",
        "data": {
            "battery_percent": state.battery_percent,
            "lens_tint_percent": state.lens_tint_percent,
            "auto_tint_enabled": state.auto_tint_enabled,
            "is_worn": state.is_worn,
            "phone_connected": state.phone.connected,
        },
    }


def create_command(
    request_id: str,
    name: str,
    arguments: dict,
) -> dict:
    if not request_id:
        raise ValueError("Request ID cannot be empty.")

    if not name:
        raise ValueError("Command name cannot be empty.")

    if not isinstance(arguments, dict):
        raise TypeError("Command arguments must be a dictionary.")

    return {
        "version": PROTOCOL_VERSION,
        "request_id": request_id,
        "type": "command",
        "name": name,
        "arguments": arguments,
    }


def create_command_result(
    request_id: str,
    name: str,
    success: bool,
    message: str,
) -> dict:
    return {
        "version": PROTOCOL_VERSION,
        "request_id": request_id,
        "type": "command_result",
        "name": name,
        "success": success,
        "message": message,
    }