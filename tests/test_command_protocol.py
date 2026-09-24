import json

from communication.protocol import (
    PROTOCOL_VERSION,
    create_command,
    create_command_result,
)


def test_command_protocol():
    command = create_command(
        request_id="phone-001",
        name="set_lens_tint",
        arguments={"percent": 65},
    )

    assert command["version"] == PROTOCOL_VERSION
    assert command["request_id"] == "phone-001"
    assert command["type"] == "command"
    assert command["name"] == "set_lens_tint"
    assert command["arguments"]["percent"] == 65

    result = create_command_result(
        request_id=command["request_id"],
        name=command["name"],
        success=True,
        message="Lens tint set to 65%.",
    )

    assert result["version"] == PROTOCOL_VERSION
    assert result["request_id"] == command["request_id"]
    assert result["type"] == "command_result"
    assert result["name"] == command["name"]
    assert result["success"] is True

    # Verify that both messages can be converted to JSON.
    assert json.loads(json.dumps(command)) == command
    assert json.loads(json.dumps(result)) == result

    print("Command protocol test passed!")


if __name__ == "__main__":
    test_command_protocol()