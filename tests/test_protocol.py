import json

from communication.protocol import (
    PROTOCOL_VERSION,
    create_device_status,
)
from models.system_state import EclipseState


def test_device_status():
    state = EclipseState()

    state.battery_percent = 85
    state.lens_tint_percent = 65
    state.auto_tint_enabled = False

    message = create_device_status(
        state,
        request_id="test-001",
    )

    assert message["version"] == PROTOCOL_VERSION
    assert message["request_id"] == "test-001"
    assert message["type"] == "device_status"

    assert message["data"]["battery_percent"] == 85
    assert message["data"]["lens_tint_percent"] == 65
    assert message["data"]["auto_tint_enabled"] is False

    # Confirm that Android-compatible JSON can be generated.
    encoded = json.dumps(message)
    decoded = json.loads(encoded)

    assert decoded == message

    print("Device status protocol test passed!")


if __name__ == "__main__":
    test_device_status()